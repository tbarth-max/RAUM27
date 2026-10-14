"""Tests for raum27.sprachprotokoll."""

from fractions import Fraction

import pytest

from raum27.sprachprotokoll import (
    CHANNELS, buffer_for, decode, encode, fixed_bits, frame_bits, in_comfort_band, mask_text,
    mean_frame_bits, predicted_position, response_time, stream_bits, transfer_time,
)

START = (1, 2, 3, 4, 5, 6)


def test_mask_marks_only_changed_channels():
    assert len(CHANNELS) == 6
    mask, payload = encode(START, START)
    assert mask_text(mask) == "000000" and payload == []
    now = (9, 2, 3, 7, 5, 6)                          # concept and event changed
    mask, payload = encode(START, now)
    assert mask_text(mask) == "100100" and payload == [(0, 9), (3, 7)]
    assert decode(START, mask, payload) == now
    with pytest.raises(ValueError):
        decode(START, mask, payload[:1])
    with pytest.raises(ValueError):
        encode(START, (16, 2, 3, 4, 5, 6))
    with pytest.raises(ValueError):
        encode(START, (1, 2))


def test_mask_wins_up_to_four_channels_and_loses_at_five():
    assert fixed_bits() == 24
    assert [frame_bits(k) for k in range(7)] == [6, 10, 14, 18, 22, 26, 30]
    assert [frame_bits(k) < 24 for k in range(7)] == [True] * 5 + [False] * 2
    assert mean_frame_bits(Fraction(3, 4)) == 24      # break-even probability
    assert mean_frame_bits(Fraction(1, 4)) == 12      # 1.5 channels per step on average
    with pytest.raises(ValueError):
        frame_bits(7)


def test_stream_of_states():
    states = [START, START, (9, 2, 3, 4, 5, 6), (9, 2, 3, 7, 5, 6)]
    assert stream_bits(states) == 24 + 6 + 10 + 10
    assert stream_bits(states) < 24 * len(states)


def test_dx_leads_dt_follows():
    assert transfer_time(33) == Fraction(1, 10)
    assert [transfer_time(x) for x in (Fraction(33, 10), 66, 165, 330)] == [
        Fraction(1, 100), Fraction(1, 5), Fraction(1, 2), 1]
    assert transfer_time(Fraction(343, 10), 343) == Fraction(1, 10)
    assert response_time(33, Fraction(2, 5)) == Fraction(1, 2)
    assert transfer_time(300000000, 300000000) == 1
    with pytest.raises(ValueError):
        transfer_time(1, 300000001)
    with pytest.raises(TypeError):
        transfer_time(33.0)


def test_processing_is_its_own_value_and_sync_buffers_the_faster_side():
    assert in_comfort_band(Fraction(2, 5)) and not in_comfort_band(Fraction(1, 10))
    assert buffer_for(Fraction(1, 5), Fraction(1, 2)) == Fraction(3, 10)
    assert buffer_for(Fraction(1, 2), Fraction(1, 5)) == 0      # the slower cannot be sped up
    assert predicted_position(2, Fraction(1, 2), Fraction(3, 10)) == Fraction(43, 20)
