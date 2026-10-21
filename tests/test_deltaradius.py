"""Tests for raum27.deltaradius."""

from fractions import Fraction

import pytest

from raum27.deltaradius import (
    READINGS, Surd3, corner_to_axis_ratio, delta_radius, delta_radius_squared_difference,
    radial_speed, radii_squared, step_period,
)
from raum27.nennerordnung import Power
from raum27.rautenraum import cube_corners, face_apexes, squared_length

ORIGIN = (Fraction(0), Fraction(0), Fraction(0))


def test_radii_match_the_existing_modules():
    assert radii_squared(9, "wuerfel") == (Fraction(81, 4), Fraction(243, 4))
    r6, r8 = radii_squared(1, "raute")
    assert {squared_length(ORIGIN, p) for p in face_apexes()} == {r6} == {1}
    assert {squared_length(ORIGIN, p) for p in cube_corners()} == {r8} == {Fraction(3, 4)}


def test_delta_radius_is_exact_and_positive():
    cube = delta_radius(9, "wuerfel")
    assert cube == Surd3(Fraction(-9, 2), Fraction(9, 2))
    assert cube.sign() == 1 and float(cube) == pytest.approx(4.5 * (3 ** 0.5 - 1))
    rhomb = delta_radius(1, "raute")
    assert rhomb == Surd3(1, Fraction(-1, 2))
    assert rhomb.sign() == 1 and float(rhomb) == pytest.approx(1 - 3 ** 0.5 / 2)
    for reading in READINGS:                              # (r8 - r6)(r8 + r6) = r8² - r6²
        r6, r8 = radii_squared(2, reading)
        assert delta_radius_squared_difference(2, reading) == abs(r8 - r6)
    assert delta_radius_squared_difference(9, "wuerfel") == Fraction(81, 2)
    assert delta_radius_squared_difference(9, "raute") == Fraction(81, 4)


def test_squaring_the_delta_back():
    # cube: ΔR = (a/2)(sqrt3 - 1), so ΔR² = (a²/4)(4 - 2 sqrt3)
    d = delta_radius(2, "wuerfel")
    assert d * d == Surd3(4, -2)
    assert Surd3(-1, 1) * Surd3(1, 1) == Surd3(2, 0)     # (sqrt3 - 1)(sqrt3 + 1) = 2


def test_ratios():
    assert corner_to_axis_ratio("wuerfel") == Power.of(3).root(2)
    assert corner_to_axis_ratio("raute") ** 2 == Power.of(Fraction(3, 4))


def test_exact_sign_and_order():
    assert Surd3(0, 0).sign() == 0
    assert Surd3(0, -1).sign() == -1 and Surd3(5, 0).sign() == 1
    assert Surd3(2, -1).sign() == 1                        # 2 > sqrt3
    assert Surd3(1, -1).sign() == -1                       # 1 < sqrt3
    assert Surd3(-2, 1).sign() == -1 and Surd3(-1, 1).sign() == 1
    assert delta_radius(1, "raute") < delta_radius(1, "wuerfel")
    assert 2 * Surd3(1, 1) == Surd3(2, 2) == Surd3(1, 1) + Surd3(1, 1)
    assert Surd3(3, 2) - Surd3(1, 1) == Surd3(2, 1)


def test_dx_over_dt():
    assert step_period(16) == Fraction(1, 16)
    v = radial_speed(16, 9, "wuerfel")
    assert v == delta_radius(9, "wuerfel") * 16
    assert radial_speed(8, 9, "wuerfel") * 2 == v          # half the frequency, half the speed
    assert float(v) == pytest.approx(16 * 4.5 * (3 ** 0.5 - 1))


def test_rejects_bad_input():
    with pytest.raises(ValueError):
        delta_radius(0)
    with pytest.raises(ValueError):
        delta_radius(9, "kugel")
    with pytest.raises(TypeError):
        delta_radius(1.5)
    with pytest.raises(TypeError):
        Surd3(True, 0)
    with pytest.raises(TypeError):
        Surd3(1, 0) * 0.5
    with pytest.raises(ValueError):
        radial_speed(0)
