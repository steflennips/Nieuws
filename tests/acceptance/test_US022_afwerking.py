"""Acceptatietests US-022 (kleine afwerking voor publicatie), iteratie 8.

- c1: de kop van het blok Vaknieuws bevat geen totaal van alle items; de link naar Nieuws luidt
  "Alle <n> berichten bekijken" met n = aantal items op Nieuws. Getoetst op de fixture-site en op de site uit
  data/nieuws.json (in een tijdelijke map; alleen als dat bestand bestaat, anders NIET GETEST).
- c2: `src/ophalen.py --config <pad>` bij een ontbrekend, onleesbaar of ongeldig configbestand: melding volledig
  Nederlands (noemt het pad), exitcode 2, geen traceback. Geen internet: het commando stopt vóór het ophalen.

Geen wijziging van de tests om te slagen: het criterium is de maatstaf.
"""
import sys
sys.dont_write_bytecode = True  # vóór de imports hieronder: geen __pycache__ in src/ (iteratie 8)

import os
import re
import shutil
import subprocess
import tempfile
import unittest

import hulp_statisch as h

OPHALEN = os.path.join(h.ROOT, "src", "ophalen.py")
ECHTE_DATA = os.path.join(h.ROOT, "data", "nieuws.json")
# Engelse OS- of Python-tekst die niet in de melding mag staan (US-022 c2) en sporen van een traceback.
ENGELS_OF_TRACEBACK = re.compile(
    r"No such file|Expecting|Errno|Permission denied|Is a directory|Invalid|decode|line \d+ column|"
    r"Traceback|not found|Errno|Illegal|byte 0x", re.I)


def _nieuws_kaarten(html):
    return len(re.findall(r'<article class="kaart"', html))


def _controleer_vaknieuws_en_link(tc, index_html, nieuws_html):
    # c1a: de kop van Vaknieuws is alleen de titel, zonder teller.
    kop = re.search(r'<div class="blok-kop"><h2>Vaknieuws</h2></div>', index_html)
    tc.assertIsNotNone(kop, "kop van Vaknieuws is niet 'Vaknieuws' zonder extra tekst")
    # c1b: geen totaal van alle items, ook niet elders op de startpagina.
    tc.assertIsNone(re.search(r"\d+\s+in totaal", index_html), "totaal van alle items op de startpagina")
    tc.assertNotIn("in totaal", index_html)
    # c1c: link naar Nieuws met het aantal items op Nieuws.
    n = _nieuws_kaarten(nieuws_html)
    tc.assertGreater(n, 0, "Nieuws toont geen items")
    tc.assertIn('<a class="alles" href="nieuws.html">Alle %d berichten bekijken</a>' % n, index_html,
                "link naar Nieuws luidt niet 'Alle %d berichten bekijken'" % n)


