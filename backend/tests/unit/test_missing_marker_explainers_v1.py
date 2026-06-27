"""N-5 adjunct — missing-marker explainer pack v1 structure."""

from __future__ import annotations

from pathlib import Path

import yaml

_PACK = (
    Path(__file__).resolve().parents[3]
    / "knowledge_bus"
    / "missing_marker_explainers_v1"
    / "missing_marker_explainers_v1.yaml"
)

_REQUIRED_KEYS = (
    "missing_marker_id",
    "biomarker_id",
    "benchmark_domain",
    "display_title",
    "caution_when_absent",
    "interpretive_limit",
    "interpretive_caution",
)


def _load_pack() -> dict:
    raw = yaml.safe_load(_PACK.read_text(encoding="utf-8"))
    assert isinstance(raw, dict)
    return raw


def test_pack_metadata():
    data = _load_pack()
    assert data.get("schema_version") == "1.0.0"
    assert data.get("pack_version") == "1.0.0"
    assert "missing_marker_explainers_v1" in str(data.get("authority", ""))


def test_missing_marker_entries_present():
    data = _load_pack()
    rows = data.get("missing_markers")
    assert isinstance(rows, list) and len(rows) >= 5
    ids = {r.get("missing_marker_id") for r in rows}
    assert "missing_ferritin_iron_context_v1" in ids
    assert "missing_egfr_renal_context_v1" in ids


def test_missing_marker_fields_substantive():
    data = _load_pack()
    for row in data["missing_markers"]:
        for key in _REQUIRED_KEYS:
            assert key in row, f"missing {key} in {row.get('missing_marker_id')}"
        for prose_key in ("caution_when_absent", "interpretive_limit", "interpretive_caution", "display_title"):
            assert len(str(row[prose_key]).strip()) > 20, prose_key
