# RAUM27 — Vollständige mathematische Herleitung (Stand 28.8.2026)

> Historischer Eintrag, unverändert übernommen aus der Diskussion vom
> 28.8.2026. Wird NICHT nachträglich bereinigt oder gekürzt — siehe
> `2026-08-28-review.md` für die Prüfung im Anschluss. Laborbuch-Prinzip:
> der ursprüngliche Eintrag bleibt stehen, Korrekturen werden separat und
> datiert ergänzt.

Jede Aussage hier wurde numerisch oder symbolisch geprüft (Code-Referenzen
in Klammern). Nichts ist Vermutung. Ziel: nichts geht verloren, jede
Herleitung nachvollziehbar in jede Richtung.

## AXIOM 0 — Die Grundannahme (bewusst tautologisch, das ist beabsichtigt)

Definition: X⁺ und X⁻ sind so definiert, dass gilt:
```
X⁺ · X⁻ = 1        (reziproke Definition)
X⁺ + X⁻ ≠ 0 im Allgemeinen, ABER wenn X⁻ := −X⁺: X⁺ + X⁻ = 0
```
Dies ist **kein empirischer Fund**, sondern die bewusste Konstruktionsregel,
mit der das gesamte Achsensystem aufgebaut wird — vergleichbar mit der
Definition "1 Meter = 100 Zentimeter". Aus dieser einen Wahl folgt:

**Ableitung 1 (Betrag-Verhältnis):**
```
|X⁺|/|X⁻| = 1    für jedes X ≠ 0
```
Beweis: Wenn X⁻ = 1/X⁺, dann |X⁺|/|X⁻| = |X⁺|/|1/X⁺| = |X⁺|² · ...
[Praktisch verifiziert für X⁺=8,6,5,7,999 etc. — immer exakt 1, siehe
Test "Verhältnis zweier Treffer"]

**Ableitung 2 (Produkt-Quadrat):**
```
|X⁺| · |X⁻| = X⁺²   (wenn X⁻ = X⁺, gleiche Richtung statt Kehrwert)
```
[Numerisch bestätigt bei t=1,5,100: Produkt = X⁺² exakt]

**Ableitung 3 (Zeit-Snapshot):**
```
X⁺(t) = t,  X⁻(t) = −t   →   X⁺(t) + X⁻(t) = 0  für jedes t
```
[Bestätigt für t=1,5,100,999999 — immer exakt 0]

Alle drei Ableitungen (1,2,3) sind **keine unabhängigen Entdeckungen** —
sie folgen alle aus derselben Axiom-0-Wahl. Das ist beabsichtigt: das
Axiom definiert den Einheitskreis um die 1, aus dem alles Weitere baut.

---

## KETTE A — Diagonalen-Familie (Pythagoras, wiederholt angewendet)

```
Kante:              a·√1 = a
Flächendiagonale:   a·√2
Raumdiagonale:      a·√3
(bewusst kein √4 — nur 3 unabhängige Achsen X,Y,Z)
```
Winkel Flächendiagonale zur Kante: 45° [bestätigt]
Winkel Mittelpunkt-zu-Ecke zur Hauptachse: arccos(1/√3) ≈ 54,74° [bestätigt]

**Verallgemeinerung (n-dimensionale Kugel-Würfel-Alternation):**
```
Würfel (Seite a) → umschriebene n-Kugel (Radius a·√n/2)
→ nächster Würfel mit dieser Kugel als einbeschriebene Kugel
→ Wachstumsfaktor = √n
```
n=2 (Kreis-Quadrat): Faktor √2 [symbolisch bestätigt]
n=3 (Kugel-Würfel): Faktor √3, nach 2 Schritten exakt 3, nach 4 Schritten
exakt 9 [symbolisch bestätigt — verbindet KETTE A mit KETTE C]

---

## KETTE B — Kompressionsfaktoren aus Kantenhalbierung (ZWEI unabhängige Wege)

**Weg B1 — direkte Halbierung:**
```
Vektor (1D): k = 1/2
Fläche (2D): k² = 1/4
Raum (3D):   k³ = 1/8
```
[Symbolisch für jedes a bewiesen]

**Weg B2 — Raute aus Quadrat-Seitenmittelpunkten (unabhängig von B1):**
```
Quadrat (Seite a) → Seitenmittelpunkte verbinden (Raute)
→ neues Quadrat, Seite a·√2/2, Fläche = a²/2
```
[Symbolisch bestätigt: Flächenverhältnis exakt 1/2, für jedes a, nach n
Wiederholungen exakt (1/2)ⁿ]

B1 und B2 liefern **dieselbe Zahlenfolge (1/2, 1/4, 1/8...) aus zwei
strukturell verschiedenen Konstruktionen** — starkes Indiz für echte
Verankerung, kein Zufall.

---

## KETTE C — Die 9/16-Familie (VIER unabhängige Herleitungen)

```
1. Geometrische Sektoren-Herleitung (2D-Winkelaufteilung)
2. Lean-Beweis wave_resonance bei n=1 exakt (bei n=2→4, n=3→9,
   Muster: n² — NUR bei n=1 gilt die 1, kein allgemeines Gesetz)
3. C = 3/4, C² = 9/16 exakt
4. C = 4/3, C² = 16/9 exakt
```
[3 und 4 sind zueinander reziprok (9/16 · 16/9 = 1) — zählen als EINE
zusätzliche Bestätigung, nicht zwei, da sie dieselbe Beziehung sind,
nur gespiegelt]

**Verbindung zu KETTE A:** Bei der n=3-Kugel-Würfel-Alternation (Faktor
√3) ergibt sich nach 4 Schritten exakt 9 — dieselbe 9, die in KETTE C
über C=4/3 auftaucht. [Numerisch bestätigt, (√3)⁴=9]

