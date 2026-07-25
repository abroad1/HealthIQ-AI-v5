---
work_id: ARCH-CONV-PKG1
branch: feature/arch-conv-pkg1-frame-identity-closure
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
stage_b_mode: MODE_2
runtime_change: YES
---

# ARCH-CONV-PKG1 — Launch-Path Activation-Frame Identity Closure

## Outcome

Close the five verified launch-path activation-frame collapse surfaces so distinct medical frames cannot silently merge after registry load.

This package is limited to frame-identity preservation and related tests.

Do not change provenance policy, package eligibility, WHY content, prose assets, PSI, Gemini, thresholds, signal firing, or frontend medical logic.

Standard Automation Bus governance applies.

## Required inputs

Read only:

```text
docs/planning-papers/HEALTHIQ_AI_V5_FINAL_ARCHITECTURE_CONVERGENCE_AND_SALVAGE_OR_REBUILD_PLAN.md
docs/architecture/HEALTHIQ_AI_V5_CONTROLLED_BETA_ARCHITECTURE_COHORT.md
docs/architecture/HEALTHIQ_AI_V5_CONVERGENCE_VIABILITY_ASSESSMENT.md
docs/architecture/HEALTHIQ_AI_V5_WHY_MIGRATION_PILOT_COHORT.md
docs/architecture/HEALTHIQ_AI_OPEN_ARCHITECTURE_OBLIGATIONS_CC.md
docs/architecture/HEALTHIQ_AI_ARCHITECTURE_RECONCILIATION_VARIANCE_CC_VS_CURSOR.md
docs/architecture/ADR-RT-IDENTITY-PROV-001_activation_frame_and_provenance_integrity.md
```

Inspect current production code and tests for:

```text
backend/core/analytics/interpretation_display_layer_publish_v1.py
backend/core/analytics/domain_score_assembler.py
backend/core/analytics/narrative_report_compiler_v1.py
backend/core/analytics/intervention_selector_v1.py
backend/core/analytics/signal_interaction_builder.py
```

Resolve actual paths where names differ.

Also inspect the existing shared activation-identity helpers and tests before creating new abstractions.

## Gate 0 pressure set

Use the exact multi-frame pressure-set cohort identified by Gate 0.

At minimum verify the families and frames recorded in:

```text
docs/architecture/HEALTHIQ_AI_V5_CONTROLLED_BETA_ARCHITECTURE_COHORT.md
```

Do not substitute a smaller synthetic-only set.

## Phase 1 — Exposure and design confirmation

Before implementation, document for each of the five surfaces:

```text
file
function or class
current keying
frame-destructive behaviour
intentional family-level behaviour, if any
active pressure-set families that reach it
required change
compatibility risk
test strategy
```

Create:

```text
docs/architecture/ARCH-CONV-PKG1_frame_identity_surface_design.md
```

## STOP Gate 1

STOP before implementation if:

- any surface requires choosing one medical frame over another;
- a new clinical priority policy is required;
- the apparent collapse is an intentional, safe family-level aggregation and changing it would alter approved product meaning;
- the required fix expands into provenance, WHY, prose, PSI, signal thresholds or frontend inference;
- Gate 0 pressure-set evidence cannot be reproduced;
- Package 2 eligibility decisions would be required to make Package 1 tests pass.

Record the issue and do not invent policy.

## Required behaviour

### 1. Interpretation display publication

Ensure distinct activation frames are not deduplicated, joined or selected by bare `signal_id`.

Where display-level family grouping is intentional:

- preserve every contributing `activation_key`;
- retain deterministic ordering;
- expose explicit family aggregation metadata;
- do not discard frame-level evidence.

### 2. Domain score assembly

Ensure domain scoring does not silently collapse distinct activation frames.

If domain scoring is intentionally family-based:

- use an explicit governed aggregation step;
- retain frame membership and provenance;
- prove that duplicate frame counting cannot inflate scores unintentionally;
- distinguish frame-preservation from score aggregation.

### 3. Narrative report compilation

Remove any blanking, dropping or replacement of a resolved `activation_key`.

Narrative lead selection must:

- preserve the selected frame;
- remain deterministic;
- avoid falling back to bare `signal_id` when a frame is available;
- fail safely when frame identity is ambiguous;
- not introduce new medical prose selection.

### 4. Intervention selection

Ensure intervention matching and deduplication are frame-safe.

Do not:

- select interventions using only `signal_id` where frames differ;
- invent frame-specific intervention policy;
- expose intervention content for unsupported frames.

Where intervention authority is family-level, label and test that scope explicitly.

### 5. Signal interaction builder

Correct the partial migration.

At minimum:

- graph-node identity must not use bare `signal_id` where distinct frames coexist;
- confidence lookup must be frame-safe;
- interaction edges must preserve participating `activation_key` values;
- family-level interaction logic must be explicit rather than accidental;
- output metadata must reflect actual internal identity behaviour.

