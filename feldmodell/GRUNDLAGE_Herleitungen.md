# RAUM27 Grundlage – intern (nicht hochladen, nicht pushen)
Stand 08.11. Rechnung: feld/verbind.py

## G1 Eine Würfelsicht ergibt 6 und 4+4 in der Fläche (gemessen)
- Blick entlang der Achse (N/S/O/W-Sicht):
  - 6 Flächen werden zu 2 in der Mitte + 4 im Ring.
  - 8 Ecken werden zu 4 im Ring (auf den Diagonalen).
  - Radienverhältnis Ecken zu Flächen: √2.
- Blick entlang der Raumdiagonale (Sechser-Sicht):
  - 8 Ecken werden zu 2 in der Mitte + 6 im Ring.
  - 6 Flächen werden zu 6 im Ring.
  - Beide Ringe liegen auf denselben Winkeln (0, 60, …, 300°).
  - Radienverhältnis Ecken zu Flächen: exakt 2 (0,8165 → 1,6330), also Verdopplung 1 → 2 (sin²).
- Wechsel zwischen den beiden Sichten: Drehung um 54,7356° = arccos(1/√3).
- Die „2 in der Mitte“ ist jeweils die Beobachter- bzw. Polachse.
- Lesart: 6 = 8 − 2 und 4 = 6 − 2. Die Sechs und die Vier+Vier sind derselbe Würfel aus zwei Blickachsen.

## G2 16/9 (gemessen und Abstraktion)
- 16/9 = 2⁴/3² = (4/3)², ln(16/9) = 4·ln2 − 2·ln3 = 0,57536.
  - Teilt man jede Achse durch 2, entsteht das 8er-Fraktal (2³ Zellen); durch 3 das 9er-Fraktal (3² in der Fläche, 27 im Raum).
  - Im Logarithmus wird der Quotient zur Differenz der beiden Fraktal-Logarithmen.
- Ein Kreis mit Durchmesser 9 hat fast die Fläche eines Quadrats mit Seite 8:
  - π ≈ 4·(8/9)² = 256/81 = 3,1605, Fehler +0,60 %.
  - 256 = 2⁸ = 4⁴; 81 = 3⁴, das sind die 81 Zellen in 4D (siehe Paritätstest).
- Damit ist 16/9 die Brücke Kreis/Kugel (Sinus) ↔ Quadrat/Würfel (8er).
- In der Sinusfunktion u = 16x/(9λ2):
  - Für λ2 = 1 läuft der Sinus ungefähr eine Kreisfläche in Quadrat-Einheiten ab.
  - Die Spirale 1/sin streicht 180°·9/16 = 101,25°.
  - Status: Abstraktion. Es ist nicht gemessen, dass die Natur 16/9 wählt.

## G3 Gittergewichte bestätigen 8 + 1 und 27 (gemessen, per Konstruktion aus 1D 2/3, 1/6, 1/6)
- Fläche, 9 Zellen:
  - Rest 4/9, 4 Achsen je 1/9 (zusammen 4/9), 4 Diagonalen je 1/36 (zusammen 1/9).
  - 4+4 Richtungen + Zentrum = 9.
- Raum, 27 Zellen:
  - Rest 8/27; 6 Flächen zusammen 4/9; 12 Kanten zusammen 2/9; 8 Ecken zusammen 1/27.
- Bereits früher festgelegt (Festlegungen): bcc 6+8 mit Rest 2/9 und Nachbarn 7/9.

## Verbindung (Kette)
Kugel/Sinus innen → Spiegel am Einheitskreis → Würfel/8er außen.
- In der Fläche sieht man, je nach Blickachse, 4+4 oder 6.
- Der Maßstab zwischen beidem ist 16/9 ≈ Kreisfläche/Quadratfläche.

## Offen (prüfbar)
- O1: Ergibt λ2 aus einem Feldmodell (Zentrum v⁴, Spitzen v²) zwingend 16/9, oder ist es frei wählbar?
  Test: Phasenverschiebung pro Schale konstant nur bei 16/9?
