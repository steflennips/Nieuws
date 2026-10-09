"""Acceptatietests iteratie 5 (online zetten voorbereiden), zonder GitHub-account, internet of git-schrijfacties.

Dekt wat lokaal te controleren is:
- .gitignore bevat de veiligheidsregels; src/veilig_check.py eindigt met exitcode 0 (alleen-lezen).
- Workflow (tekstcontrole, geen YAML-bibliotheek nodig): cron rond 06:00 NL, handmatig starten, minimale rechten,
  geen eigen geheimen, volgorde ophalen -> bouwen -> publiceren, data alleen committen bij wijziging.
- Verse checkout zonder of met leeg data/nieuws.json: geen crash, en er wordt geen voorbeelddata gepubliceerd.
- Subpad /<repo>/: alle interne links van de gebouwde site blijven onder het repo-pad en werken.
- README (stappen A-E): de commando's en namen kloppen; geen lokaal pad of persoonlijk account.

NIET GETEST hier (vereist GitHub): US-013 c1 (site bereikbaar op github.io) en c3 (Laatst bijgewerkt op de live site).
Het uitvoeren van git init/commit/push is bewust niet gedaan.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import urljoin, urlparse

import hulp_statisch as h
import hulp_feeds as hf

sys.dont_write_bytecode = True
SRC = os.path.join(h.ROOT, "src")
sys.path.insert(0, SRC)
# (iteratie 7: src/data.py is verwijderd; de voorbeelddata-controle is generiek: geen "Voorbeeld"-markering op de site)

WORKFLOW = os.path.join(h.ROOT, ".github", "workflows", "nieuws.yml")
GITIGNORE = os.path.join(h.ROOT, ".gitignore")
README = os.path.join(h.ROOT, "README.md")
VEILIG = os.path.join(SRC, "veilig_check.py")


def lees_tekst(pad):
    with open(pad, encoding="utf-8") as f:
        return f.read()


WF = lees_tekst(WORKFLOW) if os.path.exists(WORKFLOW) else ""
RM = lees_tekst(README)


class TestIT5Gitignore(unittest.TestCase):
    def test_IT5_gitignore_bevat_veiligheidsregels(self):
        regels = {r.strip() for r in lees_tekst(GITIGNORE).splitlines() if r.strip() and not r.startswith("#")}
        verplicht = ["site/", "__pycache__/", ".env", "*.log", "NTUSER*", ".claude.json*", ".claude/settings.local.json",
                     "*.pem", "*.key", "*.pfx", "id_rsa*", ".npmrc", ".netrc"]
        self.assertEqual([v for v in verplicht if v not in regels], [], "ontbrekende regels in .gitignore")

    def test_IT5_veilig_check_eindigt_met_exitcode_0(self):
        r = subprocess.run([sys.executable, "-B", VEILIG], cwd=h.ROOT, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", env=hf.omgeving(), timeout=180)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("OK: geen geheimen, e-mailadressen, lokale paden of verdachte bestanden gevonden.", r.stdout)


class TestIT5Workflow(unittest.TestCase):
    def test_IT5_c2_cron_dagelijks_0400_utc_is_0600_nl(self):
        self.assertIn('cron: "0 4 * * *"', WF)

    def test_IT5_c2_handmatig_starten_mogelijk(self):
        self.assertIn("workflow_dispatch:", WF)

    def test_IT5_rechten_zijn_minimaal(self):
        paren = set(re.findall(r"^\s+([a-z-]+):\s+(read|write|none)\b", WF, re.M))
        self.assertEqual(paren, {("contents", "write"), ("pages", "write"), ("id-token", "write")}, paren)
        self.assertNotIn("write-all", WF)

    def test_IT5_c4_geen_eigen_geheimen_in_workflow(self):
        self.assertNotIn("secrets.", WF, "de job gebruikt geen eigen sleutels (alleen het automatische GITHUB_TOKEN)")

    def test_IT5_volgorde_ophalen_bouwen_publiceren(self):
        i_op = WF.index("python src/ophalen.py")
        i_bo = WF.index("python src/bouw.py")
        i_up = WF.index("upload-pages-artifact")
        i_de = WF.index("deploy-pages")
        self.assertLess(i_op, i_bo)
        self.assertLess(i_bo, i_up)
        self.assertLess(i_up, i_de)
        self.assertIn("needs: bouwen", WF, "publiceren mag pas na een geslaagde bouw")
        self.assertNotIn("if: always()", WF, "bouwen mag niet doorlopen na een mislukt ophalen")
        self.assertNotIn("continue-on-error", WF, "een mislukte stap mag niet genegeerd worden")

    def test_IT5_pad_van_artefact_is_site_en_data_alleen_bij_wijziging(self):
        self.assertIn("path: site", WF)
        self.assertIn("git status --porcelain data/nieuws.json", WF)

    def test_IT5_naam_van_workflow_staat_in_readme(self):
        self.assertIn("name: Nieuws verversen en publiceren", WF)
        self.assertIn("Actions > Nieuws verversen en publiceren > Run workflow", RM)


class TestIT5VerseCheckout(unittest.TestCase):
    """Simuleert de eerste run: geen data/nieuws.json (of een leeg bestand). Alles in een tijdelijke map."""

    def setUp(self):
        self.tmp = h.nieuwe_tijdelijke_map(prefix="it5-")
        self.pad = os.path.join(self.tmp, "data", "nieuws.json")
        os.makedirs(os.path.dirname(self.pad))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _cfg_gesloten_poort(self):
        poort = hf.vrije_poort()
        return hf.schrijf_config(os.path.join(self.tmp, "cfg.json"),
                                 [{"naam": "Onbereikbaar", "url": "http://127.0.0.1:%d/feed.xml" % poort, "taal": "nl"}])

    def test_IT5_verse_checkout_zonder_data_geen_crash_en_niets_gepubliceerd(self):
        r = hf.run_ophalen(self._cfg_gesloten_poort(), self.pad)
        self.assertEqual(r.returncode, 1, "alle feeds mislukt: exitcode 1 (de job faalt zichtbaar)")
        self.assertFalse(os.path.exists(self.pad), "er is een databestand gemaakt terwijl alle feeds faalden")
        self.assertNotIn("Traceback", r.stdout + r.stderr)
        site = os.path.join(self.tmp, "site")
        rc, out, err = h.bouw(site, data=self.pad)
        self.assertEqual(rc, 1)
        self.assertNotIn("Traceback", err)
        self.assertFalse(os.path.exists(os.path.join(site, "index.html")), "er is een site gebouwd zonder data")

    def test_IT5_leeg_databestand_geen_crash_en_geen_publicatie(self):
        open(self.pad, "w").close()
        r = hf.run_ophalen(self._cfg_gesloten_poort(), self.pad)
        self.assertEqual(r.returncode, 1)
        self.assertNotIn("Traceback", r.stdout + r.stderr)
        self.assertEqual(os.path.getsize(self.pad), 0, "het lege bestand is aangepast terwijl alle feeds faalden")
        site = os.path.join(self.tmp, "site")
        rc, out, err = h.bouw(site, data=self.pad)
        self.assertEqual(rc, 1)
        self.assertNotIn("Traceback", err)
        self.assertFalse(os.path.exists(os.path.join(site, "index.html")))

    def test_IT5_ontbrekend_bestand_met_werkende_feed_publiceert_alleen_echte_items(self):
        with hf.FeedServer({"/rss.xml": {"body": hf.rss_feed}}) as srv:
            cfg = hf.schrijf_config(os.path.join(self.tmp, "cfg.json"),
                                    [{"naam": "Testfeed RSS", "url": srv.base + "/rss.xml", "taal": "nl"}])
            r = hf.run_ophalen(cfg, self.pad)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertTrue(os.path.exists(self.pad))
        site = os.path.join(self.tmp, "site")
        rc, out, err = h.bouw(site, data=self.pad, vandaag=None)
        self.assertEqual(rc, 0, err)
        alles = " ".join(h.lees(os.path.join(site, n)) for n in h.html_bestanden(site))
        self.assertNotIn("Voorbeeld", alles, "voorbeeldmarkering gepubliceerd (voorbeelddata uit de oude app?)")
        self.assertIn("Datawarehouse wordt goedkoper", alles, "het echte item moet op de site staan")


class TestIT5Subpad(unittest.TestCase):
    """Simuleert https://<account>.github.io/<repo>/: de site staat in een submap en de server serveert vanaf de ouder."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = h.nieuwe_tijdelijke_map(prefix="it5-sub-")
        cls.ouder = os.path.join(cls.tmp, "ouder")
        cls.repo = "nieuws-repo"
        os.makedirs(cls.ouder)
        data = h.schrijf_fixture_data(cls.tmp)
        rc, out, err = h.bouw(os.path.join(cls.ouder, cls.repo), data=data, vandaag=h.FIXTURE_VANDAAG)
        assert rc == 0, err
        cls.srv = h.StatischeServer(cls.ouder).__enter__()

    @classmethod
    def tearDownClass(cls):
        cls.srv.__exit__(None, None, None)
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_IT5_subpad_pagina_en_assets_laden_onder_repo_pad(self):
        for pad in ["/%s/" % self.repo, "/%s/index.html" % self.repo, "/%s/nieuws.html" % self.repo,
                    "/%s/bronnen.html" % self.repo, "/%s/style.css" % self.repo, "/%s/app.js" % self.repo,
                    "/%s/favicon.ico" % self.repo, "/%s/favicon.svg" % self.repo]:
            self.assertEqual(self.srv.get(pad)[0], 200, pad)

    def test_IT5_subpad_alle_interne_links_blijven_onder_repo_en_bestaan(self):
        basis = "https://account.github.io/%s/" % self.repo
        for naam in h.html_bestanden(os.path.join(self.ouder, self.repo)):
            p = h.lees(os.path.join(self.ouder, self.repo, naam))
            for waarde in re.findall(r'<(?:a|link|script)\b[^>]*?\b(?:href|src)="([^"]*)"', p):
                if waarde.startswith(("http://", "https://")):
                    continue
                url = urljoin(basis + naam, h.htmllib.unescape(waarde))
                pad = urlparse(url).path
                self.assertTrue(pad.startswith("/%s/" % self.repo), "link %r in %s ontsnapt aan het repo-pad" % (waarde, naam))
                lokaal = pad[len("/%s/" % self.repo):] or "index.html"
                self.assertEqual(self.srv.get("/%s/%s" % (self.repo, lokaal))[0], 200,
                                 "link %r in %s geeft geen 200" % (waarde, naam))

    def test_IT5_subpad_zoekfilter_in_url_werkt_onder_repo_pad(self):
        self.assertEqual(self.srv.get("/%s/nieuws.html?categorie=ai" % self.repo)[0], 200)


