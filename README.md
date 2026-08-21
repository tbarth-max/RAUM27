# 🌌 RAUM27

> Question everything.
> Benchmark everything.
> Keep only what survives.

RAUM27 is an open research project exploring prediction, pattern recognition and reproducible benchmarking.

The objective is not to prove a theory.

The objective is to break it.

Every hypothesis must survive objective benchmarks before it becomes part of the framework.

## Research Areas

- **Prediction Benchmarks** — active, see below.
- Pattern Recognition — not started.
- Multi-Agent Systems — not started.
- Information Geometry — not started.
- Reproducible Experiments — not started.

Listed for direction, not as a claim of coverage: per the principle below,
nothing here counts until it has actual benchmarked work behind it.

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

**Real data, not just synthetic:** `data/lotto_6aus49_since_2000.csv`
holds 2724 real German Lotto 6-aus-49 draws, 2000-01-01 through
2026-07-22 (source: [daowa89/lottery-archive](https://github.com/daowa89/lottery-archive),
see `data/README.md`). `load_draws_from_csv` loads it;
`scripts/run_real_data_benchmark.py` runs both `RandomPredictor` and
`FingerprintKNNPredictor` over the full real history and reports the
delta between them — the exact "Zufallsdurchlauf vs. Vorhersagedurchlauf"
comparison this benchmark exists to make. It is a standalone script, not
part of `pytest`, because the k-NN backtest over ~2700 real draws is
O(n²) and takes several minutes; `tests/test_real_data_and_ztest.py`
covers the same loading/statistics logic in milliseconds on a slice of
the real data instead.

Because a full permutation test on that much data would mean re-running
the expensive predictor hundreds of times, real-data significance is
assessed with `z_test_vs_theoretical_baseline` instead: under the null
hypothesis, walk-forward match counts are i.i.d. Hypergeometric(49,6,6)
*regardless of any correlation in the predictor's own picks* (proof in
its docstring), so the Central Limit Theorem gives an exact-in-the-large-sample
significance test without needing to re-run the predictor at all.

**Actual result, run once on the full real history (`k=5`, `seed=1`, no
tuning or cherry-picking — this is the exact specification from the
source notes):**

| | mean matches/draw | vs. theoretical baseline (0.7347) | p-value |
|---|---|---|---|
| `RandomPredictor` | 0.7384 | +0.0037 | 0.40 (not significant) |
| `FingerprintKNNPredictor` | 0.7032 | **−0.0315** | 0.98 for "better than chance" |

**Delta (Vorhersage − Zufall) = −0.0353 matches/draw.** The fingerprint/k-NN
system did not show the requested measurable improvement over random —
on this real dataset its point estimate is slightly *below* random
guessing, not above it (z ≈ −2.17; treated as its own one-sided test for
"significantly worse," that corresponds to p ≈ 0.015, though with no
correction for having looked at this after the fact, so read that as
suggestive rather than conclusive). The one claim this result does
support without qualification: there is no evidence here of the
algorithm doing better than chance, which is the bar this whole exercise
was set up to test.

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