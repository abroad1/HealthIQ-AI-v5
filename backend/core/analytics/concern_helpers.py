"""Shared helpers for clinical concern construction (CLIN-PRIORITY-CORE-1)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence, Tuple

from core.models.clinical_finding import (
    CLINICAL_FINDING_CONTRACT_VERSION,
    CLINICAL_FINDING_RULESET_VERSION,
    ClinicalFinding,
    FindingProvenance,
    RuleCitation,
    make_finding_id,
)


def num(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, dict):
        for key in ("value", "measurement", "result"):
            if key in value:
                return num(value[key])
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


_ALIASES = {
    "hb": ("hgb", "haemoglobin", "hemoglobin"),
    "hgb": ("hb", "haemoglobin", "hemoglobin"),
    "tsat": ("transferrin_saturation", "transferrin_sat"),
    "transferrin_saturation": ("tsat", "transferrin_sat"),
    "platelets": ("plt", "platelet_count"),
    "plt": ("platelets", "platelet_count"),
    "anc": ("neutrophils", "neutrophil_count", "absolute_neutrophil_count"),
    "wcc": ("wbc", "total_wcc", "white_cell_count"),
    "potassium": ("k", "k_plus"),
    "sodium": ("na", "na_plus"),
    "calcium": ("ca", "total_calcium"),
    "adjusted_calcium": ("calcium_adjusted", "adj_calcium", "corrected_calcium"),
    "egfr": ("e_gfr",),
    "creatinine": ("creat", "cr"),
    "free_t4": ("ft4", "freeT4", "t4_free"),
    "free_t3": ("ft3", "freeT3", "t3_free"),
    "triglycerides": ("tg", "trig"),
    "tg": ("triglycerides", "trig"),
    "total_cholesterol": ("tc", "cholesterol"),
    "tc": ("total_cholesterol", "cholesterol"),
    "non_hdl": ("non_hdl_c", "nonhdl"),
    "vitamin_d": ("vit_d", "vitd", "25ohd", "oh_vitamin_d"),
    "b12": ("vitamin_b12", "cobalamin"),
    "hba1c": ("hb_a1c", "a1c"),
    "ldl": ("ldl_c",),
    "hdl": ("hdl_c",),
}


def biomarker_value(biomarkers: Dict[str, Any], biomarker_id: str) -> Optional[float]:
    if biomarker_id in biomarkers:
        return num(biomarkers[biomarker_id])
    for alt in _ALIASES.get(biomarker_id, ()):
        if alt in biomarkers:
            return num(biomarkers[alt])
    return None


def range_bounds(
    lab_ranges: Dict[str, Any], biomarker_id: str
) -> Tuple[Optional[float], Optional[float]]:
    row = lab_ranges.get(biomarker_id)
    if row is None:
        for alt in _ALIASES.get(biomarker_id, ()):
            row = lab_ranges.get(alt)
            if row is not None:
                break
    if not isinstance(row, dict):
        return None, None
    lo = row.get("min", row.get("low", row.get("lrl")))
    hi = row.get("max", row.get("high", row.get("uln")))
    return num(lo), num(hi)


def x_uln(value: Optional[float], uln: Optional[float]) -> Optional[float]:
    if value is None or uln is None or uln <= 0:
        return None
    return value / uln


def is_high(value: Optional[float], uln: Optional[float]) -> bool:
    if value is None or uln is None:
        return False
    return value > uln


def is_low(value: Optional[float], lrl: Optional[float]) -> bool:
    if value is None or lrl is None:
        return False
    return value < lrl


def activation_key(row: Any) -> str:
    if isinstance(row, dict):
        return str(row.get("activation_key") or "").strip()
    return str(getattr(row, "activation_key", "") or "").strip()


def signal_id(row: Any) -> str:
    if isinstance(row, dict):
        return str(row.get("signal_id") or "").strip()
    return str(getattr(row, "signal_id", "") or "").strip()


def keys_matching(signal_results: Sequence[Any], prefixes: Tuple[str, ...]) -> List[str]:
    out: List[str] = []
    for row in signal_results or []:
        key = activation_key(row)
        sid = signal_id(row)
        hay = f"{sid}::{key}" if sid and key else (key or sid)
        if any(hay.startswith(p) or sid.startswith(p) or key.startswith(p) for p in prefixes):
            if key:
                out.append(key)
            elif sid:
                out.append(sid)
    return sorted(set(out))


def synthetic_key(finding_type: str, suffix: str) -> str:
    return f"clinical_prioritisation::{finding_type}:{suffix}"


def build_finding(
    *,
    domain: str,
    finding_type: str,
    label: str,
    keys: List[str],
    biomarkers: List[str],
    urgency: str,
    severity: Optional[str],
    tier: int,
    role: str,
    presentation_state: str = "principal",
    missing_data_state: str = "none",
    missing_data_notes: Optional[List[str]] = None,
    caveats: Optional[List[str]] = None,
    prohibited: Optional[List[str]] = None,
    serious_result_state: str = "not_applicable",
    release_gate_status: str = "RELEASE_AUTHORISED",
    withheld: bool = False,
    rule_ids: Optional[List[str]] = None,
    nested_labels: Optional[List[str]] = None,
    quarantine_flags: Optional[List[str]] = None,
    dependency_flags: Optional[List[str]] = None,
    confidence: Optional[str] = None,
    actionability: Optional[str] = None,
    severity_indeterminate: bool = False,
    compile_run_id: Optional[str] = None,
) -> ClinicalFinding:
    cleaned_keys = sorted({k for k in keys if k})
    if not cleaned_keys:
        raise ValueError(f"{finding_type} requires constituent_activation_keys")
    finding_id = make_finding_id(domain, finding_type, cleaned_keys)
    citations = [
        RuleCitation(rule_id=rid, evidence_label=None) for rid in (rule_ids or [])
    ]
    return ClinicalFinding(
        finding_id=finding_id,
        domain=domain,
        finding_type=finding_type,
        label=label,
        constituent_activation_keys=cleaned_keys,
        constituent_biomarker_ids=sorted(set(biomarkers)),
        urgency_time_band=urgency,  # type: ignore[arg-type]
        severity_band=severity,
        severity_indeterminate=severity_indeterminate,
        concern_tier=tier,  # type: ignore[arg-type]
        role=role,  # type: ignore[arg-type]
        presentation_state=presentation_state,  # type: ignore[arg-type]
        clinical_significance=None,
        actionability=actionability,
        interpretive_confidence=confidence,
        missing_data_state=missing_data_state,  # type: ignore[arg-type]
        missing_data_notes=list(missing_data_notes or []),
        caveats=list(caveats or []),
        prohibited_behaviours_asserted=list(prohibited or []),
        serious_result_state=serious_result_state,  # type: ignore[arg-type]
        release_gate_status=release_gate_status,  # type: ignore[arg-type]
        withheld=withheld,
        provenance=FindingProvenance(
            clinical_rule_ids=list(rule_ids or []),
            contract_version=CLINICAL_FINDING_CONTRACT_VERSION,
            ruleset_version=CLINICAL_FINDING_RULESET_VERSION,
            compile_run_id=compile_run_id,
            rule_citations=citations,
        ),
        relationships=[],
        nested_constituent_labels=list(nested_labels or []),
        quarantine_flags=list(quarantine_flags or []),
        dependency_flags=list(dependency_flags or []),
    )


def tier0_flags(withheld: bool = True) -> Dict[str, Any]:
    return {
        "serious_result_state": "tier_0_withheld" if withheld else "tier_0_classified",
        "release_gate_status": "SPECIFICATION_ONLY",
        "withheld": withheld,
        "dependency_flags": ["TIER_0_PATHWAY_DEPENDENCY"],
    }


def pregnancy_known(context: Dict[str, Any]) -> bool:
    return bool(
        context.get("pregnant")
        or context.get("may_be_pregnant")
        or context.get("pregnancy_known")
    )
