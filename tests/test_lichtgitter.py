"""Tests for raum27.lichtgitter."""
from __future__ import annotations

import math
import random
from fractions import Fraction

import pytest

from raum27.kern_modul_v2 import tdoa_position
from raum27.lichtgitter import (
    IDEALISED_SPEED_OF_LIGHT,
    SPEED_OF_LIGHT,
    distance_gradient,
    ellipse_y_squared,
    elliptic_coordinate_count,
    flight_time_seconds,
    focal_difference,
    focal_distance,
    focal_radii,
    focal_sum,
    idealisation_relative_error,
    light_second_semi_major,
    position_error_from_idealised_c,
    position_from_focal_difference,
    semi_minor_squared,
    ticks_per_round_trip,
)


def test_c_is_an_exact_integer_not_a_rounded_measurement():
    """The metre is DEFINED as the distance light travels in 1/c s, so c
    is an exact integer in SI. The whole-number instinct is right."""
    assert SPEED_OF_LIGHT == 299792458
    assert isinstance(SPEED_OF_LIGHT, int)
    assert Fraction(SPEED_OF_LIGHT).denominator == 1


def test_idealising_c_to_300_million_throws_away_the_exactness():
    """REFUTES the idealisation: the rounding is 0.0692%, which is
    ruinous over any real distance."""
    err = idealisation_relative_error()
    assert err == Fraction(207542, 299792458)
    assert float(err) == pytest.approx(6.9229e-4, rel=1e-3)
    assert IDEALISED_SPEED_OF_LIGHT - SPEED_OF_LIGHT == 207542
    # and the idealised value is NOT an exact tick count of the real one
    assert IDEALISED_SPEED_OF_LIGHT % SPEED_OF_LIGHT != 0


def test_the_idealisation_cost_in_kilometres():
    assert position_error_from_idealised_c(20_200_000.0) / 1000 == pytest.approx(13.97, abs=0.1)
    assert position_error_from_idealised_c(384_400_000.0) / 1000 == pytest.approx(265.9, abs=1.0)
    assert position_error_from_idealised_c(1.496e11) / 1000 == pytest.approx(103494.0, abs=50.0)
    # GPS needs sub-metre accuracy; 14 km is four orders of magnitude out
    assert position_error_from_idealised_c(20_200_000.0) > 10_000.0


def test_the_focal_radius_identity_is_exact_against_raw_geometry():
    """r1 = a - e*x and r2 = a + e*x, checked against sqrt((x +- c)^2 +
    y^2) in squared form over exact rationals. 4000 random points, zero
    tolerance."""
    random.seed(3)
    checked = 0
    for _ in range(4000):
        a = Fraction(random.randint(5, 40))
        e = Fraction(random.randint(1, 9), 10)
        c = focal_distance(a, e)
        x = Fraction(random.randint(-100, 100), 100) * a
        if abs(x) > a:
            continue
        y_sq = ellipse_y_squared(a, e, x)
        if y_sq < 0:
            continue
        r1, r2 = focal_radii(a, e, x)
        assert r1 * r1 == (x - c) ** 2 + y_sq
        assert r2 * r2 == (x + c) ** 2 + y_sq
        checked += 1
    assert checked > 3000


def test_every_route_from_cause_to_effect_has_the_same_exact_length():
    """The isochrone property: r1 + r2 = 2a for every boundary point, so
    rolling it back and forth conserves something exactly."""
    for a, e in ((Fraction(25), Fraction(3, 5)), (Fraction(7), Fraction(1, 2)),
                 (Fraction(100), Fraction(9, 10)), (Fraction(13, 2), Fraction(2, 7))):
        sums = set()
        for k in range(-20, 21):
            x = Fraction(k, 20) * a
            if ellipse_y_squared(a, e, x) < 0:
                continue
            r1, r2 = focal_radii(a, e, x)
            sums.add(r1 + r2)
        assert sums == {focal_sum(a)} == {2 * a}


def test_the_tick_count_is_an_exact_integer_for_every_route():
    for a in (1, 150, 149896229, 299792458):
        assert ticks_per_round_trip(a) == 2 * a
        assert isinstance(ticks_per_round_trip(a), int)
    # a one-light-second ellipse counts exactly c ticks
    assert ticks_per_round_trip(light_second_semi_major()) == SPEED_OF_LIGHT
    assert SPEED_OF_LIGHT % 2 == 0  # so the halving is exact


