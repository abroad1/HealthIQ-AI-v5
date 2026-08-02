# ARCH-CONV-PKGC-1 — Implementation and Verification Report

**Work ID:** `ARCH-CONV-PKGC-1`  
**Branch:** `feature/arch-conv-pkgc-1-waist-unit-remediation`  
**Risk / change type:** STANDARD / MIXED  
**Data governance:** `ARCH-CONV-PKGC-1-DATA-GOV-ANTHONY-2026-08-02` (`APPROVED_WITH_CONDITIONS`)  
**Status:** **LIVE WRITE VERIFIED** — awaiting independent Claude audit, GPT architectural review, and Anthony merge authority

## 1. Authority

| Item | Value |
|---|---|
| Stale reason | `legacy_waist_unit_defect:used_incorrectly` |
| Disposition (all 12) | `MARK_STALE_NO_REWRITE` |
| Value/unit rewrite | **Forbidden / not performed** |
| Remap / regeneration | Deferred / out of scope |
| Audit trail | `processing_metadata` JSON (`arch_conv_pkgc_1_waist_remediation`) |
| Implementation authorised | `true` |

## 2. Implemented

| Component | Path |
|---|---|
| Stale-detection rule | `backend/core/dto/result_versioning_policy_v1.py` |
| Remediation planner/applier | `backend/core/dto/arch_conv_pkgc_1_waist_remediation_v1.py` |
| Operator runner (dry-run default) | `backend/scripts/arch_conv_pkgc_1_waist_remediation.py` |
| Regression suite | `backend/tests/regression/test_arch_conv_pkgc_1_waist_remediation.py` |

### Env-load correction (live-write blocker)

Runner `_load_env` now loads `backend/.env` with override so a stale shell `DATABASE_URL` pointing at `localhost:5433/healthiq_test` cannot mask the governed project database (matches Alembic `migrations/env.py` precedence documented in `docs/ops/local-development.md`).

## 3. Governed database identity

| Field | Value |
|---|---|
| Source of truth | `backend/.env` `DATABASE_URL` (repo-documented project Postgres) |
| Host | `aws-0-eu-west-1.pooler.supabase.com` |
| Port | `5432` |
| Database | `postgres` |
| Alembic revision | `s7_profiles_billing` |
| Analyses count (estate) | 167 |
| Approved IDs present | **12 / 12** |

Not used (and rejected as targets):

- Process/shell `DATABASE_URL` → `localhost:5433/healthiq_test` (down; CI test DB)
- Repo-root `.env` Supabase eu-west-2 (33 analyses; **0 / 12** approved IDs)
- Docker Compose default `localhost:5432/healthiq` (Docker Desktop unavailable; would not contain the governed historic set)

No wipe, reseed, credential bypass, or empty substitute database was used.

## 4. Pre-write reverify

All 12 approved IDs:

- existed;
- matched audit bare numeric waist originals;
- had null/absent unit fields (unchanged);
- had no prior PKGC-1 remediation stamp;
- retained approved disposition `MARK_STALE_NO_REWRITE`.

## 5. Dry-run

```text
mode: dry_run
write_executed: false
approved_count: 12
unexpected_ids: []
missing_approved_ids: []
summary: pass_ready=12 already_remediated=0 failed=0
fail_closed: false
stale_reason (all): legacy_waist_unit_defect:used_incorrectly
value_rewritten / unit_rewritten: false
```

## 6. Governed write

```text
mode: write
write_executed: true
complete_success: true
timestamp_utc: 2026-08-02T13:49:15Z
persisted_rows: 12
fail_closed: false
```

Metadata-only updates to latest `analysis_results.processing_metadata` per analysis. Questionnaire waist values untouched.

## 7. Post-write independent verification

| Check | Result |
|---|---|
| Stamp present on all 12 | PASS |
| Stale reason exact | `legacy_waist_unit_defect:used_incorrectly` |
| Original waist values unchanged | PASS (77,77,77,60,67,75,78,78,78,78,76,22) |
| Original units unchanged | PASS (still absent/null) |
| Audit stamp work_id / decision_id | `ARCH-CONV-PKGC-1` / `ARCH-CONV-PKGC-1-DATA-GOV-ANTHONY-2026-08-02` |
| Collateral stamps outside approved set | **0** (12 stamped result rows / 12 distinct IDs) |
| Idempotent dry-run | `already_remediated=12`, actions `NO_OP_IDEMPOTENT` |

## 8. Test / gate evidence

| Check | Result |
|---|---|
| `test_arch_conv_pkgc_1_waist_remediation.py` | PASS |
| `tests/unit/test_launch_core3_result_versioning.py` | PASS |
| `tests/integration/test_persistence_service.py` | PASS |
| Architecture validation gate | PASS |
| Baseline / three-layer | Executed at kernel finish (golden gate) |
| `test_internal_uat_result_versioning_dto_contract.py` | Pre-existing fails on `missing_wave1_domain_cards` — **not** PKGC-1 attributable; no waist/remediation assertions |

## 9. Carry-forward

`CF-ARCH-CONV-WAIST-1` closed as **Resolved** after live write + independent verification of all 12 rows.

## 10. Explicit non-claims

- Historic waist values/units were **not** rewritten.
- Remap and regeneration were **not** invoked.
- PKGC-2 provenance / compiled-WHY / unrelated versioning surfaces were **not** changed.
- Branch was **not** merged by Cursor.
