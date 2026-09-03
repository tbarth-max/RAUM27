"""RAUM27 Hyperoperationen: addition, multiplication, exponentiation, and
tetration as a hierarchy where each operation is repeated application of
the one before it. Standard mathematics (Knuth's up-arrow notation /
the Grzegorczyk hierarchy) -- included here because it came up directly
in conversation, and because it clarifies a point worth stating
precisely: root extraction and the logarithm are NOT a separate rung of
this ladder above exponentiation. They are the two different inverses of
the SAME operation (b**x = y): a root solves for the base b, a logarithm
solves for the exponent x. The next real rung above exponentiation is
tetration, whose own two inverses (super-root, super-logarithm) are not
implemented here.

Ported from an external submission whose own numeric example (a=2, n=3
giving 5, 6, 8, 16) was reproduced exactly here -- with one fix: a first,
more "elegant" implementation attempted to define every level purely
recursively down to addition (matching the formal mathematical
definition), and was abandoned after it hung: at n=4 (tetration), the
argument fed into the n=3 (exponentiation) level is itself already a
tower, and simulating exponentiation as a loop of that many repeated
multiplications is computationally infeasible even for tiny inputs like
a=3, b=3. Redone using native +, *, ** for the first three levels
(mathematically exact and fast) and a manual loop only for tetration
itself, which is inherently limited to tiny bases and heights regardless
of implementation -- the same practical choice the source file made.
"""

from __future__ import annotations


def addition(a: int, b: int) -> int:
    return a + b


def multiplication_as_repeated_addition(a: int, b: int) -> int:
    result = 0
    for _ in range(b):
        result = addition(result, a)
    return result


def power_as_repeated_multiplication(a: int, b: int) -> int:
    result = 1
    for _ in range(b):
        result = result * a
    return result


def tetration_as_repeated_power(a: int, b: int) -> int:
    """a^^b: a**(a**(...**a)), b times. Grows too fast to evaluate
    honestly beyond very small a, b (e.g. 3^^3 is already 7,625,597,484,987;
    4^^3 has 155 digits) -- that growth rate is the point being
    demonstrated, not a limitation to work around."""
    result = 1
    for _ in range(b):
        result = a**result
    return result
