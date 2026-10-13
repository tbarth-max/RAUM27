"""Tests for raum27.synchronlog: chained deltas, lockstep, worlds that map back."""

from fractions import Fraction
import random

import pytest

from raum27.synchronlog import append, replay, state_digest, to_reality, to_world, verify

F = Fraction


def _log(n=50, seed=2):
    rng = random.Random(seed)
    log = []
    for _ in range(n):
        log = append(log, {rng.choice("xyz"): F(rng.randint(-9, 9), rng.randint(1, 9))})
    return log


def test_chain_holds_and_any_change_in_the_past_is_found():
    log = _log()
    assert verify(log) is None
    forged = [dict(e) for e in log]
    forged[17] = {**forged[17], "delta": {"x": F(1000)}}
    assert verify(forged) == 17


def test_lockstep_participants_compute_the_same_state_exactly():
    log = _log()
    states = [replay(log, {"x": F(1, 3)}) for _ in range(3)]       # three participants
    assert states[0] == states[1] == states[2]
    assert len({state_digest(s) for s in states}) == 1


def test_floats_drift_where_fractions_do_not():
    # the same additions in two orders: exact fractions agree, binary floats need not
    values = [F(1, 10), F(2, 10), F(3, 10)]
    assert sum(values) == sum(reversed(values))
    assert (0.1 + 0.2) + 0.3 != 0.1 + (0.2 + 0.3)


def test_a_game_world_maps_back_to_reality_exactly():
    reality = replay(_log(), {"x": 0})
    maps = {"x": (F(16, 9), 5), "y": (-3, F(1, 2)), "z": (F(1, 27), 0)}
    world = to_world(reality, maps)
    assert world != reality
    assert to_reality(world, maps) == reality
    with pytest.raises(ValueError):
        to_world(reality, {"x": (0, 1)})
    with pytest.raises(ValueError):
        to_reality(world, {"x": (0, 1)})


def test_floats_are_refused_in_the_log():
    with pytest.raises(TypeError):
        append([], {"x": 0.5})
