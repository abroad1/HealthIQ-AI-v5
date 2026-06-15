---
work_id: DHEA-S-HIGH-ACTIVATION-1_medical_authority_gated_runtime_activation
branch: work/DHEA-S-HIGH-ACTIVATION-1-medical-authority-gated-runtime-activation
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
---

# DHEA-S-HIGH-ACTIVATION-1 — Medical Authority Gated Runtime Activation

## Purpose

Activate the DHEA-S high signal as a cautious, non-diagnostic, biomarker-level runtime signal using the new medical research authority report:

```text
docs/Medical Research Documents/DHEA-S_High_Activation_Medical_Research_Review.md
```

This report supersedes the previous activation blocker for DHEA-S high only.

It states:

```text
DHEA-S high:
- activation_recommendation: DHEA_S_HIGH_ACTIVATE_NOW
- standalone_signal_allowed: true
- corroboration_required: false
```

The activation must remain narrow.

It must not activate:

```text
- DHEA-S low
- unsulfated DHEA high
- unsulfated DHEA low
- broad adrenal androgen excess context without supporting evidence
- PCOS interpretation
- adrenal tumour interpretation
- adrenal dysfunction interpretation
```

---

## Strategic context

The previous sprint `DHEA-DHEAS-CANONICALISATION-1` resolved the marker identity problem:

```text
"DHEA (Venous)" + µmol/L + DHEA-S-like reference range now resolves to canonical `dhea_s`.
```

Current expected repo state before this sprint:

```text
- DHEA/DHEA-S identity resolved
- DHEA and DHEA-S remain separate canonical concepts
- DHEA-S high package has primary_metric: dhea_s
- DHEA-S high is currently inactive_pending_external_clinician_signoff or equivalent inactive state
- DHEA-S low remains inactive
- DHEA low remains inactive
- unit-aware canonicalisation model is runtime_consumed: false
```

The new medical authority report now allows DHEA-S high to activate as a standalone cautious signal, provided the interpretation remains biomarker-level and safe.

---

## Governance classification

This sprint is:

```yaml
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
```

Rationale:

```text
- Runtime signal activation may occur.
- Endocrine/adrenal-androgen interpretation is clinically sensitive.
- Package activation status will change.
- User-facing output may change.
- Medical authority and governance registers must be updated.
```

Required route:

```text
Cursor implementation
Claude audit
GPT architectural review
Human approval before merge
```

Do not merge.

---

## Required branch

Work only on:

```text
work/DHEA-S-HIGH-ACTIVATION-1-medical-authority-gated-runtime-activation
```

Do not work on `main`.

Do not merge.

---

## Non-negotiable constraints

This sprint must not:

```text
- change DHEA/DHEA-S canonicalisation rules unless a validator proves a narrow fix is required
- silently map ambiguous DHEA to DHEA-S without unit/reference-range evidence
- activate DHEA-S low
- activate unsulfated DHEA high
- activate unsulfated DHEA low
- activate broad androgen-excess context without corroborating markers/symptoms
- diagnose PCOS
- diagnose adrenal disease
- imply adrenal tumour
- imply adrenal overactivity
- imply adrenal dysfunction
- recommend DHEA, testosterone, hormones, supplements or treatment
- change lab-derived reference range policy
- substitute global/default ranges where lab ranges exist
- change frontend rendering
- introduce frontend medical inference
- introduce fallback or dummy parsers
- introduce raw Pass 3 or investigation-spec runtime reads
- introduce LLM reasoning into runtime signal evaluation
```

Maximum permitted claim strength:

```text
may support
may be consistent with
```

Prohibited claim strength:

```text
suggests
strongly suggests
indicates
diagnostic of
```

---

## Authoritative inputs

Read before implementation:

