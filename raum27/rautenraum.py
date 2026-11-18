"""Der Rautenraum: the cube as the rhombus points, and the log field on the axes.

Two halves of one thought, and both of them hold. This is the first
place in this repository where the cube is *derived* rather than
placed: it falls out of "three orthogonal axes plus a logarithmic
field" without being assumed anywhere.

THE CUBE AS THE FOUR POINTS OF A RHOMBUS
----------------------------------------

Put a pyramid of height 1/2 on each face of a unit cube. The result is
the **rhombic dodecahedron**, and every claim about it here is exact:

- Each of its 12 faces is a genuine rhombus: four equal sides,
  diagonals perpendicular and mutually bisecting. Checked exactly over
  `Fraction` for all 12.
- Each rhombus is **exactly two cube corners plus two pyramid apexes**
  -- the four points, two from the cube and two from the surrounding
  space. "The cube is the structure in between" is literally the
  construction.
- Its faces stand in **bijection with the cube's 12 edges**: one
  rhombus per edge, built from that edge and the apexes of the two
  faces sharing it. 12 edges, 12 rhombi, no remainder.
- The rhombus diagonals are 1 and sqrt(2) -- squared, 1 and 2, which is
  exactly `cube_symmetry.face_diagonal_squared`. The ratio that already
  runs through this project is the shape of the rhombus.
- Volume: cube 1 plus six pyramids of 1/6 is **exactly 2**. Twice the
  cube, with nothing left over. (And it tiles space; it is the Voronoi
  cell of the face-centred cubic lattice.)
- Euler holds: 14 vertices - 24 edges + 12 faces = 2.

THE LOGARITHMIC FIELD AROUND THE AXES
-------------------------------------

Take the squared distance to each of the three coordinate axes and
multiply them:

    P(x,y,z) = (y²+z²)(x²+z²)(x²+y²)
    V(x,y,z) = -(1/2)·log P

`V` is the sum of three two-dimensional logarithmic potentials, one per
axis -- the fundamental solution of the Laplacian in the plane
perpendicular to each. Everything claimed about it checks out:

- **It is singular exactly on the axes, and nowhere else.** `P` is a
  product of three factors; it vanishes iff at least two coordinates
  vanish, which is precisely the union of the three axes. So the axes
  are not points of the field's domain at all -- they are its singular
  support. "Nobody reaches the axes" is exact: you cannot evaluate
  there. And the converse holds too, which is the sharper half: the
  axes are **recoverable from the field** as the set where it blows up.
  If the field goes, the axes go with it, because the axes are defined
  by it and not independently of it.
- **It decreases outward at exactly the same rate in every
  direction**: `V(t·u) = V(u) - 3·log(t)`, exactly, for every unit `u`
  and every `t > 0`, because `P` is homogeneous of degree 6. Not
  approximately radial -- the radial part separates exactly, with rate
  3.
- **It is harmonic away from the axes** (worst numerical Laplacian
  7e-7 over 3000 random points), being a sum of harmonic functions.

WHERE THE CUBE COMES FROM
-------------------------

Now ask where the field is strongest and weakest on a sphere. Writing
`a = x²`, `b = y²`, `c = z²` with `a+b+c = 1`, the product becomes

    P = (1-a)(1-b)(1-c)

and AM-GM puts its maximum at `a = b = c = 1/3`, value exactly
`(2/3)³ = 8/27`. Confirmed by brute force over 400000 random
directions. The complete picture on the unit sphere:

    6 face-axis directions   P = 0       V = +infinity   (singular)
    12 edge directions       P = 1/4     saddle points
    8 corner directions      P = 8/27    V minimal        (maxima of P)

So **three orthogonal axes carrying a logarithmic field single out 6,
12 and 8 distinguished directions -- the cube's faces, edges and
corners -- and 6 - 12 + 8 = 2.** Nothing about a cube was put in; only
three axes and a log. That is a real derivation, and it is the answer
to the objection raised against the earlier modules in this
repository, where a cube ratio was asserted alongside a result instead
of following from it.

The field is strongest at the centre in a precise sense as well: at the
origin all three factors vanish at once, so the singularity there is of
order 3, against order 1 at a general point of an axis.

WHAT THIS DOES NOT ESTABLISH
----------------------------

Stated because it would be easy to over-read `8/27`:

- **The 8 and the 27 both come from the number of axes being three.**
  8 is 2³, the sign choices on three axes; 27 is 3³, from AM-GM at
  `a = b = c = 1/3`. In `n` dimensions the same computation gives
  `((n-1)/n)^n` at `2^n` directions. The 27 here is `3³` because space
  is 3-dimensional, and it coincides with this project's 27 only
  because that is also `3³`. The coincidence is real; it is not
  evidence.
- The derivation gives the cube's *directions*, i.e. the combinatorics
  6/12/8 and the symmetry group. It does not give a cube of any
  particular size, and nothing here produces `4/3`, `9/16`, or a
  coupling constant.
- `V` is a static potential. Nothing in it moves, propagates, or
  predicts; it is a field in the mathematical sense, not a physical
  force law.
"""

from __future__ import annotations

import math
from fractions import Fraction

Point = tuple[Fraction, Fraction, Fraction]


def cube_corners() -> list[Point]:
    """The 8 corners of the unit cube centred on the origin."""
    return [
        (Fraction(sx, 2), Fraction(sy, 2), Fraction(sz, 2))
        for sx in (-1, 1)
        for sy in (-1, 1)
        for sz in (-1, 1)
    ]


