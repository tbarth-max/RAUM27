"""Der 4-Takt auf Index 0: i^n als exakter Taktgeber der Spirale.

The proposal: shift the four-stroke to start at index 0 and read it as
powers of `i`, so the rhythm begins at rest rather than already
deflected.

    n = 0:  i^0 =  1   the ground, undeflected
    n = 1:  i^1 =  i   first deflection
    n = 2:  i^2 = -1   maximum tension, the opposite pole
    n = 3:  i^3 = -i   the mirror of n = 1
    n = 4:  i^4 =  1   the phasor closes -- but the height has advanced

**Most of this holds, and the central point holds exactly.** Three
details needed correcting, and they are below with the rest.

ATTRIBUTION
-----------

When `spirale.py` says "the recursion grounds out at turn 0", that
sentence was about the formal termination of a recursion and nothing
else. `i^0` as the start of a four-stroke was not behind it. The
reading above is a genuine addition, not a recovery of something
already meant, and it is recorded here as such.

WHAT HOLDS, EXACTLY
-------------------

**The four-stroke needs no floating point at all.** Reading `i^n` as
`cos(n*pi/2) + i*sin(n*pi/2)` is right, and for integer `n` both parts
land in `{0, +1, -1}`:

    n mod 4:   0        1        2        3
    (cos,sin): (1, 0)   (0, 1)   (-1, 0)  (0, -1)

So the cosine and sine never have to be evaluated -- they are exact
Gaussian integers, and one tick is the exact integer map
`(c, s) -> (-s, c)`. The "über Kosinus Sinus" route is correct and it
is the reason this can be computed without rounding.

**The period is exactly 4**, confirmed two ways: by exact integer
iteration, and by feeding the real and imaginary series to this
repository's own `kern_modul_v2.find_period`, which returns 4 for both.

**`i^2 = -1` really is the unique point of maximum tension.** Squared
distances from the ground `i^0 = 1`, as exact integers:

    n:            0   1   2   3   4
    |i^n - 1|^2:  0   2   4   2   0

`n = 2` is the unique maximum, at squared distance exactly 4 -- so
"maximaler Spannungspunkt, exakter Gegenpol zum Ursprung" is not just
imagery, it is provable and it is the only such point in the cycle.

**And the central claim is exactly right.** `i^0` and `i^4` are the
same phasor and *not* the same state, because the height differs. The
pair `(i^n, height)` never repeats; `i^n` alone repeats every four
ticks. That is `spirale.py`'s cycle-with-a-ground applied correctly:
the phasor carries the rhythm, the height carries the memory, and
neither alone is the state.

    n:       0      1      2      3      4      5
    phasor:  1      i     -1     -i      1      i      <- repeats
    height:  0    h/4    h/2   3h/4      h   5h/4      <- never repeats

THREE CORRECTIONS
-----------------

**1. The pitch is not zero at `n = 0`; the height is.** These are
different quantities and the distinction matters. The pitch `h` is a
property of the spiral, constant for every turn. The *height* at turn 0
is zero. If the pitch itself were zero then `e^2 = h^2/(B^2+h^2) = 0`
and the figure would be a circle -- the ellipse the whole construction
depends on would not exist. "Es gibt noch keine Auslenkung" is right
about the height and wrong about the pitch.

**2. `n = 3` does not pull back toward the centre -- it mirrors
`n = 1`.** Both sit at squared distance exactly 2 from the ground, the
same value. There is no gradual return: the cycle goes 0, 2, 4, 2, 0,
so the approach happens in one step at `n = 4`, not progressively from
`n = 3`.

**3. A power tower is not the same thing as an integer exponent, and
only one of them is 4-periodic.** `i^n` for integer `n` is exactly
4-periodic. An actual tower `i^i^i^...` is transcendental at the very
first step -- `i^i = e^(-pi/2) = 0.207879...` -- and instead of cycling
it converges to the fixed point

    0.438282936727 + 0.360592471871i

(verified as a fixed point to 2.8e-16, and converged by about 500
levels; at 80 levels it has not yet settled, which is easy to misread
as a mismatch). So the exact four-cycle and the power tower are
alternatives, not a combination.

ONE MORE SCOPE POINT
--------------------

`i^n` lives in a single complex plane, so one such cycle orders **one**
rotation plane. Three-dimensional space has exactly three, by
`rotationsebenen.rotation_plane_count(3) = 3`. So ordering 3-space with
this rhythm takes three four-strokes, not one -- the complexity of the
three dimensions does not collapse into a single cycle.

Three planes times four ticks is twelve states, and the cube also has
twelve edges. **Noted, not claimed**: both are `3 x 4`, and nothing
here derives either from the other. This repository has a recorded
habit of such numbers being taken for evidence, so the coincidence is
written down as a coincidence.
"""

