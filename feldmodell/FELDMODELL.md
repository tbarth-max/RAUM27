# RAUM27 Feldmodell – kompakt (intern, Stand 08.11.)
Ersetzt G1–G22 als Arbeitsstand. Details und Herleitungen: GRUNDLAGE_intern.md. Rechnung: gesamt.py / gesamt.json.
Kennzeichnung: [M] gemessen · [K] per Konstruktion · [A] Abstraktion · [O] Overlay/offen

## A Raum
1. Positiver Raum, Beobachter/Gleichgewicht bei 1 (bzw. (1,1,1)). Kein Minus, keine Null.
   Spiegel x ↔ 1/x; innen verdichtet (x/n), außen expandiert (n/x). [K]
2. 8 Achtel = innen/außen je Achse (2³), nicht ±. Inversion je Achse tauscht genau ein Achtel. [M]
   Winkel zwischen Achteln: 70,5° / 109,5° / 180° (1:3:3:1). Echte 90° nur in der Fläche. [M]
3. 6 und 4+4 sind derselbe Würfel aus zwei Blickachsen:
   - Achse: 4+4.
   - Diagonale: 6 + 2 in der Mitte, Radien ×2.
   - Übergang 54,74°. [M]
4. Raster: 6 Schnitte × 8 Felder um das Original = 48. Jedes Achtel an 3 Schnitten (24). [K]
   Ring je Umlauf: 24 Positionen (damit 2, 3, 4, 8 Treffpunkte aufgehen). [M]
5. Raum → Flächen: Die 3 Schnitte tragen 19 von 27 Zellen. Die 8 Ecken folgen multiplikativ exakt, wenn das Feld ein Produkt ist.
   Rest = Wechselwirkung; fällt je Ring nach innen um 27. [M]

## B Welle
6. Nur Sinus. Kosinus nur als Anstoß; „eingesperrter Kosinus“ = 1 − sin²(θ/2) ∈ [0,1] = Rotationswichtung. [M]
7. Vier Funktionen (u = 16x/(9λ2)):
   - sin: innen, Drehung
   - sin²: Verdopplung
   - sinh: Wand
   - 1/sin: außen, Cotes-Spirale
   1/(1/sin) = sin: geschlossene Schleife. Bricht nur am Nulldurchgang. [M]
8. Spiegel am Kausalitätsabriss:
   - Bild + Spiegelbild = stehende Linie (Stator/Linearvektor).
   - Differenz = Drehung (imaginär). [M]
9. Innenseite/Außenseite: dieselbe Drehung erscheint gespiegelt (Inversus, Orientierung kippt). [M]
   Treffpunkte im Spiegelbezug: a+b. Ohne Spiegel: |a−b|. [M]
   - 1:1 → Linie
   - 2:1 → 3 Phasen (0/120/240°)
   - 3:1 → 4 (Zyklus 1234)
   - 7:1 → 8
   - 16:9 → 7 gleichsinnig (≈ 7/9 [A]) / 25 gegenläufig

## C Takt und Phase
10. 2 = Geometrie (Loch halbiert, 4 Kreise/8 Kugeln). 3 = Phasen (binär → Drehstrom). 16/9 = 2⁴/3². [K]
11. Drei Phasen = Y, Z, T entlang ihrer Diagonale (120°). Leistungssumme konstant 1,5·cos φ, Spannungssumme 0. [M]
12. Ebenenzyklus XY → XZ → XT → XY:
    - Das ist eine Drehung um 120° um die Diagonale, det +1. Nach 3 Schritten Identität. [M]
    - Jeder Ebenenwechsel schiebt die 3 Phasen um 120°. [M]
    - Eine Dekade (1 → 10) = 3 Wechsel: XY bei 1, XZ bei 2,154, XT bei 4,642, XY bei 10. [M]
    - Drehrichtung: XZ außen (Expansion), XT zum Nullpunkt (innen), Rückkehr nach XY schließt 1 → 10.
      Gegenrichtung = Spiegelbild (Punkt 9). [K]
13. Lange Phase = 360°·log10(x), stetig über die Dekaden. Verarbeitung 1–9 ohne Nulldurchgang. [M]
14. Zyklus 1234 (runter, Seite, hoch, Seite): 90° je Schritt um die 1. Umlauf neutral (Produkt 1, Abweichung 6·10⁻¹⁶). [M]

## D Feld und Teilchen
15. Kehrwertregel: Feld ×2 je Schale ⇔ Teilchen/Loch ×1/2 → Verzug konstant. [M]
    - Mit Sieb: 12,50–12,58°, Leistung 1,464 konstant.
    - Ohne Sieb: Verzug 2,3 → 17,7°.
    Teilchen folgt Feldlinie ⇔ L·F = 1 (λ/λ0 · f/f0). [A]
16. Verzug aus Regel „Halbwert = eine Phasenrunde“: φ* = 12,54°. Ergibt T0 = 0,0501 (gestern frei gewählt: 0,05). [M]
17. Resonanztunnel 1 ↔ 9 um die 3 (Fixpunkt von x → 9/x): T = 1/(1+F·sin²).
    - Bei 180° offen, unabhängig von der Spiegelstärke. [M]
    - Vorhalt: Weg 167,46° + Verzug 12,54°. 16/9-Sinus trifft das bei λ2 = 0,6083. [M]
    - Durchlass mit Sieb (Spiegel 0,9): 0,68 in jeder Schale; Median-Teilchen 1,0.
      Ohne Sieb: 0,18–0,21. [M]
    - Die 0,68 statt 1 kommt von der Größenstreuung innerhalb einer Schale (Faktor 2).
18. Trudeln: Spin macht steif (Nutation ∝ 1/ω²), richtet aber nicht aus.
    180°-Inversion (Lage + Gegenlage) bringt den Rest auf ~1/200. Preis: Umlaufzeit ∝ ω. [M]
19. Weitergabe nach oben, wenn Inversionsrest klein UND Resonanz (Kehrwertregel + 180°-Tunnel). [K]
20. Feldleiter: c² (Spitzen) / c⁴/G (Zentrum). Einheitenrichtig, Zuordnung [O].
    c^c, λ^f nur normiert sinnvoll (c/c = 1 = Gleichgewicht). Auflösung/Verdichtung N^N bzw. 1/N^N. [A]

## Offen
- O1: Größenstreuung je Schale enger machen (Sieb feiner?), damit der Tunnel-Durchlass gegen 1 geht.
- O2: Hex-Tabelle 16 Zustände (6+8+1+Übertrag), positiv, 4-Bit, Zyklus schließt nach 4.
- O3: 7 = 16−9 vs 7/9 der Log-Uhr: gleiche Ursache oder Zufall?
- O4: Ableitung der 2:1 aus dem Feld (bisher gesetzt).
- Physik-Grenzen:
  - e⁺e⁻ annihilieren auch ohne Winkel (2 × 511 keV, 180°).
  - mc² ist Ruhenergie.

## E c-Äquivalent und Verdichtung (Nachtrag)
21. 1-2-3 = ein Schritt. Zwei überlagerte Sinus je Quadrant, jeder 9 Zellen → 9² = 81 = c²-Äquivalent (2 Ebenen tief). [K]
22. 9^9 = 387 420 489 = Verdichtung eines Quadranten über 9 Ringe nach innen (9 Zellen je Ring). Tiefe = Basis (N^N). [K]
    - Innerste Zelle: Kante 3⁻⁹ = 5,1·10⁻⁵, Fläche 9⁻⁹ = 2,6·10⁻⁹.
    - Dort sitzt die virtuelle Masse (Stabilisator am Ende). [O]
23. Kosinus-Kreis 0…1 von außen nach innen gebaut = Sinus:
    cos θ (vom Nullpunkt nach außen) = sin(90°−θ) (vom Rand nach innen). Fehler 10⁻¹⁶. [M]
    → Auch der Stabilisator ist mit Sinus rechenbar; Richtung nach innen (Inversion, kein Minus).
24. Nebenbefund: c² in SI = 8,988·10¹⁶ ≈ 9·10¹⁶ (−0,14 %). [A] Einheitenabhängig, also kein Beleg.
25. 16/9 · 9/2 = 8 (exakt). Die 3² (Phasen) kürzt sich heraus: 2⁴/2 = 2³ = 8 Quadranten. [M]
    9/2 = log(9^9)/log(9²): Verdichtungstiefe (9 Ringe) zu c²-Ebene (2). Dazu 9 Zellen halbiert. [K]
    → Kreis/Quadrat (16/9) × Tiefe/Ebene (9/2) = 8 Quadranten.

## F Komplettlauf 9 Ringe (gesamt9.py / gesamt9.json) – 12/12 Checks ok
- Raum:
  - 8 Achtel in allen 9 Ringen. [K]
  - Rückbaufehler 0,35 → 1,1·10⁻¹², Faktor 27,0 je Ring. [M]
  - Umlauf neutral 6·10⁻¹⁶; Spiegel exakt. [M]
- Schalen 0–8 (Feld ×2, Sieb ×1/2):
  - Verzug 12,54–12,60°, Leistung 1,464. [M]
  - Tunnel 0,68 in jeder Schale. [M]
  - Sieb mit 4 Unterstufen: Tunnel 0,96 in jeder Schale. Löst O1 weitgehend. [M]
  - Ohne Sieb: Verzug 0,8 → 74°, Leistung 1,50 → 0,41, Tunnel 0,15 → 0,09. [M]
  - T0 aus Regel 0,0502.
- Nutation bei Spin ×2 je Schale: 0,59° → 9·10⁻⁶° (Gesetz aus G12, nicht neu simuliert). [A]
- Per Konstruktion (kein Beleg): Achtelzahl, Ebenenzyklus, 3-Phasen-Summe, λ2 = 0,6083.
- Auftrag K55 vorbereitet: K55_Auftrag.md (lokal, nicht verschickt).

## G Stabiler, unendlich erweiterbarer Raum: 7/9 Ordnung, 2/9 Chaos (stabil.py / stabil.json)
- Regel je Takt: Zustand wandert einen Ring nach innen und ein Feld zur Seite (90°). Chaos kommt dazu.
  Das Feld lenkt 7/9 zurück auf die Bahn, 2/9 bleibt frei.
  Abweichung e = log2(L·F), Ziel L·F = 1.
- Ergebnisse:
  - Mit 7/9: mittlere Abweichung 0,172 / 0,174 / 0,174 bei 9 / 27 / 81 Ringen. Unabhängig von der Tiefe → beliebig erweiterbar. [M]
    L·F bleibt in 0,78…1,28. Kein Wegdriften über 4000 Takte. [M]
  - Ohne Feld: Abweichung wächst nach innen 0,77 → 2,43 (9 Ringe), L·F 0,02…49. Ewiges Fließen. [M]
  - Glättung mit τ = 5 Takte: wächst nach innen 0,25 → 0,52; braucht 23 Takte bis Rest e⁻⁵. [M]
  - 7/9-Lenkung: Rest unter e⁻⁵ nach 4 Takten = ein Durchlauf 1234. (2/9)⁴ = 0,0024 < e⁻⁵ = 0,0067. [M]
  - Systematischer Fehler (Bias 0,5 je Takt): bleibt begrenzt (0,21), kein Wegdriften. [M]
