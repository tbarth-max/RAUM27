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
  Also: the cube decomposes into 6 congruent pyramids (one per face,
  apex at the cube's center) — verified two independent ways, geometry
  (apex-to-corner distance matches half the space diagonal exactly) and
  volume (`6 * pyramid_volume(edge) == cube_volume(edge)`, exact
  rational arithmetic for every edge length). One more relationship,
  submitted separately and checked against this module's own
  `coupling_constant` rather than against newly-asserted numbers:
  **squaring** the coupling constant gives `(4/3)² = 16/9` exactly (its
  reciprocal squared gives `9/16`) — both already traceable to the one
  corners/faces ratio, not to two independently-asserted "base values."
  **Cubing** it does not give `16/9` — `(4/3)³ = 64/27` — worth pinning
  down explicitly because an earlier claim in this project's history
  asserted the cube equals `16/9` and was wrong; only the square holds.
- **`ifs_attractor`** — a general Iterated Function System engine (the
  Banach fixed-point theorem applied to contraction maps), instantiated
  as the 6-map cube-face system A = ∪ᵢ f_i(A).
- **`taylor`** — a rational (exact-fraction) truncated Taylor
  approximation of sine.

Run the test suite with `pytest` (277 tests as of this module set, all
mathematical claims in this README are verified, not asserted).

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

**Two easily-conflated recurrence questions, kept separately checkable**
(`n_draw_states`, `expected_specific_state_recurrence_years`,
`expected_any_repeat_years`): "when does a specific draw repeat" and
"when does any collision happen among draws made so far" sound like the
same question but differ by a factor of roughly `sqrt(n_states)`, not a
rounding error. For German 6-aus-49 at one draw a week:
`expected_specific_state_recurrence_years` ≈ **268,920 years** (specific
state), `expected_any_repeat_years` ≈ **90 years** (birthday-paradox
asymptotics, `1.25·√n_states` draws to first collision) — about a
**3000x** difference, verified as a ratio rather than as two isolated
numbers so the relationship stays checkable if either formula changes.
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

## Module: `raum27.rubik_state` — Solved-State Check, Factored by Axis

A small, concrete idea that came up while discussing the cube's geometry:
check whether a Rubik's cube is solved by factoring the check along the
cube's 3 axes, reusing the same 6 `face_directions()` from
`cube_symmetry`. A face is "uniform" if every one of its stickers shares
one color; the cube is solved iff all 6 faces are uniform. Grouping that
into the 3 opposite-face axis pairs (each pair one AND-condition) gives 3
independent checks whose combined AND is the overall solved state —
not a new operation, just the single global "all faces uniform" check
factored along the axes already used elsewhere in this package.

Verified with real pass/fail cases, not just the solved state: a single
wrong sticker on one face makes exactly that face's axis-check fail while
the other two still pass, and a cube with only one of three axes solved
correctly reports as unsolved overall while identifying which axis is
still open. See `tests/test_rubik_state.py`.

## Module: `raum27.phase_sync` — Phase Synchronization Between Two Signals

A phase detector: two "pointers" sweep a circle at frequencies f1, f2
(`theta(t) = 2*pi*f*t`), and are "synchronized" when their phase angles
coincide within a tolerance. This is a standard, well-known concept (a
phase-locked loop's phase detector; two near-identical tones producing an
audible "beat"), formalized and verified here rather than left as prose:

- Equal frequency, equal phase → always synchronized.
- Equal frequency, offset phase → never synchronized (frequency alone
  doesn't create periodic coincidences).
- Different frequencies → synchronization recurs periodically at the
  **beat period** `1 / |f1 - f2|`. Verified by simulating two signals at
  5.0 Hz and 5.3 Hz and measuring the actual time between synchronization
  events: the measured interval matches the theoretical beat period
  (1/0.3 s ≈ 3.333 s) to within 1%.

See `tests/test_phase_sync.py`.

## Module: `raum27.octahedron` — The Cube's Dual Polyhedron

Put a vertex at each of the cube's 6 face centers (`cube_symmetry`'s
`face_directions`) and a face at each of its 8 corners
(`corner_directions`) and you get the octahedron: vertex and face counts
trade places exactly, `(8,6) -> (6,8)`, edge count stays 12. Verified via
Euler's formula (`V - E + F = 2`) and by checking each of the 8 candidate
faces really is a face of the convex hull (all other vertices strictly on
one side of its plane).

A question that came up while discussing this: does dualizing *again*
(cube → octahedron → cube, using face centroids as new vertices each
time) produce a bigger copy of the original cube? Checked in exact
rational arithmetic, corner by corner: no — it produces the original
cube shrunk by exactly **1/3**, not enlarged. Repeating the cycle
converges toward the center, it doesn't expand outward. (A different,
classical definition of "dualize" — reciprocation with respect to a
fixed sphere — instead returns exactly the original with *no* scaling
at all, `P°° = P`; neither of the two natural definitions produces
growth on its own.)

