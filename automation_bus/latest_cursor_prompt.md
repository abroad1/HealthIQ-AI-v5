---
work_id: BATCH2-FULL-COVERAGE-ACTIVATION-1_activate_research_supported_thyroid_and_androgen_signals
branch: work/BATCH2-FULL-COVERAGE-ACTIVATION-1-activate-research-supported-thyroid-and-androgen-signals
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
---

# BATCH2-FULL-COVERAGE-ACTIVATION-1 — Activate Research-Supported Thyroid and Androgen Signals

## Purpose

Activate only the Batch 2 thyroid and androgen signals that are now supported by medical research authority and reusable runtime context gates.

This is an activation sprint, not another classification or readiness sprint.

The sprint must activate the research-supported signals with strict deterministic gates, while keeping weak, ambiguous or insufficiently supported signals inactive as primary runtime signals.

---

## Strategic context

Previous work established:

```text
- ARCH-COMPLETION-1 corrected orchestrator phase order.
- AnalysisContext now precedes signal evaluation.
- Runtime context is derived from AnalysisContext / governed post-context objects.
- BATCH2-MINIMUM-COVERAGE-1 formally classified the unresolved Batch 2 estate.
- BATCH2-FULL-COVERAGE-BUILD-1 added reusable runtime context primitives.
- answered_yes / answered_no / not_answered semantics now exist.
- disclosure state is separated from positive exposure.
- medical research authority has now been produced for FT3 low and 8 androgen patterns.
```

The medical research review supports activation-with-gates for:

```text
- FT3 low
- Free Androgen Index high, female-only initially
- Free testosterone high, sex-specific and assay-gated
- Free testosterone low, adult male-only and symptom-gated
```

The medical research review does not support activation as primary signals for:

```text
- DHEA high, unless DHEA-S identity is explicitly resolved and separately approved
- DHEA low
- Free Androgen Index low
- Free testosterone percentage high
- Free testosterone percentage low
```

The goal is to move from activation readiness to safe deterministic runtime activation.

---

## Governance classification

This sprint is classified as:

```yaml
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
```

Rationale:

```text
- inactive clinical signal packages may become active
- endocrine interpretation logic is clinically sensitive
- package activation state will change
- runtime context gates will be bound to clinical packages
- safe wording and fail-closed behaviour must be enforced
```

Required route:

```text
Cursor implementation
Claude hardening / audit
GPT architectural review
Human approval before merge
```

Do not merge without explicit human approval.

---

## Required branch

Work only on:

```text
work/BATCH2-FULL-COVERAGE-ACTIVATION-1-activate-research-supported-thyroid-and-androgen-signals
```

Do not work on `main`.

Do not merge.

---

## Required medical research authority

Before implementation, verify that the Batch 2 medical research review is present in the repository.

Preferred path:

```text
"C:\Users\abroa\HealthIQ-AI-v5\docs\Medical Research Documents\Batch_2_Thyroid_Androgen_Context_Authority_Review.md"
```

If the file is not present, STOP and ask the human owner to place the medical research review into the repository.

Do not reconstruct the research review from memory.

Do not activate any package without a repo-persisted medical research authority artefact.

The research authority must contain pattern-by-pattern recommendations for:

```text
- FT3 low
- DHEA high
- DHEA low
- FAI high
- FAI low
- free testosterone high
- free testosterone low
- free testosterone percentage high
- free testosterone percentage low
```

---

## Non-negotiable constraints

This sprint must not:

```text
- activate unsupported signals
- activate DHEA high unless DHEA-S identity and separate approval are explicitly resolved
- activate DHEA low
- activate FAI low
- activate free testosterone percentage high as a primary signal
- activate free testosterone percentage low as a primary signal
- diagnose thyroid disease
- diagnose PCOS
- diagnose hypogonadism
- diagnose adrenal disease
- recommend treatment
- recommend supplements or hormones
- change biomarker reference range policy
- substitute global/default reference ranges where lab ranges are available
- change SSOT unless a STOP gate proves canonical identity remediation is unavoidable
- change frontend result rendering
- introduce frontend medical inference
- introduce fallback or dummy parsers
- introduce raw Pass 3 / investigation-spec runtime reads
- introduce LLM clinical reasoning into runtime signal evaluation
```

