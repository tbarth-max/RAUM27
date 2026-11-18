"""Tests for raum27.restkreis."""

from fractions import Fraction
from itertools import product

import pytest

from raum27.restkreis import (
    as_fraction, balanced_ternary, circles, denormalize, determinant, faces,
    from_balanced_ternary, hyperdeterminant, normalize, partial_fractions,
    rest_to_one, turned, unweigh, weigh,
)


def test_working_range_and_zoom():
    assert normalize(1) == (0, 1)
    assert normalize(Fraction(9, 2)) == (1, Fraction(1, 2))
    assert normalize(Fraction(1, 9)) == (-1, 1)
    assert normalize(Fraction(1, 4)) == (-1, Fraction(9, 4))
    for v in [Fraction(1, 1000), Fraction(7, 3), 27, 729, Fraction(355, 113), 10**12]:
        k, m = normalize(v)
        assert Fraction(1, 2) <= m < Fraction(9, 2)
        assert denormalize(k, m) == v
    assert normalize(10, base=2, low=1) == (3, Fraction(5, 4))
    for bad in (0, -1):
        with pytest.raises(ValueError):
            normalize(bad)
    with pytest.raises(ValueError):
        normalize(1, base=1)
    with pytest.raises(TypeError):
        normalize(0.5)


def test_bachet_weights_with_both_pans():
    seen = set()
    for n in range(1, 41):
        d = balanced_ternary(n)
        assert len(d) <= 4 and set(d) <= {-1, 0, 1}
        assert from_balanced_ternary(d) == n
        seen.add(tuple(d))
    assert len(seen) == 40                                   # each weight once, unique
    assert balanced_ternary(2) == [-1, 1]                    # 2 = 3 - 1
    assert balanced_ternary(0) == []
    assert from_balanced_ternary(balanced_ternary(-13)) == -13
    with pytest.raises(TypeError):
        balanced_ternary(Fraction(1, 2))


def test_weigh_a_fraction():
    for x in [Fraction(28, 29), Fraction(-7, 5), Fraction(1, 2), Fraction(9, 2), Fraction(355, 113)]:
        for p in (0, 1, 4, 9):
            i, f, rest = weigh(x, p)
            assert set(f) <= {-1, 0, 1} and len(f) == p
            assert abs(rest) <= Fraction(1, 2 * 3**p)
            assert unweigh(i, f, rest) == x
    assert weigh(Fraction(1, 3), 1) == ([], [1], 0)


def test_the_rest_as_a_fraction():
    measured = Fraction("0.966")
    assert as_fraction(measured, Fraction(1, 1000)) == Fraction(28, 29)
    assert rest_to_one(measured, Fraction(1, 1000)) == (Fraction(28, 29), Fraction(-1, 29))
    assert as_fraction(measured, 0) == measured              # no tolerance: exact
    assert 1 - Fraction(5, 12) * Fraction(3, 10) ** 2 == Fraction(77, 80)   # theory for alpha = 0.3


def test_which_circles():
    assert circles(Fraction(1, 29)) == {29: 1}
    assert circles(Fraction(3, 80)) == {2: 4, 5: 1}
    assert circles(Fraction(1, 9)) == {3: 2}
    assert circles(5) == {}
    assert partial_fractions(Fraction(3, 80)) == (-1, [(7, 16), (3, 5)])
    assert Fraction(7, 16) - Fraction(2, 5) == Fraction(3, 80)
    assert partial_fractions(Fraction(1, 29)) == (0, [(1, 29)])
    for x in [Fraction(3, 80), Fraction(-17, 360), Fraction(28, 29), Fraction(1001, 30), Fraction(7)]:
        n, parts = partial_fractions(x)
        assert n + sum(Fraction(a, pe) for a, pe in parts) == x
        assert all(0 <= a < pe for a, pe in parts)


def test_cell_and_cube():
    assert determinant(2, 3, 4, 5) == -2
    assert determinant(28, 1, 29, 1) == -1                   # 28/29 and 1/1 are neighbours
    assert determinant(1, 2, 2, 4) == 0
    u, v, w = (1, 2), (3, Fraction(1, 2)), (5, 7)
    prod_cube = [[[u[i] * v[j] * w[k] for k in (0, 1)] for j in (0, 1)] for i in (0, 1)]
    assert hyperdeterminant(prod_cube) == 0                  # one product: no rest in space
    ghz = [[[1 if i == j == k else 0 for k in (0, 1)] for j in (0, 1)] for i in (0, 1)]
    w_state = [[[1 if i + j + k == 1 else 0 for k in (0, 1)] for j in (0, 1)] for i in (0, 1)]
    assert hyperdeterminant(ghz) == 1 and hyperdeterminant(w_state) == 0
    cube = [[[2, 3], [5, 7]], [[11, 13], [17, Fraction(19, 2)]]]
    h = hyperdeterminant(cube)
    for axis in (0, 1, 2):
        assert hyperdeterminant(turned(cube, axis)) == h     # same from every side
        front, back = faces(cube, axis)
        assert front == turned(cube, axis)[0] and back == turned(cube, axis)[1]
    assert faces(cube, 0) == ([[2, 3], [5, 7]], [[11, 13], [17, Fraction(19, 2)]])
    for bad in ([[1, 2], [3, 4]], [[[1, 2]], [[3, 4]]]):
        with pytest.raises(ValueError):
            hyperdeterminant(bad)
    for f in (faces, turned):
        with pytest.raises(ValueError):
            f(cube, 3)


def test_hyperdeterminant_is_exact_on_random_integer_cubes():
    import random
    rng = random.Random(27)
    for _ in range(50):
        vals = [rng.randint(-9, 9) for _ in range(8)]
        cube = [[[vals[4 * i + 2 * j + k] for k in (0, 1)] for j in (0, 1)] for i in (0, 1)]
        h = hyperdeterminant(cube)
        assert all(hyperdeterminant(turned(cube, a)) == h for a in (0, 1, 2))
        assert h.denominator == 1
    assert len(list(product((0, 1), repeat=3))) == 8
