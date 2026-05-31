"""
MED-REV-2 — Regenerate analysis from preserved stored input (new analysis_id; immutable source).
"""

from __future__ import annotations

import copy
import logging
from typing import Any, Dict, Optional, Tuple
from uuid import UUID, uuid4

from core.dto.analysis_regeneration_v1 import REGENERATION_POLICY_ID
from core.dto.result_versioning_policy_v1 import stamp_current_policy_meta

logger = logging.getLogger(__name__)


def build_client_result_shape_from_dto(
    dto: Any,
    *,
    analysis_id: str,
    lab_origin_meta: Optional[Dict[str, Any]],
    upload_panel_observations: Dict[str, Any],
    source_analysis_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Mirror POST /start stored payload shape for persistence."""
    from core.dto.builders import (
        analysis_route_biomarker_row_with_display,
        extend_cluster_client_dict_from_hit,
    )

    meta = dict(dto.meta or {})
    meta["lab_origin"] = lab_origin_meta or {
        "lab_provider_id": "unknown",
        "lab_provider_name": None,
        "detection_method": "unknown",
        "detection_confidence": 0.0,
        "raw_evidence": None,
    }
    from core.units.display_policy import build_display_policy_meta

    meta["display_unit_policy"] = build_display_policy_meta()
    meta["upload_panel_observations"] = upload_panel_observations
    meta = stamp_current_policy_meta(meta)
    if source_analysis_id:
        meta["regenerated_from_analysis_id"] = source_analysis_id
        meta["regeneration_policy_id"] = REGENERATION_POLICY_ID

    return {
        "analysis_id": analysis_id,
        "meta": meta,
        "replay_manifest": getattr(dto, "replay_manifest", None),
        "derived_markers": dto.derived_markers,
        "biomarkers": [
            analysis_route_biomarker_row_with_display(b, upload_panel=upload_panel_observations)
            for b in dto.biomarkers
        ],
        "clusters": [
            extend_cluster_client_dict_from_hit(
                {
                    "cluster_id": c.cluster_id,
                    "name": c.name,
                    "category": getattr(c, "category", "other"),
                    "biomarkers": c.biomarkers,
                    "description": c.description,
                    "severity": c.severity,
                    "confidence": c.confidence,
                    "recommendations": getattr(c, "recommendations", []),
                },
                c,
            )
            for c in dto.clusters
        ],
        "insights": [
            {
                "id": i.insight_id,
                "category": i.category,
                "title": i.title,
                "summary": getattr(i, "summary", i.title),
                "description": i.description,
                "confidence": i.confidence,
                "severity": i.severity,
                "recommendations": i.recommendations,
                "biomarkers_involved": i.biomarkers,
            }
            for i in dto.insights
        ],
        "unmapped_biomarkers": dto.unmapped_biomarkers,
        "status": dto.status,
        "created_at": dto.created_at,
        "overall_score": dto.overall_score,
        "primary_driver_system_id": getattr(dto, "primary_driver_system_id", ""),
        "system_capacity_scores": getattr(dto, "system_capacity_scores", {}),
        "burden_hash": getattr(dto, "burden_hash", ""),
        "risk_assessment": {},
        "recommendations": [],
        "result_version": "1.0.0",
        "interpretation_display_layer_v1": (
            dto.interpretation_display_layer_v1.model_dump()
            if getattr(dto, "interpretation_display_layer_v1", None) is not None
            else None
        ),
        "narrative_report_v1": (
            dto.narrative_report_v1.model_dump()
            if getattr(dto, "narrative_report_v1", None) is not None
            else None
        ),
        "consumer_domain_scores": (
            [x.model_dump() for x in dto.consumer_domain_scores]
            if getattr(dto, "consumer_domain_scores", None) is not None
            else None
        ),
    }


def run_pipeline_from_raw_biomarkers(
    *,
    biomarkers: Dict[str, Any],
    user: Dict[str, Any],
    questionnaire_data: Optional[Dict[str, Any]],
    analysis_id: str,
) -> Tuple[Any, Dict[str, Any], Dict[str, Any]]:
    """
    Run orchestrator with the same normalisation path as POST /start.
    Returns (dto, upload_panel_observations, lab_origin_meta).
    """
    from core.canonical.hba1c_layer_b_arbitration import arbitrate_hba1c_layer_b_input
    from core.canonical.normalize import normalize_biomarkers_with_metadata, detect_canonical_collisions
    from core.canonical.errors import CanonicalCollisionError
    from core.pipeline.orchestrator import AnalysisOrchestrator, UNIT_NORMALISATION_META_KEY
    from core.units.registry import apply_unit_normalisation, UNIT_REGISTRY_VERSION, UnitConversionError
    from core.units.display_fidelity_v1 import attach_source_labels_to_upload_panel

    try:
        normalized = normalize_biomarkers_with_metadata(biomarkers)
    except CanonicalCollisionError:
        raise ValueError("canonical_collision")

    upload_panel_observations = attach_source_labels_to_upload_panel(
        {k: copy.deepcopy(v) for k, v in normalized.items() if k != UNIT_NORMALISATION_META_KEY},
        biomarkers,
    )
    normalized = arbitrate_hba1c_layer_b_input(normalized)
    normalized = apply_unit_normalisation(normalized)
    normalized[UNIT_NORMALISATION_META_KEY] = {
        "unit_normalised": True,
        "unit_registry_version": UNIT_REGISTRY_VERSION,
    }

    orchestrator = AnalysisOrchestrator()
    dto = orchestrator.run(
        normalized,
        user,
        assume_canonical=True,
        questionnaire_data=questionnaire_data,
    )
    dto = dto.model_copy(update={"analysis_id": analysis_id})
    lab_origin_meta = {
        "lab_provider_id": "regenerated",
        "lab_provider_name": None,
        "detection_method": "regeneration",
        "detection_confidence": 1.0,
        "raw_evidence": None,
    }
    return dto, upload_panel_observations, lab_origin_meta
