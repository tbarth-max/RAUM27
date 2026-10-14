"""Speech protocol core: a 6-bit change mask over six channels, and dX leading dT.

The six channels are the six faces of the cube: concept, relation,
grammar, event, prosody, control. A frame starts with a 6-bit mask, one
bit per channel: did it change? Only changed channels carry a value
(4 bits each here); unchanged channels keep their last state. ``000000``
is a whole frame meaning "nothing changed".

What it costs, exactly: 6 + 4k bits for k changed channels, against 24
for six fixed 4-bit fields. The mask wins for k <= 4, ties nowhere and
loses for k = 5 (26) and k = 6 (30). With each channel changing
independently with probability p the mean is 6 + 24p: below 24 exactly
when p < 3/4.

Time: dT_transfer = dX / v, with v fixed per medium; processing time is
a separate value per agent, never derived from dX. Synchronising to the
slower side works by buffering the faster one -- the slower cannot be
sped up. Control traffic uses prediction instead of delay: show where
the robot will be, x + v * latency.

Not in here, by decision: the integrity witness C' (hash comparison) and
any chained log -- the trust layer waits for the first trial run.
"""

from fractions import Fraction

CHANNELS = ("concept", "relation", "grammar", "event", "prosody", "control")
VALUE_BITS = 4
MASK_BITS = len(CHANNELS)
SOUND_IN_AIR = Fraction(330)          # m/s, the model's round value
MODEL_LIMIT = Fraction(300000000)      # m/s, 3 * 10^8
COMFORT_BAND = (Fraction(1, 5), Fraction(1, 2))   # 200 .. 500 ms processing


def _exact(*values):
    for v in values:
        if isinstance(v, float):
            raise TypeError("exact module: use int or Fraction, not float")
    return [Fraction(v) for v in values]


# --- change mask --------------------------------------------------------------

def encode(previous, current):
    """(mask, [(channel, value), ...]) for the channels whose value changed."""
    if len(previous) != MASK_BITS or len(current) != MASK_BITS:
        raise ValueError("six channels")
    for v in current:
        if not 0 <= v < 2 ** VALUE_BITS:
            raise ValueError("a channel value has 4 bits")
    mask, payload = 0, []
    for i, (old, new) in enumerate(zip(previous, current)):
        if old != new:
            mask |= 1 << (MASK_BITS - 1 - i)
            payload.append((i, new))
    return mask, payload


def decode(previous, mask, payload):
    """Apply a frame to the last state; channels without a bit stay as they were."""
    state = list(previous)
    flagged = [i for i in range(MASK_BITS) if mask >> (MASK_BITS - 1 - i) & 1]
    if flagged != [i for i, _ in payload]:
        raise ValueError("mask and payload disagree")
    for i, value in payload:
        state[i] = value
    return tuple(state)


def mask_text(mask):
    return format(mask, "06b")


def frame_bits(changed):
    """Bits of one masked frame with ``changed`` channels changed."""
    if not 0 <= changed <= MASK_BITS:
        raise ValueError("0..6 channels")
    return MASK_BITS + VALUE_BITS * changed


def fixed_bits():
    return MASK_BITS * VALUE_BITS


def mean_frame_bits(p):
    """Expected bits per frame if each channel changes with probability p."""
    (p,) = _exact(p)
    return MASK_BITS + MASK_BITS * VALUE_BITS * p


def stream_bits(states):
    """Total bits to send a sequence of states, the first one in full."""
    total, prev = fixed_bits(), states[0]
    for s in states[1:]:
        _, payload = encode(prev, s)
        total += frame_bits(len(payload))
        prev = s
    return total


# --- dX leading, dT derived ---------------------------------------------------

def transfer_time(dx, v=SOUND_IN_AIR):
    dx, v = _exact(dx, v)
    if v <= 0 or v > MODEL_LIMIT:
        raise ValueError("0 < v <= 3 * 10^8 m/s")
    return dx / v


def response_time(dx, processing, v=SOUND_IN_AIR):
    """Transfer from the distance plus the agent's own processing time."""
    (processing,) = _exact(processing)
    return transfer_time(dx, v) + processing


def in_comfort_band(processing):
    (processing,) = _exact(processing)
    return COMFORT_BAND[0] <= processing <= COMFORT_BAND[1]


def buffer_for(own, partner):
    """How long to hold one's own answer back to meet the slower partner (never negative)."""
    own, partner = _exact(own, partner)
    return max(Fraction(0), partner - own)


def predicted_position(x, v, latency):
    """Where a controlled object will be when the command arrives: x + v * latency."""
    x, v, latency = _exact(x, v, latency)
    return x + v * latency
