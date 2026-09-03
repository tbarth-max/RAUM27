"""Tests for raum27.hyperoperationen."""
from __future__ import annotations

from raum27.hyperoperationen import (
    addition,
    multiplication_as_repeated_addition,
    power_as_repeated_multiplication,
    tetration_as_repeated_power,
)


def test_reproduces_the_source_example_exactly():
    a, n = 2, 3
    assert addition(a, n) == 5
    assert multiplication_as_repeated_addition(a, n) == 6
    assert power_as_repeated_multiplication(a, n) == 8
    assert tetration_as_repeated_power(a, n) == 16


def test_multiplication_matches_native_operator():
    for a in range(0, 6):
        for b in range(0, 6):
            assert multiplication_as_repeated_addition(a, b) == a * b


def test_power_matches_native_operator():
    for a in range(0, 6):
        for b in range(0, 6):
            assert power_as_repeated_multiplication(a, b) == a**b


def test_tetration_matches_its_own_recursive_definition():
    def recursive_tetration(a, b):
        return 1 if b == 0 else a ** recursive_tetration(a, b - 1)

    for a in (2, 3):
        for b in range(0, 4):
            assert tetration_as_repeated_power(a, b) == recursive_tetration(a, b)


def test_tetration_of_three_unfolds_into_an_exact_power_identity():
    """a^^3 = a^(a^a) = power(a, power(a,a)) exactly -- a concrete,
    checkable relationship between two adjacent hyperoperation levels,
    rather than a vague "grows faster" claim."""
    for a in (2, 3):
        inner = power_as_repeated_multiplication(a, a)
        assert tetration_as_repeated_power(a, 3) == power_as_repeated_multiplication(a, inner)
