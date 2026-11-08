# K55 – Freigabe Phase 2 (Dauerläufer)
Freigegeben durch Thomas am 08.11.2026. Prüfung Phase 1 durch Claude: Teil 1–3 bestanden.

## Was laufen soll
- Exakt der Code aus K55_Teil3_code.py (wie in Phase 1 abgegeben). Keine Änderung der Regeln.
- Ohne Takt-Ende. Die Vielentnehmer-Phasen wiederholen sich periodisch: je 120 000 Takte dasselbe Muster (Takt mod 120 000 in 20 000–39 999 oder 80 000–99 999).

## Protokoll
- Alle 1000 Takte eine Zeile anhängen an K55/Ergebnis/K55_Dauer_protokoll.jsonl. Felder:
  - takt, bedarf, verbrauch, quelle, bilanzfehler, min_p
  - knoten_unter_boden, mittleres_defizit, std_p, min_z
- Alle 100 000 Takte einen fortsetzbaren Zwischenstand speichern: p, z, Zufallszustand, Summen.
  Datei K55_Dauer_stand.npz, ältere Stände behalten: die letzten 3.
- Einmal täglich eine Kurzzusammenfassung: K55_Dauer_tag_JJJJMMTT.md, aus dem Protokoll erzeugt, keine Handwerte.

## Automatischer Halt
Anhalten und letzten Stand plus Protokoll abgeben, wenn eine dieser Bedingungen eintritt:
- |Bilanzfehler| ≥ 1e−6
- ein Knoten unter Boden (p < 0,9)
- außerhalb der Vielentnehmer-Phasen Verbrauch ≠ Bedarf (Toleranz 1e−9)
- 5000 Takte nach Phasenende ist das mittlere Defizit noch mehr als 10 % vom Wert vor der Phase entfernt

## Hinweise
- Der Bilanzfehler wächst durch Gleitkomma-Rundung langsam (Phase 1: ~3·10⁻⁸ nach 120 000 Takten).
  Bei Annäherung an 1e−6 bitte melden, nicht still neu normieren.
- Rechner und Laufzeit dürfen frei gewählt werden. Bitte Python- und NumPy-Version ins Protokoll-Kopfstück schreiben.
