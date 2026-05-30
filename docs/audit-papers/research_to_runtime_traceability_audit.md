# Research-to-Runtime Traceability Audit

**Work package:** ARCH-RT-5  
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

### Vitamin D hypothesis (shadow)

```text
inv_vitamin_d_low_deficiency_v1.yaml (research authority)
  → manual pilot compile (ARCH-RT-4)
  → knowledge_bus/compiled/hypotheses/signal_vitamin_d_low.yaml
  → compile manifest: compiled/manifests/arch_rt4_vitamin_d_hypothesis.yaml
  → compiled_hypothesis_registry_v1.load_shadow_compiled_hypothesis() [shadow only]
  → (not yet) compile_root_cause_v1()
```

Production vitamin D WHY still traces to `vitamin_d_low_hypotheses_v1.yaml`.

## Prohibited paths (verified absent)

| Prohibited path | Status |
|-----------------|--------|
| Raw investigation spec runtime reads | **None introduced** |
| Frontend medical inference | **None introduced** |
| Consumer-visible raw `source_trace` | **Filtered** |

## Gaps (classified)

| Gap | Classification |
|-----|----------------|
| 6 Wave 1 subsystems on hard-coded card path | legacy_retained_with_justification |
| 186-package provenance backfill | deferred_non_launch_blocker |
| kb52c batch frames | blocked_pending_spec_extraction |
| Compiled hypothesis runtime promotion | deferred_non_launch_blocker |
| PSI runtime | deferred_non_launch_blocker |
