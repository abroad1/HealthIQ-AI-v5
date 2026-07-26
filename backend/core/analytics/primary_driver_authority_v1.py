"""
ARCH-CONV-CORRECT-1 — Layer B primary-driver authority projection.

Layer C previously arbitrated its own "primary driver" from cluster severity, score and
label-similarity heuristics. That is a medical ranking decision and belongs in Layer B,
which already ranks findings under a governed ranking policy.

This module adds no new medical reasoning. It projects the existing governed decision
(``report_v1.top_findings[0]``, produced by the governed ranking policy) onto the cluster
identity Layer C needs to render, using deterministic identity matching only. When the
governed lead cannot be resolved, it returns ``None`` so Layer C suppresses the section
rather than inventing a fallback.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence

PRIMARY_DRIVER_SCHEMA = "primary_driver_authority_v1"


def _norm(value: Any) -> str:
    return str(value or "").strip().lower()


def _cluster_identity(cluster: Dict[str, Any], index: int) -> str:
    for key in ("cluster_id", "id"):
        value = str(cluster.get(key) or "").strip()
        if value:
            return value
    return f"cluster-{index}"


def _cluster_system_tokens(cluster: Dict[str, Any]) -> List[str]:
    tokens: List[str] = []
    for key in ("system", "system_id", "category", "domain_id", "health_system"):
        token = _norm(cluster.get(key))
        if token:
            tokens.append(token)
    return tokens


def _cluster_biomarkers(cluster: Dict[str, Any]) -> List[str]:
    for key in ("biomarkers", "biomarkers_involved"):
        values = cluster.get(key)
        if isinstance(values, list):
            out = [str(x).strip() for x in values if str(x).strip()]
            if out:
                return out
    return []


def _resolve_cluster_for_lead(
    *,
    clusters: Sequence[Dict[str, Any]],
    lead_system: str,
    lead_primary_metric: str,
) -> Optional[Dict[str, Any]]:
    """Deterministic identity match: governed lead system first, then its primary metric."""
    system = _norm(lead_system)
    metric = _norm(lead_primary_metric)

    if system:
        for index, cluster in enumerate(clusters):
            if system in _cluster_system_tokens(cluster):
                return {"index": index, "cluster": cluster}
    if metric:
        for index, cluster in enumerate(clusters):
            if metric in {_norm(b) for b in _cluster_biomarkers(cluster)}:
                return {"index": index, "cluster": cluster}
    return None


def build_primary_driver_authority_v1(
    *,
    report_v1: Any,
    clustering_result: Optional[Dict[str, Any]],
    signal_results: Optional[Sequence[Dict[str, Any]]] = None,
    wave1_biomarker_keys: Optional[Sequence[str]] = None,
) -> Optional[Dict[str, Any]]:
    """
    Project the governed ranked lead onto the cluster Layer C renders.

    Returns ``None`` when no governed lead exists, so Layer C fails safely.
    """
    top_findings = _top_findings(report_v1)
    if not top_findings:
        return None
    lead = top_findings[0]
    lead_signal_id = str(lead.get("signal_id") or "").strip()
    if not lead_signal_id:
        return None

    lead_system = _system_for_signal(lead_signal_id, signal_results)
    lead_primary_metric = str(lead.get("primary_metric") or "").strip()

    clusters = _clusters(clustering_result)
    match = _resolve_cluster_for_lead(
        clusters=clusters,
        lead_system=lead_system,
        lead_primary_metric=lead_primary_metric,
    )

    biomarker_keys = [str(x).strip() for x in (wave1_biomarker_keys or []) if str(x).strip()]
    cluster_id = ""
    cluster_name = ""
    if match is not None:
        cluster = match["cluster"]
        cluster_id = _cluster_identity(cluster, int(match["index"]))
        cluster_name = str(cluster.get("name") or "").strip()
        if not biomarker_keys:
            biomarker_keys = _cluster_biomarkers(cluster)

    return {
        "schema": PRIMARY_DRIVER_SCHEMA,
        "authority_source": "report_v1.top_findings",
        "ranking_policy_version": _ranking_policy_version(report_v1),
        "priority_rank": _safe_int(lead.get("priority_rank"), 1),
        "signal_id": lead_signal_id,
        "activation_key": str(lead.get("activation_key") or "").strip(),
        "source_spec_id": str(lead.get("source_spec_id") or "").strip(),
        "primary_metric": lead_primary_metric,
        "system": lead_system,
        "cluster_id": cluster_id,
        "cluster_name": cluster_name,
        "cluster_resolved": match is not None,
        "biomarker_keys": biomarker_keys[:8],
    }


def _top_findings(report_v1: Any) -> List[Dict[str, Any]]:
    rows = _attr_or_key(report_v1, "top_findings")
    if not isinstance(rows, list):
        return []
    out: List[Dict[str, Any]] = []
    for row in rows:
        if isinstance(row, dict):
            out.append(row)
        elif hasattr(row, "model_dump"):
            out.append(row.model_dump())
    return out


def _ranking_policy_version(report_v1: Any) -> str:
    meta = _attr_or_key(report_v1, "meta")
    if hasattr(meta, "model_dump"):
        meta = meta.model_dump()
    if isinstance(meta, dict):
        return str(meta.get("ranking_policy_version") or "").strip()
    return ""


def _clusters(clustering_result: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if not isinstance(clustering_result, dict):
        return []
    rows = clustering_result.get("clusters")
    if not isinstance(rows, list):
        return []
    return [row for row in rows if isinstance(row, dict)]


def _system_for_signal(
    signal_id: str,
    signal_results: Optional[Sequence[Dict[str, Any]]],
) -> str:
    for row in signal_results or []:
        if not isinstance(row, dict):
            continue
        if str(row.get("signal_id") or "").strip() == signal_id:
            system = str(row.get("system") or "").strip()
            if system:
                return system
    return ""


def _attr_or_key(source: Any, name: str) -> Any:
    if isinstance(source, dict):
        return source.get(name)
    return getattr(source, name, None)


def _safe_int(value: Any, default: int) -> int:
    if isinstance(value, bool):
        return default
    if isinstance(value, int):
        return value
    return default
