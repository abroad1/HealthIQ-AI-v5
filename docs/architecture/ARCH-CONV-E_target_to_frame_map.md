# ARCH-CONV-E — ALT target-to-frame map

**Work ID:** `ARCH-CONV-E`  
**Branch:** `feature/arch-conv-e-alt-why-authority`  
**Baseline:** `39da186b7b13a1c2bf571f68c070f6201905649c`  
**Status:** Phase 0 evidence only; no medical or runtime decision

Identity is taken from embedded governed fields and explicit registers, never
from filenames, package names, directory order, or load order.

## Canonical target

| Field | Evidence |
|---|---|
| activation_key | `signal_alt_high::inv_alt_high_hepatocellular_injury` |
| signal_id | `signal_alt_high` |
| embedded spec_id | `inv_alt_high_hepatocellular_injury` |
| canonical source | `knowledge_bus/research/investigation_specs/inv_alt_high_hepatocellular_injury_v1.yaml` |
| source SHA-256 | `7189a0761558937d4dd4397e823bbe06c7bee0b13ef9bbe0b3afc70a73b7413a` (working-tree bytes) |
| package_id | `pkg_s24_alt_high_hepatocellular_injury` |
| translation_mode | `creation` |
| identity-index status | present; canonical family `signal_alt_high` |
| provenance status | source-document-derived from the canonical investigation spec |
| signal-layer status | live |
| legacy WHY status | no registry target |
| compiled WHY status | none |
| runtime WHY authority | no governed ALT compiled frame; current non-registry signal can reach generic WHY fallback |

Embedded identity is explicit at
`inv_alt_high_hepatocellular_injury_v1.yaml:1-2`. The package manifest points to
that source at lines 8-9; the filename suffix `_v1` is not part of `spec_id`.

## Pass 3 candidates requiring separate medical decisions

All three candidate identities are embedded in
`promoted_signal_intelligence.yaml:7-8` and use `signal_alt_high`. Their shared
source is `knowledge_bus/research/investigation_specs/multi_llm_research/Batch_5_Pass_3.json`.
Signal-layer presence does not confer WHY authority.

| Candidate | activation_key | package_id | translation | identity index / signal layer | provenance | current WHY authority |
|---|---|---|---|---|---|---|
| Hepatocellular injury pattern | `signal_alt_high::inv_alt_high_hepatocellular_injury_pattern` | `pkg_kb52c_alt_high_hepatocellular_injury_pattern` | `creation` | indexed active / live | blocked for explicit-lineage authority | none |
| Metabolic steatotic liver pattern | `signal_alt_high::inv_alt_high_metabolic_steatotic_liver_pattern` | `pkg_kb52c_alt_high_metabolic_steatotic_liver_pattern` | `creation` | indexed active / live | blocked for explicit-lineage authority | none |
| Muscle source or exertional pattern | `signal_alt_high::inv_alt_high_muscle_source_or_exertional_pattern` | `pkg_kb52c_alt_high_muscle_source_or_exertional_pattern` | `creation` | indexed active / live | blocked for explicit-lineage authority | none |

The candidates are also listed as primary-biomarker matches for the predecessor
package in the Pass 3 coverage audit. That inventory relationship is not an
identity alias and does not transfer WHY authority.

## Legacy predecessor and current WHY ownership

| Field | Evidence |
|---|---|
| signal_id | `signal_hepatic_alt_context` |
| activation_key | `signal_hepatic_alt_context::inv_alt_context` |
| canonical source identity | none; architecture-doc-anchored package |
| package_id | `pkg_hepatic_alt_context` |
| governed relationship | legacy predecessor/context implementation; not a runtime alias |
| legacy asset | `knowledge_bus/root_cause/hypotheses/alt_hypotheses_v1.yaml` |
| registry path | `root_cause_registry_v1.py:32` → `load_alt_hypotheses_v1` → legacy YAML |
| compiled WHY | none |
| runtime WHY authority | active legacy family-level owner, temporarily, pending ratified ARCH-CONV-E disposition |

Current observed compiler behavior:

| Fired signals | Current findings |
|---|---|
| predecessor only | one `signal_hepatic_alt_context` finding containing `alt_hepatic_cell_stress_pattern_v1` and `alt_inflammatory_coupling_context_v1` |
| canonical only | one `signal_alt_high` generic `why_engine_fallback_v1` finding |
| both | both findings above are emitted in parallel |

The parallel result is the duplicate/family-collapse risk Gate 1 and Gate 2 must
resolve before any runtime migration.

## Explicit exclusions

- No AST WHY authority.
- No bilirubin or hyperbilirubinemia migration.
- No ALP-low authority.
- `cholestatic_source_axis` remains unchanged.
- ALP/GGT compiled medical content remains unchanged.
- No frontend medical inference.
