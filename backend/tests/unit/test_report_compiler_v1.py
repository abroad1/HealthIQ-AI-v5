import hashlib
import json
from pathlib import Path

import yaml

from core.analytics.report_compiler_v1 import (
    TOP_FINDINGS_RANKING_POLICY_VERSION,
    _normalise_hypothesis_safety_class,
    compile_clinician_report_v1,
    compile_report_v1,
)
from core.dto.builders import build_analysis_result_dto


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _report_v1_with_informational_root_cause_fallback() -> dict:
    """Minimal report_v1 payload mirroring root_cause_compiler_v1 WHY fallback."""
    return {
        "meta": {
            "ranking_signal_id_fallback_invoked": False,
            "ranking_policy_version": TOP_FINDINGS_RANKING_POLICY_VERSION,
        },
        "top_findings": [
            {
                "signal_id": "signal_homocysteine",
                "signal_state": "suboptimal",
                "confidence": 0.7,
                "primary_metric": "homocysteine",
                "why_it_matters": "Elevated homocysteine may reflect methylation stress.",
                "confidence_reasons": ["PRIMARY_METRIC_PRESENT"],
                "supporting_markers": [],
            }
        ],
        "top_chains": [],
        "root_cause_v1": {
            "findings": [
                {
                    "signal_id": "signal_homocysteine",
                    "signal_state": "suboptimal",
                    "signal_confidence": 0.7,
                    "primary_metric": "homocysteine",
                    "hypotheses": [
                        {
                            "hypothesis_id": "why_engine_fallback_v1",
                            "title": "Pattern noted — deeper causal explanation not yet available",
                            "summary": (
                                "We identified a pattern on this panel, but governed causal hypotheses "
                                "are not yet available for this lead."
                            ),
                            "hypothesis_confidence": 0.0,
                            "evidence_for": [],
                            "evidence_against": [],
                            "missing_data": [],
                            "confirmatory_tests": [],
                            "safety_class": "informational",
                        }
                    ],
                }
            ],
        },
    }


def test_normalise_hypothesis_safety_class_legacy_and_unknown_tokens():
    assert _normalise_hypothesis_safety_class("informational") == "monitoring"
    assert _normalise_hypothesis_safety_class("") == "monitoring"
    assert _normalise_hypothesis_safety_class("  ") == "monitoring"
    assert _normalise_hypothesis_safety_class("legacy_unknown") == "monitoring"
    assert _normalise_hypothesis_safety_class("clinician_referral") == "clinician_referral"


def test_compile_clinician_report_v1_maps_informational_safety_class_to_monitoring():
    """LC-S8D: legacy informational safety_class must not break HypothesisV1 validation."""
    report = _report_v1_with_informational_root_cause_fallback()
    compiled = compile_clinician_report_v1(report_v1_payload=report, biomarker_rows=[])
    assert compiled is not None
    assert compiled.sections.root_cause is not None
    assert len(compiled.sections.root_cause.hypotheses) == 1
    assert compiled.sections.root_cause.hypotheses[0].safety_class == "monitoring"


def test_build_analysis_result_dto_accepts_informational_root_cause_fallback():
    """GET /api/analysis/result path: build_analysis_result_dto must not 500 on informational."""
    raw = {
        "analysis_id": "lc-s8d-informational-fallback-test",
        "biomarkers": [],
        "clusters": [],
        "insights": [],
        "status": "completed",
        "meta": {
            "insight_graph": {
                "report_v1": _report_v1_with_informational_root_cause_fallback(),
            }
        },
    }
    dto = build_analysis_result_dto(raw)
    assert dto["clinician_report_v1"] is not None
    hypotheses = dto["clinician_report_v1"]["sections"]["root_cause"]["hypotheses"]
    assert hypotheses[0]["safety_class"] == "monitoring"


