"""
ARCH-CONV-PKGC-1 — governed waist-unit historic remediation (MARK_STALE_NO_REWRITE).

Does not rewrite historic waist values/units. Stamps processing_metadata only.
Live DB write is operator-gated; this module is the deterministic planner/applier.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any, Dict, List, Mapping, MutableMapping, Optional, Sequence, Tuple

WORK_ID = "ARCH-CONV-PKGC-1"
STALE_REASON = "legacy_waist_unit_defect:used_incorrectly"
DISPOSITION = "MARK_STALE_NO_REWRITE"
REMEDIATION_META_KEY = "arch_conv_pkgc_1_waist_remediation"
CLIENT_RESULT_SHAPE_V1 = "client_result_shape_v1"

# Anthony-approved exact set (ARCH-CONV-PKGC-1-DATA-GOV-ANTHONY-2026-08-02).
APPROVED_ANALYSIS_IDS: Tuple[str, ...] = (
    "e5cfbc62-93fa-4bac-8894-dcb69117ac4c",
    "02df9062-eba8-4df1-8072-8d2182aca35d",
    "7fc35b86-15c2-4d76-843a-e964263be0b7",
    "a3244490-dd74-4922-a1c6-49a25c1f6604",
    "7f780514-d288-4331-8020-8866744b70ae",
    "ad721d67-f2e8-4942-8450-8598b8e35343",
    "7cc8b2d5-c8f0-4138-ba18-8540eece06a1",
    "91046b62-114f-44a3-a2ab-2b885ea5782b",
    "7b8c58b5-191f-41e7-8fe4-a66938bb0a98",
    "e3a1ee79-963e-46a1-afee-58657d1ffb55",
    "7aacc734-95cf-4ea5-a19c-0d03d98dd2e9",
    "d7417288-7e11-48da-8716-d0f63f77c491",
)
APPROVED_ANALYSIS_ID_SET = frozenset(APPROVED_ANALYSIS_IDS)

# Audit original bare values — Phase 0 precondition for live verify.
AUDIT_ORIGINAL_VALUES: Dict[str, float] = {
    "e5cfbc62-93fa-4bac-8894-dcb69117ac4c": 77.0,
    "02df9062-eba8-4df1-8072-8d2182aca35d": 77.0,
    "7fc35b86-15c2-4d76-843a-e964263be0b7": 77.0,
    "a3244490-dd74-4922-a1c6-49a25c1f6604": 60.0,
    "7f780514-d288-4331-8020-8866744b70ae": 67.0,
    "ad721d67-f2e8-4942-8450-8598b8e35343": 75.0,
    "7cc8b2d5-c8f0-4138-ba18-8540eece06a1": 78.0,
    "91046b62-114f-44a3-a2ab-2b885ea5782b": 78.0,
    "7b8c58b5-191f-41e7-8fe4-a66938bb0a98": 78.0,
    "e3a1ee79-963e-46a1-afee-58657d1ffb55": 78.0,
    "7aacc734-95cf-4ea5-a19c-0d03d98dd2e9": 76.0,
    "d7417288-7e11-48da-8716-d0f63f77c491": 22.0,
}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def extract_waist_circumference(questionnaire_data: Any) -> Any:
    if not isinstance(questionnaire_data, Mapping):
        return None
    return questionnaire_data.get("waist_circumference")


def remediation_stamp_from_meta(meta: Any) -> Optional[Dict[str, Any]]:
    if not isinstance(meta, Mapping):
        return None
    stamp = meta.get(REMEDIATION_META_KEY)
    return dict(stamp) if isinstance(stamp, Mapping) else None


def has_pkgc1_remediation_stamp(stored: Mapping[str, Any]) -> bool:
    meta = stored.get("meta") if isinstance(stored.get("meta"), Mapping) else {}
    stamp = remediation_stamp_from_meta(meta)
    if stamp and str(stamp.get("work_id") or "") == WORK_ID:
        return True
    # Also accept top-level processing_metadata companion when passed as stored.
    top = remediation_stamp_from_meta(stored)
    return bool(top and str(top.get("work_id") or "") == WORK_ID)


def build_remediation_stamp(
    *,
    analysis_id: str,
    actor: str = "cursor_arch_conv_pkgc_1",
    timestamp_utc: Optional[str] = None,
) -> Dict[str, Any]:
    return {
        "work_id": WORK_ID,
        "decision_id": "ARCH-CONV-PKGC-1-DATA-GOV-ANTHONY-2026-08-02",
        "disposition": DISPOSITION,
        "stale_reason": STALE_REASON,
        "analysis_id": analysis_id,
        "original_preserved": True,
        "value_rewritten": False,
        "unit_rewritten": False,
        "reversible": True,
        "actor": actor,
        "timestamp_utc": timestamp_utc or utc_now_iso(),
    }


def apply_mark_stale_no_rewrite(
    processing_metadata: Optional[Mapping[str, Any]],
    *,
    analysis_id: str,
    actor: str = "cursor_arch_conv_pkgc_1",
    timestamp_utc: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Return a new processing_metadata dict with remediation stamp.
    Does not alter questionnaire or biomarker values.
    """
    out: Dict[str, Any] = deepcopy(dict(processing_metadata or {}))
    stamp = build_remediation_stamp(
        analysis_id=analysis_id,
        actor=actor,
        timestamp_utc=timestamp_utc,
    )
    out[REMEDIATION_META_KEY] = stamp

    client = out.get(CLIENT_RESULT_SHAPE_V1)
    if isinstance(client, Mapping):
        client_out = deepcopy(dict(client))
        meta = dict(client_out.get("meta") or {}) if isinstance(client_out.get("meta"), Mapping) else {}
        meta[REMEDIATION_META_KEY] = stamp
        client_out["meta"] = meta
        # Ensure analysis_id present for stale-rule allowlist detection on DTO reads.
        if not str(client_out.get("analysis_id") or "").strip():
            client_out["analysis_id"] = analysis_id
        out[CLIENT_RESULT_SHAPE_V1] = client_out
    return out


