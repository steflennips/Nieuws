"""Acceptatietest US-013-c5 (README: letterlijke voorbeeldregel van een feed in config/feeds.json).

De test pakt de voorbeeldregel uit README.md en controleert dat die regel geldig JSON is en exact
overeenkomt met een feed in config/feeds.json (dus dat Stef de regel letterlijk kan overnemen).
"""
import json
import re
import sys
import unittest

import hulp_statisch as h

sys.dont_write_bytecode = True
README = h.os.path.join(h.ROOT, "README.technisch.md")  # was README.md; nu de lokale technische README (feeds, voorbeeldregel)


class TestUS013C5Readme(unittest.TestCase):
    def test_US013_c5_readme_bevat_letterlijke_feedregel_die_in_config_staat(self):
        tekst = h.lees(README)
        regels = [r.strip() for r in tekst.splitlines() if r.strip().startswith('{"naam"')]
        self.assertTrue(regels, "README bevat geen voorbeeldregel van een feed (regel die begint met {\"naam\")")
        with open(h.PROJECT_CONFIG, encoding="utf-8") as f:
            feeds = json.load(f)["feeds"]
        gevonden = False
        for regel in regels:
            feed = json.loads(regel)  # moet geldige JSON zijn
            self.assertEqual(set(feed.keys()), {"naam", "url", "taal"})
            if feed in feeds:
                gevonden = True
        self.assertTrue(gevonden, "voorbeeldregel uit README komt niet letterlijk overeen met een feed in config/feeds.json")

    def test_US013_c5_readme_beschrijft_feed_toevoegen_verwijderen_en_handmatig_starten(self):
        tekst = h.lees(README)
        self.assertIn("**Feeds beheren:**", tekst)
        self.assertIn("**toevoegen**", tekst)
        self.assertIn("**verwijderen**", tekst)
        self.assertIn("Run workflow", tekst)
        self.assertRegex(tekst, r"Actions > Nieuws verversen en publiceren > Run workflow")


if __name__ == "__main__":
    unittest.main()
