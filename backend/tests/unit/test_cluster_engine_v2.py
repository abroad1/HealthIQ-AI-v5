"""
Unit tests for Cluster Engine v2.
"""

import pytest
import json
from pathlib import Path
from types import SimpleNamespace

from core.clustering.cluster_engine_v2 import score_clusters, load_cluster_rules, ClusterEngineV2


@pytest.fixture
def green_metabolic_panel():
    """Load green metabolic panel fixture."""
    panel_path = Path(__file__).parent.parent / "fixtures" / "panels" / "green_metabolic.json"
    with open(panel_path, 'r', encoding='utf-8') as f:
        return json.load(f)


@pytest.fixture
def amber_hepatic_panel():
    """Load amber hepatic panel fixture."""
    panel_path = Path(__file__).parent.parent / "fixtures" / "panels" / "amber_hepatic.json"
    with open(panel_path, 'r', encoding='utf-8') as f:
        return json.load(f)


@pytest.fixture
def red_metabolic_panel():
    """Load red metabolic panel fixture."""
    panel_path = Path(__file__).parent.parent / "fixtures" / "panels" / "red_metabolic.json"
    with open(panel_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def test_happy_path_returns_8_clusters(green_metabolic_panel):
    """Test that score_clusters returns 8 clusters."""
    results = score_clusters(
        green_metabolic_panel["biomarkers"],
        green_metabolic_panel["derived"]
    )
    
    assert len(results) == 8
    
    # Check all cluster IDs are present
    cluster_ids = {r["id"] for r in results}
    expected_ids = {
        "metabolic", "cardiovascular", "hepatic", "renal",
        "inflammatory", "hematological", "hormonal", "nutritional"
    }
    assert cluster_ids == expected_ids
    
    # Check all have required fields
    for result in results:
        assert "id" in result
        assert "score" in result
        assert "band" in result
        assert "drivers" in result
        assert "confidence" in result
        assert "tags" in result
        assert isinstance(result["score"], int)
        assert 0 <= result["score"] <= 100
        assert result["band"] in ["green", "amber", "red"]
        assert 0.0 <= result["confidence"] <= 1.0


def test_hepatic_input_with_high_alt_scores_above_baseline(amber_hepatic_panel):
    """Test that hepatic cluster with high ALT scores above baseline and includes driver tag."""
    results = score_clusters(
        amber_hepatic_panel["biomarkers"],
        amber_hepatic_panel["derived"]
    )
    
    hepatic = next(r for r in results if r["id"] == "hepatic")
    
    # Should score above baseline (50) due to ALT high
    assert hepatic["score"] > 50
    
    # Should be amber or red band
    assert hepatic["band"] in ["amber", "red"]
    
    # Should include ALT in drivers
    assert len(hepatic["drivers"]) > 0
    assert any("alt" in d.lower() for d in hepatic["drivers"])


def test_confidence_behaves_correctly(amber_hepatic_panel):
    """Test that confidence behaves correctly: ALT present for hepatic -> confidence > 0, others ~0."""
    results = score_clusters(
        amber_hepatic_panel["biomarkers"],
        amber_hepatic_panel["derived"]
    )
    
    hepatic = next(r for r in results if r["id"] == "hepatic")
    metabolic = next(r for r in results if r["id"] == "metabolic")
    
    # Hepatic should have confidence > 0 (ALT and AST are present)
    assert hepatic["confidence"] > 0.0
    
    # Metabolic should have low confidence (no metabolic biomarkers in input)
    assert metabolic["confidence"] < 0.5  # Should be low since no glucose/hba1c present


def test_load_cluster_rules():
    """Test that load_cluster_rules loads rules correctly."""
    rules = load_cluster_rules()
    
    assert "rules" in rules
    assert "version" in rules
    assert isinstance(rules["rules"], list)
    assert isinstance(rules["version"], str)


def test_red_metabolic_panel_scores_high(red_metabolic_panel):
    """Test that red metabolic panel produces high scores."""
    results = score_clusters(
        red_metabolic_panel["biomarkers"],
        red_metabolic_panel["derived"]
    )
    
    metabolic = next(r for r in results if r["id"] == "metabolic")
    cardiovascular = next(r for r in results if r["id"] == "cardiovascular")
    
    # Metabolic should score high due to glucose and hba1c high
    assert metabolic["score"] >= 50
    
    # Cardiovascular should score high due to triglycerides high and HDL low
    assert cardiovascular["score"] >= 50
    
    # Should have drivers
    assert len(metabolic["drivers"]) > 0
    assert len(cardiovascular["drivers"]) > 0


def test_cluster_engine_v2_uses_policy_for_min_members(monkeypatch: pytest.MonkeyPatch):
    engine = ClusterEngineV2()
    monkeypatch.setattr(
        engine,
        "_load_cluster_scoring_policy",
        lambda: {
            "min_members_per_cluster": 3,
            "severity_thresholds": {"critical_lt": 30.0, "high_lt": 50.0, "moderate_lt": 70.0, "mild_lt": 85.0},
            "confidence": {"variance_divisor": 2500.0, "size_boost_per_member": 0.05, "max_size_boost": 0.2},
            "overall_confidence": {
                "invalid_cluster_penalty": 0.2,
                "out_of_range_cluster_count_penalty": 0.1,
                "optimal_cluster_count_min": 2,
                "optimal_cluster_count_max": 6,
            },
        },
    )
    monkeypatch.setattr(engine, "_group_biomarkers_by_health_system", lambda _: {"metabolic": ["glucose", "hba1c"]})
    scoring_result = {
        "health_system_scores": {
            "metabolic": {
                "biomarker_scores": [
                    {"biomarker_name": "glucose", "score": 80.0},
                    {"biomarker_name": "hba1c", "score": 82.0},
                ]
            }
        }
    }
    result = engine.cluster_biomarkers(context=SimpleNamespace(), scoring_result=scoring_result)
    assert result.clusters == []


def test_cluster_engine_v2_uses_policy_for_severity_thresholds(monkeypatch: pytest.MonkeyPatch):
    engine = ClusterEngineV2()
    monkeypatch.setattr(
        engine,
        "_load_cluster_scoring_policy",
        lambda: {
            "min_members_per_cluster": 2,
            "severity_thresholds": {"critical_lt": 10.0, "high_lt": 20.0, "moderate_lt": 30.0, "mild_lt": 40.0},
            "confidence": {"variance_divisor": 2500.0, "size_boost_per_member": 0.05, "max_size_boost": 0.2},
            "overall_confidence": {
                "invalid_cluster_penalty": 0.2,
                "out_of_range_cluster_count_penalty": 0.1,
                "optimal_cluster_count_min": 2,
                "optimal_cluster_count_max": 6,
            },
        },
    )
    monkeypatch.setattr(
        engine,
        "_group_biomarkers_by_health_system",
        lambda _: {"metabolic": ["glucose", "hba1c"]},
    )
    scoring_result = {
        "health_system_scores": {
            "metabolic": {
                "biomarker_scores": [
                    {"biomarker_name": "glucose", "score": 35.0},
                    {"biomarker_name": "hba1c", "score": 35.0},
                ]
            }
        }
    }
    result = engine.cluster_biomarkers(context=SimpleNamespace(), scoring_result=scoring_result)
    assert len(result.clusters) == 1
    assert result.clusters[0].severity == "mild"
