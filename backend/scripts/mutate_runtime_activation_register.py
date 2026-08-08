#!/usr/bin/env python3
"""
V5-CANONICAL-ACTIVATION-GATE-1 — CLI for governed activation-register mutations.

Fail closed. Does not invent medical policy. Launch-critical packages are refused.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Mutate package_runtime_activation_register_v1 via the canonical write path."
    )
    parser.add_argument("--repo", type=Path, default=_REPO)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--add",
        action="append",
        default=[],
        metavar="ACTIVATION_KEY=PACKAGE_ID",
        help="Add an activated frame (repeatable).",
    )
    parser.add_argument(
        "--remove",
        action="append",
        default=[],
        metavar="ACTIVATION_KEY",
        help="Remove an activated frame by activation_key (repeatable).",
    )
    args = parser.parse_args()

    sys.path.insert(0, str(args.repo / "backend"))
    from core.knowledge.activation_register_mutation_v1 import (  # noqa: PLC0415
        mutate_runtime_activation_register,
    )

    add_frames = []
    for item in args.add:
        if "=" not in item:
            print(f"invalid --add value (expected KEY=PACKAGE_ID): {item}", file=sys.stderr)
            return 2
        key, package_id = item.split("=", 1)
        add_frames.append({"activation_key": key.strip(), "package_id": package_id.strip()})

    result = mutate_runtime_activation_register(
        add_frames=add_frames,
        remove_activation_keys=args.remove,
        repo_root=args.repo,
        dry_run=bool(args.dry_run),
    )
    print(
        json.dumps(
            {
                "ok": result.ok,
                "dry_run": result.dry_run,
                "activated_frame_count": result.activated_frame_count,
                "added_keys": result.added_keys,
                "removed_keys": result.removed_keys,
                "errors": result.errors,
            },
            indent=2,
        )
    )
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
