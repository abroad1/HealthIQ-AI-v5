# N-8 — Deterministic narrative compiler v1 (implementation note)

## What was added

| Artifact | Role |
|----------|------|
| `backend/core/contracts/narrative_report_v1.py` | `NarrativeReportV1` — section fields per architecture §5 (empty allowed for unassembled sections). |
| `backend/core/analytics/narrative_report_compiler_v1.py` | `compile_narrative_report_v1(...)` — loads N-5/N-6/N-7 YAMLs; gates lead/secondary assembly on **fired suboptimal/at_risk signals** in `insight_graph.signal_results`; appends **lifestyle bridges** from `meta.lifestyle_interpretation_bridges_v1` when active; **never raises** on missing files (records skips in `meta`). |
| `backend/core/pipeline/orchestrator.py` | Invokes compiler **after** IDL publish, **before** `AnalysisDTO` construction. |
| `backend/core/models/results.py` | `AnalysisDTO.narrative_report_v1` optional field. |

## Gating (v1)

- **Lead domain** (one-carbon / homocysteine / MCV): any of `signal_homocysteine_high`, `signal_homocysteine_elevation_context`, `signal_mcv_high` in suboptimal/at_risk.
- **Secondary domain** (lipid transport): any of `signal_ldl_cholesterol_high`, `signal_hdl_cholesterol_high`, `signal_non_hdl_high`, `signal_lipid_transport_dysfunction`, `signal_triglycerides_high`.

## Limits

- Not full benchmark prose parity; sections like `retail_summary`, `longitudinal_narrative`, etc. remain **empty** until later tranches.
- Does **not** modify `report_compiler_v1.py`.

## Tests

- `backend/tests/unit/test_narrative_report_compiler_v1.py` (included in `run_baseline_tests.py`).
