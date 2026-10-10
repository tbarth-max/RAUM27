"""Die Herleitungen von 4/3 und 16/9, einzeln geprüft.

Five derivations were offered for `4/3` and `16/9`, with the conclusion
that they are "geometric, topological and mathematical necessities"
rather than invented magic numbers. **That conclusion is correct.** Both
numbers do have exact derivations in this framework. But they are not
the five that were offered: of those, one works only after being
repaired, one points at a real derivation without being one, one is a
true statement with no explanatory force, and two are wrong or empty.

The repaired version and the real cube route are both stronger than the
originals, so this module keeps all of it -- the verdicts and the
better arguments -- in the repository's usual form: checkable, with the
negative results kept rather than dropped.

1. THE SPHERE VOLUME, WITH pi "BANISHED" -- FAILS, BUT IS REPAIRABLE
--------------------------------------------------------------------

Claim: `V = (4/3)·pi·r³` with `r = 1` and `pi` set aside leaves `4/3` as
the naked three-dimensional scalar.

As stated this does not hold, for two reasons that are both arithmetic.
Setting `r = 1` alone gives `V = 4pi/3 = 4.18879...`, not `4/3`; the
`4/3` only appears after separately deciding to divide by exactly one
power of `pi`. And that decision is not a single operation: the n-ball
volume is `pi^(n/2)/Gamma(n/2+1)`, so dividing by `pi^1` leaves a
rational only in dimensions 1, 2 and 3. In 4 dimensions it leaves
`pi/2`, in 5 it leaves `8pi/15`. The power you must strip depends on the
dimension, so "take pi out" is not a law but a per-case choice. And the
answer depends entirely on what you strip: `V_3/pi = 4/3`,
`V_3/(2pi) = 2/3`, `V_3/(4pi) = 1/3`.

**The repair, which is better than the original.** `4/3` *is* an exact,
pi-free fact about the sphere -- as a ratio, where `pi` cancels
legitimately and nothing has to be banished:

    V_sphere / V_cylinder(radius r, height r)
        = (4/3)·pi·r³ / (pi·r²·r)
        = 4/3,  exactly, for every r.

That is a genuine geometric derivation of `4/3`. Its sibling is
Archimedes' own result -- against the cylinder of height `2r` the ratio
is `2/3`, and it is on his tombstone. Use this version; it needs no
special pleading about transcendental constants.

2. A 4-STROKE PROJECTED ON 3 DIMENSIONS -- VALID BUT EMPTY
----------------------------------------------------------

Claim: projecting a causal 4-stroke onto a 3-dimensional lattice
mathematically forces `4:3`.

The projection statement is true and it is also true of every other
pair: a `p`-cycle on a `q`-lattice repeats with period `lcm(p,q)` and
carries the ratio `p/q`. A 5-stroke on 3 dimensions forces `5/3`, a
7-stroke forces `7/3`. Nothing in the argument produces the 4 -- the
4-stroke is the premise, and the conclusion is the premise divided by
3. This is the failure mode recorded elsewhere in this repository: a
number placed into a slot that was already shaped to receive it.

**But `4/3` does have a genuine cube derivation, and it is already in
this repository.** `cube_symmetry.coupling_constant()` is
`8 corners / 6 faces = 4/3`, an exact ratio of two exact counts. The
cube's 4 space diagonals over 3 axes gives the same thing -- and it is
the *same* derivation, not a second one, since 8 corners is twice 4
diagonals and 6 faces is twice 3 axes. One route, counted twice.

3. THE PERFECT FOURTH -- TRUE, AND NOT EXPLANATORY
--------------------------------------------------

`4/3` is exactly the perfect fourth in Pythagorean tuning. No dispute.

The question is whether that explains anything about space, and the
answer is no -- for a reason that can be quantified. Among fractions
strictly between 1 and 2 with denominator at most 7 there are only 17,
and `4/3` ranks second by simplicity. It is one of the very simplest
ratios that exists. Simple ratios recur across unrelated domains
*because* they are simple, so finding `4/3` in music and in sphere
geometry is what simple ratios do, not evidence of a shared cause.
`3/2` recurs at least as often and nobody infers a hidden mechanism
from it.

4. "SUPERPOSITION SQUARES" -- WRONG AS STATED
---------------------------------------------

Claim: two interfering systems square, so `(4/3)² = 16/9` is the
maximum resonance amplitude when two three-dimensional systems meet.

The arithmetic is right and the physics is not. Superposition is
**linear**: amplitudes add, and it is *intensity* that goes as the
square. Two fields of amplitude `4/3` give amplitude `8/3` and intensity
`64/9` when coherent, or `32/9` when incoherent -- checked against this
repository's own `phasor_resonanzfilter.energy`. Neither is `16/9`.

`16/9` is one field's intensity at amplitude `4/3`. That is a different
statement from the superposition of two of them, and no convention makes
them the same.

**The working route to `16/9` is the cube one**: `(8/6)² = 16/9`
exactly, i.e. the square of the corner-to-face ratio. That is exact and
needs no claim about interference.

5. "16/9 x 9/16 = 1 PROVES THE BALANCE" -- TRUE AND EMPTY
--------------------------------------------------------

The identity holds, and it holds for **every** non-zero `x`, so it
distinguishes `16/9` in no way whatsoever. This repository already
proves exactly that, for arbitrary reciprocal pairs, in
`tests/test_waage.py::test_every_reciprocal_pair_balances_at_exactly_one`.
`x · (1/x) = 1` is a property of division, not of `16/9`.

The related physical claim -- that the system must collapse to zero
torque or tear apart -- is also not shown by this identity. What *is*
shown, separately and for real, is `waage.residual_torque` being exactly
zero at the centre of mass for any number of weights in any
arrangement. That result stands on its own and does not need `16/9`.

WHAT SURVIVES
-------------

Both numbers have exact derivations. There are two, and they are
independent of each other:

    4/3  = V_sphere / V_cylinder(r, h=r)          (pi cancels, exact)
    4/3  = 8 corners / 6 faces                     (exact cube counts)
    16/9 = (8/6)²                                  (exact, the square of it)

So the conclusion that `4/3` and `16/9` are not arbitrary is **right**.
What does not survive is the claim that they follow from banishing `pi`,
from a 4-stroke, from musical consonance, from superposition, or from
`x · (1/x) = 1`. Keeping the distinction is the point: an argument that
does not hold weakens a conclusion that is true, because it invites the
reader to reject both at once.

On the framing: a derivation that "stifles every doubt at the root" is
the opposite of what makes this repository worth anything. The stated
ethos is "question everything, benchmark everything, keep only what
survives" -- and `4/3` survives. It survives on two arguments rather
than five, and it is better documented for having lost three.
"""

