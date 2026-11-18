"""Tests for raum27.schalenleiter."""
from __future__ import annotations

import random
from fractions import Fraction

import pytest

from raum27.lichtgitter import SPEED_OF_LIGHT
from raum27.rational_space import involution, is_fixed_point
from raum27.schalenleiter import (
    STATED_OUTER_BOUND,
    admits_exact_ladder,
    exact_ratio,
    exact_stage_counts,
    exponent_gcd,
    geometric_ladder,
    has_constant_difference,
    has_constant_ratio,
    cluster_bound,
    dual_ladder,
    dual_ladders_cover,
    clusters_stay_exact,
    inner_ladder,
    ladder_contains,
    integer_nth_root,
    nearest_exact_bounds,
    nine_stage_bounds,
    prime_exponents,
    shared_rung_condition,
    shared_rungs,
    survives_inversion,
)
from raum27.zahlensysteme import cube_scaling_count, rgb_color_count


# --------------------------------------------- the reciprocal map itself

def test_the_reciprocal_map_is_involutive_with_one_as_its_centre():
    for value in (Fraction(2), Fraction(STATED_OUTER_BOUND), Fraction(7, 5),
                  Fraction(1, STATED_OUTER_BOUND)):
        assert involution(involution(value)) == value
    assert is_fixed_point(Fraction(1))
    assert not is_fixed_point(Fraction(2))
    # worth stating: over ALL rationals -1 is a fixed point too, so "the
    # only one" holds for the positive rationals
    assert is_fixed_point(Fraction(-1))


# ------------------------------------- Law 4 forces geometric spacing

def test_a_linear_ladder_does_not_survive_inversion():
    """1, 2, 3, 4, 5 inverts to 1, 1/2, 1/3, 1/4, 1/5 -- differences
    -1/2, -1/6, -1/12, -1/20, so neither linear nor geometric inside."""
    linear = [Fraction(k) for k in range(1, 6)]
    assert has_constant_difference(linear)
    inverted = inner_ladder(linear)
    assert inverted == [Fraction(1, k) for k in range(1, 6)]
    assert not has_constant_difference(inverted)
    assert not has_constant_ratio(inverted)
    assert not survives_inversion(linear)


def test_a_geometric_ladder_survives_inversion_with_the_reciprocal_ratio():
    outer = geometric_ladder(Fraction(8), 4)
    assert outer == [Fraction(1), Fraction(8), Fraction(64), Fraction(512), Fraction(4096)]
    assert has_constant_ratio(outer)
    inner = inner_ladder(outer)
    assert inner == [Fraction(1, 8 ** k) for k in range(5)]
    assert has_constant_ratio(inner)
    assert {inner[i + 1] / inner[i] for i in range(4)} == {Fraction(1, 8)}
    assert survives_inversion(outer)


def test_the_closure_property_over_many_random_ladders():
    """20000 of each: no linear ladder stays linear under inversion, and
    every geometric ladder stays geometric."""
    rng = random.Random(4)
    linear_survived = geometric_survived = 0
    checked = 0
    for _ in range(4000):
        step = Fraction(rng.randint(1, 20), rng.randint(1, 9))
        start = Fraction(rng.randint(1, 20), rng.randint(1, 9))
        linear = [start + k * step for k in range(4)]
        if any(v <= 0 for v in linear):
            continue
        checked += 1
        if has_constant_difference(inner_ladder(linear)):
            linear_survived += 1
        ratio = Fraction(rng.randint(2, 20), rng.randint(1, 3))
        base = Fraction(rng.randint(1, 20), rng.randint(1, 9))
        geometric = [base * ratio ** k for k in range(4)]
        if has_constant_ratio(inner_ladder(geometric)):
            geometric_survived += 1
    assert checked > 3000
    assert linear_survived == 0
    assert geometric_survived == checked


# ------------------------- and geometric spacing excludes 300 million

def test_the_stated_outer_bound_admits_no_exact_ladder_beyond_one_stage():
    """THE DECISIVE RESULT. 300000000 = 2^8 * 3 * 5^8, exponent gcd 1, so
    it is a perfect n-th power only for n = 1."""
    assert prime_exponents(STATED_OUTER_BOUND) == {2: 8, 3: 1, 5: 8}
    assert exponent_gcd(STATED_OUTER_BOUND) == 1
    assert exact_stage_counts(STATED_OUTER_BOUND) == [1]
    assert admits_exact_ladder(STATED_OUTER_BOUND, 1)
    for stages in (2, 3, 4, 8, 9, 24):
        assert not admits_exact_ladder(STATED_OUTER_BOUND, stages)
        with pytest.raises(ValueError):
            exact_ratio(STATED_OUTER_BOUND, stages)


