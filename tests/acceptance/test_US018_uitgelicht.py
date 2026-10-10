"""Acceptatietests US-018 (Uitgelicht bovenaan, vaknieuws daaronder), iteratie 6.

- c1 configuratie: minstens 2 algemene NL-feeds met headnieuws; lijst Deux-relevantietermen met de verplichte termen.
- c2 startpagina: blok "Uitgelicht" boven de tellertegels, max. 5 items uit de laatste 3 dagen, hooguit 2 AI.
- c3 scoreregel (2 punten headnieuws-feed + 1 punt per verschillende term; hoogste score, dan nieuwste), vaste volgorde.
- c4 minder dan 5 geschikte items toont alleen die; 0 items toont "Nog geen uitgelicht nieuws" zonder fout.
- c5 vaknieuws = de 5 nieuwste items die NIET in Uitgelicht staan.
- c6 375 en 1280 px: geen horizontaal scrollen (browser; zonder headless Edge: NIET GETEST).
Statische site met vaste peildatum (--vandaag 2026-10-08); de lokale app met de klokdatum van de test.
Geen internet.
"""
import sys
sys.dont_write_bytecode = True  # vóór de imports hieronder: geen __pycache__ in src/ (iteratie 8)

import datetime
import json
import os
import re
import shutil
import unittest
from unittest import mock

import hulp_statisch as h
import hulp_browser as hb
# (iteratie 7: test_echte_data_app is vervallen; TestUS018Lokaal is uitgeschakeld, zie hieronder)

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(h.ROOT, "src"))
import mix  # noqa: E402
import ophalen as o  # noqa: E402

with open(h.PROJECT_CONFIG, encoding="utf-8") as f:
    CFG = json.load(f)
README = os.path.join(h.ROOT, "README.technisch.md")  # was README.md; scoreregel staat in de technische README
TERMEN_VERPLICHT = ["MKB", "ZZP", "Nederland", "Nederlandse", "overheid", "gemeente", "AVG", "NIS2", "AI Act", "Microsoft",
                    "Power BI", "Fabric", "Qlik", "Tableau", "Looker", "dbt", "Snowflake", "n8n", "Zapier"]


# it. 7 (US-021 c2): Uitgelicht komt alleen uit headnieuws-feeds; de standaardbron van de fixture is daarom Computable
# (headnieuws, NL). Een item uit een andere bron komt dan niet in Uitgelicht maar wel in Vaknieuws/Nieuws.
def item(titel, categorie, datum, bron="Computable", n=None):
    n = n if n is not None else abs(hash((titel, datum))) % 10 ** 6
    return {"id": "u%06d" % n, "titel": titel, "categorie": categorie, "bron": bron, "taal": "nl", "datum": datum,
            "samenvatting": "Verzonnen testtekst.", "url": "https://voorbeeld-bron.example/uit-%06d" % n}


def terug(vandaag, k):
    return (vandaag - datetime.timedelta(days=k)).isoformat()


def k_fixture(vandaag):
    """k0..k9 = dagen terug. Venster (3 dagen): k0..k3. Categorieen: AI, AI, AI, BI | Data, Auto, BI, AI, Data, Auto.
    Verwacht Uitgelicht: k0, k1, k3 (3e AI wordt overgeslagen). Verwacht vaknieuws: k2, k4, k5, k6, k7."""
    cats = ["AI", "AI", "AI", "BI", "Data", "Automatisering", "BI", "AI", "Data", "Automatisering"]
    return [item("Artikel k%d (%s)" % (k, c), c, terug(vandaag, k), n=100 + k) for k, c in enumerate(cats)]


def titels(k_lijst, vandaag):
    return ["Artikel k%d (%s)" % (k, c) for k, c in k_lijst]


UIT_VERWACHT = ["Artikel k0 (AI)", "Artikel k1 (AI)", "Artikel k3 (BI)"]
VAK_VERWACHT = ["Artikel k2 (AI)", "Artikel k4 (Data)", "Artikel k5 (Automatisering)", "Artikel k6 (BI)", "Artikel k7 (AI)"]


def blok(p, id_):
    m = re.search(r'<section class="blok[^"]*" id="%s">(.*?)</section>' % id_, p, re.S)
    return m.group(1) if m else None


def blok_titels(b):
    return re.findall(r'<li><a [^>]*>([^<]+)</a>', b or "")


