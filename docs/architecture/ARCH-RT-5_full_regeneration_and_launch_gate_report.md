# ARCH-RT-5 Full Regeneration and Launch Gate Report

**Work package:** `ARCH-RT-5_full_regeneration_and_launch_gate`  
**Branch:** `work/ARCH-RT-5-full-regeneration-and-launch-gate`  
**Generated:** 2026-05-30

## Executive summary

ARCH-RT-5 completed the **launch governance gate** (M1–M5 audits, carry-forward classification, estate index, real compile manifests for ARCH-RT-3/4 pilots). Full estate regeneration and runtime promotion are **split** to follow-on packages (`ARCH-RT-5_split_recommendation.md`).

## Authority preflight (summary)

| Item | Finding |
|------|---------|
| Packages scanned | 186 |
| Compiled card artefacts | 1 (glycaemic) |
| Compiled hypothesis artefacts | 1 (vitamin D, shadow) |
| Wave 1 hard-coded subsystems | 6 (classified legacy) |
| PSI runtime | Not required for launch slice |

## Milestone summary

| Milestone | Deliverable | Implementation |
|-----------|-------------|----------------|
| M1 | M1 audit + manifests + estate index | Yes |
| M2 | M2 audit + subsystem classification | Audit + classification (no full artefact gen) |
| M3 | M3 audit + presentation mapping | Mapping doc + `summary_template`; no compiler wire |
| M4 | M4 audit | PSI deferred |
| M5 | Launch + traceability + authority manifest | Yes |

## Files changed (by milestone)

| Milestone | Paths |
|-----------|-------|
| M1 | `knowledge_bus/compiled/manifests/*`, `estate_index_v1.yaml`, `launch_estate_v1.py`, M1 audit |
| M2 | Pilot card `compile_manifest_ref` update, M2 audit |
| M3 | `compiled_hypothesis_presentation_mapping.md`, hypothesis schema/loader/artefact, M3 audit |
| M4 | M4 audit |
| M5 | `day_one_architecture_launch_readiness_audit.md`, `research_to_runtime_traceability_audit.md`, `active_intelligence_authority_manifest.md`, split doc |

## Tests

```powershell
cd backend
python -m pytest tests/unit/test_arch_rt5_launch_gate.py tests/unit/test_compiled_hypothesis_arch_rt4.py tests/unit/test_health_system_card_evidence_arch_rt3.py -q
python backend/scripts/validate_compile_manifest.py --manifest knowledge_bus/compiled/manifests/arch_rt3_glycaemic_card_evidence.yaml
```

## Confirmations

- No raw research runtime reads introduced
- No frontend medical inference introduced
- No consumer raw `source_trace` exposure
- Bilirubin / card / identity pilots protected
- No SignalRegistry / SignalEvaluator / PSI / package / spec modifications
- No helper scripts committed

## Sprint status

**Governance gate complete; implementation split recommended** for full estate regeneration.
