"""Tests for raum27.spirale."""
from __future__ import annotations

import math
from fractions import Fraction

import pytest

from raum27.lichtgitter import (
    ellipse_y_squared,
    focal_radii,
    focal_sum,
    position_from_focal_difference,
)
from raum27.spirale import (
    arc_after,
    axis_ratio_squared,
    eccentricity,
    eccentricity_squared,
    height_after,
    is_rational_spiral,
    process_state,
    pythagorean_spirals,
    returns_to_the_same_angle,
    semi_major_axis,
    semi_minor_axis,
    step,
    turn_length,
    turn_length_squared,
)


def test_the_turn_is_a_right_triangle_exactly():
    """L^2 = B^2 + h^2, no pi anywhere."""
    assert turn_length_squared(Fraction(4), Fraction(3)) == 25
    assert turn_length_squared(Fraction(12), Fraction(5)) == 169
    assert turn_length_squared(Fraction(1), Fraction(1)) == 2
    assert turn_length_squared(Fraction(1, 2), Fraction(1, 3)) == Fraction(13, 36)


def test_zero_pitch_gives_a_circle_so_the_height_makes_the_ellipse():
    """Without height there is no ellipse. That is the whole point of
    generating it from the spiral's rise."""
    for b in (Fraction(1), Fraction(4), Fraction(100)):
        assert eccentricity_squared(b, Fraction(0)) == 0
        assert eccentricity(b, Fraction(0)) == 0
        assert axis_ratio_squared(b, Fraction(0)) == 1
        assert turn_length(b, Fraction(0)) == b


def test_the_pitch_alone_decides_the_shape():
    """Scaling B and h together leaves the shape unchanged; changing
    only h changes it."""
    base = eccentricity_squared(Fraction(4), Fraction(3))
    for k in (Fraction(2), Fraction(10), Fraction(1, 7)):
        assert eccentricity_squared(4 * k, 3 * k) == base
        assert axis_ratio_squared(4 * k, 3 * k) == axis_ratio_squared(Fraction(4), Fraction(3))
    rising = [eccentricity_squared(Fraction(4), Fraction(h)) for h in (0, 1, 3, 10, 100)]
    assert all(b > a for a, b in zip(rising, rising[1:]))
    assert all(e < 1 for e in rising)  # never degenerates to a parabola


def test_the_pythagorean_spirals_are_exactly_the_rational_ones():
    assert eccentricity(Fraction(4), Fraction(3)) == Fraction(3, 5)
    assert eccentricity(Fraction(12), Fraction(5)) == Fraction(5, 13)
    assert eccentricity(Fraction(8), Fraction(15)) == Fraction(15, 17)
    assert eccentricity(Fraction(20), Fraction(21)) == Fraction(21, 29)
    assert axis_ratio_squared(Fraction(4), Fraction(3)) == Fraction(25, 16)
    assert axis_ratio_squared(Fraction(8), Fraction(15)) == Fraction(289, 64)


def test_an_irrational_spiral_raises_instead_of_rounding():
    """B = h = 1 gives L^2 = 2. An earlier draft used isqrt(2) = 1 and
    reported e = 1; this test is why that cannot recur."""
    assert not is_rational_spiral(Fraction(1), Fraction(1))
    assert turn_length_squared(Fraction(1), Fraction(1)) == 2
    with pytest.raises(ValueError):
        turn_length(Fraction(1), Fraction(1))
    with pytest.raises(ValueError):
        eccentricity(Fraction(1), Fraction(1))
    # the squared form is still available and exact
    assert eccentricity_squared(Fraction(1), Fraction(1)) == Fraction(1, 2)
    # and the true value really is irrational
    assert math.sqrt(0.5) == pytest.approx(0.7071067811865476)


def test_rational_spirals_are_detected_correctly():
    for b, h in ((4, 3), (3, 4), (12, 5), (8, 15), (20, 21), (5, 0)):
        assert is_rational_spiral(Fraction(b), Fraction(h))
    for b, h in ((1, 1), (2, 3), (1, 2), (5, 7)):
        assert not is_rational_spiral(Fraction(b), Fraction(h))
    # scaling preserves rationality
    assert is_rational_spiral(Fraction(4, 7), Fraction(3, 7))


def test_the_enumeration_finds_the_known_triples():
    spirals = pythagorean_spirals(30)
    assert (4, 3, 5) in spirals
    assert (3, 4, 5) in spirals
    assert (12, 5, 13) in spirals
    assert (8, 15, 17) in spirals
    assert (20, 21, 29) in spirals
    for b, h, l in spirals:
        assert b * b + h * h == l * l
        assert math.gcd(b, h) == 1
        assert eccentricity(Fraction(b), Fraction(h)) == Fraction(h, l)


