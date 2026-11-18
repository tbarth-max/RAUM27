"""Tests for raum27.tunnelgrenze."""
from __future__ import annotations

import math
from fractions import Fraction

import pytest

from raum27.lichtgitter import SPEED_OF_LIGHT
from raum27.tunnelgrenze import (
    ELECTRON_MASS,
    ELECTRONVOLT,
    HBAR,
    PLANCK_MASS,
    PLANCK_TIME,
    absorption_sum_rule,
    energy_at_planck_time,
    free_particle_critical_velocity,
    front_velocity,
    gap_needed_for_critical_velocity,
    gapped_critical_velocity,
    landau_critical_velocity,
    lorentz_absorption,
    lorentz_dispersion,
    lossless_resonance_is_possible,
    minimum_energy_for_time_resolution,
    minimum_transit_time,
    peak_absorption,
    refractive_index,
    roton_critical_velocity,
    transmitted_distance_is_the_minimised_quantity,
)


def _sum_rule_numeric(omega_0: float, gamma: float, strength: float) -> float:
    """Integrate w*Im chi with the Lorentzian peak properly resolved --
    a uniform grid under-resolves it badly for small damping, which is a
    quadrature artefact and not a physical result."""
    total = 0.0
    lo, hi = max(0.0, omega_0 - 60 * gamma), omega_0 + 60 * gamma
    n = 40000
    h = (hi - lo) / n
    for i in range(n):
        w = lo + (i + 0.5) * h
        total += w * lorentz_absorption(w, omega_0, gamma, strength) * h
    for a, b in ((0.0, lo), (hi, hi + 4000 * omega_0)):
        if b <= a:
            continue
        m = 20000
        h2 = (b - a) / m
        for i in range(m):
            w = a + (i + 0.5) * h2
            total += w * lorentz_absorption(w, omega_0, gamma, strength) * h2
    return total


def test_the_total_absorption_does_not_depend_on_the_damping():
    """THE DECISIVE RESULT: the f-sum rule. Total absorption is fixed by
    the oscillator strength alone, across six decades of damping and two
    resonance frequencies."""
    exact = absorption_sum_rule(1.0)
    assert exact == pytest.approx(math.pi / 2)
    for omega_0 in (1.0, 3.0):
        for gamma in (1.0, 1e-1, 1e-2, 1e-3, 1e-4, 1e-5):
            numeric = _sum_rule_numeric(omega_0, gamma, 1.0)
            assert numeric == pytest.approx(exact, rel=5e-3)


def test_shrinking_the_damping_concentrates_the_absorption_it_does_not_remove_it():
    """Peak height goes as 1/gamma while the integral stays put."""
    peaks = [peak_absorption(1.0, g, 1.0) for g in (1.0, 1e-2, 1e-4, 1e-6)]
    assert peaks == [1.0, 1e2, 1e4, 1e6]
    for g in (1.0, 1e-2, 1e-4):
        assert peak_absorption(1.0, g, 1.0) == pytest.approx(1 / g)
    # taller peak, same total
    assert peaks[-1] / peaks[0] == pytest.approx(1e6)
    assert absorption_sum_rule(1.0) == pytest.approx(math.pi / 2)


def test_the_strength_that_makes_the_resonance_is_the_strength_that_absorbs():
    """Both dispersion and absorption are proportional to wp², so you
    cannot keep one and drop the other."""
    for strength in (0.5, 1.0, 7.0):
        assert lorentz_absorption(1.0, 1.0, 0.1, strength) == pytest.approx(
            strength * lorentz_absorption(1.0, 1.0, 0.1, 1.0)
        )
        assert lorentz_dispersion(0.5, 1.0, 0.1, strength) == pytest.approx(
            strength * lorentz_dispersion(0.5, 1.0, 0.1, 1.0)
        )
        assert absorption_sum_rule(strength) == pytest.approx(math.pi * strength / 2)
    # zero strength: no absorption, but also no dispersion anywhere
    for w in (0.1, 0.5, 1.0, 2.0, 10.0):
        assert lorentz_absorption(w, 1.0, 0.1, 0.0) == 0.0
        assert lorentz_dispersion(w, 1.0, 0.1, 0.0) == 0.0


