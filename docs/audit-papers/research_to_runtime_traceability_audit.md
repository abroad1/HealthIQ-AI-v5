# Research-to-Runtime Traceability Audit

**Work package:** ARCH-RT-5D (updated from ARCH-RT-5)  
**Generated:** 2026-05-30

## Launch-included vertical slices

### Glycaemic card evidence

```text
inv_hba1c_high_glycaemia (investigation spec, research authority)
  → manual pilot compile (ARCH-RT-3)
  → knowledge_bus/compiled/health_system_cards/wave1_met_glycaemic_control.yaml
  → compile manifest: compiled/manifests/arch_rt3_glycaemic_card_evidence.yaml
  → health_system_card_evidence.load_card_evidence_artefact()
  → wave1_subsystem_evidence.assemble_subsystem_from_compiled_card_evidence()
  → ConsumerDomainScoreV1.subsystems
  → Wave1SubsystemEvidenceSection (render-only)
```

### Vitamin D hypothesis (runtime promoted — ARCH-RT-5C)

```text
inv_vitamin_d_low_deficiency_v1.yaml (research authority)
  → manual pilot compile (ARCH-RT-4)
  → knowledge_bus/compiled/hypotheses/signal_vitamin_d_low.yaml
  → compile manifest: compiled/manifests/arch_rt4_vitamin_d_hypothesis.yaml
  → compiled_hypothesis.get_compiled_hypothesis_artefact()
  → root_cause_compiler_v1._compile_compiled_hypothesis_finding()
  → RootCauseV1 (summary_template only)
```

Legacy `vitamin_d_low_hypotheses_v1.yaml` retained for comparison; not used at runtime for promoted signal.

### Wave 1 card evidence (7 subsystems — ARCH-RT-5B)

All seven Wave 1 subsystems trace through `health_system_card_evidence` compiled artefacts (see `estate_index_v1.yaml`).

## Prohibited paths (verified absent)

| Prohibited path | Status |
|-----------------|--------|
| Raw investigation spec runtime reads | **None introduced** |
| Frontend medical inference | **None introduced** |
| Consumer-visible raw `source_trace` | **Filtered** |

## Gaps (classified)

| Gap | Classification |
|-----|----------------|
| 142 batch JSON packages | `batch_json_blocked_pending_spec_extraction` (ARCH-RT-5D) |
| 11 architecture/study sourced packages | `architecture_doc_source_blocked` |
| Five card markers without inv specs | `package_manifest_inferred` (confirmed) |
| Explicit `source_spec_id` on all manifests | deferred — 0/186 explicit |
| PSI runtime | deferred_non_launch_blocker |