class TestUS018Config(unittest.TestCase):
    def test_US018_c1_minstens_2_algemene_nl_headnieuws_feeds(self):
        head = [f for f in CFG["feeds"] if f.get("headnieuws") is True and f["taal"] == "nl"]
        self.assertGreaterEqual(len(head), 2, "minstens 2 algemene NL-feeds met headnieuws")

    def test_US018_c1_deux_relevantietermen_compleet(self):
        lijst = CFG.get("deux_relevantie", [])
        self.assertIsInstance(lijst, list)
        for t in TERMEN_VERPLICHT:
            self.assertIn(t, lijst, "deux_relevantie mist: %s" % t)

    def test_US018_c3_scoreregel_staat_in_readme(self):
        tekst = h.lees(README)
        self.assertIn("Uitgelicht", tekst)
        self.assertRegex(tekst, r"2 punten.*headnieuws", "scoreregel (2 punten headnieuws) staat niet in de README")
        self.assertRegex(tekst, r"1 punt per", "scoreregel (1 punt per term) staat niet in de README")


class TestUS018Score(unittest.TestCase):
    """c3: vaste volgorde met de scoreregel, op een eigen configuratie (headnieuws-feed 'Computable')."""
    def setUp(self):
        self.cfg = {"feeds": [{"naam": "Computable", "url": "https://www.computable.nl/feed/", "taal": "nl",
                               "headnieuws": True},
                              {"naam": "Fixture A", "url": "https://voorbeeld-bron.example/a", "taal": "nl"}],
                    "deux_relevantie": CFG["deux_relevantie"]}
        v = datetime.date(2026, 10, 8)
        self.vandaag = v
        self.items = [
            item("MKB krijgt AI-hulp", "Data", "2026-10-08", "Fixture A", n=1),                               # a: 0+1 = 1
            item("Nederlandse overheid kiest Microsoft", "BI", "2026-10-07", "Computable", n=2),               # b: 2+3 = 5
            item("Power BI en Fabric voor het mkb", "BI", "2026-10-08", "Fixture A", n=3),                    # c: 0+3 = 3
            item("Computable: nieuwe AVG-regels", "AI", "2026-10-06", "Computable", n=4),                     # d: 2+1 = 3
            item("Snelle tips voor dataanalyse", "Data", "2026-10-08", "Fixture A", n=5),                     # e: 0
            item("Computable: n8n en Zapier in de gemeente", "Automatisering", "2026-10-05", "Computable", n=6),  # f: 2+3 = 5
        ]
        self.patronen = [o._patroon(t) for t in self.cfg["deux_relevantie"]]

    def test_US018_c3_volgorde_hoogste_score_eerst_bij_gelijk_nieuwste_eerst(self):
        # it. 7 (US-021 c1/c2): alleen headnieuws-items (Fixture A is geen headnieuws-feed); NL-feed krijgt +1.
        # Scores: b 2+1+3 = 6 (07 okt), f 2+1+3 = 6 (05 okt), d 2+1+1 = 4 (06 okt).
        # Was (it. 6): 5 items incl. productblog-items; die vallen nu af (US-021 c1, besluit open punten D).
        gekozen = mix.uitgelicht(self.items, self.cfg, self.vandaag)
        self.assertEqual([i["titel"] for i in gekozen], [
            "Nederlandse overheid kiest Microsoft",          # 6, 07 okt
            "Computable: n8n en Zapier in de gemeente",      # 6, 05 okt (gelijke score, ouder: na de 07 okt)
            "Computable: nieuwe AVG-regels"])                # 4, 06 okt

    def test_US018_c3_term_telt_een_keer_per_item_en_headnieuws_is_2(self):
        head = mix.headnieuws_bronnen(self.cfg)
        self.assertEqual(head, {"Computable"})
        mkb = o._patroon("MKB")
        self.assertEqual(mix.score({"titel": "MKB en MKB en MKB", "samenvatting": "MKB", "bron": "Fixture A"}, head, [mkb]), 1)
        self.assertEqual(mix.score({"titel": "Gewone titel", "samenvatting": "", "bron": "Computable"}, head, []), 2)

    def test_US018_c3_score_telt_titel_en_samenvatting_en_hele_woorden(self):
        head = mix.headnieuws_bronnen(self.cfg)
        p = [o._patroon("MKB"), o._patroon("Fabric")]
        self.assertEqual(mix.score({"titel": "Fabricator", "samenvatting": "over MKB", "bron": "Fixture A"}, head, p), 1,
                         "'Fabric' matcht niet in 'Fabricator'; 'MKB' in de samenvatting telt wel")


