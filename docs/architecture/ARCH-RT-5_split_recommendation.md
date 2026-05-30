# ARCH-RT-5 Split Recommendation

**Generated:** 2026-05-30

## Preflight decision

**Governance gate (M1–M5 audits + launch classifications):** executable in one package — **completed** in `ARCH-RT-5_full_regeneration_and_launch_gate`.

**Full estate regeneration (all artefacts + runtime promotion):** **too large for one governed package** — split along milestone boundaries per sprint plan.

## Recommended follow-on packages

| Package | Scope | Milestone |
|---------|-------|-----------|
| `ARCH-RT-5B_card_evidence_estate_generation` | Compile remaining 6 Wave 1 subsystems; retire/classify hard-coded defs | M2 implementation |
| `ARCH-RT-5C_hypothesis_runtime_promotion` | Wire `compile_root_cause_v1()` for governed pilots; multi-frame policy | M3 implementation |
| `ARCH-RT-5D_package_provenance_backfill` | Explicit `source_spec_id` on launch-critical packages; kb52c extraction | M1 implementation |
| `ARCH-RT-5E_psi_runtime_wiring` | PSI runtime only if product mandates | M4 implementation |

## What ARCH-RT-5 delivered (this package)

- Real compile manifests + `estate_index_v1.yaml`
- Updated pilot `compile_manifest_ref` paths
- `launch_estate_v1.py` provenance scan
- `compiled_hypothesis_presentation_mapping.md`
- All M1–M5 audit papers + launch gate
- No production compiler/registry mutation

## Why split

Mandatory split triggers met:

- Card evidence estate generation for 6 subsystems exceeds pilot scope safely in one sprint.
- Root-cause compiler wiring requires presentation + multi-frame policy per promoted signal.
- 186-package provenance resolution is audit-classified but not fully resolved in data.
