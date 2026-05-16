"""LC-S8D — Sentinel guardrails for UK/SI unit governance."""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from core.analytics.scoring_policy_registry import load_scoring_policy
from core.scoring.rules import (
    ScoreRange,
    ScoringRules,
    UNSCORED_REASON_UNKNOWN_UNIT_NOT_SCORED,
    UNSCORED_REASON_UNIT_REFERENCE_RANGE_INCOHERENT,
)
from core.units.display_policy import load_display_unit_policy
from core.units.registry import (
    UnitConversionError,
    UnitRegistry,
    apply_unit_normalisation,
    convert_value,
)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
FRONTEND_APP_ROOT = REPO_ROOT / "frontend" / "app"

# LC-S8D Phase C — scoring-policy unit must match biomarkers SSOT canonical unit.
LC_S8D_SSOT_SCORING_UNIT_ALIGNMENT = {
    "glucose": "mmol/L",
    "hba1c": "mmol/mol",
    "total_cholesterol": "mmol/L",
    "ldl_cholesterol": "mmol/L",
    "hdl_cholesterol": "mmol/L",
    "triglycerides": "mmol/L",
    "creatinine": "µmol/L",
    "hematocrit": "L/L",
    "platelets": "10^9/L",
    "white_blood_cells": "10^9/L",
}

# Clinical conversion factors that must not appear in frontend renderer code.
FORBIDDEN_FRONTEND_CONVERSION_RE = re.compile(
    r"(?:\b0\.055(?:555)?\b|\b18\.0(?:18)?\b|\b38\.67\b|\b88\.4\b|\b0\.02586\b|\b0\.01129\b|\b10\.929\b)"
)

FRONTEND_UNIT_REPAIR_SCAN_ALLOWLIST = {
    "DevApiProbe.tsx",
    "parsed.ts",
}


def _load_biomarkers_ssot() -> dict:
    path = REPO_ROOT / "backend" / "ssot" / "biomarkers.yaml"
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("biomarkers") or {}


def _collect_frontend_ts_sources() -> list[Path]:
    if not FRONTEND_APP_ROOT.exists():
        return []
    paths: list[Path] = []
    for ext in ("*.ts", "*.tsx"):
        paths.extend(FRONTEND_APP_ROOT.rglob(ext))
    return [p for p in paths if p.name not in FRONTEND_UNIT_REPAIR_SCAN_ALLOWLIST]


@pytest.mark.regression
class TestLC_S8DUnitGovernanceGuards:
    def test_display_policy_authority_exists(self):
        data = load_display_unit_policy()
        assert data.get("policy_version")
        assert "hba1c" in (data.get("biomarkers") or {})

    def test_phase_a_equivalence_vectors(self):
        assert convert_value("platelets", 225.0, "K/μL")[1] == "10^9/L"
        assert convert_value("white_blood_cells", 6.4, "K/uL")[1] == "10^9/L"
        assert convert_value("sodium", 140.0, "mEq/L")[1] == "mmol/L"

    def test_unknown_unit_not_scored_against_policy(self):
        rules = ScoringRules()
        _, _, reason = rules.calculate_biomarker_score(
            "glucose",
            5.0,
            input_reference_range={"min": 3.0, "max": 6.0, "unit": "g/L", "source": "lab"},
            value_unit="g/L",
        )
        assert reason == UNSCORED_REASON_UNKNOWN_UNIT_NOT_SCORED

    def test_hematocrit_fraction_not_stored_as_percent(self):
        out = apply_unit_normalisation(
            {"hematocrit": {"value": 0.438, "unit": "L/L", "reference_range": None}}
        )
        assert out["hematocrit"]["unit"] == "L/L"
        assert out["hematocrit"]["value"] == pytest.approx(0.438, abs=0.001)

    def test_bun_alias_maps_to_urea_not_urate(self):
        from core.canonical.normalize import normalize_biomarkers_with_metadata

        out = normalize_biomarkers_with_metadata({"BUN": {"value": 7.0, "unit": "mmol/L"}})
        assert "urea" in out
        assert "urate" not in out


