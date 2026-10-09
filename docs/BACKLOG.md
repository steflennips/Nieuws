# Backlog

Beheerd door de Product Owner. Statussen: `TODO` | `IN-ITERATIE` | `GEACCEPTEERD` | `AFGEWEZEN`.
Prioriteit: `MUST` | `SHOULD` | `COULD`.

## Formaat van een story
```
### US-001 Titel
- Prioriteit: MUST
- Status: TODO
- Fase: 1
- Als <gebruiker> wil ik <doel> zodat <reden>.
- Acceptatiecriteria:
  1. Gegeven <situatie>, als <actie>, dan <toetsbaar resultaat>.
  2. ...
- Opmerkingen: <optioneel>
```

## Stories

### US-001 Applicatieraamwerk, navigatie en voorbeelddata
- Prioriteit: MUST
- Status: GEACCEPTEERD (iteratie 1)
- Fase: 1
- Als teamlid wil ik een lokaal te starten website met duidelijke navigatie zodat ik snel tussen Overzicht, Nieuws en Leads kan wisselen.
- Acceptatiecriteria:
  1. Gegeven de README, als de app volgens de instructies gestart wordt, dan opent de startpagina in de browser zonder foutmelding.
  2. Gegeven een willekeurige pagina, als ik kijk naar de navigatie, dan zijn precies de items Overzicht, Nieuws en Leads zichtbaar en elk leidt naar het juiste scherm.
  3. Gegeven de app, als ik de actieve pagina bekijk, dan is het huidige menu-item visueel gemarkeerd.
  4. Gegeven de voorbeelddata, als ik die inspecteer, dan bevat die minimaal 15 nieuwsitems (minstens 4 per categorie Data, Automatisering, AI) en minimaal 10 leads (minstens 2 per status Nieuw, In behandeling, Niet interessant), allemaal met verzonnen gegevens.
  5. Gegeven de interface, als ik de teksten lees, dan zijn alle labels en knoppen in het Nederlands.
  6. Gegeven een smal scherm (breedte 375 px) en een breed scherm (1280 px), als ik de pagina's open, dan is de inhoud leesbaar zonder horizontaal scrollen.
- Opmerkingen: techniek volgens aanname in VISION.md. README moet startinstructie bevatten.

### US-002 Nieuwsoverzicht met filter en zoeken
- Prioriteit: MUST
- Status: GEACCEPTEERD (iteratie 1)
- Fase: 1
- Als teamlid wil ik nieuws over data, automatisering en AI kunnen filteren en doorzoeken zodat ik snel het relevante nieuws vind.
- Acceptatiecriteria:
  1. Gegeven het scherm Nieuws, als ik het open, dan zie ik alle nieuwsitems nieuwste eerst, met per item titel, categorie, bronnaam, datum en korte samenvatting.
  2. Gegeven het scherm Nieuws, als ik een categorie kies (Data, Automatisering of AI), dan zie ik alleen items van die categorie en klopt het getoonde aantal.
  3. Gegeven een actief categoriefilter, als ik "Alle" kies, dan zie ik weer alle items.
  4. Gegeven het scherm Nieuws, als ik een zoekterm invul die in een titel of samenvatting voorkomt, dan zie ik alleen de items die de term bevatten (hoofdletterongevoelig).
  5. Gegeven een zoekterm of combinatie met filter zonder resultaat, als ik zoek, dan zie ik de melding "Geen nieuws gevonden" en geen foutmelding.
  6. Gegeven een nieuwsitem, als ik op de titel klik, dan opent de bronlink (voorbeeldlink) in een nieuw tabblad.
- Opmerkingen: bronlinks zijn in fase 1 voorbeeldlinks.

### US-003 Leadsoverzicht met statusfilter
- Prioriteit: MUST
- Status: GEACCEPTEERD (iteratie 1); vervalt zodra US-012 klaar is
- Fase: 1
- Als teamlid wil ik een overzicht van leads met bron en status zodat ik zie welke kansen er liggen en wat opvolging verdient.
- Acceptatiecriteria:
  1. Gegeven het scherm Leads, als ik het open, dan zie ik alle leads met per lead bedrijfsnaam, korte omschrijving, branche, bron (naam van een gratis website), datum gevonden en status.
  2. Gegeven het scherm Leads, als ik een status kies (Nieuw, In behandeling, Niet interessant), dan zie ik alleen leads met die status en klopt het getoonde aantal.
  3. Gegeven een actief statusfilter, als ik "Alle" kies, dan zie ik weer alle leads.
  4. Gegeven een statusfilter zonder resultaat, als ik dat kies, dan zie ik de melding "Geen leads gevonden".
  5. Gegeven een lead, als ik de pagina bekijk, dan is de status visueel te onderscheiden (bijv. kleur of label) per status.
  6. Gegeven de voorbeelddata, als ik de leads inspecteer, dan bevatten ze alleen bedrijfsgegevens en geen persoonsnamen, e-mailadressen of telefoonnummers.
- Opmerkingen: status wijzigen valt buiten deze story (zie US-005). Bron is in fase 1 verzonnen; later alleen gratis bronnen.

### US-004 Overzichtspagina (startpagina)
- Prioriteit: MUST
- Status: GEACCEPTEERD (iteratie 2)
- Fase: 1
- Als teamlid wil ik op de startpagina in een oogopslag de nieuwste nieuwsitems en leads zien zodat ik daar mijn dag mee kan starten.
- Acceptatiecriteria:
  1. Gegeven de startpagina, als ik die open, dan zie ik de 5 nieuwste nieuwsitems (titel, categorie, datum) en de 5 nieuwste leads (bedrijf, status, datum).
  2. Gegeven de startpagina, als ik de blokken bekijk, dan toont elk blok het totaalaantal items (nieuws, leads) en een link "Alles bekijken" naar het juiste scherm.
  3. Gegeven de startpagina, als ik de teller "Nieuwe leads" bekijk, dan klopt die met het aantal leads met status Nieuw in de data.
  4. Gegeven een item op de startpagina, als ik erop klik, dan kom ik bij de bronlink (nieuws) of op het leadsscherm (lead).
- Opmerkingen: volgt op US-001 tot US-003.

### US-005 Leadstatus wijzigen
- Prioriteit: SHOULD
- Status: TODO (geparkeerd: leads buiten scope fase 2, besluit 2026-10-08-fase2-intake)
- Fase: 1
- Als teamlid wil ik de status van een lead aanpassen zodat het team ziet wie opgevolgd wordt.
- Acceptatiecriteria:
  1. Gegeven een lead, als ik een andere status kies, dan wordt de nieuwe status direct getoond.
  2. Gegeven een gewijzigde status, als ik de pagina ververs, dan blijft de status behouden gedurende de sessie van de app (lokale opslag is toegestaan).
  3. Gegeven een gewijzigde status, als ik het statusfilter en de teller op de startpagina bekijk, dan kloppen die met de nieuwe status.
