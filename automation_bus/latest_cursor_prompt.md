---
work_id: ARCH-CONV-FINAL-AUDIT
branch: audit/arch-conv-final-programme
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: CONTENT
stage_b_mode: MODE_2
runtime_change: NONE
---

# ARCH-CONV-FINAL-AUDIT — Final Independent v5 Convergence and End-to-End Leakage Audit

## Purpose

Issue the final programme-level decision on the completed v5 architecture convergence series:

```text
ARCH-CONV-PKG1 — activation-frame identity closure
ARCH-CONV-PKG2 — provenance and runtime-reachability closure
ARCH-CONV-PKG3 — WHY authority migration and pilot promotion
```

The audit must determine whether the full convergence attempt has genuinely closed the Gate 0 obligations without leaving incorrect, blocked, rejected, retired, deprecated or legacy medical logic capable of reaching Layer C or the final user experience.

This is an independent audit package.

Do not implement substantive corrections inside this audit. Any correction must be recommended as `CORRECT`, `STOP` or `V6`.

Standard Automation Bus governance applies.

## Independence requirement

Do not rely on implementation reports or prior PASS decisions as proof.

Re-execute material tests, inspect live code and runtime behaviour, and independently verify final end-to-end outputs.

Use independent review agents where useful, with disjoint scopes covering:

1. Package 1 identity closure;
2. Package 2 provenance/reachability closure;
3. Package 3 WHY authority and medical-content fidelity;
4. Layer B-to-Layer C end-to-end leakage;
5. frontend boundary ownership and human UAT evidence.

## Required programme inputs

Read the current merged versions of:

