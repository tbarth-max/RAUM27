"""The central synchronisation cell: one centre sensor, six on the sphere, eight on the cube.

The arrangement submitted: a centre sensor; six sensors on the sphere of
radius 1/2 -- the face centres of the unit cube around it -- and eight on
the cube's corners. Each measures whatever can be measured
(acceleration, inertia, any field); every quantity is handled the same
way, one scalar per sensor and quantity. What is read out is the delta of
each outer sensor against the centre: 1 x 6 and 1 x 8.

What the cell gives, exactly for rational readings:

- **6- and 8-bit words.** A sensor's bit is set when its delta against the
  centre exceeds a threshold (``bit_words``).
- **The field up to second order, plus the twist.** From the centre and
  the six axis sensors: the value, the gradient (half difference of each
  pair over R) and the three pure curvatures (half sum minus centre over
  R^2). From the eight corners: the three mixed terms xy, yz, zx and the
  twist xyz, by signed sums. Eleven terms in all (``fit``).
- **The corners check the axes.** The gradient read from the corners
  agrees with the one read from the axes exactly when the field has no
  third-order terms of the form x*y^2; their difference is that third
  order, made visible (``gradient_mismatch``). This is the six-measure,
  eight-check rule of ``raum27.verzerrung`` for any field.
- **Reading reality as a stream.** Against a stored baseline (the
  hologram) each new frame yields only the deltas, the two words and the
  change of every fitted term (``stream``).

The 45 degree link: a corner sensor lies at sqrt 3 / 2, an axis sensor at
1/2; the corner direction projects onto each cut plane as that plane's
diagonal (squared lengths 3/4 -> 1/2 -> 1/4), so the cube's eight and the
sphere's six are tied through the plane diagonals.
"""

from fractions import Fraction
from itertools import product

R = Fraction(1, 2)
CENTRE = (0, 0, 0)
AXIS = tuple(tuple(R * s if i == k else 0 for i in range(3)) for k in range(3) for s in (1, -1))
CORNERS = tuple(tuple(R * s for s in signs) for signs in product((1, -1), repeat=3))
SENSORS = (CENTRE,) + AXIS + CORNERS


def _exact(value):
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError("readings must be int or Fraction")
    return Fraction(value)


def _reading(values):
    if set(values) != set(SENSORS):
        raise ValueError("a reading needs exactly the 15 sensors of the cell")
    return {p: _exact(v) for p, v in values.items()}


def sample(field):
    """Read a field ``field(x, y, z)`` at all 15 sensors."""
    return {p: _exact(field(*p)) for p in SENSORS}


def deltas(values):
    """Outer sensors against the centre: (six axis deltas, eight corner deltas)."""
    v = _reading(values)
    c = v[CENTRE]
    return tuple(v[p] - c for p in AXIS), tuple(v[p] - c for p in CORNERS)


def bit_words(values, threshold):
    """6-bit and 8-bit words: bit i set when |delta i| > threshold."""
    threshold = _exact(threshold)
    six, eight = deltas(values)
    word = lambda ds: sum(1 << i for i, d in enumerate(ds) if abs(d) > threshold)
    return word(six), word(eight)


def fit(values):
    """The eleven terms: value, gradient, pure curvatures, mixed terms, twist."""
    v = _reading(values)
    c = v[CENTRE]
    plus = [v[AXIS[2 * k]] for k in range(3)]
    minus = [v[AXIS[2 * k + 1]] for k in range(3)]
    gradient = tuple((p - m) / (2 * R) for p, m in zip(plus, minus))
    curvature = tuple((p + m - 2 * c) / (2 * R * R) for p, m in zip(plus, minus))

    def signed(*axes):
        total = Fraction(0)
        for corner in CORNERS:
            sign = 1
            for a in axes:
                sign *= 1 if corner[a] > 0 else -1
            total += sign * v[corner]
        return total

    mixed = tuple(signed(i, j) / (8 * R * R) for i, j in ((0, 1), (1, 2), (0, 2)))
    twist = signed(0, 1, 2) / (8 * R ** 3)
    return {"value": c, "gradient": gradient, "curvature": curvature, "mixed": mixed, "twist": twist}


def gradient_from_corners(values):
    """Gradient as the eight corners see it."""
    v = _reading(values)
    result = []
    for k in range(3):
        total = sum((1 if corner[k] > 0 else -1) * v[corner] for corner in CORNERS)
        result.append(total / (8 * R))
    return tuple(result)


def gradient_mismatch(values):
    """Corner gradient minus axis gradient; zero unless third-order cross terms are present."""
    axis = fit(values)["gradient"]
    return tuple(c - a for c, a in zip(gradient_from_corners(values), axis))


def stream(baseline, frames, threshold):
    """Per frame: deltas against the baseline, the two words, and the change of every term."""
    base = _reading(baseline)
    base_fit = fit(base)
    out = []
    for frame in frames:
        f = _reading(frame)
        changed = {p: f[p] - base[p] for p in SENSORS if f[p] != base[p]}
        diff = {p: f[p] - base[p] for p in SENSORS}
        now = fit(f)
        terms = {name: (now[name] - base_fit[name]) if name in ("value", "twist")
                 else tuple(a - b for a, b in zip(now[name], base_fit[name]))
                 for name in now}
        out.append({"changed": changed, "words": bit_words(diff, threshold), "terms": terms})
    return out
