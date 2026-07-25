"""
Honest provenance status classification (ADR-RT-IDENTITY-PROV-001 §E).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

PROVENANCE_STATUSES = (
    "EXPLICIT_SPEC",
    "COMPILED_MANIFEST",
    "SOURCE_DOCUMENT_DERIVED",
    "LEGACY_INFERRED",
    "UNRESOLVED",
    "BLOCKED",
)

_REPO_ROOT = Path(__file__).resolve().parents[3]


def classify_package_provenance_status(
    *,
    manifest: Dict[str, Any],
    classification_scan: Optional[str] = None,
    investigation_specs_root: Optional[Path] = None,
) -> str:
    """
    Classify package lineage honesty.

    EXPLICIT_SPEC requires manifest.source_spec_id AND a resolvable investigation-spec YAML.
    """
    scan = str(classification_scan or "").strip()
    if scan in {
        "batch_json_blocked_pending_spec_extraction",
        "architecture_doc_source_blocked",
    }:
        # Still allow EXPLICIT override if a real inv_ file is proven later.
        pass
    if scan == "retire_candidate":
        return "BLOCKED"
    if scan == "provenance_gap":
        return "UNRESOLVED"

    explicit = manifest.get("source_spec_id")
    explicit_id = str(explicit).strip() if isinstance(explicit, str) else ""
    specs_root = investigation_specs_root or (
        _REPO_ROOT / "knowledge_bus" / "research" / "investigation_specs"
    )
    if explicit_id:
        # Accept either bare id or inv_*.yaml stem.
        candidates = [
            specs_root / f"{explicit_id}.yaml",
            specs_root / f"{explicit_id}.yml",
        ]
        # Also search one level of multi_llm_research is NOT accepted as EXPLICIT_SPEC
        # (batch JSON ≠ investigation-spec authority).
        if any(p.is_file() for p in candidates):
            return "EXPLICIT_SPEC"
        # Field present but not backed by inv_ YAML → derived/inferred honesty
        source_document = manifest.get("source_document")
        if isinstance(source_document, str) and source_document.strip():
            return "SOURCE_DOCUMENT_DERIVED"
        return "LEGACY_INFERRED"

    source_document = manifest.get("source_document")
    if isinstance(source_document, str) and source_document.strip():
        normalised = source_document.replace("\\", "/").strip()
        if "/inv_" in normalised and normalised.endswith((".yaml", ".yml")):
            return "SOURCE_DOCUMENT_DERIVED"
        if normalised.endswith(".json"):
            return "BLOCKED" if "batch" in normalised.lower() or "Pass_3" in normalised else "SOURCE_DOCUMENT_DERIVED"
        return "SOURCE_DOCUMENT_DERIVED"

    if scan == "source_document_derived":
        return "SOURCE_DOCUMENT_DERIVED"
    if scan == "batch_json_blocked_pending_spec_extraction":
        return "BLOCKED"

    return "UNRESOLVED"


def is_beta_eligible_explicit_lineage(status: str) -> bool:
    return status in {"EXPLICIT_SPEC", "COMPILED_MANIFEST"}
