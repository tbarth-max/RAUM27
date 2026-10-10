"""Tests for raum27.kugelkoordinaten."""
from __future__ import annotations

import math
from fractions import Fraction

import pytest

from raum27.cube_symmetry import face_diagonal_squared
from raum27.kugelkoordinaten import (
    NIVEN_TURN_FRACTIONS,
    cayley_menger_determinant,
    cos_squared_polar,
    equidistant_squared_distances,
    exact_cos_squared_turns,
    exact_spherical,
    fits_in_dimension,
    four_stroke_place_count,
    from_exact_spherical,
    max_equidistant_points,
    rational_cos_squared_of_turn,
    rational_cosine_of_turn,
    squared_distance,
    squared_radius,
    tan_azimuth,
)
from raum27.viertakt import period

RATIONAL_POINTS = (
    (Fraction(1), Fraction(2), Fraction(3)),
    (Fraction(3), Fraction(4), Fraction(12)),
    (Fraction(-5), Fraction(2), Fraction(1)),
    (Fraction(1, 3), Fraction(2, 5), Fraction(7, 2)),
    (Fraction(7), Fraction(-24), Fraction(0)),
    (Fraction(-1), Fraction(-1), Fraction(-1)),
)


def test_the_forwarded_scripts_example_was_exact_only_by_luck():
    """25 happens to be a perfect square. Move one endpoint and the root
    is irrational, while the squared form stays exact."""
    p1 = (Fraction(1), Fraction(2), Fraction(3))
    p2 = (Fraction(4), Fraction(6), Fraction(3))
    assert squared_distance(p1, p2) == 25
    assert math.isqrt(25) == 5
    # one endpoint moved: still exact as a square, irrational as a root
    p3 = (Fraction(1), Fraction(1), Fraction(1))
    assert squared_distance(p1, p3) == 5
    root = math.isqrt(5)
    assert root * root != 5


def test_the_full_direction_of_a_rational_point_is_exactly_rational():
    """No arccos, no arctan, no rounding -- and it agrees with the float
    computation the script performed."""
    for p in RATIONAL_POINTS:
        x, y, z = p
        r2 = squared_radius(p)
        assert r2 == x * x + y * y + z * z
        c2 = cos_squared_polar(p)
        assert c2 == z * z / r2
        # float cross-check against acos/atan2
        r = math.sqrt(float(r2))
        theta = math.acos(float(z) / r)
        assert math.cos(theta) ** 2 == pytest.approx(float(c2), abs=1e-12)
        t = tan_azimuth(p)
        if t is not None:
            phi = math.atan2(float(y), float(x))
            assert math.tan(phi) == pytest.approx(float(t), abs=1e-9)


def test_the_worked_value_from_the_script():
    p = (Fraction(1), Fraction(2), Fraction(3))
    assert squared_radius(p) == 14
    assert cos_squared_polar(p) == Fraction(9, 14)
    assert tan_azimuth(p) == 2


def test_the_exact_spherical_representation_is_lossless():
    """Given (r^2, cos^2 theta, tan phi) and three sign bits the point
    comes back exactly -- so refusing the square root gives nothing up."""
    for p in RATIONAL_POINTS:
        r2, c2, t, signs = exact_spherical(p)
        assert from_exact_spherical(r2, c2, t, signs) == p


def test_it_is_lossless_on_the_x_equals_zero_axis_too():
    for p in ((Fraction(0), Fraction(3), Fraction(4)), (Fraction(0), Fraction(0), Fraction(5))):
        r2, c2, t, signs = exact_spherical(p)
        assert t is None
        assert from_exact_spherical(r2, c2, t, signs) == p


def test_the_origin_has_no_direction():
    with pytest.raises(ValueError):
        cos_squared_polar((Fraction(0), Fraction(0), Fraction(0)))
    with pytest.raises(ValueError):
        exact_spherical((Fraction(0), Fraction(0), Fraction(0)))


def test_only_eight_turn_fractions_have_a_rational_cosine():
    """Niven's theorem, as an enumeration."""
    assert len(NIVEN_TURN_FRACTIONS) == 8
    expected = {Fraction(0), Fraction(1, 6), Fraction(1, 4), Fraction(1, 3),
                Fraction(1, 2), Fraction(2, 3), Fraction(3, 4), Fraction(5, 6)}
    assert {q for q, _ in NIVEN_TURN_FRACTIONS} == expected
    for q, cosine in NIVEN_TURN_FRACTIONS:
        assert cosine in (Fraction(0), Fraction(1), Fraction(-1),
                          Fraction(1, 2), Fraction(-1, 2))
        assert math.cos(2 * math.pi * float(q)) == pytest.approx(float(cosine), abs=1e-12)
    # denominators are only 1, 2, 3, 4, 6
    assert {q.denominator for q, _ in NIVEN_TURN_FRACTIONS} == {1, 2, 3, 4, 6}


def test_other_turn_fractions_return_none_rather_than_a_rounded_value():
    for q in (Fraction(1, 5), Fraction(1, 7), Fraction(1, 8), Fraction(1, 12), Fraction(2, 7)):
        assert rational_cosine_of_turn(q) is None


