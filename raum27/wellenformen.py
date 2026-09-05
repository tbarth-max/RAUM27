"""Fourier partial-sum synthesis of a square wave and a triangle wave,
and a correction: adding more sine layers to approximate either shape
INCREASES the partial sum's total energy monotonically toward the true
signal's energy -- it does not hold at some constant "equilibrium"
value. That's Parseval's theorem / Bessel's inequality, applied here
because an earlier version of this idea described the growth as a fixed
"Energiegleichgewicht" (energy equilibrium), which is the wrong word for
something that keeps increasing.

square_wave_partial and triangle_wave_partial are genuinely different
target shapes, not the same curve at different levels of refinement:
- Square wave: sum of sin(n*x)/n over odd n. Has the Gibbs phenomenon
  (partial sums overshoot the jump by about 9%, verified below) and
  stays near +-1 (a plateau) for most of the period.
- Triangle wave: sum of (-1)^k * sin(n*x)/n^2 over odd n, alternating
  sign, 1/n^2 decay instead of 1/n. No overshoot (it's continuous, no
  jump discontinuity for Gibbs to act on) and spends most of the period
  away from +-1 (no plateau, a smooth ramp instead).
"""

from __future__ import annotations

import numpy as np


def square_wave_partial(x: np.ndarray, n_terms: int) -> np.ndarray:
    """Partial Fourier sum of a +-1 square wave, using the first n_terms
    odd harmonics: (4/pi) * sum_{k=0}^{n_terms-1} sin((2k+1)x)/(2k+1)."""
    total = np.zeros_like(x, dtype=float)
    for k in range(n_terms):
        n = 2 * k + 1
        total += np.sin(n * x) / n
    return (4 / np.pi) * total


def triangle_wave_partial(x: np.ndarray, n_terms: int) -> np.ndarray:
    """Partial Fourier sum of a +-1 triangle wave, using the first
    n_terms odd harmonics with alternating sign and 1/n^2 decay:
    (8/pi^2) * sum_{k=0}^{n_terms-1} (-1)^k * sin((2k+1)x)/(2k+1)^2."""
    total = np.zeros_like(x, dtype=float)
    for k in range(n_terms):
        n = 2 * k + 1
        total += ((-1) ** k) * np.sin(n * x) / n**2
    return (8 / np.pi**2) * total


def mean_square_energy(signal: np.ndarray) -> float:
    """Mean of signal**2 -- the discrete stand-in for a periodic signal's
    average power over one period."""
    return float(np.mean(signal**2))
