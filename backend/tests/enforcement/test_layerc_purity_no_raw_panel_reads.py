"""
Sprint 7B - Enforcement: Layer C modules must not read raw panel data.

Deterministic source-only scanner (no imports of target modules).
"""

from __future__ import annotations

from pathlib import Path


MODULES_DIR = Path(__file__).parent.parent.parent / "core" / "insights" / "modules"
FORBIDDEN_SOURCE_SNIPPETS = [
    "biomarker_panel.biomarkers",
    'hasattr(v, "value")',
    "input_reference_ranges",
    "filtered_biomarkers",
    "unit_normalisation_meta",
]
FORBIDDEN_IMPORT_SNIPPETS = [
    "core.analytics.criticality",
    "core.analytics.ratio_registry",
    "core.analytics.scoring_policy_registry",
    "core.analytics.primitives",
]


def _module_files() -> list[Path]:
    return sorted(
        [p for p in MODULES_DIR.glob("*.py") if p.name != "__init__.py"],
        key=lambda p: p.as_posix(),
    )


def test_layerc_modules_forbid_raw_panel_source_patterns() -> None:
    violations: list[str] = []
    for path in _module_files():
        source = path.read_text(encoding="utf-8", errors="ignore")
        for snippet in FORBIDDEN_SOURCE_SNIPPETS:
            if snippet in source:
                violations.append(f"{path.as_posix()}: forbidden snippet present -> {snippet}")
    if violations:
        raise AssertionError("LAYERC_RAW_PANEL_PATTERN_VIOLATIONS:\n" + "\n".join(sorted(violations)))


def test_layerc_modules_forbid_scoring_ratio_engine_imports() -> None:
    violations: list[str] = []
    for path in _module_files():
        source = path.read_text(encoding="utf-8", errors="ignore")
        for snippet in FORBIDDEN_IMPORT_SNIPPETS:
            if snippet in source:
                violations.append(f"{path.as_posix()}: forbidden import path present -> {snippet}")
    if violations:
        raise AssertionError("LAYERC_IMPORT_VIOLATIONS:\n" + "\n".join(sorted(violations)))
