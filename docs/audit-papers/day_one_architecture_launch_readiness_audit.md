# Day-One Architecture Launch Readiness Audit

**Work package:** ARCH-RT-5_full_regeneration_and_launch_gate  
**Generated:** 2026-05-30  
**Verdict:** **Launch-ready for governed Wave 1 pilot slice** with documented deferred items and programmatic guardrails (ARCH-RT-6)

## Milestone completion

| Milestone | Evidence | Status |
|-----------|----------|--------|
| M1 Provenance + collision | `ARCH-RT-5_M1_package_provenance_and_collision_audit.md` | **Complete** |
| M2 Card evidence estate | `ARCH-RT-5_M2_card_evidence_estate_audit.md` | **Complete** |
| M3 Hypothesis / root-cause | `ARCH-RT-5_M3_hypothesis_root_cause_estate_audit.md` | **Complete** |
| M4 PSI wiring | `ARCH-RT-5_M4_psi_runtime_wiring_audit.md` | **Complete** (provisional deferral) |
| M4b PSI decision (ARCH-RT-5E) | `ARCH-RT-5E_psi_runtime_wiring_decision_audit.md` | **Complete** |
| M5 Launch gate | This document + traceability + authority manifest | **Complete** |
| M6 Guardrails & acceptance (ARCH-RT-6) | `ARCH-RT-6_day_one_architecture_acceptance_audit.md` | **Complete** |
| M7 Result versioning policy (LAUNCH-CORE-3) | `LAUNCH-CORE-3_result_versioning_replay_and_regeneration_audit.md` | **Complete** |

## Carry-forward classification register

| Carry-forward | Classification |
|---------------|----------------|
| ARCH-RT-1 `compile_manifest_schema` DRAFT label | **resolved** — required fields present; pilot manifests validated |
| ARCH-RT-1 `compile_id` / `compile_run_id` equality | **resolved** — enforced in validator |
| ARCH-RT-2 directory-derived `source_spec_id` interim only | **deferred_non_launch_blocker** for estate-wide |
| ARCH-RT-2 explicit vs inferred provenance | **deferred_non_launch_blocker** |
| ARCH-RT-2 root-cause multi-frame compiler | **deferred_non_launch_blocker** |
| ARCH-RT-2 signal_id first-match (temporary) | **legacy_retained_with_justification** for single-frame pilots |
| ARCH-RT-3 raw `source_trace` consumer display | **resolved** — UI filter retained |
| ARCH-RT-3 `compile_manifest_ref` pilot strings | **resolved** for pilots — real manifest paths |
| ARCH-RT-3 inferred `source_spec_ids` pilot only | **resolved** for pilot; estate-wide **deferred** |
| ARCH-RT-3 remaining hard-coded card subsystems | **legacy_retained_with_justification** (6 subsystems) |
| ARCH-RT-4 compiled hypothesis shadow-only | **legacy_retained_with_justification** until promotion sprint |
| ARCH-RT-4 presentation mapping | **resolved** — `compiled_hypothesis_presentation_mapping.md` |
| ARCH-RT-4 `physiological_claim` not retail summary | **resolved** — `summary_template` added |
| kb52c / batch JSON packages | **blocked_pending_spec_extraction** |
| PSI runtime wiring | **deferred_non_launch_blocker** (ARCH-RT-5E confirmed; no runtime wiring) |
| Persisted result immutability | **policy_locked** (LAUNCH-CORE-3; stale warning on GET) |

## Launch blockers found

**None** for the defined Wave 1 pilot launch slice, provided deferred items are accepted as non-launch-critical.

Full estate regeneration without classification would be a **launch_blocker** — avoided by explicit legacy/deferred registers.

## Prior sprint protections

| Fix / pilot | Protected |
|-------------|-----------|
| WAVE1-EQUIV1 bilirubin | Yes |
| ARCH-RT-2 activation_key pilot | Yes (unchanged) |
| ARCH-RT-3 glycaemic compiled card | Yes |
| ARCH-RT-4 vitamin D shadow | Yes |

## Recommended follow-on

See `docs/architecture/ARCH-RT-5_split_recommendation.md` for implementation tranches (`ARCH-RT-5B` card estate, `ARCH-RT-5C` hypothesis promotion).
