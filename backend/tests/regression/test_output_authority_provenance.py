"""Regression tests for ARCH-COMPLETION-2 output authority provenance."""

from __future__ import annotations

from pathlib import Path

import yaml

from core.analytics.output_authority_provenance_builder_v1 import (
    build_report_output_authority_provenance_v1,
    is_governed_hypothesis,
)
from core.analytics.report_compiler_v1 import compile_report_v1
from core.analytics.runtime_context_evaluator import build_runtime_context_snapshot
from core.analytics.signal_evaluator import SignalEvaluator
from core.knowledge.compiled_output_authority_v1 import (
    WHY_ENGINE_FALLBACK_HYPOTHESIS_ID,
    load_compiled_output_authority_model,
)
from core.knowledge.signal_activation_identity_v1 import resolve_activation_identity

REPO_ROOT = Path(__file__).resolve().parents[3]

ANDROGEN_LAB_RANGES = {
    "fai": {"min": 20.0, "max": 70.0},
    "testosterone": {"min": 8.0, "max": 30.0},
    "shbg": {"min": 15.0, "max": 50.0},
    "free_testosterone": {"min": 5.0, "max": 25.0},
}


def _female_androgen_context(*, hormone_therapy: bool = False, pregnant: bool = False):
    return build_runtime_context_snapshot(
        questionnaire_responses={
            "biological_sex": "female",
            "date_of_birth": "1990-01-01",
            "long_term_medications": ["Testosterone replacement"] if hormone_therapy else [],
            "supplements": [],
            "symptoms": ["acne"],
            "pregnancy_status": pregnant,
        }
    )


def _adult_male_low_context(*, hormone_therapy: bool = False):
    return build_runtime_context_snapshot(
        questionnaire_responses={
            "biological_sex": "male",
            "date_of_birth": "1985-01-01",
            "long_term_medications": ["Testosterone replacement"] if hormone_therapy else [],
            "supplements": [],
            "symptoms": ["fatigue"],
            "chronic_conditions": [],
        },
        lifestyle_factors={"calorie_restriction": False, "fasting": False},
    )


def _compile_androgen_report(signal_id: str, package_dir: str, biomarkers: dict, *, runtime_context, lab_ranges=None):
    signal = _load_package_signal(package_dir, signal_id)
    signal_results = _evaluate(
        signal,
        biomarkers,
        runtime_context=runtime_context,
        lab_ranges=lab_ranges or ANDROGEN_LAB_RANGES,
    )
    return compile_report_v1(
        signal_results=[row for row in signal_results],
        interaction_summary=[],
        interventions_v1=[],
        signal_registry_version="test",
        signal_registry_hash_sha256="abc",
        biomarker_context={k: {"value": v} for k, v in biomarkers.items()},
        input_reference_ranges=lab_ranges or ANDROGEN_LAB_RANGES,
    ), signal_results


def _signal_card_for(report, signal_id: str):
    prov = report.output_authority_provenance_v1
    assert prov is not None
    return next(
        (
            e
            for e in prov.governed_elements
            if e.output_element_type == "signal_card" and signal_id in (e.source_signal_ids or [])
        ),
        None,
    )


class _SingleSignalRegistry:
    def __init__(self, signal: dict) -> None:
        self._signal = dict(signal)

    def get_all_signals(self) -> list[dict]:
        return [dict(self._signal)]


def _load_package_signal(package_dir: str, signal_id: str) -> dict:
    path = REPO_ROOT / "knowledge_bus" / "packages" / package_dir / "signal_library.yaml"
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    for item in payload.get("signals", []):
        if item.get("signal_id") == signal_id:
            activation_key, source_spec_id, package_id = resolve_activation_identity(
                signal_id=signal_id,
                signal_library_path=path,
            )
            compiled = dict(item)
            compiled["activation_key"] = activation_key
            compiled["source_spec_id"] = source_spec_id
            compiled["package_id"] = package_id
            compiled["system"] = compiled.get("system") or "hormonal"
            return compiled
    raise AssertionError(f"signal {signal_id} not found")


def _evaluate(signal: dict, biomarkers: dict[str, float], *, runtime_context=None, lab_ranges=None):
    evaluator = SignalEvaluator(_SingleSignalRegistry(signal))
    rows = evaluator.evaluate_all(
        signal_biomarkers=biomarkers,
        signal_derived={},
        lab_ranges=lab_ranges or {},
        runtime_context=runtime_context,
    )
    return [row.model_dump() for row in rows]


