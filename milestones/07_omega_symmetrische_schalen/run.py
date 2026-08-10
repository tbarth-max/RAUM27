"""Meilenstein 7: Symmetrische Schalen (Omega und Omega^-1) plus 6x8-Kopplung.

Erweitert Meilenstein 6 um symmetrische Schalen nach innen: statt nur
Ebenen 0..LEVELS_OUT (Expansion, Omega^Ebene) laufen wir jetzt durch
Ebenen -LEVELS_IN..+LEVELS_OUT. Negative Ebenen skalieren das
effektive SNR mit Omega^Ebene < 1 (also Omega^-1, Omega^-2, ...),
passend zu "Expansion k <-> Brennpunkt 1/k". Der Bayes-Zustand bleibt
ein einzelner, fortlaufend absorbierter Zustand (kein Parallelspeicher).

Zusaetzlich: der angefragte "6x8-Kraeftequivalent"-Kopplungsoperator
D zwischen den 6 Oktaeder-Richtungen (ohne Konstante) und den 8
Wuerfelecken. D wird EINMALIG numerisch geprueft (Rang, Eigenwerte)
und pro Schale nur als beschreibender Kennwert (Norm der Projektion
des aktuellen Zustands durch D) mitgeloggt -- keine neue Mechanik,
kein zusaetzlicher physikalischer Anspruch.
"""

import math
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 3527
SNR_DB_BASE = 6.0
DIFFUSE_VAR = 1e5
MODAL_Z = 3.0
CONFIDENCE_Z = 2.0

K = 3
OMEGA = K ** 2            # = 9
BASE = 9
LEVELS_OUT = 2             # Ebenen 0, 1, 2  (Omega^0, Omega^1, Omega^2)
LEVELS_IN = 2               # Ebenen -1, -2   (Omega^-1, Omega^-2)
IMPULSE_PER_LEVEL = BASE

N_CLUSTERS = 256
PHASE_ERROR_DEG = 5.0
MISSING_OUTER = 4
MISSING_INNER = 2

# ------------------------------------------------------------------
# Fixed 8 <-> 6+1 core (identisch zu Meilenstein 5/6)
# ------------------------------------------------------------------
corners = np.array(
    [[x, y, z] for x in (-1.0, 1.0)
               for y in (-1.0, 1.0)
               for z in (-1.0, 1.0)],
    dtype=float,
)

H = np.column_stack([
    np.ones(8),
    corners[:, 0],
    corners[:, 1],
    corners[:, 2],
    corners[:, 0] * corners[:, 1],
    corners[:, 0] * corners[:, 2],
    corners[:, 1] * corners[:, 2],
    corners[:, 0] * corners[:, 1] * corners[:, 2],
]) / math.sqrt(8.0)

J = np.diag([1.0, -1.0, -1.0, -1.0, 1.0, 1.0, 1.0, -1.0])

B = np.array([
    [1, 0, 0, 0],
    [1, 1, 0, 0], [1, -1, 0, 0],
    [1, 0, 1, 0], [1, 0, -1, 0],
    [1, 0, 0, 1], [1, 0, 0, -1],
], dtype=float)
B /= np.linalg.norm(B, axis=1, keepdims=True)

GA = np.array([0, 1, 2, 3])
GB = np.array([7, 4, 5, 6])
MI = np.zeros((14, 8), dtype=float)
MI[:7, GA] = B
MI[7:, GB] = B

assert np.allclose(H.T @ H, np.eye(8))
assert np.allclose(J @ J, np.eye(8))

# ------------------------------------------------------------------
# 6x8-Kopplungsmatrix D: die 6 reinen Richtungs-Zeilen von B (ohne
# die konstante erste Zeile), gleichzeitig in die GA- und GB-Spalten
# von H eingebettet. Numerisch geprueft: Rang 4 (nicht 6), von Null
# verschiedene Eigenwerte von D D^T sind {2, 2, 2, 6}.
# ------------------------------------------------------------------
B6 = B[1:]
D = np.zeros((6, 8))
D[:, GA] = B6
D[:, GB] = B6


def describe_D():
    gram = D @ D.T
    eig = np.sort(np.linalg.eigvalsh(gram))
    rank = np.linalg.matrix_rank(D)
    return rank, eig


def choose_mask(rng, n, missing):
    m = np.ones(n, dtype=bool)
    if missing:
        m[rng.choice(n, missing, replace=False)] = False
    return m


