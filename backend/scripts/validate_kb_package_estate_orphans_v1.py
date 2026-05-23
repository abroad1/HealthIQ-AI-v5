#!/usr/bin/env python3
"""LC-S17 — Report Knowledge Bus package estate orphans vs governance inventory."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))

from core.knowledge.kb_lifecycle_contract_v1 import detect_orphan_packages  # noqa: E402


def main() -> int:
    report = detect_orphan_packages(ROOT)
    payload = {
        "disk_not_in_inventory": list(report.disk_not_in_inventory),
        "inventory_not_on_disk": list(report.inventory_not_on_disk),
        "has_orphans": report.has_orphans,
    }
    print(json.dumps(payload, indent=2))
    return 1 if report.has_orphans else 0


if __name__ == "__main__":
    raise SystemExit(main())
