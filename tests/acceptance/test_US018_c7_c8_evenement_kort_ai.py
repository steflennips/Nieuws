"""Acceptatietests US-018 c7 (evenementtermen) en c8 (Vaknieuws hooguit 2 AI, aanvullen, geen "Kort:"), iteratie 6.

Statische site, vaste peildatum (h.FIXTURE_VANDAAG = 2026-10-08), fixture-data in een tijdelijke map. Geen internet.
- c7: een evenementaankondiging (titel of samenvatting, hele woorden) komt niet in Uitgelicht of Vaknieuws, wel op Nieuws.
  Positief: gewoon nieuws blijft in Uitgelicht; "Eventueel" is geen evenementterm. Echte Techzine-titel: alleen op Nieuws
  (alleen-lezen controle op data/nieuws.json; NIET GETEST als die titel niet in de huidige data staat).
- c8: Vaknieuws hooguit 2 AI, aangevuld met niet-AI; titel die met "Kort:" begint staat niet in Uitgelicht/Vaknieuws,
  wel op Nieuws. Dataset: 6 AI-items en 1 "Kort:"-titel (plus niet-AI items, zodat het AI-plafond niets weglaat).
"""
import datetime
import json
import os
import re
import shutil
import unittest

import hulp_statisch as h

ECHT_TECHZINE = "Begin bij het einde: zo maak je agentic remediation mogelijk"


def item(titel, categorie, datum, bron="Fixture Bron A", sam="Verzonnen testtekst.", n=0):
    return {"id": "c%04d" % n, "titel": titel, "categorie": categorie, "bron": bron, "taal": "nl", "datum": datum,
            "samenvatting": sam, "url": "https://voorbeeld-bron.example/c78-%04d" % n}


def bouw_fixture(items):
    tmp = h.nieuwe_tijdelijke_map(prefix="it6-c78-")
    pad = os.path.join(tmp, "nieuws.json")
    with open(pad, "w", encoding="utf-8") as f:
        json.dump({"bijgewerkt": h.FIXTURE_BIJGEWERKT, "items": items}, f, ensure_ascii=False)
    site = os.path.join(tmp, "site")
    rc, out, err = h.bouw(site, data=pad, vandaag=h.FIXTURE_VANDAAG)
    return tmp, site, rc, out + err


def blok(p, id_):
    m = re.search(r'<section class="blok[^"]*" id="%s">(.*?)</section>' % id_, p, re.S)
    return m.group(1) if m else ""


def titels(fragment):
    """Titels van de lijstitems in een blok (ontdubbeld in volgorde; HTML-ontsnapt zoals de site ze schrijft)."""
    return [h.htmllib.unescape(t) for t in re.findall(r'<li><a [^>]*>([^<]+)</a>', fragment)]


def categorieen(fragment):
    return re.findall(r'<span class="tag">([^<]+)</span>', fragment)


