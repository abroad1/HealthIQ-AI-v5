"""
Unit tests for analysis API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)


class TestAnalysisAPI:
    """Test analysis API endpoints."""
    
    def test_get_analysis_result_includes_biomarkers(self):
        """Test that /api/analysis/result includes biomarkers field."""
        # Test the endpoint
        response = client.get("/api/analysis/result?analysis_id=123e4567-e89b-12d3-a456-426614174000")
        
        # Verify response
        assert response.status_code == 200
        data = response.json()
        
        # Verify required fields are present
        assert "analysis_id" in data
        assert "biomarkers" in data
        assert "clusters" in data
        assert "insights" in data
        assert "status" in data
        assert "created_at" in data
        
        # Verify biomarkers field structure
        biomarkers = data["biomarkers"]
        assert isinstance(biomarkers, list)
        assert len(biomarkers) > 0  # Should have sample data
        
        # Verify biomarker structure
        if biomarkers:
            biomarker = biomarkers[0]
            required_fields = [
                "biomarker_name", "value", "unit", "score", 
                "status", "interpretation"
            ]
            for field in required_fields:
                assert field in biomarker, f"Missing field: {field}"
            
            # Verify data types
            assert isinstance(biomarker["biomarker_name"], str)
            assert isinstance(biomarker["value"], (int, float))
            assert isinstance(biomarker["unit"], str)
            assert isinstance(biomarker["score"], (int, float))
            assert isinstance(biomarker["status"], str)
            assert isinstance(biomarker["interpretation"], str)
    
    def test_get_analysis_result_biomarker_status_values(self):
        """Test that biomarker status values are valid."""
        response = client.get("/api/analysis/result?analysis_id=123e4567-e89b-12d3-a456-426614174000")
        assert response.status_code == 200
        
        data = response.json()
        biomarkers = data["biomarkers"]
        
        valid_statuses = ["optimal", "normal", "elevated", "low", "critical"]
        
        for biomarker in biomarkers:
            assert biomarker["status"] in valid_statuses, \
                f"Invalid status: {biomarker['status']}"
    
    def test_get_analysis_result_reference_ranges(self):
        """Test that reference ranges are properly structured when present."""
        response = client.get("/api/analysis/result?analysis_id=123e4567-e89b-12d3-a456-426614174000")
        assert response.status_code == 200
        
        data = response.json()
        biomarkers = data["biomarkers"]
        
        for biomarker in biomarkers:
            if "reference_range" in biomarker and biomarker["reference_range"]:
                ref_range = biomarker["reference_range"]
                assert "min" in ref_range
                assert "max" in ref_range
                assert "unit" in ref_range
                assert isinstance(ref_range["min"], (int, float))
                assert isinstance(ref_range["max"], (int, float))
                assert isinstance(ref_range["unit"], str)
                assert ref_range["min"] < ref_range["max"]
    
    def test_get_analysis_result_error_handling(self):
        """Test error handling for invalid analysis IDs."""
        # Test with missing analysis_id
        response = client.get("/api/analysis/result")
        # Should return 422 for missing required parameter
        assert response.status_code == 422
