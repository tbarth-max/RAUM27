"""Documented error paths and edge-case branches.

An external review asked which critical paths the suite leaves
untested. Coverage measurement put the whole package at 97% with 40
uncovered statements; this file closes them. Most were `raise` guards
that document a contract and were never exercised, but three were
genuine logic:

- `impakt_schwelle.tate_interface_velocity` takes a *linear* path when
  rod and target have equal density, because the quadratic's leading
  coefficient vanishes. That is physically the most ordinary case --
  steel into steel -- and it was the one real untested branch. Checked
  here for correctness, not just for coverage: no bug was found.
- `clockfree_scheduler.Schedule.average_waiting_time` had no caller.
- `kern_modul_v2.find_period` returns -1 on a series too short to
  autocorrelate, and `lotto_benchmark.FingerprintKNNPredictor` has a
  cold-start path and a pad-with-random path for when voting yields
  fewer numbers than needed.

Guard clauses are tested because each one is documented behaviour with
a specific message, not because a percentage wanted moving.
"""
from __future__ import annotations

from fractions import Fraction

import numpy as np
import pytest

from raum27.autocorrelation_control import simulate_ar1
from raum27.basisoperationen import hole_wert
from raum27.clockfree_scheduler import Process, schedule_run_to_completion
from raum27.ifs_attractor import IFS
from raum27.impakt_schwelle import (
    DENSITY,
    YIELD_STRENGTH,
    ballistic_limit_velocity,
    cohesive_energy_fraction,
    hydrodynamic_penetration,
    interface_velocity,
    tate_interface_velocity,
    tate_penetration,
)
from raum27.kern_modul_v2 import find_period
from raum27.kubus_6_8_gleichgewicht import find_equilibrium
from raum27.kugelkoordinaten import (
    exact_spherical,
    from_exact_spherical,
    rational_cos_squared_of_turn,
)
from raum27.lotto_benchmark import FingerprintKNNPredictor, match_probability
from raum27.optionsraum import single_wish, squared_distance, uniform_wish
from raum27.resonanztunnel import (
    harmonic_index,
    layered_flow_bracket,
    two_layer_flow_gain,
)
from raum27.spirale import process_state
from raum27.taylor import sin_taylor
from raum27.tunnelgrenze import landau_critical_velocity, lorentz_absorption, lorentz_dispersion
from raum27.waage import balance_point, center_of_mass


# ----------------------------------------------- the one real logic gap

STEEL = DENSITY["steel"]
Y_STEEL = YIELD_STRENGTH["steel"]
R_STEEL = 3.5 * Y_STEEL


def test_equal_densities_take_the_linear_branch_and_stay_physical():
    """Rod and target of the same material make the quadratic's leading
    coefficient vanish, so the solver takes a separate linear path. This
    was the only genuinely untested branch in the package."""
    assert 0.5 * (STEEL - STEEL) == 0.0  # the degenerate coefficient
    for v in (1000.0, 2000.0, 5000.0, 20000.0):
        u = tate_interface_velocity(STEEL, STEEL, Y_STEEL, R_STEEL, v)
        assert u is not None
        assert 0.0 < u < v  # the hole deepens, but slower than the rod flies
        # and strength must slow it relative to the strengthless answer
        assert u < interface_velocity(STEEL, STEEL, v)


def test_with_no_strength_equal_densities_give_exactly_half_the_velocity():
    for v in (100.0, 1000.0, 7654.0):
        assert interface_velocity(STEEL, STEEL, v) == v / 2


def test_equal_density_penetration_respects_the_same_ceiling():
    """For equal densities the strengthless limit is exactly the rod
    length, and Tate must approach it from below."""
    length = 0.6
    limit = hydrodynamic_penetration(STEEL, STEEL, length)
    assert limit == pytest.approx(length)
    fractions = []
    for v in (1000.0, 2000.0, 5000.0, 20000.0):
        depth = tate_penetration(STEEL, STEEL, Y_STEEL, R_STEEL, v, length)
        assert 0.0 <= depth < limit
        fractions.append(depth / limit)
    assert all(b > a for a, b in zip(fractions, fractions[1:]))
    assert fractions[-1] > 0.99


def test_equal_densities_still_have_a_ballistic_limit():
    limit = ballistic_limit_velocity(STEEL, STEEL, Y_STEEL, R_STEEL)
    assert 700.0 < limit < 900.0
    assert tate_interface_velocity(STEEL, STEEL, Y_STEEL, R_STEEL, limit * 0.5) in (None, 0.0)


# ------------------------------------------------ other genuine logic

