import json
from pathlib import Path

from tools.run_golden_panel import run_golden_panel


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_golden_panel_runner_writes_error_artifacts_on_canonical_collision(tmp_path):
    fixture = Path(__file__).parent.parent / "fixtures" / "collision_fixture_hdl.json"
    run_dir, result = run_golden_panel(
        fixture_path=fixture,
        output_root=tmp_path,
        run_id="unit-collision",
        write_narrative=False,
    )

    assert run_dir.exists()
    assert result.get("status") == "error"
    assert result.get("error_type") == "canonical_collision"

    analysis_path = run_dir / "analysis_result.json"
    error_path = run_dir / "error.json"
    assert analysis_path.exists()
    assert error_path.exists()

    analysis = _load_json(analysis_path)
    assert analysis.get("status") == "error"
    assert analysis.get("error_type") == "canonical_collision"
    payload = analysis.get("error_payload", {})
    assert isinstance(payload, dict)
    collisions = payload.get("collisions", [])
    assert isinstance(collisions, list) and collisions
    first = collisions[0]
    assert first.get("canonical_id") == "hdl_cholesterol"
