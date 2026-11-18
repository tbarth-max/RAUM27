"""Reliability of a chain of N modules run "greedily" (continue until
the first failure). Standard reliability engineering -- series-system
reliability, where the whole chain succeeds only if every link does --
applied here because chaining unreliable pipeline stages, and whether a
hand-off mechanism is a structural necessity or a nice-to-have, came up
directly tonight.

chain_success_probability is the exact rule (product of independent
probabilities). simulate_greedy_chain is the empirical check: draw a
fresh random per-module success rate each trial, run until first
failure, and report both the fraction of trials that complete every
module and the average chain length before failure. At 10 modules with
per-module rates drawn uniformly from [0.70, 0.95]: about 15% of trials
complete all 10 (E[rate]=0.825, and 0.825**10 ~ 14.6%), and the average
chain length before failure is about 4 of 10 -- confirming a hand-off
mechanism ("the next module picks up from wherever the last one left
off") is a structural necessity for a chain this unreliable, not an
afterthought.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Sequence

import numpy as np


def chain_success_probability(individual_probabilities: Sequence) -> Fraction:
    """Exact probability that every module in the chain succeeds, given
    independent per-module success probabilities: the product rule for
    independent events, P(all succeed) = product(P(module_i succeeds))."""
    result = Fraction(1)
    for p in individual_probabilities:
        result *= Fraction(p)
    return result


def simulate_greedy_chain(
    rng: np.random.Generator,
    n_modules: int,
    low: float,
    high: float,
    trials: int,
) -> tuple[float, float]:
    """Monte Carlo: for each trial, draw a fresh per-module success rate
    uniformly from [low, high], then run the chain module by module,
    stopping at the first failure. Returns (fraction of trials that
    completed all n_modules, average chain length before failure)."""
    complete = 0
    lengths = []
    for _ in range(trials):
        rates = rng.uniform(low, high, n_modules)
        length = 0
        for p in rates:
            if rng.random() < p:
                length += 1
            else:
                break
        lengths.append(length)
        if length == n_modules:
            complete += 1
    return complete / trials, float(np.mean(lengths))
