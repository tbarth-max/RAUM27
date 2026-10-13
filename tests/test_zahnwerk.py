"""Tests for raum27.zahnwerk: nine positions per wheel, carry at ten."""

import pytest

from raum27.zahnwerk import DIGITS, from_value, step, tension, triggers, value, wheels_needed


def test_ninth_click_turns_the_next_wheel():
    wheels, moved = step([9, 1, 1])
    assert wheels == [1, 2, 1] and moved == 2
    wheels, moved = step([9, 9, 1])
    assert wheels == [1, 1, 2] and moved == 3
    wheels, moved = step([4, 7, 2])
    assert wheels == [5, 7, 2] and moved == 1


def test_back_and_forth_inside_one_to_nine():
    wheels = [1, 1]
    for _ in range(8):
        wheels, moved = step(wheels)
        assert moved == 1
    assert wheels == [9, 1]
    for _ in range(8):
        wheels, moved = step(wheels, -1)
        assert moved == 1
    assert wheels == [1, 1]


def test_borrow_is_the_mirror_of_carry():
    assert step([1, 2, 1], -1) == ([9, 1, 1], 2)
    assert step([1, 1, 3], -1) == ([9, 9, 2], 3)


def test_every_click_is_undone_exactly_and_counts_by_one():
    wheels = [1, 1, 1]
    for n in range(DIGITS ** 3 - 1):
        assert value(wheels) == n
        nxt, _ = step(wheels)
        assert step(nxt, -1)[0] == wheels
        wheels = nxt
    assert wheels == [9, 9, 9]


def test_full_train_and_zero_point_refuse_to_wrap():
    with pytest.raises(OverflowError):
        step([9, 9, 9])
    with pytest.raises(OverflowError):
        step([1, 1, 1], -1)


def test_tension_is_bounded_however_long_it_runs():
    wheels = [1, 1, 1, 1]
    worst = 0
    for _ in range(5000):
        wheels, _ = step(wheels)
        worst = max(worst, max(tension(wheels)))
    assert worst == DIGITS - 1


def test_value_and_from_value_are_inverse():
    for n in range(0, DIGITS ** 4, 37):
        assert value(from_value(n, 4)) == n
    assert from_value(0, 3) == [1, 1, 1]
    assert from_value(DIGITS ** 3 - 1, 3) == [9, 9, 9]


def test_nine_wheels_are_the_first_to_hold_three_hundred_million():
    assert DIGITS ** 8 == 43_046_721 < 300_000_000 <= DIGITS ** 9 == 387_420_489
    assert wheels_needed(300_000_000) == 9
    assert wheels_needed(1) == 1


@pytest.mark.parametrize("call", [
    lambda: step([0, 1]),
    lambda: step([10]),
    lambda: step([]),
    lambda: step([1], 2),
    lambda: from_value(DIGITS ** 2, 2),
    lambda: from_value(-1, 2),
    lambda: from_value(0, 0),
    lambda: wheels_needed(0),
])
def test_invalid_inputs(call):
    with pytest.raises(ValueError):
        call()


def test_duplex_trigger_condition_matches_the_train():
    fired = {(p, d) for p in range(1, 10) for d in (1, -1) if triggers(p, d)}
    assert fired == {(9, 1), (1, -1)}
    for first in range(1, 10):
        for d in (1, -1):
            _, moved = step([first, 5], d)
            assert (moved > 1) == triggers(first, d)
    with pytest.raises(ValueError):
        triggers(0, 1)
    with pytest.raises(ValueError):
        triggers(5, 0)
