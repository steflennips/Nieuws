"""Genereert de openbare, statische nieuwssite uit data/nieuws.json (alleen Python-standaardbibliotheek).

Gebruik:  python src/bouw.py [--data data/nieuws.json] [--config config/feeds.json] [--uit site]

Resultaat: een map met index.html (Overzicht), nieuws.html, bronnen.html, style.css, app.js,
favicon.svg en favicon.ico. Alle links zijn relatief, dus de site werkt ook onder
https://<account>.github.io/<repo>/. Er is geen server-code nodig. Zonder data/nieuws.json
(of zonder items) stopt het commando met een foutmelding: er wordt nooit voorbeelddata gepubliceerd.
"""
import argparse
import json
import os
import struct
import sys
from datetime import date, datetime, timedelta, timezone
from html import escape
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mix  # noqa: E402

BASIS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
STANDAARD_DATA = os.path.join(BASIS, "data", "nieuws.json")
STANDAARD_CONFIG = os.path.join(BASIS, "config", "feeds.json")
STANDAARD_UIT = os.path.join(BASIS, "site")

CATEGORIEEN = mix.CATEGORIEEN  # BI, Data, Automatisering, AI
MENU = [("index.html", "Overzicht"), ("nieuws.html", "Nieuws")]
MAANDEN = ["jan", "feb", "mrt", "apr", "mei", "jun", "jul", "aug", "sep", "okt", "nov", "dec"]
MAX_SAMENVATTING = 300

CSS = """\
:root{--donker:#1F2A44;--wit:#FFFFFF;--achtergrond:#F7F8FA;--rand:#E3E6EB;--tekst:#1F2A44;--tekst2:#5B6475;--accent:#0F766E}
*{box-sizing:border-box}
[hidden]{display:none!important}
body{margin:0;font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;background:var(--achtergrond);color:var(--tekst);line-height:1.5}
a{color:var(--accent)}
a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible{outline:2px solid var(--donker);outline-offset:2px}
header a:focus-visible{outline-color:var(--wit)}
input,button,select{font:inherit}
header{background:var(--donker);color:var(--wit)}
.wrap{max-width:1080px;margin:0 auto;padding:0 16px}
header .wrap{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:0 24px}
.logo{font-weight:700;font-size:1.1rem;padding:14px 0}
nav{display:flex;flex-wrap:wrap}
nav a{color:var(--wit);text-decoration:none;padding:14px 16px}
nav a:hover{text-decoration:underline}
nav a[aria-current=page]{background:var(--accent);font-weight:700}
main{padding:28px 0 48px}
h1{margin:0 0 16px;font-size:1.6rem;color:var(--donker)}
h2{color:var(--donker)}
.filters{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:12px;align-items:center}
.chip{padding:6px 14px;border-radius:999px;background:var(--wit);border:1px solid var(--rand);color:var(--accent);text-decoration:none;font-size:.9rem}
.chip.actief{background:var(--accent);color:var(--wit);border-color:var(--accent)}
form.zoek{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:12px}
form.zoek input[type=search]{flex:1 1 200px;min-width:0;padding:8px 12px;border:1px solid var(--rand);border-radius:6px;font-size:1rem;color:var(--tekst);background:var(--wit)}
form.zoek input::placeholder{color:var(--tekst2);opacity:1}
form.zoek button{padding:8px 16px;border:0;border-radius:6px;background:var(--accent);color:var(--wit);font-weight:600;cursor:pointer;font-size:1rem}
.aantal{color:var(--tekst2);margin:8px 0 16px}
.kaart{background:var(--wit);border:1px solid var(--rand);border-radius:8px;padding:14px 16px;margin-bottom:12px;overflow-wrap:anywhere}
.kaart h2{margin:0 0 4px;font-size:1.05rem}
.kaart p{margin:0}
.meta{color:var(--tekst2);font-size:.85rem;display:flex;flex-wrap:wrap;gap:4px 12px;margin-bottom:6px}
.tag{display:inline-block;padding:1px 10px;border-radius:999px;font-size:.8rem;font-weight:600;background:var(--achtergrond);color:var(--tekst);border:1px solid var(--rand)}
.leeg{background:var(--wit);border:1px dashed var(--rand);border-radius:8px;padding:24px;text-align:center;color:var(--tekst2)}
.intro{color:var(--tekst2);margin:0 0 20px}
.tegels{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:24px}
.tegel{display:block;background:var(--wit);border:1px solid var(--rand);border-radius:8px;padding:16px;color:var(--tekst);text-decoration:none}
.tegel:hover .label{text-decoration:underline}
.tegel .getal{display:block;font-size:2rem;font-weight:700;line-height:1.2;color:var(--donker)}
.tegel .label{color:var(--tekst2);font-size:.9rem}
.blok{background:var(--wit);border:1px solid var(--rand);border-radius:8px;padding:16px;min-width:0}
.blok h2{margin:0;font-size:1.1rem}
.blok-kop{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:baseline;gap:4px 12px;margin-bottom:8px}
.blok-kop .totaal{color:var(--tekst2);font-size:.85rem}
.lijst{list-style:none;margin:0 0 12px;padding:0}
.lijst li{padding:10px 0;border-top:1px solid var(--rand);overflow-wrap:anywhere}
.lijst a{font-weight:600}
.lijst .meta{margin:2px 0 0}
.alles{font-weight:600}
.bronnen{list-style:none;margin:0;padding:0}
.bronnen li{padding:10px 0;border-top:1px solid var(--rand);overflow-wrap:anywhere}
.bronnen li:first-child{border-top:0}
.taal{color:var(--tekst2);font-size:.85rem}
footer{border-top:1px solid var(--rand);background:var(--wit);color:var(--tekst2);font-size:.85rem;padding:16px 0}
footer p{margin:0 0 4px}
.uitgelicht{border-top:4px solid var(--donker);margin-bottom:24px}
.uitgelicht .lijst{margin-bottom:0}
.uitgelicht .lijst li:first-child{border-top:0}
.leeg-tekst{margin:0;color:var(--tekst2)}
@media (max-width:720px){.tegels{grid-template-columns:1fr}}
"""

