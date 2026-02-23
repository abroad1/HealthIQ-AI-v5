"""
v5.3 Sprint 10 - ArbitrationScenarioRunner_v1.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from collections import deque
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from core.analytics.arbitration_engine import build_arbitration_result_v1, build_dominance_edges_v1
from core.analytics.arbitration_registry import load_arbitration_registry
from core.analytics.calibration_engine import build_calibration_layer_v1
from core.analytics.causal_edge_engine import build_causal_edges_v1
from core.analytics.conflict_detector import build_conflict_set_v1
from core.analytics.conflict_registry import load_conflict_registry
from core.analytics.evidence_registry import load_evidence_registry
from core.analytics.explainability_builder import build_explainability_report_v1
from core.analytics.precedence_engine import build_precedence_v1
from core.analytics.replay_manifest_builder import build_replay_manifest_v1
from core.analytics.scoring_policy_registry import load_scoring_policy
from core.contracts.calibration_layer_v1 import CalibrationItem
from core.contracts.insight_graph_v1 import InsightGraphV1
from core.contracts.state_engine_v1 import SystemStateNode
from tools.run_golden_panel import _normalise_for_artifact_write


def _default_fixture_path() -> Path:
    return Path(__file__).resolve().parent.parent / "tests" / "fixtures" / "arbitration_scenarios_v2.json"


def _default_output_root() -> Path:
    return Path(__file__).resolve().parent.parent / "artifacts" / "arbitration_runs"


def _git_short_sha() -> str:
    try:
        out = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], text=True)
        return out.strip()
    except Exception:
        return ""


def _read_fixture(path: Path) -> List[Dict[str, Any]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("Scenario fixture must be a JSON object")
    block = raw.get("scenarios", [])
    if not isinstance(block, list):
        raise ValueError("Scenario fixture must include list field: scenarios")
    rows: List[Dict[str, Any]] = []
    for item in block:
        if isinstance(item, dict) and str(item.get("scenario_id", "")).strip():
            rows.append(item)
    rows.sort(key=lambda item: str(item.get("scenario_id", "")))
    return rows


def _build_seed_graph(scenario: Dict[str, Any]) -> InsightGraphV1:
    nodes: List[SystemStateNode] = []
    for row in sorted(scenario.get("system_states", []), key=lambda x: str(x.get("system_id", ""))):
        nodes.append(
            SystemStateNode(
                system_id=str(row.get("system_id", "")),
                state_codes=sorted(set(str(x) for x in row.get("state_codes", []) if str(x).strip())),
                rationale_codes=[],
                transition_summary_codes=sorted(
                    set(str(x) for x in row.get("transition_summary_codes", []) if str(x).strip())
                ),
                confidence_bucket=str(row.get("confidence_bucket", "insufficient")),
            )
        )
    graph = InsightGraphV1(
        graph_version="1.0.0",
        analysis_id=str(scenario.get("scenario_id", "")),
        system_states=nodes,
        edges=[],
    )
    seed_tiers = scenario.get("baseline_calibration_tiers", {})
    if isinstance(seed_tiers, dict):
        graph.calibration_items = sorted(
            [
                CalibrationItem(
                    system_id=str(sid),
                    priority_tier=str(tier),
                    urgency_band="routine",
                    action_intensity="info",
                    stability_flag="stable",
                    explanation_codes=["calibration:scenario_seed"],
                    applied_rule_ids=[],
                )
                for sid, tier in seed_tiers.items()
                if str(sid).strip()
            ],
            key=lambda item: item.system_id,
        )
    return graph


def _build_report(
    graph: InsightGraphV1,
    replay_dump: Dict[str, Any],
) -> Dict[str, Any]:
    conflicts = [
        {
            "conflict_id": c.conflict_id,
            "conflict_type": c.conflict_type,
            "severity": c.conflict_severity,
            "system_ids": sorted([c.system_a, c.system_b]),
        }
        for c in graph.conflict_set
    ]
    conflicts.sort(key=lambda row: (row["conflict_id"], row["conflict_type"], row["system_ids"]))

    precedence_rows = [
        {
            "rule_id": e.rule_id,
            "conflict_id": e.conflict_id,
            "from_system_id": e.from_system_id,
            "to_system_id": e.to_system_id,
            "precedence_tier": e.precedence_tier,
            "conflict_type": e.conflict_type,
            "rationale_codes": sorted(set(e.rationale_codes)),
        }
        for e in graph.dominance_edges
    ]
    precedence_rows.sort(
        key=lambda row: (
            row["from_system_id"],
            row["to_system_id"],
            int(row["precedence_tier"]),
            row["rule_id"],
            row["conflict_id"],
        )
    )

    causal_rows = [
        {
            "edge_id": edge.edge_id,
            "from_system_id": edge.from_system_id,
            "to_system_id": edge.to_system_id,
            "edge_code": edge.edge_type,
            "priority": edge.priority,
            "source_conflict_ids": sorted(set(edge.source_conflict_ids)),
        }
        for edge in graph.causal_edges
    ]
    causal_rows.sort(
        key=lambda row: (
            -int(row["priority"]),
            row["from_system_id"],
            row["to_system_id"],
            row["edge_id"],
        )
    )

    driver = graph.primary_driver_system_id
    coupled_tier = ""
    coupled_reasons: List[str] = []
    for item in graph.calibration_items:
        if item.system_id == driver:
            coupled_tier = item.priority_tier
            coupled_reasons = sorted(set(item.explanation_codes))
            break

    return {
        "conflict_summary": conflicts,
        "precedence_summary": precedence_rows,
        "causal_edges": causal_rows,
        "arbitration_decisions": {
            "primary_driver_system_id": driver,
            "supporting_systems": sorted(set(graph.arbitration_result.supporting_system_ids)),
            "decision_trace": sorted(set(graph.arbitration_result.decision_trace_codes)),
            "tie_breakers": sorted(set(graph.arbitration_result.tie_breaker_codes)),
        },
        "calibration_impact": {
            "system_id": driver,
            "final_calibration_tier": coupled_tier,
            "reasons": coupled_reasons,
        },
        "replay_stamps": {
            "conflict_registry_version": replay_dump.get("conflict_registry_version", ""),
            "conflict_registry_hash": replay_dump.get("conflict_registry_hash", ""),
            "arbitration_registry_version": replay_dump.get("arbitration_registry_version", ""),
            "arbitration_registry_hash": replay_dump.get("arbitration_registry_hash", ""),
            "arbitration_version": replay_dump.get("arbitration_version", ""),
            "arbitration_hash": replay_dump.get("arbitration_hash", ""),
        },
    }


def _compute_transitive_edges(precedence_rows: List[Dict[str, Any]]) -> Tuple[List[Dict[str, str]], bool]:
    systems = sorted(
        set(
            [str(r.get("from_system_id", "")) for r in precedence_rows]
            + [str(r.get("to_system_id", "")) for r in precedence_rows]
        )
    )
    adjacency: Dict[str, set[str]] = {sid: set() for sid in systems}
    indegree: Dict[str, int] = {sid: 0 for sid in systems}
    direct_pairs: set[Tuple[str, str]] = set()
    for row in precedence_rows:
        src = str(row.get("from_system_id", ""))
        dst = str(row.get("to_system_id", ""))
        if not src or not dst:
            continue
        if dst not in adjacency[src]:
            adjacency[src].add(dst)
            indegree[dst] = indegree.get(dst, 0) + 1
            direct_pairs.add((src, dst))

    queue = deque(sorted([sid for sid, deg in indegree.items() if deg == 0]))
    topo: List[str] = []
    indegree_work = dict(indegree)
    while queue:
        node = queue.popleft()
        topo.append(node)
        for nxt in sorted(adjacency.get(node, set())):
            indegree_work[nxt] -= 1
            if indegree_work[nxt] == 0:
                queue.append(nxt)

    has_cycle = len(topo) != len(systems)
    if has_cycle:
        return [], True

    reachability: Dict[str, set[str]] = {sid: set() for sid in systems}
    for node in reversed(topo):
        for nxt in sorted(adjacency.get(node, set())):
            reachability[node].add(nxt)
            reachability[node].update(reachability[nxt])

    rows: List[Dict[str, str]] = []
    for src in sorted(reachability.keys()):
        for dst in sorted(reachability[src]):
            if (src, dst) in direct_pairs:
                continue
            rows.append(
                {
                    "from_system_id": src,
                    "to_system_id": dst,
                    "edge_id": f"transitive:{src}>{dst}",
                    "source": "transitive",
                }
            )
    rows.sort(key=lambda row: (row["from_system_id"], row["to_system_id"], row["edge_id"]))
    return rows, False


def _build_explainability_report(
    graph: InsightGraphV1,
    replay_dump: Dict[str, Any],
    run_id: str,
    scenario_id: str,
    git_commit_short: str,
    generated_at_utc: str,
) -> Any:
    return build_explainability_report_v1(
        graph,
        run_id=run_id,
        scenario_id=scenario_id,
        git_commit_short=git_commit_short,
        generated_at_utc=generated_at_utc,
        conflict_registry_version=str(replay_dump.get("conflict_registry_version", "")),
        conflict_registry_hash=str(replay_dump.get("conflict_registry_hash", "")),
        arbitration_registry_version=str(replay_dump.get("arbitration_registry_version", "")),
        arbitration_registry_hash=str(replay_dump.get("arbitration_registry_hash", "")),
        arbitration_version=str(replay_dump.get("arbitration_version", "")),
        arbitration_hash=str(replay_dump.get("arbitration_hash", "")),
    )


def _scenario_summary(graph: InsightGraphV1) -> str:
    conflict_types = sorted(set(c.conflict_type for c in graph.conflict_set))
    supporting = sorted(set(graph.arbitration_result.supporting_system_ids))
    return (
        f"primary_driver_system_id={graph.primary_driver_system_id}\n"
        f"supporting_system_ids={','.join(supporting)}\n"
        f"conflict_count={len(graph.conflict_set)}\n"
        f"conflict_types={','.join(conflict_types)}\n"
        f"arbitration_hash={graph.arbitration_hash}\n"
    )


def _run_one_scenario(
    scenario: Dict[str, Any],
    scenarios_dir: Path,
    run_id: str,
    git_commit_short: str,
    generated_at_utc: str,
) -> Dict[str, Any]:
    seed_graph = _build_seed_graph(scenario)

    precedence_out, precedence_stamp = build_precedence_v1(seed_graph)
    seed_graph.precedence_output = precedence_out
    seed_graph.precedence_engine_version = precedence_stamp.precedence_engine_version
    seed_graph.precedence_engine_hash = precedence_stamp.precedence_engine_hash

    conflicts = build_conflict_set_v1(seed_graph)
    dominance_edges = build_dominance_edges_v1(seed_graph, conflicts)
    causal_edges = build_causal_edges_v1(conflicts, dominance_edges)
    primary_driver, arb_result, arb_stamp = build_arbitration_result_v1(
        seed_graph,
        conflicts,
        dominance_edges,
        causal_edges,
    )

    seed_graph.conflict_set = conflicts
    seed_graph.dominance_edges = dominance_edges
    seed_graph.causal_edges = causal_edges
    seed_graph.primary_driver_system_id = primary_driver
    seed_graph.arbitration_result = arb_result
    seed_graph.arbitration_version = arb_stamp.arbitration_version
    seed_graph.arbitration_hash = arb_stamp.arbitration_hash

    coupled, cal_stamp = build_calibration_layer_v1(seed_graph, apply_arbitration_coupling=True)
    seed_graph.calibration_items = coupled
    seed_graph.calibration_version = cal_stamp.calibration_version
    seed_graph.calibration_hash = cal_stamp.calibration_hash

    conflict_stamp = load_conflict_registry().stamp
    arb_reg_stamp = load_arbitration_registry().stamp
    scoring_stamp = load_scoring_policy().stamp
    evidence_stamp = load_evidence_registry().stamp

    replay = build_replay_manifest_v1(
        "",
        "",
        "",
        "",
        insight_graph=seed_graph,
        scoring_policy_version=scoring_stamp.scoring_policy_version,
        scoring_policy_hash=scoring_stamp.scoring_policy_hash,
        evidence_registry_version=evidence_stamp.evidence_registry_version,
        evidence_registry_hash=evidence_stamp.evidence_registry_hash,
        state_engine_version=getattr(seed_graph, "state_engine_version", ""),
        state_engine_hash=getattr(seed_graph, "state_engine_hash", ""),
        precedence_engine_version=getattr(seed_graph, "precedence_engine_version", ""),
        precedence_engine_hash=getattr(seed_graph, "precedence_engine_hash", ""),
        causal_layer_version=getattr(seed_graph, "causal_layer_version", ""),
        causal_layer_hash=getattr(seed_graph, "causal_layer_hash", ""),
        calibration_version=getattr(seed_graph, "calibration_version", ""),
        calibration_hash=getattr(seed_graph, "calibration_hash", ""),
        conflict_registry_version=conflict_stamp.conflict_registry_version,
        conflict_registry_hash=conflict_stamp.conflict_registry_hash,
        arbitration_registry_version=arb_reg_stamp.arbitration_registry_version,
        arbitration_registry_hash=arb_reg_stamp.arbitration_registry_hash,
        arbitration_version=getattr(seed_graph, "arbitration_version", ""),
        arbitration_hash=getattr(seed_graph, "arbitration_hash", ""),
        linked_snapshot_ids=[],
        analysis_result_version="1.0.0",
    )
    replay_dump = replay.model_dump()

    report = _build_report(seed_graph, replay_dump)
    explainability = _build_explainability_report(
        graph=seed_graph,
        replay_dump=replay_dump,
        run_id=run_id,
        scenario_id=str(scenario.get("scenario_id", "")),
        git_commit_short=git_commit_short,
        generated_at_utc=generated_at_utc,
    )
    explainability_primary = explainability.arbitration_decisions.primary_driver_system_id
    if explainability_primary != seed_graph.primary_driver_system_id:
        raise ValueError("Single-authority primary driver mismatch between explainability and insight graph")
    final_graph_dump = seed_graph.model_dump()

    scenario_id = str(scenario.get("scenario_id", ""))
    out_dir = scenarios_dir / scenario_id
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "insight_graph.json").write_text(
        json.dumps(_normalise_for_artifact_write(final_graph_dump), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (out_dir / "arbitration_report.json").write_text(
        json.dumps(_normalise_for_artifact_write(report), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (out_dir / "replay_manifest.json").write_text(
        json.dumps(_normalise_for_artifact_write(replay_dump), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (out_dir / "explainability_report.json").write_text(
        json.dumps(_normalise_for_artifact_write(explainability.model_dump()), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (out_dir / "summary.txt").write_text(_scenario_summary(seed_graph), encoding="utf-8")

    return {
        "scenario_id": scenario_id,
        "primary_driver_system_id": primary_driver,
        "arbitration_hash": seed_graph.arbitration_hash,
        "explainability_hash": explainability.replay_stamps.explainability_hash,
        "conflict_count": len(seed_graph.conflict_set),
        "conflict_types": sorted(set(c.conflict_type for c in seed_graph.conflict_set)),
    }


def run_arbitration_scenarios(
    fixture_path: Optional[Path] = None,
    output_root: Optional[Path] = None,
    run_id: Optional[str] = None,
    scenario_id: Optional[str] = None,
    write_narrative: bool = False,
) -> Tuple[Path, Dict[str, Any]]:
    fixture = fixture_path or _default_fixture_path()
    out_root = output_root or _default_output_root()
    if write_narrative:
        pass
    rid = run_id or datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    run_dir = out_root / rid
    scenarios_dir = run_dir / "scenarios"
    scenarios_dir.mkdir(parents=True, exist_ok=True)

    scenarios = _read_fixture(fixture)
    if scenario_id:
        scenarios = [row for row in scenarios if str(row.get("scenario_id", "")) == scenario_id]
    if not scenarios:
        raise ValueError("No scenarios selected for execution")

    git_commit_short = _git_short_sha()
    generated_at_utc = datetime.now(UTC).isoformat()
    rows = [
        _run_one_scenario(
            row,
            scenarios_dir,
            run_id=rid,
            git_commit_short=git_commit_short,
            generated_at_utc=generated_at_utc,
        )
        for row in scenarios
    ]
    rows.sort(key=lambda row: row["scenario_id"])

    conflict_stamp = load_conflict_registry().stamp
    arb_reg_stamp = load_arbitration_registry().stamp
    manifest = {
        "run_id": rid,
        "fixture_path": str(fixture),
        "output_root": str(out_root),
        "git_commit_short": git_commit_short,
        "generated_at_utc": generated_at_utc,
        "registry_stamps": {
            "conflict_registry_version": conflict_stamp.conflict_registry_version,
            "conflict_registry_hash": conflict_stamp.conflict_registry_hash,
            "arbitration_registry_version": arb_reg_stamp.arbitration_registry_version,
            "arbitration_registry_hash": arb_reg_stamp.arbitration_registry_hash,
        },
        "scenario_results": rows,
    }
    (run_dir / "manifest.json").write_text(
        json.dumps(_normalise_for_artifact_write(manifest), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return run_dir, manifest


def _cli() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic arbitration scenarios and write per-scenario artifacts.")
    parser.add_argument("--fixture", default=str(_default_fixture_path()), help="Path to scenario fixture JSON")
    parser.add_argument("--output-root", default=str(_default_output_root()), help="Root folder for scenario artifacts")
    parser.add_argument("--run-id", default=None, help="Output folder id")
    parser.add_argument("--scenario-id", default=None, help="Run only one scenario id")
    parser.add_argument("--no-narrative", action="store_true", help="Narrative output is disabled for this runner")
    args = parser.parse_args()

    run_dir, manifest = run_arbitration_scenarios(
        fixture_path=Path(args.fixture),
        output_root=Path(args.output_root),
        run_id=args.run_id,
        scenario_id=args.scenario_id,
        write_narrative=not args.no_narrative and False,
    )
    print(f"Arbitration scenarios run complete: {run_dir}")
    print(f"Scenarios: {len(manifest.get('scenario_results', []))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
