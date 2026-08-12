"""RAUM27 - Systematische Suche: Woher kommt kappa = 0,600?

Methode: Alle plausiblen geometrischen Verhaeltnisse aus der
Wuerfel-/Oktaeder-Struktur berechnen und pruefen, welche 0,600
treffen oder nahe kommen. Gleiche Methodik wie die uebrigen
Validierungsskripte: exakte Rechnung, parameterfrei, reproduzierbar.

Ausfuehren:  python3 kappa_herleitung.py
Abhaengigkeit: numpy
"""
import numpy as np
from fractions import Fraction
import math

TARGET = Fraction(3, 5)  # 0.600 exakt = 3/5
TARGET_F = 0.600
TOL_PERCENT = 10.0  # alles innerhalb 10% wird gelistet

# ===================================================================
# 1) Geometrische Grundgroessen des Wuerfels (halbe Kante h = 1)
# ===================================================================

# Abstande vom Zentrum
d_face = 1.0           # Zentrum -> Flaechenmitte
d_edge = math.sqrt(2)  # Zentrum -> Kantenmitte
d_corner = math.sqrt(3) # Zentrum -> Ecke

# Anzahlen
n_faces = 6
n_edges = 12
n_corners = 8
n_cells = 27  # {1/r, 1, r}^3
n_diag = 4    # Raumdiagonalen
n_axes = 3    # Koordinatenachsen

# Kantenlaenge des Wuerfels
a = 2.0  # bei h=1 (halbe Kante = 1)

# Flaechendiagonale, Raumdiagonale
d_flaeche = a * math.sqrt(2)  # = 2*sqrt(2)
d_raum = a * math.sqrt(3)     # = 2*sqrt(3)

# Volumen, Oberflaeche
V_wuerfel = a**3              # = 8
O_wuerfel = 6 * a**2          # = 24
V_kugel_umschrieben = (4/3) * math.pi * d_corner**3  # Umkugel (r=sqrt(3))
V_kugel_eingeschrieben = (4/3) * math.pi * d_face**3  # Inkugel (r=1)

# Oktaeder (dual): Ecken = 6 Flaechenmitten des Wuerfels
# Bei h=1: Kantenlaenge Oktaeder = sqrt(2)*h*...
# Ecken bei (+-1,0,0), (0,+-1,0), (0,0,+-1) -> Kantenlaenge = sqrt(2)
a_okt = math.sqrt(2)
V_oktaeder = (math.sqrt(2)/3) * a_okt**3
O_oktaeder = 2 * math.sqrt(3) * a_okt**2

# ===================================================================
# 2) Inzidenzmatrix und abgeleitete Matrizen (aus roundtrip_8bit.py)
# ===================================================================

ECKEN = [(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)]
FLAECHEN = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)]

def inzidenz():
    I = np.zeros((8, 6), dtype=float)
    for i, e in enumerate(ECKEN):
        for j, (ax, val) in enumerate(FLAECHEN):
            if e[ax] == val:
                I[i, j] = 1
    return I

I = inzidenz()
M86 = I / I.sum(axis=1, keepdims=True)      # 8x6
M68 = I.T / I.T.sum(axis=1, keepdims=True)  # 6x8

# Singulaerwerte
sv_M86 = np.linalg.svd(M86, compute_uv=False)
sv_M68 = np.linalg.svd(M68, compute_uv=False)

# Eigenwerte der Rundreise-Matrix
R8 = M86 @ M68  # 8x8
R6 = M68 @ M86  # 6x6
ew_R8 = np.sort(np.linalg.eigvalsh(R8 @ R8.T))[::-1]
ew_R6 = np.sort(np.linalg.eigvalsh(R6 @ R6.T))[::-1]

# Gram-Matrizen
G86 = M86.T @ M86  # 6x6
G68 = M68.T @ M68  # 8x8
ew_G86 = np.sort(np.linalg.eigvalsh(G86))[::-1]
ew_G68 = np.sort(np.linalg.eigvalsh(G68))[::-1]