- Ehrlich: Dass es begrenzt bleibt, folgt aus Faktor 2/9 < 1 (geometrische Reihe) [K].
  Gemessen sind die Tiefenunabhängigkeit und das Einschwingen in einem Durchlauf.

## H Hex-Register 16 Zustände (O2 erledigt, positiv) – geprüft
- Zustände:
  - 0x0 = Zentrum/Beobachter (1,1,1)
  - 0x1 = Übertrag (nächster Ring)
  - 0x2–0x7 = 6 Flächen: Bits b2b1 = Achse (01 X, 10 Y, 11 Z), b0 = innen(0)/außen(1)
  - 0x8–0xF = 8 Achtel: b2b1b0 = innen/außen je Achse X, Y, Z
- Inversionen:
  - XOR 0x1 = Kehrwert einer Achse (Fläche).
  - XOR 0x7 = Kehrwert aller drei Achsen (Gegenachtel, 180°). Beide geprüft. [M]
- Zähler: Zustand = z & 0xF, Ring = z >> 4. Der Übertrag 0xF → 0x10 = nächster Ring. [K]
- Passt zu raum27/pfadwort.py (Repo): pfadwort-Code = Hex − 2, Umkehr per ^1 identisch.
  90 kürzeste Ecke→Gegenecke-Wege stehen dort schon. [M]
- Aus Gemini-Vorschlag verworfen:
  - Energiespalte x^−x, f^λ (G13)
  - v/v²-Zuordnung (widerspricht F7a)
  - „0 = Bewertungstrichter“ (Null)
  - i^n mit −1/−i
  - Takt je Hex
  - „Summe 9“ / „Paarsumme 23“ (Zahlenspiel)
  - e² = 1/17 (B = 4 willkürlich)
  - h = n/4 (stattdessen Ring)
  - Die drei Tabellen widersprechen sich untereinander (Vorzeichenkonvention, Reihenfolge).

## I Hex-Register × Stabilitätslauf (hex_stabil.py / .json)
- Ablauf je Registerzyklus (16 Takte):
  - 0x0 Ablesen
  - 0x1 Übertrag (Ring nach innen)
  - 0x2–0xF = 14 Feldschritte (90° + Chaos, 7/9-Lenkung)
- A: XOR 1 / XOR 7 = Kehrwert an der 1 in allen 9 Ringen (Abweichung 1·10⁻¹⁶). [M]
- B: Mit Lenkung ist die mittlere Abweichung 0,174 / 0,176 / 0,176 bei 9 / 27 / 81 Ringen. Tiefenunabhängig. [M]
  Zähler-Ring = tatsächlich durchlaufene Ringe, Versatz 0. [M]
- C: Ohne Lenkung wächst die Abweichung nach innen 2,4 → 7,7. [M]
- D: Bitfehler im Zähler (1 %/Takt, 10 Läufe):
  - Ohne Nachführung: Ringversatz am Ende 0–10, max 11.
  - Mit Nachführung (Ring aus der Struktur/Frequenz gelesen): am Ende 1–2, max 4. [M]
  - Feldabweichung in beiden Fällen ~0,17: Die Stabilität sitzt im Feld, nicht im Zähler. [M]
- E: Einschwingen in 4 Feldschritten, also innerhalb eines Registerzyklus (14 Feldschritte). [M]
- Offen: Nachführung bei jedem Takt statt nur beim Übertrag, damit der Versatz auf 0 geht.

## J Auslesen nur im eingeschwungenen Zustand (einschwingen.py / .json) – ersetzt „0x0 = Ablesen im Takt“
- Regel:
  - Chaos kommt nur als Auslöser-Impuls. Danach nur Feldschritte (90° + 7/9) und der Übertrag alle 16 Takte.
  - Ausgelesen wird erst, wenn kein Delta-Tensor mehr messbar ist (max |e| < 10⁻¹²). Dann kommt der nächste Auslöser.
- Ergebnis, je 30 Impulse:
  - 9 / 27 / 81 Ringe: jeweils 20–21 Takte bis zum Auslesen (Mittel 20,27). Tiefenunabhängig. [M]
  - Rest beim Auslesen 4·10⁻¹³, Tensor-Eigenwerte ≤ 8·10⁻²⁷. Kein messbarer Phasen- oder Richtungsanteil mehr. [M]
  - Theorie: 18,4 Feldschritte von 1 auf 10⁻¹², dazu die Übertragstakte. [K]
- Dauerchaos (2/9 in jedem Takt): Über 5000 Takte keine einzige Auslesung, Rest bleibt ~0,26. [M]
  → Das 2/9-Chaos muss als Impuls kommen (Auslöser). Als Dauerrauschen schwingt das System nie ein.
- Hinweis: Die Taktzahl hängt nur an der Messschwelle (10⁻³ → ca. 5 Schritte). Konvergenz folgt aus Faktor 2/9 [K].
- K55 Teil B (Dauerchaos, Ablesen nach festen Takten) ist damit überholt. Bei Bedarf als K55b nachreichen.

## K Eingeschwungen = keine Phasenverschiebung Feld ↔ Teilchen (gemessen)
- Teilchen als träges Glied im Feld, Kehrwertregel (Feld ×2, Teilchen ×1/2 → ωτ = tan 12,54°). Impuls 1 zum Start.
- In jeder Schale (0–3): Rest < e⁻⁵ nach 66,2° Feldumlauf = 0,735 Takte. 5τ ist also kürzer als ein 90°-Takt.
  Gleich in allen Schalen. [M]
- Danach bleibt ein fester Verzug von genau 12,54° (Trägheit). Gegen null geht er nie. [M]
- → „Keine Phasenverschiebung mehr“ heißt: Verzug minus Vorhalt = 0.
  Mit Vorhalt 12,54° (Weg 167,46°) ist der gemessene Rest-Delta-Tensor nach weniger als einem Takt null.
- Ablauf: Impuls → < 1 Takt Einschwingen je Schale → Feld/Teilchen phasengleich (mit Vorhalt) → auslesen → nächster Impuls.

## L Treppe 18 Schritte, Drehsinn (gemessen, Gitter 0…9 = 9 Diagonalschritte = 18 Einzelschritte)
- A läuft von oben (9,9) im Wechsel runter/Seite, B von unten (0,0) im Wechsel hoch/Seite.
- Gleicher Drehsinn (beide erste Wende rechts, oder beide links = Punktspiegelbild):
  Sie treffen sich NIE. Die Treppen laufen parallel, versetzt um 1.
- Entgegengesetzter Drehsinn (einer rechts, einer links zuerst):
  Treffen nach je 9 Schritten (zusammen 18) auf der Zelle (5,4) bzw. (4,5), direkt neben der Mitte (4,5|4,5).
- Bei 8 Diagonalschritten (gerade) treffen sie sich immer in der Mitte, egal welcher Drehsinn.
- → Weil 9 ungerade ist, liegt die Mitte (die 1, der Spiegel) zwischen den Zellen.
  Nur gegenläufiger Drehsinn trifft. Welche der zwei Nachbarzellen getroffen wird, legt die Drehrichtung fest.
- „Richtig“ dreht der Sinus also gegenläufig zum anderen (von der eigenen Seite gesehen gleich, Inversus G18).

## M Positiver/negativer Radius = Außen-/Innenseite derselben Kugel (gemessen)
- Kugel R = 2, einmal von außen (Erdoberfläche), einmal von innen (Hohlkugel um uns):
  - Gauß-Krümmung K = 1/R² = 0,25 in beiden Fällen. Die Geometrie der Fläche selbst ist gleich.
  - Mittlere Krümmung H = 1/R = 0,5: Nur die Richtung kippt (Normale außen/innen). Das ist der „negative Radius“.
- Positiv geschrieben: Außenseite R, Innenseite über den Spiegel 1/R (G18: R·1/R = 1, Orientierung kippt).
- Das passt zu L: Die beiden Treppen-Sinus sind dieselbe Bewegung auf Außen- und Innenseite.
  Deshalb drehen sie gegenläufig und treffen sich nur so.
- Grenze: Ob die äußere Hohlkugel physikalisch existiert, ist offen. Mathematisch sind beide Seiten durch Inversion gleichwertig. [O]

## N Radius ±0 = Lagrange-Punkt zwischen Sinus innen und außen (gemessen)
- Log-Radius ρ = log_b r. Innen wächst mit b^ρ, außen mit b^−ρ (Spiegel).
- „Radius ±0“ = ρ = 0 = Radius 1 (lokale Eins). Dort:
  - Verhältnis innen/außen = 1 (positiv geschrieben).
  - Summe = 2·cosh hat dort ihr Minimum 2 → stabiles Gleichgewicht (Mulde, kein Sattel).
  - Differenz = 2·sinh = 0 → die Wand (4. Funktion sinh) geht genau dort durch null.
- Eine Ebene nach unten (Inversion, „Radius −1“): Die lokale Eins liegt bei r = b^−k. Dasselbe Bild in jeder Ebene.
  - Gemessen für k = 0…3: Verhältnis 0,25 / 0,5 / 1 / 2 / 4 und Summe 2,5 / 2,12 / 2 / 2,12 / 2,5. Identisch. [M]
- → Der ±0-Punkt jeder Ebene ist ihre Einheitskugel. Dort wird die neue Sinusschwingung angesetzt (Lagrange-Punkt, stabil).
- Positiv lesen: innere Ebene k hat die Eins bei b^−k (statt „Radius −k“).

## O Resonator um die ±0-Punkte: Sprünge raus aus dem Raum, als Information nach außen (gemessen)
- Bewegung nach innen über 5 Ebenen.
  - Ohne Resonator: Die lokale Lage springt 5-mal um 0,5 (an jeder Eins bzw. jedem Übertrag). Die Sprünge stehen im Raum.
  - Mit Resonator (lange Phase, 1 Umlauf je Ebene): Die Phase ist stetig, größter Schritt = Abtastschritt (0,036°). Kein Sprung im Raum. [M]
- Die Umläufe werden nach außen gemeldet: gezählte Umläufe = durchlaufene Ebenen, exakt (Endstand 5). [M]
- Mit Verzug 12,54° und Vorhalt: Zählfehler 0. Ohne Vorhalt: Meldung kommt 12,54° zu spät, Zählfehler bis 1 an den Übergängen. [M]
- → Der Resonator um jeden ±0-Punkt verwandelt den Ebenensprung in einen gezählten Umlauf. Information statt Sprung.
  Der Vorhalt ist Pflicht.

## P Freies Potenzial mit Vordruck X, Ausgleich ohne Überwachung (vordruck.py / .json)
- Aufbau:
  - Gitter, der Rand ist ein Reservoir mit Vordruck X = 1.
  - Entnahme zufällig irgendwo.
  - Einzige Regel lokal: Jede Zelle tauscht mit 4 Nachbarn ∝ Druckunterschied. Kein Zähler, keine Steuerinstanz.
