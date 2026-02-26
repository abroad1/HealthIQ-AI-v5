"""
v5.3 Sprint 6 - Unit tests for GoldenPanelRunner_v1.
"""

import json
from pathlib import Path

from core.canonical.normalize import normalize_biomarkers_with_metadata
from core.pipeline.orchestrator import AnalysisOrchestrator, UNIT_NORMALISATION_META_KEY
from core.units.registry import UNIT_REGISTRY_VERSION, apply_unit_normalisation
from tools.run_golden_panel import (
    _normalise_for_artifact_write,
    run_golden_panel,
)


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _biomarker_rows_by_name(analysis_result: dict) -> dict:
    rows = analysis_result.get("biomarkers", []) if isinstance(analysis_result, dict) else []
    out = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        name = str(row.get("biomarker_name", "")).strip()
        if name:
            out[name] = row
    return out


def _prepare_unit_normalised(biomarkers: dict) -> dict:
    normalized = normalize_biomarkers_with_metadata(biomarkers)
    normalized = apply_unit_normalisation(normalized)
    normalized[UNIT_NORMALISATION_META_KEY] = {
        "unit_normalised": True,
        "unit_registry_version": UNIT_REGISTRY_VERSION,
    }
    return normalized


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


def test_regression_golden_derived_markers_have_scored_ranges(tmp_path):
    fixture = Path(__file__).parent.parent / "fixtures" / "golden_panel_160.json"
    run_dir, analysis_result = run_golden_panel(
        fixture_path=fixture,
        output_root=tmp_path,
        run_id="unit-golden-derived-ranges",
        write_narrative=False,
    )
    assert (run_dir / "analysis_result.json").exists()
    by_name = _biomarker_rows_by_name(analysis_result if isinstance(analysis_result, dict) else {})
    for biomarker_name in ("non_hdl_cholesterol", "apoB_apoA1_ratio", "urea_creatinine_ratio"):
        row = by_name.get(biomarker_name)
        assert row is not None, f"Missing biomarker row: {biomarker_name}"
        assert row.get("status") != "unknown", f"{biomarker_name} remains unscored"
        assert row.get("range_source") is None
        assert row.get("interpretation") == "Scored using reference range"
        ref = row.get("reference_range", {})
        assert isinstance(ref, dict)
        assert ref.get("min") is not None
        assert ref.get("max") is not None
        assert str(ref.get("source", "")).lower() == "ratio_registry"


def test_regression_golden_hashes_are_deterministic_with_derived_ranges(tmp_path):
    fixture = Path(__file__).parent.parent / "fixtures" / "golden_panel_160.json"
    run_a, _ = run_golden_panel(
        fixture_path=fixture,
        output_root=tmp_path / "a",
        run_id="unit-golden-derived-a",
        write_narrative=False,
    )
    run_b, _ = run_golden_panel(
        fixture_path=fixture,
        output_root=tmp_path / "b",
        run_id="unit-golden-derived-b",
        write_narrative=False,
    )
    replay_a = _load_json(run_a / "replay_manifest.json")
    replay_b = _load_json(run_b / "replay_manifest.json")
    assert replay_a.get("burden_hash")
    assert replay_a.get("burden_hash") == replay_b.get("burden_hash")
    assert replay_a.get("explainability_hash")
    assert replay_a.get("explainability_hash") == replay_b.get("explainability_hash")


def test_regression_mini_hashes_are_deterministic_with_derived_ranges(tmp_path):
    fixture = Path(__file__).parent.parent / "fixtures" / "golden_panel_sprint14_2_thyroid_immune_mini.json"
    run_a, _ = run_golden_panel(
        fixture_path=fixture,
        output_root=tmp_path / "a-mini",
        run_id="unit-mini-derived-a",
        write_narrative=False,
    )
    run_b, _ = run_golden_panel(
        fixture_path=fixture,
        output_root=tmp_path / "b-mini",
        run_id="unit-mini-derived-b",
        write_narrative=False,
    )
    replay_a = _load_json(run_a / "replay_manifest.json")
    replay_b = _load_json(run_b / "replay_manifest.json")
    assert replay_a.get("burden_hash")
    assert replay_a.get("burden_hash") == replay_b.get("burden_hash")
    assert replay_a.get("explainability_hash")
    assert replay_a.get("explainability_hash") == replay_b.get("explainability_hash")


