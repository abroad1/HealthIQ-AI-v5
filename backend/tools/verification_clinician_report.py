"""
Compile clinician_report_v1 (with runner_up surfacing) on top of the
orchestrator artifacts already produced under
docs/audit-papers/verification-2026-05-04/artifacts/.

This mirrors what the API path does when serving the frontend.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND = REPO_ROOT / "backend"
sys.path.insert(0, str(BACKEND))

from core.dto.builders import build_analysis_result_dto  # noqa: E402

ART = REPO_ROOT / "docs" / "audit-papers" / "verification-2026-05-04" / "artifacts"
OUT = REPO_ROOT / "docs" / "audit-papers" / "verification-2026-05-04" / "clinician_report_summary.json"


def main() -> int:
    rows = []
    for run_dir in sorted(ART.iterdir()):
        if not run_dir.is_dir():
            continue
        path = run_dir / "analysis_result.json"
        if not path.exists():
            continue
        raw = json.loads(path.read_text(encoding="utf-8"))
        try:
            dto = build_analysis_result_dto(raw)
        except Exception as exc:
            rows.append({"run": run_dir.name, "error": f"{type(exc).__name__}: {exc}"})
            continue
        cr = dto.get("clinician_report_v1") or {}
        sections = cr.get("sections", {}) if isinstance(cr, dict) else {}
        page1 = sections.get("page1", {}) if isinstance(sections, dict) else {}
        root_cause = sections.get("root_cause", {}) if isinstance(sections, dict) else {}
        rc_summary = {
            "signal_id": root_cause.get("signal_id"),
            "signal_state": root_cause.get("signal_state"),
            "signal_confidence": root_cause.get("signal_confidence"),
            "hypothesis_count": len(root_cause.get("hypotheses", [])) if isinstance(root_cause.get("hypotheses"), list) else 0,
        }
        rows.append({
            "run": run_dir.name,
            "primary_concern": page1.get("primary_concern"),
            "primary_concern_mode": page1.get("primary_concern_mode"),
            "co_primary_signal_ids": page1.get("co_primary_signal_ids"),
            "key_findings": page1.get("key_findings"),
            "chains": page1.get("chains"),
            "top_hypothesis_line": page1.get("top_hypothesis_line"),
            "confidence_and_missing_data": page1.get("confidence_and_missing_data"),
            "runner_up_signal_id": page1.get("runner_up_signal_id"),
            "runner_up_topic_line": page1.get("runner_up_topic_line"),
            "runner_up_why_not_lead_line": page1.get("runner_up_why_not_lead_line"),
            "ranking_policy_version": page1.get("ranking_policy_version"),
            "root_cause_section": rc_summary,
            "section_keys": sorted(list(sections.keys())) if isinstance(sections, dict) else [],
        })

    OUT.write_text(json.dumps(rows, indent=2, default=str), encoding="utf-8")
    print(f"WROTE {OUT} (rows={len(rows)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
