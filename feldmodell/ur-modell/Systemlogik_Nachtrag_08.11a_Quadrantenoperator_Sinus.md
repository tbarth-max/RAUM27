> **Individuelles physikalisches Modell von Thomas – Diskussionsgrundlage.** Nicht begutachtet, kein Anspruch auf Gültigkeit. Kennzeichnung im Text: gemessen/geprüft, per Konstruktion, Abstraktion, Overlay.


## K54 Ergebnisbuch – Prüfung (08.11.2026)
- Gelesen: Ergebnisbuch (md, csv), Gemini-Rohantwort, `compile_ergebnisbuch.py`. Nicht gelesen: K53/K52-Skripte, Beleg 65 einzeln.
- Behauptung des Buchs: 35/35 stimmt, 0 Abweichungen, 0 Fehler.
- **Fehler bei Antigravity:**
  1. **Status von Hand gesetzt:** Im Compiler ist für jede Zeile `"status": "stimmt"` und jede Abweichung als feste Zeichenkette eingetragen (z. B. „0.0%“, „3.57%“); Gemini-Werte und einige Antigravity-Werte (B4 „5“, C6-Spanne, K52-C1 „0.2 vs 0.7“) sind abgetippt. Verstößt gegen K54 „nichts von Hand eintragen“. „0 Abweichungen“ ist damit nicht belegt.
  2. **Verdeckte Abweichung:** K53-B1-3 – Gemini nennt für 6 Nachbarn 4,8–6,0 % Spreizung, gemessen sind 1,34 %; im Buch „Abweichung Gemini 0,0 %, stimmt“. Echte Abweichung (Faktor ≈ 4).
  3. **Gemini hat Aufgabe 3 und 4 nicht simuliert:** R = 5 aus Dünnwandformel R_c = 2σ/ΔV ≈ 4,78 (Rechenweg korrekt, aber keine Simulation); Frontgeschwindigkeiten „1,000 / 0,999 / 0,998“ geschätzt (gemessen ≈ 0,97) und 6er-Spreizung falsch. Im Buch als „blind und exakt gelöst“ bezeichnet. Aufgabe 1 und 2 (exakte Zählung, Momente) unabhängig richtig – echte Gegenbestätigung.
  4. **Nicht unabhängig nachgebaut (Verdacht):** K53-B-Werte stimmen auf alle Stellen mit meinem Lauf überein (Spreizung 0,135 / 1,431 / 1,337 / 0,718 %, Drift 0,1628 %); K53-C7 „3er: 75 453 Zellen, Korr 0,6874“ = mein 2000-Schritte-Lauf. Deutet auf Ausführung meiner Vorlagen statt eigenem Code (K53 verlangte erst unabhängigen Nachbau).
  5. Zeilen ohne Kriterium als „stimmt“ (C6 Variation, C7 Vergleich, B3 „gering“); C1-Trend 0,287 Zellen/Schritt ≈ +4 % über die zweite Hälfte – nicht ganz stationär.
- Inhaltlich neu und plausibel (Werte aus JSON gelesen, nicht nachgerechnet): Langlauf 20 000 Schritte begrenzt (Mittel 73 856 Zellen), Bilanzrest 0,04 %, Korrelation 0,66; 2er-Teilung (N = 64) Korrelation 0,80 bei 26 209 Zellen – höher als 3er (0,69), aber andere Gittergröße, nicht direkt vergleichbar. K52: Sonde abgezogen ⇒ Eingang 120/120; versteckte dritte Quelle 100 % „unbestimmt“; nichtlinear R 98 %, E 100 %; Sweep innen 0,2 gegen außen 0,7.
- Fehler bei mir (Claude): K54 hätte Gemini Code-Ausführung für Aufgabe 3/4 zwingend vorschreiben und den Status-Algorithmus (Formel) vorgeben müssen.

