"""
Sprint 10 - Unit tests for RelationshipRegistry v1.
"""

from pathlib import Path

import pytest

import core.analytics.relationship_registry as relationship_registry
from core.analytics.relationship_registry import (
    evaluate_relationships,
    load_relationship_registry,
)


def test_relationship_registry_load_and_validation():
    """Registry loads with required version/hash and valid pairwise definitions."""
    registry = load_relationship_registry()
    assert registry.stamp.relationship_registry_version == "1.0.0"
    assert len(registry.stamp.relationship_registry_hash) == 64
    assert registry.definitions
    for definition in registry.definitions:
        assert len(definition.biomarkers) == 2


def test_relationship_registry_hash_is_stable():
    """Hash remains stable across repeated loads."""
    r1 = load_relationship_registry()
    r2 = load_relationship_registry()
    assert r1.stamp.relationship_registry_hash == r2.stamp.relationship_registry_hash
    assert r1.stamp.relationship_registry_version == r2.stamp.relationship_registry_version


def test_relationship_evaluation_deterministic_ordering():
    """Detections and evidence are deterministically sorted."""
    registry = load_relationship_registry()
    panel_view = {
        "hdl_cholesterol": {"status": "low", "score": 20.0},
        "triglycerides": {"status": "high", "score": 85.0},
        "apob": {"status": "high", "score": 75.0},
        "ldl_cholesterol": {"status": "normal", "score": 55.0},
    }
    derived_view = {"tg_hdl_ratio": {"status": "high", "score": 88.0}}
    out = evaluate_relationships(panel_view, derived_view, registry)
    ids = [d.relationship_id for d in out]
    assert ids == sorted(ids)
    for detection in out:
        assert detection.evidence == sorted(detection.evidence)


def test_sample_relationships_trigger_from_status_logic():
    """Two sample relationships trigger from status-based conditions."""
    registry = load_relationship_registry()
    panel_view = {
        "triglycerides": {"status": "high", "score": 84.0},
        "hdl_cholesterol": {"status": "low", "score": 22.0},
        "apob": {"status": "high", "score": 80.0},
        "ldl_cholesterol": {"status": "normal", "score": 56.0},
        "ferritin": {"status": "normal", "score": 52.0},
        "crp": {"status": "normal", "score": 46.0},
    }
    derived_view = {}
    out = evaluate_relationships(panel_view, derived_view, registry)
    by_id = {d.relationship_id: d for d in out}

    assert by_id["tg_hdl_metabolic_pattern"].triggered is True
    assert by_id["apob_ldl_discordance"].triggered is True
    assert by_id["ferritin_crp_inflammation_modifier"].triggered is False


def _write_relationships_yaml(tmp_path: Path, body: str) -> Path:
    path = tmp_path / "relationships.yaml"
    path.write_text(body, encoding="utf-8")
    return path


def test_unknown_biomarker_fails_validation(tmp_path, monkeypatch):
    """Unknown canonical biomarker IDs must fail validation."""
    path = _write_relationships_yaml(
        tmp_path,
        """
registry_version: "1.0.0"
schema_version: "1.0"
relationships:
  - relationship_id: "bad_biomarker"
    version: "1.0.0"
    biomarkers: ["not_a_real_biomarker", "hdl_cholesterol"]
    logic:
      all:
        - biomarker: "not_a_real_biomarker"
          status_in: ["high"]
          evidence_code: "x"
    classification_code: "X"
    severity: "low"
    description_short: "x"
""".strip(),
    )
    monkeypatch.setattr(relationship_registry, "_relationships_path", lambda: path)
    monkeypatch.setattr(
        relationship_registry,
        "_load_canonical_biomarkers",
        lambda: {"hdl_cholesterol", "triglycerides"},
    )
    monkeypatch.setattr(
        relationship_registry,
        "_load_derived_marker_ids",
        lambda: {"tg_hdl_ratio"},
    )
    monkeypatch.setattr(relationship_registry, "_registry_cache", None)

    with pytest.raises(ValueError, match="unknown biomarkers"):
        load_relationship_registry()


def test_valid_derived_marker_passes_even_if_not_in_biomarker_ssot(tmp_path, monkeypatch):
    """Derived marker validation must use derived ID domain, not biomarker SSOT."""
    path = _write_relationships_yaml(
        tmp_path,
        """
registry_version: "1.0.0"
schema_version: "1.0"
relationships:
  - relationship_id: "derived_ok"
    version: "1.0.0"
    biomarkers: ["triglycerides", "hdl_cholesterol"]
    uses_derived_markers: ["tg_hdl_ratio"]
    logic:
      any:
        - all:
            - derived_marker: "tg_hdl_ratio"
              status_in: ["high"]
              evidence_code: "tg_hdl_ratio_high"
    classification_code: "X"
    severity: "low"
    description_short: "x"
""".strip(),
    )
    monkeypatch.setattr(relationship_registry, "_relationships_path", lambda: path)
    # Deliberately exclude tg_hdl_ratio from biomarker domain
    monkeypatch.setattr(
        relationship_registry,
        "_load_canonical_biomarkers",
        lambda: {"triglycerides", "hdl_cholesterol"},
    )
    monkeypatch.setattr(
        relationship_registry,
        "_load_derived_marker_ids",
        lambda: {"tg_hdl_ratio"},
    )
    monkeypatch.setattr(relationship_registry, "_registry_cache", None)

    registry = load_relationship_registry()
    assert registry.definitions[0].relationship_id == "derived_ok"


def test_unknown_derived_marker_fails_validation(tmp_path, monkeypatch):
    """Unknown derived marker IDs must fail validation."""
    path = _write_relationships_yaml(
        tmp_path,
        """
registry_version: "1.0.0"
schema_version: "1.0"
relationships:
  - relationship_id: "derived_bad"
    version: "1.0.0"
    biomarkers: ["triglycerides", "hdl_cholesterol"]
    uses_derived_markers: ["not_a_real_derived"]
    logic:
      all:
        - derived_marker: "not_a_real_derived"
          status_in: ["high"]
          evidence_code: "bad"
    classification_code: "X"
    severity: "low"
    description_short: "x"
""".strip(),
    )
    monkeypatch.setattr(relationship_registry, "_relationships_path", lambda: path)
    monkeypatch.setattr(
        relationship_registry,
        "_load_canonical_biomarkers",
        lambda: {"triglycerides", "hdl_cholesterol"},
    )
    monkeypatch.setattr(
        relationship_registry,
        "_load_derived_marker_ids",
        lambda: {"tg_hdl_ratio"},
    )
    monkeypatch.setattr(relationship_registry, "_registry_cache", None)

    with pytest.raises(ValueError, match="unknown derived marker"):
        load_relationship_registry()
