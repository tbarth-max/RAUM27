"""Die Schalenleiter: wie die Schalen zwischen 1 und der Außengrenze liegen.

A good question was put precisely: the reciprocal map `I(r) = 1/r` is
already exactly defined, but it **does not determine the spacing of the
shells** between the central 1 and the outer bound. Linear, logarithmic
and a ratio sequence are mathematically different, and the question was
which of them the model already fixes.

It turns out the model already fixes it, and not by preference. The
answer follows from two laws that were in the summary, with nothing new
laid on top.

LAW 4 FORCES GEOMETRIC SPACING
------------------------------

The stated requirement is that inner and outer are not independent lists
but one structure under the same reference and the same transformation
rules. So ask which kind of spacing *survives the inversion*:

- A **linear** ladder outside, `1, 2, 3, 4, 5`, maps to
  `1, 1/2, 1/3, 1/4, 1/5` inside. Its differences are
  `-1/2, -1/6, -1/12, -1/20` -- not constant, and the ratios are not
  constant either. Inside it is neither linear nor geometric. Checked on
  20000 random linear ladders: **0** remain linear.
- A **geometric** ladder outside, `1, 8, 64, 512`, maps to
  `1, 1/8, 1/64, 1/512` inside -- geometric again, with ratio `1/r`.
  Checked on 20000 random geometric ladders: **20000** remain geometric.

So if inner and outer must obey the same rule, the spacing has to be
geometric. That is a derivation, not a choice: linear spacing breaks
Law 4 on its own.

AND GEOMETRIC SPACING EXCLUDES 300 000 000
------------------------------------------

A geometric ladder from 1 to `N` in `n` steps needs `N = r^n` with `r`
rational. Since `N` is an integer, `r` is rational only if `N` is a
perfect `n`-th power, which happens exactly when `n` divides the gcd of
`N`'s prime exponents. And

    300 000 000 = 2^8 * 3 * 5^8,    gcd(8, 1, 8) = 1

so 300 000 000 is a perfect `n`-th power **only for n = 1**. The
candidate ratios are all irrational: `17320.5...` for two stages,
`669.43...` for three, `11.47...` for eight, `8.75...` for nine.

**Therefore 300 000 000 is incompatible with Law 4 for more than a
single shell.** Either the outer bound moves, or the shells are not
exact, or inner and outer stop sharing a rule. There is no fourth
option, and this is not a matter of taste.

The same holds for the exact speed of light:
`299 792 458 = 2 * 7 * 73 * 293339`, whose exponent gcd is also 1. So
neither the round 300 million nor the exact `c` carries a ladder.

The shell list that was submitted in code was already inconsistent with
itself on this point: `(1, 100, 10 000, 300 000 000)` has ratios
`100, 100, 30 000`. Three stages of a ratio-100 ladder end at `10^6`,
not at `3 * 10^8`.

WHAT DOES WORK, AND IT IS ALREADY IN THIS PACKAGE
-------------------------------------------------

    16 777 216 = 2^24,    gcd of exponents = 24

which is `zahlensysteme.cube_scaling_count()` and also
`zahlensysteme.rgb_color_count()` -- `8^8` and `16^6`, already tested to
be the same number. Because the exponent gcd is 24, exact ladders exist
for **every stage count dividing 24**: 1, 2, 3, 4, 6, 8, 12 and 24, with
integer ratios 16777216, 4096, 256, 64, 16, 8, 4 and 2.

For **nine** stages specifically, the two nearest exact bounds are

    8^9 = 134 217 728 = 2^27      (ratio 8)
    9^9 = 387 420 489 = 3^18      (ratio 9)

and 300 000 000 sits between them without being either.

THREE CAVEATS, SO THIS IS NOT OVER-READ
---------------------------------------

**The 27 in `2^27` is not the project's 27.** It is forced by `8 = 2^3`
and `3 * 9 = 27`: pick ratio 8 and nine stages and the exponent is 27 by
arithmetic. Nothing about cube geometry enters. The coincidence is real
and it is only a coincidence, recorded here as one.

**The ratio 8 is a choice, not a result.** Eight is the cube's corner
count, which makes it an attractive choice, and `8^8 = 2^24` landing on
a number this package already holds for an unrelated reason is a genuine
cross-check. But nothing derives the ratio. Ratios 2, 4, 16, 64, 256 and
4096 all give exact ladders to the same bound.

**This module does not say what the shells mean.** It says which
spacings are compatible with the stated laws and which outer bounds a
given stage count can reach exactly. No frequency, no physical scale and
no claim about what a shell transition does -- consistent with
`zustandsmaschine`, which keeps the shell index as bookkeeping for the
same reason.
"""

