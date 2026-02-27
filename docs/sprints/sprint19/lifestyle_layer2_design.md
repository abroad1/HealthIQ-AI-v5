# Sprint 19 — Lifestyle Layer 2 Design

## Overview

Layer 2 lifestyle modelling provides deterministic, bounded additive modifiers to system burden. It uses UK metric canonical units only (cm, kg, mmHg, bpm, hours, UK alcohol units). No API wiring. No DB. No LLM.

## What Was Added

| Component | Path | Description |
|-----------|------|-------------|
| SSOT Registry | `backend/ssot/lifestyle_registry.yaml` | Units, inputs, derived definitions, system caps, modifier rules, confidence rules |
| Loader | `backend/core/analytics/lifestyle_registry_loader.py` | Loads YAML and returns dict; engine receives pre-loaded registry only |
| Engine | `backend/core/analytics/lifestyle_modifier_engine.py` | `LifestyleModifierEngine` with `compute_derived`, `validate_inputs`, `apply` |
| Unit Tests | `backend/tests/unit/test_lifestyle_modifier_engine.py` | 14 tests covering derived, thresholds, caps, ordering, confidence, sit-stand, missing base |

## Output Contract

The `apply` method returns a JSON-safe dict with this structure:

```json
{
  "derived_inputs": {
    "bmi": 27.7778,
    "waist_to_height_ratio": 0.5
  },
  "validated_inputs": {
    "alcohol_units_per_week": 7,
    "bmi": 27.7778,
    "diastolic_bp": 82,
    "height_cm": 180,
    "resting_heart_rate": 72,
    "sit_stand_test_type": "reps_30s",
    "sit_stand_value": 14,
    "sleep_hours": 7,
    "smoking_status": "never",
    "systolic_bp": 146,
    "waist_circumference_cm": 90,
    "waist_to_height_ratio": 0.5,
    "weight_kg": 90
  },
  "input_errors": [],
  "system_modifiers": {
    "cardiovascular": {
      "total_modifier": 0.07,
      "capped_total_modifier": 0.07,
      "cap": 0.2,
      "contributions": [
        {
          "input": "systolic_bp",
          "rule": "thresholds_above",
          "value": 146,
          "modifier": 0.07,
          "capped_modifier": 0.07,
          "details": {}
        }
      ],
      "missing_core_inputs": [],
      "confidence_penalty": 0.0
    }
  },
  "adjusted_system_burdens": {
    "cardiovascular": {
      "base_burden": 0.15,
      "modifier": 0.07,
      "adjusted_burden": 0.22,
      "confidence_penalty": 0.0
    }
  }
}
```

## Rule Types

| Type | Behaviour |
|------|-----------|
| `thresholds_above` | Apply the **highest** modifier among thresholds met (not cumulative). E.g. systolic_bp=146 triggers above 140 only (0.07). |
| `thresholds_below` | Same semantics: highest modifier among thresholds met. E.g. sleep_hours=5 triggers below 6 rule. |
| `categorical_values` | Direct map from input value to modifier. Unknown values default to 0.0; error recorded. |
| `sit_stand_phase1` | Conservative rule keyed by `sit_stand_test_type`: `reps_30s` if value &lt; 12 → 0.05 else 0; `time_5_reps_seconds` if value &gt; 15 → 0.05 else 0. |
| `passthrough` | No direct modifier contribution; used only to inform interpretation of a sibling input (e.g. `sit_stand_test_type` informs `sit_stand_value`). |

## Determinism Guarantees

- All system keys are sorted **alphabetically**.
- Contributions within each system are sorted alphabetically by **input** name.
- All floats rounded to **4 decimal places** consistently.
- No random or time-based behaviour.

## Caps

1. **Per-input cap**: After each rule is computed, the contribution is capped by the rule's `cap` field.
2. **Per-system cap**: The sum of contributions is capped by `system_caps[system]`.
3. **Final clamp**: `adjusted_burden` is clamped to [0, 1].

## Confidence Penalties

For each system, if any core input (from `confidence_rules.core_inputs_by_system`) is missing or invalid, apply `missing_input_confidence_penalty` **once per system** (not per missing input). The `missing_core_inputs` list reports which inputs were missing or invalid.

## How to Run Tests

```bash
# From backend/
python -m pytest tests/unit/test_lifestyle_modifier_engine.py -v
python scripts/run_baseline_tests.py
```

Both must pass before marking sprint complete.

## No API Wiring Yet

Ingestion conversion and orchestrator integration will be handled at the Layer 3 boundary in a future sprint.
