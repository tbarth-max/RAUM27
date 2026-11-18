# RAUM27 – Feldmodell (Stand 08.11.2026)

Spielmodell mit festen Regeln. Kein Anspruch auf physikalische Gültigkeit.

## Inhalt
- `FESTLEGUNGEN.md`: verbindliche Regeln F1–F15.
- `FELDMODELL.md`: Arbeitsstand Abschnitt A bis BL, mit Kennzeichnung [M] gemessen, [K] per Konstruktion, [A] Abstraktion, [O] Overlay/offen.
- `GRUNDLAGE_Herleitungen.md`: ausführliche Herleitungen G1–G22 (älterer Stand, durch FELDMODELL.md abgelöst).
- `skripte/`: alle Rechnungen (Python, NumPy; teils SciPy/SymPy). Jede Datei ist eigenständig ausführbar und schreibt ihr JSON in das aktuelle Verzeichnis.
- `ergebnisse/`: die JSON-Ausgaben der Skripte.
- `sinus/`: die vier Sinusfunktionen, Ebenentest, Tropfen, Stufe 3.
- `auftraege/`: K55 (unabhängiger Nachbau, von Antigravity bestanden), Freigabe Dauerläufer, Entwurf K56.

## Hauptläufe
- `skripte/gesamt_v2.py`: Gesamttest, 13 Prüfungen.
- `skripte/dauerlauf.py`: 8+1-Zwerge, Vordruck, Boden, 3 Ressourcen, Vielentnehmer.
- `skripte/zwergvergleich.py`, `sechser.py`, `stern.py`: Versorgungsarchitektur.
