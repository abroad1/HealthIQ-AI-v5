---
work_id: ARCH-CONV-PKG3
branch: feature/arch-conv-pkg3-why-authority-migration
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
stage_b_mode: MODE_2
runtime_change: YES
---

# ARCH-CONV-PKG3 — WHY Authority Migration and Pilot Promotion

## Outcome

Complete the bounded WHY-authority migration for the approved five-signal / ten-frame pilot as one outcome-based package.

This package must:

1. complete the remaining evidence and identity prerequisites;
2. prove the compiled-authority migration architecture;
3. prepare the consolidated medical-review pack;
4. STOP for GPT medical review and Anthony ratification;
5. implement only ratified frame decisions;
6. retire superseded legacy WHY authority safely;
7. prove that dual authority, unsupported promotion and replay ambiguity are impossible;
8. produce the final Package 3 GO / CORRECT / STOP / V6 recommendation.

Do not split this outcome into separate architecture, evidence, medical-content, retirement or clean-up sprints unless a STOP condition proves that separation is required for safety.

Standard Automation Bus and Knowledge Bus governance apply.

## Ratified governance model

The Gate 2.5 decisions are authoritative for this package:

```text
GPT = HealthIQ AI Head of Medical Research
Anthony = human project authority and production ratifier
engineering implements only Anthony-ratified decisions
```

The review format is one consolidated five-signal review pack containing ten frame-level decisions.

Separate detailed frame records are required only where risk, disagreement, revision history or audit needs justify them.

## Required inputs

Read only the current merged versions of:

```text
docs/planning-papers/HEALTHIQ_AI_V5_FINAL_ARCHITECTURE_CONVERGENCE_AND_SALVAGE_OR_REBUILD_PLAN.md
docs/architecture/HEALTHIQ_AI_V5_WHY_MIGRATION_PILOT_COHORT.md
docs/architecture/HEALTHIQ_AI_V5_WHY_PILOT_MEDICAL_REVIEW_READINESS.md
docs/Medical Research Documents/HEALTHIQ_AI_V5_WHY_PILOT_MEDICAL_REVIEW_DECISION_TEMPLATE.md
docs/architecture/HEALTHIQ_AI_V5_CONTROLLED_BETA_ARCHITECTURE_COHORT.md
docs/architecture/HEALTHIQ_AI_V5_CONVERGENCE_VIABILITY_ASSESSMENT.md
docs/architecture/ARCH-CONV-PKG2_launch_critical_provenance_decision_inventory.md
docs/audit-papers/ARCH-CONV-PKG2_implementation_and_verification_report.md
docs/audit-papers/ARCH-CONV-GATE2_5_implementation_and_verification_report.md
docs/architecture/ADR-RT-003*
docs/architecture/ADR-RT-IDENTITY-PROV-001_activation_frame_and_provenance_integrity.md
```

Resolve actual repository paths where names differ.

Inspect current production code, schemas, assets and tests for:

```text
compiled hypothesis authority
legacy root-cause YAML authority
root-cause registry
runtime authority selection
activation-frame binding
provenance and source_spec_id
report compilation
consumer WHY output
clinician WHY output
replay and audit manifests
architecture validation gates
```

## Approved pilot boundary

Use exactly the Gate 0 / Gate 2.5 pilot:

```text
5 signal families
10 activation frames
9 full medical reviews
1 retirement confirmation
```

Do not add frames or signal families without explicit human reauthorisation.

## Internal Phase 1 — Evidence and identity prerequisites

Before architecture or content promotion:

1. identify the six pilot frames that currently rely on Batch JSON rather than standalone investigation specifications;
2. extract standalone `inv_*.yaml` files using the byte-identical method independently verified in ARCH-CONV-PKG2;
3. add `inv_tpo_ab_high_euthyroid_autoimmune_risk` to `medical_frame_identity_index_v1.yaml`;
4. validate exact `signal_id`, `activation_key`, `source_spec_id` and package linkage for all ten frames;
5. prove zero medical-content drift from canonical source research.

Create:

```text
docs/architecture/ARCH-CONV-PKG3_pilot_evidence_and_identity_inventory.md
```

### STOP Gate A

STOP if:

- any standalone extraction differs materially from canonical source research;
- a `source_spec_id` must be invented;
- a pilot frame cannot be reconciled to the medical identity index;
- multiple plausible source frames exist without an approved choice;
- the exact ten-frame cohort cannot be reproduced.

Do not proceed to architecture implementation until Gate A passes.

## Internal Phase 2 — Compiled-authority architecture proof

Prove the migration architecture before promoting newly reviewed content.

At minimum:

- identify the current compiled vitamin D pilot path;
- identify all active legacy WHY paths for the ten-frame cohort;
- define one canonical per-frame WHY-authority decision;
- prevent compiled and legacy authority from both operating for the same `activation_key`;
- fail closed when authority is missing, contradictory or unratified;
- preserve activation-frame identity and explicit provenance;
- preserve deterministic replay;
- preserve intentional family-level presentation only where frame membership remains auditable;
- ensure retirement is reversible through version control and audit history, not through simultaneous runtime authority.

