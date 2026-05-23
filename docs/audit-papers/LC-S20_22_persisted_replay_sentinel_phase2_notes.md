# LC-S20/22 — Combined Implementation Notes

**Work package:** LC-S20-22  
**Branch:** `scaffold/lc-s20-22-persisted-replay-sentinel-phase2`  
**Date:** 2026-05-23

## 1. Preflight results

| Check | Result |
|-------|--------|
| Branch | `main` → `scaffold/lc-s20-22-persisted-replay-sentinel-phase2` |
| Stash | Empty |
| Kernel start | Exit 0 |
| Controlling docs | Present |

## 2. Prior scaffold guard results

All pass (LC-S8F through LC-S18, scoring rules).

## 3. Persisted replay current-state assessment

- Persistence: DB `processing_metadata[CLIENT_RESULT_SHAPE_V1]` + in-memory cache
- GET compiles clinician/balanced systems on read
- Phase-1 placeholder `test_persisted_result_replay_status.py` superseded by LC-S20/22 guards

## 4. Stale-result policy decision

**Hybrid (Option C):** historical snapshot renders as-is; staleness detectable; regeneration explicit (future).

## 5. Sentinel Phase 2 structure decision

**Hybrid (Option C):** new `scaffold_lc_s20_22_replay_render_v1.json`; `escaped_defects_v1.json` retained; `persisted_result_replay` promoted to GUARDED.

## 6. Sentinel pack rationalisation decision

No destructive reorganisation. New scaffold pack for replay/render domain; deferred split of LC-S16/18 classes to dedicated packs (LC-S23).

## 7. Files changed

| File | Purpose |
|------|---------|
| `backend/core/dto/persisted_replay_contract_v1.py` | Compatibility + stale assessment |
| `backend/scripts/generate_lc_s20_persisted_fixture_v1.py` | Fixture generator |
| `backend/tests/fixtures/persisted_results/lc_s20_ab_launch_core_v1.json` | Persisted replay fixture |
| `backend/tests/regression/test_lc_s20_22_persisted_replay_sentinel_phase2.py` | Regression guards |
| `sentinel/packs/scaffold_lc_s20_22_replay_render_v1.json` | Phase 2 scaffold pack |
| `sentinel/packs/escaped_defects_v1.json` | Promoted persisted_result_replay |
| `docs/audit-papers/LC-S20_*`, `LC-S22_*`, combined notes | Audit documentation |

## 8. Tests added/updated

- `test_lc_s20_22_persisted_replay_sentinel_phase2.py` (16 tests)

## 9. Render/API smoke coverage added

Backend DTO replay smoke on persisted fixture (primary finding, domains, leakage, homocysteine content, biomarker display fields).

## 10. Residual risks

- No Playwright render verification
- No automatic stale banner in frontend
- Regeneration path not implemented

## 11. Recommendation for LC-S21/23/23B

- **LC-S21:** Playwright results-route smoke + optional stale UI indicator
- **LC-S23:** Sentinel pack split (`scaffold_payload_contract_v1`, `scaffold_why_registry_v1`)
- **LC-S23B / KB-WAVE:** Persisted replay corpus expansion beyond single AB fixture
