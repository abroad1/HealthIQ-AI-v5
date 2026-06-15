#!/usr/bin/env python3
"""
BETA-READINESS-SPRINT-2 — Active runtime signal context gate reachability validator.

Deterministic read-only check: every runtime_active_canonical Batch 2 signal must have
context gates that are reachable for realistic users unless explicitly registered as
suppress-until-answered with medical justification.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

import yaml

_BACKEND = Path(__file__).resolve().parents[1]
if str(_BACKEND) not in sys.path:
    sys.path.insert(0, str(_BACKEND))

_REPO = Path(__file__).resolve().parents[2]
_BATCH2_REGISTER = (
    _REPO / "knowledge_bus/governance/batch2_full_coverage_activation_execution_register_v1.yaml"
)
_POLICY = (
    _REPO / "knowledge_bus/governance/active_signal_context_gate_reachability_policy_v1.yaml"
)
_QUESTIONNAIRE = _REPO / "backend/ssot/questionnaire.json"
_PACKAGES = _REPO / "knowledge_bus/packages"

_SAFE_MISSING = frozenset({"not_answered", "not_applicable", "unknown"})
_PREGNANCY_SAFE = frozenset({"answered_no", "not_answered", "not_applicable"})


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(str(path))
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def _load_questionnaire_ids(path: Path) -> frozenset[str]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        return frozenset()
    ids: set[str] = set()
    for item in raw:
        if isinstance(item, dict) and isinstance(item.get("id"), str):
            ids.add(item["id"])
    return frozenset(ids)


def _optional_field_dependent_keys(
    policy: dict[str, Any],
    *,
    package_id: str,
) -> dict[str, frozenset[str]]:
    optional = policy.get("questionnaire_optional_fields") or {}
    if not isinstance(optional, dict):
        return {}
    out: dict[str, frozenset[str]] = {}
    for field_id, row in optional.items():
        if not isinstance(row, dict):
            continue
        scope = row.get("package_scope")
        if isinstance(scope, list) and scope and package_id not in {str(item) for item in scope}:
            continue
        keys = row.get("dependent_context_keys") or []
        if isinstance(keys, list):
            out[str(field_id)] = frozenset(str(k) for k in keys if str(k).strip())
    return out


def _context_key_to_questionnaire_field(key: str) -> str | None:
    mapping = {
        "hormone_therapy_status": "long_term_medications",
        "thyroid_medication_status": "long_term_medications",
        "long_term_medications_disclosed": "long_term_medications",
        "hormone_therapy_status_disclosed": "long_term_medications",
        "illness_or_recovery_disclosure_status": "chronic_conditions",
        "dhea_supplementation_status": "supplements",
        "aas_exposure_status": "supplements",
        "aas_exposure_status_disclosed": "supplements",
        "supplements_disclosed": "supplements",
        "symptoms_status": "symptoms",
        "calorie_restriction_status": "calorie_restriction",
        "fasting_status": "fasting",
    }
    return mapping.get(key)


def _activated_packages(register: dict[str, Any]) -> list[dict[str, Any]]:
    rows = register.get("activated_packages")
    if not isinstance(rows, list):
        return []
    return [row for row in rows if isinstance(row, dict) and row.get("package_id")]


def _load_signal_library(package_id: str) -> dict[str, Any]:
    path = _PACKAGES / package_id / "signal_library.yaml"
    return _load_yaml(path)


def _signal_for_id(payload: dict[str, Any], signal_id: str) -> dict[str, Any] | None:
    for item in payload.get("signals") or []:
        if isinstance(item, dict) and item.get("signal_id") == signal_id:
            return item
    return None


def _suppress_registry(policy: dict[str, Any]) -> dict[tuple[str, str, str], str]:
    out: dict[tuple[str, str, str], str] = {}
    for row in policy.get("suppress_until_answered_gates") or []:
        if not isinstance(row, dict):
            continue
        package_id = str(row.get("package_id", "")).strip()
        context_type = str(row.get("context_type", "")).strip()
        key = str(row.get("key", "")).strip()
        justification = str(row.get("medical_justification", "")).strip()
        if package_id and context_type and key:
            out[(package_id, context_type, key)] = justification
    return out


def _validate_pregnancy_gate(
    *,
    package_id: str,
    signal_id: str,
    gate: dict[str, Any],
    errors: list[str],
) -> None:
    allowed = gate.get("allowed_values")
    if not isinstance(allowed, list):
        errors.append(f"{package_id}/{signal_id}: pregnancy_status gate missing allowed_values")
        return
    allowed_set = {str(v).strip() for v in allowed if str(v).strip()}
    if "answered_yes" in allowed_set:
        errors.append(
            f"{package_id}/{signal_id}: pregnancy_status must not allow answered_yes "
            "(pregnancy-specific logic unavailable)"
        )
    missing_safe = _PREGNANCY_SAFE - allowed_set
    if missing_safe:
        errors.append(
            f"{package_id}/{signal_id}: pregnancy_status must allow {_PREGNANCY_SAFE}; "
            f"missing {sorted(missing_safe)}"
        )


def _validate_disclosure_gate(
    *,
    package_id: str,
    signal_id: str,
    gate: dict[str, Any],
    questionnaire_ids: frozenset[str],
    absent_keys: dict[str, Any],
    lifestyle_keys: frozenset[str],
    suppress_registry: dict[tuple[str, str, str], str],
    symptoms_decisions: dict[str, Any],
    questionnaire_mappings: dict[str, Any],
    optional_dependent_keys: dict[str, frozenset[str]],
    optional_field_policy: dict[str, Any],
    errors: list[str],
) -> None:
    context_type = str(gate.get("context_type", "")).strip()
    key = str(gate.get("key", "")).strip()
    requirement = str(gate.get("requirement", "")).strip()
    if requirement != "disclosure_state":
        return

    registry_key = (package_id, context_type, key)
    if registry_key in suppress_registry:
        return

    if key == "pregnancy_status":
        _validate_pregnancy_gate(package_id=package_id, signal_id=signal_id, gate=gate, errors=errors)
        return

    if key == "symptoms_status":
        decision_row = symptoms_decisions.get(package_id)
        if isinstance(decision_row, dict):
            decision = str(decision_row.get("decision", "")).strip()
            if decision == "required_gate_with_questionnaire_mapping":
                mapped = questionnaire_mappings.get("symptoms_status") or {}
                mapped_fields = [
                    str(field)
                    for field in mapped.keys()
                    if str(field) in questionnaire_ids
                ]
                if mapped_fields:
                    return
                errors.append(
                    f"{package_id}/{signal_id}: symptoms_status mapping fields "
                    f"not present in questionnaire: {list(mapped.keys())}"
                )
                return

    for _field_id, dependent_keys in optional_dependent_keys.items():
        if key not in dependent_keys:
            continue
        field_policy = optional_field_policy.get(_field_id) if isinstance(optional_field_policy, dict) else None
        if not isinstance(field_policy, dict):
            continue
        safe = field_policy.get("safe_missing_states") or []
        safe_set = {str(v).strip() for v in safe if str(v).strip()}
        allowed = gate.get("allowed_values")
        if not isinstance(allowed, list):
            errors.append(f"{package_id}/{signal_id}: {key} gate missing allowed_values")
            return
        allowed_set = {str(v).strip() for v in allowed if str(v).strip()}
        if not (safe_set & allowed_set):
            errors.append(
                f"{package_id}/{signal_id}: {key} depends on optional field {_field_id!r}; "
                f"allowed_values must include {sorted(safe_set)}"
            )
        return

    if key in absent_keys:
        allowed = gate.get("allowed_values")
        if not isinstance(allowed, list):
            errors.append(f"{package_id}/{signal_id}: {key} gate missing allowed_values")
            return
        allowed_set = {str(v).strip() for v in allowed if str(v).strip()}
        if not (_SAFE_MISSING & allowed_set):
            errors.append(
                f"{package_id}/{signal_id}: {key} is not in questionnaire; "
                f"allowed_values must include one of {sorted(_SAFE_MISSING)}"
            )
        return

    question_field = _context_key_to_questionnaire_field(key)
    if key in lifestyle_keys:
        return

    if question_field and question_field not in questionnaire_ids:
        allowed = gate.get("allowed_values")
        if isinstance(allowed, list):
            allowed_set = {str(v).strip() for v in allowed if str(v).strip()}
            if not (_SAFE_MISSING & allowed_set):
                errors.append(
                    f"{package_id}/{signal_id}: {key} maps to questionnaire field "
                    f"'{question_field}' which is absent; must allow safe missing states"
                )


def _validate_package(
    *,
    package_row: dict[str, Any],
    questionnaire_ids: frozenset[str],
    absent_keys: dict[str, Any],
    lifestyle_keys: frozenset[str],
    suppress_registry: dict[tuple[str, str, str], str],
    symptoms_decisions: dict[str, Any],
    questionnaire_mappings: dict[str, Any],
    policy: dict[str, Any],
    errors: list[str],
    report: list[str],
) -> None:
    package_id = str(package_row["package_id"])
    signal_id = str(package_row.get("signal_id", ""))
    optional_field_policy = policy.get("questionnaire_optional_fields") or {}
    if not isinstance(optional_field_policy, dict):
        optional_field_policy = {}
    optional_dependent_keys = _optional_field_dependent_keys(policy, package_id=package_id)
    library = _load_signal_library(package_id)
    signal = _signal_for_id(library, signal_id)
    if signal is None:
        errors.append(f"{package_id}: signal {signal_id} not found in signal_library.yaml")
        return

    requirements = signal.get("runtime_context_requirements") or {}
    required = requirements.get("required_context")
    if not isinstance(required, list):
        errors.append(f"{package_id}/{signal_id}: missing required_context list")
        return

    report.append(f"[active] {package_id} :: {signal_id} ({len(required)} gates)")
    for gate in required:
        if not isinstance(gate, dict):
            errors.append(f"{package_id}/{signal_id}: invalid gate entry")
            continue
        _validate_disclosure_gate(
            package_id=package_id,
            signal_id=signal_id,
            gate=gate,
            questionnaire_ids=questionnaire_ids,
            absent_keys=absent_keys,
            lifestyle_keys=lifestyle_keys,
            suppress_registry=suppress_registry,
            symptoms_decisions=symptoms_decisions,
            questionnaire_mappings=questionnaire_mappings,
            optional_dependent_keys=optional_dependent_keys,
            optional_field_policy=optional_field_policy,
            errors=errors,
        )


def _validate_evaluator_aas_translation(errors: list[str]) -> None:
    from core.analytics.runtime_context_evaluator import build_runtime_context_snapshot

    cases = (
        (["Vitamin D"], "answered_no"),
        (["Omega-3/Fish Oil"], "answered_no"),
        (["Multivitamin"], "answered_no"),
        (["Iron"], "answered_no"),
        (["prohormone stack"], "answered_yes"),
        (["anabolic steroid"], "answered_yes"),
    )
    for supplements, expected in cases:
        ctx = build_runtime_context_snapshot(
            questionnaire_responses={"supplements": supplements},
        )
        actual = ctx["clinical_context"].get("aas_exposure_status")
        if actual != expected:
            errors.append(
                "evaluator AAS translation: supplements="
                f"{supplements!r} expected aas_exposure_status={expected}, got {actual!r}"
            )

    ctx_unanswered = build_runtime_context_snapshot()
    if ctx_unanswered["clinical_context"].get("aas_exposure_status") != "not_answered":
        errors.append("evaluator AAS translation: unanswered supplements must be not_answered")


def _validate_symptoms_gate_policy(
    policy: dict[str, Any],
    errors: list[str],
) -> None:
    decisions = policy.get("symptoms_gate_authority_decisions") or {}
    if not isinstance(decisions, dict):
        return
    for package_id, row in decisions.items():
        if not isinstance(row, dict):
            continue
        signal_id = str(row.get("signal_id", "")).strip()
        decision = str(row.get("decision", "")).strip()
        library = _load_signal_library(str(package_id))
        signal = _signal_for_id(library, signal_id)
        if signal is None:
            errors.append(f"symptoms policy: {package_id}/{signal_id} not found")
            continue
        required = (signal.get("runtime_context_requirements") or {}).get("required_context") or []
        has_symptoms_gate = any(
            isinstance(g, dict)
            and g.get("context_type") == "symptom"
            and g.get("key") == "symptoms_status"
            for g in required
        )
        if decision == "downgrade_not_suppress" and has_symptoms_gate:
            errors.append(
                f"{package_id}/{signal_id}: symptoms_status must not be hard gate "
                f"(authority decision={decision})"
            )
        if decision == "required_gate_with_questionnaire_mapping" and not has_symptoms_gate:
            errors.append(
                f"{package_id}/{signal_id}: symptoms_status required gate missing "
                f"(authority decision={decision})"
            )
        if decision == "downgrade_not_suppress" and not str(row.get("authority_citation", "")).strip():
            errors.append(f"{package_id}/{signal_id}: downgrade decision missing authority_citation")


def validate(*, repo_root: Path | None = None) -> tuple[list[str], list[str]]:
    root = repo_root or _REPO
    register = _load_yaml(root / _BATCH2_REGISTER.relative_to(_REPO))
    policy = _load_yaml(root / _POLICY.relative_to(_REPO))
    questionnaire_ids = _load_questionnaire_ids(root / _QUESTIONNAIRE.relative_to(_REPO))
    absent_keys = policy.get("questionnaire_absent_context_keys") or {}
    if not isinstance(absent_keys, dict):
        absent_keys = {}
    lifestyle_raw = policy.get("lifestyle_sourced_context_keys") or {}
    lifestyle_keys = (
        frozenset(str(k) for k in lifestyle_raw.keys())
        if isinstance(lifestyle_raw, dict)
        else frozenset()
    )

    activated = _activated_packages(register)
    expected_count = register.get("activated_package_count")
    if isinstance(expected_count, int) and len(activated) != expected_count:
        return [f"activated package count mismatch: register={expected_count} loaded={len(activated)}"], []

    suppress_registry = _suppress_registry(policy)
    symptoms_decisions = policy.get("symptoms_gate_authority_decisions") or {}
    if not isinstance(symptoms_decisions, dict):
        symptoms_decisions = {}
    questionnaire_mappings = policy.get("questionnaire_field_mappings") or {}
    if not isinstance(questionnaire_mappings, dict):
        questionnaire_mappings = {}
    errors: list[str] = []
    report: list[str] = [f"active_package_count: {len(activated)}"]

    for package_row in activated:
        _validate_package(
            package_row=package_row,
            questionnaire_ids=questionnaire_ids,
            absent_keys=absent_keys,
            lifestyle_keys=lifestyle_keys,
            suppress_registry=suppress_registry,
            symptoms_decisions=symptoms_decisions,
            questionnaire_mappings=questionnaire_mappings,
            policy=policy,
            errors=errors,
            report=report,
        )

    _validate_evaluator_aas_translation(errors)
    _validate_symptoms_gate_policy(policy, errors)

    return errors, report


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate active runtime signal context gate reachability"
    )
    parser.add_argument("--repo-root", type=Path, default=_REPO)
    args = parser.parse_args(argv)

    try:
        errors, report = validate(repo_root=args.repo_root)
    except (OSError, yaml.YAMLError, json.JSONDecodeError) as exc:
        print(f"validation_status: FAIL\nerror: {exc}", file=sys.stderr)
        return 1

    for line in report:
        print(line)

    if errors:
        print("validation_status: FAIL", file=sys.stderr)
        print(f"errors: {len(errors)}", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print("validation_status: PASS")
    print(f"errors: 0")
    print(f"active_packages_checked: {len([l for l in report if l.startswith('[active]')])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
