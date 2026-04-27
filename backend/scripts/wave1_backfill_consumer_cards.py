#!/usr/bin/env python3
"""
D-6 — Governed backfill: recompute Wave 1 consumer_domain_scores from stored raw inputs.

Requires DATABASE_URL, authentication context is out of scope for this runner — use from
a trusted admin environment. Preserves legacy snapshot under client_result key
``consumer_domain_scores_legacy_1_0`` before overwriting with card_schema_version 1.1 rows.

Steps per analysis:
  1) Load Analysis + AnalysisResult.processing_metadata[client_result_shape_v1]
  2) Stash existing consumer_domain_scores to legacy key (if not already 1.1)
  3) Re-hydrate raw biomarkers + questionnaire; apply apply_unit_normalisation
  4) Run AnalysisOrchestrator.run(..., fixed_analysis_id=<uuid>)
  5) Write back consumer_domain_scores + updated meta (includes wave1_aligned_drivers)

This module provides ``run_backfill_dry_run`` for tests; full DB wiring is operator-owned.
"""
from __future__ import annotations

import hashlib
import json
import logging
from typing import Any, Dict, List, Mapping, Optional, Tuple

logger = logging.getLogger(__name__)

LEGACY_KEY = "consumer_domain_scores_legacy_1_0"
CLIENT_SHAPE = "client_result_shape_v1"


def _hash_cards(cards: Any) -> str:
    try:
        raw = json.dumps(cards, sort_keys=True, default=str)
    except (TypeError, ValueError):
        raw = str(cards)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def merge_backfill_payload(
    stored_client: Dict[str, Any],
    new_rows: List[Dict[str, Any]],
    *,
    new_meta_fragment: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Non-destructive merge for validation window: keep legacy 1.0 cards, attach 1.1, log hashes.
    """
    out = dict(stored_client)
    prev = out.get("consumer_domain_scores")
    if prev and LEGACY_KEY not in out:
        out[LEGACY_KEY] = prev
    out["consumer_domain_scores"] = [dict(r) for r in new_rows]
    if new_meta_fragment:
        prev_meta = out.get("meta")
        m = dict(prev_meta) if isinstance(prev_meta, dict) else {}
        m.update(new_meta_fragment)
        out["meta"] = m
    logger.info(
        "wave1 backfill merge: old_hash=%s new_hash=%s",
        _hash_cards(prev),
        _hash_cards(new_rows),
    )
    return out


def run_backfill_dry_run(
    stored_client: Dict[str, Any],
    new_rows: List[Dict[str, Any]],
    analysis_id: str,
) -> Dict[str, Any]:
    """Test hook: return audit dict without DB."""
    old = stored_client.get("consumer_domain_scores")
    old_v = None
    if old and isinstance(old, list) and old:
        old_v = old[0].get("card_schema_version", "1.0") if isinstance(old[0], dict) else "1.0"
    merged = merge_backfill_payload(
        stored_client,
        new_rows,
        new_meta_fragment={"wave1_backfill_audit": {"analysis_id": analysis_id, "old_version": old_v, "new_version": "1.1"}},
    )
    return {
        "analysis_id": analysis_id,
        "old_card_version": old_v,
        "new_card_version": "1.1",
        "old_hash": _hash_cards(old),
        "new_hash": _hash_cards(new_rows),
        "legacy_preserved": LEGACY_KEY in merged,
        "merged": merged,
    }


def prepare_stored_raw_for_orchestrator(raw_biomarkers: Dict[str, Any]) -> Dict[str, Any]:
    """
    Reconstruct unit-normalised biomarker panel + `__unit_normalisation_meta__` from stored `raw_biomarkers`.

    Stored snapshots do not persist `__unit_normalisation_meta__`; backfill must re-apply the same path as live runs.
    """
    from core.canonical.hba1c_layer_b_arbitration import arbitrate_hba1c_layer_b_input
    from core.canonical.normalize import normalize_biomarkers_with_metadata
    from core.pipeline.orchestrator import UNIT_NORMALISATION_META_KEY
    from core.units.registry import UNIT_REGISTRY_VERSION, apply_unit_normalisation

    normalized = normalize_biomarkers_with_metadata(dict(raw_biomarkers or {}))
    normalized = arbitrate_hba1c_layer_b_input(normalized)
    normalized = apply_unit_normalisation(normalized)
    normalized[UNIT_NORMALISATION_META_KEY] = {
        "unit_normalised": True,
        "unit_registry_version": UNIT_REGISTRY_VERSION,
    }
    return normalized


def rerun_orchestrator_for_wave1_backfill(
    *,
    raw_biomarkers: Dict[str, Any],
    user: Mapping[str, Any],
    questionnaire_data: Optional[Dict[str, Any]],
    fixed_analysis_id: str,
    assume_canonical: bool = True,
) -> Tuple[Any, Dict[str, Any]]:
    """
    Rerun the full pipeline for one analysis id with corrected Wave 1 cards on the DTO.

    Preserves the stored `analysis_id` via `AnalysisOrchestrator.run(..., fixed_analysis_id=...)`.
    """
    from core.pipeline.orchestrator import AnalysisOrchestrator

    prepared = prepare_stored_raw_for_orchestrator(raw_biomarkers)
    orch = AnalysisOrchestrator()
    dto = orch.run(
        prepared,
        dict(user),
        assume_canonical=assume_canonical,
        questionnaire_data=questionnaire_data,
        fixed_analysis_id=fixed_analysis_id,
    )
    return dto, {
        "analysis_id": str(fixed_analysis_id),
        "orchestrator_status": getattr(dto, "status", None),
    }


def build_client_merge_from_dto(
    stored_client: Dict[str, Any],
    dto: Any,
    analysis_id: str,
) -> Dict[str, Any]:
    """
    Merge Wave 1 card rows + `meta.wave1_aligned_drivers` from a fresh DTO into the existing client_result blob.
    """
    prev_cards = stored_client.get("consumer_domain_scores")
    old_v = None
    if prev_cards and isinstance(prev_cards, list) and prev_cards:
        old_v = (
            prev_cards[0].get("card_schema_version", "1.0")
            if isinstance(prev_cards[0], dict)
            else "1.0"
        )
    cards = getattr(dto, "consumer_domain_scores", None) or []
    new_rows: List[Dict[str, Any]] = [c.model_dump() for c in cards]
    meta_fragment: Dict[str, Any] = {}
    m = getattr(dto, "meta", None) or {}
    w1 = m.get("wave1_aligned_drivers")
    if w1 is not None:
        meta_fragment["wave1_aligned_drivers"] = w1
    merged = merge_backfill_payload(
        dict(stored_client),
        new_rows,
        new_meta_fragment={
            **meta_fragment,
            "wave1_backfill_audit": {
                "analysis_id": analysis_id,
                "orchestrator_status": getattr(dto, "status", None),
                "old_version": old_v,
                "new_version": "1.1",
            },
        },
    )
    return {
        "analysis_id": analysis_id,
        "old_card_version": old_v,
        "new_card_version": "1.1",
        "old_hash": _hash_cards(prev_cards),
        "new_hash": _hash_cards(new_rows),
        "legacy_preserved": LEGACY_KEY in merged,
        "merged": merged,
    }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print(
        "D-6 wave1 backfill: use prepare_stored_raw_for_orchestrator, "
        "rerun_orchestrator_for_wave1_backfill, build_client_merge_from_dto, "
        "or PersistenceService.save_live_analysis_after_run from an admin session."
    )
