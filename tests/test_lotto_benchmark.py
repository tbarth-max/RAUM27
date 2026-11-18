import random
from fractions import Fraction

import pytest

from raum27.lotto_benchmark import (
    FingerprintKNNPredictor,
    RandomPredictor,
    backtest,
    expected_any_repeat_years,
    expected_matches,
    expected_specific_state_recurrence_years,
    match_count,
    match_probability,
    n_draw_states,
    permutation_test,
)


def test_match_probabilities_sum_to_one():
    assert sum(match_probability(m) for m in range(0, 7)) == 1


def test_jackpot_probability_is_one_in_the_full_combination_count():
    from math import comb

    assert match_probability(6) == Fraction(1, comb(49, 6))


def test_three_matches_is_about_1_76_percent_not_5_percent():
    # This is the actual baseline for "3 richtige" in 6-aus-49 -- not the
    # 5% used informally in discussion. Getting this number right matters
    # because the whole benchmark compares against it.
    p = match_probability(3)
    assert p == Fraction(20 * 12341, 13983816)
    assert 0.0176 < float(p) < 0.0177


def test_expected_matches_matches_theory():
    assert expected_matches() == Fraction(36, 49)


def test_match_count():
    assert match_count((1, 2, 3, 4, 5, 6), (1, 2, 3, 40, 41, 42)) == 3
    assert match_count((1, 2, 3, 4, 5, 6), (7, 8, 9, 10, 11, 12)) == 0


def _synthetic_history(n=80, seed=123):
    rng = random.Random(seed)
    return [tuple(sorted(rng.sample(range(1, 50), 6))) for _ in range(n)]


def test_random_predictor_matches_theoretical_expectation():
    history = _synthetic_history(n=300, seed=1)
    predictor = RandomPredictor(seed=2)
    matches = backtest(history, predictor)
    mean_matches = sum(matches) / len(matches)
    # Sanity check on the backtest harness itself: a predictor with zero
    # information should land close to the theoretical mean (36/49 ~= 0.735),
    # well within sampling noise for this many trials.
    assert abs(mean_matches - float(expected_matches())) < 0.15


def test_fingerprint_knn_shows_no_significant_edge_on_random_history():
    """The actual falsification test requested: run the source notes'
    fingerprint + k-NN forecaster exactly as specified against i.i.d.
    random draws (a certified lottery is, by design, indistinguishable
    from this), and check whether it beats the random baseline by more
    than permutation noise would predict.

    Because the history here is genuinely i.i.d. random by construction,
    there is zero mutual information between any draw and its
    predecessors -- so no function of history, however elaborate, can
    have a real edge. A non-significant p-value here is not a failure of
    the algorithm's implementation, it is the mathematically expected
    result of trying to extract signal from a process that provably has
    none.
    """
    history = _synthetic_history(n=60, seed=7)

    observed, p_value, null_stats = permutation_test(
        history,
        predictor_factory=lambda: FingerprintKNNPredictor(k=5, seed=42),
        n_permutations=40,
        seed=99,
    )

    assert len(null_stats) == 40
    # No claim of "p < 0.05 therefore it works" -- the claim under test is
    # the opposite: on true i.i.d. noise, this p-value should NOT be small.
    assert p_value > 0.05


def test_n_draw_states_matches_known_6aus49_count():
    assert n_draw_states() == 13_983_816


def test_specific_state_recurrence_is_about_269_thousand_years():
    years = expected_specific_state_recurrence_years(draws_per_year=52)
    assert 268_000 < years < 269_000


def test_any_repeat_is_about_90_years_not_269_thousand():
    years = expected_any_repeat_years(draws_per_year=52)
    assert 85 < years < 95


def test_specific_state_and_any_repeat_differ_by_about_3000x():
    """The two questions are easy to conflate ('how long until a repeat')
    but have very different answers -- verifying the ratio here keeps
    that distinction checkable rather than just asserted in prose."""
    specific = expected_specific_state_recurrence_years(draws_per_year=52)
    any_repeat = expected_any_repeat_years(draws_per_year=52)
    ratio = specific / any_repeat
    assert 2500 < ratio < 3500
