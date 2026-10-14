"""Tests for raum27.zeitachse."""

from fractions import Fraction

import pytest

from raum27.zeitachse import (
    diagonal_readings, diagonal_squared, diagrams, exact_root, helix_length_squared, hypercube_faces,
    independent_readings, intact_probability, interval_squared, rational_diagonals, square_sums, stages,
)


def test_four_axes_give_six_diagrams():
    assert diagrams() == ["XY", "XZ", "XT", "YZ", "YT", "ZT"]
    assert len(diagrams()) == 6 == len(diagrams(("x", "y", "z", "t")))
    asked = ["XY", "XZ", "XT", "XT", "YT", "ZT"]
    assert set(diagrams()) - set(asked) == {"YZ"}


def test_four_diagonals_carry_one_number():
    readings = diagonal_readings(3)
    assert len(readings) == 4 and all(c2 == 1 for _, c2 in readings)
    assert independent_readings(Fraction(27, 4)) == 1


def test_stages_come_back_only_on_perfect_powers():
    forward, back = stages(Fraction(2, 3))
    assert forward == [Fraction(2, 3), Fraction(4, 9), Fraction(8, 27), Fraction(16, 81)]
    assert back == [Fraction(2, 3)] * 4
    assert exact_root(2, 4) is None and exact_root(Fraction(1, 2), 2) is None
    assert exact_root(Fraction(81, 16), 4) == Fraction(3, 2)
    assert exact_root(10 ** 40, 4) == 10 ** 10
    with pytest.raises(ValueError):
        exact_root(-1, 2)
    with pytest.raises(TypeError):
        exact_root(2.0, 2)


def test_the_square_already_removes_the_roots():
    assert [diagonal_squared(n) for n in (1, 2, 3, 4)] == [1, 2, 3, 4]
    assert diagonal_squared(2) ** 2 == 4 and diagonal_squared(3) ** 2 == 9   # the 4th powers
    assert rational_diagonals(16) == [1, 4, 9, 16]                           # 4D diagonal = 2


def test_the_fourth_axis_closes_the_three_square_gaps():
    three, four = square_sums(3, 200), square_sums(4, 200)
    assert four == set(range(201))                                          # Lagrange
    assert sorted(set(range(1, 32)) - three) == [7, 15, 23, 28, 31]
    assert hypercube_faces(4) == {0: 16, 1: 32, 2: 24, 3: 8, 4: 1}
    assert hypercube_faces(3) == {0: 8, 1: 12, 2: 6, 3: 1}
    f = hypercube_faces(4)
    assert f[0] - f[1] + f[2] - f[3] + f[4] == 1                            # Euler for the 4-cube


def test_helix_and_spacetime():
    assert helix_length_squared(32, 1) == 33                                 # rhombus turn 4*sqrt2, rise 1
    assert interval_squared(3, 4, 0, 5) == 0                                 # on the light ray
    assert interval_squared(1, 0, 0, 0) > 0 > interval_squared(0, 0, 0, 1)


def test_relays_against_the_direct_line():
    assert intact_probability(Fraction(1, 1000), 24) == Fraction(999, 1000) ** 24
    assert 0.976 < intact_probability(Fraction(1, 1000), 24) < 0.977
    assert intact_probability(Fraction(1, 1000), 1) > intact_probability(Fraction(1, 1000), 24)
    with pytest.raises(ValueError):
        intact_probability(2, 3)
