import pytest

from raum27.q144 import (
    NUM_STATES,
    State,
    all_states,
    operator_period,
    orbit,
    phi,
)


def test_q144_has_144_states():
    states = all_states()
    assert len(states) == NUM_STATES == 144
    assert len(set(states)) == 144


def test_state_rejects_out_of_range_coordinates():
    with pytest.raises(ValueError):
        State(12, 0, 0)
    with pytest.raises(ValueError):
        State(0, 4, 0)
    with pytest.raises(ValueError):
        State(0, 0, 3)


def test_phi_is_a_bijection_on_q144():
    states = all_states()
    images = {phi(s) for s in states}
    assert images == set(states)


def test_phi_advances_each_coordinate_by_one_mod_its_modulus():
    s = State(11, 3, 2)
    assert phi(s) == State(0, 0, 0)


def test_operator_period_is_twelve():
    assert operator_period() == 12


def test_every_orbit_has_length_twelve():
    for s in all_states():
        assert len(orbit(s)) == 12


def test_orbit_returns_to_start_after_period_applications():
    s = State(5, 1, 2)
    current = s
    for _ in range(operator_period()):
        current = phi(current)
    assert current == s


def test_144_states_decompose_into_twelve_orbits_of_twelve():
    remaining = set(all_states())
    orbits = []
    while remaining:
        s = next(iter(remaining))
        o = orbit(s)
        orbits.append(o)
        remaining -= set(o)
    assert len(orbits) == 12
    assert all(len(o) == 12 for o in orbits)
