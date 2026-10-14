"""Fundamental domain of the 9x9x9 grid around 555, and the checks around it.

Only the first branch is computed, the rest follows from the symmetries --
but only from the symmetries the computation really has. A modulation
applied to one axis keeps exactly the cube symmetries that commute with it:

* the same odd function on all three axes: all 48, 35 base nodes of 729;
* an odd function on x only (``compute_vector`` with sin(16 x)): 16, the
  y/z square (8) times the x sign flip, which survives because the
  modulation is odd -- 75 base nodes;
* a function on x only that is not odd: 8, 135 base nodes.

Also here: Legendre's rule for which d^2 never occur on the lattice, the
27 ideal points (centre, faces, edges, corners at d^2 = 0, 16, 32, 48),
the octahedron/polygon sieve with its two stops, the structure constant
sigma = c / (3 * 10^8), the sum line d0 + d2 = 24 of the three-instance
sandbox, the 2^k digit cycle 1-2-4-8-7-5, and the Stern-Brocot tree.
"""

from fractions import Fraction
from itertools import permutations, product
import math

HALF = 4                                  # coordinates 1..9 around 5 -> -4..4
SIGMA = Fraction(299792458, 300000000)    # real c over the model limit 3 * 10^8
RESERVE = 1 - SIGMA                       # 103771 / 150000000, about 0.069 %
PASSIVE_STOP = Fraction(1, 100)           # 1 %: resolved passively by resonance


def _require_exact(*values):
    for v in values:
        if isinstance(v, float):
            raise TypeError("exact module: use int or Fraction, not float")


# --- symmetry group and orbits --------------------------------------------

def cube_group():
    """The 48 signed permutations as (perm, signs): v -> (s0*v[p0], s1*v[p1], s2*v[p2])."""
    return [(p, s) for p in permutations(range(3)) for s in product((1, -1), repeat=3)]


def act(g, v):
    p, s = g
    return tuple(s[i] * v[p[i]] for i in range(3))


def grid(half=HALF):
    r = range(-half, half + 1)
    return list(product(r, r, r))


def orbit_count(group, half=HALF):
    """Number of base nodes: orbits of the grid under ``group``."""
    seen, count = set(), 0
    for v in grid(half):
        if v not in seen:
            count += 1
            seen.update(act(g, v) for g in group)
    return count


def fundamental_nodes(half=HALF):
    """One representative per orbit under all 48: 0 <= c <= b <= a <= half."""
    return [(a, b, c) for a in range(half + 1) for b in range(a + 1) for c in range(b + 1)]


def x_only(f):
    """Modulation acting on x alone, as in ``compute_vector``."""
    return lambda v: (f(v[0]), v[1], v[2])


def all_axes(f):
    """The same modulation on every axis -- treats the axes alike."""
    return lambda v: (f(v[0]), f(v[1]), f(v[2]))


def symmetries_of(modulation, half=HALF):
    """The cube symmetries g with modulation(g v) == g modulation(v) on the whole grid."""
    points = grid(half)
    return [g for g in cube_group()
            if all(modulation(act(g, v)) == act(g, modulation(v)) for v in points)]


# --- lattice distances ------------------------------------------------------

def never_a_square_sum(n):
    """Legendre: n = 4^a (8b + 7) is never a sum of three squares."""
    if n <= 0:
        return False
    while n % 4 == 0:
        n //= 4
    return n % 8 == 7


def distance_squares(span):
    """All d^2 = dx^2 + dy^2 + dz^2 with |dx|, |dy|, |dz| <= span."""
    r = range(span + 1)
    return {a * a + b * b + c * c for a in r for b in r for c in r}


def ideal_points(step=HALF):
    """The 27 points 5 +- {0, step} around 555 grouped by d^2."""
    shells = {}
    for v in product((-step, 0, step), repeat=3):
        d2 = sum(t * t for t in v)
        shells[d2] = shells.get(d2, 0) + 1
    return shells


def touching_radii_squared():
    """Unit cube around its centre: face, edge and corner sphere, r^2 = 1/4 : 2/4 : 3/4."""
    return tuple(Fraction(k, 4) for k in (1, 2, 3))


def coupled_states(n=9):
    """Two coupled 3D systems against one 6D search: (n^3 + n^3, n^6)."""
    return 2 * n ** 3, n ** 6


# --- sieve: what is left between polygon / octahedron and the round body ---

def polygon_rest(n):
    """Share of the unit circle not covered by the inscribed regular n-gon."""
    return 1 - n / 2 * math.sin(2 * math.pi / n) / math.pi


