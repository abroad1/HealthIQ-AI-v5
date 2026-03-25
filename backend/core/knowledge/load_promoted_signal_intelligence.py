"""
Load optional promoted_signal_intelligence.yaml from a Knowledge Bus package directory.

Returns None when the manifest does not opt in. Deterministic: single YAML document.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_promoted_signal_intelligence_for_package(package_dir: Path) -> dict[str, Any] | None:
    """
    Read package_manifest.yaml; if ``promoted_signal_intelligence`` is set, load that file.

    ``package_dir`` is the directory containing package_manifest.yaml.
    """
    manifest_path = package_dir / "package_manifest.yaml"
    if not manifest_path.is_file():
        return None
    try:
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return None
    if not isinstance(manifest, dict):
        return None
    rel = manifest.get("promoted_signal_intelligence")
    if not isinstance(rel, str) or not rel.strip():
        return None
    target = (package_dir / rel.strip()).resolve()
    if not target.is_file():
        return None
    try:
        doc = yaml.safe_load(target.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return None
    return doc if isinstance(doc, dict) else None
