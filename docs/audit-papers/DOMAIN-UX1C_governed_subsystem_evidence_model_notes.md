# DOMAIN-UX1C — Governed Subsystem Evidence Model

## 1. Preflight results

| Check | Result |
|---|---|
| Branch | `domain-ux/domain-ux1c-governed-subsystem-evidence` |
| Stash | Empty |
| Stale token | None (DOMAIN-UX1B token removed on prior finish) |
| Kernel start | Executed for `DOMAIN-UX1C` |

## 2. Source documents reviewed

- `docs/planning-papers/DOMAIN_UX_health_systems_card_scaffold_sprint_plan_FINAL.md` (Sprint 3 scope)
- `docs/discussion documents/healthiq_health_systems_card_discussion_FINAL.md`
- `docs/architecture/User Health to Systems Map_FINAL.md`
- DOMAIN-UX1A / PATCH / UX1B audit notes
- `docs/governance/AUTOMATION_BUS_SOP_v1.3.1.md`

## 3. Subsystem model implemented

`SubsystemEvidenceV1` in `backend/core/models/results.py`:

- `subsystem_id`, `subsystem_label`, `included_marker_ids`, `missing_marker_ids`
- `status_label` (always `null` in this sprint)
- `evidence_role` (always `null`)
- `source_trace`

## 4. Domains covered

Wave 1 only:

- `wave1_cardiovascular` — 3 subsystems
- `wave1_blood_sugar` — 2 subsystems
- `wave1_liver` — 2 subsystems

## 5. Subsystem-to-marker mapping source

Single authority: `backend/core/analytics/wave1_subsystem_evidence.py` (`WAVE1_DOMAIN_SUBSYSTEM_DEFS`).

## 6. Included-marker logic

For each subsystem expected marker set: `included = (panel ∪ scored_on_rail) ∩ expected`, sorted canonical ids.

## 7. Missing-marker logic

`missing = expected − included` (backend-emitted only).

## 8. Subsystem status

`status_label` deliberately `null` — no safe derivation without new scoring logic.

## 9. DTO/model changes

- Added `SubsystemEvidenceV1`
- `ConsumerDomainScoreV1.subsystems` typed as `Optional[List[SubsystemEvidenceV1]]`
- Assembler populates via `_wave1_card_contract_extras`

## 10. Frontend type changes

- `SubsystemEvidenceV1` interface in `frontend/app/types/analysis.ts`
- **No visible subsystem UI** in `Wave1DomainCards.tsx` (DOMAIN-UX1D)

## 11. Tests added/updated

- `backend/tests/regression/test_domain_ux1c_governed_subsystem_evidence.py` (8 tests + 5 Sentinel guards)
- `backend/tests/unit/test_domain_score_assembler_v1.py` — subsystems non-null

## 12. Sentinel updates

Five new active deterministic classes pointing at UX1C regression file.

## 13. Scoring / KB / IDL / root-cause unchanged

No changes to scoring policy, signals, Knowledge Bus, IDL assets, root-cause compilers, or pipeline.

## 14. Residual gaps for DOMAIN-UX1D

- Visible subsystem chips/sections on Health Systems Cards
- Expanded card reveal grouped by subsystem
- Subsystem status when a governed derivation rule exists
- Compact biomarker mini-cards per subsystem

**Recommendation:** Start DOMAIN-UX1D as frontend-only surfacing sprint once this DTO is deployed and persisted analyses are re-run.
