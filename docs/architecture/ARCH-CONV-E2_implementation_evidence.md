# ARCH-CONV-E2 — Evidence Report

**work_id:** `ARCH-CONV-E2`  
**branch:** `feature/arch-conv-e2-alt-rvalue-runtime-authority`  
**risk_level:** HIGH / MIXED  
**result:** Gate 1 medical-governance remediation complete — awaiting Anthony Gate 2 ratification and Claude Code re-audit  
**Do not merge.**

## Gate 1 decision (recorded)

**Reference:** `ARCH-CONV-E2-GATE1-HMR-2026-07-31`  
**Gate 2 placeholder:** `ARCH-CONV-E2-GATE2-ANTHONY-PENDING`  
**Register:** `docs/architecture/ARCH-CONV-E2_medical_decision_register.yaml`

> S24 remains the foundational active ALT-high authority. R-value classifications are approved only as eligible biochemical pattern refinements and must not suppress ALT-high signalling when paired ALP or laboratory-specific ULNs are unavailable.

| Decision | Gate 1 outcome |
|---|---|
| S24 supersession by R-value frames | **NOT APPROVED** |
| `r_value_alt_alp` compute / ULN / fail-closed | **APPROVED — retain** |
| Collision-model implementation | **APPROVED — retain / update for Gate 1** |
| R-value role | Conditional biochemical pattern refinement, not replacement |
| S24 runtime | Must remain active |
| R-value hepatocellular + mixed | Withhold pending subordinate/refinement path |
| Other four ARCH-CONV-E ALT packages | Remain withheld |
| Non-ALT activation | No change |

## Verified starting state (pre-Gate-1 remediation)

Implementation commit `1bee430` had activated the two R-value frames and superseded S24 without Gate 1/2 medical-governance approval. Claude Code audit identified that defect. This remediation restores the approved activation state while retaining engineering.

Canonical Pass 3 SHA-256 (unchanged):

`7F20BF9A06B3427217AD7F753C4D9304E5D5A2C46C484699257778844B9D3267`

## Retained engineering (not reverted)

| Item | Status |
|---|---|
| `r_value_alt_alp` in `ratio_registry` (v1.2.0) | retained |
| Lab-ULN-only eligibility + fail-closed omissions | retained |
| Orchestrator `reference_ranges` threading | retained |
| Package R-value band `mandatory_pre_emission_gates` | retained for later subordinate path |
| `alt_biochemical_pattern_axis` collision group | retained; Gate 1 refs + S24 foundational policy |
| ALP/GGT `liver_injury_axis` enforcement | preserved |

## Contemporaneous / same-sample contract

Same-panel snapshot contract unchanged: markers on one analysis panel are contemporaneous; provenance records `pairing: same_panel_snapshot`.

## Activation state after Gate 1 remediation

| Frame | Runtime |
|---|---|
| `signal_alt_high::inv_alt_high_hepatocellular_injury` (S24) | **activated** (foundational) |
| R-value hepatocellular | withheld (`PROMOTE_BUT_WITHHOLD`) |
| R-value mixed | withheld (`PROMOTE_BUT_WITHHOLD`) |
| R-value cholestatic | withheld |
| Muscle / bilirubin / MASLD | withheld |
| Former Batch 5 inferred keys | unreachable |

| Metric | Value |
|---|---:|
| `activated_frame_count` | 173 |
| Active `signal_alt_high` keys | S24 only |
| Withheld ARCH-CONV-E ALT keys | 6 |

## Collision-authority decision table (Gate 1)

| Situation | Decision |
|---|---|
| ALP primary + GGT supporting | Unchanged `liver_injury_axis` suppression |
| S24 ALT-high + ALP/GGT | Coexist; S24 foundational |
| R-value frames | Not production-loaded; eligible only after subordinate path + Gate 2 |
| Missing ALP / lab ULN | R-value fails closed; **S24 ALT-high still emits** |

## Tests run (Gate 1 remediation)

```text
python -m pytest backend/tests/unit/test_arch_conv_e2_r_value_runtime_authority.py \
  backend/tests/unit/test_arch_conv_e_runtime_activation_boundary.py \
  backend/tests/unit/test_arch_conv_e_alt_package_assets.py \
  backend/tests/unit/test_ratio_registry.py \
  backend/tests/regression/test_signal_authority_collision_enforcement.py -q
```

Proof targets:

- S24 ALT frame loads
- Neither R-value frame is production-loaded
- `r_value_alt_alp` still calculates/classifies when directly exercised
- Missing-result and missing/invalid-ULN paths remain fail-closed
- Non-ALT activated package count remains 167 (+ Wave-1 kb47 unchanged)
- Package validators still pass for all six ALT packages
- R-value engineering remains available for the later refinement-authority step

## Confirmations

- No raw Pass 3 research read at runtime
- No frontend medical inference added
- No Pass 3 JSON modification
- Former Batch 5 keys not reactivated
- No merge

## Awaiting

1. Anthony Gate 2 ratification (`ARCH-CONV-E2-GATE2-ANTHONY-PENDING`)
2. Claude Code re-audit of this Gate 1 remediation
3. Later governed subordinate/refinement authority path before any R-value frame activation