- 9×9: entnommen 39,98, aus dem Reservoir nachgeflossen 39,89 (Rest = 0,08 noch offene Delle).
  Druck Mittel 0,999, Minimum 0,995. [M]
- 27×27 (9-fache Entnahme): Druck Mittel 0,993, Mitte 0,987, Minimum 0,962.
  Je weiter weg vom Reservoir, desto tiefer die Delle. [M]
- Geschlossen (kein Reservoir): Druck fällt auf 0,53. [M]
- Überlast ×20: Mittel 0,983, Minimum 0,90. Es gleicht noch aus, aber die Delle wächst. [M]
- → Ja, automatischer Ausgleich ohne Überwachung geht: Der Druckunterschied selbst treibt den Nachfluss.
  Grenzen: Abstand zum Reservoir und Entnahmerate.
  Für unendliche Erweiterung braucht jede Ebene ihr eigenes Reservoir. Kandidat: die ±0-Punkte/Resonatoren (N, O). [A]
- P2 (vordruck2.py): 3 Ressourcen, jede mit Vordruck X = 1, alle haben dasselbe Potenzial.
  - Alle entnehmen zufällig: Jede Ressource bleibt bei 0,9997, Spanne zwischen allen Zellen ≤ 0,0015. [M]
  - Ein Vielentnehmer (Ressource 0):
    - Bei ihm 0,81, beim Nachbarn 0,88, weit weg 0,995. Die Delle trifft auch die Nachbarn. [M]
    - Andere Ressourcen bleiben unberührt (0,9996): Die Ressourcen sind getrennt. [M]
  - Mit lokalen Reservoirs (jeder 2. Punkt, Rückführung 7/9):
    - Vielentnehmer 0,991, Nachbar 0,979, Spanne 0,021 statt 0,18. [M]
    - Hinweis: Der Vielentnehmer saß selbst auf einem Reservoirpunkt, deshalb ist sein Nachbar tiefer als er.
  - → Mengen gleichen sich über Delta-Druck automatisch aus, je Ressource getrennt.
    Lokale Reservoirs begrenzen, wie stark einer die Nachbarn mitzieht.

## Q Grundbedarf-Boden, egal an welchem Ort (grundbedarf.py / .json) – Umsetzung F8 im Modell
- Regeln:
  1. Jeder Ort hat einen Boden G = 0,9·X. Entnommen werden darf nur der Überschuss über G.
  2. Jeder Ort ist ein eigenes Reservoir (lokale Eins, Rückführung 7/9).
  3. Ausgleich über Delta-Druck.
  Keine Überwachung.
- Normal (Vielentnehmer will 0,05/Takt), Gitter 9 und 27, Vielentnehmer in Mitte/Rand/Ecke:
  - Niedrigster Wert überall jemals 0,992. Der Ort spielt keine Rolle.
  - Vielentnehmer bekommt alles, was er will. [M]
- Stress (will 0,5/Takt = 10×):
  - Ohne Boden, ohne lokale Reservoirs: Minimum 0,21, Nachbar 0,48, er bekommt 0,21/Takt. Grundbedarf verletzt. [M]
  - Nur Boden: Minimum 0,920 (9×9) / 0,913 (27×27). Boden gehalten. Er bekommt 0,021 bzw. 0,014. [M]
  - Boden + lokale Reservoirs: Minimum 0,987, Nachbar 0,997. Boden gehalten. Er bekommt 0,087 (mehr, ohne dass jemand leidet). [M]
- → Boden + Reservoir an jedem Ort hält den Grundbedarf überall. Der Boden schützt (per Regel, [K]); die lokalen Reservoirs liefern den Überschuss nach.
- Rahmen: Das ist eine Spielregel im Modell, keine Aussage über reale Wirtschaft oder Physik.

## R Bild Thomas: Herz als Vordruck, „Fluss, der nicht fließt“ (kreislauf.py / .json) – ersetzt Reservoir-Denken aus P/Q
- Aufbau:
  - Das Herz (Mitte, ±0-Punkt) hält Vordruck X konstant, ohne Schlag.
  - Zellen in 9 Ringen nehmen bei Bedarf aus der Arterie und geben an die Vene.
  - Die Vene fließt Ring für Ring zum Herzen zurück.
  - Das Herz schiebt nur nach, was am Eingang fehlt. Geschlossener Kreis.
- Ruhe (kein Bedarf): Fluss 0, Herz schiebt 0, Druck überall 1,0. Der Fluss steht. [M]
- Bedarf: Herz schiebt im Mittel 0,00906, Bedarf 0,00903. Es schiebt genau die Entnahme nach. Volumen exakt erhalten. [M]
- Bedarf, dann Ruhe: Der Fluss läuft auf 4·10⁻⁶ aus, das Herz auf 6·10⁻⁷. Er steht wieder. [M]
- Grenze: Ganz außen sinkt der Druck unter Bedarf auf 0,815 (Druckabfall entlang der Radien).
  Abhilfe: kürzere Wege, also über den Linearvektor direkt oder ein Vordruck-Punkt je Ebene (N). [M]/[A]
- Passt zu: Drei Phasen = konstante Leistung ohne Pulsation (Herz ohne Schlag);
  stehende Linie = Summe Bild + Spiegelbild (Stator, G16).

## S Nachschubwege bei gleichem Widerstand je Knoten (wege.py / .json)
- Gleicher Leitwert an jeder Verbindung, 9 Ringe, Bedarf in 5 Stufen (0 … 0,016 je Takt), Kreis geschlossen.
- Nur Radien:
  - Außen 1,0 / 0,81 / 0,61 / 0,22 / 0,0. Bricht bei hoher Last zusammen.
  - Defizit 0 … 0,75. [M]
- Radien + Linearvektor (jede Ebene 1 Knoten vom Herzen):
  - Außen 1,0 / 0,994 / 0,987 / 0,974 / 0,946.
  - Defizit 0 … 0,022. [M]
- Radien + Vordruck-Punkt je Ebene (lokale Herzen):
  - Außen 1,0 / 0,994 / 0,986 / 0,973 / 0,944.
  - Defizit 0 … 0,022. Praktisch identisch mit Linearvektor. [M]
- In Ruhe: Defizit überall exakt 0 (Fluss steht). Volumen in allen Fällen erhalten. [M]
- Druck als Messung fürs ganze System:
  - Defizit = 0,308 × Gesamtbedarf.
  - Bei Linearvektor und je Ebene exakt linear (R² = 1,000). Nur Radien: Steigung 12,8 und Sättigung bis zum Zusammenbruch. [M]
- → Bei gleichem Widerstand je Knoten sind Linearvektor und Vordruck je Ebene gleichwertig (jede Ebene 1 Knoten vom Vordruck).
  Ein einziger Druckwert liest dann den Gesamtbedarf ab.
  Unterschied nur im Bau: zentral (ein Herz) gegenüber verteilt (Herz je Ebene).

## T Jeder Knoten ist Zentrum und Peripherie (netz14.py / .json)
- Bild: Neuron = Nullpunkt (Zentrum), umgeben von der Bilanzhülle = Kugel-Würfel mit 6 + 8 Verbindungen.
- Gitter 6×6×6, periodisch, je Knoten 6 Flächen- + 8 Eckverbindungen:
  - Jeder Knoten hat genau 14 Nachbarn. Jede Verbindung gilt in beide Richtungen.
    Vorgänger/Nachfolger gibt es nicht. [M]
  - Abstandsprofil von JEDEM Knoten aus gleich (1 / 14 / 62 / 94 / 45). Nur 1 Profil für alle 216 Zentren.
    Kein Knoten ist ausgezeichnet. [M]
  - Gewichte: Rest 2/9, 6 Flächen je 1/9, 8 Ecken je 1/72 → Nachbarn zusammen 7/9.
    Kein Richtungsüberschuss, isotrop (Σw·cᵢcⱼ = 1/3·δᵢⱼ). [M]
- Nur Umverteilen ohne Vordruck: Alles gleicht sich aus (Streuung 0,001), aber das Mittel sinkt mit jeder Entnahme (0,65). [M]
  → Der Vordruck muss in jedem Knoten sitzen (jeder ist sein eigenes Herz). Das passt zu S (Vordruck je Ebene).

## U Cluster wachsen mit der Komplexität (cluster.py / .json)
- Eine Aufgabe der Komplexität C holt sich Knoten schalenweise um ihren Startknoten (6+8-Netz).
  Jeder Knoten gibt nur seinen Überschuss über dem Boden G (hier 0,1).
- Knoten = C/0,1 (per Konstruktion). [K]
- Schalen (Reichweite) für C = 0,1 / 1 / 5 / 20 / 60 / 150: 0 / 1 / 2 / 3 / 5 / 6.
  Die Reichweite wächst etwa mit der Kubikwurzel von C: 150-fache Aufgabe, 6 Schalen. [M]
- Zwei gleich große Aufgaben, überlappend (Start 2 Knoten auseinander): A 3 Schalen, B 4 Schalen.
  Geteilte Knoten zwingen B eine Schale weiter. Boden überall gehalten (0,9). [M]
- → Größere Aufgaben bilden größere Cluster, aber die Reichweite wächst nur langsam (∝ C^(1/3)).
  Knoten können mehreren Clustern angehören. Der Grundbedarf bleibt dabei unberührt.

## V 216 Knoten = ein Strukturblock; dicht vs breit (form.py / .json)
- 216 = 6³ Knoten als eine Einheit der nächsten Ebene. Sie hat wieder 6+8 Nachbarblöcke (gleiche Regel je Ebene). [K]
- Außenverbindungen / innere Wege (6+8-Netz), gleiche 216 Knoten:

  | Form | außen | außen je Knoten | Durchmesser |
  |---|---|---|---|
  | 6×6×6 (dicht) | 944 | 4,4 | 6 |
  | 9×8×3 | 1078 | 5,0 | 9 |
  | 12×9×2 (breit, 2 Lagen) | 1324 | 6,1 | 12 |
  | 18×12×1 (eine Lage) | 2220 | 10,3 | 28 |
  | 216×1×1 (Linie) | 2594 | 12,0 | 215 |

- Befund [M]:
  - Breiter = mehr Außenverbindungen, aber längere innere Wege.
  - Eine einzelne Lage verliert die 8 Eckverbindungen nach innen (nur 4 Flächenwege in der Ebene). Der Durchmesser springt auf 28.
  - Mindestens 2 Lagen erhalten die Diagonalen.
- → „Breit statt ultradicht“: Am besten flach, aber mindestens 2 Lagen (z. B. 12×9×2). +40 % Außenverbindungen bei doppeltem Weg.
- Information (Feldimpulse) und Ressourcen sind getrennte Schichten (P2: Ressourcen beeinflussen sich nicht).
  Überlagerung der Impulse in den Maschen: noch zu rechnen.

