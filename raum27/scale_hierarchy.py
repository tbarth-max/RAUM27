"""The 3-adic / 9-adic scale hierarchy from the source notes.

For each level k, a linear scale L_k = 3^k induces an area scale
A_k = (3^k)^2 = 9^k and a volume scale V_k = (3^k)^3 = 27^k.

The notes also claim a "digital root invariance": for k >= 1, the
iterated digit sum (digital root) of 9^k is always 9. This is a standard
number-theory fact (any nonzero multiple of 9 has digital root 9, since
digital_root(n) == 1 + (n - 1) % 9 for n > 0), not something specific to
RAUM27 -- it is reproduced here because it is true and checkable.
"""


def linear_scale(k: int) -> int:
    return 3**k


def area_scale(k: int) -> int:
    return 9**k


def volume_scale(k: int) -> int:
    return 27**k


def digital_root(n: int) -> int:
    """Iterated digit sum of a positive integer, e.g. digital_root(9999) == 9."""
    if n <= 0:
        raise ValueError("digital_root is defined for positive integers")
    return 1 + (n - 1) % 9
