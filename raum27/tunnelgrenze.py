"""Die Tunnelgrenze: the idealisation granted in full, and what still blocks it.

The question posed, taken seriously: *idealise*. Grant a completely
frictionless inner flow inside some energetic field -- magnetic,
electric, gravitational, or one entirely unknown to us. Whatever the
field is, it will still consist of geometric definitions and defined
interactions, cause and effect. Grant all of that. Then push the
transfer to the shortest measurable `dt` so the path becomes `dx`
rather than `Dx`. Is that the perfect quantum tunnel, built from
resonance?

The answer is no, and the reason is worth more than the answer: **the
premise granted in the question is what forbids the conclusion.**
"Defined interactions" and "cause and effect" are exactly the two
assumptions from which the limits follow. Nothing about the field's
identity is needed, which is why calling it unknown does not help.

Two halves of the request are already achieved in real physics. Three
are blocked, and each block is a different mechanism.

ACHIEVED, AND NOT AS AN IDEALISATION
------------------------------------

**A completely frictionless inner flow exists.** Superfluid helium-4
below its critical velocity flows with *exactly* zero dissipation --
measured, not idealised. Together with `resonanztunnel.shear_stress`,
where `tau(0) = 0` holds exactly for any layering, the frictionless
core is real.

**Transmission with minimal energy loss exists.** Superconducting
radio-frequency cavities reach quality factors above 1e11, i.e. a
fractional energy loss per cycle below 1e-11. The "minimal energy
loss" half of the request is an engineering achievement, not a
speculation.

So the idealisation is not the problem. Both of its physical halves
have been done.

BLOCK 1: A LOSSLESS RESONANCE IS NOT HARD, IT IS EMPTY
------------------------------------------------------

This is the decisive one, because resonance is the proposed mechanism.
For a Lorentz medium `chi(w) = wp²/(w0² - w² - i*gamma*w)` the
absorption is `Im chi`, and it obean exact sum rule:

    INTEGRAL_0^inf  w · Im chi(w) dw  =  pi·wp²/2

**independent of the damping `gamma` and of the resonance frequency
`w0`.** Verified numerically to within 0.3% across six decades of
`gamma` and two resonance frequencies -- the residual drift is tail
truncation in the quadrature, not physics.

So the total absorption is a *fixed constant*, set by the oscillator
strength `wp²` alone. Reducing the damping does not reduce the
absorption; it makes it narrower and taller, with the peak going as
`wp²/(gamma·w0)` -- a thousandfold smaller `gamma` gives a
thousandfold taller peak and the same integral.

And `wp²` is precisely what creates the resonance. Set it to zero and
the absorption vanishes -- along with all dispersion, all resonance,
all the structure the tunnel was supposed to exploit. Kramers-Kronig
says the same thing from the other side: if `Im chi` vanishes at every
frequency then the dispersion integral is zero, so `Re chi` vanishes
too, and the medium is vacuum. (The relation itself is checked against
a Lorentz oscillator in the tests, so the premise being used is the
real one.)

A lossless resonance is therefore not a difficult engineering target.
It is an empty set.

BLOCK 2: THE SHORTEST dt COSTS THE MOST ENERGY
----------------------------------------------

The two halves of the request pull in opposite directions,
quantitatively. Resolving a time `dt` requires

    dE >= hbar / (2·dt)

so the shorter the `dt`, the *more* energy the event must carry. At the
Planck time this minimum is **9.78e8 J** -- about 234 tonnes of TNT
equivalent, concentrated in a single quantum event, and exactly half a
Planck mass in energy. "Minimal energy loss" and "the shortest
measurable `dt`" cannot both be optimised; they are opposite ends of
one inequality.

BLOCK 3: THE MEDIUM'S OWN EXCITATIONS CAP THE FRICTIONLESS SPEED
----------------------------------------------------------------

Landau's criterion gives the critical velocity of any superfluid
directly from its excitation spectrum:

    v_c = min over p of  eps(p)/p

Below `v_c` dissipation is exactly zero; above it, exactly not. For
helium-4 the roton minimum gives **59.3 m/s** (measured ~58), which is
`2.0e-7·c`. Seven orders of magnitude short, in the best frictionless
medium known.

The general form is what answers the "unknown field" move, because it
needs no knowledge of the field:

- `eps = cs·p` (phonon-like) gives `v_c = cs`, the sound speed.
- `eps = p²/2m` (free particle) gives `v_c = 0`: **no frictionless
  regime at all.** A gap is what creates one.
- `eps = D + p²/2m` (gapped) gives `v_c = sqrt(2D/m)`.

So a frictionless regime requires a gap, and a *fast* frictionless
regime requires a large one. Pushing `v_c` to `c` needs
`D = m·c²/2` -- a gap of order the rest energy, 255 keV for an
electron. At that point pair production is open, the medium is
creating particles, and the "no interaction" premise has destroyed
itself. The requirement defeats its own assumption.

BLOCK 4: CAUSALITY ALONE FIXES THE FRONT AT c
---------------------------------------------

This is the one that makes the unknown-field argument fail outright.
Titchmarsh's theorem: if the response is causal -- no output before
input, which is exactly "cause and effect" as granted in the question
-- then the susceptibility is analytic in the upper half plane, hence
`chi(w) -> 0` as `w -> infinity`, hence `n(w) -> 1`. Checked on a
Lorentz medium: `n` deviates from 1 by 5e-3 at `w = 10·w0` and by
5e-13 at `w = 1e6·w0`.

The *front* of a signal -- the leading edge of something genuinely
switched on -- therefore moves at exactly `c` in every causal medium,
whatever it is made of. This follows from causality alone, with no
reference to the field's nature, so an unknown field is bound by it as
tightly as a known one. Group velocity can exceed `c` (see
`resonanztunnel.phase_velocity_squared` for a pipe where it does); the
front cannot.

AND THE dx -> dt MOVE ITSELF
----------------------------

`v = dx/dt`, and the front is capped at `c`, so `dt >= dx/c`. For a
1 m pipe that is 3.34 ns; to the Moon, 1.28 s. Letting `dx -> 0` does
not escape this, it just empties it: the transmitted distance *is*
`dx`, so `dx = 0` is not a fast transfer but no transfer. The quantity
being minimised and the quantity making the thing useful are the same
quantity.

WHAT IS LEFT, WHICH IS NOT NOTHING
----------------------------------

Everything in the request except the superluminal part is reachable,
and some of it is built. Zero-dissipation flow: real. Loss below 1e-11
per cycle: real. Group velocity arbitrarily close to `c`: real. A pipe
in which the phase velocity genuinely exceeds `c`: real, and in this
repository. What is not reachable is a *signal* arriving before
`dx/c`, and that is closed by causality rather than by engineering --
which means it will not yield to a better field, a better resonance,
or a better geometry.
"""

