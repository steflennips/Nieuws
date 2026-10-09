"""Acceptatietests US-016 (evenwichtige mix, BI als eigen categorie, AI-plafond, feedruil), iteratie 6.

- c1 configuratie: vier categorieen (BI, Data, Automatisering, AI), minstens 15 trefwoorden, verplichte termen.
- c2 gelijkspel: meeste treffers wint; bij gelijkspel de volgorde BI, Data, Automatisering, AI.
- c3 een AI-trefwoord alleen in de samenvatting telt niet mee.
- c4 AI-plafond: 80 AI + 20 overige items -> 13 AI + 20; de site, tellers en Overzicht gebruiken alleen de getoonde items.
- c5 feeds: max. 10, min. 3 NL en 3 EN, min. 2 BI-feeds, min. 2 algemene NL-bronnen; elke feed in het feedbesluit en op de bronnenlijst.
- c6 meting (echte ophaalronde, meldpunt): NIET AUTOMATISCH; zie het testrapport.
- c7 Overzicht en Nieuws op 375 en 1280 px: tellertegels/filterknoppen Alle, BI, Data, Automatisering, AI; categorie=bi werkt.
  (Browser; zonder headless Edge: NIET GETEST.)

Geen internet. config/feeds.json en het feedbesluit worden alleen gelezen. Fixtures staan in tijdelijke mappen.
"""
import sys
sys.dont_write_bytecode = True  # vóór de imports hieronder: geen __pycache__ in src/ (iteratie 8)

import datetime
import html as htmllib
import json
import os
import re
import shutil
import unittest
from fractions import Fraction

import hulp_statisch as h
import hulp_browser as hb
sys.path.insert(0, os.path.join(h.ROOT, "src"))
import mix  # noqa: E402
import ophalen as o  # noqa: E402

with open(h.PROJECT_CONFIG, encoding="utf-8") as f:
    CFG = json.load(f)
MATCHERS = o.maak_matchers(CFG["trefwoorden"], CFG.get("uitsluitingen"))
FEEDBESLUIT = os.path.join(h.ROOT, "docs", "decisions", "2026-10-08-nieuwsfeeds.md")
CATEGORIEEN = ["BI", "Data", "Automatisering", "AI"]
# Iteratie 7 (besluit 2026-10-09-criteria-feedruil-it7.md): geen vaste feednamen meer. "Vooral BI/analytics" wordt
# op de naam van de feed getoetst met een regel, zodat een feedruil de test niet breekt.
BI_PATROON = re.compile(r"power bi|fabric|sqlbi|analytics|\bbi\b|\bdata\b|dbt|snowflake|databricks|tableau|qlik|looker",
                        re.I)


def cat(titel, samenvatting=""):
    return o.categoriseer(titel, samenvatting, MATCHERS)


def norm(woord):
    return woord.rstrip("*").casefold()


def item(n, categorie, datum, titel=None, bron="Fixture Bron A"):
    return {"id": "m%04d" % n, "titel": titel or ("Artikel %d (%s)" % (n, categorie)), "categorie": categorie,
            "bron": bron, "taal": "nl", "datum": datum, "samenvatting": "Verzonnen testtekst.",
            "url": "https://voorbeeld-bron.example/mix-%04d" % n}


def schrijf(map, items):
    pad = os.path.join(map, "nieuws.json")
    with open(pad, "w", encoding="utf-8") as f:
        json.dump({"bijgewerkt": h.FIXTURE_BIJGEWERKT, "items": items}, f, ensure_ascii=False)
    return pad


def dag(n):
    return (datetime.date(2026, 7, 1) + datetime.timedelta(days=n)).isoformat()


def ai_plafond_fixture():
    """80 AI-items (oudste 2026-07-01 .. nieuwste 2026-09-18) + 20 overige items (BI, Data, Automatisering)."""
    items = [item(n, "AI", dag(n)) for n in range(80)]
    overig = ["BI", "Data", "Automatisering"]
    items += [item(100 + n, overig[n % 3], "2026-10-0%d" % (1 + n % 5)) for n in range(20)]
    return items