from __future__ import annotations

import math
from fractions import Fraction


def n_ball_volume(dimension: int, radius: float = 1.0) -> float:
    """pi^(n/2)/Gamma(n/2+1) · r^n -- the volume of the unit n-ball."""
    if dimension < 1:
        raise ValueError("dimension must be positive")
    return math.pi ** (dimension / 2) / math.gamma(dimension / 2 + 1) * radius ** dimension


def pi_power_in_n_ball(dimension: int) -> int:
    """The power of pi that must be stripped from the n-ball volume to
    leave a rational: floor(n/2).

    1 in dimensions 2 and 3, but 2 in dimensions 4 and 5 -- which is why
    "take pi out" is not a single operation."""
    if dimension < 1:
        raise ValueError("dimension must be positive")
    return dimension // 2


def rational_part_of_n_ball(dimension: int) -> Fraction:
    """The rational factor of the n-ball volume, exactly.

    4/3 in three dimensions, but 1/2 in four and 8/15 in five -- so 4/3
    is the *name* of the 3-ball's rational part, not a prediction of
    it."""
    value = n_ball_volume(dimension) / math.pi ** pi_power_in_n_ball(dimension)
    return Fraction(value).limit_denominator(10 ** 6)


def sphere_to_cylinder_ratio() -> Fraction:
    """4/3, exactly: the sphere's volume over that of the cylinder with
    the same radius and height equal to the radius.

    THE REPAIRED DERIVATION. pi cancels in the ratio, so nothing has to
    be banished, and the result is exact for every radius."""
    return Fraction(4, 3)


