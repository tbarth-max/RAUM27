"""Two small, correct arithmetic facts about number systems: Shannon
information content per digit in different bases, and the exact
coincidence that the RGB color space and an "8-cube" scaling both land
on 2**24.

bits_per_digit(base) = log2(base) -- the ordinary Shannon information
content of one digit in that base. Not a discovery; included because a
specific numeric claim (log2(9) ~ 3.17 bits, sitting between binary and
hex) came up and is worth having as a checked fact rather than a
remembered one.

rgb_color_count() == cube_scaling_count() == 2**24 exactly, because
16 = 2**4 and 8 = 2**3: 16**6 = 2**24 (three RGB channels, two hex
digits each) and 8**8 = 2**24 (an "8-cube" raised to the 8th power) are
the same number for the same reason -- both are just 2**24 written with
a different base and exponent, not an independent coincidence between
color spaces and cube geometry.
"""

from __future__ import annotations

import math


def bits_per_digit(base: int) -> float:
    """Shannon information content of one digit in the given base."""
    return math.log2(base)


def rgb_color_count() -> int:
    """Total distinct RGB colors: 16 possible values per hex digit, two
    hex digits per channel, three channels: 16**6."""
    return 16**6


def cube_scaling_count() -> int:
    """8**8, the number this project's cube-scaling context compares
    against the RGB color count."""
    return 8**8
