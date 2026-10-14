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

## Running It

On a clean machine:

    pip install -e ".[test]"
    pytest

781 tests as of this module set, at 100% statement coverage; all
mathematical claims in this README are verified rather than asserted.
`numpy` is the only third-party runtime dependency and `pytest` the only
test dependency — both are declared in `pyproject.toml`.

A bare `pytest` used to fail at collection with an unimportable
`raum27` package, so that only `PYTHONPATH=. python -m pytest` worked.
That was an external review finding and it is fixed:
`[tool.pytest.ini_options]` now sets `pythonpath = ["."]`, and the
package carries a `[build-system]` so the editable install above works.
Verified from a fresh virtual environment, and from a working directory
outside the repository.

### Coverage

    pip install coverage
    coverage run --source=raum27 -m pytest -q
    coverage report --show-missing

**100%, 0 uncovered statements out of 1385.**

An earlier version of this section claimed 2 statements were unreachable
by construction and deliberately left alone. **That claim was wrong, and
chasing it found two real defects** in `impakt_schwelle`. The reviewer's
question — *is the invariant guaranteed by the code, or merely suggested
by the tested examples?* — is what exposed them, and it is the right
question to ask of any such claim.

**Defect 1: the documented contract was not enforced.**
`tate_interface_velocity` promises "a root in `[0, v]`". Its acceptance
window is deliberately 1e-9 wider than that so a root sitting on a
boundary is not lost to rounding, but the return clamped only the
*lower* end. So `u` could exceed `v`, making `(v − u)` negative and the
erosion step run backwards.

Not hypothetical. A root sits exactly at `u = v` when
`0.5·ρ_t·v² + R_t − Y_p = 0`, i.e. at `v = √(2(Y_p − R_t)/ρ_t)`, which
needs rod strength above target resistance — a tungsten rod into lead.
At **v = 507.0925528366 m/s** that returned `u − v = +5.1e-10`. Fixed by
clamping both ends in the return; 0 violations across 400 000 random
parameter sets afterwards, where the previous code failed.

**Defect 2: the linear/quadratic handover was discontinuous.** The
solver switches to a linear branch when the densities are equal, and the
textbook `(−b ± √disc)/2a` lost most of its significant digits just
outside that switch: at a density difference of `1e-9` it returned
**839.68 m/s** where the linear branch and every larger difference gave
**840.764** — a **1.08 m/s step** across the handover, from catastrophic
cancellation. Replaced with the stable `q = −(b + sign(b)·√disc)/2` form
and `c/q` for the second root. The step is now **2.3e-08 m/s**, eight
orders of magnitude smaller, and the returned velocity still satisfies
the Tate balance to a relative residual of **2.7e-14** — stability was
not bought with accuracy.

**And the last statement turned out to be live code.** After the clamp,
`v = v*` gives `u = v` exactly, so erosion is exactly zero and the
zero-erosion break fires: the rod sits at the threshold and penetrates
nothing. `tate_penetration` returns exactly 0 there, while `v* + 1 m/s`
penetrates and `v* − 1 m/s` does not. So the branch was unreachable only
because the contract was unenforced, and reachable once it was.

Measuring this closed all 40 previously uncovered statements. Most were
`raise` guards documenting a contract that nothing exercised, but three
were genuine logic, now tested:

- **`tate_interface_velocity` with equal densities** takes a separate
  *linear* path, because the quadratic's leading coefficient vanishes.
  That is the most ordinary case physically — steel into steel — and was
  the one untested branch found by coverage alone: the strengthless limit
  is exactly the rod length, Tate approaches it from below, and the
  ballistic limit is 798 m/s. The two defects above sit next to it and
  were found by questioning the claim rather than by the measurement.
- `clockfree_scheduler.Schedule.average_waiting_time` had no caller.
- `kern_modul_v2.find_period` returns `-1` for a series too short to
  autocorrelate, and `FingerprintKNNPredictor` has a cold-start path and
  a pad-with-random path when voting yields fewer than six numbers.

One contract was documented wrongly in the first draft of those tests:
`basisoperationen.hole_wert` raises `KeyError`, not `ValueError`. Fixed
by reading the code rather than assuming it.

**Tested range and units**, so the claims above are reproducible: all
`impakt_schwelle` quantities are SI — densities kg/m³, strengths and
pressures Pa, velocities m/s, lengths m. The `0 ≤ u ≤ v` sweep covers
every pairing of the five tabulated materials with densities and
strengths independently scaled over `[0.2, 5]` and `[0.01, 20]`, at
velocities from 1 m/s to 30 km/s. The handover continuity check runs at
2000 m/s over density differences from 0 to 1e-6 kg/m³. Statements about
"every velocity" mean that range, not all of `ℝ`.

### Findings checked and not applicable

Three further findings from the same review were checked against this
tree and do not apply, recorded here so they are not re-raised:

- **Test count.** The review read 121 in the README against 180 passing
  in the archive it had. Both numbers are from an older snapshot; the
  line above is kept current with the suite.
- **Unsorted lottery dataset.** There is no lottery data file in this
  repository at all — `raum27/lotto_benchmark.py` takes its history as a
  function argument and reads nothing from disk, so there is no CSV to
  normalise and no loader doing it. The draw and the mean-hits figures
  the review quotes are not in this tree either.
- **`scale_selection.py`.** Listed among the modules reviewed; no such
  file exists here. Scale work lives in `scale_hierarchy.py` and
  `ifs_attractor.py`.

### What the test run does and does not establish

500 passing tests and 99% statement coverage are evidence about the
conditions tested, not about every platform or every mathematical
property. In particular, all three environments used to verify the
import fix were the **same** platform — CPython 3.11.17 on Linux
x86_64, NumPy 2.4.6 — so they establish reproducibility across working
directories and a clean virtual environment, not across Python versions
or operating systems. Statement coverage also says a line ran, not that
its behaviour is pinned down.

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



## Module: `raum27.schalenleiter` — How the Shells Are Spaced, Derived Not Chosen

A precise question was put: the reciprocal map `I(r) = 1/r` is already
exactly defined, but it **does not determine the spacing** of the shells
between the central 1 and the outer bound. Linear, logarithmic and a
ratio sequence are mathematically different — which does the model
already fix?

It already fixes it, and not by preference. The answer follows from two
laws that were already stated, with nothing new laid on top.

### Law 4 forces geometric spacing

The stated requirement is that inner and outer are one structure under
the same reference and the **same transformation rules**. So ask which
spacing *survives the inversion*:

| outer | inner | still the same kind? |
|---|---|---|
| `1, 2, 3, 4, 5` (linear) | `1, 1/2, 1/3, 1/4, 1/5` | **no** — differences `−1/2, −1/6, −1/12, −1/20` |
| `1, 8, 64, 512` (geometric) | `1, 1/8, 1/64, 1/512` | **yes** — ratio `1/8` throughout |

Checked on 4000 random ladders of each kind: **0 linear ladders stay
linear**, **every geometric ladder stays geometric**. So the spacing has
to be geometric. That is a derivation — linear spacing breaks Law 4 on
its own, before anyone argues about taste.

### And geometric spacing excludes 300 000 000

A geometric ladder from 1 to `N` in `n` steps needs `N = rⁿ` with `r`
rational, which for integer `N` means `N` is a perfect `n`-th power —
i.e. `n` divides the gcd of `N`'s prime exponents. And

    300 000 000 = 2⁸ · 3 · 5⁸,    gcd(8, 1, 8) = 1

so **300 000 000 is a perfect `n`-th power only for `n = 1`.** Candidate
ratios are all irrational: `17320.5…` for two stages, `669.43…` for
three, `11.47…` for eight, `8.75…` for nine.

**Therefore the stated outer bound is incompatible with Law 4 for more
than a single shell.** Either the bound moves, or the shells are not
exact, or inner and outer stop sharing a rule. There is no fourth
option. The same holds for the exact speed of light,
`299 792 458 = 2 · 7 · 73 · 293339`, whose exponent gcd is also 1 —
neither the round number nor the exact one carries a ladder.

The shell list submitted in code was already inconsistent with itself
here: `(1, 100, 10 000, 300 000 000)` has ratios `100, 100, 30 000`, and
three stages of a ratio-100 ladder end at `10⁶`.

### What does work — and it is already in this package

    16 777 216 = 2²⁴,    exponent gcd = 24

which is `zahlensysteme.cube_scaling_count()` *and*
`rgb_color_count()` — `8⁸` and `16⁶`, already tested equal. Because the
gcd is 24, exact ladders exist for **every stage count dividing 24**:

| stages | 1 | 2 | 3 | 4 | 6 | 8 | 12 | 24 |
|---|---|---|---|---|---|---|---|---|
| ratio | 16777216 | 4096 | 256 | 64 | 16 | **8** | 4 | 2 |

For **nine** stages the two nearest exact bounds bracket the stated one
without being it: `8⁹ = 134 217 728 = 2²⁷` and `9⁹ = 387 420 489 = 3¹⁸`.


### The indexing question decides it, and the cluster plan settles the indexing

Asked: *if we start at 1 rather than 0, can we not reach 9⁹?* Yes — and
the question turns out to be the one that matters, because whether
"nine" counts **values** or **steps** decides the top of the ladder:

| reading | top | factorisation | exact 9-stage ladder? |
|---|---|---|---|
| 9 values, ratio 8 (`k = 0…8`) | 16 777 216 | 2²⁴ | **no** |
| 9 **steps**, ratio 8 (`k = 0…9`) | 134 217 728 | **2²⁷** | **yes** |
| 9 values, ratio 9 | 43 046 721 | 3¹⁶ | no |
| 9 **steps**, ratio 9 | 387 420 489 | **3¹⁸** | **yes** |

So `9⁹` is reachable exactly; it needs ratio 9 instead of 8.

**And the decision to cluster forces the steps reading.** Repeating a
ladder whose top is `r^stages` gives boundaries `r^(stages·m) =
(r^m)^stages` — a perfect `stages`-th power for *every* `m`, so the
repetition never loses exactness. Repeating one whose top is
`r^(stages−1)` does not: for ratio 8 the boundaries would be `2^(24m)`,
and `24m` is divisible by 9 only at `m = 3, 6, …`. Verified for eight
clusters in each case.

    8⁹ clusters:  2²⁷, 2⁵⁴, 2⁸¹, 2¹⁰⁸, …   all 9-stage exact
    8⁸ clusters:  2²⁴, 2⁴⁸, 2⁷²,  …        exact only at every third

Both candidate ratios cluster consistently under the steps reading, so
**exactness does not decide between `8⁹` and `9⁹`** — that choice still
rests on other grounds. Ratio 8 has the more direct standing (it is
`corner_directions()`'s count, and `8⁸` lands on a number this package
already holds for an unrelated reason); 9 is `3²` and the modulus of
`scale_hierarchy.digital_root`.

### One tension in the navigation, worth knowing before building on it

A ratio-8 ladder holds only `2^(3k)`. So of the stated 6-bit and 8-bit
patterns:

    6 bit  =  64 = 8²    on the ratio-8 ladder
    8 bit  = 256 = 2⁸    NOT on it
    6+8 as one word = 2¹⁴   not on it either

If the navigation needs both patterns as rungs, ratio 8 cannot supply
them and a ratio-2 ladder (24 stages to 2²⁴) can — it contains every
power of two. That is a real constraint between the shell choice and the
bit-pattern choice, not a preference.


### Expansion and compression are two ladders, and that resolves the tension

The asymmetry named in the notes is exact: `x**n` reaches the unit when
the **exponent** is zero (`x**0 = 1` for every `x`), while `n**x` reaches
it when the **base** is zero (`0**0 = 1`, but `0**x = 0` for `x > 0`). So
the unit sits on a different axis in each map, and one map alone reaches
it along one axis only. That is why both are needed — the same structure
`duplex_inversion` already carries.

And it fixes the bit-pattern problem above. With ratio 8:

    A = 8**k   holds 2**(3k):   6 bit = 64 = 8²   yes    8 bit = 256   no
    B = k**8   holds k**8:      6 bit = 64        no     8 bit = 256   yes

**Together they cover both.** Neither alone does, so the navigation does
not have to choose between the shell ratio and the bit patterns — it
needs the dual pair, which the model already specified.

**Shared rungs, after two wrong guesses.** Where the ladders overlap took
three attempts and the first two are pinned as regressions:

1. *Wrong:* that the shared rungs are the `x**n = n**x` coincidences from
   `duplex_inversion`. For ratio 2 the shared rungs are `1, 4, 16, 64` —
   a whole family, not the single exceptional pair.
2. *Wrong:* that they are the powers of `r**r`. Right for 2, 3, 8 and 9,
   wrong for 4, where `16` and `4096` are shared and neither is a power
   of `256`.
3. *Derived:* `r**j = k**r` means `k = r**(j/r) = p**(a·j/r)` for
   `r = p**a`, which is an integer exactly when **`r | a·j`**. Verified
   against a direct intersection for every prime power up to 27, and the
   function reports `None` rather than guessing for a ratio that is not a
   prime power.

For ratio 8 the condition `8 | 3j` reduces to `8 | j` since
`gcd(3, 8) = 1`, so the shared rungs are the powers of `8⁸ = 2²⁴` — the
number this package already held for an unrelated reason.

### Three caveats, each pinned by a test

- **The 27 in `2²⁷` is not the project's 27.** It is forced by `8 = 2³`
  and `3·9 = 27`. Other ratios give other exponents — `4⁹ = 2¹⁸`,
  `16⁹ = 2³⁶`. Real coincidence, recorded as one.
- **The ratio 8 is a choice, not a result.** Eight being the cube's
  corner count makes it attractive, and `8⁸` landing on a number this
  package already holds for an unrelated reason is a genuine
  cross-check — but seven other ratios reach the same bound exactly.
- **This module does not say what the shells mean.** No frequency, no
  physical scale, no claim about what a transition does — same scope
  line as `zustandsmaschine`.

### One correction made while building it

`exact_ratio` first computed the root as `round(value ** (1/stages))` and
searched ±1 around it. That is a float in a module whose entire point is
exactness, and for large values its error exceeds 1, so the search was
correct by luck. Replaced with Newton's method on integers, verified
against the bracketing property `rᵈ ≤ v < (r+1)ᵈ` by brute force and
exact out to `2⁴⁰⁹⁶`. Two defensive branches that only existed to catch
the float's mistakes were then dead, and were removed rather than left
as decoration.

## Module: `raum27.pfadwort` — Reaching the Same Two Points Again, Exactly

The idea: navigate by sextants (six axis directions) and octants (eight
sign patterns), record direction changes and step lengths, and reach the
same two points on the same path every time — optimised for 6 and 8
bits, with inertia favouring straight continuation.

On the 27-cell lattice this needs no float at all. A step is one of six
directions, **3 bits** with two codes spare. A path is a word over those
six letters; replaying it from the same start reaches the same cells by
construction. The way back is the **inverse word** — reversed, each
direction flipped — and returns to the start exactly, the discrete
counterpart of the delta log in `raum27.zustandsmaschine`. Corner to
opposite corner has exactly **90** shortest paths (the multinomial
6!/(2!·2!·2!)), so choosing among them fits in 7 bits; the count formula
is checked against a breadth-first count for all 27 × 27 cell pairs.

The distinction worth keeping: **repeatability is free** — a
deterministic replay always lands on the same cells — while a bit
budget buys **accuracy** once headings are continuous. With b bits the
worst heading rounding is 1/2^(b+1) of a turn: 1/128 at 6 bits, 1/512
at 8. That error repeats identically on every replay; it moves where the
path goes, not whether it is the same path.

Measured with the submitted insect model (`raum27_insekt.py`, 10 seeds ×
12 cell pairs): pheromone plus goal direction reached the shortest path
in 0.96 ± 0.02 of runs; adding inertia 3 gave 0.95 ± 0.02 and lowered
direction changes per path from 1.41 to 1.16. **Inertia makes paths
straighter, not shorter** — useful for a turn-coded word, not for
distance.

## Module: `raum27.rueckprojektion` — Four Circles and the Negative Inside Radius 1

The picture: one circle pushes out, one presses in; eight vectors leave
the centre and return on the same path; the square's corners meet the
next circle; and the interactions, projected back through radius 1, form
the body's negative at the centre — circle 2 at 1/2, circle 3 at 1/3,
circle n at 1/n — which radiates out again unchanged.

What each part is, exactly:

- **Out and in** are multiplication by `1 + i` and by `(1 − i)/2`. Their
  product is exactly 1. Each outward step doubles the squared radius and
  advances the direction 1 → 8; eight steps give `(1 + i)⁸ = 16`, the
  carry to the next level. Turn count and direction recover the circle
  number exactly, so states are stored, not numbers. Radius 2²⁸ (circle
  56) is the last full turn below 300 million.
- **Four deltas.** From an axis point the outward delta is axial and the
  inward one diagonal; from a diagonal point it is the reverse. Outward
  deltas keep the squared length, inward ones halve it.
- **Three dimensions have a hard limit**: an integer rotation-with-scaling
  exists in 3D only for a perfect-square squared scale, since
  `det(M)² = m³`. There is no 3D `1 + i` with factor √2 or √3 (exhaustive
  search: none), while factor 3 exists. So axis → corner is built as a
  sum of unit deltas, squared length 1 → 2 → 3, and the eight octant
  vectors retrace to the centre with zero net displacement.
- **The hologram** is sphere inversion `r → 1/r`, direction kept. It is
  an involution and commutes with point reflection; the photographic
  negative (complement) is a separate involution.
- **Frequency and wavelength** are the two sides of that inversion
  (`λ = 1/f`): two frequencies meet on the surface at `lcm(f, g)`, their
  wavelengths repeat after `1/gcd(f, g)`. Checked for all f, g ≤ 60 in
  the tests (≤ 300 by hand). Frequencies 1–9 first meet together at
  2520, and adding 10 changes nothing.

Two limits stay attached. The negative carries exactly the body's
information — a bijection, no more and no less. And with equally spaced
circles 1…300 it crowds toward the centre (innermost gap 1/89 700); only
a geometric ladder, such as the `1 + i` circles, maps onto itself.

## Module: `raum27.abtastung` — Scanning Against a Stored Hologram

The procedure: store a picture of the current state (the hologram), let
only scanning impulses run through, record where they differ from the
stored state, and take a change into the internal state **only when its
pattern is recognised uniquely**; everything else — unknown or
ambiguous — goes to a second store for analysis.