def archimedes_ratio() -> Fraction:
    """2/3: sphere over the circumscribing cylinder of height 2r -- the
    result on Archimedes' tombstone, and the sibling of the above."""
    return Fraction(2, 3)


def cycle_on_lattice_ratio(cycle: int, dimensions: int) -> Fraction:
    """p/q for a p-cycle on a q-lattice.

    Returns the ratio for any pair, which is the point: the argument
    derives p/q from assuming p and q, and nothing in it produces 4."""
    if cycle < 1 or dimensions < 1:
        raise ValueError("cycle and dimension counts must be positive")
    return Fraction(cycle, dimensions)


def cycle_on_lattice_period(cycle: int, dimensions: int) -> int:
    """lcm(p, q) -- when the projected pattern repeats."""
    if cycle < 1 or dimensions < 1:
        raise ValueError("cycle and dimension counts must be positive")
    return math.lcm(cycle, dimensions)


def simple_fractions_between_one_and_two(max_denominator: int) -> list[Fraction]:
    """Every fraction strictly between 1 and 2 with denominator at most
    the given bound, in lowest terms.

    Used to quantify how unsurprising it is that 4/3 turns up in several
    places: there are very few simple ratios, so they recur."""
    if max_denominator < 1:
        raise ValueError("denominator bound must be positive")
    found = {
        Fraction(n, d)
        for d in range(1, max_denominator + 1)
        for n in range(d + 1, 2 * d + 1)
        if 1 < Fraction(n, d) < 2
    }
    return sorted(found, key=lambda f: (f.denominator, f.numerator))


def coherent_superposition_intensity(amplitudes: list[Fraction]) -> Fraction:
    """(SUM a_i)² -- amplitudes add, then the sum is squared.

    Two fields of 4/3 give 64/9, not 16/9."""
    total = sum(Fraction(a) for a in amplitudes)
    return total ** 2


def incoherent_superposition_intensity(amplitudes: list[Fraction]) -> Fraction:
    """SUM a_i² -- the intensities add. Two fields of 4/3 give 32/9."""
    return sum(Fraction(a) ** 2 for a in amplitudes)


def single_field_intensity(amplitude: Fraction) -> Fraction:
    """a². This is what 16/9 actually is at amplitude 4/3 -- one field,
    not two superposed."""
    return Fraction(amplitude) ** 2


def superposition_squares_as_claimed() -> bool:
    """False. Superposition is linear; squaring is what turns one
    amplitude into one intensity, not what combines two fields."""
    return False


def reciprocal_identity_distinguishes(x: Fraction) -> bool:
    """False for every x: x·(1/x) = 1 is a property of division, so it
    singles out 16/9 no more than any other value."""
    if Fraction(x) == 0:
        raise ValueError("zero has no reciprocal")
    return False


def surviving_derivations() -> dict[str, Fraction]:
    """The derivations that hold, after checking all five offered.

    Two independent routes to 4/3, and the square of one of them for
    16/9. The conclusion that the numbers are not arbitrary is correct;
    the surviving reasons are not the ones originally given."""
    return {
        "sphere_over_cylinder_height_r": Fraction(4, 3),
        "cube_corners_over_faces": Fraction(8, 6),
        "square_of_the_cube_ratio": Fraction(8, 6) ** 2,
    }
