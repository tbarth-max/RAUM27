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


def test_driven_system_mean_grows_by_source_mean_every_step():
    # v_{n+1} = K @ v_n + source: a source re-added every step, instead of a
    # one-off input left to decay. K preserves the mean exactly, so a source
    # with a nonzero mean makes the mean grow without bound -- resonance.
    K = cp.composed_kernel()
    source = (Fraction(2), Fraction(0), Fraction(0), Fraction(0), Fraction(0), Fraction(0))
    source_mean = sum(source) / 6

    v = tuple(Fraction(0) for _ in range(6))
    for n in range(1, 6):
        v = cp.apply_driven(K, v, source)
        assert sum(v) / 6 == n * source_mean


def test_driven_system_eigenvalue_zero_component_locks_after_one_step():
    K = cp.composed_kernel()
    (p0a, p0b), (p1a, p1b), (p2a, p2b) = _axis_pairs_by_index()
    source = [Fraction(0)] * 6
    source[p0a] = source[p0b] = Fraction(1)
    source[p1a] = source[p1b] = Fraction(1)
    source[p2a] = source[p2b] = Fraction(-2)
    source = tuple(source)  # symmetric within each pair, zero mean -> pure eigenvalue-0 mode
    assert sum(source) == 0

    v = tuple(Fraction(0) for _ in range(6))
    v = cp.apply_driven(K, v, source)
    assert v == source
    for _ in range(5):
        v = cp.apply_driven(K, v, source)
        assert v == source


def test_driven_system_eigenvalue_third_component_matches_closed_form():
    K = cp.composed_kernel()
    a, b = _axis_pairs_by_index()[0]
    source = [Fraction(0)] * 6
    source[a], source[b] = Fraction(1), Fraction(-1)  # pure eigenvalue-1/3 mode
    source = tuple(source)

    lam = Fraction(1, 3)
    v = tuple(Fraction(0) for _ in range(6))
    for n in range(1, 6):
        v = cp.apply_driven(K, v, source)
        # closed form for w_{n+1} = lam*w_n + s, w_0 = 0: w_n = s*(1-lam^n)/(1-lam)
        factor = (1 - lam**n) / (1 - lam)
        assert v == tuple(factor * x for x in source)


def test_driven_system_shape_converges_to_predicted_steady_state():
    K = cp.composed_kernel()
    source = (Fraction(2), Fraction(0), Fraction(0), Fraction(0), Fraction(0), Fraction(0))
    # Predicted steady-state pattern: eigenvalue-1/3 component -> 3/2 * its
    # source contribution (geometric series 1/(1-1/3)), eigenvalue-0
    # component -> locked to its own source contribution (see above).
    steady_shape = (Fraction(13, 6), Fraction(-5, 6), Fraction(-1, 3), Fraction(-1, 3), Fraction(-1, 3), Fraction(-1, 3))

    v = tuple(Fraction(0) for _ in range(6))
    for _ in range(40):
        v = cp.apply_driven(K, v, source)
    mean = sum(v) / 6
    shape = tuple(x - mean for x in v)

    # The eigenvalue-1/3 transient has decayed by (1/3)^40 -- astronomically
    # small but, in exact rational arithmetic, never precisely zero.
    diffs = [abs(s - p) for s, p in zip(shape, steady_shape)]
    assert all(d < Fraction(1, 10**15) for d in diffs)
