"""Positive control for the permutation-test methodology used in
`lotto_benchmark`: does the same shuffle-based significance test actually
detect real temporal structure when structure is genuinely present?

`lotto_benchmark` found no significant edge for the fingerprint/k-NN
forecaster on i.i.d. random draws. That null result is only meaningful if
the test is capable of detecting real structure when it exists --
otherwise a null result could just mean the test has no power, not that
there is nothing to find.

This module supplies that positive control with the textbook case of a
system that has genuine short-range memory: an AR(1) process, the
standard toy model for autocorrelated series such as daily temperature
anomalies. Today's weather really is informative about tomorrow's -- that
short-range physical persistence is exactly what a certified lottery drum
is engineered to destroy within seconds of the previous draw. Running the
identical shuffle-based test on both cases makes the distinction between
them a demonstrated result, not an assertion: the same statistical
machinery reports "yes, structure" on the AR(1) series and "no
structure" on i.i.d. draws.
"""

from __future__ import annotations

import random
from typing import Callable, Sequence


def simulate_ar1(n: int, phi: float, sigma: float = 1.0, seed: int | None = None) -> list[float]:
    """Generate an AR(1) series: x_t = phi * x_(t-1) + noise.

    phi in (-1, 1) controls the strength of real serial correlation
    ("memory"). phi = 0 reduces to i.i.d. noise (like a lottery draw);
    phi close to 1 is strongly persistent (like short-range weather
    persistence, where today is a good predictor of tomorrow).
    """
    if not -1 < phi < 1:
        raise ValueError("phi must be in (-1, 1) for a stationary process")
    rng = random.Random(seed)
    series = [rng.gauss(0, sigma)]
    for _ in range(n - 1):
        series.append(phi * series[-1] + rng.gauss(0, sigma))
    return series


class PersistencePredictor:
    """The standard short-range weather-forecasting baseline: predict
    tomorrow = today. Only has skill if the series actually has serial
    correlation for the predictor to exploit."""

    def predict(self, history: Sequence[float]) -> float:
        return history[-1]


def backtest_continuous(series: Sequence[float], predictor, min_history: int = 2) -> list[float]:
    """Walk-forward absolute-error backtest, mirroring lotto_benchmark.backtest."""
    errors = []
    for t in range(min_history, len(series)):
        prediction = predictor.predict(series[:t])
        errors.append(abs(series[t] - prediction))
    return errors


def permutation_test_continuous(
    series: Sequence[float],
    predictor_factory: Callable[[], object],
    n_permutations: int = 100,
    seed: int | None = None,
) -> tuple[float, float, list[float]]:
    """Mirrors lotto_benchmark.permutation_test for continuous series
    scored by mean absolute error (lower is better). Shuffling the series
    destroys any real temporal structure while preserving its values, so
    the p-value answers: "how often does destroying the order still do at
    least as well as the observed order?" A small p-value means the order
    itself carries real, exploitable information.
    """

    def mean_error(errors: list[float]) -> float:
        return sum(errors) / len(errors)

    observed = mean_error(backtest_continuous(series, predictor_factory()))
    rng = random.Random(seed)
    null_stats = []
    for _ in range(n_permutations):
        shuffled = list(series)
        rng.shuffle(shuffled)
        null_stats.append(mean_error(backtest_continuous(shuffled, predictor_factory())))
    # Lower error is better here, so real structure shows up as the
    # observed error being significantly LOWER than the shuffled null.
    p_value = (sum(1 for s in null_stats if s <= observed) + 1) / (n_permutations + 1)
    return observed, p_value, null_stats
