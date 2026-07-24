"""Rational Taylor approximation of sine.

sin(x) ~= x - x^3/3! + x^5/5! - x^7/7! + x^9/9! - ...

Computed with fractions.Fraction so the result is an exact rational
number rather than a float. This is a standard truncated Taylor series;
using exact rational arithmetic does not change its convergence
properties (it still only approximates sin(x) well for |x| that is not
too large, and error grows with the distance from 0 and shrinks with more
terms).
"""

from fractions import Fraction
from math import factorial


def sin_taylor(x: Fraction, terms: int = 5) -> Fraction:
    """Truncated Taylor series for sin(x) around 0, using `terms` odd-power
    terms (terms=5 reproduces x - x^3/6 + x^5/120 - x^7/5040 + x^9/362880).
    """
    if terms < 1:
        raise ValueError("terms must be >= 1")
    x = Fraction(x)
    result = Fraction(0)
    power = x
    x_squared = x * x
    for n in range(terms):
        exponent = 2 * n + 1
        term = power / factorial(exponent)
        result += term if n % 2 == 0 else -term
        power *= x_squared
    return result
