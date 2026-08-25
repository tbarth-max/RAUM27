"""Rubik's-cube solved-state check, factored along the cube's 3 axes.

A face is "uniform" if all of its stickers share one color. The cube is
solved iff every face is uniform. Grouping that check by the cube's 3
axes -- each axis being one pair of opposite faces from
cube_symmetry.face_directions() -- gives 3 independent AND-conditions
(one per axis) whose combined AND is the overall solved check. This is
not a new operation: it's the single global "all faces uniform" check,
factored along the same 3 axes already used elsewhere in this package.
"""

from __future__ import annotations

from typing import Dict, List, Sequence, Tuple

from raum27.cube_symmetry import face_directions

Vector3 = Tuple[int, int, int]
Cube = Dict[Vector3, List[str]]


def axis_pairs() -> list[tuple[Vector3, Vector3]]:
    """Group the 6 face directions into their 3 opposite-axis pairs."""
    dirs = face_directions()
    pairs = []
    seen: set[Vector3] = set()
    for d in dirs:
        if d in seen:
            continue
        opposite = tuple(-x for x in d)
        pairs.append((d, opposite))
        seen.add(d)
        seen.add(opposite)
    return pairs


def face_is_uniform(face_colors: Sequence[str]) -> bool:
    """A face is uniform iff every one of its stickers has the same color."""
    return len(set(face_colors)) <= 1


def axis_is_solved(cube: Cube, axis_pair: tuple[Vector3, Vector3]) -> bool:
    """One of the 3 AND-conditions: both faces of this axis are uniform."""
    a, b = axis_pair
    return face_is_uniform(cube[a]) and face_is_uniform(cube[b])


def is_solved(cube: Cube) -> bool:
    """The cube is solved iff all 3 axis pairs are solved."""
    return all(axis_is_solved(cube, pair) for pair in axis_pairs())
