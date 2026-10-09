"""Regressie op de statische site (iteratie 4): US-008 c1-c8 (stijl), US-001 c3/c5 en US-002 c1 op de site.

Deze criteria gelden voor de openbare statische site (zie BACKLOG, US-012 opmerkingen). De stijlcontroles
gebruiken de helpers uit hulp_stijl.py (zelfde regels als voor de lokale app, die in iteratie 7 is verwijderd),
en lezen de stylesheet en pagina's van de gebouwde statische site (style.css, *.html). Browserlayout staat in
test_US012_browser.py.
"""
import os
import re
import shutil
import sys
import unittest

import hulp_statisch as h
from hulp_stijl import contrast, css_regels, interface_tekst, root_vars, zichtbare_tekst  # noqa: F401

sys.dont_write_bytecode = True
VISION_FONT = "system-ui,-apple-system,\"Segoe UI\",Roboto,Arial,sans-serif"
TMP = None
MAP = None
CSS = None


def setUpModule():
    global TMP, MAP, CSS
    TMP = h.nieuwe_tijdelijke_map()
    MAP = os.path.join(TMP, "site")
    data = h.schrijf_fixture_data(TMP)
    rc, out, err = h.bouw(MAP, data=data, vandaag=h.FIXTURE_VANDAAG)
    if rc != 0:
        raise AssertionError("bouwen voor stijlcontrole faalde: %s" % err)
    with open(os.path.join(MAP, "style.css"), encoding="utf-8") as f:
        CSS = f.read()


def tearDownModule():
    if TMP:
        shutil.rmtree(TMP, ignore_errors=True)


def pagina(naam):
    return h.lees(os.path.join(MAP, naam))


class TestStatischeStijl(unittest.TestCase):
    def setUp(self):
        self.vars = root_vars(CSS)

    def test_US008_c1_statisch_kleuren_op_een_plek_gedefinieerd(self):
        verwacht = {"donker": "#1F2A44", "wit": "#FFFFFF", "achtergrond": "#F7F8FA", "rand": "#E3E6EB",
                    "tekst2": "#5B6475", "accent": "#0F766E", "tekst": "#1F2A44"}
        for naam, hexwaarde in verwacht.items():
            self.assertEqual(self.vars.get(naam), hexwaarde, naam)
        buiten_root = re.sub(r":root\{.*?\}", "", CSS, count=1, flags=re.S)
        self.assertEqual(re.findall(r"#[0-9A-Fa-f]{3,6}\b", buiten_root), [],
                         "hex-kleur buiten :root (alleen CSS-variabelen toegestaan)")
        self.assertIsNone(re.search(r"\b(rgb|hsl)\(", buiten_root))
        self.assertIsNone(re.search(r"(?<![\w-])(white|black|red|blue|green|gray|grey|navy|teal|orange|yellow)(?![\w-])",
                                    buiten_root))

    def test_US008_c2_statisch_koptekst_achtergrond_en_witte_kaarten(self):
        regels = dict(css_regels(CSS))
        self.assertIn("background:var(--donker)", regels["header"].replace(" ", ""))
        self.assertIn("background:var(--achtergrond)", regels["body"].replace(" ", ""))
        for sel in [".kaart", ".blok", ".tegel"]:
            body = regels[sel].replace(" ", "")
            self.assertIn("background:var(--wit)", body, sel)
            self.assertIn("border:1pxsolidvar(--rand)", body, sel)

    def test_US008_c3_statisch_accent_alleen_op_toegestane_plekken(self):
        toegestaan = {"a", "nav a[aria-current=page]", ".chip", ".chip.actief", "form.zoek button"}
        gevonden = set()
        for sel, body in css_regels(CSS):
            if "var(--accent)" in body:
                gevonden.add(re.sub(r"\s+", " ", sel))
        self.assertTrue(gevonden <= toegestaan, "accentkleur op niet-toegestane selectors: %s" % (gevonden - toegestaan))
        self.assertIn("nav a[aria-current=page]", gevonden)
        self.assertIn(".chip.actief", gevonden)

    def test_US008_c4_statisch_systeemfont_en_geen_externe_bestanden(self):
        regels = dict(css_regels(CSS))
        self.assertEqual(regels["body"].replace(" ", "").split("font-family:")[1].split(";")[0],
                         VISION_FONT.replace(" ", ""))
        self.assertIsNone(re.search(r"@import|@font-face|url\(", CSS))
        for naam in h.html_bestanden(MAP):
            p = pagina(naam)
            self.assertIsNone(re.search(r"<link\b[^>]*https?:|<script\b[^>]*https?:|<img\b|<iframe\b", p), naam)
            self.assertIsNone(re.search(r"<style>[^<]*url\(", p), naam)

    def test_US008_c5_statisch_contrast_minimaal_4_5(self):
        v = self.vars
        paren = [("tekst", "achtergrond"), ("tekst", "wit"), ("tekst2", "wit"), ("tekst2", "achtergrond"),
                 ("accent", "wit"), ("accent", "achtergrond"), ("wit", "accent"), ("wit", "donker")]
        for voor, achter in paren:
            ratio = contrast(v[voor], v[achter])
            self.assertGreaterEqual(ratio, 4.5, "%s op %s: %.2f" % (voor, achter, ratio))

    def test_US008_c6_statisch_tellertegels_alleen_op_startpagina(self):
        # it. 6: 4 categorietellers (BI erbij; was 3)
        self.assertEqual(pagina("index.html").count('class="tegel"'), 4)
        for naam in ["nieuws.html", "bronnen.html"]:
            p = pagina(naam)
            self.assertNotIn('class="tegel', p, naam)
            self.assertNotIn('class="tegels"', p, naam)

    def test_US008_c7_statisch_je_jij_geen_u_uw_in_interfaceteksten(self):
        teksten = " ".join(interface_tekst(pagina(n)) for n in h.html_bestanden(MAP))
        treffers = re.findall(r"(?<![\w])(u|uw|U|Uw|UW)(?![\w])", teksten)
        self.assertEqual(treffers, [], "losse u/uw gevonden")

    def test_US008_c8_statisch_breedte_en_responsief_in_stylesheet(self):
        m = re.search(r"\.wrap\{max-width:(\d+)px;margin:0auto", CSS.replace(" ", ""))
        self.assertIsNotNone(m, "wrap met max-width en gecentreerd ontbreekt")
        self.assertGreaterEqual(int(m.group(1)), 960)
        self.assertLessEqual(int(m.group(1)), 1200)
        self.assertIsNotNone(re.search(r"@media\s*\(max-width:\s*\d+px\)", CSS), "geen responsieve media query")


