"""Tests for raum27.stapelplan."""

from fractions import Fraction

import pytest

from raum27.stapelplan import (
    batch_interval, bottleneck, makespan, most_parts, part_times, seconds_per_item,
)

FIVE = [4, 4, 4, 4, 4]


def test_one_big_batch_waits_n_times_delta():
    assert makespan(FIVE) == 20
    assert seconds_per_item(4, 10000) == Fraction(36, 25)        # 1.44 s per sheet


def test_splitting_lets_the_next_stage_start_early():
    assert makespan(FIVE, parts=10) == Fraction(28, 5)           # 2 h + 9 * 0.4 h = 5.6 h
    assert makespan(FIVE, parts=4) == 8                          # 5 * 1 h + 3 * 1 h
    assert [makespan(FIVE, parts=k) for k in (1, 2, 4)] == [20, 12, 8]


def test_slowest_stage_sets_the_pace_and_instances_help_only_there():
    work = [4, 4, 8, 4, 4]
    assert bottleneck(work) == 2 and batch_interval(work) == 8
    assert batch_interval(work, [1, 1, 2, 1, 1]) == 4            # a second instance at stage 3
    assert batch_interval(work, [2, 1, 1, 1, 1]) == 8            # elsewhere: no gain
    assert makespan(work, [1, 1, 2, 1, 1], parts=4) == 8


def test_wake_intervals_cost_time_unless_staggered():
    assert makespan(FIVE, parts=4, wake=1, staggered=False) == 12
    assert makespan(FIVE, parts=4, wake=1) == 8
    assert most_parts(4, 1) == 4 and most_parts(4, Fraction(1, 60)) == 240 and most_parts(1, 4) == 1
    with pytest.raises(ValueError):
        most_parts(4, 0)


def test_input_checks():
    assert part_times([4, 2], [2, 1], parts=2) == [1, 1]
    with pytest.raises(ValueError):
        part_times([4, 4], [1])
    with pytest.raises(ValueError):
        part_times([4], parts=0)
    with pytest.raises(TypeError):
        part_times([4.0])
