---
work_id: ARCH-CONV-C
branch: feature/arch-conv-c-alp-ggt-why-authority
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# ARCH-CONV-C — ALP/GGT Hepatobiliary WHY-Authority Migration

## Objective

Deliver one bounded hepatic/biliary WHY-authority migration covering:

- `signal_alp_high::inv_alp_high_bone_biliary`
- `signal_ggt_high::inv_ggt_high_hepatic`

The package must also establish the first governed medical-authority decision for:

```text
liver_injury_axis
```

Explicitly exclude:

- `signal_alt_high`
- `signal_hepatic_alt_context`
- `signal_ast_high`
- `signal_hyperbilirubinemia`
- `signal_bilirubin_high`
- `signal_alp_low`

Do not infer any `source_spec_id` from filenames or package names. Confirm identity only from embedded canonical fields.

## Governing rules

Apply the repository-governed versions of:

- `AUTOMATION_BUS_SOP_v1.3.1.md`
- `KNOWLEDGE_BUS_SOP_v1.3.1.md`
- `KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md`

Treat this as HIGH-risk MIXED Intelligence Core work.

Preserve:

- canonical research as upstream medical authority;
- deterministic compilation into governed runtime artefacts;
- thin, non-inferential runtime loaders;
- signal presence separately from causal-WHY eligibility;
- causal separately from context-only or morphology-context roles;
- `activation_key = signal_id::source_spec_id`;
- fail-closed authority selection;
- explicit named collision and duplicate-authority resolution;
- no lexicographic, package-name, filesystem-order or load-order selection;
- no raw investigation-spec reads at runtime;
- no frontend medical inference.

## Authoritative programme baseline

Use current `main` after completed and merged ARCH-CONV-B.

ARCH-CONV-B is the implementation precedent for:

- STOP A identity/source closure;
- Gate 1 Head of Medical Research decisions;
- Gate 2 Anthony ratification;
- compiled WHY artefacts and manifests;
- explicit `why_role` propagation;
- fail-closed clinician/report handling;
- conditional legacy retirement;
- independent STOP C;
- Automation Bus closure.

No preserved hepatic-specific preparation branch or commit is authoritative for this package. Start from current `main`.

## Branch preparation

Before Automation Bus start:

1. Confirm local `main == origin/main`.
2. Create:

```text
feature/arch-conv-c-alp-ggt-why-authority
```

from current `main`.

3. Confirm the working tree is clean and stash is empty.
4. Do not cherry-pick or rebase any old hepatic/liver branch.
5. Confirm no ARCH-CONV-C product changes already exist.

STOP if current `main` does not contain the completed ARCH-CONV-B authority pattern or if the branch baseline is ambiguous.

## Required source records

Read the current repository versions of:

```text
docs/architecture/ARCH-CONV-B_STOP_A_identity_and_source_closure.md
docs/architecture/ARCH-CONV-B_target_to_frame_map.md
docs/architecture/ARCH-CONV-B_medical_review_pack.md
docs/architecture/ARCH-CONV-B_medical_decision_register.yaml
docs/architecture/ARCH-CONV-B_GATE_1_head_of_medical_research_decision.md
docs/architecture/ARCH-CONV-B_GATE_2_Anthony_ratification.md
docs/architecture/ARCH-CONV-B_STOP_C_runtime_proof.md
```

Read all canonical investigation specs, Pass 3/package-only sources, legacy WHY assets, loaders, authority registers, collision registers and tests relevant to:

```text
signal_alp_high
signal_ggt_high
liver_injury_axis
```

Inspect excluded targets only sufficiently to prove and preserve their exclusion boundaries.

## Stage 1A — Authority preflight

Before modifying runtime or governed content, identify and record:

1. Embedded canonical `spec_id` and source path for every ALP-high and GGT-high candidate.
2. Current legacy WHY file and loader/registry path for each target.
3. All Pass 3/package-only candidate frames and their governance state.
4. Current compiled WHY artefact and authority-register state.
5. Runtime loader, compiler, report and DTO paths.
6. Current `liver_injury_axis` placeholder state and every field requiring adjudication.
7. Existing tests covering compiled authority, collision selection, role propagation, fail-closed behaviour, legacy fallback/retirement and liver-domain regression.
8. Any parallel or duplicate authority source.

