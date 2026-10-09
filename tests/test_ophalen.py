"""Eigen tests voor ophalen, categoriseren en foutafhandeling. Geen internet nodig:
feeds worden door een lokale testserver (127.0.0.1) geleverd."""
import json
import os
import subprocess
import sys
import tempfile
import threading
import unittest
from datetime import date, datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src")
sys.path.insert(0, SRC)
import ophalen  # noqa: E402

NU = datetime(2026, 10, 8, 12, 0, tzinfo=timezone.utc)
TREFWOORDEN = {
    "BI": ["power bi"],  # US-022 c3: alle vier de categorieen zijn verplicht in een config
    "AI": ["ai", "machine learning", "llm*", "chatbot*"],
    "Automatisering": ["automati*", "workflow*", "rpa"],
    "Data": ["data", "dataset*", "dashboard*"],
}
MATCHERS = ophalen.maak_matchers(TREFWOORDEN)

RSS = """<?xml version="1.0"?><rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/"><channel>
<item><title>Nieuwe AI-assistent voor klantenservice</title><link>http://x.test/rss1</link>
<description>&lt;p&gt;Een &lt;b&gt;chatbot&lt;/b&gt; helpt.&lt;/p&gt;&lt;img src="http://x.test/a.png"&gt;&lt;script&gt;boem()&lt;/script&gt;</description>
<pubDate>Wed, 07 Oct 2026 09:00:00 +0200</pubDate></item>
<item><title>Workflow automatiseren zonder code</title><link>http://x.test/rss2</link><description>Korte tekst</description></item>
<item><title></title><link>http://x.test/rss3</link><description>data zonder titel</description></item>
<item><title>Recept voor appeltaart</title><link>http://x.test/rss4</link><description>Lekker</description></item>
</channel></rss>"""

OUD = """<?xml version="1.0"?><rss version="2.0"><channel>
<item><title>Oud AI-nieuws</title><link>http://x.test/oud1</link><description>x</description>
<pubDate>Mon, 07 Apr 2025 09:00:00 +0200</pubDate></item>
<item><title>Vers AI-nieuws</title><link>http://x.test/vers1</link><description>x</description>
<pubDate>Wed, 07 Oct 2026 09:00:00 +0200</pubDate></item>
</channel></rss>"""

ATOM = """<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom"><title>Atom</title>
<entry><title>Dashboard met nieuwe dataset</title><link rel="alternate" href="http://x.test/atom1"/>
<summary>Een samenvatting</summary><updated>2026-10-06T08:00:00Z</updated></entry></feed>"""

TITELS = [  # (titel, verwachte categorie): vaste testset US-010 c5
    ("OpenAI lanceert nieuw LLM voor ontwikkelaars", "AI"),
    ("Machine learning in de zorg", "AI"),
    ("Chatbots nemen klantcontact over", "AI"),
    ("Bedrijven automatiseren hun facturen met RPA", "Automatisering"),
    ("Workflow automation voor het mkb", "Automatisering"),
    ("Zo bouw je een dashboard op open data", "Data"),
    ("Nieuwe dataset over bedrijvigheid gepubliceerd", "Data"),
    ("Data en dashboards: wat werkt", "Data"),
    ("AI automatiseert workflows en data-analyse bij AI-start-up", "Automatisering"),  # 2 AI, 2 Automatisering: gelijkspel -> Automatisering
    ("Data en automatisering", "Data"),  # gelijkspel Data/Automatisering: Data wint (volgorde BI, Data, Automatisering, AI)
    ("AI en data in de logistiek", "Data"),  # gelijkspel AI/Data: Data wint
]


