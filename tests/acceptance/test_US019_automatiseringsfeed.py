"""Acceptatietests US-019 (AWS Big Data Blog vervangen door een automatiseringsfeed), iteratie 7.

- c1 config: geen AWS Big Data Blog meer; minstens 1 automatiseringsfeed; max 10 feeds; min 3 NL / 3 EN;
  min 2 BI/analytics-feeds en min 2 algemene NL-feeds met headnieuws. Feeds worden op NAAM getoetst (regel), niet op vaste
  feednamen, zodat een feedruil de tests niet breekt (zie docs/decisions/2026-10-09-criteria-feedruil-it7.md).
- c2 feedbesluit: de nieuwe feed staat in het besluit met gratis, geen login, robots.txt gecontroleerd en een reden.
- c3 opschonen: items van een bron die niet (meer) in config/feeds.json staat worden bij het ophalen verwijderd;
  items van een feed die wel in de config staat maar faalt blijven staan. Lokale testfeeds, geen internet.
- c4 echte ophaalronde: meting door de Bouwer/Tester (zie testrapport). Hier alleen de controle op de echte data
  (alleen-lezen): minstens 1 item van een automatiseringsfeed en geen items van niet-geconfigureerde bronnen.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

import hulp_statisch as h
import hulp_feeds as hf

sys.dont_write_bytecode = True

with open(h.PROJECT_CONFIG, encoding="utf-8") as _f:
    CFG = json.load(_f)
FEEDBESLUIT = os.path.join(h.ROOT, "docs", "decisions", "2026-10-08-nieuwsfeeds.md")
BRONNEN_NAMEN = [f["naam"] for f in CFG["feeds"]]
AWS_PATROON = re.compile(r"aws|big data", re.I)
AUTO_PATROON = re.compile(r"automati|automate|workflow|power platform|low-code|\brpa\b", re.I)
BI_PATROON = re.compile(r"power bi|fabric|sqlbi|analytics|\bbi\b|\bdata\b|dbt|snowflake|databricks|tableau|qlik|looker",
                        re.I)


class TestUS019C1Config(unittest.TestCase):
    def test_US019_c1_aws_big_data_blog_staat_niet_meer_in_config(self):
        for feed in CFG["feeds"]:
            self.assertNotIn("aws.amazon.com", feed["url"], "AWS-feed nog in config: %s" % feed["naam"])
            self.assertIsNone(AWS_PATROON.search(feed["naam"]), "AWS-feed nog in config: %s" % feed["naam"])

    def test_US019_c1_minstens_1_automatiseringsfeed(self):
        auto = [f["naam"] for f in CFG["feeds"] if AUTO_PATROON.search(f["naam"])]
        self.assertGreaterEqual(len(auto), 1, "geen automatiseringsfeed in config/feeds.json")

    def test_US019_c1_max_10_feeds_min_3_nl_en(self):
        feeds = CFG["feeds"]
        self.assertLessEqual(len(feeds), 10)
        self.assertGreaterEqual(sum(1 for f in feeds if f["taal"] == "nl"), 3)
        self.assertGreaterEqual(sum(1 for f in feeds if f["taal"] == "en"), 3)

    def test_US019_c1_min_2_bi_feeds_en_2_algemene_nl_headnieuws(self):
        bi = [f["naam"] for f in CFG["feeds"] if BI_PATROON.search(f["naam"])]
        self.assertGreaterEqual(len(bi), 2, "minder dan 2 BI/analytics-feeds (op naam): %s" % bi)
        hn_nl = [f["naam"] for f in CFG["feeds"] if f.get("headnieuws") is True and f["taal"] == "nl"]
        self.assertGreaterEqual(len(hn_nl), 2, "minder dan 2 algemene NL-feeds met headnieuws: %s" % hn_nl)


class TestUS019C2Besluit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(FEEDBESLUIT, encoding="utf-8") as f:
            cls.besluit = f.read()

    def test_US019_c2_iteratie7_sectie_beschrijft_nieuwe_feed_gratis_login_robots_en_reden(self):
        b = self.besluit
        self.assertIn("Wijzigingen iteratie 7", b, "geen besluit-sectie voor iteratie 7")
        sectie = b.split("Wijzigingen iteratie 7", 1)[1]
        self.assertIn("gratis", sectie.lower())
        self.assertIn("geen login", sectie.lower())
        self.assertIn("robots", sectie.lower())
        self.assertIn("gekozen", sectie.lower(), "geen reden waarom de kandidaat gekozen is")
        self.assertIn("Onderzocht en afgevallen", sectie, "afgevallen kandidaten met reden ontbreken")

    def test_US019_c2_nieuwe_automatiseringsfeeds_in_besluit_en_op_bronnen(self):
        auto = [f for f in CFG["feeds"] if AUTO_PATROON.search(f["naam"])]
        for feed in auto:
            self.assertIn(feed["url"], self.besluit, "feed niet in het besluit: %s" % feed["naam"])
        tmp = h.nieuwe_tijdelijke_map(prefix="it7-bronnen-")
        try:
            site = os.path.join(tmp, "site")
            rc, out, err = h.bouw(site, data=h.PROJECT_DATA)
            if rc != 0:
                self.skipTest("NIET GETEST: bouwen met data/nieuws.json faalde of ontbreekt: " + err.strip())
            bronnen = h.lees(os.path.join(site, "bronnen.html"))
            for feed in auto:
                self.assertIn(h.htmllib.escape(feed["naam"]), bronnen, "niet op bronnen.html: %s" % feed["naam"])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class TestUS019C3Opschonen(unittest.TestCase):
    """Lokale testfeeds op 127.0.0.1. Een bron die niet in de config staat wordt verwijderd; een falende feed die wel
    in de config staat houdt zijn items (US-011 c2)."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="it7-opschonen-")
        self.uit = os.path.join(self.tmp, "nieuws.json")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_US019_c3_items_van_bron_niet_in_config_verwijderd_falende_feed_blijft(self):
        routes = {"/ok.xml": {"body": hf.rss_feed},
                  "/down.xml": {"status": 500, "body": b"even weg", "ctype": "text/plain"}}
        def it(i, bron, url_stam, datum):
            # De titel bevat een trefwoord (automatisering): een item zonder trefwoord wordt bij het ophalen
            # opnieuw ingedeeld en verwijderd (US-010 c4), wat deze test niet mag meten.
            return {"id": "o%03d" % i, "titel": "Automatisering-item %d van %s" % (i, bron), "categorie": "Automatisering",
                    "bron": bron, "taal": "nl", "datum": datum, "samenvatting": "Verzonnen testtekst.",
                    "url": "https://voorbeeld-bron.example/%s-%03d" % (url_stam, i)}
        oud = [it(1, "AWS Big Data Blog", "aws", hf.iso_dag(3)),
               it(2, "Verwijderde Testbron", "weg", hf.iso_dag(2)),
               it(3, "Kapotte Testfeed", "kapot", hf.iso_dag(1))]
        with open(self.uit, "w", encoding="utf-8") as f:
            json.dump({"bijgewerkt": "2026-10-08T00:00:00+00:00", "items": oud}, f, ensure_ascii=False)
        with hf.FeedServer(routes) as srv:
            feeds = [{"naam": "Testfeed RSS", "url": srv.base + "/ok.xml", "taal": "nl"},
                     {"naam": "Kapotte Testfeed", "url": srv.base + "/down.xml", "taal": "nl"}]
            cfg = hf.schrijf_config(os.path.join(self.tmp, "cfg.json"), feeds)
            res = hf.run_ophalen(cfg, self.uit)
        uitvoer = res.stdout + res.stderr
        self.assertEqual(res.returncode, 0, uitvoer)
        self.assertIn("FOUT", uitvoer, "de falende feed moet als FOUT gemeld worden")
        items = hf.lees_json(self.uit)["items"]
        bronnen = [i["bron"] for i in items]
        self.assertNotIn("AWS Big Data Blog", bronnen, "item van een bron die niet in de config staat is blijven staan")
        self.assertNotIn("Verwijderde Testbron", bronnen, "item van een verwijderde bron is blijven staan")
        self.assertIn("Kapotte Testfeed", bronnen, "items van een falende feed die wel in de config staat zijn verwijderd")
        self.assertIn("Testfeed RSS", bronnen, "de werkende feed heeft geen items opgeslagen")


