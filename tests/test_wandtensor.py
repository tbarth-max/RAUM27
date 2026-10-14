"""Tests for raum27.wandtensor."""

from fractions import Fraction

import pytest

from raum27.biegelinie import three_point_chain
from raum27.wandtensor import chain, determinant, matrix, nine_steps, recover, step

EI = Fraction(1, 5)


def test_determinant_is_dx_cubed_over_twelve():
    assert determinant(Fraction(1, 8)) == Fraction(1, 6144)
    for dx in (Fraction(1, 9), Fraction(3, 2), 2):
        assert determinant(dx) == Fraction(dx) ** 3 / 12
    with pytest.raises(ValueError):
        matrix(0)
    with pytest.raises(TypeError):
        matrix(0.125)


def test_exact_for_linear_curvature_cantilever():
    line = chain(lambda x: EI * (1 - x), 1, 8)
    assert all(w == EI * (x * x / 2 - x ** 3 / 6) for x, w in line)


def test_not_exact_for_quadratic_curvature_but_three_points_are():
    curv = lambda x: EI * (1 - x) ** 2 / 2
    exact = lambda x: EI * (x * x / 4 - x ** 3 / 6 + x ** 4 / 24)
    end = chain(curv, 1, 8)[-1]
    assert exact(end[0]) - end[1] == Fraction(-1, 7680)
    assert all(w == exact(x) for x, w in three_point_chain(curv, 1, 8))


def test_two_states_give_the_curvatures_back():
    w, th = Fraction(1, 48), Fraction(3, 40)
    for fs, fe in ((Fraction(1, 10), Fraction(1, 20)), (Fraction(-2, 3), Fraction(5)), (0, 0)):
        w2, th2 = step(w, th, fs, fe, Fraction(1, 8))
        assert recover(w, th, w2, th2, Fraction(1, 8)) == (fs, fe)


def test_nine_fractions_denominators():
    rows = nine_steps()
    assert [d for _, _, d in rows] == [2187, 2187, 81, 2187, 2187, 81, 2187, 2187, 3]
    assert rows[-1][1] == Fraction(1, 3)                 # curvature 1 - x on [0, 1]: w(1) = 1/2 - 1/6
    assert 2187 == 3 ** 7 and 81 == 3 ** 4


def test_chain_needs_a_piece():
    with pytest.raises(ValueError):
        chain(lambda x: 0, 1, 0)
