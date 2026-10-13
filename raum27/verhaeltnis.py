"""Show proportions, not decimals: a display layer for any module.

A module may compute however it likes -- with decimals if its logic has
no fraction bar. What is shown, though, should keep the proportion
visible: ``(1:3)`` and ``(1:9)`` side by side show a factor of three at a
glance, ``0.3333`` and ``0.1111`` hide it.

The layer finds the simplest ratio that a number really is, using the
continued-fraction rule behind ``Fraction.limit_denominator``: among all
fractions with a bounded denominator, the closest one. A ratio is shown
only if it matches within the given tolerance; otherwise the number is
shown as it is, so nothing is dressed up as a proportion that is not one
-- sqrt 2 - 1 stays 0.4142..., it is not 2:5.
"""

from fractions import Fraction


def as_ratio(x, max_denominator=1000, tolerance=1e-9):
    """The simplest fraction equal to ``x`` within ``tolerance``, or ``None``."""
    if isinstance(x, Fraction):
        return x
    if isinstance(x, int) and not isinstance(x, bool):
        return Fraction(x)
    candidate = Fraction(x).limit_denominator(max_denominator)
    return candidate if abs(float(candidate) - x) <= tolerance * max(1.0, abs(x)) else None


def show(x, max_denominator=1000, tolerance=1e-9):
    """``(p:q)`` when ``x`` is a simple ratio, otherwise the number itself."""
    r = as_ratio(x, max_denominator, tolerance)
    if r is None:
        return repr(x)
    return f"({r.numerator}:{r.denominator})"


def proportion(a, b, max_denominator=1000, tolerance=1e-9):
    """The ratio a : b in lowest terms as ``(p:q)``, or ``None`` if it is not simple."""
    ra, rb = as_ratio(a, max_denominator, tolerance), as_ratio(b, max_denominator, tolerance)
    if ra is not None and rb is not None and rb != 0:
        r = ra / rb
    else:
        if b == 0:
            raise ZeroDivisionError("no proportion to zero")
        r = as_ratio(a / b, max_denominator, tolerance)
        if r is None:
            return None
    return f"({r.numerator}:{r.denominator})"


def annotate(values, max_denominator=1000, tolerance=1e-9):
    """Each value with its own ratio and its proportion to the first value."""
    first = values[0]
    return [(show(v, max_denominator, tolerance), proportion(v, first, max_denominator, tolerance))
            for v in values]
