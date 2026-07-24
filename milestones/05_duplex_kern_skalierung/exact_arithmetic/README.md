# Meilenstein 5b: Exakte-Arithmetik-Härtung des Duplex-Kerns

Dies ist **kein eigener Zweig** und **kein neuer Befund** — es ist eine
Korrektheits-Voraussetzung für den 8↔7-Hadamard/Simplex-Kern aus
[Meilenstein 5](../README.md), bevor darauf mit Fließkomma-Rauschen
(SNR, Phasenfehler) und einem Bayes-Filter aufgesetzt wird.

## Was hier passiert

`raum27_exact_integer_protocol.py` implementiert denselben Kern
(H8 = Hadamard-Charaktertafel von (Z2)³, dieselbe Ecken-Konstruktion wie
`raum27.cube_symmetry`; B7 = 7-Vektor-Frame in R⁴) vollständig in
Integer/Rational-Arithmetik — Zähler und Nenner werden exakt mitgeführt,
nie gerundet. Ein AST-basierter Policy-Check verbietet im Quellcode
Float-Literale, echte Division sowie Importe von `math`/`numpy`/
`fractions`, damit sich kein Rundungsfehler einschleichen kann, ohne dass
er auffällt.

`raum27_app.py` verpackt das in eine `.r27`-Containerformat-CLI (`pack`/
`unpack`/`inspect`/`verify`/`selftest`) mit CRC32/SHA256-Integritätsprüfung
und einem Selftest, der die Bytepaar-Rundreise für jede eindeutige
Byte-Kombination im Testfile auditiert.

`selftest_example.json` ist ein Beispiel-Lauf (`python3 raum27_app.py
selftest --report ...`), reproduzierbar identisch über mehrere
unabhängige Ausführungen.

## Was der Selftest beweist — und was nicht

**Bewiesen (exakte Korrektheit, exhaustiv getestet):**

- Alle 256 Bytewerte × 5 Tiefen (0, 1, 2, 4, 8) × Outer- (H8) und
  Inner-Rekonstruktion (B7): 0 Fehler.
- Alle 65536 Bytepaare × Z4-Viertelfeldrotation im Duplex-Encoding: 0 Fehler.
- Tamper-Erkennung (Ein-Bit-Flip im Archiv) wird zuverlässig erkannt.
- Reproduzierbar: drei unabhängige Läufe liefern bitidentische Reports.

**Nicht bewiesen:**

- **Kein Kompressionsgewinn durch den RAUM27-Kern selbst.** Die
  Größenreduktion in `app_roundtrips` (z. B. 24576→158 Bytes) stammt
  vollständig aus Standard-zlib/RLE-Codecs. `encode_duplex`/
  `decode_duplex` laufen nur als Audit-Seitenkanal mit und tragen null
  Bytes zur Archivgröße bei.
- **Kein Vergleich gegen eine Baseline.** Es gibt bislang keine Zahl, die
  zeigt, dass der exakte Kern gegenüber Meilenstein 5's Float/Bayes-Kern
  (BER, Moden-Freigaberate, Rauschtoleranz) einen messbaren Unterschied
  macht. Ein Beweis, dass eine lineare Transformation ihre eigene
  Inverse ist, ist notwendig, aber für sich genommen kein
  Benchmark-Ergebnis — das besteht auch eine reine Identitätsabbildung.

## Offene Punkte, bevor das mehr als eine Härtung wird

1. Konkrete, falsifizierbare Behauptung formulieren: wofür soll der
   exakte Kern in Meilenstein 5 tatsächlich etwas ändern (BER,
   Fehlerkorrektur, Moden-Freigabe)?
2. Diesen exakten Kern probeweise in `run.py`s Bayes-Filter-Pfad
   einhängen und mit denselben Metriken (SNR, Cluster-Skalen) wie in
   `results/raum27_meilenstein5_skalierung.csv` gegen den bestehenden
   Float-Kern vergleichen.
3. Erst wenn dieser Vergleich eine Zahl liefert, die den Aufwand
   rechtfertigt, ist eine Beförderung zu einem eigenen Meilenstein
   sinnvoll — nicht vorher.