def _unit(v):
    length = math.sqrt(sum(t * t for t in v))
    return [t / length for t in v]


def octahedron_rest(k):
    """Share of the unit ball outside the octahedron whose faces are split k x k, vertices on the sphere."""
    volume = 0.0
    for sx, sy, sz in product((1, -1), repeat=3):
        a, b, c = (sx, 0, 0), (0, sy, 0), (0, 0, sz)

        def point(i, j):
            return _unit([(a[t] * (k - i - j) + b[t] * i + c[t] * j) / k for t in range(3)])

        for i in range(k):
            for j in range(k - i):
                tris = [(point(i, j), point(i + 1, j), point(i, j + 1))]
                if i + j < k - 1:
                    tris.append((point(i + 1, j), point(i + 1, j + 1), point(i, j + 1)))
                for p, q, r in tris:
                    cross = (q[1] * r[2] - q[2] * r[1], q[2] * r[0] - q[0] * r[2], q[0] * r[1] - q[1] * r[0])
                    volume += abs(sum(p[t] * cross[t] for t in range(3))) / 6
    return 1 - volume / (4 / 3 * math.pi)


def sieve_stop(rest, stop):
    """First step (and its rest) whose rest falls below ``stop``; rest(step) is a function."""
    step = 1
    while True:
        value = rest(step)
        if value < stop:
            return step, value
        step += 1


# --- sum line of the three-instance sandbox --------------------------------

def sum_line(coord):
    """(d0, d2, rest) for digits 1..9: d0 = sum(9 - c), d2 = sum(c - 1), rest to the nearest third.

    d0 + d2 = 24 for every node -- the sum line carries no information of
    its own. The rest is d0 - 3 * round(d0 / 3), i.e. fixed by the digit sum
    mod 3, so it comes from the position on the grid, not from the data.
    """
    if len(coord) != 3 or not all(1 <= c <= 9 for c in coord):
        raise ValueError("three digits 1..9")
    d0 = sum(9 - c for c in coord)
    d2 = sum(c - 1 for c in coord)
    return d0, d2, Fraction(d0 - 3 * round(d0 / 3), 24)


def frequency_rest(rest, low=Fraction(1, 80), high=Fraction(15, 80)):
    """The sandbox's frequency rest for an abteil rest: rest * (low - high), +-7/960."""
    _require_exact(rest, low, high)
    return rest * (low - high)


# --- 2^k digit cycle ---------------------------------------------------------

def digit_cycle():
    """Digital roots of 2^k: 1, 2, 4, 8, 7, 5 and around again."""
    return [pow(2, k, 9) for k in range(6)]


def cycle_mirrors():
    """Two mirrors on the cycle: k and k+3 add to 9; k and 6-k multiply to 1 (mod 9)."""
    c = digit_cycle()
    additive = [(c[k], c[(k + 3) % 6]) for k in range(3)]
    multiplicative = [(c[k], c[-k % 6]) for k in range(4)]
    return additive, multiplicative


def digital_root(n):
    """Iterated digit sum 1..9 (0 for 0)."""
    n = abs(int(n))
    return 0 if n == 0 else 1 + (n - 1) % 9


def outer_inner_mirror(steps=6):
    """Outside 2^k against inside 1/2^k = 5^k / 10^k: digit roots and their product.

    2^k runs 1-2-4-8-7-5, 5^k the same cycle backwards; because
    2^k * 5^k = 10^k, the product always has digit root 1.
    """
    return [(digital_root(2 ** k), digital_root(5 ** k), digital_root(digital_root(2 ** k) * digital_root(5 ** k)))
            for k in range(steps)]


# --- Stern-Brocot tree --------------------------------------------------------

def stern_brocot_path(x):
    """L/R path from 1/1 to the positive fraction x, by mediants only."""
    x = Fraction(x)
    if x <= 0:
        raise ValueError("positive fractions only")
    lo, hi, path = (0, 1), (1, 0), []
    while True:
        m = (lo[0] + hi[0], lo[1] + hi[1])
        if Fraction(*m) == x:
            return "".join(path)
        if x < Fraction(*m):
            hi, path = m, path + ["L"]
        else:
            lo, path = m, path + ["R"]


def from_path(path):
    """The fraction at the end of an L/R path -- additions only, no division."""
    lo, hi = (0, 1), (1, 0)
    for step in path:
        m = (lo[0] + hi[0], lo[1] + hi[1])
        if step == "L":
            hi = m
        elif step == "R":
            lo = m
        else:
            raise ValueError("path uses L and R only")
    return Fraction(lo[0] + hi[0], lo[1] + hi[1])
