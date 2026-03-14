from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml


_REPO_ROOT = Path(__file__).resolve().parents[3]
_KB_S25_PACKAGE_DIRS = [
    "pkg_iron_deficiency_context",
    "pkg_iron_overload_context",
    "pkg_b12_deficiency_context",
    "pkg_inflammation_crp_context",
    "pkg_hepatic_alt_context",
    "pkg_glucose_dysregulation_hba1c_context",
    "pkg_thyroid_tsh_context",
    "pkg_s24_alt_high_hepatocellular_injury",
    "pkg_s24_creatinine_high_renal",
    "pkg_s24_crp_high_inflammation",
    "pkg_s24_ferritin_high_overload",
    "pkg_s24_ferritin_low_iron_deficiency",
    "pkg_s24_hba1c_high_glycaemia",
    "pkg_s24_ldl_high_dyslipidaemia",
    "pkg_s24_triglycerides_high_metabolic",
    "pkg_s24_tsh_high_hypothyroidism",
    "pkg_s24_tsh_low_hyperthyroidism",
    "pkg_s24_albumin_low_nutritional",
    "pkg_s24_alp_high_bone_biliary",
    "pkg_s24_calcium_high_endocrine",
    "pkg_s24_folate_low_deficiency",
    "pkg_s24_ggt_high_hepatic",
    "pkg_s24_hdl_high_cardiovascular",
    "pkg_s24_hdl_low_cardiovascular",
    "pkg_s24_hgb_low_anemia",
    "pkg_s24_homocysteine_high_metabolic",
    "pkg_s24_lym_high_lymphocytosis",
]
_EXPLANATION_KEYS = [
    "mechanism",
    "biological_pathway",
    "interpretation",
    "implications",
    "supporting_marker_roles",
]


def _load_signal_definitions():
    items = []
    for package_dir in _KB_S25_PACKAGE_DIRS:
        path = _REPO_ROOT / "knowledge_bus" / "packages" / package_dir / "signal_library.yaml"
        payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        for signal in payload.get("signals", []):
            items.append((package_dir, signal))
    return items


@pytest.mark.parametrize("package_dir,signal", _load_signal_definitions())
def test_kbs25_explanation_payload_has_required_prose_fields(package_dir: str, signal: dict):
    explanation = signal.get("explanation")
    assert isinstance(explanation, dict), f"{package_dir}:{signal.get('signal_id')} missing explanation"
    for key in _EXPLANATION_KEYS:
        value = explanation.get(key)
        assert isinstance(value, str), f"{package_dir}:{signal.get('signal_id')} explanation.{key} must be string"
        assert len(value.strip()) >= 20, f"{package_dir}:{signal.get('signal_id')} explanation.{key} too short"


@pytest.mark.parametrize("package_dir,signal", _load_signal_definitions())
def test_kbs25_explanation_payload_has_no_raw_units_or_range_brackets(package_dir: str, signal: dict):
    explanation = signal.get("explanation") or {}
    combined = " ".join(str(explanation.get(k, "")) for k in _EXPLANATION_KEYS)

    # Conservative hygiene checks to keep narrative interaction-ready and non-tabular.
    assert "mg/dL" not in combined
    assert "mmol/L" not in combined
    assert "U/L" not in combined
    assert re.search(r"\[[^\]]+\]", combined) is None
