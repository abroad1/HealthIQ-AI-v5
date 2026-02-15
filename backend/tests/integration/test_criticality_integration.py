"""
Integration tests for biomarker criticality (Sprint 3).

- Analysis with limited biomarkers (missing HbA1c) -> meta has missing_markers, downgrades, metabolic confidence < 100
- Analysis with full metabolic required set -> confidence higher, metabolic missing empty
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app


class TestCriticalityIntegration:
    """Integration tests for criticality in analysis result."""

    def test_analysis_missing_hba1c_returns_meta_with_downgrades(self):
        """Start analysis with glucose only (missing HbA1c); meta includes missing markers + downgrades."""
        client = TestClient(app)
        payload = {
            "biomarkers": {
                "glucose": {
                    "value": 95.0,
                    "unit": "mg/dL",
                    "reference_range": {"min": 70, "max": 100, "unit": "mg/dL", "source": "lab"},
                },
            },
            "user": {"user_id": "test", "age": 35, "gender": "male"},
        }
        resp = client.post("/api/analysis/start", json=payload)
        assert resp.status_code == 200
        analysis_id = resp.json().get("analysis_id")
        assert analysis_id

        result_resp = client.get(f"/api/analysis/result?analysis_id={analysis_id}")
        assert result_resp.status_code == 200
        result = result_resp.json()
        meta = result.get("meta", {})
        assert "missing_markers" in meta
        assert "confidence_downgrades" in meta
        assert "system_confidence" in meta
        assert "overall_confidence" in meta
        assert "criticality_version" in meta

        # Metabolic missing hba1c (required)
        assert "metabolic" in meta.get("missing_markers", {})
        metabolic_missing = meta["missing_markers"]["metabolic"]
        assert "hba1c" in metabolic_missing

        # Metabolic system confidence < 100
        assert meta["system_confidence"].get("metabolic", 100) < 100

        # Downgrades include hba1c
        hba1c_downgrades = [d for d in meta["confidence_downgrades"] if d.get("biomarker") == "hba1c"]
        assert len(hba1c_downgrades) >= 1

    def test_analysis_full_metabolic_confidence_higher(self):
        """Start analysis with full metabolic required set; metabolic missing empty, higher confidence."""
        client = TestClient(app)
        payload = {
            "biomarkers": {
                "glucose": {"value": 95.0, "unit": "mg/dL", "reference_range": {"min": 70, "max": 100, "unit": "mg/dL", "source": "lab"}},
                "hba1c": {"value": 5.2, "unit": "%", "reference_range": {"min": 4.0, "max": 5.6, "unit": "%", "source": "lab"}},
                "triglycerides": {"value": 120, "unit": "mg/dL", "reference_range": {"min": 0, "max": 150, "unit": "mg/dL", "source": "lab"}},
                "hdl_cholesterol": {"value": 55, "unit": "mg/dL", "reference_range": {"min": 40, "max": 60, "unit": "mg/dL", "source": "lab"}},
            },
            "user": {"user_id": "test", "age": 35, "gender": "male"},
        }
        resp = client.post("/api/analysis/start", json=payload)
        assert resp.status_code == 200
        analysis_id = resp.json().get("analysis_id")

        result_resp = client.get(f"/api/analysis/result?analysis_id={analysis_id}")
        assert result_resp.status_code == 200
        result = result_resp.json()
        meta = result.get("meta", {})

        # Metabolic has required (glucose, hba1c) + important (trig, hdl)
        metabolic_missing = meta.get("missing_markers", {}).get("metabolic", [])
        assert "glucose" not in metabolic_missing
        assert "hba1c" not in metabolic_missing

        # Metabolic confidence should be high (only insulin optional possibly missing)
        metabolic_conf = meta.get("system_confidence", {}).get("metabolic", 0)
        assert metabolic_conf >= 97  # at most 3 for optional insulin