```text
docs/Medical Research Documents/DHEA-S_High_Activation_Medical_Research_Review.md

docs/audit-papers/DHEA-DHEAS-CANONICALISATION-1_unit_aware_marker_identity_and_adrenal_androgen_resolution.md
docs/audit-papers/BATCH2-FULL-COVERAGE-ACTIVATION-1_activate_research_supported_thyroid_and_androgen_signals.md
docs/audit-papers/ARCH-COMPLETION-3_full_traceability_manifest_and_launch_estate_gate.md
docs/sprints/launch_core_carry_forward_register.md

knowledge_bus/governance/unit_aware_biomarker_canonicalisation_model_v1.yaml
knowledge_bus/governance/batch2_full_coverage_activation_execution_register_v1.yaml
knowledge_bus/governance/batch2_full_coverage_activation_readiness_register_v1.yaml
knowledge_bus/governance/day_one_full_traceability_manifest_v1.yaml
knowledge_bus/governance/day_one_launch_estate_gate_v1.yaml
knowledge_bus/governance/medical_frame_identity_index_v1.yaml

knowledge_bus/packages/pkg_kb47_dhea_high_androgen_excess_context/
knowledge_bus/packages/pkg_kb47_dhea_low_adrenal_androgen_reduction/
```

Inspect runtime files:

```text
backend/core/canonical/unit_aware_biomarker_identity_v1.py
backend/core/canonical/normalize.py
backend/core/models/biomarker.py
backend/core/analytics/signal_evaluator.py
backend/core/analytics/runtime_context_evaluator.py
backend/ssot/biomarker_alias_registry.yaml
```

Inspect tests:

```text
backend/tests/regression/test_dhea_dheas_canonicalisation.py
backend/tests/regression/test_dhea_s_high_remains_inactive.py
backend/tests/regression/test_batch2_full_coverage_activation.py
backend/tests/regression/test_output_authority_provenance.py
backend/tests/governance/test_dhea_dheas_canonicalisation_governance.py
```

---

## Authority preflight

Before editing, run and report:

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
3. DHEA-DHEAS-CANONICALISATION-1 is merged.
4. The new medical authority file exists at:
   docs/Medical Research Documents/DHEA-S_High_Activation_Medical_Research_Review.md
5. The medical authority file says DHEA_S_HIGH_ACTIVATE_NOW.
6. The medical authority file says standalone_signal_allowed: true.
7. The medical authority file says corroboration_required: false.
8. DHEA-S high is currently inactive.
9. DHEA-S low is currently inactive.
10. Unsulfated DHEA high/low are not active.
11. "DHEA (Venous)" + µmol/L + DHEA-S-like range resolves to `dhea_s`.
12. Lab-derived reference range policy remains active.
13. Day-one launch estate gate passes before modification.
```

STOP if any of these are false or unclear.

---

# Phase 1 — Medical authority interpretation

Create an implementation-facing authority summary from the medical report.

Record:

```text
DHEA-S high:
  activation_recommendation: DHEA_S_HIGH_ACTIVATE_NOW
  standalone_signal_allowed: true
  corroboration_required: false

DHEA-S low:
  recommendation: BIOMARKER_LEVEL_EXPLANATION_ONLY

Unsulfated DHEA:
  high_recommendation: DO_NOT_ACTIVATE
  low_recommendation: DO_NOT_ACTIVATE
