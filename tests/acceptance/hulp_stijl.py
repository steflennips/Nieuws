"""Gedeelde stijl- en teksthulp voor de acceptatietests (iteratie 7).

Deze functies kwamen eerder uit test_acceptance.py (de lokale app, die in iteratie 7 is verwijderd).
De logica is ongewijzigd; ze lezen nu alleen de gebouwde statische site (style.css, *.html).
Dit bestand heet niet test*.py, dus unittest verzamelt het niet als testmodule.
"""
import html as htmllib
import re


def zichtbare_tekst(page):
    page = re.sub(r"<style>.*?</style>", " ", page, flags=re.S)
    return htmllib.unescape(re.sub(r"<[^>]+>", " ", page))


def interface_tekst(page):
    """Zichtbare tekst zonder nieuws- en leadsinhoud (titels, samenvattingen, bronnamen).

    Het criterium gaat over labels, knoppen en menu's (US-001-c5, US-008-c7). Inhoud van bronnen
    (bijv. een Engelse nieuwstitel) valt daar niet onder.
    """
    page = re.sub(r"<article\b.*?</article>", " ", page, flags=re.S)
    page = re.sub(r"<li>.*?</li>", " ", page, flags=re.S)
    return zichtbare_tekst(page)


def css_van(page):
    return re.search(r"<style>(.*?)</style>", page, re.S).group(1)


def css_regels(css):
    """Lijst van (selector, body) zonder commentaar; @media-blokken worden platgeslagen."""
    return [(s.strip(), b) for s, b in re.findall(r"([^{}]+)\{([^{}]*)\}", css)]


def root_vars(css):
    root = re.search(r":root\{(.*?)\}", css, re.S).group(1)
    return {k: v.upper() for k, v in re.findall(r"--([a-z0-9-]+):(#[0-9A-Fa-f]{6})", root)}


def luminantie(hexkleur):
    h = hexkleur.lstrip("#")
    kanalen = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255
        kanalen.append(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * kanalen[0] + 0.7152 * kanalen[1] + 0.0722 * kanalen[2]


def contrast(a, b):
    la, lb = sorted([luminantie(a), luminantie(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)
