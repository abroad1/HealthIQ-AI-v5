"""
Unit tests for Cluster Engine v2.
"""

import pytest
import json
from pathlib import Path

from core.clustering.cluster_engine_v2 import score_clusters, load_cluster_rules


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
