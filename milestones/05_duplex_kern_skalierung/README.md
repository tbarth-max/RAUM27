# Meilenstein 5: Skalierung des kausalen Duplex-Kerns

Full-Duplex-Übertragung über einen festen 8 <-> 6+1 Hadamard/Simplex-Kern,
verfolgt mit einem adaptiven Bayes-Filter (Präzisionsform) über eine
Folge von Impulsen, benchmarked über steigende Cluster-Zahlen.

## Ausführen

```
python3 milestones/05_duplex_kern_skalierung/run.py
```

Benötigt `numpy` und `pandas`. Das Ergebnis wird als Tabelle auf der
Konsole ausgegeben und zusätzlich unter
`milestones/05_duplex_kern_skalierung/results/raum27_meilenstein5_skalierung.csv`
gespeichert.

## Parameter

- `SNR_DB = 6.0`, `STEPS = 24` Impulse pro Lauf
- Phasenfehler zwischen den Duplex-Richtungen: `5°`
- Cluster-Skalen: `128`, `256`, `1140`
- Bit-Wechsel-Zyklus alle 3 Impulse: 1-Bit-Flip, 4-Bit-Flip, Zufallsmuster

## Metriken

Pro Skala werden u. a. BER je Richtung und gesamt, die Rate
"selbstbewusst falscher" Bits (hohe Konfidenz, aber falsch entschieden),
mittlerer lokaler Rang der Messmatrix, Informationsvolumen (Gauß-Proxy),
Freigaberate der Moden im adaptiven Filter, Kernzustand-Speicherbedarf
und Software-Durchsatz erfasst.
