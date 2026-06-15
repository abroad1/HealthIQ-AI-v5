#!/usr/bin/env python3
"""
ARCH-COMPLETION-3 — Deterministic day-one launch estate gate validator.

Read-only: does not mutate repository files. Exits non-zero on violation.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Sequence

import yaml

_REPO = Path(__file__).resolve().parents[2]

_MANIFEST = _REPO / "knowledge_bus/governance/day_one_full_traceability_manifest_v1.yaml"
_GATE = _REPO / "knowledge_bus/governance/day_one_launch_estate_gate_v1.yaml"
_AUTHORITY_MODEL = _REPO / "knowledge_bus/governance/compiled_output_authority_model_v1.yaml"
_ROOT_CAUSE_REGISTER = _REPO / "knowledge_bus/governance/root_cause_authority_register_v1.yaml"
_CARD_REGISTER = _REPO / "knowledge_bus/governance/card_authority_register_v1.yaml"
_NARRATIVE_COMPILER = "backend/core/analytics/narrative_report_compiler_v1.py"
_REPORT_V1 = _REPO / "backend/core/contracts/report_v1.py"
_BATCH2_REGISTER = (
    _REPO / "knowledge_bus/governance/batch2_full_coverage_activation_execution_register_v1.yaml"
)

_ALLOWED_VERDICTS: Sequence[str] = (
    "DAY_ONE_ARCHITECTURE_COMPLETE",
    "DAY_ONE_ARCHITECTURE_COMPLETE_WITH_NON_BLOCKING_CARRY_FORWARD",
    "DAY_ONE_ARCHITECTURE_NOT_COMPLETE",
)

_LAUNCH_CRITICAL_REL_PATHS: Sequence[str] = (
    "backend/core/knowledge/health_system_card_evidence.py",
    "backend/core/knowledge/domain_flat_card_evidence.py",
    "backend/core/knowledge/compiled_hypothesis.py",
    "backend/core/knowledge/load_root_cause_hypotheses.py",
    "backend/core/analytics/root_cause_compiler_v1.py",
    "backend/core/analytics/wave1_subsystem_evidence.py",
    "backend/core/analytics/report_compiler_v1.py",
    "backend/core/analytics/domain_narrative_wave1.py",
    "backend/core/analytics/signal_evaluator.py",
    "backend/core/pipeline/orchestrator.py",
    "backend/core/pipeline/orchestrator_phases_v1.py",
    "backend/core/analytics/runtime_context_evaluator.py",
    "backend/core/analytics/narrative_report_compiler_v1.py",
    "backend/core/analytics/output_authority_provenance_builder_v1.py",
    "backend/core/knowledge/compiled_output_authority_v1.py",
)

_RUNTIME_SCAN_EXCLUSIONS: Sequence[str] = (
    "backend/core/knowledge/investigation_spec_to_promoted_signal.py",
    "backend/core/knowledge/package_provenance_scan_v1.py",
)

_FORBIDDEN_RUNTIME_MARKERS: Sequence[tuple[str, str]] = (
    ("Batch_2_Pass_3.json", "raw Pass 3"),
    ("knowledge_bus/research/investigation_specs", "investigation specs"),
)

_INACTIVE_DHEA_PACKAGES: Sequence[str] = (
    "pkg_kb47_dhea_high_androgen_excess_context",
    "pkg_kb47_dhea_low_adrenal_androgen_reduction",
)


def _load_yaml(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(str(path))
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _err(errors: List[str], msg: str) -> None:
    errors.append(msg)


def _scan_backend_core_forbidden(errors: List[str]) -> None:
    for rel in _LAUNCH_CRITICAL_REL_PATHS:
        if rel in _RUNTIME_SCAN_EXCLUSIONS:
            continue
        path = _REPO / rel
        if not path.is_file():
            _err(errors, f"missing launch-critical runtime path: {rel}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker, label in _FORBIDDEN_RUNTIME_MARKERS:
            if marker in text:
                _err(errors, f"forbidden {label} reference in runtime path: {rel}")


def _find_manifest_entry(manifest: dict, *, path_contains: str) -> dict | None:
    for entry in manifest.get("entries") or []:
        path = str(entry.get("path") or "")
        if path_contains in path:
            return entry
    return None


def validate(errors: List[str]) -> None:
    if not _MANIFEST.is_file():
        _err(errors, f"missing traceability manifest: {_MANIFEST.relative_to(_REPO)}")
        return
    if not _GATE.is_file():
        _err(errors, f"missing launch estate gate: {_GATE.relative_to(_REPO)}")
        return

    manifest = _load_yaml(_MANIFEST)
    gate = _load_yaml(_GATE)

    for artefact, label in (
        (_AUTHORITY_MODEL, "compiled_output_authority_model_v1.yaml"),
        (_ROOT_CAUSE_REGISTER, "root_cause_authority_register_v1.yaml"),
        (_CARD_REGISTER, "card_authority_register_v1.yaml"),
    ):
        if not artefact.is_file():
            _err(errors, f"missing governance artefact: {label}")

    report_text = _REPORT_V1.read_text(encoding="utf-8")
    if "output_authority_provenance_v1" not in report_text:
        _err(errors, "ReportV1 missing output_authority_provenance_v1 field")

    for entry in manifest.get("entries") or []:
        classification = entry.get("authority_classification")
        entry_id = entry.get("id") or entry.get("path") or "unknown"
        if classification == "UNKNOWN_BLOCKER":
            _err(errors, f"manifest entry {entry_id} is UNKNOWN_BLOCKER")
        if entry.get("user_facing") is True and classification == "BLOCKED_UNGOVERNED":
            _err(errors, f"user-facing path {entry_id} is BLOCKED_UNGOVERNED")

    narrative = _find_manifest_entry(manifest, path_contains="narrative_report_compiler_v1.py")
    if narrative is None:
        _err(errors, "narrative_report_compiler_v1.py not classified in traceability manifest")
    elif narrative.get("authority_classification") != "GOVERNED_COMPILED_ASSET":
        _err(
            errors,
            "narrative_report_compiler_v1.py must be GOVERNED_COMPILED_ASSET "
            f"(got {narrative.get('authority_classification')})",
        )

    frontend = _find_manifest_entry(manifest, path_contains="frontend/")
    if frontend is None:
        _err(errors, "frontend render-only boundary not classified in manifest")
    elif frontend.get("authority_classification") != "GOVERNED_RENDER_ONLY":
        _err(errors, "frontend must be classified GOVERNED_RENDER_ONLY")

    rc_reg = _load_yaml(_ROOT_CAUSE_REGISTER) if _ROOT_CAUSE_REGISTER.is_file() else {}
    rc_entries = rc_reg.get("entries") or []
    fallback = next(
        (e for e in rc_entries if e.get("root_cause_id") == "why_engine_fallback_v1"),
        None,
    )
    if fallback is None:
        _err(errors, "why_engine_fallback_v1 missing from root_cause_authority_register")
    elif fallback.get("activation_status") != "ROOT_CAUSE_UNTRACEABLE_BLOCKED":
        _err(errors, "why_engine_fallback_v1 must be ROOT_CAUSE_UNTRACEABLE_BLOCKED")

    verdict = gate.get("final_verdict")
    allowed = gate.get("allowed_final_verdicts") or list(_ALLOWED_VERDICTS)
    if verdict not in allowed:
        _err(errors, f"launch estate final_verdict invalid: {verdict!r}")

    if _BATCH2_REGISTER.is_file():
        batch2 = _load_yaml(_BATCH2_REGISTER)
        activated = {row.get("package_id") for row in batch2.get("activated_packages") or []}
        for row in batch2.get("kept_inactive_packages") or []:
            pkg_id = str(row.get("package_id") or "")
            if pkg_id in _INACTIVE_DHEA_PACKAGES:
                if pkg_id in activated:
                    _err(errors, f"DHEA package must remain inactive but is activated: {pkg_id}")

    _scan_backend_core_forbidden(errors)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate day-one launch estate gate")
    parser.parse_args()
    errors: List[str] = []
    try:
        validate(errors)
    except FileNotFoundError as exc:
        errors.append(str(exc))
    if errors:
        for msg in errors:
            print(f"day_one_launch_estate_gate: FAIL: {msg}", file=sys.stderr)
        return 1
    print("day_one_launch_estate_gate: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
