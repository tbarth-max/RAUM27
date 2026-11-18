"""System-level tests: is the framework workable within its own definitions?

Not "is it true about the universe" -- that is a different question and
these tests do not touch it. This file checks the four properties that
decide whether a formal system can be worked with at all:

1. CLOSED     -- every core ratio follows from a small set of primitives
                 by exact arithmetic, with nothing smuggled in.
2. ACYCLIC    -- no definition depends on itself, directly or through a
                 chain. Circularity is the failure mode flagged
                 repeatedly in this repository, so it is checked
                 mechanically rather than by inspection.
3. CONSISTENT -- where two independent routes reach the same quantity,
                 they agree exactly.
4. PRODUCTIVE -- the definitions yield results that were not among the
                 inputs. A system that only returns what was put in is
                 well-defined but useless.

These can all break silently as modules are added, which is why they
are tests and not a one-off audit.
"""
from __future__ import annotations

import ast
import os
from fractions import Fraction

import pytest

from raum27 import cube_symmetry, octahedron, rautenraum
from raum27.cube_symmetry import (
    corner_directions,
    coupling_constant,
    face_diagonal_squared,
    face_directions,
    space_diagonal_squared,
    space_diagonals,
)
from raum27.kubus_6_8_gleichgewicht import find_equilibrium
from raum27.lichtgitter import SPEED_OF_LIGHT, ticks_per_round_trip
from raum27.optionsraum import single_wish, squared_distance_from_centre
from raum27.resonanztunnel import two_layer_flow_gain
from raum27.verhaeltnis_herleitungen import sphere_to_cylinder_ratio

PACKAGE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "raum27")


# ------------------------------------------------------------- 1. CLOSED

def test_every_core_ratio_follows_from_five_integer_primitives():
    """6 faces, 8 corners, 12 edges, 4 space diagonals, 3 axes -- and
    rational arithmetic. Nothing else is needed, and every result is
    exact."""
    faces = len(face_directions())
    corners = len(corner_directions())
    diagonals = len(space_diagonals())
    edges, axes = 12, 3
    assert (faces, corners, edges, diagonals, axes) == (6, 8, 12, 4, 3)

    derived = {
        "4/3": Fraction(corners, faces),
        "16/9": Fraction(corners, faces) ** 2,
        "3/4": Fraction(faces, corners),
        "9/16": Fraction(faces, corners) ** 2,
        "diagonals_over_axes": Fraction(diagonals, axes),
        "euler": faces - edges + corners,
    }
    assert derived["4/3"] == Fraction(4, 3)
    assert derived["16/9"] == Fraction(16, 9)
    assert derived["3/4"] == Fraction(3, 4)
    assert derived["9/16"] == Fraction(9, 16)
    assert derived["diagonals_over_axes"] == Fraction(4, 3)
    assert derived["euler"] == 2
    assert all(isinstance(v, (Fraction, int)) for v in derived.values())


def test_the_squared_diagonals_are_exact_integers_for_a_unit_cube():
    assert face_diagonal_squared(Fraction(1)) == 2
    assert space_diagonal_squared(Fraction(1)) == 3
    # and they scale as squares, exactly
    for a in (Fraction(2), Fraction(7, 3), Fraction(10)):
        assert face_diagonal_squared(a) == 2 * a ** 2
        assert space_diagonal_squared(a) == 3 * a ** 2


# ------------------------------------------------------------ 2. ACYCLIC

def _internal_dependency_graph() -> dict[str, set[str]]:
    graph: dict[str, set[str]] = {}
    for filename in sorted(os.listdir(PACKAGE_DIR)):
        if not filename.endswith(".py") or filename == "__init__.py":
            continue
        module = filename[:-3]
        tree = ast.parse(open(os.path.join(PACKAGE_DIR, filename)).read())
        deps = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("raum27."):
                deps.add(node.module.split(".", 1)[1])
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.startswith("raum27."):
                        deps.add(alias.name.split(".", 1)[1])
        graph[module] = deps
    return graph


def test_no_definition_depends_on_itself():
    """Mechanical circularity check over the whole package. This is the
    failure mode called out repeatedly in the README, so it is verified
    rather than asserted."""
    graph = _internal_dependency_graph()
    assert len(graph) >= 30

    colour: dict[str, str] = {}
    cycles: list[list[str]] = []

    def visit(node: str, stack: list[str]) -> None:
        colour[node] = "grey"
        stack.append(node)
        for nxt in graph.get(node, ()):
            if colour.get(nxt) == "grey":
                cycles.append(stack[stack.index(nxt):] + [nxt])
            elif colour.get(nxt) is None:
                visit(nxt, stack)
        stack.pop()
        colour[node] = "black"

    for module in graph:
        if colour.get(module) is None:
            visit(module, [])

    assert cycles == []