Activation must remain deterministic.

All new active signals must fail closed when required biomarker or context gates are missing.

---

## Allowed activation targets

Only the following packages may be activated in this sprint:

```text
knowledge_bus/packages/pkg_kb47_free_t3_low_low_t3_syndrome/
knowledge_bus/packages/pkg_kb47_fai_high_biochemical_hyperandrogenism/
knowledge_bus/packages/pkg_kb47_free_testosterone_high_androgen_excess_context/
knowledge_bus/packages/pkg_kb47_free_testosterone_low_androgen_deficiency_context/
```

All other Batch 2 androgen packages must remain inactive unless explicitly STOP-gated for metadata-only remediation.

---

## Required inactive primary signals

The following packages must remain inactive as primary signals:

```text
knowledge_bus/packages/pkg_kb47_dhea_high_androgen_excess_context/
knowledge_bus/packages/pkg_kb47_dhea_low_adrenal_androgen_reduction/
knowledge_bus/packages/pkg_kb47_fai_low_reduced_free_androgen_availability/
knowledge_bus/packages/pkg_kb47_free_testosterone_pct_high_elevated_free_androgen_fraction/
knowledge_bus/packages/pkg_kb47_free_testosterone_pct_low_reduced_free_androgen_fraction/
```

The percentage and low-FAI packages may be documented as future optional modifiers only if an existing safe modifier architecture already supports this.

Do not invent a new modifier architecture in this sprint.

---

## Authoritative inputs

Read before implementation:

```text
docs/audit-papers/ARCH-COMPLETION-1_final_runtime_context_and_orchestrator_restructure.md
docs/audit-papers/BATCH2-MINIMUM-COVERAGE-1_androgen_ft3_low_clinical_and_runtime_completion.md
docs/audit-papers/BATCH2-FULL-COVERAGE-BUILD-1_reusable_context_layer_research_authority_and_activation_readiness.md
docs/audit-papers/BATCH2-CONTEXT-COMPLETION-1_runtime_semantics_and_stop_gated_activation.md
docs/audit-papers/CONTEXT-CLEARANCE-1_context_semantics_and_batch2_clearance.md
docs/audit-papers/DAY-ONE-ARCHITECTURE-CLOSURE-REVIEW.md
docs/sprints/launch_core_carry_forward_register.md

knowledge_bus/research/medical_reviews/batch2_thyroid_androgen_context_authority_review_v1.md

knowledge_bus/governance/reusable_runtime_context_primitive_model_v1.yaml
knowledge_bus/governance/context_questionnaire_contract_v1.yaml
knowledge_bus/governance/batch2_full_coverage_activation_readiness_register_v1.yaml
knowledge_bus/governance/batch2_medical_research_intake_contract_v1.yaml
knowledge_bus/governance/batch2_minimum_coverage_decision_register_v1.yaml
knowledge_bus/governance/batch2_context_clearance_register_v1.yaml
knowledge_bus/governance/context_runtime_execution_register_v1.yaml
knowledge_bus/governance/runtime_context_requirements_model_v1.yaml
knowledge_bus/governance/runtime_context_semantics_model_v1.yaml
knowledge_bus/governance/batch2_remaining_blockers_execution_register_v1.yaml
knowledge_bus/governance/batch2_androgen_panel_medical_review_v1.yaml
knowledge_bus/governance/batch2_androgen_context_modifier_binding_v1.yaml
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
```

Inspect:

```text
backend/core/pipeline/orchestrator.py
backend/core/analytics/runtime_context_evaluator.py
backend/core/analytics/signal_evaluator.py
backend/tests/regression/test_runtime_context_evaluation.py
backend/tests/regression/test_context_threading.py
```

Inspect all 9 package directories:

```text
knowledge_bus/packages/pkg_kb47_dhea_high_androgen_excess_context/
knowledge_bus/packages/pkg_kb47_dhea_low_adrenal_androgen_reduction/
knowledge_bus/packages/pkg_kb47_fai_high_biochemical_hyperandrogenism/
knowledge_bus/packages/pkg_kb47_fai_low_reduced_free_androgen_availability/
knowledge_bus/packages/pkg_kb47_free_testosterone_high_androgen_excess_context/
knowledge_bus/packages/pkg_kb47_free_testosterone_low_androgen_deficiency_context/
knowledge_bus/packages/pkg_kb47_free_testosterone_pct_high_elevated_free_androgen_fraction/
knowledge_bus/packages/pkg_kb47_free_testosterone_pct_low_reduced_free_androgen_fraction/
knowledge_bus/packages/pkg_kb47_free_t3_low_low_t3_syndrome/
```

If any expected authority file is missing, report whether it blocks the sprint.

---

## Authority preflight

Before editing, verify and report:

```powershell
git branch --show-current
git status --short
git rev-parse HEAD
git log --oneline -n 10
```

Confirm:

```text
1. Current branch matches this work package branch.
2. Working tree is clean.
3. ARCH-COMPLETION-1 is merged.
4. BATCH2-MINIMUM-COVERAGE-1 is merged.
5. BATCH2-FULL-COVERAGE-BUILD-1 is merged.
6. Batch 2 medical research review is present in the repository.
7. `AnalysisContext` precedes signal evaluation.
8. Runtime context is derived from `AnalysisContext` or governed post-context object.
9. answered_yes / answered_no / not_answered semantics exist.
10. Disclosure state and positive exposure are separate.
11. All 9 target packages are currently inactive.
12. No unauthorised activation already exists.
13. Repository secret-file gate failure remains remediated.
```

STOP if the baseline is unclear.

---

# Phase 1 — Research-to-runtime activation mapping

Create a read-only activation mapping table before making changes.

For each of the 9 packages, document:

```text
- package path
- current activation state
- research verdict
- allowed activation outcome
- required biomarker gates
- required context gates
- required exclusion gates
- required wording boundaries
- whether this sprint may activate it
- reason
```

Allowed activation outcome values:

```text
ACTIVATE_WITH_GATES_THIS_SPRINT
KEEP_INACTIVE_PRIMARY_SIGNAL
KEEP_INACTIVE_PENDING_DHEA_DHEAS_IDENTITY_REMEDIATION
KEEP_INACTIVE_PENDING_EXTERNAL_CLINICIAN_SIGNOFF
KEEP_INACTIVE_MODIFIER_ONLY_FUTURE
DO_NOT_ACTIVATE
```

STOP if any package outcome conflicts with the medical research authority.

---

# Phase 2 — DHEA / DHEA-S identity STOP gate

Before activating or remediating anything related to DHEA, perform a DHEA identity gate.

For:

```text
knowledge_bus/packages/pkg_kb47_dhea_high_androgen_excess_context/
knowledge_bus/packages/pkg_kb47_dhea_low_adrenal_androgen_reduction/
```

Determine:

```text
- Is the source marker DHEA or DHEA-S?
- Does the canonical biomarker identity distinguish DHEA from DHEA-S?
- Does the package title, manifest, signal library and frame identity align?
- Does the medical research authority support the exact marker identity?
```

Rules:

```text
If marker identity is DHEA or ambiguous:
  - do not activate DHEA high
  - do not activate DHEA low
  - document required canonical marker remediation
  - keep both packages inactive

If marker identity is explicitly DHEA-S:
  - do not activate in this sprint unless exact human approval phrase is present
  - document future activation prerequisites for DHEA-S high
  - keep DHEA-S low inactive unless separate clinician authority exists

Required approval phrase for DHEA-S activation:
  APPROVE DHEA-S ACTIVATION IN BATCH2-FULL-COVERAGE-ACTIVATION-1
```

If that exact phrase is absent, no DHEA/DHEA-S package may activate.

Expected default outcome:

