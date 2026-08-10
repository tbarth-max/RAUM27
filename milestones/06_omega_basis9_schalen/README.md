# Meilenstein 6: Basis-9-Schalenzähler mit Ω=k²-Skalierung

Erweiterung von Meilenstein 5 um einen diskreten **Basis-9-Stellenwertzähler**
("Registrierkasse"): 9 Impulse ("Umdrehungen") pro Stelle, danach ein
Übertrag in die nächste Stelle. Jeder Übertrag löst einen **Schalenwechsel**
aus, bei dem der dimensionslose Parameter **Ω = k²** auf das effektive
SNR der neuen Schale wirkt.

## Design-Entscheidungen (aus der Diskussion)

- **k = 3, Ω = k² = 9, 3 Ebenen (0, 1, 2)** — wie besprochen.
- **Ω ist ein reiner Skalierungsfaktor, keine physikalische Größe**: keine
  Meter, Hertz oder Lichtgeschwindigkeit — nur die dimensionslosen
  Verhältnisse aus der Schalen-Geometrie (Expansion `k` ↔ Kehrwert `1/k`).
- **Überschreiben statt Parallelspeicherung**: Es existiert immer nur ein
  einziger Bayes-Zustand (`mean`, `cov`), der fortlaufend absorbiert wird —
  keine wachsende Liste vergangener Schalen. Das entspricht dem bestehenden
  Filter-Design aus Meilenstein 5 (Präzisionsform-Update statt Historie).
- **Ω wirkt auf das effektive SNR** der Schale (`SNR_Ebene = SNR_Basis · Ω^Ebene`),
  nicht auf Länge/Zeit-Einheiten — das ist die einzige Stelle im bestehenden
  Code, an der ein "Kapazität wächst mit der Fläche"-Parameter ohne
  zusätzliche physikalische Annahme sauber andockt (Shannon-Kapazität
  skaliert mit SNR).

## Was hier *nicht* behauptet wird

- Keine Aussage über Lichtgeschwindigkeit, Photonen oder reale Hardware.
- Keine Behauptung, dass π "eliminiert" wurde — der Basis-9-Zähler zählt nur
  ganze Umdrehungen; sobald eine Position innerhalb einer Teildrehung oder
  eine echte 3D-Koordinate gebraucht wird, tauchen π/√2/√3 unverändert
  wieder auf.

## Ausführen

```
python3 milestones/06_omega_basis9_schalen/run.py
```

Ergebnis wird als Tabelle ausgegeben und unter
`milestones/06_omega_basis9_schalen/results/raum27_meilenstein6_omega_schalen.csv`
gespeichert. Erwartetes Verhalten: BER fällt von Ebene zu Ebene deutlich,
weil das effektive SNR pro Übertrag um den Faktor Ω=9 steigt — das ist die
plausibilitätsprüfbare Vorhersage dieses Modells (Shannon: mehr SNR →
weniger Fehler), keine zusätzliche freie Behauptung.

## Nächste mögliche Schritte

- Vollständiger Makro-Überlauf (999 → nächste Adresse) nach 3 Stellen ×
  9 Umdrehungen = 729 Impulsen.
- Symmetrische Schalen nach innen (Brennpunkt, Ω⁻¹ statt Ω).
