"""
Sprint 15 - Enforcement: no duplicate compute in insight modules.
"""

from pathlib import Path
import re


MODULES_DIR = Path(__file__).parent.parent.parent / "core" / "insights" / "modules"

# Legacy modules are explicitly quarantined by runtime path gating in InsightSynthesizer.
LEGACY_ALLOWLIST = {
    "detox_filtration.py",
    "inflammation.py",
    "heart_insight.py",
    "metabolic_age.py",
    "fatigue_root_cause.py",
}

FORBIDDEN_PATTERNS = [
    r"\bhoma\b",
    r"tg\s*/\s*hdl",
    r"tc\s*/\s*hdl",
    r"ldl\s*/\s*hdl",
    r"ast\s*/\s*alt",
    r"from\s+core\.analytics\.ratio_registry\s+import",
    r"from\s+core\.scoring\.rules\s+import",
    r"from\s+core\.units\.registry\s+import",
    r"context\.biomarker_panel",
    r"raw_biomarkers",
    r"reference_range",
    r"lab_range",
    r"\['value'\]",
    r"\['unit'\]",
]


def test_no_duplicate_compute_patterns_in_non_legacy_insight_modules():
    modules = [p for p in MODULES_DIR.glob("*.py") if p.name != "__init__.py"]
    violations = []
    for path in modules:
        if path.name in LEGACY_ALLOWLIST:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in FORBIDDEN_PATTERNS:
            if re.search(pattern, text, flags=re.IGNORECASE):
                violations.append(f"{path.name}: {pattern}")
    assert not violations, "Duplicate compute/raw access found in insight modules:\n" + "\n".join(violations)


def test_legacy_allowlist_is_explicit_and_bounded():
    modules = {p.name for p in MODULES_DIR.glob("*.py") if p.name != "__init__.py"}
    assert LEGACY_ALLOWLIST <= modules, "Allowlist contains unknown module(s)"
