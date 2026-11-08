# K56 (Entwurf, intern) – RAUM27-Welt als Langzeitsimulation, Schicht für Schicht
Voraussetzung: K55 Teil 1–3 unabhängig bestanden.
Rahmen:
- Spielwelt mit festen Regeln, so gut wie möglich innerhalb einer unperfekten Welt.
- Keine Aussage über reale Physik oder Wirtschaft.
Jede Schicht wird erst eingebaut, wenn die vorige ihren Test bestanden hat. Status im Code berechnet, Bericht = Beleg.

## S0 Kern (= K55 Teil 3)
- 6+8-Netz, 8+1 Zwerge, Vordruck, Boden, Herz.
- Test: Bilanz geschlossen, Boden nie verletzt, Erholung nach Last.

## S1 Regionen
- 216er-Blöcke (6³) = Regionen, je Region ein Zwerg der nächsten Ebene (8+1 rekursiv).
- Test: Druckdefizit je Region linear zum Regionsbedarf. Keine Region unter Boden.

## S2 Bewohner
- Jeder Knoten = Bewohner mit Grundbedarf je Ressource (Boden G) und frei wählbarem Zusatzwunsch (freier Wille, nur aus Überschuss).
- Test: Grundbedarf zu 100 % gedeckt in jedem Takt. Zusatzwünsche werden gedeckt, soweit Überschuss da ist.

## S3 Ressourcen
- R Arten, je eigener Vordruck X_r, Herz je Art.
- Test: Arten unabhängig. Entnahme einer Art verschiebt die anderen nicht (< 1e−6).

## S4 Information
- Fragen = Probesignal, Amplitude normiert, Periode trägt die Information. Antwort = Farbmuster (grün/rot/blau).
- Test: Strukturfehler 1 % wird am richtigen Ort erkannt. Kein Fehlalarm bei perfekter Struktur.

## S5 Wachstum
- Aufgaben bilden Cluster schalenweise. Breite Formen (≥ 2 Lagen).
- Test: Reichweite ∝ C^(1/3). Grundbedarf bleibt unberührt.

## S6 Ansicht
- Farbkarte je Takt als Bild/Video. Optional Weltmodell (z. B. Genie 3), falls verfügbar.
- Test: Bild aus denselben Zahlen erzeugt, keine Handbearbeitung.

## Dauerbetrieb
- Protokoll alle 1000 Takte.
- Zwischenstand alle 100 000 Takte.
- Automatischer Halt bei Verletzung von Bilanz, Boden oder Grundbedarf.