- O2: 54,7°-Drehung als Übergang zwischen den beiden Tropfensystemen (6 Achsentropfen ↔ 8 Diagonaltropfen) im Feld nachrechnen.

## G4 Acht Quadranten als Koordinatensystem (gemessen)
- Oktant = Vorzeichentripel (±,±,±) = Würfelecke = Diagonaltropfen.
  Die 6 Flächen/Achsen sind die Grenzen zwischen den Oktanten.
- Winkel zwischen Oktant-Richtungen, von einem Oktanten aus gezählt: 1 : 3 : 3 : 1.
  - Eigener Oktant: 0°.
  - 3 Nachbarn (1 Vorzeichen anders): 70,53°.
  - 3 übernächste (2 Vorzeichen anders): 109,47°.
  - 1 Gegenüber (alle Vorzeichen anders): 180°.
- 90° gibt es zwischen Oktanten im Raum nicht.
  - 90° tritt erst in der Achsen-Projektion auf (4 Quadranten in der Fläche).
  - In der Diagonal-Projektion sind es 60/120/180°.
- Stoßfaktor zweier Strahlen gleicher Energie (Physik, gemessen): s = 2E²(1−cosθ).
  - 70,5° → 2/3
  - 90° → 1
  - 109,5° → 4/3
  - 180° → 2
  - 90° → 180° verdoppelt also s. Die Masse wächst dabei um √2, passend zu G1 (√2 und 2).
  - Auffällig: (4/3)² = 16/9. Status: Abstraktion; noch nicht geprüft, ob das Zufall ist.

## G5 Feldleiter c², c⁴ (Abstraktion, dimensionsrichtig)
- c² = Energie pro Masse. Spitzen/Deltas.
- c⁴/G = Maximalkraft (Planck-Kraft, Vermutung in der Physik). Zentrum/Beobachtung.
- c⁵/G = Maximalleistung.
- Zuordnung zu v⁴ im Zentrum und v² in den Spitzen: Overlay, nicht gemessen.

## G6 Urknall-These Thomas – Prüfstatus
- „e⁺e⁻ treffen sich nicht, 90° versetzt“ widerspricht der Messung (Grenze der Physik).
  - Ruhende e⁺e⁻ annihilieren in 2 × 511 keV-Photonen, die 180° auseinanderfliegen (PET).
  - Der Winkel bestimmt nur, wie viel Strahlenergie zusätzlich verfügbar ist.
- „mc² = kinetische Energie“: Physikalisch ist mc² die Ruhenergie.
  Kinetische Energie ist (γ−1)mc² und kommt dazu.
- c^c ist nicht definiert: Ein Exponent muss dimensionslos sein.
  - c in m/s: Ergebnis 10^2,5 Mrd.
  - c in km/s: Ergebnis 10^1,6 Mio.
  - c = 1: Ergebnis 1.
  - → Ersetzen durch eine dimensionslose Zahl N: Verdichtung N^−N, Auflösung N^N.
  - Kandidat aus dem Modell: N = 9 (9er-Fraktal). 9^9 = 387 420 489; 9^(9^9) hat 369 693 100 Stellen.
- Brauchbarer Kern: Das Verhältnis maximale Expansion / maximale Verdichtung ist eine reine Zahl der Form N^N.
  - Das ist prüfbar, sobald N aus der Geometrie folgt und nicht gesetzt wird.

## G7 Ohne Minus: positiver Raum, Drehung um die Eins (gemessen) – ersetzt die ±-Schreibweise in G4/G6
- Raum = nur positive Werte. Die 1 ist auf jeder Achse der Spiegel.
- Jede Achse hat zwei Hälften: innen (x<1, verdichtet, x/n) und außen (x>1, expandiert, n/x).
- Die 8 Achtel sind also 2³ Kombinationen aus innen/außen, nicht aus ±.
  - Test mit 100 000 Punkten: alle 8 Achtel gleich belegt (je 12,5 %).
