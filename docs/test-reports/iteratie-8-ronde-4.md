ITERATIE: 8 | RONDE: 4 | MODUS: VOLLEDIG
RESULTAAT: NIET GESLAAGD (BLOKKEREND: bewaar_dagen-fout of 0 wist opgeslagen items stil weg, bevinding 1; dit is na de derde fixronde, dus noodrem naar Stef)

PER CRITERIUM:
- US-022-c1: OK via suite (test_US022_c1_*): geen totaal in de kop van Vaknieuws, link "Alle <n> berichten bekijken".
- US-022-c2: OK via suite (test_US022_c2_*): ontbrekend, onleesbaar, geen UTF-8, map, feeds als object: exitcode 2, Nederlands, geen traceback. Bouw met ontbrekend data-bestand: alleen Nederlandse melding (ronde 3 bevinding 3 opgelost).
- US-022-c3: OK via suite (test_US022_c3_*): trefwoorden {}, sleutel "Ai", lege lijst/term, tekst i.p.v. lijst: exitcode 2, Nederlands, data byte-gelijk.
- US-022-c4: OK op het criterium (suite groen: 50% geschreven, 51% geweigerd, --forceer-opruimen geschreven). Aanvullende tests ronde 4 (r4a) FALEN: zie bevinding 1.
- US-022-c5: OK via suite (test_US022_c5_*): BOM met tekst exitcode 0; lijstvelden, url-schema, "feeds": [] correct afgehandeld. Aanvullend (r4b) FAALT: bewaar_dagen 0 of tekst, zie bevinding 1 en 2.
- Ronde 3 bevinding 1 (onleesbaar data-bestand, BLOKKEREND): OPGELOST. Geteste varianten (echte bestanden, lokale feed): UTF-8 met BOM + inhoud: exitcode 2, Nederlands, bestand byte-gelijk; afgekapt, ongeldige JSON, latin-1, items null, lijst als root, map: exitcode 2, byte-gelijk, geen .tmp; 0 bytes, alleen witruimte, alleen BOM: leeg (exitcode 0). Netwerk: laad_opslag() wordt vóór het ophalen aangeroepen, dus bij weigering geen feedverkeer (code-inspectie).
- Ronde 3 bevinding 2 (--uitvoer naar een map): OPGELOST: exitcode 2, "is een map, geen bestand", geen .tmp.
- Ronde 3 bevinding 3 (Engelse OS-tekst bij ontbrekend bouw-bestand): OPGELOST: alleen "FOUT: ... ontbreekt. Draai eerst: python src/ophalen.py".
- Ronde 3 bevinding 6 (src/__pycache__): OPGELOST: geen __pycache__ in src/ of tests/ (gecontroleerd na alle runs).
- US-020-c1: OK voor het leadwoord-deel (src/, tests/, config/, README.md; geen leadstatussen; app.py en data.py weg). Deel verzonnen bedrijfsnamen vervallen per PO-besluit, niet getoetst.
- US-020-c2, c3, c4: OK via suite (geen ImportError, verse checkout met lokale feeds, README zonder startinstructie lokale app).
- US-013-c1 en c3: NIET GETEST, omdat er geen toegang is tot de live site en de GitHub-run.
- US-001 t/m US-021 (regressie): zie REGRESSIE.

BEVINDINGEN:
1. BLOKKEREND (dataverlies, nieuw in ronde 4; extra tests test_US022_extra_r4a_* en r4b, afgeleid van US-022 c4 en c5; geen geschreven criterium). Het vangnet van US-022 c4 dekt alleen de herindeling, niet de leeftijdsopruiming via bewaar_dagen. Reproduceren: (a) kopie van data/nieuws.json met 100 items (10 van 1 dag oud, 90 van 30 dagen oud) in een tijdelijke map; (b) config met een bereikbare lokale feed en "bewaar_dagen": 6 (typo voor 60); (c) python src/ophalen.py --config <config> --uitvoer <kopie>. Verwacht: niet stil wegschrijven: exitcode != 0 met melding en bestand ongewijzigd, of minstens 50 items over. Werkelijk: exitcode 0, 90 van 100 items verdwenen, zonder melding. Zelfde met "bewaar_dagen": 0: exitcode 0, 1 van 100 items over. Impact op de echte data (berekend op een kopie van de 87 items): bij 6 dagen zouden 68 van 87 verdwijnen. De dagelijkse job commit dat en publiceert een bijna lege site.
   Voorstel PO: (a) bewaar_dagen valideren (geheel getal, minimaal 1; anders exitcode 2 met Nederlandse melding); (b) de vangnet-regel uitbreiden naar de leeftijdsopruiming (meer dan 50% van de items van geconfigureerde bronnen weg: niets schrijven, tenzij --forceer-opruimen). Beslissing voor PO of 6 dagen bewust toegestaan moet blijven met --forceer-opruimen.
