ITERATIE: 8 | RONDE: 5 | MODUS: VOLLEDIG
RESULTAAT: NIET GESLAAGD (BLOKKEREND: bevinding 1, vangnet ziet items die vóór de herindeling al wegvallen; met exitcode 0 verdwijnt 86 van 87 items. Daarnaast BELANGRIJK: bevindingen 2-5. Dit is na de vierde fixronde: de beslissing ligt bij Stef.)

PER CRITERIUM:
- US-022-c1: OK. Suite groen (test_US022_c1_*); visueel: Overzicht zonder totaal in de kop van Vaknieuws (screenshot 1280 px en 375 px).
- US-022-c2: OK. Suite groen (test_US022_c2_*, incl. ontbrekend/onleesbaar/map/feeds-als-object; exitcode 2, Nederlands, geen traceback).
- US-022-c3: OK. Suite groen (test_US022_c3_*): trefwoorden {}, sleutel "Ai", lege lijst/term, tekst i.p.v. lijst: exitcode 2, data byte-gelijk.
- US-022-c4: OK op de letter (suite groen: 50% geschreven, 51% geweigerd, --forceer-opruimen schrijft). FAALT voor de extra tests van deze ronde: het vangnet telt items niet mee die door validatie of bronfilter wegvallen (bevinding 1 en 2).
- US-022-c5: OK op de letter (suite groen: BOM, lijstvelden, url-schema, "feeds": []). FAALT voor de extra tests van deze ronde: bewaar_dagen extreem groot en ongeldige regex geven een traceback (bevinding 3 en 5).
- US-013-c1 en c3: NIET GETEST, omdat er geen toegang is tot de live site en de GitHub-run.
- Regressie US-001 t/m US-021: zie REGRESSIE.

SUITE: acceptatie 305 tests, 294 geslaagd, 6 gefaald (de nieuwe extra tests r5a-r5f van deze ronde, zie bevindingen 1, 2, 3, 4, 5), 5 geskipt (lokale-app-tests, vervallen met US-020). Commando: `python -B -m unittest discover -s tests/acceptance -t tests/acceptance -v` vanuit de projectmap, met PYTHONDONTWRITEBYTECODE=1. Alle 294 niet-geskipte tests van vóór deze ronde (incl. de r4-tests, nu groen) slagen. Bouwer-suite: `python -B -m unittest discover -s tests -v`: 146 geslaagd, 0 gefaald.

REGRESSIE: NIET GESLAAGD door bevinding 1 (BLOKKEREND); verder OK:
- Statische site: browsertests (headless Edge) groen voor 375 px (via iframe) en 1280 px (US-001 c6, US-002 c5/c6, US-008 c8, US-012 c8, US-016 c7, US-018 c6). Eigen screenshots: 1280 px gecentreerd, vier tellertegels naast elkaar; 375 px in een iframe: navigatie volledig in beeld, kaarten onder elkaar, geen horizontaal scrollen.
- `python src/veilig_check.py`: exitcode 0.
- Geen __pycache__ in src/ of tests/ (gecontroleerd na alle runs).
- Echte ophaalronde naar een kopie in een tijdelijke map (data/nieuws.json en config/feeds.json NIET gewijzigd, cmp gecontroleerd); robots.txt wordt gevolgd: exitcode 0, 10 van 10 feeds OK, 95 items opgeslagen (kopie had 87; 8 nieuw: Computable 2, Emerce 2, Techzine 4). Bouw van de kopie: exitcode 0, 93 nieuwsitems, 10 bronnen.
  Per feed (items in feed / bewaard / geweigerd): Power BI 20/13/0 | Fabric 20/20/0 | SQLBI 30/2/0 | Power Platform 10/6/0 | Camunda 50/13/2 | n8n 15/12/1 | Computable 10/4/0 | Emerce 10/2/0 | Techzine 10/4/0 | NOS Tech 20/10/0.
  Per categorie op de site (93): BI 32 (34,4%), Data 5 (5,4%), Automatisering 19 (20,4%), AI 37 (39,8%, na het AI-plafond van 39 opgeslagen).
  Aandeel per feed binnen categorie: BI: Fabric 53%, Power BI 38%, SQLBI 6%, Camunda 3%. Data: Fabric 60% (3 van 5, niet boven 60%), Power BI 20%, Power Platform 20%. Automatisering: n8n 37%, Camunda 26%, Power Platform 21%, Techzine 11%, Emerce 5%. AI (voor het plafond): NOS Tech 26%, Computable 18%, Camunda 18%, Techzine 15%, n8n 13%, Emerce 8%, Power Platform 3%.
  Meetpunten (melden): BI+Data 39,8% (>= 30%) OK; Automatisering 20,4% (>= 20%) OK; geen feed boven 60% van een categorie (Fabric precies 60% van Data). Data blijft klein (open punt, bekend).
