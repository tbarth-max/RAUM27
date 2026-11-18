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


def test_a_marked_rotating_sphere_reads_four_values_with_one_check():
    from raum27.zeitachse import diagonal_cosines_squared, rotation, turn
    mark = (1, 0, 0)
    assert diagonal_cosines_squared(mark) == [Fraction(1, 3)] * 4          # on an axis: all equal
    q = rotation(3, 1, 2, 0)                                                # norm 9 + 1 + 4 + 0 = 14
    turned = turn(q, mark)
    readings = diagonal_cosines_squared(turned)
    assert len(set(readings)) > 1                                           # the turn makes them differ
    assert sum(readings) == Fraction(4, 3)                                  # the built-in check
    for u in ((1, 2, 3), (Fraction(1, 2), -5, 7), (0, 0, 1)):
        assert sum(diagonal_cosines_squared(u)) == Fraction(4, 3)
    with pytest.raises(ValueError):
        diagonal_cosines_squared((0, 0, 0))


def test_rational_quaternions_turn_exactly():
    from raum27.zeitachse import rotation, turn
    m = rotation(3, 1, 2, 0)
    ident = tuple(tuple(Fraction(int(i == j)) for j in range(3)) for i in range(3))
    assert tuple(tuple(sum(a * b for a, b in zip(r, q)) for q in m) for r in m) == ident   # M M^T = I
    det = (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
           + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
    assert det == 1
    assert sum(c * c for c in turn(m, (1, 2, 3))) == 14                    # radius kept
    third = rotation(1, 1, 1, 1)                                            # 120 degrees about (1,1,1)
    assert turn(third, (1, 0, 0)) == (0, 1, 0) and turn(third, (0, 1, 0)) == (0, 0, 1)
    with pytest.raises(ValueError):
        rotation(0, 0, 0, 0)


def test_path_contracts_as_time_stretches_and_the_interval_stays():
    from raum27.zeitachse import boost, gamma
    assert gamma(Fraction(3, 5)) == Fraction(5, 4) and gamma(Fraction(4, 5)) == Fraction(5, 3)
    assert gamma(0) == 1
    x, t = Fraction(7), Fraction(10)
    for beta in (Fraction(3, 5), Fraction(-4, 5), Fraction(5, 13)):
        x2, t2 = boost(x, t, beta)
        assert x2 * x2 - t2 * t2 == x * x - t * t                             # the shared quantity
    # a clock at rest (x = 0) ticks slower seen from the moving system ...
    assert boost(0, 1, Fraction(3, 5))[1] == Fraction(5, 4)
    # ... and a rod of length 1 at rest measures 4/5 there (both ends read at equal t')
    b = Fraction(3, 5)
    assert boost(0, 0, b) == (0, 0)                                            # near end at t' = 0
    assert boost(1, b, b) == (Fraction(4, 5), 0)                               # far end at t' = 0: 4/5
    with pytest.raises(ValueError):
        gamma(Fraction(1, 2))                                                  # sqrt(3)/2: not a fraction
    with pytest.raises(ValueError):
        gamma(1)


def test_halving_the_number_is_endless_the_thread_is_not():
    from raum27.zeitachse import fold_limit, halvings
    h = halvings(1, 10)
    assert h[-1] == Fraction(1, 1024) and sum(h[1:]) + h[-1] == 1             # the halves add up again
    assert fold_limit(1, Fraction(1, 10 ** 9)) == 15                           # 1 m thread, 1 nm thick
    assert fold_limit(1, Fraction(1, 10 ** 3)) == 5                            # 1 m, 1 mm thick
    with pytest.raises(ValueError):
        fold_limit(1, 0)
