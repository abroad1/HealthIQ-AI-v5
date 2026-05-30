# ARCH-RT-6 — Day-One Architecture Guardrails Report

**Work package:** `ARCH-RT-6_day_one_architecture_guardrails_and_acceptance_gate`  
**Generated:** 2026-05-30

## Summary

Permanent programmatic guardrails now enforce the day-one research-to-runtime architecture. No new product features or runtime behaviour changes were introduced.

**Final recommendation:** **`accepted_for_wave1_launch`** — guardrails pass; deferred items remain documented non-blockers.

## Guardrails implemented

| ID | Guardrail | Enforcement |
|----|-----------|-------------|
| 1–3 | Wave 1 card subsystems classified; launch-active use compiled evidence; legacy hard-coded list empty | `validate_wave1_card_estate`, estate index |
| 4 | Compile manifest refs resolve | `resolve_compile_manifest_ref` per subsystem |
| 5 | No `total_bilirubin` in compiled card artefacts | Marker scan |
| 6–7 | Frontend render-only; source_trace filter | Static scan `Wave1SubsystemEvidenceSection.tsx` |
| 8–10 | Vitamin D compiled promotion; `summary_template` required | `validate_compiled_hypothesis_promotion` |
| 11–12 | Single-frame promoted hypothesis; multi-frame blocked | Hypothesis count + registry |
| 13–15 | No within-file silent `signal_id` collapse; global `activation_key` uniqueness | `validate_signal_library_uniqueness` |
| 16–18 | 186 packages classified; inferred ≠ explicit manifest | `scan_all_package_provenance` |
| 19–20 | `compile_run_id == compile_id`; no `pending_inventory_refresh` | Launch manifest scan |
| 21–24 | PSI not on launch-critical import paths | Static scan (extends ARCH-RT-5E) |
| 25–26 | No raw investigation-spec reads on launch-critical modules | Static scan |
| — | Assembler routes compiled subsystems | `validate_wave1_assembler_routing` |

## Files checked by validator

Launch-critical Python modules (10), 8 launch compile manifests, estate index, 186 package manifests (via scan), authority manifest, frontend Wave 1 evidence component, all `signal_library.yaml` files (within-file + global activation_key).

## Sentinel integration status

**Integrated.** Pack: `sentinel/packs/day_one_architecture_guardrails_v1.json` (JSON — matches existing `sentinel/packs/*.json` convention). References `backend/scripts/validate_day_one_architecture.py` and architecture test file.

## Tests added

| Path | Role |
|------|------|
| `backend/tests/architecture/test_day_one_architecture_guardrails.py` | Validator pass + CLI + Sentinel pack presence |
| `backend/scripts/validate_day_one_architecture.py` | Deterministic guardrail command |

## Guardrails deferred

| Guardrail | Reason |
|-----------|--------|
| Cross-package `signal_id` uniqueness | **Intentionally not enforced** — MULTI_FRAME_PER_DIRECTION allows same `signal_id` with distinct `activation_key` across packages |
| Sentinel runner auto-invoke on every PR | Out of scope — pack registered; runner invocation remains existing CI/governance wiring |
| Full frontend TypeScript AST inference scan | Static heuristic guards sufficient for launch slice (`isConsumerSafeSourceTrace`, no `inferMarkerRole`) |

## Remaining launch risks

| Risk | Mitigation |
|------|------------|
| New launch-critical module bypasses validator list | Extend `_LAUNCH_CRITICAL_REL_PATHS` when adding modules |
| Drift in deferred PSI/provenance | Authority manifest + ARCH-RT-5D register |
| Manual merge without running validator | Sentinel pack + CI adoption (human process) |

## Test commands run

```text
python backend/scripts/validate_day_one_architecture.py
python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q
python -m pytest backend/tests/unit/test_health_system_card_evidence_arch_rt5b.py -q
python -m pytest backend/tests/unit/test_compiled_hypothesis_arch_rt5c.py -q
python -m pytest backend/tests/unit/test_arch_rt5d_package_provenance.py -q
python -m pytest backend/tests/unit/test_arch_rt5e_psi_runtime_wiring_decision.py -q
```

## Runtime / product behaviour

**No broad runtime changes.** Validator and tests are read-only enforcement surfaces.
