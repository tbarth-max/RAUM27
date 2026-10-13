"""Tests for raum27.fundamentalbereich."""

from collections import Counter
from fractions import Fraction
from itertools import product
import math

import pytest

from raum27.fundamentalbereich import (
    PASSIVE_STOP,
    RESERVE,
    SIGMA,
    all_axes,
    coupled_states,
    cube_group,
    cycle_mirrors,
    digit_cycle,
    distance_squares,
    frequency_rest,
    from_path,
    fundamental_nodes,
    ideal_points,
    never_a_square_sum,
    octahedron_rest,
    orbit_count,
    polygon_rest,
    sieve_stop,
    stern_brocot_path,
    sum_line,
    symmetries_of,
    touching_radii_squared,
    x_only,
)

ODD = lambda t: t + Fraction(1, 1000) * t ** 3      # stands in for x + c / sin(16 x): odd in x
EVEN_PART = lambda t: t + Fraction(1, 1000) * t * t


def test_full_cube_symmetry_leaves_35_of_729_nodes():
    assert len(cube_group()) == 48
    assert orbit_count(cube_group()) == 35 == len(fundamental_nodes())
    assert 9 ** 3 == 729


def test_modulation_keeps_only_the_symmetries_it_commutes_with():
    full = symmetries_of(all_axes(ODD))
    assert len(full) == 48 and orbit_count(full) == 35
    # compute_vector: odd modulation on x only -> y/z square times the x sign flip
    x_odd = symmetries_of(x_only(ODD))
    assert len(x_odd) == 16 and orbit_count(x_odd) == 75
    assert all(p[0] == 0 for p, s in x_odd)            # x stays on its axis
    assert {s[0] for p, s in x_odd} == {1, -1}          # but may flip sign
    # not odd and on x only: the square alone
    x_plain = symmetries_of(x_only(EVEN_PART))
    assert len(x_plain) == 8 and orbit_count(x_plain) == 135
    # same on all axes but not odd: permutations only
    assert len(symmetries_of(all_axes(EVEN_PART))) == 6


def test_compute_vector_modulation_is_odd_and_tiny():
    c = 0.1 * (0.000004883 / 50.0)
    for x in range(1, 5):
        plus = x + c / math.sin(16.0 * x)
        minus = -x + c / math.sin(-16.0 * x)
        assert minus == -plus
        assert abs(plus - x) < 4e-8


def test_legendre_explains_every_gap_until_the_grid_edge():
    assert [n for n in range(1, 64) if never_a_square_sum(n)] == [7, 15, 23, 28, 31, 39, 47, 55, 60, 63]
    on_grid = distance_squares(8)                     # differences on 1..9
    missing = [n for n in range(1, 3 * 64 + 1) if n not in on_grid]
    assert all(never_a_square_sum(n) for n in missing if n <= 90)
    assert missing[missing.index(87) + 1] == 91 and not never_a_square_sum(91)   # beyond: the grid edge
    assert not never_a_square_sum(0)
    assert not any(never_a_square_sum(n) for n in distance_squares(20))


def test_27_ideal_points_and_three_touching_spheres():
    assert ideal_points() == {0: 1, 16: 6, 32: 12, 48: 8}
    assert touching_radii_squared() == (Fraction(1, 4), Fraction(2, 4), Fraction(3, 4))
    assert coupled_states() == (1458, 531441)
    assert Fraction(531441, 1458) == Fraction(729, 2)


def test_sieve_rests_and_both_stops():
    assert polygon_rest(4) == pytest.approx(1 - 2 / math.pi)
    assert [round(100 * polygon_rest(n), 2) for n in (4, 8, 16, 32, 64, 128)] == [36.34, 9.97, 2.55, 0.64, 0.16, 0.04]
    assert octahedron_rest(1) == pytest.approx(1 - 1 / math.pi)
    assert [round(100 * octahedron_rest(k), 1) for k in (1, 2, 4, 8, 12, 16)] == [68.2, 29.7, 8.8, 2.3, 1.0, 0.6]
    assert octahedron_rest(12) > 0.01                  # 1.05 %: the 1 % stop is first crossed at k = 13
    assert sieve_stop(octahedron_rest, PASSIVE_STOP)[0] == 13
    doubling = lambda s: polygon_rest(4 * 2 ** (s - 1))
    assert sieve_stop(doubling, PASSIVE_STOP)[0] == 4     # 32-gon
    assert sieve_stop(doubling, RESERVE)[0] == 6          # 128-gon


def test_structure_constant():
    assert SIGMA == Fraction(149896229, 150000000)
    assert RESERVE == Fraction(103771, 150000000)
    assert 0.00069 < RESERVE < 0.000692


def test_sum_line_is_always_24_and_its_rest_is_the_grid_position():
    rests = Counter()
    for coord in product(range(1, 10), repeat=3):
        d0, d2, rest = sum_line(coord)
        assert d0 + d2 == 24
        assert d0 == 27 - sum(coord)
        assert rest == {0: 0, 1: Fraction(1, 24), 2: Fraction(-1, 24)}[d0 % 3]
        rests[rest] += 1
    assert rests == {Fraction(0): 243, Fraction(1, 24): 243, Fraction(-1, 24): 243}
    assert frequency_rest(Fraction(1, 24)) == Fraction(-7, 960)
    with pytest.raises(ValueError):
        sum_line((0, 5, 5))
    with pytest.raises(TypeError):
        frequency_rest(0.5)


def test_digit_cycle_has_two_mirrors():
    assert digit_cycle() == [1, 2, 4, 8, 7, 5]
    additive, multiplicative = cycle_mirrors()
    assert all(a + b == 9 for a, b in additive)
    assert all(a * b % 9 == 1 for a, b in multiplicative)
    product_all = math.prod(digit_cycle())
    assert product_all % 9 == 8                       # the plain product is not 1


def test_stern_brocot_by_mediants():
    assert stern_brocot_path(1) == ""
    assert stern_brocot_path(Fraction(16, 9)) == "RLRRRL"
    assert stern_brocot_path(Fraction(9, 16)) == "LRLLLR"       # inversion swaps L and R
    for x in (Fraction(3, 4), Fraction(4, 3), Fraction(299, 300), 7):
        assert from_path(stern_brocot_path(x)) == x
    with pytest.raises(ValueError):
        stern_brocot_path(0)
    with pytest.raises(ValueError):
        from_path("LX")
