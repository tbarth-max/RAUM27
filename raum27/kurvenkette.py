"""The four-part sine chain, phases of the 6- and 8-systems, chain and dome, ball and donut.

Kept from conversation so nothing is lost; every statement has a test.

**The four curves**, with u = 16 x / (9 lambda):

- ``lambda sin u``: starts with slope **16/9 for every lambda**; period
  9 pi lambda / 8. Its arch midpoints (peaks) all lie on one line through
  the origin, Y = 32 x / (9 pi), at 48.5 degrees -- 3.5 degrees steeper
  than the diagonal; the diagonal Y = x crosses each arch just past its
  peak. The peaks would lie on 45 degrees only with pi/2 in place of 16/9.
- ``lambda sin^2 u``: flat at the origin, a parabola 256/81 * x^2 / lambda.
- ``lambda sinh u``: the same starting slope 16/9, then exponential -- the
  hyperbola side (sin belongs to cos^2 + sin^2 = 1, sinh to
  cosh^2 - sinh^2 = 1).
- ``1 / (lambda sin u)``: the inversion; its product with the first curve
  is exactly 1 everywhere.

For small x > 0 -- below about 9/16, where the inverse 9/(16x) and the
sinh 16x/9 meet -- the order is inverse > sinh > sin > sin^2. The order
"sin > sinh" is false for every x > 0.

**Phases.** Six and eight positions per turn at one speed stand in
frequency 8 : 6 = 4 : 3 and in energy (4/3)^2 = **16/9**; they beat twice
per turn and their joint pattern repeats after lcm(6, 8) = 24 steps. Read
together, the two phases tell apart only 24 of the 48 pairs -- one bit is
shared, since both count even/odd; coprime cycles such as 8 and 9 tell
apart all 72 (``joint_phases``).

**Chain and dome.** A hanging chain y = a cosh(x/a) has arc length
a sinh(x/a) from its lowest point -- the sinh curve above is that length
with a = 9 lambda / 16. Inverted, the chain is the arch with no bending
moment. A thin spherical dome under its own weight is in ring compression
only down to cos(phi) = (sqrt 5 - 1)/2, the golden ratio, about 51.8
degrees from the crown; below it the rings pull (``dome_ring_force``).

**Ball and donut.** A rotation field on a sphere vanishes exactly at the
two poles -- the axis is forced (hairy ball theorem); the indices add to
the Euler characteristic 2. A torus carries a flow with no zero at all
(characteristic 0). A winding line on the torus with rational ratio 3 : 4
closes; with ratio 1 : sqrt 2 it never closes and comes ever nearer to
its start (``closest_return``).
"""

import math

K = 16 / 9


def curve_sin(x, lam):
    return lam * math.sin(K * x / lam)


def curve_sin2(x, lam):
    return lam * math.sin(K * x / lam) ** 2


def curve_sinh(x, lam):
    return lam * math.sinh(K * x / lam)


def curve_inverse(x, lam):
    return 1 / (lam * math.sin(K * x / lam))


def peak(lam):
    """Arch midpoint of ``curve_sin``: (9 pi lambda / 32, lambda)."""
    return 9 * math.pi * lam / 32, lam


PEAK_LINE_SLOPE = 32 / (9 * math.pi)


def diagonal_crossing(lam):
    """x where lambda sin(K x / lambda) = x past the origin (bisection on u)."""
    lo, hi = 1.0, 3.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if math.sin(mid) - mid / K > 0:
            lo = mid
        else:
            hi = mid
    return lo * lam / K


def joint_phases(a, b):
    """Number of distinct (k mod a, k mod b) pairs and the joint period."""
    return len({(k % a, k % b) for k in range(a * b)}), math.lcm(a, b)


def catenary_length(x, a, pieces=20000):
    """Arc length of a cosh(x/a) from 0 to x by summing chords."""
    total, prev = 0.0, (0.0, a)
    for i in range(1, pieces + 1):
        t = x * i / pieces
        point = (t, a * math.cosh(t / a))
        total += math.dist(prev, point)
        prev = point
    return total


GOLDEN_COS = (math.sqrt(5) - 1) / 2


def dome_ring_force(phi):
    """Ring force of a thin spherical dome under self-weight, per unit radius and load."""
    c = math.cos(phi)
    return 1 / (1 + c) - c


def rotation_field(point, axis=(0.0, 0.0, 1.0)):
    """Tangent velocity axis x point of a rigid rotation."""
    (a, b, c), (x, y, z) = axis, point
    return (b * z - c * y, c * x - a * z, a * y - b * x)


def torus_flow(theta, phi):
    """A flow along the tube direction of a torus; never zero."""
    return (-math.sin(theta) * (2 + math.cos(phi)), math.cos(theta) * (2 + math.cos(phi)), 0.0)


def closest_return(ratio, turns):
    """Closest approach of a torus winding to its start within ``turns`` turns."""
    best = math.inf
    for n in range(1, turns + 1):
        frac = (n * ratio) % 1.0
        best = min(best, min(frac, 1 - frac))
    return best