def test_report_v1_ordering_and_schema_fields():
    signal_results = [
        {
            "signal_id": "signal_b",
            "system": "hepatic",
            "signal_state": "suboptimal",
            "confidence": 0.90,
            "confidence_reasons": ["PRIMARY_METRIC_PRESENT"],
            "primary_metric": "alt",
            "supporting_markers": ["ggt"],
        },
        {
            "signal_id": "signal_a",
            "system": "vascular",
            "signal_state": "at_risk",
            "confidence": 0.50,
            "confidence_reasons": ["PRIMARY_METRIC_PRESENT"],
            "primary_metric": "homocysteine",
            "supporting_markers": ["crp"],
        },
    ]
    interaction_summary = [
        {"chain_id": "chain_020", "confidence": 0.7, "signals_involved": ["signal_b", "signal_a"]},
        {"chain_id": "chain_010", "confidence": 0.7, "signals_involved": ["signal_a"]},
    ]
    interventions = [
        {
            "intervention_id": "intv_vascular_clinician_referral_v1",
            "title": "Clinician review advised for vascular signal pattern",
            "body": "Arrange clinician follow-up.",
            "why_this_matters": "Escalated vascular signals need clinical review.",
            "signal_refs": ["signal_a"],
            "chain_refs": ["chain_020"],
            "evidence_strength": "consensus",
            "evidence_summary": "- Guideline panel, n=consensus, Journal, 2023.\n- Cohort, n=1200, Journal, 2021.",
            "safety_class": "clinician_referral",
            "escalation_required": True,
        }
    ]
    sha = "b" * 64
    report = compile_report_v1(
        signal_results=signal_results,
        interaction_summary=interaction_summary,
        interventions_v1=interventions,
        signal_registry_version="vX",
        signal_registry_hash_sha256=sha,
        interaction_map_revision="1.1.0",
        safety_contract_version="1.0.1",
        generated_at="2026-03-15T00:00:00+00:00",
    )
    dumped = report.model_dump()
    assert dumped["report_version"] == "v1"
    assert dumped["top_findings"][0]["signal_id"] == "signal_a"  # at_risk outranks suboptimal
    assert dumped["top_chains"][0]["chain_id"] == "chain_020"  # same confidence, longer chain first
    assert len(dumped["actions"]["interventions"]) == 1
    assert dumped["actions"]["interventions"][0]["intervention_id"] == interventions[0]["intervention_id"]
    assert dumped["actions"]["interventions"][0]["safety_class"] == "clinician_referral"
    assert len(dumped["actions"]["clinician_referrals"]) == 1
    assert dumped["actions"]["clinician_referrals"][0]["intervention_id"] == interventions[0]["intervention_id"]
    assert dumped["actions"]["monitoring"] == []
    assert dumped["meta"]["signal_registry_hash_sha256"] == sha
    assert dumped["meta"]["interaction_map_revision"] == "1.1.0"
    assert dumped["meta"]["safety_contract_version"] == "1.0.1"
    assert dumped["meta"]["ranking_policy_version"] == TOP_FINDINGS_RANKING_POLICY_VERSION
    assert dumped["meta"]["ranking_signal_id_fallback_invoked"] is False


def test_report_v1_additive_inputs_unchanged():
    signal_results = [
        {
            "signal_id": "signal_hba1c_high",
            "system": "metabolic",
            "signal_state": "suboptimal",
            "confidence": 0.66,
            "confidence_reasons": ["PRIMARY_METRIC_PRESENT"],
            "primary_metric": "hba1c",
            "supporting_markers": [],
        }
    ]
    interaction_summary = [
        {
            "chain_id": "chain_001",
            "priority_rank": 1,
            "signals_involved": ["signal_hba1c_high"],
            "chain_summary_text": "signal_hba1c_high",
            "confidence": 0.66,
        }
    ]
    interventions = [
        {
            "intervention_id": "intv_metabolic_repeat_monitoring_v1",
            "title": "Repeat metabolic monitoring",
            "body": "Repeat testing in 8–12 weeks.",
            "why_this_matters": "Trend confirmation supports safe monitoring decisions.",
            "signal_refs": ["signal_hba1c_high"],
            "chain_refs": ["chain_001"],
            "evidence_strength": "moderate",
            "evidence_summary": "- Cohort, n=1000, Journal, 2021.\n- Registry, n=400, Journal, 2020.",
            "safety_class": "monitoring",
            "escalation_required": False,
        }
    ]
    baseline_signal = json.loads(json.dumps(signal_results))
    baseline_chain = json.loads(json.dumps(interaction_summary))
    baseline_actions = json.loads(json.dumps(interventions))
    _ = compile_report_v1(
        signal_results=signal_results,
        interaction_summary=interaction_summary,
        interventions_v1=interventions,
        signal_registry_version="v",
        signal_registry_hash_sha256="c" * 64,
        interaction_map_revision="1.1.0",
        safety_contract_version="1.0.1",
        generated_at="2026-03-15T00:00:00+00:00",
    )
    assert signal_results == baseline_signal
    assert interaction_summary == baseline_chain
    assert interventions == baseline_actions