STOP if any authoritative path, loader relationship, identity or current authority state is ambiguous.

## Stage 1B — Reality check

Confirm that:

- ALP-high remains on active legacy WHY authority;
- GGT-high remains on active legacy WHY authority;
- no ALP-high or GGT-high compiled WHY frame is active;
- `liver_injury_axis` remains a placeholder without medical policy;
- ALP retains unresolved biliary-versus-bone interpretation;
- GGT retains unresolved hepatobiliary-versus-alcohol/enzyme-induction interpretation;
- ALT, AST, bilirubin/hyperbilirubinemia and ALP-low remain outside this package.

Cancel or rescope any no-op element.

## Stage 1C — Intelligence preflight

Before implementation, list all affected:

- canonical research assets;
- Pass 3/package-only parallel candidates;
- compiled hypothesis artefacts;
- compile manifests;
- WHY authority registers;
- legacy root-cause registry entries;
- `liver_injury_axis` collision policy;
- runtime WHY loaders/selectors;
- clinician-report and DTO role propagation;
- liver-domain scoring/card dependencies;
- regression and architecture tests.

State expected output changes and exact outputs that must remain unchanged.

# Phase 0 — Identity, source and collision-boundary reconstruction

Create:

```text
docs/architecture/ARCH-CONV-C_STOP_A_identity_and_source_closure.md
docs/architecture/ARCH-CONV-C_target_to_frame_map.md
docs/architecture/ARCH-CONV-C_medical_review_pack.md
docs/architecture/ARCH-CONV-C_medical_decision_register.yaml
```

The records must:

- verify identities from embedded canonical fields;
- map every ALP-high and GGT-high candidate frame;
- identify active legacy WHY authority;
- distinguish canonical investigation specs from package-only Pass 3 material;
- classify evidence gaps explicitly;
- reconstruct the current `liver_injury_axis` placeholder;
- define the medical-policy questions required to populate it;
- document all exclusions;
- contain no medical approval, runtime authorisation or legacy-disconnection decision.

Do not compile, activate, register or disconnect any authority during Phase 0.

# STOP A — Identity, source and package-boundary closure

## ALP-high

Confirmed provisional target:

```text
signal_alp_high::inv_alp_high_bone_biliary
```

Verify from embedded source fields.

Record:

- canonical source path;
- active legacy WHY authority;
- every biliary/cholestatic and bone-turnover candidate;
- current compiled authority state;
- relationship to GGT concordance;
- whether any candidate is package-only or lacks canonical investigation-spec authority;
- the risk of ALP being misrepresented as hepatic when bone origin remains plausible.

## GGT-high

Confirmed provisional target:

```text
signal_ggt_high::inv_ggt_high_hepatic
```

Verify from embedded source fields.

Record:

- canonical source path;
- active legacy WHY authority;
- every hepatobiliary, alcohol and enzyme-induction candidate;
- current compiled authority state;
- relationship to ALP concordance;
- whether any candidate is package-only or lacks canonical investigation-spec authority;
- the risk of context-only alcohol/enzyme-induction material surfacing as causal.

## liver_injury_axis

Document the existing placeholder policy.

Define the questions needed to decide:

- whether ALP or GGT can ever be primary authority;
- whether one must remain supporting/context-only;
- whether ALP+GGT concordance is required before biliary/cholestatic causality;
- whether discordant ALP and GGT patterns must suppress or redirect causal output;
- how bone-turnover, alcohol and enzyme-induction contexts are represented;
- how future ALT and bilirubin packages may join the same axis without being pre-empted.

Do not populate final medical policy during STOP A.

## Explicit exclusions

### ALT

`signal_alt_high` and `signal_hepatic_alt_context` remain excluded because their identity and authority relationship is unresolved.

No ALT medical decision, compile, authority registration, collision-policy decision or legacy change is permitted.

### AST

`signal_ast_high` remains excluded because no canonical WHY target currently exists.

No AST WHY target may be invented.

### Bilirubin

`signal_bilirubin_high` remains retired as a WHY identity.

`signal_hyperbilirubinemia` remains the surviving family but has no canonical investigation spec.

No bilirubin compile, identity reopening, legacy change or authority registration is permitted.

### ALP-low

`signal_alp_low` is a separate direction with no canonical investigation spec.