class TestCategorie(unittest.TestCase):
    def test_vaste_testset(self):
        for titel, verwacht in TITELS:
            self.assertEqual(ophalen.categoriseer(titel, "", MATCHERS), verwacht, titel)

    def test_hele_woorden(self):
        self.assertIsNone(ophalen.categoriseer("Je mail en je maintenance", "", MATCHERS))
        self.assertEqual(ophalen.categoriseer("Nieuwe AI", "", MATCHERS), "AI")
        self.assertEqual(ophalen.categoriseer("nieuwe ai", "", MATCHERS), "AI")

    def test_meeste_treffers(self):
        self.assertEqual(ophalen.categoriseer("Data dashboard dataset en een chatbot", "", MATCHERS), "Data")

    def test_samenvatting_telt_mee(self):
        self.assertEqual(ophalen.categoriseer("Zonder treffer", "Gaat over RPA", MATCHERS), "Automatisering")

    def test_config_heeft_trefwoorden_nl_en(self):
        with open(os.path.join(SRC, "..", "config", "feeds.json"), encoding="utf-8") as f:
            cfg = json.load(f)
        for cat in ("Data", "Automatisering", "AI"):
            self.assertTrue(cfg["trefwoorden"][cat])
        alle = " ".join(" ".join(v) for v in cfg["trefwoorden"].values()).casefold()
        for w in ("kunstmatige intelligentie", "artificial intelligence", "automati*", "gegevens", "analytics"):
            self.assertIn(w, alle)

    def test_config_feeds(self):
        with open(os.path.join(SRC, "..", "config", "feeds.json"), encoding="utf-8") as f:
            feeds = json.load(f)["feeds"]
        self.assertTrue(8 <= len(feeds) <= 10)
        self.assertGreaterEqual(len([x for x in feeds if x["taal"] == "nl"]), 3)
        self.assertGreaterEqual(len([x for x in feeds if x["taal"] == "en"]), 3)
        for x in feeds:
            self.assertTrue(x["naam"] and x["url"].startswith("https://"))


class TestTekst(unittest.TestCase):
    def test_html_weg_en_afkappen(self):
        t = ophalen.platte_tekst("<p>Hallo <b>wereld</b></p><img src='x.png'><script>x()</script>")
        self.assertEqual(t, "Hallo wereld")
        lang = ophalen.platte_tekst("<p>" + "woord " * 200 + "</p>", 300)
        self.assertLessEqual(len(lang), 300)
        self.assertTrue(lang.endswith("..."))
        self.assertNotIn("<", lang)

    def test_entiteiten_een_keer_gedecodeerd(self):
        self.assertEqual(ophalen.platte_tekst("Tom &amp;amp; Jerry"), "Tom &amp; Jerry")
        self.assertEqual(ophalen.platte_tekst("Tom &amp; Jerry &lt;b&gt;"), "Tom & Jerry <b>")


class TestParsen(unittest.TestCase):
    def verwerk(self, xml):
        ruw = ophalen.parse_feed(xml.encode())
        return ophalen.verwerk_items(ruw, {"naam": "Test", "taal": "nl"}, MATCHERS, NU.date())

    def test_rss(self):
        items, zonder_titel, zonder_cat = self.verwerk(RSS)
        self.assertEqual((len(items), zonder_titel, zonder_cat), (2, 1, 1))
        a = items[0]
        self.assertEqual((a["titel"], a["categorie"], a["bron"], a["taal"], a["datum"], a["url"]),
                         ("Nieuwe AI-assistent voor klantenservice", "AI", "Test", "nl", "2026-10-07", "http://x.test/rss1"))
        self.assertEqual(a["samenvatting"], "Een chatbot helpt.")
        self.assertNotIn("boem", a["samenvatting"])

    def test_item_zonder_datum_krijgt_ophaaldatum(self):
        items, _, _ = self.verwerk(RSS)
        self.assertEqual(items[1]["datum"], "2026-10-08")

    def test_atom(self):
        items, _, _ = self.verwerk(ATOM)
        self.assertEqual(len(items), 1)
        self.assertEqual((items[0]["categorie"], items[0]["datum"], items[0]["url"]),
                         ("Data", "2026-10-06", "http://x.test/atom1"))

    def test_ongeldige_xml_en_html(self):
        for slecht in (b"<rss><channel><item>", b"<!DOCTYPE html><html></html>", b"geen xml"):
            with self.assertRaises(ophalen.FeedFout):
                ophalen.parse_feed(slecht)

    def test_entity_declaratie_geweigerd(self):
        with self.assertRaises(ophalen.FeedFout):
            ophalen.parse_feed(b'<?xml version="1.0"?><!DOCTYPE x [<!ENTITY a "b">]><rss><channel/></rss>')


class _Handler(BaseHTTPRequestHandler):
    routes = {}

    def do_GET(self):
        r = self.routes.get(self.path)
        if r is None:
            self.send_response(404)
            self.end_headers()
            return
        self.send_response(200)
        self.end_headers()
        self.wfile.write(r if isinstance(r, bytes) else r.encode())

    def log_message(self, *a):
        pass


