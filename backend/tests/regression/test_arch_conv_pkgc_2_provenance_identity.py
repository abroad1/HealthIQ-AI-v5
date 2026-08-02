"""ARCH-CONV-PKGC-2 — provenance-identity bare-key / non-frame closure."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from core.analytics.output_authority_provenance_builder_v1 import (
    build_report_output_authority_provenance_v1,
)
from core.analytics.report_compiler_v1 import compile_report_v1
from core.analytics.runtime_context_evaluator import build_runtime_context_snapshot
from core.analytics.signal_evaluator import SignalEvaluator
from core.contracts.report_v1 import ReportActionsV1, ReportMetaV1, ReportTopFindingV1, ReportV1
from core.knowledge.signal_activation_identity_v1 import (
    build_activation_key,
    resolve_activation_identity,
)
from core.knowledge.signal_result_index_v1 import (
    FORBIDDEN_NON_FRAME_ACTIVATION_KEYS,
    parse_activation_key,
    require_activation_key,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
HISTORIC_TRUNCATED_HCY_KEY = "signal_homocysteine_high::inv_homocysteine_high"

LIVE_CANONICAL_KEYS = (
    "signal_homocysteine_high::inv_homocysteine_high_b_vitamin_related_methylation_impairment",
    "signal_homocysteine_high::inv_homocysteine_high_renal_clearance_reduction",
    "signal_fai_high::inv_fai_high_biochemical_hyperandrogenism",
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


def _minimal_report(*, signal_id: str, activation_key: str = "", signal_state: str = "at_risk") -> ReportV1:
    return ReportV1(
        actions=ReportActionsV1(),
        meta=ReportMetaV1(
            signal_registry_version="t",
            signal_registry_hash_sha256="h",
            interaction_map_revision="r",
            safety_contract_version="s",
            generated_at="2026-08-02",
        ),
        top_findings=[
            ReportTopFindingV1(
                priority_rank=1,
                signal_id=signal_id,
                activation_key=activation_key,
                system="test",
                signal_state=signal_state,
                confidence=0.5,
                primary_metric="x",
                why_it_matters="test",
            )
        ],
    )


def test_live_canonical_keys_pass_parse_and_require():
    for key in LIVE_CANONICAL_KEYS:
        sid, spec = parse_activation_key(key)
        assert build_activation_key(signal_id=sid, source_spec_id=spec) == key
        assert require_activation_key({"activation_key": key, "signal_id": sid, "source_spec_id": spec}) == key


def test_historic_truncated_hcy_key_is_forbidden_non_frame():
    assert HISTORIC_TRUNCATED_HCY_KEY in FORBIDDEN_NON_FRAME_ACTIVATION_KEYS
    with pytest.raises(ValueError, match="non-frame"):
        parse_activation_key(HISTORIC_TRUNCATED_HCY_KEY)
    with pytest.raises(ValueError, match="non-frame"):
        require_activation_key(
            {
                "signal_id": "signal_homocysteine_high",
                "activation_key": HISTORIC_TRUNCATED_HCY_KEY,
            }
        )


def test_bare_signal_only_key_rejected():
    with pytest.raises(ValueError, match="signal_id::source_spec_id"):
        parse_activation_key("signal_homocysteine_high")


def test_empty_segments_and_multi_separator_rejected():
    with pytest.raises(ValueError):
        parse_activation_key("signal_x::")
    with pytest.raises(ValueError):
        parse_activation_key("::inv_y")
    with pytest.raises(ValueError):
        parse_activation_key("a::b::c")


def test_require_activation_key_rejects_component_mismatch():
    with pytest.raises(ValueError, match="mismatch"):
        require_activation_key(
            {
                "activation_key": "signal_a::inv_a",
                "signal_id": "signal_b",
                "source_spec_id": "inv_a",
            }
        )


def test_require_activation_key_does_not_alter_canonical_text():
    key = LIVE_CANONICAL_KEYS[0]
    assert require_activation_key({"activation_key": key}) == key


def test_provenance_builder_rejects_historic_truncated_key():
    report = _minimal_report(
        signal_id="signal_homocysteine_high",
        activation_key=HISTORIC_TRUNCATED_HCY_KEY,
    )
    with pytest.raises(ValueError, match="non-frame"):
        build_report_output_authority_provenance_v1(
            signal_results=[
                {
                    "signal_id": "signal_homocysteine_high",
                    "activation_key": HISTORIC_TRUNCATED_HCY_KEY,
                    "signal_state": "at_risk",
                    "primary_metric": "homocysteine",
                    "confidence": 0.8,
                }
            ],
            report=report,
            root_cause=None,
        )


def test_provenance_builder_rejects_bare_signal_only_claimed_key():
    report = _minimal_report(signal_id="signal_free_t3_low", activation_key="signal_free_t3_low")
    with pytest.raises(ValueError, match="signal_id::source_spec_id"):
        build_report_output_authority_provenance_v1(
            signal_results=[
                {
                    "signal_id": "signal_free_t3_low",
                    "activation_key": "signal_free_t3_low",
                    "signal_state": "at_risk",
                    "primary_metric": "free_t3",
                    "confidence": 0.8,
                }
            ],
            report=report,
            root_cause=None,
        )


def test_real_evaluated_canonical_row_produces_provenance():
    signal = _load_package_signal(
        "pkg_kb47_fai_high_biochemical_hyperandrogenism",
        "signal_fai_high",
    )
    ctx = build_runtime_context_snapshot(
        questionnaire_responses={
            "biological_sex": "female",
            "date_of_birth": "1990-01-01",
            "long_term_medications": [],
            "supplements": [],
            "symptoms": ["acne"],
            "pregnancy_status": False,
        }
    )
    lab_ranges = {
        "fai": {"min": 20.0, "max": 70.0},
        "testosterone": {"min": 8.0, "max": 30.0},
        "shbg": {"min": 15.0, "max": 50.0},
    }
    signal_results = _evaluate(
        signal,
        {"fai": 90.0, "testosterone": 40.0, "shbg": 20.0},
        runtime_context=ctx,
        lab_ranges=lab_ranges,
    )
    assert signal_results
    key = signal_results[0]["activation_key"]
    parse_activation_key(key)
    assert key != HISTORIC_TRUNCATED_HCY_KEY
    report = compile_report_v1(
        signal_results=signal_results,
        interaction_summary=[],
        interventions_v1=[],
        signal_registry_version="test",
        signal_registry_hash_sha256="abc",
        biomarker_context={"fai": {"value": 90.0}},
        input_reference_ranges=lab_ranges,
    )
    prov = report.output_authority_provenance_v1
    assert prov is not None
    assert any(e.output_element_type == "signal_card" for e in prov.governed_elements)


def test_producer_and_consumer_share_one_grammar():
    key = build_activation_key(signal_id="signal_x", source_spec_id="inv_x_frame")
    assert key == "signal_x::inv_x_frame"
    assert parse_activation_key(key) == ("signal_x", "inv_x_frame")
