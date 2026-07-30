---
work_id: ARCH-CONV-B
branch: feature/arch-conv-b-renal-why-authority
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# ARCH-CONV-B — Renal WHY-Authority Migration

## Objective

Deliver one bounded renal WHY-authority migration covering:

- `signal_creatinine_high::inv_creatinine_high_renal`
- `signal_urea_high::inv_urea_high_renal`

The package must also resolve and protect the medical-authority boundary between `signal_creatinine_high` and `signal_egfr_low`.

`signal_urate_high::inv_uric_acid_high_metabolic` is explicitly excluded from implementation and remains deferred to the metabolic/systemic residual programme unless separately re-authorised.

Do not infer any `source_spec_id` from filenames or package names. Confirm identity only from embedded canonical fields.

## Governing rules

Apply the repository-governed versions of:

- `AUTOMATION_BUS_SOP_v1.3.1.md`
- `KNOWLEDGE_BUS_SOP_v1.3.1.md`
- `KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md`

Treat the work as HIGH-risk MIXED Intelligence Core work.

Preserve:

- canonical research as upstream medical authority;
- deterministic compilation into governed runtime artefacts;
- thin, non-inferential runtime loaders;
- signal presence separately from causal-WHY eligibility;
- context-only separately from causal frames;
- `activation_key = signal_id::source_spec_id`;
- fail-closed authority selection;
- explicit named duplicate-authority resolution;
- no lexicographic, package-name, filesystem-order or load-order selection;
- no raw investigation-spec reads at runtime;
- no frontend medical inference.

## Authoritative programme baseline

Use current `main` at or after:

```text
290ac180a62681da22d3132653c5cbe25d1dbb80
```

This includes the merged and published ARCH-CONV-A revised scope covering Waves 0–2.

The preserved renal preparation is:

```text
commit: 31c37a2f8b4dbf06a46a4ecbc474efd2e5c9818a
source branch: feature/arch-conv-a-renal-migration
```

That commit contains preparation only. It does not contain medical decisions, human ratification, compiled frames, runtime activation, authority-register changes or legacy disconnection.

## Branch preparation

Before Automation Bus start:

1. Confirm local `main == origin/main`.
2. Create:

```text
feature/arch-conv-b-renal-why-authority
```

from current `main`.

3. Cherry-pick `31c37a2f8b4dbf06a46a4ecbc474efd2e5c9818a`.
4. Resolve only stale work-package framing introduced by the preserved documentation.
5. Do not carry forward `ARCH-CONV-A` / `Wave 3` as the active work identity.
6. Confirm the working tree is clean before hardening and kernel start.

STOP if the cherry-pick introduces non-document renal implementation, compiled artefacts, authority-register changes or legacy disconnection.

## Required source records

Read the current repository versions of the established ARCH-CONV-A pattern, including:

```text
docs/architecture/ARCH-CONV-A_revised_scope_and_split_decision.md
docs/architecture/ARCH-CONV-A_revised_scope_completion_report.md
docs/architecture/ARCH-CONV-A_STOP_A_identity_and_source_closure.md
docs/architecture/ARCH-CONV-A_phase1_target_to_frame_map.md
docs/architecture/ARCH-CONV-A_STOP_A_ratification_record.md
docs/architecture/ARCH-CONV-A_STOP_C_wave1_runtime_proof.md
docs/architecture/ARCH-CONV-A_wave1_thyroid_gate1_gate2_decision.md
docs/architecture/ARCH-CONV-A_STOP_C_wave2_runtime_proof.md
docs/architecture/ARCH-CONV-A_wave2_lipid_gate1_gate2_decision.md
docs/architecture/ARCH-CONV-A_wave2_medical_decision_register.yaml
```

Read the preserved renal preparation after cherry-pick:

```text
docs/architecture/ARCH-CONV-A_wave3_renal_medical_review_pack.md
docs/architecture/ARCH-CONV-A_wave3_medical_decision_register.yaml
docs/architecture/ARCH-CONV-A_phase2_spec_ready_frame_index.md
```

Read all canonical investigation specs, legacy WHY assets, package records, loaders, authority registers and tests relevant to:

```text
signal_creatinine_high
signal_egfr_low
signal_urea_high
```

Inspect urate only sufficiently to prove and document its exclusion boundary.

## Stage 1A — Authority preflight

Before modifying runtime or governed content, identify and record:

1. Canonical investigation-spec path and embedded `spec_id` for every candidate frame.
2. Current legacy WHY file and loader/registry path for each target.
3. Current compiled WHY artefact paths and authority-register state.
4. Runtime loader and selector paths.
5. Existing duplicate-authority resolution mechanism.
6. Canonical tests covering loader, authority selection, context-only behaviour and legacy fallback/disconnection.
7. Any parallel or duplicate authority source.

STOP if any authoritative path, loader relationship or current authority state is ambiguous.

## Stage 1B — Reality check

Confirm that the current baseline still exhibits all of the following:

- creatinine and urea remain on active legacy WHY authority;
- no compiled renal frames are active;
- `signal_egfr_low` has no active WHY authority;
- the creatinine/eGFR causal-authority boundary remains unresolved;
- urate remains medically and architecturally mixed between renal handling and metabolic/gout framing.

Cancel or rescope any no-op element.

## Stage 1C — Intelligence preflight

Before implementation, list all affected:

- canonical research assets;
- compiled hypothesis artefacts;
- compile or promotion tooling;
- WHY authority registers;
- legacy root-cause registry entries;
- duplicate-authority resolution paths;
- runtime WHY loaders/selectors;
- DTO/report consumers;
- regression and architecture tests.

State the expected output changes and the exact outputs that must remain unchanged.

# Phase 0 — Preserved preparation reconciliation

Refresh the three preserved renal documents into ARCH-CONV-B authority.

Required outputs:

```text
docs/architecture/ARCH-CONV-B_STOP_A_identity_and_source_closure.md
docs/architecture/ARCH-CONV-B_target_to_frame_map.md
docs/architecture/ARCH-CONV-B_medical_review_pack.md
docs/architecture/ARCH-CONV-B_medical_decision_register.yaml
```

The refreshed records must:

- replace obsolete ARCH-CONV-A / Wave 3 framing;
- retain verified identities and evidence findings;
- reconcile all paths and authority states against current `main`;
- identify every candidate legacy and canonical frame;
- distinguish existing canonical investigation specs from package-only Pass 3 material;
- classify evidence gaps explicitly;
- document urate as out of implementation scope;
- contain no medical approval or ratification at this stage.

Do not compile, activate, register or disconnect any authority during Phase 0.

# STOP A — Identity, source and package-boundary closure

Produce auditable evidence confirming:

## Creatinine

Confirmed target:

```text
signal_creatinine_high::inv_creatinine_high_renal
```

Record:

- embedded identity;
- canonical source path;
- active legacy WHY authority;
- all Pass 3/package-only parallel framings;
- current compiled authority state;
- supporting/context relationship to eGFR.

## eGFR boundary

Record both known canonical frames:

```text
signal_egfr_low::inv_egfr_low_chronic_kidney_function_reduction
signal_egfr_low::inv_egfr_low_hemodynamic_filtration_drop
```

The STOP A record must explicitly prevent creatinine from silently becoming surrogate authority for the distinct eGFR signal family.

Classify this as a cross-signal medical-authority boundary, not a same-activation-key duplicate.

## Urea

Confirmed target:

```text
signal_urea_high::inv_urea_high_renal
```

Record:

- embedded identity;
- canonical source path;
- active legacy WHY authority;
- the package-only prerenal volume-depletion/catabolic-load framing;
- all evidence and structured-field gaps;
- whether candidate content may represent separate causal, contextual or deferred frames.

## Urate exclusion

Confirmed identity:

```text
signal_urate_high::inv_uric_acid_high_metabolic
```

Document why urate is excluded from this package:

- canonical research domain is metabolic;
- renal handling is only one component;
- competing gout/crystal and metabolic framing exists;
- inclusion would widen the medical and rollback boundary.

No urate medical decision, compilation, runtime integration or legacy change is permitted.

## STOP A verdict

STOP and return the completed STOP A evidence for independent architectural review.

Do not proceed to Gate 1 or any implementation until the Head of Architecture explicitly approves STOP A.

# Phase 1 — Gate 1 medical review preparation

After explicit STOP A approval, finalise the medical review pack for Head of Medical Research review.

The pack must request decisions only on:

## Creatinine/eGFR

- whether the creatinine frame is medically acceptable;
- how eGFR may act as supporting, severity or contradiction evidence;
- which causal claims belong exclusively to future `signal_egfr_low` WHY authority;
- safeguards preventing creatinine from displacing eGFR;
- legacy-versus-canonical disposition.

## Urea

- whether renal/excretory and prerenal volume-depletion/catabolic framings form:
  - one frame;
  - multiple frames;
  - context-only material;
  - or deferred content;
- whether evidence is sufficient;
- treatment of dehydration, catabolic load, corticosteroid and gastrointestinal-bleed contexts;
- legacy-versus-canonical disposition.

Do not make the medical decisions.

# STOP B — Dual medical gate

No compile or runtime work may begin until both are recorded:

1. Head of Medical Research structured Gate 1 decisions.
2. Anthony’s explicit Gate 2 production ratification.

Update:

```text
docs/architecture/ARCH-CONV-B_medical_decision_register.yaml
```

Every candidate frame must have:

- explicit decision;
- causal/context-only/rejected/deferred role;
- evidence rationale;
- legacy authority disposition;
- Head of Medical Research reference;
- Anthony ratification reference.

STOP if any implementation-relevant decision is missing, ambiguous or unratified.

# Phase 2 — Deterministic compile and authority integration

Implement only ratified decisions.

## Required implementation rules

