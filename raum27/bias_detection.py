"""Detecting a constant distributional bias, as distinct from predicting
individual future draws.

`lotto_benchmark` asks: does knowing past draws help predict the *next*
draw? For a certified, fair lottery the answer is no by construction
(each draw is independent and uniform), and that module confirms it
empirically.

This module asks a different question: if the draw mechanism itself has
a persistent, non-uniform bias (e.g. a defective ball, an unbalanced
mechanism -- exactly what lottery regulators audit for), can that bias
be detected from enough historical draws? Yes, straightforwardly: sum up
how often each number appears across many draws and compare to the
uniform expectation. This is ordinary frequency analysis (the same idea
behind a chi-squared goodness-of-fit test), not a new technique.

What this can detect: a bias that is constant across the whole history
(the same numbers over- or under-represented in every draw).

What this cannot detect (see `lotto_benchmark`/`autocorrelation_control`
instead): cyclic or time-varying patterns, or any structure that would
let you predict which specific future draw comes next. A biased-but-fair
lottery (same wrong distribution every time) is a different failure mode
than the RAUM27 notes' claim, and this module does not blur the two:
finding a bias here says nothing about whether history predicts the next
draw, and vice versa.
"""

from __future__ import annotations

from typing import Sequence


class ConstantBiasDetector:
    """Aggregates events into total counts per value and flags the
    values whose count deviates most from the uniform expectation."""

    def __init__(self, value_range: int):
        if value_range < 1:
            raise ValueError(f"value_range must be >= 1, got {value_range}")
        self.value_range = value_range

    def total_counts(self, events: Sequence[Sequence[int]]) -> list[int]:
        """Index i holds the count of value i+1 across all events (1-indexed
        values, 0-indexed list)."""
        counts = [0] * self.value_range
        for event in events:
            for value in event:
                if not 1 <= value <= self.value_range:
                    raise ValueError(f"value {value} outside [1, {self.value_range}]")
                counts[value - 1] += 1
        return counts

    def deviation_from_uniform(
        self, counts: Sequence[int], n_events: int, values_per_event: int
    ) -> list[float]:
        """counts[i] minus the count expected under a uniform distribution."""
        expected = n_events * values_per_event / self.value_range
        return [c - expected for c in counts]

    def top_candidates(
        self,
        events: Sequence[Sequence[int]],
        values_per_event: int,
        n_candidates: int = 5,
    ) -> list[int]:
        """The `n_candidates` values (1-indexed) with the highest positive
        deviation from the uniform expectation -- the strongest candidates
        for a persistent, over-represented bias."""
        counts = self.total_counts(events)
        deviation = self.deviation_from_uniform(counts, len(events), values_per_event)
        ranked = sorted(range(1, self.value_range + 1), key=lambda v: -deviation[v - 1])
        return ranked[:n_candidates]
