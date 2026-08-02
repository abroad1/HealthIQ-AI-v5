---
work_id: ARCH-CONV-PKGC-1
title: Historic Waist-Unit Stale-Detection and Remediation
risk_level: STANDARD
change_type: MIXED
execution_model: TWO_PHASE_START_FINISH
branch: feature/arch-conv-pkgc-1-waist-unit-remediation
---

# ARCH-CONV-PKGC-1 — Historic Waist-Unit Stale-Detection and Remediation

## Authority and operating mode

Execute under:

- `AUTOMATION_BUS_SOP_v1.3.1.md`
- the current Automation Bus hardening protocol
- the current repository architecture and carry-forward governance
- the locked LAUNCH-CORE-3 result-versioning, replay and regeneration policy
- `docs/audit-papers/WAIST_UNIT_LEGACY_IMPACT_AUDIT.md`
- `automation_bus/latest_pipeline_advisory.md`

This is a bounded Package C Wave 1 work package.

Do not absorb `ARCH-CONV-PKGC-2` provenance-identity work, full result-versioning advancement, or the deferred regeneration job.

## Product outcome

Close `CF-ARCH-CONV-WAIST-1` by:

1. adding the missing waist-unit stale-detection rule to the existing LAUNCH-CORE-3 stale-detection framework;
2. applying a governed, auditable disposition to the 12 analysis IDs identified in `WAIST_UNIT_LEGACY_IMPACT_AUDIT.md`;
3. preserving original historic values and sufficient lineage to explain every remediation action;
4. proving that unaffected results remain unchanged.

## Current Stage 0 decision

The work has been separated from provenance-identity closure because the two outcomes do not share implementation, testing, rollback or acceptance boundaries.

This sprint covers waist-unit stale detection and historic-row remediation only.

Expected classification:

```yaml
risk_level: STANDARD
change_type: MIXED
```

- `BEHAVIOUR`: one new stale-detection rule.
- `DATA`: governed treatment of the 12 historic analysis rows.

If repository mapping shows that the changed runtime path qualifies as Intelligence Core under Automation Bus SOP v1.3.1, STOP and reclassify to `HIGH` before implementation.

No medical-content Gate 1 or Gate 2 is expected.

A separate Anthony data-governance decision is mandatory before any historic row is changed.

# Stage 1A — Repository and authority preflight

Before kernel start or implementation, verify and record:

1. The exact current branch and `main == origin/main` state.
2. Working-tree and stash state.
3. The current status of `CF-ARCH-CONV-WAIST-1`.
4. The full 12-row affected set from:
   - `docs/audit-papers/WAIST_UNIT_LEGACY_IMPACT_AUDIT.md`
5. For each affected analysis ID:
   - current persisted value;
   - current unit or unit provenance;
   - current result-version metadata;
   - current stale state;
   - source record or lineage evidence;
   - audit classification;
   - repository-supported remediation options.
6. The locked LAUNCH-CORE-3 stale-detection policy and all existing stale-reason rules.
7. The implementation and callers of `detect_launch_core_stale_reasons()`.
8. Every reader, writer, replay path and report path that consumes the affected historic records.
9. Whether any of the 12 rows has already been remediated, deleted, superseded or regenerated.
10. Whether the current schema can preserve:
    - original value;
    - original unit;
    - remediation action;
    - reason;
    - timestamp;
    - actor/work ID;
    - reversibility or supersession linkage.
11. Whether the audit's recommended governed-remap/stale-mark treatment can be completed without:
    - the unbuilt regeneration job;
    - `CF-MEDREV2-002`;
    - a DB lineage-table change;
    - result-versioning redesign.
12. Current tests covering:
    - stale-reason detection;
    - launch-core versioning;
    - replay/regeneration;
    - data repair or migration;
    - historic-result rendering.

Use exact paths and line references in the hardening/evidence pack.

## Stage 1A classification check

Explicitly answer:

- Does `detect_launch_core_stale_reasons()` alter medical reasoning, ranking, interpretation or output construction?
- Is it an Intelligence Core component under Automation Bus SOP §3?
- Does this sprint remain `STANDARD`, or must it be `HIGH`?

Do not rely on the Stage 0 assumption. Record the repository-backed answer.

# Stage 1B — Reality check

Confirm that:

- all 12 audit-listed analysis IDs still exist or have an explicitly traceable successor state;
- each still has the waist-unit legacy defect described by the audit, unless already governed as remediated;
- the stale-detection framework still lacks a waist-unit rule;
- the existing framework can represent the required stale reason without redesign;
- the remediation does not require regeneration;
- no correct historic value needs to be guessed or reconstructed from insufficient evidence;
- this is not a no-op sprint.

