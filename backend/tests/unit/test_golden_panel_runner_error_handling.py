import json
from pathlib import Path

import pytest

from core.canonical.alias_registry_service import AliasCollisionError
from tools.run_golden_panel import run_golden_panel


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_golden_panel_runner_writes_error_artifacts_on_canonical_collision(tmp_path):
    fixture = Path(__file__).parent.parent / "fixtures" / "collision_fixture_hdl.json"
    with pytest.raises(AliasCollisionError) as exc:
        run_golden_panel(
            fixture_path=fixture,
            output_root=tmp_path,
            run_id="unit-collision",
            write_narrative=False,
        )
    message = str(exc.value)
    assert "Alias collision for key" in message
    assert "canonical_ids=" in message
