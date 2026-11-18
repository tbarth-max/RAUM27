"""The crystal lattice as carrier: band limit, decay above it, and the structure guard.

The picture submitted: the zero point is the nucleus of a crystal, the
event-driven trigger. Expansion is crystal growth; compression is crystal
flow -- not melting like a steel melt, but energy handed on as impulses
within the lattice's resonance band, charging every particle without
dissolving the structure; further deformation creates new nodes.

What is exact here, for a chain of masses ``m`` joined by springs ``k``
with spacing ``a``:

- **The band.** A wave of wavenumber q has frequency
  omega = 2 sqrt(k/m) |sin(q a / 2)| (``dispersion``). Nothing above
  **omega_max = 2 sqrt(k/m)** travels (``max_frequency``); a ring of N
  masses has exactly the frequencies 2 sqrt(k/m) |sin(pi n / N)|
  (``ring_frequencies``).
- **Above the band the lattice refuses.** Driven above omega_max, the
  amplitude falls from cell to cell by the factor
  |b| - sqrt(b^2 - 1), b = 1 - m omega^2 / (2k) (``decay_per_cell``):
  the lattice does not take the energy in, it reflects it. Inside the
  band the factor is 1 -- the wave passes.
- **The structure guard.** A crystal melts when its atoms swing by about
  a tenth of their spacing (Lindemann's criterion, an empirical 0.10 to
  0.15). With E = m omega^2 A^2 / 2 per particle, the largest energy per
  particle that keeps the structure is
  E_max = m omega^2 (L a)^2 / 2 (``max_energy_per_particle``). That is the
  submitted rule in numbers: **the inner energy must not reach the
  structure constant.**

Real counterparts kept in the README: nucleation, phonons, dislocation
glide (crystals flow without melting), work hardening and dynamic
recrystallisation (new nuclei out of deformation). Diamond, with its
stiff bonds, has one of the highest band limits of any solid and carries
heat as lattice waves better than any other bulk material.
"""

import math
from fractions import Fraction

LINDEMANN = Fraction(1, 10)
"""Conservative melting threshold: amplitude / spacing (empirically 0.10 to 0.15)."""


def max_frequency(k, m):
    """Upper band edge 2 sqrt(k/m)."""
    if k <= 0 or m <= 0:
        raise ValueError("stiffness and mass must be positive")
    return 2 * math.sqrt(k / m)


def dispersion(q, k, m, a=1.0):
    """Frequency of a lattice wave with wavenumber ``q``."""
    return max_frequency(k, m) * abs(math.sin(q * a / 2))


def ring_frequencies(n, k, m):
    """All normal-mode frequencies of a ring of ``n`` masses, sorted."""
    if n < 2:
        raise ValueError("a ring needs at least two masses")
    return sorted(max_frequency(k, m) * abs(math.sin(math.pi * j / n)) for j in range(n))


def decay_per_cell(omega, k, m):
    """Amplitude factor per cell for a chain driven at ``omega``; 1 inside the band."""
    b = 1 - m * omega ** 2 / (2 * k)
    if abs(b) <= 1:
        return 1.0
    return abs(b) - math.sqrt(b * b - 1)


def passes(omega, k, m):
    """True when a drive at ``omega`` travels through the lattice."""
    return omega <= max_frequency(k, m)


def max_energy_per_particle(m, omega, spacing, limit=LINDEMANN):
    """Largest vibrational energy per particle that keeps the crystal intact."""
    return Fraction(m) * Fraction(omega) ** 2 * (Fraction(limit) * Fraction(spacing)) ** 2 / 2


def structure_holds(energy, m, omega, spacing, limit=LINDEMANN):
    """The main guard: inner energy below the structure constant."""
    return Fraction(energy) < max_energy_per_particle(m, omega, spacing, limit)
