"""Acceptatietests US-011 (foutafhandeling bij uitgevallen feed), met lokale testfeeds (geen internet).

Feeds die niet bereikbaar zijn, een time-out geven of ongeldige XML leveren, worden nagebootst met een
gesloten poort, een trage route en een kapotte route op de lokale testserver.
"""
import json
import os
import shutil
import sys
import time
import unittest
from datetime import datetime, timezone

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from hulp_feeds import (FeedServer, HTML_PAGINA, KAPOT_XML, atom_feed, iso_dag, lees_json,  # noqa: E402
                        rss_feed, run_ophalen, schrijf_config, tmp_map, vrije_poort)


def routes_basis():
    return {
        "/rss.xml": {"body": rss_feed},
        "/atom.xml": {"body": atom_feed},
        "/kapot.xml": {"body": KAPOT_XML, "ctype": "application/xml"},
        "/html.xml": {"body": HTML_PAGINA, "ctype": "text/html"},
        "/traag.xml": {"body": rss_feed, "delay": 4},
    }


class TestUS011(unittest.TestCase):
    def setUp(self):
        self.tmp = tmp_map()
        self.uit = os.path.join(self.tmp, "nieuws.json")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _feeds(self, base, dood_poort):
        return [
            {"naam": "Dode feed", "url": "http://127.0.0.1:%d/feed.xml" % dood_poort, "taal": "nl"},
            {"naam": "Kapotte feed", "url": base + "/kapot.xml", "taal": "nl"},
            {"naam": "Geen feed", "url": base + "/html.xml", "taal": "nl"},
            {"naam": "Trage feed", "url": base + "/traag.xml", "taal": "en"},
            {"naam": "Testfeed RSS", "url": base + "/rss.xml", "taal": "nl"},
            {"naam": "Testfeed Atom", "url": base + "/atom.xml", "taal": "en"},
        ]

    # c1: uitgevallen feeds breken de rest niet; time-out na korte tijd (config 1 s, project max 15 s)
    def test_US011_c1_uitgevallen_feeds_laten_de_rest_doorgaan(self):
        dood = vrije_poort()
        with FeedServer(routes_basis()) as srv:
            cfg = schrijf_config(os.path.join(self.tmp, "cfg.json"), self._feeds(srv.base, dood), timeout=1)
            start = time.time()
            res = run_ophalen(cfg, self.uit)
            duur = time.time() - start
            items = lees_json(self.uit)["items"]
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
        self.assertLess(duur, 30, "ophalen duurde te lang: %.1f s" % duur)
        bronnen = {i["bron"] for i in items}
        self.assertIn("Testfeed RSS", bronnen, res.stdout)
        self.assertIn("Testfeed Atom", bronnen, res.stdout)
        self.assertIn("FOUT  Dode feed", res.stdout)
        self.assertIn("FOUT  Kapotte feed: ongeldige XML", res.stdout)
        self.assertIn("FOUT  Geen feed: geen feed (HTML-pagina ontvangen)", res.stdout)
        self.assertIn("FOUT  Trage feed: niet bereikbaar of time-out", res.stdout)

    # c2: een mislukte feed houdt eerder opgeslagen items van die feed
    def test_US011_c2_eerder_opgeslagen_items_van_mislukte_feed_blijven_staan(self):
        dood = vrije_poort()
        bewaard = {"id": "abc123def456", "titel": "Eerder opgehaald AI-artikel", "categorie": "AI",
                   "bron": "Dode feed", "taal": "nl", "datum": iso_dag(3), "samenvatting": "Test",
                   "url": "http://127.0.0.1:%d/oud/artikel" % dood}
        with open(self.uit, "w", encoding="utf-8") as f:
            json.dump({"items": [bewaard]}, f)
        with FeedServer(routes_basis()) as srv:
            cfg = schrijf_config(os.path.join(self.tmp, "cfg.json"), self._feeds(srv.base, dood), timeout=1)
            res = run_ophalen(cfg, self.uit)
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
        items = {i["url"]: i for i in lees_json(self.uit)["items"]}
        self.assertIn(bewaard["url"], items, "item van de mislukte feed is verdwenen")
        self.assertEqual(items[bewaard["url"]], bewaard, "item van de mislukte feed is gewijzigd")

    # c3: per feed OK of FOUT met korte reden
    def test_US011_c3_uitvoer_toont_ok_of_fout_met_reden_per_feed(self):
        dood = vrije_poort()
        with FeedServer(routes_basis()) as srv:
            cfg = schrijf_config(os.path.join(self.tmp, "cfg.json"), self._feeds(srv.base, dood), timeout=1)
            res = run_ophalen(cfg, self.uit)
        regels = [r for r in res.stdout.splitlines() if r.startswith(("OK ", "FOUT "))]
        self.assertEqual(len(regels), 6, res.stdout)
        for naam in ["Dode feed", "Kapotte feed", "Geen feed", "Trage feed"]:
            regel = [r for r in regels if r.startswith("FOUT  " + naam + ":")]
            self.assertEqual(len(regel), 1, naam)
            reden = regel[0].split(":", 1)[1].strip()
            self.assertTrue(len(reden) > 3, "geen reden bij %s" % naam)
        for naam in ["Testfeed RSS", "Testfeed Atom"]:
            self.assertTrue(any(r.startswith("OK    " + naam + ":") for r in regels), naam)

    # c4: alle feeds mislukt -> bestand ongewijzigd en foutcode (niet 0); minstens een OK -> 0
    def test_US011_c4_alle_feeds_mislukt_laat_bestand_ongewijzigd_met_foutcode(self):
        origineel = b'{"bijgewerkt": "2026-10-01T00:00:00+00:00", "feeds": [], "items": []}\n'
        with open(self.uit, "wb") as f:
            f.write(origineel)
        dood1, dood2 = vrije_poort(), vrije_poort()
        with FeedServer({"/kapot.xml": {"body": KAPOT_XML}}) as srv:
            feeds = [{"naam": "Dode A", "url": "http://127.0.0.1:%d/x.xml" % dood1, "taal": "nl"},
                     {"naam": "Dode B", "url": "http://127.0.0.1:%d/y.xml" % dood2, "taal": "en"},
                     {"naam": "Kapot", "url": srv.base + "/kapot.xml", "taal": "en"}]
            cfg = schrijf_config(os.path.join(self.tmp, "cfg.json"), feeds, timeout=1)
            res = run_ophalen(cfg, self.uit)
        self.assertNotEqual(res.returncode, 0, "bij alleen mislukte feeds moet de foutcode niet 0 zijn")
        self.assertIn("blijft ongewijzigd", res.stdout)
        with open(self.uit, "rb") as f:
            self.assertEqual(f.read(), origineel, "bestand is gewijzigd terwijl alle feeds mislukten")

    def test_US011_c4_alle_feeds_mislukt_zonder_bestaand_bestand_maakt_geen_bestand(self):
        dood = vrije_poort()
        cfg = schrijf_config(os.path.join(self.tmp, "cfg.json"),
                             [{"naam": "Dode", "url": "http://127.0.0.1:%d/x.xml" % dood, "taal": "nl"}], timeout=1)
        res = run_ophalen(cfg, self.uit)
        self.assertNotEqual(res.returncode, 0)
        self.assertFalse(os.path.exists(self.uit), "er is een uitvoerbestand gemaakt terwijl niets is opgehaald")

    def test_US011_c4_minstens_een_geslaagde_feed_geeft_foutcode_0(self):
        dood = vrije_poort()
        with FeedServer(routes_basis()) as srv:
            feeds = [{"naam": "Dode", "url": "http://127.0.0.1:%d/x.xml" % dood, "taal": "nl"},
                     {"naam": "Testfeed RSS", "url": srv.base + "/rss.xml", "taal": "nl"}]
            cfg = schrijf_config(os.path.join(self.tmp, "cfg.json"), feeds, timeout=1)
            res = run_ophalen(cfg, self.uit)
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
        self.assertTrue(lees_json(self.uit)["items"])

    # c5: item zonder titel wordt overgeslagen; item zonder datum krijgt de ophaaldatum; het ophalen stopt niet
    def test_US011_c5_item_zonder_titel_overgeslagen_zonder_datum_krijgt_ophaaldatum(self):
        def feed(base):
            return ('<?xml version="1.0"?><rss version="2.0"><channel>'
                    '<item><title></title><link>%(b)s/geen-titel</link><description>AI</description>'
                    '<pubDate>Mon, 05 Oct 2026 10:00:00 GMT</pubDate></item>'
                    '<item><title>Zonder datum over automatisering</title><link>%(b)s/geen-datum</link>'
                    '<description>Workflows</description></item>'
                    '<item><title>Met datum over data</title><link>%(b)s/met-datum</link>'
                    '<description>SQL</description><pubDate>Mon, 05 Oct 2026 10:00:00 GMT</pubDate></item>'
                    '</channel></rss>' % {"b": base}).encode("utf-8")
        with FeedServer({"/f.xml": {"body": feed}}) as srv:
            cfg = schrijf_config(os.path.join(self.tmp, "cfg.json"),
                                 [{"naam": "Randgevallen", "url": srv.base + "/f.xml", "taal": "nl"}])
            res = run_ophalen(cfg, self.uit)
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
        items = {i["url"].rsplit("/", 1)[1]: i for i in lees_json(self.uit)["items"]}
        self.assertNotIn("geen-titel", items, "item zonder titel is ten onrechte opgeslagen")
        self.assertIn("met-datum", items, "ophalen stopte na het item zonder titel")
        self.assertEqual(items["met-datum"]["datum"], "2026-10-05")
        vandaag = datetime.now(timezone.utc).date().isoformat()
        self.assertIn("geen-datum", items, "item zonder datum is niet opgeslagen")
        self.assertEqual(items["geen-datum"]["datum"], vandaag, "item zonder datum moet de ophaaldatum krijgen")


if __name__ == "__main__":
    unittest.main()
