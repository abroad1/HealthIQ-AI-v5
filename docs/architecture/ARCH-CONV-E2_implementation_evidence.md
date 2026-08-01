# ARCH-CONV-E2 — Evidence Report

**work_id:** `ARCH-CONV-E2`  
**branch:** `feature/arch-conv-e2-alt-rvalue-runtime-authority`  
**risk_level:** HIGH / MIXED  
**result:** Gate 1 (2026-08-01) canonical successor remediation complete — awaiting Anthony Gate 2 explicit ratification and Claude Code re-audit  
**Do not merge.**

## Gate references

| Gate | Reference | Status |
|---|---|---|
| Gate 1 (HMR) | `ARCH-CONV-E2-GATE1-HMR-2026-08-01` | Recorded (supersedes `ARCH-CONV-E2-GATE1-HMR-2026-07-31` / commit `6d9259f`) |
| Gate 2 (Anthony) | `ARCH-CONV-E2-GATE2-ANTHONY-2026-08-01` | ID reserved — `PENDING_EXPLICIT_RATIFICATION` |

Register: `docs/architecture/ARCH-CONV-E2_medical_decision_register.yaml`

## Gate 1 decision (2026-08-01)

Canonical Pass 3 hepatocellular package is the intended S24 successor. ALT above lab range must produce the canonical general ALT-high context even when `r_value_alt_alp` cannot be calculated. R-value governs only biochemical-pattern refinement. Missing ALP/ULN/pairing fails closed **only** for R-value classification — it must not suppress elevated-ALT recognition.

Both ranked hypotheses from `inv_alt_high_r_value_hepatocellular_biochemical_pattern` are implemented at runtime (no Pass 3 JSON read):

| Rank | Hypothesis | Selected when |
|---|---|---|
| 1 | `hyp_alt_predominant_biochemical_pattern` | `R >= 5` |
| 2 | `hyp_alt_high_general_liver_test_abnormality_context` | R unavailable/ineligible, or `R <= 2` while cholestatic package withheld |

When `2 < R < 5`, the mixed package owns the pattern; hepatocellular does not emit (no general+mixed duplicate).

## Activation state

| Frame | Runtime |
|---|---|
| Canonical hepatocellular | **activated** (foundational successor) |
| Mixed R-value (`2 < R < 5` gates) | **activated** |
| S24 ALT-high | **superseded / withheld** |
| Cholestatic / muscle / bilirubin / MASLD | withheld |
| Former Batch 5 keys | unreachable |

`activated_frame_count`: **174**  
Non-ALT activated package count: **168** (unchanged delta vs prior activated estate except ALT swap)

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

Also: S24 absent; exactly one foundational canonical hepatocellular authority (+ mixed refinement); four withheld remain withheld; package validators pass; launch-critical / rejected / opt-in intact.

## Tests

```text
python -m pytest backend/tests/unit/test_arch_conv_e2_r_value_runtime_authority.py \
  backend/tests/unit/test_arch_conv_e_runtime_activation_boundary.py \
  backend/tests/unit/test_arch_conv_e_alt_package_assets.py \
  backend/tests/unit/test_ratio_registry.py \
  backend/tests/regression/test_signal_authority_collision_enforcement.py -q
```

## Confirmations

- Canonical Pass 3 research not modified and not read at runtime
- No additional fallback package added
- No frontend inference
- No merge

## Awaiting

1. Anthony explicit Gate 2 ratification (`ARCH-CONV-E2-GATE2-ANTHONY-2026-08-01`)
2. Claude Code re-audit
