"""Die Spirale: a repeating process as a computable object, exactly.

This is the piece the framework was missing: something to **compute
with**, not talk about. A process that has cause and effect and repeats
is one turn of a spiral. The turn closes in angle -- that is the cycle
-- and advances in height -- that is why it is not a vicious circle.
And the height is what generates the ellipse, which is what makes the
whole thing definable.

CIRCLE, SPIRAL, AND CIRCULARITY ARE THREE DIFFERENT THINGS
----------------------------------------------------------

Worth separating, because this package uses "circular" as a defect
elsewhere and that is a different word for a different thing.

A **circular definition** has no ground: `A` because `B` because `A`.
Nothing can be evaluated, because every evaluation needs its own result
as input. That is the failure mode flagged in the README.

A **cycle** is a structure that returns to its starting configuration.
Nothing wrong with it, but on its own it stores no history: after one
turn you cannot tell whether you have gone round once or a thousand
times.

A **spiral** is the resolution of both. Turn `n` is computed from turn
`n-1` and never from itself, so the recursion grounds out at turn 0 --
formally acyclic. And the height records how many turns have passed, so
nothing is lost. **A spiral is a cycle with a ground.** That is exactly
why a process modelled as a spiral is computable while the same process
modelled as a closed loop is not.

THE CONSTRUCTION, AND IT IS EXACT
---------------------------------

Unroll one turn of a helix on a cylinder. The base is the circumference
`B`, the rise is the pitch `h`, and the turn itself is the hypotenuse:

    L² = B² + h²        (Pythagoras -- exact, no pi anywhere)

Cutting the cylinder with a plane at the helix's own angle gives a
genuine ellipse, with semi-minor axis `b = r` (the cylinder radius) and
semi-major `a = r/cos(theta)`. Two statements fall out that are exact
and completely free of `pi`, provided the spiral is given by its
circumference rather than its radius:

    (a/b)² = 1 + (h/B)²
    e²     = h² / (B² + h²)

So **the pitch alone decides the shape of the ellipse.** At `h = 0` the
eccentricity is 0 and the figure is a circle: the height is the only
thing that makes it an ellipse at all. And the semi-major axis is the
turn length over `2pi`, `a = L/(2*pi)` -- verified numerically, with the
`pi` appearing only when you ask for an absolute size rather than a
ratio.

WHEN IT IS EXACTLY RATIONAL
---------------------------

`e = h/L` is a rational number exactly when `L² = B² + h²` is a perfect
square -- that is, exactly when `(B, h, L)` is a Pythagorean triple:

    (4, 3, 5)    -> e = 3/5,   a/b = 5/4
    (12, 5, 13)  -> e = 5/13,  a/b = 13/12
    (8, 15, 17)  -> e = 15/17, a/b = 17/8
    (20, 21, 29) -> e = 21/29, a/b = 29/20

For `B = h = 1`, `L² = 2` and the eccentricity is irrational, so this
module refuses to return it as a `Fraction` rather than quietly
rounding. (An earlier draft of the check used `isqrt(2) = 1` and
reported `e = 1`; `is_rational_spiral` exists so that cannot happen
again.)

WHAT THIS LETS YOU COMPUTE
--------------------------

A Pythagorean spiral hands `lichtgitter` an exactly rational
eccentricity, and from there the whole ellipse is exact: the focal radii
`r1 = a - e*x` and `r2 = a + e*x` are rational, their sum is the
conserved `2a`, and the position `x` is recoverable from the difference.
So a repeating process, given as `(circumference, pitch, turn count)`,
has an exact state and an exact per-turn invariant -- `L²` is the same
for every turn no matter how many have passed, while the height
distinguishes them.

That is a closed computational loop in the useful sense: cause to
effect to the next cause, with nothing left undefined and nothing
needing itself as input.
"""

from __future__ import annotations

import math
from fractions import Fraction


def turn_length_squared(circumference: Fraction, pitch: Fraction) -> Fraction:
    """L² = B² + h², exact. The squared length of one turn of the spiral.

    This is the per-turn invariant: the same for every turn, however
    many have passed."""
    if Fraction(circumference) <= 0:
        raise ValueError("circumference must be positive")
    return Fraction(circumference) ** 2 + Fraction(pitch) ** 2


def is_rational_spiral(circumference: Fraction, pitch: Fraction) -> bool:
    """True iff L² is a perfect square of a rational, i.e. iff the
    eccentricity comes out as an exact Fraction.

    Equivalently: iff (B, h, L) is a Pythagorean triple, up to a common
    rational scale."""
    value = turn_length_squared(circumference, pitch)
    num, den = value.numerator, value.denominator
    root_num, root_den = math.isqrt(num), math.isqrt(den)
    return root_num * root_num == num and root_den * root_den == den


