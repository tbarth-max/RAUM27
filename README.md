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

Run the test suite with `pytest` (481 tests as of this module set, all
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

## Module: `raum27.duplex_inversion` — Where Two Exponent Towers Actually Meet

Ported from a Lean sketch (`RAUM27_Duplex.lean`) that stated four
theorems about `r_out(x,n) = (1/2)^(x^n)` and `r_in(x,n) = (1/2)^(n^x)`
and **proved none of them** — all four bodies were `sorry`, honestly
marked but unproven. All four statements are in fact true (re-verified
here in exact rational arithmetic), and all four are one-liners, so the
`sorry`s weren't hiding anything hard. What the sketch *missed* is the
interesting part:

- **Its "Fokalpunkt" theorem (`r_out(1,1) = r_in(1,1)`) is a tautology.**
  At `x = n = 1` both exponents are literally the same expression
  (`1**1`), so the claim says a value equals itself. Any two functions
  whatsoever agree wherever their arguments coincide.
- **The general symmetry it never states**: `r_out(x,n) == r_in(n,x)` for
  *every* pair, not just one point — true by definition, since
  `r_in(n,x)` is `(1/2)^(x^n)` spelled differently. The stated theorem is
  the weakest possible special case of this.
- **The coincidence set is bigger than claimed and genuinely
  non-obvious.** Where the two towers meet at the *same* arguments
  (`x**n == n**x`) is the whole diagonal `x == n`, **plus exactly one
  exceptional pair off it: `(2,4)` and `(4,2)`**, since `2⁴ = 4² = 16` —
  the classical result on `x^y = y^x` over the naturals. At that point
  both sides equal `(1/2)^16 = 1/65536`. Verified by exhaustive search up
  to 12; nothing else off the diagonal exists.

## Module: `raum27.waage` — A Balance Beam Reads a Ratio Off a Position

Came out of a framing worth taking seriously: don't chase an exact 0 or
100% — the logarithmic axes never reach those anyway — find the point
where two weights balance and read the **ratio** off the beam. That
intuition has an exact mathematical form, and it turns out to be the
structure already sitting in `kern_modul_v2`'s reciprocal measure.

- **The lever law is an exact, lossless ratio encoder.** Two weights
  balance when `w1·d1 = w2·d2`, giving `d1 = L·w2/(w1+w2)`. The
  fulcrum's *position* is the ratio — as an exact rational, no
  measurement of the weights themselves needed. Verified for all 121
  weight pairs up to 11, and `balance_point → ratio_from_balance_point`
  recovers the original ratio exactly for all 81 pairs up to 9. Nothing
  is lost in the encoding.
- **On a logarithmic axis, balance is the geometric mean**,
  `√(a·b)` — not the arithmetic one. For a reciprocal pair `b = 1/a`
  that product is exactly 1, so **every** reciprocal pair balances at
  exactly 1, whatever `a` is. Same fixed point as
  `rational_space.involution`, and the same "1 means equilibrium, not 0"
  convention the project uses throughout. Exposed as the *squared*
  geometric mean so it stays an exact `Fraction` — the same convention
  `cube_symmetry.py` uses for `face_diagonal_squared`, for the same
  reason (`√(a·b)` is irrational in general).
- **The cross-module connection that makes this more than a
  restatement**: `kern_modul_v2.redundancy_deviation(x)` is already
  mirror-symmetric under `x → 1/x`. In beam terms that symmetry *is* the
  balance — straying by a factor `k` to one side costs exactly what
  straying by factor `k` to the other side costs. Checked across both
  modules in `tests/test_waage.py`, not asserted. The project's own
  recurring `16/9 ↔ 9/16` pair falls out as one instance.

**Closed question, with the negative result kept** (`is_lossless_encoding`):
does the beam live in some "prime number space"? No. The load-bearing
property is **coprimality**, not primality. Coprime weights make the
balance point already irreducible (`gcd(w2, w1+w2) = gcd(w2, w1) = 1`),
so the pair is recoverable from the position alone — verified for all
132 ordered pairs of distinct primes up to 37, with no colliding
positions. But primes are merely a convenient way to guarantee
coprimality, not the reason it works: `(16, 81)` are both composite and
encode just as losslessly. And prime balance points land on nothing
special — the denominator is always `w1+w2`, and sums of two primes are
usually composite (`3+5=8`, `5+7=12`, `11+13=24`). Conversely,
non-coprime pairs genuinely collide: `(2,4)` and `(1,2)` both put the
fulcrum at `2/3`, and the beam cannot tell them apart. That's a real
limit of the method, archived rather than dropped.

Incidentally this is the working form of something that failed earlier
in the project: the DX/DT module wanted to preserve "unreduced fractions
as fingerprints" and broke on an implementation detail. With coprime
weights there is nothing to reduce, so the fingerprint survives by
construction.

### From two weights to n: the common point is exact, the individual places are free

The two-weight beam generalizes without any new machinery. For `n`
weights at positions `x_i` the common point is the centre of mass
`Σ(w_i·x_i) / Σ(w_i)` — these are barycentric coordinates (Möbius,
1827), standard mathematics, correctly applied here. Three things in it
are worth stating because they are exact, not approximate, and because
each was computed rather than assumed:

- **It is the same function, not a second construction.** For two
  weights at positions 0 and 1, `center_of_mass` returns bit-for-bit
  what `balance_point` returns — verified for all 81 pairs up to 9. The
  lever law is the n=2 case.
- **The individual places are free; the common point is not.** Three
  weights `(2, 3, 5)` at `[0, 1/2, 4/5]` and at `[1/4, 1, 2/5]` give the
  same centre, exactly `11/20`. There are infinitely many such
  arrangements. In every one of them the residual torque about the
  centre, `Σ w_i·(x_i − pivot)`, is **exactly 0** — that is what makes
  the centre the centre, and it holds for negative positions too
  (`[−7, 3, 11/3]`). Freedom in the parts, exactness in the whole.
- **A weight of 0 has a share of exactly 0, at any distance.** Its
  contribution is `w_i·x_i = 0` whatever `x_i` is, so a zero weight
  placed at 0, 100, −1000 or 10⁶ leaves the common point at exactly
  `11/20`, unchanged by any amount. "Far outside" is literal here:
  outside the system's determination entirely. And `shares` are exact
  rationals summing to exactly 1 (`(2,3,5) → 1/5, 3/10, 1/2`), so the
  share is the element's own ratio to the whole — it follows from what
  the element is, nothing assigns it.
- **All weights zero means there is no system**, not a degenerate one:
  `shares` and `center_of_mass` both raise, at the same place
  `balance_point` already raised for `w1+w2 = 0`. Division by the total
  is undefined, and no convention rescues it.

## Module: `raum27.optionsraum` — The Inversion: Everything Is the Centre, One Thing Is the Edge

The beam says: wanting *nothing* puts you infinitely far out with a
share of exactly 0. The natural next thought inverts it — wanting
*everything* is the zero point in the space of all options, and wanting
exactly *one* thing is the far outside. That inversion holds, but it
happens in a **different space**, and keeping the two apart is what
makes both statements true at once.

**Two independent coordinates.** A wish vector over `N` options carries
the total `Σw_i` (how much is wanted at all — the `waage.py`
coordinate) and the direction `p = w/Σw_i` (*what* is wanted, a
distribution on the probability simplex — this module's coordinate).
They cannot be traded against each other, so "far out" means two
different things and neither claim overrides the other. Where they
meet is exact and already in the code: the direction is **undefined**
precisely when the total is 0, which is where `waage.shares` already
raises. *Wanting nothing is not a position in the option space at all* —
it is the one place that coordinate fails to exist.

- **The all-wanting point is literally the zero point.** `p = (1/N,…,1/N)`
  is the centroid, and in centred coordinates `q = p − c` it is exactly
  the origin. `squared_distance_from_centre` returns exactly 0 there.
- **A single wish sits at exactly `(N−1)/N`.** For `N = 6`: `5/6`; for
  `N = 8`: `7/8`; for `N = 27`: `26/27`. An exact rational, and
  **strictly below 1 for every finite `N`** — the outer position is
  approached, never reached. (Caveat, stated so it isn't over-read:
  `26/27` arises for *any* 27-option space. Nothing cube-specific is
  doing the work, and nothing here derives `N = 27`.)
- **The identity doing all the work.** For every `p` on the simplex,
  `|p − c|² = Σp_i² − 1/N` exactly, because `p·c = 1/N` for every `p`.
  So "how far out you are" and "how concentrated your wishes are" are
  the same number up to a constant — verified on 2100 random exact
  rational points across `N = 2…8`. That converts the geometry into
  algebra, and both extremes then follow with complete proofs:
  `Σp² ≤ (max pᵢ)·Σpᵢ = max pᵢ ≤ 1` with equality iff some `pᵢ = 1`
  (maximum **only** at the vertices), and `(Σpᵢ)² ≤ N·Σpᵢ²` by
  Cauchy–Schwarz so `Σp² ≥ 1/N` with equality iff all equal (minimum
  **only** at the centroid). Both uniqueness claims are additionally
  brute-forced over every exact lattice point of the simplex with
  denominator 12.
- **`participation_number = 1/Σp²` reads the count back off the
  distribution**: exactly `N` for the uniform wish, exactly `1` for a
  single wish. How many things you effectively want, as an exact
  rational.

**The correction, kept rather than smoothed over.** The *maximal delta*
in this space is **not** between "everything" and "one thing". It is
between two **different** single wishes:
`|p − q|² = Σp² + Σq² − 2(p·q) ≤ 1 + 1 − 0 = 2`, with equality iff both
are vertices and `p·q = 0`. So the diameter is exactly **2**, and it is
**independent of `N`** — adding options adds no reach (checked for all
`N` from 2 to 39). Centre-to-vertex is `(N−1)/N < 1`, *less than half*
the diameter for every `N`. Two single-minded positions wanting
different things are more than twice as far apart as the all-wanting
centre is from either of them.

**So what the centre actually is** — not the far end of a maximal delta,
but the unique minimiser of the worst case:
`maxᵢ |p − eᵢ|² = Σp² + 1 − 2·minᵢ pᵢ ≥ 1/N + 1 − 2/N = (N−1)/N`, using
both bounds above, and they are tight simultaneously *only* at the
centroid. Brute-forced: over the full exact lattice for `N = 3, 4`,
**nothing beats it and nothing ties it**. From the centre every single
wish is equidistant. That is a sharper statement than "maximal delta"
and, unlike it, provable.

Cross-checked against the module it inverts: equal weights on the `N`
single wishes give the uniform wish coordinate by coordinate via
`waage.center_of_mass`. The two modules are one construction seen from
two sides.

## Module: `raum27.impakt_schwelle` — The Compression Threshold, and What It Isn't

The question was precise: define the function at which a local impulse
on a minimal `Δx` breaks the lattice and triggers the flow into a new
structure. That function exists, it is standard mechanics, and it is
computable — so this module implements it. The surrounding
interpretation contained one correct insight and two claims that are
quantitatively false; both halves are kept, because knowing which is
which is the point.

*Unit note:* unlike the rest of the package this module uses SI floats,
not exact `Fraction`s — densities and yield strengths are measured
properties, so exactness would be false precision. The one genuinely
exact statement is verified symbolically over rationals in the tests.

**Correct, and mainstream: it is not melting, it is stress-driven
flow.** The mechanism is that inertial stress overwhelms strength, so
strength drops out of the balance and both bodies behave like fluids.
The threshold is a dimensionless number, Johnson's damage number
`D = ρv²/Y` — `D ≪ 1` elastic, `D ≈ 1` plastic onset, `D ≫ 1` strength
irrelevant. Setting `D = 1` gives `v = √(Y/ρ)`: **357 m/s for steel**,
149 m/s for copper, 33 m/s for lead. That is the "strukturelle
Haltekraft" being exceeded, as a number. At 2 km/s the dynamic pressure
is **15.7 GPa against a 1 GPa yield strength** — that ratio, not any
heat, is why the lattice stops holding.

**Correct, and better than an analogy: the `dx`/`dt` framing *is* the
derivation.** Balancing stagnation pressure across the interface,
`½ρ_j(v−u)² = ½ρ_t·u²`, gives `u = v/(1+√(ρ_t/ρ_j))`; a rod of known
length is consumed in `t = L/(v−u)`; the depth is `P = u·t`. That
collapses to

    P / L = √(ρ_j / ρ_t)

exactly and **independently of impact velocity** (Birkhoff, MacDougall,
Pugh & Taylor 1948). Knowing the length and the traversal time really
does give the penetration velocity. Verified both ways: the
step-by-step `u·t` route reproduces the closed form for every material
pairing and speed, and the algebra is re-checked symbolically over
exact rationals so no float rounding can hide a mismatch. Published
ratios come out right: copper into steel 1.068, tungsten into steel
1.568, aluminium into steel 0.587.

**False: "keine thermische Entropie", "kalter Phasenübergang".** Shock
compression is the textbook *irreversible* process — the entropy jump
is what distinguishes a shock from an isentropic compression. The
Hugoniot energy jump `Δe = ½u_p²` gives `ΔT ≈ u_p²/(2c_p)`: for steel,
278 K at 500 m/s particle velocity, **1111 K at 1000 m/s, and past
steel's melting point at about 1160 m/s on shock heating alone.** The
process is emphatically hot and emphatically dissipative.

**False: "die Energie geht restlos in die Überwindung der
Gitterbindung".** Breaking *all* iron lattice bonds costs its cohesive
energy, **7.39 MJ/kg**. Kinetic energy per mass is `½v²`, so at 1700 m/s
an impact brings 1.45 MJ/kg — **19.5%** of that. Only above about
**3.8 km/s** does it even reach break-even, and most of it goes into
bulk plastic work and heat rather than bond-breaking. At ordnance
velocity the lattice is not dismantled; a thin layer at the crater wall
is sheared apart while the bulk stays a solid crystal.

**Also not a phase transition.** "Flow" here is a change of
*constitutive regime* — strength negligible against inertial stress —
not of phase. The material stays crystalline throughout.

**The recrystallisation, though, is real — for the opposite reason.**
Dynamic recrystallisation in adiabatic shear bands at high strain rate
is well documented in steel. It is driven by exactly the local
adiabatic *heating* the "cold" framing denies. The conclusion survives;
the mechanism inverts.

**Validated against reality, including a bug found doing it.** The
strengthless limit overshoots at ordinary velocity. Retaining strength
(Tate/Alekseevskii, `½ρ_j(v−u)² + Y_p = ½ρ_t·u² + R_t`) gives `P/L =
1.21` at 1700 m/s for a 0.6 m tungsten rod into steel — the band real
long-rod penetrators actually sit in — against a strengthless 1.57. The
first implementation had a sign error in the quadratic's constant term
and reported *more* penetration with strength than without; the test
`test_strength_always_reduces_penetration_never_increases_it` exists to
pin that down. The corrected model rises monotonically and approaches
the hydrodynamic ceiling from below without crossing it out to 100 km/s,
and it predicts a **ballistic limit** (~455 m/s for tungsten into
steel) that the strengthless formula structurally cannot express — that
formula has no velocity in it and so "penetrates" at walking pace.

**Where this is *not* RAUM27**, stated plainly because this project has
a recurring failure mode of dropping a number into a conceptually
waiting slot: **nothing here derives from cube geometry.** The threshold
is `ρv²/Y`, the depth ratio `√(ρ_j/ρ_t)`. Neither contains 6, 8, 4/3,
9/16 or 27, and no step uses a lattice of faces and corners — they use
momentum and mass conservation across an interface. This is real,
verified mechanics that answers the question that was asked. It is not
evidence for the RAUM27 architecture, and reading the agreement as
support would be exactly the circularity flagged elsewhere here.

## Module: `raum27.lichtgitter` — Cause and Effect on an Ellipse, in Integer Light-Ticks

The claim: the cube doesn't *produce* the physics, it *orders* it —
turning cause and effect into a long ellipse that can be rolled back
and forth, everything defined on whole-number steps of a light-speed
delta. Most of this holds. One part holds **more strongly than it was
stated**, one part doesn't hold, and one part turns out not to need
what it asked for.

**Stronger than claimed: `c` already *is* an exact integer.** Not as an
idealisation. Since 1983 the metre is *defined* as the distance light
travels in `1/299792458` s, so `c = 299792458 m/s` is exact in SI by
definition, not a measurement that rounds nicely. The whole-number
instinct is literally right and needs no idealising — **which is why
idealising to 300 000 000 throws away the exactness it was meant to
supply.** The error is 207 542 m/s, a relative 0.0692%:

| Range | Timing error | Position error |
|---|---|---|
| GPS satellite | 46.6 µs | **14 km** |
| Earth–Moon | 887 µs | 266 km |
| Earth–Sun | 345 ms | 103 494 km |

**Exact: the ellipse is an isochrone with an integer invariant.** The
focal radii obey an exact identity, rational whenever the parameters
are: `r1 = a − e·x`, `r2 = a + e·x`. Verified on 4000 exact rational
points of random ellipses against the raw geometric distance in squared
form — **zero violations**. Two consequences:

- `r1 + r2 = 2a` **exactly, for every boundary point**. Every route
  from cause to effect has the same total length, so at fixed `c` the
  ellipse is an isochrone: same total flight time whichever way round.
  Rolling it back and forth conserves something exactly.
- On a lattice of `Δx = 1 m`, `Δt = 1/c s`, the **tick count is `2a`, an
  exact integer, for every route**. A one-light-second ellipse
  (`a = 149 896 229 m`) counts exactly 299 792 458 ticks, and the flight
  time `2a/c` is an exact rational with no rounding anywhere. That is
  "whole numbers of a light-speed delta", achieved exactly.

**It connects to code already in this repo, and explains a gap in it.**
The same two radii give the other conic for free: the *sum* `2a` is the
ellipse, the *difference* `2e·x` is the TDOA hyperbola that
`kern_modul_v{1,2}.tdoa_position` already computes. The ellipse isn't
bolted on — it is the sum counterpart of the difference already
implemented, and the difference inverts exactly (`x = (r2−r1)/(2e)`)
over `Fraction`, i.e. time-difference localisation without a single
float. Better: `tdoa_position(L, v, dt) = (L − v·dt)/2` assumes the two
distances sum to `L`, and on an ellipse that sum is the conserved `2a`,
**not** the focal baseline `2c`. Fed `2a` it returns the focal radius
exactly; fed `2c` it is wrong for every off-axis point. *The ellipse's
invariant is precisely the input that function was missing* — found by
a failing test, not by inspection.

Superposing the two families gives **elliptic coordinates, orthogonal
everywhere**, with a one-line proof: the gradient of a distance
function is a unit vector, so
`∇(r1+r2)·∇(r1−r2) = |∇r1|² − |∇r2|² = 1 − 1 = 0`. Checked numerically
on 20 000 random points (worst dot product 5.6e-16) and then **exactly
over `Fraction`** on 2738 rational points where both unit gradients are
themselves rational — every dot product exactly 0. The smallest fully
integral case: `a = 25, e = 3/5` puts `(15, 16)` on the ellipse with
focal radii exactly 16 and 34.

**Does not hold: 300 million overlays add nothing.** The confocal family
is complete with **two** parameters — one sum value, one difference
value — and that pair already addresses every point of the plane.
Superposing 300 million cause–effect pairs doesn't build a richer
structure; it resamples the same two-parameter family more finely.
There is no accumulation threshold at which new structure appears, and
nothing supports "perfect". The honest count is 2, not 3×10⁸ — and that
is a *better* result than the one asked for: the model is already
complete, so the 300 million aren't needed.

**Where the cube actually stands.** Stated fairly, because "the cube
only orders it" is a much weaker and more defensible claim than the
ones rejected elsewhere here, and as an *organising frame* it is
legitimate — a coordinate choice can genuinely be what makes a
structure computable. But it is not what makes it *true*. The conserved
quantity `2a` follows from the definition of an ellipse — constant sum
of focal distances — with no reference to faces, corners, 4/3, 9/16 or
27. And the integer the lattice counts is `c` itself, which factors as
`299792458 = 2 × 7 × 73 × 293339`: **not divisible by 6, 8, or 27.** The
cube can order this material, and the ordering is useful; it does not
generate the invariant, and the invariant does not point back at it.

## Module: `raum27.resonanztunnel` — Pipe, Standing Wave, Nested Layers, and `c^X`

Four claims, four different outcomes. Two hold exactly, one is real but
**inverts** its own conclusion, and one is dimensionally dead — except
the quantity it reaches for has an exact home, and that home is
literally a pipe.

**Exact: the standing wave gives integers.** A pipe resonates at
`L = n·λ/2`, so `f_n = n·v/(2L)` — an exact rational and an exact
integer multiple of the fundamental. Same structure `lichtgitter.py`
found on the ellipse, for the same reason: a closed path with a
conserved length admits only whole-number counts.

**Exact, and the strongest claim here: the core carries no shear.** A
force balance on a cylinder of radius `r` gives the shear stress from
the pressure gradient alone:

    τ(r) = G·r / 2

Note what is *absent*: viscosity, layer structure, which fluid sits
where. It follows from the pressure balance, so it holds for **any**
nesting — and therefore `τ(0) = 0`, exactly. "The inner core flows
without friction at the wall" is exactly right, it is exact rather than
approximate, and it survives arbitrary layering. That one needed no
weakening.

Two things it does not mean. The pipe still dissipates — pressure drop
times flow rate is strictly positive (24.5 W for a 10 m, 5 cm pipe at
1 kPa/m). Zero shear *at the axis* and non-zero dissipation *in the
pipe* are both true at once. And the core is frictionless only as
`r → 0`; at finite radius the shear is linear in `r` and ordinary.

**Real, but it inverts the conclusion: nesting works, *fractal* nesting
is worse.** Lubricating the wall with a thin low-viscosity film is a
genuine industrial technique (core-annular flow, for viscous crude).
Integrating the shear law by parts gives the exact N-layer result

    Q = (π·G/8) · Σᵢ (Rᵢ⁴ − Rᵢ₋₁⁴) / μᵢ

and hence a two-layer gain of `(1−q⁴)·(μ_core/μ_film) + q⁴`. A 5% water
film on an oil core multiplies the flow by exactly **186.31** — an
exact rational, not a fitted number.

**But self-similar nesting loses, provably.** At fixed film *volume*,
splitting the film into 2, 3, 4 or 5 self-similar shells loses every
time — checked exactly over `Fraction` across a systematic family of
arrangements, worst case down by a factor of **1.61**, and not one
beating the single wall film. The reason is visible in the two
formulas: a layer's benefit is weighted `Rᵢ⁴ − Rᵢ₋₁⁴` while its volume
cost is weighted `Rᵢ² − Rᵢ₋₁²`. The fourth power favours the outside far
more steeply than the second, so for a fixed budget the entire film
belongs at the wall. Nesting it inward spends it where `τ(r) = G·r/2` is
small and buys almost nothing. Same failure mode as `optionsraum`, from
the other side: the structure is already complete at its simplest, and
subdividing is a loss, not a refinement.

**Dimensionally dead: `c^X` is not a speed.** `c` is m/s;
`c² = 89 875 517 873 681 764` is m²/s², which is not a velocity.
Nothing travels at `c²`, and `c^X` is a speed only at `X = 1`. No amount
of resonance changes units. As a *transport* speed the idea stops here.

**But `c²` has an exact home, and it is a pipe.** A waveguide — a pipe
carrying a wave above cutoff — obeys `ω² = ω_c² + c²k²`, giving
`v_phase = ω/k` and `v_group = c²k/ω`, so

    v_phase · v_group = c²,  exactly.

Both halves deserve stating. **The phase velocity genuinely exceeds
`c`**, without bound as frequency approaches cutoff — at `f = 1.01 f_c`
it is 7.1 times `c`. So something in a resonant pipe really does move
faster than light, and the exact invariant tying it down is `c²`. The
reach for `c²` was not arbitrary, and this is the mathematical
definition the idea was asking for. And the group velocity stays
strictly below `c` at every frequency (scanned over 200 000: max
`0.99887 c`). The phase velocity is the speed of a *pattern*, not a
signal; it carries no information, which is why exceeding `c` costs
nothing. The module exposes *squared* velocities so both are exact
`Fraction`s with no roots: `v_p²·v_g² = c⁴` exactly.

**On quantum tunnelling.** The Hartman effect is real — tunnelling delay
becomes independent of barrier width, so apparent group velocity through
a thick barrier can be made arbitrarily large. It does not transmit
information faster than `c`: the signal *front*, the leading edge of a
wave genuinely switched on, moves at exactly `c` in every medium. So
tunnelling can be given a consistent mathematical description here, and
the waveguide pair is a fair classical analogue — but the description
that comes out says the barrier cannot be used to beat `c`. **Closed
question, not an open one.**

## Module: `raum27.rautenraum` — Where the Cube Is Derived Instead of Placed

Two halves of one thought, and both hold. **This is the first place in
this repository where the cube falls out of something rather than being
asserted alongside it** — it comes from "three orthogonal axes plus a
logarithmic field", with no cube assumed anywhere.

### The cube as the four points of a rhombus

Put a pyramid of height 1/2 on each face of a unit cube and you get the
**rhombic dodecahedron**. Every claim below is exact over `Fraction`,
not to a tolerance:

- Each of the 12 faces is a genuine rhombus — four equal sides,
  diagonals perpendicular and mutually bisecting. Checked for all 12.
- Each rhombus is **exactly two cube corners plus two pyramid apexes**:
  the four points, two from the cube and two from the surrounding
  space. "The cube is the structure in between" *is* the construction.
- The faces are in **bijection with the cube's 12 edges** — one rhombus
  per edge, built from that edge plus the apexes of the two faces
  sharing it. 12 and 12, no remainder.
- The diagonals are 1 and √2 — squared, 1 and 2, i.e. exactly
  `cube_symmetry.face_diagonal_squared`. The ratio that already runs
  through this project *is the shape of the rhombus.*
- Volume: cube 1 plus six pyramids of 1/6 = **exactly 2**. Twice the
  cube, nothing left over. (It also tiles space — it is the Voronoi
  cell of the face-centred cubic lattice.)
- Euler: 14 − 24 + 12 = 2.

### The logarithmic field around the axes

Multiply the squared distances to the three coordinate axes:

    P(x,y,z) = (y²+z²)(x²+z²)(x²+y²),    V = −½·log P

`V` is the sum of three 2-D logarithmic potentials, one per axis.

- **Singular exactly on the axes, nowhere else.** `P` is a product of
  three factors and vanishes iff at least two coordinates do — which is
  precisely the union of the three axes. So the axes are not points of
  the domain at all; they are the singular support. "Nobody reaches the
  axes" is exact — you cannot evaluate there, and approaching one the
  field grows without bound while staying finite at every actual point.
  And the converse is the sharper half: **the axes are recoverable from
  the field** as the set where it blows up. If the field goes, the axes
  go with it, because they are defined by it and not independently.
- **Decreases outward at exactly the same rate in every direction:**
  `V(t·u) = V(u) − 3·log t`, exactly, because `P` is homogeneous of
  degree 6. Not approximately radial — the radial part separates
  exactly, with rate 3.
- **Harmonic away from the axes** (worst numerical Laplacian 7e-7 over
  3000 random points), being a sum of harmonic functions.
- Strongest at the centre in a precise sense: at the origin all three
  factors vanish at once, so the singularity is of order 3 against
  order 1 at a general axis point.

### Where the cube comes from

Ask where the field is strongest and weakest on a sphere. With
`a = x²`, `b = y²`, `c = z²` and `a+b+c = 1`, the product is
`P = (1−a)(1−b)(1−c)`, and AM–GM puts the maximum at `a = b = c = 1/3`,
value exactly `(2/3)³ = 8/27`. Confirmed by brute force over 400 000
random directions — none exceeds it. The full picture:

| directions | count | `P` | character |
|---|---|---|---|
| face axes | **6** | 0 | singular, `V = +∞` |
| edges | **12** | 1/4 | saddle points |
| corners | **8** | 8/27 | maxima |

So three orthogonal axes carrying a logarithmic field single out
**6, 12 and 8** distinguished directions — the cube's faces, edges and
corners — with `6 − 12 + 8 = 2`. Nothing about a cube was put in; only
three axes and a logarithm. That is a genuine derivation, and it is the
direct answer to the objection raised against the earlier modules here,
where a cube ratio sat *next to* a result instead of following from it.

### What this does not establish

Stated because `8/27` would be easy to over-read:

- **Both numbers come from the number of axes being three.** 8 is `2³`,
  the sign choices; 27 is `3³`, from AM–GM at `a = b = c = 1/3`. In `n`
  dimensions the same computation gives `((n−1)/n)^n` at `2^n`
  directions — `1/4` in 2-D, `81/256` in 4-D, tending to `1/e`. The 27
  here is `3³` because space is 3-dimensional, and it coincides with
  this project's 27 only because that is also `3³`. The coincidence is
  real; it is not evidence, and a test pins that down.
- The derivation gives the cube's *directions* — the 6/12/8
  combinatorics and the symmetry group. It gives no cube of any
  particular size, and produces no `4/3`, no `9/16`, no coupling
  constant.
- `V` is a static potential. Nothing in it moves, propagates or
  predicts; it is a field in the mathematical sense, not a force law.

## Module: `raum27.tunnelgrenze` — The Idealisation Granted in Full

The question, taken at face value: *idealise*. Grant completely
frictionless inner flow inside some energetic field — magnetic,
electric, gravitational, or one entirely unknown. Whatever it is, it
still consists of geometric definitions and defined interactions, cause
and effect. Grant all of it. Then push to the shortest measurable `dt`
so the path becomes `dx` rather than `Δx`. Is that the perfect quantum
tunnel from resonance?

No — and the reason matters more than the answer: **the premise granted
in the question is what forbids the conclusion.** "Defined
interactions" and "cause and effect" are precisely the two assumptions
the limits follow from. Nothing about the field's identity is needed,
which is exactly why calling it unknown does not help.

### Two halves are already achieved, and not as idealisations

- **Completely frictionless inner flow exists.** Superfluid helium-4
  below its critical velocity dissipates *exactly* nothing — measured,
  not idealised. With `resonanztunnel.shear_stress`, where `τ(0) = 0`
  holds exactly for any layering, the frictionless core is real.
- **Transmission with minimal energy loss exists.** Superconducting RF
  cavities reach quality factors above 10¹¹ — fractional loss per cycle
  below 10⁻¹¹. That is engineering, not speculation.

So the idealisation is not the problem. Both of its physical halves are
done.

### Block 1: a lossless resonance is not hard, it is empty

The decisive one, because resonance is the proposed mechanism. For a
Lorentz medium the absorption obeys an exact sum rule:

    ∫₀^∞ ω·Im χ(ω) dω = π·wp²/2

**independent of the damping `γ` and the resonance frequency `ω₀`** —
verified numerically to within 0.3% across six decades of `γ` and two
resonance frequencies (the residual drift is quadrature tail
truncation, not physics). Total absorption is a *fixed constant* set by
the oscillator strength alone. Reducing the damping does not reduce it;
it makes it narrower and taller, peak going as `wp²/(γω₀)` — a
thousandfold smaller `γ` gives a thousandfold taller peak and the same
integral.

And `wp²` is exactly what creates the resonance. Set it to zero and the
absorption vanishes along with all dispersion and all resonance.
Kramers–Kronig says the same from the other side: zero `Im χ`
everywhere forces zero `Re χ`, i.e. vacuum. (The relation is itself
checked against the Lorentz oscillator, so the premise in use is the
real one.) **A lossless resonance is an empty set, not a difficult
target.**

### Block 2: the shortest `dt` costs the most energy

`ΔE ≥ ℏ/(2Δt)` — the shorter the time, the *more* energy the event must
carry. At the Planck time the minimum is **9.78×10⁸ J**: about 234
tonnes of TNT equivalent in a single quantum event, and exactly half a
Planck mass in energy. "Minimal energy loss" and "shortest measurable
`dt`" are opposite ends of one inequality; they cannot both be
optimised.

### Block 3: the medium's own excitations cap the frictionless speed

Landau's criterion needs no knowledge of the medium, only that it has
excitations — which "defined interactions" already grants:
`v_c = minₚ ε(p)/p`. Below it dissipation is exactly zero, above it
exactly not. Helium-4's roton minimum gives **59.3 m/s** (measured
~58), i.e. `2.0×10⁻⁷·c` — seven orders short, in the best frictionless
medium known.

The general form answers the unknown-field move:

| spectrum | critical velocity |
|---|---|
| `ε = c_s·p` (phonon) | `c_s`, the sound speed |
| `ε = p²/2m` (free) | **0 — no frictionless regime at all** |
| `ε = Δ + p²/2m` (gapped) | `√(2Δ/m)` |

A gap is what *creates* a frictionless regime; a fast one needs a large
gap. Pushing `v_c` to `c` requires `Δ = mc²/2` — 255 keV for an
electron, a gap of order the rest energy. At that point pair production
is open, the medium is creating particles, and **the no-interaction
premise has destroyed itself.** The requirement defeats its own
assumption.

### Block 4: causality alone fixes the front at `c`

This is what makes the unknown-field argument fail outright.
Titchmarsh: if the response is causal — no output before input, which
*is* "cause and effect" as granted — then `χ` is analytic in the upper
half plane, so `χ → 0` and `n → 1` at high frequency. Checked on a
Lorentz medium: `n` deviates from 1 by 5×10⁻³ at `ω = 10ω₀` and
5×10⁻¹³ at `ω = 10⁶ω₀`. The signal *front* therefore moves at exactly
`c` in every causal medium, whatever it is made of — from causality
alone, with no reference to the field's nature. Group velocity can
exceed `c` (`resonanztunnel` has a pipe where the phase velocity does);
the front cannot.

### And the `dx → 0` move itself

`v = dx/dt` with the front capped at `c` gives `dt ≥ dx/c` — 3.34 ns for
a 1 m pipe, 1.28 s to the Moon. Letting `dx → 0` does not escape this,
it empties it: the transmitted distance *is* `dx`, so `dx = 0` is not a
fast transfer but no transfer. **The quantity being minimised and the
quantity that makes the transfer useful are the same quantity.**

### What is left, which is not nothing

Everything in the request except the superluminal part is reachable,
and much of it is built. Zero-dissipation flow: real. Loss below 10⁻¹¹
per cycle: real. Group velocity arbitrarily close to `c`: real. A pipe
whose phase velocity genuinely exceeds `c`: real, and in this
repository. What is unreachable is a *signal* arriving before `dx/c` —
closed by causality rather than by engineering, which means it will not
yield to a better field, a better resonance, or a better geometry.

## Module: `raum27.verhaeltnis_herleitungen` — The Five Derivations of 4/3 and 16/9, Graded

Five derivations were offered, with the conclusion that `4/3` and
`16/9` are geometric and topological necessities rather than invented
magic numbers. **That conclusion is correct.** Both numbers have exact
derivations here. But they are not the five offered: one works only
after repair, one points at a real derivation without being one, one is
true but not explanatory, and two are wrong or empty. All of it is kept
— verdicts and better arguments — in the usual form.

**1. Sphere volume with `π` banished — fails, but is repairable.**
Setting `r = 1` alone gives `V = 4π/3 = 4.18879…`, not `4/3`; the `4/3`
appears only after separately dividing by exactly one power of `π`. And
that is not one operation: the n-ball volume is `π^(n/2)/Γ(n/2+1)`, so
dividing by `π¹` leaves a rational only in dimensions 1–3. In 4-D it
leaves `π/2`, in 5-D `8π/15`. The required power is dimension-dependent,
and the answer depends on what you strip (`V₃/π = 4/3`, `V₃/2π = 2/3`,
`V₃/4π = 1/3`).

**The repair, which is stronger than the original.** `4/3` *is* an
exact, π-free fact about the sphere — as a *ratio*, where π cancels
legitimately and nothing needs banishing:

    V_sphere / V_cylinder(radius r, height r) = 4/3,  exactly, for every r

That is a genuine geometric derivation. Its sibling is Archimedes' own
result: against the cylinder of height `2r` the ratio is `2/3`. Use this
version — it needs no special pleading about transcendental constants.

**2. A 4-stroke projected on 3 dimensions — valid but empty.** A
`p`-cycle on a `q`-lattice repeats with period `lcm(p,q)` and carries
ratio `p/q` — for *every* pair. A 5-stroke forces `5/3`, a 7-stroke
`7/3`. Nothing produces the 4; the 4-stroke is the premise and the
conclusion is the premise over 3. This is the failure mode already
recorded in this repo: a number placed into a slot shaped to receive it.

**But `4/3` does have a genuine cube derivation, and it is already
here.** `cube_symmetry.coupling_constant()` is `8 corners / 6 faces =
4/3`, an exact ratio of exact counts. The cube's 4 space diagonals over
3 axes gives the same — and it is the *same* derivation, since 8 = 2·4
and 6 = 2·3. One route, counted twice.

**3. The perfect fourth — true, not explanatory.** `4/3` is exactly the
Pythagorean perfect fourth; no dispute. But among fractions strictly
between 1 and 2 with denominator ≤ 7 there are only **17**, and `4/3`
ranks **second** by simplicity. Simple ratios recur across unrelated
domains *because* they are simple. `3/2` recurs at least as often and
nobody infers a mechanism from it.

**4. "Superposition squares" — wrong as stated.** The arithmetic is
right, the physics isn't. Superposition is **linear**: amplitudes add,
and *intensity* goes as the square. Two fields of amplitude `4/3` give
amplitude `8/3` and intensity **`64/9`** coherent, **`32/9`**
incoherent — checked against this repo's own
`phasor_resonanzfilter.energy`. Neither is `16/9`. `16/9` is *one*
field's intensity at amplitude `4/3`, a different statement.
**The working route is the cube one:** `(8/6)² = 16/9` exactly.

**5. `16/9 × 9/16 = 1` as proof of balance — true and empty.** It holds
for **every** non-zero `x`, so it distinguishes `16/9` in no way. This
repo already proves exactly that for arbitrary reciprocal pairs, in
`test_every_reciprocal_pair_balances_at_exactly_one`. `x·(1/x) = 1` is a
property of division. The related claim that the system must collapse
to zero torque is not shown by it either — what *is* shown, separately
and for real, is `waage.residual_torque` being exactly zero at the
centre of mass for any number of weights in any arrangement. That stands
on its own and needs no `16/9`.

### What survives

    4/3  = V_sphere / V_cylinder(r, h = r)     (π cancels, exact, any r)
    4/3  = 8 corners / 6 faces                 (exact cube counts)
    16/9 = (8/6)²                              (exact, the square of it)

Two independent routes to `4/3`, and the square of one for `16/9`. So
**the conclusion is right and the numbers are not arbitrary.** What does
not survive is that they follow from banishing `π`, from a 4-stroke,
from musical consonance, from superposition, or from `x·(1/x) = 1`.

Keeping the distinction is the point: *an argument that does not hold
weakens a conclusion that is true*, because it invites a reader to
reject both at once. And a derivation meant to "stifle every doubt at
the root" is the opposite of what makes this repository worth anything.
The ethos is question everything, benchmark everything, keep only what
survives — and `4/3` survives. On two arguments rather than five, and
better documented for having lost three.





## Module: `raum27.kugelkoordinaten` — Spherical Coordinates With No Floating Point

A forwarded script computed a distance and a spherical conversion, and
diagnosed it correctly: squares stay exact as `Fraction`, the square
root is the first rounding, and the angles are floats because `cos` and
`sin` are not rational. Its proposed next step was to carry the angles
as fractions and evaluate the trigonometry at the end. **There is a
better fix, and it removes the floating point rather than postponing
it.**

### Don't carry angles — carry what is already rational

For any point with rational coordinates, all three pieces of spherical
information are *already* exact rationals, with no trigonometry
evaluated anywhere:

    r² = x² + y² + z²        cos²θ = z²/r²        tan φ = y/x

For `(1, 2, 3)`: `r² = 14`, `cos²θ = 9/14`, `tan φ = 2`. The float
versions agree to 1e-12 (checked), but are never needed.

**And it is lossless.** From `(r², cos²θ, tan φ)` plus three sign bits
the point comes back exactly: `z² = r²cos²θ`, `x²+y² = r² − z²`,
`x² = (x²+y²)/(1+tan²φ)`. Verified on negative and fractional points and
on the `x = 0` axis. So refusing the square root gives nothing up — the
representation carries the same information as the point.

The script's own example was exact **only by luck**: 25 is a perfect
square. Move one endpoint to `(1,1,1)` and the squared distance is 5
with an irrational root. The squared form stays exact either way — the
same reason `cube_symmetry.face_diagonal_squared` keeps the square.

### Which angles can be exact at all — a theorem, not a limitation

**Niven's theorem**: if `cos(r·π)` is rational for rational `r`, it is
one of `0, ±1/2, ±1`. So in `[0,1)` there are **exactly 8** turn
fractions with a rational cosine:

| q | 0 | 1/6 | 1/4 | 1/3 | 1/2 | 2/3 | 3/4 | 5/6 |
|---|---|---|---|---|---|---|---|---|
| cos | 1 | 1/2 | 0 | −1/2 | −1 | −1/2 | 0 | 1/2 |

Denominators only 1, 2, 3, 4, 6 — and `viertakt`'s quarter turns are
four of these eight. Everything else returns `None` rather than a
rounded value.

**The project's squared convention doubles the set to 16.** Since
`cos² = (1+cos 2x)/2`, `cos²` is rational exactly when the doubled
angle's cosine is, which adds the halves: `1/8 → 1/2` and `1/12 → 3/4`,
*even though both cosines are themselves irrational*. Keeping the square
is not a workaround here — it genuinely enlarges what can be computed
without rounding.

### The fourth dimension is a hard obstruction, not a drawing problem

Leaving it out is right, and for a stronger reason than "it can't be
pictured". The Cayley–Menger determinant of `m` points is non-zero
exactly when they span `m−1` dimensions, and for `m` mutually
equidistant points it is `±m`:

| m | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|
| CM det | 2 | −3 | 4 | **−5** | 6 |
| spans | 1 | 2 | 3 | **4** | 5 |

So **5 mutually equidistant points span 4 dimensions**, and to sit in
3-space their determinant would have to vanish. It is −5. Computed
exactly over `Fraction` and cross-checked against configurations that
genuinely *are* flat (four corners of a square give 0; a tetrahedron
gives 8, so the test is not reading an artefact). The maximum number of
mutually equidistant points in `Rⁿ` is `n+1` — there is a configuration
that exists in four dimensions and provably cannot be realised in three
at all.

What *can* be done is exactly what was described: stack 3-D slices and
let the fourth parameter be the index running through them. That index
is not a spatial coordinate, so **no embedding obstruction applies to
it** — and the package already works this way. A `viertakt` state is
`(phasor, height)`: three spatial degrees of freedom plus one index,
where the height is the flow. The fourth thing emerges from the sequence
of slices rather than being a direction inside any of them.

### Two small confirmations

**Indexing 0,1,2,3 is still four places** — that was never in dispute.
The shift moves only where the count starts, from the ground rather than
the first deflection; `period()` is 4 either way.

**"Normalise onto one axis"** has an exact form here: the radius is the
single ray (`r²`, exact) and the direction is carried separately
(`cos²θ`, `tan φ`, exact). Nothing is projected away and nothing is
rounded.

## Module: `raum27.viertakt` — The Four-Stroke on Index 0, as Powers of `i`

The proposal: start the rhythm at index 0 and read it as powers of `i`,
so it begins at rest rather than already deflected. `i⁰ = 1` (ground),
`i¹ = i` (deflection), `i² = −1` (inversion), `i³ = −i` (mirror),
`i⁴ = 1` (closes — one turn higher).

**Attribution first.** When `spirale.py` says "the recursion grounds out
at turn 0", that sentence was about the formal termination of a
recursion and nothing more. `i⁰` as the start of a four-stroke was not
behind it. The reading is a genuine addition, not a recovery of
something already meant.

**Exact, with no floating point anywhere.** For integer `n`, both
`cos(nπ/2)` and `sin(nπ/2)` land in `{0, ±1}`, so the cosine and sine
never have to be *evaluated* — the states are exact Gaussian integers
and one tick is the integer map `(c, s) → (−s, c)`. A million ticks
accumulate no error. The "über Kosinus Sinus" route is right, and that
is precisely why it is computable.

**Period exactly 4**, confirmed twice: by exact integer iteration, and
by feeding the real and imaginary series to this repo's own
`kern_modul_v2.find_period`, which returns 4 for both.

**`i² = −1` really is the unique maximum of tension.** Squared
distances from the ground, as exact integers:

| n | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| `\|iⁿ − 1\|²` | 0 | 2 | **4** | 2 | 0 |

`n = 2` is the only maximum, at squared distance exactly 4 — the
diameter. "Exakter Gegenpol zum Ursprung" is provable, not imagery.

**And the central claim is exactly right.** `i⁰` and `i⁴` are the same
complex number and *not* the same state, because the height differs.
The phasor repeats every four ticks; the pair `(iⁿ, height)` never
repeats — over 40 ticks: 4 distinct phasors, 40 distinct states. That
is `spirale.py`'s cycle-with-a-ground applied correctly: phasor carries
the rhythm, height carries the memory, neither alone is the state. With
pitch set to zero the 40 states collapse to 4 — the memory is lost,
which is the formal reason the pitch must not be zero.

### Three corrections

1. **The pitch is not zero at `n = 0`; the *height* is.** Different
   quantities: the pitch is a property of the spiral, constant for every
   turn. A genuinely zero pitch gives `e² = 0` — a circle, and the
   ellipse the construction depends on would not exist.
2. **`n = 3` does not pull back toward the centre — it mirrors `n = 1`.**
   Both sit at squared distance exactly 2. The sequence is 0, 2, 4, 2, 0,
   so the return happens in one step at `n = 4`, not gradually.
3. **A power tower is a different object and is not 4-periodic.** `iⁿ`
   with integer `n` is exactly 4-periodic. A tower `i^i^i^…` is
   transcendental at the first step (`i^i = e^(−π/2) = 0.207879…`) and
   converges to the fixed point `0.438282936727 + 0.360592471871i`
   instead of cycling — verified as a fixed point to 2.8e-16. It needs
   roughly 500 levels to settle; at 80 it has not converged, which is
   easy to misread as a mismatch (it was, once, here). The exact
   four-cycle and the tower are alternatives, not a combination.

### One scope point

`iⁿ` lives in a single complex plane, so one cycle orders **one**
rotation plane. Three-space has exactly three
(`rotationsebenen.rotation_plane_count(3) = 3`), so ordering 3-space
with this rhythm takes three four-strokes — the complexity of the three
dimensions does not collapse into one cycle.

Three planes × four ticks = 12, and the cube also has 12 edges.
**Noted, not claimed**: both are `3 × 4`, nothing here derives either
from the other, and a test asserts that so the number cannot quietly
become evidence.

## Module: `raum27.spirale` — The Cycle That Can Actually Be Computed

Circle, spiral and circularity are three different things, and the
distinction is the whole point of this module. A **circular
definition** has no ground — `A` because `B` because `A` — and nothing
can be evaluated, because every step needs its own result as input.
That is the defect flagged elsewhere in this file. A **closed cycle**
is fine as a structure but stores no history: after one turn it cannot
tell whether you have gone round once or a thousand times. A **spiral
is a cycle with a ground** — turn `n` is computed from turn `n−1` and
never from itself, so the recursion grounds out at turn 0, while the
height records how many turns have passed. That is exactly why a
process modelled as a spiral is computable where the same process
modelled as a closed loop is not.

**The construction, and it is exact.** Unroll one turn of a helix: the
base is the circumference `B`, the rise is the pitch `h`, and the turn
is the hypotenuse — `L² = B² + h²`, Pythagoras, no `π` anywhere.
Cutting the cylinder at the helix's own angle gives a genuine ellipse,
and two statements fall out that are exact and `π`-free provided the
spiral is given by its circumference rather than its radius:

    (a/b)² = 1 + (h/B)²          e² = h²/(B² + h²)

**So the pitch alone decides the shape, and `h = 0` gives `e = 0` — a
circle.** The height is the only thing that makes it an ellipse at all,
which is precisely the claim. `a = L/(2π)` is the one place `π` enters,
and only for an absolute size rather than a ratio.

**Exactly rational when `(B, h, L)` is a Pythagorean triple:**
`(4,3,5) → e = 3/5`, `(12,5,13) → e = 5/13`, `(8,15,17) → e = 15/17`,
`(20,21,29) → e = 21/29`. For `B = h = 1`, `L² = 2` and the
eccentricity is irrational, so `turn_length` and `eccentricity` **raise
rather than round** — an earlier draft used `isqrt(2) = 1` and reported
`e = 1`, and `is_rational_spiral` exists so that cannot recur.

**What it computes.** A process given as `(circumference, pitch, turns)`
has a fully determined exact state, with a per-turn invariant that does
not drift — `L² = 25` after one turn and after a million, because the
arithmetic is rational rather than floating point. And the eccentricity
feeds `lichtgitter` directly: `e = 3/5` with `a = 25` gives integer
focal radii 16 and 34, conserved sum exactly 50, and the position
recoverable exactly from the focal difference.

    turn | height |    arc   | invariant        x  |  r1  |  r2  | r1+r2
       0 |      0 |        0 | 25                0 |  25  |  25  |  50
       1 |      3 |        5 | 25                5 |  22  |  28  |  50
       2 |      6 |       10 | 25               15 |  16  |  34  |  50
     10⁶ | 3·10⁶  |   5·10⁶  | 25            25/2  | 35/2 | 65/2 |  50

Cause to effect to the next cause, with nothing undefined and nothing
needing itself as input. That is a closed loop in the useful sense.

## Is It Workable? — The System-Level Audit

The question that matters for using this at all is not whether a number
is "true about the universe" but whether the definitions are sharp
enough to compute with and yield results within their own scope. That
is testable, and `tests/test_system_arbeitsfaehigkeit.py` tests it
rather than asserting it — because all four properties can break
silently as modules are added.

- **Closed.** Every core ratio follows from five integer primitives —
  6 faces, 8 corners, 12 edges, 4 space diagonals, 3 axes — by exact
  rational arithmetic: `4/3`, `16/9`, `3/4`, `9/16`, Euler's 2, and the
  squared diagonals 2 and 3. Nothing is smuggled in.
- **Acyclic.** 32 modules, checked mechanically by walking the import
  graph: **zero cycles**. No definition depends on itself, directly or
  through a chain — the failure mode flagged repeatedly in this file is
  verified absent rather than assumed. `cube_symmetry` imports nothing
  internal, so the primitives really are primitive.
- **Consistent.** Where independent routes meet, they agree exactly.
  `4/3` from cube counts equals `4/3` from the sphere-to-cylinder ratio,
  and nothing links those two but the answer. Euler's 2 comes out of
  three separate modules — cube counts, the octahedron, and the rhombic
  dodecahedron's 14 − 24 + 12. The rhombus diagonal ratio equals
  `face_diagonal_squared`.
- **Productive.** The definitions return things nobody put in: the
  cube's 6/12/8 out of three logarithmic axes that contained no cube,
  `8/27` as the field maximum, `29809321/160000` (= 186.31×) as a flow
  gain, a one-light-second tick count equal to `c` exactly, `26/27`,
  and the root of `6^X = 8^(10−X)` located rather than assumed.
- **68% of the typed numeric surface is exact** (102 functions returning
  `Fraction`/`int` against 49 returning `float`), and the floats sit
  exactly where measured physical constants do.

**Verdict: workable, within a stated scope.** It is an exact rational
geometry of the cube and the structures derived from it, and inside
that scope it computes and produces. What it does not do is predict
measurements — no module claims to, and the audit does not test for it.
That boundary is a scope statement, not a defect.

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