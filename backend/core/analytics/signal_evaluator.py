"""
Deterministic signal registry/evaluator for package signal libraries.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from core.models.signal import SignalResult


class SignalRegistry:
    """Load authoritative package signal libraries deterministically."""

    def __init__(self) -> None:
        self._signals_by_id: Dict[str, Dict[str, Any]] = {}
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
        signals_by_id: Dict[str, Dict[str, Any]] = {}
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
                if signal_id in signals_by_id:
                    existing_source = str(signals_by_id[signal_id].get("_source_path", ""))
                    # Deterministic duplicate policy: when the same signal_id appears in
                    # multiple package files, keep the definition from the lexicographically
                    # later path and overwrite the earlier one.
                    if str(path) <= existing_source:
                        continue
                compiled = dict(item)
                compiled["_source_path"] = str(path)
                signals_by_id[signal_id] = compiled

        ordered_ids = sorted(signals_by_id.keys())
        joined = "|".join(ordered_ids)
        digest = hashlib.sha256(joined.encode("utf-8")).hexdigest()[:12]
        self.version = digest
        self.package_hash = digest
        self._signals_by_id = {sid: signals_by_id[sid] for sid in ordered_ids}

    def get_all_signals(self) -> List[Dict[str, Any]]:
        return [dict(self._signals_by_id[sid]) for sid in sorted(self._signals_by_id.keys())]


class SignalEvaluator:
    """Evaluate repository-defined signals from raw biomarker + derived values."""

    _STATE_RANK = {
        "optimal": 0,
        "suboptimal": 1,
        "at_risk": 2,
    }

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

    def _evaluate_single_condition(
        self,
        condition: Dict[str, Any],
        signal_biomarkers: Dict[str, float],
        signal_derived: Dict[str, float],
    ) -> bool:
        metric_id = str(condition.get("metric_id", "")).strip()
        operator = str(condition.get("operator", "")).strip()
        compare_value = self._as_float(condition.get("value"))
        if not metric_id or operator not in {"<", "<=", ">", ">=", "=="} or compare_value is None:
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
    ) -> str:
        if not isinstance(override_rules, list):
            raise ValueError(f"Unsupported override_rules shape: {override_rules}")

        best_state = threshold_state
        best_rank = self._STATE_RANK.get(threshold_state, -1)
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
                )
                if condition_type == "any_of":
                    any_of_results.append(condition_result)
                else:
                    all_of_results.append(condition_result)

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

        return best_state

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
    ) -> List[SignalResult]:
        results: List[SignalResult] = []
        for signal in self.registry.get_all_signals():
            primary_metric = str(signal.get("primary_metric", "")).strip()
            if not primary_metric:
                continue

            primary_value = self._resolve_primary_value(primary_metric, signal_biomarkers, signal_derived)
            if primary_value is None:
                continue

            thresholds = signal.get("thresholds")
            if not isinstance(thresholds, list):
                continue
            signal_state = self._evaluate_state(thresholds, primary_value)
            if signal_state is None:
                continue
            signal_state = self._evaluate_override_rules(
                override_rules=signal.get("override_rules", []),
                threshold_state=signal_state,
                signal_biomarkers=signal_biomarkers,
                signal_derived=signal_derived,
            )

            output = signal.get("output", {})
            supporting_markers = []
            if isinstance(output, dict) and isinstance(output.get("supporting_markers"), list):
                supporting_markers = [str(x) for x in output["supporting_markers"] if str(x).strip()]
            explanation = signal.get("explanation")
            if not isinstance(explanation, dict):
                explanation = None

            result = SignalResult(
                signal_id=str(signal.get("signal_id", "")).strip(),
                system=str(signal.get("system", "")).strip(),
                signal_state=signal_state,
                signal_value=primary_value,
                confidence=None,
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

        results.sort(key=lambda r: r.signal_id)
        return results
