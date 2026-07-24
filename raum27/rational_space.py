"""The multiplicative group of strictly positive rationals, Q+.

Source notes define a state space Q+ = {a/b | a, b in N}, excluding zero,
with X = 1 as the multiplicative identity, and a mapping I(x) = 1/x.

I is a genuine involution on Q+: I(I(x)) = x, I(1) = 1, and it swaps the
two sides of the fixed point (x > 1 iff I(x) < 1). Those three properties
are proven here as ordinary facts about reciprocals, not asserted as new
physics.
"""

from fractions import Fraction


def involution(x: Fraction) -> Fraction:
    """Return I(x) = 1/x. Raises ZeroDivisionError for x == 0, which is
    excluded from Q+ by definition."""
    if x == 0:
        raise ValueError("0 is not an element of Q+")
    return Fraction(1) / Fraction(x)


def is_fixed_point(x: Fraction) -> bool:
    """True iff x is the unique fixed point of the involution, i.e. x == 1."""
    return involution(x) == x
