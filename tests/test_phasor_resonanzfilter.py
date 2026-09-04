"""Tests for raum27.phasor_resonanzfilter."""
from __future__ import annotations

import numpy as np
import pytest

from raum27.phasor_resonanzfilter import (
    correlation,
    energy,
    fires,
    matched_detector,
    state_at,
)


def _random_pattern(rng, k):
    amplitudes = rng.uniform(0.5, 2.0, k)
    phases = rng.uniform(0, 2 * np.pi, k)
    frequencies = rng.uniform(0.5, 3.0, k)
    return amplitudes, phases, frequencies


def test_energy_is_exactly_constant_over_time():
    """|s(t)|^2 = sum(A_k^2) for every t -- each phasor's magnitude never
    changes, only its phase does."""
    rng = np.random.default_rng(0)
    A, phi, omega = _random_pattern(rng, k=8)
    expected = energy(A)
    for t in (0.0, 1.5, 100.0, -37.2, 1e6):
        s = state_at(A, phi, omega, t)
        assert np.sum(np.abs(s) ** 2) == pytest.approx(expected, rel=1e-9)


def test_matched_detector_hits_the_cauchy_schwarz_bound():
    rng = np.random.default_rng(1)
    A, phi, omega = _random_pattern(rng, k=8)
    t0 = 2.5
    detector = matched_detector(A, phi, omega, t0)
    r0 = correlation(detector, A, phi, omega, t0)
    assert r0 == pytest.approx(energy(A) ** 0.5, rel=1e-9)


def test_no_unit_vector_beats_the_matched_detector():
    """Direct Cauchy-Schwarz check: among many random unit vectors, none
    exceeds the correlation achieved by the matched detector."""
    rng = np.random.default_rng(2)
    A, phi, omega = _random_pattern(rng, k=6)
    t0 = 1.37
    detector = matched_detector(A, phi, omega, t0)
    r0 = correlation(detector, A, phi, omega, t0)

    best_random = -np.inf
    for _ in range(3000):
        v = rng.normal(size=6) + 1j * rng.normal(size=6)
        v = v / np.linalg.norm(v)
        r = float(np.real(np.vdot(v, state_at(A, phi, omega, t0))))
        best_random = max(best_random, r)
    assert r0 >= best_random - 1e-9


def test_match_time_is_a_global_not_just_local_maximum():
    """Scans R(t) across a wide range, not just near t0 -- t0 must still
    be (essentially) the unique maximum, per the Cauchy-Schwarz argument
    in the module docstring (|s(t)| is constant, so nothing elsewhere can
    exceed R(t0))."""
    rng = np.random.default_rng(3)
    A, phi, omega = _random_pattern(rng, k=6)
    t0 = 4.2
    detector = matched_detector(A, phi, omega, t0)
    r0 = correlation(detector, A, phi, omega, t0)

    ts = np.linspace(-500, 500, 200_000)
    values = np.array([correlation(detector, A, phi, omega, t) for t in ts])
    assert values.max() <= r0 + 1e-6

    near_global_max = ts[values > 0.99999 * r0]
    assert np.all(np.abs(near_global_max - t0) < 0.02)


def test_correlation_falls_off_away_from_the_match_time():
    """A fixed detector does not stay 'docked' to a rotating memory state
    -- the match is a moment, not a persistent condition."""
    rng = np.random.default_rng(4)
    A, phi, omega = _random_pattern(rng, k=6)
    t0 = 1.37
    detector = matched_detector(A, phi, omega, t0)
    r0 = correlation(detector, A, phi, omega, t0)

    for dt in (0.05, 0.2, 0.5):
        assert correlation(detector, A, phi, omega, t0 + dt) < r0
        assert correlation(detector, A, phi, omega, t0 - dt) < r0


def test_small_k_discrimination_can_actually_fail():
    """A concrete, fixed (not randomly-searched-for-in-the-test) example
    at K=4 where the detector's OWN pattern peak is lower than an
    unrelated pattern's peak -- discrimination is not automatic just
    because two patterns are different. Found by scanning seeds once
    during development (seed 18) and hardcoded here so the failure is
    reproducible on demand, not dependent on which seed a test happens
    to draw."""
    A1 = np.array([1.0989586538263592, 1.5761220189323242, 0.921234992054005, 0.6240873769971744])
    phi1 = np.array([6.09325290470506, 3.54325624082152, 4.048388002496526, 3.6245903036107783])
    omega1 = np.array([1.6884024243248401, 0.8060049746196425, 1.2839903030580453, 2.34052145671248])
    A2 = np.array([1.8610835495724976, 1.8329029177645817, 1.922481322804913, 0.5381058820574656])
    phi2 = np.array([4.637233194654726, 4.226070918702988, 3.928169796950895, 4.0063109289976895])
    omega2 = np.array([0.8156772288296683, 2.065415277541107, 2.4677295267152415, 0.5185025983113993])
    t0 = 4.605219136071874

    detector = matched_detector(A1, phi1, omega1, t0)
    ts = np.linspace(t0 - 3, t0 + 3, 1500)
    own_peak = max(correlation(detector, A1, phi1, omega1, t) for t in ts)
    other_peak = max(correlation(detector, A2, phi2, omega2, t) for t in ts)
    assert own_peak < other_peak


def test_discrimination_becomes_more_reliable_with_more_channels():
    """Not "always works", but a real, measured trend: over 150 random
    pattern pairs per channel count, the fraction where discrimination
    fails (own-pattern peak < other-pattern peak) is strictly lower at
    K=32 than at K=4, and the typical (median) margin is larger. Checked
    stable across several seeds during development before picking this
    one -- not a value cherry-picked to make the assertion pass."""
    rng = np.random.default_rng(7)

    def own_vs_other_ratio(k):
        A1, phi1, omega1 = _random_pattern(rng, k)
        A2, phi2, omega2 = _random_pattern(rng, k)
        t0 = rng.uniform(0, 5)
        detector = matched_detector(A1, phi1, omega1, t0)
        ts = np.linspace(t0 - 3, t0 + 3, 800)
        own_peak = max(correlation(detector, A1, phi1, omega1, t) for t in ts)
        other_peak = max(correlation(detector, A2, phi2, omega2, t) for t in ts)
        return own_peak / other_peak

    ratios_small_k = [own_vs_other_ratio(4) for _ in range(150)]
    ratios_large_k = [own_vs_other_ratio(32) for _ in range(150)]

    failure_rate_small_k = sum(1 for r in ratios_small_k if r < 1.0) / len(ratios_small_k)
    failure_rate_large_k = sum(1 for r in ratios_large_k if r < 1.0) / len(ratios_large_k)

    assert failure_rate_small_k > 0.0
    assert failure_rate_large_k < failure_rate_small_k
    assert np.median(ratios_large_k) > np.median(ratios_small_k)


def test_fires_respects_the_threshold():
    rng = np.random.default_rng(6)
    A, phi, omega = _random_pattern(rng, k=6)
    t0 = 0.83
    detector = matched_detector(A, phi, omega, t0)
    r0 = correlation(detector, A, phi, omega, t0)
    assert fires(detector, A, phi, omega, t0, threshold=r0 - 1e-6)
    assert not fires(detector, A, phi, omega, t0, threshold=r0 + 1e-6)
