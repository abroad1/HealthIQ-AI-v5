---
work_id: WAVE1-PUBLIC-LAUNCH-FIXES-1_pre_public_launch_blocker_remediation
branch: work/WAVE1-PUBLIC-LAUNCH-FIXES-1-pre-public-launch-blocker-remediation
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
---

# WAVE1-PUBLIC-LAUNCH-FIXES-1 — Pre-Public Launch Blocker Remediation

## Purpose

Remediate the four conditional blockers identified by the Wave 1 product launch-readiness audit so HealthIQ AI can proceed safely toward public Wave 1 launch preparation.

This is one outcome-based remediation sprint.

Do not split this into four micro-sprints unless a STOP condition proves that one blocker cannot be remediated safely within this work package.

The four launch-readiness blockers are:

```text
CB-1 — frontend PII console logging in AnalysisService.startAnalysis()
CB-2 — unauthenticated /api/upload/parse endpoint
CB-3 — urate unit conversion failure caused by Unicode mu mismatch
CB-4 — unsafe dev billing override values in backend/env.example
```

The expected outcome is:

```text
All four public-launch blockers remediated, validated, and documented.
```

---

## Strategic context

The Day-One Architecture Closure Review accepted the architecture with conditions.

The Wave 1 Launch Readiness Audit returned:

```text
LAUNCH_READY_WITH_CONDITIONS
```

No new architecture programme is required.

This sprint must fix the specific public-launch blockers and preserve the existing governed runtime architecture.

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
- privacy / health data exposure is in scope
- backend authentication is in scope
- unit conversion affects real-world lab result handling
- launch-readiness status depends on the outcome
- frontend and backend runtime behaviour may change
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
work/WAVE1-PUBLIC-LAUNCH-FIXES-1-pre-public-launch-blocker-remediation
```

Do not work on `main`.

Do not merge.

---

## Non-negotiable constraints

This sprint must not:

```text
- change clinical thresholds
- change biomarker reference range policy
- change scoring
- change report compiler logic
- change SSOT biomarker definitions
- change signal IDs
- change activation keys
- activate any package
- modify package signal_library.yaml files
- alter androgen or FT3 low activation state
- introduce fallback or dummy parsers
- introduce raw Pass 3 / investigation-spec runtime reads
- introduce frontend medical inference
- add LLM-based clinical reasoning
```

The sprint may touch frontend service code, backend route auth, unit registry normalisation, env example configuration, tests, and audit documentation only.

---

## Authoritative inputs

Read before implementation:

```text
docs/audit-papers/WAVE1-LAUNCH-READINESS-1_product_readiness_and_release_gate.md
docs/audit-papers/DAY-ONE-ARCHITECTURE-CLOSURE-REVIEW.md
docs/architecture/ADR-RT-001_research_to_runtime_day_one_architecture.md
docs/sprints/launch_core_carry_forward_register.md
```

Also inspect:

```text
frontend/app/services/analysis.ts
backend/app/routes/upload.py
backend/app/routes/analysis.py
backend/core/units/registry.py
backend/env.example
backend/.env.test
frontend/.env.local.example
sentinel/reports/sentinel_run_87c5a2cd.json
```

Inspect relevant tests for:

```text
- upload / parse route auth
- analysis route auth
- unit conversion / unit registry
- urate conversion
- frontend analysis service
- sentinel / launch-readiness regression tests
```

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
3. WAVE1-LAUNCH-READINESS-1 audit exists.
4. The audit lists CB-1, CB-2, CB-3, and CB-4.
5. BATCH2-CONTEXT-COMPLETION-1 is already merged.
6. No androgen package is active.
7. FT3 low is inactive.
```

STOP if the baseline is not the post-launch-readiness audit baseline.

---

## Reality check

Before implementation, confirm each blocker still exists.

### CB-1 reality check

Inspect:

```text
frontend/app/services/analysis.ts
```

Confirm whether `AnalysisService.startAnalysis()` still logs:

```text
- full request payload
- user demographics
- questionnaire data
- biomarker values
- JSON.stringify(data, null, 2)
```

If the logging is already removed, record that and do not re-edit unnecessarily.

### CB-2 reality check

Inspect:

```text
backend/app/routes/upload.py
backend/app/routes/analysis.py
```

