import json
from pathlib import Path

import pytest

from tools.run_golden_panel import run_golden_panel


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_golden_panel_runner_writes_error_artifacts_on_canonical_collision(tmp_path):
    """Golden runner returns error artifacts (no raise) when fixture has canonical collisions."""
    fixture = Path(__file__).parent.parent / "fixtures" / "collision_fixture_hdl.json"
    run_dir, result = run_golden_panel(
        fixture_path=fixture,
        output_root=tmp_path,
        run_id="unit-collision",
        write_narrative=False,
    )
    assert result.get("status") == "error"
    assert result.get("error_type") == "canonical_collision"
    collisions = result.get("error_payload", {}).get("collisions", [])
    assert len(collisions) > 0
    assert all("canonical_id" in c and "raw_markers" in c for c in collisions)
    assert (run_dir / "error.json").exists()
    error_json = _load_json(run_dir / "error.json")
    assert error_json.get("error_type") == "canonical_collision"
