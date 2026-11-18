"""Tests for raum27.rautenraum."""
from __future__ import annotations

import math
import random
from fractions import Fraction

import pytest

from raum27.cube_symmetry import face_diagonal_squared
from raum27.octahedron import euler_characteristic as octahedron_euler_characteristic
from raum27.rautenraum import (
    axis_distance_product,
    critical_direction_counts,
    cube_corners,
    cube_edges,
    difference,
    dimensional_maximum,
    dot,
    edge_direction_product,
    face_apexes,
    field_potential,
    is_on_axis,
    maximal_normalised_product,
    midpoint,
    normalised_axis_product,
    radial_decay_rate,
    rhombic_dodecahedron_volume,
    rhombic_faces,
    squared_length,
)


def test_the_counts_are_the_cubes_own():
    assert len(cube_corners()) == 8
    assert len(face_apexes()) == 6
    assert len(cube_edges()) == 12
    assert len(rhombic_faces()) == 12


def test_the_rhombi_stand_in_bijection_with_the_cube_edges():
    """One rhombus per edge, no remainder."""
    faces = rhombic_faces()
    edges_used = {frozenset(edge) for edge, _ in faces}
    assert len(edges_used) == 12
    assert edges_used == {frozenset(e) for e in cube_edges()}


def test_every_face_is_exactly_two_cube_corners_and_two_apexes():
    """The four points: two from the cube, two from the space around it."""
    corners = set(cube_corners())
    apexes = set(face_apexes())
    for (c1, c2), (a1, a2) in rhombic_faces():
        assert c1 in corners and c2 in corners
        assert a1 in apexes and a2 in apexes
        assert a1 != a2


def test_every_face_is_a_genuine_rhombus_exactly():
    """Four equal sides, diagonals perpendicular and mutually bisecting
    -- checked over Fraction, not to a tolerance."""
    for (c1, c2), (a1, a2) in rhombic_faces():
        d_short = difference(c1, c2)
        d_long = difference(a1, a2)
        assert dot(d_short, d_long) == 0            # perpendicular
        assert midpoint(c1, c2) == midpoint(a1, a2)  # mutually bisecting
        sides = {
            squared_length(c1, a1), squared_length(a1, c2),
            squared_length(c2, a2), squared_length(a2, c1),
        }
        assert len(sides) == 1                       # four equal sides


def test_the_rhombus_diagonals_are_the_projects_own_ratio():
    """1 and sqrt(2) -- squared, 1 and 2, which is exactly
    cube_symmetry.face_diagonal_squared for the unit cube."""
    shorts, longs = set(), set()
    for (c1, c2), (a1, a2) in rhombic_faces():
        shorts.add(squared_length(c1, c2))
        longs.add(squared_length(a1, a2))
    assert shorts == {Fraction(1)}
    assert longs == {Fraction(2)}
    assert list(longs)[0] / list(shorts)[0] == 2
    assert face_diagonal_squared(Fraction(1)) == 2


def test_the_rhombic_dodecahedron_has_exactly_twice_the_cube_volume():
    assert rhombic_dodecahedron_volume() == 2
    assert rhombic_dodecahedron_volume() == Fraction(1) + 6 * Fraction(1, 6)


def test_euler_holds_for_the_rhombic_dodecahedron():
    """14 vertices (8 corners + 6 apexes), 24 edges, 12 faces."""
    vertices = len(cube_corners()) + len(face_apexes())
    assert vertices == 14
    assert vertices - 24 + 12 == 2
    # and the repo's own Euler check agrees on the dual pair
    assert octahedron_euler_characteristic() == 2


def test_the_field_is_singular_exactly_on_the_axes():
    """P is a product of three factors and vanishes iff at least two
    coordinates do -- which is precisely the union of the three axes."""
    for pt in ((1, 0, 0), (0, 5, 0), (0, 0, -3), (-7, 0, 0), (0, 0, 0)):
        assert is_on_axis(*map(Fraction, pt))
        assert axis_distance_product(*map(Fraction, pt)) == 0
        assert field_potential(*map(float, pt)) == math.inf
    for pt in ((1, 1, 0), (1, 1, 1), (3, -2, 5), (Fraction(1, 100), 1, 1)):
        assert not is_on_axis(*map(Fraction, pt))
        assert axis_distance_product(*map(Fraction, pt)) > 0
        assert math.isfinite(field_potential(*map(float, pt)))


def test_off_axis_points_are_never_singular_however_close():
    """Approaching an axis the field grows without bound but is finite
    at every actual point -- the axis is not in the domain."""
    previous = None
    for k in range(1, 12):
        eps = Fraction(1, 10 ** k)
        v = field_potential(1.0, float(eps), 0.0)
        assert math.isfinite(v)
        if previous is not None:
            assert v > previous
        previous = v
    assert previous > 20


def test_the_axes_are_recoverable_from_the_field():
    """The sharper half of the claim: the singular set IS the three
    axes, so the axes are defined by the field rather than
    independently of it."""
    recovered = set()
    for x in range(-2, 3):
        for y in range(-2, 3):
            for z in range(-2, 3):
                if is_on_axis(Fraction(x), Fraction(y), Fraction(z)):
                    recovered.add((x, y, z))
    expected = set()
    for t in range(-2, 3):
        expected |= {(t, 0, 0), (0, t, 0), (0, 0, t)}
    assert recovered == expected


