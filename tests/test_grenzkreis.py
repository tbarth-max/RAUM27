"""Tests for raum27.grenzkreis: guard only the edge, roll back when it tears."""

from fractions import Fraction
import random

import pytest

from raum27.grenzkreis import crossings, guarded_run, inside, rewind

F = Fraction


def test_quiet_run_never_triggers_and_rewinds_exactly():
    rng = random.Random(4)
    start = {"x": F(1), "y": F(-2), "z": F(0)}
    deltas = []
    for _ in range(200):
        key = rng.choice("xyz")
        deltas.append({key: F(rng.choice((-1, 1)), rng.randint(2, 9))})
    final, accepted, events = guarded_run(start, deltas)
    assert events == [] or all(names for _, names in events)
    assert inside(final, 10)
    assert rewind(final, accepted) == start


def test_tear_is_located_and_the_step_does_not_stand():
    start = {"north": F(8), "east": F(0), "down": F(-3)}
    deltas = [{"north": F(1, 2)}, {"east": F(4)}, {"north": F(2)}, {"down": F(-1)}]
    final, accepted, events = guarded_run(start, deltas)
    assert events == [(2, ["north"])]                       # step 2 would reach 10.5 in the north
    assert final == {"north": F(17, 2), "east": F(4), "down": F(-4)}
    assert len(accepted) == 3
    assert rewind(final, accepted) == start


def test_reaching_exactly_ten_is_already_a_tear():
    final, accepted, events = guarded_run({"a": F(9)}, [{"a": F(1)}])
    assert events == [(0, ["a"])] and final == {"a": F(9)} and accepted == []
    assert crossings({"a": F(10), "b": F(-10), "c": F(9)}, 10) == ["a", "b"]


def test_bad_starts_and_values_are_refused():
    with pytest.raises(ValueError):
        guarded_run({"a": F(12)}, [])
    with pytest.raises(TypeError):
        guarded_run({"a": 0.5}, [])
