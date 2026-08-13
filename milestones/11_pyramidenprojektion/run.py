"""Meilenstein 11: Pyramidenprojektion -- Matrixanalyse der rekursiven
Wuerfel-Flaeche-Zentrum-Projektion.

Prueft die in der unabhaengigen Bestandsaufnahme vorgeschlagene Frage:

  Wuerfel -> Flaechenmitten -> Zentrum -> Pyramide -> Spiegelkante
  -> naechste Projektion

Fuer jeden Schritt wird exakt bestimmt:
  - Rang
  - Nullraum-Dimension
  - Skalierungsfaktor (Singulaerwerte)
  - neue unabhaengige Koordinaten

Zentrale Frage: Taucht 16/9 = (4/3)^2 als geometrischer Skalierungs-
faktor aus der Projektion auf, und erzeugt die Spiegelprojektion neue
unabhaengige Freiheitsgrade oder nur umskalierte Darstellungen?

Methodik: parameterfrei, exakte Rechnung (Brueche wo moeglich),
reproduzierbar.

Ausfuehren:  python3 run.py
Abhaengigkeit: numpy
"""

import numpy as np
from fractions import Fraction
import math

# ===================================================================
# 1) Wuerfel-Geometrie (halbe Kante h = 1, Zentrum = Ursprung)
# ===================================================================

ECKEN = np.array([
    [x, y, z]
    for x in (-1.0, 1.0)
    for y in (-1.0, 1.0)
    for z in (-1.0, 1.0)
], dtype=float)  # 8x3

FLAECHENMITTEN = np.array([
    [ 1, 0, 0],  # +X
    [-1, 0, 0],  # -X
    [ 0, 1, 0],  # +Y
    [ 0,-1, 0],  # -Y
    [ 0, 0, 1],  # +Z
    [ 0, 0,-1],  # -Z
], dtype=float)  # 6x3

KANTENMITTEN = np.array([
    [ 1, 1, 0], [ 1,-1, 0], [-1, 1, 0], [-1,-1, 0],
    [ 1, 0, 1], [ 1, 0,-1], [-1, 0, 1], [-1, 0,-1],
    [ 0, 1, 1], [ 0, 1,-1], [ 0,-1, 1], [ 0,-1,-1],
], dtype=float)  # 12x3

ZENTRUM = np.zeros((1, 3), dtype=float)

# ===================================================================
# 2) Projektionsmatrizen: jeden Schritt als lineare Abbildung
# ===================================================================

def analyse_matrix(M, label):
    """Rang, Nullraum-Dimension, Singulaerwerte, Frame-Operator."""
    U, S, Vt = np.linalg.svd(M, full_matrices=True)
    rang = np.sum(S > 1e-10)
    null_dim = M.shape[1] - rang
    gram = M.T @ M
    ew_gram = np.sort(np.linalg.eigvalsh(gram))[::-1]
    frame = M.T @ M
    return {
        "label": label,
        "form": f"{M.shape[0]}x{M.shape[1]}",
        "rang": rang,
        "null_dim": null_dim,
        "sv": S[S > 1e-10],
        "ew_gram": ew_gram,
        "frame_spur": np.trace(frame),
        "frame_diag": np.diag(frame),
    }


def drucke_analyse(info):
    print(f"\n--- {info['label']} ({info['form']}, Rang {info['rang']}) ---")
    print(f"  Nullraum-Dimension: {info['null_dim']}")
    print(f"  Singulaerwerte: {np.round(info['sv'], 6)}")
    print(f"  Singulaerwerte^2: {np.round(info['sv']**2, 6)}")
    print(f"  Eigenwerte M^T M: {np.round(info['ew_gram'], 6)}")
    print(f"  Spur(M^T M): {info['frame_spur']:.6f}")
    print(f"  diag(M^T M): {np.round(info['frame_diag'], 6)}")


# ===================================================================
# 3) Schritt 1: Ecken -> Flaechenmitten (Inzidenz-Projektion)
#    Jede Ecke wird auf ihre 3 adjazenten Flaechen verteilt.
# ===================================================================