class TestUS022C1Vaknieuws(unittest.TestCase):
    def test_US022_c1_fixture_startpagina_zonder_totaal_en_link_met_aantal_nieuws(self):
        tmp = tempfile.mkdtemp(prefix="it8-us022-")
        try:
            data = h.schrijf_fixture_data(tmp)
            site = os.path.join(tmp, "site")
            rc, out, err = h.bouw(site, data=data, vandaag=h.FIXTURE_VANDAAG)
            self.assertEqual(rc, 0, err)
            index = h.lees(os.path.join(site, "index.html"))
            nieuws = h.lees(os.path.join(site, "nieuws.html"))
            _controleer_vaknieuws_en_link(self, index, nieuws)
            self.assertEqual(_nieuws_kaarten(nieuws), len(h.fixture_items()))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_US022_c1_echte_data_startpagina_zonder_totaal_en_link_met_aantal_nieuws(self):
        if not os.path.isfile(ECHTE_DATA):
            self.skipTest("NIET GETEST: data/nieuws.json ontbreekt (geen ophaalronde)")
        tmp = tempfile.mkdtemp(prefix="it8-us022-echt-")
        try:
            site = os.path.join(tmp, "site")
            rc, out, err = h.bouw(site, data=ECHTE_DATA)
            self.assertEqual(rc, 0, err)
            index = h.lees(os.path.join(site, "index.html"))
            nieuws = h.lees(os.path.join(site, "nieuws.html"))
            _controleer_vaknieuws_en_link(self, index, nieuws)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class TestUS022C2ConfigMelding(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="it8-us022-cfg-")
        cls.kapot = os.path.join(cls.tmp, "kapot.json")
        with open(cls.kapot, "w", encoding="utf-8") as f:
            f.write("dit is geen json")
        cls.binair = os.path.join(cls.tmp, "binair.json")
        with open(cls.binair, "wb") as f:
            f.write(b"\xff\xfe\x00\x81\x82 geen tekst")
        cls.uitvoer = os.path.join(cls.tmp, "uitvoer.json")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def _draai(self, config):
        res = subprocess.run([sys.executable, "-B", OPHALEN, "--config", config, "--uitvoer", self.uitvoer],
                             capture_output=True, text=True, encoding="utf-8", errors="replace",
                             env=h.omgeving(), timeout=60, cwd=tempfile.gettempdir())
        return res

    def _controleer_nederlands(self, res, config):
        self.assertEqual(res.returncode, 2, res.stdout + res.stderr)
        self.assertNotIn("Traceback", res.stderr, res.stderr)
        self.assertIn("FOUT", res.stderr, res.stderr)
        self.assertIsNone(ENGELS_OF_TRACEBACK.search(res.stderr + res.stdout),
                          "Engelse OS-tekst of traceback in de melding: %r" % (res.stderr,))
        self.assertIn(os.path.basename(config), res.stderr, "melding noemt het pad niet")
        self.assertFalse(os.path.exists(self.uitvoer), "bij een configfout mag geen uitvoerbestand ontstaan")

    def test_US022_c2_ontbrekend_configbestand_nederlandse_melding_exitcode_2(self):
        config = "bestaat-niet.json"
        res = self._draai(config)
        self._controleer_nederlands(res, config)
        self.assertIn("niet gevonden", res.stderr)

    def test_US022_c2_onleesbaar_configbestand_geen_json_nederlandse_melding_exitcode_2(self):
        res = self._draai(self.kapot)
        self._controleer_nederlands(res, self.kapot)
        self.assertIn("geen geldige JSON", res.stderr)

    def test_US022_c2_configbestand_geen_tekst_nederlandse_melding_exitcode_2(self):
        res = self._draai(self.binair)
        self._controleer_nederlands(res, self.binair)
        self.assertIn("UTF-8", res.stderr)

    def test_US022_c2_map_als_configbestand_nederlandse_melding_exitcode_2(self):
        res = self._draai(self.tmp)
        self._controleer_nederlands(res, self.tmp)
        self.assertIn("niet te lezen", res.stderr)

    def test_US022_c2_extra_feed_item_dat_geen_object_is_geeft_geen_traceback(self):
        """Extra (it. 8 Tester, BELANGRIJK): een config die geldige JSON is maar een feed-item als tekst bevat
        ("feeds": ["tekst"]) gaf een traceback (TypeError) en exitcode 1. Verwacht: nette Nederlandse melding,
        exitcode 2, zoals bij andere ongeldige configuratie. Afgeleid van de geest van US-022 c2 (geen traceback)."""
        config = os.path.join(self.tmp, "feed-als-tekst.json")
        with open(config, "w", encoding="utf-8") as f:
            f.write('{"user_agent": "test", "trefwoorden": {"AI": ["ai"]}, "feeds": ["tekst"]}')
        res = self._draai(config)
        self._controleer_nederlands(res, config)

    def _schrijf_config(self, naam, inhoud):
        config = os.path.join(self.tmp, naam)
        with open(config, "w", encoding="utf-8") as f:
            f.write(inhoud)
        return config

    def test_US022_c2_extra_feed_zonder_url_nederlandse_melding_exitcode_2(self):
        """Extra (it. 8 Tester ronde 2, bevinding 2 ronde 1): feed zonder url gaf 'FOUT ... ('url')' en exitcode 1."""
        config = self._schrijf_config("feed-zonder-url.json",
                                      '{"user_agent": "test", "trefwoorden": {"AI": ["ai"]}, '
                                      '"feeds": [{"naam": "A", "taal": "nl"}]}')
        res = self._draai(config)
        self._controleer_nederlands(res, config)
        self.assertIn("url", res.stderr)

    def test_US022_c2_extra_feeds_als_object_leeg_object_en_zonder_user_agent_exitcode_2(self):
        """Extra (it. 8 Tester ronde 2): feeds als object i.p.v. lijst, een leeg object en een config zonder user_agent."""
        gevallen = {
            "feeds-als-object.json": '{"user_agent": "t", "trefwoorden": {"AI": ["ai"]}, '
                                     '"feeds": {"naam": "A", "url": "x", "taal": "nl"}}',
            "leeg-object.json": "{}",
            "zonder-user-agent.json": '{"trefwoorden": {"AI": ["ai"]}, "feeds": []}',
        }
        for naam, inhoud in gevallen.items():
            with self.subTest(config=naam):
                config = self._schrijf_config(naam, inhoud)
                res = self._draai(config)
                self._controleer_nederlands(res, config)


if __name__ == "__main__":
    unittest.main()
