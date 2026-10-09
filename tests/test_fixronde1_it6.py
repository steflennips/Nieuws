"""Eigen tests fixronde 1 iteratie 6: weigerpatronen, uitzonderingen, 'gegevens', ongeldige datum, alleen-AI, unieke links."""
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import date, datetime, timezone
from pathlib import Path

BASIS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASIS / "src"))
import bouw  # noqa: E402
import ophalen  # noqa: E402

CFG = json.loads((BASIS / "config" / "feeds.json").read_text(encoding="utf-8"))
M = ophalen.maak_matchers(CFG["trefwoorden"], CFG.get("uitsluitingen"))
W = ophalen.maak_weigerlijst(CFG)


class TestWeigerpatronen(unittest.TestCase):
    def test_geweigerd(self):
        for t in ["Nog vier weken tot Emerce EDAY", "Nog 3 dagen tot de deadline", "Save the date: Summit", "Early bird korting",
                  "Camunda Named a Leader in The Forrester Wave: Adaptive Process Orchestration Software, Q3 2026",
                  "Camunda Recognized as a Visionary in Gartner BOAT Magic Quadrant 2026",
                  "You can now top up your n8n Assistant credits", "Tickets voor de beurs", "Review: Samsung Galaxy S26",
                  "De beste games van 2026"]:
            self.assertIsNotNone(W.reden(t, ""), t)

    def test_toegelaten(self):
        for t in ["Salesforce neemt Informatica over", "Power BI September 2026 Feature Summary",
                  "Fabric Warehouse is generally available", "Gartner ziet BI-markt groeien",
                  "Run an automated operational review with the Amazon Redshift MCP server",
                  "Gemini, metadata and the analogy game", "Game theory in prijsstrategie", "Gamechanger voor MKB",
                  "Een game changer voor data", "Code review met AI", "Nog weinig tijd tot de deadline"]:
            self.assertIsNone(W.reden(t, ""), t)

    def test_patronen_in_config(self):
        tekst = " ".join(CFG["weigertermen"]).casefold()
        for t in ["save the date", "early bird", "tickets", "named a leader", "named a visionary", "recognized as a",
                  "recognised as a", "magic quadrant", "forrester wave", "credits"]:
            self.assertIn(t, tekst)
        self.assertIn("weken", tekst)
        for t in ["operational review", "code review", "peer review", "security review", "analogy game", "game theory",
                  "gamechanger", "game changer"]:
            self.assertIn(t, CFG["weiger_uitzonderingen"])


class TestGegevens(unittest.TestCase):
    def test_los_gegevens_geen_data_trefwoord(self):
        self.assertNotIn("gegevens", [w.casefold() for w in CFG["trefwoorden"]["Data"]])

    def test_nos_titels_geen_data(self):
        for t in ["Amsterdammer opgepakt in onderzoek naar hackerscollectief ShinyHunters",
                  "Hackers persen klanten boodschappendienst Flink af: betalen of data gepubliceerd",
                  "Datalek bij reisapp Polarsteps: iedereen kon meekijken, ook met afgeschermde reizen"]:
            self.assertNotEqual(ophalen.categoriseer(t, "Persoonlijke gegevens van klanten zijn gelekt.", M), "Data", t)

    def test_samenstelling_blijft_data(self):
        self.assertEqual(ophalen.categoriseer("Betere gegevenskwaliteit in je bedrijf", "", M), "Data")


def item(titel, cat, datum, n):
    return {"id": str(n), "titel": titel, "categorie": cat, "bron": "Test", "taal": "nl", "datum": datum,
            "samenvatting": "s", "url": "https://example.com/%d" % n}


class TestBouw(unittest.TestCase):
    def bouw(self, items):
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        data = Path(d.name) / "n.json"
        data.write_text(json.dumps({"bijgewerkt": "2026-10-08T04:00:00+00:00", "items": items}), encoding="utf-8")
        uit = Path(d.name) / "site"
        r = subprocess.run([sys.executable, str(BASIS / "src" / "bouw.py"), "--data", str(data), "--uit", str(uit),
                            "--vandaag", "2026-10-08"], capture_output=True, text=True, encoding="utf-8")
        return r, uit

    def test_ongeldige_datum_overgeslagen(self):
        r, uit = self.bouw([item("Goed item", "BI", "2026-10-08", 1), item("Kapot item", "BI", "garbage", 2)])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("Kapot item", r.stdout + r.stderr)
        html = (uit / "nieuws.html").read_text(encoding="utf-8")
        self.assertIn("Goed item", html)
        self.assertNotIn("Kapot item", html)

    def test_alleen_ai_melding(self):
        r, _ = self.bouw([item("AI nieuws %d" % n, "AI", "2026-10-08", n) for n in range(5)])
        self.assertEqual(r.returncode, 1)
        self.assertIn("AI-plafond", r.stderr)
        self.assertIn("40%", r.stderr)
        self.assertNotIn("bevat geen nieuwsitems", r.stderr)

    def test_tegels_1_kolom_op_smal(self):
        self.assertIn("@media (max-width:720px){.tegels{grid-template-columns:1fr}}", bouw.CSS)
        self.assertIn("grid-template-columns:repeat(4,1fr)", bouw.CSS)


class TestUniekeLinks(unittest.TestCase):
    def test_dubbele_link_telt_een_keer(self):
        rss = ("<rss><channel>" + "".join(
            "<item><title>Power BI dashboard update</title><link>https://example.com/a</link><pubDate>Thu, 08 Oct 2026 08:00:00 GMT</pubDate></item>"
            for _ in range(3)) + "</channel></rss>").encode()
        cfg = dict(CFG, feeds=[{"naam": "T", "url": "http://x/feed", "taal": "en"}])
        regels = []
        with tempfile.TemporaryDirectory() as d:
            code = ophalen.draai(cfg, str(Path(d) / "n.json"), controleer_robots=False, lees=lambda u, a, t: rss,
                                 nu=datetime(2026, 10, 8, 12, tzinfo=timezone.utc), log=regels.append)
        self.assertEqual(code, 0)
        self.assertIn("1 bewaard (1 nieuw)", regels[0])


if __name__ == "__main__":
    unittest.main()
