"""
LC-S5 — Launch-core proving binary checks (CHECK 2, 5, 6).

Uses `docs/audit-papers/launch-core-proving/latest_fingerprints.json` produced by:
  python backend/tools/launch_core_proving_harness.py

CHECK 2 (hardening 2B-001): alcohol bridge is NOT asserted from AB__lifestyle_context fingerprints
(alcohol_units_per_week=7 is below moderate threshold). Instead, orchestrator run with alcohol_units_per_week>=8.

CHECK 5 / wave1_contradiction: conservative band_label vs consequence_sentence_head polarity checks on all matrix runs.

CHECK 6: clinician primary_concern_head vs narrative.retail_summary_head share homocysteine lead family on AB/VR baseline.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List

import pytest

from core.canonical.hba1c_layer_b_arbitration import arbitrate_hba1c_layer_b_input
from core.canonical.normalize import normalize_biomarkers_with_metadata
from core.pipeline.orchestrator import AnalysisOrchestrator, UNIT_NORMALISATION_META_KEY
from core.units.registry import UNIT_REGISTRY_VERSION, apply_unit_normalisation


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _fingerprints_path() -> Path:
    return _repo_root() / "docs" / "audit-papers" / "launch-core-proving" / "latest_fingerprints.json"


def _load_fingerprints() -> Dict[str, Any]:
    path = _fingerprints_path()
    assert path.is_file(), f"Missing proving fingerprints — run: python backend/tools/launch_core_proving_harness.py ({path})"
    return json.loads(path.read_text(encoding="utf-8"))


def _prepare_ab_fixture_panel() -> Dict[str, Any]:
    path = Path(__file__).resolve().parents[1] / "fixtures" / "panels" / "ab_full_panel_with_ranges.json"
    raw = json.loads(path.read_text(encoding="utf-8"))
    biomarkers = raw["biomarkers"]
    normalized = normalize_biomarkers_with_metadata(biomarkers)
    normalized = arbitrate_hba1c_layer_b_input(normalized)
    normalized = apply_unit_normalisation(normalized)
    normalized[UNIT_NORMALISATION_META_KEY] = {
        "unit_normalised": True,
        "unit_registry_version": UNIT_REGISTRY_VERSION,
    }
    return normalized


# Conservative: stable/optimal bands must not read like acute emergency; elevated bands must not read as "all clear".
_STABLE_FORBIDDEN = re.compile(
    r"\b(911|emergency\s+room|cardiac\s+arrest|imminent\s+death|grave\s+prognosis|life-?threatening\s+emergency)\b",
    re.IGNORECASE,
)
_REASSURING_FORBIDDEN = re.compile(
    r"\b(no\s+cause\s+for\s+concern|nothing\s+to\s+worry|perfectly\s+healthy|risk-?free|completely\s+fine)\b",
    re.IGNORECASE,
)


def _assert_consumer_domain_row_consistent(band_label: str, consequence_head: str, run_key: str) -> None:
    band = (band_label or "").strip().lower()
    cons = (consequence_head or "").strip()
    assert cons, f"{run_key}: empty consequence_sentence_head for band={band_label!r}"
    if band in ("stable", "low", "optimal"):
        assert not _STABLE_FORBIDDEN.search(cons), (
            f"{run_key}: stable-like band {band_label!r} must not carry emergency/danger wording: {cons[:200]!r}"
        )
    if band in ("strong", "attention", "review", "at_risk", "elevated", "high"):
        assert not _REASSURING_FORBIDDEN.search(cons), (
            f"{run_key}: concern-like band {band_label!r} must not carry falsely reassuring wording: {cons[:200]!r}"
        )


@pytest.mark.regression
def test_lc_s5_fingerprints_stamped_and_matrix_present() -> None:
    data = _load_fingerprints()
    sha = str(data.get("git_short_sha", "")).strip()
    assert len(sha) >= 7, "fingerprints missing git_short_sha"
    runs = data.get("runs") or {}
    for key in (
        "AB__baseline",
        "AB__lifestyle_context",
        "AB__statin_off",
        "AB__statin_on",
        "VR__baseline",
        "VR__lifestyle_context",
        "VR__statin_off",
        "VR__statin_on",
    ):
        assert key in runs, f"Missing harness run {key}"


@pytest.mark.regression
def test_check2_alcohol_bridge_language_when_moderate_threshold_met() -> None:
    """CHECK 2 — alcohol / one-carbon bridge language in body_overview (orchestrator injection, not matrix fixture)."""
    prepared = _prepare_ab_fixture_panel()
    user = {"user_id": "00000000-0000-0000-0000-00000000lc5c2", "age": 45, "gender": "male"}
    lifestyle_inputs = {
        "height_cm": 180,
        "weight_kg": 90,
        "waist_circumference_cm": 95,
        "systolic_bp": 145,
        "diastolic_bp": 88,
        "resting_heart_rate": 72,
        "smoking_status": "never",
        "alcohol_units_per_week": 10,
        "sleep_hours": 6.5,
    }
    orch = AnalysisOrchestrator()
    dto = orch.run(
        prepared,
        user,
        assume_canonical=True,
        lifestyle_inputs=lifestyle_inputs,
        fixed_analysis_id="lc-s5-check2-alcohol-bridge",
    )
    assert dto.status == "completed"
    body = (dto.narrative_report_v1.body_overview if dto.narrative_report_v1 else "") or ""
    low = body.lower()
    assert "moderate alcohol" in low or "questionnaire suggests" in low, (
        f"Expected alcohol lifestyle context in body_overview; got head: {low[:400]!r}"
    )
    assert "alcohol_intake_moderate_or_higher_with_one_carbon_lab_coherence" not in low


@pytest.mark.regression
def test_check5_wave1_consumer_domain_band_vs_consequence_consistency() -> None:
    """CHECK 5 — no obvious band vs headline contradiction across harness fingerprints."""
    data = _load_fingerprints()
    runs: Dict[str, Any] = data.get("runs") or {}
    for run_key, payload in runs.items():
        rows = payload.get("consumer_domain_rows") or []
        if not isinstance(rows, list):
            continue
        for row in rows:
            if not isinstance(row, dict):
                continue
            _assert_consumer_domain_row_consistent(
                str(row.get("band_label", "")),
                str(row.get("consequence_sentence_head", "")),
                run_key,
            )


@pytest.mark.regression
def test_check4_statin_intervention_and_bounded_framing_from_fingerprints() -> None:
    """CHECK 4 — statin_on vs statin_off: intervention present only when on; bounded analytical invariants."""
    data = _load_fingerprints()
    runs: Dict[str, Any] = data.get("runs") or {}
    for panel in ("AB", "VR"):
        off_key = f"{panel}__statin_off"
        on_key = f"{panel}__statin_on"
        fa = runs.get(off_key) or {}
        fb = runs.get(on_key) or {}
        assert fa, f"Missing harness run {off_key}"
        assert fb, f"Missing harness run {on_key}"

        assert fa.get("top_finding_signal_ids") == fb.get("top_finding_signal_ids"), (
            f"{panel}: top findings must match statin off/on"
        )
        assert fa.get("signal_state_by_id") == fb.get("signal_state_by_id"), (
            f"{panel}: signal states must match statin off/on"
        )
        assert fa.get("consumer_band_labels") == fb.get("consumer_band_labels"), (
            f"{panel}: consumer band labels must match statin off/on"
        )

        ia_off = fa.get("intervention") or {}
        ia_on = fb.get("intervention") or {}
        assert not ia_off.get("present"), f"{off_key}: intervention must be absent when statins off"
        assert ia_on.get("present"), f"{on_key}: intervention must be present when statins on"

        def _cv_consequence_head(payload: Dict[str, Any]) -> str:
            for row in payload.get("consumer_domain_rows") or []:
                if isinstance(row, dict) and "cardiovascular" in str(row.get("domain_id", "")):
                    return str(row.get("consequence_sentence_head", ""))
            return ""

        cv_off = _cv_consequence_head(fa)
        cv_on = _cv_consequence_head(fb)
        assert cv_off and cv_on, f"{panel}: cardiovascular consequence_sentence required"
        assert cv_off != cv_on, (
            f"{panel}: statin on must change cardiovascular consequence framing "
            f"(off={cv_off[:80]!r} on={cv_on[:80]!r})"
        )


@pytest.mark.regression
def test_check2_lifestyle_context_narrative_differs_from_baseline() -> None:
    """CHECK 2 — matrix lifestyle_context must change narrative vs baseline (fixture alcohol >= moderate)."""
    data = _load_fingerprints()
    runs: Dict[str, Any] = data.get("runs") or {}
    for panel in ("AB", "VR"):
        base = runs.get(f"{panel}__baseline") or {}
        life = runs.get(f"{panel}__lifestyle_context") or {}
        assert base and life, f"Missing baseline or lifestyle_context for {panel}"
        n0 = base.get("narrative") or {}
        n1 = life.get("narrative") or {}
        assert n0 != n1, f"{panel}: lifestyle_context must change narrative fingerprint vs baseline"
        bo = str((n1.get("body_overview_head") or "")).lower()
        assert "moderate alcohol" in bo or "questionnaire suggests" in bo, (
            f"{panel}: expected lifestyle context in body_overview_head: {bo[:240]!r}"
        )
        slug = "alcohol_intake_moderate_or_higher_with_one_carbon_lab_coherence"
        for field in ("body_overview_head", "lead_narrative_head", "retail_summary_head"):
            text = str((n1.get(field) or "")).lower()
            assert slug not in text, f"{panel}: internal lifestyle slug leaked in {field}"


@pytest.mark.regression
def test_check6_clinician_retail_lead_family_alignment_ab_vr_baseline() -> None:
    """CHECK 6 — primary_concern_head and retail_summary_head both anchor on homocysteine lead family."""
    data = _load_fingerprints()
    runs: Dict[str, Any] = data.get("runs") or {}
    for key in ("AB__baseline", "VR__baseline"):
        payload = runs.get(key) or {}
        clin = (payload.get("clinician_page1") or {}) if isinstance(payload.get("clinician_page1"), dict) else {}
        narrative = (payload.get("narrative") or {}) if isinstance(payload.get("narrative"), dict) else {}
        pc = str(clin.get("primary_concern_head", "")).lower()
        rs = str(narrative.get("retail_summary_head", "")).lower()
        assert "homocysteine" in pc, f"{key}: expected homocysteine in primary_concern_head: {pc[:240]!r}"
        assert "homocysteine" in rs, f"{key}: expected homocysteine in retail_summary_head: {rs[:240]!r}"

