"""The zero-point system as one module with fixed names: anomaly, cause, effect.

Fixed variables (the public definition, the same for every instance):

    SKALA      = 9/2       half the axis-to-axis distance 9; the inner sphere
    ZENTRUM    = (0,0,0)   the common zero point (node 555 on the 1..9 grid)
    FLAECHEN_6             the 6 face directions (3 coordinate axes)
    ECKEN_8                the 8 corner directions (4 space diagonals)
    XYZT                   the 4 tetrahedral axes X, Y, Z, T (they sum to 0)

Classes and functions:

    Anomalie(ort, massstab, treffer)   an enclosed zero point: place, the
        radius of the enclosing sphere, the distance of its hit on an axis
        .normiert()      place scaled so the hit lies on 9/2
        .xyzt()          readings on X, Y, Z, T (sum 0)
        .pruefung()      the three built-in checks, all True for a valid record
        .zurueck(p)      undo the scaling exactly

    wirkung(ursache)     the effect: 180 degrees opposite the cause, through
                         the centre (-p; on the grid d -> 10 - d)
    vergleiche(a, b)     difference of two anomalies on X, Y, Z, T
    zeit_bei_ausgabe(weg, v)   time only at the output: t = s / v

Inside, there is no time: everything is path and path marks. Cause (the
state as it is) and effect sit opposite each other at equal distance, and
the centre between them is the common zero point. In spacetime the
picture has a counterpart: the past and future light cones of an event
touch only in the event itself.
"""

from dataclasses import dataclass
from fractions import Fraction

from raum27.eckenruecklauf import (
    COORDINATE_AXES,
    DIAGONAL_AXES,
    NINE_HALVES,
    axis_distances_squared,
    scale_to_nine_halves,
    xyzt_readings,
)
from raum27.nennerordnung import time_from_path

SKALA = NINE_HALVES
ZENTRUM = (Fraction(0), Fraction(0), Fraction(0))
FLAECHEN_6 = tuple(tuple(s * c for c in a) for a in COORDINATE_AXES for s in (1, -1))
ECKEN_8 = tuple(tuple(s * c for c in a) for a in DIAGONAL_AXES for s in (1, -1))
XYZT = DIAGONAL_AXES


def _exact_point(p):
    for c in p:
        if isinstance(c, float):
            raise TypeError("exact module: use int or Fraction, not float")
    return tuple(Fraction(c) for c in p)


@dataclass(frozen=True)
class Anomalie:
    ort: tuple
    massstab: Fraction
    treffer: Fraction

    def __post_init__(self):
        object.__setattr__(self, "ort", _exact_point(self.ort))
        for name in ("massstab", "treffer"):
            value = getattr(self, name)
            if isinstance(value, float):
                raise TypeError("exact module: use int or Fraction, not float")
            value = Fraction(value)
            if value <= 0:
                raise ValueError(f"{name} must be positive (radius 0 is never reached)")
            object.__setattr__(self, name, value)

    def faktor(self):
        return SKALA / self.treffer

    def normiert(self):
        return scale_to_nine_halves(self.ort, self.treffer)

    def xyzt(self):
        return xyzt_readings(self.normiert())

    def pruefung(self):
        p = self.normiert()
        r2 = sum(c * c for c in p)
        coord, diag = axis_distances_squared(p)
        return {
            "flaechen_6": sum(coord) == 2 * r2,
            "ecken_8": sum(diag) == Fraction(8, 3) * r2,
            "xyzt_summe_0": sum(self.xyzt()) == 0,
        }

    def zurueck(self, punkt):
        f = self.faktor()
        return tuple(c / f for c in _exact_point(punkt))


def wirkung(ursache):
    """The effect: opposite the cause through the centre (180 degrees)."""
    return tuple(-c for c in _exact_point(ursache))


def vergleiche(a, b):
    """Difference of two anomalies on the four axes X, Y, Z, T."""
    return tuple(x - y for x, y in zip(a.xyzt(), b.xyzt()))


def zeit_bei_ausgabe(weg, geschwindigkeit):
    """Time appears only at the output: t = s / v."""
    return time_from_path(weg, geschwindigkeit)
