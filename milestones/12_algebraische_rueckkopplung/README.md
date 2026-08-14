# Meilenstein 12: Algebraische Rueckkopplung -- X^2 - Y^2 = 105

Prueft ob die Gleichung X^2 - Y^2 = 105 und ihre ganzzahligen
Loesungen strukturelle Verbindungen zur Wuerfelgeometrie haben.

## Kernbefund: 105 = d * (F^2 - 1) = 3 * 5 * 7

Alle drei Primfaktoren von 105 sind Wuerfel-Topologiekonstanten:

| Faktor | Bedeutung |
|--------|-----------|
| 3 | d (Raumdimension) |
| 5 | F-1 (Flaechen minus 1) |
| 7 | F+1 (Simplexzeilen: Zentrum + 6 Richtungen) |

## Ganzzahlige Loesungen

| X | Y | X+Y | X-Y | Y = Wuerfelkonstante |
|---|---|-----|-----|----------------------|
| 53 | 52 | 105 = d(F^2-1) | 1 | --- |
| 19 | 16 | 35 = F^2-1 | 3 = d | 16 = r^2 * Omega |
| 13 | 8 | 21 = d(F+1) | 5 = F-1 | **8 = V (Ecken)** |
| 11 | 4 | 15 = d(F-1) | 7 = F+1 | **4 = Rang(M_FE)** |

Die X-Werte der zwei zentralen Loesungen: X = 2F +/- 1 = {13, 11}.

### Summenidentitaeten (zentrale Loesungen)

```
X_1 + X_2 = 13 + 11 = 24 = 4F = ||M_FE||^2_F (Frobenius-Norm)
Y_1 + Y_2 =  8 +  4 = 12 = E  (Kanten)
X_1 - X_2 = 13 - 11 =  2 = chi (Euler-Charakteristik)
Y_1 - Y_2 =  8 -  4 =  4 = Rang(M_FE)
```

## Rueckkopplung als Involution

```
F(X,Y) = (sqrt(Y^2 + 105), sqrt(X^2 - 105))
F(F(X,Y)) = (X, Y)  =>  F^2 = Identitaet
```

Jacobi-Matrix an jedem Fixpunkt:
```
J_F = [[0, Y/X], [X/Y, 0]]
det = -1,  Eigenwerte = {+1, -1}
```

Gleiche Involutionsstruktur wie der Duplex-Operator J (8x8, J^2=I,
EW = {+1, -1}).

## Strahlteiler-Analogie

Auf der Diagonalen X=Y gilt X^2 - Y^2 = 0 != 105: kein Fixpunkt.
Die zwei Kanaele bleiben immer verschieden -- analog zur Trennung
von Real- und Imaginaerteil im Duplex.

## Teilerzahl-Identitaet

```
tau(105) = tau(3*5*7) = 2^3 = 8 = V (Ecken)
#Loesungen = tau(105)/2 = 4 = Rang(M_FE)
```

105 ist ungerade und quadratfrei, daher liefert jedes Faktorpaar
eine Loesung. Die Anzahl Faktorpaare = tau(N)/2.

## Bewertung

Die Zerlegung 105 = d(F-1)(F+1) ist exakt und ausschliesslich aus
Wuerfel-Topologiekonstanten aufgebaut. Die Uebereinstimmungen
(Y-Werte, Summenidentitaeten, Teilerzahl, Involutionsstruktur)
sind numerisch exakt, aber nicht aus einer einzelnen gemeinsamen
Ableitung bewiesen.

## Ausfuehren

```
python3 milestones/12_algebraische_rueckkopplung/run.py
```