class TestOphalen(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _Handler.routes = {"/rss": RSS, "/atom": ATOM, "/kapot": "<rss><channel><item>", "/oud": OUD,
                           "/robots.txt": "User-agent: *\nDisallow: /verboden\n", "/verboden": RSS}
        cls.srv = ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
        cls.base = "http://127.0.0.1:%d" % cls.srv.server_address[1]
        threading.Thread(target=cls.srv.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()
        cls.srv.server_close()

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.uitvoer = os.path.join(self.tmp.name, "nieuws.json")
        self.log = []

    def tearDown(self):
        self.tmp.cleanup()

    def cfg(self, *feeds):
        return {"user_agent": "TestBot/1.0", "bewaar_dagen": 60, "timeout_seconden": 3, "max_samenvatting": 300,
                "trefwoorden": TREFWOORDEN,
                "feeds": [{"naam": n, "url": self.base + p, "taal": "nl"} for n, p in feeds]}

    def draai(self, cfg, nu=NU, robots=False):
        return ophalen.draai(cfg, self.uitvoer, controleer_robots=robots, nu=nu, log=self.log.append)

    def lees(self):
        with open(self.uitvoer, encoding="utf-8") as f:
            return json.load(f)

    def test_rss_en_atom_opgeslagen(self):
        self.assertEqual(self.draai(self.cfg(("R", "/rss"), ("A", "/atom"))), 0)
        d = self.lees()
        self.assertEqual(len(d["items"]), 3)
        for i in d["items"]:
            for k in ("titel", "samenvatting", "datum", "bron", "taal", "url", "categorie"):
                self.assertTrue(i[k], k)
        self.assertEqual([i["datum"] for i in d["items"]], sorted((i["datum"] for i in d["items"]), reverse=True))

    def test_geen_duplicaten_bij_opnieuw_ophalen(self):
        cfg = self.cfg(("R", "/rss"))
        self.draai(cfg)
        self.draai(cfg)
        urls = [i["url"] for i in self.lees()["items"]]
        self.assertEqual(len(urls), len(set(urls)))
        self.assertEqual(len(urls), 2)

    def test_oude_items_verwijderd(self):
        cfg = self.cfg(("R", "/rss"))
        self.draai(cfg)
        d = self.lees()
        d["items"].append({"id": "oud", "titel": "Oud AI", "categorie": "AI", "bron": "R", "taal": "nl",
                           "datum": (NU.date() - timedelta(days=61)).isoformat(), "samenvatting": "x", "url": "http://x.test/oud"})
        d["items"].append({"id": "grens", "titel": "Grens AI", "categorie": "AI", "bron": "R", "taal": "nl",
                           "datum": (NU.date() - timedelta(days=60)).isoformat(), "samenvatting": "x", "url": "http://x.test/grens"})
        with open(self.uitvoer, "w", encoding="utf-8") as f:
            json.dump(d, f)
        self.draai(cfg)
        urls = [i["url"] for i in self.lees()["items"]]
        self.assertNotIn("http://x.test/oud", urls)
        self.assertIn("http://x.test/grens", urls)

    def test_kapotte_feed_andere_feeds_gaan_door_en_oude_items_blijven(self):
        self.draai(self.cfg(("A", "/atom")))
        vooraf = len(self.lees()["items"])
        self.log.clear()
        code = self.draai(self.cfg(("Kapot", "/kapot"), ("Weg", "/bestaatniet"), ("R", "/rss"), ("A", "/atom")))
        self.assertEqual(code, 0)
        self.assertEqual(len(self.lees()["items"]), vooraf + 2)
        tekst = "\n".join(self.log)
        self.assertIn("FOUT  Kapot: ongeldige XML", tekst)
        self.assertIn("FOUT  Weg: HTTP 404", tekst)
        self.assertIn("OK    R:", tekst)

    def test_oude_items_van_mislukte_feed_blijven(self):
        self.draai(self.cfg(("A", "/atom")))
        self.draai(self.cfg(("A", "/kapot"), ("R", "/rss")))
        urls = [i["url"] for i in self.lees()["items"]]
        self.assertIn("http://x.test/atom1", urls)

    def test_items_van_bron_buiten_config_worden_verwijderd(self):
        """US-019 c3: bron niet meer in config -> items weg; bron in config maar falend -> items blijven."""
        self.draai(self.cfg(("A", "/atom"), ("R", "/rss")))
        d = self.lees()
        d["items"].append({"id": "x", "titel": "Oud AI-bericht van verwijderde bron", "categorie": "AI", "bron": "Verwijderd",
                           "taal": "en", "datum": "2026-10-07", "samenvatting": "x", "url": "http://x.test/verwijderd"})
        with open(self.uitvoer, "w", encoding="utf-8") as f:
            json.dump(d, f)
        # A valt uit (kapot) maar staat nog in de config; "Verwijderd" staat er niet meer in.
        self.assertEqual(self.draai(self.cfg(("A", "/kapot"), ("R", "/rss"))), 0)
        urls = [i["url"] for i in self.lees()["items"]]
        self.assertNotIn("http://x.test/verwijderd", urls)
        self.assertIn("http://x.test/atom1", urls)

    def test_alle_feeds_mislukt_bestand_ongewijzigd_en_foutcode(self):
        self.draai(self.cfg(("A", "/atom")))
        voor = open(self.uitvoer, "rb").read()
        code = self.draai(self.cfg(("Kapot", "/kapot"), ("Weg", "/bestaatniet")))
        self.assertNotEqual(code, 0)
        self.assertEqual(open(self.uitvoer, "rb").read(), voor)

    def test_onbereikbaar(self):
        cfg = self.cfg(("R", "/rss"))
        cfg["feeds"].insert(0, {"naam": "Dood", "url": "http://127.0.0.1:1/feed", "taal": "nl"})
        self.assertEqual(self.draai(cfg), 0)
        self.assertTrue(any(r.startswith("FOUT  Dood: niet bereikbaar") for r in self.log))

    def test_robots_txt_wordt_gerespecteerd(self):
        cfg = self.cfg(("Verboden", "/verboden"), ("R", "/rss"))
        self.assertEqual(self.draai(cfg, robots=True), 0)
        self.assertTrue(any("FOUT  Verboden: niet toegestaan volgens robots.txt" in r for r in self.log))
        self.assertTrue(any(r.startswith("OK    R:") for r in self.log))

    def test_cli_exitcodes(self):
        cfg = self.cfg(("R", "/rss"))
        cfgpad = os.path.join(self.tmp.name, "cfg.json")
        with open(cfgpad, "w", encoding="utf-8") as f:
            json.dump(cfg, f)
        basis = [sys.executable, "-I", os.path.join(SRC, "ophalen.py"), "--config", cfgpad, "--uitvoer", self.uitvoer, "--geen-robots"]
        self.assertEqual(subprocess.run(basis, capture_output=True, timeout=60).returncode, 0)
        cfg["feeds"] = [{"naam": "Weg", "url": self.base + "/nee", "taal": "nl"}]
        with open(cfgpad, "w", encoding="utf-8") as f:
            json.dump(cfg, f)
        self.assertNotEqual(subprocess.run(basis, capture_output=True, timeout=60).returncode, 0)

    def test_bewaard_telt_na_leeftijdsfilter_en_verouderd_apart(self):
        self.assertEqual(self.draai(self.cfg(("O", "/oud"))), 0)
        regel = [r for r in self.log if r.startswith("OK    O:")][0]
        self.assertIn("2 items in feed, 1 bewaard (1 nieuw), 1 verouderd", regel)
        d = self.lees()
        st = d["feeds"][0]
        self.assertEqual((st["bewaard"], st["verouderd"]), (1, 1))
        self.assertEqual(len([i for i in d["items"] if i["bron"] == "O"]), st["bewaard"])
        self.assertNotIn("http://x.test/oud1", [i["url"] for i in d["items"]])

    def test_cli_config_ontbreekt_of_ongeldig_geeft_nette_melding(self):
        basis = [sys.executable, "-I", os.path.join(SRC, "ophalen.py"), "--uitvoer", self.uitvoer, "--config"]
        r = subprocess.run(basis + [os.path.join(self.tmp.name, "bestaat-niet.json")], capture_output=True, timeout=60)
        self.assertEqual(r.returncode, 2)
        self.assertIn(b"FOUT", r.stderr)
        self.assertNotIn(b"Traceback", r.stderr)
        kapot = os.path.join(self.tmp.name, "kapot.json")
        for inhoud in ("{niet json", "[]", '{"feeds": 5}'):
            with open(kapot, "w", encoding="utf-8") as f:
                f.write(inhoud)
            r = subprocess.run(basis + [kapot], capture_output=True, timeout=60)
            self.assertEqual(r.returncode, 2, inhoud)
            self.assertIn(b"FOUT", r.stderr)
            self.assertNotIn(b"Traceback", r.stderr)
        self.assertFalse(os.path.exists(self.uitvoer))


if __name__ == "__main__":
    unittest.main()
