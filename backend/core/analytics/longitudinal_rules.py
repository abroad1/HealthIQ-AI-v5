"""
CLIN-PRIORITY-CORE-1 — Governed longitudinal rule helpers.

Six rules only (package definition v1.1 §9). No invented thresholds,
no trend-triggered tier promotion, no medication-cessation advice.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple


DAYS_PER_MONTH = 30.0


def prior_days_ago(prior: Dict[str, Any]) -> Optional[float]:
    if not isinstance(prior, dict):
        return None
    if prior.get("days_ago") is not None:
        try:
            return float(prior["days_ago"])
        except (TypeError, ValueError):
            return None
    if prior.get("months_ago") is not None:
        try:
            return float(prior["months_ago"]) * DAYS_PER_MONTH
        except (TypeError, ValueError):
            return None
    return None


def prior_value(prior: Dict[str, Any]) -> Optional[float]:
    if not isinstance(prior, dict):
        return None
    raw = prior.get("value")
    if raw is None:
        return None
    try:
        return float(raw)
    except (TypeError, ValueError):
        return None


def units_comparable(prior: Dict[str, Any], expected_unit: Optional[str] = None) -> bool:
    """Refuse longitudinal application when units are explicitly incomparable."""
    if not isinstance(prior, dict):
        return False
    if prior.get("comparable") is False:
        return False
    unit = prior.get("unit")
    if expected_unit and unit and str(unit).strip().lower() != str(expected_unit).strip().lower():
        return False
    return True


# ---------------------------------------------------------------------------
# RE-T1 — AKI (already used by concern_constructor; re-exported for coverage)
# ---------------------------------------------------------------------------


def evaluate_aki_re_t1(
    creatinine: Optional[float],
    prior: Optional[Dict[str, Any]],
) -> Tuple[bool, List[str]]:
    """NICE NG148: ≥26 µmol/L in 48h or ≥50% in 7 days."""
    notes: List[str] = []
    if creatinine is None or not isinstance(prior, dict):
        notes.append("aki_not_assessable_no_prior")
        return False, notes
    if not units_comparable(prior, prior.get("unit") or "umol/L"):
        notes.append("aki_not_assessable_incomparable_units")
        return False, notes
    prior_f = prior_value(prior)
    days = prior_days_ago(prior)
    if prior_f is None or days is None or prior_f <= 0:
        notes.append("aki_not_assessable_no_prior")
        return False, notes
    rise = creatinine - prior_f
    pct = (rise / prior_f) * 100.0
    if days <= 7 and pct >= 50:
        notes.append("re_t1_aki_50pct_within_7d")
        return True, notes
    if days <= 2 and rise >= 26:
        notes.append("re_t1_aki_26umol_within_48h")
        return True, notes
    notes.append("re_t1_aki_criteria_not_met")
    return False, notes


# ---------------------------------------------------------------------------
# RE-S-2 — CKD chronicity ≥3 months
# ---------------------------------------------------------------------------


def evaluate_ckd_chronicity_re_s2(
    egfr: Optional[float],
    prior: Optional[Dict[str, Any]],
    *,
    g3a_low: float = 45.0,
    g3a_high: float = 59.0,
    max_delta: float = 5.0,
) -> Tuple[bool, List[str]]:
    notes: List[str] = []
    if egfr is None or not (g3a_low <= egfr <= g3a_high):
        return False, notes
    if not isinstance(prior, dict):
        notes.append("ckd_chronicity_unknown_absent_prior")
        return False, notes
    if not units_comparable(prior):
        notes.append("ckd_chronicity_not_assessable_incomparable_units")
        return False, notes
    days = prior_days_ago(prior)
    if days is None or days < 3 * DAYS_PER_MONTH:
        notes.append("ckd_chronicity_window_not_met")
        return False, notes
    prior_egfr = prior_value(prior)
    if prior_egfr is None:
        if prior.get("similar") or prior.get("stable"):
            notes.append("re_s2_ckd_chronicity_established")
            return True, notes
        notes.append("ckd_chronicity_unknown_absent_prior")
        return False, notes
    if abs(prior_egfr - egfr) <= max_delta:
        notes.append("re_s2_ckd_chronicity_established")
        return True, notes
    notes.append("ckd_not_stable_within_window")
    return False, notes


# ---------------------------------------------------------------------------
# HEP-T1 — statin monitoring enzyme doubling within 3 months of start
# ---------------------------------------------------------------------------


def evaluate_statin_doubling_hep_t1(
    current_enzyme: Optional[float],
    prior: Optional[Dict[str, Any]],
    context: Dict[str, Any],
) -> Tuple[str, List[str], List[str]]:
    """
    Returns (status, caveats, notes).
    status: doubled | not_doubled | not_assessable | not_applicable
    """
    notes: List[str] = []
    caveats: List[str] = ["must_not_advise_medication_cessation"]
    statin = context.get("statin_monitoring") is True or context.get("statin_started") is True
    start_days = context.get("statin_start_days_ago")
    if start_days is None and context.get("statin_start_months_ago") is not None:
        try:
            start_days = float(context["statin_start_months_ago"]) * DAYS_PER_MONTH
        except (TypeError, ValueError):
            start_days = None
    if not statin and start_days is None:
        return "not_applicable", [], notes

    notes.append("hep_t1_statin_monitoring_context")
    if current_enzyme is None:
        notes.append("hep_t1_not_assessable_current_enzyme_absent")
        return "not_assessable", caveats, notes
    if not isinstance(prior, dict):
        notes.append("hep_t1_not_assessable_no_baseline")
        return "not_assessable", caveats, notes
    if not units_comparable(prior):
        notes.append("hep_t1_not_assessable_incomparable_units")
        return "not_assessable", caveats, notes
    prior_f = prior_value(prior)
    days = prior_days_ago(prior)
    if prior_f is None or prior_f <= 0 or days is None:
        notes.append("hep_t1_not_assessable_no_baseline")
        return "not_assessable", caveats, notes
    # Window: enzyme change within 3 months of statin start (and prior within that window)
    if start_days is not None:
        try:
            start_f = float(start_days)
        except (TypeError, ValueError):
            notes.append("hep_t1_not_assessable_start_date_invalid")
            return "not_assessable", caveats, notes
        if start_f > 3 * DAYS_PER_MONTH:
            notes.append("hep_t1_outside_3_month_start_window")
            return "not_applicable", caveats, notes
    if days > 3 * DAYS_PER_MONTH:
        notes.append("hep_t1_prior_outside_3_month_window")
        return "not_assessable", caveats, notes
    if current_enzyme >= 2.0 * prior_f:
        notes.append("hep_t1_enzyme_doubled_within_3_months")
        return "doubled", caveats, notes
    notes.append("hep_t1_enzyme_not_doubled")
    return "not_doubled", caveats, notes


# ---------------------------------------------------------------------------
# HAEM-T5 — cytopenia chronicity (12m) / rate-of-change window (3m)
# ---------------------------------------------------------------------------


def evaluate_cytopenia_haem_t5(
    current_platelets: Optional[float],
    prior: Optional[Dict[str, Any]],
) -> Tuple[str, List[str]]:
    """
    status: new_no_prior | chronicity_established | rate_window_only | prior_outside_validity
    Does not invent a numeric rate threshold — only window validity + absent≠stable.
    """
    notes: List[str] = ["haem_t5_evidence_grade_j"]
    if current_platelets is None:
        return "not_applicable", notes
    if not isinstance(prior, dict):
        notes.append("cytopenia_chronicity_unknown_absent_prior")
        notes.append("treat_cytopenia_as_new")
        notes.append("absent_history_is_not_stability")
        return "new_no_prior", notes
    if not units_comparable(prior):
        notes.append("cytopenia_longitudinal_not_assessable_incomparable_units")
        notes.append("absent_history_is_not_stability")
        return "new_no_prior", notes
    days = prior_days_ago(prior)
    prior_f = prior_value(prior)
    if days is None or prior_f is None:
        notes.append("cytopenia_chronicity_unknown_absent_prior")
        notes.append("treat_cytopenia_as_new")
        return "new_no_prior", notes
    if days <= 3 * DAYS_PER_MONTH:
        notes.append("cytopenia_rate_of_change_window_valid")
    if days <= 12 * DAYS_PER_MONTH:
        notes.append("cytopenia_chronicity_window_valid")
        # Longstanding if prior also low and within 12 months
        if prior_f < 150 and current_platelets < 150:
            notes.append("cytopenia_chronicity_established_within_12m")
            return "chronicity_established", notes
        return "rate_window_only" if days <= 3 * DAYS_PER_MONTH else "chronicity_window_only", notes
    notes.append("cytopenia_prior_outside_12m_validity")
    notes.append("treat_cytopenia_as_new")
    return "prior_outside_validity", notes


# ---------------------------------------------------------------------------
# THY-T1 — subclinical two-occasion confirmation ≥3 months
# ---------------------------------------------------------------------------


def evaluate_thyroid_two_occasion_thy_t1(
    tsh: Optional[float],
    tsh_uln: Optional[float],
    prior: Optional[Dict[str, Any]],
) -> Tuple[str, List[str], List[str]]:
    """
    status: confirmed | pending_interval | single_result | not_applicable
    """
    notes: List[str] = []
    caveats: List[str] = ["nice_two_occasion_requirement"]
    prohibited_extra = ["assert_treatment_from_single_thyroid_result"]
    if tsh is None or tsh_uln is None or tsh <= tsh_uln:
        return "not_applicable", [], []
    if not isinstance(prior, dict):
        notes.append("thy_t1_single_result_confirmation_pending")
        return "single_result", caveats, prohibited_extra
    if not units_comparable(prior):
        notes.append("thy_t1_not_assessable_incomparable_units")
        return "single_result", caveats, prohibited_extra
    prior_tsh = prior_value(prior)
    days = prior_days_ago(prior)
    if prior_tsh is None or days is None:
        notes.append("thy_t1_single_result_confirmation_pending")
        return "single_result", caveats, prohibited_extra
    if prior_tsh <= tsh_uln:
        notes.append("thy_t1_prior_not_raised")
        return "single_result", caveats, prohibited_extra
    if days < 3 * DAYS_PER_MONTH:
        notes.append("thy_t1_interval_lt_3_months_not_independent")
        return "pending_interval", caveats, prohibited_extra
    notes.append("thy_t1_two_occasion_confirmation_satisfied")
    return "confirmed", ["nice_two_occasion_confirmed"], []


# ---------------------------------------------------------------------------
# CN-T2 / CN-T3 — HbA1c spacing / diabetes confirmation
# ---------------------------------------------------------------------------


def evaluate_hba1c_confirmation_cn_t2_t3(
    hba1c: Optional[float],
    prior: Optional[Dict[str, Any]],
    *,
    diabetes_threshold: float = 48.0,
) -> Tuple[str, List[str], List[str]]:
    """
    status: confirmation_required | spacing_met | prior_too_recent | not_applicable
    Never asserts a diabetes diagnosis.
    """
    notes: List[str] = []
    prohibited = [
        "assert_diabetes_from_single_result",
        "assert_diabetes_diagnosis_from_single_result",
    ]
    if hba1c is None or hba1c < diabetes_threshold:
        return "not_applicable", [], []
    caveats = ["confirmation_required"]
    if not isinstance(prior, dict):
        notes.append("cn_t3_single_hba1c_confirmation_required")
        return "confirmation_required", caveats, prohibited
    if not units_comparable(prior):
        notes.append("cn_t2_not_assessable_incomparable_units")
        return "confirmation_required", caveats, prohibited
    prior_h = prior_value(prior)
    days = prior_days_ago(prior)
    if prior_h is None or days is None:
        notes.append("cn_t3_single_hba1c_confirmation_required")
        return "confirmation_required", caveats, prohibited
    if days < 3 * DAYS_PER_MONTH:
        notes.append("cn_t2_prior_lt_3_months_not_independent_timepoint")
        return "prior_too_recent", caveats, prohibited
    if prior_h >= diabetes_threshold:
        notes.append("cn_t2_t3_confirmation_spacing_met")
        # Still may not assert diagnosis — spacing satisfied only
        return "spacing_met", ["confirmation_spacing_met", "may_not_assert_diabetes_diagnosis"], prohibited
    notes.append("cn_t3_prior_below_diagnostic_range")
    return "confirmation_required", caveats, prohibited
