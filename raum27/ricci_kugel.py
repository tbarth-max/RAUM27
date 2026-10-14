"""A round sphere under Ricci flow, stopped before radius 0.

Perelman proved the Poincare conjecture with Ricci flow: the metric moves
against its curvature, round spheres shrink, and where a region pinches
towards radius 0 (curvature -> infinity) it is cut out and capped with a
small round piece of positive size -- "surgery" -- and the flow goes on.

For a round n-sphere the flow is exact and rational in the squared radius:

    d(r^2)/dt = -2 (n - 1)    so    r^2(t) = r0^2 - 2 (n - 1) t

It would reach r = 0 at t = r0^2 / (2 (n - 1)). Here it is stopped at the
smallest point of the grid, r = 1/N: the curvature 1/r^2 never exceeds
N^2, the radius never becomes 0, and what is left is a small round cap.

This mirrors one feature of the proof (the singularity is never entered,
it is replaced at a positive scale). It is not a proof of anything: the
conjecture is proved, by Perelman, for every simply connected closed
3-manifold, not just for round spheres.
"""

from fractions import Fraction


def _exact(*values):
    for v in values:
        if isinstance(v, float):
            raise TypeError("exact module: use int or Fraction, not float")
    return [Fraction(v) for v in values]


def shrink_rate(n):
    """d(r^2)/dt of a round n-sphere under Ricci flow: -2 (n - 1)."""
    if n < 2:
        raise ValueError("n >= 2 (a circle does not shrink under Ricci flow)")
    return -2 * (n - 1)


def radius_squared(r0_squared, t, n=3):
    (r0_squared, t) = _exact(r0_squared, t)
    r2 = r0_squared + shrink_rate(n) * t
    if r2 <= 0:
        raise ValueError("past the singularity: radius 0 is never entered")
    return r2


def extinction_time(r0_squared, n=3):
    """When a round sphere would reach radius 0."""
    (r0_squared,) = _exact(r0_squared)
    return r0_squared / -shrink_rate(n)


def surgery_time(r0_squared, resolution, n=3):
    """When the radius reaches the smallest point 1/N -- the flow stops there."""
    (r0_squared,) = _exact(r0_squared)
    floor = Fraction(1, resolution * resolution)
    if r0_squared <= floor:
        raise ValueError("already at the smallest point")
    return (r0_squared - floor) / -shrink_rate(n)


def max_curvature(resolution):
    """Largest curvature 1/r^2 the stopped flow ever shows: N^2."""
    return Fraction(resolution * resolution)
