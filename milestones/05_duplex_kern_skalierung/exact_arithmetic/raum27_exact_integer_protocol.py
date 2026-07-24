#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence
import ast
import hashlib
import json

FIRST_INTERACTION = (4, 3)
RECIPROCAL_INTERACTION = (3, 4)


@dataclass(frozen=True)
class InteractionRatio:
    upper: int
    lower: int

    def __post_init__(self) -> None:
        if self.upper <= 0 or self.lower <= 0:
            raise ValueError("ratio components must be positive integers")

    def reciprocal(self) -> "InteractionRatio":
        return InteractionRatio(self.lower, self.upper)

    def compose(self, other: "InteractionRatio") -> "InteractionRatio":
        return InteractionRatio(
            self.upper * other.upper,
            self.lower * other.lower,
        )


@dataclass(frozen=True)
class ExactVector:
    numerators: tuple[int, ...]
    denominator: int
    history: tuple[tuple[int, int], ...] = ()

    def __post_init__(self) -> None:
        if self.denominator <= 0:
            raise ValueError("denominator must be positive")
        if not self.numerators:
            raise ValueError("empty vector")

    def apply(self, ratio: InteractionRatio) -> "ExactVector":
        return ExactVector(
            tuple(value * ratio.upper for value in self.numerators),
            self.denominator * ratio.lower,
            self.history + ((ratio.upper, ratio.lower),),
        )

    def apply_reciprocal(self, ratio: InteractionRatio) -> "ExactVector":
        return self.apply(ratio.reciprocal())

    def equivalent(self, other: "ExactVector") -> bool:
        return (
            len(self.numerators) == len(other.numerators)
            and all(
                left * other.denominator == right * self.denominator
                for left, right in zip(self.numerators, other.numerators)
            )
        )

    def signs(self) -> tuple[int, ...]:
        result = []
        for value in self.numerators:
            if value > 0:
                result.append(1)
            elif value < 0:
                result.append(-1)
            else:
                result.append(0)
        return tuple(result)

    def first_raw_magnitude_ratio(self) -> tuple[int, int]:
        for value in self.numerators:
            if value:
                return (value if value > 0 else -value), self.denominator
        return 0, self.denominator


@dataclass(frozen=True)
class GaussianExactVector:
    real: tuple[int, ...]
    imag: tuple[int, ...]
    denominator: int

    def __post_init__(self) -> None:
        if len(self.real) != len(self.imag):
            raise ValueError("axis length mismatch")
        if self.denominator <= 0:
            raise ValueError("denominator must be positive")

    def quarter_turn(self, turns: int) -> "GaussianExactVector":
        q = turns % 4
        if q == 0:
            return self
        if q == 1:
            return GaussianExactVector(
                tuple(-value for value in self.imag),
                self.real,
                self.denominator,
            )
        if q == 2:
            return GaussianExactVector(
                tuple(-value for value in self.real),
                tuple(-value for value in self.imag),
                self.denominator,
            )
        return GaussianExactVector(
            self.imag,
            tuple(-value for value in self.real),
            self.denominator,
        )


CORNERS = tuple(
    (x, y, z)
    for x in (-1, 1)
    for y in (-1, 1)
    for z in (-1, 1)
)

H8 = tuple(
    (1, x, y, z, x * y, x * z, y * z, x * y * z)
    for x, y, z in CORNERS
)

B7 = (
    (1, 0, 0, 0),
    (1, 1, 0, 0),
    (1, -1, 0, 0),
    (1, 0, 1, 0),
    (1, 0, -1, 0),
    (1, 0, 0, 1),
    (1, 0, 0, -1),
)

GROUP_A = (0, 1, 2, 3)
GROUP_B = (7, 4, 5, 6)


def transpose(matrix: Sequence[Sequence[int]]) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(row[index] for row in matrix)
        for index in range(len(matrix[0]))
    )


def mat_vec(
    matrix: Sequence[Sequence[int]],
    vector: Sequence[int],
) -> tuple[int, ...]:
    return tuple(
        sum(coefficient * value for coefficient, value in zip(row, vector))
        for row in matrix
    )