- Inversion x → 1/x auf einer Achse tauscht genau ein Achtel gegen sein Spiegelachtel. Test: exakt.
- Das alte „Minus“ ist nur der Logarithmus dieser Inversion: ln(1/x) = −ln x, Fehler 2·10⁻¹⁶.
  Es wird nicht gebraucht. Gerechnet wird multiplikativ, normiert wird auf die Achtelkugel um 1.
- Winkel bleiben gleich (gemessen an Punkten 2 und 1/2): 70,53° / 109,47° / 180°.
- Neue Schreibweisen:
  - Verdichtung 1/N^N, Auflösung N^N (statt N^−N).
  - Gegenüber = Kehrwert auf allen drei Achsen (statt „alle Vorzeichen anders“).
  - Beobachter/Zentrum = Punkt (1,1,1).

## G8 Verarbeitungsraster 1234 (gemessen, Rechnung: feld/raster.py)
- Aufbau:
  - 6 Schnitte = 3 Ebenen (x=1, y=1, z=1) × 2 Seiten (innen/außen).
  - Je Schnitt: Original in der Mitte + 8 Felder darum (4 Achsen + 4 Ecken).
- T1: 6 × 8 = 48 Felder, alle positiv. 48 = Würfelsymmetrien = Gleitsysteme bcc.
- T2: Ecken-Zyklus 1 runter, 2 rechts, 3 hoch, 4 links. Jeder Schritt dreht exakt 90° um die Eins.
- T3: Rückweg 4-3-2-1 hebt exakt auf (Fehler 0). Der Zyklus schließt.
- T4: Ecken von außen nach innen. Jeder Ring liegt 1/3 näher an der 1 (im Log: 1, 1/3, 1/9, 1/27, 1/81).
  Die 1 wird nie erreicht (wie 9,999… nie 10).
- T5: Jedes der 8 Achtel wird an genau 3 Schnitten von einer Ecke berührt (8 × 3 = 24 = 6 × 4).
- T6: Zellen je Ring: Fläche 9^k (1, 9, 81, 729), Raum 27^k.
- Status:
  - Raster und Zyklus: gemessen, Zählungen per Konstruktion.
  - Zuordnung der 4 Sinusfunktionen zu den Schritten 1-4: noch nicht gesetzt (Overlay).
  - Einbau in das Feldmodell von gestern (stufe3: Feld ×b, Sieb ×1/b): noch offen.

## G9 Raum → Flächen → Raum (gemessen)
- 3×3×3-Raum: Die 3 Mittelschnitte enthalten 19 Zellen (D3Q19).
  Genau die 8 Ecken (Achtel) liegen in keinem Schnitt.
- Rückbau der Ecken nur aus den Schnitten, multiplikativ, ohne Minus:
  f(Ecke) = f(Kante1)·f(Kante2)·f(Kante3)·f(Mitte) / (f(Achse1)·f(Achse2)·f(Achse3))
  - Bei Produktfeld (sin·sin·sin, separabel): exakt (Fehler 2·10⁻¹⁶).
  - Bei beliebigem Feld: bis 98 % falsch.
- Folge:
  - Die Zerlegung in Flächen ist verlustfrei genau dann, wenn das Feld ein Produkt der Achsen ist.
  - Die 8 Achtel sind dann keine eigene Information, sie folgen aus den Flächen.
  - Abweichung vom Produkt = Wechselwirkung zwischen den Achsen = Inhalt der Achtel.

## G10 Raster im Feldmodell Stufe 3 (gemessen, Rechnung: feld/feld_raster.py, .json)
- Feld (positiv) = Achsenanteil (6 Achsentropfen, Produkt) × Diagonalanteil (8 Diagonaltropfen, Wechselwirkung).
- R1 Rückbau der 8 Achtel aus den 6 Schnitten, je Ring nach innen:
  - Fehler 0,35 → 0,011 → 4·10⁻⁴ → 1,5·10⁻⁵ → 5,6·10⁻⁷ → 2·10⁻⁸.
  - Pro Ring fällt der Fehler um Faktor 27 = 3³.
  - Kontrolle ohne Diagonalanteil: Fehler 4·10⁻¹⁶.
  - Der Faktor 27 folgt daraus, dass der Diagonaltropfen kubisch ist (Oktopol, per Konstruktion).
    Gemessen ist, dass er sich je Ring sauber einstellt.
