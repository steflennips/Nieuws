# 2026-10-08: Fixronde iteratie 4, categorie-indeling (besluit PO)

Aanleiding: testrapport iteratie 4 ronde 1, BELANGRIJK 1 en 2, KLEIN 3-6.

1. Verkeerde categorie door productnamen en generieke woorden (BELANGRIJK 1):
   - Losse generieke trefwoorden vervallen: "spark", "data" (los woord), "pipeline*". Alleen specifieke vormen tellen, zoals "Apache Spark", "data-analyse", "big data", "datawarehouse", "data pipeline", "CI/CD-pipeline".
   - "RTX Spark" en vergelijkbare productnamen komen in de uitsluitingslijst.
   - De categorie wordt niet "op titel gewogen" (te vaag om te toetsen); het probleem wordt opgelost met strakkere trefwoorden en uitsluitingen. Een rekenregel met gewichten mag de Bouwer gebruiken, maar is geen eis.
   - Testset uitgebreid met de vier foute echte titels (US-015 c6).
2. Scheve verdeling (BELANGRIJK 2): niet acceptabel als einddoel van de story. De feedlijst is een keuze van de PO (zie 2026-10-08-nieuwsfeeds.md); de Bouwer voegt 1 of 2 gratis feeds toe die vooral over automatisering/RPA/low-code/procesautomatisering gaan (US-015 c7, c8). Geen kosten, geen login, robots.txt en voorwaarden staan RSS-gebruik niet in de weg. Trefwoorden niet verruimen om het aantal te halen.
3. Cron 04:00 UTC (06:00 zomer, 05:00 winter) valt onder "rond 06:00" (US-013 c2). Geen wijziging.
4. KLEIN 4 (README voorbeeldregel feed toevoegen), KLEIN 5 (kortere placeholder zoekveld) en KLEIN 6 (eigen 404.html) gaan mee in de fixronde; KLEIN 4 en 5 als criterium (US-013 c5, US-012 c8).

Reden: de story belooft "niet door een productnaam in de verkeerde categorie" en "Automatisering zinvol gevuld"; beide zijn met de huidige uitvoer niet gehaald. Criteria zijn aangescherpt/toegevoegd, niet versoepeld.
