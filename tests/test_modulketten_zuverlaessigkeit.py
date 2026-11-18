"""Tests for raum27.modulketten_zuverlaessigkeit."""
from __future__ import annotations

from fractions import Fraction

import numpy as np

from raum27.modulketten_zuverlaessigkeit import (
    chain_success_probability,
    simulate_greedy_chain,
)


def test_chain_success_probability_is_the_exact_product():
    assert chain_success_probability([Fraction(1, 2)] * 10) == Fraction(1, 1024)
    assert chain_success_probability([Fraction(9, 10), Fraction(4, 5)]) == Fraction(18, 25)


def test_a_single_unreliable_module_drags_down_the_whole_chain():
    """One weak link (50%) in an otherwise near-perfect chain caps the
    whole chain's success probability at that link's own rate."""
    p = chain_success_probability([Fraction(99, 100)] * 9 + [Fraction(1, 2)])
    assert p < Fraction(1, 2)


def test_greedy_chain_simulation_matches_the_exact_expectation():
    """E[product of n i.i.d. draws] = E[draw]^n for independent draws.
    With rates ~ Uniform(0.70, 0.95), E[rate] = 0.825, so the fraction of
    10-module chains that complete fully should converge to 0.825**10 =
    14.55%. Checked against a real, fixed-seed simulation, not asserted."""
    rng = np.random.default_rng(0)
    fraction_complete, average_length = simulate_greedy_chain(
        rng, n_modules=10, low=0.70, high=0.95, trials=50_000
    )
    expected = 0.825**10
    assert abs(fraction_complete - expected) < 0.01
    assert 3.5 < average_length < 4.5


def test_more_modules_means_lower_completion_probability():
    rng = np.random.default_rng(1)
    frac_5, _ = simulate_greedy_chain(rng, n_modules=5, low=0.70, high=0.95, trials=20_000)
    frac_20, _ = simulate_greedy_chain(rng, n_modules=20, low=0.70, high=0.95, trials=20_000)
    assert frac_20 < frac_5