def test_the_quarter_turns_of_the_four_stroke_are_among_the_exact_eight():
    """viertakt runs on q = 0, 1/4, 1/2, 3/4 -- four of the eight."""
    for q in (Fraction(0), Fraction(1, 4), Fraction(1, 2), Fraction(3, 4)):
        cosine = rational_cosine_of_turn(q)
        assert cosine is not None
        assert cosine in (Fraction(0), Fraction(1), Fraction(-1))
    assert four_stroke_place_count() == period() == 4


def test_the_squared_convention_doubles_the_exact_set():
    """cos^2 = (1 + cos 2x)/2, so 1/8 and 1/12 become exact even though
    their cosines are not."""
    turns = exact_cos_squared_turns()
    assert len(turns) == 16
    assert len(NIVEN_TURN_FRACTIONS) == 8
    assert rational_cos_squared_of_turn(Fraction(1, 8)) == Fraction(1, 2)
    assert rational_cos_squared_of_turn(Fraction(1, 12)) == Fraction(3, 4)
    assert rational_cosine_of_turn(Fraction(1, 8)) is None
    assert rational_cosine_of_turn(Fraction(1, 12)) is None
    # every exact cos^2 value agrees with the float
    for q in turns:
        value = rational_cos_squared_of_turn(q)
        assert math.cos(2 * math.pi * float(q)) ** 2 == pytest.approx(float(value), abs=1e-12)


def test_the_squared_set_contains_the_cosine_set():
    for q, _ in NIVEN_TURN_FRACTIONS:
        assert rational_cos_squared_of_turn(q) is not None


def test_the_half_turn_cos_squared_matches_the_cube_convention():
    """1/8 of a turn gives cos^2 = 1/2, i.e. the face diagonal's own
    squared ratio -- the same reason cube_symmetry keeps squares."""
    assert rational_cos_squared_of_turn(Fraction(1, 8)) == Fraction(1, 2)
    assert face_diagonal_squared(Fraction(1)) == 2
    assert rational_cos_squared_of_turn(Fraction(1, 8)) == 1 / face_diagonal_squared(Fraction(1))


def test_equidistant_points_span_one_dimension_per_extra_point():
    """CM determinant +-m, so m points span m-1 dimensions."""
    for m in range(2, 7):
        determinant = cayley_menger_determinant(equidistant_squared_distances(m))
        assert abs(determinant) == m
        assert determinant != 0


def test_five_equidistant_points_cannot_be_realised_in_three_space():
    """THE OBSTRUCTION: leaving the fourth dimension out is not a
    concession to drawing. The determinant would have to vanish and it
    is -5."""
    d2 = equidistant_squared_distances(5)
    assert cayley_menger_determinant(d2) == -5
    assert not fits_in_dimension(d2, 3)
    assert fits_in_dimension(d2, 4)
    assert max_equidistant_points(3) == 4
    assert max_equidistant_points(4) == 5


def test_the_determinant_vanishes_for_configurations_that_really_are_flat():
    """Cross-check, so the test above is not reading an artefact: four
    corners of a square give 0, a tetrahedron gives 8."""
    square = [(Fraction(0), Fraction(0)), (Fraction(1), Fraction(0)),
              (Fraction(1), Fraction(1)), (Fraction(0), Fraction(1))]
    d2 = [[squared_distance(p, q) for q in square] for p in square]
    assert cayley_menger_determinant(d2) == 0
    assert fits_in_dimension(d2, 2)

    tetra = [(Fraction(0), Fraction(0), Fraction(0)), (Fraction(1), Fraction(0), Fraction(0)),
             (Fraction(0), Fraction(1), Fraction(0)), (Fraction(0), Fraction(0), Fraction(1))]
    d2 = [[squared_distance(p, q) for q in tetra] for p in tetra]
    assert cayley_menger_determinant(d2) == 8
    assert fits_in_dimension(d2, 3)


def test_four_equidistant_points_do_fit_in_three_space():
    d2 = equidistant_squared_distances(4)
    assert fits_in_dimension(d2, 3)
    assert cayley_menger_determinant(d2) == 4


def test_indexing_from_zero_is_still_four_places():
    """Never in dispute: 0,1,2,3 is four, exactly as 1,2,3,4 is. The
    shift moves only where the count starts."""
    assert four_stroke_place_count() == 4
    assert len(range(0, 4)) == len(range(1, 5)) == 4
    assert period() == 4


def test_degenerate_inputs_raise():
    with pytest.raises(ValueError):
        squared_distance((Fraction(1), Fraction(2)), (Fraction(1), Fraction(2), Fraction(3)))
    with pytest.raises(ValueError):
        cos_squared_polar((Fraction(1), Fraction(2)))
    with pytest.raises(ValueError):
        tan_azimuth((Fraction(1), Fraction(2)))
    with pytest.raises(ValueError):
        cayley_menger_determinant([[Fraction(0)]])
    with pytest.raises(ValueError):
        max_equidistant_points(0)
    with pytest.raises(ValueError):
        equidistant_squared_distances(1)
