"""Der Optionsraum: wanting everything is the centre, wanting one thing is the edge.

This is the *inversion* of `waage.py`, and it lives in a different space.

**Two independent coordinates, not one.** A wish vector `w` over `N`
options carries two separate pieces of information:

1. its **total** `Σw_i` -- how much is wanted at all. This is the
   `waage.py` coordinate. Total 0 means a share of exactly 0: no pull on
   the common point from any distance.
2. its **direction** `p = w / Σw_i` -- *what* is wanted, as a
   distribution over the options. That is the coordinate of this module.
   It lives on the probability simplex, `p_i ≥ 0`, `Σp_i = 1`.

These cannot be traded against each other, so "far out" means two
different things in the two modules and neither statement overrides the
other. Note where they meet: the direction is **undefined** exactly when
the total is 0 -- which is precisely where `waage.shares` already
raises. Wanting nothing is not a position in the option space at all;
it is the one place the option-space coordinate fails to exist.

**On the simplex the extremes invert.** Wanting *all* options equally is
`p = (1/N, ..., 1/N)`, the centroid -- and in centred coordinates
`q = p - c` it is exactly the origin, `q = 0`. Wanting exactly *one*
option is a vertex `e_i`, maximally far out. So in this space:

    everything  ->  the zero point
    one thing   ->  the outer boundary

the opposite way round from the beam, and both are exact.

**The identity that ties it together.** For every `p` on the simplex

    |p - c|²  =  Σp_i²  -  1/N

exactly (because `p·c = 1/N` for every `p`, and `|c|² = 1/N`). So "how
far out you are" and "how concentrated your wishes are" are literally
the same number up to the constant `1/N`. That turns the geometry into
an exact algebraic statement, and the two extremes follow with full
proofs rather than pictures:

- `Σp² ≤ (max p_i)·Σp_i = max p_i ≤ 1`, with equality iff some
  `p_i = 1`. So the maximum is attained **exactly** at the vertices, and
  `|e_i - c|² = 1 - 1/N = (N-1)/N` -- an exact rational, strictly below
  1 for every finite `N`, reaching 1 only in the limit.
- `(Σp_i)² ≤ N·Σp_i²` (Cauchy-Schwarz), so `Σp² ≥ 1/N` with equality
  iff all `p_i` are equal. The minimum is attained **only** at the
  centroid, where the distance is exactly 0.

**Where the framing needed correcting.** The largest gap in this space
is *not* between "everything" and "one thing". It is between two
*different* single wishes:

    |p - q|² = Σp² + Σq² - 2(p·q) ≤ 1 + 1 - 0 = 2

with equality iff both are vertices and `p·q = 0`, i.e. two distinct
vertices. So the diameter is exactly 2, while centroid-to-vertex is
`(N-1)/N < 1` -- less than half of it, always. Two single-minded
positions wanting different things are more than twice as far apart as
the all-wanting centre is from either.

**What the centre actually is, then.** Not the far end of the maximal
delta, but the unique minimiser of the worst case:

    max_i |p - e_i|² = Σp² + 1 - 2·min_i p_i
                     ≥ 1/N + 1 - 2/N = (N-1)/N

using `Σp² ≥ 1/N` and `min_i p_i ≤ 1/N`, and both bounds are tight only
at the centroid. So the all-wanting point is exactly the position whose
distance to the furthest single wish is as small as it can be, and it is
equidistant from all of them. That is a sharper and truer statement than
"maximal delta", and it is the one that is provable.

Everything here is exact over `Fraction`; squared distances are exposed
because the roots are irrational in general -- the same convention as
`cube_symmetry.face_diagonal_squared` and `waage.geometric_mean_squared`.
"""

from __future__ import annotations

from fractions import Fraction


def uniform_wish(n: int) -> list[Fraction]:
    """Wanting all n options equally: the centroid (1/n, ..., 1/n).

    In centred coordinates this is exactly the origin."""
    if n < 1:
        raise ValueError("an option space needs at least one option")
    return [Fraction(1, n)] * n


def single_wish(n: int, i: int) -> list[Fraction]:
    """Wanting exactly one of n options: the vertex e_i."""
    if n < 1:
        raise ValueError("an option space needs at least one option")
    if not 0 <= i < n:
        raise ValueError("option index out of range")
    return [Fraction(1) if j == i else Fraction(0) for j in range(n)]


def is_on_simplex(p: list[Fraction]) -> bool:
    """True iff p is a wish direction: non-negative and summing to 1."""
    return all(Fraction(x) >= 0 for x in p) and sum(Fraction(x) for x in p) == 1


def concentration(p: list[Fraction]) -> Fraction:
    """Σp_i², exact. Ranges over exactly [1/n, 1] on the simplex: 1/n
    only at the centroid (all options wanted equally), 1 only at a
    vertex (one option wanted)."""
    return sum(Fraction(x) * Fraction(x) for x in p)


def participation_number(p: list[Fraction]) -> Fraction:
    """1/Σp_i² -- how many options are *effectively* wanted.

    Exactly n for the uniform wish and exactly 1 for a single wish, so
    it reads the count back off the distribution. Zero wish vectors have
    no direction, so this raises rather than returning something."""
    c = concentration(p)
    if c == 0:
        raise ValueError("no direction: the wish vector is zero")
    return 1 / c


def squared_distance(p: list[Fraction], q: list[Fraction]) -> Fraction:
    """Σ(p_i - q_i)², exact. Squared because the root is irrational in
    general."""
    if len(p) != len(q):
        raise ValueError("wish vectors must have the same length")
    return sum((Fraction(a) - Fraction(b)) ** 2 for a, b in zip(p, q))


def squared_distance_from_centre(p: list[Fraction]) -> Fraction:
    """|p - c|² where c is the uniform wish, computed directly.

    Equals concentration(p) - 1/n exactly for every p on the simplex --
    the identity is cross-checked in tests/test_optionsraum.py rather
    than relied on here."""
    if not p:
        raise ValueError("an option space needs at least one option")
    return squared_distance(p, uniform_wish(len(p)))


def worst_squared_distance_to_a_single_wish(p: list[Fraction]) -> Fraction:
    """max_i |p - e_i|², exact: how far p is from the single wish it is
    furthest from.

    Minimised uniquely at the uniform wish, where it equals (n-1)/n and
    is the same for every option. That -- not "maximal delta" -- is what
    singles the all-wanting centre out."""
    if not p:
        raise ValueError("an option space needs at least one option")
    n = len(p)
    return max(squared_distance(p, single_wish(n, i)) for i in range(n))


def simplex_diameter_squared() -> Fraction:
    """The largest squared distance between any two wish directions:
    exactly 2, independent of n, attained only between two *distinct*
    single wishes.

    Does not depend on n because |p - q|² ≤ Σp² + Σq² ≤ 2 with equality
    only at two orthogonal vertices -- adding options adds no reach."""
    return Fraction(2)
