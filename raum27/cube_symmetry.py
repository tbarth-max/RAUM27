"""Symmetry of a cube (regular hexahedron) in R^3.

A cube has 6 face directions (+-e_i) and 8 corner directions
(all sign combinations of e1+e2+e3). The notes call the ratio of corner
count to face count the "coupling constant" C = 8/6 = 4/3, and its square
C^2 = 16/9. Those are just counting facts about a cube's symmetry group,
reproduced here as plain arithmetic on tuples, not as a physical constant.
"""

from fractions import Fraction
from itertools import product
from typing import Tuple

Vector3 = Tuple[int, int, int]


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
