# Package Provenance Policy

**Authority:** ADR-RT-004, ARCH-RT-0 inventories  
**Work package:** ARCH-RT-1  
**Status:** ACCEPTED (policy); manifest schema extension deferred to ARCH-RT-2b

## Purpose

Define provenance requirements for Knowledge Bus packages so activation compile, promotion, and launch-readiness audit can trace every runtime artefact to research source without guessing.

## Required fields (new generated packages)

All packages **created or regenerated** after ARCH-RT-1 must include on `package_manifest.yaml` (future schema bump):

| Field | Requirement |
|-------|-------------|
| `source_spec_id` | **Required** — equals investigation spec `spec_id` |
| `source_document` | **Required** — repo-relative research path |
| `source_document_hash` | **Required** — SHA-256 of source at compile time |
| `activation_key` | **Required** — `signal_id::spec_id` per ADR-RT-002 |
| `compile_manifest_ref` | **Required** — path to per-run compile manifest |
| `legacy_retained` | **Required** boolean |

**ARCH-RT-1 does not modify** existing `package_manifest_schema.yaml` or on-disk manifests.

## Existing packages without `source_spec_id`

| Situation | Policy |
|-----------|--------|
| **186** current manifests with `source_document` only | Classify per `legacy_package_retirement_candidates.md` |
| `source_spec_id` absent | **Permitted** until regeneration; treat as migration debt |
| Batch JSON sources | `blocked_pending_spec_extraction` until compile extracts frame `spec_id` |
| Missing `source_document` | `unknown_requires_review` (`pkg_lipid_transport`, `pkg_example`) |

## Classification enum

| Class | Meaning |
|-------|---------|
| `active_current` | Runtime-loaded; provenance acceptable for current launch scope |
| `legacy_retained` | Kept for parity; not regenerated; explicit waiver |
| `deferred_for_regeneration` | Valid shape; LC-S18A `runtime_loaded: false` |
| `blocked_pending_spec_extraction` | Batch JSON only; no per-frame manifest index |
| `retire_candidate` | Example or superseded duplicate loser |
| `unknown_requires_review` | Missing provenance |

## Batch JSON source packages (142)

- Manifest `source_document` **must** cite batch path.  
- Compile **must** emit one package per `spec_id` / `activation_key`.  
- Until extraction: class **`blocked_pending_spec_extraction`**.  
- Must not promote to `runtime_loaded: true` without `source_spec_id`.

## Architecture-doc-sourced packages (8)

- `source_document: docs/architecture/HealthIQ_Investigation_Layer.md`  
- Class: **`legacy_retained`** until replaced by investigation-spec compile.  
- Regeneration requires new spec authoring or explicit retirement ADR.

## Study-markdown-sourced packages (3)

- `knowledge_bus/research/study_*.md`  
- Class: **`legacy_retained`** or regenerate from formal investigation spec.

## Packages with PSI (20 × `pkg_kb47_*`)

| Rule | Detail |
|------|--------|
| PSI opt-in | `promoted_signal_intelligence:` on manifest |
| PSI provenance | `investigation_spec_id` inside PSI file |
| Activation provenance | Still requires `source_spec_id` on manifest after regeneration |
| PSI without activation compile | **Invalid** for new packages |

## Packages without PSI (166+)

- PSI **not required** for activation.  
- Must still meet activation compile + manifest provenance when regenerated.

## Pre-launch validation

Before launch-readiness sign-off:

1. Estate index lists all `runtime_loaded: true` packages with `source_spec_id` + `activation_key`.  
2. No unresolved `collisions_detected` in compile manifests.  
3. `validate_knowledge_package.py` PASS for each promoted package.  
4. No `unknown_requires_review` packages in launch-critical domains without waiver.

## References

- `docs/architecture/package_generation_inventory.md`  
- `docs/architecture/legacy_package_retirement_candidates.md`  
- `docs/architecture/ADR-RT-004_compile_manifest_and_package_provenance_policy.md`
