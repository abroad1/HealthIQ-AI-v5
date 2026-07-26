---
work_id: ARCH-CONV-CORRECT-1
branch: feature/arch-conv-correct-1-e2e-authority-layerc
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
stage_b_mode: MODE_2
runtime_change: YES
---

# ARCH-CONV-CORRECT-1 — End-to-End Medical Authority and Layer C Boundary Closure

## Outcome

Close the final programme-level defects identified by `ARCH-CONV-FINAL-AUDIT`.

The correction must prove that rejected, retired, legacy, sibling-frame or frontend-derived medical logic cannot survive anywhere from Layer B activation through final Layer C presentation.

This package is one outcome-based correction sprint with four internal workstreams:

1. rejected-frame total inactivation;
2. legacy “methylation capacity” wording retirement;
3. MCV frame co-service control;
4. Layer C medical-boundary closure.

Do not split these into separate sprints unless a STOP condition proves that separation is required for safety.

Standard Automation Bus and Knowledge Bus governance apply.

## Authoritative audit inputs

Read the current audit-branch versions of:

```text
docs/testing/ARCH-CONV-FINAL_frontend_end_to_end_uat.md
docs/audit-papers/ARCH-CONV-FINAL-AUDIT_implementation_and_verification_report.md
docs/architecture/ARCH-CONV-FINAL_programme_obligation_closure_matrix.md
docs/architecture/ARCH-CONV-FINAL_end_to_end_pipeline_and_leakage_report.md
docs/architecture/ARCH-CONV-FINAL_layer_c_boundary_and_leakage_inventory.md
```

Also read the current merged versions of:

```text
docs/Medical Research Documents/HEALTHIQ_AI_V5_WHY_PILOT_MEDICAL_REVIEW_GPT_REVIEWED_ANTHONY_RATIFIED.md
docs/architecture/ARCH-CONV-PKG3_compiled_why_authority_design.md
docs/architecture/ARCH-CONV-PKG3_legacy_retirement_and_authority_register.md
docs/architecture/ARCH-CONV-PKG3_output_parity_and_change_report.md
docs/audit-papers/ARCH-CONV-PKG3_implementation_and_verification_report.md
docs/audit-papers/ARCH-CONV-PKG2_implementation_and_verification_report.md
docs/audit-papers/ARCH-CONV-PKG1_implementation_and_verification_report.md
knowledge_bus/governance/compiled_why_authority_register_v1.yaml
```

Resolve actual repository paths where names differ.

## Authoritative live UAT case

Use the exact previously audited analysis:

```text
analysis_id=e34aaedf-b09f-42f0-8cc8-4653a00b4c10
```

This analysis must be rerun or replayed after correction and compared against the final-audit baseline.

Do not write credentials into source files, commits, reports, screenshots or logs.

## Confirmed defects to close

The final audit found the following `ACTIVE_LEAK` defects:

1. Rejected frame  
   `signal_homocysteine_high::inv_homocysteine_high_metabolic`  
   still fires, appears in `top_findings`, and is referenced by intervention `activation_key_refs`.

2. Signal interpretation still renders:  
   `Reflects methylation capacity and B-vitamin status.`

3. Clinician summary still surfaces legacy wording equivalent to:  
   `reduced B12-related methylation capacity`.

4. Consumer output still surfaces a `Methylation pathway pattern`.

5. MCV anchor, megaloblastic and non-megaloblastic WHY can co-emit despite the ratified frame-specific intent.

6. Previously identified Layer C frontend medical-boundary leaks remain active.

The package must close all six findings together.

# Internal Workstream 1 — Rejected-frame total inactivation

## Required behaviour

A frame with governed WHY authority state `REJECTED` must be non-active across the entire medical pipeline, not merely skipped by the root-cause compiler.

For:

```text
signal_homocysteine_high::inv_homocysteine_high_metabolic
```

prove that it cannot:

- enter the active signal result set;
- be marked fired;
- participate in ranking;
- appear in `top_findings`;
- contribute to domain scoring;
- contribute to narrative lead selection;
- appear in intervention `signal_refs` or `activation_key_refs`;
- appear in consumer or clinician summaries;
- appear in replay as an active medical result;
- act as a fallback for another frame;
- provide interpretation text.

Its rejection may remain visible only in governed audit or authority-state records.

## Canonical policy

Create or reuse one canonical frame-runtime-authority decision consumed early enough in the pipeline to prevent downstream contamination.

Do not add separate ad hoc rejection checks to every consumer if a shared upstream eligibility decision can safely close the defect.

The frame must fail closed.

## STOP Gate A

STOP if:

- the rejected frame cannot be excluded without changing medical activation rules for approved frames;
- the authority register is not available at the required pipeline stage;
- removal creates unexplained ranking or report regressions;
- a new clinical prioritisation rule would be required.

# Internal Workstream 2 — Legacy “methylation capacity” retirement

## Required behaviour

Remove all active production use of the rejected or unsupported concepts:

```text
methylation capacity
reduced B12-related methylation capacity
Methylation pathway pattern
```

where these originate from:

- `inv_homocysteine_high_metabolic`;
- legacy homocysteine elevation-context hypotheses;
- deprecated signal interpretation text;
- legacy narrative or clinician-summary fallback;
- Layer C fallback or display labels.

## Medical boundary

The ratified medical review permits:

- B-vitamin-associated hyperhomocysteinaemia when supported by relevant markers;
- renal-associated hyperhomocysteinaemia when supported by renal evidence.

It does not permit homocysteine to be described as a stand-alone measure of “methylation capacity”.

Replace or suppress legacy text only where necessary to implement the ratified medical decision.

Do not invent new medical prose.

Where wording is needed, source it from the Anthony-ratified medical review pack.

## Fingerprint closure

Build an executable fingerprint check covering:

```text
methylation capacity
reduced B12-related methylation capacity
Methylation pathway pattern
```

Search:

- active signal interpretations;
- top findings;
- consumer report;
- clinician report;
- intervention output;
- API DTOs;
- rendered frontend output;
- replay artefacts.

Any active match blocks PASS unless it is an explicitly historical/audit-only reference.

# Internal Workstream 3 — MCV frame co-service control

## Ratified rule

The general MCV anchor frame:

```text
signal_mcv_high::inv_mcv_high_macrocytosis
```

may provide morphology context, but must not generate duplicate causal WHY when either specific frame is selected:

```text
signal_mcv_high::inv_mcv_high_megaloblastic_macrocytosis
signal_mcv_high::inv_mcv_high_nonmegaloblastic_macrocytosis
```

## Required behaviour

Implement explicit governed co-service rules:

- the anchor may coexist as non-causal morphology context only;
- the anchor must not emit nutrient, hepatic, alcohol, thyroid, reticulocyte or marrow causal WHY;
- a specific MCV frame must suppress duplicate causal WHY from the anchor;
- megaloblastic and non-megaloblastic causal frames must not both serve unless an explicitly governed combined pattern exists;
- unsupported specific frames must remain inactive;
- the frontend must not reconstruct all three as parallel medical explanations.

## Required tests

At minimum prove:

1. anchor only → morphology context only;
2. megaloblastic supported → megaloblastic WHY, no anchor causal WHY, no non-megaloblastic WHY;
3. non-megaloblastic supported → non-megaloblastic WHY, no anchor causal WHY, no megaloblastic WHY;
4. ambiguous/insufficient support → safe anchor context or suppression, no speculative cause;
5. no duplicate consumer or clinician wording;
6. no duplicate intervention attribution.

## STOP Gate B

STOP if:

- the co-service rule requires a new medical policy beyond the ratified review;
- the specific-frame evidence gates are not available in Layer B;
- Layer C currently owns the only mechanism capable of suppressing duplicate explanations.

# Internal Workstream 4 — Layer C medical-boundary closure

## Boundary principle

Layer C may present, format and translate governed Layer B output.

Layer C must not:

- compare biomarkers against medical thresholds;
- activate or select signals;
- choose between activation frames;
- calculate medical confidence;
- rank findings;
- choose WHY hypotheses;
- determine intervention eligibility;
- substitute medical fallback text from raw biomarkers;
- reinterpret missing or ambiguous Layer B fields;
- combine sibling frames into a new medical story;
- alter consumer and clinician medical meaning.

## Required process

Use:

```text
docs/architecture/ARCH-CONV-FINAL_layer_c_boundary_and_leakage_inventory.md
```

as the authoritative defect list.

For every item classified `BOUNDARY_LEAK`:

- identify the Layer B authority that should supply the decision;
- remove or relocate the medical logic;
- make Layer C consume explicit DTO fields;
- preserve presentation-only behaviour;
- fail visibly and safely on missing governed medical fields;
- do not create a new frontend-side fallback.

For every item classified `UNRESOLVED`:

- resolve it as `PRESENTATION_ONLY`, `LEGITIMATE_TRANSLATION` or `BOUNDARY_LEAK`;
- no safety-material `UNRESOLVED` item may remain.

## DTO rule

DTO changes may be additive where needed to carry an already-governed Layer B decision.

Do not move new medical reasoning into DTO assembly merely to remove it from the frontend.

## Layer C failure behaviour

When required governed medical content is missing or contradictory:

- suppress the affected medical section or show a neutral technical fallback;
- do not infer an alternative interpretation;
- record the issue in diagnostics/audit evidence;
- do not display stale or sibling-frame content.

# End-to-end validation

## Mandatory replay of audited live case

Re-run or replay:

```text
analysis_id=e34aaedf-b09f-42f0-8cc8-4653a00b4c10
```

For every previously reported active leak, record:

```text
baseline finding
corrected API field
corrected rendered text
authority source
PASS / FAIL
```

Required result:

- rejected homocysteine metabolic frame absent from active results;
- absent from `top_findings`;
- absent from intervention references;
- no active “methylation capacity” wording;
- clinician summary contains only ratified B-vitamin wording;
- no consumer “Methylation pathway pattern”;
- MCV output follows the ratified co-service rule;
- no frontend medical-boundary logic changes the Layer B decision.

## Mandatory automated scenarios

Re-run all 13 scenarios from `ARCH-CONV-FINAL-AUDIT`.

Add focused regression scenarios for:

1. rejected frame attempts to fire;
2. rejected frame present in an upstream fixture but excluded before ranking;
3. intervention aggregation with rejected and approved sibling frames;
4. legacy homocysteine elevation-context hypothesis fingerprint;
5. MCV anchor + megaloblastic;
6. MCV anchor + non-megaloblastic;
7. ambiguous MCV evidence;
8. missing Layer B medical fields reaching Layer C;
9. stale cached DTO containing retired wording;
10. direct frontend component test proving no medical inference from raw biomarkers.

## Mandatory gates

Re-run:

- Package 1 identity gate and tests;
- Package 2 provenance/reachability gate and tests;
- Package 3 WHY authority gate and tests;
- final end-to-end leakage suite;
- architecture validation gate;
- NO-LLM suite;
- relevant frontend type, unit, integration and render tests.

Add one executable correction gate that fails if:

- any rejected activation key appears active downstream;
- any active fingerprint contains retired “methylation capacity” wording;
- MCV anchor causal WHY co-serves with a specific MCV frame;
- any identified Layer C boundary leak remains;
- any safety-material Layer C item remains unresolved.

# Scope discipline

This package is bounded to the defects identified by the final audit.

Do not:

- reopen the medical decisions from Package 3;
- expand the ten-frame WHY pilot;
- migrate the wider legacy WHY estate;
- change signal thresholds;
- invent new medical hypotheses;
- wire PSI;
- enable Gemini;
- redesign unrelated frontend areas;
- perform general prose-library work;
- declare controlled-beta readiness.

A new work package is permitted only if a STOP condition proves that an unrelated architecture domain or new medical policy is required.

