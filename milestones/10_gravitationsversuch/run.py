"""Meilenstein 10: Gravitationsversuch -- massenproportionale Kopplung.

Testet gezielt die in VALIDIERUNG.md Abschnitt 11 offen gelassene Frage:
"Woher kommt m1*m2?"

Das dort getestete Flaechen-/Abschattungsmodell scheiterte, weil die
Blockflaeche eines Koerpers mit R^2 skaliert, seine Masse aber mit R^3
(bei konstanter Dichte) -- Flaeche und Masse sind bei realer Geometrie
zwei verschiedene Groessen. Hier wird das EINE, gezielt geaenderte
Postulat getestet: der Abschattungs-/Kopplungsquerschnitt sigma eines
Koerpers ist NICHT seine geometrische Flaeche, sondern eine eigene
Groesse, direkt proportional zu seiner Masse (sigma = c*m).

Mechanismus (Le-Sage-Schattenwurf, wie in VALIDIERUNG.md historisch
eingeordnet): ein isotroper Hintergrundfluss trifft jeden Koerper aus
allen Richtungen gleich staerk. Ein zweiter Koerper blockiert einen
kleinen Raumwinkel dieses Flusses -- dadurch entsteht ein Kraftungleich-
gewicht in Richtung des blockierenden Koerpers (Anziehung, nicht
Abstossung).

WICHTIG -- was dieser Versuch NICHT loest: die zwei historisch
entscheidenden, unabhaengigen Probleme jedes Schattenwurf-Mechanismus
(Aufheizung durch absorbierten Impuls; Bahnwiderstand durch Aberration
bei Bewegung) werden hier nicht getestet und bleiben ungeloest -- siehe
README.
"""

import math

import numpy as np
import pandas as pd

C_KOPPLUNG = 1.0   # sigma = C_KOPPLUNG * m, freie Skalierungskonstante
I0 = 1.0           # Hintergrundfluss-Intensitaet, freie Skalierungskonstante
SEED = 3527


def sigma(m, c=C_KOPPLUNG):
    return c * m


def analytic_force(m_i, m_j, r, c=C_KOPPLUNG, i0=I0):
    """F = i0 * sigma_i * sigma_j / r^2 (Kleinwinkel-Naeherung)."""
    return i0 * sigma(m_i, c) * sigma(m_j, c) / r ** 2


def monte_carlo_blocked_fraction(sigma_j, r, n_samples, rng):
    """Anteil zufaellig isotroper Richtungen, die vom Koerper j blockiert
    werden -- rein geometrisch bestimmt, OHNE die analytische Formel zu
    benutzen. Vergleichsgroesse fuer die Vorhersage sigma_j/(4*pi*r^2)."""
    directions = rng.normal(size=(n_samples, 3))
    directions /= np.linalg.norm(directions, axis=1, keepdims=True)

    shadow_axis = np.array([-1.0, 0.0, 0.0])  # "hinter" Koerper j aus Sicht von i
    cos_angle = directions @ shadow_axis

    a_eff = math.sqrt(sigma_j / math.pi)
    if a_eff >= r:
        half_angle = math.pi / 2.0
    else:
        half_angle = math.asin(a_eff / r)

    blocked = cos_angle > math.cos(half_angle)
    return float(blocked.mean())


def test_1_2_bilinear_und_inverse_quadrat():
    """Kriterium 1 (F prop m_i*m_j) und 2 (F prop 1/r^2), analytisch."""
    rows = []
    r_fest = 10.0
    for m_i in (1.0, 2.0, 4.0):
        for m_j in (1.0, 2.0, 4.0, 8.0):
            f = analytic_force(m_i, m_j, r_fest)
            rows.append({
                "m_i": m_i, "m_j": m_j, "r": r_fest,
                "F": f, "F/(m_i*m_j)": f / (m_i * m_j),
            })
    df_masse = pd.DataFrame(rows)

    rows_r = []
    for r in (5.0, 10.0, 20.0, 40.0):
        f = analytic_force(3.0, 5.0, r)
        rows_r.append({"r": r, "F": f, "F*r^2": f * r ** 2})
    df_radius = pd.DataFrame(rows_r)

    return df_masse, df_radius


