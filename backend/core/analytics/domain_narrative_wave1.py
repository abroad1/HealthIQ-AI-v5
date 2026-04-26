"""
D-2 — Wave 1 consumer narrative assembly (Strategy A).

Deterministic only: IDL (published bundle + idl_registry static text), D-1 bands/tiers,
signal ids, and optional narrative_report / insight recommendations. No LLM.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Set, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from core.contracts.interpretation_display_layer_v1 import InterpretationDisplayRecordV1

# IDs in idl_records_v1.yaml (governed)
_ID_VASCULAR = "ph_vascular_hcy_inflammation_v1"
_ID_LIPID = "ph_lipid_residual_ldl_favourable_transport_v1"
_ID_HBA1C = "ph_hba1c_metabolic_stress_v1"
_ID_IR = "ph_metabolic_early_ir_v1"
_ID_HEP = "ph_hepatic_alt_inflammatory_v1"

_CV_SIGNAL_PRIORITY: List[str] = [
    "signal_lipid_transport_dysfunction",
    "signal_ldl_cholesterol_high",
    "signal_hdl_cholesterol_low",
    "signal_triglycerides_high",
    "signal_homocysteine_elevation",
    "signal_total_cholesterol_high",
]


def governed_idl_field(internal_id: str, field: str) -> str:
    """Read authoritative idl_registry field (stays in sync with publish)."""
    from core.analytics.interpretation_display_layer_publish_v1 import load_idl_registry_document

    _, rows = load_idl_registry_document()
    for row in rows:
        if not isinstance(row, dict):
            continue
        if str(row.get("internal_id", "")).strip() != internal_id:
            continue
        return str(row.get(field, "")).strip()
    return ""


def idl_record(
    records_by_id: Dict[str, Any],
    internal_id: str,
) -> Optional["InterpretationDisplayRecordV1"]:
    from core.contracts.interpretation_display_layer_v1 import InterpretationDisplayRecordV1

    r = records_by_id.get(internal_id)
    if r is None or not isinstance(r, InterpretationDisplayRecordV1):
        return None
    return r


def idl_records_index(bundle: Any) -> Dict[str, Any]:
    if bundle is None or not hasattr(bundle, "records"):
        return {}
    return {r.internal_id: r for r in bundle.records}


def headline_cv(band: str) -> str:
    if band == "strong":
        return "Your cardiovascular health looks strong based on your current blood results."
    if band == "stable":
        return "Your cardiovascular health looks broadly stable based on your current results."
    if band == "watch":
        return "Your cardiovascular health shows some signals worth watching in your current results."
    return "Your cardiovascular health shows patterns that deserve closer review."


def headline_met(band: str) -> str:
    if band == "strong":
        return "Your blood sugar control looks strong based on your current results."
    if band == "stable":
        return "Your blood sugar control looks broadly stable based on your current results."
    if band == "watch":
        return "Your blood sugar control shows some signals worth watching."
    return "Your blood sugar control shows a pattern that deserves closer review."


def headline_liv(band: str) -> str:
    if band == "strong":
        return "Your liver health looks strong based on your current enzyme markers."
    if band == "stable":
        return "Your liver health looks broadly stable based on your current enzyme markers."
    if band == "watch":
        return "Your liver enzyme pattern shows some signals worth watching."
    return "Your liver enzyme pattern shows a pattern that deserves closer review."


def _narrative_lowercased(contributor: str, consequence: str) -> str:
    return f"{contributor or ''} {consequence or ''}".strip().lower()


def _cv_story_conflicts_with_stable_headline(contributor: str, consequence: str) -> bool:
    """
    D-4: True when a \"stable\" band would read as false reassurance against contributor/consequence.
    """
    t = _narrative_lowercased(contributor, consequence)
    if not t:
        return False
    needles = (
        "homocysteine",
        "vascular",
        "inflammation",
        "atherogenic",
        "accumulat",
        "warrant",
        "warrants",
        "review",
        "strain",
        "adverse",
        "stress",
        "atheroscler",
        "atherosclerosis",
        "ldl is above",
        "triglycerides are elevated",
        "hdl is below",
    )
    return any(n in t for n in needles)


def _met_story_conflicts_with_stable_headline(contributor: str, consequence: str) -> bool:
    t = _narrative_lowercased(contributor, consequence)
    if not t:
        return False
    needles = (
        "glyc",
        "insulin",
        "resistance",
        "impaired",
        "hba1c",
        "strain",
        "glucose",
        "sugar",
        "metabolic stress",
        "triglyceride",
        "sustained",
        "prediabet",
        "diabet",
    )
    return any(n in t for n in needles)


def headline_cv_coherent(band: str, contributor: str, consequence: str) -> str:
    """
    D-4: When band is \"stable\" but the underlying lines imply active context, avoid \"broadly stable\".
    """
    if band == "stable" and _cv_story_conflicts_with_stable_headline(contributor, consequence):
        return (
            "Your cardiovascular results do not read as a simple all-clear: some markers look reassuring "
            "while others add context that is worth discussing with a clinician."
        )
    return headline_cv(band)


def headline_met_coherent(band: str, contributor: str, consequence: str) -> str:
    if band == "stable" and _met_story_conflicts_with_stable_headline(contributor, consequence):
        return (
            "Your blood sugar and metabolic read is mixed on this panel — it is not a clean "
            "all-stable story; several markers shape the pattern together."
        )
    return headline_met(band)


def confidence_sentence_cv_coherent(tier: str, contributor: str) -> str:
    """
    D-4: Bridge lipid-tier confidence with homocysteine-led story when both appear in the same card.
    """
    t = tier if tier in ("high", "medium", "low") else "medium"
    c = (contributor or "").lower()
    if "homocysteine" in c and t != "high":
        if t == "medium":
            return (
                "Confidence is good for the lipid data you have; where homocysteine is elevated, "
                "it is read in the same vascular picture as those lipids, not as a second headline score."
            )
        return (
            "Confidence is limited by an incomplete lipid picture; where homocysteine is elevated, "
            "it is still interpreted with the markers available on this panel, not to inflate certainty."
        )
    return confidence_sentence_for(t, "cv")


def evidence_anchor_sentence(
    domain: str,
    by_id: Dict[str, Any],
    primary_idl_id: Optional[str],
) -> str:
    """D-4: one-line collapsed traceability — primary IDL retail label, else a safe domain fallback."""
    if primary_idl_id:
        rec = idl_record(by_id, primary_idl_id)
        if rec is not None and (rec.retail_display_label or "").strip():
            return f"Based mainly on: {str(rec.retail_display_label).strip()}"
    if domain == "cv":
        return "Based mainly on: your cardiovascular signals and patterns on this panel."
    if domain == "met":
        return "Based mainly on: your blood sugar and metabolic markers on this panel."
    return "Based mainly on: your liver-related markers on this panel."


def confidence_sentence_for(tier: str, domain: str) -> str:
    t = tier if tier in ("high", "medium", "low") else "medium"
    if domain == "cv":
        if t == "high":
            return (
                "Confidence is high — your full lipid picture including derived ratios supports "
                "a complete cardiovascular read."
            )
        if t == "medium":
            return (
                "Confidence is good — core lipid markers are present; some transport markers could "
                "still add detail."
            )
        return (
            "Confidence is limited — a fuller lipid panel and ratios would improve this picture."
        )
    if domain == "met":
        if t == "high":
            return (
                "Confidence is high — key glycaemic markers and related indices are available."
            )
        if t == "medium":
            return (
                "Confidence is moderate — some markers (for example insulin or triglycerides) "
                "could still refine the read."
            )
        return "Confidence is limited — additional glycaemic markers would strengthen the read."
    # liver
    if t == "high":
        return "Confidence is high — several liver function markers are present in this panel."
    if t == "medium":
        return (
            "Confidence is moderate — key enzymes are present; a fuller LFT would add context."
        )
    return (
        "Confidence is limited — a fuller liver function panel (including GGT, ALP, albumin) "
        "would improve the read."
    )


def _is_hcy(sid: str) -> bool:
    return "homocysteine" in (sid or "").lower()


def _is_lipid_dominant(sids: Set[str], rows: List[Dict[str, Any]]) -> bool:
    """Lipid signals active without hcy as dominant gap path."""
    sids_l = {str(x) for x in sids}
    has_lip = any("ldl" in s or "hdl" in s or "triglycer" in s or "lipid" in s for s in sids_l)
    has_hcy = any(_is_hcy(s) for s in sids_l) or any(
        _is_hcy(str(r.get("signal_id", ""))) for r in rows if _active(r)
    )
    return has_lip and not has_hcy


def _active(r: Dict[str, Any]) -> bool:
    return str(r.get("signal_state", "")) in ("at_risk", "suboptimal")


def cv_contributor(
    by_id: Dict[str, Any],
    active_sids: List[str],
    sig_rows: List[Dict[str, Any]],
) -> str:
    for pid in (_ID_VASCULAR, _ID_LIPID):
        rec = idl_record(by_id, pid)
        if rec is not None and rec.severity_state != "not_observed" and rec.enabled_for_frontend:
            if rec.subtitle:
                return rec.subtitle.strip()
    sset = set(active_sids)
    for pref in _CV_SIGNAL_PRIORITY:
        if any(s.startswith(pref) or s == pref for s in sset):
            return governed_signal_line(pref, "cv")
    if any("homocysteine" in s for s in sset):
        g = governed_idl_field(_ID_VASCULAR, "subtitle")
        if g:
            return g
    for r in sig_rows:
        if not _active(r):
            continue
        sid = str(r.get("signal_id", ""))
        if any(sid.startswith(p) for p in _CV_SIGNAL_PRIORITY):
            return governed_signal_line(sid, "cv")
    return "Your key cardiovascular markers are within their reference ranges."


def governed_signal_line(signal_id: str, domain: str) -> str:
    """Narrow, non-diagnostic one-liners tied to known pattern ids (D-2)."""
    s = (signal_id or "").strip()
    if domain == "cv":
        if "ldl" in s and "high" in s:
            return "LDL is above the optimal range, adding to long-term atherogenic exposure in context."
        if "hdl" in s and "low" in s:
            return "HDL is below the optimal range, reducing the protective part of the lipid picture."
        if "triglycer" in s and "high" in s:
            return "Triglycerides are elevated, relevant to particle load and insulin resistance context."
        if "lipid_transport" in s or "non_hdl" in s:
            return "The lipid transport pattern suggests atherogenic load beyond a single value."
        if "homocysteine" in s:
            return "Homocysteine is elevated, adding a vascular-stress context alongside the lipid picture."
        if "total_cholesterol" in s and "high" in s:
            return "Total cholesterol is above the optimal range, though transport context also matters."
    if domain == "met":
        if "hba1c" in s:
            return "HbA1c is above the optimal range, reflecting sustained blood sugar load."
        if "insulin_resistance" in s:
            return "The triglyceride–glucose pattern suggests early insulin-resistance stress."
    if domain == "liver":
        if "hepatic_alt" in s or s.endswith("alt_high"):
            return "ALT is above the expected range, indicating hepatocellular strain in context."
        if "ggt" in s and "high" in s:
            return "GGT is elevated, a common marker of metabolic or alcohol-related liver load."
    return "This pattern is worth following with a clinician in context of your other results."


def met_contributor(by_id: Dict[str, Any], active_sids: Set[str], sig_rows: List[Dict[str, Any]]) -> str:
    for pid, sig_hint in (
        (_ID_HBA1C, "signal_hba1c"),
        (_ID_IR, "signal_insulin_resistance"),
    ):
        rec = idl_record(by_id, pid)
        if rec and rec.severity_state != "not_observed" and rec.enabled_for_frontend and rec.subtitle:
            if any(
                s.startswith(sig_hint)
                for s in active_sids
            ) or any(str(r.get("signal_id", "")).startswith(sig_hint) for r in sig_rows if _active(r)):
                return rec.subtitle.strip()
    for pref in ("signal_hba1c", "signal_insulin_resistance", "signal_glucose"):
        for r in sig_rows:
            if not _active(r):
                continue
            if str(r.get("signal_id", "")).startswith(pref):
                return governed_signal_line(str(r.get("signal_id", "")), "met")
    g = governed_idl_field(_ID_IR, "subtitle")
    if g:
        return g
    return "Your key blood sugar markers are within their reference ranges."


def liv_contributor(
    by_id: Dict[str, Any],
    active_sids: List[str],
    sig_rows: List[Dict[str, Any]],
) -> str:
    rec = idl_record(by_id, _ID_HEP)
    if rec and rec.severity_state != "not_observed" and rec.enabled_for_frontend and rec.subtitle:
        return rec.subtitle.strip()
    for r in sig_rows:
        if not _active(r) or "hepatic" not in str(r.get("system", "")).lower():
            continue
        if str(r.get("signal_id", "")).startswith("signal_"):
            return governed_signal_line(str(r.get("signal_id", "")), "liver")
    if any(str(s).startswith("signal_") and "hep" in str(s) for s in active_sids):
        return "Liver-enzyme signals are active on this panel and merit structured follow-up."
    return "Your liver enzyme markers are within their reference ranges."


def cv_consequence(
    by_id: Dict[str, Any],
    active_sids: List[str],
    all_sig_rows: List[Dict[str, Any]],
) -> str:
    for pid in (_ID_VASCULAR, _ID_LIPID):
        rec = idl_record(by_id, pid)
        if rec and rec.severity_state != "not_observed" and rec.enabled_for_frontend and rec.why_it_matters:
            return str(rec.why_it_matters).strip()
    if _is_lipid_dominant(set(active_sids), all_sig_rows):
        t = governed_idl_field(_ID_LIPID, "why_it_matters")
        if t:
            return t
    t2 = governed_idl_field(_ID_VASCULAR, "why_it_matters")
    return t2 or ""


def met_consequence(by_id: Dict[str, Any], active_sids: Set[str], sig_rows: List[Dict[str, Any]]) -> str:
    _ = active_sids
    hba1c_active = any(
        str(r.get("signal_id", "")).startswith("signal_hba1c")
        for r in sig_rows
        if _active(r)
    )
    ir_active = any(
        "insulin_resistance" in str(r.get("signal_id", "")) for r in sig_rows if _active(r)
    )
    if hba1c_active:
        r = idl_record(by_id, _ID_HBA1C)
        if r and r.severity_state != "not_observed" and r.enabled_for_frontend and r.why_it_matters:
            return str(r.why_it_matters).strip()
    if ir_active and not hba1c_active:
        r2 = idl_record(by_id, _ID_IR)
        if r2 and r2.severity_state != "not_observed" and r2.enabled_for_frontend and r2.why_it_matters:
            return str(r2.why_it_matters).strip()
    for pid in (_ID_HBA1C, _ID_IR):
        rec = idl_record(by_id, pid)
        if rec and rec.severity_state != "not_observed" and rec.enabled_for_frontend and rec.why_it_matters:
            return str(rec.why_it_matters).strip()
    t = governed_idl_field(_ID_HBA1C, "why_it_matters")
    if t:
        return t
    return governed_idl_field(_ID_IR, "why_it_matters")


def liv_consequence(by_id: Dict[str, Any]) -> str:
    rec = idl_record(by_id, _ID_HEP)
    if rec and rec.why_it_matters:
        if rec.severity_state != "not_observed" and rec.enabled_for_frontend:
            return str(rec.why_it_matters).strip()
    t = governed_idl_field(_ID_HEP, "why_it_matters")
    return t or ""


# D-3: governed last-resort next-step copy when no per-category InsightResult recommendation
# (liver has no standard insight module — always uses this; CV/MET use after category filter)
_GOVERNED_NEXT_STEP_CV = (
    "For cardiovascular follow-up, discuss your lipid and vascular results with a clinician, "
    "especially if the pattern is new, worsening, or you have symptoms."
)
_GOVERNED_NEXT_STEP_MET = (
    "For blood sugar and metabolic follow-up, review these results with a clinician, "
    "especially if you have risk factors, symptoms, or a history of prediabetes or diabetes."
)
_GOVERNED_NEXT_STEP_LIV = (
    "For liver enzyme follow-up, review these results with a clinician, "
    "including alcohol, medications, and any relevant liver history for correct interpretation."
)


def _first_recommendation_for_category_substrings(
    insight_results: Optional[List[Dict[str, Any]]],
    category_substrings: Tuple[str, ...],
) -> str:
    """Deterministic: iterate insights in list order, first match on category, first non-empty rec."""
    if not insight_results or not category_substrings:
        return ""
    for ins in insight_results:
        if not isinstance(ins, dict):
            continue
        cat = str(ins.get("category", "")).lower()
        if not any(sub in cat for sub in category_substrings):
            continue
        for r in (ins.get("recommendations") or []):
            s = str(r).strip()
            if s:
                return s[:600]
    return ""


def next_step_from_sources(
    insight_results: Optional[List[Dict[str, Any]]],
    narrative_report: Any,
) -> str:
    """
    Legacy global next-step (D-2). Prefer per-domain: next_step_cardiovascular / _blood_sugar / _liver.
    """
    if insight_results:
        for ins in insight_results:
            if not isinstance(ins, dict):
                continue
            for r in (ins.get("recommendations") or []):
                t = str(r).strip()
                if t:
                    return t[:600]
    if narrative_report is not None:
        n = getattr(narrative_report, "next_steps_narrative", None) or ""
        n = str(n).strip()
        if n:
            return n[:600]
    return (
        "If you have questions about these results, discuss them with a qualified clinician. "
        "This information is not a medical diagnosis."
    )


def next_step_cardiovascular(
    insight_results: Optional[List[Dict[str, Any]]],
    _narrative_report: Any,
) -> str:
    """D-3: first cardiovascular-category insight recommendation, else governed CV sentence."""
    _ = _narrative_report
    s = _first_recommendation_for_category_substrings(
        insight_results, ("cardiovascular",)
    )
    if s:
        return s
    return _GOVERNED_NEXT_STEP_CV


def next_step_blood_sugar(
    insight_results: Optional[List[Dict[str, Any]]],
    _narrative_report: Any,
) -> str:
    """D-3: first metabolic-category insight recommendation, else governed blood-sugar sentence."""
    _ = _narrative_report
    s = _first_recommendation_for_category_substrings(
        insight_results, ("metabolic",)
    )
    if s:
        return s
    return _GOVERNED_NEXT_STEP_MET


def next_step_liver(
    insight_results: Optional[List[Dict[str, Any]]],
    _narrative_report: Any,
) -> str:
    """
    D-3: no standard hepatic/liver insight category in production modules — treat optional
    category match, then always fall back to governed liver sentence.
    """
    _ = _narrative_report
    s = _first_recommendation_for_category_substrings(
        insight_results, ("hepatic", "liver", "hepat")
    )
    if s:
        return s
    return _GOVERNED_NEXT_STEP_LIV
