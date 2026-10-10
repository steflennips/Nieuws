"""Eigen tests iteratie 6-7: US-016 (4 categorieen, AI-plafond), US-017 (kwaliteitsfilter), US-018/US-021 (Uitgelicht)."""
import json
import os
import re
import sys
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

BASIS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASIS / "src"))
import bouw  # noqa: E402
import mix  # noqa: E402
import ophalen  # noqa: E402

CFG = json.loads((BASIS / "config" / "feeds.json").read_text(encoding="utf-8"))
M = ophalen.maak_matchers(CFG["trefwoorden"], CFG.get("uitsluitingen"))
W = ophalen.maak_weigerlijst(CFG)
VANDAAG = date(2026, 10, 8)


def termen(cat):
    return [w.casefold() for w in CFG["trefwoorden"][cat]]


class TestConfigUS016(unittest.TestCase):
    def test_vier_categorieen_met_15_termen(self):
        self.assertEqual(list(CFG["trefwoorden"]), ["BI", "Data", "Automatisering", "AI"])
        for cat in CFG["trefwoorden"]:
            self.assertGreaterEqual(len(CFG["trefwoorden"][cat]), 15, cat)

    def test_verplichte_termen(self):
        bi = " | ".join(termen("BI"))
        for t in ("power bi", "microsoft fabric", "qlik", "tableau", "looker", "dashboard", "rapportage", "kpi", "business intelligence"):
            self.assertIn(t, bi)
        self.assertIn("dbt", termen("Data"))
        self.assertIn("snowflake", termen("Data"))
        for t in ("n8n", "zapier", "power automate", "rpa"):
            self.assertIn(t, termen("Automatisering"))

    def test_feeds(self):
        feeds = CFG["feeds"]
        self.assertLessEqual(len(feeds), 10)
        self.assertGreaterEqual(len([f for f in feeds if f["taal"] == "nl"]), 3)
        self.assertGreaterEqual(len([f for f in feeds if f["taal"] == "en"]), 3)
        bi = [f for f in feeds if re.search(r"power bi|fabric|sqlbi", f["naam"], re.I)]
        self.assertGreaterEqual(len(bi), 2)
        self.assertGreaterEqual(len([f for f in feeds if f.get("headnieuws") and f["taal"] == "nl"]), 2)

    def test_feeds_in_besluit(self):
        tekst = (BASIS / "docs" / "decisions" / "2026-10-08-nieuwsfeeds.md").read_text(encoding="utf-8")
        for f in CFG["feeds"]:
            self.assertIn(f["url"], tekst)

    def test_feeds_in_readme_voorbeeldregel(self):
        readme = (BASIS / "README.technisch.md").read_text(encoding="utf-8")
        m = re.search(r"```\n(\{\"naam\".*?\})\n```", readme, re.S)
        self.assertIsNotNone(m)
        regel = json.loads(m.group(1))
        self.assertIn(regel, CFG["feeds"])


class TestPubliekeReadme(unittest.TestCase):
    """De README.md gaat naar GitHub: alleen bezoekersinformatie, geen lokale paden of werkafspraken."""

    def setUp(self):
        self.tekst = (BASIS / "README.md").read_text(encoding="utf-8")

    def test_geen_lokale_paden(self):
        self.assertIsNone(re.search(r"[A-Za-z]:\\|/Users/|One" + "Drive|Desk" + "top", self.tekst))

    def test_geen_werkafspraken(self):
        for woord in ["/iteratie", "Claude", "Bouwer", "Tester", "Product Owner", "unittest", "CLAUDE.md", "python "]:
            self.assertNotIn(woord, self.tekst, woord)

    def test_bevat_link_en_onderdelen(self):
        for tekst in ["https://steflennips.github.io/Nieuws/", "Uitgelicht", "Vaknieuws", "Bronnen", "06:00"]:
            self.assertIn(tekst, self.tekst)

    def test_technische_readme_niet_in_git(self):
        gi = (BASIS / ".gitignore").read_text(encoding="utf-8").splitlines()
        self.assertIn("README.technisch.md", [r.strip() for r in gi])


