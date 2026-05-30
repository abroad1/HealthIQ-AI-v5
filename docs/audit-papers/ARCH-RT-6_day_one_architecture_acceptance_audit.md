# ARCH-RT-6 — Day-One Architecture Acceptance Audit

**Generated:** 2026-05-30  
**Work package:** `ARCH-RT-6_day_one_architecture_guardrails_and_acceptance_gate`

## Final classification

| Status | Selected |
|--------|----------|
| `accepted_for_wave1_launch` | **Yes** |
| `accepted_with_deferred_non_launch_blockers` | (superseded by row above — deferred items documented) |
| `launch_blocked` | No |

Wave 1 launch slice is **accepted** with programmatic guardrails enforcing architecture delivered by ARCH-RT-0 through ARCH-RT-5E. Deferred items (PSI runtime, batch JSON provenance extraction, estate-wide explicit `source_spec_id`) remain **non-launch-blocking** per prior audits.

## Guardrails enforced

| Rule group | Mechanism | Status |
|------------|-----------|--------|
| Card evidence (1–7) | `validate_day_one_architecture.py` + `test_health_system_card_evidence_arch_rt5b.py` | **GUARDED** |
| Hypothesis / root-cause (8–12) | Validator + `test_compiled_hypothesis_arch_rt5c.py` | **GUARDED** |
| Signal identity (13–15) | Validator within-file + global `activation_key` uniqueness | **GUARDED** |
| Provenance / manifests (16–20) | Validator + `test_arch_rt5d_package_provenance.py` | **GUARDED** |
| PSI (21–24) | Validator + `test_arch_rt5e_psi_runtime_wiring_decision.py` | **GUARDED** |
| Runtime research-read (25–26) | Validator static scan of launch-critical modules | **GUARDED** |

## Validator

| Item | Path |
|------|------|
| Command | `python backend/scripts/validate_day_one_architecture.py` |
| Tests | `backend/tests/architecture/test_day_one_architecture_guardrails.py` |

## Sentinel integration

| Item | Value |
|------|-------|
| Pack location | `sentinel/packs/day_one_architecture_guardrails_v1.json` |
| Format | JSON (repository Sentinel convention; prompt yaml name mapped to v1 JSON pack) |
| Validator reference | `backend/scripts/validate_day_one_architecture.py` |

## Deferred non-launch blockers (unchanged)

| Item | Classification |
|------|----------------|
| PSI runtime wiring | `deferred_non_launch_blocker` (ARCH-RT-5E) |
| kb52c batch JSON provenance extraction | `batch_json_blocked_pending_spec_extraction` |
| Estate-wide explicit manifest `source_spec_id` | deferred |
| Multi-frame root-cause promotion | blocked pending frame-selection policy |

## Prior sprint protections

All targeted ARCH-RT-5B/5C/5D/5E regression tests remain in the required test matrix for this sprint.
