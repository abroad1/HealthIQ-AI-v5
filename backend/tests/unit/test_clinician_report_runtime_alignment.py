import json
from pathlib import Path

from core.analytics.report_compiler_v1 import (
    TOP_FINDINGS_RANKING_POLICY_VERSION,
    compile_clinician_report_v1,
)
from core.contracts.clinician_report_v1 import ClinicianReportV1
from core.dto.builders import build_analysis_result_dto
from tools.run_golden_panel import run_golden_panel

from tests.support.panel_acceptance import ab_acceptance_fixture_path, vr_acceptance_fixture_path


ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = ROOT.parent
AB_PANEL = ab_acceptance_fixture_path()
VR_PANEL = vr_acceptance_fixture_path()
AB_EXPECTED_FIXTURE = ROOT / "tests" / "fixtures" / "reports" / "clinician_report_v1_ab.json"
VR_EXPECTED_FIXTURE = ROOT / "tests" / "fixtures" / "reports" / "clinician_report_v1_vr.json"


def _compile_from_analysis_result(analysis_result: dict) -> dict:
    meta = analysis_result.get("meta", {}) if isinstance(analysis_result, dict) else {}
    insight_graph = meta.get("insight_graph", {}) if isinstance(meta, dict) else {}
    report_v1 = insight_graph.get("report_v1", {}) if isinstance(insight_graph, dict) else {}
    biomarkers = analysis_result.get("biomarkers", []) if isinstance(analysis_result, dict) else []
    mh = meta.get("medical_history_snapshot")
    mh = mh if isinstance(mh, dict) else None
    compiled = compile_clinician_report_v1(
        report_v1_payload=report_v1 if isinstance(report_v1, dict) else {},
        biomarker_rows=biomarkers if isinstance(biomarkers, list) else [],
        medical_history=mh,
    )
    assert compiled is not None
    return compiled.model_dump()


def test_clinician_report_runtime_producer_returns_valid_contract_for_ab(tmp_path):
    _, analysis_result = run_golden_panel(
        fixture_path=AB_PANEL,
        output_root=tmp_path,
        run_id="kb-s44a-ab-producer-contract",
        write_narrative=False,
    )
    compiled = _compile_from_analysis_result(analysis_result)
    contract = ClinicianReportV1(**compiled)
    assert contract.header.report_version == "v1"
    assert contract.sections.page1.primary_concern
    assert isinstance(contract.suppressed_confirmatory_tests, list)
    assert contract.sections.page1.ranking_policy_version == TOP_FINDINGS_RANKING_POLICY_VERSION
    assert contract.sections.page1.primary_concern_mode == "technical_tiebreak_lead"
    # BE-W2-RQ2 — runner-up from ranked top_findings[1] even when co_primary_signal_ids is empty (UAT-027).
    assert contract.sections.page1.co_primary_signal_ids == []
    assert contract.sections.page1.runner_up_topic_line
    assert contract.sections.page1.runner_up_why_not_lead_line
    assert "signal_" not in contract.sections.page1.runner_up_topic_line
    # Consumer hero copy leads with plain-language "why", not policy/tie-break boilerplate.
    assert contract.sections.page1.key_findings[0]
    assert "Homocysteine" in contract.sections.page1.key_findings[0]
    assert "technical tie-break" not in contract.sections.page1.key_findings[0].lower()


def test_clinician_report_ab_output_is_deterministic(tmp_path):
    _, result_a = run_golden_panel(
        fixture_path=AB_PANEL,
        output_root=tmp_path,
        run_id="kb-s44a-ab-determinism-a",
        write_narrative=False,
    )
    _, result_b = run_golden_panel(
        fixture_path=AB_PANEL,
        output_root=tmp_path,
        run_id="kb-s44a-ab-determinism-b",
        write_narrative=False,
    )
    dump_a = _compile_from_analysis_result(result_a)
    dump_b = _compile_from_analysis_result(result_b)
    assert dump_a == dump_b

    # AB fixture remains a governed anchor for contract shape and mandatory messaging.
    fixture = json.loads(AB_EXPECTED_FIXTURE.read_text(encoding="utf-8"))
    assert dump_a["header"]["report_version"] == fixture["header"]["report_version"]
    assert dump_a["header"]["footer_line"] == fixture["header"]["footer_line"]
    assert dump_a["header"]["disclaimer_top"] == fixture["header"]["disclaimer_top"]


def test_clinician_report_vr_output_is_deterministic_and_matches_vr_fixture(tmp_path):
    _, result_a = run_golden_panel(
        fixture_path=VR_PANEL,
        output_root=tmp_path,
        run_id="kb-s44a-vr-determinism-a",
        write_narrative=False,
    )
    _, result_b = run_golden_panel(
        fixture_path=VR_PANEL,
        output_root=tmp_path,
        run_id="kb-s44a-vr-determinism-b",
        write_narrative=False,
    )
    dump_a = _compile_from_analysis_result(result_a)
    dump_b = _compile_from_analysis_result(result_b)
    assert dump_a == dump_b

    vr_expected = json.loads(VR_EXPECTED_FIXTURE.read_text(encoding="utf-8"))
    assert dump_a == vr_expected


def test_clinician_page1_near_tie_ambiguity_synthetic():
    """When meta has no signal-id fallback but top signals tie on state and confidence, mode is near_tie."""
    report = {
        "meta": {
            "ranking_signal_id_fallback_invoked": False,
            "ranking_policy_version": TOP_FINDINGS_RANKING_POLICY_VERSION,
        },
        "top_findings": [
            {
                "signal_id": "sig_z",
                "signal_state": "suboptimal",
                "confidence": 0.7,
                "primary_metric": "m1",
                "why_it_matters": "z matters.",
                "confidence_reasons": ["R"],
                "supporting_markers": ["a"],
            },
            {
                "signal_id": "sig_a",
                "signal_state": "suboptimal",
                "confidence": 0.7,
                "primary_metric": "m2",
                "why_it_matters": "a matters.",
                "confidence_reasons": ["R"],
                "supporting_markers": ["b"],
            },
        ],
        "top_chains": [],
        "root_cause_v1": {"findings": []},
    }
    out = compile_clinician_report_v1(report_v1_payload=report, biomarker_rows=[])
    assert out is not None
    p1 = out.sections.page1
    assert p1.primary_concern_mode == "near_tie_ambiguity"
    assert p1.co_primary_signal_ids == ["sig_a", "sig_z"]
    assert any("Several findings have similar strength" in k for k in p1.key_findings)
    assert p1.runner_up_signal_id == "sig_a"
    assert p1.runner_up_topic_line
    assert "sig_" not in p1.runner_up_topic_line
    assert p1.runner_up_why_not_lead_line


def test_api_dto_exposes_clinician_report_v1(tmp_path):
    _, analysis_result = run_golden_panel(
        fixture_path=AB_PANEL,
        output_root=tmp_path,
        run_id="kb-s44a-api-exposure",
        write_narrative=False,
    )
    dto = build_analysis_result_dto(analysis_result)
    assert "clinician_report_v1" in dto
    assert isinstance(dto["clinician_report_v1"], dict)

    expected = _compile_from_analysis_result(analysis_result)
    assert dto["clinician_report_v1"] == expected

