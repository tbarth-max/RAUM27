"""Der Kompressions-Schwellenwert: when does a lattice stop holding and flow?

Thomas asked for exactly one thing here: the function at which a local
impulse on a minimal `Δx` breaks the existing lattice and triggers the
flow into a new structure. That function exists, it is standard
mechanics, and it is computable. This module implements it, together
with the `dx`/`dt` kinematics he described -- which turn out to be the
textbook derivation of penetration depth, not an analogy to it.

**NOTE ON UNITS.** Unlike the rest of this package this module uses
floats in SI, not exact `Fraction`s. Densities and yield strengths are
measured material properties, so exactness would be false precision.
The one genuinely exact statement here (`P/L = √(ρ_j/ρ_t)`) is verified
symbolically in the tests.

WHAT HOLDS IN THE ORIGINAL FRAMING
----------------------------------

**"Kein Schmelzen, sondern erzwungenes Fließen" is correct**, and it is
mainstream high-velocity impact mechanics, not a fringe reading. The
mechanism is that the *inertial* stress overwhelms the material's
strength, so strength drops out of the balance and both bodies behave
like fluids. The threshold is a dimensionless number -- Johnson's
damage number

    D = ρ·v² / Y

with `D << 1` elastic (the lattice holds), `D ≈ 1` the onset of plastic
flow, `D >> 1` strength irrelevant and the material flows. Setting
`D = 1` gives the flow threshold velocity `v = √(Y/ρ)`: about **357 m/s
for steel**, 149 m/s for copper, 33 m/s for lead. That is the
"strukturelle Haltekraft" being exceeded, as an actual number.

**The `dx`/`dt` framing is the real derivation.** Balancing stagnation
pressure across the interface, `½ρ_j(v−u)² = ½ρ_t·u²`, gives the
interface velocity `u = v/(1 + √(ρ_t/ρ_j))`. A rod of known length `L`
is consumed in `t = L/(v−u)` -- precisely "the time it takes to get
through" -- and the depth is `P = u·t`. Substituting collapses to

    P / L = √(ρ_j / ρ_t)

exactly, and **independent of velocity** (Birkhoff, MacDougall, Pugh &
Taylor 1948). So knowing the length and the traversal time really does
give the penetration velocity, exactly as described. That is a strong,
surprising, checkable result and it is the correct formalisation.

WHAT DOES NOT HOLD, COMPUTED RATHER THAN ASSERTED
-------------------------------------------------

**"Keine thermische Entropie", "kalter Phasenübergang" -- this is
false.** Shock compression is the textbook example of an *irreversible*
process; the entropy jump is what distinguishes a shock from an
isentropic compression. The Hugoniot internal energy jump for a shock
into material at rest is `Δe = ½u_p²`, so

    ΔT ≈ u_p² / (2·c_p)

For steel (`c_p ≈ 450 J/(kg·K)`): 278 K at a particle velocity of
500 m/s, **1111 K at 1000 m/s, and past steel's melting point at about
1160 m/s** on shock heating alone. Shaped-charge jets and impact
craters do melt material, and they do it thermally. The process is
emphatically hot and emphatically dissipative.

**"Die Energie geht restlos in die Überwindung der Gitterbindung" --
also false, by a wide margin.** Breaking *all* iron lattice bonds costs
its cohesive energy, about **7.39 MJ/kg**. Kinetic energy per unit mass
is `½v²`, so at 1700 m/s an impact brings 1.45 MJ/kg -- **19.5%** of
that. Only above roughly **3.8 km/s** does the kinetic energy per mass
even reach the cohesive energy, and most of it goes into bulk plastic
work and heat, not bond-breaking. At ordnance velocity the lattice is
not dismantled; a thin layer at the crater wall is sheared apart while
the bulk stays a solid crystal.

**It is not a phase transition.** "Flow" here means strength is
negligible compared to inertial stress -- a change of *constitutive
regime*, not of phase. The material is still crystalline solid
throughout; it is being deformed, not transformed.

**The recrystallisation is real, but for the opposite reason.** Dynamic
recrystallisation in adiabatic shear bands under high strain rate is a
well-documented effect in steel. It is driven by exactly the local
adiabatic *heating* the "cold" framing denies. The conclusion survives;
the stated mechanism inverts.

**Validation against reality.** The strengthless limit overshoots at
ordinary velocity. Adding strength back (Tate / Alekseevskii:
`½ρ_j(v−u)² + Y_p = ½ρ_t·u² + R_t`) gives, for a 0.6 m tungsten rod
into steel, `P/L = 1.21` at 1700 m/s -- which is where real long-rod
penetrators against armour steel actually sit, against a strengthless
prediction of 1.57. The Tate result rises monotonically with velocity
and approaches the hydrodynamic limit from below without ever crossing
it (checked out to 100 km/s). It also predicts a ballistic limit: below
about 455 m/s a tungsten rod stops penetrating steel at all.

WHERE THIS IS *NOT* RAUM27
--------------------------

Stated plainly, because this project has a recurring failure mode of
dropping a number into a conceptually waiting slot: **nothing here
derives from cube geometry.** The threshold is `ρv²/Y` and the depth
ratio is `√(ρ_j/ρ_t)`. Neither contains 6, 8, 4/3, 9/16 or 27, and no
step of either derivation uses a lattice of faces and corners -- they
use momentum and mass conservation across an interface. This is real,
verified mechanics that answers the question asked. It is not evidence
for the RAUM27 architecture, and treating the agreement as support
would be exactly the circularity flagged elsewhere in this repository.
"""

