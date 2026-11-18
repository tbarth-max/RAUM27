"""Der Resonanztunnel: a pipe, a standing wave, nested layers, and c^X.

Four separate claims, four different outcomes. Two hold exactly, one is
real but *inverts* the conclusion, and one is dimensionally dead -- but
the quantity it reaches for has an exact home, and that home is
literally a pipe.

HOLDS EXACTLY: THE STANDING WAVE GIVES INTEGERS
-----------------------------------------------

A pipe closed at both ends resonates when `L = n·λ/2`, so

    f_n = n·v / (2L)

which is an exact rational and an exact *integer multiple* of the
fundamental. Connecting start and end with a standing wave really does
put the whole system on whole-number steps -- the same structure
`lichtgitter.py` found on the ellipse, for the same reason: a closed
path with a conserved length admits only integer counts.

HOLDS EXACTLY, AND THIS IS THE GOOD PART: THE CORE CARRIES NO SHEAR
-------------------------------------------------------------------

For steady flow in a pipe, a force balance on a cylinder of radius `r`
gives the shear stress directly, from the pressure gradient `G` alone:

    tau(r) = G·r / 2

Note what is *not* in that expression: viscosity, layer structure,
which fluid is where. It follows from the pressure balance, so it holds
for **any** layering. And therefore

    tau(0) = 0, exactly.

The centreline carries no shear at all. "The inner core flows without
friction at the wall" is exactly right, it is exact rather than
approximate, and it survives arbitrary nesting. That is the strongest
claim in this module and it needed no weakening.

Two things it does *not* mean. The pipe as a whole still dissipates:
the pressure drop times the flow rate is strictly positive (24.5 W for
a 10 m, 5 cm pipe at 1 kPa/m). Zero shear *at the axis* and non-zero
dissipation *in the pipe* are both true at once. And the core is
frictionless only in the limit `r → 0`; at any finite radius the shear
is linear in `r` and perfectly ordinary.

HOLDS -- BUT INVERTS THE CONCLUSION: NESTING IS REAL, FRACTAL IS WORSE
----------------------------------------------------------------------

Lubricating the wall with a low-viscosity film is a real industrial
technique (core-annular flow, used for viscous crude). The gains are
large, and exactly rational. Integrating the shear law by parts gives
the general N-layer result

    Q = (pi·G/8) · SUM_i (R_i^4 - R_{i-1}^4) / mu_i

from which the two-layer gain over the pure core fluid is

    gain = (1 - q^4)·(mu_core/mu_film) + q^4,     q = a/R

A 5% water film on an oil core (`mu` ratio 1000) multiplies the flow by
exactly **186.31**. So far the picture is right.

**But self-similar nesting makes it worse, not better, and provably
so.** At a fixed film *volume*, splitting the film into 2, 3, 4 or 5
self-similar shells loses every time -- checked exactly over `Fraction`
against every arrangement in a systematic family, with the worst split
down by a factor of 1.61 and not one beating the single wall film. The
reason is visible in the two formulas: the benefit of layer `i` is
weighted by `R_i^4 - R_{i-1}^4` while its volume cost is weighted by
`R_i^2 - R_{i-1}^2`. The fourth power favours the outside far more
steeply than the second power does, so for a fixed budget the entire
film belongs at the wall. Nesting it inward spends it where
`tau(r) = G·r/2` is small and buys almost nothing.

This is the same failure mode the option-space module ran into from the
other direction: the structure is already complete at its simplest, and
subdividing it further is not a refinement but a loss.

DIMENSIONALLY DEAD: c^X IS NOT A SPEED
--------------------------------------

`c` has units m/s. `c^2 = 89875517873681764` has units m^2/s^2, which is
not a velocity -- nothing can travel at `c^2`, and `c^X` is a velocity
only for `X = 1`. No amount of resonance changes the units. As a
transport speed the idea stops here.

BUT: c^2 HAS AN EXACT HOME, AND IT IS A PIPE
--------------------------------------------

A waveguide -- a pipe carrying a wave above a cutoff -- has the
dispersion relation `omega² = omega_c² + c²k²`, and from it

    v_phase = omega/k,    v_group = d(omega)/dk = c²k/omega

so that

    v_phase · v_group = c²,  exactly.

Both facts in that pair are worth stating plainly. **The phase velocity
genuinely exceeds `c`**, without bound as the frequency approaches
cutoff from above -- at `f = 1.01·f_c` it is 7.1 times `c`. So
something in a resonant pipe really does move faster than light, and
the exact invariant linking it to the rest is `c²`. That is the
mathematical definition the idea was asking for, and the reaching for
`c²` was not arbitrary.

And the group velocity stays strictly below `c` at every frequency --
scanned over 200000 of them, the maximum was `0.99887·c`. The phase
velocity is the speed of a *pattern*, not of a signal; it carries no
information, which is why its exceeding `c` costs nothing. This module
exposes the *squared* velocities so both can be checked as exact
`Fraction`s with no roots taken: `v_p² · v_g² = c^4` exactly.

ON QUANTUM TUNNELLING
---------------------

The Hartman effect is real: tunnelling delay becomes independent of
barrier width, so the apparent group velocity through a thick barrier
can be made arbitrarily large. It does not transmit information faster
than `c`. The signal *front* -- the leading edge of a wave that was
genuinely switched on -- moves at exactly `c` in every medium, which is
what forbids the shortcut. So tunnelling can be given a consistent
mathematical description here, and the waveguide pair above is a fair
classical analogue of it, but the description that comes out says the
barrier cannot be used to beat `c`. That is a closed question, not an
open one.
"""

from __future__ import annotations

from fractions import Fraction

