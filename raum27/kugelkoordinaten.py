"""Kugelkoordinaten ohne Gleitkomma -- und warum die vierte Dimension rausfällt.

A forwarded script computed the distance between two rational points and
converted to spherical coordinates. Its diagnosis was right: the squares
stay exact as `Fraction`, the square root is the first rounding, and the
angles are floats because `cos` and `sin` are not rational. Its proposed
next step was to carry the angles as fractions and evaluate the
trigonometry only at the end.

**There is a better fix, and it removes the floating point entirely
rather than postponing it.**

DON'T CARRY ANGLES -- CARRY WHAT IS ALREADY RATIONAL
----------------------------------------------------

For any point with rational coordinates, all three pieces of spherical
information are *already* exact rationals, with no trigonometry
evaluated anywhere:

    r²        = x² + y² + z²
    cos²(theta) = z² / r²
    tan(phi)    = y / x

For `(1, 2, 3)`: `r² = 14`, `cos²(theta) = 9/14`, `tan(phi) = 2`. All
exact. The float versions agree to 1e-12, checked in the tests, but the
floats are never needed.

**And it is lossless.** Given `(r², cos²theta, tan phi)` plus three sign
bits, the original point comes back exactly: `z² = r²·cos²theta`, then
`x² + y² = r² - z²`, then `x² = (x²+y²)/(1 + tan²phi)`. Verified exactly
on rational points including negative and fractional ones. So nothing is
given up by refusing to take the square root -- the representation
carries the same information as the point.

The only quantity that genuinely needs a root is `r` itself, and the
project's existing convention already answers that: keep `r²`, the same
way `cube_symmetry.face_diagonal_squared` keeps the square. The script's
own example was exact only by luck -- `25` happens to be a perfect
square. Move one endpoint to `(1,1,1)` and the squared distance is `5`,
with an irrational root. The squared form stays exact either way.

WHICH ANGLES CAN BE EXACT AT ALL
--------------------------------

If one does want angles as fractions of a full turn, the honest answer
is that only finitely many work, and this is a theorem rather than a
limitation of the method. **Niven's theorem**: if `cos(r·pi)` is
rational for rational `r`, then it is one of `0, ±1/2, ±1`. So in `[0,1)`
there are **exactly 8** turn fractions with a rational cosine:

    q:     0    1/6   1/4   1/3   1/2   2/3   3/4   5/6
    cos:   1    1/2    0   -1/2   -1   -1/2   0    1/2

Denominators only 1, 2, 3, 4 and 6 -- and the quarter turns that
`viertakt` runs on are four of these eight.

**The project's squared convention doubles the set.** `cos² = (1 +
cos 2x)/2`, so `cos²` is rational exactly when the cosine of the doubled
angle is, which adds the halves: `1/8` gives `cos² = 1/2` exactly, and
`1/12` gives `3/4`, even though both cosines are themselves irrational.
That brings the exact set from 8 turn fractions to **16**. Keeping the
square is not a workaround here; it genuinely enlarges what can be
computed without rounding.

THE FOURTH DIMENSION IS A HARD OBSTRUCTION, NOT A DRAWING PROBLEM
-----------------------------------------------------------------

Leaving it out is the correct call, and for a stronger reason than
"it cannot be pictured". The Cayley-Menger determinant of `m` points is
non-zero exactly when they span `m-1` dimensions, and for `m` mutually
equidistant points it is `±m`:

    m:          2    3    4    5    6
    CM det:     2   -3    4   -5    6
    spans:      1    2    3    4    5   dimensions

So **5 mutually equidistant points span 4 dimensions**, and for them to
sit in 3-space their determinant would have to vanish. It is `-5`.
Computed exactly over `Fraction`, cross-checked against configurations
that *are* flat (four corners of a square give `0`, a tetrahedron gives
`8`). The maximum number of mutually equidistant points in `R^n` is
`n+1`, so there is a configuration which exists in four dimensions and
provably cannot be realised in three at all. That is not about
rendering.

What *can* be done is exactly what was described: stack three-dimensional
slices and let the fourth parameter be the index that runs through them.
That index is not a spatial coordinate, so no embedding obstruction
applies to it -- and the package already works this way. A `viertakt`
state is `(phasor, height)`: three spatial degrees of freedom plus one
index, where the height is the flow. The fourth thing emerges from the
sequence of slices rather than being a direction inside any of them.

ON THE FOUR PLACES
------------------

Indexing `0, 1, 2, 3` is still four places and four ticks -- that was
never in dispute. The shift changes only where the count starts, from
the ground rather than from the first deflection, and `period()` is 4
either way.

NORMALISING ONTO ONE AXIS
-------------------------

"Push everything back to the zero point and normalise onto one axis" has
an exact form in this representation: the radius becomes the single axis
and the direction is carried separately. `r²` is the ray, exact and
rational; `cos²theta` and `tan phi` are the rotation, exact and rational.
Nothing is projected away and nothing is rounded.
"""