def test_report_v1_text_fields_respect_denylist():
    rules_path = _repo_root() / "knowledge_bus" / "interventions" / "safety_rules_v1.yaml"
    rules = yaml.safe_load(rules_path.read_text(encoding="utf-8")) or {}
    denylist = [str(x).lower() for x in rules.get("denylist_phrases", [])]
    report = compile_report_v1(
        signal_results=[
            {
                "signal_id": "signal_x",
                "system": "metabolic",
                "signal_state": "suboptimal",
                "confidence": 0.8,
                "confidence_reasons": ["PRIMARY_METRIC_PRESENT"],
                "primary_metric": "glucose",
                "supporting_markers": [],
            }
        ],
        interaction_summary=[{"chain_id": "chain_001", "confidence": 0.8, "signals_involved": ["signal_x"]}],
        interventions_v1=[
            {
                "intervention_id": "intv_metabolic_repeat_monitoring_v1",
                "title": "Repeat metabolic monitoring",
                "body": "Repeat testing in 8–12 weeks.",
                "why_this_matters": "Trend confirmation supports safe monitoring decisions.",
                "signal_refs": ["signal_x"],
                "chain_refs": ["chain_001"],
                "evidence_strength": "moderate",
                "evidence_summary": "- Cohort, n=1000, Journal, 2021.\n- Registry, n=400, Journal, 2020.",
                "safety_class": "monitoring",
                "escalation_required": False,
            }
        ],
        signal_registry_version="v",
        signal_registry_hash_sha256="d" * 64,
        interaction_map_revision="1.1.0",
        safety_contract_version="1.0.1",
        generated_at="2026-03-15T00:00:00+00:00",
    )
    dump = report.model_dump()
    text_fields = []
    for f in dump["top_findings"]:
        text_fields.append(f["why_it_matters"])
    for c in dump["top_chains"]:
        text_fields.append(c["summary_text"])
    for i in dump["actions"]["interventions"]:
        text_fields.extend([i["title"], i["body"], i["why_this_matters"], i["evidence_summary"]])
    lowered = "\n".join(text_fields).lower()
    for phrase in denylist:
        assert phrase not in lowered


def test_report_v1_top_findings_prefers_supporting_markers_over_signal_id():
    """Same state/confidence/reasons; richer marker support ranks above lexicographic signal_id."""
    signal_results = [
        {
            "signal_id": "signal_zzz",
            "system": "metabolic",
            "signal_state": "suboptimal",
            "confidence": 0.70,
            "confidence_reasons": ["PRIMARY_METRIC_PRESENT"],
            "primary_metric": "m1",
            "supporting_markers": ["a"],
        },
        {
            "signal_id": "signal_aaa",
            "system": "metabolic",
            "signal_state": "suboptimal",
            "confidence": 0.70,
            "confidence_reasons": ["PRIMARY_METRIC_PRESENT"],
            "primary_metric": "m1",
            "supporting_markers": ["a", "b", "c"],
        },
    ]
    report = compile_report_v1(
        signal_results=signal_results,
        interaction_summary=[],
        interventions_v1=[],
        signal_registry_version="v",
        signal_registry_hash_sha256="e" * 64,
        interaction_map_revision="1.1.0",
        safety_contract_version="1.0.1",
        generated_at="2026-03-15T00:00:00+00:00",
    )
    dumped = report.model_dump()["top_findings"]
    assert len(dumped) == 2
    assert dumped[0]["signal_id"] == "signal_aaa"
    assert dumped[1]["signal_id"] == "signal_zzz"
    assert report.meta.ranking_signal_id_fallback_invoked is False