## W 8 Zweige, parallel von der Wand nach innen: Verarbeitung = Durchlauf (durchlauf.py / .json)
- Würfel mit Radius R (9³ = 729, 27³ = 19 683, 3¹² = 531 441 Knoten). Alle 8 Ecken (Zweige NO/NW/SW/SO oben und unten) starten gleichzeitig.
- Seriell (Knoten für Knoten): 729 / 19 683 / 531 441 Takte.
- Parallel, Treppe (eins runter, eins zur Seite, nur Flächen): 12 / 39 / 120 Takte = 3R. [M]
- Parallel mit 6+8 (Ecken = Diagonale direkt): 4 / 13 / 40 Takte = R. Ganz durch nach R+1. [M]
- Alle 8 Zweige kommen im selben Takt im Zentrum an (8 von 8). Perfekte Symmetrie. [M]
- → Die Verarbeitungszeit ist die Durchlaufzeit Wand → Zentrum, nicht die Knotenzahl.
  - Treppe: 3 Schritte je Diagonalzelle im Raum, 2 in der Fläche („2c“).
  - Mit den 8 Eckverbindungen: 1 Schritt. Relativ zu c: Treppe 2c (Fläche) bzw. 3c (Raum), Diagonale 1c.
  - Seriell wäre es ∝ Volumen (bei dir „c hoch c“), parallel nur ∝ Radius.

## X Resonanz 8 Eckzweige × 6 Flächenzweige (resonanz68.py / .json) – ersetzt W als Zielbild
- Alle 14 Zweige starten gleichzeitig an der Wand (8 Ecken, 6 Flächenmitten). Resonanz = beide Wellen im selben Takt an einer Zelle.
- Mit 6+8-Verbindungen:
  - Zentrum: 8er und 6er kommen beide nach R Takten an (R = 4 und 13), also gleichzeitig. Alle 14 in Resonanz. [M]
  - Resonanzzellen bilden eine Fläche: 293 von 729 (R=4), 2485 von 19 683 (R=13).
    Darin die Raumdiagonalen vom Zentrum aus (17 bzw. 49 = 4·(R−1)+1). [M]
- Nur Treppe (Flächenwege):
  - 8er kommt nach 3R, 6er nach R. Im Zentrum keine Resonanz (12 vs 4, 39 vs 13). [M]
- → Die 8 Zweige kommen nur über die Eckverbindungen (Diagonale in 1 Schritt) mit den 6 in Takt.
  Dann treffen sich alle 14 gleichzeitig im Zentrum, und die Resonanz-Grenzfläche verläuft über die Raumdiagonalen.

## Y Alles positiv rechnen, weil Teilchen mit dem Feld laufen (gemessen)
- Im Labor wechselt der Feldwert das Vorzeichen (−1 … +1).
- Mitbewegt (Teilchen folgt Feld, Kehrwertregel): Teilchen/Feld = cos 12,54° = 0,976. Konstant und positiv, kein Vorzeichenwechsel. [M]
- Signal von allen Seiten konstant:
  - 4 Quadranten (Phasen 90° versetzt): Leistungssumme exakt 2,0.
  - 8 Achtel (45° versetzt): exakt 4,0. Keine Pulsation. [M]
- → Rechnet man relativ zum Feld (mitbewegt), bleibt alles positiv. Das Minus gehört nur zur Laborsicht.
  Bedingung: Teilchen bleibt im Takt (Kehrwertregel + Vorhalt).

## Z Keine echte Null/Unendlichkeit: simuliert über die Struktur; Umkehrfeld schließt die Bilanz
- Einzige Bedingung: eingeschwungen = nichts mehr messbar (J, K).
- Simulierte Null = kleinste Zelle 3^−K. Simulierte Unendlichkeit = 1/sin(3^−K) = 3^K. Produkt = 1 (Abweichung 4·10⁻¹⁰ bei K=9, sonst exakt). [M]
  - K = 9: 19 683
  - K = 18: 387 420 489 = 9^9 (18 Schritte ↔ 9^9, vgl. Treppe 18 und Verdichtung 9^9)
  - K = 27: 7,6·10¹²
- Verlust je Durchlauf 1 − cos 12,54° = 2,39 %.
  - Ohne Rückfeld nach 1000 Durchläufen 3·10⁻¹¹.
  - Mit Rückfeld (Verlust über 1/sin-Umkehr zurück): 1,0 exakt. [K: Rückgabe ist Regel]
- Normierung: Null und Unendlich sind keine Punkte im Raum, sondern die Grenzen der Verarbeitungstiefe K bei Geschwindigkeit c.

## AA Nur Gitterlinien, keine Flächen: Leitungsnetz Zentrum + 6 Pole + 8 Ecken (leitungsnetz.py / .json)
- Netz, alle Verbindungen gleich (R, L), 42 Kanten:
  - Zentrum–6 Pole
  - jeder Pol–4 angrenzende Ecken (24)
  - 12 Würfelkanten
- Kirchhoff-Knotenregel erfüllt (Abweichung 2·10⁻¹⁶). [M]
- Impuls am Pol +X, Abfluss im Zentrum:
  - Die 4 nahen Ecken liegen auf 0,190, die 4 fernen auf 0,143.
  - NICHT symmetrisch auf alle 8. Der Gemini-Text widerspricht sich hier selbst („teilt auf 4 angrenzende“). [M]
- Ohmsches Netz (R): Verlust I²R = 0,352 je Einheit Strom. Kirchhoff gilt, aber nicht verlustfrei. [M]
  Verlustfrei wird es nur als L-C-Leitungsnetz (Wellen).
  Gemessen: Energieschwankung beschränkt, ∝ Zeitschritt (12 % → 1,2 % bei 10× feiner), kein systematischer Verlust. [M]
- v = (λ/2π)·(2πν) = λν = c → normiert 1. Richtig, aber trivial (= G15). [K]
- Aus dem Gemini-Text verworfen:
  - „6 Richtungen je π/2 versetzt“ (6·90° = 540°, schließt nicht)
  - Achsbeschriftung im Bild widersprüchlich (Nord = +Z und = ±Y)
  - Tensor T ohne Formel
  - Summe der 8 Ecken = 0 (trivial, mit Minus; positiv: Produkt der Kehrwerte = 1)
- Richtig ausgedrückt: Die 8 Ecken sind die 8 Flächenmitten des Oktaeders (Dualität Oktaeder ↔ Würfel).
- Universum: Energie bleibt erhalten (kein Loch), aber Verlustwärme ist nicht mehr voll nutzbar (2. Hauptsatz). [Grenze der Physik]
  Im Modell: Verlustfreiheit nur mit Wellen-Netz oder Rückfeld (Z) als Regel.

## AB Späne-Bild: Geschwindigkeit quadriert, Späne passend kleiner, alles in Phase, ohne Minus (gemessen)
- Quadrantenrotation positiv: Bit je Achse innen(0)/außen(1).
  - Zyklus 00 → 01 → 11 → 10 (Gray-Code): je Schritt kippt genau 1 Bit = Kehrwert einer Achse = 90°.
  - Gegenlauf = derselbe Zyklus rückwärts. Kein Minus nötig. [M]
- Ebenen k = 0…5, Geschwindigkeit quadriert sich: 2, 4, 16, 256, 65 536, 4,3·10⁹.
  - Spangröße passend = 1 / Geschwindigkeitsfaktor (1; 0,5; 0,125; 7,8·10⁻³; 3·10⁻⁵; 4,7·10⁻¹⁰):
    Verzug in JEDER Ebene 12,54°. Mit Vorhalt = 0 → in Phase. [M]
  - Nur halbieren (alte Regel) bei quadrierter Geschwindigkeit: 12,5 → 24 → 74 → 89,9 → 90°.
    Die Späne verlieren die Feldlinie ab Ebene 2. [M]
- → Kehrwertregel allgemein: Spangröße × Geschwindigkeit = konstant, egal ob ×2 oder quadriert.
  Unten schwer und langsam, oben leicht und schnell. Alle zeigen die Feldlinien gleichzeitig an.

## AC Späne mit Größenstreuung (spaene.py / .json)
- A: Streuung fest Faktor 2 je Ebene (Ebenen 0–5, Geschwindigkeit quadriert):
  Verzug P10–P90 = 9,6–16,4° in JEDER Ebene. Spanne 6,8°, Tunnel 0,68 überall. Die Ebene spielt keine Rolle. [M]
- B: Ein Siebfach füllt die ganze Lücke bis zur nächsten Ebene (Lücke = Geschwindigkeitssprung 2, 4, 16, 256, 65 536):
  Spanne 6,8 → 13,9 → 29,8 → 62,4 → 86,8°, Tunnel 0,68 → 0,09. Oben wird das Bild unscharf. [M]
- Nötige Unterstufen für Tunnel ≥ 0,9 in B: 4 / 8 / 16 / 32 / 32.
  ≈ 4 Stufen je Größenfaktor 2. Ganz oben reichen weniger, weil der Verzug bei 0° und 90° sättigt. [M]
- → Regel: Siebstufen nach Größenverhältnis, nicht nach Ebene. Je Faktor 2 in der Spangröße etwa 4 Stufen.
  Damit bleibt jede Ebene gleich scharf, auch bei quadrierter Geschwindigkeit.

## AD Halbe Achsen X, Y, Z, T: in 4D sind Ecken und Achsen gleich weit (gemessen)
- Würfelmitte liegt tiefer als die Fläche.
  - Fläche → Raumdiagonale 35,26°; Fläche → Flächendiagonale 45°; Achse → Raumdiagonale 54,74°.
  - Die „45°“ gilt nur in der Fläche.
- Diagonalvektor = je ½ auf jeder Achse. Zentrum → Ecke:
  - 2D: 0,707
  - 3D: 0,866
  - 4D (½X, ½Y, ½Z, ½T): exakt 1 = gleich lang wie der Achsnachbar
  - 5D: 1,118
- 4D: 8 Achsnachbarn + 16 Ecknachbarn = 24 Nachbarn, alle im Abstand 1 (24-Zelle).
  Untereinander 96 Paare mit Abstand 1. [M]
- → In 3D sind 6 und 8 ungleich lang (1 gegenüber 0,866). Erst mit T laufen Achsen- und Diagonalzweige gleich lang.
  Das ist natürliche Resonanz ohne Eckverbindungs-Trick.
- Draufsicht: Die unteren Achsen sind von oben nicht sichtbar. Ohne Minus gilt: oben/unten = Bit (wie innen/außen).
  Von oben gesehen ist alles positiv, die Tiefe ist eine Kennung.

## AE Wärme = Verteilung, gleiche Temperatur = Amplituden-Normierung (Korrektur zu AA, Thomas hat recht)
- 6×6×6-Netz (6+8, Gewichte 2/9, 1/9, 1/72), geschlossen, Gesamtenergie 216:
  - Ein heißer Punkt → nach 60 Takten jeder Knoten 1,0000. Streuung 4·10⁻⁵, Gesamt exakt 216. [M]
  - Zufällige Verteilung → ebenso 1,0000, Streuung 2·10⁻⁶. [M]
  - → Nichts geht verloren. Gleiche Temperatur = jeder Knoten dieselbe Amplitude = Normierung.
