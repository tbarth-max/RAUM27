"""The measuring net: spider web, sensor shells, the 90-degree finder, light and limits.

Kept from conversation so nothing is lost; every statement has a test.

**Spider web.** A web of 8 spokes and 3 rings is modelled as springs
(stiffness 1/length) with a light anchoring to the frame.

- A single sensor at the hub only tells which ring was touched, never
  which spoke; and it is **exactly blind to a torn ring**: a force at the
  hub excites only the symmetric motion, in which every ring thread stays
  unstretched, so by reciprocity no ring property reaches the hub reading
  (``hub_response``).
- Strain gauges on the spokes at the hub, read against a reference that
  takes out the common part, locate every touch point. With every thread
  cut into four pieces (168 touch points, also between knots), four
  threads -- left, top, right, bottom -- separate all 168. Arrival-time
  differences alone separate only 16: the information is in the **ratio
  of forces**, not in the timing (``triangulation``).

**Sensor shells.** With one scalar reading per sensor, the 6 axis points
alone resolve 6 of the 9 field terms up to second order, the 8 corners 7,
**both together all 9**; of the 16 terms up to third order they resolve
13 (``resolved_terms``).

**Finding 90 degrees without measuring an angle.** With poles at +1 and
-1 on an axis, |P - N|^2 - |P - S|^2 = -4 z exactly, so equal pole
distances mean the equator plane (``height_from_poles``). In time, two
equal oscillations with phase gap phi have summed energy
1 - cos(phi) cos(2x + phi): it stands still exactly at 90 degrees, and its
swing 2 |cos phi| measures the distance from 90 (``energy_swing``).

**Light.** f * lambda = c: at 300 MHz light has a wavelength of 1 m.
Two wavelengths beat with the synthetic wavelength l1 l2 / |l1 - l2|;
red 650, green 532 and blue 450 nm repeat together only after their lcm,
1 556 100 nm (``synthetic_wavelength``). A fibre Bragg grating shifts its
colour by about 0.78 * strain (``bragg_shift``).

**Limits.** A logarithmic scale over 100 decades with 14 bits has steps of
1.4 per cent (``log_step``). Erasing one bit costs at least k T ln 2,
about 2.9e-21 J at 300 K; a reversible step has no such floor
(``landauer``). A radius from three neighbouring noisy points gets
**worse** as the points get closer, roughly as noise / spacing^2
(``radius_error``).
"""

import math
import random
from fractions import Fraction
from itertools import product

import numpy as np

SPOKES, RINGS = 8, 3
BOLTZMANN = 1.380649e-23


def _web(cut=(), pieces=1):
    """Stiffness matrix and node index of the web; ``cut`` removes ring segments (ring, spoke)."""
    edges = []
    for s in range(SPOKES):
        edges.append((("C",), ("N", 1, s), 1.0))
        for r in range(1, RINGS):
            edges.append((("N", r, s), ("N", r + 1, s), 1.0))
        for r in range(1, RINGS + 1):
            if (r, s) not in cut:
                edges.append((("N", r, s), ("N", r, (s + 1) % SPOKES), r * math.pi / 4))
    springs = []
    for a, b, length in edges:
        chain = [a] + [("M", a, b, i) for i in range(1, pieces)] + [b]
        springs += [(u, v, length / pieces) for u, v in zip(chain, chain[1:])]
    nodes = sorted({n for u, v, _ in springs for n in (u, v)}, key=str)
    index = {n: i for i, n in enumerate(nodes)}
    K = np.eye(len(nodes)) * 0.05
    for u, v, length in springs:
        i, j, k = index[u], index[v], 1.0 / length
        K[i, i] += k
        K[j, j] += k
        K[i, j] -= k
        K[j, i] -= k
    return K, index, springs


def hub_response(cut=(), omega=0.37):
    """Response at the hub to a unit touch at each knot, for one driving frequency."""
    K, index, _ = _web(cut)
    G = np.linalg.inv(K - omega ** 2 * np.eye(len(K)))
    hub = index[("C",)]
    return {n: G[hub, i] for n, i in index.items() if n != ("C",)}


def triangulation(spokes, pieces=4):
    """Gauge signatures of every touch point and how many are told apart.

    Returns (touch points, distinguishable points, smallest signature
    distance, largest signal).
    """
    K, index, _ = _web(pieces=pieces)
    G = np.linalg.inv(K)
    hub = index[("C",)]
    gauge = [index[("M", ("C",), ("N", 1, s), 1)] for s in spokes]
    touch = [n for n in index if n != ("C",)]
    sigs = np.array([[G[g, index[n]] - G[hub, index[n]] for g in gauge] for n in touch])
    keys = {}
    for n, row in zip(touch, sigs):
        keys.setdefault(tuple(np.round(row, 9)), []).append(n)
    distinct = sum(1 for v in keys.values() if len(v) == 1)
    d = np.linalg.norm(sigs[:, None] - sigs[None], axis=2)
    np.fill_diagonal(d, np.inf)
    return len(touch), distinct, float(d.min()), float(np.abs(sigs).max())


