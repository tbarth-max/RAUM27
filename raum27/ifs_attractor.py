"""Iterated Function Systems (IFS) and the Banach fixed-point theorem.

The notes assert that a network of overlapping local rules necessarily
settles into "the" attractor once its generator maps are fixed, citing
A = union_{i=1}^{6} f_i(A). That claim is exactly the classical IFS
picture: if each f_i is a contraction (Lipschitz constant < 1) on a
complete metric space, the Banach fixed-point theorem guarantees a unique
non-empty compact attractor A, approximated by the "chaos game" (random
iteration of the f_i). This module implements that standard construction
-- nothing about it is specific to RAUM27, and it makes no claim about
consciousness, resonance, or prediction.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Sequence, Tuple

Point = Tuple[float, ...]


@dataclass(frozen=True)
class AffineMap:
    """A scalar contraction f(p) = ratio * p + translation.

    ratio must lie in (0, 1) for f to be a contraction mapping.
    """

    ratio: float
    translation: Point

    def __post_init__(self) -> None:
        if not 0.0 < self.ratio < 1.0:
            raise ValueError("ratio must be in (0, 1) for f to be a contraction")

    def apply(self, point: Point) -> Point:
        return tuple(self.ratio * p + t for p, t in zip(point, self.translation))


class IFS:
    """An iterated function system: a finite family of contraction maps
    whose union-of-images defines the attractor A = union_i f_i(A)."""

    def __init__(self, maps: Sequence[AffineMap]):
        if not maps:
            raise ValueError("an IFS needs at least one map")
        dims = {len(m.translation) for m in maps}
        if len(dims) != 1:
            raise ValueError("all maps must share the same dimension")
        self.maps = list(maps)
        self.dim = dims.pop()

    def is_contractive(self) -> bool:
        """True iff every map is a genuine contraction (ratio < 1), which
        is the hypothesis of the Banach fixed-point theorem."""
        return all(0.0 < m.ratio < 1.0 for m in self.maps)

    def chaos_game(
        self,
        iterations: int,
        burn_in: int = 20,
        seed: int | None = None,
        start: Point | None = None,
    ) -> list[Point]:
        """Approximate the attractor A by random iteration ("chaos game"):
        repeatedly apply a uniformly random f_i to the current point. After
        a burn-in period the orbit concentrates on A, independent of the
        starting point, by the Banach fixed-point theorem.
        """
        rng = random.Random(seed)
        point = start if start is not None else tuple(0.0 for _ in range(self.dim))
        points: list[Point] = []
        for i in range(burn_in + iterations):
            point = rng.choice(self.maps).apply(point)
            if i >= burn_in:
                points.append(point)
        return points


def cube_face_ifs(ratio: float = 0.5) -> IFS:
    """The 6-map IFS toward the cube's face directions (+-e1, +-e2, +-e3),
    a direct instantiation of the source formula A = union_{i=1}^{6} f_i(A)
    with the standard Sierpinski-style contraction ratio 1/2.
    """
    from raum27.cube_symmetry import face_directions

    maps = [AffineMap(ratio=ratio, translation=tuple(float(c) for c in d)) for d in face_directions()]
    return IFS(maps)
