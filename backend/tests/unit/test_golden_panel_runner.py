"""
v5.3 Sprint 6 - Unit tests for GoldenPanelRunner_v1.
"""

import json
import uuid
from datetime import date, datetime
from pathlib import Path

import pytest
import yaml
from core.analytics.ratio_registry import DERIVED_IDS
from core.analytics.signal_evaluator import SignalRegistry
from core.models.signal import SignalResult
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


def _load_ssot_biomarkers() -> dict:
    ssot_path = Path(__file__).parent.parent.parent / "ssot" / "biomarkers.yaml"
    payload = yaml.safe_load(ssot_path.read_text(encoding="utf-8")) or {}
    return payload.get("biomarkers", {}) if isinstance(payload, dict) else {}


def test_derived_ratio_registry_namespace_is_canonical():
    assert "homa_ir" in DERIVED_IDS
    assert "fib_4" in DERIVED_IDS
    assert "remnant_cholesterol" in DERIVED_IDS
    assert all("." not in rid for rid in DERIVED_IDS)


def test_ssot_contains_tyg_index_with_metabolic_system():
    biomarkers = _load_ssot_biomarkers()
    entry = biomarkers.get("tyg_index")
    assert isinstance(entry, dict)
    assert entry.get("system") == "metabolic"


def test_ssot_fib_4_system_is_liver_not_organ():
    biomarkers = _load_ssot_biomarkers()
    entry = biomarkers.get("fib_4")
    assert isinstance(entry, dict)
    assert entry.get("system") == "liver"
    assert entry.get("system") != "organ"


def test_orchestrator_injects_age_from_valid_questionnaire_dob(monkeypatch):
    captured = {}

    def _spy_compute(panel):
        captured["age"] = panel.get("age")
        return {"registry_version": "test", "derived": {}}

    monkeypatch.setattr("core.pipeline.orchestrator.compute", _spy_compute)
    prepared = _prepare_unit_normalised(
        {
            "glucose": {"value": 95.0, "unit": "mg/dL"},
            "triglycerides": {"value": 140.0, "unit": "mg/dL"},
        }
    )
    dob = "1990-01-01"
    AnalysisOrchestrator().run(
        prepared,
        {"user_id": "00000000-0000-0000-0000-000000000111", "age": 35, "gender": "female"},
        assume_canonical=True,
        questionnaire_data={"date_of_birth": dob},
    )
    expected_age = int((date.today() - date.fromisoformat(dob)).days / 365.25)
    assert captured.get("age") == expected_age
    assert isinstance(captured.get("age"), int)


@pytest.mark.parametrize("dob_value", ["not-a-date", None])
def test_orchestrator_invalid_or_missing_dob_injects_none_without_exception(monkeypatch, dob_value):
    captured = {}

    def _spy_compute(panel):
        captured["age"] = panel.get("age")
        return {"registry_version": "test", "derived": {}}

    monkeypatch.setattr("core.pipeline.orchestrator.compute", _spy_compute)
    prepared = _prepare_unit_normalised(
        {
            "glucose": {"value": 95.0, "unit": "mg/dL"},
            "triglycerides": {"value": 140.0, "unit": "mg/dL"},
        }
    )
    AnalysisOrchestrator().run(
        prepared,
        {"user_id": "00000000-0000-0000-0000-000000000112", "age": 35, "gender": "female"},
        assume_canonical=True,
        questionnaire_data={"date_of_birth": dob_value},
    )
    assert captured.get("age") is None


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

    analysis = _load_json(analysis_path)
    analysis_derived = (analysis.get("derived_markers") or {}).get("derived", {})
    assert "fib_4" in analysis_derived

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
    assert "fib_4" in (insight.get("derived_markers", {}) or {}).get("derived", {})
    assert isinstance(insight.get("signal_results", []), list)
    assert len(insight.get("signal_results", [])) > 0
    assert insight.get("signal_registry_version")
    assert insight.get("signal_registry_hash")
    signal_map = {row["signal_id"]: row["signal_state"] for row in insight.get("signal_results", [])}
    assert signal_map.get("signal_insulin_resistance") == "at_risk"

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
    for biomarker_name in ("non_hdl_cholesterol", "apob_apoa1_ratio", "urea_creatinine_ratio"):
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


def test_standard_golden_panel_exposes_expected_derived_markers(tmp_path):
    fixture = Path(__file__).parent.parent / "fixtures" / "golden_panel_160.json"
    _, analysis_result = run_golden_panel(
        fixture_path=fixture,
        output_root=tmp_path,
        run_id="unit-golden-kb-s13-derived-markers",
        write_narrative=False,
    )
    derived = (analysis_result or {}).get("derived_markers", {}).get("derived", {})
    assert "homa_ir" in derived
    assert "remnant_cholesterol" in derived
    assert "tyg_index" in derived