def test_a_lossless_resonance_is_an_empty_set_not_a_hard_target():
    assert lossless_resonance_is_possible() is False


def test_the_kramers_kronig_relation_holds_for_the_medium_used():
    """So the premise doing the work is the real one: Re chi reconstructed
    from Im chi by the dispersion integral matches Re chi directly."""
    omega_0, gamma, strength = 1.0, 0.2, 1.0
    n, w_max = 400000, 200.0
    h = w_max / n
    for w in (0.3, 0.7, 1.5, 3.0):
        acc = 0.0
        for i in range(n):
            wp = (i + 0.5) * h
            den = wp * wp - w * w
            if abs(den) < 1e-9:
                continue
            acc += wp * lorentz_absorption(wp, omega_0, gamma, strength) / den * h
        reconstructed = 2 / math.pi * acc
        direct = lorentz_dispersion(w, omega_0, gamma, strength)
        assert reconstructed == pytest.approx(direct, abs=5e-3)


def test_resolving_a_shorter_time_costs_more_energy_not_less():
    """The two halves of the request are opposite ends of one
    inequality."""
    energies = [minimum_energy_for_time_resolution(dt)
                for dt in (1e-9, 1e-15, 1e-18, 1e-21)]
    assert all(b > a for a, b in zip(energies, energies[1:]))
    assert minimum_energy_for_time_resolution(1e-15) == pytest.approx(5.2729e-20, rel=1e-3)
    # halving the time exactly doubles the energy floor
    assert minimum_energy_for_time_resolution(1e-15) == pytest.approx(
        2 * minimum_energy_for_time_resolution(2e-15)
    )


def test_the_planck_time_costs_half_a_planck_mass():
    e = energy_at_planck_time()
    assert e == pytest.approx(9.78e8, rel=1e-2)
    assert e / SPEED_OF_LIGHT ** 2 / PLANCK_MASS == pytest.approx(0.5, abs=1e-3)
    # in TNT-equivalent terms, in a single quantum event
    assert e / 4.184e9 == pytest.approx(0.234, abs=0.01)
    assert e == pytest.approx(HBAR / (2 * PLANCK_TIME))


def test_frictionless_flow_is_real_and_its_speed_is_tiny():
    """Superfluid helium from its roton parameters -- a check against the
    measured ~58 m/s, not a definition."""
    v = roton_critical_velocity()
    assert v == pytest.approx(59.3, abs=0.5)
    assert 50.0 < v < 70.0
    assert v / SPEED_OF_LIGHT == pytest.approx(1.98e-7, rel=1e-2)
    assert v < SPEED_OF_LIGHT / 10 ** 6


def test_landau_criterion_picks_the_minimum_of_energy_over_momentum():
    """Needs no knowledge of the medium -- only that it has excitations,
    which 'defined interactions' already grants."""
    # a linear phonon branch: eps = cs*p gives v_c = cs exactly
    cs = 240.0
    spectrum = [(p, cs * p) for p in (1e-25, 1e-24, 1e-23)]
    assert landau_critical_velocity(spectrum) == pytest.approx(cs)
    # add a roton-like dip and the minimum moves to it
    with_dip = spectrum + [(2.0e-24, 1.19e-22)]
    assert landau_critical_velocity(with_dip) < cs
    assert landau_critical_velocity(with_dip) == pytest.approx(59.5, abs=1.0)


def test_an_ungapped_medium_has_no_frictionless_regime_at_all():
    """eps = p²/2m gives eps/p = p/2m, whose infimum is 0: a gap is what
    creates the frictionless regime in the first place."""
    assert free_particle_critical_velocity() == 0.0
    # sampling p²/2m: the ratio keeps falling as p falls
    ratios = [(p ** 2 / (2 * ELECTRON_MASS)) / p for p in (1e-24, 1e-25, 1e-26, 1e-27)]
    assert all(b < a for a, b in zip(ratios, ratios[1:]))
    assert ratios[-1] < ratios[0] / 100


