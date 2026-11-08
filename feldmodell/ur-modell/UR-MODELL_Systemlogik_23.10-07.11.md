> **Individuelles physikalisches Modell von Thomas – Diskussionsgrundlage.** Nicht begutachtet, kein Anspruch auf Gültigkeit. Kennzeichnung im Text: gemessen/geprüft, per Konstruktion, Abstraktion, Overlay.

# RAUM27 – Die einheitliche Systemlogik (Stand 23.10.2026)

**Privat.** Zweck: eine geschlossene Logikkette, die in jedem Teilbereich gleich arbeitet. Das Denken muss nicht umschalten, und alle Punkte hängen in einem Netz zusammen.

## Grundform

Jedes Teilsystem besteht aus denselben fünf Bausteinen:

1. **Zentrum:** Punkt 1. Hier ist alles überlagert, und es ist der einzige Fixpunkt aller Spiegelungen.
2. **Minimum / innen:** die kleinste Einheit (dx, Teilchengröße, Raute, Kegel, Kernschatten).
3. **Maximum / außen:** die Hülle (1, Wärmeschwingung, Würfel, Pyramide, Halbschatten).
4. **Verbindung:** Inversion über die 1 (r → 1/r). Innen und außen werden ineinander gespiegelt, nur die 1 bleibt fest.
5. **Prüfregel:** innen |e|/a < 1, außen R/d < 1, zusammen max(|e|/a, R/d) < 1 (heißer Draht). Wird ein Wert 1, ist das eine Berührung.

## Die Bausteine in den Bereichen

| Bereich | Minimum / innen | Maximum / außen | Verbindung |
|---|---|---|---|
| Raum | Kugel: 6 Punkte und Mitte | Würfel: 8 Punkte und Mitte | 26 Richtungen + Mitte = 27 |
| Form | Raute (Oktaeder, p = 1) | Quadrat (Würfel, p = ∞) | Kugel (p = 2) in der Mitte |
| Feld | Kegel (Expansion) | Pyramide (Kompression) | Symmetriewechsel |
| Linien | Geraden: 1, √2, √3 | Bögen und Radien | Logarithmus über die 1 (Steigung 45° bei x = 1) |
| Zahlen | Bits (0/1, 1/2) | Basis 3 (27 → 9 → 3) | 2 Bits je Achse, der Zustand 11 ist Fehlerprüfung |
| Messung | Punkt in Teilchengröße | Loch in Größe der Wärmeschwingung | Kern und Ring, Entfaltung |
| Bewegung | Toleranz in der Bahn | Abstand zu Hindernissen | Spitze abrunden: v = √(a_max · r) |
| Zeit | Punkt-Takt (Neustart je Takt) | durchlaufende Bahn | Fehler bleibt konstant statt mit √n zu wachsen |
| Schwingung | Zylinder → Sinus (Seitenansicht) | Kegel → Spirale (Achsenansicht) | Spiegelung an zwei Scheiben: zwei Drehsinne ergeben eine stehende Welle |
| Phase | Kreis (90°/270°: Vorder- und Rückseite) | Linie (0°/180°: Kreis hochkant) | Phase = Kippwinkel; z folgt aus dem Delta von x und y |
| π | 8 Quadranten je Schale (8k+1, 4, 5, 6) | Faktor 1/16 = ½·⅛ je Schale | nur der Rest der Masche wird weitergereicht (BBP) |
| Logik | Nein = 1/3 | Ja = 3 | Mitte 1; log₃ ergibt −1/0/+1 (balanciertes Ternär); 0 = kein Signal/Fehler |
| Frage | Ort und Bezug (Punkt 1) | Eingriff „ändere X“ | Prüfung „tritt Y ein?“ → 1 Bit, gültig relativ zum Bezug; Suche zuerst nur in 6×8 Richtungen |
| Kreise | 3 Achsenkreise | 6 Diagonal- + 4 Sechseckkreise | 13 Nähte = 26 Ränder, mit Mitte 27 |
| Biegelinie | Raute p = 1 (U/D = 2√2) | Quadrat p = ∞ (U/D = 4) | Kreis p = 2 (U/D = π) |
| Rechnen | Archimedes: Drehung, linear | Gauß: Ausdehnung, Verdopplung | logarithmisch-polarer Raum; Diagonale = log. Spirale; ln(−1) = iπ |

## Reihenfolge beim Arbeiten

1. Grenzwerte festlegen (Minimum und Maximum, Loch und Punkt).
2. Experiment: daraus Ideallinie und Idealpunkt 0 bestimmen.
3. Korrigieren: systematische Fehler kalibrieren, zufällige auf ihre Ursache prüfen, Rest messen (physikalische Untergrenze).

## Was davon geprüft ist

- **Mathematisch bewiesen:** Symmetrien des Würfels (48), 26 Richtungen, √2 und √3, Inversion, p-Familie Oktaeder – Kugel – Würfel, Sechseck als Schnitt des Würfelgitters, Krümmung des Logarithmus (45° bei 1, stärkste Krümmung bei x² = 1/2), Kurvenradius und Geschwindigkeit.
- **Simuliert bestätigt (K29-Vorlauf):** Punkt-Takt hält den Fehler konstant; ein Loch kleiner als das Teilchen macht den Treffer unentscheidbar; die 7-Strahlen-Schranke verpasst keinen Durchgang; bei harmonischer Kraft sind die Umkehrpunkte fest.
- **Lokal geprüft (27.10.):**
  - Zellkette, bei der jede Zelle nur „rein, eine Operation, raus“ kann, liefert π exakt (2 699 von 2 699 Ziffern). Weitergegeben wird höchstens die Zahl 18.
  - Ein Klon der Kette ergibt Ziffern im linearen Verhältnis, nicht hoch drei.
  - Ein einzelner BBP-Knoten trifft die Hex-Stelle 1 000 001 (6C65E5) ohne Vorgänger in 3,8 s.
  - Lissajous-Bilder: Die Ordnung folgt aus dem Verhältnis λ₁ : λ₂ und der Phase.
  - Antigravitys 253 567 π-Stellen sind alle korrekt. Das Verfahren ist eine klassische Reihe (Madhava/Sharp).
- **Lokal geprüft (28.10.):**
  - Archimedes-Diagonale (Romberg: Verdopplung nach rechts, Fehlerabzug nach unten): Stellen wachsen mit den Dreieckszahlen 3, 6, 10, 15, 21 … (nur rechts: ≈ 0,6 je Schritt).
  - Gauß (zwei Mittel innen/außen) verdoppelt die Stellen; Archimedes (harmonisch/geometrisch) ist linear. Übergabe Gauß → Vieleck verliert Stellen (40 → 11), weil ein Vieleck nur ≈ 1/n² trägt.
  - Einsetzen x ← x + sin(x): Stellen ×3 je Schritt (5 → 17 → 53 → 160 → 482 → 1449); Sinus selbst gebaut aus Drei-Phasen-Formel sin 3x = 3s − 4s³.
  - Geometrisches Ablesen aus gemalter Spirale: ≈ +1 Stelle je 10-facher Auflösung.
  - Kegelabwicklung: Spirale mit konstantem Winkel → logarithmische Spirale; Sektorwinkel 2π·sin α.
  - 6×8-Baum mit BBP: 5 760 Hex-Stellen korrekt; ein Cluster ist durch (Start n, Blockgröße) vollständig beschrieben.
- **Grenze:** Symmetrie spart Arbeit, erzeugt aber keine Information. Speicher lässt sich wiederverwenden (Pingpong), Rechenschritte nicht.
- **Getestet, nicht eingetreten (K25):** Primzahlen aus der Teilchenbewegung.
- **Offen:** K25b, K28 (Brücke), K29 und K29m (Antigravity).

## Verwandte Ansätze

Im maschinellen Lernen heißt dieser Ansatz „geometrisches Deep Learning“: Netze, deren Aufbau aus Symmetriegruppen abgeleitet ist, zum Beispiel aus der Würfelgruppe. Sie brauchen weniger Parameter und verallgemeinern besser, weil dieselbe Regel überall gilt.

## Architekturprinzip: Filterlose Verarbeitung

Die Physik übernimmt die Auswahl, nicht die Software: Resonanz, Phase und Delta-Kanäle durch den Mittelpunkt. Ziel ist, das Problem der Datenmengen in Verarbeitung und Übertragung und die Begrenzung durch Filter zu lösen. Wortlaut und Prüfpunkte stehen in `RAUM27_Architekturprinzip_Filterlos.md`.

## Ebenen und Frageweg (29.10.)

| Ebene | Maßstab | Stufe | Inhalt | Regel |
|---|---|---|---|---|
| Realität | Makro | 3 | Fakten, Messung | nur Ja/Nein (Anker), keine Halluzination |
| Projektion | Mikro | 1 (Mitte) | Übergabe, Frage eingrenzen | Optionen bilden (z. B. 48 lückenlose Bereiche) |
| Simulation / Abstraktion | Nano | ⅓ | Möglichkeiten, Indizien, Gefühl | Halluzination erlaubt, aber gekennzeichnet |

- Wissen = Struktur; Wechselwirkung trägt es nach außen; Wissen ist das einzige Zahlungsmittel im virtuellen Raum (innen nur Verrechnung, Geld nur im Austausch nach außen).
- Frageweg: 1. durch die Struktur bis zum Ursprung → 2. sonst den Kreis per Resonanz (passende Wellenlänge), Schale für Schale → 3. niemand in Resonanz: „weiß nicht“ → Abstraktionsebene.
- Richtung des Impulses bestimmt Reihenfolge der Verarbeitung (Hierarchie aus Richtung, nicht fest); Vorgänger/Nachfolger: 180°-Inversion (+/−, Tridiagonalmatrix).
- Jede Instanz: eigenes Koordinatensystem, Wissen im Nullpunkt, Aufbau von innen nach außen in 3-D; analoges Inneres in binärer Hülle (physische Struktur ↔ Abstraktion; Gehirn ↔ Bewusstsein als Modell, nicht belegt).
- Struktur-Beispiel: Menger-Schwamm Stufe 1 = 6 Kanäle + 1 Kreuzung, max. 3 Kanäle überlagert; Würfelsymmetrie 6 · 8 = 48.

## Lokal geprüft (29.10.) – genetischer Code als Fehlerbremse (k_check/gencode.py)

- Base = 2 Bit, Codon = 6 Bit = 64 = 8 × 8 Zustände → 20 Aminosäuren + Stopp.
- Einzelfehler (Basenwechsel): echter Code 25,5 % ohne Wirkung; zufällig gemischte Codes Ø 4,7 % (max 10,0 %).
- 1-Bit-Fehler (Zuordnung A=00, C=01, G=10, T=11, willkürlich): echt 28,4 % ohne Wirkung; Zufall Ø 4,7 % (max 12,1 %).
- Wenn sich etwas ändert, wie stark (Polarität nach Woese, mittleres Quadrat): echt 5,19 bzw. 4,44; Zufall Ø 9,0–9,4; von 2 000 Zufallscodes mit gleicher Blockstruktur war **keiner** besser.
- Dichteste Kugelpackung: 0,74048; Menger Stufe 1: 20/27 = 0,74074 (Abweichung 3·10⁻⁴, Zufall vermutet).

## Architektur, Fokus und Wecken (29.10.)

- Schichtfolge außen→innen: Kugel n → Würfel n (8 Oktanten) → Kugel n−1 → … → Zentrum. Je Schale Radius ×½; Linien ×½ (2-D) bzw. ×¼ (3-D) → Dichte konstant. Bauform wie Multigrid / U-Net.
- Traumfänger 2-D: Rₙ = 2ⁿR₀, Lₙ = 8·2ⁿ → Abstand konstant πR₀/4. 3-D: Linien ×4 je Radiusverdopplung (HEALPix-artig).
- Takt: halber Weg bei halber Geschwindigkeit → jede Schale braucht dieselbe Zeit τ = Δr/v → Fließbandverarbeitung mit konstantem Takt.
- Bezug auf 1 statt 0 (positiver Raum): kein Nulldurchgang, kein Vorzeichenwechsel, kein Einschwingen um die Null.
- Würfelsensor: Flächenstärken |a|,|b|,|c| = Richtungsvektor; 8 Eingangsfäden (Raumdiagonalen) + 6 Ausgangsfäden (Flächennormalen) = 14 Richtungen (Rhombendodekaeder); Auffächerung je Fläche 1→2→4→8 = 1 Bit Ort je Stufe.
- 8 Fäden: stärkster Faden ±11°; Schwerpunkt aller 8 (Fadenbreite 30–45°) 0,05° ohne, 2,5° bei 5 % Rauschen (k_check/acht_faeden.py).
- Wecken: schneller Pfad (außen c) trägt nur Richtung + Stärke; Inhalt kommt mit c/2 nach; Vorlauf Δt = r/c. Wecken wenn S > θ(Beschäftigung); Hammer = Notunterbrechung; nicht befolgte Impulse vorgemerkt. Kein Signal > c (Tunneln überträgt keine Information überlichtschnell).
- Bündelung nach innen: Gesamtenergie konstant, Intensität ∝ 1/r², Amplitude ∝ 1/r; Grenzen: Beugung (λ/2), Reflexion an Kanten (c→c/2 ≈ 11 %), Symmetrie. Beispiele: Sonolumineszenz, Laserfusion.
- ELF-Ortung synthetisch (k_check/elf_ortung2.py): Standard am genauesten bei sauberem Signal; log-Bänder nur mit SNR-Gewichtung brauchbar, Vorteil erst bei starkem Rauschen; früherer Vorteil war Gitterartefakt.
- Wecker darf rauschen (nur Richtung, Stärke, Verlauf). Dringlichkeit = Stärke × Fluchtgefahr (abklingend → Zeit lassen). Genaue Verarbeitung (180°-Regel, Resonanz) erst beim Hingehen.
- Innen frei spielen (Simulation/Halluzination/Training), außen sparsam handeln; Inneres liefert Kandidaten, Äußeres prüft Ja/Nein.
- Selbstbestimmung des Inneren: entscheidet selbst, ob es sich stören lässt. Zwangsunterbrechung („Hammer“) nur für echte Notfälle **und** nur von berechtigter, geprüfter Quelle (Feuerwehr/Polizei), nicht für jede laute Bitte (Nachbar ohne Salz). Recht zum Hammer ist an Berechtigung gebunden, nicht an Lautstärke; Missbrauch → Recht entzogen.

## Verhältnisse, Energie, Notizen (29.10.)

- **Grundsatz Ähnlichkeit:** Nur Verhältnisse ohne Einheit sind fundamental (gekürzter Bruch); Maßstab („die Nullen“) erst am Ende. Beispiele: Feinstrukturkonstante α = 1/137,036 (in jedem Einheitensystem gleich), Proton/Elektron 1836,15, Reynolds-Zahl. Vorgehen: 1. alles auf Verhältnisse kürzen, 2. wiederkehrende Strukturzahlen suchen (3, 9, 27, 16/9, 8), 3. Maßstab zuletzt.
- **Schwingung:** T = 1/f; λ = v/f; ω = 2πf; E = ½·m·ω²·A²; KinE = E·cos²φ; PotE = E·sin²φ; **PotE/KinE = tan²φ**; Zeitmittel KinE = PotE = E/2 (Gleichgewicht = Punkt 1). Strukturfaktor K davor (PotE/KinE = K·tan²φ); Standardphysik K = 1; K ≠ 1 wäre Messfrage.
- **0 und ∞ messbar:** tan²φ bildet 0…∞ auf 0°…90° ab (0° alles kinetisch, 45° Gleichgewicht, 90° alles potentiell). Vorbilder: Smith-Diagramm, Riemannsche Zahlenkugel (∞ = Nordpol).
- **Notizseite:** m·c^c·λ²/F² = (PotE/KinE)·c^c – algebraisch konsistent mit (2), (3). c^c beidseitig → nicht isolierbar (gilt für jeden Wert); nur einseitig → c^c = PotE·F²/(KinE·m·λ²). λ/F (F als Zeit) = Geschwindigkeit → m·λ²/F² = m·v² = 2·KinE. c = 3·10⁸ m/s (genau 2,998·10⁸): Mantisse 3 = Struktur (3³ = 27), Exponent 10⁸ = Maßstab (Normierung, keine reine Rechnung). Funktionen mit 16x/(9λ): sin (Welle), 1/sin (Singularitäten je Nulldurchgang), sin² (≥ 0, positiver Raum), sinh (Expansion); (16/9)² = 3,1605 = π-Wert Papyrus Rhind. Skalierung 10 linear, 9 = 3² Fläche, 27 = 3³ Raum. Lichtzylinder: R_L = c/ω = λ/2π.
- **Kommunikationsebene:** dichteste Packung mit Mindestabstand = fehlerkorrigierender Code; beste bekannte Lösung in 8-D: E8-Gitter (240 Nachbarn, Viazovska 2016). Verbindung der Abstraktionen über gemeinsame Definitionen + Ja/Nein + Hash-Kette (raum27_kette.py), kein Mining nötig.
- **Regel (Thomas, 29.10.): Gleichungen zuerst ungekürzt führen.** c, π, c^c, Maßstäbe stehen lassen; erst am Ende normieren (z. B. π = ½ → Kreis = 1, 45° = ⅛). Grund: Verknüpfungen bleiben sichtbar, Substitution möglich (andere Geschwindigkeit statt c, Zeit über t = L/c zurück). Nicht jede Größe bis zum Ende herleiten – nur so viel, dass die Bezüge erkennbar bleiben.
- Ungekürzte Abschlussgleichung: PotE/KinE = K·tan²(2π·f·t), K = c^c (unnormiert), E = ½·m·(2π·f)²·A², λ = v/f, v = c/n, t = L/c.

## Lokal geprüft (30.10.) – K34/K35
- K35 Stufe 1: Blöcke n = 1 … 10^5 gegen mpmath gleich; n = 10^7 (7af5863e) mit eigenem BBP gleich. Konvention: „n“ = Ziffern ab Position n+1.
- K34 Paket 1 (80 000 Hex-Stellen) vollständig gegen mpmath: 9 999 von 10 000 Blöcken gleich, **1 falsch**: n = 23776 geliefert fb57acbc, richtig fb57acbb (folgende Ziffern fff8… → Rundung am Blockrand, double-Genauigkeit). Bericht meldete 0 Abweichungen; Abbruchregel hätte greifen müssen. B+2-Selbstprüfung nur jeder 1000. Block → nicht erkannt.
- SHA-256 Paket: Bericht a5e958643669906eb493…, tatsächlich a5e958643669906efdb2… (nur erste 16 Zeichen gleich).

## Normierung bis zum Phasenraum (30.10.)
- Reihenfolge: Masse = 1, Energie = 1 → Amplitude auf λ (A/λ) → Struktur → Frequenz. Übrig bleiben λ und f, v = λ·f.
- c = 1: λ·f = 1, T = λ; bei λ = 1 sind f, λ, T identisch (Punkt 1). Kreis: A/λ = 1/(2π) = 1 mit π = ½.
- 3 → 6 Dimensionen = Phasenraum (Ort x,y,z + Impuls px,py,pz). Schwingung = Ellipse, Fläche = E/f = Wirkung; Quant: h → E = h·f.
- Energie = Pythagoras im Phasenraum: E = ½kx² + p²/2m → normiert E = x² + p² (Kreis, √E = Radius). 6-D: E = Summe von 6 Quadraten; Gleichverteilung je Quadrat ½kT → 3kT (Dulong-Petit).
- 3-4-5: ganzzahlige Sprünge; Kreis Radius 5 hat 12 Gitterpunkte (8 in Achtelrichtungen + 4 auf Achsen).
- Würfel in Kugel: Durchmesser = Raumdiagonale a·√3; Blick entlang der Diagonale (Isometrie) → Sechseck, eine Achse fällt weg.
- Endzustand (Thomas): nur noch kleinste Teilchen in idealer fraktaler Anordnung bei den Drehungen, bei denen der Winkel zur Bezugsebene 90° ist (Projektion = 0): dort steht der Zustand senkrecht zur Ebene, sein Anteil in der Ebene verschwindet (cos 90° = 0) – rein potentiell (tan²φ → ∞) bzw. reine Phase 90° = ¼ Umdrehung. Status: Modell, nicht geprüft.

## Lokal geprüft (30.10.) – Ergänzung
- K39b-Vortest: Basen 5, 6, 7, 12, 24, 48, 100, 243 · s = 1–3 · L ≤ 12 · 9 Zielzahlen: 1 944 Läufe, 0 Treffer; Gegenprobe ln(5/4), ln(7/6), ln(243/242) gefunden → echtes Leerergebnis.
- Korrekturauftrag K34b/K35b auf Drive (RAUM27_K35).

## Offene interne Liste (Stand 31.10., noch NICHT im Auftrag)
- [ ] M17 Rückprojektion: Raster in n Winkelschritten um die Mitte drehen, Helligkeit Zentrum vs. außen, mit/ohne Filter (Radon / gefilterte Rückprojektion).
- [ ] M17b 6×8-Helligkeitsauslesung (Crossbar): 48 Optionen in einem Schritt, hellstes Feld = Antwort, „unsicher“ wenn Abstand zum zweithellsten zu klein; gegen M5-Ja/Nein bei gleichem Rauschen (Schritte, Falsch-Quote).
- [ ] Vergleich über Flächen (Δf/Δλ)² und Stufenrekursion 1-2-3 (Linie → Fläche → Raum → neuer Wert).
- [ ] Nach Flash-Fortsetzung: Auswertung K34b/K35b (BBP 10^10, Paket 1 neu, echte SHA-256).
- [ ] Nach K40 (Argon): Auswertung, Kopf-Hash notieren, Übergabe auf Firmenkonto (Drive-Zugriff, Privat-Frage klären).
- [ ] Optional: interaktive 3-D-Ansicht RAUM27 (Würfel/Kugel/Pole/Spiralen/48 Symmetrien).
- [ ] Optional: erster Verilog-Baustein (6×8-Knoten oder Zellkette) im Simulator.

