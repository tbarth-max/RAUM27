"""Tests for raum27.impakt_schwelle."""
from __future__ import annotations

import math
from fractions import Fraction

import pytest

from raum27.impakt_schwelle import (
    DENSITY,
    IRON_COHESIVE_ENERGY,
    SPECIFIC_HEAT,
    YIELD_STRENGTH,
    ballistic_limit_velocity,
    cohesive_energy_fraction,
    dynamic_pressure,
    erosion_time,
    flow_threshold_velocity,
    hydrodynamic_penetration,
    interface_velocity,
    johnson_damage_number,
    penetration_from_time,
    shock_temperature_rise,
    tate_interface_velocity,
    tate_penetration,
)


def test_the_threshold_is_exactly_where_pressure_equals_strength():
    """D = 1 is not a fitted constant: at the threshold velocity the
    dynamic pressure is exactly half the yield strength, because
    D = rho*v^2/Y and p = rho*v^2/2."""
    for m in DENSITY:
        v = flow_threshold_velocity(DENSITY[m], YIELD_STRENGTH[m])
        assert johnson_damage_number(DENSITY[m], v, YIELD_STRENGTH[m]) == pytest.approx(1.0)
        assert dynamic_pressure(DENSITY[m], v) == pytest.approx(YIELD_STRENGTH[m] / 2)


def test_the_threshold_velocities_are_the_published_order_of_magnitude():
    assert flow_threshold_velocity(DENSITY["steel"], YIELD_STRENGTH["steel"]) == pytest.approx(356.9, abs=0.5)
    assert flow_threshold_velocity(DENSITY["copper"], YIELD_STRENGTH["copper"]) == pytest.approx(149.4, abs=0.5)
    assert flow_threshold_velocity(DENSITY["lead"], YIELD_STRENGTH["lead"]) == pytest.approx(32.5, abs=0.5)
    # lead gives way at an order of magnitude lower speed than steel
    assert (flow_threshold_velocity(DENSITY["steel"], YIELD_STRENGTH["steel"])
            > 10 * flow_threshold_velocity(DENSITY["lead"], YIELD_STRENGTH["lead"]))


def test_damage_number_separates_the_three_regimes():
    rho, y = DENSITY["steel"], YIELD_STRENGTH["steel"]
    assert johnson_damage_number(rho, 10.0, y) < 0.01          # elastic
    assert 0.9 < johnson_damage_number(rho, 357.0, y) < 1.1     # onset
    assert johnson_damage_number(rho, 2000.0, y) > 30           # strength irrelevant
    assert johnson_damage_number(rho, 8000.0, y) > 500


def test_dynamic_pressure_dwarfs_strength_at_impact_speeds():
    """15.7 GPa against a 1 GPa yield strength at 2 km/s -- that ratio,
    not any heat, is why the lattice stops holding."""
    p = dynamic_pressure(DENSITY["steel"], 2000.0)
    assert p == pytest.approx(1.57e10, rel=1e-3)
    assert p > 15 * YIELD_STRENGTH["steel"]


def test_the_dx_dt_route_and_the_closed_form_agree_exactly():
    """u from the pressure balance, t = L/(v-u), P = u*t -- reproduces
    L*sqrt(rho_j/rho_t) to floating point, for every pairing and speed.
    The kinematic framing IS the derivation."""
    for rod in ("copper", "tungsten", "steel", "aluminium"):
        for target in ("steel", "aluminium", "copper"):
            for v in (800.0, 1500.0, 2500.0, 8000.0):
                u = interface_velocity(DENSITY[rod], DENSITY[target], v)
                t = erosion_time(0.600, v, u)
                assert penetration_from_time(u, t) == pytest.approx(
                    hydrodynamic_penetration(DENSITY[rod], DENSITY[target], 0.600), rel=1e-12
                )


