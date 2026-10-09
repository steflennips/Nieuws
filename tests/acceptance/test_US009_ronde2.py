"""Gerichte controles na fixronde 1 van iteratie 3 (testrapport iteratie-3-ronde-1.md, bevindingen 1, 3, 4).

Alle tests draaien src/ophalen.py tegen lokale testfeeds (geen internet). Het ophalen schrijft alleen naar een
tijdelijke map.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import unittest

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from hulp_feeds import (SRC, FeedServer, iso_dag, lees_json, rfc, rss_feed,  # noqa: E402
                        run_ophalen, schrijf_config, tmp_map)


def oud_feed(base):
    """Feed met uitsluitend verouderde items (ouder dan 60 dagen), zoals de verouderde Tweakers-feed."""
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0"><channel><title>Oude feed</title>'
        '<item><title>Oud AI-nieuws een</title><link>%(b)s/oud/1</link><description>AI</description><pubDate>%(d1)s</pubDate></item>'
        '<item><title>Oud AI-nieuws twee</title><link>%(b)s/oud/2</link><description>AI</description><pubDate>%(d2)s</pubDate></item>'
        '<item><title>Oud AI-nieuws drie</title><link>%(b)s/oud/3</link><description>AI</description><pubDate>%(d3)s</pubDate></item>'
        '</channel></rss>' % {"b": base, "d1": rfc(100), "d2": rfc(90), "d3": rfc(70)})


def gemengd_feed(base):
    """Drie verouderde items en een recent AI-item."""
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0"><channel><title>Gemengde feed</title>'
        '<item><title>Oud AI-nieuws een</title><link>%(b)s/gem/1</link><description>AI</description><pubDate>%(d1)s</pubDate></item>'
        '<item><title>Oud AI-nieuws twee</title><link>%(b)s/gem/2</link><description>AI</description><pubDate>%(d2)s</pubDate></item>'
        '<item><title>Oud AI-nieuws drie</title><link>%(b)s/gem/3</link><description>AI</description><pubDate>%(d3)s</pubDate></item>'
        '<item><title>Nieuwe AI-agent in de praktijk</title><link>%(b)s/gem/4</link><description>AI</description><pubDate>%(d4)s</pubDate></item>'
        '</channel></rss>' % {"b": base, "d1": rfc(100), "d2": rfc(90), "d3": rfc(70), "d4": rfc(1)})


def regel_van(stdout, naam):
    regels = [r for r in stdout.splitlines() if r.startswith(("OK ", "FOUT")) and (" %s:" % naam) in r]
    return regels


class TestUS009Ronde2(unittest.TestCase):
    def setUp(self):
        self.tmp = tmp_map()
        self.uit = os.path.join(self.tmp, "nieuws.json")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    # Bevinding 1 (ronde 1): "bewaard" telt na het leeftijdsfilter; verouderd apart; uitvoer en JSON kloppen.
    def test_US009_c7_bewaard_na_leeftijdsfilter_verouderd_apart_en_consistent_met_json(self):
        routes = {"/gem.xml": {"body": gemengd_feed}, "/rss.xml": {"body": rss_feed}}
        with FeedServer(routes) as srv:
            feeds = [{"naam": "Gemengde feed", "url": srv.base + "/gem.xml", "taal": "en"},
                     {"naam": "Testfeed RSS", "url": srv.base + "/rss.xml", "taal": "nl"}]
            cfg = schrijf_config(os.path.join(self.tmp, "cfg.json"), feeds)
            res = run_ophalen(cfg, self.uit)
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
        gem = regel_van(res.stdout, "Gemengde feed")
        self.assertEqual(len(gem), 1, res.stdout)
        self.assertRegex(gem[0], r"Gemengde feed: 4 items in feed, 1 bewaard \(1 nieuw\), 3 verouderd, ",
                         "bewaard moet na het leeftijdsfilter tellen en verouderde items apart melden")
        d = lees_json(self.uit)
        st = {f["feed"]: f for f in d["feeds"]}
        self.assertEqual((st["Gemengde feed"]["items"], st["Gemengde feed"]["bewaard"], st["Gemengde feed"]["verouderd"]),
                         (4, 1, 3), "feeds-status in JSON komt niet overeen met de uitvoer")
        per_bron = {}
        for i in d["items"]:
            per_bron[i["bron"]] = per_bron.get(i["bron"], 0) + 1
        for naam, f in st.items():
            if f["status"] == "OK":
                self.assertEqual(per_bron.get(naam, 0), f["bewaard"],
                                 "aantal items in JSON (%s) wijkt af van 'bewaard' in feeds-status" % naam)
        totaal = [r for r in res.stdout.splitlines() if r.startswith("Totaal opgeslagen:")]
        self.assertEqual(len(totaal), 1, res.stdout)
        self.assertIn("Totaal opgeslagen: %d items" % len(d["items"]), totaal[0],
                      "totaal in de uitvoer wijkt af van het aantal items in het JSON-bestand")
        for i in d["items"]:
            self.assertGreaterEqual(i["datum"], iso_dag(60), "verouderd item staat in het JSON-bestand: " + i["url"])
        self.assertNotIn(srv.base + "/gem/1", {i["url"] for i in d["items"]})

    # Bevinding 1 (ronde 1): een feed met alleen verouderde items is OK met 0 bewaard, geen spook-telling.
    def test_US009_c7_feed_met_alleen_verouderde_items_is_ok_met_nul_bewaard(self):
        with FeedServer({"/oud.xml": {"body": oud_feed}, "/rss.xml": {"body": rss_feed}}) as srv:
            feeds = [{"naam": "Oude feed", "url": srv.base + "/oud.xml", "taal": "en"},
                     {"naam": "Testfeed RSS", "url": srv.base + "/rss.xml", "taal": "nl"}]
            cfg = schrijf_config(os.path.join(self.tmp, "cfg.json"), feeds)
            res = run_ophalen(cfg, self.uit)
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
        oud = regel_van(res.stdout, "Oude feed")
        self.assertEqual(len(oud), 1, res.stdout)
        self.assertRegex(oud[0], r"^OK    Oude feed: 3 items in feed, 0 bewaard \(0 nieuw\), 3 verouderd, ")
        d = lees_json(self.uit)
        st = [f for f in d["feeds"] if f["feed"] == "Oude feed"][0]
        self.assertEqual((st["status"], st["items"], st["bewaard"], st["verouderd"]), ("OK", 3, 0, 3))
        self.assertFalse([i for i in d["items"] if i["bron"] == "Oude feed"],
                         "items van een feed met alleen verouderde items mogen niet in het JSON-bestand staan")

    # Bevinding 3 (ronde 1): dubbel ge-escapete entiteiten worden niet nog eens gedecodeerd (functieniveau).
    def test_US009_c3_platte_tekst_decodeert_entiteiten_niet_dubbel(self):
        code = ("import sys; sys.path.insert(0, %r); import ophalen; "
                "sys.stdout.write(ophalen.platte_tekst('Tom &amp;amp; Jerry'))" % SRC)
        res = subprocess.run([sys.executable, "-B", "-I", "-c", code], capture_output=True, text=True,
                             encoding="utf-8", timeout=30)
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertEqual(res.stdout, "Tom &amp; Jerry")

    # Bevinding 4 (ronde 1): ongeldige of ontbrekende config geeft een nette melding, geen traceback.
    def test_US009_extra_ongeldige_config_geeft_nette_fout_exitcode_2(self):
        ontbreekt = os.path.join(self.tmp, "bestaat-niet.json")
        kapot = os.path.join(self.tmp, "kapot.json")
        with open(kapot, "w", encoding="utf-8") as f:
            f.write("{geen geldige json")
        zonder_feeds = os.path.join(self.tmp, "zonder_feeds.json")
        with open(zonder_feeds, "w", encoding="utf-8") as f:
            json.dump({"trefwoorden": {}, "user_agent": "x"}, f)
        for pad in (ontbreekt, kapot, zonder_feeds):
            with self.subTest(config=os.path.basename(pad)):
                res = run_ophalen(pad, self.uit)
                self.assertEqual(res.returncode, 2, res.stdout + res.stderr)
                self.assertNotIn("Traceback", res.stderr)
                self.assertTrue(res.stderr.startswith("FOUT:"), res.stderr)
                self.assertFalse(os.path.exists(self.uit), "bij een ongeldige config mag er geen uitvoer ontstaan")


if __name__ == "__main__":
    unittest.main()
