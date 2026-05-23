#!/usr/bin/env python3
"""Emit deterministic root-cause target fingerprint JSON (LC-S18)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))

from core.knowledge.root_cause_registry_v1 import fingerprint_root_cause_targets  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Fingerprint registered root-cause WHY targets.")
    parser.add_argument(
        "-o",
        "--output",
        required=True,
        help="Output JSON path",
    )
    args = parser.parse_args()
    report = fingerprint_root_cause_targets()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"target_count": report["target_count"], "output": str(out)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
