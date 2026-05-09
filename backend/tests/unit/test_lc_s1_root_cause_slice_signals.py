"""
LC-S1 launch-core slice regression — governed WHY coverage for AB/VR proving signals.

Authoritative LDL lane runtime ID remains signal_ldl_cholesterol_high (gate-pack shorthand signal_ldl_high).
"""

from __future__ import annotations

from core.analytics.root_cause_compiler_v1 import compile_root_cause_v1


def _finding(rc, sid: str):
    assert rc is not None
    for f in rc.findings:
        if f.signal_id == sid:
            return f
    raise AssertionError(f"missing finding for {sid}")


def test_lc_s1_homocysteine_high_reuses_governed_hcy_asset_without_fallback_insert():
    root = compile_root_cause_v1(
        signal_results=[
            {
                "signal_id": "signal_homocysteine_high",
                "primary_metric": "homocysteine",
                "signal_state": "at_risk",
                "confidence": 0.82,
            }
        ],
        biomarker_context={
            "homocysteine": 18.5,
            "vitamin_b12": {"value": 155.0},
            "mcv": {"value": 94.0},
            "folate": {"value": 8.0},
        },
        input_reference_ranges={
            "homocysteine": {"min": 5.0, "max": 15.0, "unit": "µmol/L", "source": "lab"},
            "vitamin_b12": {"min": 200.0, "max": 900.0, "unit": "pmol/L", "source": "lab"},
            "mcv": {"min": 80.0, "max": 99.0, "unit": "fL", "source": "lab"},
            "folate": {"min": 10.0, "max": 45.0, "unit": "nmol/L", "source": "lab"},
        },
    )
    f = _finding(root, "signal_homocysteine_high")
    assert not any(h.hypothesis_id == "why_engine_fallback_v1" for h in f.hypotheses)
    assert len(f.hypotheses) >= 1


def test_lc_s1_mcv_high_gets_governed_hypotheses():
    root = compile_root_cause_v1(
        signal_results=[
            {
                "signal_id": "signal_mcv_high",
                "primary_metric": "mcv",
                "signal_state": "at_risk",
                "confidence": 0.71,
            }
        ],
        biomarker_context={
            "mcv": {"value": 104.0},
            "vitamin_b12": {"value": 180.0},
        },
        input_reference_ranges={
            "mcv": {"min": 80.0, "max": 99.0, "unit": "fL", "source": "lab"},
            "vitamin_b12": {"min": 200.0, "max": 900.0, "unit": "pmol/L", "source": "lab"},
        },
    )
    f = _finding(root, "signal_mcv_high")
    assert not any(h.hypothesis_id == "why_engine_fallback_v1" for h in f.hypotheses)
    ids = {h.hypothesis_id for h in f.hypotheses}
    assert "mcv_high_anchor_pattern_v1" in ids


def test_lc_s1_apoa1_cardio_risk_gets_governed_hypotheses():
    root = compile_root_cause_v1(
        signal_results=[
            {
                "signal_id": "signal_apoa1_cardio_risk",
                "primary_metric": "apoa1",
                "signal_state": "suboptimal",
                "confidence": 0.79,
            }
        ],
        biomarker_context={
            "apoa1": {"value": 1.0},
            "apob": {"value": 1.2},
            "apob_apoa1_ratio": {"value": 1.25},
        },
        input_reference_ranges={
            "apoa1": {"min": 1.2, "max": 2.0, "unit": "g/L", "source": "lab"},
            "apob": {"min": 0.5, "max": 1.5, "unit": "g/L", "source": "lab"},
            "apob_apoa1_ratio": {"min": 0.5, "max": 1.0, "unit": "ratio", "source": "lab"},
        },
    )
    f = _finding(root, "signal_apoa1_cardio_risk")
    assert not any(h.hypothesis_id == "why_engine_fallback_v1" for h in f.hypotheses)
    assert any(h.hypothesis_id == "apoa1_low_hdl_transport_anchor_v1" for h in f.hypotheses)


def test_lc_s1_hypercortisolism_gets_governed_hypotheses():
    root = compile_root_cause_v1(
        signal_results=[
            {
                "signal_id": "signal_hypercortisolism",
                "primary_metric": "cortisol",
                "signal_state": "suboptimal",
                "confidence": 0.77,
            }
        ],
        biomarker_context={
            "cortisol": {"value": 650.0},
            "hba1c": {"value": 42.0},
        },
        input_reference_ranges={
            "cortisol": {"min": 100.0, "max": 500.0, "unit": "nmol/L", "source": "lab"},
            "hba1c": {"min": 20.0, "max": 42.0, "unit": "mmol/mol", "source": "lab"},
        },
    )
    f = _finding(root, "signal_hypercortisolism")
    assert not any(h.hypothesis_id == "why_engine_fallback_v1" for h in f.hypotheses)
    assert any(h.hypothesis_id == "hypercortisolism_lab_anchor_v1" for h in f.hypotheses)


def test_lc_s1_ldl_lane_remains_canonical_signal_ldl_cholesterol_high():
    root = compile_root_cause_v1(
        signal_results=[
            {
                "signal_id": "signal_ldl_cholesterol_high",
                "primary_metric": "ldl_cholesterol",
                "signal_state": "suboptimal",
                "confidence": 0.74,
            }
        ],
        biomarker_context={
            "ldl_cholesterol": {"value": 4.2},
            "non_hdl_cholesterol": {"value": 5.0},
        },
        input_reference_ranges={
            "ldl_cholesterol": {"min": 1.0, "max": 3.0, "unit": "mmol/L", "source": "lab"},
            "non_hdl_cholesterol": {"min": 1.0, "max": 4.0, "unit": "mmol/L", "source": "lab"},
        },
    )
    f = _finding(root, "signal_ldl_cholesterol_high")
    assert not any(h.hypothesis_id == "why_engine_fallback_v1" for h in f.hypotheses)


def test_lc_s1_slice_combo_avoids_engine_fallback_for_lead_when_governed():
    """Lead ranked here is homocysteine_high — must compile governed WHY, not placeholder."""
    root = compile_root_cause_v1(
        signal_results=[
            {
                "signal_id": "signal_homocysteine_high",
                "primary_metric": "homocysteine",
                "signal_state": "at_risk",
                "confidence": 0.9,
            },
            {
                "signal_id": "signal_mcv_high",
                "primary_metric": "mcv",
                "signal_state": "at_risk",
                "confidence": 0.6,
            },
        ],
        biomarker_context={
            "homocysteine": 17.0,
            "mcv": {"value": 101.0},
            "vitamin_b12": {"value": 210.0},
        },
        input_reference_ranges={
            "homocysteine": {"min": 5.0, "max": 15.0, "unit": "µmol/L", "source": "lab"},
            "mcv": {"min": 80.0, "max": 99.0, "unit": "fL", "source": "lab"},
            "vitamin_b12": {"min": 200.0, "max": 900.0, "unit": "pmol/L", "source": "lab"},
        },
    )
    assert root is not None
    assert not any(f.signal_id == "why_engine_fallback_v1" for f in root.findings)
    assert any(f.signal_id == "signal_homocysteine_high" for f in root.findings)
    lead_fallback_present = any(
        any(h.hypothesis_id == "why_engine_fallback_v1" for h in f.hypotheses) for f in root.findings
    )
    assert not lead_fallback_present
