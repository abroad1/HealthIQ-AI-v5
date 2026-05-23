# LC-S21 — Orchestrator Phase Decomposition Notes

## Current entry point

- **Authority:** `backend/core/pipeline/orchestrator.py` — `AnalysisOrchestrator.run()`
- **DTO assembly:** `backend/core/dto/builders.py` — `build_analysis_result_dto()`

## Current call order (high level)

1. Unit normalisation gate (caller-supplied `__unit_normalisation_meta__`)
2. Canonicalisation quarantine (unmapped biomarker skip)
3. Scoring input preparation (panel → simple values + lab reference ranges)
4. Derived markers / ratios (`RatioRegistry.compute`)
5. Signal evaluation (`SignalEvaluator.evaluate_all`)
6. Analysis context (`AnalysisContextFactory`)
7. Scoring (`ScoringEngine`)
8. Clustering (`ClusterEngineV2`)
9. Criticality, insight graph, state engine stack
10. Replay manifest
11. Insight synthesis, DTO/report assembly

Documented phase names live in `backend/core/pipeline/orchestrator_phases_v1.py` as `PIPELINE_PHASE_ORDER`.

## Pain points addressed

- Quarantine, scoring prep, and signal evaluation were inline blocks (~120 lines) inside `run()`, obscuring phase boundaries.
- No single documented phase order for contributors onboarding to the pipeline.

## Decomposition decision

**Extracted (LC-S21):**

| Phase | Module function |
|-------|-----------------|
| `canonicalisation_quarantine` | `quarantine_unmapped_biomarkers()` |
| `scoring_input_preparation` | `prepare_scoring_inputs_from_panel()` |
| `signal_evaluation` | `evaluate_signal_evaluation_phase()` |

**Not extracted (risk):**

- Derived markers block — tightly coupled to policy bounds and ratio registry side effects; left in `run()`.
- Scoring, clustering, root-cause, IDL, replay — remain in orchestrator methods.

## Behaviour preservation proof

- AB baseline fingerprint: `docs/audit-papers/LC-S21_orchestrator_ab_baseline_fingerprint.json`
- Regression: `backend/tests/regression/test_lc_s21_23_23b_orchestrator_docs_ssot.py`
- Prior guards: LC-S13/14/18/20 regression suites unchanged

## Split rule

Not triggered — extraction limited to no-op structural moves with identical logic.

## Standing maintenance

Future orchestrator sprints must update `PIPELINE_PHASE_ORDER` and this note when adding or renaming phases.
