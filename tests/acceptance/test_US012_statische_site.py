"""Acceptatietests US-012 (openbare statische site zonder leads) en US-013 c2-deel voor de site.

Twee bronnen, beide in tijdelijke mappen (de projectmap wordt niet beschreven):
- FIXTURE: lokale testdata (hulp_statisch.fixture_items), deterministisch.
- ECHT: de echte data/nieuws.json (alleen gelezen), voor de criteria die over de echte uitvoer gaan.
Browsergedrag (filter, zoeken, layout) staat in test_US012_browser.py.
"""
import json
import os
import re
import shutil
import sys
import unittest
from datetime import datetime, timedelta, timezone

import hulp_statisch as h

sys.dont_write_bytecode = True
# Iteratie 7: src/data.py (voorbeeld-leads en voorbeeldnieuws) is verwijderd. De lijst met verzonnen
# bedrijfsnamen uit die oude data is daarmee niet meer beschikbaar (geen commit-historie); de c3-controles
# zijn daarom generiek gemaakt (leadvelden, leadstatussen, leadscherm, voorbeeldmarkering). Zie README.
LEAD_VELDEN = re.compile(r"Branche:|Gevonden:|st-(nieuw|in-behandeling|niet-interessant)\b", re.I)

NAV_VERWACHT = [("index.html", "Overzicht"), ("nieuws.html", "Nieuws")]
STATUS_TEKST = re.compile(r"in behandeling|niet interessant", re.I)
MAANDEN = ["jan", "feb", "mrt", "apr", "mei", "jun", "jul", "aug", "sep", "okt", "nov", "dec"]


with open(h.PROJECT_CONFIG, encoding="utf-8") as _f:
    EVENEMENT_TERMEN = json.load(_f).get("evenement_termen", [])


def _hele_woord_patroon(term):
    """Hele woorden, hoofdletterongevoelig; een '*' aan het eind = woorden die hiermee beginnen."""
    stam = term.rstrip("*")
    return re.compile(r"(?<!\w)" + re.escape(stam) + (r"\w*" if term.endswith("*") else "") + r"(?!\w)", re.I)


EVENEMENT_PATRONEN = [_hele_woord_patroon(t) for t in EVENEMENT_TERMEN]
AI_MAX_VAKNIEUWS = 2  # US-018 c8


def mag_weggelaten(item, getoond_items):
    """US-018 c5/c7/c8 (it. 6): een nieuwer item mag uit Vaknieuws worden weggelaten alleen als:
    - het een AI-item is en er al AI_MAX_VAKNIEUWS AI-items getoond worden (AI-boven-het-maximum), of
    - de titel met "Kort:" begint (digest), of
    - titel of samenvatting een evenementterm bevat (hele woorden).
    Alles anders (ook een gewoon nieuwer nieuwsitem) is een fout."""
    if item["categorie"] == "AI" and sum(1 for g in getoond_items if g["categorie"] == "AI") >= AI_MAX_VAKNIEUWS:
        return True
    if item["titel"].strip().casefold().startswith("kort:"):
        return True
    tekst = "%s %s" % (item["titel"], item.get("samenvatting", ""))
    return any(p.search(tekst) for p in EVENEMENT_PATRONEN)


def verwacht_vaknieuws_aantal(rest):
    """Onafhankelijke telling: nieuwste eerst, max 5, max 2 AI (US-018 c8). Geeft het aantal dat getoond moet worden."""
    n, ai = 0, 0
    for i in sorted(rest, key=lambda x: x["datum"], reverse=True):
        if n >= 5:
            break
        if i["categorie"] == "AI":
            if ai >= AI_MAX_VAKNIEUWS:
                continue
            ai += 1
        n += 1
    return n


def nl_tijd_onafhankelijk(iso):
    """Onafhankelijke berekening van de Nederlandse tijd (zomertijd: laatste zondag maart t/m oktober, 01:00 UTC)."""
    dt = datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(timezone.utc)

    def laatste_zondag(j, m):
        d = datetime(j, m + 1, 1, tzinfo=timezone.utc) - timedelta(days=1) if m < 12 else datetime(j, 12, 31, tzinfo=timezone.utc)
        while d.weekday() != 6:
            d -= timedelta(days=1)
        return d.replace(hour=1, minute=0, second=0, microsecond=0)
    zomer = laatste_zondag(dt.year, 3) <= dt < laatste_zondag(dt.year, 10)
    lokaal = dt + timedelta(hours=2 if zomer else 1)
    return "%d %s %d %02d:%02d" % (lokaal.day, MAANDEN[lokaal.month - 1], lokaal.year, lokaal.hour, lokaal.minute)