Do not treat `participating_activation_keys` output decoration as sufficient.

## Shared implementation rules

- Prefer one canonical shared identity/index helper over five bespoke mappings.
- Reuse Package 2 identity contracts.
- Preserve backward compatibility for genuine single-frame families.
- Do not alter signal activation or thresholds.
- Do not create frontend medical-selection behaviour.
- Deterministic ordering is mandatory.
- Ambiguous or duplicate frame identity must fail closed.
- Family-level aggregation must never destroy frame-level auditability.

## Tests

At minimum prove:

1. two frames sharing one `signal_id` remain distinct across all five surfaces;
2. interaction nodes and confidence maps are keyed frame-safely;
3. narrative lead selection retains the correct `activation_key`;
4. display publication preserves all contributing frames;
5. domain scoring does not double-count or collapse frames silently;
6. intervention selection does not borrow another frame’s intervention;
7. intentional family-level aggregation preserves member activation keys;
8. ambiguous frame identity fails safely;
9. repeated runs produce identical ordering and outputs;
10. single-frame behaviour remains compatible;
11. all Gate 0 pressure-set families are exercised;
12. deliberately invalid fixtures fail the relevant validation gate.

Run relevant existing:

- identity/provenance tests;
- signal interaction tests;
- domain scoring tests;
- narrative compiler tests;
- intervention selector tests;
- report and DTO tests;
- golden panel tests;
- replay/auditability tests;
- architecture validation gate;
- NO-LLM tests;
- frontend type/render tests where DTOs change.

## Validation gate

Extend the existing architecture validation flow only if needed to detect residual bare-`signal_id` collapse on these five surfaces.

The gate must be specific and executable, not source-text-only where behavioural verification is possible.

It must fail on a deliberately invalid multi-frame fixture.

## Forbidden scope

Do not:

- change provenance eligibility or runtime reachability;
- add or attach `source_spec_id`;
- suppress packages;
- migrate WHY assets;
- edit medical hypotheses;
- create prose;
- activate modifiers;
- wire PSI;
- enable Gemini;
- change signal thresholds or activation logic;
- redesign DTOs beyond additive identity metadata required for correctness;
- redesign the frontend;
- declare architecture convergence or beta readiness.

## Deliverables

Create:

```text
docs/architecture/ARCH-CONV-PKG1_frame_identity_surface_design.md
docs/audit-papers/ARCH-CONV-PKG1_implementation_and_verification_report.md
```

Update the BUILD register with:

- package outcome;
- exact surfaces closed;
- pressure-set coverage;
- tests and gates;
- unresolved items;
- no beta-readiness claim.

## Acceptance criteria

- [ ] All five surfaces were assessed against live code.
- [ ] STOP Gate 1 passed or escalated.
- [ ] No frame-destructive bare-`signal_id` logic remains on the five launch-path surfaces.
- [ ] Interaction node and confidence identity are genuinely frame-safe.
- [ ] Intentional family-level aggregation is explicit and auditable.
- [ ] Narrative lead frame identity is preserved.
- [ ] Domain scoring cannot silently collapse or double-count frames.
- [ ] Intervention selection cannot borrow across frames.
- [ ] Gate 0 pressure-set families are covered.
- [ ] Determinism and backward compatibility are proven.
- [ ] Relevant architecture gates and tests pass.
- [ ] No provenance, WHY, prose, PSI, Gemini or threshold scope entered.
- [ ] No architecture-completion or beta-readiness claim was made.

## STOP conditions

STOP if:

1. a medical frame-priority rule is required;
2. any fix requires changing signal firing or thresholds;
3. package scope grows by more than 25% without human reauthorisation;
4. more than one unplanned mandatory follow-on package is identified;
5. Package 2 provenance decisions become a prerequisite;
6. a launch-critical behaviour regression cannot be explained and approved;
7. the five-surface obligation cannot be closed without estate-wide redesign;
8. required gates fail for an unexplained reason.

## Gate 1 output

At completion, recommend exactly one:

```text
GO
CORRECT
STOP
V6
```

Definitions:

- `GO`: Package 1 obligation is closed; proceed to Package 2.
- `CORRECT`: one bounded correction is required.
- `STOP`: convergence approach is no longer credible without redesign.
- `V6`: kill criteria are met; freeze v5 architecture changes.

## Verification report

The report must include:

- baseline SHA;
- branch;
- files changed;
- per-surface before/after behaviour;
- pressure-set coverage;
- test commands and exit codes;
- validation-gate evidence;
- acceptance-criteria table;
- STOP-condition assessment;
- Gate 1 recommendation;
- unresolved limitations.

Do not merge without explicit human authority.