def joint_matrix(rng):
    mo = choose_mask(rng, 8, MISSING_OUTER)
    ma = choose_mask(rng, 7, MISSING_INNER)
    mb = choose_mask(rng, 7, MISSING_INNER)
    return np.vstack([H[mo], MI[np.concatenate([ma, mb])]])


def diffuse(n):
    return (
        np.zeros((n, 8), dtype=float),
        np.broadcast_to(DIFFUSE_VAR * np.eye(8), (n, 8, 8)).copy(),
    )


def posterior_from_precision(pp, pi, y, M, rvar):
    post_p = pp + (M.T @ M)[None, :, :] / rvar
    post_c = np.linalg.inv(post_p)
    info = pi + (y @ M) / rvar
    post_m = np.einsum("si,sij->sj", info, post_c)
    return post_m, post_c


def posterior(prior_mean, prior_cov, y, M, rvar):
    pp = np.linalg.inv(prior_cov)
    pi = np.einsum("si,sij->sj", prior_mean, pp)
    return posterior_from_precision(pp, pi, y, M, rvar)


def current_only(y, M, n, rvar):
    mean, cov = diffuse(n)
    return posterior(mean, cov, y, M, rvar)


def propagate(mean, cov):
    return (
        mean @ J.T,
        np.einsum("ab,sbc,cd->sad", J, cov, J.T),
    )


def adaptive_update(prior_mean, prior_cov, y, M, rvar):
    n = len(y)
    current_mean, current_cov = current_only(y, M, n, rvar)

    residual = y - prior_mean @ M.T
    innovation_cov = (
        np.einsum("ab,sbc,dc->sad", M, prior_cov, M)
        + rvar * np.eye(len(M))[None, :, :]
    )
    solved = np.linalg.solve(innovation_cov, residual[:, :, None])[:, :, 0]
    nis = np.sum(residual * solved, axis=1)
    dof = len(M)
    global_change = nis > dof + 3.0 * math.sqrt(2.0 * dof)

    diff_var = np.maximum(
        np.diagonal(prior_cov + current_cov, axis1=1, axis2=2), 1e-15,
    )
    modal = (
        np.abs(current_mean - prior_mean) / np.sqrt(diff_var) > MODAL_Z
    )
    count = modal.sum(axis=1)

    release = np.zeros((n, 8), dtype=bool)
    sparse = global_change & (count == 1)
    broad = global_change & (count != 1)
    release[sparse] = modal[sparse]
    release[broad] = True

    pp = np.linalg.inv(prior_cov)
    pi = np.einsum("si,sij->sj", prior_mean, pp)

    released_cross = release[:, :, None] | release[:, None, :]
    pp = np.where(released_cross, 0.0, pp)
    diag = np.arange(8)
    pp[:, diag, diag] = np.where(release, 1.0 / DIFFUSE_VAR, pp[:, diag, diag])
    pi = np.where(release, 0.0, pi)

    mean, cov = posterior_from_precision(pp, pi, y, M, rvar)
    return mean, cov, release


class Base9Counter:
    """3-stelliger Basis-9-Zaehler mit Uebertrag (nur Laufanzeige, kein Trigger)."""

    def __init__(self, digits=3, base=BASE):
        self.digits = [0] * digits
        self.base = base
        self.level = 0

    def tick(self):
        i = 0
        carried = False
        while i < len(self.digits):
            self.digits[i] += 1
            if self.digits[i] >= self.base:
                self.digits[i] = 0
                carried = True
                i += 1
            else:
                break
        if carried:
            self.level += 1
        return carried

    def address(self):
        return "".join(str(d) for d in reversed(self.digits))


