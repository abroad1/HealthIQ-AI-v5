"""
v5.3 Sprint 11 - Explainability report determinism tests.
"""

import json
from pathlib import Path

from tools.run_arbitration_scenarios import run_arbitration_scenarios


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _fixture_path() -> Path:
    return Path(__file__).parent.parent / "fixtures" / "arbitration_scenarios_v2.json"


def _stable_report_payload(report: dict) -> dict:
    payload = dict(report)
    meta = dict(payload.get("run_metadata", {}))
    meta.pop("run_id", None)
    meta.pop("generated_at_utc", None)
    payload["run_metadata"] = meta
    return payload


def test_explainability_report_is_stable_across_repeated_runs(tmp_path):
    fixture = _fixture_path()
    run_a, _ = run_arbitration_scenarios(
        fixture_path=fixture,
        output_root=tmp_path / "a",
        run_id="unit-explainability-a",
        scenario_id=None,
        write_narrative=False,
    )
    run_b, _ = run_arbitration_scenarios(
        fixture_path=fixture,
        output_root=tmp_path / "b",
        run_id="unit-explainability-b",
        scenario_id=None,
        write_narrative=False,
    )

    scen_a = sorted([p.name for p in (run_a / "scenarios").iterdir() if p.is_dir()])
    scen_b = sorted([p.name for p in (run_b / "scenarios").iterdir() if p.is_dir()])
    assert scen_a == scen_b
    for sid in scen_a:
        rep_a = _load_json(run_a / "scenarios" / sid / "explainability_report.json")
        rep_b = _load_json(run_b / "scenarios" / sid / "explainability_report.json")
        assert rep_a["replay_stamps"]["explainability_hash"] == rep_b["replay_stamps"]["explainability_hash"]
        assert rep_a["replay_stamps"]["arbitration_hash"] == rep_b["replay_stamps"]["arbitration_hash"]
        assert _stable_report_payload(rep_a) == _stable_report_payload(rep_b)