2. BELANGRIJK: bewaar_dagen als tekst ("60") geeft een traceback (TypeError in draai), exitcode 1, bestand ongewijzigd. Verwacht: exitcode 2, Nederlandse melding, geen traceback. Reproduceren: test_US022_extra_r4b_bewaar_dagen_tekst_is_configfout. Oplossing samen met bevinding 1 (a).
3. BELANGRIJK: geldige JSON met een opgeslagen item zonder id geeft een traceback (KeyError in de sortering), exitcode 1, bestand ongewijzigd (test_US022_extra_r4c_item_zonder_id_geen_traceback). Item met datum null: zelfde traceback (TypeError). Geen dataverlies, maar de dagelijkse job faalt elke dag tot het bestand met de hand hersteld is. Verwacht: nette Nederlandse melding of de item overslaan, geen traceback.
4. KLEIN: opgeslagen items zonder url, zonder bron (niet geconfigureerd), zonder datum-sleutel, of die geen object zijn, verdwijnen stil bij het wegschrijven (exitcode 0; geen vangnet, want die items tellen niet mee). De ophaalronde maakt zulke items zelf niet; het is alleen zichtbaar bij handmatig bewerkt bestand. Opgeslagen item met titel null blijft staan (exitcode 0); bouw slaat die over. Ter overweging PO.
5. KLEIN (ter kennis, redeneren, niet gereproduceerd): twee gelijktijdige lokale runs gebruiken dezelfde tijdelijke naam nieuws.json.tmp; het resultaat kan een corrupt bestand zijn. Dat geeft geen stille leegte (de volgende run weigert, exitcode 2), maar kan wel een run laten crashen. CI is serieel door de concurrency-groep "pages" in de workflow.
6. KLEIN (ter kennis, bekend uit ronde 3 bevinding 4 en spec US-019 c3 / US-022 c4): een feed die hernoemd of getypt wordt in config/feeds.json laat zijn items verdwijnen bij de volgende run, zonder vangnet. Voorbeeld: 10 van 87 items. Dit is zo gespecificeerd; PO beslist of het vangnet ook hiervoor moet gelden.
7. OPERATIONEEL (blijft open): drie python-processen draaien nog: PID 34772 luistert op 127.0.0.1:8000; PID 43088 luistert op 0.0.0.0:8080 (bereikbaar via het netwerk); PID 44480 zonder poort. Niet door mij gestart, dus niet gestopt. Stef of orchestrator moet controleren en stoppen.
8. KLEIN (beoordeling van het keuzepunt van de Bouwer): data/nieuws.json met BOM en inhoud wordt geweigerd (exitcode 2) i.p.v. gelezen. Dat is acceptabel: fail-safe, de README vermeldt het, het bestand blijft intact en het herstel is één handeling. Suggestie voor later: utf-8-sig lezen zoals de config, dan is er geen handwerk nodig.

SUITE: acceptatie 299 tests, 290 geslaagd, 4 gefaald (alle 4 zijn de nieuwe extra tests r4a en r4b, aangevuld met r4c-id), 5 geskipt (vervallen lokale-app-tests, met reden); de 6 extra tests van ronde 4 zijn: r4a, r4b x2, r4c x2 (datum en id), r4d. Commando: `python -B -m unittest discover -s tests/acceptance -t tests/acceptance -v` vanuit de projectmap (PYTHONDONTWRITEBYTECODE=1). Zonder de extra tests van ronde 4: 293 tests, 288 geslaagd, 5 geskipt, 0 gefaald (regressie).
Bouwer-suite: `python -B -m unittest discover -s tests -v`: 139 geslaagd, 0 gefaald.

