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


def test_raum27_points_spin_like_a_sphere_and_imbalance_grows_with_speed():
    from itertools import product
    from raum27.eckenruecklauf import imbalance_force, inertia_tensor, is_isotropic
    h = Fraction(9, 2)
    corners = list(product((-h, h), repeat=3))
    faces = [(h, 0, 0), (-h, 0, 0), (0, h, 0), (0, -h, 0), (0, 0, h), (0, 0, -h)]
    grid27 = list(product((-h, 0, h), repeat=3))
    tetra = [(h, h, h), (h, -h, -h), (-h, h, -h), (-h, -h, h)]
    for pts in (corners, faces, grid27, tetra, corners + faces + [(0, 0, 0)]):
        assert is_isotropic(inertia_tensor(pts))
    assert inertia_tensor(corners)[0][0] == 8 * (h * h + h * h)
    assert not is_isotropic(inertia_tensor(faces + [(h, h, 0)]))      # one extra mass breaks it
    assert not is_isotropic(inertia_tensor([(h, 0, 0), (-h, 0, 0)]))
    assert imbalance_force(1, Fraction(1, 100), 20) == 4              # m w^2 r
    assert imbalance_force(1, Fraction(1, 100), 40) == 16             # twice as fast, four times the pull
    assert imbalance_force(1, 0, 1000) == 0                           # centred: no pull at any speed


def test_only_the_deviation_from_the_sphere_remains():
    from itertools import product
    from raum27.eckenruecklauf import deviation_from_sphere, inertia_tensor
    h = Fraction(9, 2)
    grid27 = list(product((-h, 0, h), repeat=3))
    zero = [[0] * 3 for _ in range(3)]
    assert deviation_from_sphere(inertia_tensor(grid27)) == zero        # reference state: nothing to store
    dev = deviation_from_sphere(inertia_tensor(grid27 + [(h, h, 0)]))
    assert dev != zero
    assert sum(dev[i][i] for i in range(3)) == 0                        # traceless
    assert dev[0][1] == dev[1][0] == -h * h                             # the extra mass shows where it sits


def test_eight_corners_seen_along_the_diagonal_are_a_hexagon_and_two_at_the_centre():
    from itertools import product
    from raum27.eckenruecklauf import across_axis
    shadows = [across_axis(c) for c in product((-1, 1), repeat=3)]
    centre = [s for s in shadows if s == (0, 0, 0)]
    ring = [s for s in shadows if s != (0, 0, 0)]
    assert len(centre) == 2 and len(ring) == 6                          # the octet pattern: 6 + 2
    assert {sum(c * c for c in s) for s in ring} == {Fraction(8, 3)}    # all on one circle
    cosines = sorted({sum(a * b for a, b in zip(s, t)) / Fraction(8, 3) for s in ring for t in ring if s != t})
    assert cosines == [-1, Fraction(-1, 2), Fraction(1, 2)]            # 60-degree steps: a regular hexagon
    # in 3D none of them is at radius 0 -- the zero is only the shadow
    assert all(sum(c * c for c in corner) == 3 for corner in product((-1, 1), repeat=3))
    # 8 = 2^3 and 9 = 3^2: the only two neighbouring perfect powers (Catalan / Mihailescu)
    powers = sorted({b ** e for b in range(2, 40) for e in range(2, 12) if b ** e < 10 ** 6})
    assert [(a, b) for a, b in zip(powers, powers[1:]) if b - a == 1] == [(8, 9)]
