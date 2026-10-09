"""Acceptatietests US-012 c5 (aanvulling it. 4 ronde 3): de bronnenlijst bevat ALLE bronnen die op de site getoond worden.

US-012 c5: "...met link naar een lijst van alle bronnen". Items blijven 60 dagen in data/nieuws.json staan, ook na het
verwijderen van hun feed uit config/feeds.json. De bronnenlijst (bronnen.html) wordt nu alleen uit de config gebouwd,
dus die items tonen een bronnaam die niet in de lijst staat. Geen internet nodig.
"""
import html
import json
import os
import shutil
import sys
import unittest

import hulp_statisch as h

sys.dont_write_bytecode = True


def _schrijf_data(map, bronnen):
    items = []
    for n, bron in enumerate(bronnen, 1):
        # it. 6: categorie Data (was AI; alleen AI-items worden door het AI-plafond weggefilterd)
        items.append({"id": "b%03d" % n, "titel": "Artikel %d van %s" % (n, bron), "categorie": "Data", "bron": bron,
                      "taal": "en", "datum": "2026-10-07", "samenvatting": "Verzonnen testtekst.",
                      "url": "https://voorbeeld-bron.example/bron-%03d" % n})
    pad = os.path.join(map, "nieuws.json")
    with open(pad, "w", encoding="utf-8") as f:
        json.dump({"bijgewerkt": h.FIXTURE_BIJGEWERKT, "items": items}, f, ensure_ascii=False)
    return pad


class TestUS012C5Bronnenlijst(unittest.TestCase):
    def test_US012_c5_fixture_bron_die_niet_in_config_staat_staat_toch_op_bronnenlijst(self):
        tmp = h.nieuwe_tijdelijke_map()
        try:
            data = _schrijf_data(tmp, ["Fixture Verdwenen Bron", "Fixture Bron A"])
            site = os.path.join(tmp, "site")
            rc, out, err = h.bouw(site, data=data)
            self.assertEqual(rc, 0, err)
            bronnen = h.lees(os.path.join(site, "bronnen.html"))
            self.assertIn(html.escape("Fixture Verdwenen Bron"), bronnen,
                          "bron van een getoond item ontbreekt op de bronnenlijst")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_US012_c5_echte_data_elke_getoonde_bron_staat_op_bronnenlijst(self):
        with open(h.PROJECT_DATA, encoding="utf-8") as f:
            d = json.load(f)
        bronnen_in_data = sorted({i["bron"] for i in d["items"] if i.get("bron")})
        tmp = h.nieuwe_tijdelijke_map()
        try:
            site = os.path.join(tmp, "site")
            rc, out, err = h.bouw(site, data=h.PROJECT_DATA)
            self.assertEqual(rc, 0, err)
            tekst = h.lees(os.path.join(site, "bronnen.html"))
            ontbreekt = [b for b in bronnen_in_data if html.escape(b) not in tekst]
            self.assertEqual(ontbreekt, [], "bronnen die op de site getoond worden maar niet op bronnen.html staan")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