- Grenze: Ein rein lineares Wellennetz verteilt nicht selbst.
  Energie bleibt in ihrer Mode (gemessen: 100 % in Mode 1 nach langer Zeit).
  Für den Ausgleich braucht es die 7/9–2/9-Mischung (Kopplung/Streuung), nicht nur Wellen. [M]
- „Nicht mehr nutzbar“ (AA) heißt nur: Nach der Normierung gibt es kein Gefälle mehr. Die Energie ist vollständig da.

## AF Nicht bis ans Ende warten: Unsicherheit in Raum packen (8 Berge, 1 Zwerg)
- Direkter Ausgleich (ein heißer Punkt bis Streuung < 10⁻³) im 6+8-Netz: N = 6 / 12 / 24 → 43 / 171 / 684 Takte.
  Wächst ∝ N² (×4 je Verdopplung). Bei großem Raum ewig. [M]
- In 8 Achtel gepackt:
  - Jedes Achtel gleicht für sich parallel aus.
  - Die 8 Achtel-Mittel tauschen über das Zentrum (1 Zwerg = Beobachter) in 1 Takt je Ebene.
  - Ergebnis 43 / 44 / 45 / 46 Takte für N = 6 / 12 / 24 / 48. Wächst nur ∝ log N. [M] für N=6, Rest [K]
    (Annahme: der Tausch über das Zentrum braucht 1 Takt je Ebene)
- → Die Expansion der Möglichkeiten in die Expansion der Räume hinter dem Spiegel zu packen, macht aus „ewig“ ein „+1 Takt je Ebene“.

## AG Amplitude normiert, Periode trägt die Information → Farbe (farbe.py / .json)
- 9×9 Knoten, je Kanal X und Y ein Sinus. 30 % Amplitudenrauschen. Ausgewertet wird nur die Phase (Amplitude normiert).
- Farbe aus Phasenversatz X gegen Y (Schwelle 5°): grün = in Phase, rot = X vorn, blau = Y vorn. Kein Minus, nur Richtung.
- Ergebnisse [M]:
  - Perfekt: 81/81 grün.
  - X-Fehler +1 % an (2,3): genau dieser Knoten rot.
  - Y-Fehler +1 % an (6,6): genau dieser blau.
  - Beide zugleich: beide richtig, Rest grün.
- Warum Periode statt Amplitude:
  - 1 % Abweichung liegt weit unter 30 % Amplitudenrauschen.
  - In der Phase summiert sich 1 % aber auf: 36° nach 10 Perioden. Länger hinsehen = empfindlicher.
- Grenze: Knoten hier ungekoppelt. Im gekoppelten Netz breitet sich die Farbe als Hof um den Fehler aus (noch zu rechnen).
- Fragen stellen = Probesignal einspeisen. Antwort = Farbmuster. Kein Eingriff in einzelne Knoten nötig. [K]

## AH Gesamttest v2 (gesamt_v2.py / .json): 13/13 Checks ok – K55 v2 auf Drive (alte Fassung → _alt_v1)
- Rückbau ×27,0 je Ring.
- Späne quadriert mit Sieb 4 Stufen je Faktor 2: Tunnel 0,94–0,97, Median-Verzug 12,52–12,81°.
- Einschwingen 21 Takte bei 9/27/81 Ringen.
- XOR7 = Kehrwert.
- Druck misst Bedarf linear (R² = 1,0); in Ruhe Defizit 0.
- 8 und 6 gleichzeitig mit 6+8 (6/6), Treppe nicht (18).
- 4D: 24 Nachbarn im Abstand 1.
- Normierung: Summe 216 exakt, Streuung 4·10⁻⁵.
- Farbhof zentriert auf Fehler, fällt nach außen (0,86 / 0,42 / 0,31 / 0,23 / 0,17).
- Nicht im Test (Annahme): AF (Tausch über Zentrum 1 Takt/Ebene), Rückfeld Z als Regel.

## AI Dauerlauf 120 000 Takte (dauerlauf.py / dauerlauf_log.json) – K55 Teil 3 Referenzwerte: l–o alle erfüllt
- l) Bilanzfehler max 3,5·10⁻⁸ (geschlossen). [M]
- m) Boden nie verletzt (0 Knoten in 120 000 Takten). [M]
- n) Außerhalb der Vielentnehmer-Phasen Bedarf = Verbrauch in jedem Fenster. [M]
- o) Defizit davor 0,0015 → schon 1000 Takte nach Phasenende wieder 0,0015 (beide Phasen). [M]
- Vielentnehmer-Phasen:
  - Deckung 99,78 % (Rest hält der Boden zurück).
  - Druck min 0,949, Zwergvorrat min 0,497.
- Ruhephasen: Defizit 0,0015, Druck min 0,975 (Fenster direkt nach Phasenende).

## AJ K55 Teil 1 – Prüfung Antigravity (Ergebnis-Ordner RAUM27_K55/Ergebnis, Kopie, nicht K55/Ergebnis)
- Code eigenständig aufgebaut (Raum in reinen Python-Schleifen, eigene Sieb-Kanten). Status im Code berechnet.
  Bericht wird per Skript aus dem JSON erzeugt. Bericht = Beleg. ✔
- Zahlen = meine Referenz:
  - Verhältnis 27,14 / 27,005 / … / 26,997
  - Tunnel 0,960 / 0,956 / 0,942 / 0,940 / 0,967
  - Median 12,55–12,81°
  - 21 Takte
  - XOR7-Produkte 1
- Laufzeit 0,67 s (Windows, Python 3,14,6, NumPy 2,5). Deshalb so schnell: Das Modell ist klein.
- Auslegungen offen gelegt (Richtung „innen“ = höhere Indizes; log-Verteilung Faktor w). Beides wie bei mir.
- Per Konstruktion korrekt markiert: a, c, e und zusätzlich d.
  - Fehler bei mir (Claude), geklärt: d (21 Takte bei allen K) ist kein Befund.
  - Das Signal klingt nach 1 Übertrag ab und erreicht tiefe Ringe nie.
  - Bessere Prüfung: Einschwingen mit Impuls in Ring K/2 bzw. Messung nach Erreichen des letzten Rings.
- Offen: Teil 2, Teil 3, Gemini-Zweitrechnung noch nicht abgegeben.

## AK Gleicher Druck, Gesamtkraft skaliert mit der Kugel (gemessen)
- Druck = Kraft/Fläche. Gleicher Vordruck auf Innen- und Außenkugel:
  - Gesamtkraft ∝ Fläche ∝ r².
  - r = 1/2/4/8/16 → 12,6 / 50,3 / 201 / 804 / 3217. Je Radiusverdopplung ×4.
- Im 6+8-Netz: Knoten je Schale (2r+1)³ − (2r−1)³ = 26 / 98 / 386 / 1538 / 6146.
  Verhältnis 3,77 → 3,94 → 3,98 → 4,00. Die Gesamtversorgung einer Schale wächst ×4 je Verdopplung, bei gleichem Druck je Knoten. [M]
- Folge für S1/K56: Der Zwerg einer äußeren Schale muss bei gleichem Vordruck die r²-fache Gesamtmenge nachschieben.
  Nicht der Druck skaliert, sondern der Gesamtbetrag.

## AL K55 Teil 3 – Prüfung Antigravity (Laufzeit 193 s): l–o „stimmt“, im Code berechnet
- Code gelesen: Normierung, Zwerg-Blockbildung (reshape/transpose hin und zurück) und Herz korrekt.
  Bericht per Skript aus JSON. Bericht = Beleg. ✔
- Ruhephasen = meine Referenz: Bedarf ~2590 je 1000 Takte, Verbrauch = Bedarf, Defizit 0,0015, min p 0,993. ✔
- Bilanz max 3,6·10⁻⁸ (meine 3,5·10⁻⁸). Boden nie verletzt. Erholung: 2,6 % bzw. 5,5 % Abweichung nach 5000 Takten. ✔
- Abweichung zu meinem Lauf in der Vielentnehmer-Phase:
  - Antigravity: Deckung 95,9 %, min z = 0,200, min p 0,938
  - ich: Deckung 99,8 %, min z 0,497, min p 0,949
  - Ursache: Antigravity hat EINEN Zwerg je Block für alle 3 Ressourcen (wörtlich nach Auftrag, offen gelegt).
    Mein Code hatte einen Zwerg je Block UND je Ressource (3×216).
  - Fehler bei mir (Claude), geklärt: Auftrag und mein Code nicht deckungsgleich, der Auftrag war mehrdeutig.
- Befund daraus: Der gemeinsame Zwerg sättigt bei z = 0,2 (Herz-Zufluss 0,2·(1−z) = Abgabe). Das ist die Kapazitätsgrenze.
  → Für K56: Zwerg je Ressource oder Herz-Rate anheben.
- Per Konstruktion korrekt markiert: l, m. Auch n ist nahezu per Konstruktion (Boden greift in Ruhe nicht). Echt gemessen: o und die Kapazitätsgrenze.
- Offen: Teil 2 und Gemini-Zweitrechnung fehlen noch.

## AM Zwerg je Ressource vs. gemeinsamer Zwerg + stärkeres Herz (zwergvergleich.py / .json)
- 12³-Netz, 3 Ressourcen, 30 000 Takte, Vielentnehmer 10 000–20 000.

  | Variante | Stress auf 1 Ressource: Deckung (R0/R1/R2), z min | Stress auf alle 3: Deckung, z min |
  |---|---|---|
  | A gemeinsam, Herz 0,2 | 99,77 / 100 / 100 %, 0,45 | 95,9 % je Ressource, 0,20 (= Antigravity K55: 95,9 %) |
  | A gemeinsam, Herz 0,6 | 99,77 / 100 / 100 %, 0,91 | 99,77 %, 0,75 |
  | B je Ressource, Herz 0,2 | 99,77 / 100 / 100 %, 0,50 | 99,77 %, 0,50 |

- Befunde [M]:
  - Die Antigravity-Abweichung ist reproduziert und erklärt: Sättigung des gemeinsamen Zwergs nur bei gleichzeitiger Last auf allen Ressourcen.
  - Kein Übersprechen: Last auf R0 senkt R1/R2 auch beim gemeinsamen Zwerg nicht („asymmetrischer Rückstau“ nicht beobachtet).
  - B ≙ A mit 3-facher Herzrate: gleiche Gesamtkapazität, gleiche Deckung.
- Aus dem Gemini-Text:
  - Bestätigt: Zwerg je Ressource ist modular und braucht keine Auslegung auf Gleichzeitigkeit.
  - Nicht bestätigt bzw. Overlay: Kohärenzverlust, Hotspots, Ventile/Multiplexer, Kirchhoff-Bruch.
  - Falsch: „null Latenz/instantan“ – jeder Ausgleich braucht Takte.
- Festlegung für K56: Zwerg je Ressource (B), fraktal 8+1. Herzrate je Ebene gleich.

