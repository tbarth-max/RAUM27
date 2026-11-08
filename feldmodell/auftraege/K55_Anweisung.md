# K55 – Anweisung an Antigravity (Ablauf)
Gehört zu: RAUM27_K55_Auftrag.md (v3) im selben Ordner. Abgabe in: K55/Ergebnis.

Grundregeln:
- Das Modell wird ausschließlich nach der Beschreibung in RAUM27_K55_Auftrag.md nachgebaut. Es gibt keinen Vorlagen-Code.
- Behandlung wie ein Computerspiel mit festen Regeln, ohne Anspruch auf Physik.
- Jeder Status (a–o) wird im Code aus den Zahlen berechnet. Nichts von Hand eintragen.
- Abweichungen wörtlich melden, nichts glätten. Unklare Vorgaben nicht raten, sondern die Stelle nennen.

## Phase 1 – Fehlersuche (Zeitrahmen: bis alle drei Teile einmal sauber durchgelaufen sind)
1. Reihenfolge: Teil 1 (Kern) umsetzen, ausführen, abgeben. Dann Teil 2 (Netz). Dann Teil 3 (Dauerlauf, 120 000 Takte).
2. Abgabe je Teil in K55/Ergebnis:
   - Code (eine Datei)
   - JSON mit allen Zahlen
   - Bericht mit genau diesen Zahlen
   - Laufzeit, Python- und NumPy-Version
3. Dateinamen: K55_Teil1_code.py, K55_Teil1.json, K55_Teil1_bericht.md (entsprechend Teil2, Teil3).

## Phase 2 – Dauerläufer (erst nach Freigabe durch Thomas)
4. Teil 3 ohne Takt-Ende laufen lassen.
   - Alle 1000 Takte eine Zeile anhängen an K55_Dauer_protokoll.jsonl (Felder wie in Teil 3).
   - Alle 100 000 Takte einen Zwischenstand speichern (fortsetzbar).
5. Bei Verletzung von l, m oder n: Lauf anhalten, letzten Zwischenstand und Protokoll abgeben.

## Zweitrechnung
6. Denselben Auftrag an Google AI Studio (Gemini Flash über API) geben.
   - Gemini muss den Code selbst ausführen. Schätzungen gelten nicht.
   - Abgabe ebenfalls in K55/Ergebnis mit Präfix „Gemini_“.

## Danach
7. Auswertung durch Claude (Prüfer):
   - Code lesen
   - Bericht gegen Beleg prüfen
   - prüfen, was per Konstruktion gilt
8. Erst nach bestandenem K55 folgt K56 (Weltsimulation Schritt für Schritt).
