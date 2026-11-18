"""The boundary circle: guard only the edge, roll back when it tears.

The idea submitted: if the system is built so that it cannot break from
inside -- the 10 is out of reach, nothing goes beyond 9 -- then there is no
need to watch everything. One last circle drawn around the system is
enough: if it is crossed, intervene at once. The place is known at once,
and because the computation runs forwards and backwards, it can be reset
to the last safe state if something fatal happens.

Here a state maps names to exact values; it changes only by deltas. The
guard applies each delta, checks the one boundary rule (every value
within the circle) and, if the circle is crossed, does not let the step
stand: the state returns to the last safe state, and the event records
the step and **where** the circle was crossed (``guarded_run``). Every
accepted step is undone exactly by its inverse delta (``rewind``).

Two limits are stated, not hidden:

- Guarding only the edge is complete only if every disturbance has to
  cross the edge. The inner rule (no wheel beyond 9, as in
  ``raum27.zahnwerk``) protects the *model*; a part of real hardware can
  still fail inside, and the edge will not see that.
- Rolling back is exact for the computation and its record. In the
  physical world it means returning to a safe state, not undoing what
  happened.
"""

from fractions import Fraction


def _exact(v):
    if isinstance(v, bool) or not isinstance(v, (int, Fraction)):
        raise TypeError("values must be int or Fraction")
    return Fraction(v)


def inside(state, limit):
    """True when every value lies within the circle |v| < limit."""
    limit = _exact(limit)
    return all(abs(v) < limit for v in state.values())


def crossings(state, limit):
    """Names of the values that lie on or beyond the circle -- the place of the tear."""
    limit = _exact(limit)
    return sorted(k for k, v in state.items() if abs(v) >= limit)


def apply(state, delta):
    result = dict(state)
    for key, d in delta.items():
        result[key] = result.get(key, Fraction(0)) + _exact(d)
    return result


def guarded_run(initial, deltas, limit=10):
    """Apply deltas; a step that crosses the circle is rolled back and reported.

    Returns (final state, accepted deltas, events); each event is
    (step index, names where the circle was crossed).
    """
    state = {k: _exact(v) for k, v in initial.items()}
    if not inside(state, limit):
        raise ValueError("the start already lies outside the circle")
    accepted, events = [], []
    for i, delta in enumerate(deltas):
        trial = apply(state, delta)
        if inside(trial, limit):
            state = trial
            accepted.append(delta)
        else:
            events.append((i, crossings(trial, limit)))
    return state, accepted, events


def rewind(state, accepted):
    """Undo accepted deltas in reverse order -- back to the start, exactly."""
    for delta in reversed(accepted):
        state = apply(state, {k: -_exact(d) for k, d in delta.items()})
    return state
