"""
Sprint 22 — Layer 3 Insight Assembler unit tests.
"""

from pathlib import Path

import pytest

from core.layer3.insight_assembler_v1 import assemble_layer3_insights
from core.contracts.layer3_insights_v1 import (
    LAYER3_INSIGHTS_SCHEMA_VERSION,
    SYSTEM_CARD_IDS,
)
from core.canonical.normalize import normalize_biomarkers_with_metadata
from core.pipeline.orchestrator import AnalysisOrchestrator, UNIT_NORMALISATION_META_KEY
from core.units.registry import UNIT_REGISTRY_VERSION, apply_unit_normalisation

from tools.run_golden_panel import (
    _filter_unit_registry_supported,
    _coerce_to_ssot_units,
    run_golden_panel,
)


def _empty_session():
    class _Empty:
        def query(self, *args, **kwargs):
            return self

        def join(self, *args, **kwargs):
            return self

        def filter(self, *args, **kwargs):
            return self

        def all(self):
            return []

    return _Empty()


def _prepare_biomarkers(biomarkers: dict) -> dict:
    normalized = normalize_biomarkers_with_metadata(biomarkers)
    filtered = _filter_unit_registry_supported(normalized)
    coerced = _coerce_to_ssot_units(filtered)
    result = apply_unit_normalisation(coerced)
    result[UNIT_NORMALISATION_META_KEY] = {
        "unit_normalised": True,
        "unit_registry_version": UNIT_REGISTRY_VERSION,
    }
    return result


def _collision_free_fixture() -> Path:
    return Path(__file__).parent.parent / "fixtures" / "golden_panel_160_collision_free.json"


def _lifestyle_minimal_fixture() -> Path:
    return Path(__file__).parent.parent / "fixtures" / "lifestyle_minimal.json"


class _EmptySession:
    def query(self, *args, **kwargs):
        return self

    def join(self, *args, **kwargs):
        return self

    def filter(self, *args, **kwargs):
        return self

    def all(self):
        return []


@pytest.fixture
def dto_no_lifestyle(tmp_path):
    import json
    fixture = _collision_free_fixture()
    payload = json.loads(fixture.read_text())
    biomarkers = _prepare_biomarkers(payload["biomarkers"])
    orchestrator = AnalysisOrchestrator(db_session=_EmptySession(), allow_llm=False)
    return orchestrator.run(
        biomarkers,
        payload["user"],
        assume_canonical=True,
        lifestyle_inputs=None,
    )


@pytest.fixture
def dto_with_lifestyle(tmp_path):
    import json
    fixture = _collision_free_fixture()
    lifestyle_path = _lifestyle_minimal_fixture()
    payload = json.loads(fixture.read_text())
    biomarkers = _prepare_biomarkers(payload["biomarkers"])
    lifestyle_inputs = json.loads(lifestyle_path.read_text()) if lifestyle_path.exists() else None
    orchestrator = AnalysisOrchestrator(db_session=_EmptySession(), allow_llm=False)
    return orchestrator.run(
        biomarkers,
        payload["user"],
        assume_canonical=True,
        lifestyle_inputs=lifestyle_inputs,
    )


def test_determinism_twice_same_dto(dto_no_lifestyle):
    """Assemble twice from same dto; model_dump must be identical."""
    out1 = assemble_layer3_insights(dto_no_lifestyle)
    out2 = assemble_layer3_insights(dto_no_lifestyle)
    assert out1.model_dump(mode="json") == out2.model_dump(mode="json")


def test_exactly_10_cards(dto_no_lifestyle):
    """Exactly 10 insight cards must exist."""
    out = assemble_layer3_insights(dto_no_lifestyle)
    assert len(out.insights) == 10
    ids = [c.insight_id for c in out.insights]
    assert sorted(ids) == sorted(SYSTEM_CARD_IDS)


def test_ordering_action_watch_info_then_alphabetical(dto_no_lifestyle):
    """action cards first, then watch, then info; within same severity alphabetical system_id."""
    out = assemble_layer3_insights(dto_no_lifestyle)
    prev_rank = -1
    prev_system = ""
    for c in out.insights:
        rank = {"action": 0, "watch": 1, "info": 2}.get(c.severity, 3)
        assert rank >= prev_rank
        if rank == prev_rank:
            assert c.system_id >= prev_system
        prev_rank = rank
        prev_system = c.system_id


def test_no_timestamps_in_output(dto_no_lifestyle):
    """Assert no keys containing time, timestamp, created, generated in output."""
    out = assemble_layer3_insights(dto_no_lifestyle)
    d = out.model_dump(mode="json")

    def check_no_time(obj, path=""):
        if isinstance(obj, dict):
            for k, v in obj.items():
                kl = k.lower()
                assert "time" not in kl and "timestamp" not in kl and "created" not in kl and "generated" not in kl, (
                    f"Found time-related key: {path}.{k}"
                )
                check_no_time(v, f"{path}.{k}")
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                check_no_time(item, f"{path}[{i}]")

    check_no_time(d)


def test_schema_version_exactly_1_0_0(dto_no_lifestyle):
    """Layer3InsightsV1.schema_version must be exactly 1.0.0."""
    out = assemble_layer3_insights(dto_no_lifestyle)
    assert out.schema_version == "1.0.0"
    assert out.schema_version == LAYER3_INSIGHTS_SCHEMA_VERSION


def test_without_lifestyle_no_lifestyle_evidence(dto_no_lifestyle):
    """Without lifestyle, no insight card has lifestyle evidence block."""
    out = assemble_layer3_insights(dto_no_lifestyle)
    for c in out.insights:
        ev = c.evidence.lifestyle
        assert ev is None or len(ev) == 0


def test_with_lifestyle_has_lifestyle_evidence(dto_with_lifestyle):
    """With lifestyle, at least one card has lifestyle evidence."""
    out = assemble_layer3_insights(dto_with_lifestyle)
    has_lifestyle = False
    for c in out.insights:
        if c.evidence.lifestyle and len(c.evidence.lifestyle) > 0:
            has_lifestyle = True
            break
    assert has_lifestyle, "Expected at least one card with lifestyle evidence when lifestyle provided"