def test_the_scheduler_reports_an_average_waiting_time():
    schedule = schedule_run_to_completion([Process("long", 10), Process("short", 1)])
    waits = schedule.waiting_time_by_name()
    assert set(waits) == {"long", "short"}
    assert schedule.average_waiting_time() == pytest.approx(
        sum(waits.values()) / len(waits)
    )
    # the classical failure mode: the short job waits behind the long one
    assert waits["short"] > waits["long"]


def test_find_period_reports_failure_on_a_series_too_short_to_autocorrelate():
    assert find_period(np.array([1.0, 2.0, 3.0]), 20) == -1
    assert find_period(np.array([1.0, 2.0]), 20) == -1
    # and succeeds once there is enough signal
    assert find_period(np.array([1.0, 0.0, -1.0, 0.0] * 10), 20) == 4


def test_the_knn_predictor_cold_starts_at_random_with_too_little_history():
    predictor = FingerprintKNNPredictor(k=1, seed=3)
    for history in ([], [(1, 2, 3, 4, 5, 6)]):
        pick = predictor.predict(history)
        assert len(pick) == 6
        assert len(set(pick)) == 6
        assert all(1 <= n <= 49 for n in pick)
        assert list(pick) == sorted(pick)


def test_the_knn_predictor_pads_when_voting_yields_too_few_numbers():
    """A successor draw with repeated numbers votes for fewer than six
    distinct ones, so the random pad path runs."""
    predictor = FingerprintKNNPredictor(k=1, seed=5)
    history = [(1, 2, 3, 4, 5, 6), (7, 7, 7, 8, 8, 9)]
    pick = predictor.predict(history)
    assert len(pick) == 6
    assert len(set(pick)) == 6
    assert {7, 8, 9} <= set(pick)  # the voted numbers survive
    assert list(pick) == sorted(pick)


def test_match_probability_is_zero_outside_the_possible_range():
    assert match_probability(7) == 0            # cannot match more than drawn
    assert match_probability(-1) == 0
    assert match_probability(0, pool=6, picks=6, winning=6) == 0  # all must match
    assert sum(match_probability(m) for m in range(7)) == 1


def test_the_spherical_inverse_declines_rather_than_rounding():
    """Spherical data that no rational point produces comes back as None
    components instead of a rounded guess."""
    recovered = from_exact_spherical(
        Fraction(2), Fraction(1, 2), Fraction(1), (1, 1, 1)
    )
    assert recovered[2] == 1               # z^2 = 1 is a perfect square
    assert recovered[0] is None            # x^2 = 1/2 is not
    assert recovered[1] is None
    # real rational points still round-trip exactly
    point = (Fraction(3), Fraction(4), Fraction(12))
    assert from_exact_spherical(*exact_spherical(point)) == point


def test_cos_squared_declines_for_turn_fractions_outside_the_exact_set():
    for q in (Fraction(1, 5), Fraction(1, 7), Fraction(2, 9)):
        assert rational_cos_squared_of_turn(q) is None
    assert rational_cos_squared_of_turn(Fraction(1, 8)) == Fraction(1, 2)


# ------------------------------------------------- documented guards

def test_documented_guards_raise_with_their_contracts():
    with pytest.raises(ValueError):
        simulate_ar1(phi=1.0, n=10)              # non-stationary
    with pytest.raises(ValueError):
        simulate_ar1(phi=-1.5, n=10)
    with pytest.raises(ValueError):
        IFS([])                                   # an IFS needs a map
    with pytest.raises(ValueError):
        Process("bad", 0)                         # work_units must be positive
    with pytest.raises(ValueError):
        find_equilibrium(lo=0.0, hi=1.0)          # root not bracketed
    with pytest.raises(ValueError):
        sin_taylor(Fraction(1), terms=0)
    with pytest.raises(ValueError):
        balance_point(Fraction(1), Fraction(-1))  # weights sum to zero
    with pytest.raises(ValueError):
        center_of_mass([Fraction(1)], [Fraction(0), Fraction(1)])
    with pytest.raises(ValueError):
        harmonic_index(Fraction(440), Fraction(0))
    with pytest.raises(ValueError):
        layered_flow_bracket([Fraction(1), Fraction(2)], [Fraction(1)])
    with pytest.raises(ValueError):
        two_layer_flow_gain(Fraction(1, 2), Fraction(0))
    with pytest.raises(ValueError):
        process_state(Fraction(4), Fraction(3), -1)
    with pytest.raises(ValueError):
        lorentz_absorption(1.0, 0.0, 0.1, 1.0)    # resonance frequency zero
    with pytest.raises(ValueError):
        lorentz_dispersion(1.0, 1.0, 0.0, 1.0)    # zero damping
    with pytest.raises(ValueError):
        landau_critical_velocity([(0.0, 1.0)])    # no positive momenta
    with pytest.raises(ValueError):
        interface_velocity(0.0, STEEL, 1000.0)
    with pytest.raises(ValueError):
        cohesive_energy_fraction(1000.0, cohesive_energy=0.0)


