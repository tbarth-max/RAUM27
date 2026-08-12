# RAUM27 — Unabhängige Validierung

**Datum:** 2026-08-12
**Herkunft:** Erstellt in einer separaten Chat-Session (laut Nutzer: Opus 5),
unabhängig von den Meilenstein-Skripten in diesem Repository. Hier
unverändert übernommen, mit Querverweisen zu den Stellen, die sich mit
den Skripten in `milestones/` decken oder ihnen widersprechen.
**Methode:** Nachrechnung zentraler Behauptungen mit NumPy / exakter
Bruchrechnung (`fractions.Fraction`)
**Prinzip:** Jede Aussage hat eine Zahl. Was nicht gerechnet wurde, steht
unter „Offen".

## Querverweise zu diesem Repo

- **Abschnitt 2 (Theorem 18, Rang P_FE = 4):** deckt sich mit der
  6×8-Kopplungsmatrix `D` aus `milestones/07_omega_symmetrische_schalen/`
  (dort unabhängig, mit anderer Konstruktion — Oktaeder-Richtungen statt
  Ecke-Mittelwert-Fläche — ebenfalls Rang 4 gefunden). Beide Matrizen
  haben denselben Grund: die drei antipodalen Achsenpaare (+X/-X, +Y/-Y,
  +Z/-Z) erzeugen identische Summenvektoren, das sind 2 unabhängige
  lineare Zwangsbedingungen, nicht 3 — daher Rang 6−2=4, robust und
  zweifach bestätigt, kein Zufall einer einzelnen Konstruktion.
- **Abschnitt 1.3 (4/3 = 8 Ecken / 6 Flächen, exakt):** korrigiert die im
  Chat diskutierte, aber nie committete Herleitung von 4/3 aus dem
  Flächenverhältnis Quadrat/Kreis (die sich als π≈3-Näherung mit 4,7 %
  Abweichung herausstellte, siehe Chat-Verlauf zu Meilenstein 7). Die
  hiesige Zähl-Herleitung (8/6, Ecken zu Flächen des Würfels) ist exakt
  und braucht kein π.
- **Abschnitt 10 (v=λ·f, nicht λ/f):** deckt sich mit der Korrektur aus
  dem Chat-Verlauf vor Meilenstein 6 (Ω=k²-Definition).
- Alle übrigen Abschnitte (Gravitationszweig, κ=0,600, Ringtopologie,
  Ausleseklasse, Codierer, Speicherformat, Kompressionsvergleich)
  betreffen Themen, die in `milestones/05`–`09` noch nicht abgebildet
  sind.
- **Abschnitt 11 (Gravitationszweig, m₁·m₂ offen):** aufgegriffen in
  `milestones/10_gravitationsversuch/` — testet gezielt das eine
  Postulat "Kopplungsquerschnitt ∝ Masse statt ∝ Fläche". Kriterien 1–4
  erfüllt (teils per Monte-Carlo-Geometrie unabhängig verifiziert, nicht
  nur per Formel), aber die zwei historisch entscheidenden Probleme
  jedes Schattenwurf-Mechanismus (Aufheizung, Bahnwiderstand) bleiben
  dort ausdrücklich ungelöst. Details siehe Abschnitt 15 unten.
- **Zentralsignal-Inversion (Kontrolltest):** siehe Abschnitt 14 unten —
  widerlegt die Aussage, dass Würfelgeometrie die Rekonstruktion aus dem
  zentralen Rücksignal ermöglicht.

---

## Zusammenfassung

