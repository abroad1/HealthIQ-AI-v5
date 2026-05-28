# Intelligence Authority Inventory

**Work package:** ARCH-RT-0  
**Generated:** 2026-05-28

## Authority rows

| Domain | Current authority (path) | Runtime consumed | Source provenance | Duplicate authority risk | Target-state recommendation |
|--------|--------------------------|------------------|-------------------|--------------------------|----------------------------|
| Research source | `knowledge_bus/research/investigation_specs/` (67 files) | **NO** (not read at runtime) | Individual `inv_*.yaml` + batch JSON | Packages hand-maintained in parallel | **Single canonical research authority**; compile-only reads |
| Signal activation | `knowledge_bus/packages/*/signal_library.yaml` | **YES** (`SignalRegistry`) | Mixed batch/spec/arch doc | 45 `signal_id` collision families | **Compiled activation artefact** from investigation spec |
| Signal semantics (PSI) | `knowledge_bus/packages/pkg_kb47_*/promoted_signal_intelligence.yaml` | **NO** | PSI `investigation_spec_id` | Overlaps signal_library for kb47 | **Signal-layer compile view**; optional runtime later per ADR-008 |
| Hypothesis / WHY | `knowledge_bus/root_cause/hypotheses/*.yaml` + `root_cause_registry_v1.py` | **YES** (`root_cause_compiler_v1.py`) | Manual registry tuples | Diverges from Pass 3 spec hypotheses | **Compiled hypothesis artefact** + manifest registry |
| Health Systems Card evidence | `backend/core/analytics/wave1_subsystem_evidence.py` | **YES** | Hard-coded `expected_marker_ids` tuples | Frontend must not author grouping | **Compiled card evidence artefact** (future sprint) |
| Domain scores / card shell | `backend/core/analytics/domain_score_assembler.py` | **YES** | Scoring rails + subsystem assembler | Domain missing-marker workarounds | Keep assembler **thin**; no new hard-coded markers |
| IDL / presentation safety | `knowledge_bus/interpretation_display_layer_v1/idl_records_v1.yaml` | **YES** (narrative path) | Governed IDL publish | Retail explainer parallel | IDL gates **presentation** only |
| Retail explainer | `backend/ssot/retail_explainer_v1/registry.yaml` | **YES** (where wired) | SSOT registry | Must not override medical graph | Consumer prose safety layer |
| Interaction map | `knowledge_bus/interaction_maps/interaction_map_v1.yaml` | **PARTIAL** (validators + downstream) | Single file v1 | Family-level keys today | Re-key to **frame identity** when multi-frame adopted |
| Phenotype map | `knowledge_bus/phenotypes/phenotype_map_v1.yaml` | **PARTIAL** | Single file v1 | Same as interaction map | Align to `activation_key` policy |
| Calibration | `backend/ssot/calibration_registry.yaml` | **YES** (`calibration_engine.py`) | SSOT | Low | Retain SSOT authority |
| Confirmatory tests | `knowledge_bus/registries/confirmatory_tests_v1.yaml` | **YES** (root-cause path) | Registry file | Overlap with spec confirmatory blocks | Compile from investigation spec |
| DTO boundary | `backend/core/models/results.py`, `backend/core/models/signal.py` | **YES** | Pydantic contracts | Frontend types must mirror | Add **provenance fields** on `SignalResult` (ARCH-RT-2) |
| Frontend rendering | `frontend/app/components/results/Wave1*.tsx` | **N/A** (render only) | DTO fields | `wave1ConfidenceMarkerLabels.ts` legacy risk | **Render-only**; no medical inference |

## Investigation spec corpus

| Location | Count |
|----------|------:|
| `knowledge_bus/research/investigation_specs/` (total files) | 67 |
| `inv_*.yaml` | 31 |
| JSON batches | 28 |
| Schemas / ops files | 8 |

## Package corpus

See `package_generation_inventory.md` (186 `pkg_*` manifests).

## Key implementation paths (read-only preflight)

| # | Item | Path |
|---|------|------|
| 1 | Investigation spec corpus | `knowledge_bus/research/investigation_specs/` |
| 2 | Knowledge Bus packages | `knowledge_bus/packages/` |
| 3 | Package manifests | `knowledge_bus/packages/pkg_*/package_manifest.yaml` |
| 4 | PSI schema / translator / loader | See `psi_coverage_and_manifest_opt_in_report.md` |
| 5 | PSI artefacts | 20× `promoted_signal_intelligence.yaml` under `pkg_kb47_*` |
| 6 | Root-cause YAML | `knowledge_bus/root_cause/hypotheses/` (40 files) |
| 7 | Root-cause registry | `backend/core/knowledge/root_cause_registry_v1.py` |
| 8 | Wave 1 subsystem evidence | `backend/core/analytics/wave1_subsystem_evidence.py` |
| 9 | SignalRegistry / SignalEvaluator | `backend/core/analytics/signal_evaluator.py` |
| 10 | SignalResult model | `backend/core/models/signal.py` |
| 11 | Health Systems Card DTO | `backend/core/models/results.py` (`ConsumerDomainScoreV1`, `ConsumerSubsystemEvidenceV1`) |
| 12 | Frontend cards | `frontend/app/components/results/Wave1DomainCards.tsx`, `Wave1SubsystemEvidenceSection.tsx` |
| 13 | IDL | `knowledge_bus/interpretation_display_layer_v1/idl_records_v1.yaml` |
| 14 | Interaction / phenotype / calibration / confirmatory | See paths in authority table above |