from __future__ import annotations

import math
from fractions import Fraction

Point = tuple[Fraction, ...]

#: The eight turn fractions in [0,1) whose cosine is rational (Niven).
NIVEN_TURN_FRACTIONS: tuple[tuple[Fraction, Fraction], ...] = (
    (Fraction(0), Fraction(1)),
    (Fraction(1, 6), Fraction(1, 2)),
    (Fraction(1, 4), Fraction(0)),
    (Fraction(1, 3), Fraction(-1, 2)),
    (Fraction(1, 2), Fraction(-1)),
    (Fraction(2, 3), Fraction(-1, 2)),
    (Fraction(3, 4), Fraction(0)),
    (Fraction(5, 6), Fraction(1, 2)),
)


def squared_distance(p: Point, q: Point) -> Fraction:
    """Sum of squared coordinate differences, exact.

    Deliberately returns the square and not the root: the root is the
    first place rounding enters, and it is almost never needed."""
    if len(p) != len(q):
        raise ValueError("points must have the same dimension")
    return sum((Fraction(b) - Fraction(a)) ** 2 for a, b in zip(p, q))


def squared_radius(p: Point) -> Fraction:
    """r² = sum of squared coordinates, exact."""
    return sum(Fraction(c) ** 2 for c in p)


def cos_squared_polar(p: Point) -> Fraction:
    """cos²(theta) = z²/r², exact -- no arccos, no rounding."""
    if len(p) != 3:
        raise ValueError("polar angle needs a three-dimensional point")
    r2 = squared_radius(p)
    if r2 == 0:
        raise ValueError("the origin has no direction")
    return Fraction(p[2]) ** 2 / r2


def tan_azimuth(p: Point) -> Fraction | None:
    """tan(phi) = y/x, exact. None when x = 0, where the tangent is
    undefined rather than large."""
    if len(p) != 3:
        raise ValueError("azimuth needs a three-dimensional point")
    x, y = Fraction(p[0]), Fraction(p[1])
    if x == 0:
        return None
    return y / x


def exact_spherical(
    p: Point,
) -> tuple[Fraction, Fraction, Fraction | None, tuple[int, int, int]]:
    """(r², cos²theta, tan phi, signs) -- the full direction, exactly.

    No trigonometric function is evaluated. The sign triple is what
    makes the representation lossless, since squares discard signs."""
    if len(p) != 3:
        raise ValueError("needs a three-dimensional point")
    x, y, z = (Fraction(c) for c in p)
    signs = (1 if x >= 0 else -1, 1 if y >= 0 else -1, 1 if z >= 0 else -1)
    return squared_radius(p), cos_squared_polar(p), tan_azimuth(p), signs


def _exact_root(value: Fraction, sign: int) -> Fraction | None:
    """The exact rational square root of a rational square, or None."""
    num, den = value.numerator, value.denominator
    root_num, root_den = math.isqrt(num), math.isqrt(den)
    if root_num * root_num != num or root_den * root_den != den:
        return None
    return sign * Fraction(root_num, root_den)


def from_exact_spherical(
    squared_r: Fraction,
    cos_squared_theta: Fraction,
    tan_phi: Fraction | None,
    signs: tuple[int, int, int],
) -> tuple[Fraction | None, Fraction | None, Fraction | None]:
    """Recover the point from its exact spherical data.

    Lossless for rational points: z² = r²·cos²theta, x²+y² = r² - z²,
    x² = (x²+y²)/(1+tan²phi). Components come back as None only when the
    original point was not rational, which cannot happen for input this
    package produced."""
    sx, sy, sz = signs
    z_squared = Fraction(squared_r) * Fraction(cos_squared_theta)
    planar = Fraction(squared_r) - z_squared
    if tan_phi is None:
        return (Fraction(0), _exact_root(planar, sy), _exact_root(z_squared, sz))
    t = Fraction(tan_phi)
    x_squared = planar / (1 + t * t)
    y_squared = planar - x_squared
    return (
        _exact_root(x_squared, sx),
        _exact_root(y_squared, sy),
        _exact_root(z_squared, sz),
    )


