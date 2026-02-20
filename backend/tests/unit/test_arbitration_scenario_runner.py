"""
v5.3 Sprint 10 - Unit tests for ArbitrationScenarioRunner_v1.
"""

import json
from pathlib import Path

from tools.run_arbitration_scenarios import run_arbitration_scenarios


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _fixture_path() -> Path:
    return Path(__file__).parent.parent / "fixtures" / "arbitration_scenarios_v2.json"


def test_scenario_runner_writes_required_artifacts_and_expected_driver(tmp_path):
    fixture = _fixture_path()
    run_dir, manifest = run_arbitration_scenarios(
        fixture_path=fixture,
        output_root=tmp_path,
        run_id="unit-arb-runner-a",
        scenario_id=None,
        write_narrative=False,
    )
    assert (run_dir / "manifest.json").exists()
    assert len(manifest.get("scenario_results", [])) >= 2

    fixture_rows = _load_json(fixture)["scenarios"]
    expected_driver = {
        str(row["scenario_id"]): str(row["expected"]["primary_driver_system_id"])
        for row in fixture_rows
    }
    for row in manifest["scenario_results"][:2]:
        sid = row["scenario_id"]
        sdir = run_dir / "scenarios" / sid
        assert (sdir / "insight_graph.json").exists()
        assert (sdir / "arbitration_report.json").exists()
        assert (sdir / "replay_manifest.json").exists()
        assert (sdir / "summary.txt").exists()

        report = _load_json(sdir / "arbitration_report.json")
        replay = _load_json(sdir / "replay_manifest.json")
        assert "conflict_summary" in report
        assert "precedence_summary" in report
        assert "causal_edges" in report
        assert "arbitration_decisions" in report
        assert "replay_stamps" in report
        assert report["arbitration_decisions"]["primary_driver_system_id"] == expected_driver[sid]
        assert replay.get("arbitration_version")
        assert replay.get("arbitration_hash")
        assert replay.get("conflict_registry_version")
        assert replay.get("conflict_registry_hash")
        assert replay.get("arbitration_registry_version")
        assert replay.get("arbitration_registry_hash")


def test_scenario_runner_hash_is_stable_across_repeated_runs(tmp_path):
    fixture = _fixture_path()
    _, m1 = run_arbitration_scenarios(
        fixture_path=fixture,
        output_root=tmp_path / "a",
        run_id="unit-arb-runner-b1",
        scenario_id="transitive_depth_chain",
        write_narrative=False,
    )
    _, m2 = run_arbitration_scenarios(
        fixture_path=fixture,
        output_root=tmp_path / "b",
        run_id="unit-arb-runner-b2",
        scenario_id="transitive_depth_chain",
        write_narrative=False,
    )
    h1 = m1["scenario_results"][0]["arbitration_hash"]
    h2 = m2["scenario_results"][0]["arbitration_hash"]
    assert h1 == h2
