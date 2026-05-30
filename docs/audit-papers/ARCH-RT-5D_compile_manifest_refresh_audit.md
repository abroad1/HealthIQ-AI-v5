# ARCH-RT-5D — Compile Manifest Refresh Audit

**Generated:** 2026-05-30

## Manifests checked (8 launch-relevant)

| Manifest | compile_mode | Status |
|----------|--------------|--------|
| `arch_rt3_glycaemic_card_evidence.yaml` | card_evidence | PASS + hashes refreshed |
| `arch_rt4_vitamin_d_hypothesis.yaml` | hypothesis | PASS + hashes refreshed |
| `arch_rt5b_lipid_transport_card_evidence.yaml` | card_evidence | PASS + hashes refreshed |
| `arch_rt5b_homocysteine_pathway_card_evidence.yaml` | card_evidence | PASS + hashes refreshed |
| `arch_rt5b_vascular_strain_card_evidence.yaml` | card_evidence | PASS + hashes refreshed |
| `arch_rt5b_insulin_metabolic_card_evidence.yaml` | card_evidence | PASS + hashes refreshed |
| `arch_rt5b_enzyme_pattern_card_evidence.yaml` | card_evidence | PASS + hashes refreshed |
| `arch_rt5b_processing_context_card_evidence.yaml` | card_evidence | PASS + hashes refreshed |

## Hashes refreshed

All `source_hash` and `output_hash` fields updated from `pending_inventory_refresh` to SHA-256 digests of referenced files on disk.

## Hashes still pending

None for launch-relevant manifests.

## Validator changes

| Change | File |
|--------|------|
| `compile_run_id == compile_id` when both present | `backend/scripts/validate_compile_manifest.py` |
| `output_type` enum enforced for card_evidence/hypothesis modes | Same |
| Added `health_system_card_evidence`, `compiled_hypothesis` to schema enum | `compile_manifest_schema_v1.yaml` |

## Schema strictness decision

Schema remains **DRAFT**. Launch-relevant rules documented in `launch_relevant_manifest_rules` block. `activation_keys_emitted` / `collisions_detected` remain optional until activation compiler sprint.

## Manifest refs

All compiled card and hypothesis artefacts resolve `compile_manifest_ref` via `launch_estate_v1.resolve_compile_manifest_ref()`.

## Unresolved manifest issues

None for launch-relevant set.