| Bereich | Ergebnis |
|---|---|
| Multiplikative Algebra (ℚ⁺, Produkt = 1) | **11/11 PASS**, ohne √ oder π |
| Theorem 18 (Rang P_FE = 6) | **FAIL** — tatsächlicher Rang = 4 |
| 8-Bit durch 8×6→6×8 | **FAIL** — 2,03 Bit mittlerer Fehler |
| Ausleseklasse (Punkte × Zeit) | **PASS** — 24/24 Kanäle trennbar |
| Codierer (3 Schwellen) | **PASS unter Sinusannahme**, sonst nicht eindeutig |
| Speicherformat RGB-Hex 24 Bit | **PASS** — deckt 9 Freiheitsgrade |
| Ringtopologie (3×4 = 12 Slots) | **PASS** — geschlossener 4-regulärer Graph |
| κ = 0,600 | **Offen** — keine Herleitung gefunden |
| Gravitationszweig | **FAIL** — m₁·m₂ nicht erklärt |
| Zentralsignal-Inversion (Kontrolltest) | **FAIL** — willkürliche Kontrollkonfiguration rekonstruiert besser als die Würfelkonfiguration |
| Gravitationsversuch, massenproportionale Kopplung (Nachtrag) | **PASS unter Zusatzpostulat** — Kriterien 1–4 erfüllt, zwei historisch fatale Probleme (Aufheizung, Bahnwiderstand) ungetestet |

---

## 1. Algebraischer Kern — PASS

Zustandsraum ℚ⁺, Inversion I(x) = 1/x, Fixpunkt x = 1, Basisverhältnis r = 4/3.

| # | Prüfung | Ergebnis |
|---|---|---|
| 1 | Produkt aller 8 Ecken = 1 | PASS (= 1) |
| 2 | 4 Diagonalpaare je = 1 | PASS |
| 3 | A·B = 1 mit A = 4/3 | PASS (= 1) |
| 4 | A² = 16/9 rational | PASS (= 16/9) |
| 5 | Kaskade r¹, r², r⁴ rational | PASS |
| 6 | r⁷ · r⁻⁷ = 1 | PASS |
| 7 | C = 8/6 = 4/3 exakt | PASS |
| 8 | Alle Werte positiv | PASS |
| 9 | Keine Irrationalität | PASS |
| 10 | 27 Zellen unter Inversion abgeschlossen | PASS |
| 11 | Zentrum (1,1,1) ist Fixpunkt | PASS |

**11/11 ohne ein einziges √ oder π.**

### 1.1 Warum multiplikativ, nicht additiv

| Fassung | Werte | Produkt |
|---|---|---|
| additiv (1 ± 0,5) | 1,5 / 0,5 | **0,75** ✗ |
| multiplikativ (r^sin t, r=2) | 2,0 / 0,5 | **1,00** ✓ |

Nur die multiplikative Fassung erfüllt die Gleichgewichtsbedingung A·B = 1.

### 1.2 Korrektur: √2 gehört gestrichen wie π

Bisherige Spezifikation streicht π als irrational, behält A = 2^(1/2).
Inkonsistent. Ersatz ohne Verlust:

| A | B | A·B | A² |
|---|---|---|---|
| **4/3** | **3/4** | **1** | **16/9** |

√2 und √3 bleiben ausschließlich als *geometrische Längenverhältnisse*
(Flächendiagonale, Raumdiagonale). Sie gehören nicht in die Zustandsalgebra.

### 1.3 Korrektur: 4/3 kommt vom Abzählen

| Herleitung | Wert | Abweichung von 4/3 |
|---|---|---|
| Quadrat/Kreis gleicher Fläche | √π = 1,772 | **33 %**, irrational |
| Würfel/Kugel gleichen Volumens | 1,612 | **21 %**, irrational |
| **8 Ecken / 6 Flächen** | **4/3** | **exakt** |

Kreis-Herleitung streichen.

### 1.4 Minus vollständig entfernt

Zellmenge {−1, 0, 1}³ → **{1/r, 1, r}³**

- 27 Zellen
- Produkt aller Zellprodukte = **exakt 1**
- unter Inversion **27/27 abgeschlossen**
- Zentrum (1,1,1) als Fixpunkt

---

## 2. Theorem 18 — FAIL

*Ausführbare, exakte Reproduktion (parameterfrei, kein Seed):
[`validierung_skripte/roundtrip_8bit.py`](validierung_skripte/roundtrip_8bit.py)
— liefert dieselben Werte wie hier und in Abschnitt 3 dokumentiert.*

**Behauptung:** Φ invertierbar ⟺ rang(P_FE) = 6

**Befund:** P_FE (8 Ecken × 6 Flächen, jede Ecke = Mittelwert ihrer 3 Nachbarflächen)
hat **Rang 4**. Kern zweidimensional.