from __future__ import annotations

from fractions import Fraction
from math import gcd

from raum27.rational_space import involution

#: The outer bound as stated in the model: an idealised speed of light.
STATED_OUTER_BOUND = 300_000_000


def prime_exponents(value: int) -> dict[int, int]:
    """The prime factorisation of a positive integer, as {prime: exponent}."""
    if value < 1:
        raise ValueError("value must be a positive integer")
    remaining = value
    factors: dict[int, int] = {}
    divisor = 2
    while divisor * divisor <= remaining:
        while remaining % divisor == 0:
            factors[divisor] = factors.get(divisor, 0) + 1
            remaining //= divisor
        divisor += 1
    if remaining > 1:
        factors[remaining] = factors.get(remaining, 0) + 1
    return factors


def exponent_gcd(value: int) -> int:
    """The gcd of the prime exponents -- the largest n for which the value
    is a perfect n-th power.

    1 for 300000000 and for the exact speed of light; 24 for 2^24."""
    if value == 1:
        return 0  # 1 is a perfect n-th power for every n
    result = 0
    for exponent in prime_exponents(value).values():
        result = gcd(result, exponent)
    return result


def exact_stage_counts(value: int) -> list[int]:
    """Every stage count for which a geometric ladder from 1 reaches the
    value exactly with a rational ratio.

    These are the divisors of the exponent gcd -- so [1] alone for
    300000000, and 1, 2, 3, 4, 6, 8, 12, 24 for 2^24."""
    if value == 1:
        raise ValueError("a ladder to 1 is the trivial one-point ladder")
    limit = exponent_gcd(value)
    return [n for n in range(1, limit + 1) if limit % n == 0]


def admits_exact_ladder(value: int, stages: int) -> bool:
    """True iff a geometric ladder of this many stages reaches the value
    exactly. False for 300000000 at every stage count above 1."""
    if stages < 1:
        raise ValueError("stage count must be >= 1")
    return value != 1 and exponent_gcd(value) % stages == 0


