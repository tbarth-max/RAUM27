"""Tests for raum27.sanftabtastung: wake gently."""

import math

import pytest

from raum27.sanftabtastung import (
    detection_energy,
    detection_rate,
    gentle_plan,
    required_response,
    resonance_gain,
)


def test_splitting_lowers_each_touch_but_not_the_total():
    noise = 0.5
    assert required_response(noise, 100) == pytest.approx(required_response(noise, 1) / 10)
    totals = [detection_energy(noise, n) for n in (1, 10, 100, 10_000)]
    assert all(t == pytest.approx((4 * noise) ** 2) for t in totals)


def test_resonance_answers_q_times_and_falls_off_beside_it():
    q = 50
    assert resonance_gain(1.0, 1.0, q) == pytest.approx(q)
    assert resonance_gain(0.0, 1.0, q) == pytest.approx(1.0)        # a slow push
    assert resonance_gain(1.2, 1.0, q) < q / 10                      # 20 % off: far weaker
    assert resonance_gain(3.0, 1.0, q) < 1                           # far above: less than a push


def test_plan_keeps_every_touch_below_the_limit():
    repeats, response, drive = gentle_plan(noise=1.0, disturbance_limit=0.1, omega0=230.0, quality=40)
    assert response <= 0.1 + 1e-12
    assert repeats == math.ceil((4 * 1.0 / 0.1) ** 2) == 1600
    assert drive == pytest.approx(response / 40)


def test_planned_whisper_is_still_heard():
    repeats, response, _ = gentle_plan(noise=1.0, disturbance_limit=0.2, omega0=1.0, quality=10)
    assert detection_rate(response, 1.0, repeats) > 0.97
    assert detection_rate(0.0, 1.0, repeats) < 0.05                  # silence is not mistaken for an answer


def test_invalid_inputs():
    with pytest.raises(ValueError):
        required_response(0, 1)
    with pytest.raises(ValueError):
        resonance_gain(1, 0, 1)
    with pytest.raises(ValueError):
        gentle_plan(1, 0, 1, 1)