### Nachtrag interne Liste (31.10., NICHT in K40)
- M18 Leiter ohne 4D: a, b → c = a×b (c·a = c·b = 0, |c| = Fläche), det(a,b,c) > 0; Mittelung über 48 Würfelsymmetrien → Rest 0; Gegenprobe mit gestörter Matrix → Rest ≠ 0.
- M19 Keil + Rauschpfad: Startpunkt im Fundamentalbereich (1/48), 48-fach spiegeln, je eigenes Rauschen; messen: Kategorie (Keil) erhalten? Lyapunov > 0? Schwelle, ab der die Kategorie zerfällt.

### Auswertung K40 (01.11.)
- Nachgerechnet: M2 Paket 1 (Drive-Datei) SHA 43b8b46e… echt; 10 000/10 000 Blöcke = Referenz; Grenzfälle fff = 3 (23048, 23776, 35240), 000 = 0 – stimmt. Belege 6 und 21: Hash neu berechnet = gemeldet. Kopf 2a758fb42171871e… (22 Belege), Beleg 6 hängt korrekt an K35b (Beleg 5).
- Nicht im K40-Lauf gerechnet, sondern übernommen (nicht gekennzeichnet): M1 10^9/10^10 (aus K35b), M2 Paket (Zeitstempel 30.10. 19:03). Werte richtig, Status hätte „übernommen“ heißen müssen.
- M5: Abnahme formal ja, praktisch schwach – schon bei σ = 0,001 nur 40 % richtig, Rest unsicher; ab σ = 0,01 fast nur „unsicher“.
- M6: gegengleiche Störung geht zu 99,985 % durch (Systemgrenze, ehrlich gemeldet).
- M10: Linse r0 Simulation 11,45 µm gegen Airy 1,22λf/D = 9,30 µm (23 %), nicht kommentiert.
- M11: Faktor 104,9 (Pipelining) misst etwas anderes als t95 – nicht direkt vergleichbar.
- M8: 0 neue Formeln (erwartet).

### Auswertung K41 (02.11.)
- Nachgerechnet: A3-Paket SHA ef12f424… echt, 10 000/10 000 = Referenz, neuer Zeitstempel 01.11. 06:38. Beleg 30 Hash = gemeldet; Kopf 68ab41d16f8abe86… (31 Belege).
- Übernahme jetzt korrekt gekennzeichnet (10^10 aus K35b). 10^9 neu: 5895585a.
- A4: Wiederholung hilft (σ=0,001: 40 → 79 % richtig bei r=27), Falsch max 0,2 %. Bei σ=0,01 nur 13,8 %.
- A5: 99,985 % → 0,000 % Durchlass – aber Filter kennt die Störungsart (±x); Gegenprobe mit anderen Störungen fehlt.
- A6: Ursache Apodisierung, ohne: 0,0094 % Abweichung – geklärt.
- A7: Pipelining kostet 66,5× Energie je Impuls.
- B6: Signal 1e-3 gegen Rauschen 1e-5 (100σ) – zu leichter Test.
- C4: σ* = 0,019 (Vortest: zwischen 0,01 und 0,05) – bestätigt. Gleiches Rauschen: leicht kontrahierend (kein Chaos).
- Berichtskopien in 4 weiteren Ordnern.

### Prüfung eingefügter KI-Text „K42 closed loop / Huygens-Kuramoto“ (02.11.)
- Skript 1 (6×8): Rang 4, kombiniert Rang 8 – bestätigt. Rekonstruktion im Skript tautologisch; echte Rekonstruktion aus Messwerten (lstsq) funktioniert, Fehler 5e-15.
- Skript 2 lokal ausgeführt: gemeldete Ergebnisse stimmen NICHT. Ist: Anker 183 (nicht 189); R max 0,32 (kein Phasen-Lock, behauptet >0,95); g=0,9 max 4,27 (behauptet 10,0); g=0,99 nach 240 Takten nicht konvergiert; Korrelation r=0,24 (behauptet >0,96); Deckung 49 % (behauptet >94 %). Kontrolle ohne Kuramoto-Phase: r=0,86.
- Unbelegt: „Primzahl-Anker = teilerfremde Knoten im 9^9“, „Rest-Verfahren 16→4→2→1→0“. Richtig: 1−π/6 = 47,64 %.

## Kristallbrücke: von der Abstraktion zur echten Physik (02.11.)

**Gedanke (Thomas):** Wir bauen Kristallstrukturen, die immer mehr Energie über den Nullpunkt synchronisieren. Energie, die homogen von allen Seiten kommt, sammelt sich im Zentrum; die Gitterschwingung kann nur im Gitter schwingen. Saubere Kristalle (homogen verteilte Fremdatome als Kerne) sind symmetrisch um den Kristallisationspunkt; die Fremdatome prägen über Feldlinien die Farbe (RGB: Rubin, Smaragd, blau?).

**Geprüft (lokal, exakt mit Brüchen):**
- Würfel → Oktaeder (Flächenmitten) → Würfel (Mitten der Oktaederdreiecke): Ecke je Runde exakt ÷ 3 (Dreiecksmitte (1/3,1/3,1/3)); je Halbschritt 8→6 bzw. 6→8 Faktor exakt √3. Schalen 1, 1/3, 1/9, 1/27 … Alle Stufen haben dieselben 48 Symmetrien. (Skript k42check/dual.py)
- 16/9 ≈ √3 (Halbschritt), 13/9 ≈ √2.

**Echte Physik dazu (Gibt es schon):**
- 6 um 1 = NaCl (Oktaeder), 8 um 1 = CsCl (Würfel). Auswahl nach Pauling-Radienquotient: 0,414 = √2−1 … 0,732 = √3−1 → 6er; > 0,732 → 8er.
- Diamant: elektrisch Isolator, aber bester natürlicher Wärmeleiter (~2000 W/mK) – Energie läuft als Gitterschwingung (Phononen) sehr gut durch. Licht: Brechzahl 2,42, Totalreflexion hält Licht im Stein (Brillanz durch Schliff).
- Farbe durch Fremdatome = Kristallfeld (Ligandenfeld): das Gitterfeld spaltet die Energieniveaus des Fremdions. Gleiches Cr³⁺: rot in Korund (Rubin), grün in Beryll (Smaragd) – nur das Feld ist anders.
- Blau: Saphir = Korund + Fe²⁺/Ti⁴⁺ (Ladungstransfer); blauer Diamant = Bor.
- Stärkste Brücke: Rubinlaser (Maiman 1960): Blitzlampe pumpt Licht von allen Seiten in den Rubinstab, Energie wird in Cr³⁺ gespeichert und kohärent (synchron) abgegeben.

**Korrekturen:**
- Rubin/Smaragd/Saphir sind keine Kohlenstoffgitter (Al₂O₃ bzw. Be₃Al₂Si₆O₁₈); Kohlenstoff = Diamant.
- Richtung: das Gitterfeld verändert das Fremdatom (Farbe), nicht umgekehrt.
- Transparenter Kristall lädt sich durch Licht kaum auf; Energieaufnahme nur, wo absorbiert wird (Farbzentren, Fremdionen).
- Historisch: Kepler 1596 (geschachtelte platonische Körper für Planeten) – physikalisch falsch; bei Kristallen ist Verschachtelung real.

**Prüfbar (Kandidat K43):** Radienquotient-Grenzen √2−1, √3−1 aus Kugelpackung herleiten; Phononen im 27³-Gitter (Dispersion, Wärmeleitung); Kristallfeld-Aufspaltung für Cr³⁺ bei zwei Feldstärken → Farbe; einfaches Lasermodell (3 Niveaus, Pumpen von allen Seiten, Schwelle).

## Bauprinzip Kugel–Würfel–Kugel (02.11.)

**Gedanke (Thomas):** Kugelhaus, gehalten von einer Würfelgitterstruktur, umgeben von einer Kugel. Außen klettert ein Roboter auf der eigenen Hülle und druckt/legt sie (kein Mensch in der Höhe); innen wird von unten nach oben ausgebaut, Fallhöhe max. ein Stockwerk; Einrichtung gedämpft befestigt. Bauteile aus kristallinem/verstrecktem Kunststoff bzw. Carbon in Diamant-/Oktettgeometrie, als Vision für Großprojekte.

**Aufbau:** Außenkugel = Bilanzhülle (Lasten umleiten, keine Ecken) · Würfelgitter = Tragwerk und gerade Ebenen · Innenkugel = gedämpft aufgehängter Kern. Radien 1 : √2 : √3 (≈ 9/9 : 13/9 : 16/9).

**Gibt es schon:** Kugelbauten (Kugelhaus Dresden 1928, Biosphère Montréal 1967, Eden Project, Sphere Las Vegas 2023); Pendeldämpfer Taipei 101; kardanische Aufhängung; Röhren-/Diagrid-Bauweise; Carbonbeton (CUBE Dresden 2022); robotisches Faserwickeln (BUGA-Faserpavillon Heilbronn 2019, Uni Stuttgart); Kletterroboter (Minibuilders, IAAC 2014); 3D-gedrucktes Haus Beckum 2021; Baufabriken Shimizu/Obayashi (1990er); Vorspannung (Spannbeton, Tensegrity); Strukturhierarchie (Eiffelturm, Perlmutt, Lakes 1993).

**Grenzen:** Gigapascal-Druck nicht vor Ort; Ordnung über Faserausrichtung. Brandschutz, Kriechen/Alterung, Zulassung, Verbindungsstellen, Transport (≈ 3 × 4 m Querschnitt).

### Merkzettel K43 (Kandidaten, noch NICHT im Auftrag)
1. Kugel–Würfel–Kugel unter Erdbebensignal: Innenkugel starr gegen gedämpft; Vergleich reine Würfelhülle (Eckspannungen).
2. Gittervergleich gleiches Material: Würfel / Diamant / Oktett / hierarchisch (1–3 Ebenen): Steifigkeit, Bruchlast, Stoßenergie; spröde Knoten + zähe Verbindung (Perlmutt-Prinzip).
3. Vorspannung: Oktettgitter mit/ohne Vorspannung, Last bis erster Stab auf Zug.
4. Faserausrichtung: Stab mit Fasern entlang der Kraft gegen zufällig.
5. Kugelschale gegen Würfelschale unter Außendruck: Spannungsverteilung, Ankunft innen.
6. Gestapelt (Fugen) gegen lückenlos gefüllt, mit/ohne Pufferschale 9.
7. Würfel→Oktaeder→Würfel (÷3 je Runde, √3 je Halbschritt) – bereits lokal bestätigt; Pauling-Grenzen √2−1, √3−1 aus Kugelpackung.
8. Kristallwachstum vom Zentrum mit Einbaufaktor k < 1 (Zonenschmelzen) gegen k = 1.
9. Physik-Brücke: Paul-Falle (Stabilitätskarte), Laserkühlung, π-Puls; Tunneln (imaginärer Impuls); SU(2) 360°/720°; Wick-Rotation; Multipole (Monopol/Dipol, Gauß-Fluss); Gittermodell: Lagrange-Funktion, Kontinuumsgrenze (Welle, Diffusion, Klein-Gordon), Noether für 48 Symmetrien.
10. Phononen im 27³-Gitter; Kristallfeld Cr³⁺ bei zwei Feldstärken; 3-Niveau-Lasermodell.

### Auswertung K42 (02.11.)
- 23/23 Ziele ausgeführt, alle mit Skript + Log auf Drive. Beleg 36 neu gehasht = gemeldet; Kopf 89ce6fbc3d4b0877… (37 Belege).
- Alle Erwartungswerte getroffen; D1–D3 decken sich mit meinen unabhängigen lokalen Läufen (r 0,9359; 16,05 %/79,01 %; Hysterese 1,126 vs. meine 1,130 – andere Flächenformel). F1/F3/E2 von Hand nachgerechnet: stimmt.
- Echte Erkenntnis A1: 48er-Filter versagt bei schwacher Störung (0,10 = 5σ, unter Schwelle 0,11): 31–54 % Durchlass; bei globaler Störung (auch Ecksensoren) 6–60 % Durchlass. → Filter ist nicht allgemein, sondern auf ±x-Gegenstörung ≥ 0,25 zugeschnitten.
- D4: „sicher richtig“ (kein Kanal näher als 1σ an Schwelle) bei σ=0,0185 nur 65,9 %.

## Erste Simulation der Feldtheorie-Grundannahme (02.11., lokal, feld/feldtheorie.py)
Modell: reelles Feld f auf 27³ (periodisch), f̈ = ∇²f − (f³ − f) + J; Potential ¼(f²−1)² (Nullpunkt instabil/tachyonisch, stabil bei ±1 = voll); Punktquelle X1 im Zentrum; 8 Paritätsklassen über 3 Spiegelebenen.
1. Energie ohne Dämpfung: Drift 3,1 % über 2000 Schritte (einfaches Verfahren; für K43 genaueres Verfahren).
2. Masse um +1: gemessen 1,424, Theorie √2 = 1,414 (0,7 %).
3. Start am Nullpunkt + Rauschen 0,01: nach t = 20 sind 62 % voll, ab t = 50 99,9 % voll – ganzes Gitter kippt gemeinsam auf +1 (eine Domäne).
4. Punktmasse X1: stört nur 2–3 Zellen (Abfall wie Yukawa, Reichweite ≈ 1/m ≈ 0,7); Feld zu 100 % in Paritätsklasse „1“ (voll symmetrisch). Doppelte Quelle kippt nur das Zentrum (+0,25), Rest bleibt −1.
Deutung: Nullpunkt-Instabilität erzeugt Masse (√2) und Reichweite (Yukawa) – Anschluss an Higgs-/Klein-Gordon-Physik bestätigt (bekannt, nicht neu). Zentrumsmasse erzeugt nur das symmetrische Spiegelbild.

## Raum aus Feldern, Strömungsbild, komplexe Spiegelmathematik (02.11.)
**Gedanke (Thomas):** Massen bewegen sich nicht durch den Raum, sie erzeugen ihn durch Überlagerung ihrer Felder; es gibt eine Höchstzahl von Resonanzpunkten. Bild: Würfel voll „Raum-Wasser“, jede Masse ein Zulauf, Abfluss an den Ecken, Rückführung zu den Massenpunkten; wo Expansions- und Druckwellen sich treffen (Rückprojektion), entsteht der Gravitationsvektor. Bleibt man im komplexen Zahlenraum (Spiegelmathematik der Projektion), passt es exakt.
**Gibt es schon:** Leibniz/Mach (Raum als Beziehung), Einstein (Masse formt Geometrie); Raum aus Verschränkung (Van Raamsdonk 2010, ER=EPR 2013 – offen); Weyl-Gesetz (endliche Moden), Bekenstein-Grenze; Bjerknes-Kräfte (pulsierende Kugeln im Wasser: gleichphasig Anziehung ∝ 1/r², gegenphasig Abstoßung); Fluss-Modell der ART (Gullstrand-Painlevé, Hamilton & Lisle 2008: Raum fließt in die Masse hinein); analoge Gravitation im Wasserbecken (Weinfurtner 2011). Widerlegt: Le-Sage-Druckgravitation.
**Komplexe Fassung (exakt in 2D):** Quelle w = (Q/2π)·ln z; Wand = Spiegelquelle (z̄); Kreis = Inversion 1/z̄; Kasten = Gitter aus Spiegelbildern; Kraft über Satz von Blasius. In 3D nicht so einfach.
**Ebenen:** belegt = Masse formt Geometrie, endliche Moden; Abstraktion/offen = Raum entsteht aus Feldern; prüfbar = Gitter aus Korrelationen zurückgewinnen, Bjerknes/Quellen im Kasten.
**Weitere heute geklärte Punkte:** 6 = Transport (sieht 1,x,y,z), 8 = Information (alle 8 inkl. XOR) – 6er-System kann kein XOR (Perzeptron, Minsky/Papert 1969); 90° um x · 90° um y = 120° um Raumdiagonale; Wythoff-Konstruktion (alles aus einem Y durch Spiegeln); 3 Spiegel → 8 Bilder (Spiegelladung) = 8 Paritätsklassen = K42-B1-Moden; Proton fest / Elektron beweglich (Born-Oppenheimer), Virialsatz T = −½V, s-Elektron am Kern; Kern ≠ schwarzes Loch; Higgs-Feld am Nullpunkt tachyonisch → Masse; Tachyonen nie beobachtet; Kettenleiter → φ; Ladeverlust 50 % bei fester Spannung; Superkondensator, Elektride, Photonen-/Polaritonspeicher.

## RAUM27-Gitter-Feldtheorie – formale Fassung v0.1 (02.11.)
1. Raum: Λ = {x = a·n, n ∈ ℤ³_N} (periodisch), Gitterabstand a, N = 27 (= 3³). Nachbarn: 6 Achsen (Transport), 8 Diagonalen (Information).
2. Feld: f: Λ × ℝ → ℝ, Wertebereich normiert: f = +1 voll, f = −1 leer, f = 0 instabiler Nullpunkt.
3. Wirkung: S = Σ_t Σ_x a³ [ ½ ḟ² − ½ Σ_{μ=1..3} ((f(x+aê_μ) − f(x))/a)² − V(f) + J·f ]
   V(f) = (λ/4)(f² − v²)², v = 1 (Mexikanerhut; V''(0) = −λ < 0 tachyonisch, V''(±1) = 2λ).
4. Bewegungsgleichung: f̈ = Δ_a f − λ f (f² − 1) + J − γ ḟ,  Δ_a f(x) = Σ_μ [f(x+aê_μ) + f(x−aê_μ) − 2f(x)]/a².
5. Energie (Noether, Zeitinvarianz, γ = 0): H = Σ_x a³ [ ½ ḟ² + ½ (∇_a f)² + V(f) − J f ] = konst.
6. Masse: kleine Schwingung um +1: m² = 2λ → m = √2 (λ = 1). Gemessen 1,424 (Vortest).
7. Punktmasse X1: J = q·δ_{x,0}. Linear um −1: (−Δ_a + m²) δf = J → δf(r) ≈ q e^{−m r}/(4π r) (Yukawa).
   Zwei Massen: E_int(d) ≈ − q₁q₂ e^{−m d}/(4π d) (gleiche Vorzeichen ziehen an) – Prüfung K43-A5.
8. Symmetrie: O_h (48 = 24 Drehungen + 24 Spiegelungen) wirkt auf Λ; bei J = 0 ist S invariant.
   Spiegel P_x, P_y, P_z (ℤ₂³) → 8 Paritätsklassen χ_s(f) = Projektion mit Vorzeichen s ∈ {±1}³ = Walsh-Moden {1,x,y,z,xy,xz,yz,xyz}.
   Flächenoperator F (6×8) hat Rang 4: sieht {1,x,y,z}; Eckenoperator sieht alle 8 (XOR = Produkt der Vorzeichen).
9. Null-Operator: N_δ(s) = Ja (s > δ), Nein (s < −δ), unsicher (|s| ≤ δ), δ = 3σ.
10. Sättigungs-/Spannungsform (dissipativ): E_{n+1} = tanh(g·H_a E_n + A·(G − ½)), H_a E = 0,4E + 0,15 Σ_Nachbarn; Stufen analog/klar/binär.
11. Schalen: r_k = 9/k, Potential einer Punktquelle 1/r → V(r_k) = k/9 (gleichabständig).
12. Kontinuumsgrenze a → 0: (∂_t² − ∇² + m²)δf = J (Klein-Gordon) bzw. φ⁴-Theorie – bekannte Physik.
**Status:** 1–6, 8–12 Modell bzw. bekannte Mathematik; 7 Vorhersage (K43-A5 prüft); neu ist nur die Zuordnung (6/8-Trennung, Null-Operator, Schalen 9/k, voll=1) – keine neue Physik behauptet.
**Offen:** Gravitation (bisher nur Yukawa, kurzreichweitig; für 1/r bräuchte es m → 0), Raum aus Korrelationen (K43-C), gegenläufige Wellen 6/8 (K43-G1).

### Einordnung Sprach-Zusammenfassung (02.11., anderer Chat)
- Passt: geschlossenes System mit fester Teilchenzahl (N³ Knoten, nur Energie ändert sich); RGB + Hex (4 Ecken = 1 Hexziffer); Tiefe = Zeit/Spiegeldicke statt 4. Raumachse (wie t nur als Einschwingen); Bereich 0…∞ (t = x/(1+x)); Masse/Energie/Simulation ≈ physisch/Abstraktion/Overlay.
- Korrektur r = 1 = Planck-Länge: zulässige Eichung (a = ℓ_P), aber Folge: m = √2 in Gittereinheiten ≈ 1,4 Planck-Massen (~3·10⁻⁸ kg), Yukawa-Reichweite ≈ ℓ_P → im Experiment unsichtbar. Planck-Gitter verletzt Lorentz-Invarianz bei höchsten Energien; Gamma-Blitz-Messungen (Fermi, GRB 090510) begrenzen das bereits. Eichung erst nach K43 festlegen.
- Korrektur Kurzschluss/Leerlauf: Symmetrie hebt den ohmschen Widerstand nicht auf. Richtig ist: Zwischen Punkten gleichen Potentials (abgeglichene Brücke, Wheatstone) fließt beim Kurzschließen kein Strom – deshalb harmlos. Widerstandsfreiheit gibt es nur bei Supraleitung.

