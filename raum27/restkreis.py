"""The rest around 1: normalise, weigh, write it as a fraction, take the fraction apart.

* **A working range instead of an endless lever.** Every positive value is
  m * 9^k with exactly one integer k and 1/2 <= m < 9/2 -- the range of the
  reference, radius 1/2 to scale 9/2. k counts the zoom steps, m stays where
  a balance can be read. Both directions are exact.
* **Weigh with both pans.** With weights 1, 3, 9, 27 on either pan every
  integer up to 40 is weighed exactly once (Bachet): digits -1, 0, +1, the
  balanced ternary. A fraction is weighed the same way at 1/3, 1/9, ...
  after the nearest integer has been taken off; after p places the rest is
  never more than half the smallest weight, 3^-p / 2, on either side.
* **The rest as a fraction, not a decimal.** A measured value is cut where
  its continued fraction falls inside the measuring tolerance: 0.966 at
  1/1000 is 28/29, the rest to 1 is -1/29. Decimals end only for
  denominators made of 2 and 5; 1/29 never does.
* **Which circles the rest comes from.** The reduced denominator splits into
  prime powers. Different primes are circles side by side: the fraction is
  an integer plus one part a / p^e per prime power (3/80 = -1 + 7/16 + 3/5).
  The exponent is how deep that circle is zoomed: 1/9 is a third of a third,
  1/16 four halvings. A prime denominator is one circle and cannot be split.
* **The 2 x 2 cell and the 2 x 2 x 2 cube.** a b / c d is in balance when
  ad - bc = 0; +-1 means neighbouring fractions. For eight values on the
  corners of a cube Cayley's hyperdeterminant plays the same part: it is 0
  for a cube that is one product u_i v_j w_k, and it does not depend on the
  direction the cube is cut into a front and a back face.
"""

from fractions import Fraction

from raum27.bruchkreis import continued_fraction


def _exact(*values):
    for v in values:
        if isinstance(v, float):
            raise TypeError("exact module: use int or Fraction, not float")
    return [Fraction(v) for v in values]


# --- working range and zoom ---------------------------------------------------------------


def normalize(value, base=9, low=Fraction(1, 2)):
    """(k, m) with value = m * base^k and low <= m < low * base."""
    value, low = _exact(value, low)
    if value <= 0:
        raise ValueError("only positive values have a zoom step")
    if not isinstance(base, int) or base < 2:
        raise ValueError("the base is an integer of at least 2")
    k, m = 0, value
    while m >= low * base:
        m /= base
        k += 1
    while m < low:
        m *= base
        k -= 1
    return k, m


def denormalize(k, m, base=9):
    """m * base^k, exact."""
    (m,) = _exact(m)
    return m * Fraction(base) ** k


# --- the balance with two pans ------------------------------------------------------------


def balanced_ternary(n):
    """Digits -1, 0, +1 of the integer n, lowest place first (weights 1, 3, 9, ...)."""
    if not isinstance(n, int):
        raise TypeError("balanced_ternary takes an integer")
    digits = []
    while n:
        r = n % 3
        if r == 2:
            r = -1
        digits.append(r)
        n = (n - r) // 3
    return digits


def from_balanced_ternary(digits):
    """Sum of d * 3^i, lowest place first."""
    return sum(d * 3**i for i, d in enumerate(digits))


def weigh(x, places):
    """x = integer part + sum d_i 3^-i + rest, digits in {-1, 0, 1}, |rest| <= 3^-places / 2."""
    (x,) = _exact(x)
    n = (x + Fraction(1, 2)).numerator // (x + Fraction(1, 2)).denominator
    r, digits = x - n, []
    for _ in range(places):
        r *= 3
        d = (r + Fraction(1, 2)).numerator // (r + Fraction(1, 2)).denominator
        digits.append(d)
        r -= d
    return balanced_ternary(n), digits, r / Fraction(3) ** places


def unweigh(int_digits, frac_digits, rest=0):
    """Back from weigh: exact."""
    (rest,) = _exact(rest)
    frac = sum(Fraction(d, 3 ** (i + 1)) for i, d in enumerate(frac_digits))
    return from_balanced_ternary(int_digits) + frac + rest


# --- the rest as a fraction ------------------------------------------------------------------


def as_fraction(measured, tolerance):
    """The first convergent of the measured value inside the tolerance."""
    return continued_fraction(measured, tolerance)[-1]


def rest_to_one(measured, tolerance):
    """(fraction, fraction - 1): the value and its rest to 1, both exact."""
    f = as_fraction(measured, tolerance)
    return f, f - 1