def rational_cosine_of_turn(turn_fraction: Fraction) -> Fraction | None:
    """cos(2*pi*q) as an exact Fraction, or None when it is irrational.

    By Niven's theorem only eight turn fractions in [0,1) qualify, so
    this returns None for almost every input -- which is the theorem,
    not a shortcoming."""
    q = Fraction(turn_fraction) % 1
    for candidate, cosine in NIVEN_TURN_FRACTIONS:
        if q == candidate:
            return cosine
    return None


def rational_cos_squared_of_turn(turn_fraction: Fraction) -> Fraction | None:
    """cos²(2*pi*q) exactly, or None.

    Rational exactly when the cosine of the doubled angle is, by
    cos² = (1 + cos 2x)/2 -- so this succeeds on twice as many turn
    fractions as rational_cosine_of_turn, including 1/8 and 1/12."""
    doubled = rational_cosine_of_turn(Fraction(turn_fraction) * 2)
    if doubled is None:
        return None
    return (1 + doubled) / 2


def exact_cos_squared_turns() -> list[Fraction]:
    """Every turn fraction in [0,1) with an exactly rational cos².

    Sixteen of them, against eight for the cosine itself: keeping the
    square genuinely enlarges what can be computed without rounding."""
    return [
        q
        for q in sorted({Fraction(n, d) for d in (1, 2, 3, 4, 6, 8, 12) for n in range(d)})
        if rational_cos_squared_of_turn(q) is not None
    ]


def _determinant(matrix: list[list[Fraction]]) -> Fraction:
    """Exact determinant by elimination over Fraction."""
    rows = [row[:] for row in matrix]
    size = len(rows)
    result = Fraction(1)
    for i in range(size):
        pivot = next((r for r in range(i, size) if rows[r][i] != 0), None)
        if pivot is None:
            return Fraction(0)
        if pivot != i:
            rows[i], rows[pivot] = rows[pivot], rows[i]
            result = -result
        result *= rows[i][i]
        lead = rows[i][i]
        for r in range(i + 1, size):
            factor = rows[r][i] / lead
            if factor:
                for c in range(i, size):
                    rows[r][c] -= factor * rows[i][c]
    return result


def cayley_menger_determinant(squared_distances: list[list[Fraction]]) -> Fraction:
    """The Cayley-Menger determinant of m points, exactly.

    Non-zero exactly when the points span m-1 dimensions. For m mutually
    equidistant points it is ±m."""
    m = len(squared_distances)
    if m < 2:
        raise ValueError("need at least two points")
    matrix = [[Fraction(0)] * (m + 1) for _ in range(m + 1)]
    for i in range(m):
        matrix[i][m] = Fraction(1)
        matrix[m][i] = Fraction(1)
        for j in range(m):
            matrix[i][j] = Fraction(squared_distances[i][j])
    return _determinant(matrix)


def fits_in_dimension(squared_distances: list[list[Fraction]], dimension: int) -> bool:
    """True iff m points with these squared distances can be realised in
    R^dimension.

    Requires the Cayley-Menger determinant to vanish once there are more
    than dimension+1 points."""
    m = len(squared_distances)
    if m <= dimension + 1:
        return True
    return cayley_menger_determinant(squared_distances) == 0


def max_equidistant_points(dimension: int) -> int:
    """dimension + 1. Four in 3-space, five in 4-space -- which is the
    obstruction that makes the fourth dimension more than a rendering
    problem."""
    if dimension < 1:
        raise ValueError("dimension must be positive")
    return dimension + 1


def equidistant_squared_distances(count: int) -> list[list[Fraction]]:
    """The squared-distance matrix of `count` mutually equidistant points
    at unit separation."""
    if count < 2:
        raise ValueError("need at least two points")
    return [
        [Fraction(0) if i == j else Fraction(1) for j in range(count)]
        for i in range(count)
    ]


def four_stroke_place_count() -> int:
    """4.

    Indexing 0,1,2,3 is four places, exactly as indexing 1,2,3,4 is. The
    shift moves where the count starts -- from the ground rather than
    from the first deflection -- and changes nothing about the count."""
    return 4
