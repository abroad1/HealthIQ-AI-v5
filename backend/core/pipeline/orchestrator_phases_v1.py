"""
LC-S21 — Named orchestrator pipeline phases (behaviour-preserving extraction).

Phase order is documented here; orchestrator.run() remains the single entry point.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import date
from typing import Any, Callable, Dict, List, Mapping, Optional, Tuple

from core.analytics.primitives import coerce_optional_float

# Documented pipeline phase order (actual execution remains in AnalysisOrchestrator.run).
PIPELINE_PHASE_ORDER: Tuple[str, ...] = (
    "unit_normalisation_gate",
    "canonicalisation_quarantine",
    "scoring_input_preparation",
    "derived_markers",
    "analysis_context",
    "signal_evaluation",
    "scoring",
    "clustering",
    "criticality",
    "insight_graph",
    "state_engine_stack",
    "burden_capacity_validation",
    "replay_manifest",
    "insight_synthesis",
    "dto_assembly",
    "report_narrative_idl",
)


@dataclass(frozen=True)
class QuarantinePhaseResult:
    filtered_biomarkers: Dict[str, Any]
    unmapped_biomarkers: List[str]
    skipped_unmapped: int


@dataclass(frozen=True)
class ScoringInputPrepResult:
    simple_biomarkers: Dict[str, Any]
    input_reference_ranges: Dict[str, Any]
    input_reference_profiles: Dict[str, Any]


@dataclass(frozen=True)
class SignalEvaluationPhaseResult:
    signal_results_serialized: List[Dict[str, Any]]
    signal_registry_hash_sha256: Optional[str]
    report_generated_at: str


def quarantine_unmapped_biomarkers(
    biomarkers: Mapping[str, Any],
    *,
    alias_service: Any,
) -> QuarantinePhaseResult:
    unmapped_biomarkers: List[str] = []
    filtered_biomarkers: Dict[str, Any] = {}
    for key, value in biomarkers.items():
        if key.startswith("unmapped_"):
            unmapped_biomarkers.append(key)
            continue
        resolved = alias_service.resolve(key)
        if resolved.startswith("unmapped_"):
            unmapped_biomarkers.append(resolved)
            continue
        filtered_biomarkers[key] = value
    unmapped_biomarkers = sorted(set(unmapped_biomarkers))
    skipped = len(biomarkers) - len(filtered_biomarkers)
    return QuarantinePhaseResult(
        filtered_biomarkers=filtered_biomarkers,
        unmapped_biomarkers=unmapped_biomarkers,
        skipped_unmapped=skipped,
    )


def prepare_scoring_inputs_from_panel(
    filtered_biomarkers: Mapping[str, Any],
    *,
    logger: logging.Logger,
) -> ScoringInputPrepResult:
    simple_biomarkers: Dict[str, Any] = {}
    input_reference_ranges: Dict[str, Any] = {}
    input_reference_profiles: Dict[str, Any] = {}
    for biomarker_name, biomarker_data in filtered_biomarkers.items():
        if isinstance(biomarker_data, dict):
            simple_biomarkers[biomarker_name] = biomarker_data.get("value", biomarker_data.get("measurement", 0))
            ref_range = biomarker_data.get("reference_range") or biomarker_data.get("referenceRange")
            if ref_range and isinstance(ref_range, dict):
                min_val = coerce_optional_float(ref_range.get("min"))
                max_val = coerce_optional_float(ref_range.get("max"))
                has_min = min_val is not None
                has_max = max_val is not None
                if has_min and has_max and float(min_val) >= float(max_val):
                    logger.warning(
                        "[Orchestrator] Invalid input reference range for %s: min=%s, max=%s",
                        biomarker_name,
                        min_val,
                        max_val,
                    )
                elif has_min or has_max:
                    input_reference_ranges[biomarker_name] = {
                        "min": float(min_val) if has_min else None,
                        "max": float(max_val) if has_max else None,
                        "unit": ref_range.get("unit", ""),
                        "source": ref_range.get("source", "lab"),
                    }
                    logger.debug(
                        "[Orchestrator] Preserved input reference range for %s: %s",
                        biomarker_name,
                        input_reference_ranges[biomarker_name],
                    )
            ref_profile = biomarker_data.get("reference_profile") or biomarker_data.get("referenceProfile")
            if isinstance(ref_profile, dict):
                input_reference_profiles[biomarker_name] = dict(ref_profile)
        else:
            simple_biomarkers[biomarker_name] = biomarker_data
    return ScoringInputPrepResult(
        simple_biomarkers=simple_biomarkers,
        input_reference_ranges=input_reference_ranges,
        input_reference_profiles=input_reference_profiles,
    )


def evaluate_signal_evaluation_phase(
    *,
    signal_evaluator: Any,
    simple_biomarkers: Mapping[str, Any],
    derived_ratios_meta: Mapping[str, Any],
    input_reference_ranges: Mapping[str, Any],
    input_reference_profiles: Mapping[str, Any],
    registry_hash_fn: Callable[[], Optional[str]],
    utc_now_fn: Callable[[], str],
    runtime_context: Optional[Dict[str, Any]] = None,
) -> SignalEvaluationPhaseResult:
    signal_biomarkers = {k: v for k, v in simple_biomarkers.items() if k != "age"}
    signal_derived = {
        rid: data["value"]
        for rid, data in (derived_ratios_meta.get("ratios") or {}).items()
        if isinstance(data, dict) and isinstance(data.get("value"), (int, float))
    }
    signal_results_raw = signal_evaluator.evaluate_all(
        signal_biomarkers,
        signal_derived,
        lab_ranges=input_reference_ranges,
        reference_profiles=input_reference_profiles,
        runtime_context=runtime_context,
    )
    return SignalEvaluationPhaseResult(
        signal_results_serialized=[r.model_dump() for r in signal_results_raw],
        signal_registry_hash_sha256=registry_hash_fn(),
        report_generated_at=utc_now_fn(),
    )


def inject_questionnaire_age(
    simple_biomarkers: Dict[str, Any],
    questionnaire_data: Optional[Dict[str, Any]],
) -> None:
    dob = (questionnaire_data or {}).get("date_of_birth")
    try:
        age = int((date.today() - date.fromisoformat(dob)).days / 365.25) if dob else None
    except (ValueError, TypeError):
        age = None
    simple_biomarkers["age"] = age
