# ARCH-CONV-D — STOP A ALT identity and authority closure

**Work ID:** `ARCH-CONV-D`  
**Date (UTC):** 2026-07-30  
**Author role:** Cursor (`healthiq-core-engine`) — repository evidence only  
**Authority:** Automation Bus SOP v1.3.1; Knowledge Bus SOP v1.3.1; Pass 3
Promotion Protocol v1.1  
**Status:** `STOP_A_SUBMISSION_READY_FOR_HEAD_OF_ARCHITECTURE`

This record contains no identity approval, medical approval, runtime
authorisation, compilation, authority registration, legacy disconnection, or
threshold remediation.

Companion artefacts:

- `docs/architecture/ARCH-CONV-D_alt_identity_map.md`
- `docs/architecture/ARCH-CONV-D_identity_decision_register.yaml`

---

## Work-package state

| Field | Evidence |
|---|---|
| Branch | `feature/arch-conv-d-alt-identity-closure` |
| Baseline | local `main == origin/main == e2d7ce38adc095387e632c6e50ebad68110cbe10` (ARCH-CONV-C merge) before branch creation |
| ARCH-CONV-D artefacts before branch | none |
| Unmerged ALT preparation branch | none found |
| Stash | empty; no convenience stash created |
| Change boundary reached | Phase 0 evidence only |
| Identity / medical / runtime decisions | **None** |
| ARCH-CONV-C artefacts modified | **None** |

---

## Evidence classification legend

| Class | Meaning |
|---|---|
| **Repository fact** | Directly observable from current files or loaders |
| **Architecture inference** | Structural interpretation offered for STOP A; not a decision |
| **Unresolved medical meaning** | Requires Head of Medical Research if STOP A cannot decide from identity alone |

---

## Stage 1A — Identity preflight

### `signal_alt_high`

| Field | Class | Evidence |
|---|---|---|
| signal_id | Repository fact | `pkg_s24_alt_high_hepatocellular_injury/signal_library.yaml:8` |
| Embedded canonical `spec_id` | Repository fact | `inv_alt_high_hepatocellular_injury_v1.yaml:1` = `inv_alt_high_hepatocellular_injury`; line 2 = `signal_id: signal_alt_high` |
| Package on-disk `source_spec_id` field | Repository fact | Absent in package YAML |
| Runtime source identity | Repository fact | Derived from package `source_document` stem → `inv_alt_high_hepatocellular_injury` |
| Canonical path / SHA-256 | Repository fact | `knowledge_bus/research/investigation_specs/inv_alt_high_hepatocellular_injury_v1.yaml` / `7189a0761558937d4dd4397e823bbe06c7bee0b13ef9bbe0b3afc70a73b7413a` |
| package_id / translation_mode | Repository fact | `pkg_s24_alt_high_hepatocellular_injury` / `creation` |
| Identity-index status | Repository fact | Present: `medical_frame_identity_index_v1.yaml:124-277` (six frames) |
| Signal-layer reachability | Repository fact | Live; primary_metric `alt`; four activation keys including s24 + three Pass 3 |
| Legacy WHY | Repository fact | **Absent** from `ROOT_CAUSE_TARGET_SPECS` (`root_cause_registry_v1.py`) |
| Compiled WHY | Repository fact | **Absent** from `compiled_why_authority_register_v1.yaml` |
| Runtime WHY status | Repository fact | Not in `_PILOT_SIGNAL_IDS`; no registry target → **no WHY emit path** |

### `signal_hepatic_alt_context`

