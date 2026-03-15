"""
KB-S32 deterministic report compiler.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from core.contracts.report_v1 import (
    ReportActionsV1,
    ReportInterventionV1,
    ReportMetaV1,
    ReportTopChainV1,
    ReportTopFindingV1,
    ReportV1,
)
from core.analytics.root_cause_compiler_v1 import compile_root_cause_v1


_STATE_RANK = {"at_risk": 4, "suboptimal": 3, "optimal": 2, "unknown": 1}


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
    text = f"{signal_id} is {signal_state}. {primary_metric} is the primary driver."
    return text[:200]


def _chain_summary_text(chain_id: str, signals: List[str]) -> str:
    joined = " -> ".join(signals) if signals else "none"
    return f"Chain {chain_id}: {joined}."[:200]


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

    ordered_findings = sorted(
        signal_results,
        key=lambda row: (
            -_STATE_RANK.get(str(row.get("signal_state", "unknown")).strip(), 1),
            -float(row.get("confidence", 0.0) if isinstance(row.get("confidence"), (int, float)) else 0.0),
            str(row.get("signal_id", "")),
        ),
    )
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
    )
    root_cause_v1 = compile_root_cause_v1(
        signal_results=signal_results,
        biomarker_context=biomarker_context,
        input_reference_ranges=input_reference_ranges,
    )

    return ReportV1(
        report_version="v1",
        top_findings=top_findings,
        top_chains=top_chains,
        actions=actions,
        meta=meta,
        root_cause_v1=root_cause_v1,
    )
