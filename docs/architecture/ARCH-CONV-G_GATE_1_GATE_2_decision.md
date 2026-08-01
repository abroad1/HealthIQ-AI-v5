# ARCH-CONV-G — Gate 1 / Gate 2 Decision Record

**Work ID:** `ARCH-CONV-G`  
**Date opened:** 2026-08-01  
**Hardening pack:** `docs/architecture/ARCH-CONV-G_hardening_pack.md`  
**Medical decision register:** `docs/architecture/ARCH-CONV-G_medical_decision_register.yaml`  
**Implementation status:** **NONE** — Phase 0 mapping only; sprint is not implemented, complete, or merged

## Gate references

| Gate | Reference | Status |
|---|---|---|
| Gate 1 — Head of Medical Research | `ARCH-CONV-G-GATE1-HMR-PENDING` | `PENDING` |
| Gate 2 — Anthony (project authority) | `ARCH-CONV-G-GATE2-ANTHONY-PENDING` | `PENDING` |

## Decision authority split

- **Head of Medical Research (Gate 1)** decides medical disposition: WHY role, competitor retirement vs retention, override presentation narrowing, and whether any gout/crystal subordinate context wording is permitted.
- **Head of Architecture** advises readiness for Anthony Gate 2 after Gate 1 medical decisions are recorded.
- **Anthony (Gate 2)** is human project authority for proceed/hold. Anthony is **not** the source of medical judgement.

## Register state

```text
register_state: PHASE_0_MAPPED_AWAITING_GATE_1_AND_GATE_2
gate1_status: PENDING
gate2_status: PENDING
```

## Exact proposed decisions for Gate 1 / Gate 2

### Canonical activation

- **Activation key:** `signal_urate_high::inv_uric_acid_high_metabolic`
- **Canonical package:** `pkg_s24_urate_high_metabolic`
- **Proposed WHY role:** `morphology_context` (flat; no conditional branch)
- **Alternative (Gate 1 only):** narrowed `causal` limited to elevated-urate / hyperuricaemia metabolic finding with identical presentation prohibitions

### Override interpretation

- Retain `or_uric_acid_renal_risk` (`egfr < 60` → `at_risk`)
- Concern / risk escalation only
- One eGFR result must not diagnose CKD
- No eGFR-owned WHY; no creatinine/urea authority change; no UACR/chronicity addition

### Package dispositions

| Package | Proposed disposition |
|---|---|
| `pkg_s24_urate_high_metabolic` | Retain as canonical compiled-WHY source |
| `pkg_kb52c_urate_high_gout_crystal_deposition_risk` | `LEGACY_RETIRED_FOR_WHY_ONLY` (package + PSI unchanged) |

### Presentation restrictions

- No gout / crystal-arthropathy diagnosis from urate alone
- No renal-failure / kidney-stone / metabolic-syndrome diagnosis from this frame
- No treatment, medication, lifestyle, or referral directive wording
- Do not compile either package’s raw `explanation.implications` verbatim

### Exclusions

HbA1c (any), creatinine, urea, eGFR/UACR/chronicity as independent WHY, ferritin, haemoglobin, ALT, thyroid, lipid, ALP/GGT, bilirubin WHY, total-cholesterol WHY, urate-low, unrelated urate signals.

### Expected authority delta (if Gate 1 confirms)

- `+1 COMPILED_ACTIVE`
- `+1 LEGACY_RETIRED`

## Non-claims

- This document does **not** authorise implementation.
- Gate recording (when later approved) still requires Automation Bus resume under a gate-consistent hardened prompt before runtime changes.
- Retrospective ratification is forbidden.

## Required next human actions

1. GPT / Head of Medical Research: record Gate 1 approval or narrowing against this proposed disposition.
2. Anthony: record Gate 2 approval after Gate 1.
3. Commit both gate statuses on disk (replace `PENDING` references).
4. Resume `ARCH-CONV-G` for implementation only if disposition matches this pack, or revise prompt + re-harden if material change is required.
