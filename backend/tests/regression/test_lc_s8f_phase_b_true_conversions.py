"""
LC-S8F — Phase B UK/SI true conversion regression (Ca, corrected Ca, Mg, Free T4, Hb, urate).

Proves runtime dispatch in registry.py (not YAML-only) and lab-derived reference-range coherence.
"""

from __future__ import annotations

import pytest

from core.canonical.normalize import normalize_biomarkers_with_metadata
from core.units.registry import (
    UnitRegistry,
    UnitConversionError,
    _STRICT_CONVERSION_BIOMARKERS,
    apply_unit_normalisation,
    convert_value,
)


@pytest.mark.regression
class TestLC_S8FPhaseBConversionVectors:
    @pytest.mark.parametrize(
      "biomarker_id,raw_value,from_unit,expected,atol",
      [
          ("calcium", 9.4, "mg/dL", 2.35, 0.02),
          ("corrected_calcium", 9.4, "mg/dL", 2.35, 0.02),
          ("magnesium", 2.1, "mg/dL", 0.86, 0.02),
          ("free_t4", 1.2, "ng/dL", 15.45, 0.02),
          ("hemoglobin", 14.6, "g/dL", 146.0, 0.1),
          ("urate", 5.8, "mg/dL", 345.1, 0.5),
      ],
    )
    def test_phase_b_value_conversion(self, biomarker_id, raw_value, from_unit, expected, atol):
        val, unit = convert_value(biomarker_id, raw_value, from_unit)
        reg = UnitRegistry()
        assert unit == reg.get_base_unit(biomarker_id)
        assert val == pytest.approx(expected, abs=atol)

    def test_runtime_dispatch_factors_and_strict_set(self):
        reg = UnitRegistry()
        assert reg._get_conversion_factor("calcium", "mg/dL", "mmol/L") == pytest.approx(0.2495, abs=1e-6)
        assert reg._get_conversion_factor("free_t4", "ng/dL", "pmol/L") == pytest.approx(12.871, abs=1e-6)
        for bid in ("calcium", "corrected_calcium", "magnesium", "free_t4", "hemoglobin", "urate"):
            assert bid in _STRICT_CONVERSION_BIOMARKERS
        with pytest.raises(UnitConversionError):
            convert_value("calcium", 2.0, "g/L")


@pytest.mark.regression
class TestLC_S8FPhaseBUkPassThrough:
    def test_hemoglobin_uk_g_L_unchanged(self):
      out = apply_unit_normalisation(
          {
              "hemoglobin": {
                  "value": 144.0,
                  "unit": "g/L",
                  "reference_range": {
                      "min": 130.0,
                      "max": 175.0,
                      "unit": "g/L",
                      "source": "lab",
                  },
              }
          }
      )
      row = out["hemoglobin"]
      assert row["unit"] == "g/L"
      assert row["value"] == pytest.approx(144.0, abs=0.01)
      ref = row["reference_range"]
      assert ref["unit"] == "g/L"
      assert ref["min"] == pytest.approx(130.0, abs=0.01)
      assert ref["max"] == pytest.approx(175.0, abs=0.01)

    def test_urate_uk_umol_L_unchanged(self):
      out = apply_unit_normalisation(
          {
              "urate": {
                  "value": 440.0,
                  "unit": "µmol/L",
                  "reference_range": {
                      "min": 220.0,
                      "max": 547.0,
                      "unit": "µmol/L",
                      "source": "lab",
                  },
              }
          }
      )
      row = out["urate"]
      assert row["unit"] == "µmol/L"
      assert row["value"] == pytest.approx(440.0, abs=0.1)
      ref = row["reference_range"]
      assert ref["min"] == pytest.approx(220.0, abs=0.1)
      assert ref["max"] == pytest.approx(547.0, abs=0.1)

    def test_free_t4_uk_pmol_L_lab_range_preserved(self):
      out = apply_unit_normalisation(
          {
              "free_t4": {
                  "value": 16.8,
                  "unit": "pmol/L",
                  "reference_range": {
                      "min": 12.0,
                      "max": 22.0,
                      "unit": "pmol/L",
                      "source": "lab",
                  },
              }
          }
      )
      row = out["free_t4"]
      assert row["value"] == pytest.approx(16.8, abs=0.01)
      ref = row["reference_range"]
      assert ref["unit"] == "pmol/L"
      assert ref["min"] == pytest.approx(12.0, abs=0.01)
      assert ref["max"] == pytest.approx(22.0, abs=0.01)

    def test_free_t4_ng_dL_converts_value_and_lab_range(self):
      out = apply_unit_normalisation(
          {
              "free_t4": {
                  "value": 1.2,
                  "unit": "ng/dL",
                  "reference_range": {
                      "min": 0.8,
                      "max": 1.8,
                      "unit": "ng/dL",
                      "source": "lab",
                  },
              }
          }
      )
      row = out["free_t4"]
      assert row["unit"] == "pmol/L"
      assert row["value"] == pytest.approx(15.45, abs=0.05)
      ref = row["reference_range"]
      assert ref["unit"] == "pmol/L"
      assert ref["min"] == pytest.approx(10.3, abs=0.2)
      assert ref["max"] == pytest.approx(23.17, abs=0.2)

    def test_calcium_mg_dL_value_and_range_convert_together(self):
      out = apply_unit_normalisation(
          {
              "calcium": {
                  "value": 9.4,
                  "unit": "mg/dL",
                  "reference_range": {
                      "min": 8.5,
                      "max": 10.5,
                      "unit": "mg/dL",
                      "source": "lab",
                  },
              }
          }
      )
      row = out["calcium"]
      assert row["unit"] == "mmol/L"
      assert row["value"] == pytest.approx(2.35, abs=0.02)
      ref = row["reference_range"]
      assert ref["unit"] == "mmol/L"
      assert ref["min"] == pytest.approx(2.12, abs=0.03)
      assert ref["max"] == pytest.approx(2.62, abs=0.03)


@pytest.mark.regression
class TestLC_S8FAliasBoundaries:
    def test_uric_acid_maps_to_urate_not_urea(self):
      out = normalize_biomarkers_with_metadata(
          {
              "uric_acid": {"value": 440.0, "unit": "µmol/L"},
              "BUN": {"value": 5.0, "unit": "mmol/L"},
          }
      )
      assert "urate" in out
      assert "urea" in out
      assert "uric_acid" not in out

    def test_bun_never_maps_to_urate(self):
      out = normalize_biomarkers_with_metadata({"BUN": {"value": 5.0, "unit": "mmol/L"}})
      assert "urea" in out
      assert "urate" not in out
