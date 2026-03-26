import json
from pathlib import Path

import pytest
import yaml

from core.analytics.root_cause_compiler_v1 import compile_root_cause_v1
from tools.run_golden_panel import run_golden_panel


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _finding_by_signal(root_cause: dict, signal_id: str):
    findings = root_cause.get("findings", []) if isinstance(root_cause, dict) else []
    for finding in findings:
        if isinstance(finding, dict) and str(finding.get("signal_id", "")).strip() == signal_id:
            return finding
    return None


@pytest.mark.parametrize(
    "fixture_name",
    [
        "ab_full_panel_with_ranges.json",
        "vr_full_panel_with_ranges.json",
    ],
)
def test_root_cause_v1_present_for_homocysteine_and_non_regression(tmp_path, fixture_name):
    fixture = Path(__file__).parent.parent / "fixtures" / "panels" / fixture_name
    run_a, _ = run_golden_panel(
        fixture_path=fixture,
        output_root=tmp_path / "a",
        run_id=f"unit-root-cause-{fixture.stem}-a",
        write_narrative=False,
    )
    run_b, _ = run_golden_panel(
        fixture_path=fixture,
        output_root=tmp_path / "b",
        run_id=f"unit-root-cause-{fixture.stem}-b",
        write_narrative=False,
    )

    insight_a = _load_json(run_a / "insight_graph.json") or {}
    insight_b = _load_json(run_b / "insight_graph.json") or {}
    report_a = insight_a.get("report_v1") or {}
    report_b = insight_b.get("report_v1") or {}
    root_a = report_a.get("root_cause_v1")
    root_b = report_b.get("root_cause_v1")

    assert isinstance(root_a, dict)
    assert isinstance(root_b, dict)
    assert root_a.get("version") == "v1"
    assert root_b.get("version") == "v1"
    finding = _finding_by_signal(root_a, "signal_homocysteine_elevation_context")
    assert isinstance(finding, dict)
    assert finding.get("signal_id") == "signal_homocysteine_elevation_context"
    hypotheses = finding.get("hypotheses", [])
    assert len(hypotheses) >= 3
    assert any(float(h.get("hypothesis_confidence", 0.0)) >= 0.40 for h in hypotheses if isinstance(h, dict))

    # Non-regression guards: signal and intervention outputs remain deterministic and unchanged.
    assert insight_a.get("signal_results", []) == insight_b.get("signal_results", [])
    assert report_a.get("actions", {}).get("interventions", []) == report_b.get("actions", {}).get("interventions", [])


def test_root_cause_v1_homocysteine_finding_absent_when_context_signal_not_fired(tmp_path):
    fixture = Path(__file__).parent.parent / "fixtures" / "golden_panel_160.json"
    run_dir, _ = run_golden_panel(
        fixture_path=fixture,
        output_root=tmp_path / "absent",
        run_id="unit-root-cause-absent",
        write_narrative=False,
    )
    report = (_load_json(run_dir / "insight_graph.json") or {}).get("report_v1", {})
    root_cause = report.get("root_cause_v1") or {}
    findings = root_cause.get("findings") or []
    hcy_finding = _finding_by_signal(root_cause, "signal_homocysteine_elevation_context")
    assert hcy_finding is None
    # Other governed targets (e.g. systemic inflammation) may still emit findings on this panel.
    assert isinstance(findings, list)


def test_root_cause_v1_text_fields_respect_safety_denylist(tmp_path):
    fixture = Path(__file__).parent.parent / "fixtures" / "panels" / "ab_full_panel_with_ranges.json"
    run_dir, _ = run_golden_panel(
        fixture_path=fixture,
        output_root=tmp_path / "denylist",
        run_id="unit-root-cause-denylist",
        write_narrative=False,
    )
    insight = _load_json(run_dir / "insight_graph.json") or {}
    root_cause = ((insight.get("report_v1") or {}).get("root_cause_v1") or {})
    findings = root_cause.get("findings", [])
    assert findings

    rules_path = Path(__file__).resolve().parents[3] / "knowledge_bus" / "interventions" / "safety_rules_v1.yaml"
    rules = yaml.safe_load(rules_path.read_text(encoding="utf-8")) or {}
    denylist = [str(x).lower() for x in rules.get("denylist_phrases", [])]

    text_fields = []
    for finding in findings:
        for hypothesis in finding.get("hypotheses", []):
            text_fields.append(str(hypothesis.get("title", "")))
            text_fields.append(str(hypothesis.get("summary", "")))
            for item in hypothesis.get("evidence_for", []):
                text_fields.append(str(item.get("item", "")))
            for item in hypothesis.get("evidence_against", []):
                text_fields.append(str(item.get("item", "")))
            for item in hypothesis.get("missing_data", []):
                text_fields.append(str(item.get("reason", "")))
            for item in hypothesis.get("confirmatory_tests", []):
                text_fields.append(str(item.get("rationale", "")))
    lowered = "\n".join(text_fields).lower()
    for phrase in denylist:
        assert phrase not in lowered


