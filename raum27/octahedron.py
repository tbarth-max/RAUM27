"""The octahedron: dual polyhedron of the cube.

Put a vertex at each of the cube's 6 face centers (cube_symmetry's
face_directions) and a triangular face at each of its 8 corners
(corner_directions) -- vertex and face counts trade places exactly,
(8,6) -> (6,8), while the edge count stays 12. This is the classical
cube-octahedron duality, constructed here from the same building blocks
already verified in cube_symmetry.py, not asserted separately.

Dualizing a second time (taking face centroids of this octahedron as new
"corners") does not return a copy at the same size: it returns the
original cube's corners scaled by exactly 1/3 (see dual_cube_corners
and tests/test_octahedron.py). Two dualizations in a row shrink toward
the center; they do not grow.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
from typing import Tuple

from raum27.cube_symmetry import corner_directions, face_directions

Point3 = Tuple[Fraction, Fraction, Fraction]
Face = Tuple[Point3, Point3, Point3]


def _centroid(points: list[Point3]) -> Point3:
    n = len(points)
    return tuple(sum(p[i] for p in points) / n for i in range(3))


def vertices() -> list[Point3]:
    """The 6 octahedron vertices: exactly the cube's face directions."""
    return [tuple(Fraction(x) for x in v) for v in face_directions()]


def faces() -> list[Face]:
    """The 8 triangular faces: one per cube corner direction (sx,sy,sz),
    connecting the 3 octahedron vertices (sx,0,0), (0,sy,0), (0,0,sz)."""
    result = []
    for sx, sy, sz in corner_directions():
        result.append((
            (Fraction(sx), Fraction(0), Fraction(0)),
            (Fraction(0), Fraction(sy), Fraction(0)),
            (Fraction(0), Fraction(0), Fraction(sz)),
        ))
    return result


def edges() -> set[frozenset[Point3]]:
    """The 12 unique edges, each shared by exactly 2 of the 8 faces."""
    result: set[frozenset[Point3]] = set()
    for face in faces():
        for a, b in combinations(face, 2):
            result.add(frozenset((a, b)))
    return result


def euler_characteristic() -> int:
    """V - E + F: 2 for any convex polyhedron."""
    return len(vertices()) - len(edges()) + len(faces())


def dual_cube_corners() -> list[Point3]:
    """Dualizing this octahedron once more: the centroid of each of its 8
    faces. Same order as corner_directions()."""
    return [_centroid(list(face)) for face in faces()]