from __future__ import annotations

import math

# Reference properties, SI. Yield strengths are order-of-magnitude
# representative values for engineering alloys, not single-crystal data.
DENSITY = {
    "steel": 7850.0,
    "copper": 8960.0,
    "tungsten": 19300.0,
    "aluminium": 2700.0,
    "lead": 11340.0,
}
YIELD_STRENGTH = {
    "steel": 1.0e9,
    "copper": 2.0e8,
    "tungsten": 1.5e9,
    "aluminium": 2.8e8,
    "lead": 1.2e7,
}
SPECIFIC_HEAT = {"steel": 450.0, "copper": 385.0, "tungsten": 134.0, "aluminium": 900.0}

#: Cohesive (sublimation) energy of iron, J/kg -- the cost of breaking
#: every lattice bond. 4.28 eV/atom over a molar mass of 55.845 g/mol.
IRON_COHESIVE_ENERGY = 4.28 * 1.602176634e-19 * 6.02214076e23 / 0.055845


def dynamic_pressure(density: float, velocity: float) -> float:
    """Stagnation pressure ½ρv², Pa -- the load the lattice has to hold."""
    return 0.5 * density * velocity * velocity


def johnson_damage_number(density: float, velocity: float, strength: float) -> float:
    """D = ρv²/Y, the threshold the question was asking for.

    D << 1 elastic, the lattice holds. D ≈ 1 onset of plastic flow.
    D >> 1 strength is irrelevant and the material flows."""
    if strength <= 0:
        raise ValueError("strength must be positive")
    return density * velocity * velocity / strength


def flow_threshold_velocity(density: float, strength: float) -> float:
    """The velocity at which D = 1: v = √(Y/ρ).

    Below it the structure carries the load elastically; above it the
    lattice gives. 357 m/s for steel."""
    if density <= 0:
        raise ValueError("density must be positive")
    return math.sqrt(strength / density)


def interface_velocity(density_rod: float, density_target: float, velocity: float) -> float:
    """u = v/(1 + √(ρ_t/ρ_j)), from ½ρ_j(v−u)² = ½ρ_t·u².

    The speed at which the hole deepens -- the dx/dt of the process."""
    if density_rod <= 0 or density_target <= 0:
        raise ValueError("densities must be positive")
    return velocity / (1.0 + math.sqrt(density_target / density_rod))


def erosion_time(length: float, velocity: float, interface: float) -> float:
    """t = L/(v−u): how long a rod of known length takes to be consumed.

    This is the measurable quantity -- the traversal time."""
    if velocity <= interface:
        raise ValueError("rod is not being consumed: v must exceed u")
    return length / (velocity - interface)