## AN Zwerge auf die 6 (Flächenmitten bei Radius 1) statt einem in der Mitte (zwerg_sechs.py / .json)
- Leitungsnetz Zentrum + 6 Pole + 8 Ecken. Widerstand ∝ Leitungslänge. Entnahme 1 an Ecke (1,1,1).
- Druckabfall an der Ecke [M]:
  - Ein Zwerg in der Mitte: 0,485
  - 6 Zwerge auf den Flächenmitten: 0,295 (−40 %)
  - Davon tragen die 3 anliegenden Zwerge 84 % (je 0,280), die 3 fernen je 0,053.
  - Ein Flächen-Zwerg ausgefallen: 0,322. Es läuft weiter, die Nachbarn übernehmen. Jede Ecke hat 3 Versorger.
  - Mitte zusätzlich zu den 6: bringt nichts (Strom 0). Die Mitte bleibt frei für den Beobachter/Takt.
- Abstand Fläche → Ecke √2 = 1,414 kürzer als Mitte → Ecke √3 = 1,732.
- → Festlegung K56: Zwerge auf die 6 Flächenmitten (Radius 1, am Spiegel), je Ressource. Die Mitte nur Takt (Meta-Zwerg).
- Offen: Herz als Druckstoß für den Übergang von einer Sphäre zur nächsten (Knoten → nach oben) rechnen.

## AO Sechser-System je Ring: 6 Zwerge je Cluster, aus 6 untergeordneten (sechser.py / .json)
- 9×9×9-Netz (2 Ebenen 3×3×3), gleiche Entnahme je Knoten, Zwerge halten Druck 1. Druckabfall max / Mittel [M]:
  - 1 Zwerg je 3er-Block (Mitte), 27 Zwerge: 0,0028 / 0,0026
  - 6 Zwerge je 3er-Block (Flächen), 162 Zwerge: 0,0008 / 0,0003 (bestes)
  - „6 aus 6“, nur die 6 Flächenblöcke des Ganzen, 36 Zwerge: 0,0045 / 0,0029 (schlechter als 27 in der Mitte – Eck- und Kantenblöcke zu weit weg)
  - dazu der Zentrumsblock, 42 Zwerge: 0,0043 / 0,0027
- 6 Zwerge je 27er-Block = 6/27 = 2/9 der Knoten. Zwerge = 2/9, Versorgte = 7/9. Das ist exakt die 7/9–2/9-Aufteilung. [K, auffällig]
- → Rekursiv „6 aus 6“ reicht allein nicht. Jeder 3er-Block braucht seine eigenen 6 (dann 2/9).
  Die 6 der höheren Ebene sind die Takt-/Meta-Ebene, nicht die Versorgung.

## AP Alles kommt aus dem Nullpunkt; die 6 Zwerge sind Speicher, keine Quelle (nullquelle.py / .json)
- Mitte = einzige Quelle (Druck 1). Zwerge auf den 6 Flächenmitten mit Speicherkapazität C. Puls: Ecke entnimmt 0,5 für 20 Zeiteinheiten.
- Bilanz: Aus dem Nullpunkt kommt genau, was verbraucht wurde (10,0 = 10,0 bei C = 1 und C = 10). [M]
- Tiefster Druck an der Ecke: C = 1 → 0,757; C = 10 → 0,773; C = 100 → 0,833. Größere Zwergspeicher dämpfen den Stoß. [M]
- Preis: Mit C = 100 sind am Ende noch 0,21 offen. Der Speicher füllt sich langsamer aus der Mitte nach. [M]
- → Bild: Nullpunkt = Herz (einzige Quelle, auch für Wechselwirkung der 8 Achsen und innere Verarbeitung).
  Die 6 Zwerge puffern. Kurze Stöße fangen die Zwerge ab, die Dauerlast trägt der Nullpunkt.

## AQ Eimerkette 1/9 … 9 (eimerkette.py / .json)
- Stellen logarithmisch von 1/9 bis 9. Spiegel um 1 (1/9·9 = 1), Spanne 81 = 9².
  Jede Stelle gibt nur an die Nachbarn weiter. Innen Vordruck (Nullpunkt), außen schwankende Entnahme.
- Mittlerer Fluss auf JEDEM Glied gleich (5 Stellen: 0,00995; 9 Stellen: 0,01015). Dazwischen ruhiger Durchfluss, Kirchhoff. [M]
- Schwankung steigt linear nach außen (9 Stellen: 0 → 0,003 → … → 0,032). Die Mitte ist ruhiger, aber nicht still. [M]
- Druck fällt linear nach außen (9 Stellen: 1,0 → 0,675). Eine lange Kette kostet Druck. [M]
- → Bild bestätigt für den Mittelwert (gleicher Fluss überall, Bewegung nur an den Enden).
  Für eine wirklich stille Mitte und gehaltenen Druck braucht jede Stufe Puffer/Vordruck (6 Zwerge je Stufe, AO/AP).

## AR K55 Teil 2 Antigravity + Gemini-Zweitrechnung – Prüfung
- Antigravity Teil 2: Status f–k „stimmt“, im Code berechnet. Laufzeit 1,8 s.
  - Werte = meine Referenz:
    - Ankunft 6/6 und 18/6
    - 24 Abstände = 1
    - Summe 216 (Fehler 7·10⁻¹³), Streuung 4,35·10⁻⁵
    - Farbe 0,8605 / 0,4219 / 0,3053 / 0,2259 / 0,1682, Max (5,9)
    - R² = 1,0, Defizit bei d = 0 exakt 0 ✔
  - Abweichung Bericht ↔ Code (Kreislauf):
    - Auslegung sagt „Ring 0 hängt an 1“, der Code setzt für Ring 0 aber A[1] als inneren Nachbarn.
    - Der Fluss wird nur addiert, nicht beim Nachbarn abgezogen (nicht summentreu). Status f bleibt erfüllt (Linearität), die Steigung ist aber nicht vergleichbar.
    - Ursache auch mein Auftrag (Satz mehrdeutig). → Für K56 eindeutig formulieren.
  - Per Konstruktion korrekt markiert: f–j. k ist ebenfalls deterministisch (lineares Gleichungssystem).
    Teil 2 ist eine Konsistenzprüfung, kein neuer Befund.
- Gemini (AI Studio):
  - Nur Teil 2 abgegeben. Teil 1 und 3 fehlen.
  - Ausgabe für 6–9 echt ausgeführt (np.float64-Ausgaben), Werte identisch.
  - Abweichungen:
    - Die abgelegte Code-Datei ist unvollständig (Hilfsfunktionen und Auftrag 5 fehlen). Die Werte zu Auftrag 5 (R² 0,99999) sind nicht durch Code belegt.
    - Im Text steht Summe „216,00000000000000“, die Ausgabe sagt 215,99999999999923 (geglättet). Bericht ≠ Beleg (Fehler bei Gemini).
- Gesamt K55: Antigravity Teil 1–3 bestanden (15/15, davon die meisten per Konstruktion; echte Befunde: Faktor 27, Tunnel-Siebregel, Erholung o, Kapazitätsgrenze des gemeinsamen Zwergs).
  Gemini unvollständig.

## AS Sternförmig von Ring zu Ring: Druckabfall bleibt begrenzt (stern.py / .json)
- Nullpunkt in der Mitte (Druck 1). Weitergabe in alle Richtungen (6+8). Gesamtentnahme 1 auf der äußersten Schale.
- Größter Druckabfall bei R = 3 / 6 / 9 / 12: 0,083 / 0,084 / 0,084 / 0,084. Praktisch unabhängig vom Radius. [M]
- Zum Vergleich die 1D-Eimerkette: Abfall 3 / 6 / 9 / 12, wächst mit der Länge.
- Grund: Im Raum verteilt sich der Fluss auf die Kugelfläche (∝ r²). Der Widerstand nach außen konvergiert (∝ 1/r), statt zu wachsen.
- → Die Lücke aus AQ (Druckverlust der Kette) ist im sternförmigen Netz geschlossen. Thomas: „Haben wir doch.“
  Eimerkette nur entlang einer Feldlinie, aber viele parallel in alle Richtungen.

## AT Der Schritt zur Seite ist die Rotation (Mitrotation)
- Teilchen: je Takt 1 Ring nach außen. Der Ring dreht sich je Takt um 1 Zelle.
  - Labor: Treppe, 2 Schritte je Ring.
  - Mitrotierend: nur radial, 1 Schritt je Ring. Der seitliche Schritt kostet keinen Transport. [K]
- Ring r hat 8r Zellen. Umlauf 8r Takte, Winkelgeschwindigkeit 45°/r je Takt, Bahngeschwindigkeit überall 1 Zelle/Takt (= c). [M]
- Abstraktion: Gleiche Bahngeschwindigkeit in allen Ringen = „flache Rotationskurve“ (ω ∝ 1/r). Bekannt aus Galaxien. Nur Overlay, nicht geprüft.

## AU Pyramidenwürfel: 1 hoch + 1 seitlich in einem Takt = Diagonale unter 45° (gemessen)
- Der Würfel (Kante 2a) zerfällt exakt in 6 Pyramiden mit Spitze im Nullpunkt und Basis = Würfelfläche.
  6 · 4/3 a³ = 8a³. [M]
- Seitenflächen der Pyramide unter genau 45° (Höhe a = halbe Basis a). Das ist die Diagonale des Taktdreiecks (1 hoch, 1 seitlich, √2). [M]
- Seitenkanten = Raumdiagonalen Mitte → Ecke (√3).
- Je Ring: 2D-Ring 8r Zellen = 4 Dreiecke à 2r. 3D-Schale 24r² + 2 = 6 Pyramidenbasen à 4r² (+2 gemeinsame Ecken/Kanten-Anteil).
- Bezug:
  - 6 Pyramiden = 6 Zwerge auf den Flächenmitten (AN). Jeder Zwerg sitzt in der Basismitte „seiner“ Pyramide.
  - Die Spitze ist der Nullpunkt (Quelle).
  - Die Treppe (oben + seitlich) läuft auf der 45°-Pyramidenfläche.

## AV Wie viele Zwerge? 6^x vs. Bedarf (Zählung, Bezug AO)
- Ebene x: Knoten 27^x. Versorgungs-Zwerge nach AO: 6 je 27er-Block = 6·27^(x−1) = 2/9 der Knoten.
- 6^x (Takt-/Meta-Zwerge, „6 aus 6“): 6 / 36 / 216 / 1296. Reicht nicht zur Versorgung (AO: 36 Zwerge schlechter als 27 in den Blockmitten), passt aber als Taktbaum. [M]/[K]
- 6^(x^n), n = 2: 6 / 1296 / 10⁷ / 2,8·10¹². Übersteigt ab x = 2 die Knotenzahl (729), also mehr Zwerge als Knoten. Nicht sinnvoll als Zwergzahl. [K]
  Höchstens als Zahl der Zustände/Spiegelbilder denkbar (Overlay, vgl. N^N, 9^9).
