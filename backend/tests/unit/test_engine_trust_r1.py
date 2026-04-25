"""
R-1 — Engine trust bugs (reset Sprint 1) regression tests.
"""

from __future__ import annotations

from core.analytics.root_cause_compiler_v1 import compile_root_cause_v1
from core.analytics.signal_evaluator import SignalEvaluator, SignalRegistry
from core.scoring.rules import ScoringRules


def test_bug1_contradictory_total_cholesterol_activation_respects_upper_flag() -> None:
    reg = SignalRegistry()
    ev = SignalEvaluator(reg)
    lab_ranges = {"total_cholesterol": {"min": 3.0, "max": 5.0}}
    mid = 4.0

    high_only = {
        "activation_config": {
            "enable_upper_bound": True,
            "enable_lower_bound": False,
        },
    }
    low_only = {
        "activation_config": {
            "enable_upper_bound": False,
            "enable_lower_bound": True,
        },
    }
    s_high = ev._evaluate_lab_range_activation_state(  # noqa: SLF001
        high_only, "total_cholesterol", mid, lab_ranges
    )
    s_low = ev._evaluate_lab_range_activation_state(  # noqa: SLF001
        low_only, "total_cholesterol", mid, lab_ranges
    )
    assert s_high is None
    assert s_low is None

    s_high2 = ev._evaluate_lab_range_activation_state(  # noqa: SLF001
        high_only, "total_cholesterol", 5.5, lab_ranges
    )
    s_low2 = ev._evaluate_lab_range_activation_state(  # noqa: SLF001
        low_only, "total_cholesterol", 2.5, lab_ranges
    )
    assert s_high2 in {"at_risk", "suboptimal", "optimal", "unknown"}
    assert s_low2 in {"at_risk", "suboptimal", "optimal", "unknown"}


def test_bug2_one_sided_ldl_hdl_scored_without_unscored_reason() -> None:
    rules = ScoringRules()
    ldl = {"min": None, "max": 3.0, "unit": "mmol/L", "source": "lab"}
    s_ldl, _, u_ldl = rules.calculate_biomarker_score("ldl_cholesterol", 2.5, None, None, input_reference_range=ldl)
    hdl = {"min": 1.0, "max": None, "unit": "mmol/L", "source": "lab"}
    s_hdl, _, u_hdl = rules.calculate_biomarker_score("hdl_cholesterol", 1.2, None, None, input_reference_range=hdl)
    assert u_ldl is None
    assert u_hdl is None
    assert 0.0 < float(s_ldl) <= 100.0
    assert 0.0 < float(s_hdl) <= 100.0


def test_bug3_lead_without_governed_why_receives_engine_fallback() -> None:
    root = compile_root_cause_v1(
        signal_results=[
            {
                "signal_id": "signal_r1_placeholder_not_in_root_cause_targets",
                "primary_metric": "vitamin_d_25_oh",
                "signal_state": "at_risk",
                "confidence": 0.7,
            }
        ],
        biomarker_context={"vitamin_d_25_oh": 42.0},
        input_reference_ranges={"vitamin_d_25_oh": {"min": 75.0, "max": 200.0, "unit": "nmol/L", "source": "lab"}},
    )
    assert root is not None
    assert len(root.findings) == 1
    f0 = root.findings[0]
    assert f0.signal_id == "signal_r1_placeholder_not_in_root_cause_targets"
    assert f0.hypotheses[0].hypothesis_id == "why_engine_fallback_v1"
    assert "not yet available" in f0.hypotheses[0].summary.lower()
