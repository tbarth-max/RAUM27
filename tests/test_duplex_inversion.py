"""Tests for raum27.duplex_inversion."""
from __future__ import annotations

from fractions import Fraction

from raum27.duplex_inversion import (
    BASE,
    coincidence_points,
    off_diagonal_coincidences,
    r_in,
    r_out,
)


def test_expansion_anchor_holds_for_every_n():
    """The Lean sketch's Theorem 1, actually checked: r_out(1, n) = 1/2
    for every n, because 1**n = 1 (including 1**0 = 1)."""
    for n in range(0, 30):
        assert r_out(1, n) == Fraction(1, 2)


def test_compression_anchor_holds_for_every_x():
    """Theorem 2: r_in(x, 1) = 1/2 for every x."""
    for x in range(0, 30):
        assert r_in(x, 1) == Fraction(1, 2)


def test_both_maps_are_strictly_positive():
    """Theorem 4: a positive base to a natural power stays positive."""
    for x in range(0, 8):
        for n in range(0, 8):
            assert r_out(x, n) > 0
            assert r_in(x, n) > 0


def test_the_general_symmetry_the_sketch_did_not_state():
    """r_out(x, n) == r_in(n, x) for EVERY pair, not just at (1,1) --
    the sketch's 'Fokalpunkt' theorem is the degenerate special case of
    this."""
    for x in range(0, 7):
        for n in range(0, 7):
            assert r_out(x, n) == r_in(n, x)


def test_the_focal_point_theorem_is_a_tautology():
    """At x = n = 1 both exponents are literally the same expression
    (1**1), so the claim reduces to 'this value equals itself'. Shown
    here explicitly so it isn't mistaken for a structural result."""
    assert 1**1 == 1**1
    assert r_out(1, 1) == r_in(1, 1) == Fraction(1, 2)


def test_coincidences_are_the_diagonal_plus_exactly_one_exceptional_pair():
    """Where expansion and compression meet at the same arguments
    (x**n == n**x) is not only (1,1): the whole diagonal, plus (2,4) and
    (4,2) -- the classical result over the naturals."""
    assert off_diagonal_coincidences(12) == [(2, 4), (4, 2)]
    assert all(x == n for (x, n) in coincidence_points(12) if (x, n) not in [(2, 4), (4, 2)])


def test_the_exceptional_pair_lands_on_one_over_sixty_five_thousand():
    assert 2**4 == 4**2 == 16
    assert r_out(2, 4) == r_in(2, 4) == BASE**16 == Fraction(1, 65536)
