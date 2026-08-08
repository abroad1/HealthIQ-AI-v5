"""
V5-RUNTIME-AUTHORITY-INTEGRITY-1 — cross-authority activation integrity.

Reconciles explicit governed activation prohibitions with the runtime package
activation register. This is a validation/enforcement invariant only: it does not
create a third medical activation SSOT.

Semantic boundary (mandatory):
- ``LEGACY_RETIRED``, ``SUPERSEDED_BY_*``, and other WHY-skip / non-owning states are
  **not** treated as runtime deactivation by themselves.
- Runtime activation is prohibited only where existing governed authority explicitly
  establishes that the signal / activation must not be active.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

import yaml

#: Explicit activation-prohibition statuses recognised on medical decision registers.
EXPLICIT_PROHIBITION_STATUSES = frozenset(
    {
        "NOT_AUTHORISED",
        "DO_NOT_ACTIVATE",
        "REJECTED_FOR_ACTIVATION",
        "REJECTED",
    }
)

#: Anthony decision tokens that explicitly prohibit activation (not mere WHY retirement).
EXPLICIT_ANTHONY_PROHIBITION_TOKENS = frozenset(
    {
        "NOT_AUTHORISED",
        "NOT_AUTHORISED_WAVE1",
        "NOT_AUTHORISED_WAVE2",
        "DO_NOT_ACTIVATE",
        "REJECTED_FOR_ACTIVATION",
    }
)


@dataclass(frozen=True)
class ExplicitActivationProhibition:
    """One explicit activation prohibition drawn from governed artefacts."""

    signal_id: str
    activation_key: str
    status: str
    source: str
    reason: str = ""


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def activation_register_path(repo_root: Optional[Path] = None) -> Path:
    root = repo_root or _repo_root()
    return root / "knowledge_bus" / "governance" / "package_runtime_activation_register_v1.yaml"


def compiled_why_register_path(repo_root: Optional[Path] = None) -> Path:
    root = repo_root or _repo_root()
    return root / "knowledge_bus" / "governance" / "compiled_why_authority_register_v1.yaml"


def medical_decision_register_glob(repo_root: Optional[Path] = None) -> Path:
    root = repo_root or _repo_root()
    return root / "docs" / "architecture"


def _signal_id_from_activation_key(activation_key: str) -> str:
    key = str(activation_key or "").strip()
    if "::" in key:
        return key.split("::", 1)[0].strip()
    return key


def _load_yaml_mapping(path: Path) -> Dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"missing governed artefact: {path}")
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(payload, dict):
        raise ValueError(f"governed artefact root must be a mapping: {path}")
    return payload


def _anthony_decision_is_explicit_prohibition(decision: str) -> bool:
    token = str(decision or "").strip()
    if not token:
        return False
    if token in EXPLICIT_ANTHONY_PROHIBITION_TOKENS:
        return True
    # Fail closed for future NOT_AUTHORISED_* tokens without inventing new medical meaning.
    return token.startswith("NOT_AUTHORISED")


def collect_explicit_activation_prohibitions(
    *,
    repo_root: Optional[Path] = None,
    why_register: Optional[Mapping[str, Any]] = None,
    medical_registers: Optional[Sequence[Tuple[str, Mapping[str, Any]]]] = None,
) -> List[ExplicitActivationProhibition]:
    """
    Collect explicit activation prohibitions from governed artefacts.

    Sources:
    1. Wave / ARCH medical decision registers: ``blocked_targets`` with explicit status.
    2. Compiled WHY register: rows whose ``anthony_decision`` is an explicit prohibition.
    """
    root = repo_root or _repo_root()
    prohibitions: List[ExplicitActivationProhibition] = []

    if medical_registers is None:
        arch_dir = medical_decision_register_glob(root)
        discovered: List[Tuple[str, Mapping[str, Any]]] = []
        if arch_dir.is_dir():
            for path in sorted(arch_dir.glob("*medical_decision_register*.yaml")):
                discovered.append((str(path.relative_to(root)).replace("\\", "/"), _load_yaml_mapping(path)))
        medical_registers = discovered

    for source, doc in medical_registers:
        blocked = doc.get("blocked_targets") or []
        if not isinstance(blocked, list):
            raise ValueError(f"{source}: blocked_targets must be a list")
        for row in blocked:
            if not isinstance(row, dict):
                raise ValueError(f"{source}: blocked_targets row must be a mapping")
            status = str(row.get("status") or "").strip()
            if status not in EXPLICIT_PROHIBITION_STATUSES:
                continue
            signal_id = str(row.get("signal_id") or "").strip()
            activation_key = str(row.get("activation_key") or "").strip()
            if not signal_id and activation_key:
                signal_id = _signal_id_from_activation_key(activation_key)
            if not signal_id and not activation_key:
                raise ValueError(f"{source}: blocked_targets row missing signal_id/activation_key")
            prohibitions.append(
                ExplicitActivationProhibition(
                    signal_id=signal_id,
                    activation_key=activation_key,
                    status=status,
                    source=f"{source}#blocked_targets",
                    reason=str(row.get("reason") or "").strip(),
                )
            )

    if why_register is None:
        why_register = _load_yaml_mapping(compiled_why_register_path(root))
    frames = why_register.get("frames") or []
    if not isinstance(frames, list):
        raise ValueError("compiled WHY register frames must be a list")

    # Detect conflicting anthony_decision values for the same activation_key.
    by_key: Dict[str, set[str]] = {}
    for row in frames:
        if not isinstance(row, dict):
            raise ValueError("compiled WHY frame row must be a mapping")
        activation_key = str(row.get("activation_key") or "").strip()
        decision = str(row.get("anthony_decision") or "").strip()
        if activation_key and decision:
            by_key.setdefault(activation_key, set()).add(decision)

    conflicts = sorted(key for key, decisions in by_key.items() if len(decisions) > 1)
    if conflicts:
        raise ValueError(
            "conflicting anthony_decision values for activation_key(s): "
            + ", ".join(conflicts)
        )

    for row in frames:
        assert isinstance(row, dict)
        decision = str(row.get("anthony_decision") or "").strip()
        if not _anthony_decision_is_explicit_prohibition(decision):
            continue
        activation_key = str(row.get("activation_key") or "").strip()
        signal_id = str(row.get("signal_id") or "").strip() or _signal_id_from_activation_key(
            activation_key
        )
        if not signal_id and not activation_key:
            raise ValueError("compiled WHY prohibition row missing signal_id/activation_key")
        prohibitions.append(
            ExplicitActivationProhibition(
                signal_id=signal_id,
                activation_key=activation_key,
                status=decision,
                source="knowledge_bus/governance/compiled_why_authority_register_v1.yaml#anthony_decision",
                reason=str(row.get("notes") or row.get("reason") or "").strip(),
            )
        )

    return prohibitions


def _activated_frames_from_register(payload: Mapping[str, Any]) -> List[Dict[str, str]]:
    frames = payload.get("activated_frames") or []
    if not isinstance(frames, list):
        raise ValueError("activated_frames must be a list")
    out: List[Dict[str, str]] = []
    for row in frames:
        if not isinstance(row, dict):
            raise ValueError("activated_frames row must be a mapping")
        key = str(row.get("activation_key") or "").strip()
        package_id = str(row.get("package_id") or "").strip()
        if not key:
            raise ValueError("activated_frames row missing activation_key")
        out.append({"activation_key": key, "package_id": package_id})
    return out


def prohibition_matches_activation(
    prohibition: ExplicitActivationProhibition, activation_key: str
) -> bool:
    key = str(activation_key or "").strip()
    if not key:
        return False
    if prohibition.activation_key and prohibition.activation_key == key:
        return True
    if prohibition.signal_id and (
        key == prohibition.signal_id or key.startswith(f"{prohibition.signal_id}::")
    ):
        return True
    return False


def find_runtime_activation_violations(
    *,
    activated_frames: Sequence[Mapping[str, str]],
    prohibitions: Sequence[ExplicitActivationProhibition],
) -> List[str]:
    """Return deterministic error strings for prohibited activations present at runtime."""
    errors: List[str] = []
    for frame in activated_frames:
        activation_key = str(frame.get("activation_key") or "").strip()
        package_id = str(frame.get("package_id") or "").strip()
        hits = [p for p in prohibitions if prohibition_matches_activation(p, activation_key)]
        if not hits:
            continue
        # Stable, exact conflict report.
        sources = sorted({p.source for p in hits})
        statuses = sorted({p.status for p in hits})
        signal_ids = sorted({p.signal_id for p in hits if p.signal_id})
        errors.append(
            "runtime activation prohibited: "
            f"activation_key={activation_key!r} package_id={package_id!r} "
            f"signal_id={signal_ids!r} prohibition_status={statuses!r} "
            f"authority_source={sources!r}"
        )
    return sorted(set(errors))


def run_runtime_medical_authority_integrity_validation(
    *,
    repo_root: Optional[Path] = None,
    activation_register: Optional[Mapping[str, Any]] = None,
    why_register: Optional[Mapping[str, Any]] = None,
    medical_registers: Optional[Sequence[Tuple[str, Mapping[str, Any]]]] = None,
) -> List[str]:
    """
    Fail-closed integrity check: explicit activation prohibitions must not appear in
    ``package_runtime_activation_register_v1.yaml``.
    """
    root = repo_root or _repo_root()
    try:
        prohibitions = collect_explicit_activation_prohibitions(
            repo_root=root,
            why_register=why_register,
            medical_registers=medical_registers,
        )
        if activation_register is None:
            activation_register = _load_yaml_mapping(activation_register_path(root))
        activated = _activated_frames_from_register(activation_register)
        declared = activation_register.get("activated_frame_count")
        if isinstance(declared, int) and declared != len(activated):
            return [
                f"activated_frame_count {declared} does not match {len(activated)} activated frames"
            ]
        return find_runtime_activation_violations(
            activated_frames=activated,
            prohibitions=prohibitions,
        )
    except (FileNotFoundError, ValueError, yaml.YAMLError) as exc:
        return [f"runtime medical authority integrity fail-closed: {exc}"]
