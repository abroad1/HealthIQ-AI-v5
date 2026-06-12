"""Governance tests for runtime_context_semantics_model_v1.yaml."""

from __future__ import annotations

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
SEMANTICS_PATH = REPO_ROOT / "knowledge_bus/governance/runtime_context_semantics_model_v1.yaml"
REQUIREMENTS_PATH = REPO_ROOT / "knowledge_bus/governance/runtime_context_requirements_model_v1.yaml"


def _load(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def test_semantics_model_exists_and_is_clearance_authority():
    model = _load(SEMANTICS_PATH)
    assert model["runtime_consumed"] is False
    assert model["authority_role"] == "clearance_and_classification_only"
    assert "hard_prerequisite_gate" in model["semantic_classes"]
    assert "disclosed_context_requirement" in model["semantic_classes"]
    assert "interpretation_modifier" in model["semantic_classes"]
    assert "companion_biomarker_requirement" in model["semantic_classes"]


def test_semantics_model_does_not_duplicate_runtime_execution_authority():
    semantics = _load(SEMANTICS_PATH)
    requirements = _load(REQUIREMENTS_PATH)
    assert semantics["execution_companion"] == str(
        REQUIREMENTS_PATH.relative_to(REPO_ROOT)
    ).replace("\\", "/")
    assert requirements["runtime_consumed"] is True
    assert semantics["runtime_consumed"] is False


def test_disclosed_semantics_distinct_from_positive_presence():
    model = _load(SEMANTICS_PATH)
    disclosed = model["semantic_classes"]["disclosed_context_requirement"]
    hard = model["semantic_classes"]["hard_prerequisite_gate"]
    assert disclosed["runtime_requirement_mode"] == "disclosed"
    assert hard["runtime_requirement_mode"] == "present"
    assert disclosed["definition"] != hard["definition"]


def test_misclassification_patterns_document_hormone_and_aas():
    model = _load(SEMANTICS_PATH)
    patterns = model.get("misclassification_patterns") or []
    positive = next(p for p in patterns if p["pattern_id"] == "positive_presence_instead_of_disclosed")
    assert "medication.hormone_therapy" in positive["affected_keys"]
    assert "clinical_context.aas_exposure" in positive["affected_keys"]
