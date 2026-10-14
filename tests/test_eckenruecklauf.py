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


def test_turning_about_the_diagonal_meets_six_faces_and_keeps_six_symmetries():
    from itertools import permutations
    from raum27.eckenruecklauf import axis_keepers, split_along_axis
    keepers = axis_keepers()
    assert len(keepers) == 6
    assert all(s == (1, 1, 1) for p, s in keepers)                      # no sign flips
    assert sorted(p for p, s in keepers) == sorted(permutations(range(3)))
    h = Fraction(9, 2)
    faces = [(h, 0, 0), (-h, 0, 0), (0, h, 0), (0, -h, 0), (0, 0, h), (0, 0, -h)]
    for f in faces:
        along, across = split_along_axis(f)
        assert (along, across) == (Fraction(27, 4), Fraction(27, 2))
        assert along + across == h * h                                   # 9/2 from the centre
    # across-parts of neighbouring faces are 60 degrees apart: cos = 1/2
    def across(v):
        d = sum(v) / 3
        return tuple(c - d for c in v)
    a, b = across(faces[0]), across(faces[5])                            # +x and -z
    dot = sum(x * y for x, y in zip(a, b))
    norm2 = sum(x * x for x in a)
    assert dot / norm2 == Fraction(1, 2)
