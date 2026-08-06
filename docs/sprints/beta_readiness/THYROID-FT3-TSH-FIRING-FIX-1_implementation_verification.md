# THYROID-FT3-TSH-FIRING-FIX-1 — Implementation verification

**Work ID:** `THYROID-FT3-TSH-FIRING-FIX-1`  
**Branch:** `fix/thyroid-ft3-tsh-firing`  
**Date:** 2026-08-06  
**Risk / change type:** HIGH / BEHAVIOUR  
**Operator:** Cursor (implement only — no self-certify / no merge)

## Starting state

| Item | Value |
| --- | --- |
| Starting branch | `fix/thyroid-ft3-tsh-firing` (created from `main`) |
| Starting HEAD | `6354404490e10d4f469cc485abafa81d9dc04072` |
| Kernel start | PASS — active token `THYROID-FT3-TSH-FIRING-FIX-1` |
| Stash | Empty throughout |

## Baseline defect reproduction

```text
python -m pytest tests/unit/test_p1_22_thyroid_activation_pack.py::test_ft3_high_requires_tsh_suppressed_companion_gate -v
```

**Result before fix:** FAILED — `assert 0 == 1` (no signal returned for FT3=7.0, TSH=0.2).

## Authority path inspected

| Role | Path |
| --- | --- |
| Activation frame | `knowledge_bus/packages/pkg_kb47_free_t3_high_t3_predominant_thyrotoxicosis/signal_library.yaml` |
| TSH gate | `require_tsh_suppressed` / `below_min` |
| FT4 differential gate | `require_free_t4_not_high` / `not_above_max` (retained) |
| Evaluator | `backend/core/analytics/signal_evaluator.py` (`_evaluate_single_condition`, `_passes_mandatory_pre_emission_gates`) |
| Ratified medical boundary | `docs/architecture/ARCH-CONV-A_wave1_thyroid_gate1_gate2_decision.md` |
| Clinical sign-off | `docs/Medical Research Documents/thyroid_blood_marker_interpretation_clinical_signoff.md` |
| Adjacent regression | `backend/tests/regression/test_batch2_thyroid_tsh_gating.py` |

## Root cause

`require_free_t4_not_high` is a **deliberate** medical-review gate: suppress the T3-predominant frame when FT4 is also elevated (ARCH-CONV-A Gate 1/2; STOP C proof).

The defect was **not** absence of that gate. It was evaluator fail-closed behaviour: when `free_t4` is missing from inputs, `_evaluate_single_condition` returned `False` for **all** lab-range-boundary gates, including companion-normality boundaries (`not_above_max` / `not_below_min`). That incorrectly blocked `signal_free_t3_high` whenever FT4 was absent, even with FT3 high and TSH suppressed.

Clinical sign-off for FT3 high: **TSH mandatory**; FT4 **strongly recommended**, block unless TSH available — not block unless FT4 available.

## Correction (policy-preserving)

In `signal_evaluator.py` `_evaluate_single_condition` for `lab_range_boundary`:

- Missing metric + `not_above_max` / `not_below_min` → **pass** (absence is not proof of elevation/depression).
- Missing metric + presence-requiring boundaries (`below_min`, `above_max`, `out_of_range`) → **fail closed** (TSH-absent still blocks).
- Present FT4 above max → `not_above_max` still **fails** (differential suppress retained).

No signal_library / threshold / activation-frame identity changes. No Knowledge Bus content edits. No frontend changes.

## Files changed

1. `backend/core/analytics/signal_evaluator.py`
2. `backend/tests/unit/test_p1_22_thyroid_activation_pack.py`
3. `backend/tests/unit/test_signal_evaluator.py`
4. `docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md`
5. `docs/sprints/beta_readiness/THYROID-FT3-TSH-FIRING-FIX-1_implementation_verification.md` (this file)

## Signal-estate baseline

| Metric | Before | After |
| --- | --- | --- |
| `SignalRegistry` loaded signals | 183 | 183 |
| `signal_free_t3_high` instances | 1 | 1 |
| Gates on frame | `require_tsh_suppressed`, `require_free_t4_not_high` | unchanged |

## Validation commands and results

```text
python -m pytest tests/unit/test_p1_22_thyroid_activation_pack.py -q
python -m pytest tests/regression/test_batch2_thyroid_tsh_gating.py -q
python -m pytest tests/regression/test_arch_conv_a_wave1_thyroid_stop_c.py -q
python -m pytest tests/unit/test_signal_evaluator.py::test_kb_s51_lab_range_boundary_not_above_max_passes_when_companion_absent -q
# Combined focused thyroid suites:
python -m pytest tests/unit/test_p1_22_thyroid_activation_pack.py tests/regression/test_batch2_thyroid_tsh_gating.py tests/regression/test_arch_conv_a_wave1_thyroid_stop_c.py -q
```

**Results:** all PASS (42 tests in the combined thyroid suite). Corrected case re-run twice → PASS both times.

**Pre-existing unrelated failure observed when sweeping full `test_signal_evaluator.py`:**  
`test_kbs23_catalogue_panel_harness_runs_all_panel_fixtures` → `ValueError: Golden panel fixture must include biomarkers and user` — not introduced by this change (out of package scope).

## Behavioural coverage mapped

1. FT3 high + TSH suppressed → fires  
2. FT3 high + TSH not suppressed → no fire  
3. FT3 not high + TSH suppressed → no fire  
4. FT3 high + TSH absent → no fire (governed missing-companion)  
5. FT3 ULN boundary → governed `>` ULN behaviour  
6. TSH LLN boundary → suppressed only strictly below LLN  
7. Canonical ids `free_t3` / `tsh` / `free_t4`  
8. No duplicate `signal_free_t3_high`  
9. FT4 elevated still suppresses; adjacent BATCH2 / STOP C thyroid suites green  
10. Estate baseline 183 unchanged  

## Stop conditions

None triggered. FT4 suppress-when-elevated gate retained (not removed). No MEDICAL AUTHORITY REQUIRED stop — evaluator semantics aligned to ratified suppress-when-elevated + clinical TSH-mandatory / FT4-recommended sign-off.
