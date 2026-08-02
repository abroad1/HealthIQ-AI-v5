---
work_id: ARCH-CONV-I-ALT-IDPROV-1
title: Identity/Provenance Multi-Frame Test-Estate Restoration
risk_level: STANDARD
change_type: BEHAVIOUR
execution_model: TWO_PHASE_START_FINISH
branch: feature/arch-conv-i-alt-idprov-test-estate-restoration
---

# ARCH-CONV-I-ALT-IDPROV-1 — Identity/Provenance Multi-Frame Test-Estate Restoration

## Authority and operating mode

Execute under:

- `AUTOMATION_BUS_SOP_v1.3.1.md`
- the current Automation Bus hardening protocol
- `automation_bus/latest_pipeline_advisory.md`
- `docs/architecture/ADR-RT-002_signal_spec_identity_and_registry_policy(1).md`
- `docs/architecture/ARCH-CONV-I_hardening_pack.md`
- `docs/architecture/ARCH-CONV-I_GATE_1_GATE_2_decision.md`
- `docs/architecture/ARCH-CONV-I_medical_decision_register.yaml`
- `docs/audit-papers/ARCH-CONV-I_implementation_and_verification_report.md`
- `docs/architecture/ARCH-CONV-PKGC-2_identity_contract_map.md`
- `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`
- `docs/sprints/launch_core_carry_forward_register.md`

This is a bounded, test-estate-only restoration sprint.

Do not modify production runtime code, medical content, signal authority, compiled-WHY content, package activation, provenance runtime behaviour, result versioning, frontend behaviour or any governance register other than the two delivery/carry-forward records required for closure.

## Product/architecture outcome

Restore pilot-cohort-migration-safe regression coverage for:

- multi-frame activation identity preservation;
- report compilation preserving multiple findings for one signal;
- clinician-report avoidance of silent singleton collapse;
- DTO serialisation preserving all activation keys;
- persistence/replay round-trip fidelity;
- deterministic ordering;
- root-cause compiler per-frame emission;
- package-manifest schema path robustness.

Then add the repaired test file to the governed baseline suite so future Package A/B migrations cannot silently break this contract again.

## Repository-verified Stage 0 findings

The current carry-forward records eight failures, but Stage 0 re-verification established:

- only seven tests genuinely fail for the recorded architecture reason;
- `test_package_manifest_schema_declares_source_spec_id` passes when pytest is invoked from repository root;
- its prior failure was caused by a working-directory-dependent relative path;
- the seven genuine failures occur before their assertions because the test fixtures use synthetic or dynamically selected activation identities that now correctly hit the pilot-cohort fail-closed boundary;
- no production path uses `signal_alt_high::inv_alt_high_frame_*`;
- no production runtime defect was identified;
- the coverage remains architecturally required;
- the debt is fixture fragility, not obsolete test intent.

## Exact scope

Modify only:

- `backend/tests/unit/test_arch_rt_identity_prov_1.py`
- `backend/scripts/run_baseline_tests.py`
- standard sprint evidence/closure documents
- `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`
- `docs/sprints/launch_core_carry_forward_register.md`

No production file under `backend/core/` may change.

No file under `knowledge_bus/`, `backend/ssot/` or `frontend/` may change.

# Stage 1A — Mandatory preflight and reality check

Before implementation:

1. Confirm branch creation from current `main`.
2. Confirm `main == origin/main`.
3. Confirm working tree and stash state.
4. Read `backend/tests/unit/test_arch_rt_identity_prov_1.py` in full.
5. Re-run the file from repository root.
6. Re-run the file from `backend/` or the exact invocation context that caused the prior false eighth failure.
7. Confirm exactly seven genuine fail-closed failures and one path-dependent robustness issue.
8. Confirm the seven failing tests are:

   - `test_report_and_output_authority_preserve_both_frames`
   - `test_clinician_report_retains_multi_findings_without_silent_singleton`
   - `test_dto_serialization_preserves_multiple_frames`
   - `test_persistence_replay_round_trip_preserves_activation_identity_and_provenance`
   - `test_deterministic_ordering_across_repeated_executions`
   - `test_three_or_more_simultaneous_frames`
   - `test_root_cause_compiler_emits_finding_per_frame_for_shared_signal_id`

