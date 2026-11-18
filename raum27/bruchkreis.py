"""Fraction circles: the cross, the circle from one fraction, the tree, and when to stop.

* **Four fields around one centre.** Laid out q1 q2 / q3 q4, the closed
  ring q1/q2 * q2/q3 * q3/q4 * q4/q1 is 1 for *any* four numbers -- it
  says nothing about them. What does: the cross ratio (q1 q4) / (q2 q3),
  unchanged when any row or column is rescaled. For four consecutive
  numbers a .. a+3 the diagonal sums are equal and the diagonal products
  always differ by exactly 2 (2 3 4 5: 10 against 12, ratio 5/6).
* **Read across the centre with a sign.** u and the opposite -w give a
  diagonal of length u + w whose midpoint lies at (u - w)/2: 2 | -5 and
  3 | -4 both have length 7, midpoints -3/2 and -1/2 -- that pair is the
  delta. With perpendicular diagonals the area is d1 d2 / 2.
* **One fraction, every function.** t gives the exact circle point
  ((1 - t^2)/(1 + t^2), 2t/(1 + t^2)), and sin, 1/sin, sin^2, sinh, cosh
  as fractions of t; circle and hyperbola differ only in the sign of the
  denominator. Raum direction n (|n|^2 = 1) and T part t together give
  the four-velocity (cosh, sinh n) with cosh^2 - sinh^2 |n|^2 = 1.
* **Which fractions touch.** a/b and c/d are neighbours when
  ad - bc = +-1; then their Ford circles (radius 1/(2 q^2)) touch. Every
  new fraction is the mediant of two neighbours; the Stern-Brocot tree
  doubles its strokes per level (1, 2, 4, 8) and gives each fraction an
  L/R address.
* **When to stop.** The continued fraction ends by itself when the rest
  is 0 (a fraction: 100 % reached), otherwise stop at the tolerance:
  each convergent p/q lies closer than every fraction with a smaller
  denominator.
* **Two lattices and a grating.** Parallel lattices d1, d2 give a moire
  period d1 d2 / |d1 - d2|. A grating moves order m to
  sin_out = sin_in + m lambda / d: in sines the pattern is a rigid grid,
  the viewing angle only shifts it.
"""

from fractions import Fraction
from math import gcd


def _exact(*values):
    for v in values:
        if isinstance(v, float):
            raise TypeError("exact module: use int or Fraction, not float")
    return [Fraction(v) for v in values]


# --- four fields around one centre --------------------------------------------------


def ring_product(values):
    """q1/q2 * q2/q3 * ... * qn/q1 -- always 1, whatever the values."""
    v = _exact(*values)
    if any(x == 0 for x in v):
        raise ZeroDivisionError("a ratio needs non-zero terms")
    out = Fraction(1)
    for a, b in zip(v, v[1:] + v[:1]):
        out *= a / b
    return out


def cross_ratio(q1, q2, q3, q4):
    """(q1 q4) / (q2 q3) for the layout q1 q2 / q3 q4: unchanged by row and column scaling."""
    q1, q2, q3, q4 = _exact(q1, q2, q3, q4)
    if q2 * q3 == 0:
        raise ZeroDivisionError("the second diagonal must not be zero")
    return q1 * q4 / (q2 * q3)


def consecutive_delta(a):
    """(a+1)(a+2) - a(a+3): always 2."""
    (a,) = _exact(a)
    return (a + 1) * (a + 2) - a * (a + 3)


def across(u, w):
    """u and the opposite value read as -w: (diagonal length u + w, midpoint (u - w)/2)."""
    u, w = _exact(u, w)
    return u + w, (u - w) / 2


def kite_area(d1, d2):
    """Area of a quadrilateral with perpendicular diagonals: d1 d2 / 2, wherever they cross."""
    d1, d2 = _exact(d1, d2)
    return d1 * d2 / 2


# --- one fraction, every function -----------------------------------------------------


def circle_point(t):
    """The exact point on the unit circle belonging to the fraction t."""
    (t,) = _exact(t)
    n = 1 + t * t
    return (1 - t * t) / n, 2 * t / n


def sin_of(t):
    (t,) = _exact(t)
    return 2 * t / (1 + t * t)


def csc_of(t):
    """1 / sin -- not at t = 0, where sin is 0 (radius 0 is never reached)."""
    s = sin_of(t)
    if s == 0:
        raise ZeroDivisionError("sin is 0 here")
    return 1 / s


def sin2_of(t):
    return sin_of(t) ** 2


