# CI-ARCH-GATE-1A — Architecture Gate PYTHONPATH Follow-up Report

**Work ID:** `CI-ARCH-GATE-1A_architecture_gate_pythonpath_followup`  
**Date:** 2026-06-02  
**SOP:** AUTOMATION_BUS_SOP_v1.3.1

---

## Executive verdict

**PASS (infra only).** Added `PYTHONPATH: backend` to `.github/workflows/architecture-gate.yml` job `env`, matching `golden_gate.yml`. Local architecture gate and validators pass. No runtime, package, frontend, or governance model changes.

---

## Workflow files inspected

| Workflow | PYTHONPATH setting |
|----------|-------------------|
| `validate.yml` | `PYTHONPATH: ${{ github.workspace }}/backend` (job-level `env`) |
| `golden_gate.yml` | `PYTHONPATH: backend` (job-level `env`) |
| `architecture-gate.yml` (before) | **Missing** — only `PYTHONUNBUFFERED` |
| `architecture-gate.yml` (after) | `PYTHONPATH: backend` on job `architecture-gate` |

**Placement decision:** Job-level `env` on `architecture-gate`, same block as `PYTHONUNBUFFERED`, using literal `backend` like `golden_gate.yml` (repo-root working directory for gate script).

---

## Files changed

| File | Change |
|------|--------|
| `.github/workflows/architecture-gate.yml` | Add `PYTHONPATH: backend` |

---

## Runtime boundary confirmation

No changes to `backend/core/`, packages, frontend, governance YAML models, or evaluators.

---

## Carry-forward

**CF-SENTINEL-001** remains **Resolved**. Note: CI-ARCH-GATE-1A completed workflow PYTHONPATH hardening for `architecture-gate.yml`.

---

## Remaining limitations

None for this follow-up. Duplicate validator steps in `run_architecture_validation_gate.py` intentionally unchanged per sprint scope.

---

## Validation output (actual)

```text
python backend/scripts/run_architecture_validation_gate.py
[architecture-gate] validate_medical_frame_identity_index
validation_status: PASS
[architecture-gate] validate_context_modifier_catalogue
validation_status: PASS
[architecture-gate] validate_day_one_architecture
day_one_architecture_validation: PASS
[architecture-gate] validate_medical_intelligence_architecture
medical_intelligence_architecture_validation: PASS
[architecture-gate] pytest_architecture_guardrails
.......s..
[architecture-gate] pytest_governance_regression
..................... 
architecture_validation_gate: PASS

python backend/scripts/validate_medical_intelligence_architecture.py
medical_intelligence_architecture_validation: PASS

python backend/scripts/validate_day_one_architecture.py
day_one_architecture_validation: PASS

python -m pytest backend/tests/architecture/test_medical_intelligence_architecture_sentinels.py -q
......

python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q
....
```
