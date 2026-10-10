"""Tests for raum27.resonanztunnel."""
from __future__ import annotations

from fractions import Fraction

import pytest

from raum27.lichtgitter import SPEED_OF_LIGHT
from raum27.resonanztunnel import (
    c_power_is_a_velocity,
    dissipated_power,
    film_area_fraction,
    group_velocity_squared,
    harmonic_index,
    layered_flow_bracket,
    phase_group_product_squared,
    phase_velocity_squared,
    shear_stress,
    standing_wave_frequency,
    two_layer_flow_gain,
)


def test_the_standing_wave_resonances_are_exact_integer_multiples():
    v, L = Fraction(340), Fraction(3)
    fundamental = standing_wave_frequency(1, v, L)
    assert fundamental == Fraction(170, 3)
    for n in range(1, 13):
        assert standing_wave_frequency(n, v, L) == n * fundamental
        assert harmonic_index(standing_wave_frequency(n, v, L), fundamental) == n
        assert harmonic_index(standing_wave_frequency(n, v, L), fundamental).denominator == 1


def test_a_closed_pipe_admits_only_integer_counts():
    """Same structure as the ellipse in lichtgitter: a closed path with a
    conserved length admits only whole-number steps."""
    for v in (Fraction(340), Fraction(1500), Fraction(SPEED_OF_LIGHT)):
        for L in (Fraction(1), Fraction(3), Fraction(7, 2)):
            f0 = standing_wave_frequency(1, v, L)
            indices = {harmonic_index(standing_wave_frequency(n, v, L), f0)
                       for n in range(1, 10)}
            assert indices == {Fraction(n) for n in range(1, 10)}
            assert all(i.denominator == 1 for i in indices)


def test_the_centreline_carries_no_shear_exactly():
    """The strongest claim in the module: tau(0) = 0 exactly."""
    for g in (Fraction(1000), Fraction(1), Fraction(-500), Fraction(10**9)):
        assert shear_stress(g, Fraction(0)) == 0


def test_the_shear_law_contains_no_viscosity_so_it_survives_any_nesting():
    """tau(r) = G*r/2 comes from the pressure balance alone, so it is the
    same whatever fluids are layered where -- which is exactly why the
    frictionless-core claim holds for arbitrary nesting."""
    g = Fraction(1000)
    r = Fraction(1, 40)
    expected = g * r / 2
    assert expected == Fraction(25, 2)
    # the function takes no viscosity argument at all; the value cannot
    # depend on one
    assert shear_stress(g, r) == expected
    # and it is strictly linear in r
    for k in range(1, 20):
        assert shear_stress(g, k * r) == k * expected


def test_shear_grows_linearly_and_is_maximal_at_the_wall():
    g, R = Fraction(1000), Fraction(1, 20)
    values = [shear_stress(g, Fraction(k, 20) * R) for k in range(21)]
    assert values[0] == 0
    assert values[-1] == max(values)
    assert all(b > a for a, b in zip(values, values[1:]))


def test_zero_shear_at_the_axis_is_not_a_frictionless_pipe():
    """Both true at once: no shear on the centreline, strictly positive
    dissipation in the pipe."""
    assert shear_stress(Fraction(1000), Fraction(0)) == 0
    power = dissipated_power(10_000.0, 2.454369e-3)
    assert power == pytest.approx(24.54, abs=0.1)
    assert power > 0


def test_the_n_layer_law_reduces_to_hagen_poiseuille():
    """Single fluid: the bracket is R^4/mu, i.e. Q = pi*G*R^4/(8*mu)."""
    for r_sq in (Fraction(1), Fraction(1, 400), Fraction(9, 16)):
        for mu in (Fraction(1), Fraction(1, 1000), Fraction(7, 3)):
            assert layered_flow_bracket([r_sq], [mu]) == r_sq ** 2 / mu


def test_the_two_layer_closed_form_matches_the_general_law():
    """gain = (1-q^4)*ratio + q^4, derived independently of the sum."""
    mu_core, mu_film = Fraction(1), Fraction(1, 1000)
    r_sq = Fraction(1)
    for q in (Fraction(19, 20), Fraction(9, 10), Fraction(4, 5), Fraction(1, 2)):
        layered = layered_flow_bracket([q ** 2 * r_sq, r_sq], [mu_core, mu_film])
        pure = layered_flow_bracket([r_sq], [mu_core])
        assert layered / pure == two_layer_flow_gain(q, mu_core / mu_film)


def test_a_five_percent_wall_film_multiplies_the_flow_by_exactly_186():
    """Core-annular lubrication is real, and the gain is exactly
    rational -- not a fitted number."""
    gain = two_layer_flow_gain(Fraction(19, 20), Fraction(1000))
    assert gain == Fraction(19, 20) ** 4 + (1 - Fraction(19, 20) ** 4) * 1000
    assert float(gain) == pytest.approx(186.3083, abs=1e-3)
    assert gain > 180


def test_the_gain_is_monotone_in_the_viscosity_ratio_and_in_film_thickness():
    q = Fraction(19, 20)
    gains = [two_layer_flow_gain(q, Fraction(r)) for r in (1, 10, 100, 1000, 10000)]
    assert all(b > a for a, b in zip(gains, gains[1:]))
    assert two_layer_flow_gain(Fraction(1), Fraction(1000)) == 1  # no film, no gain
    thicker = [two_layer_flow_gain(Fraction(k, 20), Fraction(1000)) for k in (20, 19, 18, 16)]
    assert all(b > a for a, b in zip(thicker, thicker[1:]))


