"""Tests for raum27.nullpunkt."""

from fractions import Fraction

import pytest

from raum27.nullpunkt import (
    ECKEN_8, FLAECHEN_6, SKALA, XYZT, ZENTRUM, Anomalie, vergleiche, wirkung, zeit_bei_ausgabe,
)


def test_fixed_names():
    assert SKALA == Fraction(9, 2) and ZENTRUM == (0, 0, 0)
    assert len(FLAECHEN_6) == 6 and len(ECKEN_8) == 8 and len(XYZT) == 4
    assert [sum(a[i] for a in XYZT) for i in range(3)] == [0, 0, 0]
    assert len(set(FLAECHEN_6)) == 6 and len(set(ECKEN_8)) == 8


def test_anomaly_normalised_checked_and_returned():
    a = Anomalie((Fraction(1, 3), Fraction(-2, 3), Fraction(5, 7)), Fraction(1, 9), Fraction(3, 2))
    assert a.faktor() == 3
    assert a.normiert() == (1, -2, Fraction(15, 7))
    assert all(a.pruefung().values())
    assert a.zurueck(a.normiert()) == a.ort
    x, y, z, t = a.xyzt()
    assert x + y + z + t == 0
    with pytest.raises(ValueError):
        Anomalie((0, 0, 0), 0, 1)                                     # radius 0 is never reached
    with pytest.raises(TypeError):
        Anomalie((0.5, 0, 0), 1, 1)
    with pytest.raises(TypeError):
        Anomalie((0, 0, 0), 1, 0.5)


def test_cause_and_effect_opposite_through_the_centre():
    u = (Fraction(1, 2), 2, -3)
    w = wirkung(u)
    assert w == (Fraction(-1, 2), -2, 3)
    assert tuple(a + b for a, b in zip(u, w)) == ZENTRUM               # the centre lies between them
    assert sum(c * c for c in u) == sum(c * c for c in w)            # equal distance
    assert wirkung(w) == tuple(Fraction(c) for c in u)               # twice: back to the cause


def test_compare_and_time_only_at_output():
    a = Anomalie((1, 0, 0), 1, 1)
    b = Anomalie((1, 0, 0), 1, Fraction(9, 2))
    assert vergleiche(a, a) == (0, 0, 0, 0)
    d = vergleiche(a, b)
    assert sum(d) == 0 and d != (0, 0, 0, 0)
    assert zeit_bei_ausgabe(33, 330) == Fraction(1, 10)