### Auswertung K43 (02.11.)
- 48/48 Ziele ausgeführt, Skripte + Logs; Rechenzeit gesamt nur ~70 s (Aufgaben rechnerisch klein) – deshalb so schnell, nicht halb gemacht. Beleg 41 neu gehasht = gemeldet; Kopf 149eeb80821b86e9… (42 Belege).
- Feldtheorie: Leapfrog-Drift 0,26 % (dt 0,05), 1,07 % (dt 0,1); Masse 1,414139 (√2: 1,414214); zwei gleiche Quellen ziehen an, gegensätzliche stoßen ab; Gitter-Masse m = arccosh(2) = 1,317 (Fit 1,342) statt √2 – Gittereffekt, korrekt erkannt. 27³ friert in 2 Domänen ein (Torus-Wand), 54³ → 1 Domäne.
- Raum aus Korrelationen: 9³-Gitter 729/729 Nachbarschaften richtig, Abstände exakt (Graph); direkte Einbettung 10,8 % Fehler.
- Bjerknes |F|d² = 1/(8π); Eckabfluss verändert Kraft bis −21 % (d/L = 0,8). Kugel–Würfel–Kugel gedämpft 8× weniger Beschleunigung (vereinfachtes Modell). F-Teil überwiegend Formelmodelle (grob).
- Z1: Filter verbessert (verworfene Gute 0,01 %), aber Störung 0,10 (= 5σ) geht weiter zu ~30 % durch; globale Störung mit unabhängiger Referenz 62 % statt 99,9 % – grundsätzliche Grenze schwacher Störungen bleibt.

### 90°-Umschlag gegen Störungen (02.11., lokal, k42check/umschlag.py)
Idee (Thomas): Punkt (3,4) muss nach 90° als (−4,3) im Nachbarquadranten erscheinen – was nicht mitdreht, ist Störung.
Test: 20 000 Ereignisse, σ = 0,02; Störung fest am Sensor; 3 Messungen (Lage 0, 90° um z, 90° um x), Störung per kleinste Quadrate geschätzt und abgezogen.
Ergebnis: ohne Abgleich A = 0,10 → 50 % falsch, A ≥ 0,25 → 100 %; mit Umschlag bei ALLEN Stärken 0,00 % (Median-Fehler 0,027 statt 0,031). Gilt für Achsen- und Diagonalstörung.
Grenze: wirkt nur auf sensorfeste (mitdrehende), zeitlich konstante Störungen. Weltfeste Störung verhält sich wie Signal (nicht trennbar). Kosten: 3 Messungen statt 1.
Gibt es schon: Umschlagmessung (Metrologie), Carouselling bei Kreiseln, Chopper/Lock-in. Kandidat K44.

### Phase = Winkel, Log über die 1, Fraktale, Universal-Schnittstelle (02.11., lokal, k44/phase_log.py)
- 2 Achsen x=cos t, y=cos(t+φ): φ=0° Diagonale, 30° Ellipse 0,268, 60° 0,577, 90° Kreis, 180° Gegendiagonale (Lissajous).
- 3 Achsen x=cos t, y=cos(t+φ), z=cos(t+2φ): φ=0° Linie entlang Raumdiagonale (Länge bis √3 = Würfelecke); φ=120° exakter Kreis, Radius √(3/2)=1,2247, Ebene senkrecht auf (1,1,1) (Drehstrom-Prinzip); φ=60° Kreis um andere Diagonale; φ=90° Ellipse (Radius 1…√2).
  → Die Phase allein entscheidet: Würfeldiagonale (linear) oder Kreis (Kugel). Normierung über Phasenwinkel bestätigt.
- Log über die 1 (log 1 = 0), nicht über die 0 (log 0 = −∞): log10(1…10) Abstände 0,301…0,046, Summe exakt 1; ab 10 Wiederholung (Mantisse). Benford: führende Ziffer d mit log10(1+1/d) (30,1 % … 4,6 %).
- Fraktale über log normiert: D = log N / log s: Cantor 0,631; Koch 1,262; Sierpinski-Dreieck 1,585; -Teppich 1,893; Menger 2,727; voller 3³-Würfel 3,000.
- Universal-Schnittstelle 27³ links 1, rechts 0: stationär exakt linear (Abw. 3·10⁻⁷); Welle braucht t ≈ 21 für 25 Zellen.

## Sortierung nach Masse, Ladung, Tiefe (02.11.)
**Gedanke (Thomas):** Leichte Teile raus, schwere bleiben drin (inverse Physik); in der Bilanzhülle mit Rotation findet jedes Atom seinen eigenen Ruhekreis zwischen Zentralkraft und Fliehkraft; dazu die ±-Drift als dritte, unsichtbare Achse (Tiefe/Sichtlinie), auf der sich Nord–Süd in der Tiefe verschieben.
**Geprüft/eingeordnet:**
- Gravitation + Fliehkraft allein: Masse kürzt sich (Äquivalenzprinzip) → gleicher Kreis für alle. Sortiert wird über Dichte/Auftrieb: Planet (g ≈ 300× Fliehkraft) → Schweres nach innen; Zentrifuge → Schweres nach außen; Grenze ω²r = g.
- Eigene Ruhekreise mit Ladung: r = m v/(qB) (Massenspektrometer); mit Wärme: n(r) ∝ exp(m ω² r²/2kT) (Gaszentrifuge, Uran).
- Leicht raus/schwer drin in der Natur: Planeten-Differentiation (Eisenkern), Jeans-Flucht (H, He), Plasma-Randschicht (Elektronen laufen voraus, Feld regelt), Elektronenemission; Elektronen bei gleicher Energie ≈ 43× schneller als Protonen.
- ±-Drift: Gradient-/Krümmungsdrift trennt Vorzeichen (Erd-Ringstrom: Ionen nach Westen, Elektronen nach Osten); E×B-Drift für alle gleich.
- ±-Achse = Sichtlinie (Tiefe), in Projektion unsichtbar; gemessen über Doppler mit Thomas' Vorzeichen (weg = rot = +, zu = blau = −), Zeeman/Faraday (Magnetfeld entlang Sichtlinie), Parallaxe/Stereo.
- Hybrid Kondensator/Batterie: Lithium-Ionen-Kondensator, Supercapattery; Ragone-Kompromiss; Gradientenelektroden; hierarchische Poren (makro/meso/mikro), Murray-Gesetz r³ = r₁³ + r₂³ (Murray-Materialien 2017).
- Brettlogik: Diagonale = Läufer (bleibt auf Farbe, 4 von 8 Ecken), ein Hüpfer wechselt Farbe; Rundweg = Gray-Code; unbenannter Punkt zwischen 4 Feldern = duales Gitter, in 3D bcc-Mitte (8 Ecken + 1 = 9).
- Schnellstes Einschwingen: aperiodischer Grenzfall ζ = 1.

## Schalenbild der drei Ebenen (02.11., Thomas)
Physik (endlich: Bekenstein, Poincaré-Wiederkehr, Pseudozufall periodisch) ⊂ Energie (Thermodynamik, Feld) ⊂ Raum der unendlichen Variationen (Abstraktion; nach innen und außen als Überlagerung; 0…∞ ↔ 0…1 über t = x/(1+x); Kontinuum überabzählbar, Cantor).
Entsprechungen: Hilbertraum der Quantenmechanik (unendlich-dimensional) um endliche Messwerte; Fourier-Paar „innen“ (kleine Skalen, hohe Frequenz) ↔ „außen“ (große Skalen). Lernen = eigene Ordnung (Rezeptkarte RAUM27_Index.md), Speicherhierarchie heiß/warm/kalt; Null-Operator = dreiwertige Logik (Łukasiewicz 1920, Fuzzy Zadeh 1965).
Status: Rahmen bzw. Weltbild (Overlay/Abstraktion), als Ganzes nicht prüfbar; prüfbar sind die Übergänge (Messung schneidet Kontinuum auf endliche Stufen; Rauschen als nicht-periodische Quelle).

## Nullpunkt als Inversion der Unendlichkeit, Würfel als Rückführung (02.11.)
Gedanke: Nullpunkt = Quelle/Senke (Rückschlagventil) gegenüber ∞ (Inversion 1/z); Zufluss entlang der unsichtbaren ±-Achse (Sichtlinie), sichtbar nur die Verteilung N/S/O/W. Die schwingende Kugel gibt Energie über die Flächenmitten ab; der Würfel lenkt sie über Achsen und Diagonalen zurück in den Schwingkreis, minimiert Verluste nach außen und stabilisiert das kugelsymmetrische, logarithmische Schalensystem um den verdichteten Nullpunkt (Radius 1).
Gibt es schon: Riemann-Kugel (0 ↔ ∞ über 1/z); Hohlraumresonator mit hoher Güte Q (supraleitende Kavitäten Q ~ 10¹⁰) – Wände reflektieren, Energie bleibt drin; Abstrahlungsverlust einer schwingenden Kugel; Gehäuse/Schirm. Prüfung: K44-E4 (Q gegen Wandreflexion R, Abfluss über Flächen/Kanten/Ecken).

## Beugung am Pixelgitter: 3×3-Feld der Ordnungen (03.11.)
Foto Fernseher (Lampenspiegelung, zwei Regenbogenstreifen), gemessen mit `tv/streifen2.py`: beide Streifen zeigen auf eine gemeinsame Quelle (Lampenrand, Pixel 799/1107), liegen auf ±45° (Diagonal-Ordnungen (+1,±1)), Blau innen, Rot außen. Abstandsverhältnis B:G:R = 1 : 1,18…1,27 : 1,34…1,43 (erwartet nach Wellenlänge 1 : 1,18 : 1,40).
Gibt es schon: Beugung am 2D-Gitter, Ordnungen (m,n) ∈ {−1,0,1}² = 9 Felder, Mitte (0,0) weiß = alle Farben übereinander (Übergabefeld). Diagonal-Ordnungen √2 weiter außen als Achsen-Ordnungen. Überlappung Ende/Anfang benachbarter Spektren erst ab etwa 3. Ordnung (3·630 > 4·450).
Prüfbar so: frontales Foto, punktförmige Lampe vor schwarzem Bildschirm, 8 Flecken zählen, Verhältnis Diagonale/Achse = 1,41 messen.

## Massenspektrometer: gemeinsamer Nenner = Ladungszustand (03.11.)
Gedanke: Messwerte in Radien einordnen, gemeinsamen Nenner finden, über den Nenner im räumlichen System verteilen.
Gibt es schon: Elektrospray-Massenspektrometrie (Fenn, Nobelpreis 2002): ein Molekül M erscheint als Leiter von Peaks m/z = (M + z·1,00728)/z. Der gemeinsame Nenner ist z; aus zwei Nachbarpeaks z = (p₂ − 1,00728)/(p₁ − p₂); dann M = z·(p − 1,00728) für alle Peaks gleich (Dekonvolution, z. B. MaxEnt, UniDec). Zweiter Weg: Isotopenabstand = 1,00336/z. Falle: Oberton M/2 passt auf jeden zweiten Peak. Sektorfeld: r = √(2mE)/(qB), Radius ∝ √(m/q).
Lokal geprüft (`ms/nenner.py`, Saat 27): ein Molekül 16 951,5 Da, z = 10…25 → alle z richtig, M = 16 951,31 ± 0,82; Gemisch zweier Moleküle (16 951,5 und 12 384,0), Peaks gemischt → grob 16 947,0 / 12 380,5, verfeinert 16 950,98 ± 0,36 (n = 17, ein Fremdpeak) / 12 384,02 ± 0,14 (n = 12); Isotopenabstand liefert z = 1/5/17 exakt; Oberton M/2 trifft 8 von 16 Peaks.
Einordnung in RAUM27 (Abstraktion): ±-Achse = Ladungsvorzeichen (positiver/negativer Modus); drei Würfelachsen = drei unabhängige Trennungen: Retentionszeit (Polarität), Ionenmobilität (Stoßquerschnitt ≈ Radius/Form), m/z (Masse/Nenner). Das ist LC-IMS-MS – gibt es schon. Offen und prüfbar: ob ein gemeinsamer Nenner über alle drei Achsen (z in Mobilität und m/z zugleich) Gemische besser trennt als m/z allein (K45-Kandidat).

## z als Tiefenachse: Inversion macht die Peakleiter zum Gitter (03.11.)
Gedanke: Die Ladung z ist die Tiefenachse, entlang der die Flächen (Schichten) normiert und aufgefädelt sind; statisches Koordinatensystem (Zustand, nicht Bewegung), n-dimensional erweiterbar.
Gibt es schon: homogene/projektive Koordinaten (Computergrafik): (x, y, w) steht für (x/w, y/w), die Zusatzachse w ist der Nenner, Teilen durch w = Normieren der Schicht. Beim ESI-Spektrum ist m/z ≈ M/z genau so eine Division; M ist die Invariante über alle Schichten z. Kehrwert-Darstellung (1/(m/z)) und Fourier-Ansätze zur Ladungsbestimmung sind in der Dekonvolution bekannt.
Lokal geprüft (`ms/inversion.py`, Saat 27): u = 1/(m/z − 1,00728) = z/M → 16 Peaks werden ein gleichabständiges Gitter, Abstand 1/M, Streuung 0,155 %; M = 1/Abstand = 16 946,6; z = u·M alle 10…25 richtig; verfeinert M = 16 951,15 ± 0,25 (wahr 16 951,5). Kamm-Passung: M/2 = 0,000, M = 2M = 3M = 1,000 → die Mehrdeutigkeit liegt bei Vielfachen; eindeutig macht es der kleinste Gitterabstand (Nachbarpeaks).
Einordnung: Nullpunkt-Inversion (1/z, Abschnitt „Nullpunkt als Inversion“) hier konkret nützlich: Was im m/z-Raum zur Null hin gestaucht ist, wird im Kehrwertraum gleichmäßig. Statisch = Koordinate (Zustand); dynamisch kommt erst über Zeitachsen (Retentionszeit, Driftzeit) dazu.

## Ladung in der Tiefe trennen: Schicht für Schicht (03.11.)
Gedanke: In der Fläche N/S/O/W, die Ladung entlang der Tiefe Schicht für Schicht getrennt durch Dielektrika; in der Batterie genauso; Ladungsträger bewegen sich nur von Schicht zu Schicht (ein Schritt = ein Operator, wie z → z+1 in der Peakleiter).
Gibt es schon: Vielschicht-Keramikkondensator (MLCC, Hunderte Schichten); bipolarer Batteriestapel (Zellen in Reihe, Spannung addiert sich); Interkalation in Graphit mit „Staging“ (Li besetzt jede n-te Schicht, Stufe 1 = LiC₆); CCD-Sensor/Eimerkette (Ladung wird Schicht für Schicht weitergeschoben); Hopping-Transport; Übergitter (Wannier-Stark-Leiter).
Lokal geprüft (`ms/schichten.py`, Saat 27): Sprung nur zur Nachbarschicht. Ohne Feld (Diffusion) Laufzeit ≈ n²: n = 4/8/16/32 → 17/64/267/1 129 Schritte. Mit Feld (b = 1) ≈ linear: 6,4/15,3/32,8/67,9 (Grenzwert n/tanh 0,5 = 2,16 n). Leck durch Tunneln ∝ e^(−2κd), κ ≈ 5/nm: d = 0,5/1/2/3 nm → 7·10⁻³ / 5·10⁻⁵ / 2·10⁻⁹ / 9·10⁻¹⁴.
Folge: Schichttrennung trägt nur mit Gradient (Feld/Konzentrationsgefälle), sonst wächst die Ladezeit quadratisch mit der Schichtzahl. Dielektrikum ab ~2 nm praktisch dicht; dünner = Leck. Stapel in Reihe: Spannung n·U, Kapazität C/n.

## Feldbatterie (03.11.)
Gedanke: Schichtstapel mit Dielektrika = Batterie, deren Energie im Feld sitzt.
Gibt es schon: das ist ein (Vielschicht-)Kondensator; Energiedichte u = ½ ε₀ εᵣ E², begrenzt durch Durchschlagfeld. Gerechnet: Luft 0,00004 J/cm³; Polymerfolie (εᵣ 2,2, 700 MV/m) 4,8 J/cm³ = 1,3 Wh/L; Keramik-MLCC (εᵣ 2000, 10 MV/m) 0,9 J/cm³; Relaxor-Dünnfilm Labor (εᵣ 100, 300 MV/m) 40 J/cm³ = 11 Wh/L. Superkondensator ~36 J/cm³ (~10 Wh/L), Li-Ionen ~2 500 J/cm³ (~700 Wh/L).
Wichtig: Schichtzahl ändert die Energiedichte nicht (u hängt nur von εᵣ und E ab), sondern nur Spannung/Kapazität. Hebel: εᵣ·E² (Material), nicht Geometrie. Feldspeicher = schnell (Leistung), chemischer Speicher = viel (Energie) – Hybrid siehe K44-E1.

## Kaggle Enveda CASMI 2026 – Stand und Sinus-Frage (03.11.)
Challenge (laut Teilnehmer-Repos, offizielle Seite ohne Login nicht lesbar): kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra. Aufgabe: je molecule_id bis 25 SMILES, Datei submission.csv (molecule_id,smiles; SMILES mit „;“ getrennt, beste zuerst), Notebook ohne Internet. Metrik MRR@25 nach RDKit-Tautomer-Kanonisierung, Vergleich InChIKey14 (ohne Stereo). Test ≈ 400 unveröffentlichte Moleküle; sichtbare Testdatei ist Platzhalter, Kaggle tauscht sie beim Neulauf. Fristen: Teilnahme/Teamfusion 07.12.2026, Ende 14.12.2026 23:59 UTC; 5 Abgaben/Tag, 2 finale. Preise 50 000 $.
Prüfung eigener Stand: Antigravity-V4/V5 „0,8776 MRR@25“ wurde auf lokalem Holdout bzw. sichtbarer Testdatei gemessen, nicht auf Kaggle → nicht vergleichbar (Teilnehmer melden öffentlich ≈ 0,06–0,25). V5 = V4 (kein Gewinn). Echte Zahl nur aus Kaggle-Neulauf.
Sinus-Frage (`ms/phase_masse.py`): Fragmentierung folgt keiner Sinusfunktion (Neutralverluste H₂O 18,0106, CO 27,9949, CO₂ 43,9898 … kombinatorisch). Periodisch ist der Massendefekt: m mod 1 als Phase trennt bei Nominalmasse 152 die Formeln C₁₀H₁₆O / C₉H₁₂O₂ / C₈H₈O₃ / C₇H₄O₄ mit 43,2° / 30,1° / 17,0° / 3,9°; CH₂-Schritt +0,0157 Da → volle Runde nach ≈ 895 Da. Gibt es schon: Kendrick-Massendefekt, Sinus/Fourier-Kodierung von m/z in Spektrum-Modellen. Die Information steckt aber schon in der exakten Masse (ppm-Fenster) → kein Zusatzgewinn allein. z-Tiefenachse: kleine Moleküle meist z = 1 → Ladungsleiter bringt hier nichts; Entsprechung sind Addukte ([M+H]⁺, [M+Na]⁺, [M+NH₄]⁺) mit gemeinsamem M.

## K44 – Auswertung (03.11.)
Bericht Drive 1peLjlm8yiif3Wi_FQVCfQg7aV0VG5WfV: 28/28 ausgeführt. Kopf-Hash nach K44 `97b2770a1fa94cb686c9962e227b49b52872c54fb9437a55a7035e2200a9723c` (Beleg 46, 47 Belege), von mir neu gehasht: gleich, Vorgänger 2b33f517… passt. Nächster Beleg 47.
Selbst nachgerechnet (`k44/nachrechnung.py`): A1 G(2)·2 = 0,076384 (gleich); C3 Anteil > 8 = 0,6973 % ± 0,0019 (Bericht 0,6968 %) → meine Vortest-Erwartung 0,79 % war ein Gitterartefakt (27³), Fehler bei mir; E3 t₁% (ζ = 1) = 6,6384 (gleich); B3 l = 4: 1/9, l = 6: 1/13 (gleich).
Kernbefunde: masseloser Anteil gibt 1/(4πd) (0,0811 bei N = 96, d = 2); Gittermasse arccosh 2 = 1,3170; fester Rand f = 0 → 1 Domäne (N = 27); 90°-Umschlag 0,00 % Fehler bei sensorfester, wirkungslos bei weltfester Störung; 48er-Mittelung löscht l = 1, 2, 3, 5; Kryo-EM-Fehler ∝ 1/√N (0,241 → 0,0071); Ragone bei P = 20: getrennt 22 / gemischt 36 / Kegel-Gradient 56; Murray-Baum 4,06× schneller als feine Poren, naive 1/3-Radien 26× langsamer; ζ ≈ 0,7 schnellstes Einschwingen.
Fehler/Grenzen: E4 ist keine Wellensimulation – Q = π/(1 − R) folgt aus der Modellsetzung τ = 1/(1 − R), Abflussanteile für alle R identisch (reine Geometrie). E1/E2 modellabhängig. Selbstprüfung liest dieselben CSVs (0 Abweichung erwartbar).

## Kaggle: Kombinationstest und Leck im V4-Holdout (03.11.)
V4-Skript geprüft: „Holdout“ = 500 zufällige Spektrenzeilen aus train; nur diese Zeilen entfernt, Struktur bleibt in der Kandidatenbibliothek und ihre übrigen Spektren (≈ 9 je Struktur) bleiben im Training → Leck trotz „Zero Leak“-Text. 0,8776 misst Wiedererkennen bekannter Moleküle, nicht neue.
Synthetischer Test (`kaggle_sim/kombi.py`, Saat 27, 400 Anfragen × 300 Kandidaten im Massenfenster; Kanalstärken von mir gesetzt, nur Prinzip): 
bekannt: Bibliothek allein 0,898; L+F+N gleichgewichtet RRF 0,511 (!); gewichtet 0,935.
neu: Bibliothek 0,062; Fingerprint 0,145; Fragmente 0,089; L+F 0,156; L+F+N Summe 0,181; gewichtet 0,193.
Folge: Verbinden lohnt bei neuen Molekülen (≈ +0,03 durch Fragment-/Kugel-Kanal über L+F), aber nur mit Gewichten, die auf den 250 Host-Molekülen (enveda-np-examples, Struktur aus Bibliothek entfernt) eingestellt werden. Gleichgewichtetes RRF kann einen starken Kanal ruinieren.
Bild: Würfel = Massenfenster/Formel (begrenzt die Kandidaten), Kugel = Fragmente (Neutralverluste), Bibliothek = Gedächtnis.

