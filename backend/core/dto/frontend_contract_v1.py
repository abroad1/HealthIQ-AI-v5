"""
LC-S19 — Layer B → Layer C frontend payload contract (governance constants).

Field classification is documented in docs/audit-papers/LC-S19_payload_contract_hardening_notes.md.
This module machine-enforces root-key stability for GET /api/analysis/result consumers.
"""

from __future__ import annotations

from typing import Final, FrozenSet

# Root keys emitted by build_analysis_result_dto — must stay aligned with AnalysisResult (frontend).
FRONTEND_CONSUMED_ROOT_KEYS: Final[FrozenSet[str]] = frozenset(
    {
        "analysis_id",
        "biomarkers",
        "clusters",
        "insights",
        "status",
        "created_at",
        "overall_score",
        "primary_driver_system_id",
        "system_capacity_scores",
        "burden_hash",
        "risk_assessment",
        "recommendations",
        "result_version",
        "derived_markers",
        "meta",
        "clinician_report_v1",
        "balanced_systems_v1",
        "replay_manifest",
        "interpretation_display_layer_v1",
        "narrative_report_v1",
        "consumer_domain_scores",
        "intervention_annotations_v1",
    }
)

# Nested under meta.insight_graph — analytical truth; not primary retail surfaces but exposed today.
INTERNAL_ANALYTICAL_META_PATHS: Final[FrozenSet[str]] = frozenset(
    {
        "meta.insight_graph",
        "meta.insight_graph.report_v1",
        "meta.insight_graph.signal_results",
    }
)

# User-facing string fields scanned for leakage guards (subset; see regression tests).
USER_FACING_DTO_TEXT_PATHS: Final[tuple[str, ...]] = (
    "narrative_report_v1.retail_summary",
    "narrative_report_v1.body_overview",
    "narrative_report_v1.lead_narrative",
    "narrative_report_v1.next_steps_narrative",
    "clinician_report_v1.sections.page1.primary_concern",
    "consumer_domain_scores[].headline_sentence",
    "consumer_domain_scores[].contributor_sentence",
    "interpretation_display_layer_v1.records[].retail_display_label",
    "interpretation_display_layer_v1.records[].why_it_matters",
)