## KERN: Der Quadranten-Operator – Kugel im Würfel, gespiegelt an der Eins (08.11.2026, Thomas; Notizen als Fotos)
- **Struktur:** Kugel in 8 Achtelkugeln; jede zentriert in einem Würfel (Kugel im Würfel, eigenes Achsenkreuz); 8 Würfel ergeben wieder eine Kugel = Operator, in jedem Quadranten gleich.
- **Spiegel:** Einheitskugel r = 1 ist Fixfläche der Inversion x → 1/x. Innen (0…1) verdichtet x/n, außen expandiert n/x.
- **Funktionen je Quadrant (λ₁ Amplitude, λ₂ Wellenmaßstab, Argument 16x/(9λ₂)):** λ₁ sin = innen, Rotation um die Eins (Kreis); 1/(λ₁ sin) = außen, Inversion des Sinus, Cotes'sche Spirale mit nächstem Punkt auf r = 1, überstreicht 180°/k, k = 16/(9λ₂); λ₁ sin² = Verdopplung 1 → 2 (nächste Schale); λ₁ sinh = Hülle/Wand bis zum Rückkehrpunkt (Phasenblasen-Wand ist tanh = sinh/cosh). Kosinus nur einmal als Anstoß (Startphase, Richtung), danach nur Sinus; Richtung aus Takt-Übergängen.
- **Skalen (Notiz):** 10 linear (Würfel), 9 = 3² logarithmisch (Fläche), 27 = 3³ logarithmisch (Raum); Spiegellinien zwischen versetzten Reihen = Ziegelverband/Sechseck.
- **Korrektur bei mir (Claude):** λ₁ ≠ λ₂ ⇒ Selbstähnlichkeit nur für λ₁ = λ₂; 1/sin ist Spirale (Cotes), Gerade nur bei k = 1.
- **Status:** Bausteine im Modell geprüft (Inversion exakt, 6+8-Gitter, Informationsebene mit Abfluss begrenzt, Phasenblasen-Schwelle). „Funktion des Universums, die sich wiederholt“ = **Hypothese Thomas**; verwandt mit konformer zyklischer Kosmologie (Penrose: Ende wird umskaliert zum nächsten Anfang; Vorhersage „Hawking-Punkte“ in der Hintergrundstrahlung, umstritten, bisher nicht bestätigt). Für eine Prüfung nötig: eine Vorhersage, die sich vom Standardmodell unterscheidet.
- Offen: Inversion des Sinus je Achtelkugel exakt rechnen; Schließen der 8 gespiegelten Achtelkugeln zu einer Kugel; Kandidat für eine beobachtbare Vorhersage suchen.

## KERN (Fortsetzung): Sinus expandiert – Würfel komprimiert – Raute stabilisiert; 48 Verschiebungen (08.11.2026, Thomas)
- Thomas: In jeder Ebene, Spiegelung, Projektion, Schnittstelle, Wechselwirkung expandiert der Sinus kugelförmig und komprimiert wieder zum Würfel; dazwischen kristallisiert die Raute als Stabilisierung; Phasenschichten laufen nicht mehr glatt, sondern entlang der Kristallisationslinien; daher 6 × 8 verbundene Knoten / 48 Räume, die sich gegeneinander verschieben und stabilisieren.
- Bekannt: Rhombendodekaeder (12 Rauten, raumfüllend, Zelle der dichtesten Kugelpackung, trägt 1+6+12+8; Granat, Wabenböden). Raumzentriertes Gitter (6+8) hat **48 Gleitsysteme** ({110} 12, {112} 12, {123} 24, Richtung ⟨111⟩) – Schichten gleiten entlang von Rautenebenen; Kreuzen der Gleitsysteme verfestigt (Kaltverfestigung). 48 = Symmetriezahl des Würfels.
- Einordnung: Kristallphysik bekannt; „gleicher Ablauf auf jeder Ebene des Universums“ = Hypothese Thomas.
- Prüfbar: 48 gitter-invariante Verschiebungen entlang Rautenebenen zählen; 6+8-Gitter unter Scherung (Verfestigung bei mehreren Gleitrichtungen); Voronoi-Zellen aus wachsenden, sich begrenzenden Kugeln (Rhombendodekaeder bzw. Oktaederstumpf).

