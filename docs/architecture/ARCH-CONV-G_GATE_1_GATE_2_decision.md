# ARCH-CONV-G — Gate 1 / Gate 2 Decision Record

**Work ID:** `ARCH-CONV-G`  
**Date opened:** 2026-08-01  
**Date ratified:** 2026-08-01  
**Hardening pack:** `docs/architecture/ARCH-CONV-G_hardening_pack.md`  
**Medical decision register:** `docs/architecture/ARCH-CONV-G_medical_decision_register.yaml`  
**Implementation status:** **IMPLEMENTED on feature branch** — Gate 1 / Gate 2 recorded; compiled-WHY activation delivered under Automation Bus `ARCH-CONV-G`; pending independent audit and human merge.

## Gate references

| Gate | Reference | Status |
|---|---|---|
| Gate 1 — Head of Medical Research | `ARCH-CONV-G-GATE1-HMR-2026-08-01` | `APPROVED_WITH_NARROWING` |
| Gate 2 — Anthony (project authority) | `ARCH-CONV-G-GATE2-ANTHONY-2026-08-01` | `APPROVED` |

## Decision authority split

- **Head of Medical Research (Gate 1)** is the source of the medical judgement and narrowing for the urate WHY frame below.
- **Head of Architecture** advised readiness for Anthony Gate 2 on the Phase 0 design.
- **Anthony (Gate 2)** approved ARCH-CONV-G to proceed. Anthony is the human project authority and is **not** treated as the source of the medical judgement.

## Register state

```text
register_state: GATE_1_AND_GATE_2_RATIFIED_IMPLEMENTATION_AUTHORISED
gate1_status: APPROVED_WITH_NARROWING
gate2_status: APPROVED
```

## Approved medical disposition

### Canonical activation

- **Activation key:** `signal_urate_high::inv_uric_acid_high_metabolic`
- **Canonical package:** `pkg_s24_urate_high_metabolic`
- **`why_role`:** `morphology_context` (flat; no conditional branch)
- **Naming:** urate versus uric acid remains an existing terminology convention only; no new alias or identity

### Clinical prohibitions (narrowing)

No diagnosis of:

- gout
- urate crystal deposition
- CKD
- renal failure
- specific metabolic disease
- treatment need

from this compiled-WHY frame.

### Competing frame

- **Activation key:** `signal_urate_high::inv_urate_high_gout_crystal_deposition_risk`
- **Disposition:** `LEGACY_RETIRED_FOR_WHY_ONLY`
- Valid gout/crystal-deposition content may remain **only as subordinate risk context** within the canonical frame
- Package-layer and PSI status **unchanged**

### Override interpretation

- Retain `or_uric_acid_renal_risk` (`egfr < 60` → `at_risk`)
- Concern / risk escalation only
- No CKD diagnosis from one eGFR
- No eGFR-owned WHY authority
- No change to creatinine or urea authority
- No UACR or chronicity inference
- Missing eGFR prevents renal-risk attribution but does **not** block the basic urate-context finding

### Expected authority delta

- `+1 COMPILED_ACTIVE`
- `+1 LEGACY_RETIRED`

### Exclusions preserved

HbA1c (any), creatinine, urea, eGFR/UACR/chronicity as independent WHY, ferritin, haemoglobin, ALT, thyroid, lipid, ALP/GGT, bilirubin WHY, total-cholesterol WHY, urate-low, unrelated urate signals.

## Implementation authorisation

Gate recording authorises resume of ARCH-CONV-G implementation under the existing active Automation Bus work package. Do not re-run `start`. Do not merge from this recording commit alone.
