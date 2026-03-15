"""
KB-S31 deterministic intervention selector.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

EVIDENCE_ORDER = {"exploratory": 1, "moderate": 2, "strong": 3, "consensus": 4}
ESCALATION_SYSTEMS = {"vascular", "hepatic", "renal"}


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


@lru_cache(maxsize=1)
def load_safety_rules_v1() -> Dict[str, Any]:
    path = _repo_root() / "knowledge_bus" / "interventions" / "safety_rules_v1.yaml"
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if payload.get("schema_version") != "1.0.1":
        raise ValueError("safety_rules_v1.yaml must declare schema_version: 1.0.1")
    return payload


@lru_cache(maxsize=1)
def load_intervention_library_v1() -> Dict[str, Any]:
    path = _repo_root() / "knowledge_bus" / "interventions" / "intervention_library_v1.yaml"
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    interventions = payload.get("interventions")
    if not isinstance(interventions, list):
        raise ValueError("intervention_library_v1.yaml must contain interventions list")
    return payload


def _sentence_count(text: str) -> int:
    return len([s for s in text.replace("?", ".").replace("!", ".").split(".") if s.strip()])


def _contains_deny_phrase(text: str, denylist: List[str]) -> Optional[str]:
    lowered = text.lower()
    for phrase in denylist:
        if phrase.lower() in lowered:
            return phrase
    return None


def validate_intervention_payloads(
    interventions: List[Dict[str, Any]],
    safety_rules: Optional[Dict[str, Any]] = None,
) -> None:
    rules = safety_rules or load_safety_rules_v1()
    denylist = [str(x) for x in rules.get("denylist_phrases", [])]
    title_max = int((rules.get("text_limits") or {}).get("title_max_chars", 80))
    body_max_sentences = int((rules.get("text_limits") or {}).get("body_max_sentences", 3))
    why_max = int((rules.get("text_limits") or {}).get("why_this_matters_max_chars", 200))
    allowed_strength = set(rules.get("allowed_evidence_strength", []))
    allowed_class = set(rules.get("allowed_safety_classes", []))
    min_strength = str(rules.get("minimum_evidence_strength", "moderate"))
    min_rank = EVIDENCE_ORDER.get(min_strength, 2)

    for entry in interventions:
        for field in ("intervention_id", "title", "body", "why_this_matters", "evidence_summary", "safety_class", "evidence_strength"):
            if not isinstance(entry.get(field), str) or not str(entry.get(field)).strip():
                raise ValueError(f"Intervention missing required field: {field}")

        if len(entry["title"]) > title_max:
            raise ValueError(f"title exceeds max length: {entry['intervention_id']}")
        if _sentence_count(entry["body"]) > body_max_sentences:
            raise ValueError(f"body exceeds sentence limit: {entry['intervention_id']}")
        if len(entry["why_this_matters"]) > why_max:
            raise ValueError(f"why_this_matters exceeds max length: {entry['intervention_id']}")
        if entry["evidence_strength"] not in allowed_strength:
            raise ValueError(f"invalid evidence_strength: {entry['intervention_id']}")
        if EVIDENCE_ORDER.get(entry["evidence_strength"], 0) < min_rank:
            raise ValueError(f"evidence strength below floor: {entry['intervention_id']}")
        if entry["safety_class"] not in allowed_class:
            raise ValueError(f"invalid safety_class: {entry['intervention_id']}")
        if "\n- " not in entry["evidence_summary"]:
            raise ValueError(f"evidence_summary must contain 2-3 bullet lines: {entry['intervention_id']}")
        if "n=" not in entry["evidence_summary"]:
            raise ValueError(f"evidence_summary must include sample size n=: {entry['intervention_id']}")

        for text_field in ("title", "body", "why_this_matters", "evidence_summary"):
            deny = _contains_deny_phrase(str(entry.get(text_field, "")), denylist)
            if deny:
                raise ValueError(f"denylist phrase '{deny}' found in {text_field}: {entry['intervention_id']}")


def _requires_escalation(signal_state: str, system: str) -> bool:
    if signal_state == "at_risk":
        return True
    return signal_state == "suboptimal" and system in ESCALATION_SYSTEMS


def _signal_chain_context(
    signal_id: str,
    interaction_summary: List[Dict[str, Any]],
) -> Tuple[float, List[str]]:
    refs: List[Tuple[float, str]] = []
    for item in interaction_summary:
        if not isinstance(item, dict):
            continue
        signals = item.get("signals_involved")
        if not isinstance(signals, list):
            continue
        if signal_id not in signals:
            continue
        chain_id = str(item.get("chain_id", "")).strip()
        conf = item.get("confidence")
        if not isinstance(conf, (int, float)):
            conf = 0.0
        if chain_id:
            refs.append((float(conf), chain_id))
    if not refs:
        return 0.0, []
    refs.sort(key=lambda x: (-x[0], x[1]))
    return refs[0][0], [refs[0][1]]


def _build_candidate(
    *,
    template: Dict[str, Any],
    signal_row: Dict[str, Any],
    chain_confidence: float,
    chain_refs: List[str],
    low_confidence_clause: str,
) -> Dict[str, Any]:
    signal_id = str(signal_row.get("signal_id", "")).strip()
    signal_state = str(signal_row.get("signal_state", "")).strip()
    system = str(signal_row.get("system", "")).strip()
    signal_conf = signal_row.get("confidence")
    if not isinstance(signal_conf, (int, float)):
        signal_conf = 0.0
    escalation_required = _requires_escalation(signal_state, system)
    body = str(template.get("body", "")).strip()
    if template.get("safety_class") == "clinician_referral" and signal_conf < 0.40:
        if low_confidence_clause not in body:
            body = f"{body} {low_confidence_clause}".strip()
    return {
        "intervention_id": template["intervention_id"],
        "title": template["title"],
        "body": body,
        "why_this_matters": f"{template['why_this_matters']} (signal: {signal_id}).",
        "signal_refs": [signal_id],
        "chain_refs": chain_refs,
        "evidence_strength": template["evidence_strength"],
        "evidence_summary": template["evidence_summary"],
        "safety_class": template["safety_class"],
        "escalation_required": escalation_required,
        "contraindications": template.get("contraindications") or [],
        "retest_guidance": template.get("retest_guidance"),
        "_system": system,
        "_signal_confidence": float(signal_conf),
        "_chain_confidence": float(chain_confidence),
    }


def select_interventions_v1(
    *,
    signal_results: List[Dict[str, Any]],
    interaction_summary: Optional[List[Dict[str, Any]]] = None,
    interaction_chains: Optional[List[List[str]]] = None,  # reserved for future parity use
    library_payload: Optional[Dict[str, Any]] = None,
    safety_rules: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    del interaction_chains  # explicit: v1 selection relies on interaction_summary chain metadata
    rules = safety_rules or load_safety_rules_v1()
    library = library_payload or load_intervention_library_v1()
    templates: List[Dict[str, Any]] = [x for x in (library.get("interventions") or []) if isinstance(x, dict)]
    validate_intervention_payloads(templates, rules)

    threshold = float(rules.get("confidence_threshold", 0.40))
    max_total = int(rules.get("max_interventions_per_report", 5))
    max_per_system = int(rules.get("max_interventions_per_system", 2))
    low_confidence_clause = str(rules.get("low_confidence_clause", "")).strip()
    fallback_text = str(rules.get("low_confidence_monitoring_fallback", "")).strip()

    interaction_summary = interaction_summary or []

    candidates: List[Dict[str, Any]] = []
    low_confidence_detected = False
    for row in signal_results:
        if not isinstance(row, dict):
            continue
        signal_id = str(row.get("signal_id", "")).strip()
        system = str(row.get("system", "")).strip()
        signal_state = str(row.get("signal_state", "")).strip()
        signal_conf = row.get("confidence")
        if not isinstance(signal_conf, (int, float)):
            signal_conf = 0.0

        if signal_state not in {"suboptimal", "at_risk"}:
            continue
        escalation_required = _requires_escalation(signal_state, system)
        if signal_conf < threshold and not escalation_required:
            low_confidence_detected = True

        chain_conf, chain_refs = _signal_chain_context(signal_id, interaction_summary)
        for template in templates:
            if str(template.get("system", "")).strip() != system:
                continue
            safety_class = str(template.get("safety_class", "")).strip()
            if safety_class == "clinician_referral":
                if not escalation_required:
                    continue
            else:
                if signal_conf < threshold:
                    continue
            candidate = _build_candidate(
                template=template,
                signal_row=row,
                chain_confidence=chain_conf,
                chain_refs=chain_refs,
                low_confidence_clause=low_confidence_clause,
            )
            candidates.append(candidate)

    # Deduplicate intervention IDs (attribution to highest-confidence chain context).
    dedup: Dict[str, Dict[str, Any]] = {}
    for c in candidates:
        existing = dedup.get(c["intervention_id"])
        if existing is None:
            dedup[c["intervention_id"]] = c
            continue
        c_key = (-c["_chain_confidence"], -c["_signal_confidence"], -EVIDENCE_ORDER[c["evidence_strength"]], c["intervention_id"])
        e_key = (-existing["_chain_confidence"], -existing["_signal_confidence"], -EVIDENCE_ORDER[existing["evidence_strength"]], existing["intervention_id"])
        if c_key < e_key:
            dedup[c["intervention_id"]] = c
    ordered = sorted(
        dedup.values(),
        key=lambda c: (
            -c["_chain_confidence"],
            -c["_signal_confidence"],
            -EVIDENCE_ORDER[c["evidence_strength"]],
            c["intervention_id"],
        ),
    )

    referrals = [c for c in ordered if c["safety_class"] == "clinician_referral"]
    non_referrals = [c for c in ordered if c["safety_class"] != "clinician_referral"]
    selected: List[Dict[str, Any]] = []
    per_system: Dict[str, int] = {}

    # Referrals first (safety priority), still deterministic.
    for c in referrals:
        if len(selected) >= max_total:
            break
        system = c["_system"]
        if per_system.get(system, 0) >= max_per_system:
            continue
        selected.append(c)
        per_system[system] = per_system.get(system, 0) + 1

    for c in non_referrals:
        if len(selected) >= max_total:
            break
        system = c["_system"]
        if per_system.get(system, 0) >= max_per_system:
            continue
        selected.append(c)
        per_system[system] = per_system.get(system, 0) + 1

    if not selected and low_confidence_detected:
        selected.append(
            {
                "intervention_id": "intv_general_monitoring_low_confidence_v1",
                "title": "Low-confidence monitoring follow-up",
                "body": fallback_text,
                "why_this_matters": "Low-confidence signal context needs repeat data before reliable intervention prioritization.",
                "signal_refs": [],
                "chain_refs": [],
                "evidence_strength": "moderate",
                "evidence_summary": "- Laboratory monitoring framework, n=980, Clinical Chemistry, 2019.\n- Repeat-testing reliability study, n=410, Annals of Laboratory Medicine, 2022.",
                "safety_class": "monitoring",
                "escalation_required": False,
                "contraindications": [],
                "retest_guidance": "Retest in 8–12 weeks with a complete panel.",
            }
        )

    result: List[Dict[str, Any]] = []
    for c in selected:
        row = {
            "intervention_id": c["intervention_id"],
            "title": c["title"],
            "body": c["body"],
            "why_this_matters": c["why_this_matters"][:200],
            "signal_refs": c.get("signal_refs", []),
            "chain_refs": c.get("chain_refs", []),
            "evidence_strength": c["evidence_strength"],
            "evidence_summary": c["evidence_summary"],
            "safety_class": c["safety_class"],
            "escalation_required": bool(c.get("escalation_required", False)),
        }
        contraindications = c.get("contraindications")
        if isinstance(contraindications, list) and contraindications:
            row["contraindications"] = [str(x) for x in contraindications if str(x).strip()]
        retest = c.get("retest_guidance")
        if isinstance(retest, str) and retest.strip():
            row["retest_guidance"] = retest.strip()
        result.append(row)

    validate_intervention_payloads(result, rules)
    return result
