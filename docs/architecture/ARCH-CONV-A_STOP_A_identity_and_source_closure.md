# ARCH-CONV-A — STOP A Identity and Source Closure Report

**Work ID:** `ARCH-CONV-A`  
**Date (UTC):** 2026-07-27  
**Author role:** Cursor (`healthiq-core-engine`) — implementation / evidence only  
**Authority:** Automation Bus SOP v1.3.1 § STOP A; prompt §12 / §25 / §26  

---

## WORK PACKAGE

| Field | Value |
|---|---|
| work_id | ARCH-CONV-A |
| branch | feature/arch-conv-a-estate-why-authority-migration |
| baseline main commit | `942de1ffda260bdcab8ab00ded17f4602dba478a` |
| Automation Bus status | IN_PROGRESS (kernel); STOP A **ratified** — internal continuation authorised; **finish not called** |
| authority token | `automation_bus/state/work_package_active.json` → `ARCH-CONV-A` / STARTED |

Ratification artefact: `docs/architecture/ARCH-CONV-A_STOP_A_ratification_record.md`

---

## PHASE 0

Unchanged from Phase 0 reconciliation evidence (`ARCH-CONV-A_phase0_estate_reconciliation.md`): 41/5/36 baseline verified; single emit funnel; estate index refreshed; D-9 provenance register corrected.

---

## PHASE 1 (post-ratification)

| Field | Finding |
|---|---|
| Inventory baseline targets | **41** (pre–D-3 snapshot) |
| Live WHY registry after D-3 | **40** |
| Migrated targets | **5** |
| Package A before duplicate retirement | **36** |
| Surviving Package A identities after D-3 | **35** |
| Non-contingent Package A frames after D-2 | **20** |
| Waves | 7 retained; Wave 4 effective identities **6** |
| D-2 disposition | **FOLD_SUPPRESS** — independent frame count **0** |
| D-3 disposition | **MERGE_TO_ONE** — survivor `signal_hyperbilirubinemia`; retire WHY target `signal_bilirubin_high` |
| D-9 | Closed in Phase 0 |

Evidence: `docs/architecture/ARCH-CONV-A_phase1_target_to_frame_map.md`

---

## STOP A

| Field | Value |
|---|---|
| identity closure complete | **YES — RATIFIED** |
| canonical-source closure complete | **YES for disposition** |
| D-2 recorded | FOLD_SUPPRESS / frame_count 0 |
| D-3 recorded | MERGE_TO_ONE; registry alias applied |
| identity correction | `signal_bilirubin_high` removed from `ROOT_CAUSE_TARGET_SPECS`; alias register added |
| medical decisions | **None made by Cursor** |
| compile / runtime activation | **None** |

---

## VERDICT

```text
STOP A RATIFIED — INTERNAL CONTINUATION AUTHORISED
```

**Next authorised action (this continuation):** Phase 2 Wave 0 closure + Wave 1 medical-review pack → STOP B.
