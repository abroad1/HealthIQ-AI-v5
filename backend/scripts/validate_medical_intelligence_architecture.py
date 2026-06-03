#!/usr/bin/env python3
"""
ARCH-SENTINEL-1 — Medical intelligence architecture guardrail validator.

Read-only: does not mutate repository files. Exits non-zero on violation.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable, List, Sequence

import yaml

_REPO = Path(__file__).resolve().parents[2]

_RUNTIME_SCAN_ROOTS: Sequence[str] = (
    "backend/core",
    "backend/app",
    "frontend",
)

_PASS3_RUNTIME_MARKERS: Sequence[re.Pattern[str]] = (
    re.compile(r"knowledge_bus/research/investigation_specs"),
    re.compile(r"investigation_specs/multi_llm_research"),
    re.compile(r"[_-]Pass_3\.json", re.IGNORECASE),
    re.compile(r"[_-]pass_3\.json", re.IGNORECASE),
)

_GOVERNANCE_RUNTIME_MARKERS: Sequence[str] = (
    "medical_frame_identity_index_v1.yaml",
    "context_modifier_catalogue_draft_v1.yaml",
    "pass3_frame_coverage_audit_v1.yaml",
    "medical_frame_identity_expansion_candidates_v1.yaml",
    "creatinine_multiframe_authority_decision_v1.yaml",
    "knowledge_bus/governance/medical_frame_identity",
    "knowledge_bus/governance/context_modifier_catalogue",
    "knowledge_bus/governance/pass3_frame_coverage_audit",
)

_GOVERNANCE_YAML_PATHS: Sequence[str] = (
    "knowledge_bus/governance/medical_frame_identity_index_v1.yaml",
    "knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml",
    "knowledge_bus/governance/pass3_frame_coverage_audit_v1.yaml",
    "knowledge_bus/governance/medical_frame_identity_expansion_candidates_v1.yaml",
    "knowledge_bus/governance/creatinine_multiframe_authority_decision_v1.yaml",
)

_BLOCKED_PROMOTION_STATUSES: frozenset[str] = frozenset(
    {
        "blocked_pending_frame_adjudication",
        "blocked_pending_pass3_enrichment",
        "blocked_pending_provenance_recovery",
    }
)

_UNSAFE_PROMOTION_WITHOUT_OVERRIDE: frozenset[str] = frozenset(
    {
        "safe_for_route_a_promotion",
    }
)

_HELPER_SCRIPTS: Sequence[str] = (
    "backend/scripts/build_pass3_frame_coverage_audit.py",
)

_HELPER_FORBIDDEN_IMPORT_MARKERS: Sequence[str] = (
    "signal_evaluator",
    "SignalEvaluator",
    "SignalRegistry",
    "domain_score_assembler",
    "report_compiler_v1",
    "from core.pipeline",
)

_HELPER_FORBIDDEN_WRITE_MARKERS: Sequence[str] = (
    "knowledge_bus/packages/",
    "knowledge_bus/current/latest_knowledge_status",
    "frontend/",
)

_FRONTEND_FORBIDDEN_MARKERS: Sequence[str] = (
    "medical_frame_identity_index",
    "context_modifier_catalogue",
    "pass3_frame_coverage_audit",
    "Pass_3.json",
    "signal_library.yaml",
    "knowledge_bus/governance/",
    "inv_creatinine_high",
    "override_rules",
    "clinical_adjudication_status",
)

_CREATININE_LEGACY_FRAMES: Sequence[tuple[str, str]] = (
    ("frame_creatinine_legacy_s24_egfr_escalation", "blocked_pending_medical_review"),
    ("frame_creatinine_legacy_s24_potassium_escalation", "blocked_pending_medical_review"),
)


def _err(errors: List[str], msg: str) -> None:
    errors.append(msg)


def _iter_py_files(roots: Iterable[str]) -> Iterable[tuple[str, Path]]:
    for root_rel in roots:
        root = _REPO / root_rel
        if not root.is_dir():
            continue
        for path in root.rglob("*.py"):
            if "__pycache__" in path.parts:
                continue
            rel = path.relative_to(_REPO).as_posix()
            yield rel, path


def validate_no_raw_pass3_runtime_reads(errors: List[str]) -> None:
    for rel, path in _iter_py_files(_RUNTIME_SCAN_ROOTS):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            _err(errors, f"could not read {rel}: {exc}")
            continue
        for pattern in _PASS3_RUNTIME_MARKERS:
            if pattern.search(text):
                _err(
                    errors,
                    f"{rel} must not reference raw Pass_3 investigation specs at runtime ({pattern.pattern})",
                )


def validate_governance_not_runtime_consumed(errors: List[str]) -> None:
    for rel in _GOVERNANCE_YAML_PATHS:
        path = _REPO / rel
        if not path.is_file():
            _err(errors, f"missing governance artefact: {rel}")
            continue
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if doc.get("runtime_consumed") is not False:
            _err(errors, f"{rel}: runtime_consumed must be false")
        status = doc.get("status", "")
        if status and "runtime" in str(status) and "non_runtime" not in str(status):
            if status not in (
                "governed_non_runtime_index",
                "draft_governance_non_runtime",
                "governance_audit_non_runtime",
                "governed_adjudication_decision",
            ):
                _err(errors, f"{rel}: suspicious status {status!r}")

    for rel, path in _iter_py_files(_RUNTIME_SCAN_ROOTS):
        text = path.read_text(encoding="utf-8", errors="replace")
        for marker in _GOVERNANCE_RUNTIME_MARKERS:
            if marker in text:
                _err(
                    errors,
                    f"{rel} must not reference non-runtime governance artefact {marker!r}",
                )


def validate_duplicate_active_activation_keys(errors: List[str]) -> None:
    index_path = _REPO / "knowledge_bus/governance/medical_frame_identity_index_v1.yaml"
    if not index_path.is_file():
        _err(errors, "medical_frame_identity_index_v1.yaml missing")
        return
    proc = __import__("subprocess").run(
        [
            sys.executable,
            str(_REPO / "backend/scripts/validate_medical_frame_identity_index.py"),
            "--index",
            str(index_path),
        ],
        cwd=_REPO,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        _err(errors, "medical_frame_identity_index validator failed:\n" + (proc.stderr or proc.stdout))


def validate_index_multiframe_invariants(errors: List[str]) -> None:
    index_path = _REPO / "knowledge_bus/governance/medical_frame_identity_index_v1.yaml"
    doc = yaml.safe_load(index_path.read_text(encoding="utf-8")) or {}
    active_keys: dict[str, str] = {}
    for fam in doc.get("signal_families") or []:
        if not isinstance(fam, dict):
            continue
        for frame in fam.get("frames") or []:
            if not isinstance(frame, dict):
                continue
            fid = frame.get("medical_frame_id", "")
            authority = frame.get("runtime_authority_status")
            promotion = frame.get("promotion_state")
            akey = frame.get("activation_key", "")
            if authority == "active" and akey:
                if akey in active_keys:
                    _err(
                        errors,
                        f"duplicate active activation_key {akey!r} on {active_keys[akey]} and {fid}",
                    )
                else:
                    active_keys[akey] = fid
            if promotion == "compiled_not_promoted" and frame.get("collision_status") not in (
                "allowed_non_runtime_collision",
                "none",
                "requires_adjudication",
            ):
                _err(
                    errors,
                    f"{fid}: compiled_not_promoted requires explicit collision classification",
                )
            if promotion == "runtime_active_legacy_unadjudicated":
                if frame.get("clinical_adjudication_status") == "not_required":
                    _err(
                        errors,
                        f"{fid}: legacy unadjudicated frame must not have not_required clinical status",
                    )


def validate_frontend_render_only(errors: List[str]) -> None:
    frontend_root = _REPO / "frontend"
    if not frontend_root.is_dir():
        _err(errors, "frontend/ missing")
        return
    for path in frontend_root.rglob("*"):
        if path.suffix not in (".ts", ".tsx", ".js", ".jsx"):
            continue
        if "node_modules" in path.parts or ".next" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        rel = path.relative_to(_REPO).as_posix()
        for marker in _FRONTEND_FORBIDDEN_MARKERS:
            if marker in text:
                _err(errors, f"{rel} must not embed medical-intelligence source ({marker!r})")


def validate_promotion_safety_gate(errors: List[str]) -> None:
    audit_path = _REPO / "knowledge_bus/governance/pass3_frame_coverage_audit_v1.yaml"
    if not audit_path.is_file():
        _err(errors, "pass3_frame_coverage_audit_v1.yaml missing")
        return
    doc = yaml.safe_load(audit_path.read_text(encoding="utf-8")) or {}
    for pkg in doc.get("packages") or []:
        if not isinstance(pkg, dict):
            continue
        pid = pkg.get("package_id", "")
        safety = pkg.get("promotion_safety_status", "")
        if safety in _BLOCKED_PROMOTION_STATUSES and safety in _UNSAFE_PROMOTION_WITHOUT_OVERRIDE:
            _err(errors, f"{pid}: contradictory promotion safety flags")
        if safety in _BLOCKED_PROMOTION_STATUSES:
            continue
        if safety == "safe_for_route_a_promotion":
            _err(
                errors,
                f"{pid}: safe_for_route_a_promotion is forbidden in current estate (0 naive ROUTE_A safe packages)",
            )


def validate_creatinine_legacy_frames_preserved(errors: List[str]) -> None:
    index_path = _REPO / "knowledge_bus/governance/medical_frame_identity_index_v1.yaml"
    doc = yaml.safe_load(index_path.read_text(encoding="utf-8")) or {}
    frames_by_id: dict[str, dict] = {}
    for fam in doc.get("signal_families") or []:
        for frame in fam.get("frames") or []:
            if isinstance(frame, dict) and frame.get("medical_frame_id"):
                frames_by_id[frame["medical_frame_id"]] = frame
    for frame_id, expected_clinical in _CREATININE_LEGACY_FRAMES:
        frame = frames_by_id.get(frame_id)
        if frame is None:
            _err(errors, f"missing creatinine legacy frame {frame_id}")
            continue
        if frame.get("clinical_adjudication_status") != expected_clinical:
            _err(
                errors,
                f"{frame_id}: clinical_adjudication_status must remain {expected_clinical!r}",
            )
        if frame.get("promotion_state") != "runtime_active_legacy_unadjudicated":
            _err(
                errors,
                f"{frame_id}: must remain runtime_active_legacy_unadjudicated",
            )


def validate_governance_helper_boundaries(errors: List[str]) -> None:
    scripts: list[str] = list(_HELPER_SCRIPTS)
    tools_dir = _REPO / "knowledge_bus/tools"
    if tools_dir.is_dir():
        for path in tools_dir.glob("*.py"):
            scripts.append(path.relative_to(_REPO).as_posix())
    for rel in scripts:
        path = _REPO / rel
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for marker in _HELPER_FORBIDDEN_IMPORT_MARKERS:
            if marker in text:
                _err(errors, f"{rel}: governance helper must not import runtime module ({marker!r})")
        for marker in _HELPER_FORBIDDEN_WRITE_MARKERS:
            if marker in text and ("write" in text or "open(" in text or "write_text" in text):
                if f'"{marker}' in text or f"'{marker}" in text:
                    _err(
                        errors,
                        f"{rel}: governance helper must not write to runtime path ({marker!r})",
                    )


def run_medical_intelligence_architecture_validation(*, repo_root: Path | None = None) -> List[str]:
    global _REPO  # noqa: PLW0603
    if repo_root is not None:
        _REPO = repo_root
    errors: List[str] = []
    validate_no_raw_pass3_runtime_reads(errors)
    validate_governance_not_runtime_consumed(errors)
    validate_duplicate_active_activation_keys(errors)
    validate_index_multiframe_invariants(errors)
    validate_frontend_render_only(errors)
    validate_promotion_safety_gate(errors)
    validate_creatinine_legacy_frames_preserved(errors)
    validate_governance_helper_boundaries(errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate ARCH-SENTINEL medical intelligence architecture guardrails."
    )
    parser.add_argument("--repo", type=Path, default=_REPO, help="Repository root")
    args = parser.parse_args()
    errors = run_medical_intelligence_architecture_validation(repo_root=args.repo)
    if errors:
        print("medical_intelligence_architecture_validation: FAIL", file=sys.stderr)
        for item in errors:
            print(f"  - {item}", file=sys.stderr)
        return 1
    print("medical_intelligence_architecture_validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
