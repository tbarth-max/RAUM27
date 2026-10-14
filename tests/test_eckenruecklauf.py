"""Tests for raum27.eckenruecklauf."""

from fractions import Fraction

import pytest

from raum27.eckenruecklauf import (
    corner_radius, corner_reflect, diagonal_reach, opposite_digit_node, reaches_corner,
    remaining_gaps, touching_radii_squared,
)
from raum27.nennerordnung import Power


def test_the_three_spheres_of_the_nine_cube():
    faces, edges, corners = touching_radii_squared(9)
    assert (faces, edges, corners) == (Fraction(81, 4), Fraction(81, 2), Fraction(243, 4))
    assert faces == Fraction(9, 2) ** 2                       # inner radius a/2 = 9/2
    assert (faces * 2, faces * 3) == (edges, corners)         # 1 : 2 : 3


def test_the_p_ball_never_reaches_the_corner():
    r = Fraction(9, 2)
    assert diagonal_reach(r, 2).rational() == r               # sphere: the diagonal reach is r
    corner = Power.of(r) * Power.of(3).root(2)                # r * sqrt 3
    previous = diagonal_reach(r, 2)
    for p in (3, 4, 8, 16, 1000):
        reach = diagonal_reach(r, p)
        assert previous < reach < corner                      # closer with every p, never there
        previous = reach
    assert not reaches_corner(1000) and reaches_corner(None)
    assert diagonal_reach(r, 1) < diagonal_reach(r, 2)        # the octahedron lies inside
    with pytest.raises(ValueError):
        diagonal_reach(r, Fraction(1, 2))


def test_no_sharp_corner():
    assert corner_radius(Fraction(1, 9)) == Fraction(1, 9)
    with pytest.raises(ValueError):
        corner_radius(0)


def test_approaching_without_arriving():
    gaps = remaining_gaps(Fraction(9, 2), Fraction(1, 2), 40)
    assert all(g > 0 for g in gaps)
    assert gaps[-1] == Fraction(9, 2) / 2 ** 40
    pushes = sum(a - b for a, b in zip(gaps, gaps[1:]))
    assert pushes < Fraction(9, 2) and pushes + gaps[-1] == Fraction(9, 2)
    with pytest.raises(ValueError):
        remaining_gaps(1, 1, 3)


def test_the_corner_sends_everything_back():
    for v in ((1, 2, 3), (Fraction(1, 2), -4, 0)):
        back = corner_reflect(v)
        assert back == tuple(-Fraction(c) for c in v)
        assert corner_reflect(back) == tuple(Fraction(c) for c in v)
    assert opposite_digit_node("123") == "987"
    assert int("123") + int(opposite_digit_node("123")) == 1110
    assert opposite_digit_node("555") == "555"
    with pytest.raises(TypeError):
        corner_reflect((0.5, 0, 0))
