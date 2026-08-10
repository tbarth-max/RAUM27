"""Meilenstein 6: Basis-9-Schalenzaehler mit Omega=k^2-Skalierung.

Erweitert den Duplex-Kern aus Meilenstein 5 um einen diskreten
Basis-9-Stellenwertzaehler ("fraktale Registrierkasse"): 9 Impulse
("Umdrehungen") pro Stelle, danach ein Uebertrag in die naechste
Stelle. Jeder Uebertrag loest einen Schalenwechsel aus, bei dem der
dimensionslose Skalierungsparameter Omega = k^2 auf das effektive
SNR der Schale wirkt (mehr Flaeche/Kapazitaet -> hoeheres
Signal-Rausch-Verhaeltnis). Der Bayes-Zustand wird dabei nicht
dupliziert, sondern fortlaufend absorbiert (bounded state, ein
einzelner mean/cov-Zustand) -- es existiert immer nur die aktuell
aktive Schale, keine parallelen Kopien frueherer Schalen.
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
OMEGA = K ** 2          # = 9: Skalierungsfaktor pro Schalenwechsel
BASE = 9                # Basis-9-Zaehler: 9 Umdrehungen pro Stelle
LEVELS = 3               # Anzahl durchlaufener Schalen (0, 1, 2)
IMPULSE_PER_LEVEL = BASE  # eine volle Stelle = 9 Impulse = 1 Uebertrag

N_CLUSTERS = 256
PHASE_ERROR_DEG = 5.0
MISSING_OUTER = 4
MISSING_INNER = 2

# ------------------------------------------------------------------
# Fixed 8 <-> 6+1 core (identisch zu Meilenstein 5)
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
    """3-stelliger Basis-9-Zaehler mit Uebertrag ('fraktale Registrierkasse')."""

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


def run_omega_schalen(k=K, levels=LEVELS, n_clusters=N_CLUSTERS, seed=SEED):
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
    for level in range(levels):
        snr_level = snr_base * (omega ** level)
        rvar_level = 0.5 / snr_level

        errors_a = errors_b = 0
        confident_wrong = 0
        released_modes = 0
        info_values = []
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

        rows.append({
            "Schale (Ebene)": level,
            "Zaehlerstand": counter.address(),
            "Uebertraege bisher": counter.level,
            "Omega^Ebene": omega ** level,
            "effektives SNR [linear]": snr_level,
            "Impulse in Schale": IMPULSE_PER_LEVEL,
            "BER Richtung A": errors_a / (n_clusters * 8 * IMPULSE_PER_LEVEL),
            "BER Richtung B": errors_b / (n_clusters * 8 * IMPULSE_PER_LEVEL),
            "BER Duplex gesamt": (errors_a + errors_b) / total_bits,
            "selbstbewusst falsche Bits": confident_wrong,
            "Freigaberate Moden [%]": 100.0 * released_modes / total_bits,
            "mittleres Informationsvolumen [bit, Gauss-Proxy]": float(
                np.mean(info_values)
            ),
        })

    return pd.DataFrame(rows)


def main():
    result = run_omega_schalen()

    out_dir = Path(__file__).parent / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "raum27_meilenstein6_omega_schalen.csv"
    result.to_csv(path, index=False)

    print(f"Basis-9-Schalenzaehler: k={K}, Omega=k^2={OMEGA}, {LEVELS} Ebenen")
    print(result.to_string(index=False))
    print(f"\nCSV: {path}")


if __name__ == "__main__":
    main()