Confirm whether `/api/upload/parse` still lacks the authentication dependency used by `/api/analysis/start`.

If already authenticated, record that and do not re-edit unnecessarily.

### CB-3 reality check

Inspect:

```text
backend/core/units/registry.py
```

Confirm whether the registry still treats these as distinct incompatible units:

```text
μmol/L  # U+03BC Greek small letter mu
µmol/L  # U+00B5 micro sign
```

Reproduce or identify the failing sentinel / regression tests if possible.

### CB-4 reality check

Inspect:

```text
backend/env.example
```

Confirm whether it still contains unsafe launch-risk defaults:

```text
HEALTHIQ_DISABLE_BILLING_ENFORCEMENT=1
HEALTHIQ_FREE_COMPLETED_ANALYSES=99
```

If already removed or neutralised, record that.

---

## Scope

This sprint may remediate only:

```text
CB-1 — remove frontend PII console logging
CB-2 — add auth to /api/upload/parse
CB-3 — normalise Unicode mu variants in unit registry
CB-4 — remove / neutralise dev billing override values in env.example
```

It may also add or update tests directly proving those fixes.

It may add a sprint audit paper and, if useful, a launch-fixes evidence register.

---

# Phase 1 — CB-1: Remove frontend PII console logging

## Required remediation

In:

```text
frontend/app/services/analysis.ts
```

Remove production console logging from:

```text
AnalysisService.startAnalysis()
```

Specifically remove or guard any logging of:

```text
- full analysis payload
- user demographics
- questionnaire data
- biomarker values
- request body JSON
- JSON.stringify(data, null, 2)
- console.group trace blocks containing health data
```

Preferred fix:

```text
Remove the logs entirely.
```

Do not replace them with another logging pathway.

Do not introduce a debug flag that could accidentally expose health data in production.

## Allowed remaining logs

Only non-sensitive operational logs may remain if already present and necessary, for example:

```text
- request started
- request completed
- status code
```

But do not log payload contents, biomarker values, user data, questionnaire answers, or full JSON bodies.

## Required tests / checks

Add or update frontend tests if a suitable test pattern exists.

At minimum, perform a grep check proving no live frontend service logs sensitive analysis payloads:

```text
frontend/app/services/analysis.ts
```

Search for:

```text
console.log
console.group
console.groupEnd
JSON.stringify(data
Full Payload
Request body
User data
```

If logs remain, explain why they are safe.

---

# Phase 2 — CB-2: Authenticate /api/upload/parse

## Required remediation

In:

```text
backend/app/routes/upload.py
```

Add the same authentication dependency / bearer-token pattern used by:

```text
backend/app/routes/analysis.py
/api/analysis/start
```

Do not invent a new authentication pattern.

Do not create a parallel auth mechanism.

Do not weaken analysis route authentication.

The goal is:

```text
/api/upload/parse must require an authenticated user before accepting file or text parsing requests.
```

## Required behaviour

Unauthenticated requests to `/api/upload/parse` must fail safely.

Authenticated requests must continue to work.

The route must still support the existing accepted inputs:

```text
- UploadFile
- text_content
```

Do not alter parsing semantics except for authentication gating.

## Required tests

Add or update backend route tests proving:

```text
1. unauthenticated /api/upload/parse request is rejected
2. authenticated /api/upload/parse request reaches the existing parse flow
3. /api/analysis/start auth behaviour is unchanged
```

If test infrastructure for route auth is not available, create the narrowest safe regression test or document the blocker and STOP before committing.

---

# Phase 3 — CB-3: Fix Unicode mu unit conversion defect

## Required remediation

In:

```text
backend/core/units/registry.py
```

Normalise visually equivalent micro unit characters before unit matching / conversion.

The defect:

```text
μmol/L  # U+03BC Greek small letter mu
µmol/L  # U+00B5 micro sign
```

must not cause a `UnitConversionError` when they represent the same clinical unit.

Required behaviour:

```text
μmol/L and µmol/L must resolve to the same canonical unit for conversion purposes.
```

The fix should be general enough for unit parsing, but must not silently alter unrelated units.

## Design requirements

The fix must:

```text
- be deterministic
- be centralised in the unit normalisation path
- preserve existing known-good unit conversions
- avoid special-casing urate only if a general unit-normalisation function exists or can be safely used
- not change biomarker thresholds or reference ranges
- not change canonical biomarker identity
```

