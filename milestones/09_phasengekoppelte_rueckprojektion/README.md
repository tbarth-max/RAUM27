# Meilenstein 9: Phasengekoppelte Rückprojektion (J^n als Reflexions-Operator)

Verdrahtet die in Meilenstein 8 offen gelassene Phasenbeziehung.

## Die Regel

$$\varphi(n) = \pi \cdot (n \bmod 2), \quad \text{realisiert über } J^n$$

- n gerade → `J^n = I` → Gleichphase → Signalamplitude ×2
- n ungerade → `J^n = J` → Gegenphase → Signalamplitude ×0 (Auslöschung)

n = Anzahl abgeschlossener Basis-9-Neunerzyklen (`counter.level`). J ist
der im Duplex-Kern bereits vorhandene Involutions-Operator (`J·J = I`),
hier als Reflexions-Phasensprung zweckentfremdet — siehe Begründung im
vorherigen Gespräch.

**Wichtige Einschränkung:** Nur die *Parität* von n wirkt hier. Der
Betrag R_n = 2^n aus Meilenstein 8 bleibt weiterhin unverdrahtet.

## Ergebnis — ein deutlicher, überraschender Effekt

| Ebene | n | Phase | Amplitude | SNR (nominal) | BER |
|---|---|---|---|---|---|
| -2 | 1 | Gegenphase | ×0 | 0,049 | **50,6 %** |
| -1 | 2 | Gleichphase | ×2 | 0,442 | 1,0 % |
| 0 | 3 | Gegenphase | ×0 | 3,981 | **50,0 %** |
| +1 | 4 | Gleichphase | ×2 | 35,83 | 0,0 % |
| +2 | 5 | Gegenphase | ×0 | 81 → 322,5 | **50,9 %** |

**Der wichtige Befund:** Bei Gegenphase wird die BER exakt zum
Zufallsniveau (≈50 %) — **unabhängig davon, wie hoch Ω das nominelle SNR
treibt**. Bei Ebene +2 steht ein SNR von 322 auf dem Papier, aber die
tatsächliche Fehlerrate ist trotzdem Zufall, weil die Amplitude durch die
Auslöschung exakt null ist. Das ist keine Rundung oder ein kleiner Effekt
— die Phasenkopplung dominiert vollständig über die Ω-Skalierung, sobald
Gegenphase eintritt.

## Offene Frage, die das aufwirft

Mit dieser Reflexionsannahme (fest, π-Phasensprung bei jedem ungeraden
Zyklus) verliert das System **jede zweite Schale komplett** — dort kommt
strukturell keine Information durch, egal wie stark Ω verstärkt. Falls
das Ziel ein durchgehend funktionierender Mehrschalen-Übertragungsweg
ist, ist das vermutlich nicht das gewünschte Verhalten. Zwei
Möglichkeiten, falls das korrigiert werden soll:

1. Die Zuordnung umkehren (gerade ↔ ungerade), löst das Problem aber nur
   für die jeweils andere Hälfte der Schalen.
2. Von *vollständiger* Reflexion (Amplitude ×0 oder ×2) zu einer
   *partiellen* Reflexion übergehen (Reflexionskoeffizient r zwischen 0
   und 1, wie bei echten Wellenleitern mit Impedanzsprung statt starrer
   Wand) — dann verschwindet keine Schale vollständig, aber die
   "saubere" 0/2-Struktur aus der reinen Involution geht verloren.

Das ist eine echte Modellentscheidung, keine Rechenfrage — beide
Optionen sind mathematisch möglich, sie haben nur unterschiedliche
Konsequenzen für "funktioniert jede Schale" vs. "reine 2-Zustands-Physik
aus J".

## Ausführen

```
python3 milestones/09_phasengekoppelte_rueckprojektion/run.py
```

CSV unter
`milestones/09_phasengekoppelte_rueckprojektion/results/raum27_meilenstein9_phasengekoppelt.csv`.
