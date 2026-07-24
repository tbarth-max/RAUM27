import pytest

from raum27.ifs_attractor import AffineMap, IFS, cube_face_ifs


def test_affine_map_rejects_non_contractive_ratio():
    with pytest.raises(ValueError):
        AffineMap(ratio=1.0, translation=(0.0, 0.0))
    with pytest.raises(ValueError):
        AffineMap(ratio=1.5, translation=(0.0, 0.0))


def test_ifs_requires_matching_dimensions():
    a = AffineMap(ratio=0.5, translation=(0.0, 0.0))
    b = AffineMap(ratio=0.5, translation=(0.0, 0.0, 0.0))
    with pytest.raises(ValueError):
        IFS([a, b])


def test_cube_face_ifs_is_contractive():
    ifs = cube_face_ifs()
    assert ifs.dim == 3
    assert len(ifs.maps) == 6
    assert ifs.is_contractive()


def test_chaos_game_produces_bounded_orbit():
    ifs = cube_face_ifs(ratio=0.5)
    points = ifs.chaos_game(iterations=2000, burn_in=20, seed=42)
    assert len(points) == 2000
    # Banach fixed point theorem: for ratio r and unit-distance targets,
    # the attractor is confined to a bounded region around the origin
    # independent of the (arbitrary) starting point.
    bound = 1.0 / (1.0 - 0.5) + 1.0
    assert all(abs(c) <= bound for p in points for c in p)


def test_chaos_game_is_deterministic_given_seed():
    ifs = cube_face_ifs()
    p1 = ifs.chaos_game(iterations=100, seed=7)
    p2 = ifs.chaos_game(iterations=100, seed=7)
    assert p1 == p2