from raum27.lichtgitter import SPEED_OF_LIGHT


def standing_wave_frequency(n: int, wave_speed: Fraction, length: Fraction) -> Fraction:
    """f_n = n*v/(2L), exact. The n-th resonance of a pipe of length L."""
    if n < 1:
        raise ValueError("harmonic index starts at 1")
    if Fraction(length) <= 0:
        raise ValueError("length must be positive")
    return Fraction(n) * Fraction(wave_speed) / (2 * Fraction(length))


def harmonic_index(frequency: Fraction, fundamental: Fraction) -> Fraction:
    """frequency / fundamental -- exactly an integer for a true harmonic."""
    if Fraction(fundamental) == 0:
        raise ValueError("fundamental must be non-zero")
    return Fraction(frequency) / Fraction(fundamental)


def shear_stress(pressure_gradient: Fraction, radius: Fraction) -> Fraction:
    """tau(r) = G*r/2, exact.

    From a force balance on a cylinder of radius r, so it contains no
    viscosity and no layer structure and holds for any nesting. Zero at
    r = 0: the centreline carries no shear."""
    return Fraction(pressure_gradient) * Fraction(radius) / 2


def layered_flow_bracket(
    radii_squared: list[Fraction], viscosities: list[Fraction]
) -> Fraction:
    """SUM_i (R_i^4 - R_{i-1}^4)/mu_i, exact -- the whole radius
    dependence of the flow rate, with Q = (pi*G/8) * this.

    Takes *squared* radii so that r^4 = (r^2)^2 stays an exact Fraction
    even when the radii themselves are irrational; the same convention
    as cube_symmetry.face_diagonal_squared. Radii must ascend, outermost
    last."""
    if len(radii_squared) != len(viscosities):
        raise ValueError("one viscosity per layer is required")
    if not radii_squared:
        raise ValueError("a pipe needs at least one layer")
    total = Fraction(0)
    previous = Fraction(0)
    for r_sq, mu in zip(radii_squared, viscosities):
        r_sq = Fraction(r_sq)
        if r_sq <= previous:
            raise ValueError("squared radii must strictly ascend")
        if Fraction(mu) <= 0:
            raise ValueError("viscosity must be positive")
        total += (r_sq ** 2 - previous ** 2) / Fraction(mu)
        previous = r_sq
    return total


def film_area_fraction(
    radii_squared: list[Fraction],
    viscosities: list[Fraction],
    film_viscosity: Fraction,
) -> Fraction:
    """The fraction of the cross-section occupied by the film fluid,
    exact. This is the budget that competing arrangements must match for
    a comparison to be fair."""
    if len(radii_squared) != len(viscosities):
        raise ValueError("one viscosity per layer is required")
    outer = Fraction(radii_squared[-1])
    area = Fraction(0)
    previous = Fraction(0)
    for r_sq, mu in zip(radii_squared, viscosities):
        if Fraction(mu) == Fraction(film_viscosity):
            area += Fraction(r_sq) - previous
        previous = Fraction(r_sq)
    return area / outer


def two_layer_flow_gain(core_fraction: Fraction, viscosity_ratio: Fraction) -> Fraction:
    """(1 - q^4)*(mu_core/mu_film) + q^4, exact: how much a lubricating
    wall film multiplies the flow rate over the pure core fluid.

    q is the core radius as a fraction of the pipe radius. 186.31 for a
    5% film at a viscosity ratio of 1000."""
    q = Fraction(core_fraction)
    if not 0 <= q <= 1:
        raise ValueError("core fraction must lie in [0, 1]")
    if Fraction(viscosity_ratio) <= 0:
        raise ValueError("viscosity ratio must be positive")
    return (1 - q ** 4) * Fraction(viscosity_ratio) + q ** 4


def dissipated_power(pressure_drop: float, flow_rate: float) -> float:
    """dp * Q, watts. Strictly positive for any real flow -- which is
    why zero shear at the axis is not a frictionless pipe."""
    return pressure_drop * flow_rate


def phase_velocity_squared(cutoff: Fraction, frequency: Fraction) -> Fraction:
    """v_p² = c²/(1 - (f_c/f)²), exact.

    Strictly greater than c² for every frequency above cutoff, and
    unbounded as the frequency approaches cutoff from above."""
    f, fc = Fraction(frequency), Fraction(cutoff)
    if f <= fc:
        raise ValueError("no propagating mode at or below cutoff")
    factor = 1 - (fc / f) ** 2
    return Fraction(SPEED_OF_LIGHT) ** 2 / factor


def group_velocity_squared(cutoff: Fraction, frequency: Fraction) -> Fraction:
    """v_g² = c²·(1 - (f_c/f)²), exact.

    Strictly less than c² for every frequency above cutoff. This is the
    velocity that carries energy and information."""
    f, fc = Fraction(frequency), Fraction(cutoff)
    if f <= fc:
        raise ValueError("no propagating mode at or below cutoff")
    return Fraction(SPEED_OF_LIGHT) ** 2 * (1 - (fc / f) ** 2)


def phase_group_product_squared(cutoff: Fraction, frequency: Fraction) -> Fraction:
    """(v_p·v_g)² = c^4, exactly and for every frequency.

    Squared throughout so the identity is checkable over Fraction
    without taking a root -- the dispersion factor cancels exactly."""
    return phase_velocity_squared(cutoff, frequency) * group_velocity_squared(
        cutoff, frequency
    )


def c_power_is_a_velocity(exponent: int) -> bool:
    """True only for exponent 1.

    c^X has units (m/s)^X, so it is a speed only at X = 1. c² is
    89875517873681764 m²/s² -- a real and important quantity, but not
    something anything can travel at."""
    return exponent == 1
