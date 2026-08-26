"""Tests for raum27.kern_modul_v2.

The one test that matters most here is test_periodicity_control_has_real_assert:
the source this module was ported from ran the equivalent check, printed a
number, and asserted nothing -- it could not fail no matter what came out.
This file gives it an actual, empirically-grounded threshold.
"""
from __future__ import annotations

from fractions import Fraction

import numpy as np

from raum27 import kern_modul_v2 as k


def determinant3(rows):
    (a, b, c), (d, e, f), (g, h, i) = rows
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def test_rotate_about_x_is_a_rotation_not_a_reflection():
    matrix = [k.rotate_about_x((1, 0, 0)), k.rotate_about_x((0, 1, 0)), k.rotate_about_x((0, 0, 1))]
    columns = list(zip(*matrix))
    assert determinant3(columns) == 1


def test_rotate_about_y_is_a_rotation_not_a_reflection():
    matrix = [k.rotate_about_y((1, 0, 0)), k.rotate_about_y((0, 1, 0)), k.rotate_about_y((0, 0, 1))]
    columns = list(zip(*matrix))
    assert determinant3(columns) == 1


def test_reconstruct_face_directions_gives_exactly_six_unit_axes():
    faces = k.reconstruct_face_directions()
    assert faces == {
        (1, 0, 0), (-1, 0, 0),
        (0, 1, 0), (0, -1, 0),
        (0, 0, 1), (0, 0, -1),
    }


def test_reconstruct_corners_gives_all_eight_signed_triples():
    faces = k.reconstruct_face_directions()
    corners = k.reconstruct_corners(faces)
    assert corners == {(x, y, z) for x in (1, -1) for y in (1, -1) for z in (1, -1)}


def test_initial_rays_are_eight_evenly_spaced_directions():
    rays = k.initial_rays()
    assert len(rays) == 8
    assert k.is_evenly_spaced(rays)


def test_bisect_rays_doubles_count_and_stays_evenly_spaced():
    rays = k.initial_rays()
    for expected_len in (16, 32, 64):
        rays = k.bisect_rays(rays)
        assert len(rays) == expected_len
        assert k.is_evenly_spaced(rays)


def test_bisect_rays_is_pure_with_no_hidden_accumulating_state():
    """Guards against the Super-Crystal-style bug seen elsewhere in the
    source package: a function that silently grows a global each call.
    bisect_rays takes no global state, so the same input must always give
    the same output, no matter how many times it's been called before."""
    rays = k.initial_rays()
    first_call = k.bisect_rays(list(rays))
    for _ in range(50):
        k.bisect_rays(list(rays))
    later_call = k.bisect_rays(list(rays))
    assert first_call == later_call


def test_tdoa_position_matches_closed_form():
    L, v, dt = Fraction(300), Fraction(3), Fraction(10)
    assert k.tdoa_position(L, v, dt) == Fraction(135)


def test_velocity_wavelength_roundtrip_is_an_identity():
    v_true = Fraction(343, 1)
    frequency = Fraction(50, 1)
    wavelength = k.wavelength_from_velocity_and_frequency(v_true, frequency)
    recovered = k.velocity_from_wavelength_and_frequency(wavelength, frequency)
    assert recovered == v_true


def test_redundancy_correction_recovers_true_value_within_noise():
    rng = np.random.default_rng(1)
    x_true = 5.0
    reading = k.averaged_reading(x_true, noise=0.01, n_axes=16, rng=rng)
    assert abs(reading - x_true) < 0.2


def test_find_period_detects_a_planted_period():
    t = np.arange(60)
    series = np.sin(2 * np.pi * t / 6)
    assert k.find_period(series, max_period=20) == 6


def test_periodicity_control_has_real_assert():
    """The bug being fixed: the source printed false_positive_counts and
    asserted nothing. Here we require the winning candidate period on pure
    random (period-free) noise not dominate the trials. Empirically, across
    10 independent seeds x 500 trials x 18 candidate lags, the observed max
    share was 6.8%-8.6% against a uniform baseline of 1/18 = 5.6%. A method
    that quietly always reports the same period would show up here as a
    fraction near 1.0, not 0.08 -- so 0.15 is a real, non-flaky bound.
    """
    rng = np.random.default_rng(7)
    counts = k.false_positive_counts(rng, trials=500)
    total = sum(counts.values())
    winning_period, winning_count = counts.most_common(1)[0]
    assert winning_count / total < 0.15, (
        f"period {winning_period} won {winning_count}/{total} trials on pure "
        "random data -- the detector is biased toward reporting a fixed period"
    )


def test_redundancy_state_third_slot_is_always_exactly_one():
    for x in (Fraction(2), Fraction(1, 3), Fraction(1618, 1000), Fraction(-7, 5)):
        state = k.redundancy_state(x)
        assert state == (x, 1 / x, Fraction(1))


def test_redundancy_deviation_at_reference_is_zero():
    assert k.redundancy_deviation(Fraction(1)) == 0
    assert k.redundancy_deviation(Fraction(5), reference=Fraction(5)) == 0


def test_redundancy_deviation_is_symmetric_under_inversion():
    for n, d in ((3, 1), (7, 2), (1, 5), (11, 4)):
        x = Fraction(n, d)
        assert k.redundancy_deviation(x) == k.redundancy_deviation(1 / x)


def test_redundancy_deviation_increases_moving_away_from_one_in_each_direction():
    above_one = [Fraction(10 + n, 10) for n in range(0, 90)]
    values_above = [k.redundancy_deviation(x) for x in above_one]
    assert all(values_above[i] < values_above[i + 1] for i in range(len(values_above) - 1))

    below_one = [Fraction(n, 100) for n in range(1, 101)]
    values_below = [k.redundancy_deviation(x) for x in below_one]
    assert all(values_below[i] > values_below[i + 1] for i in range(len(values_below) - 1))


def test_redundancy_deviation_not_monotonic_in_plain_distance_from_reference():
    """deviation(2) == deviation(1/2) even though |2-1| != |1/2-1| -- the
    quantity is symmetric under x -> 1/x, not a function of |x-1| alone.
    Documented here so this isn't silently mis-described as such later."""
    assert k.redundancy_deviation(Fraction(2)) == k.redundancy_deviation(Fraction(1, 2))
    assert abs(Fraction(2) - 1) != abs(Fraction(1, 2) - 1)
