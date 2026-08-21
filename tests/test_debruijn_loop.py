import pytest

from raum27.debruijn_loop import generate, lookup_position, position_map, shannon_capacity


def test_generate_length_is_two_to_the_k():
    for k in range(1, 9):
        loop = generate(k)
        assert len(loop) == 2**k, f"k={k}: expected {2**k}, got {len(loop)}"


def test_generate_only_binary_values():
    for k in range(1, 7):
        loop = generate(k)
        assert all(b in (0, 1) for b in loop), f"k={k}: non-binary values in loop"


def test_all_windows_present_exactly_once():
    for k in range(1, 8):
        loop = generate(k)
        n = len(loop)
        doubled = loop + loop[: k - 1]
        seen: dict[tuple[int, ...], int] = {}
        for i in range(n):
            w = tuple(doubled[i : i + k])
            assert w not in seen, (
                f"k={k}: window {w} appears at positions {seen[w]} and {i}"
            )
            seen[w] = i
        assert len(seen) == 2**k, f"k={k}: expected {2**k} windows, got {len(seen)}"


def test_position_map_has_correct_size():
    for k in (3, 4, 5):
        loop = generate(k)
        table = position_map(loop, k)
        assert len(table) == 2**k


def test_lookup_position_correct_for_all_positions():
    for k in (3, 4, 5, 6):
        loop = generate(k)
        table = position_map(loop, k)
        doubled = loop + loop[: k - 1]
        for i in range(len(loop)):
            window = tuple(doubled[i : i + k])
            assert lookup_position(window, table) == i, (
                f"k={k}, pos={i}: lookup returned {lookup_position(window, table)}"
            )


def test_lookup_position_unknown_window_raises():
    k = 4
    loop = generate(k)
    table = position_map(loop, k)
    # (2, 0, 0, 0) cannot be in the binary table
    with pytest.raises(KeyError):
        lookup_position((2, 0, 0, 0), table)


def test_position_map_raises_on_non_debruijn_input():
    # A repeated-window sequence triggers the ValueError in position_map.
    bad = [0, 0, 1, 1]  # windows (0,0), (0,1), (1,1), (1,0) — actually valid for k=2
    # Use a hand-crafted k=2 non-de-bruijn sequence: [0,0,0,0]
    with pytest.raises(ValueError, match="appears"):
        position_map([0, 0, 0, 0], 2)


def test_generate_rejects_k_zero():
    with pytest.raises(ValueError):
        generate(0)


def test_shannon_capacity_matches_log2():
    import math
    for n in (2, 4, 8, 16, 32, 64):
        assert abs(shannon_capacity(n) - math.log2(n)) < 1e-12


def test_loop_traversal_forward_and_backward_same_capacity():
    """The reversed loop contains the same windows — it is still a De Bruijn loop."""
    k = 4
    loop = generate(k)
    rev = list(reversed(loop))
    # Build the position map for the reversed loop; it should succeed without error.
    table_rev = position_map(rev, k)
    assert len(table_rev) == 2**k
