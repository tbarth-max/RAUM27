"""Meilenstein 6: Taktfreier Scheduler -- ehrlich benchmarked.

The source notes' pitch is: replace a fixed-quantum ("tick") scheduler
with one that runs every process to completion of its own workload
("taktfrei"), using exactly the example from the notes -- three processes
needing 3, 1_000_000_000 and 100 operations respectively.

That is implemented here as `schedule_run_to_completion` (a real,
tested policy: raum27/clockfree_scheduler.py). This script does not just
narrate it -- it runs both that scheduler and the classical time-sliced
round-robin baseline on the notes' own workload and reports what actually
happens, including the failure mode the notes don't mention: the convoy
effect. Which policy wins depends on the workload and the queue order,
not on which one is described as "more elegant".
"""

from raum27.clockfree_scheduler import (
    Process,
    schedule_round_robin,
    schedule_run_to_completion,
)


def report(title: str, procs: list[Process], quantum: int) -> None:
    print(f"\n=== {title} ===")
    print(f"processes (queue order): {[(p.name, p.work_units) for p in procs]}")

    rtc = schedule_run_to_completion(procs)
    rr = schedule_round_robin(procs, quantum=quantum)

    print(f"\n{'name':<8}{'work':>14}{'RTC wait':>14}{'RR wait (q='+str(quantum)+')':>18}")
    rtc_wait = rtc.waiting_time_by_name()
    rr_wait = rr.waiting_time_by_name()
    for p in procs:
        print(f"{p.name:<8}{p.work_units:>14}{rtc_wait[p.name]:>14}{rr_wait[p.name]:>18}")

    print(
        f"\ncontext switches -- run-to-completion: {rtc.context_switches}, "
        f"round-robin: {rr.context_switches}"
    )
    print(
        f"average waiting time -- run-to-completion: {rtc.average_waiting_time():.1f}, "
        f"round-robin: {rr.average_waiting_time():.1f}"
    )


def main() -> None:
    # Exactly the workload and queue order from the notes' worked example.
    notes_example = [
        Process("A", 3),
        Process("B", 1_000_000_000),
        Process("C", 100),
    ]
    report("Notes' own example (long job queued before two short ones)", notes_example, quantum=1000)

    # Same three processes, queue reordered short-jobs-first.
    reordered = [
        Process("A", 3),
        Process("C", 100),
        Process("B", 1_000_000_000),
    ]
    report("Same workload, short jobs queued first", reordered, quantum=1000)

    print(
        "\nConclusion: run-to-completion ('taktfrei') has fewer context "
        "switches and, when short jobs happen to be queued first, the "
        "lowest possible waiting time for everyone -- it is a real, "
        "verified efficiency win in that case. But it is not a free "
        "lunch: queue a short job behind a long one (the notes' own "
        "example) and run-to-completion makes it wait for the long job's "
        "*entire* runtime (the classical 'convoy effect'), which "
        "round-robin bounds by design regardless of queue order. Neither "
        "policy is unconditionally better; which one to use depends on "
        "whether job sizes are known in advance and how they get queued."
    )


if __name__ == "__main__":
    main()
