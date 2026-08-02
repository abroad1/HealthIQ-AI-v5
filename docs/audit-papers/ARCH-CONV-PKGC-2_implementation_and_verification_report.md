# ARCH-CONV-PKGC-2 — Implementation and Verification Report

**Work ID:** `ARCH-CONV-PKGC-2`  
**Branch:** `feature/arch-conv-pkgc-2-provenance-identity-closure`  
**Risk:** **STANDARD — CONTRACT_ADJACENT**  
**Status:** Implementation complete — awaiting Claude audit / GPT review / Anthony merge

## 1. Stage 1A classification

Confirmed:

1. `output_authority_provenance_builder_v1.py` is additive/descriptive only — does not feed report inclusion, clinician filtering, hypothesis selection/ranking, narrative, or signal/frame authority decisions.
2. `signal_result_index_v1.py` and `signal_activation_identity_v1.py` share one grammar: `signal_id::source_spec_id`.
3. ARCH-COMPLETION-2 “compiler quarantine filter” is `report_compiler_v1._normalise_root_cause_finding` + `is_governed_hypothesis` (why_engine_fallback skip) — distinct from the provenance builder decision surface.

Evidence: `docs/architecture/ARCH-CONV-PKGC-2_hardening_pack.md`, `docs/architecture/ARCH-CONV-PKGC-2_identity_contract_map.md`.

## 2. Implementation

| Change | Path |
|---|---|
| Form parse + historic non-frame denylist + consistency checks | `backend/core/knowledge/signal_result_index_v1.py` (`parse_activation_key`, strengthened `require_activation_key`) |
| Provenance fail-closed on claimed malformed/non-frame keys | `backend/core/analytics/output_authority_provenance_builder_v1.py` |
| Positive fixture → real evaluated FT3 row | `backend/tests/regression/test_output_authority_provenance.py` |
| Focused regression suite | `backend/tests/regression/test_arch_conv_pkgc_2_provenance_identity.py` |
| Duplicate-key fixture consistency | `backend/tests/unit/test_arch_rt_identity_prov_1.py` |

Historic truncated key `signal_homocysteine_high::inv_homocysteine_high` retained only as explicit fail-closed denylist / negative tests (`FORBIDDEN_NON_FRAME_ACTIVATION_KEYS`).

## 3. Verification

| Check | Result |
|---|---|
| `test_arch_conv_pkgc_2_provenance_identity.py` | PASS |
| `test_output_authority_provenance.py` | PASS |
| `test_report_compiler_v1.py` | PASS |
| `test_duplicate_activation_key_fails_closed` / index helpers | PASS |
| Live canonical keys (HCY frame keys + FAI) | PASS parse/require |
| Truncated HCY non-frame key | REJECTED |
| Bare signal-only / empty / multi-separator | REJECTED |

Pre-existing (not introduced by PKGC-2): eight `test_arch_rt_identity_prov_1` cases using obsolete synthetic `signal_alt_high::inv_alt_high_frame_*` identities fail under the ARCH-CONV-I pilot-cohort WHY fail-closed boundary — independently confirmed by stash-reverting PKGC-2 runtime changes. Tracked as **`CF-ARCH-CONV-I-ALT-IDPROV-1`** (Open); not remediated on this branch.

## 4. Carry-forward

`CF-ARCH-CONV-PROV-1` → **Resolved**.

## 5. Explicit non-claims

- No waist / PKGC-1 changes
- No result-versioning / regeneration
- No compiled-WHY authority-state changes
- No report inclusion / narrative / ranking changes
- No Gate 1/2 (STANDARD classification)
- Not merged by Cursor
