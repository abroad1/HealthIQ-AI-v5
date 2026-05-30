# ARCH-RT-5 M1 — Package Provenance and Collision Audit

**Generated:** 2026-05-30  
**Scan:** `launch_estate_v1.scan_package_provenance()`

## Package estate summary

| Metric | Count |
|--------|------:|
| Packages with `package_manifest.yaml` | **186** |
| `pkg_kb52c_*` | **67** |
| `pkg_kb52d_*` | (included in blocked count) |
| `KBP-0001` | 1 (`legacy_retained_with_justification`) |

## Provenance classification

| Classification | Count | Launch posture |
|----------------|------:|----------------|
| `blocked_pending_spec_extraction` | 71 | Non-launch-critical until per-frame spec extraction |
| `source_document_unparsed` | 82 | Requires manifest backfill or retirement |
| `source_document_derived` | 31 | Acceptable interim; not canonical explicit |
| `provenance_gap` | 2 | Must resolve or retire |
| `legacy_retained_with_justification` | 1 | KBP-0001 example package |

## Collision / identity

| Check | Result |
|-------|--------|
| `activation_key` on ARCH-RT-2 pilot frames | Governed in `signal_activation_identity_v1` |
| Active runtime SignalRegistry | No silent `signal_id` collapse for promoted pilots |
| kb52c multi-frame packages | **Classified** `blocked_pending_spec_extraction` — not launch-critical authority |

## Compile manifests (M1 deliverable)

| Manifest | Artefact |
|----------|----------|
| `knowledge_bus/compiled/manifests/arch_rt3_glycaemic_card_evidence.yaml` | `health_system_cards/wave1_met_glycaemic_control.yaml` |
| `knowledge_bus/compiled/manifests/arch_rt4_vitamin_d_hypothesis.yaml` | `hypotheses/signal_vitamin_d_low.yaml` |
| `knowledge_bus/compiled/estate_index_v1.yaml` | Estate linkage index |

Both manifests: **validator PASS** (`validate_compile_manifest.py`).

## M1 outcome

**Complete for launch gate** with explicit classifications. Full package provenance backfill is **deferred_non_launch_blocker** for non-Wave-1 launch surfaces.