```text
docs/planning-papers/HEALTHIQ_AI_V5_FINAL_ARCHITECTURE_CONVERGENCE_AND_SALVAGE_OR_REBUILD_PLAN.md
docs/architecture/HEALTHIQ_AI_V5_CONTROLLED_BETA_ARCHITECTURE_COHORT.md
docs/architecture/HEALTHIQ_AI_V5_CONVERGENCE_VIABILITY_ASSESSMENT.md
docs/architecture/HEALTHIQ_AI_V5_WHY_MIGRATION_PILOT_COHORT.md
docs/architecture/HEALTHIQ_AI_V5_WHY_PILOT_MEDICAL_REVIEW_READINESS.md

docs/architecture/ARCH-CONV-PKG1_frame_identity_surface_design.md
docs/audit-papers/ARCH-CONV-PKG1_implementation_and_verification_report.md

docs/architecture/ARCH-CONV-PKG2_launch_critical_provenance_decision_inventory.md
docs/architecture/ARCH-CONV-PKG2_runtime_suppression_impact_report.md
docs/audit-papers/ARCH-CONV-PKG2_implementation_and_verification_report.md

docs/architecture/ARCH-CONV-PKG3_pilot_evidence_and_identity_inventory.md
docs/architecture/ARCH-CONV-PKG3_compiled_why_authority_design.md
docs/architecture/ARCH-CONV-PKG3_legacy_retirement_and_authority_register.md
docs/architecture/ARCH-CONV-PKG3_output_parity_and_change_report.md
docs/Medical Research Documents/HEALTHIQ_AI_V5_WHY_PILOT_MEDICAL_REVIEW_GPT_REVIEWED_ANTHONY_RATIFIED.md
docs/audit-papers/ARCH-CONV-PKG3_implementation_and_verification_report.md

docs/architecture/ADR-RT-IDENTITY-PROV-001_activation_frame_and_provenance_integrity.md
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

Resolve actual repository paths where names differ.

Inspect current merged production code, tests, manifests, authority registers, DTOs, API responses and frontend rendering paths.

## Audit question

Answer:

> Does the complete HealthIQ AI pipeline prove that Layer C receives only current, provenance-valid, activation-frame-correct and medically ratified Layer B output, and that no incorrect, blocked, rejected, retired, deprecated or legacy medical logic survives into the final user experience?

A final PASS is forbidden unless this is proven through code inspection, automated execution and human frontend UAT.

# Workstream 1 — Package 1 identity closure

Independently verify the five launch-path surfaces:

```text
interpretation_display_layer_publish_v1.py
domain_score_assembler.py
narrative_report_compiler_v1.py
intervention_selector_v1.py
signal_interaction_builder.py
```

Confirm:

- distinct activation frames do not collapse accidentally;
- intentional family-level aggregation remains explicit and auditable;
- activation keys survive ranking, grouping, narrative selection and reporting;
- interventions cannot be borrowed from sibling frames;
- interaction participation is frame-auditable;
- ambiguous identity fails safely;
- single-frame compatibility remains intact.

Re-run the Package 1 pressure-set tests and validation gate.

# Workstream 2 — Package 2 provenance and reachability

Independently verify:

- every production-reachable launch-critical package has explicit lineage;
- blocked or beta-ineligible packages do not enter the production registry;
- excluded packages cannot fire, rank, reach reports or appear as active replay results;
- test-only opt-in remains explicit and closed by default;
- unknown or contradictory eligibility fails closed;
- non-cohort package generations are not unintentionally affected.

Re-run the Package 2 tests and reachability gate.

# Workstream 3 — Package 3 WHY authority and medical fidelity

Independently verify all ten pilot frames against the ratified medical-review pack.

Confirm:

- exactly nine frames are `COMPILED_ACTIVE`;
- the rejected broad homocysteine metabolic frame remains inactive;
- no compiled artefact exists for the rejected frame;
- no rejected, deferred or unratified frame can generate WHY;
- each compiled artefact faithfully implements its ratified hypotheses, caveats and audience boundaries;
- no frame has simultaneous legacy and compiled runtime authority;
- retired legacy content remains historically preserved but non-reachable for the migrated frame;
- missing compiled authority cannot silently fall back to retired legacy YAML;
- activation key and source specification survive runtime and replay.

Live-execute the rejected frame and prove it produces no WHY output.

Re-run Package 3 tests and the compiled WHY authority gate.

# Workstream 4 — End-to-end pipeline and Layer C leakage

## Pipeline boundary under test

Run controlled cases through:

```text
Layer A ingestion and canonical facts
→ Layer B signal activation
→ activation-frame selection
→ provenance and runtime eligibility
→ WHY authority selection
→ ranking and report compilation
→ API / DTO payload
→ Layer C presentation
→ final rendered consumer and clinician output
```

The audit must test both:

### A. Medical logic implemented in Layer C

Layer C must not independently:

- compare raw biomarkers against medical thresholds;
- activate or select signals;
- choose between activation frames;
- rank medical findings;
- calculate clinical confidence;
- select WHY hypotheses;
- determine intervention eligibility;
- reconstruct root-cause logic;
- substitute fallback medical prose based on raw values;
- alter consumer or clinician medical meaning.

### B. Incorrect or legacy medical logic leaking through to Layer C

Final API payloads and rendered outputs must not contain:

- rejected frames;
- provenance-blocked signals;
- retired legacy WHY hypotheses;
- deprecated package-generation logic;
- obsolete boilerplate;
- sibling-frame hypotheses;
- unsupported causal explanations;
- stale ranking or confidence decisions;
- simultaneous legacy and compiled explanations;
- fallback content bypassing current authority registers;
- stale medical content retained in caches, DTOs or report assembly.

## Required automated end-to-end scenarios

Run at least:

1. **Rejected broad homocysteine frame**
   - no WHY from `signal_homocysteine_high::inv_homocysteine_high_metabolic`;
   - no shared-legacy fallback;
   - no generic “methylation capacity” explanation.

2. **B-vitamin homocysteine frame**
   - only ratified B-vitamin hypotheses;
   - no renal hypothesis without renal evidence;
   - no broad metabolic frame;
   - no assertion of proven vitamin deficiency.

3. **Renal homocysteine frame**
   - renal WHY only with renal evidence;
   - no CKD diagnosis from one result;
   - no B-vitamin cause without supporting vitamin evidence.

4. **General MCV anchor**
   - morphology context only;
   - no unearned nutrient, hepatic, alcohol, thyroid or marrow cause;
   - no duplicate WHY if a specific MCV frame is selected.

5. **Megaloblastic MCV frame**
   - B12/folate interpretation only with supporting evidence;
   - no unsupported hepatic or alcohol explanation.

6. **Non-megaloblastic MCV frame**
   - only evidence-supported differential contexts;
   - no inferred alcohol use from MCV or GGT alone;
   - no consumer-facing marrow diagnosis.

7. **Low free T3 illness context**
   - contextual low-T3 wording only with supporting thyroid-panel and illness context;
   - no automatic hypothyroidism diagnosis;
   - no treatment recommendation.

8. **TPO antibodies with hypothyroid physiology**
   - autoimmune contribution tied to the actual TSH/FT4 pattern;
   - overt and subclinical patterns remain distinct;
   - no claim that antibodies alone prove current hypothyroidism.

9. **Euthyroid TPO antibody context**
   - current thyroid function described as preserved;
   - future-risk context only;
   - no present hypothyroidism claim;
   - no personalised progression probability.

10. **Provenance-blocked package**
    - no signal, ranking, WHY, intervention or prose reaches Layer C.

11. **Retired legacy WHY asset**
    - no retired hypothesis ID or distinctive phrase appears in API payloads or rendered reports;
    - no fallback reactivates it.

12. **Invalid or ambiguous activation frame**
    - fail-safe or suppressed output;
    - no sibling-frame substitution;
    - no legacy fallback;
    - no interpretation invented in Layer C.

13. **Normal/single-frame compatibility**
    - legitimate single-frame output remains stable.

## Required assertions

For every automated case capture:

```text
input facts
questionnaire context
activated signal_id
selected activation_key
source_spec_id
runtime eligibility decision
WHY authority state
hypothesis IDs selected
ranking result
consumer DTO
clinician DTO
rendered consumer text
rendered clinician text
replay/audit record
expected result
actual result
PASS / FAIL
```

# Workstream 5 — Legacy fingerprint and stale-content scan

Build a bounded fingerprint set from:

- retired pilot legacy YAML;
- rejected homocysteine metabolic wording;
- blocked package hypothesis IDs;
- deprecated package-generation identifiers;
- old root-cause fallback strings;
- known obsolete boilerplate;
- legacy hypothesis IDs belonging to sibling frames.

Search:

```text
production API payloads
consumer report output
clinician report output
frontend-rendered text
replay artefacts
cached fixtures used by the tested route
```

Classify every match:

```text
EXPECTED_HISTORICAL_REFERENCE
TEST_FIXTURE_ONLY
ACTIVE_LEAK
FALSE_POSITIVE
UNRESOLVED
```

Any `ACTIVE_LEAK` blocks PASS.

# Workstream 6 — Frontend boundary scan

Inspect frontend and Layer C translation paths for medical logic.

For each potentially medical branch record:

```text
file
function/component
input
logic performed
output
classification
required action
```

Allowed classifications:

```text
PRESENTATION_ONLY
LEGITIMATE_TRANSLATION
BOUNDARY_LEAK
UNRESOLVED
```

Legitimate Layer C activity may include:

- formatting;
- rendering order already decided by Layer B;
- plain-language translation within supplied boundaries;
- visibility/layout decisions that do not alter medical meaning;
- rendering provenance and evidence metadata.

Any `BOUNDARY_LEAK` or safety-material `UNRESOLVED` item blocks PASS.

Create:

```text
docs/architecture/ARCH-CONV-FINAL_layer_c_boundary_and_leakage_inventory.md
```

# Mandatory Human UAT Gate

Automated evidence is necessary but insufficient.

Anthony must run fresh cases through the real application from blood-panel and lifestyle-questionnaire entry to final results.

## Minimum human UAT cases

Run at least:

1. **Normal or mostly normal panel**
   - verifies baseline usability and absence of false WHY content.

2. **Pilot multi-frame panel**
   - deliberately exercises at least one of:
     - B-vitamin homocysteine;
     - renal homocysteine;
     - megaloblastic MCV;
     - non-megaloblastic MCV;
     - euthyroid TPO;
     - TPO with hypothyroid physiology;
     - contextual low FT3.

3. **Negative leakage panel**
   - proves a cause does not appear when supporting evidence is absent;
   - for example renal homocysteine without renal impairment, or megaloblastic MCV without B12/folate support.

Where technically possible, include a case confirming that the rejected homocysteine metabolic frame does not surface.

## UAT evidence to preserve

For each case preserve:

```text
case ID
date/time
environment and commit SHA
exact blood inputs
units and reference ranges
lifestyle answers
screenshots of input completion
screenshots of results pages
consumer report/export
clinician report/export
API payload or replay artefact
Anthony observations
PASS / FAIL
```

## Anthony’s UAT questions

For each case answer:

- Does the displayed interpretation make medical and business sense?
- Does the displayed WHY match the actual input pattern?
- Is any cause asserted without supporting evidence?
- Is any wording visibly old, duplicated, contradictory or out of context?
- Is rejected, blocked or retired content visible?
- Do consumer and clinician views tell the same underlying medical story?
- Is the correct activation frame traceable?
- Does the result appear to have been inferred or altered in Layer C?
- Is anything surprising enough to require medical or architecture review?

Create:

```text
docs/uat/ARCH-CONV-FINAL_frontend_end_to_end_uat.md
```

Use the actual repository UAT folder convention if different.

## Mandatory STOP — Await human UAT

Complete the automated and code-based audit first, then STOP and hand the UAT plan to Anthony.

Do not issue final PASS before Anthony supplies completed UAT evidence.

After Anthony’s evidence is added, resume the same audit work ID and complete the programme decision.

# Programme kill-criteria review

Explicitly assess:

- whether more than one unplanned mandatory architecture package is now required;
- whether any package exceeded the ratified 25% scope-growth ceiling without authorisation;
- whether unresolved medical-review throughput undermines convergence;
- whether overlapping authority remains;
- whether provenance and runtime reachability disagree;
- whether Layer C boundary leakage remains;
- whether the end-to-end pipeline produces clinically unexplained output;
- whether any correction would reopen a supposedly closed architecture domain.

# Required outputs

Create:

```text
docs/architecture/ARCH-CONV-FINAL_programme_obligation_closure_matrix.md
docs/architecture/ARCH-CONV-FINAL_end_to_end_pipeline_and_leakage_report.md
docs/architecture/ARCH-CONV-FINAL_layer_c_boundary_and_leakage_inventory.md
docs/uat/ARCH-CONV-FINAL_frontend_end_to_end_uat.md
docs/audit-papers/ARCH-CONV-FINAL-AUDIT_implementation_and_verification_report.md
```

Update:

```text
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

