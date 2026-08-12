"""RAUM27 - Kontrolltest: Ist die Rekonstruktion aus dem zentralen Ruecksignal
                       wuerfelspezifisch?

HINTERGRUND
-----------
Behauptung: Aus dem zentralen Ruecksignal

    y(t) = 6*x(t - 2) + 8*x(t - 2*sqrt(3))

laesst sich x(t) per Frequenzbereichs-Inversion zurueckrechnen. Gemessener
relativer RMSE: ca. 8.6e-4. Das wurde als Beleg dafuer gelesen, dass die
Wuerfelgeometrie die Rekonstruktion ermoeglicht.

KONTROLLE
---------
Dieselbe Inversion wird mit geometriefremden Verzoegerungen und Amplituden
wiederholt. Wenn diese ebenso gut oder besser rekonstruieren, geht die
Wuerfelgeometrie in das Ergebnis nicht ein.

Das ist der uebliche Kontrolltest: ein Verfahren, das mit beliebigen Werten
genauso funktioniert, belegt nichts ueber die konkret gewaehlten Werte.

ERWARTUNG BEI GUELTIGER BEHAUPTUNG
----------------------------------
Wuerfelkonfiguration deutlich besser als Kontrollkonfigurationen.

BEFUND (nachgerechnet): NEGATIV. Kontrolle B (rein willkuerliche Werte)
rekonstruiert besser als die Wuerfelkonfiguration. Siehe VALIDIERUNG.md
Abschnitt 14 fuer die Einordnung.

Ausfuehren:  python3 test_zentralinversion.py
Abhaengigkeit: numpy
"""
import numpy as np

# ---------------------------------------------------------------
# Testsignal - identisch zur urspruenglichen Rechnung
# ---------------------------------------------------------------
DT = 0.002
T_END = 30.0
LAMBDA_REG = 1e-8          # Regularisierung, rein numerisch

t = np.arange(0.0, T_END, DT)
N = len(t)
envelope = np.exp(-((t - 12.0) / 7.0) ** 2)
x = envelope * (
    0.65 * np.sin(2 * np.pi * 0.72 * t + 0.25)
    + 0.35 * np.sin(2 * np.pi * 1.31 * t - 0.70)
)

f = np.fft.rfftfreq(N, DT)
X = np.fft.rfft(x)
mask = envelope > 0.05
peak = float(np.max(np.abs(x[mask])))


def rel_rmse(a1, tau1, a2, tau2):
    """Zwei-Tap-Verzoegerungsfilter aufbauen, invertieren, Fehler messen."""
    H = a1 * np.exp(-1j * 2 * np.pi * f * tau1) \
        + a2 * np.exp(-1j * 2 * np.pi * f * tau2)
    Y = H * X                                              # Vorwaertsmodell
    X_rec = Y * np.conj(H) / (np.abs(H) ** 2 + LAMBDA_REG)  # Inversion
    x_rec = np.fft.irfft(X_rec, n=N)
    return float(np.sqrt(np.mean((x[mask] - x_rec[mask]) ** 2)) / peak)


# ---------------------------------------------------------------
# Konfigurationen
# ---------------------------------------------------------------
S3 = np.sqrt(3.0)
S2 = np.sqrt(2.0)

KONFIGURATIONEN = [
    # (Label,                                    a1, tau1,  a2, tau2,  ist_wuerfel)
    ("Wuerfel: 6 Flaechen (t=2) + 8 Ecken (t=2sqrt3)", 6, 2.0,  8, 2 * S3, True),
    ("Variante mit sqrt(2) statt sqrt(3)",             6, 2.0,  8, 2 * S2, False),
    ("Kontrolle A: willkuerlich (1, 0.70)+(1, 1.90)",  1, 0.70, 1, 1.90,  False),
    ("Kontrolle B: willkuerlich (3, 0.13)+(17, 4.77)", 3, 0.13, 17, 4.77, False),
    ("Kontrolle C: gleiche Ampl., ganzz. Delays",      5, 1.0,  5, 2.0,   False),
    ("Kontrolle D: trivial (1, 0)+(1, 1)",             1, 0.0,  1, 1.0,   False),
]


def main():
    print("=" * 72)
    print("KONTROLLTEST: Zentralsignal-Inversion")
    print("=" * 72)
    print(f"Signal: {N} Abtastwerte, dt={DT}, Regularisierung lambda={LAMBDA_REG:g}")
    print()
    print(f"  {'Konfiguration':46} {'rel. RMSE':>12}")
    print("  " + "-" * 60)

    ergebnisse = []
    for label, a1, tau1, a2, tau2, ist_wuerfel in KONFIGURATIONEN:
        r = rel_rmse(a1, tau1, a2, tau2)
        ergebnisse.append((label, r, ist_wuerfel))
        print(f"  {label:46} {r:12.3e}")

    wuerfel = [r for _, r, w in ergebnisse if w][0]
    kontrollen = [r for _, r, w in ergebnisse if not w]
    besser = sum(1 for r in kontrollen if r <= wuerfel)

    print()
    print("=" * 72)
    print("AUSWERTUNG")
    print("=" * 72)
    print(f"  Wuerfelkonfiguration:            {wuerfel:.3e}")
    print(f"  bester Kontrollwert:             {min(kontrollen):.3e}")
    print(f"  schlechtester Kontrollwert:      {max(kontrollen):.3e}")
    print(f"  Kontrollen mindestens so gut:    {besser} von {len(kontrollen)}")
    print()

    if besser > 0:
        print("  BEFUND: NEGATIV.")
        print("  Geometriefremde Verzoegerungen rekonstruieren ebenso gut")
        print("  oder besser. Die Inversion eines Zwei-Tap-Verzoegerungs-")
        print("  filters ist im rauschfreien Fall generisch moeglich.")
        print()
        print("  Die niedrige Fehlerzahl belegt daher NICHT, dass die")
        print("  Wuerfelgeometrie die Rekonstruktion ermoeglicht. Sie belegt,")
        print("  dass zwei Verzoegerungen invertierbar sind - beliebige zwei.")
    else:
        print("  BEFUND: POSITIV.")
        print("  Die Wuerfelkonfiguration ist allen Kontrollen ueberlegen.")

    # ---------------------------------------------------------------
    # Was unabhaengig davon korrekt bleibt
    # ---------------------------------------------------------------
    tau_face, tau_corner = 2.0, 2.0 * S3
    f1 = 1.0 / (tau_corner - tau_face)
    print()
    print("=" * 72)
    print("UNBERUEHRT GUELTIG")
    print("=" * 72)
    print(f"  Laufzeitdifferenz  dt = 2(sqrt3 - 1) = {tau_corner - tau_face:.9f}")
    print(f"  1. konstruktive Frequenz f1 = 1/dt   = {f1:.9f}")
    print("  (Nachgerechnet korrekt. Hoehere Ordnungen bei n*f1.)")
    print()
    print("  Geometrische Abstaende im Wuerfel (halbe Kante = 1):")
    print(f"    Zentrum -> Flaechenmitte  = 1        (6 Stueck)")
    print(f"    Zentrum -> Kantenmitte    = {S2:.6f} (12 Stueck)")
    print(f"    Zentrum -> Ecke           = {S3:.6f} (8 Stueck)")
    print("  sqrt(2) und sqrt(3) sind beide real - verschiedene Punkttypen,")
    print("  keine konkurrierenden Rechenwege fuer denselben Abstand.")


if __name__ == "__main__":
    main()
