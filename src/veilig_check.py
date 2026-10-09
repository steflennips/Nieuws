"""Controle vooraf op wat je openbaar zet: geheimen, e-mailadressen, lokale paden, verdachte bestandsnamen.

Gebruik (vanuit de projectmap, VOOR de eerste push en daarna zo vaak je wilt):
    python src/veilig_check.py

Welke bestanden worden gecontroleerd:
- Staat de projectmap zelf als git-repo (git rev-parse --show-toplevel wijst naar deze map), dan precies de bestanden
  die git zou meenemen (`git ls-files --cached --others --exclude-standard`), dus rekening houdend met .gitignore.
- Anders (nog geen eigen repo) loopt het alle bestanden in de map door en slaat de mappen over die in .gitignore staan.
Exitcode 0 = niets gevonden, 1 = bevindingen (zie uitvoer), 2 = kon niet uitvoeren. Alleen stdlib, geen internet.
"""
import fnmatch
import os
import re
import subprocess
import sys

BASIS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Bestanden die de zoekpatronen zelf (of bewust valse voorbeeldsleutels voor een test) bevatten.
EIGEN_BESTANDEN = {"src/veilig_check.py", "tests/test_online.py", "tests/test_bouw.py",
                   "tests/acceptance/test_US013_workflow.py"}
# Het enige e-mailadres dat mag: het officiele noreply-adres van de GitHub-bot.
TOEGESTAAN_EMAIL = re.compile(r"^\d+\+github-actions\[bot\]@users\.noreply\.github\.com$|@users\.noreply\.github\.com$")

VERDACHTE_NAMEN = ["NTUSER*", "ntuser*", ".claude.json*", ".env", ".env.*", "*.pem", "*.key", "*.pfx", "*.p12",
                   "id_rsa*", "id_ed25519*", ".gitconfig", "*.pyc", "*.log", "credentials*", ".npmrc", ".netrc"]

PATRONEN = {
    "GitHub-token": r"gh[pousr]_[A-Za-z0-9]{36,}",
    "GitHub fine-grained token": r"github" r"_pat_[A-Za-z0-9_]{20,}",
    "AWS-sleutel": r"AKIA[0-9A-Z]{16}",
    "OpenAI/Anthropic-achtige sleutel": r"(?<![A-Za-z0-9_/-])sk-[A-Za-z0-9_-]{20,}",
    "Slack-token": r"xox[abprs]-[A-Za-z0-9-]{10,}",
    "private sleutel": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "wachtwoord/sleutel in toekenning": (r"(?i)\b(password|passwd|wachtwoord|api[_-]?key|client_secret|access[_-]?token|"
                                         r"auth[_-]?token|secret)\b\s*[:=]\s*['\"]?[A-Za-z0-9/+_.-]{8,}"),
    "geheim in URL-parameter": r"[?&](token|apikey|api_key|sig|signature|auth|secret)=[^&\s\"']{8,}",
    "lokaal pad (Windows-gebruikersmap)": r"(?i)\b[a-z]:[\\/]+Users[\\/]",
    "lokaal pad (Unix-thuismap)": r"(?<![A-Za-z0-9.])/(Users|home)/[A-Za-z0-9._-]+/",
    "OneDrive-pad": r"OneDrive",
}
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")
GENEGEERD_ALTIJD = {".git", "__pycache__", "node_modules", ".venv"}


def _git(args):
    return subprocess.run(["git"] + args, cwd=BASIS, capture_output=True, text=True, encoding="utf-8", errors="replace")


def git_toplevel():
    try:
        r = _git(["rev-parse", "--show-toplevel"])
    except OSError:
        return None
    return r.stdout.strip() if r.returncode == 0 else None


def _zelfde_map(a, b):
    return os.path.normcase(os.path.realpath(a)) == os.path.normcase(os.path.realpath(b))


