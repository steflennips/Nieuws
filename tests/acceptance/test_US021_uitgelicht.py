"""Acceptatietests US-021 (Uitgelicht alleen uit headnieuws, voorkeur Nederlands), iteratie 7.

- c1 een niet-headnieuws-feed (productblog) met de hoogste relevantie komt niet in Uitgelicht; wel op Nieuws en
  (als hij daar hoort) in Vaknieuws.
- c2 selectie alleen uit headnieuws-feeds; scoreregel US-018 c3 plus 1 punt voor taal "nl". Vaste volgorde op een
  testconfig (NL en EN headnieuws met gelijke relevantie: NL eerst).
- c3 geen aanvulling: 2 geschikte items geven precies 2 items; 0 items geeft "Nog geen uitgelicht nieuws" zonder fout;
  Vaknieuws blijft dan gewoon items tonen.
- c4 Vaknieuws ongewijzigd: de 5 nieuwste items die niet in Uitgelicht staan, ongeacht taal.

Statische site, vaste peildatum (2026-10-08), fixtures in een tijdelijke map. Geen internet.
Scores (controle met de hand, testconfig = projectconfig met andere feeds): headnieuws 2 + nl 1 + 1 per term uit
deux_relevantie in titel of samenvatting (hele woorden).
"""
import html as htmllib
import json
import os
import re
import shutil
import sys
import unittest

import hulp_statisch as h
import hulp_feeds as hf

sys.dont_write_bytecode = True
VANDAAG = h.FIXTURE_VANDAAG  # 2026-10-08: laatste 3 dagen = vanaf 2026-10-05

HN_NL = {"naam": "Krant NL", "url": "https://krant-nl.example/feed", "taal": "nl", "headnieuws": True}
HN_EN = {"naam": "Krant EN", "url": "https://krant-en.example/feed", "taal": "en", "headnieuws": True}
PROD_EN = {"naam": "Vakblog EN", "url": "https://vakblog-en.example/feed", "taal": "en"}
PROD_NL = {"naam": "Blog NL", "url": "https://blog-nl.example/feed", "taal": "nl"}
TESTFEEDS = [HN_NL, HN_EN, PROD_EN, PROD_NL]


def it(n, titel, bron, datum, taal="nl", cat="BI", sam="Verzonnen testtekst."):
    return {"id": "u%03d" % n, "titel": titel, "categorie": cat, "bron": bron, "taal": taal, "datum": datum,
            "samenvatting": sam, "url": "https://voorbeeld-bron.example/u21-%03d" % n}


def bouw(items, feeds=None):
    """Bouwt de site met de items. feeds=None: projectconfig; anders een testconfig met die feeds."""
    tmp = h.nieuwe_tijdelijke_map(prefix="it7-uitgelicht-")
    data = os.path.join(tmp, "nieuws.json")
    with open(data, "w", encoding="utf-8") as f:
        json.dump({"bijgewerkt": h.FIXTURE_BIJGEWERKT, "items": items}, f, ensure_ascii=False)
    cfg = h.PROJECT_CONFIG
    if feeds is not None:
        cfg = hf.schrijf_config(os.path.join(tmp, "cfg.json"), feeds)
    site = os.path.join(tmp, "site")
    rc, out, err = h.bouw(site, data=data, config=cfg, vandaag=VANDAAG)
    return tmp, site, rc, out + err


def blok(p, id_):
    m = re.search(r'<section class="blok[^"]*" id="%s">(.*?)</section>' % id_, p, re.S)
    return m.group(1) if m else ""


def titels(fragment):
    return [htmllib.unescape(t) for t in re.findall(r'<li><a [^>]*>([^<]+)</a>', fragment)]


