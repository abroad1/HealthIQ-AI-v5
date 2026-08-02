# ARCH-CONV-PKGC-1 — Data-Governance Decision Record

**Work ID:** `ARCH-CONV-PKGC-1`  
**Date opened:** 2026-08-02  
**Hardening pack:** `docs/architecture/ARCH-CONV-PKGC-1_hardening_pack.md`  
**Remediation register:** `docs/architecture/ARCH-CONV-PKGC-1_data_remediation_register.yaml`  
**Implementation status:** **NOT AUTHORISED** — awaiting Anthony data-governance approval

## Decision authority

- **Anthony (project / data-governance authority)** must approve the complete row-by-row remediation register.
- This is **not** a Head of Medical Research Gate 1 / Gate 2 medical-content decision (`ARCH-CONV_legacy_dependency_register.md` L-11: medical-review requirement = No).

## Register state

```text
register_state: AWAITING_ANTHONY_DATA_GOVERNANCE
implementation_authorised: false
live_db_probe: CONNECTION_REFUSED (localhost:5433)
risk_level: STANDARD
```

---

## Exact Anthony decision required

Anthony must approve **all** of the following. Silent omission is not approval.

### D1 — Stale-reason identifier

Approve proposed stale-reason id:

```text
legacy_waist_unit_defect:used_incorrectly
```

or name a replacement identifier and semantics.

### D2 — Default disposition for the 12 audit `used_incorrectly` rows

Phase 0 proposes:

```text
MARK_STALE_NO_REWRITE
```

for **all 12** analysis IDs listed in the remediation register.

Confirm or revise each row. Permitted dispositions:

- `GOVERNED_REMAP`
- `MARK_STALE_NO_REWRITE`
- `ALREADY_REMEDIATED_NO_ACTION`
- `BLOCKED_AMBIGUOUS`

### D3 — Persisted value rewrite policy

Confirm whether any persisted waist / questionnaire value may be rewritten.

Phase 0 recommendation: **No rewrite** (`MARK_STALE_NO_REWRITE` only).  
`GOVERNED_REMAP` is not proposed because correcting derived clinical outputs requires the unbuilt regeneration job.

### D4 — Stale-only policy

Confirm that rows approved as `MARK_STALE_NO_REWRITE` must not have clinical values overwritten.

### D5 — Audit trail and reversibility

Confirm remediation metadata may be stored in existing JSON `processing_metadata` (and/or equivalent) without a new DB lineage-table migration, recording at minimum:

- original value / unit payload preserved
- remediation action
- reason / stale_reason
- timestamp
- actor / work_id (`ARCH-CONV-PKGC-1`)
- reversibility / supersession linkage

### D6 — Ambiguous / blocked rows

Confirm treatment of `d7417288-7e11-48da-8716-d0f63f77c491` (`original_value=22`, outside typical UK-cm cluster):

- Phase 0 default: still `MARK_STALE_NO_REWRITE`
- Anthony may elevate to `BLOCKED_AMBIGUOUS`

Confirm no inferred historic value is authorised for any row.

### D7 — Live DB precondition

Acknowledge Phase 0 could not reach the live database (`CONNECTION_REFUSED`). Approve that Phase 1 write mode must:

1. re-verify all 12 IDs live;
2. fail closed if any row is missing, already remediated differently, or precondition-mismatched;
3. refuse to invent values when evidence is insufficient.

### D8 — Implementation authorisation

Set explicitly:

```text
implementation_authorised: true | false
```

Runtime Phase 1 (stale rule + remediation) is forbidden until this is `true` on disk.

---

## Anthony decision block (to be completed)

```text
decision_id: ARCH-CONV-PKGC-1-DATA-GOV-ANTHONY-YYYY-MM-DD
decision: PENDING
d1_stale_reason_id: PENDING
d2_row_dispositions: PENDING
d3_persisted_value_rewrite_allowed: PENDING
d4_stale_only_no_rewrite: PENDING
d5_audit_trail_mechanism: PENDING
d6_ambiguous_row_treatment: PENDING
d7_live_db_precondition_acknowledged: PENDING
d8_implementation_authorised: false
notes:
```

---

## Non-claims until approval

- Cursor must not add the waist-unit stale-detection rule.
- Cursor must not mutate any historic analysis row.
- Cursor must not run remediation write mode.
- Cursor must not invoke or build regeneration.
- Cursor must not touch provenance-identity / PKGC-2 surfaces.
- Cursor must not infer missing conversion context.

## Resume condition

Phase 1 is authorised only when:

1. This decision record is completed by Anthony; and  
2. The remediation register matches the approved dispositions; and  
3. `implementation_authorised: true` is written into this file and the register.