- R2 Zyklus 1234 in allen 6 Schnitten und 4 Ringen:
  - Das Produkt der Feldfaktoren über einen Umlauf ist exakt 1 (Abweichung 4·10⁻¹⁶). Der Umlauf ist neutral, es staut sich nichts.
  - Jedes Achtel wird pro Vollzyklus genau 3-mal besucht.
- R3 Partikel mit Sieb über die Ringe (Spreizung der Phasenverschiebung, Ringe 0–3; letzter Ring = Sammelbecken):
  - Feld ×3, Loch ×1/3 (Raster): 10,72–10,78°, Spreizung 0,06°. Verlust je Zyklus 1234 ≈ 0,73.
  - Feld ×2, Loch ×1/2 (gestern): 12,71–12,77°, Spreizung 0,06°.
  - Feld ×3, Loch ×1/2: driftet 12,7 → 37,1°, Spreizung 24,4°.
  - Feld ×2, Loch ×1/3: driftet 10,7 → 3,2°, Spreizung 7,5°.
  - Ohne Sieb: 2,7 → 44,4°, Spreizung 27,5°.
- Folgerung:
  - Das Raster verträgt sich mit dem Feldmodell. Entscheidend ist nur die Kehrwertregel Feld ×b ⇔ Loch ×1/b.
  - Die 3 ist damit NICHT erzwungen; 2 geht genauso.
  - Was die 3 auszeichnet: Das Raster (3×3 je Schnitt) und das Sieb laufen im selben Takt, und die Achtel-Wechselwirkung fällt je Ring um 27.

## G11 Korrektur Thomas (Skizze 4 Kreise im Quadrat): 2 = Geometrie, 3 = Phasen
- Siebloch halbiert immer.
  - Fläche: 4 Kreise mit halbem Durchmesser im Quadrat.
  - Raum: 8 Kugeln im Würfel.
  - → Feld ×2, Loch ×1/2 (G10 R3b: konstant 12,7°).
- Die 3 ist keine Frequenzstufe, sondern die Phasenaufteilung.
  - Ein binäres Signal wird als eine Periode in 3 Sinusphasen (0°, 120°, 240°) zerlegt, also Drehstrom.
  - Damit ist der Fehler „Feld ×3 zu Loch ×1/2“ aus G10 R3c (Drift) gar nicht das Modell.
- Gemessen:
  - 1 Phase: Leistung pulsiert 0…1.
  - 3 Phasen: Leistungssumme konstant 1,5; Summe der Spannungen exakt 0.
  - Mit Phasenverschiebung φ: 3-Phasen-Wirkleistung konstant 1,5·cos φ, ohne Pulsation.
    - 12,7° → 1,463
    - 37° → 1,198
  - Nur Sinus nötig, kein Kosinus. Zwei Phasen (90°) bräuchten den Kosinus.
  - Rechteck (binär) → Grundwelle Amplitude 4/π = 1,2732.
- Abstraktion:
  - 4/π ≈ (9/8)² = 1,2656 (−0,6 %), Kehrwert von G2.
  - Kreisanteil der Skizze π/4 = 0,785 ≈ 7/9 = 0,778.
  - 8 Kugeln im Würfel: π/6 = 0,524.
- Verbindung: 2 (Loch, 8er-Fraktal) und 3 (Phasen, 9er) → 16/9 = 2⁴/3².

