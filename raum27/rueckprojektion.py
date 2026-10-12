"""Four circles, eight return vectors, and the negative inside radius 1.

The picture submitted, step by step, with what each step is exactly:

- **Two circles in the plane, one pushing out, one pressing in.** Outward
  is multiplication by ``1 + i``: a 45 degree turn and a radius times
  sqrt 2. Inward is division by ``1 + i``, i.e. multiplication by
  ``(1 - i) / 2``. Their product is exactly 1. Everything stays in
  Gaussian rationals, so no root is ever evaluated.
- **The eight directions 1..8.** Each outward step advances the direction
  by one; after eight steps it is back on 1 with the radius times 16,
  because ``(1 + i)**8 == 16``. That full turn is the carry "state 10".
  Turn count and direction together recover the circle number exactly
  (``circle_state`` / ``circle_number``): states are stored, not numbers.
- **Four delta vectors.** From an axis point the outward delta runs
  along an axis and the inward delta along a diagonal; from a diagonal
  point it is the other way round (``delta_out`` / ``delta_in``).
- **Three dimensions.** An exact integer rotation-with-scaling in 3D
  exists only when the scale factor itself is an integer: the
  determinant would otherwise be ``sqrt(m)**3``. So there is no 3D
  ``1 + i`` with factor sqrt 2 or sqrt 3, and the step from an axis to a
  cube corner is built as a *sum of unit deltas* instead, squared length
  1 -> 2 -> 3 (``corner_path``). Retracing the same deltas backwards
  returns to the centre exactly; the eight octant vectors do so together
  (``eight_round_trips``).
- **The hologram inside radius 1.** Back-projection through radius 1 is
  sphere inversion: direction kept, radius r -> 1/r. Circle 2 lands on
  1/2, circle 3 on 1/3, circle n on 1/n -- the whole body lands inside
  the unit sphere as its negative (``hologram``). Inverting again
  radiates it back out unchanged: the map is an involution.

Two limits that stay attached to the picture:

- The negative carries exactly the information of the body -- the map is
  a bijection, it neither adds nor loses anything.
- With equally spaced circles 1..N the negative crowds towards the
  centre: the innermost gap is ``1/(N-1) - 1/N`` (1/89700 for N = 300).
  Only a geometric ladder, such as the ``1 + i`` circles, maps onto
  itself under inversion (``ladder_is_self_inverse``) -- the same result
  as ``raum27.schalenleiter``.
"""

from fractions import Fraction
from itertools import product
from math import gcd, lcm

OUT = (Fraction(1), Fraction(1))
"""Outward step: multiply by 1 + i."""

IN = (Fraction(1, 2), Fraction(-1, 2))
"""Inward step: multiply by 1 / (1 + i) = (1 - i) / 2."""

PLANE_DIRECTIONS = ((1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1))
"""The eight plane directions, labelled 1..8 in this order (axis, diagonal, ...)."""

SEXTANTS = tuple(v for v in product((-1, 0, 1), repeat=3) if sum(map(abs, v)) == 1)
OCTANTS = tuple(product((-1, 1), repeat=3))


def _gauss(z):
    return (Fraction(z[0]), Fraction(z[1]))


def multiply(a, b):
    """Product of two Gaussian rationals given as (real, imaginary)."""
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def outward(z):
    """One step out: 45 degrees on, radius times sqrt 2."""
    return multiply(_gauss(z), OUT)


def inward(z):
    """One step in: 45 degrees back, radius times 1/sqrt 2."""
    return multiply(_gauss(z), IN)


def squared_length(v):
    """Squared length of a vector of any dimension, exact."""
    return sum(Fraction(x) ** 2 for x in v)


def delta_out(z):
    """Displacement of one outward step from ``z``."""
    moved = outward(z)
    return (moved[0] - z[0], moved[1] - z[1])


def delta_in(z):
    """Displacement of one inward step from ``z``."""
    moved = inward(z)
    return (moved[0] - z[0], moved[1] - z[1])


