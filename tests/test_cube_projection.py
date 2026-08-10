from fractions import Fraction

from raum27 import cube_projection as cp
from raum27.cube_symmetry import face_directions


def test_incidence_matrix_row_and_column_sums():
    I = cp.incidence_matrix()
    assert all(sum(row) == 3 for row in I)  # each corner touches 3 faces
    cols = list(zip(*I))
    assert all(sum(col) == 4 for col in cols)  # each face has 4 corners


def _axis_pairs_by_index():
    faces = face_directions()
    seen = set()
    pairs = []
    for f in faces:
        if f in seen:
            continue
        opposite = tuple(-x for x in f)
        pairs.append((faces.index(f), faces.index(opposite)))
        seen.add(f)
        seen.add(opposite)
    return pairs


def test_uniform_state_is_the_unique_fixed_point():
    K = cp.composed_kernel()
    uniform = tuple(Fraction(1) for _ in range(6))
    assert cp.apply(K, uniform) == uniform


def test_antisymmetric_axis_modes_have_eigenvalue_one_third():
    K = cp.composed_kernel()
    for i, j in _axis_pairs_by_index():
        v = [Fraction(0)] * 6
        v[i], v[j] = Fraction(1), Fraction(-1)
        v = tuple(v)
        result = cp.apply(K, v)
        assert result == tuple(Fraction(1, 3) * x for x in v)


def test_symmetric_orthogonal_modes_are_erased_in_one_step():
    K = cp.composed_kernel()
    (p0a, p0b), (p1a, p1b), (p2a, p2b) = _axis_pairs_by_index()

    for x, y, z in [(1, -1, 0), (1, 0, -1)]:
        v = [Fraction(0)] * 6
        v[p0a] = v[p0b] = Fraction(x)
        v[p1a] = v[p1b] = Fraction(y)
        v[p2a] = v[p2b] = Fraction(z)
        result = cp.apply(K, tuple(v))
        assert result == tuple(Fraction(0) for _ in range(6))


def test_repeated_application_decays_nonuniform_modes_exactly():
    # A mix of the uniform (eigenvalue 1) and one antisymmetric (eigenvalue
    # 1/3) mode: repeated application must leave the uniform part alone and
    # shrink the antisymmetric part by exactly (1/3)^n -- checked exactly,
    # not approximately, since exact rational arithmetic never rounds.
    K = cp.composed_kernel()
    (a, b) = _axis_pairs_by_index()[0]

    uniform = [Fraction(1)] * 6
    antisym = [Fraction(0)] * 6
    antisym[a], antisym[b] = Fraction(1), Fraction(-1)

    c0, c1 = Fraction(2), Fraction(9)
    v = tuple(c0 * u + c1 * s for u, s in zip(uniform, antisym))

    n = 3
    result = v
    for _ in range(n):
        result = cp.apply(K, result)

    expected = tuple(c0 * u + c1 * Fraction(1, 3) ** n * s for u, s in zip(uniform, antisym))
    assert result == expected
