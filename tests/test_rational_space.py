from fractions import Fraction

import pytest

from raum27.rational_space import involution, is_fixed_point


@pytest.mark.parametrize("x", [Fraction(1, 1), Fraction(3, 7), Fraction(22, 5), Fraction(1, 100)])
def test_involution_is_involutive(x):
    assert involution(involution(x)) == x


def test_involution_fixed_point_is_one():
    assert involution(Fraction(1)) == Fraction(1)
    assert is_fixed_point(Fraction(1))


@pytest.mark.parametrize("x", [Fraction(2), Fraction(5, 3), Fraction(101)])
def test_involution_swaps_sides_of_one(x):
    assert x > 1
    assert involution(x) < 1


def test_zero_is_excluded():
    with pytest.raises(ValueError):
        involution(Fraction(0))