def test_report_includes_output_authority_provenance():
    signal_results = [
        {
            "signal_id": "signal_homocysteine_high",
            "package_id": "pkg_s24_homocysteine_high",
            "activation_key": "signal_homocysteine_high::inv_homocysteine_high",
            "system": "cardiovascular",
            "signal_state": "at_risk",
            "confidence": 0.8,
            "confidence_reasons": [],
            "primary_metric": "homocysteine",
            "supporting_markers": [],
        }
    ]
    report = compile_report_v1(
        signal_results=signal_results,
        interaction_summary=[],
        interventions_v1=[],
        signal_registry_version="test",
        signal_registry_hash_sha256="abc",
        biomarker_context={"homocysteine": {"value": 15.0}},
        input_reference_ranges={"homocysteine": {"min": 5.0, "max": 12.0}},
    )
    prov = report.output_authority_provenance_v1
    assert prov is not None
    assert prov.governed_elements
    assert all(element.authority_status for element in prov.governed_elements)


def test_why_engine_fallback_quarantined_not_governed_hypothesis():
    assert not is_governed_hypothesis(WHY_ENGINE_FALLBACK_HYPOTHESIS_ID)


def test_ft3_low_active_signal_produces_traceable_signal_card():
    signal = _load_package_signal("pkg_kb47_free_t3_low_low_t3_syndrome", "signal_free_t3_low")
    ctx = build_runtime_context_snapshot(
        questionnaire_responses={
            "long_term_medications": [],
            "chronic_conditions": [],
            "pregnancy_status": False,
        },
        lifestyle_factors={"calorie_restriction": False, "fasting": False},
    )
    lab_ranges = {
        "free_t3": {"min": 2.0, "max": 4.4},
        "tsh": {"min": 0.4, "max": 4.5},
        "free_t4": {"min": 0.8, "max": 1.8},
    }
    signal_results = _evaluate(
        signal,
        {"free_t3": 1.5, "tsh": 2.0, "free_t4": 1.2},
        runtime_context=ctx,
        lab_ranges=lab_ranges,
    )
    assert signal_results
    report = compile_report_v1(
        signal_results=signal_results,
        interaction_summary=[],
        interventions_v1=[],
        signal_registry_version="test",
        signal_registry_hash_sha256="abc",
        biomarker_context={"free_t3": {"value": 1.5}, "tsh": {"value": 2.0}, "free_t4": {"value": 1.2}},
        input_reference_ranges=lab_ranges,
    )
    prov = report.output_authority_provenance_v1
    assert prov is not None
    signal_cards = [e for e in prov.governed_elements if e.output_element_type == "signal_card"]
    assert signal_cards
    assert "signal_free_t3_low" in signal_cards[0].source_signal_ids


def test_dhea_high_inactive_produces_no_signal_card():
    signal = _load_package_signal("pkg_kb47_dhea_high_androgen_excess_context", "signal_dhea_high")
    ctx = build_runtime_context_snapshot(
        questionnaire_responses={
            "biological_sex": "female",
            "date_of_birth": "1990-01-01",
            "supplements": [],
            "long_term_medications": [],
        }
    )
    signal_results = _evaluate(signal, {"dhea": 20.0}, runtime_context=ctx, lab_ranges={"dhea": {"min": 1.0, "max": 10.0}})
    assert signal_results == []
    report = compile_report_v1(
        signal_results=signal_results,
        interaction_summary=[],
        interventions_v1=[],
        signal_registry_version="test",
        signal_registry_hash_sha256="abc",
    )
    prov = report.output_authority_provenance_v1
    assert prov is not None
    assert not [e for e in prov.governed_elements if e.output_element_type == "signal_card"]


_ANDROGEN_BIOMARKERS = {"fai": 90.0, "testosterone": 40.0, "shbg": 20.0}
_FT_HIGH_BIOMARKERS = {"free_testosterone": 30.0, "testosterone": 40.0, "shbg": 20.0}
_FT_LOW_BIOMARKERS = {"free_testosterone": 3.0, "testosterone": 5.0, "shbg": 40.0}


def test_fai_high_active_produces_governed_signal_card_provenance():
    report, signal_results = _compile_androgen_report(
        "signal_fai_high",
        "pkg_kb47_fai_high_biochemical_hyperandrogenism",
        _ANDROGEN_BIOMARKERS,
        runtime_context=_female_androgen_context(),
    )
    assert signal_results
    card = _signal_card_for(report, "signal_fai_high")
    assert card is not None
    assert card.authority_status == "CARD_GOVERNED_ACTIVE"


def test_fai_high_suppressed_produces_no_governed_signal_card():
    report, signal_results = _compile_androgen_report(
        "signal_fai_high",
        "pkg_kb47_fai_high_biochemical_hyperandrogenism",
        _ANDROGEN_BIOMARKERS,
        runtime_context=_female_androgen_context(hormone_therapy=True),
    )
    assert signal_results == []
    assert _signal_card_for(report, "signal_fai_high") is None


