"""
Run baseline (infra-free deterministic) tests.

These tests do not require DB, LLM, or external providers.
Use as a gate for infra-free verification.

Usage:
  python backend/scripts/run_baseline_tests.py

Exit: 0 on pass, non-zero on failure.
"""

import subprocess
import sys
from pathlib import Path


def main() -> int:
    backend = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "tests/enforcement/test_canonical_only.py",
            "tests/unit/test_default_golden_fixture_is_collision_free.py",
            "-v",
        ],
        cwd=backend,
    )
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
