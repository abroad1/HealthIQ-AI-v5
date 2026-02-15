"""
Integration tests for Derived Ratio Registry (Sprint 4/5).

- Ratios computed once and persisted in meta["derived_ratios"] for analysis route
- Top-level derived_markers in API result with provenance
- Ratios present in scoring when bounds exist (tc/tg/ldl HDL) produce non-unknown statuses
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app


def _lipid_payload():
    """Payload with lipid biomarkers (unit-normalised by analysis route)."""
    return {
        "biomarkers": {
            "total_cholesterol": {"value": 220.0, "unit": "mg/dL", "reference_range": {"min": 0, "max": 200, "unit": "mg/dL", "source": "lab"}},
            "hdl_cholesterol": {"value": 45.0, "unit": "mg/dL", "reference_range": {"min": 40, "max": 60, "unit": "mg/dL", "source": "lab"}},
            "ldl_cholesterol": {"value": 140.0, "unit": "mg/dL", "reference_range": {"min": 0, "max": 100, "unit": "mg/dL", "source": "lab"}},
            "triglycerides": {"value": 180.0, "unit": "mg/dL", "reference_range": {"min": 0, "max": 150, "unit": "mg/dL", "source": "lab"}},
        },
        "user": {"user_id": "test", "age": 35, "gender": "male"},
    }


class TestRatioRegistryIntegration:
    """Integration tests for derived ratios in analysis result."""

    def test_analysis_route_persists_derived_ratios_in_meta(self):
        """POST /api/analysis/start with lipids; result meta includes derived_ratios and derived_markers."""
        client = TestClient(app)
        payload = _lipid_payload()
        resp = client.post("/api/analysis/start", json=payload)
        assert resp.status_code == 200
        analysis_id = resp.json().get("analysis_id")
        assert analysis_id

        result_resp = client.get(f"/api/analysis/result?analysis_id={analysis_id}")
        assert result_resp.status_code == 200
        result = result_resp.json()

        # Sprint 5: Top-level derived_markers
        derived_markers = result.get("derived_markers")
        assert derived_markers is not None
        assert "registry_version" in derived_markers
        assert "derived" in derived_markers
        dm_ratios = derived_markers["derived"]
        assert "tc_hdl_ratio" in dm_ratios
        assert dm_ratios["tc_hdl_ratio"].get("source") == "computed"
        assert dm_ratios["tc_hdl_ratio"].get("value") == pytest.approx(220.0 / 45.0, rel=0.01)

        meta = result.get("meta", {})
        assert "derived_ratios" in meta
        dr = meta["derived_ratios"]
        assert "ratio_registry_version" in dr
        assert "ratios" in dr

        ratios = dr["ratios"]
        assert "tc_hdl_ratio" in ratios
        assert "tg_hdl_ratio" in ratios
        assert "ldl_hdl_ratio" in ratios
        assert "non_hdl_cholesterol" in ratios

        tc = ratios["tc_hdl_ratio"]
        assert "value" in tc
        assert "unit" in tc
        assert "bounds_applied" in tc
        assert tc["bounds_applied"] is True
        assert tc["value"] == pytest.approx(220.0 / 45.0, rel=0.01)

    def test_ratios_with_bounds_receive_non_unknown_status_in_biomarkers(self):
        """tc_hdl_ratio, tg_hdl_ratio, ldl_hdl_ratio in result biomarkers with status != unknown."""
        client = TestClient(app)
        payload = _lipid_payload()
        resp = client.post("/api/analysis/start", json=payload)
        assert resp.status_code == 200
        analysis_id = resp.json().get("analysis_id")

        result_resp = client.get(f"/api/analysis/result?analysis_id={analysis_id}")
        assert result_resp.status_code == 200
        result = result_resp.json()
        biomarkers = result.get("biomarkers", [])

        biomarker_names = {b["biomarker_name"] for b in biomarkers}
        ratio_names = {"tc_hdl_ratio", "tg_hdl_ratio", "ldl_hdl_ratio"}
        found = biomarker_names & ratio_names
        assert len(found) >= 1, f"Expected at least one lipid ratio in biomarkers, got {biomarker_names}"

        for b in biomarkers:
            if b["biomarker_name"] in ratio_names:
                assert b.get("status") != "unknown", f"Ratio {b['biomarker_name']} should have non-unknown status"

    def test_insight_pipeline_metabolic_category_passes(self):
        """Analysis route with metabolic biomarkers returns valid metabolic insights."""
        client = TestClient(app)
        payload = {
            "biomarkers": {
                "glucose": {"value": 95.0, "unit": "mg/dL", "reference_range": {"min": 70, "max": 100, "unit": "mg/dL", "source": "lab"}},
                "hba1c": {"value": 5.2, "unit": "%", "reference_range": {"min": 4.0, "max": 5.6, "unit": "%", "source": "lab"}},
                "insulin": {"value": 10.0, "unit": "μU/mL", "reference_range": {"min": 2, "max": 25, "unit": "μU/mL", "source": "lab"}},
                "total_cholesterol": {"value": 200.0, "unit": "mg/dL", "reference_range": {"min": 0, "max": 200, "unit": "mg/dL", "source": "lab"}},
                "hdl_cholesterol": {"value": 50.0, "unit": "mg/dL", "reference_range": {"min": 40, "max": 60, "unit": "mg/dL", "source": "lab"}},
                "triglycerides": {"value": 100.0, "unit": "mg/dL", "reference_range": {"min": 0, "max": 150, "unit": "mg/dL", "source": "lab"}},
            },
            "user": {"user_id": "test", "age": 35, "gender": "male"},
        }
        resp = client.post("/api/analysis/start", json=payload)
        assert resp.status_code == 200
        analysis_id = resp.json().get("analysis_id")

        result_resp = client.get(f"/api/analysis/result?analysis_id={analysis_id}")
        assert result_resp.status_code == 200
        result = result_resp.json()

        insights = result.get("insights", [])
        metabolic_insights = [i for i in insights if i.get("category") == "metabolic"]
        assert len(metabolic_insights) >= 1, "Expected at least one metabolic insight"
        for mi in metabolic_insights:
            assert mi.get("id")
            assert mi.get("category") == "metabolic"
            assert mi.get("recommendations") is not None

    def test_lab_supplied_tc_hdl_ratio_wins_source_lab(self):
        """When lab supplies tc_hdl_ratio with value and reference_range, source=lab, value preserved."""
        client = TestClient(app)
        payload = {
            "biomarkers": {
                "total_cholesterol": {"value": 220.0, "unit": "mg/dL", "reference_range": {"min": 0, "max": 200, "unit": "mg/dL", "source": "lab"}},
                "hdl_cholesterol": {"value": 45.0, "unit": "mg/dL", "reference_range": {"min": 40, "max": 60, "unit": "mg/dL", "source": "lab"}},
                "ldl_cholesterol": {"value": 140.0, "unit": "mg/dL", "reference_range": {"min": 0, "max": 100, "unit": "mg/dL", "source": "lab"}},
                "triglycerides": {"value": 180.0, "unit": "mg/dL", "reference_range": {"min": 0, "max": 150, "unit": "mg/dL", "source": "lab"}},
                "tc_hdl_ratio": {"value": 3.2, "unit": "ratio", "reference_range": {"min": 2.0, "max": 5.0, "unit": "ratio", "source": "lab"}},
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
        dr = meta.get("derived_ratios", {})
        tc_entry = dr.get("ratios", {}).get("tc_hdl_ratio")
        assert tc_entry is not None
        assert tc_entry.get("source") == "lab"
        assert tc_entry.get("value") == pytest.approx(3.2, abs=0.01)
        assert tc_entry.get("bounds_applied") is True
        assert tc_entry.get("inputs_used") is None

        biom = next((b for b in result.get("biomarkers", []) if b["biomarker_name"] == "tc_hdl_ratio"), None)
        assert biom is not None
        assert biom["value"] == pytest.approx(3.2, abs=0.01)
        rr = biom.get("reference_range") or {}
        assert rr.get("source") == "lab"
        assert rr.get("min") == 2.0
        assert rr.get("max") == 5.0

    def test_lab_supplied_ratio_value_no_range_gets_static_bounds(self):
        """When lab supplies ratio value but no reference_range, static bounds injected, bounds_applied true."""
        client = TestClient(app)
        payload = {
            "biomarkers": {
                "total_cholesterol": {"value": 200.0, "unit": "mg/dL", "reference_range": {"min": 0, "max": 200, "unit": "mg/dL", "source": "lab"}},
                "hdl_cholesterol": {"value": 50.0, "unit": "mg/dL", "reference_range": {"min": 40, "max": 60, "unit": "mg/dL", "source": "lab"}},
                "tc_hdl_ratio": {"value": 4.1, "unit": "ratio"},
            },
            "user": {"user_id": "test", "age": 35, "gender": "male"},
        }
        resp = client.post("/api/analysis/start", json=payload)
        assert resp.status_code == 200
        analysis_id = resp.json().get("analysis_id")

        result_resp = client.get(f"/api/analysis/result?analysis_id={analysis_id}")
        assert result_resp.status_code == 200
        result = result_resp.json()
        tc_entry = result.get("meta", {}).get("derived_ratios", {}).get("ratios", {}).get("tc_hdl_ratio")
        assert tc_entry is not None
        assert tc_entry.get("source") == "lab"
        assert tc_entry.get("value") == pytest.approx(4.1, abs=0.01)
        assert tc_entry.get("bounds_applied") is True

        biom = next((b for b in result.get("biomarkers", []) if b["biomarker_name"] == "tc_hdl_ratio"), None)
        assert biom is not None
        assert biom["value"] == pytest.approx(4.1, abs=0.01)
        rr = biom.get("reference_range") or {}
        assert rr.get("source") == "ratio_registry"
        assert rr.get("min") == 0.0
        assert rr.get("max") == 5.0
