"""
Unit tests for Unit Registry (Sprint 1 - Unit Registry).

Deterministic conversion to base SI units. No external calls.
"""

import pytest
from core.units.registry import (
    UnitRegistry,
    UnitConversionError,
    convert_value,
    apply_unit_normalisation,
)


class TestConvertValue:
    """Tests for convert_value."""

    def test_glucose_mg_dl_to_mmol_l(self):
        """Glucose: mg/dL -> mmol/L (factor 0.0555)."""
        val, unit = convert_value("glucose", 95.0, "mg/dL")
        assert unit == "mmol/L"
        assert abs(val - (95.0 * 0.0555)) < 0.001
        assert abs(val - 5.2725) < 0.001

    def test_cholesterol_mg_dl_to_mmol_l(self):
        """Total cholesterol: mg/dL -> mmol/L (factor 0.0259)."""
        val, unit = convert_value("total_cholesterol", 200.0, "mg/dL")
        assert unit == "mmol/L"
        assert abs(val - (200.0 * 0.0259)) < 0.001
        assert abs(val - 5.18) < 0.001

    def test_hba1c_percent_to_mmol_mol(self):
        """HbA1c: % -> mmol/mol (factor 10.929)."""
        val, unit = convert_value("hba1c", 5.5, "%")
        assert unit == "mmol/mol"
        assert abs(val - (5.5 * 10.929)) < 0.01
        assert abs(val - 60.11) < 0.1

    def test_identity_when_already_base_unit(self):
        """Value already in base unit passes through."""
        val, unit = convert_value("glucose", 5.27, "mmol/L")
        assert unit == "mmol/L"
        assert val == 5.27

    def test_identity_for_biomarkers_without_conversion(self):
        """Biomarkers without conversion path use SSOT unit as base."""
        val, unit = convert_value("creatinine", 1.0, "mg/dL")
        assert unit == "mg/dL"
        assert val == 1.0

    def test_reject_unknown_unit_no_conversion_path(self):
        """Reject when from_unit has no conversion to base."""
        with pytest.raises(UnitConversionError) as exc:
            convert_value("glucose", 5.0, "g/L")
        assert "glucose" in str(exc.value) or exc.value.biomarker_id == "glucose"
        assert exc.value.from_unit == "g/L"
        assert exc.value.expected_base_unit == "mmol/L"

    def test_reject_unknown_biomarker(self):
        """Reject unknown biomarker (not in SSOT)."""
        with pytest.raises(UnitConversionError) as exc:
            convert_value("unknown_biomarker_xyz", 1.0, "mg/dL")
        assert "unknown_biomarker_xyz" in str(exc.value)

    def test_missing_unit_rejects_explicit_conversion(self):
        """convert_value requires explicit unit; no silent SSOT fallback."""
        with pytest.raises(UnitConversionError) as exc:
            convert_value("glucose", 95.0, "")
        assert "glucose" in str(exc.value)
        assert "Missing unit" in str(exc.value) or exc.value.from_unit == ""

    def test_missing_unit_unknown_biomarker_rejects(self):
        """Missing unit for unknown biomarker rejects."""
        with pytest.raises(UnitConversionError):
            convert_value("nonexistent_marker", 1.0, "")