def test_orchestrator_dob_enables_fib4_and_no_unmapped_age_warning(capsys):
    prepared = _prepare_unit_normalised(
        {
            "glucose": {"value": 5.6, "unit": "mmol/L"},
            "insulin": {"value": 10.0, "unit": "μU/mL"},
            "triglycerides": {"value": 1.8, "unit": "mmol/L"},
            "total_cholesterol": {"value": 5.2, "unit": "mmol/L"},
            "ldl_cholesterol": {"value": 3.0, "unit": "mmol/L"},
            "hdl_cholesterol": {"value": 1.2, "unit": "mmol/L"},
            "ast": {"value": 40.0, "unit": "U/L"},
            "alt": {"value": 20.0, "unit": "U/L"},
            "platelets": {"value": 200.0, "unit": "K/μL"},
        }
    )
    dto = AnalysisOrchestrator().run(
        prepared,
        {"user_id": "00000000-0000-0000-0000-000000000113", "age": 35, "gender": "female"},
        assume_canonical=True,
        questionnaire_data={"date_of_birth": "1990-01-01"},
    )
    derived = (dto.derived_markers or {}).get("derived", {})
    assert "fib_4" in derived
    assert "homa_ir" in derived
    assert "remnant_cholesterol" in derived
    assert "tyg_index" in derived

    captured = capsys.readouterr()
    combined = f"{captured.out}\n{captured.err}"
    assert "unmapped_age" not in combined
    assert "Warning: Unmapped biomarker keys" not in combined


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


def test_one_sided_lab_ranges_are_preserved_in_output_dto(tmp_path):
    fixture_path = tmp_path / "one-sided-lab-ranges.json"
    fixture_payload = {
        "biomarkers": {
            "hba1c": {
                "value": 26.0,
                "unit": "mmol/mol",
                "reference_range": {"min": None, "max": 39.0, "unit": "mmol/mol", "source": "lab"},
            },
            "ldl_cholesterol": {
                "value": 2.75,
                "unit": "mmol/L",
                "reference_range": {"min": None, "max": 2.59, "unit": "mmol/L", "source": "lab"},
            },
            "hdl_cholesterol": {
                "value": 2.22,
                "unit": "mmol/L",
                "reference_range": {"min": 1.55, "max": None, "unit": "mmol/L", "source": "lab"},
            },
            "triglycerides": {
                "value": 0.68,
                "unit": "mmol/L",
                "reference_range": {"min": None, "max": 1.7, "unit": "mmol/L", "source": "lab"},
            },
            "total_cholesterol": {
                "value": 5.26,
                "unit": "mmol/L",
                "reference_range": {"min": 0.0, "max": 5.18, "unit": "mmol/L", "source": "lab"},
            },
        },
        "user": {"age": 58, "biological_sex": "male"},
    }
    fixture_path.write_text(json.dumps(fixture_payload), encoding="utf-8")

    _, analysis_result = run_golden_panel(
        fixture_path=fixture_path,
        output_root=tmp_path,
        run_id="unit-one-sided-ranges",
        write_narrative=False,
    )
    rows = _biomarker_rows_by_name(analysis_result)

    for biomarker_name in ("hba1c", "ldl_cholesterol", "hdl_cholesterol", "triglycerides"):
        row = rows.get(biomarker_name)
        assert isinstance(row, dict), f"Missing biomarker row for {biomarker_name}"
        ref = row.get("reference_range")
        assert isinstance(ref, dict), f"Expected preserved reference_range for {biomarker_name}"
        assert ref.get("source") == "lab"
        assert row.get("range_source") == "lab"
        assert row.get("interpretation") != "Not scored - no reference range available"

    # Regression: two-sided ranges remain carried and scoreable.
    tc_row = rows.get("total_cholesterol")
    assert isinstance(tc_row, dict)
    tc_ref = tc_row.get("reference_range")
    assert isinstance(tc_ref, dict)
    assert tc_ref.get("min") == 0.0
    assert tc_ref.get("max") == 5.18
    assert tc_ref.get("source") == "lab"
    assert tc_row.get("range_source") == "lab"


