"""
ARCH-CONV-A — named duplicate activation-authority resolution.

When two package candidates resolve to the same activation_key, select one by
governed authority criteria only. Never use path order, package-id order,
filesystem load order, or first/last-loaded wins.

Equal-authority ties fail closed.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Tuple

from core.knowledge.why_authority_v1 import STATE_COMPILED_ACTIVE, authority_state_for

PROVENANCE_RANK: Dict[str, int] = {
    "EXPLICIT_SPEC": 5,
    "COMPILED_MANIFEST": 4,
    "SOURCE_DOCUMENT_DERIVED": 3,
    "LEGACY_INFERRED": 2,
    "UNRESOLVED": 1,
    "BLOCKED": 0,
}

_REPO_ROOT = Path(__file__).resolve().parents[3]
_SPECS_ROOT = _REPO_ROOT / "knowledge_bus" / "research" / "investigation_specs"


class DuplicateAuthorityConflict(ValueError):
    """Raised when duplicate activation authorities cannot be distinguished."""


@dataclass(frozen=True)
class AuthorityCandidate:
    activation_key: str
    source_spec_id: str
    package_id: str
    provenance_status: str
    has_explicit_source_spec_id: bool
    has_validated_canonical_inv_spec: bool
    source_path: str = ""

    def authority_rank(self) -> Tuple[int, int, int, int]:
        """
        Higher tuple wins.

        1. explicit activation_key / source_spec_id declaration
        2. validated canonical investigation_spec source
        3. ratified/promoted COMPILED_ACTIVE authority for this activation_key
        4. higher provenance governance rank
        """
        compiled_active = 1 if authority_state_for(self.activation_key) == STATE_COMPILED_ACTIVE else 0
        return (
            1 if self.has_explicit_source_spec_id else 0,
            1 if self.has_validated_canonical_inv_spec else 0,
            compiled_active,
            PROVENANCE_RANK.get(str(self.provenance_status or "").strip(), -1),
        )


def validated_canonical_inv_spec_exists(source_spec_id: str) -> bool:
    sid = str(source_spec_id or "").strip()
    if not sid:
        return False
    return any(
        (_SPECS_ROOT / name).is_file()
        for name in (f"{sid}.yaml", f"{sid}.yml", f"{sid}_v1.yaml", f"{sid}_v1.yml")
    )


def candidate_from_signal_row(row: Mapping[str, Any], *, manifest: Optional[Mapping[str, Any]] = None) -> AuthorityCandidate:
    man = dict(manifest or {})
    explicit = man.get("source_spec_id")
    has_explicit = isinstance(explicit, str) and bool(explicit.strip())
    if "has_explicit_source_spec_id" in row:
        has_explicit = bool(row.get("has_explicit_source_spec_id"))
    source_spec_id = str(row.get("source_spec_id") or "").strip()
    activation_key = str(row.get("activation_key") or "").strip()
    if "has_validated_canonical_inv_spec" in row:
        has_canonical = bool(row.get("has_validated_canonical_inv_spec"))
    else:
        has_canonical = validated_canonical_inv_spec_exists(source_spec_id)
        if not has_canonical:
            source_document = man.get("source_document")
            if isinstance(source_document, str):
                normalised = source_document.replace("\\", "/").strip()
                if "/inv_" in normalised and normalised.endswith((".yaml", ".yml")):
                    has_canonical = True
    return AuthorityCandidate(
        activation_key=activation_key,
        source_spec_id=source_spec_id,
        package_id=str(row.get("package_id") or "").strip(),
        provenance_status=str(row.get("provenance_status") or "").strip(),
        has_explicit_source_spec_id=has_explicit,
        has_validated_canonical_inv_spec=has_canonical,
        source_path=str(row.get("_source_path") or "").strip(),
    )


def resolve_duplicate_authority(
    left: AuthorityCandidate,
    right: AuthorityCandidate,
) -> AuthorityCandidate:
    """
    Return the higher-authority candidate, or raise DuplicateAuthorityConflict.
    """
    if left.activation_key != right.activation_key:
        raise ValueError(
            "duplicate authority resolution requires identical activation_key; "
            f"got {left.activation_key!r} vs {right.activation_key!r}"
        )
    left_rank = left.authority_rank()
    right_rank = right.authority_rank()
    if left_rank > right_rank:
        return left
    if right_rank > left_rank:
        return right
    raise DuplicateAuthorityConflict(
        "Duplicate activation authority conflict for "
        f"{left.activation_key!r}: equal governed authority ranks "
        f"{left_rank!r} between packages {left.package_id!r} and {right.package_id!r}. "
        "Refusing path/package-id/load-order selection."
    )
