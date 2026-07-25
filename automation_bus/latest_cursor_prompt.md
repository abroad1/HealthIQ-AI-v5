---
work_id: P3-LAYERB-INTEL-1
branch: feature/p3-layerb-intel-1-frame-routing-why-depth
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
stage_b_mode: MODE_2
knowledge_bus_impact: YES
medical_review_gate: REQUIRED
---

# P3-LAYERB-INTEL-1 — Layer B Intelligence Completion

## Outcome

Deliver a deterministic, frame-correct Layer B explanation system with governed modifier binding, frame-aware prose routing, expanded compiled WHY coverage, and sufficient validation evidence for controlled-beta reassessment.

Standard Automation Bus and Knowledge Bus governance apply.

## Required inputs

Read only:

```text
docs/architecture/HEALTHIQ_AI_CURRENT_STATE_BASELINE_2026-07-25.md
docs/architecture/ADR-RT-IDENTITY-PROV-001_activation_frame_and_provenance_integrity.md
docs/architecture/ARCH-RT-IDENTITY-PROV-1_launch_critical_provenance_inventory.md
docs/audit-papers/ARCH-RT-IDENTITY-PROV-1_implementation_and_verification_report.md
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

Also inspect the current production implementations and tests for:

```text
retail explainers
pathway / functional / entity packs
root-cause compilation
compiled hypothesis loading
clinician report compilation
narrative report compilation
modifier catalogue
frame routing
frontend Layer B DTO consumers
```

Do not read unrelated historical strategy or sprint papers unless repository reality requires them.

## Scope

### 1. Frame-aware prose routing

Implement deterministic prose selection using `activation_key` / `source_spec_id`.

Requirements:

- no prose selection by bare `signal_id` where multiple frames exist;
- explicit fallback for legacy family-level content;
- no wrong-frame prose attachment;
- deterministic ordering;
- no frontend medical inference.

### 2. Modifier binding

Implement governed binding for supported modifiers only.

Requirements:

- explicit eligibility rules;
- deterministic precedence;
- contradiction handling;
- fail-safe behaviour for unsupported combinations;
- provenance for selected modifiers;
- no free-form LLM selection.

### 3. Compiled WHY expansion

Expand compiled root-cause authority beyond the current pilot only for a bounded, medically reviewed cohort.

Requirements:

- preserve Package 2 frame identity and provenance contracts;
- use versioned compiled artefacts;
- retain legacy family-level labels where migration is incomplete;
- do not silently convert legacy family-level WHY into frame-specific authority;
- no broad estate migration.

### 4. Round 2 prose pipeline

Create medically reviewed production-ready prose from current research authority.

Requirements:

- MR-BATCH-001B remains benchmark/test-only;
- no direct promotion of its candidate text;
- Round 2 assets must be newly authored, reviewed, versioned and validated;
- consumer and clinician variants remain distinct where required;
- unsupported claims must not be introduced.

### 5. Coverage and validation

Expand only the launch-critical Layer B cohort needed for controlled-beta reassessment.

Include:

- representative normal, abnormal, conflicting and incomplete panels;
- same-`signal_id` multi-frame cases;
- modifier combinations;
- legacy fallback cases;
- provenance and replay checks;
- frontend render-only verification.

## Phase 1 — Design and inventory

Before implementation:

1. Identify active Layer B content authorities and runtime selection paths.
2. Produce a bounded migration cohort.
3. Map each cohort item to:
   - activation frame;
   - current prose authority;
   - current WHY authority;
   - modifier needs;
   - provenance state;
   - medical-review requirement.
4. Confirm which assets are production, legacy, candidate or test-only.
5. Confirm MR-BATCH-001B has zero production imports.

Create:

```text
docs/architecture/P3-LAYERB-INTEL-1_migration_and_coverage_inventory.md
```

## STOP Gate 1

STOP before implementation if:

- frame routing policy is ambiguous;
- modifier precedence requires a product or medical decision;
- a WHY mapping cannot be tied to a defensible frame;
- provenance is unresolved for a proposed promoted asset;
- migration would require broad legacy rewrite;
- frontend changes would introduce medical inference.

Record the decision before continuing.

## Deliverables

### A. Frame-routing contract

Create or update one canonical runtime contract for:

```text
activation frame
prose asset eligibility
modifier eligibility
fallback authority
selection provenance
```

Avoid duplicated selectors.

### B. Modifier binder

Implement one deterministic binder used by all relevant Layer B compilers.

### C. Prose registry / compiled assets

Add only the bounded, reviewed Round 2 assets required by the migration inventory.

### D. Compiled WHY cohort

Promote only the approved cohort through the existing compiled-hypothesis path.

### E. Runtime integration

Wire routing, modifiers and compiled WHY into:

```text
root-cause output
consumer narrative
clinician report
DTO / replay evidence
```

### F. Validation gate

Add one Layer B integrity gate to the existing architecture validation flow.

It must detect:

- wrong-frame prose;
- unsupported modifier combinations;
- missing provenance;
- false production status;
- candidate/test-only asset imports;
- frame-specific WHY bound to family-level authority;
- non-deterministic output.

### G. Continuity

Update the BUILD register with:

- cohort delivered;
- content and WHY authority changes;
- medical-review decisions;
- unresolved legacy coverage;
- validation results;
- no controlled-beta authorisation.

## Medical review

Medical review is required before any new prose or compiled WHY asset becomes production authority.

The review must approve:

- frame fit;
- claim accuracy;
- consumer wording;
- clinician wording;
- modifier effect;
- confirmatory-test wording;
- fallback behaviour.

Do not treat schema validation as medical approval.

## Tests

At minimum prove:

1. same-family frames receive the correct distinct prose;
2. unsupported frames do not borrow another frame’s prose;
3. modifier precedence is deterministic;
4. contradictory modifiers fail safely;
5. legacy family-level fallback is labelled honestly;
6. compiled WHY selects by activation frame;
7. candidate/test-only content cannot load in production;
8. MR-BATCH-001B remains isolated;
9. consumer and clinician outputs preserve provenance;
10. replay round-trip preserves selected asset IDs and modifiers;
11. repeated runs produce identical output;
12. frontend renders backend decisions without medical inference;
13. old single-frame outputs remain compatible;
14. the Layer B gate fails on deliberately invalid fixtures.

Run relevant existing:

- architecture and launch-estate gates;
- identity/provenance gate;
- root-cause and clinician-report suites;
- narrative and retail-explainer suites;
- replay/auditability tests;
- golden panels;
- NO-LLM tests;
- PSI and MR-BATCH isolation tests;
- frontend type and render tests.

## Forbidden scope

Do not:

- activate PSI;
- promote MR-BATCH-001B;
- enable Gemini;
- change thresholds or signal firing;
- redesign the results page;
- migrate the entire legacy WHY estate;
- create unreviewed medical claims;
- alter Package 2 identity/provenance contracts;
- declare controlled-beta readiness.

## Acceptance criteria

- [ ] Migration cohort is bounded and documented.
- [ ] STOP Gate 1 is passed or escalated.
- [ ] Frame-aware prose routing is production-wired.
- [ ] Modifier binding is deterministic and governed.
- [ ] Approved compiled WHY cohort is production-wired.
- [ ] Round 2 assets have explicit medical approval.
- [ ] Candidate/test-only assets remain isolated.
- [ ] Provenance is preserved through DTO and replay.
- [ ] Layer B integrity gate is CI-wired.
- [ ] Required tests pass.
- [ ] No PSI, Gemini or MR-BATCH promotion occurred.
- [ ] No controlled-beta claim was made.

## STOP conditions

STOP if:

1. medical review rejects any proposed production asset;
2. source authority is ambiguous;
3. a frame-specific mapping requires unsupported inference;
4. modifier behaviour changes clinical meaning without approval;
5. Package 2 identity/provenance contracts would need redesign;
6. a candidate asset is required to make tests pass;
7. implementation expands beyond the bounded cohort;
8. required gates fail for an unexplained reason.

## Output

Create:

```text
docs/audit-papers/P3-LAYERB-INTEL-1_implementation_and_verification_report.md
```

Include:

- baseline SHA;
- migration cohort;
- medical-review evidence;
- files changed;
- routing and modifier decisions;
- compiled WHY changes;
- test commands and exit codes;
- acceptance-criteria table;
- STOP-condition assessment;
- unresolved carry-forwards.

Do not merge without explicit human authority.
