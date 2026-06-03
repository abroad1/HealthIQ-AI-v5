---
work_id: CI-ARCH-GATE-1A_architecture_gate_pythonpath_followup
branch: work/CI-ARCH-GATE-1A-architecture-gate-pythonpath-followup
risk_level: STANDARD
execution_model: TWO_PHASE_START_FINISH
change_type: INFRA
---

# CI-ARCH-GATE-1A — Architecture Gate PYTHONPATH Follow-up

## Purpose

Apply the small CI hardening amendment missed after `CI-ARCH-GATE-1`.

`CI-ARCH-GATE-1` successfully wired the medical-intelligence architecture gate into local and CI validation, but the new GitHub workflow omitted the same `PYTHONPATH: backend` environment setting used by existing validation workflows.

This sprint must add that setting and re-run the architecture gate.

This is a follow-up infrastructure hygiene sprint only.

Do not change medical logic, runtime behaviour, package artefacts, frontend, SSOT, SignalEvaluator, SignalRegistry, or governance models.

---

## Baseline requirement

Start from clean `main`.

Expected prior completed work:

```text
CI-ARCH-GATE-1 merged
ARCH-SENTINEL-1 merged
```

Before starting, run and report:

```powershell
git branch --show-current
git status --short
git log --oneline -n 8
git rev-parse HEAD
git rev-parse origin/main
```

STOP if:

```text
- current branch is not main
- local main does not equal origin/main
- working tree is not clean
- .github/workflows/architecture-gate.yml is missing
- backend/scripts/run_architecture_validation_gate.py is missing
```

---

## Required change

Update:

```text
.github/workflows/architecture-gate.yml
```

Add workflow-level or job-level environment setting:

```yaml
env:
  PYTHONPATH: backend
```

Match the existing pattern used by other repo workflows such as:

```text
.github/workflows/validate.yml
.github/workflows/golden_gate.yml
```

Use the smallest safe diff.

---

## Required validations

Run and paste actual output:

```powershell
python backend/scripts/run_architecture_validation_gate.py
python backend/scripts/validate_medical_intelligence_architecture.py
python backend/scripts/validate_day_one_architecture.py
python -m pytest backend/tests/architecture/test_medical_intelligence_architecture_sentinels.py -q
python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q
```

---

## Required report

Create:

```text
docs/audit-papers/CI-ARCH-GATE-1A_architecture_gate_pythonpath_followup_report.md
```

---

## Runtime boundary

Do not modify runtime, packages, frontend, or governance models.

---

## Success criteria

```text
1. architecture-gate.yml sets PYTHONPATH: backend
2. architecture gate passes locally
3. validators and sentinel pytest pass
4. no runtime/package/frontend/governance model changes
```
