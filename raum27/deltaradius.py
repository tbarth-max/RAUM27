"""The delta radius between the 6 and the 8 crossing points, and dX/dT.

The six axis directions and the eight corner directions cross a shell
around the centre at two different distances. Their difference is the
**delta radius** ΔR, the radial step between the 6-system and the
8-system. Taken over one period ``dT = 1/f`` of the frequency key it
gives the radial speed ``dX/dT = ΔR · f``.

Two readings are in use in this repository, and they give different
numbers, so both are named here and neither is preferred:

* **Cube reading** (``"wuerfel"``, as in `eckenruecklauf`): edge ``a``
  around the centre, the 6 points are the face centres at ``a/2``, the
  8 points the corners at ``a·sqrt 3/2``. The corner is further out:
  ``ΔR = (a/2)(sqrt 3 - 1)``, difference of the squared radii ``a²/2``,
  ratio ``r8/r6 = sqrt 3``.
* **Rhombus reading** (``"raute"``, as in `rautenraum`): the 6 points are
  the pyramid apexes at ``a``, the 8 points the cube corners at
  ``a·sqrt 3/2``. Here the apex is further out:
  ``ΔR = a(1 - sqrt 3/2)``, difference of the squares ``a²/4``, ratio
  ``r8/r6 = sqrt 3/2``.

Everything is exact. A radius difference is irrational, so it is kept
as ``p + q·sqrt 3`` with rational ``p`` and ``q`` (`Surd3`); its sign
and order are decided exactly by comparing squares, never by floats.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from raum27.eckenruecklauf import touching_radii_squared
from raum27.nennerordnung import Power
from raum27.zustandshologramm import period

READINGS = ("wuerfel", "raute")


def _rational(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError(f"{name} must be int or Fraction, got {type(value).__name__}")
    return Fraction(value)


@dataclass(frozen=True)
class Surd3:
    """The exact number p + q·sqrt 3."""

    p: Fraction
    q: Fraction

    def __post_init__(self):
        object.__setattr__(self, "p", _rational(self.p, "p"))
        object.__setattr__(self, "q", _rational(self.q, "q"))

    def __add__(self, other):
        return Surd3(self.p + other.p, self.q + other.q)

    def __sub__(self, other):
        return Surd3(self.p - other.p, self.q - other.q)

    def __mul__(self, other):
        if isinstance(other, Surd3):
            return Surd3(self.p * other.p + 3 * self.q * other.q, self.p * other.q + self.q * other.p)
        k = _rational(other, "factor")
        return Surd3(self.p * k, self.q * k)

    __rmul__ = __mul__

    def sign(self):
        """-1, 0 or +1, exactly: compare p² with 3q² when p and q disagree."""
        sp = (self.p > 0) - (self.p < 0)
        sq = (self.q > 0) - (self.q < 0)
        if sp == sq or sq == 0:
            return sp
        if sp == 0:
            return sq
        a, b = self.p * self.p, 3 * self.q * self.q
        return sp if a > b else (sq if b > a else 0)

    def __lt__(self, other):
        return (self - other).sign() < 0

    def __float__(self):
        return float(self.p) + float(self.q) * 3 ** 0.5


def _edge(edge):
    a = _rational(edge, "edge")
    if a <= 0:
        raise ValueError("edge must be positive")
    return a


def _reading(reading):
    if reading not in READINGS:
        raise ValueError(f"reading must be one of {READINGS}, got {reading!r}")
    return reading


def radii_squared(edge=9, reading="wuerfel"):
    """(r6², r8²): squared distances of the 6 and the 8 crossing points from the centre."""
    a, reading = _edge(edge), _reading(reading)
    faces, _, corners = touching_radii_squared(a)
    return (faces if reading == "wuerfel" else a * a), corners


def delta_radius(edge=9, reading="wuerfel"):
    """ΔR = |r8 - r6| as an exact Surd3 (always positive)."""
    a, reading = _edge(edge), _reading(reading)
    if reading == "wuerfel":
        return Surd3(-a / 2, a / 2)          # a·sqrt3/2 - a/2
    return Surd3(a, -a / 2)                  # a - a·sqrt3/2


def delta_radius_squared_difference(edge=9, reading="wuerfel"):
    """|r8² - r6²|, which stays rational: a²/2 (cube) or a²/4 (rhombus)."""
    r6, r8 = radii_squared(edge, reading)
    return abs(r8 - r6)


def corner_to_axis_ratio(reading="wuerfel"):
    """r8 / r6 as an exact power form: sqrt 3 (cube) or sqrt 3 / 2 (rhombus)."""
    root3 = Power.of(3).root(2)
    return root3 if _reading(reading) == "wuerfel" else root3 / Power.of(2)


def step_period(frequency):
    """dT: the period of one step under the frequency key, 1/f."""
    if isinstance(frequency, bool) or not isinstance(frequency, int) or frequency < 1:
        raise ValueError(f"frequency must be a positive integer, got {frequency!r}")
    return period(frequency)


def radial_speed(frequency, edge=9, reading="wuerfel"):
    """dX/dT = ΔR / dT = ΔR · f, exact."""
    return delta_radius(edge, reading) * (1 / step_period(frequency))
