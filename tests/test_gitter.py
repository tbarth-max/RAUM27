"""Tests for raum27.gitter: band limit, decay above it, structure guard."""

from fractions import Fraction
import math

import numpy as np
import pytest

from raum27.gitter import (
    LINDEMANN,
    decay_per_cell,
    dispersion,
    max_energy_per_particle,
    max_frequency,
    passes,
    ring_frequencies,
    structure_holds,
)


def test_ring_frequencies_match_the_eigenvalues_of_the_spring_ring():
    n, k, m = 12, 3.0, 2.0
    K = np.zeros((n, n))
    for i in range(n):
        j = (i + 1) % n
        K[i, i] += k
        K[j, j] += k
        K[i, j] -= k
        K[j, i] -= k
    exact = sorted(math.sqrt(max(v, 0.0) / m) if v > 1e-12 else 0.0 for v in np.linalg.eigvalsh(K))
    assert ring_frequencies(n, k, m) == pytest.approx(exact, abs=1e-9)
    assert max(exact) == pytest.approx(max_frequency(k, m))


def test_dispersion_is_bounded_by_the_band_edge():
    k, m = 5.0, 1.5
    top = max_frequency(k, m)
    values = [dispersion(q, k, m) for q in np.linspace(-math.pi, math.pi, 401)]
    assert max(values) == pytest.approx(top)
    assert all(v <= top + 1e-12 for v in values)


def test_inside_the_band_passes_above_it_decays_cell_by_cell():
    k, m = 4.0, 1.0
    top = max_frequency(k, m)
    assert passes(0.99 * top, k, m) and decay_per_cell(0.99 * top, k, m) == 1.0
    assert not passes(1.5 * top, k, m)
    factor = decay_per_cell(1.5 * top, k, m)
    assert 0 < factor < 1
    # check against the recurrence u[n+1] + u[n-1] = 2 b u[n] for the decaying solution
    b = 1 - m * (1.5 * top) ** 2 / (2 * k)
    r = -factor  # the decaying root alternates in sign above the band
    assert r * r - 2 * b * r + 1 == pytest.approx(0, abs=1e-12)
    assert decay_per_cell(3 * top, k, m) < factor           # further above, faster decay


def test_structure_guard_is_the_lindemann_energy():
    m, omega, a = 2, 3, Fraction(1, 2)
    e_max = max_energy_per_particle(m, omega, a)
    assert e_max == Fraction(2 * 9, 2) * (LINDEMANN * a) ** 2
    assert structure_holds(e_max * Fraction(99, 100), m, omega, a)
    assert not structure_holds(e_max, m, omega, a)          # reaching it is already too much


def test_invalid_inputs():
    with pytest.raises(ValueError):
        max_frequency(0, 1)
    with pytest.raises(ValueError):
        ring_frequencies(1, 1, 1)
