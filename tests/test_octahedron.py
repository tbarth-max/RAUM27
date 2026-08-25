from fractions import Fraction

from raum27 import octahedron
from raum27.cube_symmetry import corner_directions, face_directions


def test_octahedron_has_six_vertices_eight_faces_twelve_edges():
    assert len(octahedron.vertices()) == 6
    assert len(octahedron.faces()) == 8
    assert len(octahedron.edges()) == 12


def test_octahedron_satisfies_eulers_formula():
    assert octahedron.euler_characteristic() == 2


def test_octahedron_vertices_are_exactly_the_cube_face_directions():
    expected = [tuple(Fraction(x) for x in v) for v in face_directions()]
    assert octahedron.vertices() == expected


def test_octahedron_faces_are_valid_convex_hull_faces():
    verts = octahedron.vertices()
    for face in octahedron.faces():
        a, b, c = face
        ab = tuple(b[i] - a[i] for i in range(3))
        ac = tuple(c[i] - a[i] for i in range(3))
        normal = (
            ab[1] * ac[2] - ab[2] * ac[1],
            ab[2] * ac[0] - ab[0] * ac[2],
            ab[0] * ac[1] - ab[1] * ac[0],
        )
        others = [v for v in verts if v not in face]
        signs = [sum(normal[i] * (v[i] - a[i]) for i in range(3)) for v in others]
        assert all(s < 0 for s in signs) or all(s > 0 for s in signs)


def test_dualizing_twice_shrinks_the_cube_by_exactly_one_third():
    duals = octahedron.dual_cube_corners()
    originals = [tuple(Fraction(x) for x in c) for c in corner_directions()]
    for dual, original in zip(duals, originals):
        assert dual == tuple(x / 3 for x in original)
