# K55 (v2) – Unabhängiger Nachbau „RAUM27 Gesamtmodell“
Ausführung: Antigravity (Code + Ausführung). Zweitrechnung: Google AI Studio (Gemini Flash über API, MIT Codeausführung).
Regeln:
- Kein Wert von Hand. Jeder Status wird im Code aus der Zahl berechnet. Bericht = Beleg.
- Jede Abweichung wörtlich melden, nichts glätten.
- Rahmen: Das Modell ist wie ein Computerspiel zu behandeln, mit festen Spielregeln und ohne Anspruch auf Physik.
  Geprüft wird nur, ob die Regeln ein geschlossenes, stabiles System ergeben.
Zwei Teile, getrennt abgeben. Erst Teil 1, dann Teil 2. Zufallsstartwert überall 27.

## TEIL 1 – Kern
1. Raum. Feld F(u) = exp(0,7·u1 + 0,5·u2 + 0,4·u3 + 0,3·u1·u2·u3).
   - Ring k = 0…8: Gitter u ∈ {−3^−k, 0, 3^−k}³.
   - Jede der 8 Ecken aus den Mittelschnitten rekonstruieren:
     F(i,j,l) ≈ F(i,j,M)·F(i,M,l)·F(M,j,l)·F(M,M,M) / (F(i,M,M)·F(M,j,M)·F(M,M,l)), M = Mitte.
   - Max. relativen Fehler je Ring melden, dazu das Verhältnis Fehler(k)/Fehler(k+1) für k = 1…7.
2. Späne.
   - Ebene k = 0…4: Geschwindigkeit w = 2^(2^k), mittlere Größe s = 2/w.
   - Größen log-gleichverteilt im Faktor w um s (100 000 Stück).
   - T0 = tan(12,54°)/2. Verzug φ = atan(w·s·T0).
   - Sieb mit n = max(4, 4·log2(w)) gleich breiten Log-Stufen. Bezug je Stufe = Median-φ der Stufe.
   - Tunnel T = 1/(1 + 360·sin²(φ − Bezug)). Melden je Ebene: Mittel T und Median φ.
3. Einschwingen.
   - Zustand e: K Ringe × 24 Positionen × 2D, K ∈ {9, 27, 81}.
   - Start: Ring 0 gleichverteilt in [−1,1], sonst 0. Zähler z ab 0.
   - Je Takt:
     - wenn z mod 16 = 1: alle Ringe eins nach innen schieben, Ring 0 = 0
     - sonst: jede Position übernimmt den Wert der Nachbarposition (Index −1), dreht ihn um 90° ((x,y) → (−y,x)) und multipliziert mit 2/9.
   - Takte zählen bis max|e| < 1e−12.
4. Hex-Register. Achtel-Code h = 8…15, Bit je Achse: 1 = außen (Wert 2), 0 = innen (Wert 1/2).
   Prüfen: Wert(h) · Wert(h XOR 7) = 1 je Achse.
Status Teil 1:
- a) Fehlerverhältnis ∈ (26; 28) für k = 1…7
- b) Tunnel ≥ 0,9 in allen Ebenen
- c) Median-φ = 12,54° ± 0,5°
- d) Takte bei K = 9/27/81 identisch
- e) XOR-7-Produkt = 1 (< 1e−12)

## TEIL 2 – Netz
5. Kreislauf.
   - 9 Ringe, Druck A = 1. Je Takt nimmt jeder Ring mit Wahrscheinlichkeit 0,5 einen Bedarf ∈ [0, 2d] (nicht mehr als vorhanden).
   - Danach in dieser Reihenfolge:
     - Fluss vom inneren Nachbarn f = 0,25·(A_innen − A), Ring 0 hängt an 1
     - zusätzlich Linearvektor A += max(0,25·(1 − A), 0)
   - d ∈ {0; 0,002; 0,004; 0,008; 0,016}, 3000 Takte, ausgewertet ab Takt 1500.
   - Melden: mittleres Defizit (1 − Mittel A) gegen mittleren Bedarf, R², Defizit bei d = 0.