def _lees_gitignore():
    pats = []
    try:
        with open(os.path.join(BASIS, ".gitignore"), encoding="utf-8") as f:
            for r in f:
                r = r.strip()
                if r and not r.startswith("#") and not r.startswith("!"):
                    pats.append(r)
    except OSError:
        pass
    return pats


def genegeerd(rel, pats):
    delen = rel.split("/")
    for p in pats:
        dir_only = p.endswith("/")
        q = p.strip("/")
        if "/" in q:  # pad ten opzichte van de projectmap
            if fnmatch.fnmatch(rel, q) or any(fnmatch.fnmatch("/".join(delen[:i]), q) for i in range(1, len(delen))):
                return True
        else:
            namen = delen[:-1] if dir_only else delen
            if any(fnmatch.fnmatch(n, q) for n in namen):
                return True
    return False


def te_pushen_bestanden():
    """Geeft (lijst relatieve paden met /, bron-omschrijving)."""
    top = git_toplevel()
    if top and _zelfde_map(top, BASIS):
        r = _git(["ls-files", "--cached", "--others", "--exclude-standard", "-z"])
        if r.returncode == 0:
            namen = [n for n in r.stdout.split("\0") if n and os.path.isfile(os.path.join(BASIS, n))]
            return sorted(namen), "git-repo in de projectmap (volgens .gitignore)"
    pats = _lees_gitignore()
    uit = []
    for dirpad, mappen, bestanden in os.walk(BASIS):
        mappen[:] = [m for m in mappen if m not in GENEGEERD_ALTIJD]
        for n in bestanden:
            rel = os.path.relpath(os.path.join(dirpad, n), BASIS).replace(os.sep, "/")
            if not genegeerd(rel, pats):
                uit.append(rel)
    return sorted(uit), "projectmap doorlopen met .gitignore (nog geen eigen git-repo hier; git zou %s)" % (
        "de map " + top if top else "niets") + " gebruiken"


def scan_tekst(tekst):
    """Geeft lijst (regelnummer, soort) voor een stuk tekst."""
    uit = []
    for naam, p in PATRONEN.items():
        for m in re.finditer(p, tekst):
            uit.append((tekst.count("\n", 0, m.start()) + 1, naam))
    for m in EMAIL.finditer(tekst):
        if not TOEGESTAAN_EMAIL.search(m.group(0)):
            uit.append((tekst.count("\n", 0, m.start()) + 1, "e-mailadres"))
    return uit


def controleer(bestanden):
    bevindingen = []
    for rel in bestanden:
        naam = rel.rsplit("/", 1)[-1]
        if any(fnmatch.fnmatch(naam, v) for v in VERDACHTE_NAMEN):
            bevindingen.append((rel, 0, "verdachte bestandsnaam"))
            continue
        if rel in EIGEN_BESTANDEN:
            continue
        pad = os.path.join(BASIS, rel)
        try:
            with open(pad, "rb") as f:
                ruw = f.read()
        except OSError:
            continue
        if b"\0" in ruw[:4096]:
            continue  # binair (bijv. favicon.ico)
        for regel, soort in scan_tekst(ruw.decode("utf-8", errors="ignore")):
            bevindingen.append((rel, regel, soort))
    return bevindingen


def main():
    try:
        bestanden, bron = te_pushen_bestanden()
    except Exception as e:  # noqa: BLE001
        print("FOUT: kon de bestandenlijst niet bepalen (%s)" % e, file=sys.stderr)
        return 2
    print("Gecontroleerd: %d bestanden, bron: %s" % (len(bestanden), bron))
    b = controleer(bestanden)
    if not b:
        print("OK: geen geheimen, e-mailadressen, lokale paden of verdachte bestanden gevonden.")
        return 0
    for rel, regel, soort in b:
        print("GEVONDEN  %s%s  %s" % (rel, ":%d" % regel if regel else "", soort))
    print("NIET VEILIG: %d bevinding(en). Los ze op voordat je pusht." % len(b))
    return 1


if __name__ == "__main__":
    sys.exit(main())
