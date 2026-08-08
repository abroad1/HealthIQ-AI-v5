# V5 Runtime Authority — Same-class Sweep

**Work ID:** `V5-RUNTIME-AUTHORITY-INTEGRITY-1`  
**Scope:** runtime-active / activation-registered keys that conflict with an **explicit** pre-existing activation prohibition.  
**Not in scope:** general medical-content audit; treating `LEGACY_RETIRED` / WHY-skip as deactivation.

## Prohibition sources searched

1. All `docs/architecture/*medical_decision_register*.yaml` → `blocked_targets` with status in `{NOT_AUTHORISED, DO_NOT_ACTIVATE, REJECTED_FOR_ACTIVATION, REJECTED}`
2. `knowledge_bus/governance/compiled_why_authority_register_v1.yaml` → `anthony_decision` in `{NOT_AUTHORISED, NOT_AUTHORISED_WAVE*, DO_NOT_ACTIVATE, REJECTED_FOR_ACTIVATION}` or starting with `NOT_AUTHORISED`

## Estate findings

| Candidate | Evidence | Classification |
|---|---|---|
| `signal_total_cholesterol_high` (2 activation keys) | Wave 2 `blocked_targets` `NOT_AUTHORISED`; WHY `anthony_decision: NOT_AUTHORISED_WAVE2`; present in activation register pre-fix | **CONFIRMED_VIOLATION** |
| `signal_apoa1_cardio_risk` (1 key) | Wave 2 `blocked_targets` `NOT_AUTHORISED`; present in activation register pre-fix | **CONFIRMED_VIOLATION** |
| `signal_lipid_transport_dysfunction` (2 keys) | Wave 2 `blocked_targets` `NOT_AUTHORISED`; present in activation register pre-fix | **CONFIRMED_VIOLATION** |
| Wave 1–I / PKGB / E / F / G / H medical decision registers | `blocked_targets: []` or absent | **NO_CONFLICT** |
| WHY rows with `anthony_decision: SUPERSEDED_BY_WAVE1/WAVE2` still listed in activation register | Supersession / WHY path change — **not** an explicit activation prohibition; comment in `why_authority_v1.py` states parallel Pass-3 lipids may still evaluate | **NO_CONFLICT** (do not deactivate) |
| WHY `authority_state: LEGACY_RETIRED` alone | WHY non-owning state; not activation prohibition | **NO_CONFLICT** |

## Explicit activation-prohibition inventory (current estate)

Only Wave 2 contributes `blocked_targets`. Only two compiled-WHY rows carry `NOT_AUTHORISED_WAVE2` (both total-cholesterol). No other `NOT_AUTHORISED*` anthony decisions exist in the compiled WHY register (53 frames surveyed).

## Ambiguous authority

**None.** No `AMBIGUOUS_AUTHORITY_STOP` candidates. No later ratified supersession of the Wave 2 “do not activate” decision was found.

## Corrections applied

Removed the five CONFIRMED_VIOLATION activation-register rows and set `activated_frame_count: 172`. No other runtime mutations.
