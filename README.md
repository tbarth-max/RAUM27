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
  C = 8/6 = 4/3. Also the cube's diagonals, in exact rational arithmetic:
  the third face direction as the cross product of the other two
  (`ex × ey = ez`), the 8 corner directions collapsing into 4 unique
  space diagonals, and a correction of a claim from the notes — the 4
  diagonals that meet at the cube's center have squared length 3
  (i.e. **√3**), not √2. √2 is real (it's the *face* diagonal, legs 1
  and 1 via Pythagoras), but the face diagonal's midpoint is its own
  face's center, not the cube's center — only the space (body) diagonal,
  corner to opposite corner, passes through the cube's center. Verified
  by comparing exact midpoints and squared lengths, never a float `sqrt`.
- **`ifs_attractor`** — a general Iterated Function System engine (the
  Banach fixed-point theorem applied to contraction maps), instantiated
  as the 6-map cube-face system A = ∪ᵢ f_i(A).
- **`taylor`** — a rational (exact-fraction) truncated Taylor
  approximation of sine.

Run the test suite with `pytest` (56 tests, all mathematical claims in
this README are verified, not asserted).

## Module: `raum27.lotto_benchmark` — Null-Hypothesis Forecast Benchmark

The source notes describe using the fingerprint above to *predict*
lottery-style draws. Whether that has any real signal cannot be argued
away in prose — the project's own principle says to benchmark it, so
this module does exactly that, and reports the result honestly either
way.

**Why a lottery, specifically:** verifying a forecasting method against a
slow, causally-connected system (e.g. a climate model) can take decades
before ground truth is known. A certified lottery draw is the opposite —
fast feedback, and by construction an i.i.d. uniform random process with
zero mutual information between draws. That makes it a useful *null
test*: a method that fabricates false-positive structure out of pure
noise (the standard failure mode of an overfit forecasting pipeline)
should reveal that here, immediately, instead of only decades into a real
forecast.

**What it contains:**

- `match_probability(m)` — the exact hypergeometric baseline. Worth
  stating precisely because it's easy to misremember: P(3 of 6 matches
  in 6-aus-49) ≈ **1.76%**, not 5%. The whole benchmark is only as
  correct as this baseline.