```

This sprint must treat the report as the superseding authority for DHEA-S high activation.

Do not treat it as approval for broad androgen-excess diagnosis.

---

# Phase 2 — Runtime activation design

Activate DHEA-S high as a cautious standalone biomarker-level signal.

Required activation condition:

```text
Activate DHEA-S high only when:
1. canonical_id is `dhea_s`
2. source marker is not unsulfated DHEA
3. value is above the lab-provided reference range
4. age is present
5. biological sex is present
6. DHEA supplementation status is captured or explicitly not answered
7. testosterone therapy status is captured or explicitly not answered
8. anabolic steroid / AAS exposure status is captured or explicitly not answered
9. pregnancy status is captured where applicable, or marked not applicable / not answered according to current context model
10. HRT / hormone therapy status is captured where applicable, or explicitly not answered
```

Required suppression:

```text
- suppress if DHEA supplementation answered_yes
- suppress if pregnancy answered_yes and pregnancy-specific logic is unavailable
- suppress if age missing
- suppress if biological sex missing
- suppress if canonical identity is ambiguous
- suppress if marker is unsulfated DHEA
```

Required downgrade / limitation wording:

```text
- downgrade if testosterone therapy answered_yes
- downgrade if anabolic steroid exposure answered_yes
- downgrade if HRT / hormone therapy answered_yes
- downgrade if known adrenal condition disclosed
- downgrade if glucocorticoid medication disclosed
- downgrade if severe acute illness disclosed
- downgrade if symptom context missing
- allow with caution if testosterone / SHBG / FAI are missing
```

Important:

```text
Testosterone, SHBG, FAI and symptoms are not required for the basic DHEA-S high signal.
They are required only for broader androgen-excess interpretation, which is out of scope unless already supported by existing governed mechanisms.
```

---

# Phase 3 — Package activation

Target package:

```text
knowledge_bus/packages/pkg_kb47_dhea_high_androgen_excess_context/
```

Update package identity and activation state so that:

```text
primary_metric: dhea_s
identity_remediation_status: IDENTITY_RESOLVED_PRIMARY_METRIC_DHEA_S
governance_runtime_activation_status: runtime_active_canonical
behavioural_impact: SIGNAL_RUNTIME_ACTIVATION
```

If existing schema uses different exact enum values, inspect nearby active packages and use the established repo convention.

Do not create a new enum unless required by validators.

Update signal/library metadata to make clear:

```text
- signal is DHEA-S high
- signal is standalone biomarker-level
- companion androgen markers are strongly recommended but not required
- broad androgen-excess wording requires corroboration
- diagnosis wording is prohibited
```

Do not rename the package directory unless existing governance requires it. If the directory remains `pkg_kb47_dhea_high_androgen_excess_context`, the manifest must clearly state that runtime primary metric is DHEA-S and that broad androgen-excess wording is not permitted without corroboration.

---

# Phase 4 — Safe wording implementation

User-facing wording must stay close to the medical authority wording.

Permitted wording:

```text
Your DHEA-S result is above the reference range provided by the laboratory. DHEA-S is an adrenal androgen marker, meaning it is mainly produced by the adrenal glands and can act as a precursor to other sex hormones. A higher result may be consistent with increased adrenal androgen production, but this result is not diagnostic on its own. Interpretation depends on age, biological sex, symptoms, hormone therapy, anabolic steroid or DHEA supplement use, pregnancy status where relevant, and other androgen markers such as testosterone, SHBG or free androgen index if available.
```

If symptom or companion androgen context is missing, include a limitation such as:

```text
Because symptom information and/or supporting androgen markers are not available, this should be treated as a biomarker-level observation rather than a broader androgen-excess interpretation.
```

If level is markedly raised or severe/rapid symptoms are present and current runtime can represent that safely, use clinician-review wording only:

```text
Markedly raised DHEA-S or rapid new androgen-related symptoms may warrant clinical review.
```

Forbidden wording:

```text
You have adrenal androgen excess.
You have adrenal overactivity.
This means you have PCOS.
This suggests an adrenal tumour.
Your adrenal glands are dysfunctional.
This confirms hyperandrogenism.
You need DHEA, testosterone, hormone therapy or supplements.
```

---

# Phase 5 — Governance updates

Update governance so the new authority chain is explicit.

Likely files:

```text
knowledge_bus/governance/batch2_full_coverage_activation_execution_register_v1.yaml
knowledge_bus/governance/batch2_full_coverage_activation_readiness_register_v1.yaml
knowledge_bus/governance/day_one_full_traceability_manifest_v1.yaml
knowledge_bus/governance/day_one_launch_estate_gate_v1.yaml
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
docs/sprints/launch_core_carry_forward_register.md
```

Required governance outcome:

```text
- DHEA-S high moves from inactive / pending sign-off to activated package
- activated_package_count increases from 4 to 5 if that is the existing count
- CF-DHEA-S-ACTIVATION-001 is closed
- CF-BATCH2-010 is updated to remove DHEA-S high from the inactive androgen package set
- DHEA-S low remains inactive
- unsulfated DHEA high/low remain inactive
- new medical authority report is cited as superseding authority for DHEA-S high only
```

Do not reopen day-one architecture unless a validator requires it.

---

# Phase 6 — Tests

Add or update tests proving all of the following.

## Activation tests

```text
1. DHEA-S high activates when `dhea_s` is above lab-provided range and required demographic/context gates are present.
2. "DHEA (Venous)" + µmol/L + DHEA-S-like range canonicalises to `dhea_s` and can activate DHEA-S high if above range.
3. Explicit DHEAS / DHEA-S labels can activate when above lab range.
4. Normal DHEA-S does not activate.
5. Low DHEA-S does not activate a primary signal.
6. Unsulfated DHEA high does not activate DHEA-S high.
7. Ambiguous DHEA without unit/reference-range evidence fails closed and does not activate.
```

## Suppression tests

```text
8. DHEA supplementation answered_yes suppresses the signal.
9. Pregnancy answered_yes suppresses the signal if pregnancy-specific logic is unavailable.
10. Missing age suppresses the signal.
11. Missing biological sex suppresses the signal.
```

## Downgrade / wording tests

```text
12. Missing testosterone / SHBG / FAI does not suppress the basic signal.
13. Missing testosterone / SHBG / FAI prevents broader androgen-excess wording.
14. Missing symptoms prevents broader androgen-excess wording.
15. Testosterone therapy answered_yes downgrades or limits interpretation.
16. AAS exposure answered_yes downgrades or limits interpretation.
17. Output contains no PCOS diagnosis.
18. Output contains no adrenal tumour implication.
19. Output contains no adrenal overactivity / adrenal dysfunction claim.
20. Output contains no treatment, supplement or hormone recommendation.
```

## Regression tests

```text
21. Existing four Batch 2 active signals remain active and unchanged.
22. DHEA-S low remains inactive.
23. DHEA low remains inactive.
24. Free testosterone / FAI signals remain unchanged.
25. Day-one launch estate validator still passes.
26. No raw Pass 3 runtime reads are introduced.
27. No frontend changes are required.
28. No scoring changes are required.
```

If the current test framework cannot inspect wording directly, document the gap and add the strongest available assertion.

---

# Phase 7 — Required validation

Run and paste full output.

## Architecture / governance validators

```powershell
python backend/scripts/run_architecture_validation_gate.py
python backend/scripts/validate_day_one_architecture.py
python backend/scripts/validate_day_one_launch_estate_gate.py
python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
python backend/scripts/validate_context_modifier_catalogue.py --catalogue knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
```

## Regression tests

```powershell
python -m pytest backend/tests/regression/test_dhea_dheas_canonicalisation.py -q
python -m pytest backend/tests/regression/test_dhea_s_high_activation.py -q
python -m pytest backend/tests/regression/test_batch2_full_coverage_activation.py -q
python -m pytest backend/tests/regression/test_output_authority_provenance.py -q
python -m pytest backend/tests/regression/test_runtime_context_evaluation.py -q
python -m pytest backend/tests/regression/test_context_threading.py -q
```

Run all new/updated governance and unit tests.

## Secret-file guardrail

Run if present:

```powershell
python scripts/check_no_secret_files.py
```

---

# Phase 8 — Required audit paper

Create:

```text
docs/audit-papers/DHEA-S-HIGH-ACTIVATION-1_medical_authority_gated_runtime_activation.md
```

The audit paper must include:

```text
- executive verdict
- files inspected
- files changed
- medical authority summary
- explanation of why this report supersedes the prior DHEA-S high blocker
- confirmation DHEA-S high is activated only as biomarker-level cautious signal
- confirmation corroboration is not required for basic signal
- confirmation corroboration is required for broader androgen-excess wording
- exact activation gates
- exact suppression gates
- exact downgrade/limitation rules
- wording safety review
- DHEA-S low outcome
- unsulfated DHEA outcome
- governance updates
- carry-forward updates
- confirmation no frontend changes
- confirmation no scoring changes
- confirmation no report compiler changes unless explicitly justified
- confirmation no raw research runtime reads introduced
- confirmation no diagnosis wording introduced
- confirmation no treatment/supplement recommendation introduced
- full validator output
- full test output
- rollback path
- recommended next action
```

Validation and test output must be pasted in full, not summarised.

---

# Phase 9 — Git evidence requirements

Before commit, report:

```powershell
git branch --show-current
git status --short
git diff --name-only
git diff --cached --name-only
```

Expected commit message:

```text
feat(signals): activate medically authorised DHEA-S high signal
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