JS = """\
/* Filteren en zoeken op nieuws.html via de URL (?categorie=AI&q=zoekterm). Zonder JavaScript zie je alle items. */
(function () {
  var CATS = @CATS@;
  var params = new URLSearchParams(window.location.search);
  var w = (params.get("categorie") || "").trim().toLowerCase();
  var cat = "";
  CATS.forEach(function (c) { if (c.toLowerCase() === w) { cat = c; } });
  var q = (params.get("q") || "").trim();
  var ql = q.toLowerCase();

  var zoekveld = document.getElementById("zoekveld");
  var verborgen = document.getElementById("zoek-categorie");
  zoekveld.value = q;
  if (cat) { verborgen.value = cat; } else { verborgen.removeAttribute("name"); }

  Array.prototype.forEach.call(document.querySelectorAll(".chip"), function (chip) {
    var c = chip.getAttribute("data-categorie");
    var p = new URLSearchParams();
    if (c) { p.set("categorie", c); }
    if (q) { p.set("q", q); }
    var s = p.toString();
    chip.setAttribute("href", "nieuws.html" + (s ? "?" + s : ""));
    var actief = (c || "") === cat;
    chip.classList.toggle("actief", actief);
    if (actief) { chip.setAttribute("aria-current", "true"); } else { chip.removeAttribute("aria-current"); }
  });

  var zichtbaar = 0;
  Array.prototype.forEach.call(document.querySelectorAll("article.kaart"), function (kaart) {
    var tekst = (kaart.querySelector("h2").textContent + " " + kaart.querySelector("p").textContent).toLowerCase();
    var toon = (!cat || kaart.getAttribute("data-categorie") === cat) && (!ql || tekst.indexOf(ql) !== -1);
    kaart.hidden = !toon;
    if (toon) { zichtbaar++; }
  });
  document.getElementById("aantal").textContent = zichtbaar + (zichtbaar === 1 ? " nieuwsitem" : " nieuwsitems");
  document.getElementById("geen-nieuws").hidden = zichtbaar !== 0;
})();
"""

