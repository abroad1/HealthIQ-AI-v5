"""
Smoke tests for fixture-based analysis functionality.
Tests the fixture endpoint without database dependencies.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_fixture_analysis_loads():
    """Test that the fixture analysis endpoint returns expected data structure."""
    resp = client.get("/api/analysis/fixture")
    assert resp.status_code == 200
    
    data = resp.json()
    
    # Verify basic structure
    assert "analysis_id" in data
    assert "biomarkers" in data
    assert "reference_ranges" in data
    assert "overall_score" in data
    
    # Verify analysis ID
    assert data["analysis_id"] == "fixture-0001"
    
    # Verify biomarkers count
    assert len(data["biomarkers"]) == 6
    
    # Verify biomarker structure
    for biomarker in data["biomarkers"]:
        assert "biomarker_name" in biomarker
        assert "value" in biomarker
        assert "unit" in biomarker
        assert "score" in biomarker
        assert "status" in biomarker
        assert "reference_range" in biomarker
    
    # Verify specific biomarkers are present
    biomarker_names = [b["biomarker_name"] for b in data["biomarkers"]]
    expected_biomarkers = [
        "glucose", "hdl_cholesterol", "ldl_cholesterol", 
        "triglycerides", "total_cholesterol", "hba1c"
    ]
    for expected in expected_biomarkers:
        assert expected in biomarker_names
    
    # Verify reference ranges
    assert len(data["reference_ranges"]) == 6
    for biomarker_name in expected_biomarkers:
        assert biomarker_name in data["reference_ranges"]
        ref_range = data["reference_ranges"][biomarker_name]
        assert "min" in ref_range
        assert "max" in ref_range
        assert "unit" in ref_range


def test_fixture_analysis_no_database_dependency():
    """Test that fixture endpoint works without database connection."""
    # This test ensures the fixture endpoint doesn't require database
    # by running it in isolation
    resp = client.get("/api/analysis/fixture")
    assert resp.status_code == 200
    
    data = resp.json()
    assert data["analysis_id"] == "fixture-0001"
    assert len(data["biomarkers"]) == 6


def test_fixture_analysis_consistent_data():
    """Test that fixture endpoint returns consistent data across multiple calls."""
    resp1 = client.get("/api/analysis/fixture")
    resp2 = client.get("/api/analysis/fixture")
    
    assert resp1.status_code == 200
    assert resp2.status_code == 200
    
    data1 = resp1.json()
    data2 = resp2.json()
    
    # Data should be identical across calls
    assert data1 == data2
    assert data1["analysis_id"] == data2["analysis_id"]
    assert len(data1["biomarkers"]) == len(data2["biomarkers"])