H8_T = transpose(H8)
B7_T = transpose(B7)


def byte_to_modes(value: int) -> ExactVector:
    if not 0 <= value <= 255:
        raise ValueError("byte outside 0..255")
    return ExactVector(
        tuple(1 if (value >> bit) & 1 else -1 for bit in range(8)),
        1,
    )


def modes_to_byte(vector: ExactVector) -> int:
    value = 0
    for bit, sign in enumerate(vector.signs()):
        if sign > 0:
            value |= 1 << bit
    return value


def outer_project(vector: ExactVector) -> ExactVector:
    return ExactVector(
        mat_vec(H8, vector.numerators),
        vector.denominator,
        vector.history,
    )


def outer_reconstruct(outer: ExactVector) -> ExactVector:
    return ExactVector(
        mat_vec(H8_T, outer.numerators),
        outer.denominator * 8,
        outer.history + ((8, 8),),
    )


def inner_project(vector: ExactVector) -> tuple[ExactVector, ExactVector]:
    group_a = tuple(vector.numerators[index] for index in GROUP_A)
    group_b = tuple(vector.numerators[index] for index in GROUP_B)
    return (
        ExactVector(mat_vec(B7, group_a), vector.denominator, vector.history),
        ExactVector(mat_vec(B7, group_b), vector.denominator, vector.history),
    )


def reconstruct_focus_group(focus: ExactVector) -> ExactVector:
    projected = mat_vec(B7_T, focus.numerators)
    return ExactVector(
        (
            2 * projected[0],
            7 * projected[1],
            7 * projected[2],
            7 * projected[3],
        ),
        focus.denominator * 14,
        focus.history + ((14, 14),),
    )


def inner_reconstruct(
    phase_a: ExactVector,
    phase_b: ExactVector,
) -> ExactVector:
    group_a = reconstruct_focus_group(phase_a)
    group_b = reconstruct_focus_group(phase_b)
    if group_a.denominator != group_b.denominator:
        raise ValueError("focus denominator mismatch")
    numerators = [0] * 8
    for local, global_index in enumerate(GROUP_A):
        numerators[global_index] = group_a.numerators[local]
    for local, global_index in enumerate(GROUP_B):
        numerators[global_index] = group_b.numerators[local]
    return ExactVector(
        tuple(numerators),
        group_a.denominator,
        group_a.history + group_b.history,
    )


def gaussian_outer_project(value: GaussianExactVector) -> GaussianExactVector:
    return GaussianExactVector(
        mat_vec(H8, value.real),
        mat_vec(H8, value.imag),
        value.denominator,
    )


def gaussian_outer_reconstruct(value: GaussianExactVector) -> GaussianExactVector:
    return GaussianExactVector(
        mat_vec(H8_T, value.real),
        mat_vec(H8_T, value.imag),
        value.denominator * 8,
    )


def encode_duplex(
    left_byte: int,
    right_byte: int,
    depth: int,
    quarter_turns: int,
) -> GaussianExactVector:
    ratio = InteractionRatio(*FIRST_INTERACTION)
    left = byte_to_modes(left_byte)
    right = byte_to_modes(right_byte)
    for _ in range(depth):
        left = left.apply(ratio)
        right = right.apply(ratio)
    packed = GaussianExactVector(
        left.numerators,
        right.numerators,
        left.denominator,
    )
    return gaussian_outer_project(packed.quarter_turn(quarter_turns))


def decode_duplex(
    packet: GaussianExactVector,
    quarter_turns: int,
) -> tuple[int, int]:
    reconstructed = gaussian_outer_reconstruct(packet)
    aligned = reconstructed.quarter_turn(-quarter_turns)
    left = ExactVector(aligned.real, aligned.denominator)
    right = ExactVector(aligned.imag, aligned.denominator)
    return modes_to_byte(left), modes_to_byte(right)


