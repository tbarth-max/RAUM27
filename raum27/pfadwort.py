"""Paths on the 27-cell lattice as words: exact replay, exact return.

The idea submitted: use sextants (six axis directions) and octants (eight
sign patterns), and reach the same two points again and again on the
same path, by recording direction changes and step lengths -- optimised
for 6 and 8 bits, with "inertia" favouring straight continuation.

On the lattice ``{-1, 0, 1}^3`` this is exact and needs no float at all:

- a step is one of six directions, so it fits in **3 bits** (eight codes,
  six used; the two spare codes are left free on purpose);
- a path is a word over those six letters; replaying the word from the
  same start reaches the same cells, every time, by construction;
- the way back is the **inverse word** -- reversed order, each direction
  flipped -- and it returns to the start exactly. This is the discrete
  counterpart of the delta log in ``raum27.zustandsmaschine``;
- the eight corners are the eight octants (``octant``), the six face
  centres the six directions;
- the number of shortest paths between two cells is the multinomial
  ``(|dx|+|dy|+|dz|)! / (|dx|! |dy|! |dz|!)``; corner to opposite corner
  has 90 of them, so the *choice* among shortest paths fits in 7 bits.

Two things this separates that are easy to run together:

- **repeatability** is free: a deterministic replay of the same word
  always lands on the same cells. Nothing has to be optimised for it.
- **accuracy** is what a bit budget buys once headings are continuous.
  With ``b`` bits a full turn is cut into ``2**b`` headings, the step is
  ``1 / 2**b`` of a turn, and the worst rounding is half of that
  (``heading_step``, ``worst_heading_error``). 6 bits: 1/128 of a turn;
  8 bits: 1/512. That error is per heading, deterministic, and repeats
  identically on every replay -- it shifts *where* the path goes, not
  *whether* it is the same path.

What inertia changes is measured in ``turns``: with the submitted insect
model (``raum27_insekt.py``, 10 seeds x 12 pairs), inertia 3 lowered the
direction changes per path from 1.41 to 1.16 and did not raise the share
of shortest paths (0.96 vs 0.95). It makes paths straighter, which makes
a turn-coded word shorter to store; it does not make them shorter.
"""

from fractions import Fraction
from math import factorial

DIRECTIONS = ((0, 1), (0, -1), (1, 1), (1, -1), (2, 1), (2, -1))
"""The six directions as (axis, sign); the index is the 3-bit code."""

BITS_PER_STEP = 3


def step(cell, code):
    """One step from ``cell`` in direction ``code``; ValueError off the lattice."""
    axis, sign = DIRECTIONS[code]
    moved = list(cell)
    moved[axis] += sign
    if not -1 <= moved[axis] <= 1:
        raise ValueError(f"step {code} leaves the lattice from {cell}")
    return tuple(moved)


def walk(start, word):
    """All cells visited by replaying ``word`` from ``start``, start included."""
    cells = [tuple(start)]
    for code in word:
        cells.append(step(cells[-1], code))
    return cells


def inverse(word):
    """The word that undoes ``word``: reversed order, each direction flipped."""
    return [code ^ 1 for code in reversed(word)]


def turns(word):
    """Number of direction changes along the word."""
    return sum(a != b for a, b in zip(word, word[1:]))


def octant(cell):
    """Sign pattern of a corner cell as a 3-bit number (bit k set: axis k negative)."""
    if 0 in cell:
        raise ValueError(f"{cell} is not a corner")
    return sum(1 << k for k, x in enumerate(cell) if x < 0)


def distance(a, b):
    """Shortest number of steps between two cells (sum of axis distances)."""
    return sum(abs(x - y) for x, y in zip(a, b))


def shortest_path_count(a, b):
    """How many shortest paths connect ``a`` and ``b`` (a multinomial)."""
    parts = [abs(x - y) for x, y in zip(a, b)]
    count = factorial(sum(parts))
    for part in parts:
        count //= factorial(part)
    return count


def pack(word):
    """The word as one integer, 3 bits per step, first step in the lowest bits."""
    number = 0
    for position, code in enumerate(word):
        if not 0 <= code < len(DIRECTIONS):
            raise ValueError(f"no direction with code {code}")
        number |= code << (BITS_PER_STEP * position)
    return number


def unpack(number, length):
    """Inverse of ``pack`` for a word of known length."""
    word = [(number >> (BITS_PER_STEP * i)) & 0b111 for i in range(length)]
    if any(code >= len(DIRECTIONS) for code in word) or number >> (BITS_PER_STEP * length):
        raise ValueError(f"{number} is not a packed word of length {length}")
    return word


def heading_step(bits):
    """Size of one heading step as an exact fraction of a full turn."""
    return Fraction(1, 2 ** bits)


def worst_heading_error(bits):
    """Largest rounding error of a heading quantised to ``bits``, as a fraction of a turn."""
    return heading_step(bits) / 2
