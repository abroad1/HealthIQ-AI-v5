"""
Unit tests for analysis API endpoints.
"""

import uuid
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

from tests.auth_headers import ANALYSIS_TEST_AUTH_HEADERS

client = TestClient(app)

AUTH_HEADERS = dict(ANALYSIS_TEST_AUTH_HEADERS)
TEST_USER_ID = ANALYSIS_TEST_AUTH_HEADERS["X-Test-Auth-User-Id"]

# Fixture analysis_id (must be a valid UUID; GET /result validates with UUID())
FIXTURE_ANALYSIS_ID = str(uuid.UUID("00000000-0000-4000-8000-000000000001"))


def _fixture_result():
    """Build result dict compatible with build_analysis_result_dto from SAMPLE_ANALYSIS."""
    from tests.fixtures.sample_analysis import SAMPLE_ANALYSIS
    return {
        "analysis_id": FIXTURE_ANALYSIS_ID,
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

    def test_get_analysis_result_requires_auth(self):
        """GET /result without credentials returns 401."""
        analysis_id = str(uuid.uuid4())
        response = client.get(f"/api/analysis/result?analysis_id={analysis_id}")
        assert response.status_code == 401

    def test_get_analysis_result_returns_404_when_missing(self):
        """Missing analysis for authenticated user returns 404."""
        analysis_id = str(uuid.uuid4())
        response = client.get(
            f"/api/analysis/result?analysis_id={analysis_id}",
            headers=AUTH_HEADERS,
        )
        assert response.status_code == 404
        assert response.json().get("detail") == "Analysis not found"

    @patch("app.routes.analysis._analysis_results", {})
    @patch("app.routes.analysis._analysis_owners", {})
    def test_get_analysis_result_includes_biomarkers(self):
        """Test that /api/analysis/result includes biomarkers when analysis exists."""
        from app.routes import analysis

        analysis._analysis_results[FIXTURE_ANALYSIS_ID] = _fixture_result()
        analysis._analysis_owners[FIXTURE_ANALYSIS_ID] = TEST_USER_ID
        response = client.get(
            f"/api/analysis/result?analysis_id={FIXTURE_ANALYSIS_ID}",
            headers=AUTH_HEADERS,
        )

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
    @patch("app.routes.analysis._analysis_owners", {})
    def test_get_analysis_result_biomarker_status_values(self):
        """Test that biomarker status values are valid."""
        from app.routes import analysis

        analysis._analysis_results[FIXTURE_ANALYSIS_ID] = _fixture_result()
        analysis._analysis_owners[FIXTURE_ANALYSIS_ID] = TEST_USER_ID
        response = client.get(
            f"/api/analysis/result?analysis_id={FIXTURE_ANALYSIS_ID}",
            headers=AUTH_HEADERS,
        )
        assert response.status_code == 200

        data = response.json()
        biomarkers = data["biomarkers"]
        valid_statuses = ["optimal", "normal", "elevated", "low", "critical"]

        for biomarker in biomarkers:
            assert biomarker["status"] in valid_statuses, \
                f"Invalid status: {biomarker['status']}"

    @patch("app.routes.analysis._analysis_results", {})
    @patch("app.routes.analysis._analysis_owners", {})
    def test_get_analysis_result_reference_ranges(self):
        """Test that reference ranges are properly structured when present."""
        from app.routes import analysis

        analysis._analysis_results[FIXTURE_ANALYSIS_ID] = _fixture_result()
        analysis._analysis_owners[FIXTURE_ANALYSIS_ID] = TEST_USER_ID
        response = client.get(
            f"/api/analysis/result?analysis_id={FIXTURE_ANALYSIS_ID}",
            headers=AUTH_HEADERS,
        )
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
        """Missing analysis_id with auth returns 422."""
        response = client.get("/api/analysis/result", headers=AUTH_HEADERS)
        assert response.status_code == 422
