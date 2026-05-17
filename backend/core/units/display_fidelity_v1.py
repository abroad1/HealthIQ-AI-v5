"""
LC-S8G — Uploaded-unit display fidelity for Layer C biomarker rows.

Populates display_* fields from pre-normalisation upload_panel_observations while
keeping value/unit/reference_range as Layer B analytical canonical fields.
No conversions performed here — only selects governed upload source rows.
"""

from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional, Tuple

from core.canonical.alias_registry_service import get_alias_registry_service
from core.units.display_policy import get_biomarker_display_policy
from core.units.registry import (
    UnitRegistry,
    _units_equivalent,
    value_and_reference_units_coherent_for_numeric_compare,
)

_SKIP_UPLOAD_KEYS = frozenset({"__unit_normalisation_meta__"})


def _normalize_unit_token(unit: str) -> str:
    return (unit or "").lower().replace(" ", "").replace("µ", "u").replace("μ", "u")


def _parse_upload_observation(raw: Any) -> Optional[Dict[str, Any]]:
    if not isinstance(raw, dict):
        return None
    val = raw.get("value", raw.get("measurement"))
    if not isinstance(val, (int, float)):
        return None
    unit = str(raw.get("unit") or "").strip()
    if not unit:
        return None
    ref_raw = raw.get("reference_range") or raw.get("referenceRange")
    ref_out: Optional[Dict[str, Any]] = None
    if isinstance(ref_raw, dict):
        ref_out = {
            "min": ref_raw.get("min"),
            "max": ref_raw.get("max"),
            "unit": str(ref_raw.get("unit") or unit).strip() or unit,
            "source": ref_raw.get("source", "lab"),
        }
    return {"value": float(val), "unit": unit, "reference_range": ref_out}


def _canonical_id_for_upload_key(key: str) -> Optional[str]:
    alias = get_alias_registry_service()
    try:
        cid = str(alias.resolve(key)).strip()
    except Exception:
        return None
    if not cid or cid.startswith("unmapped_"):
        return None
    return cid


def _equivalent_upload_keys(canonical_id: str) -> List[str]:
    keys: List[str] = [canonical_id]
    policy = get_biomarker_display_policy(canonical_id)
    if policy:
        uploaded = policy.get("uploaded_panel_fidelity") or {}
        equiv = uploaded.get("equivalent_canonical_ids")
        if isinstance(equiv, list):
            for alt in equiv:
                if isinstance(alt, str) and alt.strip():
                    keys.append(alt.strip())
    if canonical_id == "hba1c":
        keys.append("hba1c_pct")
    return keys


def _select_upload_source(
    canonical_id: str,
    upload_panel: Mapping[str, Any],
    registry: UnitRegistry,
) -> Optional[Dict[str, Any]]:
    """Pick the governed upload observation row for display (pre-normalisation payload)."""
    candidates: List[Tuple[str, Dict[str, Any]]] = []
    for key, raw in upload_panel.items():
        if key in _SKIP_UPLOAD_KEYS or str(key).startswith("unmapped_"):
            continue
        cid = _canonical_id_for_upload_key(str(key))
        if cid != canonical_id:
            continue
        parsed = _parse_upload_observation(raw)
        if parsed:
            candidates.append((str(key), parsed))

    if not candidates:
        return None

    by_key = {k: obs for k, obs in candidates}
    if canonical_id in by_key:
        return by_key[canonical_id]

    base_unit = registry.get_base_unit(canonical_id)
    for prefer_key in _equivalent_upload_keys(canonical_id):
        if prefer_key in by_key and _units_equivalent(by_key[prefer_key]["unit"], base_unit):
            return by_key[prefer_key]

    return candidates[0][1]


def _ref_dict(
    ref: Optional[Dict[str, Any]],
    fallback_unit: str,
) -> Dict[str, Any]:
    if isinstance(ref, dict):
        return {
            "min": ref.get("min"),
            "max": ref.get("max"),
            "unit": str(ref.get("unit") or fallback_unit).strip() or fallback_unit,
            "source": ref.get("source", "lab"),
        }
    return {
        "min": None,
        "max": None,
        "unit": fallback_unit,
        "source": "lab",
    }


def _upload_safe_for_display(
    canonical_id: str,
    upload_obs: Dict[str, Any],
    analytical_unit: str,
    registry: UnitRegistry,
) -> bool:
    upload_unit = str(upload_obs.get("unit") or "").strip()
    if not upload_unit:
        return False
    if _units_equivalent(upload_unit, analytical_unit):
        return True
    return value_and_reference_units_coherent_for_numeric_compare(
        canonical_id, upload_unit, analytical_unit, registry=registry
    )


def enrich_biomarker_row_display_fields(
    row: Dict[str, Any],
    *,
    upload_panel: Optional[Mapping[str, Any]],
    registry: Optional[UnitRegistry] = None,
) -> Dict[str, Any]:
    """Add display_* and analytical_* fields to an API biomarker row dict."""
    out = dict(row)
    reg = registry or UnitRegistry()
    canonical_id = str(out.get("biomarker_name") or "").strip()
    if not canonical_id:
        return out

    analytical_value = out.get("value")
    analytical_unit = str(out.get("unit") or "").strip()
    analytical_ref = out.get("reference_range")
    if isinstance(analytical_ref, dict):
        analytical_ref_payload = dict(analytical_ref)
    else:
        analytical_ref_payload = _ref_dict(None, analytical_unit)

    out["analytical_value"] = analytical_value
    out["analytical_unit"] = analytical_unit
    out["analytical_reference_range"] = analytical_ref_payload

    upload_panel = upload_panel or {}
    upload_obs = _select_upload_source(canonical_id, upload_panel, reg)

    if upload_obs and _upload_safe_for_display(canonical_id, upload_obs, analytical_unit, reg):
        display_value = upload_obs["value"]
        display_unit = upload_obs["unit"]
        upload_ref = upload_obs.get("reference_range")
        display_ref = (
            _ref_dict(upload_ref, display_unit)
            if isinstance(upload_ref, dict)
            else _ref_dict(None, display_unit)
        )
        same_unit = _normalize_unit_token(display_unit) == _normalize_unit_token(analytical_unit)
        same_value = (
            isinstance(analytical_value, (int, float))
            and abs(float(display_value) - float(analytical_value)) < 1e-6
        )
        display_is_uploaded = not (same_unit and same_value)
    else:
        display_value = analytical_value
        display_unit = analytical_unit
        display_ref = analytical_ref_payload
        display_is_uploaded = False

    out["display_value"] = display_value
    out["display_unit"] = display_unit
    out["display_reference_range"] = display_ref
    out["display_is_uploaded_unit"] = display_is_uploaded
    if display_is_uploaded and analytical_unit:
        out["analytical_transparency_unit"] = analytical_unit
    else:
        out.pop("analytical_transparency_unit", None)

    return out


def enrich_biomarker_rows_with_display_fields(
    rows: List[Dict[str, Any]],
    upload_panel: Optional[Mapping[str, Any]],
    *,
    registry: Optional[UnitRegistry] = None,
) -> List[Dict[str, Any]]:
    reg = registry or UnitRegistry()
    panel = upload_panel or {}
    return [enrich_biomarker_row_display_fields(r, upload_panel=panel, registry=reg) for r in rows]