class TestUS018Statisch(unittest.TestCase):
    """c2, c4, c5 op de statische site met vaste peildatum."""
    @classmethod
    def bouw_met(cls, items):
        tmp = h.nieuwe_tijdelijke_map()
        pad = os.path.join(tmp, "nieuws.json")
        with open(pad, "w", encoding="utf-8") as f:
            json.dump({"bijgewerkt": h.FIXTURE_BIJGEWERKT, "items": items}, f, ensure_ascii=False)
        site = os.path.join(tmp, "site")
        rc, out, err = h.bouw(site, data=pad, vandaag=h.FIXTURE_VANDAAG)
        return tmp, rc, err, site

    @classmethod
    def setUpClass(cls):
        v = datetime.date.fromisoformat(h.FIXTURE_VANDAAG)
        cls.tmp, cls.rc, cls.err, cls.site = cls.bouw_met(k_fixture(v))
        assert cls.rc == 0, cls.err
        cls.p = h.lees(os.path.join(cls.site, "index.html"))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_US018_c2_uitgelicht_staat_boven_de_tellertegels(self):
        self.assertIn('id="blok-uitgelicht"', self.p)
        self.assertLess(self.p.index('id="blok-uitgelicht"'), self.p.index('class="tegels"'))

    def test_US018_c2_max_5_items_uit_laatste_3_dagen_hooguit_2_ai(self):
        titels_uit = blok_titels(blok(self.p, "blok-uitgelicht"))
        self.assertLessEqual(len(titels_uit), 5)
        self.assertEqual(titels_uit, UIT_VERWACHT, "Uitgelicht: %s" % titels_uit)
        cats = re.findall(r'<span class="tag">([^<]+)</span>', blok(self.p, "blok-uitgelicht"))
        self.assertLessEqual(cats.count("AI"), 2)

    def test_US018_c2_uitgelicht_item_toont_titel_link_bron_datum_categorie(self):
        b = blok(self.p, "blok-uitgelicht")
        items = re.findall(r'<li><a href="([^"]+)"[^>]*>([^<]+)</a><div class="meta"><span class="tag">([^<]+)</span>'
                           r'<span>([^<]+)</span><span>([^<]+)</span></div></li>', b)
        self.assertEqual(len(items), len(UIT_VERWACHT))
        for href, titel, cat, bron, datum in items:
            self.assertTrue(href.startswith("https://"), href)
            self.assertIn('target="_blank"', b)
            self.assertIn(bron, ["Computable"])  # it. 7: de fixture-bron is een headnieuws-feed (zie item())
            self.assertRegex(datum, r"^\d{1,2} [a-z]{3} \d{4}$")
            self.assertIn(cat, ["BI", "Data", "Automatisering", "AI"])

    def test_US018_c5_vaknieuws_is_de_5_nieuwste_die_niet_in_uitgelicht_staan(self):
        uit = blok_titels(blok(self.p, "blok-uitgelicht"))
        vak = blok_titels(blok(self.p, "blok-nieuws"))
        self.assertEqual(vak, VAK_VERWACHT)
        self.assertEqual(set(uit) & set(vak), set(), "een item staat in Uitgelicht en in vaknieuws")

    def test_US018_c4_minder_dan_5_items_toont_alleen_de_beschikbare(self):
        v = datetime.date.fromisoformat(h.FIXTURE_VANDAAG)
        tmp, rc, err, site = self.bouw_met([item("Artikel k0 (BI)", "BI", terug(v, 0), n=1),
                                           item("Artikel k1 (Data)", "Data", terug(v, 1), n=2)])
        try:
            self.assertEqual(rc, 0, err)
            p = h.lees(os.path.join(site, "index.html"))
            self.assertEqual(blok_titels(blok(p, "blok-uitgelicht")), ["Artikel k0 (BI)", "Artikel k1 (Data)"])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_US018_c4_nul_items_toont_nog_geen_uitgelicht_nieuws_zonder_fout(self):
        v = datetime.date.fromisoformat(h.FIXTURE_VANDAAG)
        oud = [item("Artikel k%d (BI)" % k, "BI", terug(v, k), n=10 + k) for k in range(4, 8)]
        tmp, rc, err, site = self.bouw_met(oud)
        try:
            self.assertEqual(rc, 0, err)
            p = h.lees(os.path.join(site, "index.html"))
            self.assertIn("Nog geen uitgelicht nieuws", blok(p, "blok-uitgelicht"))
            self.assertEqual(blok_titels(blok(p, "blok-nieuws")), ["Artikel k4 (BI)", "Artikel k5 (BI)",
                                                                  "Artikel k6 (BI)", "Artikel k7 (BI)"])
            self.assertNotIn("Traceback", err)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