def c7_fixture():
    """Voor de browsertests: 3 BI, 2 Data, 2 Automatisering, 3 AI (geen AI-plafond-effect)."""
    cats = ["BI"] * 3 + ["Data"] * 2 + ["Automatisering"] * 2 + ["AI"] * 3
    return [item(200 + n, c, "2026-10-0%d" % (1 + n % 8)) for n, c in enumerate(cats)]


class TestUS016Config(unittest.TestCase):
    def test_US016_c1_precies_vier_categorieen_bi_data_automatisering_ai(self):
        self.assertEqual(set(CFG["trefwoorden"].keys()), set(CATEGORIEEN))
        self.assertEqual(mix.CATEGORIEEN, CATEGORIEEN)

    def test_US016_c1_minstens_15_trefwoorden_per_categorie_nl_en(self):
        nl = {"BI": {"rapportage*", "stuurinformatie", "managementinformatie", "visualisatie*"},
              "Data": {"gegevens", "datakwaliteit", "databeheer", "datagedreven"},
              "Automatisering": {"geautomati*", "procesoptimalisatie", "bedrijfsprocessen", "robotisering"},
              "AI": {"kunstmatige intelligentie", "machinaal leren", "taalmodel*"}}
        en = {"BI": {"data visualization", "self-service bi", "business intelligence"},
              "Data": {"data science", "big data", "analytics"},
              "Automatisering": {"robotic process", "business process*", "low-code"},
              "AI": {"machine learning", "large language model*", "generative"}}
        for c in CATEGORIEEN:
            woorden = CFG["trefwoorden"][c]
            self.assertGreaterEqual(len(woorden), 15, "%s heeft %d trefwoorden" % (c, len(woorden)))
            self.assertTrue(nl[c] & set(woorden), "%s: geen Nederlands trefwoord" % c)
            self.assertTrue(en[c] & set(woorden), "%s: geen Engels trefwoord" % c)

    def test_US016_c1_bi_data_automatisering_bevatten_verplichte_termen(self):
        kw = {norm(w) for w in CFG["trefwoorden"]["BI"]}
        for t in ["power bi", "microsoft fabric", "qlik", "tableau", "looker", "dashboard", "rapportage", "kpi",
                  "business intelligence"]:
            self.assertIn(t, kw, "BI mist: %s" % t)
        self.assertIn("dbt", {norm(w) for w in CFG["trefwoorden"]["Data"]})
        self.assertIn("snowflake", {norm(w) for w in CFG["trefwoorden"]["Data"]})
        kw_a = {norm(w) for w in CFG["trefwoorden"]["Automatisering"]}
        for t in ["n8n", "zapier", "power automate", "rpa"]:
            self.assertIn(t, kw_a, "Automatisering mist: %s" % t)


