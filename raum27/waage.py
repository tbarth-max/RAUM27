"""Die Waage: a balance beam reads a ratio off a position.

Thomas's framing: don't chase an exact 0 or 100%, which the logarithmic
axes never reach anyway -- find the centre, the point where two weights
balance, and read the ratio off the beam. That intuition has an exact
mathematical form, and it turns out to be the same structure already
sitting in kern_modul_v2's reciprocal redundancy measure.

**The lever law.** Two weights w1, w2 on a beam of length L balance when
w1*d1 == w2*d2 with d1 + d2 == L. Solving gives

    d1 = L * w2 / (w1 + w2)

so the fulcrum's POSITION is the ratio -- exactly, as a rational number,
no measurement of the weights themselves required. Reading it back out
(ratio_from_balance_point) is exact too, so the beam is a lossless
ratio encoder, not an approximation.

**Why the logarithmic axis matters.** On a log scale the midpoint
between a and b sits at (log a + log b)/2, which is the GEOMETRIC mean
sqrt(a*b), not the arithmetic one. For a reciprocal pair -- b = 1/a --
that product is exactly 1, so every such pair balances at exactly 1,
whatever a is. That is the same fixed point rational_space.involution
has, and the same "1 means equilibrium, not 0" convention the project
uses throughout.

Since sqrt(a*b) is irrational in general, this module exposes the
SQUARED geometric mean (a*b), which stays an exact Fraction -- the same
convention cube_symmetry.py uses for face_diagonal_squared, and for the
same reason.

**The connection that makes this more than a restatement**:
kern_modul_v2.redundancy_deviation(x) is already symmetric under
x -> 1/x. In beam terms that symmetry IS the balance: deviating by a
factor of 2 to one side costs exactly what deviating by a factor of 2 to
the other side costs. Verified across modules in
tests/test_waage.py rather than asserted here.
"""

from __future__ import annotations

from fractions import Fraction
from math import gcd


def balance_point(w1: Fraction, w2: Fraction, beam_length: Fraction = Fraction(1)) -> Fraction:
    """Distance from the w1 end to the fulcrum, for a beam that balances.
    Exact: d1 = L * w2 / (w1 + w2)."""
    if w1 + w2 == 0:
        raise ValueError("weights must not sum to zero")
    return beam_length * Fraction(w2) / (Fraction(w1) + Fraction(w2))


def lever_law_holds(w1: Fraction, w2: Fraction, beam_length: Fraction = Fraction(1)) -> bool:
    """True iff w1*d1 == w2*d2 exactly at the computed balance point."""
    d1 = balance_point(w1, w2, beam_length)
    d2 = beam_length - d1
    return Fraction(w1) * d1 == Fraction(w2) * d2


def ratio_from_balance_point(d1: Fraction, beam_length: Fraction = Fraction(1)) -> Fraction:
    """Read w1/w2 back out of the fulcrum position: (L - d1) / d1.
    Exact inverse of balance_point -- the beam loses nothing."""
    if d1 == 0:
        raise ValueError("fulcrum at the w1 end encodes no finite ratio")
    return (beam_length - Fraction(d1)) / Fraction(d1)


def geometric_mean_squared(a: Fraction, b: Fraction) -> Fraction:
    """(sqrt(a*b))**2 = a*b. Squared, so it stays an exact Fraction --
    the geometric mean itself is irrational for most inputs."""
    return Fraction(a) * Fraction(b)


def balances_at_one(a: Fraction, b: Fraction) -> bool:
    """True iff a and b balance at exactly 1 on a logarithmic axis,
    i.e. their geometric mean is 1, i.e. a*b == 1 -- exactly the
    reciprocal-pair condition."""
    return geometric_mean_squared(a, b) == 1


def is_lossless_encoding(w1: int, w2: int) -> bool:
    """True iff the beam encodes this weight pair without loss, i.e. iff
    gcd(w1, w2) == 1.

    The beam only ever sees the RATIO, never the weights: (2,4) and (1,2)
    both put the fulcrum at 2/3, so the position cannot tell them apart.
    When the weights are coprime there is nothing to cancel -- the
    balance point w2/(w1+w2) is already in lowest terms, since
    gcd(w2, w1+w2) == gcd(w2, w1) == 1 -- so the pair is recoverable
    from the position alone.

    NEGATIVE RESULT, kept rather than dropped (checked in
    tests/test_waage.py): the load-bearing property is coprimality, NOT
    primality. Prime weights work because distinct primes are always
    coprime, not because they are prime -- (16, 81) are both composite
    and work exactly as well. And balance points of prime pairs land on
    nothing special: the denominator is always w1+w2, and sums of two
    primes are usually composite (3+5=8, 5+7=12, 11+13=24). There is no
    "prime space" structure here beyond ordinary coprimality.
    """
    return gcd(int(w1), int(w2)) == 1


def shares(weights: list[Fraction]) -> list[Fraction]:
    """Each weight's share of the whole, w_i / sum(w). Exact, and the
    shares sum to exactly 1.

    This is the element's own ratio to the total -- nobody assigns it,
    it follows from what the element is. A weight of 0 gets a share of
    exactly 0: it neither pulls nor is pulled on."""
    total = sum(Fraction(w) for w in weights)
    if total == 0:
        raise ValueError("no system: all weights are zero, so there is no common point")
    return [Fraction(w) / total for w in weights]


def center_of_mass(weights: list[Fraction], positions: list[Fraction]) -> Fraction:
    """The common point: sum(w_i * x_i) / sum(w_i), exact.

    For two weights at positions 0 and 1 this reduces exactly to
    balance_point(w1, w2) -- cross-checked in tests/test_waage.py.

    A zero weight contributes w_i * x_i = 0 whatever its position, so it
    can sit arbitrarily far out without moving the common point by any
    amount at all. That is "far outside" in the exact sense: outside the
    system's determination entirely."""
    if len(weights) != len(positions):
        raise ValueError("weights and positions must have the same length")
    total = sum(Fraction(w) for w in weights)
    if total == 0:
        raise ValueError("no system: all weights are zero, so there is no common point")
    return sum(Fraction(w) * Fraction(x) for w, x in zip(weights, positions)) / total


def residual_torque(
    weights: list[Fraction], positions: list[Fraction], pivot: Fraction
) -> Fraction:
    """sum(w_i * (x_i - pivot)), exact. Zero exactly at the centre of
    mass, for any number of weights and any arrangement of them."""
    return sum(Fraction(w) * (Fraction(x) - Fraction(pivot)) for w, x in zip(weights, positions))