@unittest.skip("VERVALLEN iteratie 7 (US-020): lokale app verwijderd; dekking op de statische site in TestUS018Statisch")
class TestUS018Lokaal(unittest.TestCase):
    """c2, c4, c5 in de lokale app (klokdatum van de test); en het BI-filter (US-016 c7) in de lokale app."""

    def _items(self, vandaag):
        return k_fixture(vandaag)

    def test_US018_c2_lokale_app_uitgelicht_boven_tegels_en_juiste_items(self):
        v = datetime.date.today()
        self.schrijf(self._items(v))
        p = self.pagina("/")
        self.assertLess(p.index('id="blok-uitgelicht"'), p.index('class="tegels"'))
        self.assertEqual(blok_titels(blok(p, "blok-uitgelicht")), UIT_VERWACHT)

    def test_US018_c5_lokale_app_vaknieuws_is_de_5_nieuwste_niet_in_uitgelicht(self):
        v = datetime.date.today()
        self.schrijf(self._items(v))
        p = self.pagina("/")
        self.assertEqual(blok_titels(blok(p, "blok-nieuws")), VAK_VERWACHT)

    def test_US018_c4_lokale_app_nul_items_nog_geen_uitgelicht_nieuws(self):
        v = datetime.date.today()
        self.schrijf([item("Artikel k%d (BI)" % k, "BI", terug(v, k), n=10 + k) for k in range(4, 8)])
        p = self.pagina("/")
        self.assertIn("Nog geen uitgelicht nieuws", blok(p, "blok-uitgelicht"))

    def test_US016_c7_lokale_app_categorie_bi_filter_en_chip(self):
        v = datetime.date.today()
        items = self._items(v)
        self.schrijf(items)
        p = self.pagina("/nieuws", {"categorie": ["bi"]})
        self.assertEqual(len(re.findall(r'<article class="kaart">', p)), len([i for i in items if i["categorie"] == "BI"]))
        self.assertIn(">BI</a>", p, "BI-filterknop ontbreekt")


@unittest.skipUnless(hb.EDGE, hb.SLA_OVER)
class TestUS018Browser(unittest.TestCase):
    """c6: startpagina met Uitgelicht op 375 en 1280 px, en geen console-fouten."""
    @classmethod
    def setUpClass(cls):
        cls.tmp = h.nieuwe_tijdelijke_map()
        cls.map = os.path.join(cls.tmp, "site")
        v = datetime.date.fromisoformat(h.FIXTURE_VANDAAG)
        pad = os.path.join(cls.tmp, "nieuws.json")
        with open(pad, "w", encoding="utf-8") as f:
            json.dump({"bijgewerkt": h.FIXTURE_BIJGEWERKT, "items": k_fixture(v)}, f, ensure_ascii=False)
        rc, out, err = h.bouw(cls.map, data=pad, vandaag=h.FIXTURE_VANDAAG)
        assert rc == 0, err
        cls.site = hb.Site(cls.map)

    @classmethod
    def tearDownClass(cls):
        cls.site.stop()
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_US018_c6_startpagina_375_px_en_1280_px_geen_horizontaal_scrollen(self):
        for w in (375, 1280):
            r = self.site.meting("/index.html", w)
            self.assertFalse(r["horizontalOverflow"], "%d px: horizontaal scrollen (%s)" % (w, r["buitenBeeld"]))
        self.assertTrue(self.site.meting("/index.html", 375)["navInView"])

    def test_US018_c6_startpagina_zonder_console_fouten(self):
        dom, errs = self.site.laad("/index.html")
        self.assertEqual(errs, [], "console-fouten: %s" % errs)
        self.assertIn("Uitgelicht", dom)


if __name__ == "__main__":
    unittest.main()