FAVICON_SVG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><rect width="16" height="16" rx="3" fill="#1F2A44"/>'
               '<rect x="4" y="4" width="8" height="8" rx="1" fill="#FFFFFF"/></svg>\n')


def favicon_ico():
    """Kleine 16x16 .ico (donkerblauw met wit vlak), zodat /favicon.ico geen 404 geeft."""
    donker, wit = (0x44, 0x2A, 0x1F, 255), (255, 255, 255, 255)  # BGRA
    rijen = []
    for y in range(16):
        rijen.append(b"".join(struct.pack("4B", *(wit if 4 <= x < 12 and 4 <= y < 12 else donker)) for x in range(16)))
    pixels = b"".join(reversed(rijen))  # bottom-up
    masker = b"\x00" * (4 * 16)
    kop = struct.pack("<IiiHHIIiiII", 40, 16, 32, 1, 32, 0, len(pixels) + len(masker), 0, 0, 0, 0)
    data = kop + pixels + masker
    return struct.pack("<HHH", 0, 1, 1) + struct.pack("<BBBBHHII", 16, 16, 0, 0, 1, 32, len(data), 22) + data


# ---------- hulpfuncties ----------
def fmt_datum(iso):
    j, m, d = iso[:10].split("-")
    return "%d %s %s" % (int(d), MAANDEN[int(m) - 1], j)


def _laatste_zondag(jaar, maand):
    d = date(jaar, maand, 31)
    return d - timedelta(days=(d.weekday() + 1) % 7)


def nl_tijd(dt):
    """UTC-tijdstip -> Nederlandse tijd (CET/CEST) zonder tijdzonedatabase (werkt ook op Windows zonder tzdata)."""
    dt = dt.astimezone(timezone.utc)
    start = datetime.combine(_laatste_zondag(dt.year, 3), datetime.min.time(), timezone.utc) + timedelta(hours=1)
    einde = datetime.combine(_laatste_zondag(dt.year, 10), datetime.min.time(), timezone.utc) + timedelta(hours=1)
    return dt + timedelta(hours=2 if start <= dt < einde else 1)


def fmt_bijgewerkt(iso):
    dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    lokaal = nl_tijd(dt)
    return "%d %s %d %02d:%02d" % (lokaal.day, MAANDEN[lokaal.month - 1], lokaal.year, lokaal.hour, lokaal.minute), dt.isoformat()


def veilige_url(url):
    return isinstance(url, str) and urlparse(url).scheme in ("http", "https")


def knip(tekst, maximaal=MAX_SAMENVATTING):
    tekst = " ".join((tekst or "").split())
    return tekst if len(tekst) <= maximaal else tekst[:maximaal - 3].rstrip() + "..."


# ---------- pagina's ----------
def pagina(titel, bestand, inhoud, bijgewerkt, scripts=""):
    menu = "".join('<a href="%s"%s>%s</a>' % (href, ' aria-current="page"' if href == bestand else "", naam)
                   for href, naam in MENU)
    tekst, iso = bijgewerkt
    return """<!doctype html>
<html lang="nl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s - Deux2Qonnect</title>
<link rel="stylesheet" href="style.css">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="icon" href="favicon.ico" sizes="16x16">
</head>
<body><header><div class="wrap"><div class="logo">Deux2Qonnect</div><nav aria-label="Hoofdmenu">%s</nav></div></header>
<main><div class="wrap">%s</div></main>
<footer><div class="wrap">
<p>Laatst bijgewerkt: <time datetime="%s">%s</time></p>
<p>Koppen en samenvattingen op deze site zijn afkomstig van de genoemde bronnen; de rechten liggen bij die bronnen. Bekijk <a href="bronnen.html">alle bronnen</a>.</p>
</div></footer>%s</body></html>
""" % (escape(titel), menu, inhoud, escape(iso), escape(tekst), scripts)


