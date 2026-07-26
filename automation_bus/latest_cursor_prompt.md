---
work_id: ARCH-CONV-GATE2_5
branch: feature/arch-conv-gate2-5-medical-review-readiness
risk_level: STANDARD
execution_model: TWO_PHASE_START_FINISH
change_type: CONTENT
stage_b_mode: MODE_2
runtime_change: NONE
---

# ARCH-CONV-GATE2.5 — WHY Pilot Medical Review Ownership and Capacity Confirmation

## Outcome

Confirm that the bounded WHY migration pilot has a named medical-review owner, a complete evidence pack, a governed decision format, and sufficient review capacity before Package 3A/3B begins.

This is a governance and readiness gate.

Do not change runtime code, schemas, signal packages, hypotheses, prose, tests, loaders or production behaviour.

Standard Automation Bus and Knowledge Bus governance apply.

## Required inputs

Read only:

```text
docs/planning-papers/HEALTHIQ_AI_V5_FINAL_ARCHITECTURE_CONVERGENCE_AND_SALVAGE_OR_REBUILD_PLAN.md
docs/architecture/HEALTHIQ_AI_V5_WHY_MIGRATION_PILOT_COHORT.md
docs/architecture/HEALTHIQ_AI_V5_CONTROLLED_BETA_ARCHITECTURE_COHORT.md
docs/architecture/HEALTHIQ_AI_V5_CONVERGENCE_VIABILITY_ASSESSMENT.md
docs/architecture/ARCH-CONV-PKG2_launch_critical_provenance_decision_inventory.md
docs/audit-papers/ARCH-CONV-PKG2_implementation_and_verification_report.md
docs/architecture/ADR-RT-003*
docs/architecture/ADR-RT-IDENTITY-PROV-001_activation_frame_and_provenance_integrity.md
```

Resolve actual repository paths where names differ.

Also inspect the current source research, investigation specifications, legacy WHY YAML, compiled hypothesis pilot, report outputs and tests for the exact pilot cohort.

## Gate questions

### 1. Exact pilot cohort

Confirm the exact five-signal / ten-frame pilot cohort from Gate 0.

For each frame record:

```text
signal_id
activation_key
source_spec_id
current WHY authority
legacy YAML asset
compiled hypothesis status
consumer output surface
clinician output surface
medical review type required
```

Do not silently add or remove frames.

### 2. Medical-review ownership

Record:

```text
primary medical-review owner
review role
decision authority
human ratification authority
engineering implementation owner
independent audit owner
```

Operating model:

```text
GPT Head of Medical Research
→ conducts structured medical evidence review
→ records APPROVE / REVISE / REJECT decisions
→ human project authority explicitly ratifies production promotion
→ engineering implements only ratified assets
→ independent audit verifies runtime authority and evidence fidelity
```

Do not treat GPT review alone as production authorisation.

### 3. Evidence-pack completeness

For each pilot frame confirm availability of:

- canonical investigation specification;
- original source research;
- current legacy WHY YAML;
- current runtime output examples;
- activation-frame definition;
- existing medical-review decisions;
- known limitations and safety constraints;
- relevant tests and fixtures;
- provenance identity.

Mark each item:

```text
AVAILABLE
MISSING
STALE
CONFLICTING
NOT_APPLICABLE
```

### 4. Review workload

For each pilot frame classify the required work:

```text
RETIREMENT_CONFIRMATION_ONLY
LIGHT_REVIEW
FULL_NEW_MEDICAL_REVIEW
RESEARCH_GAP
BLOCKED
```

Report totals for:

- frames requiring full review;
- frames requiring only retirement confirmation;
- frames requiring new research;
- unresolved frames.

### 5. Review decision standard

Create one reusable decision template containing:

```text
frame identity
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
production disposition
reviewer
review date
human ratification
```

Allowed frame decisions:

```text
APPROVE_FOR_COMPILED_PROMOTION
APPROVE_WITH_REVISIONS
REJECT
DEFER_PENDING_RESEARCH
RETIREMENT_CONFIRMATION_ONLY
```

### 6. Capacity and programme viability

Confirm whether the pilot can be reviewed within the ratified convergence programme ceilings.

Record:

```text
review owner confirmed
human ratifier confirmed
review inputs complete
estimated review units
blocking research gaps
programme-window fit
capacity conclusion
```

Allowed capacity conclusions:

```text
READY
READY_WITH_CONDITIONS
NOT_READY
```

Do not invent availability, commitment or dates.

## Required outputs

Create:

```text
docs/architecture/HEALTHIQ_AI_V5_WHY_PILOT_MEDICAL_REVIEW_READINESS.md
docs/medical-research/HEALTHIQ_AI_V5_WHY_PILOT_MEDICAL_REVIEW_DECISION_TEMPLATE.md
docs/audit-papers/ARCH-CONV-GATE2_5_implementation_and_verification_report.md
```

Resolve the medical-research folder path according to repository convention.

## Decision

Issue exactly one Gate 2.5 decision:

```text
GO
CONDITIONAL_GO
STOP
V6
```

### GO

Use only if:

- exact cohort is confirmed;
- medical-review owner is named;
- human ratifier is named;
- evidence pack is complete enough;
- workload is bounded;
- review capacity is credible;
- no material research gap blocks the pilot.

### CONDITIONAL_GO

Use if:

- architecture remains viable;
- the pilot is bounded;
- only specific, enumerated evidence or ownership conditions remain;
- those conditions can be completed without changing Package 3 scope.

List every condition explicitly.

### STOP

Use if:

- ownership or capacity is unavailable;
- evidence is materially incomplete;
- the pilot requires redesign;
- medical review cannot fit within programme ceilings.

### V6

Use only if the Gate 2.5 findings meet a ratified programme kill criterion and show that v5 convergence is no longer credible.

## STOP conditions

STOP and escalate if:

1. the pilot cohort cannot be reconciled to Gate 0;
2. canonical research is missing for a pilot frame;
3. current legacy WHY cannot be identified;
4. a frame requires new medical interpretation outside approved research;
5. decision authority is unclear;
6. human ratification ownership is absent;
7. review effort exceeds programme ceilings;
8. Package 3 architecture design must change before review can proceed;
9. repository state is not clean at package start.

## Acceptance criteria

- [ ] Exact five-signal / ten-frame cohort is confirmed or discrepancy escalated.
- [ ] Medical-review owner is named.
- [ ] Human production-ratification authority is named.
- [ ] Evidence-pack status is recorded for every frame.
- [ ] Review workload is classified per frame.
- [ ] Reusable medical-review decision template is created.
- [ ] Capacity is assessed honestly.
- [ ] GO / CONDITIONAL_GO / STOP / V6 decision is issued.
- [ ] No runtime, schema, signal, hypothesis, prose or test files are changed.
- [ ] No medical asset is approved or promoted in this gate.
- [ ] No beta-readiness declaration is made.

## Verification report

Include:

- baseline SHA;
- branch;
- evidence read;
- cohort table;
- ownership decision;
- evidence-pack completeness;
- workload totals;
- capacity assessment;
- decision-template path;
- acceptance-criteria table;
- STOP-condition assessment;
- Gate 2.5 decision;
- unresolved limitations.

Do not merge without explicit human authority.
