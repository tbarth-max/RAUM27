"""Tests for raum27.zustandshologramm: wavelength steps recorded as 1 + 6 + 8 bits."""

from fractions import Fraction
import random

import pytest

from raum27.zustandshologramm import (
    BITS,
    OCTANTS,
    SEXTANTS,
    Record,
    delta,
    direction,
    elapsed_time,
    end_point_from_hologram,
    hologram,
    mirrored,
    navigate,
    pack,
    period,
    retrace,
    unpack,
    wavelength,
)

F = Fraction


def _records(n=500, seed=3):
    rng = random.Random(seed)
    out = []
    for _ in range(n):
        if rng.random() < 0.2:
            out.append(Record(rng.randint(1, 300), False))
        else:
            out.append(Record(rng.randint(1, 300), True, rng.randrange(64), rng.randrange(256)))
    return out


def test_step_is_wavelength_and_time_is_period():
    assert wavelength(300, 3) == 100
    assert wavelength(F(1, 2), 2) == F(1, 4)
    assert period(8) == F(1, 8)
    assert wavelength(7, 7) * 7 == 7
    with pytest.raises(TypeError):
        wavelength(0.5, 2)


def test_state_is_fifteen_bits_and_round_trips():
    assert BITS == 15
    for r in _records():
        assert 0 <= pack(r) < 1 << 15
        assert unpack(r.frequency, pack(r)) == r
    with pytest.raises(ValueError):
        unpack(1, 1 << 15)


@pytest.mark.parametrize("kwargs", [
    dict(frequency=0, pulse=True),
    dict(frequency=True, pulse=True),
    dict(frequency=1, pulse=True, sextant_bits=64),
    dict(frequency=1, pulse=True, octant_bits=256),
    dict(frequency=1, pulse=False, sextant_bits=1),
])
def test_invalid_records_are_refused(kwargs):
    with pytest.raises(ValueError):
        Record(**kwargs)


def test_single_directions():
    for bit, vector in enumerate(SEXTANTS):
        assert direction(Record(1, True, 1 << bit, 0)) == vector
    for bit, vector in enumerate(OCTANTS):
        assert direction(Record(1, True, 0, 1 << bit)) == vector
    assert direction(Record(5, False)) == (0, 0, 0)
    assert direction(Record(1, True, 0b000011, 0)) == (0, 0, 0)  # +x and -x cancel
    assert direction(Record(1, True, 0, 255)) == (0, 0, 0)       # all eight octants cancel


def test_delta_is_wavelength_times_direction():
    r = Record(4, True, 0b000001, 1 << 7)  # +x and octant (1, 1, 1)
    assert delta(r, 1) == (F(2, 4), F(1, 4), F(1, 4))


def test_way_back_returns_exactly():
    records = _records()
    start = (F(1, 3), 0, -2)
    out = navigate(start, records, F(299792458, 1000))
    back = navigate(out[-1], retrace(records), F(299792458, 1000))
    assert back[-1] == out[0]
    assert back == out[::-1]
    for r in records:
        assert mirrored(mirrored(r)) == r


def test_hologram_keeps_end_point_but_not_order():
    records = _records()
    speed = F(3, 2)
    keyed = hologram(records)
    assert sum(len(v) for v in keyed.values()) == len(records)
    assert end_point_from_hologram((0, 0, 0), keyed, speed) == navigate((0, 0, 0), records, speed)[-1]
    shuffled = records[:]
    random.Random(9).shuffle(shuffled)
    assert navigate((0, 0, 0), shuffled, speed)[-1] == navigate((0, 0, 0), records, speed)[-1]
    assert navigate((0, 0, 0), shuffled, speed) != navigate((0, 0, 0), records, speed)


def test_elapsed_time():
    assert elapsed_time([Record(2, False), Record(3, False), Record(6, False)]) == 1
    assert elapsed_time([]) == 0
