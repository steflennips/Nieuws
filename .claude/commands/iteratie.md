---
description: Draai één volledige iteratie van het team (Product Owner, Bouwer, Tester) volgens het protocol in CLAUDE.md
---

Draai één iteratie van de loop zoals beschreven in `CLAUDE.md`.

Extra instructies van Stef (kan leeg zijn): $ARGUMENTS

Doe het volgende:
1. Lees `CLAUDE.md` en `docs/STATUS.md`.
2. Voer de stappen 1 t/m 8 uit. Gebruik de subagents `product-owner`, `builder` en `tester`. Schrijf zelf geen productcode.
3. Stel vragen van de PO aan Stef met AskUserQuestion.
4. Respecteer de noodremmen en de autonomie-instelling.
5. Sluit af met een korte samenvatting (max 10 regels) en vraag om go voor de volgende iteratie, tenzij de instelling anders zegt.