- Opmerkingen: meerdere gebruikers tegelijk en wie wijzigde: fase 2.

### US-006 Nieuws markeren als relevant
- Prioriteit: COULD
- Status: TODO (geparkeerd: markeren per gebruiker kan niet op openbare site zonder login)
- Fase: 1
- Als teamlid wil ik nieuwsitems kunnen markeren zodat ik belangrijke artikelen terugvind.
- Acceptatiecriteria:
  1. Gegeven een nieuwsitem, als ik op de markeerknop klik, dan is het item zichtbaar gemarkeerd en kan ik de markering weer ongedaan maken.
  2. Gegeven gemarkeerde items, als ik filter op "Gemarkeerd", dan zie ik alleen die items.
- Opmerkingen: nog niet inplannen; eerst Stef-feedback na iteratie 1.

### US-007 Kleine technische nettheid
- Prioriteit: COULD
- Status: GEACCEPTEERD (iteratie 2)
- Fase: 1
- Als teamlid wil ik geen onnodige fouten of verwarrende filterresultaten zodat de app betrouwbaar aanvoelt.
- Acceptatiecriteria:
  1. Gegeven de draaiende app, als de browser /favicon.ico opvraagt, dan is het antwoord geen 404 (icoon of leeg antwoord 204) en verschijnt er geen fout in het serverlog.
  2. Gegeven het scherm Nieuws of Leads, als de filterparameter in kleine letters wordt meegegeven (bijv. categorie=ai), dan wordt hetzelfde filter toegepast als bij de juiste schrijfwijze.
  3. Gegeven een onbekende filterwaarde in de URL, als ik de pagina open, dan zie ik alle items en is "Alle" als actief filter gemarkeerd, zonder foutmelding.
- Opmerkingen: komt voort uit testbevindingen iteratie 1 (alle KLEIN). HEAD/POST 501 bewust niet opgepakt: niet relevant in fase 1.

### US-008 Visuele stijl en huisstijl
- Prioriteit: MUST
- Status: GEACCEPTEERD (iteratie 2, na fixrondes)
- Fase: 1
- Als teamlid wil ik een verzorgde, rustige en zakelijke uitstraling zodat de site prettig is om dagelijks te gebruiken.
- Acceptatiecriteria:
  1. Gegeven de stylesheet, als ik die inspecteer, dan zijn de kleuren uit VISION.md (`#1F2A44`, `#FFFFFF`, `#F7F8FA`, `#E3E6EB`, `#5B6475`, accent `#0F766E`) op één plek gedefinieerd (bijv. CSS-variabelen) en komen er buiten de statuslabel-tinten geen andere kleuren voor.
  2. Gegeven een willekeurige pagina, als ik die bekijk, dan is de koptekst/navigatie donkerblauw `#1F2A44`, de paginaachtergrond `#F7F8FA` en staat de inhoud op witte kaarten met rand `#E3E6EB`.
  3. Gegeven links, het actieve menu-item, het actieve filter en knoppen, als ik die bekijk, dan gebruiken ze de accentkleur `#0F766E`; de accentkleur komt nergens anders voor.
  4. Gegeven de stylesheet, als ik het lettertype controleer, dan is dat de systeemfontstack uit VISION.md en worden er geen externe fonts of externe bestanden geladen.
  5. Gegeven alle tekst/achtergrond-combinaties, als ik het contrast meet, dan is dat minimaal 4,5:1 (WCAG AA) voor normale tekst.
  6. Gegeven Nieuws en Leads, als ik die open, dan staan daar geen tellertegels; tellertegels staan alleen op de startpagina.
  7. Gegeven alle interfaceteksten, als ik die lees, dan wordt de gebruiker aangesproken met je/jij en komen de losse woorden "u" en "uw" niet voor.
  8. Gegeven breedte 1280 px, als ik een pagina open, dan is de inhoud gecentreerd met een maximale breedte tussen 960 en 1200 px; gegeven breedte 375 px is alles leesbaar zonder horizontaal scrollen, staat de navigatie volledig in beeld en staan kaarten onder elkaar.
- Opmerkingen: geen Deux2qonnect-huisstijl/logo in fase 1. Tester controleert kleuren en contrast via de broncode/stylesheet; Stef beoordeelt het totaalbeeld.

## Fase 2 (besluit: docs/decisions/2026-10-08-fase2-intake.md)
Regressie fase 1: US-002, US-007 en US-008 blijven gelden (de techniek mag wijzigen, het gedrag niet; filteren via URL-parameter mag client-side). Vervallen: US-001 c4 nieuwsdeel zodra US-009 klaar is; US-003 en de lead-delen van US-001 c2/c4 en US-004 c1-c4 zodra US-012 klaar is (nav wordt Overzicht, Nieuws). Tests mogen het internet niet nodig hebben: gebruik lokale testfeeds.

### US-009 Echte nieuwsfeeds ophalen en opslaan
- Prioriteit: MUST
- Status: GEACCEPTEERD (iteratie 3)
- Fase: 2
- Als bezoeker wil ik echt, actueel nieuws zien in plaats van voorbeelddata zodat de site echt nuttig is.
- Acceptatiecriteria:
  1. Gegeven het configuratiebestand met feeds, als ik dat inspecteer, dan bevat het 8 tot 10 feeds (minstens 3 Nederlands, 3 Engels) met per feed naam, URL en taal, volgens docs/decisions/2026-10-08-nieuwsfeeds.md of gemelde vervanger.
  2. Gegeven een RSS 2.0- en een Atom-testfeed, als het ophaalcommando (gedocumenteerd in de README) draait, dan worden per item titel, samenvatting, publicatiedatum, bronnaam, taal en link opgeslagen in een JSON-bestand.
  3. Gegeven een feeditem met HTML, afbeeldingen of volledige artikeltekst, als het wordt opgeslagen, dan is de samenvatting platte tekst van maximaal 300 tekens (afgekapt met "...") en worden geen afbeeldingen of volledige artikelinhoud opgeslagen.
  4. Gegeven een item dat al opgeslagen is (zelfde link), als het ophalen opnieuw draait, dan staat het item er maar één keer in.
  5. Gegeven opgeslagen items ouder dan 60 dagen, als het ophalen draait, dan worden die verwijderd.
  6. Gegeven de app na het ophalen, als ik Nieuws open, dan zie ik de opgeslagen echte items in plaats van de voorbeeldnieuwsitems, nieuwste eerst, met werkende link naar het origineel.
  7. Gegeven een echte ophaalronde door de Bouwer, als die klaar is, dan meldt de Bouwer per feed het aantal opgehaalde items (bewijs dat minimaal 6 feeds werken).
