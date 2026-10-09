# 2026-10-08 Uitwerking stijl (iteratie 2)

- CSS blijft inline in `src/app.py` (geen externe bestanden); alle kleuren staan als variabelen in `:root`, inclusief de drie statustinten van leads.
- Actief menu-item: witte tekst op teal; inactieve items wit op donkerblauw (geen extra kleur). Geen schaduwen, om kleurafwijkingen te vermijden.
- Maximale breedte 1080 px; onder 720 px staan tegels en blokken onder elkaar.
- Filterwaarden worden met `kies()` hoofdletterongevoelig naar de canonieke schrijfwijze omgezet; onbekend wordt Alle.
- `/favicon.ico` geeft 204.