class TestApplyUnitNormalisation:
    """Tests for apply_unit_normalisation on full biomarker dict."""

    def test_converts_value_and_reference_range(self):
        """Both value and reference_range min/max converted."""
        normalized = {
            "glucose": {
                "value": 95.0,
                "unit": "mg/dL",
                "reference_range": {"min": 70.0, "max": 100.0, "unit": "mg/dL", "source": "lab"},
            },
        }
        result = apply_unit_normalisation(normalized)
        g = result["glucose"]
        assert g["unit"] == "mmol/L"
        assert abs(g["value"] - 5.2725) < 0.001
        assert g["reference_range"]["unit"] == "mmol/L"
        assert abs(g["reference_range"]["min"] - (70 * 0.0555)) < 0.001
        assert abs(g["reference_range"]["max"] - (100 * 0.0555)) < 0.001
        assert g["original_unit"] == "mg/dL"
        assert g["unit_normalised"] is True

    def test_unmapped_rejected_by_default(self):
        """unmapped_ keys rejected by default (production safety)."""
        normalized = {"unmapped_foo": {"value": 42, "unit": "U/L"}}
        with pytest.raises(UnitConversionError) as exc:
            apply_unit_normalisation(normalized)
        assert "unmapped_foo" in str(exc.value) or exc.value.biomarker_id == "unmapped_foo"
        assert "UNIT_ALLOW_UNMAPPED" in str(exc.value)

    def test_unmapped_allowed_when_flag_true(self):
        """unmapped_ passthrough only when allow_unmapped=True."""
        normalized = {"unmapped_foo": {"value": 42, "unit": "U/L"}}
        result = apply_unit_normalisation(normalized, allow_unmapped=True)
        assert result["unmapped_foo"] == {"value": 42, "unit": "U/L"}

    def test_reject_unsupported_conversion(self):
        """Reject when conversion path does not exist."""
        normalized = {"glucose": {"value": 5.0, "unit": "g/L", "reference_range": None}}
        with pytest.raises(UnitConversionError):
            apply_unit_normalisation(normalized)

    def test_missing_unit_adopts_ref_unit(self):
        """Rule (a): missing unit + ref range unit present -> adopt ref unit."""
        normalized = {
            "glucose": {
                "value": 95.0,
                "unit": "",
                "reference_range": {"min": 70, "max": 100, "unit": "mg/dL", "source": "lab"},
            },
        }
        result = apply_unit_normalisation(normalized)
        g = result["glucose"]
        assert g["unit"] == "mmol/L"
        assert abs(g["value"] - 5.2725) < 0.001
        assert g["unit_source"] == "reference_range"
        assert g["confidence_downgrade_unit_assumed"] is False

    def test_missing_unit_ssot_assumed_with_audit(self):
        """Rule (b): missing unit + SSOT exists + ref bounds -> allow with audit flags."""
        normalized = {
            "glucose": {
                "value": 95.0,
                "unit": "",
                "reference_range": {"min": 70, "max": 100, "source": "lab"},
            },
        }
        result = apply_unit_normalisation(normalized)
        g = result["glucose"]
        assert g["unit"] == "mmol/L"
        assert abs(g["value"] - 5.2725) < 0.001
        assert g["unit_source"] == "ssot_assumed"
        assert g["confidence_downgrade_unit_assumed"] is True
        assert g["reference_unit_assumed"] is True

    def test_missing_unit_reject_no_ssot_no_ref(self):
        """Rule (c): missing unit + no ref unit + no ref bounds -> reject."""
        normalized = {"glucose": {"value": 95.0, "unit": "", "reference_range": None}}
        with pytest.raises(UnitConversionError) as exc:
            apply_unit_normalisation(normalized)
        assert "glucose" in str(exc.value)

    def test_missing_unit_reject_unknown_biomarker_no_unit(self):
        """Rule (c): unknown biomarker with no unit rejects."""
        normalized = {"unknown_xyz": {"value": 1.0, "unit": "", "reference_range": None}}
        with pytest.raises(UnitConversionError):
            apply_unit_normalisation(normalized)

    def test_ref_range_unit_mismatch_rejects(self):
        """Ref range unit not convertible to base rejects."""
        normalized = {
            "glucose": {
                "value": 5.0,
                "unit": "mmol/L",
                "reference_range": {"min": 3, "max": 7, "unit": "g/L", "source": "lab"},
            },
        }
        with pytest.raises(UnitConversionError) as exc:
            apply_unit_normalisation(normalized)
        assert "glucose" in str(exc.value)

    def test_ref_range_unit_missing_assumes_input_unit(self):
        """Ref range missing unit: assume input unit, set reference_unit_assumed."""
        normalized = {
            "glucose": {
                "value": 95.0,
                "unit": "mg/dL",
                "reference_range": {"min": 70, "max": 100, "source": "lab"},
            },
        }
        result = apply_unit_normalisation(normalized)
        g = result["glucose"]
        assert g["reference_unit_assumed"] is True
        assert g["reference_range"]["unit"] == "mmol/L"
        assert abs(g["reference_range"]["min"] - (70 * 0.0555)) < 0.001

    def test_scoring_unchanged_when_already_base_units(self):
        """Input in base units: output identical values."""
        normalized = {
            "glucose": {"value": 5.27, "unit": "mmol/L", "reference_range": None},
            "creatinine": {"value": 1.0, "unit": "mg/dL", "reference_range": None},
        }
        result = apply_unit_normalisation(normalized)
        assert result["glucose"]["value"] == 5.27
        assert result["glucose"]["unit"] == "mmol/L"
        assert result["glucose"]["unit_normalised"] is False
        assert result["creatinine"]["value"] == 1.0
        assert result["creatinine"]["unit"] == "mg/dL"


