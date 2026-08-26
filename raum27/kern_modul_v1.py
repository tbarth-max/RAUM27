"""RAUM27 Kern-Modul v1: five independently-checkable facts about the
cube's reflection group, its solid-angle/parity structure, TDOA
localization, a redundancy identity, and a rational identity behind
"1/9". Ported from an external Lean 4 draft (RAUM27_Modul_v1.lean) after
independent verification here in exact rational arithmetic.

Left out on purpose, because nothing backs them yet: the draft's three
`sorry`-marked claims (full transitivity of the {flipX,flipY,flipZ}
reflection group -- true, but not formalized here either; an empirical
"2.6-3.2x noise reduction" factor with no reproducible experiment
attached; and an unrelated, explicitly unfinished compression chain).

One thing worth flagging rather than silently accepting: the source
material calls `face_contribution` and `complement_contribution` two
"independent" derivations of 1/9. They aren't. `complement_contribution`
is `1 - 8/9`, true by construction for any assumed 8/9 -- it doesn't
derive the 8/9 from anything. It's included so that distinction stays
checkable, not because it's a real second proof.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product
from typing import Callable, Iterable, Tuple

Corner = Tuple[int, int, int]


def all_corners() -> list[Corner]:
    """The 8 corners of the unit cube, as 0/1 bit-triples."""
    return list(product((0, 1), repeat=3))


def flip_x(c: Corner) -> Corner:
    return (1 - c[0], c[1], c[2])


def flip_y(c: Corner) -> Corner:
    return (c[0], 1 - c[1], c[2])


def flip_z(c: Corner) -> Corner:
    return (c[0], c[1], 1 - c[2])


def reachable(start: Corner, flips: Iterable[Callable[[Corner], Corner]]) -> set[Corner]:
    """The set of corners reachable from `start` by repeatedly applying
    any of `flips`, in any order (BFS closure)."""
    seen = {start}
    frontier = {start}
    while frontier:
        new = set()
        for c in frontier:
            for f in flips:
                p = f(c)
                if p not in seen:
                    new.add(p)
        seen |= new
        frontier = new
    return seen


def octant_solid_angle() -> Fraction:
    """Solid angle of one octant (3 mutually perpendicular planes through
    a point), as a fraction of the full sphere's 4*pi sr, in units of pi
    sr: 4/8 = 1/2. True for any octant regardless of cube size."""
    return Fraction(4, 8)


def parity(corner: Corner) -> int:
    """Number of set bits mod 2."""
    return sum(corner) % 2


def face_diagonal(c: Corner) -> Corner:
    """The corner reached by flipping 2 of the 3 bits."""
    return (1 - c[0], 1 - c[1], c[2])


def space_diagonal(c: Corner) -> Corner:
    """The corner reached by flipping all 3 bits (the antipodal corner)."""
    return (1 - c[0], 1 - c[1], 1 - c[2])


def tdoa_position(L: Fraction, v: Fraction, dt: Fraction) -> Fraction:
    """Time-difference-of-arrival source position along a baseline of
    length L, given signal speed v and measured arrival-time difference
    dt: x = (L - v*dt) / 2."""
    return (L - v * dt) / 2


def redundancy_holds(x: Fraction) -> bool:
    """X * (1/X) = 1 for X != 0 -- the redundancy condition itself."""
    return x * (1 / x) == 1


def face_contribution() -> Fraction:
    """One corner's contribution in a 1/r^4-type field model: (sqrt(3))^4
    = (sqrt(3)^2)^2 = 3^2 = 9, so the contribution is 1/9. Computed via
    the exact rational square of 3, never introducing an irrational
    sqrt(3) into the arithmetic."""
    return Fraction(1, 3**2)


def complement_contribution() -> Fraction:
    """1 - 8/9. NOT an independent derivation of 1/9 -- it assumes the
    other 8 corners contribute exactly 8/9 without deriving that from any
    model, so this is a restatement of the complement, not a second
    proof. See module docstring."""
    return 1 - Fraction(8, 9)