class TestUS016Categorie(unittest.TestCase):
    def test_US016_c2_gelijkspel_bi_en_andere_volgorde_bi_data_automatisering_ai(self):
        gevallen = [
            ("Dashboard met AI-assistent", "BI", "gelijkspel BI/AI"),
            ("Dataset met Tableau", "BI", "gelijkspel BI/Data"),
            ("Snowflake en Qlik", "BI", "gelijkspel BI/Data (Qlik)"),
            ("Dataset en RPA", "Data", "gelijkspel Data/Automatisering"),
            ("n8n en ChatGPT", "Automatisering", "gelijkspel Automatisering/AI"),
            ("AI AI dataset", "AI", "meeste treffers (2 AI tegen 1 Data) wint"),
        ]
        for titel, verwacht, uitleg in gevallen:
            self.assertEqual(cat(titel), verwacht, "%s: %s" % (uitleg, titel))

    def test_US016_c2_volgorde_in_config_is_bi_data_automatisering_ai(self):
        self.assertEqual(o.VOLGORDE_GELIJKSPEL, CATEGORIEEN)

    def test_US016_c3_ai_alleen_in_samenvatting_telt_niet_mee(self):
        self.assertIsNone(cat("Nieuwe tool voor het mkb", "Werkt met AI en chatbots"), "AI alleen in samenvatting")
        self.assertIsNone(cat("Nieuwe tool voor het mkb", "Werkt met ChatGPT"), "ChatGPT alleen in samenvatting")

    def test_US016_c3_ai_in_titel_telt_en_samenvatting_van_bi_telt_wel(self):
        self.assertEqual(cat("ChatGPT voor het mkb", ""), "AI")
        self.assertEqual(cat("Nieuwe Power BI-release", "Met AI-functies"), "BI")

    def test_US016_c3_item_met_ai_alleen_in_samenvatting_wordt_niet_opgeslagen(self):
        ruw = [{"titel": "Nieuwe tool voor het mkb", "link": "https://voorbeeld-bron.example/c3-a",
                "samenvatting_html": "Werkt met AI en chatbots", "datum": datetime.date(2026, 10, 8)},
               {"titel": "ChatGPT voor het mkb", "link": "https://voorbeeld-bron.example/c3-b",
                "samenvatting_html": "", "datum": datetime.date(2026, 10, 8)}]
        uit, zonder_titel, zonder_cat = o.verwerk_items(ruw, {"naam": "Fixture", "taal": "nl"}, MATCHERS,
                                                        datetime.date(2026, 10, 8))
        self.assertEqual([i["categorie"] for i in uit], ["AI"])
        self.assertEqual(zonder_cat, 1, "het item zonder AI-treffer in de titel moet als 'zonder categorie' tellen")


