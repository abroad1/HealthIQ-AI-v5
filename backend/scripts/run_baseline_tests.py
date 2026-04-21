"""
Run baseline (infra-free deterministic) tests.

These tests do not require DB, LLM, or external providers.
Use as a gate for infra-free verification.

Includes the governed phenotype regression suite (`test_phenotype_suite_v1.py`, KB-S58A)
so phenotype determinism, signal firing, and declared chain/root-cause expectations
cannot bypass the standard gate.

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
            "tests/enforcement/test_retail_explainer_registry_b1b.py",
            "tests/unit/test_default_golden_fixture_is_collision_free.py",
            "tests/unit/test_retail_explainer_b1a.py",
            "tests/unit/test_retail_explainer_b1b.py",
            "tests/unit/test_pathway_explainers_v1.py",
            "tests/unit/test_functional_interpretation_v1.py",
            "tests/unit/test_interpretation_entities_benchmark_v1.py",
            "tests/unit/test_narrative_report_compiler_v1.py",
            "tests/unit/test_phenotype_suite_v1.py",
            "-v",
        ],
        cwd=backend,
    )
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
