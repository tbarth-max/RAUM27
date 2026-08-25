from fractions import Fraction

from raum27.kern_modul_v1 import (
    all_corners,
    complement_contribution,
    face_contribution,
    face_diagonal,
    flip_x,
    flip_y,
    flip_z,
    octant_solid_angle,
    parity,
    reachable,
    redundancy_holds,
    space_diagonal,
    tdoa_position,
)

START = (0, 0, 0)


def test_one_reflection_reaches_only_two_corners():
    assert len(reachable(START, [flip_x])) == 2


def test_two_reflections_reach_only_four_corners():
    assert len(reachable(START, [flip_x, flip_y])) == 4


def test_three_reflections_reach_all_eight_corners():
    assert reachable(START, [flip_x, flip_y, flip_z]) == set(all_corners())


def test_octant_solid_angle_is_one_half_of_four_pi_sr():
    assert octant_solid_angle() == Fraction(1, 2)


def test_parity_is_four_and_four():
    corners = all_corners()
    even = sum(1 for c in corners if parity(c) == 0)
    odd = sum(1 for c in corners if parity(c) == 1)
    assert even == 4
    assert odd == 4


def test_edge_flip_always_toggles_parity():
    assert all(parity(flip_x(c)) != parity(c) for c in all_corners())


def test_face_diagonal_never_toggles_parity():
    assert all(parity(face_diagonal(c)) == parity(c) for c in all_corners())


def test_space_diagonal_always_toggles_parity():
    assert all(parity(space_diagonal(c)) != parity(c) for c in all_corners())


def test_tdoa_at_zero_delay_is_the_midpoint():
    L, v = Fraction(100), Fraction(343)
    assert tdoa_position(L, v, Fraction(0)) == L / 2


def test_tdoa_is_linear_in_delay():
    L, v = Fraction(100), Fraction(343)
    dt1, dt2 = Fraction(1, 10), Fraction(3, 10)
    diff = tdoa_position(L, v, dt1) - tdoa_position(L, v, dt2)
    assert diff == -v * (dt1 - dt2) / 2


def test_redundancy_condition_for_various_rationals():
    for x in [Fraction(7, 3), Fraction(-5, 2), Fraction(1, 1000), Fraction(999)]:
        assert redundancy_holds(x)


def test_face_and_complement_contribution_agree_numerically():
    # They agree on the number -- but complement_contribution doesn't
    # independently derive it, see its docstring.
    assert face_contribution() == complement_contribution() == Fraction(1, 9)


def test_complement_contribution_is_true_by_construction_not_derivation():
    # Demonstrates the point made in the docstring: swap in any other
    # assumed share and the complement identity "works" the same way,
    # which is exactly why it isn't independent confirmation of 8/9.
    assumed_other_share = Fraction(5, 9)
    assert Fraction(1) - assumed_other_share == Fraction(4, 9)
