# Active Intelligence Authority Manifest

**Version:** 1.0.0 (ARCH-RT-5)  
**Updated:** 2026-05-30

## Wave 1 card evidence

| subsystem_id | Authority module | Artefact / source |
|--------------|------------------|-------------------|
| `wave1_met_glycaemic_control` | `health_system_card_evidence.py` | `compiled/health_system_cards/wave1_met_glycaemic_control.yaml` |
| All other Wave 1 subsystems | `wave1_subsystem_evidence.py` | Hard-coded `_Wave1SubsystemDef` (classified legacy) |

## Root-cause / hypothesis

| signal_id | Production authority | Shadow authority |
|-----------|---------------------|------------------|
| All 41 registered signals | `load_root_cause_hypotheses.py` + `ROOT_CAUSE_TARGET_SPECS` | — |
| `signal_vitamin_d_low` | `vitamin_d_low_hypotheses_v1.yaml` | `compiled_hypothesis_registry_v1.py` |

## Signal identity

| Component | Authority |
|-----------|-----------|
| Runtime activation frames | `signal_activation_identity_v1.py` (ARCH-RT-2) |
| Signal evaluation | `SignalEvaluator` (unchanged ARCH-RT-5) |

## PSI

| Layer | Authority | Runtime |
|-------|-----------|---------|
| Signal semantics | `promoted_signal_intelligence.yaml` per package | **Not consumed** (deferred) |

## Estate index

`knowledge_bus/compiled/estate_index_v1.yaml` — linkage for launch-included compiled pilots only.
