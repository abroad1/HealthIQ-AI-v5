---
work_id: ARCH-CONV-PKGC-2
title: Provenance-Identity Bare-Key Closure
risk_level: PROVISIONAL
change_type: MIXED
execution_model: TWO_PHASE_START_FINISH
branch: feature/arch-conv-pkgc-2-provenance-identity-closure
---

# ARCH-CONV-PKGC-2 — Provenance-Identity Bare-Key Closure

## Authority and operating mode

Execute under:

- `AUTOMATION_BUS_SOP_v1.3.1.md`
- `KNOWLEDGE_BUS_SOP_v1.3.1.md` where applicable
- the current Automation Bus hardening protocol
- the current repository architecture and carry-forward governance
- `automation_bus/latest_pipeline_advisory.md`
- `docs/architecture/ARCH-CONV_legacy_dependency_register.md`
- `docs/architecture/ARCH-CONV_programme_closure_record.md`
- `docs/sprints/launch_core_carry_forward_register.md`
- `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`
- the current implementation of `output_authority_provenance_builder_v1.py`
- the current provenance regression tests

This is the second Package C work package produced by the Stage 0 bundling split.

Do not absorb waist-unit remediation, full result-versioning advancement, regeneration-job work, DB-lineage-table work, compiled-WHY migration, or signal-authority redesign.

## Product outcome

Close `CF-ARCH-CONV-PROV-1` by:

1. replacing the synthetic bare-key provenance fixture with a real evaluated authority row;
2. adding defensive validation that rejects non-canonical provenance identity before output-authority provenance is emitted;
3. proving all currently live activation keys are canonical and unaffected;
4. preserving fail-closed behaviour without changing medical content or authority decisions.

## Current Stage 0 finding

Repository investigation previously found:

- the suspect bare key `signal_homocysteine_high::inv_homocysteine_high` exists only as a synthetic test fixture;
- it does not appear in live governance registers;
- no known live emitter produces it;
- `output_authority_provenance_builder_v1.py` lacks a defensive validation guard against non-canonical activation keys;
- the risk is dormant but real.

Reverify all of these facts on current `main`.

## Provisional classification

The Stage 0 recommendation left risk unresolved:

- `HIGH` if `output_authority_provenance_builder_v1.py` is an Intelligence Core output-assembly component under Automation Bus SOP v1.3.1;
- otherwise `STANDARD` if it is contract-adjacent DTO/provenance validation only.

Do not assume either classification.

# Stage 1A — Mandatory risk and boundary classification

Before implementation, inspect and record:

1. The full implementation of `output_authority_provenance_builder_v1.py`, all direct callers, all output DTOs/contracts it populates, and all consumers of its output.
2. Whether it changes medical interpretation, selects or ranks hypotheses, changes signal/frame authority, changes clinical narrative, changes report inclusion, or only serialises/validates already-decided provenance.
3. Its current architecture classification in repository documents.
4. Whether prior sprints treated it as Intelligence Core, contract-adjacent, DTO/output assembly, or boundary code.
5. The exact canonical activation-key contract and where it is defined.
6. Every live source of activation keys entering the provenance builder.
7. Every current live activation key emitted by compiled-WHY authority, legacy authority, package/signal evaluation, report compilation, and any production-modelled test fixture.
8. Whether the suspicious bare key exists anywhere outside synthetic tests.
9. Whether malformed keys can currently reach production output.
10. Whether validation belongs in the provenance builder, a shared identity constructor, a registry boundary, or an earlier emitter.

## Classification decision

The hardening pack must conclude exactly one of:

- `RISK_CLASSIFICATION: HIGH — INTELLIGENCE_CORE`
- `RISK_CLASSIFICATION: STANDARD — CONTRACT_ADJACENT`

### If HIGH

STOP after Phase 0 mapping and prepare Gate 1/Gate 2 material.

No runtime implementation is authorised until Gate 1 confirms the validation is mechanical only and must not alter medical authority or content, and Anthony ratifies Gate 1 exactly.

### If STANDARD

No medical Gate 1/Gate 2 is required, but proceed only after the hardening pack proves:

- no medical interpretation changes;
- no authority-state changes;
- no live canonical key is rejected;
- no output-contract shape changes except fail-closed rejection of malformed identity.

# Stage 1B — Reality check

Confirm on current `main` that:

- the synthetic bare-key fixture still exists;
- it is not backed by a real live evaluated authority row;
- the provenance builder still lacks defensive canonical-key validation;
- no live governance register contains the malformed key;
- no live emitter currently produces it;
- the carry-forward item remains open;
- the sprint is not already complete.

If any premise is false, STOP and re-scope.

# Stage 1C — Hardening deliverables

Harden `automation_bus/latest_cursor_prompt.md` and create:

- `docs/architecture/ARCH-CONV-PKGC-2_hardening_pack.md`
- `docs/architecture/ARCH-CONV-PKGC-2_identity_contract_map.md`
- `docs/architecture/ARCH-CONV-PKGC-2_GATE_1_GATE_2_decision.md` only if classified HIGH

The hardening pack must include:

- final risk classification;
- exact canonical activation-key grammar;
- authoritative source of that grammar;
- all live emitters;
- all live keys sampled or enumerated;
- malformed-key examples;
- exact validation boundary;
- expected exception/failure contract;
- fixture-replacement plan;
- test matrix;
- rollback plan;
- explicit exclusions.

# Phase 0 — Mandatory STOP conditions

STOP before implementation if:

- risk is HIGH and Gate 1/Gate 2 are not recorded;
- the canonical identity contract is not unambiguous;
- more than one incompatible activation-key grammar exists;
- any currently live key would be rejected by the proposed guard;
- the suspicious bare key is actually emitted in live runtime;
- fixing it requires authority-register or medical-content changes;
- the correct validation boundary cannot be established;
- the change would alter report inclusion or clinical narrative;
- the carry-forward item is inaccurately scoped.