class TestUS021C1GeenProductblogInUitgelicht(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        items = [
            # productblog (niet headnieuws) met de hoogste relevantie: 5 termen (Microsoft, Power BI, Fabric, Nederland, MKB)
            it(1, "Microsoft Power BI en Fabric: nieuws voor Nederland en het MKB", "Power BI Blog (Microsoft)",
               "2026-10-08", taal="en", cat="BI"),
            # headnieuws NL: score 2 + 1 + 1 (AVG) = 4
            it(2, "AVG-toezicht bij toezichthouders wordt strenger", "Computable", "2026-10-07", cat="Data",
               sam="Nieuwe regels voor de AVG."),
            it(3, "Automatisering van bestellingen bij het mkb", "Techzine", "2026-10-06", cat="Automatisering"),
        ]
        cls.tmp, cls.site, cls.rc, cls.melding = bouw(items)
        assert cls.rc == 0, cls.melding
        cls.p = h.lees(os.path.join(cls.site, "index.html"))
        cls.nieuws = h.lees(os.path.join(cls.site, "nieuws.html"))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_US021_c1_productblog_met_hoogste_score_niet_in_uitgelicht(self):
        uit = titels(blok(self.p, "blok-uitgelicht"))
        self.assertNotIn("Microsoft Power BI en Fabric: nieuws voor Nederland en het MKB", uit)
        self.assertIn("AVG-toezicht bij toezichthouders wordt strenger", uit)

    def test_US021_c1_productblog_wel_op_nieuws_en_in_vaknieuws_als_nieuwste(self):
        self.assertIn("Microsoft Power BI en Fabric: nieuws voor Nederland en het MKB", htmllib.unescape(self.nieuws))
        vak = titels(blok(self.p, "blok-nieuws"))
        self.assertIn("Microsoft Power BI en Fabric: nieuws voor Nederland en het MKB", vak,
                      "de nieuwste productblog hoort in Vaknieuws (US-018 c5)")


class TestUS021C2SelectieEnVolgorde(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Verwachte scores (headnieuws 2 + nl 1 + termen):
        #  a: NL, termen overheid/AI Act/MKB = 3 -> 6, 2026-10-06
        #  c: NL, termen Nederlandse/Power BI = 2 -> 5, 2026-10-07
        #  g: NL, termen overheid/MKB = 2 -> 5, 2026-10-06  (EN met gelijke termen zou 4 zijn)
        #  h: EN, termen Microsoft/Fabric = 2 -> 4, 2026-10-08 (nieuwer dan g, maar lager: NL-punt wint)
        #  b: EN, termen Snowflake/dbt = 2 -> 4, 2026-10-07
        #  d: EN, termen Tableau/Nederland = 2 -> 4, 2026-10-06 (zesde: valt af, max 5)
        #  f: productblog EN (niet headnieuws), termen Looker/Qlik = 2 -> niet in aanmerking
        items = [
            it(1, "Overheid werkt aan AI Act voor het MKB", "Krant NL", "2026-10-06"),
            it(2, "Nederlandse gemeenten kiezen voor Power BI", "Krant NL", "2026-10-07"),
            it(3, "Overheid en MKB-regels voor 2027", "Krant NL", "2026-10-06"),
            it(4, "Microsoft en Fabric in de praktijk", "Krant EN", "2026-10-08", taal="en"),
            it(5, "Snowflake en dbt verbeteren de datastack", "Krant EN", "2026-10-07", taal="en"),
            it(6, "Tableau-dashboards voor Nederland", "Krant EN", "2026-10-06", taal="en"),
            it(7, "Looker en Qlik vergeleken", "Vakblog EN", "2026-10-08", taal="en"),
        ]
        cls.tmp, cls.site, cls.rc, cls.melding = bouw(items, feeds=TESTFEEDS)
        assert cls.rc == 0, cls.melding
        cls.p = h.lees(os.path.join(cls.site, "index.html"))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_US021_c2_uitgelicht_exacte_volgorde_met_nl_punt(self):
        uit = titels(blok(self.p, "blok-uitgelicht"))
        verwacht = ["Overheid werkt aan AI Act voor het MKB",     # 6
                    "Nederlandse gemeenten kiezen voor Power BI",  # 5, nieuwer dan g
                    "Overheid en MKB-regels voor 2027",            # 5 (NL-punt), ook al ouder dan h
                    "Microsoft en Fabric in de praktijk",          # 4, nieuwste EN
                    "Snowflake en dbt verbeteren de datastack"]    # 4
        self.assertEqual(uit, verwacht)

    def test_US021_c2_productblog_looker_qlik_niet_in_uitgelicht(self):
        # Een productblog mag in Vaknieuws en op Nieuws staan (US-021 c1); alleen Uitgelicht is afgesloten.
        self.assertNotIn("Looker en Qlik vergeleken", titels(blok(self.p, "blok-uitgelicht")))


class TestUS021C3GeenAanvulling(unittest.TestCase):
    def test_US021_c3_twee_geschikte_items_geven_precies_twee(self):
        items = [
            it(1, "Gemeenten kiezen voor AVG-proof dashboards", "Krant NL", "2026-10-08"),
            it(2, "Snowflake-update voor het mkb", "Krant EN", "2026-10-07", taal="en"),
        ]
        items += [it(10 + k, "Productnieuws %d over datawarehouses" % k, "Vakblog EN", "2026-10-0%d" % (8 - k % 4),
                     taal="en", cat="Data") for k in range(12)]
        tmp, site, rc, melding = bouw(items, feeds=TESTFEEDS)
        try:
            self.assertEqual(rc, 0, melding)
            p = h.lees(os.path.join(site, "index.html"))
            uit = titels(blok(p, "blok-uitgelicht"))
            self.assertEqual(uit, ["Gemeenten kiezen voor AVG-proof dashboards", "Snowflake-update voor het mkb"],
                             "Uitgelicht is aangevuld met productblogs")
            self.assertNotIn("Nog geen uitgelicht nieuws", p)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_US021_c3_nul_geschikte_items_toont_melding_en_vaknieuws_blijft(self):
        items = [it(20 + k, "Productnieuws %d over datawarehouses" % k, "Vakblog EN", "2026-10-0%d" % (8 - k % 4),
                    taal="en", cat="Data") for k in range(8)]
        tmp, site, rc, melding = bouw(items, feeds=TESTFEEDS)
        try:
            self.assertEqual(rc, 0, melding)
            p = h.lees(os.path.join(site, "index.html"))
            self.assertIn("Nog geen uitgelicht nieuws", p)
            self.assertNotIn("Traceback", melding)
            self.assertEqual(len(titels(blok(p, "blok-nieuws"))), 5, "Vaknieuws moet nog steeds 5 items tonen")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class TestUS021C4VaknieuwsOngewijzigd(unittest.TestCase):
    def test_US021_c4_vaknieuws_is_5_nieuwste_niet_in_uitgelicht_ongeacht_taal(self):
        items = [
            it(1, "Nederlands blognieuws van vandaag", "Blog NL", "2026-10-08", cat="Automatisering"),   # nieuwste, NL
            it(2, "English vendor news of the day", "Vakblog EN", "2026-10-07", taal="en", cat="BI"),
            it(3, "Nederlands blognieuws van gisteren", "Blog NL", "2026-10-06", cat="Data"),
            it(4, "English vendor news van eergisteren", "Vakblog EN", "2026-10-05", taal="en", cat="BI"),
            it(5, "Nederlands blognieuws van twee dagen terug", "Blog NL", "2026-10-04", cat="Data"),
            it(6, "English news van vier dagen terug", "Vakblog EN", "2026-10-04", taal="en", cat="BI"),
            it(7, "Oudste Nederlandse item", "Blog NL", "2026-10-01", cat="Data"),
            it(8, "Headnieuws NL van vandaag", "Krant NL", "2026-10-08"),  # wel in Uitgelicht
        ]
        tmp, site, rc, melding = bouw(items, feeds=TESTFEEDS)
        try:
            self.assertEqual(rc, 0, melding)
            p = h.lees(os.path.join(site, "index.html"))
            self.assertEqual(titels(blok(p, "blok-uitgelicht")), ["Headnieuws NL van vandaag"])
            vak = titels(blok(p, "blok-nieuws"))
            # de 5 nieuwste die niet in Uitgelicht staan, op datum; de twee items van 2026-10-04 hebben gelijke datum:
            # alleen de datum wordt getoetst, de volgorde binnen gelijke datum is niet vastgelegd.
            self.assertEqual(vak[0], "Nederlands blognieuws van vandaag")
            self.assertEqual(vak[1], "English vendor news of the day")
            self.assertEqual(set(vak[2:4]), {"Nederlands blognieuws van gisteren", "English vendor news van eergisteren"})
            self.assertNotIn("Oudste Nederlandse item", vak)
            self.assertNotIn("Headnieuws NL van vandaag", vak)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class TestUS021Readme(unittest.TestCase):
    def test_US021_c2_readme_beschrijft_headnieuws_en_nl_punt(self):
        readme = h.lees(os.path.join(h.ROOT, "README.technisch.md"))  # was README.md; NL-punt staat in de technische README
        self.assertIn("headnieuws", readme)
        self.assertTrue("1 extra punt" in readme or "1 punt" in readme, "README beschrijft het NL-punt niet")
        self.assertIn("niet aangevuld", readme, "README moet zeggen dat Uitgelicht niet met productblogs wordt aangevuld")


if __name__ == "__main__":
    unittest.main()