## Expected changed files

Likely changed files:

```text
knowledge_bus/packages/pkg_kb47_dhea_high_androgen_excess_context/package_manifest.yaml
knowledge_bus/packages/pkg_kb47_dhea_high_androgen_excess_context/signal_library.yaml
knowledge_bus/packages/pkg_kb47_dhea_high_androgen_excess_context/promoted_signal_intelligence.yaml

knowledge_bus/governance/batch2_full_coverage_activation_execution_register_v1.yaml
knowledge_bus/governance/batch2_full_coverage_activation_readiness_register_v1.yaml
knowledge_bus/governance/day_one_full_traceability_manifest_v1.yaml
knowledge_bus/governance/day_one_launch_estate_gate_v1.yaml
knowledge_bus/governance/medical_frame_identity_index_v1.yaml

docs/sprints/launch_core_carry_forward_register.md
docs/audit-papers/DHEA-S-HIGH-ACTIVATION-1_medical_authority_gated_runtime_activation.md

backend/tests/regression/test_dhea_s_high_activation.py
backend/tests/regression/test_dhea_dheas_canonicalisation.py
backend/tests/governance/test_dhea_s_high_activation_governance.py
```

No frontend files are expected.

No scoring files are expected.

No parser fallback files are expected.

---

## STOP conditions

