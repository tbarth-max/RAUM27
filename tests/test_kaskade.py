"""Tests for raum27.kaskade: known out, mirror, compare, hand over the rest."""

from fractions import Fraction
import random

import pytest

from raum27.kaskade import cascade, explain, known_circle_ratio, manual_share

F = Fraction
FACTORS = [F(4, 3), F(16, 9)]


def _stream(seed=7):
    rng = random.Random(seed)
    samples = []
    for _ in range(300):
        x = F(rng.randint(1, 40), rng.randint(1, 40))
        kind = rng.random()
        if kind < 0.4:
            samples.append((x, F(4, 3) * x))                 # known proportion
        elif kind < 0.7:
            samples.append((x, F(16, 9) / x))                # known inverse proportion
        elif kind < 0.9:
            samples.append((x, x * F(2 ** rng.randint(0, 3), 3 ** rng.randint(0, 3))))  # 2-3 circles
        else:
            samples.append((x, x * F(5 * rng.randint(1, 4), 7)))                       # beyond the walls
    return samples


def test_known_circle_ratio_stays_inside_two_and_three():
    assert known_circle_ratio(3, 8) == F(8, 3)
    assert known_circle_ratio(1, F(27, 16)) == F(27, 16)
    assert known_circle_ratio(1, F(5, 3)) is None              # the 5 is a wall
    assert known_circle_ratio(0, 1) is None


def test_explain_names_the_pattern():
    assert explain(F(3), F(4), FACTORS) == ("prop", F(4, 3))
    assert explain(F(2), F(8, 9), FACTORS) == ("inv", F(16, 9))
    assert explain(F(5), F(5, 2), FACTORS) == ("circle", F(1, 2))
    assert explain(F(1), F(5, 7), FACTORS) is None


def test_cascade_hands_over_only_the_small_rest():
    samples = _stream()
    confirmed, manual = cascade(samples, FACTORS)
    assert len(confirmed) + len(manual) == len(samples)
    # everything outside the 2-3 world reaches the manual folder ...
    beyond = [s for s in samples if known_circle_ratio(*s) is None
              and explain(*s, FACTORS) is None]
    assert {s for s, _ in manual} >= set(beyond)
    # ... and nothing from it is ever confirmed
    assert not any(known_circle_ratio(*s) is None and explain(*s, FACTORS) is None for s, _ in confirmed)
    assert manual_share(samples, FACTORS) < F(1, 5)


def test_mirror_keeps_inverse_with_inverted_factor():
    confirmed, manual = cascade([(F(2), F(8, 9))], FACTORS)
    assert confirmed == [((F(2), F(8, 9)), ("inv", F(16, 9)))]
    assert manual == []


def test_a_point_on_two_curves_is_ambiguous_not_guessed():
    # (4/3, 1) lies on y = (4/3)/x and its mirror (3/4, 1) on y = (4/3) x
    confirmed, manual = cascade([(F(4, 3), F(1))], [F(4, 3)])
    assert confirmed == []
    assert manual == [((F(4, 3), F(1)), "ambiguous: original and mirror name different patterns")]


def test_following_the_inverse_of_a_known_factor_is_flagged():
    # y = (3/5) x: unknown here, but its mirror follows the known factor 5/3
    confirmed, manual = cascade([(F(1), F(3, 5))], [F(5, 3)])
    assert confirmed == []
    assert manual == [((F(1), F(3, 5)), "explained on one side only")]


def test_zero_and_bad_input_are_handed_over_or_refused():
    confirmed, manual = cascade([(0, 1), (F(1), F(0))], FACTORS)
    assert confirmed == [] and len(manual) == 2
    assert all(reason == "zero cannot be mirrored" for _, reason in manual)
    with pytest.raises(TypeError):
        cascade([(0.5, 1)], FACTORS)
    with pytest.raises(ValueError):
        manual_share([], FACTORS)