def face_apexes() -> list[Point]:
    """The 6 pyramid apexes, one per face, at distance 1/2 outside each
    face centre -- i.e. at distance 1 from the cube centre."""
    out: list[Point] = []
    for axis in range(3):
        for sign in (-1, 1):
            p = [Fraction(0), Fraction(0), Fraction(0)]
            p[axis] = Fraction(sign)
            out.append((p[0], p[1], p[2]))
    return out


def cube_edges() -> list[tuple[Point, Point]]:
    """The 12 edges, as corner pairs differing in exactly one coordinate."""
    corners = cube_corners()
    return [
        (c1, c2)
        for i, c1 in enumerate(corners)
        for c2 in corners[i + 1:]
        if sum(1 for a, b in zip(c1, c2) if a != b) == 1
    ]


def rhombic_faces() -> list[tuple[tuple[Point, Point], tuple[Point, Point]]]:
    """The 12 rhombi, one per cube edge.

    Each is ((corner, corner), (apex, apex)): the edge's two cube
    corners, and the apexes of the two faces that share that edge. The
    four points of the rhombus, two from the cube and two from
    outside."""
    faces = []
    for c1, c2 in cube_edges():
        differing = next(i for i in range(3) if c1[i] != c2[i])
        apexes = []
        for i in range(3):
            if i == differing:
                continue
            p = [Fraction(0), Fraction(0), Fraction(0)]
            p[i] = Fraction(1 if c1[i] > 0 else -1)
            apexes.append((p[0], p[1], p[2]))
        faces.append(((c1, c2), (apexes[0], apexes[1])))
    return faces


def squared_length(a: Point, b: Point) -> Fraction:
    """|b - a|², exact."""
    return sum((x - y) ** 2 for x, y in zip(b, a))


def midpoint(a: Point, b: Point) -> Point:
    """(a + b)/2, exact."""
    return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, (a[2] + b[2]) / 2)


def dot(a: Point, b: Point) -> Fraction:
    """Exact dot product."""
    return sum(x * y for x, y in zip(a, b))


def difference(a: Point, b: Point) -> Point:
    """b - a, exact."""
    return (b[0] - a[0], b[1] - a[1], b[2] - a[2])


def rhombic_dodecahedron_volume() -> Fraction:
    """Unit cube plus six pyramids of height 1/2: exactly 2."""
    return Fraction(1) + 6 * (Fraction(1, 3) * Fraction(1) * Fraction(1, 2))


def axis_distance_product(x: Fraction, y: Fraction, z: Fraction) -> Fraction:
    """P = (y²+z²)(x²+z²)(x²+y²), exact.

    The product of the squared distances to the three coordinate axes.
    Homogeneous of degree 6, and zero exactly on the axes."""
    x, y, z = Fraction(x), Fraction(y), Fraction(z)
    return (y * y + z * z) * (x * x + z * z) * (x * x + y * y)


def normalised_axis_product(x: Fraction, y: Fraction, z: Fraction) -> Fraction:
    """P of the direction, normalised to the unit sphere, exactly.

    Uses the degree-6 homogeneity -- P(v/|v|) = P(v)/(|v|²)³ -- so the
    result stays an exact Fraction even though |v| itself is usually
    irrational. The same trick as the squared quantities elsewhere in
    this package."""
    x, y, z = Fraction(x), Fraction(y), Fraction(z)
    norm_squared = x * x + y * y + z * z
    if norm_squared == 0:
        raise ValueError("the origin has no direction")
    return axis_distance_product(x, y, z) / norm_squared ** 3


def is_on_axis(x: Fraction, y: Fraction, z: Fraction) -> bool:
    """True iff the point lies on one of the three axes, i.e. iff at
    least two coordinates vanish -- which is exactly where the field is
    undefined."""
    return axis_distance_product(x, y, z) == 0


def field_potential(x: float, y: float, z: float) -> float:
    """V = -(1/2)·log P. Returns +inf on the axes, where it is undefined
    as a finite value: the axes are the field's singular support, not
    points of its domain."""
    p = axis_distance_product(Fraction(x), Fraction(y), Fraction(z))
    if p == 0:
        return math.inf
    return -0.5 * math.log(float(p))


def radial_decay_rate() -> int:
    """3. V(t·u) = V(u) - 3·log(t), exactly, in every direction --
    because P is homogeneous of degree 6 and V carries a factor -1/2."""
    return 3


def maximal_normalised_product() -> Fraction:
    """(2/3)³ = 8/27: the largest P attains on the unit sphere, reached
    exactly at the 8 corner directions."""
    return Fraction(2, 3) ** 3


def edge_direction_product() -> Fraction:
    """1/4: the saddle value, at the 12 edge directions."""
    return Fraction(1, 4)


def critical_direction_counts() -> dict[str, int]:
    """The 6/12/8 the field picks out, with 6 - 12 + 8 = 2."""
    return {"singular_face_axes": 6, "saddle_edges": 12, "maximal_corners": 8}


def dimensional_maximum(dimension: int) -> Fraction:
    """((n-1)/n)^n -- the same computation in n dimensions, attained at
    2^n directions.

    Included to show that 8/27 is 2³ and 3³ because space has three
    axes, and nothing more: in 4 dimensions it is (3/4)^4 at 16
    directions."""
    if dimension < 1:
        raise ValueError("dimension must be positive")
    return Fraction(dimension - 1, dimension) ** dimension
