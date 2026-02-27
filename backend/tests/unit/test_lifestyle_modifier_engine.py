"""
Sprint 19 Layer 2 — Unit tests for Lifestyle Modifier Engine.

Pure unit tests. No DB. No external calls. Registry dict passed directly.
"""

import pytest

from core.analytics.lifestyle_modifier_engine import LifestyleModifierEngine
from core.analytics.lifestyle_registry_loader import load_lifestyle_registry


@pytest.fixture
def registry():
    """Load registry once per test module (tests pass dict to engine)."""
    return load_lifestyle_registry()


@pytest.fixture
def engine(registry):
    return LifestyleModifierEngine(registry)


# --- 1) Derived computation ---
def test_derived_waist_to_height_ratio(engine):
    """height_cm=180, waist_circumference_cm=90 -> waist_to_height_ratio=0.5"""
    inputs = {"height_cm": 180, "waist_circumference_cm": 90}
    derived = engine.compute_derived(inputs)
    assert "waist_to_height_ratio" in derived
    assert derived["waist_to_height_ratio"] == 0.5


def test_derived_bmi(engine):
    """weight_kg=90, height_cm=180 -> bmi=27.7778 (rounded to 4dp)"""
    inputs = {"weight_kg": 90, "height_cm": 180}
    derived = engine.compute_derived(inputs)
    assert "bmi" in derived
    assert derived["bmi"] == 27.7778


# --- 2) Threshold rule behaviour (highest met only, not cumulative) ---
def test_threshold_systolic_145_triggers_above_140_only(engine):
    """systolic_bp=145 -> modifier=0.07 (above 140 rule, not 0.03+0.07)"""
    inputs = {
        "systolic_bp": 145,
        "height_cm": 180,
        "weight_kg": 70,
        "waist_circumference_cm": 80,
        "smoking_status": "never",
    }
    base = {"cardiovascular": 0.1}
    result = engine.apply(base, inputs)
    cv = result["system_modifiers"]["cardiovascular"]
    systolic_contrib = next(c for c in cv["contributions"] if c["input"] == "systolic_bp")
    assert systolic_contrib["modifier"] == 0.07
    assert systolic_contrib["capped_modifier"] == 0.07


def test_threshold_systolic_125_triggers_above_120_only(engine):
    """systolic_bp=125 -> modifier=0.03 (above 120 rule only)"""
    inputs = {
        "systolic_bp": 125,
        "height_cm": 180,
        "weight_kg": 70,
        "waist_circumference_cm": 80,
        "smoking_status": "never",
    }
    base = {"cardiovascular": 0.1}
    result = engine.apply(base, inputs)
    cv = result["system_modifiers"]["cardiovascular"]
    systolic_contrib = next(c for c in cv["contributions"] if c["input"] == "systolic_bp")
    assert systolic_contrib["modifier"] == 0.03


# --- 3) Caps ---
def test_input_level_cap_before_system_cap(engine):
    """Input-level cap is applied before system cap."""
    inputs = {
        "systolic_bp": 200,
        "diastolic_bp": 110,
        "resting_heart_rate": 100,
        "waist_circumference_cm": 120,
        "height_cm": 170,
        "weight_kg": 70,
        "smoking_status": "current",
    }
    base = {"cardiovascular": 0.0}
    result = engine.apply(base, inputs)
    cv = result["system_modifiers"]["cardiovascular"]
    assert cv["total_modifier"] >= 0
    assert cv["capped_total_modifier"] <= cv["cap"]
    assert result["adjusted_system_burdens"]["cardiovascular"]["adjusted_burden"] <= 1.0


def test_system_cap_bounds_total(engine):
    """System cap bounds total even when multiple inputs each contribute."""
    inputs = {
        "systolic_bp": 160,
        "diastolic_bp": 100,
        "resting_heart_rate": 90,
        "waist_circumference_cm": 110,
        "height_cm": 170,
        "weight_kg": 80,
        "smoking_status": "current",
    }
    base = {"cardiovascular": 0.0}
    result = engine.apply(base, inputs)
    cv = result["system_modifiers"]["cardiovascular"]
    assert cv["capped_total_modifier"] <= cv["cap"]
    assert cv["cap"] == 0.2


