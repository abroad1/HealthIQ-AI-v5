"""
Derived Ratio Registry — centralised deterministic ratio computation.

Sprint 4 (Derived Ratio Registry). PRD §3.4, §4.5.
Sprint 5: Extended with nlr, bun_creatinine_ratio, ast_alt_ratio; structured output.
All derived ratios computed here; insights must not compute ratios locally.
Runs after unit normalisation; uses base-unit values only.
"""

from typing import Dict, Optional, Any, List

from core.analytics.primitives import safe_ratio


class RatioRegistry:
    """Centralised ratio computation. Sprint 4/5."""

    version = "1.1.0"

# Ratio precision: 3 decimal places for dimensionless ratios
RATIO_PRECISION = 3
# non_hdl_cholesterol uses concentration unit (mmol/L); 2 dp sufficient
NON_HDL_PRECISION = 2

# All derived markers (order: lipid first, then others)
DERIVED_IDS = (
    "tc_hdl_ratio", "tg_hdl_ratio", "ldl_hdl_ratio", "non_hdl_cholesterol", "apoB_apoA1_ratio",
    "nlr", "bun_creatinine_ratio", "ast_alt_ratio",
)
RATIO_IDS = DERIVED_IDS  # Backwards compatibility

# Input biomarkers per derived marker
_DERIVED_INPUTS: Dict[str, List[str]] = {
    "tc_hdl_ratio": ["total_cholesterol", "hdl_cholesterol"],
    "tg_hdl_ratio": ["triglycerides", "hdl_cholesterol"],
    "ldl_hdl_ratio": ["ldl_cholesterol", "hdl_cholesterol"],
    "non_hdl_cholesterol": ["total_cholesterol", "hdl_cholesterol"],
    "apoB_apoA1_ratio": ["apob", "apoa1"],
    "nlr": ["neutrophils", "lymphocytes"],
    "bun_creatinine_ratio": ["bun", "creatinine"],
    "ast_alt_ratio": ["ast", "alt"],
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

    if _lab_supplied(panel, "apoB_apoA1_ratio"):
        v = _numeric(panel["apoB_apoA1_ratio"])
        result["derived"]["apoB_apoA1_ratio"] = {
            "value": v, "unit": "ratio", "source": "lab",
            "bounds_applied": False, "inputs_used": [],
        }
    else:
        apo_ratio = safe_ratio(apob_val, apoa1_val)
        if apo_ratio is not None:
            result["derived"]["apoB_apoA1_ratio"] = {
                "value": round(apo_ratio, RATIO_PRECISION), "unit": "ratio", "source": "computed",
                "bounds_applied": False, "inputs_used": _DERIVED_INPUTS["apoB_apoA1_ratio"],
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

    # BUN/creatinine
    bun = _numeric(panel.get("bun"))
    creat = _numeric(panel.get("creatinine"))
    if _lab_supplied(panel, "bun_creatinine_ratio"):
        v = _numeric(panel["bun_creatinine_ratio"])
        result["derived"]["bun_creatinine_ratio"] = {
            "value": v, "unit": "ratio", "source": "lab",
            "bounds_applied": False, "inputs_used": [],
        }
    else:
        bc_ratio = safe_ratio(bun, creat)
        if bc_ratio is not None:
            result["derived"]["bun_creatinine_ratio"] = {
                "value": round(bc_ratio, RATIO_PRECISION), "unit": "ratio", "source": "computed",
                "bounds_applied": False, "inputs_used": _DERIVED_INPUTS["bun_creatinine_ratio"],
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
