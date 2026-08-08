#!/usr/bin/env python3
"""
V5-RUNTIME-AUTHORITY-INTEGRITY-1 — CLI for runtime medical-authority integrity.

Read-only: does not mutate repository files. Exits non-zero on violation.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate explicit activation prohibitions against runtime activation register."
    )
    parser.add_argument("--repo", type=Path, default=_REPO, help="Repository root")
    args = parser.parse_args()

    sys.path.insert(0, str(args.repo / "backend"))
    from core.knowledge.runtime_medical_authority_integrity_v1 import (  # noqa: PLC0415
        run_runtime_medical_authority_integrity_validation,
    )

    errors = run_runtime_medical_authority_integrity_validation(repo_root=args.repo)
    if errors:
        print("runtime_medical_authority_integrity: FAIL", file=sys.stderr)
        for item in errors:
            print(f"  - {item}", file=sys.stderr)
        return 1
    print("runtime_medical_authority_integrity: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
