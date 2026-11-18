"""Tests for raum27.zustandsmaschine.

Includes the defects found in both submitted versions, as regressions,
so neither can come back.
"""
from __future__ import annotations

import random
from decimal import Decimal
from fractions import Fraction

import pytest

from raum27.spirale import eccentricity_squared
from raum27.zustandsmaschine import (
    TICKS_PER_TURN,
    Delta,
    Machine,
    State,
    climbs_more_than_it_turns,
    exact,
    step_eccentricity_squared,
)


# ------------------------------------------- what both versions got right

def test_a_fractional_phase_survives_exactly():
    machine = Machine(shells=4)
    machine.step(Fraction(7, 3), Fraction(1, 2))
    assert machine.state.turns == Fraction(7, 3)
    assert machine.state.phase == Fraction(7, 3)
    assert machine.state.phase.denominator == 3
    assert not machine.state.is_node


def test_the_four_discrete_ticks_are_nodes_and_nothing_else_is():
    for whole in (0, 1, 2, 3, 4, 8, 11):
        assert State(0, Fraction(whole), Fraction(0)).is_node
    for broken in (Fraction(7, 3), Fraction(1, 2), Fraction(9, 4), Fraction(1, 100)):
        assert not State(0, broken, Fraction(0)).is_node


def test_rotation_and_rise_accumulate_independently():
    machine = Machine(shells=4)
    machine.step(Fraction(7, 3), Fraction(1, 2))
    machine.step(Fraction(1), Fraction(3))
    assert machine.state.turns == Fraction(10, 3)
    assert machine.state.rise == Fraction(7, 2)
    assert machine.state.shell == 1


# --------------------------------- regressions against the first version

def test_the_revolution_count_is_not_lost():
    """REGRESSION. The first version exposed only the phase remainder, so
    two states two full turns apart were indistinguishable in its own
    output."""
    near = State(0, Fraction(10, 3), Fraction(0))
    far = State(0, Fraction(10, 3) + 8, Fraction(0))
    assert near.phase == far.phase == Fraction(10, 3)
    assert near.completed_turns == 0
    assert far.completed_turns == 2
    assert near != far
    # and the pair reconstructs the total exactly
    for state in (near, far):
        assert TICKS_PER_TURN * state.completed_turns + state.phase == state.turns


def test_binary_floats_are_refused_rather_than_silently_inflated():
    """REGRESSION. The first version accepted `0.1` and stored
    3602879701896397/36028797018963968, which is not 1/10."""
    machine = Machine(shells=2)
    with pytest.raises(TypeError):
        machine.step(0.1, Fraction(0))
    with pytest.raises(TypeError):
        exact(0.1)
    assert Fraction(0.1) != Fraction(1, 10)  # why it matters


def test_the_decimal_hole_in_the_critiques_float_ban_is_closed():
    """REGRESSION. The critique rejected `float` but accepted `Decimal`
    and `str` unchecked, so `Decimal(0.1)` -- constructed from a float --
    carried the binary fraction straight through."""
    assert Fraction(Decimal(0.1)) != Fraction(1, 10)
    with pytest.raises(TypeError):
        exact(Decimal(0.1))
    with pytest.raises(TypeError):
        exact(Decimal("0.1"))   # refused too: the type cannot be trusted
    with pytest.raises(TypeError):
        exact("1/10")
    # the exact types still work
    assert exact(Fraction(1, 10)) == Fraction(1, 10)
    assert exact(3) == Fraction(3)
    with pytest.raises(TypeError):
        exact(True)             # bool is not a coordinate


# ------------------------------------ regressions against the critique

def test_the_inverse_is_recomputed_not_recalled():
    """REGRESSION against the FIRST version, whose `invertiere()` returned
    a cached predecessor and so answered correctly even when the forward
    step was nonsense.

    Here `backward` recomputes from the successor, so handing it an
    unrelated successor is detected."""
    machine = Machine(shells=4)
    machine.step(Fraction(1), Fraction(3))
    delta = machine.log[-1]
    # the genuine successor reconstructs
    assert delta.backward(machine.state) == State(0, Fraction(0), Fraction(0))
    # a fabricated successor does not
    with pytest.raises(ValueError):
        delta.backward(State(99, Fraction(10 ** 9), Fraction(10 ** 9)))


def test_a_delta_applied_out_of_context_is_rejected():
    """REGRESSION. In the critique's version `vorwaerts` accepted any
    state and silently produced a valid-looking wrong answer -- a delta
    recorded at the origin applied to (100, 100) returned
    (shell=1, 101, 103) with no complaint."""
    machine = Machine(shells=4)
    machine.step(Fraction(1), Fraction(3))
    delta = machine.log[-1]
    with pytest.raises(ValueError):
        delta.forward(State(0, Fraction(100), Fraction(100)))
    # only its own origin is accepted
    assert delta.forward(delta.origin) == machine.state


def test_a_denied_ascent_is_recorded_rather_than_relabelled():
    """REGRESSION. At the ceiling both versions reported a local step, so
    the same (dn, dh) gave different deltas depending on shell count with
    nothing marking why."""
    tall = Machine(shells=4)
    flat = Machine(shells=1)
    tall_delta = tall.step(Fraction(1), Fraction(3))
    flat_delta = flat.step(Fraction(1), Fraction(3))

    assert tall_delta.action == "ascend"
    assert tall_delta.d_shell == 1
    assert not tall_delta.ascent_denied

    assert flat_delta.d_shell == 0          # the ceiling still binds
    assert flat_delta.action == "local"
    assert flat_delta.ascent_denied         # but the refusal is on the record


