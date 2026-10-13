"""The gear train: nine positions per wheel, the tenth click turns the next wheel.

The rule submitted: a spring is not wound on without end -- its tension
would grow with the square of the turns until it tears or snaps back.
Instead each wheel has nine positions, 1 to 9, and may turn back and
forth freely between them. The stop at 10 does not hold the wheel; it
keeps it from turning over. The click that would reach 10 sets the wheel
back to 1 and advances the next wheel by one. Going below 1 is the
mirror image: the wheel goes to 9 and the next wheel steps back.

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
  silent wrap would lose the count.
"""

DIGITS = 9


def _check(wheels):
    if not wheels or any(not isinstance(d, int) or not 1 <= d <= DIGITS for d in wheels):
        raise ValueError(f"every wheel stands on 1..{DIGITS}")


def step(wheels, direction=1):
    """Turn the first wheel one click; carries and borrows move to the next wheels.

    ``wheels[0]`` is the fastest wheel. Returns ``(new_wheels, wheels_moved)``.
    """
    _check(wheels)
    if direction not in (1, -1):
        raise ValueError("a click goes one position forward (1) or back (-1)")
    result = list(wheels)
    for i in range(len(result)):
        moved = result[i] + direction
        if 1 <= moved <= DIGITS:
            result[i] = moved
            return result, i + 1
        result[i] = 1 if direction == 1 else DIGITS
    raise OverflowError("the last wheel would turn over; the train is full" if direction == 1
                        else "the train stands at its zero point")


def value(wheels):
    """Number of clicks from the zero point (all wheels at 1)."""
    _check(wheels)
    return sum((d - 1) * DIGITS ** i for i, d in enumerate(wheels))


def from_value(number, count):
    """Wheel positions for ``number`` clicks on a train of ``count`` wheels."""
    if count < 1 or not 0 <= number < DIGITS ** count:
        raise ValueError(f"{number} does not fit on {count} wheels")
    return [number // DIGITS ** i % DIGITS + 1 for i in range(count)]


def tension(wheels):
    """Clicks each wheel is wound from rest; never more than DIGITS - 1."""
    _check(wheels)
    return [d - 1 for d in wheels]


def wheels_needed(total):
    """Fewest wheels whose train holds at least ``total`` states."""
    if total < 1:
        raise ValueError("at least one state is needed")
    count = 1
    while DIGITS ** count < total:
        count += 1
    return count
