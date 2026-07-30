# ARCH-CONV-C — Target-to-Frame and Canonical-Source Map

**Work ID:** `ARCH-CONV-C`  
**Date (UTC):** 2026-07-30  
**State:** `PHASE_0_DRAFT_AWAITING_STOP_A_APPROVAL`  
**Purpose:** Identity/source and collision-boundary reconstruction only. No medical
decision, compilation, activation, collision-policy population, or legacy
disconnection is authorised by this map.

Identity is derived from embedded source fields:

```text
activation_key = signal_id::source_spec_id
```

## Scope summary

| Category | Identities |
|---|---|
| Provisional migration targets | `signal_alp_high::inv_alp_high_bone_biliary`; `signal_ggt_high::inv_ggt_high_hepatic` |
| ALP Pass 3 candidates | `signal_alp_high::inv_alp_high_cholestatic_pattern`; `signal_alp_high::inv_alp_high_high_bone_turnover_pattern` |
| GGT Pass 3 candidates | `signal_ggt_high::inv_ggt_high_hepatobiliary_cholestatic_context`; `signal_ggt_high::inv_ggt_high_alcohol_or_enzyme_induction_context` |
| Collision boundary | `liver_injury_axis` placeholder |
| Explicit exclusions | `signal_alt_high`; `signal_hepatic_alt_context`; `signal_ast_high`; `signal_hyperbilirubinemia`; retired `signal_bilirubin_high`; `signal_alp_low` |
| Active compiled ALP/GGT WHY | none |
| Active legacy ALP/GGT WHY | both target families |

## Canonical target identities

| signal_id | Embedded `spec_id` | Canonical source | SHA-256 | Activation key |
|---|---|---|---|---|
| `signal_alp_high` | `inv_alp_high_bone_biliary` | `knowledge_bus/research/investigation_specs/inv_alp_high_bone_biliary.yaml` | `1a8e2da95d4aeae0505897da445709632f5ea4c39c34d4aaf906ef3462eb61ef` | `signal_alp_high::inv_alp_high_bone_biliary` |
| `signal_ggt_high` | `inv_ggt_high_hepatic` | `knowledge_bus/research/investigation_specs/inv_ggt_high_hepatic.yaml` | `3e2cc6cf074dcb73b825e9a97fe93b43c4f50dc874a0c85cbaa34b754d46c8a1` | `signal_ggt_high::inv_ggt_high_hepatic` |

Embedded evidence is at lines 1-3 of each source. Filenames and package names
were not used to infer identity.

## Frame map

| Scope role | Activation key | Source type | Current runtime signal state | Current WHY state | Phase 0 disposition |
|---|---|---|---|---|---|
| Migration target | `signal_alp_high::inv_alp_high_bone_biliary` | Canonical investigation-spec YAML + S24 package | Loaded; `SOURCE_DOCUMENT_DERIVED` | Family-level legacy WHY | `PENDING_STOP_A_AND_MEDICAL_GATE` |
| ALP candidate | `signal_alp_high::inv_alp_high_cholestatic_pattern` | Pass 3 v3 record in `Batch_5_Pass_3.json` + translated package | Loaded; provenance `BLOCKED` | Same family-level legacy WHY if fired | `PASS3_MEDICAL_DISPOSITION_REQUIRED` |
| ALP candidate | `signal_alp_high::inv_alp_high_high_bone_turnover_pattern` | Pass 3 v3 record in `Batch_5_Pass_3.json`; no runtime package found | Not loaded as a separate runtime frame | No separate WHY authority | `PASS3_UNPACKAGED_MEDICAL_DISPOSITION_REQUIRED` |
| Migration target | `signal_ggt_high::inv_ggt_high_hepatic` | Canonical investigation-spec YAML + S24 package | Loaded; `SOURCE_DOCUMENT_DERIVED` | Family-level legacy WHY | `PENDING_STOP_A_AND_MEDICAL_GATE` |
| GGT candidate | `signal_ggt_high::inv_ggt_high_hepatobiliary_cholestatic_context` | Pass 3 v3 record in `Batch_6_Pass_3.json` + package + staged PSI | Loaded; provenance `BLOCKED` | Same family-level legacy WHY if fired | `PASS3_MEDICAL_DISPOSITION_REQUIRED` |
| GGT candidate | `signal_ggt_high::inv_ggt_high_alcohol_or_enzyme_induction_context` | Pass 3 v3 record in `Batch_6_Pass_3.json` + package + staged PSI | Loaded; provenance `BLOCKED` | Same family-level legacy WHY if fired | `PASS3_MEDICAL_DISPOSITION_REQUIRED` |

The live `SignalRegistry` exposes two ALP-high activation keys and three GGT-high
activation keys. The Pass 3 package frames are signal-layer candidates, not
active compiled WHY authority. Package presence or translated PSI presence does
not itself ratify medical WHY authority.

## Legacy WHY map

