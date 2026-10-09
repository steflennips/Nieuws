"""Gedeelde hulp voor de acceptatietests van iteratie 4 (US-012, US-015, US-013 c2/c4/c5).

Regels die hier gelden:
- De statische site wordt ALTIJD naar een tijdelijke map gebouwd (nooit naar site/ in de projectmap).
- Er wordt nooit in data/ of config/ geschreven. De echte data en configuratie worden alleen gelezen.
- Geen internet: de fixture-data is lokaal (dit bestand), de browser en de server draaien op 127.0.0.1.

Dit bestand heet niet test*.py, dus unittest verzamelt het niet als testmodule.
"""
import html as htmllib
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
from functools import partial
from html.parser import HTMLParser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
BOUW = os.path.join(ROOT, "src", "bouw.py")
PROJECT_DATA = os.path.join(ROOT, "data", "nieuws.json")
PROJECT_CONFIG = os.path.join(ROOT, "config", "feeds.json")
PROJECT_SITE = os.path.join(ROOT, "site")

# Vaste fixture: bijgewerkt om 18:03 UTC op 8 oktober 2026 = 20:03 Nederlandse zomertijd.
FIXTURE_BIJGEWERKT = "2026-10-08T18:03:16+00:00"
FIXTURE_BIJGEWERKT_NL = "8 okt 2026 20:03"
# Vaste peildatum voor Uitgelicht (bouw --vandaag), zodat de fixture-tests niet van de klokdatum afhangen.
FIXTURE_VANDAAG = "2026-10-08"
ZOEKUNIEK = "ZoekUniek"
LANGE_SAMENVATTING = ("Dit is een lange samenvatting over generatieve systemen. " * 12).strip()


def fixture_items():
    """Lokale nieuwsitems (verzonnen testdata, geen echte artikelen)."""
    def it(i, titel, cat, bron, datum, sam):
        return {"id": "f%03d" % i, "titel": titel, "categorie": cat, "bron": bron, "taal": "nl",
                "datum": datum, "samenvatting": sam,
                "url": "https://voorbeeld-bron.example/artikel-%03d" % i}
    return [
        it(1, "Datawarehouse-keuze voor het mkb", "Data", "Fixture Bron A", "2026-10-07",
           "Een vergelijking van datawarehouses voor kleine teams."),
        it(2, "Open data van gemeenten beter vindbaar", "Data", "Fixture Bron B", "2026-10-03",
           "Gemeenten publiceren meer open data."),
        it(3, "Workflow-automatisering bespaart uren", "Automatisering", "Fixture Bron A", "2026-10-06",
           "Een workflow die handmatig werk overneemt."),
        it(4, "Low-code tools winnen terrein", "Automatisering", "Fixture Bron B", "2026-10-02",
           "Low-code platformen versnellen de bouw van interne apps."),
        it(5, "Taalmodellen worden goedkoper", "AI", "Fixture Bron A", "2026-10-08",
           "Nieuwe taalmodellen kosten minder per vraag."),
        it(6, "Chatbot voor de klantenservice", "AI", "Fixture Bron B", "2026-10-05", LANGE_SAMENVATTING),
        # it. 6 (US-016 c4): was categorie AI; met 4 AI en 4 overige items valt een AI-item weg door het AI-plafond.
        # Nu BI, zodat de fixture ook BI dekt en alle 8 items getoond worden.
        it(7, "Dashboards voor de zorg: alles in een scherm", "BI", "Fixture Bron A", "2026-09-30",
           "Zorgorganisaties testen rapportages. Tom &amp; Jerry <b>vet</b> in de tekst."),
        it(8, "Zoekbaar nieuws over %s" % ZOEKUNIEK, "AI", "Fixture Bron B", "2026-09-28",
           "De samenvatting bevat het woord %s." % ZOEKUNIEK),
    ]


def schrijf_fixture_data(map):
    pad = os.path.join(map, "nieuws.json")
    with open(pad, "w", encoding="utf-8") as f:
        json.dump({"bijgewerkt": FIXTURE_BIJGEWERKT, "items": fixture_items()}, f, ensure_ascii=False)
    return pad


def omgeving():
    env = dict(os.environ)
    env.pop("NIEUWS_BRON", None)
    env.update({"PYTHONIOENCODING": "utf-8", "NO_PROXY": "127.0.0.1,localhost", "no_proxy": "127.0.0.1,localhost"})
    return env


def verwacht_getoond(items):
    """Onafhankelijke uitwerking van het AI-plafond (US-016 c4), los van de code in src/mix.py.

    Alle niet-AI items blijven. Van AI de nieuwste k, met k = de grootste waarde waarvoor AI <= 40% van het totaal:
    3k <= 2n (n = aantal niet-AI), dus k = (2n) // 3. Voorbeeld: 20 niet-AI -> 13 AI.
    Geeft de getoonde items (zelfde dict-objecten als in de invoer)."""
    niet_ai = [i for i in items if i["categorie"] != "AI"]
    ai = sorted((i for i in items if i["categorie"] == "AI"), key=lambda i: i["datum"], reverse=True)
    k = (2 * len(niet_ai)) // 3
    return niet_ai + ai[:k]


