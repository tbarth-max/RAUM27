"""Tests for raum27.schallgrenze."""

from fractions import Fraction

import pytest

from raum27.schallgrenze import (
    expansion_cap_cubed, first_x_beyond_c, mirrored, speed_squared, stiffness_for_speed,
    work_at_constant_pressure,
)

WATER_K, WATER_RHO = 2200000000, 1000            # 2.2 GPa, 1000 kg/m^3
LEAD_K, LEAD_RHO = 46000000000, 11340
DIAMOND_K, DIAMOND_RHO = 443000000000, 3510


def test_stiffness_over_density_not_density_alone():
    assert speed_squared(WATER_K, WATER_RHO) == 2200000                  # about 1483 m/s
    assert 1480 ** 2 < speed_squared(WATER_K, WATER_RHO) < 1485 ** 2
    assert 2000 ** 2 < speed_squared(LEAD_K, LEAD_RHO) < 2020 ** 2       # dense, slow
    assert speed_squared(DIAMOND_K, DIAMOND_RHO) > 10000 ** 2            # 3.5 x water, fast
    ratio = stiffness_for_speed(300000000, WATER_RHO) / WATER_K
    assert 4 * 10 ** 10 < ratio < Fraction(42, 10) * 10 ** 10            # "about 40 billion times"
    with pytest.raises(ValueError):
        speed_squared(0, 1)
    with pytest.raises(TypeError):
        speed_squared(1.0, 1)


def test_expansion_and_compression_mirror_around_c0():
    base = speed_squared(WATER_K, WATER_RHO)
    for x in (2, Fraction(3, 2), 10):
        exp2, comp2 = mirrored(WATER_K, WATER_RHO, x)
        assert exp2 * comp2 == base * base                               # the product never moves
        assert exp2 > base > comp2
    assert mirrored(WATER_K, WATER_RHO, 1) == (base, base)
    with pytest.raises(ValueError):
        mirrored(WATER_K, WATER_RHO, 0)


def test_the_light_limit_caps_the_expansion():
    cap = expansion_cap_cubed(WATER_K, WATER_RHO)
    x = first_x_beyond_c(WATER_K, WATER_RHO)
    assert x == 3446
    assert (x - 1) ** 3 <= cap < x ** 3
    assert mirrored(WATER_K, WATER_RHO, x)[0] > 300000000 ** 2
    assert mirrored(WATER_K, WATER_RHO, x - 1)[0] <= 300000000 ** 2


def test_keeping_the_pressure_costs_work():
    assert work_at_constant_pressure(100000, 1, 8) == 700000             # 1 bar, volume x8 (x = 2)
    assert work_at_constant_pressure(100000, 1, 1) == 0
