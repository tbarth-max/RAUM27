"""Optical ring register: a cyclic RGB-word shift register, and why the
optical part of the idea (a passive mirror loop) cannot store information
on its own -- it needs regeneration.

The source idea: stack RGB LED states at discrete positions around a loop
(a mirror-reflection delay line), read them back out at a fixed tap, and
feed the last position back into the first. The discrete part of that is
an ordinary circular shift register over 24-bit RGB words -- addressable
by position, indexed mod N (Z/N), same family as the cyclic structures
already in this package (`debruijn_loop`, `q144`). That part is implemented
and tested directly here.

The optical part -- that the mirror loop itself keeps the light circulating
as a store, without anything electronic in the loop -- is checked too, and
it does NOT survive: every real mirror has reflectivity R < 1, so after n
round trips the signal amplitude is R**n of the original (the standard
geometric decay of any passive optical cavity, the same law behind cavity
finesse/Q). `round_trips_until_below_quantization` computes exactly how many
round trips a given mirror reflectivity survives before the attenuated
signal drops below one quantization step of an 8-bit channel. For any real
first-surface mirror (R roughly 0.90-0.99) that number is small -- tens to
low hundreds of round trips, not a stable long-term store.

What makes the register usable as storage is regeneration: re-emitting the
stored value at full amplitude on read, which is an electronic operation on
the measured/digital value, not something the optics do for free.
`OpticalRingRegister` models this explicitly by tracking round-trip age per
cell and letting `regenerate` reset it.

What this module does NOT claim:
- That a real mirror arrangement can be built to exactly match any chosen
  reflectivity or capacity; those are free parameters here, not measurements
  of a built device.
- Anything about "resonance," consciousness, or physical information
  transfer beyond ordinary geometric attenuation of reflected light.
- That the ring topology stores more information than a linear array of the
  same length -- `total_capacity_bits` is the same either way, matching the
  conclusion already established in `debruijn_loop.shannon_capacity` for a
  different kind of cyclic structure.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class RGBWord:
    """One 24-bit RGB state, the information word held at a register position."""

    r: int
    g: int
    b: int

    def __post_init__(self) -> None:
        for name, value in (("r", self.r), ("g", self.g), ("b", self.b)):
            if not 0 <= value <= 255:
                raise ValueError(f"{name}={value} out of 8-bit range [0, 255]")

    def to_hex(self) -> str:
        return f"#{self.r:02X}{self.g:02X}{self.b:02X}"


class RingRegister:
    """Fixed-capacity circular shift register of RGB words, addressed mod N."""

    def __init__(self, capacity: int) -> None:
        if capacity < 1:
            raise ValueError(f"capacity must be >= 1, got {capacity}")
        self._capacity = capacity
        self._cells: list[RGBWord | None] = [None] * capacity

    @property
    def capacity(self) -> int:
        return self._capacity

    def write(self, position: int, word: RGBWord) -> None:
        self._cells[position % self._capacity] = word

    def read(self, position: int) -> RGBWord | None:
        return self._cells[position % self._capacity]

    def rotate(self, steps: int = 1) -> None:
        """Shift every word by `steps` positions (the loop's feedback path)."""
        n = self._capacity
        steps %= n
        if steps == 0:
            return
        self._cells = self._cells[-steps:] + self._cells[:-steps]

    def snapshot(self) -> list[RGBWord | None]:
        return list(self._cells)


def total_capacity_bits(n_positions: int, bits_per_channel: int = 8) -> int:
    """Total stored bits for n RGB positions.

    Equal to a linear array of the same length -- the ring topology changes
    access pattern (fixed tap, feedback), not storage capacity.
    """
    return n_positions * 3 * bits_per_channel


def mirror_attenuation(reflectivity: float, round_trips: int) -> float:
    """Fraction of original amplitude remaining after n round trips through a
    passive mirror loop with per-bounce reflectivity R: amplitude = R**n.
    """
    if not 0.0 < reflectivity <= 1.0:
        raise ValueError(f"reflectivity must be in (0, 1], got {reflectivity}")
    if round_trips < 0:
        raise ValueError(f"round_trips must be >= 0, got {round_trips}")
    return reflectivity**round_trips


def round_trips_until_below_quantization(reflectivity: float, bit_depth: int = 8) -> int:
    """Smallest n with mirror_attenuation(reflectivity, n) < 1 / 2**bit_depth.

    Below this many round trips the attenuated signal is still above one
    quantization step of a `bit_depth`-bit channel; at or beyond it, the
    passive optical loop alone can no longer represent the original value.
    This is the concrete number behind "the loop needs periodic regeneration."
    """
    if not 0.0 < reflectivity < 1.0:
        raise ValueError(f"reflectivity must be in (0, 1), got {reflectivity}")
    threshold = 1.0 / (2**bit_depth)
    # Smallest integer n with n > ratio, where reflectivity**ratio == threshold
    # exactly. floor(ratio) + 1 (rather than ceil(ratio)) is required so that
    # an exact-power case (ratio lands on an integer) still returns the next
    # integer up, since reflectivity**ratio == threshold there, not < threshold.
    ratio = math.log(threshold) / math.log(reflectivity)
    return math.floor(ratio) + 1


class OpticalRingRegister(RingRegister):
    """RingRegister where each cell also tracks round trips since it was last
    written or regenerated, and reports the mirror-attenuated amplitude
    alongside the stored digital value.
    """

    def __init__(self, capacity: int, reflectivity: float) -> None:
        super().__init__(capacity)
        if not 0.0 < reflectivity <= 1.0:
            raise ValueError(f"reflectivity must be in (0, 1], got {reflectivity}")
        self._reflectivity = reflectivity
        self._age = [0] * capacity

    def write(self, position: int, word: RGBWord) -> None:
        super().write(position, word)
        self._age[position % self.capacity] = 0

    def rotate(self, steps: int = 1) -> None:
        super().rotate(steps)
        n = self.capacity
        s = steps % n
        if s:
            self._age = self._age[-s:] + self._age[:-s]
        # Every requested step is one round trip through the mirror loop,
        # even when capacity==1 makes the position shift itself a no-op
        # (s == 0): the light still made the trip, so age still accrues.
        self._age = [
            age + steps if cell is not None else age
            for age, cell in zip(self._age, self._cells)
        ]

    def amplitude(self, position: int) -> float:
        """Fraction of original signal strength remaining at this cell."""
        return mirror_attenuation(self._reflectivity, self._age[position % self.capacity])

    def is_still_resolvable(self, position: int, bit_depth: int = 8) -> bool:
        """Whether the attenuated signal is still above one quantization step."""
        return self.amplitude(position) >= 1.0 / (2**bit_depth)

    def regenerate(self, position: int) -> None:
        """Re-emit the stored word at full amplitude: resets the round-trip
        counter without changing the digital value. This is the concrete
        implementation of "periodic regeneration keeps the loop stable."
        """
        self._age[position % self.capacity] = 0
