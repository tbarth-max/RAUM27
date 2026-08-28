import random

from raum27.bias_detection import ConstantBiasDetector


def _weighted_draw(rng: random.Random, pool: range, weights: list[float], size: int) -> list[int]:
    """Sample `size` distinct values from `pool` without replacement,
    proportional to `weights` (stdlib-only, no numpy dependency)."""
    remaining = list(pool)
    remaining_weights = list(weights)
    drawn = []
    for _ in range(size):
        [choice] = random.choices(remaining, weights=remaining_weights, k=1)
        idx = remaining.index(choice)
        drawn.append(remaining.pop(idx))
        remaining_weights.pop(idx)
    return sorted(drawn)


def _biased_draws(rng: random.Random, biased_values: set[int], strength: float, n: int, pool_size: int = 49, picks: int = 6):
    weights = [1.0] * pool_size
    for v in biased_values:
        weights[v - 1] += strength * 5
    return [_weighted_draw(rng, range(1, pool_size + 1), weights, picks) for _ in range(n)]


def test_detector_finds_a_deliberately_injected_constant_bias():
    rng = random.Random(1)
    biased_values = {5, 15, 25, 35, 45}
    draws = _biased_draws(rng, biased_values, strength=0.10, n=1500)

    detector = ConstantBiasDetector(value_range=49)
    candidates = detector.top_candidates(draws, values_per_event=6, n_candidates=5)

    assert len(set(candidates) & biased_values) >= 4  # allow for one sampling miss


def test_detection_strength_increases_with_bias_strength():
    rng = random.Random(2)
    biased_values = {5, 15, 25, 35, 45}
    detector = ConstantBiasDetector(value_range=49)

    hits = []
    for strength in (0.0, 0.05, 0.15, 0.30):
        draws = _biased_draws(rng, biased_values, strength=strength, n=1500)
        candidates = detector.top_candidates(draws, values_per_event=6, n_candidates=5)
        hits.append(len(set(candidates) & biased_values))

    assert hits[-1] >= hits[0]


def test_false_positive_rate_matches_chance_when_there_is_no_bias():
    """With no injected bias, the top-5 deviation candidates should match
    the biased_values set about as often as picking 5 numbers at random
    would overlap with any fixed 5-number set: E[overlap] = 5*5/49 ~= 0.51.
    Run over several seeds so a single unlucky draw doesn't look like a
    false detection."""
    biased_values = {5, 15, 25, 35, 45}
    detector = ConstantBiasDetector(value_range=49)

    overlaps = []
    for seed in range(20):
        rng = random.Random(seed)
        draws = _biased_draws(rng, biased_values, strength=0.0, n=1500)
        candidates = detector.top_candidates(draws, values_per_event=6, n_candidates=5)
        overlaps.append(len(set(candidates) & biased_values))

    mean_overlap = sum(overlaps) / len(overlaps)
    # generous band around the theoretical 0.51 -- this is a calibration
    # sanity check, not a tight statistical bound
    assert mean_overlap < 1.5


def test_deviation_from_uniform_is_zero_for_exactly_uniform_counts():
    detector = ConstantBiasDetector(value_range=10)
    counts = [3] * 10
    deviation = detector.deviation_from_uniform(counts, n_events=5, values_per_event=6)
    assert all(d == 0 for d in deviation)


def test_total_counts_rejects_out_of_range_values():
    detector = ConstantBiasDetector(value_range=10)
    import pytest

    with pytest.raises(ValueError):
        detector.total_counts([[1, 2, 11]])