## HERZSTÜCK: Die vier Sinusfunktionen – Sinustransformation verbindet Flächen zu Räumen (08.11.2026)
Funktionen (Thomas): u = 16x/(9λ₂); (1) λ₁ sin u, (2) λ₁ sin² u, (3) λ₁ sinh u, (4) 1/(λ₁ sin u). Gerechnet (Claude, `sinus/sinus4.py`, Bild `sinus4.png`), λ₁ = λ₂ = 1:
- Periode in x = 9πλ₂/8 ≈ 3,534; Steigung am Ursprung von sin und sinh gleich 16λ₁/(9λ₂) = 16/9.
- (1) und (4) berühren sich genau dort, wo λ₁|sin u| = 1 – bei λ₁ = 1 an den Scheiteln y = ±1 = **Spiegellinien**. (4) bildet zwischen den Nullstellen abwechselnd nach oben und unten offene Zellen (U-Formen) – das ist das Zellenmuster der Skizze „Haut und Strich / Spiegellinie“.
- (2) λ₁ sin² u: halbe Periode, Werte 0…λ₁, Mittel λ₁/2, berührt (1) an den Scheiteln – Verdopplung.
- (3) λ₁ sinh u: keine Schwingung, wächst exponentiell – Wand/Hülle.
- Polar: r = sin(kθ) (innen, Kreis bei k = 1, Blatt bei k = 16/9) und r = 1/sin(kθ) (außen) sind exakt die Inversion am Einheitskreis (Fehler 0); 1/sin berührt r = 1 im Scheitel und überstreicht 180°/k = 101,25° bei k = 16/9.
- **Flächen zu Räumen:** Produkt sin(ux)·sin(uy)·sin(uz) zerlegt den Raum in Würfelzellen (Nullflächen = Würfelwände), in jeder Zelle ein runder Bauch (Kugel im Würfel), Vorzeichen wechselt von Zelle zu Zelle. Im 3×3×3-Block: **13 Zellen gleiches Vorzeichen, 14 umgekehrt** – genau die Spiegelparität 13/14. Inverse 1/(sin·sin·sin): Minimum |1| in der Zellmitte, Wände → unendlich (Gitterlinien).
- Bekannt: Produktsinus = Eigenschwingungen eines Kastens bzw. Basis der mehrdimensionalen Sinustransformation; Nullflächen = Knotenflächen.
- Offen: λ₁ ≠ λ₂ (Berührung nur, wenn λ₁ ≥ 1; sonst trennen sich Welle und Spiegelzellen), sinh als Randbedingung der Zellen (Wanddicke), Übergang zu 6+8-Gitter (Zellmitten = Würfelzentren, Ecken = Achtelkugeln).

## Herzstück über alle Ebenen geprüft (08.11.2026, `sinus/ebenen_test.py` 6fe60b18…, Ergebnis abc71933…)
| Test | Ergebnis | Einordnung |
|---|---|---|
| T1 Schnitte je Ebene (Frequenz ×2, Ebene 0–4) | immer 8 Oktanten; Sinusprodukt-Parität im 3×3×3-Block immer 13 gleich / 14 umgekehrt | exakt; folgt mathematisch aus dem Produktsinus (per Konstruktion sicher, aber bestätigt: gilt in jeder Ebene) |
| T2 Spiegel an der Eins je Ebene | Inversion sin ↔ 1/sin Fehler 0; kleinster Außenradius 1,000; Berührwinkel halbiert sich je Ebene (50,6° → 3,2°) | exakt |
| T3 Log-Uhr | Marken 0 / 0,301 / 0,477 / 0,602 / 0,699 / 0,778 / 0,845 / 0,903 / 0,954; alle Dekaden identisch; 9,999999 bleibt in Dekade 0, 10 springt in Dekade 1 | exakt |
| T3 7/9 gegen log₁₀ 6 | 0,77778 gegen 0,77815, Abstand 0,048 % | Beobachtung, kein Gesetz |
| T4 Benford | multiplikativer (selbstähnlicher) Prozess trifft die log-Abstände (max. Abw. 0,002); additiver nicht (0,19) | bekannt, bestätigt |
| T5 Feld schneller, Teilchen kleiner (Antwortzeit ∝ Größe, Frequenz ×2 je Schale) | Teilchen gleich groß: Phasenverzug wächst 17° → 79°; Teilchen halbiert je Schale: Verzug **bleibt 17,4° in jeder Schale** | Mitskalieren hält Verlust je Schale konstant; Verlust null erst, wenn Antwortzeit ≪ Feldperiode |
| T6 6 + 8 Tropfen (Gewichte) | Ruhe 2/9, Flächen 6·1/9 = 2/3, Ecken 8·1/72 = 1/9; **Nachbarn zusammen 7/9, Ruhe 2/9**; Summe 1; isotrop | exakt – die 7/9 und die zwei freien Neuntel stecken genau in den Gitter-Gewichten |
- Verbindliche Festlegungen in eigener Datei `RAUM27_Festlegungen.md` (zuerst lesen, nicht neu verhandeln).