def test_a_faster_frictionless_regime_needs_a_bigger_gap():
    velocities = [gapped_critical_velocity(d * ELECTRONVOLT, ELECTRON_MASS)
                  for d in (1e-3, 1.0, 1e3, 1e6)]
    assert all(b > a for a, b in zip(velocities, velocities[1:]))
    assert velocities[1] == pytest.approx(5.93e5, rel=1e-2)
    # quadrupling the gap doubles the critical velocity
    assert gapped_critical_velocity(4.0, 1.0) == pytest.approx(
        2 * gapped_critical_velocity(1.0, 1.0)
    )


def test_pushing_the_critical_velocity_to_c_needs_a_rest_energy_gap():
    """At which point pair production opens and the no-interaction
    premise has destroyed itself."""
    gap = gap_needed_for_critical_velocity(float(SPEED_OF_LIGHT), ELECTRON_MASS)
    assert gap == pytest.approx(ELECTRON_MASS * SPEED_OF_LIGHT ** 2 / 2)
    assert gap / ELECTRONVOLT == pytest.approx(2.555e5, rel=1e-3)
    # exactly half the electron rest energy
    rest = ELECTRON_MASS * SPEED_OF_LIGHT ** 2
    assert gap / rest == pytest.approx(0.5)
    # and the inverse is consistent
    assert gapped_critical_velocity(gap, ELECTRON_MASS) == pytest.approx(
        float(SPEED_OF_LIGHT)
    )


def test_the_refractive_index_tends_to_one_so_the_front_moves_at_c():
    """Causality alone fixes this -- which is why an unknown field is
    bound as tightly as a known one."""
    deviations = [abs(refractive_index(w, 1.0, 0.2, 1.0) - 1.0)
                  for w in (1e1, 1e2, 1e3, 1e4, 1e6)]
    assert all(b < a for a, b in zip(deviations, deviations[1:]))
    assert deviations[0] == pytest.approx(5.06e-3, rel=5e-2)
    assert deviations[-1] < 1e-11
    assert front_velocity() == SPEED_OF_LIGHT


def test_the_minimum_transit_time_is_exactly_distance_over_c():
    assert minimum_transit_time(Fraction(1)) == Fraction(1, SPEED_OF_LIGHT)
    assert float(minimum_transit_time(Fraction(1))) == pytest.approx(3.3356e-9, rel=1e-3)
    assert float(minimum_transit_time(Fraction(1000))) == pytest.approx(3.3356e-6, rel=1e-3)
    moon = Fraction(3844, 10) * 10 ** 6
    assert float(minimum_transit_time(moon)) == pytest.approx(1.2822, rel=1e-3)
    # exactly zero only for zero distance -- i.e. for no transfer
    assert minimum_transit_time(Fraction(0)) == 0


def test_shrinking_the_path_to_zero_transmits_nothing():
    assert transmitted_distance_is_the_minimised_quantity() is True
    assert minimum_transit_time(Fraction(0)) == 0
    # the time falls only in proportion to the distance that is given up
    for d in (Fraction(1), Fraction(1, 10), Fraction(1, 1000)):
        assert minimum_transit_time(d) / d == Fraction(1, SPEED_OF_LIGHT)


def test_degenerate_inputs_raise():
    with pytest.raises(ValueError):
        minimum_energy_for_time_resolution(0.0)
    with pytest.raises(ValueError):
        minimum_energy_for_time_resolution(-1e-20)
    with pytest.raises(ValueError):
        lorentz_absorption(1.0, 1.0, 0.0, 1.0)
    with pytest.raises(ValueError):
        gapped_critical_velocity(1.0, 0.0)
    with pytest.raises(ValueError):
        gap_needed_for_critical_velocity(1.0, 0.0)
    with pytest.raises(ValueError):
        landau_critical_velocity([])
    with pytest.raises(ValueError):
        minimum_transit_time(Fraction(-1))
