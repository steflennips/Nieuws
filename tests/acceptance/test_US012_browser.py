"""Browsertests (headless Microsoft Edge) voor de statische site: filter, zoeken, foutmeldingen en layout.

Criteria: US-012 c6/c7 (filter en zoeken zoals US-002 c2-c5 en US-007 c2-c3), US-002 c5/c6 op de statische
site, US-001 c2/c6, US-008 c8 en US-004 c2 (tegels) op de statische site.

Werkwijze (zelfde mechanisme als test_browser_layout.py, dat al werkt in deze omgeving):
- De fixture-site wordt in een tijdelijke map gebouwd en door een kleine proxy geserveerd op 127.0.0.1.
- De proxy voegt aan elke HTML-pagina een klein script toe. Dat script meldt na het laden de DOM
  (na JavaScript) en eventuele console-fouten terug aan de proxy. Zo testen we het echte gedrag van de pagina
  die de gebruiker ziet, inclusief filter- en zoek-JavaScript (?categorie=, ?q=).
- Edge wordt gestart op de echte URL (met de parameters). Het resultaat wordt opgehaald uit de proxy.
- Layout: een meetpagina laadt de site in een iframe van 375 of 1280 px (zoals test_browser_layout.py).

Zonder Edge: alle klassen in dit bestand worden overgeslagen; de browsercontroles zijn dan NIET GETEST.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import unittest
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

import hulp_statisch as h

sys.dont_write_bytecode = True

EDGE = h.vind_edge()
SLA_OVER = "NIET GETEST: geen headless Edge gevonden op de standaardlocaties (browsercontroles)"

# Meld na het laden de DOM en console-fouten terug. Wordt alleen in HTML-pagina's van de site ingevoegd.
MELDSCRIPT = (
    "<script>(function(){var K=location.pathname+location.search,E=[];"
    "var ce=console.error;console.error=function(){E.push(Array.prototype.slice.call(arguments).map(String).join(' '));"
    "return ce.apply(console,arguments)};"
    "window.addEventListener('error',function(e){E.push('Uncaught: '+e.message)});"
    "window.addEventListener('load',function(){setTimeout(function(){fetch('/__r',{method:'POST',"
    "headers:{'Content-Type':'application/json'},body:JSON.stringify({kind:'dom',url:K,"
    "dom:document.documentElement.outerHTML,errs:E})})},500)});})();</script>"
)

MEETPAGINA = """<!doctype html><html lang="nl"><head><meta charset="utf-8"><style>body{margin:0;background:#888}</style></head>
<body><iframe id="f" style="border:0;display:block"></iframe>
<script>
const q = new URLSearchParams(location.search);
const w = parseInt(q.get('w') || '375'), p = q.get('p') || '/index.html';
const f = document.getElementById('f');
f.style.width = w + 'px'; f.style.height = '1400px'; f.src = p;
f.onload = () => {
  const d = f.contentDocument, win = d.defaultView; const r = {kind: 'layout', url: p, viewport: w};
  r.docScrollWidth = d.documentElement.scrollWidth;
  r.docClientWidth = d.documentElement.clientWidth;
  r.horizontalOverflow = r.docScrollWidth > r.docClientWidth;
  const navs = [...d.querySelectorAll('nav a')];
  r.navNames = navs.map(a => a.textContent.trim());
  r.navInView = navs.length > 0 && navs.every(a => { const b = a.getBoundingClientRect(); return b.left >= 0 && b.right <= w; });
  const wb = d.querySelector('main .wrap').getBoundingClientRect();
  r.wrapWidth = wb.width; r.wrapLeft = wb.left; r.wrapRightGap = d.documentElement.clientWidth - wb.right;
  const tg = d.querySelector('.tegels'); if (tg) r.tegelsCols = win.getComputedStyle(tg).gridTemplateColumns;
  r.blokken = [...d.querySelectorAll('.kaart, .tegel, .blok')].filter(e => !e.hidden).map(e => {
    const b = e.getBoundingClientRect(); return [Math.round(b.left), Math.round(b.top), Math.round(b.right), Math.round(b.bottom)]; });
  r.buitenBeeld = [...d.querySelectorAll('body *')].filter(el => { const b = el.getBoundingClientRect(); return b.width > 0 && b.right > w + 0.5; })
    .map(el => el.tagName + '.' + el.className).slice(0, 10);
  fetch('/__r', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(r)});
};
</script></body></html>"""


def maak_proxy(static_base, rapporten):
    class H(BaseHTTPRequestHandler):
        def do_POST(self):
            n = int(self.headers.get("Content-Length", 0))
            rapporten.append(json.loads(self.rfile.read(n).decode("utf-8")))
            self.send_response(204)
            self.end_headers()

        def do_GET(self):
            if urlparse(self.path).path == "/__h":
                data, ct, code = MEETPAGINA.encode("utf-8"), "text/html; charset=utf-8", 200
            else:
                try:
                    with urllib.request.urlopen(static_base + self.path, timeout=10) as r:
                        data, ct, code = r.read(), r.headers.get("Content-Type", "text/html"), r.status
                except urllib.error.HTTPError as e:
                    data, ct, code = e.read(), "text/html", e.code
                if code == 200 and ct.startswith("text/html"):
                    data = data.decode("utf-8").replace("<head>", "<head>" + MELDSCRIPT, 1).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", ct)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def log_message(self, *a):
            pass
    return H


def start_edge(url):
    profiel = tempfile.mkdtemp(prefix="t4-edge-")
    proc = subprocess.Popen([EDGE, "--headless", "--disable-gpu", "--no-first-run",
                             "--no-default-browser-check", "--user-data-dir=" + profiel,
                             "--virtual-time-budget=6000", "--window-size=1280,1000", url],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return proc, profiel


@unittest.skipUnless(EDGE, SLA_OVER)
class TestStatischeSiteBrowser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = h.nieuwe_tijdelijke_map()
        cls.map = os.path.join(cls.tmp, "site")
        data = h.schrijf_fixture_data(cls.tmp)
        rc, out, err = h.bouw(cls.map, data=data, vandaag=h.FIXTURE_VANDAAG)
        assert rc == 0, err
        # Sanity-pagina (alleen in deze tijdelijke site): bewijst dat console-fouten worden teruggemeld.
        with open(os.path.join(cls.map, "probe-iteratie4.html"), "w", encoding="utf-8") as f:
            f.write('<!doctype html><html lang="nl"><head><meta charset="utf-8"></head><body>'
                    '<script>console.error("probe-fout-iteratie4");</script></body></html>')
        cls.srv = h.StatischeServer(cls.map).__enter__()
        cls.rapporten = []
        cls.proxy = ThreadingHTTPServer(("127.0.0.1", 0), maak_proxy(cls.srv.base, cls.rapporten))
        threading.Thread(target=cls.proxy.serve_forever, daemon=True).start()
        cls.base = "http://127.0.0.1:%d" % cls.proxy.server_address[1]
        cls.cache = {}
        cls._metingen = {}
        cls.console_zichtbaar = None

    @classmethod
    def tearDownClass(cls):
        cls.proxy.shutdown()
        cls.proxy.server_close()
        cls.srv.__exit__(None, None, None)
        shutil.rmtree(cls.tmp, ignore_errors=True)

    @classmethod
    def _wacht_op(cls, pad, kind, w=None, timeout=60):
        """Start Edge op de URL en wacht tot de pagina zich heeft gemeld."""
        proc, profiel = start_edge(cls.base + pad)
        try:
            eind = time.time() + timeout
            while time.time() < eind:
                for r in list(cls.rapporten):
                    if r.get("url") == pad and r.get("kind") == kind and (w is None or r.get("viewport") == w):
                        return r
                time.sleep(0.3)
            raise AssertionError("Edge meldde geen %s-rapport voor %s binnen %d s" % (kind, pad, timeout))
        finally:
            h.stop_proces(proc)
            h.stop_edge_profiel(profiel)
            shutil.rmtree(profiel, ignore_errors=True)

    def laad(self, pad):
        """Geeft (DOM na JavaScript, lijst console-fouten) voor een pad inclusief zoek-/filterparameters."""
        if pad not in self.cache:
            r = self._wacht_op(pad, "dom")
            self.cache[pad] = (r["dom"], r.get("errs", []))
        return self.cache[pad]

    def assertGeenConsoleFouten(self, pad):
        if self.console_zichtbaar is None:
            type(self).console_zichtbaar = "probe-fout-iteratie4" in self.laad_probe()
        if not self.console_zichtbaar:
            self.skipTest("NIET GETEST: console-fouten worden niet teruggemeld (sanity-check faalde); %s" % pad)
        _, fouten = self.laad(pad)
        self.assertEqual(fouten, [], "console-fout op %s" % pad)

    def laad_probe(self):
        r = self._wacht_op("/probe-iteratie4.html", "dom")
        return " ".join(r.get("errs", []))

    # ---- US-012 c7 / US-002 c2-c5 / US-007 c2-c3 ----
    def test_US012_c7_categoriefilter_toont_alleen_categorie_en_juist_aantal(self):
        dom, _ = self.laad("/nieuws.html?categorie=AI")
        zichtbaar = h.zichtbare_kaarten(dom)
        # it. 6: 3 AI-items in de fixture (was 4; item 7 is nu BI, zie hulp_statisch.fixture_items)
        self.assertEqual(len(zichtbaar), 3)
        self.assertTrue(all(k["cat"] == "AI" for k in zichtbaar))
        self.assertEqual(h.element_tekst(dom, "aantal")[0], "3 nieuwsitems")
        chips = {c["tekst"]: c for c in h.chips_in(dom)}
        self.assertTrue(chips["AI"]["actief"])
        self.assertFalse(chips["Alle"]["actief"])
        self.assertTrue(chips["AI"]["aria"])
        self.assertGeenConsoleFouten("/nieuws.html?categorie=AI")

    def test_US012_c7_alle_toont_weer_alles_via_chip(self):
        dom, _ = self.laad("/nieuws.html?categorie=Data")
        self.assertEqual(len(h.zichtbare_kaarten(dom)), 2)
        alle = [c for c in h.chips_in(dom) if c["tekst"] == "Alle"][0]
        self.assertEqual(alle["href"], "nieuws.html", "Alle-chip linkt niet naar het ongefilterde overzicht")
        dom2, _ = self.laad("/" + alle["href"])
        self.assertEqual(len(h.zichtbare_kaarten(dom2)), 8)
        self.assertTrue([c for c in h.chips_in(dom2) if c["tekst"] == "Alle"][0]["actief"])

    def test_US012_c7_zonder_filter_alle_nieuwsitems_zichtbaar(self):
        dom, _ = self.laad("/nieuws.html")
        self.assertEqual(len(h.zichtbare_kaarten(dom)), 8)
        self.assertEqual(h.element_tekst(dom, "aantal")[0], "8 nieuwsitems")

    def test_US007_c2_kleine_letters_categorie_gelijk_aan_juiste_schrijfwijze(self):
        dom_klein, _ = self.laad("/nieuws.html?categorie=ai")
        dom_juist, _ = self.laad("/nieuws.html?categorie=AI")
        self.assertEqual([k["h2"] for k in h.zichtbare_kaarten(dom_klein)],
                         [k["h2"] for k in h.zichtbare_kaarten(dom_juist)])
        self.assertEqual(len(h.zichtbare_kaarten(dom_klein)), 3)

    def test_US007_c3_onbekende_filterwaarde_toont_alles_en_alle_actief(self):
        dom, _ = self.laad("/nieuws.html?categorie=Onbekend")
        self.assertEqual(len(h.zichtbare_kaarten(dom)), 8)
        chips = {c["tekst"]: c for c in h.chips_in(dom)}
        self.assertTrue(chips["Alle"]["actief"])
        self.assertEqual(h.element_tekst(dom, "geen-nieuws")[1], True, "melding 'geen nieuws' hoort verborgen te zijn")
        self.assertGeenConsoleFouten("/nieuws.html?categorie=Onbekend")

    def test_US012_c7_zoeken_titel_en_samenvatting_hoofdletterongevoelig(self):
        dom, _ = self.laad("/nieuws.html?q=ZOEKUNIEK")
        self.assertEqual([k["h2"] for k in h.zichtbare_kaarten(dom)], ["Zoekbaar nieuws over ZoekUniek"])
        dom2, _ = self.laad("/nieuws.html?q=zoekuniek")
        self.assertEqual(len(h.zichtbare_kaarten(dom2)), 1, "kleine letters moeten dezelfde zoekuitslag geven")

    def test_US012_c7_zoeken_vindt_ook_alleen_in_samenvatting(self):
        dom, _ = self.laad("/nieuws.html?q=handmatig")
        self.assertEqual([k["h2"] for k in h.zichtbare_kaarten(dom)], ["Workflow-automatisering bespaart uren"])

    def test_US012_c7_combinatie_filter_en_zoeken_zonder_resultaat(self):
        dom, logs_ = self.laad("/nieuws.html?categorie=AI&q=handmatig")
        self.assertEqual(h.zichtbare_kaarten(dom), [])
        self.assertEqual(h.element_tekst(dom, "aantal")[0], "0 nieuwsitems")
        self.assertFalse(h.element_tekst(dom, "geen-nieuws")[1], "melding moet zichtbaar zijn")

    def test_US002_c5_geen_resultaat_melding_zonder_fout(self):
        dom, _ = self.laad("/nieuws.html?q=zzzqqq")
        tekst, verborgen = h.element_tekst(dom, "geen-nieuws")
        self.assertEqual(tekst, "Geen nieuws gevonden")
        self.assertFalse(verborgen, "melding 'Geen nieuws gevonden' moet zichtbaar zijn")
        self.assertEqual(h.zichtbare_kaarten(dom), [])
        self.assertGeenConsoleFouten("/nieuws.html?q=zzzqqq")

    def test_US012_c7_speciale_tekens_in_zoekterm_geven_geen_opmaak_of_fout(self):
        for zoek in ["%3Cb%3Evet%3C%2Fb%3E", "%25", "%27%22%3B", "a" * 400]:
            pad = "/nieuws.html?q=" + zoek
            dom, errs = self.laad(pad)
            self.assertNotIn("<b>vet</b>", dom, zoek[:20])
            self.assertIsNotNone(h.element_tekst(dom, "aantal")[0], zoek[:20])
            self.assertEqual(errs, [], "console-fout bij zoekterm %s" % zoek[:20])

    def test_US012_c7_lege_zoekterm_en_lege_categorie_tonen_alles(self):
        dom, _ = self.laad("/nieuws.html?q=&categorie=")
        self.assertEqual(len(h.zichtbare_kaarten(dom)), 8)

    def test_US002_c6_titel_opent_bronlink_in_nieuw_tabblad_statisch(self):
        dom, _ = self.laad("/nieuws.html")
        links = re.findall(r'<h2><a href="([^"]+)" target="_blank" rel="noopener noreferrer">', dom)
        self.assertEqual(len(links), 8)
        self.assertTrue(all(l.startswith("https://voorbeeld-bron.example/") for l in links))

    def test_US012_c6_startpagina_tellers_in_browser(self):
        dom, _ = self.laad("/index.html")
        self.assertEqual(h.element_tekst(dom, "teller-data")[0], "2")
        self.assertEqual(h.element_tekst(dom, "teller-automatisering")[0], "2")
        self.assertEqual(h.element_tekst(dom, "teller-ai")[0], "3")
        self.assertEqual(h.element_tekst(dom, "teller-bi")[0], "1")
        self.assertIn('href="nieuws.html?categorie=AI"', dom)
        self.assertGeenConsoleFouten("/index.html")

    # ---- layout 375 en 1280 px ----
    def meting(self, pad, w):
        key = (pad, w)
        if key not in self._metingen:
            type(self)._metingen[key] = self._meet(pad, w)
        return self._metingen[key]

    @classmethod
    def _meet(cls, pad, w):
        url = "%s/__h?w=%d&p=%s" % (cls.base, w, urllib.parse.quote(pad, safe=""))
        proc, profiel = start_edge(url)
        try:
            eind = time.time() + 90
            while time.time() < eind:
                for r in list(cls.rapporten):
                    if r.get("kind") == "layout" and r.get("url") == pad and r.get("viewport") == w:
                        return r
                time.sleep(0.3)
            raise AssertionError("geen meetrapport van Edge voor %s bij %d px binnen 90 s" % (pad, w))
        finally:
            h.stop_proces(proc)
            h.stop_edge_profiel(profiel)
            shutil.rmtree(profiel, ignore_errors=True)

    def test_US001_c6_statisch_375_px_geen_horizontaal_scrollen_en_navigatie_in_beeld(self):
        for pad in ["/index.html", "/nieuws.html"]:
            r = self.meting(pad, 375)
            self.assertFalse(r["horizontalOverflow"], "%s: horizontaal scrollen bij 375 px (%s)" % (pad, r["buitenBeeld"]))
            self.assertTrue(r["navInView"], "%s: navigatie niet volledig in beeld" % pad)

    def test_US001_c6_statisch_1280_px_geen_horizontaal_scrollen(self):
        for pad in ["/index.html", "/nieuws.html"]:
            self.assertFalse(self.meting(pad, 1280)["horizontalOverflow"], "%s: horizontaal scrollen bij 1280 px" % pad)

    def test_US001_c2_statisch_navigatie_precies_overzicht_en_nieuws(self):
        for pad in ["/index.html", "/nieuws.html"]:
            for w in (375, 1280):
                self.assertEqual(self.meting(pad, w)["navNames"], ["Overzicht", "Nieuws"], "%s %d px" % (pad, w))

    def test_US008_c8_statisch_1280_px_inhoud_gecentreerd_tussen_960_en_1200(self):
        for pad in ["/index.html", "/nieuws.html"]:
            r = self.meting(pad, 1280)
            self.assertGreaterEqual(r["wrapWidth"], 960, pad)
            self.assertLessEqual(r["wrapWidth"], 1200, pad)
            self.assertLessEqual(abs(r["wrapLeft"] - r["wrapRightGap"]), 1.5, "niet gecentreerd: %s" % pad)

    def test_US008_c8_statisch_375_px_kaarten_onder_elkaar(self):
        r = self.meting("/nieuws.html", 375)
        blokken = r["blokken"]
        self.assertGreaterEqual(len(blokken), 8)
        for a, b in zip(blokken, blokken[1:]):
            self.assertLessEqual(abs(a[0] - b[0]), 1, "kaarten niet in een kolom")
            self.assertGreaterEqual(b[1], a[3] - 1, "kaarten overlappen")
        self.assertEqual(len(self.meting("/index.html", 375)["tegelsCols"].split()), 1,
                         "tegels bij 375 px niet onder elkaar")

    def test_US004_c2_statisch_1280_px_tegels_naast_elkaar(self):
        """it. 6: was 'drie kolommen' bij 3 tellers. Nu 4 categorietellers (BI, Data, Automatisering, AI, US-012 c6):
        op 1280 px staan alle 4 naast elkaar in een rij."""
        self.assertEqual(len(self.meting("/index.html", 1280)["tegelsCols"].split()), 4)


if __name__ == "__main__":
    unittest.main()