def test_fractal_nesting_is_strictly_worse_at_equal_film_volume():
    """REFUTES the fractal-layer claim, exactly over Fraction. At a fixed
    film volume, every self-similar split of the film loses to putting it
    all at the wall."""
    mu_core, mu_film = Fraction(1), Fraction(1, 1000)
    r_sq = Fraction(1)
    q = Fraction(19, 20)
    budget = 1 - q ** 2
    reference = layered_flow_bracket([q ** 2, r_sq], [mu_core, mu_film])
    assert film_area_fraction([q ** 2, r_sq], [mu_core, mu_film], mu_film) == budget

    tested = 0
    for k in (2, 3, 4, 5):
        shell = budget / k
        for gap in (Fraction(1, 40), Fraction(1, 20), Fraction(1, 10), Fraction(1, 5)):
            outers = sorted(r_sq - gap * Fraction(j) for j in range(k))
            radii: list[Fraction] = []
            viscs: list[Fraction] = []
            previous = Fraction(0)
            ok = True
            for outer in outers:
                inner = outer - shell
                if inner <= previous or inner < 0:
                    ok = False
                    break
                radii += [inner, outer]
                viscs += [mu_core, mu_film]
                previous = outer
            if not ok or radii[-1] != r_sq:
                continue
            assert film_area_fraction(radii, viscs, mu_film) == budget
            assert layered_flow_bracket(radii, viscs) < reference
            tested += 1
    assert tested >= 10


def test_why_nesting_loses_the_fourth_power_favours_the_wall():
    """The structural reason, as an inequality on the weights: a shell of
    given area contributes more the further out it sits, because the
    benefit goes as r^4 while the cost goes as r^2."""
    area = Fraction(1, 100)
    contributions = []
    for outer in (Fraction(1), Fraction(4, 5), Fraction(3, 5), Fraction(2, 5)):
        inner = outer - area
        contributions.append(outer ** 2 - inner ** 2)
    assert all(b < a for a, b in zip(contributions, contributions[1:]))


def test_c_squared_is_not_a_speed():
    """Dimensional stop: c^X is a velocity only at X = 1."""
    assert c_power_is_a_velocity(1)
    for x in (0, 2, 3, -1, 27):
        assert not c_power_is_a_velocity(x)
    assert SPEED_OF_LIGHT ** 2 == 89875517873681764


def test_the_phase_velocity_really_does_exceed_c():
    """And without bound as the frequency approaches cutoff."""
    fc = Fraction(10 ** 9)
    c_sq = Fraction(SPEED_OF_LIGHT) ** 2
    previous = None
    for ratio in (Fraction(100), Fraction(5), Fraction(2), Fraction(11, 10), Fraction(101, 100)):
        vp_sq = phase_velocity_squared(fc, fc * ratio)
        assert vp_sq > c_sq
        if previous is not None:
            assert vp_sq > previous
        previous = vp_sq
    # 1.01*fc gives a phase velocity above 7c
    assert phase_velocity_squared(fc, fc * Fraction(101, 100)) > 49 * c_sq


def test_the_group_velocity_never_reaches_c():
    fc = Fraction(10 ** 9)
    c_sq = Fraction(SPEED_OF_LIGHT) ** 2
    for ratio in (Fraction(101, 100), Fraction(2), Fraction(100), Fraction(10 ** 6)):
        vg_sq = group_velocity_squared(fc, fc * ratio)
        assert vg_sq < c_sq
    # and it increases towards c without attaining it
    seq = [group_velocity_squared(fc, fc * Fraction(r)) for r in (2, 10, 100, 1000)]
    assert all(b > a for a, b in zip(seq, seq[1:]))
    assert all(s < c_sq for s in seq)


def test_the_product_of_phase_and_group_velocity_is_exactly_c_squared():
    """The exact invariant: v_p * v_g = c^2, checked in squared form so
    no root is ever taken and the identity is a Fraction equality."""
    c_fourth = Fraction(SPEED_OF_LIGHT) ** 4
    for fc in (Fraction(10 ** 9), Fraction(1), Fraction(7, 3)):
        for ratio in (Fraction(101, 100), Fraction(3, 2), Fraction(2),
                      Fraction(5), Fraction(10 ** 4)):
            assert phase_group_product_squared(fc, fc * ratio) == c_fourth


def test_no_propagating_mode_at_or_below_cutoff():
    fc = Fraction(10 ** 9)
    for f in (fc, fc / 2, Fraction(0)):
        with pytest.raises(ValueError):
            phase_velocity_squared(fc, f)
        with pytest.raises(ValueError):
            group_velocity_squared(fc, f)


def test_degenerate_pipe_geometry_raises():
    with pytest.raises(ValueError):
        layered_flow_bracket([], [])
    with pytest.raises(ValueError):
        layered_flow_bracket([Fraction(1), Fraction(1, 2)], [Fraction(1), Fraction(1)])
    with pytest.raises(ValueError):
        layered_flow_bracket([Fraction(1)], [Fraction(0)])
    with pytest.raises(ValueError):
        layered_flow_bracket([Fraction(1)], [Fraction(1), Fraction(1)])
    with pytest.raises(ValueError):
        standing_wave_frequency(0, Fraction(340), Fraction(3))
    with pytest.raises(ValueError):
        standing_wave_frequency(1, Fraction(340), Fraction(0))
    with pytest.raises(ValueError):
        two_layer_flow_gain(Fraction(3, 2), Fraction(1000))