class SitePlus:
    """Gedeelde controles op een gebouwde site. Subklassen zetten self.map, self.items, self.bijgewerkt."""
    map = None
    items = None
    bijgewerkt_iso = None

    def pagina(self, naam):
        return h.lees(os.path.join(self.map, naam))

    # ---- c1 ----
    def test_US012_c1_bouwcommando_maakt_statische_map_zonder_server_code(self):
        bestanden = os.listdir(self.map)
        for naam in ["index.html", "nieuws.html", "bronnen.html", "style.css", "app.js", "favicon.ico"]:
            self.assertIn(naam, bestanden)
        vreemd = [n for n in bestanden if os.path.splitext(n)[1].lower() not in
                  (".html", ".css", ".js", ".ico", ".svg", "")]
        self.assertEqual(vreemd, [], "bestanden die geen statische site zijn")
        with h.StatischeServer(self.map) as srv:
            status, typ, body = srv.get("/")
            self.assertEqual(status, 200)
            self.assertIn("Overzicht", body)
            status2, _, _ = srv.get("/nieuws.html")
            self.assertEqual(status2, 200)

    # ---- c2 ----
    def test_US012_c2_navigatie_precies_overzicht_en_nieuws_op_elke_pagina(self):
        for naam in h.html_bestanden(self.map):
            pagina = self.pagina(naam)
            nav = re.search(r'<nav aria-label="Hoofdmenu">(.*?)</nav>', pagina, re.S)
            self.assertIsNotNone(nav, naam)
            links = re.findall(r'<a href="([^"]+)"[^>]*>([^<]+)</a>', nav.group(1))
            self.assertEqual(links, NAV_VERWACHT, naam)
            self.assertIsNone(re.search(r'href="[^"]*leads', pagina, re.I), "leads-link in %s" % naam)

    def test_US012_c2_geen_leadsscherm_bestand(self):
        self.assertEqual([n for n in h.html_bestanden(self.map) if "lead" in n.lower()], [])

    # ---- c3 (zoeken op leads-schermen, leadstatussen, verzonnen bedrijfsnamen, voorbeeldnieuws) ----
    def test_US012_c3_geen_leadstatussen_of_leadscherm_in_bestanden(self):
        for naam in h.html_bestanden(self.map) + ["app.js"]:
            tekst = self.pagina(naam)
            self.assertIsNone(STATUS_TEKST.search(tekst), "leadstatus gevonden in %s" % naam)
            self.assertIsNone(re.search(r">\s*Nieuw\s*<", tekst), "statuslabel 'Nieuw' gevonden in %s" % naam)
            self.assertIsNone(re.search(r'href="[^"]*leads|id="leads|class="leads', tekst, re.I),
                              "leadscherm-element in %s" % naam)

    def test_US012_c3_geen_lead_velden_bedrijf_branche_gevonden(self):
        """Generiek (iteratie 7): geen leadvelden (branche, gevonden, leadstatus-klassen) in de gegenereerde bestanden.
        De oude lijst met verzonnen bedrijfsnamen kan niet meer gelezen worden (src/data.py is verwijderd): NIET GETEST als lijst."""
        for naam in h.html_bestanden(self.map) + ["app.js"]:
            tekst = self.pagina(naam)
            self.assertIsNone(LEAD_VELDEN.search(tekst), "leadveld gevonden in %s" % naam)

    def test_US012_c3_geen_voorbeeldmarkering_uit_app_data(self):
        """Generiek (iteratie 7): de voorbeelddata van de lokale app was als 'Voorbeeld' herkenbaar. Die mag niet op de site staan.
        De oude voorbeeldtitels zelf kunnen niet meer gelezen worden (src/data.py is verwijderd): NIET GETEST als lijst."""
        for naam in h.html_bestanden(self.map):
            self.assertNotIn("Voorbeeld", self.pagina(naam), "voorbeeldmarkering in %s" % naam)

    # ---- c4 ----
    def test_US012_c4_nieuwsitem_toont_bron_datum_samenvatting_en_link(self):
        pagina = self.pagina("nieuws.html")
        kaarten = re.findall(r'<article class="kaart" data-categorie="[^"]*">(.*?)</article>', pagina, re.S)
        self.assertEqual(len(kaarten), len(self.items), "aantal kaarten op Nieuws klopt niet")
        per_url = {h.htmllib.escape(i["url"]): i for i in self.items}
        gevonden = []
        for k in kaarten:
            href = re.search(r'<h2><a href="([^"]+)"', k)
            self.assertIsNotNone(href, "kaart zonder link naar het origineel")
            item = per_url.get(href.group(1))
            self.assertIsNotNone(item, "kaart met onbekende link: %s" % href.group(1))
            gevonden.append(item["url"])
            self.assertIn('target="_blank"', k)
            self.assertIn("Bron: %s" % h.htmllib.escape(item["bron"]), k)
            sam = re.search(r"<p>(.*?)</p>", k, re.S)
            self.assertIsNotNone(sam)
            self.assertLessEqual(len(h.tekst_van(sam.group(1))), 300, "samenvatting langer dan 300 tekens")
        self.assertEqual(sorted(gevonden), sorted(i["url"] for i in self.items), "niet alle getoonde items op Nieuws")
        for naam in h.html_bestanden(self.map):
            p = self.pagina(naam)
            self.assertIsNone(re.search(r"<img\b|<picture\b|<video\b|<audio\b|<iframe\b|<object\b|<embed\b", p, re.I),
                              "afbeelding of ingesloten inhoud in %s" % naam)

    def test_US012_c4_samenvattingen_zijn_afgekapt_met_puntjes_en_max_300(self):
        pagina = self.pagina("nieuws.html")
        for sam in re.findall(r'<p>(.*?)</p>', pagina, re.S):
            t = h.tekst_van(sam)
            if len(t) > 0:
                self.assertLessEqual(len(t), 300)

    # ---- c5 ----
    def test_US012_c5_voet_laatst_bijgewerkt_bronvermelding_en_bronnenlijst(self):
        for naam in h.html_bestanden(self.map):
            p = self.pagina(naam)
            m = re.search(r"Laatst bijgewerkt: <time datetime=\"([^\"]+)\">([^<]+)</time>", p)
            self.assertIsNotNone(m, "geen 'Laatst bijgewerkt' in %s" % naam)
            self.assertRegex(m.group(2), r"^\d{1,2} [a-z]{3} \d{4} \d{2}:\d{2}$")
            self.assertEqual(m.group(2), nl_tijd_onafhankelijk(self.bijgewerkt_iso), naam)
            self.assertIn("afkomstig van de genoemde bronnen", p, naam)
            self.assertIn('href="bronnen.html">alle bronnen</a>', p, naam)
        bronnen = self.pagina("bronnen.html")
        with open(h.PROJECT_CONFIG, encoding="utf-8") as f:
            feeds = json.load(f)["feeds"]
        for feed in feeds:
            self.assertIn(h.htmllib.escape(feed["naam"]), bronnen, "bron ontbreekt op bronnenlijst: %s" % feed["naam"])

    # ---- c6 ----
    def test_US012_c6_startpagina_tellers_per_categorie_kloppen_met_data(self):
        p = self.pagina("index.html")
        for cat in ["BI", "Data", "Automatisering", "AI"]:
            m = re.search(r'id="teller-%s">(\d+)<' % cat.lower(), p)
            self.assertIsNotNone(m, cat)
            verwacht = len([i for i in self.items if i["categorie"] == cat])
            self.assertEqual(int(m.group(1)), verwacht, "teller %s" % cat)
        # US-022 c1 (it. 8; was: "%d in totaal" van alle items in de kop van Vaknieuws). Nu: geen totaal in de kop,
        # en de link naar Nieuws luidt "Alle <n> berichten bekijken" met n = aantal items op Nieuws.
        self.assertNotIn("in totaal", p, "totaal van alle items staat nog op de startpagina")
        self.assertIn(">Alle %d berichten bekijken</a>" % len(self.items), p)

    def test_US012_c6_startpagina_toont_vijf_nieuwste_items(self):
        """it. 6 (US-018 c5): het vaknieuws-blok toont de 5 nieuwste getoonde items die NIET in Uitgelicht staan.
        Was: de 5 nieuwste items (it. 4). De Uitgelicht-titels worden uit de pagina gelezen (onafhankelijk van de datum)."""
        p = self.pagina("index.html")
        uit = re.search(r'<section class="blok uitgelicht" id="blok-uitgelicht">(.*?)</section>', p, re.S)
        self.assertIsNotNone(uit, "blok Uitgelicht ontbreekt")
        uit_titels = re.findall(r'<li><a [^>]*>([^<]+)</a>', uit.group(1))
        blok = re.search(r'<section class="blok" id="blok-nieuws">(.*?)</section>', p, re.S)
        self.assertIsNotNone(blok)
        getoond = re.findall(r'<li><a [^>]*>([^<]+)</a><div class="meta">.*?<span>(\d{1,2} [a-z]{3} \d{4})</span>', blok.group(1), re.S)
        def maand_nr(s):
            d, mnd, j = s.split()
            return "%s-%02d-%02d" % (j, MAANDEN.index(mnd) + 1, int(d))
        rest = [i for i in h.verwacht_getoond(self.items) if h.htmllib.escape(i["titel"]) not in uit_titels]
        # it. 6 (US-018 c8): hooguit 2 AI in Vaknieuws, dus het verwachte aantal is niet altijd min(5, len(rest)).
        verwacht_n = verwacht_vaknieuws_aantal(rest)
        self.assertEqual(len(getoond), verwacht_n, "aantal vaknieuws-items klopt niet")
        rest_titels = {h.htmllib.escape(i["titel"]) for i in rest}
        self.assertTrue({t for t, _ in getoond} <= rest_titels, "vaknieuws bevat een item dat in Uitgelicht staat of niet getoond wordt")
        getoond_iso = [maand_nr(d) for _, d in getoond]
        self.assertEqual(getoond_iso, sorted(getoond_iso, reverse=True), "vaknieuws niet nieuwste eerst")
        getoond_items = [i for i in rest if h.htmllib.escape(i["titel"]) in {t for t, _ in getoond}]
        self.assertLessEqual(sum(1 for i in getoond_items if i["categorie"] == "AI"), AI_MAX_VAKNIEUWS,
                             "vaknieuws bevat meer dan 2 AI-items")
        if rest and getoond_iso:
            # Een weggelaten item dat nieuwer is dan het oudste getoonde, moet een geldige reden hebben
            # (AI-boven-het-maximum, 'Kort:' of evenementterm). Zonder reden is het een fout.
            getoond_titels = {t for t, _ in getoond}
            for i in rest:
                if h.htmllib.escape(i["titel"]) in getoond_titels:
                    continue
                if i["datum"] > min(getoond_iso):  # gelijke datum: volgorde binnen een dag is niet vastgelegd
                    self.assertTrue(mag_weggelaten(i, getoond_items),
                                    "nieuwer vaknieuws-item weggelaten zonder reden (AI-max, 'Kort:' of evenement): %r" % i["titel"])

    def test_US012_c6_weggelaten_nieuwere_items_uitzonderingen_positief_en_negatief(self):
        """it. 6 (US-018 c5/c7/c8): de uitzonderingen op 'nieuwer weggelaten' werken positief EN negatief."""
        gewoon_ai = {"titel": "Taalmodel wordt goedkoper", "categorie": "AI", "samenvatting": "Kosten dalen."}
        gewoon_data = {"titel": "Nieuwe datawarehouse-release", "categorie": "Data", "samenvatting": "Kosten dalen."}
        twee_ai = [{"titel": "A", "categorie": "AI", "samenvatting": ""}, {"titel": "B", "categorie": "AI", "samenvatting": ""}]
        een_ai = [{"titel": "A", "categorie": "AI", "samenvatting": ""}]
        # positief
        self.assertTrue(mag_weggelaten(gewoon_ai, twee_ai), "AI boven het maximum van 2 moet weggelaten mogen worden")
        self.assertTrue(mag_weggelaten({"titel": "Kort: Google-detector ...", "categorie": "Data", "samenvatting": ""}, []),
                        "titel met 'Kort:' moet weggelaten mogen worden")
        self.assertTrue(mag_weggelaten({"titel": "Begin bij het einde", "categorie": "Automatisering",
                                        "samenvatting": "Aankondiging van het ServiceNow World Forum."}, []),
                        "evenementterm 'world forum' in samenvatting moet weggelaten mogen worden")
        self.assertTrue(mag_weggelaten({"titel": "Aanmelden kan nog tot 1 november", "categorie": "Data",
                                        "samenvatting": ""}, []), "evenementterm 'aanmelden' in titel moet weggelaten mogen worden")
        # negatief
        self.assertFalse(mag_weggelaten(gewoon_ai, een_ai), "AI terwijl er maar 1 AI getoond wordt, mag NIET weggelaten worden")
        self.assertFalse(mag_weggelaten(gewoon_data, twee_ai), "gewoon nieuwsitem (Data) mag niet weggelaten worden")
        self.assertFalse(mag_weggelaten({"titel": "Kortom: de stand van zaken", "categorie": "Data", "samenvatting": ""}, []),
                         "'Kortom:' is geen 'Kort:'-titel")
        self.assertFalse(mag_weggelaten({"titel": "Congresbezoekers over dataplatformen", "categorie": "Data",
                                         "samenvatting": "Een verslag."}, []),
                         "'congres' mag niet matchen in 'Congresbezoekers' (hele woorden)")

    # ---- relatieve links en geen externe bestanden ----
    def test_US012_links_relatief_en_geen_externe_bestanden(self):
        for naam in h.html_bestanden(self.map):
            p = self.pagina(naam)
            for tag in re.findall(r"<(a|link|script|img)\b([^>]*)>", p):
                attrs = tag[1]
                href = re.search(r'\b(href|src)="([^"]*)"', attrs)
                if not href:
                    continue
                waarde = h.htmllib.unescape(href.group(2))
                if waarde.startswith(("http://", "https://")):
                    self.assertEqual(tag[0], "a", "externe %s in %s" % (tag[0], naam))
                    self.assertIn('target="_blank"', attrs, "externe link zonder nieuw tabblad in %s" % naam)
                else:
                    self.assertFalse(waarde.startswith("/"), "absoluut pad '%s' in %s" % (waarde, naam))
                    self.assertFalse(waarde.startswith("//"), "protocol-relatief pad in %s" % naam)
        self.assertIsNone(re.search(r"@import|url\(\s*['\"]?https?:", h.lees(os.path.join(self.map, "style.css"))))
        self.assertIsNone(re.search(r"https?://", h.lees(os.path.join(self.map, "app.js"))))

    def test_US012_links_blijven_binnen_het_repo_pad_op_github_pages(self):
        """Simuleert https://<account>.github.io/<repo>/: elke interne link moet onder /<repo>/ blijven."""
        from urllib.parse import urljoin, urlparse as up
        basis = "https://account.github.io/repo/"
        for naam in h.html_bestanden(self.map):
            p = self.pagina(naam)
            for href in re.findall(r'<(?:a|link|script)\b[^>]*?\b(?:href|src)="([^"]*)"', p):
                if href.startswith(("http://", "https://")):
                    continue
                pad = up(urljoin(basis + naam, h.htmllib.unescape(href))).path
                self.assertTrue(pad.startswith("/repo/"), "link '%s' in %s ontsnapt aan /repo/ (%s)" % (href, naam, pad))
                self.assertTrue(os.path.exists(os.path.join(self.map, pad[len("/repo/"):].split("?")[0] or "index.html"))
                                or pad == "/repo/", "doel van '%s' in %s bestaat niet" % (href, naam))

    # ---- US-007 c1 op de statische site ----
    def test_US007_c1_statisch_favicon_geen_404(self):
        with h.StatischeServer(self.map) as srv:
            status, typ, _ = srv.get("/favicon.ico")
            self.assertEqual(status, 200, "favicon.ico geeft %s" % status)
            self.assertEqual(srv.get("/favicon.svg")[0], 200)


