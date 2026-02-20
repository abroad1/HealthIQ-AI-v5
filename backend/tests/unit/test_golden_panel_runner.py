"""
v5.3 Sprint 6 - Unit tests for GoldenPanelRunner_v1.
"""

import json
from pathlib import Path

from tools.run_golden_panel import (
    _normalise_for_artifact_write,
    run_golden_panel,
)


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_golden_panel_runner_writes_snapshot_pack_with_required_stamps(tmp_path):
    fixture = Path(__file__).parent.parent / "fixtures" / "golden_panel_160.json"
    run_dir, _ = run_golden_panel(
        fixture_path=fixture,
        output_root=tmp_path,
        run_id="unit-golden",
        write_narrative=True,
    )

    analysis_path = run_dir / "analysis_result.json"
    insight_path = run_dir / "insight_graph.json"
    replay_path = run_dir / "replay_manifest.json"
    arbitration_report_path = run_dir / "arbitration_report.json"
    narrative_path = run_dir / "narrative.txt"

    assert analysis_path.exists()
    assert insight_path.exists()
    assert replay_path.exists()
    assert arbitration_report_path.exists()
    assert narrative_path.exists()

    replay = _load_json(replay_path)
    assert replay.get("state_transition_version")
    assert replay.get("state_transition_hash")
    assert replay.get("state_engine_version")
    assert replay.get("state_engine_hash")
    assert replay.get("precedence_engine_version")
    assert replay.get("precedence_engine_hash")
    assert replay.get("causal_layer_version")
    assert replay.get("causal_layer_hash")
    assert replay.get("calibration_version")
    assert replay.get("calibration_hash")
    assert replay.get("arbitration_version")
    assert replay.get("arbitration_hash")
    assert replay.get("conflict_registry_version")
    assert replay.get("conflict_registry_hash")
    assert replay.get("arbitration_registry_version")
    assert replay.get("arbitration_registry_hash")
    assert replay.get("evidence_registry_version")
    assert replay.get("evidence_registry_hash")
    assert "linked_snapshot_ids" in replay
    assert isinstance(replay["linked_snapshot_ids"], list)

    insight = _load_json(insight_path)
    assert isinstance(insight.get("conflict_set", []), list)
    assert isinstance(insight.get("dominance_edges", []), list)
    assert isinstance(insight.get("causal_edges", []), list)
    assert len(insight.get("conflict_set", [])) > 0
    assert len(insight.get("dominance_edges", [])) > 0
    assert len(insight.get("causal_edges", [])) > 0
    assert insight.get("primary_driver_system_id")

    report = _load_json(arbitration_report_path)
    assert "conflict_summary" in report
    assert "precedence_summary" in report
    assert "causal_edges" in report
    assert "arbitration_decisions" in report
    assert "calibration_impact" in report
    assert report["arbitration_decisions"].get("primary_driver_system_id")


def test_golden_panel_runner_artifact_normaliser_strips_volatile_fields():
    payload = {
        "created_at": "2026-01-01T00:00:00Z",
        "elapsed_ms": 101,
        "nested": {"created_at": "2026-01-01T00:00:01Z", "keep": True},
        "insights": [{"id": "x", "created_at": "2026-01-01T00:00:02Z", "text": "ok"}],
    }
    out = _normalise_for_artifact_write(payload)
    assert "created_at" not in out
    assert "elapsed_ms" not in out
    assert "created_at" not in out["nested"]
    assert "created_at" not in out["insights"][0]