- Opmerkingen: alleen Python-standaardbibliotheek tenzij de Bouwer een gratis bibliotheek motiveert. Leads blijven deze iteratie ongewijzigd.

### US-010 Categorie automatisch toewijzen
- Prioriteit: MUST
- Status: GEACCEPTEERD (iteratie 3)
- Fase: 2
- Als bezoeker wil ik dat elk nieuwsitem in de juiste categorie staat zodat het filter Data/Automatisering/AI blijft werken met echte data.
- Acceptatiecriteria:
  1. Gegeven het configuratiebestand, als ik dat inspecteer, dan staan er per categorie (Data, Automatisering, AI) trefwoorden in het Nederlands en Engels.
  2. Gegeven een item met trefwoorden van één categorie in titel of samenvatting, als het wordt verwerkt, dan krijgt het die categorie (hoofdletterongevoelig, hele woorden: "AI" matcht niet in "mail").
  3. Gegeven een item met trefwoorden van meerdere categorieen, als het wordt verwerkt, dan krijgt het de categorie met de meeste treffers; bij gelijkspel geldt de volgorde AI, Automatisering, Data.
  4. Gegeven een item zonder enkele treffer, als het wordt verwerkt, dan wordt het niet opgeslagen en niet getoond.
  5. Gegeven een testset van minimaal 10 vaste voorbeeldtitels met verwachte categorie, als de tests draaien, dan krijgt elk de verwachte categorie.

### US-011 Foutafhandeling bij uitgevallen feed
- Prioriteit: MUST
- Status: GEACCEPTEERD (iteratie 3)
- Fase: 2
- Als bezoeker wil ik dat de site blijft werken als een nieuwsbron uitvalt zodat ik altijd nieuws zie.
- Acceptatiecriteria:
  1. Gegeven een feed die niet bereikbaar is, een time-out geeft (na maximaal 15 seconden) of ongeldige XML levert, als het ophalen draait, dan worden de overige feeds gewoon verwerkt.
  2. Gegeven een mislukte feed, als het ophalen klaar is, dan blijven de eerder opgeslagen items van die feed staan.
  3. Gegeven een mislukte feed, als het ophalen klaar is, dan staat in de uitvoer per feed "OK" of "FOUT" met korte reden.
  4. Gegeven dat alle feeds mislukken, als het ophalen klaar is, dan blijft het bestaande JSON-bestand ongewijzigd en eindigt het commando met een foutcode (niet 0); bij minstens één geslaagde feed is de foutcode 0.
  5. Gegeven een item zonder datum of zonder titel, als het wordt verwerkt, dan wordt een item zonder titel overgeslagen en krijgt een item zonder datum de ophaaldatum, zonder dat het ophalen stopt.

### US-012 Openbare nieuwssite zonder leads, met bronvermelding
- Prioriteit: MUST
- Status: GEACCEPTEERD (iteratie 4)
- Fase: 2
- Als bezoeker wil ik een openbare nieuwssite met duidelijke bronvermelding zodat ik betrouwbaar nieuws vind en rechthebbenden erkend worden.
- Acceptatiecriteria:
  1. Gegeven het bouwcommando (README), als het draait, dan ontstaat een map met statische HTML/CSS/JS-bestanden die zonder server-code werkt (te openen via een eenvoudige statische server).
  2. Gegeven de gegenereerde site, als ik de navigatie bekijk, dan zijn precies de items Overzicht en Nieuws zichtbaar; er is geen Leads-scherm.
  3. Gegeven alle gegenereerde bestanden, als ik die doorzoek, dan komen er geen leads, leadstatussen of verzonnen bedrijfsnamen uit de voorbeelddata in voor.
  4. Gegeven een nieuwsitem, als ik het bekijk, dan zie ik bronnaam, datum, samenvatting (max 300 tekens) en een link naar het origineel; er staan geen volledige artikelen of afbeeldingen van bronnen op de site.
  5. Gegeven elke pagina, als ik de voet bekijk, dan staat daar "Laatst bijgewerkt: <datum en tijd>" en de tekst dat koppen en samenvattingen afkomstig zijn van de genoemde bronnen, met link naar een lijst van alle bronnen.
  6. Gegeven de startpagina, als ik die open, dan zie ik tellertegels per categorie (Data, Automatisering, AI) en de 5 nieuwste items; de tellers kloppen met de data.
  7. Gegeven Nieuws, als ik filter op categorie of zoek, dan werkt dit zoals in US-002 c2-c5 en US-007 c2-c3.
  8. Gegeven Nieuws op 375 px, als ik het lege zoekveld bekijk, dan is de placeholdertekst volledig zichtbaar (niet afgekapt).
- Opmerkingen: regressie US-008 (stijl) en US-007 c1 (favicon geen 404) gelden voor de statische site; US-001 c3, c5, c6 ook. Filteren via URL-parameter mag client-side. De lokale app (src/app.py) met leads mag blijven bestaan maar valt buiten de gegenereerde site en buiten de regressie; US-001 c1 wordt vervangen door c1 hierboven.

### US-013 Online op gratis hosting met dagelijkse verversing
- Prioriteit: MUST
- Status: TODO. c2, c4, c5 geslaagd (it. 4 en it. 6 ronde 1-3); voorbereiding it. 5 geslaagd (.gitignore, veilig_check, workflow, README A-E, subpad, verse checkout). c1 en c3 open: publiceren na afronding US-020 (it. 8) en akkoord van Stef op het voorbeeld; daarna live-check door Tester.
- Fase: 2
- Als bezoeker wil ik de site op een vast internetadres vinden met elke dag nieuw nieuws zodat ik er dagelijks mee kan starten.
- Acceptatiecriteria:
  1. Gegeven het GitHub-account van Stef, als de site gepubliceerd is, dan is die bereikbaar via een https://...github.io/...-adres en laadt de startpagina zonder fout.
  2. Gegeven de geplande job, als ik de configuratie inspecteer, dan draait die dagelijks (rond 06:00 Nederlandse tijd) en is die ook handmatig te starten.
  3. Gegeven een run van de job, als die klaar is, dan toont de live site een bijgewerkte "Laatst bijgewerkt"-tijd.
  4. Gegeven de repository, als ik die doorzoek, dan bevat die geen wachtwoorden, tokens of sleutels.
  5. Gegeven de README, als Stef die volgt, dan staat erin hoe hij feeds toevoegt/verwijdert (met een letterlijke voorbeeldregel van een feed in config/feeds.json) en hoe hij de job handmatig start.
