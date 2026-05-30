# Active Intelligence Authority Manifest

**Version:** 1.2.0 (ARCH-RT-5E)  
**Updated:** 2026-05-30

## Wave 1 card evidence

| subsystem_id | Authority module | Artefact / source | Launch |
|--------------|------------------|-------------------|--------|
| `wave1_met_glycaemic_control` | `health_system_card_evidence.py` | `compiled/health_system_cards/wave1_met_glycaemic_control.yaml` | launch_included_compiled |
| `wave1_cv_lipid_transport` | `health_system_card_evidence.py` | `compiled/health_system_cards/wave1_cv_lipid_transport.yaml` | launch_included_compiled |
| `wave1_cv_homocysteine_pathway` | `health_system_card_evidence.py` | `compiled/health_system_cards/wave1_cv_homocysteine_pathway.yaml` | launch_included_compiled |
| `wave1_cv_vascular_strain` | `health_system_card_evidence.py` | `compiled/health_system_cards/wave1_cv_vascular_strain.yaml` | launch_included_compiled |
| `wave1_met_insulin_metabolic` | `health_system_card_evidence.py` | `compiled/health_system_cards/wave1_met_insulin_metabolic.yaml` | launch_included_compiled |
| `wave1_liv_enzyme_pattern` | `health_system_card_evidence.py` | `compiled/health_system_cards/wave1_liv_enzyme_pattern.yaml` | launch_included_compiled |
| `wave1_liv_processing_context` | `health_system_card_evidence.py` | `compiled/health_system_cards/wave1_liv_processing_context.yaml` | launch_included_compiled |

Legacy hard-coded Wave 1 card path: **none remaining** (estate index `wave1_subsystems_legacy_hard_coded` empty).

## Root-cause / hypothesis

| signal_id | Production authority | Notes |
|-----------|---------------------|-------|
| 40 non-pilot registered signals | `load_root_cause_hypotheses.py` + `ROOT_CAUSE_TARGET_SPECS` | Legacy YAML unchanged |
| `signal_vitamin_d_low` | `compiled_hypothesis.py` via `root_cause_compiler_v1._compile_compiled_hypothesis_finding()` | Runtime promoted (ARCH-RT-5C); legacy YAML retained |

## Signal identity

| Component | Authority |
|-----------|-----------|
| Runtime activation frames | `signal_activation_identity_v1.py` (ARCH-RT-2) |
| Signal evaluation | `SignalEvaluator` (unchanged) |

## PSI (ARCH-RT-5E decision)

| Layer | Authority | Runtime | Launch classification |
|-------|-----------|---------|------------------------|
| Signal semantics | `promoted_signal_intelligence.yaml` per package (20× `pkg_kb47_*` opt-in) | **Not consumed** | **`deferred_non_launch_blocker`** |

Evidence: `docs/audit-papers/ARCH-RT-5E_psi_runtime_wiring_decision_audit.md`. Loader exists (`load_promoted_signal_intelligence.py`) for validation/ingest only; no orchestrator, card, root-cause, or report compiler import.

## Estate index

`knowledge_bus/compiled/estate_index_v1.yaml` — launch-included compiled card (7) and hypothesis (1) artefacts with resolving compile manifests.

## Package provenance (ARCH-RT-5D)

| Metric | Value |
|--------|------:|
| Packages classified | 186 / 186 |
| Explicit `source_spec_id` on manifest | 0 |
| Launch-relevant compile manifest hashes | Refreshed (8 manifests) |

See `docs/audit-papers/ARCH-RT-5D_package_provenance_backfill_audit.md`.
