"""Tests for raum27.kurvenkette."""

import math

import pytest

from raum27.kurvenkette import (
    GOLDEN_COS,
    K,
    PEAK_LINE_SLOPE,
    catenary_length,
    closest_return,
    curve_inverse,
    curve_sin,
    curve_sin2,
    curve_sinh,
    diagonal_crossing,
    dome_ring_force,
    joint_phases,
    peak,
    rotation_field,
    torus_flow,
)

LAMBDAS = (0.5, 1.0, 3.0, 17.0)


def test_common_slope_sixteen_ninths_for_every_lambda():
    h = 1e-7
    for lam in LAMBDAS:
        assert curve_sin(h, lam) / h == pytest.approx(16 / 9, rel=1e-6)
        assert curve_sinh(h, lam) / h == pytest.approx(16 / 9, rel=1e-6)
        assert curve_sin2(1e-4, lam) / 1e-8 == pytest.approx(256 / 81 / lam, rel=1e-3)
        assert curve_sin(9 * math.pi * lam / 8, lam) == pytest.approx(0, abs=1e-9)


def test_inverse_times_curve_is_one():
    for lam in LAMBDAS:
        for x in (0.01, 0.3, 1.1):
            assert curve_sin(x, lam) * curve_inverse(x, lam) == pytest.approx(1)


def test_order_for_small_x_refutes_sin_above_sinh():
    for lam in LAMBDAS:
        for x in (0.001, 0.05, 0.3):
            assert curve_inverse(x, lam) > curve_sinh(x, lam) > curve_sin(x, lam) > curve_sin2(x, lam)


def test_peaks_lie_on_one_line_at_48_5_degrees():
    for lam in LAMBDAS:
        x, y = peak(lam)
        assert y / x == pytest.approx(PEAK_LINE_SLOPE)
        assert curve_sin(x, lam) == pytest.approx(lam)
        crossing = diagonal_crossing(lam)
        assert curve_sin(crossing, lam) == pytest.approx(crossing)
        assert x < crossing                                   # just past the peak
    assert math.degrees(math.atan(PEAK_LINE_SLOPE)) == pytest.approx(48.537, abs=1e-3)
    assert K != math.pi / 2


def test_six_and_eight_share_a_bit_eight_and_nine_do_not():
    assert joint_phases(6, 8) == (24, 24)
    assert joint_phases(8, 9) == (72, 72)
    assert joint_phases(8, 3) == (24, 24)
    assert (8 / 6) ** 2 == pytest.approx(16 / 9)


def test_chain_length_is_sinh_and_dome_limit_is_golden():
    a = 9 * 2.0 / 16
    assert catenary_length(1.3, a) == pytest.approx(a * math.sinh(1.3 / a), rel=1e-6)
    assert GOLDEN_COS ** 2 + GOLDEN_COS - 1 == pytest.approx(0, abs=1e-15)
    phi = math.acos(GOLDEN_COS)
    assert math.degrees(phi) == pytest.approx(51.83, abs=0.01)
    assert dome_ring_force(phi) == pytest.approx(0, abs=1e-12)
    assert dome_ring_force(phi - 0.1) < 0 < dome_ring_force(phi + 0.1)  # compression above, tension below


def test_rotation_on_the_ball_vanishes_only_at_the_poles_the_torus_never():
    zeros = []
    for i in range(0, 181, 5):
        for j in range(0, 360, 10):
            t, p = math.radians(i), math.radians(j)
            point = (math.sin(t) * math.cos(p), math.sin(t) * math.sin(p), math.cos(t))
            if max(abs(c) for c in rotation_field(point)) < 1e-12:
                zeros.append(round(point[2], 9))
    assert set(zeros) == {1.0, -1.0}
    assert min(math.hypot(*torus_flow(math.radians(i), math.radians(j)))
               for i in range(0, 360, 5) for j in range(0, 360, 5)) >= 1.0 - 1e-12


def test_rational_winding_closes_irrational_comes_ever_nearer():
    assert closest_return(3 / 4, 4) == pytest.approx(0, abs=1e-12)
    near = [closest_return(math.sqrt(2) - 1, n) for n in (10, 100, 1000, 10000)]
    assert all(b < a for a, b in zip(near, near[1:]))
    assert near[-1] > 0


def test_inverse_falls_below_sinh_near_nine_sixteenths():
    # small-x forms 9/(16x) and 16x/9 meet at x = 9/16; the true curves cross close to it
    for lam in (1.0, 3.0, 17.0):
        assert curve_inverse(0.5, lam) > curve_sinh(0.5, lam)
        assert curve_inverse(0.65, lam) < curve_sinh(0.65, lam)