class TestCategorieUS016(unittest.TestCase):
    def cat(self, titel, samen=""):
        return ophalen.categoriseer(titel, samen, M)

    def test_bi_wint_van_ai_bij_gelijkspel(self):
        self.assertEqual(self.cat("Copilot in Power BI"), "BI")  # 1 AI (titel), 1 BI

    def test_volgorde_bi_data_automatisering_ai(self):
        self.assertEqual(self.cat("Power BI en dataset"), "BI")  # BI 1, Data 1
        self.assertEqual(self.cat("Dataset en RPA"), "Data")  # Data 1, Autom. 1
        self.assertEqual(self.cat("RPA en ChatGPT"), "Automatisering")  # Autom. 1, AI 1
        self.assertEqual(self.cat("Qlik en OpenAI en RPA"), "BI")  # drie-weg gelijkspel

    def test_meeste_treffers_wint(self):
        self.assertEqual(self.cat("Power BI en Qlik en Tableau met een ChatGPT"), "BI")
        self.assertEqual(self.cat("ChatGPT en Gemini en Claude bij Power BI"), "AI")

    def test_ai_alleen_in_titel(self):
        self.assertIsNone(self.cat("Nieuwe functies voor je team", "Met een slimme AI-assistent en ChatGPT"))
        self.assertEqual(self.cat("Nieuwe RPA-functies", "Met een slimme AI-assistent en ChatGPT"), "Automatisering")
        self.assertEqual(self.cat("Nieuwe AI-functies", ""), "AI")

    def test_bi_termen_hele_woorden(self):
        self.assertEqual(self.cat("Qlik Sense krijgt nieuwe grafieken"), "BI")
        self.assertEqual(self.cat("Looker Studio koppelt Google Sheets"), "BI")
        self.assertEqual(self.cat("Microsoft Fabric voor het mkb"), "BI")
        self.assertIsNone(self.cat("Fabrics en kleding in de winkel"))  # 'fabrics' is geen heel woord 'fabric'


def _it(n, cat, dag=None, bron="B"):
    return {"id": str(n), "titel": "%s %d" % (cat, n), "categorie": cat, "bron": bron,
            "datum": (VANDAAG - timedelta(days=dag if dag is not None else n % 30)).isoformat(),
            "samenvatting": "s", "url": "https://x.test/%s%d" % (cat, n)}


class TestPlafondUS016(unittest.TestCase):
    def test_80_ai_en_20_overig_geeft_20_plus_13(self):
        items = [_it(i, "AI", dag=i % 40) for i in range(80)] + [_it(1000 + i, "Data", dag=i) for i in range(20)]
        uit = mix.beperk_ai(items)
        ai = [i for i in uit if i["categorie"] == "AI"]
        self.assertEqual(len(uit) - len(ai), 20)
        self.assertEqual(len(ai), 13)
        nieuwste = sorted((i["datum"] for i in items if i["categorie"] == "AI"), reverse=True)[:13]
        self.assertEqual(sorted((i["datum"] for i in ai), reverse=True), nieuwste)  # de nieuwste 13

    def test_randgevallen(self):
        self.assertEqual(mix.beperk_ai([_it(i, "AI") for i in range(5)]), [])  # alleen AI: niets
        for n in range(0, 40):
            items = [_it(i, "AI", dag=i) for i in range(50)] + [_it(500 + i, "BI", dag=i) for i in range(n)]
            ai = len([i for i in mix.beperk_ai(items) if i["categorie"] == "AI"])
            self.assertLessEqual(ai, 0.4 * (n + ai) + 1e-9)
            self.assertGreater(ai + 1, 0.4 * (n + ai + 1) - 1e-9) if ai < 50 else None

    def test_site_gebruikt_alleen_getoonde_items(self):
        items = [_it(i, "AI", dag=i % 40) for i in range(80)] + [_it(1000 + i, "Data", dag=i) for i in range(20)]
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            (t / "d.json").write_text(json.dumps({"bijgewerkt": "2026-10-08T04:00:00+00:00", "items": items}), encoding="utf-8")
            (t / "c.json").write_text(json.dumps({"feeds": []}), encoding="utf-8")
            n, _ = bouw.bouw(str(t / "d.json"), str(t / "c.json"), str(t / "s"), VANDAAG)
            self.assertEqual(n, 33)
            idx = (t / "s" / "index.html").read_text(encoding="utf-8")
            nws = (t / "s" / "nieuws.html").read_text(encoding="utf-8")
        self.assertIn('id="teller-ai">13<', idx)
        self.assertIn('id="teller-data">20<', idx)
        self.assertIn('id="teller-bi">0<', idx)
        self.assertEqual(nws.count('<article class="kaart"'), 33)
        self.assertIn("33 nieuwsitems", nws)
        self.assertNotIn("in totaal", idx)
        self.assertIn("Alle 33 berichten bekijken", idx)


