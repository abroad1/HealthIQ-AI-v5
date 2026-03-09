"""
Derived Ratio Registry — centralised deterministic ratio computation.

Sprint 4 (Derived Ratio Registry). PRD §3.4, §4.5.
Sprint 5: Extended with nlr, urea_creatinine_ratio, ast_alt_ratio; structured output.
All derived ratios computed here; insights must not compute ratios locally.
Runs after unit normalisation; uses base-unit values only.
"""

from math import log, sqrt
from typing import Dict, Optional, Any, List

from core.analytics.primitives import safe_ratio


class RatioRegistry:
    """Centralised ratio computation. Sprint 4/5."""

    version = "1.1.0"

# Ratio precision: 3 decimal places for dimensionless ratios
RATIO_PRECISION = 3
# non_hdl_cholesterol uses concentration unit (mmol/L); 2 dp sufficient
NON_HDL_PRECISION = 2
TYG_SI_CONSTANT = 1596.0  # 88.5714 * 18.018; SI-native TyG constant (no runtime unit conversion)

# All derived markers (order: lipid first, then others)
DERIVED_IDS = (
    "tc_hdl_ratio", "tg_hdl_ratio", "ldl_hdl_ratio", "non_hdl_cholesterol", "apob_apoa1_ratio",
    "remnant_cholesterol", "homa_ir", "fib_4", "tyg_index", "tyg_bmi_index", "nlr", "sii",
    "urea_creatinine_ratio", "ast_alt_ratio", "testosterone_free_testosterone_ratio",
)
RATIO_IDS = DERIVED_IDS  # Backwards compatibility

# Input biomarkers per derived marker
_DERIVED_INPUTS: Dict[str, List[str]] = {
    "tc_hdl_ratio": ["total_cholesterol", "hdl_cholesterol"],
    "tg_hdl_ratio": ["triglycerides", "hdl_cholesterol"],
    "ldl_hdl_ratio": ["ldl_cholesterol", "hdl_cholesterol"],
    "non_hdl_cholesterol": ["total_cholesterol", "hdl_cholesterol"],
    "apob_apoa1_ratio": ["apob", "apoa1"],
    "remnant_cholesterol": ["total_cholesterol", "ldl_cholesterol", "hdl_cholesterol"],
    "homa_ir": ["glucose", "insulin"],
    "fib_4": ["age", "ast", "platelets", "alt"],
    "tyg_index": ["triglycerides", "glucose"],
    "tyg_bmi_index": ["triglycerides", "glucose", "bmi"],
    "nlr": ["neutrophils", "lymphocytes"],
    "sii": ["platelets", "neutrophils", "lymphocytes"],
    "urea_creatinine_ratio": ["urea", "creatinine"],
    "ast_alt_ratio": ["ast", "alt"],
    "testosterone_free_testosterone_ratio": ["testosterone", "free_testosterone"],
}


