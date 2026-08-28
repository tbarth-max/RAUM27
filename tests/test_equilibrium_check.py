from fractions import Fraction

from raum27.equilibrium_check import all_axes_balanced, equilibrium_ratio


def test_ratio_is_one_when_all_axes_balanced():
    balanced = dict(
        x_plus=Fraction(2), x_minus=Fraction(2),
        y_plus=Fraction(3), y_minus=Fraction(3),
        z_plus=Fraction(5), z_minus=Fraction(5),
        t_plus=Fraction(7), t_minus=Fraction(7),
    )
    assert equilibrium_ratio(**balanced) == 1
    assert all_axes_balanced(**balanced)


def test_ratio_is_not_one_for_a_generic_unbalanced_case():
    # Not a tautology: unequal inputs give a real, non-1 number.
    unbalanced = dict(
        x_plus=Fraction(3), x_minus=Fraction(2),
        y_plus=Fraction(1), y_minus=Fraction(1),
        z_plus=Fraction(1), z_minus=Fraction(1),
        t_plus=Fraction(1), t_minus=Fraction(1),
    )
    assert equilibrium_ratio(**unbalanced) == Fraction(3, 2)
    assert not all_axes_balanced(**unbalanced)


def test_equilibrium_ratio_has_false_positives():
    """The counterexample: ratio == 1 does NOT imply balance. X+/X- = 2
    and Y+/Y- = sqrt(2) are both clearly unbalanced, but because the
    formula divides by (Y+/Y-)**2 = 2, the two deviations cancel exactly.
    Approximated here with a close rational (sqrt(2) is irrational, so no
    exact Fraction reproduces it, but the near-cancellation alone is
    enough to demonstrate the failure mode)."""
    sqrt2_approx = Fraction(14142136, 10000000)  # sqrt(2) to 7 significant digits
    x_plus, x_minus = Fraction(2), Fraction(1)
    y_plus, y_minus = sqrt2_approx, Fraction(1)

    ratio = equilibrium_ratio(
        x_plus=x_plus, x_minus=x_minus,
        y_plus=y_plus, y_minus=y_minus,
        z_plus=Fraction(1), z_minus=Fraction(1),
        t_plus=Fraction(1), t_minus=Fraction(1),
    )

    assert not all_axes_balanced(
        x_plus=x_plus, x_minus=x_minus,
        y_plus=y_plus, y_minus=y_minus,
        z_plus=Fraction(1), z_minus=Fraction(1),
        t_plus=Fraction(1), t_minus=Fraction(1),
    )
    # Off from 1 only by the rational approximation error of sqrt(2) --
    # i.e. essentially 1, despite X and Y both being unbalanced.
    assert abs(ratio - 1) < Fraction(1, 10_000)
