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


class AuthorityModelLoadError(RuntimeError):
    """Raised when the signal authority collision model cannot be loaded or validated."""


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


def _normalize_override_boundary(raw: Any) -> str:
    if not isinstance(raw, str):
        return ""
    token = raw.strip().lower().replace("-", "_")
    if token in {"lower", "below_min"}:
        return "lower"
    if token in {"upper", "above_max"}:
        return "upper"
    if token == "out_of_range":
        return "out_of_range"
    if token in {"not_above_max", "at_or_below_max"}:
        return "not_above_max"
    if token in {"not_below_min", "at_or_above_min"}:
        return "not_below_min"
    return ""


def _evaluate_lab_range_boundary_condition(
    boundary_mode: str,
    observed: float,
    lab_ranges: Mapping[str, dict],
    metric_id: str,
) -> bool:
    ref = lab_ranges.get(metric_id)
    if not isinstance(ref, dict):
        return False
    low = _as_float(ref.get("min"))
    high = _as_float(ref.get("max"))
    if boundary_mode == "lower":
        if low is None:
            return False
        return observed < low
    if boundary_mode == "upper":
        if high is None:
            return False
        return observed > high
    if boundary_mode == "out_of_range":
        below = low is not None and observed < low
        above = high is not None and observed > high
        return below or above
    if boundary_mode == "not_above_max":
        if high is None:
            return False
        return observed <= high
    if boundary_mode == "not_below_min":
        if low is None:
            return False
        return observed >= low
    return False


def _evaluate_override_condition(
    condition: Dict[str, Any],
    signal_biomarkers: Mapping[str, float],
    signal_derived: Mapping[str, float],
    lab_ranges: Mapping[str, dict],
) -> bool:
    metric_id = str(condition.get("metric_id", "")).strip()
    if not metric_id:
        return False

    comp_raw = condition.get("comparator_type")
    comp = str(comp_raw).strip() if comp_raw is not None else ""

    if comp == "lab_range_boundary":
        boundary_mode = _normalize_override_boundary(condition.get("boundary"))
        if not boundary_mode:
            return False
        observed = _resolve_metric_value(metric_id, signal_biomarkers, signal_derived)
        if observed is None:
            return False
        return _evaluate_lab_range_boundary_condition(
            boundary_mode=boundary_mode,
            observed=observed,
            lab_ranges=lab_ranges,
            metric_id=metric_id,
        )

    operator = str(condition.get("operator", "")).strip()
    compare_value = _as_float(condition.get("value"))
    if comp not in ("", "numeric_value"):
        return False
    if operator not in {"<", "<=", ">", ">=", "=="} or compare_value is None:
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
    return observed == compare_value


def _override_rule_fires(
    rule: Dict[str, Any],
    signal_biomarkers: Mapping[str, float],
    signal_derived: Mapping[str, float],
    lab_ranges: Mapping[str, dict],
) -> bool:
    conditions = rule.get("conditions")
    if not isinstance(conditions, list) or not conditions:
        return False
    any_of_results: List[bool] = []
    all_of_results: List[bool] = []
    for condition in conditions:
        if not isinstance(condition, dict):
            return False
        condition_type = str(condition.get("condition_type", "")).strip()
        if condition_type not in {"any_of", "all_of"}:
            return False
        condition_result = _evaluate_override_condition(
            condition=condition,
            signal_biomarkers=signal_biomarkers,
            signal_derived=signal_derived,
            lab_ranges=lab_ranges,
        )
        if condition_type == "any_of":
            any_of_results.append(condition_result)
        else:
            all_of_results.append(condition_result)
    all_of_ok = all(all_of_results) if all_of_results else True
    any_of_ok = any(any_of_results) if any_of_results else True
    return all_of_ok and any_of_ok


def _load_governed_override_rule(
    source_package_path: str,
    override_rule_id: str,
) -> Dict[str, Any]:
    path = _repo_root() / source_package_path.replace("\\", "/") / "signal_library.yaml"
    if not path.is_file():
        raise AuthorityModelLoadError(
            f"Governed override source package not found: {source_package_path}"
        )
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    signals = payload.get("signals")
    if not isinstance(signals, list):
        raise AuthorityModelLoadError(
            f"Invalid signal library for governed override source: {source_package_path}"
        )
    for signal in signals:
        if not isinstance(signal, dict):
            continue
        override_rules = signal.get("override_rules")
        if not isinstance(override_rules, list):
            continue
        for rule in override_rules:
            if not isinstance(rule, dict):
                continue
            if str(rule.get("rule_id", "")).strip() == override_rule_id:
                return rule
    raise AuthorityModelLoadError(
        f"Governed override rule {override_rule_id!r} not found in {source_package_path}"
    )


