"""Tests for raum27.messnetz."""

from fractions import Fraction
import math

import pytest

from raum27.messnetz import (
    AXIS_SENSORS,
    CORNER_SENSORS,
    arrival_time_classes,
    bragg_shift,
    energy_swing,
    height_from_poles,
    hub_response,
    landauer,
    log_step,
    radius_error,
    resolved_terms,
    synthetic_wavelength,
    triangulation,
)

F = Fraction


def test_single_hub_sensor_sees_only_the_ring_and_is_blind_to_a_tear():
    intact = hub_response()
    torn = hub_response(cut=((2, 0),))
    for node in intact:
        assert intact[node] == pytest.approx(torn[node], abs=1e-12)
    rings = {round(v, 9) for v in intact.values()}
    assert len(rings) == 3


def test_four_threads_triangulate_every_touch_point_by_force_ratio():
    touch, distinct, gap, signal = triangulation((0, 2, 4, 6))
    assert touch == 168 and distinct == 168
    assert 0.003 < gap / signal < 0.006           # about 0.4 % of full scale
    assert triangulation(tuple(range(8)))[2] > 2.5 * gap
    assert triangulation((0, 1))[1] == 168


def test_arrival_times_alone_tell_few_points_apart():
    touch, distinct = arrival_time_classes((0, 2, 4, 6))
    assert touch == 168 and distinct == 16


def test_six_plus_eight_sensors_resolve_full_second_order():
    assert resolved_terms(AXIS_SENSORS, 2) == 6
    assert resolved_terms(CORNER_SENSORS, 2) == 7
    assert resolved_terms(AXIS_SENSORS + CORNER_SENSORS, 2) == 9
    assert resolved_terms(AXIS_SENSORS + CORNER_SENSORS, 3) == 13
    assert resolved_terms(AXIS_SENSORS, 1) == 4


def test_ninety_degrees_from_equal_pole_distances():
    assert height_from_poles((3, 4, F(1, 2))) == F(1, 2)
    assert height_from_poles((F(2, 7), -5, 0)) == 0
    assert height_from_poles((0, 0, F(-3, 4))) == F(-3, 4)


def test_energy_stands_still_only_at_ninety_degrees():
    assert energy_swing(math.pi / 2) == pytest.approx(0, abs=1e-15)
    assert energy_swing(0) == 2 and energy_swing(math.pi) == pytest.approx(2)
    assert energy_swing(math.pi / 4) == pytest.approx(math.sqrt(2))


def test_light_wavelengths_and_colour_shift():
    assert F(300_000_000) / 300_000_000 == 1                  # 300 MHz -> 1 m
    assert synthetic_wavelength(650, 450) == F(2925, 2)       # 1462.5 nm
    assert math.lcm(650, 532, 450) == 1_556_100
    assert bragg_shift(1550, F(1, 1000)) == F(1209, 1000)     # 1.209 nm at 0.1 % strain
    with pytest.raises(ValueError):
        synthetic_wavelength(532, 532)


def test_limits():
    assert log_step(14, 100) == pytest.approx(1.01416, rel=1e-4)
    assert log_step(8, 100) == pytest.approx(2.4582, rel=1e-4)
    assert landauer(300) == pytest.approx(2.87e-21, rel=1e-2)
    errors = [radius_error(h, 1e-4) for h in (0.5, 0.1, 0.03)]
    assert errors[0] < errors[1] < errors[2]                  # closer points, worse radius
