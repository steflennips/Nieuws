"""Acceptatietests US-009 (echte nieuwsfeeds ophalen en opslaan), met lokale testfeeds (geen internet).

c7 (echte ophaalronde door de Bouwer) toetst hier alleen het formaat van de uitvoer; de echte ronde
zelf is apart uitgevoerd en staat in het testrapport.
"""
import os
import re
import subprocess
import sys
import time
import unittest
import urllib.request

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hulp_statisch as hs  # noqa: E402  (verwacht_getoond: het AI-plafond van de app, it. 6)
from hulp_feeds import (ROOT, SRC, FeedServer, atom_feed, rss_feed, iso_dag, lees_json,  # noqa: E402
                        omgeving, project_config, run_ophalen, schrijf_config, tmp_map, vrije_poort,
                        vandaag)
import shutil  # noqa: E402

CONFIG_PAD = None  # niet gebruikt; configs worden per test in een eigen map geschreven


def feeds_met_server(base):
    return [
        {"naam": "Testfeed RSS", "url": base + "/rss.xml", "taal": "nl"},
        {"naam": "Testfeed Atom", "url": base + "/atom.xml", "taal": "en"},
    ]


def standaard_routes():
    return {"/rss.xml": {"body": rss_feed}, "/atom.xml": {"body": atom_feed}}


def lees_uitvoer(res):
    return res.stdout + res.stderr


