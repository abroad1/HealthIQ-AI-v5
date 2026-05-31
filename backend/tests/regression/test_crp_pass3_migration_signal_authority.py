"""
CRP-PASS3-MIGRATION — CRP legacy s24 package and signal naming alignment regression.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from core.analytics.domain_score_assembler import assemble_consumer_domain_scores_v1
from core.contracts.confidence_model_v1 import ConfidenceModelV1
from core.contracts.insight_graph_v1 import InsightGraphV1
from core.knowledge.crp_signal_authority_v1 import (
    CHRONIC_INFLAMMATION_RUNTIME_PACKAGE,
    CRP_RUNTIME_PACKAGE_SIGNAL_CRP_HIGH,
    CRP_SIGNAL_IDS,
    ROOT_CAUSE_INFLAMMATION_SIGNAL_ID,
    WAVE1_VASCULAR_STRAIN_SUBSYSTEM_ID,
    authority_by_signal_id,
    load_crp_runtime_authority,
)
from core.knowledge.health_system_card_evidence import get_card_evidence_artefact
from core.knowledge.root_cause_registry_v1 import ROOT_CAUSE_TARGET_SPECS

_REPO = Path(__file__).resolve().parents[3]
_PACKAGES = _REPO / "knowledge_bus" / "packages"


def _packages_defining_signal(signal_id: str) -> list[str]:
    holders: list[str] = []
    for lib_path in sorted(_PACKAGES.glob("*/signal_library.yaml")):
        doc = yaml.safe_load(lib_path.read_text(encoding="utf-8")) or {}
        for entry in doc.get("signals") or []:
            if isinstance(entry, dict) and str(entry.get("signal_id", "")).strip() == signal_id:
                holders.append(lib_path.parent.name)
    return holders


@pytest.mark.regression
def test_crp_authority_registry_covers_all_crp_signals() -> None:
    doc = load_crp_runtime_authority()
    assert doc["sprint_outcome"] == "classification_and_guardrail_complete"
    assert doc["sprint_type"] == "classification_and_guardrail"
    assert set(authority_by_signal_id().keys()) == set(CRP_SIGNAL_IDS)


@pytest.mark.regression
def test_signal_crp_high_runtime_package_is_s24_only() -> None:
    row = authority_by_signal_id()["signal_crp_high"]
    assert row.runtime_package_id == CRP_RUNTIME_PACKAGE_SIGNAL_CRP_HIGH
    assert _packages_defining_signal("signal_crp_high") == [CRP_RUNTIME_PACKAGE_SIGNAL_CRP_HIGH]


@pytest.mark.regression
def test_signal_systemic_inflammation_distinct_from_crp_high() -> None:
    crp = authority_by_signal_id()["signal_crp_high"]
    systemic = authority_by_signal_id()["signal_systemic_inflammation"]
    assert crp.activation_logic == "lab_range_exceeded"
    assert systemic.activation_logic == "deterministic_threshold"
    assert systemic.root_cause_target is True
    assert crp.root_cause_target is False
    assert crp.pass3_derived is False
    assert systemic.pass3_derived is False
    assert CHRONIC_INFLAMMATION_RUNTIME_PACKAGE in systemic.runtime_package_ids


@pytest.mark.regression
def test_pkg_chronic_inflammation_documented_for_kb_rereview() -> None:
    doc = load_crp_runtime_authority()
    chronic = (doc.get("runtime_packages") or {}).get(CHRONIC_INFLAMMATION_RUNTIME_PACKAGE)
    assert isinstance(chronic, dict)
    assert chronic.get("runtime_loaded") is True
    assert chronic.get("pass3_derived") is False
    assert chronic.get("internal_kb_rereview_required") is True
    assert chronic.get("drives_signal_id") == ROOT_CAUSE_INFLAMMATION_SIGNAL_ID


@pytest.mark.regression
def test_root_cause_registry_uses_systemic_not_crp_high() -> None:
    ids = {spec.signal_id for spec in ROOT_CAUSE_TARGET_SPECS}
    assert ROOT_CAUSE_INFLAMMATION_SIGNAL_ID in ids
    assert "signal_crp_high" not in ids


@pytest.mark.regression
def test_vascular_strain_subsystem_remains_hidden() -> None:
    artefact = get_card_evidence_artefact(WAVE1_VASCULAR_STRAIN_SUBSYSTEM_ID)
    assert artefact.visibility_tier == "hidden_v1"


@pytest.mark.regression
def test_cv_card_stays_lipid_led_when_crp_signal_fires() -> None:
    scoring = {
        "health_system_scores": {
            "cardiovascular": {
                "overall_score": 70.0,
                "missing_biomarkers": [],
                "biomarker_scores": [{"biomarker_name": "total_cholesterol"}],
            },
            "metabolic": {"overall_score": 68.0, "missing_biomarkers": [], "biomarker_scores": []},
            "liver": {"overall_score": 75.0, "missing_biomarkers": [], "biomarker_scores": []},
        }
    }
    ig = InsightGraphV1(
        analysis_id="crp-pass3",
        signal_results=[
            {
                "signal_id": "signal_crp_high",
                "signal_state": "at_risk",
                "system": "inflammatory",
                "primary_metric": "crp",
            },
        ],
        system_capacity_scores={"hepatic": 70, "cardiovascular": 80, "metabolic": 70},
        confidence=ConfidenceModelV1(
            cluster_confidence={"cardiovascular": 0.9, "metabolic": 0.7, "hepatic": 0.7}
        ),
    )
    panel = {
        "total_cholesterol",
        "ldl_cholesterol",
        "hdl_cholesterol",
        "triglycerides",
        "crp",
    }
    rows, _ = assemble_consumer_domain_scores_v1(
        scoring_result=scoring,
        insight_graph=ig,
        idl_bundle=None,
        derived_ratios_meta=None,
        panel_biomarker_ids=panel,
    )
    cv = next(r for r in rows if r.domain_id == "wave1_cardiovascular")
    visible = {s.subsystem_id for s in cv.subsystems or []}
    assert WAVE1_VASCULAR_STRAIN_SUBSYSTEM_ID not in visible
    assert visible == {"wave1_cv_lipid_transport"}
    assert "homocysteine" not in (cv.contributor_sentence or "").lower()
    assert "inflammation" not in (cv.contributor_sentence or "").lower()
