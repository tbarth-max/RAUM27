"""Tests for raum27.ricci_kugel."""

from fractions import Fraction

import pytest

from raum27.ricci_kugel import extinction_time, max_curvature, radius_squared, shrink_rate, surgery_time

R0 = Fraction(81, 4)                                           # the 9/2 sphere


def test_round_spheres_shrink_linearly_in_r_squared():
    assert shrink_rate(2) == -2 and shrink_rate(3) == -4
    assert extinction_time(R0, 2) == Fraction(81, 8)           # 2-sphere
    assert extinction_time(R0, 3) == Fraction(81, 16)          # 3-sphere (Poincare's case)
    assert radius_squared(R0, 1, 3) == Fraction(65, 4)
    assert radius_squared(R0, Fraction(81, 32), 3) == Fraction(81, 8)   # half the time, half of r^2
    with pytest.raises(ValueError):
        radius_squared(R0, extinction_time(R0, 3), 3)          # radius 0 is never entered
    with pytest.raises(ValueError):
        shrink_rate(1)


def test_stopped_at_the_smallest_point():
    t = surgery_time(R0, 9, 3)
    assert t == (R0 - Fraction(1, 81)) / 4 < extinction_time(R0, 3)
    assert radius_squared(R0, t, 3) == Fraction(1, 81)         # the cap: radius 1/9, not 0
    assert 1 / radius_squared(R0, t, 3) == max_curvature(9) == 81
    with pytest.raises(ValueError):
        surgery_time(Fraction(1, 100), 9)
    with pytest.raises(TypeError):
        radius_squared(20.25, 0)
