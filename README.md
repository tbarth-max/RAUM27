# 🌌 RAUM27

> Question everything.
> Benchmark everything.
> Keep only what survives.

RAUM27 is an open research project exploring prediction, pattern recognition and reproducible benchmarking.

The objective is not to prove a theory.

The objective is to break it.

Every hypothesis must survive objective benchmarks before it becomes part of the framework.

## Research Areas

- Prediction Benchmarks
- Pattern Recognition
- Multi-Agent Systems
- Information Geometry
- Reproducible Experiments

## Research Principle

If a new idea does not outperform the baseline,

it does not stay.

## Module: `raum27` — Rational-Space Geometry & Fractal Attractors

This package implements the parts of the project's source notes that are
ordinary, checkable mathematics:

- **`rational_space`** — the multiplicative group of positive rationals
  Q+, with the involution I(x) = 1/x and its fixed point at X = 1.
- **`scale_hierarchy`** — the 3-adic/9-adic scale ladder
  L_k = 3^k, A_k = 9^k, V_k = 27^k, and the digital-root invariance of
  powers of 9.
- **`cube_symmetry`** — the 6 face directions and 8 corner directions of
  a cube, their vector equilibrium, and the coupling constant
  C = 8/6 = 4/3.
- **`ifs_attractor`** — a general Iterated Function System engine (the
  Banach fixed-point theorem applied to contraction maps), instantiated
  as the 6-map cube-face system A = ∪ᵢ f_i(A).
- **`taylor`** — a rational (exact-fraction) truncated Taylor
  approximation of sine.

Run the test suite with `pytest` (47 tests, all mathematical claims above
are verified, not asserted).

### What this deliberately excludes

The source notes also describe using this geometry to *predict* random
draws (lottery-style numbers), and frame the system in terms of
"resonance," "holography," and AI "consciousness." Those claims are out
of scope here:

- Predicting independent random draws from their geometric encoding
  cannot outperform chance, by definition of statistical independence —
  no amount of feature engineering changes that. Per this project's own
  principle above, that idea does not stay unless it is benchmarked and
  shown to beat a random baseline; it hasn't been, and it won't be.
- Claims about physical "resonance," instantaneous coupling, or AI
  consciousness are not represented in this codebase.