**Ursache (algebraisch, nicht numerisch):**

```
(+X) + (−X) = (+Y) + (−Y) = (+Z) + (−Z) = (1/√3)·[1,1,1,1,1,1,1,1]
```

Jede Ecke liegt an genau einer von je zwei Gegenflächen. Alle drei Achsen
erzeugen dieselbe Summenbeziehung → zwei unabhängige lineare Relationen →
Rang ≤ 6 − 2 = 4.

Zum Vergleich: eine zufällige 8×6-Matrix hat Rang 6. Die geometrische
Konstruktion ist die Ausnahme.

### 2.1 Gegenprüfungen

| Ansatz | Rang |
|---|---|
| P_FE direkt | 4 |
| S_Ecke · P_FE · S_Fläche (Retroreflexion, det = ±1) | 4 |
| mit 5 zufälligen invertierbaren Matrizen davor/danach | 4, 4, 4, 4, 4 |
| Pyramide über Zentrum (R⁶ → R¹ → R⁸) | **1** |

**Satz:** rang(B·M·A) = rang(M) für invertierbare A, B.
Reflexionen können verlorene Dimensionen grundsätzlich nicht zurückholen.

Die Pyramiden-Variante ist schlechter, nicht besser: ein Zentrumspunkt ist
eindimensional, also ein Nadelöhr.

### 2.2 Was stattdessen gilt

(+X, −X) als **ein** Freiheitsgrad gelesen → 3 Freiheitsgrade, **Rang 3, injektiv**.
Gültige, aber kleinere Aussage als Theorem 18.

---

## 3. Bit-Erhaltung 8×6 → 6×8 — FAIL

Alle 256 möglichen 8-Bit-Muster durchgerechnet:

| Bitfehler | Anzahl Muster |
|---|---|
| 0 | 27 |
| 1 | 64 |
| 2 | 76 |
| 3 | 64 |
| 4 | 20 |
| 6 | 4 |
| 8 | 1 |

**Mittlerer Fehler: 2,03 von 8 Bit.** Nur 27 von 256 Mustern überleben fehlerfrei.

Dies bestätigt die Angabe „2 Bit systematisch verklebt" im Simulations-Log
und **widerlegt** den PASS-Eintrag im Übersichtsblatt.
→ Übersichtsblatt korrigieren.

---

## 4. Ausleseklasse — PASS

24 Quellen im 19³-Gitter, gedämpfte Wellengleichung, Rang = trennbare Kanäle:

| Konfiguration | 1 Zeitpunkt | 3 Zeitpunkte | 10 Zeitpunkte |
|---|---|---|---|
| Zentrum allein (1 Punkt) | 1 | 3 | 10 |
| 4 Äquatorpunkte | 3 | 11 | **24** |
| Zentrum + 4 außen (5 Punkte) | 4 | 14 | **24** |
| 6 Flächenmitten | 5 | 17 | **24** |
| 8 Ecken | **0** | 16 | **24** |

**Regel:** trennbare Kanäle ≈ Auslesepunkte × unabhängige Zeitpunkte.

**Minimalkonfiguration:** 5 Punkte leisten dasselbe wie 8.

**Eckenentartung:** Bei einem Zeitpunkt Rang 0 — alle 8 Ecken sehen durch die
Symmetrie dasselbe. Erst die Zeit bricht die Entartung.

### 4.1 Ortsinformation

Korrelation erste Ankunftszeit ↔ geometrischer Abstand: **+0,93**
→ Quellort per Multilateration rekonstruierbar.

---

## 5. Geometrie

### 5.1 Laufzeiten — Inkommensurabilität

| Ziel | Anzahl | Weg (h=1) | Verhältnis |
|---|---|---|---|
| Flächenmitte | 6 | 1,0000 | 1 |
| Kantenmitte | 12 | 1,4142 | √2 |
| Ecke | 8 | 1,7321 | √3 |

Nach 1–5 Flächenumläufen liegt die Ecken-Rückkehr bei
0,577 / 1,155 / 1,732 / 2,309 / 2,887 Umläufen — **nie ganzzahlig**.
Die drei Punkttypen treffen sich nach dem Start nie wieder gleichzeitig.