def _li(n):
    return ('<li><a href="%s" target="_blank" rel="noopener noreferrer">%s</a>'
            '<div class="meta"><span class="tag">%s</span><span>%s</span><span>%s</span></div></li>'
            % (escape(n["url"]), escape(n["titel"]), escape(n["categorie"]), escape(n["bron"]), fmt_datum(n["datum"])))


def view_overzicht(items, bijgewerkt, uitgelicht=None, vaknieuws=None):
    uitgelicht = [] if uitgelicht is None else uitgelicht
    vaknieuws = items[:5] if vaknieuws is None else vaknieuws
    tegels = "".join(
        '<a class="tegel" href="nieuws.html?categorie=%s"><span class="getal" id="teller-%s">%d</span>'
        '<span class="label">%s</span></a>' % (c, c.lower(), len([i for i in items if i["categorie"] == c]), c)
        for c in CATEGORIEEN)
    if uitgelicht:
        uit = '<ul class="lijst">%s</ul>' % "".join(_li(n) for n in uitgelicht)
    else:
        uit = '<p class="leeg-tekst">Nog geen uitgelicht nieuws</p>'
    inhoud = ('<h1>Overzicht</h1><p class="intro">Het nieuwste nieuws over BI, data, automatisering en AI, '
              'elke dag bijgewerkt uit openbare bronnen.</p>'
              '<section class="blok uitgelicht" id="blok-uitgelicht"><div class="blok-kop"><h2>Uitgelicht</h2>'
              '<span class="totaal">laatste 3 dagen</span></div>%s</section>'
              '<div class="tegels">%s</div>'
              '<section class="blok" id="blok-nieuws"><div class="blok-kop"><h2>Vaknieuws</h2></div>'
              '<ul class="lijst">%s</ul>'
              '<a class="alles" href="nieuws.html">Alle %d berichten bekijken</a></section>'
              % (uit, tegels, "".join(_li(n) for n in vaknieuws), len(items)))
    return pagina("Overzicht", "index.html", inhoud, bijgewerkt)


def view_nieuws(items, bijgewerkt):
    chips = "".join('<a class="chip%s" data-categorie="%s" href="nieuws.html%s">%s</a>' % (
        " actief" if not c else "", c, "?categorie=" + c if c else "", c or "Alle") for c in [""] + CATEGORIEEN)
    kaarten = "".join(
        '<article class="kaart" data-categorie="%s">'
        '<h2><a href="%s" target="_blank" rel="noopener noreferrer">%s</a></h2>'
        '<div class="meta"><span class="tag">%s</span><span>Bron: %s</span><span>%s</span></div>'
        '<p>%s</p></article>' % (escape(n["categorie"]), escape(n["url"]), escape(n["titel"]), escape(n["categorie"]),
                                 escape(n["bron"]), fmt_datum(n["datum"]), escape(n["samenvatting"]))
        for n in items)
    inhoud = ('<h1>Nieuws</h1>'
              '<form class="zoek" method="get" action="nieuws.html" role="search">'
              '<input type="hidden" id="zoek-categorie" name="categorie" value="">'
              '<input type="search" id="zoekveld" name="q" value="" placeholder="Zoek in nieuws" aria-label="Zoeken">'
              '<button type="submit">Zoeken</button></form>'
              '<div class="filters">%s</div>'
              '<p class="aantal" id="aantal">%d %s</p>'
              '<div class="leeg" id="geen-nieuws" hidden>Geen nieuws gevonden</div>%s'
              % (chips, len(items), "nieuwsitem" if len(items) == 1 else "nieuwsitems", kaarten))
    return pagina("Nieuws", "nieuws.html", inhoud, bijgewerkt, '<script src="app.js"></script>')


