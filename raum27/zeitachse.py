"""Time as a path: the T axis in the cube, what it adds, and what it does not.

Checked against the idea "X = Y^2 = Z^3 = T^4 in the cube, the sphere
expanding from the centre, time read off the four space diagonals, six
diagrams XY XZ YZ XT YT ZT":

* Four axes x, y, z, t have C(4,2) = **6** coordinate planes -- the six
  diagrams. The list XY, XZ, XT, XT, YT, ZT has XT twice and lacks YZ.
* An expanding sphere cuts all four space diagonals at the same distance:
  the four readings are one number. The diagonals do not give four time
  axes, they give one scale parameter, read eight times (one per corner).
  That is the existing rule: time is the index of the shells, not a
  direction inside a shell (``kugelkoordinaten``, ``viertakt``).
* Stages a, a^2, a^3, a^4 all come back to a by the 1st..4th root -- but
  as a fraction only when the value is a perfect power. W^(1/4) of 2 is
  not rational; nothing is gained by the 4th power that the square does
  not already give: (sqrt 2)^2 = 2 and (sqrt 3)^2 = 3 are exact, so d^2
  removes the roots one step earlier than d^4.
* What a real 4th axis does add, exactly: the unit 4-cube has diagonal
  sqrt 4 = **2**, rational, and every natural number is a sum of four
  squares (Lagrange) -- the 3D gaps 4^a (8b + 7) close. Its faces are
  16 corners, 32 edges, 24 squares and 8 cubes.
* Physics adds time with the opposite sign: s^2 = x^2 + y^2 + z^2 - (c t)^2.
  The Euclidean t axis is a modelling choice, not the spacetime metric.

And the direct line: a message through n relays arrives unchanged with
probability (1 - p)^n even if every relay checks its own hand-over.
Only a check between the two ends covers the whole way.
"""

from fractions import Fraction
from itertools import combinations
from math import comb, isqrt

AXES = ("x", "y", "z", "t")
SPACE_DIAGONALS = ((1, 1, 1), (1, 1, -1), (1, -1, 1), (-1, 1, 1))


def _exact(*values):
    for v in values:
        if isinstance(v, float):
            raise TypeError("exact module: use int or Fraction, not float")
    return [Fraction(v) for v in values]


def diagrams(axes=AXES):
    """All coordinate planes: one diagram per pair of axes."""
    return ["".join(pair).upper() for pair in combinations(axes, 2)]


def diagonal_readings(radius_squared):
    """Where a sphere of radius^2 R cuts the four space diagonals: R for each, coordinate^2 = R/3."""
    (r2,) = _exact(radius_squared)
    return [(d, r2 / 3) for d in SPACE_DIAGONALS]


def independent_readings(radius_squared):
    """How many different numbers the four diagonal readings carry."""
    return len({c2 for _, c2 in diagonal_readings(radius_squared)})


def _integer_root(n, k):
    """Exact integer k-th root of n >= 0 by bisection, or None."""
    lo, hi = 0, 1
    while hi ** k <= n:
        hi *= 2
    while lo < hi - 1:
        mid = (lo + hi) // 2
        if mid ** k <= n:
            lo = mid
        else:
            hi = mid
    return lo if lo ** k == n else None


def exact_root(value, k):
    """The rational k-th root of a non-negative fraction, or None if there is none."""
    (value,) = _exact(value)
    if k < 1 or value < 0:
        raise ValueError("k >= 1 and a non-negative value")
    num, den = _integer_root(value.numerator, k), _integer_root(value.denominator, k)
    return None if num is None or den is None else Fraction(num, den)


def stages(a):
    """X = a, Y^2 = a^2, Z^3 = a^3, T^4 = a^4 -- and each one back to a."""
    (a,) = _exact(a)
    forward = [a ** k for k in (1, 2, 3, 4)]
    back = [exact_root(w, k) for k, w in zip((1, 2, 3, 4), forward)]
    return forward, back


def diagonal_squared(dimension):
    """Squared main diagonal of the unit cube in n dimensions: n."""
    return dimension


def rational_diagonals(up_to):
    """Dimensions whose unit-cube diagonal is rational: the perfect squares."""
    return [n for n in range(1, up_to + 1) if isqrt(n) ** 2 == n]


def hypercube_faces(dimension=4):
    """k-dimensional faces of the n-cube: C(n, k) * 2^(n-k)."""
    return {k: comb(dimension, k) * 2 ** (dimension - k) for k in range(dimension + 1)}


def square_sums(count, limit):
    """Which n <= limit are a sum of ``count`` integer squares."""
    squares = [i * i for i in range(isqrt(limit) + 1)]
    reach = {0}
    for _ in range(count):
        reach = {r + s for r in reach for s in squares if r + s <= limit}
    return reach


def helix_length_squared(base_squared, height):
    """One unrolled turn: path^2 = base^2 + height^2 (exact when base^2 is)."""
    b2, h = _exact(base_squared, height)
    return b2 + h * h


def interval_squared(x, y, z, t, c=1):
    """Spacetime interval s^2 = x^2 + y^2 + z^2 - (c t)^2; 0 on a light ray."""
    x, y, z, t, c = _exact(x, y, z, t, c)
    return x * x + y * y + z * z - (c * t) ** 2


def intact_probability(error_per_hop, hops):
    """Chance that a message passes ``hops`` relays unchanged: (1 - p)^n."""
    (p,) = _exact(error_per_hop)
    if not 0 <= p <= 1 or hops < 0:
        raise ValueError("0 <= p <= 1 and hops >= 0")
    return (1 - p) ** hops
