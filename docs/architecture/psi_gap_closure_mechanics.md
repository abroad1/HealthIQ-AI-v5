# PSI Gap Closure Mechanics

**Authority:** ADR-008, ARCH-RT-0 `psi_coverage_and_manifest_opt_in_report.md`  
**Work package:** ARCH-RT-1

## Current PSI coverage (ARCH-RT-0 baseline)

| Metric | Value |
|--------|------:|
| PSI files on disk | 20 |
| Manifest opt-in | 20 (all `pkg_kb47_*`) |
| Package generations with PSI | kb47 only |
| Runtime consumption | **None** on Intelligence Core path |

## What PSI already does

| Capability | Detail |
|------------|--------|
| Schema | `promoted_signal_intelligence_schema_v1.yaml` |
| Translation | `investigation_spec_to_promoted_signal.py` (v3.0.0 → PSI v1) |
| Validation | `validate_promoted_signal_intelligence.py` |
| Ingest | `kb_s47_batch2_ingest.py` produces package + PSI together |
| Content | Signal-layer semantics: metrics, roles, overrides, trigger_direction |
| Provenance | `translation.investigation_spec_id`, `signal_id` inside PSI file |

## What PSI does not do

- Signal **activation** / firing thresholds (→ `signal_library.yaml`)  
- Hypotheses / WHY graphs (→ hypothesis compile, ADR-008 exclusion)  
- Health Systems Card evidence (→ future card evidence compile)  
- Runtime evaluation today (not loaded by `SignalRegistry` / `SignalEvaluator`)  
- Full estate coverage (166 packages without PSI)

## Why PSI is not the activation compiler

ADR-008 and ARCH-RT-0 inventories confirm:

- Activation path loads **`signal_library.yaml`** only.  
- PSI is **opt-in** and **signal-semantics** shaped.  
- Mixing activation into PSI would violate ADR-008 and blur compile manifests (`compile_mode` must differ).

## PSI opt-in validation

When `package_manifest.yaml` includes `promoted_signal_intelligence:`:

1. Referenced file must exist.  
2. `validate_promoted_signal_intelligence.py` must PASS.  
3. PSI `package_id` must match manifest `package_id`.  
4. `investigation_spec_id` in PSI must match future `source_spec_id` policy.  
5. PSI must not contain forbidden keys (`hypotheses`, `narrative`, etc.).

`validate_knowledge_package.py` orchestrates these checks when opt-in present.

## Gap classification

| Gap class | Count / scope | Closure mechanism |
|-----------|---------------|-------------------|
| No PSI on disk | ~166 packages | Optional PSI compile from v3 spec OR defer |
| PSI without future runtime | 20 kb47 | ARCH-RT-5+ wiring sprint |
| Spec not v3-wrapped | Most `inv_*.yaml` s24 | Spec normalisation before PSI compile |
| No `source_spec_id` on manifest | 186 | Activation compile + manifest schema bump |

## How PSI joins runtime later

1. `SignalResult` carries `activation_key` + `source_spec_id`.  
2. PSI loader indexes by `activation_key` (estate index).  
3. Evaluator attaches PSI semantics to fired results **without** changing firing logic.  
4. DTO exposes presentation-safe PSI fields; frontend does not parse PSI files.

## Separation from other artefacts

| Artefact | Must not appear in PSI |
|----------|------------------------|
| Hypothesis graphs | Yes — separate compile |
| Card subsystem markers | Yes — separate compile |
| Raw investigation spec | Yes — compile-time only |
| Research brief full text | Yes — separate file |

## References

- `architecture/ADR-008-promoted-signal-intelligence-contract-v1.md`  
- `docs/architecture/psi_runtime_wiring_design.md`  
- `docs/architecture/activation_compile_contract.md`