**Lösung:** ausschließlich die 4 Raumdiagonalen nutzen (alle exakt 2√3·h lang).
Bei nur einer Weglänge ist Irrationalität irrelevant.

### 5.2 Dualität Würfel ↔ Oktaeder — PASS, aber wirkungslos

Konvexe Hülle der 6 Flächenmitten: **6 Ecken, 8 Flächen, 12 Kanten** = Oktaeder.
Geometrisch korrekt. Ändert den Rang von P_FE **nicht** — es ist dieselbe
Punktmenge unter anderem Namen.

### 5.3 Nullstellen im würfelsymmetrischen Feld

Feld aus 3 stehenden Wellen mit 120° Phasenversatz. Nullstellen bei:
**8 Ecken + 6 Flächenmitten + 12 Kantenmitten + 1 Zentrum = 27**

Durchgehende Nulllinie entlang x = y = z (Intensität 10⁻³¹).
Entlang der Achsen **keine** durchgehende Nulllinie.

*Einschränkung:* gilt für diese Anregung. Andere Phasenlagen → andere Nullstellen.

---

## 6. Codierer — PASS unter Modellannahme

Drei Schwellen (Mittellinie, +h, −h). Rekonstruktion via A = h / sin(ω·t_h):

| wahr A | wahr ω | rekonstruiert A | rekonstruiert ω |
|---|---|---|---|
| 1,00 | 1,00 | **1,00** | 1,00 |
| 2,50 | 1,00 | **2,50** | 1,00 |
| 0,70 | 3,00 | **0,70** | 3,00 |
| 5,00 | 0,50 | **5,00** | 0,50 |

Löst das Amplitudenproblem reiner Nulldurchgangserfassung.

### 6.1 Grenze — Gegenbeispiel

Zwei Wellen mit **identischen Durchgängen** an allen drei Schwellen:

- +0,5-Durchgänge beide bei 0,5218 und 2,6151
- −0,5-Durchgänge beide bei 3,6649 und 5,7583
- Maximaler Unterschied der Signale: **0,35**
- Maxima: 1,0000 vs **1,0145**

→ Durchgänge bestimmen eine **beliebige** Welle nicht eindeutig.

**Tragfähige Formulierung:**
> Unter der Annahme sinusförmiger Wellen bestimmen Mittellinien- und
> Ring-Durchgänge Amplitude, Frequenz und Phase vollständig.

### 6.2 Kapazität

| Signal | Durchgänge/s | Entropie |
|---|---|---|
| reiner Sinus (3 FG) | 23 | 2,00 Bit |
| 3 Komponenten (9 FG) | 38 | 3,73 Bit |
| rauschartig | 56 | 3,80 Bit |

- ≤3 Freiheitsgrade → 8 Bit reichen (≈6 Stufen je Größe)
- 9 Freiheitsgrade → 8 Bit geben 1,9 Stufen je Größe → **unbrauchbar**, ≈24 Bit nötig

**Belegt:** „Signal mit ≤3 Freiheitsgraden → 8 Bit + Laufzeit."
**Nicht belegt:** „jedes Analogsignal → 8 Bit."

---

## 7. Speicherformat — PASS

`#RRGGBB` = 6 Hexziffern × 4 Bit = **24 Bit** = 16.777.216 Zustände

Mapping: **1 Hexziffer je Würfelfläche** (6 ↔ 6), 16 Stufen pro Fläche.

24 Bit entspricht exakt der für 9 Freiheitsgrade benötigten Kapazität
(unabhängig hergeleitet, siehe 6.2).

Metamerie (verschiedene Spektren → gleicher Code) ist hier **kein Defekt**:
Ziel ist Musterspeicherung, nicht Wellenformrekonstruktion.

---

## 8. Ringtopologie — PASS

| Ring | Knoten |
|---|---|
| ⊥ Z | +X, +Y, −X, −Y |
| ⊥ Y | +X, +Z, −X, −Z |
| ⊥ X | +Y, +Z, −Y, −Z |

