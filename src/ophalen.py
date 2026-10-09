"""Nieuwsfeeds ophalen, categoriseren en opslaan (alleen Python-standaardbibliotheek).

Gebruik:  python src/ophalen.py [--config config/feeds.json] [--uitvoer data/nieuws.json]

Per feed staat in de uitvoer "OK" of "FOUT" met korte reden. Exitcode 0 als minstens
een feed slaagde, anders 1 (het bestaande JSON-bestand blijft dan ongewijzigd).
"""
import argparse
import gzip
import hashlib
import html
import json
import os
import re
import sys
import urllib.error
import urllib.request
import urllib.robotparser
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from urllib.parse import urlparse

BASIS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
STANDAARD_CONFIG = os.path.join(BASIS, "config", "feeds.json")
STANDAARD_UITVOER = os.path.join(BASIS, "data", "nieuws.json")
VOLGORDE_GELIJKSPEL = ["BI", "Data", "Automatisering", "AI"]
MAX_BYTES = 8 * 1024 * 1024


class FeedFout(Exception):
    """Fout bij een hele feed (korte reden voor de uitvoer)."""


# ---------- tekst ----------
class _Tekst(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.delen, self.negeer = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.negeer += 1
        elif tag in ("p", "br", "div", "li"):
            self.delen.append(" ")

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self.negeer:
            self.negeer -= 1

    def handle_data(self, data):
        if not self.negeer:
            self.delen.append(data)


def platte_tekst(raw, maximaal=300):
    """HTML -> platte tekst, samengevouwen spaties, afgekapt op 'maximaal' tekens (incl. '...')."""
    p = _Tekst()
    try:
        p.feed(raw or "")
        p.close()
        tekst = "".join(p.delen)
    except Exception:
        tekst = html.unescape(re.sub(r"<[^>]*>", " ", raw or ""))
    tekst = re.sub(r"[­​‌‍﻿]", "", tekst)  # zachte koppeltekens e.d.
    tekst = re.sub(r"\s+", " ", tekst).strip()
    if len(tekst) > maximaal:
        tekst = tekst[:maximaal - 3].rstrip() + "..."
    return tekst


# ---------- categorie ----------
def _patroon(woord):
    """Hele woorden, hoofdletterongevoelig. Eindigt het trefwoord op '*', dan telt een woord dat ermee begint."""
    if woord.startswith("re:"):  # reguliere expressie op de kleine-letterstekst (voor patronen als "nog vier weken tot")
        return re.compile(woord[3:], re.IGNORECASE)
    prefix = woord.endswith("*")
    kern = re.escape(woord.rstrip("*").casefold())
    return re.compile(r"(?<!\w)" + kern + (r"\w*" if prefix else r"(?!\w)"))


class Matchers(dict):
    """Per categorie een lijst patronen (dict), plus de uitsluitingspatronen in .uitsluit."""
    uitsluit = ()


def maak_matchers(trefwoorden, uitsluitingen=None):
    m = Matchers({cat: [_patroon(w) for w in woorden] for cat, woorden in trefwoorden.items()})
    m.uitsluit = tuple(_patroon(w) for w in (uitsluitingen or []))
    return m


def categoriseer(titel, samenvatting, matchers):
    """Categorie met de meeste treffers; gelijkspel: BI, Data, Automatisering, AI. Geen treffer: None.
    Tekst die onder een uitsluitingsterm valt (bijv. "Data Master") telt niet mee.
    AI telt alleen met een AI-woord in de titel (een AI-woord in de samenvatting telt niet)."""
    def schoon(t):
        t = (t or "").casefold()
        for u in getattr(matchers, "uitsluit", ()):
            t = u.sub(" ", t)
        return t
    t_titel = schoon(titel)
    t_alles = schoon("%s %s" % (titel or "", samenvatting or ""))
    score = {cat: sum(len(p.findall(t_titel if cat == "AI" else t_alles)) for p in pats)
             for cat, pats in matchers.items()}
    beste = max(score.values(), default=0)
    if beste == 0:
        return None
    kandidaten = [c for c, s in score.items() if s == beste]
    kandidaten.sort(key=lambda c: VOLGORDE_GELIJKSPEL.index(c) if c in VOLGORDE_GELIJKSPEL else 99)
    return kandidaten[0]


# ---------- kwaliteitsfilter (US-017) ----------
class Weigerlijst:
    """Weigertermen in de titel, en promotietermen die ook in de samenvatting tellen (hele woorden, hoofdletterongevoelig)."""
    def __init__(self, titel=(), samenvatting=(), uitzonderingen=()):
        self.titel = tuple(_patroon(w) for w in titel)
        self.samenvatting = tuple(_patroon(w) for w in samenvatting)
        self.uitzonderingen = tuple(_patroon(w) for w in uitzonderingen)

    def _schoon(self, tekst):
        """Tekst onder een uitzondering (bijv. "operational review") telt niet als weigerterm."""
        t = (tekst or "").casefold()
        for u in self.uitzonderingen:
            t = u.sub(" ", t)
        return t

    def reden(self, titel, samenvatting):
        """De term die tot weigeren leidt, of None."""
        t = self._schoon(titel)
        for p in self.titel:
            if p.search(t):
                return p.pattern
        s = self._schoon(samenvatting)
        for p in self.samenvatting:
            if p.search(s):
                return p.pattern
        return None


def maak_weigerlijst(cfg):
    sam = cfg.get("weigertermen_samenvatting", [])
    # Promotietermen (sponsored e.d.) gelden in titel en samenvatting; de rest alleen in de titel.
    return Weigerlijst(list(cfg.get("weigertermen", [])) + list(sam), sam, cfg.get("weiger_uitzonderingen", []))


# ---------- parsen ----------
def _lokaal(tag):
    return tag.rsplit("}", 1)[-1] if isinstance(tag, str) else ""


def _kind(el, naam):
    for k in el:
        if _lokaal(k.tag) == naam:
            return k
    return None


def _tekst_van(el, *namen):
    for n in namen:
        k = _kind(el, n)
        if k is not None:
            t = "".join(k.itertext()).strip()
            if t:
                return t
    return ""


def _datum(tekst):
    if not tekst:
        return None
    tekst = tekst.strip()
    try:
        d = parsedate_to_datetime(tekst)
    except (TypeError, ValueError, IndexError):
        d = None
    if d is None:
        try:
            d = datetime.fromisoformat(tekst.replace("Z", "+00:00"))
        except ValueError:
            return None
    if d.tzinfo is not None:
        d = d.astimezone(timezone.utc)
    return d.date()


def parse_feed(inhoud):
    """Bytes -> lijst ruwe items {titel, link, samenvatting_html, datum}. Gooit FeedFout bij een ongeldige feed."""
    kop = inhoud[:4096].lower()
    if b"<!doctype html" in kop or b"<html" in kop:
        raise FeedFout("geen feed (HTML-pagina ontvangen)")
    if b"<!entity" in inhoud[:65536].lower():
        raise FeedFout("onveilige XML (entity-declaratie)")
    try:
        root = ET.fromstring(inhoud)
    except ET.ParseError as e:
        raise FeedFout("ongeldige XML (%s)" % e)
    items = []
    for el in root.iter():
        soort = _lokaal(el.tag)
        if soort == "item":
            link = _tekst_van(el, "link")
            samen = _tekst_van(el, "description", "encoded")
            d = _datum(_tekst_van(el, "pubDate", "date"))
        elif soort == "entry":
            link = ""
            for k in el:
                if _lokaal(k.tag) == "link" and k.get("href") and k.get("rel", "alternate") == "alternate":
                    link = k.get("href").strip()
                    break
            samen = _tekst_van(el, "summary", "content")
            d = _datum(_tekst_van(el, "published", "updated"))
        else:
            continue
        items.append({"titel": _tekst_van(el, "title"), "link": link, "samenvatting_html": samen, "datum": d})
    if not items and _lokaal(root.tag) not in ("rss", "feed", "RDF"):
        raise FeedFout("onbekend feedformaat")
    return items


def verwerk_items(ruw, feed, matchers, vandaag, max_samenvatting=300, weiger=None, geweigerd=None, geweigerd_links=None):
    """Ruwe items -> (opgeslagen items, aantal zonder titel/link, aantal zonder categorie).
    Geweigerde items (kwaliteitsfilter) komen niet in de uitvoer; hun titels worden aan de lijst 'geweigerd' toegevoegd."""
    uit, zonder_titel, zonder_cat = [], 0, 0
    for r in ruw:
        try:
            titel = platte_tekst(r["titel"], 10 ** 6)
            link = (r["link"] or "").strip()
            if not titel or urlparse(link).scheme not in ("http", "https"):
                zonder_titel += 1
                continue
            samen = platte_tekst(r["samenvatting_html"], max_samenvatting)
            if weiger is not None and weiger.reden(titel, samen):
                if geweigerd is not None:
                    geweigerd.append(titel)
                    if geweigerd_links is not None:
                        geweigerd_links.append(link)
                continue
            cat = categoriseer(titel, samen, matchers)
            if cat is None:
                zonder_cat += 1
                continue
            d = r["datum"]
            if d is None or d > vandaag + timedelta(days=1):
                d = vandaag
            uit.append({"id": hashlib.sha1(link.encode("utf-8")).hexdigest()[:12], "titel": titel,
                        "categorie": cat, "bron": feed["naam"], "taal": feed.get("taal", ""),
                        "datum": d.isoformat(), "samenvatting": samen, "url": link})
        except Exception:
            zonder_titel += 1
    return uit, zonder_titel, zonder_cat


# ---------- ophalen ----------
def _lees(url, ua, timeout):
    req = urllib.request.Request(url, headers={
        "User-Agent": ua, "Accept-Encoding": "gzip",
        "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml, */*"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read(MAX_BYTES + 1)
        if r.headers.get("Content-Encoding") == "gzip" or data[:2] == b"\x1f\x8b":
            data = gzip.decompress(data)
    if len(data) > MAX_BYTES:
        raise FeedFout("feed te groot")
    return data


def robots_toegestaan(url, ua, timeout, lees=_lees):
    """True als robots.txt het ophalen toestaat (geen of onbereikbare robots.txt telt als toegestaan)."""
    u = urlparse(url)
    rp = urllib.robotparser.RobotFileParser()
    try:
        regels = lees("%s://%s/robots.txt" % (u.scheme, u.netloc), ua, timeout).decode("utf-8", "replace")
    except Exception:
        return True
    rp.parse(regels.splitlines())
    return rp.can_fetch(ua, url)


def haal_feed(feed, cfg, controleer_robots=True, lees=_lees):
    ua, timeout = cfg["user_agent"], cfg.get("timeout_seconden", 15)
    if controleer_robots and not robots_toegestaan(feed["url"], ua, timeout, lees):
        raise FeedFout("niet toegestaan volgens robots.txt")
    try:
        return lees(feed["url"], ua, timeout)
    except FeedFout:
        raise
    except urllib.error.HTTPError as e:
        raise FeedFout("HTTP %s" % e.code)
    except Exception as e:
        reden = getattr(e, "reason", e)
        raise FeedFout("niet bereikbaar of time-out (%s)" % str(reden)[:80])


class OpslagFout(Exception):
    """Het bestaande opslagbestand is onleesbaar; het mag niet stil als leeg worden behandeld."""


def _is_leeg(pad):
    try:
        with open(pad, "rb") as f:
            return not f.read().replace(bytes([0xEF, 0xBB, 0xBF]), b"").strip()
    except OSError:
        return False


def laad_opslag(pad):
    """Ontbrekend bestand: lege opslag (eerste run). Bestaand maar onleesbaar of met een andere structuur
    (behalve 0 bytes: telt als leeg, er is niets te verliezen): OpslagFout, zodat het bestand nooit wordt overschreven."""
    uitleg = " Het bestand is niet overschreven of gewijzigd; herstel of verwijder het zelf en draai daarna opnieuw."
    if os.path.isdir(pad):
        raise OpslagFout("het opslagpad %s is een map, geen bestand." % pad + uitleg)
    try:
        with open(pad, encoding="utf-8") as f:
            d = json.load(f)
    except FileNotFoundError:
        return {"items": []}
    except OSError:
        raise OpslagFout("het opslagbestand %s kan niet gelezen worden." % pad + uitleg)
    except ValueError:  # ongeldige JSON, afgekapt of geen UTF-8
        if _is_leeg(pad):  # 0 bytes (of alleen witruimte): er is niets te verliezen, dus gewoon leeg beginnen
            return {"items": []}
        raise OpslagFout("het opslagbestand %s is onleesbaar (geen geldige JSON in UTF-8 zonder BOM, of afgekapt)." % pad + uitleg)
    if not isinstance(d, dict) or not isinstance(d.get("items"), list):
        raise OpslagFout("het opslagbestand %s heeft een onverwachte structuur (verwacht een object met een lijst 'items')." % pad + uitleg)
    return d


def _opslag_probleem(i):
    """Reden (tekst) als een opgeslagen item niet bruikbaar is, anders None. Ontbrekend id telt niet (wordt hersteld)."""
    if not isinstance(i.get("url"), str) or not i["url"].strip():
        return "link ontbreekt"
    if i.get("titel") is not None and not isinstance(i.get("titel"), str):
        return "titel is geen tekst"
    d = i.get("datum")
    if not isinstance(d, str):
        return "datum ontbreekt"
    try:
        datetime.strptime(d, "%Y-%m-%d")
    except ValueError:
        return "datum is ongeldig"
    if "id" in i and i["id"] is not None and not isinstance(i["id"], str):
        return "id is geen tekst"
    return None


VERPLICHTE_CATEGORIEEN = ("BI", "Data", "Automatisering", "AI")
OPRUIM_GRENS = 0.5  # meer dan dit aandeel van de opgeslagen items verwijderen door herindeling = vangnet


def draai(cfg, uitvoer, controleer_robots=True, lees=_lees, nu=None, log=print, forceer_opruimen=False):
    """Haalt alle feeds op. Geeft de exitcode (0 = minstens een feed OK, 1 = niets gedaan, vangnet of alle feeds mislukt)."""
    nu = nu or datetime.now(timezone.utc)
    vandaag = nu.date()
    dagen = cfg.get("bewaar_dagen", 60)
    grens = (vandaag - timedelta(days=dagen)).isoformat()
    matchers = maak_matchers(cfg["trefwoorden"], cfg.get("uitsluitingen"))
    weiger = maak_weigerlijst(cfg)
    bestaand = laad_opslag(uitvoer)
    items = {}
    for i in bestaand["items"]:
        if not isinstance(i, dict) or "url" not in i:
            continue
        reden = _opslag_probleem(i)
        if reden:
            log("WAARSCHUWING: opgeslagen item overgeslagen en niet bewaard (%s): titel %r, link %r." % (
                reden, i.get("titel"), i.get("url")))
            continue
        if not i.get("id"):  # id ontbreekt: herleidbaar uit de link, net als bij nieuwe items
            i["id"] = hashlib.sha1(i["url"].encode("utf-8")).hexdigest()[:12]
        items[i["url"]] = i
    # Items van een bron die niet (meer) in de config staat worden verwijderd (US-019 c3); items van een
    # feed die wel in de config staat maar faalt blijven staan.
    bekend = {f.get("naam") for f in cfg["feeds"] if isinstance(f, dict)}
    for url, i in list(items.items()):
        if i.get("bron") not in bekend:
            del items[url]
    # Opgeslagen items opnieuw indelen, zodat wijzigingen in trefwoorden/uitsluitingen ook voor oude items gelden.
    # Vangnet: verdwijnt daardoor meer dan de helft van de items van geconfigureerde bronnen, dan is de config
    # waarschijnlijk fout (typo, lege lijst) en wordt niets weggeschreven.
    totaal_bron = len(items)
    start_urls = set(items)
    herindeling = {}
    for url, i in list(items.items()):
        cat = categoriseer(i.get("titel", ""), i.get("samenvatting", ""), matchers)
        if cat is None or weiger.reden(i.get("titel", ""), i.get("samenvatting", "")):
            herindeling[url] = None
        else:
            herindeling[url] = cat
    weg = sum(1 for c in herindeling.values() if c is None)
    if totaal_bron and weg > totaal_bron * OPRUIM_GRENS and not forceer_opruimen:
        log("STOP: de herindeling zou %d van de %d opgeslagen items (%d%%) verwijderen; dat is meer dan %d%%. "
            "Er is niets weggeschreven: %s blijft ongewijzigd. Controleer trefwoorden, uitsluitingen en weigertermen "
            "in de config, of draai opnieuw met --forceer-opruimen als dit de bedoeling is." % (
                weg, totaal_bron, round(100 * weg / totaal_bron), round(100 * OPRUIM_GRENS), os.path.basename(uitvoer)))
        return 1
    for url, cat in herindeling.items():
        if cat is None:
            del items[url]
        else:
            items[url]["categorie"] = cat
    status, geslaagd = [], 0
    for feed in cfg["feeds"]:
        try:
            ruw = parse_feed(haal_feed(feed, cfg, controleer_robots, lees))
            geweigerd, geweigerd_links = [], []
            nieuw, zonder_titel, zonder_cat = verwerk_items(
                ruw, feed, matchers, vandaag, cfg.get("max_samenvatting", 300), weiger, geweigerd, geweigerd_links)
            # Geweigerd tellen op unieke link, zoals bewaarde items (dubbele links binnen een feed tellen een keer).
            gezien, uniek_geweigerd = set(), []
            for t, l in zip(geweigerd, geweigerd_links):
                if l not in gezien:
                    gezien.add(l)
                    uniek_geweigerd.append(t)
            geweigerd = uniek_geweigerd
            uniek = {}
            for n in nieuw:  # dubbele links binnen een feed tellen een keer
                uniek.setdefault(n["url"], n)
            nieuw = list(uniek.values())
            recent = [n for n in nieuw if n["datum"] >= grens]
            verouderd = len(nieuw) - len(recent)
            toegevoegd = len([n for n in recent if n["url"] not in items])
            for n in recent:
                items[n["url"]] = n
            geslaagd += 1
            regel = ("OK    %s: %d items in feed, %d bewaard (%d nieuw), %d verouderd, "
                     "%d zonder categorie, %d geweigerd (kwaliteit), %d zonder titel/link overgeslagen") % (
                feed["naam"], len(ruw), len(recent), toegevoegd, verouderd, zonder_cat, len(geweigerd), zonder_titel)
            if geweigerd:
                regel += "\n      geweigerd, bijv.: " + " | ".join(t[:80] for t in geweigerd[:3])
            status.append({"feed": feed["naam"], "status": "OK", "items": len(ruw), "bewaard": len(recent),
                           "verouderd": verouderd, "geweigerd": len(geweigerd)})
        except FeedFout as e:
            regel = "FOUT  %s: %s" % (feed["naam"], e)
            status.append({"feed": feed["naam"], "status": "FOUT", "reden": str(e)})
        except Exception as e:  # een onverwachte fout in een feed stopt de rest niet
            regel = "FOUT  %s: onverwachte fout (%s)" % (feed["naam"], type(e).__name__)
            status.append({"feed": feed["naam"], "status": "FOUT", "reden": regel})
        log(regel)
    if geslaagd == 0:
        log("Alle feeds mislukt: %s blijft ongewijzigd." % os.path.basename(uitvoer))
        return 1
    behouden = [i for i in items.values() if i.get("datum", "") >= grens]
    behouden.sort(key=lambda i: (i["datum"], i["id"]), reverse=True)
    # Vangnet over alles samen (herindeling en leeftijdsopruiming): van de opgeslagen items van geconfigureerde
    # bronnen mag niet meer dan de helft verdwijnen. Gewoon verouderen van een gezonde opslag blijft ver daaronder.
    blijft = {i["url"] for i in behouden}
    verdwijnt = len(start_urls - blijft)
    if start_urls and verdwijnt > len(start_urls) * OPRUIM_GRENS and not forceer_opruimen:
        log("STOP: herindeling en leeftijdsopruiming (bewaar_dagen: %s) zouden samen %d van de %d opgeslagen items "
            "(%d%%) verwijderen; dat is meer dan %d%%. Er is niets weggeschreven: %s blijft ongewijzigd. Controleer "
            "'bewaar_dagen' en de trefwoorden in de config, of draai opnieuw met --forceer-opruimen als dit de "
            "bedoeling is." % (dagen, verdwijnt, len(start_urls), round(100 * verdwijnt / len(start_urls)),
                               round(100 * OPRUIM_GRENS), os.path.basename(uitvoer)))
        return 1
    log("Totaal opgeslagen: %d items (%d ouder dan %d dagen verwijderd)." % (
        len(behouden), len(items) - len(behouden), dagen))
    uit = {"bijgewerkt": nu.replace(microsecond=0).isoformat(), "feeds": status, "items": behouden}
    os.makedirs(os.path.dirname(os.path.abspath(uitvoer)), exist_ok=True)
    tmp = uitvoer + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(uit, f, ensure_ascii=False, indent=1)
    os.replace(tmp, uitvoer)
    return 0


def controleer_config(cfg):
    """Gooit ValueError met een Nederlandse melding als de configuratie niet bruikbaar is."""
    if not isinstance(cfg, dict):
        raise ValueError("verwacht een JSON-object")
    if not isinstance(cfg.get("user_agent"), str) or not cfg["user_agent"].strip():
        raise ValueError("'user_agent' ontbreekt of is geen tekst")
    tw = cfg.get("trefwoorden")
    if not isinstance(tw, dict):
        raise ValueError("'trefwoorden' ontbreekt of is geen object")
    for cat, woorden in tw.items():
        if not isinstance(woorden, list) or not all(isinstance(w, str) for w in woorden):
            raise ValueError("trefwoorden van categorie \"%s\" zijn geen lijst van tekst" % cat)
    feeds = cfg.get("feeds")
    if not isinstance(feeds, list):
        raise ValueError("'feeds' ontbreekt of is geen lijst")
    for n, feed in enumerate(feeds, 1):
        if not isinstance(feed, dict):
            raise ValueError("feed %d is geen object" % n)
        naam = feed.get("naam")
        if not isinstance(naam, str) or not naam.strip():
            raise ValueError("feed %d mist een naam (tekst)" % n)
        for veld in ("url", "taal"):
            if not isinstance(feed.get(veld), str) or not feed[veld].strip():
                raise ValueError('feed "%s" mist %s (tekst)' % (naam, veld))
        if not feed["url"].strip().lower().startswith(("http://", "https://")):
            raise ValueError('feed "%s": de url moet beginnen met http:// of https://' % naam)
    if not feeds:
        raise ValueError("geen feeds ingesteld ('feeds' is een lege lijst)")
    for cat in VERPLICHTE_CATEGORIEEN:
        woorden = tw.get(cat)
        if woorden is None:
            raise ValueError("trefwoorden ontbreken voor categorie \"%s\" (verplicht: %s; let op hoofdletters)" % (
                cat, ", ".join(VERPLICHTE_CATEGORIEEN)))
        if not woorden or not all(w.strip() for w in woorden):
            raise ValueError("trefwoorden van categorie \"%s\" zijn leeg of bevatten een lege term" % cat)
    if "bewaar_dagen" in cfg:
        bd = cfg["bewaar_dagen"]
        if isinstance(bd, bool) or not isinstance(bd, int) or bd < 1:
            raise ValueError("'bewaar_dagen' moet een geheel getal van minimaal 1 zijn (bijv. 60)")
    for veld in ("uitsluitingen", "weigertermen", "weigertermen_samenvatting", "weiger_uitzonderingen"):
        if veld in cfg and (not isinstance(cfg[veld], list) or not all(isinstance(w, str) for w in cfg[veld])):
            raise ValueError("'%s' is geen lijst van tekst" % veld)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Haal nieuwsfeeds op en sla ze op als JSON.")
    ap.add_argument("--config", default=STANDAARD_CONFIG)
    ap.add_argument("--uitvoer", default=STANDAARD_UITVOER)
    ap.add_argument("--forceer-opruimen", action="store_true",
                    help="schrijf ook weg als de herindeling meer dan 50%% van de opgeslagen items verwijdert")
    ap.add_argument("--geen-robots", action="store_true", help="alleen voor tests met lokale feeds")
    a = ap.parse_args(argv)
    try:
        with open(a.config, encoding="utf-8-sig") as f:
            cfg = json.load(f)
        controleer_config(cfg)
    except FileNotFoundError:
        print("FOUT: configuratiebestand niet gevonden: %s" % a.config, file=sys.stderr)
        return 2
    except OSError:
        print("FOUT: configuratiebestand niet te lezen: %s" % a.config, file=sys.stderr)
        return 2
    except json.JSONDecodeError:
        print("FOUT: ongeldig configuratiebestand %s: geen geldige JSON" % a.config, file=sys.stderr)
        return 2
    except UnicodeDecodeError:
        print("FOUT: ongeldig configuratiebestand %s: geen leesbare tekst (UTF-8)" % a.config, file=sys.stderr)
        return 2
    except ValueError as e:
        print("FOUT: ongeldig configuratiebestand %s: %s" % (a.config, e), file=sys.stderr)
        return 2
    try:
        return draai(cfg, a.uitvoer, controleer_robots=not a.geen_robots, forceer_opruimen=a.forceer_opruimen)
    except OpslagFout as e:
        print("FOUT: %s" % e, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
