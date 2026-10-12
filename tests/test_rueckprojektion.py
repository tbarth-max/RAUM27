"""Tests for raum27.rueckprojektion: four circles and the negative inside radius 1."""

from fractions import Fraction
from math import gcd, lcm

import pytest

from raum27.rueckprojektion import (
    IN,
    OCTANTS,
    OUT,
    SEXTANTS,
    circle_number,
    circle_point,
    circle_state,
    connection_repeat,
    corner_path,
    delta_in,
    delta_out,
    direction_label,
    eight_round_trips,
    hologram,
    inner_gap,
    integer_similarity_3d_possible,
    inward,
    ladder_is_self_inverse,
    multiply,
    negative,
    outward,
    point_reflection,
    retrace,
    squared_length,
    surface_meeting,
    wavelength,
)

F = Fraction


def test_out_and_in_cancel_exactly():
    assert multiply(OUT, IN) == (1, 0)
    for z in [(1, 0), (1, 1), (F(3, 7), F(-2, 5))]:
        assert inward(outward(z)) == (F(z[0]), F(z[1]))


def test_each_outward_step_doubles_squared_radius_and_turns_one_direction():
    for k in range(40):
        z = circle_point(k)
        assert squared_length(z) == 2 ** k
        assert direction_label(z) == k % 8 + 1


def test_full_turn_is_times_sixteen():
    assert circle_point(8) == (16, 0)


def test_four_deltas_cross_axis_and_diagonal():
    assert delta_out((1, 0)) == (0, 1)
    assert delta_in((1, 0)) == (F(-1, 2), F(-1, 2))
    assert delta_out((1, 1)) == (-1, 1)
    assert delta_in((1, 1)) == (0, -1)
    for z in [(1, 0), (1, 1), (0, 2), (-2, 2)]:
        assert squared_length(delta_out(z)) == squared_length(z)
        assert squared_length(delta_in(z)) == squared_length(z) / 2


def test_state_round_trip_and_reach_of_300_million():
    for k in range(200):
        assert circle_number(*circle_state(k)) == k
    assert circle_state(56) == (7, 1)
    assert squared_length(circle_point(56)) == 2 ** 56  # radius 2**28
    assert 2 ** 28 < 300_000_000 < 2 ** 29


@pytest.mark.parametrize("call", [
    lambda: circle_state(-1),
    lambda: circle_number(0, 9),
    lambda: circle_number(-1, 1),
    lambda: direction_label((0, 0)),
    lambda: direction_label((2, 1)),
    lambda: corner_path((1, 0, 0)),
])
def test_invalid_inputs_are_refused(call):
    with pytest.raises(ValueError):
        call()


def test_corner_by_deltas_and_back():
    assert len(SEXTANTS) == 6 and len(OCTANTS) == 8
    for octant in OCTANTS:
        path = corner_path(octant)
        assert [squared_length(p) for p in path] == [0, 1, 2, 3]
        assert path[-1] == octant
        assert retrace(path)[-1] == (0, 0, 0)
    assert eight_round_trips() == (0, 0, 0)


def test_three_d_has_no_exact_root_two_or_root_three_rotation():
    assert not integer_similarity_3d_possible(2)
    assert not integer_similarity_3d_possible(3)
    assert integer_similarity_3d_possible(9)
    assert integer_similarity_3d_possible(1)


def test_hologram_is_inside_radius_one_and_an_involution():
    body = {(r, d) for r in range(1, 301) for d in OCTANTS if (r * (d[0] + 2)) % 3 == 0}
    inner = hologram(body)
    assert all(radius <= 1 for radius, _ in inner)
    assert hologram(inner) == {(F(r), d) for r, d in body}
    assert {r for r, _ in hologram({(n, OCTANTS[0]) for n in (2, 3, 4, 5)})} == {
        F(1, 2), F(1, 3), F(1, 4), F(1, 5)}


def test_negative_and_point_reflection_are_involutions_and_commute_with_inversion():
    radii = range(1, 13)
    body = {(r, d) for r in radii for d in SEXTANTS if (r + d[0] + 2 * d[1]) % 2 == 0}
    assert negative(negative(body, radii, SEXTANTS), radii, SEXTANTS) == {(F(r), d) for r, d in body}
    assert point_reflection(point_reflection(body)) == body
    assert hologram(point_reflection(body)) == point_reflection(hologram(body))


def test_linear_circles_crowd_but_a_geometric_ladder_maps_onto_itself():
    assert inner_gap(300) == F(1, 89700)
    assert not ladder_is_self_inverse(range(1, 301))
    assert ladder_is_self_inverse([F(2) ** k for k in range(-28, 29)])


def test_frequency_and_wavelength_swap_lcm_and_gcd():
    for f in range(1, 61):
        for g in range(1, 61):
            assert wavelength(f) * f == 1
            assert surface_meeting(f, g) == lcm(f, g)
            assert connection_repeat(f, g) == F(1, gcd(f, g))
            assert surface_meeting(f, g) * gcd(f, g) == f * g
    assert lcm(*range(1, 10)) == lcm(*range(1, 11)) == 2520
