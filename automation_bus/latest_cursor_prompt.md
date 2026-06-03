---
work_id: ARCH-SENTINEL-1_medical_intelligence_architecture_guardrails
branch: work/ARCH-SENTINEL-1-medical-intelligence-architecture-guardrails
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# ARCH-SENTINEL-1 — Medical Intelligence Architecture Guardrails

## Purpose

Create sentinel tests and validation checks that protect the new HealthIQ medical-intelligence architecture from regression.

This sprint must ensure future work cannot quietly compromise the architecture by:

```text
- reading raw Pass_3 files at runtime
- treating draft/governance artefacts as runtime authority
- collapsing multiple medical frames into one flat signal
- introducing duplicate active activation keys
- allowing frontend medical inference
- bypassing frame-coverage safety gates during package promotion
- retiring legacy edge-case logic without adjudication
- using governance helper scripts to mutate runtime/package/frontend files
````

This is a guardrail sprint, not a feature sprint.

Do not change medical logic, runtime scoring, frontend behaviour, package activation, or user-facing output.

---

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
PASS3-FRAME-COVERAGE-1 merged
PASS3-FRAME-INDEX-2 merged
KB-UTIL-2-CREATININE-AUTHORITY-ADJUDICATION merged
MED-FRAME-2 merged
CONTEXT-MOD-1 merged
KNOWLEDGE_BUS_SOP_v1.3.1 committed
KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1 committed
```

Before starting, run and report:

```powershell
git branch --show-current
git status --short
git log --oneline -n 12
git rev-parse HEAD
git rev-parse origin/main
```

STOP if:

```text
- current branch is not main
- local main does not equal origin/main
- working tree is not clean
- medical_frame_identity_index_v1.yaml is missing
- context_modifier_catalogue_draft_v1.yaml is missing
- pass3_frame_coverage_audit_v1.yaml is missing
- governance helper README is missing
```

---

## Governance classification

```yaml
risk_level: HIGH
change_type: MIXED
execution_model: TWO_PHASE_START_FINISH
```

Reason:

This sprint adds architecture-protection tooling/tests. It should not change runtime behaviour, but it protects medical-intelligence authority boundaries.

---

## Required inputs

Read before implementation:

```text
docs/governance/KNOWLEDGE_BUS_SOP_v1.3.1.md
docs/governance/KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md
docs/architecture/MED-FRAME-1_signal_family_contextual_frame_architecture.md
docs/audit-papers/MED-FRAME-2_medical_frame_identity_index_report.md
docs/architecture/CONTEXT-MOD-1_questionnaire_and_medication_modifier_governance.md
docs/audit-papers/PASS3-FRAME-COVERAGE-1_estate_wide_multiframe_research_coverage_audit.md
docs/audit-papers/PASS3-FRAME-INDEX-2_high_risk_signal_family_index_expansion_report.md
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
knowledge_bus/governance/pass3_frame_coverage_audit_v1.yaml
knowledge_bus/governance/medical_frame_identity_expansion_candidates_v1.yaml
knowledge_bus/tools/README_governance_helpers.md
docs/sprints/launch_core_carry_forward_register.md
```

Also inspect existing tests:

```text
backend/scripts/validate_day_one_architecture.py
backend/tests/architecture/test_day_one_architecture_guardrails.py
backend/scripts/validate_medical_frame_identity_index.py
backend/tests/regression/test_med_frame_identity_index.py
backend/scripts/validate_context_modifier_catalogue.py
backend/tests/regression/test_context_modifier_catalogue.py
backend/tests/regression/test_kb_util2_pass3_pilot_compiler.py
backend/tests/regression/test_kb_util2_promote_pilot.py
```

If paths differ, locate and report actual paths.

---

## Required guardrail areas

Create or extend sentinel coverage for the following.

### 1. No raw Pass_3 runtime reads

Runtime code must not read directly from:

```text
knowledge_bus/research/investigation_specs/
*_Pass_3.json
*_pass_3.json
```

Allowed:

```text
- governance tools
- validators
- compiler scripts
- audit builders
- tests
```

Forbidden:

```text
- SignalEvaluator
- SignalRegistry
- runtime loaders
- report compiler
- domain score assembler
- frontend
```

### 2. Non-runtime governance artefacts remain non-runtime

The following must not be runtime-consumed:

```text
medical_frame_identity_index_v1.yaml
context_modifier_catalogue_draft_v1.yaml
pass3_frame_coverage_audit_v1.yaml
medical_frame_identity_expansion_candidates_v1.yaml
creatinine_multiframe_authority_decision_v1.yaml
```

Sentinel checks must confirm they are not imported/read by runtime code.

### 3. No duplicate active frame authority

Existing medical frame identity validator already blocks duplicate active activation keys.

This sprint must add a higher-level sentinel or regression check proving:

```text
- duplicate active activation_key remains forbidden
- compiled_not_promoted collisions are allowed only when explicitly classified
- runtime_active_legacy_unadjudicated frames remain clearly marked
```

### 4. No frontend medical inference

Frontend must remain render-only.

Sentinel tests should guard against frontend code importing or hardcoding medical intelligence sources, including:

```text
Pass_3
medical frame index
context modifier catalogue
package signal libraries
clinical thresholds
diagnostic/escalation logic
```

If existing day-one guardrails already cover part of this, extend or document the coverage.

### 5. Package promotion blocked by frame-coverage safety

Future promotion work must not treat ROUTE_A as automatically safe.

Add a sentinel check over:

```text
knowledge_bus/governance/pass3_frame_coverage_audit_v1.yaml
```

that confirms any package with:

```text
promotion_safety_status:
  - blocked_pending_frame_adjudication
  - blocked_pending_pass3_enrichment
  - blocked_pending_provenance_recovery
```

