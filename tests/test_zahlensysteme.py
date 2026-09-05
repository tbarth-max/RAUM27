"""Tests for raum27.zahlensysteme."""
from __future__ import annotations

import math

from raum27.zahlensysteme import bits_per_digit, cube_scaling_count, rgb_color_count


def test_bits_per_digit_matches_known_values():
    assert bits_per_digit(2) == 1.0
    assert math.isclose(bits_per_digit(9), 3.169925001442312)
    assert bits_per_digit(16) == 4.0


def test_base_nine_sits_strictly_between_binary_and_hex():
    assert bits_per_digit(2) < bits_per_digit(9) < bits_per_digit(16)


def test_rgb_and_cube_scaling_are_the_same_number_for_the_same_reason():
    assert rgb_color_count() == cube_scaling_count() == 2**24 == 16_777_216