class TestAnalysisRouteUnitValidation:
    """Verify analysis route returns 400 on unit conversion failure."""

    def test_analysis_start_rejects_unknown_unit(self):
        """POST /api/analysis/start returns 400 when unit has no conversion path."""
        from fastapi.testclient import TestClient
        from app.main import app

        client = TestClient(app)
        payload = {
            "biomarkers": {
                "glucose": {"value": 5.0, "unit": "g/L", "reference_range": {"min": 3, "max": 7, "unit": "g/L", "source": "lab"}},
            },
            "user": {"user_id": "test", "age": 35, "gender": "male"},
        }
        response = client.post("/api/analysis/start", json=payload)
        assert response.status_code == 400
        detail = response.json().get("detail", "") if response.status_code == 400 else ""
        assert "Unit conversion failed" in detail or "glucose" in detail

    def test_analysis_start_rejects_unmapped_by_default(self):
        """POST /api/analysis/start returns 400 when unmapped_ biomarkers present (production default)."""
        from fastapi.testclient import TestClient
        from app.main import app

        client = TestClient(app)
        payload = {
            "biomarkers": {
                "glucose": {"value": 95.0, "unit": "mg/dL"},
                "unmapped_foo": {"value": 42, "unit": "U/L"},
            },
            "user": {"user_id": "test", "age": 35, "gender": "male"},
        }
        response = client.post("/api/analysis/start", json=payload)
        assert response.status_code == 400
        detail = response.json().get("detail", "")
        assert "Unit conversion failed" in detail or "unmapped" in detail.lower()

    @pytest.mark.integration
    def test_analysis_start_accepts_valid_mg_dl_converts(self):
        """POST /api/analysis/start accepts mg/dL glucose and completes (converts to base units internally)."""
        from fastapi.testclient import TestClient
        from app.main import app

        client = TestClient(app)
        payload = {
            "biomarkers": {
                "glucose": {"value": 95.0, "unit": "mg/dL", "reference_range": {"min": 70, "max": 100, "unit": "mg/dL", "source": "lab"}},
                "hdl_cholesterol": {"value": 50.0, "unit": "mg/dL", "reference_range": {"min": 40, "max": 60, "unit": "mg/dL", "source": "lab"}},
            },
            "user": {"user_id": "test", "age": 35, "gender": "male"},
        }
        response = client.post("/api/analysis/start", json=payload)
        assert response.status_code == 200
        result = response.json()
        assert result.get("status") == "completed"


class TestUnitRegistryDirect:
    """Direct UnitRegistry tests."""

    def test_get_base_unit_glucose(self):
        reg = UnitRegistry()
        assert reg.get_base_unit("glucose") == "mmol/L"

    def test_get_base_unit_total_cholesterol(self):
        reg = UnitRegistry()
        assert reg.get_base_unit("total_cholesterol") == "mmol/L"

    def test_get_base_unit_hba1c(self):
        reg = UnitRegistry()
        assert reg.get_base_unit("hba1c") == "mmol/mol"

    def test_get_base_unit_creatinine(self):
        reg = UnitRegistry()
        assert reg.get_base_unit("creatinine") == "mg/dL"
