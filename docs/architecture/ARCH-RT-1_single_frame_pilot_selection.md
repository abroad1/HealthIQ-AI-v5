# ARCH-RT-1 Single-Frame Pilot Selection

**Work package:** ARCH-RT-1  
**Generated:** 2026-05-28

## Selection criteria (from sprint prompt)

- Single-frame (no multi-frame collision)  
- Valid investigation spec on disk  
- No duplicate `signal_id` across packages  
- Clear package ↔ spec relationship  
- PSI gap useful but not required  
- Low runtime blast radius  

## Rejected candidates

| Candidate | Reason rejected |
|-----------|-----------------|
| **ALT** (`signal_alt_high`, 4 packages) | Multi-frame medical case; 45-family collision inventory |
| **CRP** (`signal_crp_high`) | Prompt-excluded; overlaps `pkg_inflammation_crp_context` legacy context id |
| **Homocysteine** (`signal_homocysteine_high`, 3 packages) | Multi-frame + dual registry rows |
| **LDL / TSH / HbA1c** (s24 winners) | Duplicate families with kb52c — not single-frame |
| **`pkg_kb47_*`** | PSI present — useful for PSI doc, wrong for activation-only pilot |
| **Batch JSON kb52c frames** | `blocked_pending_spec_extraction`; multi-frame by design |

## Selected pilot

| Field | Value |
|-------|-------|
| **Package** | `pkg_s24_vitamin_d_low_deficiency` |
| **Investigation spec** | `knowledge_bus/research/investigation_specs/inv_vitamin_d_low_deficiency_v1.yaml` |
| **`spec_id`** | `inv_vitamin_d_low_deficiency` |
| **`signal_id`** | `signal_vitamin_d_low` |
| **Proposed `activation_key`** | `signal_vitamin_d_low::inv_vitamin_d_low_deficiency` |
| **Collision check** | **Unique** — only `pkg_s24_vitamin_d_low_deficiency` owns `signal_vitamin_d_low` (ARCH-RT-0 inventory command) |
| **PSI** | **Absent** — tests PSI gap narrative without conflating pilot |
| **`source_document`** | Present on manifest (individual spec path) |
| **`source_spec_id` on manifest** | **Absent** (migration debt — pilot demonstrates future requirement) |
| **Runtime blast radius** | Low — nutritional domain; unique signal; s24 governed tier |

## Evidence

```text
# Unique s24 signal_ids (excerpt)
('signal_vitamin_d_low', 'pkg_s24_vitamin_d_low_deficiency')
```

Manifest excerpt:

```yaml
source_document: knowledge_bus/research/investigation_specs/inv_vitamin_d_low_deficiency_v1.yaml
```

Spec excerpt:

```yaml
spec_id: inv_vitamin_d_low_deficiency
signal_id: signal_vitamin_d_low
```

## Pilot use in ARCH-RT-1

- Template `compile_manifest.yaml` (synthetic, not committed to package dir)  
- Validator smoke test in `test_compile_manifest_schema_v1.py`  
- Provenance evidence doc — read-only validation of existing package

## Uncertainty

- Investigation spec file lacks `investigation_spec_contract_version: 3.0.0` wrapper in YAML (s24 legacy shape). Future activation compiler must normalise or require v3 envelope before compile.
