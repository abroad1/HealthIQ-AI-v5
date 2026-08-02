---
work_id: ARCH-CONV-PKGB-1
branch: feature/arch-conv-pkgb-1-homocysteine-exclusivity-resolver-closure
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# ARCH-CONV-PKGB-1 — Homocysteine Dual-Authority Exclusivity and Shared Resolver Defect Closure

## Purpose

Deliver the first concrete Package B outcome:

- eliminate live dual-authority WHY output for the homocysteine family;
- implement the already-ratified `FOLD_SUPPRESS` disposition for `signal_homocysteine_elevation_context`;
- correct the shared bare-activation-key resolver defect affecting pilot signal families with no `COMPILED_ACTIVE` row;
- absorb the two stale HbA1c and urate hypothesis-ID regression assertions into the same bounded implementation sprint.

This sprint must not expand into Package B Wave 2 fallback quarantine, cross-producer precedence, family aggregation policy, or Package C replay/versioning work.

## Governing sources

Read and apply:

- `AUTOMATION_BUS_SOP_v1.3.1.md`
- `KNOWLEDGE_BUS_SOP_v1.3.1.md`
- `KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md`
- `docs/architecture/ARCH-CONV-A_stage0_outcome_and_package_boundary.md`
- `docs/architecture/ARCH-CONV-A_phase1_target_to_frame_map.md`
- `docs/architecture/ARCH-CONV_legacy_dependency_register.md`
- `automation_bus/latest_pipeline_advisory.md`
- `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`
- relevant ARCH-CONV-PKG3, A Wave 0, G, H and I decision/evidence artefacts

## Stage 1A — Authority preflight

Before implementation, verify and record:

1. The current compiled-WHY authority for `signal_homocysteine_high`.
2. The current live legacy WHY path for `signal_homocysteine_elevation_context`.
3. The shared physical asset and loader/registry wiring:
   - `hcy_hypotheses_v1.yaml`
   - its loader
   - both `RootCauseTargetSpec` registrations
4. The ratified `FOLD_SUPPRESS` disposition for `signal_homocysteine_elevation_context`.
5. The current behaviour of:
   - `resolve_frame_why_authority`
   - bare-activation-key resolution
   - fail-closed handling in `root_cause_compiler_v1.py`
6. Every pilot `signal_id` with zero `COMPILED_ACTIVE` rows, not only `signal_total_cholesterol_high`.
7. The current failing assertions in `backend/tests/unit/test_root_cause_v1_homocysteine.py`.
8. That no new medical research, compiled hypothesis content, signal identity, package activation or frontend behaviour is required.
9. That L-04 `why_engine_fallback_v1`, L-05 `_why_template`, and L-06 family-level aggregation remain outside this sprint.

Record exact paths and line references in the Phase 0 evidence pack.

## Stage 1B — Reality check

Confirm on current `main` that:

- `signal_homocysteine_elevation_context` still reaches legacy WHY content;
- `signal_homocysteine_high` already has compiled-WHY authority;
- both identities still reference the shared homocysteine hypothesis asset or selector path;
- the bare-key resolver still raises for `signal_total_cholesterol_high`;
- the HbA1c and urate hypothesis-ID tests are stale in the shared regression file;
- the defects are not already resolved.

If any statement is false, STOP and re-scope rather than creating a no-op sprint.

## Stage 1C — Intelligence preflight

Identify all affected Intelligence Core surfaces, including at minimum:

- `backend/core/knowledge/why_authority_v1.py`
- `backend/core/knowledge/root_cause_registry_v1.py`
- homocysteine hypothesis loader and asset
- `backend/core/analytics/root_cause_compiler_v1.py`
- compiled-WHY authority register
- legacy root-cause authority register
- output-authority/provenance projection where relevant
- shared root-cause regression tests
- architecture and compiled-WHY gates

Expected behaviour change must be limited to:

1. `signal_homocysteine_elevation_context` no longer independently emitting legacy WHY content.
2. Bare-key resolution for a pilot family with no compiled-active row returning a governed non-emitting disposition rather than raising.
3. Stale tests reflecting already-ratified HbA1c and urate compiled hypothesis IDs.

# Phase 0 — Mandatory Gate 1 / Gate 2 preparation

After kernel start, perform repository mapping only.

Create and commit:

- `docs/architecture/ARCH-CONV-PKGB-1_hardening_pack.md`
- `docs/architecture/ARCH-CONV-PKGB-1_medical_decision_register.yaml`
- `docs/architecture/ARCH-CONV-PKGB-1_GATE_1_GATE_2_decision.md`

## Gate 1 questions

Head of Medical Research must confirm:

1. `signal_homocysteine_elevation_context` remains `FOLD_SUPPRESS`.
2. It must not independently own or emit WHY content.
3. No new medical hypothesis or replacement narrative is required for that identity.
4. `signal_homocysteine_high` compiled content remains unchanged.
5. The total-cholesterol resolver correction is mechanical authority handling only and must not create new medical content.
6. The HbA1c and urate test corrections are assertion alignment only and must not alter runtime content.
7. No L-04/L-05/L-06 product-policy decision is being made in this sprint.

## Gate 2

Anthony must ratify Gate 1 exactly.

No runtime implementation is authorised until both decisions are recorded on disk and agree.

## Mandatory STOP

After committing the Phase 0 pack:

- STOP.
- Keep the work package `IN_PROGRESS`.
- Do not alter resolver behaviour.
- Do not disconnect or split the shared homocysteine asset.
- Do not change authority registers.
- Do not modify test expectations.
- Do not touch L-04, L-05, L-06 or Package C.
- Report the exact Gate 1 decision required.