- Opmerkingen: vereist dat Stef een GitHub-account heeft en de repo openbaar zet (gratis plan). Online zetten (repo aanmaken, pushen, Pages aanzetten) is een handeling van Stef met README-stappen. Kiest Stef Netlify/Cloudflare, dan moeten c1 en het workflow-bestand worden aangepast (besluit vastleggen). c2 wordt in iteratie 4 getoetst via het workflow-bestand (cron in UTC die rond 06:00 NL-tijd valt, plus workflow_dispatch); de job draait het ophaal- en bouwcommando. Let op (PO, it. 4): de huidige git-root is je gebruikersmap (hele gebruikersmap); publiceren moet vanuit een eigen repo met alleen de projectmap. Data/nieuws.json moet tussen runs bewaard blijven (60 dagen, items van uitgevallen feeds).

### US-014 Taalfilter NL/EN
- Prioriteit: COULD
- Status: TODO
- Fase: 2
- Als bezoeker wil ik nieuws op taal kunnen filteren zodat ik alleen Nederlands of Engels nieuws zie.
- Acceptatiecriteria:
  1. Gegeven Nieuws, als ik "Nederlands" of "Engels" kies, dan zie ik alleen items van feeds met die taal en klopt het getoonde aantal.
  2. Gegeven een taalfilter, als ik ook een categorie kies, dan gelden beide filters tegelijk.

### US-015 Betere categorie-indeling
- Prioriteit: SHOULD
- Status: GEACCEPTEERD (iteratie 4); c12 feed-aandeel niet gehaald (AWS Big Data 83% van Data, n8n 67% van Automatisering), gemeld als open punt conform criterium. Vanaf it. 6: c12 vervangen door US-016 c6; in c10 verhuizen "business intelligence" en "Power BI" naar BI (testtitels via die termen verwachten BI).
- Fase: 2
- Als bezoeker wil ik dat items niet door een productnaam in de verkeerde categorie belanden en dat ook Automatisering zinvol gevuld is, zodat filteren echt helpt.
- Acceptatiecriteria:
  1. Gegeven het configuratiebestand, als ik dat inspecteer, dan staat er een lijst uitsluitingstermen (minstens "Data Master"); tekst die onder een uitsluitingsterm valt telt niet mee als trefwoordtreffer.
  2. Gegeven een item met titel "Firmware-update - Asustor ADM 5.1.4.RM62" en samenvatting "Asustor Data Master krijgt nieuwe functies", als het wordt verwerkt, dan krijgt het niet de categorie Data.
  3. Gegeven het configuratiebestand, als ik dat inspecteer, dan staan er per categorie minstens 15 trefwoorden, in het Nederlands en Engels.
  4. Gegeven een vaste testset van minstens 20 voorbeeldtitels (minstens 5 per categorie, waarvan minstens 3 echte titels uit een ophaalronde), als de tests draaien, dan krijgt elk de verwachte categorie.
  5. Gegeven een echte ophaalronde door de Bouwer, als die klaar is, dan meldt de Bouwer het aantal items per categorie (ter informatie; geen minimum, het hangt af van het nieuws).
  6. Gegeven de vaste testset, als de tests draaien, dan krijgen deze echte titels (met hun echte samenvatting uit de ronde van 8 okt) NIET de genoemde categorie: "Laptops met Nvidia RTX Spark-processor kosten in Nederland minstens 2999 euro" niet Data; "Instapversie Microsoft Surface-laptop met Nvidia RTX Spark-cpu kost 2600 dollar" niet Data; "Colt brengt SCION als managed netwerkdienst naar Europa" niet Data; "Uber Eats Rebuilds Search Pipeline..." niet Automatisering. En "Manage Amazon SageMaker HyperPod Spaces..." krijgt AI en niet Data.
  7. Gegeven config/feeds.json, als ik dat inspecteer, dan staan er minstens 2 gratis feeds (geen login) die vooral over automatisering, RPA, low-code of procesautomatisering gaan (nu: n8n Blog, Camunda Blog, Microsoft Power Platform Blog), en staan die ook in de bronnenlijst en in docs/decisions/2026-10-08-nieuwsfeeds.md. (Bijgewerkt it. 7.)
  8. Gegeven een echte ophaalronde door de Bouwer met de nieuwe feeds, als die klaar is, dan heeft Automatisering minstens 8 items en is het filter Automatisering op Nieuws niet leeg.
  9. Gegeven de vaste testset, als de tests draaien, dan krijgt "New Archestra's OpenAPPA Saturates Two Major Security Benchmarks with a 0% Attack Success Rate" (met echte samenvatting, bevat "workflows") NIET Automatisering; een los "workflow"/"workflows" telt niet als treffer, "workflow automation", "workflowautomatisering" en "workflow-automatisering" wel (elk met een testtitel).
  10. Gegeven het configuratiebestand, als ik dat inspecteer, dan bevat Data minstens 10 specifieke termen uit: dataset, data engineering, data lake, data warehouse/datawarehouse, SQL, analytics/data-analyse, ETL, business intelligence, Power BI, Databricks, Snowflake, dbt, pandas, datakwaliteit, data governance, datamodel (NL- en EN-vormen tellen als één term); en de vaste testset bevat minstens 5 extra titels die elk via een andere van deze termen Data krijgen.
  11. Gegeven config/feeds.json, als ik dat inspecteer, dan staat er minstens 1 gratis feed (geen login, robots.txt en voorwaarden staan het niet in de weg) die vooral over data-platforms, BI of analytics gaat (nu: Microsoft Fabric Blog, Power BI Blog, SQLBI), met nog steeds max. 10 feeds en min. 3 NL en 3 EN; ook in bronnenlijst en feedbesluit. Er wordt geen specifieke feed (zoals AWS Big Data Blog) getoetst. (Bijgewerkt it. 7.)
  12. Gegeven een echte ophaalronde door de Bouwer, als die klaar is, dan meldt de Bouwer per categorie het aantal en per categorie het aantal per feed; doel: Data >= 8, Automatisering >= 8, en geen enkele feed levert meer dan 60% van Data of van Automatisering. Niet gehaald met eerlijke feeds en termen: melden als open punt (zie besluit), niet oplossen met generieke trefwoorden.
