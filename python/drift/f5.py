#!/usr/bin/env python3
"""Compare F5 BIG-IP inventory snapshots and report configuration drift."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


COLLECTIONS = (
    "devices",
    "device_groups",
    "interfaces",
    "vlans",
    "self_ips",
    "virtual_servers",
    "pools",
    "nodes",
)


def object_identity(item: dict[str, Any]) -> str:
    """Return the most useful stable identity for an F5 object."""
    for key in ("full_path", "name", "hostname", "address"):
        value = item.get(key)
        if value:
            return str(value)

    return json.dumps(item, sort_keys=True)


def index_collection(items: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Index a collection of F5 objects by stable identity."""
    return {object_identity(item): item for item in items}


def compare_collection(
    before: list[dict[str, Any]],
    after: list[dict[str, Any]],
) -> dict[str, list[Any]]:
    """Compare one F5 object collection."""
    before_index = index_collection(before)
    after_index = index_collection(after)

    before_keys = set(before_index)
    after_keys = set(after_index)

    added = sorted(after_keys - before_keys)
    removed = sorted(before_keys - after_keys)

    modified = []

    for key in sorted(before_keys & after_keys):
        if before_index[key] != after_index[key]:
            modified.append(
                {
                    "object": key,
                    "before": before_index[key],
                    "after": after_index[key],
                }
            )

    return {
        "added": added,
        "removed": removed,
        "modified": modified,
    }


def compare_snapshots(
    before: dict[str, Any],
    after: dict[str, Any],
) -> dict[str, Any]:
    """Compare two F5 inventory snapshots."""
    result: dict[str, Any] = {
        "before": before.get("metadata", {}),
        "after": after.get("metadata", {}),
        "collections": {},
    }

    for collection in COLLECTIONS:
        result["collections"][collection] = compare_collection(
            before.get(collection, []),
            after.get(collection, []),
        )

    return result


def load_snapshot(path: Path) -> dict[str, Any]:
    """Load one JSON inventory snapshot."""
    with path.open("r", encoding="utf-8") as file_handle:
        return json.load(file_handle)


def has_drift(result: dict[str, Any]) -> bool:
    """Return True when any infrastructure drift was detected."""
    for changes in result["collections"].values():
        if changes["added"] or changes["removed"] or changes["modified"]:
            return True

    return False


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Compare two F5 BIG-IP inventory snapshots."
    )

    parser.add_argument(
        "--before",
        required=True,
        type=Path,
        help="Older F5 JSON snapshot",
    )

    parser.add_argument(
        "--after",
        required=True,
        type=Path,
        help="Newer F5 JSON snapshot",
    )

    parser.add_argument(
        "--output",
        type=Path,
        help="Optional JSON file for drift results",
    )

    args = parser.parse_args()

    before = load_snapshot(args.before)
    after = load_snapshot(args.after)

    result = compare_snapshots(before, after)

    output = json.dumps(result, indent=2, sort_keys=True)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(f"{output}\n", encoding="utf-8")

    print(output)

    if has_drift(result):
        print("\nDrift detected.")
    else:
        print("\nNo drift detected.")


if __name__ == "__main__":
    main()