"""Acceptatietest US-015-c11 (minstens 1 gratis data-/BI-/analytics-feed in config, bronnenlijst en feedbesluit). Geen internet.

Iteratie 7 (besluit 2026-10-09-criteria-feedruil-it7.md): de criteriumtekst noemt geen vaste feed meer (AWS Big Data
Blog is verwijderd). De test toetst op de NAAM van de feed (regel: power bi, fabric, analytics, data, BI, dbt, ...),
zodat een feedruil de test niet breekt. Er wordt geen specifieke feed getoetst.

De feed zelf wordt hier NIET opgehaald; de handmatige ophaalronde (US-016 c6 / US-019 c4) staat in het testrapport.
Robots.txt van de feeds is in de feedbesluit-notitie vastgelegd; dat is niet automatisch getest.
"""
import html as htmllib
import json
import os
import re
import shutil
import sys
import unittest

import hulp_statisch as h

sys.dont_write_bytecode = True
DECISION = os.path.join(h.ROOT, "docs", "decisions", "2026-10-08-nieuwsfeeds.md")
DATA_PATROON = re.compile(r"power bi|fabric|sqlbi|analytics|analyse|\bbi\b|\bdata\b|dbt|snowflake|databricks|tableau|qlik|looker",
                          re.I)


class TestUS015C11(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(h.PROJECT_CONFIG, encoding="utf-8") as f:
            cls.cfg = json.load(f)
        cls.data_feeds = [f for f in cls.cfg["feeds"] if DATA_PATROON.search(f["naam"])]

    def test_US015_c11_config_bevat_minstens_1_gratis_data_feed_zonder_login(self):
        self.assertGreaterEqual(len(self.data_feeds), 1, "geen data-/BI-feed (op naam) in config/feeds.json")
        for feed in self.data_feeds:
            self.assertTrue(feed["url"].startswith("https://"), feed["naam"])
            self.assertNotIn("?", feed["url"], "geen parameters/sleutels in de feed-URL: %s" % feed["naam"])

    def test_US015_c11_feedaantal_blijft_max_10_en_min_3_per_taal(self):
        feeds = self.cfg["feeds"]
        self.assertLessEqual(len(feeds), 10)
        self.assertGreaterEqual(sum(1 for f in feeds if f["taal"] == "nl"), 3)
        self.assertGreaterEqual(sum(1 for f in feeds if f["taal"] == "en"), 3)

    def test_US015_c11_datafeeds_staan_in_feedbesluit(self):
        with open(DECISION, encoding="utf-8") as f:
            tekst = f.read()
        for feed in self.data_feeds:
            self.assertIn(feed["url"], tekst, "data-feed staat niet in docs/decisions/2026-10-08-nieuwsfeeds.md: %s" % feed["naam"])

    def test_US015_c11_datafeeds_staan_op_bronnen_html(self):
        tmp = h.nieuwe_tijdelijke_map()
        try:
            site = os.path.join(tmp, "site")
            rc, out, err = h.bouw(site, data=h.PROJECT_DATA)
            if rc != 0:
                self.skipTest("NIET GETEST: bouwen met data/nieuws.json faalde of ontbreekt: " + err.strip())
            tekst = h.lees(os.path.join(site, "bronnen.html"))
            for feed in self.data_feeds:
                self.assertIn(htmllib.escape(feed["naam"]), tekst, "data-bron ontbreekt op bronnen.html: %s" % feed["naam"])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
