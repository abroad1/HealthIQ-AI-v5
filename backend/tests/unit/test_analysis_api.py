"""
Unit tests for analysis API endpoints.
"""

import uuid
from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Fixture analysis_id used when injecting fixture data into _analysis_results
FIXTURE_ANALYSIS_ID = "fixture-0001"


def _fixture_result():
    """Build result dict compatible with build_analysis_result_dto from SAMPLE_ANALYSIS."""
    from tests.fixtures.sample_analysis import SAMPLE_ANALYSIS
    return {
        "analysis_id": SAMPLE_ANALYSIS["analysis_id"],
        "biomarkers": SAMPLE_ANALYSIS["biomarkers"],
        "clusters": [],
        "insights": [],
        "status": "completed",
        "created_at": SAMPLE_ANALYSIS["created_at"],
        "overall_score": SAMPLE_ANALYSIS["overall_score"],
        "risk_assessment": SAMPLE_ANALYSIS.get("risk_assessment", {}),
        "recommendations": SAMPLE_ANALYSIS.get("recommendations", []),
        "result_version": SAMPLE_ANALYSIS.get("result_version", "1.0.0"),
    }


class TestAnalysisAPI:
    """Test analysis API endpoints."""

    def test_get_analysis_result_returns_404_when_missing(self):
        """Missing analysis_id returns 404."""
        analysis_id = str(uuid.uuid4())
        response = client.get(f"/api/analysis/result?analysis_id={analysis_id}")
        assert response.status_code == 404
        assert response.json().get("detail") == "Analysis not found"

    @patch("app.routes.analysis._analysis_results", {})
    def test_get_analysis_result_includes_biomarkers(self):
        """Test that /api/analysis/result includes biomarkers when analysis exists."""
        from app.routes import analysis
        analysis._analysis_results[FIXTURE_ANALYSIS_ID] = _fixture_result()
        response = client.get(f"/api/analysis/result?analysis_id={FIXTURE_ANALYSIS_ID}")

        assert response.status_code == 200
        data = response.json()

        assert "analysis_id" in data
        assert "biomarkers" in data
        assert "clusters" in data
        assert "insights" in data
        assert "status" in data
        assert "created_at" in data

        biomarkers = data["biomarkers"]
        assert isinstance(biomarkers, list)
        assert len(biomarkers) > 0, "Expected non-empty biomarkers from stored result"

        biomarker = biomarkers[0]
        required_fields = [
            "biomarker_name", "value", "unit", "score",
            "status", "interpretation"
        ]
        for field in required_fields:
            assert field in biomarker, f"Missing field: {field}"
        assert isinstance(biomarker["biomarker_name"], str)
        assert isinstance(biomarker["value"], (int, float))
        assert isinstance(biomarker["unit"], str)
        assert isinstance(biomarker["score"], (int, float))
        assert isinstance(biomarker["status"], str)
        assert isinstance(biomarker["interpretation"], str)

    @patch("app.routes.analysis._analysis_results", {})
    def test_get_analysis_result_biomarker_status_values(self):
        """Test that biomarker status values are valid."""
        from app.routes import analysis
        analysis._analysis_results[FIXTURE_ANALYSIS_ID] = _fixture_result()
        response = client.get(f"/api/analysis/result?analysis_id={FIXTURE_ANALYSIS_ID}")
        assert response.status_code == 200

        data = response.json()
        biomarkers = data["biomarkers"]
        valid_statuses = ["optimal", "normal", "elevated", "low", "critical"]

        for biomarker in biomarkers:
            assert biomarker["status"] in valid_statuses, \
                f"Invalid status: {biomarker['status']}"

    @patch("app.routes.analysis._analysis_results", {})
    def test_get_analysis_result_reference_ranges(self):
        """Test that reference ranges are properly structured when present."""
        from app.routes import analysis
        analysis._analysis_results[FIXTURE_ANALYSIS_ID] = _fixture_result()
        response = client.get(f"/api/analysis/result?analysis_id={FIXTURE_ANALYSIS_ID}")
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
        response = client.get("/api/analysis/result")
        assert response.status_code == 422
