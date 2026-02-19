"""
v5.3 Sprint 4 - Unit tests for CausalLayer registry loader.
"""

from pathlib import Path

import pytest

import core.analytics.causal_layer_registry as registry_module
from core.analytics.causal_layer_registry import load_causal_layer_registry


def test_causal_layer_registry_load_and_stamp():
    reg = load_causal_layer_registry()
    assert reg.rules
    assert reg.stamp.causal_layer_registry_version == "1.0.0"
    assert len(reg.stamp.causal_layer_registry_hash) == 64


def test_causal_layer_registry_deterministic_order():
    reg = load_causal_layer_registry()
    ids = [r.edge_id for r in reg.rules]
    assert ids == sorted(ids)


def test_causal_layer_registry_duplicate_id_fails(tmp_path, monkeypatch):
    p = tmp_path / "causal_layer_registry.yaml"
    p.write_text(
        """
registry_version: "1.0.0"
schema_version: "1.0"
rules:
  - edge_id: "dup"
    from_system_id: "a"
    to_system_id: "b"
    edge_type: "driver"
    priority: 1
    conditions: []
    rationale_codes: []
  - edge_id: "dup"
    from_system_id: "a"
    to_system_id: "c"
    edge_type: "driver"
    priority: 1
    conditions: []
    rationale_codes: []
        """.strip(),
        encoding="utf-8",
    )
    monkeypatch.setattr(registry_module, "_registry_cache", None)
    monkeypatch.setattr(registry_module, "_registry_path", lambda: p)
    with pytest.raises(ValueError, match="duplicate edge_id"):
        load_causal_layer_registry()


def test_causal_layer_registry_fixture_soft_fail_when_missing(tmp_path, monkeypatch):
    p = Path(tmp_path) / "missing.yaml"
    monkeypatch.setenv("HEALTHIQ_MODE", "fixture")
    monkeypatch.setattr(registry_module, "_registry_cache", None)
    monkeypatch.setattr(registry_module, "_registry_path", lambda: p)
    reg = load_causal_layer_registry()
    assert reg.rules == []
    assert reg.stamp.causal_layer_registry_hash == ""


def test_causal_layer_registry_production_fail_when_missing(tmp_path, monkeypatch):
    p = Path(tmp_path) / "missing.yaml"
    monkeypatch.delenv("HEALTHIQ_MODE", raising=False)
    monkeypatch.setattr(registry_module, "_registry_cache", None)
    monkeypatch.setattr(registry_module, "_registry_path", lambda: p)
    with pytest.raises(FileNotFoundError, match="Causal layer registry not found"):
        load_causal_layer_registry()
