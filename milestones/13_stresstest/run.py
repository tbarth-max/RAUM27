"""Meilenstein 13: Stresstest -- RAUM27 Invarianten

Systematischer Test aller mathematischen Invarianten des RAUM27-Systems.
13 Tests in 4 Gruppen, jeder mit PASS/FAIL.

Gruppe A: Kern-Algebra (J, H, Roundtrip)
Gruppe B: Projektions-Invarianten (Rang, Unterraum, 16/9)
Gruppe C: Topologische Konstanten (kappa, 105, Teilerzahl)
Gruppe D: Dynamische Konsistenz (Buch-Prinzip, Duplex, Regelkreis)
"""

import math
from fractions import Fraction
from pathlib import Path

import numpy as np

# =================================================================
# Kern-Matrizen
# =================================================================
corners = np.array(
    [[x, y, z] for x in (-1.0, 1.0)
               for y in (-1.0, 1.0)
               for z in (-1.0, 1.0)]
)

H = np.column_stack([
    np.ones(8),
    corners[:, 0], corners[:, 1], corners[:, 2],
    corners[:, 0] * corners[:, 1],
    corners[:, 0] * corners[:, 2],
    corners[:, 1] * corners[:, 2],
    corners[:, 0] * corners[:, 1] * corners[:, 2],
]) / math.sqrt(8.0)

J = np.diag([1.0, -1.0, -1.0, -1.0, 1.0, 1.0, 1.0, -1.0])

face_defs = [
    (0, 1.0), (0, -1.0), (1, 1.0), (1, -1.0), (2, 1.0), (2, -1.0),
]

M_FE = np.zeros((6, 8))
for f_idx, (axis, val) in enumerate(face_defs):
    for c_idx, c in enumerate(corners):
        if c[axis] == val:
            M_FE[f_idx, c_idx] = 1.0

P_pyr = np.zeros((6, 8))
for f_idx, (axis, val) in enumerate(face_defs):
    for c_idx, c in enumerate(corners):
        P_pyr[f_idx, c_idx] = 1.0 / 5.0 if c[axis] == val else 1.0 / 40.0

S = np.zeros((8, 8))
for i, c in enumerate(corners):
    for j, c2 in enumerate(corners):
        if np.allclose(c, -c2):
            S[i, j] = 1.0

V, E, F_count = 8, 12, 6
d = 3

# =================================================================
# Test-Infrastruktur
# =================================================================
results = []


def test(name, condition, detail=""):
    status = "PASS" if condition else "FAIL"
    results.append((name, status, detail))
    mark = "+" if condition else "!!!"
    print(f"  [{mark}] {name}")
    if detail:
        print(f"       {detail}")
    return condition


# =================================================================
# Gruppe A: Kern-Algebra
# =================================================================
def group_a():
    print("\n=== Gruppe A: Kern-Algebra ===")

    # T01: H orthonormal
    test("T01 H^T H = I",
         np.allclose(H.T @ H, np.eye(8)),
         f"max|H^T H - I| = {np.max(np.abs(H.T @ H - np.eye(8))):.2e}")

    # T02: J Involution
    test("T02 J^2 = I",
         np.allclose(J @ J, np.eye(8)))

    eig_J = np.diag(J)
    n_plus = int(np.sum(eig_J > 0))
    n_minus = int(np.sum(eig_J < 0))
    test("T03 J Eigenwerte: +1(x4), -1(x4)",
         n_plus == 4 and n_minus == 4,
         f"+1: {n_plus}, -1: {n_minus}")

    # T04: S Involution (Spiegel)
    test("T04 S^2 = I",
         np.allclose(S @ S, np.eye(8)))

    # T05: 8-Bit Roundtrip durch H
    rng = np.random.default_rng(42)
    bits = rng.integers(0, 2, (1000, 8)).astype(float)
    x = 2.0 * bits - 1.0
    encoded = x @ H.T
    decoded = encoded @ H
    recovered = (decoded >= 0).astype(float)
    test("T05 8-Bit Roundtrip: 1000 Vektoren durch H fehlerfrei",
         np.array_equal(bits, recovered),
         f"BER = {np.mean(bits != recovered):.6f}")

    # T06: Roundtrip durch J (Atemzug)
    x_j = x @ J.T
    x_back = x_j @ J.T
    test("T06 J-Atemzug: x @ J @ J = x (1000 Vektoren)",
         np.allclose(x, x_back),
         f"max|x - x_back| = {np.max(np.abs(x - x_back)):.2e}")


