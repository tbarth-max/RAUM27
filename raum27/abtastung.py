"""Scanning against a stored hologram: keep the deltas, accept only what is recognised.

The procedure submitted:

1. Take a picture of the current state -- the hologram -- and store it.
2. Let only scanning impulses run through; the system deflects them,
   they do not change it.
3. Wherever a scan differs from the stored state, there is a delta.
4. If the delta pattern is recognised **uniquely**, take it over into
   the internal state. If not -- unknown or ambiguous -- route it to a
   second store for analytical processing instead.

A state is a mapping ``(plane, circle, direction) -> value`` with
directions 1..8 around each circle. Only non-zero differences are kept
(``scan``), so storage scales with what changed, not with the size of the
system. Applying and reverting deltas is exact (``apply`` / ``revert``),
the same delta log as in ``raum27.zustandsmaschine``.

Recognition works per circle on the eight-direction ring. Two delta
patterns count as the same pattern when one of the eight symmetries of
the ring -- four turns by 90 degrees and four mirrorings -- carries one
onto the other, so a pattern is recognised in any orientation
(``canonical``). A pattern is accepted only when it matches exactly one
entry of the library; no match and several matches both go to analysis.
That rule is what keeps the internal state free of guesses.

What this does not decide: whether most deltas really are zero. The
saving is ``1 - stored / scanned`` (``storage_ratio``) and depends on the
object scanned, not on the method.
"""

from fractions import Fraction

RING = 8


def _exact(value):
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError(f"state values must be int or Fraction, got {type(value).__name__}")
    return value


def snapshot(state):
    """The hologram: an independent copy of the state, values checked exact."""
    return {key: _exact(value) for key, value in state.items()}


def scan(reference, observed):
    """Non-zero differences ``observed - reference`` over the union of keys."""
    deltas = {}
    for key in reference.keys() | observed.keys():
        difference = _exact(observed.get(key, 0)) - _exact(reference.get(key, 0))
        if difference:
            deltas[key] = difference
    return deltas


def apply(state, deltas):
    """State plus deltas; entries that reach zero are dropped."""
    result = dict(state)
    for key, difference in deltas.items():
        value = result.get(key, 0) + difference
        if value:
            result[key] = value
        else:
            result.pop(key, None)
    return result


def revert(state, deltas):
    """Undo ``apply``."""
    return apply(state, {key: -difference for key, difference in deltas.items()})


def ring_symmetries():
    """The eight symmetries of the eight-direction ring, as index maps."""
    turns = [[(i + 2 * k) % RING for i in range(RING)] for k in range(4)]
    mirrors = [[(2 * k - i) % RING for i in range(RING)] for k in range(4)]
    return turns + mirrors


def canonical(pattern):
    """Orientation-free form of an eight-direction pattern (tuple of 8 values)."""
    if len(pattern) != RING:
        raise ValueError(f"a ring pattern has {RING} entries, got {len(pattern)}")
    images = []
    for symmetry in ring_symmetries():
        image = [0] * RING
        for i, value in enumerate(pattern):
            image[symmetry[i]] = value
        images.append(tuple(image))
    return min(images)


def ring_patterns(deltas):
    """Group deltas by (plane, circle) into eight-direction patterns."""
    rings = {}
    for (plane, circle, direction), difference in deltas.items():
        if not 1 <= direction <= RING:
            raise ValueError(f"direction {direction} is not in 1..{RING}")
        rings.setdefault((plane, circle), [0] * RING)[direction - 1] = difference
    return {key: tuple(pattern) for key, pattern in rings.items()}


def recognise(pattern, library):
    """Labels in ``library`` (label -> pattern) matching ``pattern`` in any orientation."""
    form = canonical(pattern)
    return sorted(label for label, known in library.items() if canonical(known) == form)


def process(state, observed, library):
    """One scanning pass.

    Returns ``(new_state, accepted, analysis)``: ``accepted`` maps each
    uniquely recognised ring to its label and has been applied;
    ``analysis`` maps every other changed ring to its candidate labels
    (empty: unknown, several: ambiguous) and has not been applied.
    """
    deltas = scan(state, observed)
    accepted, analysis, taken = {}, {}, {}
    for ring, pattern in ring_patterns(deltas).items():
        labels = recognise(pattern, library)
        if len(labels) == 1:
            accepted[ring] = labels[0]
            for direction, difference in enumerate(pattern, start=1):
                if difference:
                    taken[ring + (direction,)] = difference
        else:
            analysis[ring] = labels
    return apply(state, taken), accepted, analysis


def storage_ratio(deltas, scanned):
    """Share of scanned values that had to be stored."""
    if scanned <= 0:
        raise ValueError("at least one value must have been scanned")
    return Fraction(len(deltas), scanned)
