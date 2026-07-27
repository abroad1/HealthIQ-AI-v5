# ARCH-CONV-A WHY identity alias register (D-3)

**Work ID:** `ARCH-CONV-A`  
**Purpose:** Record reversible, non-medical WHY-target identity aliases after STOP A ratification.  
**Runtime emit authority:** unchanged for surviving identities; aliased IDs are **not** iterated by `get_root_cause_targets()`.

```yaml
schema_version: "1.0.0"
work_id: ARCH-CONV-A
ratification_ref: docs/architecture/ARCH-CONV-A_STOP_A_ratification_record.md
entries:
  - retired_signal_id: signal_bilirubin_high
    surviving_signal_id: signal_hyperbilirubinemia
    disposition: MERGE_TO_ONE
    why_registry_state: REMOVED_FROM_ROOT_CAUSE_TARGET_SPECS
    legacy_asset_retained: knowledge_bus/root_cause/hypotheses/bilirubin_high_hypotheses_v1.yaml
    survivor_legacy_asset: knowledge_bus/root_cause/hypotheses/hyperbilirubinemia_hypotheses_v1.yaml
    medical_frame_approval: NONE
    notes: >
      Signal-family identity merge only. Provisional Gilbert / haemolytic /
      hepatobiliary frames remain unapproved. No compile or runtime WHY
      activation authorised by this alias.
```

Human-readable mirror of `knowledge_bus/governance/arch_conv_a_why_identity_alias_register_v1.yaml`.
