from fractions import Fraction

from raum27.cube_symmetry import (
    axis_cross_product,
    corner_directions,
    coupling_constant,
    cube_center,
    cube_volume,
    face_diagonal_midpoint,
    face_diagonal_squared,
    face_directions,
    pyramid_apex_to_corner_squared,
    pyramid_base_half_diagonal_squared,
    pyramid_height,
    pyramid_volume,
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


def test_coupling_constant_reciprocal_squared_is_nine_sixteenths():
    """(1/coupling_constant())**2 = 9/16, exactly: coupling_constant is
    corners/faces = 8/6 = 4/3 (already established above), so its
    reciprocal is faces/corners = 6/8 = 3/4, and squaring that gives
    9/16. Both 16/9 and 9/16 trace back to this one already-verified
    ratio -- not to two separately-asserted "base values"."""
    c = coupling_constant()
    assert (1 / c) == Fraction(3, 4)
    assert (1 / c) ** 2 == Fraction(9, 16)


def test_coupling_constant_cubed_is_not_sixteen_ninths():
    """SQUARING coupling_constant gives 16/9 exactly (see above).
    CUBING it does not -- (4/3)**3 = 64/27, not 16/9. Worth pinning down
    explicitly: an earlier claim in this project's history asserted
    (4/3)**3 = 16/9 and was wrong (64/27 =/= 16/9); the exponent matters,
    and only the square holds."""
    c = coupling_constant()
    assert c**3 == Fraction(64, 27)
    assert c**3 != Fraction(16, 9)


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


def test_pyramid_dimensions_for_radius_one_cube():
    # edge=2: center-to-face distance ("radius") = 1.
    edge = Fraction(2)
    assert pyramid_height(edge) == Fraction(1)
    assert pyramid_base_half_diagonal_squared(edge) == Fraction(2)  # sqrt(2)
    assert pyramid_apex_to_corner_squared(edge) == Fraction(3)      # sqrt(3)


def test_pyramid_apex_to_corner_matches_half_the_space_diagonal():
    for edge in (Fraction(1), Fraction(2), Fraction(5), Fraction(7, 3)):
        assert pyramid_apex_to_corner_squared(edge) == space_diagonal_squared(edge) / 4


def test_six_pyramids_fill_the_cube_exactly():
    for edge in (Fraction(1), Fraction(2), Fraction(3), Fraction(5, 2)):
        assert 6 * pyramid_volume(edge) == cube_volume(edge)