REGRESSIE: NIET GESLAAGD door bevinding 1 (BLOKKEREND). Overig OK:
- Statische site, browsertests in de suite (headless Edge, 375 px via iframe en 1280 px): OK (US-001 c6, US-002 c5/c6, US-008 c8, US-012 c8, US-016 c7, US-018 c6).
- python src/veilig_check.py: exitcode 0 ("OK: geen geheimen, e-mailadressen, lokale paden of verdachte bestanden gevonden.").
- Geen __pycache__ in src/ of tests/ (controle na alle runs).
- Echte ophaalronde (eenmalig, naar een kopie van data/nieuws.json in de tijdelijke map; data/nieuws.json NIET aangeraakt; robots.txt gecontroleerd door de Bouwer, ophalen volgt robots.txt): exitcode 0, 10 van 10 feeds OK, 94 items opgeslagen (kopie had 87; 7 nieuw). Bouw van de kopie: exitcode 0, 93 nieuwsitems, 10 bronnen, geen fouten.
  Per feed (items in feed / bewaard / geweigerd): Power BI Blog 20/13/0 (7 verouderd) | Microsoft Fabric Blog 20/20/0 | SQLBI 30/2/0 | Power Platform Blog 10/6/0 | Camunda Blog 50/13/2 | n8n Blog 15/12/1 | Computable 10/4/0 (1 nieuw) | Emerce 10/2/0 (2 nieuw) | Techzine 10/4/0 (4 nieuw) | NOS Tech 20/10/0.
  Per categorie opgeslagen (94, vóór AI-plafond): BI 32 (34,0%), Data 5 (5,3%), Automatisering 19 (20,2%), AI 38 (40,4%). Na bouwen: 93 items, AI 37 (plafond 40%).
  Per feed binnen categorie: BI: Fabric 53%, Power BI 38%, SQLBI 6%. Data: Fabric 60% (3 van 5, niet boven 60%), Power BI 20%, Power Platform 20%. Automatisering: n8n 37%, Camunda 26%, Power Platform 21%. AI: NOS Tech 26%, Camunda 18%, Techzine 16%.
  Meetpunten (melden): BI+Data 39,4% (>= 30%) OK; Automatisering 20,2% (>= 20%) OK; geen feed boven 60% van een categorie. Open punt: Data klein (5,3%), al bekend.
- Atomair schrijven: bij een mislukte schrijfactie (surrogaat in een opgeslagen item) blijft het origineel byte-gelijk (test r4d OK); er blijft een .tmp-restbestand over (gitignored, geen dataverlies).
- Vaknieuws-kop, tellers, Uitgelicht: via suite groen (US-018, US-021, US-022 c1).
- Categorie-herindeling van opgeslagen items met onbekende of ontbrekende categorie: herindeeld op titel (LUMC, leeg, AI zonder treffer: correct).
- Basischecks: de echte ronde gaf geen FOUT-regels. Logs van de gebruikte commando's: geen fouten behalve de hierboven genoemde.
- Servers: de testfeedserver van de Tester is gestopt; geen eigen processen meer actief.

BENODIGD VAN BOUWER:
- BLOKKEREND (bevinding 1): bewaar_dagen valideren (geheel getal >= 1, anders exitcode 2 Nederlands) en het vangnet uitbreiden naar de leeftijdsopruiming; daarna test_US022_extra_r4a_* en r4b groen.
- BELANGRIJK (bevinding 2 en 3): bewaar_dagen als tekst zonder traceback; opgeslagen item zonder id of met datum null zonder traceback (test r4c-id groen).
- PO: beslissing over bevinding 1 (voorstel en uitzondering met --forceer-opruimen), bevinding 4 en 6 ter kennis.
- Stef of orchestrator: processen 34772, 43088 en 44480 controleren en stoppen (bevinding 7). Na drie fixrondes: noodrem, Stef moet beslissen (CLAUDE.md).
- Stef: US-013 c1 en c3 blijven open tot na publicatie en live-check. Visuele beoordeling en de interactie-tests (zie NIET GETEST) blijven aan Stef.

NIET GETEST (en telt niet als geslaagd):
- Visuele beoordeling in deze ronde (geen screenshots gemaakt): NIET GETEST, visuele beoordeling door Stef nodig. Geautomatiseerde browsertests zijn wel groen.
- Snel klikken, terugnavigeren, herladen, toetsenbord-Tab en console van een echte browser: NIET GETEST, omdat er geen interactieve browsersessie is opgezet.
- US-013 c1 en c3 (live site en GitHub-run): NIET GETEST, geen toegang tot de live site.
- De dagelijkse GitHub-job zelf: NIET GETEST (alleen het workflow-bestand is geanalyseerd en via de suite gecontroleerd).
- python -m http.server voor de lokale site: NIET GETEST in deze ronde (de suite bouwt de site en test de statische output).
- Samenloop van twee echte runs (bevinding 5): NIET GETEST, alleen geredeneerd.

BESTANDEN GEWIJZIGD DOOR MIJ:
- tests/acceptance/test_US022_ronde4_dataverlies.py (nieuw; 6 extra tests, 4 rood: r4a, r4b x2, r4c-id)
- tests/acceptance/README.md (tabel "Iteratie 8, Tester ronde 4" toegevoegd)
- docs/test-reports/iteratie-8-ronde-4.md (dit rapport)
Tijdelijke bestanden (kopieën van data, configs, logs, testfeed): alleen in de tijdelijke map van het systeem, buiten de projectmap.
