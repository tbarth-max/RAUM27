"""Guards for four specific overclaims caught while reviewing the
2026-08-27 "RAUM27 -- Alle mathematisch bestaetigten Zusammenhaenge"
synthesis document. Each test pins down the correction so a future
edit can't silently drift back to the overclaim.
"""

from fractions import Fraction

from raum27.cube_projection import composed_kernel
from raum27.cube_symmetry import coupling_constant


def test_sixteen_ninths_has_exactly_one_verified_independent_derivation_here():
    """The notes claim 16/9 is "vierfach unabhaengig bestaetigt" (four
    independent confirmations). Two of the four are the same fact told
    twice (C=3/4 squared and C=4/3 squared are reciprocals of each other,
    not independent derivations), and a third ("Lean-Beweis bei n=1") has
    no corresponding code in this repository to check. Only one is
    actually verified here: C = corners/faces = 4/3, and C**2 = 16/9.
    """
    c = coupling_constant()
    assert c == Fraction(4, 3)
    assert c**2 == Fraction(16, 9)
    # The "reciprocal, squared" restatement is the same fact, not a second
    # derivation: (1/C)**2 == 1/C**2 by ordinary arithmetic, not by any
    # independent geometric argument.
    assert (1 / c) ** 2 == 1 / (c**2)


def test_face_to_corner_reconstruction_is_not_lossless():
    """The notes claim reconstructing the 8 corners from the 6 face
    midpoints has "kein Informationsverlust" (no information loss). That
    contradicts the already-verified eigenstructure of the corner<->face
    round trip in cube_projection.py: the composed kernel K has a
    2-dimensional eigenvalue-0 eigenspace, i.e. two independent modes are
    erased by a single round trip. Demonstrated directly here: a vector
    in that erased eigenspace does not survive being passed through K.
    """
    K = composed_kernel()
    # An eigenvalue-0 vector for this K: within the "both faces of an axis
    # equal" subspace, K acts as the rank-1 average-of-three-axes map, whose
    # null space is everything orthogonal to (1,1,1) -- e.g. axis X at +1,
    # axis Y at -1, axis Z at 0, with each axis's two opposite faces equal.
    # Using face order (+x,-x,+y,-y,+z,-z): (1, 1, -1, -1, 0, 0).
    erased_mode = (Fraction(1), Fraction(1), Fraction(-1), Fraction(-1), Fraction(0), Fraction(0))
    result = tuple(sum(row[i] * erased_mode[i] for i in range(6)) for row in K)
    assert all(x == 0 for x in result), (
        "a nonzero input was mapped to the zero vector: information about "
        "this mode is provably not recoverable from the face values alone"
    )
    assert any(x != 0 for x in erased_mode)


def test_speed_of_light_threshold_is_not_unit_invariant():
    """The notes treat "9**9 crosses 300 million, the speed of light in
    m/s" as a meaningful convergence. It is specific to the SI unit
    choice: the same physical speed c, expressed in different units,
    gives wildly different numbers, none of which bear any special
    relationship to 9**9 or 10**9. A real structural fact about c would
    not depend on which units happen to be in use.
    """
    c_m_per_s = 299_792_458
    c_km_per_h = c_m_per_s * 3.6
    c_miles_per_s = c_m_per_s / 1609.344

    nine_to_the_nine = 9**9  # 387_420_489

    # "Crosses" only in m/s -- not in km/h (three orders of magnitude off)
    # or miles/s (three orders of magnitude off the other way).
    assert abs(nine_to_the_nine - c_m_per_s) / c_m_per_s < 0.5
    assert abs(nine_to_the_nine - c_km_per_h) / c_km_per_h > 0.5
    assert abs(nine_to_the_nine - c_miles_per_s) / c_miles_per_s > 100
