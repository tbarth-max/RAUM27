"""Tests for raum27.wuerfelgeometrie."""

from fractions import Fraction
import math

import pytest

from raum27.wuerfelgeometrie import (
    AXIS_DIRECTIONS,
    DIAGONAL_DIRECTIONS,
    archimedes_bounds,
    cube_symmetries,
    dual_exponent,
    element_orders,
    line_count_rank,
    octant_cube_sharing,
    plane_area_ratio,
    shells,
    solid_volume_ratio,
    views_are_ambiguous,
)


def test_twenty_seven_is_one_six_twelve_eight():
    assert shells() == {0: 1, 1: 6, 2: 12, 3: 8}
    assert sum(shells().values()) == 27 == (1 + 2) ** 3


def test_reflection_eight_times_rotation_six_is_forty_eight():
    assert len(cube_symmetries()) == 48 == 8 * 6
    assert element_orders(rotations_only=True) == {1: 1, 2: 9, 3: 8, 4: 6}
    assert element_orders() == {1: 1, 2: 19, 3: 8, 4: 12, 6: 8}
    assert 8 not in element_orders()


def test_shape_ratios():
    assert plane_area_ratio() == (2, 4)            # rhombus : circle : square = 2 : pi : 4
    assert solid_volume_ratio() == (1, 6)          # octahedron : sphere : cube = 1 : pi : 6
    previous = None
    for k in range(6):
        inner, outer = archimedes_bounds(k)
        assert inner < math.pi < outer
        if previous:
            assert outer - inner < (previous[1] - previous[0]) / 3.5
        previous = (inner, outer)
    assert archimedes_bounds(0) == pytest.approx((2 * math.sqrt(2), 4.0))


def test_sphere_is_the_only_self_dual_exponent():
    assert dual_exponent(1) is None and dual_exponent(None) == 1
    assert dual_exponent(2) == 2
    assert dual_exponent(3) == Fraction(3, 2) and dual_exponent(Fraction(3, 2)) == 3
    for p in (Fraction(5, 4), 3, 7, Fraction(11, 3)):
        assert dual_exponent(dual_exponent(p)) == p
        assert dual_exponent(p) != p
    with pytest.raises(ValueError):
        dual_exponent(Fraction(1, 2))


def test_axis_views_are_ambiguous_by_the_two_tetrahedra():
    found = views_are_ambiguous(AXIS_DIRECTIONS)
    assert found is not None
    plus, minus = found
    assert len(plus) == len(minus) == 4
    # the two sets are the even and odd corners of one small cube
    corners = set(plus) | set(minus)
    xs, ys, zs = ({c[i] for c in corners} for i in range(3))
    assert len(xs) == len(ys) == len(zs) == 2
    parity = lambda c: sum(c) % 2
    assert len({parity(c) for c in plus}) == 1 and len({parity(c) for c in minus}) == 1
    assert line_count_rank(AXIS_DIRECTIONS) == 19


def test_axes_plus_one_octant_direction_decide_every_body():
    assert views_are_ambiguous(AXIS_DIRECTIONS + DIAGONAL_DIRECTIONS[:1]) is None
    assert line_count_rank(AXIS_DIRECTIONS + DIAGONAL_DIRECTIONS[:1]) == 26
    assert line_count_rank(AXIS_DIRECTIONS + DIAGONAL_DIRECTIONS[:2]) == 27


def test_eight_octant_cubes_meet_in_the_27_points_with_binary_sharing():
    sharing = octant_cube_sharing()
    assert sharing == {8: 1, 4: 6, 2: 12, 1: 8}
    assert sum(sharing.values()) == 27
    assert sum(k * v for k, v in sharing.items()) == 8 * 8      # every cube has its 8 corners
