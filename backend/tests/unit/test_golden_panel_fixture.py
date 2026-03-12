"""
v5.3 Sprint 6 - Golden panel fixture sanity tests.
"""

import json
from pathlib import Path

from core.canonical.normalize import normalize_biomarkers_with_metadata


def test_golden_panel_fixture_contains_expected_size_and_shape():
    path = Path(__file__).parent.parent / "fixtures" / "golden_panel_160.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    assert isinstance(payload.get("biomarkers"), dict)
    assert len(payload["biomarkers"]) == 63
    normalize_biomarkers_with_metadata(payload["biomarkers"])
    sample_key = sorted(payload["biomarkers"].keys())[0]
    sample = payload["biomarkers"][sample_key]
    assert "value" in sample
    assert "unit" in sample
    assert "reference_range" in sample


def test_normalize_preserves_one_sided_reference_ranges():
    payload = {
        "ldl_cholesterol": {
            "value": 2.75,
            "unit": "mmol/L",
            "reference_range": {"min": None, "max": 2.59, "unit": "mmol/L", "source": "lab"},
        },
        "hdl_cholesterol": {
            "value": 2.22,
            "unit": "mmol/L",
            "reference_range": {"min": 1.55, "max": None, "unit": "mmol/L", "source": "lab"},
        },
    }
    out = normalize_biomarkers_with_metadata(payload)
    ldl = out["ldl_cholesterol"]["reference_range"]
    hdl = out["hdl_cholesterol"]["reference_range"]

    assert isinstance(ldl, dict)
    assert ldl["min"] is None
    assert ldl["max"] == 2.59
    assert ldl["source"] == "lab"

    assert isinstance(hdl, dict)
    assert hdl["min"] == 1.55
    assert hdl["max"] is None
    assert hdl["source"] == "lab"


def test_normalize_preserves_reference_profile_payload():
    payload = {
        "hba1c": {
            "value": 26.0,
            "unit": "mmol/mol",
            "reference_range": {"min": None, "max": 39.0, "unit": "mmol/mol", "source": "lab"},
            "reference_profile": {
                "source": "lab",
                "effective_from": "2024-09-11",
                "note": "Please note new reference range in effect from 11/09/2024",
                "bands": [
                    {"label": "Normal", "min": None, "max": 39.0, "unit": "mmol/mol"},
                    {"label": "Prediabetes", "min": 39.0, "max": 48.0, "unit": "mmol/mol"},
                    {"label": "Diabetic", "min": 48.0, "max": None, "unit": "mmol/mol"},
                ],
            },
        },
    }
    out = normalize_biomarkers_with_metadata(payload)
    prof = out["hba1c"].get("reference_profile")
    assert isinstance(prof, dict)
    assert prof.get("effective_from") == "2024-09-11"
    assert isinstance(prof.get("bands"), list)
    assert prof["bands"][0]["label"] == "Normal"