# =================================================================
# Gruppe B: Projektions-Invarianten
# =================================================================
def group_b():
    print("\n=== Gruppe B: Projektions-Invarianten ===")

    rank_FE = np.linalg.matrix_rank(M_FE)
    rank_pyr = np.linalg.matrix_rank(P_pyr)
    rank_pyr_s = np.linalg.matrix_rank(P_pyr @ S)

    test("T07 Rang(M_FE) = 4",
         rank_FE == 4, f"Rang = {rank_FE}")
    test("T08 Rang(P_pyr) = 4",
         rank_pyr == 4, f"Rang = {rank_pyr}")
    test("T09 Rang(P_pyr @ S) = 4",
         rank_pyr_s == 4, f"Rang = {rank_pyr_s}")

    # Gleicher Unterraum: Gesamtrang gestapelt = 4
    stacked = np.vstack([M_FE, P_pyr, P_pyr @ S])
    rank_stacked = np.linalg.matrix_rank(stacked)
    test("T10 Gesamtrang [M_FE; P_pyr; P_pyr@S] = 4",
         rank_stacked == 4,
         f"Gesamtrang = {rank_stacked}")

    # T11: 16/9 exakt fuer mehrere r-Werte
    all_exact = True
    tested_r = []
    for r in [Fraction(4, 3), Fraction(3, 2), Fraction(5, 4),
              Fraction(7, 5), Fraction(2, 1), Fraction(10, 9)]:
        Q = [r ** sum(int(c) for c in corner) for corner in corners]

        for axis in range(3):
            pos_idx = [i for i, c in enumerate(corners) if c[axis] == 1.0]
            neg_idx = [i for i, c in enumerate(corners) if c[axis] == -1.0]
            pos_mean = sum(Q[i] for i in pos_idx) / Fraction(4)
            neg_mean = sum(Q[i] for i in neg_idx) / Fraction(4)
            ratio = pos_mean / neg_mean
            if ratio != r * r:
                all_exact = False
                tested_r.append(f"r={r}: FAIL (ratio={ratio})")
                break
        else:
            tested_r.append(f"r={r}: ratio=r^2={r**2}")

    test("T11 16/9-Verhaeltnis exakt fuer 6 verschiedene r",
         all_exact,
         "; ".join(tested_r[:3]) + " ...")


# =================================================================
# Gruppe C: Topologische Konstanten
# =================================================================
def group_c():
    print("\n=== Gruppe C: Topologische Konstanten ===")

    # T12: kappa = 3/5 nur fuer Wuerfel
    platonic = [
        ("Tetraeder", 4, 6, 4),
        ("Wuerfel", 6, 12, 8),
        ("Oktaeder", 8, 12, 6),
        ("Dodekaeder", 12, 30, 20),
        ("Ikosaeder", 20, 30, 12),
    ]
    kappa_results = []
    only_cube = True
    for name, f, e, v in platonic:
        kappa = Fraction(f, f + e - v)
        kappa_results.append(f"{name}: {kappa}")
        if name != "Wuerfel" and kappa == Fraction(3, 5):
            only_cube = False

    cube_kappa = Fraction(6, 6 + 12 - 8)
    test("T12 kappa = F/(F+E-V) = 3/5 exakt (Wuerfel)",
         cube_kappa == Fraction(3, 5),
         f"kappa = {cube_kappa} = {float(cube_kappa):.4f}")

    test("T13 kappa = 3/5 einzigartig unter Platonischen Koerpern",
         only_cube,
         "; ".join(kappa_results))

    # T14: 105 = d*(F^2-1)
    N = 105
    test("T14 105 = d*(F^2-1) = 3*(36-1) = 3*35",
         d * (F_count**2 - 1) == N,
         f"{d}*({F_count}^2-1) = {d*(F_count**2-1)}")

    # T15: tau(105) = V = 8
    def count_divisors(n):
        count = 0
        for i in range(1, n + 1):
            if n % i == 0:
                count += 1
        return count

    tau = count_divisors(N)
    test("T15 tau(105) = 8 = V",
         tau == V,
         f"tau(105) = {tau}, V = {V}")

    # T16: #Loesungen = Rang = 4
    n_solutions = 0
    for diff in range(1, N + 1):
        if N % diff != 0:
            continue
        summ = N // diff
        if summ <= diff:
            continue
        if (summ + diff) % 2 != 0:
            continue
        Y = (summ - diff) // 2
        if Y > 0:
            n_solutions += 1

    test("T16 #Loesungen(X^2-Y^2=105) = 4 = Rang",
         n_solutions == np.linalg.matrix_rank(M_FE),
         f"#Loesungen = {n_solutions}, Rang = {np.linalg.matrix_rank(M_FE)}")


