# ARCH-CONV-I-ALT-IDPROV-1 — Implementation and Verification Report

**Work ID:** `ARCH-CONV-I-ALT-IDPROV-1`  
**Branch:** `feature/arch-conv-i-alt-idprov-test-estate-restoration`  
**Risk / change type:** STANDARD / BEHAVIOUR  
**Status:** **CLOSED** — merged to `main` (`d865f87`); published to `origin/main`

## 1. Preflight

| Check | Result |
|---|---|
| Branch from current `main` | Yes |
| Stash | Empty (governed) |
| Working tree before start | Only staged prompt/hardening |
| `main` vs `origin/main` | Local `main` cleanly **2 commits ahead** of `origin/main` (docs-only headline investigation merge `6f4b094`); no remote-only commits; disposition understood before start |
| Production files changed | **None** |

## 2. Pre-change failure evidence

From repository root (`pytest backend/tests/unit/test_arch_rt_identity_prov_1.py`):

**Seven genuine failures** (WHY fail-closed on piloted `signal_alt_high` synthetic frames):

1. `test_report_and_output_authority_preserve_both_frames`
2. `test_clinician_report_retains_multi_findings_without_silent_singleton`
3. `test_root_cause_compiler_emits_finding_per_frame_for_shared_signal_id`
4. `test_dto_serialization_preserves_multiple_frames`
5. `test_persistence_replay_round_trip_preserves_activation_identity_and_provenance`
6. `test_deterministic_ordering_across_repeated_executions`
7. `test_three_or_more_simultaneous_frames`

**False eighth (path artefact):**

- `test_package_manifest_schema_declares_source_spec_id`
- Passes from repository root
- Fails from `backend/` with `FileNotFoundError: knowledge_bus\schema\package_manifest_schema.yaml` due to relative path

No production path uses `signal_alt_high::inv_alt_high_frame_*`. Failures are fixture fragility against the ARCH-CONV-I pilot-cohort boundary, not a runtime defect.

## 3. Fixture strategy

**Chosen: Option A — Explicit synthetic non-pilot fixture isolation**

- Identity: `signal_test_synthetic_multiframe_v1`
- Frames: `inv_test_synthetic_multiframe_frame_{a,b,c}`
- Guard: `_require_synthetic_non_pilot()` asserts `not is_pilot_signal_id(...)` so future pilot migration fails loudly
- Root-cause test: monkeypatches `_ROOT_CAUSE_TARGETS` to the synthetic id with a test-only hypotheses loader (no dynamic `_ROOT_CAUSE_TARGETS[0]`)
- Rationale: least coupled to product rollout; cannot silently recur when more real signals enter `_PILOT_SIGNAL_IDS`; no production/register changes

## 4. Changes

| File | Change |
|---|---|
| `backend/tests/unit/test_arch_rt_identity_prov_1.py` | Synthetic non-pilot fixtures; schema path via `REPO_ROOT`; root-cause monkeypatch |
| `backend/scripts/run_baseline_tests.py` | Add `tests/unit/test_arch_rt_identity_prov_1.py` (cwd already `backend/`) |

## 5. Verification

| Check | Result |
|---|---|
| Full file from repo root | **22 passed** |
| Full file from `backend/` | **22 passed** |
| Schema path robustness both cwds | PASS |
| `test_arch_conv_pkgc_2_provenance_identity.py` | PASS |
| Zero `backend/core/` changes | Confirmed |
| Obsolete `inv_alt_high_frame_*` positive fixtures | Removed (docstring historical mention only) |

## 6. Carry-forward

`CF-ARCH-CONV-I-ALT-IDPROV-1` → **Resolved** (corrected: seven genuine failures + one path artefact; no production defect).
