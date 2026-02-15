"""
Integration tests for lab origin (Sprint 2).

- POST /api/upload/parse with text containing known lab marker returns lab_origin != unknown
- POST /api/analysis/start with lab_origin persists it and /api/analysis/result returns it
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app


# Lab marker strings (short, realistic)
MEDICHECKS_MARKER = "MediChecks\nYour blood test results"
RANDOX_MARKER = "Randox Health\nLaboratory Report"
NHS_MARKER = "NHS Foundation Trust – Pathology Services"  # Structured marker (no bare NHS)


class TestUploadParseLabOrigin:
    """Upload parse returns lab_origin."""

    def test_parse_with_medichecks_marker_returns_lab_origin(self):
        """POST /api/upload/parse with text containing MediChecks returns lab_origin != unknown."""
        client = TestClient(app)
        # Use deterministic CSV format so we avoid LLM; prepend lab header
        text = f"""{MEDICHECKS_MARKER}

glucose,95,mg/dL
hdl_cholesterol,50,mg/dL
"""
        response = client.post(
            "/api/upload/parse",
            data={"text_content": text},
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("success") is True
        assert "lab_origin" in data
        lo = data["lab_origin"]
        assert lo is not None
        assert lo.get("lab_provider_id") == "medichecks"
        assert lo.get("lab_provider_name") == "MediChecks"
        assert lo.get("detection_method") == "header_regex"
        assert lo.get("detection_confidence") == 0.9

    def test_parse_with_nhs_structured_marker_returns_nhs_generic(self):
        """POST /api/upload/parse with NHS Foundation Trust – Pathology Services returns nhs_generic."""
        client = TestClient(app)
        text = f"""{NHS_MARKER}

glucose,95,mg/dL
hdl_cholesterol,50,mg/dL
"""
        response = client.post(
            "/api/upload/parse",
            data={"text_content": text},
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("success") is True
        lo = data.get("lab_origin", {})
        assert lo.get("lab_provider_id") == "nhs_generic"
        assert lo.get("lab_provider_name") == "NHS"

    def test_parse_with_unknown_marker_returns_unknown(self):
        """POST /api/upload/parse with no known lab marker returns lab_origin unknown."""
        client = TestClient(app)
        text = """Generic Lab Report
glucose,95,mg/dL
"""
        response = client.post(
            "/api/upload/parse",
            data={"text_content": text},
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("lab_origin", {}).get("lab_provider_id") == "unknown"


class TestAnalysisPersistsLabOrigin:
    """Analysis start persists lab_origin and result returns it."""

    def test_analysis_start_with_lab_origin_persists_and_result_returns_it(self):
        """POST /api/analysis/start with lab_origin persists it; GET /api/analysis/result returns it."""
        client = TestClient(app)
        lab_origin_payload = {
            "lab_provider_id": "medichecks",
            "lab_provider_name": "MediChecks",
            "detection_method": "header_regex",
            "detection_confidence": 0.9,
            "raw_evidence": "MediChecks",
        }
        payload = {
            "biomarkers": {
                "glucose": {"value": 95.0, "unit": "mg/dL", "reference_range": {"min": 70, "max": 100, "unit": "mg/dL", "source": "lab"}},
                "hdl_cholesterol": {"value": 50.0, "unit": "mg/dL", "reference_range": {"min": 40, "max": 60, "unit": "mg/dL", "source": "lab"}},
            },
            "user": {"user_id": "test", "age": 35, "gender": "male"},
            "lab_origin": lab_origin_payload,
        }
        start_resp = client.post("/api/analysis/start", json=payload)
        assert start_resp.status_code == 200
        analysis_id = start_resp.json().get("analysis_id")
        assert analysis_id

        result_resp = client.get(f"/api/analysis/result?analysis_id={analysis_id}")
        assert result_resp.status_code == 200
        result = result_resp.json()
        assert "meta" in result
        assert "lab_origin" in result["meta"]
        meta_lo = result["meta"]["lab_origin"]
        assert meta_lo["lab_provider_id"] == "medichecks"
        assert meta_lo["lab_provider_name"] == "MediChecks"

    def test_analysis_start_without_lab_origin_returns_unknown_in_result(self):
        """POST /api/analysis/start without lab_origin stores unknown; result returns it."""
        client = TestClient(app)
        payload = {
            "biomarkers": {
                "glucose": {"value": 95.0, "unit": "mg/dL", "reference_range": {"min": 70, "max": 100, "unit": "mg/dL", "source": "lab"}},
            },
            "user": {"user_id": "test", "age": 35, "gender": "male"},
        }
        start_resp = client.post("/api/analysis/start", json=payload)
        assert start_resp.status_code == 200
        analysis_id = start_resp.json().get("analysis_id")

        result_resp = client.get(f"/api/analysis/result?analysis_id={analysis_id}")
        assert result_resp.status_code == 200
        result = result_resp.json()
        meta_lo = result.get("meta", {}).get("lab_origin", {})
        assert meta_lo.get("lab_provider_id") == "unknown"
        assert meta_lo.get("detection_method") == "unknown"
