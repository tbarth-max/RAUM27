"""Tests for raum27.verhaeltnis_herleitungen -- the five derivations, graded."""
from __future__ import annotations

import math
from fractions import Fraction

import numpy as np
import pytest

from raum27.cube_symmetry import (
    coupling_constant,
    corner_directions,
    face_directions,
    space_diagonals,
)
from raum27.phasor_resonanzfilter import energy
from raum27.rational_space import involution
from raum27.verhaeltnis_herleitungen import (
    archimedes_ratio,
    coherent_superposition_intensity,
    cycle_on_lattice_period,
    cycle_on_lattice_ratio,
    incoherent_superposition_intensity,
    n_ball_volume,
    pi_power_in_n_ball,
    rational_part_of_n_ball,
    reciprocal_identity_distinguishes,
    simple_fractions_between_one_and_two,
    single_field_intensity,
    sphere_to_cylinder_ratio,
    superposition_squares_as_claimed,
    surviving_derivations,
)
from raum27.waage import balances_at_one


# ---------------------------------------------------------------- 1

def test_setting_the_radius_to_one_does_not_give_four_thirds():
    """V = 4pi/3 = 4.18879..., not 4/3. The 4/3 only appears after a
    separate decision to divide by pi."""
    assert n_ball_volume(3, 1.0) == pytest.approx(4.18879, abs=1e-5)
    assert n_ball_volume(3, 1.0) != pytest.approx(4 / 3, abs=0.1)


def test_taking_pi_out_is_not_a_single_operation():
    """It leaves a rational for pi^1 only in dimensions 1-3. In 4 and 5
    the required power is 2, so the rule is dimension-dependent."""
    assert pi_power_in_n_ball(2) == 1
    assert pi_power_in_n_ball(3) == 1
    assert pi_power_in_n_ball(4) == 2
    assert pi_power_in_n_ball(5) == 2
    assert pi_power_in_n_ball(6) == 3
    # dividing the 4-ball by pi^1 leaves pi/2, not a rational
    assert n_ball_volume(4) / math.pi == pytest.approx(math.pi / 2)


def test_the_rational_part_is_different_in_every_dimension():
    """So 4/3 is the NAME of the 3-ball's rational part, not a
    prediction of it."""
    assert rational_part_of_n_ball(3) == Fraction(4, 3)
    assert rational_part_of_n_ball(2) == 1
    assert rational_part_of_n_ball(4) == Fraction(1, 2)
    assert rational_part_of_n_ball(5) == Fraction(8, 15)
    assert rational_part_of_n_ball(6) == Fraction(1, 6)
    parts = {rational_part_of_n_ball(n) for n in range(2, 8)}
    assert len(parts) == 6  # all different


def test_the_answer_depends_entirely_on_what_is_stripped():
    v3 = n_ball_volume(3)
    assert Fraction(v3 / math.pi).limit_denominator(100) == Fraction(4, 3)
    assert Fraction(v3 / (2 * math.pi)).limit_denominator(100) == Fraction(2, 3)
    assert Fraction(v3 / (4 * math.pi)).limit_denominator(100) == Fraction(1, 3)


def test_the_repaired_derivation_is_exact_and_needs_no_banishing():
    """THE ONE THAT WORKS: 4/3 is the sphere-to-cylinder volume ratio
    with height equal to the radius. pi cancels legitimately."""
    assert sphere_to_cylinder_ratio() == Fraction(4, 3)
    # exact for every radius, in units of pi: (4/3)r^3 over r^2 * r
    for r in (Fraction(1), Fraction(2), Fraction(7, 3), Fraction(100)):
        sphere = Fraction(4, 3) * r ** 3
        cylinder = r ** 2 * r
        assert sphere / cylinder == Fraction(4, 3)
    # and the sibling on Archimedes' tombstone, against height 2r
    assert archimedes_ratio() == Fraction(2, 3)
    assert sphere_to_cylinder_ratio() / 2 == archimedes_ratio()


# ---------------------------------------------------------------- 2

def test_a_cycle_on_a_lattice_forces_nothing_about_four():
    """The argument derives p/q from assuming p and q. Every pair works,
    so the 4-stroke is the premise rather than a result."""
    assert cycle_on_lattice_ratio(4, 3) == Fraction(4, 3)
    assert cycle_on_lattice_ratio(5, 3) == Fraction(5, 3)
    assert cycle_on_lattice_ratio(7, 3) == Fraction(7, 3)
    assert cycle_on_lattice_ratio(3, 3) == 1
    ratios = {cycle_on_lattice_ratio(p, 3) for p in range(1, 10)}
    assert len(ratios) == 9  # nothing privileges p = 4
    assert cycle_on_lattice_period(4, 3) == 12
    assert cycle_on_lattice_period(5, 3) == 15


