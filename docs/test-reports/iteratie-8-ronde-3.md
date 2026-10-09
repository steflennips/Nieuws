ITERATIE: 8 | RONDE: 3 | MODUS: VOLLEDIG
RESULTAAT: NIET GESLAAGD (BLOKKEREND: dataverlies bij een onleesbaar data/nieuws.json, bevinding 1; de criteria US-022 c3-c5 zelf zijn OK)

PER CRITERIUM:
- US-022-c1: OK via suite (test_US022_c1_fixture_* en test_US022_c1_echte_data_*): geen totaal in de kop van Vaknieuws, link "Alle <n> berichten bekijken".
- US-022-c2: OK via suite (test_US022_c2_*, incl. de ronde-1/2-extra's); ontbrekend, onleesbaar, geen UTF-8, map, feed-item als tekst, feed zonder url, feeds als object: exitcode 2, Nederlands, geen traceback.
- US-022-c3: OK. Zeven gevallen (trefwoorden {}, sleutel "Ai", lege lijst, lege term, term met alleen spaties, tekst i.p.v. lijst, categorie Data ontbreekt): exitcode 2, Nederlandse melding die de categorie noemt, data/nieuws.json byte-gelijk (sha256). Reproductie ronde 2 (87 items, echte feedlijst, bereikbare lokale feed, `trefwoorden: {}`): exitcode 2, bestand intact (test_US022_c3_repro_ronde2_*).
- US-022-c4: OK op het criterium. 50% geschreven (10 van 10 en 50 van 100: exitcode 0). 51% geweigerd (51 van 100 en 6 van 10: exitcode 1, data ongewijzigd, melding "51 van de 100 ... --forceer-opruimen ... niets weggeschreven"). Met `--forceer-opruimen` geschreven (exitcode 0, 49 items). Feedruil telt niet mee (30 items van een niet-geconfigureerde bron: 10 eigen items blijven, exitcode 0). Gewone ronde niet geblokkeerd (lokale feed met nieuw item; kopie van de echte data met echte trefwoorden: exitcode 0). Workflow gebruikt de optie niet. Aanvullend (extra test, NIET als criterium geschreven): onleesbaar data-bestand wordt stil leeggeschreven, zie bevinding 1: FAALT.
- US-022-c5: OK. UTF-8 met BOM: exitcode 0. uitsluitingen, weigertermen, weigertermen_samenvatting, weiger_uitzonderingen als tekst, getal, object of lijst van niet-tekst: exitcode 2, Nederlands, data ongewijzigd. Url file:///, FILE:///, ftp://, zonder schema, leeg: exitcode 2. `"feeds": []`: exitcode 2 met "geen feeds ingesteld", niet "mislukt"; data ongewijzigd.
- US-020-c1: OK voor het leadwoord-deel (src/, config/, README.md en tests/ zonder lead/leads; geen leadstatussen; app.py en data.py weg; test_US020_c1_*). Het deel verzonnen bedrijfsnamen is vervallen per PO-besluit 2026-10-09-fixronde2-it8 en niet getoetst.
- US-020-c2, c3, c4: OK via suite (test_US020_c2_*, c3 verse checkout met lokale feeds, c4 README).
- US-013-c1 en c3: NIET GETEST, omdat er geen toegang is tot de live site en de GitHub-run.
- US-001 t/m US-021 (regressie): OK in de suite, zie REGRESSIE.

SUITE: acceptatie 293 tests, 286 geslaagd, 2 gefaald (extra test uit bevinding 1, twee varianten), 5 geskipt (vervallen lokale-app-tests met reden). Commando: `python -B -m unittest discover -s . -t . -v` vanuit tests/acceptance (met PYTHONDONTWRITEBYTECODE=1). Ronde 3 voegt 23 tests toe (test_US022_c3_c5_vangnet.py). Vóór mijn toevoeging: 270 tests, 265 geslaagd, 5 geskipt.
Bouwer-suite: `python -B -m unittest discover -s tests -v` vanuit de projectmap: 131 geslaagd, 0 gefaald.

REGRESSIE: NIET GESLAAGD door bevinding 1 (BLOKKEREND). Overig OK:
- Statische site, browsertests in de suite (headless Edge, 375 px via iframe en 1280 px): OK (US-001 c6, US-002 c5/c6, US-007 c2/c3, US-008 c8, US-012 c6/c7).
- Visueel (handmatig, screenshots in de tijdelijke map): 375 px via iframe: tellers onder elkaar, Uitgelicht leesbaar, navigatie in beeld. 1280 px: gecentreerd, tellers 32/5/19/37, donkerblauwe kop, teal op actief menu-item en links. Een directe 375-px-screenshot van headless Edge toonde een breder layout; niet nagegaan (waarschijnlijk minimale venstergrootte van headless), de iframe-methode van de suite is leidend. Totaalbeeld en smaak: aan Stef. Bekende KLEINE punten zichtbaar in Uitgelicht: een vendor-productitem (OutSystems via Techzine) en een LUMC-item als Automatisering.
- `python src/veilig_check.py`: exitcode 0 (97 bestanden; geen geheimen, e-mailadressen, lokale paden).
- __pycache__: geen nieuwe door mij (alle runs met -B / PYTHONDONTWRITEBYTECODE). Wel aanwezig: src/__pycache__ met mix- en ophalen-bytecode, tijdstip 16:32 vandaag, dus vóór mijn run; gitignored; niet verwijderd (buiten mijn map). tests/ en tests/acceptance/: geen __pycache__.
- Echte ophaalronde (eenmalig, naar een kopie van data/nieuws.json in de tijdelijke map, robots.txt gecontroleerd, data/nieuws.json NIET aangeraakt): exitcode 0, 10 van 10 feeds OK, 94 items opgeslagen (kopie had 87; 7 nieuw).
  Per feed (items in feed / bewaard / geweigerd): Power BI Blog 20/13/0 (7 verouderd) | Microsoft Fabric Blog 20/20/0 | SQLBI 30/2/0 | Power Platform Blog 10/6/0 | Camunda Blog 50/13/2 | n8n Blog 15/12/1 | Computable 10/4/0 | Emerce 10/2/0 | Techzine 10/4/0 | NOS Tech 20/10/0.
  Per categorie opgeslagen (94, vóór AI-plafond): BI 32 (34,0%), Data 5 (5,3%), Automatisering 19 (20,2%), AI 38 (40,4%). Na bouwen: 93 nieuwsitems, AI 37 (plafond 40%).
  Per feed binnen categorie: BI: Fabric 17 van 32 (53%), Power BI 12 (38%), SQLBI 2, Camunda 1. Data: Fabric 3 van 5 (60%), Power BI 1, Power Platform 1. Automatisering: n8n 7 van 19 (37%), Camunda 5 (26%), Power Platform 4 (21%), Techzine 2, Emerce 1. AI: NOS Tech 10, Camunda 7, Techzine 6, Computable 6, n8n 5, Emerce 3, Power Platform 1.
  Meetpunten (melden): BI+Data 39,4% (>= 30%) OK; Automatisering 20,2% (>= 20%) OK, net; geen feed boven 60% van een categorie (Fabric precies 60% van Data).
  Geweigerd (ter info): "Camunda Named a Leader in The Forrester Wave ...", "Camunda Recognized as a Visionary in Gartner BOAT Magic Quadrant 2026", "You can now top up your n8n Assistant credits".
- Verkennend (CLI, tijdelijke map): bouw met ontbrekend data-bestand: exitcode 1, Nederlandse hoofdzin (Engelse OS-tekst erachter, zie bevinding 3). Bouw met leeg items: exitcode 1, Nederlandse melding. Bouw met `--vandaag 2026-13-45`: exitcode 1, Nederlandse melding met formaat JJJJ-MM-DD. Ophalen met `--uitvoer` naar een bestaande map: traceback, exitcode 1 (bevinding 2).
- Basischecks: de echte ronde gaf geen FOUT-regels; geen fouten in de logs van de gebruikte commando's behalve de hierboven genoemde. README (vangnet, configcontrole, BOM, exitcodes) klopt met het gemeten gedrag van de tests. Niet getest: console van de browser in een echte browser (klikken, snel klikken, terugnavigeren, herladen): NIET GETEST.
- Servers: alle testservers stoppen zelf na de test; ik heb geen eigen server of headless-Edge-proces laten draaien.

BEVINDINGEN:
1. BLOKKEREND (dataverlies, nieuw in ronde 3; extra test, geen geschreven criterium). Reproduceren: (a) kopieer data/nieuws.json (87 items) naar een tijdelijke map; (b) zet er een UTF-8-BOM voor, of kap het bestand af op de helft; (c) gebruik een geldige config met één bereikbare feed; (d) `python src/ophalen.py --config <config> --uitvoer <kopie>`. Verwacht: niet leeg wegschrijven, dus exitcode niet 0 met Nederlandse melding, of de 87 items blijven staan. Werkelijk: exitcode 0, "Totaal opgeslagen: 0 items", het bestand heeft 0 items (gemeten met BOM en met afgekapt bestand). Oorzaak: laad_opslag() in src/ophalen.py leest met encoding utf-8 zonder BOM-afhandeling en vangt elke ValueError op als lege opslag. Het vangnet van US-022 c4 telt dan niets en de nieuwe feeditems vervangen alles. Impact: de dagelijkse job commit data/nieuws.json; een BOM of beschadigd bestand maakt de publieke site leeg. Test: test_US022_c4_extra_onleesbaar_data_bestand_leegt_de_opslag_niet (ROOD, beide varianten).
2. KLEIN: ophalen met `--uitvoer` naar een bestaande map: traceback (PermissionError) in plaats van een Nederlandse melding, exitcode 1, en er blijft een `<map>.tmp` achter. Reproduceren: `python src/ophalen.py --uitvoer <map>` met een geldige config. Verwacht: Nederlandse melding, geen traceback, geen restbestand.
3. KLEIN: bouw.py bij een ontbrekend data-bestand: de melding is Nederlands, maar bevat de Engelse OS-tekst "[Errno 2] No such file or directory". Verwacht: alleen Nederlandse tekst, zoals US-022 c2 voor ophalen. Reproduceren: `python src/bouw.py --data <bestaat-niet>`.
4. KLEIN, ter kennis PO (volgt uit de code, niet apart gereproduceerd): een feed-naam die in config/feeds.json gewijzigd of getypt wordt, laat de items van die feed bij de volgende run verdwijnen, zonder vangnet. Dit is bewust per besluit 2026-10-09-fixronde2-it8 (punt 2) en US-019 c3. Het is wel een dataverlies-pad: een hernoemde feed van 10 van 87 items verliest die 10 zonder melding.
5. OPERATIONEEL (bevinding 6 uit ronde 2, nog open): drie python-processen draaien: PID 34772 luistert op 127.0.0.1:8000, PID 43088 op 0.0.0.0:8080 (dus bereikbaar via het netwerk), PID 44480 zonder poort (gestart 16:32 vandaag). Niet door mij gestart; niet gestopt. Stef of de orchestrator controleert en stopt ze.
6. OPERATIONEEL, KLEIN: src/__pycache__ bestaat (mix- en ophalen-bytecode, 16:32 vandaag, vóór mijn run). Gitignored, dus niet in de repo; wel tegen de regel "geen __pycache__ in src/". Niet door mij gemaakt en niet verwijderd.

BENODIGD VAN BOUWER:
- BLOKKEREND (bevinding 1): laad_opslag() mag een onleesbare data/nieuws.json niet stil als lege opslag behandelen: stoppen met Nederlandse melding (exitcode 2) en/of utf-8-sig lezen. Daarna test test_US022_c4_extra_onleesbaar_data_bestand_leegt_de_opslag_niet groen, en opnieuw SNEL plus regressie.
- KLEIN (bevindingen 2, 3, 6): --uitvoer-map, Engelse OS-tekst in bouw, pycache opruimen of -B afdwingen.
- Stef of orchestrator: processen 34772, 43088 en 44480 controleren en stoppen (bevinding 5).
- PO: besluit of "onleesbaar data-bestand" een geschreven criterium wordt (uitbreiding US-022 c4); bevinding 4 ter kennis. Bij rapportage aan Stef bevestigen dat het bedrijfsnamen-deel van US-020 c1 vervalt (PO-besluit).
- Stef: US-013 c1 en c3 blijven open tot na publicatie en live-check.

BESTANDEN GEWIJZIGD DOOR MIJ:
- tests/acceptance/test_US022_c3_c5_vangnet.py (nieuw; 23 tests)
- tests/acceptance/README.md (tabel "Iteratie 8, Tester ronde 3" toegevoegd)
- docs/test-reports/iteratie-8-ronde-3.md (dit rapport)
Tijdelijke bestanden (kopie van de data, configs, log, screenshots): alleen in de tijdelijke map van het systeem, buiten de projectmap.