If there is an existing unit normalisation helper, use it.

If no such helper exists, create the smallest safe helper in the unit registry module.

## Required tests

Add or update tests proving:

```text
1. urate with µmol/L still works
2. urate with μmol/L now works
3. μmol/L and µmol/L normalise to the same conversion key
4. unrelated units still behave unchanged
5. the six failing sentinel regression tests now pass
```

The launch audit identified six sentinel failures with the same root cause. Run the failing tests directly if their paths are present.

---

# Phase 4 — CB-4: Neutralise dev billing override risk

## Required remediation

In:

```text
backend/env.example
```

Remove, comment out, or clearly neutralise:

```text
HEALTHIQ_DISABLE_BILLING_ENFORCEMENT=1
HEALTHIQ_FREE_COMPLETED_ANALYSES=99
```

Preferred fix:

```text
Remove these enabled dev defaults from env.example and replace them with safe commented examples.
```

Example acceptable pattern:

```text
# Local development only. Do not enable in production.
# HEALTHIQ_DISABLE_BILLING_ENFORCEMENT=1
# HEALTHIQ_FREE_COMPLETED_ANALYSES=99
```

If a production-safe default is needed, use:

```text
HEALTHIQ_DISABLE_BILLING_ENFORCEMENT=0
HEALTHIQ_FREE_COMPLETED_ANALYSES=1
```

Do not change runtime billing code unless absolutely necessary.

## Required checks

Confirm:

```text
- env.example no longer enables billing bypass by default
- production deployment cannot accidentally inherit 99 free analyses from env.example without explicit override
```

---

# Phase 5 — Confirm forbidden areas unchanged

After remediation, verify that the following were not changed:

```text
knowledge_bus/packages/**/signal_library.yaml
backend/ssot/**
backend/core/analytics/signal_evaluator.py
backend/core/analytics/runtime_context_evaluator.py
backend/core/pipeline/orchestrator.py
backend/core/pipeline/orchestrator_phases_v1.py
backend/core/reporting/**
backend/core/scoring/**
frontend/app/components/clusters/ClusterInsightPanel.tsx
frontend/app/(app)/results/page.tsx
```

If any of these changed, STOP and explain why before proceeding.

---

# Phase 6 — Required validation

Run and paste full output.

## Architecture / governance validators

```powershell
python backend/scripts/run_architecture_validation_gate.py
python backend/scripts/validate_day_one_architecture.py
python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
python backend/scripts/validate_context_modifier_catalogue.py --catalogue knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
```

## Context safety regressions

```powershell
python -m pytest backend/tests/regression/test_runtime_context_evaluation.py -q
python -m pytest backend/tests/regression/test_context_threading.py -q
```

## Unit conversion tests

Run the existing unit registry / unit conversion tests.

Also run the six previously failing sentinel tests if present:

```powershell
python -m pytest tests/regression/test_lc_s5_proving_checks.py::test_check2_alcohol_bridge_language_when_moderate_threshold_met -q
python -m pytest tests/regression/test_obs2_questionnaire_exercise_unknown_regression.py::test_obs2_ab_baseline_vs_statin_off_consumer_bands_align -q
python -m pytest tests/regression/test_obs2_questionnaire_exercise_unknown_regression.py::test_obs2_ab_statin_off_vs_on_analytical_invariants -q
python -m pytest tests/regression/test_obs2_questionnaire_exercise_unknown_regression.py::test_obs2_vr_baseline_vs_statin_off_consumer_bands_align -q
python -m pytest tests/regression/test_obs2_questionnaire_exercise_unknown_regression.py::test_obs2_lifestyle_fixture_with_partial_questionnaire_completes -q
python -m pytest tests/regression/test_lc_s4_statin_signal_isolation_regression.py::test_statin_on_vs_off_preserves_scoring_body_overview_framing_only -q
```

If actual paths differ, discover and run the correct tests. Report the actual paths.

## Backend auth tests

Run affected backend route/auth tests.

If no route/auth tests exist, add targeted tests and run them.

## Frontend tests

Run the narrowest relevant frontend test command for `frontend/app/services/analysis.ts`.

If no existing test coverage exists, run TypeScript/lint checks if available and perform grep evidence proving sensitive console logging is removed.

## Sentinel