## Module: `raum27.cube_projection` — Corner↔Face Projection, Exact Eigenstructure

Two linear maps built from the cube's corner/face incidence (each corner
touches 3 faces, each face has 4 corners): `m_6to8` distributes 6
face-values onto 8 corner-values (average of the 3 adjacent faces),
`m_8to6` projects 8 corner-values back onto 6 face-values (average of the
4 corners). Their composition `K = m_8to6 @ m_6to8` (6×6) has a closed
form, `K = (1/6)(I + A - P)` (`A` = all-ones, `P` = swap-with-opposite-face),
with an exact eigenstructure verified in rational arithmetic — no floats,
no numpy:

- **eigenvalue 1** (multiplicity 1): the uniform state — the only state
  that survives a corner-then-face round trip unchanged.
- **eigenvalue 1/3** (multiplicity 3): one "this face up, its opposite
  face down" mode per axis.
- **eigenvalue 0** (multiplicity 2): modes erased in a single round trip.

Since every non-uniform eigenvalue has magnitude < 1, repeated
application of `K` to *any* starting state converges toward the uniform
state — checked exactly (not approximately) by decomposing a mixed input
into its eigen-components and verifying the non-uniform part shrinks by
precisely `(1/3)ⁿ` after `n` applications, while the uniform part is
untouched.

**Driven system:** `apply_driven` adds a constant source every step
instead of a single one-off input left to decay, `v_{n+1} = K @ v_n +
source`. This behaves differently per eigenspace, verified against the
exact closed-form solution of the linear recurrence (not by iterating
and eyeballing convergence):

- A source component along the eigenvalue-1 (uniform) direction is never
  damped — the mean grows by exactly `mean(source)` every step, without
  bound. This is resonance in the ordinary linear-systems sense: a
  constant drive aligned with an undamped eigendirection.
- A source component in the eigenvalue-1/3 eigenspace converges to a
  finite steady state, `source_component * 3/2` (the geometric series
  `1/(1 - 1/3)`).
- A source component in the eigenvalue-0 eigenspace locks to exactly the
  source's own value after a single step.

A source with components in more than one eigenspace therefore produces
an ever-growing mean with a fixed, bounded pattern superimposed on it —
a standing pattern riding an unbounded carrier, driven by a source that
never stops. See `tests/test_cube_projection.py`.

## Module: `raum27.kern_modul_v1` — Five Checkable Facts, Ported from a Lean Draft

Independently re-verified here in exact rational arithmetic, from an
external Lean 4 draft (`RAUM27_Modul_v1.lean`) that itself explicitly
marked its unproven parts with `sorry` instead of hiding them:

- **Reflection group on the cube's 8 corners**: 1 reflection reaches only
  2 corners, 2 reflections (X, Y) reach only 4, and all 3 (X, Y, Z) are
  needed to reach all 8 — checked by breadth-first closure, not asserted.
- **Octant solid angle**: exactly 1/2 (in units of π sr) of the full
  sphere's 4π sr, for any octant regardless of cube size.