Jede Fläche liegt auf **genau 2** Ringen. 3 × 4 = 12 = 6 × 2.
→ geschlossener 4-regulärer Graph.

**Rahmen (12 Slots/Umlauf):**

| Slots | Inhalt |
|---|---|
| 1–8 | Nutzdaten |
| 9–10 | Quelladresse |
| 11 | Parität |
| 12 | Rahmenende / Token |

Entspricht IEEE 802.5 (Token-Ring).

---

## 9. Kompressionsvergleich

4000 Abtastwerte, float32 = 16.000 Byte roh:

| Signal | gzip | bzip2 | lzma | RAUM27 | Faktor vs gzip |
|---|---|---|---|---|---|
| reiner Sinus 5 Hz | 843 | 1.220 | 756 | **360** | 2,34× |
| 3 Komponenten | 3.147 | 4.809 | 2.128 | **452** | 6,96× |
| 10 Komponenten | 3.878 | 5.599 | 3.400 | **248** | 15,64× |
| weißes Rauschen | 14.839 | 15.965 | 14.972 | **2.132** | 6,96× |

### 9.1 Einordnung — wichtig

**Der Vergleich ist nicht fair.** gzip ist immer verlustfrei, RAUM27 nicht:

| Signal | rekonstruierte Grundfrequenz | Soll |
|---|---|---|
| reiner Sinus | **5,00 Hz** | 5 Hz ✓ |
| 3 Komponenten | 9,14 Hz | 5 Hz ✗ |
| 10 Komponenten | 5,02 Hz | mehrdeutig |
| weißes Rauschen | 251,63 Hz | — ✗ |

**Korrekte Aussage:**
> RAUM27 schlägt gzip um Faktor 2,3 bei **verlustfreier** Codierung
> einfacher (Ein-Komponenten-)Signale. Bei komplexen Signalen ist es ein
> verlustbehafteter Merkmalsextraktor, kein Kompressor — dort ist der
> Vergleich mit gzip unzulässig.

---

## 10. Physikalische Korrekturen

| Behauptung | Befund |
|---|---|
| v = λ/f | **falsch.** v = λ·f (λ/f hat Einheit m·s) |
| Ω = F/Λ | Einheit 1/(m·s), **nicht** 1/s. Korrekt: Ω = 2πf, k = 2π/λ, v = f/k |
| Sinus = Kreis | Kreis hat konstante Krümmung, Sinus nicht |
| konstanter Betrag nach innen | Amplitude ∝ **1/r**. Konstant ist r·Amplitude = 1 |
| konstante Beschleunigung im Feld | Fluss konstant (Gauß), g ∝ **1/r²** |
| innen beschleunigend | massive Kugel: g ∝ r, Zentrum **0**. Hohlkugel: innen exakt **0** |
| ewiges Schwingen | Dämpfung 0 → Signalenergie 0,0065 → 0,33, Kanal permanent belegt |
| Information ohne Energie | Landauer: 2,87·10⁻²¹ J/Bit bei 300 K |
| π gestrichen | gilt nur bei Verhältnissen gleichartiger Größen. Umfang/Durchmesser = π bleibt |

### 10.1 Zugunsten des Modells korrigiert

**Knoten einer stehenden Welle sind Orte maximaler Energie**, nicht Leere:

| Ort | Auslenkung | (du/dx)² | (du/dt)² |
|---|---|---|---|
| Knoten | 0 | **4,00** | 0 |
| Bauch | max | 0 | max |

Zwei zu trennende Fälle:
- **gegenläufige Wellen** (stehende Welle): Energie umverteilt, erhalten
- **gleichlaufende, 180° versetzt**: Summe überall exakt 0

In 2D/3D zusätzlich: Energiefluss **zirkuliert um die Nullstelle**
(Phasensingularität / optischer Wirbel), Netto-Umlaufkomponente nachgewiesen.

### 10.2 Kohärent vs. thermisch

50 Schwinger, identische Energie:

| Betriebsart | Maximum |
|---|---|
| kohärent (gleiche Phase) | **50,0** |
| thermisch (Zufallsphasen) | **5,5** |

Amplituden addieren sich N-fach, Energien nur √N-fach.
→ RAUM27 erfordert kohärenten Betrieb.

