# Compile Manifest Contract

**Authority:** ADR-RT-004, `knowledge_bus/schema/compile_manifest_schema_v1.yaml`  
**Work package:** ARCH-RT-1  
**Status:** DRAFT (schema v1.0.0)

## Purpose

A **compile manifest** is immutable evidence that a governed compile run transformed validated research inputs into runtime-consumable artefacts with deterministic hashes, identity keys, and validator outcomes. Manifests support package promotion, launch-readiness audit, and estate regeneration without raw research reads at runtime.

## Per-run vs per-artefact vs estate index

| Artifact | Scope | Filename (convention) |
|----------|-------|------------------------|
| **Compile manifest** | One compile run (one or more specs) | `knowledge_bus/compile_manifests/<compile_id>.yaml` |
| **Per-package manifest copy** | Optional pointer on package | `package_manifest.yaml` → `compile_manifest_ref` (future field) |
| **Estate index** | Aggregate of all promoted packages | `knowledge_bus/compile_manifests/compile_estate_index.yaml` |

ARCH-RT-1 defines schema only; storage directories are created in ARCH-RT-3 regeneration.

## Required fields

See schema `root_required_fields`. Minimum semantic set:

- `compile_id` — unique run identifier  
- `compiler_name` / `compiler_version` — tool identity  
- `compile_mode` — `activation` \| `psi` \| `hypothesis` \| `card_evidence` \| `estate_index` \| `pilot`  
- `source_contract_version` — investigation spec contract (e.g. `3.0.0`)  
- `source_specs[]` — `source_spec_id`, `source_path`, `source_hash`, `source_hash_algorithm`  
- `outputs[]` — artefact type, path, hash, optional `activation_key` / `package_id`  
- `translation_rules_version` — rules file version used  
- `compiled_at_utc`, `compiled_by`  
- `provenance_status` — completeness classification  

Recommended: `activation_keys_emitted`, `collisions_detected`, `policy_version`, `validator_results`.

## Hash rules

| Rule | Detail |
|------|--------|
| Algorithm | **SHA-256** hex (`source_hash_algorithm` / `output_hash_algorithm`) |
| Source hash | Raw bytes of `source_path` file at compile time |
| Output hash | Raw bytes of each emitted artefact after write |
| Ordering | `source_specs` sorted by `source_spec_id`; `outputs` sorted by `output_path` |
| Determinism | Same inputs + compiler version → same hashes |

## Deterministic ordering

Compilers **must** emit list fields in stable sort order so manifest diffs are meaningful for parity and audit.

## Package promotion

A package may move `runtime_loaded: true` in LC-S18A inventory only when:

1. Listed in estate index with matching `activation_key` and `source_spec_id`.  
2. `compile_manifest_ref` resolves to a manifest with `provenance_status: complete`.  
3. `collisions_detected` is empty.  
4. `validator_results` show PASS for `validate_knowledge_package.py`.

## Launch-readiness audit

Manifests provide:

- Proof that outputs were generated from hashed sources (not hand-edited silently).  
- Full `activation_keys_emitted` list for collision audits.  
- Compiler version for reproducibility.

## Relationship to `latest_knowledge_status.json`

| Asset | Role |
|-------|------|
| `knowledge_bus/current/latest_knowledge_status.json` | **Operational** KB lifecycle / validator readiness snapshot |
| `compile_manifest.yaml` | **Per-run provenance** evidence for compile outputs |

Manifests **must not** replace `latest_knowledge_status.json`; they **reference** it optionally in `validator_results` when KB validators run post-compile.

## Legacy-retained artefacts

When `provenance_status: legacy_retained`:

- `source_specs[].legacy_retained: true` may be set.  
- Outputs may reference on-disk packages without regeneration.  
- `activation_key` should still be recorded for migration tracking even if not yet on `signal_library.yaml`.

## Identity model (ADR-RT-002)

- **`activation_key`** required on activation compile outputs (`signal_id::spec_id`).  
- **`signal_id`** retained as family identifier.  
- **`source_spec_id`** required for research-derived outputs.

## References

- `docs/architecture/ADR-RT-004_compile_manifest_and_package_provenance_policy.md`  
- `docs/architecture/package_provenance_policy.md`
