# 2026-10-08: Wijzigingen in de feedlijst (Bouwer, iteratie 3)

Samengevoegd en door de PO bevestigd in 2026-10-08-nieuwsfeeds.md (actuele lijst). Dit bestand blijft als historie.

Gecontroleerd op 2026-10-08 met de eigen User-Agent en robots.txt.
- VentureBeat AI: HTTP 429 (blokkeert de bot), vervangen door AWS Machine Learning Blog (EN).
- AI News (artificialintelligence-news.com): feed werkt nu wel (HTTP 200); is destijds vervangen door BigDATAwire (EN); niet teruggezet (8-10 feeds blijft gelden).
- AG Connect: /rss gaf 404 (ook /rss.xml), vervangen door Techzine (NL).
- Frankwatching: HTTP 403 voor de bot, vervangen door een NL-bron (zie Techzine/Computable).
- Tweakers: feedburner-URL leverde alleen items uit april 2025. Nu https://tweakers.net/feeds/mixed.xml (vers; robots.txt staat /feeds toe).
- Computable: URL /feed/ i.p.v. /rss.
Feeds-status in het JSON-bestand bevat nu per feed "bewaard" (na 60-dagenfilter) en "verouderd".