- **Corner parity** (number of set bits mod 2): exactly 4 of the 8
  corners are even, 4 are odd. An edge (1 bit flips) always toggles
  parity; a face diagonal (2 bits) never does; a space diagonal (3 bits)
  always does.
- **TDOA localization**: `x = (L - v·Δt) / 2` puts the source at the
  midpoint when Δt = 0, and is exactly linear in Δt (so a small timing
  error produces a proportional, not runaway, position error).
- **Redundancy condition** `X · (1/X) = 1` for `X ≠ 0`, checked for a
  batch of random rationals.
- **A rational identity behind "1/9"**: `(√3)⁴ = (√3²)² = 3² = 9` (no
  irrational ever appears in the arithmetic), so a corner's `1/r⁴`-model
  contribution is `1/9`.

**Deliberately left out**, because nothing backs them yet: the source
draft's three `sorry`-marked claims (full transitivity of the reflection
group — true, but not formalized here either; an empirical "2.6–3.2×
noise reduction" factor with no reproducible experiment attached; and an
explicitly unfinished compression chain).

**One thing flagged rather than accepted**: the source presents the 1/9
identity above and a second computation, `1 − 8/9 = 1/9`, as two
*independent* confirmations. They aren't — the second one assumes the
other 8 corners contribute exactly 8/9 without deriving that from
anything, so `1 − 8/9 = 1/9` holds by construction for whatever share is
assumed, not as independent evidence. Both functions are still included
(`face_contribution`, `complement_contribution`) so this distinction
stays checkable rather than silently accepted. See
`tests/test_kern_modul_v1.py`.

## Module: `raum27.kern_modul_v2` — Corrections from an External Code Package

