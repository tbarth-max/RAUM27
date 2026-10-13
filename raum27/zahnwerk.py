"""The gear train: nine positions per wheel, the tenth click turns the next wheel.

The rule submitted: a spring is not wound on without end -- its tension
would grow with the square of the turns until it tears or snaps back.
Instead each wheel has nine positions, 1 to 9, and may turn back and
forth freely between them. The stop at 10 does not hold the wheel; it
keeps it from turning over. The click that would reach 10 sets the wheel
back to 1 and advances the next wheel by one. Going below 1 is the
mirror image: the wheel goes to 9 and the next wheel steps back.

The rule that decides when the next wheel moves is the **duplex trigger
condition** (``triggers``): forward from 9, or backward from 1.

This is an odometer with the digits 1..9, the number 10 being the
spring constant: the limit no wheel can reach. Consequences pinned by
the tests:

- the tension on any wheel never exceeds eight clicks from its rest
  position, however long the train runs (``tension``);
- every step is undone exactly by the opposite step (``step``);
- ``n`` wheels hold ``9**n`` states, numbered 0 .. 9**n - 1 with all
  wheels at 1 as the zero point (``value`` / ``from_value``);
- nine wheels hold 9**9 = 387 420 489 states, the first count of wheels
  that covers 300 000 000; eight hold only 43 046 721;
- turning the last wheel over is refused rather than wrapped, since a
  silent wrap would lose the count;
- with the hook zero (``low=HOOK``) a wheel reads 0..9: the click that
  would make 10 leaves 0 showing here and opens the 1 on the next wheel,
  so one, two, three wheels count to 9, 99, 999 -- decimal place value.
  Nine wheels are needed for 300 000 000 in either mode.
"""

DIGITS = 9
HOOK = 0
"""The hook zero: pass ``low=HOOK`` for wheels that read 0..9 (see below)."""

# Hook mode: the wheel also has an inner zero. When the click that would
# make 10 arrives, the wheel stops on its hook, shows 0 outside, and the 1
# opens on the next wheel to the right. The ten is still never shown; it
# becomes "1 there, 0 here". That gives the counts 9, 99, 999, ... and is
# ordinary decimal place value. The default ``low=1`` keeps the original
# nine-position wheel without a zero.


def _check(wheels, low):
    if low not in (1, HOOK):
        raise ValueError("a wheel starts at 1, or at the hook zero 0")
    if not wheels or any(not isinstance(d, int) or not low <= d <= DIGITS for d in wheels):
        raise ValueError(f"every wheel stands on {low}..{DIGITS}")


def _base(low):
    return DIGITS - low + 1


def triggers(position, direction, low=1):
    """The duplex trigger condition of one wheel.

    A click hands on to the next wheel exactly when it would leave the
    wheel's range: forward from 9 (carry) or backward from its lowest
    position (borrow). Two sides, one rule -- hence duplex.
    """
    _check([position], low)
    if direction not in (1, -1):
        raise ValueError("a click goes one position forward (1) or back (-1)")
    return (position == DIGITS and direction == 1) or (position == low and direction == -1)


def step(wheels, direction=1, low=1):
    """Turn the first wheel one click; carries and borrows move to the next wheels.

    ``wheels[0]`` is the fastest wheel. Returns ``(new_wheels, wheels_moved)``.
    """
    _check(wheels, low)
    if direction not in (1, -1):
        raise ValueError("a click goes one position forward (1) or back (-1)")
    result = list(wheels)
    for i in range(len(result)):
        moved = result[i] + direction
        if low <= moved <= DIGITS:
            result[i] = moved
            return result, i + 1
        result[i] = low if direction == 1 else DIGITS
    raise OverflowError("the last wheel would turn over; the train is full" if direction == 1
                        else "the train stands at its zero point")


def value(wheels, low=1):
    """Number of clicks from the zero point (all wheels at their lowest position)."""
    _check(wheels, low)
    return sum((d - low) * _base(low) ** i for i, d in enumerate(wheels))


def from_value(number, count, low=1):
    """Wheel positions for ``number`` clicks on a train of ``count`` wheels."""
    base = _base(low)
    if count < 1 or not 0 <= number < base ** count:
        raise ValueError(f"{number} does not fit on {count} wheels")
    return [number // base ** i % base + low for i in range(count)]


def tension(wheels, low=1):
    """Clicks each wheel is wound from rest; never more than ``9 - low``."""
    _check(wheels, low)
    return [d - low for d in wheels]


def wheels_needed(total, low=1):
    """Fewest wheels whose train holds at least ``total`` states."""
    if total < 1:
        raise ValueError("at least one state is needed")
    base, count = _base(low), 1
    while base ** count < total:
        count += 1
    return count
