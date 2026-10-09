# 2026-10-08: Techniek nieuws ophalen (Bouwer, iteratie 3)

- Alleen Python-standaardbibliotheek (urllib, xml.etree, html.parser, robotparser). Geen nieuwe afhankelijkheden.
- `src/ophalen.py` (CLI) + `config/feeds.json` (feeds, trefwoorden, bewaartermijn, time-out 15 s, User-Agent). Opslag: `data/nieuws.json`, atomisch geschreven; bij 0 geslaagde feeds niet geschreven en exitcode 1.
- Trefwoorden: hele woorden, `*` aan het eind = prefix. Score = aantal treffers in titel+samenvatting.
- Veiligheid: robots.txt wordt gelezen en gerespecteerd; XML met entity-declaraties wordt geweigerd (geen entity-expansie); max. 8 MB per feed.
- App leest `data/nieuws.json` met mtime-cache; ontbreekt het, dan voorbeelddata. `NIEUWS_BRON=voorbeeld` forceert voorbeelddata (regressietests).
- `data/nieuws.json` staat in .gitignore; of de online site het bestand in git zet (dagelijkse commit) beslist iteratie 4.
- Feedcontrole (2026-10-08): vervangen wegens fouten: VentureBeat AI (HTTP 429), AI News (levert HTML i.p.v. feed), AG Connect (levert HTML), Frankwatching (HTTP 403 voor een eerlijke bot-User-Agent; niet omzeild). Vervangers: AWS Machine Learning Blog (en), BigDATAwire/Datanami (en), Techzine (nl). Computable-URL naar /feed/ (redirect vermeden).