def test_primary_markers_never_use_policy_or_ssot_ranges():
    prepared = _prepare_unit_normalised(
        {
            "glucose": {
                "value": 105.0,
                "unit": "mg/dL",
            }
        }
    )
    dto = AnalysisOrchestrator().run(
        prepared,
        {"user_id": "00000000-0000-0000-0000-000000000017", "age": 40, "gender": "female"},
        assume_canonical=True,
    )
    row = next((b for b in dto.biomarkers if b.biomarker_name == "glucose"), None)
    assert row is not None
    assert row.status == "unknown"
    assert row.range_source is None
    assert row.interpretation == "Not scored - no reference range available"
    assert row.reference_range is None


def test_derived_ratio_uses_policy_only_when_lab_range_missing():
    prepared = _prepare_unit_normalised(
        {
            "apoB": {
                "value": 1.2,
                "unit": "g/L",
                "reference_range": {"min": 0.6, "max": 1.0, "unit": "g/L", "source": "lab"},
            },
            "apoA1": {
                "value": 1.0,
                "unit": "g/L",
                "reference_range": {"min": 1.1, "max": 1.8, "unit": "g/L", "source": "lab"},
            },
        }
    )
    dto = AnalysisOrchestrator().run(
        prepared,
        {"user_id": "00000000-0000-0000-0000-000000000018", "age": 40, "gender": "female"},
        assume_canonical=True,
    )
    row = next((b for b in dto.biomarkers if b.biomarker_name == "apoB_apoA1_ratio"), None)
    assert row is not None
    assert row.status != "unknown"
    assert row.range_source is None
    assert row.interpretation == "Scored using reference range"
    assert isinstance(row.reference_range, dict)
    assert str(row.reference_range.get("source", "")).lower() == "ratio_registry"


def test_derived_ratio_lab_range_precedence_over_policy():
    prepared = _prepare_unit_normalised(
        {
            "apoB_apoA1_ratio": {
                "value": 1.1,
                "unit": "ratio",
                "reference_range": {"min": 0.0, "max": 2.0, "unit": "ratio", "source": "lab"},
            }
        }
    )
    dto = AnalysisOrchestrator().run(
        prepared,
        {"user_id": "00000000-0000-0000-0000-000000000015", "age": 40, "gender": "female"},
        assume_canonical=True,
    )
    row = next((b for b in dto.biomarkers if b.biomarker_name == "apoB_apoA1_ratio"), None)
    assert row is not None
    assert row.range_source == "lab"
    assert row.interpretation == "Scored using lab reference range"
    assert isinstance(row.reference_range, dict)
    assert str(row.reference_range.get("source", "")).lower() == "lab"


def test_derived_policy_unit_mismatch_is_unscored_with_deterministic_reason(monkeypatch):
    import core.pipeline.orchestrator as orch_mod

    original = dict(orch_mod.DERIVED_RATIO_POLICY_BOUNDS)
    mismatched = dict(original)
    mismatched["non_hdl_cholesterol"] = {
        "min": 0.0,
        "max": 4.0,
        "unit": "ratio",
        "source": "healthiq_policy",
        "notes": "intentional mismatch for test",
    }
    monkeypatch.setattr(orch_mod, "DERIVED_RATIO_POLICY_BOUNDS", mismatched)

    prepared = _prepare_unit_normalised(
        {
            "total_cholesterol": {
                "value": 220.0,
                "unit": "mg/dL",
                "reference_range": {"min": 0.0, "max": 239.0, "unit": "mg/dL", "source": "lab"},
            },
            "hdl_cholesterol": {
                "value": 40.0,
                "unit": "mg/dL",
                "reference_range": {"min": 0.0, "max": 50.0, "unit": "mg/dL", "source": "lab"},
            },
        }
    )
    dto = AnalysisOrchestrator().run(
        prepared,
        {"user_id": "00000000-0000-0000-0000-000000000016", "age": 40, "gender": "female"},
        assume_canonical=True,
    )
    row = next((b for b in dto.biomarkers if b.biomarker_name == "non_hdl_cholesterol"), None)
    assert row is not None
    assert row.status == "unknown"
    assert row.range_source == "policy"
    assert row.interpretation == "Not scored - no compatible policy bounds"


def test_golden_runner_default_mode_does_not_instantiate_gemini(tmp_path, monkeypatch):
    fixture = Path(__file__).parent.parent / "fixtures" / "golden_panel_sprint14_2_thyroid_immune_mini.json"

    def _boom(*args, **kwargs):
        raise AssertionError("GeminiClient must not be instantiated in default NO-LLM mode")

    monkeypatch.setattr("core.insights.synthesis.GeminiClient", _boom)

    run_dir, result = run_golden_panel(
        fixture_path=fixture,
        output_root=tmp_path,
        run_id="unit-mini-no-llm-default",
        write_narrative=False,
    )
    assert (run_dir / "analysis_result.json").exists()
    assert str(result.get("status")) == "completed"