# Required deliverables

Create:

```text
docs/architecture/ARCH-CONV-CORRECT-1_rejected_frame_inactivation_design.md
docs/architecture/ARCH-CONV-CORRECT-1_mcv_co_service_design.md
docs/architecture/ARCH-CONV-CORRECT-1_layer_c_boundary_closure_report.md
docs/architecture/ARCH-CONV-CORRECT-1_end_to_end_leakage_correction_report.md
docs/audit-papers/ARCH-CONV-CORRECT-1_implementation_and_verification_report.md
```

Update:

```text
docs/testing/ARCH-CONV-FINAL_frontend_end_to_end_uat.md
docs/architecture/ARCH-CONV-FINAL_end_to_end_pipeline_and_leakage_report.md
docs/architecture/ARCH-CONV-FINAL_layer_c_boundary_and_leakage_inventory.md
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

Record:

- each active leak before and after;
- exact runtime surfaces changed;
- Layer C boundary items closed;
- MCV co-service results;
- fingerprint results;
- live analysis replay result;
- test and gate evidence;
- unresolved limitations;
- no beta-readiness claim.

# Acceptance criteria

- [ ] Rejected homocysteine metabolic frame is inactive end to end.
- [ ] Rejected frame cannot appear in top findings.
- [ ] Rejected frame cannot contribute to interventions.
- [ ] Rejected frame cannot contribute interpretation or summary text.
- [ ] No active “methylation capacity” legacy wording remains.
- [ ] B-vitamin and renal homocysteine frames remain correctly differentiated.
- [ ] MCV anchor cannot co-emit duplicate causal WHY with a specific MCV frame.
- [ ] Megaloblastic and non-megaloblastic WHY do not co-serve without explicit authority.
- [ ] Every final-audit Layer C `BOUNDARY_LEAK` is closed.
- [ ] No safety-material `UNRESOLVED` Layer C item remains.
- [ ] Layer C performs presentation/translation only.
- [ ] Missing governed medical fields fail safely without medical fallback.
- [ ] Live analysis `e34aaedf-b09f-42f0-8cc8-4653a00b4c10` passes all corrected leakage checks.
- [ ] All 13 original end-to-end scenarios pass.
- [ ] New focused correction scenarios pass.
- [ ] Package 1–3 protections remain intact.
- [ ] No unrelated medical or architecture scope entered.
- [ ] No controlled-beta readiness claim made.

# STOP conditions

STOP if:

1. rejected-frame inactivation requires changing approved medical activation rules;
2. legacy wording cannot be removed without reopening ratified medical content;
3. MCV co-service requires a new medical policy;
4. Layer C boundary closure requires redesign of an unrelated domain;
5. package scope grows by more than 25% without human reauthorisation;
6. more than one unplanned mandatory follow-on package is identified;
7. corrected live output shows unexplained clinical drift;
8. any Package 1–3 safety gate regresses;
9. a required correction would weaken provenance, identity, authority or ratification controls;
10. substantive correction cannot be completed in this outcome-based package.

# Final package recommendation

Recommend exactly one:

```text
GO
CORRECT
STOP
V6
```

Definitions:

- `GO`: all identified final-audit corrections are closed; resume `ARCH-CONV-FINAL-AUDIT`.
- `CORRECT`: one bounded defect remains within this package.
- `STOP`: correction requires programme redesign.
- `V6`: ratified kill criteria are met; freeze v5 architecture work.

# Verification report

Include:

- baseline and final SHA;
- branch;
- files changed;
- per-defect before/after evidence;
- rejected-frame lifecycle trace;
- legacy fingerprint results;
- MCV co-service matrix;
- Layer C boundary closure matrix;
- live analysis replay evidence;
- automated scenario results;
- test commands and exit codes;
- validation-gate evidence;
- acceptance-criteria table;
- STOP-condition assessment;
- final `GO / CORRECT / STOP / V6` recommendation;
- remaining obligations outside this package.

Do not merge without explicit human authority.
