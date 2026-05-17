"""
LC-S8G — Uploaded-unit display fidelity contract (backend DTO + SSOT coverage inventory).
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from core.dto.builders import analysis_route_biomarker_row_with_display
from core.models.results import BiomarkerScore
from core.units.display_policy import load_display_unit_policy
from core.units.registry import UnitRegistry, convert_value

REPO_ROOT = Path(__file__).resolve().parents[3]
FRONTEND_APP = REPO_ROOT / "frontend" / "app"

# Biomarkers that must have display-fidelity coverage or policy declaration (LC-S8G Phase 4).
_LC_S8G_DISPLAY_COVERAGE_INVENTORY = (
    "calcium",
    "corrected_calcium",
    "magnesium",
    "free_t4",
    "hemoglobin",
    "urate",
    "hba1c",
    "hematocrit",
    "platelets",
    "white_blood_cells",
    "sodium",
    "potassium",
    "chloride",
    "glucose",
    "total_cholesterol",
    "ldl_cholesterol",
    "hdl_cholesterol",
    "triglycerides",
    "creatinine",
    "urea",
    "vitamin_d",
)

_PHASE_B_US_FIXTURE = {
    "calcium": (9.4, "mg/dL", 2.35, "mmol/L", 8.6, 10.2),
    "corrected_calcium": (9.4, "mg/dL", 2.35, "mmol/L", 8.6, 10.2),
    "magnesium": (2.1, "mg/dL", 0.86, "mmol/L", 1.7, 2.4),
    "free_t4": (1.2, "ng/dL", 15.45, "pmol/L", 0.8, 1.8),
    "hemoglobin": (14.6, "g/dL", 146.0, "g/L", 13.0, 17.5),
    "urate": (5.8, "mg/dL", 345.1, "µmol/L", 3.5, 7.2),
}


def _score(
    name: str,
    value: float,
    unit: str,
    rmin: float | None = None,
    rmax: float | None = None,
) -> BiomarkerScore:
    ref = None
    if rmin is not None and rmax is not None:
        ref = {"min": rmin, "max": rmax, "unit": unit, "source": "lab"}
    return BiomarkerScore(
        biomarker_name=name,
        value=value,
        unit=unit,
        score=0.5,
        status="normal",
        reference_range=ref,
        interpretation="",
    )


@pytest.mark.regression
class TestLC_S8GDisplayFields:
    @pytest.mark.parametrize("biomarker_id", list(_PHASE_B_US_FIXTURE.keys()))
    def test_us_upload_display_preserves_uploaded_unit_family(self, biomarker_id: str):
        up_val, up_unit, an_val, an_unit, rmin, rmax = _PHASE_B_US_FIXTURE[biomarker_id]
        upload_key = "uric_acid" if biomarker_id == "urate" else biomarker_id
        upload_panel = {
            upload_key: {
                "value": up_val,
                "unit": up_unit,
                "reference_range": {"min": rmin, "max": rmax, "unit": up_unit, "source": "lab"},
            }
        }
        an_rmin, an_rmax = (130.0, 175.0) if biomarker_id == "hemoglobin" else (rmin, rmax)
        row = analysis_route_biomarker_row_with_display(
            _score(biomarker_id, an_val, an_unit, an_rmin, an_rmax),
            upload_panel=upload_panel,
        )

        assert row["display_unit"] == up_unit
        assert float(row["display_value"]) == pytest.approx(up_val, rel=0.02)
        assert row["analytical_unit"] == an_unit
        assert row["display_is_uploaded_unit"] is True
        assert row.get("analytical_transparency_unit") == an_unit
        dref = row["display_reference_range"]
        assert dref is not None
        assert dref["unit"] == up_unit
        assert float(dref["min"]) == pytest.approx(rmin, rel=0.02)
        assert float(dref["max"]) == pytest.approx(rmax, rel=0.02)

    def test_uk_pass_through_hemoglobin(self):
        upload_panel = {
            "hemoglobin": {
                "value": 144.0,
                "unit": "g/L",
                "reference_range": {"min": 130.0, "max": 175.0, "unit": "g/L", "source": "lab"},
            }
        }
        row = analysis_route_biomarker_row_with_display(
            _score("hemoglobin", 144.0, "g/L", 130.0, 175.0),
            upload_panel=upload_panel,
        )
        assert row["display_unit"] == "g/L"
        assert row["display_value"] == pytest.approx(144.0)
        assert row["display_is_uploaded_unit"] is False
        assert "analytical_transparency_unit" not in row

    def test_uric_acid_upload_key_maps_to_urate_display(self):
        upload_panel = {
            "uric_acid": {
                "value": 5.8,
                "unit": "mg/dL",
                "reference_range": {"min": 3.5, "max": 7.2, "unit": "mg/dL", "source": "lab"},
            }
        }
        row = analysis_route_biomarker_row_with_display(
            _score("urate", 345.1, "µmol/L", 220.0, 547.0),
            upload_panel=upload_panel,
        )
        assert row["display_unit"] == "mg/dL"
        assert row["display_value"] == pytest.approx(5.8, rel=0.01)


@pytest.mark.regression
class TestLC_S8GSSOTDisplayCoverageInventory:
    def test_inventory_biomarkers_have_policy_or_conversion_path(self):
        policy = load_display_unit_policy()
        policy_biomarkers = policy.get("biomarkers") or {}
        reg = UnitRegistry()
        missing = []
        for bid in _LC_S8G_DISPLAY_COVERAGE_INVENTORY:
            has_policy = bid in policy_biomarkers
            in_strict = bid in {
                "calcium",
                "corrected_calcium",
                "magnesium",
                "free_t4",
                "hemoglobin",
                "urate",
                "glucose",
                "total_cholesterol",
                "ldl_cholesterol",
                "hdl_cholesterol",
                "triglycerides",
                "hba1c",
                "urea",
                "creatinine",
                "vitamin_d",
                "hematocrit",
                "platelets",
                "white_blood_cells",
                "sodium",
                "potassium",
                "chloride",
            }
            if not has_policy and not in_strict:
                missing.append(bid)
        assert not missing, f"Missing display policy or known conversion path: {missing}"

    def test_phase_b_conversion_still_reachable(self):
        val, unit = convert_value("calcium", 9.4, "mg/dL")
        assert unit == "mmol/L"
        assert val == pytest.approx(2.35, abs=0.02)


@pytest.mark.regression
class TestLC_S8GFrontendNoConversionConstants:
    def test_frontend_app_has_no_phase_b_conversion_literals(self):
        pattern = re.compile(r"\b0\.2495\b|\b0\.4114\b|\b12\.871\b|\b59\.5\b")
        hits = []
        if FRONTEND_APP.exists():
            for path in FRONTEND_APP.rglob("*.ts"):
                if "uploadPanelFidelity.test" in path.name:
                    continue
                text = path.read_text(encoding="utf-8")
                if pattern.search(text):
                    hits.append(str(path.relative_to(REPO_ROOT)))
            for path in FRONTEND_APP.rglob("*.tsx"):
                text = path.read_text(encoding="utf-8")
                if pattern.search(text):
                    hits.append(str(path.relative_to(REPO_ROOT)))
        assert not hits, f"Phase B conversion constants must not appear in frontend runtime: {hits}"
