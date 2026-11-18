"""Scanning sphere and cube through ellipsoids: the six axes give the strain, the eight corners test it.

The idea submitted: reproduce physical interaction in the projection
model by passing the ideal spheres and cubes through the ellipses they
really become. In continuum mechanics this is the strain ellipsoid: a
linear deformation ``F`` turns the unit sphere into an ellipsoid and the
cube into a parallelepiped. Everything here is exact for rational ``F``.

What the 6 + 8 point system does with it:

- **The six axis points determine the deformation.** Their images are
  ``F e`` and ``-F e``; half the difference of an opposite pair is a
  column of ``F`` (``deformation_from_axes``). Half their sum must be
  zero for a deformation that keeps the centre fixed -- if it is not,
  the centre moved or the deformation is not linear
  (``axis_asymmetry``).
- **The eight corners then test it.** For a linear deformation each
  corner image is the signed sum of the three axis images, so every
  corner is predicted before it is measured. What remains
  (``corner_residuals``) is exactly what a linear law cannot explain:
  the nonlinear part of the real interaction.

So the sextant system measures and the octant system checks. The ellipsoid
itself is read from ``C = F^T F``: its eigenvalues are the squared
semi-axes, ``det F`` is the volume ratio, and ``C = I`` means a rigid
motion (``is_rigid``). The eigenvalues are roots of a cubic and need not
be rational; the cubic's coefficients -- the three invariants -- are
always exact (``invariants``).

Example kept in the tests: stretching by 4/3 along one axis and 3/4
along another gives squared semi-axes 16/9, 1, 9/16 and keeps the volume
exactly, since 4/3 * 3/4 = 1.
"""

from fractions import Fraction
from itertools import product

AXES = tuple(tuple(int(i == k) * s for i in range(3)) for k in range(3) for s in (1, -1))
CORNERS = tuple(product((-1, 1), repeat=3))


def _matrix(F):
    M = tuple(tuple(Fraction(x) for x in row) for row in F)
    if len(M) != 3 or any(len(row) != 3 for row in M):
        raise ValueError("a deformation is a 3x3 matrix")
    return M


def apply(F, point):
    """Image of ``point`` under the linear deformation ``F``."""
    M = _matrix(F)
    return tuple(sum(M[i][j] * point[j] for j in range(3)) for i in range(3))


def deformation_from_axes(images):
    """``F`` from the images of the six axis points, in the order of ``AXES``."""
    if len(images) != 6:
        raise ValueError("six axis images are needed")
    columns = []
    for k in range(3):
        plus, minus = images[2 * k], images[2 * k + 1]
        columns.append([(Fraction(p) - Fraction(m)) / 2 for p, m in zip(plus, minus)])
    return tuple(tuple(columns[j][i] for j in range(3)) for i in range(3))


def axis_asymmetry(images):
    """Half the sum of each opposite pair; all zero for a centre-fixed linear map."""
    return tuple(tuple((Fraction(p) + Fraction(m)) / 2 for p, m in zip(images[2 * k], images[2 * k + 1]))
                 for k in range(3))


def corner_residuals(F, corner_images):
    """Measured corner images minus what the linear law predicts, in the order of ``CORNERS``."""
    if len(corner_images) != 8:
        raise ValueError("eight corner images are needed")
    return tuple(tuple(Fraction(m) - p for m, p in zip(measured, apply(F, corner)))
                 for measured, corner in zip(corner_images, CORNERS))


def cauchy_green(F):
    """``C = F^T F``; its eigenvalues are the squared semi-axes of the ellipsoid."""
    M = _matrix(F)
    return tuple(tuple(sum(M[k][i] * M[k][j] for k in range(3)) for j in range(3)) for i in range(3))


def determinant(F):
    M = _matrix(F)
    return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
            - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
            + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))


def invariants(F):
    """(I1, I2, I3) of ``C``: the coefficients of the cubic whose roots are the squared semi-axes."""
    C = cauchy_green(F)
    i1 = C[0][0] + C[1][1] + C[2][2]
    i2 = (C[0][0] * C[1][1] + C[1][1] * C[2][2] + C[0][0] * C[2][2]
          - C[0][1] ** 2 - C[1][2] ** 2 - C[0][2] ** 2)
    return i1, i2, determinant(F) ** 2


def is_rigid(F):
    """True exactly when ``F`` only turns or mirrors: the sphere stays a sphere."""
    identity = tuple(tuple(Fraction(int(i == j)) for j in range(3)) for i in range(3))
    return cauchy_green(F) == identity


def squared_semi_axes_if_diagonal(F):
    """Squared semi-axes when ``C`` is diagonal (the axes are the coordinate axes)."""
    C = cauchy_green(F)
    if any(C[i][j] for i in range(3) for j in range(3) if i != j):
        raise ValueError("C is not diagonal; use invariants() and solve the cubic")
    return tuple(sorted((C[0][0], C[1][1], C[2][2]), reverse=True))