def turn_length(circumference: Fraction, pitch: Fraction) -> Fraction:
    """L, exact -- but only for a rational spiral.

    Raises rather than rounding when L is irrational, so an irrational
    eccentricity can never be silently reported as a Fraction."""
    value = turn_length_squared(circumference, pitch)
    if not is_rational_spiral(circumference, pitch):
        raise ValueError(
            f"turn length is irrational (L^2 = {value}); use turn_length_squared"
        )
    return Fraction(math.isqrt(value.numerator), math.isqrt(value.denominator))


def eccentricity_squared(circumference: Fraction, pitch: Fraction) -> Fraction:
    """e² = h²/(B² + h²), exact and always rational.

    Zero exactly when the pitch is zero: without height there is no
    ellipse, only a circle."""
    return Fraction(pitch) ** 2 / turn_length_squared(circumference, pitch)


def eccentricity(circumference: Fraction, pitch: Fraction) -> Fraction:
    """e = h/L, exact -- for a rational spiral. Raises otherwise."""
    return abs(Fraction(pitch)) / turn_length(circumference, pitch)


def axis_ratio_squared(circumference: Fraction, pitch: Fraction) -> Fraction:
    """(a/b)² = 1 + (h/B)², exact. The ellipse's shape, free of pi."""
    return 1 + Fraction(pitch) ** 2 / Fraction(circumference) ** 2


def semi_major_axis(circumference: Fraction, pitch: Fraction) -> float:
    """a = L/(2*pi). Returns a float, because this is the one quantity
    where pi genuinely enters -- an absolute size rather than a ratio."""
    return math.sqrt(float(turn_length_squared(circumference, pitch))) / (2 * math.pi)


def semi_minor_axis(circumference: Fraction) -> float:
    """b = r = B/(2*pi), the cylinder radius. Also a float, for the same
    reason."""
    if Fraction(circumference) <= 0:
        raise ValueError("circumference must be positive")
    return float(circumference) / (2 * math.pi)


def pythagorean_spirals(limit: int) -> list[tuple[int, int, int]]:
    """Every (B, h, L) with L <= limit that gives an exactly rational
    eccentricity, in lowest terms."""
    if limit < 1:
        raise ValueError("limit must be positive")
    found = []
    for b in range(1, limit):
        for h in range(1, limit):
            l_squared = b * b + h * h
            root = math.isqrt(l_squared)
            if root * root == l_squared and root <= limit and math.gcd(b, h) == 1:
                found.append((b, h, root))
    return sorted(found, key=lambda t: (t[2], t[0]))


def height_after(pitch: Fraction, turns: int) -> Fraction:
    """n·h, exact. What the spiral records and a closed cycle does not:
    how many turns have passed."""
    if turns < 0:
        raise ValueError("turn count must be non-negative")
    return Fraction(pitch) * turns


def arc_after(circumference: Fraction, pitch: Fraction, turns: int) -> Fraction:
    """n·L, exact, for a rational spiral."""
    if turns < 0:
        raise ValueError("turn count must be non-negative")
    return turn_length(circumference, pitch) * turns


def returns_to_the_same_angle(turns: int) -> bool:
    """True for every whole turn count: the angle closes, which is the
    cycle. The height does not, which is the advance."""
    return turns == int(turns)


def process_state(
    circumference: Fraction, pitch: Fraction, turns: int
) -> dict[str, Fraction]:
    """The exact state of a repeating process after n turns.

    Fully determined by (circumference, pitch, turns) -- nothing else,
    and no step needs its own output as input. The per-turn invariant is
    returned alongside, to make explicit that it does not drift."""
    if turns < 0:
        raise ValueError("turn count must be non-negative")
    state = {
        "turns": Fraction(turns),
        "height": height_after(pitch, turns),
        "turn_invariant_squared": turn_length_squared(circumference, pitch),
        "eccentricity_squared": eccentricity_squared(circumference, pitch),
        "axis_ratio_squared": axis_ratio_squared(circumference, pitch),
    }
    if is_rational_spiral(circumference, pitch):
        state["arc"] = arc_after(circumference, pitch, turns)
        state["eccentricity"] = eccentricity(circumference, pitch)
    return state


def step(state: dict[str, Fraction], circumference: Fraction, pitch: Fraction) -> dict[str, Fraction]:
    """One turn forward, from the previous state only.

    This is what makes the structure formally acyclic despite being
    cyclic: `step` reads turn n-1 and writes turn n, and never needs
    turn n. The recursion grounds out at turn 0."""
    return process_state(circumference, pitch, int(state["turns"]) + 1)
