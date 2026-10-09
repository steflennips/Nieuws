# Status

- **AUTONOMIE:** stop-per-iteratie   <!-- opties: stop-per-iteratie | stop-bij-vragen | volledig-autonoom -->
- **BUDGET PER ITERATIE:** maximaal 14 subagent-aanroepen (de intake in iteratie 0 telt niet mee)   <!-- Stef kan dit aanpassen; overschrijding = noodrem -->
- **FASE:** 2 (echte data en echte website; fase 1 goedgekeurd door Stef op 2026-10-08)
- **HUIDIGE ITERATIE:** 7 beoordeeld (US-019, US-021 geaccepteerd; US-020 afgewezen op 3 vervallen testbestanden). Voorstel 8: US-020 afronden + US-022 kleine afwerking, daarna voorbeeld bij Stef, publiceren en live-check US-013 c1/c3.
- **AANROEPEN DEZE ITERATIE:** 11 / 14
- **FIXRONDES DEZE ITERATIE:** 4 (3 + 1 extra met akkoord Stef); NOODREM: loop gestopt, wacht op beslissing Stef
- **LAATSTE TESTRESULTAAT:** NIET GESLAAGD (iteratie 8, ronde 5): 294 tests groen; 6 nieuwe extra dataverlies/traceback-tests rood (vangnet-gat bij handmatig gewijzigde opslag, extreme config-waarden)
- **RELEASE-ADVIES PO:** NEE (US-020 c1 afronden en US-013 c1/c3 live check open)

## Context-samenvatting
<!-- Beheerd door de Product Owner. Maximaal 25 regels. Alle agents lezen dit EERST en openen daarna alleen wat ze nodig hebben. -->
- Doel fase 2: openbare, gratis nieuwssite (Data/Automatisering/AI, NL+EN) met echte RSS-data, dagelijks ververst. Geen login, geen leads. Fase 1 (prototype met leads, voorbeelddata) goedgekeurd 2026-10-08.
- Techniek: Python stdlib. Lokale app verwijderd (it. 7). src/: ophalen.py -> data/nieuws.json, bouw.py -> statische site (site/), mix.py, veilig_check.py. config/feeds.json: 10 feeds (4 NL headnieuws, 6 EN; AWS Big Data vervangen door Power Platform Blog). GitHub Actions dagelijks ~06:00 NL + handmatig. Bekijken: `python -m http.server --directory site`. Tests zonder internet.
- Tests na it. 7: 112 unittests + 264 acceptatietests (256 groen, 8 geskipt vervallen lokale-app-tests), 375/1280 px headless Edge. 4 categorieen BI/Data/Automatisering/AI, AI max 40%, weigerlijst, Uitgelicht (alleen headnieuws, +1 NL) + Vaknieuws.
- Geaccepteerd: US-001-004, US-007, US-008 (fase 1); US-009-011 (it. 3); US-012, US-015 (it. 4); US-016-018 (it. 6); US-019, US-021 (it. 7). Regressie volgens tabel "Regressie na US-020" in BACKLOG. Vervallen: US-003, US-004, US-001 c1/c2/c4.
- Open: US-020 Lokale app verwijderen (MUST, afgewezen it. 7: 3 vervallen testbestanden met "lead(s)" in tests/acceptance + bedrijfsnamencheck via git 66e4d21); US-013 Online (MUST; c1/c3 live na akkoord Stef); US-022 Kleine afwerking (SHOULD: Vaknieuws-teller, NL --config-melding); US-014 taalfilter (COULD). Geparkeerd: US-005, US-006.
- Besluiten Stef: 2026-10-09-open-punten-a-d.md. Echte ronde it. 7: 86 items; BI 37%, Data 5,8%, Autom. 22%, AI 35%.
- Publiceren alleen vanuit een eigen repo met de projectmap (git-root is nu de gebruikersmap; README stap C stopt dan). data/nieuws.json blijft tussen runs bewaard.
- Beslissingen: docs/decisions/2026-10-08-fase2-intake.md, -nieuwsfeeds.md (actuele feedlijst, vervangers bevestigd). Alleen titel, samenvatting (platte tekst, max 300 tekens), datum, bron, link; geen volledige artikelen/afbeeldingen. Items zonder trefwoordtreffer niet tonen. Bewaartermijn 60 dagen. Geen kosten. Leads later, niet op openbare site. Accentkleur strikt op 4 plekken.
- Bekende problemen / open punten:
  - It. 6 fixrondes: besluiten -fixronde1-it6.md en -fixronde2-it6.md. US-016 c7 alleen statische site.
  - KLEIN (na publicatie, Stef oordeelt live): vendor-productitem van headnieuwssite in Uitgelicht (OutSystems/Techzine); LUMC-AI-item als Automatisering; Data klein (Fabric 60% van Data); Engelse titels (US-014); brede trefwoorden; grens geheimenscan. Acceptatietests zetten bytecode-verbod te laat (pycache). Oud proces `python src/app.py` op poort 8000 (Stef stopt). Niet getest: /nieuws zonder .html op GitHub Pages, echte-browserinteractie.
  - Dubbele entiteit-decodering ("Tom &amp;amp; Jerry" -> "Tom & Jerry"): bewust niet opgepakt (zie BACKLOG Planning).
  - Testrapporten it. 1 en 2 ontbreken als bestand; vanaf it. 3 aanwezig in docs/test-reports/.
  - Niet getest: toetsenbord-Tab, echt toestel, browser auto-open, terugknop/snel klikken, grotere datasets; Stef verifieert handmatig.
