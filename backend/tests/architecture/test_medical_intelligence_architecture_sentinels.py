"""ARCH-SENTINEL-1 — medical intelligence architecture sentinel tests."""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[3]
_VALIDATOR = _REPO / "backend" / "scripts" / "validate_medical_intelligence_architecture.py"
_GATE = _REPO / "backend" / "scripts" / "run_architecture_validation_gate.py"
_SENTINEL_PACK = _REPO / "sentinel" / "packs" / "medical_intelligence_architecture_guardrails_v1.json"


def _load_validator():
    spec = importlib.util.spec_from_file_location(
        "validate_medical_intelligence_architecture", _VALIDATOR
    )
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_medical_intelligence_validator_passes_on_current_repo():
    mod = _load_validator()
    errors = mod.run_medical_intelligence_architecture_validation(repo_root=_REPO)
    assert errors == [], "\n".join(errors)


def test_medical_intelligence_validator_cli_exit_zero():
    proc = subprocess.run(
        [sys.executable, str(_VALIDATOR)],
        cwd=_REPO,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout
    assert "medical_intelligence_architecture_validation: PASS" in proc.stdout


_GOVERNANCE_NON_RUNTIME_PATHS: tuple[str, ...] = (
    "knowledge_bus/governance/medical_frame_identity_index_v1.yaml",
    "knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml",
    "knowledge_bus/governance/pass3_frame_coverage_audit_v1.yaml",
    "knowledge_bus/governance/medical_frame_identity_expansion_candidates_v1.yaml",
    "knowledge_bus/governance/creatinine_multiframe_authority_decision_v1.yaml",
)


def test_governance_artefacts_declare_non_runtime():
    import yaml

    for rel in _GOVERNANCE_NON_RUNTIME_PATHS:
        path = _REPO / rel
        assert path.is_file(), f"missing governance artefact: {rel}"
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        assert doc.get("runtime_consumed") is False, rel


def test_architecture_validation_gate_cli_exit_zero():
    if os.environ.get("ARCHITECTURE_GATE_CHILD") == "1":
        pytest.skip("full gate already executed by run_architecture_validation_gate.py")

    proc = subprocess.run(
        [sys.executable, str(_GATE)],
        cwd=_REPO,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout
    assert "architecture_validation_gate: PASS" in proc.stdout


def test_sentinel_pack_references_gate_and_validator():
    import json

    assert _SENTINEL_PACK.is_file()
    payload = json.loads(_SENTINEL_PACK.read_text(encoding="utf-8"))
    assert payload.get("pack_id") == "medical_intelligence_architecture_guardrails_v1"
    assert "validate_medical_intelligence_architecture" in payload.get("validator_script", "")
    assert "run_architecture_validation_gate" in payload.get("gate_script", "")


def test_creatinine_legacy_s24_frames_present():
    import yaml

    doc = yaml.safe_load(
        (_REPO / "knowledge_bus/governance/medical_frame_identity_index_v1.yaml").read_text(
            encoding="utf-8"
        )
    ) or {}
    frame_ids = {
        f.get("medical_frame_id")
        for fam in doc.get("signal_families") or []
        for f in fam.get("frames") or []
        if isinstance(f, dict)
    }
    assert "frame_creatinine_legacy_s24_egfr_escalation" in frame_ids
    assert "frame_creatinine_legacy_s24_potassium_escalation" in frame_ids
