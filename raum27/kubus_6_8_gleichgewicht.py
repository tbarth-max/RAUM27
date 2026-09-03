"""RAUM27 6/8-Gleichgewicht: where does 6^X = 8^(10-X)?

6 (cube faces) and 8 (cube corners) sit as the bases of two competing
exponentials over a fixed budget of 10. f(X) = 6^X - 8^(10-X) has
derivative f'(X) = ln(6)*6^X + ln(8)*8^(10-X) -- a sum of two strictly
positive terms for every real X, so f is strictly increasing everywhere.
That means there is EXACTLY ONE crossing point over all real numbers,
not merely "a root exists in some interval someone happened to check."
is_strictly_increasing_on_sample below checks this numerically; the
derivative argument above is why it must hold, not just an empirical
observation.

Solved by bisection (standard library only, no external solver
dependency) -- valid specifically because of the monotonicity guarantee
above, which is what makes bisection converge to the one true root
rather than an arbitrary one.

NEGATIVE FINDING, documented rather than dropped: naively "raising the
exponents themselves" -- comparing 6**(X**N) against 8**(N**X) -- is not
a generalization of this equilibrium to a family of them. Both sides
explode super-exponentially and diverge from each other rather than
staying in balance: already at X=N=2 they differ by more than 3x (1296
vs 4096), and the gap only widens from there. exploding_exponent_mismatch
exists to keep this checkable, not to be built on.
"""

from __future__ import annotations

import math


def _f(x: float) -> float:
    return 6.0**x - 8.0 ** (10 - x)


def find_equilibrium(lo: float = -50.0, hi: float = 50.0, tol: float = 1e-12) -> float:
    """Bisection root of 6^X = 8^(10-X), valid because _f is strictly
    increasing everywhere (see module docstring)."""
    f_lo, f_hi = _f(lo), _f(hi)
    if f_lo > 0 or f_hi < 0:
        raise ValueError("bracket does not contain the root; widen lo/hi")
    while hi - lo > tol:
        mid = (lo + hi) / 2
        if _f(mid) < 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def is_strictly_increasing_on_sample(lo: float = -20.0, hi: float = 30.0, n: int = 2000) -> bool:
    """Numerically checks the monotonicity the uniqueness argument relies
    on, by dense sampling -- not a proof by itself, but a check that
    nothing in the implementation contradicts the derivative argument
    above."""
    step = (hi - lo) / n
    values = [_f(lo + i * step) for i in range(n + 1)]
    return all(values[i] < values[i + 1] for i in range(len(values) - 1))


def exploding_exponent_mismatch(x: int, n: int) -> tuple[int, int]:
    """The rejected generalization: 6**(x**n) vs 8**(n**x). Returns both
    sides for small x, n -- they diverge immediately, not just
    eventually. Not a source of equilibria; see module docstring."""
    return 6 ** (x**n), 8 ** (n**x)
