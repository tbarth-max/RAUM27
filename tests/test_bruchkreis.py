"""Tests for raum27.bruchkreis."""

from fractions import Fraction

import pytest

from raum27.bruchkreis import (
    across, circle_point, consecutive_delta, continued_fraction, cosh_of,
    cross_ratio, csc_of, ford_circle, ford_touch, four_velocity, interval, kite_area,
    mediant, moire_period, neighbours, new_points, order_sine, ring_product, sin2_of,
    sin_of, sinh_of, stern_brocot_level, stern_brocot_path,
)
from raum27.zeitachse import rotation


def test_ring_is_always_one_cross_ratio_is_not():
    assert ring_product([3, 5, 6, 2]) == 1 and ring_product([7, 100, Fraction(1, 3), 42]) == 1
    assert cross_ratio(3, 5, 6, 2) == Fraction(1, 5)
    assert cross_ratio(3 * 7, 5 * 7, 6 * 11, 2 * 11) == Fraction(1, 5)    # rows rescaled
    assert cross_ratio(3 * 2, 5 * 13, 6 * 2, 2 * 13) == Fraction(1, 5)    # columns rescaled
    assert cross_ratio(2, 3, 4, 5) == Fraction(5, 6)
    with pytest.raises(ZeroDivisionError):
        ring_product([1, 0])
    with pytest.raises(ZeroDivisionError):
        cross_ratio(1, 0, 1, 1)
    with pytest.raises(TypeError):
        cross_ratio(0.5, 1, 1, 1)


def test_consecutive_numbers_leave_two():
    assert all(consecutive_delta(a) == 2 for a in range(-5, 50))
    assert consecutive_delta(Fraction(1, 3)) == 2


def test_across_the_centre_two_sevens_and_the_delta():
    assert across(2, 5) == (7, Fraction(-3, 2))
    assert across(3, 4) == (7, Fraction(-1, 2))
    assert kite_area(7, 7) == Fraction(49, 2)


def test_one_fraction_every_function():
    assert circle_point(Fraction(1, 2)) == (Fraction(3, 5), Fraction(4, 5))
    assert circle_point(Fraction(2, 3)) == (Fraction(5, 13), Fraction(12, 13))
    for t in (Fraction(1, 2), Fraction(2, 3), Fraction(-3, 7)):
        x, y = circle_point(t)
        assert x * x + y * y == 1 and sin_of(t) == y
        assert sin_of(t) * csc_of(t) == 1 and sin2_of(t) == y * y
        assert cosh_of(t) ** 2 - sinh_of(t) ** 2 == 1
    assert (sinh_of(Fraction(1, 2)), cosh_of(Fraction(1, 2))) == (Fraction(4, 3), Fraction(5, 3))
    assert (sinh_of(Fraction(2, 3)), cosh_of(Fraction(2, 3))) == (Fraction(12, 5), Fraction(13, 5))
    with pytest.raises(ZeroDivisionError):
        csc_of(0)
    with pytest.raises(ValueError):
        sinh_of(1)                                                         # the light limit


def test_four_velocity_gives_the_common_one():
    n = tuple(row[0] for row in rotation(1, 1, 0, 1))                    # x turned onto (1/3, 2/3, 2/3)
    assert n == (Fraction(1, 3), Fraction(2, 3), Fraction(2, 3))
    u = four_velocity(Fraction(1, 2), n)
    assert u == (Fraction(5, 3), Fraction(4, 9), Fraction(8, 9), Fraction(8, 9))
    assert interval(u) == 1 and interval((1, 0, 0, 0)) == 1
    with pytest.raises(ValueError):
        four_velocity(Fraction(1, 2), (1, 1, 0))


def test_neighbours_mediants_and_ford_circles():
    assert neighbours(Fraction(1, 2), Fraction(2, 3)) and not neighbours(Fraction(1, 3), Fraction(2, 3))
    assert mediant(Fraction(1, 2), Fraction(2, 3)) == Fraction(3, 5)
    assert ford_circle(Fraction(1, 2)) == (Fraction(1, 2), Fraction(1, 8), Fraction(1, 8))
    for x, y in [(Fraction(1, 2), Fraction(2, 3)), (Fraction(1, 3), Fraction(2, 5)), (0, 1)]:
        assert neighbours(x, y) and ford_touch(x, y)
    assert not ford_touch(Fraction(1, 3), Fraction(2, 3))


def test_denominator_circles_and_the_doubling_tree():
    assert [new_points(q) for q in range(2, 10)] == [1, 2, 2, 4, 2, 6, 4, 6]
    assert stern_brocot_level(1) == [Fraction(1, 2)]
    assert stern_brocot_level(3) == [Fraction(1, 4), Fraction(2, 5), Fraction(3, 5), Fraction(3, 4)]
    assert [len(stern_brocot_level(k)) for k in range(1, 7)] == [1, 2, 4, 8, 16, 32]
    assert stern_brocot_path(Fraction(3, 5)) == "LRL" and stern_brocot_path(1) == ""
    assert stern_brocot_path(Fraction(5, 2)) == "RRL"
    with pytest.raises(ValueError):
        new_points(1)
    with pytest.raises(ValueError):
        stern_brocot_level(0)
    with pytest.raises(ValueError):
        stern_brocot_path(0)


def test_continued_fraction_stops_by_itself_or_at_the_tolerance():
    assert continued_fraction(Fraction(7, 5)) == [1, Fraction(3, 2), Fraction(7, 5)]
    pi = Fraction(31415926535897932384626, 10 ** 22)
    c = continued_fraction(pi, Fraction(1, 10 ** 6))
    assert c == [3, Fraction(22, 7), Fraction(333, 106), Fraction(355, 113)]
    for p in c:
        assert abs(pi - p) < Fraction(1, p.denominator ** 2)


def test_moire_and_grating():
    assert moire_period(10, 11) == 110
    with pytest.raises(ValueError):
        moire_period(3, 3)
    s0 = order_sine(Fraction(1, 5), 1, 450, 2000)
    s1 = order_sine(Fraction(1, 5), 2, 450, 2000)
    assert s1 - s0 == s0 - Fraction(1, 5)                                 # rigid grid in sines
    assert order_sine(Fraction(-1, 5), 1, 450, 2000) - Fraction(-1, 5) == s0 - Fraction(1, 5)
    with pytest.raises(ValueError):
        order_sine(0, 5, 450, 2000)
