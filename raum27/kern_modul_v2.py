"""RAUM27 Kern-Modul v2: cube reconstruction from a minimal 2-vector
basis, angular-bisection doubling of a ray grid, TDOA/frequency
consistency, an empirical noise-redundancy check, and a periodicity
finder with a real control test against pure randomness.

Ported from an external Python package ("RAUM27 - Geprüfter Kern",
Stand 26.8.2026) after running every file in it and fixing what didn't
hold up:

- The source calls two 90-degree coordinate rotations "Spiegelungen"
  (reflections/mirrors). A true reflection has determinant -1; both
  maps here have determinant +1 -- they're rotations. Renamed
  accordingly; the underlying vector arithmetic itself was correct.
- Likewise the angular-doubling step (the source's "Doppelspiegelung")
  is a rotation-and-union, not a reflection; renamed to match.
- The source's "two independent systems agree on velocity" test
  computed a wavelength as v_true/f_true and then multiplied it back
  by f_true -- that recovers v_true algebraically for *any* v_true,
  f_true, regardless of any real independent measurement. Kept, but
  labeled for what it is: an identity, not independent confirmation.
- The source's control test against periodicity false-positives on
  pure random data printed a result but asserted nothing about it --
  it could not fail no matter what came out. Fixed here with a real
  threshold assertion (see false_positive_counts / its test).

Left out (not ported): the LED/hex-color demo scaffolding and the
"live" noise-reduction wrapper around it. Both ran without error but
don't carry an independent checkable claim beyond what the redundancy
check below already covers -- they're UI/demo plumbing, not verified
math.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import product
from typing import Tuple

import numpy as np

Vector3 = Tuple[int, int, int]

VECTOR_X: Vector3 = (1, 0, 0)
VECTOR_Y: Vector3 = (0, 1, 0)


def rotate_about_x(v: Vector3) -> Vector3:
    """90-degree rotation about the x-axis: (x,y,z) -> (x,-z,y).
    Determinant +1 -- a rotation, not a reflection."""
    x, y, z = v
    return (x, -z, y)


def rotate_about_y(v: Vector3) -> Vector3:
    """90-degree rotation about the y-axis: (x,y,z) -> (z,y,-x).
    Determinant +1, likewise a rotation."""
    x, y, z = v
    return (z, y, -x)


def reconstruct_face_directions() -> set[Vector3]:
    """The 6 cube face directions, generated from 2 starting vectors and
    2 rotations plus negation -- no information beyond those 2 vectors
    and the two rotation rules."""
    basis = {VECTOR_X, VECTOR_Y}
    basis |= {rotate_about_x(v) for v in (VECTOR_X, VECTOR_Y)}
    basis |= {rotate_about_y(v) for v in (VECTOR_X, VECTOR_Y)}
    negated = {tuple(-k for k in v) for v in basis}
    return basis | negated


def reconstruct_corners(faces: set[Vector3]) -> set[Vector3]:
    """All 8 cube corners as sums of one choice from each of the 3 axis pairs."""
    axis_groups = [
        [v for v in faces if v[0] != 0],
        [v for v in faces if v[1] != 0],
        [v for v in faces if v[2] != 0],
    ]
    corners = set()
    for vx, vy, vz in product(*axis_groups):
        corners.add(tuple(a + b + c for a, b, c in zip(vx, vy, vz)))
    return corners


def initial_rays() -> list[float]:
    """4 axis directions (0/45/90/135 degrees) give 8 evenly spaced rays."""
    directions = [0, 45, 90, 135]
    return sorted({(a + offset) % 360 for a in directions for offset in (0, 180)})


def bisect_rays(rays: list[float]) -> list[float]:
    """Doubles the ray count by inserting a new ray at the midpoint of
    every gap: rotate the whole set by half the current spacing, union
    with the original. A finite, explicit construction -- it only grows
    for as many times as this is called, no accumulating state."""
    spacing = 360 / len(rays)
    shifted = [(r + spacing / 2) % 360 for r in rays]
    return sorted(set(rays + shifted))


def is_evenly_spaced(rays: list[float], tolerance: float = 1e-9) -> bool:
    ordered = sorted(rays)
    gaps = [(ordered[(i + 1) % len(ordered)] - ordered[i]) % 360 for i in range(len(ordered))]
    return all(abs(g - gaps[0]) < tolerance for g in gaps)


def tdoa_position(L: Fraction, v: Fraction, dt: Fraction) -> Fraction:
    """Time-difference-of-arrival source position: x = (L - v*dt) / 2."""
    return (L - v * dt) / 2


def wavelength_from_velocity_and_frequency(v: Fraction, frequency: Fraction) -> Fraction:
    return v / frequency


def velocity_from_wavelength_and_frequency(wavelength: Fraction, frequency: Fraction) -> Fraction:
    """v = wavelength * frequency. Composed with
    wavelength_from_velocity_and_frequency, this recovers the original v
    for *any* v and frequency -- an algebraic identity (v/f)*f = v, not
    independent confirmation from two separate measurement systems."""
    return wavelength * frequency


def redundancy_corrected_reading(x_true: float, noise: float, rng: np.random.Generator) -> float:
    """One noisy axis: independently noisy X and 1/X readings, rescaled
    using the known constraint X*(1/X)=1."""
    x_noisy = x_true + rng.normal(0, noise)
    invx_noisy = 1 / x_true + rng.normal(0, noise)
    product = x_noisy * invx_noisy
    correction = 1 / np.sqrt(abs(product))
    return x_noisy * correction


def averaged_reading(x_true: float, noise: float, n_axes: int, rng: np.random.Generator) -> float:
    return float(np.mean([redundancy_corrected_reading(x_true, noise, rng) for _ in range(n_axes)]))


def find_period(series: np.ndarray, max_period: int = 20) -> int:
    """Best-guess period via raw autocorrelation argmax over lags
    2..max_period. A coarse tool -- see kern_modul_v1 / cube_projection
    for the point that a proper spectral (FFT) analysis is the correct
    tool when the period must be pinned down precisely."""
    centered = np.asarray(series) - np.mean(series)
    autocorr = np.correlate(centered, centered, mode="full")
    autocorr = autocorr[len(autocorr) // 2:]
    if len(autocorr) < 4:
        return -1
    return int(np.argmax(autocorr[2:max_period]) + 2)


def false_positive_counts(rng: np.random.Generator, trials: int = 200,
                           series_len: int = 60, max_period: int = 20) -> Counter:
    """Runs find_period on pure random (period-free) data `trials` times
    and counts how often each candidate period "won". Used to check the
    method isn't quietly biased toward reporting one period as real."""
    found = []
    for _ in range(trials):
        series = rng.uniform(-1, 1, series_len)
        found.append(find_period(series, max_period))
    return Counter(found)