No ALP-low action is permitted.

## STOP A verdict

STOP and return the completed STOP A evidence for independent Head of Architecture approval.

Do not proceed to Gate 1 or implementation until STOP A is explicitly approved.

# Phase 1 — Gate 1 medical review preparation

After STOP A approval, finalise the medical review pack.

The pack must request decisions only on:

## ALP

- whether the canonical ALP frame is medically acceptable;
- whether it requires narrowing;
- whether ALP alone may support a causal candidate;
- whether GGT concordance is required before hepatobiliary or cholestatic interpretation;
- whether bone-turnover content is causal, context-only, rejected or deferred;
- fail-closed behaviour where GGT, bilirubin, calcium, phosphate, vitamin D, bone history or imaging are absent;
- legacy disposition.

## GGT

- whether the canonical GGT frame is medically acceptable;
- whether GGT alone may support hepatobiliary causality;
- whether alcohol and enzyme-induction content is causal, context-only, rejected or deferred;
- how ALP concordance changes role, confidence or eligibility;
- fail-closed behaviour where alcohol, medication, ALP, bilirubin or imaging context is absent;
- legacy disposition.

## liver_injury_axis

- primary/supporting/context roles for ALP and GGT;
- concordant versus discordant behaviour;
- suppression or refusal rules;
- future-safe boundary for ALT and bilirubin;
- deterministic selection rules.

Do not make medical decisions.

# STOP B — Dual medical gate

No compile or runtime work may begin until both are recorded:

1. Head of Medical Research structured Gate 1 decisions.
2. Anthony’s explicit Gate 2 ratification.

Update:

```text
docs/architecture/ARCH-CONV-C_medical_decision_register.yaml
```

Every candidate frame and every implementation-relevant `liver_injury_axis` policy element must have:

- explicit decision;
- causal/context-only/rejected/deferred role;
- evidence rationale;
- collision-axis role;
- legacy authority disposition;
- Head of Medical Research reference;
- Anthony ratification reference.

STOP if any implementation-relevant decision is missing, ambiguous or unratified.

# Phase 2 — Deterministic compile and authority integration

Implement only ratified decisions.

## Required implementation rules

- Compile only from canonical research or an explicitly governed accepted source.
- Emit deterministic compiled WHY artefacts and manifests.
- Preserve source lineage, source hash, output hash and compiler/promoter version.
- Use `activation_key = signal_id::source_spec_id`.
- Register only approved causal frames as causal authority.
- Preserve context-only or morphology-context frames as non-causal.
- Fail closed on missing, blank or unsupported role metadata.
- Fail closed on duplicate `activation_key`.
- Use explicit named `liver_injury_axis` policy.
- Never select by filename, package name, lexical order, directory order or load order.
- Do not read raw investigation specs at runtime.
- Do not use `physiological_claim` as fallback presentation text.
- Do not disconnect legacy authority before replacement equivalence and reachability are proven.

## ALP safeguards

Implementation must prove:

- ALP cannot silently imply hepatic or biliary causality where bone origin remains plausible;
- GGT concordance is applied exactly as ratified;
- bone-turnover content cannot surface as hepatobiliary causal WHY unless ratified;
- missing supporting data fails closed.

## GGT safeguards

Implementation must prove:

- alcohol and enzyme-induction context cannot surface as causal unless ratified;
- GGT cannot silently diagnose cholestasis or hepatobiliary disease;
- ALP concordance is applied exactly as ratified;
- missing supporting data fails closed.

## liver_injury_axis safeguards

Implementation must prove:

- the axis policy is explicit and named;
- primary/supporting/context roles are deterministic;
- discordant patterns follow ratified suppression or refusal rules;
- future ALT and bilirubin authority is not displaced or pre-decided;
- no order-dependent fallback remains.

## Legacy handling

Legacy ALP-high and GGT-high authority may be disconnected only where:

- replacement authority is compiled;
- authority registration is explicit;
- runtime reachability is proven;
- output comparison is accepted;
- Gate 1 and Gate 2 authorise disconnection;
- independent STOP C confirms safe replacement.

No physical deletion of legacy assets is permitted.

# STOP C — Independent runtime proof

An independent auditor must verify:

1. Every approved ALP and GGT frame is compiled and reachable.
2. Every rejected or deferred frame is unreachable.
3. Context-only content cannot emit causal WHY.
4. Missing or unsupported role metadata fails closed.
5. Duplicate activation keys fail closed.
6. `liver_injury_axis` selection is explicit, named and deterministic.
7. ALP cannot misrepresent bone-origin patterns as hepatobiliary causality.
8. GGT alcohol/enzyme-induction context cannot emerge as causal unless ratified.
9. Concordant and discordant ALP/GGT patterns behave exactly as ratified.
10. Legacy authority is disconnected only where authorised.
11. Legacy fallback remains safe where replacement is incomplete.
12. ALT, AST, bilirubin/hyperbilirubinemia and ALP-low remain unchanged.
13. Liver scoring/card behaviour remains unchanged unless explicitly required and ratified.
14. Thyroid, lipid, renal and unrelated domains show no behavioural regression.
15. Identical inputs produce identical outputs.
16. Source-to-compiled-to-runtime lineage is complete.

Required evidence:

```text
docs/architecture/ARCH-CONV-C_STOP_C_runtime_proof.md
```

STOP C must be independent from implementation.

# Testing requirements

At minimum, add or update tests proving:

- embedded identity and activation-key correctness;
- deterministic compile output;
- compiled artefact schema validation;
- causal versus context-only enforcement;
- missing/unsupported role refusal;
- duplicate activation-key refusal;
- explicit `liver_injury_axis` selection;
- no lexicographic or load-order dependency;
- ALP bone-versus-biliary safeguards;
- GGT hepatobiliary-versus-context safeguards;
- concordant and discordant ALP/GGT behaviour;
- legacy fallback/disconnection behaviour;
- ALT unchanged;
- AST unchanged;
- bilirubin/hyperbilirubinemia unchanged;
- ALP-low unchanged;
- liver scoring/card regression stability;
- thyroid, lipid and renal regression stability;
- repeat-run determinism.

Use canonical existing test modules where possible. Do not create parallel test authorities.

# Completion criteria

The package is complete only when:

- STOP A is independently approved;
- all implementation-relevant medical and collision-policy decisions are completed and ratified;
- compiled artefacts are deterministic and source-traceable;
- ALP and GGT roles are explicit and enforced;
- `liver_injury_axis` is explicit, named and deterministic;
- no ungoverned duplicate active WHY authority remains for migrated frames;
- no rejected/context-only frame can emit causal WHY;
- excluded signals remain untouched;
- STOP C passes independently;
- the canonical regression suite passes with no new failures;
- Automation Bus finish passes;
- the Post-Implementation Closure Protocol is completed;
- the branch is clean and ready for merge review.

Finish readiness is not merge authority.

# Rollback boundary

This branch must remain one coherent rollback unit containing only:

- ALP-high WHY-authority migration;
- GGT-high WHY-authority migration;
- `liver_injury_axis` policy required for those targets;
- directly required compiled artefacts;
- directly required authority-register, loader, compiler, contract and DTO changes;
- directly required tests and audit documents.

Rollback must restore the pre-ARCH-CONV-C hepatic/biliary authority state without affecting ALT, AST, bilirubin/hyperbilirubinemia, ALP-low, thyroid, lipid, renal, iron/haematology or metabolic/systemic authority.

# Explicit non-goals

- ALT identity resolution or migration.
- AST WHY creation.
- Bilirubin/hyperbilirubinemia canonical-spec authoring or migration.
- ALP-low migration.
- Liver-card scoring redesign.
- Frontend medical logic or presentation redesign.
- Hepatic estate-wide migration.
- New medical research or threshold invention.
- PSI runtime wiring.
- Estate-wide provenance backfill.
- Physical deletion of legacy WHY assets.
- Any implementation before STOP A approval and dual Gate 1/Gate 2 completion.

# Required final report

Return:

1. Branch and commit summary.
2. Files changed.
3. STOP A approval evidence.
4. Gate 1 and Gate 2 decision references.
5. Compiled artefact and lineage summary.
6. `liver_injury_axis` policy changes.
7. Authority-register changes.
8. Legacy authority disposition.
9. Test results.
10. STOP C verdict.
11. Post-Implementation Closure Protocol evidence.
12. Remaining risks and successor-package boundaries.
13. Merge recommendation.

Do not merge without explicit human authority.
