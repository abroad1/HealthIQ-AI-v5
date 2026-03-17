#!/usr/bin/env python3
"""
Validate interaction_map_v1 against signal registry and phenotype governance coverage.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

import yaml


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INTERACTION_MAP_PATH = ROOT / "knowledge_bus" / "interaction_maps" / "interaction_map_v1.yaml"
DEFAULT_PHENOTYPE_MAP_PATH = ROOT / "knowledge_bus" / "phenotypes" / "phenotype_map_v1.yaml"
DEFAULT_PACKAGES_ROOT = ROOT / "knowledge_bus" / "packages"
STOP_EMPTY_ALLOWED = (
    "STOP validate_interaction_map_v1: phenotype_map contains no required_edges entries. "
    "Cannot evaluate phenotype coverage with empty allowed set. Verify KB-S35 phenotype map is "
    "populated before running this validator."
)


def _load_yaml(path: Path) -> Dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(payload, dict):
        raise ValueError(f"YAML document must be a mapping: {path}")
    return payload


def _collect_known_signal_ids(packages_root: Path) -> Set[str]:
    known: Set[str] = set()
    for signal_path in sorted(packages_root.rglob("signal_library.yaml")):
        payload = yaml.safe_load(signal_path.read_text(encoding="utf-8")) or {}
        if not isinstance(payload, dict):
            continue
        for row in payload.get("signals", []) or []:
            if not isinstance(row, dict):
                continue
            signal_id = str(row.get("signal_id", "")).strip()
            if signal_id:
                known.add(signal_id)
    return known


def _get_edge_signals(edge: Dict[str, Any]) -> Tuple[str, str]:
    from_signal = str(edge.get("from_signal", edge.get("from_signal_id", ""))).strip()
    to_signal = str(edge.get("to_signal", edge.get("to_signal_id", ""))).strip()
    return from_signal, to_signal


def _build_allowed_edges(
    phenotype_payload: Dict[str, Any],
) -> Tuple[Set[Tuple[str, str]], Dict[Tuple[str, str], List[Tuple[str, str]]]]:
    allowed: Set[Tuple[str, str]] = set()
    rationale_by_edge: Dict[Tuple[str, str], List[Tuple[str, str]]] = {}
    phenotypes = phenotype_payload.get("phenotypes", []) or []

    for phenotype in phenotypes:
        if not isinstance(phenotype, dict):
            continue
        phenotype_id = str(phenotype.get("phenotype_id", "")).strip() or "unknown"
        for edge in phenotype.get("required_edges", []) or []:
            if not isinstance(edge, dict):
                continue
            from_signal = str(edge.get("from_signal_id", "")).strip()
            to_signal = str(edge.get("to_signal_id", "")).strip()
            if not from_signal or not to_signal:
                continue
            key = (from_signal, to_signal)
            allowed.add(key)
            basis = edge.get("evidence_basis") or {}
            basis_type = str((basis or {}).get("type", "")).strip()
            basis_ref = str((basis or {}).get("ref", "")).strip()
            if bool(edge.get("requires_research_promotion")) and basis_type == "rationale_md":
                rationale_by_edge.setdefault(key, []).append((phenotype_id, basis_ref))

    return allowed, rationale_by_edge


def validate_interaction_map_v1(
    interaction_map_path: Path | None = None,
    phenotype_map_path: Path | None = None,
    packages_root: Path | None = None,
) -> Tuple[bool, List[str], List[str], bool]:
    interaction_map_path = interaction_map_path or DEFAULT_INTERACTION_MAP_PATH
    phenotype_map_path = phenotype_map_path or DEFAULT_PHENOTYPE_MAP_PATH
    packages_root = packages_root or DEFAULT_PACKAGES_ROOT

    errors: List[str] = []
    warnings: List[str] = []

    if not interaction_map_path.exists():
        return False, [f"ERROR interaction_map_v1: interaction map file not found path={interaction_map_path}"], warnings, False
    if not phenotype_map_path.exists():
        return False, [f"ERROR interaction_map_v1: phenotype map file not found path={phenotype_map_path}"], warnings, False

    try:
        interaction_payload = _load_yaml(interaction_map_path)
    except Exception as exc:
        return False, [f"ERROR interaction_map_v1: failed to parse interaction map: {exc}"], warnings, False
    try:
        phenotype_payload = _load_yaml(phenotype_map_path)
    except Exception as exc:
        return False, [f"ERROR interaction_map_v1: failed to parse phenotype map: {exc}"], warnings, False

    known_signal_ids = _collect_known_signal_ids(packages_root)
    allowed_edges, rationale_by_edge = _build_allowed_edges(phenotype_payload)

    if not allowed_edges:
        return False, [STOP_EMPTY_ALLOWED], warnings, True

    interaction_edges = interaction_payload.get("edges", []) or []
    edge_signal_set: Set[str] = set()

    for edge in interaction_edges:
        if not isinstance(edge, dict):
            continue
        from_signal, to_signal = _get_edge_signals(edge)
        edge_repr = f"{from_signal}->{to_signal}"
        if from_signal:
            edge_signal_set.add(from_signal)
        if to_signal:
            edge_signal_set.add(to_signal)

        if from_signal not in known_signal_ids:
            errors.append(
                f"ERROR interaction_map_v1: orphaned_edge signal_id={from_signal} edge={edge_repr}"
            )
        if to_signal not in known_signal_ids:
            errors.append(
                f"ERROR interaction_map_v1: orphaned_edge signal_id={to_signal} edge={edge_repr}"
            )
        if from_signal and to_signal and (from_signal, to_signal) not in allowed_edges:
            warnings.append(
                f"WARN interaction_map_v1: edge_not_covered_by_any_phenotype edge={edge_repr}"
            )
        for phenotype_id, ref in rationale_by_edge.get((from_signal, to_signal), []):
            warnings.append(
                "WARN interaction_map_v1: edge_requires_research_promotion "
                f"edge={edge_repr} phenotype_id={phenotype_id} ref={ref}"
            )

    nodes = interaction_payload.get("nodes")
    if isinstance(nodes, list):
        node_signal_ids: Set[str] = set()
        for node in nodes:
            if not isinstance(node, dict):
                continue
            signal_id = str(node.get("signal_id", "")).strip()
            if signal_id:
                node_signal_ids.add(signal_id)
        for signal_id in sorted(edge_signal_set):
            if signal_id not in node_signal_ids:
                warnings.append(
                    "WARN interaction_map_v1: nodes_list_omits_edge_signal "
                    f"signal_id={signal_id}"
                )

    return len(errors) == 0, errors, warnings, False


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate interaction map v1 governance constraints.")
    parser.add_argument("--interaction-map", default=str(DEFAULT_INTERACTION_MAP_PATH))
    parser.add_argument("--phenotype-map", default=str(DEFAULT_PHENOTYPE_MAP_PATH))
    parser.add_argument("--packages-root", default=str(DEFAULT_PACKAGES_ROOT))
    return parser.parse_args(argv)


def _resolve_path(path_value: str, default_path: Path) -> Path:
    candidate = Path(path_value)
    return candidate if candidate.is_absolute() else (ROOT / candidate if path_value else default_path)


def main(argv: List[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    interaction_map_path = _resolve_path(str(args.interaction_map), DEFAULT_INTERACTION_MAP_PATH)
    phenotype_map_path = _resolve_path(str(args.phenotype_map), DEFAULT_PHENOTYPE_MAP_PATH)
    packages_root = _resolve_path(str(args.packages_root), DEFAULT_PACKAGES_ROOT)

    is_valid, errors, warnings, _ = validate_interaction_map_v1(
        interaction_map_path=interaction_map_path,
        phenotype_map_path=phenotype_map_path,
        packages_root=packages_root,
    )
    for warning in warnings:
        print(warning)
    if not is_valid:
        for error in errors:
            print(error)
        return 1
    print("interaction_map_v1: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
