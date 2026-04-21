"""
N-4 — Deterministic lifestyle → interpretation bridge outputs for narrative compilation prep.

Does not extend InsightGraphV1. Emits a versioned, inspectable dict for AnalysisDTO.meta.

Rule class: contextual support only — no causal over-claim; inactive when inputs/labs absent.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Tuple

import yaml

_SSOT_PATH = Path(__file__).resolve().parents[2] / "ssot" / "lifestyle_interpretation_bridges_v1.yaml"


def _load_spec() -> Dict[str, Any]:
    raw = yaml.safe_load(_SSOT_PATH.read_text(encoding="utf-8"))
    return raw if isinstance(raw, dict) else {}


def _float_val(row: Any) -> Optional[float]:
    if isinstance(row, dict):
        raw = row.get("value", row.get("measurement"))
    else:
        raw = row
    if isinstance(raw, (int, float)):
        return float(raw)
    return None


def _ref_bounds(ref: Mapping[str, Any]) -> Tuple[Optional[float], Optional[float]]:
    lo = ref.get("min")
    hi = ref.get("max")
    a = float(lo) if isinstance(lo, (int, float)) else None
    b = float(hi) if isinstance(hi, (int, float)) else None
    return a, b


def _band(
    value: float,
    ref: Optional[Mapping[str, Any]],
) -> str:
    if ref is None or not isinstance(ref, dict):
        return "unknown"
    lo, hi = _ref_bounds(ref)
    if lo is None and hi is None:
        return "unknown"
    if lo is not None and value < lo:
        return "low"
    if hi is not None and value > hi:
        return "high"
    return "normal"


def _alcohol_units(lifestyle_inputs: Mapping[str, Any], questionnaire: Mapping[str, Any]) -> Optional[float]:
    v = lifestyle_inputs.get("alcohol_units_per_week")
    if isinstance(v, (int, float)):
        return float(v)
    cons = questionnaire.get("alcohol_drinks_weekly")
    if cons is None:
        cons = questionnaire.get("alcohol_consumption")
    if cons == "None":
        return 0.0
    if cons == "1-3 drinks":
        return 2.0
    if cons == "4-7 drinks":
        return 5.0
    if cons == "8-14 drinks":
        return 11.0
    if cons == "15+ drinks":
        return 20.0
    return None


def _fluid_liters(lifestyle_inputs: Mapping[str, Any], questionnaire: Mapping[str, Any]) -> Optional[float]:
    v = lifestyle_inputs.get("fluid_intake_liters")
    if isinstance(v, (int, float)):
        return float(v)
    intake = questionnaire.get("daily_fluid_intake")
    if intake == "Less than 1 litre":
        return 0.5
    if intake == "1-2 litres":
        return 1.5
    if intake == "2-3 litres":
        return 2.5
    if intake == "More than 3 litres":
        return 3.5
    return None


def compute_lifestyle_interpretation_bridges_v1(
    *,
    lifestyle_inputs: Mapping[str, Any],
    questionnaire_responses: Mapping[str, Any],
    biomarkers: Mapping[str, Any],
    reference_ranges: Mapping[str, Mapping[str, Any]],
) -> Dict[str, Any]:
    """
    Return deterministic bridge bundle for meta.lifestyle_interpretation_bridges_v1.

    Args:
        lifestyle_inputs: Merged Layer-2 lifestyle inputs (may be empty).
        questionnaire_responses: Raw questionnaire dict when available.
        biomarkers: Canonical filtered biomarker map from orchestrator.
        reference_ranges: input_reference_ranges from orchestrator (lab/policy merged).
    """
    spec = _load_spec()
    ver = str(spec.get("version", "1.0.0"))
    asset_id = str(spec.get("asset_id", "lifestyle_interpretation_bridges_v1"))

    li = dict(lifestyle_inputs) if lifestyle_inputs else {}
    q = dict(questionnaire_responses) if questionnaire_responses else {}

    alcohol_spec = spec.get("alcohol_one_carbon_macrocytosis") or {}
    mod_min = float(alcohol_spec.get("moderate_units_min", 8.0))
    el_min = float(alcohol_spec.get("elevated_units_min", 15.0))
    hcy_id = str(alcohol_spec.get("coherence_biomarkers", {}).get("homocysteine_id", "homocysteine"))
    mcv_id = str(alcohol_spec.get("coherence_biomarkers", {}).get("mcv_id", "mcv"))

    units = _alcohol_units(li, q)
    tier = "absent"
    if units is not None:
        if units <= 0:
            tier = "none"
        elif units < mod_min:
            tier = "low"
        elif units < el_min:
            tier = "moderate"
        else:
            tier = "elevated"

    hcy_ref = reference_ranges.get(hcy_id)
    mcv_ref = reference_ranges.get(mcv_id)
    hcy_val = _float_val(biomarkers.get(hcy_id))
    mcv_val = _float_val(biomarkers.get(mcv_id))
    hcy_band = _band(hcy_val, hcy_ref) if hcy_val is not None else "unknown"
    mcv_band = _band(mcv_val, mcv_ref) if mcv_val is not None else "unknown"

    lab_coherence = (hcy_band == "high") or (mcv_band == "high")
    alcohol_active = (
        units is not None
        and units >= mod_min
        and lab_coherence
        and (hcy_val is not None or mcv_val is not None)
    )

    alcohol_block = {
        "active": bool(alcohol_active),
        "alcohol_intake_tier": tier,
        "alcohol_units_per_week": units,
        "coherence": {
            "homocysteine_band": hcy_band,
            "mcv_band": mcv_band,
        },
        "rationale_codes": (
            ["alcohol_intake_moderate_or_higher_with_one_carbon_lab_coherence"]
            if alcohol_active
            else []
        ),
    }

    renal_spec = spec.get("hydration_activity_renal") or {}
    fluid_max = float(renal_spec.get("fluid_intake_low_liters_max", 1.2))
    low_labels = list(renal_spec.get("daily_fluid_intake_low_labels") or ["Less than 1 litre"])
    vig_high = list(renal_spec.get("vigorous_exercise_high_labels") or [])
    res_high = list(renal_spec.get("resistance_training_high_labels") or [])
    renal_ids: List[str] = list(renal_spec.get("renal_biomarker_ids") or ["egfr", "creatinine", "urea"])

    fliters = _fluid_liters(li, q)
    fluid_low = fliters is not None and fliters <= fluid_max
    if q.get("daily_fluid_intake") in low_labels:
        fluid_low = True

    vig = str(q.get("vigorous_exercise_days", "")).strip()
    res = str(q.get("resistance_training_days", "")).strip()
    high_activity = vig in vig_high or res in res_high

    renal_present = any(_float_val(biomarkers.get(rid)) is not None for rid in renal_ids)

    renal_active = bool(renal_present and (fluid_low or high_activity))

    renal_block = {
        "active": renal_active,
        "hydration_context": {
            "fluid_intake_liters": fliters,
            "fluid_intake_low": bool(fluid_low),
        },
        "activity_context": {
            "vigorous_exercise_days": vig or None,
            "resistance_training_days": res or None,
            "high_activity_pattern": bool(high_activity),
        },
        "rationale_codes": (
            ["renal_panel_with_volume_or_exercise_interpretation_context"]
            if renal_active
            else []
        ),
    }

    fspec = spec.get("fasting_dietary_glycaemic") or {}
    if_label = str(fspec.get("dietary_intermittent_fasting_label", "Intermittent fasting"))
    ext_hours = list(fspec.get("extended_fasting_hour_labels") or [])
    hba1c_id = str(fspec.get("glycaemic_biomarker_id", "hba1c"))

    dietary = str(q.get("dietary_pattern", "")).strip()
    fasting_hours = str(q.get("fasting_hours", "")).strip()
    if_pattern = dietary == if_label or (fasting_hours in ext_hours)

    hba1c_val = _float_val(biomarkers.get(hba1c_id))
    hba1c_ref = reference_ranges.get(hba1c_id)
    hba1c_band = _band(hba1c_val, hba1c_ref) if hba1c_val is not None else "unknown"

    glyc_active = bool(
        if_pattern
        and hba1c_val is not None
        and hba1c_band in {"normal", "low"}
    )

    glyc_block = {
        "active": glyc_active,
        "fasting_pattern": {
            "dietary_pattern": dietary or None,
            "fasting_hours": fasting_hours or None,
            "intermittent_fasting_or_extended_overnight_fast": bool(if_pattern),
        },
        "glycaemic_markers": {
            "hba1c_band": hba1c_band,
        },
        "rationale_codes": (
            ["fasting_pattern_with_favourable_glycaemic_lab_context"]
            if glyc_active
            else []
        ),
    }

    inputs_fingerprint = json.dumps(
        {
            "li_keys": sorted(li.keys()),
            "q_keys": sorted(q.keys()),
            "biomarker_keys": sorted(biomarkers.keys()),
        },
        sort_keys=True,
    )

    return {
        "bridge_asset_version": ver,
        "bridge_asset_id": asset_id,
        "bridge_asset_path": str(_SSOT_PATH.as_posix()),
        "alcohol_methylation_macrocytosis": alcohol_block,
        "hydration_activity_renal": renal_block,
        "fasting_dietary_glycaemic": glyc_block,
        "trace": {
            "inputs_fingerprint_sha256": hashlib.sha256(
                inputs_fingerprint.encode("utf-8")
            ).hexdigest(),
        },
    }