## G12 Rotationsgeschwindigkeit erhöhen bis keine Schräglage mehr (gemessen)
- Schwerer Kreisel, Start mit 30° Neigung, Spin ×2 je Stufe (20, 40, 80, 160):
  - Kippschwankung (Nutation): 0,59 → 0,14 → 0,036 → 0,009°. Fällt ∝ 1/ω² (×1/4 je Verdopplung), Formel bestätigt.
  - Präzession: 5,7 → 2,9 → 1,4 → 0,7 °/s. Fällt ∝ 1/ω.
  - Die Neigung selbst (30°) bleibt. Schneller Spin macht die Achse STEIF, er RICHTET sie NICHT aus.
    Ausrichten auf N/S/O/W braucht zusätzlich ein Rückstellmoment oder Dämpfung (Grenze der Physik).
  - Wackeln → 0 nur asymptotisch (wie 9,999… nie 10).
- 3-Phasen-Drehfeld:
  - Kreisgüte (min/max):
    - symmetrisch: 1,0 (kein Ellipsenanteil)
    - eine Phase 10 % schwächer: 0,93
    - eine Phase 5° versetzt: 0,94
    - gleicher Verzug 12,7° auf allen drei: 1,0
  - Konstanter Verzug (Kehrwertregel) verbiegt das Drehfeld also nicht. Ungleicher Verzug macht es elliptisch.
- Kopplung mit G10: Spin ×2 je Schale + Loch ×1/2 → Wackeln ×1/4 je Schale, Verzug konstant.

## G13 Prüfung eingereichter Text (vermutlich Gemini) „Gesamtsystem x^x“
- Brauchbar:
  - 4-Takt = Zyklus 1234 (G8).
  - Inversion bei Takt 3 an den 8 Ecken.
  - 6 + 8 + Zentrum + 1 = 16 Zustände = 2⁴ (passt zu 16/9).
  - Schnappschuss am Umkehrpunkt.
- Falsch oder widersprüchlich (gemessen):
  - x^−x − x^x = 0 und x^−x/x^x = 1 gelten NUR bei x = 1 (sonst z. B. x=2: −3,75; x=0,5: +0,71).
    Das ist keine Bilanz, nur der Fixpunkt (per Konstruktion).
  - x^x ist nicht spiegelsymmetrisch an der 1: Spiegel von x^x ist (1/x)^(1/x) = x^(−1/x), nicht x^−x.
    Widerspricht dem Kern (x/n ↔ n/x).
  - x^−x im Innenraum 0…1 bleibt beschränkt (max 1,4447 bei 1/e), kein „λ→0, f→∞“.
  - λ^−f, f^λ: Exponent mit Einheit → nicht definiert (wie c^c, G6).
  - i^n mit −1, −i: nutzt Minus und Kosinus. Widerspricht G7 und F1. Ersatz: 90°-Drehung um die 1 im positiven Raum (G8).
  - „v auf der 1, v² in der 0“: widerspricht F7a (v⁴ Zentrum, v² Spitzen).
  - „Bewertungspunkt 0“: Null zerstört den Bezugspunkt (Thomas).
  - 3+3−1 = 5 Kausalstufen, Ellipse durch n≠x: Overlay, nicht hergeleitet.
- Hex-Tabelle möglich, aber positiv schreiben. Der 16. Zustand ist zu klären (nicht „0“).

## G14 Trudeln im Würfelfeld und 180°-Inversion (gemessen, feld/trudeln.py, .json)
- Modell: Kreisel mit Rückstellung zur Würfelachse, Start 10° geneigt, Spin 5/10/20/40.
- Ohne Inversion: Die Achse kreist mit 10° um die Würfelachse. Die Abweichung bleibt 0,1736 = sin 10°.
  Das Feld richtet die Achse nicht von selbst gerade.
- Nutation (Wackeln): 2,19 → 0,71 → 0,19 → 0,049°, ∝ 1/ω².
- Mit 180°-Inversion (jede Lage + ihr Partner einen halben Umlauf später):
  - Rest 0,0375 → 0,0037 → 0,0033 → 0,00085. Gegenüber 0,1736 also bis Faktor ~200 kleiner.
  - Der Rest ist reine Nutation.