class TestUS018C7Evenementen(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        items = [
            item(ECHT_TECHZINE, "Automatisering", "2026-10-08", bron="Techzine", n=1,
                 sam="Aankondiging van het ServiceNow World Forum op 28 oktober in Amsterdam. Meld je aan."),
            item("Nederlandse gemeenten kiezen Power BI voor dashboards", "BI", "2026-10-07", bron="Computable", n=2,
                 sam="Gemeenten en het mkb kiezen voor Power BI."),
            item("Eventueel tekort aan BI-specialisten in het mkb", "BI", "2026-10-06", n=3,
                 sam="Een rapport over rapportages."),
        ]
        cls.tmp, cls.site, cls.rc, cls.melding = bouw_fixture(items)
        assert cls.rc == 0, cls.melding
        cls.p = h.lees(os.path.join(cls.site, "index.html"))
        cls.nieuws = h.lees(os.path.join(cls.site, "nieuws.html"))
        cls.uit = titels(blok(cls.p, "blok-uitgelicht"))
        cls.vak = titels(blok(cls.p, "blok-nieuws"))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_US018_c7_evenementaankondiging_niet_in_uitgelicht_of_vaknieuws(self):
        self.assertNotIn(ECHT_TECHZINE, self.uit, "evenementaankondiging staat in Uitgelicht")
        self.assertNotIn(ECHT_TECHZINE, self.vak, "evenementaankondiging staat in Vaknieuws")

    def test_US018_c7_evenementaankondiging_blijft_op_nieuws(self):
        self.assertIn(ECHT_TECHZINE, h.htmllib.unescape(self.nieuws), "evenementitem is van Nieuws verdwenen")

    def test_US018_c7_gewoon_nieuws_blijft_in_uitgelicht(self):
        self.assertIn("Nederlandse gemeenten kiezen Power BI voor dashboards", self.uit)

    def test_US018_c7_eventueel_is_geen_evenementterm(self):
        self.assertIn("Eventueel tekort aan BI-specialisten in het mkb", self.uit + self.vak,
                      "'Eventueel' werd ten onrechte als evenement uitgesloten")

    def test_US018_c7_echte_techzine_titel_alleen_op_nieuws_als_die_in_de_data_staat(self):
        """Alleen-lezen controle op de echte data (geen wijziging). Zonder die titel in de data: NIET GETEST."""
        if not os.path.exists(h.PROJECT_DATA):
            self.skipTest("NIET GETEST: data/nieuws.json ontbreekt")
        with open(h.PROJECT_DATA, encoding="utf-8") as f:
            echt = json.load(f).get("items", [])
        if not any(i.get("titel") == ECHT_TECHZINE for i in echt):
            self.skipTest("NIET GETEST: de echte Techzine-titel staat niet in de huidige data/nieuws.json")
        tmp = h.nieuwe_tijdelijke_map(prefix="it6-c7-echt-")
        try:
            site = os.path.join(tmp, "site")
            rc, out, err = h.bouw(site, data=h.PROJECT_DATA)
            self.assertEqual(rc, 0, out + err)
            p = h.lees(os.path.join(site, "index.html"))
            esc = h.htmllib.escape(ECHT_TECHZINE)
            self.assertNotIn(esc, blok(p, "blok-uitgelicht"), "echte Techzine-titel staat in Uitgelicht")
            self.assertNotIn(esc, blok(p, "blok-nieuws"), "echte Techzine-titel staat in Vaknieuws")
            self.assertIn(esc, h.lees(os.path.join(site, "nieuws.html")), "echte Techzine-titel niet op Nieuws")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class TestUS018C8VaknieuwsAI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # it. 7 (US-021): Uitgelicht komt alleen uit headnieuws-feeds; AI A en B komen daarom uit Computable (headnieuws, NL).
        ai = [item("AI-bericht %s" % letter, "AI", datum, bron=("Computable" if k < 2 else "Fixture Bron A"), n=10 + k)
              for k, (letter, datum) in enumerate(zip("ABCDEF", ["2026-10-08", "2026-10-07", "2026-10-06",
                                                                  "2026-10-05", "2026-10-04", "2026-10-03"]))]
        kort = item("Kort: Google-detector vindt nieuwe phishing", "Data", "2026-10-08", n=30,
                    sam="Een digest van vandaag.")
        overig = [item("Overig-%d (%s)" % (k, cat), cat, dat, n=40 + k)
                  for k, (cat, dat) in enumerate([("BI", "2026-10-02"), ("Data", "2026-10-01"),
                                                  ("Automatisering", "2026-09-30"), ("BI", "2026-09-29"),
                                                  ("Data", "2026-09-28"), ("Automatisering", "2026-09-27"),
                                                  ("BI", "2026-09-26"), ("Data", "2026-09-25"),
                                                  ("Automatisering", "2026-09-24")])]
        cls.tmp, cls.site, cls.rc, cls.melding = bouw_fixture(ai + [kort] + overig)
        assert cls.rc == 0, cls.melding
        cls.p = h.lees(os.path.join(cls.site, "index.html"))
        cls.nieuws = h.lees(os.path.join(cls.site, "nieuws.html"))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_US018_c8_vaknieuws_hooguit_2_ai_en_aangevuld_met_niet_ai(self):
        vak = titels(blok(self.p, "blok-nieuws"))
        self.assertEqual(len(vak), 5, "Vaknieuws moet met niet-AI aangevuld worden tot 5: %s" % vak)
        ai_n = sum(1 for t in vak if t.startswith("AI-bericht"))
        self.assertLessEqual(ai_n, 2, "Vaknieuws bevat meer dan 2 AI-items: %s" % vak)
        self.assertGreaterEqual(len(vak) - ai_n, 3, "Vaknieuws niet aangevuld met niet-AI")

    def test_US018_c8_vaknieuws_exacte_volgorde(self):
        """Verwacht (nieuwste eerst, max 2 AI, Kort: niet). Uitgelicht = AI A, AI B (max 2 AI).
        Vaknieuws = AI C, AI D (2 AI), daarna de nieuwste niet-AI: Overig-0, Overig-1, Overig-2."""
        uit = titels(blok(self.p, "blok-uitgelicht"))
        vak = titels(blok(self.p, "blok-nieuws"))
        self.assertEqual(uit, ["AI-bericht A", "AI-bericht B"])
        self.assertEqual(vak, ["AI-bericht C", "AI-bericht D", "Overig-0 (BI)", "Overig-1 (Data)", "Overig-2 (Automatisering)"])

    def test_US018_c8_kort_titel_niet_in_uitgelicht_of_vaknieuws(self):
        uit = titels(blok(self.p, "blok-uitgelicht"))
        vak = titels(blok(self.p, "blok-nieuws"))
        for t in uit + vak:
            self.assertFalse(t.casefold().startswith("kort:"), "'Kort:'-titel in Uitgelicht/Vaknieuws: %s" % t)

    def test_US018_c8_kort_titel_blijft_op_nieuws(self):
        self.assertIn("Kort: Google-detector vindt nieuwe phishing", h.htmllib.unescape(self.nieuws))

    def test_US018_c8_uitgelicht_hooguit_2_ai(self):
        uit = titels(blok(self.p, "blok-uitgelicht"))
        self.assertLessEqual(sum(1 for t in uit if t.startswith("AI-bericht")), 2, uit)


if __name__ == "__main__":
    unittest.main()