def load_signal_authority_collision_model(
    model_path: Optional[Path] = None,
) -> Dict[str, Any]:
    path = model_path or DEFAULT_MODEL_PATH
    if not path.is_file():
        raise AuthorityModelLoadError(f"Signal authority collision model not found: {path}")
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        raise AuthorityModelLoadError(
            f"Signal authority collision model is malformed YAML: {path}"
        ) from exc
    if not isinstance(payload, dict):
        raise AuthorityModelLoadError(
            f"Invalid signal authority collision model payload: {path}"
        )
    return payload


def validate_signal_authority_collision_model(
    model: Dict[str, Any],
    *,
    model_path: Path,
) -> None:
    if model.get("runtime_consumed") is not True:
        raise AuthorityModelLoadError(
            f"Signal authority collision model must set runtime_consumed: true ({model_path})"
        )
    groups = model.get("authority_groups")
    if not isinstance(groups, list) or not groups:
        raise AuthorityModelLoadError(
            f"Signal authority collision model missing authority_groups ({model_path})"
        )

    enforceable = _iter_enforceable_groups(model)
    if not enforceable:
        raise AuthorityModelLoadError(
            f"Signal authority collision model has no enforceable authority groups ({model_path})"
        )

    renal = next(
        (group for group in enforceable if group.get("authority_group_id") == "renal_filtration_axis"),
        None,
    )
    if renal is None:
        raise AuthorityModelLoadError(
            f"renal_filtration_axis enforceable group missing ({model_path})"
        )

    layers = renal.get("distinct_risk_layers")
    if not isinstance(layers, list) or not layers:
        raise AuthorityModelLoadError(
            f"renal_filtration_axis missing distinct_risk_layers ({model_path})"
        )
    electrolyte_layer = next(
        (
            layer
            for layer in layers
            if isinstance(layer, dict)
            and layer.get("layer_id") == "hyperkalemia_or_electrolyte_complication"
        ),
        None,
    )
    if electrolyte_layer is None:
        raise AuthorityModelLoadError(
            f"hyperkalemia_or_electrolyte_complication layer missing ({model_path})"
        )
    preserve_when = electrolyte_layer.get("preserve_when")
    if not isinstance(preserve_when, dict):
        raise AuthorityModelLoadError(
            f"distinct risk layer missing preserve_when ({model_path})"
        )
    mechanism = str(preserve_when.get("mechanism", "")).strip()
    if mechanism != "governed_override_rule":
        raise AuthorityModelLoadError(
            f"distinct risk layer preserve_when mechanism must be governed_override_rule ({model_path})"
        )
    source_package_path = str(preserve_when.get("source_package_path", "")).strip()
    override_rule_id = str(preserve_when.get("override_rule_id", "")).strip()
    if not source_package_path or not override_rule_id:
        raise AuthorityModelLoadError(
            f"governed_override_rule preserve_when missing source_package_path or override_rule_id ({model_path})"
        )
    _load_governed_override_rule(source_package_path, override_rule_id)


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
    lab_ranges: Mapping[str, dict],
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
        preserve_when = layer.get("preserve_when")
        if not isinstance(preserve_when, dict):
            continue
        mechanism = str(preserve_when.get("mechanism", "")).strip()
        if mechanism != "governed_override_rule":
            continue
        source_package_id = str(preserve_when.get("source_package_id", "")).strip()
        if source_package_id and source_package_id != result.package_id:
            continue
        source_package_path = str(preserve_when.get("source_package_path", "")).strip()
        override_rule_id = str(preserve_when.get("override_rule_id", "")).strip()
        if not source_package_path or not override_rule_id:
            continue
        rule = _load_governed_override_rule(source_package_path, override_rule_id)
        if _override_rule_fires(
            rule,
            signal_biomarkers=signal_biomarkers,
            signal_derived=signal_derived,
            lab_ranges=lab_ranges,
        ):
            return True
    return False


def apply_signal_authority_collision_policy(
    results: List[SignalResult],
    *,
    signal_biomarkers: Mapping[str, float],
    signal_derived: Mapping[str, float],
    lab_ranges: Optional[Mapping[str, dict]] = None,
    model_path: Optional[Path] = None,
) -> List[SignalResult]:
    """
    Apply governed authority/collision policy to assembled signal results.

    Missing or invalid authority model raises AuthorityModelLoadError — silent pass-through
    is forbidden when authority-controlled overlap could occur.
    """
    path = model_path or DEFAULT_MODEL_PATH
    model = load_signal_authority_collision_model(model_path=path)
    validate_signal_authority_collision_model(model, model_path=path)

    lab_ranges = lab_ranges or {}
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
            if _distinct_risk_layer_active(
                group,
                row,
                signal_biomarkers,
                signal_derived,
                lab_ranges,
            ):
                kept.append(row)
                continue
            continue
        filtered = kept

    filtered.sort(key=lambda r: (r.signal_id, r.activation_key))
    return filtered