cannot be listed as safe for promotion without an explicit override/decision artefact.

Do not implement actual promotion logic.

This is a guardrail over governance state.

### 6. Legacy edge-case logic must not be silently retired

Sentinel must check that high-risk known legacy frames remain represented in governance.

At minimum confirm:

```text
- creatinine s24 eGFR frame still exists in medical_frame_identity_index_v1.yaml
- creatinine s24 potassium frame still exists in medical_frame_identity_index_v1.yaml
- both remain unadjudicated / blocked pending medical review or enrichment
```

Do not adjudicate them.

### 7. Governance helper script boundary

Add a sentinel or test ensuring governance helper scripts under:

```text
knowledge_bus/tools/
```

and any existing governance helper under:

```text
backend/scripts/build_pass3_frame_coverage_audit.py
```

do not import runtime/evaluator/frontend modules and do not write to runtime/package/frontend paths.

---

## Required artefacts

Create or update:

```text
backend/tests/architecture/test_medical_intelligence_architecture_sentinels.py
docs/audit-papers/ARCH-SENTINEL-1_medical_intelligence_architecture_guardrails_report.md
```

Update if needed:

```text
backend/scripts/validate_day_one_architecture.py
docs/sprints/launch_core_carry_forward_register.md
```

Optional, only if useful and justified:

```text
backend/scripts/validate_medical_intelligence_architecture.py
```

If creating a new validator, keep it independent and non-runtime.

---

## Required report content

The report must include:

```text
- executive verdict
- files inspected
- sentinel checks added
- existing guardrails reused
- raw Pass_3 runtime-read protection
- non-runtime governance artefact protection
- duplicate active authority protection
- frontend render-only protection
- promotion safety gate protection
- legacy edge-case preservation checks
- governance helper boundary checks
- validation output pasted in full
- carry-forward updates
- remaining limitations
- recommended next sprint
```

---

## Runtime boundary

Do not modify:

```text
SignalEvaluator
SignalRegistry
runtime loaders
domain_score_assembler
report_compiler
frontend behaviour
SSOT
scoring thresholds
unit conversion
knowledge_bus/packages/*
knowledge_bus/current/latest_knowledge_status.json
```

Do not alter emitted analysis.

If a sentinel requires runtime code changes to pass, STOP and report the architectural gap.

---

## Carry-forward handling

Update:

```text
docs/sprints/launch_core_carry_forward_register.md
```

Expected handling:

```text
CF-PASS3FRAME-003
May be updated to reference the new sentinel coverage, but should remain open unless promotion pause logic is fully governed.

CF-GOVHELPER-001
Should already be resolved. Confirm the new sentinel reinforces it.

Possible new carry-forward:
CF-SENTINEL-001 — integrate medical-intelligence sentinel checks into the standard Automation Bus / CI gate if not already wired.
```

Do not mark package promotion, Pass_3 enrichment, or context-modifier runtime binding as resolved.

---

## Required validations

Run and paste actual output:

```powershell
python backend/scripts/validate_medical_frame_identity_index.py --index knowledge_bus/governance/medical_frame_identity_index_v1.yaml
python backend/scripts/validate_context_modifier_catalogue.py --catalogue knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml
python backend/scripts/validate_day_one_architecture.py
python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q
python -m pytest backend/tests/architecture/test_medical_intelligence_architecture_sentinels.py -q
python -m pytest backend/tests/regression/test_med_frame_identity_index.py -q
python -m pytest backend/tests/regression/test_context_modifier_catalogue.py -q
```

If a new validator is created, run it too.

Do not write only “see implementation evidence”.

---

## Out of scope

Do not:

```text
- promote packages
- activate packages
- enrich Pass_3 specs
- change runtime loaders
- change evaluator logic
- change frontend
- modify package files
- implement Layer B frame assembly
- implement context modifier evaluation
- create the human-readable biomarker tree
```

---

## STOP conditions

STOP and report if:

```text
1. sentinel checks reveal runtime reads of raw Pass_3 files
2. frontend currently imports medical-intelligence sources
3. governance artefacts are already runtime-consumed
4. duplicate active activation keys exist
5. creatinine legacy eGFR/potassium frames are missing
6. governance helper scripts write to runtime/package/frontend paths
7. any required sentinel would need runtime behaviour changes
8. validators fail
```

---

## Evidence required from Cursor

Cursor must report:

```text
1. baseline branch/status evidence
2. files inspected
3. sentinel tests added
4. existing guardrails reused
5. validation commands run
6. actual validation output
7. carry-forward updates
8. confirmation no runtime/package/frontend changes
9. confirmation no emitted reasoning changes
```

---

## Closure requirements

Before finish, run and report:

```powershell
git branch --show-current
git status --short
git log --oneline -n 5
git diff --name-only
git diff --cached --name-only
git stash list
```

Do not run finish unless:

```text
- current branch matches work/ARCH-SENTINEL-1-medical-intelligence-architecture-guardrails
- only in-scope tests/scripts/docs/register files changed
- no runtime package files changed
- no frontend/runtime evaluator files changed
- no ambiguous stash exists
- validators and sentinel tests pass
```

---

## Success criteria

This sprint is complete only if:

```text
1. sentinel tests protect against raw Pass_3 runtime reads
2. sentinel tests protect non-runtime governance artefacts from runtime consumption
3. duplicate active frame authority remains protected
4. frontend render-only boundary is protected
5. promotion safety status is guarded
6. creatinine legacy eGFR/potassium frames are protected from silent loss
7. governance helper script boundaries are tested or documented
8. no runtime/package/frontend behaviour changes occur
9. actual validator output is pasted
10. all tests pass
```

```
```
