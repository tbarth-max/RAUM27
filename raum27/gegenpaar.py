"""Keep only what stands opposite: the 180° pair filter and the 90° classes between two of them.

A signal is sampled at M equally spaced points of a circle. Each sample
is a pair (I, Q): the left-right channel and the up-down channel, written
as one exact Gaussian rational I + iQ (`Gauss`). Turning the circle by a
quarter moves every sample M/4 places on.

**The 180° filter.** Keep only what has an exact counterpart a half turn
away with the opposite sign:

    P f[j] = (f[j] - f[j + M/2]) / 2

Everything that comes back unchanged after half a turn -- the constant
ground level (a bias voltage on which the information is modulated) and
every even harmonic -- is removed. ``P`` is a projection: applying it
twice changes nothing, and ``f = P f + (1 - P) f`` without remainder.

**The limit of 180°.** A disturbance that is itself a perfect opposite
pair passes the 180° filter unchanged, just like the signal.

**The 90° classes.** Between the two 180° systems lies the quarter turn.
Splitting by how a pattern answers a quarter turn (factor 1, i, -1 or -i)
gives four exact classes

    P_r f[j] = (1/4) Σ_{m=0..3} i^(-r·m) f[j + m·M/4],   r = 0, 1, 2, 3

with P_1 + P_3 = P (the 180° pairs) and P_0 + P_2 = 1 - P. A signal turning
one way (r = 1) and a disturbance turning the other way (r = 3) are both
perfect opposite pairs, yet the quarter classes separate them exactly.

**What stays inseparable.** A disturbance in the *same* quarter class as
the signal -- same turning sense, same response to every quarter turn --
cannot be removed by any of these projections; only a further channel
(another axis, another frequency) can tell them apart. That is a limit of
the method, stated rather than hidden.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


def _rational(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError(f"{name} must be int or Fraction, got {type(value).__name__}")
    return Fraction(value)


@dataclass(frozen=True)
class Gauss:
    """The exact number I + iQ."""

    re: Fraction
    im: Fraction = Fraction(0)

    def __post_init__(self):
        object.__setattr__(self, "re", _rational(self.re, "re"))
        object.__setattr__(self, "im", _rational(self.im, "im"))

    def __add__(self, other):
        return Gauss(self.re + other.re, self.im + other.im)

    def __sub__(self, other):
        return Gauss(self.re - other.re, self.im - other.im)

    def __mul__(self, other):
        if isinstance(other, Gauss):
            return Gauss(self.re * other.re - self.im * other.im, self.re * other.im + self.im * other.re)
        k = _rational(other, "factor")
        return Gauss(self.re * k, self.im * k)

    __rmul__ = __mul__

    def norm(self):
        """|z|² = I² + Q², exact."""
        return self.re * self.re + self.im * self.im


I_POWERS = (Gauss(1), Gauss(0, 1), Gauss(-1), Gauss(0, -1))   # i^0 .. i^3


def _signal(samples, quarters=False):
    f = [s if isinstance(s, Gauss) else Gauss(_rational(s, "sample")) for s in samples]
    step = 4 if quarters else 2
    if not f or len(f) % step:
        raise ValueError(f"need a non-empty number of samples divisible by {step}")
    return f


def opposite_pairs(samples):
    """The 180° filter P: keep only what reverses sign half a turn away."""
    f = _signal(samples)
    h = len(f) // 2
    return [(f[j] - f[(j + h) % len(f)]) * Fraction(1, 2) for j in range(len(f))]


def returning_part(samples):
    """1 - P: what comes back unchanged after half a turn (ground level, even harmonics)."""
    f = _signal(samples)
    h = len(f) // 2
    return [(f[j] + f[(j + h) % len(f)]) * Fraction(1, 2) for j in range(len(f))]


def quarter_class(samples, r):
    """P_r: the part that answers a quarter turn with the factor i^r."""
    if r not in (0, 1, 2, 3):
        raise ValueError("r must be 0, 1, 2 or 3")
    f = _signal(samples, quarters=True)
    q = len(f) // 4
    out = []
    for j in range(len(f)):
        total = Gauss(0)
        for m in range(4):
            total = total + I_POWERS[(-r * m) % 4] * f[(j + m * q) % len(f)]
        out.append(total * Fraction(1, 4))
    return out


def energy(samples):
    """Σ |f[j]|², exact."""
    return sum((s if isinstance(s, Gauss) else Gauss(_rational(s, "sample"))).norm() for s in samples)


def occupied_classes(samples):
    """The quarter classes a signal has energy in."""
    return {r for r in range(4) if energy(quarter_class(samples, r)) != 0}


def separable(signal, disturbance):
    """Can the quarter classes split signal from disturbance? Only if they share no class."""
    return not (occupied_classes(signal) & occupied_classes(disturbance))