A state maps `(plane, circle, direction)` to an exact value, directions
1–8 around each circle. `scan` keeps only non-zero differences, so
storage scales with what changed; `apply` and `revert` reconstruct both
ways exactly. Recognition is per circle on the eight-direction ring, up
to the ring's eight symmetries (four 90° turns, four mirrorings), so a
known pattern is recognised in any orientation. A 45° shift is *not*
one of those symmetries: the diagonal cross is not the axis cross, and
the tests pin that it is routed to analysis rather than guessed.

The saving is `1 − stored/scanned` and depends on the object, not the
method: one change in a thousand values stores 1/1000; if most values
change, deltas save nothing.

## Module: `raum27.zustandshologramm` — Wavelength Steps Recorded as 1 + 6 + 8 Bits

The step is not chosen freely: it is the wavelength, `dx = v / f`, and
each step takes the period `1 / f`. Each step is recorded under its
frequency key as a 15-bit state: 1 bit for "an impulse left a delta",
6 bits for the active sextant directions, 8 bits for the active octant
directions. The delta vector is `dx` times the sum of the active
directions, so for rational speed and integer frequency every position
is exact; an octant direction is a cube diagonal with lattice
components, and no root is computed.

Grouped by frequency the records form the hologram. Its superposition
keeps the **end point** exactly — vector addition ignores order — but
not the **path**, which needs the sequence; the tests pin both. The way
back is the records reversed with every direction mirrored, and returns
to the start exactly, here with the speed of light in mm/ms as the
rational speed.

## Module: `raum27.biegelinie` — The Bending Line From Chained Arcs, Exactly

Engineering mechanics normally gets the bending line by integrating the
curvature twice. Here the beam is cut into pieces `dx` (the wavelength
along the beam), each piece gets its own radius from mechanics —
curvature `κ = M/EI`, the frequency of the piece — and the arcs are set
end to end. Beams on two supports are started flat and turned rigidly
onto the far support; turning a chain changes no arc.

| Chain | Result against the closed forms |
|---|---|
| true circular arcs, curvature read mid-piece | error falls with 1/n² |
| same in exact rationals (small deflection) | error falls with 1/n², never exact |
| **curvature read at start, middle, end of each piece** | **exact at every piece end, for any n** |

The exactness holds whenever the curvature is a polynomial of degree ≤ 2
on each piece, which covers the cantilever (`PL³/3EI`), the centre load
(`PL³/48EI`, with a piece boundary at the load) and the uniform load
(`5qL⁴/384EI`). A kink inside a piece breaks it — boundaries belong on
the load points. Example pinned by a test: a 100 m steel bridge
(`EI = 210 GPa · 1 m⁴`, 100 kN/m) sags exactly `5qL⁴/384EI ≈ 0.620 m`
with only ten pieces.

Load duration enters as the dynamic amplification of a rectangular
pulse on an undamped oscillator: a load held at least half a natural
period, including a permanent load put on suddenly, deflects **twice**
the static value; a short impulse much less; a slowly applied permanent
load (the standing test) exactly the static value.

## Module: `raum27.verzerrung` — Six Axes Measure, Eight Corners Check

Passing the ideal sphere and cube through the ellipsoids they really
become is the strain ellipsoid of continuum mechanics: a linear
deformation `F` turns the unit sphere into an ellipsoid with squared
semi-axes equal to the eigenvalues of `C = FᵀF`, and the cube into a
parallelepiped; `det F` is the volume ratio. Everything is exact for
rational `F`.

The 6 + 8 point system splits the work cleanly. **The six axis points
determine the deformation**: half the difference of each opposite pair
is a column of `F`, and half their sum must vanish unless the centre
moved. **The eight corners then test it**: for a linear law each corner
image is the signed sum of the axis images, so it is predicted before it
is measured, and the residual is exactly what a linear law cannot
explain. The tests pin a nonlinear law (`x' = x + a·y·z`) that is
invisible on all six axes and shows up as `±a` on all eight corners.

Stretching by 4/3 and 3/4 gives squared semi-axes 16/9, 1, 9/16 and
keeps the volume exactly. When `C` is not diagonal its eigenvalues are
roots of a cubic and need not be rational; the cubic's coefficients,
the three invariants, are always exact.

## Module: `raum27.zahnwerk` — Nine Positions per Wheel, the Tenth Click Turns the Next

A spring wound on without end stores energy that grows with the square
of the turns until it tears or snaps back. The rule instead: each wheel
has nine positions and turns freely back and forth between 1 and 9; the
stop at 10 does not hold the wheel but keeps it from turning over — the
click that would reach 10 sets it back to 1 and advances the next wheel.
Going below 1 mirrors this; the two-sided rule is the **duplex trigger
condition** (`triggers`): forward from 9 or backward from 1. Ten is the spring constant, the limit no
wheel reaches; it is the escapement and gear train of a mechanical
clock.

Pinned by the tests: every click is undone exactly by the opposite
click; no wheel is ever wound more than eight clicks from rest however
long the train runs; `n` wheels hold `9ⁿ` states with all wheels at 1 as
the zero point; nine wheels (9⁹ = 387 420 489) are the first to hold
300 000 000, eight hold only 43 046 721; and turning the last wheel over
is refused, since a silent wrap would lose the count.

With the **hook zero** (`low=HOOK`) each wheel also has an inner 0: the
click that would make 10 leaves the wheel on its hook showing 0 and opens
the 1 on the next wheel to the right. Ten is still never shown; one, two,
three wheels count to 9, 99, 999 — decimal place value — and nine wheels
are again the first to hold 300 000 000.

## Module: `raum27.wuerfelgeometrie` — Why 27, Why 48, and What Views Decide

Each axis takes three states (−1, 0, +1, i.e. 0/1/2 with 1 as the
middle). Grouped by how many axes are triggered the 27 cells split as
**1 + 6 + 12 + 8** — centre, face centres (sextants), edge midpoints (the
four diagonals of each cut plane), corners (octants) — which is
(1 + 2)³ multiplied out, at squared distances 0, 1, 2, 3.

The three cut planes as mirrors give 2³ = 8 sign changes; swapping the
axes gives 3! = 6; together **48 = 8 × 6**, the full symmetry of the
cube. Element orders: 1 (×1), 2 (×19), 3 (×8), 4 (×12), 6 (×8) — **no
order 8**, so the 1–8 cycle belongs to the square in a cut plane, not to
the cube.

Rhombus : circle : square = **2 : π : 4**; octahedron : sphere : cube =
**1 : π : 6**; doubling rhombus and square pins π between them
(Archimedes). In the family |x|ᵖ + |y|ᵖ + |z|ᵖ = 1 (octahedron at p = 1,
sphere at 2, cube at ∞), duality p → p/(p − 1) swaps 1 and ∞ and has
exactly one fixed point, **p = 2: the sphere is the self-dual middle**
between the 6-system and the 8-system.

The octants as cubes: eight unit cubes stacked 2 × 2 × 2 meet exactly in
the 27 points, and each point is shared by 2^(coordinates in the middle)
cubes — the centre by all **8**, the 6 face centres by **4**, the 12
edge midpoints by **2**, the 8 outer corners by **1** (8 + 24 + 24 + 8 =
64 = 8 cubes × 8 corners). The eight octant cubes rebuild the 27-point
cube one level up: the architecture repeats itself.

Counting the cells on every line through the 3×3×3 cube, the three axis
directions alone are ambiguous — the two interpenetrating tetrahedra of
a small cube give identical counts — while the axes plus **one**
space-diagonal (octant) direction determine every one of the 2²⁷ bodies.
(One-off computation, not in the tests because it takes 20 s: with
occupied/empty silhouettes instead of counts, the three axis views give
only 1 614 530 distinct triples for 134 217 728 bodies, and three full
squares fit 10 323 979 bodies.)

## Module: `raum27.messnetz` — Spider Web, Sensor Shells, the 90° Finder, Light and Limits

**Spider web** (8 spokes, 3 rings, springs of stiffness 1/length). A
single sensor at the hub tells only which ring was touched, and it is
**exactly blind to a torn ring**: a force at the hub excites only the
symmetric motion, in which no ring thread stretches, so by reciprocity
no ring property reaches the hub. Strain gauges on the spokes at the
hub, read against a reference that removes the common part, locate
every touch point: with each thread cut into four (168 touch points,
also between knots) the four threads left, top, right, bottom separate
all 168; the closest two differ by about 0.4 % of full scale, all eight
threads give about three times that margin. **Arrival-time differences
alone separate only 16** — the information is in the ratio of forces.

**Sensor shells.** One scalar reading per sensor: the 6 axis points
resolve 6 of the 9 field terms up to second order, the 8 corners 7,
**both together all 9**; up to third order 13 of 16.

**90° without measuring an angle.** Poles at ±1: |P − N|² − |P − S|² =
−4z exactly, so equal pole distances mean the equator plane. In time,
two equal oscillations with phase gap φ have summed energy
1 − cos φ · cos(2x + φ): it stands still exactly at 90°, and its swing
2|cos φ| measures the distance from 90°.

**Light.** f·λ = c: at 300 MHz light has λ = 1 m. Red 650, green 532 and
blue 450 nm repeat together only after their lcm, 1 556 100 nm ≈ 1.56 mm;
a fibre Bragg grating shifts colour by about 0.78 × strain (1.2 nm at
0.1 % for 1550 nm).

**Limits.** 14 bits on a logarithmic scale over 100 decades give steps of
1.4 %. Erasing a bit costs at least kT ln 2 ≈ 2.9·10⁻²¹ J at 300 K; a
reversible step has no such floor. A radius from three neighbouring
noisy points gets **worse** as the points get closer (≈ noise/spacing²);
dense points help only when fitted together over a fixed arc.