class TestKwaliteitUS017(unittest.TestCase):
    TOEGELATEN = [
        "Salesforce rondt overname van Informatica af na deal van 8 miljard",  # 'deal' (enkelvoud) blijft
        "Microsoft sluit deal met Qlik over Power BI-koppeling",
        "Overname van Tableau-partner door Snowflake aangekondigd",
        "ERP-dealer automatiseert orderverwerking met n8n",  # 'dealer' blijft
        "Power BI krijgt nieuwe rapportage-opties",
        "Zo automatiseer je je facturen met Zapier",
    ]
    GEWEIGERD = [
        "Webinar: Power BI voor beginners",
        "Black Friday deals op laptops",
        "Review: nieuwe smartphone met AI",
        "Unboxing van de nieuwe game console",
        "Korting op Microsoft 365 voor het mkb",
        "Hands-on met de nieuwe Surface",
        "Gadgets voor op je bureau",
        "Cloudplatform voor games op de markt",
    ]

    def test_weigeren_titel(self):
        for t in self.GEWEIGERD:
            self.assertTrue(W.reden(t, ""), t)

    def test_toelaten_en_overnames_blijven(self):
        for t in self.TOEGELATEN:
            self.assertIsNone(W.reden(t, ""), t)

    def test_hoofdletterongevoelig_en_hele_woorden(self):
        self.assertTrue(W.reden("WEBINAR over data", ""))
        self.assertTrue(W.reden("Alle DEALS van de week", ""))
        self.assertIsNone(W.reden("Een dealer in data", ""))
        self.assertIsNone(W.reden("Consolidatie van databases", ""))  # 'console*' is geen prefix van 'consolidatie'

    def test_promotie_in_samenvatting(self):
        for woord in ("sponsored", "gesponsord", "partnerbijdrage", "advertorial"):
            self.assertTrue(W.reden("Power BI tips", "Dit is een %s artikel" % woord), woord)
        # andere weigertermen gelden alleen in de titel
        self.assertIsNone(W.reden("Power BI tips", "Met korting op een webinar"))

    def test_config_bevat_verplichte_weigertermen(self):
        lijst = " | ".join(CFG["weigertermen"] + CFG["weigertermen_samenvatting"]).casefold()
        for t in ("webinar", "webcast", "sponsored", "gesponsord", "partnerbijdrage", "advertorial", "aanbieding", "korting",
                  "kortingscode", "deals", "prijsverlaging", "black friday", "review", "unboxing", "hands-on", "smartphone",
                  "game", "console"):
            self.assertIn(t, lijst)
        self.assertNotIn("deal*", lijst)

    def test_verwerk_items_telt_geweigerd(self):
        ruw = [{"titel": "Webinar: Power BI", "link": "https://x.test/1", "samenvatting_html": "x", "datum": VANDAAG},
               {"titel": "Power BI nieuws", "link": "https://x.test/2", "samenvatting_html": "Gesponsord door X", "datum": VANDAAG},
               {"titel": "Power BI nieuws", "link": "https://x.test/3", "samenvatting_html": "ok", "datum": VANDAAG}]
        geweigerd = []
        uit, _, _ = ophalen.verwerk_items(ruw, {"naam": "B", "taal": "en"}, M, VANDAAG, 300, W, geweigerd)
        self.assertEqual([i["url"] for i in uit], ["https://x.test/3"])
        self.assertEqual(len(geweigerd), 2)