| signal_id | Registry | Loader | Asset |
|---|---|---|---|
| `signal_alp_high` | `backend/core/knowledge/root_cause_registry_v1.py:75` | `backend/core/knowledge/load_root_cause_hypotheses.py:159-160` | `knowledge_bus/root_cause/hypotheses/alp_high_hypotheses_v1.yaml` |
| `signal_ggt_high` | `backend/core/knowledge/root_cause_registry_v1.py:67` | `backend/core/knowledge/load_root_cause_hypotheses.py:139-140` | `knowledge_bus/root_cause/hypotheses/ggt_high_hypotheses_v1.yaml` |

`backend/core/knowledge/why_authority_v1.py` does not include either signal in
the compiled cohort, so its out-of-cohort rule preserves legacy selection. No
ALP/GGT row exists in:

- `knowledge_bus/governance/compiled_why_authority_register_v1.yaml`
- `knowledge_bus/governance/root_cause_authority_register_v1.yaml`
- `knowledge_bus/compiled/estate_index_v1.yaml`

No ALP/GGT compiled hypothesis artefact or compile manifest is registered.

## Candidate evidence boundaries

### ALP

- The canonical target states that ALP is present in liver and bone and requires
  GGT source discrimination.
- The canonical target uses high GGT plus high bilirubin for escalation, while
  calcium provides bone-context corroboration.
- Pass 3 separates a cholestatic frame from a high-bone-turnover frame.
- The Pass 3 coverage audit incorrectly groups two ALP-low frames with two
  ALP-high frames under `signal_alp_high`; only the two high-direction frames
  above are candidates for this package.
- The legacy ALP WHY asset emits hepatobiliary/cholestatic language from the
  ALP-high signal and records GGT only as missing-data context. This creates a
  risk of hepatic interpretation where bone origin remains plausible.

### GGT

- The canonical target describes GGT as sensitive but non-specific and includes
  hepatobiliary stress, alcohol use, NAFLD, and enzyme-inducing medicines.
- Pass 3 separates hepatobiliary/cholestatic context from alcohol/enzyme
  induction context.
- The alcohol/enzyme-induction source explicitly says GGT must not be used alone
  to infer alcohol exposure or liver-disease severity.
- The legacy GGT WHY asset emits a generic hepatic-enzyme pattern and a
  metabolic/inflammatory coupling hypothesis; it does not preserve the Pass 3
  causal-versus-context distinction.

## `liver_injury_axis` boundary

`knowledge_bus/governance/signal_authority_collision_model_v1.yaml:110-122`
contains an unadjudicated placeholder:

- `biological_axis: hepatocellular_injury`
- `primary_signal_family: null`
- `supporting_signal_families: []`
- all four collision-policy fields are `null`
- `runtime_action: none_governance_only`
- `requires_runtime_support: false`
- notes mention ALT / AST / GGT / bilirubin, but omit ALP

The runtime collision resolver loads this model but enforces only adjudicated
groups. Therefore `liver_injury_axis` currently has no runtime selection policy.
Its omission of ALP is a recorded naming/scope gap, not permission to infer a
policy.

## Exclusion boundaries

| Excluded identity | Repository state to preserve |
|---|---|
| `signal_alt_high` | Multiple active signal frames; not a root-cause registry family |
| `signal_hepatic_alt_context` | Separate legacy root-cause family at `root_cause_registry_v1.py:32`; not to be merged with `signal_alt_high` |
| `signal_ast_high` | No canonical WHY target found; no target may be invented |
| `signal_bilirubin_high` | Retired WHY identity under ARCH-CONV-A |
| `signal_hyperbilirubinemia` | Surviving legacy family, but no canonical investigation spec; unchanged |
| `signal_alp_low` | Separate direction and legacy WHY family at `root_cause_registry_v1.py:76`; the audit's grouped ALP rows do not widen scope |

## Existing validation and regression authorities

- Signal activation and package cases:
  `backend/tests/unit/test_signal_evaluator.py`
- Activation identity and duplicate-key failure:
  `backend/tests/unit/test_signal_activation_identity_v1.py`,
  `backend/tests/unit/test_duplicate_authority_resolution_v1.py`
- Collision enforcement:
  `backend/tests/regression/test_signal_authority_collision_enforcement.py`
- Compiled WHY selection and role enforcement:
  `backend/tests/unit/test_why_authority_pkg3.py`,
  ARCH-CONV-A/B STOP C suites
- Legacy liver/root-cause regression:
  `backend/tests/unit/test_root_cause_v1_homocysteine.py`
- Liver card/scoring boundaries:
  `backend/tests/regression/test_kb_util1_pass3_card_evidence_compile_and_consume.py`,
  `backend/tests/unit/test_health_system_card_evidence_arch_rt3.py`,
  `backend/tests/unit/test_health_system_card_evidence_arch_rt5b.py`,
  `backend/tests/unit/test_wave1_liver_d7.py`
- GGT and bilirubin aliases:
  `backend/tests/regression/test_ggt_alias_regression.py`,
  `backend/tests/regression/test_bilirubin_alias_regression.py`

## STOP A disposition

No row in this map constitutes medical approval, collision-policy approval,
runtime authorisation, or legacy retirement. All implementation-relevant roles
remain pending independent STOP A, Head of Medical Research Gate 1, and Anthony
Gate 2.