def test_the_depth_ratio_identity_is_algebraically_exact():
    """P/L = 1/k where k = sqrt(rho_t/rho_j), checked symbolically over
    exact rationals so no float rounding can hide a mismatch:
    u = v/(1+k), v-u = v*k/(1+k), P = u*L/(v-u) = L/k."""
    for k in (Fraction(1, 2), Fraction(2), Fraction(3, 7), Fraction(16, 9)):
        for v in (Fraction(1500), Fraction(8000)):
            L = Fraction(3, 5)
            u = v / (1 + k)
            assert v - u == v * k / (1 + k)
            assert u * (L / (v - u)) == L / k


def test_penetration_depth_does_not_depend_on_impact_velocity():
    """The surprising part of the 1948 result."""
    depths = {
        round(penetration_from_time(
            interface_velocity(DENSITY["tungsten"], DENSITY["steel"], v),
            erosion_time(0.600, v, interface_velocity(DENSITY["tungsten"], DENSITY["steel"], v)),
        ), 9)
        for v in (900.0, 1500.0, 2500.0, 5000.0, 8000.0, 20000.0)
    }
    assert len(depths) == 1


def test_published_depth_ratios():
    assert hydrodynamic_penetration(DENSITY["copper"], DENSITY["steel"], 1.0) == pytest.approx(1.068, abs=1e-3)
    assert hydrodynamic_penetration(DENSITY["tungsten"], DENSITY["steel"], 1.0) == pytest.approx(1.568, abs=1e-3)
    assert hydrodynamic_penetration(DENSITY["aluminium"], DENSITY["steel"], 1.0) == pytest.approx(0.587, abs=1e-3)
    # same material in and out: exactly its own length
    assert hydrodynamic_penetration(DENSITY["steel"], DENSITY["steel"], 0.6) == pytest.approx(0.6)


def test_the_process_is_not_cold_steel_passes_its_melting_point():
    """REFUTES the 'kalter Phasenuebergang' framing: shock heating alone
    takes steel past melting at a particle velocity around 1160 m/s."""
    cp = SPECIFIC_HEAT["steel"]
    assert shock_temperature_rise(500.0, cp) == pytest.approx(277.8, abs=1.0)
    assert shock_temperature_rise(1000.0, cp) == pytest.approx(1111.1, abs=1.0)
    melt_rise = 1500.0
    v_melt = math.sqrt(2 * cp * melt_rise)
    assert v_melt == pytest.approx(1162.0, abs=2.0)
    assert shock_temperature_rise(1270.0, cp) > melt_rise
    assert shock_temperature_rise(4000.0, cp) > 10_000.0


def test_the_energy_does_not_go_restlos_into_lattice_bonds():
    """REFUTES the energy-bookkeeping claim: at ordnance velocity the
    impact does not even bring enough energy per unit mass to break all
    the bonds, let alone spend it all that way."""
    assert IRON_COHESIVE_ENERGY == pytest.approx(7.39e6, rel=5e-3)
    assert cohesive_energy_fraction(1700.0) == pytest.approx(0.195, abs=5e-3)
    assert cohesive_energy_fraction(1000.0) < 0.07
    for v in (500.0, 1000.0, 1700.0, 2000.0, 3000.0):
        assert cohesive_energy_fraction(v) < 1.0
    break_even = math.sqrt(2 * IRON_COHESIVE_ENERGY)
    assert break_even == pytest.approx(3844.0, abs=10.0)
    assert cohesive_energy_fraction(break_even) == pytest.approx(1.0)
    assert cohesive_energy_fraction(8000.0) > 4.0


def test_strength_always_reduces_penetration_never_increases_it():
    """Physical sanity, and the bug that showed up first time round: the
    Tate result must sit below the strengthless limit at every speed."""
    L = 0.600
    hyd = hydrodynamic_penetration(DENSITY["tungsten"], DENSITY["steel"], L)
    for v in (800.0, 1200.0, 1700.0, 2500.0, 5000.0, 10000.0, 20000.0):
        p = tate_penetration(
            DENSITY["tungsten"], DENSITY["steel"],
            YIELD_STRENGTH["tungsten"], 3.5 * YIELD_STRENGTH["steel"], v, L,
        )
        assert 0.0 <= p < hyd


