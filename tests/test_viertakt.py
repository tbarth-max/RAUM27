"""Tests for raum27.viertakt."""
from __future__ import annotations

import cmath
import math
from fractions import Fraction

import numpy as np
import pytest

from raum27.kern_modul_v2 import find_period
from raum27.rotationsebenen import rotation_plane_count
from raum27.spirale import eccentricity_squared
from raum27.viertakt import (
    GROUND,
    I_POWERS,
    cos_sin_quarter_turn,
    height_at_tick,
    i_power,
    i_tower_fixed_point,
    is_ground,
    is_maximal_tension,
    mirrors,
    period,
    phasor_repeats,
    planes_needed,
    squared_distance_from_ground,
    state_repeats,
    tick,
    tick_state,
    tower_is_periodic,
)


def test_the_four_stroke_is_exact_integers_not_floats():
    """cos(n*pi/2) and sin(n*pi/2) land in {0, +-1} for integer n, so the
    rhythm needs no transcendental evaluation at all."""
    assert I_POWERS == ((1, 0), (0, 1), (-1, 0), (0, -1))
    for n in range(-8, 13):
        c, s = i_power(n)
        assert isinstance(c, int) and isinstance(s, int)
        assert c in (-1, 0, 1) and s in (-1, 0, 1)
        assert c * c + s * s == 1  # always on the unit circle


def test_it_agrees_with_the_actual_complex_exponential():
    for n in range(0, 13):
        c, s = cos_sin_quarter_turn(n)
        z = cmath.exp(1j * n * math.pi / 2)
        assert z.real == pytest.approx(c, abs=1e-12)
        assert z.imag == pytest.approx(s, abs=1e-12)
        assert math.cos(n * math.pi / 2) == pytest.approx(c, abs=1e-12)
        assert math.sin(n * math.pi / 2) == pytest.approx(s, abs=1e-12)


def test_the_ground_is_i_to_the_zero():
    assert i_power(0) == GROUND == (1, 0)
    assert is_ground(0)
    assert squared_distance_from_ground(0) == 0


def test_the_period_is_exactly_four_two_ways():
    """Exact integer iteration, and the repository's own find_period on
    the real and imaginary series."""
    assert period() == 4
    state = GROUND
    orbit = [state]
    for _ in range(12):
        state = tick(state)
        orbit.append(state)
    assert orbit[:5] == [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 0)]
    assert next(k for k in range(1, 13) if orbit[k] == GROUND) == 4

    real = np.array([i_power(n)[0] for n in range(40)], dtype=float)
    imaginary = np.array([i_power(n)[1] for n in range(40)], dtype=float)
    assert find_period(real, 20) == 4
    assert find_period(imaginary, 20) == 4


def test_ticking_is_exact_integer_arithmetic_forever():
    """A million ticks accumulate no error, because nothing is a float."""
    state = GROUND
    for _ in range(1_000_000):
        state = tick(state)
    assert state == GROUND  # 1e6 is divisible by 4
    state = tick(state)
    assert state == (0, 1)


def test_the_inversion_is_the_unique_point_of_maximum_tension():
    """0, 2, 4, 2 as exact integers -- n=2 is the only maximum, so
    'exakter Gegenpol zum Ursprung' is provable, not imagery."""
    distances = [squared_distance_from_ground(n) for n in range(5)]
    assert distances == [0, 2, 4, 2, 0]
    assert max(distances) == 4
    assert distances.count(4) == 1
    assert is_maximal_tension(2)
    for n in (0, 1, 3, 4, 5, 7):
        assert not is_maximal_tension(n)
    # and 4 is the squared diameter of the unit circle: |1 - (-1)|^2
    assert squared_distance_from_ground(2) == (1 - (-1)) ** 2


def test_the_fourth_tick_mirrors_the_second_it_does_not_return_early():
    """CORRECTION: n=1 and n=3 are at exactly equal distance. The return
    happens in one step at n=4, not gradually from n=3."""
    assert squared_distance_from_ground(1) == squared_distance_from_ground(3) == 2
    assert mirrors(1, 3)
    assert not mirrors(1, 2)
    # strictly: n=3 is no nearer the ground than n=1
    assert not squared_distance_from_ground(3) < squared_distance_from_ground(1)


