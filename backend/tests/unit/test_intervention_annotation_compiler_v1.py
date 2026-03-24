"""KB-S48e intervention annotation compiler and parallel report contract tests."""

from __future__ import annotations

from pathlib import Path

import yaml

from core.analytics.intervention_annotation_compiler_v1 import (
    approved_intervention_class_ids_v1,
    build_intervention_annotations_v1,
)
from core.analytics.report_compiler_v1 import compile_report_v1
from scripts.validate_user_intervention_exposure import APPROVED_INTERVENTION_CLASS_IDS as USER_EXPOSURE_CLASS_IDS

ROOT = Path(__file__).resolve().parents[3]
USER_EXPOSURE_FIXTURE = ROOT / "backend" / "tests" / "fixtures" / "user_intervention_exposure" / "valid_record_set.yaml"
ROOT_CAUSE_CONTRACT = ROOT / "backend" / "core" / "contracts" / "root_cause_v1.py"
KB31_SELECTOR = ROOT / "backend" / "core" / "analytics" / "intervention_selector_v1.py"


def test_approved_class_ids_match_user_exposure_validator() -> None:
    assert approved_intervention_class_ids_v1() == USER_EXPOSURE_CLASS_IDS


def test_build_annotations_none_without_document() -> None:
    assert build_intervention_annotations_v1(None) is None
    assert build_intervention_annotations_v1({}) is None
    assert build_intervention_annotations_v1({"schema_version": "1.0.0", "intervention_records": []}) is None


def test_fixture_mapped_and_unresolved_split() -> None:
    doc = yaml.safe_load(USER_EXPOSURE_FIXTURE.read_text(encoding="utf-8"))
    ann = build_intervention_annotations_v1(doc)
    assert ann is not None
    assert ann.version == "v1"
    assert ann.registry_id == "intervention_effects_registry_v1"
    assert {r.intervention_record_id for r in ann.resolved} == {
        "rec_metformin_001",
        "rec_lisinopril_003",
    }
    assert len(ann.unresolved) == 1
    assert ann.unresolved[0].intervention_record_id == "rec_unknown_supplement_002"
    assert "Not mapped" in ann.unresolved[0].note


def test_mapped_intervention_includes_registry_effects() -> None:
    doc = yaml.safe_load(USER_EXPOSURE_FIXTURE.read_text(encoding="utf-8"))
    ann = build_intervention_annotations_v1(doc)
    assert ann is not None
    met = next(r for r in ann.resolved if r.intervention_record_id == "rec_metformin_001")
    assert len(met.effects) >= 1
    kinds = {e.effect_type for e in met.effects}
    assert "expected_biomarker_effect" in kinds


def test_unmapped_does_not_receive_registry_effects() -> None:
    doc = {
        "schema_version": "1.0.0",
        "intervention_records": [
            {
                "intervention_record_id": "u1",
                "intervention_type": "supplement",
                "entered_label": "mystery powder",
                "canonical_class": {"link_status": "unmapped", "intervention_class_id": None},
                "timeline": {
                    "effective_from_date": "2024-01-01",
                    "effective_to_date": None,
                    "is_ongoing": True,
                    "change_event_type": "started",
                },
                "provenance": {"source_type": "user_reported", "confidence": "unknown"},
            }
        ],
    }
    ann = build_intervention_annotations_v1(doc)
    assert ann is not None
    assert ann.resolved == []
    assert len(ann.unresolved) == 1


def test_invalid_unmapped_with_class_id_skipped_no_rich_effects() -> None:
    """Dishonest unmapped row (non-null class id) produces no resolved annotation."""
    doc = {
        "schema_version": "1.0.0",
        "intervention_records": [
            {
                "intervention_record_id": "bad",
                "intervention_type": "medication",
                "entered_label": "x",
                "canonical_class": {"link_status": "unmapped", "intervention_class_id": "raas_inhibitor"},
                "timeline": {
                    "effective_from_date": "2024-01-01",
                    "effective_to_date": None,
                    "is_ongoing": True,
                    "change_event_type": "started",
                },
                "provenance": {"source_type": "user_reported", "confidence": "estimated"},
            }
        ],
    }
    assert build_intervention_annotations_v1(doc) is None


def test_report_root_cause_unchanged_when_user_interventions_passed() -> None:
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
            "intervention_id": "intv_test",
            "title": "t",
            "body": "b",
            "why_this_matters": "w",
            "signal_refs": [],
            "chain_refs": [],
            "evidence_strength": "moderate",
            "evidence_summary": "e",
            "safety_class": "monitoring",
            "escalation_required": False,
        }
    ]
    user_doc = yaml.safe_load(USER_EXPOSURE_FIXTURE.read_text(encoding="utf-8"))
    base_kw = dict(
        signal_results=signal_results,
        interaction_summary=interaction_summary,
        interventions_v1=interventions,
        signal_registry_version="vX",
        signal_registry_hash_sha256="a" * 64,
        biomarker_context={"hba1c": {"value": 48.0}},
        input_reference_ranges={"hba1c": {"min": 20.0, "max": 42.0}},
        generated_at="2026-01-01T00:00:00Z",
    )
    r1 = compile_report_v1(**base_kw)
    r2 = compile_report_v1(**base_kw, user_intervention_document=user_doc)
    assert r1.root_cause_v1 is not None and r2.root_cause_v1 is not None
    assert r1.root_cause_v1.model_dump() == r2.root_cause_v1.model_dump()
    assert r1.intervention_annotations_v1 is None
    assert r2.intervention_annotations_v1 is not None


def test_kb31_selector_and_root_cause_contract_files_exist_unchanged_scope() -> None:
    """Guard rails: KB-S48e does not remove KB-S31 selector or root-cause contract module."""
    assert ROOT_CAUSE_CONTRACT.is_file()
    assert KB31_SELECTOR.is_file()