def test_an_unknown_basis_name_raises_a_key_error_not_a_value_error():
    """The public contract is KeyError, and the message lists what is
    available. Checked rather than assumed -- the first draft of this
    file guessed ValueError and was wrong."""
    with pytest.raises(KeyError) as excinfo:
        hole_wert("kein_solcher_name", Fraction(2))
    assert "Unbekannte Groesse" in str(excinfo.value)
    assert "ecken" in str(excinfo.value)  # the message names the options


def test_the_reference_checker_trips_on_a_basis_entry_without_a_reference():
    """`_direkt_berechnen` exists so `hole_wert` can be checked against
    an independent recomputation rather than against itself. Its final
    raise is unreachable through the public API by construction -- it
    fires only if BASIS gains a name with no reference, which is exactly
    the mistake it is there to catch."""
    from raum27.basisoperationen import BASIS, _direkt_berechnen

    with pytest.raises(ValueError, match="Kein Referenztest"):
        _direkt_berechnen("noch_nicht_definiert", Fraction(1))
    # every name actually in BASIS does have one
    for name in BASIS:
        assert _direkt_berechnen(name, Fraction(1)) == hole_wert(name, Fraction(1))


def test_a_degenerate_impact_has_no_interface_velocity_at_all():
    """Equal densities AND zero velocity make both the quadratic and the
    linear coefficient vanish, so there is nothing to solve."""
    assert tate_interface_velocity(STEEL, STEEL, Y_STEEL, R_STEEL, 0.0) is None


def test_the_q144_state_exposes_its_phase_and_plane():
    """Two property accessors that nothing else in the suite reached."""
    from raum27.q144 import PLANES, State

    state = State(edge=0, phase=2, plane=1)
    assert state.phase_degrees == 180
    assert State(edge=0, phase=0, plane=0).phase_degrees == 0
    assert State(edge=0, phase=3, plane=0).phase_degrees == 270
    assert state.plane_name == PLANES[1]
    assert state.plane_name in PLANES


def test_remaining_dimension_and_length_guards():
    from raum27.kugelkoordinaten import exact_spherical as spherical
    from raum27.optionsraum import (
        squared_distance_from_centre,
        worst_squared_distance_to_a_single_wish,
    )
    from raum27.resonanztunnel import film_area_fraction
    from raum27.spirale import arc_after
    from raum27.tunnelgrenze import peak_absorption

    with pytest.raises(ValueError):
        hydrodynamic_penetration(0.0, STEEL, 0.6)
    with pytest.raises(ValueError):
        spherical((Fraction(1), Fraction(2)))        # not three-dimensional
    with pytest.raises(ValueError):
        squared_distance_from_centre([])
    with pytest.raises(ValueError):
        worst_squared_distance_to_a_single_wish([])
    with pytest.raises(ValueError):
        film_area_fraction([Fraction(1), Fraction(2)], [Fraction(1)], Fraction(1))
    with pytest.raises(ValueError):
        arc_after(Fraction(4), Fraction(3), -1)
    with pytest.raises(ValueError):
        peak_absorption(1.0, 0.0, 1.0)              # zero damping
    with pytest.raises(ValueError):
        peak_absorption(0.0, 0.1, 1.0)              # zero resonance frequency


def test_two_defensive_branches_are_left_uncovered_on_purpose():
    """`tate_interface_velocity`'s no-root-in-range return and
    `tate_penetration`'s zero-erosion break both guard against states the
    solver cannot produce: it constrains u to [0, v], so erosion is
    positive whenever a root exists.

    They are kept as tripwires in case that constraint is ever relaxed,
    and deliberately not chased with contrived inputs -- hitting them
    would move a percentage without testing anything real. Recorded here
    so the gap is a decision rather than an oversight."""
    for v in (500.0, 1500.0, 5000.0):
        u = tate_interface_velocity(STEEL, STEEL, Y_STEEL, R_STEEL, v)
        if u is not None:
            assert 0.0 <= u <= v      # the invariant that makes them unreachable
            assert (v - u) >= 0.0


def test_option_space_guards():
    with pytest.raises(ValueError):
        uniform_wish(0)
    with pytest.raises(ValueError):
        single_wish(0, 0)
    with pytest.raises(ValueError):
        single_wish(3, 5)                         # index out of range
    with pytest.raises(ValueError):
        single_wish(3, -1)
    with pytest.raises(ValueError):
        squared_distance(uniform_wish(2), uniform_wish(3))