- Basischecks: ophaallog zonder FOUT-regels; bouwlog zonder fouten. Browser-console niet uitgelezen (zie NIET GETEST).

BEVINDINGEN:
1. BLOKKEREND (dataverlies, exitcode 0; extra test test_US022_extra_r5a_andere_datumnotatie_wist_niet_stil_86_van_87). Het vangnet telt alleen items die na de validatie en het bronfilter overblijven. Items die worden overgeslagen omdat hun datum niet JJJJ-MM-DD is, tellen dus niet mee. Reproduceren: opslagbestand met 87 items, bron correct, datum "2026-10-08T00:00:00"; draai `python src/ophalen.py --config <config> --uitvoer <kopie>` met één werkende lokale feed. Verwacht: exitcode != 0 met het bestand ongewijzigd, of minstens 44 items over (README belooft het vangnet voor "opgeslagen items van geconfigureerde bronnen"). Werkelijk: 87 WAARSCHUWING-regels, exitcode 0, bestand met 1 item (de nieuwe). De dagelijkse job zou dat committen en publiceren. Trigger: alleen bij een handmatig of toekomstig gewijzigde opslagnotatie; de huidige ronde schrijft JJJJ-MM-DD (95 items, geen waarschuwingen). Voorstel: items die om welke reden dan ook worden overgeslagen meetellen in het vangnet, of het vangnet dekt die reden ook.
2. BELANGRIJK, deels ontwerpvraag PO (extra test test_US022_extra_r5b_bronnaam_van_alle_items_gewijzigd_wist_niet_stil). Items van een bronnaam die niet exact in de config staat, verdwijnen vóór het vangnet. Reproduceren: 87 items met bron "Testfeed R5 oud", config-feednaam "Testfeed R5". Verwacht: geen stille wis (exitcode != 0 of minstens de helft blijft). Werkelijk: exitcode 0, 1 item over, en de log zegt "0 ouder dan 60 dagen verwijderd" zonder de werkelijke wis te melden. Een naamwijziging van één feed (10 van 87) gedraagt zich volgens US-019 c3 en is bekend (KLEIN, eerdere ronde). Wat hier BELANGRIJK maakt: een spatie in de naam van álle feeds wist vrijwel alles zonder enige melding. Ontwerpkeuze: items van niet-geconfigureerde bronnen verwijderen (US-019 c3). Bevinding: de logmelding is onjuist en het vangnet ziet deze wis niet.
3. BELANGRIJK (extra test test_US022_extra_r5c_bewaar_dagen_extreem_groot_geen_traceback). bewaar_dagen boven ca. 739.000 passeert de validatie (geheel getal >= 1) en geeft een OverflowError met traceback, exitcode 1 (bijv. 1000000 of 10^9). README zegt: geheel getal van minimaal 1, anders exitcode 2. Verwacht: exitcode 2 met Nederlandse melding of geen traceback. Geen dataverlies; de run faalt wel.
4. BELANGRIJK (extra tests test_US022_extra_r5d_* en r5e_*). Opgeslagen item met samenvatting als getal (5) geeft AttributeError; item met bron als lijst geeft TypeError. Beide: traceback, exitcode 1, bestand ongewijzigd (crash vóór het schrijven). Verwacht: geen traceback (overslaan met waarschuwing zoals bij ongeldige datum). Dagelijkse job faalt tot handmatige correctie.
5. BELANGRIJK (extra test test_US022_extra_r5f_*). Ongeldige regex in weigertermen (bijv. "re:([") passeert controleer_config en geeft re.error met traceback, exitcode 1, data ongewijzigd. Verwacht: exitcode 2 met Nederlandse melding; regex vooraf valideren.
6. KLEIN. Opgeslagen item met id als getal (5) wordt overgeslagen met waarschuwing, terwijl link, titel en datum geldig zijn en een ontbrekend id wel hersteld wordt. Niet getest (KLEIN).
7. KLEIN (r4 bevinding 4, ongewijzigd). Items zonder bron of met een bron die geen tekst is, verdwijnen stil met exitcode 0 (alleen bij handmatig bewerkt bestand).
8. KLEIN. Configwaarden timeout_seconden of max_samenvatting als tekst worden niet gevalideerd. Bij max_samenvatting "300" krijgen nieuwe items geen fout: de feed meldt OK met "zonder titel/link overgeslagen" en 0 bewaard. Gemeten in een in-proces probe, niet via de CLI.
9. KLEIN, ontwerpkeuze ter kennis (PO). De 50%-grens vangt een typo als 14 wél (52%), maar 30 niet: op de echte kopie verdwijnen dan 21 van 95 items (22%) met exitcode 0. Gemeten: bewaar_dagen 45 = 10 weg; 30 = 21 weg; 14 = 49 weg (STOP); 6 = 68 weg (STOP).
10. Ontwerpkeuzes (geen bevinding): ongeldige datum/link/titel van opgeslagen items overslaan met waarschuwing (spec); --forceer-opruimen wist bij een trefwoordtypo alles met exitcode 0 (bedoeld); BOM in het opslagbestand wordt geweigerd (r4 bevinding 8, KLEIN).
11. Ter kennis, ongewijzigd: r4 bevinding 5 (twee gelijktijdige runs, KLEIN) en bevinding 6 (feed hernoemen laat items verdwijnen, KLEIN).
12. OPERATIONEEL (niet door mij gestart, dus niet gestopt): drie python-processen uit eerdere rondes draaien nog: PID 34772 (127.0.0.1:8000), PID 43088 (0.0.0.0:8080, bereikbaar via het netwerk), PID 44480 (zonder poort). Stef of de orchestrator moet controleren en stoppen. Mijn eigen headless Edge-processen zijn afgesloten.
13. Let op voor de orchestrator: bevinding 1 is qua mechanisme dezelfde klasse als r4 bevinding 1 (vangnet-gat), met een andere trigger. Dat kan onder de noodremregel "dezelfde bevinding in 2 opeenvolgende rondes" vallen; de beslissing is aan Stef.

