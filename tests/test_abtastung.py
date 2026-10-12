"""Tests for raum27.abtastung: scanning against a stored hologram."""

from fractions import Fraction
import random

import pytest

from raum27.abtastung import (
    apply,
    canonical,
    process,
    recognise,
    revert,
    ring_patterns,
    ring_symmetries,
    scan,
    snapshot,
    storage_ratio,
)


def _state(n_circles=20, seed=0):
    rng = random.Random(seed)
    return {(p, c, d): rng.randint(1, 255)
            for p in range(3) for c in range(1, n_circles + 1) for d in range(1, 9)}


def test_snapshot_is_independent_and_exact():
    state = _state()
    hologram = snapshot(state)
    state[(0, 1, 1)] += 1
    assert hologram[(0, 1, 1)] != state[(0, 1, 1)]
    with pytest.raises(TypeError):
        snapshot({(0, 1, 1): 0.5})
    with pytest.raises(TypeError):
        snapshot({(0, 1, 1): True})


def test_unchanged_scan_stores_nothing():
    state = _state()
    assert scan(state, dict(state)) == {}


def test_deltas_reconstruct_exactly_both_ways():
    state = _state()
    observed = dict(state)
    observed[(1, 5, 3)] += 7
    observed[(2, 9, 8)] = Fraction(1, 3)
    del observed[(0, 2, 2)]
    observed[(0, 99, 1)] = 4
    deltas = scan(state, observed)
    assert len(deltas) == 4
    assert apply(state, deltas) == observed
    assert revert(observed, deltas) == state


def test_ring_has_eight_distinct_symmetries():
    syms = ring_symmetries()
    assert len({tuple(s) for s in syms}) == 8
    assert all(sorted(s) == list(range(8)) for s in syms)


def test_canonical_ignores_turns_and_mirrors_but_not_shape():
    axis_cross = (1, 0, 1, 0, 1, 0, 1, 0)
    diagonal_cross = (0, 1, 0, 1, 0, 1, 0, 1)
    assert canonical(axis_cross) != canonical(diagonal_cross)  # 45 degrees is not a symmetry
    arrow = (3, 1, 0, 0, 0, 0, 0, 1)
    turned = arrow[-2:] + arrow[:-2]
    mirrored = (arrow[0],) + tuple(reversed(arrow[1:]))
    assert canonical(arrow) == canonical(turned) == canonical(mirrored)
    with pytest.raises(ValueError):
        canonical((1, 2, 3))


def test_ring_patterns_rejects_bad_direction():
    with pytest.raises(ValueError):
        ring_patterns({(0, 1, 9): 1})


def test_unique_pattern_is_taken_over_unknown_and_ambiguous_go_to_analysis():
    state = _state()
    library = {
        "Achsenkreuz": (1, 0, 1, 0, 1, 0, 1, 0),
        "Pfeil": (3, 1, 0, 0, 0, 0, 0, 1),
    }
    observed = dict(state)
    for d, v in enumerate((0, 1, 0, 1, 0, 1, 0, 1), start=1):  # diagonal cross
        observed[(0, 4, d)] += v
    for d, v in enumerate((5, 0, 0, 0, 0, 0, 0, 0), start=1):   # unknown
        observed[(1, 7, d)] += v
    new_state, accepted, analysis = process(state, observed, library)
    assert accepted == {}
    # the diagonal cross is not the axis cross turned: unknown, not guessed
    assert analysis[(0, 4)] == []
    assert analysis[(1, 7)] == []
    assert new_state == state

    observed2 = dict(state)
    for d, v in enumerate((0, 0, 1, 0, 1, 0, 1, 0), start=1):
        observed2[(2, 3, d)] += v
    observed2[(2, 3, 1)] += 1  # completes an axis cross turned by 90 degrees
    new_state, accepted, analysis = process(state, observed2, library)
    assert accepted == {(2, 3): "Achsenkreuz"}
    assert analysis == {}
    assert new_state == observed2


def test_ambiguous_library_match_is_not_taken_over():
    state = _state()
    library = {"A": (1, 2, 0, 0, 0, 0, 0, 0), "B": (0, 0, 0, 0, 0, 0, 1, 2)}  # same shape, turned
    assert recognise((1, 2, 0, 0, 0, 0, 0, 0), library) == ["A", "B"]
    assert recognise((2, 1, 0, 0, 0, 0, 0, 0), library) == []  # a 45 degree shift is not a symmetry
    observed = dict(state)
    observed[(0, 1, 1)] += 1
    observed[(0, 1, 2)] += 2
    new_state, accepted, analysis = process(state, observed, library)
    assert accepted == {} and analysis == {(0, 1): ["A", "B"]}
    assert new_state == state


def test_storage_ratio():
    state = _state(n_circles=125)  # 3 * 125 * 8 = 3000 values
    observed = dict(state)
    for key in list(state)[:3]:
        observed[key] += 1
    deltas = scan(state, observed)
    assert storage_ratio(deltas, len(state)) == Fraction(1, 1000)
    with pytest.raises(ValueError):
        storage_ratio(deltas, 0)
