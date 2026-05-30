"""
ARCH-RT-5D — Package provenance classification scan (read-only).

Classifies all package manifests without modifying clinical content or runtime behaviour.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Tuple

import yaml

from core.knowledge.launch_estate_v1 import _infer_source_spec_id, packages_root

ARCH_RT5D_CLASSIFICATIONS = frozenset(
    {
        "explicit_source_spec_id",
        "source_document_derived",
        "package_manifest_inferred",
        "package_id_inferred",
        "batch_json_blocked_pending_spec_extraction",
        "architecture_doc_source_blocked",
        "legacy_retained_with_justification",
        "deferred_for_regeneration",
        "retire_candidate",
        "provenance_gap",
        "unknown_requires_review",
    }
)

INFERRED_CARD_MARKERS: Tuple[Tuple[str, str], ...] = (
    ("total_cholesterol", "package_manifest_inferred"),
    ("tc_hdl_ratio", "package_manifest_inferred"),
    ("insulin", "package_manifest_inferred"),
    ("ast", "package_manifest_inferred"),
    ("bilirubin", "package_manifest_inferred"),
)

_RETIRE_CANDIDATE_IDS = frozenset({"pkg_example"})


@dataclass(frozen=True)
class PackageProvenanceClassificationRow:
    package_id: str
    package_path: str
    classification: str
    source_document: Optional[str]
    inferred_source_spec_id: Optional[str]
    source_spec_id_on_manifest: Optional[str]
    source_spec_id_source: Optional[str]
    has_activation_key: bool


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def classify_package_manifest_rt5d(
    manifest: Mapping[str, Any],
    *,
    package_id: str,
) -> PackageProvenanceClassificationRow:
    """Classify one package manifest using ARCH-RT-5D taxonomy."""
    source_spec_id = manifest.get("source_spec_id")
    ss = source_spec_id.strip() if isinstance(source_spec_id, str) and source_spec_id.strip() else None
    source_document = manifest.get("source_document")
    sd = source_document.strip() if isinstance(source_document, str) and source_document.strip() else None
    activation_key = manifest.get("activation_key")
    has_activation_key = isinstance(activation_key, str) and bool(activation_key.strip())

    if package_id in _RETIRE_CANDIDATE_IDS:
        classification = "retire_candidate"
    elif package_id == "KBP-0001":
        classification = "legacy_retained_with_justification"
    elif ss:
        spec_source = manifest.get("source_spec_id_source")
        if spec_source == "explicit":
            classification = "explicit_source_spec_id"
        elif spec_source in ("source_document_derived", "package_id_inferred"):
            classification = str(spec_source)
        else:
            classification = "explicit_source_spec_id"
    elif not sd:
        classification = "provenance_gap"
    elif package_id.startswith("pkg_kb52c_") or package_id.startswith("pkg_kb52d_"):
        classification = "batch_json_blocked_pending_spec_extraction"
    elif sd.endswith(".json") or "multi_llm_research" in sd.replace("\\", "/"):
        classification = "batch_json_blocked_pending_spec_extraction"
    elif "HealthIQ_Investigation_Layer" in sd or sd.startswith("docs/architecture/"):
        classification = "architecture_doc_source_blocked"
    elif sd.startswith("knowledge_bus/research/study_") or "/study_" in sd:
        classification = "architecture_doc_source_blocked"
    else:
        inferred = _infer_source_spec_id(sd)
        if inferred and (sd.endswith(".yaml") or sd.endswith(".yml")):
            classification = "source_document_derived"
        else:
            classification = "unknown_requires_review"

    inferred_spec = _infer_source_spec_id(sd) if sd else None
    spec_source: Optional[str] = None
    if ss:
        spec_source = str(manifest.get("source_spec_id_source") or "explicit")
    elif classification == "source_document_derived" and inferred_spec:
        spec_source = "source_document_derived"

    package_path = f"knowledge_bus/packages/{package_id}"
    return PackageProvenanceClassificationRow(
        package_id=package_id,
        package_path=package_path,
        classification=classification,
        source_document=sd,
        inferred_source_spec_id=inferred_spec,
        source_spec_id_on_manifest=ss,
        source_spec_id_source=spec_source,
        has_activation_key=has_activation_key,
    )


def scan_all_package_provenance() -> List[PackageProvenanceClassificationRow]:
    rows: List[PackageProvenanceClassificationRow] = []
    root = packages_root()
    for path in sorted(root.glob("*/package_manifest.yaml")):
        payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        package_id = str(payload.get("package_id") or path.parent.name).strip()
        rel = str(path.parent.relative_to(_repo_root())).replace("\\", "/")
        row = classify_package_manifest_rt5d(payload, package_id=package_id)
        rows.append(
            PackageProvenanceClassificationRow(
                package_id=row.package_id,
                package_path=rel,
                classification=row.classification,
                source_document=row.source_document,
                inferred_source_spec_id=row.inferred_source_spec_id,
                source_spec_id_on_manifest=row.source_spec_id_on_manifest,
                source_spec_id_source=row.source_spec_id_source,
                has_activation_key=row.has_activation_key,
            )
        )
    return rows


def classification_counts(rows: List[PackageProvenanceClassificationRow]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for row in rows:
        counts[row.classification] = counts.get(row.classification, 0) + 1
    return dict(sorted(counts.items()))


def refresh_compile_manifest_hashes(manifest: Dict[str, Any], *, repo: Optional[Path] = None) -> Tuple[Dict[str, Any], List[str]]:
    """Return manifest copy with refreshed sha256 hashes; list gaps for missing files."""
    repo = repo or _repo_root()
    out = yaml.safe_load(yaml.safe_dump(manifest)) or {}
    gaps: List[str] = []
    for idx, spec in enumerate(out.get("source_specs") or []):
        if not isinstance(spec, dict):
            continue
        rel = str(spec.get("source_path", "")).strip()
        path = repo / rel.replace("/", "\\") if "\\" in rel else repo / rel
        if path.is_file():
            spec["source_hash"] = sha256_file(path)
        else:
            gaps.append(f"source_specs[{idx}] missing file: {rel}")
    for idx, item in enumerate(out.get("outputs") or []):
        if not isinstance(item, dict):
            continue
        rel = str(item.get("output_path", "")).strip()
        path = repo / rel
        if path.is_file():
            item["output_hash"] = sha256_file(path)
        else:
            gaps.append(f"outputs[{idx}] missing file: {rel}")
    return out, gaps
