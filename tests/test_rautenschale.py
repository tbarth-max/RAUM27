"""Tests for raum27.rautenschale."""

from fractions import Fraction
import itertools

import pytest

from raum27.rautenschale import (
    REST, balance_factor, closes, cos2_to_corner, fold, jump, kind, octant_diagonal,
    octree_address, octree_point, opposite, scale_shell_to_nine_halves, shell,
    sphere_r2_from_shell, unfold, unjump, xyzt_bits,
)

A = 9
FACE, EDGE, CORNER = (Fraction(A, 2), 0, 0), (Fraction(A, 2), Fraction(A, 2), 0), (Fraction(A, 2),) * 3


def test_shells_of_face_edge_corner_count_one_two_three():
    assert [shell(p) for p in (FACE, EDGE, CORNER)] == [Fraction(9, 2), 9, Fraction(27, 2)]
    assert [balance_factor(p) for p in (FACE, EDGE, CORNER)] == [1, 2, 3]
    for p in (FACE, EDGE, CORNER):
        assert sphere_r2_from_shell(shell(p), balance_factor(p)) == sum(c * c for c in p)


def test_angle_balances_rhombus_and_sphere_for_any_rational_point():
    for p in [(3, 1, -2), (Fraction(1, 3), Fraction(-5, 7), 2), (0, 4, -1)]:
        assert shell(p) ** 2 == 3 * cos2_to_corner(p) * sum(Fraction(c) ** 2 for c in p)
        assert 1 <= balance_factor(p) <= 3
    assert cos2_to_corner((1, 0, 0)) == Fraction(1, 3)                 # the magic angle
    with pytest.raises(ValueError):
        cos2_to_corner((0, 0, 0))
    with pytest.raises(ValueError):
        sphere_r2_from_shell(1, 0)
    with pytest.raises(TypeError):
        shell((0.5, 0, 0))


def test_scaling_onto_nine_halves_needs_no_root():
    q = scale_shell_to_nine_halves((3, 4, 0))
    assert q == (Fraction(27, 14), Fraction(18, 7), 0) and shell(q) == Fraction(9, 2)
    with pytest.raises(ValueError):
        scale_shell_to_nine_halves((0, 0, 0))


def test_octant_diagonal_and_zero_rule():
    assert octant_diagonal((1, -2, 3)) == (1, -1, 1)
    assert octant_diagonal((0, -1, 0)) == (1, -1, 1)
    assert octant_diagonal((0, -1, 0), zero_positive=False) == (-1, -1, -1)


def test_four_bits_hold_six_faces_and_eight_corners():
    faces = [tuple(s if i == j else 0 for j in range(3)) for i in range(3) for s in (1, -1)]
    corners = list(itertools.product((1, -1), repeat=3))
    face_words = {xyzt_bits(p) for p in faces}
    corner_words = {xyzt_bits(p) for p in corners}
    assert len(face_words) == 6 and all(kind(w) == "face" for w in face_words)
    assert len(corner_words) == 8 and all(kind(w) == "corner" for w in corner_words)
    assert face_words.isdisjoint(corner_words) and len(face_words | corner_words) == 14
    assert xyzt_bits((1, 0, 0)) == (1, 1, 0, 0) and xyzt_bits((1, 1, 1)) == (1, 0, 0, 0)
    for p in faces + corners:
        assert opposite(xyzt_bits(p)) == xyzt_bits(tuple(-c for c in p))
    assert xyzt_bits((0, 0, 0)) == REST and kind(REST) == "rest"
    assert xyzt_bits((1, 1, 0), zero_bit=1) == (1, 1, 1, 0)           # reading exactly 0: the open rule
    with pytest.raises(ValueError):
        kind((1, 1, 1, 1))
    with pytest.raises(ValueError):
        opposite(REST)


def test_octree_address_is_exact_both_ways():
    address, rest = octree_address((3, 1, -2), 2)
    assert address == [(1, 1, -1), (1, -1, 1)]
    assert rest == (Fraction(-3, 2), Fraction(-1, 2), Fraction(-7, 2))
    assert octree_point(address, rest) == (3, 1, -2)
    with pytest.raises(ValueError):
        octree_address((5, 0, 0), 1)


def test_fold_with_fraction_counts():
    assert fold(Fraction(7, 2)) == (3, Fraction(1, 2))                  # lands on the middle
    assert fold(Fraction(10, 3)) == (3, Fraction(2, 3))
    assert fold(Fraction(9, 4)) == (2, Fraction(1, 4))
    for c in (Fraction(7, 2), Fraction(10, 3), Fraction(9, 4), 0):
        assert unfold(*fold(c)) == c
    assert closes((2, 4, 6)) and not closes((2, 3, 4)) and not closes((Fraction(5, 2), 2, 2))
    with pytest.raises(ValueError):
        fold(-1)


def test_complexity_jump_and_way_back():
    assert jump(Fraction(1, 6), bits=2) == (2, Fraction(2, 3))
    assert unjump(2, Fraction(2, 3)) == Fraction(1, 6)
    assert jump(Fraction(1, 6)) == (2, Fraction(2, 3))
    assert jump(Fraction(1, 30), base=3) == (3, Fraction(9, 10))
    assert unjump(3, Fraction(9, 10), base=3) == Fraction(1, 30)
    assert jump(Fraction(3, 4)) == (0, Fraction(3, 4)) and jump(0) == (0, 0)
    with pytest.raises(ValueError):
        jump(1, bits=0)
