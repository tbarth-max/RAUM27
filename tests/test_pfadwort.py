"""Tests for raum27.pfadwort: lattice paths as words."""

from collections import deque
from fractions import Fraction
from itertools import permutations, product

import pytest

from raum27.pfadwort import (
    DIRECTIONS,
    distance,
    heading_step,
    inverse,
    octant,
    pack,
    shortest_path_count,
    step,
    turns,
    unpack,
    walk,
    worst_heading_error,
)

CELLS = list(product((-1, 0, 1), repeat=3))


def _count_shortest_by_search(a, b):
    dist, ways, queue = {a: 0}, {a: 1}, deque([a])
    while queue:
        u = queue.popleft()
        for code in range(6):
            try:
                v = step(u, code)
            except ValueError:
                continue
            if v not in dist:
                dist[v], ways[v] = dist[u] + 1, ways[u]
                queue.append(v)
            elif dist[v] == dist[u] + 1:
                ways[v] += ways[u]
    return dist[b], ways[b]


def test_six_directions_fit_three_bits_with_two_codes_spare():
    assert len(DIRECTIONS) == 6 < 2 ** 3
    assert len(set(DIRECTIONS)) == 6


def test_step_off_the_lattice_is_refused():
    with pytest.raises(ValueError):
        step((1, 0, 0), 0)


def test_inverse_word_returns_to_start_for_every_corner_route():
    start = (-1, -1, -1)
    routes = set(permutations([0, 0, 2, 2, 4, 4]))
    assert len(routes) == 90
    for route in routes:
        cells = walk(start, list(route))
        assert cells[-1] == (1, 1, 1)
        back = walk(cells[-1], inverse(list(route)))
        assert back == cells[::-1]


def test_replay_is_identical():
    word = [0, 2, 1, 4, 3, 5]
    assert walk((0, 0, 0), word) == walk((0, 0, 0), word)


def test_shortest_path_count_matches_search_for_all_pairs():
    for a in CELLS:
        for b in CELLS:
            d, ways = _count_shortest_by_search(a, b)
            assert d == distance(a, b)
            assert ways == shortest_path_count(a, b)
    assert shortest_path_count((-1, -1, -1), (1, 1, 1)) == 90 < 2 ** 7


def test_pack_round_trip_and_size():
    for word in product(range(6), repeat=4):
        assert unpack(pack(list(word)), 4) == list(word)
    assert pack([5] * 6) < 2 ** 18


@pytest.mark.parametrize("number,length", [(6, 1), (7, 1), (8, 1)])
def test_unpack_rejects_unused_codes_and_overflow(number, length):
    with pytest.raises(ValueError):
        unpack(number, length)


def test_pack_rejects_unknown_code():
    with pytest.raises(ValueError):
        pack([6])


def test_turns_counts_direction_changes():
    assert turns([0, 0, 2, 2, 4, 4]) == 2
    assert turns([0, 2, 0, 2, 4, 4]) == 4
    assert turns([]) == 0


def test_eight_corners_are_eight_octants():
    corners = [c for c in CELLS if 0 not in c]
    assert sorted(octant(c) for c in corners) == list(range(8))
    with pytest.raises(ValueError):
        octant((0, 1, 1))


def test_heading_resolution_six_and_eight_bits():
    assert heading_step(6) == Fraction(1, 64)
    assert worst_heading_error(6) == Fraction(1, 128)
    assert worst_heading_error(8) == Fraction(1, 512)