def test_the_pitch_is_not_zero_at_the_ground_only_the_height_is():
    """CORRECTION: pitch and height are different quantities. A zero
    pitch would destroy the ellipse the construction depends on."""
    pitch = Fraction(3)
    assert height_at_tick(pitch, 0) == 0
    # the pitch is unchanged at every tick
    for n in (0, 1, 2, 3, 4, 100):
        assert tick_state(pitch, n)[1] == pitch * n / 4
    # a genuinely zero pitch collapses the ellipse to a circle
    assert eccentricity_squared(Fraction(4), Fraction(0)) == 0
    assert eccentricity_squared(Fraction(4), pitch) > 0


def test_a_full_turn_lifts_by_exactly_the_pitch():
    pitch = Fraction(3)
    assert height_at_tick(pitch, 4) == pitch
    assert height_at_tick(pitch, 8) == 2 * pitch
    assert height_at_tick(pitch, 1) == Fraction(3, 4)
    assert height_at_tick(pitch, 2) == Fraction(3, 2)


def test_the_phasor_repeats_but_the_state_never_does():
    """THE CENTRAL CLAIM, and it is exactly right: i^0 and i^4 are the
    same complex number and not the same state."""
    pitch = Fraction(3)
    assert phasor_repeats(0, 4)
    assert phasor_repeats(1, 5)
    assert phasor_repeats(2, 1002)
    assert not state_repeats(pitch, 0, 4)
    assert not state_repeats(pitch, 1, 5)
    assert state_repeats(pitch, 7, 7)
    # over a long run: four distinct phasors, every state distinct
    phasors = {i_power(n) for n in range(40)}
    states = {tick_state(pitch, n) for n in range(40)}
    assert len(phasors) == 4
    assert len(states) == 40


def test_with_zero_pitch_the_spiral_degenerates_to_a_memoryless_loop():
    """Which is exactly why the pitch must not be zero: without it the
    state cannot distinguish one turn from a thousand."""
    assert state_repeats(Fraction(0), 0, 4)
    states = {tick_state(Fraction(0), n) for n in range(40)}
    assert len(states) == 4  # memory lost


def test_the_power_tower_is_not_the_same_thing_and_is_not_periodic():
    """CORRECTION: i^n with an integer exponent is 4-periodic. A tower of
    i is transcendental at the first step and converges instead."""
    assert tower_is_periodic() is False
    first = 1j ** 1j
    assert first.real == pytest.approx(math.exp(-math.pi / 2), abs=1e-12)
    assert first.real == pytest.approx(0.207879576351, abs=1e-12)

    z = 1j
    history = []
    for _ in range(600):
        z = 1j ** z
        history.append(z)
    assert abs(history[4] - history[0]) > 1e-3  # not 4-periodic
    assert abs(history[-1] - i_tower_fixed_point()) < 1e-9
    # and it really is a fixed point
    assert abs(1j ** history[-1] - history[-1]) < 1e-12


def test_the_tower_needs_hundreds_of_levels_to_settle():
    """Recorded because 80 levels looks like a mismatch and is only
    incomplete convergence."""
    def tower(levels: int) -> complex:
        z = 1j
        for _ in range(levels):
            z = 1j ** z
        return z

    assert abs(tower(80) - i_tower_fixed_point()) > 1e-6
    assert abs(tower(500) - i_tower_fixed_point()) < 1e-9
    assert abs(tower(5000) - i_tower_fixed_point()) < 1e-9


def test_one_cycle_orders_one_plane_so_three_space_needs_three():
    """SCOPE: the complexity of three dimensions does not collapse into
    a single four-stroke."""
    assert planes_needed(2) == 1 == rotation_plane_count(2)
    assert planes_needed(3) == 3 == rotation_plane_count(3)
    assert planes_needed(4) == 6 == rotation_plane_count(4)
    # three planes, four ticks each
    assert planes_needed(3) * period() == 12


def test_twelve_is_recorded_as_a_coincidence_not_a_derivation():
    """The cube has 12 edges and 3 planes x 4 ticks is 12. Both are 3x4
    and neither follows from the other -- asserted here so the number
    cannot quietly become evidence."""
    from raum27.cube_symmetry import corner_directions, face_directions

    assert planes_needed(3) * period() == 12
    # nothing about the cube enters planes_needed or period
    assert planes_needed(3) == 3 * 2 // 2
    assert period() == 4
    # and the cube's own counts are independent inputs
    assert len(face_directions()) == 6
    assert len(corner_directions()) == 8


def test_degenerate_inputs_raise():
    with pytest.raises(ValueError):
        height_at_tick(Fraction(3), -1)
    with pytest.raises(ValueError):
        planes_needed(0)