def test_flight_time_is_an_exact_rational_with_no_rounding():
    t = flight_time_seconds(Fraction(light_second_semi_major()))
    assert t == 1
    assert flight_time_seconds(Fraction(150)) == Fraction(300, SPEED_OF_LIGHT)
    # 2/c reduces, because c is even -- the 2 cancels exactly
    assert flight_time_seconds(Fraction(1)) == Fraction(2, SPEED_OF_LIGHT)
    assert flight_time_seconds(Fraction(1)).denominator == SPEED_OF_LIGHT // 2
    # an odd semi-major axis keeps the full denominator
    assert flight_time_seconds(Fraction(1, 2)) == Fraction(1, SPEED_OF_LIGHT)


def test_sum_is_the_ellipse_and_difference_is_the_tdoa_hyperbola():
    a, e = Fraction(25), Fraction(3, 5)
    for x in (Fraction(0), Fraction(5), Fraction(-10), Fraction(25, 2)):
        r1, r2 = focal_radii(a, e, x)
        assert r1 + r2 == focal_sum(a)              # independent of x
        assert r2 - r1 == focal_difference(e, x)    # depends on x
        assert position_from_focal_difference(r2 - r1, e) == x


def test_the_difference_inverts_exactly_over_many_parameters():
    """Time-difference localisation with no floating point anywhere."""
    for a in (Fraction(10), Fraction(25), Fraction(99, 7)):
        for e in (Fraction(1, 5), Fraction(3, 5), Fraction(7, 8)):
            for k in range(-9, 10):
                x = Fraction(k, 10) * a
                if ellipse_y_squared(a, e, x) < 0:
                    continue
                r1, r2 = focal_radii(a, e, x)
                assert position_from_focal_difference(r2 - r1, e) == x


def test_a_circle_has_no_time_difference_to_localise_with():
    a = Fraction(5)
    r1, r2 = focal_radii(a, Fraction(0), Fraction(3))
    assert r1 == r2 == a
    assert focal_difference(Fraction(0), Fraction(3)) == 0
    with pytest.raises(ValueError):
        position_from_focal_difference(Fraction(0), Fraction(0))


def test_the_confocal_families_are_orthogonal_exactly_over_fractions():
    """grad(r1+r2) . grad(r1-r2) = |grad r1|^2 - |grad r2|^2 = 0, since
    the gradient of a distance function is a unit vector. Checked on
    every rational point (up to a search bound) where both unit
    gradients are themselves rational, so the dot product is an exact
    Fraction and not a small float."""
    exact_points = 0
    for a in range(2, 26):
        for num in range(1, 10):
            for den in range(num + 1, 11):
                e = Fraction(num, den)
                c = focal_distance(Fraction(a), e)
                if c.denominator != 1:
                    continue
                for xn in range(-10 * a, 10 * a + 1):
                    x = Fraction(xn, 10)
                    if abs(x) > a:
                        continue
                    y_sq = ellipse_y_squared(Fraction(a), e, x)
                    if y_sq <= 0:
                        continue
                    yn, yd = y_sq.numerator, y_sq.denominator
                    ry, rd = math.isqrt(yn), math.isqrt(yd)
                    if ry * ry != yn or rd * rd != yd:
                        continue
                    y = Fraction(ry, rd)
                    r1, r2 = focal_radii(Fraction(a), e, x)
                    if r1 <= 0 or r2 <= 0:
                        continue
                    g1 = distance_gradient(x, y, c, Fraction(0), r1)
                    g2 = distance_gradient(x, y, -c, Fraction(0), r2)
                    if g1[0] ** 2 + g1[1] ** 2 != 1:
                        continue
                    if g2[0] ** 2 + g2[1] ** 2 != 1:
                        continue
                    s = (g1[0] + g2[0], g1[1] + g2[1])
                    d = (g1[0] - g2[0], g1[1] - g2[1])
                    assert s[0] * d[0] + s[1] * d[1] == 0
                    exact_points += 1
    assert exact_points > 500


def test_a_worked_exact_example_of_the_orthogonality():
    """a = 25, e = 3/5 puts (15, 16) on the ellipse with both focal
    radii integers -- the smallest fully integral case."""
    a, e = Fraction(25), Fraction(3, 5)
    x, y = Fraction(15), Fraction(16)
    assert ellipse_y_squared(a, e, x) == y * y
    r1, r2 = focal_radii(a, e, x)
    assert (r1, r2) == (Fraction(16), Fraction(34))
    assert r1 + r2 == 50 == 2 * a
    g1 = distance_gradient(x, y, focal_distance(a, e), Fraction(0), r1)
    g2 = distance_gradient(x, y, -focal_distance(a, e), Fraction(0), r2)
    assert g1 == (Fraction(0), Fraction(1))
    assert g2 == (Fraction(15, 17), Fraction(8, 17))
    assert g1[0] ** 2 + g1[1] ** 2 == 1
    assert g2[0] ** 2 + g2[1] ** 2 == 1
    s = (g1[0] + g2[0], g1[1] + g2[1])
    d = (g1[0] - g2[0], g1[1] - g2[1])
    assert s[0] * d[0] + s[1] * d[1] == 0