- Compile from canonical research or an explicitly governed accepted source.
- Emit deterministic compiled WHY artefacts.
- Preserve source lineage, source hash, output hash and compiler/promoter version.
- Use `activation_key = signal_id::source_spec_id`.
- Register only approved causal frames as causal authority.
- Preserve context-only frames as non-causal.
- Fail closed on duplicate `activation_key`.
- Use explicit named resolution for any overlapping current authority.
- Never select by filename, package name, lexical order, directory order or load order.
- Do not read raw investigation specs at runtime.
- Do not use `physiological_claim` as fallback presentation text.
- Do not disconnect legacy authority before replacement equivalence and reachability are proven.

## Creatinine/eGFR protection

Implementation must prove:

- creatinine WHY may consume approved eGFR context only as ratified;
- creatinine does not emit or claim standalone `signal_egfr_low` WHY authority;
- future eGFR WHY migration remains possible without duplicate or displaced authority.

## Urea

Implement only the ratified frame structure.

Do not silently merge prerenal, renal, catabolic or bleeding-related concepts unless the ratified decision explicitly requires it.

## Legacy handling

Legacy creatinine and urea authority may be disconnected only where:

- replacement authority is compiled;
- authority registration is explicit;
- runtime reachability is proven;
- output comparison is accepted;
- fallback behaviour remains fail-closed;
- the ratified decision authorises disconnection.

No physical deletion of legacy assets is permitted.

# STOP C — Independent runtime proof

An independent auditor must verify and document:

1. Every approved frame is compiled and reachable.
2. Every rejected or deferred frame is unreachable.
3. Context-only content cannot emit causal WHY.
4. Duplicate activation keys fail closed.
5. Authority selection is deterministic and independent of ordering.
6. Creatinine does not absorb eGFR WHY authority.
7. Urea emits only the ratified causal structure.
8. Legacy authority is disconnected only where explicitly authorised.
9. Legacy fallback remains safe where replacement is incomplete.
10. Urate remains unchanged.
11. Thyroid, lipid/cardiometabolic and unrelated domains show no behavioural regression.
12. Identical inputs produce identical outputs.
13. Source-to-compiled-to-runtime lineage is complete.

Required evidence:

```text
docs/architecture/ARCH-CONV-B_STOP_C_runtime_proof.md
```

STOP C must be performed independently from implementation.

# Testing requirements

At minimum, add or update tests proving:

- embedded identity and activation-key correctness;
- deterministic compile output;
- compiled artefact schema validation;
- causal versus context-only enforcement;
- duplicate activation-key refusal;
- explicit authority selection;
- no lexicographic or load-order dependency;
- creatinine/eGFR boundary protection;
- urea ratified-frame behaviour;
- legacy fallback/disconnection behaviour;
- urate unchanged;
- unrelated domain regression stability;
- repeat-run determinism.

Use the canonical existing test modules where possible. Do not create parallel test authorities.

# Completion criteria

The package is complete only when:

- STOP A is independently approved;
- all implementation-relevant medical decisions are completed and ratified;
- compiled artefacts are deterministic and source-traceable;
- creatinine/eGFR authority boundaries are explicit and enforced;
- urea authority matches the ratified decision;
- no duplicate active WHY authority remains for migrated frames;
- no rejected/context-only frame can emit causal WHY;
- urate remains untouched;
- STOP C passes independently;
- the full canonical regression suite passes with no new failures;
- Automation Bus finish passes;
- the Post-Implementation Closure Protocol is completed;
- the branch is clean and ready for merge review.

Finish readiness is not merge authority.

# Rollback boundary

This branch must remain one coherent rollback unit containing only:

- creatinine/eGFR authority-boundary handling;
- creatinine WHY-authority migration;
- urea WHY-authority migration;
- directly required compiled artefacts;
- directly required authority-register, loader and selector changes;
- directly required tests and audit documents.

Rollback must restore the complete pre-ARCH-CONV-B renal state without affecting thyroid, lipid/cardiometabolic, urate, hepatic/biliary, iron/haematology or metabolic/systemic authority.

# Explicit non-goals

- Urate WHY migration.
- Standalone eGFR WHY migration.
- Hepatic/biliary migration.
- Iron/haematology migration.
- Metabolic/systemic residual migration.
- New medical research or threshold invention.
- PSI runtime wiring.
- Frontend or presentation redesign.
- General compiler, registry or loader redesign unrelated to this package.
- Estate-wide provenance backfill.
- Package B dual-authority retirement.
- Package C replay/versioning work.
- Physical deletion of legacy WHY assets.
- Any implementation before STOP A approval and dual Gate 1/Gate 2 completion.

# Required final report

Return:

1. Branch and commit summary.
2. Files changed.
3. STOP A approval evidence.
4. Gate 1 and Gate 2 decision references.
5. Compiled artefact and lineage summary.
6. Authority-register changes.
7. Legacy authority disposition.
8. Test results.
9. STOP C verdict.
10. Post-Implementation Closure Protocol evidence.
11. Remaining risks and successor-package boundaries.
12. Merge recommendation.

Do not merge without explicit human authority.
