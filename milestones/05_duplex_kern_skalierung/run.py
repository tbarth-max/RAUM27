"""Meilenstein 5: Skalierung des kausalen Duplex-Kerns.

Full-duplex transmission over a fixed 8 <-> 6+1 Hadamard/simplex core,
tracked with an adaptive Bayesian (precision-form) filter across a
sequence of impulses, and benchmarked across increasing cluster counts.
"""

import math
import time
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 3527
SNR_DB = 6.0
SNR = 10.0 ** (SNR_DB / 10.0)
RVAR = 0.5 / SNR
DIFFUSE_VAR = 1e5
MODAL_Z = 3.0
CONFIDENCE_Z = 2.0

STEPS = 24
PHASE_ERROR_DEG = 5.0
MISSING_OUTER = 4
MISSING_INNER = 2
CLUSTER_COUNTS = (128, 256, 1140)

# ------------------------------------------------------------------
# Fixed 8 <-> 6+1 core
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
        np.broadcast_to(
            DIFFUSE_VAR * np.eye(8), (n, 8, 8)
        ).copy(),
    )


def posterior_from_precision(pp, pi, y, M):
    post_p = pp + (M.T @ M)[None, :, :] / RVAR
    post_c = np.linalg.inv(post_p)
    info = pi + (y @ M) / RVAR
    post_m = np.einsum("si,sij->sj", info, post_c)
    return post_m, post_c


def posterior(prior_mean, prior_cov, y, M):
    pp = np.linalg.inv(prior_cov)
    pi = np.einsum("si,sij->sj", prior_mean, pp)
    return posterior_from_precision(pp, pi, y, M)


def current_only(y, M, n):
    mean, cov = diffuse(n)
    return posterior(mean, cov, y, M)


def propagate(mean, cov):
    return (
        mean @ J.T,
        np.einsum("ab,sbc,cd->sad", J, cov, J.T),
    )


