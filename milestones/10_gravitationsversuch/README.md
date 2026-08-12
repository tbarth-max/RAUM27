# Meilenstein 10: Gravitationsversuch — massenproportionale Kopplung

Direkte Antwort auf die in `VALIDIERUNG.md` Abschnitt 11 offene Frage:
**"Woher kommt m₁·m₂?"**

## Was geändert wurde

Das dort getestete Flächen-/Abschattungsmodell scheiterte an einer
präzisen, benennbaren Ursache: Blockfläche skaliert mit R² (Geometrie),
Masse mit R³ (bei konstanter Dichte) — zwei verschiedene Größen. Hier
wird **ein einziges, gezieltes Postulat** getestet: Der
Abschattungs-/Kopplungsquerschnitt σ eines Körpers ist keine geometrische
Fläche, sondern eine eigene Größe **σ = c·m**, direkt proportional zur
Masse.

## Ergebnis: alle 4 Kriterien erfüllt — aber mit einer wichtigen Einschränkung

| Kriterium | Ergebnis |
|---|---|
| 1. F ∝ m₁·m₂ | **PASS** — F/(mᵢ·mⱼ) konstant = 0,01 über alle 12 getesteten Massenkombinationen |
| 2. F ∝ 1/r² | **PASS** — F·r² konstant = 15,0 über r=5…40 |
| 3. immer anziehend | **PASS** — Kraftrichtung zeigt in allen 3 getesteten Konfigurationen zu j, nie weg |
| 4. Netto-Kraft auf isolierten Körper = 0 | **PASS** — \|Netto-Richtung\| = 0,00025 (2 Mio. Zufallsrichtungen) |

**Wichtig, damit das nicht als "Gravitation gelöst" missverstanden wird:**
Kriterium 1+2 wurden **zweifach** geprüft — einmal analytisch (per
Konstruktion trivial wahr) und einmal **unabhängig per Monte-Carlo**
(2 Mio. zufällig isotrope Richtungen, geometrische Verdeckung direkt
simuliert, ohne die Kraftformel zu benutzen). Beide stimmen auf 0,2–7,3 %
überein (statistisches Rauschen bei kleinen Wahrscheinlichkeiten) — das
bestätigt, dass die **Verdeckungs-Geometrie selbst** tatsächlich 1/r² und
Linearität in σⱼ liefert, das ist kein Zirkelschluss.

**Aber:** σ geht in die Rechnung an **zwei Stellen** ein — als
Verdeckungsquerschnitt des blockierenden Körpers j (**das** wurde
geometrisch verifiziert) und als Kopplungsstärke des empfangenden
Körpers i (wie stark i überhaupt auf eintreffenden Fluss reagiert). Die
zweite Stelle ist **nicht** aus der Geometrie ableitbar — sie ist ein
zusätzliches Postulat, exakt analog zum Äquivalenzprinzip der
Standardphysik (träge Masse = schwere Masse, ebenfalls nicht aus
tieferen Prinzipien hergeleitet, sondern experimentell auf 1:10¹³
bestätigt). Das ist also kein Defizit, das RAUM27 einzigartig hat — es
ist derselbe unerklärte Fakt, der in der Standardphysik genauso besteht.

## Was hiermit ausdrücklich NICHT gelöst ist

Zwei historisch **unabhängige und als entscheidend geltende** Probleme
jedes Schattenwurf-Mechanismus (Le Sage, 1748) werden hier nicht
getestet und bleiben ungelöst — die Korrektur des Masse-Problems behebt
sie nicht:

1. **Aufheizung:** Der blockierte Impuls muss irgendwo bleiben. Jeder
   Körper, der ständig Fluss absorbiert/streut, müsste sich kontinuierlich
   aufheizen. Beobachtet wird das nicht.
2. **Bahnwiderstand:** Ein sich bewegender Körper sieht den
   Hintergrundfluss durch Aberration leicht asymmetrisch — das erzeugt
   einen geschwindigkeitsabhängigen Bremswiderstand. Planetenbahnen
   zeigen über Jahrmillionen keinerlei solchen Widerstand; das war
   historisch der entscheidendere Sargnagel für Le-Sage-Theorien als das
   Masse-Problem.

## Fazit — Antwort auf die Ausgangsfrage

**Immer noch nicht guten Gewissens implementierbar als physikalische
Behauptung.** Aber der Status ist jetzt präziser als vorher: Aus "wir
wissen nicht, warum m₁·m₂" ist geworden "wir wissen genau, mit welchem
Postulat sich m₁·m₂ erzeugen lässt (Kopplung ∝ Masse statt ∝ Fläche,
teilweise geometrisch verifiziert), und wir wissen genau, welche zwei
unabhängigen, historisch als fatal geltenden Probleme dabei offen
bleiben (Aufheizung, Bahnwiderstand)." Das ist ein echter Erkenntnisfortschritt,
aber kein PASS für ein vollständiges Gravitationsmodell.

## Ausführen

```
python3 milestones/10_gravitationsversuch/run.py
```

CSVs unter `milestones/10_gravitationsversuch/results/`.
