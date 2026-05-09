"""Bounded tests for launch_core_proving_harness (fixture merge + matrix integrity only)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from core.pipeline.questionnaire_mapper import STATINS_LONG_TERM_MEDICATION_LABEL
from tools.launch_core_proving_harness import (
    DEFAULT_MATRIX,
    build_merged_fixture,
    load_matrix,
)

BACKEND = Path(__file__).resolve().parents[2]


def test_launch_core_matrix_ssot_statin_label_exact() -> None:
    raw = json.loads(DEFAULT_MATRIX.read_text(encoding="utf-8"))
    scenarios = raw.get("scenarios") or []
    statin_on = next((s for s in scenarios if isinstance(s, dict) and s.get("id") == "statin_on"), None)
    assert statin_on is not None
    qd = statin_on.get("questionnaire_data") or {}
    meds = qd.get("long_term_medications") or []
    assert meds == [STATINS_LONG_TERM_MEDICATION_LABEL]


def test_build_merged_fixture_omits_vs_sets_questionnaire(tmp_path: Path) -> None:
    panel_path = BACKEND / "tests" / "fixtures" / "panels" / "ab_full_panel_with_ranges.json"
    assert panel_path.exists()
    out_a = tmp_path / "baseline.json"
    build_merged_fixture(panel_path, {"questionnaire_data": None}, out_a)
    data_a = json.loads(out_a.read_text(encoding="utf-8"))
    assert "questionnaire_data" not in data_a

    out_b = tmp_path / "statin.json"
    build_merged_fixture(
        panel_path,
        {"questionnaire_data": {"long_term_medications": [STATINS_LONG_TERM_MEDICATION_LABEL]}},
        out_b,
    )
    data_b = json.loads(out_b.read_text(encoding="utf-8"))
    assert data_b.get("questionnaire_data", {}).get("long_term_medications") == [
        STATINS_LONG_TERM_MEDICATION_LABEL
    ]


def test_load_matrix_shape() -> None:
    panels, scenarios = load_matrix(DEFAULT_MATRIX)
    assert "AB" in panels and "VR" in panels
    ids = [str(s.get("id")) for s in scenarios]
    assert ids == ["baseline", "lifestyle_context", "statin_off", "statin_on"]