- Stijl (2026-10-08): strak/zakelijk, licht, donkerblauw #1F2A44 + wit, accent teal #0F766E, systeemfont, informeel (je/jij), desktop eerst, 375 px moet werken. Details in VISION.md.

## Logboek
| Iteratie | Doel | Stories | Test (snel/volledig) | PO-besluit | Aanroepen | Geschat verbruik | Datum |
|---|---|---|---|---|---|---|---|
| 1 | Prototype met navigatie, nieuws en leads (voorbeelddata) | US-001, US-002, US-003 | volledig GESLAAGD in ronde 1 (rapportbestand ontbreekt) | 3x ACCEPTEER | 4 (plan, bouw, test, beoordeling; intake telt niet) | ca. 150k subagent-tokens | 2026-10-08 |
| 2 | Startpagina met tellers en zakelijke stijl | US-004, US-007, US-008 | volledig: ronde 1 GESLAAGD, ronde 2 NIET GESLAAGD (focusrand header), ronde 3 GESLAAGD (rapportbestanden ontbreken) | 3x ACCEPTEER (US-008 na 2 fixrondes), RELEASE-ADVIES JA | 10 | ca. 480k subagent-tokens | 2026-10-08 |
| 3 | Echte RSS-data ophalen, categoriseren, foutafhandeling | US-009, US-010, US-011 | volledig: ronde 1 NIET GESLAAGD (telling Tweakers), ronde 2 GESLAAGD | 3x ACCEPTEER; RELEASE-ADVIES NEE (US-012/013 open) | 6 | ca. 650k subagent-tokens | 2026-10-08 |
| 4 | Statische openbare site, betere categorie-indeling, workflow (niet gepubliceerd) | US-012, US-015, US-013 c2/c4/c5 | volledig: ronde 1-3 NIET GESLAAGD (categorie, bronnenlijst), ronde 4 GESLAAGD (c12 open punt) | US-012 en US-015 ACCEPTEER; US-013 open (c1/c3); RELEASE-ADVIES NEE | 13 | ca. 1,9M subagent-tokens | 2026-10-08 |
| 5+6 | Online zetten voorbereiden; BI-categorie, AI-plafond, kwaliteitsfilter, Uitgelicht | US-013 voorbereiding, US-016, US-017, US-018 | volledig: ronde 1 en 2 NIET GESLAAGD, ronde 3 alle tests groen maar formeel NIET GESLAAGD (2 inhoudelijke punten voor Stef) | ACCEPTEER US-016/017/018 en voorbereiding; US-013 open; RELEASE-ADVIES NEE | 13 | ca. 3,5M subagent-tokens | 2026-10-09 |
| 7 | Feedruil, lokale app verwijderd, Uitgelicht alleen headnieuws | US-019, US-020, US-021 | volledig GESLAAGD in ronde 1 (264 acceptatietests, 8 bewust geskipt) | US-019 en US-021 ACCEPTEER, US-020 AFWIJZEN (c1: 3 vervallen testbestanden verwijderen, wacht op akkoord Stef); RELEASE-ADVIES NEE | 5 | ca. 0,7M subagent-tokens | 2026-10-09 |