| Field | Class | Evidence |
|---|---|---|
| signal_id | Repository fact | `pkg_hepatic_alt_context/signal_library.yaml:10` |
| Embedded canonical investigation-spec identity | Repository fact | **Absent** |
| Package source_document | Repository fact | `docs/architecture/HealthIQ_Investigation_Layer.md` (`package_manifest.yaml:9`) |
| Inferred runtime identity | Repository fact | `inv_alt_context` from package body; no matching investigation-spec YAML |
| Identity-index status | Repository fact | **Absent** from `medical_frame_identity_index_v1.yaml` |
| Signal-layer reachability | Repository fact | Live; primary_metric `alt`; key `signal_hepatic_alt_context::inv_alt_context` |
| Legacy WHY ownership | Repository fact | Sole ALT target: `root_cause_registry_v1.py:32` → `load_alt_hypotheses_v1` → `alt_hypotheses_v1.yaml` (`primary_signal_id: signal_hepatic_alt_context`) |
| Compiled WHY | Repository fact | **Absent** |
| Runtime WHY status | Repository fact | Legacy family-level WHY active on this signal_id |

### Required confirmations

| Claim | Verdict | Class |
|---|---|---|
| `signal_alt_high` embeds / binds to `inv_alt_high_hepatocellular_injury` | **Confirmed** via investigation-spec embedded fields and package `source_document` derivation (no literal package YAML `source_spec_id` field) | Repository fact |
| `signal_alt_high` in governed identity index | **Confirmed** | Repository fact |
| `signal_alt_high` has no current legacy or compiled WHY path | **Confirmed** | Repository fact |
| `signal_hepatic_alt_context` has no embedded canonical investigation-spec identity | **Confirmed** | Repository fact |
| `signal_hepatic_alt_context` absent from canonical identity index | **Confirmed** | Repository fact |
| `signal_hepatic_alt_context` owns the legacy ALT WHY loader | **Confirmed** | Repository fact |
| Both signals live; ALT primary marker | **Confirmed** | Repository fact |
| Runtime signal logic not identical | **Confirmed** (different override models, supporting sets, WHY ownership) | Repository fact |

---

## Stage 1B — Parallel-frame reconstruction

| Candidate | activation_key | Listed families (audit) | Translated package signal | Signal layer | WHY |
|---|---|---|---|---|---|
| `inv_alt_high_hepatocellular_injury_pattern` | `signal_alt_high::inv_alt_high_hepatocellular_injury_pattern` | both ALT families | `signal_alt_high` | live / BLOCKED provenance | none |
| `inv_alt_high_metabolic_steatotic_liver_pattern` | `signal_alt_high::inv_alt_high_metabolic_steatotic_liver_pattern` | both ALT families | `signal_alt_high` | live / BLOCKED provenance | none |
| `inv_alt_high_muscle_source_or_exertional_pattern` | `signal_alt_high::inv_alt_high_muscle_source_or_exertional_pattern` | both ALT families | `signal_alt_high` | live / BLOCKED provenance | none |

Additional ALT candidate (not Pass 3 pattern):

- `inv_alt_high_hepatocellular_injury` — s24 research YAML; indexed under
  `signal_alt_high`; no WHY path.

**Identity evidence only.** No Pass 3 frame is approved, rejected, compiled,
promoted, or medically classified by this package.

---

## Stage 1C — Legacy and threshold boundary

### Exact legacy WHY path

```text
backend/core/knowledge/root_cause_registry_v1.py:32
  RootCauseTargetSpec("signal_hepatic_alt_context", load_alt_hypotheses_v1, "alt_hypotheses_v1.yaml")
→ backend/core/knowledge/load_root_cause_hypotheses.py:79-80
→ knowledge_bus/root_cause/hypotheses/alt_hypotheses_v1.yaml
```

### WHY path for `signal_alt_high`

**Absent.**

### Authority selection level

| Layer | Behaviour |
|---|---|
| Compiled / pilot WHY | Activation-key selection via compiled WHY register |
| ALT WHY today | Family-level legacy on `signal_hepatic_alt_context` only |
| Signal discovery | Sorted package glob for iteration; duplicate activation keys are authority-ranked (not path/package/load-order wins) |

### Multi-marker override (`pkg_hepatic_alt_context`)

Rule `hepatic_multimarker_pattern`: four `any_of` conditions — AST>45, GGT>60,
ALP>130, bilirubin>20. Fires if **any** supporting marker exceeds its hardcoded
cutoff while ALT is already lab-range activated.

### Hardcoded thresholds