Ported from a larger external Python/Lean package ("RAUM27 – Geprüfter
Kern", Stand 26.8.2026) after running every file in it rather than
accepting its own "✅ Bestätigt" status table. Three real issues were
found and fixed, one Lean syntax error was found and corrected:

- **Naming error, not a math error**: the source calls two coordinate
  rotations "Spiegelungen" (reflections/mirrors) and an angular-doubling
  step "Doppelspiegelung". A true reflection has determinant −1; both
  rotations here have determinant +1, confirmed by direct computation
  (`rotate_about_x`, `rotate_about_y`, tested in
  `test_kern_modul_v2.py`). The underlying arithmetic was correct — only
  the name was wrong, so it's renamed here rather than dropped.
- **A circular "two independent systems" test**: the source computed a
  wavelength as `v_true / f_true` and multiplied it back by `f_true`,
  presenting the recovered `v_true` as confirmation from two separate
  measurement systems. It isn't — `(v/f)·f = v` holds algebraically for
  *any* `v` and `f`, independent of any real measurement. Kept
  (`wavelength_from_velocity_and_frequency` /
  `velocity_from_wavelength_and_frequency`) but the docstring and test
  name it as the identity it is, not as independent evidence.
- **A control test with no assertion**: the source's check for
  periodicity false-positives on pure random (period-free) data printed a
  result but asserted nothing — it could not fail regardless of what came
  out. Fixed here: `false_positive_counts` runs the same detector on
  random noise across many trials, and
  `test_periodicity_control_has_real_assert` requires that no single
  candidate period wins more than 15% of trials. Measured baseline across
  10 independent seeds × 500 trials × 18 candidate lags: 6.8%–8.6%
  (uniform-chance baseline is 1/18 ≈ 5.6%), so the 15% bound is real and
  would catch an actual regression (e.g. a detector that always reports
  the same period), not just pass by construction.
- **A Lean syntax error**: `RAUM27_Gitterraster.lean`, theorem
  `keine_feinere_ausloesung`, line 24, has 5 opening brackets/parens and
  only 4 closing ones — it would not parse, regardless of whether the
  proof idea is right. Confirmed with a standalone bracket-balance
  checker (independent of any Lean toolchain, since none is available
  here). The corrected line is
  `` rw [abs_of_neg (by nlinarith [mul_pos hDX (show (0:ℚ) < 1 by norm_num)])] ``.
  As with `kern_modul_v1`, the `.lean` source itself is not added to this
  repo (no Lean toolchain here to verify it compiles) — only the
  independently-checked Python port is.

**Deliberately left out**: the source package's LED/hex-color demo
scaffolding and its "live" noise-reduction wrapper. Both ran without
error, but neither carries an independent checkable claim beyond what
`redundancy_corrected_reading` below already covers — they're UI/demo
plumbing, not verified math.

**A second submission for the same package** claimed "Alle 133 Tests
bestanden". Running it as given falsifies that on the first attempt: its
`NegativraumTensor` computes `welle + (-welle)`, which is identically 0
for every input by construction, while its own test asserts the result
is positive — a 100%-reproducible failure (checked directly across 5
random trials, all exactly `0.0`), not bad luck with a seed. Its "133
Tests" line was also just that repo's unrelated whole-suite `pytest`
total, copied onto a file that defines 8 test functions. Dropped
entirely, along with its `Kompressionskreis` helpers (bare wrappers
around division/exponentiation with no independent claim) and its
duplicated German-named re-implementations of the rotation, ray-doubling,
TDOA, and periodicity-control functions already above.

One piece of it survived: a redundancy check on the triple
`[x, 1/x, x·(1/x)]`. Its own version used floats and checked
"monotonicity" at exactly two points; redone here in exact `Fraction`
arithmetic as `redundancy_state` / `redundancy_deviation`, checked on a
90-point grid in each direction instead of two points, plus an exact
symmetry check `deviation(x) == deviation(1/x)`. A generalization of that
symmetry to an arbitrary reference point was tried and found **false** by
direct counterexample before it went anywhere near this file — so the
docstring only claims what was actually proven, for reference = 1.

**The rest of the original package was checked too:**

- `raum27_delta_mustererkennung.py`, `raum27_led_sensor.py`,
  `raum27_live_kompakt.py` all duplicate content already covered above
  (the `[x, 1/x, x·(1/x)]` delta, a TDOA formula with a constant offset,
  and the same hex-color demo pattern) — except one real, new claim in
  `raum27_live_kompakt.py`: averaging 8 independent noisy redundancy
  readings should cut the mean error by about `√8 ≈ 2.828` (ordinary
  statistics — standard error falls off as `√n` for `n` i.i.d. samples).
  The source measured 2.572 in a single 500-trial run and stopped. Rerun
  against this module's own `redundancy_corrected_reading` /
  `averaged_reading` across 4 seeds × 400 trials: 2.61–2.88 — 2.572 was
  one noisy sample of a real effect, not a discrepancy. Now covered by
  `test_averaging_eight_axes_reduces_noise_by_roughly_sqrt_eight`.
- `raum27_kompressionskreis.py` was named in the package's own status
  table but was never actually among the files pasted — nothing to
  verify, so nothing was ported under that name.
- The three Lean files that passed the bracket-balance check
  (`RAUM27_Kern.lean`, `RAUM27_Wuerfelsymmetrie.lean`,
  `RAUM27_Resonanzauslese.lean`) contain no `sorry` and no circular
  proofs; their corner-reflection and TDOA/velocity/period claims check
  out algebraically. One naming overreach found in `RAUM27_Kern.lean`:
  `wave_resonance_left_right` sounds like a general law, but its
  hypothesis fixes `n.val = 1`; the same formula at `n.val = 2` gives
  `(2·16/9)·(2·9/16) = 4`, not 1. The Lean statement is honest about the
  restriction — the hypothesis is right there — but the name oversells a
  trivial special case as a general resonance effect. Not ported.

**Two more additions**, from a "Farbspektrum, Spiegelung, Wellenform"
submission that mostly restated existing content — `reflections_needed_for_full_circle`
and `central_inversion_angle`:

- Reconstructing a full circle from a single arc via repeated
  reflection-doubling (already what `bisect_rays` does) needs
  `log2(denominator)` steps for a starting arc of `360/denominator`
  degrees — standard dihedral-group math, made explicit as a formula and
  cross-checked against an actual doubling simulation, not just the
  closed form.
- `270°` doesn't need its own independent state if central inversion
  (`v → -v`) is already available: `central_inversion_angle(90) == 270`
  exactly — a real, verified reduction from 4 angle states to 3, not
  asserted.

**Left out from the same submission:** a claim that hexadecimal (16)
is "geometrically derived" from `4` angle nodes applied independently to
two axes (`4² = 16`). That's correct arithmetic for whichever number of
nodes you start with — the same `bⁿ` fact holds for any base `b`, so it
doesn't derive *why* 4 nodes specifically, only that 4×4=16 once 4 is
already chosen. Same pattern as the `(1/8)/(1/9)=9/8` argument earlier in
this module: a real operation applied to an unexplained starting choice.

See `tests/test_kern_modul_v2.py`.

## Module: `raum27.basisoperationen` — Scale a Cube Without Recomputing Its Geometry

Ported from a separately-submitted "RAUM27 Kern-Release" package after
independently reproducing its own claimed test count first (72/72,
confirmed by direct execution before anything was ported — the correct
order, given how many earlier submissions this session claimed passing
tests that turned out not to hold up).

The idea itself is real and useful: every cube quantity scales as `k^n`
under a uniform scale factor `k`, where `n` depends only on the
quantity's *type* — 0 for ratios/angles/combinatorics (corner count, face
count, ...), 1 for lengths, 2 for areas, 3 for volumes — never on which
specific quantity it is. `hole_wert(name, k)` looks this up in O(1) from
the `k=1` value instead of re-deriving the geometry at every scale.