# --- 4) Deterministic ordering ---
def test_system_keys_sorted_alphabetically(engine):
    """Output system keys are sorted alphabetically."""
    inputs = {"height_cm": 180, "weight_kg": 70, "waist_circumference_cm": 85}
    base = {"cardiovascular": 0.1, "metabolic": 0.1}
    result = engine.apply(base, inputs)
    system_keys = list(result["system_modifiers"].keys())
    assert system_keys == sorted(system_keys)
    adj_keys = list(result["adjusted_system_burdens"].keys())
    assert adj_keys == sorted(adj_keys)


def test_contributions_sorted_alphabetically_by_input(engine):
    """Contributions within each system are sorted alphabetically by input name."""
    inputs = {
        "systolic_bp": 150,
        "diastolic_bp": 95,
        "resting_heart_rate": 80,
        "waist_circumference_cm": 100,
        "height_cm": 170,
        "weight_kg": 75,
        "smoking_status": "former",
    }
    base = {"cardiovascular": 0.1}
    result = engine.apply(base, inputs)
    cv = result["system_modifiers"]["cardiovascular"]
    contrib_inputs = [c["input"] for c in cv["contributions"]]
    assert contrib_inputs == sorted(contrib_inputs)


# --- 5) Confidence penalty ---
def test_missing_systolic_bp_applies_confidence_penalty(engine):
    """Missing systolic_bp for cardiovascular applies confidence_penalty=0.10."""
    inputs = {"diastolic_bp": 80, "smoking_status": "never"}
    base = {"cardiovascular": 0.1}
    result = engine.apply(base, inputs)
    cv = result["system_modifiers"]["cardiovascular"]
    assert cv["confidence_penalty"] == 0.1
    assert "systolic_bp" in cv["missing_core_inputs"]


# --- 6) Sit-stand rules ---
def test_sit_stand_reps_30s_low_triggers_modifier(engine):
    """sit_stand_test_type=reps_30s, sit_stand_value=10 -> musculoskeletal modifier=0.05"""
    inputs = {
        "sit_stand_test_type": "reps_30s",
        "sit_stand_value": 10,
    }
    base = {"musculoskeletal": 0.0}
    result = engine.apply(base, inputs)
    ms = result["system_modifiers"]["musculoskeletal"]
    assert ms["capped_total_modifier"] == 0.05


def test_sit_stand_reps_30s_high_no_modifier(engine):
    """sit_stand_test_type=reps_30s, sit_stand_value=14 -> musculoskeletal modifier=0.00"""
    inputs = {
        "sit_stand_test_type": "reps_30s",
        "sit_stand_value": 14,
    }
    base = {"musculoskeletal": 0.0}
    result = engine.apply(base, inputs)
    ms = result["system_modifiers"]["musculoskeletal"]
    assert ms["capped_total_modifier"] == 0.0


def test_sit_stand_time_5_reps_high_triggers_modifier(engine):
    """sit_stand_test_type=time_5_reps_seconds, sit_stand_value=20 -> musculoskeletal modifier=0.05"""
    inputs = {
        "sit_stand_test_type": "time_5_reps_seconds",
        "sit_stand_value": 20,
    }
    base = {"musculoskeletal": 0.0}
    result = engine.apply(base, inputs)
    ms = result["system_modifiers"]["musculoskeletal"]
    assert ms["capped_total_modifier"] == 0.05


def test_sit_stand_time_5_reps_low_no_modifier(engine):
    """sit_stand_test_type=time_5_reps_seconds, sit_stand_value=12 -> musculoskeletal modifier=0.00"""
    inputs = {
        "sit_stand_test_type": "time_5_reps_seconds",
        "sit_stand_value": 12,
    }
    base = {"musculoskeletal": 0.0}
    result = engine.apply(base, inputs)
    ms = result["system_modifiers"]["musculoskeletal"]
    assert ms["capped_total_modifier"] == 0.0


# --- 7) Missing base_system_burdens key ---
def test_system_in_modifiers_but_absent_from_base_reported(engine):
    """System present in system_modifiers but absent from base_system_burdens is reported with base_burden=0.0."""
    inputs = {"sit_stand_test_type": "reps_30s", "sit_stand_value": 10}
    base = {}  # No musculoskeletal key
    result = engine.apply(base, inputs)
    assert "musculoskeletal" in result["adjusted_system_burdens"]
    adj = result["adjusted_system_burdens"]["musculoskeletal"]
    assert adj["base_burden"] == 0.0
    assert adj["modifier"] == 0.05
    assert adj["adjusted_burden"] == 0.05