- Zuordnung c² (Quadrant) / c⁴ (Beobachter im Nullpunkt): Overlay, nicht hergeleitet.
- Festlegung Vorschlag: Versorgung 6·27^(x−1) (2/9), Takt 6^x, Spiegel n = Zahl der Ebenen.

## AW Skalierbarkeit – was belegt ist, was Grenze ist
- Belegt [M]:
  - Druckabfall sternförmig unabhängig vom Radius (AS).
  - Wechselwirkung fällt ×27 je Ring nach innen (Zoom).
  - Normierung und Bilanz erhalten.
  - 7/9-Lenkung tiefenunabhängig (G, mit Einschränkung aus AJ).
  - Gleiche Regel an jedem Knoten (T).
- Grenzen:
  - Laufzeit wächst mit dem Radius (R Takte).
  - Je Ebene 2/9 Versorgungs-Zwerge.
  - Rechenaufwand ∝ Knotenzahl (für Simulation).
  - Zoom-Ersatz (6 Zwerge = 1 Ersatz-Zwerg) noch nicht gerechnet.
- Zugang „für jeden, der rein möchte“: Eintritt und Austritt frei (F8, freier Wille). Grundbedarf ab Eintritt gesichert (Boden).

## AX 6 Zwerge → 1 je Ebene: Komplexität als Potenz 6^x; Ableitung = Integral bis auf Faktor (gerechnet, sympy)
- 6^x ist sich selbst gleich unter Ableitung und Integral: Nur der Faktor ln 6 ändert sich.
  - 8. Ableitung = (ln 6)⁸ · 6^x. 8. Wurzel dieses Faktors = ln 6 (= eine Ableitung). [M]
  - 8. Integral = (ln 6)⁻⁸ · 6^x. Ableitungs- × Integralfaktor = 1 (Spiegel). [M]
- Gilt NICHT für Potenzen x^8: 8. Ableitung = 40 320 (Konstante), 8. Wurzel = x. [M]
  → „8. Ableitung = 8. Wurzel“ stimmt nur für die Exponentialform 6^x (bzw. b^x), im Faktor.
- Quadrierkette c → c² → c⁴ → c⁸: Die 8. Wurzel von c⁸ ist c. 3× Quadrieren ↔ 2³-te Wurzel. [K]
  So bleibt man „innerhalb 2c, c², c⁴“.

## AY Fläche vs. Raum über 9 Ebenen (gezählt)
- Fläche: 9 in 9, neunmal → 9⁹ = 387 420 489 = 3¹⁸. Gleiche Zahl wie die simulierte Unendlichkeit bei K = 18 (Z). [K]
- Raum: 27 in 27, neunmal → 27⁹ = 7 625 597 484 987 = 3²⁷. Gleiche Zahl wie die simulierte Unendlichkeit bei K = 27 (Z): „RAUM27“. [K]
- Bei 9 Ebenen im Raum:
  - Versorgungs-Zwerge 2/9 · 27⁹ = 6·27⁸ ≈ 1,7·10¹²
  - Organisationseinheiten 6⁹ = 10 077 696
  - 6^(9²) hätte 64 Stellen (Zustandszahl, Overlay).

## AZ Ur-Zwerg: 1 stupst 6 Flächen an, jede spannt 8 Achsen auf (90° versetzt) → 6×8 = 48 (gezählt)
- Ur-Zwerg in der Mitte → 6 Flächen (direkt). Jede Fläche → 8 Richtungen in ihrer Ebene (4 Achsen + 4 Diagonalen), 90° zur Elternachse.
- 6 × 8 = 48 Wege. Sie treffen 20 verschiedene Ziele [M]:
  - 12 Kanten, je 2 Wege
  - 8 Ecken, je 3 Wege
  - Mit den 6 Flächen werden alle 26 Nachbarn erreicht.
- 48 = Ordnung der vollen Würfelsymmetrie (alle Drehungen + Spiegelungen). Jede Lage des Würfels genau einmal. [K]
- Druckmessung: Kanten doppelt, Ecken dreifach abgesichert (Redundanz = Messgenauigkeit / Ausfallsicherheit).
- Rekursiv: Jedes Ziel ist Mitte des nächsten 27er-Blocks. Der Ur-Zwerg verbindet alles über 1 → 6 → 48.

## BA Kreislauf-Bild: Mitte = Herzschlag; 6 Achsen hinaus (Arterien), 8 Diagonalen zurück (Venen)
- Ablauf:
  1. Ein Druckabfall außen läuft als Information über die Zwerge nach innen.
  2. Die Mitte merkt es und gibt einen Druckstoß über die 6 gefüllten Achsen-Adern hinaus.
  3. Verbrauchtes läuft über die 8 Diagonal-Kanäle zurück.
- Deckt sich mit F7 (Festlegungen): 6 Tropfen innen → außen, 8 Tropfen außen → innen, orthogonal. [K]
- Laufzeiten (aus K55 Teil 2, bestätigt): Achsen R Takte, Diagonalen mit Eckverbindung ebenfalls R Takte, als Treppe 3R.
  → Hin und Rück gleich lang, Kreislauf im Takt nur mit 6+8-Verbindungen. [M]
- Reaktionszeit: Meldung nach innen R + Stoß nach außen R = 2R. Rückfluss R. Ein Umlauf 3R? Noch zu rechnen (Puffer der Zwerge verkürzt die Wirkung vor Ort, AP).

## BB Gesamtbild: Rechenmaschine mit Kurbel
- RAUM27 arbeitet wie eine mechanische Rechenmaschine (Staffelwalze/Arithmometer):
  - Zählräder mit Totzeit: Erst zählen, wie viele Zähne fehlen (Lücken, die am Herzen ankommen), dann genau so weit drehen.
  - Übertrag bei 10 = 90°-Umleitung in die nächste Ebene.
  - Die Totzeit (1 Takt je Ring) verhindert Überschießen; mit der 7/9-Lenkung stabil.
- Die Kurbel, die alles antreibt, ist der Wunsch bzw. Bedarf. Ohne Kurbel steht die Maschine (Fluss in Ruhe 0).
- Mehr Operatoren als beim Taschenrechner:
  - Spiegel/Kehrwert (XOR 1, XOR 7)
  - Drehung um die 1 (Zyklus 1234)
  - Verdopplung (sin²)
  - Wand (sinh)
  - Inversion (1/sin)
  - Normierung (7/9–2/9)
  - Boden (Grundbedarf)
  - Resonanztunnel (180°)

## BC Prüfung F13 (Antigravity, Ordnungsmodell Optionsraum)
- Passt zum System:
  - 7/9 Ordnung + 2/9 frei, aufgeteilt in 1/9 nach außen (90°-Übertrag XY→XZ→XT) und 1/9 nach innen (Inversion). = F5 + F11. ✔
  - 6 Blickrichtungen auf denselben Zustand; erst 6+8 schließt. = F7. ✔
  - 2^N Orthanten (3D 8, 4D 16). ✔
- Zu korrigieren:
  - „−1/9“, „±1/9“: Minus widerspricht F9. Schreibweise: 1/9 nach innen / 1/9 nach außen.
  - „Unter 7/9 ist die Perkolationsschwelle nicht erreicht“ ist falsch (Fehler bei Antigravity).
    Gemessen im 6+8-Gitter (40³, 20 Läufe): ein durchgehender Cluster entsteht schon ab ~14 % Besetzung (0,13: 0/20; 0,14: 9/20; 0,15: 20/20).
    7/9 ist eine gesetzte Regel, keine Perkolationsgrenze.
  - „Kältetod bei 9/9“: Overlay.
  - „7/9 der Relationen kohärent“ ist noch nicht messbar definiert.
    Vorschlag: Anteil der Verbindungen mit |Verzug − Vorhalt| < Schwelle.
- Status: Testbasis, ungeprüft. Die Testliste (Skalensprung, Deadlock, Bilanz, Störung) ist sinnvoll.

## BD Untere Hälfte weglassen: nur oben rechnen, Richt-Bit ergänzt (gemessen)
- Feld nur für z ≥ 0 gerechnet, unten = Spiegelbild × Richt-Bit (+ oder −):
  - gerade Anteile (Dipol x, z²): Bit + → exakt (4·10⁻¹⁶). Mit falschem Bit Fehler 4.
  - ungerade Anteile (Oktopol xyz): Bit − → exakt (2·10⁻¹⁶). Mit falschem Bit Fehler 2.
  - gemischt (z + z²): Mit einem Bit allein falsch (Fehler 2). Muss in geraden und ungeraden Teil getrennt werden, jeder mit eigenem Bit.
- → In der Fläche bzw. oberen Hälfte rechnen ist exakt, wenn jeder Anteil sein Richt-Bit trägt (Richtoperator, F9).
  Die 6 Achsentropfen sind je Achse ungerade, der Oktopol in allen drei.
- Pro Spiegelschnitt halbiert sich die Rechnung. Mit den drei Schnitten (2 Polschnitte, 90° versetzt, + Äquator) auf 1/8: ein Achtel + 3 Bits.
- Grenze: Nur für symmetrische Felder. Eine einseitige Störung (z. B. Vielentnehmer an einer Stelle) bricht die Symmetrie, dann voll rechnen oder Störung getrennt führen.

## BE Grundgitter Kugel/Würfel: ein Achtel + 3 Richt-Bits (gittermuster.py / gittermuster_achtel.json)
- Drei Bits: Seite (welches Achtel), Blick (innen → außen / außen → innen), Fluss (hinaus / zurück). Gerechnet wird nur ein Achtel.
- R = 6:
  - Achtel 343 Knoten. Durch Spiegeln das Vollgitter 2197 = 13³, exakt, keine Doppelten. [M]
  - Im Achtel: 1 Zentrum, 18 auf Achsen, 108 auf Spiegelflächen, 216 = 6³ innen.
- Würfelschalen im Achtel: 1, 7, 19, 37, 61, 91, 127 = 3s² + 3s + 1 = zentrierte Sechseckzahlen.
  Die Achtel-Schale eines Würfels, von der Raumdiagonale gesehen, ist ein Sechseck (G1). [M]
- Kugelschalen im Achtel: 1, 6, 13, 19, 39, 55, 72 (euklidisch gerundet). Zum Vergleich mit den Würfelschalen.

## BF Achtel ↔ Pyramidenwürfel (gezählt)
- Ein Achtel enthält je ein Viertel von 3 Pyramiden (+X, +Y, +Z). Zugehörigkeit: Die Pyramide ist dort, wo diese Koordinate am größten ist.
- R = 6, Achtel 343 Knoten [M]:
  - 91 je Pyramidenviertel (×3)
  - 69 auf den 45°-Flächen x = y, y = z, x = z (gemeinsam, hier läuft die Treppe)
  - 1 Zentrum
- Die 45°-Flächen zerlegen das Achtel in 3! = 6 Tetraeder (Grundbereiche).
  - Je Pyramide 8 Tetraeder.
  - Gesamt 8 Achtel × 6 = 6 Pyramiden × 8 = 48 = Würfelsymmetrie (vgl. AZ, Ur-Zwerg 6×8). [K]