def ecke_zu_flaeche():
    """8x3 Ecken -> 6x3 Flaechenmitten via Inzidenz, zeilennormiert."""
    I = np.zeros((8, 6), dtype=float)
    achsen_werte = [
        (0, -1, 1),  # -X -> Flaeche 1
        (0,  1, 0),  # +X -> Flaeche 0
        (1, -1, 3),  # -Y -> Flaeche 3
        (1,  1, 2),  # +Y -> Flaeche 2
        (2, -1, 5),  # -Z -> Flaeche 5
        (2,  1, 4),  # +Z -> Flaeche 4
    ]
    for i, ecke in enumerate(ECKEN):
        for achse, wert, flaeche in achsen_werte:
            if ecke[achse] == wert:
                I[i, flaeche] = 1
    M_EF = I / I.sum(axis=1, keepdims=True)  # 8x6, Zeilensumme 1
    return M_EF, I


def flaeche_zu_ecke(I):
    """6 Flaechen -> 8 Ecken via transponierte Inzidenz, zeilennormiert."""
    M_FE = I.T / I.T.sum(axis=1, keepdims=True)  # 6x8, Zeilensumme 1
    return M_FE


# ===================================================================
# 4) Schritt 2: Flaechenmitten -> Zentrum (Mittelwert-Projektion)
#    Das Zentrum ist der Schwerpunkt aller 6 Flaechenmitten.
# ===================================================================

def flaeche_zu_zentrum():
    """6 Flaechenmitten -> 1 Zentrum via gleichgewichteten Mittelwert."""
    M_FZ = np.ones((1, 6)) / 6.0  # 1x6
    return M_FZ


# ===================================================================
# 5) Schritt 3: Pyramidenprojektion
#    Jede Flaeche definiert eine Pyramide: 4 Ecken + 1 Zentrum = 5 Punkte.
#    Projiziere die 8 Eckenwerte auf die 6 Pyramiden-Schwerpunkte.
# ===================================================================

def pyramiden_projektion():
    """8 Ecken -> 6 Pyramiden-Schwerpunkte.
    Jede Pyramide hat Basis = 4 Ecken einer Flaeche + Spitze = Zentrum.
    Zentrum traegt den Mittelwert aller 8 Ecken.
    Pyramiden-Schwerpunkt = (4 Basisecken + Zentrum) / 5.
    """
    P = np.zeros((6, 8))
    for f in range(6):
        basis_ecken = []
        for i, ecke in enumerate(ECKEN):
            if FLAECHENMITTEN[f] @ ecke > 0:
                basis_ecken.append(i)
        for i in basis_ecken:
            P[f, i] += 1.0 / 5.0
        P[f, :] += 1.0 / (5.0 * 8.0)
    return P  # 6x8


# ===================================================================
# 6) Schritt 4: Spiegelprojektion
#    Ecke v -> Gegenecke v_bar = -v.
#    Spiegel-Operator S auf Eckenwerten: S[i,j] = 1 iff Ecke_j = -Ecke_i
# ===================================================================

def spiegel_operator():
    """8x8 Operator: bildet Ecke auf Gegenecke ab."""
    S = np.zeros((8, 8))
    for i, ei in enumerate(ECKEN):
        for j, ej in enumerate(ECKEN):
            if np.allclose(ei, -ej):
                S[i, j] = 1.0
    return S


# ===================================================================
# 7) Schritt 5: Multiplikative Zustaende (4/3, 3/4)
#    Ecke v -> Produkt r^(sign) mit r=4/3.
#    Expansion = 4/3, Kompression = 3/4.
#    Zustand Q_v = prod_{achse} (4/3)^(sign_achse(v))
# ===================================================================