def _hyperbola(t):
    (t,) = _exact(t)
    if not -1 < t < 1:
        raise ValueError("|t| < 1: t = 1 is the light limit")
    return t, 1 - t * t


def sinh_of(t):
    t, n = _hyperbola(t)
    return 2 * t / n


def cosh_of(t):
    t, n = _hyperbola(t)
    return (1 + t * t) / n


def four_velocity(t, direction):
    """(cosh, sinh * n) for the T part t and a space direction n with |n|^2 = 1."""
    n = _exact(*direction)
    if sum(c * c for c in n) != 1:
        raise ValueError("the direction must have |n|^2 = 1")
    s = sinh_of(t)
    return (cosh_of(t),) + tuple(s * c for c in n)


def interval(u):
    """u0^2 - u1^2 - u2^2 - u3^2: the common 1."""
    u = _exact(*u)
    return u[0] * u[0] - sum(c * c for c in u[1:])


# --- which fractions touch -----------------------------------------------------------


def neighbours(x, y):
    """a/b and c/d touch when ad - bc = +-1."""
    x, y = _exact(x, y)
    return abs(x.numerator * y.denominator - x.denominator * y.numerator) == 1


def mediant(x, y):
    """(a + c) / (b + d) -- the fraction born between two neighbours."""
    x, y = _exact(x, y)
    return Fraction(x.numerator + y.numerator, x.denominator + y.denominator)


def ford_circle(x):
    """(centre x, centre height, radius) of the Ford circle on the fraction x: radius 1/(2 q^2)."""
    (x,) = _exact(x)
    r = Fraction(1, 2 * x.denominator ** 2)
    return x, r, r


def ford_touch(x, y):
    """True when the two Ford circles touch (squared centre distance = (r1 + r2)^2)."""
    (x1, h1, r1), (x2, h2, r2) = ford_circle(x), ford_circle(y)
    return (x1 - x2) ** 2 + (h1 - h2) ** 2 == (r1 + r2) ** 2


def new_points(q):
    """How many fractions in (0, 1) live on the denominator circle q: Euler's phi(q)."""
    if q < 2:
        raise ValueError("q >= 2")
    return sum(1 for p in range(1, q) if gcd(p, q) == 1)


def stern_brocot_level(k):
    """The fractions in (0, 1) born at level k (k >= 1): 2^(k-1) of them."""
    if k < 1:
        raise ValueError("k >= 1")
    row = [Fraction(0), Fraction(1)]
    born = []
    for _ in range(k):
        born = [mediant(a, b) for a, b in zip(row, row[1:])]
        merged = [row[0]]
        for m, b in zip(born, row[1:]):
            merged += [m, b]
        row = merged
    return born


def stern_brocot_path(x):
    """The L/R address of a positive fraction, starting at 1/1."""
    (x,) = _exact(x)
    if x <= 0:
        raise ValueError("positive fractions only")
    lo, hi = (0, 1), (1, 0)
    path = ""
    while True:
        m = Fraction(lo[0] + hi[0], lo[1] + hi[1])
        if m == x:
            return path
        if x < m:
            path, hi = path + "L", (m.numerator, m.denominator)
        else:
            path, lo = path + "R", (m.numerator, m.denominator)


# --- when to stop ---------------------------------------------------------------------


def continued_fraction(x, tolerance=0):
    """Convergents of x until the rest is 0 or the error is below the tolerance."""
    (x,) = _exact(x)
    (tolerance,) = _exact(tolerance)
    h0, h1, k0, k1 = 0, 1, 1, 0
    rest, out = x, []
    while True:
        a = rest.numerator // rest.denominator
        h0, h1 = h1, a * h1 + h0
        k0, k1 = k1, a * k1 + k0
        out.append(Fraction(h1, k1))
        if rest == a or abs(x - out[-1]) < tolerance:
            return out
        rest = 1 / (rest - a)


# --- two lattices and a grating ---------------------------------------------------------


def moire_period(d1, d2):
    """Superlattice of two parallel lattices: d1 d2 / |d1 - d2|."""
    d1, d2 = _exact(d1, d2)
    if d1 == d2:
        raise ValueError("equal lattices have no beat")
    return d1 * d2 / abs(d1 - d2)


def order_sine(sin_in, m, wavelength, pitch):
    """Sine of the outgoing direction of order m: sin_in + m lambda / d (|sin| <= 1)."""
    sin_in, wavelength, pitch = _exact(sin_in, wavelength, pitch)
    s = sin_in + m * wavelength / pitch
    if abs(s) > 1:
        raise ValueError("this order does not leave the grating")
    return s
