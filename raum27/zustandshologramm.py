"""Dead reckoning with the wavelength as step, recorded as a state hologram.

The rule submitted: the step dx is not chosen freely, it is the
wavelength -- speed over frequency, ``dx = v / f`` -- and each step takes
the period ``1 / f``. Speed and time give the lengths; the lengths and
directions give the delta vectors in outer space. What is recorded per
step is a state of **1 + 6 + 8 bits** under its frequency key:

- 1 bit: did the impulse leave a delta at all;
- 6 bits: which of the six sextant directions (+x, -x, +y, -y, +z, -z)
  carry it;
- 8 bits: which of the eight octant directions (+-1, +-1, +-1) carry it.

The delta vector of a step is ``dx`` times the sum of its active
directions, so every component is ``dx`` times an integer and the whole
reckoning is exact for rational speed and integer frequency. An octant
direction is a cube diagonal with lattice components, i.e. length
``sqrt 3`` per unit of ``dx``; nothing irrational is ever computed.

Grouped by frequency, the records form the hologram (``hologram``). Its
superposition keeps the end point exactly -- vector addition does not
care about order -- but not the order of the steps, so the path itself
needs the sequence (``navigate``). The way back is the same records
reversed with every direction mirrored (``retrace``).
"""

from dataclasses import dataclass
from fractions import Fraction
from itertools import product

SEXTANTS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
OCTANTS = tuple(product((-1, 1), repeat=3))
BITS = 1 + 6 + 8


def _speed(value):
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError(f"speed must be int or Fraction, got {type(value).__name__}")
    return Fraction(value)


@dataclass(frozen=True)
class Record:
    frequency: int
    pulse: bool
    sextant_bits: int = 0
    octant_bits: int = 0

    def __post_init__(self):
        if not isinstance(self.frequency, int) or isinstance(self.frequency, bool) or self.frequency < 1:
            raise ValueError(f"frequency must be a positive integer, got {self.frequency!r}")
        if not 0 <= self.sextant_bits < 64 or not 0 <= self.octant_bits < 256:
            raise ValueError("sextant bits must fit 6 bits and octant bits 8 bits")
        if not self.pulse and (self.sextant_bits or self.octant_bits):
            raise ValueError("a record without pulse carries no directions")


def wavelength(speed, frequency):
    """The step dx: speed over frequency."""
    return _speed(speed) / frequency


def period(frequency):
    """Time one step takes."""
    return Fraction(1, frequency)


def direction(record):
    """Integer direction of a record: sum of its active sextant and octant vectors."""
    total = [0, 0, 0]
    if record.pulse:
        for bit, vector in enumerate(SEXTANTS):
            if record.sextant_bits >> bit & 1:
                total = [t + v for t, v in zip(total, vector)]
        for bit, vector in enumerate(OCTANTS):
            if record.octant_bits >> bit & 1:
                total = [t + v for t, v in zip(total, vector)]
    return tuple(total)


def delta(record, speed):
    """Delta vector of one step: wavelength times direction."""
    dx = wavelength(speed, record.frequency)
    return tuple(dx * component for component in direction(record))


def navigate(start, records, speed):
    """All positions from ``start`` through the records, start included."""
    positions = [tuple(Fraction(c) for c in start)]
    for record in records:
        positions.append(tuple(p + d for p, d in zip(positions[-1], delta(record, speed))))
    return positions


def elapsed_time(records):
    """Total time of the recorded steps."""
    return sum((period(r.frequency) for r in records), Fraction(0))


def _mirror_sextants(bits):
    return sum(1 << (bit ^ 1) for bit in range(6) if bits >> bit & 1)


def _mirror_octants(bits):
    return sum(1 << (bit ^ 7) for bit in range(8) if bits >> bit & 1)


def mirrored(record):
    """The same record with every direction reversed."""
    return Record(record.frequency, record.pulse,
                  _mirror_sextants(record.sextant_bits), _mirror_octants(record.octant_bits))


def retrace(records):
    """The way back: records reversed, each direction mirrored."""
    return [mirrored(r) for r in reversed(records)]


def pack(record):
    """The 15-bit state of a record (the frequency is the key, kept separately)."""
    return int(record.pulse) | record.sextant_bits << 1 | record.octant_bits << 7


def unpack(frequency, state):
    """Inverse of ``pack`` under a frequency key."""
    if not 0 <= state < 1 << BITS:
        raise ValueError(f"{state} is not a {BITS}-bit state")
    return Record(frequency, bool(state & 1), state >> 1 & 63, state >> 7 & 255)


def hologram(records):
    """Records grouped by frequency key, as packed 15-bit states in arrival order."""
    keyed = {}
    for record in records:
        keyed.setdefault(record.frequency, []).append(pack(record))
    return keyed


def end_point_from_hologram(start, keyed, speed):
    """End point from the hologram alone -- exact, since addition ignores order."""
    position = [Fraction(c) for c in start]
    for frequency, states in keyed.items():
        for state in states:
            step = delta(unpack(frequency, state), speed)
            position = [p + d for p, d in zip(position, step)]
    return tuple(position)
