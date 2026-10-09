# 2026-10-08: Intake fase 2 (antwoorden Stef + keuzes PO)

1. Nieuws (Stef): NL + EN, startlijst van 8-10 gratis RSS-feeds, door PO gekozen, later aanpasbaar. Lijst in docs/decisions/2026-10-08-nieuwsfeeds.md.
2. Leads (Stef): "laat de leads eerst maar zitten. Ik wil een website voor al dat nieuws. De leads doen we later op een andere manier."
   Besluit PO: leads buiten scope fase 2. Het Leads-scherm, het leads-menu-item, de leadtellers en alle verzonnen leads verdwijnen van de openbare site (geen nepdata live). Daarmee vervallen US-003, US-005 en de lead-delen van US-001 c2/c4 en US-004 c1-c4 zodra US-012 is gebouwd.
   Voor later vastgelegd (VISION.md): leads uit Oost-Nederland, ook "kreten"/vacatures voor opdrachten data/AI/automatisering van 8-12 uur per week.
3. Hosting (Stef: "een gratis site"). Keuze PO, met bouweradvies: statische site op GitHub Pages, ververst door een dagelijkse GitHub Actions-job die de feeds ophaalt en de pagina's opnieuw genereert. Opslag als JSON-bestand in de repo (geen database nodig).
   Afwegingen: valt niet in slaap (statisch, sneller dan gratis PaaS zoals Render); gratis HTTPS. Nadelen: geen eigen domein (adres <account>.github.io/<repo>), servers in de VS (acceptabel: alleen openbaar nieuws, geen persoonsgegevens), repo moet openbaar zijn op het gratis plan (dus geen geheimen in de repo), geplande jobs kunnen enkele uren vertraagd zijn en GitHub zet ze uit na 60 dagen zonder repo-activiteit (de dagelijkse data-commit houdt de repo actief). Stef moet zelf een GitHub-account hebben/aanmaken.
4. Toegang (Stef): openbaar, geen login. Eis: alleen koppen, korte samenvattingen (max 300 tekens, platte tekst) en links met bronvermelding; geen volledige artikelen of afbeeldingen (auteursrecht); geen interne of lead-data.