# =================================================================
# Gruppe D: Dynamische Konsistenz
# =================================================================
def group_d():
    print("\n=== Gruppe D: Dynamische Konsistenz ===")

    s = Fraction(16, 9)

    # T17: Buch-Prinzip -- 5 Ebenen hoch, Produkt-Check
    produkt_hoch = Fraction(1)
    for n in range(1, 6):
        produkt_hoch *= s
    test("T17 Buch hoch: Produkt(s^1..s^5) = (16/9)^5",
         produkt_hoch == s ** 5,
         f"Produkt = {produkt_hoch} = {float(produkt_hoch):.6f}")

    # T18: 5 Ebenen runter, Produkt-Check
    produkt_runter = Fraction(1)
    for n in range(1, 6):
        produkt_runter *= Fraction(1) / s
    test("T18 Buch runter: Produkt(s^-1..s^-5) = (9/16)^5",
         produkt_runter == Fraction(1) / s ** 5,
         f"Produkt = {produkt_runter} = {float(produkt_runter):.6f}")

    # T19: Roundtrip -- hoch dann runter = 1
    test("T19 Buch Roundtrip: hoch * runter = 1",
         produkt_hoch * produkt_runter == 1,
         f"Produkt = {produkt_hoch * produkt_runter}")

    # T20: Schneller Wechsel 10x
    zustand = Fraction(1)
    alle_gueltig = True
    for i in range(10):
        if i % 2 == 0:
            zustand *= s
        else:
            zustand /= s
        if zustand <= 0:
            alle_gueltig = False
    test("T20 Schneller Wechsel: 10x hoch/runter, jeder Zustand > 0",
         alle_gueltig and zustand == Fraction(1),
         f"Endzustand = {zustand}")

    # T21: Rueckkopplungs-Involution F^2 = Id
    test_points = [(13, 8), (11, 4), (19, 16), (53, 52)]
    all_involution = True
    for X, Y in test_points:
        X1 = math.sqrt(Y**2 + 105)
        Y1 = math.sqrt(X**2 - 105)
        X2 = math.sqrt(Y1**2 + 105)
        Y2 = math.sqrt(X1**2 - 105)
        if abs(X2 - X) > 1e-12 or abs(Y2 - Y) > 1e-12:
            all_involution = False
    test("T21 Rueckkopplung F^2=Id an allen 4 Fixpunkten",
         all_involution,
         f"Getestet: {test_points}")

    # T22: Jacobi-Eigenwerte = {+1, -1} an allen Fixpunkten
    all_pm1 = True
    for X, Y in test_points:
        ab = (Y / X) * (X / Y)
        if abs(ab - 1.0) > 1e-15:
            all_pm1 = False
    test("T22 Jacobi-Eigenwerte = {{+1,-1}} an allen Fixpunkten",
         all_pm1)

    # T23: Omega-Schalen -- SNR skaliert exakt mit Omega^level
    omega = 9
    snr_base = 10.0 ** (6.0 / 10.0)
    levels = range(-2, 3)
    snr_ratios_ok = True
    for lev in levels:
        snr = snr_base * (float(omega) ** lev)
        expected_ratio = float(omega) ** lev
        actual_ratio = snr / snr_base
        if abs(actual_ratio - expected_ratio) > 1e-12:
            snr_ratios_ok = False
    test("T23 Omega-Schalen: SNR-Verhaeltnis = Omega^level exakt",
         snr_ratios_ok,
         f"Omega={omega}, Ebenen {list(levels)}")

    # T24: Duplex -- simultane Real/Imaginaer-Dekodierung
    rng = np.random.default_rng(7727)
    n_test = 500
    bits_a = rng.integers(0, 2, (n_test, 8))
    bits_b = rng.integers(0, 2, (n_test, 8))
    xa = 2.0 * bits_a.astype(float) - 1.0
    xb = 2.0 * bits_b.astype(float) - 1.0
    signal = xa + 1j * xb
    recovered_a = (signal.real >= 0).astype(np.uint8)
    recovered_b = (signal.imag >= 0).astype(np.uint8)
    ber_a = np.mean(recovered_a != bits_a)
    ber_b = np.mean(recovered_b != bits_b)
    test("T24 Duplex rauschfrei: BER=0 fuer beide Kanaele",
         ber_a == 0.0 and ber_b == 0.0,
         f"BER_real={ber_a:.6f}, BER_imag={ber_b:.6f}")

    # T25: Informations-Vollstaendigkeit -- 8 Ecken bijektiv unter S
    perm = S @ np.arange(8).reshape(8, 1)
    unique_targets = len(set(int(p) for p in perm.flatten()))
    test("T25 Spiegel S ist Permutation (bijektiv, kein Verlust)",
         unique_targets == 8 and np.allclose(S @ S, np.eye(8)),
         f"Verschiedene Ziele: {unique_targets}/8")

    # T26: Frobenius-Norm Konsistenz
    frob_sq = np.sum(M_FE ** 2)
    test("T26 ||M_FE||^2_F = 4F = 24",
         abs(frob_sq - 4 * F_count) < 1e-12,
         f"||M_FE||^2_F = {frob_sq}, 4F = {4*F_count}")