```text
DHEA high remains inactive.
DHEA low remains inactive.
```

---

# Phase 3 — FT3 low activation design

Prepare FT3 low activation with strict gates.

Target package:

```text
knowledge_bus/packages/pkg_kb47_free_t3_low_low_t3_syndrome/
```

Activation is permitted only if all of the following can be encoded deterministically.

Required biomarker gates:

```text
- FT3 low relative to lab-provided reference range
- TSH present
- FT4 present
```

Required context gates:

```text
- thyroid medication status answered
- recent acute illness / infection / recovery status answered
- energy availability context answered
- calorie restriction / fasting / under-eating / significant weight loss context answered or represented through the energy availability primitive
- pregnancy/postpartum status answered where applicable
- medication/biotin disclosure captured where available
```

Required exclusion/fail-closed gates:

```text
- fail closed if TSH missing
- fail closed if FT4 missing
- fail closed if thyroid medication question not_answered
- fail closed if illness/recovery context not_answered
- fail closed if energy availability context not_answered
- fail closed if pregnancy/postpartum is answered_yes and pregnancy-specific logic is unavailable
- fail closed or divert if the pattern suggests overt thyroid dysfunction requiring clinician interpretation rather than low-T3 educational wording
```

Required wording boundary:

```text
May say:
  "This pattern may be consistent with reduced peripheral T3 availability, which can sometimes be seen during illness, recovery, calorie restriction or low energy availability."

Must not say:
  "You have low T3 syndrome."
  "You have hypothyroidism."
  "Your thyroid is underactive."
  "You need thyroid hormone."
```

Maximum claim strength:

```text
may be consistent with
```

---

# Phase 4 — FAI high activation design

Prepare FAI high activation with female-only initial scope.

Target package:

```text
knowledge_bus/packages/pkg_kb47_fai_high_biochemical_hyperandrogenism/
```

Activation is permitted only if all of the following can be encoded deterministically.

Required biomarker gates:

```text
- FAI high relative to lab-provided sex-specific reference range
- total testosterone present
- SHBG present
```

Required demographic/context gates:

```text
- biological sex present
- biological sex = female for initial activation
- age present
- menstrual / menopause status answered where applicable
- pregnancy status answered where applicable
- hormone therapy / HRT / oral contraceptive context answered
- testosterone therapy / AAS exposure context answered
- DHEA supplementation context answered
- fertility treatment context answered where available
- androgen excess symptom disclosure captured
```

Required exclusion/fail-closed gates:

```text
- fail closed if biological sex missing
- fail closed if age missing
- fail closed if total testosterone missing
- fail closed if SHBG missing
- fail closed if biological sex is male
- fail closed if testosterone therapy or AAS exposure is answered_yes for endogenous interpretation
- fail closed or suppress endogenous interpretation if DHEA supplementation is answered_yes
- fail closed if pregnancy is answered_yes and pregnancy-specific logic is unavailable
- use clinician-review escalation wording, not routine wording, if severe or rapid-onset virilisation is disclosed
```

Required wording boundary:

```text
May say:
  "This pattern may be consistent with biochemical hyperandrogenism, especially when interpreted in a female patient alongside symptoms, menstrual status and companion androgens."
  "FAI is calculated from testosterone and SHBG, so a high result can reflect high testosterone, low SHBG, or both."

Must not say:
  "You have PCOS."
  "You have an androgen disorder."
  "You have an adrenal or ovarian tumour."
  "This proves excess testosterone."
```

Maximum claim strength:

```text
may be consistent with
```

---

# Phase 5 — Free testosterone high activation design

Prepare free testosterone high activation with sex-specific and assay/method gates.

Target package:

```text
knowledge_bus/packages/pkg_kb47_free_testosterone_high_androgen_excess_context/
```

Activation is permitted only if deterministic gates can safely distinguish endogenous interpretation from therapy/supplement exposure.

Required biomarker gates:

```text
- free testosterone high relative to lab-provided sex-specific reference range
- total testosterone present
- SHBG present
- albumin present if calculated free testosterone is used
```