# ----------------------------- the theorem, tested where it belongs

def test_reconstruction_is_exact_over_many_random_transitions():
    """`backward(forward(s)) == s` is a theorem about Fraction arithmetic,
    not a runtime property -- adding and subtracting the same exact
    rational always cancels. The critique asserted it per step, where it
    can never fail; across 188865 valid random cases in its own code it
    fired 0 times.

    Its proper place is here, as a property over many inputs."""
    rng = random.Random(2)
    checked = 0
    for _ in range(20000):
        state = State(
            rng.randint(0, 5),
            Fraction(rng.randint(0, 999), rng.randint(1, 97)),
            Fraction(rng.randint(0, 999), rng.randint(1, 97)),
        )
        delta = Delta(
            Fraction(rng.randint(0, 999), rng.randint(1, 97)),
            Fraction(rng.randint(0, 999), rng.randint(1, 97)),
            rng.choice([-1, 0, 1]),
            "local",
            False,
            state,
        )
        try:
            successor = delta.forward(state)
        except ValueError:
            continue          # the increment would leave the valid region
        assert delta.backward(successor) == state
        checked += 1
    assert checked > 15000


def test_a_long_history_replays_and_unwinds_exactly():
    rng = random.Random(7)
    machine = Machine(shells=3)
    for _ in range(300):
        machine.step(
            Fraction(rng.randint(0, 20), rng.randint(1, 7)),
            Fraction(rng.randint(0, 20), rng.randint(1, 7)),
        )
    final = machine.state
    assert machine.replay() == final        # forward from the start
    for _ in range(300):
        machine.undo()
    assert machine.state == State(0, Fraction(0), Fraction(0))
    assert machine.log == []


def test_the_round_trip_holds_at_the_shell_ceiling_too():
    """Where saturation makes the shell path non-obvious."""
    machine = Machine(shells=2)
    sequence = [(Fraction(1), Fraction(3))] * 3 + [(Fraction(4), Fraction(0))]
    for dn, dh in sequence:
        machine.step(dn, dh)
    final = machine.state
    recorded = [(d.d_turns, d.d_rise, d.d_shell, d.action, d.ascent_denied)
                for d in machine.log]
    assert [r[3] for r in recorded] == ["ascend", "local", "local", "descend"]
    assert [r[4] for r in recorded] == [False, True, True, False]
    for _ in sequence:
        machine.undo()
    assert machine.state == State(0, Fraction(0), Fraction(0))
    for dn, dh in sequence:
        machine.step(dn, dh)
    assert machine.state == final
    assert [(d.d_turns, d.d_rise, d.d_shell, d.action, d.ascent_denied)
            for d in machine.log] == recorded


# ------------------------------------------- what the threshold really is

def test_the_eccentricity_threshold_is_exactly_a_comparison():
    """e² > 1/2 <=> dh² > dn² <=> dh > dn. 20000 exact random pairs, no
    disagreement -- so the eccentricity form is not a metric doing hidden
    work."""
    rng = random.Random(1)
    for _ in range(20000):
        dn = Fraction(rng.randint(0, 400), rng.randint(1, 40))
        dh = Fraction(rng.randint(0, 400), rng.randint(1, 40))
        if dn == 0 and dh == 0:
            continue
        assert (step_eccentricity_squared(dn, dh) > Fraction(1, 2)) == (dh > dn)
        assert climbs_more_than_it_turns(dn, dh) == (dh > dn)


def test_the_step_eccentricity_is_the_spirale_formula():
    """Cross-module: the rotational increment plays the role of the
    circumference, so the threshold means the helix pitch exceeds its
    circumference -- the climb angle passing 45 degrees."""
    for dn, dh in ((Fraction(4), Fraction(3)), (Fraction(1), Fraction(3)),
                   (Fraction(3), Fraction(4)), (Fraction(1), Fraction(1))):
        assert step_eccentricity_squared(dn, dh) == eccentricity_squared(dn, dh)
    # at exactly 45 degrees the threshold is not crossed
    assert step_eccentricity_squared(Fraction(1), Fraction(1)) == Fraction(1, 2)
    assert not climbs_more_than_it_turns(Fraction(1), Fraction(1))
    # a pure rise is fully eccentric; a pure turn is not eccentric at all
    assert step_eccentricity_squared(Fraction(0), Fraction(1)) == 1
    assert step_eccentricity_squared(Fraction(1), Fraction(0)) == 0
    assert step_eccentricity_squared(Fraction(0), Fraction(0)) == 0


# ------------------------------------------------------------- guards

def test_construction_and_step_guards():
    with pytest.raises(TypeError):
        Machine(shells=True)
    with pytest.raises(ValueError):
        Machine(shells=0)
    with pytest.raises(ValueError):
        State(-1, Fraction(0), Fraction(0))
    with pytest.raises(TypeError):
        State(Fraction(1), Fraction(0), Fraction(0))
    with pytest.raises(ValueError):
        State(0, Fraction(-1), Fraction(0))
    with pytest.raises(ValueError):
        State(0, Fraction(0), Fraction(-1))
    machine = Machine(shells=2)
    with pytest.raises(ValueError):
        machine.step(Fraction(-1), Fraction(0))
    with pytest.raises(ValueError):
        machine.step(Fraction(0), Fraction(-1))
    with pytest.raises(IndexError):
        machine.undo()


def test_descending_below_the_base_shell_is_not_possible():
    machine = Machine(shells=3)
    delta = machine.step(Fraction(4), Fraction(0))
    assert delta.action == "local"      # already at the base, nothing to descend
    assert delta.d_shell == 0
    assert machine.state.shell == 0
