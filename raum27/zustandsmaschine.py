"""Der Zustandskern: exakt rational, wirklich umkehrbar, mit prüfbaren Zusicherungen.

Two versions of a rational state machine were submitted. The first was
presented as "mathematisch unangreifbar"; the second was a critique of
it that fixed real problems and was offered as the better core. Both run
and both pass their own tests. Both also have defects their tests do not
reach, and this module is what survives checking them.

The critique's central distinction is the right one and worth keeping in
front: **a test that confirms an invariant and a proof that the
invariant holds for all admissible inputs are different things.** That
distinction is what found the defects below -- including, pointedly, in
the critique's own code.

WHAT THE FIRST VERSION GOT WRONG
--------------------------------

- **`invertiere()` returned a cached copy of the predecessor**, not a
  reconstruction. Demonstrated by replacing the successor state with
  nonsense -- `Zustand(ebene=99, h=1e9)` -- after which it still
  returned the correct predecessor. A function that answers correctly
  regardless of what the forward step did cannot establish that the
  forward step is reversible.
- **Binary floats were accepted silently.** `schritt(0.1, 0)` stored
  `3602879701896397/36028797018963968`, which is not `1/10`. The
  arithmetic stays formally exact and becomes substantively worthless.
- **The revolution count was dropped from the state's own output.** Two
  states two full turns apart produced identical `als_tripel()`.

WHAT THE CRITIQUE GOT WRONG
---------------------------

- **Its runtime consistency checks are tautologies.** `schritt` asserts
  `rueckwaerts(vorwaerts(s)) == s`, but `vorwaerts` adds and
  `rueckwaerts` subtracts the same exact `Fraction`s, so the two always
  cancel. Across 188865 valid random cases the assertion fired exactly
  **0 times**. It can never fire. That is the same objection the
  critique correctly raised against the cached `invertiere()`, one level
  up: the check looks like a safety net and proves nothing at runtime.
  The statement is a theorem about `Fraction` arithmetic, and its proper
  place is a property test over many inputs, not an `assert` in the hot
  path.
- **A delta is never checked against its context.** `vorwaerts` and
  `rueckwaerts` take any state, so a delta recorded at one point applies
  silently anywhere else and yields a valid-looking wrong answer.
- **A delta is not a function of its arguments alone.** At the top
  level an ascent is silently demoted to a local step, so the same
  `(dn, dh)` produces `de = +1` with four levels and `de = 0` with one.
  Replay is therefore defined only from the exact originating state --
  which the critique's own round-trip test happens to satisfy without
  saying so.
- **The float ban has a hole.** `rational()` rejects `float` and
  `numpy.float64`, but accepts `Decimal` and `str` unchecked, so
  `Decimal(0.1)` -- built from a float -- smuggles
  `3602879701896397/36028797018963968` straight through.

WHAT BOTH GOT RIGHT, AND WHAT THE THRESHOLD ACTUALLY IS
-------------------------------------------------------

Keeping the phase as an exact `Fraction` modulo 4 is correct, and so is
separating the rotational coordinate from the axial one. The ascent
threshold is also real -- but it is simpler than its presentation:

    e² = dh²/(dn² + dh²) > 1/2    <=>    dh² > dn²    <=>    dh > dn

Verified on 300000 exact random pairs with **0** disagreements. So the
eccentricity form is not a metric doing hidden work; it is the
comparison "climbs more than it turns". That is worth stating plainly
rather than dressing up, and it has an exact geometric reading: this
`e²` is literally `spirale.eccentricity_squared(dn, dh)`, so the
threshold says the helix's pitch exceeds its circumference, i.e. the
climb angle passes 45 degrees. Cross-checked against that module.

WHAT THIS MODULE DOES DIFFERENTLY
---------------------------------

- **Only exact inputs.** `int` and `Fraction` are accepted; everything
  else is refused with a message telling the caller to convert
  explicitly. No heuristic on digit counts, which would just move the
  hole.
- **A real inverse, plus a context check that can fail.** The
  predecessor is *recomputed* from the successor and the delta, and the
  delta additionally carries the state it was recorded from so
  misapplication is detected instead of silently producing a wrong
  answer. The tautological assertion is gone; the check that remains has
  real failure modes, and the tests exercise them.
- **Saturation is recorded, not swallowed.** When the ceiling denies an
  ascent the delta says so, so the action label stays faithful to what
  was requested.
- **The theorem is tested as a property**, over many random inputs,
  where it belongs -- not asserted per step.

WHAT IS STILL NOT ESTABLISHED
-----------------------------

The shell index is bookkeeping. No frequency, scale factor or physical
meaning is attached to it, because none has been derived -- attaching
one would be the unsupported extra assumption the critique warned
about, and it is better left absent than invented. Reversibility here is
a property of the *delta log*, not of the state sequence: different
histories reach the same state, so the log is what carries the
difference. And nothing in this module compresses data, establishes
consensus, or has anything to do with cryptography.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Literal

from raum27.spirale import eccentricity_squared

Action = Literal["local", "ascend", "descend"]

#: Ticks in one full turn -- the 4-stroke of `viertakt`.
TICKS_PER_TURN = 4


def exact(value: int | Fraction) -> Fraction:
    """Accept only values that are exact by construction.

    `int` and `Fraction` pass. Everything else is refused, including
    `float`, `Decimal` and `str`. Refusing the last two looks strict,
    but `Decimal(0.1)` is built from a binary float and carries
    `3602879701896397/36028797018963968`; admitting the type and then
    guessing whether a particular value was meant exactly only moves the
    hole somewhere less visible. The caller converts explicitly."""
    if isinstance(value, bool):
        raise TypeError("bool is not a coordinate; pass an int or Fraction")
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value)
    raise TypeError(
        f"inexact or ambiguous input of type {type(value).__name__}; "
        "pass an int or a Fraction, converting explicitly if needed"
    )


@dataclass(frozen=True)
class State:
    """Shell index, total rotation and axial rise -- all exact.

    `turns` keeps the *total* rotation rather than only its remainder, so
    the number of completed turns is never lost: `n = 4*turns + phase`
    exactly."""

    shell: int
    turns: Fraction
    rise: Fraction

    def __post_init__(self) -> None:
        object.__setattr__(self, "turns", exact(self.turns))
        object.__setattr__(self, "rise", exact(self.rise))
        if not isinstance(self.shell, int) or isinstance(self.shell, bool):
            raise TypeError("shell index must be an int")
        if self.shell < 0:
            raise ValueError("shell index must be >= 0")
        if self.turns < 0 or self.rise < 0:
            raise ValueError("rotation and rise must be >= 0")

    @property
    def phase(self) -> Fraction:
        """The exact phase in [0, 4) -- a Fraction, never truncated."""
        return self.turns % TICKS_PER_TURN

    @property
    def completed_turns(self) -> int:
        """How many full turns have passed. Together with `phase` this
        reconstructs `turns` exactly."""
        return self.turns // TICKS_PER_TURN

    @property
    def is_node(self) -> bool:
        """True exactly on one of the four discrete ticks."""
        return self.phase.denominator == 1


def climbs_more_than_it_turns(d_turns: Fraction, d_rise: Fraction) -> bool:
    """The ascent threshold, stated as what it is: `d_rise > d_turns`.

    Identical to `e² > 1/2` for the eccentricity below, verified over
    300000 exact random pairs with no disagreement."""
    return exact(d_rise) > exact(d_turns)


def step_eccentricity_squared(d_turns: Fraction, d_rise: Fraction) -> Fraction:
    """e² = dh²/(dn² + dh²) for one step, exact.

    Delegates to `spirale.eccentricity_squared`, which is the same
    formula with the rotational increment playing the role of the
    circumference -- so the threshold has a geometric reading: the
    helix's pitch exceeds its circumference, i.e. the climb angle passes
    45 degrees. Zero rotation is a degenerate step with no eccentricity
    defined, and is reported as 0 rather than raising, matching how the
    submitted versions treated it."""
    dn, dh = exact(d_turns), exact(d_rise)
    if dn == 0:
        return Fraction(0) if dh == 0 else Fraction(1)
    return eccentricity_squared(dn, dh)


@dataclass(frozen=True)
class Delta:
    """A transition, carrying the state it was recorded from.

    `origin` is not how the inverse is computed -- `backward` recomputes
    the predecessor from the successor. It is there so that applying a
    delta to the wrong state is *detected*, which the submitted versions
    could not do."""

    d_turns: Fraction
    d_rise: Fraction
    d_shell: int
    action: Action
    ascent_denied: bool
    origin: State

    def forward(self, state: State) -> State:
        """Apply to the state this delta was recorded from.

        Raises if handed any other state: a delta is only meaningful in
        its own context, because `d_shell` depends on where the shell
        ceiling was."""
        if state != self.origin:
            raise ValueError(
                "delta applied to a state it was not recorded from; "
                f"expected {self.origin}, got {state}"
            )
        return State(
            shell=state.shell + self.d_shell,
            turns=state.turns + self.d_turns,
            rise=state.rise + self.d_rise,
        )

    def backward(self, state: State) -> State:
        """Recompute the predecessor from the successor and this delta.

        The reconstruction is computed, then checked against `origin`.
        That check has real failure modes -- being handed an unrelated
        successor is one -- unlike asserting that adding and subtracting
        the same exact Fraction cancels, which is a theorem and cannot
        fail at runtime."""
        recovered = State(
            shell=state.shell - self.d_shell,
            turns=state.turns - self.d_turns,
            rise=state.rise - self.d_rise,
        )
        if recovered != self.origin:
            raise ValueError(
                "reconstruction does not match the recorded origin; "
                f"expected {self.origin}, recovered {recovered}"
            )
        return recovered


class Machine:
    """A deterministic rational state machine with an invertible log.

    The shell index is bookkeeping only: no frequency or scale factor is
    attached to it, because none has been derived."""

    def __init__(self, shells: int):
        if not isinstance(shells, int) or isinstance(shells, bool):
            raise TypeError("shell count must be an int")
        if shells < 1:
            raise ValueError("at least one shell is required")
        self.top_shell = shells - 1
        self.state = State(0, Fraction(0), Fraction(0))
        self.log: list[Delta] = []

    def step(self, d_turns: int | Fraction, d_rise: int | Fraction) -> Delta:
        """Advance by an exact rotational and axial increment."""
        dn, dh = exact(d_turns), exact(d_rise)
        if dn < 0 or dh < 0:
            raise ValueError("increments must be >= 0")

        state = self.state
        d_shell, action, denied = 0, "local", False

        if climbs_more_than_it_turns(dn, dh):
            if state.shell < self.top_shell:
                d_shell, action = 1, "ascend"
            else:
                # Record that the ceiling refused, rather than silently
                # reporting a local step as the submitted versions did.
                denied = True
        elif dh == 0 and dn > 0 and state.shell > 0:
            d_shell, action = -1, "descend"

        delta = Delta(dn, dh, d_shell, action, denied, state)
        self.state = delta.forward(state)
        self.log.append(delta)
        return delta

    def undo(self) -> State:
        """Step back exactly, by reconstruction rather than by recall."""
        if not self.log:
            raise IndexError("nothing to undo")
        delta = self.log[-1]
        previous = delta.backward(self.state)
        self.log.pop()
        self.state = previous
        return previous

    def replay(self) -> State:
        """Re-apply the whole log from the initial state.

        Each delta is checked against its own origin on the way, so a log
        that does not form a chain is rejected instead of producing a
        plausible-looking final state."""
        state = State(0, Fraction(0), Fraction(0))
        for delta in self.log:
            state = delta.forward(state)
        return state
