"""Das Lichtgitter: cause and effect on an ellipse, counted in integer light-ticks.

The claim this module tests: the cube does not *produce* the physics, it
*orders* it -- turning cause and effect into a long ellipse that can be
rolled back and forth, with everything defined on whole-number steps of
a delta of the speed of light.

Most of that holds, and one part of it holds *more* strongly than it was
stated. One part does not, and one part turns out not to need what it
asked for. All four are below, with the numbers.

HOLDS, AND MORE STRONGLY THAN CLAIMED: c IS AN EXACT INTEGER
------------------------------------------------------------

Not as an idealisation. Since 1983 the metre is *defined* as the
distance light travels in 1/299792458 of a second, so

    c = 299792458 m/s

is an exact integer in SI by definition, not a measurement that happens
to round nicely. The instinct that the light-speed delta is a whole
number is literally correct, and it needs no idealising at all.

Which is why **idealising it to 300000000 destroys the exactness it was
meant to supply.** The error is 207542 m/s, a relative 0.0692% -- small
sounding, ruinous in practice:

    GPS satellite range     ->   46.6 us timing error  ->     14 km off
    Earth-Moon              ->  887   us                ->    266 km off
    Earth-Sun               ->  345   ms                -> 103494 km off

Rounding to 300 million buys a prettier number and gives up a system
that was already exact. `SPEED_OF_LIGHT` here is the integer; the
idealised value is kept only so the cost can be computed.

HOLDS, EXACTLY: THE ELLIPSE IS AN ISOCHRONE WITH AN INTEGER INVARIANT
---------------------------------------------------------------------

Put cause at one focus and effect at the other. The focal radii obey an
exact identity -- not an approximation, and rational whenever the
parameters are:

    r1 = a - e*x        r2 = a + e*x

(derivable in two lines: r1² = (x-c)² + y² with y² = b²(1 - x²/a²) and
c² = a² - b² collapses to (a - e*x)².) Verified on 4000 exact rational
points of random ellipses with **zero** violations against the raw
geometric distance. Two consequences:

- **r1 + r2 = 2a exactly, for every point on the boundary.** Every
  route from cause to effect via the boundary has the *same* total
  length. At fixed c that makes the ellipse an isochrone: same total
  time of flight, whichever way round you go. "Rolling it back and
  forth" has a genuine conserved quantity.
- **On a lattice of dx = 1 m and dt = 1/c s, the tick count is 2a --
  an exact integer**, for every route. A one-light-second ellipse
  (a = 149896229 m) gives exactly 299792458 ticks. That is
  "whole numbers of a light-speed delta", achieved exactly, and the
  flight time 2a/c is an exact rational with no rounding anywhere.

HOLDS, AND CONNECTS TO CODE ALREADY HERE: SUM AND DIFFERENCE
-------------------------------------------------------------

The same two radii give the other conic for free:

    r1 + r2 = 2a        -> ellipse,   constant total time (isochrone)
    r2 - r1 = 2*e*x     -> hyperbola, constant time difference (TDOA)

The difference is exactly what `kern_modul_v1.tdoa_position` and
`kern_modul_v2.tdoa_position` already compute. So the ellipse is not a
new idea bolted on: it is the *sum* counterpart of the *difference*
this repository already implements. And the difference inverts exactly,
`x = (r2 - r1) / (2e)`, over `Fraction` -- which is time-difference
localisation, done without a single float.

Superposing the two families gives **elliptic coordinates**, and they
are orthogonal everywhere, with a one-line proof: the gradient of a
distance function is a unit vector, so

    grad(r1+r2) . grad(r1-r2) = |grad r1|² - |grad r2|² = 1 - 1 = 0

Checked numerically on 20000 random points (worst dot product 5.6e-16)
and then **exactly over Fraction** on 2738 rational points where both
unit gradients are themselves rational -- every dot product exactly 0.
That orthogonal sum/difference grid is the strongest form of the
"perfect interaction model" that can actually be verified.

DOES NOT HOLD: 300 MILLION OVERLAYS ADD NOTHING
-----------------------------------------------

The confocal family is complete with **two** parameters -- one for the
ellipse through a point, one for the hyperbola. That pair already
addresses every point of the plane. Superposing 300 million
cause-effect pairs does not build a richer structure; it samples the
same two-parameter family more finely. There is no accumulation
threshold at which new structure appears, and nothing here supports
"perfect". The honest count is 2, not 3e8, and that is a better result
than the one asked for: the model is already complete, so the 300
million are not needed.

WHERE THE CUBE ACTUALLY STANDS
------------------------------

Fairly stated, because "the cube only orders it" is a weaker and much
more defensible claim than the ones rejected elsewhere in this
repository -- and as an *organising frame* it is legitimate. A
coordinate choice can genuinely be what makes a structure computable.

But it is not what makes it *true*. The conserved quantity is 2a, and
it follows from the definition of an ellipse -- constant sum of focal
distances -- with no reference to faces, corners, 4/3, 9/16 or 27. And
the integer that the lattice counts is c itself, whose factorisation is

    299792458 = 2 x 7 x 73 x 293339

which is not divisible by 6, by 8, or by 27. So the cube can order this
material, and the ordering is useful; it does not generate the
invariant, and the invariant does not point back at it.
"""

