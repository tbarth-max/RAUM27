"""Compare patterns first, compute last: roots as fractional exponents, ratios by denominator.

* **Every root is a power with a fractional exponent.** A number built by
  multiplying, dividing and taking roots is a product of primes with
  rational exponents, sqrt 2 = 2^(1/2), cbrt 3 = 3^(1/3), and that form is
  unique. So equality is exact (sqrt 2 * sqrt 8 = 2^(1/2 + 3/2) = 4) and so
  is order: raise both sides to the lcm N of all exponent denominators
  and compare fractions -- sqrt 2 < cbrt 3 because 2^3 = 8 < 9 = 3^2. No
  decimal is ever evaluated. The limit: sums of different roots
  (sqrt 2 + sqrt 3) have no such form; they stay as an open expression.

* **Every ratio is kept as Z1 : Z2.** Put on the common denominator, the
  numerators can be compared directly; grouped by the reduced
  denominator, each ratio sits on its circle. That gives two orderings,
  not one: *which circle* (denominator, the resolution) and *where on
  it* (numerator, the position) -- the same pair as in ``verhaeltnis``.

* **Units out, then time out.** A length divided by a reference length
  is a pure ratio. Inside, time is kept as path s = v t; only the output
  turns it back, t = s / v_out.
"""

from fractions import Fraction
from math import lcm


def _exact(*values):
    for v in values:
        if isinstance(v, float):
            raise TypeError("exact module: use int or Fraction, not float")
    return [Fraction(v) for v in values]


def _factor(n):
    out, p = {}, 2
    while p * p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


class Power:
    """A positive number as {prime: rational exponent}."""

    __slots__ = ("exponents",)

    def __init__(self, exponents=None):
        self.exponents = {p: Fraction(e) for p, e in (exponents or {}).items() if e != 0}

    @classmethod
    def of(cls, value):
        (value,) = _exact(value)
        if value <= 0:
            raise ValueError("positive numbers only")
        exps = {p: Fraction(e) for p, e in _factor(value.numerator).items()}
        for p, e in _factor(value.denominator).items():
            exps[p] = exps.get(p, 0) - e
        return cls(exps)

    def __mul__(self, other):
        e = dict(self.exponents)
        for p, x in other.exponents.items():
            e[p] = e.get(p, 0) + x
        return Power(e)

    def __truediv__(self, other):
        return self * other ** -1

    def __pow__(self, k):
        (k,) = _exact(k)
        return Power({p: e * k for p, e in self.exponents.items()})

    def root(self, n):
        return self ** Fraction(1, n)

    def __eq__(self, other):
        return isinstance(other, Power) and self.exponents == other.exponents

    def __hash__(self):
        return hash(frozenset(self.exponents.items()))

    def common_power(self):
        """Smallest N with self^N rational."""
        return lcm(1, *(e.denominator for e in self.exponents.values()))

    def rational(self):
        """The exact value if there is no root left, else None."""
        if self.common_power() != 1:
            return None
        v = Fraction(1)
        for p, e in self.exponents.items():
            v *= Fraction(p) ** int(e)
        return v

    def __lt__(self, other):
        n = lcm(self.common_power(), other.common_power())
        return (self ** n).rational() < (other ** n).rational()

    def __repr__(self):
        if not self.exponents:
            return "1"
        return "·".join(f"{p}^({e})" if e.denominator != 1 else f"{p}^{e}" for p, e in sorted(self.exponents.items()))


def on_common_denominator(pairs):
    """Ratios (z1, z2), not reduced, written over one denominator: (N, [numerators])."""
    for z1, z2 in pairs:
        if z2 == 0:
            raise ZeroDivisionError("a ratio needs a non-zero second term")
    n = lcm(*(abs(z2) for _, z2 in pairs))
    return n, [z1 * (n // abs(z2)) * (1 if z2 > 0 else -1) for z1, z2 in pairs]


def by_denominator(pairs):
    """Group ratios by their circle (reduced denominator), each group by position."""
    groups = {}
    for z1, z2 in pairs:
        f = Fraction(z1, z2)
        groups.setdefault(f.denominator, []).append(((z1, z2), f))
    return {q: [pair for pair, _ in sorted(items, key=lambda t: t[1])] for q, items in sorted(groups.items())}


def unit_free(value, reference):
    """A quantity over its reference quantity: a pure ratio."""
    value, reference = _exact(value, reference)
    if reference == 0:
        raise ZeroDivisionError("reference must not be zero")
    return value / reference


def path_from_time(t, v):
    t, v = _exact(t, v)
    return v * t


def time_from_path(s, v_out):
    s, v_out = _exact(s, v_out)
    if v_out <= 0:
        raise ValueError("output speed must be positive")
    return s / v_out
