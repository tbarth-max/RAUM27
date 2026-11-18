"""Tests for raum27.rotationsebenen."""
from __future__ import annotations

import numpy as np

from raum27.rotationsebenen import (
    elementary_rotation,
    rotation_plane_count,
    rotation_planes,
)


def test_plane_count_matches_known_so_n_dimensions():
    assert rotation_plane_count(2) == 1
    assert rotation_plane_count(3) == 3
    assert rotation_plane_count(4) == 6
    assert rotation_plane_count(5) == 10


def test_three_dimensions_gives_the_three_named_planes():
    assert rotation_planes(["X", "Y", "Z"]) == [("X", "Y"), ("X", "Z"), ("Y", "Z")]


def test_four_dimensions_gives_six_planes_not_three():
    planes = rotation_planes(["X", "Y", "Z", "T"])
    assert len(planes) == 6
    assert planes == [
        ("X", "Y"), ("X", "Z"), ("X", "T"),
        ("Y", "Z"), ("Y", "T"), ("Z", "T"),
    ]


def test_indexing_by_only_the_three_x_touching_planes_loses_information():
    """Two 4D rotation states built with IDENTICAL XY, XZ, XT angles but
    a differing YZ component act differently on the same vector -- if you
    only recorded the three X-touching angles, you couldn't tell these
    two states apart, even though they're not the same rotation."""
    X, Y, Z, T = 0, 1, 2, 3
    a, b, c = 0.3, 0.5, 0.2

    without_yz = (
        elementary_rotation(X, T, c, 4)
        @ elementary_rotation(X, Z, b, 4)
        @ elementary_rotation(X, Y, a, 4)
    )
    with_yz = without_yz @ elementary_rotation(Y, Z, 0.7, 4)

    v = np.array([1.0, 2.0, 3.0, 4.0])
    assert not np.allclose(without_yz @ v, with_yz @ v)


def test_elementary_rotation_is_identity_outside_its_own_plane():
    R = elementary_rotation(0, 1, 1.234, dimension=4)
    assert R[2, 2] == 1.0 and R[3, 3] == 1.0
    assert R[0, 2] == 0.0 and R[0, 3] == 0.0
    assert R[1, 2] == 0.0 and R[1, 3] == 0.0


def test_elementary_rotation_preserves_vector_length():
    rng = np.random.default_rng(0)
    v = rng.normal(size=4)
    R = elementary_rotation(1, 3, 0.77, dimension=4)
    assert np.isclose(np.linalg.norm(R @ v), np.linalg.norm(v))