class TestUS016AIPlafond(unittest.TestCase):
    def test_US016_c4_mix_80_ai_en_20_overig_geeft_13_ai_en_20_overig(self):
        items = ai_plafond_fixture()
        getoond = mix.beperk_ai(items)
        self.assertEqual(len([i for i in getoond if i["categorie"] != "AI"]), 20, "alle 20 overige items moeten blijven")
        ai = sorted((i for i in getoond if i["categorie"] == "AI"), key=lambda i: i["datum"])
        self.assertEqual(len(ai), 13, "precies 13 AI-items (AI <= 40%)")
        self.assertEqual({i["id"] for i in ai}, {i["id"] for i in items if i["categorie"] == "AI" and i["datum"] >= dag(67)},
                         "het moeten de 13 nieuwste AI-items zijn")
        self.assertEqual(len(getoond), 33)

    def test_US016_c4_ai_aandeel_nooit_boven_40_procent_en_maximaal(self):
        """Voor 0..200 overige items: AI-aandeel <= 40% (exact gerekend) en 1 AI meer zou boven 40% uitkomen."""
        grens = Fraction(2, 5)
        for n_overig in range(0, 201):
            overig = [item(n, "BI", dag(0)) for n in range(n_overig)]
            ai = [item(1000 + n, "AI", dag(n % 100)) for n in range(200)]
            k = len([i for i in mix.beperk_ai(overig + ai) if i["categorie"] == "AI"])
            if k + n_overig:
                self.assertLessEqual(Fraction(k, k + n_overig), grens, "n_overig=%d: %d AI" % (n_overig, k))
            if k < 200:  # er zijn 200 AI-items beschikbaar
                self.assertGreater(Fraction(k + 1, k + 1 + n_overig), grens,
                                   "n_overig=%d: %d AI kan niet naar beneden afgerond zijn" % (n_overig, k))

    def test_US016_c4_site_nieuws_tellers_en_overzicht_tonen_alleen_de_getoonde_items(self):
        tmp = h.nieuwe_tijdelijke_map()
        try:
            data = schrijf(tmp, ai_plafond_fixture())
            site = os.path.join(tmp, "site")
            rc, out, err = h.bouw(site, data=data, vandaag=h.FIXTURE_VANDAAG)
            self.assertEqual(rc, 0, err)
            nieuws = h.lees(os.path.join(site, "nieuws.html"))
            urls = re.findall(r'<article class="kaart" data-categorie="([^"]*)"[^>]*>\s*<h2><a href="([^"]+)"', nieuws)
            self.assertEqual(len(urls), 33, "Nieuws toont %d items, verwacht 33" % len(urls))
            self.assertEqual(sum(1 for c, _ in urls if c == "AI"), 13)
            self.assertIn('id="aantal">33 nieuwsitems', nieuws)
            index = h.lees(os.path.join(site, "index.html"))
            self.assertEqual(re.search(r'id="teller-ai">(\d+)<', index).group(1), "13")
            self.assertEqual(sum(int(re.search(r'id="teller-%s">(\d+)<' % c, index).group(1))
                                 for c in ["bi", "data", "automatisering", "ai"]), 33)
            # US-022 c1 (it. 8; was: '<span class="totaal">33 in totaal</span>'): geen totaal van alle items meer.
            self.assertNotIn("in totaal", index, "totaal van alle items staat nog op de startpagina")
            self.assertIn(">Alle 33 berichten bekijken</a>", index)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    @unittest.skip("VERVALLEN iteratie 7 (US-020): de lokale app (logica.py) is verwijderd; het plafond wordt getest via bouw in test_US016_c4_*")
    def test_US016_c4_lokale_app_gebruikt_hetzelfde_plafond(self):
        import data as app_data
        import logica
        items = ai_plafond_fixture()
        getoond = logica.filter_nieuws(items=items)
        self.assertEqual(len(getoond), 33)
        self.assertEqual(len([i for i in getoond if i["categorie"] == "AI"]), 13)
        self.assertEqual(len(logica.filter_nieuws("AI", items=items)), 13, "filter AI toont dezelfde 13")
        self.assertIn("BI", app_data.CATEGORIEEN)


class TestUS016Feeds(unittest.TestCase):
    def test_US016_c5_max_10_feeds_minstens_3_nl_en(self):
        feeds = CFG["feeds"]
        self.assertLessEqual(len(feeds), 10)
        self.assertGreaterEqual(len([f for f in feeds if f["taal"] == "nl"]), 3)
        self.assertGreaterEqual(len([f for f in feeds if f["taal"] == "en"]), 3)

    def test_US016_c5_minstens_2_bi_feeds_en_2_algemene_nl_bronnen(self):
        bi = [f for f in CFG["feeds"] if BI_PATROON.search(f["naam"])]
        self.assertGreaterEqual(len(bi), 2, "minstens 2 BI/analytics-feeds (op naam): %s" % [f["naam"] for f in bi])
        algemeen_nl = [f for f in CFG["feeds"] if f["taal"] == "nl" and not BI_PATROON.search(f["naam"])]
        self.assertGreaterEqual(len(algemeen_nl), 2, "minstens 2 algemene NL tech/business-bronnen")

    def test_US016_c5_elke_feed_in_feedbesluit_met_robots_gratis_en_geen_login(self):
        with open(FEEDBESLUIT, encoding="utf-8") as f:
            besluit = f.read()
        for feed in CFG["feeds"]:
            self.assertIn(feed["url"], besluit, "feed ontbreekt in nieuwsfeeds.md: %s" % feed["naam"])
        self.assertIn("robots", besluit.lower())
        self.assertIn("gratis", besluit.lower())
        self.assertIn("geen login", besluit.lower())

    def test_US016_c5_elke_feed_staat_op_de_bronnenlijst(self):
        tmp = h.nieuwe_tijdelijke_map()
        try:
            data = schrijf(tmp, c7_fixture())
            site = os.path.join(tmp, "site")
            rc, out, err = h.bouw(site, data=data, vandaag=h.FIXTURE_VANDAAG)
            self.assertEqual(rc, 0, err)
            bronnen = h.lees(os.path.join(site, "bronnen.html"))
            for feed in CFG["feeds"]:
                self.assertIn(htmllib.escape(feed["naam"]), bronnen, "bronnenlijst mist: %s" % feed["naam"])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class TestUS016Vervallen(unittest.TestCase):
    """US-015 c12 (feed-aandeel, hard) is vervangen door US-016 c6 (meldpunt). Die vervanging moet in de backlog staan,
    en het oude harde criterium mag niet meer als automatische test terugkomen."""

    def test_US015_c12_is_vervangen_door_US016_c6_in_backlog(self):
        backlog = h.lees(os.path.join(h.ROOT, "docs", "BACKLOG.md"))
        self.assertIn("c12 vervangen door US-016 c6", backlog)
        self.assertIn("(Vervangt US-015 c12.)", backlog)
        self.assertIn("niet hard getoetst", backlog)