def arrival_time_classes(spokes, pieces=4):
    """How many touch points are told apart by arrival-time differences alone."""
    import heapq
    _, index, springs = _web(pieces=pieces)
    adjacency = {}
    for u, v, length in springs:
        if ("C",) in (u, v):
            continue
        adjacency.setdefault(u, []).append((v, length))
        adjacency.setdefault(v, []).append((u, length))
    keys = {}
    for source in adjacency:
        dist, queue, tick = {source: 0.0}, [(0.0, 0, source)], 1
        while queue:
            t, _, u = heapq.heappop(queue)
            if t > dist[u]:
                continue
            for v, w in adjacency[u]:
                if t + w < dist.get(v, math.inf) - 1e-12:
                    dist[v] = t + w
                    heapq.heappush(queue, (t + w, tick, v))
                    tick += 1
        times = [dist[("N", 1, s)] for s in spokes]
        first = min(times)
        keys.setdefault(tuple(round(t - first, 9) for t in times), []).append(source)
    return len(adjacency), sum(1 for v in keys.values() if len(v) == 1)


def _harmonics(x, y, z):
    return [1, x, y, z, x * y, y * z, z * x, x * x - y * y, 2 * z * z - x * x - y * y,
            x * (x * x - 3 * y * y), y * (3 * x * x - y * y), z * (x * x - y * y), x * y * z,
            x * (4 * z * z - x * x - y * y), y * (4 * z * z - x * x - y * y),
            z * (2 * z * z - 3 * x * x - 3 * y * y)]


def resolved_terms(points, degree):
    """How many harmonic field terms up to ``degree`` the sensor ``points`` can tell apart."""
    n = {1: 4, 2: 9, 3: 16}[degree]
    rows = [[Fraction(v) for v in _harmonics(*p)[:n]] for p in points]
    rank = 0
    for col in range(n):
        pivot = next((i for i in range(rank, len(rows)) if rows[i][col]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for i in range(len(rows)):
            if i != rank and rows[i][col]:
                f = rows[i][col] / rows[rank][col]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[rank])]
        rank += 1
    return rank


AXIS_SENSORS = tuple(v for v in product((-1, 0, 1), repeat=3) if sum(map(abs, v)) == 1)
CORNER_SENSORS = tuple(product((-1, 1), repeat=3))


def height_from_poles(point):
    """Height above the equator from the two pole distances: z = -(dN^2 - dS^2) / 4."""
    p = [Fraction(c) for c in point]
    north = sum((a - b) ** 2 for a, b in zip(p, (0, 0, 1)))
    south = sum((a - b) ** 2 for a, b in zip(p, (0, 0, -1)))
    return -(north - south) / 4


def energy_swing(phase_gap):
    """Peak-to-peak swing of sin^2(x) + sin^2(x + phase_gap): 2 |cos phase_gap|."""
    return 2 * abs(math.cos(phase_gap))


def synthetic_wavelength(l1, l2):
    """Beat wavelength of two wavelengths, exact for rational inputs."""
    l1, l2 = Fraction(l1), Fraction(l2)
    if l1 == l2:
        raise ValueError("equal wavelengths do not beat")
    return l1 * l2 / abs(l1 - l2)


def bragg_shift(wavelength, strain, photoelastic=Fraction(22, 100)):
    """Colour shift of a fibre Bragg grating: wavelength * (1 - p_e) * strain."""
    return Fraction(wavelength) * (1 - photoelastic) * Fraction(strain)


def log_step(bits, decades):
    """Factor between neighbouring steps of a logarithmic scale."""
    return 10 ** (decades / 2 ** bits)


def landauer(temperature):
    """Least energy to erase one bit, in joules."""
    return BOLTZMANN * temperature * math.log(2)


def radius_error(spacing, noise, trials=2000, seed=1):
    """Median error of the radius of a unit circle from three noisy neighbouring points."""
    rng = random.Random(seed)
    errors = []
    for _ in range(trials):
        t = rng.uniform(0, 2 * math.pi)
        p = [(math.cos(t + k * spacing) + rng.gauss(0, noise),
              math.sin(t + k * spacing) + rng.gauss(0, noise)) for k in (-1, 0, 1)]
        a, b, c = math.dist(p[1], p[2]), math.dist(p[0], p[2]), math.dist(p[0], p[1])
        area = abs((p[1][0] - p[0][0]) * (p[2][1] - p[0][1]) - (p[1][1] - p[0][1]) * (p[2][0] - p[0][0])) / 2
        errors.append(abs(a * b * c / (4 * area) - 1) if area else math.inf)
    errors.sort()
    return errors[len(errors) // 2]
