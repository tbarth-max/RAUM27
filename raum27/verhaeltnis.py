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
from math import gcd, lcm


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


# --- denominator circles: look before computing ---------------------------
#
# A denominator n is a circle with n raster points 0/n .. (n-1)/n; the
# numerator is the position in the beat, n/n = 1 closes the turn. Circle m
# lies entirely on circle n exactly when m divides n, so most points of a
# "round" circle are inherited from smaller ones and only phi(n) are new.
# Reducing a fraction hides which circle it came from: 2/6 sits on circle
# 6 and is the same point as 1/3 on circle 3. These helpers keep that
# information instead of cancelling it away.


def origin(k, n):
    """The smallest circle a point k/n lives on, and its position there."""
    if n < 1:
        raise ValueError("a circle has at least one raster point")
    k %= n
    g = gcd(k, n) if k else n
    return k // g, n // g


def circle_points(n):
    """Every raster point of circle n: (k, n, origin circle, inherited?)."""
    points = []
    for k in range(n):
        _, home = origin(k, n)
        points.append((k, n, home, home != n))
    return points


def new_points(n):
    """How many points circle n adds that no smaller circle has (Euler's phi)."""
    return sum(1 for *_, inherited in circle_points(n) if not inherited)


def contains(m, n):
    """Does circle n carry every point of circle m?"""
    return n % m == 0


def common_circle(*circles):
    """The smallest circle that carries all given circles."""
    return lcm(*circles)


def positions_up_to(limit):
    """Distinct points on all circles 1..limit together."""
    return sum(new_points(n) for n in range(1, limit + 1))


def factors(n):
    """n written as its prime factors, e.g. 12 -> '2·2·3'."""
    if n < 2:
        return str(n)
    parts, p = [], 2
    while p * p <= n:
        while n % p == 0:
            parts.append(str(p))
            n //= p
        p += 1
    if n > 1:
        parts.append(str(n))
    return "·".join(parts)


def show_unreduced(k, n):
    """'2/6 (circle 6) = 1/3 (circle 3)' -- the point with its origin, nothing cancelled away."""
    j, home = origin(k, n)
    here = f"{k}/{n} (circle {n})"
    return here if home == n else f"{here} = {j}/{home} (circle {home})"
