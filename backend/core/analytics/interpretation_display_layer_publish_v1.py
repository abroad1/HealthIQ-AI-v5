"""
BE-IDL-1 — Deterministic IDL publisher (read-only InsightGraph + static registry).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import yaml

from core.analytics.consumer_prose_safety_v1 import sanitize_retail_display_label
from core.contracts.interpretation_display_layer_v1 import (
    InterpretationDisplayLayerBundleV1,
    InterpretationDisplayRecordV1,
    SeverityStateV1,
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _humanize_metric(metric_id: str) -> str:
    s = str(metric_id or "").strip().replace("_", " ")
    if not s:
        return "marker"
    return s.title()


def _load_yaml(path: Path) -> Dict[str, Any]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    return raw if isinstance(raw, dict) else {}


def load_idl_registry_document() -> Tuple[str, List[Dict[str, Any]]]:
    """Return (schema_version, static record dicts) from governed IDL YAML."""
    path = _repo_root() / "knowledge_bus" / "interpretation_display_layer_v1" / "idl_records_v1.yaml"
    payload = _load_yaml(path)
    schema_ver = str(payload.get("schema_version") or "1.0.0").strip() or "1.0.0"
    rows = payload.get("records")
    if not isinstance(rows, list):
        return schema_ver, []
    out: List[Dict[str, Any]] = []
    for row in rows:
        if isinstance(row, dict):
            out.append(dict(row))
    return schema_ver, out


def load_idl_static_record_dicts() -> List[Dict[str, Any]]:
    _, rows = load_idl_registry_document()
    return rows


def load_phenotype_required_signals_by_id() -> Dict[str, List[str]]:
    path = _repo_root() / "knowledge_bus" / "phenotypes" / "phenotype_map_v1.yaml"
    payload = _load_yaml(path)
    phenotypes = payload.get("phenotypes")
    if not isinstance(phenotypes, list):
        return {}
    out: Dict[str, List[str]] = {}
    for p in phenotypes:
        if not isinstance(p, dict):
            continue
        pid = str(p.get("phenotype_id", "")).strip()
        req = p.get("required_signals") or []
        if not pid or not isinstance(req, list):
            continue
        signals = [str(s).strip() for s in req if str(s).strip()]
        out[pid] = signals
    return out


def _signal_fire_states(insight_graph: Dict[str, Any]) -> Tuple[Set[str], Dict[str, str]]:
    """Returns (fired_signal_ids, signal_id -> signal_state) for suboptimal/at_risk only."""
    fired: Set[str] = set()
    states: Dict[str, str] = {}
    for row in insight_graph.get("signal_results") or []:
        if not isinstance(row, dict):
            continue
        sid = str(row.get("signal_id", "")).strip()
        st = str(row.get("signal_state", "")).strip()
        if not sid:
            continue
        states[sid] = st
        if st in {"suboptimal", "at_risk"}:
            fired.add(sid)
    return fired, states


def _derive_severity_state(
    required: List[str],
    fired: Set[str],
    states: Dict[str, str],
) -> SeverityStateV1:
    req = [s for s in required if s]
    if not req:
        return "not_observed"
    present = [s for s in req if s in fired]
    if not present:
        return "not_observed"
    if len(present) < len(req):
        return "watch"
    any_at_risk = any(states.get(s) == "at_risk" for s in req)
    if any_at_risk:
        return "strong_signal"
    return "attention"


def _supporting_summary_for_phenotype(
    required: List[str],
    fired: Set[str],
    signal_rows: List[Dict[str, Any]],
) -> str:
    """2–4 marker names from fired required signals' primary_metric, deterministic order."""
    metrics: List[str] = []
    by_id = {
        str(r.get("signal_id", "")).strip(): r
        for r in signal_rows
        if isinstance(r, dict) and str(r.get("signal_id", "")).strip()
    }
    for sid in sorted(s for s in required if s in fired):
        row = by_id.get(sid)
        if not isinstance(row, dict):
            continue
        pm = str(row.get("primary_metric", "")).strip()
        if pm:
            h = _humanize_metric(pm)
            if h not in metrics:
                metrics.append(h)
        for sup in row.get("supporting_markers") or []:
            if isinstance(sup, str) and sup.strip():
                h2 = _humanize_metric(sup.strip())
                if h2 not in metrics:
                    metrics.append(h2)
        if len(metrics) >= 4:
            break
    if not metrics:
        return "Key pattern signals for this interpretation."
    return ", ".join(metrics[:4])


def publish_interpretation_display_layer_v1(
    insight_graph: Optional[Dict[str, Any]],
) -> InterpretationDisplayLayerBundleV1:
    """
    Build the IDL bundle for this analysis. Read-only over insight_graph.

    When insight_graph is empty/None, severity defaults to not_observed and summaries are generic.
    """
    ig: Dict[str, Any] = insight_graph if isinstance(insight_graph, dict) else {}
    schema_ver, static_rows = load_idl_registry_document()
    required_by_id = load_phenotype_required_signals_by_id()
    fired, states = _signal_fire_states(ig)
    signal_rows = [r for r in (ig.get("signal_results") or []) if isinstance(r, dict)]

    out_records: List[InterpretationDisplayRecordV1] = []
    for row in sorted(static_rows, key=lambda r: int(r.get("display_order_priority", 999))):
        internal_id = str(row.get("internal_id", "")).strip()
        if not internal_id:
            continue
        required = required_by_id.get(internal_id, [])
        sev = _derive_severity_state(required, fired, states)
        summary = _supporting_summary_for_phenotype(required, fired, signal_rows)
        static_enabled = bool(row.get("enabled_for_frontend", True))
        enabled = static_enabled and sev != "not_observed"

        rec = InterpretationDisplayRecordV1(
            internal_id=internal_id,
            scientific_class=row["scientific_class"],
            clinical_display_label=str(row.get("clinical_display_label", "")),
            retail_display_label=sanitize_retail_display_label(
                str(row.get("retail_display_label", ""))
            ),
            subtitle=str(row.get("subtitle", "")),
            why_it_matters=str(row.get("why_it_matters", "")),
            severity_state=sev,
            supporting_biomarkers_summary=summary,
            frontend_allowed_term=row["frontend_allowed_term"],
            display_order_priority=int(row.get("display_order_priority", 1)),
            enabled_for_frontend=enabled,
            supporting_systems_summary=(
                str(row["supporting_systems_summary"])
                if row.get("supporting_systems_summary") is not None
                else None
            ),
            user_safe_description=(
                str(row["user_safe_description"])
                if row.get("user_safe_description") is not None
                else None
            ),
            future_commercial_domain=(
                str(row["future_commercial_domain"])
                if row.get("future_commercial_domain") is not None
                else None
            ),
            display_caveat=(
                str(row["display_caveat"]) if row.get("display_caveat") is not None else None
            ),
        )
        out_records.append(rec)

    return InterpretationDisplayLayerBundleV1(schema_version=schema_ver, records=out_records)
