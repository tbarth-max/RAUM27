"""The rhombus shell: the sphere's bookkeeping inside the cube, without a single root.

* **The rhombus is the sphere in grid distance.** |x| + |y| + |z| = s is
  the octahedron (the p-ball with p = 1). At s = a/2 its six tips sit on
  the face centres, at s = a it runs through the 12 edge midpoints (the
  cuboctahedron), at s = 3a/2 it reaches the corners. The shell of a hit
  is a sum, so scaling it onto 9/2 always needs a fraction, never a root.
* **The angle balances rhombus and sphere.** With theta the angle between
  p and the diagonal of its octant: shell^2 = 3 cos^2(theta) |p|^2, and
  cos^2(theta) is a fraction for every rational point. The factor
  3 cos^2 counts 1 : 2 : 3 on face, edge and corner -- the same count as
  the sphere's r^2 = a^2/4 : a^2/2 : 3a^2/4.
* **Four bits on X, Y, Z, T.** One bit per tetrahedral axis (1 when the
  reading is positive). Because X + Y + Z + T = 0, only 14 of the 16
  words occur: two ones -- the 6 faces, one or three ones -- the 8
  corners. 0000 is rest (nothing to see), 1111 never occurs; the opposite
  direction is the inverted word.
* **Halving (octree) and folding.** Each halving names one of 8 octants
  (3 bits) and moves its centre to the zero point; each fold mirrors at
  a wall, and a fractional fold count says knicks + position.
* **The complexity jump.** A delta below the binary limit 1/base^bits is
  scaled up by base^bits and carried on one level down -- mantissa and
  level, as in floating point; the way back is exact. The carry of the
  ten into the next wheel is ``zahnwerk``.

Open definitions are parameters, not fixed here: what a coordinate that
is exactly 0 counts as (``zero_positive`` / ``zero_bit``), and the jump
factor (``base``).
"""

from fractions import Fraction

from raum27.eckenruecklauf import DIAGONAL_AXES, NINE_HALVES


def _exact(*values):
    for v in values:
        if isinstance(v, float):
            raise TypeError("exact module: use int or Fraction, not float")
    return [Fraction(v) for v in values]


def _dot(p, d):
    return sum(a * b for a, b in zip(p, d))


# --- shell, angle, scale -----------------------------------------------------------


def shell(point):
    """Grid distance |x| + |y| + |z|: the rhombus (octahedron) through the point."""
    return sum(abs(c) for c in _exact(*point))


def octant_diagonal(point, zero_positive=True):
    """The corner direction (+-1, +-1, +-1) of the point's octant."""
    return tuple(1 if c > 0 or (c == 0 and zero_positive) else -1 for c in _exact(*point))


def cos2_to_corner(point):
    """cos^2 of the angle between the point and the diagonal of its octant, exact."""
    p = _exact(*point)
    r2 = sum(c * c for c in p)
    if r2 == 0:
        raise ValueError("the centre has no direction")
    return _dot(p, octant_diagonal(p)) ** 2 / (3 * r2)


def balance_factor(point):
    """3 cos^2: 1 on a face direction, 2 on an edge, 3 on a corner."""
    return 3 * cos2_to_corner(point)


def sphere_r2_from_shell(shell_value, factor):
    """|p|^2 back from the rhombus shell and the balance factor: shell^2 / factor."""
    shell_value, factor = _exact(shell_value, factor)
    if factor <= 0:
        raise ValueError("the balance factor lies between 1 and 3")
    return shell_value * shell_value / factor


def scale_shell_to_nine_halves(point):
    """Scale the point so that its rhombus shell is 9/2 -- the factor is always a fraction."""
    p = _exact(*point)
    s = shell(p)
    if s == 0:
        raise ValueError("the centre has no shell")
    return tuple(NINE_HALVES / s * c for c in p)


# --- four bits on X, Y, Z, T -------------------------------------------------------

REST = (0, 0, 0, 0)


def xyzt_bits(point, zero_bit=0):
    """One bit per tetrahedral axis: 1 when the reading is positive, ``zero_bit`` when it is 0."""
    p = _exact(*point)
    bits = []
    for d in DIAGONAL_AXES:
        r = _dot(p, d)
        bits.append(1 if r > 0 else zero_bit if r == 0 else 0)
    return tuple(bits)


def kind(bits):
    """'rest', 'face' (two ones) or 'corner' (one or three ones); 1111 cannot occur."""
    ones = sum(bits)
    if ones == 4:
        raise ValueError("1111 cannot occur: X + Y + Z + T = 0")
    if tuple(bits) == REST:
        return "rest"
    return "face" if ones == 2 else "corner"


def opposite(bits):
    """The word of the opposite direction (through the centre): every bit inverted."""
    if tuple(bits) == REST:
        raise ValueError("rest has no opposite direction")
    return tuple(1 - b for b in bits)


# --- halving: the octree address ----------------------------------------------------


def octree_address(point, levels, half=NINE_HALVES, zero_positive=True):
    """(octant signs per level, rest point): move the octant centre to 0, double, repeat."""
    p = list(_exact(*point))
    (half,) = _exact(half)
    if any(abs(c) > half for c in p):
        raise ValueError("the point lies outside the cube")
    address = []
    for _ in range(levels):
        signs = octant_diagonal(p, zero_positive)
        address.append(signs)
        p = [2 * (c - s * half / 2) for c, s in zip(p, signs)]
    return address, tuple(p)


def octree_point(address, rest, half=NINE_HALVES):
    """Undo it exactly: halve and add the octant centre back, level by level."""
    p = list(_exact(*rest))
    (half,) = _exact(half)
    for signs in reversed(address):
        p = [c / 2 + s * half / 2 for c, s in zip(p, signs)]
    return tuple(p)


# --- folding: knicks and the position in the first cube ----------------------------


def fold(count):
    """A fold count (a fraction, path / edge) as (knicks, position in the first cube, 0..1)."""
    (count,) = _exact(count)
    if count < 0:
        raise ValueError("count the path from the start, not backwards")
    knicks = count.numerator // count.denominator
    rest = count - knicks
    return knicks, rest if knicks % 2 == 0 else 1 - rest


def unfold(knicks, position):
    """The fold count back from knicks and position."""
    (position,) = _exact(position)
    return knicks + (position if knicks % 2 == 0 else 1 - position)


def closes(counts):
    """The folded path is back at its start, in its old direction: every count an even integer."""
    return all(c.denominator == 1 and c.numerator % 2 == 0 for c in _exact(*counts))


# --- the complexity jump -------------------------------------------------------------


def jump(value, bits=1, base=2):
    """(level, mantissa): while |value| < 1/base^bits, scale it up by base^bits."""
    (value,) = _exact(value)
    if bits < 1 or base < 2:
        raise ValueError("bits >= 1 and base >= 2")
    limit = Fraction(1, base ** bits)
    level = 0
    while value != 0 and abs(value) < limit:
        value *= base ** bits
        level += bits
    return level, value


def unjump(level, mantissa, base=2):
    """The value back from level and mantissa: mantissa / base^level."""
    (mantissa,) = _exact(mantissa)
    return mantissa / Fraction(base) ** level