def evaluate_row_precondition(
    *,
    analysis_id: str,
    exists: bool,
    questionnaire_data: Any = None,
    processing_metadata: Any = None,
    already_superseded: bool = False,
) -> Dict[str, Any]:
    """Fail-closed precondition evaluation for one approved ID."""
    before = {
        "exists": exists,
        "waist_circumference": extract_waist_circumference(questionnaire_data),
        "has_remediation_stamp": False,
        "already_superseded": already_superseded,
    }
    if analysis_id not in APPROVED_ANALYSIS_ID_SET:
        return {
            "analysis_id": analysis_id,
            "precondition": "FAIL_UNKNOWN_ID",
            "action": "NONE",
            "success": False,
            "before": before,
            "after": None,
            "stale_reason": STALE_REASON,
            "audit_reference": None,
            "error": "analysis_id not in approved set",
        }
    if not exists:
        return {
            "analysis_id": analysis_id,
            "precondition": "FAIL_MISSING",
            "action": "NONE",
            "success": False,
            "before": before,
            "after": None,
            "stale_reason": STALE_REASON,
            "audit_reference": None,
            "error": "analysis row missing",
        }
    if already_superseded:
        return {
            "analysis_id": analysis_id,
            "precondition": "FAIL_SUPERSEDED",
            "action": "NONE",
            "success": False,
            "before": before,
            "after": None,
            "stale_reason": STALE_REASON,
            "audit_reference": None,
            "error": "row superseded",
        }

    pm = processing_metadata if isinstance(processing_metadata, Mapping) else {}
    client = pm.get(CLIENT_RESULT_SHAPE_V1) if isinstance(pm.get(CLIENT_RESULT_SHAPE_V1), Mapping) else {}
    stamped = has_pkgc1_remediation_stamp(pm) or (
        isinstance(client, Mapping) and has_pkgc1_remediation_stamp(client)
    )
    before["has_remediation_stamp"] = stamped
    if stamped:
        return {
            "analysis_id": analysis_id,
            "precondition": "ALREADY_REMEDIATED",
            "action": "NO_OP_IDEMPOTENT",
            "success": True,
            "before": before,
            "after": before,
            "stale_reason": STALE_REASON,
            "audit_reference": REMEDIATION_META_KEY,
            "error": None,
        }

    waist = extract_waist_circumference(questionnaire_data)
    expected = AUDIT_ORIGINAL_VALUES.get(analysis_id)
    # Precondition: bare numeric waist matching audit original (Phase 0).
    if not isinstance(waist, (int, float)) or isinstance(waist, bool):
        return {
            "analysis_id": analysis_id,
            "precondition": "FAIL_PRECONDITION_WAIST_SHAPE",
            "action": "NONE",
            "success": False,
            "before": before,
            "after": None,
            "stale_reason": STALE_REASON,
            "audit_reference": None,
            "error": "waist_circumference is not a bare numeric (precondition mismatch)",
        }
    if expected is not None and float(waist) != float(expected):
        return {
            "analysis_id": analysis_id,
            "precondition": "FAIL_PRECONDITION_VALUE_MISMATCH",
            "action": "NONE",
            "success": False,
            "before": before,
            "after": None,
            "stale_reason": STALE_REASON,
            "audit_reference": None,
            "error": f"waist value {waist} != audit original {expected}",
        }

    return {
        "analysis_id": analysis_id,
        "precondition": "PASS",
        "action": DISPOSITION,
        "success": True,
        "before": before,
        "after": None,  # filled by planner/applier
        "stale_reason": STALE_REASON,
        "audit_reference": REMEDIATION_META_KEY,
        "error": None,
    }


