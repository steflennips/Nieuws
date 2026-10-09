# 2026-10-09 Bouwkeuzes fixronde 1, iteratie 6
- Weigerpatronen met woordgroepen staan als gewone termen in `weigertermen`; "nog <getal/telwoord> dagen|weken|maanden tot" als regex met voorvoegsel `re:` (kleine uitbreiding van _patroon in ophalen.py, geen nieuwe afhankelijkheid).
- Uitzonderingen: `weiger_uitzonderingen` in config; die tekst wordt voor de weigercontrole uit titel (en samenvatting) gehaald.
- Tegels op 375 px: 1 kolom in bouw.py (breekpunt 720 px, daarboven 4 naast elkaar). De lokale app had al 1 kolom onder 720 px (3 tegels).
- AI-plafond-controle verhuisd van laad_items naar bouw(), zodat de melding "alleen AI" apart kan.