6. Resonanz 6×8.
   - Würfel 13×13×13 (R = 6).
   - Breitensuche gleichzeitig von 8 Ecken und gesondert von 6 Flächenmitten.
   - Einmal mit Verbindungen 6 Flächen + 8 Ecken, einmal nur 6 Flächen.
   - Melden: Ankunftstakt im Zentrum je Fall.
7. 4D. Punkte (±½)⁴ und ±Einheitsvektoren (24 Stück). Melden: Abstände zum Ursprung.
8. Normierung.
   - Gitter 6×6×6 periodisch, Start 216 in einem Knoten.
   - Je Takt: neu = 2/9·alt + Σ 1/9·(6 Flächennachbarn) + Σ 1/72·(8 Ecknachbarn).
   - 60 Takte. Melden: Summe, Standardabweichung.
9. Farbe.
   - Gitter 15×15, 8 Nachbarn (Flächen + Diagonalen). Randknoten zusätzlich an die Bezugsphase gekoppelt (+1 auf der Diagonale).
   - Löse L·φ = Δ mit Δ = 3,6 am Knoten (5,9), sonst 0.
   - Melden: Ort des Maximums, φ entlang (5,9…13).
Status Teil 2:
- f) R² > 0,999 und Defizit bei d = 0 exakt 0
- g) mit 6+8: 8er-Ankunft = 6er-Ankunft
- h) nur Flächen: 8er-Ankunft ≠ 6er-Ankunft
- i) alle 24 Abstände = 1
- j) Summe = 216 (< 1e−9), Standardabweichung < 1e−3
- k) Maximum bei (5,9), streng fallend nach außen

## TEIL 3 – Dauerlauf (Ressourcen und Stabilität)
Gitter und Regeln:
- Gitter 12×12×12, periodisch, 3 Ressourcen. Knotendruck p, Start 1. Vordruck X = 1, Boden G = 0,9.
- 8+1: Je 2×2×2-Block gibt es einen Zwerg-Vorrat z (216 Stück, Start 1).

Je Takt in dieser Reihenfolge:
1. Bedarf
   - Je Knoten und Ressource mit Wahrscheinlichkeit 0,05 ein Wunsch ∈ [0; 0,02].
   - Vielentnehmer: In den Takten 20 000–39 999 und 80 000–99 999 kommt im Block x, y, z ∈ {2, 3} je Knoten +0,05 dazu.
   - Entnommen wird min(Wunsch, max(p − G, 0)).
2. Normierung: p = 2/9·p + Σ 1/9·(6 Flächennachbarn) + Σ 1/72·(8 Ecknachbarn).
3. Zwerg
   - fehl = 0,25·max(X − p, 0) je Knoten.
   - Der Zwerg gibt seinem Block min(Σ fehl, z). Die Verteilung auf die Knoten ist anteilig zu fehl.
   - z wird um die gegebene Menge verringert.
4. Herz (Quelle von außen): Jeder Zwerg bekommt 0,2·max(1 − z, 0).

Laufzeit: 120 000 Takte.

Alle 1000 Takte melden:
- Bedarf, Verbrauch, Quelle
- Bilanzfehler: (Σp + Σz) − (Start + Quelle − Verbrauch)
- minimaler p, Anzahl Knoten mit p < G
- mittleres Defizit (X − Mittel p), Standardabweichung von p, minimaler z

Status Teil 3:
- l) Bilanzfehler |·| < 1e−6 in jedem Fenster
- m) Boden nie verletzt
- n) Verbrauch = Bedarf außerhalb der Vielentnehmer-Phasen
- o) mittleres Defizit nach jeder Vielentnehmer-Phase innerhalb von 5000 Takten zurück auf den Wert davor (±10 %)

## Für AI Studio
Beide Teile selbst in Code umsetzen und ausführen. Keine Schätzung. Code und Zahlen zurückgeben.