def test_the_conserved_sum_is_exactly_the_L_the_repos_tdoa_needs():
    """Cross-module, and it pins down what 2a is FOR.

    kern_modul_v2.tdoa_position(L, v, dt) = (L - v*dt)/2 returns the
    distance to the first receiver, and it assumes the two distances sum
    to L. On an ellipse that sum is the conserved 2a -- not the focal
    baseline 2c. Fed 2a, the existing function returns the focal radius
    exactly, over Fraction: (2a - c*((r2-r1)/c))/2 = a - e*x = r1.

    So the ellipse's invariant is precisely the input that function was
    always missing, and the two modules compose without a float."""
    c_light = Fraction(SPEED_OF_LIGHT)
    for a in (Fraction(25), Fraction(10), Fraction(99, 7)):
        for e in (Fraction(1, 2), Fraction(3, 5), Fraction(7, 8)):
            for k in range(-8, 9):
                x = Fraction(k, 10) * a
                if ellipse_y_squared(a, e, x) < 0:
                    continue
                r1, r2 = focal_radii(a, e, x)
                dt = (r2 - r1) / c_light
                assert tdoa_position(focal_sum(a), c_light, dt) == r1
                # and the baseline 2c would be the WRONG L unless the
                # point sits on the segment between the foci
                if abs(x) < a and ellipse_y_squared(a, e, x) > 0:
                    wrong = tdoa_position(2 * focal_distance(a, e), c_light, dt)
                    assert wrong != r1


def test_three_hundred_million_overlays_add_nothing():
    """REFUTES the accumulation claim: the confocal family is complete
    at two parameters. A sum value and a difference value already pin a
    point down, so further overlays only resample the same grid."""
    assert elliptic_coordinate_count() == 2
    a, e = Fraction(25), Fraction(3, 5)
    recovered = set()
    for k in range(-10, 11):
        x = Fraction(k, 10) * a
        if ellipse_y_squared(a, e, x) < 0:
            continue
        r1, r2 = focal_radii(a, e, x)
        # the pair (sum, difference) determines x with nothing left over
        recovered.add((r1 + r2, position_from_focal_difference(r2 - r1, e)))
    assert len({s for s, _ in recovered}) == 1          # sum carries no position info
    assert len({p for _, p in recovered}) == len(recovered)  # difference carries all of it


def test_the_cube_does_not_divide_the_light_speed_integer():
    """Stated as a limit: the lattice counts c, and c carries no cube
    structure. 299792458 = 2 x 7 x 73 x 293339."""
    assert SPEED_OF_LIGHT == 2 * 7 * 73 * 293339
    assert SPEED_OF_LIGHT % 6 != 0
    assert SPEED_OF_LIGHT % 8 != 0
    assert SPEED_OF_LIGHT % 27 != 0
    assert SPEED_OF_LIGHT % 3 != 0


def test_degenerate_parameters_raise():
    with pytest.raises(ValueError):
        focal_radii(Fraction(10), Fraction(1), Fraction(0))     # e = 1 is a parabola
    with pytest.raises(ValueError):
        focal_radii(Fraction(10), Fraction(3, 2), Fraction(0))  # e > 1 is a hyperbola
    with pytest.raises(ValueError):
        focal_radii(Fraction(10), Fraction(1, 2), Fraction(11))  # x outside
    with pytest.raises(ValueError):
        distance_gradient(Fraction(0), Fraction(0), Fraction(0), Fraction(0), Fraction(0))


def test_semi_minor_squared_matches_the_pythagorean_relation():
    """b^2 = a^2 - c^2, exact."""
    for a, e in ((Fraction(25), Fraction(3, 5)), (Fraction(13), Fraction(5, 13)),
                 (Fraction(4), Fraction(1, 2))):
        c = focal_distance(a, e)
        assert semi_minor_squared(a, e) == a * a - c * c
    assert semi_minor_squared(Fraction(25), Fraction(3, 5)) == 400  # b = 20
