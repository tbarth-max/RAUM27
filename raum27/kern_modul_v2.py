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

A second, independently-written "kern_modul_v2" was later submitted for
the same package, claiming "Alle 133 Tests bestanden". Running it as-is
falsifies that claim on the first attempt: its NegativraumTensor class
computes ueberlagerung = welle + (-welle), which is identically 0 for
every input by construction, yet its own test asserts the resulting
"Spannung" is positive -- a deterministic, 100%-reproducible failure, not
an occasional bad seed (checked directly: 5/5 random trials give exactly
0.0). Dropped entirely, along with its Kompressionskreis helpers
(reziprokes_label, verhaeltnis_zweier_treffer,
kompression_nach_n_wuerfeln), which are bare wrappers around division
and exponentiation with no independent claim attached -- and the
"133 Tests" line itself, which is that submission's own 8-function test
count reporting a number copied from this repo's unrelated whole-suite
pytest total. Its Minimalrekonstruktion/Doppelspiegelung/Resonanzmodell
sections duplicate rotate_about_x/bisect_rays/tdoa_position above under
German names with no new content, and its periodicity-control
reimplementation duplicates false_positive_counts below (feeding it a
lottery-hit-pair encoding instead of a raw series -- same detector,
different cosmetic input).

One piece of that submission held up and is ported below:
redundancy_state/redundancy_deviation. Its own version used floats and
an under-tested "monotonic" claim checked at exactly two points; redone
here in exact Fraction arithmetic and checked on a full grid instead
(see its docstring and tests/test_kern_modul_v2.py for exactly what
was verified and what was NOT -- a symmetry generalization to an
arbitrary reference point was tried and found FALSE by direct
counterexample, so the claim below stays scoped to the one reference
point (1) it was actually proven for).

The remaining files in the original package were then checked too:

- raum27_delta_mustererkennung.py: its core ([x, 1/x, x*(1/x)] delta) is
  the same construction as redundancy_state/redundancy_deviation above
  (confirms the port was based on the right source), its TDOA class is
  the same tdoa_position formula with a constant axis-offset added (not
  independently new), and it ends in the same hex-color demo pattern as
  the LED file -- all three already accounted for above.
- raum27_led_sensor.py: runs cleanly, but "zustand_als_zahl" (frequency x
  brightness x (1 + morse-code weight)) is an arbitrary made-up formula
  with no geometric grounding and nothing to falsify. Left out.
- raum27_live_kompakt.py: same hex-demo pattern, but it also carries a
  real claim worth keeping: averaging 8 independent noisy redundancy
  readings should cut the mean error by about sqrt(8)=2.828 (ordinary
  statistics: standard error falls off as sqrt(n) for n i.i.d. samples).
  The source measured 2.572 in one 500-trial run and stopped there.
  Re-measured against this module's own redundancy_corrected_reading /
  averaged_reading across 4 seeds x 400 trials each: 2.61-2.88 -- 2.572
  was just one noisy sample of a real effect, not a discrepancy. Added as
  test_averaging_eight_axes_reduces_noise_by_roughly_sqrt_eight.
- raum27_kompressionskreis.py, listed in the package's own status table,
  was never actually present in the files that were pasted -- it isn't
  ported here because there is nothing to verify.
- The three Lean files that passed the bracket-balance check
  (RAUM27_Kern.lean, RAUM27_Wuerfelsymmetrie.lean,
  RAUM27_Resonanzauslese.lean) contain no `sorry` and no circular proofs.
  RAUM27_Wuerfelsymmetrie's corner-reflection claims and
  RAUM27_Resonanzauslese's TDOA/velocity/period theorems check out
  algebraically. One naming overreach in RAUM27_Kern.lean:
  `wave_resonance_left_right` sounds like a general law but its own
  hypothesis fixes n.val = 1; substituting n.val = 2 into the same
  formula gives (2*16/9)*(2*9/16) = 4, not 1. The Lean statement itself
  is honest about the restriction (the hypothesis is right there), but
  the name oversells a trivial special case as a general resonance
  effect. Not ported -- kern_modul_v1/v2 don't need it, and there's no
  general version of the claim to port.
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


def reflections_needed_for_full_circle(arc_fraction_denominator: int) -> float:
    """How many doublings of bisect_rays it takes to go from a single arc
    of 360/denominator degrees to a full 360-degree circle:
    log2(denominator). E.g. a quarter arc (denominator=4) needs 2
    doublings, an eighth arc needs 3 -- the same doubling this module
    already implements in bisect_rays, made explicit as a plain formula.
    Real, standard group theory (dihedral group reflection generation),
    not new math -- just spelled out precisely since it came up again in
    a submission that treated it as freshly discovered."""
    import math

    return math.log2(arc_fraction_denominator)


def central_inversion_angle(theta_degrees: float) -> float:
    """The angle you get by reflecting a point at theta_degrees THROUGH
    THE CENTER (point inversion, v -> -v): theta + 180, mod 360.
    Concretely, central_inversion_angle(90) == 270 -- if central
    inversion is already an available operation, 270 degrees doesn't need
    its own independent state; it's derived from 90."""
    return (theta_degrees + 180) % 360


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


def redundancy_state(x: Fraction) -> Tuple[Fraction, Fraction, Fraction]:
    """[x, 1/x, x*(1/x)]. The third slot is exactly Fraction(1) for any
    x != 0 -- proven, not just tested, since Fraction division is exact.
    (A float version of this same triple can fail to hit 1.0 exactly,
    e.g. x=1.618: 1.618 * (1/1.618) == 0.9999999999999999 in float64 --
    one more reason this is done in Fraction, not float.)"""
    inv = 1 / x
    return (x, inv, x * inv)


def redundancy_deviation(x: Fraction, reference: Fraction = Fraction(1)) -> Fraction:
    """Squared distance between redundancy_state(x) and redundancy_state(reference),
    restricted to the two slots that can actually vary -- the third slot
    is always 1 for both, by redundancy_state's own guarantee, so it
    never contributes and is left out rather than computed and discarded.

    Proven (see tests/test_kern_modul_v2.py) for reference == 1 only:
    strictly increasing as x moves away from 1 through (1, infinity), and
    strictly increasing as x moves away from 1 through (0, 1] towards 0.
    Also exactly symmetric under x -> 1/x, e.g. deviation(2) == deviation(1/2)
    -- so it is NOT a monotonic function of |x - reference| (2 and 1/2 are
    at different distances from 1 but give the same value). A guess that
    this symmetry generalizes to deviation(x, r) == deviation(r*r/x, r) for
    an arbitrary reference r was checked and found FALSE by counterexample,
    so no claim is made here for reference != 1."""
    return (x - reference) ** 2 + (1 / x - 1 / reference) ** 2
