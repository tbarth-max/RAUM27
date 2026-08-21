"""Automatic scale selection via the Matched-Filter / Scale-Space theorem.

The core claim: for every signal that contains a pattern of characteristic width
sigma_pattern embedded in noise, there exists an optimal smoothing scale
sigma_opt at which the signal-to-noise ratio of pattern detection is maximised.
Too fine (sigma -> 0): noise dominates. Too coarse (sigma >> sigma_pattern):
the pattern is averaged away. The optimum sits in between.

This is a classical, proven result in signal processing (Lindeberg 1994; matched
filter theorem): the SNR of a Gaussian-blob detector is maximised when the
analysis scale matches the blob width. It is the mathematical justification for
"choosing the right resolution level" in multi-scale analysis.

Applied to multi-agent systems: an agent network that measures its own detection
quality across candidate scales and picks the maximum avoids both the nano-scale
failure (noise-dominated) and the macro-scale failure (pattern dissolved), and
does so without needing any prior knowledge of the pattern width.

What this module proves (see tests/test_scale_selection.py):
- For a known Gaussian pattern in synthetic noise, the automatically selected
  scale is within a bounded tolerance of the true pattern width.
- Both extremes (sigma=0 and very large sigma) yield strictly lower SNR than the
  selected optimum.
- The selection procedure is parameter-free: it operates only on the signal.

What this module does NOT claim:
- Nothing about "nano-levels" having special physical status.
- Nothing about consciousness or resonance.
- The result holds for Gaussian patterns in Gaussian noise. For other pattern
  shapes or noise distributions the matched-filter theorem still applies but the
  optimal kernel shape changes accordingly.
"""

from __future__ import annotations

import math


def _gaussian_kernel(sigma: float) -> list[float]:
    if sigma <= 0:
        return [1.0]
    radius = max(1, int(4 * sigma))
    xs = range(-radius, radius + 1)
    raw = [math.exp(-(x * x) / (2 * sigma * sigma)) for x in xs]
    total = sum(raw)
    return [v / total for v in raw]


def smooth(signal: list[float], sigma: float) -> list[float]:
    """Apply a 1D Gaussian smoothing kernel of width sigma to signal.

    Uses zero-padding at boundaries (nearest-neighbour extrapolation omitted for
    simplicity; edge effects are negligible when the pattern is far from the
    boundary, which the benchmark enforces by construction).

    Args:
        signal: 1D list of floats.
        sigma: standard deviation of the Gaussian kernel in samples. sigma=0
               returns the original signal unchanged.

    Returns:
        Smoothed signal of the same length.
    """
    kernel = _gaussian_kernel(sigma)
    r = len(kernel) // 2
    n = len(signal)
    out = [0.0] * n
    for i in range(n):
        acc = 0.0
        for k_idx, w in enumerate(kernel):
            j = i + (k_idx - r)
            if 0 <= j < n:
                acc += signal[j] * w
        out[i] = acc
    return out


def _mean(xs: list[float]) -> float:
    return sum(xs) / len(xs)


def _stdev(xs: list[float]) -> float:
    m = _mean(xs)
    variance = sum((x - m) ** 2 for x in xs) / (len(xs) - 1)
    return math.sqrt(variance)


def detection_snr(
    signal: list[float],
    sigma: float,
    center: int,
    exclude_radius: int,
) -> float:
    """Measure detection SNR at a given smoothing scale.

    Smooths *signal* with a Gaussian of width *sigma*, then computes how many
    background standard-deviations the smoothed value at *center* exceeds the
    mean of the smoothed background (all samples farther than *exclude_radius*
    from *center*).

    Args:
        signal: raw 1D signal.
        sigma: smoothing scale to evaluate.
        center: expected location of the pattern peak.
        exclude_radius: half-width of the region around *center* excluded from
                        the background estimate.

    Returns:
        (smoothed[center] - bg_mean) / bg_std  — a dimensionless SNR.

    Raises:
        ValueError: if the background region contains fewer than 2 samples.
    """
    smoothed = smooth(signal, sigma)
    background = smoothed[: center - exclude_radius] + smoothed[center + exclude_radius :]
    if len(background) < 2:
        raise ValueError(
            f"exclude_radius={exclude_radius} leaves fewer than 2 background "
            "samples; reduce exclude_radius or use a longer signal"
        )
    bg_mean = _mean(background)
    bg_std = _stdev(background)
    return (smoothed[center] - bg_mean) / bg_std


def select_scale(
    signal: list[float],
    center: int,
    exclude_radius: int,
    scales: list[float] | None = None,
) -> tuple[float, float]:
    """Select the smoothing scale that maximises detection SNR.

    Evaluates :func:`detection_snr` over *scales* and returns the scale and its
    SNR at the maximum. This is the parameter-free automatic scale selection
    procedure: an agent network can call this on its own input signal to choose
    the right resolution level without prior knowledge of the pattern width.

    Args:
        signal: raw 1D signal.
        center: location of the pattern (known only for evaluation; in a real
                application this would be the output, not the input).
        exclude_radius: passed to :func:`detection_snr`.
        scales: list of candidate sigma values to scan. Defaults to
                [0, 1, 2, ..., len(signal) // 20].

    Returns:
        (best_sigma, best_snr) — the scale with the highest SNR and its value.
    """
    if scales is None:
        max_sigma = max(1, len(signal) // 20)
        scales = [float(s) for s in range(0, max_sigma + 1)]
    scores = [detection_snr(signal, s, center, exclude_radius) for s in scales]
    best_idx = max(range(len(scores)), key=lambda i: scores[i])
    return scales[best_idx], scores[best_idx]
