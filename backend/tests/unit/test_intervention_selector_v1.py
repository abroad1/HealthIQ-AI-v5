from pathlib import Path

import pytest
import yaml

from core.analytics.intervention_selector_v1 import (
    select_interventions_v1,
    validate_intervention_payloads,
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _safe_entry(
    intervention_id: str,
    system: str,
    safety_class: str,
    evidence_strength: str = "strong",
) -> dict:
    return {
        "intervention_id": intervention_id,
        "system": system,
        "title": f"Title {intervention_id}"[:80],
        "body": "Use a conservative plan. Repeat follow-up promptly.",
        "why_this_matters": "This intervention links directly to elevated deterministic signal context.",
        "evidence_strength": evidence_strength,
        "evidence_summary": "- Randomized trial, n=200, Journal A, 2020.\n- Cohort study, n=500, Journal B, 2021.",
        "safety_class": safety_class,
    }


def test_safety_contract_artifacts_v101_and_ordering_rules_present():
    root = _repo_root()
    rules_path = root / "knowledge_bus" / "interventions" / "safety_rules_v1.yaml"
    contract_path = root / "knowledge_bus" / "interventions" / "SAFETY_CONTRACT_v1.md"
    rules = yaml.safe_load(rules_path.read_text(encoding="utf-8")) or {}
    contract_text = contract_path.read_text(encoding="utf-8")

    assert rules.get("schema_version") == "1.0.1"
    assert rules.get("contract_version") == "1.0.1"
    assert rules.get("selection_ordering") == [
        "chain_confidence desc",
        "signal_confidence desc",
        "evidence_strength_ordinal desc",
        "intervention_id asc",
    ]
    assert (rules.get("text_limits") or {}).get("why_this_matters_max_chars") == 200
    deny = [str(x).lower() for x in rules.get("denylist_phrases", [])]
    assert "take" not in deny
    assert "treat" not in deny
    for expected in [
        "take medication",
        "take this drug",
        "take the pill",
        "take a supplement",
        "this will treat",
        "we can treat",
        "reverse",
    ]:
        assert expected in deny
    assert "Contract modification governance" in contract_text


def test_library_has_no_exploratory_and_passes_payload_validation():
    root = _repo_root()
    library_path = root / "knowledge_bus" / "interventions" / "intervention_library_v1.yaml"
    rules_path = root / "knowledge_bus" / "interventions" / "safety_rules_v1.yaml"
    library = yaml.safe_load(library_path.read_text(encoding="utf-8")) or {}
    rules = yaml.safe_load(rules_path.read_text(encoding="utf-8")) or {}
    interventions = library.get("interventions") or []

    assert interventions
    assert len(interventions) <= 25
    for row in interventions:
        assert row.get("evidence_strength") in {"moderate", "strong", "consensus"}
    validate_intervention_payloads(interventions, rules)


def test_confidence_gating_suppresses_lifestyle_and_returns_single_fallback_monitoring():
    library = {
        "interventions": [
            _safe_entry("intv_metabolic_lifestyle_v1", "metabolic", "lifestyle"),
            _safe_entry("intv_metabolic_monitoring_v1", "metabolic", "monitoring", "moderate"),
        ]
    }
    rules = {
        "schema_version": "1.0.1",
        "allowed_safety_classes": ["lifestyle", "monitoring", "clinician_referral"],
        "allowed_evidence_strength": ["moderate", "strong", "consensus"],
        "minimum_evidence_strength": "moderate",
        "denylist_phrases": ["take medication", "reverse"],
        "text_limits": {"title_max_chars": 80, "body_max_sentences": 3, "why_this_matters_max_chars": 200},
        "confidence_threshold": 0.40,
        "max_interventions_per_report": 5,
        "max_interventions_per_system": 2,
        "low_confidence_clause": "Some markers needed to fully assess this signal are missing from your panel.",
        "low_confidence_monitoring_fallback": "Insufficient data to generate reliable recommendations. Retest recommended in 8–12 weeks with a complete panel.",
    }
    out = select_interventions_v1(
        signal_results=[
            {"signal_id": "signal_x", "system": "metabolic", "signal_state": "suboptimal", "confidence": 0.20}
        ],
        interaction_summary=[],
        library_payload=library,
        safety_rules=rules,
    )
    assert len(out) == 1
    assert out[0]["safety_class"] == "monitoring"
    assert out[0]["body"] == rules["low_confidence_monitoring_fallback"]


def test_escalation_referral_survives_low_confidence_and_contains_required_clause():
    library = {
        "interventions": [
            _safe_entry("intv_vascular_clinician_referral_v1", "vascular", "clinician_referral", "consensus")
        ]
    }
    rules = {
        "schema_version": "1.0.1",
        "allowed_safety_classes": ["lifestyle", "monitoring", "clinician_referral"],
        "allowed_evidence_strength": ["moderate", "strong", "consensus"],
        "minimum_evidence_strength": "moderate",
        "denylist_phrases": ["take medication", "reverse"],
        "text_limits": {"title_max_chars": 80, "body_max_sentences": 3, "why_this_matters_max_chars": 200},
        "confidence_threshold": 0.40,
        "max_interventions_per_report": 5,
        "max_interventions_per_system": 2,
        "low_confidence_clause": "Some markers needed to fully assess this signal are missing from your panel.",
        "low_confidence_monitoring_fallback": "Insufficient data to generate reliable recommendations. Retest recommended in 8–12 weeks with a complete panel.",
    }
    out = select_interventions_v1(
        signal_results=[
            {"signal_id": "signal_v", "system": "vascular", "signal_state": "at_risk", "confidence": 0.10}
        ],
        interaction_summary=[],
        library_payload=library,
        safety_rules=rules,
    )
    assert len(out) == 1
    assert out[0]["safety_class"] == "clinician_referral"
    assert "Some markers needed to fully assess this signal are missing from your panel." in out[0]["body"]


def test_ordering_respects_chain_then_signal_then_evidence_then_id():
    library = {
        "interventions": [
            _safe_entry("intv_metabolic_alpha_v1", "metabolic", "lifestyle", "strong"),
            _safe_entry("intv_metabolic_beta_v1", "metabolic", "lifestyle", "consensus"),
        ]
    }
    rules = {
        "schema_version": "1.0.1",
        "allowed_safety_classes": ["lifestyle", "monitoring", "clinician_referral"],
        "allowed_evidence_strength": ["moderate", "strong", "consensus"],
        "minimum_evidence_strength": "moderate",
        "denylist_phrases": ["take medication", "reverse"],
        "text_limits": {"title_max_chars": 80, "body_max_sentences": 3, "why_this_matters_max_chars": 200},
        "confidence_threshold": 0.40,
        "max_interventions_per_report": 5,
        "max_interventions_per_system": 2,
        "low_confidence_clause": "Some markers needed to fully assess this signal are missing from your panel.",
        "low_confidence_monitoring_fallback": "Insufficient data to generate reliable recommendations. Retest recommended in 8–12 weeks with a complete panel.",
    }
    signals = [
        {"signal_id": "signal_a", "system": "metabolic", "signal_state": "suboptimal", "confidence": 0.70},
        {"signal_id": "signal_b", "system": "metabolic", "signal_state": "suboptimal", "confidence": 0.90},
    ]
    summary = [
        {"chain_id": "chain_001", "signals_involved": ["signal_a"], "confidence": 0.30},
        {"chain_id": "chain_002", "signals_involved": ["signal_b"], "confidence": 0.80},
    ]
    out = select_interventions_v1(
        signal_results=signals,
        interaction_summary=summary,
        library_payload=library,
        safety_rules=rules,
    )
    # Same library IDs can be attributed to either signal; highest chain/signal context wins.
    assert [x["intervention_id"] for x in out] == ["intv_metabolic_beta_v1", "intv_metabolic_alpha_v1"]


def test_caps_max_five_max_two_per_system_and_referral_priority():
    library = {
        "interventions": [
            _safe_entry("intv_metabolic_lifestyle_v1", "metabolic", "lifestyle"),
            _safe_entry("intv_metabolic_monitoring_v1", "metabolic", "monitoring", "moderate"),
            _safe_entry("intv_metabolic_clinician_referral_v1", "metabolic", "clinician_referral", "consensus"),
            _safe_entry("intv_hepatic_lifestyle_v1", "hepatic", "lifestyle"),
            _safe_entry("intv_hepatic_monitoring_v1", "hepatic", "monitoring", "moderate"),
            _safe_entry("intv_hepatic_clinician_referral_v1", "hepatic", "clinician_referral", "strong"),
            _safe_entry("intv_vascular_clinician_referral_v1", "vascular", "clinician_referral", "consensus"),
        ]
    }
    rules = {
        "schema_version": "1.0.1",
        "allowed_safety_classes": ["lifestyle", "monitoring", "clinician_referral"],
        "allowed_evidence_strength": ["moderate", "strong", "consensus"],
        "minimum_evidence_strength": "moderate",
        "denylist_phrases": ["take medication", "reverse"],
        "text_limits": {"title_max_chars": 80, "body_max_sentences": 3, "why_this_matters_max_chars": 200},
        "confidence_threshold": 0.40,
        "max_interventions_per_report": 5,
        "max_interventions_per_system": 2,
        "low_confidence_clause": "Some markers needed to fully assess this signal are missing from your panel.",
        "low_confidence_monitoring_fallback": "Insufficient data to generate reliable recommendations. Retest recommended in 8–12 weeks with a complete panel.",
    }
    signals = [
        {"signal_id": "signal_m", "system": "metabolic", "signal_state": "at_risk", "confidence": 0.95},
        {"signal_id": "signal_h", "system": "hepatic", "signal_state": "at_risk", "confidence": 0.94},
        {"signal_id": "signal_v", "system": "vascular", "signal_state": "at_risk", "confidence": 0.93},
    ]
    summary = [
        {"chain_id": "chain_001", "signals_involved": ["signal_m"], "confidence": 0.9},
        {"chain_id": "chain_002", "signals_involved": ["signal_h"], "confidence": 0.8},
        {"chain_id": "chain_003", "signals_involved": ["signal_v"], "confidence": 0.7},
    ]
    out = select_interventions_v1(
        signal_results=signals,
        interaction_summary=summary,
        library_payload=library,
        safety_rules=rules,
    )
    assert len(out) <= 5
    per_system = {}
    for row in out:
        system = row["intervention_id"].split("_")[1]
        per_system[system] = per_system.get(system, 0) + 1
    assert all(v <= 2 for v in per_system.values())
    assert any(row["safety_class"] == "clinician_referral" for row in out)


def test_denylist_enforced_on_template_text():
    rules = {
        "allowed_safety_classes": ["lifestyle", "monitoring", "clinician_referral"],
        "allowed_evidence_strength": ["moderate", "strong", "consensus"],
        "minimum_evidence_strength": "moderate",
        "denylist_phrases": ["take medication", "reverse"],
        "text_limits": {"title_max_chars": 80, "body_max_sentences": 3, "why_this_matters_max_chars": 200},
    }
    bad = [
        {
            "intervention_id": "intv_bad_v1",
            "title": "Bad Title",
            "body": "Please take medication immediately.",
            "why_this_matters": "Reason text.",
            "evidence_summary": "- Cohort, n=50, Journal, 2020.\n- Trial, n=100, Journal, 2021.",
            "safety_class": "monitoring",
            "evidence_strength": "moderate",
        }
    ]
    with pytest.raises(ValueError, match="denylist phrase"):
        validate_intervention_payloads(bad, rules)
