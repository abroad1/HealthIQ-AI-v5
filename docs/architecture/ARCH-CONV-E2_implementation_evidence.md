# ARCH-CONV-E2 — Evidence Report

**work_id:** `ARCH-CONV-E2`  
**branch:** `feature/arch-conv-e2-alt-rvalue-runtime-authority`  
**risk_level:** HIGH / MIXED  
**result:** Gate 2 ratified; Post-Implementation Closure / merge authorised  
**Gate 2:** `ARCH-CONV-E2-GATE2-ANTHONY-2026-08-01` — **RATIFIED** (see `docs/architecture/ARCH-CONV-E2_GATE_2_Anthony_ratification.md`)

## Gate references

| Gate | Reference | Status |
|---|---|---|
| Gate 1 (HMR) | `ARCH-CONV-E2-GATE1-HMR-2026-08-01` | Recorded (supersedes `ARCH-CONV-E2-GATE1-HMR-2026-07-31` / commit `6d9259f`) |
| Gate 2 (Anthony) | `ARCH-CONV-E2-GATE2-ANTHONY-2026-08-01` | **RATIFIED** |

Register: `docs/architecture/ARCH-CONV-E2_medical_decision_register.yaml`

## Gate 1 decision (2026-08-01)

Canonical Pass 3 hepatocellular package is the intended S24 successor. ALT above lab range must produce the canonical general ALT-high context even when `r_value_alt_alp` cannot be calculated. R-value governs only biochemical-pattern refinement. Missing ALP/ULN/pairing fails closed **only** for R-value classification — it must not suppress elevated-ALT recognition.

Both ranked hypotheses from `inv_alt_high_r_value_hepatocellular_biochemical_pattern` are implemented at runtime (no Pass 3 JSON read):

| Rank | Hypothesis | Selected when |
|---|---|---|
| 1 | `hyp_alt_predominant_biochemical_pattern` | `R >= 5` |
| 2 | `hyp_alt_high_general_liver_test_abnormality_context` | R unavailable/ineligible, or `R <= 2` while cholestatic package withheld |

When `2 < R < 5`, the mixed package owns the pattern; hepatocellular does not emit (no general+mixed duplicate).

Medical design / R-value metric / package architecture / collision model / rank-2 fallback: **not reopened** in this remediation (Claude Code independently verified as sound).

## Activation state

| Frame | Runtime |
|---|---|
| Canonical hepatocellular | **activated** (foundational successor) |
| Mixed R-value (`2 < R < 5` gates) | **activated** |
| S24 ALT-high | **superseded / withheld** |
| Cholestatic / muscle / bilirubin / MASLD | withheld |
| Former Batch 5 keys | unreachable |

`activated_frame_count` (register): **174**

## Retained engineering

- `r_value_alt_alp` compute, lab-ULN validity, same-panel pairing, fail-closed omissions (`pairing_eligible=False` → `alt_alp_pairing_ineligible`)
- Orchestrator ULN threading
- Collision model (`alt_biochemical_pattern_axis` updated for Gate 1 2026-08-01)
- ALP/GGT `liver_injury_axis` preserved

## Runtime proofs (A–G)

Covered by `backend/tests/unit/test_arch_conv_e2_r_value_runtime_authority.py`:

- A: `R >= 5` → hepatocellular + rank-1 predominant; no mixed; no general duplicate
- B: `2 < R < 5` → mixed only; no general fallback
- C: ALP absent → general hyp; no R-value pattern
- D/E: missing R-value path (ULN absent upstream) → general hyp
- F: ineligible pairing → R omitted; general hyp emits
- G: ALT not high → no ALT-high emission
- **Bilirubin escalation (new):** canonical hepatocellular frame escalates `suboptimal` → `at_risk` when bilirubin is above its governed laboratory range; rank-2 general hyp retained; no mixed; no Hy’s Law consumer wording on surface IDs

Also: S24 absent; exactly one foundational canonical hepatocellular authority (+ mixed refinement); four withheld remain withheld; package validators pass; launch-critical / rejected / opt-in intact.

## Mechanical remediation (re-audit findings)

### 1. Bilirubin escalation regression

**Failing node:** `backend/tests/unit/test_signal_evaluator.py::test_kbs24_signals_trigger_suboptimal_then_escalate[signal_alt_high]`

**Root cause:** Canonical hepatocellular override `or_alt_high_with_bilirubin_high` uses `comparator_type: lab_range_boundary` / `boundary: above_max`. The KBS24 fixture supplied ALT lab range only and omitted bilirubin’s laboratory max. Evaluator correctly fail-closed (override did not fire). S24 historically used a hardcoded numeric bilirubin threshold (`value: 20.0`), which masked the missing range.

**Fix:** Fixture `lab_ranges` for `signal_alt_high` now includes governed `bilirubin: {min: 0.0, max: 20.0}` — fixture was medically incomplete for lab-range-boundary semantics under the canonical package (not an evaluator bug; not a medical Gate 1 reopen). Evaluator / fail-closed ULN behaviour / R-value / rank-2 / collision model unchanged.

