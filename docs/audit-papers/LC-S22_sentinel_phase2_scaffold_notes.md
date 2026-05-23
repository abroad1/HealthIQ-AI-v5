# LC-S22 — Sentinel Phase 2 Scaffold

**Work package:** LC-S20-22  
**Date:** 2026-05-23

## 1. Executive verdict

**PASS** — Hybrid Sentinel structure adopted; scaffold-specific pack created; render/API smoke path guarded deterministically.

## 2. Existing Sentinel pack assessment

`escaped_defects_v1.json` had grown to 20+ defect classes spanning escaped defects and scaffold guards. `persisted_result_replay` was a Phase-1 PLACEHOLDER.

## 3. Chosen Sentinel Phase 2 structure

**Option C — Hybrid:**

- Keep `escaped_defects_v1.json` for escaped defects (including promoted `persisted_result_replay`).
- Add `sentinel/packs/scaffold_lc_s20_22_replay_render_v1.json` for LC-S20/22 scaffold guards.
- Existing sprint packs (`lc_s8d_*`, `lc_s10b_*`) unchanged.

Grouping metadata: new pack includes `scaffold_phase: LC-S20-22`.

## 4. Persisted replay fixture dependency

All Phase 2 render guards depend on `backend/tests/fixtures/persisted_results/lc_s20_ab_launch_core_v1.json`.

## 5. New/updated defect classes

| Class | Pack |
|-------|------|
| `persisted_result_schema_incompatible` | scaffold_lc_s20_22 |
| `persisted_result_render_failure` | scaffold_lc_s20_22 |
| `stale_analysis_unmarked` | scaffold_lc_s20_22 |
| `results_page_missing_primary_finding` | scaffold_lc_s20_22 |
| `results_page_placeholder_text_visible` | scaffold_lc_s20_22 |
| `results_page_internal_token_visible` | scaffold_lc_s20_22 |
| `results_page_missing_domain_cards` | scaffold_lc_s20_22 |
| `results_page_unit_display_regression` | scaffold_lc_s20_22 |
| `persisted_result_replay` (promoted) | escaped_defects_v1 |

## 6. Render/API smoke path

Backend API-to-DTO smoke (no Playwright):

1. Load persisted fixture JSON
2. `validate_persisted_result_for_replay`
3. `build_analysis_result_dto` roundtrip
4. Assert primary finding, Wave 1 domains, no placeholder/internal leakage

## 7. DTO/schema compatibility guards

`test_lc_s20_required_root_keys_present`, `test_lc_s20_api_dto_replay_path_accepts_fixture`

## 8. Placeholder/internal-token guards

`find_user_facing_leakage` in `persisted_replay_contract_v1.py` + `test_lc_s22_no_placeholder_or_internal_token_leakage`

## 9. Unit/display fidelity guards

`test_lc_s22_biomarker_display_fidelity_fields_in_fixture` (homocysteine row). Full LC-S8G matrix deferred.

## 10. Knowledge Bus surfacing guards

Preserved via prior sprint regression inclusion in guard preflight (LC-S16/17/19, LC-S18).

## 11. What remains deferred

- Playwright stored-result render smoke
- Frontend mock sync automation
- Sentinel runner auto-discovery of scaffold packs (manual pack JSON validation only)

## 12. Recommended next Sentinel work

- LC-S21: Playwright minimal results-route smoke using persisted fixture
- LC-S23: Split additional scaffold packs (`scaffold_payload_contract_v1`, `scaffold_why_registry_v1`) from escaped_defects catch-all
- Wire `sentinel_runner.py` to load all `scaffold_*.json` packs
