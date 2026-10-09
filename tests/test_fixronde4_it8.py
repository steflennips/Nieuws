"""Fixronde 4 iteratie 8 (US-022): bewaar_dagen-validatie, vangnet voor de leeftijdsopruiming, onvolledige opgeslagen items.
Geen internet: de feed wordt via een stub gelezen."""
import json
import os
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
import ophalen  # noqa: E402

NU = datetime(2026, 10, 8, 12, 0, tzinfo=timezone.utc)
RSS = (b'<?xml version="1.0"?><rss version="2.0"><channel><item><title>Nieuwe bikern</title>'
       b'<link>http://x.test/nieuw1</link><description>x</description>'
       b'<pubDate>Wed, 07 Oct 2026 09:00:00 +0200</pubDate></item></channel></rss>')
TW = {"BI": ["bikern"], "Data": ["datakern"], "Automatisering": ["autokern"], "AI": ["aikern"]}


def lees(url, ua, timeout):
    return RSS


def item(n, dagen):
    return {"id": "i%d" % n, "titel": "bikern %d" % n, "samenvatting": "x",
            "datum": (NU.date() - timedelta(days=dagen)).isoformat(), "bron": "T", "taal": "nl",
            "url": "http://x.test/%d" % n, "categorie": "BI"}


def cfg(**extra):
    c = {"user_agent": "T/1", "trefwoorden": TW, "feeds": [{"naam": "T", "url": "http://x.test/f", "taal": "nl"}]}
    c.update(extra)
    return c


class Basis(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.pad = os.path.join(self.tmp.name, "nieuws.json")
        self.logs = []

    def tearDown(self):
        self.tmp.cleanup()

    def schrijf(self, items):
        with open(self.pad, "w", encoding="utf-8") as f:
            json.dump({"items": items}, f)

    def draai(self, c, **kw):
        return ophalen.draai(c, self.pad, controleer_robots=False, lees=lees, nu=NU, log=self.logs.append, **kw)

    def lees_items(self):
        with open(self.pad, encoding="utf-8") as f:
            return json.load(f)["items"]


class TestBewaarDagen(unittest.TestCase):
    def test_ongeldige_waarden(self):
        for w in (0, -5, "60", 60.0, True, None, []):
            with self.assertRaises(ValueError, msg=repr(w)):
                ophalen.controleer_config(cfg(bewaar_dagen=w))

    def test_geldige_waarde(self):
        ophalen.controleer_config(cfg(bewaar_dagen=1))
        ophalen.controleer_config(cfg())


class TestVangnetLeeftijd(Basis):
    def test_typo_bewaar_dagen_schrijft_niet(self):
        self.schrijf([item(i, 1) for i in range(10)] + [item(100 + i, 30) for i in range(90)])
        voor = open(self.pad, "rb").read()
        self.assertEqual(self.draai(cfg(bewaar_dagen=6)), 1)
        self.assertEqual(open(self.pad, "rb").read(), voor)
        self.assertIn("--forceer-opruimen", self.logs[-1])

    def test_forceer_schrijft_wel(self):
        self.schrijf([item(i, 1) for i in range(10)] + [item(100 + i, 30) for i in range(90)])
        self.assertEqual(self.draai(cfg(bewaar_dagen=6), forceer_opruimen=True), 0)
        self.assertEqual(len(self.lees_items()), 11)

    def test_gewone_veroudering_werkt(self):
        # 20 van 100 items vallen buiten 60 dagen: normaal, geen vangnet
        self.schrijf([item(i, 1) for i in range(80)] + [item(100 + i, 61) for i in range(20)])
        self.assertEqual(self.draai(cfg()), 0)
        self.assertEqual(len(self.lees_items()), 81)


class TestOnvolledigItem(Basis):
    def test_zonder_datum_en_null_datum_overgeslagen(self):
        a, b = item(50, 1), item(51, 1)
        del a["datum"]
        b["datum"] = None
        self.schrijf([item(i, 1) for i in range(5)] + [a, b])
        self.assertEqual(self.draai(cfg()), 0)
        self.assertEqual(len(self.lees_items()), 6)  # 5 + 1 nieuw
        waarschuwingen = [l for l in self.logs if l.startswith("WAARSCHUWING")]
        self.assertEqual(len(waarschuwingen), 2)
        self.assertIn("bikern 50", waarschuwingen[0])

    def test_zonder_id_wordt_hersteld(self):
        a = item(60, 1)
        del a["id"]
        self.schrijf([item(i, 1) for i in range(5)] + [a])
        self.assertEqual(self.draai(cfg()), 0)
        ids = [i["id"] for i in self.lees_items() if i["url"] == a["url"]]
        self.assertEqual(len(ids), 1)
        self.assertTrue(ids[0])


if __name__ == "__main__":
    unittest.main()