**One change from the source:** it computed diagonal lengths with
`math.sqrt` in floats, which are irrational and so lose exactness. Redone
here with the SQUARED diagonal lengths instead — the same convention
`cube_symmetry.py` already uses for `face_diagonal_squared` /
`space_diagonal_squared`, and for the same reason (`√2`, `√3` are
irrational; `2`, `3` are exact rationals) — so every value in this module
stays an exact `Fraction`, including at fractional scale factors.

`hole_wert` is checked against `cube_symmetry.py`'s independently-derived
functions, not against itself: 88 exact matches (11 quantities × 8 scale
factors, including `1/3`, `9/8`, and `1/1000`), all in
`tests/test_basisoperationen.py`.

## Module: `raum27.hyperoperationen` — Addition, Multiplication, Power, Tetration

Ported from a "RAUM27_Operatorkette_und_6_8_Gleichgewicht.py" submission
after independently reproducing its own numeric example (`a=2, n=3` →
`5, 6, 8, 16`) by direct execution. The hierarchy itself — each operation
is repeated application of the one before it — is standard mathematics
(Knuth's up-arrow notation), included here because it clarifies a point
worth stating precisely: **roots and logarithms are not a separate rung
of this ladder above exponentiation.** They are the two different
inverses of the same operation `b**x = y` — a root solves for the base
`b`, a logarithm solves for the exponent `x`. The real next rung above
exponentiation is tetration.

**One implementation choice corrected before shipping:** a first attempt
tried to define every level purely recursively down to addition (the
textbook-formal definition). It hung. At tetration, the argument passed
into the exponentiation level is already an enormous tower, and
simulating exponentiation as that many repeated multiplications is
infeasible even for `a=3, b=3`. Redone with native `+`, `*`, `**` for the
first three levels (exact and fast) and a manual loop only for tetration
itself, which is inherently limited to tiny inputs regardless of
implementation — `3^^3 = 7,625,597,484,987`, `4^^3` already has 155
digits.

## Module: `raum27.kubus_6_8_gleichgewicht` — Where 6^X = 8^(10-X)

Also from the "Operatorkette" submission, reproduced and then
strengthened before porting. `f(X) = 6^X - 8^(10-X)` has derivative
`f'(X) = ln(6)·6^X + ln(8)·8^(10-X)` — a sum of two strictly positive
terms for every real `X` — so `f` is strictly increasing everywhere. That
means there is **exactly one** crossing point over all real numbers, not
merely "a root was found inside the interval `[5,6]`, which is what the
source checked. Verified here by confirming the root found in a wide
bracket (`[-50,50]`) matches the one found in the narrow bracket exactly,
and by sampling the derivative's sign directly across a wide range.
Solved by plain bisection (standard library only — no new dependency
added for one root-find).

**Negative finding kept, not dropped:** the source also tried "raising
the exponents themselves" — comparing `6**(X**N)` against `8**(N**X)` —
hoping for a family of equilibria. It isn't one: both sides explode
super-exponentially and diverge from each other rather than staying
balanced (`X=N=2` already gives 1,296 vs 4,096, and the ratio only
grows). `exploding_exponent_mismatch` exists so this stays a checkable
"this doesn't work," not a silently-dropped idea.

**Left out of both modules, from the same submission:**
- The claim that `(1/8)/(1/9) = 9/8` "strengthens r=9/8 over r=4/3" —
  arithmetically correct, but circular: nothing here independently
  justifies "Raum-Gleichgewicht = 1/8" or "Eckenintensität = 1/9" in the
  first place, so dividing two asserted numbers doesn't add evidence for
  either one. The `9/8` vs `4/3` question stays open.
- The "diameter-of-predecessor-equals-radius-of-successor" doubling rule
  — defines `f(r) = 2r` and then observes that iterating `f` produces
  powers of 2, which is restating the definition, not deriving it from
  independent geometry.
- The circle-area/sphere-volume scaling demo — correct, standard
  geometry, but already covered by `raum27.scale_hierarchy`
  (`area_scale`, `volume_scale`); nothing new to add.
- The `X0`/`X1`/`X2` "Ausleseoperatoren" — `X0` is the identity function,
  `X1` is division, `X2`'s "exact reversibility" is squaring and
  square-rooting, which is invertible by construction for any positive
  input. None of the three carries an independent claim beyond what
  they're already named as.

## Module: `raum27.phasor_resonanzfilter` — A Matched Filter, Not a Metaphor

Grew out of a late-night description — "ein Kreis als Masche um einen
Knoten, Information rotiert als Schwingkreis-Spektrum, ein Ereignisvektor
dockt via Impuls an" — that stayed pure metaphor through two earlier
rounds (a "Thomas'sche Zahlenkugel" neural-net sketch, a vaguer "networks
rotating around us" idea) before getting pinned down to three concrete,
checkable answers. Once precise, it turned out to be exactly **matched
filter / correlation receiver theory**, applied to a memory made of
several independently-rotating complex phasors:

- **State**: `s(t)_k = A_k · exp(i·(ω_k·t + φ_k))` — a bank of `K`
  phasors, each rotating at its own frequency.
- **Detector**: `e = s(t₀)/|s(t₀)|` — a unit vector "trained" on one
  snapshot of the memory.
- **Match**: `R(t) = Re[e^H · s(t)]` — real-valued correlation; fires
  when `R(t) ≥ θ`.

**What's provable, not just observed:** `|s(t)|² = Σ Aₖ²` is *exactly*
constant over `t` (each phasor's own magnitude never changes, only its
phase does). Combined with Cauchy–Schwarz, that constancy means `t₀` is
a **global** maximum of `R(t)` — not just a nearby local one. Verified by
scanning `R(t)` across a 1,000-point-wide range, not merely a handful of
points near `t₀`.

**Two things worth stating precisely rather than leaving implied by the
"always available" framing:**

- The match is a **moment**, not a persistent state. A fixed detector
  does not stay "docked" to a rotating `s(t)` — `R(t)` falls off as `t`
  moves away from `t₀`, because the phasors keep rotating apart. A
  system built on this needs to keep re-evaluating `R(t)` over time
  (exactly what a real correlation receiver does), not assume a match,
  once found, holds.
- Discrimination between two independently-generated patterns is a
  **statistical tendency, not a guarantee**, and depends heavily on the
  channel count `K`. There's a concrete, reproducible `K=4` example
  where the detector's *own* pattern peak is lower than an unrelated
  pattern's peak — different patterns don't automatically get told
  apart. Measured over 150 random pattern pairs per `K`: a nonzero
  failure fraction at `K=4`, a lower one and a bigger typical margin at
  `K=32`. More channels help; no `K` tested makes it a certainty for a
  single instance — the same kind of correction this project needed
  before, when an assumed-safe method turned out to need a real,
  measured threshold instead of an assumption
  (`kern_modul_v2`'s periodicity control test).

## Module: `raum27.rotationsebenen` — How Many Rotation Planes Does a Space Need?

From a "Tagesabschluss" summary with six claimed building blocks and no
code attached. Most restated existing content or weren't independently
checkable from the description alone — but two were, without needing any
external code, so they were verified directly and are ported here.

Standard mathematics: the rotation group SO(n) has dimension `n(n-1)/2`
— one independent generator per pair of axes. Ordinary 3D space needs 3
planes (XY, XZ, YZ); a 4th, genuinely *rotatable* axis needs 6 (XY, XZ,
XT, YZ, YT, ZT), not 3. Checked here for `n = 2..5` against the closed
form (`1, 3, 6, 10`), and — the actual point of the submission — with a
concrete counterexample: two 4D rotation states built from *identical*
XY, XZ, and XT angles, differing only in an added YZ rotation, act
differently on the same test vector. So indexing a 4D rotation state by
only its three axis-touching angles genuinely loses information; you
need all six.

**Said precisely, because this project has its own explicit principle
that could otherwise get bent to fit:** "T = Matroschka-Skalierungsachse,
keine 4. Raumdimension" (see the top of this README) — T is explicitly
NOT treated as a rotatable spatial axis anywhere else in this codebase.
This module verifies the general fact (*if* a 4th axis were rotatable,
you'd need 6 planes), not a claim that T is one.

## Module: `raum27.modulketten_zuverlaessigkeit` — Chained Modules Need a Hand-Off, Not Hope

The other independently-checkable piece from the same submission:
series-system reliability, applied to a chain of pipeline modules run
"greedily" (continue until the first failure). Standard reliability
engineering — a chain only succeeds if every link does, so the exact
success probability is the *product* of the individual ones
(`chain_success_probability`) — plus a Monte Carlo check
(`simulate_greedy_chain`) of the specific claim in the submission: with
10 modules at independently-drawn success rates between 70% and 95%,
only about 15% of runs complete the whole chain
(`E[rate]^10 = 0.825^10 ≈ 14.6%`, confirmed by simulation to within 1
percentage point over 50,000 trials), and the average chain breaks after
about 4 of 10 modules. That's not a marginal inefficiency — it's the
quantitative case for why a hand-off mechanism ("the next module resumes
from wherever the last one stopped") is structurally necessary for a
chain this unreliable, not an optional nicety.

**Left out of both modules, from the same submission:**
- The reciprocal Y/X pair (`1/Y=X`, `1/X=Y`, avoiding `0×∞=1`) — already
  exactly what `rational_space.py`'s `involution(x)=1/x` on Q+ does (Q+
  excludes 0 by construction, which is precisely what sidesteps the
  `0×∞` issue). Nothing new to add under a different variable name.
- The angle-controlled coupling (`C²` at 0°, `-C²` at 180°, `0` at 90°,
  continuous in between) is exactly `C²·cos(θ)`, the ordinary dot-product
  formula between two unit vectors. Correct, but there's no independent
  content beyond "cosine is continuous" to test.
- The index notation (`XY-Süd-+`) and the encapsulation/`8^n`-growth
  argument aren't mathematical claims with a specific checkable content
  of their own — the general point ("independent choices compound
  multiplicatively, not additively") is true but generic to
  combinatorics, and the specific "8" was never derived from anything.

## Module: `raum27.wellenformen` — Square and Triangle Waves Are Different Shapes, and Neither Sits Still

From the same "Farbspektrum, Spiegelung, Wellenform" submission: a
correction to an earlier "Energiegleichgewicht" (fixed energy
equilibrium) framing of Fourier partial-sum approximation, plus a real
distinction between two wave shapes that's easy to blur together.

- **The correction, verified**: adding more sine terms to approximate a
  square wave doesn't hold the total energy at some constant value — it
  strictly *increases*, converging up towards the true signal's energy
  (Parseval's theorem / Bessel's inequality). Checked over 1, 2, 3, 5,
  10, 20, 50, 100 terms: strictly monotonic, reaching 99.8% of the full
  energy at 100 terms, never sitting still along the way.
- **Square and triangle waves are genuinely different target shapes**,
  not the same curve at different levels of refinement. The square
  wave's partial sums overshoot the jump by about 18% at 200 terms (the
  Gibbs phenomenon — a real signature of approximating a discontinuous
  function with finitely many continuous sines) and spend over 90% of
  the period near ±1 (a plateau); the triangle wave's partial sums never
  overshoot ±1 (it's continuous, so there's no jump for Gibbs to act on)
  and spend under 10% of the period near the extremes (a ramp, not a
  plateau).

## Module: `raum27.zahlensysteme` — RGB and an "8-Cube" Are the Same Number, for the Same Reason

Two small, correct facts, also from the same submission: `log2(9) ≈
3.17` bits per digit sits strictly between binary (1 bit) and hex (4
bits) — ordinary Shannon information content, not a discovery, but
checked rather than assumed. And `16⁶ = 8⁸ = 2²⁴ = 16,777,216` exactly —
because `16 = 2⁴` and `8 = 2³`, so `16⁶` (RGB: 3 channels × 2 hex digits)
and `8⁸` (an "8-cube" to the 8th power) are the same number written two
different ways, not an independent coincidence between color spaces and
cube geometry.

## Open Questions — Where Verification Stopped, Not Where an Idea Was Refuted

For whoever picks this up next: these are points where the trail runs
out because something specific is still missing, not because the
underlying idea was shown wrong. Each one names exactly what's needed to
move it forward.

1. **Matroschka scaling factor: `r = 9/8` or `r = 4/3`?** Both appear
   across the source material; neither is formally decided here.
   `coupling_constant()` (`cube_symmetry.py`) independently establishes
   `4/3` as corners/faces. A competing derivation for `9/8` also exists
   (an octant's volume, `1/8`, divided by `kmv1_face_contribution()`,
   `1/9`) — but *why division of specifically these two quantities*
   should equal the correct scaling factor, rather than any other
   combination, has never been derived, only asserted. Needed: an
   independent argument for that specific operation, or a decision to
   drop the claim.
2. **`kern_modul_v1`'s "Weg B" for the 1/9 result**
   (`complement_contribution`, `1 - 8/9`) is documented as NOT an
   independent second derivation — it assumes the complement (`8/9`)
   rather than deriving it from a model. If a genuinely independent
   second path to `1/9` exists, it hasn't been supplied yet.
3. **A weighted, full-rank cube↔octahedron mapping** (6 face-centers ↔ 8
   corners, referenced in external notes as reaching rank 6 with
   non-uniform edge weights, vs. rank 4 for uniform ones): no code for
   this has ever been supplied here to verify, and "some weights work by
   random search" isn't the same as a geometrically-motivated choice.
   Needed: the actual weights, and a reason they're the right ones, not
   just a working ones.
4. **`raum27_kompressionskreis.py`** — named in an external status table,
   never actually delivered here. Content unknown; nothing to evaluate
   until it's supplied.
5. **Forecasting/ML work (e.g. the Zindi financial-inclusion
   competition, any multi-agent forecasting system)** is deliberately
   kept OUT of this repo on purpose, not as an oversight: its correctness
   is judged by an external leaderboard on held-out data, which is a
   stronger, harder-to-game check than anything a code review here could
   provide. Nothing to integrate unless the underlying *general-purpose
   math* (not the forecasting claim itself) turns out to be reusable
   elsewhere.