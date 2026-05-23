# HealthIQ AI Runtime Architecture Map v1

## Purpose

Describe the **current** HealthIQ AI analytical runtime — not a target-state design.

## Ingestion

- API / upload paths normalise panels before orchestration.
- Unit normalisation: `backend/core/units/registry.py` — callers must set `__unit_normalisation_meta__` on the panel dict before `AnalysisOrchestrator.run()`.

## Canonicalisation

- Alias resolution: `backend/core/canonical/normalize.py` — `BiomarkerNormalizer`
- Quarantine: unmapped keys skipped in `orchestrator_phases_v1.quarantine_unmapped_biomarkers()`
- HbA1c arbitration: `backend/core/canonical/hba1c_layer_b_arbitration.py`

## Scoring

- Engine: `backend/core/scoring/engine.py`
- Policy: `backend/ssot/scoring_policy.yaml` (read-only authority; do not edit in scaffold sprints)
- Direction-aware scoring: LC-S14 overlays in scoring rules

## Signals

- Registry + evaluator: `backend/core/analytics/signal_evaluator.py`
- Phase wrapper: `orchestrator_phases_v1.evaluate_signal_evaluation_phase()`

## Knowledge Bus package lifecycle

- Packages live under `knowledge_bus/packages/` — **content estate**, not runtime orchestration authority.
- Lifecycle framework: `docs/audit-papers/LC-S17_knowledge_bus_lifecycle_framework.md`
- Frontend surface audit: `docs/audit-papers/LC-S16_knowledge_asset_frontend_surface_audit.md`

## Root-cause / WHY registry

- Registry: `backend/core/knowledge/root_cause_registry_v1.py`
- Compiler: `backend/core/analytics/root_cause_compiler_v1.py`
- 41 manual_v1 targets (LC-S18)

## Lifestyle propagation

- Questionnaire mapping: `backend/core/pipeline/questionnaire_mapper.py`
- Overlays: `backend/core/scoring/overlays.py`
- LC-S13 narrative coherence guards in regression suite

## DTO contract

- Builder: `backend/core/dto/builders.py`
- Frontend contract: `backend/core/dto/frontend_contract_v1.py`
- Persisted replay: `backend/core/dto/persisted_replay_contract_v1.py`

## Persisted replay

- Fixture: `backend/tests/fixtures/persisted_results/lc_s20_ab_launch_core_v1.json`
- Strategy: `docs/audit-papers/LC-S20_persisted_replay_stale_result_strategy.md`

## Frontend rendering boundary

- Frontend consumes DTO root keys only — no clinical logic in `frontend/`.
- Payload contract: LC-S19 audit paper + `frontend_contract_v1.py`

## Sentinel

- Escaped defects pack: `sentinel/packs/escaped_defects_v1.json`
- Phase 2 replay render: `sentinel/packs/scaffold_lc_s20_22_replay_render_v1.json`

## Automation Bus workflow

- SOP: `docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md`
- Work packages: `backend/scripts/run_work_package.py` start/finish

## Orchestration entry point

- `backend/core/pipeline/orchestrator.py` — `AnalysisOrchestrator.run()`
- Documented phases: `backend/core/pipeline/orchestrator_phases_v1.py`

## Standing maintenance

Future KB-WAVE or scaffold sprints must update this document if they introduce or change the relevant architectural pattern.