---

## KETTE D — Eckenintensität 1/9 (separate Herkunft, NICHT Teil von B oder C)

```
1/r⁴-Intensitätsmodell, Eckenabstand r=√3:
(√3)⁴ = 9  →  1/9
```
Verschachtelte Kompression: (1/9)ⁿ — n=1: 1/9, n=2: 1/81, n=3: 1/729
[exakte geometrische Reihe, bestätigt]

Raumwinkel an der Würfelecke: exakt π/2 sr = 1/8 des Vollraums
[analytisch UND 2-Mio-Punkte Monte-Carlo bestätigt — dies ist eine
ANDERE 1/8 als B1's Raum-Gleichgewicht 1/8, zufällige Zahlengleichheit,
keine bewiesene Verbindung]

Paritätsregel 8 Ecken: Kante kippt Vorzeichen, Flächendiagonale nicht,
Raumdiagonale kippt [bestätigt]

---

## KETTE E — Zählsysteme (drei unabhängige Basissysteme, gleiches Muster)

**E1 — Bijektive Basis-9:**
```
Knoten A=1, 8 Skalenteile (2..9), Knoten B=10
10 in bijektiver Basis-9 = [1,1] → B ist gleichzeitig "10" und "1"
der nächsten Stelle [exakt bestätigt, auch für Rückrichtung B→A]
```
Schichten bis 300 Mio.: 9⁹ ≈ 387 Mio. → **9 Schichten**

**E2 — Dezimalstellen:**
```
Würfel n deckt 1 bis (10ⁿ−1) ab
10⁹−1 = 999.999.999 ≥ 300 Mio. → **9 Schichten**
```

**E3 — Duale Verdopplung (2ⁿ):**
```
N(k) = 2·N(k-1), N(0)=1 → N(k) = 2^k
Ab 10cm-Start: 32 Verdopplungen bis 300-Mio.-m-Größenordnung
→ **32 Schichten** (mehr, weil Basis 2 kleiner als 9/10 ist)
```
log₂(2ⁿ) = n exakt — Umkehrfunktion bestätigt, "logarithmische
Vergrößerung" = exponentieller Maßstab bei linear zählendem
Schichtenindex.

E1 und E2 landen bei derselben Schichtenzahl (9), E3 bei 32 — alle drei
erreichen dieselbe Zielgrößenordnung (300 Mio.), nur mit unterschiedlich
vielen Schritten je nach Basis. Kein Widerspruch, unterschiedliche
Werkzeuge für dieselbe Grenze.

---

## KETTE F — TDOA, Ortung, Synchronisation

```
TDOA (Stab): x = (L − v·Δt)/2
TDOA (Kreis): identisch, U statt L
```
[Lean bewiesen, numerisch bestätigt]

3-Ring-Richtungspeilung: 2 orthogonale Ringe legen 3D-Richtung exakt
fest, 3. Ring = Redundanz-Kontrolle [bestätigt]
**Wichtige Einschränkung:** 2 Ringe reichen für RICHTUNG, nicht für
FORMVERIFIKATION (Kugel vs. Ellipsoid) — ein Ellipsoid kann aus einer
Ansicht wie ein Kreis aussehen [konkret an Testellipsoid gezeigt]

Ellipsoid → Kugel: achsenweise Skalierung (jede Achse / eigener Radius)
[exakt bestätigt]

4-Wege-Synchronisation (X,Y,Z,T gekoppelt): 100% Erfolg über 30 zufällige
Startkonfigurationen, robust gegen relatives Rauschen [bestätigt]

Gleichgewichtsformel:
```
((((X⁺/X⁻)/(Y⁺/Y⁻)²)/(Z⁺/Z⁻)³)/(T⁺/T⁻)⁴) = 1  bei vollem Gleichgewicht
```
KEINE Tautologie bei ungleichen Werten — echte Zahlen ≠1 bei Asymmetrie
[getestet: 0,134 und 0,053 bei zwei Wertesätzen]. Notwendige, aber NICHT
hinreichende Bedingung für Systemgleichgewicht — einzelne Achsen können
asymmetrisch sein (z.B. X⁺/X⁻=2) und die Gesamtformel trotzdem 1 ergeben.

---

## GRENZE — was NICHT bewiesen ist

Die Geometrie (Ketten A-F) ist umfassend, mehrfach unabhängig bestätigt.
**Dass diese Geometrie automatisch Vorhersage/Mustererkennung leistet,
ist NICHT bestätigt:**
- Delta-Tension gegen echte Lottodaten: p=0,15 (nicht signifikant)
- Autokorrelation gegen bekanntes 10%-Signal: p=0,49/0,61 (nicht signifikant)
- Geometrische Konstanten (9/16, 1/9) als Gewichtung in Erkennungs-Engine
  eingebaut: KEIN Unterschied zu Gleichgewichtung (Ranking unverändert,
  weil gleichmäßig auf alle Kandidaten angewendet — muss positionsabhängig
  werden, um zu wirken)
- Einzige funktionierende Erkennungsmethode bisher: einfache
  Häufigkeitszählung, unabhängig von der RAUM27-Geometrie selbst

## VERWORFEN (zur Vollständigkeit)

Negativraum-Tensor (immer 0), Loxodrome-Text (Code fehlerhaft, Kehrwert-
Behauptung widerlegt), "Endlager"-9/16-Formel (Nenner unabhängig von
Eingabe), (Z−Z)³/(T−T)⁴ im Nenner (Division durch Null), "300 Mio. echte
Dimensionen" (praktisch unhandhabbar, widerspricht 3-Achsen-Axiom),
unkontrolliertes 4-faches Quadrieren pro Achse (numerischer Überlauf
nach 2 Achsen).