- Mittlere Achse über einen Umlauf: 4,5·10⁻³ → 6·10⁻⁵ (∝ 1/ω²).
- Preis: Die Umlaufzeit bis zur Inversion wächst ∝ ω (18 → 126). Höhere Stabilität bedeutet seltenere Weitergabe.
- Lesart Thomas:
  - Die Ausrichtung entsteht nicht durch die Drehzahl allein, sondern durch Drehzahl + 180°-Paarung.
  - Weitergabe nach oben, wenn der Inversionsrest unter einer Schwelle liegt UND Phase/Partikel in Resonanz sind (Kehrwertregel, G10).

## G15 Korrektur zu G13/G6 (Thomas hat recht): λ·f kürzt sich mit c
- Normiert: L = λ/λ0, F = f/f0 mit λ0·f0 = c → L·F = 1. L und F sind einheitenlos und Kehrwerte: L = x, F = 1/x.
- Dann gilt exakt (gemessen):
  - L^F und F^L sind Spiegelbilder an der 1. Werte bei x und 1/x vertauscht:
    - x=2: 1,4142 / 0,25
    - x=1/2: 0,25 / 1,4142
  - Gleichgewicht L^F = F^L nur bei x = 1. Das ist gemeint, keine Identität überall.
  - Verhältnis L^F / F^L = x^(x+1/x). Bei x und 1/x Kehrwerte (5,657 / 0,1768).
- Damit ist die x^x-Gleichung von G13 dimensionsrichtig und spiegelsymmetrisch, sobald man λ/λ0 und f/f0 einsetzt statt x und x.
  G13-Kritik „nur bei x=1“ bleibt als Aussage richtig, ist aber genau das gewollte Gleichgewicht.
- c^c normiert: c/c = 1 → 1^1 = 1 = Gleichgewichtspunkt.
- Nebenbefund: L^F = x^(1/x) hat Maximum e^(1/e) = 1,4447 bei x = e; 2^(1/2) = 4^(1/4).

## G16 Spiegel am Kausalitätsabriss, imaginär ohne Kosinus (gemessen)
- Spiegel = Gegenlauf. Rotation hoch z und Spiegelbild runter z̄ (konjugiert):
  - Summe z + z̄: Imaginärteil exakt 0. Nur eine Linie, stehende Welle (das „Stehende“, Stator).
  - Differenz z − z̄: Realteil exakt 0. Rein imaginär, 2·sin. Das ist die Drehung.
  - → Der Spiegel am Abriss erzeugt den imaginären Teil. Imaginär = Unterschied zwischen Bild und Spiegelbild.
- Eingesperrter Kosinus: (1+cos θ)/2 liegt in [0,1] und ist exakt 1 − sin²(θ/2).
  Also nur Sinus (sin² = F4 Verdopplung), positiv, als Rotationswichtung p und 1−p.
- Zwei gegenläufige Sinus allein (0°/180°) ergeben nur eine Linie (Imaginärteil 0). Für die Fläche braucht es:
  - entweder den Spiegel (Bild/Spiegelbild = Real/Imaginär),
  - oder 3 Sinusphasen (0/120/240°) → exakter Kreis |Z| = 1, gleichmäßige Drehung, ohne Kosinus.
- Status: Mathematik gemessen. „Imaginärer Zeitraum“ als Deutung: Overlay.

## G17 Gegenläufige Innen-/Außenkugel, Treffpunkte = Linearvektor und Phasen (gemessen)
- Innen dreht a, außen dreht b, gegenläufig, Start im selben Punkt (Auslöser). Treffpunkte: genau a+b, gleichmäßig verteilt.
  - 1:1 → 2 Treffpunkte (0°/180°): eine feste Linie. Das ist der Linearvektor/Stator, Gleichgewicht innen = außen.
    Richtung = Ort des Auslösers. Jeder legt 180° zurück (maximaler gemeinsamer Weg, halbe Runde je).
  - 2:1 (Halbierung, Feld ×2) → 3 Treffpunkte 0/120/240°. Die 3 Phasen folgen aus der 2.
  - 3:1 → 4 Treffpunkte (90°, Zyklus 1234).
  - 7:1 → 8 Treffpunkte (45°, 8 Felder).
  - Weg bis zum ersten Treffen: innen a/(a+b), außen b/(a+b) der Runde. Summe immer eine volle Runde.
