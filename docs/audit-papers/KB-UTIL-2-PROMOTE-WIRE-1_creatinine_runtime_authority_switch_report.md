# KB-UTIL-2-PROMOTE-WIRE-1 — Creatinine Runtime Authority Switch Report

**Work ID:** `KB-UTIL-2-PROMOTE-WIRE-1_creatinine_runtime_authority_switch`  
**Date:** 2026-06-02

---

## Executive verdict

Activation of `pkg_creatinine_high_renal_pass3_v1` into runtime was **refused** in this sprint.

Runtime authority remains unchanged:
- `pkg_s24_creatinine_high_renal` remains present for `signal_creatinine_high::inv_creatinine_high_renal`
- `pkg_kb52c_creatinine_high_reduced_glomerular_filtration` remains canonical for `signal_creatinine_high::inv_creatinine_high_reduced_glomerular_filtration`

This avoids introducing duplicate activation-key authority and preserves deterministic runtime behaviour.

---

## Runtime authority preflight

1. Packages currently defining `signal_creatinine_high`:
   - `knowledge_bus/packages/pkg_s24_creatinine_high_renal`
   - `knowledge_bus/packages/pkg_kb52c_creatinine_high_reduced_glomerular_filtration`
2. Activation keys currently present:
   - `signal_creatinine_high::inv_creatinine_high_renal`
   - `signal_creatinine_high::inv_creatinine_high_reduced_glomerular_filtration`
3. `pkg_s24_creatinine_high_renal` runtime-loaded: **Yes** (package runtime path)
4. `pkg_kb52c_creatinine_high_reduced_glomerular_filtration` runtime-loaded: **Yes** (package runtime path)
5. Promoted Pass_3 candidate runtime-loaded: **No** (still under `generated_pilot/promoted_candidates`)
6. Duplicate activation keys already exist: **No** (distinct activation identities)
7. Runtime authority before sprint:
   - Pass_3 frame (`inv_creatinine_high_reduced_glomerular_filtration`): `pkg_kb52c_*`
   - Legacy frame (`inv_creatinine_high_renal`): `pkg_s24_*`
8. Proposed switch evaluated:
   - Do not activate promoted candidate while equivalent Pass_3 runtime authority already exists (`pkg_kb52c_*`) and legacy divergence adjudication remains unresolved.

---

## Collision investigation and decision

- Investigated collision claim from activation-readiness artefacts.
- Result: collision is **signal_id-level equivalence**, not current duplicate activation-key conflict in runtime.
- Decision: **D — Candidate and pkg_kb52c are equivalent; retain one canonical runtime authority.**
- Canonical retained for Pass_3 frame: `pkg_kb52c_creatinine_high_reduced_glomerular_filtration`.

---

## Override divergence decision

- Legacy s24 override rules (`eGFR < 60`, `potassium > 5.2`) remain different from Pass_3 UACR escalation.
- Decision: **C — Block full authority convergence pending clinical adjudication.**
- No hybrid rule was invented or introduced.

---

## Package promoted or activation refused

- Promoted candidate package under `generated_pilot` remains `compiled_not_promoted`.
- No runtime package activation performed for `pkg_creatinine_high_renal_pass3_v1`.

---

## Package authority files changed

- `knowledge_bus/governance/pass3_promotion_decision_register_v1.yaml`
  - added explicit WIRE-1 preflight findings
  - recorded collision decision
  - recorded override divergence decision
  - recorded activation refusal and rollback path

No runtime authority state file change was performed because the active runtime mechanism is package scanning under `knowledge_bus/packages`.

---

## Legacy package treatment

- `pkg_s24_creatinine_high_renal`: preserved unchanged (legacy retained pending adjudication)
- `pkg_kb52c_creatinine_high_reduced_glomerular_filtration`: preserved unchanged (retained canonical for Pass_3 frame)

---

## Rollback path

No runtime switch was performed.  
Rollback is therefore immediate and deterministic: existing runtime authority remains active with no additional action required.

---

## Validation results

- `python backend/scripts/validate_knowledge_package.py --package-dir knowledge_bus/generated_pilot/kb_util_2_pilot/promoted_candidates/pkg_creatinine_high_renal_pass3_v1` — PASS
- `python backend/scripts/validate_promoted_signal_intelligence.py --model knowledge_bus/generated_pilot/kb_util_2_pilot/promoted_candidates/pkg_creatinine_high_renal_pass3_v1/promoted_signal_intelligence.yaml` — PASS
- `python backend/scripts/validate_day_one_architecture.py` — PASS
- `python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q` — PASS
- `python -m pytest backend/tests/regression/test_kb_util2_pass3_pilot_compiler.py -q` — PASS
- `python -m pytest backend/tests/regression/test_kb_util2_promote_pilot.py -q` — PASS

---

## Tests added/updated

Updated `backend/tests/regression/test_kb_util2_promote_pilot.py` with WIRE-1 coverage:
- activation-key preflight assertions for `signal_creatinine_high`
- candidate remains non-runtime under package runtime path
- candidate override-rule equivalence with `pkg_kb52c`
- register assertions for activation refusal and rollback path

---

## Runtime behaviour change assessment

No runtime behaviour changes were introduced in this sprint because no runtime authority switch was executed.

---

## Boundary confirmation

- No frontend changes
- No SSOT changes
- No scoring threshold changes
- No SignalEvaluator or SignalRegistry behavioural changes

---

## Remaining carry-forwards

- `CF-KBUTIL1-001` remains open:
  - Pass_3 candidate non-activation decision recorded
  - legacy vs Pass_3 divergence adjudication still required for full convergence

---

## Recommended next sprint

`KB-UTIL-2-CREATININE-AUTHORITY-ADJUDICATION`:
- perform explicit medical adjudication for legacy vs Pass_3 override divergence
- define whether `pkg_s24_creatinine_high_renal` remains intentionally distinct or should be retired
- if retirement is approved, execute controlled de-dup authority transition with dedicated regression and rollback controls