Record:

- package-level obligation result;
- automated end-to-end scenarios;
- leakage findings;
- frontend-boundary findings;
- human UAT results;
- kill-criteria result;
- final programme decision;
- explicit statement that controlled-beta readiness was or was not assessed.

# Acceptance criteria

- [ ] Package 1 identity closure independently reverified.
- [ ] Package 2 provenance/reachability closure independently reverified.
- [ ] Package 3 WHY authority and ratified content independently reverified.
- [ ] Rejected homocysteine frame live-executed and proven inert.
- [ ] All required automated end-to-end scenarios executed.
- [ ] Final consumer and clinician payloads inspected.
- [ ] Final rendered frontend outputs inspected.
- [ ] Legacy fingerprint scan completed.
- [ ] No blocked, rejected, retired or sibling-frame logic reaches Layer C.
- [ ] Frontend boundary scan completed.
- [ ] No medical decision logic remains in Layer C.
- [ ] Invalid or ambiguous payloads fail safely.
- [ ] Replay and rendering are deterministic.
- [ ] Anthony completed required fresh frontend UAT.
- [ ] UAT evidence is preserved.
- [ ] No unexplained medical or presentation drift remains.
- [ ] Programme kill criteria assessed.
- [ ] Final decision issued.
- [ ] No beta-readiness claim is made unless separately and explicitly assessed.

