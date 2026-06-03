# CI-ARCH-GATE-1 — Medical Intelligence Architecture CI Gate Report

**Work ID:** `CI-ARCH-GATE-1_medical_intelligence_architecture_ci_gate`  
**Date:** 2026-06-02  
**SOP:** AUTOMATION_BUS_SOP_v1.3.1

---

## Executive verdict

**PASS (validation/CI only).** Medical-intelligence architecture checks are wired into the standard architecture gate (`run_architecture_validation_gate.py`), Automation Bus `golden_gate_local.py` (first check), and GitHub `architecture-gate.yml` on `main`/`develop`. **CF-SENTINEL-001 resolved.** ARCH-SENTINEL-1 clean-up items addressed. No runtime behaviour changes.

---

## Gate / CI entry points inspected

| Entry point | Role before sprint | After sprint |
|-------------|-------------------|--------------|
| `backend/scripts/golden_gate_local.py` | Baseline tests + three-layer pipeline only | **+** `run_architecture_validation_gate.py` (first check) |
| `backend/scripts/run_work_package.py finish` | Invokes golden gate | Unchanged; inherits new gate checks |
| `.github/workflows/ci.yml` | Unit tests, lint, security | Unchanged (no architecture overlap) |
| `.github/workflows/golden_gate.yml` | Golden panel on legacy branch | Unchanged |
| `.github/workflows/validate.yml` | Nightly `run_all_tests.py` | Unchanged |
| `validate_day_one_architecture.py` | Day-one guardrails | Already delegates to medical-intelligence validator (ARCH-SENTINEL-1) |

---

## Integration decision

Single canonical gate script avoids a parallel forgotten pathway:

- **`backend/scripts/run_architecture_validation_gate.py`** — ordered validators + architecture/regression pytest
- **`golden_gate_local.py`** — calls gate before baseline tests (Automation Bus finish requirement)
- **`.github/workflows/architecture-gate.yml`** — PR/push gate on `main` and `develop`
- **`sentinel/packs/medical_intelligence_architecture_guardrails_v1.json`** — documents validator + gate script

Day-one validation is **not weakened**; medical-intelligence checks run both via day-one delegation and explicit gate step (idempotent, fast).

---

## Files changed

| File | Change |
|------|--------|
| `backend/scripts/run_architecture_validation_gate.py` | **New** standard architecture gate |
| `backend/scripts/golden_gate_local.py` | First check = architecture gate |
| `.github/workflows/architecture-gate.yml` | **New** CI job |
| `sentinel/packs/medical_intelligence_architecture_guardrails_v1.json` | **New** sentinel pack metadata |
| `backend/scripts/validate_medical_intelligence_architecture.py` | Remove dead promotion-safety branch |
| `backend/tests/architecture/test_medical_intelligence_architecture_sentinels.py` | 5 governance artefacts; gate/pack tests; skip nested gate under `ARCHITECTURE_GATE_CHILD` |
| `docs/sprints/launch_core_carry_forward_register.md` | CF-SENTINEL-001 resolved |

---

## Sentinel checks now in standard gate

- `validate_medical_frame_identity_index.py`
- `validate_context_modifier_catalogue.py`
- `validate_day_one_architecture.py` (includes medical-intelligence delegation)
- `validate_medical_intelligence_architecture.py`
- `test_day_one_architecture_guardrails.py`
- `test_medical_intelligence_architecture_sentinels.py`
- `test_med_frame_identity_index.py`
- `test_context_modifier_catalogue.py`

---

## ARCH-SENTINEL-1 clean-up items

| Item | Status |
|------|--------|
| Dead condition in `validate_promotion_safety_gate` | **Resolved** — removed impossible `blocked ∩ unsafe` branch |
| Expand governance artefact pytest coverage to 5 YAML files | **Resolved** — expansion candidates + creatinine adjudication added |

---

## Runtime boundary confirmation

No changes to SignalEvaluator, packages, frontend, SSOT, scoring, or emitted analysis.

---

## Carry-forward updates

| ID | Status |
|----|--------|
| CF-SENTINEL-001 | **Resolved** — gate + CI workflow + golden gate integration |
| CF-PASS3FRAME-003, CF-PASS3FRAME-002, CF-CONTEXT-MOD-2 | **Open** (unchanged) |

---

## Remaining limitations

- `ci.yml` high-value backend job still runs `backend/tests/unit/` only; architecture gate is a **separate** workflow job (by design — avoids DB/docker coupling).
- Full `golden_gate_local.py` (baseline + three-layer) is heavier than architecture gate alone; run before bus `finish` on sprint branches.

---

## Recommended next sprint

Pass_3 enrichment or CONTEXT-MOD-2 runtime binder — architecture gates now block regressions automatically.

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
.......s..  (1 skipped: gate self-test under ARCHITECTURE_GATE_CHILD)
[architecture-gate] pytest_governance_regression
..................... 
architecture_validation_gate: PASS

python backend/scripts/validate_medical_intelligence_architecture.py
medical_intelligence_architecture_validation: PASS

python backend/scripts/validate_day_one_architecture.py
day_one_architecture_validation: PASS

python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q
....

python -m pytest backend/tests/architecture/test_medical_intelligence_architecture_sentinels.py -q
.......

python -m pytest backend/tests/regression/test_med_frame_identity_index.py -q
...........

python -m pytest backend/tests/regression/test_context_modifier_catalogue.py -q
..........
```