def bouw(uit, data=None, config=PROJECT_CONFIG, vandaag=None):
    """Draait src/bouw.py met de opgegeven data naar een uitvoermap. Geeft (exitcode, stdout, stderr)."""
    cmd = [sys.executable, "-B", BOUW, "--config", config, "--uit", uit]
    if vandaag:
        cmd += ["--vandaag", vandaag]
    if data is not None:
        cmd += ["--data", data]
    else:
        cmd += ["--data", os.path.join(uit, "geen-data", "nieuws.json")]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace",
                       env=omgeving(), timeout=120, cwd=tempfile.gettempdir())
    return r.returncode, r.stdout, r.stderr


def nieuwe_tijdelijke_map(prefix="t4-site-"):
    return tempfile.mkdtemp(prefix=prefix)


def lees(pad):
    with open(pad, encoding="utf-8") as f:
        return f.read()


def tekst_van(html_fragment):
    """HTML -> platte, samengevouwen tekst (voor zoek- en telcontroles)."""
    t = re.sub(r"<[^>]*>", " ", html_fragment)
    return re.sub(r"\s+", " ", htmllib.unescape(t)).strip()


class _Stil(SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


class StatischeServer:
    """Serveert een map als eenvoudige statische server op 127.0.0.1 (poort vrij gekozen)."""

    def __init__(self, map):
        self.map = map
        self.srv = ThreadingHTTPServer(("127.0.0.1", 0), partial(_Stil, directory=map))
        self.base = "http://127.0.0.1:%d" % self.srv.server_address[1]
        self.thread = threading.Thread(target=self.srv.serve_forever, daemon=True)

    def __enter__(self):
        self.thread.start()
        return self

    def __exit__(self, *a):
        self.srv.shutdown()
        self.srv.server_close()

    def get(self, pad):
        import urllib.error
        import urllib.request
        try:
            with urllib.request.urlopen(self.base + pad, timeout=10) as r:
                return r.status, r.headers.get("Content-Type", ""), r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            return e.code, e.headers.get("Content-Type", ""), e.read().decode("utf-8", "replace")


def html_bestanden(map):
    return sorted(n for n in os.listdir(map) if n.endswith(".html"))


# ---------- DOM-controle (uitvoer van Edge --dump-dom) ----------
def kaarten_in(dom):
    """Lijst van nieuwskaarten: {'cat', 'verborgen', 'h2', 'p'} in volgorde van de pagina."""
    uit = []
    for attrs, inhoud in re.findall(r'<article class="kaart"([^>]*)>(.*?)</article>', dom, re.S):
        cat = re.search(r'data-categorie="([^"]*)"', attrs)
        h2 = re.search(r"<h2>(.*?)</h2>", inhoud, re.S)
        p = re.search(r"<p>(.*?)</p>", inhoud, re.S)
        uit.append({"cat": cat.group(1) if cat else None, "verborgen": bool(re.search(r"\shidden(=|\s|$)", attrs)),
                    "h2": tekst_van(h2.group(1)) if h2 else "", "p": tekst_van(p.group(1)) if p else ""})
    return uit


def zichtbare_kaarten(dom):
    return [k for k in kaarten_in(dom) if not k["verborgen"]]


def chips_in(dom):
    uit = []
    for m in re.finditer(r'<a class="([^"]*\bchip\b[^"]*)"([^>]*)>(.*?)</a>', dom, re.S):
        href = re.search(r'href="([^"]*)"', m.group(2))
        uit.append({"actief": "actief" in m.group(1).split(), "href": htmllib.unescape(href.group(1)) if href else None,
                    "tekst": tekst_van(m.group(3)), "aria": bool(re.search(r"aria-current", m.group(2)))})
    return uit


def element_tekst(dom, id_):
    m = re.search(r'<(\w+)[^>]*\bid="%s"([^>]*)>(.*?)</\1>' % re.escape(id_), dom, re.S)
    if not m:
        return None, False
    return tekst_van(m.group(3)), bool(re.search(r"\shidden(=|\s|$)", m.group(2)))


def zoekveld_waarde(dom):
    m = re.search(r'<input[^>]*\bid="zoekveld"[^>]*>', dom)
    if not m:
        return None
    v = re.search(r'\bvalue="([^"]*)"', m.group(0))
    return htmllib.unescape(v.group(1)) if v else ""


# ---------- Edge (headless, alleen lokaal) ----------
EDGE_KANDIDATEN = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]


def vind_edge():
    for pad in EDGE_KANDIDATEN:
        if os.path.exists(pad):
            return pad
    return None


def stop_edge_profiel(profiel):
    """Stopt alle Edge-processen die met dit eigen tijdelijke profiel zijn gestart (inclusief kinderen).

    Edge start op Windows vaak een launcher die meteen eindigt; de browser zelf draait dan los door.
    Zonder deze stap blijven headless-processen achter. Alleen processen met dit profielpad worden gestopt.
    """
    if sys.platform != "win32":
        return
    script = ("Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'msedge.exe' -and "
              "$_.CommandLine -like '*%s*' } | "
              "ForEach-Object { & taskkill /F /T /PID $_.ProcessId | Out-Null }") % profiel
    subprocess.run(["powershell.exe", "-NoProfile", "-Command", script], capture_output=True, timeout=120)


def stop_proces(proc):
    """Stopt een proces inclusief kinderen (Edge start er meerdere)."""
    if proc.poll() is None:
        if sys.platform == "win32":
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)], capture_output=True)
        else:
            proc.kill()
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        pass


def pad_van(url):
    p = urlparse(url)
    return p.path + ("?" + p.query if p.query else "")
