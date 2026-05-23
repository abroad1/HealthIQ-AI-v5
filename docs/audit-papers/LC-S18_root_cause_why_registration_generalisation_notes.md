# LC-S18 — Root Cause / WHY Registration Generalisation Notes

**Work package:** LC-S18  
**Branch:** `scaffold/lc-s18-root-cause-why-registration`  
**Date:** 2026-05-23

## 1. Preflight results

| Check | Result |
|-------|--------|
| Branch (start) | `main` → `scaffold/lc-s18-root-cause-why-registration` |
| Stash | Empty |
| Out-of-scope file | `frontend/.env.local.example` modified — **restored** (not in sprint scope) |
| Controlling docs | Present (scaffold definition, LC-S17, LC-S19) |
| Kernel start | Exit 0 after clean porcelain |
| Prior scaffold guards | All pass (including LC-S16/17/19) |

## 2. Current root-cause / WHY registration map

| Layer | Authority |
|-------|-----------|
| Compiler | `backend/core/analytics/root_cause_compiler_v1.py` — `compile_root_cause_v1` |
| Registry (LC-S18) | `backend/core/knowledge/root_cause_registry_v1.py` — `ROOT_CAUSE_TARGET_SPECS`, `get_root_cause_targets()` |
| Hypothesis assets | `knowledge_bus/root_cause/hypotheses/*.yaml` via `load_root_cause_hypotheses.py` |
| Fallback WHY | `_compile_why_engine_fallback_finding` — `why_engine_fallback_v1` when lead has no registered target |

## 3. Current registered target count (sprint start)

**41** targets in `ROOT_CAUSE_TARGET_SPECS` (discovered at sprint start from `root_cause_compiler_v1.py` `_ROOT_CAUSE_TARGETS`).

## 4. Fingerprint (before change)

Stored: `docs/audit-papers/LC-S18_root_cause_why_registration_before_fingerprint.json`

All 41 targets: `asset_loads=true`, `governed=true`, deterministic `hypothesis_asset_fingerprint` per target.

## 5. Package estate drift findings

`python backend/scripts/validate_kb_package_estate_orphans_v1.py` → exit 1

- **~109** package directories on disk not in `package_estate_KB-S49_v1.yaml`
- **0** inventory entries missing on disk
- Drift unchanged from LC-S16/17/19

**LC-S18 assessment:** Safe to proceed **without** auto-discovery. Orphan packages are **not** loaded into root-cause registration. Registration remains `manual_v1` specs only.

**STOP for auto-discovery:** Not triggered. Recommended follow-on: **LC-S18A — package estate inventory refresh** before metadata-only discovery from packages.

## 6. Proposed registration mechanism

**Pattern:** Hybrid manual table plus metadata validation (approved by human merge-authorised implementation request in-session).

| Question | Answer |
|----------|--------|
| Metadata-driven vs hybrid? | Hybrid: `RootCauseTargetSpec` rows + `validate_root_cause_registry()` |
| Required metadata | `signal_id`, `asset_filename`, `loader`, `registration_source` |
| Draft/unvalidated exclusion | No package scanning; `registration_source=manual_v1` only |
| Orphan handling | Reporter only; no auto-load |
| Malformed assets | `RootCauseRegistryValidationError` at validation |
| Duplicate IDs | Rejected loudly |
| Missing hypothesis file | Loader raises `FileNotFoundError` during validation |
| Deterministic ordering | Legacy list order preserved in `ROOT_CAUSE_TARGET_SPECS` tuple |
| Preserve current targets | Same 41 loaders/signal IDs |
| Future asset-first path | Add one `RootCauseTargetSpec` row + loader function (no compiler loop edit) |

## 7. GPT/Claude review checkpoint

Human authorised implementation in the same session (“implement … do not stop at start unless blocked”). Mechanism: **hybrid registry + validation**, no orphan auto-discovery.

## 8. Implementation summary

- Added `root_cause_registry_v1.py` with 41 `RootCauseTargetSpec` entries.
- `root_cause_compiler_v1.py` now calls `get_root_cause_targets()` (validates on import).
- CLI `fingerprint_root_cause_targets_v1.py` for audit JSON.
- Regression `test_lc_s18_root_cause_why_registration.py` + Sentinel defect classes.

## 9. Validation and failure-mode behaviour

| Failure | Behaviour |
|---------|-----------|
| Duplicate `signal_id` | `RootCauseRegistryValidationError` |
| Empty `signal_id` | `RootCauseRegistryValidationError` |
| Asset missing / invalid | Loader or validation error (not silent skip) |
| Unregistered fired signal | Unchanged: no finding unless lead fallback path applies |
| Unregistered lead | Explicit `why_engine_fallback_v1` finding |

## 10. Tests added/updated

- `backend/tests/regression/test_lc_s18_root_cause_why_registration.py` (new)

## 11. Sentinel updates

Added to `escaped_defects_v1.json`: `root_cause_target_not_loaded`, `why_asset_silent_skip`, `metadata_malformed_not_failed`, `why_output_changed_after_registration_migration`, `new_why_asset_requires_backend_code`, `orphan_why_asset_auto_loaded`, `duplicate_why_target_id_not_rejected`.

## 12. After fingerprint

`docs/audit-papers/LC-S18_root_cause_why_registration_after_fingerprint.json` — **equivalent** to before (all `hypothesis_asset_fingerprint` values match).

## 13. Residual risks

- New targets still need a loader function in `load_root_cause_hypotheses.py` (not fully metadata-only).
- Estate inventory stale; LC-S18A needed before package-metadata discovery.
- Runtime `SignalRegistry` still loads all packages (unchanged; out of scope).

## 14. Recommendation for LC-S20/22

1. **LC-S18A:** Refresh `package_estate_KB-S49_v1.yaml` from disk; close orphan drift.
2. **LC-S20/22:** Metadata-driven discovery limited to inventory-listed, validated packages with manifest `root_cause` block pointing at hypothesis asset path.
3. Optional: generate `RootCauseTargetSpec` rows from manifest at build/validate time (no runtime orphan scan).
