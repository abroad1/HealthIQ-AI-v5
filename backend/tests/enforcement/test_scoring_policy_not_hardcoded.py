"""
Sprint 13 - Enforcement: scoring policy must be SSOT-driven.
"""

from pathlib import Path


def test_rules_py_has_no_inline_biomarker_policy_literals():
    """Scoring policy literals should live in scoring_policy.yaml, not rules.py."""
    path = Path(__file__).parent.parent.parent / "core" / "scoring" / "rules.py"
    text = path.read_text(encoding="utf-8", errors="ignore")

    forbidden_snippets = [
        "optimal_range=(",
        "normal_range=(",
        "borderline_range=(",
        "high_range=(",
        "very_high_range=(",
        "critical_range=(",
        "_HAS_TO_SCORE_RANGE = {",
        "0.2 <= position <= 0.8",
        "0.1 <= position <= 0.9",
        "0.05 <= position <= 0.95",
        "\"tc_hdl_ratio\": {\"min\": 0.0, \"max\": 5.0}",
        "\"tg_hdl_ratio\": {\"min\": 0.0, \"max\": 4.0}",
        "\"ldl_hdl_ratio\": {\"min\": 0.0, \"max\": 3.5}",
    ]

    violations = [snippet for snippet in forbidden_snippets if snippet in text]
    assert not violations, (
        "Sprint 13: hardcoded scoring policy found in rules.py: "
        + ", ".join(violations)
    )


def test_rules_py_loads_scoring_policy_registry():
    """Rules must resolve scoring policy from registry loader."""
    path = Path(__file__).parent.parent.parent / "core" / "scoring" / "rules.py"
    text = path.read_text(encoding="utf-8", errors="ignore")
    assert "from core.analytics.scoring_policy_registry import load_scoring_policy" in text
    assert "self._policy = load_scoring_policy()" in text
