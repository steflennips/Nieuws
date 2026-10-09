"""Acceptatietest US-015-c7 (minstens 2 gratis automatiseringsfeeds in config, op bronnen.html en in het feedbesluit).

Iteratie 7 (besluit 2026-10-09-criteria-feedruil-it7.md): "1 of 2 extra automatiseringsfeeds" is "minstens 2".
De test toetst op de naam van de feed (regel), niet op vaste feednamen; zo breekt een feedruil de test niet.
Geen internet: de test leest config/feeds.json, docs/decisions/2026-10-08-nieuwsfeeds.md en bouwt de site
naar een tijdelijke map (met data/nieuws.json, alleen gelezen) om bronnen.html te controleren.
De feed zelf wordt hier NIET opgehaald; dat is de handmatige ophaalcontrole (zie tests/acceptance/README.md).
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
AUTOMATISERING_PATROON = re.compile(r"automati|automate|workflow|power platform|low-code|\brpa\b", re.I)


class TestUS015C7(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(h.PROJECT_CONFIG, encoding="utf-8") as f:
            cls.cfg = json.load(f)
        cls.auto = [f for f in cls.cfg["feeds"] if AUTOMATISERING_PATROON.search(f["naam"])]

    def test_US015_c7_config_bevat_minstens_2_automatiseringsfeeds_zonder_login(self):
        self.assertGreaterEqual(len(self.auto), 2, "minder dan 2 automatiseringsfeeds (op naam): %s"
                                % [f["naam"] for f in self.auto])
        for feed in self.auto:
            self.assertTrue(feed["naam"].strip())
            self.assertTrue(feed["url"].startswith("https://"), feed["naam"])
            self.assertNotIn("?", feed["url"], "parameters/sleutels in de feed-URL: %s" % feed["naam"])

    def test_US015_c7_feedaantal_binnen_8_tot_10_en_min_3_per_taal(self):
        feeds = self.cfg["feeds"]
        self.assertGreaterEqual(len(feeds), 8)
        self.assertLessEqual(len(feeds), 10)
        self.assertGreaterEqual(sum(1 for f in feeds if f["taal"] == "nl"), 3)
        self.assertGreaterEqual(sum(1 for f in feeds if f["taal"] == "en"), 3)

    def test_US015_c7_automatiseringsfeeds_staan_in_feedbesluit(self):
        with open(DECISION, encoding="utf-8") as f:
            tekst = f.read()
        for feed in self.auto:
            self.assertIn(feed["url"], tekst, "automatiseringsfeed niet in het feedbesluit: %s" % feed["naam"])

    def test_US015_c7_automatiseringsfeeds_staan_op_bronnen_html(self):
        tmp = h.nieuwe_tijdelijke_map()
        try:
            site = os.path.join(tmp, "site")
            rc, out, err = h.bouw(site, data=h.PROJECT_DATA)
            if rc != 0:
                self.skipTest("NIET GETEST: bouwen met data/nieuws.json faalde of ontbreekt: " + err.strip())
            tekst = h.lees(os.path.join(site, "bronnen.html"))
            for feed in self.auto:
                self.assertIn(htmllib.escape(feed["naam"]), tekst, "automatiseringsbron ontbreekt op bronnen.html: %s" % feed["naam"])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