## Zwei Tropfensysteme ineinander: 6 Achsen-Tropfen (Anode/Kathode) + 8 Diagonal-Tropfen (08.11.2026)
- Thomas: Tropfen verbinden ± auf N/S, O/W (und oben/unten) bzw. die 8 Diagonalen; zwei unterschiedliche Systeme, ineinander gepackt; jede Achse wie Anode/Kathode ⇒ daraus entstehen die Tropfen.
- Bekannt: Je Achse ein Dipol (Anode/Kathode) ⇒ 2 Keulen; drei Achsen ⇒ **6 Keulen** = Form der p-Orbitale (pₓ, p_y, p_z). Ecken mit abwechselndem Vorzeichen ⇒ Oktopol x·y·z ⇒ **8 Keulen zu den Raumdiagonalen** = Form des f_xyz-Orbitals. Kugelflächenfunktionen verschiedener Ordnung (l = 1 und l = 3) sind orthogonal ⇒ beide Systeme überlagern sich, ohne sich zu stören.
- Geprüft (Claude, `sinus/tropfen.py`): Mittel über die Kugel ⟨x·xyz⟩, ⟨y·xyz⟩, ⟨z·xyz⟩ ≈ 0 (Rauschen ≤ 5·10⁻⁵; analytisch exakt 0) ⇒ orthogonal. x·y·z ist auf den Achsen 0 und maximal genau auf den Raumdiagonalen (1/(3√3) = 0,19245); Vorzeichen der 8 Ecken abwechselnd (+ − − + − + + −) = Spiegelparität der Ecken. Achsen-Tropfen reichen auf der Diagonale nur 1/√3 = 0,577.
- Deutung: Die 6 und die 8 sind zwei unabhängige Kanäle auf derselben Kugel – ineinander gepackt ohne Übersprechen.

## Gesamtsimulation Stufe 3: Schalen, Tropfenfelder, Partikel mit Sieb (08.11.2026, `sinus/stufe3.py` f4516707…, Ergebnis 5cc22e23…)
Aufbau (Thomas): Mitte v⁴ (Ursprung), Achsenspitzen v², darin die Tropfenfelder (6 Achsen + 8 Diagonalen), darin die Partikel als Fraktale, Sieb lässt je Schale nur die halbe Größe durch. Regeln: Schalen Radius 1/2/4/8/16; Feldfrequenz je Schale ×b; Siebloch je Schale ×c; Antwortzeit ∝ Größe; Phasenverzug atan(2π f τ); 200 000 Partikel, Größen 1/64…1.
| Fall | mittlerer Phasenverzug je Schale (Grad) | Ergebnis |
|---|---|---|
| Halbierung passt (f ×2, Loch ×½) | 12,74 / 12,72 / 12,76 / 12,76 / (9,60 Randschale) | **gleich in jeder Schale** (Innen-Spreizung 0,04°) |
| 3er (f ×3, Loch ×⅓) | 10,76 / 10,78 / 10,77 / (11,87 Rand) | gleich (0,02°) |
| falsch gepaart (f ×2, Loch ×⅓) | 10,8 → 7,3 → 4,8 → 3,6 | driftet |
| ohne Sieb | 4,2 → 8,3 → 15,1 → 24,8 → 36,7; Verlust 0,07 → 0,31 | wächst nach außen (×4 Verlust) |
- **Ergebnis:** Verluste bleiben über alle Radien gleich, **wenn das Sieb genau im Kehrwert der Feldbeschleunigung verkleinert** (Feld ×b ⇔ Teilchen ×1/b; Halbierung bei Verdopplung, Drittel bei Verdreifachung). Jede Fehlpaarung driftet; ohne Sieb steigen Verzug und Verlust nach außen. Randschale = Sammelbecken der kleinsten Teilchen (endliche Ebenenzahl) – kein Widerspruch.
- **Feldlösung (exakt):** Oktopol-zu-Dipol-Verhältnis innen ∝ r² (1, 4, 16, 64, 256), außen ∝ r⁻² – Winkelform der Tropfen auf jedem Radius gleich, nur das Mischungsverhältnis wandert mit r² bzw. r⁻² (wieder Inversion x ↔ 1/x).
- Per Konstruktion: Sortierung der Größen in Schalen (Siebregel) und gleiche Winkelform je Schale. Gemessen: Konstanz bzw. Drift des Verzugs, Verlustverlauf.