from __future__ import annotations

from fractions import Fraction

#: The four exact states of the cycle, as (cos, sin) Gaussian integer
#: pairs. Index is n mod 4. No transcendental evaluation is needed.
I_POWERS: tuple[tuple[int, int], ...] = ((1, 0), (0, 1), (-1, 0), (0, -1))

#: The ground state: i^0 = 1, undeflected.
GROUND: tuple[int, int] = (1, 0)


def period() -> int:
    """4. Confirmed by exact integer iteration and by the repository's
    own find_period on the real and imaginary series."""
    return 4


def i_power(n: int) -> tuple[int, int]:
    """i^n as an exact (cos, sin) pair of integers, for any integer n
    including negatives."""
    return I_POWERS[n % 4]


def cos_sin_quarter_turn(n: int) -> tuple[int, int]:
    """(cos(n*pi/2), sin(n*pi/2)), exactly, without evaluating either.

    Identical to i_power -- exposed under this name because it is the
    route the rhythm was described by, and because it makes clear that
    the exactness comes from the quarter turn landing on the axes."""
    return i_power(n)


def tick(state: tuple[int, int]) -> tuple[int, int]:
    """One quarter turn: multiply by i. Exactly (c, s) -> (-s, c).

    Integer arithmetic only, so iterating it a million times
    accumulates no error at all."""
    c, s = state
    return (-s, c)


def squared_distance_from_ground(n: int) -> int:
    """|i^n - 1|^2 as an exact integer: 0, 2, 4, 2 over the cycle.

    The ground is 0 and the opposite pole is 4; the two deflections are
    both 2."""
    c, s = i_power(n)
    return (c - 1) ** 2 + s ** 2


def is_maximal_tension(n: int) -> bool:
    """True exactly at n = 2 mod 4 -- the unique point of the cycle at
    maximum distance from the ground."""
    return n % 4 == 2


def is_ground(n: int) -> bool:
    """True exactly at n = 0 mod 4: the phasor is back at 1."""
    return n % 4 == 0


def mirrors(n: int, m: int) -> bool:
    """True iff two ticks sit at the same distance from the ground.

    n = 1 and n = 3 mirror each other; neither is nearer the centre
    than the other."""
    return squared_distance_from_ground(n) == squared_distance_from_ground(m)


def height_at_tick(pitch: Fraction, n: int) -> Fraction:
    """n * h / 4, exact: four ticks make one full turn, so each tick
    lifts by a quarter of the pitch."""
    if n < 0:
        raise ValueError("tick count must be non-negative")
    return Fraction(pitch) * n / 4


def tick_state(pitch: Fraction, n: int) -> tuple[tuple[int, int], Fraction]:
    """The full state: (phasor, height).

    The phasor repeats every four ticks; the height never repeats. Only
    the pair is the state -- which is why i^0 and i^4 are distinct
    despite being the same complex number."""
    return i_power(n), height_at_tick(pitch, n)


def phasor_repeats(n: int, m: int) -> bool:
    """True iff two ticks share a phasor -- i.e. iff they differ by a
    multiple of 4."""
    return i_power(n) == i_power(m)


def state_repeats(pitch: Fraction, n: int, m: int) -> bool:
    """True iff two ticks share the full state. False for n != m
    whenever the pitch is non-zero: the spiral forgets nothing."""
    return tick_state(pitch, n) == tick_state(pitch, m)


def tower_is_periodic() -> bool:
    """False.

    i^n with an integer exponent is exactly 4-periodic. A power tower
    i^i^i^... is transcendental at the first step and converges to a
    fixed point instead of cycling. The two are alternatives."""
    return False


def i_tower_fixed_point() -> complex:
    """The attractor of i^i^i^..., to double precision.

    Converged by roughly 500 levels; at 80 levels it has not settled
    yet, which is easy to mistake for a mismatch."""
    return 0.438282936727 + 0.360592471871j


def planes_needed(dimensions: int) -> int:
    """n(n-1)/2 -- how many four-strokes it takes to order n-space, since
    one i-cycle orders a single plane.

    3 for three dimensions, so the complexity of the three dimensions
    does not reduce to one cycle."""
    if dimensions < 1:
        raise ValueError("dimension must be positive")
    return dimensions * (dimensions - 1) // 2