HEAD = {"feeds": [{"naam": "NLBron", "url": "https://nl.test/f", "taal": "nl", "headnieuws": True},
                  {"naam": "ENHead", "url": "https://enh.test/f", "taal": "en", "headnieuws": True},
                  {"naam": "ENBron", "url": "https://en.test/f", "taal": "en"}],
        "deux_relevantie": ["MKB", "Power BI", "Microsoft", "AVG"]}


def _ui(naam, bron, titel, dagen, cat="Data", samen=""):
    return {"id": naam, "titel": titel, "categorie": cat, "bron": bron, "samenvatting": samen,
            "datum": (VANDAAG - timedelta(days=dagen)).isoformat(), "url": "https://x.test/" + naam}


class TestUitgelichtUS018(unittest.TestCase):
    """Uitgelicht na US-021: alleen headnieuws-feeds; 2 punten headnieuws, +1 NL-feed, +1 per relevantieterm."""

    def test_scoreregel_volgorde(self):
        items = [
            _ui("a", "ENHead", "Niets bijzonders", 0),                                  # 2
            _ui("b", "NLBron", "Algemeen nieuws", 1),                                   # 2 + 1 = 3
            _ui("c", "ENHead", "Power BI voor het MKB", 2, "BI"),                       # 2 + 2 = 4
            _ui("d", "NLBron", "Microsoft Power BI en AVG", 2, "BI"),                   # 2 + 1 + 3 = 6
            _ui("e", "ENHead", "Power BI Power BI Power BI", 3, "BI"),                  # 2 + 1 (verschillende termen) = 3
            _ui("f", "NLBron", "Oud nieuws", 4),                                        # buiten 3 dagen
            _ui("g", "NLBron", "Nog nieuws over Microsoft", 0),                         # 2 + 1 + 1 = 4
            _ui("h", "ENBron", "Microsoft Power BI en AVG voor het MKB", 0, "BI"),      # geen headnieuws: nooit
        ]
        uit = mix.uitgelicht(items, HEAD, VANDAAG)
        # d=6, g=4 (nieuwer dan c=4), c=4, b=3 (nieuwer dan e=3); a=2 valt af (max 5)
        self.assertEqual([i["id"] for i in uit], ["d", "g", "c", "b", "e"])

    def test_nl_gaat_voor_bij_verder_gelijke_score(self):
        items = [_ui("en", "ENHead", "Gewoon bericht", 0), _ui("nl", "NLBron", "Gewoon bericht", 1)]
        self.assertEqual([i["id"] for i in mix.uitgelicht(items, HEAD, VANDAAG)], ["nl", "en"])

    def test_productblog_met_hoogste_score_staat_niet_in_uitgelicht(self):
        items = [_ui("blog", "ENBron", "Power BI Microsoft AVG MKB", 0, "BI"), _ui("nws", "NLBron", "Nieuws", 1)]
        uit = mix.uitgelicht(items, HEAD, VANDAAG)
        self.assertEqual([i["id"] for i in uit], ["nws"])
        self.assertEqual([i["id"] for i in mix.vaknieuws(items, uit)], ["blog"])

    def test_hooguit_5_en_2_ai(self):
        items = [_ui("ai%d" % i, "NLBron", "AI nieuws %d" % i, 0, "AI") for i in range(4)] +                 [_ui("d%d" % i, "ENHead", "Data %d" % i, 1) for i in range(6)]
        uit = mix.uitgelicht(items, HEAD, VANDAAG)
        self.assertEqual(len(uit), 5)
        self.assertEqual(len([i for i in uit if i["categorie"] == "AI"]), 2)

    def test_geen_aanvulling_met_productblogs_en_leeg(self):
        items = [_ui("a", "NLBron", "x", 1), _ui("b", "NLBron", "y", 9)] + [_ui("p%d" % i, "ENBron", "z", 0) for i in range(10)]
        self.assertEqual([i["id"] for i in mix.uitgelicht(items, HEAD, VANDAAG)], ["a"])
        self.assertEqual(mix.uitgelicht([_ui("p", "ENBron", "y", 0)], HEAD, VANDAAG), [])

    def test_vaknieuws_is_vijf_nieuwste_zonder_uitgelicht(self):
        items = [_ui("i%d" % i, "ENHead", "t%d" % i, i) for i in range(10)]
        uit = mix.uitgelicht(items, HEAD, VANDAAG)  # i0..i3
        vak = mix.vaknieuws(items, uit)
        self.assertEqual([i["id"] for i in vak], ["i4", "i5", "i6", "i7", "i8"])

    def test_config_heeft_relevantietermen_en_headnieuws(self):
        lijst = [t.casefold() for t in CFG["deux_relevantie"]]
        for t in ("mkb", "zzp", "nederland", "nederlandse", "overheid", "gemeente", "avg", "nis2", "ai act", "microsoft",
                  "power bi", "fabric", "qlik", "tableau", "looker", "dbt", "snowflake", "n8n", "zapier"):
            self.assertIn(t, lijst)
        self.assertGreaterEqual(len([f for f in CFG["feeds"] if f.get("headnieuws")]), 2)

    def test_site_blok_uitgelicht_en_leeg(self):
        items = [_ui("a", "NLBron", "Power BI nieuws", 0, "BI"), _ui("b", "ENBron", "Oud nieuws", 20)]  # b: geen headnieuws
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            (t / "d.json").write_text(json.dumps({"bijgewerkt": "2026-10-08T04:00:00+00:00", "items": items}), encoding="utf-8")
            (t / "c.json").write_text(json.dumps(HEAD), encoding="utf-8")
            bouw.bouw(str(t / "d.json"), str(t / "c.json"), str(t / "s"), VANDAAG)
            h = (t / "s" / "index.html").read_text(encoding="utf-8")
            bouw.bouw(str(t / "d.json"), str(t / "c.json"), str(t / "s2"), VANDAAG + timedelta(days=10))
            h2 = (t / "s2" / "index.html").read_text(encoding="utf-8")
        self.assertLess(h.index("Uitgelicht"), h.index('class="tegels"'))  # boven de tegels
        self.assertLess(h.index('class="tegels"'), h.index('id="blok-nieuws"'))
        uit = re.search(r'id="blok-uitgelicht".*?</section>', h, re.S).group(0)
        self.assertEqual(uit.count("<li>"), 1)
        self.assertIn("Power BI nieuws", uit)
        vak = re.search(r'id="blok-nieuws".*?</section>', h, re.S).group(0)
        self.assertNotIn("Power BI nieuws", vak)
        self.assertIn("Oud nieuws", vak)
        self.assertIn("Nog geen uitgelicht nieuws", h2)
        self.assertNotIn("Traceback", h2)

    def test_site_filter_bi_in_js_en_chips(self):
        items = [_ui("a", "NLBron", "Power BI nieuws", 0, "BI")]
        with tempfile.TemporaryDirectory() as t:
            t = Path(t)
            (t / "d.json").write_text(json.dumps({"items": items}), encoding="utf-8")
            (t / "c.json").write_text(json.dumps(HEAD), encoding="utf-8")
            bouw.bouw(str(t / "d.json"), str(t / "c.json"), str(t / "s"), VANDAAG)
            nws = (t / "s" / "nieuws.html").read_text(encoding="utf-8")
            js = (t / "s" / "app.js").read_text(encoding="utf-8")
        self.assertEqual(re.findall(r'data-categorie="([^"]*)" href', nws), ["", "BI", "Data", "Automatisering", "AI"])
        self.assertIn('["BI", "Data", "Automatisering", "AI"]', js)


if __name__ == "__main__":
    unittest.main()