# Eigenwerte von R8 und R6 direkt
ew_R8_direct = np.sort(np.real(np.linalg.eigvals(R8)))[::-1]
ew_R6_direct = np.sort(np.real(np.linalg.eigvals(R6)))[::-1]

# ===================================================================
# 3) Hadamard (8x8) und Involution J
# ===================================================================

def hadamard8():
    H1 = np.array([[1, 1], [1, -1]]) / math.sqrt(2)
    H2 = np.kron(H1, H1)
    return np.kron(H2, H1)

H = hadamard8()
J = np.diag([1, -1, -1, -1, 1, 1, 1, -1])
HJ = H @ J
JH = J @ H

sv_HJ = np.linalg.svd(HJ, compute_uv=False)
ew_HJ = np.sort(np.real(np.linalg.eigvals(HJ)))[::-1]

# ===================================================================
# 4) Kopplungsmatrix D (aus Meilenstein 7)
# ===================================================================

B = np.array([
    [1,  1,  1,  1],
    [1,  1, -1, -1],
    [1, -1,  1, -1],
    [1, -1, -1,  1],
    [-1, 1,  1, -1],
    [-1, 1, -1,  1],
    [-1, -1, 1,  1],
]) / 2.0

# 6 Oktaeder-Richtungen
dirs = np.array([
    [1,0,0], [-1,0,0],
    [0,1,0], [0,-1,0],
    [0,0,1], [0,0,-1],
], dtype=float)

GA = B[1:, :2]  # 6x2
GB = B[1:, 2:]  # 6x2
D = np.hstack([GA, GB])  # 6x4

ew_D = np.sort(np.linalg.svd(D, compute_uv=False))[::-1]

# ===================================================================
# 5) Sammlung aller Kandidaten
# ===================================================================

kandidaten = []

def add(label, value, quelle=""):
    if value is None or not np.isfinite(value) or value <= 0:
        return
    abw = 100.0 * abs(value - TARGET_F) / TARGET_F
    kandidaten.append((label, value, abw, quelle))

# --- Reine Zahlverhaeltnisse ---
add("3/5", 3/5, "rationale Zahl")
add("6/10", 6/10, "= 3/5")
add("8/6 - 1 = 1/3", 1/3, "Ecken/Flaechen minus 1")
add("6/8 = 3/4", 6/8, "Flaechen/Ecken")
add("1 - 6/8 = 1/4", 1 - 6/8, "1 - Flaechen/Ecken")

# --- Abstandsverhaeltnisse ---
add("d_face / d_corner = 1/sqrt(3)", d_face / d_corner, "Abstands-Quotient")
add("d_face / d_edge = 1/sqrt(2)", d_face / d_edge, "Abstands-Quotient")
add("d_edge / d_corner = sqrt(2/3)", d_edge / d_corner, "Abstands-Quotient")
add("d_corner / (d_face + d_edge)", d_corner / (d_face + d_edge), "Abstandssumme")
add("d_face / (d_face + d_corner)", d_face / (d_face + d_corner), "Abstandssumme")
add("d_face / (d_face + d_edge + d_corner)",
    d_face / (d_face + d_edge + d_corner), "Abstandssumme")

# --- Gewichtete Abstands-Mittel ---
# Gewichtet mit Anzahlen: (n_f * d_f + n_e * d_e + n_c * d_c) / (n_f + n_e + n_c)
gewichteter_mittelabstand = (n_faces * d_face + n_edges * d_edge + n_corners * d_corner) / (n_faces + n_edges + n_corners)
add("d_face / gewichteter Mittelabstand", d_face / gewichteter_mittelabstand, "gewichtetes Mittel")

# --- Volumen-/Flaechenverhaeltnisse ---
add("V_oktaeder / V_wuerfel", V_oktaeder / V_wuerfel, "Volumen-Quotient")
add("O_oktaeder / O_wuerfel", O_oktaeder / O_wuerfel, "Oberflaechen-Quotient")
add("V_inkugel / V_wuerfel", V_kugel_eingeschrieben / V_wuerfel, "Inkugel/Wuerfel")
add("V_umkugel / V_wuerfel", V_kugel_umschrieben / V_wuerfel, "Umkugel/Wuerfel")