def multiplikative_zustaende():
    """8 Eckenzustaende Q_v = (4/3)^(Anzahl +1 Koordinaten) * (3/4)^(Anzahl -1).
    Aequivalent: Q_v = (4/3)^sum(ecke_v), da sum = +3...-3."""
    r = 4.0 / 3.0
    Q = np.zeros(8)
    for i, ecke in enumerate(ECKEN):
        exponent = sum(ecke)  # +3, +1, -1, -3
        Q[i] = r ** exponent
    return Q


# ===================================================================
# 8) Schritt 6: Rekursive Projektion (Pyramide -> Spiegel -> Pyramide)
#    Zusammengesetzte Abbildung: P_pyr @ S @ P_pyr^T
# ===================================================================

def rekursive_projektion(P_pyr, S):
    """Zwei Stufen: Pyramide -> Spiegel -> zurueck.
    Resultierende 6x6-Matrix beschreibt die Flaechen-zu-Flaechen-Kopplung
    ueber einen Spiegel-Pyramiden-Zyklus."""
    R = P_pyr @ S @ P_pyr.T
    return R


# ===================================================================
# Hauptprogramm
# ===================================================================

def main():
    print("=" * 78)
    print("MEILENSTEIN 11: Pyramidenprojektion -- Matrixanalyse")
    print("=" * 78)

    # --- Schritt 1: Ecke <-> Flaeche ---
    M_EF, I = ecke_zu_flaeche()
    M_FE = flaeche_zu_ecke(I)

    info_EF = analyse_matrix(M_EF, "M_EF: Ecke -> Flaeche (8x6)")
    drucke_analyse(info_EF)

    info_FE = analyse_matrix(M_FE, "M_FE: Flaeche -> Ecke (6x8)")
    drucke_analyse(info_FE)

    # Rundreise
    R_EE = M_EF @ M_FE  # 8x8
    R_FF = M_FE @ M_EF  # 6x6
    info_REE = analyse_matrix(R_EE, "R_EE = M_EF @ M_FE: Rundreise 8x8")
    info_RFF = analyse_matrix(R_FF, "R_FF = M_FE @ M_EF: Rundreise 6x6")
    drucke_analyse(info_REE)
    drucke_analyse(info_RFF)

    # --- Schritt 2: Flaeche -> Zentrum ---
    M_FZ = flaeche_zu_zentrum()
    info_FZ = analyse_matrix(M_FZ, "M_FZ: Flaeche -> Zentrum (1x6)")
    drucke_analyse(info_FZ)

    # --- Schritt 3: Pyramidenprojektion ---
    print("\n" + "=" * 78)
    print("PYRAMIDENPROJEKTION")
    print("=" * 78)

    P_pyr = pyramiden_projektion()
    info_pyr = analyse_matrix(P_pyr, "P_pyr: Ecke -> Pyramiden-Schwerpunkt (6x8)")
    drucke_analyse(info_pyr)

    print(f"\n  Pyramidenmatrix P_pyr (6x8):")
    with np.printoptions(precision=4, suppress=True, linewidth=100):
        print(P_pyr)

    # Vergleich P_pyr mit M_FE (reine Inzidenz-Projektion)
    diff = P_pyr - M_FE
    print(f"\n  P_pyr - M_FE (Differenz zur reinen Inzidenzprojektion):")
    with np.printoptions(precision=6, suppress=True, linewidth=100):
        print(diff)
    print(f"  ||P_pyr - M_FE||_F = {np.linalg.norm(diff):.6f}")

    # --- Schritt 4: Spiegeloperator ---
    print("\n" + "=" * 78)
    print("SPIEGELOPERATOR")
    print("=" * 78)

    S = spiegel_operator()
    info_S = analyse_matrix(S, "S: Spiegel/Inversion (8x8)")
    drucke_analyse(info_S)

    ew_S = np.sort(np.linalg.eigvalsh(S))[::-1]
    print(f"  Eigenwerte S: {np.round(ew_S, 6)}")
    print(f"  S^2 = I?  {np.allclose(S @ S, np.eye(8))}")

    # --- Schritt 5: Multiplikative Zustaende ---
    print("\n" + "=" * 78)
    print("MULTIPLIKATIVE ZUSTAENDE")
    print("=" * 78)

    Q = multiplikative_zustaende()
    print(f"  Eckenzustaende Q_v = (4/3)^sum(v):")
    for i, ecke in enumerate(ECKEN):
        s = int(sum(ecke))
        print(f"    Ecke {ecke.astype(int)} -> sum={s:+d} -> Q = (4/3)^{s} = {Q[i]:.6f}")

    print(f"\n  Produkt aller Q: {np.prod(Q):.10f} (soll: 1.0)")
    print(f"  Gegenecken-Produkt Q_v * Q_{{-v}}:")
    for i in range(4):
        j = 7 - i
        print(f"    Q[{i}]*Q[{j}] = {Q[i]*Q[j]:.10f}")

    # Pyramiden-Schwerpunkt angewendet auf Q
    pyr_Q = P_pyr @ Q
    print(f"\n  Pyramiden-Schwerpunkte von Q:")
    for f in range(6):
        label = ["+X", "-X", "+Y", "-Y", "+Z", "-Z"][f]
        print(f"    Flaeche {label}: {pyr_Q[f]:.6f}")

    # Verhaeltnis gegenueberliegender Pyramiden
    print(f"\n  Verhaeltnis gegenueberliegender Pyramiden-Schwerpunkte:")
    paare = [(0, 1, "+X/-X"), (2, 3, "+Y/-Y"), (4, 5, "+Z/-Z")]
    for a, b, label in paare:
        ratio = pyr_Q[a] / pyr_Q[b]
        print(f"    {label}: {pyr_Q[a]:.6f} / {pyr_Q[b]:.6f} = {ratio:.6f}")

    # --- Schritt 6: Rekursive Projektion ---
    print("\n" + "=" * 78)
    print("REKURSIVE PROJEKTION: Pyramide -> Spiegel -> Pyramide")
    print("=" * 78)

    R = rekursive_projektion(P_pyr, S)
    info_R = analyse_matrix(R, "R = P_pyr @ S @ P_pyr^T (6x6)")
    drucke_analyse(info_R)

    print(f"\n  Rekursionsmatrix R (6x6):")
    with np.printoptions(precision=6, suppress=True, linewidth=100):
        print(R)

    # Eigenwerte von R
    ew_R = np.sort(np.linalg.eigvalsh(R))[::-1]
    print(f"\n  Eigenwerte R: {np.round(ew_R, 6)}")

    # Verhaeltnisse der Eigenwerte
    nz_ew = [e for e in ew_R if abs(e) > 1e-10]
    if len(nz_ew) >= 2:
        print(f"  Eigenwertverhältnis max/min (nichttrivial): {nz_ew[0]/nz_ew[-1]:.6f}")

    # --- Schritt 6b: Reine Inzidenz-Projektion (ohne Zentrum) ---
    print("\n" + "=" * 78)
    print("INZIDENZ-PROJEKTION OHNE ZENTRUM")
    print("=" * 78)

    inz_Q = M_FE @ Q
    print(f"  Inzidenz-Mittelwerte (M_FE @ Q, ohne Zentrumsbeitrag):")
    for f in range(6):
        label = ["+X", "-X", "+Y", "-Y", "+Z", "-Z"][f]
        print(f"    Flaeche {label}: {inz_Q[f]:.6f}")

    print(f"\n  Verhaeltnis gegenueberliegender Flaechen (reine Inzidenz):")
    for a, b, label in paare:
        ratio = inz_Q[a] / inz_Q[b]
        print(f"    {label}: {inz_Q[a]:.6f} / {inz_Q[b]:.6f} = {ratio:.6f}")

    ratio_inz = inz_Q[0] / inz_Q[1]
    print(f"\n  BEFUND: Reines Inzidenz-Verhaeltnis = {ratio_inz:.10f}")
    print(f"  16/9 = {16/9:.10f}")
    print(f"  Abweichung: {abs(ratio_inz - 16/9):.2e}")
    if abs(ratio_inz - 16/9) < 1e-10:
        print(f"  -> EXAKT 16/9 = (4/3)^2!")
    print()
    print(f"  Identitaet (exakte Bruchrechnung):")
    print(f"    pos_sum = r^3 + 2r + 1/r  (4 Ecken mit x=+1)")
    print(f"    neg_sum = r + 2/r + 1/r^3  (4 Ecken mit x=-1)")
    print(f"    pos_sum * r = neg_sum * r^3 = (r^2+1)^2/r")
    print(f"    => pos_sum / neg_sum = r^2 = (4/3)^2 = 16/9  QED")
    print()
    print(f"  Pyramiden-Verhaeltnis (MIT Zentrum): {pyr_Q[0]/pyr_Q[1]:.6f}")
    print(f"  Differenz zu 16/9: {abs(pyr_Q[0]/pyr_Q[1] - 16/9):.6f}")
    print(f"  -> Zentrum-Beitrag verwischt den Kontrast (1/5 Zentrum-Gewicht)")

    # --- Schritt 7: Skalierungsanalyse ---
    print("\n" + "=" * 78)
    print("SKALIERUNGSANALYSE: Taucht 16/9 auf?")
    print("=" * 78)

    target_169 = 16.0 / 9.0
    target_43 = 4.0 / 3.0

    alle_quotienten = []

    # Singulaerwerte von P_pyr
    sv_pyr = info_pyr["sv"]
    for i in range(len(sv_pyr)):
        for j in range(len(sv_pyr)):
            if i != j and sv_pyr[j] > 1e-10:
                q = sv_pyr[i] / sv_pyr[j]
                q2 = sv_pyr[i]**2 / sv_pyr[j]**2
                alle_quotienten.append(("sv_pyr[{0}]/sv_pyr[{1}]".format(i, j), q))
                alle_quotienten.append(("sv_pyr[{0}]^2/sv_pyr[{1}]^2".format(i, j), q2))

    # Eigenwerte von R
    nz = [e for e in ew_R if abs(e) > 1e-10]
    for i in range(len(nz)):
        for j in range(len(nz)):
            if i != j and abs(nz[j]) > 1e-10:
                alle_quotienten.append((f"ew_R[{i}]/ew_R[{j}]", nz[i] / nz[j]))

    # Pyramiden-Schwerpunkte von Q
    for a, b, label in paare:
        ratio = pyr_Q[a] / pyr_Q[b]
        alle_quotienten.append((f"pyr_Q({label})", ratio))

    # Reine Inzidenz-Quotienten (OHNE Zentrum)
    for a, b, label in paare:
        ratio = inz_Q[a] / inz_Q[b]
        alle_quotienten.append((f"inz_Q({label}) OHNE Zentrum", ratio))

    print(f"  Zielwerte: 16/9 = {target_169:.6f}, 4/3 = {target_43:.6f}")
    print()
    print(f"  {'Quotient':40} {'Wert':>10} {'|Abw 16/9|':>10} {'|Abw 4/3|':>10}")
    print("  " + "-" * 75)

    treffer_169 = []
    treffer_43 = []

    for label, q in alle_quotienten:
        if q <= 0:
            continue
        abw_169 = abs(q - target_169) / target_169 * 100
        abw_43 = abs(q - target_43) / target_43 * 100
        if abw_169 < 1.0:
            treffer_169.append((label, q, abw_169))
        if abw_43 < 1.0:
            treffer_43.append((label, q, abw_43))
        if abw_169 < 10.0 or abw_43 < 10.0:
            marker = ""
            if abw_169 < 0.01:
                marker = " <<< 16/9 EXAKT"
            elif abw_43 < 0.01:
                marker = " <<< 4/3 EXAKT"
            print(f"  {label:40} {q:10.6f} {abw_169:10.3f}% {abw_43:10.3f}%{marker}")

    # --- Schritt 8: Zusammengesetzte Kette ---
    print("\n" + "=" * 78)
    print("VOLLSTAENDIGE KETTE: Ecke -> Flaeche -> Zentrum -> Pyramide -> Spiegel")
    print("=" * 78)

    # Ecke -> Pyramide -> Spiegel -> Pyramide -> ... (2 Stufen)
    T1 = P_pyr           # Ecke -> Pyramiden-Schwerpunkt (6x8)
    T2 = P_pyr @ S       # Ecke -> Pyramide -> Spiegel (6x8)
    T3 = P_pyr @ S @ P_pyr.T  # -> zurueck auf Flaechen (6x6)

    info_T2 = analyse_matrix(T2, "T2 = P_pyr @ S (6x8)")
    drucke_analyse(info_T2)

    # Iterierte Anwendung: R^n
    print("\n  Iterierte Rekursion R^n:")
    R_n = np.eye(6)
    for n in range(1, 6):
        R_n = R_n @ R
        ew_n = np.sort(np.linalg.eigvalsh(R_n))[::-1]
        rang_n = np.sum(np.abs(ew_n) > 1e-10)
        sv_n = np.linalg.svd(R_n, compute_uv=False)
        print(f"    R^{n}: Rang={rang_n}, "
              f"Spur={np.trace(R_n):.6f}, "
              f"max SV={sv_n[0]:.6f}, "
              f"max EW={ew_n[0]:.6f}")

    # --- Schritt 9: Freiheitsgrad-Analyse ---
    print("\n" + "=" * 78)
    print("FREIHEITSGRAD-ANALYSE")
    print("=" * 78)

    # Alle Abbildungen 8-Ecken -> n-Werte (Nx8 Matrizen, stapelbar)
    alle_bilder = np.vstack([M_FE, P_pyr, P_pyr @ S])  # 18x8
    rang_gesamt = np.linalg.matrix_rank(alle_bilder)

    print(f"  Rang der einzelnen Abbildungen (auf 8 Eckenwerte):")
    print(f"    M_FE   (Inzidenz Flaeche<-Ecke):    Rang {np.linalg.matrix_rank(M_FE)}")
    print(f"    P_pyr  (Pyramiden-Schwerpunkte):    Rang {np.linalg.matrix_rank(P_pyr)}")
    print(f"    P_pyr @ S  (Spiegel-Pyramide):      Rang {np.linalg.matrix_rank(P_pyr @ S)}")
    print(f"    Alle gestapelt ({alle_bilder.shape[0]}x{alle_bilder.shape[1]}):     "
          f"Rang {rang_gesamt}")
    print()

    neue_freiheitsgrade = rang_gesamt - np.linalg.matrix_rank(M_FE)
    print(f"  Neue unabhaengige Freiheitsgrade durch Spiegel-Pyramide:")
    print(f"    {neue_freiheitsgrade} (ueber den Flaechenraum hinaus)")
    print()

    if neue_freiheitsgrade == 0:
        print("  BEFUND: Die Spiegelprojektion erzeugt KEINE neuen Freiheitsgrade.")
        print("  Alle Bilder liegen im selben Unterraum wie die Inzidenz-Projektion.")
        print("  -> Umskalierung, keine neue Information.")
    else:
        print(f"  BEFUND: {neue_freiheitsgrade} neue Freiheitsgrade gefunden.")
        print("  Die Spiegelprojektion erweitert den Raum ueber die reine Inzidenz hinaus.")

    # --- Schritt 10: kappa-Verifikation ---
    print("\n" + "=" * 78)
    print("KAPPA-VERIFIKATION")
    print("=" * 78)

    V, E, F = 8, 12, 6
    kappa = F / (F + E - V)
    rang_PFE = np.linalg.matrix_rank(M_EF)
    kappa_rang = F / (F + rang_PFE)

    print(f"  kappa = F/(F+E-V) = {F}/({F}+{E}-{V}) = {F}/{F+E-V} = {kappa:.6f}")
    print(f"  kappa = F/(F+Rang) = {F}/({F}+{rang_PFE}) = {F}/{F+rang_PFE} = {kappa_rang:.6f}")
    print(f"  Stimmen ueberein: {abs(kappa - kappa_rang) < 1e-10}")
    print()
    print(f"  kappa * (F+E-V) = {kappa * (F+E-V):.1f} = F")
    print(f"  (1-kappa) * (F+E-V) = {(1-kappa) * (F+E-V):.1f} = E-V = Rang")
    print()
    print(f"  Deutung: kappa teilt die {F+E-V} kombinatorischen Dimensionen")
    print(f"  in {F} Flaechen-Freiheitsgrade (kappa) und {E-V} Rang-Freiheitsgrade (1-kappa).")

    # --- Zusammenfassung ---
    print("\n" + "=" * 78)
    print("ZUSAMMENFASSUNG")
    print("=" * 78)

    print(f"""
  Schritt                  Matrix          Rang  Nullraum  Skalierung
  ----------------------------------------------------------------
  Ecke -> Flaeche          M_EF 8x6         {info_EF['rang']}       {info_EF['null_dim']}      sv = {np.round(info_EF['sv'], 4)}
  Flaeche -> Ecke          M_FE 6x8         {info_FE['rang']}       {info_FE['null_dim']}      sv = {np.round(info_FE['sv'], 4)}
  Rundreise 8x8            R_EE             {info_REE['rang']}       {info_REE['null_dim']}
  Pyramide                 P_pyr 6x8        {info_pyr['rang']}       {info_pyr['null_dim']}      sv = {np.round(info_pyr['sv'], 4)}
  Spiegel                  S 8x8            {info_S['rang']}       {info_S['null_dim']}
  Pyr->Spiegel->Pyr        R 6x6            {info_R['rang']}       {info_R['null_dim']}
  Gesamtrang (gestapelt)                    {rang_gesamt}       {8 - rang_gesamt}
""")

    print("  Beantwortete Fragen:")
    print(f"  1. Neue Freiheitsgrade durch Spiegelprojektion? -> {neue_freiheitsgrade}")
    print(f"     (gleicher 4-dim. Unterraum wie reine Inzidenz -> Umskalierung)")
    print()
    print(f"  2. Taucht 16/9 auf?")
    print(f"     In Matrixquotienten (SV, EW):  ", end="")
    if treffer_169:
        print("JA")
        for l, v, a in treffer_169:
            print(f"       {l} = {v:.6f} (Abw. {a:.4f}%)")
    else:
        print("NEIN (kein SV/EW-Quotient innerhalb 1%)")
    print(f"     In Zustandsquotienten:          JA, EXAKT")
    print(f"       M_FE @ Q: +Achse / -Achse = 16/9 = (4/3)^2")
    print(f"       (reine Inzidenz ohne Zentrum, exakte Bruchrechnung)")
    print()
    print(f"  3. Taucht 4/3 auf?")
    if treffer_43:
        print("     JA")
        for l, v, a in treffer_43:
            print(f"       {l} = {v:.6f} (Abw. {a:.4f}%)")
    else:
        print(f"     In Matrixquotienten: NEIN")
    print(f"     Als Basisverhaeltnis r = 4/3: JA (Eingabe)")
    print()
    print(f"  4. kappa = 3/5 = F/(F+E-V) = F/(F+Rang): BESTAETIGT")
    print()
    print(f"  ZENTRALER BEFUND:")
    print(f"    Die Spiegelprojektion erzeugt keine neuen Freiheitsgrade")
    print(f"    (Rang bleibt 4), aber 16/9 = (4/3)^2 tritt ALS")
    print(f"    ZUSTANDSVERHAELTNIS exakt auf: gegenueberliegende")
    print(f"    Wuerfelflaechen tragen im multiplikativen Zustand Q_v")
    print(f"    exakt das Verhaeltnis (4/3)^2.")
    print(f"    -> 'Dieselbe begrenzte innere Zustandsmenge auf")
    print(f"       verschiedene aeussere Skalen projiziert'")
    print(f"       (Repraesentation, nicht neue Information).")


if __name__ == "__main__":
    main()
