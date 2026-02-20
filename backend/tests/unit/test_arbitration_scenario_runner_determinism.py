"""
v5.3 Sprint 10 - Runner-path determinism tests.
"""

import json
from pathlib import Path

from tools.run_arbitration_scenarios import run_arbitration_scenarios


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _fixture_payload(base: Path, scenario_id: str, reverse_order: bool) -> dict:
    src = _load_json(base)
    rows = [row for row in src["scenarios"] if str(row.get("scenario_id", "")) == scenario_id]
    if not rows:
        raise ValueError("scenario id not found")
    row = dict(rows[0])
    state_rows = list(row.get("system_states", []))
    if reverse_order:
        state_rows = list(reversed(state_rows))
    row["system_states"] = state_rows
    return {"scenarios": [row]}


def test_runner_is_invariant_under_system_state_order(tmp_path):
    base = Path(__file__).parent.parent / "fixtures" / "arbitration_scenarios_v2.json"
    left_fixture = tmp_path / "left.json"
    right_fixture = tmp_path / "right.json"
    left_fixture.write_text(
        json.dumps(_fixture_payload(base, "transitive_depth_chain", reverse_order=False), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    right_fixture.write_text(
        json.dumps(_fixture_payload(base, "transitive_depth_chain", reverse_order=True), indent=2, sort_keys=True),
        encoding="utf-8",
    )

    left_dir, _ = run_arbitration_scenarios(
        fixture_path=left_fixture,
        output_root=tmp_path / "left_out",
        run_id="perm-left",
        scenario_id="transitive_depth_chain",
        write_narrative=False,
    )
    right_dir, _ = run_arbitration_scenarios(
        fixture_path=right_fixture,
        output_root=tmp_path / "right_out",
        run_id="perm-right",
        scenario_id="transitive_depth_chain",
        write_narrative=False,
    )

    l_report = _load_json(left_dir / "scenarios" / "transitive_depth_chain" / "arbitration_report.json")
    r_report = _load_json(right_dir / "scenarios" / "transitive_depth_chain" / "arbitration_report.json")
    l_replay = _load_json(left_dir / "scenarios" / "transitive_depth_chain" / "replay_manifest.json")
    r_replay = _load_json(right_dir / "scenarios" / "transitive_depth_chain" / "replay_manifest.json")

    assert l_report["arbitration_decisions"]["primary_driver_system_id"] == r_report["arbitration_decisions"]["primary_driver_system_id"]
    assert l_report["arbitration_decisions"]["decision_trace"] == r_report["arbitration_decisions"]["decision_trace"]
    assert l_report["causal_edges"] == r_report["causal_edges"]
    assert l_report["precedence_summary"] == r_report["precedence_summary"]
    assert l_replay["arbitration_hash"] == r_replay["arbitration_hash"]