### 10.3 Resonator-Aufbau

E_neu = E_alt·(1−Verlust) + Zufuhr → Gleichgewicht bei **E_max = Zufuhr/Verlust = Q**

| Verlust/Umlauf | Q | Endwert |
|---|---|---|
| 0,1 | 10 | 10,0 |
| 0,01 | 100 | 100,0 |
| 0,001 | 1000 | 1000,0 |

Wächst **nicht** unbegrenzt.

### 10.4 Impulsantwort

Für lineare, zeitinvariante Systeme bestimmt h(t) alles.
Rekonstruktionsfehler: **0,00e+00**.

| Speicherart | Werte |
|---|---|
| alles speichern (50 Quellen × 400 Schritte) | 20.000 |
| h + Ereignisse | **650** |

**Faktor 31.** Bedingung: Linearität. Mit tanh-Nichtlinearität: Fehler 0,659.

---

## 11. Gravitationszweig — FAIL

Mindestanforderungen an ein Gravitationsmodell:

1. Kraft ∝ **m₁·m₂** (Produkt)
2. Kraft ∝ 1/r²
3. immer anziehend
4. Nettokraft auf isolierten Körper = 0

| Variante | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| Flächen-/Abschattungsmodell | ✗ | ✓ | ✓ | ✓ |
| Emissions-/Rückprojektionsmodell | ✗ | (✓) | ? | ✓ |

**Flächenmodell:** Fläche ∝ R², Masse ∝ R³. Bei 10× Radius sagt das Modell
100× Kraft, gemessen wird 1000×. Eöt-Wash: Kopplung an Masse auf 1:10¹³ genau.
Historisch identisch mit Le-Sage-Gravitation (1748), gescheitert an
Masse-vs-Fläche, Abschattung, Aufheizung.

**Emissionsmodell:** beschreibt eine Selbstwechselwirkung. Kugelsymmetrische
Rückkehr hebt sich exakt auf (2000 Zufallsvektoren, Nettobetrag 0,013).

**Offen und entscheidend:** Woher kommt **m₁·m₂**?
Zwei Resonatoren nebeneinander **addieren** ihre Felder, sie multiplizieren
sie nicht.

---

## 12. Offene Punkte

| # | Punkt | Status |
|---|---|---|
| 1 | κ = 0,600 — Herleitung | **offen.** 10 geometrische Kandidaten geprüft, keiner trifft. Nächster: 1/√3 = 0,577 (3,8 % daneben), 32/(9π√3) = 0,653 (8,9 % daneben). Ohne Herleitung ein gesetzter Wert. |
| 2 | Duplex-Trennung (f/g auf einer Leitung) | **offen.** Prinzip etabliert (Richtkoppler), numerische Demo in dieser Session unsauber (Korrelationen +0,08 / −0,39) |
| 3 | m₁·m₂ im Gravitationszweig | **offen** |

---

## 13. Fazit

**Belegt:** exakt rechnender, rational definierter Zustandsautomat auf
Würfelgeometrie — mit verifizierter Ausleseklasse (5 Punkte × Zeitabtastung),
Codierverfahren (3 Schwellen, unter Sinusannahme exakt), Speicherformat
(24 Bit, 6 Hexziffern) und Ringtopologie (12 Slots).

**Widerlegt:** Theorem 18 in der Rang-6-Fassung. 8-Bit-Erhaltung durch 8×6→6×8.
Gravitation als Flächen- oder Emissionsmodell. Zentralsignal-Inversion als
Beleg für Würfelgeometrie (siehe Abschnitt 14).

**Strukturelle Konstante:** Jede Erhaltungsgröße im System ist ein **Produkt**,
nie ein Einzelwert — Ecke × Gegenecke, |x| × |Inversion|, r × Amplitude,
Fläche × Feldstärke, Querschnitt × Feldstärke: alle = 1.

**Strukturelle Grenze:** Jede Kapazitätsschranke ist dieselbe Rangfrage.
Trennbar ist so viel, wie der Ausleser Dimensionen hat.

---

## 14. Zentralsignal-Inversion — Kontrolltest, FAIL

