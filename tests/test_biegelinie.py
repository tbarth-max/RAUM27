"""Tests for raum27.biegelinie: bending lines from chained arcs."""

from fractions import Fraction
import math

import pytest

from raum27.biegelinie import (
    arc_chain,
    cantilever_end_load,
    centre_load,
    deflection_at,
    dynamic_amplification,
    pieces_for_tolerance,
    slope_chain,
    supported,
    supported_exact,
    three_point_chain,
    uniform_load,
)

F = Fraction
P = F(1, 1000)  # small load: the closed forms are small-deflection results


def _cantilever(x):
    return P * (1 - x)


def _centre(x):
    return P * min(x, 1 - x) / 2


def _uniform(x):
    return P * x * (1 - x) / 2


def test_arc_chain_converges_with_square_of_pieces():
    for build, x_at, ref, on_supports in [
        (cantilever_end_load, 1.0, None, False),
        (centre_load, 0.5, None, True),
        (uniform_load, 0.5, None, True),
    ]:
        k, ref = build(1e-3, 1.0, 1.0)
        errors = []
        for n in (8, 16, 32):
            pts = arc_chain(k, 1.0, n)
            if on_supports:
                pts = supported(pts)
            errors.append(abs(abs(deflection_at(pts, x_at)) - ref) / ref)
        assert 3.5 < errors[0] / errors[1] < 4.5 and 3.5 < errors[1] / errors[2] < 4.5


def test_one_point_rational_chain_is_close_but_not_exact():
    pts = slope_chain(_cantilever, 1, 64)
    w = deflection_at(pts, 1)
    assert w != F(1, 3000)
    assert abs(w - F(1, 3000)) / F(1, 3000) < F(1, 10000)


@pytest.mark.parametrize("pieces", [1, 2, 3, 5, 8])
def test_three_point_chain_is_exact_for_the_cantilever(pieces):
    pts = three_point_chain(_cantilever, 1, pieces)
    assert pts[-1][1] == F(1, 3000)  # P L^3 / 3 EI
    # every node lies on w(x) = P x^2 (3L - x) / 6 EI
    assert all(w == P * x * x * (3 - x) / 6 for x, w in pts)


@pytest.mark.parametrize("pieces", [2, 4, 6, 10])
def test_three_point_chain_is_exact_on_two_supports(pieces):
    centre = supported_exact(three_point_chain(_centre, 1, pieces))
    assert -deflection_at(centre, F(1, 2)) == F(1, 48000)  # P L^3 / 48 EI
    uniform = supported_exact(three_point_chain(_uniform, 1, pieces))
    assert -deflection_at(uniform, F(1, 2)) == F(5, 384000)  # 5 q L^4 / 384 EI


def test_uniform_load_exact_at_every_node_even_for_odd_pieces():
    pts = supported_exact(three_point_chain(_uniform, 1, 7))
    assert all(-w == P * x * (1 - 2 * x ** 2 + x ** 3) / 24 for x, w in pts)


def test_kink_inside_a_piece_breaks_exactness():
    # the centre load bends sharply at mid-span; with 3 pieces the kink is inside one
    pts = supported_exact(three_point_chain(_centre, 1, 3))
    exact = lambda x: P * x * (3 - 4 * x * x) / 48 if x <= F(1, 2) else exact(1 - x)
    assert any(-w != exact(x) for x, w in pts[1:-1])


def test_bridge_of_one_hundred_metres():
    # steel E = 210 GPa, I = 1 m^4, uniform load 100 kN/m, span 100 m
    EI, q, L = 210 * 10 ** 9, 100_000, 100
    pts = supported_exact(three_point_chain(lambda x: F(q) * x * (L - x) / (2 * EI), L, 10))
    sag = -deflection_at(pts, 50)
    assert sag == F(5 * q * L ** 4, 384 * EI)
    assert 0.62 < float(sag) < 0.621  # metres


def test_pieces_for_tolerance_finds_a_count_and_refuses_impossible():
    k, ref = cantilever_end_load(1e-3, 1.0, 1.0)
    n, w = pieces_for_tolerance(lambda m: arc_chain(k, 1.0, m)[-1][1], 1e-9)
    assert abs(w - ref) < 1e-8 and n <= 1024
    with pytest.raises(ValueError):
        pieces_for_tolerance(lambda m: float(m), 0.5, limit=64)


def test_invalid_piece_counts():
    for chain in (arc_chain, slope_chain, three_point_chain):
        with pytest.raises(ValueError):
            chain(_cantilever, 1, 0)


def test_dynamic_amplification():
    assert dynamic_amplification(math.inf) == 2       # permanent load put on suddenly
    assert dynamic_amplification(F(1, 2)) == 2
    assert dynamic_amplification(F(1, 6)) == pytest.approx(1.0)   # 2 sin(pi/6)
    assert dynamic_amplification(F(1, 100)) < 0.07    # short impulse: far below static
    with pytest.raises(ValueError):
        dynamic_amplification(0)