def integer_nth_root(value: int, degree: int) -> int:
    """The floor of the n-th root, computed in integers only.

    Deliberately not `round(value ** (1 / degree))`: that is a float, and
    for large values its error can exceed 1, so a search around it is
    correct by luck rather than by construction. In a module whose point
    is exactness, the float has no business being here. Newton's method
    on integers has no such limit."""
    if value < 0:
        raise ValueError("value must be non-negative")
    if degree < 1:
        raise ValueError("degree must be >= 1")
    if value < 2:
        return value
    guess = 1 << ((value.bit_length() + degree - 1) // degree)
    while True:
        nxt = ((degree - 1) * guess + value // guess ** (degree - 1)) // degree
        if nxt >= guess:
            return guess
        guess = nxt


def exact_ratio(value: int, stages: int) -> int:
    """The integer ratio of the exact ladder, or a refusal.

    Refuses rather than returning a rounded root, which is the whole
    point: an inexact ratio breaks the exactness the package is built
    on. The root itself is computed in integers, so the result is exact
    by construction and the refusal below cannot fire for a value that
    `admits_exact_ladder` accepted."""
    if not admits_exact_ladder(value, stages):
        raise ValueError(
            f"{value} is not a perfect {stages}-th power, so no rational "
            f"ratio reaches it in {stages} stages"
        )
    ratio = integer_nth_root(value, stages)
    # No refusal here. admits_exact_ladder has already established that
    # the value is a perfect `stages`-th power, and integer_nth_root is
    # exact rather than a float guess, so the root is the ratio. The
    # earlier version had a defensive raise at this point; it was only
    # needed because the root was computed in floating point.
    assert ratio ** stages == value, "integer_nth_root contract violated"
    return ratio


def geometric_ladder(ratio: Fraction, stages: int) -> list[Fraction]:
    """The outer shells: 1, r, r², ..., r^stages. Exact."""
    if stages < 0:
        raise ValueError("stage count must be >= 0")
    r = Fraction(ratio)
    if r <= 0:
        raise ValueError("ratio must be positive")
    return [r ** k for k in range(stages + 1)]


def inner_ladder(outer: list[Fraction]) -> list[Fraction]:
    """The inner shells, by the reciprocal map already in the package."""
    return [involution(Fraction(value)) for value in outer]


def has_constant_ratio(ladder: list[Fraction]) -> bool:
    """True iff consecutive values share one ratio -- i.e. geometric."""
    if len(ladder) < 3:
        return True
    ratios = {ladder[i + 1] / ladder[i] for i in range(len(ladder) - 1)}
    return len(ratios) == 1


def has_constant_difference(ladder: list[Fraction]) -> bool:
    """True iff consecutive values share one difference -- i.e. linear."""
    if len(ladder) < 3:
        return True
    differences = {ladder[i + 1] - ladder[i] for i in range(len(ladder) - 1)}
    return len(differences) == 1


def survives_inversion(ladder: list[Fraction]) -> bool:
    """True iff the ladder's *kind* of spacing is preserved by `1/r`.

    Geometric ladders survive -- the ratio becomes its reciprocal and the
    kind is unchanged. Linear ladders do not: 1, 2, 3, 4 inverts to
    1, 1/2, 1/3, 1/4, which is neither linear nor geometric. This is why
    Law 4 forces geometric spacing rather than leaving it open."""
    inverted = inner_ladder(ladder)
    if has_constant_ratio(ladder):
        return has_constant_ratio(inverted)
    if has_constant_difference(ladder):
        return has_constant_difference(inverted)
    return False


def nine_stage_bounds() -> dict[int, int]:
    """The exact outer bounds a nine-stage ladder can reach, by ratio.

    `8^9 = 2^27` and `9^9 = 3^18` bracket the stated 300000000 without
    either equalling it."""
    return {ratio: ratio ** 9 for ratio in range(2, 11)}


def nearest_exact_bounds(target: int, stages: int) -> tuple[int, int]:
    """The exact `stages`-stage bounds immediately below and above the
    target. (134217728, 387420489) for 300000000 at nine stages."""
    if stages < 1:
        raise ValueError("stage count must be >= 1")
    below = above = None
    ratio = 1
    while True:
        value = ratio ** stages
        if value <= target:
            below = value
        else:
            above = value
            break
        ratio += 1
    return below, above


def cluster_bound(ratio: int, stages: int, cluster: int) -> int:
    """The top of cluster `m`, when each cluster's top becomes the next
    cluster's 1: `ratio ** (stages * cluster)`.

    Cluster 0 is the origin, 1."""
    if ratio < 2:
        raise ValueError("ratio must be at least 2")
    if stages < 1 or cluster < 0:
        raise ValueError("stages must be >= 1 and cluster >= 0")
    return ratio ** (stages * cluster)


def clusters_stay_exact(ratio: int, stages: int, clusters: int = 8) -> bool:
    """True iff every cluster boundary still admits an exact ladder of the
    same stage count.

    This is what decides the indexing question. Repeating a ladder whose
    top is `r ** stages` gives boundaries `r ** (stages * m)`, which is
    `(r ** m) ** stages` -- a perfect `stages`-th power for every `m`, so
    the repetition never loses exactness.

    Repeating one whose top is `r ** (stages - 1)` does not: for ratio 8
    and nine stages the boundaries are `2 ** (24 m)`, and 24m is divisible
    by 9 only for m = 3, 6, ... So the cluster plan only works if "nine"
    counts the *steps*, with the ladder running `r**0 ... r**9`."""
    return all(
        admits_exact_ladder(cluster_bound(ratio, stages, m), stages)
        for m in range(1, clusters + 1)
    )


def ladder_contains(ratio: int, stages: int, value: int) -> bool:
    """True iff the value is one of the ladder's rungs.

    A ratio-8 ladder holds only `2 ** (3k)`, so a 6-bit pattern (64 = 8²)
    sits on it and an 8-bit pattern (256 = 2⁸) does not. A ratio-2 ladder
    holds both."""
    if ratio < 2:
        raise ValueError("ratio must be at least 2")
    if stages < 0:
        raise ValueError("stages must be >= 0")
    return any(ratio ** k == value for k in range(stages + 1))


def dual_ladder(exponent: int, stages: int) -> list[int]:
    """The other ladder: `k ** exponent` for k = 0..stages.

    Expansion and compression are not one map. `x ** n` reaches the unit
    when the *exponent* is zero -- `x**0 = 1` for every x -- while
    `n ** x` reaches it when the *base* is zero, since `0**0 = 1`. So the
    unit sits on a different axis in each, and one map alone reaches it
    along one axis only. That asymmetry is why both are needed, and it is
    the same structure `duplex_inversion` already carries.

    Practically, the two ladders cover different rungs. With ratio 8 the
    first holds only `2**(3k)`, so a 6-bit pattern (64 = 8²) is a rung and
    an 8-bit pattern (256) is not -- but 256 = 2⁸ *is* a rung of this one.
    Together they supply both."""
    if exponent < 1:
        raise ValueError("exponent must be at least 1")
    if stages < 0:
        raise ValueError("stages must be >= 0")
    return [k ** exponent for k in range(stages + 1)]


def dual_ladders_cover(ratio: int, stages: int, value: int) -> bool:
    """True iff the value is a rung of `ratio**k` or of `k**ratio`."""
    return ladder_contains(ratio, stages, value) or value in dual_ladder(ratio, stages)


def shared_rung_condition(ratio: int) -> tuple[int, int] | None:
    """For `ratio = p**a`, the pair (ratio, a) such that `ratio**j` is also
    a rung of `k**ratio` exactly when `ratio` divides `a*j`.

    Derivation: `r**j = k**r` means `k = r**(j/r) = p**(a*j/r)`, which is
    an integer exactly when `r | a*j`. Returns None when the ratio is not
    a prime power, where this does not apply.

    Recorded because it took three attempts. The first guess was that the
    shared rungs were the `x**n = n**x` coincidences from
    `duplex_inversion` -- wrong; for ratio 2 the shared rungs are
    `1, 4, 16, 64`, a whole family, not the single exceptional pair. The
    second was that they are the powers of `r**r` -- right for 2, 3, 8
    and 9 but wrong for 4, where `16` and `4096` are shared and are not
    powers of `256`. Only the third is derived rather than pattern-matched,
    and it holds for every prime power tested up to 27."""
    remaining, prime = ratio, 2
    while prime * prime <= remaining:
        if remaining % prime == 0:
            exponent = 0
            value = remaining
            while value % prime == 0:
                exponent += 1
                value //= prime
            return (ratio, exponent) if value == 1 else None
        prime += 1
    return (ratio, 1)


def shared_rungs(ratio: int, stages: int) -> list[int]:
    """The values that are rungs of both ladders, by the condition above."""
    factored = shared_rung_condition(ratio)
    if factored is None:
        # Not a prime power: fall back to intersecting the two ladders.
        return sorted(
            {ratio ** k for k in range(stages + 1)} & set(dual_ladder(ratio, stages))
        )
    _, a = factored
    dual = set(dual_ladder(ratio, stages))
    return sorted(
        ratio ** j for j in range(stages + 1)
        if (a * j) % ratio == 0 and ratio ** j in dual
    )
