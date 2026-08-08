"""
V5-CANONICAL-ACTIVATION-GATE-2 — governed write path for the activation register.

All programmatic mutations of ``package_runtime_activation_register_v1.yaml`` must go
through this module. Direct YAML edits remain possible via git, but day-one / integrity
validators fail closed on prohibited content; this helper is the required automation
path for append/remove so new entries cannot bypass:

- canonical activation-authority rules (register membership);
- ``runtime_medical_authority_integrity_v1`` prohibition validation;
- package-existence / identity preconditions;
- launch-critical provenance/lineage eligibility when mutating ``pkg_kb47_*``.

Does not invent medical policy. Launch-critical entries are allowed only when lineage
eligibility already passes (Stage 2 fold-in).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence

import yaml

from core.knowledge.canonical_runtime_activation_gate_v1 import (
    clear_canonical_activation_gate_cache,
)
from core.knowledge.package_activation_register_v1 import (
    activation_register_path,
    clear_activation_register_cache,
)
from core.knowledge.package_runtime_eligibility_v1 import (
    is_launch_critical_package_id,
    launch_critical_lineage_eligible,
    load_package_manifest,
)
from core.knowledge.runtime_medical_authority_integrity_v1 import (
    run_runtime_medical_authority_integrity_validation,
)


@dataclass(frozen=True)
class ActivationRegisterMutationResult:
    ok: bool
    errors: List[str]
    activated_frame_count: int
    added_keys: List[str]
    removed_keys: List[str]
    dry_run: bool


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _packages_dir(repo_root: Path) -> Path:
    return repo_root / "knowledge_bus" / "packages"


def _load_register_document(path: Path) -> Dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(payload, dict):
        raise ValueError("activation register root must be a mapping")
    frames = payload.get("activated_frames")
    if not isinstance(frames, list):
        raise ValueError("activated_frames must be a list")
    return payload


def _sorted_frames(frames: Sequence[Mapping[str, Any]]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for row in frames:
        if not isinstance(row, dict):
            raise ValueError("activated_frames row must be a mapping")
        key = str(row.get("activation_key") or "").strip()
        package_id = str(row.get("package_id") or "").strip()
        if not key or not package_id:
            raise ValueError("activated frame requires activation_key and package_id")
        rows.append({"activation_key": key, "package_id": package_id})
    return sorted(rows, key=lambda item: item["activation_key"])


def _validate_candidate_frame(repo_root: Path, activation_key: str, package_id: str) -> List[str]:
    errors: List[str] = []
    package_dir = _packages_dir(repo_root) / package_id
    if not package_dir.is_dir():
        errors.append(f"package directory missing for {package_id!r}: {package_dir}")
        return errors
    if not (package_dir / "signal_library.yaml").is_file():
        errors.append(f"signal_library.yaml missing for {package_id!r}")

    signal_id = activation_key.split("::", 1)[0] if "::" in activation_key else activation_key
    if not signal_id.startswith("signal_"):
        errors.append(f"activation_key signal_id must start with 'signal_': {activation_key!r}")
    if "::" not in activation_key:
        errors.append(f"activation_key must be signal_id::source_spec_id: {activation_key!r}")

    manifest = load_package_manifest(package_dir)
    if is_launch_critical_package_id(package_id):
        lineage_ok, status = launch_critical_lineage_eligible(manifest=manifest)
        if not lineage_ok:
            errors.append(
                f"launch-critical provenance/lineage eligibility failed for {package_id!r} "
                f"(status={status!r}); refusing register mutation"
            )
    return errors


def mutate_runtime_activation_register(
    *,
    add_frames: Optional[Sequence[Mapping[str, str]]] = None,
    remove_activation_keys: Optional[Sequence[str]] = None,
    repo_root: Optional[Path] = None,
    dry_run: bool = False,
) -> ActivationRegisterMutationResult:
    """
    Apply an additive/removal mutation to the governed activation register.

    Fail closed: returns ``ok=False`` with errors and does not write on any validation failure.
    """
    root = repo_root or _repo_root()
    path = (
        activation_register_path()
        if repo_root is None
        else root / "knowledge_bus" / "governance" / "package_runtime_activation_register_v1.yaml"
    )
    errors: List[str] = []
    added: List[str] = []
    removed: List[str] = []

    try:
        doc = _load_register_document(path)
        frames = _sorted_frames(doc.get("activated_frames") or [])
    except (OSError, ValueError, yaml.YAMLError) as exc:
        return ActivationRegisterMutationResult(
            ok=False,
            errors=[f"activation register write-path fail-closed: {exc}"],
            activated_frame_count=0,
            added_keys=[],
            removed_keys=[],
            dry_run=dry_run,
        )

    by_key = {row["activation_key"]: row for row in frames}

    for key in remove_activation_keys or []:
        activation_key = str(key or "").strip()
        if not activation_key:
            errors.append("remove_activation_keys contains an empty key")
            continue
        if activation_key in by_key:
            del by_key[activation_key]
            removed.append(activation_key)
        else:
            errors.append(f"cannot remove missing activation_key {activation_key!r}")

    for row in add_frames or []:
        if not isinstance(row, dict):
            errors.append("add_frames row must be a mapping")
            continue
        activation_key = str(row.get("activation_key") or "").strip()
        package_id = str(row.get("package_id") or "").strip()
        if not activation_key or not package_id:
            errors.append("add_frames row requires activation_key and package_id")
            continue
        errors.extend(_validate_candidate_frame(root, activation_key, package_id))
        if activation_key in by_key:
            existing_pkg = by_key[activation_key]["package_id"]
            if existing_pkg != package_id:
                errors.append(
                    f"conflicting package_id for {activation_key!r}: "
                    f"existing={existing_pkg!r} proposed={package_id!r}"
                )
            continue
        by_key[activation_key] = {"activation_key": activation_key, "package_id": package_id}
        added.append(activation_key)

    if errors:
        return ActivationRegisterMutationResult(
            ok=False,
            errors=sorted(set(errors)),
            activated_frame_count=len(by_key),
            added_keys=sorted(added),
            removed_keys=sorted(removed),
            dry_run=dry_run,
        )

    new_frames = _sorted_frames(list(by_key.values()))
    candidate = dict(doc)
    candidate["activated_frames"] = new_frames
    candidate["activated_frame_count"] = len(new_frames)

    integrity_errors = run_runtime_medical_authority_integrity_validation(
        repo_root=root,
        activation_register=candidate,
    )
    if integrity_errors:
        return ActivationRegisterMutationResult(
            ok=False,
            errors=integrity_errors,
            activated_frame_count=len(new_frames),
            added_keys=sorted(added),
            removed_keys=sorted(removed),
            dry_run=dry_run,
        )

    if dry_run:
        return ActivationRegisterMutationResult(
            ok=True,
            errors=[],
            activated_frame_count=len(new_frames),
            added_keys=sorted(added),
            removed_keys=sorted(removed),
            dry_run=True,
        )

    out_doc = dict(doc)
    out_doc["activated_frame_count"] = len(new_frames)
    out_doc["activated_frames"] = new_frames
    path.write_text(
        yaml.safe_dump(out_doc, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    clear_activation_register_cache()
    clear_canonical_activation_gate_cache()
    return ActivationRegisterMutationResult(
        ok=True,
        errors=[],
        activated_frame_count=len(new_frames),
        added_keys=sorted(added),
        removed_keys=sorted(removed),
        dry_run=False,
    )
