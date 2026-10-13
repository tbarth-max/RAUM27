"""The automation cascade: take out what is known, mirror, compare, hand over only the rest.

The procedure submitted: let the data stream run through; take out every
sample that fits something already known -- a proportion, an inverse
proportion, a ratio built from the known circles; run the same stream a
second time mirrored (inverted); compare the two at the end of the
cascade. What is left is a small delta, and only that goes to the folder
for manual work.

A sample is a pair (x, y) of exact numbers. The known patterns:

- **proportional** with a known factor k: y = k x;
- **inverse proportional** with a known factor k: y = k / x;
- **a ratio of the known circles**: y / x reduces to p/q with every prime
  of p and q among the allowed ones (default 2 and 3 -- the chains RAUM27
  is built from; a 5 or a 7 is a wall into another space).

Mirroring maps (x, y) to (1/x, 1/y). It keeps each pattern and inverts
its factor: y = k x becomes 1/y = (1/k)(1/x), y = k/x becomes
1/y = (1/k)/(1/x). A sample is **confirmed** only if it is explained in
the original stream and its mirror is explained by exactly the mirrored
pattern. Explained on one side only is suspicious; a point whose
original and mirror name different patterns lies on two curves at once
and is ambiguous; explained on neither side is new. All of these go to
the manual folder with their reason -- nothing is guessed, as in
``raum27.abtastung``. Zero cannot be mirrored and is always handed over.
"""

from fractions import Fraction

MIRRORS = ("inversion", "diagonal", "both", "axis")
"""inversion: (x, y) -> (1/x, 1/y); diagonal: the 45-degree mirror (x, y) -> (y, x);
both: diagonal after inversion, (x, y) -> (1/y, 1/x); axis: the 90-degree mirror (x, y) -> (-x, y)."""


def _exact(v):
    if isinstance(v, bool) or not isinstance(v, (int, Fraction)):
        raise TypeError("samples must be int or Fraction")
    return Fraction(v)


def _primes(n):
    n, out, p = abs(n), set(), 2
    while p * p <= n:
        while n % p == 0:
            out.add(p)
            n //= p
        p += 1
    if n > 1:
        out.add(n)
    return out


def known_circle_ratio(x, y, allowed=(2, 3)):
    """y / x as p/q if all primes of p and q are allowed, else None."""
    if x == 0 or y == 0:
        return None
    r = Fraction(y) / Fraction(x)
    if _primes(r.numerator) | _primes(r.denominator) <= set(allowed):
        return r
    return None


def explain(x, y, factors, allowed=(2, 3)):
    """Which known pattern explains (x, y): ('prop', k), ('inv', k), ('circle', r) or None."""
    for k in factors:
        if y == k * x:
            return ("prop", k)
    for k in factors:
        if x != 0 and y == k / x:
            return ("inv", k)
    r = known_circle_ratio(x, y, allowed)
    if r is not None:
        return ("circle", r)
    return None


def mirror(sample, mode="inversion"):
    """The sample seen in one of the mirrors (see ``MIRRORS``)."""
    x, y = sample
    if mode == "inversion":
        return 1 / x, 1 / y
    if mode == "diagonal":
        return y, x
    if mode == "both":
        return 1 / y, 1 / x
    if mode == "axis":
        return -x, y
    raise ValueError(f"unknown mirror {mode!r}")


def mirrored_pattern(pattern, mode="inversion"):
    """What a pattern becomes in a mirror.

    =========  =========================  =========================
    mirror     y = k x  becomes            y = k / x  becomes
    =========  =========================  =========================
    inversion  y = (1/k) x                 y = (1/k) / x
    diagonal   y = (1/k) x                 y = k / x   (unchanged)
    both       y = k x   (unchanged)       y = (1/k) / x
    axis       y = -k x                    y = -k / x
    =========  =========================  =========================

    The 45-degree mirror keeps inverse proportion and inverts the
    proportional factor; doing it after the inversion turns that back.
    """
    kind, k = pattern
    if kind == "circle":
        return ("circle", {"inversion": 1 / k, "diagonal": 1 / k, "both": k, "axis": -k}[mode])
    if mode == "inversion":
        return (kind, 1 / k)
    if mode == "diagonal":
        return (kind, 1 / k) if kind == "prop" else (kind, k)
    if mode == "both":
        return (kind, k) if kind == "prop" else (kind, 1 / k)
    if mode == "axis":
        return (kind, -k)
    raise ValueError(f"unknown mirror {mode!r}")


def _mirror_of(pattern):
    return mirrored_pattern(pattern, "inversion")


def newton_image(object_distance, focal_length):
    """Newton's lens law x * x' = f^2: the focal point as an inversion of radius f.

    Distances are measured from the front and back focal points. Returns
    the image distance x' and the magnification -f/x: the image is upside
    down -- one inversion. Two lenses in a row turn it upright again.
    """
    x, f = _exact(object_distance), _exact(focal_length)
    if x == 0:
        raise ValueError("an object in the focal point has its image at infinity")
    return f * f / x, -f / x


def cascade(samples, factors, allowed=(2, 3)):
    """Run the stream and its mirror; return (confirmed, manual).

    ``confirmed`` holds (sample, pattern); ``manual`` holds (sample, reason).
    """
    factors = [_exact(k) for k in factors]
    mirrored_factors = factors + [1 / k for k in factors if k != 0]
    confirmed, manual = [], []
    for x, y in samples:
        x, y = _exact(x), _exact(y)
        if x == 0 or y == 0:
            manual.append(((x, y), "zero cannot be mirrored"))
            continue
        here = explain(x, y, factors, allowed)
        there = explain(1 / x, 1 / y, mirrored_factors, allowed)
        if here is None and there is None:
            manual.append(((x, y), "new: fits no known pattern"))
        elif here is None or there is None:
            manual.append(((x, y), "explained on one side only"))
        elif here[0] == "circle" or there == _mirror_of(here):
            confirmed.append(((x, y), here))
        else:
            manual.append(((x, y), "ambiguous: original and mirror name different patterns"))
    return confirmed, manual


def manual_share(samples, factors, allowed=(2, 3)):
    """Share of the stream that still needs a hand."""
    confirmed, manual = cascade(samples, factors, allowed)
    total = len(confirmed) + len(manual)
    if total == 0:
        raise ValueError("an empty stream has no share")
    return Fraction(len(manual), total)
