"""
Deterministic Signal Interaction Builder (KB-S28).

Applies an explicit interaction map to fired signal results.
No runtime inference is allowed beyond declared edges.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import yaml


_VALID_SIGNAL_STATES = {"suboptimal", "at_risk"}
_VALID_RELATIONSHIP_TYPES = {"driver", "consequence", "co_occurrence", "bidirectional"}
_VALID_EVIDENCE_STRENGTH = {"exploratory", "moderate", "strong", "consensus"}
_EVIDENCE_RANK = {
    "exploratory": 1,
    "moderate": 2,
    "strong": 3,
    "consensus": 4,
}
_MAX_CHAIN_LENGTH = 5


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _default_map_path() -> Path:
    return _repo_root() / "knowledge_bus" / "interaction_maps" / "interaction_map_v1.yaml"


def load_interaction_map_v1(map_path: Optional[str] = None) -> Dict[str, Any]:
    path = Path(map_path) if map_path else _default_map_path()
    if not path.exists():
        raise FileNotFoundError(f"Interaction map not found: {path}")

    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if payload.get("map_version") != "v1":
        raise ValueError("interaction_map_v1.yaml must declare map_version: 'v1'")

    nodes = payload.get("nodes")
    edges = payload.get("edges")
    if not isinstance(nodes, list) or not isinstance(edges, list):
        raise ValueError("interaction map must contain list fields: nodes and edges")

    node_ids: Set[str] = set()
    for node in nodes:
        if not isinstance(node, dict):
            raise ValueError("interaction map nodes must be objects")
        signal_id = node.get("signal_id")
        if not isinstance(signal_id, str) or not signal_id:
            raise ValueError("each interaction map node requires non-empty signal_id")
        node_ids.add(signal_id)

    for edge in edges:
        if not isinstance(edge, dict):
            raise ValueError("interaction map edges must be objects")
        from_signal = edge.get("from_signal")
        to_signal = edge.get("to_signal")
        relationship_type = edge.get("relationship_type")
        evidence_strength = edge.get("evidence_strength")
        rationale = edge.get("rationale")
        if not isinstance(from_signal, str) or not isinstance(to_signal, str):
            raise ValueError("each interaction map edge requires from_signal and to_signal")
        if from_signal not in node_ids or to_signal not in node_ids:
            raise ValueError("all edge endpoints must be declared in nodes")
        if relationship_type not in _VALID_RELATIONSHIP_TYPES:
            raise ValueError(f"invalid relationship_type: {relationship_type}")
        if evidence_strength not in _VALID_EVIDENCE_STRENGTH:
            raise ValueError(f"invalid evidence_strength: {evidence_strength}")
        if not isinstance(rationale, str) or len(rationale.strip()) < 20:
            raise ValueError("each interaction edge rationale must be at least 20 chars")

    return payload


def _enumerate_simple_paths(
    adjacency: Dict[str, List[str]],
    max_nodes: int,
) -> List[Tuple[str, ...]]:
    results: Set[Tuple[str, ...]] = set()

    def dfs(path: List[str], visited: Set[str]) -> None:
        current = path[-1]
        neighbors = adjacency.get(current, [])
        advanced = False
        for nxt in neighbors:
            if nxt in visited:
                continue
            if len(path) >= max_nodes:
                continue
            advanced = True
            path.append(nxt)
            visited.add(nxt)
            dfs(path, visited)
            visited.remove(nxt)
            path.pop()
        if not advanced and len(path) >= 2:
            results.add(tuple(path))

    for start in sorted(adjacency.keys()):
        dfs([start], {start})

    return sorted(results)


def _chain_evidence_score(path: Tuple[str, ...], edge_lookup: Dict[Tuple[str, str], Dict[str, Any]]) -> int:
    score = 0
    for idx in range(len(path) - 1):
        edge = edge_lookup[(path[idx], path[idx + 1])]
        score += _EVIDENCE_RANK[edge["evidence_strength"]]
    return score


def _is_contiguous_subpath(candidate: Tuple[str, ...], container: Tuple[str, ...]) -> bool:
    if len(candidate) >= len(container):
        return False
    for start in range(0, len(container) - len(candidate) + 1):
        if container[start : start + len(candidate)] == candidate:
            return True
    return False


def build_signal_interactions_v1(
    signal_results: Optional[List[Dict[str, Any]]],
    map_payload: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    payload = map_payload or load_interaction_map_v1()
    nodes = payload.get("nodes", [])
    edges = payload.get("edges", [])

    node_ids = {n["signal_id"] for n in nodes if isinstance(n, dict) and isinstance(n.get("signal_id"), str)}
    signal_results = signal_results or []
    fired = {
        r.get("signal_id"): r.get("signal_state")
        for r in signal_results
        if isinstance(r, dict)
        and isinstance(r.get("signal_id"), str)
        and r.get("signal_state") in _VALID_SIGNAL_STATES
    }
    confidence_by_signal: Dict[str, float] = {}
    for row in signal_results:
        if not isinstance(row, dict):
            continue
        sid = row.get("signal_id")
        if not isinstance(sid, str):
            continue
        confidence_value = row.get("confidence")
        if isinstance(confidence_value, (int, float)):
            confidence_by_signal[sid] = float(confidence_value)
        else:
            confidence_by_signal[sid] = 0.0
    present_ids = sorted(sid for sid in fired.keys() if sid in node_ids)

    present_set = set(present_ids)
    active_edges: List[Dict[str, Any]] = []
    for edge in edges:
        if not isinstance(edge, dict):
            continue
        src = edge.get("from_signal")
        dst = edge.get("to_signal")
        if src in present_set and dst in present_set:
            active_edges.append(
                {
                    "from_signal": src,
                    "to_signal": dst,
                    "relationship_type": edge.get("relationship_type"),
                    "evidence_strength": edge.get("evidence_strength"),
                    "rationale": edge.get("rationale"),
                }
            )

    active_edges.sort(
        key=lambda e: (
            str(e.get("from_signal", "")),
            str(e.get("to_signal", "")),
            str(e.get("relationship_type", "")),
            str(e.get("evidence_strength", "")),
        )
    )

    adjacency: Dict[str, List[str]] = {sid: [] for sid in present_ids}
    edge_lookup: Dict[Tuple[str, str], Dict[str, Any]] = {}
    for edge in active_edges:
        src = edge["from_signal"]
        dst = edge["to_signal"]
        adjacency[src].append(dst)
        edge_lookup[(src, dst)] = edge
    for src in adjacency.keys():
        adjacency[src] = sorted(adjacency[src])

    raw_paths = _enumerate_simple_paths(adjacency=adjacency, max_nodes=_MAX_CHAIN_LENGTH)
    maximal_paths = [
        path
        for path in raw_paths
        if not any(_is_contiguous_subpath(path, other) for other in raw_paths if other != path)
    ]
    ranked_paths = sorted(
        maximal_paths,
        key=lambda path: (
            0 if any(fired[sid] == "at_risk" for sid in path) else 1,
            -len(path),
            -_chain_evidence_score(path, edge_lookup),
            path,
        ),
    )

    interaction_chains = [list(path) for path in ranked_paths]
    interaction_summary = []
    for idx, path in enumerate(ranked_paths, start=1):
        chain_edges = [edge_lookup[(path[i], path[i + 1])] for i in range(len(path) - 1)]
        chain_text = " -> ".join(path)
        evidence_text = ", ".join(edge["evidence_strength"] for edge in chain_edges)
        chain_confidence = min(confidence_by_signal.get(signal_id, 0.0) for signal_id in path)
        interaction_summary.append(
            {
                "chain_id": f"chain_{idx:03d}",
                "priority_rank": idx,
                "signals_involved": list(path),
                "chain_summary_text": f"{chain_text} (edge evidence: {evidence_text})",
                "confidence": round(chain_confidence, 4),
            }
        )

    return {
        "interaction_graph": {
            "map_version": payload.get("map_version", "v1"),
            "nodes": present_ids,
            "edges": active_edges,
        },
        "interaction_chains": interaction_chains,
        "interaction_summary": interaction_summary,
    }
