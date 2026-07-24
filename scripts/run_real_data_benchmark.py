"""One-off analysis script: run the full real-data lotto benchmark.

Not part of the automated test suite -- the FingerprintKNNPredictor
backtest over the full ~2700-draw history since 2000 takes several
minutes (its distance computation is O(n^2) in the number of draws).
tests/test_lotto_benchmark.py and tests/test_real_data_and_ztest.py cover
the same logic on small/synthetic data in seconds, for fast CI runs.

Usage: python3 scripts/run_real_data_benchmark.py
"""

import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from raum27.lotto_benchmark import (
    FingerprintKNNPredictor,
    RandomPredictor,
    backtest,
    expected_matches,
    load_draws_from_csv,
    z_test_vs_theoretical_baseline,
)

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "lotto_6aus49_since_2000.csv")


def report(name: str, matches: list[int], elapsed: float) -> None:
    n = len(matches)
    mean_matches = sum(matches) / n
    baseline = float(expected_matches())
    delta = mean_matches - baseline
    z, p = z_test_vs_theoretical_baseline(matches)
    print(f"\n== {name} ==")
    print(f"draws evaluated:     {n}")
    print(f"runtime:             {elapsed:.1f}s")
    print(f"mean matches/draw:   {mean_matches:.4f}")
    print(f"theoretical baseline:{baseline:.4f}")
    print(f"delta vs baseline:   {delta:+.4f}")
    print(f"z-score:             {z:+.3f}")
    print(f"p-value (one-sided): {p:.4f}")


def main() -> None:
    draws = load_draws_from_csv(DATA_PATH)
    print(f"Loaded {len(draws)} real draws from {DATA_PATH}")
    print(f"({draws[0]} ... {draws[-1]})")

    t0 = time.time()
    random_matches = backtest(draws, RandomPredictor(seed=1))
    report("Zufalls-Baseline (RandomPredictor)", random_matches, time.time() - t0)

    t0 = time.time()
    knn_matches = backtest(draws, FingerprintKNNPredictor(k=5, seed=1))
    report("Fingerprint/k-NN-Vorhersagesystem", knn_matches, time.time() - t0)

    random_mean = sum(random_matches) / len(random_matches)
    knn_mean = sum(knn_matches) / len(knn_matches)
    print(f"\n== Delta Zufall vs. Vorhersage ==")
    print(f"delta = {knn_mean - random_mean:+.4f} matches/draw")


if __name__ == "__main__":
    main()