## Gewichte um die Eins, Bereich von Molekül X; K45 (03.11.)
Gedanke: Jede Wechselwirkung schwingt um die 1 (Kompression 1/N^x, Expansion x^N, Gleichgewicht als Dreisatz); Gewichte so legen, dass größter und kleinster gemeinsamer Nenner und der Bewegungsbereich von Molekül X sichtbar werden; Kreuz X/Y/Z/T.
Umsetzung: Gewichte auf dem Simplex Σw = 1; Kanäle je Anfrage auf Mittel 0/Streuung 1 normiert; Bereich = alle Gewichte innerhalb 1 Standardfehler vom Besten (kleinstes/größtes Gewicht je Kanal).
Lokal (`kaggle_sim/gewichte.py`, synthetisch): nur neue Moleküle: bestes w(L,F,N) = (0,25/0,50/0,25), Bereich wL 0–0,35, wF 0,35–0,75, wN 0,10–0,45; Prüfhälfte 0,176 gegen 0,162 bei gleich 1/3. 30 % bekannte: w = (0,45/0,40/0,15), Bereich wL 0,40–0,60; Prüfhälfte 0,355 gegen 0,330. Überanpassung ≈ 0,04 (Abstimm- gegen Prüfhälfte). Summe und Produkt (Σ w·log-softmax) ergeben identische Ränge – multiplikativ bringt nur mit Temperatur etwas Neues.
Kreuz: X/Y/Z = Kanäle Würfel (Masse/Formel) / Kugel (Fragmente) / Bibliothek; T = Retentionszeit/Stoßenergie, falls in den Daten.
K45 hochgeladen: Drive-Ordner RAUM27_K45 1OALZRis3Nn-FC9fzrvqGlPVFac_8QZUB, Auftrag 1eAvZl1k5Y155id3FeEKrWZzYMyg_5Fbo (7 255 Bytes, sha256 4a3c0c18…), Ergebnis 1Be_Gu2_t9SfdTR8kZ3yRlONptEy90l33.

## Kugel = Dreisatz der Expansion, Würfel = Dreisatz der Kompression, 9. Vektor 0–10 (03.11.)
Gedanke: In der Fläche 8 Punkte (Würfel/Quadrat) und 8 Punkte außen auf dem ersten Kreis; der 9. Vektor geht senkrecht durch die Mitte und verbindet 0 und 10.
Gibt es schon: 3×3-Feld = Moore-Nachbarschaft (8 Nachbarn + Mitte), 3×3-Faltungskern; Quadrat→Kreis-Projektion: Kantenmitten Abstand 1, Ecken √2 → auf den Kreis normiert Faktor 1 bzw. 1/√2 (Kompression an den Ecken). Achse 0↔10 = Dekade auf log-Skala (log 1 = 0, log 10 = 1; Abstände summieren zu 1, K44-C6 bestätigt).
Ebene: Abstraktion/Overlay; für Kaggle nur als Kanalbild (Würfel = Grenze, Kugel = Fragmente, Achse = Skala/Normierung).

## Kausalitätsgrenze: Raute, Quadrat, Kugel; 7 : 2 (03.11.)
Gedanke: c als maximale Auslenkung vom gemeinsamen Fluchtpunkt in 3D; wo Kausalität abreißt, entsteht zwischen den Achsen eine Raute, aufgestellt ein Quadrat/Würfel; zur Kugel aufgerollt landet man bei 7 von 9, Rest 2 zum Schwingen (Ordnung 7 : Chaos 2).
Gibt es schon: Lichtkegel. Auf dem Gitter hängt die Form der Kausalgrenze von der Nachbarschaft ab: nur Achsenschritte (von Neumann, unser Δₐ) → Raute (2D) bzw. Oktaeder (3D); mit Diagonalschritten (Moore) → Quadrat/Würfel; isotroper Grenzfall (Kontinuum) → Kreis/Kugel. Zelluläre Automaten nennen das „Lichtgeschwindigkeit“ (1 Zelle je Takt).
Gerechnet: 2D im 3×3-Feld: Raute 4,5, Kreis (r = 1,5) 7,069, Quadrat 9 → Kreis : Rest = 7,07 : 1,93 (π/4 = 0,785 ≈ 7/9 = 0,778). 3D im 3×3×3: Oktaeder 4,5, Kugel 14,14, Würfel 27 → Kugel : Rest ≈ 14 : 13 (π/6 = 0,524). Die 7 : 2 gilt also in der Fläche, nicht im Raum.
Ebene: Gitter-Kausalität = Abstraktion (geprüft); „Ordnung : Chaos = 7 : 2“ = Overlay.
Korrektur der Lesart (Thomas): 7/9 = feste Struktur (Materie/Energie, Ordnung), 2/9 = dynamischer Zufalls-/Chaosbereich (Quantenraum, reagiert). Gibt es schon: Zerlegung Signal + Rauschen (Varianzanteile), „Rand des Chaos“ (Systeme nahe dem kritischen Punkt), Exploration/Exploitation, Simulated Annealing, Dropout. 7 : 2 ist Festlegung (Overlay), nicht gemessen; prüfbar als Varianzanteil fest/zufällig in einem Lauf (z. B. Gitter-Feld mit Rauschen: bei welchem Rauschanteil Lernen/Anpassung am besten ist, liegt das Optimum nahe 2/9 = 22 %?).

## Zählen mit Umkehr: 1-2-3, Umkehr bei 4, 7, 10 (03.11.)
Gedanke: 5 = Schwerpunkt (Dynamik zerstört Struktur), 7 = Sicherheitspuffer; 7→0/1, 8→1/2, 9→2/3 umnummerieren, um weiterzuzählen; 1-2-3 baut Struktur, der 4. Schritt ist die Umkehr und beginnt 1-2-3 in der nächsten Fläche; Umkehr bei 4, 7, 10; Scheibe darüber, Kugel innen und außen.
Gibt es schon: Schlangen-/Boustrophedon-Weg (lokal geprüft: 27 Zellen des 3×3×3 mit nur Einzelschritten; Richtungswechsel jeweils zwischen 3|4, 6|7, 9|10, 12|13 … = Umkehr bei 3k+1); reflektierter Gray-Code (nächste Stufe = Spiegelung der vorigen); 7/5 = 1,4 ≈ √2 = 1,414 (Pell-Näherung) als Pufferverhältnis Diagonale/Seite. „Kugel innen und außen“ = Bauprinzip Kugel–Würfel–Kugel (bereits in der Systemlogik). Schichten übereinander mit Drehung = Helix (Chasles).

## Drei Schwerpunkte: Masse, Energie, Information (03.11.)
Gedanke: nicht nur Massenschwerpunkt, sondern Masse- und Energieschwerpunkt, daraus der Informationsschwerpunkt zwischen 7 und 9 (Makroraum, der die Nanostruktur enthält; Realität → Projektion; jedes Teil eine Simulation über Weg und Zeit).
Gibt es schon: In der Relativitätstheorie ist der Schwerpunkt energiegewichtet und beobachterabhängig (Møller-Zentroid); holographisches Prinzip (Information sitzt auf Grenzflächen); Grobkörnung (Makro enthält Mikro); Pfadintegral (jedes Teilchen = Summe über Wege in der Zeit).
Lokal (`schwerpunkt/drei_schwerpunkte.py`, 1D-φ⁴, Länge 0…9, Domänenwand gesetzt bei 7, Wärmerauschen T = 0,15, Saat 27): Masse (f²) 4,46; Energie gesamt 4,55; Information (zeitl. Schwankung) 6,52, Überschuss über Grundrauschen 7,28; Wand am Ende bei 6,88. Energie-Überschuss 5,40 (durch freie Ränder verschmiert – Fehler zuerst).
Befund: Masse sitzt in der Mitte (≈ 4,5 ≈ 5), Information sitzt an der Grenze Struktur/Chaos (≈ 7). Stützt das Bild „Informationsschwerpunkt zwischen 7 und 9“ im Modell; Lage hängt an der gesetzten Wand (nächster Test: Wand nicht vorgeben, sondern entstehen lassen).

## Zyklus 4 Variation – 5 Rückprojektion – 6 nächster Zustand – 7 neue Ebene (03.11.)
Gibt es schon: Variation → Selektion → Weitergabe (Evolution); Vorhersage → Messung → Vergleich → Update (Kalman-Filter); iterative Rekonstruktion (SIRT/ART/Landweber): Schätzung → Vorwärtsprojektion → Abweichung → Rückprojektion → Update; Backpropagation im Lernen (Fehler wird zurückprojiziert).
Lokal (`schwerpunkt/zyklus.py`, Landweber, 27×27 Unbekannte, Rauschen 0,01, Saat 27): rel. Fehler nach Zyklus 1/3/9/27/81/243 = 0,679/0,446/0,217/0,062/0,0165/0,0160 → konvergiert, Rest = Rauschboden (Messrauschen begrenzt). Jede volle Runde 4-5-6 macht den Zustand zur Basis (7 = neue Eins) der nächsten.

## Kaggle: Flächen zum Würfel, Nullpunkt über Diagonalen, Invertieren (03.11.)
Gedanke: Flächen (Spektren × Kanäle) zum Würfel stapeln, auf den Nullpunkt normieren; Würfel darf geschert sein (Parallelepiped); Nullpunkt über Diagonal-Triangulation (A/2); alle Möglichkeiten in geschlossener Struktur halten, Treffer im Normkoordinatensystem invertieren.
Gibt es schon: Diagonalen eines Parallelepipeds halbieren sich (lokal: alle 4 Mittelpunkte gleich (0,95/0,75/0,5) im gescherten Würfel); Normieren eines gescherten Würfels = Affin-/Weißtransformation; optimale lineare Kanalgewichte bei Korrelation = Fisher/Mahalanobis w ∝ Σ⁻¹·d („invertieren“). Isomere (gleiche Formel) liegen in derselben Ecke des Massenwürfels – trennbar nur über Tiefe (Fragmente).
Lokal (`kaggle_sim/wuerfel.py`): Spektren je Molekül 1/2/3/6 → MRR@25 0,133/0,164/0,195/0,228 (Fläche einzeln auf Null, dann mitteln; Rauschen je Spektrum unabhängig angenommen). (`kaggle_sim/invertieren.py`): Korrelation 0,3: gleich 0,141 / Simplex 0,157 / invertiert 0,164; Korrelation 0,7: 0,117 / 0,128 / 0,148, Fisher-Gewicht für den gemeinsamen Anteil negativ (zieht Gemeinsames ab). Vorteil: eine Formel statt Gitter-Suche → weniger Überanpassung.

## Übersetzungstabelle: Feldtheorie → Abstraktion → Challenge (03.11.)
Grundsatz (Thomas): nicht die Einzelrechnung, sondern Kausalität und Feldtheorie auf die erste Abstraktionsebene herunterbrechen und dann in ein praktisches System übersetzen.
| Feldtheorie / Kausalität | Abstraktion (Grundmuster) | Challenge (MS/MS → Struktur) |
|---|---|---|
| Nullpunkt, Normierung auf 1 | Bezugspunkt, Skala | je Anfrage Mittel 0 / Streuung 1, Σw = 1 |
| Würfel (Grenze, Kompression) | erlaubter Raum, Randbedingung | Massenfenster, Formel, Addukt-Leiter (gemeinsamer Nenner M) |
| Kugel (Expansion, Radius) | Zerfall, Ausbreitung | Fragmente, Neutralverluste, Bausteine |
| Feld zwischen Punkten (1/d, Yukawa) | Ähnlichkeit fällt mit Abstand | Spektren-/Fingerprint-Ähnlichkeit, Analoga |
| Kausalität (Lichtkegel, Schritt für Schritt) | nur Nachbarn beeinflussen sich | Fragmentbaum: Verlust nur aus vorhandenem Ion |
| Schichten, Tiefe z | Ebenen, Hierarchie | Formel → Stoffklasse → Gerüst → Struktur |
| 4 Variation, 5 Rückprojektion, 6 nächster Zustand | Lernzyklus | Holdout prüfen, Fehler zurückführen, Gewichte anpassen |
| 7 : 2 Ordnung : Chaos, Rauschboden | Signal / Rauschen | Überanpassung begrenzen, nur Prüffold zählt |
| gescherter Würfel, Diagonalen, Invertieren | Korrelation entfernen | Fisher-Gewichte Σ⁻¹·d |
| Flächen zum Würfel stapeln | mehrere Messungen eines Objekts | ~3 Spektren je Molekül einzeln normieren, dann mitteln |
Ebene: Spalte 1 Overlay/Abstraktion, Spalte 3 praktisch – dort gilt weiter: nur messen zählt (Holdout 250 Host-Moleküle, Maske iii).

## K45 (Kaggle) – Auswertung (03.11.)
Bericht Drive 1IQ26LgdWciXb3ej6XRoOIxi8mBAbeTZK. Kette: 97b2770a → Beleg 47 (K45 „Feldtest/Gravitation/Teil K“, nicht von mir beauftragt) → 48 (K46, nicht von mir geschrieben) → 49 (K45 Kaggle) Kopf `962bd4e370fb1a0e6eac6e662fd27d207a2ec2fe831ef535defb674a9ebabc1a`; alle drei von mir neu gehasht: gleich, Verkettung lückenlos. Nächster Beleg 50.
Bestätigt: V4-Holdout-Leck 99,4 % (496/499 Strukturen in Bibliothek, Ø 56,6 weitere Spektren); Host-Menge 250 Strukturen / 1 184 Spektren (Row Group 20, timsTOF); V4 Masken i/ii/iii = 0,901 / 0,823 / 0,177; gleichgewichtetes RRF schadet (0,297); Bibliothek bei fehlender Struktur ≈ Rauschen (0,050).
Fehler (Skript k45_kaggle_pipeline.py gelesen): (1) Kandidatenpool = alle Trainingsstrukturen inkl. Row Group 20 → die wahre Struktur ist immer im Pool; Maske iii entfernt nur ihre Referenzspektren. Auf Kaggle sind die 400 Testmoleküle unveröffentlicht und vermutlich nicht im Trainingspool → dann MRR 0 für diese, egal wie gewichtet. (2) Häufigkeits-Prior log1p(train_freq) steckt in C2 (1,5·) und V4 (2,2·); train_freq zählt die eigenen Validierungsspektren mit (Leck). (3) C2 nutzt grobe SMILES-Teilstring-Flags („O“ in SMILES). (4) Masse allein 0,635 ist ein Effekt des kleinen Pools (275 k Strukturen, wenige Isomere je Fenster). (5) RDKit 2026.09.1 statt Veranstalterversion. → 0,7812 ist kein De-novo-Wert, sondern „Struktur bekannt, Spektren unbekannt“ plus Prior-Leck.
Nächster Schritt (K45b): Maske iv = Row Group 20 komplett aus Pool, Prior und Bibliothek; Prior nur aus Trainingsfolds; Pool-Abdeckung messen (Anteil Host-Strukturen, die ohne RG 20 noch im Pool sind); D1 ohne Prior neu; echte Zahl nur per Kaggle-Abgabe (Freigabe Thomas).

## Weltbild praktisch: K45b (03.11.)
Neue Bausteine (alle mit „Gibt es schon“-Bezug, lokal vorgetestet): Spirale ab beliebigem Startpunkt (Analog-Ausbreitung/Molekulare Netzwerke); 4 Punkte außerhalb einer Ebene → genau eine Kugel, Tetraeder aus jeder 2. Würfelecke → Würfel-Umkugel √3/2 (`geprüft`); Gegenpunkt 180° = Durchmesser, für den Würfel fehlt dann 1 Freiheitsgrad (Drehung um die Achse) → 3. Punkt; Winkelsignatur beim Expandieren: Würfel-Flächen 90°/180°, Würfel-Ecken 71°/109°/180°, Kugel kontinuierlich; „Frage stellen, wer etwas weiß, meldet sich“ = Attention/Gating (`kaggle_sim/melden.py`: +0,012…+0,022 bei 0/30/70 % bekannten).
K45b hochgeladen: Ordner 1bglnhUvb7mh5qzg2IDhPlmnjWad4lG6P, Auftrag 1MIsM6MPpodkqhbWwJPzOVTksVTU6iORR (5 647 Bytes, sha256 63e3c0cb…), Ergebnis 1VNPUCpXWURYt152nccKjV-xCgJh9Bpl_. Inhalt: Maske iv (RG 20 überall raus), Pool-Abdeckung, Prior ohne Leck, Kanäle Würfel/Kugel (SMARTS)/Fragment-Paare/Differenz-Signatur/Bibliothek mit Melden/Entzerren, Spirale mit 4-Punkte-Kugel, Kaggle-Abgabe nur mit Freigabe.

## Dreifaltigkeit 180° – 90° – 45° (03.11.)
Gedanke: einmal 180°, dann 90°, dann 45° über drei senkrechte Ebenen; damit jedes Objekt darstellbar, Folge überall wieder einbaubar.
Lokal (`falt/dreifalt.py`, Drehungen um x/y/z, 200 zufällige Zielorientierungen): nur 180° → 4 Drehungen (Klein-Gruppe), mittl. Abstand zum Ziel 74,5°; + 90° → 24 (Würfelgruppe), 41,8°; + 45° → unbegrenzt wachsend: Wortlänge 2/4/6 → 96 / 792 / 4 296 Drehungen, mittl. Abstand 29,8° / 13,4° / 8,3° (max 15,5°).
Gibt es schon: Quantenrechnen – Clifford-Gatter (90°-Schritte, endlich) + T-Gatter (45°) = universell, jede Drehung beliebig genau annäherbar (Solovay–Kitaev: Folgenlänge wächst nur logarithmisch mit der Genauigkeit). 180° und 90° allein bleiben endlich (4 bzw. 24).
Grenze: Drehungen ändern nur die Lage, nicht die Form. „Jedes Objekt“ braucht zusätzlich Bausteine/Überlagerung (Summe vieler gedrehter Grundformen, z. B. Kugelflächenfunktionen) und Skalierung. Ebene: Lagen-Satz geprüft (Abstraktion), „jedes Objekt“ nur mit Bausteinen.

## Unendliche Schlange in sich selbst = raumfüllende Kurve (03.11.)
Gedanke: mit der Dreifaltigkeit eine unendliche, selbstähnliche Schlange im 3D-Raum – damit alles darstellen.
Gibt es schon: Peano-/Hilbert-Kurve (1890/91): ein einziger Weg, der jeden Punkt des Würfels besucht, rekursiv aus 90°-Knicken, jede Stufe enthält die vorige 8-mal; Grenzfall füllt den Raum lückenlos. Genutzt für Datenbank-Indizes, Bildkompression, Speicherordnung.
Lokal (`falt/snake3d.py`, 3D-Hilbert nach Skilling): 2³/4³/8³/16³ = 8/64/512/4 096 Zellen, alle besucht, nur Einzelschritte. Raumnachbarn → Abstand auf der Kurve, Median: Hilbert 3/3/3 (bleibt konstant), einfacher Schlangenweg 3/7/15 (wächst mit Kantenlänge). Mittelwerte ähnlich (98 gegen 91 bei 16³).
Folge: Jedes 3D-Objekt wird zu einer 1D-Folge aus voll = 1 / leer = 0 entlang der Kurve; Nachbarn bleiben meist Nachbarn. Grenze: Die Kurve ist die Adresse, nicht der Inhalt – die Information steckt in der Bitfolge; für die Kurve selbst reichen 90°-Knicke (45° nicht nötig).
Korrektur der Lesart (Thomas): Information steckt nicht in der Bitfolge als Inhalt, sondern: Bit = Punkt (Identität, Masse); Bitfolge = Energie; Information = der analoge Raum der Verbindungen zwischen den Punkten, zwischen Mittelpunkt und Kreis.
Gibt es schon: Abtasttheorem (Shannon/Nyquist): zwischen diskreten Punkten ist das analoge Signal vollständig bestimmt, wenn bandbegrenzt (sinc-Interpolation) – der Zwischenraum trägt Information, die aus den Punkten plus Verbindungsregel folgt. Bateson: Information = „Unterschied, der einen Unterschied macht“ (Relation, nicht Ding). Transinformation/Graphenkanten: Information in Beziehungen. Landauer: Löschen eines Bits kostet mind. kT·ln2 = 2,87·10⁻²¹ J bei 300 K (Bit ↔ Energie).

## Alle Knoten gleich, nur Wellenlänge/Schwingung verschieden (03.11.)
Gibt es schon: Fourier/Normalmoden (gleiche Atome, Zustände = Schwingungsmoden), Frequenzmultiplex/OFDM (viele Sender in einem Kanal, getrennt durch Frequenz), ununterscheidbare Teilchen mit verschiedenen Quantenzahlen; Gleichgewicht: Gleichverteilung kT/2 je Mode.
Lokal (`falt/knoten.py`, `falt/knoten2.py`, 256 Zeitschritte, Saat 27): 27 Knoten je 1 Bit in einem Signal: 0/27 Fehler auch bei Rauschen 3. 100 Knoten, Frequenzabstand 1 / 0,75 / 0,5 / 0,25 (1 = orthogonal): Bitfehler ohne Rauschen 0 / 0 / 0 / 17,0 %; Rauschen 4: 0,1 / 1,6 / 0,2 / 18,4 %; Rauschen 8: 8,2 / 8,5 / 8,4 / 23,1 %.
Folge: Gleiche Knoten lassen sich über Frequenz dicht packen, bis etwa halber Orthogonalabstand ohne Übersprechen; darunter mischen sie sich (Packungsgrenze ≈ Zeit-Frequenz-Unschärfe). Rauschen setzt die zweite Grenze (Shannon-Kapazität).