def test_the_semi_axes_are_the_turn_length_and_circumference_over_two_pi():
    """a = L/(2pi), b = B/(2pi) -- the only place pi genuinely enters,
    and only for an absolute size rather than a ratio."""
    for b, h in ((4, 3), (12, 5), (2, 7)):
        a = semi_major_axis(Fraction(b), Fraction(h))
        bb = semi_minor_axis(Fraction(b))
        assert a == pytest.approx(math.sqrt(b * b + h * h) / (2 * math.pi))
        assert bb == pytest.approx(b / (2 * math.pi))
        # and the ratio reproduces the exact pi-free statement
        assert (a / bb) ** 2 == pytest.approx(float(axis_ratio_squared(Fraction(b), Fraction(h))))


def test_a_zero_pitch_spiral_has_equal_axes():
    a = semi_major_axis(Fraction(4), Fraction(0))
    b = semi_minor_axis(Fraction(4))
    assert a == pytest.approx(b)


def test_the_angle_closes_but_the_height_does_not():
    """The cycle and the advance, side by side. This is what a closed
    loop cannot store: after one turn it cannot tell one from a
    thousand."""
    heights = [height_after(Fraction(3), n) for n in range(6)]
    assert heights == [Fraction(0), Fraction(3), Fraction(6), Fraction(9), Fraction(12), Fraction(15)]
    assert len(set(heights)) == 6          # every turn distinguishable
    for n in range(6):
        assert returns_to_the_same_angle(n)  # yet the angle always closes


def test_the_per_turn_invariant_does_not_drift():
    """L^2 is the same after one turn and after a hundred thousand --
    exact rational arithmetic, so no accumulation of error."""
    b, h = Fraction(4), Fraction(3)
    invariant = turn_length_squared(b, h)
    for n in (1, 10, 1000, 100_000):
        assert process_state(b, h, n)["turn_invariant_squared"] == invariant == 25
        assert arc_after(b, h, n) == 5 * n
        assert height_after(h, n) == 3 * n


def test_the_state_is_fully_determined_by_three_inputs():
    b, h = Fraction(4), Fraction(3)
    for n in (0, 1, 7, 50):
        assert process_state(b, h, n) == process_state(b, h, n)
        state = process_state(b, h, n)
        assert state["turns"] == n
        assert state["height"] == 3 * n
        assert state["arc"] == 5 * n
        assert state["eccentricity"] == Fraction(3, 5)


def test_stepping_forward_never_needs_its_own_output():
    """The formal difference from a circular definition: step reads turn
    n-1 and writes turn n, so the recursion grounds out at turn 0."""
    b, h = Fraction(4), Fraction(3)
    state = process_state(b, h, 0)
    assert state["height"] == 0
    for expected in range(1, 12):
        state = step(state, b, h)
        assert state["turns"] == expected
        assert state["height"] == 3 * expected
        assert state["arc"] == 5 * expected
    # stepping n times equals computing turn n directly
    assert state == process_state(b, h, 11)


def test_an_irrational_spiral_still_has_a_usable_state():
    """It just omits the quantities that would have to be rounded."""
    state = process_state(Fraction(1), Fraction(1), 5)
    assert state["turns"] == 5
    assert state["height"] == 5
    assert state["turn_invariant_squared"] == 2
    assert state["eccentricity_squared"] == Fraction(1, 2)
    assert "arc" not in state
    assert "eccentricity" not in state


def test_the_spiral_hands_lichtgitter_an_exactly_rational_ellipse():
    """The bridge, and the reason this is computable end to end: the
    pitch picks the eccentricity, and every focal quantity downstream
    stays an exact Fraction."""
    b, h = Fraction(4), Fraction(3)
    e = eccentricity(b, h)
    assert e == Fraction(3, 5)
    for a in (Fraction(25), Fraction(5), Fraction(50)):
        x = a * Fraction(3, 5)
        assert ellipse_y_squared(a, e, x) >= 0
        r1, r2 = focal_radii(a, e, x)
        assert r1 + r2 == focal_sum(a) == 2 * a
        assert position_from_focal_difference(r2 - r1, e) == x
        assert r1.denominator <= 5 and r2.denominator <= 5
    # the integral case: a = 25 gives integer focal radii
    r1, r2 = focal_radii(Fraction(25), e, Fraction(15))
    assert (r1, r2) == (Fraction(16), Fraction(34))


def test_every_pythagorean_spiral_gives_an_exact_ellipse():
    for b, h, l in pythagorean_spirals(30):
        e = eccentricity(Fraction(b), Fraction(h))
        a = Fraction(l) ** 2
        x = a * e
        if ellipse_y_squared(a, e, x) < 0:
            continue
        r1, r2 = focal_radii(a, e, x)
        assert r1 + r2 == 2 * a
        assert position_from_focal_difference(r2 - r1, e) == x


def test_degenerate_inputs_raise():
    with pytest.raises(ValueError):
        turn_length_squared(Fraction(0), Fraction(3))
    with pytest.raises(ValueError):
        turn_length_squared(Fraction(-1), Fraction(3))
    with pytest.raises(ValueError):
        semi_minor_axis(Fraction(0))
    with pytest.raises(ValueError):
        height_after(Fraction(3), -1)
    with pytest.raises(ValueError):
        process_state(Fraction(4), Fraction(3), -1)
    with pytest.raises(ValueError):
        pythagorean_spirals(0)
