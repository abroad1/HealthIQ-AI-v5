"""
v5.3 Sprint 5 - Unit tests for calibration registry.
"""

from pathlib import Path

import pytest

import core.analytics.calibration_registry as registry_module
from core.analytics.calibration_registry import load_calibration_registry


def test_calibration_registry_load_validation_and_stamp():
    reg = load_calibration_registry()
    assert reg.rules
    assert reg.stamp.calibration_registry_version == "1.0.0"
    assert len(reg.stamp.calibration_registry_hash) == 64


def test_calibration_registry_rule_sorting_is_deterministic():
    reg = load_calibration_registry()
    pairs = [(r.rank, r.rule_id) for r in reg.rules]
    assert pairs == sorted(pairs)


def test_calibration_registry_duplicate_rule_id_fails(tmp_path, monkeypatch):
    p = tmp_path / "calibration_registry.yaml"
    p.write_text(
        """
registry_version: "1.0.0"
schema_version: "1.0"
calibration_rules:
  - rule_id: "dup"
    match: {}
    outputs:
      priority_tier: "p3"
      urgency_band: "routine"
      action_intensity: "info"
      stability_flag: "stable"
      explanation_codes: []
    precedence: { rank: 1 }
  - rule_id: "dup"
    match: {}
    outputs:
      priority_tier: "p2"
      urgency_band: "soon"
      action_intensity: "medium"
      stability_flag: "unstable"
      explanation_codes: []
    precedence: { rank: 2 }
        """.strip(),
        encoding="utf-8",
    )
    monkeypatch.setattr(registry_module, "_registry_cache", None)
    monkeypatch.setattr(registry_module, "_registry_path", lambda: p)
    with pytest.raises(ValueError, match="duplicate rule_id"):
        load_calibration_registry()


def test_calibration_registry_fixture_soft_fail_when_missing(tmp_path, monkeypatch):
    p = Path(tmp_path) / "missing.yaml"
    monkeypatch.setenv("HEALTHIQ_MODE", "fixture")
    monkeypatch.setattr(registry_module, "_registry_cache", None)
    monkeypatch.setattr(registry_module, "_registry_path", lambda: p)
    reg = load_calibration_registry()
    assert reg.rules == []
    assert reg.stamp.calibration_registry_hash == ""


def test_calibration_registry_production_fail_when_missing(tmp_path, monkeypatch):
    p = Path(tmp_path) / "missing.yaml"
    monkeypatch.delenv("HEALTHIQ_MODE", raising=False)
    monkeypatch.setattr(registry_module, "_registry_cache", None)
    monkeypatch.setattr(registry_module, "_registry_path", lambda: p)
    with pytest.raises(FileNotFoundError, match="Calibration registry not found"):
        load_calibration_registry()