def adaptive_update(prior_mean, prior_cov, y, M):
    n = len(y)
    current_mean, current_cov = current_only(y, M, n)

    residual = y - prior_mean @ M.T
    innovation_cov = (
        np.einsum("ab,sbc,dc->sad", M, prior_cov, M)
        + RVAR * np.eye(len(M))[None, :, :]
    )
    solved = np.linalg.solve(
        innovation_cov, residual[:, :, None]
    )[:, :, 0]
    nis = np.sum(residual * solved, axis=1)
    dof = len(M)
    global_change = nis > dof + 3.0 * math.sqrt(2.0 * dof)

    diff_var = np.maximum(
        np.diagonal(
            prior_cov + current_cov,
            axis1=1,
            axis2=2,
        ),
        1e-15,
    )
    modal = (
        np.abs(current_mean - prior_mean) / np.sqrt(diff_var)
        > MODAL_Z
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
    pp[:, diag, diag] = np.where(
        release,
        1.0 / DIFFUSE_VAR,
        pp[:, diag, diag],
    )
    pi = np.where(release, 0.0, pi)

    mean, cov = posterior_from_precision(pp, pi, y, M)
    return mean, cov, release


def change_bits(rng, bits, kind):
    n = len(bits)
    out = bits.copy()
    if kind == "1":
        idx = rng.integers(0, 8, n)
        out[np.arange(n), idx] ^= 1
    elif kind == "4":
        idx = np.argpartition(
            rng.random((n, 8)), 3, axis=1
        )[:, :4]
        out[np.arange(n)[:, None], idx] ^= 1
    elif kind == "random":
        out = rng.integers(0, 2, bits.shape, dtype=np.uint8)
    return out


def run_scale(n_clusters, seed):
    rng = np.random.default_rng(seed)
    bits_a = rng.integers(
        0, 2, (n_clusters, 8), dtype=np.uint8
    )
    bits_b = rng.integers(
        0, 2, (n_clusters, 8), dtype=np.uint8
    )

    mean_a, cov_a = diffuse(n_clusters)
    mean_b, cov_b = diffuse(n_clusters)

    cycle = ("1", "4", "random")
    cycle_index = 0

    errors_a = errors_b = 0
    confident_wrong = 0
    released_modes = 0
    total_bits = n_clusters * 8 * STEPS * 2
    ranks = []
    info_values = []

    delta = math.radians(PHASE_ERROR_DEG)

    start = time.perf_counter()

    for step_index in range(STEPS):
        if step_index > 0 and step_index % 3 == 0:
            kind = cycle[cycle_index % 3]
            cycle_index += 1
            bits_a = change_bits(rng, bits_a, kind)
            bits_b = change_bits(rng, bits_b, kind)

        step = step_index + 1
        xa = 2.0 * bits_a.astype(float) - 1.0
        xb = 2.0 * bits_b.astype(float) - 1.0
        xa_o = xa @ J.T if step % 2 else xa
        xb_o = xb @ J.T if step % 2 else xb

        M = joint_matrix(rng)
        rank = np.linalg.matrix_rank(M, tol=1e-10)
        ranks.append(rank)

        gram = M.T @ M
        sign, logdet = np.linalg.slogdet(
            np.eye(8) + SNR * gram
        )
        info_values.append(
            float(0.5 * logdet / math.log(2.0))
            if sign > 0 else 0.0
        )

        signal_a = xa_o @ M.T
        signal_b = xb_o @ M.T

        y = (
            signal_a
            + np.exp(1j * (math.pi / 2.0 + delta)) * signal_b
            + rng.normal(
                0.0, math.sqrt(RVAR),
                (n_clusters, len(M)),
            )
            + 1j * rng.normal(
                0.0, math.sqrt(RVAR),
                (n_clusters, len(M)),
            )
        )

        pm_a, pc_a = propagate(mean_a, cov_a)
        pm_b, pc_b = propagate(mean_b, cov_b)

        mean_a, cov_a, rel_a = adaptive_update(
            pm_a, pc_a, y.real, M
        )
        mean_b, cov_b, rel_b = adaptive_update(
            pm_b, pc_b, y.imag, M
        )

        released_modes += int(rel_a.sum() + rel_b.sum())

        ca = mean_a @ J.T if step % 2 else mean_a
        cb = mean_b @ J.T if step % 2 else mean_b
        cova = (
            np.einsum("ab,sbc,cd->sad", J, cov_a, J.T)
            if step % 2 else cov_a
        )
        covb = (
            np.einsum("ab,sbc,cd->sad", J, cov_b, J.T)
            if step % 2 else cov_b
        )

        da = (ca >= 0).astype(np.uint8)
        db = (cb >= 0).astype(np.uint8)
        wa = da != bits_a
        wb = db != bits_b

        errors_a += int(wa.sum())
        errors_b += int(wb.sum())

        stda = np.sqrt(
            np.maximum(
                np.diagonal(cova, axis1=1, axis2=2),
                1e-15,
            )
        )
        stdb = np.sqrt(
            np.maximum(
                np.diagonal(covb, axis1=1, axis2=2),
                1e-15,
            )
        )
        cona = np.abs(ca) / stda >= CONFIDENCE_Z
        conb = np.abs(cb) / stdb >= CONFIDENCE_Z
        confident_wrong += int(
            (wa & cona).sum() + (wb & conb).sum()
        )

    elapsed = time.perf_counter() - start
    processed_bits = total_bits

    state_bytes = (
        n_clusters
        * 2
        * (8 + 8 * 8)
        * np.dtype(np.float64).itemsize
    )

    return {
        "Cluster": n_clusters,
        "Impulse": STEPS,
        "Duplex-Bits verarbeitet": processed_bits,
        "BER Richtung A": errors_a / (n_clusters * 8 * STEPS),
        "BER Richtung B": errors_b / (n_clusters * 8 * STEPS),
        "BER Duplex gesamt": (
            (errors_a + errors_b) / processed_bits
        ),
        "selbstbewusst falsche Bits": confident_wrong,
        "mittlerer lokaler Rang": float(np.mean(ranks)),
        "mittleres Informationsvolumen [bit, Gauß-Proxy]": float(
            np.mean(info_values)
        ),
        "Freigaberate Moden [%]": (
            100.0 * released_modes / processed_bits
        ),
        "Kernzustand Speicher [MiB]": (
            state_bytes / (1024.0 * 1024.0)
        ),
        "Laufzeit [s]": elapsed,
        "Software-Durchsatz [Mbit/s]": (
            processed_bits / elapsed / 1e6
        ),
    }


def main():
    # One warm-up outside the measured scales.
    _ = run_scale(32, SEED - 1)

    rows = [
        run_scale(n, SEED + n)
        for n in CLUSTER_COUNTS
    ]
    result = pd.DataFrame(rows)

    out_dir = Path(__file__).parent / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "raum27_meilenstein5_skalierung.csv"
    result.to_csv(path, index=False)

    print("KOMPAKTE SKALIERUNG")
    print(result.to_string(index=False))
    print(f"\nCSV: {path}")


if __name__ == "__main__":
    main()