def test_report_v1_top_findings_signal_id_last_resort_only():
    """Fully tied evidential key: lexicographic signal_id breaks the tie; flag is set."""
    signal_results = [
        {
            "signal_id": "signal_b",
            "system": "metabolic",
            "signal_state": "suboptimal",
            "confidence": 0.70,
            "confidence_reasons": ["PRIMARY_METRIC_PRESENT"],
            "primary_metric": "m1",
            "supporting_markers": ["x"],
        },
        {
            "signal_id": "signal_a",
            "system": "metabolic",
            "signal_state": "suboptimal",
            "confidence": 0.70,
            "confidence_reasons": ["PRIMARY_METRIC_PRESENT"],
            "primary_metric": "m1",
            "supporting_markers": ["x"],
        },
    ]
    report = compile_report_v1(
        signal_results=signal_results,
        interaction_summary=[],
        interventions_v1=[],
        signal_registry_version="v",
        signal_registry_hash_sha256="f" * 64,
        interaction_map_revision="1.1.0",
        safety_contract_version="1.0.1",
        generated_at="2026-03-15T00:00:00+00:00",
    )
    dumped = report.model_dump()["top_findings"]
    assert dumped[0]["signal_id"] == "signal_a"
    assert dumped[1]["signal_id"] == "signal_b"
    assert report.meta.ranking_signal_id_fallback_invoked is True


def test_report_v1_top_findings_ordering_deterministic_across_runs():
    rows = [
        {
            "signal_id": "sig_y",
            "system": "s",
            "signal_state": "at_risk",
            "confidence": 0.55,
            "confidence_reasons": ["B", "A"],
            "primary_metric": "p",
            "supporting_markers": [],
        },
        {
            "signal_id": "sig_x",
            "system": "s",
            "signal_state": "at_risk",
            "confidence": 0.55,
            "confidence_reasons": ["A", "B"],
            "primary_metric": "p",
            "supporting_markers": [],
        },
    ]
    kw = dict(
        signal_results=list(rows),
        interaction_summary=[],
        interventions_v1=[],
        signal_registry_version="v",
        signal_registry_hash_sha256="a" * 64,
        interaction_map_revision="1.1.0",
        safety_contract_version="1.0.1",
        generated_at="2026-03-15T00:00:00+00:00",
    )
    a = compile_report_v1(**kw)
    b = compile_report_v1(**kw)
    assert a.model_dump()["top_findings"] == b.model_dump()["top_findings"]


def test_report_v1_meta_hash_sha256_semantics():
    artifact = [
        {"signal_id": "signal_a", "system": "metabolic"},
        {"signal_id": "signal_b", "system": "vascular"},
    ]
    expected_sha = hashlib.sha256(
        json.dumps(artifact, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    report = compile_report_v1(
        signal_results=[],
        interaction_summary=[],
        interventions_v1=[],
        signal_registry_version="v",
        signal_registry_hash_sha256=expected_sha,
        interaction_map_revision="1.1.0",
        safety_contract_version="1.0.1",
        generated_at="2026-03-15T00:00:00+00:00",
    )
    assert len(report.meta.signal_registry_hash_sha256) == 64
    int(report.meta.signal_registry_hash_sha256, 16)  # valid hex
    assert report.meta.signal_registry_hash_sha256 == expected_sha
    assert report.meta.ranking_policy_version == TOP_FINDINGS_RANKING_POLICY_VERSION
    assert report.meta.ranking_signal_id_fallback_invoked is False
