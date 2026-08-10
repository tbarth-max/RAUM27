"""Phase synchronization between two periodic signals (a phase detector).

Two "pointers" sweep a circle at frequencies f1, f2: theta(t) = 2*pi*f*t.
They're "synchronized" when their phase angles coincide (mod 2*pi, within
a tolerance). At equal frequency this is either always true (equal phase)
or never true (mod tolerance) -- equal frequency alone doesn't create
periodic coincidences. At different frequencies, synchronization recurs
periodically at the beat period 1/|f1-f2|, the same beat-frequency result
used throughout acoustics and radio (two near-identical tones "beating"
against each other; a phase-locked loop's phase detector).
"""

from __future__ import annotations

import math


def phase_angle(t: float, frequency: float, phase: float = 0.0) -> float:
    """theta(t) = 2*pi*f*t + phase, not reduced mod 2*pi."""
    return 2 * math.pi * frequency * t + phase


def phase_difference(theta1: float, theta2: float) -> float:
    """Shortest angular distance between two phase angles, in [0, pi]."""
    d = (theta1 - theta2) % (2 * math.pi)
    return min(d, 2 * math.pi - d)


def is_synchronized(
    t: float,
    f1: float,
    f2: float,
    phi1: float = 0.0,
    phi2: float = 0.0,
    tolerance: float = 0.05,
) -> bool:
    """True iff the two phase angles at time t coincide within `tolerance`."""
    theta1 = phase_angle(t, f1, phi1)
    theta2 = phase_angle(t, f2, phi2)
    return phase_difference(theta1, theta2) < tolerance


def beat_period(f1: float, f2: float) -> float:
    """Time between successive synchronization events, for f1 != f2."""
    if f1 == f2:
        raise ValueError("beat_period is undefined for f1 == f2 (never repeats or always synced)")
    return 1.0 / abs(f1 - f2)
