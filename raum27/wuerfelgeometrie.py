"""Cube, sphere and octahedron: the counts, ratios and views behind RAUM27.

Everything here was computed in conversation and is kept so it is not
lost; each statement has a test.

- **Why 27.** Each axis takes three states (-1, 0, +1, i.e. 0/1/2 with 1
  as the middle). Grouped by how many axes are "triggered" (not in the
  middle) the 27 cells split as 1 + 6 + 12 + 8: centre, face centres
  (sextants), edge midpoints (the four diagonals in each of the three
  cut planes), corners (octants) -- (1 + 2)^3 multiplied out, with
  squared distances 0, 1, 2, 3 (``shells``).
- **Reflection gives 8, rotation gives 6.** The three cut planes as
  mirrors give 2^3 = 8 sign changes; swapping the axes gives 3! = 6.
  Together 48, the full symmetry of the cube. The orders of its elements
  are 1 (x1), 2 (x19), 3 (x8), 4 (x12), 6 (x8): there is **no element of
  order 8**, so the 1..8 cycle belongs to the square in a cut plane, not
  to the cube (``element_orders``).
- **Rhombus, circle, square** in a cut plane have areas 2 : pi : 4;
  **octahedron, sphere, cube** have volumes 4/3 : 4 pi/3 : 8 = 1 : pi : 6.
  Doubling rhombus and square into 8-, 16-, 32-gons pins pi between them
  (Archimedes, ``archimedes_bounds``).
- **The p-family** |x|^p + |y|^p + |z|^p = 1 runs octahedron (p = 1),
  sphere (p = 2), cube (p -> infinity). Duality p -> p/(p-1) swaps 1 and
  infinity and has exactly one fixed point, p = 2: the sphere is the
  self-dual middle between the 6-system and the 8-system
  (``dual_exponent``).
- **Views of a body.** Counting how many cells lie on each line through
  the 3x3x3 cube, the three axis directions alone are ambiguous -- the
  two interpenetrating tetrahedra of a small cube give identical counts
  -- while the axes plus one space-diagonal (octant) direction determine
  every one of the 2^27 bodies (``views_are_ambiguous``). Linear algebra
  alone leaves one degree of freedom there (rank 26 of 27); the 0/1
  nature of the cells closes it.
"""

from fractions import Fraction
from itertools import permutations, product
import math

CELLS = tuple(product((-1, 0, 1), repeat=3))
AXIS_DIRECTIONS = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
DIAGONAL_DIRECTIONS = ((1, 1, 1), (1, 1, -1), (1, -1, 1), (-1, 1, 1))


def shells():
    """Cells grouped by squared distance from the centre: {0: 1, 1: 6, 2: 12, 3: 8}."""
    counts = {}
    for cell in CELLS:
        r2 = sum(x * x for x in cell)
        counts[r2] = counts.get(r2, 0) + 1
    return counts


def cube_symmetries():
    """The 48 signed permutation matrices."""
    return [tuple(tuple(signs[i] if perm[i] == j else 0 for j in range(3)) for i in range(3))
            for perm in permutations(range(3)) for signs in product((1, -1), repeat=3)]


def _mul(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)) for i in range(3))


def _det(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def element_orders(rotations_only=False):
    """How many symmetries have each order."""
    identity = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    counts = {}
    for g in cube_symmetries():
        if rotations_only and _det(g) != 1:
            continue
        n, h = 1, g
        while h != identity:
            h, n = _mul(h, g), n + 1
        counts[n] = counts.get(n, 0) + 1
    return counts


def plane_area_ratio():
    """Rhombus and square areas around a unit circle (circle area is pi)."""
    return Fraction(2), Fraction(4)


def solid_volume_ratio():
    """Octahedron and cube volumes around a unit sphere, in units of the octahedron (sphere: pi)."""
    octahedron, cube = Fraction(4, 3), Fraction(8)
    return Fraction(1), cube / octahedron


def archimedes_bounds(doublings):
    """(inner, outer) half-perimeters of the 4 * 2^k-gons around a unit circle."""
    n, s_in, s_out = 4, math.sqrt(2), 2.0
    for _ in range(doublings):
        s_in = math.sqrt(2 - math.sqrt(4 - s_in ** 2))
        s_out = 2 * s_out / (math.sqrt(4 + s_out ** 2) + 2)
        n *= 2
    return n * s_in / 2, n * s_out / 2


def dual_exponent(p):
    """The dual exponent p/(p-1); 1 and infinity (``None``) swap."""
    if p is None:
        return Fraction(1)
    p = Fraction(p)
    if p < 1:
        raise ValueError("the p-family starts at p = 1")
    if p == 1:
        return None
    return p / (p - 1)


def _lines(direction):
    lines = {}
    for cell in CELLS:
        start = cell
        while all(-1 <= start[i] - direction[i] <= 1 for i in range(3)):
            start = tuple(start[i] - direction[i] for i in range(3))
        lines.setdefault(start, []).append(CELLS.index(cell))
    return list(lines.values())


def line_count_rank(directions):
    """Rank of the line-sum equations over the rationals."""
    rows = [[Fraction(int(j in line)) for j in range(27)] for d in directions for line in _lines(d)]
    rank = 0
    for col in range(27):
        pivot = next((i for i in range(rank, len(rows)) if rows[i][col]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for i in range(len(rows)):
            if i != rank and rows[i][col]:
                f = rows[i][col] / rows[rank][col]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[rank])]
        rank += 1
    return rank


def views_are_ambiguous(directions):
    """Two different 0/1 bodies with the same count on every line, or ``None``.

    Searches for a non-zero difference pattern in {-1, 0, 1}^27 whose
    count on every line is zero; such a pattern is exactly a swap that
    the views cannot see.
    """
    lines = [set(line) for d in directions for line in _lines(d)]
    pattern = [0] * 27

    def feasible(k):
        for line in lines:
            done = sum(pattern[j] for j in line if j < k)
            left = sum(1 for j in line if j >= k)
            if abs(done) > left:
                return False
        return True

    def search(k):
        if k == 27:
            return any(pattern)
        for v in (0, 1, -1):
            pattern[k] = v
            if feasible(k + 1) and search(k + 1):
                return True
        pattern[k] = 0
        return False

    if not search(0):
        return None
    plus = sorted(CELLS[i] for i in range(27) if pattern[i] == 1)
    minus = sorted(CELLS[i] for i in range(27) if pattern[i] == -1)
    return plus, minus


def octant_cube_sharing():
    """Eight unit cubes stacked 2x2x2: how many cubes share each of their corner points.

    The corners are the 27 points {0, 1, 2}^3. A point is shared by
    2^(number of its coordinates equal to 1) cubes: the centre by all 8,
    the 6 face centres by 4, the 12 edge midpoints by 2, the 8 outer
    corners by 1. Returns {cubes sharing: number of points}.
    """
    counts = {}
    for point in product((0, 1, 2), repeat=3):
        cubes = sum(1 for origin in product((0, 1), repeat=3)
                    if all(o <= p <= o + 1 for o, p in zip(origin, point)))
        counts[cubes] = counts.get(cubes, 0) + 1
    return counts
