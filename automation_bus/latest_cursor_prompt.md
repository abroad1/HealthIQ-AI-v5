---
work_id: KB-UTIL-2-PROMOTE-WIRE-1_creatinine_runtime_authority_switch
branch: work/KB-UTIL-2-PROMOTE-WIRE-1-creatinine-runtime-authority-switch
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
---

# KB-UTIL-2-PROMOTE-WIRE-1 — Creatinine Runtime Authority Switch

## Purpose

Decide whether the Pass_3-derived creatinine candidate can safely become the governed runtime authority for `signal_creatinine_high`.

This sprint must resolve the two remaining activation blockers from `KB-UTIL-2-ACTIVATION-READINESS`:

```text
1. Signal identity collision with pkg_kb52c_creatinine_high_reduced_glomerular_filtration.
2. Override-rule divergence between legacy eGFR/potassium escalation and Pass_3 UACR escalation.
````

The goal is not simply to “wire the new package”. The goal is to prove that HealthIQ can safely replace legacy runtime medical intelligence with Pass_3-derived intelligence through a controlled authority switch.

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
KB-UTIL-2-PILOT merged
KB-UTIL-2-PROMOTE-PILOT merged
KB-UTIL-2-ACTIVATION-READINESS merged
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
- promoted creatinine candidate is missing
- activation-readiness report is missing
- pass3_promotion_decision_register_v1.yaml is missing
```

## Required inputs

Read:

```text
docs/governance/KNOWLEDGE_BUS_SOP_v1.3.1.md
docs/governance/KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md
docs/audit-papers/KB-UTIL-2-ACTIVATION-READINESS_creatinine_candidate_divergence_and_collision_resolution_report.md
docs/audit-papers/KB-UTIL-2-PROMOTE-PILOT_route_a_single_package_promotion_report.md
docs/sprints/launch_core_carry_forward_register.md
knowledge_bus/governance/pass3_promotion_decision_register_v1.yaml
knowledge_bus/generated_pilot/kb_util_2_pilot/promoted_candidates/pkg_creatinine_high_renal_pass3_v1/
knowledge_bus/packages/pkg_s24_creatinine_high_renal/
knowledge_bus/packages/pkg_kb52c_creatinine_high_reduced_glomerular_filtration/
```

Also inspect as needed:

```text
SignalRegistry / signal loading code
Knowledge Bus package loading code
runtime authority manifests
backend/scripts/validate_knowledge_package.py
backend/scripts/validate_promoted_signal_intelligence.py
backend/scripts/validate_day_one_architecture.py
backend/tests/regression/
backend/tests/architecture/
```

If paths differ, locate and report actual paths.

## Mandatory preflight

Before making changes, produce a short authority preflight report covering:

```text
1. Which packages currently define signal_creatinine_high.
2. Which activation keys currently exist for signal_creatinine_high.
3. Whether pkg_s24_creatinine_high_renal is currently runtime-loaded.
4. Whether pkg_kb52c_creatinine_high_reduced_glomerular_filtration is currently runtime-loaded.
5. Whether the promoted Pass_3 candidate is currently runtime-loaded.
6. Whether duplicate activation keys already exist.
7. Which package should be treated as current runtime authority before this sprint.
8. What exact runtime authority switch is proposed.
```

STOP if the current runtime authority cannot be determined.

## Blocker 1 — Signal identity collision

Resolve or formally adjudicate the real collision:

```text
pkg_kb52c_creatinine_high_reduced_glomerular_filtration
signal_id: signal_creatinine_high
```

Required decision:

```text
A. Candidate supersedes pkg_kb52c.
B. Candidate supersedes pkg_s24 only, while pkg_kb52c remains separate.
C. Candidate cannot be activated because collision creates unsafe duplicate authority.
D. Candidate and pkg_kb52c are equivalent, and one should be retained as canonical.
```

Do not leave duplicate active runtime authority for the same activation identity.

If a package is superseded, do not delete it. Classify it as superseded/retained for traceability.

## Blocker 2 — Override-rule divergence

The divergence is currently classified as:

```text
BEHAVIOURAL_DIFFERENCE_LOW
accepted_with_rationale: false
```

Legacy rules:

```text
eGFR < 60 → at_risk
potassium > 5.2 → at_risk
```

Pass_3 candidate rule:

```text
UACR above_max via lab_range_boundary → at_risk
```

Required decision:

```text
A. Accept the Pass_3 UACR escalation as the correct replacement.
B. Retain eGFR/potassium escalation as additional runtime logic if supported by canonical research.
C. Block activation pending medical review.
```

Do not manually invent a hybrid rule.

If retaining eGFR/potassium is proposed, prove it comes from canonical research or explicitly classify it as legacy retained with rationale.

STOP if the divergence requires clinical adjudication beyond architecture.

## Activation policy

Runtime activation is allowed only if:

```text
- one canonical runtime authority is selected
- collision is resolved
- override divergence is accepted or resolved
- generated package validates
- promoted signal intelligence validates
- source-field preservation audit remains intact
- no raw Pass_3 runtime read is introduced
- legacy package is preserved unchanged
- rollback path is documented
```

If any condition fails, do not activate. Update registers and report blockers.

## Preferred implementation approach

Preferred safe method:

