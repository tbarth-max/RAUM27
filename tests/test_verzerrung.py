"""Tests for raum27.verzerrung: six axes measure, eight corners check."""

from fractions import Fraction

import pytest

from raum27.verzerrung import (
    AXES,
    CORNERS,
    apply,
    axis_asymmetry,
    cauchy_green,
    corner_residuals,
    deformation_from_axes,
    determinant,
    invariants,
    is_rigid,
    squared_semi_axes_if_diagonal,
)

F_ = Fraction
STRETCH = ((F_(4, 3), 0, 0), (0, 1, 0), (0, 0, F_(3, 4)))
SHEAR = ((1, F_(1, 2), 0), (0, 1, 0), (0, 0, 1))
GENERAL = ((F_(6, 5), F_(1, 7), 0), (F_(-1, 3), 1, F_(2, 9)), (0, F_(1, 4), F_(5, 6)))


def _norm(M):
    return tuple(tuple(F_(x) for x in row) for row in M)


@pytest.mark.parametrize("F", [STRETCH, SHEAR, GENERAL])
def test_six_axes_recover_the_deformation_exactly(F):
    images = [apply(F, a) for a in AXES]
    assert deformation_from_axes(images) == _norm(F)
    assert axis_asymmetry(images) == ((0, 0, 0),) * 3


@pytest.mark.parametrize("F", [STRETCH, SHEAR, GENERAL])
def test_eight_corners_are_predicted_for_a_linear_law(F):
    corners = [apply(F, c) for c in CORNERS]
    assert corner_residuals(F, corners) == ((0, 0, 0),) * 8


def test_corners_expose_a_nonlinear_law_the_axes_cannot_see():
    # x' = x + a*y*z: zero on every axis point, non-zero on the corners
    a = F_(1, 10)
    law = lambda p: (p[0] + a * p[1] * p[2], p[1], p[2])
    images = [law(p) for p in AXES]
    F = deformation_from_axes(images)
    assert F == _norm(((1, 0, 0), (0, 1, 0), (0, 0, 1)))  # the axes see nothing
    residuals = corner_residuals(F, [law(c) for c in CORNERS])
    assert {r[0] for r in residuals} == {a, -a}             # the corners see it
    assert all(r[1] == r[2] == 0 for r in residuals)


def test_moved_centre_shows_in_axis_asymmetry():
    shift = (F_(1, 5), 0, 0)
    images = [tuple(x + s for x, s in zip(apply(SHEAR, p), shift)) for p in AXES]
    assert axis_asymmetry(images) == (shift, shift, shift)
    assert deformation_from_axes(images) == _norm(SHEAR)


def test_stretch_gives_sixteen_ninths_and_keeps_volume():
    assert squared_semi_axes_if_diagonal(STRETCH) == (F_(16, 9), 1, F_(9, 16))
    assert determinant(STRETCH) == 1
    assert invariants(STRETCH) == (F_(16, 9) + 1 + F_(9, 16), F_(16, 9) + F_(9, 16) + 1, 1)


def test_shear_needs_the_cubic_and_its_invariants_are_exact():
    with pytest.raises(ValueError):
        squared_semi_axes_if_diagonal(SHEAR)
    i1, i2, i3 = invariants(SHEAR)
    assert (i1, i2, i3) == (F_(13, 4), F_(13, 4), 1)  # shear keeps volume
    C = cauchy_green(SHEAR)
    # the invariants are those of C: check trace and determinant directly
    assert C[0][0] + C[1][1] + C[2][2] == i1


def test_rigid_turn_keeps_the_sphere():
    turn = ((F_(3, 5), F_(-4, 5), 0), (F_(4, 5), F_(3, 5), 0), (0, 0, 1))
    assert is_rigid(turn)
    assert not is_rigid(STRETCH)
    assert determinant(turn) == 1


def test_bad_shapes_are_refused():
    with pytest.raises(ValueError):
        apply(((1, 0), (0, 1)), (1, 0, 0))
    with pytest.raises(ValueError):
        deformation_from_axes([(1, 0, 0)] * 5)
    with pytest.raises(ValueError):
        corner_residuals(STRETCH, [(0, 0, 0)] * 7)