def test_confirmatory_test_suppression_and_repeat_behavior_for_ab_panel(tmp_path):
    fixture = Path(__file__).parent.parent / "fixtures" / "panels" / "ab_full_panel_with_ranges.json"
    run_dir, _ = run_golden_panel(
        fixture_path=fixture,
        output_root=tmp_path / "suppression",
        run_id="unit-root-cause-suppression-ab",
        write_narrative=False,
    )
    insight = _load_json(run_dir / "insight_graph.json") or {}
    root_cause = (insight.get("report_v1") or {}).get("root_cause_v1") or {}
    findings = root_cause.get("findings") or []
    hcy_finding = _finding_by_signal(root_cause, "signal_homocysteine_elevation_context")
    assert isinstance(hcy_finding, dict)
    hypotheses = hcy_finding.get("hypotheses", [])
    by_id = {str(h.get("hypothesis_id", "")).strip(): h for h in hypotheses if isinstance(h, dict)}
    b12 = by_id.get("hcy_b12_pattern_v1")
    assert isinstance(b12, dict)
    tests = {str(t.get("test_id", "")).strip() for t in (b12.get("confirmatory_tests") or []) if isinstance(t, dict)}

    # Present in AB panel -> should be suppressed.
    assert "test_serum_vitamin_b12_v1" not in tests
    assert "test_holotranscobalamin_active_b12_v1" not in tests
    # Absent in AB panel -> should remain.
    assert "test_methylmalonic_acid_v1" in tests
    # Repeat tests should not be suppressed.
    folate = by_id.get("hcy_folate_pattern_v1")
    assert isinstance(folate, dict)
    folate_tests = {
        str(t.get("test_id", "")).strip()
        for t in (folate.get("confirmatory_tests") or [])
        if isinstance(t, dict)
    }
    assert "test_homocysteine_repeat_v1" in folate_tests


def test_confirmatory_test_suppression_output_is_deterministic_for_ab_panel(tmp_path):
    fixture = Path(__file__).parent.parent / "fixtures" / "panels" / "ab_full_panel_with_ranges.json"
    run_a, _ = run_golden_panel(
        fixture_path=fixture,
        output_root=tmp_path / "det-a",
        run_id="unit-root-cause-suppression-det-a",
        write_narrative=False,
    )
    run_b, _ = run_golden_panel(
        fixture_path=fixture,
        output_root=tmp_path / "det-b",
        run_id="unit-root-cause-suppression-det-b",
        write_narrative=False,
    )
    root_a = ((_load_json(run_a / "insight_graph.json") or {}).get("report_v1") or {}).get("root_cause_v1")
    root_b = ((_load_json(run_b / "insight_graph.json") or {}).get("report_v1") or {}).get("root_cause_v1")
    assert root_a == root_b


def test_root_cause_v1_hba1c_hypotheses_emit_for_hba1c_signal():
    root = compile_root_cause_v1(
        signal_results=[
            {
                "signal_id": "signal_hba1c_high",
                "signal_state": "at_risk",
                "confidence": 0.81,
                "primary_metric": "hba1c",
            }
        ],
        biomarker_context={
            "hba1c": {"value": 49.0},
            "glucose": {"value": 7.2},
            "triglycerides": {"value": 2.1},
            "hdl_cholesterol": {"value": 0.9},
        },
        input_reference_ranges={
            "hba1c": {"min": 20.0, "max": 42.0},
            "glucose": {"min": 3.9, "max": 5.5},
            "triglycerides": {"min": 0.4, "max": 1.7},
            "hdl_cholesterol": {"min": 1.0, "max": 3.0},
        },
    )
    dump = root.model_dump() if root is not None else {}
    finding = _finding_by_signal(dump, "signal_hba1c_high")
    assert isinstance(finding, dict)
    hypothesis_ids = {
        str(h.get("hypothesis_id", "")).strip()
        for h in (finding.get("hypotheses") or [])
        if isinstance(h, dict)
    }
    assert "hba1c_glycaemic_exposure_pattern_v1" in hypothesis_ids
    assert "hba1c_lipid_coupling_context_v1" in hypothesis_ids


