---
work_id: BETA-READINESS-SPRINT-2_runtime_gate_consistency_and_active_signal_reachability
branch: work/BETA-READINESS-SPRINT-2-runtime-gate-consistency-and-active-signal-reachability
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
---

# BETA-READINESS-SPRINT-2 — Runtime Gate Consistency and Active Signal Reachability

## Purpose

Sprint 2 must harden the active runtime signal estate before further beta/product-readiness work proceeds.

The immediate carry-forward from `DHEA-S-HIGH-ACTIVATION-1` is:

```text id="axjz5p"
Some already-active signals have pregnancy_status gates requiring answered_no.
Because the current questionnaire may not capture pregnancy_status, these signals may be suppressed for real users when pregnancy_status is absent.
```

This sprint must resolve that issue properly and prevent recurrence.

This is not a micro-sprint.

This is the first beta-readiness runtime hardening sprint after DHEA-S high activation.

---

## Strategic objective

By the end of this sprint, every currently active signal must be reachable by a realistic user context unless it is deliberately and medically justified to suppress it.

Cursor must not simply patch one YAML field and move on.

The sprint must establish an active-signal gate reachability discipline:

```text id="77npqs"
If a runtime signal is active, every required context gate must either:
1. be produced by the real questionnaire/runtime context layer;
2. allow not_answered / not_applicable where clinically safe; or
3. be explicitly documented as a deliberate suppress-until-answered gate with medical justification.
```

---

## Current expected baseline

This sprint starts after these previous works are merged:

```text id="98hm46"
ARCH-COMPLETION-3
DHEA-DHEAS-CANONICALISATION-1
DHEA-S-HIGH-ACTIVATION-1
```

Expected current state:

```text id="ghj3ke"
- Day-one architecture complete with non-blocking carry-forward
- DHEA/DHEA-S identity resolved
- DHEA-S high active as cautious standalone biomarker-level signal
- DHEA-S low inactive
- unsulfated DHEA high/low inactive
- Batch 2 active package count is 5
- Known carry-forward: pregnancy_status gate consistency for FAI high, FT3 low and free testosterone high
```

---

## Governance classification

This sprint is classified as:

```yaml id="6ri9vv"
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
```

Rationale:

```text id="5fgvjp"
- active signal runtime reachability may change
- context gate semantics may change
- runtime context evaluator may require narrow deterministic changes
- endocrine signal behaviour may change for real users
- safety wording / suppression rules must remain medically governed
```

Required route:

```text id="ya3lk9"
Cursor implementation
Claude audit
GPT architectural review
Human approval before merge
```

Do not merge.

---

## Required branch

Work only on:

```text id="8nw0oj"
work/BETA-READINESS-SPRINT-2-runtime-gate-consistency-and-active-signal-reachability
```

Do not work on `main`.

Do not merge.

---

## Non-negotiable constraints

This sprint must not:

```text id="fwaz1e"
- activate any new signal package
- deactivate any currently active signal package unless a STOP condition requires escalation
- change DHEA/DHEA-S canonicalisation rules
- change lab-derived reference range policy
- substitute global/default ranges where lab ranges exist
- introduce fallback or dummy parsers
- introduce raw Pass 3 or investigation-spec runtime reads
- introduce LLM reasoning into runtime signal evaluation
- change frontend rendering
- introduce frontend medical inference
- change scoring
- change report compiler behaviour unless explicitly required by validator failure
- add diagnosis wording
- add treatment, supplement or hormone recommendations
- make pregnancy_status answered_yes pass for signals where pregnancy-specific logic is unavailable
```

Pregnancy `answered_yes` must remain suppressive unless an existing medical authority explicitly allows pregnancy-specific interpretation.

---

## Authoritative inputs

Read before implementation:

```text id="j8pnuw"
docs/audit-papers/DHEA-S-HIGH-ACTIVATION-1_medical_authority_gated_runtime_activation.md
docs/audit-papers/DHEA-DHEAS-CANONICALISATION-1_unit_aware_marker_identity_and_adrenal_androgen_resolution.md
docs/audit-papers/BATCH2-FULL-COVERAGE-ACTIVATION-1_activate_research_supported_thyroid_and_androgen_signals.md
docs/audit-papers/ARCH-COMPLETION-3_full_traceability_manifest_and_launch_estate_gate.md

docs/Medical Research Documents/DHEA-S_High_Activation_Medical_Research_Review.md
docs/sprints/launch_core_carry_forward_register.md

knowledge_bus/governance/batch2_full_coverage_activation_execution_register_v1.yaml
knowledge_bus/governance/batch2_full_coverage_activation_readiness_register_v1.yaml
knowledge_bus/governance/day_one_full_traceability_manifest_v1.yaml
knowledge_bus/governance/day_one_launch_estate_gate_v1.yaml
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
```

Inspect all active Batch 2 package directories, including but not limited to:

```text id="4h3k30"
knowledge_bus/packages/pkg_kb47_free_t3_low_low_t3_syndrome/
knowledge_bus/packages/pkg_kb47_fai_high_biochemical_hyperandrogenism/
knowledge_bus/packages/pkg_kb47_free_testosterone_high_androgen_excess_context/
knowledge_bus/packages/pkg_kb47_free_testosterone_low_androgen_deficiency_context/
knowledge_bus/packages/pkg_kb47_dhea_high_androgen_excess_context/
```

Inspect runtime context and signal files:

```text id="xqb5q1"
backend/core/analytics/runtime_context_evaluator.py
backend/core/analytics/signal_evaluator.py
backend/core/canonical/normalize.py
backend/core/models/biomarker.py
```

Inspect questionnaire/source context files:

```text id="vf2054"
backend/config/questionnaire.json
backend/ssot/**
backend/core/data/**
```

Inspect relevant tests:

```text id="27xdmd"
backend/tests/regression/test_runtime_context_evaluation.py
backend/tests/regression/test_context_threading.py
backend/tests/regression/test_batch2_full_coverage_activation.py
backend/tests/regression/test_dhea_s_high_activation.py
backend/tests/regression/test_output_authority_provenance.py
backend/tests/governance/**
```

---

## Authority preflight

Before editing, run and report:

```powershell id="a17zab"
git branch --show-current
git status --short
git rev-parse HEAD
git log --oneline -n 10
```

Confirm:

```text id="m8y8sb"
1. Current branch matches this work package branch.
2. Working tree is clean.
3. DHEA-S-HIGH-ACTIVATION-1 is merged into main.
4. DHEA-S high is runtime_active_canonical.
5. DHEA-S low remains inactive.
6. Unsulfated DHEA high/low remain inactive.
7. Batch 2 activated package count is 5.
8. Day-one launch estate gate passes before modification.
9. The current questionnaire still does not reliably capture pregnancy_status for all users.
10. No frontend work is already staged.
```

STOP if the baseline is unclear.

---

# Phase 0 — Active signal reachability audit

Perform a read-only audit of every currently active runtime signal package.

For each active package, document:

```text id="glb0d5"
- package id
- signal id
- primary metric
- activation status
- required biomarker gates
- required context gates
- context bucket
- context key
- allowed values
- whether the key is produced by runtime_context_evaluator
- whether the key is actually captured by questionnaire.json
- whether missing / not_answered / not_applicable is allowed
- whether answered_yes suppresses, downgrades or allows
- whether the gate may suppress real users unintentionally
```

At minimum, audit:

```text id="9bsig9"
- FT3 low
- FAI high
- free testosterone high
- free testosterone low
- DHEA-S high
```

Create a temporary audit table in the sprint audit paper before making changes.

Do not edit code until this audit is complete.

---

# Phase 1 — Pregnancy-gate consistency fix

Resolve the known pregnancy gate carry-forward for:

```text id="146upe"
- pkg_kb47_fai_high_biochemical_hyperandrogenism
- pkg_kb47_free_t3_low_low_t3_syndrome
- pkg_kb47_free_testosterone_high_androgen_excess_context
```

