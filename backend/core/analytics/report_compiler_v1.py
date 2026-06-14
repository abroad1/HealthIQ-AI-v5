"""
KB-S32 deterministic report compiler.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Tuple

import yaml

from core.contracts.report_v1 import (
    ReportActionsV1,
    ReportInterventionV1,
    ReportMetaV1,
    ReportTopChainV1,
    ReportTopFindingV1,
    ReportV1,
)
from core.contracts.intervention_annotation_v1 import InterventionAnnotationsV1
from core.contracts.clinician_report_v1 import (
    ClinicianReportV1,
    ClinicianHeaderV1,
    ClinicianSectionsV1,
    ConfirmatoryTestItem,
    DataQualityV1,
    EvidenceItem,
    HypothesisV1,
    MissingDataItem,
    Page1SummaryBlockV1,
    RootCauseFindingV1,
)
from core.analytics.intervention_annotation_compiler_v1 import build_intervention_annotations_v1
from core.analytics.intervention_annotation_formatter_v1 import (
    format_intervention_annotation_clinician_page1_v1,
)
from core.analytics.medication_caveat_assembler_v1 import (
    build_medication_supplement_interpretation_caveat,
)
from core.analytics.consumer_prose_safety_v1 import (
    format_confidence_consumer,
    format_runner_up_topic_consumer,
    format_runner_up_why_consumer,
)
from core.analytics.output_authority_provenance_builder_v1 import (
    build_report_output_authority_provenance_v1,
    is_governed_hypothesis,
)
from core.analytics.root_cause_compiler_v1 import compile_root_cause_v1
from core.knowledge.load_confirmatory_tests_registry import load_confirmatory_tests_registry_v1


_STATE_RANK = {"at_risk": 4, "suboptimal": 3, "optimal": 2, "unknown": 1}

_ALLOWED_HYPOTHESIS_SAFETY_CLASSES = frozenset(
    {"monitoring", "clinician_referral", "lifestyle"}
)


def _normalise_hypothesis_safety_class(raw: Any) -> Literal["monitoring", "clinician_referral", "lifestyle"]:
    """
    Map legacy/internal root-cause safety_class tokens to clinician_report_v1 HypothesisV1 literals.
    """
    token = str(raw or "").strip().lower()
    if token == "informational":
        return "monitoring"
    if token in _ALLOWED_HYPOTHESIS_SAFETY_CLASSES:
        return token  # type: ignore[return-value]
    return "monitoring"

# KB-S54B Phase 2a — report-layer ordering under PRIMARY_CONCERN_AND_RANKED_AMBIGUITY_POLICY v1.
TOP_FINDINGS_RANKING_POLICY_VERSION = (
    "PRIMARY_CONCERN_AND_RANKED_AMBIGUITY_POLICY_V1+report-runtime-2a-v1"
)

PrimaryConcernMode = Literal["distinct_lead", "near_tie_ambiguity", "technical_tiebreak_lead"]


def _humanize_signal_id(signal_id: str) -> str:
    """Consumer-facing label: strip internal prefixes and use title-style words (no raw snake_case IDs)."""
    s = str(signal_id or "").strip()
    if s.startswith("signal_"):
        s = s[7:]
    parts = [p for p in s.replace("-", "_").split("_") if p]
    if not parts:
        return "This pattern"
    return " ".join(w[:1].upper() + w[1:] if w else "" for w in parts)


def _state_consumer_phrase(state: str) -> str:
    """Plain-English gloss for signal_state in headlines (not clinical staging)."""
    key = str(state or "").strip().lower()
    return {
        "at_risk": "warrants attention on this panel",
        "suboptimal": "also stood out on this panel",
        "optimal": "looks favourable on this panel",
        "unknown": "is not fully characterised from this panel alone",
    }.get(key, f"is described as {key.replace('_', ' ')} on this panel")


def _normalize_confidence_reasons_tuple(row: Dict[str, Any]) -> Tuple[str, ...]:
    reasons = row.get("confidence_reasons")
    if not isinstance(reasons, list):
        return tuple()
    return tuple(sorted(str(x) for x in reasons if str(x).strip()))


def _supporting_marker_count(row: Dict[str, Any]) -> int:
    supporting = row.get("supporting_markers")
    if not isinstance(supporting, list):
        return 0
    return sum(1 for x in supporting if str(x).strip())


def _top_finding_sort_tuple(row: Dict[str, Any]) -> Tuple[Any, ...]:
    """Deterministic total order: state, confidence, evidence density, then technical keys.

    Lexicographic ``signal_id`` is only the final stabiliser when all governed comparisons tie.
    """
    state = str(row.get("signal_state", "unknown")).strip() or "unknown"
    conf = _safe_float(row.get("confidence"), 0.0)
    signal_id = str(row.get("signal_id", "")).strip()
    primary_metric = str(row.get("primary_metric", "")).strip()
    reasons_key = _normalize_confidence_reasons_tuple(row)
    supp_n = _supporting_marker_count(row)
    return (
        -_STATE_RANK.get(state, 1),
        -conf,
        -supp_n,
        reasons_key,
        primary_metric,
        signal_id,
    )


def _signal_id_fallback_invoked_for_top_findings(rows: List[Dict[str, Any]]) -> bool:
    """True when any two rows share the same governed sort prefix but differ in ``signal_id``."""
    by_prefix: Dict[Tuple[Any, ...], List[str]] = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        full = _top_finding_sort_tuple(row)
        prefix, sid = full[:-1], full[-1]
        by_prefix.setdefault(prefix, []).append(sid)
    return any(len(set(sids)) > 1 for sids in by_prefix.values())


def _technical_tie_bucket_signal_ids(top_findings: List[Dict[str, Any]]) -> List[str]:
    """Signal ids in ``top_findings`` that share the same governed tie prefix as the lead row."""
    if not top_findings:
        return []
    primary = top_findings[0]
    if not isinstance(primary, dict):
        return []
    prefix = _top_finding_sort_tuple(primary)[:-1]
    ids = {
        str(r.get("signal_id", "")).strip()
        for r in top_findings
        if isinstance(r, dict)
        and _top_finding_sort_tuple(r)[:-1] == prefix
        and str(r.get("signal_id", "")).strip()
    }
    return sorted(ids)


def _near_tie_cluster_in_top3(top_findings: List[Dict[str, Any]], *, epsilon: float = 0.05) -> List[str]:
    """Signals in the top three that tie with the lead on state and near-equal confidence."""
    if len(top_findings) < 2:
        return []
    primary = top_findings[0]
    if not isinstance(primary, dict):
        return []
    ps = str(primary.get("signal_state", "unknown")).strip() or "unknown"
    pc = _safe_float(primary.get("confidence"))
    cluster: set[str] = set()
    pid = str(primary.get("signal_id", "")).strip()
    if pid:
        cluster.add(pid)
    for r in top_findings[1:3]:
        if not isinstance(r, dict):
            continue
        rs = str(r.get("signal_state", "unknown")).strip() or "unknown"
        rc = _safe_float(r.get("confidence"))
        rid = str(r.get("signal_id", "")).strip()
        if not rid:
            continue
        if rs == ps and abs(rc - pc) <= epsilon:
            cluster.add(rid)
    if len(cluster) < 2:
        return []
    return sorted(cluster)


def _page1_policy_key_finding_line(mode: PrimaryConcernMode, co_ids: List[str]) -> str:
    """Secondary clarification for ambiguity/tie modes — plain English, humanized labels only."""
    labels = [_humanize_signal_id(x) for x in co_ids if str(x).strip()]
    tail = ""
    if len(labels) >= 2:
        tail = f" Related patterns in the same tier: {', '.join(labels[:4])}."
    if mode == "near_tie_ambiguity" and len(co_ids) >= 2:
        return (
            "Several findings have similar strength on this panel; the headline highlights one first so discussion "
            "has a clear starting point." + tail
        )[:220]
    if mode == "technical_tiebreak_lead":
        base = (
            "Several findings scored similarly; the first item follows a stable ordering rule so your summary "
            "has a single lead topic."
        )
        if len(labels) >= 2:
            return (base + tail)[:220]
        return (base)[:220]
    return ""


def _resolve_page1_concern_mode(
    top_findings: List[Dict[str, Any]],
    *,
    ranking_signal_id_fallback_invoked: bool,
) -> Tuple[PrimaryConcernMode, List[str]]:
    if ranking_signal_id_fallback_invoked:
        bucket = _technical_tie_bucket_signal_ids(top_findings)
        co = bucket[:4] if len(bucket) >= 2 else []
        return "technical_tiebreak_lead", co

    near = _near_tie_cluster_in_top3(top_findings)
    if len(near) >= 2:
        return "near_tie_ambiguity", near[:4]

    return "distinct_lead", []


def _build_runner_up_page1_fields(
    top_findings: List[Dict[str, Any]],
    concern_mode: PrimaryConcernMode,
) -> Tuple[str, str, str]:
    """
    Surface the competing ranked finding (top_findings[1]) for close-call hero modes.
    Copy is derived only from existing ranked row fields — no new medical claims.
    """
    if concern_mode not in ("near_tie_ambiguity", "technical_tiebreak_lead"):
        return "", "", ""
    if len(top_findings) < 2:
        return "", "", ""
    primary = top_findings[0]
    secondary = top_findings[1]
    if not isinstance(primary, dict) or not isinstance(secondary, dict):
        return "", "", ""
    sec_sid = str(secondary.get("signal_id", "")).strip()
    if not sec_sid:
        return "", "", ""
    pri_sid = str(primary.get("signal_id", "")).strip()
    st = str(secondary.get("signal_state", "unknown")).strip() or "unknown"
    topic = format_runner_up_topic_consumer(_humanize_signal_id(sec_sid), st)[:220]
    pc = _safe_float(primary.get("confidence"))
    sc = _safe_float(secondary.get("confidence"))
    pri_label = _humanize_signal_id(pri_sid) if pri_sid else "the lead pattern"
    sec_label = _humanize_signal_id(sec_sid)
    near_tie = concern_mode == "technical_tiebreak_lead" or abs(pc - sc) <= 0.05
    why = format_runner_up_why_consumer(pri_label, sec_label, near_tie=near_tie)[:280]
    return sec_sid[:120], topic, why


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _load_map_revision() -> str:
    path = _repo_root() / "knowledge_bus" / "interaction_maps" / "interaction_map_v1.yaml"
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return str(payload.get("map_revision", ""))


def _load_safety_contract_version() -> str:
    path = _repo_root() / "knowledge_bus" / "interventions" / "safety_rules_v1.yaml"
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return str(payload.get("schema_version", ""))


def _why_template(signal_id: str, signal_state: str, primary_metric: str) -> str:
    topic = _humanize_signal_id(signal_id)
    metric = str(primary_metric or "").strip().replace("_", " ")
    metric_label = metric.title() if metric else ""
    state_phrase = _state_consumer_phrase(signal_state)
    if metric_label:
        text = f"{topic} {state_phrase}, with {metric_label.lower()} as the main marker on this panel."
    else:
        text = f"{topic} {state_phrase}."
    return text[:200]


def _chain_summary_text(chain_id: str, signals: List[str]) -> str:
    hum = [_humanize_signal_id(s) for s in signals if str(s).strip()]
    joined = " → ".join(hum) if hum else "—"
    return f"Linked pattern ({chain_id}): {joined}."[:200]


def _to_dict(value: Any) -> Dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, dict):
        return value
    if hasattr(value, "model_dump"):
        dumped = value.model_dump()
        return dumped if isinstance(dumped, dict) else {}
    return {}


def _to_list(value: Any) -> List[Any]:
    if isinstance(value, list):
        return value
    return []


def _safe_float(value: Any, default: float = 0.0) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    return default


def _quality_label(reference_range: Dict[str, Any]) -> str:
    min_val = reference_range.get("min")
    max_val = reference_range.get("max")
    has_min = isinstance(min_val, (int, float))
    has_max = isinstance(max_val, (int, float))
    if has_min and has_max:
        if float(min_val) < float(max_val):
            return "complete"
        return "missing"
    if has_min or has_max:
        return "one-sided"
    return "missing"


def _has_usable_range(reference_range: Dict[str, Any]) -> bool:
    return _quality_label(reference_range) in {"complete", "one-sided"}


def _build_biomarker_snapshot(
    biomarker_rows: List[Dict[str, Any]],
) -> Dict[str, Dict[str, Any]]:
    snapshot: Dict[str, Dict[str, Any]] = {}
    for row in biomarker_rows:
        if not isinstance(row, dict):
            continue
        marker_id = str(row.get("biomarker_name", "")).strip()
        if not marker_id:
            continue
        reference_range = row.get("reference_range")
        ref_payload = reference_range if isinstance(reference_range, dict) else {}
        snapshot[marker_id] = {
            "value": row.get("value"),
            "unit": str(row.get("unit", "")).strip(),
            "reference_range": ref_payload,
        }
    return snapshot


def _marker_ready_for_suppression(marker: Dict[str, Any]) -> bool:
    return (
        marker.get("value") is not None
        and bool(str(marker.get("unit", "")).strip())
        and _has_usable_range(_to_dict(marker.get("reference_range")))
    )


def _build_ranking_rationale(hypothesis_row: Dict[str, Any], rank: int) -> str:
    evidence_for = _to_list(hypothesis_row.get("evidence_for"))
    evidence_against = _to_list(hypothesis_row.get("evidence_against"))
    missing_data = _to_list(hypothesis_row.get("missing_data"))

    for_anchor = "available evidence"
    against_anchor = "limited contradictory evidence"

    if evidence_for and isinstance(evidence_for[0], dict):
        marker_refs = [
            str(m).strip()
            for m in _to_list(evidence_for[0].get("marker_refs"))
            if str(m).strip()
        ]
        if marker_refs:
            for_anchor = f"{marker_refs[0]} evidence"

    if evidence_against and isinstance(evidence_against[0], dict):
        marker_refs = [
            str(m).strip()
            for m in _to_list(evidence_against[0].get("marker_refs"))
            if str(m).strip()
        ]
        if marker_refs:
            against_anchor = f"{marker_refs[0]} counter-evidence"
    elif missing_data and isinstance(missing_data[0], dict):
        marker_id = str(missing_data[0].get("marker_id", "")).strip()
        if marker_id:
            against_anchor = f"missing {marker_id} context"

    return f"Ranked #{rank} because {for_anchor}; {against_anchor}."


def _normalise_root_cause_finding(
    finding_row: Dict[str, Any],
) -> RootCauseFindingV1:
    hypotheses_in = [
        row for row in _to_list(finding_row.get("hypotheses")) if isinstance(row, dict)
    ]
    hypotheses_out: List[HypothesisV1] = []
    rank = 0
    for hypothesis_row in hypotheses_in[:4]:
        hypothesis_id = str(hypothesis_row.get("hypothesis_id", "")).strip()
        if not is_governed_hypothesis(hypothesis_id):
            continue
        rank += 1
        evidence_for = [
            EvidenceItem(
                item=str(item.get("item", "")).strip(),
                marker_refs=[str(x) for x in _to_list(item.get("marker_refs")) if str(x).strip()],
            )
            for item in hypothesis_row.get("evidence_for", [])
            if isinstance(item, dict) and str(item.get("item", "")).strip()
        ]
        evidence_against = [
            EvidenceItem(
                item=str(item.get("item", "")).strip(),
                marker_refs=[str(x) for x in _to_list(item.get("marker_refs")) if str(x).strip()],
            )
            for item in hypothesis_row.get("evidence_against", [])
            if isinstance(item, dict) and str(item.get("item", "")).strip()
        ]
        missing_data = [
            MissingDataItem(
                marker_id=str(item.get("marker_id", "")).strip(),
                reason=str(item.get("reason", "")).strip(),
            )
            for item in hypothesis_row.get("missing_data", [])
            if isinstance(item, dict)
            and str(item.get("marker_id", "")).strip()
            and str(item.get("reason", "")).strip()
        ]
        confirmatory_tests = [
            ConfirmatoryTestItem(
                test_id=str(item.get("test_id", "")).strip(),
                display_name=str(item.get("display_name", "")).strip(),
                rationale=str(item.get("rationale", "")).strip(),
            )
            for item in hypothesis_row.get("confirmatory_tests", [])
            if isinstance(item, dict)
            and str(item.get("test_id", "")).strip()
            and str(item.get("display_name", "")).strip()
            and str(item.get("rationale", "")).strip()
        ]
        hypotheses_out.append(
            HypothesisV1(
                hypothesis_id=hypothesis_id,
                title=str(hypothesis_row.get("title", "")).strip(),
                summary=str(hypothesis_row.get("summary", "")).strip(),
                hypothesis_confidence=_safe_float(hypothesis_row.get("hypothesis_confidence")),
                ranking_rationale=_build_ranking_rationale(hypothesis_row, rank),
                evidence_for=evidence_for,
                evidence_against=evidence_against,
                missing_data=missing_data,
                confirmatory_tests=confirmatory_tests,
                safety_class=_normalise_hypothesis_safety_class(
                    hypothesis_row.get("safety_class")
                ),
            )
        )
    return RootCauseFindingV1(
        signal_id=str(finding_row.get("signal_id", "")).strip(),
        signal_state=str(finding_row.get("signal_state", "")).strip() or "unknown",
        signal_confidence=_safe_float(finding_row.get("signal_confidence")),
        primary_metric=str(finding_row.get("primary_metric", "")).strip(),
        hypotheses=hypotheses_out,
    )


def _collect_confirmatory_with_suppression(
    root_cause_finding: Optional[RootCauseFindingV1],
    biomarker_snapshot: Dict[str, Dict[str, Any]],
) -> Tuple[List[ConfirmatoryTestItem], List[str]]:
    if root_cause_finding is None:
        return [], []

    tests_registry = load_confirmatory_tests_registry_v1()
    tests_by_id = tests_registry.get("tests_by_id", {})
    tests_by_id = tests_by_id if isinstance(tests_by_id, dict) else {}

    selected: Dict[str, ConfirmatoryTestItem] = {}
    suppressed: set[str] = set()
    for hypothesis in root_cause_finding.hypotheses:
        for test_item in hypothesis.confirmatory_tests:
            registry_row = _to_dict(tests_by_id.get(test_item.test_id))
            mapped_markers = [
                str(marker_id).strip()
                for marker_id in _to_list(registry_row.get("maps_to_biomarkers"))
                if str(marker_id).strip()
            ]
            should_suppress = False
            for marker_id in mapped_markers:
                marker = _to_dict(biomarker_snapshot.get(marker_id))
                if marker and _marker_ready_for_suppression(marker):
                    should_suppress = True
                    break
            if should_suppress:
                suppressed.add(test_item.test_id)
                continue
            selected[test_item.test_id] = test_item

    return [selected[k] for k in sorted(selected.keys())], sorted(suppressed)


def compile_clinician_report_v1(
    *,
    report_v1_payload: Dict[str, Any],
    biomarker_rows: List[Dict[str, Any]],
    medical_history: Optional[Dict[str, Any]] = None,
    intervention_annotations_v1: Optional[InterventionAnnotationsV1] = None,
) -> Optional[ClinicianReportV1]:
    report_row = _to_dict(report_v1_payload)
    if not report_row:
        return None

    top_findings = [row for row in _to_list(report_row.get("top_findings")) if isinstance(row, dict)]
    top_chains = [row for row in _to_list(report_row.get("top_chains")) if isinstance(row, dict)]
    root_cause_row = _to_dict(report_row.get("root_cause_v1"))
    root_findings = [row for row in _to_list(root_cause_row.get("findings")) if isinstance(row, dict)]

    meta_row = _to_dict(report_row.get("meta"))
    ranking_fallback = bool(meta_row.get("ranking_signal_id_fallback_invoked"))
    ranking_policy_version = str(meta_row.get("ranking_policy_version", "") or "")
    concern_mode, co_primary_signal_ids = _resolve_page1_concern_mode(
        top_findings,
        ranking_signal_id_fallback_invoked=ranking_fallback,
    )
    runner_up_signal_id, runner_up_topic_line, runner_up_why_not_lead_line = _build_runner_up_page1_fields(
        top_findings,
        concern_mode,
    )

    primary = top_findings[0] if top_findings else {}
    primary_signal_id = str(primary.get("signal_id", "")).strip()
    primary_state = str(primary.get("signal_state", "unknown")).strip() or "unknown"
    primary_metric = str(primary.get("primary_metric", "")).strip()
    primary_confidence = _safe_float(primary.get("confidence"))

    primary_root_row = next(
        (row for row in root_findings if str(row.get("signal_id", "")).strip() == primary_signal_id),
        None,
    )
    primary_root = _normalise_root_cause_finding(primary_root_row) if isinstance(primary_root_row, dict) else None

    biomarker_snapshot = _build_biomarker_snapshot(biomarker_rows)
    consolidated_tests, suppressed_ids = _collect_confirmatory_with_suppression(
        primary_root,
        biomarker_snapshot,
    )

    top_hypothesis_line = "No hypothesis set available for this concern in v1."
    missing_count = 0
    if primary_root is not None and primary_root.hypotheses:
        top_hypothesis = primary_root.hypotheses[0]
        hc = round(float(top_hypothesis.hypothesis_confidence), 2)
        top_hypothesis_line = (
            f"Top hypothesis: {top_hypothesis.title} "
            f"(confidence {hc:.2f})."
        )
        missing_count = sum(len(h.missing_data) for h in primary_root.hypotheses)

    confidence_missing_line = format_confidence_consumer(
        missing_markers=bool(missing_count),
        near_tie=concern_mode in ("near_tie_ambiguity", "technical_tiebreak_lead"),
    )

    chain_lines = []
    for row in top_chains[:2]:
        summary_text = str(row.get("summary_text", "")).strip()
        if summary_text:
            chain_lines.append(summary_text)

    if primary_signal_id:
        lead_topic = _humanize_signal_id(primary_signal_id)
        primary_concern = f"{lead_topic}: {_state_consumer_phrase(primary_state)}"[:160]
    else:
        primary_concern = "No primary concern identified in v1."[:160]
    key_findings = [
        line
        for line in [
            str(primary.get("why_it_matters", "")).strip(),
            f"Primary metric: {primary_metric}." if primary_metric else "",
            f"Top chain confidence: {(_safe_float(top_chains[0].get('confidence')) if top_chains else 0.0):.2f}."
            if top_chains
            else "",
        ]
        if line
    ]
    policy_kf = _page1_policy_key_finding_line(concern_mode, co_primary_signal_ids)
    if policy_kf:
        key_findings.append(policy_kf)
    key_findings = key_findings[:5]

    expected_metrics = sorted(
        {
            str(row.get("primary_metric", "")).strip()
            for row in top_findings
            if str(row.get("primary_metric", "")).strip()
        }
    )
    present_metrics = 0
    quality_lines: List[str] = []
    quality_ok = True
    for metric in expected_metrics:
        marker = _to_dict(biomarker_snapshot.get(metric))
        if marker and marker.get("value") is not None:
            present_metrics += 1
        quality = _quality_label(_to_dict(marker.get("reference_range")))
        quality_lines.append(f"{metric}: {quality}")
        if quality == "missing" or not bool(str(marker.get("unit", "")).strip()):
            quality_ok = False
    if not expected_metrics:
        quality_lines = ["no_primary_metrics: missing"]
        quality_ok = False

    lowest_confidence = min(
        [_safe_float(row.get("confidence"), 1.0) for row in top_findings],
        default=0.0,
    )
    confidence_caveat = (
        "Given available markers, confidence is constrained by missing or partial reference-range context."
        if lowest_confidence < 0.6 or not quality_ok
        else "Given available markers, confidence supports stable discussion-level interpretation."
    )

    data_quality_passed = bool(expected_metrics) and (present_metrics == len(expected_metrics)) and quality_ok

    med_caveat = build_medication_supplement_interpretation_caveat(medical_history)

    def _snap_root_cause_floats(root: Optional[RootCauseFindingV1]) -> Optional[RootCauseFindingV1]:
        if root is None:
            return None
        hyps = [
            h.model_copy(update={"hypothesis_confidence": round(float(h.hypothesis_confidence), 2)})
            for h in root.hypotheses
        ]
        return root.model_copy(
            update={
                "hypotheses": hyps,
                "signal_confidence": round(float(root.signal_confidence), 2),
            }
        )

    primary_root_snapped = _snap_root_cause_floats(primary_root)

    ia_ctx = format_intervention_annotation_clinician_page1_v1(intervention_annotations_v1)[:420]

    return ClinicianReportV1(
        header=ClinicianHeaderV1(
            report_version="v1",
            disclaimer_top=(
                "Generated by HealthIQ from commercial laboratory results. Structured discussion aid "
                "summarising patterns, hypotheses, and confirmatory testing considerations. "
                "Not a clinical diagnosis or treatment recommendation."
            ),
            footer_line=(
                "HealthIQ Clinician Summary Report — discussion aid; not diagnostic or prescriptive."
            ),
        ),
        data_quality=DataQualityV1(
            panel_completeness_present=present_metrics,
            panel_completeness_expected=len(expected_metrics),
            lab_range_quality_by_primary_metric=quality_lines,
            confidence_caveat=confidence_caveat[:220],
            data_quality_passed=data_quality_passed,
        ),
        sections=ClinicianSectionsV1(
            page1=Page1SummaryBlockV1(
                primary_concern=primary_concern[:160],
                key_findings=key_findings,
                chains=chain_lines,
                top_hypothesis_line=top_hypothesis_line[:220],
                confidence_and_missing_data=confidence_missing_line[:220],
                primary_concern_mode=concern_mode,
                co_primary_signal_ids=co_primary_signal_ids,
                ranking_policy_version=ranking_policy_version[:220],
                runner_up_signal_id=runner_up_signal_id,
                runner_up_topic_line=runner_up_topic_line,
                runner_up_why_not_lead_line=runner_up_why_not_lead_line,
                intervention_annotation_context=ia_ctx,
            ),
            root_cause=primary_root_snapped,
            confirmatory_tests=consolidated_tests,
        ),
        suppressed_confirmatory_tests=suppressed_ids,
        medication_supplement_interpretation_caveat=med_caveat,
    )


def compile_report_v1(
    *,
    signal_results: List[Dict[str, Any]],
    interaction_summary: Optional[List[Dict[str, Any]]],
    interventions_v1: Optional[List[Dict[str, Any]]],
    signal_registry_version: Optional[str],
    signal_registry_hash_sha256: Optional[str],
    biomarker_context: Optional[Dict[str, Any]] = None,
    input_reference_ranges: Optional[Dict[str, Any]] = None,
    interaction_map_revision: Optional[str] = None,
    safety_contract_version: Optional[str] = None,
    generated_at: Optional[str] = None,
    user_intervention_document: Optional[Dict[str, Any]] = None,
) -> ReportV1:
    signal_results = [row for row in (signal_results or []) if isinstance(row, dict)]
    interaction_summary = [row for row in (interaction_summary or []) if isinstance(row, dict)]
    interventions_v1 = [row for row in (interventions_v1 or []) if isinstance(row, dict)]
    biomarker_context = biomarker_context or {}
    input_reference_ranges = input_reference_ranges or {}

    signal_system = {
        str(row.get("signal_id", "")).strip(): str(row.get("system", "")).strip()
        for row in signal_results
        if str(row.get("signal_id", "")).strip()
    }

    fallback_invoked = _signal_id_fallback_invoked_for_top_findings(signal_results)
    ordered_findings = sorted(signal_results, key=_top_finding_sort_tuple)
    top_findings: List[ReportTopFindingV1] = []
    for idx, row in enumerate(ordered_findings, start=1):
        signal_id = str(row.get("signal_id", "")).strip()
        signal_state = str(row.get("signal_state", "unknown")).strip() or "unknown"
        primary_metric = str(row.get("primary_metric", "")).strip()
        confidence = float(row.get("confidence", 0.0) if isinstance(row.get("confidence"), (int, float)) else 0.0)
        reasons = row.get("confidence_reasons")
        if not isinstance(reasons, list):
            reasons = []
        supporting = row.get("supporting_markers")
        if not isinstance(supporting, list):
            supporting = []
        top_findings.append(
            ReportTopFindingV1(
                priority_rank=idx,
                signal_id=signal_id,
                system=str(row.get("system", "")).strip(),
                signal_state=signal_state,
                confidence=confidence,
                confidence_reasons=[str(x) for x in reasons if str(x).strip()],
                primary_metric=primary_metric,
                supporting_markers=[str(x) for x in supporting if str(x).strip()],
                why_it_matters=_why_template(signal_id, signal_state, primary_metric),
            )
        )

    ordered_chains = sorted(
        interaction_summary,
        key=lambda row: (
            -float(row.get("confidence", 0.0) if isinstance(row.get("confidence"), (int, float)) else 0.0),
            -len(row.get("signals_involved", []) if isinstance(row.get("signals_involved"), list) else []),
            str(row.get("chain_id", "")),
        ),
    )
    top_chains: List[ReportTopChainV1] = []
    for idx, row in enumerate(ordered_chains, start=1):
        chain_id = str(row.get("chain_id", "")).strip()
        signals = row.get("signals_involved")
        if not isinstance(signals, list):
            signals = []
        ordered_signals = [str(x) for x in signals if str(x).strip()]
        summary_tokens = [signal_system[s] for s in ordered_signals if s in signal_system and signal_system[s]]
        top_chains.append(
            ReportTopChainV1(
                priority_rank=idx,
                chain_id=chain_id,
                confidence=float(row.get("confidence", 0.0) if isinstance(row.get("confidence"), (int, float)) else 0.0),
                signals_involved=ordered_signals,
                summary_tokens=summary_tokens,
                summary_text=_chain_summary_text(chain_id, ordered_signals),
            )
        )

    intervention_models = [ReportInterventionV1(**row) for row in interventions_v1]
    actions = ReportActionsV1(
        interventions=intervention_models,
        clinician_referrals=[i for i in intervention_models if i.safety_class == "clinician_referral"],
        monitoring=[i for i in intervention_models if i.safety_class == "monitoring"],
    )

    meta = ReportMetaV1(
        signal_registry_version=str(signal_registry_version or ""),
        signal_registry_hash_sha256=str(signal_registry_hash_sha256 or ""),
        interaction_map_revision=str(interaction_map_revision or _load_map_revision()),
        safety_contract_version=str(safety_contract_version or _load_safety_contract_version()),
        generated_at=str(generated_at or ""),
        ranking_policy_version=TOP_FINDINGS_RANKING_POLICY_VERSION,
        ranking_signal_id_fallback_invoked=fallback_invoked,
    )
    root_cause_v1 = compile_root_cause_v1(
        signal_results=signal_results,
        biomarker_context=biomarker_context,
        input_reference_ranges=input_reference_ranges,
    )
    intervention_annotations_v1 = build_intervention_annotations_v1(user_intervention_document)
    output_authority_provenance_v1 = build_report_output_authority_provenance_v1(
        signal_results=signal_results,
        report=ReportV1(
            report_version="v1",
            top_findings=top_findings,
            top_chains=top_chains,
            actions=actions,
            meta=meta,
            root_cause_v1=root_cause_v1,
            intervention_annotations_v1=intervention_annotations_v1,
        ),
        root_cause=root_cause_v1,
    )

    return ReportV1(
        report_version="v1",
        top_findings=top_findings,
        top_chains=top_chains,
        actions=actions,
        meta=meta,
        root_cause_v1=root_cause_v1,
        intervention_annotations_v1=intervention_annotations_v1,
        output_authority_provenance_v1=output_authority_provenance_v1,
    )