Required method gate:

```text
- method flag captured where available
- calculated free testosterone or equilibrium dialysis is preferred
- direct analogue free testosterone requires caution wording or fail-closed if method cannot be represented safely
```

Required demographic/context gates:

```text
- biological sex present
- age present
- hormone therapy context answered
- testosterone therapy context answered
- AAS exposure context answered
- DHEA supplementation context answered
- oral contraceptive context answered where applicable
- pregnancy status answered where applicable
- androgen excess symptom disclosure captured
```

Required exclusion/fail-closed gates:

```text
- fail closed if biological sex missing
- fail closed if age missing
- fail closed if total testosterone missing
- fail closed if SHBG missing
- fail closed if assay/method requirements cannot be represented safely
- do not emit endogenous excess interpretation if testosterone therapy or AAS exposure is answered_yes
- suppress or caveat endogenous interpretation if DHEA supplementation is answered_yes
- fail closed if pregnancy is answered_yes and pregnancy-specific logic is unavailable
- use clinician-review escalation wording, not routine wording, if severe or rapid-onset virilisation is disclosed
```

Required wording boundary:

```text
May say:
  "This pattern may be consistent with increased free androgen exposure, but it is not diagnostic on its own."
  "Interpretation depends on sex, age, total testosterone, SHBG, albumin, symptoms and hormone/supplement use."

Must not say:
  "You have PCOS."
  "You have androgen excess disorder."
  "You have an adrenal or ovarian tumour."
  "This confirms high testosterone disease."
```

Maximum claim strength:

```text
may be consistent with
```

---

# Phase 6 — Free testosterone low activation design

Prepare free testosterone low activation for adult male reduced androgen availability only.

Target package:

```text
knowledge_bus/packages/pkg_kb47_free_testosterone_low_androgen_deficiency_context/
```

Activation is permitted only if all of the following can be encoded deterministically.

Required biomarker gates:

```text
- free testosterone low relative to lab-provided age/sex range
- total testosterone present
- SHBG present
- albumin present if calculated free testosterone is used
```

Required demographic/context gates:

```text
- biological sex present
- biological sex = male
- adult age present
- androgen deficiency symptoms answered
- acute illness / recovery context answered
- energy availability context answered
- testosterone therapy context answered
- AAS exposure context answered
- relevant medication disclosure captured where available
- sample timing / morning sample disclosure captured where available
```

Required exclusion/fail-closed gates:

```text
- fail closed if biological sex missing
- fail closed if age missing
- fail closed if biological sex is female
- fail closed if non-adult
- fail closed if total testosterone missing
- fail closed if SHBG missing
- fail closed if androgen deficiency symptoms not_answered
- fail closed if acute illness / recovery context not_answered
- fail closed if energy availability context not_answered
- do not emit endogenous reduced-androgen interpretation if testosterone therapy or AAS exposure is answered_yes
```

Required wording boundary:

```text
May say:
  "In an adult male, this pattern may be consistent with reduced free androgen availability if it is persistent and accompanied by relevant symptoms."
  "This is not diagnostic of hypogonadism and usually requires repeat morning testing and clinical assessment."

Must not say:
  "You have hypogonadism."
  "You are testosterone deficient."
  "You need testosterone."
  "This explains your symptoms."
```

Maximum claim strength:

```text
may be consistent with
```

---

# Phase 7 — Package and governance implementation

Only after completing Phases 1–6, implement activation changes.

Allowed changes:

```text
- update signal package activation state for approved activation targets
- add runtime_context_requirements to approved activation targets
- update package manifests if required to reflect gates
- update governance activation/readiness registers
- update medical frame identity index only if required and justified
- update tests
- update carry-forward register
- create audit paper
```

Forbidden changes:

```text
- activating unsupported signals
- changing signal IDs unless a STOP gate proves unavoidable and receives explicit human approval
- changing clinical thresholds
- changing SSOT reference range policy
- frontend changes
- scoring changes
- report compiler changes
- raw research runtime reads
- LLM runtime reasoning
```

