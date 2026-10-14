"""Batch cascade: how long a chain of agents takes, and how to split the batch.

Stage i needs w_i hours for one full batch (e.g. 10 000 sheets) and may
run m_i instances side by side. Splitting the batch into k equal parts
lets the next stage start early; the chain then behaves like a flow
line with identical parts, exactly:

    t_i      = w_i / (m_i * k)                 time of one part at stage i
    makespan = sum(t_i) + (k - 1) * max(t_i)    first part in .. last part out

    k = 1, five stages of 4 h:   20 h
    k = 10:                      2 h + 9 * 0.4 h = 5.6 h

Steady state: one full batch every max_i(w_i / m_i) -- the slowest stage
sets the pace, and an extra instance helps only there. Agents that only
wake every ``wake`` hours add up to one wake interval per hand-over
unless their wake times are staggered, and a part shorter than the wake
interval just waits -- so with hourly wakes and a 4 h stage, k <= 4.
"""

from fractions import Fraction


def _exact(*values):
    for v in values:
        if isinstance(v, float):
            raise TypeError("exact module: use int or Fraction, not float")
    return [Fraction(v) for v in values]


def part_times(work, instances=None, parts=1):
    """Hours one part spends at each stage."""
    work = _exact(*work)
    instances = [1] * len(work) if instances is None else list(instances)
    if len(instances) != len(work) or parts < 1 or any(m < 1 for m in instances):
        raise ValueError("one instance count >= 1 per stage, parts >= 1")
    return [w / (m * parts) for w, m in zip(work, instances)]


def makespan(work, instances=None, parts=1, wake=0, staggered=True):
    """Hours from the first part entering stage 1 to the last part leaving the last stage."""
    t = part_times(work, instances, parts)
    (wake,) = _exact(wake)
    waiting = 0 if staggered else wake * (len(t) - 1)
    return sum(t) + (parts - 1) * max(t) + waiting


def batch_interval(work, instances=None):
    """Steady state: hours between two finished full batches."""
    return max(part_times(work, instances, 1))


def bottleneck(work, instances=None):
    """Index of the stage that sets the pace."""
    t = part_times(work, instances, 1)
    return t.index(max(t))


def most_parts(stage_hours, wake):
    """Largest split k whose parts still last at least one wake interval."""
    stage_hours, wake = _exact(stage_hours, wake)
    if wake <= 0:
        raise ValueError("wake interval must be positive")
    return max(1, int(stage_hours // wake))


def seconds_per_item(hours, items):
    (hours,) = _exact(hours)
    return hours * 3600 / items