@unittest.skipUnless(os.path.exists(h.PROJECT_DATA), "NIET GETEST: data/nieuws.json ontbreekt in het project")
class TestUS016EchteData(unittest.TestCase):
    """US-016 c4 op de echte data (alleen-lezen): het AI-aandeel op de site is hooguit 40%."""

    def test_US016_c4_echte_data_ai_aandeel_op_site_hooguit_40_procent(self):
        tmp = h.nieuwe_tijdelijke_map()
        try:
            site = os.path.join(tmp, "site")
            rc, out, err = h.bouw(site, data=h.PROJECT_DATA)
            self.assertEqual(rc, 0, err)
            nieuws = h.lees(os.path.join(site, "nieuws.html"))
            cats = re.findall(r'<article class="kaart" data-categorie="([^"]*)"', nieuws)
            self.assertGreater(len(cats), 0)
            self.assertLessEqual(cats.count("AI") / len(cats), 0.4 + 1e-9, "AI %d van %d" % (cats.count("AI"), len(cats)))
            with open(h.PROJECT_DATA, encoding="utf-8") as f:
                alle = json.load(f)["items"]
            self.assertEqual(len(cats), len(h.verwacht_getoond([i for i in alle if i.get("categorie") in CATEGORIEEN])))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class TestUS016Filter(unittest.TestCase):
    """US-016 c7 (statische site, zonder browser): de filterknoppen en de categorie-URL."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = h.nieuwe_tijdelijke_map()
        cls.site = os.path.join(cls.tmp, "site")
        data = schrijf(cls.tmp, c7_fixture())
        rc, out, err = h.bouw(cls.site, data=data, vandaag=h.FIXTURE_VANDAAG)
        assert rc == 0, err

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_US016_c7_nieuws_heeft_filterknoppen_alle_bi_data_automatisering_ai(self):
        p = h.lees(os.path.join(self.site, "nieuws.html"))
        knoppen = re.findall(r'<a class="chip[^"]*"[^>]*>([^<]+)</a>', p)
        self.assertEqual(knoppen, ["Alle", "BI", "Data", "Automatisering", "AI"])

    def test_US016_c7_overzicht_heeft_tegels_bi_data_automatisering_ai(self):
        p = h.lees(os.path.join(self.site, "index.html"))
        labels = re.findall(r'<span class="label">([^<]+)</span>', p)
        self.assertEqual(labels, ["BI", "Data", "Automatisering", "AI"])

    def test_US016_c7_categorie_bi_in_url_filtert_en_is_hoofdletterongevoelig(self):
        p = h.lees(os.path.join(self.site, "nieuws.html"))
        # Het filter gebeurt in de browser (app.js); hier controleren we dat de categorie-code in JS staat en dat
        # de kaarten het juiste data-categorie-attribuut hebben. De browsercontrole staat in TestUS016Browser.
        self.assertIn('data-categorie="BI"', p)
        js = h.lees(os.path.join(self.site, "app.js"))
        self.assertIn("toLowerCase", js, "filter in URL moet hoofdletterongevoelig zijn (US-007 c2)")


@unittest.skipUnless(hb.EDGE, hb.SLA_OVER)
class TestUS016Browser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = h.nieuwe_tijdelijke_map()
        cls.map = os.path.join(cls.tmp, "site")
        data = schrijf(cls.tmp, c7_fixture())
        rc, out, err = h.bouw(cls.map, data=data, vandaag=h.FIXTURE_VANDAAG)
        assert rc == 0, err
        cls.site = hb.Site(cls.map)

    @classmethod
    def tearDownClass(cls):
        cls.site.stop()
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_US016_c7_browser_categorie_bi_toont_alleen_bi_en_juist_aantal(self):
        dom, errs = self.site.laad("/nieuws.html?categorie=bi")
        zichtbaar = h.zichtbare_kaarten(dom)
        self.assertEqual(len(zichtbaar), 3)
        self.assertTrue(all(k["cat"] == "BI" for k in zichtbaar))
        self.assertEqual(h.element_tekst(dom, "aantal")[0], "3 nieuwsitems")
        self.assertEqual(errs, [], "console-fouten: %s" % errs)

    def test_US016_c7_browser_tellers_op_overzicht(self):
        dom, errs = self.site.laad("/index.html")
        self.assertEqual([h.element_tekst(dom, "teller-" + c)[0] for c in ["bi", "data", "automatisering", "ai"]],
                         ["3", "2", "2", "3"])
        self.assertEqual(errs, [])

    def test_US016_c7_browser_375_en_1280_px_geen_horizontaal_scrollen(self):
        for pad in ["/index.html", "/nieuws.html"]:
            r = self.site.meting(pad, 375)
            self.assertFalse(r["horizontalOverflow"], "%s bij 375 px (%s)" % (pad, r["buitenBeeld"]))
            self.assertTrue(r["navInView"], "%s: navigatie niet volledig in beeld bij 375 px" % pad)
            self.assertFalse(self.site.meting(pad, 1280)["horizontalOverflow"], "%s bij 1280 px" % pad)


# ---------- US-016 c8-c10 (fixronde 1, iteratie 6; besluit docs/decisions/2026-10-09-fixronde1-it6.md) ----------
# De drie NOS-titels met hun echte samenvatting (uit de ophaalronde van 8 okt 2026, opgeslagen tekst; afgekapt op 300 tekens).
NOS_HACKS = [
    ("Amsterdammer opgepakt in onderzoek naar hackerscollectief ShinyHunters",
     "Een man van 24 uit Amsterdam is opgepakt voor betrokkenheid bij ShinyHunters, zegt de politie. Dat hackerscollectief is "
     "onder meer bekend van de grootschalige aanval op Odido eerder dit jaar, waarbij gegevens van miljoenen Nederlanders werden "
     "gestolen. De Amsterdammer moet morgen voor de rechtban..."),
    ("Hackers persen klanten boodschappendienst Flink af: betalen of data gepubliceerd",
     "Een voorheen onbekende hackergroep claimt te hebben ingebroken bij boodschappenbezorger Flink. De hackers benaderen "
     "momenteel medewerkers en klanten met een ultimatum: als ze niet betalen, worden hun gegevens gepubliceerd. Het gaat om een "
     "bedrag van circa 10 tot 15 euro aan cryptovaluta per perso..."),
    ("Datalek bij reisapp Polarsteps: iedereen kon meekijken, ook met afgeschermde reizen",
     "De in Nederland opgerichte en wereldwijd populaire reisapp Polarsteps heeft zeker een halfjaar de gegevens van zijn gebruikers "
     "onvoldoende beschermd. Onderzoeksplatform Follow The Money (FTM) ontdekte dat via een lek in de beveiliging van de app "
     "reisinformatie van miljoenen reizigers kon worden v..."),
]


class TestUS016Kwaliteit(unittest.TestCase):
    # c8: los "gegevens" is geen Data-trefwoord; samenstellingen wel
    def test_US016_c8_los_gegevens_is_geen_data_trefwoord(self):
        self.assertNotIn("gegevens", CFG["trefwoorden"]["Data"], "'gegevens' staat nog als los Data-trefwoord")
        for samenstelling in ["gegevensanalyse", "gegevensbeheer", "gegevenskwaliteit"]:
            self.assertIn(samenstelling, CFG["trefwoorden"]["Data"], "samenstelling ontbreekt: %s" % samenstelling)
        self.assertEqual(cat("Gegevensanalyse van klantdata", ""), "Data",
                         "samenstelling gegevensanalyse moet Data geven")
        self.assertNotEqual(cat("Gegevens over klanten bewaren", ""), "Data", "los 'gegevens' geeft Data")

    def test_US016_c8_drie_nos_titels_met_echte_samenvatting_krijgen_geen_data(self):
        for titel, samen in NOS_HACKS:
            self.assertNotEqual(cat(titel, samen), "Data", "%r krijgt ten onrechte Data" % titel)

    # c9: ongeldige datum -> item overslaan met melding (titel of link), overige items getoond, exitcode 0
    def test_US016_c9_ongeldige_datum_wordt_overgeslagen_met_melding_bouw_gaat_door(self):
        tmp = h.nieuwe_tijdelijke_map()
        try:
            goed = [item(1, "BI", "2026-10-07", titel="Dashboards voor de zorg"),
                    item(2, "Automatisering", "2026-10-06", titel="Low-code tools winnen terrein"),
                    item(3, "Data", "2026-10-05", titel="Datawarehouse-keuze voor het mkb")]
            slecht = item(4, "Data", "garbage", titel="Kapotte datum artikel")
            data = schrijf(tmp, goed + [slecht])
            uit = os.path.join(tmp, "site")
            rc, out, err = h.bouw(uit, data=data, vandaag=h.FIXTURE_VANDAAG)
            self.assertEqual(rc, 0, "bouw breekt af door ongeldige datum: %s %s" % (out, err))
            melding = out + err
            self.assertTrue("Kapotte datum artikel" in melding or slecht["url"] in melding,
                            "geen melding met titel of link van het overgeslagen item: %s" % melding)
            nieuws = h.lees(os.path.join(uit, "nieuws.html"))
            for g in goed:
                self.assertIn(g["titel"], nieuws, "goed item ontbreekt na overslaan: %s" % g["titel"])
            self.assertNotIn("Kapotte datum artikel", nieuws, "item met ongeldige datum is toch getoond")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    # c10: alleen AI-items -> exitcode 1, melding noemt het AI-plafond (niet "bevat geen nieuwsitems")
    def test_US016_c10_alleen_ai_items_geeft_exitcode_1_en_melding_ai_plafond(self):
        tmp = h.nieuwe_tijdelijke_map()
        try:
            data = schrijf(tmp, [item(n, "AI", "2026-10-0%d" % (1 + n % 8)) for n in range(10)])
            uit = os.path.join(tmp, "site")
            rc, out, err = h.bouw(uit, data=data, vandaag=h.FIXTURE_VANDAAG)
            self.assertEqual(rc, 1, "exitcode bij alleen-AI-data moet 1 zijn: %s" % (out + err))
            melding = (out + err).lower()
            self.assertIn("AI", out + err, "melding noemt AI niet")
            self.assertTrue("plafond" in melding and "40" in melding,
                            "melding noemt het AI-plafond (max 40%%) niet: %s" % (out + err))
            self.assertNotIn("bevat geen nieuwsitems", melding, "misleidende melding: %s" % (out + err))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
