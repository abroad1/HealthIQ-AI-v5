---
work_id: ARCH-CONV-A-THYROID-RESIDUAL-DISPOSITION-1
branch: governance/arch-conv-a-thyroid-residual-disposition-1
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: CONTENT
---

# ARCH-CONV-A — Thyroid Residual Authority & Disposition

## Objective

Re-open the residual ARCH-CONV-A programme from current repository reality, not the obsolete 2026-07-27 Wave 1 assumptions.

This package is a bounded **authority/disposition sprint only**. It must determine the exact remaining thyroid clinical-intelligence work after the already-completed TSH / FT3 / FT4 / TPOAb hypothyroid-path compilation and activation work.

It must not implement runtime behaviour, activate packages, compile new WHY artefacts, or author fresh medical research.

The required output is a ratifiable thyroid residual authority pack that leaves each remaining item in exactly one governed state:

- `PROMOTE_COMPILE`
- `REMAIN_DEFERRED`
- `RESEARCH_REQUIRED`
- `SEPARATE_PRESENTATION_OR_INTERVENTION_WORK`
- `RETIRE_OR_SUBSUME`
- `NO_FURTHER_WORK`

## Governing Context

Treat the repository-reality reconciliation as the current starting evidence, but independently verify all material facts from current `main`.

The known provisional residuals to verify are:

1. `signal_tgab_high` — existing package / Pass 3 research, not compiled; likely review/promotion/compilation rather than new research.
2. `signal_tpo_ab_high` euthyroid-autoimmune-risk variant — research exists but activation was deliberately deferred; requires explicit disposition.
3. `signal_tpo_ab_high` hypothyroid variant — already compiled/active; confirmatory-test content exists upstream but is not wired into downstream intervention/next-step output.
4. TRAb / TSI — suspected genuine Graves-specific research gap; verify absence before classifying as `RESEARCH_REQUIRED`.
5. `signal_thyroid_tsh_context` — previously deliberately excluded; verify no later authority reopened it.
6. THY-U5 / consumer naming of Hashimoto's / Graves' — unresolved communication/product authority; determine exactly what existing ratified authority permits and what requires Anthony decision.

## Stage 1A — Authority Preflight

Before doing any disposition work, verify from current `main`:

1. canonical research authority for thyroid residuals;
2. current compiled-WHY authority register;
3. current activation authority;
4. current thyroid medical decision / ADR authority;
5. current consumer-communication authority relevant to disease naming;
6. current intervention / confirmatory-test authority;
7. no later superseding thyroid decision exists.

At minimum inspect the current authoritative versions of:

- `docs/architecture/ARCH-CONV-A_RESIDUAL_PROGRAMME_REPOSITORY_REALITY_RECONCILIATION.md`
- `docs/architecture/ARCH-CONV-A_wave1_thyroid_gate1_gate2_decision.md`
- `docs/architecture/ADR-THYROID-MR-V2-ACTIVATION-1.md`
- thyroid entries in `knowledge_bus/governance/compiled_why_authority_register_v1.yaml`
- thyroid entries in `knowledge_bus/governance/package_runtime_activation_register_v1.yaml`
- relevant thyroid investigation specs / Pass 3 source artefacts
- relevant thyroid package manifests / signal libraries
- the current intervention library / next-step authority
- the document containing THY-U5

If any listed path is stale, renamed, superseded, or non-authoritative, use the current authoritative replacement and record the substitution.

## Stage 1B — Reality / No-Op Check

Independently verify each provisional residual.

If current `main` shows all residuals already dispositioned and no unresolved thyroid clinical-intelligence authority remains, STOP with:

`NO_OP_OR_REBASE_REQUIRED`

Do not create a decision package merely to restate already-closed authority.

## Stage 1C — Intelligence Preflight

This sprint must not change emitted runtime behaviour.

Affected intelligence surfaces are **authority documents only**, but because the decisions govern future clinical-intelligence promotion, treat the package as HIGH risk.

No changes are authorised to:

- signal firing;
- thresholds/comparators;
- activation register;
- compiled WHY artefacts;
- package content;
- prioritisation;
- clinical concern construction;
- frontend;
- consumer narrative;
- intervention runtime.

## Required Analysis

### 1. Build the exact residual identity/source map

For each remaining thyroid item, record:

- signal / frame identity;
- source research authority;
- package identity;
- compiled-WHY state;
- runtime activation state;
- prior medical decision;
- current residual;
- proposed disposition;
- exact evidence citations.

Do not assume one signal ID equals one medical frame.

### 2. TgAb disposition

For every currently represented `signal_tgab_high` variant:

- identify the source medical framing;
- verify whether existing Pass 3 / investigation-spec evidence is sufficient for governed medical review;
- determine whether the variant should:
  - proceed to compiled-WHY promotion;
  - remain deferred;
  - be consolidated with another thyroid antibody frame;
  - or require fresh research.

Do not author the compiled artefact in this sprint.

### 3. TPOAb euthyroid variant disposition

Re-evaluate the previously deferred euthyroid-autoimmune-risk TPOAb variant against current product scope and existing research.

The decision must explicitly be one of:

- `PROMOTE_COMPILE`
- `REMAIN_DEFERRED`
- `RETIRE_OR_SUBSUME`

Do not silently inherit the old deferral if the product requirement has materially changed; equally, do not reactivate it merely because research exists.

### 4. TPOAb confirmatory-test wiring classification

For the already-active hypothyroid TPOAb variant:

- verify the upstream `confirmatory_tests` content;
- verify whether equivalent governed downstream next-step/intervention content exists;
- classify the gap.

This sprint must decide whether this is:

- a clinical-intelligence compilation gap;
- a presentation/intervention wiring gap;
- already closed;
- or out of product scope.

Do not implement the wiring here.

### 5. TRAb / TSI research-gap verification

Search the canonical research estate, package estate, SSOT/biomarker authority, and governed compiled estate for TRAb / TSI / TSH-receptor-antibody identities and synonyms.

If no governed source exists, classify:

`RESEARCH_REQUIRED`

and define the narrow research question needed for the Medical Research lane.

Do not invent thresholds, biomarker identities, or medical claims.

If valid governed research does exist, classify from evidence instead of creating duplicate research.

### 6. `signal_thyroid_tsh_context`

Verify the existing retirement / exclusion authority.

If still closed, classify:

`RETIRE_OR_SUBSUME — NO FURTHER ARCH-CONV-A WORK`

If later authority reopened it, STOP for architectural review rather than silently reversing the previous decision.

### 7. THY-U5 consumer disease naming

Resolve the exact existing authority boundary for naming:

- Hashimoto's disease;
- Graves' disease;
- autoimmune thyroid disease;
- biochemical hyperthyroid / hypothyroid patterns.

Separate:

1. **clinical follow-up capability** — whether HealthIQ may recommend discussing further testing;
2. **consumer disease naming** — whether the product may name or imply a specific diagnosis/cause.

Do not treat those as the same decision.

Produce a recommended product/medical communication disposition, but if existing ratified authority does not already permit the proposed naming position, mark:

`ANTHONY_RATIFICATION_REQUIRED`

No runtime wording may change in this sprint.

## Required Deliverables

Create:

1. `docs/architecture/ARCH-CONV-A_THYROID_RESIDUAL_AUTHORITY_PACK.md`
2. `docs/architecture/ARCH-CONV-A_THYROID_RESIDUAL_DISPOSITION_REGISTER.yaml`

The YAML register must contain one row per residual frame/item with:

- `item_id`
- `signal_id`
- `frame_id` where known
- `source_authority`
- `current_runtime_state`
- `prior_decision`
- `disposition`
- `requires_medical_research`
- `requires_anthony_ratification`
- `next_work_class`
- `evidence_refs`

Allowed `next_work_class` values:

- `NONE`
- `PROMOTION_COMPILATION`
- `RESEARCH`
- `INTERVENTION_PRESENTATION`
- `GOVERNANCE_ONLY`

Also update the programme continuity register only if the governing register format requires a Stage-0/disposition entry.

## Required Decision Output

The authority pack must end with:

### A. Closed thyroid items
Items requiring no further ARCH-CONV-A work.

### B. Promotion-ready thyroid items
Existing research sufficient; exact next compilation/promotion cohort.

### C. Research-required thyroid items
Only genuine gaps.

### D. Separate product/presentation items
Items that should not be smuggled into compiled-WHY work.

### E. Ratification questions
Only decisions that genuinely require Anthony.

### F. Recommended next implementation package
One bounded package only, based on the disposition evidence.

## Explicit Non-Scope

Do not:

- compile TgAb or any other thyroid WHY;
- activate/deactivate signals;
- edit activation registers;
- edit package signal logic;
- change thyroid thresholds;
- add TRAb/TSI to SSOT;
- conduct new literature research;
- change intervention runtime;
- change frontend copy;
- change disease naming in consumer output;
- reopen already-ratified TSH/FT3/FT4 logic;
- reopen the FT3/TSH firing fix;
- alter cross-domain prioritisation;
- combine iron/haematology or other ARCH-CONV-A domains into this sprint.

## STOP Conditions

STOP and escalate if:

1. current authority conflicts on whether a thyroid residual is active, deferred, rejected, or superseded;
2. TgAb identities cannot be mapped deterministically to source research;
3. TPOAb euthyroid promotion would require new medical policy rather than application of existing evidence;
4. TRAb/TSI evidence exists but its authority status cannot be determined;
5. disease-naming authority conflicts with the current ratified thyroid medical decision;
6. resolving THY-U5 would require changing runtime/consumer behaviour in this sprint;
7. a proposed disposition changes signal identity, threshold, comparator, or firing semantics;
8. the task expands beyond thyroid residual authority/disposition.

## Success Criteria

All must be true:

- every thyroid residual is independently re-verified against current `main`;
- no obsolete Wave-1 assumption is carried forward unexamined;
- TgAb has an explicit governed disposition;
- TPOAb euthyroid variant has an explicit governed disposition;
- TPOAb confirmatory-test gap is correctly classified;
- TRAb/TSI is confirmed as existing authority or genuine research gap;
- `signal_thyroid_tsh_context` is confirmed closed or escalated;
- clinical follow-up capability is explicitly separated from disease naming;
- THY-U5 is either resolved from existing authority or presented as a precise Anthony ratification question;
- no runtime behaviour changes;
- exactly one next implementation/research package is recommended.

## Post-Implementation Closure

Before:

`python backend/scripts/run_work_package.py finish`

run the mandatory Automation Bus v1.3.1 post-implementation closure protocol.

After finish, Claude must independently audit:

1. Did the package use current authority rather than historical Wave-1 assumptions?
2. Is every residual disposition evidence-backed?
3. Did it avoid inventing medical policy or research?
4. Are promotion-ready, research-required, and presentation-only gaps cleanly separated?
5. Did it preserve all existing runtime behaviour?
6. Is the recommended next package genuinely supported by the disposition evidence?

HIGH-risk closure requires GPT architectural review and Anthony approval.

## Hardening Invocation

Use exactly:

`harden work_id: ARCH-CONV-A-THYROID-RESIDUAL-DISPOSITION-1 — verify source content and produce evidence checklist`