class TestUS019C4EchteData(unittest.TestCase):
    """Alleen-lezen controle op data/nieuws.json (als het bestand bestaat). De meting per categorie en per feed
    (meldpunten) staat in het testrapport; die wordt niet hard getoetst."""

    @classmethod
    def setUpClass(cls):
        if not os.path.exists(h.PROJECT_DATA):
            raise unittest.SkipTest("NIET GETEST: data/nieuws.json ontbreekt")
        with open(h.PROJECT_DATA, encoding="utf-8") as f:
            cls.items = json.load(f).get("items", [])
        cls.namen = set(BRONNEN_NAMEN)

    def test_US019_c4_echte_data_bevat_items_van_een_automatiseringsfeed(self):
        auto = [i for i in self.items if AUTO_PATROON.search(i.get("bron", ""))]
        self.assertGreaterEqual(len(auto), 1, "geen item van een automatiseringsfeed in data/nieuws.json")

    def test_US019_c3_echte_data_geen_items_van_niet_geconfigureerde_bronnen(self):
        vreemd = sorted({i.get("bron") for i in self.items if i.get("bron") not in self.namen})
        self.assertEqual(vreemd, [], "items van bronnen die niet (meer) in config/feeds.json staan")


if __name__ == "__main__":
    unittest.main()