- Opmerkingen: komt uit testbevinding it. 3 ronde 2 nr. 2 en it. 4 ronde 1 nr. 1 en 2, it. 4 ronde 2 nr. 1-3 (besluit docs/decisions/2026-10-08-categorie-fixronde2-it4.md). US-010 c1-c5 blijven gelden. Besluit: docs/decisions/2026-10-08-categorie-fixronde-it4.md (losse "spark", "data", "pipeline*" vervallen; trefwoorden niet verruimen om c8 te halen; Bouwer controleert robots.txt en voorwaarden van nieuwe feeds). c8 haalt de Bouwer niet door generieke trefwoorden toe te voegen; lukt c8 niet met eerlijke feeds, dan melden als open punt.

## Iteratie 6: mix, kwaliteit en headnieuws (besluit: docs/decisions/2026-10-08-mix-kwaliteit-uitgelicht.md)
Aanleiding: Stef: "veel te veel AI" (ca. 70-80%); hij wil headnieuws en nuttige info voor Deux (MKB/ZZP), ook BI en automatisering. Max. 10 feeds; ruilen naar BI-gerichte en algemene NL-bronnen mag (gratis, geen login, robots.txt gecontroleerd door de Bouwer).

### US-016 Evenwichtige mix met BI als eigen categorie
- Prioriteit: MUST
- Status: GEACCEPTEERD (iteratie 6, ronde 3); c6 meldpunt niet gehaald (Autom. 16,7%, AWS Big Data 73% van Data): opgepakt in US-019
- Fase: 2
- Als bezoeker van Deux wil ik vooral nieuws over BI, data en automatisering zien en AI alleen als het echt over AI gaat, zodat de site nuttig is voor het werk van Deux.
- Acceptatiecriteria:
  1. Gegeven het configuratiebestand, als ik dat inspecteer, dan zijn er precies 4 categorieen (BI, Data, Automatisering, AI), elk met minstens 15 trefwoorden in NL en EN; BI bevat minstens: Power BI, Microsoft Fabric, Qlik, Tableau, Looker, dashboard, rapportage, KPI, business intelligence; Data bevat minstens dbt en Snowflake; Automatisering bevat minstens n8n, Zapier, Power Automate en RPA.
  2. Gegeven items met trefwoordtreffers van meerdere categorieen, als ze worden verwerkt, dan wint de categorie met de meeste treffers en geldt bij gelijkspel de volgorde BI, Data, Automatisering, AI (vervangt de volgorde in US-010 c3); test met minstens 4 titels, waaronder een gelijkspel BI-AI dat BI wordt.
  3. Gegeven een item met een AI-trefwoord alleen in de samenvatting (niet in de titel), als het wordt verwerkt, dan telt die AI-treffer niet mee; heeft het geen andere treffer, dan wordt het niet getoond; test met minstens 2 titels.
  4. Gegeven een testdataset met 80 AI-items en 20 items van andere categorieen, als de site wordt gebouwd, dan bevat de site alle 20 overige items en precies de 13 nieuwste AI-items (AI hooguit 40% van alle getoonde items, naar beneden afgerond); Nieuws, tellertegels en Overzicht gebruiken alleen deze getoonde items.
  5. Gegeven config/feeds.json, als ik dat inspecteer, dan staan er max. 10 feeds, min. 3 NL en 3 EN, waarvan minstens 2 vooral over BI/analytics en minstens 2 algemene NL tech/business-bronnen; elke feed staat ook in de bronnenlijst en in docs/decisions/2026-10-08-nieuwsfeeds.md (met vermelding robots.txt gecontroleerd, gratis, geen login). Tests toetsen deze regels op de actuele config, niet op vaste feednamen; AWS Big Data Blog staat er niet in (US-019 c1). (Bijgewerkt it. 7.)
  6. Gegeven een echte ophaalronde door de Bouwer, als die klaar is, dan meldt de Bouwer per categorie het aantal getoonde items en het aandeel, en per categorie het aandeel per feed; doel (melden, niet hard getoetst): BI+Data >= 30%, Automatisering >= 20%, geen feed > 60% van een categorie. Niet gehaald met eerlijke feeds en termen: open punt, niet oplossen met generieke trefwoorden. (Vervangt US-015 c12.)
  7. Gegeven Overzicht en Nieuws op 375 en 1280 px, als ik die open, dan staan op Overzicht tellertegels voor BI, Data, Automatisering en AI en op Nieuws filterknoppen voor Alle, BI, Data, Automatisering en AI (geen tellertegels op Nieuws, US-008 c6), en werken filter en zoeken zoals in US-002 c2-c5 en US-007 c2-c3 (ook categorie=bi). (Verduidelijkt fixronde 1.)
  8. Gegeven het configuratiebestand, als ik dat inspecteer, dan is los "gegevens" geen Data-trefwoord (samenstellingen zoals gegevensanalyse, gegevensbeheer, gegevenskwaliteit mogen); en gegeven de 3 NOS-titels "Amsterdammer opgepakt in onderzoek naar hackerscollectief ShinyHunters", "Hackers persen klanten boodschappendienst Flink af: betalen of data gepubliceerd" en "Datalek bij reisapp Polarsteps: iedereen kon meekijken, ook met afgeschermde reizen" (met echte samenvatting), als ze worden verwerkt, dan krijgt geen ervan Data.
  9. Gegeven data/nieuws.json met een item met ongeldige datum (bijv. "garbage") naast geldige items, als de site wordt gebouwd, dan wordt dat item overgeslagen met een melding die titel of link noemt, worden de overige items getoond en is de exitcode 0.
  10. Gegeven data/nieuws.json met uitsluitend AI-items, als de site wordt gebouwd, dan eindigt de bouw met exitcode 1 en noemt de melding dat alle items AI zijn en door het AI-plafond (max 40%) niets overblijft (niet "bevat geen nieuwsitems").
  11. Gegeven `python src/bouw.py --vandaag 2026-13-45`, als de bouw start, dan is de melding Nederlands en noemt het verwachte formaat JJJJ-MM-DD, exitcode 1, geen traceback. (Fixronde 2.)
- Opmerking: c7 geldt alleen voor de statische site; de lokale app valt buiten regressie (besluit 2026-10-09-fixronde2-it6.md).