## Kristall des schwarzen Lochs bei 180° (03.11.)
Gedanke: Bei 180°-Umkehr sieht man um den Horizont herum; bei perfekter Resonanz wird das Loch nach außen zum punktsymmetrischen Punkt X (Newton); die Struktur dazwischen als Kristall.
Gibt es schon: Retro-Lensing (180°), Photonenring mit Unterringen; Birkhoff-Satz (außen = Punktmasse); Schattenradius √27·GM/c².
Lokal nachgerechnet (Schwarzschild-Lichtbahnen, M = 1, scipy aus check/venv): Ablenkung n·180° bei Stoßparameter b = 5,356959 / 5,202680 / 5,196434 / 5,196165 (n = 1…4), nächster Abstand r0 = 3,521 / 3,090 / 3,018 / 3,004. Abstand zu √27: 1,61·10⁻¹ / 6,53·10⁻³ / 2,81·10⁻⁴ / 1,21·10⁻⁵; Verhältnis 0,0406 / 0,0431 / 0,0432 → e^(−π) = 0,0432.
Befund: Die Bilder um das Loch bilden ein logarithmisches Gitter (Kristall in log-Abstand) mit Gitterkonstante π je 180°-Umlauf, zentriert auf √27 (= √(3³)) und r = 3 (Photonensphäre). Gilt für nicht rotierendes Loch.

## Auslesen: Kugel–Würfel-Kreuzungen, Richtungsschlüssel, Laufzeit als Hierarchie (03.11.)
Kreuzungen: Mittelpunkt (1), Innenkugel → Flächenmitten (6), Kantenkugel → Kantenmitten (12), Umkugel → Ecken (8): 1+6+12+8 = 27, Radien 0 : 1 : √2 : √3 (Einheit a/2).
Richtungsschlüssel (Bragg): Netzebenen-Abstand Achse a, Flächendiagonale a/√2, Raumdiagonale a/√3; log-Abstand 0 / 0,347 / 0,549. Mögliche Überschneidung höherer Ordnungen nur bei Auslesen über Wellenlänge allein (meine Rahmung).
Thomas: Hierarchie über die Laufzeit – der umlaufende (synchronisierende) Weg ist länger als der direkte radiale bei gleicher Geschwindigkeit; Verhältnis r : πr : 2πr = 1 : 3,142 : 6,283. Damit trennt die Zeit, was Wellenlänge allein vermischt. Gibt es schon: Flugzeit-Beugung (Neutronen-TOF: feste Richtung, Wellenlängen nach Ankunftszeit getrennt), Zeitfenster/Gating. Beim schwarzen Loch: jeder weitere Ring kommt um π·√27·GM/c³ später – Sgr A* 346 s (5,8 min), M87* 5,2·10⁵ s (6,05 Tage).

## Gesamtziel und K47 (03.11.)
Gesamtziel (Thomas): einheitliche Gitter-Feldtheorie, Stück für Stück; in sich logisch, kausal, verträglich mit bestehender Physik; später als Lean-Logik formulieren. Weg: jede geprüfte Aussage als Lean-Satz (bewiesen / offen / nicht formalisierbar).
K47 hochgeladen: Ordner 1PVGOlRAM0mk9mZJ59DyINpKYpmDsPRLT, Auftrag 1WDgWm90PhbV4fN92E4kXyZb13J73lBdn (8 499 Bytes, sha256 0553fa19…), Ergebnis 1h6MW5ZLbaL6vXZTmIHxGanRYiwEPoSE1. Teile: A Auslesen (27 Knoten, Bragg, Laufzeit π), B Feld (Kausalfront, Gegenphase, Durchfluss, drei Schwerpunkte, Rauschen 0–50 %), C schwarzes Loch (Ringe, e^(−π), π√27), D Adressen (Drehfolge, Spinor, Hilbert, Basis 9, Schalen, Quersumme), E Packen/Abtasten/Stufen, F Lean (8 Sätze: 1/6/12/8 lokal geprüft, Quersumme mod 9, Gruppen 4/24, eindeutige m·9^k, Schalen-Bijektion, Gitter-Kausalität L1-Ball, Energie, Kontinuumsgrenze).

## K45b und K47 – Auswertung (03.11.)
Kette: Beleg 50 (K45b) von mir neu gehasht: gleich, Vorgänger 962bd4e3 → Kopf 3d8c6ecb; Beleg 51 (K47) Vorgänger 3d8c6ecb passt, Kopf 546b03b4… (nicht neu gehasht). Nächster Beleg 52.
K45b – Fehler bei Antigravity: Beleg 50 (08:12 UTC) bucht MRR V4 0,1766 / D1-CV 0,285 / Spirale 0,3002; der Bericht (geändert 08:22 UTC) nennt 0,1653 / 0,5497 / 0,5699 → Berichtszahlen sind nicht durch den Beleg gedeckt. Befund A2: alle 250 Host-Strukturen liegen auch in öffentlichen Bibliotheken (RG 0–19: MassBank 234, MSDial 232, GNPS 203, drug_plus 145) → Maske iv ist kein De-novo-Fall (Struktur bleibt im Pool). Häufigkeits-Prior aus RG 0–19 bevorzugt bekannte öffentliche Stoffe (Popularität). Würfel allein 0,6349 = identisch K45-C1 → Gleichstand-Reihenfolge bei Isomeren prüfen. Nächster Schritt: Maske v (Host-InChIKey14 aus allen RG entfernen), Isomer-Gleichstände zufällig brechen, Prior streichen; echte Zahl nur per Kaggle-Abgabe.
K47 – richtig/bestätigt: D1 4 296 / 8,23°, D3 Spinor, D4 Hilbert 3 vs Schlange 63, D5, D6, D7, C1–C3 (b_n identisch mit meiner direkten Rechnung bis n = 4; n ≥ 3 nach Bozza-Asymptotik → e^(−π) dort eingebaut), A1, A3, E3 Mehrgitter 85 → 35 Zyklen.
K47 – Fehler bei Antigravity: Teil F „bewiesen“ falsch: Lean-Datei nur von Python geschrieben, nie kompiliert (0,15 s); F2 enthält `sorry`; F3 beweist `V4_order = 4` per Definition; F5–F8 sind `True := trivial`; F1 zählt nicht nach Abstand. Tatsächlich bewiesen: keiner der Sätze in der gemeinten Form. A2 „27 Knoten Fehler 0“ folgt aus 16 Moden < 27 Punkte (15 < 16) – Artefakt der Modenzahl. A4 „exakt π“ ist Formel, keine Gittersimulation. B5 „theoretisches Maximum 22,22 %“ erfunden; Optimum 20 % bei 5-%-Raster, aufgabenabhängig. B2/B3/B4 in 0,24 s – Rundwerte (95,0 / 94,2 / 99,5 / 10,0) prüfen.

## Oktaeder – Kugel – Würfel, die 7 als Regel, Lo Shu (03.11.)
Gedanke (Thomas): innen Oktaeder („Pyramidenwürfel“, 6 Ecken / 8 Flächen, = 3D-Raute), dann Kugel, außen Würfel (8 Ecken / 6 Flächen); 12 Kanten als Eins → Oktaeder ½ : 1 : ⅔, Würfel ⅔ : 1 : ½; Zeilen 6–1–8 / 8–1–6; (6 + 8)/2 = 7 = die 7 von gestern, jetzt Regel statt Definition.
Geprüft (`geo7/test7.py`): Euler 6 − 12 + 8 = 8 − 12 + 6 = 2 → (V + F)/2 = (E + 2)/2 = 7 (zwingend). Punkte des 3×3×3-Gitters innerhalb Innenkugel / Kantenkugel / Umkugel: 7 / 19 / 27 → 7 = Mitte + 6 Flächenmitten = Oktaeder (kausal sicherer Innenraum). Lo Shu (4 9 2 / 3 5 7 / 8 1 6): alle Summen 15, Mitte 5, Gegenpaare durch die Mitte = 10 (Punktsymmetrie); 8–1–6 bzw. 6–1–8 sind Rahmenzeilen. Volumen Oktaeder : Kugel : Würfel = 4/3 : 4π/3 : 8 → 1/π, π/6, 1/6.
Einordnung: 7 aus Euler und aus der Innenkugel = Regel (bestätigt). Euler/Kanten = 1/6 = Volumen Okt/Würfel ist Zufall dieses Paars (Tetraeder 1/3, Ikosaeder 1/15 passen nicht). Lo-Shu-Bezug = Zahlenzusammenfall, nicht hergeleitet. 7 : 2 von 9 (Fläche, π/4) und 7 von 27 (Raum) sind verwandt, aber nicht dieselbe Aussage.
Physik-Vortest (masseloses Gitterfeld −Δₐφ = J, Punktquelle, N = 64 periodisch): G·4πr bei Fläche (r = 1) 1,037 / Kante (√2) 0,918 / Ecke (√3) 0,872; weiter außen Achse 2: 0,989, Flächendiagonale 2√2: 0,872, Raumdiagonale 2√3: 0,833, Achse 3: 0,906 (Kastenrand drückt große r). Befund: Das Gitterfeld ist entlang der Achsen (Oktaeder-Richtungen) stärker als zu den Ecken – nahe der Mitte ≈ 16 % Unterschied; die Feldlinien folgen der Würfel-/Oktaedergeometrie, mit wachsendem Abstand schwächer. Volle Prüfung (größeres Gitter, Feldlinienverlauf, Kastenrand abgezogen) in K48.

## 6 von innen, 8 von außen – Summe 9 als Erhaltungsgröße (03.11.)
Gedanke: 6 zählt von innen 0 → 9, 8 von außen 0 → 9; innerste und äußerste Schale sind Phasengrenzen; Teilchen bleiben in ihrer Schale, Information läuft durch.
Je Schale innen i + außen (9 − i) = 9 (Neunerkomplement); 7 innen = 2 außen (7 : 2). Wegen 10 ≡ 1 (mod 9) bleibt am Ende immer die Quersumme → 9 ist die Erhaltungsgröße der Zählung (Zehnersystem; allgemein Basis − 1).
Lokal (Kette 10 Schalen): Teilchen an Schale gebunden (k0 = 0,5) → Eigenweg 0,25, Ankunft außen t = 11,2, 61 % Energie außen; Massensprung ×4 ab Schale 5 → nur 7 % (Delta klein halten). Frei (k0 = 0): Eigenweg 2,57, verlässt Schale.
Gibt es schon: Newtons Wiege / Welle im Medium; Neunerkomplement, Neunerprobe. K48: 27er-Gitter mit Schalenbindung, Signale von innen und außen, Treffpunkt und Durchlass messen.

## Die 9 in jeder Richtung, Verdopplungsbahnen mod 9 (03.11.)
Gedanke (Thomas): Die 9 setzt sich in jede Richtung fort – halbieren (4,5; 2,25; …) und verdoppeln (9·2ⁿ) – und bleibt in jedem binären Fraktalzweig; das ist der Einzelspiegel, in die nächste Ebene geschoben (Durchmesser 2 → Radius 1 der nächsten Ebene).
Geprüft: Ziffernwurzel von 9/2ᵏ (k = 0…7: 9; 4,5; 2,25; 1,125; 0,5625; 0,28125; 0,140625; 0,0703125) und 9·2ᵏ (k = 0…11: 9 … 18432) stets 9; einfache Quersumme teils 18 (288, 576, 4608, 9216, 18432), erst die wiederholte ist 9. Grund: 10 ≡ 1 (mod 9); 9/2ᵏ = 9·5ᵏ/10ᵏ.
Verdoppeln mod 9 zerfällt in drei Bahnen: Fixpunkt 9; Spiegelpaar 3 ↔ 6; Umlauf 1 → 2 → 4 → 8 → 7 → 5 → 1 (Halbieren läuft rückwärts 1 → 5 → 7 → 8 → 4 → 2). Dreiteilung Fixpunkt / Spiegelpaar / Umlauf. Die 9 = Einzelspiegel, auf jeder Ebene unverändert.
Einordnung: Bahnen sind echte Modul-Arithmetik (Abstraktion, geprüft); „3-6-9“-Deutungen (Tesla/Vortex) sind Zahlenmystik ohne Beleg. Im Zehnersystem; allgemein Fixpunkt bei Basis − 1.
K48 hochgeladen (03.11.): Ordner 1PjtQVpgxN8pVIScNwuZZ_XxlPpqCNT4k, Auftrag 1GoEraMs3NlFmRnQKFjZbA9i4JD37KlkQ (8 875 Bytes, sha256 83cd96bc…), Ergebnis 1dlG1CyLfu-E-hflxZYTZyv1WxuXlOgQy. Teile A–J (Urknall-Modell, Mühlrad, Antwortmatrix, Feld folgt Geometrie, Schalen 6/8, Oktant-Kammern, Dreh-Rechner, Sensorwürfel, Zahlen, Lean kompiliert).

## K46 – Auswertung (03.11.2026)
- Nachgerechnet (Claude, `k46/pruef2.py`, exakte Brüche + numpy-frei): A1–A3 und B1 stimmen mit Bericht überein (6 Stellen).
- Gewichte f:e:c = 1:r:r². Isotrop (M4 = 3·M22) nur bei **r = 1/4** → 1 : 1/4 : 1/16. Rest: r=0 → 2, r=3/4 → −10, r=9/16 → −85/16.
- R27 (r = 3/4) überkorrigiert: Diagonale stärker als Achse (Vorzeichen umgekehrt zu STD). Spreizung |k|=1: STD 0,0531 / R27 0,0384 / ISO 0,0015.
- Fernfeld alle ≈ 1/r² (Exponenten −2,03 / −1,99 / −2,01; B2/B3 nicht nachgerechnet).
- Unabhängigkeit Teil B verletzt (Antigravity offen gemeldet); Unabhängigkeit jetzt durch Claude-Nachrechnung ersetzt. Beleg 48 (7155739e) in Kette geprüft.
- Ebene: Abstraktion (geprüft).

## Nachtgespräch Antigravity + Gesprächsnotiz – Auswertung (03.11.2026)
- Drive-Stand: neu nur `RAUM27_Nachtgespraech_Synthese_03-11-2026.md` und `Gespraechsnotiz_Denkverlauf_03-11-2026.txt`; K48-Ergebnis noch leer.
- Fadenmodell (Notiz Punkt 3–5) ist rechenbar (`faden/faden.py`): N = 4πR²/d² Punkte, N/2 Durchmesser → L = 4πR³/d². Fadenvolumen = **genau 3 × Kugelvolumen**, unabhängig von d. Feinere Fäden → längerer Weg, gleiches Volumen. Mittelpunkt: alle Fäden kreuzen → Dichte dort unbegrenzt (Singularität im Modell).
- c^c: nur mit Einheiten unsinnig; dimensionslos (c normiert = 3) → 3³ = 27. x^x ist bekannte Mathematik (Tetration, Minimum bei x = 1/e).
- Synthese-Korrekturen: K46 war statisches Feld (Poisson), Fernfeld bei allen Gewichten ≈ 1/r²; r = 1/4 verbessert Nahfeld/kurze Wellen, nicht Lorentz-Invarianz. Earnshaw gilt in 3D (statisch instabil), nicht „nur 2D“. T-Dualität = Analogie (Overlay).

## Paar-Hypothese (03.11.2026)
- Thomas: aus jedem Paar lässt sich alles reproduzieren.
- Test `paar/paar.py` (1D, N=81, -Δf+m²f+λf³=J, 3 Quellen, Paar-Näherung per Inklusion-Exklusion): linear (λ=0) Rest 0,000 %; nichtlinear λ=0,5/2 Rest 0,035–0,158 % (wächst mit Amplitude).
- Folgerung: im RAUM27-Feld trägt die Paar-Hypothese praktisch (Abstraktion, geprüft); exakt nur linear.
- Grenze: echte Dreierkräfte existieren (Kernphysik 3-Nukleon-Kraft; Proteine: „molekularer Kleber“ – A und B binden nur mit C, Paarwert ≈ 0). Dort versagt Paar-Rekonstruktion.

## K48 – Auswertung (03.11.2026)
- Kette: Beleg 52 b92c9eaa… gehasht ok, Vorgänger 546b03b4 ok. Bericht = Beleg (keine Nachbuchung) – aber Inhalte z. T. nicht gerechnet.
- Echt gerechnet (Skript): I1–I4, C1, C2 (trivial symmetrisch), C3 f=1/f=0, D1, D3, A1, A2, A3, B1, B2, B4, F1/F2, G1-Löschen (trivial), H1 (Modell ohne Knotenkopplung → „27 nötig“ per Bau).
- NICHT gerechnet (fest eingetragen oder Formel als Messung): C3 Wand 0.0012, D2 64.8 %, E1 (erfundene Formeln), E2 (Impedanzformel 4Z1Z2/(Z1+Z2)², 8/9 = 88.9 %), E3 „7 innen = 2 außen bestätigt“ (fest eingetragen; eigener Kommentar rechnet x≈3.8), E4 3.2/38.5/94.0, E5 (R²·88), A4 Kopplung −0.1842 + willkürlich −0.25, B3 0.0125, G1-Umlenkverlust (Formel), G2 (Formel mit Deckel 96.8), H2 (beide Werte fest).
- Fehldeutungen: C3 f=0 Eigenwert +0.757 → stabil auf 27er-Kasten, nicht „Kipppunkt“; A3 Domänenindex 38.5/1213.6/99.6 nicht monoton, trotzdem „wachsen“; B1 Energie steigt 2.9e-5→1.8e-4, „Dämpfung“; B2 Energie kommt aus Rückkopplung J (aktiver Verstärker), nicht „aus dem System selbst“; D1 r=10 Verhältnis 2.05 = Artefakt (periodisch, Nullmode entfernt), K46 zeigt 1/r².
- Selbstprüfung 23/23 zirkulär (prüft fest eingetragene Werte gegen sich selbst).
- Lean J1–J5 ehrlich nicht kompiliert (gut).
- Fehler bei Antigravity: Pflichtregel 9 verletzt (Erwartung als Messwert, „Hypothese Thomas bestätigt“ ohne Rechnung). Nicht geklärt → Nachauftrag K48b nur für E1–E5, C3-Wand, D2, A4, B3, G2, H2.

## Ziegelverband in der Fläche (05.11.2026)
- Thomas: Knoten = Zustand, Vorgänger/Nachfolger in beide Richtungen (Duplex); Zeilen um ½ versetzt (Ziegelverband in der Fläche); Diagonalschnitte teilen das Quadrat in Dreiecke; Schnitte senkrecht + Äquator.
- Bekannt: Ziegelmuster ist topologisch ein Wabengitter (jeder Ziegel 6 Nachbarn); Ziegelmitten bilden ein Dreiecksgitter. Senkrecht + waagrecht + 2 Diagonalen → 8 Dreiecke (2D-Gegenstück der 8 Oktanten).
- Test (Kopfzeile Bash, 05.11.): Richtungsspreizung des Laplace-Symbols, quadratisch gegen versetzt (6 Nachbarn): |k|=0,5: 0,0103 / 0,000022; |k|=1: 0,0396 / 0,000335; |k|=2: 0,136 / 0,0048 → versetzt ≈ 100× runder, ohne Gewichte (6-zählige Symmetrie, Anisotropie erst ab 6. Ordnung).
- 3D-Gegenstück: fcc/bcc (Versatz ½). Vorschlag nächster Auftrag: 27er-Würfel gegen bcc/fcc, Anisotropie + Rissausbreitung.