# Phase 1 — Implementation after Gate 1 and Gate 2 only

Implement the ratified disposition with the smallest safe mechanism.

## A. Homocysteine exclusivity

Ensure:

- `signal_homocysteine_elevation_context` cannot independently emit legacy WHY content;
- `signal_homocysteine_high` remains the sole compiled-WHY owner for the ratified homocysteine-high frame;
- no fallback path silently restores the retired/suppressed elevation-context WHY;
- package, PSI, card, signal activation and compiled homocysteine content remain unchanged.

Use the existing authority model. Do not invent a new medical hypothesis, signal identity, alias or compiler path.

The final implementation may:

- disconnect the legacy identity from the shared selector;
- split the registry path;
- add a governed skip/retired disposition;
- or use another existing mechanism proven by Phase 0.

Choose the narrowest implementation that satisfies exclusivity and preserves determinism.

## B. Shared bare-key resolver defect

Fix `resolve_frame_why_authority` so that a pilot `signal_id` with zero `COMPILED_ACTIVE` rows does not unconditionally cause a runtime `ValueError` when resolved without an activation key.

Requirements:

- return a governed non-emitting/skip disposition when all relevant rows are retired/rejected/non-owning;
- preserve fail-closed behaviour for genuine ambiguity or missing governance;
- do not create compiled authority for `signal_total_cholesterol_high`;
- do not revive legacy total-cholesterol WHY;
- inspect and disclose every pilot signal family with zero `COMPILED_ACTIVE` rows;
- add tests for each affected structural class, not only the one observed example.

## C. Stale test corrections

Update only the stale assertions to the already-ratified IDs:

- HbA1c: `hyp_hba1c_elevated_glycaemia_context`
- Urate: `hyp_urate_elevated_non_causal_context`

Do not alter production content to satisfy old tests.

# Explicit exclusions

Do not:

- change `signal_homocysteine_high` compiled medical content;
- add independent WHY authority for `signal_homocysteine_elevation_context`;
- alter homocysteine activation logic, thresholds, package reachability, PSI or frontend output;
- create new total-cholesterol medical content;
- add total cholesterol to `COMPILED_ACTIVE`;
- change lipid activation or scoring;
- alter L-04 `_compile_why_engine_fallback_finding`;
- alter L-05 `_why_template`;
- decide or change L-06 family aggregation;
- begin Package C replay, provenance, waist remediation or result versioning;
- introduce a new fallback parser or compiler mechanism;
- read raw research at runtime;
- make governance-only or register-only changes without the corresponding runtime proof.

# Tests

Add a dedicated regression suite:

`backend/tests/regression/test_arch_conv_pkgb_1_exclusivity_resolver.py`

At minimum prove:

1. `signal_homocysteine_elevation_context` does not independently emit WHY.
2. `signal_homocysteine_high` compiled WHY remains unchanged.
3. A panel containing both identities produces only the ratified compiled homocysteine WHY.
4. No legacy/fallback path restores the suppressed elevation-context content.
5. Bare-key `signal_total_cholesterol_high` no longer raises.
6. Total cholesterol remains non-owning and emits no invented compiled WHY.
7. Every pilot family with zero `COMPILED_ACTIVE` rows resolves deterministically.
8. Genuine ambiguous or ungoverned cases still fail closed.
9. HbA1c and urate assertions use the ratified hypothesis IDs.
10. ARCH-CONV-F, G, H and I regression suites remain green.
11. Package, PSI, scoring, frontend and SSOT state remain unchanged.
12. No L-04/L-05/L-06 behaviour changes.

Run at minimum:

- the new regression suite;
- `backend/tests/unit/test_root_cause_v1_homocysteine.py`;
- ARCH-CONV-F/G/H/I regression suites;
- `python backend/scripts/validate_compiled_why_authority_gate.py`;
- architecture validation gate;
- baseline tests required by the Automation Bus;
- three-layer pipeline verification.

## Baseline coverage check

Because the shared root-cause unit file was previously absent from the curated baseline suite, determine whether it should be added to `backend/scripts/run_baseline_tests.py`.

If adding it is safe and proportionate, include it so these failures cannot remain invisible.

If adding it would introduce unrelated unstable coverage, STOP and report rather than silently broadening the baseline gate.

# STOP conditions during implementation

STOP if:

- Gate 1 and Gate 2 do not match;
- exclusivity requires changing compiled homocysteine medical content;
- the legacy elevation-context identity cannot be suppressed without changing package/signal activation;
- the resolver correction would convert ambiguity into silent skipping;
- any pilot family with zero `COMPILED_ACTIVE` rows has a materially different governance shape requiring separate adjudication;
- total cholesterol requires new medical content or authority;
- L-04/L-05/L-06 behaviour must change;
- any Package C file or behaviour must change;
- any unrelated compiled-WHY authority or register row changes;
- any regression cannot be attributed and bounded.

# Evidence and closure

Produce:

- `docs/audit-papers/ARCH-CONV-PKGB-1_implementation_and_verification_report.md`
- updated Gate decision record
- updated medical decision register
- updated Build Deliverables Register entry
- updated central carry-forward register only for genuinely closed or newly exposed obligations

Before `finish`, complete the mandatory Post-Implementation Closure Protocol.

Run kernel finish only after:

- implementation and tests are complete;
- repo hygiene is proven;
- no unrelated files remain;
- all required gates pass.

Do not merge.

After kernel COMPLETE, stop for independent Claude Code audit, GPT architectural review and Anthony merge authority.
