"""Tests for raum27.konsens: A and B compute, C checks one value."""

from fractions import Fraction

import pytest

from raum27.konsens import balance_point, consensus, inverse_check, locate_from_poles, moment_check
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


def _squared_distances(point, pole=1):
    plus = [sum((point[i] - (pole if i == k else 0)) ** 2 for i in range(3)) for k in range(3)]
    minus = [sum((point[i] + (pole if i == k else 0)) ** 2 for i in range(3)) for k in range(3)]
    return plus, minus


def test_plus_and_minus_meet_exactly_where_c_stands():
    for point in ((0, 0, 0), (F(1, 3), F(-2, 7), F(5, 4)), (F(9, 16), 0, F(-1, 2))):
        plus, minus = _squared_distances(point)
        assert locate_from_poles(plus, minus) == tuple(F(c) for c in point)
    plus, minus = _squared_distances((0, 0, 0))
    assert plus == minus                                   # in the centre both sides agree
    assert consensus(plus, minus, rule="poles") == (True, (0, 0, 0))


def test_one_pair_gives_only_the_equator_and_c_refuses_off_centre():
    # every point of the equator circle has equal north and south distances
    for p in ((1, 0, 0), (0, 1, 0), (F(3, 5), F(4, 5), 0)):
        plus, minus = _squared_distances(p)
        assert plus[2] == minus[2]                          # z-pair cannot tell them apart
    plus, minus = _squared_distances((F(1, 10), 0, 0))
    accepted, reason = consensus(plus, minus, rule="poles")
    assert not accepted and "1/10" in reason
    with pytest.raises(ValueError):
        locate_from_poles([1], [1, 2])
    with pytest.raises(ValueError):
        locate_from_poles([1], [1], pole=0)
