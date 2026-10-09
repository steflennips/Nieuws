"""Gedeelde hulp voor de acceptatietests van fase 2 (US-009, US-010, US-011, echte data).

Geen internet nodig: de tests draaien een lokale testserver op 127.0.0.1 met RSS-, Atom-, kapotte
en trage feeds. Dit bestand heet niet test*.py, dus unittest verzamelt het niet als testmodule.
"""
import copy
import email.utils
import json
import os
import socket
import subprocess
import sys
import tempfile
import threading
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SRC = os.path.join(ROOT, "src")
OPHALEN = os.path.join(SRC, "ophalen.py")
PROJECT_CONFIG = os.path.join(ROOT, "config", "feeds.json")
NIEUWS_JSON = os.path.join(ROOT, "data", "nieuws.json")


def project_config():
    """Leest de echte configuratie (alleen-lezen); de trefwoorden van het project worden zo getest."""
    with open(PROJECT_CONFIG, encoding="utf-8") as f:
        return json.load(f)


def vandaag():
    return datetime.now(timezone.utc).date()


def rfc(dagen_terug, uur=12):
    dt = datetime.combine(vandaag() - timedelta(days=dagen_terug), datetime.min.time(), tzinfo=timezone.utc)
    return email.utils.format_datetime(dt.replace(hour=uur))


def iso_dag(dagen_terug):
    return (vandaag() - timedelta(days=dagen_terug)).isoformat()


def vrije_poort():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    poort = s.getsockname()[1]
    s.close()
    return poort


def omgeving(extra=None):
    """Omgeving voor subprocessen: geen proxy voor localhost, UTF-8 uitvoer, geen NIEUWS_BRON-forcering."""
    env = dict(os.environ)
    env.pop("NIEUWS_BRON", None)
    env.update({"NO_PROXY": "127.0.0.1,localhost", "no_proxy": "127.0.0.1,localhost",
                "PYTHONIOENCODING": "utf-8", "PYTHONUNBUFFERED": "1"})
    if extra:
        env.update(extra)
    return env


class FeedServer:
    """Lokale testserver. routes: pad -> dict(body=bytes|callable(base)->bytes, status, ctype, delay).

    Alle opgevraagde paden worden bijgehouden in self.opgevraagd (voor de robots.txt-test).
    """

    def __init__(self, routes):
        self.routes = routes
        self.opgevraagd = []
        self.srv = None

    def __enter__(self):
        outer = self

        class H(BaseHTTPRequestHandler):
            def do_GET(self):
                pad = urlparse(self.path).path
                outer.opgevraagd.append(pad)
                rt = outer.routes.get(pad)
                if rt is None:
                    body, status, ctype, delay = b"niet gevonden", 404, "text/plain", 0
                else:
                    body = rt["body"](outer.base) if callable(rt["body"]) else rt["body"]
                    if isinstance(body, str):
                        body = body.encode("utf-8")
                    status, ctype, delay = rt.get("status", 200), rt.get("ctype", "application/xml"), rt.get("delay", 0)
                if delay:
                    import time
                    time.sleep(delay)
                try:
                    self.send_response(status)
                    self.send_header("Content-Type", ctype + "; charset=utf-8")
                    self.send_header("Content-Length", str(len(body)))
                    self.end_headers()
                    self.wfile.write(body)
                except OSError:
                    pass

            def log_message(self, *a):
                pass

        self.srv = ThreadingHTTPServer(("127.0.0.1", 0), H)
        self.srv.daemon_threads = True
        self.base = "http://127.0.0.1:%d" % self.srv.server_address[1]
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()
        return self

    def __exit__(self, *a):
        self.srv.shutdown()
        self.srv.server_close()

    def url(self, pad):
        return self.base + pad


def rss_feed(base):
    """RSS 2.0 met: HTML + afbeelding in beschrijving, & in link, item zonder datum, item zonder titel,
    en een zeer lange tekst."""
    lang = ("Dit is de eerste zin over datawarehouses en rapportages. " * 30)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0"><channel><title>Testfeed RSS</title>'
        '<item><title>Nieuwe AI-tool voor kantoren</title>'
        '<link>%(b)s/artikel/1?a=1&amp;b=2</link>'
        '<description>&lt;p&gt;Een &lt;b&gt;korte&lt;/b&gt; tekst met &lt;img src="x.jpg"&gt;.&lt;/p&gt;</description>'
        '<pubDate>%(d1)s</pubDate></item>'
        '<item><title>Datawarehouse wordt goedkoper</title><link>%(b)s/artikel/2</link>'
        '<description>%(lang)s</description><pubDate>%(d2)s</pubDate></item>'
        '<item><title></title><link>%(b)s/artikel/3</link><description>Lege titel met AI</description>'
        '<pubDate>%(d1)s</pubDate></item>'
        '<item><title>Automatisering van workflows bij de gemeente</title><link>%(b)s/artikel/4</link>'
        '<description>Zonder datum.</description></item>'
        '</channel></rss>' % {"b": base, "d1": rfc(2), "d2": rfc(5), "lang": lang})


def atom_feed(base):
    return (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<feed xmlns="http://www.w3.org/2005/Atom"><title>Testfeed Atom</title>'
        '<entry><title>Machine learning in de praktijk</title>'
        '<link rel="alternate" href="%(b)s/atom/1"/>'
        '<summary>Samenvatting &amp; meer over modellen</summary>'
        '<published>%(p)s</published></entry>'
        '<entry><title>Kunstmatige intelligentie bij gemeenten</title>'
        '<link href="%(b)s/atom/2"/>'
        '<content type="html">&lt;p&gt;Volledige tekst van het artikel&lt;/p&gt;</content>'
        '<updated>%(u)s</updated></entry>'
        '</feed>' % {"b": base, "p": "%sT09:00:00+00:00" % iso_dag(1), "u": "%sT10:00:00Z" % iso_dag(4)})


KAPOT_XML = b'<?xml version="1.0"?><rss version="2.0"><channel><item><title>kapot</channel>'
HTML_PAGINA = b"<!DOCTYPE html><html><head><title>Onderhoud</title></head><body>Even weg</body></html>"


def schrijf_config(pad, feeds, timeout=15, bewaar_dagen=60):
    cfg = copy.deepcopy(project_config())
    cfg["feeds"] = feeds
    cfg["timeout_seconden"] = timeout
    cfg["bewaar_dagen"] = bewaar_dagen
    with open(pad, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=1)
    return pad


def run_ophalen(config_pad, uitvoer, extra=()):
    """Draait src/ophalen.py zoals de README voorschrijft (zonder --geen-robots, tenzij in extra)."""
    return subprocess.run([sys.executable, "-B", OPHALEN, "--config", config_pad, "--uitvoer", uitvoer] + list(extra),
                          capture_output=True, text=True, encoding="utf-8", env=omgeving(), timeout=90)


def lees_json(pad):
    with open(pad, encoding="utf-8") as f:
        return json.load(f)


def tmp_map():
    return tempfile.mkdtemp(prefix="t3-accept-")
