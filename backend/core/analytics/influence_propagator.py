"""
Sprint 13 - Deterministic System Burden & Capacity Engine v1.

Module C: graph-aware influence damping.
"""

from __future__ import annotations

from collections import deque
from typing import Any, Dict, Mapping, Sequence, Tuple

INFLUENCE_PROPAGATOR_VERSION = "1.0.0"


def _shortest_path_distances(
    *,
    primary_driver_system_id: str,
    causal_edges: Sequence[Mapping[str, Any]],
    systems: Sequence[str],
) -> Dict[str, float]:
    adjacency: Dict[str, set[str]] = {sid: set() for sid in systems}
    for edge in causal_edges:
        src = str(edge.get("from_system_id", "")).strip()
        dst = str(edge.get("to_system_id", "")).strip()
        if src and dst and src in adjacency and dst in adjacency:
            adjacency[src].add(dst)

    distances: Dict[str, float] = {sid: float("inf") for sid in systems}
    if primary_driver_system_id not in distances:
        raise ValueError("influence_propagator: primary driver not present in systems")
    distances[primary_driver_system_id] = 0.0

    queue: deque[str] = deque([primary_driver_system_id])
    while queue:
        node = queue.popleft()
        base = distances[node]
        for nxt in sorted(adjacency.get(node, set())):
            candidate = base + 1.0
            if candidate < distances[nxt]:
                distances[nxt] = candidate
                queue.append(nxt)
    return distances


def propagate_influence_v1(
    *,
    raw_system_burden_vector: Mapping[str, float],
    primary_driver_system_id: str,
    causal_edges: Sequence[Mapping[str, Any]],
) -> Tuple[Dict[str, float], Dict[str, float]]:
    systems = sorted(str(k) for k in raw_system_burden_vector.keys())
    if not primary_driver_system_id:
        raise ValueError("influence_propagator: missing primary_driver_system_id")
    distances = _shortest_path_distances(
        primary_driver_system_id=primary_driver_system_id,
        causal_edges=causal_edges,
        systems=systems,
    )
    adjusted: Dict[str, float] = {}
    for system_id in systems:
        raw = float(raw_system_burden_vector[system_id])
        distance = distances[system_id]
        if distance == float("inf"):
            damping = 0.0
        else:
            damping = 1.0 / (1.0 + float(distance))
        adjusted[system_id] = raw * damping
    return adjusted, distances
