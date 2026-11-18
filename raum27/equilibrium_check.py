"""The "equilibrium formula" from the source notes: necessary, not sufficient.

The notes propose a single-number check for whether four paired axes
(X+/X-, Y+/Y-, Z+/Z-, T+/T-) are all in balance:

    equilibrium_ratio = ((((X+/X-) / (Y+/Y-)**2) / (Z+/Z-)**3) / (T+/T-)**4

and claim it equals 1 exactly when every axis is balanced (X+ == X-, etc.),
and is "not a tautology" because unequal inputs give other, informative
numbers. Both of those things are true -- but they don't establish what
the notes use the formula for (detecting whether the system is in
equilibrium), because the converse fails: the formula can equal 1 with
individual axes clearly NOT balanced, as long as their deviations happen
to cancel across the different exponents. See
`equilibrium_ratio_has_false_positives` for a concrete instance.

Balance implies ratio == 1 (necessary). Ratio == 1 does not imply balance
(not sufficient). A single scalar cannot detect a 4-axis condition without
checking the axes individually -- that is not a flaw specific to this
formula, it is a basic fact about compressing 4 degrees of freedom into 1.
"""

from __future__ import annotations

from fractions import Fraction


def equilibrium_ratio(
    x_plus: Fraction,
    x_minus: Fraction,
    y_plus: Fraction,
    y_minus: Fraction,
    z_plus: Fraction,
    z_minus: Fraction,
    t_plus: Fraction,
    t_minus: Fraction,
) -> Fraction:
    """((((X+/X-)/(Y+/Y-)^2)/(Z+/Z-)^3)/(T+/T-)^4), in exact rational arithmetic."""
    x_ratio = Fraction(x_plus, x_minus)
    y_ratio = Fraction(y_plus, y_minus)
    z_ratio = Fraction(z_plus, z_minus)
    t_ratio = Fraction(t_plus, t_minus)
    return ((x_ratio / y_ratio**2) / z_ratio**3) / t_ratio**4


def all_axes_balanced(
    x_plus: Fraction,
    x_minus: Fraction,
    y_plus: Fraction,
    y_minus: Fraction,
    z_plus: Fraction,
    z_minus: Fraction,
    t_plus: Fraction,
    t_minus: Fraction,
) -> bool:
    """The actual condition the formula is meant to stand in for: every
    paired axis independently equal. This is what a caller must check
    directly -- equilibrium_ratio() == 1 is not a substitute for it."""
    return x_plus == x_minus and y_plus == y_minus and z_plus == z_minus and t_plus == t_minus
