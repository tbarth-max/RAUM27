"""Tests for raum27.konsens: A and B compute, C checks one value."""

from fractions import Fraction

import pytest

from raum27.konsens import balance_point, consensus, inverse_check, moment_check
from raum27.synchronsensor import AXIS, CORNERS

F = Fraction


def a_forward(x):
    """Instance A: a ratio computed forward."""
    return F(16, 9) * x


def b_mirror(x):
    """Instance B: the same quantity reached by its own route, through the mirror."""
    return F(9, 16) / x


def test_independent_pair_closes_and_a_wrong_instance_is_caught():
    for x in (F(1), F(3, 4), F(5, 2)):
        assert consensus(a_forward(x), b_mirror(x)) == (True, F(16, 9) * x)
        wrong = a_forward(x) + F(1, 100)
        accepted, reason = consensus(wrong, b_mirror(x))
        assert not accepted and reason.startswith("does not close")


def test_derived_b_proves_nothing():
    wrong = F(7, 5)                         # A got it wrong ...
    derived = 1 / wrong                     # ... and B was computed from A's output
    assert inverse_check(wrong, derived) == 1
    assert consensus(wrong, derived)[0]     # the check closes on a wrong answer


def test_moment_balance_about_the_centre():
    # equal weights on the six axis points and the eight corners balance in the centre
    for points in (AXIS, CORNERS, AXIS + CORNERS):
        weights = [1] * len(points)
        assert balance_point(weights, points) == (0, 0, 0)
        assert consensus(weights, list(points), rule="moment", centre=(0, 0, 0)) == (True, (0, 0, 0))
    # a heavier corner shifts the balance point; C refuses
    weights = [1] * 7 + [2]
    accepted, reason = consensus(weights, list(CORNERS), rule="moment", centre=(0, 0, 0))
    assert not accepted
    assert balance_point(weights, CORNERS) != (0, 0, 0)
    assert moment_check(weights, CORNERS, balance_point(weights, CORNERS)) == (0, 0, 0)


def test_diagonal_screws_balance_edge_screws_do_not():
    # plate corners at (+-1, +-1); the centre of weight (0, 0) lies on the diagonal pair
    diagonal = [(1, 1), (-1, -1)]
    edge = [(1, 1), (1, -1)]
    assert balance_point([1, 1], diagonal) == (0, 0)
    assert balance_point([1, 1], edge) == (1, 0)          # half a plate width off the centre


def test_bad_calls_are_refused():
    with pytest.raises(ValueError):
        consensus(1, 1, rule="vote")
    with pytest.raises(ValueError):
        consensus([1], [(0, 0)], rule="moment")
    with pytest.raises(ValueError):
        balance_point([1, -1], [(0,), (1,)])
    with pytest.raises(TypeError):
        inverse_check(0.5, 2)
