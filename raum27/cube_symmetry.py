"""Symmetry of a cube (regular hexahedron) in R^3.

A cube has 6 face directions (+-e_i) and 8 corner directions
(all sign combinations of e1+e2+e3). The notes call the ratio of corner
count to face count the "coupling constant" C = 8/6 = 4/3, and its square
C^2 = 16/9. Those are just counting facts about a cube's symmetry group,
reproduced here as plain arithmetic on tuples, not as a physical constant.

Also here: the cube's diagonals. A note elsewhere claimed the 4 diagonals
that meet at the cube's center have length sqrt(2); that is the *face*
diagonal, which does not pass through the center (it only crosses its own
face's center). The 4 diagonals through the cube's center are the *space*
(body) diagonals, corner to opposite corner, and their length is sqrt(3)
-- a second application of Pythagoras. Both facts are verified below in
exact rational arithmetic (by comparing squared lengths and midpoints,
never a float sqrt), see tests/test_cube_symmetry.py.

And: a cube decomposes into 6 congruent pyramids, one per face, each with
its apex at the cube's center. For a cube with center-to-face distance
"radius" 1 (edge 2), each pyramid has height 1, a base half-diagonal
(face center to face corner) of sqrt(2), and an apex-to-corner distance
of sqrt(3) -- matching the space diagonal above, since center-to-corner
is exactly half of corner-to-opposite-corner. Cross-checked independently
by volume: 6 * pyramid_volume(edge) == cube_volume(edge) exactly, for
every edge length, in exact rational arithmetic.
"""

from fractions import Fraction
from itertools import product
from typing import Tuple

Vector3 = Tuple[int, int, int]
Point3 = Tuple[Fraction, Fraction, Fraction]


def face_directions() -> list[Vector3]:
    """The 6 unit-axis directions (+-e1, +-e2, +-e3)."""
    dirs = []
    for axis in range(3):
        for sign in (1, -1):
            v = [0, 0, 0]
            v[axis] = sign
            dirs.append(tuple(v))
    return dirs


def corner_directions() -> list[Vector3]:
    """The 8 corner directions (all sign combinations of e1+e2+e3)."""
    return list(product((1, -1), repeat=3))


def vector_equilibrium() -> Vector3:
    """Sum of all corner direction vectors. Symmetric sign choices cancel
    pairwise, so this is always (0, 0, 0)."""
    corners = corner_directions()
    return tuple(sum(v[i] for v in corners) for i in range(3))


def coupling_constant() -> Fraction:
    """C = |corner directions| / |face directions| = 8/6 = 4/3."""
    return Fraction(len(corner_directions()), len(face_directions()))


def axis_cross_product(u: Vector3, v: Vector3) -> Vector3:
    """The standard 3D cross product. For the cube's own axis-aligned
    face directions this recovers the third one from the other two, e.g.
    ex x ey = ez -- ordinary vector algebra, not specific to this cube."""
    return (
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0],
    )


def space_diagonals() -> list[frozenset[Vector3]]:
    """The 4 unique space (body) diagonals of the cube: each of the 8
    corner directions paired with its antipodal corner. The 8 directed
    corner vectors collapse into 4 undirected lines through the center."""
    corners = corner_directions()
    seen: set[frozenset[Vector3]] = set()
    diagonals = []
    for c in corners:
        opposite = tuple(-x for x in c)
        pair = frozenset((c, opposite))
        if pair not in seen:
            seen.add(pair)
            diagonals.append(pair)
    return diagonals


def face_diagonal_squared(edge: Fraction = Fraction(1)) -> Fraction:
    """Squared length of a diagonal across one face of the cube (Pythagoras
    with both legs = edge). Returned squared, in exact rational arithmetic,
    because the diagonal itself (sqrt(2) * edge) is irrational."""
    return edge**2 + edge**2


def space_diagonal_squared(edge: Fraction = Fraction(1)) -> Fraction:
    """Squared length of a space (body) diagonal: a second application of
    Pythagoras, combining a face diagonal with the remaining edge. For
    edge=1 this is 3 (i.e. sqrt(3)), not 2 (sqrt(2)) -- sqrt(2) is the
    face diagonal, which does not pass through the cube's center."""
    return face_diagonal_squared(edge) + edge**2


def cube_center(edge: Fraction = Fraction(1)) -> Point3:
    """Center of a cube with one corner at the origin and edges along
    the axes, running from 0 to `edge`."""
    half = edge / 2
    return (half, half, half)


def face_diagonal_midpoint(edge: Fraction = Fraction(1)) -> Point3:
    """Midpoint of the diagonal across the cube's z=0 face, from (0,0,0)
    to (edge,edge,0)."""
    half = edge / 2
    return (half, half, Fraction(0))


def space_diagonal_midpoint(edge: Fraction = Fraction(1)) -> Point3:
    """Midpoint of the body diagonal from (0,0,0) to (edge,edge,edge)."""
    half = edge / 2
    return (half, half, half)


def cube_volume(edge: Fraction = Fraction(1)) -> Fraction:
    return edge**3


def pyramid_height(edge: Fraction = Fraction(1)) -> Fraction:
    """Perpendicular distance from the cube's center to one face: edge/2.
    The height of each of the 6 congruent pyramids formed by pairing the
    center with one face (see pyramid_volume / cube_volume below)."""
    return edge / 2


def pyramid_base_half_diagonal_squared(edge: Fraction = Fraction(1)) -> Fraction:
    """Squared distance from a face's center to one of its own corners:
    Pythagoras with both legs = edge/2."""
    half = edge / 2
    return half**2 + half**2


def pyramid_apex_to_corner_squared(edge: Fraction = Fraction(1)) -> Fraction:
    """Squared distance from the cube's center to one of its corners: a
    second Pythagoras, combining the pyramid height with the base's half
    diagonal. This is a quarter of the full space diagonal squared,
    because center-to-corner is half of corner-to-opposite-corner."""
    return pyramid_height(edge) ** 2 + pyramid_base_half_diagonal_squared(edge)


def pyramid_volume(edge: Fraction = Fraction(1)) -> Fraction:
    """Volume of one of the 6 face-pyramids (apex at the cube's center,
    base = one face): (1/3) * base area * height."""
    return Fraction(1, 3) * edge**2 * pyramid_height(edge)
