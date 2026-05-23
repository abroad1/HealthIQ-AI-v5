# LC-S20 — Persisted Replay and Stale-Result Strategy

**Work package:** LC-S20-22  
**Date:** 2026-05-23

## 1. Executive verdict

**PASS** — Persisted replay fixture established; hybrid stale-result policy documented; deterministic compatibility contract added without DTO restructuring.

## 2. Current persisted-result architecture

| Layer | Authority |
|-------|-----------|
| Storage | `PersistenceService` — `CLIENT_RESULT_SHAPE_V1` in `processing_metadata` |
| In-process cache | `backend/app/routes/analysis.py` — `_analysis_results` |
| GET `/result` | `_raw_result_payload_for_analysis_id` → `build_analysis_result_dto` |
| Replay stamp | `build_replay_manifest_v1` in orchestrator |

## 3. Stored DTO fields

POST persists orchestrator client shape (biomarkers, clusters, meta, narrative, IDL, domain scores, replay_manifest, etc.). GET adds compile-on-read `clinician_report_v1` and `balanced_systems_v1`.

Fixture `lc_s20_ab_launch_core_v1.json` captures **API-ready** shape (post-`build_analysis_result_dto`) for render contract testing.

## 4. Replay manifest assessment

`replay_manifest` is meaningful: stamps engine/registry/policy versions (`ReplayManifestV1`). Used for audit/replay determinism, not frontend render directly.

## 5. Result/versioning assessment

`result_version` is `"1.0.0"` today. Staleness detectable when version or `replay_manifest.manifest_version` drifts from current contract constants.

## 6. Stale-result policy decision

**Option C — Hybrid (preferred):**

- Stored reports render as **historical artefacts** (immutable JSON snapshot).
- Regeneration requires explicit user action when raw inputs are available (not implemented this sprint).
- Stale state is **detectable** via `assess_persisted_result_compatibility()` — does not silently reinterpret old reports.

## 7. Persisted replay fixture strategy

| Item | Value |
|------|-------|
| Fixture | `backend/tests/fixtures/persisted_results/lc_s20_ab_launch_core_v1.json` |
| Source | AB full panel baseline via `AnalysisOrchestrator` + `build_analysis_result_dto` |
| Generator | `backend/scripts/generate_lc_s20_persisted_fixture_v1.py` |
| analysis_id | `lc-s20-persisted-fixture-v1` |

## 8. Compatibility checks added

`backend/core/dto/persisted_replay_contract_v1.py`:

- Required render keys validation
- Root-key contract alignment (`FRONTEND_CONSUMED_ROOT_KEYS`)
- Stale version detection
- Render smoke: primary finding, Wave 1 domain cards, leakage scan

## 9. Failure behaviour

| Condition | Behaviour |
|-----------|-----------|
| Missing required keys | `PersistedReplayCompatibilityError` |
| Version drift | `stale=True` with reasons (non-fatal for load) |
| Missing primary finding / domains | `render_blockers` populated |

## 10. Residual risks

- No Playwright render test (backend DTO smoke only).
- DB migration path for old `result_version` not implemented.
- Regeneration UX not built.

## 11. Implications for Sentinel Phase 2

New scaffold pack `scaffold_lc_s20_22_replay_render_v1.json` guards replay/render contract. `persisted_result_replay` escaped defect promoted from PLACEHOLDER to GUARDED.