### US-017 Kwaliteitsfilter tegen productnieuws en marketing
- Prioriteit: MUST
- Status: GEACCEPTEERD (iteratie 6, ronde 3)
- Fase: 2
- Als bezoeker wil ik geen gadget-, deal- of promotieberichten zien zodat ik alleen zakelijk relevant nieuws lees.
- Acceptatiecriteria:
  1. Gegeven het configuratiebestand, als ik dat inspecteer, dan staat er een aanpasbare lijst weigertermen met minstens: webinar, webcast, sponsored, gesponsord, partnerbijdrage, advertorial, aanbieding, korting, kortingscode, deals, prijsverlaging, Black Friday, review, unboxing, hands-on, smartphone, game*, console.
  2. Gegeven een item met een weigerterm in de titel (hoofdletterongevoelig, hele woorden), als het wordt verwerkt, dan wordt het niet opgeslagen en niet getoond, ook als het trefwoordtreffers heeft.
  3. Gegeven een item met "sponsored", "gesponsord", "partnerbijdrage" of "advertorial" alleen in de samenvatting, als het wordt verwerkt, dan wordt het ook geweigerd.
  4. Gegeven een vaste testset van minstens 10 echte titels (minstens 5 te weigeren, minstens 5 toe te laten, waaronder een zakelijke overnametitel met het woord "deal" en een titel met "dealer"), als de tests draaien, dan klopt de uitkomst voor elk.
  5. Gegeven een echte ophaalronde door de Bouwer, als die klaar is, dan meldt de Bouwer per feed hoeveel items door het kwaliteitsfilter zijn geweigerd, met 3 voorbeeldtitels; het ophaallog telt per feed unieke nieuwe links (dubbele links binnen een feed tellen één keer).
  6. Gegeven het configuratiebestand, als ik dat inspecteer, dan bevat de aanpasbare weigerlijst (titel, hoofdletterongevoelig) ook evenement- en vendor-PR-patronen, minstens: "nog <getal of telwoord> (dagen|weken|maanden) tot", "save the date", "early bird", "tickets", "named a leader", "named a visionary", "recognized as a", "recognised as a", "magic quadrant", "forrester wave", "credits"; en de vaste testset weigert "Nog vier weken tot Emerce EDAY", "Camunda Named a Leader in The Forrester Wave: Adaptive Process Orchestration Software, Q3 2026", "Camunda Recognized as a Visionary in Gartner BOAT Magic Quadrant 2026" en "You can now top up your n8n Assistant credits", en laat toe: een overnametitel (bijv. "Salesforce neemt Informatica over"), "Power BI September 2026 Feature Summary", een Fabric-releasetitel met "generally available" en een titel met "Gartner" zonder deze patronen.
  7. Gegeven het configuratiebestand, als ik dat inspecteer, dan staat er een aanpasbare uitzonderingslijst voor de weigerlijst met minstens "operational review", "code review", "peer review", "security review", "analogy game", "game theory", "gamechanger"/"game changer"; tekst onder een uitzondering telt niet als weigerterm; de vaste testset laat "Run an automated operational review with the Amazon Redshift MCP server" en "Gemini, metadata and the analogy game" toe en weigert nog steeds een titel met los "review" (bijv. "Review: Samsung Galaxy S26") en een met "games".

### US-018 Headnieuws uitgelicht
- Prioriteit: MUST
- Status: GEACCEPTEERD (iteratie 6, ronde 3); c3 aangevuld door US-021 (alleen headnieuws, +1 NL)
- Fase: 2
- Als bezoeker wil ik bovenaan het belangrijkste nieuws van de dag zien en daaronder het vaknieuws, zodat ik in een minuut weet wat er speelt.
- Acceptatiecriteria:
  1. Gegeven config/feeds.json, als ik dat inspecteer, dan zijn minstens 2 algemene NL-feeds gemarkeerd als headnieuws en staat er een aanpasbare lijst Deux-relevantietermen met minstens: MKB, ZZP, Nederland, Nederlandse, overheid, gemeente, AVG, NIS2, AI Act, Microsoft, Power BI, Fabric, Qlik, Tableau, Looker, dbt, Snowflake, n8n, Zapier.
  2. Gegeven de startpagina, als ik die open, dan staat bovenaan (boven de tellertegels) een blok met de kop "Uitgelicht" met maximaal 5 items uit de laatste 3 dagen (per item titel met link, bron, datum, categorie), waarvan hooguit 2 AI.
  3. Gegeven de selectie, als die wordt gemaakt, dan geldt de scoreregel: 2 punten als het item uit een headnieuws-feed komt, plus 1 punt per verschillende relevantieterm in titel of samenvatting; hoogste score eerst, bij gelijke score nieuwste eerst; de regel staat in de README; test met minstens 6 voorbeeldtitels met vaste verwachte volgorde.
  4. Gegeven minder dan 5 geschikte items, als ik de startpagina open, dan toont het blok alleen de beschikbare items; bij 0 items staat er "Nog geen uitgelicht nieuws", zonder foutmelding.
  5. Gegeven de startpagina, als ik onder de tellertegels kijk, dan toont het blok vaknieuws de 5 nieuwste items die niet in Uitgelicht staan.
  6. Gegeven de startpagina op 375 en 1280 px, als ik die bekijk, dan is alles leesbaar zonder horizontaal scrollen en blijft US-008 gelden (de accentkleur alleen op de 4 toegestane plekken).
  7. Gegeven het configuratiebestand, als ik dat inspecteer, dan staat er een aanpasbare lijst evenementtermen (titel of samenvatting, hoofdletterongevoelig, hele woorden) met minstens: evenement, conferentie, congres, summit, "world forum", "meld je aan", aanmelden, inschrijven; een item met zo'n term komt niet in Uitgelicht of Vaknieuws maar blijft op Nieuws; test met de echte Techzine-titel "Begin bij het einde: zo maak je agentic remediation mogelijk" (met opgeslagen samenvatting: niet in Uitgelicht, wel op Nieuws) en minstens 1 gewoon nieuwsbericht dat wel in Uitgelicht kan. (Fixronde 2.)
  8. Gegeven de startpagina, als ik Vaknieuws bekijk, dan bevat het hooguit 2 AI-items (aangevuld met de volgende nieuwste niet-AI-items, anders minder dan 5); en een titel die begint met "Kort:" staat niet in Uitgelicht of Vaknieuws, wel op Nieuws; test met een dataset van minstens 6 AI-items en 1 "Kort:"-titel. (Fixronde 2.)

## Iteratie 7: feedruil, lokale app weg, Uitgelicht scherper (besluit: docs/decisions/2026-10-09-open-punten-a-d.md)

