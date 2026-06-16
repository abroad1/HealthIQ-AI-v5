"""
LC-S20 — Persisted result replay and stale-result compatibility contract.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, FrozenSet, List, Optional, Sequence

from core.dto.frontend_contract_v1 import FRONTEND_CONSUMED_ROOT_KEYS

CURRENT_RESULT_VERSION = "1.0.0"
CURRENT_REPLAY_MANIFEST_VERSION = "1.0.0"

# Minimum fields required for results-page render contract (LC-S20 fixture strategy).
PERSISTED_RENDER_REQUIRED_KEYS: FrozenSet[str] = frozenset(
    {
        "analysis_id",
        "biomarkers",
        "consumer_domain_scores",
        "clinician_report_v1",
        "narrative_report_v1",
        "interpretation_display_layer_v1",
        "replay_manifest",
        "meta",
        "result_version",
    }
)

_PLACEHOLDER_PATTERNS = (
    re.compile(r"summarise structured signals", re.IGNORECASE),
    re.compile(r"\bYour analysis summary\b"),
    re.compile(r"\bunmapped_\w+"),
    re.compile(r"\bsignal_[a-z0-9_]+\b", re.IGNORECASE),
    re.compile(r"\bLC-S\d+\b"),
    re.compile(r"\bpkg_[a-z0-9_]+\b"),
)

_WAVE1_DOMAIN_IDS = (
    "wave1_cardiovascular",
    "wave1_blood_sugar",
    "wave1_liver",
)


@dataclass(frozen=True)
class PersistedCompatibilityAssessment:
    compatible: bool
    stale: bool
    missing_required_keys: tuple[str, ...]
    missing_root_keys: tuple[str, ...]
    stale_reasons: tuple[str, ...]
    render_blockers: tuple[str, ...]


class PersistedReplayCompatibilityError(ValueError):
    """Raised when persisted payload cannot be loaded for replay."""


def assess_persisted_result_compatibility(stored: Dict[str, Any]) -> PersistedCompatibilityAssessment:
    if not isinstance(stored, dict):
        raise PersistedReplayCompatibilityError("persisted payload must be a dict")

    missing_required = tuple(
        sorted(k for k in PERSISTED_RENDER_REQUIRED_KEYS if k not in stored or stored[k] is None)
    )
    missing_root = tuple(sorted(k for k in FRONTEND_CONSUMED_ROOT_KEYS if k not in stored))

    stale_reasons: List[str] = []
    version = str(stored.get("result_version") or "").strip()
    if not version:
        stale_reasons.append("result_version_missing")
    elif version != CURRENT_RESULT_VERSION:
        stale_reasons.append(f"result_version_mismatch:{version}!={CURRENT_RESULT_VERSION}")

    replay = stored.get("replay_manifest")
    if not isinstance(replay, dict):
        stale_reasons.append("replay_manifest_missing_or_invalid")
    else:
        manifest_version = str(replay.get("manifest_version") or "").strip()
        if manifest_version and manifest_version != CURRENT_REPLAY_MANIFEST_VERSION:
            stale_reasons.append(
                f"replay_manifest_version_mismatch:{manifest_version}!={CURRENT_REPLAY_MANIFEST_VERSION}"
            )

    render_blockers: List[str] = list(missing_required)
    if not _has_primary_finding(stored):
        render_blockers.append("missing_primary_finding")
    if not _has_wave1_domain_cards(stored):
        render_blockers.append("missing_wave1_domain_cards")

    compatible = not missing_required and not missing_root
    stale = bool(stale_reasons)
    return PersistedCompatibilityAssessment(
        compatible=compatible,
        stale=stale,
        missing_required_keys=missing_required,
        missing_root_keys=missing_root,
        stale_reasons=tuple(stale_reasons),
        render_blockers=tuple(render_blockers),
    )


def validate_persisted_result_for_replay(stored: Dict[str, Any]) -> PersistedCompatibilityAssessment:
    assessment = assess_persisted_result_compatibility(stored)
    if assessment.missing_required_keys or assessment.missing_root_keys:
        raise PersistedReplayCompatibilityError(
            f"incompatible persisted result: missing={assessment.missing_required_keys or assessment.missing_root_keys}"
        )
    return assessment


def _has_primary_finding(stored: Dict[str, Any]) -> bool:
    cr = stored.get("clinician_report_v1")
    if isinstance(cr, dict):
        sections = cr.get("sections")
        if isinstance(sections, dict):
            page1 = sections.get("page1")
            if isinstance(page1, dict):
                concern = str(page1.get("primary_concern") or "").strip()
                if concern:
                    return True
    nr = stored.get("narrative_report_v1")
    if isinstance(nr, dict):
        for key in ("retail_summary", "lead_narrative", "body_overview"):
            if str(nr.get(key) or "").strip():
                return True
    idl = stored.get("interpretation_display_layer_v1")
    if isinstance(idl, dict):
        records = idl.get("records")
        if isinstance(records, list) and records:
            return True
    return False


def _has_wave1_domain_cards(stored: Dict[str, Any]) -> bool:
    scores = stored.get("consumer_domain_scores")
    if not isinstance(scores, list) or not scores:
        return False
    present = {str(row.get("domain_id", "")).strip() for row in scores if isinstance(row, dict)}
    return all(domain_id in present for domain_id in _WAVE1_DOMAIN_IDS)


def collect_user_facing_text(stored: Dict[str, Any]) -> List[str]:
    chunks: List[str] = []
    nr = stored.get("narrative_report_v1")
    if isinstance(nr, dict):
        for key in (
            "retail_summary",
            "body_overview",
            "lead_narrative",
            "next_steps_narrative",
            "longitudinal_narrative",
        ):
            val = nr.get(key)
            if isinstance(val, str):
                chunks.append(val)
    for row in stored.get("consumer_domain_scores") or []:
        if not isinstance(row, dict):
            continue
        for key in (
            "headline_sentence",
            "contributor_sentence",
            "consequence_sentence",
            "next_step_sentence",
            "confidence_sentence",
            "evidence_anchor_sentence",
        ):
            val = row.get(key)
            if isinstance(val, str):
                chunks.append(val)
    idl = stored.get("interpretation_display_layer_v1")
    if isinstance(idl, dict):
        for rec in idl.get("records") or []:
            if not isinstance(rec, dict):
                continue
            for key in (
                "retail_display_label",
                "subtitle",
                "why_it_matters",
                "user_safe_description",
                "display_caveat",
            ):
                val = rec.get(key)
                if isinstance(val, str):
                    chunks.append(val)
    cr = stored.get("clinician_report_v1")
    if isinstance(cr, dict):
        sections = cr.get("sections")
        if isinstance(sections, dict):
            page1 = sections.get("page1")
            if isinstance(page1, dict):
                for key in ("primary_concern", "top_hypothesis_line", "runner_up_why_not_lead_line"):
                    val = page1.get(key)
                    if isinstance(val, str):
                        chunks.append(val)
    return [c for c in chunks if c.strip()]


def find_user_facing_leakage(stored: Dict[str, Any]) -> List[str]:
    hits: List[str] = []
    for text in collect_user_facing_text(stored):
        for pattern in _PLACEHOLDER_PATTERNS:
            if pattern.search(text):
                hits.append(text[:120])
                break
    return hits
