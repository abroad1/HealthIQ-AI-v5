"""
D-1 — Deterministic Wave 1 customer domain score + confidence assembly (Strategy A).

Translation layer only: reads scoring rails, burden/capacity, signals, IDL. Does not
mutate engines. Scoring track vs burden/capacity track is explicit in source_track and
raw_evidence_refs to avoid silent calibration mixing.

Liver: scoring key is ``liver`` (scoring_policy.yaml); burden/capacity key is ``hepatic``
(system_burden_engine / InsightGraph.system_capacity_scores). Never read capacity using ``liver``.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence, Set, Tuple, cast

from core.analytics.domain_narrative_wave1 import (
    confidence_sentence_cv_coherent,
    confidence_sentence_for,
    cv_consequence_for_lipid_visible_card,
    cv_consequence_primary,
    cv_contributor_for_lipid_visible_card,
    cv_contributor_primary,
    cv_uses_lipid_subsystem_narrative_authority,
    evidence_anchor_sentence,
    headline_cv_coherent,
    headline_liv,
    headline_met_coherent,
    idl_record,
    idl_records_index,
    liv_consequence_primary,
    liv_contributor_primary,
    met_consequence_for_glycaemic_visible_card,
    met_consequence_primary,
    met_contributor_primary,
    met_uses_glycaemic_subsystem_narrative_authority,
    next_step_blood_sugar,
    next_step_cardiovascular,
    next_step_kidney,
    next_step_blood_iron_oxygen,
    next_step_liver,
    headline_ren,
    headline_bio,
    ren_contributor_primary,
    ren_consequence_primary,
    bio_contributor_primary,
    bio_consequence_primary,
)
from core.contracts.interpretation_display_layer_v1 import InterpretationDisplayLayerBundleV1
from core.analytics.wave1_subsystem_evidence import (
    assemble_wave1_flat_domain_evidence,
    assemble_wave1_subsystem_evidence,
)
from core.models.results import ConfidenceTierV1, ConsumerDomainScoreV1

# --- Scoring policy rails (authoritative names) ---
_RAIL_CARDIOVASCULAR = "cardiovascular"
_RAIL_METABOLIC = "metabolic"
_RAIL_LIVER = "liver"
_RAIL_KIDNEY = "kidney"
_RAIL_CBC = "cbc"

# P1-18: transferrin transport upregulation (pkg_kb61) — ID-matched production package.
# Other CBC/iron signals remain excluded pending frame adjudication (P1-3 carry-forward).
_BLOOD_IRON_OXYGEN_LAUNCH_SIGNAL_IDS: frozenset[str] = frozenset({"signal_transferrin_high"})
_BURDEN_HEPATIC = "hepatic"

# D-4: user-safe caveat lines (replaces internal slug list for retail cards)
_LIVER_CAVEAT_USER_LINES = (
    "Only the liver markers available on this panel are used here; a fuller liver profile would narrow the picture.",
    "Liver load is also interpreted with related metabolic (hepatic) context, not from the liver score line alone.",
)

# Wave 1 IDL selection order (MED-REV-2: lipid/glycaemic anchors align with visible scored subsystems)
_IDL_ORDER_CV = ("ph_lipid_residual_ldl_favourable_transport_v1", "ph_vascular_hcy_inflammation_v1")
_IDL_ORDER_MET = ("ph_hba1c_metabolic_stress_v1",)
_IDL_ORDER_LIV = ("ph_hepatic_alt_inflammatory_v1",)
_IDL_ORDER_REN = ("ph_renal_stress_v1",)

# Biomarker coverage: cardiovascular rail (ssot/scoring_policy systems.cardiovascular)
_CV_RAIL_BIOMARKERS = (
    "total_cholesterol",
    "ldl_cholesterol",
    "hdl_cholesterol",
    "triglycerides",
    "tc_hdl_ratio",
)

# Blood sugar: glucose + HbA1c core; insulin / triglycerides improve confidence
_MET_CORE = ("glucose", "hba1c")
_MET_ENHANCERS = ("insulin", "triglycerides")

# Hepatic pool for domain-level confidence (domain doc; not cluster schema alone)
_HEP_CONFIDENCE_POOL = (
    "alt",
    "ast",
    "ggt",
    "alp",
    "albumin",
    "total_bilirubin",
    "bilirubin",
    "total_protein",
    "globulin",
)


def _liver_panel_has_bilirubin_coverage(panel: Set[str]) -> bool:
    """SSOT uses canonical ``bilirubin``; some rails still say ``total_bilirubin`` — either satisfies coverage."""
    return ("bilirubin" in panel) or ("total_bilirubin" in panel)


def _band_label_from_0_100(score_0_100: float) -> str:
    s = max(0.0, min(100.0, float(score_0_100)))
    if s >= 80.0:
        return "strong"
    if s >= 65.0:
        return "stable"
    if s >= 45.0:
        return "watch"
    return "review"


def _as_float_0_100(overall: Any) -> float:
    try:
        v = float(overall)
    except (TypeError, ValueError):
        return 0.0
    return max(0.0, min(100.0, v))


def _health_systems(scoring_result: Dict[str, Any]) -> Dict[str, Any]:
    hss = scoring_result.get("health_system_scores")
    return hss if isinstance(hss, dict) else {}


def _system_rail_data(hss: Dict[str, Any], system_key: str) -> Dict[str, Any]:
    block = hss.get(system_key)
    return block if isinstance(block, dict) else {}


def _iter_signal_results(insight_graph: Any) -> List[Dict[str, Any]]:
    raw = getattr(insight_graph, "signal_results", None)
    if not isinstance(raw, list):
        return []
    out: List[Dict[str, Any]] = []
    for item in raw:
        if isinstance(item, dict):
            out.append(item)
    return out


def _active_signal_state(st: str) -> bool:
    return st in ("at_risk", "suboptimal")


def _is_wave1_cardiovascular(row: Dict[str, Any]) -> bool:
    if not _active_signal_state(str(row.get("signal_state", ""))):
        return False
    system = str(row.get("system", "")).strip()
    sid = str(row.get("signal_id", ""))
    primary = str(row.get("primary_metric", "")).strip()
    if system == "lipid_transport":
        return True
    if primary in _CV_RAIL_BIOMARKERS:
        return True
    if "homocysteine" in sid or "non_hdl" in primary:
        return True
    for pref in (
        "signal_total_cholesterol",
        "signal_ldl",
        "signal_hdl",
        "signal_triglycerides",
        "signal_lipid",
        "signal_apo",
    ):
        if sid.startswith(pref):
            return True
    return False


def _is_wave1_blood_sugar(row: Dict[str, Any]) -> bool:
    if not _active_signal_state(str(row.get("signal_state", ""))):
        return False
    system = str(row.get("system", "")).strip()
    sid = str(row.get("signal_id", ""))
    primary = str(row.get("primary_metric", "")).strip()
    if system == "metabolic":
        return True
    if "glucose" in primary or "hba1c" in primary or "insulin" in primary:
        return True
    if "insulin_resistance" in sid or "hba1c" in sid or "glucose" in sid:
        return True
    return False


def _is_wave1_liver(row: Dict[str, Any]) -> bool:
    if not _active_signal_state(str(row.get("signal_state", ""))):
        return False
    system = str(row.get("system", "")).strip()
    sid = str(row.get("signal_id", ""))
    if system == "hepatic":
        return True
    for pref in ("signal_alt", "signal_ast", "signal_ggt", "signal_alp", "signal_hepatic", "signal_bilirubin"):
        if sid.startswith(pref):
            return True
    return False


def _is_wave1_kidney(row: Dict[str, Any]) -> bool:
    if not _active_signal_state(str(row.get("signal_state", ""))):
        return False
    sid = str(row.get("signal_id", ""))
    primary = str(row.get("primary_metric", "")).strip()
    if sid in ("signal_egfr_low", "signal_creatinine_high", "signal_creatinine_low"):
        return True
    if primary in ("creatinine", "egfr"):
        return True
    if sid.startswith("signal_egfr") or sid.startswith("signal_creatinine"):
        return True
    return False


def _is_wave1_blood_iron_oxygen(row: Dict[str, Any]) -> bool:
    if not _active_signal_state(str(row.get("signal_state", ""))):
        return False
    sid = str(row.get("signal_id", "")).strip()
    return sid in _BLOOD_IRON_OXYGEN_LAUNCH_SIGNAL_IDS


def _kidney_confidence_tier(panel: Set[str]) -> str:
    core = sum(1 for m in ("creatinine", "egfr") if m in panel)
    if core >= 2:
        return "high"
    if core >= 1:
        return "medium"
    return "low"


def _bio_confidence_tier(panel: Set[str]) -> str:
    core = sum(1 for m in ("hemoglobin", "hematocrit") if m in panel)
    if core >= 2:
        return "high"
    if core >= 1:
        return "medium"
    return "low"


def _collect_signal_ids(rows: List[Dict[str, Any]], pred) -> List[str]:
    out: List[str] = []
    for row in rows:
        if not pred(row):
            continue
        sid = str(row.get("signal_id", "")).strip()
        if sid and sid not in out:
            out.append(sid)
    return out


def _cluster_confidence_map(insight_graph: Any) -> Dict[str, float]:
    conf = getattr(insight_graph, "confidence", None)
    if conf is None:
        return {}
    if hasattr(conf, "model_dump"):
        d = conf.model_dump()
    elif isinstance(conf, dict):
        d = conf
    else:
        return {}
    cc = d.get("cluster_confidence")
    if not isinstance(cc, dict):
        return {}
    out: Dict[str, float] = {}
    for k, v in cc.items():
        try:
            out[str(k)] = float(v)
        except (TypeError, ValueError):
            continue
    return out


def _select_primary_idl(
    bundle: Optional[InterpretationDisplayLayerBundleV1],
    priority_ids: Tuple[str, ...],
) -> Optional[str]:
    if bundle is None or not isinstance(bundle, InterpretationDisplayLayerBundleV1):
        return None
    by_id = {r.internal_id: r for r in bundle.records}
    for pid in priority_ids:
        rec = by_id.get(pid)
        if rec is None:
            continue
        if rec.severity_state == "not_observed":
            continue
        if not rec.enabled_for_frontend:
            continue
        return pid
    return None


def _ratios_map(derived_ratios_meta: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    if not isinstance(derived_ratios_meta, dict):
        return {}
    r = derived_ratios_meta.get("ratios")
    return r if isinstance(r, dict) else {}


def _cardiovascular_confidence_tier(
    panel: Set[str],
    ratios: Dict[str, Any],
) -> str:
    """Return high | medium | low (mapped from doc bands)."""
    has_tc = "total_cholesterol" in panel
    has_ldl = "ldl_cholesterol" in panel
    has_hdl = "hdl_cholesterol" in panel
    has_tg = "triglycerides" in panel
    ratio_keys = {str(k) for k in ratios.keys()} if ratios else set()
    has_ratio = bool(
        ratio_keys
        & {
            "tc_hdl_ratio",
            "tg_hdl_ratio",
            "ldl_hdl_ratio",
            "non_hdl_cholesterol",
        }
    )
    if has_tc and has_ldl and has_hdl and has_tg and has_ratio:
        return "high"
    if has_tc and has_ldl and has_hdl and (has_tg or has_ratio):
        return "high"
    if has_tc and has_ldl and has_hdl:
        return "medium"
    if has_tc and has_ldl:
        return "low"
    return "low"


def _metabolic_blood_sugar_confidence_tier(
    panel: Set[str],
    ratios: Dict[str, Any],
) -> str:
    has_g = "glucose" in panel
    has_a1c = "hba1c" in panel
    has_ins = "insulin" in panel
    has_tg = "triglycerides" in panel
    has_tyg = "tyg_index" in ratios or "tyg" in str(ratios.keys()).lower()
    if has_g and has_a1c and has_ins and (has_tg or has_tyg):
        return "high"
    if has_g and has_a1c and (has_tg or has_ins):
        return "high"
    if has_g and has_a1c:
        return "medium"
    if has_g or has_a1c:
        return "low"
    return "low"


def _liver_confidence_tier_domain(panel: Set[str]) -> str:
    """Wave 1 liver: count hepatic pool; doc DOMAIN_NARRATIVE_CONTRACT_WAVE1 §3.3."""
    present = [m for m in _HEP_CONFIDENCE_POOL if m in panel]
    n = len(present)
    has_alt = "alt" in panel
    if not has_alt:
        return "low"
    s = set(present)
    if s >= {"alt", "ast", "ggt", "alp", "albumin"}:
        return "high"
    if s >= {"alt", "ast", "ggt"} or (n >= 4 and "ast" in s):
        return "high"
    if s >= {"alt", "ast"}:
        return "medium"
    return "low"


def _merge_tier_rail_and_domain(
    rail_tier: str,
    domain_tier: str,
) -> str:
    order = {"low": 0, "medium": 1, "high": 2}
    a = order.get(rail_tier, 0)
    b = order.get(domain_tier, 0)
    m = min(a, b)
    for k, v in order.items():
        if v == m:
            return k
    return "low"


def _missing_for_rail(hss: Dict[str, Any], system_key: str) -> List[str]:
    data = _system_rail_data(hss, system_key)
    mb = data.get("missing_biomarkers")
    if not isinstance(mb, list):
        return []
    return sorted({str(x) for x in mb if str(x).strip()})


_WAVE1_PLAIN_DESCRIPTOR: Dict[str, str] = {
    "wave1_cardiovascular": "Heart, arteries and circulation",
    "wave1_blood_sugar": "Long-term blood sugar pattern",
    "wave1_liver": "Liver health from your blood markers",
    "wave1_kidney": "Kidney filtration markers from your blood test",
    "wave1_blood_iron_oxygen": "Red-cell and oxygen-carrying markers from your blood test",
}


def _evidence_completeness_for_rail(
    hss: Dict[str, Any],
    system_key: str,
    missing_marker_ids: List[str],
) -> Tuple[int, int]:
    """
    DOMAIN-UX1A: derive completeness from existing rail scored markers + missing list.
    denominator = scored on rail + missing; numerator = scored on rail.

    LAUNCH-CORE-1: prefer ``_evidence_completeness_from_subsystems`` when Wave 1
    compiled subsystem rows are available (card summary must match expanded detail).
    """
    data = _system_rail_data(hss, system_key)
    bs = data.get("biomarker_scores")
    scored_count = len(bs) if isinstance(bs, list) else 0
    missing_count = len(missing_marker_ids)
    denominator = scored_count + missing_count
    numerator = scored_count
    return numerator, denominator


def _evidence_completeness_from_subsystems(subsystems: Sequence[Any]) -> Tuple[int, int]:
    """
    LAUNCH-CORE-1: union of compiled subsystem included + missing marker ids.

    Card summary completeness must match expanded subsystem evidence (no frontend recompute).
    """
    included: Set[str] = set()
    expected: Set[str] = set()
    for row in subsystems:
        for mid in getattr(row, "included_marker_ids", []) or []:
            if str(mid).strip():
                included.add(str(mid).strip())
                expected.add(str(mid).strip())
        for mid in getattr(row, "missing_marker_ids", []) or []:
            if str(mid).strip():
                expected.add(str(mid).strip())
    if not expected:
        return 0, 0
    return len(included), len(expected)


def _evidence_completeness_from_flat_domain(flat: Any) -> Tuple[int, int]:
    """
    KB-UTIL-1: liver flat card summary completeness must match flat_domain_evidence panel rows.
    """
    included = {
        str(mid).strip()
        for mid in (getattr(flat, "included_marker_ids", None) or [])
        if str(mid).strip()
    }
    missing = {
        str(mid).strip()
        for mid in (getattr(flat, "missing_marker_ids", None) or [])
        if str(mid).strip()
    }
    expected = included | missing
    if not expected:
        return 0, 0
    return len(included), len(expected)


def _evidence_anchor_from_visible_subsystems(
    subsystems: Sequence[Any] | None,
    *,
    domain: str,
    by_id: Dict[str, Any],
    primary_idl: Optional[str],
) -> str:
    """MED-REV-2: card anchor follows visible scored subsystem label when present."""
    if subsystems:
        for sub in subsystems:
            tier = getattr(sub, "visibility_tier", None)
            label = (getattr(sub, "subsystem_label", None) or "").strip()
            if tier == "scored_subsystem" and label:
                return f"Based mainly on: {label}"
    return evidence_anchor_sentence(domain, by_id, primary_idl)


def _wave1_card_contract_extras(
    *,
    domain_id: str,
    hss: Dict[str, Any],
    system_key: str,
    missing_marker_ids: List[str],
    panel_biomarker_ids: Set[str],
) -> Dict[str, Any]:
    rail_data = _system_rail_data(hss, system_key)
    subsystems = assemble_wave1_subsystem_evidence(
        domain_id=domain_id,
        panel_biomarker_ids=panel_biomarker_ids,
        rail_biomarker_scores=rail_data.get("biomarker_scores"),
    )
    if subsystems:
        num, den = _evidence_completeness_from_subsystems(subsystems)
    else:
        num, den = _evidence_completeness_for_rail(hss, system_key, missing_marker_ids)
    return {
        "plain_english_descriptor": _WAVE1_PLAIN_DESCRIPTOR.get(domain_id, ""),
        "evidence_completeness_numerator": num,
        "evidence_completeness_denominator": den,
        "subsystems": subsystems or None,
    }


def _wave1_aligned_drivers_meta(
    rows: List[ConsumerDomainScoreV1],
    sig_rows: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    D-6: Same evidence basis as Wave 1 cards — primary_metrics from active signals in each domain.
    Frontend 'What's driving this' should prefer this over independent cluster arbitration for Wave 1.
    """
    by_domain: Dict[str, List[str]] = {}
    ordered_keys: List[str] = []
    for d in rows:
        acc: List[str] = []
        want = set(d.active_signal_ids)
        for sr in sig_rows:
            if str(sr.get("signal_id", "")) not in want:
                continue
            if not _active_signal_state(str(sr.get("signal_state", ""))):
                continue
            pm = str(sr.get("primary_metric", "")).strip()
            if pm and pm not in acc:
                acc.append(pm)
        by_domain[d.domain_id] = acc[:8]
        for k in acc:
            if k not in ordered_keys:
                ordered_keys.append(k)
    return {
        "schema": "wave1_aligned_drivers_v1",
        "biomarker_keys": ordered_keys[:16],
        "by_domain": by_domain,
    }


