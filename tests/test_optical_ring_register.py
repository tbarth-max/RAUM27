import math

import pytest

from raum27.optical_ring_register import (
    SPEED_OF_LIGHT,
    OpticalRingRegister,
    RGBWord,
    RingRegister,
    free_spectral_range,
    is_resonant,
    mirror_attenuation,
    nearest_mode_number,
    resonant_frequency,
    resonant_wavelength,
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


def test_free_spectral_range_matches_earlier_bandwidth_calculation():
    # 3 cm mirror spacing, vacuum: this is the same c/(2L) quantity as the
    # "required source modulation rate" computed earlier in the discussion
    # for a 10-position ring at this spacing -- both are ~5 GHz.
    fsr = free_spectral_range(cavity_length=0.03)
    assert fsr == pytest.approx(5e9, rel=1e-3)


def test_free_spectral_range_scales_inversely_with_cavity_length():
    short = free_spectral_range(cavity_length=0.01)
    long = free_spectral_range(cavity_length=1.0)
    assert short > long
    assert short == pytest.approx(long * 100, rel=1e-9)


def test_free_spectral_range_scales_inversely_with_refractive_index():
    vacuum = free_spectral_range(cavity_length=0.03, refractive_index=1.0)
    glass = free_spectral_range(cavity_length=0.03, refractive_index=1.44)
    assert glass == pytest.approx(vacuum / 1.44)


def test_free_spectral_range_rejects_invalid_inputs():
    with pytest.raises(ValueError):
        free_spectral_range(cavity_length=0.0)
    with pytest.raises(ValueError):
        free_spectral_range(cavity_length=-1.0)
    with pytest.raises(ValueError):
        free_spectral_range(cavity_length=1.0, refractive_index=0.0)


def test_resonant_frequency_is_mode_number_times_fsr():
    fsr = free_spectral_range(cavity_length=0.03)
    for m in (1, 2, 3, 10, 100):
        assert resonant_frequency(cavity_length=0.03, mode_number=m) == pytest.approx(m * fsr)


def test_resonant_frequency_rejects_nonpositive_mode_number():
    with pytest.raises(ValueError):
        resonant_frequency(cavity_length=0.03, mode_number=0)
    with pytest.raises(ValueError):
        resonant_frequency(cavity_length=0.03, mode_number=-1)


def test_resonant_wavelength_round_trip_satisfies_2nl_equals_m_lambda():
    L = 0.03
    n = 1.0
    for m in (1, 2, 5, 50):
        wl = resonant_wavelength(cavity_length=L, mode_number=m, refractive_index=n)
        assert 2 * n * L == pytest.approx(m * wl)


def test_resonant_wavelength_times_frequency_equals_speed_of_light():
    # lambda_m (vacuum wavelength convention) * nu_m == c, independent of n.
    for n in (1.0, 1.44):
        wl = resonant_wavelength(cavity_length=0.03, mode_number=7, refractive_index=n)
        freq = resonant_frequency(cavity_length=0.03, mode_number=7, refractive_index=n)
        assert wl * freq == pytest.approx(SPEED_OF_LIGHT)


def test_is_resonant_true_exactly_at_a_computed_resonant_wavelength():
    L = 0.03
    wl = resonant_wavelength(cavity_length=L, mode_number=42)
    assert is_resonant(wavelength=wl, cavity_length=L)


def test_is_resonant_false_for_a_half_mode_detuned_wavelength():
    L = 0.03
    n_modes_wl = resonant_wavelength(cavity_length=L, mode_number=42)
    # detune by roughly half a free spectral range in frequency space
    detuned_freq = resonant_frequency(cavity_length=L, mode_number=42) + free_spectral_range(L) / 2
    detuned_wl = SPEED_OF_LIGHT / detuned_freq
    assert not is_resonant(wavelength=detuned_wl, cavity_length=L)
    assert detuned_wl != n_modes_wl


def test_is_resonant_rejects_nonpositive_wavelength():
    with pytest.raises(ValueError):
        is_resonant(wavelength=0.0, cavity_length=0.03)


def test_nearest_mode_number_recovers_the_mode_a_wavelength_was_built_from():
    L = 0.03
    for m in (1, 5, 100, 1000):
        wl = resonant_wavelength(cavity_length=L, mode_number=m)
        assert nearest_mode_number(wavelength=wl, cavity_length=L) == m


def test_nearest_mode_number_rejects_nonpositive_wavelength():
    with pytest.raises(ValueError):
        nearest_mode_number(wavelength=0.0, cavity_length=0.03)
