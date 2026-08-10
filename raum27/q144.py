"""Q144: the 144-state space and the Phi cyclic operator on it.

Ordinary discrete math, nothing physical: a state is a triple
(edge, phase, plane) with edge in Z/12 (the 12 edges of a cube),
phase in Z/4 (representing rotation by 0/90/180/270 degrees), and
plane in Z/3 (the three axis-aligned projection planes XY, XZ, YZ).
The product space has 12 * 4 * 3 = 144 elements.

Phi advances all three coordinates by one step at once, i.e. it is the
direct sum of three cyclic shifts of orders 12, 4 and 3. Because a point
returns to itself only once *all three* coordinates have completed a full
turn simultaneously, phi is a single permutation of Q144 consisting
entirely of cycles of length lcm(12, 4, 3) = 12 -- not a claim, a
verified fact about this permutation (see tests/test_q144.py).
"""

from __future__ import annotations

from dataclasses import dataclass
from math import lcm

NUM_EDGES = 12
NUM_PHASES = 4
NUM_PLANES = 3
NUM_STATES = NUM_EDGES * NUM_PHASES * NUM_PLANES  # 144

PLANES = ("XY", "XZ", "YZ")


@dataclass(frozen=True, order=True)
class State:
    edge: int
    phase: int
    plane: int

    def __post_init__(self) -> None:
        if not (0 <= self.edge < NUM_EDGES):
            raise ValueError(f"edge out of range: {self.edge}")
        if not (0 <= self.phase < NUM_PHASES):
            raise ValueError(f"phase out of range: {self.phase}")
        if not (0 <= self.plane < NUM_PLANES):
            raise ValueError(f"plane out of range: {self.plane}")

    @property
    def phase_degrees(self) -> int:
        return self.phase * 90

    @property
    def plane_name(self) -> str:
        return PLANES[self.plane]


def all_states() -> list[State]:
    """All 144 states of Q144, in a fixed enumeration order."""
    return [
        State(edge, phase, plane)
        for edge in range(NUM_EDGES)
        for phase in range(NUM_PHASES)
        for plane in range(NUM_PLANES)
    ]


def phi(state: State) -> State:
    """(edge, phase, plane) -> (edge+1, phase+1, plane+1), each mod its own modulus."""
    return State(
        (state.edge + 1) % NUM_EDGES,
        (state.phase + 1) % NUM_PHASES,
        (state.plane + 1) % NUM_PLANES,
    )


def orbit(state: State) -> list[State]:
    """States visited by repeatedly applying phi from `state`, up to (but
    not including) the first repeat."""
    seen: list[State] = []
    seen_set: set[State] = set()
    current = state
    while current not in seen_set:
        seen.append(current)
        seen_set.add(current)
        current = phi(current)
    return seen


def operator_period() -> int:
    """The order of phi as a permutation of Q144: lcm(12, 4, 3) = 12."""
    return lcm(NUM_EDGES, NUM_PHASES, NUM_PLANES)
