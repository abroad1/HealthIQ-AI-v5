# ADR-RT-004 — Compile Manifest and Package Provenance Policy

| Field | Value |
|-------|-------|
| **Status** | ACCEPTED |
| **Date** | 2026-05-28 |
| **Work package** | ARCH-RT-0 |

## Context

ARCH-RT-0 found:

- **0 / 186** manifests carry `source_spec_id`.  
- **142** packages cite batch JSON only (`BATCH_JSON_ONLY` traceability).  
- **112** LC-S18A packages are inventory-registered but `runtime_loaded: false`.  
- No governed per-run compile manifest exists.

## Decision 1 — Compile manifest convention

Every governed compile run **must** emit:

**`compile_manifest.yaml`** (per run) plus optional **estate index** (`compile_estate_index.yaml`).

### Per-run manifest (minimum fields)

| Field | Required | Description |
|-------|----------|-------------|
| `compile_run_id` | Yes | UUID or deterministic hash of inputs |
| `compile_utc` | Yes | ISO-8601 timestamp |
| `compiler_name` | Yes | e.g. `activation_compile_v1` |
| `compiler_version` | Yes | Semver or git SHA |
| `input_spec_hashes` | Yes | Map spec_id → content hash |
| `outputs` | Yes | List of emitted artefacts with paths + hashes |
| `activation_keys_emitted` | Yes | Full list for collision audit |
| `collisions_detected` | Yes | Empty or hard-fail report |
| `policy_version` | Yes | ADR-RT-002 / ADR-RT-004 version tag |

### Estate index (aggregate)

| Field | Description |
|-------|-------------|
| `package_id` | Target package directory |
| `activation_key` | Primary frame identity |
| `source_spec_id` | Investigation spec frame id |
| `source_document` | Original research path |
| `legacy_retained` | Boolean classification |
| `runtime_loaded` | Promotion flag (LC-S18A aligned) |

## Decision 2 — Package manifest provenance (required fields)

All **new or regenerated** `package_manifest.yaml` files **must** include:

| Field | Policy |
|-------|--------|
| `source_spec_id` | **Required** when compiles from investigation spec |
| `source_document` | **Required** (research path or batch JSON path) |
| `source_document_hash` | **Required** on regeneration |
| `compile_run_id` | **Required** linking to manifest |
| `activation_key` | **Required** per ADR-RT-002 |
| `legacy_retained` | **Required** boolean for migration class |

Existing packages without these fields are **`legacy_retained_candidate`** until regenerated.

## Decision 3 — `source_spec_id` policy

- **Mandatory** for any package claiming investigation-spec provenance.  
- Must equal investigation spec `spec_id` (not package directory name).  
- Batch JSON packages: compile step **must extract** frame ids from JSON — **BLOCKED_PENDING_SPEC_EXTRACTION** ends at compile time.

## Decision 4 — `legacy_retained` classification

| Value | Meaning |
|-------|---------|
| `false` | Fully traceable; generated from governed compile |
| `true` | Retained for parity only; supersession documented in estate index |

Promotion to `runtime_loaded: true` requires `legacy_retained: false` **or** explicit clinical waiver recorded in manifest.

## Decision 5 — Batch JSON source handling

| Rule | Detail |
|------|--------|
| Traceability | Manifest must cite **batch path + frame spec_id** |
| Multi-frame | One package per `activation_key`; shared `signal_id` allowed |
| Compile | Batch ingest is **not** a runtime loader — compile-only |
| Extraction | ARCH-RT-1 delivers batch → frame index generator |

## Decision 6 — Package promotion / traceability

A package may be promoted (`runtime_loaded: true`) only when:

1. Listed in compile estate index.  
2. Validated by `validate_knowledge_package.py`.  
3. No duplicate `activation_key` in estate index.  
4. Parity evidence attached (shadow run id) for replacements.

## Decision 7 — Owning sprint

| Deliverable | Owner |
|-------------|-------|
| Manifest schema extension | **ARCH-RT-1** |
| First compile manifest emitter | **ARCH-RT-1** (pilot) |
| Estate-wide regeneration manifests | **ARCH-RT-3** |

## Consequences

- ARCH-RT-0 documentation sprints may not edit manifests; this ADR governs **future** compiles only.  
- LC-S18A inventory fields should align with `runtime_loaded` / `legacy_retained` in estate index.  
- CI must reject packages missing `source_spec_id` after ARCH-RT-1 schema bump.

## References

- `docs/architecture/package_generation_inventory.md`  
- `docs/architecture/legacy_package_retirement_candidates.md`  
- `docs/audit-papers/LC-S18A_package_estate_inventory_delta_report.md`