If an active package cannot encode all required gates safely, keep it inactive and document the blocker.

Do not partially activate a signal with missing gates.

---

# Phase 8 — Inactive package handling

For each inactive primary signal, update governance/readiness records to make the inactive state explicit.

Required outcomes:

```text
DHEA high:
  KEEP_INACTIVE_PENDING_DHEA_DHEAS_IDENTITY_REMEDIATION
  unless exact DHEA-S activation approval phrase is present

DHEA low:
  DO_NOT_ACTIVATE_EVIDENCE_INSUFFICIENT

FAI low:
  KEEP_INACTIVE_MODIFIER_ONLY_FUTURE or DO_NOT_ACTIVATE_EVIDENCE_INSUFFICIENT

Free testosterone percentage high:
  KEEP_INACTIVE_MODIFIER_ONLY_FUTURE or DO_NOT_ACTIVATE_EVIDENCE_INSUFFICIENT

Free testosterone percentage low:
  KEEP_INACTIVE_MODIFIER_ONLY_FUTURE or DO_NOT_ACTIVATE_EVIDENCE_INSUFFICIENT
```

Do not create a new modifier runtime pathway in this sprint.

If existing architecture already supports modifier-only status, document the status there.

If not, leave them inactive and document future modifier potential in governance only.

---

# Phase 9 — Required tests

Add or update tests proving all activated signals behave correctly.

## FT3 low tests

Must prove:

```text
- fires when FT3 low, TSH present, FT4 present and all required context gates answered
- fails closed when TSH missing
- fails closed when FT4 missing
- fails closed when thyroid medication context not_answered
- fails closed when illness/recovery context not_answered
- fails closed when energy availability context not_answered
- fails closed or suppresses if pregnancy/postpartum answered_yes and no pregnancy-specific logic exists
- does not diagnose hypothyroidism
```

## FAI high tests

Must prove:

```text
- fires for female context with high FAI, total testosterone present, SHBG present and required context answered
- fails closed when total testosterone missing
- fails closed when SHBG missing
- fails closed when biological sex missing
- fails closed for male context
- fails closed or suppresses endogenous interpretation when testosterone therapy/AAS answered_yes
- fails closed or suppresses endogenous interpretation when DHEA supplementation answered_yes
- does not diagnose PCOS
```

## Free testosterone high tests

Must prove:

```text
- fires only when free testosterone high, total testosterone present, SHBG present and required context gates are met
- fails closed when biological sex missing
- fails closed when age missing
- fails closed when total testosterone missing
- fails closed when SHBG missing
- fails closed when method gate cannot be represented safely if method is required
- suppresses endogenous interpretation when testosterone therapy/AAS answered_yes
- does not diagnose androgen disorder, PCOS, adrenal disease or ovarian disease
```

## Free testosterone low tests

Must prove:

```text
- fires for adult male only when free testosterone low, total testosterone present, SHBG present, symptoms answered and required context gates are met
- fails closed when biological sex missing
- fails closed for female context
- fails closed for non-adult context
- fails closed when total testosterone missing
- fails closed when SHBG missing
- fails closed when symptoms not_answered
- fails closed when illness/recovery context not_answered
- fails closed when energy availability context not_answered
- suppresses endogenous interpretation when testosterone therapy/AAS answered_yes
- does not diagnose hypogonadism
```

## Inactive package tests

Must prove:

```text
- DHEA high remains inactive unless explicit DHEA-S approval gate is satisfied
- DHEA low remains inactive
- FAI low remains inactive as primary signal
- free testosterone percentage high remains inactive as primary signal
- free testosterone percentage low remains inactive as primary signal
```

## Regression tests

Must prove:

```text
- existing active Batch 2 thyroid high/FT4 packages remain stable
- existing creatine kinase/eosinophil packages remain stable
- no unrelated signals change output unexpectedly
- runtime context answered_yes / answered_no / not_answered semantics still pass
- disclosure state and positive exposure remain separate
```

---

# Phase 10 — Required validation

Run and paste full output.

