# ARCH-CONV-D — STOP C identity / runtime non-change proof

**Work ID:** `ARCH-CONV-D`  
**Branch:** `feature/arch-conv-d-alt-identity-closure`  
**Date (UTC):** 2026-07-30  
**Author role:** Cursor (`healthiq-core-engine`) — implementation evidence only  
**Status:** `AWAITING_INDEPENDENT_STOP_C_APPROVAL`  
**STOP A reference:** `ARCH-CONV-D-STOP-A-HOA-2026-07-30`  
**Decision encoded:** `MERGE_TO_SIGNAL_ALT_HIGH`  
**Automation Bus finish:** **NOT RUN** (forbidden until independent STOP C)

This document is a review submission, not self-certification.

---

## Governed identity relationship recorded

| Claim | Evidence |
|---|---|
| Canonical future ALT identity | `signal_alt_high` |
| Legacy predecessor / context implementation | `signal_hepatic_alt_context` |
| Relationship artefact | `knowledge_bus/governance/arch_conv_d_alt_identity_relationship_v1.yaml` |
| Decision register | `docs/architecture/ARCH-CONV-D_identity_decision_register.yaml` (`PHASE_1_COMPLETE_AWAITING_STOP_C`) |
| HOA decision | `docs/architecture/ARCH-CONV-D_STOP_A_head_of_architecture_decision.md` |
| Identity-index encoding | `signal_hepatic_alt_context` family added as `promotion_state: superseded`, `runtime_authority_status: none`, `superseded_by: pkg_s24_alt_high_hepatocellular_injury`; s24 Hy's Law frame `supersedes: pkg_hepatic_alt_context` |
| Runtime alias | **Not created** (`runtime_alias_created: false`) |
| Legacy WHY owner | Remains `signal_hepatic_alt_context` → `alt_hypotheses_v1.yaml` |
| Threshold flag | Mandatory ARCH-CONV-E precondition recorded |
| `hepatocellular_injury_axis` | Reserved for ARCH-CONV-E; not created |

The next ALT migration package (ARCH-CONV-E) now has one unambiguous canonical
target: `signal_alt_high`, with an explicit governed blocker set for thresholds,
axis design, medical roles, and legacy WHY transfer.

---

## No-behaviour-change proof checklist

| Requirement | Result | Evidence |
|---|---|---|
| Approved identity relationship recorded deterministically | PASS | relationship YAML + decision register + identity-index supersession fields |
| No ALT WHY frame compiled / activated / promoted / medically adjudicated | PASS | no compiled ALT artefacts; no `_PILOT_SIGNAL_IDS` ALT add; medical_decisions_made: false |
| No legacy ALT WHY loader or runtime reachability change | PASS | `root_cause_registry_v1.py` unchanged; `alt_hypotheses_v1.yaml` unchanged; still only `signal_hepatic_alt_context` |
| No ALT signal activation logic or hardcoded threshold change | PASS | both `signal_library.yaml` files unchanged |
| No Pass 3 candidate gained authority | PASS | no compiled/register promotion of Pass 3 ALT frames |
| No `cholestatic_source_axis` behaviour change | PASS | `signal_authority_collision_model_v1.yaml` unchanged |
| AST and bilirubin/hyperbilirubinemia unchanged | PASS | no AST/bilirubin file edits |
| No frontend file changed | PASS | no `frontend/` paths in diff |
| Existing focused authority and signal tests stable | PASS | see verification commands below |
| Selection does not depend on filename / lexical / package / filesystem / load order | PASS | relationship is explicit signal_id + package_id fields; no loader order change |

---

## Diff boundary (Phase 1 + STOP C evidence)

Expected changed paths only:

```text
docs/architecture/ARCH-CONV-D_*
knowledge_bus/governance/arch_conv_d_alt_identity_relationship_v1.yaml
knowledge_bus/governance/medical_frame_identity_index_v1.yaml
```

Forbidden paths must remain untouched:

```text
backend/core/**
knowledge_bus/packages/pkg_s24_alt_high_hepatocellular_injury/signal_library.yaml
knowledge_bus/packages/pkg_hepatic_alt_context/signal_library.yaml
knowledge_bus/root_cause/hypotheses/alt_hypotheses_v1.yaml
knowledge_bus/governance/compiled_why_authority_register_v1.yaml
knowledge_bus/governance/root_cause_authority_register_v1.yaml
knowledge_bus/governance/signal_authority_collision_model_v1.yaml
knowledge_bus/compiled/**
frontend/**
```

---

## Verification commands and results

```text
python backend/scripts/validate_medical_frame_identity_index.py
→ validation_status: PASS; errors: 0

python -m pytest backend/tests/regression/test_med_frame_identity_index.py -q
→ 11 passed

python -m pytest backend/tests/unit/test_root_cause_v1_homocysteine.py::test_root_cause_v1_alt_hypotheses_emit_for_alt_signal -q
→ 1 passed

Forbidden runtime/threshold/frontend/compiled paths vs main: unchanged
  - root_cause_registry_v1.py
  - why_authority_v1.py
  - signal_evaluator.py
  - signal_authority_collision_resolver.py
  - both ALT signal_library.yaml files
  - alt_hypotheses_v1.yaml
  - compiled_why_authority_register_v1.yaml
  - signal_authority_collision_model_v1.yaml
  - frontend/
```

Targeted assertions:

1. Identity-index validator PASS with the new superseded hepatic family.
2. ALT WHY still emits only for `signal_hepatic_alt_context`.
3. Diff excludes all forbidden runtime/threshold/frontend/compiled paths above.

---

## STOP C status

`AWAITING INDEPENDENT HEAD OF ARCHITECTURE STOP C APPROVAL`

Do not run Automation Bus finish or merge until that approval is recorded.