# Final programme decision

Issue exactly one:

```text
PASS
CORRECT
STOP
V6
```

Definitions:

- `PASS`: retain v5 and formally close the architecture convergence programme.
- `CORRECT`: one bounded correction is required before closure.
- `STOP`: convergence remains incomplete or unstable and requires redesign.
- `V6`: ratified kill criteria are met; freeze v5 architecture work and begin controlled v6 migration.

A `PASS` is forbidden if:

- Anthony has not completed UAT;
- any required test is missing;
- any active legacy or incorrect logic reaches Layer C;
- any Layer C medical-decision boundary leak remains;
- any rejected or blocked frame reaches user-facing output;
- any unexplained consumer/clinician inconsistency remains;
- any safety-material item is `UNRESOLVED`.

# Verification report

Include:

- baseline and final SHA;
- branch;
- auditors and independence model;
- evidence read;
- code and boundary surfaces inspected;
- independently re-run commands and exit codes;
- end-to-end scenario table;
- API and rendered-output findings;
- legacy fingerprint results;
- Layer C boundary classification;
- Anthony UAT evidence and decision;
- package obligation closure matrix;
- kill-criteria assessment;
- final PASS / CORRECT / STOP / V6 decision;
- remaining obligations outside this programme.

Do not merge without explicit human authority.
