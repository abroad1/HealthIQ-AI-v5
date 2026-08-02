# ARCH-CONV-PKGC-1 — Data-Governance Decision Record

**Work ID:** `ARCH-CONV-PKGC-1`  
**Date opened:** 2026-08-02  
**Anthony decision recorded:** 2026-08-02  
**Hardening pack:** `docs/architecture/ARCH-CONV-PKGC-1_hardening_pack.md`  
**Remediation register:** `docs/architecture/ARCH-CONV-PKGC-1_data_remediation_register.yaml`  
**Implementation status:** **LIVE WRITE VERIFIED** — all 12 rows stamped; values/units unchanged; awaiting Claude/GPT audit and Anthony merge

## Decision authority

- **Anthony (project / data-governance authority)** approved the complete row-by-row remediation register.
- This is **not** a Head of Medical Research Gate 1 / Gate 2 medical-content decision.

## Register state

```text
register_state: ANTHONY_APPROVED_WITH_CONDITIONS
decision_id: ARCH-CONV-PKGC-1-DATA-GOV-ANTHONY-2026-08-02
decision: APPROVED_WITH_CONDITIONS
implementation_authorised: true
risk_level: STANDARD
```

---

## Anthony decision (`ARCH-CONV-PKGC-1-DATA-GOV-ANTHONY-2026-08-02`)

```text
decision_id: ARCH-CONV-PKGC-1-DATA-GOV-ANTHONY-2026-08-02
decision: APPROVED_WITH_CONDITIONS
d1_stale_reason_id: legacy_waist_unit_defect:used_incorrectly
d2_row_dispositions: MARK_STALE_NO_REWRITE for all 12 governed analysis IDs
d3_persisted_value_rewrite_allowed: false
d4_stale_only_no_rewrite: true
d5_audit_trail_mechanism: existing processing_metadata JSON
d6_ambiguous_row_treatment: MARK_STALE_NO_REWRITE retained for all 12 (including d7417288)
d7_live_db_precondition_acknowledged: true
d8_implementation_authorised: true
governed_remap: deferred_out_of_scope
regeneration: deferred_out_of_scope
```

### Approved conditions

1. Historic values and units must **not** be rewritten.
2. Governed remap and regeneration remain deferred / out of scope.
3. Audit trail must use existing `processing_metadata` JSON.
4. Before any write, reconnect to the live governed database and re-verify:
   - each approved analysis ID exists;
   - current state matches Phase 0 precondition;
   - not already remediated, superseded, or marked stale for this work;
   - no additional / unexpected analysis IDs included.
5. Any missing, changed, ambiguous, or already-remediated row must **fail closed** and be reported without mutation.
6. Operation must be dry-run first, idempotent, and limited exactly to the approved 12 IDs.

### Approved analysis IDs (exactly 12)

1. `e5cfbc62-93fa-4bac-8894-dcb69117ac4c`
2. `02df9062-eba8-4df1-8072-8d2182aca35d`
3. `7fc35b86-15c2-4d76-843a-e964263be0b7`
4. `a3244490-dd74-4922-a1c6-49a25c1f6604`
5. `7f780514-d288-4331-8020-8866744b70ae`
6. `ad721d67-f2e8-4942-8450-8598b8e35343`
7. `7cc8b2d5-c8f0-4138-ba18-8540eece06a1`
8. `91046b62-114f-44a3-a2ab-2b885ea5782b`
9. `7b8c58b5-191f-41e7-8fe4-a66938bb0a98`
10. `e3a1ee79-963e-46a1-afee-58657d1ffb55`
11. `7aacc734-95cf-4ea5-a19c-0d03d98dd2e9`
12. `d7417288-7e11-48da-8716-d0f63f77c491`

---

## Live-write execution (2026-08-02)

```text
live_write_status: EXECUTED_AND_VERIFIED
timestamp_utc: 2026-08-02T13:49:15Z
database: backend/.env project Postgres (aws-0-eu-west-1.pooler.supabase.com:5432/postgres)
alembic_version: s7_profiles_billing
rows_stamped: 12 / 12
disposition: MARK_STALE_NO_REWRITE
stale_reason: legacy_waist_unit_defect:used_incorrectly
value_rewritten: false
unit_rewritten: false
collateral_stamps_outside_approved_set: 0
idempotent_dry_run: already_remediated=12 / NO_OP_IDEMPOTENT
carry_forward: CF-ARCH-CONV-WAIST-1 Resolved
```

All Anthony conditions for live write were satisfied before `--write`. See
`docs/audit-papers/ARCH-CONV-PKGC-1_implementation_and_verification_report.md`.