def penetration_from_time(interface: float, time: float) -> float:
    """P = u·t. Depth as velocity times traversal time, the dx/dt form."""
    return interface * time


def hydrodynamic_penetration(
    density_rod: float, density_target: float, length: float
) -> float:
    """P = L·√(ρ_j/ρ_t), the strengthless limit.

    Independent of impact velocity -- the surprising content of the
    1948 result. Cross-checked against the step-by-step u·t route in
    tests/test_impakt_schwelle.py."""
    if density_rod <= 0 or density_target <= 0:
        raise ValueError("densities must be positive")
    return length * math.sqrt(density_rod / density_target)


def shock_temperature_rise(particle_velocity: float, specific_heat: float) -> float:
    """ΔT ≈ u_p²/(2c_p), from the Hugoniot energy jump Δe = ½u_p².

    Exists precisely because shock compression is irreversible, which is
    why the process cannot be called a cold or entropy-free
    transition."""
    if specific_heat <= 0:
        raise ValueError("specific heat must be positive")
    return particle_velocity * particle_velocity / (2.0 * specific_heat)


def cohesive_energy_fraction(
    velocity: float, cohesive_energy: float = IRON_COHESIVE_ENERGY
) -> float:
    """½v² divided by the cost of breaking every lattice bond.

    Below 1 the impact cannot possibly dismantle the lattice, however it
    is distributed. 0.195 at 1700 m/s for iron."""
    if cohesive_energy <= 0:
        raise ValueError("cohesive energy must be positive")
    return 0.5 * velocity * velocity / cohesive_energy


def tate_interface_velocity(
    density_rod: float,
    density_target: float,
    strength_rod: float,
    resistance_target: float,
    velocity: float,
) -> float | None:
    """Interface velocity with strength retained:
    ½ρ_j(v−u)² + Y_p = ½ρ_t·u² + R_t.

    Returns None when no root in [0, v] exists -- the rod is below the
    ballistic limit and does not penetrate at all, which the
    strengthless model cannot express."""
    a = 0.5 * (density_target - density_rod)
    b = density_rod * velocity
    c = resistance_target - strength_rod - 0.5 * density_rod * velocity * velocity
    if abs(a) < 1e-12:
        if abs(b) < 1e-12:
            return None
        u = -c / b
        return u if 0.0 <= u <= velocity else None
    disc = b * b - 4.0 * a * c
    if disc < 0.0:
        return None
    root = math.sqrt(disc)
    candidates = [r for r in ((-b + root) / (2 * a), (-b - root) / (2 * a))
                  if -1e-9 <= r <= velocity + 1e-9]
    if not candidates:
        return None
    return max(0.0, min(candidates))


def tate_penetration(
    density_rod: float,
    density_target: float,
    strength_rod: float,
    resistance_target: float,
    velocity: float,
    length: float,
    dt: float = 2e-9,
) -> float:
    """Integrate the Tate model: erode the rod, decelerate it, deepen
    the hole, until the rod is gone or it drops below the ballistic
    limit.

    Stays below hydrodynamic_penetration at every velocity and
    approaches it from below -- verified in the tests, and the reason
    the strengthless limit must be read as a ceiling rather than a
    prediction."""
    depth = 0.0
    remaining = length
    v = velocity
    while remaining > 1e-9 and v > 0.0:
        u = tate_interface_velocity(
            density_rod, density_target, strength_rod, resistance_target, v
        )
        if u is None or u <= 0.0:
            break
        eroded = (v - u) * dt
        if eroded <= 0.0:
            break
        remaining -= eroded
        depth += u * dt
        v -= strength_rod / (density_rod * max(remaining, 1e-9)) * dt
    return depth


def ballistic_limit_velocity(
    density_rod: float,
    density_target: float,
    strength_rod: float,
    resistance_target: float,
    upper: float = 5.0e4,
) -> float:
    """Slowest impact velocity that still penetrates, by bisection on
    whether tate_interface_velocity has a usable root."""
    lo, hi = 1.0, upper
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        u = tate_interface_velocity(
            density_rod, density_target, strength_rod, resistance_target, mid
        )
        if u is None or u <= 0.0:
            lo = mid
        else:
            hi = mid
    return hi