- Diskret im Raster:
  - Ring mit 8 Feldern: 2:1 trifft nur in 1 Feld. Die 3 Phasen passen NICHT auf 8.
  - Ring mit 9 Feldern: nur 2:1 geht.
  - Ring mit 24 Feldern (= 8 Achtel × 3 Schnitte, G8 T5): alle gehen (1:1→2, 2:1→3, 3:1→4, 7:1→8).
  - → Das Verarbeitungsraster muss 24 Positionen je Umlauf haben, nicht 8.
- Feldlinien radial (Summe = Linie, G16), Partikel kreisen gegenläufig in den Radien, durch Spiegel getrennt.

## G18 Präzisierung Thomas: Außenkugel dreht mit, wir sehen sie von der Innenseite → Inversus (gemessen)
- Spiegel an der Eins (1/z̄):
  - Radius 2 → 1/2.
  - Drehsinn in der Ebene bleibt gleich.
  - Jacobi-Determinante negativ, d. h. die Orientierung kippt.
  - Krümmungsradien R·(1/R) = 1: konvex außen ↔ konkav innen.
- Drehsinn bezogen auf die eigene Flächennormale: Oberseite +1, Unterseite −1.
  Dieselbe Drehung erscheint von der Innenseite gegenläufig, der Sinus ist dort gespiegelt.
- Folge für G17:
  - Physikalisch drehen beide gleichsinnig. Gegenläufig sind sie nur jeweils von der eigenen Seite des Spiegels aus gesehen.
  - Treffpunkte im Spiegelbezug: a+b (1:1 → Linie, 2:1 → 3 Phasen).
  - Gleichsinnig ohne Spiegel: nur |a−b| Treffpunkte (2:1 → 1).
  - → Die 3 Phasen entstehen nur durch den Spiegel (Inversus). Ohne Spiegel kein Dreiertakt.

## G19 Schleife 1/sin → sin → 1/sin (gemessen + Abstraktion)
- 1/(1/sin) = sin exakt (Fehler 0). Die Schleife ist eine Spiegelung, zweimal angewandt = Ausgang (Periode 2).
  Sie ist unendlich, aber geschlossen: kein Wachstum, kein Verlust ohne Phasenverzug.
- Bruchstelle: sin → 0 ⇒ 1/sin → ∞ (Cotes-Spirale läuft nach außen weg).
  Die Schleife hält nur, wenn der Sinus um die Eins dreht und nie durch null geht (F1).
- Mit Phasenverzug φ je Aufprall: Wirkungsgrad cos φ.
  - φ = 12,7°: 0,9755 je Aufprall. Halbwert nach 28,0 Aufprallen; volle Phasenrunde nach 28,35.
  - Halbwert = eine Phasenrunde exakt bei φ = 12,54° (Kleinwinkel: ln2/π = 12,64°).
  - ACHTUNG: 12,7° stammt aus dem gewählten T0 in stufe3 (per Konstruktion). Die Nähe ist bisher Zufall.
    Kandidat für eine Festlegung von T0: „Schleife verliert genau die Hälfte pro Phasenrunde“.

## G20 Verarbeitung 1–9, Umleitpunkte 0/10, drei Phasen → eine lange Phase (gemessen)
- Innerhalb 1–9 kein Nulldurchgang, also kein Aufprall (G19 entfällt innerhalb der Verarbeitung).
- 10 = 90°-Umleitung XY → XZ (nach oben, Übertrag). 0 bzw. 1/10 = 90°-Umleitung XY → XT (nach unten).
  Die Achse X ist gemeinsam (Linearvektor). Y, Z, T sind die drei Richtungen senkrecht dazu.