## Module: `raum27.kurvenkette` — The Four-Part Sine Chain, Phases, Chain and Dome, Ball and Donut

With u = 16x/(9λ): **λ sin u** starts with slope 16/9 for every λ; its
arch midpoints all lie on one line Y = 32x/(9π) at 48.5°, 3.5° steeper
than the diagonal (exactly 45° would need π/2 in place of 16/9).
**λ sin² u** is a parabola 256/81 · x²/λ at the origin. **λ sinh u** has
the same starting slope and is the hyperbola side. **1/(λ sin u)** is the
inversion; its product with the first curve is exactly 1. For x below
about 9/16 the order is inverse > sinh > sin > sin² — "sin > sinh" is
false for every x > 0.

Six and eight positions per turn stand in frequency 4 : 3 and in energy
**(8/6)² = 16/9**, beat twice per turn and repeat after lcm(6, 8) = 24;
the two phases together tell apart only 24 of 48 pairs (one shared bit),
while coprime 8 and 9 tell apart all 72.

The hanging chain a·cosh(x/a) has arc length **a·sinh(x/a)** — the sinh
curve above with a = 9λ/16 — and inverted is the arch without bending
moment. A thin spherical dome under self-weight stays in ring compression
down to **cos φ = (√5 − 1)/2, the golden ratio**, 51.8° from the crown.
A rotation on a ball must vanish somewhere — exactly at the two poles,
the forced axis (hairy ball theorem, indices summing to 2); a torus
carries a flow with no zero. A winding on the torus with ratio 3 : 4
closes; with 1 : √2 it never closes and comes ever nearer to its start.

## Module: `raum27.gitter` — The Lattice as Carrier: Band Limit and Structure Guard

The zero point as the nucleus of a crystal: expansion is crystal growth,
compression is crystal flow — energy handed on as lattice waves, charging
every particle without dissolving the structure. For a chain of masses
`m` and springs `k`: a wave of wavenumber q has frequency
2√(k/m)·|sin(qa/2)|; **nothing above ω_max = 2√(k/m) travels** (a ring
of N masses has exactly the frequencies 2√(k/m)·|sin(πn/N)|, checked
against the eigenvalues). Driven above the band, the amplitude falls per
cell by |b| − √(b² − 1), b = 1 − mω²/(2k): the lattice reflects instead
of absorbing. The structure guard is Lindemann's criterion — a crystal
melts when its atoms swing by about a tenth of their spacing — giving
the largest energy per particle E_max = mω²(La)²/2: **the inner energy
must stay below the structure constant**, and reaching it is already too
much. Real counterparts: nucleation, phonons, dislocation glide (crystals
flow without melting), work hardening and dynamic recrystallisation (new
nuclei out of deformation); diamond has one of the highest band limits
of any solid.

## Module: `raum27.synchronsensor` — One Centre, Six on the Sphere, Eight on the Cube

The central measuring cell: a centre sensor, six on the sphere of radius
1/2 (the face centres of the unit cube) and eight on its corners at
√3/2. Every measured quantity — acceleration, inertia, any field — is
treated alike, one scalar per sensor; what is read is each outer
sensor's delta against the centre, 1 × 6 and 1 × 8, and from it a 6-bit
and an 8-bit word (bit set when the delta exceeds a threshold).

From centre and axis pairs the cell recovers the value, the gradient and
the three pure curvatures; from signed sums over the corners the three
mixed terms and the twist xyz — eleven terms, exact for rational
readings. The corners then **check** the axes: their gradient agrees
with the axes' exactly when no third-order cross term (x·y² and the
like) is present, and the difference is that term, made visible — the
six-measure, eight-check rule of `verzerrung`, now for any field.
Against a stored baseline each new frame yields only the changed
sensors, the two words and the change of every fitted term: reality read
as a stream of deltas. The 45° link: a corner projects onto each cut
plane as that plane's diagonal, squared lengths 3/4 → 1/2 → 1/4.

## Module: `raum27.verhaeltnis` — Think First, Then Compute: Show the Proportion

A module may compute with decimals if its logic has no fraction bar;
what it shows should still keep the proportion visible — `(1:3)` next to
`(1:9)` shows a factor three at a glance that `0.3333` and `0.1111` hide.
The layer finds the simplest fraction a number really is (continued
fractions, bounded denominator) and shows it only if it matches within
tolerance; an irrational number such as √2 − 1 stays a decimal and is
never dressed up as a ratio. The same principle at the level of
formulas: in λ·sin(16x/9λ) the two λ cannot be cancelled — the sine is
not a product — but writing u = x/λ and y = Y/λ turns the whole family
into the single curve y = sin(16u/9). Simplify by choosing the right
ratios first, then compute once.

