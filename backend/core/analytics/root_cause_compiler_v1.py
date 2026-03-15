"""
KB-S33 deterministic root-cause compiler (homocysteine v1 only).
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Set

from core.analytics.intervention_selector_v1 import load_safety_rules_v1
from core.contracts.root_cause_v1 import (
    RootCauseConfirmatoryTestV1,
    RootCauseEvidenceItemV1,
    RootCauseFindingV1,
    RootCauseHypothesisV1,
    RootCauseMissingItemV1,
    RootCauseV1,
)
from core.knowledge.load_confirmatory_tests_registry import load_confirmatory_tests_registry_v1
from core.knowledge.load_root_cause_hypotheses import load_hcy_hypotheses_v1

_TARGET_SIGNAL_ID = "signal_homocysteine_elevation_context"


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


def _contains_deny_phrase(text: str, denylist: List[str]) -> Optional[str]:
    lowered = text.lower()
    for phrase in denylist:
        if phrase.lower() in lowered:
            return phrase
    return None


def _marker_value(marker_id: str, biomarker_context: Dict[str, Any]) -> Optional[float]:
    if marker_id not in biomarker_context:
        return None
    row = biomarker_context.get(marker_id)
    if isinstance(row, (int, float)):
        return float(row)
    if isinstance(row, dict):
        value = row.get("value", row.get("measurement"))
        if isinstance(value, (int, float)):
            return float(value)
    return None


def _marker_status(
    marker_id: str,
    *,
    biomarker_context: Dict[str, Any],
    reference_ranges: Dict[str, Any],
) -> Optional[str]:
    value = _marker_value(marker_id, biomarker_context)
    if value is None:
        return None
    bounds = reference_ranges.get(marker_id)
    if not isinstance(bounds, dict):
        return None
    lower = bounds.get("min")
    upper = bounds.get("max")
    if not isinstance(lower, (int, float)) or not isinstance(upper, (int, float)):
        return None
    if value < float(lower):
        return "low"
    if value > float(upper):
        return "high"
    return "normal"


def _direction_match(
    direction: str,
    *,
    marker_present: bool,
    marker_status: Optional[str],
) -> Optional[bool]:
    if direction == "high_or_missing":
        if not marker_present:
            return True
        if marker_status is None:
            return None
        return marker_status == "high"

    if not marker_present:
        return None
    if marker_status is None:
        return None
    if direction in {"flagged_or_high", "high"}:
        return marker_status == "high"
    if direction in {"low_or_borderline", "low"}:
        return marker_status == "low"
    if direction == "clearly_normal":
        return marker_status == "normal"
    return None


def _evaluate_marker_block(
    *,
    marker_ids: List[str],
    any_mode: bool,
    direction: str,
    biomarker_context: Dict[str, Any],
    reference_ranges: Dict[str, Any],
) -> Optional[bool]:
    if not marker_ids:
        return None
    if any_mode:
        evaluated: List[bool] = []
        for marker_id in marker_ids:
            present = marker_id in biomarker_context
            status = _marker_status(
                marker_id,
                biomarker_context=biomarker_context,
                reference_ranges=reference_ranges,
            )
            matched = _direction_match(direction, marker_present=present, marker_status=status)
            if matched is not None:
                evaluated.append(matched)
        if not evaluated:
            return None
        return any(evaluated)

    evaluated_all: List[bool] = []
    for marker_id in marker_ids:
        present = marker_id in biomarker_context
        status = _marker_status(
            marker_id,
            biomarker_context=biomarker_context,
            reference_ranges=reference_ranges,
        )
        matched = _direction_match(direction, marker_present=present, marker_status=status)
        if matched is None:
            return None
        evaluated_all.append(matched)
    return all(evaluated_all)


def _evaluate_rule(
    rule: Dict[str, Any],
    *,
    biomarker_context: Dict[str, Any],
    reference_ranges: Dict[str, Any],
    fired_signals: Set[str],
) -> Optional[bool]:
    direction = str(rule.get("direction", "")).strip()
    if not direction:
        return None

    results: List[Optional[bool]] = []

    markers_any = rule.get("markers_any")
    if isinstance(markers_any, list):
        results.append(
            _evaluate_marker_block(
                marker_ids=[str(x) for x in markers_any if str(x).strip()],
                any_mode=True,
                direction=direction,
                biomarker_context=biomarker_context,
                reference_ranges=reference_ranges,
            )
        )
    markers_all = rule.get("markers_all")
    if isinstance(markers_all, list):
        results.append(
            _evaluate_marker_block(
                marker_ids=[str(x) for x in markers_all if str(x).strip()],
                any_mode=False,
                direction=direction,
                biomarker_context=biomarker_context,
                reference_ranges=reference_ranges,
            )
        )
    signals_any = rule.get("signals_any")
    if isinstance(signals_any, list):
        signal_ids = {str(x).strip() for x in signals_any if str(x).strip()}
        if direction == "fired":
            results.append(any(s in fired_signals for s in signal_ids))
        else:
            results.append(None)

    if not results:
        return None
    if any(r is False for r in results):
        return False
    if any(r is None for r in results):
        return None
    return True


def _compile_hypothesis_confidence(hypothesis: Dict[str, Any], marker_present: Set[str]) -> float:
    required = [str(x) for x in (hypothesis.get("required_markers") or []) if str(x).strip()]
    confirmatory = [str(x) for x in (hypothesis.get("confirmatory_markers") or []) if str(x).strip()]
    differentiators = [str(x) for x in (hypothesis.get("differentiator_markers") or []) if str(x).strip()]

    score = 0.20
    if required and all(m in marker_present for m in required):
        score += 0.20
    if confirmatory and any(m in marker_present for m in confirmatory):
        score += 0.20
    if differentiators and any(m not in marker_present for m in differentiators):
        score -= 0.20
    if required and all(m not in marker_present for m in required):
        score -= 0.20
    return _clamp01(score)


def compile_root_cause_v1(
    *,
    signal_results: List[Dict[str, Any]],
    biomarker_context: Optional[Dict[str, Any]] = None,
    input_reference_ranges: Optional[Dict[str, Any]] = None,
) -> Optional[RootCauseV1]:
    rows = [r for r in (signal_results or []) if isinstance(r, dict)]
    target = next((r for r in rows if str(r.get("signal_id", "")).strip() == _TARGET_SIGNAL_ID), None)
    if target is None:
        return None

    biomarker_context = biomarker_context or {}
    input_reference_ranges = input_reference_ranges or {}
    marker_present = {str(k).strip() for k in biomarker_context.keys() if str(k).strip()}
    fired_signals = {
        str(r.get("signal_id", "")).strip()
        for r in rows
        if str(r.get("signal_state", "")).strip() in {"suboptimal", "at_risk"}
    }

    tests_registry = load_confirmatory_tests_registry_v1()
    tests_by_id: Dict[str, Dict[str, Any]] = tests_registry["tests_by_id"]
    hypotheses_payload = load_hcy_hypotheses_v1()["hypotheses"]

    compiled_hypotheses: List[RootCauseHypothesisV1] = []
    for hypothesis in hypotheses_payload:
        evidence_for: List[RootCauseEvidenceItemV1] = []
        for rule in hypothesis.get("evidence_for_rules", []):
            if not isinstance(rule, dict):
                continue
            matched = _evaluate_rule(
                rule,
                biomarker_context=biomarker_context,
                reference_ranges=input_reference_ranges,
                fired_signals=fired_signals,
            )
            if matched is True:
                marker_refs = [str(x) for x in (rule.get("marker_refs") or []) if str(x).strip()]
                evidence_for.append(
                    RootCauseEvidenceItemV1(
                        item=str(rule.get("evidence_for_item", "")).strip()[:120],
                        marker_refs=marker_refs,
                    )
                )

        evidence_against: List[RootCauseEvidenceItemV1] = []
        for rule in hypothesis.get("evidence_against_rules", []):
            if not isinstance(rule, dict):
                continue
            matched = _evaluate_rule(
                rule,
                biomarker_context=biomarker_context,
                reference_ranges=input_reference_ranges,
                fired_signals=fired_signals,
            )
            if matched is True:
                marker_refs = [str(x) for x in (rule.get("marker_refs") or []) if str(x).strip()]
                evidence_against.append(
                    RootCauseEvidenceItemV1(
                        item=str(rule.get("evidence_against_item", "")).strip()[:120],
                        marker_refs=marker_refs,
                    )
                )

        missing_data: List[RootCauseMissingItemV1] = []
        for marker_meta in hypothesis.get("missing_data_markers", []):
            if not isinstance(marker_meta, dict):
                continue
            marker_id = str(marker_meta.get("marker_id", "")).strip()
            reason = str(marker_meta.get("reason", "")).strip()
            if marker_id and marker_id not in marker_present:
                missing_data.append(RootCauseMissingItemV1(marker_id=marker_id, reason=reason[:120]))

        confirmatory_tests: List[RootCauseConfirmatoryTestV1] = []
        for test_id in hypothesis.get("confirmatory_tests", []):
            tid = str(test_id).strip()
            if not tid:
                continue
            if tid not in tests_by_id:
                raise ValueError(
                    f"Unknown confirmatory test_id={tid!r} referenced by hypothesis_id={hypothesis.get('hypothesis_id')!r}"
                )
            test_row = tests_by_id[tid]
            mapped_biomarkers = [
                str(x).strip()
                for x in (test_row.get("maps_to_biomarkers") or [])
                if str(x).strip()
            ]
            is_repeat_test = bool(test_row.get("is_repeat_test", False))
            if not is_repeat_test and mapped_biomarkers and all(m in marker_present for m in mapped_biomarkers):
                continue
            confirmatory_tests.append(
                RootCauseConfirmatoryTestV1(
                    test_id=tid,
                    display_name=str(test_row.get("display_name", "")).strip(),
                    rationale=str(test_row.get("rationale_template", "")).strip()[:120],
                )
            )

        compiled_hypotheses.append(
            RootCauseHypothesisV1(
                hypothesis_id=str(hypothesis.get("hypothesis_id", "")).strip(),
                title=str(hypothesis.get("title", "")).strip(),
                summary=str(hypothesis.get("summary_template", "")).strip()[:200],
                hypothesis_confidence=_compile_hypothesis_confidence(hypothesis, marker_present),
                evidence_for=evidence_for,
                evidence_against=evidence_against,
                missing_data=missing_data,
                confirmatory_tests=confirmatory_tests,
                safety_class=str(hypothesis.get("safety_class", "")).strip(),
            )
        )

    finding = RootCauseFindingV1(
        signal_id=_TARGET_SIGNAL_ID,
        primary_metric=str(target.get("primary_metric", "")).strip(),
        signal_state=str(target.get("signal_state", "unknown")).strip() or "unknown",
        signal_confidence=float(target.get("confidence", 0.0) if isinstance(target.get("confidence"), (int, float)) else 0.0),
        hypotheses=compiled_hypotheses,
    )
    root_cause = RootCauseV1(version="v1", findings=[finding])

    rules = load_safety_rules_v1()
    denylist = [str(x) for x in rules.get("denylist_phrases", []) if str(x).strip()]
    text_fields: List[str] = []
    for h in root_cause.findings[0].hypotheses:
        text_fields.extend([h.title, h.summary])
        text_fields.extend(item.item for item in h.evidence_for)
        text_fields.extend(item.item for item in h.evidence_against)
        text_fields.extend(item.reason for item in h.missing_data)
        text_fields.extend(item.rationale for item in h.confirmatory_tests)
    for text in text_fields:
        deny = _contains_deny_phrase(text, denylist)
        if deny:
            raise ValueError(f"Denylist phrase '{deny}' found in root_cause_v1 text field")

    return root_cause
