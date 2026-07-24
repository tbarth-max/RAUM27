from raum27.autocorrelation_control import (
    PersistencePredictor,
    permutation_test_continuous,
    simulate_ar1,
)


def test_persistence_detects_real_autocorrelation():
    """Positive control: with strong real serial correlation (phi=0.85,
    a stand-in for short-range weather persistence), the same
    permutation-test methodology used for the lotto benchmark DOES find
    a significant edge. This shows the test has power -- it is not
    structurally incapable of detecting structure.
    """
    series = simulate_ar1(n=200, phi=0.85, seed=1)
    observed, p_value, null_stats = permutation_test_continuous(
        series,
        predictor_factory=PersistencePredictor,
        n_permutations=200,
        seed=2,
    )
    assert p_value < 0.05


def test_persistence_shows_no_edge_without_autocorrelation():
    """Negative control: with phi=0 the series is i.i.d. noise, exactly
    the lottery case. Knowing yesterday's value tells you nothing about
    today's, so the same predictor that succeeded above should show no
    significant edge here -- the same discriminating result the lotto
    benchmark found, now demonstrated side by side with its positive
    counterpart using identical machinery.
    """
    series = simulate_ar1(n=200, phi=0.0, seed=3)
    observed, p_value, null_stats = permutation_test_continuous(
        series,
        predictor_factory=PersistencePredictor,
        n_permutations=200,
        seed=4,
    )
    assert p_value > 0.05
