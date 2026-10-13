"""Tests for raum27.verhaeltnis: show proportions, not decimals."""

from fractions import Fraction
import math

import pytest

from raum27.verhaeltnis import annotate, as_ratio, proportion, show


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