If any core premise is false, STOP and re-scope.

# Stage 1C — Hardening deliverables

Harden `automation_bus/latest_cursor_prompt.md` and produce the standard evidence checklist.

The hardening pack must include:

- exact affected-code surface;
- exact affected-data surface;
- row-by-row evidence table;
- risk classification decision;
- proposed stale-reason identifier and semantics;
- proposed row disposition for all 12 IDs;
- rollback/reversal design;
- idempotency design;
- acceptance-test matrix;
- explicit exclusion proof for PKGC-2, compiled-WHY and full result versioning.

# Phase 0 — Mandatory data-governance STOP

After mapping and before any historic-row mutation, create and commit:

- `docs/architecture/ARCH-CONV-PKGC-1_hardening_pack.md`
- `docs/architecture/ARCH-CONV-PKGC-1_data_remediation_register.yaml`
- `docs/architecture/ARCH-CONV-PKGC-1_DATA_GOVERNANCE_decision.md`

The data-remediation register must contain one entry for each of the 12 analysis IDs with:

```yaml
analysis_id:
audit_classification:
current_value:
current_unit:
source_or_lineage_evidence:
proposed_disposition:
proposed_corrected_value:
proposed_corrected_unit:
stale_reason:
original_preserved:
reversible:
rationale:
confidence:
implementation_authorised: false
```

Permitted proposed dispositions are limited to repository-supported treatments, for example:

- `GOVERNED_REMAP`
- `MARK_STALE_NO_REWRITE`
- `ALREADY_REMEDIATED_NO_ACTION`
- `BLOCKED_AMBIGUOUS`

Do not invent a disposition merely to make all 12 rows actionable.

## Required Anthony decision

Anthony must approve the complete row-by-row remediation register, including:

- the treatment selected for every analysis ID;
- whether a persisted value may be rewritten;
- whether a row must instead be marked stale without rewriting;
- the audit-trail and reversibility mechanism;
- any blocked or ambiguous rows;
- confirmation that no inferred historic value is authorised.

## Mandatory STOP

After committing Phase 0:

- STOP.
- Keep the work package `IN_PROGRESS`.
- Do not add the stale-detection rule.
- Do not mutate any historic analysis row.
- Do not run a remediation script in write mode.
- Do not invoke or build regeneration.
- Do not touch provenance-identity code.
- Report the exact data-governance decision required.

# Phase 1 — Implementation after data-governance approval only

Proceed only after Anthony's decision is recorded on disk and `implementation_authorised: true`.

## A. Waist-unit stale-detection rule

Add one narrowly bounded rule to the existing `detect_launch_core_stale_reasons()` framework.

Requirements:

1. Use the existing stale-reason contract and return shape.
2. Detect only the proven waist-unit legacy defect.
3. Use canonical, deterministic evidence available in the persisted result and its version/lineage metadata.
4. Do not infer a defect solely from a surprising waist value.
5. Do not classify records stale where the unit and provenance are valid.
6. Produce a stable, named stale-reason identifier.
7. Preserve all six existing rules and their ordering/semantics unless the governing policy requires otherwise.
8. Do not create a parallel stale-detection engine.
9. Do not trigger regeneration.
10. Repeated evaluation must be deterministic.

The exact rule must be derived from the audit and repository evidence, not from assumptions in this prompt.

## B. Historic-row remediation

Implement the approved row-by-row dispositions for the 12 analysis IDs.

Requirements:

1. Apply exactly the approved action for each row.
2. Preserve original values and units through the repository's existing audit, supersession or lineage mechanism.
3. Never overwrite a row where the approved disposition is `MARK_STALE_NO_REWRITE`.
4. Never touch a row marked `BLOCKED_AMBIGUOUS`.
5. Do not infer missing conversion context.
6. Ensure remediation is idempotent.
7. Ensure a dry-run mode produces the exact intended change set before write mode.
8. Ensure write mode refuses to run if:
   - the target row no longer matches its approved precondition;
   - the affected-set count differs unexpectedly;
   - an unknown analysis ID appears;
   - the operation would affect rows outside the approved 12;
   - audit-trail persistence fails.
9. Produce a machine-readable remediation output showing:
   - analysis ID;
   - precondition result;
   - action;
   - before state;
   - after state;
   - stale reason;
   - audit reference;
   - success/failure.
10. Do not claim all 12 were remediated if any remain blocked or no-action.

