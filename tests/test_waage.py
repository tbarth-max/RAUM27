"""Tests for raum27.waage."""
from __future__ import annotations

from fractions import Fraction

import pytest

from raum27.kern_modul_v2 import redundancy_deviation
from raum27.rational_space import involution
from raum27.waage import (
    balance_point,
    balances_at_one,
    geometric_mean_squared,
    lever_law_holds,
    ratio_from_balance_point,
)


def test_equal_weights_balance_in_the_middle():
    assert balance_point(Fraction(1), Fraction(1)) == Fraction(1, 2)


def test_lever_law_holds_exactly_for_many_weight_pairs():
    for w1 in range(1, 12):
        for w2 in range(1, 12):
            assert lever_law_holds(Fraction(w1), Fraction(w2))


def test_balance_point_is_an_exact_rational_not_an_approximation():
    assert balance_point(Fraction(3), Fraction(4)) == Fraction(4, 7)
    assert balance_point(Fraction(9), Fraction(16)) == Fraction(16, 25)
    assert balance_point(Fraction(2), Fraction(8)) == Fraction(4, 5)


def test_the_beam_is_a_lossless_ratio_encoder():
    """Position -> ratio -> position recovers the original exactly, so
    reading a ratio off the beam loses nothing."""
    for w1 in range(1, 10):
        for w2 in range(1, 10):
            d1 = balance_point(Fraction(w1), Fraction(w2))
            assert ratio_from_balance_point(d1) == Fraction(w1, w2)


def test_fulcrum_at_the_end_has_no_finite_ratio():
    with pytest.raises(ValueError):
        ratio_from_balance_point(Fraction(0))


def test_every_reciprocal_pair_balances_at_exactly_one():
    """On a logarithmic axis the balance point is the geometric mean, so
    x and 1/x balance at exactly 1 for every x -- the same fixed point
    rational_space.involution has."""
    for n, d in ((2, 1), (4, 1), (3, 1), (16, 9), (9, 16), (7, 5)):
        x = Fraction(n, d)
        assert balances_at_one(x, involution(x))
        assert geometric_mean_squared(x, involution(x)) == 1


def test_non_reciprocal_pairs_do_not_balance_at_one():
    assert not balances_at_one(Fraction(2), Fraction(3))
    assert geometric_mean_squared(Fraction(2), Fraction(3)) == 6


def test_the_repos_own_deviation_measure_is_the_same_balance_symmetry():
    """Cross-module check: kern_modul_v2.redundancy_deviation is already
    mirror-symmetric under x -> 1/x. In beam terms that symmetry IS the
    balance -- straying by a factor k to one side costs exactly what
    straying by factor k to the other side costs."""
    for n, d in ((2, 1), (4, 1), (16, 9), (9, 16), (5, 3)):
        x = Fraction(n, d)
        assert redundancy_deviation(x) == redundancy_deviation(involution(x))
        assert balances_at_one(x, involution(x))


def test_the_projects_own_constants_balance_at_one():
    """16/9 and 9/16 -- the expansion/compression pair that recurs
    throughout this project -- are a reciprocal pair, so they balance at
    exactly 1."""
    assert balances_at_one(Fraction(16, 9), Fraction(9, 16))
    assert balance_point(Fraction(16, 9), Fraction(9, 16)) == Fraction(81, 337)
