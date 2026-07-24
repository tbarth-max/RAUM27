from fractions import Fraction

from raum27.cube_symmetry import (
    corner_directions,
    coupling_constant,
    face_directions,
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
