# Techniekkeuze iteratie 1 (2026-10-08)

- Python 3.12, alleen standaardbibliotheek (http.server), server-side HTML. Geen npm/pip-installatie, geen database, geen JavaScript nodig.
- Filters en zoeken via querystring (`/nieuws?categorie=AI&q=...`, `/leads?status=Nieuw`), dus linkbaar en eenvoudig testbaar.
- Voorbeelddata in `src/data.py` (in-memory), logica in `src/logica.py`.
- Tests: `unittest` (standaard).
- Reden: eenvoudigste techniek die de criteria haalt; start in een commando. Definitieve techniek voor fase 2: zie advies in bouwrapport.
