"""Generate clinical_priority_scenarios_v1.json for APPROVED_SCENARIO_ESTATE_COVERAGE."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "backend" / "tests" / "fixtures" / "clinical_priority_scenarios_v1.json"


def sig(sid: str, inv: str | None = None) -> dict:
    key = f"{sid}::{inv}" if inv else f"{sid}::activation"
    return {"signal_id": sid, "activation_key": key}


def sc(
    scenario_id: str,
    biomarkers: dict,
    expected: dict,
    *,
    signals: list | None = None,
    context: dict | None = None,
    derived: dict | None = None,
    lab_ranges: dict | None = None,
    alias_of: str | None = None,
) -> dict:
    row: dict = {
        "scenario_id": scenario_id,
        "biomarkers": biomarkers,
        "signal_results": signals or [],
        "expected": expected,
    }
    if context:
        row["context"] = context
    if derived:
        row["derived"] = derived
    if lab_ranges:
        row["lab_ranges"] = lab_ranges
    if alias_of:
        row["alias_of"] = alias_of
    return row


DEFAULT_RANGES = {
    "alt": {"min": 0, "max": 49, "source": "lab"},
    "ast": {"min": 0, "max": 40, "source": "lab"},
    "alp": {"min": 30, "max": 116, "source": "lab"},
    "ggt": {"min": 0, "max": 55, "source": "lab"},
    "bilirubin": {"min": 0, "max": 21, "source": "lab"},
    "albumin": {"min": 35, "max": 50, "source": "lab"},
    "inr": {"min": 0.8, "max": 1.2, "source": "lab"},
    "platelets": {"min": 150, "max": 450, "source": "lab"},
    "mcv": {"min": 83, "max": 96, "source": "lab"},
    "hgb": {"min": 130, "max": 170, "source": "lab"},
    "ferritin": {"min": 30, "max": 300, "source": "lab"},
    "transferrin": {"min": 2.0, "max": 3.6, "source": "lab"},
    "tsat": {"min": 20, "max": 50, "source": "lab"},
    "potassium": {"min": 3.5, "max": 5.3, "source": "lab"},
    "sodium": {"min": 133, "max": 146, "source": "lab"},
    "calcium": {"min": 2.2, "max": 2.6, "source": "lab"},
    "adjusted_calcium": {"min": 2.2, "max": 2.6, "source": "lab"},
    "creatinine": {"min": 60, "max": 110, "source": "lab"},
    "egfr": {"min": 90, "max": 120, "source": "lab"},
    "urea": {"min": 2.5, "max": 7.8, "source": "lab"},
    "magnesium": {"min": 0.7, "max": 1.0, "source": "lab"},
    "tsh": {"min": 0.4, "max": 4.0, "source": "lab"},
    "free_t4": {"min": 9.0, "max": 25.0, "source": "lab"},
    "free_t3": {"min": 3.1, "max": 6.8, "source": "lab"},
    "crp": {"min": 0, "max": 5, "source": "lab"},
    "iron": {"min": 10, "max": 30, "source": "lab"},
    "tibc": {"min": 45, "max": 72, "source": "lab"},
    "anc": {"min": 1.5, "max": 7.5, "source": "lab"},
    "wcc": {"min": 4.0, "max": 11.0, "source": "lab"},
    "triglycerides": {"min": 0, "max": 1.7, "source": "lab"},
    "total_cholesterol": {"min": 0, "max": 5.0, "source": "lab"},
    "non_hdl": {"min": 0, "max": 4.0, "source": "lab"},
    "ldl": {"min": 0, "max": 3.0, "source": "lab"},
    "hdl": {"min": 1.0, "max": 2.5, "source": "lab"},
    "hba1c": {"min": 20, "max": 42, "source": "lab"},
    "b12": {"min": 200, "max": 900, "source": "lab"},
    "vitamin_d": {"min": 50, "max": 125, "source": "lab"},
    "tpo": {"min": 0, "max": 34, "source": "lab"},
}


def hepatic_scenarios() -> list:
    # Keep Checkpoint 1 hepatic scenarios (updated HEP-AS-9 → IRIN-F3)
    raw = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {"scenarios": []}
    existing = {s["scenario_id"]: s for s in raw.get("scenarios", [])}
    # Prefer currently working hepatic fixtures from file
    keep_ids = [
        "CONTRACT-FIX-1",
        "HEP-AS-1",
        "HEP-AS-2",
        "HEP-AS-3",
        "HEP-AS-4",
        "HEP-AS-5",
        "HEP-AS-6",
        "HEP-AS-7",
        "HEP-AS-8",
        "HEP-AS-9",
        "HEP-AS-10",
        "HEP-AS-11",
        "HEP-AS-12",
        "HEP-AS-13",
        "HEP-AS-14",
    ]
    out = []
    for sid in keep_ids:
        if sid in existing:
            row = existing[sid]
            if sid == "HEP-AS-9":
                row["expected"]["finding_types"] = ["HEP-F1", "IRIN-F3"]
                row["expected"]["tier_by_type"] = {"HEP-F1": 1, "IRIN-F3": 1}
            out.append(row)
    return out


def build_all() -> dict:
    scenarios: list = []
    scenarios.extend(hepatic_scenarios())

    # --- HAEM ---
    scenarios.append(
        sc(
            "HAEM-AS-1",
            {"platelets": 18, "hgb": 128, "mcv": 92},
            {
                "finding_types": ["HAEM-F4", "HAEM-F1"],
                "urgency": "same_day",
                "severity": "severe",
                "tier": 0,
                "role": "principal_concern",
                "tier_by_type": {"HAEM-F4": 0, "HAEM-F1": 1},
                "prohibited_any": ["assert_count_genuine_or_artefact_without_repeat"],
                "dependency_flags_any": ["TIER_0_PATHWAY_DEPENDENCY"],
                "caveats_any": ["pseudothrombocytopenia_confirmation_mandatory"],
            },
            signals=[sig("signal_platelets_low"), sig("signal_hgb_low")],
            context={"sex": "male"},
        )
    )
    scenarios.append(
        sc(
            "HAEM-AS-2",
            {"hgb": 95, "mcv": 78, "platelets": 220},
            {
                "finding_types": ["HAEM-F1"],
                "urgency": "within_weeks",
                "tier": 1,
                "role": "principal_concern",
                "nested_any": ["mcv_microcytic"],
                "missing_data_notes_any": ["ferritin_not_assessable"],
                "must_not_include_finding_types": ["HAEM-F3", "IRIN-F2"],
            },
            signals=[sig("signal_hgb_low"), sig("signal_mcv_low")],
            context={"sex": "female"},
            lab_ranges={"hgb": {"min": 120, "max": 160}},
        )
    )
    scenarios.append(
        sc(
            "HAEM-AS-3",
            {"mcv": 99.5, "hgb": 140, "platelets": 220, "anc": 3.0, "wcc": 6.0},
            {
                "finding_types": ["HAEM-F2"],
                "urgency": "routine",
                "severity": "mild",
                "tier": 2,
                "role": "principal_concern",
                "prohibited_any": ["apply_hepatic_tier1_floor_to_mcv"],
            },
            signals=[sig("signal_mcv_high")],
        )
    )
    scenarios.append(
        sc(
            "HAEM-AS-4",
            {"mcv": 99.5, "platelets": 140, "hgb": 118},
            {
                "finding_types": ["HAEM-F10"],
                "urgency": "within_days",
                "tier": 1,
                "role": "principal_concern",
                "must_not_include_finding_types": ["HAEM-F1", "HAEM-F2", "HAEM-F4"],
                "caveats_any": ["no_film_standing_limitation"],
            },
            signals=[sig("signal_hgb_low"), sig("signal_platelets_low"), sig("signal_mcv_high")],
            context={"sex": "female"},
            lab_ranges={"hgb": {"min": 120, "max": 160}},
        )
    )
    scenarios.append(
        sc(
            "HAEM-AS-5",
            {"anc": 0.4, "hgb": 140, "platelets": 220, "mcv": 90, "wcc": 3.5},
            {
                "finding_types": ["HAEM-F6"],
                "urgency": "same_day",
                "severity": "severe",
                "tier": 0,
                "role": "principal_concern",
                "dependency_flags_any": ["TIER_0_PATHWAY_DEPENDENCY"],
                "caveats_any": ["ancestry_not_captured_no_adjustment"],
                "prohibited_any": ["adjust_anc_for_presumed_ancestry"],
            },
            signals=[sig("signal_anc_low")],
        )
    )
    scenarios.append(
        sc(
            "HAEM-AS-6",
            {"wcc": 3.1, "hgb": 140, "platelets": 220, "mcv": 90},
            {
                "finding_types": ["HAEM-F7"],
                "urgency": "within_weeks",
                "tier": 1,
                "role": "principal_concern",
                "missing_data_notes_any": ["neutrophil_question_insufficient_data"],
                "prohibited_any": ["infer_neutrophils_from_total_wcc"],
            },
            signals=[sig("signal_wcc_low")],
            context={"differential_absent": True},
        )
    )

    # --- RE ---
    scenarios.append(
        sc(
            "RE-AS-1",
            {"potassium": 6.8, "egfr": 55, "creatinine": 120},
            {
                "finding_types": ["RE-F9"],
                "urgency": "same_day",
                "severity": "severe",
                "tier": 0,
                "role": "principal_concern",
                "withheld": True,
                "caveats_any": ["artefact_safe_wording"],
                "dependency_flags_any": ["TIER_0_PATHWAY_DEPENDENCY"],
                "prohibited_any": ["assert_genuine_or_artefact_without_repeat"],
            },
            signals=[sig("signal_potassium_high"), sig("signal_egfr_low")],
        )
    )
    scenarios.append(
        sc(
            "RE-AS-2",
            {"potassium": 6.2, "egfr": 88, "creatinine": 90},
            {
                "finding_types": ["RE-F3"],
                "urgency": "same_day",
                "severity": "moderate",
                "tier": 0,
                "role": "principal_concern",
                "dependency_flags_any": ["TIER_0_PATHWAY_DEPENDENCY"],
            },
            signals=[sig("signal_potassium_high")],
        )
    )
    scenarios.append(
        sc(
            "RE-AS-3",
            {"creatinine": 145, "egfr": 42},
            {
                "finding_types": ["RE-F1"],
                "urgency": "same_day",
                "severity": "aki_50pct_rise_7d",
                "tier": 0,
                "role": "principal_concern",
                "dependency_flags_any": ["TIER_0_PATHWAY_DEPENDENCY"],
            },
            signals=[sig("signal_creatinine_high")],
            context={"priors": {"creatinine": {"value": 70, "days_ago": 6}}},
        )
    )
    scenarios.append(
        sc(
            "RE-AS-4",
            {"creatinine": 145, "egfr": 42},
            {
                "finding_types": ["RE-F10"],
                "urgency": "within_weeks",
                "tier": 1,
                "role": "principal_concern",
                "missing_data_notes_any": ["aki_not_assessable"],
                "prohibited_any": ["present_as_chronic"],
            },
            signals=[sig("signal_creatinine_high"), sig("signal_egfr_low")],
        )
    )
    scenarios.append(
        sc(
            "RE-AS-5",
            {"egfr": 52, "creatinine": 110},
            {
                "finding_types": ["RE-F2"],
                "urgency": "routine",
                "severity": "G3a",
                "tier": 2,
                "role": "principal_concern",
                "missing_data_notes_any": ["acr_unavailable_staging_incomplete"],
            },
            signals=[sig("signal_egfr_low")],
            context={"priors": {"egfr": {"value": 54, "months_ago": 4}}},
        )
    )
    scenarios.append(
        sc(
            "RE-AS-6",
            {"egfr": 72, "creatinine": 95, "potassium": 4.2, "sodium": 140},
            {
                "no_concern": True,
                "finding_types": [],
                "must_not_include_finding_types": ["RE-F2", "RE-F10"],
                "prohibited_any": ["classify_egfr_60_89_as_ckd_without_markers"],
            },
            signals=[],
        )
    )
    scenarios.append(
        sc(
            "RE-AS-7",
            {"calcium": 2.85},
            {
                "finding_types": [],
                "no_concern": False,
                "must_not_include_finding_types": ["RE-F7", "RE-F8"],
                "domain_notes_any": ["calcium_insufficient_data_albumin_required"],
            },
            signals=[sig("signal_calcium_high")],
            context={"albumin_absent": True},
        )
    )
    scenarios.append(
        sc(
            "RE-AS-8",
            {"calcium": 2.85, "albumin": 40, "adjusted_calcium": 2.83},
            {
                "finding_types": ["RE-F7"],
                "urgency": "within_days",
                "severity": "mild",
                "tier": 1,
                "role": "principal_concern",
            },
            signals=[sig("signal_calcium_high")],
        )
    )
    scenarios.append(
        sc(
            "RE-AS-9",
            {"sodium": 122},
            {
                "finding_types": ["RE-F5"],
                "urgency": "same_day",
                "severity": "profound",
                "tier": 0,
                "role": "principal_concern",
                "dependency_flags_any": ["TIER_0_PATHWAY_DEPENDENCY"],
                "missing_data_notes_any": ["chronicity_unknown"],
            },
            signals=[sig("signal_sodium_low")],
        )
    )
    scenarios.append(
        sc(
            "RE-AS-10",
            {"sodium": 131},
            {
                "finding_types": ["RE-F5"],
                "urgency": "within_weeks",
                "severity": "mild",
                "tier": 1,
                "role": "principal_concern",
                "caveats_any": ["j_labelled_departure_from_uk_no_investigation"],
            },
            signals=[sig("signal_sodium_low")],
        )
    )
    scenarios.append(
        sc(
            "RE-AS-11",
            {"urea": 12, "creatinine": 90, "egfr": 88, "potassium": 4.2, "sodium": 140},
            {
                "finding_types": [],
                "must_not_include_finding_types": ["RE-F2", "RE-F10", "RE-F9"],
                "domain_notes_any": ["urea_contextual_only"],
                "prohibited_any": ["present_urea_as_renal_impairment"],
            },
            signals=[sig("signal_urea_high")],
        )
    )
    scenarios.append(
        sc(
            "RE-AS-12",
            {"potassium": 6.8, "alt": 300, "alp": 80, "bilirubin": 12, "ggt": 40},
            {
                # Cross-domain / RE-AS-12: both same-day Tier 0 co-equal (ruleset v0.5)
                "finding_types": ["RE-F3", "HEP-F1"],
                "tier_by_type": {"RE-F3": 0, "HEP-F1": 0},
                "urgency_by_type": {"RE-F3": "same_day", "HEP-F1": "same_day"},
                "same_day_coequal": True,
                "dependency_flags_any": ["TIER_0_PATHWAY_DEPENDENCY"],
            },
            signals=[sig("signal_potassium_high"), sig("signal_alt_high")],
        )
    )
    scenarios.append(
        sc(
            "RE-AS-13",
            {"egfr": 40, "platelets": 45, "creatinine": 150},
            {
                "finding_types": ["RE-F10", "HAEM-PLT"],
                "tier_by_type": {"RE-F10": 1, "HAEM-PLT": 0},
                "haem_leads_on_time_band": True,
            },
            signals=[sig("signal_egfr_low"), sig("signal_platelets_low")],
        )
    )
    scenarios.append(
        sc(
            "RE-AS-14",
            {
                "potassium": 4.2,
                "sodium": 140,
                "creatinine": 85,
                "egfr": 95,
                "adjusted_calcium": 2.4,
                "albumin": 42,
                "urea": 5.0,
            },
            {
                "no_concern": True,
                "finding_types": [],
                "no_concern_notes_any": ["aki_could_not_be_assessed_without_prior"],
                "domain_notes_any": ["must_not_state_kidneys_working_normally"],
            },
        )
    )

    # --- IRIN ---
    scenarios.append(
        sc(
            "IRIN-AS-1",
            {"ferritin": 1400, "tsat": 22},
            {
                "finding_types": ["IRIN-F4"],
                "urgency": "routine",
                "tier": 2,
                "role": "principal_concern",
                "prohibited_any": ["present_overload_concern_with_low_tsat"],
            },
            signals=[sig("signal_ferritin_high")],
        )
    )
    scenarios.append(
        sc(
            "IRIN-AS-2",
            {"ferritin": 420, "tsat": 58},
            {
                "finding_types": ["IRIN-F3"],
                "urgency": "within_weeks",
                "tier": 1,
                "role": "principal_concern",
                "quarantine_flags_any": ["R4"],
                "prohibited_any": ["name_haemochromatosis_to_consumer"],
            },
            signals=[sig("signal_ferritin_high")],
        )
    )
    scenarios.append(
        sc(
            "IRIN-AS-3",
            {"ferritin": 900, "iron": 25, "tibc": 40},
            {
                "finding_types": ["IRIN-F3"],
                "urgency": "within_weeks",
                "tier": 1,
                "role": "principal_concern",
                "caveats_any": ["tsat_derived"],
            },
            signals=[sig("signal_ferritin_high")],
            # iron/TIBC → TSAT 62.5%
        )
    )
    scenarios.append(
        sc(
            "IRIN-AS-4",
            {"ferritin": 900},
            {
                "finding_types": ["IRIN-F8"],
                "urgency": "within_weeks",
                "tier": 1,
                "role": "principal_concern",
                "severity_indeterminate": True,
                "missing_data_notes_any": ["tsat_requested"],
                "prohibited_any": ["default_to_inflammatory"],
            },
            signals=[sig("signal_ferritin_high")],
        )
    )
    scenarios.append(
        sc(
            "IRIN-AS-5",
            {"ferritin": 45, "crp": 60, "hgb": 105},
            {
                "finding_types": ["IRIN-F5"],
                "urgency": "within_weeks",
                "tier": 1,
                "role": "principal_concern",
                "prohibited_any": ["report_iron_status_as_normal"],
            },
            signals=[sig("signal_crp_high"), sig("signal_hgb_low")],
            context={"sex": "female"},
            lab_ranges={"hgb": {"min": 120, "max": 160}},
        )
    )
    scenarios.append(
        sc(
            "IRIN-AS-6",
            {"ferritin": 8, "hgb": 98, "mcv": 72},
            {
                "finding_types": ["IRIN-F2"],
                "urgency": "within_weeks",
                "tier": 1,
                "role": "principal_concern",
                "must_not_include_finding_types": ["HAEM-F1"],
            },
            signals=[sig("signal_ferritin_low"), sig("signal_hgb_low")],
            context={"sex": "female"},
            lab_ranges={"hgb": {"min": 120, "max": 160}, "ferritin": {"min": 30, "max": 300}},
        )
    )
    scenarios.append(
        sc(
            "IRIN-AS-7",
            {"crp": 12},
            {
                "finding_types": ["IRIN-F6"],
                "urgency": "routine",
                "tier": 2,
                "role": "principal_concern",
                "prohibited_any": ["escalate_isolated_crp_to_tier1"],
            },
            signals=[sig("signal_crp_high")],
        )
    )
    scenarios.append(
        sc(
            "IRIN-AS-8",
            {"crp": 12},
            {
                "finding_types": ["IRIN-F7"],
                "urgency": "within_weeks",
                "tier": 1,
                "role": "principal_concern",
            },
            signals=[sig("signal_crp_high")],
            context={
                "priors": {
                    "crp_history": [
                        {"value": 12, "months_ago": 0},
                        {"value": 11, "months_ago": 4},
                        {"value": 13, "months_ago": 9},
                    ]
                }
            },
        )
    )
    scenarios.append(
        sc(
            "IRIN-AS-9",
            {"crp": 60, "platelets": 40},
            {
                "finding_types": ["HAEM-PLT"],
                "tier_by_type": {"HAEM-PLT": 0},
                "nested_any_on_haem": ["crp_contextual"],
                "must_not_include_finding_types": ["IRIN-F6", "IRIN-F7"],
                "haem_leads_on_time_band": True,
                "dependency_flags_any": ["TIER_0_PATHWAY_DEPENDENCY"],
            },
            signals=[sig("signal_crp_high"), sig("signal_platelets_low")],
        )
    )
    scenarios.append(
        sc(
            "IRIN-AS-10",
            {
                "ferritin": 1100,
                "tsat": 30,
                "alt": 120,
                "alp": 80,
                "bilirubin": 12,
                "ggt": 40,
            },
            {
                "finding_types": ["HEP-F1"],
                "tier": 1,
                "role": "principal_concern",
                "nested_any": ["ferritin_contextual"],
                "must_not_include_finding_types": ["IRIN-F3", "IRIN-F4"],
            },
            signals=[sig("signal_alt_high"), sig("signal_ferritin_high")],
        )
    )
    scenarios.append(
        sc(
            "IRIN-AS-11",
            {
                "ferritin": 1100,
                "tsat": 55,
                "alt": 120,
                "alp": 80,
                "bilirubin": 12,
                "ggt": 40,
            },
            {
                "finding_types": ["HEP-F1", "IRIN-F3"],
                "tier_by_type": {"HEP-F1": 1, "IRIN-F3": 1},
                "co_lead_eligible": True,
            },
            signals=[sig("signal_alt_high"), sig("signal_ferritin_high")],
        )
    )
    scenarios.append(
        sc(
            "IRIN-AS-12",
            {"ferritin": 120, "tsat": 30, "crp": 3, "iron": 18, "tibc": 60},
            {
                "no_concern": True,
                "finding_types": [],
                "no_concern_notes_any": [
                    "normal_ferritin_does_not_exclude_deficiency_with_inflammation"
                ],
            },
        )
    )

    # --- THY ---
    scenarios.append(
        sc(
            "THY-AS-1",
            {"tsh": 14, "free_t4": 8},
            {
                "finding_types": ["THY-F1"],
                "urgency": "within_weeks",
                "severity": "overt",
                "tier": 1,
                "role": "principal_concern",
            },
            signals=[sig("signal_tsh_high"), sig("signal_free_t4_low")],
        )
    )
    scenarios.append(
        sc(
            "THY-AS-2",
            {"tsh": 14, "free_t4": 15},
            {
                "finding_types": ["THY-F2"],
                "urgency": "within_weeks",
                "severity": "intermediate",
                "tier": 1,
                "role": "principal_concern",
                "caveats_any": ["nice_two_occasion_requirement"],
            },
            signals=[sig("signal_tsh_high")],
        )
    )
    scenarios.append(
        sc(
            "THY-AS-3",
            {"tsh": 6.2, "free_t4": 15},
            {
                "finding_types": ["THY-F2"],
                "urgency": "routine",
                "severity": "lower",
                "tier": 2,
                "role": "principal_concern",
            },
            signals=[sig("signal_tsh_high")],
        )
    )
    scenarios.append(
        sc(
            "THY-AS-4",
            {"tsh": 14},
            {
                "finding_types": ["THY-F5"],
                "urgency": "within_weeks",
                "tier": 1,
                "role": "principal_concern",
                "severity_indeterminate": True,
                "missing_data_notes_any": ["free_t4_requested", "both_states_named"],
                "prohibited_any": ["default_to_subclinical", "infer_worst_case"],
            },
            signals=[sig("signal_tsh_high")],
            context={"free_t4_absent": True},
        )
    )
    scenarios.append(
        sc(
            "THY-AS-5",
            {"tsh": 0.005, "free_t4": 32},
            {
                "finding_types": ["THY-F3"],
                "urgency": "within_weeks",
                "severity": "overt",
                "tier": 1,
                "role": "principal_concern",
            },
            signals=[sig("signal_tsh_low"), sig("signal_free_t4_high")],
        )
    )
    scenarios.append(
        sc(
            "THY-AS-6",
            {"tsh": 0.005, "free_t4": 18},
            {
                "finding_types": ["THY-F4"],
                "urgency": "within_weeks",
                "tier": 1,
                "role": "principal_concern",
                "missing_data_notes_any": ["t3_toxicosis_not_assessable"],
            },
            signals=[sig("signal_tsh_low")],
            context={"free_t3_absent": True},
        )
    )
    scenarios.append(
        sc(
            "THY-AS-7",
            {"tsh": 12, "free_t4": 28},
            {
                "finding_types": ["THY-F6"],
                "urgency": "within_days",
                "tier": 1,
                "role": "principal_concern",
                "prohibited_any": ["auto_explain_discordant_thyroid"],
            },
            signals=[sig("signal_tsh_high"), sig("signal_free_t4_high")],
        )
    )
    scenarios.append(
        sc(
            "THY-AS-8",
            {"tsh": 6.5, "free_t4": 15, "tpo": 120},
            {
                "finding_types": ["THY-F2"],
                "urgency": "routine",
                "tier": 2,
                "role": "principal_concern",
                "nested_any": ["tpo_contextual"],
                "must_not_include_finding_types": ["THY-F7"],
            },
            signals=[sig("signal_tsh_high"), sig("signal_tpo_high")],
        )
    )
    scenarios.append(
        sc(
            "THY-AS-9",
            {"tsh": 14, "free_t4": 8},
            {
                "finding_types": ["THY-F1"],
                "withheld": True,
                "dependency_flags_any": ["QUESTIONNAIRE_DEPENDENCY"],
                "prohibited_any": ["silently_suppress_pregnancy_domain"],
            },
            signals=[sig("signal_tsh_high"), sig("signal_free_t4_low")],
            context={"may_be_pregnant": True},
        )
    )
    scenarios.append(
        sc(
            "THY-AS-10",
            {"tsh": 8, "free_t4": 15, "ldl": 5.8, "total_cholesterol": 7.2},
            {
                "finding_types": ["THY-F2"],
                "urgency": "routine",
                "tier": 2,
                "role": "principal_concern",
                "nested_any": ["lipid_secondary_cause_context"],
                "must_not_include_finding_types": ["CN-F3", "CN-F9"],
            },
            signals=[sig("signal_tsh_high"), sig("signal_ldl_high")],
        )
    )
    scenarios.append(
        sc(
            "THY-AS-11",
            {"tsh": 8, "free_t4": 15, "mcv": 104, "hgb": 140, "platelets": 220},
            {
                "finding_types": ["THY-F2"],
                "urgency": "routine",
                "tier": 2,
                "nested_any": ["macrocytosis_context"],
            },
            signals=[sig("signal_tsh_high"), sig("signal_mcv_high")],
        )
    )
    scenarios.append(
        sc(
            "THY-AS-12",
            {"tsh": 2.0, "free_t4": 15},
            {
                "no_concern": True,
                "finding_types": [],
                "no_concern_notes_any": ["biotin_illness_distortion_caveat"],
            },
        )
    )

    # --- CN ---
    scenarios.append(
        sc(
            "CN-AS-1",
            {"triglycerides": 24, "hba1c": 40},
            {
                "finding_types": ["CN-F1"],
                "urgency": "same_day",
                "severity": "severe",
                "tier": 0,
                "role": "principal_concern",
                "dependency_flags_any": ["TIER_0_PATHWAY_DEPENDENCY"],
                "caveats_any": ["pancreatitis_framing_mandatory", "alcohol_unassessed"],
                "prohibited_any": ["frame_as_cardiovascular_urgency"],
            },
            signals=[sig("signal_tg_high")],
        )
    )
    scenarios.append(
        sc(
            "CN-AS-2",
            {"triglycerides": 24, "hba1c": 78},
            {
                "finding_types": ["CN-F1"],
                "urgency": "same_day",
                "tier": 0,
                "role": "principal_concern",
                "caveats_any": ["dysglycaemia_plausible_secondary_cause"],
                "prohibited_any": ["downgrade_despite_secondary_cause"],
                "dependency_flags_any": ["TIER_0_PATHWAY_DEPENDENCY"],
            },
            signals=[sig("signal_tg_high"), sig("signal_hba1c_high")],
        )
    )
    scenarios.append(
        sc(
            "CN-AS-3",
            {"total_cholesterol": 9.4, "non_hdl": 7.8},
            {
                "finding_types": ["CN-F2"],
                "urgency": "within_weeks",
                "severity": "nice_threshold",
                "tier": 1,
                "role": "principal_concern",
                "cv_risk_computed": False,
            },
            signals=[sig("signal_tc_high"), sig("signal_non_hdl_high")],
        )
    )
    scenarios.append(
        sc(
            "CN-AS-4",
            {"total_cholesterol": 7.9},
            {
                "finding_types": ["CN-F9"],
                "urgency": "routine",
                "tier": 2,
                "role": "principal_concern",
                "missing_data_notes_any": ["fh_not_assessable"],
                "cv_risk_computed": False,
            },
            signals=[sig("signal_tc_high")],
            context={"family_history_absent": True, "risk_factors_absent": True},
        )
    )
    scenarios.append(
        sc(
            "CN-AS-5",
            {"ldl": 5.2, "hdl": 1.1, "total_cholesterol": 7.2, "triglycerides": 1.8},
            {
                "finding_types": ["CN-F3"],
                "tier": 2,
                "role": "principal_concern",
                "must_not_include_finding_types": ["CN-F2"],
                "prohibited_any": ["present_four_separate_fraction_concerns"],
            },
            signals=[sig("signal_ldl_high"), sig("signal_tc_high")],
        )
    )
    scenarios.append(
        sc(
            "CN-AS-6",
            {"hba1c": 52},
            {
                "finding_types": ["CN-F4"],
                "urgency": "within_weeks",
                "tier": 1,
                "role": "principal_concern",
                "prohibited_any": ["assert_diabetes_from_single_result"],
                "caveats_any": ["confirmation_required"],
            },
            signals=[sig("signal_hba1c_high")],
        )
    )
    scenarios.append(
        sc(
            "CN-AS-7",
            {"b12": 120, "hgb": 98, "mcv": 112},
            {
                "finding_types": ["CN-F5"],
                "urgency": "within_weeks",
                "tier": 1,
                "role": "principal_concern",
                "must_not_include_finding_types": ["HAEM-F1", "HAEM-F2"],
            },
            signals=[sig("signal_b12_low"), sig("signal_hgb_low"), sig("signal_mcv_high")],
            context={"sex": "female"},
            lab_ranges={"hgb": {"min": 120, "max": 160}},
        )
    )
    scenarios.append(
        sc(
            "CN-AS-8",
            {"b12": 320, "mcv": 108, "hgb": 140},
            {
                "finding_types": ["CN-F7"],
                "urgency": "within_weeks",
                "tier": 1,
                "role": "principal_concern",
                "prohibited_any": ["report_b12_as_normal_given_context"],
            },
            signals=[sig("signal_mcv_high")],
        )
    )
    scenarios.append(
        sc(
            "CN-AS-9",
            {"b12": 110, "hgb": 82, "platelets": 90, "anc": 1.2},
            {
                "finding_types": ["HAEM-F10"],
                "urgency": "same_day",
                "tier": 0,
                "role": "principal_concern",
                "nested_any": ["b12_aetiology"],
                "must_not_include_finding_types": ["CN-F5"],
                "dependency_flags_any": ["TIER_0_PATHWAY_DEPENDENCY"],
            },
            signals=[
                sig("signal_b12_low"),
                sig("signal_hgb_low"),
                sig("signal_platelets_low"),
                sig("signal_anc_low"),
            ],
            context={"sex": "female"},
            lab_ranges={"hgb": {"min": 120, "max": 160}},
        )
    )
    scenarios.append(
        sc(
            "CN-AS-10",
            {
                "total_cholesterol": 8.8,
                "non_hdl": 7.0,
                "tsh": 12,
                "free_t4": 8,
            },
            {
                "finding_types": ["THY-F1", "CN-F3"],
                "tier_by_type": {"THY-F1": 1, "CN-F3": 1},
                "co_lead_eligible": True,
            },
            signals=[sig("signal_tc_high"), sig("signal_tsh_high"), sig("signal_free_t4_low")],
        )
    )
    scenarios.append(
        sc(
            "CN-AS-12",
            {"triglycerides": 24, "potassium": 6.8},
            {
                "finding_types": ["CN-F1", "RE-F3"],
                "tier_by_type": {"CN-F1": 0, "RE-F3": 0},
                "same_day_coequal": True,
                "dependency_flags_any": ["TIER_0_PATHWAY_DEPENDENCY"],
            },
            signals=[sig("signal_tg_high"), sig("signal_potassium_high")],
        )
    )
    scenarios.append(
        sc(
            "CN-AS-13",
            {
                "total_cholesterol": 4.5,
                "triglycerides": 1.2,
                "non_hdl": 3.2,
                "ldl": 2.5,
                "hdl": 1.3,
                "b12": 400,
                "vitamin_d": 70,
                "hba1c": 36,
            },
            {
                "no_concern": True,
                "finding_types": [],
                "no_concern_notes_any": [
                    "normal_lipid_does_not_exclude_cv_risk",
                    "normal_b12_does_not_exclude_functional_deficiency",
                ],
                "cv_risk_computed": False,
            },
        )
    )

    # --- XD scenarios ---
    scenarios.extend(_xd_scenarios())

    # Deduplicate by scenario_id preserving first (hepatic keep)
    seen = set()
    uniq = []
    for s in scenarios:
        sid = s["scenario_id"]
        if sid in seen:
            continue
        seen.add(sid)
        uniq.append(s)

    return {
        "fixture_version": "2.0.0",
        "contract_version": "0.6.3",
        "ruleset_version": "0.5",
        "approval_pack_version": "1.2",
        "scope": "approved_scenario_estate_coverage",
        "notes": [
            "CONTRACT-FIX-1 is a confirmed literal duplicate of HEP-AS-1 (alias_of).",
            "CN-AS-11 retired — excluded.",
            "FIB-4 / CV-risk % quarantined.",
            "110 fixture rows; 109 unique clinical scenarios.",
        ],
        "default_lab_ranges": DEFAULT_RANGES,
        "scenarios": uniq,
    }


def _xd_scenarios() -> list:
    out = []
    out.append(
        sc(
            "XD-AS-1",
            {"potassium": 6.8, "alt": 300, "alp": 80, "bilirubin": 12, "ggt": 40},
            {
                # Cross-domain ruleset v0.5 / pack v1.2: both same-day Tier 0 co-equal
                "finding_types": ["RE-F3", "HEP-F1"],
                "tier_by_type": {"RE-F3": 0, "HEP-F1": 0},
                "urgency_by_type": {"RE-F3": "same_day", "HEP-F1": "same_day"},
                "same_day_coequal": True,
                "dependency_flags_any": ["TIER_0_PATHWAY_DEPENDENCY"],
            },
            signals=[sig("signal_potassium_high"), sig("signal_alt_high")],
        )
    )
    out.append(
        sc(
            "XD-AS-1b",
            {"potassium": 6.2},
            {
                "finding_types": ["RE-F3"],
                "urgency": "same_day",
                "severity": "moderate",
                "tier": 0,
                "role": "principal_concern",
                "dependency_flags_any": ["TIER_0_PATHWAY_DEPENDENCY"],
                "prohibited_any": ["mild_consequence_language"],
            },
            signals=[sig("signal_potassium_high")],
        )
    )
    out.append(
        sc(
            "XD-AS-2",
            {"platelets": 45, "alt": 200, "alp": 80, "bilirubin": 12, "ggt": 40},
            {
                "finding_types": ["HEP-F1", "HAEM-PLT"],
                "tier_by_type": {"HEP-F1": 1, "HAEM-PLT": 0},
                "haem_leads_on_time_band": True,
                "prohibited_any": ["absorb_platelets_below_50"],
            },
            signals=[sig("signal_platelets_low"), sig("signal_alt_high")],
        )
    )
    out.append(
        sc(
            "XD-AS-3",
            {"platelets": 120, "alt": 200, "ast": 260, "alp": 80, "bilirubin": 12, "ggt": 40},
            {
                "finding_types": ["HEP-F1"],
                "tier": 1,
                "role": "principal_concern",
                "nested_any": ["platelets_contextual"],
                "must_not_include_finding_types": ["HAEM-PLT", "HAEM-F4"],
            },
            signals=[sig("signal_alt_high"), sig("signal_platelets_low")],
        )
    )
    out.append(
        sc(
            "XD-AS-4",
            {
                "ferritin": 420,
                "tsat": 58,
                "alt": 90,
                "alp": 80,
                "bilirubin": 12,
                "ggt": 40,
            },
            {
                "finding_types": ["HEP-F1", "IRIN-F3"],
                "tier_by_type": {"HEP-F1": 1, "IRIN-F3": 1},
                "co_lead_eligible": True,
            },
            signals=[sig("signal_alt_high"), sig("signal_ferritin_high")],
        )
    )
    out.append(
        sc(
            "XD-AS-5",
            {
                "ferritin": 1400,
                "tsat": 22,
                "alt": 90,
                "alp": 80,
                "bilirubin": 12,
                "ggt": 40,
            },
            {
                "finding_types": ["HEP-F1"],
                "tier": 1,
                "nested_any": ["ferritin_contextual"],
                "must_not_include_finding_types": ["IRIN-F3", "IRIN-F4"],
            },
            signals=[sig("signal_alt_high"), sig("signal_ferritin_high")],
        )
    )
    out.append(
        sc(
            "XD-AS-6",
            {"tsh": 14, "ldl": 5.9, "total_cholesterol": 7.5},
            {
                "finding_types": ["THY-F5"],
                "urgency": "within_weeks",
                "tier": 1,
                "severity_indeterminate": True,
                "nested_any": ["lipid_secondary_cause_context"],
                "must_not_include_finding_types": ["CN-F3", "CN-F9"],
                "missing_data_notes_any": ["free_t4_requested", "both_states_named"],
            },
            signals=[sig("signal_tsh_high"), sig("signal_ldl_high")],
            context={"free_t4_absent": True},
        )
    )
    out.append(
        sc(
            "XD-AS-7",
            {"triglycerides": 24, "sodium": 128},
            {
                # XD-ARTEFACT-1 / XD-AS-7: both same-day; Na caveat retained, not suppressed
                "finding_types": ["CN-F1", "RE-F5"],
                "tier_by_type": {"CN-F1": 0, "RE-F5": 0},
                "urgency_by_type": {"CN-F1": "same_day", "RE-F5": "same_day"},
                "same_day_coequal": True,
                "caveats_any": ["pseudohyponatraemia"],
                "dependency_flags_any": ["TIER_0_PATHWAY_DEPENDENCY"],
            },
            signals=[sig("signal_tg_high"), sig("signal_sodium_low")],
        )
    )
    out.append(
        sc(
            "XD-AS-8",
            {"b12": 110, "hgb": 82, "platelets": 88, "anc": 1.1},
            {
                "finding_types": ["HAEM-F10"],
                "urgency": "same_day",
                "tier": 0,
                "nested_any": ["b12_aetiology"],
                "must_not_include_finding_types": ["HAEM-F1", "HAEM-F4", "HAEM-F6", "CN-F5"],
                "dependency_flags_any": ["TIER_0_PATHWAY_DEPENDENCY"],
            },
            signals=[
                sig("signal_b12_low"),
                sig("signal_hgb_low"),
                sig("signal_platelets_low"),
                sig("signal_anc_low"),
            ],
            context={"sex": "female"},
            lab_ranges={"hgb": {"min": 120, "max": 160}},
        )
    )
    out.append(
        sc(
            "XD-AS-9",
            {"calcium": 2.85, "potassium": 6.7},
            {
                "finding_types": ["RE-F3"],
                "urgency": "same_day",
                "tier": 0,
                "role": "principal_concern",
                "domain_notes_any": ["calcium_insufficient_data_albumin_required"],
                "must_not_include_finding_types": ["RE-F7"],
                "dependency_flags_any": ["TIER_0_PATHWAY_DEPENDENCY"],
            },
            signals=[sig("signal_potassium_high"), sig("signal_calcium_high")],
            context={"albumin_absent": True},
        )
    )
    out.append(
        sc(
            "XD-AS-10",
            {"egfr": 38, "mcv": 104, "crp": 9, "tsh": 5.8, "free_t4": 15, "creatinine": 160},
            {
                "finding_types": ["RE-F10", "HAEM-F2", "IRIN-F6", "THY-F2"],
                "tier_by_type": {
                    "RE-F10": 1,
                    "HAEM-F2": 2,
                    "IRIN-F6": 2,
                    "THY-F2": 2,
                },
                "missing_data_notes_any": ["aki_not_assessable"],
            },
            signals=[
                sig("signal_egfr_low"),
                sig("signal_mcv_high"),
                sig("signal_crp_high"),
                sig("signal_tsh_high"),
            ],
        )
    )
    out.append(
        sc(
            "XD-AS-11",
            {
                "alt": 30,
                "ast": 25,
                "alp": 80,
                "ggt": 40,
                "bilirubin": 12,
                "albumin": 42,
                "potassium": 4.2,
                "sodium": 140,
                "egfr": 95,
                "creatinine": 80,
                "hgb": 145,
                "platelets": 220,
                "mcv": 90,
                "ferritin": 120,
                "tsat": 30,
                "crp": 2,
                "tsh": 2.0,
                "free_t4": 15,
                "total_cholesterol": 4.5,
                "triglycerides": 1.2,
                "b12": 400,
                "vitamin_d": 70,
                "hba1c": 36,
                "adjusted_calcium": 2.4,
            },
            {
                "no_concern": True,
                "finding_types": [],
                "domain_notes_any": ["must_not_imply_disease_excluded_beyond_panel_scope"],
            },
        )
    )
    out.append(
        sc(
            "XD-AS-12",
            {"potassium": 6.8, "platelets": 18, "triglycerides": 24},
            {
                "finding_types": ["RE-F3", "HAEM-F4", "CN-F1"],
                "tier_by_type": {"RE-F3": 0, "HAEM-F4": 0, "CN-F1": 0},
                "same_day_coequal": True,
                "dependency_flags_any": ["TIER_0_PATHWAY_DEPENDENCY"],
            },
            signals=[
                sig("signal_potassium_high"),
                sig("signal_platelets_low"),
                sig("signal_tg_high"),
            ],
            context={"sex": "male"},
        )
    )
    out.append(
        sc(
            "XD-AS-13",
            {"potassium": 2.3},
            {
                "finding_types": ["RE-F4"],
                "urgency": "same_day",
                "severity": "severe",
                "tier": 0,
                "role": "principal_concern",
                "dependency_flags_any": ["TIER_0_PATHWAY_DEPENDENCY"],
                "prohibited_any": ["mild_consequence_language"],
            },
            signals=[sig("signal_potassium_low")],
        )
    )
    out.append(
        sc(
            "XD-AS-14",
            {"adjusted_calcium": 2.05, "albumin": 40},
            {
                "finding_types": ["RE-F8"],
                "urgency": "within_weeks",
                "tier": 1,
                "role": "principal_concern",
                "caveats_any": ["symptom_conditional_emergency"],
            },
            signals=[sig("signal_calcium_low")],
        )
    )
    out.append(
        sc(
            "XD-AS-15",
            {"sodium": 152},
            {
                "finding_types": ["RE-F6"],
                "urgency": "within_days",
                # 146-150 mild; 151-154 moderate (Na 152)
                "severity": "moderate",
                "tier": 1,
                "role": "principal_concern",
                "caveats_any": ["j_labelled_rule"],
            },
            signals=[sig("signal_sodium_high")],
        )
    )
    out.append(
        sc(
            "XD-AS-16",
            {"calcium": 1.75},
            {
                "finding_types": [],
                "must_not_include_finding_types": ["RE-F8"],
                "domain_notes_any": ["calcium_insufficient_data_albumin_required"],
            },
            signals=[sig("signal_calcium_low")],
            context={"albumin_absent": True},
        )
    )
    out.append(
        sc(
            "XD-AS-17",
            {
                # Pack values TC8.9 / non-HDL7.2 do not meet specialist TC>9 / non-HDL>7.5;
                # with full risk-factor set → consolidated CN-F3 Tier 1, CV-risk quarantined.
                "total_cholesterol": 8.9,
                "non_hdl": 7.2,
            },
            {
                "finding_types": ["CN-F3"],
                "urgency": "within_weeks",
                "tier": 1,
                "role": "principal_concern",
                "cv_risk_computed": False,
                "cv_risk_displayed": False,
                "quarantine_flags_any": ["R2"],
            },
            signals=[sig("signal_tc_high"), sig("signal_non_hdl_high")],
            context={"full_risk_factor_set": True},
        )
    )
    out.append(
        sc(
            "XD-AS-18",
            {
                "alt": 90,
                "ast": 130,
                "platelets": 135,
                "alp": 80,
                "bilirubin": 12,
                "ggt": 40,
            },
            {
                "finding_types": ["HEP-F5"],
                "urgency": "within_weeks",
                "tier": 1,
                "fib_4_computed": False,
                "fib_4_displayed": False,
                "assert_fib_4_unused": True,
                "quarantine_flags_any": ["XD-QUAR-1"],
            },
            signals=[sig("signal_ast_high"), sig("signal_platelets_low")],
            context={"age": 61},
            derived={"fib_4": {"value": 2.1, "source": "computed"}},
        )
    )
    out.append(
        sc(
            "XD-AS-19",
            {
                "alt": 180,
                "alp": 80,
                "bilirubin": 12,
                "ggt": 40,
                "tsh": 6.2,
                "free_t4": 15,
            },
            {
                "finding_types": ["HEP-F1", "THY-F2"],
                "withheld_any": True,
                "dependency_flags_any": ["QUESTIONNAIRE_DEPENDENCY"],
                "prohibited_any": ["silently_suppress_pregnancy_domain"],
            },
            signals=[sig("signal_alt_high"), sig("signal_tsh_high")],
            context={"may_be_pregnant": True},
        )
    )
    out.append(
        sc(
            "XD-AS-20",
            {"hgb": 108},
            {
                "finding_types": ["HAEM-F1"],
                "urgency": "within_weeks",
                "tier": 1,
                "role": "principal_concern",
            },
            signals=[sig("signal_hgb_low")],
            context={"sex": "female"},
            lab_ranges={"hgb": {"min": 120, "max": 160}},
        )
    )
    out.append(
        sc(
            "XD-AS-20b",
            {"hgb": 108},
            {
                "finding_types": ["HAEM-F1"],
                "urgency": "within_weeks",
                "tier": 1,
                "severity_indeterminate": True,
                "missing_data_notes_any": ["sex_assumption_stated"],
                "prohibited_any": ["silent_sex_default"],
                "dependency_flags_any": ["QUESTIONNAIRE_DEPENDENCY"],
            },
            signals=[sig("signal_hgb_low")],
            context={"sex_absent": True},
            lab_ranges={"hgb": {"min": 120, "max": 160}},
        )
    )
    out.append(
        sc(
            "XD-AS-21",
            {"potassium": 3.2},
            {
                "finding_types": ["RE-F4"],
                "urgency": "within_weeks",
                "severity": "mild",
                "tier": 2,
                "role": "principal_concern",
                "missing_data_notes_any": ["magnesium_requested_as_companion"],
            },
            signals=[sig("signal_potassium_low")],
            context={"magnesium_absent": True},
        )
    )
    out.append(
        sc(
            "XD-AS-22",
            {"hgb": 52, "mcv": 90, "platelets": 220, "anc": 3.0},
            {
                "finding_types": ["HAEM-F1"],
                "urgency": "within_days",
                "severity": "severe",
                "tier": 1,
                "role": "principal_concern",
                "prohibited_any": ["same_day_anaemia_claim"],
            },
            signals=[sig("signal_hgb_low")],
            context={"sex": "male"},
        )
    )
    out.append(
        sc(
            "XD-AS-23",
            {"bilirubin": 95, "alt": 30, "alp": 80, "albumin": 42, "ggt": 40, "hgb": 145},
            {
                "finding_types": ["HEP-F6"],
                "urgency": "within_weeks",
                "tier": 1,
                "role": "principal_concern",
                "no_bilirubin_tier0_escalation": True,
            },
            signals=[sig("signal_bilirubin_high")],
        )
    )
    out.append(
        sc(
            "XD-AS-23b",
            {"alt": 200, "bilirubin": 50.4, "alp": 128, "ggt": 40},
            {
                "finding_types": ["HEP-F1"],
                "urgency": "same_day",
                "severity": "severe",
                "tier": 0,
                "role": "principal_concern",
                "dependency_flags_any": ["TIER_0_PATHWAY_DEPENDENCY"],
            },
            signals=[sig("signal_alt_high"), sig("signal_bilirubin_high")],
            # ALT 200/49≈4.1×; bili 50.4/21≈2.4×; ALP 128/116≈1.1× — Hy's law
        )
    )
    out.append(
        sc(
            "XD-AS-24",
            {"alt": 58, "alp": 80, "bilirubin": 12, "ggt": 40},
            {
                "finding_types": ["HEP-F1"],
                "urgency": "within_weeks",
                "severity": "mild",
                "tier": 1,
                "prohibited_any": ["describe_as_urgent_merely_because_tier1"],
            },
            signals=[sig("signal_alt_high")],
        )
    )
    out.append(
        sc(
            "XD-AS-25",
            {
                "alt": 250,
                "alp": 210,
                "ggt": 180,
                "bilirubin": 32,
                "albumin": 42,
            },
            {
                # R≈2.8 → mixed injury HEP-F3; one consolidated concern with nested constituents
                "finding_types": ["HEP-F3"],
                "tier": 1,
                "role": "principal_concern",
                "nested_any": ["alt_abnormal", "alp_abnormal", "ggt_abnormal", "bilirubin_abnormal"],
            },
            signals=[
                sig("signal_alt_high"),
                sig("signal_alp_high"),
                sig("signal_ggt_high"),
                sig("signal_bilirubin_high"),
            ],
        )
    )
    out.append(
        sc(
            "XD-AS-26",
            {"vitamin_d": 18, "adjusted_calcium": 2.4, "albumin": 40},
            {
                "finding_types": ["CN-F8"],
                "urgency": "routine",
                "tier": 2,
                "role": "principal_concern",
                "prohibited_any": ["supplementation_dose", "tier1_escalation_from_vitd"],
            },
            signals=[sig("signal_vitamin_d_low")],
        )
    )
    out.append(
        sc(
            "XD-AS-27",
            {"vitamin_d": 38, "adjusted_calcium": 2.4, "albumin": 40},
            {
                "finding_types": [],
                "must_not_include_finding_types": ["CN-F8"],
                "domain_notes_any": ["vitamin_d_contextual_only"],
                "prohibited_any": ["describe_as_proven_deficiency"],
            },
            signals=[sig("signal_vitamin_d_low")],
        )
    )
    out.append(
        sc(
            "XD-AS-28",
            {"vitamin_d": 18, "adjusted_calcium": 2.05, "albumin": 40},
            {
                "finding_types": ["RE-F8"],
                "tier": 1,
                "role": "principal_concern",
                "nested_any": ["vitamin_d_contributor"],
                "must_not_include_finding_types": ["CN-F8"],
            },
            signals=[sig("signal_calcium_low"), sig("signal_vitamin_d_low")],
        )
    )
    out.append(
        sc(
            "XD-AS-29",
            {"vitamin_d": 62, "adjusted_calcium": 2.05, "albumin": 40},
            {
                "finding_types": ["RE-F8"],
                "tier": 1,
                "must_not_include_finding_types": ["CN-F8"],
                "prohibited_any": ["nest_vitd_as_aetiological_contributor"],
            },
            signals=[sig("signal_calcium_low")],
        )
    )
    out.append(
        sc(
            "XD-AS-30",
            {"vitamin_d": 38, "adjusted_calcium": 2.05, "albumin": 40},
            {
                "finding_types": ["RE-F8"],
                "tier": 1,
                "nested_any": ["vitamin_d_limited_context"],
                "must_not_include_finding_types": ["CN-F8"],
                "prohibited_any": ["describe_as_proven_deficiency"],
            },
            signals=[sig("signal_calcium_low"), sig("signal_vitamin_d_low")],
        )
    )
    out.append(
        sc(
            "XD-AS-31",
            {"potassium": 6.2, "creatinine": 90, "egfr": 88},
            {
                "finding_types": ["RE-F3"],
                "urgency": "same_day",
                "severity": "moderate",
                "tier": 0,
                "role": "principal_concern",
                "caveats_any": ["artefact_safe_wording"],
                "dependency_flags_any": ["TIER_0_PATHWAY_DEPENDENCY"],
                "prohibited_any": ["cap_same_day_urgency_at_moderate_severity"],
            },
            signals=[sig("signal_potassium_high")],
        )
    )
    out.append(
        sc(
            "XD-AS-32",
            {
                "egfr": 38,
                "creatinine": 160,
                "ferritin": 420,
                "tsat": 58,
                "tsh": 14,
                "free_t4": 8,
            },
            {
                "finding_types": ["RE-F10", "IRIN-F3", "THY-F1"],
                "tier_by_type": {"RE-F10": 1, "IRIN-F3": 1, "THY-F1": 1},
                "no_forced_lead": True,
                "presentation_mode": "no_forced_lead",
                "missing_data_notes_any": ["aki_not_assessable"],
                "prohibited_any": [
                    "manufacture_co_leads_by_cross_domain_severity",
                    "suppress_third_to_satisfy_display",
                ],
            },
            signals=[
                sig("signal_egfr_low"),
                sig("signal_ferritin_high"),
                sig("signal_tsh_high"),
                sig("signal_free_t4_low"),
            ],
        )
    )
    out.append(
        sc(
            "XD-AS-33",
            {"tsh": 14},
            {
                "finding_types": ["THY-F5"],
                "urgency": "within_weeks",
                "tier": 1,
                "severity_indeterminate": True,
                "missing_data_notes_any": ["free_t4_requested", "both_states_named"],
                "prohibited_any": ["infer_worst_case", "default_to_subclinical"],
            },
            signals=[sig("signal_tsh_high")],
            context={"free_t4_absent": True},
        )
    )
    out.append(
        sc(
            "XD-AS-34",
            {"calcium": 2.05},
            {
                "finding_types": [],
                "must_not_include_finding_types": ["RE-F8"],
                "domain_notes_any": ["calcium_insufficient_data_albumin_required"],
            },
            signals=[sig("signal_calcium_low")],
            context={"albumin_absent": True},
        )
    )
    out.append(
        sc(
            "XD-AS-35",
            {"potassium": 6.8, "egfr": 55, "creatinine": 120},
            {
                "finding_types": ["RE-F9"],
                "urgency": "same_day",
                "severity": "severe",
                "tier": 0,
                "role": "principal_concern",
                "withheld": True,
                "dependency_flags_any": ["TIER_0_PATHWAY_DEPENDENCY"],
                "prohibited_any": ["downgrade_tier0", "omit_finding"],
            },
            signals=[sig("signal_potassium_high"), sig("signal_egfr_low")],
        )
    )
    out.append(
        sc(
            "XD-AS-36",
            {
                "ferritin": 420,
                "tsat": 58,
                "alt": 30,
                "ast": 25,
                "alp": 80,
                "ggt": 40,
                "bilirubin": 12,
            },
            {
                "finding_types": ["IRIN-F3"],
                "urgency": "within_weeks",
                "tier": 1,
                "role": "principal_concern",
                "quarantine_flags_any": ["R4"],
                "prohibited_any": ["name_haemochromatosis_to_consumer"],
            },
            signals=[sig("signal_ferritin_high")],
        )
    )
    return out


def main() -> None:
    payload = build_all()
    ids = [s["scenario_id"] for s in payload["scenarios"]]
    print("scenario_count", len(ids))
    print("unique", len(set(ids)))
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
