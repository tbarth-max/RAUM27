"""Bending lines from chained circular arcs, checked against engineering mechanics.

The model submitted: cut the beam into pieces ``dx`` (the wavelength,
the connection along the beam); give each piece its own bending radius
(the frequency of the piece is its curvature ``1/r``); set the arcs end
to end -- geometry instead of integration.

Mechanics supplies the curvature: ``kappa(x) = M(x) / EI``, bending
moment over bending stiffness. Two chains are provided:

- ``arc_chain`` sets true circular arcs end to end. It is geometrically
  exact for any size of deflection; only the piece length limits it.
- ``slope_chain`` is the same idea for small deflections in exact
  rational arithmetic: the slope turns by ``kappa * dx`` per piece and
  the height follows the mean slope of the piece.

For a beam on two supports the starting slope is not known in advance;
the chain is started flat and then turned rigidly so that it ends on the
far support (``supported``). Turning a whole chain changes no arc, so
this is still pure geometry.

Reading each piece's curvature at three points -- start, middle, end --
instead of one makes the chain **exact** (``three_point_chain``): for
curvature that is a polynomial of degree at most 2 on each piece, which
covers all three textbook cases, every piece end lies exactly on the
bending line, for any number of pieces. A kink inside a piece (a point
load not on a piece boundary) breaks this; put the boundaries on the
load points.

Measured against the closed forms (cantilever ``PL^3/3EI``, centre load
``PL^3/48EI``, uniform load ``5qL^4/384EI``) the error falls with the
square of the number of pieces for the one-point chains; ``pieces_for_tolerance`` doubles the
count until two results agree to the tolerance asked for.

Load duration enters through the dynamic amplification of a rectangular
load pulse on an undamped oscillator (``dynamic_amplification``): a load
held for at least half a natural period, including a permanent load put
on suddenly, deflects **twice** as far as the same load applied slowly.
A slowly applied permanent load -- the standing test -- has factor 1.
"""

import math
from fractions import Fraction


def arc_chain(curvature, length, pieces, start_slope=0.0):
    """Points of the bending line built from ``pieces`` circular arcs.

    ``curvature(x)`` is evaluated at the middle of each piece.
    """
    if pieces < 1:
        raise ValueError("at least one piece is needed")
    h = length / pieces
    x = y = 0.0
    phi = start_slope
    points = [(x, y)]
    for i in range(pieces):
        k = curvature((i + 0.5) * h)
        turn = k * h
        chord = h if turn == 0 else 2 * math.sin(turn / 2) / k
        x += chord * math.cos(phi + turn / 2)
        y += chord * math.sin(phi + turn / 2)
        phi += turn
        points.append((x, y))
    return points


def slope_chain(curvature, length, pieces):
    """Small-deflection bending line in exact arithmetic: (x, w) per piece end."""
    if pieces < 1:
        raise ValueError("at least one piece is needed")
    h = Fraction(length) / pieces
    slope, w = Fraction(0), Fraction(0)
    points = [(Fraction(0), w)]
    for i in range(pieces):
        new_slope = slope + Fraction(curvature((i + Fraction(1, 2)) * h)) * h
        w += h * (slope + new_slope) / 2
        slope = new_slope
        points.append(((i + 1) * h, w))
    return points


def three_point_chain(curvature, length, pieces):
    """Like ``slope_chain``, but each piece reads its curvature at start, middle and end.

    Slope turns by ``h (k0 + 4 km + k1) / 6`` and the height rises by
    ``h * slope + h^2 (k0 + 2 km) / 6``. For curvature that is a
    polynomial of degree at most 2 on each piece -- every textbook case
    below -- this is not an approximation: the chain hits the bending
    line exactly at every piece end, for any number of pieces.
    """
    if pieces < 1:
        raise ValueError("at least one piece is needed")
    h = Fraction(length) / pieces
    slope, w = Fraction(0), Fraction(0)
    points = [(Fraction(0), w)]
    for i in range(pieces):
        k0 = Fraction(curvature(i * h))
        km = Fraction(curvature((i + Fraction(1, 2)) * h))
        k1 = Fraction(curvature((i + 1) * h))
        w += h * slope + h * h * (k0 + 2 * km) / 6
        slope += h * (k0 + 4 * km + k1) / 6
        points.append(((i + 1) * h, w))
    return points


def supported(points):
    """Turn a chain rigidly so that it ends on the line of its first point."""
    (x0, y0), (x1, y1) = points[0], points[-1]
    angle = math.atan2(y1 - y0, x1 - x0)
    c, s = math.cos(-angle), math.sin(-angle)
    return [(x0 + (x - x0) * c - (y - y0) * s, y0 + (x - x0) * s + (y - y0) * c) for x, y in points]


def supported_exact(points):
    """Small-deflection version of ``supported``: subtract the chord line exactly."""
    (x0, w0), (x1, w1) = points[0], points[-1]
    return [(x, w - w0 - (w1 - w0) * (x - x0) / (x1 - x0)) for x, w in points]


# --- the three textbook cases: curvature from M / EI, and the closed form ---

def cantilever_end_load(P, L, EI):
    """Fixed at x = 0, load P at the free end. Returns (curvature, tip deflection)."""
    return (lambda x: P * (L - x) / EI), P * L ** 3 / (3 * EI)


def centre_load(P, L, EI):
    """Two supports, load P in the middle. Returns (curvature, deflection at mid-span)."""
    return (lambda x: P * min(x, L - x) / (2 * EI)), P * L ** 3 / (48 * EI)


def uniform_load(q, L, EI):
    """Two supports, load q per length. Returns (curvature, deflection at mid-span)."""
    return (lambda x: q * x * (L - x) / (2 * EI)), 5 * q * L ** 4 / (384 * EI)


def deflection_at(points, x_target):
    """Height of the chain at the piece end nearest to ``x_target``."""
    return min(points, key=lambda p: abs(p[0] - x_target))[1]


def pieces_for_tolerance(compute, tolerance, start=2, limit=1 << 16):
    """Double the piece count until two successive results differ by less than ``tolerance``."""
    n, previous = start, compute(start)
    while n < limit:
        n *= 2
        current = compute(n)
        if abs(current - previous) < tolerance:
            return n, current
        previous = current
    raise ValueError(f"no agreement to {tolerance} within {limit} pieces")


def dynamic_amplification(duration_over_period):
    """Peak deflection over static deflection for a rectangular load pulse.

    Undamped single oscillator, load switched on and off instantly.
    ``inf`` stands for a permanent load put on suddenly.
    """
    ratio = duration_over_period
    if ratio <= 0:
        raise ValueError("the load must act for a positive time")
    if ratio >= Fraction(1, 2):
        return 2
    return 2 * math.sin(math.pi * ratio)
