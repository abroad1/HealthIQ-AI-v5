"""
Deterministic signal registry/evaluator for package signal libraries.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from core.analytics.signal_authority_collision_resolver import apply_signal_authority_collision_policy
from core.analytics.signal_confidence_builder import calculate_signal_confidence
from core.contracts.signal_contract import STATE_RANK as _STATE_RANK_IMPORT
from core.knowledge.signal_activation_identity_v1 import resolve_activation_identity
from core.models.signal import SignalResult


class SignalRegistry:
    """Load authoritative package signal libraries deterministically."""

    def __init__(self) -> None:
        self._signals_by_activation_key: Dict[str, Dict[str, Any]] = {}
        self.version: str = ""
        self.package_hash: str = ""
        self._load()

    def _packages_dir(self) -> Path:
        return Path(__file__).resolve().parents[3] / "knowledge_bus" / "packages"

    def _iter_signal_library_paths(self) -> List[Path]:
        root = self._packages_dir()
        paths = sorted(root.glob("*/signal_library.yaml"))
        return [p for p in paths if p.parent.name != "pkg_example"]

    def _load_yaml(self, path: Path) -> Dict[str, Any]:
        payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if not isinstance(payload, dict):
            raise ValueError(f"Invalid signal library payload at {path}")
        return payload

    def _load(self) -> None:
        signals_by_activation_key: Dict[str, Dict[str, Any]] = {}
        for path in self._iter_signal_library_paths():
            payload = self._load_yaml(path)
            signal_items = payload.get("signals")
            if not isinstance(signal_items, list):
                raise ValueError(f"Signal library missing 'signals' list: {path}")
            for item in signal_items:
                if not isinstance(item, dict):
                    continue
                signal_id = str(item.get("signal_id", "")).strip()
                if not signal_id:
                    continue
                activation_key, source_spec_id, package_id = resolve_activation_identity(
                    signal_id=signal_id,
                    signal_library_path=path,
                )
                if activation_key in signals_by_activation_key:
                    existing = signals_by_activation_key[activation_key].get("_source_path", "")
                    raise ValueError(
                        "Duplicate activation_key collision: "
                        f"{activation_key!r} at {path} and {existing}"
                    )
                compiled = dict(item)
                compiled["_source_path"] = str(path)
                compiled["activation_key"] = activation_key
                compiled["source_spec_id"] = source_spec_id
                compiled["package_id"] = package_id
                signals_by_activation_key[activation_key] = compiled

        ordered_keys = sorted(signals_by_activation_key.keys())
        joined = "|".join(ordered_keys)
        digest = hashlib.sha256(joined.encode("utf-8")).hexdigest()[:12]
        self.version = digest
        self.package_hash = digest
        self._signals_by_activation_key = {
            key: signals_by_activation_key[key] for key in ordered_keys
        }

    def get_all_signals(self) -> List[Dict[str, Any]]:
        return [
            dict(self._signals_by_activation_key[key])
            for key in sorted(self._signals_by_activation_key.keys())
        ]


class SignalEvaluator:
    """Evaluate repository-defined signals from raw biomarker + derived values."""

    _STATE_RANK = _STATE_RANK_IMPORT

    def __init__(self, registry: SignalRegistry) -> None:
        self.registry = registry

    @staticmethod
    def _as_float(value: Any) -> Optional[float]:
        if isinstance(value, (int, float)):
            return float(value)
        return None

    def _resolve_primary_value(
        self,
        primary_metric: str,
        signal_biomarkers: Dict[str, float],
        signal_derived: Dict[str, float],
    ) -> Optional[float]:
        if primary_metric in signal_biomarkers:
            return self._as_float(signal_biomarkers[primary_metric])
        if primary_metric in signal_derived:
            return self._as_float(signal_derived[primary_metric])
        return None

    def _matches_threshold(self, threshold: Dict[str, Any], value: float) -> bool:
        operator = str(threshold.get("operator", "")).strip()
        if operator == "range":
            min_value = self._as_float(threshold.get("min_value"))
            max_value = self._as_float(threshold.get("max_value"))
            if min_value is None or max_value is None:
                return False
            return min_value <= value <= max_value

        compare_value = self._as_float(threshold.get("value"))
        if compare_value is None:
            return False
        if operator == "<":
            return value < compare_value
        if operator == "<=":
            return value <= compare_value
        if operator == ">":
            return value > compare_value
        if operator == ">=":
            return value >= compare_value
        if operator == "==":
            return value == compare_value
        return False

    def _evaluate_state(self, thresholds: List[Dict[str, Any]], primary_value: float) -> Optional[str]:
        best_state: Optional[str] = None
        best_rank = -1
        for threshold in thresholds:
            if not isinstance(threshold, dict):
                continue
            severity = str(threshold.get("severity", "")).strip()
            rank = self._STATE_RANK.get(severity)
            if rank is None:
                continue
            if self._matches_threshold(threshold, primary_value) and rank > best_rank:
                best_rank = rank
                best_state = severity
        return best_state

    def _evaluate_lab_range_activation_state(
        self,
        signal: Dict[str, Any],
        primary_metric: str,
        primary_value: float,
        lab_ranges: Dict[str, dict],
    ) -> Optional[str]:
        ref = (lab_ranges or {}).get(primary_metric)
        if not isinstance(ref, dict):
            return None
        low = self._as_float(ref.get("min"))
        high = self._as_float(ref.get("max"))
        if low is None and high is None:
            return None

        activation_cfg = signal.get("activation_config", {})
        if not isinstance(activation_cfg, dict):
            activation_cfg = {}
        upper_bound_state = str(activation_cfg.get("upper_bound_state", "at_risk")).strip()
        if upper_bound_state not in self._STATE_RANK:
            upper_bound_state = "at_risk"

        upper_bound_enabled = bool(activation_cfg.get("enable_upper_bound", True))
        if upper_bound_enabled and high is not None and primary_value > high:
            return upper_bound_state

        lower_bound_enabled = bool(activation_cfg.get("enable_lower_bound", False))
        lower_bound_state = str(activation_cfg.get("lower_bound_state", "at_risk")).strip()
        if lower_bound_state not in self._STATE_RANK:
            lower_bound_state = "at_risk"
        if lower_bound_enabled and low is not None and primary_value < low:
            return lower_bound_state

        return None

    def _resolve_condition_metric_value(
        self,
        metric_id: str,
        signal_biomarkers: Dict[str, float],
        signal_derived: Dict[str, float],
    ) -> Optional[float]:
        if metric_id in signal_biomarkers:
            return self._as_float(signal_biomarkers[metric_id])
        if metric_id in signal_derived:
            return self._as_float(signal_derived[metric_id])
        return None

    @staticmethod
    def _normalize_override_boundary(raw: Any) -> str:
        """Map governed boundary tokens (and ingestion aliases) to canonical modes."""
        if not isinstance(raw, str):
            return ""
        token = raw.strip().lower().replace("-", "_")
        if token in {"lower", "below_min"}:
            return "lower"
        if token in {"upper", "above_max"}:
            return "upper"
        if token == "out_of_range":
            return "out_of_range"
        # KB-S51 — narrow companion-normality semantics (see governance artifact).
        if token in {"not_above_max", "at_or_below_max"}:
            return "not_above_max"
        if token in {"not_below_min", "at_or_above_min"}:
            return "not_below_min"
        return ""

    def _evaluate_lab_range_boundary_condition(
        self,
        boundary_mode: str,
        observed: float,
        lab_ranges: Dict[str, dict],
        metric_id: str,
    ) -> bool:
        """
        Evaluate lab-range-boundary semantics against authoritative lab_ranges[metric_id].
        Uses min/max from the reference dict; missing bounds fail closed (False).
        """
        ref = (lab_ranges or {}).get(metric_id)
        if not isinstance(ref, dict):
            return False
        low = self._as_float(ref.get("min"))
        high = self._as_float(ref.get("max"))
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

    def _evaluate_single_condition(
        self,
        condition: Dict[str, Any],
        signal_biomarkers: Dict[str, float],
        signal_derived: Dict[str, float],
        lab_ranges: Dict[str, dict],
    ) -> bool:
        metric_id = str(condition.get("metric_id", "")).strip()
        if not metric_id:
            raise ValueError(f"Unsupported override condition shape: {condition}")

        comp_raw = condition.get("comparator_type")
        comp = str(comp_raw).strip() if comp_raw is not None else ""

        if comp == "lab_range_boundary":
            boundary_mode = self._normalize_override_boundary(condition.get("boundary"))
            if not boundary_mode:
                raise ValueError(f"Unsupported override condition boundary for lab_range_boundary: {condition}")
            if "value" in condition:
                raise ValueError(f"lab_range_boundary override must not include value: {condition}")

            observed = self._resolve_condition_metric_value(
                metric_id=metric_id,
                signal_biomarkers=signal_biomarkers,
                signal_derived=signal_derived,
            )
            if observed is None:
                return False
            return self._evaluate_lab_range_boundary_condition(
                boundary_mode=boundary_mode,
                observed=observed,
                lab_ranges=lab_ranges or {},
                metric_id=metric_id,
            )

        # Legacy numeric (comparator absent) or explicit numeric_value
        operator = str(condition.get("operator", "")).strip()
        compare_value = self._as_float(condition.get("value"))
        if comp not in ("", "numeric_value"):
            raise ValueError(f"Unsupported override comparator_type: {condition}")
        if operator not in {"<", "<=", ">", ">=", "=="} or compare_value is None:
            raise ValueError(f"Unsupported override condition shape: {condition}")

        observed = self._resolve_condition_metric_value(
            metric_id=metric_id,
            signal_biomarkers=signal_biomarkers,
            signal_derived=signal_derived,
        )
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

    def _evaluate_override_rules(
        self,
        override_rules: Any,
        threshold_state: str,
        signal_biomarkers: Dict[str, float],
        signal_derived: Dict[str, float],
        lab_ranges: Dict[str, dict],
    ) -> tuple[str, Optional[int]]:
        if not isinstance(override_rules, list):
            raise ValueError(f"Unsupported override_rules shape: {override_rules}")

        best_state = threshold_state
        best_rank = self._STATE_RANK.get(threshold_state, -1)
        best_satisfied_count: Optional[int] = None
        for rule in override_rules:
            if not isinstance(rule, dict):
                raise ValueError(f"Unsupported override rule shape: {rule}")
            _rule_id = str(rule.get("rule_id", "")).strip()
            resulting_state = str(rule.get("resulting_state", "")).strip()
            conditions = rule.get("conditions")
            if not _rule_id or resulting_state not in self._STATE_RANK or not isinstance(conditions, list) or not conditions:
                raise ValueError(f"Unsupported override rule shape: {rule}")

            any_of_results: List[bool] = []
            all_of_results: List[bool] = []
            satisfied_count = 0
            for condition in conditions:
                if not isinstance(condition, dict):
                    raise ValueError(f"Unsupported override condition shape: {condition}")
                condition_type = str(condition.get("condition_type", "")).strip()
                if condition_type not in {"any_of", "all_of"}:
                    raise ValueError(f"Unsupported override condition_type: {condition}")
                condition_result = self._evaluate_single_condition(
                    condition=condition,
                    signal_biomarkers=signal_biomarkers,
                    signal_derived=signal_derived,
                    lab_ranges=lab_ranges,
                )
                if condition_type == "any_of":
                    any_of_results.append(condition_result)
                else:
                    all_of_results.append(condition_result)
                if condition_result:
                    satisfied_count += 1

            all_of_ok = all(all_of_results) if all_of_results else True
            any_of_ok = any(any_of_results) if any_of_results else True
            fires = all_of_ok and any_of_ok
            if not fires:
                continue

            rank = self._STATE_RANK[resulting_state]
            # Deterministic precedence:
            # - higher rank always wins
            # - on same rank, later rule in YAML order wins
            if rank >= best_rank:
                best_rank = rank
                best_state = resulting_state
                best_satisfied_count = satisfied_count

        return best_state, best_satisfied_count

    def _passes_mandatory_pre_emission_gates(
        self,
        signal: Dict[str, Any],
        signal_biomarkers: Dict[str, float],
        signal_derived: Dict[str, float],
        lab_ranges: Dict[str, dict],
    ) -> bool:
        gates = signal.get("mandatory_pre_emission_gates")
        if not isinstance(gates, list) or not gates:
            return True

        for gate in gates:
            if not isinstance(gate, dict):
                return False

            comparator_type = str(gate.get("comparator_type", "")).strip()
            metric_id = str(gate.get("metric_id", "")).strip()
            if not metric_id:
                return False

            if comparator_type == "biomarker_present":
                observed = self._resolve_condition_metric_value(
                    metric_id=metric_id,
                    signal_biomarkers=signal_biomarkers,
                    signal_derived=signal_derived,
                )
                if observed is None:
                    return False
                continue

            condition = dict(gate)
            condition.setdefault("condition_type", "all_of")
            if not self._evaluate_single_condition(
                condition=condition,
                signal_biomarkers=signal_biomarkers,
                signal_derived=signal_derived,
                lab_ranges=lab_ranges or {},
            ):
                return False

        return True

    def _lab_normal_but_flagged(
        self,
        primary_metric: str,
        signal_state: str,
        primary_value: float,
        lab_ranges: Dict[str, dict],
    ) -> bool:
        if signal_state not in {"suboptimal", "at_risk"}:
            return False
        ref = lab_ranges.get(primary_metric)
        if not isinstance(ref, dict):
            return False
        low = self._as_float(ref.get("min"))
        high = self._as_float(ref.get("max"))
        if low is None or high is None:
            return False
        return low <= primary_value <= high

    def evaluate_all(
        self,
        signal_biomarkers: Dict[str, float],
        signal_derived: Dict[str, float],
        lab_ranges: Dict[str, dict],
        reference_profiles: Optional[Dict[str, dict]] = None,
    ) -> List[SignalResult]:
        results: List[SignalResult] = []
        reference_profiles = reference_profiles or {}
        available_metric_ids = set(signal_biomarkers.keys()) | set(signal_derived.keys())
        for signal in self.registry.get_all_signals():
            primary_metric = str(signal.get("primary_metric", "")).strip()
            if not primary_metric:
                continue

            primary_value = self._resolve_primary_value(primary_metric, signal_biomarkers, signal_derived)
            primary_metric_present = primary_value is not None
            if primary_value is None:
                continue

            activation_logic = str(signal.get("activation_logic", "deterministic_threshold")).strip()
            if activation_logic == "lab_range_exceeded":
                signal_state = self._evaluate_lab_range_activation_state(
                    signal=signal,
                    primary_metric=primary_metric,
                    primary_value=primary_value,
                    lab_ranges=lab_ranges or {},
                )
                if signal_state is None:
                    continue
            else:
                thresholds = signal.get("thresholds")
                if not isinstance(thresholds, list):
                    continue
                signal_state = self._evaluate_state(thresholds, primary_value)
                if signal_state is None:
                    continue
            signal_state, override_satisfied_count = self._evaluate_override_rules(
                override_rules=signal.get("override_rules", []),
                threshold_state=signal_state,
                signal_biomarkers=signal_biomarkers,
                signal_derived=signal_derived,
                lab_ranges=lab_ranges or {},
            )

            if not self._passes_mandatory_pre_emission_gates(
                signal=signal,
                signal_biomarkers=signal_biomarkers,
                signal_derived=signal_derived,
                lab_ranges=lab_ranges or {},
            ):
                continue

            output = signal.get("output", {})
            supporting_markers = []
            if isinstance(output, dict) and isinstance(output.get("supporting_markers"), list):
                supporting_markers = [str(x) for x in output["supporting_markers"] if str(x).strip()]
            explanation = signal.get("explanation")
            if not isinstance(explanation, dict):
                explanation = None
            confidence, confidence_reasons = calculate_signal_confidence(
                primary_metric=primary_metric,
                primary_metric_present=primary_metric_present,
                supporting_markers=supporting_markers,
                available_metrics=available_metric_ids,
                signal_state=signal_state,
                lab_ranges=lab_ranges or {},
                reference_profiles=reference_profiles,
                override_satisfied_count=override_satisfied_count,
            )

            result = SignalResult(
                signal_id=str(signal.get("signal_id", "")).strip(),
                activation_key=str(signal.get("activation_key", "")).strip(),
                source_spec_id=str(signal.get("source_spec_id", "")).strip(),
                package_id=str(signal.get("package_id", "")).strip(),
                system=str(signal.get("system", "")).strip(),
                signal_state=signal_state,
                signal_value=primary_value,
                confidence=confidence,
                confidence_reasons=confidence_reasons,
                primary_metric=primary_metric,
                lab_normal_but_flagged=self._lab_normal_but_flagged(
                    primary_metric=primary_metric,
                    signal_state=signal_state,
                    primary_value=primary_value,
                    lab_ranges=lab_ranges or {},
                ),
                supporting_markers=supporting_markers,
                explanation=explanation,
            )
            results.append(result)

        results.sort(key=lambda r: (r.signal_id, r.activation_key))
        return apply_signal_authority_collision_policy(
            results,
            signal_biomarkers=signal_biomarkers,
            signal_derived=signal_derived,
            lab_ranges=lab_ranges or {},
        )
