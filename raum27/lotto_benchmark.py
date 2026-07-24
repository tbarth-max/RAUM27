"""Null-hypothesis benchmark: does a forecasting algorithm beat chance on
a known-random process?

The methodological idea behind this module is legitimate and worth
stating precisely, because it is easy to misuse: verifying a forecasting
method against a slow, causally-connected system (e.g. a climate model)
can take decades before ground truth is known. A certified lottery draw
is the opposite kind of test case -- it is fast-feedback and, by
construction, an i.i.d. uniform random process with zero mutual
information between successive draws. That makes it a useful *null
test*: a method that fabricates false-positive "signal" out of pure noise
(the standard failure mode of an overfit forecasting pipeline) should
reveal that failure mode here, fast, instead of only surfacing it decades
into a real forecast.

What this benchmark can prove: whether a specific algorithm shows a
statistically significant edge over the exact combinatorial (hypergeometric)
baseline, on i.i.d. random draws.

What it cannot prove, and does not claim: that failing here implies a
method is bad at forecasting *causally connected* systems like climate,
or that passing here would imply anything about those systems either.
Climate has real physical autocorrelation a certified lottery deliberately
has none of; a result on one says nothing about the other. This module
also is not, and must not be used as, a gambling tool: an apparent "edge"
found on a finite historical sample is expected sampling noise unless it
survives the permutation test below with a low p-value AND replicates on
held-out data collected after the method was fixed.
"""

from __future__ import annotations

import random
from fractions import Fraction
from math import comb
from typing import Callable, Sequence

from raum27.taylor import sin_taylor

Draw = Sequence[int]


def match_probability(m: int, pool: int = 49, picks: int = 6, winning: int = 6) -> Fraction:
    """Exact hypergeometric probability of matching exactly m numbers
    when picking `picks` numbers out of `pool`, given `winning` numbers
    are drawn. E.g. match_probability(3) is the real probability of
    "3 richtige" in German 6-aus-49 -- about 1.76%, not 5%.
    """
    if m < 0 or m > min(picks, winning) or (picks - m) > (pool - winning):
        return Fraction(0)
    numerator = comb(winning, m) * comb(pool - winning, picks - m)
    denominator = comb(pool, picks)
    return Fraction(numerator, denominator)


def expected_matches(pool: int = 49, picks: int = 6, winning: int = 6) -> Fraction:
    """E[number of matches] for a uniformly random pick = picks*winning/pool."""
    return Fraction(picks * winning, pool)


class RandomPredictor:
    """The baseline: a uniformly random pick, independent of history."""

    def __init__(self, pool: int = 49, picks: int = 6, seed: int | None = None):
        self.pool = pool
        self.picks = picks
        self.rng = random.Random(seed)

    def predict(self, history: Sequence[Draw]) -> tuple[int, ...]:
        return tuple(sorted(self.rng.sample(range(1, self.pool + 1), self.picks)))


class FingerprintKNNPredictor:
    """The fingerprint + k-nearest-neighbours forecaster described in the
    source notes: normalize a draw by its first number, run each
    resulting ratio through a rational Taylor-sine approximation at 4
    phases, compare draws by L1 distance in that 24-dimensional space,
    and vote on the next draw using the k nearest historical neighbours'
    actual successors, inverse-distance weighted.
    """

    def __init__(self, k: int = 5, pool: int = 49, picks: int = 6, seed: int = 0):
        self.k = k
        self.pool = pool
        self.picks = picks
        self._rng = random.Random(seed)
        self._fingerprint_cache: dict[Draw, list[Fraction]] = {}

    def _fingerprint(self, draw: Draw) -> list[Fraction]:
        cached = self._fingerprint_cache.get(draw)
        if cached is not None:
            return cached
        z1 = draw[0]
        y = [Fraction(z, z1) for z in draw]
        vec = []
        for t in range(4):
            phase = Fraction(t, 1) * Fraction(4, 9)
            for yi in y:
                x = Fraction(16, 9) * yi + phase
                vec.append(sin_taylor(x, terms=5))
        self._fingerprint_cache[draw] = vec
        return vec

    @staticmethod
    def _l1(a: list[Fraction], b: list[Fraction]) -> Fraction:
        return sum(abs(x - y) for x, y in zip(a, b))

    def predict(self, history: Sequence[Draw]) -> tuple[int, ...]:
        if len(history) < 2:
            return tuple(sorted(self._rng.sample(range(1, self.pool + 1), self.picks)))

        current_fp = self._fingerprint(history[-1])
        distances = [(idx, self._l1(current_fp, self._fingerprint(history[idx]))) for idx in range(len(history) - 1)]
        distances.sort(key=lambda pair: pair[1])
        nearest = distances[: self.k]

        votes: dict[int, Fraction] = {}
        for idx, d in nearest:
            weight = Fraction(10**6) if d == 0 else Fraction(1) / d
            for number in history[idx + 1]:
                votes[number] = votes.get(number, Fraction(0)) + weight

        ranked = sorted(votes, key=lambda n: votes[n], reverse=True)
        picks = ranked[: self.picks]
        if len(picks) < self.picks:
            remaining = [n for n in range(1, self.pool + 1) if n not in picks]
            self._rng.shuffle(remaining)
            picks = picks + remaining[: self.picks - len(picks)]
        return tuple(sorted(picks))


def match_count(draw: Draw, prediction: Draw) -> int:
    return len(set(draw) & set(prediction))


def backtest(history: Sequence[Draw], predictor, min_history: int = 2) -> list[int]:
    """Walk-forward backtest: predict draw[t] using only draws[:t] (no
    lookahead), for every t from `min_history` to len(history) - 1.
    Returns the list of match counts."""
    matches = []
    for t in range(min_history, len(history)):
        prediction = predictor.predict(history[:t])
        matches.append(match_count(history[t], prediction))
    return matches


def permutation_test(
    history: Sequence[Draw],
    predictor_factory: Callable[[], object],
    stat_fn: Callable[[list[int]], float] = lambda matches: sum(matches) / len(matches),
    n_permutations: int = 100,
    seed: int | None = None,
) -> tuple[float, float, list[float]]:
    """Null-hypothesis significance test for "does this predictor exploit
    real structure in the draw order". Shuffling the draw order destroys
    any temporal structure a predictor could legitimately exploit while
    preserving the exact set of draws, so if the predictor's statistic on
    the real order is not extreme relative to the shuffled-order null
    distribution, there is no evidence of real predictive skill.

    Returns (observed_statistic, p_value, null_distribution).
    """
    observed = stat_fn(backtest(history, predictor_factory()))
    rng = random.Random(seed)
    null_stats = []
    for _ in range(n_permutations):
        shuffled = list(history)
        rng.shuffle(shuffled)
        null_stats.append(stat_fn(backtest(shuffled, predictor_factory())))
    p_value = (sum(1 for s in null_stats if s >= observed) + 1) / (n_permutations + 1)
    return observed, p_value, null_stats