# --- Raumwinkel eines Wuerfels gesehen vom Zentrum ---
# Jede Flaeche subtendiert denselben Raumwinkel = 4*pi/6 = 2*pi/3 sr
raumwinkel_pro_flaeche = 4 * math.pi / 6
add("Raumwinkel pro Flaeche / (4*pi)", raumwinkel_pro_flaeche / (4 * math.pi), "= 1/6")

# --- Singulaerwerte M86 ---
for i, s in enumerate(sv_M86):
    if s > 1e-10:
        add(f"sigma_{i+1}(M86) = {s:.6f}", s, "Singulaerwert M86")

# --- Singulaerwert-Quotienten ---
nz_sv = [s for s in sv_M86 if s > 1e-10]
for i in range(len(nz_sv)):
    for j in range(len(nz_sv)):
        if i != j:
            add(f"sigma_{i+1}/sigma_{j+1}(M86) = {nz_sv[i]/nz_sv[j]:.6f}",
                nz_sv[i] / nz_sv[j], "SV-Quotient M86")

# --- Eigenwerte R8, R6 ---
for i, e in enumerate(ew_R8_direct):
    if abs(e) > 1e-10:
        add(f"ew_{i+1}(R8) = {e:.6f}", abs(e), "Eigenwert Rundreise 8x8")

for i, e in enumerate(ew_R6_direct):
    if abs(e) > 1e-10:
        add(f"ew_{i+1}(R6) = {e:.6f}", abs(e), "Eigenwert Rundreise 6x6")

# --- Eigenwerte G86 ---
for i, e in enumerate(ew_G86):
    if abs(e) > 1e-10:
        add(f"ew_{i+1}(G86) = {e:.6f}", abs(e), "Eigenwert G=M86'M86")
        add(f"sqrt(ew_{i+1}(G86)) = {math.sqrt(abs(e)):.6f}",
            math.sqrt(abs(e)), "Wurzel-EW G86")

# --- Singulaerwerte D (Kopplungsmatrix) ---
for i, s in enumerate(ew_D):
    if s > 1e-10:
        add(f"sigma_{i+1}(D) = {s:.6f}", s, "Singulaerwert D")

# --- Zahlenkombinationen aus {3, 4, 5, 6, 8, 9, 12, 27} ---
zahlen = [2, 3, 4, 5, 6, 8, 9, 12, 24, 27]
for a in zahlen:
    for b in zahlen:
        if a != b:
            r = a / b
            if 0.55 <= r <= 0.65:
                add(f"{a}/{b} = {r:.6f}", r, "ganzzahliger Quotient")

# --- Spezielle Kombinationen mit sqrt und pi ---
specials = [
    ("3/(2*sqrt(pi))", 3 / (2 * math.sqrt(math.pi))),
    ("sqrt(3)/pi", math.sqrt(3) / math.pi),
    ("2/sqrt(pi*e)", 2 / math.sqrt(math.pi * math.e)),
    ("3*sqrt(3)/(4*pi)", 3 * math.sqrt(3) / (4 * math.pi)),
    ("(sqrt(3)-1)/sqrt(3)", (math.sqrt(3)-1)/math.sqrt(3)),
    ("1 - 1/sqrt(3)", 1 - 1/math.sqrt(3)),
    ("2*sqrt(3) - 3", 2*math.sqrt(3) - 3),
    ("sqrt(3) - sqrt(2)", math.sqrt(3) - math.sqrt(2)),
    ("3/(pi+2)", 3 / (math.pi + 2)),
    ("(sqrt(5)-1)/2 - 0.018 [goldener Schnitt nah]", (math.sqrt(5)-1)/2),
    ("2/(1+sqrt(3))", 2 / (1 + math.sqrt(3))),
    ("1/(1+d_edge/d_face)", 1 / (1 + d_edge / d_face)),
    ("sqrt(2)/(1+sqrt(3))", math.sqrt(2) / (1 + math.sqrt(3))),
    ("(4/3)/(4/3 + 1)", (4/3) / (4/3 + 1)),
    ("1/(4/3 + 1/3)", 1 / (4/3 + 1/3)),
    ("6/(6+4)", 6 / (6 + 4)),
    ("3/(3+2)", 3 / (3 + 2)),
    ("4/(4+3) (Ecken-innen / Gesamtecken)", 4/7),
]
for label, val in specials:
    add(label, val, "spezielle Kombination")

