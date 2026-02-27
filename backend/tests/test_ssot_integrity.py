"""
SSOT integrity checks for registry cross-references.
"""

from pathlib import Path
from typing import Any

import pytest
import yaml


def _load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _collect_invalid_alias_entries(
    alias_registry: dict[str, Any], valid_canonical_ids: set[str]
) -> list[tuple[str, str]]:
    invalid: list[tuple[str, str]] = []
    for entry_key in sorted(alias_registry.keys()):
        entry = alias_registry.get(entry_key)
        canonical_id = entry.get("canonical_id") if isinstance(entry, dict) else None
        canonical_str = canonical_id if isinstance(canonical_id, str) else "<missing_or_non_string>"
        if canonical_str not in valid_canonical_ids:
            invalid.append((entry_key, canonical_str))
    return invalid


def _format_invalid_entries(invalid: list[tuple[str, str]]) -> str:
    lines = [f"- {entry_key}: canonical_id={canonical_id}" for entry_key, canonical_id in invalid]
    return "\n".join(lines)


def test_biomarker_alias_registry_canonical_ids_exist_in_biomarkers_ssot() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    biomarkers_path = repo_root / "ssot" / "biomarkers.yaml"
    alias_registry_path = repo_root / "ssot" / "biomarker_alias_registry.yaml"

    biomarkers_doc = _load_yaml(biomarkers_path)
    alias_registry_doc = _load_yaml(alias_registry_path)

    biomarkers = biomarkers_doc.get("biomarkers")
    assert isinstance(biomarkers, dict), "biomarkers.yaml must contain top-level 'biomarkers' mapping."
    assert isinstance(alias_registry_doc, dict), "biomarker_alias_registry.yaml must be a top-level mapping."

    valid = {k for k in biomarkers.keys() if isinstance(k, str)}
    invalid = _collect_invalid_alias_entries(alias_registry_doc, valid)

    if invalid:
        pytest.fail(
            "Invalid alias registry canonical_ids (must exist in ssot/biomarkers.yaml):\n"
            f"{_format_invalid_entries(invalid)}"
        )


def test_invalid_alias_entries_report_is_deterministic() -> None:
    valid = {"alpha", "beta"}
    alias_registry = {
        "z_key": {"canonical_id": "zzz"},
        "a_key": {"canonical_id": "aaa"},
        "b_key": {"canonical_id": "beta"},
    }
    invalid = _collect_invalid_alias_entries(alias_registry, valid)
    assert invalid == [("a_key", "aaa"), ("z_key", "zzz")]
    assert _format_invalid_entries(invalid) == (
        "- a_key: canonical_id=aaa\n"
        "- z_key: canonical_id=zzz"
    )
