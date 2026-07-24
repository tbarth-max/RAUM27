import math
from fractions import Fraction

import pytest

from raum27.taylor import sin_taylor


@pytest.mark.parametrize("x", [0, 0.1, 0.5, 1.0, -0.3])
def test_matches_math_sin_near_zero(x):
    approx = float(sin_taylor(Fraction(x).limit_denominator(10_000), terms=6))
    assert approx == pytest.approx(math.sin(x), abs=1e-4)


def test_reproduces_documented_five_term_expansion():
    x = Fraction(1, 3)
    expected = x - x**3 / 6 + x**5 / 120 - x**7 / 5040 + x**9 / 362880
    assert sin_taylor(x, terms=5) == expected


def test_more_terms_does_not_change_result_at_x_zero():
    assert sin_taylor(Fraction(0), terms=3) == 0
    assert sin_taylor(Fraction(0), terms=9) == 0


def test_accuracy_degrades_far_from_zero():
    # Truncated Taylor series are local approximations: accuracy is good
    # near 0 and gets worse further out, even with more terms than the
    # source notes use. This is not a bug, it is why the source notes'
    # claim of an exact "fingerprint" from a fixed 5-term expansion does
    # not hold uniformly.
    near = abs(float(sin_taylor(Fraction(1, 2), terms=5)) - math.sin(0.5))
    far = abs(float(sin_taylor(Fraction(10), terms=5)) - math.sin(10))
    assert near < 1e-3
    assert far > 1.0
