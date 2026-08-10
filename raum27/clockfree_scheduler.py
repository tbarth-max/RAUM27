"""Clock-free ("taktfrei") vs. time-sliced process scheduling.

The notes propose replacing a fixed-quantum ("tick") scheduler with one
that runs each process to completion of its own workload, arguing this is
more efficient because it never spends a tick on a process that has
nothing left to do. That much is true, and is implemented here as
`schedule_run_to_completion` -- it is exactly the classical *first-come,
first-served, non-preemptive* discipline.

What the notes don't mention is the classical failure mode of that same
discipline: if a short job queues up behind a long one, it waits for the
long job's *entire* runtime before it gets to run at all (the "convoy
effect"). `schedule_round_robin` is the standard preemptive baseline that
trades a fixed number of extra context switches for bounding that worst
case. Which one is actually better depends on the workload and the queue
order -- see milestones/06_taktfreier_kernel for the benchmark.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class Process:
    name: str
    work_units: int

    def __post_init__(self) -> None:
        if self.work_units <= 0:
            raise ValueError(f"work_units must be positive: {self.work_units}")


@dataclass(frozen=True)
class ScheduleResult:
    name: str
    completion_tick: int
    waiting_time: int


@dataclass(frozen=True)
class Schedule:
    results: list[ScheduleResult]
    context_switches: int

    def waiting_time_by_name(self) -> dict[str, int]:
        return {r.name: r.waiting_time for r in self.results}

    def average_waiting_time(self) -> float:
        return sum(r.waiting_time for r in self.results) / len(self.results)


def schedule_run_to_completion(processes: Sequence[Process]) -> Schedule:
    """Clock-free scheduling: run each process, in queue order, until its
    own work is exhausted, before starting the next. No preemption."""
    results = []
    clock = 0
    for p in processes:
        clock += p.work_units
        results.append(ScheduleResult(p.name, clock, clock - p.work_units))
    return Schedule(results, context_switches=len(processes))


def schedule_round_robin(processes: Sequence[Process], quantum: int) -> Schedule:
    """Classic time-sliced preemptive scheduling: each process gets at
    most `quantum` operations per turn, then is requeued behind the others
    if work remains."""
    if quantum <= 0:
        raise ValueError(f"quantum must be positive: {quantum}")
    remaining = {p.name: p.work_units for p in processes}
    queue = deque(p.name for p in processes)
    clock = 0
    context_switches = 0
    completion_tick: dict[str, int] = {}
    while queue:
        name = queue.popleft()
        context_switches += 1
        slice_ = min(quantum, remaining[name])
        clock += slice_
        remaining[name] -= slice_
        if remaining[name] == 0:
            completion_tick[name] = clock
        else:
            queue.append(name)
    results = [
        ScheduleResult(p.name, completion_tick[p.name], completion_tick[p.name] - p.work_units)
        for p in processes
    ]
    return Schedule(results, context_switches)