from __future__ import annotations

import math
from fractions import Fraction

#: Reduced Planck constant, J*s (SI exact since 2019: h = 6.62607015e-34).
HBAR = 1.054571817e-34
#: Boltzmann constant, J/K (SI exact since 2019).
BOLTZMANN = 1.380649e-23
#: Planck time, s.
PLANCK_TIME = 5.391247e-44
#: Planck mass, kg.
PLANCK_MASS = 2.176434e-8
#: Electron mass, kg.
ELECTRON_MASS = 9.1093837015e-31
#: Joules per electronvolt.
ELECTRONVOLT = 1.602176634e-19

from raum27.lichtgitter import SPEED_OF_LIGHT  # noqa: E402


def lorentz_absorption(
    omega: float, omega_0: float, gamma: float, strength: float
) -> float:
    """Im chi for a Lorentz medium: the absorption at a given frequency.

    strength is wp², the oscillator strength -- the same quantity that
    produces the resonance."""
    if gamma <= 0 or omega_0 <= 0:
        raise ValueError("damping and resonance frequency must be positive")
    denominator = (omega_0 ** 2 - omega ** 2) ** 2 + gamma ** 2 * omega ** 2
    return strength * gamma * omega / denominator


def lorentz_dispersion(
    omega: float, omega_0: float, gamma: float, strength: float
) -> float:
    """Re chi for a Lorentz medium: the dispersion, which is what a
    resonant tunnel would exploit. Proportional to the same strength."""
    if gamma <= 0 or omega_0 <= 0:
        raise ValueError("damping and resonance frequency must be positive")
    denominator = (omega_0 ** 2 - omega ** 2) ** 2 + gamma ** 2 * omega ** 2
    return strength * (omega_0 ** 2 - omega ** 2) / denominator


def absorption_sum_rule(strength: float) -> float:
    """The exact total absorption, pi*wp²/2.

    Independent of the damping and of the resonance frequency. This is
    the number that cannot be reduced: shrinking the damping only
    concentrates the same total into a narrower, taller peak."""
    return math.pi * strength / 2


