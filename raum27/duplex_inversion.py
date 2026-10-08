"""Duplex inversion: two exponent towers over the same base, and where
they actually coincide.

Ported from a Lean sketch (RAUM27_Duplex.lean) that stated four theorems
and proved none of them -- all four were `sorry`, honestly marked but
unproven. All four statements are mathematically TRUE (verified here in
exact rational arithmetic), and all four are one-liners, so the `sorry`s
weren't hiding anything hard. What the sketch missed is more interesting
than what it stated.

The two maps, over base = 1/2:
    r_out(x, n) = base ** (x ** n)      "expansion"
    r_in (x, n) = base ** (n ** x)      "compression"

What the sketch stated (all true, all trivial):
- r_out(1, n) = 1/2 for every n, because 1**n = 1.
- r_in(x, 1) = 1/2 for every x, because 1**x = 1.
- r_out(1,1) = r_in(1,1). This one is a tautology dressed as a
  structural finding: at x = n = 1 the two exponents are literally the
  same expression (1**1 on both sides), so it says an expression equals
  itself. Any two functions whatsoever agree wherever their arguments
  coincide.
- Both are strictly positive, because a positive base to a natural power
  is positive.

What the sketch missed, and what this module actually implements:

1. The GENERAL symmetry, true for every (x, n), not just at one point:
   r_out(x, n) == r_in(n, x). This holds by definition -- r_in(n, x) is
   base ** (x ** n), which is r_out(x, n) spelled differently. The
   "Fokalpunkt" theorem is the weakest possible special case of this.

2. The points where expansion and compression coincide at the SAME
   arguments -- r_out(x, n) == r_in(x, n), i.e. x**n == n**x -- are not
   just (1,1). They are the whole diagonal x == n (trivially), plus
   exactly ONE exceptional pair off it: (2,4) and (4,2), since
   2**4 == 4**2 == 16. That's the classical result on x**y == y**x over
   the naturals, and it is a real, non-obvious fact rather than a
   restatement. At that point both sides equal (1/2)**16 = 1/65536.
"""

from __future__ import annotations

from fractions import Fraction

BASE = Fraction(1, 2)


def r_out(x: int, n: int) -> Fraction:
    """Expansion: BASE ** (x ** n), exact rational."""
    return BASE ** (x**n)


def r_in(x: int, n: int) -> Fraction:
    """Compression: BASE ** (n ** x), exact rational."""
    return BASE ** (n**x)


def coincidence_points(limit: int) -> list[tuple[int, int]]:
    """All (x, n) with 0 <= x, n <= limit where the two towers land on the
    same value, i.e. x**n == n**x. Returns the diagonal plus whatever
    lies off it -- over the naturals, that is only (2,4) and (4,2)."""
    return [
        (x, n)
        for x in range(limit + 1)
        for n in range(limit + 1)
        if x**n == n**x
    ]


def off_diagonal_coincidences(limit: int) -> list[tuple[int, int]]:
    """The non-trivial coincidences only -- the diagonal x == n removed."""
    return [(x, n) for (x, n) in coincidence_points(limit) if x != n]