class TestIT5Readme(unittest.TestCase):
    def test_IT5_readme_stappen_A_tot_E_en_commando_s_aanwezig(self):
        for stap in ["Stap A", "Stap B", "Stap C", "Stap D", "Stap E"]:
            self.assertIn(stap, RM, stap)
        for cmd in ["python src/veilig_check.py", "git rev-parse --show-toplevel", "git remote -v", "git init",
                    "git add .", 'git commit -m "Eerste versie"', "git branch -M main",
                    "git remote add origin https://github.com/<accountnaam>/<repo>.git", "git push -u origin main",
                    "Source: GitHub Actions", "Read and write permissions"]:
            self.assertIn(cmd, RM, "README mist: %s" % cmd)

    def test_IT5_readme_toplevel_controle_met_stopinstructie(self):
        self.assertIn("eindigt op `POC app`", RM)
        self.assertIn("stop", RM.lower())

    def test_IT5_readme_veilig_check_eindregel_klopt_met_script(self):
        self.assertIn("OK: geen geheimen, e-mailadressen, lokale paden of verdachte bestanden gevonden.", RM)

    def test_IT5_readme_geen_lokaal_pad_of_persoonlijk_account(self):
        # Een losse letter gevolgd door ":/" of ":\" (niet "https://"); de veiligheidscontrole (veilig_check) doet de rest.
        verboden = [r"(?<![A-Za-z])[A-Za-z]:\\", r"(?<![A-Za-z])[A-Za-z]:/(?!/)", r"/Users/", r"steflennips",
                    r"deux2qonnect"]
        gevonden = [v for v in verboden if re.search(v, RM, re.I)]
        self.assertEqual(gevonden, [], "README bevat een lokaal pad of persoonlijk account")


if __name__ == "__main__":
    unittest.main()
