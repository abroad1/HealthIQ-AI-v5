"""
Reusable runtime context requirement evaluation for package-declared context gates.

Deterministic, fail-closed, no LLM calls, no hardcoded clinical thresholds.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence

import yaml

DEFAULT_MODEL_PATH = (
    Path(__file__).resolve().parents[3]
    / "knowledge_bus"
    / "governance"
    / "runtime_context_requirements_model_v1.yaml"
)

SUPPORTED_CONTEXT_TYPES = frozenset(
    {
        "demographic",
        "biomarker",
        "medication",
        "supplement",
        "symptom",
        "clinical_context",
        "known_condition",
    }
)

SUPPORTED_MISSING_BEHAVIOURS = frozenset(
    {
        "suppress_signal",
        "emit_context_insufficient",
        "defer_activation",
    }
)


class RuntimeContextModelError(RuntimeError):
    """Raised when the runtime context requirements model cannot be loaded or validated."""


@dataclass(frozen=True)
class RuntimeContextEvaluationResult:
    satisfied: bool
    missing_requirements: tuple[str, ...] = ()
    behaviour: str = "suppress_signal"


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


def _normalize_boundary(raw: Any) -> str:
    if not isinstance(raw, str):
        return ""
    token = raw.strip().lower().replace("-", "_")
    if token in {"lower", "below_min"}:
        return "lower"
    if token in {"upper", "above_max"}:
        return "upper"
    if token == "out_of_range":
        return "out_of_range"
    return ""


def _evaluate_lab_range_boundary(
    *,
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
    return False


def load_runtime_context_requirements_model(
    model_path: Optional[Path] = None,
) -> Dict[str, Any]:
    path = model_path or DEFAULT_MODEL_PATH
    if not path.is_file():
        raise RuntimeContextModelError(f"Runtime context requirements model not found: {path}")
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        raise RuntimeContextModelError(
            f"Runtime context requirements model is malformed YAML: {path}"
        ) from exc
    if not isinstance(payload, dict):
        raise RuntimeContextModelError(f"Invalid runtime context requirements model: {path}")
    return payload


def validate_runtime_context_requirements_model(model: Dict[str, Any], *, model_path: Path) -> None:
    if model.get("runtime_consumed") is not True:
        raise RuntimeContextModelError(
            f"runtime_context_requirements_model must set runtime_consumed: true ({model_path})"
        )
    supported = model.get("supported_context_types")
    if not isinstance(supported, list) or not supported:
        raise RuntimeContextModelError(f"supported_context_types missing ({model_path})")


def _context_bucket(runtime_context: Mapping[str, Any], context_type: str) -> Mapping[str, Any]:
    bucket = runtime_context.get(context_type)
    if isinstance(bucket, Mapping):
        return bucket
    return {}


def _requirement_label(requirement: Mapping[str, Any]) -> str:
    context_type = str(requirement.get("context_type", "")).strip()
    key = str(requirement.get("key", "")).strip()
    req = str(requirement.get("requirement", "present")).strip()
    return f"{context_type}.{key}:{req}"


def _value_present(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict, tuple, set)):
        return len(value) > 0
    return True


def build_runtime_context_snapshot(
    *,
    questionnaire_responses: Optional[Mapping[str, Any]] = None,
    lifestyle_factors: Optional[Mapping[str, Any]] = None,
    medical_history: Optional[Mapping[str, Any]] = None,
    signal_biomarkers: Optional[Mapping[str, float]] = None,
) -> Dict[str, Any]:
    """
    Build a deterministic runtime context snapshot from available upstream inputs.

    Only includes keys that can be derived from supplied data — never invents context.
    """
    snapshot: Dict[str, Any] = {
        "demographic": {},
        "biomarker": {},
        "medication": {},
        "supplement": {},
        "symptom": {},
        "clinical_context": {},
        "known_condition": {},
    }
    responses = dict(questionnaire_responses or {})
    history = dict(medical_history or {})

    sex = responses.get("biological_sex")
    if sex is not None and str(sex).strip():
        snapshot["demographic"]["sex"] = str(sex).strip().lower()

    dob = responses.get("date_of_birth")
    if dob is not None:
        try:
            if hasattr(dob, "year"):
                born = dob if isinstance(dob, date) else date.fromisoformat(str(dob)[:10])
            else:
                born = date.fromisoformat(str(dob).replace("Z", "").split("T")[0][:10])
            today = date.today()
            age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
            snapshot["demographic"]["age"] = age
        except (ValueError, TypeError, AttributeError):
            pass

    age_metric = (signal_biomarkers or {}).get("age")
    if age_metric is not None and "age" not in snapshot["demographic"]:
        snapshot["demographic"]["age"] = int(age_metric)

    if "symptoms" in responses and _value_present(responses.get("symptoms")):
        snapshot["symptom"]["symptoms_present"] = True

    if "supplements" in responses and _value_present(responses.get("supplements")):
        snapshot["supplement"]["supplements_disclosed"] = True

    meds = responses.get("long_term_medications") or history.get("medications")
    if _value_present(meds):
        snapshot["medication"]["long_term_medications"] = meds

    med_classes = history.get("long_term_medication_classes") or meds
    if isinstance(med_classes, list):
        lowered = {str(item).strip().lower() for item in med_classes if str(item).strip()}
        if any("testosterone" in item or "hormone" in item for item in lowered):
            snapshot["medication"]["hormone_therapy"] = True
        if any("steroid" in item or "corticosteroid" in item for item in lowered):
            snapshot["medication"]["steroid"] = True
        if any("thyroid" in item for item in lowered):
            snapshot["medication"]["thyroid_medication"] = True

    conditions = history.get("conditions") or responses.get("chronic_conditions")
    if _value_present(conditions):
        snapshot["known_condition"]["known_conditions"] = conditions

    if responses.get("stress_level") is not None or (lifestyle_factors or {}).get("stress_level") is not None:
        snapshot["clinical_context"]["stress_context"] = True

    if _value_present(responses.get("chronic_conditions")):
        snapshot["clinical_context"]["illness_or_recovery_status"] = True

    supplements = responses.get("supplements")
    if isinstance(supplements, list):
        lowered = {str(item).strip().lower() for item in supplements}
        if any("testosterone" in item for item in lowered):
            snapshot["supplement"]["testosterone_supplement"] = True
        if any("steroid" in item or "prohormone" in item for item in lowered):
            snapshot["clinical_context"]["aas_exposure"] = True

    return snapshot


def evaluate_runtime_context_requirements(
    requirements: Mapping[str, Any],
    *,
    runtime_context: Optional[Mapping[str, Any]],
    signal_biomarkers: Mapping[str, float],
    signal_derived: Mapping[str, float],
    lab_ranges: Mapping[str, dict],
) -> RuntimeContextEvaluationResult:
    if not isinstance(requirements, dict) or not requirements:
        return RuntimeContextEvaluationResult(satisfied=True)

    behaviour = str(requirements.get("missing_context_behaviour", "suppress_signal")).strip()
    if behaviour not in SUPPORTED_MISSING_BEHAVIOURS:
        behaviour = "suppress_signal"

    required = requirements.get("required_context")
    if not isinstance(required, list) or not required:
        return RuntimeContextEvaluationResult(satisfied=True, behaviour=behaviour)

    ctx = runtime_context if isinstance(runtime_context, Mapping) else {}
    missing: List[str] = []

    for item in required:
        if not isinstance(item, dict):
            missing.append("invalid_requirement")
            continue

        context_type = str(item.get("context_type", "")).strip()
        key = str(item.get("key", "")).strip()
        requirement = str(item.get("requirement", "present")).strip() or "present"

        if context_type not in SUPPORTED_CONTEXT_TYPES or not key:
            missing.append(_requirement_label(item))
            continue

        if context_type == "biomarker":
            observed = _resolve_metric_value(key, signal_biomarkers, signal_derived)
            if requirement == "present":
                if observed is None:
                    missing.append(_requirement_label(item))
                continue
            if requirement == "lab_range_boundary":
                boundary = _normalize_boundary(item.get("boundary"))
                if observed is None or not boundary:
                    missing.append(_requirement_label(item))
                    continue
                if not _evaluate_lab_range_boundary(
                    boundary_mode=boundary,
                    observed=observed,
                    lab_ranges=lab_ranges,
                    metric_id=key,
                ):
                    missing.append(_requirement_label(item))
                continue
            missing.append(_requirement_label(item))
            continue

        bucket = _context_bucket(ctx, context_type)
        if requirement == "present":
            if not _value_present(bucket.get(key)):
                missing.append(_requirement_label(item))
            continue

        missing.append(_requirement_label(item))

    return RuntimeContextEvaluationResult(
        satisfied=not missing,
        missing_requirements=tuple(missing),
        behaviour=behaviour,
    )


def passes_runtime_context_requirements(
    signal: Mapping[str, Any],
    *,
    runtime_context: Optional[Mapping[str, Any]],
    signal_biomarkers: Mapping[str, float],
    signal_derived: Mapping[str, float],
    lab_ranges: Mapping[str, dict],
) -> bool:
    requirements = signal.get("runtime_context_requirements")
    if not isinstance(requirements, dict) or not requirements:
        return True

    result = evaluate_runtime_context_requirements(
        requirements,
        runtime_context=runtime_context,
        signal_biomarkers=signal_biomarkers,
        signal_derived=signal_derived,
        lab_ranges=lab_ranges,
    )
    if result.satisfied:
        return True
    if result.behaviour in {"suppress_signal", "defer_activation"}:
        return False
    return False