def test_the_exact_speed_of_light_carries_no_ladder_either():
    assert prime_exponents(SPEED_OF_LIGHT) == {2: 1, 7: 1, 73: 1, 293339: 1}
    assert exponent_gcd(SPEED_OF_LIGHT) == 1
    assert exact_stage_counts(SPEED_OF_LIGHT) == [1]
    for stages in (2, 3, 9):
        assert not admits_exact_ladder(SPEED_OF_LIGHT, stages)


def test_the_submitted_shell_list_was_inconsistent_with_itself():
    """(1, 100, 10000, 300000000) has ratios 100, 100, 30000. Three
    stages of a ratio-100 ladder end at 10^6."""
    submitted = [1, 100, 10_000, 300_000_000]
    ratios = [submitted[i + 1] // submitted[i] for i in range(3)]
    assert ratios == [100, 100, 30_000]
    assert len(set(ratios)) == 2          # not one ratio, so not geometric
    assert 100 ** 3 == 1_000_000
    assert 100 ** 3 != STATED_OUTER_BOUND


# ------------------------------- what works, and is already in the package

def test_two_to_the_twentyfour_admits_eight_different_exact_ladders():
    bound = cube_scaling_count()
    assert bound == rgb_color_count() == 2 ** 24 == 16_777_216
    assert prime_exponents(bound) == {2: 24}
    assert exponent_gcd(bound) == 24
    assert exact_stage_counts(bound) == [1, 2, 3, 4, 6, 8, 12, 24]
    expected = {1: 16_777_216, 2: 4096, 3: 256, 4: 64, 6: 16, 8: 8, 12: 4, 24: 2}
    for stages, ratio in expected.items():
        assert exact_ratio(bound, stages) == ratio
        assert ratio ** stages == bound


def test_the_ratio_eight_ladder_is_exact_and_pairs_to_one():
    """8^8 = 2^24, and every outer shell times its inner partner is
    exactly 1 -- the shared reference the model asks for."""
    outer = geometric_ladder(Fraction(8), 8)
    assert outer[-1] == cube_scaling_count()
    inner = inner_ladder(outer)
    for o, i in zip(outer, inner):
        assert o * i == 1
    assert len(outer) == 9        # nine shells, eight steps


def test_nine_stages_bracket_the_stated_bound_without_reaching_it():
    bounds = nine_stage_bounds()
    assert bounds[8] == 134_217_728 == 2 ** 27
    assert bounds[9] == 387_420_489 == 3 ** 18
    assert bounds[8] < STATED_OUTER_BOUND < bounds[9]
    assert nearest_exact_bounds(STATED_OUTER_BOUND, 9) == (134_217_728, 387_420_489)
    assert admits_exact_ladder(2 ** 27, 9)
    assert exact_ratio(2 ** 27, 9) == 8
    assert admits_exact_ladder(3 ** 18, 9)
    assert exact_ratio(3 ** 18, 9) == 9


def test_the_twentyseven_in_two_to_the_twentyseven_is_arithmetic_not_the_projects_27():
    """CAVEAT, as a test so it cannot be over-read: the exponent is
    forced by 8 = 2^3 and 3*9 = 27. Nothing about cube geometry enters,
    and the same construction gives other exponents for other ratios."""
    assert 8 ** 9 == 2 ** 27
    assert 8 == 2 ** 3
    assert 3 * 9 == 27
    # other ratios give other exponents, with no 27 in sight
    assert 4 ** 9 == 2 ** 18
    assert 16 ** 9 == 2 ** 36
    assert 9 ** 9 == 3 ** 18


def test_the_ratio_is_a_choice_not_a_result():
    """CAVEAT: eight is attractive because it is the cube's corner count,
    and 8^8 landing on a number this package already holds for an
    unrelated reason is a real cross-check. But six other ratios reach
    the same bound exactly."""
    bound = cube_scaling_count()
    working = [exact_ratio(bound, n) for n in exact_stage_counts(bound)]
    assert 8 in working
    assert len(working) == 8          # eight different ratios work
    assert sorted(working) == [2, 4, 8, 16, 64, 256, 4096, 16_777_216]


# ------------------------------------------------------------- guards

def test_guards():
    with pytest.raises(ValueError):
        prime_exponents(0)
    with pytest.raises(ValueError):
        prime_exponents(-5)
    with pytest.raises(ValueError):
        exact_stage_counts(1)
    with pytest.raises(ValueError):
        admits_exact_ladder(100, 0)
    with pytest.raises(ValueError):
        geometric_ladder(Fraction(0), 3)
    with pytest.raises(ValueError):
        geometric_ladder(Fraction(8), -1)
    with pytest.raises(ValueError):
        nearest_exact_bounds(100, 0)
    assert exponent_gcd(1) == 0


# ----------------------------------- the root is exact, not float-guessed

def test_the_nth_root_is_computed_in_integers_and_bracketed_correctly():
    """r^d <= v < (r+1)^d for every value and degree -- the defining
    property of a floor root, checked by brute force rather than by
    comparing against a float."""
    for value in range(0, 600):
        for degree in (1, 2, 3, 5, 7):
            root = integer_nth_root(value, degree)
            assert root ** degree <= value < (root + 1) ** degree


def test_the_root_stays_exact_where_floating_point_would_not():
    """`round(value ** (1 / degree))` is a float, and for large values its
    error can exceed 1, so a search around it would be correct by luck.
    Newton's method on integers has no such limit."""
    rng = random.Random(9)
    for _ in range(300):
        base = rng.randint(2, 50)
        degree = rng.randint(2, 60)
        assert integer_nth_root(base ** degree, degree) == base
    # and exact_ratio inherits that, far past float range
    for value, stages in ((2 ** 600, 24), (3 ** 300, 30), (7 ** 200, 50),
                          (10 ** 500, 100), (2 ** 4096, 64)):
        ratio = exact_ratio(value, stages)
        assert ratio ** stages == value
    assert exact_ratio(2 ** 4096, 64) == 2 ** 64


def test_short_ladders_are_trivially_both_kinds():
    """Fewer than three points cannot distinguish linear from geometric,
    so both predicates accept them."""
    for ladder in ([], [Fraction(5)], [Fraction(1), Fraction(8)]):
        assert has_constant_ratio(ladder)
        assert has_constant_difference(ladder)


def test_a_ladder_that_is_neither_kind_does_not_survive_inversion():
    irregular = [Fraction(1), Fraction(2), Fraction(4), Fraction(5)]
    assert not has_constant_ratio(irregular)
    assert not has_constant_difference(irregular)
    assert not survives_inversion(irregular)


def test_root_guards():
    with pytest.raises(ValueError):
        integer_nth_root(-1, 2)
    with pytest.raises(ValueError):
        integer_nth_root(16, 0)
    assert integer_nth_root(0, 3) == 0
    assert integer_nth_root(1, 7) == 1


# ------------------------------------------------- clustering the ladder

def test_cluster_boundaries_are_powers_of_the_ladder_top():
    assert cluster_bound(8, 9, 0) == 1
    assert cluster_bound(8, 9, 1) == 8 ** 9 == 2 ** 27
    assert cluster_bound(8, 9, 2) == 8 ** 18 == 2 ** 54
    assert cluster_bound(8, 9, 3) == 2 ** 81


def test_the_cluster_plan_requires_counting_steps_not_values():
    """THE DECISIVE POINT for the indexing question. Repeating a ladder
    whose top is r**stages keeps every boundary a perfect stages-th
    power, because r**(stages*m) = (r**m)**stages. Repeating one whose
    top is r**(stages-1) does not."""
    # nine STEPS: 8**9 = 2**27, every cluster boundary 2**(27m)
    assert clusters_stay_exact(8, 9)
    assert clusters_stay_exact(9, 9)
    assert clusters_stay_exact(2, 24)
    # nine VALUES: top 8**8 = 2**24, boundaries 2**(24m) -- 24m divisible
    # by 9 only for m = 3, 6, ...
    assert not admits_exact_ladder(8 ** 8, 9)
    assert not admits_exact_ladder(8 ** 16, 9)
    assert admits_exact_ladder(8 ** 24, 9)        # m = 3 happens to work
    assert exponent_gcd(8 ** 8) == 24
    assert 24 % 9 != 0


def test_both_candidate_ratios_cluster_consistently():
    """So exactness does not decide between 8**9 and 9**9 -- both work,
    and the choice has to be made on other grounds."""
    for ratio in (8, 9):
        for m in range(1, 6):
            top = cluster_bound(ratio, 9, m)
            assert admits_exact_ladder(top, 9)
            assert exact_ratio(top, 9) == ratio ** m


# --------------------------------- which bit patterns sit on the ladder

def test_a_ratio_eight_ladder_misses_the_eight_bit_pattern():
    """A real tension worth knowing: the ratio-8 ladder holds only
    2**(3k), so a 6-bit pattern is a rung and an 8-bit pattern is not."""
    assert ladder_contains(8, 9, 2 ** 6)      # 64 = 8**2
    assert not ladder_contains(8, 9, 2 ** 8)  # 256 = 2**8
    assert ladder_contains(8, 9, 2 ** 24)
    assert ladder_contains(8, 9, 2 ** 27)
    # a ratio-2 ladder holds both
    assert ladder_contains(2, 24, 2 ** 6)
    assert ladder_contains(2, 24, 2 ** 8)
    # and the combined 6+8 bit word is on neither power-of-eight rung
    assert not ladder_contains(8, 9, 2 ** 14)
    assert ladder_contains(2, 24, 2 ** 14)


def test_cluster_guards():
    with pytest.raises(ValueError):
        cluster_bound(1, 9, 1)
    with pytest.raises(ValueError):
        cluster_bound(8, 0, 1)
    with pytest.raises(ValueError):
        cluster_bound(8, 9, -1)
    with pytest.raises(ValueError):
        ladder_contains(1, 9, 64)
    with pytest.raises(ValueError):
        ladder_contains(8, -1, 64)


# ----------------------------- expansion and compression are two ladders

def test_the_unit_sits_on_a_different_axis_in_each_map():
    """x**0 = 1 for every x; 0**0 = 1 but 0**x = 0 for x > 0. So one map
    reaches the unit along the exponent axis and the other along the base
    axis -- which is why both are needed."""
    for x in range(5):
        assert x ** 0 == 1
    assert 0 ** 0 == 1
    for x in range(1, 5):
        assert 0 ** x == 0
    assert dual_ladder(8, 9)[0] == 0        # k = 0 gives 0, not 1
    assert geometric_ladder(Fraction(8), 9)[0] == 1


def test_the_two_ladders_together_cover_both_bit_patterns():
    """The tension the single ladder had: ratio 8 holds only 2**(3k), so
    a 6-bit rung exists and an 8-bit one does not. The dual ladder
    supplies it."""
    assert ladder_contains(8, 9, 2 ** 6)
    assert not ladder_contains(8, 9, 2 ** 8)
    assert 2 ** 8 in dual_ladder(8, 9)
    assert 2 ** 6 not in dual_ladder(8, 9)
    assert dual_ladders_cover(8, 9, 2 ** 6)
    assert dual_ladders_cover(8, 9, 2 ** 8)
    # and the top is a rung of both
    assert dual_ladders_cover(8, 9, 2 ** 24)


def test_the_shared_rung_condition_is_derived_and_holds_for_prime_powers():
    """REGRESSION against two wrong guesses of mine. The shared rungs are
    not the duplex_inversion coincidences, and not the powers of r**r --
    they are the r**j with r | a*j for r = p**a."""
    for ratio in (2, 3, 4, 8, 9, 16, 27):
        stages = 12
        direct = sorted(
            {ratio ** k for k in range(stages + 1)} & set(dual_ladder(ratio, stages))
        )
        assert shared_rungs(ratio, stages) == direct

    # the two wrong guesses, pinned so they cannot come back
    assert shared_rungs(2, 12) == [1, 4, 16, 64]        # a family, not just 16
    assert shared_rungs(4, 12) == [1, 16, 256, 4096]    # 16 and 4096 are not powers of 256
    assert 16 not in (256 ** m for m in range(4))
    # ratio 8: the condition 8 | 3j reduces to 8 | j since gcd(3, 8) = 1
    assert shared_rung_condition(8) == (8, 3)
    assert shared_rungs(8, 12) == [1, 2 ** 24]


def test_a_non_prime_power_ratio_is_reported_rather_than_mis_handled():
    assert shared_rung_condition(6) is None
    # and the fallback still intersects correctly
    direct = sorted({6 ** k for k in range(13)} & set(dual_ladder(6, 12)))
    assert shared_rungs(6, 12) == direct


def test_dual_ladder_guards():
    with pytest.raises(ValueError):
        dual_ladder(0, 9)
    with pytest.raises(ValueError):
        dual_ladder(8, -1)
