# Activation Compile Contract

**Authority:** ADR-RT-001, ADR-RT-002, ADR-RT-004  
**Work package:** ARCH-RT-1

## Target governed path

```text
investigation_spec (validated v3.0.0)
  → signal_library.yaml
  → research_brief.yaml
  → package_manifest.yaml
```

Each run **must** emit a **`compile_manifest.yaml`** conforming to `compile_manifest_schema_v1.yaml`.

## Distinction from PSI compile

| Path | Output | Layer |
|------|--------|-------|
| **Activation compile** | `signal_library.yaml`, `research_brief.yaml`, `package_manifest.yaml` | Firing / thresholds / dependencies / evidence traceability |
| **PSI compile** | `promoted_signal_intelligence.yaml` | Signal-layer semantics only (ADR-008) |

```text
investigation_spec → promoted_signal_intelligence   # PSI translator — NOT activation
```

**Must not conflate:** hypotheses, card evidence, or full narrative into activation outputs.

## Output responsibilities

| Output | Responsibility |
|--------|----------------|
| `signal_library.yaml` | Activation, firing, thresholds, dependencies, overrides; **`activation_key` per signal entry** (future schema) |
| `research_brief.yaml` | Evidence traceability, sources, biomarker context |
| `package_manifest.yaml` | Package identity, `source_spec_id`, `compile_manifest_ref`, optional PSI opt-in path |
| `promoted_signal_intelligence.yaml` | Signal-layer semantics only — separate compile mode `psi` |

## Current repository state

| Compiler | Exists? |
|----------|---------|
| Full-estate governed activation compiler | **NO** |
| Sprint/batch scripts | **YES** — partial |
| `backend/scripts/generate_kb_s45d_batch1_packages.py` | Batch activation triple |
| `knowledge_bus/tools/kb_s47_batch2_ingest.py` | Package + PSI (kb47) |
| `investigation_spec_to_promoted_signal.py` | PSI only |

**Conclusion:** No single governed `investigation_spec → activation triple` compiler exists for full estate regeneration (confirmed ARCH-RT-0).

## Future activation compiler must prove

1. **Deterministic output** — identical inputs + version → byte-identical artefacts (modulo timestamps in manifest only).  
2. **Source hash preservation** — `source_specs[].source_hash` matches disk.  
3. **`source_spec_id` propagation** — on manifest and manifest outputs list.  
4. **`activation_key` propagation** — `signal_id::spec_id` on every activation signal.  
5. **No silent `signal_id` collapse** — duplicate `activation_key` → hard fail; duplicate `signal_id` across frames → allowed.  
6. **`validate_knowledge_package.py` compatibility** — post-compile PASS.  
7. **No PSI / hypothesis / card evidence conflation** — separate compile modes and manifests.

## Multi-frame policy (binding)

Per ADR-RT-002 **MULTI_FRAME_PER_DIRECTION**:

- One investigation spec frame → one package (or one frame entry) → one `activation_key`.  
- Shared `signal_id` across frames is **expected**; registry must not overwrite.

## Owning sprint

| Deliverable | Sprint |
|-------------|--------|
| Schema + contract (this document) | **ARCH-RT-1** |
| Pilot compiler + manifest emitter | **ARCH-RT-2** (identity runtime pilot) |
| Estate-wide regeneration | **ARCH-RT-3** |

## References

- `docs/architecture/activation_compile_gap_report.md` (ARCH-RT-0)  
- `docs/architecture/compile_manifest_contract.md`
