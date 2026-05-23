"""
LC-S20/22 — Persisted replay, stale-result strategy, Sentinel Phase 2 scaffold.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any, Dict

import pytest

from core.dto.builders import build_analysis_result_dto
from core.dto.frontend_contract_v1 import FRONTEND_CONSUMED_ROOT_KEYS
from core.dto.persisted_replay_contract_v1 import (
    CURRENT_RESULT_VERSION,
    PERSISTED_RENDER_REQUIRED_KEYS,
    PersistedReplayCompatibilityError,
    assess_persisted_result_compatibility,
    find_user_facing_leakage,
    validate_persisted_result_for_replay,
)

_REPO_ROOT = Path(__file__).resolve().parents[3]
_FIXTURE = _REPO_ROOT / "backend" / "tests" / "fixtures" / "persisted_results" / "lc_s20_ab_launch_core_v1.json"
_SCAFFOLD_PACK = _REPO_ROOT / "sentinel" / "packs" / "scaffold_lc_s20_22_replay_render_v1.json"


def _load_fixture() -> Dict[str, Any]:
    assert _FIXTURE.is_file(), f"missing persisted fixture: {_FIXTURE}"
    data = json.loads(_FIXTURE.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


@pytest.mark.regression
def test_lc_s20_persisted_fixture_loads() -> None:
    payload = _load_fixture()
    assert payload.get("analysis_id") == "lc-s20-persisted-fixture-v1"


@pytest.mark.regression
def test_lc_s20_required_root_keys_present() -> None:
    payload = _load_fixture()
    assert frozenset(payload.keys()) == FRONTEND_CONSUMED_ROOT_KEYS


@pytest.mark.regression
def test_lc_s20_render_required_fields_present() -> None:
    payload = _load_fixture()
    missing = PERSISTED_RENDER_REQUIRED_KEYS - set(payload.keys())
    assert not missing, missing


@pytest.mark.regression
def test_lc_s20_replay_manifest_parseable() -> None:
    payload = _load_fixture()
    replay = payload.get("replay_manifest")
    assert isinstance(replay, dict)
    assert str(replay.get("manifest_version") or "").strip()


@pytest.mark.regression
def test_lc_s20_result_version_present_and_current() -> None:
    payload = _load_fixture()
    assert payload.get("result_version") == CURRENT_RESULT_VERSION


@pytest.mark.regression
def test_lc_s20_stale_version_detectable() -> None:
    payload = copy.deepcopy(_load_fixture())
    payload["result_version"] = "0.9.0"
    assessment = assess_persisted_result_compatibility(payload)
    assert assessment.stale is True
    assert any("result_version_mismatch" in r for r in assessment.stale_reasons)


@pytest.mark.regression
def test_lc_s20_missing_critical_field_fails_loudly() -> None:
    payload = copy.deepcopy(_load_fixture())
    del payload["consumer_domain_scores"]
    with pytest.raises(PersistedReplayCompatibilityError, match="incompatible"):
        validate_persisted_result_for_replay(payload)


@pytest.mark.regression
def test_lc_s20_api_dto_replay_path_accepts_fixture() -> None:
    payload = _load_fixture()
    validate_persisted_result_for_replay(payload)
    roundtrip = build_analysis_result_dto(payload)
    assert frozenset(roundtrip.keys()) == FRONTEND_CONSUMED_ROOT_KEYS


@pytest.mark.regression
def test_lc_s22_render_smoke_primary_finding_present() -> None:
    payload = _load_fixture()
    assessment = assess_persisted_result_compatibility(payload)
    assert "missing_primary_finding" not in assessment.render_blockers


@pytest.mark.regression
def test_lc_s22_render_smoke_wave1_domain_cards_present() -> None:
    payload = _load_fixture()
    assessment = assess_persisted_result_compatibility(payload)
    assert "missing_wave1_domain_cards" not in assessment.render_blockers


@pytest.mark.regression
def test_lc_s22_no_placeholder_or_internal_token_leakage() -> None:
    payload = _load_fixture()
    leaks = find_user_facing_leakage(payload)
    assert not leaks, leaks


@pytest.mark.regression
def test_lc_s22_homocysteine_primary_content_in_fixture() -> None:
    payload = _load_fixture()
    combined = json.dumps(
        {
            "narrative": payload.get("narrative_report_v1"),
            "clinician": payload.get("clinician_report_v1"),
        }
    ).lower()
    assert "homocysteine" in combined or "methylation" in combined


@pytest.mark.regression
def test_lc_s22_scaffold_sentinel_pack_valid() -> None:
    assert _SCAFFOLD_PACK.is_file()
    pack = json.loads(_SCAFFOLD_PACK.read_text(encoding="utf-8"))
    classes = pack.get("defect_classes") or {}
    assert len(classes) >= 8
    for entry in classes.values():
        assert entry.get("test_file") == "backend/tests/regression/test_lc_s20_22_persisted_replay_sentinel_phase2.py"
        assert entry.get("status") == "GUARDED"


def _escaped_pack() -> Dict[str, Any]:
    path = _REPO_ROOT / "sentinel" / "packs" / "escaped_defects_v1.json"
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.mark.regression
@pytest.mark.parametrize(
    "defect_class",
    [
        "persisted_result_schema_incompatible",
        "persisted_result_render_failure",
        "stale_analysis_unmarked",
        "results_page_missing_primary_finding",
        "results_page_placeholder_text_visible",
        "results_page_internal_token_visible",
        "results_page_missing_domain_cards",
        "results_page_unit_display_regression",
    ],
)
def test_lc_s22_sentinel_defect_classes_registered(defect_class: str) -> None:
    classes = (_escaped_pack().get("defect_classes") or {})
    scaffold = json.loads(_SCAFFOLD_PACK.read_text(encoding="utf-8")).get("defect_classes") or {}
    entry = classes.get(defect_class) or scaffold.get(defect_class)
    assert entry is not None, defect_class
    assert entry.get("status") == "GUARDED"


@pytest.mark.regression
def test_lc_s22_biomarker_display_fidelity_fields_in_fixture() -> None:
    payload = _load_fixture()
    hcy = next(
        (b for b in payload.get("biomarkers") or [] if isinstance(b, dict) and b.get("biomarker_name") == "homocysteine"),
        None,
    )
    assert hcy is not None
    assert hcy.get("value") is not None
    assert str(hcy.get("unit") or "").strip()


@pytest.mark.regression
def test_lc_s22_persisted_result_replay_promoted_from_placeholder() -> None:
    entry = (_escaped_pack().get("defect_classes") or {}).get("persisted_result_replay")
    assert entry is not None
    assert entry.get("status") == "GUARDED"
    assert "test_lc_s20_22_persisted_replay_sentinel_phase2.py" in str(entry.get("test_file"))