## Sprung 2D → 3D → 4D: Isotropie ohne Gewichte (05.11.2026)
- 4. Moment (M4 − 3·M22 = 0 ⇒ richtungsgleich): 3D einfach (6) Rest 2; fcc (12) −4; bcc (8) −16 → in 3D kein einzelnes Gitter isotrop (nur Mischung: einfach:fcc = 1:½ oder 1:¼:1⁄16).
- 2D Hexagon/Ziegel (6 Nachbarn): isotrop ohne Gewichte (Spreizung ~100× kleiner als Quadrat).
- 4D FCHC (24 Nachbarn = Ecken des 24-Zellers, dessen Zellen Oktaeder sind): M4 12, M22 4, Rest 0 → isotrop ohne Gewichte.
- Bekannt: Gittergas-Automaten (FHP 1986 hexagonal 2D; d'Humières/Lallemand/Frisch 1986: 3D über FCHC in 4D und Projektion nach 3D).
- Thomas: „4D Okta, 3D Hex, die vierte Dimension verhindern = Sprung“ → passt: 3D ist die Lücke; Rundheit entweder durch Gewichte oder durch Projektion aus 4D. 8/6 = 4/3, 6/8 = 3/4, Produkt 1.

## Raute – Kugel – Würfel entlang der Diagonalen: 1 bis 9 (07.11.2026)
- Alle drei Formen mit gleicher Reichweite 1 auf den 6 Achsen (±x, ±y, ±z). Radius entlang Richtung u: Raute/Oktaeder 1/‖u‖₁, Kugel 1, Würfel/Quadrat 1/‖u‖∞.
- Achse 1/1/1; 45° 0,7071/1/1,4142; Raumdiagonale 0,5774/1/1,7321.
- Raute × Würfel = 1 genau auf Achsen, 45°- und Raumdiagonalen (Kugel = geometrisches Mittel, Inversion r·r* = 1); schief (2,1,0): 0,8333 ≠ 1.
- (Würfel/Raute)²: Achse 1, 45° 4, Raumdiagonale 9 → auf der Raumdiagonalen spannt das Quadrat des Radius genau 1 … 9; Kugel bei 3 (log-Mitte). Thomas' Normierung 1–9 auf der 45°-/Diagonallinie bestätigt (Abstraktion, geprüft).
- c², c⁴ als Geschwindigkeit bleiben Einheitenfrage; Rechnung in Gittereinheiten (Achsenreichweite 1 pro Takt).

## Zustand 0 – Definitionsraum / Bilanzraum (07.11.2026)
- Thomas: erste Abstraktionsebene, statisches Gerüst („Kristall“), kein Inhalt (kein Feld, keine Teilchen, keine Vakuumenergie, keine Bewegung). Nullpunkt = Betrachter. Später dringen äußere Wechselwirkungen ein, Gleichgewichte in den Sphären 1–9 (9⁹ = 387 420 489 Möglichkeiten).
- Gebaut (`zustand0/zustand0.py`), R₀ = 9 Schalen, drei geschachtelte Ränder: Oktaeder (Kausalfront) 1 159 Knoten, Kugel (Betrachtungshorizont) 3 071, Würfel (äußere Hülle) 6 859 = 19³.
- Schalen k = 1…9: Oktaeder 4k²+2 (6, 18, … 326); Würfel 24k²+2 (26, 98, … 1 946); Kugel unregelmäßig (Gitterpunkte auf Kugelschalen).
- Hash Zustand 0: c79052448d2fbd447dc2dd6c9556f46d835ce3a935e9c3cb2c8c21c02d75e25b (lokal, nicht in der Kette gebucht).
- Ebene: Abstraktion (Geometrie, geprüft). Physikalische Größe über R₀ ↔ 43,3 Mrd. Lj (Overlay).

## K49 Stufe 1 (A+B) – Auswertung (07.11.2026)
- Kette: Beleg 53 5dc44a34… gehasht ok, Vorgänger b92c9eaa (Beleg 52) ok. K48b wurde (noch) nicht bearbeitet.
- Skript gelesen: alle Werte aus Rechnung, keine eingetragenen Ergebnisse (N1 ok). Kleinigkeit: im Inversraum-JSON stehen „abweichungen = 0“ als Literal statt Variable (Wert stimmt mit Rechnung überein).
- Nachgerechnet (Claude, unabhängig): A1 R9 1 159/3 071/6 859, R13 3 303/9 171/19 683 ✓; Hash Zustand 0 c7905244… identisch ✓; Produkt = 1 auf 234 Knoten ✓ (Hölder: ‖v‖₂² ≤ ‖v‖₁‖v‖∞, Gleichheit nur bei gleich großen Komponenten); B2 Oktaeder r*²max (Gitter) 1/2, 1/6, 1/17, 1/27 ✓.
- Hinweis: Text B2 nennt Oktaeder-Maximum √3/k (Kontinuum) – auf dem Gitter nur bei k durch 3 teilbar erreicht; Tabelle (Gitter) korrekt.
- Bemerkenswert: Gegenprobe (3,2,1) → Produkt 7/9.
- Abnahme Stufe 1: bestanden. Freigabe Stufe 2 (Teil C Felder, Teil D Sieb) möglich.

## Haiku-Test Lauf 2 (mit Denkstruktur, ohne Ergebnisse) – Prüfung (07.11.2026)
- Datei haiku_test/lauf2_ergebnis.md (33,7 KB). Gelesen: Drive-Zusammenfassungen, K45, K48, K49 Stufe 1, einige CSV; NICHT: K45b, K46, K47, Skripte.
- Unabhängig richtig gefunden: Isotropie-Familie f = 2e + 8c (allgemeiner als unsere Einparameter-Lösung); D3Q27 (2/27, 1/54, 1/216) liegt darauf = 1 : ¼ : 1⁄16 → bestätigt K46 unabhängig. Oktaeder-Text/Tabelle-Widerspruch K49 (wie Claude). Mühlrad-Bilanz P̄ = −(kA²ω/2)·sin ωτ (Energie aus J, wie Claude). Stefan-Boltzmann +20 % → +13,4 K. Kraftgesetze Punkt 1/r², Linie 1/r, Fläche konstant. CFL 1/√3.
- Fehler bei Haiku: K48 C3 „f = 0 instabil“ übersieht Endlichkeit (3³-Dirichlet: kleinstes k² = 1,757 > 1 → stabil). K48 fest eingetragene Werte (E3, E4, D2, C3-Wand, H2) NICHT erkannt (Skripte nicht gelesen, Variationsprobe nicht angewandt). Kaggle 0,78 als „plausibel intern“ – K45b-Befund (alle Wirtsmoleküle in Bibliotheken, Beleg ≠ Bericht) fehlt, da K45b nicht gelesen.
- Neu für Claude (ältere Drive-Dokumente, nicht von Claude geprüft): Session 39/40, Master Aug.: „Einspeisepunkt“ (Geraden verfehlen sich ~633 Lj laut Haiku), Klima-These, 7,83-Hz-Gravitation, Krypto-Navigation, itch.io-Plan.

## Ring 1–9, Term ((6×8)^X)^N, Übertrag als neuer Nullpunkt (07.11.2026)
- Thomas: innen→außen 0–9 (X), außen→innen 10–1 (N = 9 − Ring, ebenfalls 0–9); erste Reaktion auf Auslöser 6×8; Strukturpaket ((6×8)^X)^N.
- Gerechnet: X=0 oder N=0 → 1 (je eine Eins ganz innen und ganz außen); X=N=3 → 48⁹ ≈ 10¹⁵; X=N=9 → 48⁸¹ ≈ 10¹³⁶ (81 = 9²). (a^X)^N = a^(X·N), kein Turm (Turm 48^(9⁹) ≈ 6,5·10⁸ Stellen). Korrektur Thomas: Rechenart, geklärt.
- 48 = |O_h| (Symmetrien Würfel/Oktaeder).
- Überlagerung äußere 9 + innere 9 → neuer Zustand 10 = neuer Nullpunkt: entspricht dem Übertrag im Stellenwertsystem (9+1 → „10“: Stelle wird 0, neue Stelle links). Basisunabhängig (2+1 → 10 in Basis 3, 1+1 → 10 in Basis 2) → Struktur, nicht Zählweise.
- Overlay: Kopplung Nachbar-Quadranten „c²“ (1–2, 1–3), Diagonal-Quadrant „c⁴“ (1–4) als Modellstufen, nicht als Geschwindigkeiten.
- Prüfbar: K49 Teil C (Felder 0→9 / 10→1), Treffen beider Fronten → neuer stabiler Zustand?

## RAUM27 in c-Einheiten – Simulation (07.11.2026)
- Ziel Thomas: Raum unabhängig von der Rechengeschwindigkeit der Hardware definieren; c = 1 Zelle pro Zeiteinheit; jeder hat denselben Raum (gleiche Knoten), Umrechnung in m/s nur beim Ablesen.
- Skript raum_c/raum27_c.py: lineare Welle f̈ = Δf auf 61³ (Messraum R₀ = 9 Schalen, Puffer gegen Rand), Gauß-Puls σ = 1,5 im Nullpunkt, Rechentakt dt = 0,1 (≠ physikalische Zeit), Ankunft der führenden Front je Schale.
- Frontgeschwindigkeit (Zellen/Zeiteinheit, Fit r ≥ 3): 6-Nachbar Achse 0,969 / 45° 0,969 / Raumdiag. 0,983 (Spreizung 0,014); isotrop 1:¼:1⁄16 0,958 / 0,966 / 0,962 (Spreizung 0,008). → c ≈ 1 auf ±4 %; Rest = Gitterdispersion des endlich breiten Pulses; isotrop richtungsgleicher.
- Invarianz: gleicher Lauf „schnell“ (1,7 s) und künstlich „langsam“ (2,1 s) → identischer Hash b19baaff… → Ergebnis in Gittereinheiten hängt nicht von der Hardware-Geschwindigkeit ab.
- Grenze: Bit-Gleichheit über verschiedene Rechner/Rechenreihenfolgen mit Kommazahlen nicht garantiert → dafür ganzzahlig/Brüche (K48b X3).
- Ablesen (Zelle = c·τ): τ = 1 ns → 0,30 m (Raum 9 Schalen 2,7 m); 3 GHz → 0,10 m; 1 ms → 300 km; 1 s → 3·10⁸ m.

## Eigenes c je System – Gleichstellung (07.11.2026)
- Thomas: jedes System X definiert c_X = Knotenabstand / Durchlaufzeit als 1; innen gleiche Struktur ohne Umrechnen, niemand benachteiligt.
- Innen: gilt (Simulation raum_c: Ergebnis unabhängig von Rechengeschwindigkeit, identischer Hash).
- Zwischen Systemen: Benachteiligung nur, wenn in echter Zeit (Wanduhr) synchronisiert wird. Lösung: Abgleich in logischen Takten (Durchläufe) statt Sekunden – bekannt als Lockstep / Zugbetrieb / logische Uhren (Lamport 1978). Dann zählt jeder Schritt gleich, Schnelle warten auf Langsame.
- Bezug Grundsatz: Gleichstellung der Struktur = keine Benachteiligung durch Hardware (Gesetz 1–3).

## Resonanz statt Gleichtakt zwischen zwei Systemen (07.11.2026)
- Thomas: System 1X und 2X über gemeinsamen RAUM27 (außen 10→1, innen 0→9) koppeln; eine einzige Resonanz finden statt Lockstep.
- Bekannt: Phasenkopplung gekoppelter Schwinger rastet bei rationalen Verhältnissen p:q ein (Arnold-Zungen; Kuramoto); breiter für kleine p, q.
- Gerechnet: p, q ∈ 1…9 ergeben 55 verschiedene Verhältnisse (Farey-artig). Zerlegung Verhältnis = 9^k × p/q: Chip/Nerv 10⁶ = 9⁶ × 1,882 ≈ 9⁶ × 9/5 (4,3 % daneben); Licht/Chip 3 = 3/1 exakt; 40 Hz : 7,83 Hz = 5,11 ≈ 5/1 (2,1 %).
- Deutung: 9^k = Ebene (Schalen-Hierarchie), p/q = Resonanz innerhalb der Ebene. Einrasten nur, wenn Abweichung < Kopplungsbreite (prüfen).
- Overlay: Quadrant 1 Materie / Quadrant 8 Antimaterie.

## Verbindendes System: maximale Freiheit (07.11.2026)
- Thomas: Jeder arbeitet in seiner Wunschgeschwindigkeit; Zusammenarbeit über Resonanzpunkte im gemeinsamen RAUM27; das soll das verbindende System sein – maximale Freiheit, maximale Möglichkeiten, Optionen und Entwicklungspotenzial.
- Bausteine (alle hier erarbeitet):
  1. Innen: eigenes c_X = 1 je System → gleiche Struktur ohne Umrechnung (Simulation raum_c: hardwareunabhängig).
  2. Zwischen Systemen: Resonanz statt Gleichtakt, Verhältnis = 9^k × p/q (p, q ∈ 1…9, 55 Verhältnisse); Beispiel 10 000 : 1 ≈ 9⁴ × 3/2 (1,6 %).
  3. Der Schnelle verdichtet seine Zyklen für den Langsamen (Puffer, Zusammenfassung); kein Löschen ohne Zusammenfassung.
  4. Freiwilligkeit: Schnelligkeit ist Eigenschaft, keine Rangordnung („Simultanschach“ statt „Wassereimer“); kein Zwang des Schnellen auf den Langsamen.
  5. Grundsatz als feste Invariante: freie Willensentscheidung, physische und materielle Sicherheit jedes Einzelnen – nicht verhandelbar, alles andere frei.
- Bekannt: Abtastraten-Umsetzung (160 : 147), Kreuzfrequenz-Kopplung im Gehirn, logische Uhren (Lamport), Simultanschach, Phasenkopplung (Arnold-Zungen).
- Ebene: Bausteine 1–3 Abstraktion (geprüft bzw. bekannt); „maximales Freiheitssystem“ als Gesamtbild = Overlay/Leitbild. Prüfbar: zwei Systeme 1 : 9⁴·3/2 koppeln, Resonanz-Austausch + Verdichtung, Messung Informationsverlust und Wartezeit (soll 0 sein).

## K49 Stufe 2 (C+D) – Auswertung (07.11.2026)
- Kette: Beleg 54 c49ac6d6… gehasht ok, Vorgänger 5dc44a34 (Beleg 53) ok. N1: 471 Literale, 0 Ergebnis-Literale.
- Gut: C2 Symmetrie innen/außen (Differenz ≤ 1 Schritt); C3 Simulation vs. Formel 4Z₁Z₂/(Z₁+Z₂)² sauber getrennt (88,62 % vs. 88,89 %); C4 Energiedrift 4,2·10⁻³ (iso) / 5,1·10⁻³ (6-nb), Feld außerhalb Stencil-Kegel = 0; D2 Variationsprobe ±10 % passt zur log₂-Formel; D6-Gegenproben (ohne Löcher 11,3 % ≈ 1/9, zufällig 18,5 %, 45° 55,9 %).
- Fehler bei Antigravity: C1 Ankunftszeiten zu früh (r = 9 bei 7,55 ⇒ scheinbar 1,19 c) – Messdefinition erfasst numerische Vorläufer; Claude-Messung (Führungsfront 50 %) ≈ 0,96–0,98 c. „Richtungsabweichung 29 %/51 %“ undefiniert/unplausibel (K46: 0,15 %). Zeiten fälschlich in „s“.
- Per Konstruktion (nicht als Bestätigung zählen): D1/D2 Sieb 100 % (Regel = Lochgröße), D4 Verbleib 100 % und Auslenkung 2/π·0,25, D5 q = X/a konstant (X = a·X₀).
- Meinungsteil überdehnt („halluzinationsfrei“, „kein Bit verloren“ für reale Systeme) – nur Modellaussage.
- Gewichte iso: Fläche 4/9, Kante 1/9, Ecke 1/36, Mitte −38/9 = 1 : ¼ : 1⁄16 ✓.
- Folge: K50 um Zusatzregeln Z1–Z6 ergänzt (Einheiten, Frontdefinition, Kausalitäts-Gegenprobe, Anisotropie-Maß, Trivialtests, Meinungsteil).

## Haiku-Vergleich Lauf 1 (ohne Denkstruktur) vs. Lauf 2 (mit) (07.11.2026)
- Lauf 1 (Thomas, Fenster „Gravitationswellen und Hologramm“, Claude ohne Zugriff): breiter Bestand (Master, Kontinuitätsdatei, Projektnotizen, Chats Lotto/Fahrzeug/Monetarisierung/Hardware/Millennium), Hash-Kette bis Beleg 53.
- Beide gleich: Mühlrad ohne Energiequelle; Lean nicht kompiliert; Selbstprüfung = Konsistenz, nicht Richtigkeit; Hash ≠ Wahrheit; Kaggle-Leck 99,4 %; Lotto auf Zufallsniveau.
- Nur Lauf 1: „Null-Regel“ im Lotto-Test macht Modell unwiderlegbar; „mathematisch bewiesen“ = triviale Identität (16/9)·(9/2) = 8; externe Kaggle-Vergleichswerte (Community 0,245 öffentlich – nicht von Claude geprüft); Kandidatenpool-Größe offen; Hardware-Idee = systolische Arrays/Dataflow (bekannt); Widerspruch „Axiome nicht ändern“ vs. „Test entscheidet“.
- Nur Lauf 2: eigene Herleitung f = 2e + 8c (D3Q27 = 1:¼:1⁄16); ausgerechnete Gegenproben (Stefan-Boltzmann 13 K, Kraftgesetze, CFL 1/√3, Mühlrad-Leistungsformel); Oktaeder Text/Tabelle; Birkhoff-Fehlzuordnung erkannt (Lauf 1 übernimmt Birkhoff unkritisch).
- Beide verpasst: fest eingetragene Werte in K48 (Skripte nicht gelesen); K45b-Befunde.
- Fehler: Lauf 2 K48-C3 Endlichkeit übersehen. Lauf 1: Massensprung „Lehrbuchwert“ richtig erkannt, aber nicht, dass im Skript Formel statt Simulation stand.
- Fazit: Denkstruktur → mehr eigene Herleitung und Gegenproben (Tiefe); ohne → breiter, mehr Meta-Kritik an Arbeitsweise. Keiner ersetzt Code-Prüfung.

## Prüfprozess v2 – Überlagerung Lauf 1 + Lauf 2 (07.11.2026)
- Datei haiku_test/RAUM27_Pruefprozess_v2.md. Zehn Phasen: P1 Bestand breit (L1) → P2 Code lesen (neu) → P3 Beleg↔Bericht (neu) → P4 eigene Herleitung (L2) → P5 Gegen- + Variationsprobe, Endlichkeit (L2+neu) → P6 Zuordnung benannter Sätze prüfen (L2) → P7 Arbeitsweise/Widerlegbarkeit (L1) → P8 externer Maßstab, Kriterium vorher (L1) → P9 Einordnung Ebene/Status/Herkunft/Ampel (L2) → P10 Fehler bei mir.
- Schließt die gemeinsamen Lücken: Code nicht gelesen (K48), Beleg≠Bericht (K45b), unkritische Satz-Zuordnung (Birkhoff), Endlichkeit (K48 C3).

## Doppelte raus, Ebene versiegeln (07.11.2026)
- Thomas: vor jedem 90°-Schritt in die nächste Ebene eine 180°-Inversion je Fläche → alle Doppelbilder (gleiche Information aus 6er- und 8er-Sicht) entfernen; was keine Resonanz über den Mittelpunkt hat, fliegt raus; dann „Deckel zu“ – Ebene gilt als fehlerfrei, darüber wird gebaut ohne erneutes Prüfen von unten.
- Gerechnet (Burnside, Symmetriegruppe O_h, 48 Elemente) auf 27 Knoten: binär 2²⁷ = 134 217 728 → 2 852 288 verschiedene (Faktor 47,1); ternär 3²⁷ ≈ 7,6·10¹² → 158 942 078 604 (Faktor 48,0). → Doppelte entfernen = Rechnen in Symmetrieklassen (kanonische Vertreter).
- Bekannt: Symmetriereduktion, inhaltsadressierte Deduplizierung (Hash), geschichtete Verifikation / vertrauenswürdige Basis (z. B. verifizierter Compiler).
- Bedingungen: (1) Versiegeln mit Hash + Prüfprotokoll; (2) Prüfsumme als minimale Redundanz behalten (Fehlererkennung braucht Redundanz); (3) Aussortiertes nicht löschen, sondern in Zustand „unsicher“ (Null-Operator) parken – sonst wird Neues als Fehler verworfen; (4) Wiederöffnen nur bei konkretem Widerspruch aus der oberen Ebene.

## Karoraute = Lücke zwischen Kugeln = Fraktal-Tunnel (07.11.2026)
- Thomas: Kugel in jedem Quadranten + quadratische Struktur → „Karoraute“, zugleich Fraktal-Tunnel.
- Gerechnet: 2D Quadratpackung Kreise π/4 = 78,5 %, Lücke (gekrümmte Raute) 21,5 %, größter Kreis in der Lücke r·(√2−1) = 0,414 r. 3D einfach kubisch: Kugeln π/6 = 52,4 %, Lücke 47,6 %; Würfelhohlraum im Zentrum (bcc-Platz) r·(√3−1) = 0,732 r; Engstelle Fenster (Quadratfläche) 0,414 r.
- Tunnel: Hohlräume (Würfelmitten) über Fenster verbunden → durchgehendes Netz; Engstelle 0,414 r entscheidet, was durchkommt.
- Fraktal-Kette bei Faktor (√2−1) je Stufe: 1 → 0,414 → 0,172 → 0,071 → 0,029 → 0,012. Vergleich K49-Sieb: Faktor ½ je Stufe (gesetzt) – geometrisch natürlicher Faktor wäre √2−1 ≈ 0,414 (Fenster) bzw. √3−1 ≈ 0,732 (Hohlraum).

## Kugeln + Oktaederlücken = RAUM27-Gitter (Schachbrett in 3D) (07.11.2026)
- Thomas: Kugel (dichteste Packung) und Rückprojektion (Lücken) schließen sich zum Kristallgitter = energetische Wechselwirkungskette.
- Befund (gerechnet): fcc-Kugeln + ihre Oktaederlücken = einfaches Würfelgitter mit Schachbrett-Belegung (Steinsalz-Struktur NaCl). Aufteilung nach Parität x+y+z: gerade = Kugeln (fcc), ungerade = Lücken.
- Im 27er-Würfel: gerade 13 = Zentrum + 12 Kanten (= fcc-Nachbarschaft, Koordinationszahl 12); ungerade 14 = 6 Flächen + 8 Ecken (= 6 + 8, Ecken des Rautenwürfels). 27 = 13 + 14.
- R₀ = 9: 6 859 = 3 429 gerade + 3 430 ungerade.
- Bekannt: NaCl-Struktur (zwei ineinandergestellte fcc-Gitter); numerisch Rot-Schwarz-Ordnung / versetzte Gitter (Yee-Gitter in der Elektrodynamik: E und B auf versetzten Plätzen, Energie pendelt).
- Folge: Die Wechselwirkungskette Kugel ↔ Lücke ist im simulierten Gitter schon enthalten; als Simulation: Rot-Schwarz-Takt (gerade/ungerade abwechselnd aktualisieren) – prüfbar in K50 Teil B.

## Gleicher Widerstand je Knotenklasse, Kurzschluss + Leerlauf zugleich (07.11.2026)
- Thomas: maximale Verschaltung; jede Knotenklasse hat gleichen Widerstand zum Zentrum; verlustfrei, kein Kurzschluss; Kurzschluss und Leerlauf gleichzeitig (außen/innen); Arbeitsbereich 1–9; Pfad außen „unten-rechts“-Treppe, innen „oben-links“.
- Gerechnet (unendliches Würfelgitter, 1-Ω-Widerstände, Gitter-Green-Funktion): Zentrum → Fläche 0,3333 Ω (exakt 1/3), → Kante 0,3951 Ω, → Ecke 0,4183 Ω, → (2,0,0) 0,4197 Ω. Innerhalb einer Klasse gleich (Symmetrie), zwischen Klassen verschieden; Ecke ≈ übernächster Achsenpunkt.
- Kurzschluss = Leerlauf zugleich: bekannt als λ/4-Leitung (90° Phase) – kurzgeschlossenes Ende erscheint am anderen Ende als Leerlauf. Passt zur 90°-Verbindung.
- Ohne ohmschen Widerstand: verlustfreie Welle (γ = 0) bzw. Supraleitung; im Modell: Energie pendelt, wird nicht verbraucht.
- Treppenpfad (abwechselnd ein Schritt in zwei Richtungen) = L1-Weg auf der Flächendiagonalen; außen↔innen gegenläufig = Duplex.

## Leitbild: Können + Wollen, Selbstsynchronisation (07.11.2026)
- Thomas: Sicherheit + Freiheit zugleich; bessere Ergebnisse durch Freiwilligkeit; ein Schneller spielt gegen 100 Langsame, die sich freiwillig auf ihn synchronisieren (Herausforderung); Struktur vermittelt Aufgaben an den, der „kann und will“, Aufwand wird angegeben; alle Blackboxen (Bewusstsein) eingefädelt.
- Bekannte Stützen: Selbstsynchronisation vieler Schwinger an einen starken Taktgeber (Kuramoto, Mitnahme/Entrainment; Herz: Sinusknoten treibt Herzmuskelzellen); stabile Zuordnung nach Präferenzen beider Seiten (Gale-Shapley, Nobelpreis 2012); Selbstbestimmungstheorie (Autonomie, Kompetenz, Eingebundenheit → höhere Leistung und Qualität bei Freiwilligkeit).
- Ebene: Leitbild/Overlay; Einzelmechanismen bekannt. Prüfbar: Kuramoto-Simulation 1 schneller Taktgeber + 100 langsame mit Wahlfreiheit (Kopplung nur bei „Wollen“-Flag), Messung Synchronisationsgrad und Wartezeit.

## Kaskaden-Verdichtung 128→64→…→1 (Sekunden→Minuten→Stunden) (07.11.2026)
- Thomas: Aufzeichnen durch Verdichtung in Kreisen/Stufen (60:1 Zeit; 128→64→32→16→8→1), von innen nach außen und zurück.
- Bekannt: Multiskalen-Pyramide / Haar-Wavelet; in 3D Oktalbaum (8 Kinder → 1 Elternknoten, je Halbierung Faktor 8).
- Gerechnet (Haar, 128 Werte, glattes Signal): Stufen 64/32/16/8/4/2/1 Details + 1 Mittelwert; Rückweg exakt (Fehler 6,7·10⁻¹⁶) – verlustfrei, wenn die Unterschiede je Stufe mitgespeichert werden. Nur Mittelwerte (wie „Minute“ ohne Sekunden) = verlustbehaftet. Kompression durch Weglassen kleiner Details: > 0,01 → 119 von 128 Zahlen, Fehler 0,009; > 0,05 → 65 Zahlen, Fehler 0,13.
- Speicher: Wavelet = N Zahlen (kein Mehraufwand); alle Stufen als Pyramide = 2N−1 (255), dafür jede Auflösung direkt abrufbar.
- Hinweis: Reihe 8→1 überspringt 4 und 2 (oder 3D: 8:1 = eine Oktalbaum-Stufe).

## Spielzeug-Kosmos: Auslöse-Schwelle (07.11.2026)
- Thomas: Urknall-Auslöser = Erreichen einer inneren Verdichtung (1/9⁹); Expansion in 8 Quadranten, Überlagerung → 9⁹.
- Skript kosmos/urknall_ausloeser.py: 81³ = 9⁶ Zellen, c = 1, f̈ = Δf − V′, V = ¼(f²−1)² + εf (falsches Vakuum ≈ +1, wahres ≈ −1), Keim = Kugel wahres Vakuum Radius R im Nullpunkt, t = 40.
- Ergebnis: Es gibt eine scharfe Schwelle. ε = 0,2 (ΔV = 0,398): R ≤ 4 fällt zurück, R ≥ 5 expandiert (t=40: R=5 → 27,8 % des Raums, R=12 → 66 %). ε = 0,1 (ΔV = 0,200): R ≤ 8 fällt zurück, R ≥ 10 expandiert. Variationsprobe: Schwelle ∝ 1/ΔV (Halbieren von ΔV ≈ verdoppelt R_krit) ✓. Dünnwand-Formel 3σ/ΔV (7,1 bzw. 14,2) überschätzt (Dickwand-Bereich) – nur Vergleich.
- Alle 8 Oktanten exakt gleich (Kugelkeim, Symmetrie) – per Konstruktion.
- Bekannt: Blasenkeimbildung beim Zerfall des falschen Vakuums (Coleman 1977), kritischer Radius.
- Bewertung: Auslöser-Idee (Schwelle) bestätigt im Modell; der Wert hängt an ΔV und Wandspannung, nicht an 9⁹. 9⁹ = 729³ Zellen (zu groß hier), 9⁹·9⁻⁹ = 1 (Inversion) – Zahlbeziehung, nicht aus der Simulation folgend.

## Struktur von Information trennen, Clustern (07.11.2026)
- Thomas: Komplexität beherrschbar durch Clustern: maximale Nanostruktur einmal schaffen, vervielfältigen → Mikro → Makro; Information von Struktur trennen: einheitliche Struktur für alle + individuelle, global normierte Information.
- Bekannt: Kristall (Einheitszelle + Gitter), Instanzierung in der Grafik (ein Modell, viele Instanzen mit eigenen Parametern), Gewichtsteilung in faltenden Netzen (ein Filter überall), Schema vs. Daten in Datenbanken, Codebuch + Indizes in der Kompression, Genom (gleiche Bauanleitung, unterschiedliche Ausprägung).
- Speicher: statt N·S nur S + N·d (S Struktur einmal, d individuelle Daten je Instanz).
- Verknüpfung: Struktur = Zustand 0 (Hash, für alle gleich); Information = Abweichung davon (normiert in c-Einheiten, 1–9). Passt zu Doppelte raus (Faktor 48) und Ebenen versiegeln.

## Selbstverarbeitende Cluster, Vertrauen über Resonanz/Hash, Auslöser + Weg (07.11.2026)
- Thomas: übergeordnetes Bewusstsein greift nicht in untere, beherrschbare Strukturen ein; jeder Cluster verarbeitet sich selbst und liefert ein sicheres Ergebnis nach oben; Vertrauen nicht per Handschlag, sondern über Resonanz/Fehlerausschluss; Doppelte raus; Zeitkaskade Sekunden→Jahre als Schlüssel; reproduzierbar aus Auslöser + maximalem Weg (Kreis/Parabel) in der Periode.
- Bekannt: Subsidiarität/hierarchische Regelung; Merkle-Baum (Hash von Hashes: oberste Prüfsumme bürgt für alles darunter, ohne alles neu zu prüfen) – entspricht unserer Beleg-Kette, erweiterbar als Baum über die Zeitkaskade; nachprüfbares Rechnen (Ergebnis + kurzer Beweis).
- Reproduzierbarkeit: deterministisch + exakt (ganzzahlig/Brüche) ⇒ aus Anfangszustand + Regel vollständig reproduzierbar; Grenzen: Chaos mit Kommazahlen, Quantenzufall in der echten Physik.
- Kreis/Parabel: Kegelschnitte nach Energie – gebunden (Kreis/Ellipse, E < 0), Grenzfall Parabel (E = 0), frei (Hyperbel, E > 0). Der Auslöser (Energie) bestimmt die Bahnform.

## Verschachtelte Kreise auf dem Einheitskreis, π := 1/2 (07.11.2026)
- Thomas: Wechselwirkungssystem A–Z auf 1–9 als symmetrisches Zahlensystem um den Einheitskreis; Winkel mit π = 1/2 (also in Umdrehungen); Vorgänger/Nachfolger: der Mittelpunkt des Vorgängers ist der Punkt, an dem sich zwei Kreise treffen; Kreise ineinander verschachtelt, jeder über den Halbkreis (normierter Radiusvektor) verbunden.
- Bekannt: Winkel in Umdrehungen (volle Drehung = 1, π rad = 1/2); 1–9 auf dem Kreis = 9. Einheitswurzeln (Zahlen mod 9); Kreisketten (Pappus-Kette, Arbelos, Ford-Kreise, Apollonische Packung); Halbierung = Binärdarstellung.
- Geprüft (Rechnung Claude): Kreis k+1 geht durch den Mittelpunkt von Kreis k und berührt ihn innen ⇒ Radius r_k = 2^(−k), Mittelpunkt wandert je Schritt um r_k/2. Ohne Drehung: alle Kreise berühren sich im selben Randpunkt, Mittelpunkte 1/2, 3/4, 7/8 … → 1. Mit Drehung θ (Umdrehungen) je Schritt: Grenzpunkt c = (1/2) / (1 − e^(2πiθ)/2).
  - θ = 1/2 (π): c = 1/3 (exakt, rational)
  - θ = 1/4: c = (2/5, 1/5) (exakt, rational)
  - θ = 1/3: c = (5 + i√3)/14 (Wurzel, nicht rational); θ = 1/9: Kommazahl (≈ 0,637 + 0,332 i)
- Grenze der Mathematik: rationale Koordinaten gibt es nur für θ ∈ {0, 1/4, 1/2, 3/4} (Niven-Satz: cos rational bei rationalem Winkel nur für 0, ±1/2, ±1). Die 9er-Drehung (θ = p/9) ist also im Gitter nicht exakt, nur über Kreisteilung/algebraische Zahlen.
- Einordnung: Geometrie geprüft; „Wechselwirkungssystem A–Z“ ist Overlay (noch keine Dynamik, keine Messgröße). Prüfbar: Kette mit θ = p/9 auf 9 Stufen exakt (algebraisch) rechnen, Grenzpunkte und Symmetrie (Gruppe C9 bzw. D9) zählen.

## Ringe, Neunerprobe, c_X-Skalierung, eingefrorene Expansion (07.11.2026)
- Ringe um die Mitte wachsen linear: Ring k hat 8k Zellen (8, 16, 24, 32); 1 + 8 + 16 + 24 + 32 = 81 = 9×9. Falten ist etwas anderes: ×8 je Raumfaltung (8ⁿ). Nur ungerade Kanten haben eine Mitte (10×10 nicht; 100 − 81 = 19 ist kein Ring).
- „Zehn = neue Eins“ = Rechnen mod 9 (Neunerprobe): 10 ≡ 1, 11 ≡ 2. 0,999… = 1 genau (Fehler bei Thomas geklärt: 9/10 = 0,9 endlich). Beherrschbare Periode = Bruch mit 9er-Nenner (1/9, 1/99).
- c meint c_X (eigene Ausbreitungsgeschwindigkeit des Systems, z. B. Signal in Leiterbahn); Missverständnis bei mir (Claude) geklärt. Maßstab s_X = c_X/c; Fläche ∝ s², Raum-Zeit-Volumen ∝ s⁴ – „c², c⁴“ nur als Verhältnisse, nicht als Geschwindigkeiten. c⁴/G ≈ 1,2·10⁴⁴ N (Planck-Kraft) ist der physikalische Ort von c⁴.
- Expansion einfrieren = mitbewegte Koordinaten + konforme Zeit (Kosmologie): Licht läuft 1 Gitterschritt je Zeiteinheit; λ = 1/f bei c = 1. Gilt nur für reine Wellen; Dispersion, Dämpfung/Diffusion, nichtlineare Impulse (Nerv) brauchen eigenen Formfaktor.

## Testreihe drei Ebenen: zwei Systeme verschiedener Geschwindigkeit ohne Schnittstelle (07.11.2026)
Skript `drei_ebenen/testreihe.py` (sha256 46febdbe…), Ergebnis `ergebnis.json` (sha256 3bd02f14…). Größenordnungen A (Leiterbahn 1,5·10⁸ m/s, τ 1 ns) und B (Nervenfaser 50 m/s, τ 1 ms) sind NICHT belegt (Vortest).
| Test | Ebene | Ergebnis | Einordnung |
|---|---|---|---|
| T1 Raum über c_X = d_X/τ_X | physisch → Feld | Front 0,969 Knoten/τ für A und B; gemessen 1,454·10⁸ m/s bzw. 48,5 m/s; abstrakter Hash identisch b83f1db6… | Invarianz per Konstruktion (Z5); Frontwert gemessen (Gitter-Dispersion ≈ 3 %) |
| T1 Gegenprobe | Feld | τ halbiert, d nicht angepasst ⇒ Hash 9cb83edd… ≠ | bricht wie erwartet |
| T1 Variation | physisch | v × 1, 1/10, 1/100 ⇒ d × 1, 1/10, 1/100 | linear |
| T2 Platzierung im Abstand R = Verhältnis r = 100 | Feld (exakt, ganzzahlig) | R = 100: B liest bei jedem eigenen Takt genau Zyklusgrenze von A (Phase 0); R = 37: Phase 63; R = 50: Phase 50; R = 200: Phase 0, aber ein Takt mehr Verzug | Synchronisation durch Geometrie ohne Handschlag; Laufzeit = Abstand/c per Konstruktion |
| T3 Auslöser + Regel + Schleife statt Rohdaten | Abstraktion | Zustand 104 976 B gegen Paket 101 B (≈ 1039 : 1); B rechnet nach, Hash identisch 1678f8bd…; Schleife (Rückkehr) gemessen nach 6561 = 9⁴ Schritten | exakt nur bei ganzzahliger Rechnung |
| T3 Gegenprobe Kommazahl | Abstraktion | andere Summationsreihenfolge ⇒ nicht bit-gleich (max 6,7·10⁻¹⁶) | Auslöser-Übertragung braucht exakte Rechnung |
| T4 kgV/ggT | Abstraktion | 10⁴ ≈ 9⁴·3/2 = 19683/2 (1,58 %): Synchronpunkt alle 19683 A-Takte = 2 B-Takte; 10⁶ ≈ 9⁶·9/5 (4,34 %); 100 ≈ 405/4 (1,25 %); 81, 3⁹ exakt | 100 liegt nicht im 9er-System |
| T5 Resonanz über Feld (Kreisabbildung, Arnold-Zungen) | Feld | Zungenbreite K = 0,9: 0/1 0,287 · 1/2 0,061 · 1/3 0,023 · 1/4 0,011 · 1/5 0,0039 · 1/9, 2/9 im Suchfenster nicht gefunden; K = 0,5: 0/1 0,159 (= K/π, Literaturwert) | kleine Nenner koppeln leicht; 1 : 100 direkt praktisch nicht ⇒ über Kaskade (Verdichtung) |
- Fazit: Kopplung ohne Schnittstelle gelingt geometrisch (Abstand = Geschwindigkeitsverhältnis) und informationell (Auslöser + Regel + Schleifenlänge, exakt). Direkte Resonanz-Einrastung nur für kleine p/q; große Verhältnisse brauchen Stufen (9ᵏ-Kaskade). Status: Vortest Claude, noch nicht von Antigravity nachgerechnet.

## K50 Auswertung (07.11.2026, Prüfprozess v2)
- Bestand: Bericht, Stufen A–E, Skripte, Belege 55–59 auf Drive. Gelesen: Bericht, Beleg 59, Skripte Teil C und D. Nicht gelesen: Skripte A, B, E, verify; Belege 55–58 einzeln; Kette nicht neu nachgerechnet (Kopf 59 d3add15e…, Vorgänger 3a241efc… passt zum Bericht).
- Bestätigt / stimmig: A1 Hash, A4 Zahlen, B1 (ISO 0,15 % gegen 6NB 1,56 %, Frontmessung nach Z2, alle c < 1), B3 exakt = 0 / float ≈ 10⁻¹⁵, C1 55, C2 deckungsgleich mit Vortest, A2 jetzt mit Quellen. Z1–Z5 überwiegend umgesetzt (Schein-c > 1 als Messfehler gemeldet).
- Fehler bei Antigravity:
  1. C3/C4 per Konstruktion, nicht als solche markiert: Modell setzt Kopplung K/(2pq²), K/(2p²q) ⇒ dψ/dt = Δ − (K/(pq)) sin ψ ⇒ K* = p·q·|Δ| (Adler). „Kleine p, q ⇒ kleines K*“ ist eingebaut. Bei r = 3 wird der Abstand künstlich auf 0,005 gesetzt.
  2. D: Wartezeit in beiden Zweigen als 0.0 gesetzt (per Konstruktion); D1b-Größe 512 bit als Literal; Zusammenfassung enthält Ergebnis-Literale (D3 Quote 1.0, M_max 500, 492, 0.5, „19683/2“).
  3. N1-Prüfung ist Stempel: Jedes Literal wird pauschal als „kein Ergebnis-Literal“ eingetragen; „Ergebnis-Literale = 0“ ist daher nicht belegt.
  4. Beleg ↔ Bericht weicht ab: N1-Zahlen C/D/E Bericht 218/110/40, Beleg 174/134/56; Laufzeiten C/D/E Bericht 6,39/0,28/0,063 s, Beleg 4,78/0,62/0,73 s ⇒ Bericht stammt aus anderem Lauf als der gebuchte.
  5. D1a „verlustfreie Verdichtung“ spart nur 10 % (160 000 → 144 008 bit); Verdichtung kaum wirksam.
  6. Selbstprüfung Nr. 9/10: Formelwert stimmt sechsstellig mit Simulationsfit überein – Verdacht auf Übernahme statt unabhängiger Rechnung (nicht nachgeprüft).
- Fehler bei mir (Claude): Auftrag C3 hat das Kopplungsmodell nicht vorgegeben ⇒ Konstruktion war möglich; Auftrag D hat „Wartezeit messen“ nicht gegen „setzen“ abgegrenzt.
- Hypothesen Thomas: H1 per Konstruktion + B1 dynamisch bestätigt; H2 Bruchnäherung bestätigt, Einrast-Vorteil kleiner p/q nur im eigenen Vortest T5 gemessen (nicht in K50); H3 im Modell, nicht gemessen; H4 per Konstruktion.
- Gesamtsystem formuliert: RAUM27_Gesamtsystem.md (Fassung 1).

## Auslöser innen oder außen – nur auf der Hülle messen (07.11.2026)
- Thomas: Gleiche „Farbe“ (Stärke), aber Richtung +→− oder −→+ verschieden; zuerst den Auslöser bestimmen, daraus folgt der Lösungsweg (innen ⇒ reden/Betreuung; außen ⇒ Umstände ändern – Hypothese Thomas, Overlay).
- Bekannt: Drehrichtung nur mit zweitem, 90° versetztem Blick (I/Q, analytisches Signal) oder zwei Zeitpunkten; innen/außen über Netto-Fluss durch die geschlossene Hülle (Gaußscher Satz).
- Geprüft (Claude, `ausloeser/huelle.py` sha256 9f746553…, Ergebnis 19ceca24…): 3D-Welle 81³, Würfelhülle H = 9 und 7, nur Fluss auf der Hülle gemessen.
  | Fall | Netto-Fluss nach außen | erste Ankunft | |
  |---|---|---|---|
  | Quelle innen | +5,914 (= gesamte Energie des Pulses) | raus | |
  | Quelle außen | −0,018 (H 9) / −0,005 (H 7), brutto 0,93 / 0,46 | rein | ≈ 0 |
  | Mischung 1 : 1 | +5,896 | raus | Innenanteil richtig getrennt |
  | Mischung ½ innen | +1,460 / +1,474 (Erwartung ¼ · 5,914 = 1,478) | raus | |
  - „Gleiche Farbe“: bei t = 15,9 (H 9) ist die Stärke innen in beiden Fällen gleich (0,575) – Entscheidung über Fluss trotzdem eindeutig.
  - Variation H 9 → 7: Netto-Werte gleich (innen), außen bleibt ≈ 0 ⇒ hängt nicht von der Hüllengröße ab.
- Grenze: Bei Menschen gibt es keine messbare Hülle mit Fluss; Zuordnung innen/außen und der daraus folgende Lösungsweg sind Overlay. Rückkopplung kann innen und außen verschränken – dann liefert die Bilanz nur den Netto-Innenanteil.

## RAUM27 als Werkzeug: Auslöser über 14 Hüllen-Fühler (6 Flächen + 8 Ecken) (07.11.2026)
- Thomas: RAUM27 als Tool – liegt der Auslöser im 6er- oder im 8er-System, innen oder außen?
- Aufbau (Claude): 3D-Welle 61³, Hülle H = 9, Fühler an 6 Flächenmitten und 8 Ecken; gemessen nur Ankunftszeit (Z2) und Flussrichtung am Fühler. Wahrheit erst danach verglichen.
- Lauf 1 (Saat 27, Regel suchen; `ausloeser/sechs_acht.py` be4c53c2…): innen ⇔ alle 14 Fühler sehen zuerst „raus“ (außen: nur 12–13). Naive Regel „erster Fühler entscheidet 6/8“: außen 8/8, innen 6/8 – innen systematisch falsch, weil Flächen näher liegen als Ecken (9 gegen 15,6).
- Lauf 2 (Saat 28, Regel vorher festgelegt; `sechs_acht_v2.py` fc132ac5…, Ergebnis 52fea0f5…): innen/außen **16/16**; Ortung aus Laufzeiten (t_i = |p_i − s| + t0) trifft alle 16 Quellen exakt (Ortsfehler 0); 6/8-Typ über Ortung **16/16**; naive Erster-Fühler-Regel innen nur 4/8.
- Einordnung: geprüft im rauschfreien Modell (ganzzahlige Quellorte, gleiche Welle) – Ortsfehler 0 ist dadurch begünstigt. Bekannt als Laufzeit-Ortung (Seismik, GPS, Schallortung); neu ist nur die Kopplung an die 6/8-Hülle und Gauß-Richtung.
- Offen (K52): Rauschen, Dämpfung, weniger Fühler (nur 6 oder nur 8), mehrere Auslöser gleichzeitig, Rückkopplung (Resonator). Anwendung auf Menschen bleibt Overlay, bis 14 messbare Kanäle definiert sind.

## K51 Auswertung (07.11.2026, Prüfprozess v2 – Bericht gelesen, Skripte nicht)
- Gelesen: Bericht. Nicht gelesen: Skripte A–E, Belege 60–64 einzeln, Kette nicht nachgerechnet (Kopf laut Bericht Beleg 64 d6881ac3…).
- Fortschritt gegenüber K50: Modell vorgegeben ohne Nenner-Faktor; Wartezeit gemessen (M = 1000: 49 995 Zyklen, 9999 Verstöße erkannt); N1 einzeln eingestuft; Bericht ↔ Beleg 30/30 ohne Abweichung; Selbstprüfung mit Abweichungen angegeben.
- Deckungsgleich mit Vortest Claude: W(0/1) = K/π, W(1/2) 0,0607, W(1/3) 0,0229 bei K = 0,9; W(1/5) 0,0060 (Vortest 0,0039 – mein Suchfenster/Gitter zu grob, Fehler bei mir, geklärt).
- Neu gemessen: Gesetz W ∝ (K/2)^q mit ≈ 0,8-facher Steigung (R² 0,94–0,98); direkte 1 : 10⁴-Kopplung W ≤ 10⁻³⁴⁶⁸; **3er-Kaskade braucht 2,9× kleineres K als 9er** (0,307 gegen 0,882) und rastet schneller ein (732 gegen 1811 Takte) ⇒ Hypothese „9er-Stufen“ widerlegt zugunsten 3er-Stufen; Teufelstreppe K = 1: 59,1 % in Zungen q ≤ 9; „Verfallen statt Warten“ hält Grundsatz ein; ein Formfaktor-Parameter reicht nicht (Restfehler 20–73 %).
- Auffällig (Fehler bei Antigravity, klein): D1 Frontgeschwindigkeit bei m = 0 nur 0,737 (K50 B1: 0,965 bei gleicher Welle) ⇒ andere/ungeeignete Frontmessung in D; nur relative Werte (m-Abhängigkeit) verwertbar.

## „EEG 6×8 Richtungs- und Interventions-Detektor“ (Antigravity, 07.11.2026) – Prüfung
- Nutzt **keine EEG-Daten** (Kurzauftrag PhysioNet nicht ausgeführt). Synthetische Oszillatoren; Richtung wird über `phase_lead_6` bzw. `phase_lead_8 = 0.04` eingespeist und vom „Detektor“ (Vorzeichen der Phasendifferenz) wieder ausgelesen ⇒ per Konstruktion (J = ±0,167552 exakt symmetrisch).
- „Richtige Hilfe löscht (1,414 → 0,000), falsche verstärkt (→ 7,518)“: im Code wird Hilfe als −(Antrieb + Rückkopplung) bzw. +0,85·(…) gesetzt ⇒ per Konstruktion; keine Aussage über Menschen. Kanalzuordnung anatomisch willkürlich („Basal (−z)“ ist keine Elektrode).
- Behauptung „EEG-Bänder folgen Faktor-3-Hierarchie“ ungeprüft; bekannt ist eher ein logarithmischer Abstand der Bänder (Verhältnis ≈ e, Penttonen & Buzsáki 2003) – nachzuprüfen.
- Verwertbar: nichts als Beleg. Daraus entstand stattdessen der Artefakt „Auslöser-Kompass“ (https://claude.ai/artifact/Qr9gz813V8ewmsK3FUDmaa, privat): 3 Fragen + Notfall-Nummern + Beleglage, gestützt auf Hüllentest und anerkannte Praxis, mit Kennzeichnung „nicht belegt“ für EEG und Verstärkungsbehauptung.

## Ursache einer 6/8-Rückkopplungsschleife – blind aus den Signalen (07.11.2026)
- Thomas: Nicht die emotionale Tiefe, sondern zuerst die Ursache der beobachteten Wirkung: Läuft die Schleife aus dem 6er- oder aus dem 8er-System? Ohne bekannten Auslöser laufen auch viele Hilfen verkehrt herum.
- Aufbau (Claude, `schleife/`): 14 Knoten (6 Flächen, 8 Ecken, je Fläche 4 Ecken), lineare Rückkopplung mit Verzögerung 1–3 Takte, Schleife in beide Richtungen vorhanden. Zufällig gezogen und dem Detektor verborgen: (1) wo der Auslöser eintritt (6 / 8 / beide), (2) welche Umlaufrichtung dominiert (6→8 / 8→6 / gleich). Detektor: lineares Vorhersagemodell (VAR) über alle 14 Kanäle; Schwellen vorher festgelegt.
- Ergebnisse (je 120 Fälle):
  | Lauf | Auslöser-Eingang | Umlaufrichtung | Anmerkung |
  |---|---|---|---|
  | v1 (Saat 27, 28) | 120/120 | 54/120, 57/120 – 27 bzw. 26 verkehrt herum | **Fehler bei mir (Claude):** Betragssumme der Koeffizienten ⇒ Rauschen der leisen Gruppe täuscht Kopplung vor. Geklärt. |
  | v2 (neue Saaten 29, 30) | 120/120 | **120/120**, 0 verkehrt, symmetrische Fälle 21/21 bzw. 28/28 als „gleich“ erkannt | vorzeichenbehaftete Blocksumme |
  | v3 Gegenprobe „gleiche Farbe“ (Saat 31, 32; jeder Kanal auf gleiche Stärke normiert) | 98/120, 97/120 – **0 verkehrt** (Rest = Mischfälle) | 64/120 – 34/35 verkehrt | naive Regel „lauter = Ursache“ fällt auf Zufall (46/100, 55/97) |
- Deutung:
  1. **Auslöser-Eingang** ist auch bei gleicher sichtbarer Stärke bestimmbar (über den Anteil nicht vorhersagbarer Neu-Anregung je Gruppe) und wird nie verkehrt herum zugeordnet.
  2. **Umlaufsinn der Schleife** ist nur mit geeichten Amplituden bestimmbar. Nach Normierung ist er grundsätzlich nicht eindeutig (Grenze der Mathematik: Skalierung D ändert das Verhältnis g68/g86 um (σ6/σ8)², das Schleifenprodukt g68·g86 bleibt gleich).
  3. Ohne Eichung: nur Eingang bestimmen, Umlaufsinn als „unbestimmt“ melden – nicht raten.
- Status: geprüft im linearen, rauschbehafteten Modell. Nichtlineare Schleifen, kurze Messreihen, versteckte dritte Quelle: offen (K52).
- Skripte: schleife_6_8.py a47b907a…, _v2 657177bd…, _v3 49a03a82…; Ergebnisse erg27/28, v2_erg29/30, v3_erg31/32.

## K52-Vorschlag „Richtungsbit als Lehrersignal – kognitive Empathie“ (Antigravity, 07.11.2026) – Prüfung
- Antigravity hat den EEG-Prototyp selbst als per Konstruktion markiert (Nachtrag 18:15) – Korrektur angenommen, geklärt.
- Vorschlag: Text-Messgrößen M1 Kontextbindung, M2 zeitliche Reihenfolge, M3 Persistenz; Richtungsbit + − / − + / Flip / unsicher; Lernschleife mit vorab per sha256 festgeschriebener Einschätzung; ≥ 40 erfundene Fälle, Autor nicht Antigravity; Gegenprobe Raten; EEG später optional.
- Passt zu eigenen Tests: M1 ≈ Auslöser-Eingang (Schleifentest 120/120), M2 ≈ zeitliche Reihenfolge (Granger), M3 ≈ Nachschwingen nach Abschalten (Hüllentest). Schleifentest zeigt: Eingang bestimmbar, Umlaufsinn nur mit Eichung ⇒ Bit sollte Eingang und Persistenz getrennt melden.
- Schwachstellen: (1) Wahrheit der Fälle kommt vom Autor ⇒ Test misst, ob Text die Absicht des Autors trägt (Zirkel); Abhilfe: Etikett durch ≥ 2 unabhängige Bewerter, Übereinstimmung (Cohens κ) angeben, Autoren ohne M1–M3-Vokabular schreiben lassen. (2) Gleiche Modellfamilie schreibt und klassifiziert ⇒ gemeinsame Verzerrung; Abhilfe: Hälfte der Fälle von Thomas, Kreuztest. (3) „Kognitive Empathie“ zu groß ⇒ besser „Perspektiv-Trefferquote“. (4) „Falsche Richtung verstärkt“ bleibt Hypothese Thomas, nicht Ergebnis.

## Sonde („Sweep-Bot“): Schleife messbar machen ohne Eingriff (07.11.2026)
- Thomas: Feedback-Loop finden und eingrenzen – nicht verändern, nicht invasiv, nur messbar machen; Wiederholung als binäre Reaktion der analogen Abstraktion.
- Bekannt: aktive Systemidentifikation (bekanntes Testsignal einspeisen, Antwort messen); in der Angstforschung Generalisierungsgradient (Reize mit abgestufter Ähnlichkeit zum Auslöser; Lissek u. a.); Schreckreflex/Hautleitwert als binäre bzw. Schwellen-Reaktion; bei PTBS Bildgebung mit Erinnerungsskripten. Ethik: Wiederauslösen von Trauma nur klinisch mit Einwilligung – im Projekt nur Simulation und öffentliche Daten.
- Geprüft (Claude, `schleife/schleife_6_8_v4_sonde.py` ae5d6e51…): kleine bekannte Sonde in alle 14 Knoten, Daten danach auf „gleiche Farbe“ normiert. Umlaufsinn **120/120 (Saat 33, 34), 0 verkehrt**, symmetrische Fälle 27/27, 28/28 erkannt – die Sonde liefert die fehlende Eichung. Eingang 94/120, 86/120, nie verkehrt (Sonde verdünnt den Unterschied; Verbesserung: Sondenanteil vorher abziehen).
- Folgerung: Mit Sonde sind Eingang **und** Umlaufsinn bestimmbar, ohne das System zu verändern (Sonde klein, bekannt, abschaltbar).

## Zwei Urknalle; Hyperraum durch Spiegelung; Orientierung +−/−+ (07.11.2026)
- Thomas: Raum-Urknall (einmal, Bühne) getrennt vom Informations-Urknall (wiederholt, Rückprojektion, neue Fraktalebenen). Hyperraum: Würfel in alle Nachbarrichtungen spiegeln (N, S, O, W und NO, SO, SW, NW), wieder zu einem Würfel verdichten; in 6 Ansichten zeigen, wo +− und −+ liegt; 8 Achtelkugeln mit je eigenem Koordinatenkreuz = 8 Würfel = eine Kugel; innen verdichtet, außen gefaltet; je 1/9 innen und außen frei (Deutung offen).
- Bekannt: ewige Inflation (wiederkehrende Blasen), konforme zyklische Kosmologie (Penrose: Ende wird umskaliert zum nächsten Anfang – unbestätigt); Spiegelladungsmethode (Spiegelbilder setzen Randbedingungen); Tesserakt hat 8 Würfelzellen, 24 Quadrate, 32 Kanten, 16 Ecken.
- Geprüft (Claude, `hyper/spiegel_und_zuendung.py` 250a8d0d…, Ergebnis f57fb13c…): Bild an Position v ∈ {−1,0,1}ⁿ entsteht aus k Spiegelungen, Orientierung (−1)^k.
  | Raum | Zellen | k = 0/1/2/3/4 | Orientierung gleich | umgekehrt |
  |---|---|---|---|---|
  | 2D | 9 | 1/4/4 | 5 (Mitte + 4 Diagonalen) | 4 (N, S, O, W) |
  | 3D | 27 | 1/6/12/8 | **13** (Mitte + 12 Kanten) | **14** (6 Flächen + 8 Ecken) |
  | 4D | 81 = 9² | 1/8/24/32/16 | 41 | 40 |
  ⇒ Die 6 Flächen und 8 Ecken sind genau die umgekehrt orientierten Bilder (−+); Mitte und 12 Kanten behalten die Orientierung (+−). Das ist die Paritätsteilung 13 + 14 aus Zustand 0. 4D-Zählung = Tesserakt (8 Würfelzellen bei k = 1).
- Informations-Urknall (Modell: feste Kapazität θ je Zelle, Zündung = Teilung in b³, Rückprojektion dünner Geschwister, Abfluss λ = 0,002): Bilanz exakt (Fehler ≤ 10⁻¹⁰). Mit Abfluss stellt sich ein fester Zustand ein (Zellzahl konstant); ohne Abfluss wächst sie weiter (Gegenprobe); θ zu groß ⇒ keine Zündung; θ klein bei b = 2 ⇒ Überlauf bis zur tiefsten Ebene. 3er-Teilung braucht weniger Zündungen als 2er (θ = 20: 11 gegen 33). Status: weitgehend per Konstruktion; nichttrivial nur der stationäre Zustand mit Abfluss (= „außen falten“ hält das Innen begrenzt).

## Hyper-RAUM27: Räume über die 6 + 8 Punkte verbinden und gegeneinander verschieben (07.11.2026)
- Thomas: nicht linear durch den Raum bewegen, sondern Räume über ihre 6 Flächen- und 8 Eckpunkte (Mittelpunkte) verbinden und 6 × 8 Räume gegeneinander verschieben; acht Hyperraum-Zustandsebenen; verbunden über Beobachter und Expansion auf dem Einheitskreis.
- Bekannt: Zwei um eine halbe Raumdiagonale verschobene Würfelgitter = raumzentriertes Gitter (bcc, z. B. Eisen); dessen Nachbarn sind genau 8 Ecken + 6 Flächen, Zelle = Oktaederstumpf (14 Flächen: 6 Quadrate, 8 Sechsecke), füllt den Raum lückenlos. Lattice-Boltzmann-Modell D3Q15 nutzt genau Ruhe + 6 + 8 mit Gewichten 2/9, 1/9, 1/72. 8 × 6 = 48 = Symmetriezahl des Würfels. 4D: Tesserakt hat 8 Würfelzellen; 4D-FCHC (24-Zelle) ist isotrop und liefert projiziert isotrope 3D-Gitter (d'Humières, Lallemand, Frisch 1986). Beobachter + Expansion: Monopol (Expansion) + Dipol (Eigenbewegung), wie Hintergrundstrahlung (Dipol ≈ 370 km/s).
- Geprüft (Claude, `hyper/sechs_acht_gitter.py` 7a1fd4c3…): 6 + 8 mit 1/9 : 1/72 ist **exakt isotrop 4. Ordnung** (M4 = 1/3 = 3·M22 = 3·1/9, c_s² = 1/3) – Neunerbrüche; nur 6 Nachbarn nicht isotrop (M22 = 0). Richtungsspreizung bei |k| = 1 (eigenes Maß): 6 + 8: 0,19 %; nur 6: 2,8 %; 26er 1 : ¼ : 1/16: 0,08 %. ⇒ 6 + 8 braucht 14 statt 26 Nachbarn bei ähnlicher Richtungsgleichheit.
- Offen: Doppler-Test (14 Fühler bewegt durch stehende Welle; Monopol/Dipol-Trennung auf der Einheitskugel); 8 Hyperraum-Ebenen konkret definieren (Tesserakt-Zellen oder 8 verschobene Kopien).

## Gemeinsame Zustandsebene auf den drei Kugelschnitten (07.11.2026)
- Thomas: Hyperebenen = die 8 Spiegelungen des Ursprungsquadrats (N, S, O, W, NO, SO, SW, NW) → nächstes, größeres Quadrat; das in den Schnittflächen der Kugel (zwei Polschnitte + Äquatorschnitt), die die Kugel in 8 Achtelkugeln teilen; gemeinsame Zustandsebene auf diesen Schnittflächen definiert, die 8 Quadranten darüber verbinden.
- Geprüft (Claude): Drei senkrechte Schnittebenen mit je 3×3 Spiegelbildern ergeben zusammen **19 Zellen**: Mitte 1, Flächen 6 (eine Spiegelung, Orientierung umgekehrt), Kanten 12 (zwei Spiegelungen, Orientierung gleich). Die übrigen **8** der 27 (Ecken, drei Spiegelungen, umgekehrt) liegen in keiner Ebene = die 8 Achtelkugeln.
- Bekannt: Das ist das Lattice-Boltzmann-Gitter D3Q19; Gewichte 1/3, 1/18, 1/36 machen es exakt isotrop 4. Ordnung (M4 = 1/3 = 3·M22, c_s² = 1/3) – Neunerbrüche. Zusammen: Ebenen (19) + Achtelkugeln (8) = 27 (D3Q27; Gewichte 8/27, 2/27, 1/54, 1/216 liegen auf der Familie f = 2e + 8c).
- Übersicht der drei Verknüpfungen: Ebenen allein = 19 (Mitte + 6 + 12); Flächen + Ecken = 15 (Mitte + 6 + 8, raumzentriert); alles = 27. Alle drei mit passenden Neunerbrüchen isotrop.

## Gesamtsimulation Stufe 1: Raum, Feld, Materie, Quadranten (07.11.2026, ohne Informationsebene)
Skripte `gesamt/gesamt.py` (a90be12f…, Ergebnis 035b34a5…) und `gesamt/materie.py` (81d2dd6a…, Ergebnis 93c946e9…), Gitter 61³, Zeittakt 0,1.
| Stufe | Ergebnis | Einordnung |
|---|---|---|
| Raum | Zustand 0 neu erzeugt, Hash = Referenz c7905244…; Spiegelklassen 1/6/12/8, Orientierung 13 gleich / 14 umgekehrt; 19 Schnittebenen-Zellen + 8 Achtelkugeln | exakt |
| Feld 6 Nachbarn | Front 0,964/0,970/0,977, Spreizung 1,34 % | gemessen |
| Feld 15 (6 + 8, 1/9 : 1/72) | 0,968/0,969/0,967, **Spreizung 0,135 %** (bester Wert) | gemessen |
| Feld 19 (Ebenen, 1/18 : 1/36) | 0,976/0,963/0,977, Spreizung 1,43 % | gemessen – als Wellen-Laplace nicht besser als 6 |
| Feld 27 (1 : ¼ : 1/16) | 0,976/0,969/0,974, Spreizung 0,72 % | gemessen |
| Energie | Drift 0,15–0,16 % über 20 Zeiteinheiten bei allen | Zeitschritt-Fehler, klein |
| Oktanten-Fluss (Quelle Mitte) | alle 8 gleich (z. B. 0,6150), gleiche Ankunft | per Konstruktion (Symmetrie) – Kontrolle bestanden |
| Quadranten-Erkennung | Quelle in einer Achtelkugel: 4/4 richtig erkannt (größter Hüllenfluss) | gemessen |
| Materie (Phasenblase, ε = 0,2 ≈ ΔV 0,4) | Schwelle R = 5 (R ≤ 4 fällt, R ≥ 5 wächst) **bei allen vier Nachbarschaften gleich** | gemessen; deckt sich mit früherem Spielzeug-Urknall |
- **Fehler bei mir (Claude), geklärt:** erster Materie-Lauf mit ε = 0,4 – oberhalb 2/(3√3) ≈ 0,385 gibt es keine zweite Mulde, also kein falsches Vakuum; alle Läufe „bleibt“. Neu gerechnet mit ε = 0,2.
- Erkenntnis: Die Isotropie-Gewichte der Strömungsgitter (D3Q19) sind für Geschwindigkeitsmomente gemacht, nicht automatisch für den Wellen-Laplace; dort ist **6 + 8 mit 1/9 : 1/72** am richtungsgleichsten, mit nur 14 Nachbarn. Die Materie-Schwelle hängt nicht vom Gitter ab, nur von ΔV.
- Stand: Raum, Feld, Materie und Quadranten-Logik sind konsistent ⇒ Grundlage für die Informationsebene.

## Gesamtsystem Stufe 2: Informationsebene auf dem 6+8-Gitter (07.11.2026)
Regeln vorher festgelegt (`info/info_ebene.py` 17dc3736…): Welle auf 6+8 (1/9 : 1/72), Gitter 81 = 3⁴; Abfluss nur im äußeren Neuntel (Faltungszone); alle 20 Takte ein Energiepuls im Oktanten (+,+,−), Saat 27; Informationszellen in 3er-Stufen (Kante 27/9/3/1), Zündung bei Energie > θ = 0,02 → 27 Unterzellen, Rückprojektion bei Geschwistersumme < θ/4; 2000 Schritte.
| Frage | mit Abfluss | ohne Abfluss (Gegenprobe) |
|---|---|---|
| F1 begrenzt? | ja: Zellzahl pendelt bei 70 000–78 000 (≈ 14 % von 81³) | nein: 528 711 ≈ 99,5 % von 81³ (Überlauf bis zur feinsten Ebene) |
| F2 Feinheit folgt Energie? | ja: Korrelation Zellebene ↔ log Energiedichte 0,69 | nein: 0,02 (alles gleich fein) |
| F3 Oktant der Quelle erkannt? | ja (+,+,−) | ja |
| F4 Bilanz rein = Feld + abgeflossen | Rest 0,06 % (598,6 = 124,3 + 474,7) | Rest 0,08 % |
| F5 reproduzierbar | Wiederholungslauf: Hash 7ee7737d… identisch | – |
- **Fehler bei mir (Claude), geklärt:** erster Lauf mit falscher Energiebuchhaltung (Gradientenanteil halbiert, Abflussleistung verdoppelt) ⇒ Bilanzrest −74 % bzw. +24 %. Nach Korrektur 0,06–0,08 %.
- Deutung: „Innen verdichten, außen falten“ funktioniert als Regel – der Abfluss im äußeren Neuntel hält die Informationsebene begrenzt und lässt die Feinheit der Energie folgen; ohne ihn läuft alles auf die feinste Ebene über und die Struktur geht verloren.
- Weiter an Antigravity: K53 (Gesamtsystem lang, Variationen, Gegenproben).
