"""
Sentinel Phase 1 — Escaped-defect status: persisted result replay gap.

Defect class: persisted_result_replay
Guard type: status_reporting (Phase 1 placeholder)

Full persisted-result replay (loading a golden run JSON through the current pipeline
validator and asserting schema compatibility + correct frontend rendering) is deferred
to Phase 2+. The blocking gap: the existing persistence e2e test uses mock DB sessions,
and frontend replay requires Playwright.

This test serves as:
  1. A named regression slot in the escaped-defect pack so the gap is visible.
  2. A structural check that the golden run corpus exists and is non-empty.
  3. A basic schema sanity check: each golden run JSON has the minimum expected fields.

Evidence model:
  - trigger: this file / Sentinel regression pack
  - check: golden_runs/ corpus existence + minimum field presence
  - customer impact: old result loaded into new frontend may render broken or silently wrong
  - governance escalation: yes — persistence integrity is a meaning-bearing surface
  - coverage gap: full deterministic DTO schema replay deferred to Phase 2+
"""
import json
import os
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
GOLDEN_RUNS_DIR = REPO_ROOT / "backend" / "artifacts" / "golden_runs"

MINIMUM_RESULT_FIELDS = [
    "analysis_id",
]


@pytest.mark.regression
class TestPersistedResultReplayStatus:
    """Phase 1 status placeholder — persisted result replay gap."""

    def test_coverage_gap_acknowledged(self):
        """
        Explicit gap acknowledgement: full persisted-result replay is not implemented in
        Phase 1. This test records the gap in Sentinel reports. Full DTO schema comparison
        against the golden run corpus is deferred to Phase 2+. Governance escalation: YES.
        """
        assert True  # gap acknowledged

    def test_golden_runs_corpus_exists(self):
        """Golden run artifact directory must exist and be non-empty."""
        assert GOLDEN_RUNS_DIR.exists(), (
            f"COVERAGE GAP: Golden runs corpus not found at {GOLDEN_RUNS_DIR}. "
            f"Persisted-result replay cannot proceed."
        )
        run_dirs = [d for d in GOLDEN_RUNS_DIR.iterdir() if d.is_dir()]
        assert run_dirs, (
            f"COVERAGE GAP: No run directories found in {GOLDEN_RUNS_DIR}. "
            f"Golden run corpus is empty."
        )

    def test_golden_run_jsons_have_minimum_fields(self):
        """
        Each analysis_result.json in the golden run corpus must contain minimum
        expected fields. This is a structural sanity check, not a full schema replay.
        """
        if not GOLDEN_RUNS_DIR.exists():
            pytest.skip("Golden runs corpus not found — skipping schema sanity check")

        import re as _re
        # Only check timestamped run directories (UTC pattern: digits + T + digits + Z)
        # Skip named verification/fixture directories (verify_*, v5.*, etc.)
        _ts_pattern = _re.compile(r'^\d{8}T\d{6}Z$')
        run_dirs = sorted(
            [d for d in GOLDEN_RUNS_DIR.iterdir() if d.is_dir() and _ts_pattern.match(d.name)],
            key=lambda d: d.name,
            reverse=True,
        )
        # Check the 5 most recent timestamped runs to keep this fast
        checked = 0
        failures: list[str] = []
        for run_dir in run_dirs[:5]:
            result_file = run_dir / "analysis_result.json"
            if not result_file.exists():
                continue
            try:
                data = json.loads(result_file.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError) as exc:
                failures.append(f"{result_file}: parse error — {exc}")
                continue
            missing = [f for f in MINIMUM_RESULT_FIELDS if f not in data]
            if missing:
                failures.append(
                    f"{result_file.parent.name}: missing fields {missing}"
                )
            checked += 1

        if checked == 0:
            pytest.skip(
                "COVERAGE GAP: No analysis_result.json files found in recent golden run "
                "directories. Corpus may be empty or differently structured."
            )

        assert not failures, (
            f"Golden run schema sanity check FAIL — {len(failures)} issue(s):\n"
            + "\n".join(failures)
        )

    def test_phase2_replay_gap_reported(self):
        """
        Documents what Phase 2 must add:
          - Load each golden run JSON through the current DTO validator
          - Assert structural compatibility (no missing required fields, no type changes)
          - Assert frontend mock data is in sync with backend DTO schema
          - Playwright: load a stored result in the current frontend and scan for regressions
        This test always passes — it is a documentation anchor.
        """
        phase2_requirements = [
            "DTO schema comparison harness (golden run JSON vs current schema)",
            "Frontend mock sync check (analysis-result.json vs backend DTO)",
            "Playwright: render stored result, assert no slug leakage or broken sections",
        ]
        # Always passes — records the deferred scope
        assert phase2_requirements
