# Vision: POC app

> Status: fase 1 goedgekeurd door Stef op 2026-10-08. Intake fase 2 afgerond op 2026-10-08: openbare nieuwssite, leads geparkeerd (zie "Fase 2").

## Doel
Een interne website voor Deux2qonnect met op een plek (1) nuttig nieuws over data, automatisering en AI, en (2) leads (potentiele klanten/kansen). Succes: het team opent de site en ziet in een minuut wat relevant is en welke leads opvolging verdienen, zonder zelf rond te zoeken.

## Gebruikers
Klein intern team van 2 tot 10 personen met gelijke rechten (geen rollen). Gebruikt de site dagelijks als startpunt voor nieuws en lead-opvolging.

## Kernscenario's (fase 1, bewuste keuze PO: klein houden, 3 schermen)
1. Nieuws bekijken: team opent het nieuwsoverzicht, filtert op categorie (Data / Automatisering / AI) of zoekt op trefwoord, en opent de bronlink.
2. Leads bekijken: team opent het leadsoverzicht met bedrijf, korte omschrijving, bron en status (Nieuw / In behandeling / Niet interessant), en filtert op status.
3. Overzicht (startpagina): in een oogopslag de nieuwste nieuwsitems en nieuwste leads, met doorklik naar de twee lijsten.
Motivatie: dit is het minimum om de kernwaarde (nieuws + leads) te ervaren; bewerken, opslaan en echte koppelingen volgen later.

## Buiten scope (bewust niet, fase 1)
- Echte nieuws- of leadkoppelingen, scrapers, API's (alleen voorbeelddata).
- Inloggen, rollen, gebruikersbeheer.
- Betaalde databronnen of betaalde diensten voor leads (ook niet in fase 2).
- E-mailnotificaties, exports, CRM-koppeling, AI-samenvattingen.

## Stijl en uitstraling
Vastgelegd 2026-10-08 (antwoorden Stef, uitwerking PO; zie docs/decisions/2026-10-08-stijl.md).
- Look-and-feel: strak en zakelijk. Licht, veel wit, rustige kaarten (witte kaart, dunne lichte rand, kleine afronding, hooguit een subtiele schaduw). Tellertegels alleen op de startpagina.
- Voorbeelden die Stef mooi vindt: niet genoemd.
- Kleuren: neutraal donkerblauw/wit met één accentkleur. Nog geen Deux2qonnect-huisstijl (kan in een latere fase).
  - Donkerblauw (koptekst/navigatie, koppen): `#1F2A44`
  - Wit (kaarten): `#FFFFFF`; achtergrond pagina: `#F7F8FA`; randen: `#E3E6EB`
  - Tekst: `#1F2A44`; secundaire tekst: `#5B6475`
  - Accentkleur (keuze PO): teal `#0F766E`, alleen voor links, actief menu-item, actief filter en knoppen.
  - Statuslabels leads mogen eigen lichte tinten hebben (geen extra felle kleuren).
- Lettertype: systeemlettertype (`system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif`), geen externe fonts.
- Toon en taal: Nederlands, informeel (je/jij).
- Apparaten: desktop/laptop eerst (ontwerpbreedte 1280 px), telefoon (375 px) moet goed bruikbaar zijn.

## Fasering
- **Fase 1: prototype.** Mooi en werkend, met voorbeelddata, geen productie-koppelingen. Doel: Stef kan het ervaren en bijsturen.
- **Fase 2: in productie name (IPN).** De goedgekeurde app wordt geschikt gemaakt voor echt gebruik. De PO werkt dit uit zodra fase 1 is goedgekeurd en legt met Stef vast: waar de app draait (hosting), welke echte gegevens erin komen en wat dat voor de AVG betekent, wie toegang krijgt (inloggen, rollen), beveiliging, back-ups, monitoring, wie het beheert en hoe updates uitgerold worden. Hier horen ook de echte nieuws- en leadbronnen bij.