def assemble_consumer_domain_scores_v1(
    *,
    scoring_result: Dict[str, Any],
    insight_graph: Any,
    idl_bundle: Optional[InterpretationDisplayLayerBundleV1],
    derived_ratios_meta: Optional[Dict[str, Any]],
    panel_biomarker_ids: Set[str],
    narrative_report_v1: Any = None,
    insight_results: Optional[List[Dict[str, Any]]] = None,
    intervention_cv_suffix: str = "",
) -> Tuple[List[ConsumerDomainScoreV1], Dict[str, Any]]:
    """
    Build five Wave 1 domain rows. Always returns five entries in stable order:
    cardiovascular, blood sugar, liver, kidney, blood / iron / oxygen.

    D-2: Populates consumer narrative fields from deterministic sources (IDL, D-1 bands/tiers, insights).
    D-6: Returns (rows, wave1_aligned_drivers_meta) for a single narrative authority + driving-strip alignment.
    """
    hss = _health_systems(scoring_result)
    sig_rows = _iter_signal_results(insight_graph)
    by_id = idl_records_index(idl_bundle)
    ratios = _ratios_map(derived_ratios_meta)
    cap: Dict[str, int] = {}
    sc_raw = dict(getattr(insight_graph, "system_capacity_scores", {}) or {})
    for k, v in sc_raw.items():
        try:
            cap[str(k)] = int(v)
        except (TypeError, ValueError):
            continue
    # Burden: hepatic only for liver context (never `liver`)
    hepatic_cap = cap.get(_BURDEN_HEPATIC)
    cardio_cap = cap.get("cardiovascular")
    metabolic_cap = cap.get("metabolic")

    cluster_conf = _cluster_confidence_map(insight_graph)

    def cv_block() -> ConsumerDomainScoreV1:
        data = _system_rail_data(hss, _RAIL_CARDIOVASCULAR)
        raw_100 = _as_float_0_100(data.get("overall_score"))
        score_01 = raw_100 / 100.0
        band = _band_label_from_0_100(raw_100)
        tier_doc = _cardiovascular_confidence_tier(panel_biomarker_ids, ratios)
        rail_cc = cluster_conf.get("cardiovascular")
        tier_rail = "medium"
        if rail_cc is not None:
            if rail_cc >= 0.85:
                tier_rail = "high"
            elif rail_cc < 0.5:
                tier_rail = "low"
        tier = _merge_tier_rail_and_domain(tier_rail, tier_doc)
        missing = _missing_for_rail(hss, _RAIL_CARDIOVASCULAR)
        sids = _collect_signal_ids(sig_rows, _is_wave1_cardiovascular)
        ev: Dict[str, Any] = {
            "layer3_system_pressure_id": "cardiovascular__system_pressure",
            "burden_capacity_cardiovascular": cardio_cap,
            "derived_ratio_keys": sorted(ratios.keys()) if ratios else [],
        }
        _cv_extras = _wave1_card_contract_extras(
            domain_id="wave1_cardiovascular",
            hss=hss,
            system_key=_RAIL_CARDIOVASCULAR,
            missing_marker_ids=missing,
            panel_biomarker_ids=panel_biomarker_ids,
        )
        _lipid_visible = cv_uses_lipid_subsystem_narrative_authority(_cv_extras.get("subsystems"))
        if _lipid_visible:
            idl = _select_primary_idl(idl_bundle, (_IDL_ORDER_CV[0],))
            _contrib = cv_contributor_for_lipid_visible_card(by_id, sids, sig_rows, idl)
            _cons = cv_consequence_for_lipid_visible_card(
                by_id, sids, sig_rows, idl, contributor_sentence=_contrib
            )
        else:
            idl = _select_primary_idl(idl_bundle, _IDL_ORDER_CV)
            _contrib = cv_contributor_primary(by_id, sids, sig_rows, idl)
            _cons = cv_consequence_primary(by_id, sids, sig_rows, idl)
        _suffix = (intervention_cv_suffix or "").strip()
        _cons_cv = (_cons + " " + _suffix).strip() if _suffix else _cons
        _primary_rec = idl_record(by_id, idl) if idl else None
        return ConsumerDomainScoreV1(
            domain_id="wave1_cardiovascular",
            card_schema_version="1.2",
            consumer_label="Cardiovascular health",
            clinical_label="Cardiometabolic / Vascular Risk Status",
            score=score_01,
            band_label=band,
            confidence_tier=cast(ConfidenceTierV1, tier),
            active_signal_ids=sids,
            primary_idl_record_id=idl,
            missing_marker_ids=missing,
            source_track="base:scoring_rail:cardiovascular;context:optional_burden_capacity:cardiovascular;narrative:primary_idl_single_authority_d6",
            caveat_flags=[],
            contributing_system_keys=["cardiovascular"],
            raw_evidence_refs=ev,
            headline_sentence=headline_cv_coherent(band, _contrib, _cons_cv, _primary_rec),
            contributor_sentence=_contrib,
            confidence_sentence=confidence_sentence_cv_coherent(tier, _contrib),
            consequence_sentence=_cons_cv,
            next_step_sentence=next_step_cardiovascular(
                insight_results,
                narrative_report_v1,
            ),
            evidence_anchor_sentence=_evidence_anchor_from_visible_subsystems(
                _cv_extras.get("subsystems"),
                domain="cv",
                by_id=by_id,
                primary_idl=idl,
            ),
            **_cv_extras,
        )

    def met_block() -> ConsumerDomainScoreV1:
        data = _system_rail_data(hss, _RAIL_METABOLIC)
        raw_100 = _as_float_0_100(data.get("overall_score"))
        score_01 = raw_100 / 100.0
        band = _band_label_from_0_100(raw_100)
        tier_doc = _metabolic_blood_sugar_confidence_tier(panel_biomarker_ids, ratios)
        rail_cc = cluster_conf.get("metabolic")
        tier_rail = "medium"
        if rail_cc is not None:
            if rail_cc >= 0.85:
                tier_rail = "high"
            elif rail_cc < 0.5:
                tier_rail = "low"
        tier = _merge_tier_rail_and_domain(tier_rail, tier_doc)
        missing = _missing_for_rail(hss, _RAIL_METABOLIC)
        sids = _collect_signal_ids(sig_rows, _is_wave1_blood_sugar)
        idl = _select_primary_idl(idl_bundle, _IDL_ORDER_MET)
        caveats: List[str] = []
        ev: Dict[str, Any] = {
            "layer3_system_pressure_id": "metabolic__system_pressure",
            "burden_capacity_metabolic": metabolic_cap,
        }
        sset = set(sids)
        _met_extras = _wave1_card_contract_extras(
            domain_id="wave1_blood_sugar",
            hss=hss,
            system_key=_RAIL_METABOLIC,
            missing_marker_ids=missing,
            panel_biomarker_ids=panel_biomarker_ids,
        )
        _m_contrib = met_contributor_primary(by_id, sset, sig_rows, idl)
        if met_uses_glycaemic_subsystem_narrative_authority(_met_extras.get("subsystems")):
            _m_cons = met_consequence_for_glycaemic_visible_card(
                by_id,
                sset,
                sig_rows,
                idl,
                contributor_sentence=_m_contrib,
                band_label=band,
            )
        else:
            _m_cons = met_consequence_primary(by_id, sset, sig_rows, idl)
        _m_primary_rec = idl_record(by_id, idl) if idl else None
        return ConsumerDomainScoreV1(
            domain_id="wave1_blood_sugar",
            card_schema_version="1.2",
            consumer_label="Blood sugar control",
            clinical_label="Glycaemic Regulation / Insulin Resistance Status",
            score=score_01,
            band_label=band,
            confidence_tier=cast(ConfidenceTierV1, tier),
            active_signal_ids=sids,
            primary_idl_record_id=idl,
            missing_marker_ids=missing,
            source_track="base:scoring_rail:metabolic(blood_sugar);narrative:primary_idl_single_authority_d6",
            caveat_flags=caveats,
            contributing_system_keys=["metabolic"],
            raw_evidence_refs=ev,
            headline_sentence=headline_met_coherent(band, _m_contrib, _m_cons, _m_primary_rec),
            contributor_sentence=_m_contrib,
            confidence_sentence=confidence_sentence_for(tier, "met"),
            consequence_sentence=_m_cons,
            next_step_sentence=next_step_blood_sugar(
                insight_results,
                narrative_report_v1,
            ),
            evidence_anchor_sentence=_evidence_anchor_from_visible_subsystems(
                _met_extras.get("subsystems"),
                domain="met",
                by_id=by_id,
                primary_idl=idl,
            ),
            **_met_extras,
        )

    def liv_block() -> ConsumerDomainScoreV1:
        data = _system_rail_data(hss, _RAIL_LIVER)
        base_100 = _as_float_0_100(data.get("overall_score"))
        # Blueprint: min(liver_rail, hepatic capacity) as floor; both 0-100 "higher is better"
        blended_100 = base_100
        if hepatic_cap is not None:
            blended_100 = min(base_100, float(hepatic_cap))
        score_01 = blended_100 / 100.0
        band = _band_label_from_0_100(blended_100)
        dom_tier = _liver_confidence_tier_domain(panel_biomarker_ids)
        # D-6: User-facing liver tier follows domain-level hepatic marker depth, not cluster rail floor.
        tier = cast(ConfidenceTierV1, dom_tier)
        rail_cc = cluster_conf.get("hepatic")
        missing = list(_missing_for_rail(hss, _RAIL_LIVER))
        if _liver_panel_has_bilirubin_coverage(panel_biomarker_ids):
            missing = [x for x in missing if x not in ("bilirubin", "total_bilirubin")]
        for m in ("ast", "ggt", "alp", "albumin"):
            if m not in panel_biomarker_ids and m not in missing:
                missing.append(m)
        if not _liver_panel_has_bilirubin_coverage(panel_biomarker_ids):
            if "bilirubin" not in missing:
                missing.append("bilirubin")
        missing = sorted(set(missing))
        sids = _collect_signal_ids(sig_rows, _is_wave1_liver)
        idl = _select_primary_idl(idl_bundle, _IDL_ORDER_LIV)
        caveats: List[str] = list(_LIVER_CAVEAT_USER_LINES)
        _l_head = headline_liv(band)
        ev: Dict[str, Any] = {
            "layer3_system_pressure_id": "hepatic__system_pressure",
            "burden_capacity_hepatic": hepatic_cap,
            "scoring_rail_liver_overall_0_100": base_100,
            "blended_with_hepatic_capacity": hepatic_cap is not None,
            "cluster_confidence_hepatic_rail": rail_cc,
            "caveat_keys_internal": [
                "enzyme_limited_assessment",
                "hepatic_burden_uses_key_hepatic_not_liver_scoring_rail",
            ],
        }
        ckeys = ["liver"]
        if hepatic_cap is not None:
            ckeys.append("hepatic")
        _l_contrib = liv_contributor_primary(by_id, sids, sig_rows, idl)
        _l_cons = liv_consequence_primary(
            by_id,
            idl,
            contributor_sentence=_l_contrib,
            headline_sentence=_l_head,
            active_liver_signal_ids=sids,
            band_label=band,
        )
        _liv_extras = _wave1_card_contract_extras(
            domain_id="wave1_liver",
            hss=hss,
            system_key=_RAIL_LIVER,
            missing_marker_ids=missing,
            panel_biomarker_ids=panel_biomarker_ids,
        )
        _liv_flat = assemble_wave1_flat_domain_evidence(
            domain_id="wave1_liver",
            panel_biomarker_ids=panel_biomarker_ids,
            rail_biomarker_scores=_system_rail_data(hss, _RAIL_LIVER).get("biomarker_scores"),
        )
        if _liv_flat is not None:
            num, den = _evidence_completeness_from_flat_domain(_liv_flat)
            _liv_extras["evidence_completeness_numerator"] = num
            _liv_extras["evidence_completeness_denominator"] = den
        return ConsumerDomainScoreV1(
            domain_id="wave1_liver",
            card_schema_version="1.2",
            consumer_label="Liver health",
            clinical_label="Hepatic-Metabolic Strain Status",
            score=score_01,
            band_label=band,
            confidence_tier=cast(ConfidenceTierV1, tier),
            active_signal_ids=sids,
            primary_idl_record_id=idl,
            missing_marker_ids=missing,
            source_track=(
                "base:scoring_rail:liver;context:burden_capacity:hepatic"
                + "(explicit_key_split_from_scoring_rail_liver);narrative:primary_idl_single_authority_d6"
            ),
            caveat_flags=caveats,
            contributing_system_keys=ckeys,
            raw_evidence_refs=ev,
            headline_sentence=_l_head,
            contributor_sentence=_l_contrib,
            confidence_sentence=confidence_sentence_for(
                tier, "liver", panel_biomarker_ids=panel_biomarker_ids
            ),
            consequence_sentence=_l_cons,
            next_step_sentence=next_step_liver(
                insight_results,
                narrative_report_v1,
            ),
            evidence_anchor_sentence=evidence_anchor_sentence("liver", by_id, idl),
            flat_domain_evidence=_liv_flat,
            **_liv_extras,
        )

    def ren_block() -> ConsumerDomainScoreV1:
        data = _system_rail_data(hss, _RAIL_KIDNEY)
        raw_100 = _as_float_0_100(data.get("overall_score"))
        score_01 = raw_100 / 100.0
        band = _band_label_from_0_100(raw_100)
        tier = cast(ConfidenceTierV1, _kidney_confidence_tier(panel_biomarker_ids))
        missing = _missing_for_rail(hss, _RAIL_KIDNEY)
        sids = _collect_signal_ids(sig_rows, _is_wave1_kidney)
        idl = _select_primary_idl(idl_bundle, _IDL_ORDER_REN)
        ev: Dict[str, Any] = {
            "layer3_system_pressure_id": "renal__system_pressure",
        }
        _ren_extras = _wave1_card_contract_extras(
            domain_id="wave1_kidney",
            hss=hss,
            system_key=_RAIL_KIDNEY,
            missing_marker_ids=missing,
            panel_biomarker_ids=panel_biomarker_ids,
        )
        _r_contrib = ren_contributor_primary(by_id, sids, sig_rows, idl)
        _r_cons = ren_consequence_primary(
            by_id,
            idl,
            contributor_sentence=_r_contrib,
            active_renal_signal_ids=sids,
        )
        return ConsumerDomainScoreV1(
            domain_id="wave1_kidney",
            card_schema_version="1.2",
            consumer_label="Kidney function",
            clinical_label="Renal Filtration / Kidney Function Context",
            score=score_01,
            band_label=band,
            confidence_tier=tier,
            active_signal_ids=sids,
            primary_idl_record_id=idl,
            missing_marker_ids=missing,
            source_track="base:scoring_rail:kidney;narrative:primary_idl_single_authority_p1_2",
            caveat_flags=[],
            contributing_system_keys=["kidney"],
            raw_evidence_refs=ev,
            headline_sentence=headline_ren(band),
            contributor_sentence=_r_contrib,
            confidence_sentence=confidence_sentence_for(tier, "kidney"),
            consequence_sentence=_r_cons,
            next_step_sentence=next_step_kidney(
                insight_results,
                narrative_report_v1,
            ),
            evidence_anchor_sentence=_evidence_anchor_from_visible_subsystems(
                _ren_extras.get("subsystems"),
                domain="kidney",
                by_id=by_id,
                primary_idl=idl,
            ),
            **_ren_extras,
        )

    def bio_block() -> ConsumerDomainScoreV1:
        data = _system_rail_data(hss, _RAIL_CBC)
        raw_100 = _as_float_0_100(data.get("overall_score"))
        score_01 = raw_100 / 100.0
        band = _band_label_from_0_100(raw_100)
        tier = cast(ConfidenceTierV1, _bio_confidence_tier(panel_biomarker_ids))
        missing = _missing_for_rail(hss, _RAIL_CBC)
        sids = _collect_signal_ids(sig_rows, _is_wave1_blood_iron_oxygen)
        idl = None
        ev: Dict[str, Any] = {
            "layer3_system_pressure_id": "hematological__system_pressure",
        }
        _bio_extras = _wave1_card_contract_extras(
            domain_id="wave1_blood_iron_oxygen",
            hss=hss,
            system_key=_RAIL_CBC,
            missing_marker_ids=missing,
            panel_biomarker_ids=panel_biomarker_ids,
        )
        _b_contrib = bio_contributor_primary(by_id, sids, sig_rows, idl)
        _b_cons = bio_consequence_primary(
            by_id,
            idl,
            contributor_sentence=_b_contrib,
            active_bio_signal_ids=sids,
        )
        return ConsumerDomainScoreV1(
            domain_id="wave1_blood_iron_oxygen",
            card_schema_version="1.2",
            consumer_label="Blood / iron / oxygen",
            clinical_label="Red-Cell / Oxygen-Carrying Marker Context",
            score=score_01,
            band_label=band,
            confidence_tier=tier,
            active_signal_ids=sids,
            primary_idl_record_id=idl,
            missing_marker_ids=missing,
            source_track="base:scoring_rail:cbc;narrative:primary_idl_single_authority_p1_3",
            caveat_flags=[],
            contributing_system_keys=["cbc"],
            raw_evidence_refs=ev,
            headline_sentence=headline_bio(band),
            contributor_sentence=_b_contrib,
            confidence_sentence=confidence_sentence_for(tier, "bio"),
            consequence_sentence=_b_cons,
            next_step_sentence=next_step_blood_iron_oxygen(
                insight_results,
                narrative_report_v1,
            ),
            evidence_anchor_sentence=_evidence_anchor_from_visible_subsystems(
                _bio_extras.get("subsystems"),
                domain="bio",
                by_id=by_id,
                primary_idl=idl,
            ),
            **_bio_extras,
        )

    out_rows = [cv_block(), met_block(), liv_block(), ren_block(), bio_block()]
    return out_rows, _wave1_aligned_drivers_meta(out_rows, sig_rows)