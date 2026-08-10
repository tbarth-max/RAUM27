# Meilenstein 8: Rückprojektionsskala R_n = 2^n (deskriptiv, unverdrahtet)

Erweitert Meilenstein 7 um einen zweiten, **bewusst getrennten** Parameter
neben der Zustandsebene Ω=k².

## Zwei getrennte Operationen (wie festgelegt)

| Parameter | Bedeutung | Wirkung im Code |
|---|---|---|
| **Ω = k² = 9** | Zustandsebene (Basis-9-Neuner-Struktur) | skaliert das effektive SNR pro Schale, wie in Meilenstein 6/7 |
| **R_n = 2^n** | Rückprojektionsebene (n = Anzahl abgeschlossener Neunerzyklen) | wird nur **protokolliert**, fließt in keine Berechnung ein |

Kein gemeinsamer Faktor 9×2=18 — die beiden Skalen bleiben unabhängig
sichtbar in der Ergebnistabelle.

## Warum R_n noch nicht verdrahtet ist

Eine echte Überlagerung von "Hinweg"- und "Rückprojektions"-Welle ist eine
Superposition, deren Ergebnis von der **Phasenbeziehung** abhängt:

- gleichphasig: `A_ges = 2·A`
- gegenphasig: `A_ges = 0`

Ohne eine definierte Phase zwischen den beiden Wellen wäre jede
Verrechnung von R_n in SNR/Energie/Amplitude eine Annahme, die wir noch
nicht getroffen haben. Deshalb bleibt R_n bis auf Weiteres ein reiner
Kennwert in der Ausgabetabelle.

## Ergebnis

```
Ebene  Zaehlerstand  n   Omega^Ebene  R_n=2^n  SNR       BER
  -2      010        1    0.012346      2      0.049    21.2 %
  -1      020        2    0.111111      4      0.442     1.7 %
   0      030        3    1.000000      8      3.981     0.0 %
  +1      040        4    9.000000     16     35.830     0.0 %
  +2      050        5   81.000000     32    322.467     0.0 %
```

Die BER-Werte sind **identisch** zu Meilenstein 7 — Bestätigung, dass R_n
tatsächlich nirgends in die Simulation einfließt, wie vorgesehen.

## Ausführen

```
python3 milestones/08_retroprojektionsskala/run.py
```

CSV unter
`milestones/08_retroprojektionsskala/results/raum27_meilenstein8_retroprojektionsskala.csv`.

## Nächster Schritt (noch offen)

Bevor R_n irgendwo wirkt, muss die Phasenbeziehung zwischen der
ursprünglichen Welle und der Rückprojektions-Welle definiert werden —
erst dann lässt sich entscheiden, ob/wie R_n in RVAR, Amplitude oder
einen dritten, eigenen Kanal einfließt.