class TestUS009(unittest.TestCase):
    def setUp(self):
        self.tmp = tmp_map()
        self.uit = os.path.join(self.tmp, "nieuws.json")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    # c1: configuratie
    def test_US009_c1_config_8_tot_10_feeds_minstens_3_nl_en_met_naam_url_taal(self):
        cfg = project_config()
        feeds = cfg["feeds"]
        self.assertGreaterEqual(len(feeds), 8)
        self.assertLessEqual(len(feeds), 10)
        self.assertGreaterEqual(len([f for f in feeds if f.get("taal") == "nl"]), 3, "minstens 3 Nederlandse feeds")
        self.assertGreaterEqual(len([f for f in feeds if f.get("taal") == "en"]), 3, "minstens 3 Engelse feeds")
        for f in feeds:
            self.assertTrue(f.get("naam"), f)
            self.assertRegex(f.get("url", ""), r"^https://", f)
            self.assertIn(f.get("taal"), ("nl", "en"), f)
        self.assertEqual(len({f["url"] for f in feeds}), len(feeds), "dubbele feed-URL in config")
        self.assertLessEqual(cfg.get("timeout_seconden", 99), 15, "time-out moet maximaal 15 s zijn (US-011)")

    # c2: RSS 2.0 en Atom
    def test_US009_c2_rss_en_atom_velden_opgeslagen(self):
        with FeedServer(standaard_routes()) as srv:
            cfg = schrijf_config(os.path.join(self.tmp, "cfg.json"), feeds_met_server(srv.base))
            res = run_ophalen(cfg, self.uit)
        self.assertEqual(res.returncode, 0, lees_uitvoer(res))
        items = {i["url"]: i for i in lees_json(self.uit)["items"]}
        rss = items[srv.base + "/artikel/1?a=1&b=2"]
        self.assertEqual(rss["titel"], "Nieuwe AI-tool voor kantoren")
        self.assertEqual(rss["samenvatting"], "Een korte tekst met .")
        self.assertEqual(rss["datum"], iso_dag(2))
        self.assertEqual(rss["bron"], "Testfeed RSS")
        self.assertEqual(rss["taal"], "nl")
        atom = items[srv.base + "/atom/1"]
        self.assertEqual(atom["titel"], "Machine learning in de praktijk")
        self.assertEqual(atom["samenvatting"], "Samenvatting & meer over modellen")
        self.assertEqual(atom["datum"], iso_dag(1))
        self.assertEqual(atom["bron"], "Testfeed Atom")
        self.assertEqual(atom["taal"], "en")
        self.assertIn(srv.base + "/atom/2", items, "Atom-link zonder rel moet ook werken")

    # c3: platte tekst, max 300 tekens, geen afbeeldingen of volle inhoud
    def test_US009_c3_html_en_lange_tekst_platte_samenvatting_max_300(self):
        with FeedServer(standaard_routes()) as srv:
            cfg = schrijf_config(os.path.join(self.tmp, "cfg.json"), feeds_met_server(srv.base))
            run_ophalen(cfg, self.uit)
        items = lees_json(self.uit)["items"]
        self.assertTrue(items)
        for i in items:
            s = i["samenvatting"]
            self.assertLessEqual(len(s), 300, i["url"])
            self.assertNotRegex(s, r"<[a-zA-Z/!]", "HTML in samenvatting: " + i["url"])
            self.assertNotIn("x.jpg", s)
            self.assertEqual(set(i.keys()), {"id", "titel", "categorie", "bron", "taal", "datum", "samenvatting", "url"},
                             "onverwachte velden (volledige inhoud of afbeeldingen opgeslagen?)")
        lang = [i for i in items if i["url"].endswith("/artikel/2")][0]
        self.assertGreaterEqual(len(lang["samenvatting"]), 290, "lange tekst moet tot dicht bij 300 tekens worden afgekapt")
        self.assertTrue(lang["samenvatting"].endswith("..."))

    # c4: geen dubbelen
    def test_US009_c4_zelfde_link_staat_maar_een_keer(self):
        with FeedServer(standaard_routes()) as srv:
            cfg = schrijf_config(os.path.join(self.tmp, "cfg.json"), feeds_met_server(srv.base))
            self.assertEqual(run_ophalen(cfg, self.uit).returncode, 0)
            eerste = lees_json(self.uit)["items"]
            self.assertEqual(run_ophalen(cfg, self.uit).returncode, 0)
            tweede = lees_json(self.uit)["items"]
        self.assertEqual(len(tweede), len(eerste))
        urls = [i["url"] for i in tweede]
        self.assertEqual(len(urls), len(set(urls)), "dubbele links na tweede ophaalronde")
        self.assertEqual(urls.count(srv.base + "/artikel/1?a=1&b=2"), 1)

    # c5: ouder dan 60 dagen verwijderd
    def test_US009_c5_items_ouder_dan_60_dagen_worden_verwijderd(self):
        def oud(url, dagen):
            return {"id": "x" + str(dagen), "titel": "Oud AI-artikel", "categorie": "AI", "bron": "Testfeed RSS",
                    "taal": "nl", "datum": iso_dag(dagen), "samenvatting": "Test", "url": url}
        with FeedServer(standaard_routes()) as srv:
            seed = {"items": [oud(srv.base + "/oud/61", 61), oud(srv.base + "/recent/59", 59)]}
            import json
            with open(self.uit, "w", encoding="utf-8") as f:
                json.dump(seed, f)
            cfg = schrijf_config(os.path.join(self.tmp, "cfg.json"), feeds_met_server(srv.base))
            res = run_ophalen(cfg, self.uit)
        self.assertEqual(res.returncode, 0, lees_uitvoer(res))
        urls = {i["url"] for i in lees_json(self.uit)["items"]}
        self.assertNotIn(srv.base + "/oud/61", urls, "item van 61 dagen oud is niet verwijderd")
        self.assertIn(srv.base + "/recent/59", urls, "item van 59 dagen oud is ten onrechte verwijderd")
        for i in lees_json(self.uit)["items"]:
            self.assertGreaterEqual(i["datum"], iso_dag(60), i["url"])

    # c6: de gebouwde statische site (Nieuws) toont de opgehaalde items, nieuwste eerst, met werkende link.
    # Iteratie 7: was "de app" (src/app.py verwijderd); de criteria blijven gelden op de statische site (US-009 c6).
    def test_US009_c6_site_toont_opgehaalde_items_nieuwste_eerst_met_link(self):
        import html as htmllib
        import re as _re
        with FeedServer(standaard_routes()) as srv:
            cfg = schrijf_config(os.path.join(self.tmp, "cfg.json"), feeds_met_server(srv.base))
            self.assertEqual(run_ophalen(cfg, self.uit).returncode, 0)
        site = os.path.join(self.tmp, "site")
        rc, out, err = hs.bouw(site, data=self.uit, vandaag=vandaag().isoformat())
        self.assertEqual(rc, 0, out + err)
        na = hs.lees(os.path.join(site, "nieuws.html"))
        self.assertNotIn("Voorbeeld", na, "na het ophalen mogen voorbeeldartikelen niet meer zichtbaar zijn")
        items = hs.verwacht_getoond(lees_json(self.uit)["items"])
        self.assertIn('<p class="aantal" id="aantal">%d ' % len(items), na)
        links = _re.findall(r'<article class="kaart"[^>]*><h2><a href="([^"]*)" target="_blank"', na)
        self.assertEqual(sorted(htmllib.unescape(h) for h in links), sorted(i["url"] for i in items))
        datums = _re.findall(r'<span>(\d+ \w+ \d{4})</span></div>', na)
        self.assertEqual(len(datums), len(items))
        # nieuwste eerst: de volgorde van de kaarten is aflopend op datum
        maanden = ["jan", "feb", "mrt", "apr", "mei", "jun", "jul", "aug", "sep", "okt", "nov", "dec"]
        sleutels = []
        for d, m, j in _re.findall(r'<span>(\d+) (\w+) (\d{4})</span></div>', na):
            sleutels.append((int(j), maanden.index(m.lower()) + 1, int(d)))
        self.assertEqual(sleutels, sorted(sleutels, reverse=True), "Nieuws is niet nieuwste eerst")

    # c7: per feed het aantal opgehaalde items in de uitvoer
    def test_US009_c7_uitvoer_toont_per_feed_aantal_items(self):
        with FeedServer(standaard_routes()) as srv:
            cfg = schrijf_config(os.path.join(self.tmp, "cfg.json"), feeds_met_server(srv.base))
            res = run_ophalen(cfg, self.uit)
        regels = res.stdout.splitlines()
        rss = [r for r in regels if r.startswith("OK    Testfeed RSS:")]
        atom = [r for r in regels if r.startswith("OK    Testfeed Atom:")]
        self.assertEqual(len(rss), 1, res.stdout)
        self.assertEqual(len(atom), 1, res.stdout)
        self.assertRegex(rss[0], r"Testfeed RSS: 4 items in feed, \d+ bewaard")
        self.assertRegex(atom[0], r"Testfeed Atom: 2 items in feed, \d+ bewaard")
        self.assertTrue(any(r.startswith("Totaal opgeslagen:") for r in regels))

    # Aanvullend (robots.txt, opdrachtvereiste): een disallow wordt gerespecteerd.
    def test_US009_extra_robots_txt_gerespecteerd(self):
        routes = standaard_routes()
        routes["/robots.txt"] = {"body": b"User-agent: *\nDisallow: /geblokkeerd/\n", "ctype": "text/plain"}
        routes["/geblokkeerd/feed.xml"] = {"body": rss_feed}
        with FeedServer(routes) as srv:
            feeds = feeds_met_server(srv.base) + [{"naam": "Geblokkeerd", "url": srv.base + "/geblokkeerd/feed.xml", "taal": "nl"}]
            cfg = schrijf_config(os.path.join(self.tmp, "cfg.json"), feeds)
            res = run_ophalen(cfg, self.uit)
            opgevraagd = list(srv.opgevraagd)
        self.assertEqual(res.returncode, 0, lees_uitvoer(res))
        self.assertIn("FOUT  Geblokkeerd: niet toegestaan volgens robots.txt", res.stdout)
        self.assertNotIn("/geblokkeerd/feed.xml", opgevraagd, "een door robots.txt verboden feed is toch opgevraagd")
        urls = [i["url"] for i in lees_json(self.uit)["items"]]
        self.assertFalse(any("/geblokkeerd/" in u for u in urls))


if __name__ == "__main__":
    unittest.main()
