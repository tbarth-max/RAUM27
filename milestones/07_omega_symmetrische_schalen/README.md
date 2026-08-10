# Meilenstein 7: Symmetrische Schalen (Ω und Ω⁻¹) + 6×8-Kopplungsversuch

Zwei getrennte Teile, mit unterschiedlichem Vertrauensgrad — bitte nicht
vermischen.

## Teil 1: Symmetrische Schalen — solide, funktioniert wie erwartet

Erweitert Meilenstein 6 um Ebenen **-2, -1, 0, +1, +2** (statt nur 0..2).
Negative Ebenen benutzen `Ω^Ebene < 1` (also `Ω⁻¹ = 1/9`, `Ω⁻² = 1/81`),
passend zur früher festgelegten Beziehung "Expansion k ↔ Brennpunkt 1/k".
Gemessenes Ergebnis:

| Ebene | Ω^Ebene | SNR (linear) | BER gesamt |
|---|---|---|---|
| -2 | 1/81 | 0,049 | 21,2 % |
| -1 | 1/9 | 0,442 | 1,7 % |
| 0 | 1 | 3,981 | 0 % |
| +1 | 9 | 35,8 | 0 % |
| +2 | 81 | 322,5 | 0 % |

Das ist die erwartete, falsifizierbare Konsequenz: Richtung Brennpunkt
(negative Ebenen) sinkt das effektive SNR, die Fehlerrate steigt messbar
an — symmetrisch zum bereits validierten Verhalten Richtung Expansion aus
Meilenstein 6. Kein neuer Mechanismus, reine Spiegelung der bestehenden
Logik auf negative Exponenten.

## Teil 2: 6×8-"Kräfteäquivalent" D — Versuch, mit offenem Ergebnis

Angefragt war eine 6×8- bzw. 8×6-Matrix als Verhältnis zwischen innerer
Rotation (6 Oktaeder-Richtungen) und äußerer Expansion (8 Würfelecken).
Gebaut: `D` (6×8) aus den 6 reinen Richtungs-Zeilen von `B` (ohne die
konstante erste Zeile), gleichzeitig in die GA- und GB-Spalten von `H`
eingebettet.

**Was numerisch tatsächlich rauskommt:**

- `D` hat **Rang 4, nicht 6** — die 6 Richtungen sind nicht unabhängig,
  weil sie aus derselben 4-dimensionalen Richtungsvorlage (`B`) stammen.
  Zwei Eigenwerte von `D·Dᵀ` sind exakt Null.
- Die vier von Null verschiedenen Eigenwerte sind `{2, 2, 2, 6}`.
- Verhältnis größter zu den übrigen: **6/2 = 3**, exakt euer `k`.

**Wichtige Einschränkung, damit hier nichts überinterpretiert wird:** `D`
ist rein aus `B`, `GA`, `GB` gebaut — an keiner Stelle geht `k` oder `Ω` in
diese Matrix ein. Dass der Eigenwert-Quotient zufällig `3` ergibt, ist mit
hoher Wahrscheinlichkeit **Zufall** (die Zahl 3 taucht in dieser
Cube-Oktaeder-Konstruktion mutmaßlich aus kombinatorischen Gründen auf,
unabhängig davon, welches `k` ihr für die Schalen-Skalierung wählt). Es
ist **kein Beleg**, dass "Rotation" und "Expansion" über diese Matrix
tatsächlich gekoppelt sind — dafür bräuchte es einen zweiten, unabhängigen
Fall mit anderem `k`, bei dem sich derselbe Zusammenhang zeigt. Das haben
wir nicht geprüft.

`D` wird im Skript nur als **beschreibender Kennwert** verwendet: pro
Schale die mittlere Norm der Zustandsprojektion `mean_a @ Dᵀ`
(„6×8-Readout"). Das ist eine reale, berechenbare Zahl, aber keine neue
Mechanik — sie beeinflusst die Bayes-Simulation nicht, sie beschreibt sie
nur zusätzlich.

## Ausführen

```
python3 milestones/07_omega_symmetrische_schalen/run.py
```

Gibt zuerst die D-Matrix-Diagnose aus, dann die Schalen-Tabelle. CSV unter
`milestones/07_omega_symmetrische_schalen/results/raum27_meilenstein7_symmetrische_schalen.csv`.

## Korrektur zur "Zufalls"-Einschätzung oben

Wichtig zu verstehen: `D` wird **ausschließlich** aus `B`, `GA`, `GB`
gebaut — der Parameter `k` taucht in `D` an keiner Stelle auf. Das
Eigenwert-Verhältnis 3 ist deshalb eine **feste geometrische Konstante**
dieser Cube-Oktaeder-Konstruktion, die sich niemals ändert, egal welches
`k` ihr für die Schalen-Skalierung wählt (auch bei k=2 oder k=5 bliebe der
Wert exakt 3). Ein Nachrechnen mit anderem `k` würde also nichts prüfen —
`D` reagiert darauf gar nicht. Die einzige echte "Übereinstimmung" ist,
dass ihr zufällig `k=3` gewählt habt, was zahlenmäßig mit dieser fixen
Konstante zusammenfällt. Es gibt in diesem Aufbau keinen Mechanismus, der
`k` und diese Konstante tatsächlich koppelt — dafür müsste `D` selbst von
`k` abhängen, tut es aber nicht. Ohne eine solche Kopplung ist "3 = 3"
hier Zahlenspiel, kein Beleg.

## Offene Fragen für eine echte Kraft-Kopplung

- Eine konkrete Definition, wie `k` (oder `Ω`) überhaupt in `D` einfließen
  soll — aktuell ist `D` komplett unabhängig von der Schalen-Skalierung.
  Ohne diese Kopplung bleibt „Kräfteäquivalent" ein Name ohne Mechanik.
- Eine konkrete Definition, was "Kräfteäquivalent" rechnerisch bedeuten
  soll (aktuell nur deskriptiv als Readout-Norm, keine Wirkung auf den
  Zustand).
