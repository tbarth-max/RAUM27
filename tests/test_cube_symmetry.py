from fractions import Fraction

from raum27.cube_symmetry import (
    axis_cross_product,
    corner_directions,
    coupling_constant,
    cube_center,
    face_diagonal_midpoint,
    face_diagonal_squared,
    face_directions,
    space_diagonal_midpoint,
    space_diagonal_squared,
    space_diagonals,
    vector_equilibrium,
)


def test_six_face_directions():
    faces = face_directions()
    assert len(faces) == 6
    assert len(set(faces)) == 6


def test_eight_corner_directions():
    corners = corner_directions()
    assert len(corners) == 8
    assert len(set(corners)) == 8
    assert all(abs(c) == 1 for corner in corners for c in corner)


def test_vector_equilibrium_is_zero():
    assert vector_equilibrium() == (0, 0, 0)


def test_coupling_constant_is_four_thirds():
    c = coupling_constant()
    assert c == Fraction(4, 3)
    assert c**2 == Fraction(16, 9)


def test_axis_cross_products_recover_the_third_face_direction():
    ex, ey, ez = (1, 0, 0), (0, 1, 0), (0, 0, 1)
    assert axis_cross_product(ex, ey) == ez
    assert axis_cross_product(ey, ez) == ex
    assert axis_cross_product(ez, ex) == ey


def test_eight_corners_collapse_into_four_space_diagonals():
    diagonals = space_diagonals()
    assert len(diagonals) == 4
    covered = set()
    for pair in diagonals:
        assert len(pair) == 2
        covered |= pair
    assert covered == set(corner_directions())


def test_face_diagonal_is_sqrt2_space_diagonal_is_sqrt3():
    # Squared lengths, in exact rational arithmetic: sqrt(2)^2 = 2, sqrt(3)^2 = 3.
    assert face_diagonal_squared(Fraction(1)) == Fraction(2)
    assert space_diagonal_squared(Fraction(1)) == Fraction(3)


def test_only_the_space_diagonal_passes_through_the_cube_center():
    center = cube_center(Fraction(1))
    assert center == (Fraction(1, 2), Fraction(1, 2), Fraction(1, 2))
    assert space_diagonal_midpoint(Fraction(1)) == center
    assert face_diagonal_midpoint(Fraction(1)) != center


def test_diagonal_facts_scale_with_edge_length():
    edge = Fraction(5)
    assert face_diagonal_squared(edge) == 2 * edge**2
    assert space_diagonal_squared(edge) == 3 * edge**2
    assert space_diagonal_midpoint(edge) == cube_center(edge)