**Focused regression added:** `TestGate1RuntimeProofs::test_canonical_alt_high_escalates_at_risk_when_bilirubin_above_lab_max`

### 2. Stale registry assertion

**Failing node:** `backend/tests/unit/test_signal_evaluator.py::test_signal_registry_alt_high_multi_frame_pilot`

**Fix:** Assert exact ARCH-CONV-E2 activation keys:

- present: `signal_alt_high::inv_alt_high_r_value_hepatocellular_biochemical_pattern`
- present: `signal_alt_high::inv_alt_high_r_value_mixed_biochemical_pattern`
- absent: S24 `signal_alt_high::inv_alt_high_hepatocellular_injury`
- absent: four withheld ALT packages (cholestatic / muscle / bilirubin / MASLD)
- no duplicate foundational hepatocellular authority

## Tests

### Full `test_signal_evaluator.py`

```text
python -m pytest backend/tests/unit/test_signal_evaluator.py -q --tb=line
........................................................................ [ 43%]
F....................................................................... [ 86%]
.......................                                                  [100%]
================================== FAILURES ===================================
C:\Users\abroa\HealthIQ-AI-v5\backend\tools\run_golden_panel.py:74: ValueError: Golden panel fixture must include biomarkers and user
=========================== short test summary info ===========================
FAILED backend\tests\unit\test_signal_evaluator.py::test_kbs23_catalogue_panel_harness_runs_all_panel_fixtures
EXIT=1
```

**Attribution of remaining failure:** same node fails on clean `main` (`4bcdaef`) with identical `ValueError: Golden panel fixture must include biomarkers and user`. Pre-existing catalogue fixture failure — **not** introduced by ARCH-CONV-E2. All ARCH-CONV-E2-related evaluator tests pass after remediation (bilirubin escalation + multi-frame pilot + remainder of file aside from catalogue harness).

### Focused / related suites (clean feature tip)

```text
python -m pytest backend/tests/unit/test_arch_conv_e2_r_value_runtime_authority.py \
  backend/tests/unit/test_arch_conv_e_runtime_activation_boundary.py \
  backend/tests/unit/test_arch_conv_e_alt_package_assets.py \
  backend/tests/unit/test_ratio_registry.py \
  backend/tests/regression/test_signal_authority_collision_enforcement.py -q
........................................................................ [ 79%]
...................                                                      [100%]
EXIT=0
```

### Package validators (active ALT packages)

```text
python backend/scripts/validate_knowledge_package.py --package-dir knowledge_bus/packages/pkg_kb52c_alt_high_hepatocellular_injury_pattern
→ signal_validation: PASS; ready_for_implementation: True; EXIT=0

python backend/scripts/validate_knowledge_package.py --package-dir knowledge_bus/packages/pkg_kb52c_alt_high_mixed_biochemical_pattern
→ signal_validation: PASS; ready_for_implementation: True; EXIT=0
```

### Committed-state runtime probe

| Check | Result |
|---|---|
| Register `activated_frame_count` | 174 |
| Loaded ALT keys | hepatocellular + mixed only (exact) |
| S24 present | False |
| Four withheld absent | True |
| ALT 70 / bili 12 / max 20 → state | `suboptimal` + general hyp on hepatocellular |
| ALT 70 / bili 25 / max 20 → state | `at_risk` + general hyp on hepatocellular |
| Mixed co-emission on that panel | None |

## Confirmations

- Canonical Pass 3 research not modified and not read at runtime
- No additional fallback package added
- No frontend inference
- Medical Gate 1 / R-value / collision / rank-2 design not reopened
- Gate 2 (`ARCH-CONV-E2-GATE2-ANTHONY-2026-08-01`) explicitly ratified by Anthony (2026-08-01)
- Gate 2 ratification commit updates governance status only (register / collision refs / activation register / evidence); no metric, package, collision-policy, or runtime behaviour change
- Merge authorised under Post-Implementation Closure Protocol

## Post-Implementation Closure

| Check | Result | Evidence |
|---|---|---|
| Gate 2 status | RATIFIED | `ARCH-CONV-E2-GATE2-ANTHONY-2026-08-01` |
| Merge authorised | Yes | Human approval 2026-08-01 |
| Sprint branch | `feature/arch-conv-e2-alt-rvalue-runtime-authority` | Fast-forward into `main` |
| Feature tip SHA | `901f640` | Closure evidence tip (includes Gate 2 + kernel COMPLETE) |
| Working tree (pre-merge) | Clean | `git status --short` empty |
| Stash | Empty | `git stash list` empty |
| Kernel status | COMPLETE | `automation_bus/latest_cursor_status.json` |
| Finish | PASS | `python backend/scripts/run_work_package.py finish` exit 0 |
| Publish | Required | push `main` → `origin/main`; verify local `main` == `origin/main` |