# Phase 1 — Implementation

Proceed only after all required Phase 0 conditions are satisfied.

## A. Canonical identity validation

Add the narrowest safe validation mechanism that ensures provenance output uses canonical activation identity.

Requirements:

1. Validate against the repository's existing canonical activation-key contract.
2. Reuse an existing parser, constructor or registry helper if one exists.
3. Do not create a second competing identity grammar.
4. Reject malformed or bare activation keys before provenance output is emitted.
5. Preserve valid canonical keys unchanged.
6. Preserve deterministic output ordering and shape.
7. Fail closed with a clear, testable error or governed omission according to the existing output contract.
8. Do not silently rewrite malformed keys into guessed canonical identities.
9. Do not derive missing investigation identity from signal identity alone.
10. Do not create new authority rows or medical content.

The implementation location must follow the hardening evidence. Do not force the guard into the provenance builder if a more authoritative shared boundary already exists.

## B. Synthetic fixture replacement

Replace the synthetic malformed fixture in the provenance test with a real evaluated authority row or repository-backed production-equivalent fixture.

Requirements:

1. The replacement must use a canonical live-shaped activation key.
2. It must exercise the actual evaluation path used in production.
3. It must not fabricate an authority state that cannot exist.
4. Keep a separate negative test proving malformed bare keys are rejected.
5. Do not weaken existing assertions merely to make the new guard pass.
6. Do not change expected medical content.

## C. Carry-forward closure

Close `CF-ARCH-CONV-PROV-1` only if:

- the malformed synthetic fixture is removed or explicitly converted into a negative test;
- canonical-key validation is live;
- all current live keys pass;
- malformed keys fail closed;
- no authority or content behaviour changes;
- all regression and architecture gates pass.

# Explicit exclusions

Do not:

- modify waist-unit code or records;
- reopen `ARCH-CONV-PKGC-1`;
- implement `CF-ARCH-CONV-VERSION-1`;
- build regeneration;
- implement `CF-MEDREV2-002`;
- change compiled-WHY or legacy authority states;
- add or remove signal activation;
- alter hypotheses, narratives, ranking, report inclusion or clinical wording;
- introduce aliases between malformed and canonical keys;
- infer an investigation ID;
- alter package, PSI, SSOT or frontend medical logic;
- redesign provenance output schema;
- broaden into general identity-registry refactoring.

# Required tests

Add a focused regression suite for `ARCH-CONV-PKGC-2`.

At minimum prove:

## Canonical identity

1. Every currently live canonical activation key passes validation.
2. The real evaluated authority-row fixture produces expected provenance.
3. A bare signal-only key is rejected.
4. A signal-plus-wrong-investigation key is rejected if the contract requires registry membership.
5. Missing activation key fails according to the existing governed contract.
6. Unknown signal identity fails closed.
7. Unknown investigation identity fails closed.
8. Malformed delimiter or empty segments fail closed.
9. Validation does not alter canonical key text.
10. Validation is deterministic.

## Provenance behaviour

11. Valid provenance output remains byte-for-byte or structurally unchanged.
12. No medical content, authority state, ranking or report inclusion changes.
13. Existing provenance tests remain green.
14. The former malformed synthetic fixture cannot masquerade as a production-valid case.
15. Negative malformed-key tests are explicit and isolated.
16. Multiple valid rows preserve existing ordering and deduplication.
17. Error handling does not leak partial or misleading provenance.

## Non-regression

18. Compiled-WHY authority gates remain green.
19. Root-cause and report-compiler regression suites remain green.
20. Package, PSI, SSOT and frontend state remain unchanged.
21. Result-versioning and waist-unit behaviour remain unchanged.
22. Architecture validation, baseline and three-layer pipeline pass.

# Verification

Run at minimum:

- the new `ARCH-CONV-PKGC-2` regression suite;
- all existing output-authority provenance tests;
- relevant authority-registry and activation-key tests;
- relevant report-compiler and DTO contract tests;
- compiled-WHY authority validation;
- architecture validation gate;
- baseline test suite;
- three-layer pipeline verification;
- a repository-wide search proving the malformed key is absent from live governance/configuration and retained only in explicit negative-test context, if anywhere.

# STOP conditions during implementation

STOP if:

- risk classification changes;
- a Gate is required but absent;
- any live canonical key fails;
- malformed identity exists in live production data or governance;
- fixing the issue requires a new authority decision;
- validation changes report inclusion or medical output;
- the guard requires guessing missing identity;
- more than one canonical grammar is found;
- the change expands into PKGC-1, result versioning, regeneration or compiled-WHY;
- unrelated regressions cannot be bounded and attributed.

# Evidence and closure

Produce:

- `docs/audit-papers/ARCH-CONV-PKGC-2_implementation_and_verification_report.md`
- final `docs/architecture/ARCH-CONV-PKGC-2_hardening_pack.md`
- final `docs/architecture/ARCH-CONV-PKGC-2_identity_contract_map.md`
- final Gate decision record if HIGH
- updated `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`
- updated `docs/sprints/launch_core_carry_forward_register.md`

Complete the mandatory Post-Implementation Closure Protocol before kernel finish.

Run `python backend/scripts/run_work_package.py finish` only when:

- implementation is complete;
- all required gates are satisfied;
- all tests and architecture checks pass;
- carry-forward closure is accurate;
- no out-of-scope files are present;
- repository and stash hygiene are clean.

Do not merge.

After kernel `COMPLETE`, stop for independent Claude Code audit, GPT architectural review and Anthony merge authority.
