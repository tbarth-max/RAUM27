"""Tests for raum27.waage."""
from __future__ import annotations

from fractions import Fraction

import pytest

from raum27.kern_modul_v2 import redundancy_deviation
from raum27.rational_space import involution
from raum27.waage import (
    is_lossless_encoding,
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


def test_coprime_weights_are_encoded_without_loss():
    """gcd(w1,w2)==1 means the balance point is already in lowest terms,
    so the pair is recoverable from the position alone. Checked for all
    132 ordered pairs of distinct primes up to 37."""
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    pairs = [(a, b) for a in primes for b in primes if a != b]
    assert len(pairs) == 132
    for w1, w2 in pairs:
        assert is_lossless_encoding(w1, w2)
        d1 = balance_point(Fraction(w1), Fraction(w2))
        assert d1.denominator == w1 + w2  # nothing cancelled
        assert ratio_from_balance_point(d1) == Fraction(w1, w2)


def test_coprime_prime_pairs_give_no_colliding_balance_points():
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    points = {balance_point(Fraction(a), Fraction(b))
              for a in primes for b in primes if a != b}
    assert len(points) == 132


def test_non_coprime_pairs_collide_so_the_beam_cannot_tell_them_apart():
    """The beam sees only the ratio. Archived as a limit of the method,
    not a bug."""
    assert balance_point(Fraction(1), Fraction(2)) == balance_point(Fraction(2), Fraction(4))
    assert balance_point(Fraction(3), Fraction(5)) == balance_point(Fraction(9), Fraction(15))
    assert not is_lossless_encoding(2, 4)
    assert not is_lossless_encoding(9, 15)


def test_primality_is_sufficient_but_not_necessary():
    """NEGATIVE RESULT, archived: it is coprimality doing the work, not
    primality. Both members composite, still lossless."""
    for w1, w2 in ((4, 9), (8, 15), (9, 16), (25, 27), (16, 81)):
        assert is_lossless_encoding(w1, w2)
        d1 = balance_point(Fraction(w1), Fraction(w2))
        assert ratio_from_balance_point(d1) == Fraction(w1, w2)


def test_prime_balance_points_land_on_nothing_special():
    """NEGATIVE RESULT, archived: the denominator is always w1+w2, and
    sums of two primes are usually composite -- no 'prime space'
    structure beyond ordinary coprimality."""
    primes = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47}
    denominators = [balance_point(Fraction(a), Fraction(b)).denominator
                    for a in (3, 5, 7, 11) for b in (5, 7, 11, 13) if a != b]
    prime_denominators = [d for d in denominators if d in primes]
    assert len(prime_denominators) < len(denominators) / 2
