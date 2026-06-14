"""
ARCH-COMPLETION-2 — Build governed provenance metadata for compiled analytical outputs.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Set

from core.contracts.output_authority_provenance_v1 import (
    OutputAuthorityProvenanceBundleV1,
    OutputElementAuthorityV1,
)
from core.contracts.report_v1 import ReportV1
from core.contracts.root_cause_v1 import RootCauseV1
from core.knowledge.compiled_hypothesis_registry_v1 import is_runtime_promoted_compiled_signal
from core.knowledge.compiled_output_authority_v1 import (
    WHY_ENGINE_FALLBACK_AUTHORITY_STATUS,
    WHY_ENGINE_FALLBACK_HYPOTHESIS_ID,
    authority_model_ref,
    card_entry_for_type,
    card_register_ref,
    classify_root_cause_finding,
    element_type_policy,
    GOVERNED_DOMAIN_CARD,
    GOVERNED_IDL_CARD,
    GOVERNED_SIGNAL_CARD,
    root_cause_register_ref,
)


def _signal_index(rows: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        sid = str(row.get("signal_id", "")).strip()
        if sid:
            out[sid] = row
    return out


def _governed_signal_card_element(row: Dict[str, Any], *, rank: int) -> OutputElementAuthorityV1:
    signal_id = str(row.get("signal_id", "")).strip()
    package_id = str(row.get("package_id", "")).strip()
    primary_metric = str(row.get("primary_metric", "")).strip()
    policy = element_type_policy("signal_card") or {}
    return OutputElementAuthorityV1(
        output_element_id=f"signal_card::{signal_id}::rank_{rank}",
        output_element_type="signal_card",
        source_signal_ids=[signal_id] if signal_id else [],
        source_package_ids=[package_id] if package_id else [],
        source_biomarker_ids=[primary_metric] if primary_metric else [],
        authority_register_ref=card_register_ref(),
        authority_status=str(
            (card_entry_for_type("signal_card") or {}).get("activation_status") or GOVERNED_SIGNAL_CARD
        ),
        wording_strength=str(policy.get("default_wording_strength") or "informational"),
        generated_by="core.analytics.report_compiler_v1.compile_report_v1",
    )


def _root_cause_element(finding: Any, *, uses_compiled: bool) -> OutputElementAuthorityV1:
    hypothesis_ids = [h.hypothesis_id for h in finding.hypotheses]
    status = classify_root_cause_finding(
        signal_id=finding.signal_id,
        hypothesis_ids=hypothesis_ids,
        uses_compiled_artefact=uses_compiled,
    )
    return OutputElementAuthorityV1(
        output_element_id=f"root_cause_card::{finding.signal_id}",
        output_element_type="root_cause_card",
        source_signal_ids=[finding.signal_id],
        source_biomarker_ids=[finding.primary_metric] if finding.primary_metric else [],
        source_root_cause_ids=[h.hypothesis_id for h in finding.hypotheses],
        authority_register_ref=root_cause_register_ref(),
        authority_status=status,
        wording_strength="informational",
        generated_by="core.analytics.root_cause_compiler_v1.compile_root_cause_v1",
    )


def build_report_output_authority_provenance_v1(
    *,
    signal_results: List[Dict[str, Any]],
    report: ReportV1,
    root_cause: Optional[RootCauseV1],
) -> OutputAuthorityProvenanceBundleV1:
    governed: List[OutputElementAuthorityV1] = []
    quarantined: List[OutputElementAuthorityV1] = []

    signal_by_id = _signal_index(signal_results)
    for finding in report.top_findings:
        row = signal_by_id.get(finding.signal_id, {})
        element = _governed_signal_card_element(row or {"signal_id": finding.signal_id}, rank=finding.priority_rank)
        if finding.signal_state in {"suboptimal", "at_risk"}:
            governed.append(element)
        else:
            element = element.model_copy(
                update={"authority_status": "CARD_GOVERNED_INACTIVE", "output_element_id": element.output_element_id + "::inactive"}
            )
            quarantined.append(element)

    if root_cause is not None:
        for finding in root_cause.findings:
            uses_compiled = is_runtime_promoted_compiled_signal(finding.signal_id)
            element = _root_cause_element(finding, uses_compiled=uses_compiled)
            hypothesis_ids = {h.hypothesis_id for h in finding.hypotheses}
            if WHY_ENGINE_FALLBACK_HYPOTHESIS_ID in hypothesis_ids or element.authority_status == WHY_ENGINE_FALLBACK_AUTHORITY_STATUS:
                quarantined.append(element)
            else:
                governed.append(element)

    return OutputAuthorityProvenanceBundleV1(
        authority_model_ref=authority_model_ref(),
        root_cause_register_ref=root_cause_register_ref(),
        card_register_ref=card_register_ref(),
        governed_elements=governed,
        quarantined_elements=quarantined,
    )


def build_domain_card_provenance_element(
    *,
    domain_id: str,
    active_signal_ids: List[str],
) -> OutputElementAuthorityV1:
    policy = element_type_policy("system_summary") or {}
    entry = card_entry_for_type("consumer_domain_card") or {}
    return OutputElementAuthorityV1(
        output_element_id=f"consumer_domain_card::{domain_id}",
        output_element_type="system_summary",
        source_signal_ids=list(active_signal_ids),
        authority_register_ref=card_register_ref(),
        authority_status=str(entry.get("activation_status") or GOVERNED_DOMAIN_CARD),
        wording_strength=str(policy.get("default_wording_strength") or "informational"),
        generated_by="core.analytics.domain_score_assembler.assemble_consumer_domain_scores_v1",
    )


def build_idl_card_provenance_element(*, record_id: str, source_signal_ids: List[str]) -> OutputElementAuthorityV1:
    entry = card_entry_for_type("interpretation_display_layer_card") or {}
    return OutputElementAuthorityV1(
        output_element_id=f"interpretation_display_layer_card::{record_id}",
        output_element_type="cluster_summary",
        source_signal_ids=list(source_signal_ids),
        authority_register_ref=card_register_ref(),
        authority_status=str(entry.get("activation_status") or GOVERNED_IDL_CARD),
        wording_strength="informational",
        generated_by="core.analytics.interpretation_display_layer_publish_v1.publish_interpretation_display_layer_v1",
    )


def is_quarantined_root_cause_signal(
    provenance: Optional[OutputAuthorityProvenanceBundleV1],
    signal_id: str,
) -> bool:
    sid = str(signal_id or "").strip()
    if not provenance or not sid:
        return False
    quarantined_ids: Set[str] = set()
    for element in provenance.quarantined_elements:
        if element.output_element_type == "root_cause_card":
            quarantined_ids.update(element.source_signal_ids)
    return sid in quarantined_ids


def is_governed_hypothesis(hypothesis_id: str) -> bool:
    return str(hypothesis_id or "").strip() != WHY_ENGINE_FALLBACK_HYPOTHESIS_ID