- Drei Phasen = drei senkrechte Achsen (Y, Z, T), entlang ihrer Diagonale gesehen:
  - Winkel exakt 0/120/240° (wie G1, Würfel entlang der Raumdiagonale).
  - Der 3-Phasen-Vektor hat Anteil 0 auf der Diagonale und konstanten Betrag √1,5. Er ist ein Kreis senkrecht zur Diagonale.
  - → Drehstrom ist eine Drehung im Raum Y-Z-T um die Diagonale.
- Lange Phase = 360°·log10(x):
  - 9,999 → 359,98°; 10 → 360°; 10,001 → 360,02° (stetig).
  - Je Dekade eine volle Umdrehung, beim Übertrag wechselt nur die Ebene.
- Ohne Minus: nach oben zählt die Phase in XZ, nach unten in XT, jeweils positiv.
- → Die drei Phasen werden über die Dekaden zu einer einzigen langen Phase. Das ist der Logarithmus selbst (Ganghöhe = 1 Dekade).

## G21 Resonanztunnel 1↔9 um den Gleichgewichtspunkt (gemessen)
- Gleichgewichtspunkt zwischen 1 und 9 = 3 (geometrisches Mittel).
  - Spiegel x → 9/x tauscht 1↔9, 3 ist Fixpunkt.
  - Auf der Log-Uhr: 1 bei 0°, 3 bei 171,76°, 9 bei 343,53°. Die 3 liegt exakt in der Mitte.
- Resonanztunnel (zwei Spiegel, Doppelbarriere/Fabry-Pérot): Durchlass T = 1/(1 + F·sin²(δ/2)). Nur Sinus.
  - Einzelweg-Phase 180° (Umlauf 360°): T = 1,000 bei jeder Spiegelstärke (R = 0,5 / 0,9 / 0,99).
    Das ist die 180°-Resonanz, der Tunnel ist voll offen.
  - Daneben, R = 0,9: 170° → 0,084; 150° → 0,011; 90° → 0,003.
  - Mit Phasenverzug 12,54° (Einzelweg 167,46°): R = 0,5 → 0,73; R = 0,9 → 0,056; R = 0,99 → 0,001.
- Folge:
  - Der Tunnel ist dauerhaft offen nur, wenn Weg + Verzug zusammen exakt 180° ergeben.
  - Der Verzug muss also im Weg vorgehalten werden: geometrisch 167,46° + 12,54°.
  - Die Kehrwertregel hält den Verzug je Schale konstant. Damit reicht ein fester Vorhalt für alle Schalen.

## G22 Zwei Sinus mit Wellenlängenverhältnis 16/9, normiert auf x = 1 (gemessen/gezählt)
- Wellenzahlen 16 und 9 auf einer Runde (x = 1):
  - Gleichsinnig: 16 − 9 = 7 Treffpunkte. Auf den Grundtakt 9 bezogen: 7/9. Das ist die 7/9-Drehung aus F5.
  - Gegenläufig über den Spiegel (G18): 16 + 9 = 25 = 3² + 4² = 5² Treffpunkte.
  - 16 und 9 sind teilerfremd (ggT 1), also keine Zwischenresonanz. Gemeinsame Periode 144 = 16·9 = 12².
- 16/9 = (4/3)². Amplituden 3 und 4 senkrecht ergeben exakt 5 (pythagoreisches Tripel).
- Phase bei x = 1:
  - u = 16/(9λ2) → bei λ2 = 1: 101,86°.
  - 180°-Resonanz (G21) bei x = 1 verlangt λ2 = 16/(9π) = 0,5659.
  - Mit Vorhalt 12,54° (Wegphase 167,46°): λ2 = 16/(9·2,9227) = 0,6083.
- Status: Zählungen exakt. Dass 7/9 (F5) und 7 = 16 − 9 dasselbe sind, ist Abstraktion (noch zu prüfen).