### US-019 AWS Big Data vervangen door automatiseringsfeed
- Prioriteit: MUST
- Status: GEACCEPTEERD (iteratie 7, ronde 1); meetpunten gehaald (Autom. 22,1%, BI+Data 43,0%); Data klein (5,8%, Fabric 60% van Data) = open punt
- Fase: 2
- Als bezoeker van Deux wil ik meer nieuws over (proces)automatisering en minder AWS-diepteartikelen zodat de mix past bij het werk van Deux.
- Acceptatiecriteria:
  1. Gegeven config/feeds.json, als ik dat inspecteer, dan staat AWS Big Data Blog er niet meer in en staat er minstens 1 nieuwe gratis feed die vooral over (proces)automatisering gaat (bij voorkeur NL); totaal max. 10 feeds, min. 3 NL en 3 EN, min. 2 BI/analytics-feeds en min. 2 algemene NL-feeds gemarkeerd als headnieuws.
  2. Gegeven de nieuwe feed, als ik bronnen.html en docs/decisions/2026-10-08-nieuwsfeeds.md bekijk, dan staat de feed in beide, met in het besluit: gratis, geen login, robots.txt gecontroleerd, en waarom deze kandidaat gekozen is (Bouwer noemt ook afgevallen kandidaten met reden).
  3. Gegeven data/nieuws.json met items van een bron die niet (meer) in config/feeds.json staat, als het ophalen draait, dan zijn die items verwijderd; items van een feed die wel in de config staat maar faalt blijven staan (US-011 c2 blijft gelden); test met een lokale testfeed.
  4. Gegeven een echte ophaalronde door de Bouwer, als die klaar is, dan levert de nieuwe feed minstens 1 item op en meldt de Bouwer per categorie aantal en aandeel en per categorie het aandeel per feed. Meetpunt (melden, niet hard getoetst): Automatisering >= 20%, BI+Data >= 30%, geen feed > 60% van een categorie; niet gehaald = open punt, niet oplossen met generieke trefwoorden.

### US-020 Lokale app verwijderen (alleen nieuws in de repo)
- Prioriteit: MUST
- Status: AFGEWEZEN (iteratie 7, ronde 1): c1 niet gehaald voor tests/ (3 vervallen, geskipte bestanden met "lead(s)" staan er nog; verwijderen vraagt akkoord Stef) en verzonnen bedrijfsnamen niet getoetst. c2-c4 OK. Afronden in iteratie 8.
- Fase: 2
- Als Stef wil ik dat de openbare repo alleen de nieuwssite bevat zodat er geen leads-restanten of verzonnen bedrijfsgegevens gepubliceerd worden.
- Acceptatiecriteria:
  1. Gegeven de projectmap, als ik die inspecteer, dan bestaan src/app.py, src/data.py en de leads-voorbeelddata niet meer, en bevat geen bestand in src/, tests/, config/ of README.md de hele woorden "lead" of "leads", of een leadstatus ("In behandeling", "Niet interessant"). (Deel "verzonnen bedrijfsnaam" vervallen, zie docs/decisions/2026-10-09-fixronde2-it8.md.)
  2. Gegeven src/, als ik die doorzoek, dan importeert geen bestand http.server of een verwijderd module (app, data) en bevat src/logica.py (als het blijft bestaan) alleen functies die ophalen, bouwen, mix of veilig_check gebruiken.
  3. Gegeven een verse checkout, als ophalen (met lokale testfeeds), bouwen, `src/veilig_check.py` en alle overgebleven unit- en acceptatietests draaien, dan slagen ze zonder ImportError en zonder internet.
  4. Gegeven de README, als ik die lees, dan staat er geen startinstructie voor de lokale app meer, wel: ophalen, bouwen, de gebouwde site lokaal bekijken met een eenvoudige statische server, feeds aanpassen en publiceren (US-013 c5 blijft gelden).
- Regressie na US-020 (Tester past tests hierop aan):
  - US-001: c1, c2, c4 vervallen; c3, c5, c6 toetsen op de statische site.
  - US-002: c1-c6 toetsen op de statische site (Nieuws); tests tegen de lokale app vervallen.
  - US-003 en US-004: vervallen geheel (startpagina valt onder US-012 c6 en US-018).
  - US-007: c1 favicon geen 404 via de statische server; c2/c3 alleen Nieuws (categorie=ai e.d.); leads-delen vervallen.
  - US-008: alle criteria op de statische site; c6 leest "Nieuws" (Leads vervalt).
  - US-009 c6: toetsen op de gebouwde site in plaats van de app.
  - US-012: opmerking "lokale app mag blijven bestaan" vervalt; c3 blijft (geen leads in gegenereerde bestanden).
  - US-005, US-006: blijven geparkeerd; bij heroppakken opnieuw uitwerken (er is geen lokale app meer).
  - Unittests die alleen app.py/data.py/lokale-app-logica testten vervallen; unittests van ophalen, bouw, mix en veilig_check blijven.

### US-021 Uitgelicht: alleen headnieuws, voorkeur Nederlands
- Prioriteit: MUST
- Status: GEACCEPTEERD (iteratie 7, ronde 1)
- Fase: 2
- Als bezoeker wil ik in Uitgelicht echt headnieuws zien, liefst Nederlands, en geen vendor-productblogs, zodat ik in een minuut weet wat er speelt.
- Acceptatiecriteria:
  1. Gegeven een dataset waarin een item uit een niet-headnieuws-feed (bijv. een Power BI-, Fabric-, n8n- of Camunda-blog) de hoogste relevantiescore heeft, als de site wordt gebouwd, dan staat dat item niet in Uitgelicht, wel op Nieuws, en in Vaknieuws als het daar volgens US-018 c5/c8 bij de 5 nieuwste hoort.
  2. Gegeven de selectie voor Uitgelicht, als die wordt gemaakt, dan komen alleen items uit feeds gemarkeerd als headnieuws in aanmerking en geldt de scoreregel van US-018 c3 plus 1 punt als de feed taal "nl" heeft; hoogste score eerst, bij gelijke score nieuwste eerst; de README beschrijft de nieuwe regel; test met minstens 6 voorbeeldtitels met vaste verwachte volgorde, waaronder een NL- en een EN-headnieuwsitem (testconfig) met verder gelijke score waarbij NL eerst komt.
  3. Gegeven een dataset met 2 geschikte headnieuws-items in de laatste 3 dagen en minstens 10 recente items uit andere feeds, als de site wordt gebouwd, dan toont Uitgelicht precies die 2 items (geen aanvulling); bij 0 geschikte headnieuws-items staat er "Nog geen uitgelicht nieuws", zonder foutmelding, en toont Vaknieuws nog steeds items volgens US-018 c5/c8.
  4. Gegeven Vaknieuws, als ik dat bekijk, dan is de selectie ongewijzigd ten opzichte van US-018 c5/c8 (geen taalvoorkeur in Vaknieuws).
- Opmerking: US-018 c1-c8 blijven gelden; c3 wordt aangevuld door c2 hierboven (headnieuws-filter en NL-punt).

