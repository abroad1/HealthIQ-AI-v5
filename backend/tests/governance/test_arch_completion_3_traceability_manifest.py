"""Governance tests for ARCH-COMPLETION-3 full traceability manifest."""

from __future__ import annotations

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
MANIFEST = REPO_ROOT / "knowledge_bus/governance/day_one_full_traceability_manifest_v1.yaml"


def _load() -> dict:
    assert MANIFEST.is_file(), "day_one_full_traceability_manifest_v1.yaml missing"
    return yaml.safe_load(MANIFEST.read_text(encoding="utf-8")) or {}


def test_manifest_exists_with_pipeline_phases_and_forbidden_inputs():
    payload = _load()
    assert payload.get("runtime_consumed") is True
    assert payload.get("pipeline_phases")
    assert payload.get("forbidden_runtime_inputs")
    assert "Batch_2_Pass_3.json" in payload["forbidden_runtime_inputs"]


def test_manifest_covers_required_domains():
    payload = _load()
    paths = {str(e.get("path") or "") for e in payload.get("entries") or []}
    required_fragments = [
        "orchestrator.py",
        "runtime_context_evaluator.py",
        "signal_evaluator.py",
        "report_compiler_v1.py",
        "output_authority_provenance_builder",
        "root_cause_compiler_v1.py",
        "narrative_report_compiler_v1.py",
        "frontend/",
    ]
    for fragment in required_fragments:
        assert any(fragment in p for p in paths), f"missing domain: {fragment}"


def test_narrative_compiler_classified_governed_compiled_asset():
    payload = _load()
    entry = next(
        e
        for e in payload.get("entries") or []
        if "narrative_report_compiler_v1.py" in str(e.get("path") or "")
    )
    assert entry["authority_classification"] == "GOVERNED_COMPILED_ASSET"
    assert entry.get("launch_gate_status") == "PASS"


def test_no_unknown_blocker_or_blocked_ungoverned_user_facing():
    payload = _load()
    for entry in payload.get("entries") or []:
        classification = entry.get("authority_classification")
        assert classification != "UNKNOWN_BLOCKER", entry.get("id")
        if entry.get("user_facing") is True:
            assert classification != "BLOCKED_UNGOVERNED", entry.get("id")
