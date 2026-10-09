"""Acceptatietest US-016 c11 (fixronde 2, iteratie 6): ongeldige --vandaag geeft een Nederlandse melding.

Gegeven `python src/bouw.py --vandaag 2026-13-45`: melding in het Nederlands, noemt het formaat JJJJ-MM-DD,
exitcode 1, geen traceback. Positieve controle: een geldige peildatum bouwt wel (exitcode 0).
Geen internet; gebouwd naar een tijdelijke map met fixture-data.
"""
import json
import os
import shutil
import unittest

import hulp_statisch as h


class TestUS016C11Peildatum(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = h.nieuwe_tijdelijke_map(prefix="it6-c11-")
        cls.data = os.path.join(cls.tmp, "nieuws.json")
        with open(cls.data, "w", encoding="utf-8") as f:
            json.dump({"bijgewerkt": h.FIXTURE_BIJGEWERKT, "items": h.fixture_items()}, f, ensure_ascii=False)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def _bouw(self, vandaag, naam):
        return h.bouw(os.path.join(self.tmp, naam), data=self.data, vandaag=vandaag)

    def test_US016_c11_ongeldige_maand_geeft_nederlandse_melding_exitcode_1(self):
        rc, out, err = self._bouw("2026-13-45", "site-13")
        melding = out + err
        self.assertEqual(rc, 1, "exitcode moet 1 zijn: %s" % melding)
        self.assertNotIn("Traceback", melding, "traceback in de uitvoer")
        self.assertIn("JJJJ-MM-DD", melding, "melding noemt het verwachte formaat niet: %s" % melding)
        self.assertIn("ongeldige peildatum", melding.casefold(), "melding is niet Nederlands/duidelijk: %s" % melding)
        for engels in ["month must be", "day is out of range", "invalid", "must be in", "Traceback"]:
            self.assertNotIn(engels, melding, "Engelse Python-tekst in de melding: %s" % melding)

    def test_US016_c11_ongeldige_dag_geeft_dezelfde_nederlandse_melding(self):
        rc, out, err = self._bouw("2026-02-30", "site-feb30")
        melding = out + err
        self.assertEqual(rc, 1, "exitcode moet 1 zijn: %s" % melding)
        self.assertNotIn("Traceback", melding)
        self.assertIn("JJJJ-MM-DD", melding, melding)

    def test_US016_c11_positieve_controle_geldige_peildatum_bouwt(self):
        rc, out, err = self._bouw(h.FIXTURE_VANDAAG, "site-ok")
        self.assertEqual(rc, 0, "geldige peildatum moet bouwen: %s" % (out + err))
        self.assertTrue(os.path.exists(os.path.join(self.tmp, "site-ok", "index.html")))


if __name__ == "__main__":
    unittest.main()
