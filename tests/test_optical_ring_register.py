import math

import pytest

from raum27.optical_ring_register import (
    OpticalRingRegister,
    RGBWord,
    RingRegister,
    mirror_attenuation,
    round_trips_survived_near_ideal,
    round_trips_until_below_quantization,
    total_capacity_bits,
)


def test_rgb_word_rejects_out_of_range_channels():
    RGBWord(0, 0, 0)
    RGBWord(255, 255, 255)
    with pytest.raises(ValueError):
        RGBWord(256, 0, 0)
    with pytest.raises(ValueError):
        RGBWord(0, -1, 0)


def test_rgb_word_to_hex():
    assert RGBWord(255, 0, 0).to_hex() == "#FF0000"
    assert RGBWord(0, 255, 0).to_hex() == "#00FF00"
    assert RGBWord(0, 0, 255).to_hex() == "#0000FF"
    assert RGBWord(0, 0, 0).to_hex() == "#000000"


def test_ring_register_write_read_roundtrip():
    reg = RingRegister(capacity=4)
    words = [RGBWord(255, 0, 0), RGBWord(0, 255, 0), RGBWord(0, 0, 255), RGBWord(255, 255, 0)]
    for i, w in enumerate(words):
        reg.write(i, w)
    for i, w in enumerate(words):
        assert reg.read(i) == w


def test_ring_register_addressing_wraps_modulo_capacity():
    reg = RingRegister(capacity=3)
    reg.write(0, RGBWord(1, 2, 3))
    assert reg.read(3) == RGBWord(1, 2, 3)
    assert reg.read(-3) == RGBWord(1, 2, 3)


def test_ring_register_full_rotation_returns_to_original_arrangement():
    reg = RingRegister(capacity=5)
    words = [RGBWord(i, i, i) for i in range(5)]
    for i, w in enumerate(words):
        reg.write(i, w)
    before = reg.snapshot()
    reg.rotate(5)
    assert reg.snapshot() == before


def test_ring_register_rotate_shifts_by_one_each_step():
    reg = RingRegister(capacity=3)
    words = [RGBWord(0, 0, 0), RGBWord(1, 1, 1), RGBWord(2, 2, 2)]
    for i, w in enumerate(words):
        reg.write(i, w)
    reg.rotate(1)
    assert reg.snapshot() == [words[2], words[0], words[1]]


def test_total_capacity_bits_matches_linear_array_same_length():
    assert total_capacity_bits(1) == 24
    assert total_capacity_bits(10) == 240
    assert total_capacity_bits(10) == 10 * total_capacity_bits(1)


def test_mirror_attenuation_perfect_mirror_never_decays():
    for n in (0, 1, 100, 10_000):
        assert mirror_attenuation(1.0, n) == 1.0


def test_mirror_attenuation_matches_geometric_decay_exactly():
    r = 0.98
    for n in range(6):
        assert mirror_attenuation(r, n) == pytest.approx(r**n)


def test_mirror_attenuation_is_monotonically_decreasing_for_r_below_one():
    r = 0.95
    values = [mirror_attenuation(r, n) for n in range(20)]
    assert all(a > b for a, b in zip(values, values[1:]))


def test_mirror_attenuation_rejects_invalid_inputs():
    with pytest.raises(ValueError):
        mirror_attenuation(0.0, 1)
    with pytest.raises(ValueError):
        mirror_attenuation(1.5, 1)
    with pytest.raises(ValueError):
        mirror_attenuation(0.9, -1)


@pytest.mark.parametrize("reflectivity", [0.999, 0.99, 0.95, 0.90, 0.5])
def test_round_trips_until_below_quantization_is_a_tight_boundary(reflectivity):
    n = round_trips_until_below_quantization(reflectivity, bit_depth=8)
    threshold = 1.0 / 256
    assert mirror_attenuation(reflectivity, n) < threshold
    assert mirror_attenuation(reflectivity, n - 1) >= threshold


def test_round_trips_until_below_quantization_is_small_for_realistic_mirrors():
    n_best = round_trips_until_below_quantization(0.99, bit_depth=8)
    n_worst = round_trips_until_below_quantization(0.90, bit_depth=8)
    assert n_worst < n_best
    assert n_worst < 100
    assert n_best < 1000


def test_round_trips_until_below_quantization_decreases_with_lower_reflectivity():
    trips = [round_trips_until_below_quantization(r, bit_depth=8) for r in (0.999, 0.99, 0.95, 0.9)]
    assert trips == sorted(trips, reverse=True)


def test_optical_ring_register_fresh_write_has_full_amplitude():
    reg = OpticalRingRegister(capacity=4, reflectivity=0.95)
    reg.write(0, RGBWord(10, 20, 30))
    assert reg.amplitude(0) == pytest.approx(1.0)
    assert reg.is_still_resolvable(0)


def test_optical_ring_register_amplitude_decays_with_round_trips():
    reflectivity = 0.9
    reg = OpticalRingRegister(capacity=3, reflectivity=reflectivity)
    reg.write(0, RGBWord(10, 20, 30))
    for n in range(1, 6):
        reg.rotate(1)
        pos = n % 3
        assert reg.amplitude(pos) == pytest.approx(mirror_attenuation(reflectivity, n))


def test_optical_ring_register_becomes_unresolvable_at_the_computed_boundary():
    reflectivity = 0.9
    reg = OpticalRingRegister(capacity=1, reflectivity=reflectivity)
    n_boundary = round_trips_until_below_quantization(reflectivity, bit_depth=8)
    reg.write(0, RGBWord(100, 100, 100))
    for _ in range(n_boundary - 1):
        reg.rotate(1)
    assert reg.is_still_resolvable(0)
    reg.rotate(1)
    assert not reg.is_still_resolvable(0)


def test_optical_ring_register_regenerate_resets_amplitude_without_changing_value():
    reg = OpticalRingRegister(capacity=1, reflectivity=0.9)
    word = RGBWord(1, 2, 3)
    reg.write(0, word)
    for _ in range(50):
        reg.rotate(1)
    assert reg.amplitude(0) < 1.0
    assert reg.read(0) == word

    reg.regenerate(0)
    assert reg.amplitude(0) == pytest.approx(1.0)
    assert reg.read(0) == word


def test_round_trips_survived_grows_without_bound_as_reflectivity_approaches_one():
    """The Carnot-style idealized limit: as R -> 1, survived round trips
    diverges. This is a genuine, calculable mathematical limit (like a
    Carnot engine's 1 - Tc/Th), not a claim that any real mirror reaches
    it -- every sampled R here is still strictly below 1."""
    results = round_trips_survived_near_ideal(bit_depth=8)
    reflectivities = [r for r, _ in results]
    trips = [n for _, n in results]

    assert reflectivities == sorted(reflectivities)
    assert all(r < 1.0 for r in reflectivities)
    assert trips == sorted(trips)
    assert trips[-1] > 100_000  # unbounded growth, not a small fixed number


def test_optical_ring_register_without_regeneration_eventually_loses_resolvability_but_digital_value_is_unaffected():
    reflectivity = 0.95
    reg = OpticalRingRegister(capacity=1, reflectivity=reflectivity)
    word = RGBWord(200, 50, 25)
    reg.write(0, word)
    n_boundary = round_trips_until_below_quantization(reflectivity, bit_depth=8)
    for _ in range(n_boundary + 5):
        reg.rotate(1)
    assert not reg.is_still_resolvable(0)
    # the register still holds the exact digital value: it is the optical
    # amplitude, not the stored word, that has become unresolvable.
    assert reg.read(0) == word