@pytest.mark.regression
class TestLC_S8DLayerBUnitDeclared:
    """Sentinel: layer_b_unit_declared + uk_layer_b_canonical_unit_drift."""

    def test_every_scored_biomarker_declares_layer_b_unit(self):
        policy = load_scoring_policy().raw
        biomarkers = policy.get("biomarkers") or {}
        missing = [
            name
            for name, item in biomarkers.items()
            if not (isinstance(item, dict) and str(item.get("unit", "")).strip())
        ]
        assert not missing, f"scoring_policy biomarkers missing unit: {missing}"

    def test_lc_s8d_migrated_units_match_ssot_canonical(self):
        """Layer B scoring-policy unit must match biomarkers SSOT for Phase C migrated rows."""
        policy = load_scoring_policy().raw
        scoring_biomarkers = policy.get("biomarkers") or {}
        ssot = _load_biomarkers_ssot()
        drift = []
        for biomarker_id, expected_unit in LC_S8D_SSOT_SCORING_UNIT_ALIGNMENT.items():
            policy_item = scoring_biomarkers.get(biomarker_id)
            ssot_item = ssot.get(biomarker_id)
            if not isinstance(policy_item, dict):
                drift.append(f"{biomarker_id}: missing scoring_policy entry")
                continue
            if not isinstance(ssot_item, dict):
                drift.append(f"{biomarker_id}: missing biomarkers.yaml entry")
                continue
            policy_unit = str(policy_item.get("unit", "")).strip()
            ssot_unit = str(ssot_item.get("unit", "")).strip()
            if policy_unit != expected_unit or ssot_unit != expected_unit:
                drift.append(
                    f"{biomarker_id}: policy={policy_unit!r} ssot={ssot_unit!r} expected={expected_unit!r}"
                )
        assert not drift, f"Layer B / SSOT unit drift: {drift}"

    def test_phase_a_electrolytes_ssot_canonical_mmol_L(self):
        """Phase A electrolytes: SSOT canonical mmol/L (not in scoring_policy)."""
        ssot = _load_biomarkers_ssot()
        for biomarker_id in ("sodium", "potassium", "chloride"):
            entry = ssot.get(biomarker_id)
            assert isinstance(entry, dict), biomarker_id
            assert str(entry.get("unit", "")).strip() == "mmol/L"


@pytest.mark.regression
class TestLC_S8DInputUnitHasAuthority:
    """Sentinel: input_unit_has_authority."""

    def test_authorised_legacy_unit_converts_to_canonical_base(self):
        val, unit = convert_value("glucose", 95.0, "mg/dL")
        assert unit == "mmol/L"
        assert val == pytest.approx(5.277778, abs=0.01)

    def test_unauthorised_unit_rejects_without_fallback(self):
        with pytest.raises(UnitConversionError) as exc:
            convert_value("glucose", 5.0, "g/L")
        assert exc.value.biomarker_id == "glucose"

    def test_named_ssot_unit_entry_exists_for_phase_a_tokens(self):
        reg = UnitRegistry()
        data = reg._load_units()
        named = data.get("units") or {}
        for key in ("mmol_L", "mEq_L", "ten_9_L"):
            assert key in named, f"units.yaml missing named entry {key}"


@pytest.mark.regression
class TestLC_S8DBiomarkerValueReferenceUnitIncoherence:
    """Sentinel: biomarker_value_reference_unit_incoherence."""

    def test_incoherent_value_and_reference_units_unscored(self):
        rules = ScoringRules()
        score, band, reason = rules.calculate_biomarker_score(
            "hemoglobin",
            14.0,
            input_reference_range={
                "min": 8.0,
                "max": 11.0,
                "unit": "mmol/L",
                "source": "lab",
            },
            value_unit="g/dL",
        )
        assert score == 0.0
        assert band == ScoreRange.CRITICAL
        assert reason == UNSCORED_REASON_UNIT_REFERENCE_RANGE_INCOHERENT

    def test_coherent_units_allow_scoring(self):
        rules = ScoringRules()
        score, band, reason = rules.calculate_biomarker_score(
            "hemoglobin",
            14.0,
            input_reference_range={
                "min": 12.0,
                "max": 18.0,
                "unit": "g/dL",
                "source": "lab",
            },
            value_unit="g/dL",
        )
        assert reason is None
        assert 0.0 <= score <= 100.0


@pytest.mark.regression
class TestLC_S8DFrontendNoUnitRepair:
    """Sentinel: frontend_no_unit_repair — static scan."""

    def test_frontend_app_has_no_clinical_conversion_constants(self):
        findings: list[str] = []
        for path in _collect_frontend_ts_sources():
            try:
                source = path.read_text(encoding="utf-8")
            except OSError:
                continue
            for match in FORBIDDEN_FRONTEND_CONVERSION_RE.finditer(source):
                line_no = source[: match.start()].count("\n") + 1
                line = source.splitlines()[line_no - 1].strip()
                if line.startswith("//") or line.startswith("*"):
                    continue
                findings.append(f"{path.relative_to(REPO_ROOT)}:{line_no} — {match.group()!r} in {line[:100]}")
        assert not findings, "Forbidden unit conversion constants in frontend:\n" + "\n".join(findings)


@pytest.mark.regression
class TestLC_S8DNewBiomarkerUnitMetadata:
    """Sentinel: new_biomarker_unit_metadata."""

    def test_scoring_system_biomarkers_have_ssot_unit_metadata(self):
        policy = load_scoring_policy().raw
        ssot = _load_biomarkers_ssot()
        systems = policy.get("systems") or {}
        missing_unit: list[str] = []
        missing_ssot: list[str] = []
        for system_name, system_item in systems.items():
            if not isinstance(system_item, dict):
                continue
            for biomarker_id in system_item.get("biomarkers") or []:
                bid = str(biomarker_id)
                entry = ssot.get(bid)
                if not isinstance(entry, dict):
                    missing_ssot.append(f"{system_name}:{bid}")
                    continue
                if not str(entry.get("unit", "")).strip():
                    missing_unit.append(f"{system_name}:{bid}")
        assert not missing_ssot, f"Scoring biomarkers missing from biomarkers.yaml: {missing_ssot}"
        assert not missing_unit, f"Scoring biomarkers missing unit in SSOT: {missing_unit}"
