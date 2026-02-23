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
    explainability_path = run_dir / "explainability_report.json"
    burden_path = run_dir / "burden_vector.json"
    arbitration_report_path = run_dir / "arbitration_report.json"
    narrative_path = run_dir / "narrative.txt"

    assert analysis_path.exists()
    assert insight_path.exists()
    assert replay_path.exists()
    assert explainability_path.exists()
    assert burden_path.exists()
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
    assert replay.get("explainability_version")
    assert replay.get("explainability_hash")
    assert replay.get("explainability_artifact_filename") == "explainability_report.json"
    assert replay.get("bio_stats_engine_version")
    assert replay.get("system_burden_engine_version")
    assert replay.get("influence_propagator_version")
    assert replay.get("capacity_scaler_version")
    assert replay.get("validation_gate_version")
    assert replay.get("burden_hash")
    assert replay.get("burden_artifact_filename") == "burden_vector.json"
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
    assert isinstance(insight.get("influence_order", []), list)
    assert len(insight.get("influence_order", [])) > 0

    explainability = _load_json(explainability_path)
    assert explainability.get("arbitration_decisions", {}).get("primary_driver_system_id")
    assert (
        explainability.get("arbitration_decisions", {}).get("primary_driver_system_id")
        == insight.get("primary_driver_system_id")
    )
    assert explainability.get("dominance_resolution", {}).get("influence_ordering", {}).get("influence_order")
    assert explainability.get("system_burden", {}).get("system_capacity_scores")
    assert explainability.get("replay_stamps", {}).get("burden_hash")

    burden = _load_json(burden_path)
    assert burden.get("raw_system_burden_vector") is not None
    assert burden.get("adjusted_system_burden_vector") is not None
    assert burden.get("system_capacity_scores") is not None
    assert burden.get("burden_hash")

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
