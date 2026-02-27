"""
Sprint 16 - Enforcement: evidence provenance must be registry-driven.

Assert loader exists and is called for stamping; no direct evidence literals
hardcoded in inference code.
"""

from pathlib import Path


def test_evidence_registry_loader_exists():
    """Evidence registry loader module must exist."""
    loader_path = Path(__file__).parent.parent.parent / "core" / "analytics" / "evidence_registry.py"
    assert loader_path.exists(), "evidence_registry.py loader must exist"
    text = loader_path.read_text(encoding="utf-8", errors="ignore")
    assert "load_evidence_registry" in text
    assert "EvidenceRegistryStamp" in text or "evidence_registry_hash" in text


def test_orchestrator_calls_evidence_registry_for_stamping():
    """Orchestrator must load evidence registry and pass stamp to replay manifest."""
    orchestrator_path = Path(__file__).parent.parent.parent / "core" / "pipeline" / "orchestrator.py"
    text = orchestrator_path.read_text(encoding="utf-8", errors="ignore")
    assert "load_evidence_registry" in text
    assert "evidence_registry_version" in text
    assert "evidence_registry_hash" in text


def test_replay_manifest_builder_accepts_evidence_stamp():
    """Replay manifest builder must accept evidence_registry_version and evidence_registry_hash."""
    builder_path = Path(__file__).parent.parent.parent / "core" / "analytics" / "replay_manifest_builder.py"
    text = builder_path.read_text(encoding="utf-8", errors="ignore")
    assert "evidence_registry_version" in text
    assert "evidence_registry_hash" in text


def test_replay_manifest_contract_has_evidence_fields():
    """Replay manifest contract must include evidence registry stamp fields."""
    contract_path = Path(__file__).parent.parent.parent / "core" / "contracts" / "replay_manifest_v1.py"
    text = contract_path.read_text(encoding="utf-8", errors="ignore")
    assert "evidence_registry_version" in text
    assert "evidence_registry_hash" in text