def test_ab_profile_fixture_pass_through_and_hba1c_band_label(tmp_path):
    fixture = Path(__file__).parent.parent / "fixtures" / "panels" / "ab_full_panel_with_profiles.json"
    _, analysis_result = run_golden_panel(
        fixture_path=fixture,
        output_root=tmp_path,
        run_id="unit-ab-profiles-pass-through",
        write_narrative=False,
    )
    rows = _biomarker_rows_by_name(analysis_result)

    hba1c = rows.get("hba1c")
    assert isinstance(hba1c, dict)
    profile = hba1c.get("reference_profile")
    assert isinstance(profile, dict)
    assert profile.get("source") == "lab"
    assert profile.get("effective_from") == "2024-09-11"
    assert "bands" in profile and isinstance(profile["bands"], list)
    assert hba1c.get("lab_band_label") == "Normal"

    # KB-S26 regression: one-sided range still preserved on output rows.
    ldl = rows.get("ldl_cholesterol")
    assert isinstance(ldl, dict)
    ldl_ref = ldl.get("reference_range")
    assert isinstance(ldl_ref, dict)
    assert ldl_ref.get("min") is None
    assert ldl_ref.get("max") == 2.59
    assert ldl_ref.get("source") == "lab"


def test_band_classifier_sets_middle_band_label_from_profile(tmp_path):
    fixture_path = tmp_path / "middle-band-profile.json"
    fixture_payload = {
        "biomarkers": {
            "hba1c": {
                "value": 42.0,
                "unit": "mmol/mol",
                "reference_range": {"min": None, "max": 39.0, "unit": "mmol/mol", "source": "lab"},
                "reference_profile": {
                    "source": "lab",
                    "effective_from": "2024-09-11",
                    "note": "Band test fixture",
                    "bands": [
                        {"label": "Normal", "min": None, "max": 39.0, "unit": "mmol/mol"},
                        {"label": "Prediabetes", "min": 39.0, "max": 48.0, "unit": "mmol/mol"},
                        {"label": "Diabetic", "min": 48.0, "max": None, "unit": "mmol/mol"},
                    ],
                },
            },
        },
        "user": {"age": 58, "biological_sex": "male"},
    }
    fixture_path.write_text(json.dumps(fixture_payload), encoding="utf-8")

    _, analysis_result = run_golden_panel(
        fixture_path=fixture_path,
        output_root=tmp_path,
        run_id="unit-band-middle",
        write_narrative=False,
    )
    row = _biomarker_rows_by_name(analysis_result).get("hba1c")
    assert isinstance(row, dict)
    assert row.get("lab_band_label") == "Prediabetes"


def test_malformed_bands_yield_null_label_without_pipeline_crash(tmp_path):
    fixture_path = tmp_path / "malformed-band-profile.json"
    fixture_payload = {
        "biomarkers": {
            "hba1c": {
                "value": 42.0,
                "unit": "mmol/mol",
                "reference_range": {"min": None, "max": 39.0, "unit": "mmol/mol", "source": "lab"},
                "reference_profile": {
                    "source": "lab",
                    "effective_from": "2024-09-11",
                    "note": "Malformed overlap fixture",
                    "bands": [
                        {"label": "BandA", "min": 30.0, "max": 50.0, "unit": "mmol/mol"},
                        {"label": "BandB", "min": 40.0, "max": 60.0},
                    ],
                },
            },
        },
        "user": {"age": 58, "biological_sex": "male"},
    }
    fixture_path.write_text(json.dumps(fixture_payload), encoding="utf-8")

    _, analysis_result = run_golden_panel(
        fixture_path=fixture_path,
        output_root=tmp_path,
        run_id="unit-band-malformed",
        write_narrative=False,
    )
    row = _biomarker_rows_by_name(analysis_result).get("hba1c")
    assert isinstance(row, dict)
    assert isinstance(row.get("reference_profile"), dict)
    assert row.get("lab_band_label") is None


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
    row = next((b for b in dto.biomarkers if b.biomarker_name == "apob_apoa1_ratio"), None)
    assert row is not None
    assert row.status != "unknown"
    assert row.range_source is None
    assert row.interpretation == "Scored using reference range"
    assert isinstance(row.reference_range, dict)
    assert str(row.reference_range.get("source", "")).lower() == "ratio_registry"


