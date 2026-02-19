"""
Sprint 16 - Unit tests for EvidenceRegistry v1.
"""

import pytest
from pydantic import ValidationError

from core.analytics.evidence_registry import load_evidence_registry
from core.contracts.evidence_registry_v1 import (
    EVIDENCE_REGISTRY_V1_VERSION,
    EvidenceItem,
    EvidenceRegistryStamp,
    canonical_json_sha256,
)


def test_evidence_registry_load_and_validation():
    """Registry loads with required version/hash and valid evidence items."""
    registry = load_evidence_registry()
    assert registry.stamp.evidence_registry_version == "1.0.0"
    assert len(registry.stamp.evidence_registry_hash) == 64
    assert registry.items
    for item in registry.items:
        assert item.evidence_id
        assert item.title
        assert item.source_type in ("guideline", "paper", "textbook", "expert_consensus", "internal_policy")
        assert item.quality_grade in ("high", "moderate", "low", "unknown")
        assert len(item.last_reviewed) >= 10  # YYYY-MM-DD


def test_evidence_registry_hash_is_stable():
    """Hash remains stable across repeated loads."""
    r1 = load_evidence_registry()
    r2 = load_evidence_registry()
    assert r1.stamp.evidence_registry_hash == r2.stamp.evidence_registry_hash
    assert r1.stamp.evidence_registry_version == r2.stamp.evidence_registry_version


def test_evidence_registry_items_sorted_by_evidence_id():
    """Items are deterministically sorted by evidence_id."""
    registry = load_evidence_registry()
    ids = [item.evidence_id for item in registry.items]
    assert ids == sorted(ids)


def test_evidence_registry_stamp_structure():
    """Stamp contains evidence_registry_version and evidence_registry_hash."""
    registry = load_evidence_registry()
    stamp = registry.stamp
    assert isinstance(stamp, EvidenceRegistryStamp)
    assert stamp.evidence_registry_version == EVIDENCE_REGISTRY_V1_VERSION
    assert all(c in "0123456789abcdef" for c in stamp.evidence_registry_hash)


def test_canonical_json_sha256_deterministic():
    """Canonical JSON SHA-256 produces stable hashes."""
    obj = {"a": 1, "b": [2, 3], "c": "x"}
    h1 = canonical_json_sha256(obj)
    h2 = canonical_json_sha256(obj)
    assert h1 == h2
    assert len(h1) == 64


def test_evidence_item_model_validates_enums():
    """EvidenceItem rejects invalid source_type and quality_grade."""
    with pytest.raises(ValidationError):
        EvidenceItem(
            evidence_id="x",
            title="t",
            source_type="invalid",  # type: ignore
            source_ref="ref",
            quality_grade="high",
            last_reviewed="2025-01-15",
        )
    with pytest.raises(ValidationError):
        EvidenceItem(
            evidence_id="x",
            title="t",
            source_type="guideline",
            source_ref="ref",
            quality_grade="invalid",  # type: ignore
            last_reviewed="2025-01-15",
        )


def test_evidence_item_model_validates_date_format():
    """EvidenceItem rejects invalid last_reviewed format."""
    with pytest.raises(ValidationError):
        EvidenceItem(
            evidence_id="x",
            title="t",
            source_type="guideline",
            source_ref="ref",
            quality_grade="high",
            last_reviewed="2025/01/15",  # wrong format
        )


def test_evidence_registry_fixture_mode_soft_fail_when_missing(monkeypatch, tmp_path):
    """Fixture mode: when SSOT file missing, returns empty registry with empty hash."""
    import core.analytics.evidence_registry as mod

    monkeypatch.setenv("HEALTHIQ_MODE", "fixture")
    monkeypatch.setattr(mod, "_registry_cache", None)
    monkeypatch.setattr(mod, "_evidence_registry_path", lambda: tmp_path / "nonexistent.yaml")

    registry = load_evidence_registry()
    assert registry.stamp.evidence_registry_version == EVIDENCE_REGISTRY_V1_VERSION
    assert registry.stamp.evidence_registry_hash == ""
    assert registry.items == []


def test_evidence_registry_fails_loud_when_missing(monkeypatch, tmp_path):
    """Production mode: when SSOT file missing, raises FileNotFoundError."""
    import core.analytics.evidence_registry as mod

    monkeypatch.delenv("HEALTHIQ_MODE", raising=False)
    monkeypatch.setattr(mod, "_registry_cache", None)
    monkeypatch.setattr(mod, "_evidence_registry_path", lambda: tmp_path / "nonexistent.yaml")

    with pytest.raises(FileNotFoundError, match="Evidence registry not found"):
        load_evidence_registry()
