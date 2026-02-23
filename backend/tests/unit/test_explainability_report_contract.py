"""
v5.3 Sprint 11 - Explainability report contract and ordering tests.
"""

import json
from pathlib import Path

from tools.run_arbitration_scenarios import run_arbitration_scenarios


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _fixture_path() -> Path:
    return Path(__file__).parent.parent / "fixtures" / "arbitration_scenarios_v2.json"


def test_explainability_report_contains_required_keys_and_sorted_sections(tmp_path):
    run_dir, _ = run_arbitration_scenarios(
        fixture_path=_fixture_path(),
        output_root=tmp_path,
        run_id="unit-explainability-contract",
        scenario_id="transitive_depth_chain",
        write_narrative=False,
    )
    report = _load_json(
        run_dir / "scenarios" / "transitive_depth_chain" / "explainability_report.json"
    )
    assert "run_metadata" in report
    assert "conflict_summary" in report
    assert "precedence_summary" in report
    assert "dominance_resolution" in report
    assert "causal_edges" in report
    assert "arbitration_decisions" in report
    assert "calibration_impact" in report
    assert "replay_stamps" in report

    conflicts = report["conflict_summary"]
    assert conflicts == sorted(
        conflicts,
        key=lambda row: (
            row["conflict_type"],
            row["conflict_id"],
            row["from_system_id"],
            row["to_system_id"],
            row["severity"],
        ),
    )
    precedence = report["precedence_summary"]
    assert precedence == sorted(
        precedence,
        key=lambda row: (
            int(row["precedence_tier"]),
            row["rule_id"],
            row["from_system_id"],
            row["to_system_id"],
            row["conflict_id"],
        ),
    )
    direct_edges = report["dominance_resolution"]["direct_edges"]
    assert direct_edges == sorted(
        direct_edges,
        key=lambda row: (row["from_system_id"], row["to_system_id"], row["edge_id"]),
    )
    transitive_edges = report["dominance_resolution"]["transitive_edges"]
    assert transitive_edges == sorted(
        transitive_edges,
        key=lambda row: (row["from_system_id"], row["to_system_id"], row["edge_id"]),
    )
    influence_ordering = report["dominance_resolution"]["influence_ordering"]
    assert influence_ordering.get("primary_driver_system_id")
    assert isinstance(influence_ordering.get("supporting_systems", []), list)
    assert isinstance(influence_ordering.get("influence_order", []), list)
    assert influence_ordering["influence_order"][0] == influence_ordering["primary_driver_system_id"]
    causal_edges = report["causal_edges"]
    assert causal_edges == sorted(
        causal_edges,
        key=lambda row: (
            -int(row["priority"]),
            row["from_system_id"],
            row["to_system_id"],
            row["edge_id"],
        ),
    )
    assert report["arbitration_decisions"]["supporting_systems"] == sorted(
        report["arbitration_decisions"]["supporting_systems"]
    )
    assert report["calibration_impact"]["reasons"] == sorted(
        report["calibration_impact"]["reasons"]
    )
