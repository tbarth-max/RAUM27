"""RAUM27 Basisoperationen: cube quantities scale by k^n depending on
their TYPE, not by re-deriving the geometry from scratch at every scale.

Ported from an external file (RAUM27_Basisoperationen.py) whose own
72/72-test claim was independently reproduced here by direct execution
before anything was ported. The idea itself is correct and useful; the
source implementation used floats and `math.sqrt` for the diagonal
lengths, which are irrational and so can't be represented exactly. Redone
here with exact Fraction arithmetic throughout, by working with SQUARED
diagonal lengths -- the same convention cube_symmetry.py already uses,
and for the same reason (sqrt(2) and sqrt(3) are irrational; their
squares, 2 and 3, are exact rationals).

Every quantity type scales as k^n for a fixed integer n, independent of
which cube property it is:
    n=0  ratios, angles, combinatorics (corners, faces, edges, ...) --
         invariant under uniform scaling
    n=1  lengths (edge)                    -- scale as k
    n=2  areas, and squared lengths        -- scale as k^2
    n=3  volumes                           -- scale as k^3

hole_wert(name, k) looks up the value at scale k in O(1) from the k=1
basis value, instead of recomputing the underlying geometry every time.
"""

from __future__ import annotations

from fractions import Fraction

from raum27.cube_symmetry import (
    corner_directions,
    cube_volume,
    face_diagonal_squared,
    face_directions,
    space_diagonal_squared,
)

# name -> (value at k=1, scaling exponent n)
BASIS: dict[str, tuple[Fraction, int]] = {
    "ecken": (Fraction(8), 0),
    "flaechen": (Fraction(6), 0),
    "kanten": (Fraction(12), 0),
    "flaechendiagonalen": (Fraction(12), 0),
    "ecke_flaeche_inzidenzen": (Fraction(24), 0),
    "flaechen_pro_ecke": (Fraction(3), 0),
    "ecken_pro_flaeche": (Fraction(4), 0),
    "verh_raumdiag_flaechendiag_quadrat": (Fraction(3, 2), 0),
    "kante": (Fraction(1), 1),
    "flaechendiagonale_quadrat": (Fraction(2), 2),
    "raumdiagonale_quadrat": (Fraction(3), 2),
    "oberflaeche": (Fraction(6), 2),
    "volumen": (Fraction(1), 3),
}


def hole_wert(name: str, k: Fraction) -> Fraction:
    """Value of `name` at scale factor k, via basiswert * k**n -- no
    geometry recomputed."""
    if name not in BASIS:
        raise KeyError(f"Unbekannte Groesse '{name}'. Verfuegbar: {sorted(BASIS)}")
    basiswert, n = BASIS[name]
    return basiswert * (k**n)


def _direkt_berechnen(name: str, k: Fraction) -> Fraction:
    """Reference value for `name` at scale k, recomputed directly from
    cube_symmetry.py's already-verified exact functions -- independent of
    BASIS, so hole_wert can be checked against it rather than against
    itself."""
    edge = Fraction(1) * k
    if name == "kante":
        return edge
    if name == "flaechendiagonale_quadrat":
        return face_diagonal_squared(edge)
    if name == "raumdiagonale_quadrat":
        return space_diagonal_squared(edge)
    if name == "oberflaeche":
        return 6 * edge**2
    if name == "volumen":
        return cube_volume(edge)
    if name == "verh_raumdiag_flaechendiag_quadrat":
        return space_diagonal_squared(edge) / face_diagonal_squared(edge)
    if name == "ecken":
        return Fraction(len(corner_directions()))
    if name == "flaechen":
        return Fraction(len(face_directions()))
    if name in ("kanten", "flaechendiagonalen", "ecke_flaeche_inzidenzen",
                "flaechen_pro_ecke", "ecken_pro_flaeche"):
        return BASIS[name][0]
    raise ValueError(f"Kein Referenztest fuer '{name}' definiert")
