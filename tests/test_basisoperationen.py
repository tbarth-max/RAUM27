"""Tests for raum27.basisoperationen."""
from __future__ import annotations

from fractions import Fraction

import pytest

from raum27.basisoperationen import BASIS, _direkt_berechnen, hole_wert

FAKTOREN = [
    Fraction(1), Fraction(2), Fraction(5),
    Fraction(1, 3), Fraction(9, 8), Fraction(4, 3),
    Fraction(100), Fraction(1, 1000),
]

NAMEN = [
    "kante", "flaechendiagonale_quadrat", "raumdiagonale_quadrat",
    "oberflaeche", "volumen", "verh_raumdiag_flaechendiag_quadrat",
    "ecken", "flaechen", "kanten", "flaechendiagonalen",
    "ecke_flaeche_inzidenzen",
]


@pytest.mark.parametrize("name", NAMEN)
@pytest.mark.parametrize("k", FAKTOREN)
def test_hole_wert_matches_direct_recomputation(name, k):
    assert hole_wert(name, k) == _direkt_berechnen(name, k)


def test_unbekannte_groesse_wirft_keyerror():
    with pytest.raises(KeyError):
        hole_wert("nicht_vorhanden", Fraction(1))


def test_combinatorial_quantities_are_scale_invariant():
    for name in ("ecken", "flaechen", "kanten"):
        _, n = BASIS[name]
        assert n == 0
        assert hole_wert(name, Fraction(1)) == hole_wert(name, Fraction(1000))


def test_lengths_scale_linearly_areas_quadratically_volume_cubically():
    k = Fraction(5)
    assert hole_wert("kante", k) == k * hole_wert("kante", Fraction(1))
    assert hole_wert("oberflaeche", k) == k**2 * hole_wert("oberflaeche", Fraction(1))
    assert hole_wert("volumen", k) == k**3 * hole_wert("volumen", Fraction(1))


def test_ratio_of_squared_diagonals_is_exactly_three_halves_at_every_scale():
    """space_diagonal^2 / face_diagonal^2 = 3/2 for every edge length --
    a pure ratio, so it must come out scale-invariant (n=0) here too."""
    for k in FAKTOREN:
        assert hole_wert("verh_raumdiag_flaechendiag_quadrat", k) == Fraction(3, 2)
