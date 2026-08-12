"""
RAUM27 - 8-Bit-Rundreise-Test  8 Ecken -> 6 Flaechen -> 8 Ecken
Exakte, reproduzierbare Definition. Keine Zufallszahlen, kein Seed noetig.

Reproduziert und bestaetigt exakt die Werte aus VALIDIERUNG.md Abschnitt 2
(Theorem 18, Rang P_FE=4) und Abschnitt 3 (8-Bit-Erhaltung 8x6->6x8, FAIL,
mittlerer Bitfehler 2,03 von 8). Diese Version ist parameterfrei -- die
Inzidenzmatrix I ist exakt und deterministisch aus der Wuerfelgeometrie
konstruiert, kein Zufall/Seed noetig.

Ausfuehren:  python3 roundtrip_8bit.py
"""
import numpy as np

# ---------------------------------------------------------------
# 1) Ecken: alle 8 Kombinationen aus {0,1}^3, feste Reihenfolge
# ---------------------------------------------------------------
ECKEN = [(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)]
# Index 0..7 = (0,0,0) (0,0,1) (0,1,0) (0,1,1) (1,0,0) (1,0,1) (1,1,0) (1,1,1)

# ---------------------------------------------------------------
# 2) Flaechen: (Achse, Wert). Achse 0=X, 1=Y, 2=Z. Wert 0 oder 1.
# ---------------------------------------------------------------
FLAECHEN = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)]
# Index 0..5 = X0, X1, Y0, Y1, Z0, Z1

# ---------------------------------------------------------------
# 3) Inzidenz: Ecke e liegt auf Flaeche (ax, val)  <=>  e[ax] == val
#    Jede Ecke liegt auf genau 3 Flaechen.
# ---------------------------------------------------------------
def inzidenz():
    I = np.zeros((8, 6), dtype=int)
    for i, e in enumerate(ECKEN):
        for j, (ax, val) in enumerate(FLAECHEN):
            if e[ax] == val:
                I[i, j] = 1
    return I

I = inzidenz()
assert I.sum(axis=1).tolist() == [3]*8, "jede Ecke auf 3 Flaechen"
assert I.sum(axis=0).tolist() == [4]*6, "jede Flaeche hat 4 Ecken"

# ---------------------------------------------------------------
# 4) M86: Ecke -> Flaeche.   Zeilennormiert (Zeilensumme = 1)
#    M86[i,j] = 1/3, falls Ecke i auf Flaeche j liegt, sonst 0
# ---------------------------------------------------------------
M86 = I / I.sum(axis=1, keepdims=True)      # 8x6, Zeilensumme 1

# ---------------------------------------------------------------
# 5) M68: Flaeche -> Ecke.   Zeilennormiert (Zeilensumme = 1)
#    M68[j,i] = 1/4, falls Ecke i auf Flaeche j liegt, sonst 0
# ---------------------------------------------------------------
M68 = I.T / I.T.sum(axis=1, keepdims=True)  # 6x8, Zeilensumme 1

# ---------------------------------------------------------------
# 6) Rundreise: b (8 Bit) -> y (6 Flaechen) -> z (8 Ecken) -> Bits
#    Schwelle: Mittelwert von z  (parameterfrei)
# ---------------------------------------------------------------
def roundtrip(bits):
    b = np.asarray(bits, dtype=float)
    y = M86.T @ b          # 6 Flaechenwerte
    z = M68.T @ y          # 8 Eckenwerte
    return (z > z.mean()).astype(int)

def main():
    print("Inzidenzmatrix I (8x6):"); print(I)
    print(f"\nRang(M86) = {np.linalg.matrix_rank(M86)}")
    print(f"Rang(M68) = {np.linalg.matrix_rank(M68)}")
    R8 = M86 @ M68
    print(f"Rang(M86 @ M68) [8x8] = {np.linalg.matrix_rank(R8)}")
    sv = np.linalg.svd(M86, compute_uv=False)
    print(f"\nSingulaerwerte M86: {np.round(sv,6)}")
    ew = np.linalg.eigvalsh(M86 @ M86.T)
    print(f"Eigenwerte M86@M86^T: {np.round(np.sort(ew)[::-1],6)}")

    verteilung = {}
    fehl = 0
    for v in range(256):
        b = [(v >> k) & 1 for k in range(8)]
        rec = roundtrip(b)
        d = int(np.sum(rec != np.array(b)))
        verteilung[d] = verteilung.get(d, 0) + 1
        fehl += d
    print("\nBitfehler ueber alle 256 Muster:")
    for d in sorted(verteilung):
        print(f"  {d} Bit falsch: {verteilung[d]:3} Muster")
    print(f"Mittlerer Bitfehler: {fehl/256:.4f} von 8")

if __name__ == "__main__":
    main()