**Denominator circles — look before computing.** A denominator n is a
circle of n raster points; the numerator is the position in the beat,
n/n = 1 closes the turn. Circle m lies entirely on circle n exactly when
m divides n, so a round circle mostly repeats smaller ones: circle 12
has 12 points, only 4 of them new (1/12, 5/12, 7/12, 11/12 — Euler's φ),
while a prime circle such as 11 brings 10 new points and connects
nothing. The 6- and 8-systems meet on circle 24 = lcm(6, 8); circles
1–9 together hold 28 positions. Cancelling hides which circle a point
came from, so the layer keeps it: `2/6 (circle 6) = 1/3 (circle 3)`.
Written with factored denominators, 1/(1·2), 1/(2·3), 1/(3·4), … shows
at a glance that each term is 1/n − 1/(n+1) and the sum is n/(n+1); the
innermost gap 1/89 700 of the inverted circles is 1/(299·300) — patterns
that the decimals 0.5, 0.1667, 0.0833 … and 0.0000111 keep invisible.

Nine and ten see each other as periodic: 1/9 is 0.(1) in base 10 but
0.1 in base 9; 1/10 is 0.1 in base 10 but 0.(08) in base 9. What ends in
one system repeats without end in the other — the fraction is exact in
both. On a circle 0/n and n/n are one point: k steps on circle n are
(k div n) completed turns and position k mod n, the turn counter
advancing exactly where the position falls back to zero. Joining the
side midpoints of a square gives the rhombus — the square turned by 45°
— with exactly half the area: 1, 1/2, 1/4, 1/8, … entirely rational,
with no π.

## Module: `raum27.kaskade` — Take Out the Known, Mirror, Compare, Hand Over the Rest

The automation cascade for a data stream that should not be touched by
hand but cannot be fully automated. Each sample (x, y) is first matched
against what is already known — proportional with a known factor
(y = kx), inverse proportional (y = k/x), or a ratio built only from
the circles of 2 and 3 (a 5 or 7 is a wall into another space). The same
stream then runs mirrored, (x, y) → (1/x, 1/y), which keeps each
pattern and inverts its factor. A sample is confirmed only when the
original and the mirror name exactly matching patterns; everything else
goes to the manual folder with its reason — new (fits nothing),
explained on one side only (for instance a value that follows the
*inverse* of a known factor), ambiguous (a point on two curves at once,
such as (4/3, 1) on y = (4/3)/x whose mirror lies on y = (4/3)x), or
zero (cannot be mirrored). Nothing is guessed, as in `abtastung`. In the
test stream of 300 samples with 10 % from beyond the 2–3 walls, under a
fifth reaches the manual folder, and every sample from beyond the walls
is among them.

Which mirror is used matters, and it is pinned in a table:

| mirror | y = kx becomes | y = k/x becomes |
|---|---|---|
| inversion (x, y) → (1/x, 1/y) | y = (1/k)x | y = (1/k)/x |
| 45° (x, y) → (y, x) | y = (1/k)x | **unchanged** |
| both, (x, y) → (1/y, 1/x) | **unchanged** | y = (1/k)/x |
| 90° axis (x, y) → (−x, y) | y = −kx | y = −k/x |

Every mirror applied twice gives back the sample; the 45° mirror after
the inversion turns the proportional factor back. The focal point is
literally an inversion: Newton's lens law x·x′ = f², distances from the
two focal points, with magnification −f/x — the image stands upside
down; a second lens turns it upright again, which is why a terrestrial
telescope needs an erecting lens.

## Module: `raum27.konsens` — A and B Compute, C in the Centre Checks One Value

Three-instance consensus: instances A and B do the work; the central
instance C needs a single value, because the result must close back to 1
— to C's own place in the centre. Two exact forms: an **inversion pair**
(A computes a quantity, B its inverse by its own route, C checks
a·b = 1) and a **moment balance** (A gives the weights, B where they act,
C checks that the moments about its position cancel — equal weights on
the six axis points or the eight corners balance exactly in the centre;
two screws on the diagonal of a plate balance in its middle, two on an
edge sit half a plate width off it). C accepts only an exact close and
never picks between disagreeing answers; a refusal goes to manual work.
A third form uses **plus and minus as the two sides**: A measures the
squared distance to the plus pole of each axis, B to the minus pole;
since |P − Re|² − |P + Re|² = −4R·p, each axis gives C's coordinate
exactly, (minus − plus)/(4R). One pair fixes only the plane of equal
distances — on the sphere, the equator circle; two fix a line; all three
fix the point where plus and minus meet, and C accepts only if that is
its own centre.

**The condition without which it proves nothing: A and B must be
independent.** If B is computed from A's output (B = 1/A), then a·b = 1
holds whatever A got wrong — the test pins the check closing on a wrong
answer. B must reach its value by its own route, and errors both routes
share still pass: agreement measures independence as much as
correctness (the known limit of N-version computing).

## Module: `raum27.sanftabtastung` — Gentle Inverse Probing: Wake, Do Not Push

Probing a system — an insect on the sensor cell, a crystal, anything —
through passive interaction only, with the smallest reaction that still
answers. Three exact rules: (1) **many small pulses instead of one**: a
response a in noise σ is detected with k sigmas after N repeats when
a ≥ kσ/√N, so each touch shrinks with √N while the total energy
N·a² = (kσ)² stays exactly the same — splitting lowers the disturbance
per touch, not the price of certainty; (2) **ask at the natural
frequency**: a driven oscillator answers Q times more strongly at
resonance than to a slow push and falls off fast beside it (20 % off:
below a tenth), so the drive needed drops by Q and its energy by Q²;
(3) **stay below the disturbance limit** (the Lindemann limit of
`gitter`, or an insect's reaction threshold): the plan returns the
fewest repeats keeping every response under it. Simulated with a matched
filter, the planned whisper is found in over 97 % of trials and silence
is mistaken for an answer in under 5 %.

**The alarm loop.** When the house is on fire, waking is not gentle: a
reading above a critical level drops the gentle plan for one hard pulse
— the same total budget (kσ)² in a single touch, answered after one
pulse instead of 1600, as hard as it must be. The state is binary
(quiet / alarm) with hysteresis — on above one level, off only below a
lower one — so it does not flutter at the edge.

## Module: `raum27.grenzkreis` — Guard Only the Edge, Roll Back When It Tears

If the system cannot break from inside — the 10 is out of reach — there
is no need to watch everything: one last circle around it is enough. A
state changes only by exact deltas; each step is tried against the one
boundary rule (every value strictly inside the circle). A step that
would cross it does not stand: the state stays at the last safe state
and the event records the step and **where** the circle was crossed —
reaching exactly 10 already counts. Every accepted step is undone
exactly by its inverse, so the run rewinds to its start. Two limits are
stated: guarding only the edge is complete only if every disturbance
must cross the edge (a part of real hardware can still fail inside), and
rolling back is exact for the computation and its record — physically
it means returning to a safe state, not undoing what happened.

## Module: `raum27.fundamentalbereich` — Compute One Branch, Mirror the Rest, but Only Along Real Symmetries

Checked against the summary `RAUM27_Geometrie_Resonanz_Physik.md` and the
scripts `raum27_raspi_sprachmodell.py` / `sandbox_drei_instanzen_loop.py`
of 2026-10-13.

- **Fundamental domain.** The 729 nodes around 555 fall into **35** orbits
  under the 48 cube symmetries (0 ≤ c ≤ b ≤ a ≤ 4), as the summary says.
- **The x-only modulation keeps 16 symmetries, not 8.** Under
  `berechne_vektor_ns_inversion` / `compute_vector`, x becomes
  x + c/sin(16x) and y, z stay. Because x ↦ x + c/sin(16x) is odd, flipping
  x still commutes with it. What survives is the y/z square (8) times the
  x sign flip: 16 symmetries, **75** base nodes. Only a modulation that is
  not odd leaves 8 (135 nodes). The fix is the same odd function on all
  three axes, `all_axes(f)`, which gives all 48 and 35 nodes. The same
  function, not odd, on all axes keeps only the 6 permutations.
- **The modulation is about 3·10⁻⁸ in size.** With c = 0.1·λ₂/λ₁ ≈ 9.8·10⁻⁹
  the shift is at most 3.4·10⁻⁸ (|x| = 1). In `float32` it survives only
  at |x| = 1, as one unit in the last place. At |x| = 2, 3, 4 it rounds
  away. In practice the symmetry break is a rounding-level effect.
- **Legendre.** 4ᵃ(8b+7) is never a sum of three squares. On the 1..9 grid
  this explains every missing d² up to 87. From 91 on, the grid edge
  (|Δ| ≤ 8) is the cause.
- **27 ideal points**, d² = 0 / 16 / 32 / 48 (counts 1, 6, 12, 8). The
  three touching spheres of the unit cube have r² = 1/4 : 2/4 : 3/4.
- **Two coupled 3D systems** have 1458 states, one 6D search has 531 441.
  The ratio is exactly 729/2.
- **Sieve.** The octahedron table checks out (68.2 / 29.7 / 8.8 / 2.3 /
  1.05 / 0.6 % at 1, 2, 4, 8, 12, 16 divisions). The 1 % stop is first
  crossed at 13, not 12. The polygon row (36.3 % rhombus … 0.04 % 128-gon)
  also checks out: 1 % is passed at the 32-gon and the reserve
  1 − σ = 103771/150000000 ≈ 0.069 % at the 128-gon. σ = 149896229/150000000.
- **Sum line of the sandbox.** d0 + d2 = 24 for **every** node, so
  "24/24 = 1" is an identity and carries no information. The split's
  rest ±1/24 (±7/960 in frequency) depends only on the digit sum mod 3:
  243 nodes have rest 0, 243 have +1/24, 243 have −1/24. It is a
  property of the grid position, not of the data.
- **Digit cycle 1-2-4-8-7-5** (2ᵏ mod 9) has two mirrors. Additively,
  k and k+3 sum to 9. Multiplicatively, k and 6−k give a product of 1 mod 9.
  The plain product of all six is 8, not 1.
- **Stern-Brocot.** `stern_brocot_path(16/9) = "RLRRRL"`, and 9/16 is the
  same path with L and R swapped (inversion = mirror). `from_path` builds
  the fraction back with additions only.

## Module: `raum27.wandtensor` — The Wall Tensor Is the Exact Step for Linear Curvature

From `raum27_wandneigung_tensor.py`, checked in exact fractions. T(DX) =
[[2/6 DX², 1/6 DX²], [1/2 DX, 1/2 DX]] acting on (f_start, f_end) is the
exact step of a bending line whose curvature is linear on the piece:
w' = w + DX·θ + DX²(2f₀ + f₁)/6, θ' = θ + DX(f₀ + f₁)/2. det T = DX³/12
(1/6144 at DX = 1/8), so two successive states give both curvatures back.

- **Cantilever with end load** (linear curvature): error **0** at all 8 nodes.
- **Uniform load** (quadratic curvature): error **1/7680** at the end with
  8 pieces. The middle reading of `biegelinie.three_point_chain` makes it 0.
  "Random error off" holds for linear curvature only.
- **Nine fractions 1 − k/9** as a ramp with DX = 1/9: the denominators run
  2187, 2187, 81, 2187, 2187, 81, 2187, 2187, 3, and w ends at exactly 1/3.
- **Left out:** the "zero-layer contact contract". Built from the tensor,
  its condition holds by algebra for every input. It is part of the trust
  layer, which waits for the first trial run.

Also checked from the same folder: in `holomorphic_wand_tensor.py`, the coupled
energy ratio is k/m for every state, not a measurement. The quadrant labels
Y1 … Y4 are shifted by 90°: "Y1 = 90°" is still unrotated. In
`raum27_pendel_fraktal_bruchnetz.py`, the digit roots of 2ᵏ (1-2-4-8-7-5)
and 5ᵏ (the same cycle backwards) multiply to digit root 1 on every
step, because 2ᵏ·5ᵏ = 10ᵏ (`fundamentalbereich.outer_inner_mirror`).

## Module: `raum27.sprachprotokoll` — Six Channels, a 6-Bit Change Mask, ΔX Leading

The six cube faces are six channels: concept, relation, grammar, event,
prosody and control. A frame is a 6-bit **change mask** followed by a
4-bit value for each changed channel. Unchanged channels keep their
current state. `000000` is a complete frame and means "nothing changed".

- **Exact cost:** 6 + 4k bits for k changed channels, against 24 for six
  fixed fields. The mask wins for k ≤ 4 (22 bits at most) and loses for
  k = 5 (26) and k = 6 (30). If each channel changes with probability p,
  the mean is 6 + 24p, so it pays off exactly when p < 3/4. At 1.5 changed
  channels per step (p = 1/4) the mean is 12 bits.
- **ΔT = ΔX / v**, with v fixed per medium and at most 3·10⁸ m/s. 33 m of
  sound at 330 m/s is exactly 1/10 s. Processing time is a separate value
  per agent (comfort band 200–500 ms) and is never derived from ΔX.
- **Synchronising to the slower side** is one-way: the faster answer is
  buffered by the difference, and the slower one cannot be sped up.
  Control traffic uses prediction (x + v·latency) instead of delay.
- **Open:** 16 values per channel is far too few for real vocabulary. The
  shared dictionary, references and the benchmark against UTF-8 on real
  sentences are still missing. The integrity witness C′ (hash comparison)
  waits, with the rest of the trust layer, for the first trial run.

## Module: `raum27.zeitachse` — Time as a Path: What a T Axis Adds and What It Does Not

Checked against the idea "X = Y² = Z³ = T⁴ in the cube, the sphere
expanding from the centre, time read off the four space diagonals, six
diagrams".

- **Six diagrams.** Four axes x, y, z, t give C(4,2) = 6 planes: XY, XZ,
  XT, YZ, YT, ZT. The list as dictated had XT twice and no YZ.
- **The four diagonals carry one number.** A sphere expanding from the
  centre cuts all four space diagonals at the same distance (coordinate²
  = R/3), so the four readings are a single scale parameter. This is
  the existing rule: time is the index of the shells, not a direction
  inside one (`kugelkoordinaten`, `viertakt`).
- **Roots come back exactly only on perfect powers.** a, a², a³, a⁴ all
  return to a, but 2^(1/4) is not a fraction. The square already removes
  the roots: (√2)² = 2, (√3)² = 3. The 4th power (4 and 9) adds nothing
  exact, and that 9 = (√3)⁴ coincides with 8·1/9 + 1/9 = 1 is
  arithmetic, not a derivation.
- **What a real fourth axis adds, exactly.** The unit 4-cube has
  diagonal √4 = 2, which is rational (only dimensions 1, 4, 9, 16 … give
  rational diagonals). Every natural number is a sum of four squares
  (Lagrange), so the 3D gaps 4ᵃ(8b+7) close. The 4-cube has 16 corners,
  32 edges, 24 squares and 8 cubes.
- **Physics has the opposite sign.** s² = x² + y² + z² − (ct)², which is 0
  on a light ray. A Euclidean t axis is a modelling choice.
- **The sphere can rotate, and then the diagonals do say more.** A bare
  sphere looks the same however it turns, so rotation alone changes no
  reading. A sphere with a **mark** does. The mark's cos² to the four
  diagonals gives four different values that always add up to exactly
  4/3: four readings, three unknowns, one built-in check (the
  6-measure / 8-check pattern again). The rotation itself takes four
  numbers, a quaternion (a, b, c, d), whose norm a² + b² + c² + d² is a
  sum of four squares. That is where the fourth axis really sits. With
  integer a, b, c, d the rotation matrix consists of fractions and the
  turn stays exact (e.g. (3, 1, 2, 0), norm 14). (1, 1, 1, 1) is the
  120° turn about a space diagonal: x → y → z.
- **Moving time into the path does not escape time dilation.** Between
  two systems in relative motion the path contracts by the same factor γ
  by which time stretches. At v = 3/5 c, γ = 5/4 exactly: a clock at rest
  shows 5/4 there, and a rod of length 1 measures 4/5. What is the same
  for every system is the **interval** s² = x² − (ct)², a square and exact
  in fractions. That is the real shared quantity. γ is a fraction only for
  speeds from Pythagorean triples (3/5, 4/5, 5/13 …); at v = c/2 it
  contains √3.
- **Halving the number is endless, halving a thread is not.** L/2ⁿ is
  exact for every n, and the halves add up to L again. A real thread
  folded n times is 2ⁿ strands of length L/2ⁿ. It becomes as thick as it
  is long when 4ⁿ ≥ L/d: after 15 folds for 1 m at 1 nm thickness, after
  5 at 1 mm. The model therefore halves the number, not the thread.
- **Direct line versus relays.** Through n relays a message arrives
  unchanged with probability (1 − p)ⁿ: 0.976 for 24 relays at p = 1/1000,
  even if every relay checks its own hand-over. Only a check between the
  two ends covers the whole way (the end-to-end argument). The check
  itself belongs to the trust layer and waits for the first trial run.

## Module: `raum27.nennerordnung` — Compare Patterns First, Compute Last

- **Every root is a power with a fractional exponent.** Anything built
  by multiplying, dividing and taking roots is a product of primes with
  rational exponents (√2 = 2^(1/2), √12 = 2·3^(1/2)), and that form is
  unique. Equality is exact: √2·√8 = 2^(1/2 + 3/2) = 4. Order is exact
  too, without evaluating a decimal: raise both sides to the lcm of the
  exponent denominators. √2 < ∛3 because 2³ = 8 < 9 = 3². **Limit:** a sum
  of different roots (√2 + √3) has no such form and stays an open
  expression.
- **Every ratio is kept as Z1 : Z2.** On the common denominator the
  numerators compare directly (1:3, 2:6, 1:4, 3:4, 5:12 over 12 →
  4, 4, 3, 9, 5). Grouped by the reduced denominator, each ratio sits on
  its circle, and 1:3 and 2:6 stay as two origins of one point. That
  gives **two** orderings, not one: which circle (the denominator, i.e.
  the resolution) and where on it (the numerator, i.e. the position).
- **Units out, then time out.** A length over a reference length is a
  pure ratio. Inside, time is kept as a path s = v·t, and only the output
  turns it back with the output speed: t = s / v_out.
- **Every world in its own unit.** Nano world in nm, micro world in µm,
  our world in m, the large world in km and light-paths. A unit is only
  the denominator 10^(3k): the number stays between 1 and 1000, and the
  conversion is exact both ways (Earth–Moon 384 400 000 m = 384.4 Mm,
  light time 3844/3000 s in the model). Exactness matters across the
  scales: one light-year plus one nanometre loses the nanometre in a
  float and keeps it as a fraction. Time stays system-dependent: in each
  world it follows the path with that world's speed. Changing the unit
  changes the numbers, not the physics; quantum effects at the nanometre
  are a different law, not a different unit.
- **The smallest point is a denominator.** The resolution is the circle
  N, so the smallest distinguishable point is 1/N. Below it a value
  counts as 0. That makes "1/∞ = 0" a rule of the grid, not of
  arithmetic. The rest is carried, not dropped: twenty values of 1/20 on
  the grid of ninths each show 0 and would lose 1 in total if dropped,
  while carried they sum exactly to 1. Physically the zero-point
  oscillation of a crystal never vanishes; the goal is to make it as
  small as the resolution, not zero.

## Module: `raum27.schallgrenze` — Stiffness Over Density, Expansion Mirrored by Compression

c_s² = K/ρ: stiffness over density, not density alone. Water ≈ 1483 m/s,
lead (dense) ≈ 2 km/s, diamond (3.5 × water) > 10 km/s. For c_s = c the
stiffness would have to be K = ρc², for water about 4.1·10¹⁰ times its real
value. This is the continuum form of the lattice band limit in `gitter`.

The idea "keep the amount, expand the space, keep the stiffness, mirror
the path as x ↔ 1/x" in exact squares:

- c_exp² = K·x³/ρ₀ and c_comp² = K/(ρ₀x³). Their **product is (K/ρ₀)² for
  every x**: the two speeds mirror each other around c₀ like x and 1/x
  around 1 (`rueckprojektion`, `schalenleiter`).
- **The light limit caps the expansion.** With K held fixed, c_exp grows
  like x^(3/2) and would pass c at a linear factor of 3446 for water.
  "The wave speed stays stable and below the limit" therefore does not
  follow; the cap c_s ≤ c has to be imposed as the outer boundary circle
  (`grenzkreis`).
- **Keeping the pressure while expanding costs work** p·ΔV (1 bar, volume
  × 8: 700 kJ per m³ of start volume). It is paid from inside, which is
  the main condition E_inner ≥ E_outer, now with a number.
- **A real gas does not do this by itself.** At fixed temperature K = γp
  falls with ρ and c_s stays the same.

## Module: `raum27.stapelplan` — The Batch Cascade Between Agents

Stage i needs wᵢ hours per full batch (e.g. 10 000 sheets) with mᵢ
parallel instances. Split into k equal parts, the chain is a flow line:
tᵢ = wᵢ/(mᵢk) and makespan = Σtᵢ + (k − 1)·max tᵢ, exactly.

- **One whole batch through five 4 h stages takes 20 h** (N·Δ). Split into
  4 parts it takes 8 h, into 10 parts 5.6 h. The next stage starts as soon
  as the first part is ready.
- **The slowest stage sets the pace.** Steady state is one batch every
  max(wᵢ/mᵢ). A second instance helps only at the bottleneck: an 8 h
  stage with 2 instances brings the chain back to 4 h per batch; a second
  instance anywhere else gains nothing.
- **Wake intervals cost time.** Agents that wake on their own schedule
  add up to one wake interval per hand-over unless their wake times are
  staggered (8 h → 12 h for 4 parts with hourly wakes). A part shorter
  than the wake interval only waits, so with hourly wakes and 4 h stages
  k ≤ 4. A continuously running runner can split much finer.
- 10 000 sheets in 4 h is 1.44 s per sheet.

## Module: `raum27.eckenruecklauf` — The Corner Is the Ten That Is Never Reached

Cube edge a = 9: inner sphere radius a/2 = 9/2 (the proportionality factor
of the first cube), touching spheres r² = 81/4, 81/2 and 243/4 (1 : 2 : 3).
The corner lies on the outer sphere and is the 10.

- **From sphere to cube without a corner.** The p-ball |x|ᵖ+|y|ᵖ+|z|ᵖ = rᵖ
  touches every face at r for every p and reaches along a diagonal to
  r·3^(1/2 − 1/p). That is r at p = 2 (the sphere) and r/√3 at p = 1 (the
  octahedron). It approaches r·√3, the corner, only as p → ∞. The order is
  checked exactly with fractional exponents (`nennerordnung`). For every
  finite p the corner is rounded. A corner radius of 0, the sharp 90°
  where a real structure cracks, is refused.
- **Approaching without arriving.** After n pushes, each covering the
  share 1 − q of what is left, the rest is gap·qⁿ. It is never 0, and
  the pushes never add up to more than the gap.
- **The return comes out of the corner.** Reflection on three
  perpendicular faces turns every direction v into −v: the corner
  reflector, as on the Moon. On the grid this is the opposite pole
  d → 10 − d (XYZ + opposite = 1110). Whatever is sent toward a corner
  comes straight back.
- **Fixed by Thomas: 9/2 is the scaled proportionality factor.** The
  distance from axis to axis is 9. Seen from the centre that is 9/2,
  taken as a magnitude ("without minus"), and squared it scales as 81/4.
  With four axes X, Y, Z, T drawn as the tetrahedral directions
  (alternate cube corners, summing to 0), a point at the corner
  (9/2, 9/2, 9/2) reads 27/2 on its own axis and −9/2 on each of the
  three others. The readings add up to 0, and their squares to 4·|v|² =
  243 (the built-in check of `zeitachse`). Without sign, every other
  axis shows exactly 9/2. A spiral that grows toward this limit reads
  9/2·(1 − qⁿ) at its axis hits (9/4, 27/8, 63/16 … for q = 1/2). It
  approaches 9/2 and does not pass it.
- **The spiral turns about a space diagonal.** Seen along (1, 1, 1), the
  six face directions (up, down, left, right, front, back) form a regular
  hexagon, so the spiral meets one of them every 60°. Each face centre
  stays at 9/2 from the centre: 81/4 = 27/4 along the axis + 27/2 across
  it. The cube symmetries that keep this axis in place are exactly the 6
  permutations of the coordinate axes, i.e. the 6 orders of XY, XZ, XT
  (XY·XZ·XT, XY·XT·XZ, XZ·XY·XT, XZ·XT·XY, XT·XY·XZ, XT·XZ·XY). Up and
  down lie on one axis line and therefore share one plane.
- **The balance that can spin.** Stopped, it weighs (statics, `waage`).
  Spinning, every imbalance shows as a pull m·ω²·r: twice the speed gives
  four times the pull, and a centred mass gives none at any speed. Fast
  spinning does not make an unbalanced body symmetric. It only looks
  symmetric to a slow eye, and mechanically it shakes harder. What it
  does give is a stiff axis (gyroscope). The RAUM27 point sets themselves
  have an isotropic inertia tensor: the 8 corners, the 6 faces, the full
  27, the 4 tetrahedron corners and 1+6+8. About every axis through the
  centre they turn like a sphere. One extra mass breaks this.

## Module: `raum27.zustandsmaschine` — Two Submitted Cores, and What Survived

Two versions of a rational state machine arrived: the first presented as
*"mathematisch unangreifbar"*, the second a critique of it offered as the
better core. **Both run, both pass their own tests, and both have
defects their tests do not reach.** The critique's own distinction is
what found them, including in the critique itself: *a test that confirms
an invariant and a proof that it holds for all admissible inputs are
different things.*

### What the first version got wrong

- **`invertiere()` returned a cached copy of the predecessor**, not a
  reconstruction. Shown by replacing the successor with nonsense
  (`ebene=99, h=10⁹`) — it still returned the correct predecessor. A
  function that answers correctly regardless of what the forward step did
  cannot establish reversibility.
- **Binary floats were accepted silently.** `schritt(0.1, 0)` stored
  `3602879701896397/36028797018963968`, which is not `1/10`. The
  arithmetic stays formally exact and becomes substantively worthless.
- **The revolution count vanished from the state's own output.** Two
  states two full turns apart gave identical `als_tripel()`.

### What the critique got wrong

- **Its runtime consistency checks are tautologies.** `schritt` asserts
  `rueckwaerts(vorwaerts(s)) == s`, but one adds and the other subtracts
  the same exact `Fraction`s. Across **188 865 valid random cases the
  assertion fired 0 times** — it cannot fire. That is precisely the
  objection the critique raised against the cached `invertiere()`, one
  level up: it looks like a safety net and proves nothing at runtime. The
  statement is a theorem about `Fraction` arithmetic, and belongs in a
  property test, not an `assert` in the hot path.
- **A delta is never checked against its context.** A delta recorded at
  the origin, applied to `(100, 100)`, returned `(shell=1, 101, 103)`
  with no complaint.
- **A delta is not a function of its arguments alone.** At the top shell
  an ascent is silently demoted, so the same `(dn, dh)` gives `de = +1`
  with four shells and `de = 0` with one. Replay is defined only from the
  exact originating state — which the critique's round-trip test happens
  to satisfy without saying so.
- **The float ban has a hole.** `rational()` rejects `float` and
  `numpy.float64` but accepts `Decimal` and `str` unchecked, so
  `Decimal(0.1)` — built from a float — smuggles the binary fraction
  straight through.

### What the threshold actually is

Both kept `e² = dh²/(dn² + dh²) > 1/2`. That is exactly `dh > dn`:

    e² > 1/2  ⟺  2dh² > dn² + dh²  ⟺  dh² > dn²  ⟺  dh > dn

**300 000 exact random pairs, 0 disagreements.** So the eccentricity form
is not a metric doing hidden work — it is the comparison "climbs more
than it turns", and this module says so in the function name. It does
have an exact geometric reading, though: this `e²` *is*
`spirale.eccentricity_squared(dn, dh)`, so the threshold means the
helix's pitch exceeds its circumference — the climb angle passing 45°.
Cross-checked against that module, and at exactly 45° the threshold is
correctly *not* crossed.

### What this module does differently

- **Only exact inputs.** `int` and `Fraction`; everything else refused
  with a message to convert explicitly. No digit-count heuristic, which
  would only move the hole.
- **A real inverse plus a check that can fail.** The predecessor is
  *recomputed* from the successor, and the delta carries the state it was
  recorded from so misapplication is detected instead of silently
  returning a wrong answer. The tautological assertion is gone.
- **Saturation is recorded, not swallowed** — a denied ascent says so.
- **The theorem is a property test** over 20 000 random transitions,
  where it belongs.

### What is still not established

The shell index is bookkeeping. No frequency, scale factor or physical
meaning is attached, because none has been derived — attaching one would
be the unsupported extra assumption the critique rightly warned about.
Reversibility is a property of the **delta log**, not of the state
sequence: different histories reach the same state, so the log carries
the difference. And nothing here compresses data, establishes consensus,
or touches cryptography.

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

## Thesis Model — The Whole Chain in One Line of Thought

Status marks: **[checked]** computed and pinned by tests; **[set]** a
modelling rule chosen, not derived; **[open]** not yet decided or shown.

1. **Structure first.** Each axis has three states; three axes give the
   27 cells, 1 + 6 + 12 + 8 at squared distances 0–3. Reflection gives 8,
   axis exchange 6, together the 48 symmetries. [checked —
   `wuerfelgeometrie`]
2. **Six measure, eight check.** The six axis points determine a linear
   deformation; the eight corners predict themselves and expose what is
   nonlinear; as sensors, 6 + 8 together resolve a field fully to second
   order where neither alone does. [checked — `verzerrung`, `messnetz`]
3. **The sphere is the middle.** Octahedron (6) inside, cube (8)
   outside, sphere the self-dual fixed point between them; 1 : π : 6.
   [checked — `wuerfelgeometrie`]
4. **Inversion at radius 1 is the negative.** r → 1/r, an exact
   involution; frequency ↔ wavelength swap lcm and gcd; only a geometric
   ladder maps onto itself; 0 and ∞ are the poles of the number sphere.
   [checked — `schalenleiter`, `rueckprojektion`]
5. **Bounded wheels, unbounded count.** Nine positions per wheel, the
   tenth click turns the next (duplex trigger; hook zero gives 9, 99,
   999); every click reversible; nine wheels hold 300 000 000. [checked —
   `zahnwerk`]
6. **States, not numbers.** A path is a word; a step is a wavelength
   dx = v/f recorded as 1 + 6 + 8 bits; a scan stores only deltas
   against the hologram and takes over only unique patterns. [checked —
   `pfadwort`, `zustandshologramm`, `abtastung`]
7. **Arcs instead of corners.** The bending line from chained arcs is
   exact at every node with three readings per piece. [checked —
   `biegelinie`]
8. **Measurement lives in ratios.** A hub reads the web only through
   several threads against a reference; 90° is found from equal pole
   distances or a still energy sum; the central cell of 1 + 6 + 8 sensors
   reads any field to second order and checks it. [checked — `messnetz`,
   `synchronsensor`]
9. **The lattice carries, below its limits.** Energy travels as lattice
   waves up to ω_max and stays crystalline below the Lindemann energy.
   [checked — `gitter`]
10. **The main condition.** E_inner ≥ E_outer: energy leaves the zero
    outward and returns only as field compression; lasting states need
    equality on average; the energy layer is one-way while the
    information layer stays reversible. [set — README "Main Condition"]
11. **Each part does its own job; supervision is passive, intervention
    only in emergencies.** Agents compute on their own beat; a centre
    checks one value; the stream is read as deltas against a hologram
    without touching it; probing is a whisper at the natural frequency;
    a binary alarm with hysteresis acts only above a critical level, and
    whatever the system will not do it says, never silently. Data and
    computation then scale with what changes, not with what exists.
    [set — `abtastung`, `kaskade`, `konsens`, `sanftabtastung`]
12. **Physical identities** (one drive for strong force and gravity,
    big bang as inversion, the field constant that closes from below,
    the frequency's own 6/8 pattern). [open — README "Open Questions"]

What the chain claims and what it does not is therefore visible at a
glance: items 1–9 are mathematics and engineering that hold, 10 and 11 are the
rules the model adds, 12 is where it would have to meet experiment.

## Main Condition (Set, Not Derived): The Inner Source Is Never Smaller

Stated as the governing rule of the model: **E_inner ≥ E_outer.** The
zero point is not empty but the reservoir of potential energy. Energy
leaves it outward and spreads through the spheres; it never returns into
the zero linearly, only through the field, as pressure that compresses
the zero further (the crystal folding further). E_inner > E_outer is
expansion, E_inner = E_outer is the standing state (state 1); E_outer >
E_inner would crush the resonator.

What follows from it, checked against conservation of energy:

- In a closed system the strict inequality can only hold for a while:
  if energy leaves and nothing returns, the source runs down. A lasting
  state needs the outward flow to be paid back as compression work, i.e.
  **equality on average** — the rule then fixes the *direction* of the
  flow (from inside out), not a permanent surplus.
- This is how a star works: the core is the denser, hotter reservoir,
  energy flows only outward as radiation, gravity — a field — presses
  back as compression, and when the fuel is spent the compression goes
  on: carbon crystallises in white-dwarf cores (see the diamond entry
  under "Refuted"). Outer pressure exceeding inner support is core
  collapse.
- One-way flow from hot to cold is irreversible (second law). The
  model therefore has two layers that must not be confused: the
  **information layer** (gear train, delta log) is exactly reversible;
  the **energy layer** under this condition is one-way.

Status: a modelling axiom with a clear physical counterpart, not a
derivation. Proposed reading (`schallgrenze`, set, not derived): the field
constant that "closes from below" is the stiffness K, which is held
fixed. The work to hold it while the space grows is p·ΔV, paid from
inside. The compression is measured by the sound speed itself:
c_comp²/c₀² = 1/x³. Still open: whether a real medium can hold K fixed
this way. A gas at fixed temperature does not.

## Refuted — Claims That Were Checked and Do Not Hold

Kept on purpose: a refutation is a result. Each entry names the check.

- **"c^c" as a physical bound.** c carries a unit; c^c has about 2.5·10⁹
  digits in m/s and 1.6·10⁶ in km/s. A number that depends on the unit
  is not a property of nature. In the system's own units c = 1.
- **"∞ · 0 = 1" as arithmetic.** n·(1/n) = 1 but 2n·(1/n) = 2 and
  n²·(1/n) → ∞. It holds only as the pairing of a quantity with its own
  inverse across radius 1 — which is the Riemann sphere, 0 and ∞ as poles.
- **The forwarded "TensorBendingEngine".** Its path radius is always 1
  whatever the bending radius; the turn per step grows (0.2, 0.3, 0.4…)
  because the accumulated phase is reapplied; "XT" grows without bound
  (1888 after 2000 steps at r = 300); one step forward and back does not
  return; a million states need at least 15.6 MB, not 8.5 KiB.
- **"A diamond pressed at the Earth's centre cannot be destroyed on
  Earth."** Hydrostatic pressure tests only the spherical part of stress;
  diamond fails by shear and cleavage (a blade and a hammer split it
  along its octahedral planes), burns in air near 700 °C and is laser-cut
  routinely. Its lattice also stores no energy on decompression.
- **"Destructive interference raises the inner energy."** Two equal
  waves give 2I₀(1 + cos φ): zero where they cancel, 4I₀ where they add,
  2I₀ on average — energy is moved, not created. In a standing wave the
  node of one form is the antinode of the other (E vs B, displacement vs
  strain), and sin² + cos² = 1 keeps the time-averaged energy the same
  everywhere. What does build up is in-phase driving (resonance).
- **"Scaling to the largest energy removes shear."** Shear depends on
  the direction of a load relative to the axes, not on its size; it
  vanishes in the principal axes of each load, which turn with the load.
- **"The smaller the points, the more exact the radius."** True without
  noise; with noise σ a radius from neighbouring points errs by about
  σ/spacing² (0.0006 at spacing 0.5, 0.63 at 0.01).
- **"dx proportional to the bending radius is more accurate."** At equal
  piece count it was worse than equal pieces (6·10⁻⁵ vs 2·10⁻⁷ at 200
  pieces on a kinked line): an arc is exact for constant radius, the
  error comes from the radius changing inside a piece.
- **"sin > sinh"** in the submitted chain of curves: false for all x > 0.
- **"A single hub sensor reads the whole web."** It reads only the ring
  and is exactly blind to a torn ring (`messnetz`).
- **"Three views determine a body."** They do not (`wuerfelgeometrie`).
- **"The period of a reversible 2²⁶-state system cannot exceed 2²⁶."**
  True for one trajectory; the whole system returns only after the lcm of
  its cycles, which can be far larger (cycles 2, 3, 5, 7, 11, 13 on 41
  states return together after 30 030 steps).
- **"A 1-bit seed unfolds into infinite information."** A function of one
  bit has at most two outputs; an 8748-byte buffer has finitely many
  states.
- **The 10-minute hardware report.** 26 155 062 vectors in 600.01 s is
  43 591/s, not 43 732; 235 ns per vector and 48.69 MiB/s disagree with
  that rate by about a factor of 100; "60 minutes stable, verified" was
  written while the run was still going; "temperature-stable" with no
  temperature data.
- **"Only the y/z symmetries (factor 8) remain under the x-only
  modulation."** The modulation is odd in x, so the x sign flip survives
  as well: 16 symmetries, 75 base nodes (`fundamentalbereich`).
- **"The sum line d0 + d2 = 24/24 decides per node."** It equals 24 for
  every node. The rest ±1/24 comes from the digit sum mod 3, i.e. from
  the grid, not from the data (`fundamentalbereich`).
- **"Constant stiffness with mirrored expansion keeps the wave speed
  stable below the limit."** The product of the two speeds is fixed, but
  the expanding side grows like x^(3/2) and passes c at x = 3446 for
  water (`schallgrenze`). The limit must be imposed, it does not follow.
- **B3 / B4 resonance code.** Phases averaged arithmetically, not on the
  circle (359° and 1° average to 180°); `mirror_phases` never used;
  `route_signal` is a linear scan, not O(1).

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
6. **`raum27_flug.py`** — imported by both flight scripts in Drive
   (`raum27 flug pruefung.py`, `raum27 flug stapel.py`) but not supplied.
   Until it is, the flight claims (702 flights, return error 1.3·10⁻¹³)
   cannot be reproduced.
7. **The 60-minute hardware run** — to be evaluated neutrally once its
   results are uploaded (Drive folder "Anti Gravity").
8. **Which 6- and 8-bit pattern a frequency carries**, and the rule by
   which an impulse leaves an interaction point on a circle. The modules
   accept any pattern; the rule itself has not been stated.
9. **Physical readings of the geometry**: that strong force and gravity
   share one drive, that the inversion of the largest space is the big
   bang or a multiverse, that a crystal "folds" pressure energy, and the
   meaning of "Hyperraum 27". None is derived or tested here; the
   geometry stands without them.
10. **The inner counter-rotation** that is to stabilise the system:
    whether a co-rotating gyroscope (stiffens the axis) or a
    counter-rotating pair (cancels angular momentum) is meant decides the
    design; the intermediate axis of rotation is unstable either way.
11. **"Time as much as space" on the equatorial torus**: equal volume,
    surface or diameter? A torus as wide as the sphere with a closed hole
    holds only about 59 % of the sphere's volume.
12. **The reading "3 × 4 = 12 − 3 = 9"**: the nine cells of a cut plane,
    or the twelve edge midpoints? Not fixed yet.
13. **The 6/8 coupling through "λ sin(16x/9λ)" as physics**: the curves
    are analysed in `kurvenkette`; what physical quantity λ and Y are has
    not been fixed.
14. **The erkenntnis grid** (knowledge X, causality Y, intuition Z on
    the levels 1/q, 1, q; intuition proposes, X and Y decide): agreed in
    principle, not yet built.
15. **The chained delta log ("blockchain") and lockstep synchronisation**
    are held back on purpose until a first trial run has shown they work
    as intended: trust in that layer must not rest on an untested draft.
    The draft (hash-chained deltas, lockstep replay in exact fractions,
    invertible world maps) is kept in the git history (commit "synchronlog:
    chained delta log, lockstep replay, worlds that map back") and can be
    restored from there.
16. **Sandbox three-instance loop as a whole run.** The three modules it
    imports were found (13.10.) and checked (`wandtensor`; see there for the
    holomorphic tensor and the fraction net). The loop itself needs numpy
    and the language-model file and has not been run here.
17. **Octahedron/polygon sieve as a stepping procedure on data**, and
    **pulsar timing data** as a test bed: the numbers are checked
    (`fundamentalbereich`), the run on data is not done.
18. **Comparison with the local code base (Antigravity, 14.10.).**
    Taken over: the inner rotation is a counter-rotating pair with net
    angular momentum 0. The torus is equal in volume to the sphere; with
    a closed hole its tube radius is then R·(2/(3π))^(1/3) ≈ 0.596 R and its
    outer radius ≈ 1.19 R. Still to resolve:
    - "12 − 3 = 9" as nine planes XY … XC needs ten axes, not four.
    - Y = λ·sin(16x/(9λ)) has period (9/8)·π·λ, not λ.
    - A dictionary of 729 entries needs at least 10 bits, not 4.
    - E·I (N·m²) is not the compression modulus K (Pa), and bending
      waves are dispersive.
    The nesting factor (4/3, 9/8 or 9/2) and q (3 or 9/2) are not decided.
    Details in Drive: `RAUM27_Abgleich_9_Fragen_2026-10-14.md`.