- → Kleinste Rechenzelle: 1 Tetraeder (1/48) + Bits für Achtel, Pyramide und Reihenfolge. Gilt nur bei voller Symmetrie.

## BG Kausalitätsabriss = Courant-Bedingung (CFL); neuer Spiegel = Zellgröße ×2 (gemessen)
- Übertragung höchstens 1 Zelle je Takt.
  - Ist die Feldgeschwindigkeit größer (Courant-Zahl > 1), explodiert die Lösung: 1,5 Zellen/Takt → Amplitude 10¹⁰³ nach 400 Takten = Chaos/Abriss.
  - Genau bei 1: verlustfrei (Amplitude 1).
  - Unter 1: stabil, glättet (0,44 bei 0,75).
- Abhilfe = neuer Spiegel, Zellgröße ×2:
  - 1,5 Zellen/Takt bei doppelter Zelle → Courant 0,75 → stabil.
  - 3 Zellen/Takt → braucht ×4 (zwei Spiegel).
  - Allgemein: je Verdopplung der Geschwindigkeit ein weiterer Spiegel (½ ↔ 2). [M]
- Das ist das bekannte Stabilitätskriterium der Numerik (Courant–Friedrichs–Lewy). Thomas' Abriss ist damit präzise definiert: v·Takt/Zelle > 1.
- Auslesen: 3 Schnitte × 2 Seiten (Richt-Bit) = 6 Bilder, je ein Quadratgitter.
  Vollständig nur für Produktfelder (G9: 19 von 27 Zellen in den Schnitten, Ecken nur bei separablem Feld). Sonst fehlt die Wechselwirkung in den Achteln.

## BH Abriss als Reichweite mit Rückweg (Bild Thomas: 10 km Reichweite, hin und zurück)
- Reichweite je Takt L = 10. Er muss zurückkommen und beide Richtungen bedienen. Größter Knotenabstand [M]:
  - Fläche, Treppe (hoch + seitlich, zurück): L/4 = 2,5 (Thomas' Zahl)
  - Raum, Treppe (3 Achsen, zurück): L/6 = 1,67
  - Fläche, Diagonale direkt: L/(2√2) = 3,54
  - Raum, Raumdiagonale direkt (6+8): L/(2√3) = 2,89
- Mit Eckverbindungen 5,2-mal weniger Knoten im Raum für dieselbe Reichweite.
- Abriss = Knotenabstand größer als diese Grenze. Neuer Spiegel = Abstand halbieren bzw. Zelle ×2 (BG).
- BH2 Mit 90°-Drehung und Spiegel muss nur ein Quadrant abgelaufen werden (L = 10):
  - A Stern: links hin + zurück, hoch hin + zurück: 4d = 10 → d = 2,5; 2 Achsknoten.
  - B Pythagoras-Dreieck: Zentrum → links (d) → Ecke (d) → diagonal zurück (d√2). d(2 + √2) = 10 → d = 2,93.
    Achse + Ecke in einer Runde; ×4 Drehung/Spiegel = alle 8 Nachbarn (3×3). Besser als A. [M]
  - Raum: Zentrum → Achse → Kante → Ecke → Raumdiagonale zurück. d(3 + √3) = 10 → d = 2,11.
    Achse, Kante, Ecke in einer Runde; ×48 Symmetrie = alle 26 Nachbarn. [M]

## BI Prüfung eingereichter Rückmeldung (zu O1, O3, O4, Hex-Code)
- Zusammenfassung der Invarianten: korrekt wiedergegeben.
- O1 (4 Siebstufen = Zyklus 1234, Faktor 2^(1/4) je 90°): stimmig mit AC (≈ 4 Stufen je Faktor 2). Übernehmen als Festlegung der Stufung.
  Tunnel je Faktor 2 mit n Stufen [M]:
  - n = 1: 0,680
  - n = 2: 0,871
  - n = 4: 0,961
  - n = 8: 0,990
  - n = 16: 0,997
  „Gegen 1 ohne Zusatzparameter“ ist überzogen: Mit 4 Stufen sind es 0,96, gegen 1 erst mit mehr Stufen.
- O3: 16/9 − 1 = 7/9 ist arithmetisch richtig [M]. Dass die 7/9 der Log-Uhr (1/9 … 8/9) dadurch verursacht wird, ist nicht gezeigt. Status: Abstraktion, O3 bleibt offen.
- O4 (2:1 aus E25 abgeleitet): keine Herleitung, Formel fehlt. Overlay. O4 bleibt offen.
- Hex-Code-Baustein: korrekt, entspricht H. Nichts Neues.
- Angebot, GRUNDLAGE_intern.md im Drive zu suchen: Datei ist bewusst nur lokal (intern), nicht auf Drive.

## BJ Dauerläufer: Rundungstest bewusst offen lassen (Entscheidung Thomas)
- Die absolute Grenze 1e−6 bleibt. Erwartung: Halt bei ~5 Mio. Takten (Drift ~1,9·10⁻¹³ je Takt, Stand 550 000: 1,05·10⁻⁷).
- Hält er wegen Rundung, ist die Struktur zu ändern, nicht die Grenze. Kandidaten:
  1. Ganzzahlige Eimer (Eimerkette, BB/BH): Ressource in festen Einheiten, Weitergabe ganzzahlig → Summe exakt, keine Rundung.
  2. Kompensierte Summation (Kahan) der Bilanz.
  3. Festkomma-Arithmetik.
- Vorzug: 1 (passt zum Modell, Erhaltung per Konstruktion exakt).

## BK Perfekte 180°-Inversion häuft keine Rundung an (gemessen)
- x → 1/x zweimal: Bei 86 % der Gleitkommawerte exakt zurück, sonst 1 Rundungsschritt daneben.
- 2 / 10 / 1000 / 100 000 Inversionen hintereinander: max. Abweichung bleibt 2,2·10⁻¹⁶. Kein Anwachsen, der Fehler ist eingesperrt. [M]
- → Thomas' Bedingung bestätigt: Sind alle Ebenen über perfekte 180°-Inversion (Involution) gekoppelt, wächst die Rundung nicht.
  Die Drift im Dauerläufer kommt aus den nicht-involutiven Schritten: Entnahme mit beliebigen Gleitkommawerten, Zwerg-Anteile, Herz-Rate.
- Umbau-Regel: Jeder Schritt als exaktes Paar (Hin = Rück). Inversion, XOR, ganze Eimer.

## BL Vierfarben-Anzeige (Vorschlag Thomas, Regeln ausformuliert)
Messgröße je Knoten: Δ = Verzug − Vorhalt (Phase), Änderung je Takt dΔ.
- Grün: |Δ| < Schwelle und |dΔ| < Schwelle → eingeschwungen, gleicher Abstand.
- Rot: Δ nimmt ab (Kennung −) → Annäherung.
- Blau: Δ nimmt zu (Kennung +) → Flucht.
- Gelb: Rest in dieser Ebene nicht auflösbar (Courant > 1 oder Rest > Schwelle nach Einschwingzeit)
  → Übergabe über das 1/9-Tor nach außen (90°-Übertrag) oder nach innen (Inversion). Richt-Bit sagt, wohin.
- Hinweis: In der Physik (Doppler) ist es umgekehrt: Annäherung blau, Flucht rot. Für die Präsentation Konvention festlegen.
- BL2 Prüfung Gemini-Farbtext:
  - Richtig: Gelb = Rot + Grün (additiv), Komplement zu Blau; Farbtonkreis R 0° / Y 60° / G 120° / C 180° / B 240° / M 300°; Gegenfarben des Auges Rot–Grün und Blau–Gelb (Hering).
  - Ungenau: Höchste Helligkeitsempfindlichkeit liegt bei 555 nm (gelbgrün), nicht bei 575–580 nm. Spektrum 400–700 nm ist ein Verhältnis von 1,75, keine volle Oktave.
  - Widerspruch: Gemini setzt Rot = Expansion, Blau = Kontraktion. Bei Thomas (BL) ist Blau = Flucht, Rot = Annäherung. Muss einheitlich werden.
  - „6 Flächen ↔ 60°“ und „RGB = Weiß = Nullsumme“: Overlay.
- Empfehlung: 90°-Kreuz (passt zum 4-Takt 1234 und zum Übertrag):
  - Achse in der Ebene: Rot (Annäherung) ↔ Blau (Flucht), Kennung −/+.
  - Achse senkrecht dazu: Grün (bleibt in der Ebene, eingeschwungen) ↔ Gelb (verlässt die Ebene, 90°-Übertrag in die nächste Oktave).
  - Gelb ist damit genau der 90°-Sprung. Die Farbtheorie wird dafür nicht gebraucht (eigene Konvention).
- BL3 Festlegung Thomas (ersetzt BL/BL2):
  - Grün: in Phase, okay.
  - Blau: Phasenverschiebung, Richt-Bit sagt welche:
    - induktiv (Strom läuft nach, Verzug, Kennung +) = Entfernen
    - kapazitiv (Strom läuft vor, Kennung −) = Annähern
    - Elektrisch: Spule bis 90° nach, Kondensator bis 90° vor. Unser fester Verzug 12,54° ist induktiv.
  - Gelb: Rest, der weitergegeben wird. Entsteht erst, wenn 7/9 eines Blocks grün (stabil) sind.
    Dann geht der 2/9-Rest gelb über die 1/9-Tore nach außen/innen.
  - Rot: frei. Vorschlag: Abriss/Fehler (Courant > 1, Boden verletzt).
- BL4 Gelb genau (Thomas bestätigt):
  - Gelb = was nach dem Stabilisieren der Rotation als Schräglage gegenüber den perfekten 90° übrig bleibt.
    Das ist der Rest der 180°-Paarung (G14: Nutation ∝ 1/ω², bei Spin 40 ≈ 0,0009 von 0,17).
  - Weitergabe nach außen: Skala 1–10 (Übertrag bei 10, größere Ebene).
  - Weitergabe nach innen: Skala 0–9 (Nachkommastelle, feinere Ebene, über die Inversion).
  - Beide Skalen sind an der 1 gespiegelt.
- BL5 Der gelbe 2/9-Rest teilt sich in zwei einzelne Neuntel:
  - nach außen als 9/1
  - nach innen als 1/9
  9/1 · 1/9 = 1 → Spiegelpaar an der 1, die Bilanz bleibt geschlossen. Jedes Tor trägt genau ein Neuntel. [K]
- BL6 Aus der Dualität werden zwei Singularitäten (Thomas):
  - Das Paar 9/1 | 1/9 trennt sich in zwei einzelne Punkte.
  - Jeder wird zum neuen Zentrum (lokale Eins, ±0-Punkt aus N) seiner Ebene: außen der Keim der größeren, innen der Keim der feineren Ebene. Je ein neuer Ur-Zwerg.
  - Begriff: „Singularität“ hier = Einzelpunkt/Keim. Nicht im physikalischen Sinn unendlicher Dichte (nur 1/9 Menge, endlich).