def direction_label(z):
    """Which of the eight plane directions ``z`` points along, as 1..8."""
    x, y = _gauss(z)
    if x == 0 and y == 0:
        raise ValueError("the centre has no direction")
    scale = max(abs(x), abs(y))
    unit = (x / scale, y / scale)
    if unit not in PLANE_DIRECTIONS:
        raise ValueError(f"{z} is not on one of the eight directions")
    return PLANE_DIRECTIONS.index(unit) + 1


def circle_point(k):
    """The point on circle ``k`` reached from (1, 0) by k outward steps."""
    z = (Fraction(1), Fraction(0))
    for _ in range(k):
        z = outward(z)
    return z


def circle_state(k):
    """Circle number as a stored state: (full turns, direction 1..8)."""
    if k < 0:
        raise ValueError("circle numbers start at 0")
    return k // 8, k % 8 + 1


def circle_number(turns, direction):
    """Inverse of ``circle_state``."""
    if not 1 <= direction <= 8 or turns < 0:
        raise ValueError(f"no state ({turns}, {direction})")
    return 8 * turns + direction - 1


def corner_path(octant):
    """Axis -> edge -> corner as unit deltas; squared lengths 1, 2, 3."""
    if octant not in OCTANTS:
        raise ValueError(f"{octant} is not an octant")
    points = [(0, 0, 0)]
    for axis in range(3):
        step = [0, 0, 0]
        step[axis] = octant[axis]
        points.append(tuple(p + s for p, s in zip(points[-1], step)))
    return points


def retrace(path):
    """The same path walked back to its start."""
    return list(reversed(path))


def eight_round_trips():
    """All eight octant vectors out and back; returns the summed displacement."""
    total = [0, 0, 0]
    for octant in OCTANTS:
        out = corner_path(octant)
        back = retrace(out)
        if back[-1] != out[0]:  # pragma: no cover - retrace ends where it began
            raise AssertionError("round trip did not close")
        for axis in range(3):
            total[axis] += back[-1][axis] - out[0][axis]
    return tuple(total)


def integer_similarity_3d_possible(m):
    """Can an integer 3x3 matrix satisfy M M^T = m I with m > 0?

    Necessary: det(M)**2 = m**3, so m must be a perfect square. This
    function checks it by exhaustive search over rows of squared length m.
    """
    rows = [r for r in product(range(-m, m + 1), repeat=3) if sum(x * x for x in r) == m]
    for a in rows:
        for b in rows:
            if sum(x * y for x, y in zip(a, b)):
                continue
            for c in rows:
                if not sum(x * y for x, y in zip(a, c)) and not sum(x * y for x, y in zip(b, c)):
                    return True
    return False


def hologram(body):
    """Back-projection through radius 1: each (radius, direction) -> (1/radius, direction)."""
    return {(1 / Fraction(radius), direction) for radius, direction in body}


def negative(body, radii, directions):
    """The photographic negative: every lit point dark, every dark point lit."""
    return {(Fraction(r), d) for r in radii for d in directions} - {
        (Fraction(r), d) for r, d in body
    }


def point_reflection(body):
    """Each direction replaced by its opposite."""
    return {(radius, tuple(-x for x in direction)) for radius, direction in body}


def inner_gap(n):
    """Gap between the two innermost negative circles for circles 1..n."""
    return Fraction(1, n - 1) - Fraction(1, n)


def ladder_is_self_inverse(radii):
    """Does r -> 1/r map this set of radii onto itself?"""
    radii = {Fraction(r) for r in radii}
    return {1 / r for r in radii} == radii


def wavelength(frequency):
    """With the speed normalised to 1: wavelength = 1 / frequency."""
    return Fraction(1, frequency)


def surface_meeting(f, g):
    """Circle on which two frequencies meet on the surface: lcm(f, g)."""
    return lcm(f, g)


def connection_repeat(f, g):
    """Common repeat of the two wavelengths: 1 / gcd(f, g)."""
    return Fraction(1, gcd(f, g))
