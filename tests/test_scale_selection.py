import math
import random

import pytest

from raum27.scale_selection import detection_snr, select_scale, smooth


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_signal(n=2000, pattern_width=15.0, pattern_amp=3.0, noise_std=2.0, seed=42):
    rng = random.Random(seed)
    center = n // 2
    pattern = [
        pattern_amp * math.exp(-((x - center) ** 2) / (2 * pattern_width ** 2))
        for x in range(n)
    ]
    noise = [rng.gauss(0.0, noise_std) for _ in range(n)]
    return [p + z for p, z in zip(pattern, noise)], center


# ---------------------------------------------------------------------------
# smooth()
# ---------------------------------------------------------------------------

def test_smooth_sigma0_returns_original():
    signal = [1.0, 2.0, 3.0, 2.0, 1.0]
    result = smooth(signal, 0.0)
    assert result == signal


def test_smooth_preserves_length():
    signal = list(range(100))
    for sigma in (0.0, 1.0, 5.0, 20.0):
        assert len(smooth(signal, sigma)) == len(signal)


def test_smooth_flat_signal_unchanged():
    # kernel radius for sigma=10 is 4*10=40; only interior samples are unaffected
    # by zero-padding at boundaries
    signal = [3.14] * 200
    result = smooth(signal, 10.0)
    for v in result[45:155]:
        assert abs(v - 3.14) < 1e-10


def test_smooth_reduces_amplitude_of_spike():
    signal = [0.0] * 50 + [100.0] + [0.0] * 50
    smoothed = smooth(signal, 5.0)
    assert smoothed[50] < 100.0
    assert smoothed[50] > 0.0


# ---------------------------------------------------------------------------
# detection_snr()
# ---------------------------------------------------------------------------

def test_detection_snr_increases_with_amplitude():
    n, center = 500, 250
    exclude_radius = 50
    scales = [10.0]
    signal_weak, _ = _make_signal(n=n, pattern_amp=1.0, noise_std=0.5, seed=1)
    signal_strong, _ = _make_signal(n=n, pattern_amp=5.0, noise_std=0.5, seed=1)
    snr_weak = detection_snr(signal_weak, 10.0, center, exclude_radius)
    snr_strong = detection_snr(signal_strong, 10.0, center, exclude_radius)
    assert snr_strong > snr_weak


def test_detection_snr_raises_on_tiny_exclude_radius():
    signal = list(range(20))
    with pytest.raises(ValueError, match="fewer than 2"):
        detection_snr(signal, 0.0, center=10, exclude_radius=10)


# ---------------------------------------------------------------------------
# select_scale() — the core claim
# ---------------------------------------------------------------------------

def test_selected_scale_near_true_pattern_width():
    """Matched-filter theorem: optimal scale should be close to pattern width."""
    pattern_width = 15.0
    signal, center = _make_signal(pattern_width=pattern_width, seed=42)
    scales = [float(s) for s in range(0, 61, 2)]
    best_sigma, best_snr = select_scale(signal, center, exclude_radius=100, scales=scales)
    tolerance = 10.0  # sigma units — generous, theorem is approximate in finite noise
    assert abs(best_sigma - pattern_width) <= tolerance, (
        f"best_sigma={best_sigma} is more than {tolerance} away from "
        f"true width {pattern_width}"
    )


def test_extremes_are_strictly_worse_than_optimum():
    """Both too-fine (sigma=0) and too-coarse (sigma=55) must be worse than the optimum."""
    signal, center = _make_signal(seed=42)
    scales = [float(s) for s in range(0, 61, 2)]
    _, best_snr = select_scale(signal, center, exclude_radius=100, scales=scales)

    snr_too_fine = detection_snr(signal, 0.0, center, exclude_radius=100)
    snr_too_coarse = detection_snr(signal, 55.0, center, exclude_radius=100)

    assert snr_too_fine < best_snr, (
        f"sigma=0 SNR ({snr_too_fine:.2f}) should be worse than optimum ({best_snr:.2f})"
    )
    assert snr_too_coarse < best_snr, (
        f"sigma=55 SNR ({snr_too_coarse:.2f}) should be worse than optimum ({best_snr:.2f})"
    )


def test_select_scale_default_scales_works():
    signal, center = _make_signal(n=500, pattern_width=8.0, noise_std=1.5, seed=7)
    best_sigma, best_snr = select_scale(signal, center, exclude_radius=40)
    assert best_snr > 0.0


def test_select_scale_different_pattern_widths():
    """Optimal scale should track the true pattern width across a range."""
    for pattern_width in (5.0, 10.0, 20.0, 30.0):
        signal, center = _make_signal(
            n=2000, pattern_width=pattern_width, pattern_amp=4.0, noise_std=1.5, seed=99
        )
        scales = [float(s) for s in range(0, 71, 2)]
        best_sigma, _ = select_scale(signal, center, exclude_radius=80, scales=scales)
        assert abs(best_sigma - pattern_width) <= 15.0, (
            f"pattern_width={pattern_width}: best_sigma={best_sigma} too far off"
        )