Create:

```text
docs/architecture/ARCH-CONV-PKG3_compiled_why_authority_design.md
```

### Required authority states

Use an explicit governed state model equivalent to:

```text
LEGACY_ACTIVE
COMPILED_CANDIDATE
MEDICALLY_APPROVED
HUMAN_RATIFIED
COMPILED_ACTIVE
LEGACY_RETIRED
REJECTED
DEFERRED
BLOCKED
```

The exact implementation may adapt to existing contracts, but must preserve these distinctions.

### STOP Gate B

STOP if:

- retirement requires deleting evidence history;
- authority cannot be selected per activation frame;
- the design depends on bare `signal_id` where frames differ;
- legacy and compiled authority cannot be prevented from co-serving;
- runtime selection would need a new medical-priority policy;
- implementation expands into unrelated prose, PSI, Gemini or signal-threshold work.

## Internal Phase 3 — Consolidated medical-review pack

Prepare one consolidated review pack for GPT medical review.

Create:

```text
docs/Medical Research Documents/HEALTHIQ_AI_V5_WHY_PILOT_CONSOLIDATED_MEDICAL_REVIEW.md
```

The pack must contain one section for each of the ten frames and must include:

```text
signal_id
activation_key
source_spec_id
current legacy authority
proposed compiled authority
medical interpretation
evidence summary
causal limits
consumer wording boundary
clinician wording boundary
approved hypotheses
rejected hypotheses
uncertainty
confirmatory-test context
modifier compatibility
legacy-parity assessment
proposed production disposition
```

Allowed proposed dispositions:

```text
APPROVE_FOR_COMPILED_PROMOTION
APPROVE_WITH_REVISIONS
REJECT
DEFER_PENDING_RESEARCH
RETIREMENT_CONFIRMATION_ONLY
```

Cursor must assemble the evidence pack but must not make the medical decision on GPT's behalf.

## Mandatory Human STOP Gate C — Medical review and ratification

After the consolidated pack is assembled:

STOP implementation and provide the pack for:

1. GPT medical review;
2. Anthony's explicit frame-level ratification.

Do not continue automatically.

The continuation authority must identify, for every frame:

```text
GPT medical-review decision
required revisions
Anthony ratification decision
final implementation disposition
```

No frame may be promoted because another frame in the same signal family was approved.

No blank, implied, batch-level or inherited ratification is permitted.

## Internal Phase 4 — Implement only ratified decisions

After explicit continuation authority:

- implement only frames ratified by Anthony;
- apply all required revisions exactly;
- compile approved hypotheses into the governed authority model;
- preserve source and decision lineage;
- keep rejected or deferred frames inactive;
- do not create substitute content for rejected frames;
- do not reinterpret the medical decision;
- ensure consumer and clinician boundaries match the ratified record.

For the retirement-confirmation frame:

- confirm the existing compiled authority is medically acceptable;
- retire the legacy authority only after explicit ratification and runtime parity checks.

## Internal Phase 5 — Legacy retirement and dual-authority prevention

For each promoted frame:

- make compiled authority canonical;
- make superseded legacy authority non-runtime-reachable;
- preserve legacy content as historical evidence where repository policy requires;
- record retirement identity, date, work ID and replacement authority;
- prove that no runtime path can select both;
- prove that fallback cannot silently reactivate retired content;
- ensure missing compiled assets fail closed rather than falling back to retired legacy authority.

Create:

```text
docs/architecture/ARCH-CONV-PKG3_legacy_retirement_and_authority_register.md
```

## Internal Phase 6 — Verification and convergence evidence

At minimum prove:

1. all ten pilot frames have explicit evidence and identity records;
2. every promoted frame has GPT review and Anthony ratification;
3. no unratified frame can become runtime-active;
4. no activation frame has simultaneous compiled and legacy authority;
5. rejected and deferred frames remain inactive;
6. legacy retirement is explicit and auditable;
7. retired legacy authority cannot silently return through fallback;
8. consumer output respects consumer wording boundaries;
9. clinician output respects clinician wording boundaries;
10. activation keys and source specifications survive runtime and replay;
11. family-level presentation preserves participating frame identity;
12. repeated runs are deterministic;
13. Package 1 frame-identity controls remain intact;
14. Package 2 provenance/reachability controls remain intact;
15. deliberately invalid authority fixtures fail closed;
16. no unrelated WHY estate is modified.

Run all relevant:

- compiled hypothesis tests;
- legacy root-cause registry tests;
- activation-frame identity tests;
- provenance/reachability tests;
- report compiler tests;
- consumer and clinician output tests;
- replay/auditability tests;
- golden and representative panels;
- architecture validation gates;
- NO-LLM tests;
- medical asset validation;
- frontend type/render tests where additive DTO metadata changes.

## Validation gate

Add or extend one executable WHY-authority migration gate.

It must detect:

- simultaneous compiled and legacy authority for one activation key;
- compiled authority without medical review;
- compiled authority without Anthony ratification;
- retired legacy authority still runtime-reachable;
- missing or mismatched source specification;
- bare-signal family collapse where frame authority differs;
- rejected or deferred frame becoming active;
- implicit fallback to retired legacy content;
- replay authority mismatch;
- unknown or contradictory authority state.

The gate must exercise real runtime selection behaviour.

## Golden and representative-output review

For every output change:

- identify the frame and authority responsible;
- compare legacy and compiled behaviour;
- classify the change as intended, required revision, regression or unresolved;
- confirm alignment with the ratified medical-review pack;
- STOP on unexplained clinical drift.

Create:

```text
docs/architecture/ARCH-CONV-PKG3_output_parity_and_change_report.md
```

## Scope discipline

This package may contain internal phases and commits, but remains one work package.

Do not create follow-on sprints for work already required to achieve this package outcome.

A separate follow-on package is allowed only if a STOP condition proves:

- unresolved medical research is required;
- a new product or clinical policy is required;
- an unrelated architecture domain must change;
- the package exceeds the ratified scope-growth ceiling;
- a programme kill criterion is met.

## Forbidden scope

Do not:

- expand beyond the ten pilot frames;
- migrate the remaining legacy WHY estate;
- invent medical content;
- change signal thresholds or firing logic;
- wire PSI;
- enable Gemini;
- redesign the frontend;
- perform general prose-library expansion;
- regenerate unrelated packages;
- declare controlled-beta readiness;
- weaken human ratification requirements;
- replace frame-level decisions with family-level approval.

## Deliverables

Create:

```text
docs/architecture/ARCH-CONV-PKG3_pilot_evidence_and_identity_inventory.md
docs/architecture/ARCH-CONV-PKG3_compiled_why_authority_design.md
docs/Medical Research Documents/HEALTHIQ_AI_V5_WHY_PILOT_CONSOLIDATED_MEDICAL_REVIEW.md
docs/architecture/ARCH-CONV-PKG3_legacy_retirement_and_authority_register.md
docs/architecture/ARCH-CONV-PKG3_output_parity_and_change_report.md
docs/audit-papers/ARCH-CONV-PKG3_implementation_and_verification_report.md
```

Update:

```text
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

Record:

- exact frames reviewed;
- GPT decisions;
- Anthony ratification;
- frames promoted;
- frames revised;
- frames rejected or deferred;
- legacy authorities retired;
- validation and output changes;
- unresolved limitations;
- no beta-readiness claim.

## Acceptance criteria

- [ ] Exact five-signal / ten-frame cohort preserved.
- [ ] Six standalone investigation specifications extracted byte-identically.
- [ ] Missing TPO antibody identity-index entry added.
- [ ] Evidence and identity Gate A passed.
- [ ] Compiled-authority architecture Gate B passed.
- [ ] Consolidated review pack completed.
- [ ] Mandatory STOP Gate C observed.
- [ ] GPT review recorded for every frame.
- [ ] Anthony ratification recorded for every frame.
- [ ] Only ratified frames promoted.
- [ ] No frame has dual runtime authority.
- [ ] Legacy retirement is explicit and auditable.
- [ ] Rejected and deferred frames remain inactive.
- [ ] Consumer and clinician boundaries are enforced.
- [ ] Provenance, frame identity and replay remain deterministic.
- [ ] Relevant tests, golden panels and validation gates pass.
- [ ] Package 1 and Package 2 protections remain intact.
- [ ] No unrelated WHY estate or forbidden scope entered.
- [ ] No architecture-completion or beta-readiness claim made.

## Programme STOP conditions

STOP if:

1. canonical evidence or frame identity cannot be established;
2. medical review rejects the migration model materially;
3. Anthony does not ratify enough of the pilot to prove the outcome;
4. dual authority cannot be prevented;
5. output parity exposes unexplained clinical drift;
6. package scope grows by more than 25% without reauthorisation;
7. more than one unplanned mandatory follow-on package is identified;
8. an unrelated architecture domain becomes necessary;
9. required gates fail for an unexplained reason;
10. completion requires weakening provenance, identity or ratification controls.

## Final Package 3 decision

Recommend exactly one:

```text
GO
CORRECT
STOP
V6
```

Definitions:

- `GO`: bounded WHY migration and promotion outcome is closed; proceed to final independent convergence audit.
- `CORRECT`: one bounded correction is required within the existing package.
- `STOP`: the v5 convergence approach requires redesign.
- `V6`: ratified kill criteria are met; freeze v5 architecture changes.

## Verification report

Include:

- baseline SHA;
- branch and internal phase commits;
- files changed;
- Gate A, Gate B and Gate C evidence;
- exact ten-frame review and ratification table;
- authority before/after per frame;
- legacy retirement evidence;
- output parity results;
- test commands and exit codes;
- validation-gate evidence;
- acceptance-criteria table;
- STOP-condition assessment;
- final Package 3 recommendation;
- unresolved limitations.

Do not merge without explicit human authority.