- `RandomPredictor` — the zero-information baseline.
- `FingerprintKNNPredictor` — the fingerprint + k-nearest-neighbours
  forecaster from the source notes, implemented exactly as specified
  (rational Taylor-sine fingerprint, L1 nearest neighbours,
  inverse-distance-weighted vote on the neighbours' successors).
- `backtest` — walk-forward evaluation (predicts draw t from draws
  `[:t]` only, never with lookahead).
- `permutation_test` — shuffles the draw order to build a null
  distribution and reports a p-value for "does this predictor's
  performance exceed what shuffled, structure-free data would produce."

**Result, run on synthetic i.i.d. random draws (`tests/test_lotto_benchmark.py`):**
the fingerprint/k-NN predictor shows **no statistically significant
edge** over the random baseline (p > 0.05). This is not a bug in the
implementation — it is the mathematically expected outcome of applying
any function of history to a process with provably zero mutual
information between past and future draws, and the benchmark's job is to
demonstrate that honestly rather than assume it.

**What this does and does not establish:**

- It shows this specific algorithm does not manufacture a fake edge out
  of pure noise, which is a reasonable prerequisite before trusting it on
  anything else — a sanity check, not proof of general forecasting
  ability.
- It says nothing about causally-connected systems (weather, climate,
  markets with real autocorrelation). Those have physical structure a
  certified lottery deliberately has none of; a result on one does not
  transfer to the other in either direction.
- **This is not a gambling tool.** An apparent "edge" on a small
  historical sample is expected sampling noise unless it survives
  permutation testing *and* replicates on data collected after the
  method was fixed. Do not use this to make wagering decisions.

Claims about physical "resonance," instantaneous coupling, or AI
consciousness from the source notes are still not represented anywhere
in this codebase.

## Module: `raum27.q144` — The 144-State Space and the Φ Operator

The notes describe a "clock-free kernel" built on a 144-state space
(Q₁₄₄) and a cyclic Φ operator. The state-space part of that is ordinary,
checkable combinatorics, and is implemented here:

- 144 states = 12 cube edges × 4 phases (0°/90°/180°/270°) × 3 projection
  planes (XY/XZ/YZ).
- `phi(state)` advances all three coordinates by one step at once.
  Verified in `tests/test_q144.py`: Φ is a permutation of Q₁₄₄, every
  orbit has exactly length 12 (= lcm(12, 4, 3)), and the 144 states
  decompose into exactly 12 disjoint orbits of that length.

## Module: `raum27.clockfree_scheduler` + Milestone 6 — Taktfreier Scheduler, Benchmarked

The notes claim a scheduler that runs processes to completion of their
own workload ("taktfrei") instead of in fixed time slices is simply
better. [`milestones/06_taktfreier_kernel/`](milestones/06_taktfreier_kernel/README.md)
implements that policy for real — `schedule_run_to_completion`, a
non-preemptive FCFS scheduler — and benchmarks it against the standard
time-sliced baseline, `schedule_round_robin`, on the notes' own worked
example (three processes needing 3, 1,000,000,000 and 100 operations).

**Result:** run-to-completion needs far fewer context switches and, when
short jobs happen to be queued first, gives everyone the lowest possible
waiting time. But queue a short job behind a long one — exactly the
notes' own example — and it waits for the long job's *entire* runtime
before running at all: the classical **convoy effect** of non-preemptive
FCFS scheduling, which round-robin bounds by design. Neither policy is
unconditionally better; the notes only show the favorable case. This is
the project's own benchmarking principle applied to the notes' scheduling
claim rather than to a prediction claim.

The notes' interactive console, published apps, arXiv preprint, and
physical hypotheses (fractal densification, "neutral resonance fields,"
crystallization nuclei) are not part of this milestone — they are either
UI around the logic implemented here, or claims that would need their
own benchmarks against physical measurements, not scheduling metrics.

## Module: `raum27.autocorrelation_control` — Positive Control

A null result is only meaningful if the test could have found something.
This module checks that: it runs the *identical* shuffle-based
permutation test from `lotto_benchmark` against an AR(1) process, the
textbook toy model for a system with genuine short-range memory (e.g.
daily temperature anomalies, where today really is informative about
tomorrow).

- With strong real autocorrelation (`phi=0.85`), the test finds a
  significant edge (**p ≈ 0.005**, stable across seeds).
- With no autocorrelation (`phi=0`, i.e. i.i.d. noise — structurally the
  same situation as a lottery draw), the identical test finds **no**
  significant edge (p > 0.05, also stable across seeds).

This is the direct answer to "isn't a lottery drum just physics, the same
as weather?" — yes, both are classical mechanical/fluid systems, but that
alone doesn't make them equally predictable from a sequence of past
outputs. What actually matters is whether that sequence carries
serial correlation, and by how much, relative to how fast the system's
chaos erases it:

- **Weather** has real short-range serial correlation (measured in
  hours to days) *and* is fed by dense, continuous sensor networks
  (satellites, stations) plus physical PDE models — which is why
  forecasts work for roughly two weeks before chaos (the same
  sensitive-dependence-on-initial-conditions effect) erases predictability.
- **A certified lottery drum is engineered to do the opposite**: turbulent
  air jets and ball collisions are specifically designed to erase any
  memory of the ball positions within seconds — regulators certify
  machines on exactly this property. And critically, the forecaster here
  never receives physical sensor data about the machine at all — only the
  final output numbers of past draws, a data stream that decades of
  statistical certification testing on real lotteries has never found
  serial structure in.

"It's all physics" is true of both and settles nothing; what settles it
is whether the specific data stream you hand the model has measurable
memory in it. This module demonstrates, with the same code, that the
methodology correctly says yes to one and no to the other.