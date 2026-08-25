from raum27.cube_symmetry import face_directions
from raum27.rubik_state import axis_is_solved, axis_pairs, face_is_uniform, is_solved

COLORS = ["white", "yellow", "red", "orange", "green", "blue"]


def solved_cube():
    return {d: [c] * 9 for d, c in zip(face_directions(), COLORS)}


def test_axis_pairs_cover_all_six_face_directions_exactly_once():
    pairs = axis_pairs()
    assert len(pairs) == 3
    covered = [d for pair in pairs for d in pair]
    assert sorted(covered) == sorted(face_directions())


def test_axis_pairs_are_opposite_directions():
    for a, b in axis_pairs():
        assert b == tuple(-x for x in a)


def test_face_is_uniform():
    assert face_is_uniform(["red"] * 9)
    assert face_is_uniform(["red"])
    assert not face_is_uniform(["red"] * 8 + ["blue"])


def test_solved_cube_is_solved():
    cube = solved_cube()
    assert is_solved(cube)
    assert all(axis_is_solved(cube, pair) for pair in axis_pairs())


def test_single_wrong_sticker_fails_only_its_own_axis():
    cube = solved_cube()
    pairs = axis_pairs()
    bad_face = pairs[0][0]
    cube[bad_face] = ["white"] * 8 + ["blue"]

    assert not is_solved(cube)
    assert axis_is_solved(cube, pairs[0]) is False
    assert axis_is_solved(cube, pairs[1]) is True
    assert axis_is_solved(cube, pairs[2]) is True


def test_only_one_of_three_axes_solved():
    cube = solved_cube()
    pairs = axis_pairs()
    for face, _ in pairs[1:]:
        cube[face] = ["x", "y"] + ["x"] * 7

    assert not is_solved(cube)
    assert axis_is_solved(cube, pairs[0]) is True
    assert axis_is_solved(cube, pairs[1]) is False
    assert axis_is_solved(cube, pairs[2]) is False