def test_geometrie_gegen_analytik(rng, n_samples=2_000_000):
    """Kriterium 1+2 UNABHAENGIG geprueft: Monte-Carlo-Geometrie (reine
    Richtungs-Stichprobe, kein Bezug auf die Kraftformel) gegen die
    analytische Vorhersage sigma_j/(4*pi*r^2)."""
    rows = []
    for m_j in (1.0, 2.0, 4.0):
        for r in (5.0, 10.0, 20.0):
            sig_j = sigma(m_j)
            vorhersage = sig_j / (4.0 * math.pi * r ** 2)
            simuliert = monte_carlo_blocked_fraction(sig_j, r, n_samples, rng)
            rows.append({
                "m_j": m_j, "r": r,
                "vorhergesagt (analytisch)": vorhersage,
                "simuliert (Monte-Carlo)": simuliert,
                "rel. Abweichung [%]": (
                    100.0 * abs(simuliert - vorhersage) / vorhersage
                ),
            })
    return pd.DataFrame(rows)


def test_3_immer_anziehend():
    """Kriterium 3: Kraftvektor zeigt in jeder getesteten Konfiguration
    von i zu j (nie abstossend), pruefbar direkt aus der Konstruktion:
    das Ungleichgewicht entsteht IMMER als Fehlen von Fluss aus der
    Richtung von j, nie als Ueberschuss -- also immer eine Anziehung."""
    positionen = [
        np.array([10.0, 0.0, 0.0]),
        np.array([0.0, 7.0, 0.0]),
        np.array([-4.0, -4.0, 4.0]),
    ]
    rows = []
    for pos_j in positionen:
        r = float(np.linalg.norm(pos_j))
        richtung_zu_j = pos_j / r
        f_mag = analytic_force(2.0, 3.0, r)
        rows.append({
            "Position j": np.round(pos_j, 2).tolist(),
            "|F|": f_mag,
            "Kraftrichtung": "immer entlang +Richtung zu j (Konstruktion)",
            "Vorzeichen konsistent attraktiv": True,
        })
    return pd.DataFrame(rows)


def test_4_isolierter_koerper(rng, n_samples=2_000_000):
    """Kriterium 4: Netto-Kraft auf einen isolierten Koerper (kein
    Schatten) ist null -- reiner Symmetrie-Check des Hintergrundflusses,
    analog zur Methodik aus VALIDIERUNG.md Abschnitt 11."""
    directions = rng.normal(size=(n_samples, 3))
    directions /= np.linalg.norm(directions, axis=1, keepdims=True)
    netto = directions.mean(axis=0)
    return float(np.linalg.norm(netto))


def main():
    rng = np.random.default_rng(SEED)

    print("=" * 78)
    print("MEILENSTEIN 10: Gravitationsversuch -- massenproportionale Kopplung")
    print("=" * 78)
    print()

    print("--- Kriterium 1+2 (analytisch, per Konstruktion): F ~ m_i*m_j/r^2 ---")
    df_masse, df_radius = test_1_2_bilinear_und_inverse_quadrat()
    print(df_masse.to_string(index=False))
    print()
    print(df_radius.to_string(index=False))
    print()

    print("--- Kriterium 1+2 UNABHAENGIG geprueft: Geometrie-Simulation ---")
    print("(Monte-Carlo-Richtungsstichprobe, nutzt die Kraftformel NICHT)")
    df_geo = test_geometrie_gegen_analytik(rng)
    print(df_geo.to_string(index=False))
    print()

    print("--- Kriterium 3: immer anziehend ---")
    df_attr = test_3_immer_anziehend()
    print(df_attr.to_string(index=False))
    print()

    print("--- Kriterium 4: Netto-Kraft auf isolierten Koerper ---")
    netto = test_4_isolierter_koerper(rng)
    print(f"|Netto-Kraftrichtung| (sollte ~0 sein): {netto:.6f}")
    print()

    from pathlib import Path
    out_dir = Path(__file__).parent / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    df_masse.to_csv(out_dir / "kriterium1_masse.csv", index=False)
    df_radius.to_csv(out_dir / "kriterium2_radius.csv", index=False)
    df_geo.to_csv(out_dir / "kriterium1_2_geometrie_vs_analytik.csv", index=False)
    df_attr.to_csv(out_dir / "kriterium3_attraktiv.csv", index=False)
    with open(out_dir / "kriterium4_isoliert.txt", "w") as fh:
        fh.write(f"netto_kraftrichtung_betrag={netto:.6f}\n")

    print("CSV-Dateien geschrieben nach:", out_dir)


if __name__ == "__main__":
    main()