Prefer the repository's established migration/remediation mechanism. Do not introduce ad hoc direct database mutation if a governed mechanism exists.

# Explicit exclusions

Do not:

- modify `output_authority_provenance_builder_v1.py`;
- modify `test_output_authority_provenance.py` for PKGC-2;
- implement provenance activation-key validation;
- advance `CF-ARCH-CONV-PROV-1`;
- advance `CF-ARCH-CONV-VERSION-1`;
- build or invoke the deferred regeneration job;
- implement `CF-MEDREV2-002`;
- redesign result versioning, replay or lineage;
- touch compiled-WHY authority, root-cause authority or medical content;
- touch signal activation, packages, PSI, SSOT or frontend medical logic;
- change waist thresholds or clinical interpretation;
- infer historic measurements from demographics, later results or current values;
- broaden remediation beyond the 12 governed analysis IDs;
- combine this work with `ARCH-CONV-PKGC-2`.

# Required tests

Add a focused regression suite for `ARCH-CONV-PKGC-1`.

At minimum prove:

## Stale-detection behaviour

1. Every governed affected record shape receives the new waist-unit stale reason.
2. Correct centimetre records are not marked stale.
3. Correct inch records with valid provenance are not marked stale.
4. Records without sufficient proof of the legacy defect are not automatically rewritten.
5. Existing stale-detection rules remain unchanged.
6. Multiple applicable stale reasons compose according to the locked policy.
7. Repeated detection is deterministic.

## Remediation behaviour

8. Dry-run identifies exactly the approved affected rows.
9. Each of the 12 analysis IDs receives exactly its approved disposition.
10. No unapproved row is mutated.
11. Governed remaps preserve original value/unit and audit lineage.
12. Stale-only rows are not rewritten.
13. Blocked rows remain untouched and are reported.
14. Re-running remediation creates no additional mutation.
15. Changed preconditions cause a fail-closed refusal.
16. Partial failure cannot be reported as complete success.
17. Rollback or supersession behaviour works as designed.

## Non-regression

18. Result-versioning rules 1–6 remain unchanged.
19. Replay behaviour remains unchanged except for the approved stale classification.
20. No regeneration job is called.
21. No provenance-identity behaviour changes.
22. No compiled-WHY, package, PSI, SSOT or frontend drift occurs.
23. Architecture and baseline gates remain green.

# Verification

Run at minimum:

- the new focused regression suite;
- all existing launch-core stale-detection tests;
- all relevant result-versioning and replay tests;
- relevant persistence/data-remediation tests;
- architecture validation gate;
- baseline test suite;
- three-layer pipeline verification;
- any database/migration validation required by the actual implementation;
- a dry-run against the governed 12-row set;
- a post-write verification proving exact approved outcomes, if the repository test environment supports governed write execution.

Do not use production data or an uncontrolled live database.

# STOP conditions during implementation

STOP if:

- repository evidence raises risk to `HIGH` and the work package has not been re-hardened;
- Anthony's data-governance approval is absent, incomplete or differs from the implementation;
- any row's correct disposition is ambiguous beyond the audit;
- any corrected value would need to be inferred;
- remediation requires the unbuilt regeneration job;
- the schema cannot preserve the required audit trail;
- the stale rule produces false positives on valid records;
- the affected set differs from the approved register;
- implementation touches PKGC-2, provenance, compiled-WHY or medical content;
- result-versioning redesign is required;
- a write cannot be made idempotent and fail-closed;
- unrelated regressions cannot be bounded and attributed.

# Evidence and closure

Produce:

- `docs/audit-papers/ARCH-CONV-PKGC-1_implementation_and_verification_report.md`
- final `docs/architecture/ARCH-CONV-PKGC-1_data_remediation_register.yaml`
- final `docs/architecture/ARCH-CONV-PKGC-1_DATA_GOVERNANCE_decision.md`
- updated `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`
- updated `docs/sprints/launch_core_carry_forward_register.md`

Close only the carry-forward obligation actually resolved.

If any of the 12 rows remains blocked, record that explicitly and do not mark the carry-forward item fully resolved unless its governing definition permits partial closure.

Complete the mandatory Post-Implementation Closure Protocol before kernel finish.

Run `python backend/scripts/run_work_package.py finish` only when:

- implementation is complete;
- approved data actions are verified;
- all required tests and gates pass;
- the branch is clean except for permitted kernel-owned status handling;
- no out-of-scope or tooling files are present;
- stash state is governed and empty unless explicitly authorised.

Do not merge.

After kernel `COMPLETE`, stop for independent Claude Code audit, GPT architectural review and Anthony merge authority.