def test_root_cause_v1_alt_hypotheses_emit_for_alt_signal():
    root = compile_root_cause_v1(
        signal_results=[
            {
                "signal_id": "signal_hepatic_alt_context",
                "signal_state": "at_risk",
                "confidence": 0.74,
                "primary_metric": "alt",
            }
        ],
        biomarker_context={
            "alt": {"value": 95.0},
            "ast": {"value": 62.0},
            "ggt": {"value": 71.0},
            "crp": {"value": 4.0},
        },
        input_reference_ranges={
            "alt": {"min": 10.0, "max": 45.0},
            "ast": {"min": 10.0, "max": 40.0},
            "ggt": {"min": 10.0, "max": 55.0},
            "crp": {"min": 0.0, "max": 3.0},
        },
    )
    dump = root.model_dump() if root is not None else {}
    finding = _finding_by_signal(dump, "signal_hepatic_alt_context")
    assert isinstance(finding, dict)
    hypothesis_ids = {
        str(h.get("hypothesis_id", "")).strip()
        for h in (finding.get("hypotheses") or [])
        if isinstance(h, dict)
    }
    assert "alt_hepatic_cell_stress_pattern_v1" in hypothesis_ids
    assert "alt_inflammatory_coupling_context_v1" in hypothesis_ids


def test_root_cause_v1_tsh_hypotheses_emit_for_tsh_signal():
    root = compile_root_cause_v1(
        signal_results=[
            {
                "signal_id": "signal_thyroid_tsh_context",
                "signal_state": "suboptimal",
                "confidence": 0.69,
                "primary_metric": "tsh",
            },
            {
                "signal_id": "signal_tsh_high",
                "signal_state": "at_risk",
                "confidence": 0.73,
                "primary_metric": "tsh",
            },
        ],
        biomarker_context={
            "tsh": {"value": 6.8},
            "free_t4": {"value": 10.5},
            "free_t3": {"value": 3.2},
            "ldl_cholesterol": {"value": 4.4},
        },
        input_reference_ranges={
            "tsh": {"min": 0.4, "max": 4.5},
            "free_t4": {"min": 12.0, "max": 22.0},
            "free_t3": {"min": 3.1, "max": 6.8},
            "ldl_cholesterol": {"min": 1.0, "max": 3.0},
        },
    )
    dump = root.model_dump() if root is not None else {}
    finding = _finding_by_signal(dump, "signal_thyroid_tsh_context")
    assert isinstance(finding, dict)
    hypothesis_ids = {
        str(h.get("hypothesis_id", "")).strip()
        for h in (finding.get("hypotheses") or [])
        if isinstance(h, dict)
    }
    assert "tsh_axis_regulation_pattern_v1" in hypothesis_ids
    assert "tsh_metabolic_coupling_context_v1" in hypothesis_ids


def test_root_cause_v1_suppresses_non_repeat_confirmatory_tests_when_present():
    root = compile_root_cause_v1(
        signal_results=[
            {
                "signal_id": "signal_hepatic_alt_context",
                "signal_state": "suboptimal",
                "confidence": 0.61,
                "primary_metric": "alt",
            }
        ],
        biomarker_context={
            "alt": {"value": 65.0},
            "ast": {"value": 54.0},
            "ggt": {"value": 69.0},
        },
        input_reference_ranges={
            "alt": {"min": 10.0, "max": 45.0},
            "ast": {"min": 10.0, "max": 40.0},
            "ggt": {"min": 10.0, "max": 55.0},
        },
    )
    dump = root.model_dump() if root is not None else {}
    finding = _finding_by_signal(dump, "signal_hepatic_alt_context")
    assert isinstance(finding, dict)
    by_id = {
        str(h.get("hypothesis_id", "")).strip(): h
        for h in (finding.get("hypotheses") or [])
        if isinstance(h, dict)
    }
    alt_hypothesis = by_id.get("alt_hepatic_cell_stress_pattern_v1")
    assert isinstance(alt_hypothesis, dict)
    confirmatory_test_ids = {
        str(t.get("test_id", "")).strip()
        for t in (alt_hypothesis.get("confirmatory_tests") or [])
        if isinstance(t, dict)
    }
    assert "test_liver_ggt_alt_ast_v1" not in confirmatory_test_ids