9. Confirm `test_package_manifest_schema_declares_source_spec_id` passes from repository root.
10. Confirm `signal_alt_high::inv_alt_high_frame_*` appears only in this test file.
11. Confirm no production path depends on those synthetic identities.
12. Confirm the underlying production behaviour is already correct and the failures occur only because fixture construction reaches the governed fail-closed boundary.

If any of these findings differs materially, STOP and re-scope.

# Stage 1B — Fixture strategy decision

Choose one robust fixture-isolation strategy for the seven genuine failing tests.

Permitted strategies:

## Option A — Explicit synthetic non-pilot fixture isolation

Use a clearly synthetic test-only signal identity, for example:

`signal_test_synthetic_multiframe_v1`

and ensure the test explicitly isolates it from `_PILOT_SIGNAL_IDS` for the duration of the test using the narrowest safe fixture/monkeypatch mechanism.

Requirements:

- no production registry entry;
- no production authority row;
- no production code change;
- test-only isolation;
- deterministic restoration after test execution;
- no global state leakage across tests.

## Option B — Explicit real non-pilot target with migration guard

Use a currently non-pilot real target only if:

- the target is appropriate for the test behaviour;
- each affected test explicitly asserts the target remains outside `_PILOT_SIGNAL_IDS`;
- failure messaging clearly states that a future pilot migration requires fixture review;
- no current medical/authority content is relied upon beyond the mechanics under test.

Do not simply hardcode another currently safe signal without a guard.

## Required choice

Prefer the strategy that:

- is least coupled to current product rollout state;
- cannot silently recur when more signals become piloted;
- does not require production code or register changes;
- keeps the original behavioural assertions intact.

Record the chosen strategy and rationale in the implementation report.

# Phase 1 — Implementation

## A. Repair the six multi-frame mechanics tests

Repair:

- `test_report_and_output_authority_preserve_both_frames`
- `test_clinician_report_retains_multi_findings_without_silent_singleton`
- `test_dto_serialization_preserves_multiple_frames`
- `test_persistence_replay_round_trip_preserves_activation_identity_and_provenance`
- `test_deterministic_ordering_across_repeated_executions`
- `test_three_or_more_simultaneous_frames`

Requirements:

1. Preserve the original architectural intent.
2. Keep multi-frame identities distinct.
3. Preserve activation-key fidelity through all exercised layers.
4. Do not weaken assertions.
5. Do not convert positive architecture-contract tests into negative fail-closed tests.
6. Do not use a real governed activation key in a way that couples the test to current medical content.
7. Ensure the fixture remains safe if future Package A/B waves add more signals to `_PILOT_SIGNAL_IDS`.

## B. Repair root-cause compiler per-frame test

Repair:

`test_root_cause_compiler_emits_finding_per_frame_for_shared_signal_id`

Requirements:

1. Remove the fragile `_ROOT_CAUSE_TARGETS[0]` dynamic-selection strategy.
2. Use the same migration-safe fixture strategy selected for the six tests above.
3. Preserve the assertion that one root-cause finding is emitted per activation frame, not per signal ID.
4. Do not change `root_cause_compiler_v1.py`.
5. Do not add new production registry or authority rows.

## C. Fix schema-path robustness

Repair:

`test_package_manifest_schema_declares_source_spec_id`

Requirements:

1. Replace the working-directory-dependent relative path with the existing repository-root helper already used in the same file.
2. Ensure the test passes from:
   - repository root;
   - `backend/`;
   - the baseline runner invocation.
3. Do not change the package manifest schema.

## D. Correct recorded failure count

Update closure records to state:

- seven genuine fail-closed fixture failures;
- one audit-invocation path artefact;
- no production defect.

Correct the carry-forward record from eight to seven genuine failures before closing it.

## E. Add to governed baseline suite

After the entire test file is green:

- add `backend/tests/unit/test_arch_rt_identity_prov_1.py` to `backend/scripts/run_baseline_tests.py`;
- use the repository’s established curated-baseline invocation pattern;
- ensure the baseline runner executes it from a stable working directory;
- do not broaden the baseline suite beyond this file.

# Explicit exclusions

Do not modify:

- `backend/core/knowledge/why_authority_v1.py`
- `backend/core/analytics/root_cause_compiler_v1.py`
- `backend/core/analytics/output_authority_provenance_builder_v1.py`
- `backend/core/knowledge/signal_result_index_v1.py`
- any authority or governance register
- any compiled-WHY content
- any signal package
- any PSI/SSOT/frontend file
- any medical narrative, hypothesis, ranking or activation logic
- any production identity grammar
- any runtime fallback or fail-closed behaviour

Do not make real registered ALT frames pass by weakening authority enforcement.

Do not add aliases for synthetic activation keys.

Do not retain `signal_alt_high::inv_alt_high_frame_*` as positive production-shaped fixtures.

# Required verification

## Focused test file

Run from repository root:

```text
pytest backend/tests/unit/test_arch_rt_identity_prov_1.py
```

Run from `backend/` using the equivalent supported invocation.

All tests in the file must pass under both contexts.

## Behaviour preservation

Prove:

1. Two frames of one signal survive report compilation.
2. Clinician output does not silently collapse multiple findings to one.
3. DTO serialisation preserves all activation keys.
4. Persistence/replay round-trip preserves activation identity and provenance.
5. Ordering remains deterministic across repeated executions.
6. Three or more simultaneous frames remain preserved.
7. Root-cause compiler emits one finding per frame.
8. Duplicate activation keys still fail closed.
9. Existing passing identity/provenance tests remain unchanged in behaviour.
10. Pilot-cohort fail-closed behaviour remains unchanged in production code.
11. Schema test passes from both invocation roots.

## Baseline inclusion

Run:

- the updated baseline suite;
- architecture validation gate;
- three-layer pipeline verification;
- relevant identity/provenance regression tests;
- relevant ARCH-CONV-I and ARCH-CONV-PKGC-2 regression suites.

Confirm the new baseline entry is exercised and not silently skipped.

# STOP conditions

STOP if:

- any repair requires a production file change;
- any authority register or compiled-WHY row must change;
- a real registered activation key fails for a reason other than the known fixture/pilot-cohort mismatch;
- a genuine runtime regression is discovered;
- more than this one test file shares the same fragile fixture pattern;
- baseline inclusion introduces unrelated instability;
- tests can only be made green by weakening fail-closed behaviour;
- any medical or authority decision becomes necessary;
- any scope outside the two declared implementation files is required.

If a STOP condition occurs, leave the work package `IN_PROGRESS` and report the new evidence without implementing out-of-scope remediation.

# Evidence and closure

Produce:

- `docs/audit-papers/ARCH-CONV-I-ALT-IDPROV-1_implementation_and_verification_report.md`
- updated `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`
- updated `docs/sprints/launch_core_carry_forward_register.md`

The implementation report must include:

- pre-change seven-failure evidence;
- explanation of the false eighth failure;
- selected fixture-isolation strategy;
- before/after test mapping;
- both working-directory invocation results;
- baseline inclusion proof;
- confirmation of zero production-code changes;
- confirmation that no live medical or authority behaviour changed.

Close `CF-ARCH-CONV-I-ALT-IDPROV-1` only when:

- all seven genuine failures are repaired;
- the path robustness issue is fixed;
- the complete test file passes under both invocation contexts;
- the file is included in the governed baseline suite;
- all required gates pass;
- no production file changed.

Complete the mandatory Post-Implementation Closure Protocol.

Run kernel finish only when:

- implementation is complete;
- required tests and gates pass;
- the working tree is clean except for permitted kernel status handling;
- stash state is governed;
- no out-of-scope files are present.

Do not merge.

After kernel `COMPLETE`, stop for independent Claude Code audit, GPT architectural review and Anthony merge authority.
