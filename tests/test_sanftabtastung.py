"""Tests for raum27.sanftabtastung: wake gently."""

import math

import pytest

from raum27.sanftabtastung import (
    alarm_states,
    respond,
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


def test_alarm_is_one_hard_pulse_with_the_same_total_budget():
    mode, pulses, response = respond(9.0, critical=5.0, noise=1.0, disturbance_limit=0.1,
                                     omega0=230.0, quality=40)
    assert (mode, pulses) == ("alarm", 1)
    assert response == pytest.approx(4.0)                          # k sigma at once
    calm = respond(1.0, critical=5.0, noise=1.0, disturbance_limit=0.1, omega0=230.0, quality=40)
    assert calm[0] == "gentle" and calm[1] == 1600
    assert pulses * response ** 2 == pytest.approx(calm[1] * calm[2] ** 2)   # same energy
    assert calm[1] / pulses == 1600                                # answered 1600 times sooner


def test_hysteresis_does_not_flutter_at_the_edge():
    readings = [1, 4.9, 5.1, 4.9, 5.1, 4.0, 3.1, 2.9, 3.5, 5.0]
    assert alarm_states(readings, on=5.0, off=3.0) == [
        False, False, True, True, True, True, True, False, False, True]
    flutter = [r >= 5.0 for r in readings]                          # a single threshold flips twice as often
    flips = lambda xs: sum(a != b for a, b in zip(xs, xs[1:]))
    assert flips(flutter) > flips(alarm_states(readings, on=5.0, off=3.0))
    with pytest.raises(ValueError):
        alarm_states(readings, on=3.0, off=5.0)
