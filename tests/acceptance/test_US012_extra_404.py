"""Aanvullende controle (KLEIN 6 uit iteratie 4 ronde 1, geen eigen criterium): de gebouwde site heeft een eigen 404.html.

GitHub Pages toont site/404.html bij een onbekend adres. Hier controleren we de inhoud van het bestand in een
tijdelijke gebouwde site. Het gedrag op de live site is NIET GETEST (geen live site).
"""
import os
import re
import shutil
import sys
import unittest

import hulp_statisch as h

sys.dont_write_bytecode = True


class TestUS012Extra404(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = h.nieuwe_tijdelijke_map()
        cls.site = os.path.join(cls.tmp, "site")
        rc, out, err = h.bouw(cls.site, data=h.PROJECT_DATA)
        assert rc == 0, err

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_US012_extra_404_html_bestaat_en_is_nederlands(self):
        pad = os.path.join(self.site, "404.html")
        self.assertTrue(os.path.isfile(pad))
        tekst = h.lees(pad)
        self.assertIn('lang="nl"', tekst)
        self.assertIn("Pagina niet gevonden", tekst)
        self.assertIn('href="index.html"', tekst)
        self.assertIn('href="nieuws.html"', tekst)

    def test_US012_extra_404_html_laadt_niets_van_buiten(self):
        tekst = h.lees(os.path.join(self.site, "404.html"))
        self.assertIsNone(re.search(r'(src|href)="https?://', tekst), "404.html laadt externe bestanden of links")
        self.assertIsNone(re.search(r'<link[^>]*href="https?://', tekst), "404.html laadt een extern bestand via link")


if __name__ == "__main__":
    unittest.main()
