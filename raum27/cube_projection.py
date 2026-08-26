"""Linear maps between the cube's 8 corners and 6 faces, and the exact
eigenstructure of their composition.

Each corner touches exactly 3 faces; each face has exactly 4 corners
(cube_symmetry's corner_directions/face_directions). Averaging over that
incidence gives two linear maps: m_6to8 distributes 6 face-values onto 8
corner-values, m_8to6 projects 8 corner-values back onto 6 face-values.
Their composition K = m_8to6 @ m_6to8 (6x6) has a closed form,

    K = (1/6) * (I + A - P)

where A is the 6x6 all-ones matrix and P swaps each face index with its
opposite face's index. That gives an exact eigenstructure, verified below
in rational arithmetic (no floats, no numpy):

- eigenvalue 1, the uniform state (1,1,1,1,1,1) -- the only state that
  survives a corner-then-face round trip unchanged.
- eigenvalue 1/3, multiplicity 3 -- one "this face up, its opposite face
  down" mode per axis.
- eigenvalue 0, multiplicity 2 -- modes erased in a single round trip.

Repeatedly applying K to any starting vector converges to the uniform
state, since 1 is the only eigenvalue with magnitude 1.

A *driven* system -- a constant source added every step instead of a
single one-off input left to decay, v_{n+1} = K @ v_n + source -- behaves
very differently depending on which eigenspace the source falls in:

- A source component along the eigenvalue-1 (uniform) direction is never
  damped: the mean of v grows by exactly mean(source) every step,
  without bound. This is resonance in the ordinary linear-systems sense
  -- a constant drive aligned with an undamped eigendirection.
- A source component in the eigenvalue-1/3 eigenspace converges to a
  finite steady state, source_component * 3/2 (the geometric series
  1/(1-1/3)).
- A source component in the eigenvalue-0 eigenspace locks to exactly the
  source's own value after a single step (there's no previous state left
  for K to add to).

So a source with components in more than one eigenspace produces an
ever-growing mean with a fixed, bounded pattern superimposed on it --
verified in tests/test_cube_projection.py against the exact closed-form
solution of the linear recurrence, not just by iterating and eyeballing
convergence.
"""

from __future__ import annotations

from fractions import Fraction

from raum27.cube_symmetry import corner_directions, face_directions

Matrix = list
Vector = tuple


def incidence_matrix() -> Matrix:
    """8x6 matrix: I[c][f] = 1 if corner c lies on face f, else 0."""
    corners = corner_directions()
    faces = face_directions()

    def on_face(corner, face):
        axis = next(k for k in range(3) if face[k] != 0)
        return corner[axis] == face[axis]

    return [[Fraction(1) if on_face(c, f) else Fraction(0) for f in faces] for c in corners]


def _transpose(matrix: Matrix) -> Matrix:
    return [list(row) for row in zip(*matrix)]


def _matmul(a: Matrix, b: Matrix) -> Matrix:
    inner, cols = len(b), len(b[0])
    return [[sum(a[r][k] * b[k][c] for k in range(inner)) for c in range(cols)] for r in range(len(a))]


def m_6to8() -> Matrix:
    """Distributes 6 face-values onto 8 corner-values: average of each
    corner's 3 adjacent faces."""
    return [[x / 3 for x in row] for row in incidence_matrix()]


def m_8to6() -> Matrix:
    """Projects 8 corner-values onto 6 face-values: average of each
    face's 4 corners."""
    return [[x / 4 for x in row] for row in _transpose(incidence_matrix())]


def composed_kernel() -> Matrix:
    """K = m_8to6 @ m_6to8, a 6x6 matrix."""
    return _matmul(m_8to6(), m_6to8())


def apply(matrix: Matrix, vector: Vector) -> Vector:
    return tuple(sum(row[i] * vector[i] for i in range(len(vector))) for row in matrix)


def apply_driven(matrix: Matrix, vector: Vector, source: Vector) -> Vector:
    """One step of a driven system: v_{n+1} = matrix @ v_n + source."""
    driven = apply(matrix, vector)
    return tuple(a + b for a, b in zip(driven, source))
