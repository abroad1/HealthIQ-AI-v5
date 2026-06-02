# KB-UTIL-2-ACTIVATION-READINESS — Creatinine Candidate Divergence and Collision Resolution Report

**Work ID:** `KB-UTIL-2-ACTIVATION-READINESS_creatinine_candidate_divergence_and_collision_resolution`  
**Date:** 2026-06-02  
**Candidate path:** `knowledge_bus/generated_pilot/kb_util_2_pilot/promoted_candidates/pkg_creatinine_high_renal_pass3_v1`

---

## Executive verdict

The promoted creatinine candidate remains **non-runtime** and **compiled_not_promoted**.

Activation is **blocked** pending:
- real activation-key collision with `pkg_kb52c_creatinine_high_reduced_glomerular_filtration`
- unresolved override-rule divergence acceptance/resolution (legacy eGFR + potassium vs promoted UACR)

---

## Issue 1 — Divergence classification correction

- Updated `knowledge_bus/governance/pass3_promotion_decision_register_v1.yaml`.
- Reclassified `override_rules` and `overall` from `RICHNESS_GAIN_ONLY` to `BEHAVIOURAL_DIFFERENCE_LOW`.
- Marked `accepted_with_rationale: false` until explicit divergence acceptance or resolution.

---

## Issue 2 — `pkg_kb52c` collision investigation

- Confirmed `pkg_kb52c_creatinine_high_reduced_glomerular_filtration` exists in repository.
- Confirmed real signal identity collision (`signal_creatinine_high`).
- Classified collision as **real and unresolved for runtime activation**.
- Updated promoted compile manifest blocker field to explicit real-collision classification.
- Carry-forward register updated with exact blocker details.

---

## Issue 3 — `output_root` correction and promotion hardening

- Corrected promoted candidate `compile_manifest.yaml` `output_root` to the promoted path.
- Added promotion-hardening logic in `backend/scripts/compile_pass3_pilot_artifacts.py`:
  - `normalize_promoted_compile_manifest(...)`
  - `--normalize-promoted-manifest` CLI option
- This prevents future promoted candidates from keeping stale generated-package `output_root`.

---

## Issue 4 — No-op legacy non-overwrite test replacement

- Replaced hash-to-self no-op test with a meaningful check:
  - captures legacy hash
  - runs promotion-manifest normalization path
  - verifies legacy package hash unchanged

---

## Issue 5 — Explicit boundary regression coverage

Added/extended regression checks in `backend/tests/regression/test_kb_util2_promote_pilot.py` to prove:
- promoted candidate remains `compiled_not_promoted`
- promoted candidate remains `runtime_active: false`
- collision blocker classification is explicit and stable
- promotion validator runs do not create/modify `knowledge_bus/current/latest_knowledge_status.json`

No runtime evaluator, SignalRegistry, loader, frontend, SSOT, or scoring logic was modified in this sprint.

---

## Files changed

- `knowledge_bus/governance/pass3_promotion_decision_register_v1.yaml`
- `knowledge_bus/generated_pilot/kb_util_2_pilot/promoted_candidates/pkg_creatinine_high_renal_pass3_v1/compile_manifest.yaml`
- `backend/scripts/compile_pass3_pilot_artifacts.py`
- `backend/tests/regression/test_kb_util2_promote_pilot.py`
- `docs/sprints/launch_core_carry_forward_register.md`
- `docs/audit-papers/KB-UTIL-2-ACTIVATION-READINESS_creatinine_candidate_divergence_and_collision_resolution_report.md`

---

## Validation results

- `python backend/scripts/validate_knowledge_package.py --package-dir knowledge_bus/generated_pilot/kb_util_2_pilot/promoted_candidates/pkg_creatinine_high_renal_pass3_v1` — PASS
- `python backend/scripts/validate_promoted_signal_intelligence.py --model knowledge_bus/generated_pilot/kb_util_2_pilot/promoted_candidates/pkg_creatinine_high_renal_pass3_v1/promoted_signal_intelligence.yaml` — PASS
- `python backend/scripts/validate_day_one_architecture.py` — PASS
- `python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q` — PASS
- `python -m pytest backend/tests/regression/test_kb_util2_pass3_pilot_compiler.py -q` — PASS
- `python -m pytest backend/tests/regression/test_kb_util2_promote_pilot.py -q` — PASS

---

## Runtime and activation status

- Candidate classification: `compiled_not_promoted`
- Future runtime activation: **Conditional / blocked**
- Activation condition: collision and behavioural divergence must be explicitly accepted or resolved in a governed promotion/activation sprint

---

## Remaining carry-forwards

- `CF-KBUTIL1-001` remains open with updated blocker details.
