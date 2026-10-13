"""Three-instance consensus: A and B compute, C in the centre checks one value.

The rule submitted: two instances, A and B, do the work; the central
instance C needs only one value to know both computed correctly, because
over the moments and fields the result must close back to 1 -- to C's
own place in the centre.

Two exact forms of "closing back to 1":

- **Inversion pair.** A computes a quantity, B computes its mirror
  (the inverse) on its own path; C checks a * b == 1 (``inverse_check``).
- **Moment balance.** A delivers the weights (forces, masses, field
  strengths), B delivers where they act; C checks that the moments about
  its own position cancel, i.e. the balance point is the centre
  (``moment_check``). This is the diagonal screw rule in measuring form:
  balanced about the middle, nothing tips.

``consensus`` accepts a result only if C's check closes exactly; anything
else is refused with its reason and goes to manual work, as in
``raum27.abtastung`` and ``raum27.kaskade`` -- C never picks one of two
disagreeing answers.

**The condition without which this proves nothing: A and B must be
independent.** If B is derived from A -- B = 1/A computed from A's output
-- then a * b == 1 holds whatever A got wrong; the check closes on a
wrong answer. The tests pin exactly that failure. B has to reach its
value by its own route (its own data, the mirrored stream, a different
method), and even then errors that both routes share are not caught.
This is the known limit of N-version computing: agreement measures
independence as much as correctness.
"""

from fractions import Fraction


def _exact(v):
    if isinstance(v, bool) or not isinstance(v, (int, Fraction)):
        raise TypeError("values must be int or Fraction")
    return Fraction(v)


def inverse_check(a, b):
    """C's one value for an inversion pair: a * b (closes when it is 1)."""
    return _exact(a) * _exact(b)


def balance_point(weights, positions):
    """Where the weights balance: sum(w p) / sum(w), exact."""
    weights = [_exact(w) for w in weights]
    total = sum(weights)
    if total == 0 or len(weights) != len(positions):
        raise ValueError("weights must match positions and must not sum to zero")
    dims = len(positions[0])
    return tuple(sum(w * _exact(p[i]) for w, p in zip(weights, positions)) / total for i in range(dims))


def moment_check(weights, positions, centre):
    """C's one value for a moment balance: total moment about the centre (closes when zero)."""
    weights = [_exact(w) for w in weights]
    dims = len(centre)
    return tuple(sum(w * (_exact(p[i]) - _exact(centre[i])) for w, p in zip(weights, positions))
                 for i in range(dims))


def locate_from_poles(plus_squared, minus_squared, pole=1):
    """Where C stands, from the plus side and the minus side of each axis.

    Instance A measures the squared distance to the plus pole of each axis
    (north, east, front), instance B to the minus pole (south, west, back);
    poles at +-``pole``. Since |P - (+R e)|^2 - |P - (-R e)|^2 = -4 R p_e,
    each axis gives C's coordinate exactly: p_e = (minus - plus) / (4 R).

    One axis pair alone fixes only the plane where both distances are equal
    -- on the sphere, the equator circle; two pairs fix a line; all three
    fix the point. Returns C's position as a tuple of Fractions.
    """
    pole = _exact(pole)
    if pole == 0:
        raise ValueError("the poles must be apart")
    if len(plus_squared) != len(minus_squared):
        raise ValueError("every axis needs a plus and a minus distance")
    return tuple((_exact(m) - _exact(p)) / (4 * pole) for p, m in zip(plus_squared, minus_squared))


def consensus(a, b, rule="inverse", centre=None):
    """Accept A's result only if C's single check closes exactly.

    ``rule='inverse'``: ``a`` and ``b`` are numbers, closes when a * b == 1.
    ``rule='moment'``: ``a`` are weights, ``b`` positions, closes when the
    moment about ``centre`` is zero.
    ``rule='poles'``: ``a`` squared distances to the plus poles, ``b`` to the
    minus poles; closes when they meet in ``centre`` (default the origin).
    Returns ``(accepted, value_or_reason)``.
    """
    if rule == "inverse":
        product = inverse_check(a, b)
        if product == 1:
            return True, _exact(a)
        return False, f"does not close: a * b = {product}"
    if rule == "poles":
        position = locate_from_poles(a, b)
        target = tuple(_exact(c) for c in (centre if centre is not None else (0,) * len(position)))
        if position == target:
            return True, position
        return False, "does not close: plus and minus meet at (" + ", ".join(str(c) for c in position) + ")"
    if rule == "moment":
        if centre is None:
            raise ValueError("a moment check needs C's centre")
        moment = moment_check(a, b, centre)
        if all(m == 0 for m in moment):
            return True, tuple(_exact(c) for c in centre)
        return False, f"does not close: moment {moment}"
    raise ValueError(f"unknown rule {rule!r}")