For each package, inspect the existing medical authority and signal wording.

Allowed outcomes per package:

```text id="bu58wk"
A. Update pregnancy_status allowed_values to include answered_no, not_answered, not_applicable
B. Keep answered_no-only but document explicit medical authority requiring suppression unless answered_no
C. STOP because current authority is insufficient to decide safely
```

Preferred default, if medically safe and consistent with DHEA-S high gating model:

```yaml id="v14jch"
pregnancy_status:
  allowed_values:
    - answered_no
    - not_answered
    - not_applicable
```

Required suppression:

```text id="5vmh6r"
pregnancy_status = answered_yes must suppress the signal unless pregnancy-specific interpretation is explicitly governed.
```

Required reasoning:

```text id="2jiyqo"
Missing pregnancy_status should not automatically suppress a non-pregnancy-specific educational signal unless the governing medical authority says explicit pregnancy exclusion is required.
```

Do not guess.

If a package is clinically unsafe without explicit pregnancy exclusion, keep it suppressed and document that as an intentional design, not an accidental gate failure.

---

# Phase 2 — General active-gate reachability validator

Add a validator to prevent this class of issue recurring.

Preferred path:

```text id="ny1v03"
backend/scripts/validate_active_signal_context_gate_reachability.py
```

The validator must inspect active runtime signal packages and verify that required context gates are reachable.

Minimum validator behaviour:

```text id="mq5o8u"
For each active package:
1. Load required_context gates.
2. Identify context bucket and key.
3. Determine whether runtime_context_evaluator produces the key.
4. Determine whether allowed_values include safe missing-state handling where the questionnaire does not reliably capture the field.
5. Fail if an active signal requires a context key that is neither produced nor intentionally marked as suppress-until-answered.
6. Fail if pregnancy_status answered_yes is allowed without pregnancy-specific authority.
7. Produce a clear package-by-package report.
```

Acceptable implementation:

```text id="883kxb"
The first version may use an explicit registry/allowlist for known questionnaire-produced context keys, provided it is transparent and tested.
```

Forbidden implementation:

```text id="j19mnk"
- hardcoded PASS for all active packages
- ignoring required_context gates
- relying on Cursor comments rather than actual package data
- broad parser rewrite
- LLM evaluation
```

Wire the validator into the architecture/golden gate only if it is stable and deterministic.

If wiring into the global gate creates too much risk, run it as a sprint-specific validator and document follow-up to promote it.

---

# Phase 3 — Real-user active signal regression suite

Add tests proving each active signal is reachable using realistic runtime context.

At minimum, tests must cover:

```text id="dmoxb0"
1. DHEA-S high activates with:
   - biological sex
   - date of birth / age
   - DHEA-S above lab range
   - no pregnancy_status field
   - no symptoms field
   - no supplements field

2. FAI high behaviour with:
   - biological sex
   - date of birth / age
   - FAI high or required testosterone/SHBG inputs
   - no pregnancy_status field

3. Free testosterone high behaviour with:
   - biological sex
   - date of birth / age
   - free testosterone high
   - no pregnancy_status field

4. FT3 low behaviour with:
   - biological sex
   - date of birth / age
   - FT3 low pattern as required by existing package
   - no pregnancy_status field
```

For each signal, tests must also cover:

```text id="3hd9u6"
- pregnancy_status answered_yes suppresses where pregnancy-specific logic is unavailable
- pregnancy_status answered_no allows where other gates pass
- pregnancy_status not_answered / not_applicable behaviour
- missing age suppresses if age is required
- missing biological sex suppresses if sex is required
```

If a package deliberately requires answered_no pregnancy status, write the test to prove that deliberate suppression and cite the governing reason in the audit paper.

---

# Phase 4 — Runtime context evaluator review

Review `runtime_context_evaluator.py` for disclosure-state consistency.

Specifically inspect:

```text id="eslrx2"
- pregnancy_status
- dhea_supplementation_status
- hormone_therapy_status
- aas_exposure_status
- symptoms_status
- sex
- age
```

Required outcome:

