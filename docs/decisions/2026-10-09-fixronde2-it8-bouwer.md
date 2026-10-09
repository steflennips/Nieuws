# 2026-10-09 Fixronde 2 it. 8: uitvoering (Bouwer)

- Vangnet wordt berekend voor het ophalen (op de opgeslagen items van geconfigureerde bronnen); bij weigeren geen netwerkverkeer en exitcode 1. Drempel: verwijderd > 50% (OPRUIM_GRENS in src/ophalen.py).
- Validatievolgorde in controleer_config: bestaande controles eerst (zodat bestaande meldingen gelijk blijven), daarna lege feedlijst, vier trefwoordcategorieen, lijstvelden.
- Testfixture tests/test_ophalen.py kreeg categorie "BI" erbij: de oude fixture had maar 3 categorieen en is volgens c3 geen geldige config meer. Geen assertie gewijzigd.