class TestSiteFixture(SitePlus, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = h.nieuwe_tijdelijke_map()
        cls.map = os.path.join(cls.tmp, "site")
        data = h.schrijf_fixture_data(cls.tmp)
        cls.rc, cls.out, cls.err = h.bouw(cls.map, data=data, vandaag=h.FIXTURE_VANDAAG)
        cls.items = h.fixture_items()
        cls.bijgewerkt_iso = h.FIXTURE_BIJGEWERKT

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def setUp(self):
        self.assertEqual(self.rc, 0, "bouwen met fixture faalde: %s" % self.err)

    def test_US012_c5_fixture_tijd_in_nederlandse_tijd(self):
        self.assertEqual(nl_tijd_onafhankelijk(h.FIXTURE_BIJGEWERKT), h.FIXTURE_BIJGEWERKT_NL)
        self.assertIn(h.FIXTURE_BIJGEWERKT_NL, self.pagina("index.html"))

    def test_US012_c4_fixture_html_in_samenvatting_wordt_tekst_niet_opmaak(self):
        p = self.pagina("nieuws.html")
        self.assertNotIn("<b>vet</b>", p, "HTML uit een bron wordt als opmaak gerenderd")
        self.assertIn("&lt;b&gt;vet&lt;/b&gt;", p)

    def test_US012_c4_fixture_lange_samenvatting_afgekapt_met_puntjes(self):
        p = self.pagina("nieuws.html")
        self.assertIn("Chatbot voor de klantenservice", p)
        sam = h.tekst_van(re.search(r"Chatbot voor de klantenservice.*?<p>(.*?)</p>", p, re.S).group(1))
        self.assertTrue(sam.endswith("..."), sam[-20:])
        self.assertLessEqual(len(sam), 300)

    def test_US012_bouw_zonder_data_geeft_fout_exitcode_1_en_publiceert_niets(self):
        leeg = h.nieuwe_tijdelijke_map()
        try:
            uit = os.path.join(leeg, "site")
            rc, out, err = h.bouw(uit, data=None)
            self.assertEqual(rc, 1, "zonder data moet het commando met exitcode 1 stoppen")
            self.assertIn("FOUT", err)
            self.assertFalse(os.path.exists(os.path.join(uit, "index.html")), "er is toch een site gebouwd")
        finally:
            shutil.rmtree(leeg, ignore_errors=True)

    def test_US012_bouw_met_lege_items_geeft_fout_exitcode_1(self):
        leeg = h.nieuwe_tijdelijke_map()
        try:
            pad = os.path.join(leeg, "nieuws.json")
            with open(pad, "w", encoding="utf-8") as f:
                json.dump({"bijgewerkt": h.FIXTURE_BIJGEWERKT, "items": []}, f)
            uit = os.path.join(leeg, "site")
            rc, out, err = h.bouw(uit, data=pad)
            self.assertEqual(rc, 1)
            self.assertIn("FOUT", err)
            self.assertFalse(os.path.exists(os.path.join(uit, "index.html")))
        finally:
            shutil.rmtree(leeg, ignore_errors=True)

    def test_US012_bouw_met_kapot_databestand_geeft_fout_exitcode_1(self):
        leeg = h.nieuwe_tijdelijke_map()
        try:
            pad = os.path.join(leeg, "nieuws.json")
            with open(pad, "w", encoding="utf-8") as f:
                f.write("{kapot")
            rc, out, err = h.bouw(os.path.join(leeg, "site"), data=pad)
            self.assertEqual(rc, 1)
            self.assertNotIn("Traceback", err, "kapot databestand geeft een traceback in plaats van een nette melding")
        finally:
            shutil.rmtree(leeg, ignore_errors=True)


@unittest.skipUnless(os.path.exists(h.PROJECT_DATA), "NIET GETEST: data/nieuws.json ontbreekt in het project")
class TestSiteEchteData(SitePlus, unittest.TestCase):
    """Bouwt de site uit de echte data (alleen-lezen) naar een tijdelijke map. site/ wordt niet aangeraakt."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = h.nieuwe_tijdelijke_map()
        cls.map = os.path.join(cls.tmp, "site")
        cls.rc, cls.out, cls.err = h.bouw(cls.map, data=h.PROJECT_DATA)
        with open(h.PROJECT_DATA, encoding="utf-8") as f:
            d = json.load(f)
        # it. 6: de getoonde items (incl. BI en het AI-plafond); was: alleen Data/Automatisering/AI (70 van 104).
        cls.items = h.verwacht_getoond([i for i in d["items"] if i.get("categorie") in ("BI", "Data", "Automatisering", "AI")])
        cls.bijgewerkt_iso = d["bijgewerkt"]

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def setUp(self):
        self.assertEqual(self.rc, 0, "bouwen met echte data faalde: %s" % self.err)

    def test_US012_echte_data_bouwt_zonder_fout_en_aantal_klopt(self):
        self.assertIn("nieuwsitems", self.out)
        self.assertGreaterEqual(len(self.items), 20, "echte data heeft te weinig items voor een zinvolle controle")

    def test_US012_c6_echte_data_tellers_kloppen(self):
        p = self.pagina("index.html")
        for cat in ["BI", "Data", "Automatisering", "AI"]:
            m = re.search(r'id="teller-%s">(\d+)<' % cat.lower(), p)
            self.assertEqual(int(m.group(1)), len([i for i in self.items if i["categorie"] == cat]))

    def test_US012_c4_echte_data_geen_ruwe_html_of_scripts_in_samenvattingen(self):
        p = self.pagina("nieuws.html")
        self.assertEqual(re.findall(r"<script[^>]*>", p), ['<script src="app.js">'], "alleen het eigen app.js mag")
        self.assertNotIn("&lt;script", p.lower(), "ruwe script-tekst uit een bron in de samenvatting")
        self.assertIsNone(re.search(r"<img\b", p, re.I))


if __name__ == "__main__":
    unittest.main()
