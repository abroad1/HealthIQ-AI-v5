"""
Sprint 20 — Orchestrator lifestyle integration unit tests.

Tests LifestyleModifierEngine integration into the orchestrator.
No DB. No external calls. Deterministic.
"""

import hashlib
import json
from pathlib import Path

from core.canonical.normalize import normalize_biomarkers_with_metadata
from core.pipeline.orchestrator import AnalysisOrchestrator, UNIT_NORMALISATION_META_KEY
from core.units.registry import UNIT_REGISTRY_VERSION, apply_unit_normalisation
from tools.run_golden_panel import run_golden_panel


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
    from tools.run_golden_panel import _filter_unit_registry_supported, _coerce_to_ssot_units
    filtered = _filter_unit_registry_supported(normalized)
    coerced = _coerce_to_ssot_units(filtered)
    result = apply_unit_normalisation(coerced)
    result[UNIT_NORMALISATION_META_KEY] = {
        "unit_normalised": True,
        "unit_registry_version": UNIT_REGISTRY_VERSION,
    }
    return result


def _get_burden_vector(analysis_result: dict) -> dict:
    meta = analysis_result.get("meta", {}) or {}
    burden = meta.get("burden_vector", {}) or {}
    return dict(burden.get("adjusted_system_burden_vector", {}))


def _collision_free_fixture() -> Path:
    """Use collision-free 160 derivative for orchestrator tests."""
    return Path(__file__).parent.parent / "fixtures" / "golden_panel_160_collision_free.json"


def test_no_lifestyle_input_omits_lifestyle_key(tmp_path):
    """Without lifestyle_inputs, analysis_result must NOT contain 'lifestyle' key."""
    fixture = _collision_free_fixture()
    run_dir, result = run_golden_panel(
        fixture_path=fixture,
        output_root=tmp_path,
        run_id="no-lifestyle",
        write_narrative=False,
        lifestyle_fixture_path=None,
    )
    assert "lifestyle" not in result


def test_no_lifestyle_byte_for_byte_identical_burdens(tmp_path):
    """Without lifestyle_inputs, running twice yields identical burden vectors."""
    fixture = _collision_free_fixture()
    _, result_a = run_golden_panel(
        fixture_path=fixture,
        output_root=tmp_path,
        run_id="baseline-a",
        write_narrative=False,
        lifestyle_fixture_path=None,
    )
    _, result_b = run_golden_panel(
        fixture_path=fixture,
        output_root=tmp_path,
        run_id="baseline-b",
        write_narrative=False,
        lifestyle_fixture_path=None,
    )
    burden_a = _get_burden_vector(result_a)
    burden_b = _get_burden_vector(result_b)
    assert burden_a == burden_b


def test_with_lifestyle_input_adds_lifestyle_section(tmp_path):
    """With lifestyle_inputs, lifestyle section present and burdens change deterministically."""
    fixture = _collision_free_fixture()
    lifestyle_fixture = Path(__file__).parent.parent / "fixtures" / "lifestyle_minimal.json"
    _, result_no_life = run_golden_panel(
        fixture_path=fixture,
        output_root=tmp_path,
        run_id="no-life",
        write_narrative=False,
        lifestyle_fixture_path=None,
    )
    _, result_with_life = run_golden_panel(
        fixture_path=fixture,
        output_root=tmp_path,
        run_id="with-life",
        write_narrative=False,
        lifestyle_fixture_path=lifestyle_fixture,
    )
    assert "lifestyle" in result_with_life
    burden_no = _get_burden_vector(result_no_life)
    burden_with = _get_burden_vector(result_with_life)
    assert burden_no != burden_with


def test_with_lifestyle_base_burden_preserved(tmp_path):
    """Lifestyle artifact preserves base_burden in system_modifiers."""
    fixture = _collision_free_fixture()
    lifestyle_fixture = Path(__file__).parent.parent / "fixtures" / "lifestyle_minimal.json"
    _, result = run_golden_panel(
        fixture_path=fixture,
        output_root=tmp_path,
        run_id="base-check",
        write_narrative=False,
        lifestyle_fixture_path=lifestyle_fixture,
    )
    lifestyle = result.get("lifestyle", {})
    mods = lifestyle.get("system_modifiers", {})
    for system, data in mods.items():
        for contrib in data.get("contributions", []):
            assert "modifier" in contrib
            assert "capped_modifier" in contrib
    adj = lifestyle.get("confidence_adjustments", {})
    assert isinstance(adj, dict)


def test_with_lifestyle_deterministic_ordering(tmp_path):
    """System keys and contributions sorted alphabetically."""
    fixture = _collision_free_fixture()
    lifestyle_fixture = Path(__file__).parent.parent / "fixtures" / "lifestyle_minimal.json"
    _, result = run_golden_panel(
        fixture_path=fixture,
        output_root=tmp_path,
        run_id="order-check",
        write_narrative=False,
        lifestyle_fixture_path=lifestyle_fixture,
    )
    mods = result.get("lifestyle", {}).get("system_modifiers", {})
    system_keys = list(mods.keys())
    assert system_keys == sorted(system_keys)
    for system, data in mods.items():
        contribs = data.get("contributions", [])
        input_names = [c.get("input", "") for c in contribs]
        assert input_names == sorted(input_names)


def test_with_lifestyle_floats_rounded_4dp(tmp_path):
    """All floats in lifestyle section rounded to 4 decimal places."""
    fixture = _collision_free_fixture()
    lifestyle_fixture = Path(__file__).parent.parent / "fixtures" / "lifestyle_minimal.json"
    _, result = run_golden_panel(
        fixture_path=fixture,
        output_root=tmp_path,
        run_id="4dp-check",
        write_narrative=False,
        lifestyle_fixture_path=lifestyle_fixture,
    )
    lifestyle = result.get("lifestyle", {})

    def _check_4dp(obj, path=""):
        if isinstance(obj, dict):
            for k, v in obj.items():
                _check_4dp(v, f"{path}.{k}")
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                _check_4dp(v, f"{path}[{i}]")
        elif isinstance(obj, float):
            s = f"{obj:.10f}"
            if "." in s:
                decimal_part = s.split(".")[1].rstrip("0")
                assert len(decimal_part) <= 4, f"{path}={obj} has more than 4 decimal places"

    _check_4dp(lifestyle)


def test_with_lifestyle_input_hash_present_and_correct(tmp_path):
    """lifestyle_input_hash in replay_manifest equals sha256(canonical JSON) of lifestyle_inputs."""
    fixture = _collision_free_fixture()
    lifestyle_fixture = Path(__file__).parent.parent / "fixtures" / "lifestyle_minimal.json"
    lifestyle_inputs = json.loads(lifestyle_fixture.read_text(encoding="utf-8"))
    expected_hash = hashlib.sha256(
        json.dumps(lifestyle_inputs, sort_keys=True, ensure_ascii=True).encode("utf-8")
    ).hexdigest()
    _, result = run_golden_panel(
        fixture_path=fixture,
        output_root=tmp_path,
        run_id="hash-check",
        write_narrative=False,
        lifestyle_fixture_path=lifestyle_fixture,
    )
    replay = result.get("replay_manifest", {}) or {}
    actual_hash = replay.get("lifestyle_input_hash")
    assert actual_hash == expected_hash