STOP and report if:

```text
1. DHEA-DHEAS-CANONICALISATION-1 is not merged.
2. The medical authority report is missing.
3. The report does not contain DHEA_S_HIGH_ACTIVATE_NOW.
4. The report does not contain standalone_signal_allowed: true.
5. The report does not contain corroboration_required: false.
6. DHEA-S identity is not resolved.
7. DHEA and DHEA-S are conflated.
8. "DHEA (Venous)" + µmol/L + DHEA-S-like range does not resolve to `dhea_s`.
9. DHEA supplementation cannot suppress endogenous interpretation.
10. Pregnancy cannot suppress where required.
11. Missing age or sex cannot suppress.
12. Activation would require frontend changes.
13. Activation would require scoring changes.
14. Activation would require broad SSOT redesign.
15. Activation would introduce diagnosis wording.
16. Activation would introduce treatment/supplement/hormone recommendation.
17. DHEA-S low would become active.
18. Unsulfated DHEA would become active.
19. Validators fail.
20. Tests fail.
21. Secret-file guardrail fails.
22. Rollback path cannot be defined.
```

Do not perform ad hoc remediation beyond scope.

---

## Success criteria

This sprint succeeds only if:

```text
- DHEA-S high is activated as a cautious standalone biomarker-level signal
- activation uses lab-provided reference range
- activation requires age and biological sex
- activation suppresses DHEA supplementation
- activation suppresses pregnancy where pregnancy-specific logic is unavailable
- companion androgen markers are not required for the basic signal
- companion androgen markers are required for broader androgen-excess wording
- DHEA-S low remains inactive
- unsulfated DHEA high/low remain inactive
- DHEA/DHEA-S canonicalisation remains intact
- governance cites the new medical authority report
- CF-DHEA-S-ACTIVATION-001 is closed
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

Then proceed to the next product/beta readiness or architecture-debt item.
```
