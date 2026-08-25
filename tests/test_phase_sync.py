import math

import pytest

from raum27.phase_sync import (
    beat_period,
    is_synchronized,
    phase_angle,
    phase_difference,
)


def test_phase_difference_is_symmetric_and_bounded():
    for a, b in [(0.0, 0.0), (1.0, 5.0), (6.0, 0.1), (3.14, -3.14)]:
        d_ab = phase_difference(a, b)
        d_ba = phase_difference(b, a)
        assert math.isclose(d_ab, d_ba)
        assert 0.0 <= d_ab <= math.pi + 1e-9


def test_phase_difference_of_equal_angles_is_zero():
    assert phase_difference(1.2345, 1.2345) == pytest.approx(0.0)


def test_same_frequency_same_phase_is_always_synchronized():
    f = 3.0
    for t in (0.0, 0.1, 1.0, 7.3, 100.0):
        assert is_synchronized(t, f, f)


def test_same_frequency_with_phase_offset_is_never_synchronized():
    f = 3.0
    for t in (0.0, 0.1, 1.0, 7.3, 100.0):
        assert not is_synchronized(t, f, f, phi2=1.0)


def test_beat_period_matches_measured_sync_interval():
    f1, f2 = 5.0, 5.3
    theory = beat_period(f1, f2)
    assert theory == pytest.approx(1.0 / 0.3)

    dt = 1e-4
    t_max = 5.0
    steps = int(t_max / dt)

    sync_times = []
    was_synced = False
    for i in range(steps):
        t = i * dt
        synced = is_synchronized(t, f1, f2)
        if synced and not was_synced:
            sync_times.append(t)
        was_synced = synced

    gaps = [b - a for a, b in zip(sync_times, sync_times[1:])]
    measured = sum(gaps) / len(gaps)
    assert measured == pytest.approx(theory, rel=0.05)


def test_beat_period_raises_for_equal_frequencies():
    with pytest.raises(ValueError):
        beat_period(4.0, 4.0)


def test_phase_angle_is_linear_in_time():
    f = 2.0
    assert phase_angle(0.0, f) == pytest.approx(0.0)
    assert phase_angle(1.0, f) == pytest.approx(2 * math.pi * f)
    assert phase_angle(0.5, f, phase=1.0) == pytest.approx(math.pi * f + 1.0)
