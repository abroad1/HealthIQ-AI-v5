# N-4 — Implementation note (lifestyle interpretation bridges)

## What was added

- **Governed SSOT:** `backend/ssot/lifestyle_interpretation_bridges_v1.yaml` — thresholds and field bindings for three narrowed bridges (no weight-loss bridge; no occupational physical-work field).
- **Engine:** `backend/core/analytics/lifestyle_interpretation_bridge_engine.py` — `compute_lifestyle_interpretation_bridges_v1(...)` returns a deterministic, version-stamped bundle.
- **Runtime exposure:** `AnalysisDTO.meta["lifestyle_interpretation_bridges_v1"]` set in `core/pipeline/orchestrator.py` after scoring/clustering/InsightGraph build. **InsightGraphV1 is not extended.**

## Bridges (narrowed scope)

1. **Alcohol → methylation / macrocytosis context:** moderate-or-higher intake **and** coherent lab signal (homocysteine and/or MCV high vs reference), with explicit bands in output.
2. **Hydration / high-activity → renal context:** renal panel biomarker present **and** (low fluid intake and/or high vigorous/resistance pattern from questionnaire).
3. **Fasting / dietary-pattern → glycaemic context:** intermittent-fasting or extended overnight fast **and** HbA1c present with normal/low band — no weight-loss questionnaire mapping.

## What this unblocks

- Later **deterministic narrative compiler** work can read `meta.lifestyle_interpretation_bridges_v1` without coupling to InsightGraph schema churn.

## Tests

- `backend/tests/unit/test_lifestyle_interpretation_bridges_v1.py`
