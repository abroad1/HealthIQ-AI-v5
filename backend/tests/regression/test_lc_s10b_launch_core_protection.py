"""
LC-S10B — Durable protection for the proven launch-core slice (Sprint 6).

Guards behaviours proven in LC-S8D, FE-S8E, LC-S9B, and LC-S9C via fingerprints and targeted regression.
Does not change analytical behaviour; fails on drift or consumer-facing leakage.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[3]
_FINGERPRINTS = _REPO_ROOT / "docs" / "audit-papers" / "launch-core-proving" / "latest_fingerprints.json"

_MATRIX_RUN_KEYS = (
    "AB__baseline",
    "AB__lifestyle_context",
    "AB__statin_off",
    "AB__statin_on",
    "VR__baseline",
    "VR__lifestyle_context",
    "VR__statin_off",
    "VR__statin_on",
)

_LIFESTYLE_SLUG = "alcohol_intake_moderate_or_higher_with_one_carbon_lab_coherence"
_NARRATIVE_USER_FIELDS = ("body_overview_head", "lead_narrative_head", "retail_summary_head")
_CLINICIAN_USER_FIELDS = ("primary_concern_head", "key_findings_head", "top_hypothesis_line_head")

_WHY_FALLBACK_FORBIDDEN = re.compile(r"No governed WHY for signal_", re.IGNORECASE)
_RAW_SIGNAL_ID = re.compile(r"\bsignal_[a-z0-9_]+\b", re.IGNORECASE)


def _load_fingerprints() -> Dict[str, Any]:
    assert _FINGERPRINTS.is_file(), (
        f"Missing proving fingerprints — run: python backend/tools/launch_core_proving_harness.py ({_FINGERPRINTS})"
    )
    return json.loads(_FINGERPRINTS.read_text(encoding="utf-8"))


def _user_facing_text_chunks(payload: Dict[str, Any]) -> Iterable[tuple[str, str]]:
    narrative = payload.get("narrative") or {}
    if isinstance(narrative, dict):
        for field in _NARRATIVE_USER_FIELDS:
            yield f"narrative.{field}", str(narrative.get(field) or "")
    clinician = payload.get("clinician_page1") or {}
    if isinstance(clinician, dict):
        for field in _CLINICIAN_USER_FIELDS:
            yield f"clinician_page1.{field}", str(clinician.get(field) or "")
    for row in payload.get("consumer_domain_rows") or []:
        if isinstance(row, dict):
            did = str(row.get("domain_id") or "domain")
            yield f"consumer_domain_rows.{did}", str(row.get("consequence_sentence_head") or "")


@pytest.mark.regression
def test_lc_s10b_matrix_runs_present_with_consumer_domain_rows() -> None:
    data = _load_fingerprints()
    runs = data.get("runs") or {}
    for key in _MATRIX_RUN_KEYS:
        assert key in runs, f"Missing harness run {key}"
        rows = runs[key].get("consumer_domain_rows")
        assert isinstance(rows, list) and len(rows) >= 1, (
            f"{key}: consumer_domain_rows required for CHECK 4/5 protection"
        )


@pytest.mark.regression
def test_lc_s10b_no_lifestyle_slug_or_why_fallback_leakage() -> None:
    data = _load_fingerprints()
    runs: Dict[str, Any] = data.get("runs") or {}
    for run_key, payload in runs.items():
        if run_key not in _MATRIX_RUN_KEYS:
            continue
        for field_path, text in _user_facing_text_chunks(payload):
            low = text.lower()
            assert _LIFESTYLE_SLUG not in low, f"{run_key}: lifestyle slug in {field_path}"
            assert not _WHY_FALLBACK_FORBIDDEN.search(text), (
                f"{run_key}: WHY fallback debug in {field_path}: {text[:120]!r}"
            )
            for match in _RAW_SIGNAL_ID.finditer(text):
                assert False, (
                    f"{run_key}: raw signal id {match.group(0)!r} in {field_path}"
                )


@pytest.mark.regression
def test_lc_s10b_fingerprint_sha_stamped() -> None:
    data = _load_fingerprints()
    sha = str(data.get("git_short_sha", "")).strip()
    assert len(sha) >= 7, "fingerprints must record git_short_sha for drift traceability"