def test_derived_ratio_lab_range_precedence_over_policy():
    prepared = _prepare_unit_normalised(
        {
            "apob_apoa1_ratio": {
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
    row = next((b for b in dto.biomarkers if b.biomarker_name == "apob_apoa1_ratio"), None)
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


def test_golden_panel_insight_graph_exposes_signal_fields(tmp_path):
    fixture = Path(__file__).parent.parent / "fixtures" / "golden_panel_160.json"
    run_dir, _ = run_golden_panel(
        fixture_path=fixture,
        output_root=tmp_path,
        run_id="unit-golden-signals",
        write_narrative=False,
    )
    insight = _load_json(run_dir / "insight_graph.json")
    assert "signal_registry_version" in insight
    assert "signal_registry_hash" in insight
    assert isinstance(insight.get("signal_results", []), list)


def test_golden_panel_signal_results_carry_explanation_metadata(tmp_path, monkeypatch):
    fixture = Path(__file__).parent.parent / "fixtures" / "golden_panel_160.json"

    def _stub_evaluate_all(self, signal_biomarkers, signal_derived, lab_ranges, reference_profiles=None):
        return [
            SignalResult(
                signal_id="signal_homocysteine_elevation_context",
                system="vascular",
                signal_state="suboptimal",
                signal_value=12.4,
                confidence=None,
                primary_metric="homocysteine",
                supporting_markers=["vitamin_b12", "folate", "transferrin", "mcv", "crp"],
                explanation={
                    "mechanism": "Homocysteine elevation may reflect methylation strain.",
                    "biological_pathway": "One-carbon metabolism and remethylation.",
                    "interpretation": "Context suggests B-vitamin and transport interactions.",
                    "implications": "Potential endothelial stress if persistent.",
                    "supporting_marker_roles": {
                        "vitamin_b12": "Cofactor for remethylation.",
                        "folate": "Methyl donor support.",
                        "transferrin": "Nutrient transport context.",
                        "mcv": "Macrocytic context marker.",
                        "crp": "Inflammatory context marker.",
                    },
                },
            )
        ]

    monkeypatch.setattr("core.analytics.signal_evaluator.SignalEvaluator.evaluate_all", _stub_evaluate_all)
    run_dir, _ = run_golden_panel(
        fixture_path=fixture,
        output_root=tmp_path,
        run_id="unit-golden-signal-explanation",
        write_narrative=False,
    )
    insight = _load_json(run_dir / "insight_graph.json")
    row = next(
        (
            item
            for item in insight.get("signal_results", [])
            if item.get("signal_id") == "signal_homocysteine_elevation_context"
        ),
        None,
    )
    assert isinstance(row, dict)
    assert isinstance(row.get("explanation"), dict)
    assert "mechanism" in row["explanation"]


def test_golden_panel_signal_fields_are_deterministic_across_runs(tmp_path, monkeypatch):
    fixed_analysis_id = uuid.UUID("00000000-0000-0000-0000-000000000160")
    monkeypatch.setattr(uuid, "uuid4", lambda: fixed_analysis_id)
    fixture = Path(__file__).parent.parent / "fixtures" / "golden_panel_160.json"
    run_a, _ = run_golden_panel(
        fixture_path=fixture,
        output_root=tmp_path / "signals-a",
        run_id="unit-golden-signals-a",
        write_narrative=False,
    )
    run_b, _ = run_golden_panel(
        fixture_path=fixture,
        output_root=tmp_path / "signals-b",
        run_id="unit-golden-signals-b",
        write_narrative=False,
    )
    insight_a = _load_json(run_a / "insight_graph.json")
    insight_b = _load_json(run_b / "insight_graph.json")
    assert insight_a.get("signal_registry_version") == insight_b.get("signal_registry_version")
    assert insight_a.get("signal_registry_hash") == insight_b.get("signal_registry_hash")
    assert insight_a.get("signal_results", []) == insight_b.get("signal_results", [])
    replay_a = _load_json(run_a / "replay_manifest.json")
    replay_b = _load_json(run_b / "replay_manifest.json")
    assert replay_a["schema_hashes"]["insight_graph_hash"] == replay_b["schema_hashes"]["insight_graph_hash"]


def test_golden_panel_lab_range_activation_signal_appears_in_signal_results(tmp_path, monkeypatch):
    fixture_path = tmp_path / "lab-range-panel.json"
    fixture_path.write_text(
        json.dumps(
            {
                "biomarkers": {
                    "homocysteine": {
                        "value": 16.0,
                        "unit": "umol/L",
                        "reference_range": {"min": 4.0, "max": 14.0, "unit": "umol/L", "source": "lab"},
                    }
                },
                "user": {"age": 58, "biological_sex": "female"},
            }
        ),
        encoding="utf-8",
    )

    original_get_all = SignalRegistry.get_all_signals

    def _lab_range_signals(self):
        signals = original_get_all(self)
        signals.append(
            {
                "signal_id": "signal_hcy_lab_range_test",
                "system": "vascular",
                "primary_metric": "homocysteine",
                "activation_logic": "lab_range_exceeded",
                "activation_config": {
                    "upper_bound_state": "at_risk",
                    "enable_lower_bound": False,
                },
                "thresholds": [{"severity": "at_risk", "operator": ">=", "value": 9999.0}],
                "override_rules": [],
                "output": {"supporting_markers": []},
            }
        )
        return signals

    monkeypatch.setattr("core.analytics.signal_evaluator.SignalRegistry.get_all_signals", _lab_range_signals)
    run_dir, _ = run_golden_panel(
        fixture_path=fixture_path,
        output_root=tmp_path,
        run_id="unit-golden-lab-range-signal",
        write_narrative=False,
    )
    insight = _load_json(run_dir / "insight_graph.json")
    signal_map = {row["signal_id"]: row["signal_state"] for row in insight.get("signal_results", [])}
    assert signal_map.get("signal_hcy_lab_range_test") == "at_risk"


def test_golden_panel_lab_range_activation_signal_is_deterministic_across_runs(tmp_path, monkeypatch):
    fixture_path = tmp_path / "lab-range-panel-det.json"
    fixture_path.write_text(
        json.dumps(
            {
                "biomarkers": {
                    "homocysteine": {
                        "value": 16.0,
                        "unit": "umol/L",
                        "reference_range": {"min": 4.0, "max": 14.0, "unit": "umol/L", "source": "lab"},
                    }
                },
                "user": {"age": 58, "biological_sex": "female"},
            }
        ),
        encoding="utf-8",
    )

    original_get_all = SignalRegistry.get_all_signals

    def _lab_range_signals(self):
        signals = original_get_all(self)
        signals.append(
            {
                "signal_id": "signal_hcy_lab_range_test",
                "system": "vascular",
                "primary_metric": "homocysteine",
                "activation_logic": "lab_range_exceeded",
                "activation_config": {
                    "upper_bound_state": "at_risk",
                    "enable_lower_bound": False,
                },
                "thresholds": [{"severity": "at_risk", "operator": ">=", "value": 9999.0}],
                "override_rules": [],
                "output": {"supporting_markers": []},
            }
        )
        return signals

    monkeypatch.setattr("core.analytics.signal_evaluator.SignalRegistry.get_all_signals", _lab_range_signals)
    run_a, _ = run_golden_panel(
        fixture_path=fixture_path,
        output_root=tmp_path / "a",
        run_id="unit-golden-lab-range-a",
        write_narrative=False,
    )
    run_b, _ = run_golden_panel(
        fixture_path=fixture_path,
        output_root=tmp_path / "b",
        run_id="unit-golden-lab-range-b",
        write_narrative=False,
    )
    insight_a = _load_json(run_a / "insight_graph.json")
    insight_b = _load_json(run_b / "insight_graph.json")
    assert insight_a.get("signal_results", []) == insight_b.get("signal_results", [])


@pytest.mark.parametrize(
    "fixture_name",
    [
        "ab_full_panel_with_ranges.json",
        "vr_full_panel_with_ranges.json",
    ],
)
def test_report_v1_present_and_stable_for_ab_vr_panels(tmp_path, fixture_name):
    fixture = Path(__file__).parent.parent / "fixtures" / "panels" / fixture_name
    run_a, _ = run_golden_panel(
        fixture_path=fixture,
        output_root=tmp_path / "a",
        run_id=f"unit-report-v1-{fixture.stem}-a",
        write_narrative=False,
    )
    run_b, _ = run_golden_panel(
        fixture_path=fixture,
        output_root=tmp_path / "b",
        run_id=f"unit-report-v1-{fixture.stem}-b",
        write_narrative=False,
    )

    report_a = (_load_json(run_a / "insight_graph.json") or {}).get("report_v1", {})
    report_b = (_load_json(run_b / "insight_graph.json") or {}).get("report_v1", {})
    assert isinstance(report_a, dict) and report_a
    assert isinstance(report_b, dict) and report_b
    generated_a = str((report_a.get("meta") or {}).get("generated_at", "")).strip()
    generated_b = str((report_b.get("meta") or {}).get("generated_at", "")).strip()
    assert generated_a
    assert generated_b
    assert generated_a.endswith("Z")
    assert generated_b.endswith("Z")
    datetime.fromisoformat(generated_a.replace("Z", "+00:00"))
    datetime.fromisoformat(generated_b.replace("Z", "+00:00"))

    # generated_at is expected to differ between runs; everything else is deterministic.
    meta_a = dict(report_a.get("meta", {}) or {})
    meta_b = dict(report_b.get("meta", {}) or {})
    meta_a.pop("generated_at", None)
    meta_b.pop("generated_at", None)
    report_a["meta"] = meta_a
    report_b["meta"] = meta_b

    assert report_a == report_b