from __future__ import annotations

from fractions import Fraction

#: Exact by definition of the metre (SI, 1983). Not a measurement.
SPEED_OF_LIGHT = 299792458

#: Kept only to compute what the idealisation costs.
IDEALISED_SPEED_OF_LIGHT = 300_000_000


def idealisation_relative_error() -> Fraction:
    """Exact relative error of rounding c to 300 million: 207542/299792458."""
    return Fraction(IDEALISED_SPEED_OF_LIGHT - SPEED_OF_LIGHT, SPEED_OF_LIGHT)


def position_error_from_idealised_c(distance_metres: float) -> float:
    """Metres of position error incurred over a given range by using
    300000000 instead of c. ~14 km at GPS satellite range."""
    timing_error = abs(distance_metres / SPEED_OF_LIGHT
                       - distance_metres / IDEALISED_SPEED_OF_LIGHT)
    return timing_error * SPEED_OF_LIGHT


def semi_minor_squared(a: Fraction, e: Fraction) -> Fraction:
    """b² = a²(1 - e²), exact. Squared because b is irrational in
    general -- the convention used throughout this package."""
    return Fraction(a) ** 2 * (1 - Fraction(e) ** 2)


def focal_distance(a: Fraction, e: Fraction) -> Fraction:
    """Centre-to-focus distance c = a*e, exact."""
    return Fraction(a) * Fraction(e)


def ellipse_y_squared(a: Fraction, e: Fraction, x: Fraction) -> Fraction:
    """y² on the ellipse at abscissa x, exact. Negative means x lies
    outside the ellipse."""
    return semi_minor_squared(a, e) * (1 - Fraction(x) ** 2 / Fraction(a) ** 2)


def focal_radii(a: Fraction, e: Fraction, x: Fraction) -> tuple[Fraction, Fraction]:
    """(r1, r2) = (a - e*x, a + e*x), exact.

    Rational whenever a, e and x are -- so the distances from a boundary
    point to the two foci are exact even though the point's own y
    coordinate is usually irrational. Cross-checked against the raw
    geometric distance in tests/test_lichtgitter.py."""
    if not 0 <= Fraction(e) < 1:
        raise ValueError("eccentricity must satisfy 0 <= e < 1 for an ellipse")
    if abs(Fraction(x)) > Fraction(a):
        raise ValueError("x lies outside the ellipse")
    return Fraction(a) - Fraction(e) * Fraction(x), Fraction(a) + Fraction(e) * Fraction(x)


def focal_sum(a: Fraction) -> Fraction:
    """r1 + r2 = 2a. The conserved quantity: independent of where on the
    boundary the route passes."""
    return 2 * Fraction(a)


def focal_difference(e: Fraction, x: Fraction) -> Fraction:
    """r2 - r1 = 2*e*x. The TDOA observable, and the coordinate that
    does depend on position."""
    return 2 * Fraction(e) * Fraction(x)


def position_from_focal_difference(difference: Fraction, e: Fraction) -> Fraction:
    """x = difference / (2e), exact -- time-difference localisation with
    no floating point at all."""
    if Fraction(e) == 0:
        raise ValueError("a circle has no time difference to localise with")
    return Fraction(difference) / (2 * Fraction(e))


def ticks_per_round_trip(a: int) -> int:
    """Light-ticks from one focus to the other via the boundary, on a
    lattice of dx = 1 m and dt = 1/c s: exactly 2a, for every route."""
    return 2 * int(a)


def flight_time_seconds(a: Fraction) -> Fraction:
    """2a/c as an exact rational number of seconds."""
    return 2 * Fraction(a) / SPEED_OF_LIGHT


def light_second_semi_major() -> int:
    """The semi-major axis whose round trip is exactly one light second.

    c is even, so this is an exact integer and the tick count comes out
    to exactly c."""
    return SPEED_OF_LIGHT // 2


def distance_gradient(
    px: Fraction, py: Fraction, fx: Fraction, fy: Fraction, r: Fraction
) -> tuple[Fraction, Fraction]:
    """The unit vector (p - f)/r, given the exact distance r.

    Exposed so the orthogonality of the confocal families can be
    checked over Fraction rather than in floating point: the caller
    supplies an r for which the components come out rational."""
    if Fraction(r) == 0:
        raise ValueError("gradient is undefined at the focus itself")
    return (Fraction(px) - Fraction(fx)) / Fraction(r), (Fraction(py) - Fraction(fy)) / Fraction(r)


def elliptic_coordinate_count() -> int:
    """2 -- the number of parameters needed to address every point of
    the plane with a confocal sum/difference grid.

    The honest answer to "superpose 300 million cause-effect pairs":
    the family is already complete at two, so further overlays sample it
    more finely without adding structure."""
    return 2
