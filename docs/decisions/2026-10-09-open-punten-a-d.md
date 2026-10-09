# 2026-10-09 Open punten A-D (besluit Stef, uitgewerkt door PO)

Besluit:
- A. AWS Big Data Blog gaat eruit en wordt vervangen door een gratis feed over (proces)automatisering, bij voorkeur Nederlandstalig. De Bouwer zoekt kandidaten (feed werkt, geen login, robots.txt staat het toe). Meetpunt (niet hard getoetst): Automatisering >= 20%, geen feed > 60% van een categorie, BI+Data >= 30%. Max 10 feeds, min 2 BI-feeds, min 2 algemene NL-bronnen, min 3 NL/3 EN blijven gelden. Items van een bron die niet meer in config/feeds.json staat worden bij het ophalen verwijderd (PO-keuze, zodat de oude AWS-items niet 60 dagen blijven staan). -> US-019.
- B. De lokale app (src/app.py, src/data.py, lokale-app-delen van src/logica.py, leads-voorbeelddata, bijbehorende tests en README-delen) wordt verwijderd VOOR publicatie. De openbare repo gaat alleen over nieuws. Tests die alleen de lokale app testten vervallen of worden verplaatst naar de statische site (per criterium in BACKLOG, sectie "Regressie na US-020"). -> US-020.
- C. Voorkeur voor Nederlands in Uitgelicht: +1 punt voor items uit NL-feeds in de scoreregel van US-018 c3. Vaknieuws ongewijzigd. -> US-021.
- D. Uitgelicht alleen uit headnieuws-feeds. Productblogs (Fabric, Power BI, OutSystems, n8n, Camunda e.d.) blijven in Vaknieuws en op Nieuws. Te weinig headnieuws: minder dan 5 items tonen, geen aanvulling met productblogs (PO-keuze conform Stef). -> US-021.
- Publiceren (US-013 c1/c3) gebeurt pas NA iteratie 7 en na akkoord van Stef op het voorbeeld.

Reden: Stef wil een nieuwsrepo zonder leads-restanten, meer automatiseringsnieuws en een Uitgelicht-blok met echt (liefst Nederlands) headnieuws in plaats van Engels vendor-productnieuws.
