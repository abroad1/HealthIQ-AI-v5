---
work_id: CI-ARCH-GATE-1_medical_intelligence_architecture_ci_gate
branch: work/CI-ARCH-GATE-1-medical-intelligence-architecture-ci-gate
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# CI-ARCH-GATE-1 — Medical Intelligence Architecture CI Gate

## Purpose

Integrate the new medical-intelligence architecture guardrails into the standard validation / CI pathway so they run automatically, not only when called manually.

This sprint must make the protections from `ARCH-SENTINEL-1` part of the normal architecture gate.

The goal is to ensure future work cannot accidentally compromise the new architecture by bypassing:

```text
- medical frame identity validation
- context modifier catalogue validation
- medical-intelligence architecture sentinels
- raw Pass_3 runtime-read protection
- frontend render-only protection
- promotion safety gating
- governance helper script boundary checks
````

Do not change runtime behaviour.

---

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
ARCH-SENTINEL-1 merged
PASS3-FRAME-INDEX-2 merged
PASS3-FRAME-COVERAGE-1 merged
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
- ARCH-SENTINEL-1 is not merged
- validate_medical_intelligence_architecture.py is missing
- test_medical_intelligence_architecture_sentinels.py is missing
```

---

## Governance classification

```yaml
risk_level: HIGH
change_type: MIXED
execution_model: TWO_PHASE_START_FINISH
```

Reason:

This sprint modifies validation / CI / Automation Bus gate behaviour. It must not affect runtime output, but it affects how future architecture work is blocked or allowed.

---

## Required inputs

Read before implementation:

```text
docs/audit-papers/ARCH-SENTINEL-1_medical_intelligence_architecture_guardrails_report.md
backend/scripts/validate_medical_intelligence_architecture.py
backend/scripts/validate_day_one_architecture.py
backend/tests/architecture/test_medical_intelligence_architecture_sentinels.py
backend/tests/architecture/test_day_one_architecture_guardrails.py
docs/sprints/launch_core_carry_forward_register.md
docs/governance/KNOWLEDGE_BUS_SOP_v1.3.1.md
docs/governance/KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md
```

Also inspect current validation / CI / Automation Bus entry points:

```text
.github/workflows/**
automation_bus/**
backend/scripts/run_work_package.py
backend/scripts/golden_gate_local.py
backend/scripts/update_cursor_status.py
backend/scripts/validate_day_one_architecture.py
package.json
pyproject.toml
pytest.ini
```

If paths differ, locate and report actual paths.

---

## Core requirement

The new sentinel validator must become part of the standard architecture validation profile.

At minimum, the following must run as part of the standard architecture gate:

```powershell
python backend/scripts/validate_medical_intelligence_architecture.py
python -m pytest backend/tests/architecture/test_medical_intelligence_architecture_sentinels.py -q
```

Prefer integration through the existing architecture validation path, not a separate forgotten command.

---

## Required investigation

Before editing, report:

```text
1. Current standard validation commands.
2. Which scripts/workflows currently call validate_day_one_architecture.py.
3. Whether validate_day_one_architecture.py already delegates to validate_medical_intelligence_architecture.py.
4. Whether pytest architecture tests already include the new sentinel module.
5. Where CI / local gates are defined.
6. What minimal integration is needed.
```

STOP if the standard gate entry point cannot be determined.

---

## Required implementation

Implement the smallest safe change that ensures the medical-intelligence sentinel checks run automatically.

Allowed changes may include:

```text
- CI workflow update
- architecture validation script update
- local gate script update
- pytest collection/gate update
- documentation/report update
- carry-forward register update
```

Do not duplicate validation logic unnecessarily.

Do not create a parallel validation pathway that future agents may forget.

---

## Carry-forward items to resolve

This sprint must address:

```text
CF-SENTINEL-001
Wire validate_medical_intelligence_architecture.py and test_medical_intelligence_architecture_sentinels.py into the standard CI / Automation Bus gate.
```

Also address the two non-blocking ARCH-SENTINEL-1 clean-up items if safe:

```text
1. Remove the dead condition in validate_promotion_safety_gate.
2. Expand pytest coverage so all 5 non-runtime governance artefacts are checked, not only 3.
```

Do not let these clean-up items distract from the primary CI/gate integration.

---

## Required tests / validations

Run and paste actual output:

```powershell
python backend/scripts/validate_medical_intelligence_architecture.py
python backend/scripts/validate_day_one_architecture.py
python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q
python -m pytest backend/tests/architecture/test_medical_intelligence_architecture_sentinels.py -q
python -m pytest backend/tests/regression/test_med_frame_identity_index.py -q
python -m pytest backend/tests/regression/test_context_modifier_catalogue.py -q
```

If there is a CI/local gate command, run it too and paste the output.

Do not write only “all tests passed”.

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

If integration requires runtime changes, STOP and report.

---

## Required artefacts

Create:

```text
docs/audit-papers/CI-ARCH-GATE-1_medical_intelligence_architecture_ci_gate_report.md
```

Update as needed:

```text
docs/sprints/launch_core_carry_forward_register.md
```

Possible files to update if confirmed as the right gate path:

```text
.github/workflows/*
backend/scripts/validate_day_one_architecture.py
backend/tests/architecture/test_medical_intelligence_architecture_sentinels.py
backend/scripts/validate_medical_intelligence_architecture.py
automation_bus/*
```

Only touch Automation Bus files if they are definitely the correct validation integration point.

---

## Required report content

The report must include:

```text
- executive verdict
- current gate/CI entry points inspected
- integration decision
- files changed
- sentinel checks now included in standard gate
- ARCH-SENTINEL-1 clean-up items addressed
- validation output pasted in full
- runtime boundary confirmation
- carry-forward updates
- remaining limitations
- recommended next sprint
```

---

## STOP conditions

STOP and report if:

```text
1. standard CI/gate entry point cannot be identified
2. integration would require runtime code changes
3. integration would weaken existing day-one validation
4. medical-intelligence validator fails
5. day-one validator fails
6. sentinel pytest fails
7. Automation Bus changes are required but unsafe to make in this sprint
```

---

## Evidence required from Cursor

Cursor must report:

```text
1. baseline branch/status evidence
2. files inspected
3. gate/CI entry point findings
4. files changed
5. validation commands run
6. actual validation output
7. carry-forward updates
8. confirmation no runtime/package/frontend changes
9. confirmation CF-SENTINEL-001 status
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
- current branch matches work/CI-ARCH-GATE-1-medical-intelligence-architecture-ci-gate
- only in-scope validation/CI/test/docs/register files changed
- no runtime package files changed
- no frontend/runtime evaluator files changed
- no ambiguous stash exists
- validators and sentinel tests pass
```

---

## Success criteria

This sprint is complete only if:

```text
1. medical-intelligence validator is included in the standard architecture validation path
2. medical-intelligence sentinel pytest is included in the standard architecture test path or CI profile
3. existing day-one validation is not weakened
4. ARCH-SENTINEL-1 clean-up items are resolved or explicitly carried forward
5. CF-SENTINEL-001 is resolved only if gate integration is complete
6. no runtime/package/frontend behaviour changes occur
7. actual validator outputs are pasted
8. all required tests pass
```

```
```
