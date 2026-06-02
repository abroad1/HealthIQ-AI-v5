---
work_id: KB-UTIL-2-ACTIVATION-READINESS_creatinine_candidate_divergence_and_collision_resolution
branch: work/KB-UTIL-2-ACTIVATION-READINESS-creatinine-candidate-divergence-and-collision-resolution
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# KB-UTIL-2-ACTIVATION-READINESS — Creatinine Candidate Divergence and Collision Resolution

## Purpose

Resolve the mandatory activation-readiness advisories from `KB-UTIL-2-PROMOTE-PILOT` before any runtime wiring or activation is considered.

This sprint must not activate the promoted package.

The goal is to determine whether the promoted Pass_3-derived creatinine candidate is safe and correctly documented as a future runtime authority candidate.

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
KB-UTIL-2-PILOT merged
KB-UTIL-2-PROMOTE-PILOT merged
KNOWLEDGE_BUS_SOP_v1.3.1 committed
KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1 committed
````

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
- promoted creatinine candidate directory is missing
- KB-UTIL-2-PROMOTE-PILOT report is missing
```

## Required inputs

Read:

```text
docs/audit-papers/KB-UTIL-2-PROMOTE-PILOT_route_a_single_package_promotion_report.md
docs/sprints/launch_core_carry_forward_register.md
knowledge_bus/governance/pass3_promotion_decision_register_v1.yaml
knowledge_bus/governance/pass3_pilot_compile_manifest_index_v1.yaml
knowledge_bus/generated_pilot/kb_util_2_pilot/promoted_candidates/pkg_creatinine_high_renal_pass3_v1/
knowledge_bus/packages/pkg_s24_creatinine_high_renal/
```

Also inspect as needed:

```text
backend/scripts/compile_pass3_pilot_artifacts.py
backend/tests/regression/test_kb_util2_promote_pilot.py
backend/tests/regression/test_kb_util2_pass3_pilot_compiler.py
backend/scripts/validate_knowledge_package.py
backend/scripts/validate_promoted_signal_intelligence.py
```

## Mandatory issues to resolve

### Issue 1 — Override-rule divergence classification

The audit found that the divergence was incorrectly classified as:

```text
RICHNESS_GAIN_ONLY
```

Correct classification should be:

```text
BEHAVIOURAL_DIFFERENCE_LOW
```

Reason:

```text
Legacy package includes escalation rules using eGFR and potassium.
Generated Pass_3 candidate uses UACR-based escalation.
This is a rule substitution, not merely extra richness.
```

Required action:

```text
- update pass3_promotion_decision_register_v1.yaml
- update sprint/report documentation if needed
- explicitly classify the candidate as not ready for runtime activation until divergence is accepted or resolved
```

Do not alter the clinical logic in this sprint.

### Issue 2 — `pkg_kb52c` activation-key collision

The promoted candidate manifest references:

```text
duplicate_activation_key_collision_with_pkg_kb52c
```

Required action:

```text
- identify what pkg_kb52c is
- determine whether it exists in the repo
- determine whether the activation-key collision is real
- explain why it was not in the 55-package mapping plan if applicable
- classify the collision as real, stale, mistaken, or unresolved
- update the manifest/report/register accordingly
```

STOP if the collision implies a broader SignalRegistry identity problem that cannot be resolved in this sprint.

### Issue 3 — Incorrect `output_root`

The promoted candidate compile manifest points to the original generated location instead of the promoted candidate location.

Required action:

```text
- correct output_root in the promoted candidate compile_manifest.yaml
- update compiler/promotion logic so future promoted candidates do not inherit stale output_root
- add or update regression test
```

### Issue 4 — No-op legacy non-overwrite test

The existing test compares a hash to itself.

Required action:

```text
- replace with a meaningful test
- prove the legacy package was not overwritten
- use a committed fixture hash, known baseline content assertion, or equivalent robust check
```

### Issue 5 — Missing explicit boundary regression coverage

The audit noted not all required checks were explicitly covered.

Required action:

Add or extend tests proving:

```text
- no raw Pass_3 runtime read was introduced
- no runtime evaluator/frontend files changed or required
- promoted candidate remains non-runtime
- latest_knowledge_status.json is not created or modified
```

## Scope

Allowed:

```text
- update governance decision register
- update compile manifest for promoted candidate
- update compiler/promotion script so future output_root is correct
- update tests
- update sprint report/addendum
- update carry-forward register
```

Forbidden:

```text
- runtime activation
- updating latest_knowledge_status.json
- modifying SignalEvaluator
- modifying SignalRegistry
- modifying runtime loaders
- modifying frontend
- modifying scoring thresholds
- modifying SSOT
- overwriting legacy package
- manually changing clinical rule logic
```

## Required validation

Run:

```powershell
python backend/scripts/validate_knowledge_package.py --package-dir knowledge_bus/generated_pilot/kb_util_2_pilot/promoted_candidates/pkg_creatinine_high_renal_pass3_v1
python backend/scripts/validate_promoted_signal_intelligence.py --file knowledge_bus/generated_pilot/kb_util_2_pilot/promoted_candidates/pkg_creatinine_high_renal_pass3_v1/promoted_signal_intelligence.yaml
python backend/scripts/validate_day_one_architecture.py
python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q
python -m pytest backend/tests/regression/test_kb_util2_pass3_pilot_compiler.py -q
python -m pytest backend/tests/regression/test_kb_util2_promote_pilot.py -q
```

## Required deliverable

Create:

```text
docs/audit-papers/KB-UTIL-2-ACTIVATION-READINESS_creatinine_candidate_divergence_and_collision_resolution_report.md
```

Report must include:

```text
- executive verdict
- Issue 1 resolution
- Issue 2 collision investigation
- Issue 3 output_root fix
- Issue 4 test correction
- Issue 5 boundary test coverage
- files changed
- validation results
- whether candidate remains compiled_not_promoted
- whether future runtime activation is allowed, blocked, or conditional
- remaining carry-forwards
```

## Carry-forward register

Update:

```text
docs/sprints/launch_core_carry_forward_register.md
```

Only mark items resolved if actually resolved.

If future runtime activation remains conditional, add the exact blocker.

## STOP conditions

STOP and report if:

```text
- pkg_kb52c collision cannot be understood
- divergence appears clinically significant beyond BEHAVIOURAL_DIFFERENCE_LOW
- resolving the collision requires SignalRegistry/runtime changes
- output_root correction would require regenerating active runtime packages
- tests fail
- any runtime activation becomes necessary
```

## Success criteria

This sprint is complete only if:

```text
1. divergence classification is corrected
2. pkg_kb52c collision is explained or carried forward with exact blocker
3. promoted candidate output_root is corrected
4. legacy non-overwrite test is meaningful
5. explicit boundary tests are added
6. promoted candidate still validates
7. promoted signal intelligence still validates
8. candidate remains non-runtime / compiled_not_promoted
9. no runtime/frontend/evaluator behaviour changes
10. carry-forward register is accurate
```

```
```
