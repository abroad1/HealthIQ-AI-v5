"""
Governed activation-frame identity resolution (ADR-RT-002).

Derives activation_key = signal_id::source_spec_id from package manifests and
package paths without modifying on-disk package files.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import yaml

_INV_YAML_SUFFIX_RE = re.compile(r"\.yaml$", re.IGNORECASE)
_INV_VERSION_SUFFIX_RE = re.compile(r"_v\d+$")
_PKG_BODY_RE = re.compile(r"^pkg_[^_]+_(.+)$")

ACTIVATION_KEY_SEP = "::"


def build_activation_key(*, signal_id: str, source_spec_id: str) -> str:
    sid = signal_id.strip()
    spec = source_spec_id.strip()
    if not sid or not spec:
        raise ValueError("signal_id and source_spec_id required for activation_key")
    return f"{sid}{ACTIVATION_KEY_SEP}{spec}"


def _load_manifest(package_dir: Path) -> Dict[str, Any]:
    manifest_path = package_dir / "package_manifest.yaml"
    if not manifest_path.is_file():
        return {}
    payload = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
    return payload if isinstance(payload, dict) else {}


def infer_source_spec_id(*, package_id: str, source_document: Optional[str]) -> str:
    """Infer investigation spec frame id from manifest fields (no package mutation)."""
    if source_document:
        normalised = source_document.replace("\\", "/").strip()
        if "/inv_" in normalised and _INV_YAML_SUFFIX_RE.search(normalised):
            stem = Path(normalised).stem
            return _INV_VERSION_SUFFIX_RE.sub("", stem)
    match = _PKG_BODY_RE.match(package_id)
    if match:
        return f"inv_{match.group(1)}"

    return package_id


def resolve_activation_identity(
    *,
    signal_id: str,
    signal_library_path: Path,
) -> Tuple[str, str, str]:
    """
    Return (activation_key, source_spec_id, package_id) for a signal library entry.
    """
    package_dir = signal_library_path.parent
    package_id = package_dir.name
    manifest = _load_manifest(package_dir)

    explicit_spec = manifest.get("source_spec_id")
    source_spec_id = (
        str(explicit_spec).strip()
        if isinstance(explicit_spec, str) and explicit_spec.strip()
        else infer_source_spec_id(
            package_id=package_id,
            source_document=manifest.get("source_document")
            if isinstance(manifest.get("source_document"), str)
            else None,
        )
    )

    activation_key = build_activation_key(signal_id=signal_id, source_spec_id=source_spec_id)
    return activation_key, source_spec_id, package_id
