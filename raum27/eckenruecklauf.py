"""The corner as the unreachable ten: a sphere grows into the cube but never into its corner.

Cube edge a = 9 around the centre: the touching spheres have radius^2
a^2/4, a^2/2, 3a^2/4 (faces, edges, corners) -- 81/4, 81/2, 243/4. The
inner one, radius a/2 = 9/2, is the proportionality factor of the first
cube; the corner, the 10, lies on the outer one.

* **From sphere to cube without a corner.** The p-ball
  |x|^p + |y|^p + |z|^p = r^p touches every face at r for every p, and
  reaches along a space diagonal to r * 3^(1/2 - 1/p): r at p = 2 (the
  sphere), r * sqrt 3 only for p -> infinity (the cube). For every finite
  p the corner is rounded, its radius never 0 -- no 90 degrees, no
  infinite curvature (a sharp corner is where a real structure cracks).
* **Approaching without arriving.** What is left of the way after n
  pushes, each taking the fraction 1 - q of the rest, is gap * q^n: never
  0, and the pushes together never exceed the gap.
* **The return comes out of the corner.** Three mirrors at right angles
  turn every direction v into -v -- the corner reflector (the laser
  reflectors on the Moon). On the grid that is the opposite pole
  d -> 10 - d. What is sent towards a corner comes straight back.
"""

from fractions import Fraction

from raum27.nennerordnung import Power


def _exact(*values):
    for v in values:
        if isinstance(v, float):
            raise TypeError("exact module: use int or Fraction, not float")
    return [Fraction(v) for v in values]


def touching_radii_squared(edge=9):
    """(faces, edges, corners) radius^2 for a cube of the given edge: a^2/4, a^2/2, 3a^2/4."""
    (a,) = _exact(edge)
    return a * a / 4, a * a / 2, 3 * a * a / 4


def diagonal_reach(r, p):
    """How far the p-ball of radius r reaches along a space diagonal, as an exact power form."""
    r, p = _exact(r, p)
    if r <= 0 or p < 1:
        raise ValueError("r > 0 and p >= 1")
    return Power.of(r) * Power.of(3) ** (Fraction(1, 2) - 1 / p)


def reaches_corner(p):
    """Only the cube itself (p infinite, passed as None) has a sharp corner."""
    return p is None


def corner_radius(radius):
    """A corner radius for the structure; 0 (a sharp 90 degree corner) is refused."""
    (radius,) = _exact(radius)
    if radius <= 0:
        raise ValueError("radius 0 is a sharp corner: not allowed in the structure")
    return radius


def remaining_gaps(gap, q, steps):
    """What is left of the way after each push: gap * q^n, never 0 for 0 < q < 1."""
    gap, q = _exact(gap, q)
    if not 0 < q < 1 or gap <= 0:
        raise ValueError("0 < q < 1 and a positive gap")
    return [gap * q ** n for n in range(steps + 1)]


def corner_reflect(v):
    """Reflect on the three faces of a corner, one after the other: v -> -v."""
    v = list(_exact(*v))
    for axis in range(3):
        v[axis] = -v[axis]
    return tuple(v)


def opposite_digit_node(node):
    """The same on the 1..9 grid: each digit d -> 10 - d."""
    return "".join(str(10 - int(d)) for d in node)


# --- turning about a space diagonal ---------------------------------------------
#
# A spiral turning about the space diagonal (1, 1, 1) meets the six face
# directions (up, down, left, right, front, back) every 60 degrees: seen
# along the diagonal they form a regular hexagon. The cube symmetries that
# keep this axis in place are exactly the 6 permutations of the three
# coordinate axes -- the 6 orders of XY, XZ, XT. Each face centre stays at
# 9/2 from the centre: (9/2)^2 = 81/4 = 27/4 along the axis + 27/2 across.

DIAGONAL = (1, 1, 1)


def axis_keepers(axis=DIAGONAL):
    """Signed axis permutations g with g(axis) = axis."""
    from raum27.fundamentalbereich import act, cube_group
    return [g for g in cube_group() if act(g, axis) == tuple(axis)]


def split_along_axis(point, axis=DIAGONAL):
    """(squared part along the axis, squared part across it) of a point, exactly."""
    point = _exact(*point)
    axis = _exact(*axis)
    dot = sum(p * a for p, a in zip(point, axis))
    along2 = dot * dot / sum(a * a for a in axis)
    return along2, sum(p * p for p in point) - along2