Run the sentinel or architecture gate command that produced the previous 54 passed / 6 failed result, if available.

The six Unicode mu failures must be resolved.

---

# Phase 7 — Required audit report

Create:

```text
docs/audit-papers/WAVE1-PUBLIC-LAUNCH-FIXES-1_pre_public_launch_blocker_remediation.md
```

The report must include:

```text
- executive verdict
- files inspected
- files changed
- CB-1 remediation evidence
- CB-2 remediation evidence
- CB-3 remediation evidence
- CB-4 remediation evidence
- confirmation no packages activated
- confirmation androgen packages remain inactive
- confirmation FT3 low remains inactive
- confirmation no clinical thresholds changed
- confirmation no reference range policy changed
- confirmation no signal IDs changed
- confirmation no activation keys changed
- confirmation no report compiler changed
- confirmation no scoring changed
- confirmation no SSOT changed
- confirmation no raw research runtime reads introduced
- full validator output
- full test output
- sentinel / regression output
- rollback path
- residual launch-readiness observations
- recommendation for next action
```

Validation and test output must be pasted in full, not summarised.

---

# Phase 8 — Launch readiness update

The audit report must conclude with one of:

```text
PUBLIC_LAUNCH_BLOCKERS_RESOLVED
PUBLIC_LAUNCH_BLOCKERS_PARTIALLY_RESOLVED
PUBLIC_LAUNCH_BLOCKERS_NOT_RESOLVED
INCONCLUSIVE_EVIDENCE_GAP
```

If not all blockers are resolved, state exactly which remain.

---

## Expected changed files

Expected changed files may include:

```text
frontend/app/services/analysis.ts
backend/app/routes/upload.py
backend/core/units/registry.py
backend/env.example

backend/tests/**/*
frontend/**/*test*
docs/audit-papers/WAVE1-PUBLIC-LAUNCH-FIXES-1_pre_public_launch_blocker_remediation.md
automation_bus/latest_cursor_status.json
```

No package files are expected to change.

No SSOT files are expected to change.

No orchestrator or signal evaluator files are expected to change.

---

## Forbidden changes

Do not change:

```text
knowledge_bus/packages/**
backend/ssot/**
backend/core/analytics/signal_evaluator.py
backend/core/analytics/runtime_context_evaluator.py
backend/core/pipeline/orchestrator.py
backend/core/pipeline/orchestrator_phases_v1.py
backend/core/reporting/**
backend/core/scoring/**
frontend/app/components/clusters/ClusterInsightPanel.tsx
frontend/app/(app)/results/page.tsx
```

Do not activate:

```text
- androgen packages
- FT3 low
- any inactive package
```

Do not introduce:

```text
- fallback parsers
- dummy parsers
- raw research runtime reads
- frontend clinical inference
- new LLM clinical reasoning
```

---

## STOP conditions

STOP and report if:

```text
1. the launch-readiness audit cannot be found
2. the four blockers cannot be confirmed or mapped to current files
3. fixing /api/upload/parse auth requires redesigning auth globally
4. unit registry fix requires changing biomarker reference ranges
5. unit registry fix requires changing clinical thresholds
6. removing PII console logging requires altering analysis payload shape
7. env.example remediation requires changing runtime billing code
8. any package activation is required
9. any androgen or FT3 low activation state changes
10. architecture validators fail
11. unit conversion tests still fail
12. parse auth tests fail
13. sensitive frontend console logging remains
14. sentinel still reports the Unicode mu defect
15. unexpected files change and cannot be justified
16. rollback path cannot be defined
```

If a STOP condition is triggered, do not perform ad hoc remediation beyond the approved scope.

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
fix(launch): remediate Wave 1 public launch blockers
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
- CB-1 PII console logging is removed
- CB-2 /api/upload/parse requires authentication
- CB-3 Unicode mu unit conversion defect is fixed
- CB-4 env.example no longer enables unsafe dev billing defaults
- the six previously failing sentinel tests pass
- architecture validators pass
- context package safety remains unchanged
- no packages are activated
- no clinical logic is changed
- no reference range policy is changed
- no frontend clinical inference is introduced
- no fallback parser is introduced
- audit paper is complete with full evidence
```

Expected next action after success:

```text
Run a short read-only Wave 1 launch-readiness re-check.
```

Do not proceed directly to public launch without confirming the four blockers are closed.