# --- which circles ---------------------------------------------------------------------------


def circles(x):
    """Prime -> exponent of the reduced denominator: circles side by side, exponent = zoom depth."""
    (x,) = _exact(x)
    q, out, p = x.denominator, {}, 2
    while p * p <= q:
        while q % p == 0:
            out[p] = out.get(p, 0) + 1
            q //= p
        p += 1
    if q > 1:
        out[q] = out.get(q, 0) + 1
    return out


def partial_fractions(x):
    """(integer, [(a, p^e), ...]) with x = integer + sum a / p^e and 0 <= a < p^e."""
    (x,) = _exact(x)
    q = x.denominator
    parts = []
    for p, e in sorted(circles(x).items()):
        pe = p**e
        rest = q // pe
        a = (x.numerator * pow(rest, -1, pe)) % pe
        parts.append((a, pe))
    integer = x - sum(Fraction(a, pe) for a, pe in parts)
    return int(integer), parts


# --- the cell and the cube -------------------------------------------------------------------


def determinant(a, b, c, d):
    """ad - bc for the cell a b / c d: 0 in balance, +-1 for neighbouring fractions."""
    a, b, c, d = _exact(a, b, c, d)
    return a * d - b * c


def _check_cube(cube):
    try:
        shaped = len(cube) == 2 and all(len(row) == 2 and all(len(c) == 2 for c in row) for row in cube)
    except TypeError:
        shaped = False
    if not shaped:
        raise ValueError("a cube is 2 x 2 x 2: cube[i][j][k]")
    return [[_exact(*cube[i][j]) for j in (0, 1)] for i in (0, 1)]


def hyperdeterminant(cube):
    """Cayley's hyperdeterminant of cube[i][j][k]: 0 for a product u_i v_j w_k."""
    a = _check_cube(cube)
    g = lambda i, j, k: a[i][j][k]  # noqa: E731
    return (
        g(0, 0, 0) ** 2 * g(1, 1, 1) ** 2
        + g(0, 0, 1) ** 2 * g(1, 1, 0) ** 2
        + g(0, 1, 0) ** 2 * g(1, 0, 1) ** 2
        + g(1, 0, 0) ** 2 * g(0, 1, 1) ** 2
        - 2 * g(0, 0, 0) * g(0, 0, 1) * g(1, 1, 0) * g(1, 1, 1)
        - 2 * g(0, 0, 0) * g(0, 1, 0) * g(1, 0, 1) * g(1, 1, 1)
        - 2 * g(0, 0, 0) * g(1, 0, 0) * g(0, 1, 1) * g(1, 1, 1)
        - 2 * g(0, 0, 1) * g(0, 1, 0) * g(1, 0, 1) * g(1, 1, 0)
        - 2 * g(0, 0, 1) * g(1, 0, 0) * g(0, 1, 1) * g(1, 1, 0)
        - 2 * g(0, 1, 0) * g(1, 0, 0) * g(0, 1, 1) * g(1, 0, 1)
        + 4 * g(0, 0, 0) * g(0, 1, 1) * g(1, 0, 1) * g(1, 1, 0)
        + 4 * g(0, 0, 1) * g(0, 1, 0) * g(1, 0, 0) * g(1, 1, 1)
    )


def faces(cube, axis):
    """The front and back 2 x 2 face when the cube is cut across axis 0, 1 or 2."""
    a = _check_cube(cube)
    if axis not in (0, 1, 2):
        raise ValueError("axis is 0, 1 or 2")
    out = []
    for s in (0, 1):
        if axis == 0:
            out.append([[a[s][j][k] for k in (0, 1)] for j in (0, 1)])
        elif axis == 1:
            out.append([[a[i][s][k] for k in (0, 1)] for i in (0, 1)])
        else:
            out.append([[a[i][j][s] for j in (0, 1)] for i in (0, 1)])
    return out[0], out[1]


def turned(cube, axis):
    """The same cube with the cutting axis moved to the front: (i, j, k) -> axis first."""
    a = _check_cube(cube)
    if axis not in (0, 1, 2):
        raise ValueError("axis is 0, 1 or 2")
    idx = [(0, 1, 2), (1, 0, 2), (2, 0, 1)][axis]
    out = [[[None] * 2 for _ in (0, 1)] for _ in (0, 1)]
    for i in (0, 1):
        for j in (0, 1):
            for k in (0, 1):
                p = (i, j, k)
                out[p[idx[0]]][p[idx[1]]][p[idx[2]]] = a[i][j][k]
    return out
