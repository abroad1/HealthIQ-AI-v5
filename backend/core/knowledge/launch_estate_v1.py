"""
ARCH-RT-5 — Launch estate index, package provenance scan, and authority tables.

Read-only scans for audit generation; does not modify packages or investigation specs.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Tuple

import yaml

from core.knowledge.compiled_hypothesis_registry_v1 import list_compiled_hypothesis_pilot_signal_ids
from core.knowledge.health_system_card_evidence import (
    PILOT_COMPILED_SUBSYSTEM_IDS,
    get_card_evidence_artefact,
)


@dataclass(frozen=True)
class PackageProvenanceRow:
    package_id: str
    package_path: str
    has_source_document: bool
    has_source_spec_id: bool
    source_document: Optional[str]
    source_spec_id: Optional[str]
    classification: str


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def packages_root() -> Path:
    return _repo_root() / "knowledge_bus" / "packages"


def estate_index_path() -> Path:
    return _repo_root() / "knowledge_bus" / "compiled" / "estate_index_v1.yaml"


def manifests_dir() -> Path:
    return _repo_root() / "knowledge_bus" / "compiled" / "manifests"


def _infer_source_spec_id(source_document: Optional[str]) -> Optional[str]:
    if not source_document:
        return None
    name = Path(source_document).name
    m = re.match(r"^(inv_[a-z0-9_]+?)(?:_v\d+)?\.ya?ml$", name)
    if m:
        return m.group(1)
    return None


def classify_package_manifest(manifest: Mapping[str, Any], package_id: str) -> str:
    source_spec_id = manifest.get("source_spec_id")
    if isinstance(source_spec_id, str) and source_spec_id.strip():
        return "explicit_source_spec_id"
    source_document = manifest.get("source_document")
    if isinstance(source_document, str) and source_document.strip():
        if package_id.startswith("pkg_kb52c_") or package_id.startswith("pkg_kb52d_"):
            return "blocked_pending_spec_extraction"
        inferred = _infer_source_spec_id(source_document)
        if inferred:
            return "source_document_derived"
        return "source_document_unparsed"
    if package_id == "KBP-0001":
        return "legacy_retained_with_justification"
    return "provenance_gap"


def scan_package_provenance() -> List[PackageProvenanceRow]:
    rows: List[PackageProvenanceRow] = []
    root = packages_root()
    for path in sorted(root.glob("*/package_manifest.yaml")):
        payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        package_id = str(payload.get("package_id") or path.parent.name).strip()
        source_document = payload.get("source_document")
        source_spec_id = payload.get("source_spec_id")
        sd = source_document.strip() if isinstance(source_document, str) else None
        ss = source_spec_id.strip() if isinstance(source_spec_id, str) else None
        rows.append(
            PackageProvenanceRow(
                package_id=package_id,
                package_path=str(path.parent.relative_to(_repo_root())).replace("\\", "/"),
                has_source_document=bool(sd),
                has_source_spec_id=bool(ss),
                source_document=sd,
                source_spec_id=ss,
                classification=classify_package_manifest(payload, package_id),
            )
        )
    return rows


def wave1_subsystem_authority_rows() -> List[Dict[str, str]]:
    out: List[Dict[str, str]] = []
    for subsystem_id in sorted(PILOT_COMPILED_SUBSYSTEM_IDS):
        artefact = get_card_evidence_artefact(subsystem_id)
        out.append(
            {
                "domain_id": artefact.domain_id,
                "subsystem_id": subsystem_id,
                "subsystem_label": artefact.subsystem_label,
                "active_authority": "compiled_card_evidence",
                "launch_classification": "launch_included_compiled",
            }
        )
    return out


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_estate_index() -> Dict[str, Any]:
    path = estate_index_path()
    if not path.is_file():
        raise FileNotFoundError(f"estate index missing: {path}")
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(payload, dict):
        raise ValueError("estate index must be a mapping")
    return payload


def resolve_compile_manifest_ref(ref: str) -> Optional[Path]:
    """Resolve compile_manifest_ref to a manifest file under knowledge_bus/compiled/manifests/."""
    ref = ref.strip().replace("\\", "/")
    repo = _repo_root()
    if ref.startswith("knowledge_bus/"):
        full = repo / ref
        if full.is_file():
            return full
    name = Path(ref).name
    if not name.endswith(".yaml"):
        name = f"{name}.yaml"
    direct = manifests_dir() / name
    if direct.is_file():
        return direct
    alt = manifests_dir() / ref
    if alt.is_file():
        return alt
    return None