```text
1. Move or copy the promoted candidate from generated_pilot into a governed package directory.
2. Preserve generated_pilot copy as audit evidence.
3. Preserve legacy package directories unchanged.
4. Update package authority / manifest / registry only through governed controls.
5. Add tests proving only one active runtime authority for signal_creatinine_high.
```

Suggested governed package path:

```text
knowledge_bus/packages/pkg_creatinine_high_renal_pass3_v1/
```

Do not overwrite:

```text
knowledge_bus/packages/pkg_s24_creatinine_high_renal/
knowledge_bus/packages/pkg_kb52c_creatinine_high_reduced_glomerular_filtration/
```

## Runtime status

If activation proceeds, update runtime authority according to Knowledge Bus SOP v1.3.1.

If the repo uses:

```text
knowledge_bus/current/latest_knowledge_status.json
```

then update it only with validator PASS evidence.

If the repo uses another active package authority mechanism, locate it, document it, and use the existing governed path.

STOP if the authority mechanism is unclear.

## Required validation

Run:

```powershell
python backend/scripts/validate_knowledge_package.py --package-dir knowledge_bus/packages/pkg_creatinine_high_renal_pass3_v1
python backend/scripts/validate_promoted_signal_intelligence.py --file knowledge_bus/packages/pkg_creatinine_high_renal_pass3_v1/promoted_signal_intelligence.yaml
python backend/scripts/validate_day_one_architecture.py
python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q
python -m pytest backend/tests/regression/test_kb_util2_pass3_pilot_compiler.py -q
python -m pytest backend/tests/regression/test_kb_util2_promote_pilot.py -q
```

Add targeted regression tests proving:

```text
1. only one active runtime authority exists for signal_creatinine_high
2. legacy packages are not overwritten
3. promoted package validates
4. promoted signal intelligence validates
5. latest_knowledge_status.json or equivalent authority file is updated only after validation
6. raw Pass_3 files are not runtime-read
7. rollback path is documented
8. activation blockers are cleared or activation is refused
```

## Runtime boundary

Do not modify unless strictly necessary and justified:

```text
SignalEvaluator
frontend
SSOT
scoring thresholds
unit conversion
```

SignalRegistry / package authority loading may be inspected and modified only if required to resolve the activation-key collision.

If modifying SignalRegistry or loader behaviour, classify the exact behavioural impact and add regression coverage.

## Required deliverable

Create:

```text
docs/audit-papers/KB-UTIL-2-PROMOTE-WIRE-1_creatinine_runtime_authority_switch_report.md
```

Update:

```text
knowledge_bus/governance/pass3_promotion_decision_register_v1.yaml
docs/sprints/launch_core_carry_forward_register.md
```

If activation proceeds, also update the relevant package authority file.

## Required report content

The report must include:

```text
- executive verdict
- runtime authority preflight
- collision investigation and decision
- override divergence decision
- package promoted or activation refused
- package authority files changed
- legacy package treatment
- rollback path
- validation results
- tests added/updated
- whether runtime behaviour changed
- confirmation no frontend/SSOT/scoring changes
- remaining carry-forwards
- recommended next sprint
```

## Carry-forward register

Update:

```text
docs/sprints/launch_core_carry_forward_register.md
```

If activation succeeds, mark the creatinine-specific blocker resolved.

If activation is refused, record the exact blocker:

```text
- collision unresolved
- override divergence not accepted
- runtime authority mechanism unclear
- validator failure
- clinical adjudication required
```

Do not mark broad ROUTE_A migration resolved from this single package.

## Out of scope

Do not:

```text
- bulk promote ROUTE_A packages
- promote CRP/systemic inflammation
- resolve ROUTE_C multi-frame adjudication
- delete legacy packages
- manually invent clinical rules
- change frontend
- implement root-cause replacement
- implement card evidence runtime consumption
- implement LLM narrative generation
```

## STOP conditions

STOP and report if:

```text
1. runtime authority mechanism cannot be determined
2. duplicate activation authority cannot be safely resolved
3. override divergence requires clinical adjudication
4. SignalRegistry changes would create broader behavioural risk
5. package validation fails
6. promoted signal intelligence validation fails
7. rollback path cannot be defined
8. activation would require frontend/scoring/SSOT changes
9. ARCH-RT validator fails
```

## Evidence required from Cursor

Cursor must report:

```text
1. baseline branch/status evidence
2. governance inputs read
3. authority preflight findings
4. collision decision
5. override divergence decision
6. promoted package path or activation refusal
7. authority file changes
8. tests added/updated
9. validation commands run
10. validation results
11. rollback path
12. files changed
13. confirmation no frontend/SSOT/scoring changes
```

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
- current branch matches work/KB-UTIL-2-PROMOTE-WIRE-1-creatinine-runtime-authority-switch
- only in-scope files changed
- no legacy package was overwritten
- no duplicate active authority remains if activation proceeds
- rollback path is documented
- no ambiguous stash exists
- validator evidence is recorded
```

## Success criteria

This sprint is complete only if:

```text
1. creatinine runtime authority is clearly determined
2. pkg_kb52c collision is resolved or activation is refused
3. override divergence is accepted, resolved, or activation is refused
4. no duplicate active authority remains
5. promoted package validates
6. promoted signal intelligence validates
7. legacy packages are preserved
8. rollback path exists
9. no frontend/SSOT/scoring changes are made
10. carry-forward register is accurate
```

```
```
