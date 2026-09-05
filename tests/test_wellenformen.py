"""Tests for raum27.wellenformen."""
from __future__ import annotations

import numpy as np

from raum27.wellenformen import (
    mean_square_energy,
    square_wave_partial,
    triangle_wave_partial,
)

X = np.linspace(0, 2 * np.pi, 200_000, endpoint=False)


def test_square_wave_energy_grows_monotonically_not_at_a_constant_equilibrium():
    """Correction of an earlier 'Energiegleichgewicht' (fixed energy
    equilibrium) framing: adding more terms strictly increases the
    partial sum's energy, converging up towards the true square wave's
    energy of 1 -- it never sits at one constant value along the way."""
    term_counts = [1, 2, 3, 5, 10, 20, 50, 100]
    energies = [mean_square_energy(square_wave_partial(X, n)) for n in term_counts]
    assert all(energies[i] < energies[i + 1] for i in range(len(energies) - 1))
    assert energies[-1] < 1.0
    assert energies[-1] > 0.99


def test_square_wave_shows_the_gibbs_overshoot():
    """A +-1 square wave's Fourier partial sums overshoot the jump by
    about 9% (the Gibbs phenomenon) -- a real signature of approximating
    a discontinuous function with a finite number of continuous sines."""
    sq = square_wave_partial(X, n_terms=200)
    assert 1.05 < sq.max() < 1.20


def test_triangle_wave_has_no_overshoot():
    """The triangle wave is continuous (no jump discontinuity), so there
    is nothing for the Gibbs phenomenon to act on -- its partial sums
    stay within (or essentially at) +-1."""
    tri = triangle_wave_partial(X, n_terms=200)
    assert tri.max() < 1.01


def test_square_and_triangle_are_different_target_shapes_not_resolution_levels():
    """Plateau fraction (time spent near +-1) distinguishes a square
    wave (mostly at the extremes) from a triangle wave (mostly ramping
    between them) -- these are different shapes, not the same curve at
    different levels of completion."""
    sq = square_wave_partial(X, n_terms=200)
    tri = triangle_wave_partial(X, n_terms=200)
    plateau_fraction_sq = np.mean(np.abs(sq) > 0.95)
    plateau_fraction_tri = np.mean(np.abs(tri) > 0.95)
    assert plateau_fraction_sq > 0.9
    assert plateau_fraction_tri < 0.1