## Fase 2: openbare nieuwssite met echte data (intake afgerond 2026-10-08)
Wens Stef: "nu wil ik het met echte data hebben. En ook op een echte website." Besluiten: docs/decisions/2026-10-08-fase2-intake.md.
- Doel fase 2: een openbare, gratis website met dagelijks ververst echt nieuws over Data, Automatisering en AI (NL + EN).
- Bronnen: 8-10 gratis openbare RSS/Atom-feeds (lijst: docs/decisions/2026-10-08-nieuwsfeeds.md), later aanpasbaar via een configuratiebestand. Geen kosten, geen betaalde API's.
- Per item tonen: titel, korte samenvatting (platte tekst, max 300 tekens), datum, bronnaam en link naar het origineel. Geen volledige artikelen, geen afbeeldingen (auteursrecht).
- Categorie Data/Automatisering/AI automatisch op trefwoorden (NL + EN); items zonder treffer worden niet getoond.
- Hosting: statische site op GitHub Pages (gratis, HTTPS, adres <account>.github.io/<repo>, geen eigen domein). Dagelijkse GitHub Actions-job haalt feeds op, slaat op in een JSON-bestand en genereert de site. Servers in de VS; acceptabel omdat er alleen openbaar nieuws en geen persoonsgegevens op staan.
- Toegang: openbaar, geen login. Er staat geen interne data en geen lead-data op de site.
- Leads: buiten scope fase 2. Leads-scherm, menu-item, tellers en verzonnen leads verdwijnen van de site. De lokale fase-1-app met leads wordt voor publicatie uit de repo verwijderd (besluit 2026-10-09-open-punten-a-d.md).
- Uitgelicht: alleen headnieuws-feeds, voorkeur voor Nederlands; productblogs alleen in Vaknieuws en op Nieuws.
- Buiten scope fase 2: leads, login, eigen domein, database-server, e-mailnotificaties, CRM-koppeling, exports, AI-samenvattingen, markeren per gebruiker.
- Succescriteria fase 2: de site is online via HTTPS, toont echte items uit minimaal 6 feeds, ververst dagelijks zonder handwerk, een uitgevallen feed breekt de site niet, en Stef keurt het resultaat goed.

## Later (na fase 2, apart te besluiten)
- Leads "op een andere manier" (Stef): bedrijven in Oost-Nederland, en "kreten"/vacatures voor opdrachten data/AI/automatisering van 8-12 uur per week. Eerdere PO-aannames blijven gelden: alleen gratis bronnen die automatisch ophalen toestaan, alleen bedrijfsgegevens, AVG/koude-acquisitie laten toetsen. Leads horen niet op een openbare site (login of afgeschermde omgeving nodig).
- Eigen domein (Deux2qonnect), Deux2qonnect-huisstijl.

## Succescriteria fase 1
- Alle 3 schermen werken en zijn bereikbaar via navigatie, zonder foutmeldingen.
- Voorbeelddata: minimaal 15 nieuwsitems (alle 3 categorieen) en 10 leads (alle 3 statussen).
- Filteren op categorie/status en zoeken op nieuws werken aantoonbaar.
- Stef kan de app met de README in minder dan 5 minuten lokaal starten en bekijken.
- Stef keurt het uiterlijk en de opzet goed (of geeft bijsturing).

## Randvoorwaarden
- Techniek: aanname fase 1 is een eenvoudige lokale webapp met voorbeelddata (bijv. JSON/in-memory), zonder database-server, zonder externe koppelingen. De Bouwer adviseert na iteratie 1 een definitieve techniek; Stef beslist.
- Gegevens: alleen voorbeelddata in fase 1, geen echte bedrijfs- of persoonsgegevens, voorbeeldbedrijven zijn verzonnen.
- Leads: mogen later uitsluitend uit gratis bronnen komen (websites zonder kosten). Geen betaalde bronnen of abonnementen.
- Taal van de interface: Nederlands.

## Open punten
- Juridisch/AVG (fase 2, nog te beslissen): leads kunnen persoonsgegevens bevatten (namen, e-mail, telefoon). Te beantwoorden: rechtsgrond (gerechtvaardigd belang) en informatieplicht, dataminimalisatie (bij voorkeur alleen bedrijfsgegevens), bewaartermijn, voorwaarden/robots.txt van gratis bronnen (scrapen kan verboden zijn), en regels rond koude acquisitie (Telecommunicatiewet, e-mail/bellen). Advies: juridisch laten toetsen voor fase 2.
- Hosting besloten (GitHub Pages + Actions); Stef moet een GitHub-account hebben en de repo openbaar zetten (nodig voor US-013).
- Leadbronnen: later, zie "Later".