def plan_remediation(
    rows: Sequence[Mapping[str, Any]],
    *,
    timestamp_utc: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Dry-run planner.

    Each row mapping must include:
      analysis_id, exists, questionnaire_data?, processing_metadata?, already_superseded?
    """
    ts = timestamp_utc or utc_now_iso()
    results: List[Dict[str, Any]] = []
    seen: List[str] = []

    for row in rows:
        aid = str(row.get("analysis_id") or "").strip()
        seen.append(aid)
        evaluated = evaluate_row_precondition(
            analysis_id=aid,
            exists=bool(row.get("exists")),
            questionnaire_data=row.get("questionnaire_data"),
            processing_metadata=row.get("processing_metadata"),
            already_superseded=bool(row.get("already_superseded")),
        )
        if evaluated["precondition"] == "PASS":
            new_pm = apply_mark_stale_no_rewrite(
                row.get("processing_metadata") if isinstance(row.get("processing_metadata"), Mapping) else {},
                analysis_id=aid,
                timestamp_utc=ts,
            )
            evaluated["after"] = {
                "exists": True,
                "waist_circumference": extract_waist_circumference(row.get("questionnaire_data")),
                "has_remediation_stamp": True,
                "value_rewritten": False,
                "unit_rewritten": False,
                "processing_metadata_stamp": new_pm.get(REMEDIATION_META_KEY),
            }
            evaluated["planned_processing_metadata"] = new_pm
        results.append(evaluated)

    unexpected = [x for x in seen if x and x not in APPROVED_ANALYSIS_ID_SET]
    missing_from_input = [x for x in APPROVED_ANALYSIS_IDS if x not in seen]
    hard_failures = [
        r
        for r in results
        if not r.get("success")
        or str(r.get("precondition") or "").startswith("FAIL_")
    ]
    # ALREADY_REMEDIATED counts as success idempotent, not hard failure.
    hard_failures = [r for r in results if r.get("precondition", "").startswith("FAIL_")]

    return {
        "work_id": WORK_ID,
        "mode": "dry_run",
        "timestamp_utc": ts,
        "approved_count": len(APPROVED_ANALYSIS_IDS),
        "input_count": len(seen),
        "unexpected_ids": unexpected,
        "missing_approved_ids": missing_from_input,
        "fail_closed": bool(unexpected or missing_from_input or hard_failures),
        "results": results,
        "summary": {
            "pass_ready": sum(1 for r in results if r.get("precondition") == "PASS"),
            "already_remediated": sum(
                1 for r in results if r.get("precondition") == "ALREADY_REMEDIATED"
            ),
            "failed": len(hard_failures),
        },
    }


def apply_planned_remediation(
    plan: Mapping[str, Any],
    *,
    write: bool = False,
) -> Dict[str, Any]:
    """
    Apply a previously computed plan.

    When write=False, returns the plan annotated as dry_run (no mutation claim).
    When write=True, refuses if plan.fail_closed is true.
    """
    out = deepcopy(dict(plan))
    if out.get("fail_closed"):
        out["mode"] = "write_refused" if write else "dry_run"
        out["write_executed"] = False
        out["complete_success"] = False
        out["error"] = "fail_closed: unexpected set, missing IDs, or precondition failures"
        return out

    if not write:
        out["mode"] = "dry_run"
        out["write_executed"] = False
        out["complete_success"] = False
        out["note"] = "dry-run only; no database mutation"
        return out

    # Write mode: caller persists planned_processing_metadata per PASS row.
    out["mode"] = "write"
    out["write_executed"] = True
    out["complete_success"] = True
    out["rows_to_persist"] = [
        {
            "analysis_id": r["analysis_id"],
            "processing_metadata": r.get("planned_processing_metadata"),
        }
        for r in out.get("results") or []
        if r.get("precondition") == "PASS" and r.get("planned_processing_metadata")
    ]
    return out
