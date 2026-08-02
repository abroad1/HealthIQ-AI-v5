# ARCH-CONV-PKGC-1 — Implementation and Verification Report

**Work ID:** `ARCH-CONV-PKGC-1`  
**Branch:** `feature/arch-conv-pkgc-1-waist-unit-remediation`  
**Risk / change type:** STANDARD / MIXED  
**Data governance:** `ARCH-CONV-PKGC-1-DATA-GOV-ANTHONY-2026-08-02` (`APPROVED_WITH_CONDITIONS`)  
**Status:** **IN_PROGRESS** — mechanism implemented and tested; **live 12-row write not executed**

## 1. Authority

| Item | Value |
|---|---|
| Stale reason | `legacy_waist_unit_defect:used_incorrectly` |
| Disposition (all 12) | `MARK_STALE_NO_REWRITE` |
| Value/unit rewrite | **Forbidden** |
| Remap / regeneration | Deferred / out of scope |
| Audit trail | `processing_metadata` JSON (`arch_conv_pkgc_1_waist_remediation`) |
| Implementation authorised | `true` (with live-write conditions) |

## 2. Implemented

| Component | Path |
|---|---|
| Stale-detection rule | `backend/core/dto/result_versioning_policy_v1.py` |
| Remediation planner/applier | `backend/core/dto/arch_conv_pkgc_1_waist_remediation_v1.py` |
| Operator runner (dry-run default) | `backend/scripts/arch_conv_pkgc_1_waist_remediation.py` |
| Regression suite | `backend/tests/regression/test_arch_conv_pkgc_1_waist_remediation.py` |

### Stale rule behaviour

- Emits `legacy_waist_unit_defect:used_incorrectly` when:
  - `analysis_id` is in the Anthony-approved 12-ID allowlist; or
  - remediation stamp is present in DTO `meta`.
- Does **not** infer from waist magnitude alone.
- Preserves existing six LAUNCH-CORE-3 heuristics; composes via dedupe.

### Remediation behaviour

- Dry-run plans exact 12-ID set.
- Write refused on unexpected IDs, missing approved IDs, missing rows, value/shape precondition mismatch, or supersession.
- Idempotent: already-stamped rows → `ALREADY_REMEDIATED` / no-op.
- Never rewrites questionnaire waist values/units.

## 3. Verification

| Check | Result |
|---|---|
| `test_arch_conv_pkgc_1_waist_remediation.py` | PASS |
| `test_launch_core3_result_versioning.py` | PASS |
| Live DB dry-run | **FAIL** — `CONNECTION_REFUSED` localhost:5433 |
| Live write | **Not executed** |
| 12-row remediation complete | **Not claimed** |

## 4. Outstanding execution dependency

```text
dependency: live governed DATABASE_URL reachable
blocker: psycopg2 OperationalError connection refused (localhost:5433)
required before closure:
  1) reconnect live DB
  2) dry-run against live 12 IDs
  3) write mode only if dry-run fail_closed=false
  4) post-write verify stamps + stale reasons
  5) then finish / carry-forward closure
```

`CF-ARCH-CONV-WAIST-1` remains **Open** until live remediation is verified.

## 5. Explicit non-claims

- Historic waist values were not rewritten.
- The 12 governed rows were not stamped in the live database.
- Kernel `finish` was not run.
- Work package remains `IN_PROGRESS`.
