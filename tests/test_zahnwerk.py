"""Tests for raum27.zahnwerk: nine positions per wheel, carry at ten."""

import pytest

from raum27.zahnwerk import DIGITS, HOOK, from_value, step, tension, triggers, value, wheels_needed


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


def test_hook_zero_shows_zero_outside_and_opens_the_one_on_the_right():
    assert step([9, 0], low=HOOK) == ([0, 1], 2)            # 9 -> 10 = "1 there, 0 here"
    assert step([9, 9, 0], low=HOOK) == ([0, 0, 1], 3)      # 99 -> 100
    assert step([0, 1], -1, low=HOOK) == ([9, 0], 2)        # and back
    assert triggers(9, 1, low=HOOK) and triggers(0, -1, low=HOOK)
    assert not triggers(1, -1, low=HOOK)


def test_hook_mode_counts_nine_ninety_nine_nine_hundred_ninety_nine():
    for count, top in ((1, 9), (2, 99), (3, 999)):
        assert value([9] * count, low=HOOK) == top
    wheels = [0, 0, 0]
    for n in range(1000 - 1):
        assert value(wheels, low=HOOK) == n
        assert from_value(n, 3, low=HOOK) == wheels
        nxt, _ = step(wheels, low=HOOK)
        assert step(nxt, -1, low=HOOK)[0] == wheels
        wheels = nxt
    assert max(tension([9, 9], low=HOOK)) == 9


def test_both_modes_need_nine_wheels_for_three_hundred_million():
    assert wheels_needed(300_000_000) == 9
    assert wheels_needed(300_000_000, low=HOOK) == 9
    assert value([9] * 8, low=HOOK) == 99_999_999 < 300_000_000 <= value([9] * 9, low=HOOK)


def test_unknown_low_is_refused():
    with pytest.raises(ValueError):
        step([5], low=2)