NIET GETEST (en telt niet als geslaagd):
- Snel klikken, terugnavigeren, herladen, toetsenbord-Tab en browserconsole in een echte interactieve sessie: NIET GETEST (geen interactieve browser; alleen headless screenshots en de geautomatiseerde browsertests).
- Definitieve visuele beoordeling: indicatief via screenshots (1280 en 375 px in iframe) beoordeeld, geen fouten zichtbaar; tekstuele opmerkingen: enkele titels beginnen met een kleine "ai" (bron), en Engelse titels in Vaknieuws (bekend, US-014). Het oordeel over de stijl blijft aan Stef.
- US-013 c1 en c3 (live site en GitHub-run): NIET GETEST.
- De dagelijkse GitHub-job zelf: NIET GETEST (alleen de workflow-inhoud gecontroleerd via de suite).
- Samenloop van twee echte runs (r4 bevinding 5): NIET GETEST.

BENODIGD VAN BOUWER:
- BLOKKEREND (bevinding 1): het vangnet moet ook items meetellen die om datum, link, titel of bronnaam worden overgeslagen (of de vangnet-regel uitbreiden zoals de PO beslist). Daarna test_US022_extra_r5a_* en r5b groen.
- BELANGRIJK (bevindingen 3-5): bewaar_dagen boven de datumgrens, samenvatting/bron van het verkeerde type en de ongeldige regex: geen traceback meer. Daarna r5c-r5f groen.
- PO: beslissing over bevinding 2 (bronnaam-wis, en de logmelding), bevinding 9 en de noodremvraag (bevinding 13).
- Stef of orchestrator: processen 34772, 43088 en 44480 controleren en stoppen (bevinding 12).

BESTANDEN GEWIJZIGD DOOR MIJ:
- tests/acceptance/test_US022_ronde5_dataverlies.py (nieuw; 6 extra tests, alle 6 rood: r5a, r5b, r5c, r5d, r5e, r5f)
- tests/acceptance/README.md (tabel "Iteratie 8, Tester ronde 5" toegevoegd)
- docs/test-reports/iteratie-8-ronde-5.md (dit rapport)
Tijdelijke bestanden (kopie van data en config, logs, screenshots, probe-scripts): alleen in de tijdelijke map van het systeem, buiten de projectmap.