Recorded in the identity map under flag
`HARDCODED_ALT_CONTEXT_THRESHOLDS_NOT_FROM_BIOMARKER_SSOT`.

**Not remediated in ARCH-CONV-D.** If STOP A retains or transfers the affected
behaviour, this flag becomes a mandatory ARCH-CONV-E precondition.

---

## Architecture questions for Head of Architecture

### Q1 — Superseded predecessor or distinct context family?

**Repository facts:**

- `signal_alt_high` has a governed investigation-spec identity and identity-index
  presence.
- `signal_hepatic_alt_context` has neither; it is architecture-doc anchored and
  owns legacy WHY.
- Both are live ALT-primary signals with non-identical escalation logic.

**Architecture inference (not a decision):**

- Naming and inventory dual-listing can look like predecessor/successor conflict,
  but the distinct multimarker `any_of` escalation is real runtime behaviour that
  is not a pure alias of s24’s three `all_of` rules.

**Unresolved medical meaning:**

- Whether the multimarker context signal is clinically intended as a separate
  family, or only as a temporary investigation-layer stand-in for ALT high.

### Q2 — Which identity should survive?

Unresolved decision options (register PENDING):

1. `MERGE_TO_SIGNAL_ALT_HIGH`
2. `RETAIN_AS_DISTINCT_CONTEXT_SIGNAL`
3. `RETIRE_WITHOUT_TRANSFER`
4. `DEFER_IDENTITY_UNRESOLVED`

### Q3 — Legacy WHY ownership classification

**Repository fact:** legacy ALT WHY is owned exclusively by
`signal_hepatic_alt_context` today.

**Architecture inference:** any future ALT WHY migration package needs an
explicit ownership classification before changing loaders. This package must not
disconnect or transfer that ownership.

### Q4 — Package / alias / predecessor records

STOP A must say whether identity-index relationship fields, predecessor/successor
records, or alias records are required in Phase 1 — still without changing
runtime reachability.

### Q5 — Future `hepatocellular_injury_axis`

ARCH-CONV-C established `cholestatic_source_axis` and preserved ALT independence.
STOP A must say whether a future hepatocellular axis is **required** for later
migration or merely **reserved**. Creating or adjudicating that axis is out of
scope for ARCH-CONV-D.

### Q6 — Hardcoded-threshold blocker

If the surviving or retained identity keeps current override cutoffs, the
threshold flag is a successor blocker for ARCH-CONV-E. If STOP A retires the
behaviour without transfer, the flag remains recorded but may not block identity
closure alone.

---

## Exclusion proof (inspect-only)

| Boundary | Proof |
|---|---|
| AST | No AST authority created; `signal_ast_high` outside this package |
| `cholestatic_source_axis` | Unchanged ARCH-CONV-C policy; ALT explicitly outside (`signal_authority_collision_model_v1.yaml:129-139`) |
| Bilirubin / hyperbilirubinemia | Unchanged; future independence preserved by ARCH-CONV-C |
| Frontend | No frontend files in Phase 0 change set |

---

## STOP A required output

Head of Architecture must record exactly one of:

```text
MERGE_TO_SIGNAL_ALT_HIGH
RETAIN_AS_DISTINCT_CONTEXT_SIGNAL
RETIRE_WITHOUT_TRANSFER
DEFER_IDENTITY_UNRESOLVED
```

and must also specify:

1. surviving identity or distinct-family relationship;
2. predecessor/alias classification;
3. legacy WHY ownership classification;
4. status of existing signal behaviour pending ARCH-CONV-E;
5. whether the threshold issue becomes a mandatory ARCH-CONV-E precondition;
6. whether a future `hepatocellular_injury_axis` is required or merely reserved.

If distinguishing the signals requires medical interpretation, STOP A must request
a bounded Head of Medical Research review before Phase 1 implementation.

---

## STOP A status

`AWAITING INDEPENDENT HEAD OF ARCHITECTURE APPROVAL`

Do not proceed to Phase 1, STOP C, Automation Bus finish, or merge.
