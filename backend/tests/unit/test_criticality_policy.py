"""
Unit tests for biomarker criticality policy (Sprint 3).

Deterministic: missing required/important/optional, penalties, cap, overall aggregation.
"""

import pytest
from core.analytics.criticality import (
    load_criticality_policy,
    evaluate_criticality,
    CriticalityPolicy,
)


class TestLoadCriticalityPolicy:
    """Tests for load_criticality_policy."""

    def test_loads_version_and_systems(self):
        """Policy loads version and systems."""
        policy = load_criticality_policy()
        assert policy.version == "1.0.0"
        assert "metabolic" in policy.systems
        assert "cardiovascular" in policy.systems
        assert "required" in policy.systems["metabolic"]
        assert "glucose" in policy.systems["metabolic"]["required"]
        assert "hba1c" in policy.systems["metabolic"]["required"]

    def test_loads_penalties(self):
        """Policy loads penalty config."""
        policy = load_criticality_policy()
        assert policy.penalties["required_missing"] == 25
        assert policy.penalties["important_missing"] == 10
        assert policy.penalties["optional_missing"] == 3
        assert policy.penalties["max_penalty_per_system"] == 70


class TestEvaluateCriticality:
    """Tests for evaluate_criticality."""

    def test_missing_required_reduces_system_confidence(self):
        """Missing required biomarker reduces metabolic system confidence by 25."""
        scoring_result = {
            "health_system_scores": {"metabolic": {"overall_score": 80, "biomarker_scores": []}},
        }
        # All metabolic except hba1c (required) - so only hba1c missing
        available = {"glucose", "triglycerides", "hdl_cholesterol", "insulin"}
        out = evaluate_criticality(scoring_result, available)
        assert "metabolic" in out["system_confidence"]
        assert out["system_confidence"]["metabolic"] == 75.0  # 100 - 25 (hba1c required)
        assert "hba1c" in out["missing_markers"].get("metabolic", [])
        downgrades_hba1c = [d for d in out["confidence_downgrades"] if d["biomarker"] == "hba1c"]
        assert len(downgrades_hba1c) == 1
        assert downgrades_hba1c[0]["penalty"] == 25
        assert downgrades_hba1c[0]["tier"] == "required"

    def test_missing_important_vs_optional_penalties(self):
        """Important penalty 10, optional penalty 3."""
        scoring_result = {"health_system_scores": {"metabolic": {}}}
        # glucose, hba1c (required), hdl (important). Missing triglycerides (important), insulin (optional)
        available = {"glucose", "hba1c", "hdl_cholesterol"}
        out = evaluate_criticality(scoring_result, available)
        penalties = {d["biomarker"]: d["penalty"] for d in out["confidence_downgrades"] if d["system"] == "metabolic"}
        assert penalties.get("triglycerides") == 10
        assert penalties.get("insulin") == 3
        # metabolic: 100 - 10 - 3 = 87
        assert out["system_confidence"]["metabolic"] == 87.0

    def test_cap_at_max_penalty_per_system(self):
        """System confidence floored at 100 - max_penalty_per_system."""
        scoring_result = {"health_system_scores": {"cardiovascular": {}}}
        available = set()  # All cardiovascular required missing = 4 * 25 = 100, capped at 70
        out = evaluate_criticality(scoring_result, available)
        assert out["system_confidence"]["cardiovascular"] == 30.0  # 100 - 70

    def test_overall_confidence_aggregation_deterministic(self):
        """Overall confidence is weighted by systems present in scoring."""
        scoring_result = {
            "health_system_scores": {
                "metabolic": {"overall_score": 80},
                "cardiovascular": {"overall_score": 70},
            },
        }
        # Full metabolic, full cardiovascular (present in scoring)
        available = {
            "glucose", "hba1c", "triglycerides", "hdl_cholesterol", "insulin",
            "ldl_cholesterol", "total_cholesterol", "crp",
        }
        out = evaluate_criticality(scoring_result, available)
        # Metabolic and cardiovascular in scoring, both fully covered -> avg 100
        assert out["overall_confidence"] == 100.0
        assert out["missing_markers"].get("metabolic", []) == []
        assert out["missing_markers"].get("cardiovascular", []) == []

    def test_full_metabolic_no_missing(self):
        """Full metabolic required set -> no missing, confidence 100."""
        scoring_result = {"health_system_scores": {"metabolic": {}}}
        available = {"glucose", "hba1c", "triglycerides", "hdl_cholesterol", "insulin"}
        out = evaluate_criticality(scoring_result, available)
        assert out["system_confidence"]["metabolic"] == 100.0
        assert out["missing_markers"].get("metabolic", []) == []
        assert not any(d["system"] == "metabolic" for d in out["confidence_downgrades"])