**Behauptung:** Aus dem zentralen Rücksignal `y(t) = 6·x(t−2) + 8·x(t−2√3)`
lässt sich `x(t)` per Frequenzbereichs-Inversion zurückrechnen
(rel. RMSE ≈ 8,6e-4), gelesen als Beleg dafür, dass die Würfelgeometrie
(6 Flächen, 8 Ecken, Abstandsverhältnis √3) die Rekonstruktion ermöglicht.

**Kontrolle:** dieselbe Inversion mit geometriefremden Verzögerungen/
Amplituden wiederholt.

| Konfiguration | rel. RMSE | Würfelbezug |
|---|---|---|
| Würfel: 6 Flächen (τ=2) + 8 Ecken (τ=2√3) | 1,697e-11 | ja |
| Kontrolle B: willkürlich (3, 0,13)+(17, 4,77) | **1,218e-11** | nein |
| Variante mit √2 statt √3 | 1,492e-10 | nein |
| Kontrolle A: willkürlich (1, 0,70)+(1, 1,90) | 2,956e-08 | nein |
| Kontrolle C/D: entartete Fälle (Nullstellen von H(f)) | 8,197e-04 | nein |

**Befund: negativ.** Kontrolle B (rein willkürliche Werte, kein
Würfelbezug) rekonstruiert **besser** als die Würfelkonfiguration. Ein
Zwei-Tap-Verzögerungsfilter ist im rauschfreien Fall für nahezu beliebige
Parameter invertierbar — das ist generische Signalverarbeitung
(`X_rec = Y·H*/(|H|²+λ)`), keine geometrische Besonderheit des Würfels.
Die niedrige Fehlerzahl der Würfelkonfiguration belegt damit **nicht**,
dass Würfelgeometrie die Rekonstruktion ermöglicht.

**Unberührt gültig bleibt** die reine Arithmetik: Laufzeitdifferenz
`Δt = 2(√3−1)`, erste konstruktive Frequenz `f₁ = 1/Δt`, und die drei
verschiedenen geometrischen Abstände im Würfel (Flächenmitte=1,
Kantenmitte=√2, Ecke=√3, je von der Kubuszentrum aus, halbe Kante=1).
Das sind korrekte Zahlen — sie belegen nur nichts über Rekonstruierbarkeit.

---

## 15. Gravitationsversuch — massenproportionale Kopplung (Nachtrag)

Aufgreifend auf Abschnitt 11 (offene Frage: woher kommt m₁·m₂?): ein
gezielter Versuch in `milestones/10_gravitationsversuch/` testet **ein**
geändertes Postulat — Kopplungsquerschnitt σ = c·m (proportional zur
Masse) statt σ ∝ R² (geometrische Fläche, der Grund für das ursprüngliche
Scheitern).

| Kriterium | Ergebnis |
|---|---|
| F ∝ m₁·m₂ | PASS (F/(mᵢmⱼ) konstant über 12 Massenkombinationen) |
| F ∝ 1/r² | PASS (F·r² konstant über r=5…40) |
| immer anziehend | PASS |
| Netto-Kraft auf isolierten Körper = 0 | PASS (Monte-Carlo, 2 Mio. Richtungen, Reststand 0,00025) |

Kriterien 1+2 wurden zusätzlich **unabhängig per Monte-Carlo-Geometrie**
verifiziert (reine Richtungsstichprobe, ohne die Kraftformel zu benutzen)
— Übereinstimmung mit der analytischen Vorhersage auf 0,2–7,3 %.

**Wichtige Einschränkung:** σ∝m ist ein **Postulat**, nicht aus der
Geometrie ableitbar (analog zum unerklärten Äquivalenzprinzip der
Standardphysik). Und: die zwei historisch als entscheidend geltenden,
unabhängigen Probleme jedes Schattenwurf-Mechanismus — **Aufheizung**
durch absorbierten Impuls und **Bahnwiderstand** durch Aberration bei
Bewegung — werden hier nicht getestet und bleiben ungelöst. Fazit dort:
"immer noch nicht guten Gewissens implementierbar als physikalische
Behauptung", aber präziser gefasst als vorher.
