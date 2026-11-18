"""Tests for raum27.synchronsensor: centre + 6 sphere + 8 cube sensors."""

from fractions import Fraction

import pytest

from raum27.synchronsensor import (
    AXIS,
    CORNERS,
    R,
    SENSORS,
    bit_words,
    deltas,
    fit,
    gradient_from_corners,
    gradient_mismatch,
    sample,
    stream,
)

F = Fraction
COEF = dict(c=F(7, 3), g=(F(1, 2), F(-2), F(3, 5)), a=(F(1), F(-1, 4), F(2)),
            b=(F(3), F(-1, 2), F(5, 7)), t=F(9, 2))


def quadratic(x, y, z):
    c, g, a, b, t = COEF["c"], COEF["g"], COEF["a"], COEF["b"], COEF["t"]
    return (c + g[0] * x + g[1] * y + g[2] * z
            + a[0] * x * x + a[1] * y * y + a[2] * z * z
            + b[0] * x * y + b[1] * y * z + b[2] * x * z + t * x * y * z)


def test_geometry_sphere_half_cube_corners_and_the_plane_diagonal():
    assert len(SENSORS) == 15 and len(AXIS) == 6 and len(CORNERS) == 8
    assert all(sum(c * c for c in p) == R * R for p in AXIS)                 # sphere r = 1/2
    assert all(sum(c * c for c in p) == 3 * R * R for p in CORNERS)          # corners at sqrt3/2
    corner = CORNERS[0]
    assert corner[0] ** 2 + corner[1] ** 2 == 2 * R * R                      # projection: plane diagonal


def test_all_eleven_terms_recovered_exactly():
    result = fit(sample(quadratic))
    assert result["value"] == COEF["c"]
    assert result["gradient"] == COEF["g"]
    assert result["curvature"] == COEF["a"]
    assert result["mixed"] == COEF["b"]
    assert result["twist"] == COEF["t"]
    assert gradient_mismatch(sample(quadratic)) == (0, 0, 0)


def test_corners_expose_third_order_the_axes_cannot_separate():
    third = lambda x, y, z: quadratic(x, y, z) + 4 * x * y * y
    axis_gradient = fit(sample(third))["gradient"]
    assert axis_gradient == COEF["g"]                    # the axes see nothing of x*y^2
    mismatch = gradient_mismatch(sample(third))
    assert mismatch == (4 * R * R, 0, 0)                 # the corners see it
    assert gradient_from_corners(sample(third))[0] == COEF["g"][0] + 4 * R * R


def test_deltas_and_words():
    reading = sample(lambda x, y, z: 10 + (1 if (x, y, z) == AXIS[2] else 0) + (2 if (x, y, z) == CORNERS[5] else 0))
    six, eight = deltas(reading)
    assert six == (0, 0, 1, 0, 0, 0) and eight == (0, 0, 0, 0, 0, 2, 0, 0)
    assert bit_words(reading, F(1, 2)) == (0b000100, 0b00100000)
    assert bit_words(reading, 1) == (0, 0b00100000)


def test_stream_reports_only_changes_against_the_baseline():
    base = sample(quadratic)
    moved = sample(lambda x, y, z: quadratic(x, y, z) + F(1, 10) * x)     # a small extra gradient
    frames = stream(base, [base, moved], F(1, 100))
    assert frames[0]["changed"] == {} and frames[0]["words"] == (0, 0)
    assert frames[1]["terms"]["gradient"] == (F(1, 10), 0, 0)
    assert frames[1]["terms"]["curvature"] == (0, 0, 0)
    assert frames[1]["terms"]["twist"] == 0
    six, eight = frames[1]["words"]
    assert six == 0b000011 and eight == 0b11111111


def test_bad_readings_are_refused():
    with pytest.raises(ValueError):
        deltas({(0, 0, 0): 1})
    with pytest.raises(TypeError):
        sample(lambda x, y, z: 0.5)
