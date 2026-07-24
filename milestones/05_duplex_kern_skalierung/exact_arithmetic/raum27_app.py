#!/usr/bin/env python3
"""
RAUM27 exact integer container application.

The RAUM27 core remains an exact reversible computation layer. The container
stores interaction history symbolically rather than expanding 12**depth.

Compression is honest:
- the archive selects a reversible byte codec;
- the full archive size, including metadata and hashes, is compared with input;
- no universal compression claim is made;
- random or already-compressed data normally remains raw.

No floating-point arithmetic is used in this file.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable
import argparse
import binascii
import hashlib
import json
import struct
import sys
import zlib

from raum27_exact_integer_protocol import (
    FIRST_INTERACTION,
    RECIPROCAL_INTERACTION,
    decode_duplex,
    encode_duplex,
    run_tests as run_core_tests,
)


MAGIC = b"R27I"
VERSION = 1
PROTOCOL_ID = b"861Z4I01"
PHASE_PAIR_SUM = 1
FIXED_HEADER_SIZE = 4 + 1 + 1 + 1 + 1 + 8 + 4 + 32 + 32

CODEC_RAW = 0
CODEC_RLE = 1
CODEC_XOR_RLE = 2
CODEC_ZLIB = 3
CODEC_XOR_ZLIB = 4

CODEC_NAMES = {
    CODEC_RAW: "raw",
    CODEC_RLE: "rle",
    CODEC_XOR_RLE: "xor-rle",
    CODEC_ZLIB: "zlib",
    CODEC_XOR_ZLIB: "xor-zlib",
}
NAME_TO_CODEC = {name: code for code, name in CODEC_NAMES.items()}


class ContainerError(ValueError):
    pass


@dataclass(frozen=True)
class ContainerInfo:
    version: int
    codec: str
    depth: int
    phase_mode: str
    original_size: int
    payload_size: int
    archive_size: int
    crc32_hex: str
    sha256_hex: str
    core_sha256_hex: str
    interaction: str
    reciprocal: str
    duplex_pairs: int
    odd_tail: bool

    def as_dict(self) -> dict[str, object]:
        return {
            "version": self.version,
            "codec": self.codec,
            "depth": self.depth,
            "phase_mode": self.phase_mode,
            "original_size": self.original_size,
            "payload_size": self.payload_size,
            "archive_size": self.archive_size,
            "crc32": self.crc32_hex,
            "sha256": self.sha256_hex,
            "core_sha256": self.core_sha256_hex,
            "interaction": self.interaction,
            "reciprocal": self.reciprocal,
            "duplex_pairs": self.duplex_pairs,
            "odd_tail": self.odd_tail,
            "storage_result": storage_result(self.original_size, self.archive_size),
        }


def encode_varint(value: int) -> bytes:
    if value < 0:
        raise ValueError("varint requires a non-negative integer")
    output = bytearray()
    while True:
        part = value & 127
        value >>= 7
        if value:
            output.append(part | 128)
        else:
            output.append(part)
            return bytes(output)


def decode_varint(data: bytes, offset: int) -> tuple[int, int]:
    value = 0
    shift = 0
    while True:
        if offset >= len(data):
            raise ContainerError("truncated varint")
        part = data[offset]
        offset += 1
        value |= (part & 127) << shift
        if not part & 128:
            return value, offset
        shift += 7
        if shift > 63:
            raise ContainerError("varint is too large")


def rle_encode(data: bytes) -> bytes:
    if not data:
        return b""
    output = bytearray()
    start = 0
    while start < len(data):
        value = data[start]
        end = start + 1
        while end < len(data) and data[end] == value:
            end += 1
        output.extend(encode_varint(end - start))
        output.append(value)
        start = end
    return bytes(output)


def rle_decode(payload: bytes, expected_size: int) -> bytes:
    output = bytearray()
    offset = 0
    while offset < len(payload):
        count, offset = decode_varint(payload, offset)
        if count <= 0:
            raise ContainerError("invalid RLE run")
        if offset >= len(payload):
            raise ContainerError("truncated RLE value")
        value = payload[offset]
        offset += 1
        if len(output) + count > expected_size:
            raise ContainerError("RLE expands beyond declared size")
        output.extend(bytes((value,)) * count)
    if len(output) != expected_size:
        raise ContainerError("RLE size mismatch")
    return bytes(output)


def xor_delta(data: bytes) -> bytes:
    if not data:
        return b""
    output = bytearray(len(data))
    previous = 0
    for index, value in enumerate(data):
        output[index] = value ^ previous
        previous = value
    return bytes(output)


def xor_restore(data: bytes) -> bytes:
    output = bytearray(len(data))
    previous = 0
    for index, value in enumerate(data):
        restored = value ^ previous
        output[index] = restored
        previous = restored
    return bytes(output)


def compress_with(codec: int, data: bytes) -> bytes:
    if codec == CODEC_RAW:
        return data
    if codec == CODEC_RLE:
        return rle_encode(data)
    if codec == CODEC_XOR_RLE:
        return rle_encode(xor_delta(data))
    if codec == CODEC_ZLIB:
        return zlib.compress(data, level=9)
    if codec == CODEC_XOR_ZLIB:
        return zlib.compress(xor_delta(data), level=9)
    raise ContainerError("unknown codec")


def decompress_with(codec: int, payload: bytes, expected_size: int) -> bytes:
    if codec == CODEC_RAW:
        data = payload
    elif codec == CODEC_RLE:
        data = rle_decode(payload, expected_size)
    elif codec == CODEC_XOR_RLE:
        data = xor_restore(rle_decode(payload, expected_size))
    elif codec == CODEC_ZLIB:
        data = zlib.decompress(payload)
    elif codec == CODEC_XOR_ZLIB:
        data = xor_restore(zlib.decompress(payload))
    else:
        raise ContainerError("unknown codec")
    if len(data) != expected_size:
        raise ContainerError("decoded size does not match header")
    return data


def choose_codec(data: bytes, requested: str) -> tuple[int, bytes]:
    if requested != "auto":
        codec = NAME_TO_CODEC[requested]
        return codec, compress_with(codec, data)

    candidates = []
    for codec in sorted(CODEC_NAMES):
        payload = compress_with(codec, data)
        candidates.append((len(payload), codec, payload))
    _, codec, payload = min(candidates, key=lambda item: (item[0], item[1]))
    return codec, payload


def core_path() -> Path:
    return Path(__file__).with_name("raum27_exact_integer_protocol.py")


def core_digest() -> bytes:
    return hashlib.sha256(core_path().read_bytes()).digest()


def phase_turns(left: int, right: int) -> int:
    return (left + right) & 3


def audit_duplex_pairs(data: bytes, depth: int) -> int:
    """Audit every distinct byte pair at most once."""
    unique_pairs: set[tuple[int, int]] = set()
    for offset in range(0, len(data), 2):
        left = data[offset]
        right = data[offset + 1] if offset + 1 < len(data) else 0
        unique_pairs.add((left, right))

    for left, right in unique_pairs:
        turns = phase_turns(left, right)
        packet = encode_duplex(left, right, depth, turns)
        if decode_duplex(packet, turns) != (left, right):
            raise ContainerError(
                "exact duplex audit failed for pair "
                + str((left, right))
            )
    return len(unique_pairs)


def build_archive(data: bytes, depth: int, codec_name: str, audit: bool) -> tuple[bytes, ContainerInfo]:
    if depth < 0:
        raise ValueError("depth must be non-negative")

    if audit:
        audit_duplex_pairs(data, depth)

    codec, payload = choose_codec(data, codec_name)
    original_sha = hashlib.sha256(data).digest()
    original_crc = binascii.crc32(data) & 0xFFFFFFFF
    digest = core_digest()

    variable = b"".join(
        (
            encode_varint(depth),
            encode_varint(len(data)),
            encode_varint(len(payload)),
        )
    )

    fixed = b"".join(
        (
            MAGIC,
            bytes((VERSION, codec, PHASE_PAIR_SUM, 0)),
            PROTOCOL_ID,
            struct.pack(">I", original_crc),
            original_sha,
            digest,
        )
    )
    archive = fixed + variable + payload
    info = ContainerInfo(
        version=VERSION,
        codec=CODEC_NAMES[codec],
        depth=depth,
        phase_mode="pair-sum-z4",
        original_size=len(data),
        payload_size=len(payload),
        archive_size=len(archive),
        crc32_hex=f"{original_crc:08x}",
        sha256_hex=original_sha.hex(),
        core_sha256_hex=digest.hex(),
        interaction=f"{FIRST_INTERACTION[0]}:{FIRST_INTERACTION[1]}",
        reciprocal=f"{RECIPROCAL_INTERACTION[0]}:{RECIPROCAL_INTERACTION[1]}",
        duplex_pairs=(len(data) + 1) // 2,
        odd_tail=bool(len(data) & 1),
    )
    return archive, info


def parse_archive(archive: bytes, require_current_core: bool = True) -> tuple[ContainerInfo, int, bytes, bytes]:
    if len(archive) < FIXED_HEADER_SIZE:
        raise ContainerError("archive is too short")
    if archive[:4] != MAGIC:
        raise ContainerError("wrong magic")

    version, codec, phase_mode, flags = archive[4:8]
    if version != VERSION:
        raise ContainerError("unsupported version")
    if codec not in CODEC_NAMES:
        raise ContainerError("unsupported codec")
    if phase_mode != PHASE_PAIR_SUM:
        raise ContainerError("unsupported phase mode")
    if flags != 0:
        raise ContainerError("unsupported flags")
    if archive[8:16] != PROTOCOL_ID:
        raise ContainerError("wrong protocol identifier")

    crc = struct.unpack(">I", archive[16:20])[0]
    sha = archive[20:52]
    stored_core_sha = archive[52:84]
    offset = 84
    depth, offset = decode_varint(archive, offset)
    original_size, offset = decode_varint(archive, offset)
    payload_size, offset = decode_varint(archive, offset)

    if payload_size != len(archive) - offset:
        raise ContainerError("payload length mismatch")
    if require_current_core and stored_core_sha != core_digest():
        raise ContainerError("container was created with a different core source")

    payload = archive[offset:]
    info = ContainerInfo(
        version=version,
        codec=CODEC_NAMES[codec],
        depth=depth,
        phase_mode="pair-sum-z4",
        original_size=original_size,
        payload_size=payload_size,
        archive_size=len(archive),
        crc32_hex=f"{crc:08x}",
        sha256_hex=sha.hex(),
        core_sha256_hex=stored_core_sha.hex(),
        interaction=f"{FIRST_INTERACTION[0]}:{FIRST_INTERACTION[1]}",
        reciprocal=f"{RECIPROCAL_INTERACTION[0]}:{RECIPROCAL_INTERACTION[1]}",
        duplex_pairs=(original_size + 1) // 2,
        odd_tail=bool(original_size & 1),
    )
    return info, codec, sha, payload


def extract_archive(archive: bytes, audit: bool, require_current_core: bool = True) -> tuple[bytes, ContainerInfo]:
    info, codec, expected_sha, payload = parse_archive(
        archive,
        require_current_core=require_current_core,
    )
    data = decompress_with(codec, payload, info.original_size)
    crc = binascii.crc32(data) & 0xFFFFFFFF
    if f"{crc:08x}" != info.crc32_hex:
        raise ContainerError("CRC32 verification failed")
    if hashlib.sha256(data).digest() != expected_sha:
        raise ContainerError("SHA-256 verification failed")
    if audit:
        audit_duplex_pairs(data, info.depth)
    return data, info


def storage_result(original_size: int, archive_size: int) -> dict[str, object]:
    difference = original_size - archive_size
    if original_size == 0:
        basis_points = 0
    else:
        basis_points = difference * 10000 // original_size
    return {
        "difference_bytes": difference,
        "savings_basis_points": basis_points,
        "savings_percent": format_basis_points(basis_points),
        "actually_smaller": archive_size < original_size,
    }


def format_basis_points(value: int) -> str:
    sign = "-" if value < 0 else ""
    magnitude = -value if value < 0 else value
    return f"{sign}{magnitude // 100}.{magnitude % 100:02d}%"


def print_info(info: ContainerInfo) -> None:
    result = info.as_dict()
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))


def command_pack(args: argparse.Namespace) -> int:
    data = args.input.read_bytes()
    archive, info = build_archive(data, args.depth, args.codec, not args.no_audit)
    args.output.write_bytes(archive)
    print_info(info)
    return 0


def command_unpack(args: argparse.Namespace) -> int:
    data, info = extract_archive(
        args.input.read_bytes(),
        audit=not args.no_audit,
        require_current_core=not args.allow_core_mismatch,
    )
    args.output.write_bytes(data)
    print_info(info)
    return 0


def command_inspect(args: argparse.Namespace) -> int:
    info, _, _, _ = parse_archive(
        args.input.read_bytes(),
        require_current_core=not args.allow_core_mismatch,
    )
    print_info(info)
    return 0


def command_verify(args: argparse.Namespace) -> int:
    _, info = extract_archive(
        args.input.read_bytes(),
        audit=not args.no_audit,
        require_current_core=not args.allow_core_mismatch,
    )
    print_info(info)
    return 0


def command_selftest(args: argparse.Namespace) -> int:
    core_report = run_core_tests()
    if core_report["fatal_error"]:
        raise ContainerError("core self-test failed")

    samples = {
        "empty": b"",
        "one-byte": b"X",
        "all-bytes": bytes(range(256)),
        "repeated": b"RAUM27" * 4096,
        "runs": bytes((0,)) * 8192 + bytes((255,)) * 8192,
        "deterministic-noise": hashlib.shake_256(b"raum27-selftest").digest(8192),
    }
    app_results = []
    for name, sample in samples.items():
        archive, info = build_archive(sample, depth=3, codec_name="auto", audit=True)
        restored, _ = extract_archive(archive, audit=True)
        if restored != sample:
            raise ContainerError("app roundtrip failed: " + name)
        app_results.append(
            {
                "sample": name,
                "original_size": len(sample),
                "archive_size": len(archive),
                "codec": info.codec,
                "actually_smaller": len(archive) < len(sample),
            }
        )

    tampered, _ = build_archive(b"tamper-test" * 100, 3, "auto", True)
    damaged = bytearray(tampered)
    damaged[-1] ^= 1
    tamper_detected = False
    try:
        extract_archive(bytes(damaged), audit=False)
    except (ContainerError, zlib.error):
        tamper_detected = True
    if not tamper_detected:
        raise ContainerError("tamper test failed")

    report = {
        "core": core_report,
        "app_roundtrips": app_results,
        "tamper_detected": tamper_detected,
        "fatal_error": False,
    }
    print(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True))
    if args.report:
        args.report.write_text(
            json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True),
            encoding="utf-8",
        )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Exact integer RAUM27 container application."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    pack = sub.add_parser("pack", help="create an .r27 archive")
    pack.add_argument("input", type=Path)
    pack.add_argument("output", type=Path)
    pack.add_argument("--depth", type=int, default=3)
    pack.add_argument(
        "--codec",
        choices=("auto",) + tuple(NAME_TO_CODEC),
        default="auto",
    )
    pack.add_argument("--no-audit", action="store_true")
    pack.set_defaults(function=command_pack)

    unpack = sub.add_parser("unpack", help="restore the original file")
    unpack.add_argument("input", type=Path)
    unpack.add_argument("output", type=Path)
    unpack.add_argument("--no-audit", action="store_true")
    unpack.add_argument("--allow-core-mismatch", action="store_true")
    unpack.set_defaults(function=command_unpack)

    inspect = sub.add_parser("inspect", help="show archive metadata")
    inspect.add_argument("input", type=Path)
    inspect.add_argument("--allow-core-mismatch", action="store_true")
    inspect.set_defaults(function=command_inspect)

    verify = sub.add_parser("verify", help="verify hashes and protocol pairs")
    verify.add_argument("input", type=Path)
    verify.add_argument("--no-audit", action="store_true")
    verify.add_argument("--allow-core-mismatch", action="store_true")
    verify.set_defaults(function=command_verify)

    selftest = sub.add_parser("selftest", help="run exhaustive core and app tests")
    selftest.add_argument("--report", type=Path)
    selftest.set_defaults(function=command_selftest)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.function(args)
    except (ContainerError, OSError, zlib.error) as error:
        print("error: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