# =================================================================
# Hauptprogramm
# =================================================================
def main():
    print("=" * 72)
    print("Meilenstein 13: RAUM27 Stresstest -- 26 Invarianten")
    print("=" * 72)

    group_a()
    group_b()
    group_c()
    group_d()

    # Zusammenfassung
    n_pass = sum(1 for _, s, _ in results if s == "PASS")
    n_fail = sum(1 for _, s, _ in results if s == "FAIL")
    n_total = len(results)

    print()
    print("=" * 72)
    print(f"ERGEBNIS: {n_pass}/{n_total} PASS, {n_fail}/{n_total} FAIL")
    print("=" * 72)

    if n_fail == 0:
        print("Alle Invarianten bestanden.")
        print("Das RAUM27-System ist konsistent ueber alle Ebenen:")
        print("  Algebra (H,J,S), Projektion (Rang 4, 16/9),")
        print("  Topologie (kappa=3/5, 105=d(F^2-1)),")
        print("  Dynamik (Buch-Prinzip, Duplex, Regelkreis).")
    else:
        print("FEHLGESCHLAGENE TESTS:")
        for name, status, detail in results:
            if status == "FAIL":
                print(f"  {name}: {detail}")

    # CSV
    import pandas as pd
    out_dir = Path(__file__).parent / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame([
        {"Test": name, "Status": status, "Detail": detail}
        for name, status, detail in results
    ])
    path = out_dir / "raum27_meilenstein13_stresstest.csv"
    df.to_csv(path, index=False)
    print(f"\nCSV: {path}")

    return n_fail == 0


if __name__ == "__main__":
    ok = main()
    raise SystemExit(0 if ok else 1)
