"""Tests for raum27.nennerordnung."""

from fractions import Fraction

import pytest

from raum27.nennerordnung import (
    Power, by_denominator, on_common_denominator, path_from_time, time_from_path, unit_free,
)


def test_roots_as_fractional_exponents_multiply_exactly():
    r2, r8 = Power.of(2).root(2), Power.of(8).root(2)
    assert repr(r2) == "2^(1/2)"
    assert (r2 * r8).rational() == 4
    assert (Power.of(Fraction(9, 4)).root(2)).rational() == Fraction(3, 2)
    assert Power.of(2).root(2).rational() is None
    assert Power.of(12).root(2) == Power.of(2) * Power.of(3).root(2)      # sqrt 12 = 2 sqrt 3
    assert (Power.of(6) / Power.of(6)).rational() == 1 and repr(Power.of(1)) == "1"
    assert repr(Power.of(Fraction(4, 3)).root(3)) == "2^(2/3)·3^(-1/3)"
    assert len({Power.of(4).root(2), Power.of(2)}) == 1
    with pytest.raises(ValueError):
        Power.of(0)


def test_order_without_evaluating_a_root():
    assert Power.of(2).root(2) < Power.of(3).root(3)                       # 8 < 9 after the 6th power
    assert Power.of(3).root(3) < Power.of(Fraction(3, 2))
    assert not Power.of(2).root(2) < Power.of(2).root(2)
    assert Power.of(2) ** Fraction(1, 2) == Power.of(2).root(2)


def test_common_denominator_and_circles():
    pairs = [(1, 3), (2, 6), (1, 4), (3, 4), (5, 12), (-1, -2)]
    n, nums = on_common_denominator(pairs)
    assert n == 12 and nums == [4, 4, 3, 9, 5, 6]
    groups = by_denominator(pairs)
    assert list(groups) == [2, 3, 4, 12]
    assert groups[3] == [(1, 3), (2, 6)]                                   # same point, both origins kept
    assert groups[4] == [(1, 4), (3, 4)]
    with pytest.raises(ZeroDivisionError):
        on_common_denominator([(1, 0)])


def test_units_out_and_time_as_path():
    assert unit_free(Fraction(33, 10), Fraction(33, 100)) == 10
    s = path_from_time(Fraction(1, 10), 330)
    assert s == 33 and time_from_path(s, 330) == Fraction(1, 10)
    assert time_from_path(s, 300000000) == Fraction(11, 100000000)
    with pytest.raises(ZeroDivisionError):
        unit_free(1, 0)
    with pytest.raises(ValueError):
        time_from_path(1, 0)
    with pytest.raises(TypeError):
        unit_free(0.5, 1)


def test_every_world_in_its_own_unit():
    from raum27.nennerordnung import in_world, light_time, to_metres
    assert in_world(Fraction(5, 10 ** 9)) == (5, "nm")
    assert in_world(Fraction(3, 10 ** 5)) == (30, "µm")
    assert in_world(Fraction(33, 10)) == (Fraction(33, 10), "m")
    assert in_world(384400000) == (Fraction(3844, 10), "Mm")             # Earth to Moon
    assert in_world(Fraction(1, 10 ** 12)) == (Fraction(1, 1000), "nm")  # below the ladder: stays exact
    for v, u in ((7, "nm"), (Fraction(1, 2), "km"), (999, "Gm")):
        assert to_metres(*in_world(to_metres(v, u))) == to_metres(v, u)    # round trip, exact
    assert in_world(to_metres(Fraction(1, 2), "km")) == (500, "m")
    assert light_time(1) == Fraction(1, 300000000)
    assert light_time(384400000) == Fraction(3844, 3000)                  # about 1.28 s
    light_year = 300000000 * 365 * 24 * 3600
    assert (Fraction(light_year) + Fraction(1, 10 ** 9)) - light_year == Fraction(1, 10 ** 9)
    assert (light_year + 1e-9) - light_year == 0.0                        # a float loses the nanometre
    with pytest.raises(ValueError):
        in_world(0)


def test_smallest_point_and_carried_rest():
    from raum27.nennerordnung import snap, snap_series
    assert snap(Fraction(1, 3), 9) == (Fraction(3, 9), 0)
    assert snap(Fraction(1, 100), 9) == (0, Fraction(1, 100))          # below the grid: shown as 0
    small = [Fraction(1, 20)] * 20                                      # each below 1/9
    dropped = sum(snap(v, 9)[0] for v in small)
    assert dropped == 0                                                 # setting each to 0 loses 1
    shown, rest = snap_series(small, 9)
    assert sum(shown) + rest == 1 and abs(rest) <= Fraction(1, 18)      # carried: nothing lost
    with pytest.raises(ValueError):
        snap(1, 0)
