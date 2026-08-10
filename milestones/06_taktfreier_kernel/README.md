# Meilenstein 6: Taktfreier Scheduler

Die Notizen behaupten, ein "taktfreier Kernel" -- ein Scheduler, der
Prozesse nach Arbeitsaufwand statt nach festen Zeitscheiben laufen lässt
-- sei einem klassischen zeitgetakteten Scheduler grundsätzlich
überlegen. Dieser Meilenstein implementiert genau das (kein Pseudocode,
kein Konsolen-Mockup) und benchmarked es ehrlich gegen die
Standard-Baseline, statt die Behauptung nur zu wiederholen.

## Ausführen

```
PYTHONPATH=. python3 milestones/06_taktfreier_kernel/run.py
```

Benötigt nur die Standardbibliothek.

## Was implementiert ist

- **`raum27.q144`** -- der 144-Zustandsraum (12 Kanten × 4 Phasen × 3
  Ebenen) und der Φ-Operator `(Kante, Phase, Ebene) → (Kante+1, Phase+90°,
  Ebene+1)`. Verifiziert: Φ ist eine Permutation von Q₁₄₄, jede Bahn hat
  exakt Länge 12 (= kgV(12, 4, 3)), und die 144 Zustände zerfallen in 12
  disjunkte Bahnen dieser Länge. Reine, nachrechenbare Kombinatorik --
  keine physikalische Behauptung.
- **`raum27.clockfree_scheduler`** -- zwei Scheduling-Policies über
  Prozesse mit einem festen `work_units`-Bedarf:
  - `schedule_run_to_completion` -- die "taktfreie" Policy aus den
    Notizen: nicht-präemptiv, jeder Prozess läuft in Warteschlangen-
    Reihenfolge bis sein Arbeitsaufwand erschöpft ist. Das ist exakt die
    klassische *First-Come-First-Served*-Disziplin.
  - `schedule_round_robin` -- die zeitgetaktete Baseline: jeder Prozess
    bekommt maximal `quantum` Operationen pro Zug, dann wird er (falls
    noch nicht fertig) ans Ende der Warteschlange zurückgestellt.

## Ergebnis

Mit dem Workload aus den Notizen selbst -- drei Prozesse mit 3, 1
Milliarde und 100 Arbeitseinheiten -- und der dort angegebenen
Warteschlangen-Reihenfolge (A, B, C):

| Prozess | Arbeit        | Wartezeit (taktfrei) | Wartezeit (Round-Robin, q=1000) |
|---------|---------------|-----------------------|----------------------------------|
| A       | 3             | 0                     | 0                                |
| B       | 1.000.000.000 | 3                     | 103                              |
| C       | 100           | **1.000.000.003**     | 1.003                            |

Kontextwechsel: taktfrei = 3, Round-Robin = 1.000.002.

Der taktfreie Scheduler braucht drastisch weniger Kontextwechsel -- aber
Prozess C, der in den Notizen als "fertig nach 100 Operationen"
beschrieben wird, wartet in Wirklichkeit **eine Milliarde Takte**, weil er
hinter dem großen Prozess B in der Warteschlange steht. Das ist kein Bug
der Implementierung, sondern der klassische **Convoy-Effekt** von
nicht-präemptivem FCFS-Scheduling -- exakt das Verhalten, das
zeitgetaktetes Round-Robin durch Design begrenzt (Wartezeit für C bleibt
unter einem Kontextwechsel-Budget, unabhängig davon, was vor ihm in der
Schlange steht).

Wird dieselbe Arbeitslast stattdessen mit kurzen Prozessen zuerst
eingereiht (A, C, B), gewinnt der taktfreie Scheduler in jeder Metrik --
niedrigste Wartezeit für alle drei Prozesse, wenige Kontextwechsel. Siehe
die Konsolen-Ausgabe von `run.py` für beide Fälle nebeneinander.

**Fazit:** "Taktfrei" ist kein grundsätzlicher Fortschritt gegenüber
Zeitscheiben, sondern ein Trade-off, der genau dem entspricht, was die
Scheduling-Theorie seit Jahrzehnten kennt (FCFS vs. Round-Robin, SJF,
Convoy-Effekt): weniger Overhead und optimale Wartezeit, wenn die
Job-Größen vorab bekannt sind und günstig eingereiht werden können; im
Worst Case (kleiner Job hinter großem Job, unbekannt bei Ankunft)
unbeschränkte Wartezeit. Die Notizen zeigen nur den günstigen Fall.

## Was hier bewusst nicht implementiert ist

Der Blogpost, aus dem dieser Meilenstein stammt, beschreibt außerdem eine
interaktive Konsole (`raum27_os_kernel_v11.py`), veröffentlichte Apps auf
itch.io, ein arXiv-Preprint und drei physikalische Hypothesen (H9-H11:
fraktale Verdichtung, neutrale Resonanzfelder, Kristallisationskerne).
Keiner dieser Punkte ist Teil dieses Codebase-Meilensteins: Die Konsole
ist ein Interface um die hier implementierte, echte Logik herum und kein
zusätzlicher mathematischer Inhalt; die Hypothesen sind explizit als
ungetestet markiert und würden eigene, unabhängige Benchmarks gegen
physikalische Messdaten brauchen, nicht Software-Scheduling-Metriken.
Das entspricht dem bestehenden Prinzip des Projekts (siehe
Haupt-README): nur was verifiziert benchmarked wurde, bleibt.