def source_policy_check(path: Path) -> dict[str, int]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    float_literals = 0
    true_divisions = 0
    banned_imports = 0
    banned_calls = 0
    forbidden_modules = {"math", "numpy", "fractions"}
    forbidden_functions = {"sin", "cos", "tan", "sqrt", "gcd"}

    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, float):
            float_literals += 1
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
            true_divisions += 1
        if isinstance(node, ast.Import):
            for name in node.names:
                if name.name.split(".")[0] in forbidden_modules:
                    banned_imports += 1
        if isinstance(node, ast.ImportFrom):
            if node.module and node.module.split(".")[0] in forbidden_modules:
                banned_imports += 1
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in forbidden_functions:
                banned_calls += 1
            if isinstance(node.func, ast.Attribute) and node.func.attr in forbidden_functions:
                banned_calls += 1

    return {
        "float_literals": float_literals,
        "true_divisions": true_divisions,
        "banned_imports": banned_imports,
        "banned_calls": banned_calls,
    }


def run_tests() -> dict[str, object]:
    ratio = InteractionRatio(*FIRST_INTERACTION)
    cases = 0
    outer_errors = 0
    inner_errors = 0
    disagreement = 0
    history_errors = 0

    for value in range(256):
        original = byte_to_modes(value)
        for depth in (0, 1, 2, 4, 8):
            state = original
            for _ in range(depth):
                state = state.apply(ratio)
            outer_back = outer_reconstruct(outer_project(state))
            phase_a, phase_b = inner_project(state)
            inner_back = inner_reconstruct(phase_a, phase_b)
            cases += 1
            if not state.equivalent(outer_back):
                outer_errors += 1
            if not state.equivalent(inner_back):
                inner_errors += 1
            if not outer_back.equivalent(inner_back):
                disagreement += 1
            cycled = state
            for _ in range(depth):
                cycled = cycled.apply_reciprocal(ratio)
            expected = 12 ** depth
            raw_upper, raw_lower = cycled.first_raw_magnitude_ratio()
            if raw_upper != expected or raw_lower != expected:
                history_errors += 1

    probe = GaussianExactVector(
        (1, 2, 3, 4, 5, 6, 7, 8),
        (-8, -7, -6, -5, -4, -3, -2, -1),
        9,
    )
    quarter_turn_errors = 0
    if probe.quarter_turn(4) != probe:
        quarter_turn_errors += 1
    if probe.quarter_turn(1).quarter_turn(3) != probe:
        quarter_turn_errors += 1

    duplex_pairs = 0
    duplex_errors = 0
    for left in range(256):
        for right in range(256):
            turns = (left + right) % 4
            packet = encode_duplex(left, right, 3, turns)
            if decode_duplex(packet, turns) != (left, right):
                duplex_errors += 1
            duplex_pairs += 1

    policy = source_policy_check(Path(__file__))
    fatal = any(policy.values()) or any(
        (
            outer_errors,
            inner_errors,
            disagreement,
            history_errors,
            quarter_turn_errors,
            duplex_errors,
        )
    )

    return {
        "protocol": {
            "first_interaction": list(FIRST_INTERACTION),
            "reciprocal_interaction": list(RECIPROCAL_INTERACTION),
            "phase_group": "Z4",
            "outer_reconstruction_ratio": [8, 8],
            "inner_reconstruction_ratio": [14, 14],
            "automatic_reduction": False,
        },
        "source_policy": policy,
        "single_byte_tests": {
            "cases": cases,
            "outer_roundtrip_errors": outer_errors,
            "inner_roundtrip_errors": inner_errors,
            "outer_inner_disagreement": disagreement,
            "history_errors": history_errors,
        },
        "quarter_turn_tests": {
            "errors": quarter_turn_errors,
        },
        "duplex_tests": {
            "pairs": duplex_pairs,
            "errors": duplex_errors,
        },
        "fatal_error": bool(fatal),
    }


def main() -> int:
    report = run_tests()
    report_path = Path(__file__).with_name(
        "raum27_exact_integer_protocol_report.json"
    )
    report_path.write_text(
        json.dumps(report, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if report["fatal_error"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
