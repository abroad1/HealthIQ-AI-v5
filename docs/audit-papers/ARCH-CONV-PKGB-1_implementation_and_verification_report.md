# ARCH-CONV-PKGB-1 — Implementation and Verification Report

**Work ID:** `ARCH-CONV-PKGB-1`  
**Branch:** `feature/arch-conv-pkgb-1-homocysteine-exclusivity-resolver-closure`  
**Risk / change type:** HIGH / MIXED  
**Gate 1:** `ARCH-CONV-PKGB-1-GATE1-HMR-2026-08-02` (`APPROVED_WITH_NARROWING`)  
**Gate 2:** `ARCH-CONV-PKGB-1-GATE2-ANTHONY-2026-08-02` (`APPROVED`)  
**Hardening:** `automation_bus/latest_prompt_hardening.json` — `HARDENED`  
**Implementation owner:** Cursor (`healthiq-core-engine`)

## 1. Baseline proof

| Check | Result |
|---|---|
| Phase 0 baseline counts | `COMPILED_ACTIVE=26`, `LEGACY_RETIRED=25`, `REJECTED=1`, frames=52 |
| Elevation-context authority | Absent from pilot / register → live `"legacy"` emit |
| Bare zero-compiled pilots | Five all-`LEGACY_RETIRED` families → bare-key `fail_closed` |
| Stash | Empty throughout |
| Active WP | Resumed after Gate 2 without re-`start` |

## 2. Source-to-runtime rule map

| Ratified rule | Runtime representation |
|---|---|
| `signal_homocysteine_elevation_context` = `FOLD_SUPPRESS` | Pilot membership + `LEGACY_RETIRED` row → `skip` |
| Independent WHY ownership/emission prohibited | Compiler skips; no legacy shared-file emit for elevation-context |
| New hypothesis / narrative prohibited | No new compiled artefact; shared YAML unchanged on disk |
| `signal_homocysteine_high` compiled content unchanged | B-vitamin + renal `COMPILED_ACTIVE` artefacts untouched |
| Bare-key zero-compiled → governed skip | `resolve_frame_why_authority` bare branch |
| Genuine ambiguity / missing governance → fail closed | Multi-`COMPILED_ACTIVE` bare; unknown keyed row |
| No new medical content for five zero-compiled pilots | Skip only; no `COMPILED_ACTIVE` added |
| HbA1c / urate assertion alignment | Test IDs only |
| L-04 / L-05 / L-06 out of scope | Untouched |

## 3. Mechanism chosen

**Option A — WHY-only retirement via existing authority model** (narrowest proven pattern; mirrors ARCH-CONV-I hepatic_alt retirement):

1. Add `signal_homocysteine_elevation_context` to `_PILOT_SIGNAL_IDS`.
2. Add register row `signal_homocysteine_elevation_context::inv_elevation_context` as `LEGACY_RETIRED`.
3. Leave shared `hcy_hypotheses_v1.yaml` and dual `RootCauseTargetSpec` registrations on disk.
4. Fix bare-key zero-`COMPILED_ACTIVE` path to return `skip` when all rows are unambiguously non-owning.

## 4. Files changed (implementation)

- `backend/core/knowledge/why_authority_v1.py`
- `knowledge_bus/governance/compiled_why_authority_register_v1.yaml`
- `backend/scripts/validate_compiled_why_authority_gate.py`
- `backend/tests/regression/test_arch_conv_pkgb_1_exclusivity_resolver.py` (new)
- `backend/tests/unit/test_why_authority_pkg3.py`
- `backend/tests/unit/test_root_cause_v1_homocysteine.py`
- `backend/tests/fixtures/panels/phenotypes/phenotype_expectations_v1.yaml`
- Gate / medical / hardening docs; Build Deliverables Register; carry-forward register
- This report

## 5. Register delta

| State | Before | After | Delta |
|---|---|---|---|
| frames | 52 | 53 | +1 |
| `COMPILED_ACTIVE` | 26 | 26 | 0 |
| `REJECTED` | 1 | 1 | 0 |
| `LEGACY_RETIRED` | 25 | 26 | +1 |

## 6. Verification

| Gate / suite | Result |
|---|---|
| `test_arch_conv_pkgb_1_exclusivity_resolver.py` | PASS |
| `test_root_cause_v1_homocysteine.py` | PASS |
| ARCH-CONV-F / G / H / I regression suites | PASS |
| `validate_compiled_why_authority_gate.py` | PASS |
| `run_architecture_validation_gate.py` | PASS |
| `run_baseline_tests.py` (incl. phenotype suite) | PASS |
| `verify_three_layer_pipeline.py` | PASS |

## 7. Baseline coverage check

`backend/tests/unit/test_root_cause_v1_homocysteine.py` was **not** added to `run_baseline_tests.py`.

Reason: the file mixes golden-panel / acceptance harness runs with direct compiler unit checks. Adding the whole file would broaden the infra-free baseline gate beyond proportionate curated coverage. Phenotype expectation updates already restore baseline visibility for elevation-context FOLD_SUPPRESS. Recommend a future dedicated lightweight unit extraction if baseline coverage of bare-key / exclusivity is required without golden panels.

## 8. Explicit non-changes

- No change to `signal_homocysteine_high` compiled medical content
- No new TC / LDL / HDL / HGB / hepatic-alt compiled authority
- No L-04 / L-05 / L-06 behaviour change
- No Package C replay/versioning
- No package / PSI / scoring / frontend activation changes (package activation keys retained)

## 9. Carry-forwards

- Closed: `CF-ARCH-CONV-DUAL-HCY-1` (dual elevation-context WHY emit)
- Remains open: Package B Wave 2 (L-04/L-05/L-06), Package C items, physical shared-YAML retirement (optional later hygiene; not required for exclusivity)

## 10. Closure posture

Ready for kernel `finish`, then independent Claude Code audit, GPT architectural review, and Anthony merge authority. Do not merge from this agent.
