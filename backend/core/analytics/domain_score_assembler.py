"""
D-1 — Deterministic Wave 1 customer domain score + confidence assembly (Strategy A).

Translation layer only: reads scoring rails, burden/capacity, signals, IDL. Does not
mutate engines. Scoring track vs burden/capacity track is explicit in source_track and
raw_evidence_refs to avoid silent calibration mixing.

Liver: scoring key is ``liver`` (scoring_policy.yaml); burden/capacity key is ``hepatic``
(system_burden_engine / InsightGraph.system_capacity_scores). Never read capacity using ``liver``.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Set, Tuple, cast

from core.analytics.domain_narrative_wave1 import (
    confidence_sentence_cv_coherent,
    confidence_sentence_for,
    cv_consequence,
    cv_contributor,
    evidence_anchor_sentence,
    headline_cv_coherent,
    headline_liv,
    headline_met_coherent,
    idl_records_index,
    liv_consequence,
    liv_contributor,
    met_consequence,
    met_contributor,
    next_step_blood_sugar,
    next_step_cardiovascular,
    next_step_liver,
)
from core.contracts.interpretation_display_layer_v1 import InterpretationDisplayLayerBundleV1
from core.models.results import ConfidenceTierV1, ConsumerDomainScoreV1

# --- Scoring policy rails (authoritative names) ---
_RAIL_CARDIOVASCULAR = "cardiovascular"
_RAIL_METABOLIC = "metabolic"
_RAIL_LIVER = "liver"
_BURDEN_HEPATIC = "hepatic"

# D-4: user-safe caveat lines (replaces internal slug list for retail cards)
_LIVER_CAVEAT_USER_LINES = (
    "Only the liver markers available on this panel are used here; a fuller liver profile would narrow the picture.",
    "Liver load is also interpreted with related metabolic (hepatic) context, not from the liver score line alone.",
)

# Wave 1 IDL selection order (per docs/DOMAIN_NARRATIVE_CONTRACT_WAVE1.md)
_IDL_ORDER_CV = ("ph_vascular_hcy_inflammation_v1", "ph_lipid_residual_ldl_favourable_transport_v1")
_IDL_ORDER_MET = ("ph_hba1c_metabolic_stress_v1", "ph_metabolic_early_ir_v1")
_IDL_ORDER_LIV = ("ph_hepatic_alt_inflammatory_v1",)

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


def assemble_consumer_domain_scores_v1(
    *,
    scoring_result: Dict[str, Any],
    insight_graph: Any,
    idl_bundle: Optional[InterpretationDisplayLayerBundleV1],
    derived_ratios_meta: Optional[Dict[str, Any]],
    panel_biomarker_ids: Set[str],
    narrative_report_v1: Any = None,
    insight_results: Optional[List[Dict[str, Any]]] = None,
) -> List[ConsumerDomainScoreV1]:
    """
    Build three Wave 1 domain rows. Always returns three entries in stable order:
    cardiovascular, blood sugar, liver.

    D-2: Populates consumer narrative fields from deterministic sources (IDL, D-1 bands/tiers, insights).
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
        idl = _select_primary_idl(idl_bundle, _IDL_ORDER_CV)
        ev: Dict[str, Any] = {
            "layer3_system_pressure_id": "cardiovascular__system_pressure",
            "burden_capacity_cardiovascular": cardio_cap,
            "derived_ratio_keys": sorted(ratios.keys()) if ratios else [],
        }
        _contrib = cv_contributor(by_id, sids, sig_rows)
        _cons = cv_consequence(by_id, sids, sig_rows)
        return ConsumerDomainScoreV1(
            domain_id="wave1_cardiovascular",
            consumer_label="Cardiovascular health",
            clinical_label="Cardiometabolic / Vascular Risk Status",
            score=score_01,
            band_label=band,
            confidence_tier=cast(ConfidenceTierV1, tier),
            active_signal_ids=sids,
            primary_idl_record_id=idl,
            missing_marker_ids=missing,
            source_track="base:scoring_rail:cardiovascular;context:optional_burden_capacity:cardiovascular",
            caveat_flags=[],
            contributing_system_keys=["cardiovascular"],
            raw_evidence_refs=ev,
            headline_sentence=headline_cv_coherent(band, _contrib, _cons),
            contributor_sentence=_contrib,
            confidence_sentence=confidence_sentence_cv_coherent(tier, _contrib),
            consequence_sentence=_cons,
            next_step_sentence=next_step_cardiovascular(
                insight_results,
                narrative_report_v1,
            ),
            evidence_anchor_sentence=evidence_anchor_sentence("cv", by_id, idl),
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
        _m_contrib = met_contributor(by_id, sset, sig_rows)
        _m_cons = met_consequence(by_id, sset, sig_rows)
        return ConsumerDomainScoreV1(
            domain_id="wave1_blood_sugar",
            consumer_label="Blood sugar control",
            clinical_label="Glycaemic Regulation / Insulin Resistance Status",
            score=score_01,
            band_label=band,
            confidence_tier=cast(ConfidenceTierV1, tier),
            active_signal_ids=sids,
            primary_idl_record_id=idl,
            missing_marker_ids=missing,
            source_track="base:scoring_rail:metabolic(blood_sugar);not_metabolic_burden_electrolyte_track",
            caveat_flags=caveats,
            contributing_system_keys=["metabolic"],
            raw_evidence_refs=ev,
            headline_sentence=headline_met_coherent(band, _m_contrib, _m_cons),
            contributor_sentence=_m_contrib,
            confidence_sentence=confidence_sentence_for(tier, "met"),
            consequence_sentence=_m_cons,
            next_step_sentence=next_step_blood_sugar(
                insight_results,
                narrative_report_v1,
            ),
            evidence_anchor_sentence=evidence_anchor_sentence("met", by_id, idl),
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
        rail_cc = cluster_conf.get("hepatic")
        tier_rail = "medium"
        if rail_cc is not None:
            if rail_cc >= 0.85:
                tier_rail = "high"
            elif rail_cc < 0.5:
                tier_rail = "low"
        tier = _merge_tier_rail_and_domain(tier_rail, dom_tier)
        missing = _missing_for_rail(hss, _RAIL_LIVER)
        for m in ("ast", "ggt", "alp", "albumin", "total_bilirubin"):
            if m not in panel_biomarker_ids and m not in missing:
                missing.append(m)
        missing = sorted(set(missing))
        sids = _collect_signal_ids(sig_rows, _is_wave1_liver)
        idl = _select_primary_idl(idl_bundle, _IDL_ORDER_LIV)
        caveats: List[str] = list(_LIVER_CAVEAT_USER_LINES)
        ev: Dict[str, Any] = {
            "layer3_system_pressure_id": "hepatic__system_pressure",
            "burden_capacity_hepatic": hepatic_cap,
            "scoring_rail_liver_overall_0_100": base_100,
            "blended_with_hepatic_capacity": hepatic_cap is not None,
            "caveat_keys_internal": [
                "enzyme_limited_assessment",
                "hepatic_burden_uses_key_hepatic_not_liver_scoring_rail",
            ],
        }
        ckeys = ["liver"]
        if hepatic_cap is not None:
            ckeys.append("hepatic")
        return ConsumerDomainScoreV1(
            domain_id="wave1_liver",
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
                + "(explicit_key_split_from_scoring_rail_liver)"
            ),
            caveat_flags=caveats,
            contributing_system_keys=ckeys,
            raw_evidence_refs=ev,
            headline_sentence=headline_liv(band),
            contributor_sentence=liv_contributor(by_id, sids, sig_rows),
            confidence_sentence=confidence_sentence_for(tier, "liver"),
            consequence_sentence=liv_consequence(by_id),
            next_step_sentence=next_step_liver(
                insight_results,
                narrative_report_v1,
            ),
            evidence_anchor_sentence=evidence_anchor_sentence("liver", by_id, idl),
        )

    return [cv_block(), met_block(), liv_block()]