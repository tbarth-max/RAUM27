"""Gentle inverse probing: wake, do not push.

The aim submitted: probe a system only through passive interaction of the
fields -- no heating, minimal energy loss, just the impulse that draws the
smallest possible reaction. Wake it gently; do not shove it out of bed.

Three exact rules make that a plan:

- **Many small pulses instead of one large one.** A response of amplitude
  a in noise sigma is detected with confidence k once it is summed over N
  repeats with a matched filter: a >= k sigma / sqrt(N). The energy per
  pulse goes as a^2, so the **total** energy N a^2 = (k sigma)^2 does not
  depend on N at all. Splitting the same small budget into many pulses
  keeps every single touch as light as one likes (``required_response``,
  ``detection_energy``).
- **Ask at the natural frequency.** A system with quality factor Q
  answers a drive at its own frequency Q times more strongly than a slow
  push; off resonance the gain falls off fast. Driving there lowers the
  needed drive by Q and its energy by Q^2 (``resonance_gain``).
- **Stay below the disturbance limit.** Each response must stay under
  the level at which the system would be disturbed (for a crystal, the
  Lindemann limit of ``raum27.gitter``; for an insect, its reaction
  threshold). ``gentle_plan`` returns the fewest repeats for which that
  holds, and the drive per pulse.

**The alarm loop.** When the house is on fire, waking is not gentle.
If a reading crosses a critical level, the gentle plan is dropped for one
hard pulse: the whole budget (k sigma)^2 in a single touch, answered
after one pulse instead of N -- N times faster, as hard as needed. The
state is binary (quiet / alarm) with hysteresis, a Schmitt trigger: it
switches on above one level and off only below a lower one, so it does
not flutter at the edge (``alarm_states``, ``respond``).

What remains true and is not hidden: the total budget (k sigma)^2 is the
price of certainty against the noise and cannot be lowered by splitting;
only the disturbance per touch can.
"""

import math
import random


def required_response(noise, repeats, confidence=4.0):
    """Smallest response amplitude detectable with ``confidence`` sigmas after ``repeats`` pulses."""
    if noise <= 0 or repeats < 1:
        raise ValueError("noise must be positive and at least one pulse is needed")
    return confidence * noise / math.sqrt(repeats)


def detection_energy(noise, repeats, confidence=4.0):
    """Total response energy (sum of a^2) for a confident detection; independent of ``repeats``."""
    return repeats * required_response(noise, repeats, confidence) ** 2


def resonance_gain(omega, omega0, quality):
    """Response of a driven oscillator relative to a slow push: 1 / sqrt((1-r^2)^2 + (r/Q)^2)."""
    if omega0 <= 0 or quality <= 0:
        raise ValueError("natural frequency and quality must be positive")
    r = omega / omega0
    return 1.0 / math.sqrt((1 - r * r) ** 2 + (r / quality) ** 2)


def gentle_plan(noise, disturbance_limit, omega0, quality, confidence=4.0):
    """Fewest repeats whose per-pulse response stays below the limit, and the drive per pulse.

    The drive is placed at the natural frequency, so it is the response
    divided by Q. Returns (repeats, response per pulse, drive per pulse).
    """
    if disturbance_limit <= 0:
        raise ValueError("the disturbance limit must be positive")
    repeats = max(1, math.ceil((confidence * noise / disturbance_limit) ** 2))
    response = required_response(noise, repeats, confidence)
    return repeats, response, response / resonance_gain(omega0, omega0, quality)


def detection_rate(response, noise, repeats, trials=400, confidence=4.0, seed=3):
    """Share of trials in which a matched filter finds the response (simulation)."""
    rng = random.Random(seed)
    found = 0
    threshold = confidence * noise / math.sqrt(repeats) / 2
    for _ in range(trials):
        mean = sum(response + rng.gauss(0, noise) for _ in range(repeats)) / repeats
        found += mean > threshold
    return found / trials


def alarm_states(readings, on, off):
    """Binary alarm state per reading with hysteresis: on above ``on``, off only below ``off``."""
    if off >= on:
        raise ValueError("the off level must lie below the on level")
    state, states = False, []
    for value in readings:
        if not state and value >= on:
            state = True
        elif state and value <= off:
            state = False
        states.append(state)
    return states


def respond(reading, critical, noise, disturbance_limit, omega0, quality, confidence=4.0):
    """Gentle plan in calm, one hard pulse in an emergency.

    Returns (mode, pulses, response per pulse). In an emergency the
    response is k * sigma in a single pulse: the same total energy as the
    gentle plan, delivered at once.
    """
    if reading >= critical:
        return "alarm", 1, required_response(noise, 1, confidence)
    repeats, response, _ = gentle_plan(noise, disturbance_limit, omega0, quality, confidence)
    return "gentle", repeats, response