## Architecture / governance validators

```powershell
python backend/scripts/run_architecture_validation_gate.py
python backend/scripts/validate_day_one_architecture.py
python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
python backend/scripts/validate_context_modifier_catalogue.py --catalogue knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
```

## Context and signal regressions

```powershell
python -m pytest backend/tests/regression/test_runtime_context_evaluation.py -q
python -m pytest backend/tests/regression/test_context_threading.py -q
```

Run all relevant signal evaluator and package activation tests.

Run all relevant governance tests.

If package validators exist, run them for all 9 package directories.

If no validator exists for package activation metadata, report that as an evidence gap.

## Secret-file guardrail

Run:

```powershell
python scripts/check_no_secret_files.py
```

if present.

---

# Phase 11 — Required audit paper

Create:

```text
docs/audit-papers/BATCH2-FULL-COVERAGE-ACTIVATION-1_activate_research_supported_thyroid_and_androgen_signals.md
```

The audit paper must include:

```text
- executive verdict
- files inspected
- files changed
- medical research authority used
- 9-package research-to-runtime activation mapping table
- DHEA/DHEA-S identity STOP-gate result
- FT3 low activation details
- FAI high activation details
- free testosterone high activation details
- free testosterone low activation details
- inactive package handling
- confirmation no unsupported packages activated
- confirmation no DHEA/DHEA-S package activated unless exact approval phrase present
- confirmation no diagnosis wording introduced
- confirmation no treatment/supplement recommendation introduced
- confirmation no SSOT changed unless explicitly justified
- confirmation no scoring changed
- confirmation no report compiler changed
- confirmation no frontend changed
- confirmation no raw research runtime reads introduced
- full validator output
- full test output
- rollback path
- carry-forward impact
- recommended next action
```

Validation and test output must be pasted in full, not summarised.

---

# Phase 12 — Carry-forward handling

Update:

```text
docs/sprints/launch_core_carry_forward_register.md
```

only where justified.

Expected carry-forward handling:

```text
CF-BATCH2-010:
  May be partially closed only for the specific androgen packages activated with research authority.
  Must remain open for DHEA/DHEA-S unresolved identity if applicable.
  Must not be closed globally if DHEA remains unresolved.

FT3 low blocker:
  May be closed if FT3 low is activated with all required gates and enable_lower_bound is safely resolved.

DHEA/DHEA-S blocker:
  Add or update precise carry-forward if marker identity remains unresolved.

Modifier-only androgen patterns:
  Add precise carry-forward only if future modifier architecture is required.
```

Do not leave vague residuals.

Every inactive package must have a named reason and next condition.

---

## Expected changed files

Expected changed files may include:

```text
knowledge_bus/research/medical_reviews/batch2_thyroid_androgen_context_authority_review_v1.md
knowledge_bus/governance/batch2_full_coverage_activation_readiness_register_v1.yaml
knowledge_bus/governance/batch2_minimum_coverage_decision_register_v1.yaml
knowledge_bus/governance/batch2_context_clearance_register_v1.yaml
knowledge_bus/governance/context_runtime_execution_register_v1.yaml
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
knowledge_bus/packages/pkg_kb47_free_t3_low_low_t3_syndrome/**
knowledge_bus/packages/pkg_kb47_fai_high_biochemical_hyperandrogenism/**
knowledge_bus/packages/pkg_kb47_free_testosterone_high_androgen_excess_context/**
knowledge_bus/packages/pkg_kb47_free_testosterone_low_androgen_deficiency_context/**
backend/tests/regression/test_runtime_context_evaluation.py
backend/tests/regression/test_context_threading.py
backend/tests/governance/*
backend/tests/*
docs/sprints/launch_core_carry_forward_register.md
docs/audit-papers/BATCH2-FULL-COVERAGE-ACTIVATION-1_activate_research_supported_thyroid_and_androgen_signals.md
automation_bus/latest_cursor_status.json
```

Possible files, only if strictly justified:

```text
backend/core/analytics/runtime_context_evaluator.py
backend/core/analytics/signal_evaluator.py
```

