#!/usr/bin/env python3
"""Sanitize F5 BIG-IP SCF files for safe configuration review."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


SENSITIVE_BLOCK_PATTERNS = (
    re.compile(r"^cm\s+cert\s+"),
    re.compile(r"^cm\s+key\s+"),
    re.compile(r"^sys\s+file\s+ssl-key\s+"),
    re.compile(r"^sys\s+file\s+ssl-cert\s+"),
)

SENSITIVE_VALUE_PATTERN = re.compile(
    r"^(\s*)"
    r"(encrypted-password|password|passphrase|secret|master-key)"
    r"\s+.*$",
    re.IGNORECASE,
)


def is_sensitive_block(header: str) -> bool:
    """Return True when an SCF block should be removed completely."""
    stripped = header.lstrip()
    return any(pattern.match(stripped) for pattern in SENSITIVE_BLOCK_PATTERNS)


def sanitize_lines(lines: list[str]) -> tuple[list[str], int, int]:
    """Sanitize SCF content.

    Returns:
        sanitized lines,
        number of removed blocks,
        number of redacted values.
    """
    output: list[str] = []
    removed_blocks = 0
    redacted_values = 0

    index = 0

    while index < len(lines):
        line = lines[index]

        if is_sensitive_block(line):
            removed_blocks += 1

            depth = line.count("{") - line.count("}")
            index += 1

            while index < len(lines) and depth > 0:
                depth += lines[index].count("{")
                depth -= lines[index].count("}")
                index += 1

            output.append("# [REDACTED SENSITIVE BLOCK]\n")
            continue

        sensitive_match = SENSITIVE_VALUE_PATTERN.match(line)

        if sensitive_match:
            indent = sensitive_match.group(1)
            key = sensitive_match.group(2)
            output.append(f"{indent}{key} <REDACTED>\n")
            redacted_values += 1
        else:
            output.append(line)

        index += 1

    return output, removed_blocks, redacted_values


def sanitize_file(source: Path, destination: Path) -> None:
    """Sanitize one SCF file."""
    lines = source.read_text(encoding="utf-8", errors="replace").splitlines(
        keepends=True
    )

    sanitized, removed_blocks, redacted_values = sanitize_lines(lines)

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text("".join(sanitized), encoding="utf-8")

    print(f"Source:          {source}")
    print(f"Destination:     {destination}")
    print(f"Blocks removed:  {removed_blocks}")
    print(f"Values redacted: {redacted_values}")


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Sanitize an F5 BIG-IP SCF for configuration review."
    )

    parser.add_argument(
        "--input",
        required=True,
        type=Path,
        help="Raw BIG-IP SCF file",
    )

    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Destination sanitized SCF file",
    )

    return parser.parse_args()


def main() -> None:
    """Program entry point."""
    args = parse_args()

    if not args.input.is_file():
        raise SystemExit(f"Input file does not exist: {args.input}")

    sanitize_file(args.input, args.output)


if __name__ == "__main__":
    main()