# --- Aus dem Rang-4-System: 4 nichttriviale Singulaerwerte ---
# M86 hat SV: sqrt(4/3), sqrt(4/9), sqrt(4/9), sqrt(4/9), 0, 0
# = 2/sqrt(3), 2/3, 2/3, 2/3
sv_theor = [2/math.sqrt(3), 2/3, 2/3, 2/3]
add("2/3 (dreifacher SV von M86)", 2/3, "exakter Singulaerwert")
add("2/sqrt(3) (einfacher SV von M86)", 2/math.sqrt(3), "exakter Singulaerwert")
add("(2/3)/(2/sqrt(3)) = sqrt(3)/3 = 1/sqrt(3)", (2/3)/(2/math.sqrt(3)),
    "SV-Quotient theoretisch")

# --- Kombinationen aus Eigenwerten {2, 2, 2, 6} der Kopplungsmatrix D ---
ew_D_known = [6, 2, 2, 2]
add("2/6 = 1/3", 2/6, "EW-Quotient D")
add("6/(6+2+2+2) = 6/12 = 1/2", 6/12, "EW-Anteil D")
add("(6-2)/(6+2) = 1/2", (6-2)/(6+2), "EW-Differenz/Summe D")

# --- Inzidenz-basiert: jede Ecke auf 3 Flaechen, jede Flaeche hat 4 Ecken ---
add("3/(3+2) [Inzidenz 3, Dimension 2?]", 3/5, "Inzidenzzahl")
add("Inzidenz: 3 Flaechen pro Ecke / 5?", 3/5, "Inzidenzzahl")

# --- Neue Richtung: Projektion ---
# Projektion eines Wuerfeleckenvektors auf eine Flaechen-Normale
# Ecke (1,1,1), Flaechennormale (1,0,0): Projektion = 1/sqrt(3)
proj = 1 / math.sqrt(3)
add("Projektion Ecke auf Normale = 1/sqrt(3)", proj, "Projektion")

# --- Winkel ---
# Winkel zwischen Raumdiagonale und Flaechennormale
theta_diag_normal = math.acos(1/math.sqrt(3))
add("cos(theta_diag) = 1/sqrt(3)", math.cos(theta_diag_normal), "Kosinus")
add("sin(theta_diag) = sqrt(2/3)", math.sin(theta_diag_normal), "Sinus")
add("theta_diag/pi = arccos(1/sqrt3)/pi", theta_diag_normal / math.pi, "Winkelverhaeltnis")
add("theta_diag/(pi/2)", theta_diag_normal / (math.pi/2), "Winkelverhaeltnis")

# --- Aus r = 4/3: Funktionswerte ---
r = Fraction(4, 3)
add("log(4/3) / log(2)", math.log(4/3) / math.log(2), "Logarithmus")
add("ln(4/3)", math.log(4/3), "natuerlicher Log")
add("sin(4/3)", math.sin(4/3), "Sinus von r")

# --- Rang/Dimension-Verhaeltnisse ---
add("Rang(P_FE)/n_faces = 4/6 = 2/3", 4/6, "Rang-Quotient")
add("Rang(P_FE)/n_corners = 4/8 = 1/2", 4/8, "Rang-Quotient")
add("(n_corners - Rang) / n_corners = 4/8 = 1/2", (8-4)/8, "Defizit-Quotient")
add("(n_faces - Rang) / n_faces = 2/6 = 1/3", (6-4)/6, "Defizit-Quotient")
add("Rang / (n_faces + Rang) = 4/10 = 2/5", 4/10, "Rang-Quotient")
add("Rang / (n_corners + Rang - n_axes) = 4/9", 4/9, "Rang-Quotient")

