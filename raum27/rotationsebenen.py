"""Number of independent rotation planes in n-dimensional space, and a
concrete demonstration that indexing a rotation state by fewer planes
than that loses information.

Standard mathematics: the rotation group SO(n) has dimension
n(n-1)/2 -- one independent generator per pair of axes. For ordinary 3D
space (n=3): 3 planes (XY, XZ, YZ). If a 4th, genuinely rotatable axis
is added (n=4): 6 planes (XY, XZ, XT, YZ, YT, ZT), not 3.

This module is about that hypothetical n=4 case specifically because
this project's own stated principle is "T = Matroschka-Skalierungsachse,
keine 4. Raumdimension" (see README) -- T is explicitly NOT treated as a
rotatable spatial axis elsewhere in this codebase. What's verified here
is the general fact (if T, or any 4th axis, WERE rotatable, you'd need 6
planes, not 3), not a claim that T actually is one.
"""

from __future__ import annotations

from itertools import combinations

import numpy as np


def rotation_plane_count(n: int) -> int:
    """Number of independent rotation planes in n-dimensional space:
    C(n,2) = n(n-1)/2. This is the dimension of SO(n)."""
    return n * (n - 1) // 2


def rotation_planes(axis_names: list[str]) -> list[tuple[str, str]]:
    """The actual named planes for a list of axis labels, e.g.
    ['X','Y','Z','T'] -> [('X','Y'), ('X','Z'), ('X','T'), ('Y','Z'),
    ('Y','T'), ('Z','T')]."""
    return list(combinations(axis_names, 2))


def elementary_rotation(axis_a: int, axis_b: int, angle: float, dimension: int) -> np.ndarray:
    """The elementary rotation matrix acting only in the (axis_a, axis_b)
    plane by `angle`, identity on every other axis."""
    matrix = np.eye(dimension)
    c, s = np.cos(angle), np.sin(angle)
    matrix[axis_a, axis_a] = c
    matrix[axis_b, axis_b] = c
    matrix[axis_a, axis_b] = -s
    matrix[axis_b, axis_a] = s
    return matrix
