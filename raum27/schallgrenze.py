"""Sound speed c_s^2 = K / rho under expansion and its mirrored compression.

The idea: keep the amount, expand the space, keep the stiffness K. On the
expanding side the density falls by x^3, on the mirrored side the path
shrinks to 1/x and the density rises by x^3. Kept as squares, exactly:

    c_exp^2  = K x^3 / rho0        c_comp^2 = K / (rho0 x^3)
    c_exp^2 * c_comp^2 = (K / rho0)^2      -- the product never moves

so the two speeds mirror each other around c0 like x and 1/x around 1.
Three limits come with it, all exact:

* c_s <= c caps the expansion: c_exp reaches c once x^3 = rho0 c^2 / K.
  For water (K = 2.2 GPa, rho = 1000 kg/m^3) rho c^2 / K is about
  4.1 * 10^10, so the cap comes at a linear factor of 3446.
* Keeping K (the pressure) while the volume grows is not free: it is the
  work p * dV, paid from inside -- the main condition E_inner >= E_outer.
* A real gas does not do this by itself: at fixed temperature K = gamma p
  falls with rho, and c_s stays the same.
"""

from fractions import Fraction

MODEL_C = Fraction(300000000)


def _exact(*values):
    for v in values:
        if isinstance(v, float):
            raise TypeError("exact module: use int or Fraction, not float")
    return [Fraction(v) for v in values]


def speed_squared(stiffness, density):
    K, rho = _exact(stiffness, density)
    if K <= 0 or rho <= 0:
        raise ValueError("positive stiffness and density")
    return K / rho


def stiffness_for_speed(speed, density):
    """K that would make c_s equal to ``speed``: K = rho c^2."""
    c, rho = _exact(speed, density)
    return rho * c * c


def mirrored(stiffness, density, x):
    """(c_exp^2, c_comp^2) when one side expands by x and the mirror compresses to 1/x."""
    (x,) = _exact(x)
    if x <= 0:
        raise ValueError("x > 0")
    base = speed_squared(stiffness, density)
    return base * x ** 3, base / x ** 3


def expansion_cap_cubed(stiffness, density, c=MODEL_C):
    """x^3 at which the expanding side reaches c: rho0 c^2 / K."""
    return stiffness_for_speed(c, density) / Fraction(stiffness)


def first_x_beyond_c(stiffness, density, c=MODEL_C):
    """Smallest whole expansion factor at which c_exp would exceed c."""
    cap = expansion_cap_cubed(stiffness, density, c)
    x = 1
    step = 1
    while (x + step) ** 3 <= cap:
        step *= 2
    while step:
        if (x + step) ** 3 <= cap:
            x += step
        step //= 2
    return x + 1


def work_at_constant_pressure(pressure, volume_before, volume_after):
    """Energy needed to keep the pressure while the volume grows: p * dV."""
    p, v0, v1 = _exact(pressure, volume_before, volume_after)
    return p * (v1 - v0)