def peak_absorption(omega_0: float, gamma: float, strength: float) -> float:
    """Im chi at resonance: wp²/(gamma*w0).

    Diverges as the damping goes to zero -- the sum rule being conserved
    is why."""
    if gamma <= 0 or omega_0 <= 0:
        raise ValueError("damping and resonance frequency must be positive")
    return strength / (gamma * omega_0)


def lossless_resonance_is_possible() -> bool:
    """False.

    Zero absorption at every frequency forces zero dispersion by
    Kramers-Kronig, which means no resonance at all. The set of lossless
    resonances is empty rather than merely hard to reach."""
    return False


def minimum_energy_for_time_resolution(delta_t: float) -> float:
    """hbar/(2*dt): the least energy an event must carry to resolve a
    time dt. Grows as dt shrinks -- the opposite of minimal loss."""
    if delta_t <= 0:
        raise ValueError("a resolved time must be positive")
    return HBAR / (2 * delta_t)


def energy_at_planck_time() -> float:
    """9.78e8 J -- the minimum for resolving the Planck time, which is
    exactly half a Planck mass in energy."""
    return minimum_energy_for_time_resolution(PLANCK_TIME)


def landau_critical_velocity(
    spectrum: list[tuple[float, float]]
) -> float:
    """min over p of eps(p)/p, from a sampled excitation spectrum given
    as (momentum, energy) pairs.

    Below this speed a superfluid dissipates exactly nothing; above it,
    exactly something. Requires no knowledge of what the medium is --
    only that it has excitations, which "defined interactions" already
    grants."""
    if not spectrum:
        raise ValueError("a medium with no excitations is not a medium")
    ratios = [energy / momentum for momentum, energy in spectrum if momentum > 0]
    if not ratios:
        raise ValueError("no positive momenta in the sampled spectrum")
    return min(ratios)


def gapped_critical_velocity(gap: float, mass: float) -> float:
    """sqrt(2*gap/mass): the critical velocity of a gapped spectrum
    eps = gap + p²/2m, attained at p = sqrt(2*m*gap).

    A gap is what creates a frictionless regime at all -- a free-particle
    spectrum p²/2m gives a critical velocity of exactly zero."""
    if gap < 0 or mass <= 0:
        raise ValueError("gap must be non-negative and mass positive")
    return math.sqrt(2 * gap / mass)


def free_particle_critical_velocity() -> float:
    """0.0. eps = p²/2m gives eps/p = p/2m, whose infimum as p -> 0 is
    zero: an ungapped medium has no frictionless regime at any speed."""
    return 0.0


def gap_needed_for_critical_velocity(velocity: float, mass: float) -> float:
    """m*v²/2 -- the gap required to push the frictionless regime up to a
    given speed.

    At v = c this is m*c²/2, a gap of order the rest energy, where pair
    production opens and the no-interaction premise fails."""
    if mass <= 0:
        raise ValueError("mass must be positive")
    return mass * velocity ** 2 / 2


def roton_critical_velocity(
    gap_kelvin: float = 8.65, momentum_inverse_metres: float = 1.91e10
) -> float:
    """Superfluid helium-4 from its roton parameters: 59.3 m/s.

    The measured value is about 58 m/s, so this is a check against
    reality rather than a definition."""
    gap = gap_kelvin * BOLTZMANN
    momentum = momentum_inverse_metres * HBAR
    return gap / momentum


def refractive_index(
    omega: float, omega_0: float, gamma: float, strength: float
) -> float:
    """sqrt(1 + Re chi) for a Lorentz medium. Tends to 1 as the frequency
    grows, which is what fixes the signal front at c."""
    return math.sqrt(1 + lorentz_dispersion(omega, omega_0, gamma, strength))


def front_velocity() -> int:
    """c, exactly, in every causal medium.

    From causality alone (Titchmarsh): no output before input makes chi
    analytic in the upper half plane, so chi -> 0 and n -> 1 at high
    frequency. Independent of what the medium is, which is why an
    unknown field is bound as tightly as a known one."""
    return SPEED_OF_LIGHT


def minimum_transit_time(distance: Fraction) -> Fraction:
    """dx/c, exact. The least time a signal can take to cross a
    distance, set by the front velocity."""
    if Fraction(distance) < 0:
        raise ValueError("distance must be non-negative")
    return Fraction(distance) / SPEED_OF_LIGHT


def transmitted_distance_is_the_minimised_quantity() -> bool:
    """True.

    Letting dx -> 0 does not produce a fast transfer; the transmitted
    distance *is* dx, so dx = 0 is no transfer. The quantity being
    minimised and the quantity that makes the transfer useful are the
    same quantity."""
    return True
