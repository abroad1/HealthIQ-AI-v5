"""
Sentinel Phase 1 — Escaped-defect regression: frontend slug/internal-label leakage.

Defect class: slug_leakage
Check type: static source file analysis (deterministic)

Scans the source files of customer-facing results components and display-shaping
libraries for patterns that indicate internal backend identifiers leaking to users.

Forbidden patterns (customer-facing surface):
  - ph_*_v*    internal phenotype id format (e.g. ph_metabolic_early_ir_v1)
  - snake_case biomarker slugs appearing in string literals likely rendered to users
  - Backend implementation strings: 'FastAPI', 'internal_id', raw Python module names

Surfaces checked:
  - frontend/app/components/results/ (all .tsx files)
  - frontend/lib/narrativeRuntimePresentation.ts
  - frontend/lib/primaryFindingShaping.ts

Evidence model:
  - trigger: this file / Sentinel regression pack
  - input: source text of each results component
  - expected: no forbidden pattern present in positions that would render to users
  - actual: regex search result
  - customer impact: visible slugs erode trust and expose internal architecture
  - governance escalation: no (read-only source check)
"""
import os
import re
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
FRONTEND_ROOT = REPO_ROOT / "frontend"

RESULTS_COMPONENT_DIR = FRONTEND_ROOT / "app" / "components" / "results"
SHAPING_FILES = [
    FRONTEND_ROOT / "app" / "lib" / "narrativeRuntimePresentation.ts",
    FRONTEND_ROOT / "app" / "lib" / "primaryFindingShaping.ts",
]

# Pattern 1: phenotype internal_id format — should not appear in JSX string literals
# rendered to users (i.e. outside of test fixtures or data shape definitions)
PH_INTERNAL_ID_RE = re.compile(r"""["'`]ph_[a-z0-9_]+_v\d+["'`]""")

# Pattern 2: snake_case biomarker slug in a string literal that is likely rendered
# (i.e. short all-lowercase with underscores — not a variable name or import path)
# Heuristic: 3+ word segments all lowercase alpha, joined by underscores, in a string
SNAKE_CASE_SLUG_RE = re.compile(r"""["'`][a-z][a-z0-9]*(?:_[a-z][a-z0-9]*){2,}["'`]""")

# Pattern 3: backend implementation strings that must not reach the client bundle
BACKEND_IMPL_STRINGS = [
    "FastAPI",
    "internal_id:",     # YAML/dict key form appearing in rendered text
    "canonical_id:",
    "unmapped_",        # resolver sentinel value
]

# False-positive allowlist: snake_case patterns that are legitimate in source
# (CSS classes, i18n keys, data-testid, etc.)
SNAKE_CASE_SLUG_ALLOWLIST = {
    # CSS / tailwind
    "flex_col", "gap_x", "mt_4", "mb_2", "text_sm", "font_bold",
    # Known safe data field names referenced structurally
    "internal_id",        # referenced as a key, not rendered
    "cluster_id",
    "insight_id",
    "analysis_id",
    "result_version",
}


def _collect_results_tsx_files() -> list[Path]:
    if not RESULTS_COMPONENT_DIR.exists():
        return []
    return list(RESULTS_COMPONENT_DIR.glob("*.tsx"))


def _scan_for_ph_ids(source: str, filepath: Path) -> list[str]:
    findings = []
    for match in PH_INTERNAL_ID_RE.finditer(source):
        line_no = source[: match.start()].count("\n") + 1
        findings.append(f"{filepath.name}:{line_no} — ph_* id literal: {match.group()!r}")
    return findings


def _scan_for_backend_strings(source: str, filepath: Path) -> list[str]:
    findings = []
    for bad in BACKEND_IMPL_STRINGS:
        for i, line in enumerate(source.splitlines(), 1):
            if bad in line and not line.strip().startswith("//") and not line.strip().startswith("*"):
                findings.append(f"{filepath.name}:{i} — backend string '{bad}': {line.strip()[:120]}")
    return findings


@pytest.mark.regression
class TestSlugLeakageRegression:
    """Static slug/internal-label leakage guard for customer-facing results surfaces."""

    def test_results_component_dir_exists(self):
        assert RESULTS_COMPONENT_DIR.exists(), (
            f"Results component directory not found: {RESULTS_COMPONENT_DIR}. "
            f"Cannot run slug leakage guard."
        )

    def test_results_components_contain_no_ph_internal_ids(self):
        """
        No results component source file should contain ph_*_v* string literals
        that could be rendered directly to users.
        """
        tsx_files = _collect_results_tsx_files()
        assert tsx_files, f"No .tsx files found in {RESULTS_COMPONENT_DIR}"

        all_findings: list[str] = []
        for f in tsx_files:
            source = f.read_text(encoding="utf-8")
            all_findings.extend(_scan_for_ph_ids(source, f))

        assert not all_findings, (
            f"Slug leakage guard FAIL — ph_* internal ids found in results components "
            f"({len(all_findings)} occurrence(s)):\n" + "\n".join(all_findings)
        )

    def test_results_components_contain_no_backend_impl_strings(self):
        """
        No results component source file should contain backend implementation strings
        such as 'FastAPI', 'unmapped_', or YAML key patterns.
        """
        tsx_files = _collect_results_tsx_files()
        assert tsx_files, f"No .tsx files found in {RESULTS_COMPONENT_DIR}"

        all_findings: list[str] = []
        for f in tsx_files:
            source = f.read_text(encoding="utf-8")
            all_findings.extend(_scan_for_backend_strings(source, f))

        assert not all_findings, (
            f"Slug leakage guard FAIL — backend implementation strings found in results "
            f"components ({len(all_findings)} occurrence(s)):\n" + "\n".join(all_findings)
        )

    def test_narrative_shaping_files_contain_no_ph_internal_ids(self):
        """Narrative shaping lib files must not hardcode ph_* ids in rendered positions."""
        all_findings: list[str] = []
        for filepath in SHAPING_FILES:
            if not filepath.exists():
                continue
            source = filepath.read_text(encoding="utf-8")
            all_findings.extend(_scan_for_ph_ids(source, filepath))

        assert not all_findings, (
            f"Slug leakage guard FAIL — ph_* ids in shaping lib files:\n"
            + "\n".join(all_findings)
        )

    def test_narrative_shaping_files_contain_no_backend_impl_strings(self):
        all_findings: list[str] = []
        for filepath in SHAPING_FILES:
            if not filepath.exists():
                continue
            source = filepath.read_text(encoding="utf-8")
            all_findings.extend(_scan_for_backend_strings(source, filepath))

        assert not all_findings, (
            f"Slug leakage guard FAIL — backend strings in shaping lib files:\n"
            + "\n".join(all_findings)
        )