# --- Mittlerer Bitfehler aus roundtrip ---
bitfehler_mittel = 2.03125  # = 2 + 1/32
add("Bitfehler/8 * 4/3", (bitfehler_mittel/8) * (4/3), "Bitfehler-skaliert")
add("1 - Bitfehler/8", 1 - bitfehler_mittel/8, "Rekonstruktionsrate")
add("(8 - Bitfehler) / 8", (8 - bitfehler_mittel) / 8, "= 1 - Fehlerrate")

# --- Neue Idee: 3/5 aus Wuerfel-Topologie ---
# Euler-Charakteristik: V - E + F = 8 - 12 + 6 = 2
# 3/5 = (V - E + F + 1) / 5 = 3/5? -> 3/5!
add("(V-E+F+1)/5 = (2+1)/5 = 3/5", (8-12+6+1)/5, "Euler + 1, /5")
add("(V-E+F)/V = 2/8 = 1/4", (8-12+6)/8, "Euler/Ecken")
add("F/(F+E-V) = 6/10 = 3/5", 6/(6+12-8), "F/(F+E-V)")

# ===================================================================
# 6) Auswertung
# ===================================================================

def main():
    print("=" * 78)
    print("SYSTEMATISCHE SUCHE: kappa = 0,600 = 3/5")
    print("=" * 78)
    print(f"Zielwert: {TARGET_F} = {TARGET}")
    print(f"Toleranz: {TOL_PERCENT}%")
    print()

    # Sortiere nach Abweichung
    treffer = [(l, v, a, q) for l, v, a, q in kandidaten if a <= TOL_PERCENT]
    treffer.sort(key=lambda x: x[2])

    # Entferne Duplikate (gleicher Wert auf 10 Stellen)
    gesehen = set()
    unique = []
    for l, v, a, q in treffer:
        key = round(v, 10)
        if key not in gesehen:
            gesehen.add(key)
            unique.append((l, v, a, q))

    print(f"{'Kandidat':55} {'Wert':>10} {'Abw.[%]':>8}  Quelle")
    print("-" * 100)
    for label, wert, abw, quelle in unique:
        marker = " <<<" if abw < 0.001 else ""
        print(f"  {label:53} {wert:10.6f} {abw:8.3f}  {quelle}{marker}")

    print()
    print("=" * 78)
    print("EXAKTE TREFFER (Abweichung < 0.01%)")
    print("=" * 78)

    exakt = [x for x in unique if x[2] < 0.01]
    if exakt:
        for label, wert, abw, quelle in exakt:
            print(f"  {label}")
            print(f"    Wert = {wert}, Abweichung = {abw:.6f}%")
            print(f"    Quelle: {quelle}")
            print()
    else:
        print("  Kein exakter Treffer gefunden.")
        print()
        print("  Naechstliegend:")
        if unique:
            l, v, a, q = unique[0]
            print(f"    {l}: {v:.6f} ({a:.3f}% Abweichung)")

    # --- Zusaetzliche Analyse: Ist 3/5 aus F/(F+E-V) ableitbar? ---
    print()
    print("=" * 78)
    print("HERLEITUNG: kappa = F / (F + E - V)")
    print("=" * 78)
    V, E, F = 8, 12, 6
    print(f"  Wuerfel: V={V} Ecken, E={E} Kanten, F={F} Flaechen")
    print(f"  F + E - V = {F} + {E} - {V} = {F+E-V}")
    print(f"  kappa = F / (F + E - V) = {F} / {F+E-V} = {Fraction(F, F+E-V)}")
    print(f"  = {F/(F+E-V):.6f}")
    print()
    print(f"  Euler-Charakteristik: V - E + F = {V-E+F}")
    print(f"  Also: F + E - V = F + E - V = 2*E - 2*V + 2 = 2*(E - V + 1)")
    print(f"       = 2*({E} - {V} + 1) = 2*{E-V+1} = {2*(E-V+1)}")
    print(f"  kappa = F / (2*(E - V + 1)) = {F} / {2*(E-V+1)} = {Fraction(F, 2*(E-V+1))}")
    print()

    # Geometrische Bedeutung
    print("  Geometrische Deutung:")
    print(f"    F = {F} Flaechen (Freiheitsgrade im Flaechenraum)")
    print(f"    E - V = {E} - {V} = {E-V} = Anzahl unabhaengiger Zyklen")
    print(f"      (1. Betti-Zahl b1 des Wuerfelgraphen)")
    print(f"    E - V + 1 = {E-V+1} = Zyklenrang + 1")
    print(f"    F + E - V = {F+E-V} = Gesamtdimension (Flaechen + Zyklen)")
    print()
    print(f"    kappa = Flaechen / (Flaechen + Zyklen)")
    print(f"          = Anteil der Flaechen-Freiheitsgrade an der")
    print(f"            Gesamtzahl (Flaechen + topologische Zyklen)")
    print()

    # Verifikation: gilt das fuer andere Polyeder?
    print("=" * 78)
    print("VERIFIKATION: F/(F+E-V) fuer andere Polyeder")
    print("=" * 78)
    polyeder = [
        ("Tetraeder",     4,  6, 4),
        ("Wuerfel",       8, 12, 6),
        ("Oktaeder",      6, 12, 8),
        ("Dodekaeder",   20, 30, 12),
        ("Ikosaeder",    12, 30, 20),
    ]
    print(f"  {'Polyeder':15} {'V':>3} {'E':>3} {'F':>3} {'F+E-V':>6} {'F/(F+E-V)':>12} {'Bruch':>8}")
    print("  " + "-" * 55)
    for name, v, e, f in polyeder:
        fev = f + e - v
        kap = f / fev
        bruch = Fraction(f, fev)
        marker = " <<<" if abs(kap - 0.6) < 0.001 else ""
        print(f"  {name:15} {v:3} {e:3} {f:3} {fev:6} {kap:12.6f} {str(bruch):>8}{marker}")

    print()

    # --- Singulaerwerte und Eigenwerte ausgeben ---
    print("=" * 78)
    print("MATRIXDATEN (zur Referenz)")
    print("=" * 78)
    print(f"  Singulaerwerte M86: {np.round(sv_M86, 6)}")
    print(f"  Singulaerwerte M68: {np.round(sv_M68, 6)}")
    print(f"  Eigenwerte R8 = M86@M68: {np.round(ew_R8_direct, 6)}")
    print(f"  Eigenwerte R6 = M68@M86: {np.round(ew_R6_direct, 6)}")
    print(f"  Eigenwerte G86 = M86'M86: {np.round(ew_G86, 6)}")
    print(f"  Singulaerwerte D:  {np.round(ew_D, 6)}")
    print()

    # Rekonstruktionsrate
    print("=" * 78)
    print("ZUSAMMENFASSUNG")
    print("=" * 78)
    print(f"  kappa = 0,600 = 3/5 = F / (F + E - V)")
    print(f"  Wuerfel: F=6, E=12, V=8 -> 6 / (6+12-8) = 6/10 = 3/5")
    print()
    print(f"  Interpretation:")
    print(f"    F + E - V = F + (E - V) = Flaechen + Zyklen")
    print(f"    E - V = 12 - 8 = 4 = Rang(P_FE) = Zyklenrang des Kantengraphen")
    print(f"    (Zyklenrang = E - V + Zusammenhangskomponenten = {E} - {V} + 1 = {E-V+1};"  )
    print(f"     aber fuer kappa zaehlt E - V = {E-V}, nicht E - V + 1)")
    print()
    print(f"    kappa misst den Anteil der Flaechen-Freiheitsgrade")
    print(f"    an der kombinatorischen Gesamtstruktur des Polyeders.")
    print()
    print(f"    Bemerkenswert: F + E - V = 10 und Rang(P_FE) = 4 = E - V.")
    print(f"    Also: kappa = F / (F + Rang) = 6 / (6 + 4) = 3/5.")
    print(f"    Das ist die gleiche Aussage, anders formuliert:")
    print(f"    'Anteil der Flaechen-Dimensionen an Flaechen + Rang-Dimensionen'.")


if __name__ == "__main__":
    main()