class TestStatischeRegressie(unittest.TestCase):
    def test_US001_c3_statisch_actief_menu_item_gemarkeerd(self):
        for naam, actief in [("index.html", "Overzicht"), ("nieuws.html", "Nieuws")]:
            p = pagina(naam)
            markeringen = re.findall(r'<a href="[^"]+"( aria-current="page")?>([^<]+)</a>', p)
            gemarkeerd = [tekst for mark, tekst in markeringen if mark]
            self.assertEqual(gemarkeerd, [actief], naam)

    def test_US001_c5_statisch_interface_is_nederlands(self):
        teksten = " ".join(interface_tekst(pagina(n)) for n in h.html_bestanden(MAP))
        self.assertIn('lang="nl"', pagina("index.html"))
        for engels in ["Home", "Search", "Filter", "Submit", "Loading", "Read more", "Dashboard",
                       "Overview", "Login", "Show all", "Back to", "Error", "Not found", "Welcome"]:
            self.assertIsNone(re.search(r"\b%s\b" % re.escape(engels), teksten), engels)
        for nederlands in ["Overzicht", "Nieuws", "Geen nieuws gevonden", "Zoeken"]:
            self.assertIn(nederlands, teksten)
        # US-022 c1 (it. 8; was: "Alles bekijken"): de link luidt "Alle <n> berichten bekijken".
        self.assertRegex(teksten, r"Alle \d+ berichten bekijken")

    def test_US002_c1_statisch_nieuws_nieuwste_eerst_met_alle_velden(self):
        p = pagina("nieuws.html")
        kaarten = re.findall(r'<article class="kaart" data-categorie="([^"]*)">(.*?)</article>', p, re.S)
        self.assertEqual(len(kaarten), 8)
        datums = []
        for cat, inhoud in kaarten:
            self.assertIn(cat, ["BI", "Data", "Automatisering", "AI"])
            self.assertIn('class="tag"', inhoud)
            self.assertIn("Bron: ", inhoud)
            self.assertRegex(inhoud, r'<span>\d{1,2} [a-z]{3} \d{4}</span>')
            self.assertIn("<p>", inhoud)
            datums.append(re.search(r"<span>(\d{1,2}) ([a-z]{3}) (\d{4})</span>", inhoud).groups())
        maanden = ["jan", "feb", "mrt", "apr", "mei", "jun", "jul", "aug", "sep", "okt", "nov", "dec"]
        iso = ["%s-%02d-%02d" % (j, maanden.index(m) + 1, int(d)) for d, m, j in datums]
        self.assertEqual(iso, sorted(iso, reverse=True), "niet nieuwste eerst")


if __name__ == "__main__":
    unittest.main()
