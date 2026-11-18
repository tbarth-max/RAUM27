"""Tests for raum27.verhaeltnis: show proportions, not decimals."""

from fractions import Fraction
import math

import pytest

from raum27.verhaeltnis import (
    annotate, as_ratio, circle_points, expansion, turns_and_position, common_circle, contains, factors, new_points,
    origin, positions_up_to, proportion, show, show_unreduced,
)


def test_decimals_that_are_ratios_show_as_ratios():
    assert show(1 / 3) == "(1:3)"
    assert show(1 / 9) == "(1:9)"
    assert show(16 / 9) == "(16:9)"
    assert show(Fraction(4, 3)) == "(4:3)"
    assert show(2) == "(2:1)"


def test_irrational_numbers_are_not_dressed_up():
    assert as_ratio(math.sqrt(2) - 1) is None
    assert show(math.pi).startswith("3.14159")
    assert proportion(math.sqrt(2), 1) is None


def test_proportion_shows_the_factor_at_a_glance():
    assert proportion(1 / 3, 1 / 9) == "(3:1)"
    assert proportion(Fraction(8), Fraction(6)) == "(4:3)"
    assert proportion(math.sqrt(8), math.sqrt(2)) == "(2:1)"
    with pytest.raises(ZeroDivisionError):
        proportion(1.5, 0)


def test_annotate_a_row_of_values():
    assert annotate([1 / 9, 1 / 3, 1.0]) == [("(1:9)", "(1:1)"), ("(1:3)", "(3:1)"), ("(1:1)", "(9:1)")]


def test_new_points_are_eulers_phi_and_round_circles_mostly_inherit():
    assert [new_points(n) for n in range(1, 13)] == [1, 1, 2, 2, 4, 2, 6, 4, 6, 4, 10, 4]
    inherited = [k for k, n, home, inh in circle_points(12) if inh]
    assert len(inherited) == 8
    assert [k for k, n, home, inh in circle_points(12) if not inh] == [1, 5, 7, 11]


def test_circles_nest_and_six_and_eight_meet_on_twenty_four():
    assert contains(3, 12) and contains(4, 12) and not contains(5, 12)
    assert common_circle(6, 8) == 24
    assert all(contains(c, 24) for c in (1, 2, 3, 4, 6, 8, 12, 24))
    assert positions_up_to(9) == 28


def test_origin_keeps_what_cancelling_hides():
    assert origin(2, 6) == (1, 3)
    assert origin(0, 7) == (0, 1)
    assert origin(9, 6) == (1, 2)          # a full turn plus 3/6
    assert show_unreduced(2, 6) == "2/6 (circle 6) = 1/3 (circle 3)"
    assert show_unreduced(5, 12) == "5/12 (circle 12)"
    with pytest.raises(ValueError):
        origin(1, 0)


def test_factored_denominators_make_the_pattern_visible():
    row = [f"1/({factors(n)}·{factors(n + 1)})" for n in range(1, 6)]
    assert row == ["1/(1·2)", "1/(2·3)", "1/(3·2·2)", "1/(2·2·5)", "1/(5·2·3)"]
    assert factors(89700) == "2·2·3·5·5·13·23"     # = 299 · 300, the innermost gap
    total = sum(Fraction(1, n * (n + 1)) for n in range(1, 300))
    assert total == Fraction(299, 300)              # telescoping: n/(n+1)


def test_nine_and_ten_see_each_other_as_periodic():
    assert expansion(1, 9, 10) == ("", "1")         # 0.(1)
    assert expansion(1, 9, 9) == ("1", "")          # 0.1
    assert expansion(1, 10, 10) == ("1", "")        # 0.1
    assert expansion(1, 10, 9) == ("", "08")        # 0.(08)
    assert expansion(1, 27, 10) == ("", "037")
    assert expansion(1, 81, 10) == ("", "012345679")
    assert expansion(1, 18, 10) == ("0", "5")
    with pytest.raises(ValueError):
        expansion(3, 2)


def test_zero_and_one_meet_on_the_circle():
    assert turns_and_position(0, 9) == (0, 0)
    assert turns_and_position(9, 9) == (1, 0)       # n/n: one turn done, back at the start
    assert turns_and_position(13, 9) == (1, 4)
    assert origin(9, 9) == origin(0, 9) == (0, 1)
    with pytest.raises(ValueError):
        turns_and_position(1, 0)