BASE_SCRIPT = ("<script>(function(){var s=location.pathname.split('/')[1]||'';"
               "var b=(/[.]github[.]io$/.test(location.hostname)&&s)?'/'+s+'/':'/';"
               "document.write('<base href=\"'+b+'\">');})();</script>")


def view_404(bijgewerkt):
    """Eigen 404-pagina in huisstijl. Staat op een willekeurig pad, dus: stijl inline en een <base> via script."""
    inhoud = ('<h1>Pagina niet gevonden</h1><p class="intro">Deze pagina bestaat niet (meer). '
              'Ga terug naar het <a href="index.html">Overzicht</a> of bekijk het <a href="nieuws.html">nieuws</a>.</p>')
    html = pagina("Pagina niet gevonden", "404.html", inhoud, bijgewerkt)
    html = html.replace('<link rel="stylesheet" href="style.css">', "<style>" + CSS + "</style>")
    return html.replace("<head>", "<head>" + BASE_SCRIPT, 1)


def view_bronnen(bronnen, bijgewerkt):
    def regel(b):
        taal = ' <span class="taal">(%s)</span>' % ("Nederlands" if b["taal"] == "nl" else "Engels") if b["taal"] else ""
        if b["link"]:
            return ('<li><a href="%s" target="_blank" rel="noopener noreferrer">%s</a>%s</li>'
                    % (escape(b["link"]), escape(b["naam"]), taal))
        return "<li>%s%s</li>" % (escape(b["naam"]), taal)  # bron buiten de config: alleen de naam, geen link
    li = "".join(regel(b) for b in bronnen)
    inhoud = ('<h1>Bronnen</h1><p class="intro">Alle koppen en samenvattingen op deze site komen uit de openbare feeds van '
              'onderstaande bronnen (ook bronnen waarvan nog berichten op de site staan). Elke titel leidt naar het originele artikel; de rechten liggen bij de bronnen.</p>'
              '<div class="blok"><ul class="bronnen">%s</ul></div>' % li)
    return pagina("Bronnen", "bronnen.html", inhoud, bijgewerkt)


# ---------- bouwen ----------
def laad_items(data, meld=None):
    """Geldige items, nieuwste eerst, AI beperkt. Een item met ongeldige datum wordt overgeslagen met een melding."""
    items = []
    for i in data.get("items", []):
        if not (isinstance(i, dict) and i.get("titel") and veilige_url(i.get("url")) and i.get("categorie") in CATEGORIEEN
                and i.get("bron") and i.get("datum")):
            continue
        try:
            date.fromisoformat(str(i["datum"])[:10])
        except ValueError:
            (meld or (lambda t: print(t, file=sys.stderr)))(
                "WAARSCHUWING: item met ongeldige datum %r overgeslagen: %s (%s)" % (i["datum"], i["titel"][:80], i["url"]))
            continue
        items.append({"titel": i["titel"], "url": i["url"], "categorie": i["categorie"], "bron": i["bron"],
                      "datum": str(i["datum"])[:10], "samenvatting": knip(i.get("samenvatting", ""))})
    items.sort(key=lambda i: i["datum"], reverse=True)
    return items


