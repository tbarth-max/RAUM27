import os
import random

from raum27.lotto_benchmark import (
    RandomPredictor,
    backtest,
    load_draws_from_csv,
    match_probability,
    z_test_vs_theoretical_baseline,
)

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "lotto_6aus49_since_2000.csv")


def test_real_dataset_loads_and_is_well_formed():
    draws = load_draws_from_csv(DATA_PATH)
    assert len(draws) > 2700
    for draw in draws:
        assert len(draw) == 6
        assert len(set(draw)) == 6
        assert all(1 <= n <= 49 for n in draw)


def test_variance_formula_matches_the_exact_distribution():
    # Cross-check the closed-form hypergeometric variance used by the
    # z-test against the exact distribution from match_probability.
    mean = sum(m * float(match_probability(m)) for m in range(7))
    var_from_distribution = sum((m - mean) ** 2 * float(match_probability(m)) for m in range(7))

    picks, winning, pool = 6, 6, 49
    var_formula = picks * (winning / pool) * ((pool - winning) / pool) * ((pool - picks) / (pool - 1))

    assert abs(var_from_distribution - var_formula) < 1e-9


def test_z_test_shows_no_significance_for_genuinely_random_matches():
    rng = random.Random(0)
    history = [tuple(sorted(rng.sample(range(1, 50), 6))) for _ in range(400)]
    matches = backtest(history, RandomPredictor(seed=1))
    z, p = z_test_vs_theoretical_baseline(matches)
    assert p > 0.05


def test_z_test_flags_an_artificially_inflated_match_rate():
    # Sanity check that the test has power: if matches were suspiciously
    # high (e.g. averaging 2 matches instead of the ~0.73 baseline), the
    # z-test must flag it as significant.
    inflated_matches = [2] * 400
    z, p = z_test_vs_theoretical_baseline(inflated_matches)
    assert p < 0.001