def test_free_testosterone_high_active_produces_governed_signal_card_provenance():
    report, signal_results = _compile_androgen_report(
        "signal_free_testosterone_high",
        "pkg_kb47_free_testosterone_high_androgen_excess_context",
        _FT_HIGH_BIOMARKERS,
        runtime_context=_female_androgen_context(),
    )
    assert signal_results
    card = _signal_card_for(report, "signal_free_testosterone_high")
    assert card is not None
    assert card.authority_status == "CARD_GOVERNED_ACTIVE"


def test_free_testosterone_high_suppressed_produces_no_governed_signal_card():
    report, signal_results = _compile_androgen_report(
        "signal_free_testosterone_high",
        "pkg_kb47_free_testosterone_high_androgen_excess_context",
        _FT_HIGH_BIOMARKERS,
        runtime_context=_female_androgen_context(pregnant=True),
    )
    assert signal_results == []
    assert _signal_card_for(report, "signal_free_testosterone_high") is None


def test_free_testosterone_low_active_produces_governed_signal_card_provenance():
    report, signal_results = _compile_androgen_report(
        "signal_free_testosterone_low",
        "pkg_kb47_free_testosterone_low_androgen_deficiency_context",
        _FT_LOW_BIOMARKERS,
        runtime_context=_adult_male_low_context(),
    )
    assert signal_results
    card = _signal_card_for(report, "signal_free_testosterone_low")
    assert card is not None
    assert card.authority_status == "CARD_GOVERNED_ACTIVE"


def test_free_testosterone_low_suppressed_produces_no_governed_signal_card():
    report, signal_results = _compile_androgen_report(
        "signal_free_testosterone_low",
        "pkg_kb47_free_testosterone_low_androgen_deficiency_context",
        _FT_LOW_BIOMARKERS,
        runtime_context=_adult_male_low_context(hormone_therapy=True),
    )
    assert signal_results == []
    assert _signal_card_for(report, "signal_free_testosterone_low") is None


def test_runtime_does_not_read_raw_pass3_json():
    backend_core = REPO_ROOT / "backend" / "core"
    forbidden = "Batch_2_Pass_3.json"
    hits = []
    for path in backend_core.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        if forbidden in text and "forbidden" not in text.lower():
            hits.append(str(path.relative_to(REPO_ROOT)))
    assert hits == []


def test_compiled_output_authority_model_forbids_raw_research():
    model = load_compiled_output_authority_model()
    forbidden = model.get("forbidden_compiler_inputs") or []
    assert "Batch_2_Pass_3.json" in forbidden


def test_provenance_builder_classifies_quarantined_fallback():
    from core.contracts.report_v1 import ReportActionsV1, ReportMetaV1, ReportTopFindingV1, ReportV1
    from core.contracts.root_cause_v1 import RootCauseFindingV1, RootCauseHypothesisV1, RootCauseV1

    report = ReportV1(
        actions=ReportActionsV1(),
        meta=ReportMetaV1(
            signal_registry_version="t",
            signal_registry_hash_sha256="h",
            interaction_map_revision="r",
            safety_contract_version="s",
            generated_at="2026-06-14",
        ),
        top_findings=[
            ReportTopFindingV1(
                priority_rank=1,
                signal_id="signal_unknown_lead",
                system="test",
                signal_state="at_risk",
                confidence=0.5,
                primary_metric="x",
                why_it_matters="test",
            )
        ],
        root_cause_v1=RootCauseV1(
            findings=[
                RootCauseFindingV1(
                    signal_id="signal_unknown_lead",
                    primary_metric="x",
                    signal_state="at_risk",
                    signal_confidence=0.5,
                    hypotheses=[
                        RootCauseHypothesisV1(
                            hypothesis_id=WHY_ENGINE_FALLBACK_HYPOTHESIS_ID,
                            title="fallback",
                            summary="fallback summary",
                            hypothesis_confidence=0.0,
                            safety_class="informational",
                        )
                    ],
                )
            ]
        ),
    )
    prov = build_report_output_authority_provenance_v1(
        signal_results=[
            {
                "signal_id": "signal_unknown_lead",
                "signal_state": "at_risk",
                "primary_metric": "x",
                "confidence": 0.5,
            }
        ],
        report=report,
        root_cause=report.root_cause_v1,
    )
    assert prov.quarantined_elements
    assert any(
        e.authority_status == "ROOT_CAUSE_UNTRACEABLE_BLOCKED" for e in prov.quarantined_elements
    )