def bouw(data_pad, config_pad, uit, vandaag=None):
    """Geeft (aantal items, aantal bronnen). Gooit ValueError met een nette melding bij ontbrekende data."""
    try:
        with open(data_pad, encoding="utf-8-sig") as f:
            data = json.load(f)
    except FileNotFoundError:
        raise ValueError("%s ontbreekt. Draai eerst: python src/ophalen.py" % data_pad)
    except OSError:
        raise ValueError("%s kan niet gelezen worden. Controleer het pad en de rechten." % data_pad)
    except ValueError:
        raise ValueError("%s is geen geldig nieuwsbestand (geen leesbare JSON). Draai opnieuw: python src/ophalen.py" % data_pad)
    alle = laad_items(data if isinstance(data, dict) else {})
    if not alle:
        raise ValueError("%s bevat geen nieuwsitems; er wordt niets gebouwd." % data_pad)
    items = mix.beperk_ai(alle)  # AI hooguit 40% van de getoonde items
    if not items:
        raise ValueError("alle %d items in %s zijn AI en door het AI-plafond (maximaal 40%% AI) blijft niets over; "
                         "er wordt niets gebouwd. Haal eerst ook BI-, Data- of Automatisering-nieuws op." % (len(alle), data_pad))
    try:
        with open(config_pad, encoding="utf-8") as f:
            config = json.load(f)
            feeds = config["feeds"]
    except (OSError, ValueError, KeyError) as e:
        raise ValueError("configuratiebestand niet te lezen: %s (%s)" % (config_pad, e))
    bronnen = []
    for fd in feeds:
        u = urlparse(fd["url"])
        bronnen.append({"naam": fd["naam"], "taal": fd.get("taal", ""), "link": "%s://%s/" % (u.scheme, u.netloc)})
    bekend = {b["naam"] for b in bronnen}
    for naam in sorted({i["bron"] for i in items}):
        if naam not in bekend:
            # Bron buiten de config: alleen een link als alle artikelen van die bron op dezelfde site staan (https).
            sites = {"%s://%s/" % (urlparse(i["url"]).scheme, urlparse(i["url"]).netloc) for i in items if i["bron"] == naam}
            link = sites.pop() if len(sites) == 1 else ""
            if not link.startswith("https://"):
                link = ""
            bronnen.append({"naam": naam, "taal": "", "link": link})
            bekend.add(naam)
    uitg = mix.uitgelicht(items, config, vandaag)
    bijgewerkt = fmt_bijgewerkt(data.get("bijgewerkt") or datetime.now(timezone.utc).isoformat())
    os.makedirs(uit, exist_ok=True)
    bestanden = {
        "index.html": view_overzicht(items, bijgewerkt, uitg, mix.vaknieuws(items, uitg, config)), "nieuws.html": view_nieuws(items, bijgewerkt),
        "bronnen.html": view_bronnen(bronnen, bijgewerkt), "404.html": view_404(bijgewerkt), "style.css": CSS, "app.js": JS.replace("@CATS@", json.dumps(CATEGORIEEN)),
        "favicon.svg": FAVICON_SVG, ".nojekyll": "",
    }
    for naam, inhoud in bestanden.items():
        with open(os.path.join(uit, naam), "w", encoding="utf-8", newline="\n") as f:
            f.write(inhoud)
    with open(os.path.join(uit, "favicon.ico"), "wb") as f:
        f.write(favicon_ico())
    return len(items), len(bronnen)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Genereer de statische nieuwssite.")
    ap.add_argument("--data", default=STANDAARD_DATA)
    ap.add_argument("--config", default=STANDAARD_CONFIG)
    ap.add_argument("--uit", default=STANDAARD_UIT)
    ap.add_argument("--vandaag", help="peildatum JJJJ-MM-DD voor Uitgelicht (standaard: vandaag; voor tests)")
    a = ap.parse_args(argv)
    try:
        try:
            vandaag = date.fromisoformat(a.vandaag) if a.vandaag else None
        except ValueError:
            raise ValueError("ongeldige peildatum %r bij --vandaag; gebruik het formaat JJJJ-MM-DD (bijvoorbeeld 2026-10-09)" % a.vandaag)
        n, b = bouw(a.data, a.config, a.uit, vandaag)
    except ValueError as e:
        print("FOUT: %s" % e, file=sys.stderr)
        return 1
    print("Site gebouwd in %s: %d nieuwsitems, %d bronnen." % (os.path.abspath(a.uit), n, b))
    return 0


if __name__ == "__main__":
    sys.exit(main())