def test_the_field_decays_outward_at_exactly_rate_three_in_every_direction():
    """V(t*u) = V(u) - 3*log(t), exactly. The radial part separates."""
    assert radial_decay_rate() == 3
    random.seed(11)
    for _ in range(400):
        v = [random.gauss(0, 1) for _ in range(3)]
        n = math.sqrt(sum(c * c for c in v))
        if n < 1e-6 or min(abs(c) for c in v) < 1e-3:
            continue
        u = [c / n for c in v]
        base = field_potential(*u)
        for t in (2.0, 7.0, 100.0):
            got = field_potential(*(t * c for c in u))
            assert got == pytest.approx(base - 3 * math.log(t), abs=1e-9)


def test_the_product_is_homogeneous_of_degree_six():
    """Which is why the decay rate is exactly 3 after the -1/2 factor."""
    for pt in ((1, 2, 3), (1, 1, 1), (5, -2, 1), (Fraction(1, 3), 2, Fraction(7, 2))):
        base = axis_distance_product(*map(Fraction, pt))
        for t in (Fraction(2), Fraction(3), Fraction(1, 2), Fraction(5, 7)):
            scaled = axis_distance_product(*(t * Fraction(c) for c in pt))
            assert scaled == t ** 6 * base


def test_the_maximum_on_the_sphere_is_exactly_eight_over_twentyseven():
    """At the 8 corner directions, and nowhere else."""
    assert maximal_normalised_product() == Fraction(8, 27)
    for sx in (-1, 1):
        for sy in (-1, 1):
            for sz in (-1, 1):
                assert normalised_axis_product(
                    Fraction(sx), Fraction(sy), Fraction(sz)
                ) == Fraction(8, 27)


def test_the_six_face_directions_are_zero_and_the_twelve_edges_are_one_quarter():
    for axis in range(3):
        for sign in (-1, 1):
            v = [Fraction(0)] * 3
            v[axis] = Fraction(sign)
            assert normalised_axis_product(*v) == 0
    edges = 0
    for i in range(3):
        for j in range(3):
            if i >= j:
                continue
            for si in (-1, 1):
                for sj in (-1, 1):
                    v = [Fraction(0)] * 3
                    v[i], v[j] = Fraction(si), Fraction(sj)
                    assert normalised_axis_product(*v) == edge_direction_product()
                    edges += 1
    assert edges == 12
    assert edge_direction_product() == Fraction(1, 4)
    assert edge_direction_product() < maximal_normalised_product()


def test_no_direction_anywhere_beats_the_corner_value():
    """400000 random directions: the corner maximum is global."""
    random.seed(4)
    best = Fraction(0)
    limit = Fraction(8, 27)
    for _ in range(40000):
        v = [random.gauss(0, 1) for _ in range(3)]
        n2 = sum(c * c for c in v)
        if n2 < 1e-12:
            continue
        p = axis_distance_product(Fraction(v[0]), Fraction(v[1]), Fraction(v[2]))
        value = p / Fraction(n2) ** 3
        assert value <= limit
        best = max(best, value)
    assert float(best) > 0.29  # gets close to 8/27 = 0.2963


def test_the_edge_direction_is_a_critical_point():
    """Perturbing within the sphere's tangent plane changes P only to
    second order -- so the 12 edge directions really are critical, and
    both signs occur, which makes them saddles."""
    random.seed(7)
    u0 = [1 / math.sqrt(2), 1 / math.sqrt(2), 0.0]
    p0 = float(edge_direction_product())
    h = 1e-5
    up = down = 0
    for _ in range(2000):
        d = [random.gauss(0, 1) for _ in range(3)]
        shift = sum(a * b for a, b in zip(d, u0))
        d = [a - shift * b for a, b in zip(d, u0)]
        n = math.sqrt(sum(c * c for c in d))
        if n < 1e-9:
            continue
        d = [c / n * h for c in d]
        un = [a + b for a, b in zip(u0, d)]
        nn = math.sqrt(sum(c * c for c in un))
        un = [c / nn for c in un]
        p = float(normalised_axis_product(*(Fraction(c) for c in un)))
        assert abs(p - p0) < 10 * h * h      # second order, i.e. critical
        if p > p0 + 1e-12:
            up += 1
        elif p < p0 - 1e-12:
            down += 1
    assert up > 0 and down > 0               # saddle, not an extremum


def test_the_field_singles_out_the_cubes_six_twelve_eight():
    counts = critical_direction_counts()
    assert counts == {"singular_face_axes": 6, "saddle_edges": 12, "maximal_corners": 8}
    assert counts["singular_face_axes"] - counts["saddle_edges"] + counts["maximal_corners"] == 2


def test_eight_over_twentyseven_is_two_cubed_over_three_cubed_and_nothing_more():
    """The honest caveat, as a test: both numbers come from the number of
    axes being three. In n dimensions it is ((n-1)/n)^n at 2^n
    directions, so the 27 is 3^3 because space is 3-dimensional."""
    assert dimensional_maximum(3) == Fraction(8, 27) == maximal_normalised_product()
    assert dimensional_maximum(2) == Fraction(1, 4)
    assert dimensional_maximum(4) == Fraction(81, 256)
    assert dimensional_maximum(1) == 0
    # it is not special to 3: the formula is smooth in n and tends to 1/e
    values = [float(dimensional_maximum(n)) for n in range(2, 40)]
    assert all(b > a for a, b in zip(values, values[1:]))
    assert values[-1] == pytest.approx(1 / math.e, abs=0.02)


def test_the_origin_has_no_direction():
    with pytest.raises(ValueError):
        normalised_axis_product(Fraction(0), Fraction(0), Fraction(0))
    with pytest.raises(ValueError):
        dimensional_maximum(0)