## Iteratie 8: afwerking voor publicatie

### US-022 Kleine afwerking voor publicatie
- Prioriteit: SHOULD
- Status: TODO (voorstel it. 8, na go van Stef)
- Fase: 2
- Als bezoeker wil ik geen verwarrende tellers of half-Engelse foutmeldingen zodat de site en de commando's verzorgd overkomen.
- Acceptatiecriteria:
  1. Gegeven de startpagina, als ik de kop van het blok Vaknieuws bekijk, dan staat daar geen totaal van alle items (zoals "86 in totaal"); staat er een link naar Nieuws met een aantal, dan luidt die "Alle <n> berichten bekijken" met n = aantal items op Nieuws.
  2. Gegeven `python src/ophalen.py --config bestaat-niet.json`, als het commando draait, dan is de melding volledig Nederlands (noemt het pad, geen Engelse OS-tekst), exitcode 2, geen traceback; idem voor een onleesbaar (geen JSON) configbestand.
  3. Gegeven een config waarin trefwoorden niet precies de vier sleutels BI, Data, Automatisering en AI elk met een niet-lege lijst van niet-lege termen bevat (bijv. `{}`, sleutel "Ai", lege lijst, term ""), als ophalen draait, dan: exitcode 2, Nederlandse melding die de ontbrekende of foute categorie noemt, geen traceback, data/nieuws.json byte-gelijk.
  4. Gegeven data/nieuws.json met N items van bronnen die in de config staan, als de herindeling meer dan 50% van die N items zou verwijderen (items van niet-geconfigureerde bronnen tellen niet mee, US-019 c3), dan wordt het bestand niet geschreven, exitcode 1, Nederlandse melding met aantallen en de optie `--forceer-opruimen`; met `--forceer-opruimen` wordt wel geschreven (exitcode 0). Test met een lokale testfeed: 50% verwijderd = schrijven, 51% = weigeren.
  5. Gegeven een config met (a) UTF-8 met BOM: wordt normaal gelezen; (b) uitsluitingen, weigertermen of weiger_uitzonderingen geen lijst van tekst: exitcode 2; (c) een feed-url die niet met http:// of https:// begint (bijv. file:///): exitcode 2; (d) `"feeds": []`: exitcode 2 met melding "geen feeds ingesteld" (niet "alle feeds mislukt"). Bij (b)-(d): Nederlandse melding, geen traceback, data/nieuws.json ongewijzigd.
- Opmerking: bewust NIET in deze story: vendor-productnieuws van headnieuwssites in Uitgelicht, LUMC-categorie, kleine Data-categorie, Engelse titels (US-014). Eerst publiceren en Stefs oordeel op de live site.

## Planning
- Iteratie 7 beoordeeld (PO): US-019 en US-021 GEACCEPTEERD; US-020 AFGEWEZEN (alleen de 3 vervallen testbestanden + bedrijfsnamencheck via git-historie, commit 66e4d21 src/data.py). Voorstel it. 8 (klein): US-020 afronden + US-022. Daarna voorbeeld bij Stef, publiceren (README A-E), live-check US-013 c1/c3.
- Iteratie 7: US-019, US-020, US-021 (MUST). Daarna beoordeelt Stef het voorbeeld; pas na zijn akkoord publiceert hij (US-013 c1/c3), daarna live-check door de Tester. Daarna: US-014 (COULD).
- Iteratie 1: US-001, US-002, US-003. Alle drie GEACCEPTEERD.
- Iteratie 2: US-004, US-007 en US-008 GEACCEPTEERD. Fase 1 goedgekeurd door Stef.
- Iteratie 3: US-009, US-010, US-011 GEACCEPTEERD.
- Iteratie 4: US-012 en US-015 GEACCEPTEERD; US-013 c2/c4/c5 geslaagd (c1/c3 open).
- Iteratie 5: online zetten voorbereid (Bouwer klaar). Nog te doen: volledige test (regressie + README-stappen, .gitignore, `src/veilig_check.py` exitcode 0, workflow), daarna PO-beoordeling. US-013 blijft open tot c1/c3 live slagen; mag samen met de test van iteratie 6.
- Iteratie 6 fixronde 1 (besluit docs/decisions/2026-10-09-fixronde1-it6.md): US-008 c8 tegels 1 kolom op 375 px; US-016 c7 verduidelijkt, c8-c10 nieuw; US-017 c5 aangevuld, c6-c7 nieuw. Open punt voor Stefs inhoudsreview: AWS-diepteartikelen in Data en "Kort:"-digests.
- Iteratie 6 fixronde 2 (besluit docs/decisions/2026-10-09-fixronde2-it6.md): US-017 c5 geweigerd-telling unieke links (BLOKKEREND); US-018 c7 evenementen niet in Uitgelicht/Vaknieuws, c8 Vaknieuws max 2 AI en geen "Kort:"; US-016 c11 Nederlandse --vandaag-melding. Open voor Stef: AWS Big Data vervangen/extra Automatisering-feed (US-016 c6), lokale app uitfaseren, Engelse titels/listicles.
- Iteratie 5 + 6 beoordeeld (besluit 2026-10-09-beoordeling-it5-it6.md): US-016, US-017, US-018 GEACCEPTEERD; it. 5 voorbereiding geslaagd; US-013 c1/c3 open. Geen derde fixronde. Open voor Stef: A feedruil AWS Big Data/extra Automatisering, B lokale app uitfaseren, C Engelse titels (US-014/NL-voorkeur), D vendor-productnieuws in Uitgelicht. KLEIN later: Engels OS-deel in --config-foutmelding; LUMC-item in Automatisering.
- Iteratie 6: US-016, US-017, US-018 (MUST). Daarna kijkt Stef naar de inhoud; pas na zijn akkoord publiceren (US-013 c1/c3). Daarna: US-014 (COULD). Geparkeerd: US-005, US-006.
- KLEIN, naar later (it. 4 ronde 4): bronnen buiten config zonder link op bronnen.html; brede trefwoorden (integratie*, analyse); grens van de geheimenscan; feed-aandeel Data/Automatisering (US-015 c12) eventueel verbeteren met een extra eerlijke feed.
- KLEIN, naar later: GET //nieuws toont overzicht, HEAD/POST 501, dubbele statusparameter (vervallen met de statische site).
- Niet oppakken (PO, it. 3 bevinding 3): dubbele entiteit-decodering ("Tom &amp;amp; Jerry" -> "Tom & Jerry"). Veel feeds escapen dubbel (bijv. &amp;#8217;), de uitvoer wordt geescapet en de echte data bevat 0 tags; huidig gedrag is acceptabel.
