# 2026-10-08: Statische site en workflow (iteratie 4, Bouwer)

- `src/bouw.py` genereert `site/` (index, nieuws, bronnen, CSS, JS, favicons) uit `data/nieuws.json`; alleen stdlib, geen afhankelijkheden. HTML wordt server-side volledig gerenderd; `app.js` filtert/zoekt client-side op `?categorie=` en `?q=` (zonder JS zie je alle items). Relatieve links, zodat het ook onder `/<repo>/` werkt.
- Geen voorbeelddata: zonder echte data stopt het bouwen met een fout. De lokale app (`src/app.py`, met leads) blijft ongewijzigd bestaan, maar deelt geen code met de statische site.
- "Laatst bijgewerkt" in Nederlandse tijd, berekend zonder tijdzonedatabase (CET/CEST-regel), omdat `zoneinfo` op Windows `tzdata` nodig heeft.
- Workflow: een cron (04:00 UTC = 06:00 zomertijd, 05:00 winter) in plaats van twee crons met uur-controle, omdat GitHub geplande jobs kan uitstellen en een uur-controle dan ten onrechte zou overslaan. Rechten: `contents: write` om `data/nieuws.json` terug te committen (60 dagen bewaren), `pages: write` en `id-token: write` voor publiceren. Geen eigen geheimen.
- `data/nieuws.json` is uit `.gitignore` gehaald (de job bewaart daarin de 60 dagen historie); `site/` is erbij gezet.
- US-015: `uitsluitingen` in `config/feeds.json` (tekst die eronder valt telt niet mee), meer trefwoorden, en `ophalen.py` deelt opgeslagen items opnieuw in bij elke ronde (items die geen treffer meer hebben vallen weg). `maak_matchers(trefwoorden, uitsluitingen=None)` blijft compatibel met bestaande aanroepen.
