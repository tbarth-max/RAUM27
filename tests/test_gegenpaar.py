"""Tests for raum27.gegenpaar."""

from fractions import Fraction

import pytest

from raum27.gegenpaar import (
    I_POWERS, Gauss, energy, occupied_classes, opposite_pairs, quarter_class, returning_part, separable,
)

TURN_LEFT = [I_POWERS[(j // 2) % 4] for j in range(8)]       # a quarter turn (2 samples) multiplies by i: class 1
TURN_RIGHT = [I_POWERS[(-(j // 2)) % 4] for j in range(8)]   # multiplies by -i: turns the other way, class 3


def _add(a, b):
    return [x + y for x, y in zip(a, b)]


def test_ground_level_drops_out_and_the_pairs_stay():
    signal = [3, 1, -2, 5, -3, -1, 2, -5]                     # f[j+4] = -f[j]: perfect opposite pairs
    bias = [7] * 8                                            # the neutral ground voltage
    biased = [s + 7 for s in signal]
    assert opposite_pairs(biased) == [Gauss(s) for s in signal]
    assert returning_part(biased) == [Gauss(b) for b in bias]


def test_the_180_filter_is_an_exact_projection():
    f = [Fraction(1, 3), 4, -2, 9, 0, Fraction(-7, 2), 1, 6]
    p = opposite_pairs(f)
    assert opposite_pairs(p) == p                             # P² = P
    assert _add(p, returning_part(f)) == [Gauss(x) for x in f]  # nothing lost, nothing added
    assert all(v == Gauss(0) for v in opposite_pairs(returning_part(f)))


def test_the_limit_of_180_and_the_90_degree_classes():
    # signal turns left, disturbance turns right: both are perfect opposite pairs
    assert opposite_pairs(TURN_LEFT) == TURN_LEFT
    assert opposite_pairs(TURN_RIGHT) == TURN_RIGHT
    mixed = _add(TURN_LEFT, [z * 3 for z in TURN_RIGHT])
    assert opposite_pairs(mixed) == mixed                     # 180° alone cannot separate them
    assert quarter_class(mixed, 1) == TURN_LEFT               # the quarter turn can, exactly
    assert quarter_class(mixed, 3) == [z * 3 for z in TURN_RIGHT]
    assert occupied_classes(TURN_LEFT) == {1} and occupied_classes(TURN_RIGHT) == {3}
    assert separable(TURN_LEFT, TURN_RIGHT)


def test_classes_add_up_and_nest_inside_the_pairs():
    f = [Gauss(1, 2), Gauss(-3, 0), Gauss(0, 5), Gauss(4, -1),
         Gauss(2, 2), Gauss(Fraction(1, 2), 3), Gauss(-1, -1), Gauss(0, 7)]
    parts = [quarter_class(f, r) for r in range(4)]
    assert [a + b + c + d for a, b, c, d in zip(*parts)] == f
    assert _add(parts[1], parts[3]) == opposite_pairs(f)     # P1 + P3 = P
    assert _add(parts[0], parts[2]) == returning_part(f)     # P0 + P2 = 1 - P
    for r in range(4):
        assert quarter_class(parts[r], r) == parts[r]        # each class a projection
    assert energy(f) == sum(energy(p) for p in parts)        # the classes are orthogonal


def test_same_class_disturbance_stays():
    disturbance = [z * 2 for z in TURN_LEFT]                  # same turning sense as the signal
    assert not separable(TURN_LEFT, disturbance)
    assert quarter_class(_add(TURN_LEFT, disturbance), 1) == [z * 3 for z in TURN_LEFT]


def test_rejects_bad_input():
    with pytest.raises(ValueError):
        opposite_pairs([1, 2, 3])
    with pytest.raises(ValueError):
        quarter_class([1, 2, 3, 4, 5, 6], 1)
    with pytest.raises(ValueError):
        quarter_class([1, 2, 3, 4], 4)
    with pytest.raises(ValueError):
        returning_part([])
    with pytest.raises(TypeError):
        opposite_pairs([0.5, 1])
    with pytest.raises(TypeError):
        Gauss(1) * 0.5
    assert Gauss(1, 1) * Gauss(1, -1) == Gauss(2) and 2 * Gauss(1) == Gauss(2)
    assert Gauss(3, 4) - Gauss(1, 1) == Gauss(2, 3) and Gauss(3, 4).norm() == 25
