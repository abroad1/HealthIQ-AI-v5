"""
Reusable signal authority / collision enforcement from governance model.

Post-processes SignalResult lists after evaluate_all() — does not modify per-signal evaluation.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence

import yaml

from core.models.signal import SignalResult

DEFAULT_MODEL_PATH = (
    Path(__file__).resolve().parents[3]
    / "knowledge_bus"
    / "governance"
    / "signal_authority_collision_model_v1.yaml"
)

ADJUDICATED_RUNTIME_STATUSES = frozenset(
    {
        "adjudicated_governance_only",
        "adjudicated_runtime_enforced",
    }
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _as_float(value: Any) -> Optional[float]:
    if isinstance(value, (int, float)):
        return float(value)
    return None


def _resolve_metric_value(
    metric_id: str,
    signal_biomarkers: Mapping[str, float],
    signal_derived: Mapping[str, float],
) -> Optional[float]:
    if metric_id in signal_biomarkers:
        return _as_float(signal_biomarkers[metric_id])
    if metric_id in signal_derived:
        return _as_float(signal_derived[metric_id])
    return None


def _evaluate_numeric_condition(
    condition: Dict[str, Any],
    signal_biomarkers: Mapping[str, float],
    signal_derived: Mapping[str, float],
) -> bool:
    metric_id = str(condition.get("metric_id", "")).strip()
    operator = str(condition.get("operator", "")).strip()
    compare_value = _as_float(condition.get("value"))
    if not metric_id or compare_value is None:
        return False
    observed = _resolve_metric_value(metric_id, signal_biomarkers, signal_derived)
    if observed is None:
        return False
    if operator == "<":
        return observed < compare_value
    if operator == "<=":
        return observed <= compare_value
    if operator == ">":
        return observed > compare_value
    if operator == ">=":
        return observed >= compare_value
    if operator == "==":
        return observed == compare_value
    return False


def _evaluate_preserve_conditions(
    conditions: Sequence[Dict[str, Any]],
    signal_biomarkers: Mapping[str, float],
    signal_derived: Mapping[str, float],
) -> bool:
    if not conditions:
        return False
    for condition in conditions:
        if not isinstance(condition, dict):
            return False
        condition_type = str(condition.get("condition_type", "all_of")).strip()
        if condition_type != "all_of":
            return False
        if not _evaluate_numeric_condition(condition, signal_biomarkers, signal_derived):
            return False
    return True


def load_signal_authority_collision_model(
    model_path: Optional[Path] = None,
) -> Dict[str, Any]:
    path = model_path or DEFAULT_MODEL_PATH
    if not path.is_file():
        raise FileNotFoundError(f"Signal authority collision model not found: {path}")
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(payload, dict):
        raise ValueError(f"Invalid signal authority collision model payload: {path}")
    return payload


def _iter_enforceable_groups(model: Dict[str, Any]) -> List[Dict[str, Any]]:
    groups = model.get("authority_groups")
    if not isinstance(groups, list):
        return []
    enforceable: List[Dict[str, Any]] = []
    for group in groups:
        if not isinstance(group, dict):
            continue
        status = str(group.get("status", "")).strip()
        if status not in ADJUDICATED_RUNTIME_STATUSES:
            continue
        if not bool(group.get("requires_runtime_support", False)):
            continue
        policy = group.get("collision_policy")
        if not isinstance(policy, dict):
            continue
        if not bool(policy.get("suppress_supporting_when_primary_present", False)):
            continue
        primary = str(group.get("primary_signal_family", "")).strip()
        supporting = group.get("supporting_signal_families")
        if not primary or not isinstance(supporting, list):
            continue
        enforceable.append(group)
    return enforceable


def _distinct_risk_layer_active(
    group: Dict[str, Any],
    result: SignalResult,
    signal_biomarkers: Mapping[str, float],
    signal_derived: Mapping[str, float],
) -> bool:
    if not bool((group.get("collision_policy") or {}).get("allow_parallel_if_distinct_risk_layer", False)):
        return False
    layers = group.get("distinct_risk_layers")
    if not isinstance(layers, list):
        return False
    for layer in layers:
        if not isinstance(layer, dict):
            continue
        layer_family = str(layer.get("signal_family", "")).strip()
        if layer_family and layer_family != result.signal_id:
            continue
        preserve_conditions = layer.get("preserve_conditions")
        if isinstance(preserve_conditions, list) and preserve_conditions:
            if _evaluate_preserve_conditions(preserve_conditions, signal_biomarkers, signal_derived):
                return True
            continue
        # Backward-compatible metadata-only layers without runtime conditions are not preserved.
    return False


def apply_signal_authority_collision_policy(
    results: List[SignalResult],
    *,
    signal_biomarkers: Mapping[str, float],
    signal_derived: Mapping[str, float],
    model_path: Optional[Path] = None,
) -> List[SignalResult]:
    """
    Apply governed authority/collision policy to assembled signal results.

    Fail-safe: if the model file is missing, return results unchanged.
    """
    try:
        model = load_signal_authority_collision_model(model_path)
    except FileNotFoundError:
        return results

    filtered = list(results)
    for group in _iter_enforceable_groups(model):
        primary_family = str(group.get("primary_signal_family", "")).strip()
        supporting_families = {
            str(item).strip()
            for item in (group.get("supporting_signal_families") or [])
            if str(item).strip()
        }
        if not supporting_families:
            continue

        primary_present = any(row.signal_id == primary_family for row in filtered)
        if not primary_present:
            continue

        kept: List[SignalResult] = []
        for row in filtered:
            if row.signal_id not in supporting_families:
                kept.append(row)
                continue
            if _distinct_risk_layer_active(group, row, signal_biomarkers, signal_derived):
                kept.append(row)
                continue
            # Supporting family suppressed when primary authority is present.
            continue
        filtered = kept

    filtered.sort(key=lambda r: (r.signal_id, r.activation_key))
    return filtered
