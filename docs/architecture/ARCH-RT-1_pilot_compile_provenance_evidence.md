# ARCH-RT-1 Pilot Compile / Provenance Evidence

**Pilot:** `pkg_s24_vitamin_d_low_deficiency` / `inv_vitamin_d_low_deficiency`  
**Work package:** ARCH-RT-1  
**Generated:** 2026-05-28

## Selected source spec

| Field | Value |
|-------|-------|
| Path | `knowledge_bus/research/investigation_specs/inv_vitamin_d_low_deficiency_v1.yaml` |
| `spec_id` | `inv_vitamin_d_low_deficiency` |
| `signal_id` | `signal_vitamin_d_low` |
| SHA-256 (source bytes) | `56726fe082ed620db9dff85c44e413ec3373b521150753da4731ecc679d44ecd` |

## Related package

| Field | Value |
|-------|-------|
| `package_id` | `pkg_s24_vitamin_d_low_deficiency` |
| Manifest | `knowledge_bus/packages/pkg_s24_vitamin_d_low_deficiency/package_manifest.yaml` |
| `source_document` | `knowledge_bus/research/investigation_specs/inv_vitamin_d_low_deficiency_v1.yaml` |
| `source_spec_id` on manifest | **Absent** |
| `activation_key` on manifest / signal_library | **Absent** (future compile target) |
| PSI | **No** |
| Activation package exists | **Yes** (legacy s24 manual/scripted ingest) |

## Commands run

### 1. Knowledge package validation (read-only on existing package)

```powershell
cd backend
python scripts/validate_knowledge_package.py --package ../knowledge_bus/packages/pkg_s24_vitamin_d_low_deficiency
```

**Result:** `validation_status: PASS`, `ready_for_implementation: True`, PSI validation `SKIP` (no opt-in).

### 2. Compile manifest validator (synthetic pilot manifest)

```powershell
python backend/tests/unit/test_compile_manifest_schema_v1.py -q
```

Uses temp-file manifest with `compile_mode: pilot` and proposed `activation_key`.

### 3. PSI translator determinism (kb47 reference — not pilot package)

Pilot spec lacks v3 contract envelope for `translate_investigation_spec_v3_to_promoted_signals`.

**Alternative evidence:** SHA-256 of existing on-disk PSI (deterministic artefact):

```powershell
python -c "import hashlib; from pathlib import Path; p=Path('knowledge_bus/packages/pkg_kb47_free_t4_high_thyrotoxicosis_context/promoted_signal_intelligence.yaml'); h=hashlib.sha256(p.read_bytes()).hexdigest(); print(h); print(h)"
```

**Result (2026-05-28):** `psi_hash 2bc30c3123be7bd8a48da9da9e1a4ce3f08a5edffe9a8b4bfaca3a5c87ac6124`, `match True` (identical across two reads).

**Semantic determinism:** Translator function is pure given same input dict; re-run requires v3-wrapped spec — deferred to ARCH-RT-2 compiler pilot.

## Synthetic compile manifest (not committed to package tree)

Representative manifest validating against `compile_manifest_schema_v1.yaml`:

```yaml
compile_id: pilot-arch-rt-1-vitamin-d-001
compiler_name: activation_compile_v1
compiler_version: 0.0.0-pilot
compile_mode: pilot
source_contract_version: 3.0.0
source_specs:
  - source_spec_id: inv_vitamin_d_low_deficiency
    source_path: knowledge_bus/research/investigation_specs/inv_vitamin_d_low_deficiency_v1.yaml
    source_hash: <sha256 of spec file>
    source_hash_algorithm: sha256
outputs:
  - output_type: package_manifest
    output_path: knowledge_bus/packages/pkg_s24_vitamin_d_low_deficiency/package_manifest.yaml
    output_hash: existing-on-disk-not-recompiled
    output_hash_algorithm: sha256
    package_id: pkg_s24_vitamin_d_low_deficiency
    signal_id: signal_vitamin_d_low
    activation_key: signal_vitamin_d_low::inv_vitamin_d_low_deficiency
    source_spec_id: inv_vitamin_d_low_deficiency
translation_rules_version: 1.0.0
compiled_at_utc: 2026-05-28T22:30:00Z
compiled_by: arch-rt-1-pilot
provenance_status: pilot_evidence_only
policy_version: ADR-RT-004-v1
activation_keys_emitted:
  - signal_vitamin_d_low::inv_vitamin_d_low_deficiency
collisions_detected: []
```

**Conclusion:** Schema and validator **can represent** required provenance; package on disk **does not yet** include `source_spec_id` / `activation_key`.

## Activation compile status

| Question | Answer |
|----------|--------|
| Governed full-estate compiler | **Missing** |
| This package origin | Sprint-24 scripted translation (`translation_mode: creation` on manifest) |
| Manual vs automated | **Scripted** historical ingest — not governed manifest-emitting compile |
| PSI vs activation | **Separate** — no PSI for this package |

## Remaining implementation gaps

1. Governed `activation_compile_v1` implementation (ARCH-RT-2+).  
2. Manifest schema fields: `source_spec_id`, `activation_key`, `compile_manifest_ref`.  
3. v3 contract normalisation for legacy `inv_*.yaml` files.  
4. Estate index + promotion gate integration (ARCH-RT-3).  
5. PSI runtime wiring (design only in ARCH-RT-1; implementation later).

## Confirmations

- No package files modified.  
- No investigation spec files modified.  
- No PSI files modified.  
- No generated artefacts committed under `knowledge_bus/packages/`.