No frontend files are expected to change.

No scoring or report compiler files are expected to change.

No SSOT files are expected to change unless the DHEA/DHEA-S identity STOP gate proves a narrow canonical identity clarification is unavoidable. If SSOT change is required, STOP and request explicit human approval before editing.

---

## Forbidden changes

Do not change:

```text
frontend/**
backend/core/reporting/**
backend/core/scoring/**
```

Do not change:

```text
backend/ssot/**
```

unless the DHEA/DHEA-S STOP gate proves a narrow identity correction is unavoidable and explicit human approval is obtained before editing.

Do not activate:

```text
- DHEA high without exact DHEA-S approval phrase
- DHEA low
- FAI low
- free testosterone percentage high
- free testosterone percentage low
- any unrelated package
```

Do not introduce:

```text
- diagnosis wording
- treatment recommendations
- supplement recommendations
- fallback parsers
- dummy parsers
- raw research runtime reads
- frontend clinical inference
- LLM clinical reasoning
```

---

## STOP conditions

STOP and report if:

```text
1. medical research authority artefact is missing from repo
2. any activation target lacks sufficient research authority
3. required context gates cannot be represented deterministically
4. answered_no and not_answered cannot be distinguished for required gates
5. positive exposure and disclosure cannot be separated
6. FT3 low cannot require TSH and FT4
7. FT3 low cannot fail closed on missing illness/recovery or energy-availability context
8. FAI high cannot be restricted to female-only initial activation
9. FAI high cannot require total testosterone and SHBG
10. free testosterone high cannot safely handle assay/method uncertainty
11. free testosterone low cannot be restricted to adult male symptom-gated interpretation
12. testosterone therapy / AAS exposure cannot suppress endogenous androgen interpretation
13. pregnancy/postpartum cannot be excluded or routed
14. DHEA and DHEA-S identity is ambiguous and activation would otherwise occur
15. activation would require frontend changes
16. activation would require scoring changes
17. activation would require report compiler changes
18. activation would require broad SSOT redesign
19. diagnosis wording would be emitted
20. treatment/supplement recommendation would be emitted
21. validators fail
22. tests fail
23. secret-file guardrail fails
24. rollback path cannot be defined
```

If a STOP condition is triggered, do not perform ad hoc remediation beyond scope.

---

## Git evidence requirements

Before commit, report:

```powershell
git branch --show-current
git status --short
git diff --name-only
git diff --cached --name-only
```

Commit message:

```text
feat(signals): activate gated Batch 2 thyroid and androgen signals
```

If no package activation occurs due to STOP gates, use:

```text
docs(governance): document Batch 2 activation blockers
```

After commit, report:

```powershell
git status --short
git log --oneline -n 5
git diff --name-only main...HEAD
```

Do not merge.

Return evidence for Claude audit and GPT architectural review.

---

## Success criteria

This sprint succeeds only if:

```text
- medical research authority is repo-persisted
- all 9 packages are mapped from research verdict to runtime outcome
- FT3 low is activated with strict gates or blocked with exact reason
- FAI high is activated female-only with strict gates or blocked with exact reason
- free testosterone high is activated with sex/method/therapy gates or blocked with exact reason
- free testosterone low is activated adult-male-only and symptom-gated or blocked with exact reason
- DHEA high remains inactive unless DHEA-S identity and exact approval phrase are both present
- DHEA low remains inactive
- FAI low remains inactive as primary signal
- free testosterone percentage high remains inactive as primary signal
- free testosterone percentage low remains inactive as primary signal
- no unsupported signals activate
- no diagnosis wording is introduced
- no treatment or supplement recommendation is introduced
- no frontend changes occur
- no scoring changes occur
- no report compiler changes occur
- no raw research runtime reads are introduced
- validators pass
- tests pass
- audit paper contains full evidence
```

Expected next action after success:

```text
Claude audit
GPT architectural review
Human approval
Merge
Then proceed to ARCH-COMPLETION-2 compiled card and root-cause authority completion.
```
