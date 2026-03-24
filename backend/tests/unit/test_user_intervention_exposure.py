"""Tests for user intervention / exposure record-set validation (KB-S48d)."""

from __future__ import annotations

from pathlib import Path

import yaml

from scripts.validate_intervention_effects_registry import APPROVED_CLASS_IDS as REGISTRY_APPROVED_CLASS_IDS
from scripts.validate_user_intervention_exposure import (
    APPROVED_INTERVENTION_CLASS_IDS,
    SCHEMA_VERSION,
    main,
    validate_user_intervention_exposure_document,
)

ROOT = Path(__file__).resolve().parents[3]
FIXTURE_VALID = ROOT / "backend" / "tests" / "fixtures" / "user_intervention_exposure" / "valid_record_set.yaml"
SCHEMA_PATH = ROOT / "knowledge_bus" / "schema" / "user_intervention_exposure_schema_v1.yaml"
REGISTRY_SCHEMA_PATH = ROOT / "knowledge_bus" / "schema" / "intervention_effects_registry_schema_v1.yaml"


def _base_doc() -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "intervention_records": [
            {
                "intervention_record_id": "r1",
                "intervention_type": "medication",
                "entered_label": "Example drug label text",
                "canonical_class": {"link_status": "mapped", "intervention_class_id": "raas_inhibitor"},
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


def test_fixture_valid_passes(tmp_path: Path) -> None:
    audit = tmp_path / "audit.md"
    code = main(["--document", str(FIXTURE_VALID), "--audit-path", str(audit)])
    assert code == 0
    assert audit.read_text(encoding="utf-8").startswith("# User Intervention / Exposure Audit")


def test_missing_timeline_field_fails() -> None:
    doc = _base_doc()
    del doc["intervention_records"][0]["timeline"]["change_event_type"]
    errors: list[str] = []
    validate_user_intervention_exposure_document(doc, errors)
    assert errors
    assert any("change_event_type" in e for e in errors)


def test_missing_provenance_source_fails() -> None:
    doc = _base_doc()
    del doc["intervention_records"][0]["provenance"]["source_type"]
    errors: list[str] = []
    validate_user_intervention_exposure_document(doc, errors)
    assert errors
    assert any("source_type" in e for e in errors)


def test_invalid_source_type_enum_fails() -> None:
    doc = _base_doc()
    doc["intervention_records"][0]["provenance"]["source_type"] = "hospital_emr_direct_feed"
    errors: list[str] = []
    validate_user_intervention_exposure_document(doc, errors)
    assert errors


def test_invalid_confidence_enum_fails() -> None:
    doc = _base_doc()
    doc["intervention_records"][0]["provenance"]["confidence"] = "very_sure"
    errors: list[str] = []
    validate_user_intervention_exposure_document(doc, errors)
    assert errors


def test_invalid_confidence_legacy_moderate_rejected() -> None:
    doc = _base_doc()
    doc["intervention_records"][0]["provenance"]["confidence"] = "moderate"
    errors: list[str] = []
    validate_user_intervention_exposure_document(doc, errors)
    assert errors
    assert any("confidence" in e for e in errors)


def test_invalid_intervention_type_fails() -> None:
    doc = _base_doc()
    doc["intervention_records"][0]["intervention_type"] = "prescription_only"
    errors: list[str] = []
    validate_user_intervention_exposure_document(doc, errors)
    assert errors


def test_invalid_intervention_type_legacy_non_medication_rejected() -> None:
    doc = _base_doc()
    doc["intervention_records"][0]["intervention_type"] = "non_medication"
    errors: list[str] = []
    validate_user_intervention_exposure_document(doc, errors)
    assert errors
    assert any("intervention_type" in e for e in errors)


def test_mapped_invalid_class_id_fails() -> None:
    doc = _base_doc()
    doc["intervention_records"][0]["canonical_class"]["intervention_class_id"] = "not_a_v1_class"
    errors: list[str] = []
    validate_user_intervention_exposure_document(doc, errors)
    assert errors


def test_unmapped_must_use_null_class_id() -> None:
    doc = _base_doc()
    doc["intervention_records"][0]["canonical_class"] = {
        "link_status": "unmapped",
        "intervention_class_id": "raas_inhibitor",
    }
    errors: list[str] = []
    validate_user_intervention_exposure_document(doc, errors)
    assert errors
    assert any("unmapped" in e.lower() for e in errors)


def test_unmapped_with_explicit_null_passes() -> None:
    doc = _base_doc()
    doc["intervention_records"][0]["canonical_class"] = {
        "link_status": "unmapped",
        "intervention_class_id": None,
    }
    errors: list[str] = []
    validate_user_intervention_exposure_document(doc, errors)
    assert not errors


def test_ongoing_requires_null_effective_to() -> None:
    doc = _base_doc()
    doc["intervention_records"][0]["timeline"]["is_ongoing"] = True
    doc["intervention_records"][0]["timeline"]["effective_to_date"] = "2024-06-01"
    errors: list[str] = []
    validate_user_intervention_exposure_document(doc, errors)
    assert errors


def test_duplicate_record_id_fails() -> None:
    doc = _base_doc()
    doc["intervention_records"].append(
        {
            **doc["intervention_records"][0],
            "intervention_record_id": "r1",
            "entered_label": "other label",
        }
    )
    errors: list[str] = []
    validate_user_intervention_exposure_document(doc, errors)
    assert any("duplicate" in e for e in errors)


def test_schema_forbidden_fragments_match_registry_schema() -> None:
    user_doc = yaml.safe_load(SCHEMA_PATH.read_text(encoding="utf-8"))
    reg_doc = yaml.safe_load(REGISTRY_SCHEMA_PATH.read_text(encoding="utf-8"))
    assert frozenset(user_doc["forbidden_key_fragments"]) == frozenset(
        reg_doc["forbidden_key_fragments"]
    )


def test_approved_intervention_class_ids_match_registry_validator() -> None:
    """Drift guard: mapped-class allowlist stays aligned with KB-S48a registry validator."""
    assert APPROVED_INTERVENTION_CLASS_IDS == REGISTRY_APPROVED_CLASS_IDS
    assert len(APPROVED_INTERVENTION_CLASS_IDS) == 8