def run_symmetric_schalen(
    k=K, levels_out=LEVELS_OUT, levels_in=LEVELS_IN,
    n_clusters=N_CLUSTERS, seed=SEED,
):
    omega = k ** 2
    snr_base = 10.0 ** (SNR_DB_BASE / 10.0)
    rng = np.random.default_rng(seed)
    bits_a = rng.integers(0, 2, (n_clusters, 8), dtype=np.uint8)
    bits_b = rng.integers(0, 2, (n_clusters, 8), dtype=np.uint8)

    mean_a, cov_a = diffuse(n_clusters)
    mean_b, cov_b = diffuse(n_clusters)

    counter = Base9Counter()
    delta = math.radians(PHASE_ERROR_DEG)

    rows = []
    step = 0
    levels = list(range(-levels_in, levels_out + 1))
    for level in levels:
        snr_level = snr_base * (float(omega) ** level)
        rvar_level = 0.5 / snr_level

        errors_a = errors_b = 0
        confident_wrong = 0
        released_modes = 0
        info_values = []
        readout_norms = []
        total_bits = n_clusters * 8 * IMPULSE_PER_LEVEL * 2

        for _ in range(IMPULSE_PER_LEVEL):
            step += 1
            counter.tick()

            xa = 2.0 * bits_a.astype(float) - 1.0
            xb = 2.0 * bits_b.astype(float) - 1.0
            xa_o = xa @ J.T if step % 2 else xa
            xb_o = xb @ J.T if step % 2 else xb

            M = joint_matrix(rng)
            gram = M.T @ M
            sign, logdet = np.linalg.slogdet(np.eye(8) + snr_level * gram)
            info_values.append(
                float(0.5 * logdet / math.log(2.0)) if sign > 0 else 0.0
            )

            signal_a = xa_o @ M.T
            signal_b = xb_o @ M.T

            y = (
                signal_a
                + np.exp(1j * (math.pi / 2.0 + delta)) * signal_b
                + rng.normal(0.0, math.sqrt(rvar_level), (n_clusters, len(M)))
                + 1j * rng.normal(0.0, math.sqrt(rvar_level), (n_clusters, len(M)))
            )

            pm_a, pc_a = propagate(mean_a, cov_a)
            pm_b, pc_b = propagate(mean_b, cov_b)

            mean_a, cov_a, rel_a = adaptive_update(pm_a, pc_a, y.real, M, rvar_level)
            mean_b, cov_b, rel_b = adaptive_update(pm_b, pc_b, y.imag, M, rvar_level)
            released_modes += int(rel_a.sum() + rel_b.sum())

            ca = mean_a @ J.T if step % 2 else mean_a
            cb = mean_b @ J.T if step % 2 else mean_b
            cova = np.einsum("ab,sbc,cd->sad", J, cov_a, J.T) if step % 2 else cov_a
            covb = np.einsum("ab,sbc,cd->sad", J, cov_b, J.T) if step % 2 else cov_b

            da = (ca >= 0).astype(np.uint8)
            db = (cb >= 0).astype(np.uint8)
            wa = da != bits_a
            wb = db != bits_b
            errors_a += int(wa.sum())
            errors_b += int(wb.sum())

            stda = np.sqrt(np.maximum(np.diagonal(cova, axis1=1, axis2=2), 1e-15))
            stdb = np.sqrt(np.maximum(np.diagonal(covb, axis1=1, axis2=2), 1e-15))
            cona = np.abs(ca) / stda >= CONFIDENCE_Z
            conb = np.abs(cb) / stdb >= CONFIDENCE_Z
            confident_wrong += int((wa & cona).sum() + (wb & conb).sum())

            readout = ca @ D.T
            readout_norms.append(float(np.mean(np.linalg.norm(readout, axis=1))))

        rows.append({
            "Ebene": level,
            "Richtung": "innen (Brennpunkt)" if level < 0 else (
                "Kern" if level == 0 else "aussen (Expansion)"
            ),
            "Zaehlerstand": counter.address(),
            "Omega^Ebene": omega ** level,
            "effektives SNR [linear]": snr_level,
            "BER Duplex gesamt": (errors_a + errors_b) / total_bits,
            "selbstbewusst falsche Bits": confident_wrong,
            "Freigaberate Moden [%]": 100.0 * released_modes / total_bits,
            "mittleres Informationsvolumen [bit, Gauss-Proxy]": float(
                np.mean(info_values)
            ),
            "6x8-Readout ||D*Zustand|| (Mittel)": float(np.mean(readout_norms)),
        })

    return pd.DataFrame(rows)


def main():
    rank, eig = describe_D()
    print("6x8-Kopplungsmatrix D (Oktaeder-Richtungen x Wuerfelecken):")
    print(f"  Rang: {rank} von 6 moeglichen Zeilen (nicht voller Rang)")
    print(f"  Eigenwerte von D D^T: {np.round(eig, 6).tolist()}")
    print(
        "  Verhaeltnis groesster/mittlerer Eigenwert: "
        f"{eig[-1] / eig[-2]:.4f} "
        "(zufaellig = k=3, siehe README -- nicht als Beleg interpretieren)"
    )
    print()

    result = run_symmetric_schalen()

    out_dir = Path(__file__).parent / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "raum27_meilenstein7_symmetrische_schalen.csv"
    result.to_csv(path, index=False)

    print(f"Symmetrische Schalen: k={K}, Omega=k^2={OMEGA}, "
          f"Ebenen -{LEVELS_IN}..+{LEVELS_OUT}")
    print(result.to_string(index=False))
    print(f"\nCSV: {path}")


if __name__ == "__main__":
    main()