def test_tate_approaches_the_hydrodynamic_ceiling_monotonically_from_below():
    L = 0.600
    hyd = hydrodynamic_penetration(DENSITY["tungsten"], DENSITY["steel"], L)
    ratios = [
        tate_penetration(
            DENSITY["tungsten"], DENSITY["steel"],
            YIELD_STRENGTH["tungsten"], 3.5 * YIELD_STRENGTH["steel"], v, L,
        ) / hyd
        for v in (2000.0, 5000.0, 10000.0, 50000.0)
    ]
    assert all(b > a for a, b in zip(ratios, ratios[1:]))
    assert all(r < 1.0 for r in ratios)
    assert ratios[-1] > 0.99


def test_the_strength_model_matches_real_long_rod_performance():
    """Validation against the world: a 0.6 m tungsten rod at 1700 m/s
    reaches P/L ~ 1.21 against steel, which is the band real long-rod
    penetrators sit in -- while the strengthless limit says 1.57. The
    ceiling is a ceiling, not a prediction."""
    L = 0.600
    p = tate_penetration(
        DENSITY["tungsten"], DENSITY["steel"],
        YIELD_STRENGTH["tungsten"], 3.5 * YIELD_STRENGTH["steel"], 1700.0, L,
    )
    assert 1.0 < p / L < 1.3
    assert hydrodynamic_penetration(DENSITY["tungsten"], DENSITY["steel"], L) / L > 1.5


def test_there_is_a_ballistic_limit_the_strengthless_model_cannot_express():
    """Below a cutoff nothing penetrates at all. The hydrodynamic
    formula has no velocity in it and so predicts full penetration at
    1 m/s, which is the clearest sign it is only a high-speed limit."""
    v_lim = ballistic_limit_velocity(
        DENSITY["tungsten"], DENSITY["steel"],
        YIELD_STRENGTH["tungsten"], 3.5 * YIELD_STRENGTH["steel"],
    )
    assert 400.0 < v_lim < 520.0
    assert tate_interface_velocity(
        DENSITY["tungsten"], DENSITY["steel"],
        YIELD_STRENGTH["tungsten"], 3.5 * YIELD_STRENGTH["steel"], v_lim * 0.5,
    ) in (None, 0.0)
    # and the strengthless model happily "penetrates" at walking pace
    assert hydrodynamic_penetration(DENSITY["tungsten"], DENSITY["steel"], 0.6) > 0.9


def test_a_slower_rod_is_consumed_more_slowly():
    """The measurable dt: halving the impact speed roughly doubles the
    traversal time, which is what makes the velocity recoverable from
    the time."""
    times = []
    for v in (1000.0, 2000.0, 4000.0):
        u = interface_velocity(DENSITY["tungsten"], DENSITY["steel"], v)
        times.append(erosion_time(0.600, v, u))
    assert times[0] == pytest.approx(2 * times[1], rel=1e-9)
    assert times[1] == pytest.approx(2 * times[2], rel=1e-9)


def test_degenerate_inputs_raise_instead_of_returning_nonsense():
    with pytest.raises(ValueError):
        johnson_damage_number(DENSITY["steel"], 100.0, 0.0)
    with pytest.raises(ValueError):
        flow_threshold_velocity(0.0, 1e9)
    with pytest.raises(ValueError):
        interface_velocity(0.0, DENSITY["steel"], 1000.0)
    with pytest.raises(ValueError):
        shock_temperature_rise(1000.0, 0.0)
    with pytest.raises(ValueError):
        erosion_time(0.6, 1000.0, 1000.0)  # rod not being consumed
