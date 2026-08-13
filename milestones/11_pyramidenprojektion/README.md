# Meilenstein 11: Pyramidenprojektion -- Matrixanalyse

Prueft die in der unabhaengigen Bestandsaufnahme vorgeschlagene zentrale
Frage: Erzeugt die rekursive Wuerfel-Flaeche-Zentrum-Pyramide-Spiegel-
Projektion neue unabhaengige Freiheitsgrade, und taucht 16/9 = (4/3)^2
als geometrischer Skalierungsfaktor auf?

## Methode

Jeden Schritt der Kette als Matrix aufbauen, exakt den Rang, Nullraum,
Singulaerwerte und Eigenwerte bestimmen:

```
Ecke (8) -> Flaeche (6) -> Zentrum (1) -> Pyramide (6) -> Spiegel (8) -> ...
```

Zusaetzlich: multiplikative Zustaende Q_v = (4/3)^sum(v) auf die
Projektionen anwenden und Verhaeltnisse gegenueberliegender Flaechen
berechnen.

## Ergebnisse

| Frage | Antwort |
|---|---|
| Neue Freiheitsgrade durch Spiegel? | **NEIN** -- Rang bleibt 4, gleicher Unterraum wie reine Inzidenz |
| Taucht 16/9 auf? | **JA, EXAKT** -- als Zustandsverhaeltnis gegenueberliegender Flaechen |
| Taucht 4/3 auf? | Nur als Eingabe (Basisverhaeltnis r), nicht als Matrix-Quotient |
| kappa = 3/5 bestaetigt? | **JA** -- F/(F+E-V) = F/(F+Rang) = 6/10 = 3/5 |

### 16/9 = (4/3)^2 -- exakte Herleitung

Die reine Inzidenzprojektion M_FE (ohne Zentrumsbeitrag) ergibt fuer
die multiplikativen Zustaende Q_v = (4/3)^sum(v):

```
+Achse Mittelwert = (r^3 + 2r + 1/r) / 4
-Achse Mittelwert = (r + 2/r + 1/r^3) / 4
```

Exakte Bruchrechnung zeigt:
```
pos * r = neg * r^3 = (r^2 + 1)^2 / r
=> pos / neg = r^2 = (4/3)^2 = 16/9
```

Das ist eine algebraische Identitaet, die fuer jedes r > 0 gilt.
Sie folgt direkt aus der Symmetrie der Wuerfel-Inzidenz (jede +Achse-
Flaeche sieht exakt die Gegenecken der -Achse-Flaeche).

### Freiheitsgrade

Die Pyramidenprojektion (mit Zentrum als Spitze) hat Rang 4 --
identisch mit der reinen Inzidenzprojektion. Spiegel, Pyramide und
Inzidenz spannen alle denselben 4-dimensionalen Unterraum auf
(Gesamtrang gestapelt: 4). Die Rekursion erzeugt keine neue Information,
sondern projiziert dieselben 4 Freiheitsgrade auf verschiedene Skalen.

Das beantwortet die offene Frage aus der Bestandsaufnahme:

> "Sind diese Komponenten nur verschiedene Darstellungen derselben Algebra?"
> **Ja.** Gleicher Unterraum, verschiedene Skalierung.

## Ausfuehren

```
python3 milestones/11_pyramidenprojektion/run.py
```
