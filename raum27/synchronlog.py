"""Shared synchronisation: a chained delta log, lockstep replay, and worlds that map back to reality.

The construct submitted: one sensor cell (sphere, cube, circle) hands
over the deltas of the measured state; every simulation decides live
what to take over; a real world or a game world -- with real changes --
stays causally consistent and can always be computed back to reality;
all participants stay in sync and can talk to each other, without
producing heaps of data.

Three exact pieces:

- **A chained log.** Each entry carries its delta and the hash of the
  entry before it, so the history cannot be changed unnoticed: altering
  any past delta breaks every hash after it (``append``, ``verify``). This
  is the useful core of a blockchain; between parties who trust each
  other no mining or energy-hungry consensus is needed.
- **Lockstep replay.** Only the deltas travel; every participant computes
  the state itself. This works only if every machine computes exactly
  the same result -- with binary floats different hardware and compilers
  can drift apart and the worlds desynchronise; with exact fractions the
  replay is bit-identical everywhere (``replay``, ``state_digest``).
- **Worlds that map back.** A game world is reality seen through a
  transformation -- here an affine map per value, scaled and shifted by
  exact fractions. As long as the map is invertible, every state of the
  game can be computed back to the real state, exactly (``to_world``,
  ``to_reality``).
"""

import hashlib
from fractions import Fraction

GENESIS = "0" * 64


def _exact(v):
    if isinstance(v, bool) or not isinstance(v, (int, Fraction)):
        raise TypeError("values must be int or Fraction")
    return Fraction(v)


def _encode(delta):
    return ";".join(f"{k}={_exact(v).numerator}/{_exact(v).denominator}" for k, v in sorted(delta.items()))


def append(log, delta):
    """Add a delta; the entry is chained to the previous one by its hash."""
    previous = log[-1]["hash"] if log else GENESIS
    body = _encode(delta)
    digest = hashlib.sha256(f"{previous}|{body}".encode()).hexdigest()
    return log + [{"delta": dict(delta), "previous": previous, "hash": digest}]


def verify(log):
    """Index of the first entry that does not fit the chain, or None if all fit."""
    previous = GENESIS
    for i, entry in enumerate(log):
        expected = hashlib.sha256(f"{previous}|{_encode(entry['delta'])}".encode()).hexdigest()
        if entry["previous"] != previous or entry["hash"] != expected:
            return i
        previous = entry["hash"]
    return None


def replay(log, start=None):
    """Every participant's own computation of the state from the deltas."""
    state = {k: _exact(v) for k, v in (start or {}).items()}
    for entry in log:
        for k, d in entry["delta"].items():
            state[k] = state.get(k, Fraction(0)) + _exact(d)
    return state


def state_digest(state):
    """A fingerprint of a state; equal on every machine that computed the same state."""
    return hashlib.sha256(_encode(state).encode()).hexdigest()


def to_world(state, maps):
    """Reality seen in a world: value -> scale * value + shift for each mapped name."""
    world = {}
    for k, v in state.items():
        scale, shift = maps.get(k, (1, 0))
        scale, shift = _exact(scale), _exact(shift)
        if scale == 0:
            raise ValueError(f"the map for {k!r} is not invertible")
        world[k] = scale * _exact(v) + shift
    return world


def to_reality(world, maps):
    """The world computed back to reality -- exact as long as every map is invertible."""
    reality = {}
    for k, v in world.items():
        scale, shift = maps.get(k, (1, 0))
        scale, shift = _exact(scale), _exact(shift)
        if scale == 0:
            raise ValueError(f"the map for {k!r} is not invertible")
        reality[k] = (_exact(v) - shift) / scale
    return reality
