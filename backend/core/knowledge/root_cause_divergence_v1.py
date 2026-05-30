"""
ARCH-RT-4 — Divergence comparison between legacy root-cause YAML and compiled hypothesis artefacts.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional


@dataclass
class HypothesisDivergenceRow:
    hypothesis_id: str
    title_match: bool
    in_legacy_yaml: bool
    in_compiled_artefact: bool
    legacy_title: Optional[str] = None
    compiled_title: Optional[str] = None
    claims_only_in_compiled: List[str] = field(default_factory=list)
    claims_only_in_legacy: List[str] = field(default_factory=list)
    evidence_for_differences: List[str] = field(default_factory=list)
    evidence_against_differences: List[str] = field(default_factory=list)
    missing_data_differences: List[str] = field(default_factory=list)
    confirmatory_test_differences: List[str] = field(default_factory=list)
    retail_wording_differences: List[str] = field(default_factory=list)


@dataclass
class RootCauseDivergenceReport:
    signal_id: str
    recommendation: str  # acceptable | acceptable_with_carry_forward | blocks_runtime_pilot | requires_clinical_adjudication
    blocks_runtime_pilot: bool
    rows: List[HypothesisDivergenceRow] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)


def _legacy_hypothesis_index(yaml_payload: Mapping[str, Any]) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    for row in yaml_payload.get("hypotheses") or []:
        if isinstance(row, dict):
            hid = str(row.get("hypothesis_id", "")).strip()
            if hid:
                out[hid] = row
    return out


def _compiled_hypothesis_index(shadow_payload: Mapping[str, Any]) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    for row in shadow_payload.get("hypotheses") or []:
        if isinstance(row, dict):
            hid = str(row.get("hypothesis_id", "")).strip()
            if hid:
                out[hid] = row
    return out


def _legacy_rule_evidence_strings(row: Dict[str, Any], rules_key: str) -> List[str]:
    items: List[str] = []
    for rule in row.get(rules_key) or []:
        if isinstance(rule, dict):
            text = str(rule.get("evidence_for_item", "")).strip()
            if text:
                items.append(text)
    return items


def _legacy_missing_policy(row: Dict[str, Any]) -> str:
    parts: List[str] = []
    for item in row.get("missing_data_markers") or []:
        if isinstance(item, dict):
            mid = str(item.get("marker_id", "")).strip()
            reason = str(item.get("reason", "")).strip()
            if mid or reason:
                parts.append(f"{mid}: {reason}".strip(": "))
    return "; ".join(parts)


def compare_legacy_yaml_to_compiled_shadow(
    *,
    signal_id: str,
    legacy_loader_payload: Mapping[str, Any],
    compiled_shadow_payload: Mapping[str, Any],
) -> RootCauseDivergenceReport:
    legacy_idx = _legacy_hypothesis_index(legacy_loader_payload.get("payload") or legacy_loader_payload)
    compiled_idx = _compiled_hypothesis_index(compiled_shadow_payload)

    all_ids = sorted(set(legacy_idx.keys()) | set(compiled_idx.keys()))
    rows: List[HypothesisDivergenceRow] = []
    blocks = False

    for hid in all_ids:
        leg = legacy_idx.get(hid)
        comp = compiled_idx.get(hid)
        row = HypothesisDivergenceRow(
            hypothesis_id=hid,
            in_legacy_yaml=leg is not None,
            in_compiled_artefact=comp is not None,
            title_match=False,
        )
        if leg:
            row.legacy_title = str(leg.get("title", "")).strip()
        if comp:
            row.compiled_title = str(comp.get("title", "")).strip()
        if row.legacy_title and row.compiled_title:
            row.title_match = row.legacy_title == row.compiled_title

        if leg and not comp:
            row.claims_only_in_legacy.append("hypothesis present only in legacy YAML")
            blocks = True
        if comp and not leg:
            row.claims_only_in_compiled.append("hypothesis present only in compiled artefact")
            blocks = True

        if leg and comp:
            leg_for = _legacy_rule_evidence_strings(leg, "evidence_for_rules")
            comp_for = [str(x).strip() for x in (comp.get("evidence_for") or []) if str(x).strip()]
            if set(leg_for) != set(comp_for):
                row.evidence_for_differences.append(
                    f"legacy rules ({len(leg_for)}) vs compiled strings ({len(comp_for)})"
                )

            leg_against = _legacy_rule_evidence_strings(leg, "evidence_against_rules")
            comp_against = [
                str(x).strip() for x in (comp.get("evidence_against") or []) if str(x).strip()
            ]
            if set(leg_against) != set(comp_against):
                row.evidence_against_differences.append("evidence_against content differs")

            leg_missing = _legacy_missing_policy(leg)
            comp_missing = str(comp.get("missing_data_policy", "")).strip()
            if leg_missing and comp_missing and leg_missing != comp_missing:
                row.missing_data_differences.append("missing-data policy wording differs")

            leg_tests = sorted(str(x) for x in (leg.get("confirmatory_tests") or []))
            comp_tests = sorted(str(x) for x in (comp.get("confirmatory_tests") or []))
            if leg_tests != comp_tests:
                row.confirmatory_test_differences.append(
                    f"legacy={leg_tests!r} compiled={comp_tests!r}"
                )

            summary = str(leg.get("summary_template", "")).strip()
            claim = str(comp.get("physiological_claim", "")).strip()
            if summary and claim and summary[:80] != claim[:80]:
                row.retail_wording_differences.append(
                    "legacy summary_template vs compiled physiological_claim (expected pilot translation delta)"
                )

        rows.append(row)

    if blocks:
        recommendation = "requires_clinical_adjudication"
    elif any(r.evidence_for_differences or r.retail_wording_differences for r in rows):
        recommendation = "acceptable_with_carry_forward"
    else:
        recommendation = "acceptable"

    notes = [
        "Legacy YAML remains runtime authority for all 41 registry signals.",
        "Compiled artefact is shadow/pilot only for signal_vitamin_d_low.",
        "Root-cause compiler still matches signal_id family only (not activation_key).",
    ]
    return RootCauseDivergenceReport(
        signal_id=signal_id,
        recommendation=recommendation,
        blocks_runtime_pilot=blocks,
        rows=rows,
        notes=notes,
    )
