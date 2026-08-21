"""De Bruijn loop: a binary cyclic sequence with instant absolute-position lookup.

A De Bruijn sequence B(2, k) is a cyclic binary sequence of length 2^k in which
every possible k-bit subsequence appears exactly once as a contiguous window.
Consequence: reading any k consecutive bits from the loop (at any entry point,
without knowing where you started) is enough to reconstruct the absolute position
unambiguously, in O(1) via a lookup table.

This is ordinary combinatorics (Martin, 1934; van Aardenne-Ehrenfest & de Bruijn,
1951). It is the mathematical core of absolute rotary encoders used in robotics
and CNC machinery, and is what makes the "instant readable from any entry point"
property precise and provable rather than metaphorical.

What this module proves (see tests/test_debruijn_loop.py):
- The sequence has length exactly 2^k.
- Every k-bit window appears exactly once (injectivity over the cyclic indexing).
- The position_map derived from the sequence gives a correct O(1) lookup.
- Traversal works equally in the forward and reverse direction.

What this module does NOT claim:
- Nothing about photonics, resonance fields, or physical signal coupling.
- The circular arrangement stores the same amount of information as a linear one
  (Shannon capacity is log2(N) bits for N distinguishable positions, period).
  The loop's advantage is access pattern, not storage density.
"""

from __future__ import annotations

import math


def generate(k: int) -> list[int]:
    """Return a De Bruijn sequence B(2, k) of length 2^k.

    Uses the FKM (Fredericksen-Kessler-Maurer) recursive construction, which
    produces the lexicographically smallest sequence in this family.

    Args:
        k: window size in bits. Must be >= 1.

    Returns:
        A list of 0s and 1s of length 2**k.
    """
    if k < 1:
        raise ValueError(f"k must be >= 1, got {k}")
    a = [0] * (2 * k)
    sequence: list[int] = []

    def _db(t: int, p: int) -> None:
        if t > k:
            if k % p == 0:
                sequence.extend(a[1 : p + 1])
        else:
            a[t] = a[t - p]
            _db(t + 1, p)
            for j in range(a[t - p] + 1, 2):
                a[t] = j
                _db(t + 1, t)

    _db(1, 1)
    return sequence


def position_map(loop: list[int], k: int) -> dict[tuple[int, ...], int]:
    """Build a lookup table mapping every k-bit window to its start position.

    Args:
        loop: a De Bruijn sequence of length N = 2^k.
        k: window width.

    Returns:
        A dict with 2^k entries {window_tuple: position}.

    Raises:
        ValueError: if any window appears more than once (i.e. loop is not
                    a valid De Bruijn sequence for the given k).
    """
    n = len(loop)
    doubled = loop + loop[: k - 1]
    table: dict[tuple[int, ...], int] = {}
    for i in range(n):
        window = tuple(doubled[i : i + k])
        if window in table:
            raise ValueError(
                f"window {window} appears at positions {table[window]} and {i}; "
                "not a valid De Bruijn sequence"
            )
        table[window] = i
    return table


def lookup_position(window: tuple[int, ...], table: dict[tuple[int, ...], int]) -> int:
    """Return the absolute position of a k-bit window using a prebuilt table.

    This is the O(1) lookup that makes the De Bruijn loop useful: read k bits,
    hand them to this function, get back the absolute start position.

    Args:
        window: a tuple of k bits (0 or 1).
        table: the position map returned by :func:`position_map`.

    Returns:
        The unique position index in [0, 2^k).

    Raises:
        KeyError: if the window is not in the table.
    """
    return table[window]


def shannon_capacity(n: int) -> float:
    """Information capacity of a sequence with n distinguishable positions.

    Returns log2(n) bits. This is the same for linear and circular arrangements
    of the same n positions — the loop topology does not add storage capacity.
    """
    return math.log2(n)