def _numeric(value: Any) -> Optional[float]:
    """Extract numeric value; return None if missing or non-numeric."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if hasattr(value, "value"):
        v = value.value
        return float(v) if isinstance(v, (int, float)) else None
    if isinstance(value, dict) and "value" in value:
        v = value["value"]
        return float(v) if isinstance(v, (int, float)) else None
    return None


def _lab_supplied(panel: Dict[str, Any], rid: str) -> bool:
    """True if derived marker exists in panel with valid numeric."""
    return rid in panel and _numeric(panel.get(rid)) is not None


def _derived_unit(rid: str) -> str:
    """Unit for derived marker (mmol/L for non_hdl_cholesterol, ratio otherwise)."""
    return "mmol/L" if rid == "non_hdl_cholesterol" else "ratio"


def compute(panel: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compute derived ratios from a biomarker panel.

    Panel keys must be canonical. Values may be float, BiomarkerValue, or dict with "value" key.
    Returns structured output with registry_version and derived dict.
    Never raises; missing inputs result in omitted entries or value None.

    Lab-supplied: if a derived marker already exists in panel with valid value, it is skipped.
    """
    result: Dict[str, Any] = {
        "registry_version": RatioRegistry.version,
        "derived": {},
    }

    # Lipid ratios
    tc = _numeric(panel.get("total_cholesterol"))
    hdl = _numeric(panel.get("hdl_cholesterol"))
    ldl = _numeric(panel.get("ldl_cholesterol"))
    tg = _numeric(panel.get("triglycerides"))
    glucose = _numeric(panel.get("glucose"))
    apob_val = _numeric(panel.get("apob"))
    apoa1_val = _numeric(panel.get("apoa1"))

    if _lab_supplied(panel, "tc_hdl_ratio"):
        v = _numeric(panel["tc_hdl_ratio"])
        result["derived"]["tc_hdl_ratio"] = {
            "value": v, "unit": "ratio", "source": "lab",
            "bounds_applied": False, "inputs_used": [],
        }
    else:
        tc_hdl = safe_ratio(tc, hdl)
        if tc_hdl is not None:
            result["derived"]["tc_hdl_ratio"] = {
                "value": round(tc_hdl, RATIO_PRECISION), "unit": "ratio", "source": "computed",
                "bounds_applied": True, "inputs_used": _DERIVED_INPUTS["tc_hdl_ratio"],
            }

    if _lab_supplied(panel, "tg_hdl_ratio"):
        v = _numeric(panel["tg_hdl_ratio"])
        result["derived"]["tg_hdl_ratio"] = {
            "value": v, "unit": "ratio", "source": "lab",
            "bounds_applied": False, "inputs_used": [],
        }
    else:
        tg_hdl = safe_ratio(tg, hdl)
        if tg_hdl is not None:
            result["derived"]["tg_hdl_ratio"] = {
                "value": round(tg_hdl, RATIO_PRECISION), "unit": "ratio", "source": "computed",
                "bounds_applied": True, "inputs_used": _DERIVED_INPUTS["tg_hdl_ratio"],
            }

    if _lab_supplied(panel, "ldl_hdl_ratio"):
        v = _numeric(panel["ldl_hdl_ratio"])
        result["derived"]["ldl_hdl_ratio"] = {
            "value": v, "unit": "ratio", "source": "lab",
            "bounds_applied": False, "inputs_used": [],
        }
    else:
        ldl_hdl = safe_ratio(ldl, hdl)
        if ldl_hdl is not None:
            result["derived"]["ldl_hdl_ratio"] = {
                "value": round(ldl_hdl, RATIO_PRECISION), "unit": "ratio", "source": "computed",
                "bounds_applied": True, "inputs_used": _DERIVED_INPUTS["ldl_hdl_ratio"],
            }

    if _lab_supplied(panel, "non_hdl_cholesterol"):
        v = _numeric(panel["non_hdl_cholesterol"])
        result["derived"]["non_hdl_cholesterol"] = {
            "value": v, "unit": "mmol/L", "source": "lab",
            "bounds_applied": False, "inputs_used": [],
        }
    elif tc is not None and hdl is not None:
        non_hdl = tc - hdl
        result["derived"]["non_hdl_cholesterol"] = {
            "value": round(non_hdl, NON_HDL_PRECISION), "unit": "mmol/L", "source": "computed",
            "bounds_applied": False, "inputs_used": _DERIVED_INPUTS["non_hdl_cholesterol"],
        }

    if _lab_supplied(panel, "apob_apoa1_ratio"):
        v = _numeric(panel["apob_apoa1_ratio"])
        result["derived"]["apob_apoa1_ratio"] = {
            "value": v, "unit": "ratio", "source": "lab",
            "bounds_applied": False, "inputs_used": [],
        }
    else:
        apo_ratio = safe_ratio(apob_val, apoa1_val)
        if apo_ratio is not None:
            result["derived"]["apob_apoa1_ratio"] = {
                "value": round(apo_ratio, RATIO_PRECISION), "unit": "ratio", "source": "computed",
                "bounds_applied": False, "inputs_used": _DERIVED_INPUTS["apob_apoa1_ratio"],
            }

    if _lab_supplied(panel, "remnant_cholesterol"):
        v = _numeric(panel["remnant_cholesterol"])
        result["derived"]["remnant_cholesterol"] = {
            "value": v, "unit": "mmol/L", "source": "lab",
            "bounds_applied": False, "inputs_used": [],
        }
    elif tc is not None and ldl is not None and hdl is not None:
        remnant = tc - ldl - hdl
        result["derived"]["remnant_cholesterol"] = {
            "value": round(max(remnant, 0.0), NON_HDL_PRECISION), "unit": "mmol/L", "source": "computed",
            "bounds_applied": False, "inputs_used": _DERIVED_INPUTS["remnant_cholesterol"],
        }

    insulin = _numeric(panel.get("insulin"))
    if _lab_supplied(panel, "homa_ir"):
        v = _numeric(panel["homa_ir"])
        result["derived"]["homa_ir"] = {
            "value": v, "unit": "ratio", "source": "lab",
            "bounds_applied": False, "inputs_used": [],
        }
    elif glucose is not None and insulin is not None:
        homa = (glucose * insulin) / 22.5
        result["derived"]["homa_ir"] = {
            "value": round(homa, RATIO_PRECISION), "unit": "ratio", "source": "computed",
            "bounds_applied": False, "inputs_used": _DERIVED_INPUTS["homa_ir"],
        }

    if _lab_supplied(panel, "fib_4"):
        v = _numeric(panel["fib_4"])
        result["derived"]["fib_4"] = {
            "value": v, "unit": "ratio", "source": "lab",
            "bounds_applied": False, "inputs_used": [],
        }
    else:
        # TODO(KB-S10): orchestrator must inject questionnaire-derived age for deterministic FIB-4.
        ast_for_fib4 = _numeric(panel.get("ast"))
        alt_for_fib4 = _numeric(panel.get("alt"))
        platelets_for_fib4 = _numeric(panel.get("platelets"))
        age = _numeric(panel.get("age"))
        if (
            age is not None
            and ast_for_fib4 is not None
            and platelets_for_fib4 is not None
            and alt_for_fib4 is not None
            and platelets_for_fib4 > 0
            and alt_for_fib4 > 0
        ):
            fib4 = (age * ast_for_fib4) / (platelets_for_fib4 * sqrt(alt_for_fib4))
            result["derived"]["fib_4"] = {
                "value": round(fib4, RATIO_PRECISION), "unit": "ratio", "source": "computed",
                "bounds_applied": False, "inputs_used": _DERIVED_INPUTS["fib_4"],
            }

    # TyG index (SI-native formulation; no runtime unit conversion)
    if _lab_supplied(panel, "tyg_index"):
        v = _numeric(panel["tyg_index"])
        result["derived"]["tyg_index"] = {
            "value": v, "unit": "ratio", "source": "lab",
            "bounds_applied": False, "inputs_used": [],
        }
    elif tg is not None and glucose is not None and tg > 0 and glucose > 0:
        tyg_index = log((tg * glucose * TYG_SI_CONSTANT) / 2.0)
        result["derived"]["tyg_index"] = {
            "value": round(tyg_index, RATIO_PRECISION), "unit": "ratio", "source": "computed",
            "bounds_applied": False, "inputs_used": _DERIVED_INPUTS["tyg_index"],
        }

    # TyG-BMI index = TyG * BMI; BMI retrieved directly from panel
    if _lab_supplied(panel, "tyg_bmi_index"):
        v = _numeric(panel["tyg_bmi_index"])
        result["derived"]["tyg_bmi_index"] = {
            "value": v, "unit": "ratio", "source": "lab",
            "bounds_applied": False, "inputs_used": [],
        }
    else:
        bmi = _numeric(panel.get("bmi"))
        tyg_entry = result["derived"].get("tyg_index", {})
        tyg_value = tyg_entry.get("value") if isinstance(tyg_entry, dict) else None
        if isinstance(tyg_value, (int, float)) and bmi is not None:
            tyg_bmi_index = float(tyg_value) * bmi
            result["derived"]["tyg_bmi_index"] = {
                "value": round(tyg_bmi_index, RATIO_PRECISION), "unit": "ratio", "source": "computed",
                "bounds_applied": False, "inputs_used": _DERIVED_INPUTS["tyg_bmi_index"],
            }

    # NLR
    neut = _numeric(panel.get("neutrophils"))
    lymph = _numeric(panel.get("lymphocytes"))
    if _lab_supplied(panel, "nlr"):
        v = _numeric(panel["nlr"])
        result["derived"]["nlr"] = {
            "value": v, "unit": "ratio", "source": "lab",
            "bounds_applied": False, "inputs_used": [],
        }
    else:
        nlr_val = safe_ratio(neut, lymph)
        if nlr_val is not None:
            result["derived"]["nlr"] = {
                "value": round(nlr_val, RATIO_PRECISION), "unit": "ratio", "source": "computed",
                "bounds_applied": False, "inputs_used": _DERIVED_INPUTS["nlr"],
            }

    # SII = (platelets * neutrophils) / lymphocytes
    platelets = _numeric(panel.get("platelets"))
    if _lab_supplied(panel, "sii"):
        v = _numeric(panel["sii"])
        result["derived"]["sii"] = {
            "value": v, "unit": "ratio", "source": "lab",
            "bounds_applied": False, "inputs_used": [],
        }
    elif (
        platelets is not None
        and neut is not None
        and lymph is not None
        and lymph > 0
    ):
        sii_val = (platelets * neut) / lymph
        result["derived"]["sii"] = {
            "value": round(sii_val, RATIO_PRECISION), "unit": "ratio", "source": "computed",
            "bounds_applied": False, "inputs_used": _DERIVED_INPUTS["sii"],
        }

    # Urea/creatinine
    urea = _numeric(panel.get("urea"))
    creat = _numeric(panel.get("creatinine"))
    if _lab_supplied(panel, "urea_creatinine_ratio") or _lab_supplied(panel, "bun_creatinine_ratio"):
        ratio_key = "urea_creatinine_ratio" if _lab_supplied(panel, "urea_creatinine_ratio") else "bun_creatinine_ratio"
        v = _numeric(panel[ratio_key])
        result["derived"]["urea_creatinine_ratio"] = {
            "value": v, "unit": "ratio", "source": "lab",
            "bounds_applied": False, "inputs_used": [],
        }
    else:
        bc_ratio = safe_ratio(urea, creat)
        if bc_ratio is not None:
            result["derived"]["urea_creatinine_ratio"] = {
                "value": round(bc_ratio, RATIO_PRECISION), "unit": "ratio", "source": "computed",
                "bounds_applied": False, "inputs_used": _DERIVED_INPUTS["urea_creatinine_ratio"],
            }

    # AST/ALT
    ast_val = _numeric(panel.get("ast"))
    alt_val = _numeric(panel.get("alt"))
    if _lab_supplied(panel, "ast_alt_ratio"):
        v = _numeric(panel["ast_alt_ratio"])
        result["derived"]["ast_alt_ratio"] = {
            "value": v, "unit": "ratio", "source": "lab",
            "bounds_applied": False, "inputs_used": [],
        }
    else:
        ast_alt = safe_ratio(ast_val, alt_val)
        if ast_alt is not None:
            result["derived"]["ast_alt_ratio"] = {
                "value": round(ast_alt, RATIO_PRECISION), "unit": "ratio", "source": "computed",
                "bounds_applied": False, "inputs_used": _DERIVED_INPUTS["ast_alt_ratio"],
            }

    # Testosterone / Free Testosterone ratio (lab-supplied or computed)
    test_total = _numeric(panel.get("testosterone"))
    test_free = _numeric(panel.get("free_testosterone"))
    if _lab_supplied(panel, "testosterone_free_testosterone_ratio"):
        v = _numeric(panel["testosterone_free_testosterone_ratio"])
        result["derived"]["testosterone_free_testosterone_ratio"] = {
            "value": v, "unit": "ratio", "source": "lab",
            "bounds_applied": False, "inputs_used": [],
        }
    else:
        tf_ratio = safe_ratio(test_total, test_free)
        if tf_ratio is not None:
            result["derived"]["testosterone_free_testosterone_ratio"] = {
                "value": round(tf_ratio, RATIO_PRECISION), "unit": "ratio", "source": "computed",
                "bounds_applied": False, "inputs_used": _DERIVED_INPUTS["testosterone_free_testosterone_ratio"],
            }

    return result


def compute_legacy(panel: Dict[str, Any]) -> Dict[str, Optional[float]]:
    """
    Legacy flat {id: value} output for backwards compatibility with orchestrator.
    Orchestrator will migrate to structured compute() output.
    """
    structured = compute(panel)
    out: Dict[str, Optional[float]] = {rid: None for rid in DERIVED_IDS}
    for rid, entry in structured.get("derived", {}).items():
        if isinstance(entry, dict) and "value" in entry:
            out[rid] = entry["value"]
    return out
