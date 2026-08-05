"""
CLIN-PRIORITY-CORE-1 — Focused concern-constructor corrections.
"""

from core.analytics.concern_constructor import construct_clinical_concern_set
from core.analytics.prioritisation_registry import load_prioritisation_package


PKG = load_prioritisation_package()

DEFAULT_RANGES = {
    "alt": {"min": 0, "max": 49, "source": "lab"},
    "alp": {"min": 30, "max": 116, "source": "lab"},
    "bilirubin": {"min": 0, "max": 21, "source": "lab"},
    "ggt": {"min": 0, "max": 55, "source": "lab"},
}


def test_xd_as_1_same_day_coequal_no_forced_lead():
    concern = construct_clinical_concern_set(
        signal_results=[
            {
                "signal_id": "signal_potassium_high",
                "activation_key": "signal_potassium_high::activation",
            },
            {
                "signal_id": "signal_alt_high",
                "activation_key": "signal_alt_high::activation",
            },
        ],
        biomarkers={
            "potassium": 6.8,
            "alt": 300,
            "alp": 80,
            "bilirubin": 12,
            "ggt": 40,
        },
        lab_ranges=DEFAULT_RANGES,
        package=PKG,
    )
    by_type = {f.finding_type: f for f in concern.findings}
    assert set(by_type) >= {"RE-F3", "HEP-F1"}
    assert by_type["RE-F3"].urgency_time_band == "same_day"
    assert by_type["HEP-F1"].urgency_time_band == "same_day"
    assert by_type["RE-F3"].concern_tier == 0
    assert by_type["HEP-F1"].concern_tier == 0
    same_day = [f for f in concern.findings if f.urgency_time_band == "same_day"]
    assert len(same_day) >= 2
    assert concern.presentation_mode == "co_lead"
    # No manufactured solo lead inside the co-equal group
    assert not (
        concern.presentation_mode == "principal"
        and len(concern.lead_finding_ids) == 1
        and not concern.co_lead_finding_ids
    )
    assert set(concern.co_lead_finding_ids) == {f.finding_id for f in same_day}
    assert concern.lead_finding_ids == []


def test_xd_as_7_same_day_pseudohyponatraemia_caveat():
    concern = construct_clinical_concern_set(
        signal_results=[
            {
                "signal_id": "signal_tg_high",
                "activation_key": "signal_tg_high::activation",
            },
            {
                "signal_id": "signal_sodium_low",
                "activation_key": "signal_sodium_low::activation",
            },
        ],
        biomarkers={"triglycerides": 24, "sodium": 128},
        lab_ranges=DEFAULT_RANGES,
        package=PKG,
    )
    by_type = {f.finding_type: f for f in concern.findings}
    assert set(by_type) >= {"CN-F1", "RE-F5"}
    assert by_type["CN-F1"].urgency_time_band == "same_day"
    assert by_type["RE-F5"].urgency_time_band == "same_day"
    assert by_type["CN-F1"].concern_tier == 0
    assert by_type["RE-F5"].concern_tier == 0
    caveats = " ".join(by_type["RE-F5"].caveats or [])
    assert "pseudohyponatraemia" in caveats
    same_day = [f for f in concern.findings if f.urgency_time_band == "same_day"]
    assert len(same_day) >= 2
    assert concern.presentation_mode == "co_lead"
    assert concern.lead_finding_ids == []
