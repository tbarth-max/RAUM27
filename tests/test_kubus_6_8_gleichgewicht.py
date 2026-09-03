"""Tests for raum27.kubus_6_8_gleichgewicht."""
from __future__ import annotations

import math

from raum27.kubus_6_8_gleichgewicht import (
    _f,
    exploding_exponent_mismatch,
    find_equilibrium,
    is_strictly_increasing_on_sample,
)


def test_equilibrium_matches_the_source_value():
    x = find_equilibrium()
    assert math.isclose(x, 5.371566952531225, rel_tol=1e-9)


def test_equilibrium_actually_zeroes_the_function():
    x = find_equilibrium()
    assert abs(_f(x)) < 1e-6


def test_derivative_is_always_positive_so_the_root_is_globally_unique():
    """f'(X) = ln(6)*6^X + ln(8)*8^(10-X) is a sum of two strictly
    positive terms for every real X -- checked directly here, which is
    why is_strictly_increasing_on_sample below must hold, not just an
    empirical coincidence."""
    for x in range(-20, 31):
        derivative = math.log(6) * 6.0**x + math.log(8) * 8.0 ** (10 - x)
        assert derivative > 0


def test_monotonic_on_a_wide_sample_not_just_near_the_root():
    assert is_strictly_increasing_on_sample(lo=-20.0, hi=30.0, n=2000)


def test_root_is_identical_whether_the_bracket_is_wide_or_narrow():
    """If the function is genuinely monotonic everywhere, the root found
    in a wide bracket and a narrow one around the source's [5,6] must
    coincide -- unlike a merely-locally-found root, which could differ if
    another crossing existed elsewhere."""
    wide = find_equilibrium(lo=-50.0, hi=50.0)
    narrow = find_equilibrium(lo=5.0, hi=6.0)
    assert math.isclose(wide, narrow, rel_tol=1e-9)


def test_exploding_exponent_mismatch_diverges_from_x_equals_2():
    """The rejected generalization: verifies the two sides are already
    unequal (and by a growing margin) rather than silently assuming it."""
    a, b = exploding_exponent_mismatch(2, 2)
    assert (a, b) == (1296, 4096)
    a3, b3 = exploding_exponent_mismatch(3, 3)
    ratio_at_2 = b / a
    ratio_at_3 = b3 / a3
    assert ratio_at_3 > ratio_at_2 > 1
