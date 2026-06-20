"""
D-2 — Wave 1 consumer narrative assembly (Strategy A).

Deterministic only: IDL (published bundle + idl_registry static text), D-1 bands/tiers,
signal ids, and optional narrative_report / insight recommendations. No LLM.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence, Set, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from core.contracts.interpretation_display_layer_v1 import InterpretationDisplayRecordV1

# IDs in idl_records_v1.yaml (governed)
_ID_VASCULAR = "ph_vascular_hcy_inflammation_v1"
_ID_LIPID = "ph_lipid_residual_ldl_favourable_transport_v1"
_ID_HBA1C = "ph_hba1c_metabolic_stress_v1"
_ID_IR = "ph_metabolic_early_ir_v1"
_ID_HEP = "ph_hepatic_alt_inflammatory_v1"

# MED-REV-2 / KB-UTIL-1: visible scored subsystem ids (narrative authority follows card surface)
_WAVE1_CV_LIPID_SUBSYSTEM_ID = "wave1_cv_lipid_transport"
_WAVE1_MET_GLYCAEMIC_SUBSYSTEM_ID = "wave1_met_glycaemic_control"

# LC-S11A: honest glycaemic copy when no active blood-sugar signals on the panel.
_MET_NO_ACTIVE_SIGNAL_CONTRIBUTOR = (
    "HbA1c is within range on this panel. Glucose and insulin were not included, "
    "so a fuller glycaemic read would require those markers."
)

_MET_CONSEQUENCE_NEUTRAL_LIMITED_GLYCAEMIC = (
    "HbA1c reflects longer-term blood sugar context on this panel. Glucose and insulin were not "
    "included here, so they would add detail if you and your clinician choose to review them later."
)

_CV_CONSEQUENCE_NEUTRAL_LIPID_IN_RANGE = (
    "Favourable lipid markers on this panel are supportive for cardiovascular context; "
    "discuss trends with your clinician if you track lipids over time."
)

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
        return "Your liver health looks strong based on your current blood markers."
    if band == "stable":
        return "Your liver health looks broadly stable based on your current blood markers."
    if band == "watch":
        return "Your liver health shows some signals worth watching based on your current markers."
    return "Your liver health shows a pattern that deserves closer review based on your current markers."


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


def _met_contributor_reads_limited_coverage_reassuring(contributor: str) -> bool:
    """True when glycaemic card contributor reflects HbA1c-only / in-range limited coverage."""
    c = (contributor or "").lower()
    if "not included" in c or "were not included" in c:
        return True
    if "within range" in c or "within their reference" in c:
        return True
    return False


def _met_story_conflicts_with_stable_headline(contributor: str, consequence: str) -> bool:
    t = _narrative_lowercased(contributor, consequence)
    if not t:
        return False
    if "not included" in t or "were not included" in t or "not on this panel" in t:
        return False
    if _met_contributor_reads_limited_coverage_reassuring(contributor):
        active_strain_needles = (
            "active signals",
            "sustained glyc",
            "glycaemic strain",
            "glycemic strain",
            "impaired",
            "prediabet",
            "insulin resistance",
            "metabolic stress",
        )
        return any(n in t for n in active_strain_needles)
    needles = (
        "glyc",
        "insulin",
        "resistance",
        "impaired",
        "hba1c",
        "strain",
        "metabolic stress",
        "triglyceride",
        "sustained",
        "prediabet",
        "diabet",
        "active signals",
    )
    if "glucose" in t and "within range" in t:
        return False
    return any(n in t for n in needles)


def _idl_suggests_risk_or_review_led(primary_rec: Any) -> bool:
    """D-6: When the resolved IDL record is not reassuring, block band-only 'looks strong' copy."""
    if primary_rec is None:
        return False
    st = str(getattr(primary_rec, "severity_state", "") or "")
    return st in ("watch", "attention", "strong_signal")


# D-7: Neutral consequence when headline/contributor read stable/in-range but strain consequence would contradict.
_LIV_CONSEQUENCE_NEUTRAL_WHEN_SURFACE_STABLE_D7 = (
    "Fibrosis-type risk is not something this enzyme snapshot alone can confirm or exclude; "
    "your clinician can interpret these markers alongside history and any follow-up testing they consider appropriate."
)

_LIVER_CONTRIBUTOR_STRAIN_NEEDLES_D7 = (
    "elevated",
    "above the expected range",
    "above the optimal range",
    "merit structured follow-up",
    "liver-enzyme signals are active",
    "hepatocellular strain",
    "metabolic or inflammatory strain",
)


def _liver_surface_reads_stable_or_in_range(contributor: str, headline: str) -> bool:
    """True when collapsed/expanded liver lines read as broadly reassuring (D-7 coherence gate)."""
    c = (contributor or "").lower()
    h = (headline or "").lower()
    if "within their reference ranges" in c or "within their reference range" in c:
        return True
    if "looks strong" in h or "broadly stable" in h:
        return True
    return False


def _liver_contributor_implies_active_enzyme_strain(contributor: str) -> bool:
    """True when contributor copy reflects enzyme strain / active hepatic signals (D-7)."""
    t = (contributor or "").lower()
    return any(n in t for n in _LIVER_CONTRIBUTOR_STRAIN_NEEDLES_D7)


def _liver_signal_ids_imply_enzyme_strain(active_liver_signal_ids: List[str]) -> bool:
    """True only when listed liver signals reflect enzyme strain, not ancillary ids."""
    strain_prefixes = (
        "signal_alt",
        "signal_ast",
        "signal_ggt",
        "signal_hepatic_alt",
        "signal_hepatic",
    )
    for sid in active_liver_signal_ids:
        s = str(sid).lower()
        if any(s.startswith(p) for p in strain_prefixes):
            return True
    return False


def _liver_use_neutral_consequence_instead_of_strain_copy(
    *,
    contributor_sentence: str,
    headline_sentence: str,
    primary_rec_for_hepatic: Any,
    active_liver_signal_ids: List[str],
    band_label: str = "",
) -> bool:
    """
    D-7: Use proportionate neutral consequence instead of MASLD-style strain copy.

    Neutral when the surface reads stable/in-range and evidence does not support an active-strain story.

    Strong strain consequence remains when:
    - resolved hepatic IDL is risk-/review-led (watch / attention / strong_signal), or
    - Wave 1 hepatic enzyme-strain signals are active on the panel, or
    - contributor copy already reflects enzyme elevation / strain.
    """
    if not _liver_surface_reads_stable_or_in_range(contributor_sentence, headline_sentence):
        return False
    if _liver_contributor_implies_active_enzyme_strain(contributor_sentence):
        return False
    if primary_rec_for_hepatic is not None and _idl_suggests_risk_or_review_led(primary_rec_for_hepatic):
        return False
    if active_liver_signal_ids and _liver_signal_ids_imply_enzyme_strain(active_liver_signal_ids):
        return False
    if active_liver_signal_ids and band_label not in ("strong", "stable"):
        return False
    return True


def headline_cv_coherent(
    band: str,
    contributor: str,
    consequence: str,
    primary_rec: Any = None,
) -> str:
    """
    D-4 + D-6: Headline follows resolved primary IDL, not the numeric band alone.
    Never use reassuring 'looks strong' / 'broadly stable' when the IDL is risk- or review-led.
    """
    if band in ("strong", "stable") and _idl_suggests_risk_or_review_led(primary_rec):
        return (
            "Your cardiovascular read on this panel is not a simple all-clear: the leading pattern here "
            "still deserves clinical context alongside your numbers."
        )
    if band == "strong" and _cv_story_conflicts_with_stable_headline(contributor, consequence):
        return (
            "Some markers in this cardiovascular view still need context with a clinician, even when "
            "parts of the picture look supportive."
        )
    if band == "stable" and _cv_story_conflicts_with_stable_headline(contributor, consequence):
        return (
            "Your cardiovascular results do not read as a simple all-clear: some markers look reassuring "
            "while others add context that is worth discussing with a clinician."
        )
    return headline_cv(band)


def headline_met_coherent(
    band: str,
    contributor: str,
    consequence: str,
    primary_rec: Any = None,
) -> str:
    if band in ("strong", "stable") and _idl_suggests_risk_or_review_led(primary_rec):
        return (
            "Your blood sugar and metabolic read is led by a pattern that still warrants structured review, "
            "not a simple 'all good' label from the band alone."
        )
    if band == "strong" and _met_story_conflicts_with_stable_headline(contributor, consequence):
        return (
            "Your blood sugar and metabolic context still has active signals to address in care planning, "
            "even if some results look in range on the surface."
        )
    if band == "stable" and _met_story_conflicts_with_stable_headline(contributor, consequence):
        return (
            "Your blood sugar and metabolic read is mixed on this panel — it is not a clean "
            "all-stable story; several markers shape the pattern together."
        )
    return headline_met(band)


def confidence_sentence_cv_coherent(tier: str, contributor: str) -> str:
    """D-4 / MED-REV-2: CV confidence uses governed lipid-tier copy only (no homocysteine bridge)."""
    t = tier if tier in ("high", "medium", "low") else "medium"
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
        return "Based mainly on: your cardiovascular signals and patterns from your markers."
    if domain == "met":
        return "Based mainly on: your blood sugar and metabolic markers from your panel."
    return "Based mainly on: your liver-related markers from your panel."


def confidence_sentence_for(
    tier: str,
    domain: str,
    *,
    panel_biomarker_ids: Optional[Set[str]] = None,
) -> str:
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
    if domain in ("ren", "kidney"):
        if t == "high":
            return (
                "Confidence is high — creatinine and eGFR are both present on this panel."
            )
        if t == "medium":
            return (
                "Confidence is moderate — one core filtration marker is present; "
                "adding the other would strengthen the read."
            )
        return (
            "Confidence is limited — core kidney filtration markers are missing from this panel."
        )
    if domain == "bio":
        if t == "high":
            return (
                "Confidence is high — haemoglobin and haematocrit are both present on this panel."
            )
        if t == "medium":
            return (
                "Confidence is moderate — one core red-cell marker is present; "
                "adding the other would strengthen the read."
            )
        return (
            "Confidence is limited — core red-cell markers are missing from this panel."
        )
    # liver
    panel = panel_biomarker_ids or set()
    if t == "high":
        return "Confidence is high — several liver function markers are present in this panel."
    if t == "medium":
        return (
            "Confidence is moderate — key enzymes are present; a fuller LFT would add context."
        )
    missing_labels: List[str] = []
    for mid, label in (("ggt", "GGT"), ("alp", "ALP"), ("albumin", "albumin")):
        if mid not in panel:
            missing_labels.append(label)
    if missing_labels:
        joined = ", ".join(missing_labels)
        return f"Confidence is limited — adding {joined} would strengthen this read."
    return "Confidence is limited — additional liver markers would strengthen this read."


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


def cv_contributor_primary(
    by_id: Dict[str, Any],
    active_sids: List[str],
    sig_rows: List[Dict[str, Any]],
    primary_idl: Optional[str],
) -> str:
    """
    D-6: Single authority — subtitle from resolved primary IDL only; then signal fallback (no IDL greedy loop).
    """
    if primary_idl:
        rec = idl_record(by_id, primary_idl)
        if rec is not None and rec.severity_state != "not_observed" and rec.enabled_for_frontend and rec.subtitle:
            return rec.subtitle.strip()
    return _cv_contributor_signal_fallback(set(active_sids), sig_rows)


def _cv_contributor_signal_fallback(sset: Set[str], sig_rows: List[Dict[str, Any]]) -> str:
    for pref in _CV_SIGNAL_PRIORITY:
        if any(s.startswith(pref) or s == pref for s in sset):
            return governed_signal_line(pref, "cv")
    for r in sig_rows:
        if not _active(r):
            continue
        sid = str(r.get("signal_id", ""))
        if any(sid.startswith(p) for p in _CV_SIGNAL_PRIORITY):
            return governed_signal_line(sid, "cv")
    return "Your key cardiovascular markers are within their reference ranges."


def _cv_contributor_lipid_only_signal_fallback(sset: Set[str], sig_rows: List[Dict[str, Any]]) -> str:
    """Signal fallback for lipid-visible CV card — excludes homocysteine / vascular hidden pathways."""
    lipid_priority = [p for p in _CV_SIGNAL_PRIORITY if not _is_hcy(p)]
    for pref in lipid_priority:
        if any(s.startswith(pref) or s == pref for s in sset):
            return governed_signal_line(pref, "cv")
    for r in sig_rows:
        if not _active(r):
            continue
        sid = str(r.get("signal_id", ""))
        if _is_hcy(sid):
            continue
        if any(sid.startswith(p) for p in lipid_priority):
            return governed_signal_line(sid, "cv")
    return "Your key cardiovascular markers are within their reference ranges."


def _scored_visible_subsystems(subsystems: Sequence[Any] | None) -> List[Any]:
    if not subsystems:
        return []
    return [
        sub
        for sub in subsystems
        if getattr(sub, "visibility_tier", None) == "scored_subsystem"
    ]


def cv_uses_lipid_subsystem_narrative_authority(subsystems: Sequence[Any] | None) -> bool:
    """MED-REV-2: when the card surface is lipid-only, narrative must not follow hidden vascular IDL."""
    scored = _scored_visible_subsystems(subsystems)
    if len(scored) != 1:
        return False
    return str(getattr(scored[0], "subsystem_id", "")).strip() == _WAVE1_CV_LIPID_SUBSYSTEM_ID


def met_uses_glycaemic_subsystem_narrative_authority(subsystems: Sequence[Any] | None) -> bool:
    """MED-REV-2: long-term blood sugar visible card — do not imply insulin/active strain without evidence."""
    scored = _scored_visible_subsystems(subsystems)
    if len(scored) != 1:
        return False
    return str(getattr(scored[0], "subsystem_id", "")).strip() == _WAVE1_MET_GLYCAEMIC_SUBSYSTEM_ID


def cv_contributor_for_lipid_visible_card(
    by_id: Dict[str, Any],
    active_sids: List[str],
    sig_rows: List[Dict[str, Any]],
    lipid_idl: Optional[str],
) -> str:
    """Contributor when visible scored subsystem is Atherogenic lipid pattern only."""
    if lipid_idl == _ID_LIPID:
        rec = idl_record(by_id, lipid_idl)
        if rec is not None and rec.severity_state != "not_observed" and rec.enabled_for_frontend and rec.subtitle:
            return rec.subtitle.strip()
    return _cv_contributor_lipid_only_signal_fallback(set(active_sids), sig_rows)


def cv_consequence_for_lipid_visible_card(
    by_id: Dict[str, Any],
    active_sids: List[str],
    sig_rows: List[Dict[str, Any]],
    lipid_idl: Optional[str],
    *,
    contributor_sentence: str = "",
) -> str:
    """Consequence aligned with lipid-visible CV card — never homocysteine/inflammation IDL copy."""
    if lipid_idl == _ID_LIPID:
        rec = idl_record(by_id, lipid_idl)
        if rec and rec.severity_state != "not_observed" and rec.enabled_for_frontend and rec.why_it_matters:
            return str(rec.why_it_matters).strip()
    if "within their reference ranges" in (contributor_sentence or "").lower():
        return _CV_CONSEQUENCE_NEUTRAL_LIPID_IN_RANGE
    lipid_only_sids = {s for s in active_sids if not _is_hcy(str(s))}
    lipid_rows = [r for r in sig_rows if not _is_hcy(str(r.get("signal_id", "")))]
    if _is_lipid_dominant(lipid_only_sids, lipid_rows):
        t = governed_idl_field(_ID_LIPID, "why_it_matters")
        if t:
            return t
    t = governed_idl_field(_ID_LIPID, "why_it_matters")
    return t or _CV_CONSEQUENCE_NEUTRAL_LIPID_IN_RANGE


def _met_has_active_glycaemic_strain_signals(
    active_sids: Set[str],
    sig_rows: List[Dict[str, Any]],
) -> bool:
    for r in sig_rows:
        if not _active(r):
            continue
        sid = str(r.get("signal_id", ""))
        if sid.startswith("signal_hba1c") or sid.startswith("signal_glucose"):
            return True
        if "insulin_resistance" in sid:
            return True
    for sid in active_sids:
        s = str(sid)
        if s.startswith("signal_hba1c") or s.startswith("signal_glucose") or "insulin_resistance" in s:
            return True
    return False


def _met_use_neutral_consequence_for_limited_glycaemic(
    *,
    contributor_sentence: str,
    band_label: str,
    active_sids: Set[str],
    sig_rows: List[Dict[str, Any]],
    primary_idl: Optional[str],
    by_id: Dict[str, Any],
) -> bool:
    if band_label not in ("strong", "stable"):
        return False
    primary_rec = idl_record(by_id, primary_idl) if primary_idl else None
    if primary_rec is not None and _idl_suggests_risk_or_review_led(primary_rec):
        return False
    if _met_has_active_glycaemic_strain_signals(active_sids, sig_rows):
        return False
    return _met_contributor_reads_limited_coverage_reassuring(contributor_sentence)


def met_consequence_for_glycaemic_visible_card(
    by_id: Dict[str, Any],
    active_sids: Set[str],
    sig_rows: List[Dict[str, Any]],
    primary_idl: Optional[str],
    *,
    contributor_sentence: str = "",
    band_label: str = "",
) -> str:
    """Consequence for long-term blood sugar visible card — proportionate when HbA1c-only in range."""
    if _met_use_neutral_consequence_for_limited_glycaemic(
        contributor_sentence=contributor_sentence,
        band_label=band_label,
        active_sids=active_sids,
        sig_rows=sig_rows,
        primary_idl=primary_idl,
        by_id=by_id,
    ):
        return _MET_CONSEQUENCE_NEUTRAL_LIMITED_GLYCAEMIC
    return met_consequence_primary(by_id, active_sids, sig_rows, primary_idl)


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
    if domain in ("ren", "kidney"):
        if "egfr" in s and "low" in s:
            return (
                "eGFR is below the reference range on this panel, a marker that can relate "
                "to reduced kidney filtration."
            )
        if "creatinine" in s and "high" in s:
            return (
                "Creatinine is above the reference range, which can reflect reduced filtration "
                "or other influences such as muscle mass."
            )
        if "creatinine" in s and "low" in s:
            return (
                "Creatinine is below the reference range, which can reflect lower muscle mass "
                "or reduced generation rather than kidney disease alone."
            )
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


def met_contributor_primary(
    by_id: Dict[str, Any],
    active_sids: Set[str],
    sig_rows: List[Dict[str, Any]],
    primary_idl: Optional[str],
) -> str:
    """D-6: Primary IDL subtitle only, then signal fallback (no greedy IDL loop)."""
    if primary_idl:
        rec = idl_record(by_id, primary_idl)
        if rec and rec.severity_state != "not_observed" and rec.enabled_for_frontend and rec.subtitle:
            return rec.subtitle.strip()
    if not active_sids:
        return _MET_NO_ACTIVE_SIGNAL_CONTRIBUTOR
    for pref in ("signal_hba1c", "signal_glucose"):
        for r in sig_rows:
            if not _active(r):
                continue
            if str(r.get("signal_id", "")).startswith(pref):
                return governed_signal_line(str(r.get("signal_id", "")), "met")
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


def liv_contributor_primary(
    by_id: Dict[str, Any],
    active_sids: List[str],
    sig_rows: List[Dict[str, Any]],
    primary_idl: Optional[str],
) -> str:
    """D-6: Primary IDL subtitle only, then prior signal fallback."""
    if primary_idl:
        rec = idl_record(by_id, primary_idl)
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


def liv_consequence_primary(
    by_id: Dict[str, Any],
    primary_idl: Optional[str],
    *,
    contributor_sentence: str = "",
    headline_sentence: str = "",
    active_liver_signal_ids: Optional[List[str]] = None,
    band_label: str = "",
) -> str:
    """D-7: Gate strain consequence against stable contributor/headline when evidence does not support it."""
    active_sids = list(active_liver_signal_ids or [])
    if primary_idl:
        rec = idl_record(by_id, primary_idl)
        if rec and rec.why_it_matters and rec.severity_state != "not_observed" and rec.enabled_for_frontend:
            if _liver_use_neutral_consequence_instead_of_strain_copy(
                contributor_sentence=contributor_sentence,
                headline_sentence=headline_sentence,
                primary_rec_for_hepatic=rec,
                active_liver_signal_ids=active_sids,
                band_label=band_label,
            ):
                return _LIV_CONSEQUENCE_NEUTRAL_WHEN_SURFACE_STABLE_D7
            return str(rec.why_it_matters).strip()
    return liv_consequence(
        by_id,
        contributor_sentence=contributor_sentence,
        headline_sentence=headline_sentence,
        active_liver_signal_ids=active_sids,
        band_label=band_label,
    )


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


def cv_consequence_primary(
    by_id: Dict[str, Any],
    active_sids: List[str],
    all_sig_rows: List[Dict[str, Any]],
    primary_idl: Optional[str],
) -> str:
    """D-6: why_it_matters from resolved primary IDL first; lipid-dominant KB path preserved (deferred content gap)."""
    if primary_idl:
        rec = idl_record(by_id, primary_idl)
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


def met_consequence_primary(
    by_id: Dict[str, Any],
    active_sids: Set[str],
    sig_rows: List[Dict[str, Any]],
    primary_idl: Optional[str],
) -> str:
    """D-6: why_it_matters from primary IDL when set; else same tiered logic as met_consequence."""
    _ = active_sids
    if primary_idl:
        rec = idl_record(by_id, primary_idl)
        if rec and rec.severity_state != "not_observed" and rec.enabled_for_frontend and rec.why_it_matters:
            return str(rec.why_it_matters).strip()
    return met_consequence(by_id, active_sids, sig_rows)


def liv_consequence(
    by_id: Dict[str, Any],
    *,
    contributor_sentence: str = "",
    headline_sentence: str = "",
    active_liver_signal_ids: Optional[List[str]] = None,
    band_label: str = "",
) -> str:
    """Fallback liver consequence path (non-primary-IDL); D-7 neutral gate applies to YAML/str copy."""
    active_sids = list(active_liver_signal_ids or [])
    rec = idl_record(by_id, _ID_HEP)
    if rec and rec.why_it_matters:
        if rec.severity_state != "not_observed" and rec.enabled_for_frontend:
            if _liver_use_neutral_consequence_instead_of_strain_copy(
                contributor_sentence=contributor_sentence,
                headline_sentence=headline_sentence,
                primary_rec_for_hepatic=rec,
                active_liver_signal_ids=active_sids,
                band_label=band_label,
            ):
                return _LIV_CONSEQUENCE_NEUTRAL_WHEN_SURFACE_STABLE_D7
            return str(rec.why_it_matters).strip()
    t = governed_idl_field(_ID_HEP, "why_it_matters")
    if (
        t
        and _liver_use_neutral_consequence_instead_of_strain_copy(
            contributor_sentence=contributor_sentence,
            headline_sentence=headline_sentence,
            primary_rec_for_hepatic=None,
            active_liver_signal_ids=active_sids,
            band_label=band_label,
        )
    ):
        return _LIV_CONSEQUENCE_NEUTRAL_WHEN_SURFACE_STABLE_D7
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
_GOVERNED_NEXT_STEP_REN = (
    "For kidney filtration markers, discuss out-of-range results with a clinician, "
    "especially if they are new, worsening, or you have symptoms or risk factors."
)
_GOVERNED_NEXT_STEP_BIO = (
    "For red-cell and oxygen-carrying markers, discuss out-of-range results with a clinician, "
    "especially if they are new, persistent, or you have relevant symptoms."
)

_ID_RENAL = "ph_renal_stress_v1"


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


def headline_ren(band: str) -> str:
    """P1-2: non-diagnostic kidney filtration headline."""
    b = (band or "").strip().lower()
    if b in ("review", "watch"):
        return "Your kidney filtration markers may need follow-up in clinical context."
    if b == "stable":
        return "Your kidney filtration markers look broadly stable on this panel."
    return "Your kidney filtration markers are within a broadly favourable range on this panel."


def ren_contributor_primary(
    by_id: Dict[str, Any],
    active_sids: List[str],
    sig_rows: List[Dict[str, Any]],
    primary_idl: Optional[str],
) -> str:
    if primary_idl:
        rec = idl_record(by_id, primary_idl)
        if rec and rec.severity_state != "not_observed" and rec.enabled_for_frontend and rec.subtitle:
            return rec.subtitle.strip()
    for pref in ("signal_egfr", "signal_creatinine"):
        for r in sig_rows:
            if not _active(r):
                continue
            sid = str(r.get("signal_id", ""))
            if sid.startswith(pref):
                return governed_signal_line(sid, "kidney")
    if active_sids:
        return "Kidney filtration markers on this panel are outside their reference ranges."
    return "Your kidney filtration markers are within their reference ranges on this panel."


def ren_consequence_primary(
    by_id: Dict[str, Any],
    primary_idl: Optional[str],
    *,
    contributor_sentence: str = "",
    active_renal_signal_ids: Optional[List[str]] = None,
) -> str:
    if primary_idl:
        rec = idl_record(by_id, primary_idl)
        if rec and rec.why_it_matters and rec.severity_state != "not_observed" and rec.enabled_for_frontend:
            text = str(rec.why_it_matters).strip()
            if "disease" not in text.lower() and "ckd" not in text.lower():
                return text
    if active_renal_signal_ids:
        return (
            "Filtration markers can shift with hydration, muscle mass, and medications; "
            "they are worth discussing with a clinician if out of range."
        )
    return (
        "Kidney filtration markers help describe how waste is cleared; "
        "a single panel snapshot is not a full kidney assessment."
    )


def next_step_kidney(
    insight_results: Optional[List[Dict[str, Any]]],
    _narrative_report: Any,
) -> str:
    _ = _narrative_report
    s = _first_recommendation_for_category_substrings(
        insight_results, ("renal", "kidney", "filtration", "detox")
    )
    if s:
        return s
    return _GOVERNED_NEXT_STEP_REN


def headline_bio(band: str) -> str:
    """P1-3: non-diagnostic blood / iron / oxygen headline."""
    b = (band or "").strip().lower()
    if b in ("review", "watch"):
        return "Your red-cell and oxygen-carrying markers may need follow-up in clinical context."
    if b == "stable":
        return "Your red-cell and oxygen-carrying markers look broadly stable on this panel."
    return "Your red-cell and oxygen-carrying markers are within a broadly favourable range on this panel."


def bio_contributor_primary(
    by_id: Dict[str, Any],
    active_sids: List[str],
    sig_rows: List[Dict[str, Any]],
    primary_idl: Optional[str],
) -> str:
    if primary_idl:
        rec = idl_record(by_id, primary_idl)
        if rec and rec.severity_state != "not_observed" and rec.enabled_for_frontend and rec.subtitle:
            text = rec.subtitle.strip().lower()
            if "anaemia" not in text and "iron deficiency" not in text and "bleeding" not in text:
                return rec.subtitle.strip()
    for pref in ("signal_ferritin", "signal_hemoglobin", "signal_hgb"):
        for r in sig_rows:
            if not _active(r):
                continue
            sid = str(r.get("signal_id", ""))
            if sid.startswith(pref) and sid in active_sids:
                return governed_signal_line(sid, "bio")
    if active_sids:
        return (
            "Red-cell and oxygen-carrying markers on this panel are outside their reference ranges."
        )
    return (
        "Your red-cell and oxygen-carrying markers are within their reference ranges on this panel."
    )


def bio_consequence_primary(
    by_id: Dict[str, Any],
    primary_idl: Optional[str],
    *,
    contributor_sentence: str = "",
    active_bio_signal_ids: Optional[List[str]] = None,
) -> str:
    if primary_idl:
        rec = idl_record(by_id, primary_idl)
        if rec and rec.why_it_matters and rec.severity_state != "not_observed" and rec.enabled_for_frontend:
            text = str(rec.why_it_matters).strip().lower()
            if not any(
                term in text
                for term in ("anaemia", "iron deficiency", "bleeding", "cancer", "haemochromatosis")
            ):
                return str(rec.why_it_matters).strip()
    if active_bio_signal_ids:
        return (
            "Red-cell and iron-status markers can shift with diet, inflammation, and other factors; "
            "they are worth discussing with a clinician if out of range or persistent."
        )
    return (
        "Red-cell and oxygen-carrying markers help describe oxygen transport context; "
        "a single panel snapshot is not a full haematological assessment."
    )


def next_step_blood_iron_oxygen(
    insight_results: Optional[List[Dict[str, Any]]],
    _narrative_report: Any,
) -> str:
    _ = _narrative_report
    s = _first_recommendation_for_category_substrings(
        insight_results, ("hematological", "hematologic", "blood", "iron", "oxygen")
    )
    if s:
        return s
    return _GOVERNED_NEXT_STEP_BIO
