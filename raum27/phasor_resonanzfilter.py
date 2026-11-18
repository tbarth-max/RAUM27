"""RAUM27 Phasor-Resonanzfilter: a matched filter / correlation detector
over a bank of independently rotating complex phasors.

Grew out of a late-night description ("ein Kreis als Masche um einen
Knoten, Information rotiert als Schwingkreis-Spektrum, ein
Ereignisvektor dockt via Impuls an") that turned out, once made precise,
to be exactly matched-filter theory in the frequency domain (a
correlation receiver) -- applied to a memory made of several
independently-rotating phasors instead of one signal.

The memory state at time t is a vector of K phasors:
    s(t)_k = A_k * exp(i * (omega_k * t + phi_k))
Each entry rotates at its own frequency omega_k. |s(t)| is EXACTLY
CONSTANT over all t (each phasor's own magnitude never changes, only its
phase does) -- that constancy is what makes the rest provable rather
than just empirically observed:

Given a unit detector vector e (|e| = 1), the real correlation
    R(t) = Re[ e^H . s(t) ]   (e^H = conjugate transpose)
satisfies R(t) <= |s(t)| = |s(t0)| for every t, by Cauchy-Schwarz. So
setting e = s(t0)/|s(t0)| (a detector "trained" on one snapshot) makes
t0 a GLOBAL maximum of R(t), not merely a local one -- confirmed here by
scanning R(t) across a wide range of t, not just near t0 (see
test_phasor_resonanzfilter.py).

Two things worth stating precisely rather than leaving implied:

- The match is a MOMENT, not a persistent state. A fixed detector does
  not stay "docked" to a rotating s(t) -- R(t) falls off as t moves away
  from t0, because the phasors keep rotating apart. A system built on
  this needs to keep re-evaluating R(t) over time (exactly what a real
  correlation receiver does), not assume a match, once found, holds.
- Discrimination between two independently-generated patterns, using a
  detector trained on one of them, is a STATISTICAL TENDENCY, not a
  guarantee, and depends heavily on the channel count K. There is a
  concrete, reproducible K=4 example where the detector's OWN pattern
  peak is *lower* than an unrelated pattern's peak -- discrimination is
  not automatic just because two patterns differ (see
  test_small_k_discrimination_can_actually_fail). Measured over 150
  random pattern pairs per K: at K=4 a nonzero fraction fail this way;
  at K=32 the failure rate is lower and the typical (median) margin
  bigger. More channels means more reliable discrimination, but no K
  tested makes it a certainty for a single instance -- the same kind of
  correction this project needed before when an assumed-safe method
  turned out to need a real, measured threshold instead (kern_modul_v2's
  periodicity control test).
"""

from __future__ import annotations

import numpy as np


def state_at(
    amplitudes: np.ndarray, phases: np.ndarray, frequencies: np.ndarray, t: float
) -> np.ndarray:
    """s(t)_k = A_k * exp(i*(omega_k*t + phi_k)) -- a bank of independently
    rotating phasors, one per (amplitude, phase, frequency) triple."""
    return amplitudes * np.exp(1j * (frequencies * t + phases))


def energy(amplitudes: np.ndarray) -> float:
    """|s(t)|^2 = sum(A_k^2), exactly, for every t -- each phasor's own
    magnitude never changes, only its phase does, so the sum of squared
    magnitudes carries no t dependence at all."""
    return float(np.sum(amplitudes**2))


def matched_detector(
    amplitudes: np.ndarray, phases: np.ndarray, frequencies: np.ndarray, t0: float
) -> np.ndarray:
    """The unit vector e = s(t0)/|s(t0)|. By Cauchy-Schwarz, this is the
    unit vector that maximizes Re[e^H . s(t0)] -- "training" the detector
    on a single snapshot of the memory state."""
    snapshot = state_at(amplitudes, phases, frequencies, t0)
    return snapshot / np.linalg.norm(snapshot)


def correlation(
    detector: np.ndarray,
    amplitudes: np.ndarray,
    phases: np.ndarray,
    frequencies: np.ndarray,
    t: float,
) -> float:
    """R(t) = Re[detector^H . s(t)]."""
    return float(np.real(np.vdot(detector, state_at(amplitudes, phases, frequencies, t))))


def fires(
    detector: np.ndarray,
    amplitudes: np.ndarray,
    phases: np.ndarray,
    frequencies: np.ndarray,
    t: float,
    threshold: float,
) -> bool:
    """True iff the correlation at time t reaches the given threshold."""
    return correlation(detector, amplitudes, phases, frequencies, t) >= threshold
