"""
Test that the scoring subsystem has ZERO SSOT/global-range hooks.

Scoring must never import or call SSOT or CanonicalResolver range lookups.
Scoring may ONLY use lab-provided reference ranges, except for DERIVED ratios
where the lab did not provide bounds (the one permitted exception).
"""

import pytest
from pathlib import Path
from unittest.mock import patch

# Forbidden strings in scoring code - presence of any fails the test
_FORBIDDEN_STRINGS = [
    "CanonicalResolver",
    "get_reference_range",
    "backend.ssot",
    "from backend.ssot",
    "import backend.ssot",
    "ssot_reference",
    "get_ssot",
    "reference_range_provider",
]

# Directories to ignore when scanning
_IGNORE_DIRS = frozenset({
    "venv", ".venv", "site-packages", "node_modules", ".git",
    "__pycache__", "build", "dist", "eggs", ".eggs",
})


def _scoring_dir() -> Path:
    """Path to backend/core/scoring/ (robust across cwd)."""
    this_file = Path(__file__).resolve()
    # tests/test_scoring_no_ssot_hooks.py -> backend/core/scoring
    backend = this_file.parent.parent
    return backend / "core" / "scoring"


def _iter_scoring_py_files() -> list[Path]:
    """All *.py files under backend/core/scoring/, excluding ignore dirs."""
    base = _scoring_dir()
    if not base.exists():
        return []
    files = []
    for p in base.rglob("*.py"):
        parts = p.relative_to(base).parts
        if any(d in _IGNORE_DIRS for d in parts):
            continue
        files.append(p)
    return sorted(files)


class TestStaticImportScan:
    """A. Static import scan - scoring folder must not contain SSOT hooks."""

    def test_no_forbidden_strings_in_scoring(self):
        """Fail if any scoring *.py contains SSOT/global-range accessor strings."""
        scoring_dir = _scoring_dir()
        assert scoring_dir.exists(), f"Scoring dir not found: {scoring_dir}"

        files = _iter_scoring_py_files()
        assert len(files) >= 1, f"No *.py files found under {scoring_dir}"

        violations = []
        for py_file in files:
            try:
                content = py_file.read_text(encoding="utf-8")
            except Exception as e:
                raise AssertionError(f"Cannot read {py_file}: {e}") from e

            rel = py_file.relative_to(scoring_dir)
            for forbidden in _FORBIDDEN_STRINGS:
                if forbidden in content:
                    violations.append(f"{rel}: contains '{forbidden}'")

        assert not violations, (
            "Scoring must not contain SSOT/global-range hooks. Violations:\n  - " + "\n  - ".join(violations)
        )


class TestRuntimeGuard:
    """B. Runtime guard - scoring path must never call SSOT reference-range accessors."""

    def _make_ssot_trap(self):
        """Return a side_effect that raises if SSOT range lookup is invoked."""
        def _trap(*args, **kwargs):
            raise AssertionError("SSOT called from scoring")
        return _trap

    def test_scoring_engine_never_calls_ssot(self):
        """
        Patch CanonicalResolver.get_reference_range (and any SSOT accessor).
        Run scoring on a panel with lab ranges; assert no SSOT call occurs.
        """
        with patch(
            "core.canonical.resolver.CanonicalResolver.get_reference_range",
            side_effect=self._make_ssot_trap(),
        ):
            from core.scoring.engine import ScoringEngine

            biomarkers = {
                "hdl": 50.0,
                "ldl": 90.0,
                "total_cholesterol": 180.0,
                "triglycerides": 120.0,
                "tc_hdl_ratio": 3.6,
            }
            input_reference_ranges = {
                "hdl": {"min": 40.0, "max": 60.0, "unit": "mg/dL", "source": "lab"},
                "ldl": {"min": 0.0, "max": 100.0, "unit": "mg/dL", "source": "lab"},
                "total_cholesterol": {"min": 0.0, "max": 200.0, "unit": "mg/dL", "source": "lab"},
                "triglycerides": {"min": 0.0, "max": 150.0, "unit": "mg/dL", "source": "lab"},
            }

            engine = ScoringEngine()
            result = engine.score_biomarkers(
                biomarkers,
                age=35,
                sex="male",
                input_reference_ranges=input_reference_ranges,
            )

            assert result.overall_score >= 0
            assert "cardiovascular" in result.health_system_scores
