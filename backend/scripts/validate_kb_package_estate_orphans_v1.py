#!/usr/bin/env python3
"""LC-S17 — Report Knowledge Bus package estate orphans vs governance inventory."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))

from core.knowledge.kb_lifecycle_contract_v1 import (  # noqa: E402
    assess_package_estate,
    detect_orphan_packages,
)


def main() -> int:
    report = detect_orphan_packages(ROOT)
    assessment = assess_package_estate(ROOT)
    payload = {
        "disk_not_in_inventory": list(report.disk_not_in_inventory),
        "inventory_not_on_disk": list(report.inventory_not_on_disk),
        "has_orphans": report.has_orphans,
        "disk_package_count": assessment.disk_package_count,
        "inventory_package_count": assessment.inventory_package_count,
        "review_queue_count": assessment.review_queue_count,
        "lipid_relevant_orphan_count": len(assessment.lipid_relevant_orphans),
        "duplicate_inventory_package_ids": list(assessment.duplicate_package_ids),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 1 if report.has_orphans else 0


if __name__ == "__main__":
    raise SystemExit(main())