def test_root_cause_v1_insulin_resistance_hypotheses_emit_kb_s46():
    root = compile_root_cause_v1(
        signal_results=[
            {
                "signal_id": "signal_insulin_resistance",
                "signal_state": "at_risk",
                "confidence": 0.84,
                "primary_metric": "tyg_index",
            }
        ],
        biomarker_context={
            "glucose": {"value": 6.1},
            "triglycerides": {"value": 2.4},
            "tyg_index": {"value": 8.72},
            "hdl_cholesterol": {"value": 0.95},
            "hba1c": {"value": 44.0},
        },
        input_reference_ranges={
            "glucose": {"min": 3.9, "max": 5.5},
            "triglycerides": {"min": 0.4, "max": 1.7},
            "tyg_index": {"min": 4.0, "max": 8.2},
            "hdl_cholesterol": {"min": 1.0, "max": 3.0},
            "hba1c": {"min": 20.0, "max": 42.0},
        },
    )
    dump = root.model_dump() if root is not None else {}
    finding = _finding_by_signal(dump, "signal_insulin_resistance")
    assert isinstance(finding, dict)
    hypothesis_ids = {
        str(h.get("hypothesis_id", "")).strip()
        for h in (finding.get("hypotheses") or [])
        if isinstance(h, dict)
    }
    assert "ir_tyg_metabolic_resistance_pattern_v1" in hypothesis_ids
    assert "ir_dysglycaemia_coupling_context_v1" in hypothesis_ids
    assert "ir_hepatic_metabolic_coupling_v1" in hypothesis_ids


def test_root_cause_v1_systemic_inflammation_hypotheses_emit_kb_s46():
    root = compile_root_cause_v1(
        signal_results=[
            {
                "signal_id": "signal_systemic_inflammation",
                "signal_state": "at_risk",
                "confidence": 0.83,
                "primary_metric": "crp",
            }
        ],
        biomarker_context={
            "crp": {"value": 3.8},
            "glucose": {"value": 5.9},
            "triglycerides": {"value": 2.0},
            "alt": {"value": 52.0},
            "ggt": {"value": 62.0},
        },
        input_reference_ranges={
            "crp": {"min": 0.0, "max": 3.0},
            "glucose": {"min": 3.9, "max": 5.5},
            "triglycerides": {"min": 0.4, "max": 1.7},
            "alt": {"min": 10.0, "max": 45.0},
            "ggt": {"min": 10.0, "max": 55.0},
        },
    )
    dump = root.model_dump() if root is not None else {}
    finding = _finding_by_signal(dump, "signal_systemic_inflammation")
    assert isinstance(finding, dict)
    hypothesis_ids = {
        str(h.get("hypothesis_id", "")).strip()
        for h in (finding.get("hypotheses") or [])
        if isinstance(h, dict)
    }
    assert "infl_persistent_low_grade_burden_v1" in hypothesis_ids
    assert "infl_metabolic_companion_context_v1" in hypothesis_ids
    assert "infl_hepatic_coupling_context_v1" in hypothesis_ids


def test_root_cause_v1_hba1c_only_finding_unchanged_kb_s46_regression():
    """Untouched signals must not gain extra findings when only hba1c fires."""
    root = compile_root_cause_v1(
        signal_results=[
            {
                "signal_id": "signal_hba1c_high",
                "signal_state": "at_risk",
                "confidence": 0.81,
                "primary_metric": "hba1c",
            }
        ],
        biomarker_context={
            "hba1c": {"value": 49.0},
            "glucose": {"value": 7.2},
            "triglycerides": {"value": 2.1},
            "hdl_cholesterol": {"value": 0.9},
        },
        input_reference_ranges={
            "hba1c": {"min": 20.0, "max": 42.0},
            "glucose": {"min": 3.9, "max": 5.5},
            "triglycerides": {"min": 0.4, "max": 1.7},
            "hdl_cholesterol": {"min": 1.0, "max": 3.0},
        },
    )
    dump = root.model_dump() if root is not None else {}
    assert len(dump.get("findings") or []) == 1
    assert _finding_by_signal(dump, "signal_hba1c_high") is not None
    assert _finding_by_signal(dump, "signal_insulin_resistance") is None
    assert _finding_by_signal(dump, "signal_systemic_inflammation") is None