```text id="a0o0mf"
Context keys used by active package gates must be produced deterministically or deliberately absent with documented reason.
```

Allowed change:

```text id="52f87y"
Small deterministic additions that set missing optional disclosure fields to not_answered / not_applicable where this is consistent with the context model.
```

Forbidden change:

```text id="cjoqaw"
- broad context model rewrite
- new questionnaire UX fields
- frontend changes
- LLM-based context inference
- changing answered_yes semantics to pass where it should suppress
```

If broader context model changes are genuinely needed, STOP and report.

---

# Phase 5 — Governance and carry-forward cleanup

Update governance and sprint records.

Required updates:

```text id="fd3s55"
- Close or resolve the pregnancy-gate consistency carry-forward.
- Add new validator to architecture/golden gate if promoted.
- If not promoted, record exact promotion condition.
- Confirm DHEA-S high remains active.
- Confirm DHEA-S low remains inactive.
- Confirm unsulfated DHEA remains inactive.
- Confirm Batch 2 active package count remains 5.
```

Likely files:

```text id="1hpzxm"
docs/sprints/launch_core_carry_forward_register.md
knowledge_bus/governance/day_one_launch_estate_gate_v1.yaml
knowledge_bus/governance/day_one_full_traceability_manifest_v1.yaml
knowledge_bus/governance/batch2_full_coverage_activation_execution_register_v1.yaml
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
```

Do not inflate carry-forward.

Every remaining carry-forward must have:

```text id="00bk7r"
- owner
- reason
- closure condition
- target work_id or decision point
- consequence if not resolved
```

---

# Phase 6 — Safety wording and output boundary check

Review active endocrine signal wording only where touched or where tests expose risk.

Must confirm:

```text id="bf6o1e"
- no PCOS diagnosis
- no adrenal tumour implication
- no adrenal overactivity wording
- no adrenal dysfunction wording
- no confirmed hyperandrogenism claim
- no treatment, supplement or hormone recommendation
- no pregnancy-specific interpretation unless medically governed
```

Do not rewrite broader report content.

Do not change report compiler architecture.

If user-facing wording is materially changed, add wording-safety tests or document why existing tests cover it.

---

# Phase 7 — Required tests and validation

Run and paste full output.

## Architecture / governance validators

```powershell id="ohfl5a"
python backend/scripts/run_architecture_validation_gate.py
python backend/scripts/validate_day_one_architecture.py
python backend/scripts/validate_day_one_launch_estate_gate.py
python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
python backend/scripts/validate_context_modifier_catalogue.py --catalogue knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
```

Run the new active gate reachability validator:

```powershell id="7fegos"
python backend/scripts/validate_active_signal_context_gate_reachability.py
```

if created.

## Regression tests

```powershell id="or20o1"
python -m pytest backend/tests/regression/test_runtime_context_evaluation.py -q
python -m pytest backend/tests/regression/test_context_threading.py -q
python -m pytest backend/tests/regression/test_batch2_full_coverage_activation.py -q
python -m pytest backend/tests/regression/test_dhea_s_high_activation.py -q
python -m pytest backend/tests/regression/test_output_authority_provenance.py -q
```

Run all new/updated active signal reachability tests.

Run all relevant governance tests.

## Secret-file guardrail

Run if present:

```powershell id="8kqc8w"
python scripts/check_no_secret_files.py
```

---

# Phase 8 — Required audit paper

Create:

```text id="gmc63k"
docs/audit-papers/BETA-READINESS-SPRINT-2_runtime_gate_consistency_and_active_signal_reachability.md
```

The audit paper must include:

```text id="b7glbz"
- executive verdict
- files inspected
- files changed
- active signal reachability audit table
- pregnancy-gate consistency findings
- per-package decision for FAI high, FT3 low and free testosterone high
- exact gate changes made
- exact gates deliberately not changed and why
- runtime context evaluator review
- validator design and output
- real-user scenario tests
- safety wording review
- governance updates
- carry-forward updates
- confirmation DHEA-S high remains active
- confirmation DHEA-S low remains inactive
- confirmation unsulfated DHEA remains inactive
- confirmation no new signal activation
- confirmation no signal deactivation unless explicitly escalated
- confirmation no frontend changes
- confirmation no scoring changes
- confirmation no report compiler changes
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

```powershell id="x45ksd"
git branch --show-current
git status --short
git diff --name-only
git diff --cached --name-only
```

Expected commit message:

```text id="70fsz4"
fix(signals): harden active signal context gate reachability
```

After commit, report:

```powershell id="2fgs7o"
git status --short
git log --oneline -n 5
git diff --name-only main...HEAD
```

Run:

```powershell id="gw0832"
python backend/scripts/run_work_package.py finish
```

Return final gate evidence.

Do not merge.

---

## Expected changed files

Likely changed files:

```text id="gsdlhr"
knowledge_bus/packages/pkg_kb47_fai_high_biochemical_hyperandrogenism/signal_library.yaml
knowledge_bus/packages/pkg_kb47_free_t3_low_low_t3_syndrome/signal_library.yaml
knowledge_bus/packages/pkg_kb47_free_testosterone_high_androgen_excess_context/signal_library.yaml

backend/core/analytics/runtime_context_evaluator.py
backend/scripts/validate_active_signal_context_gate_reachability.py

backend/tests/regression/test_runtime_context_evaluation.py
backend/tests/regression/test_context_threading.py
backend/tests/regression/test_batch2_full_coverage_activation.py
backend/tests/regression/test_active_signal_context_gate_reachability.py
backend/tests/governance/test_active_signal_context_gate_reachability_governance.py

knowledge_bus/governance/day_one_launch_estate_gate_v1.yaml
knowledge_bus/governance/day_one_full_traceability_manifest_v1.yaml
knowledge_bus/governance/medical_frame_identity_index_v1.yaml

docs/sprints/launch_core_carry_forward_register.md
docs/audit-papers/BETA-READINESS-SPRINT-2_runtime_gate_consistency_and_active_signal_reachability.md
```

No frontend files are expected.

No scoring files are expected.

No parser files are expected unless a validator proves a narrow issue.

---

## STOP conditions

STOP and report if:

```text id="2hhzvb"
1. DHEA-S-HIGH-ACTIVATION-1 is not merged.
2. DHEA-S high is not active.
3. Batch 2 active package count is not 5.
4. Existing active signal package gates cannot be read deterministically.
5. Pregnancy_status semantics cannot be resolved from existing medical authority.
6. Any package appears unsafe to allow not_answered / not_applicable pregnancy status.
7. Any active signal would require a new questionnaire field before it can safely fire.
8. A fix would require frontend changes.
9. A fix would require scoring changes.
10. A fix would require report compiler changes.
11. A fix would require broad runtime context redesign.
12. Pregnancy answered_yes would need to pass without pregnancy-specific authority.
13. Any new signal activation is required.
14. Any existing active signal deactivation is required.
15. Diagnosis wording would be introduced.
16. Treatment/supplement/hormone recommendation would be introduced.
17. Validators fail.
18. Tests fail.
19. Secret-file guardrail fails.
20. Rollback path cannot be defined.
```

Do not perform ad hoc remediation beyond scope.

---

## Success criteria

This sprint succeeds only if:

```text id="atz97x"
- pregnancy-gate consistency is resolved for FAI high, FT3 low and free testosterone high
- every active signal is reachable by realistic user context or deliberately suppressed with medical justification
- pregnancy answered_yes remains suppressive unless governed
- not_answered / not_applicable behaviour is explicit
- DHEA-S high remains active
- DHEA-S low remains inactive
- unsulfated DHEA remains inactive
- no new signals are activated
- no active signals are unintentionally suppressed for real users
- active gate reachability validator exists or a documented reason explains why it was not promoted
- validators pass
- tests pass
- audit paper contains full evidence
```

Expected next action after success:

```text id="lo3s24"
Claude audit
GPT architectural review
Human approval
Merge

Then proceed to the next beta/product-readiness sprint.
```
