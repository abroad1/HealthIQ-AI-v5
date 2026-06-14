"""
Reusable runtime context requirement evaluation for package-declared context gates.

Deterministic, fail-closed, no LLM calls, no hardcoded clinical thresholds.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Mapping, Optional, Sequence

import yaml

if TYPE_CHECKING:
    from core.models.context import AnalysisContext

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

DISCLOSURE_ANSWERED_YES = "answered_yes"
DISCLOSURE_ANSWERED_NO = "answered_no"
DISCLOSURE_NOT_ANSWERED = "not_answered"
DISCLOSURE_UNKNOWN = "unknown"
DISCLOSURE_NOT_APPLICABLE = "not_applicable"

SUPPORTED_DISCLOSURE_STATES = frozenset(
    {
        DISCLOSURE_ANSWERED_YES,
        DISCLOSURE_ANSWERED_NO,
        DISCLOSURE_NOT_ANSWERED,
        DISCLOSURE_UNKNOWN,
        DISCLOSURE_NOT_APPLICABLE,
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


def _field_answered(mapping: Mapping[str, Any], key: str) -> bool:
    return key in mapping


def _medications_question_answered(
    responses: Mapping[str, Any],
    history: Mapping[str, Any],
) -> bool:
    if _field_answered(responses, "long_term_medications"):
        return True
    if _field_answered(responses, "current_medications"):
        return True
    if _field_answered(history, "medications"):
        return True
    if _field_answered(history, "long_term_medication_classes"):
        return True
    return False


def _disclosure_state_from_value(value: Any, *, field_answered: bool) -> str:
    """Map a user-declared field value to a reusable disclosure-state primitive."""
    if not field_answered:
        return DISCLOSURE_NOT_ANSWERED
    if value is None:
        return DISCLOSURE_NOT_ANSWERED
    if isinstance(value, list):
        if len(value) == 0:
            return DISCLOSURE_ANSWERED_NO
        lowered = {str(item).strip().lower() for item in value if str(item).strip()}
        if lowered <= {"", "none", "no", "false", "n/a", "not_applicable"}:
            return DISCLOSURE_ANSWERED_NO
        return DISCLOSURE_ANSWERED_YES
    if isinstance(value, str):
        stripped = value.strip().lower()
        if not stripped or stripped in {"none", "no", "false", "n/a", "not_applicable"}:
            return DISCLOSURE_ANSWERED_NO
        return DISCLOSURE_ANSWERED_YES
    if isinstance(value, bool):
        return DISCLOSURE_ANSWERED_YES if value else DISCLOSURE_ANSWERED_NO
    return DISCLOSURE_ANSWERED_YES if _value_present(value) else DISCLOSURE_ANSWERED_NO


def _set_disclosure_state(bucket: Dict[str, Any], key: str, state: str) -> None:
    if state in SUPPORTED_DISCLOSURE_STATES:
        bucket[key] = state


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

    age_value = snapshot["demographic"].get("age")
    if isinstance(age_value, int):
        snapshot["demographic"]["is_adult"] = age_value >= 18

    lifestyle = dict(lifestyle_factors or {})
    pregnancy_answered = _field_answered(responses, "pregnancy_status") or _field_answered(
        lifestyle, "pregnancy_status"
    )
    if pregnancy_answered:
        pregnancy_value = responses.get("pregnancy_status") or lifestyle.get("pregnancy_status")
        pregnancy_state = _disclosure_state_from_value(
            pregnancy_value,
            field_answered=True,
        )
        _set_disclosure_state(
            snapshot["clinical_context"],
            "pregnancy_status",
            pregnancy_state,
        )

    if "symptoms" in responses and _value_present(responses.get("symptoms")):
        snapshot["symptom"]["symptoms_present"] = True

    supplements_answered = _field_answered(responses, "supplements")
    supplements_value = responses.get("supplements")
    supplement_state = _disclosure_state_from_value(
        supplements_value,
        field_answered=supplements_answered,
    )
    _set_disclosure_state(snapshot["supplement"], "supplements_status", supplement_state)
    if supplements_answered:
        snapshot["supplement"]["supplements_disclosed"] = True

    medications_answered = _medications_question_answered(responses, history)
    meds = responses.get("long_term_medications") or history.get("medications") or history.get(
        "long_term_medication_classes"
    )
    if responses.get("current_medications") is not None and not _field_answered(responses, "long_term_medications"):
        meds = responses.get("current_medications")
    long_term_meds_state = _disclosure_state_from_value(
        meds,
        field_answered=medications_answered,
    )
    _set_disclosure_state(
        snapshot["medication"],
        "long_term_medications_status",
        long_term_meds_state,
    )
    if medications_answered:
        snapshot["medication"]["long_term_medications_disclosed"] = True
        snapshot["medication"]["hormone_therapy_status_disclosed"] = True
        snapshot["medication"]["steroid_use_disclosed"] = True
        snapshot["medication"]["thyroid_medication_disclosed"] = True

    if _value_present(meds):
        snapshot["medication"]["long_term_medications"] = meds

    med_classes = history.get("long_term_medication_classes") or meds
    hormone_therapy_state = DISCLOSURE_ANSWERED_NO if medications_answered else DISCLOSURE_NOT_ANSWERED
    steroid_use_state = DISCLOSURE_ANSWERED_NO if medications_answered else DISCLOSURE_NOT_ANSWERED
    thyroid_medication_state = (
        DISCLOSURE_ANSWERED_NO if medications_answered else DISCLOSURE_NOT_ANSWERED
    )
    if isinstance(med_classes, list):
        lowered = {str(item).strip().lower() for item in med_classes if str(item).strip()}
        if any("testosterone" in item or "hormone" in item for item in lowered):
            snapshot["medication"]["hormone_therapy"] = True
            hormone_therapy_state = DISCLOSURE_ANSWERED_YES
        if any("steroid" in item or "corticosteroid" in item for item in lowered):
            snapshot["medication"]["steroid"] = True
            steroid_use_state = DISCLOSURE_ANSWERED_YES
        if any("thyroid" in item for item in lowered):
            snapshot["medication"]["thyroid_medication"] = True
            thyroid_medication_state = DISCLOSURE_ANSWERED_YES
    _set_disclosure_state(snapshot["medication"], "hormone_therapy_status", hormone_therapy_state)
    _set_disclosure_state(snapshot["medication"], "steroid_use_status", steroid_use_state)
    _set_disclosure_state(snapshot["medication"], "thyroid_medication_status", thyroid_medication_state)

    conditions = history.get("conditions") or responses.get("chronic_conditions")
    if _value_present(conditions):
        snapshot["known_condition"]["known_conditions"] = conditions

    if responses.get("stress_level") is not None or (lifestyle_factors or {}).get("stress_level") is not None:
        snapshot["clinical_context"]["stress_context"] = True

    if _value_present(responses.get("chronic_conditions")):
        snapshot["clinical_context"]["illness_or_recovery_exposure"] = True

    illness_answered = _field_answered(responses, "chronic_conditions") or _field_answered(
        responses, "recent_infections"
    )
    illness_value = responses.get("chronic_conditions")
    if _field_answered(responses, "recent_infections") and illness_value is None:
        illness_value = responses.get("recent_infections")
    illness_state = _disclosure_state_from_value(
        illness_value,
        field_answered=illness_answered,
    )
    _set_disclosure_state(
        snapshot["clinical_context"],
        "illness_or_recovery_disclosure_status",
        illness_state,
    )
    if illness_answered:
        snapshot["clinical_context"]["illness_or_recovery_status_disclosed"] = True

    aas_state = supplement_state if supplements_answered else DISCLOSURE_NOT_ANSWERED
    if supplements_answered:
        snapshot["clinical_context"]["aas_exposure_status_disclosed"] = True

    supplements = responses.get("supplements")
    if isinstance(supplements, list):
        lowered = {str(item).strip().lower() for item in supplements}
        if any("testosterone" in item for item in lowered):
            snapshot["supplement"]["testosterone_supplement"] = True
        if any("steroid" in item or "prohormone" in item for item in lowered):
            snapshot["clinical_context"]["aas_exposure"] = True
            aas_state = DISCLOSURE_ANSWERED_YES
        if any("dhea" in item for item in lowered):
            snapshot["supplement"]["dhea_supplementation"] = True
    _set_disclosure_state(snapshot["clinical_context"], "aas_exposure_status", aas_state)

    if _field_answered(responses, "symptoms"):
        symptom_state = _disclosure_state_from_value(
            responses.get("symptoms"),
            field_answered=True,
        )
        _set_disclosure_state(snapshot["symptom"], "symptoms_status", symptom_state)

    if _field_answered(responses, "biological_sex"):
        _set_disclosure_state(
            snapshot["demographic"],
            "sex_status",
            DISCLOSURE_ANSWERED_YES if snapshot["demographic"].get("sex") else DISCLOSURE_ANSWERED_NO,
        )
    if _field_answered(responses, "date_of_birth") or (signal_biomarkers or {}).get("age") is not None:
        _set_disclosure_state(snapshot["demographic"], "age_status", DISCLOSURE_ANSWERED_YES)

    lifestyle = dict(lifestyle_factors or {})
    for field_name, primitive_key in (
        ("calorie_restriction", "calorie_restriction_status"),
        ("fasting", "fasting_status"),
        ("under_eating", "under_eating_status"),
        ("weight_loss_phase", "weight_loss_phase_status"),
        ("heavy_training_load", "heavy_training_load_status"),
        ("overtraining", "overtraining_status"),
    ):
        if _field_answered(lifestyle, field_name):
            _set_disclosure_state(
                snapshot["clinical_context"],
                primitive_key,
                _disclosure_state_from_value(lifestyle.get(field_name), field_answered=True),
            )

    for biomarker_id in signal_biomarkers or {}:
        snapshot["biomarker"][f"{biomarker_id}_available"] = True

    return snapshot


def build_runtime_context_snapshot_from_analysis_context(
    context: AnalysisContext,
    *,
    signal_biomarkers: Optional[Mapping[str, float]] = None,
) -> Dict[str, Any]:
    """
    Build runtime context from assembled AnalysisContext (post-governance assembly).

    Signal evaluation must use this adapter rather than reading raw questionnaire_data
    before AnalysisContext exists.
    """
    questionnaire_responses = getattr(context, "questionnaire_responses", None)
    lifestyle_factors = getattr(context, "lifestyle_factors", None)
    medical_history = getattr(context, "medical_history", None)
    return build_runtime_context_snapshot(
        questionnaire_responses=questionnaire_responses,
        lifestyle_factors=lifestyle_factors,
        medical_history=medical_history,
        signal_biomarkers=signal_biomarkers,
    )


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

        if requirement == "disclosed":
            if bucket.get(key) is not True:
                missing.append(_requirement_label(item))
            continue

        if requirement == "disclosure_state":
            allowed = item.get("allowed_values")
            observed = bucket.get(key)
            if not isinstance(allowed, list) or not allowed:
                missing.append(_requirement_label(item))
                continue
            allowed_set = {str(value).strip() for value in allowed if str(value).strip()}
            if observed not in allowed_set:
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
