import pytest

from raum27.clockfree_scheduler import (
    Process,
    schedule_round_robin,
    schedule_run_to_completion,
)


def test_process_rejects_non_positive_work():
    with pytest.raises(ValueError):
        Process("p", 0)
    with pytest.raises(ValueError):
        Process("p", -1)


def test_run_to_completion_matches_total_work_exactly():
    procs = [Process("A", 3), Process("B", 100), Process("C", 7)]
    schedule = schedule_run_to_completion(procs)
    assert schedule.results[-1].completion_tick == sum(p.work_units for p in procs)
    assert schedule.context_switches == len(procs)


def test_run_to_completion_completion_order_matches_queue_order():
    procs = [Process("A", 3), Process("B", 1_000_000_000), Process("C", 100)]
    schedule = schedule_run_to_completion(procs)
    ticks = [r.completion_tick for r in schedule.results]
    assert ticks == [3, 1_000_000_003, 1_000_000_103]


def test_run_to_completion_causes_convoy_effect_for_short_job_behind_long_one():
    procs = [Process("long", 1_000_000_000), Process("short", 100)]
    schedule = schedule_run_to_completion(procs)
    waits = schedule.waiting_time_by_name()
    assert waits["short"] == 1_000_000_000
    assert waits["long"] == 0


def test_round_robin_bounds_short_job_wait_regardless_of_queue_order():
    procs = [Process("long", 1_000_000_000), Process("short", 100)]
    schedule = schedule_round_robin(procs, quantum=100)
    waits = schedule.waiting_time_by_name()
    assert waits["short"] < 1000


def test_round_robin_matches_total_work_exactly():
    procs = [Process("A", 250), Process("B", 90), Process("C", 4)]
    schedule = schedule_round_robin(procs, quantum=10)
    assert max(r.completion_tick for r in schedule.results) == sum(p.work_units for p in procs)


def test_round_robin_rejects_non_positive_quantum():
    with pytest.raises(ValueError):
        schedule_round_robin([Process("A", 1)], quantum=0)


def test_run_to_completion_has_fewer_context_switches_than_round_robin():
    procs = [Process("A", 300), Process("B", 300), Process("C", 300)]
    rtc = schedule_run_to_completion(procs)
    rr = schedule_round_robin(procs, quantum=10)
    assert rtc.context_switches < rr.context_switches


def test_single_process_both_schedulers_agree():
    procs = [Process("solo", 42)]
    rtc = schedule_run_to_completion(procs)
    rr = schedule_round_robin(procs, quantum=10)
    assert rtc.results[0].completion_tick == rr.results[0].completion_tick == 42
