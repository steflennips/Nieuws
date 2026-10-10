# Workflow: terugcommit van data/nieuws.json conflictvrij (2026-10-10)

Probleem: `git pull --rebase` gaf een merge-conflict op data/nieuws.json als er tussentijds was gepusht (GitHub Desktop); de job faalde.

Keuze: data/nieuws.json is gegenereerd, dus de job-versie wint. De stap kopieert het bestand opzij, doet `git fetch` + `git reset --hard origin/<branch>`, zet het bestand terug, commit en pusht (geen force). Maximaal 3 pogingen met korte pauze als de push wordt afgewezen. (Een rebase met `-X theirs` is verwarrend, want in een rebase is "theirs" de eigen commit; de reset-methode heeft geen merge en dus geen conflict.)

Publiceren: de site wordt gebouwd en geupload voor of los van de push. Mislukt de push na 3 pogingen, dan eindigt de stap met een zichtbare waarschuwing (`::warning` en samenvatting van de run) en wordt de site toch gepubliceerd; de volgende run probeert het opnieuw. Bewust gekozen: verse content online gaat voor opslag in de repo.
