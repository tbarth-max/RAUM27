"""Tests for raum27.optionsraum."""
from __future__ import annotations

import random
from fractions import Fraction
from itertools import product

import pytest

from raum27.optionsraum import (
    concentration,
    is_on_simplex,
    participation_number,
    simplex_diameter_squared,
    single_wish,
    squared_distance,
    squared_distance_from_centre,
    uniform_wish,
    worst_squared_distance_to_a_single_wish,
)
from raum27.waage import center_of_mass, shares


def test_both_extremes_are_on_the_simplex():
    for n in (1, 2, 3, 6, 8, 27):
        assert is_on_simplex(uniform_wish(n))
        for i in range(n):
            assert is_on_simplex(single_wish(n, i))


def test_the_identity_linking_distance_and_concentration():
    """|p - c|^2 == concentration(p) - 1/n, exactly, for every wish
    direction -- not just at the extremes. Checked on 2100 random exact
    rational points across n = 2..8."""
    random.seed(7)
    for n in range(2, 9):
        for _ in range(300):
            raw = [Fraction(random.randint(0, 40), random.randint(1, 9)) for _ in range(n)]
            if sum(raw) == 0:
                continue
            p = shares(raw)
            assert is_on_simplex(p)
            assert squared_distance_from_centre(p) == concentration(p) - Fraction(1, n)


def test_concentration_is_minimal_exactly_at_the_all_wanting_centre():
    """Brute force over every exact lattice point of the simplex with
    denominator 12: the minimum 1/n is attained at the uniform wish and
    nowhere else."""
    for n in (2, 3, 4, 6):
        g = 12
        points = [[Fraction(k, g) for k in comb]
                  for comb in product(range(g + 1), repeat=n) if sum(comb) == g]
        values = [concentration(p) for p in points]
        assert min(values) == Fraction(1, n)
        minimisers = [p for p, v in zip(points, values) if v == Fraction(1, n)]
        assert minimisers == [uniform_wish(n)]


def test_concentration_is_maximal_exactly_at_the_single_wishes():
    """Same brute force: the maximum 1 is attained at the vertices and
    nowhere else."""
    for n in (2, 3, 4, 6):
        g = 12
        points = [[Fraction(k, g) for k in comb]
                  for comb in product(range(g + 1), repeat=n) if sum(comb) == g]
        values = [concentration(p) for p in points]
        assert max(values) == 1
        maximisers = [p for p, v in zip(points, values) if v == 1]
        assert len(maximisers) == n
        assert all(m in maximisers for m in (single_wish(n, i) for i in range(n)))


def test_the_all_wanting_centre_is_exactly_the_zero_point():
    for n in (2, 3, 6, 8, 27):
        assert squared_distance_from_centre(uniform_wish(n)) == 0


def test_a_single_wish_sits_at_exactly_n_minus_one_over_n():
    """Exact rational, strictly below 1 for every finite n -- the outer
    position is never actually reached, only approached."""
    for n in (2, 3, 4, 6, 8, 12, 27, 64):
        d = squared_distance_from_centre(single_wish(n, 0))
        assert d == Fraction(n - 1, n)
        assert d < 1
    assert squared_distance_from_centre(single_wish(6, 0)) == Fraction(5, 6)
    assert squared_distance_from_centre(single_wish(8, 0)) == Fraction(7, 8)
    assert squared_distance_from_centre(single_wish(27, 0)) == Fraction(26, 27)


def test_participation_number_reads_the_count_back_off_the_distribution():
    for n in (1, 2, 3, 6, 8, 27):
        assert participation_number(uniform_wish(n)) == n
        assert participation_number(single_wish(n, 0)) == 1


def test_a_zero_wish_vector_has_no_direction_at_all():
    """The same boundary waage.shares already raises at: wanting nothing
    is not a point in the option space."""
    with pytest.raises(ValueError):
        participation_number([Fraction(0), Fraction(0), Fraction(0)])
    with pytest.raises(ValueError):
        shares([Fraction(0), Fraction(0), Fraction(0)])


def test_the_maximal_delta_is_between_two_different_single_wishes_not_centre_to_edge():
    """CORRECTION, kept explicitly: the diameter of the option space is
    exactly 2 and independent of n, attained only between two distinct
    single wishes. Centre-to-vertex is (n-1)/n < 1 -- less than half of
    it, for every n."""
    for n in (2, 3, 6, 8, 27):
        a, b = single_wish(n, 0), single_wish(n, 1 % n)
        if n > 1:
            assert squared_distance(a, b) == simplex_diameter_squared() == 2
            assert squared_distance_from_centre(a) == Fraction(n - 1, n)
            assert 2 * squared_distance_from_centre(a) < squared_distance(a, b)


def test_no_pair_of_wish_directions_exceeds_the_diameter():
    random.seed(11)
    for n in range(2, 8):
        for _ in range(200):
            ps = []
            for _ in range(2):
                raw = [Fraction(random.randint(0, 30), random.randint(1, 7)) for _ in range(n)]
                if sum(raw) == 0:
                    raw[0] = Fraction(1)
                ps.append(shares(raw))
            assert squared_distance(ps[0], ps[1]) <= simplex_diameter_squared()


def test_the_centre_uniquely_minimises_the_worst_case_to_any_single_wish():
    """This is what actually singles out the all-wanting point. Brute
    force over the full exact lattice: nothing ties it, nothing beats
    it, and from the centre every single wish is equidistant."""
    for n in (3, 4):
        g = 12
        c = uniform_wish(n)
        ref = worst_squared_distance_to_a_single_wish(c)
        assert ref == Fraction(n - 1, n)
        better = tied = 0
        for comb in product(range(g + 1), repeat=n):
            if sum(comb) != g:
                continue
            p = [Fraction(k, g) for k in comb]
            if p == c:
                continue
            w = worst_squared_distance_to_a_single_wish(p)
            if w < ref:
                better += 1
            elif w == ref:
                tied += 1
        assert better == 0
        assert tied == 0
    for n in (3, 6, 8):
        c = uniform_wish(n)
        distances = {squared_distance(c, single_wish(n, i)) for i in range(n)}
        assert distances == {Fraction(n - 1, n)}


def test_the_centre_is_the_centre_of_mass_of_the_single_wishes():
    """Cross-module check against waage.center_of_mass: equal weights on
    the n single wishes give the uniform wish coordinate by coordinate.
    The two modules describe one construction from two sides."""
    for n in (2, 3, 6, 8):
        w = [Fraction(1)] * n
        coords = [center_of_mass(w, [co[i] for co in (single_wish(n, j) for j in range(n))])
                  for i in range(n)]
        assert coords == uniform_wish(n)


def test_adding_options_never_adds_reach():
    """The diameter does not grow with n: a larger option space does not
    put two single wishes further apart."""
    assert {squared_distance(single_wish(n, 0), single_wish(n, 1)) for n in range(2, 40)} == {2}
