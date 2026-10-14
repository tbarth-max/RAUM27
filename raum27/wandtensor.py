"""The wall tensor T(DX) from ``raum27_wandneigung_tensor.py``, checked.

    T(DX) = [[2/6 DX^2, 1/6 DX^2],
             [1/2 DX,   1/2 DX  ]]

acts on the curvature pair (f_start, f_end) of one piece of length DX and
gives the extra sag and the turn of the slope:

    w'     = w + DX * theta + DX^2 (2 f_start + f_end) / 6
    theta' = theta + DX (f_start + f_end) / 2

This is the exact step for curvature that is linear on the piece. A
cantilever with an end load has linear curvature, so the chain hits the
bending line with error 0 at every node. For curvature of degree 2 (a
uniform load) it is no longer exact; the middle reading of
``biegelinie.three_point_chain`` closes that gap. det T = DX^3 / 12, so
two successive states give the two curvatures back exactly.

Left out on purpose: the "zero-layer contact contract" of the same file.
Built from the tensor, its condition (central moment = field moment +
overhang moment) holds by algebra for every input, so it checks nothing;
and the trust layer waits for the first trial run anyway.
"""

from fractions import Fraction


def _exact(*values):
    for v in values:
        if isinstance(v, float):
            raise TypeError("exact module: use int or Fraction, not float")
    return [Fraction(v) for v in values]


def matrix(dx):
    (dx,) = _exact(dx)
    if dx <= 0:
        raise ValueError("DX must be positive")
    return ((Fraction(2, 6) * dx * dx, Fraction(1, 6) * dx * dx),
            (dx / 2, dx / 2))


def determinant(dx):
    (a, b), (c, d) = matrix(dx)
    return a * d - b * c


def step(w, theta, f_start, f_end, dx):
    """One piece: (w, theta) -> (w', theta') with the wall tensor."""
    w, theta, f_start, f_end = _exact(w, theta, f_start, f_end)
    (a, b), (c, d) = matrix(dx)
    dx = Fraction(dx)
    return w + theta * dx + a * f_start + b * f_end, theta + c * f_start + d * f_end


def recover(w, theta, w_next, theta_next, dx):
    """The two curvatures (f_start, f_end) that turned one state into the next."""
    w, theta, w_next, theta_next = _exact(w, theta, w_next, theta_next)
    (a, b), (c, d) = matrix(dx)
    sag = w_next - (w + theta * Fraction(dx))
    turn = theta_next - theta
    det = a * d - b * c
    return (d * sag - b * turn) / det, (-c * sag + a * turn) / det


def chain(curvature, length, pieces):
    """Bending line from the wall tensor, clamped at x = 0: [(x, w), ...]."""
    if pieces < 1:
        raise ValueError("at least one piece is needed")
    h = Fraction(length) / pieces
    w = theta = Fraction(0)
    points = [(Fraction(0), w)]
    for i in range(pieces):
        w, theta = step(w, theta, curvature(i * h), curvature((i + 1) * h), h)
        points.append(((i + 1) * h, w))
    return points


def nine_steps():
    """The nine fractions 1 - k/9 as curvature ramp, DX = 1/9: (k, w, denominator)."""
    w = theta = Fraction(0)
    rows = []
    for k in range(1, 10):
        w, theta = step(w, theta, Fraction(10 - k, 9), Fraction(9 - k, 9), Fraction(1, 9))
        rows.append((k, w, w.denominator))
    return rows