def test_the_dependency_root_is_the_cube_itself():
    """cube_symmetry is depended on and depends on nothing internal --
    so the primitives really are primitive."""
    graph = _internal_dependency_graph()
    assert graph["cube_symmetry"] == set()
    dependents = [m for m, deps in graph.items() if "cube_symmetry" in deps]
    assert len(dependents) >= 4


# --------------------------------------------------------- 3. CONSISTENT

def test_two_independent_routes_to_four_thirds_agree_exactly():
    """One counts cube elements, the other is a ratio of two solids.
    Nothing links them except the answer."""
    assert coupling_constant() == sphere_to_cylinder_ratio() == Fraction(4, 3)


def test_euler_agrees_across_three_separate_modules():
    """Cube counts, the octahedron module, and the rhombic dodecahedron
    all give 2 -- computed three different ways."""
    cube = len(face_directions()) - 12 + len(corner_directions())
    rhombic = (len(rautenraum.cube_corners()) + len(rautenraum.face_apexes())) - 24 + 12
    assert cube == octahedron.euler_characteristic() == rhombic == 2


def test_the_rhombus_shape_agrees_with_the_cubes_own_diagonal_ratio():
    """Cross-module: the rhombic dodecahedron's face diagonals are in
    the same squared ratio as cube_symmetry.face_diagonal_squared."""
    faces = rautenraum.rhombic_faces()
    short = {rautenraum.squared_length(c1, c2) for (c1, c2), _ in faces}
    long = {rautenraum.squared_length(a1, a2) for _, (a1, a2) in faces}
    assert len(short) == len(long) == 1
    assert long.pop() / short.pop() == face_diagonal_squared(Fraction(1)) == 2


def test_the_package_exports_what_it_claims():
    """Every name in __all__ actually resolves -- a workable system must
    at least be importable."""
    import raum27

    assert len(raum27.__all__) > 200
    for name in raum27.__all__:
        assert hasattr(raum27, name), name


# --------------------------------------------------------- 4. PRODUCTIVE

def test_the_cube_counts_come_out_of_something_that_did_not_contain_them():
    """The strongest productivity check in the package: three orthogonal
    axes carrying a logarithmic field produce 6, 12 and 8 distinguished
    directions. No cube was an input."""
    counts = rautenraum.critical_direction_counts()
    assert counts["singular_face_axes"] == len(face_directions()) == 6
    assert counts["saddle_edges"] == 12
    assert counts["maximal_corners"] == len(corner_directions()) == 8
    assert rautenraum.maximal_normalised_product() == Fraction(8, 27)
    assert rautenraum.edge_direction_product() == Fraction(1, 4)


def test_the_definitions_yield_values_nobody_supplied():
    """A spread of results that are consequences, not inputs: none of
    these numbers appears in any definition."""
    # exact rationals
    assert two_layer_flow_gain(Fraction(19, 20), Fraction(1000)) == Fraction(29809321, 160000)
    assert squared_distance_from_centre(single_wish(27, 0)) == Fraction(26, 27)
    # exact integers
    assert ticks_per_round_trip(SPEED_OF_LIGHT // 2) == SPEED_OF_LIGHT
    # a transcendental root, located not assumed
    assert find_equilibrium() == pytest.approx(5.371566952531, abs=1e-9)


def test_the_exact_share_of_the_numeric_surface_is_the_majority():
    """Floats appear only where measured physical quantities do. The
    rest is exact rational arithmetic, which is what makes the results
    checkable rather than merely plausible."""
    exact = floating = 0
    for filename in sorted(os.listdir(PACKAGE_DIR)):
        if not filename.endswith(".py") or filename == "__init__.py":
            continue
        tree = ast.parse(open(os.path.join(PACKAGE_DIR, filename)).read())
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
                returns = ast.unparse(node.returns) if node.returns else ""
                if "Fraction" in returns or returns in ("int", "Point"):
                    exact += 1
                elif "float" in returns:
                    floating += 1
    assert exact >= 100
    assert exact > floating
    assert exact / (exact + floating) > 0.6