def test_the_genuine_cube_derivation_is_already_in_the_repo():
    """8 corners over 6 faces, exact counts, and it is 4/3."""
    assert len(face_directions()) == 6
    assert len(corner_directions()) == 8
    assert coupling_constant() == Fraction(4, 3)
    assert coupling_constant() == Fraction(len(corner_directions()), len(face_directions()))


def test_the_space_diagonal_route_is_the_same_derivation_not_a_second():
    """4 space diagonals over 3 axes equals 8/6 because 8 = 2*4 and
    6 = 2*3. One route, counted twice."""
    assert len(space_diagonals()) == 4
    assert Fraction(len(space_diagonals()), 3) == Fraction(4, 3)
    assert len(corner_directions()) == 2 * len(space_diagonals())
    assert len(face_directions()) == 2 * 3
    assert Fraction(len(space_diagonals()), 3) == coupling_constant()


# ---------------------------------------------------------------- 3

def test_four_thirds_is_the_perfect_fourth_and_also_barely_surprising():
    """True statement, no explanatory force: 4/3 is among the very
    simplest ratios there are, and simple ratios recur because they are
    simple."""
    simple = simple_fractions_between_one_and_two(7)
    assert len(simple) == 17
    assert Fraction(4, 3) in simple
    assert simple.index(Fraction(4, 3)) == 1  # second simplest
    assert simple[0] == Fraction(3, 2)
    # with a tighter bound there are only a handful at all
    assert simple_fractions_between_one_and_two(3) == [Fraction(3, 2), Fraction(4, 3), Fraction(5, 3)]


# ---------------------------------------------------------------- 4

def test_superposing_two_four_thirds_fields_does_not_give_sixteen_ninths():
    """REFUTES the superposition derivation. Amplitudes add; squaring is
    what turns one amplitude into one intensity."""
    a = Fraction(4, 3)
    assert coherent_superposition_intensity([a, a]) == Fraction(64, 9)
    assert incoherent_superposition_intensity([a, a]) == Fraction(32, 9)
    assert single_field_intensity(a) == Fraction(16, 9)
    assert coherent_superposition_intensity([a, a]) != Fraction(16, 9)
    assert incoherent_superposition_intensity([a, a]) != Fraction(16, 9)
    assert superposition_squares_as_claimed() is False


def test_the_repos_own_phasor_energy_agrees():
    """Cross-check against phasor_resonanzfilter.energy, which sums
    squared amplitudes."""
    assert energy(np.array([4 / 3])) == pytest.approx(float(Fraction(16, 9)))
    assert energy(np.array([4 / 3, 4 / 3])) == pytest.approx(float(Fraction(32, 9)))
    assert (8 / 3) ** 2 == pytest.approx(float(Fraction(64, 9)))


def test_the_working_route_to_sixteen_ninths_is_the_cube_one():
    assert coupling_constant() ** 2 == Fraction(16, 9)
    assert Fraction(8, 6) ** 2 == Fraction(16, 9)
    assert Fraction(16, 9) == single_field_intensity(Fraction(4, 3))


# ---------------------------------------------------------------- 5

def test_the_reciprocal_identity_distinguishes_nothing():
    """REFUTES the balance proof: it holds for every x, so it singles
    out 16/9 no more than any other value. The repo already proves this
    for arbitrary reciprocal pairs."""
    for x in (Fraction(16, 9), Fraction(2), Fraction(7, 5),
              Fraction(1000, 3), Fraction(1, 12345)):
        assert x * involution(x) == 1
        assert balances_at_one(x, involution(x))
        assert reciprocal_identity_distinguishes(x) is False


def test_zero_has_no_reciprocal():
    with pytest.raises(ValueError):
        reciprocal_identity_distinguishes(Fraction(0))


# ---------------------------------------------------------------- summary

def test_what_survives_is_two_independent_routes():
    """The conclusion that the numbers are not arbitrary is correct. The
    surviving reasons are not the five that were offered."""
    surviving = surviving_derivations()
    assert surviving["sphere_over_cylinder_height_r"] == Fraction(4, 3)
    assert surviving["cube_corners_over_faces"] == Fraction(4, 3)
    assert surviving["square_of_the_cube_ratio"] == Fraction(16, 9)
    # the two routes to 4/3 are genuinely independent: one is about a
    # sphere and a cylinder, the other counts cube elements
    assert surviving["sphere_over_cylinder_height_r"] == sphere_to_cylinder_ratio()
    assert surviving["cube_corners_over_faces"] == coupling_constant()
    assert surviving["square_of_the_cube_ratio"] == coupling_constant() ** 2


def test_degenerate_inputs_raise():
    with pytest.raises(ValueError):
        n_ball_volume(0)
    with pytest.raises(ValueError):
        pi_power_in_n_ball(0)
    with pytest.raises(ValueError):
        cycle_on_lattice_ratio(0, 3)
    with pytest.raises(ValueError):
        cycle_on_lattice_period(4, 0)
    with pytest.raises(ValueError):
        simple_fractions_between_one_and_two(0)
