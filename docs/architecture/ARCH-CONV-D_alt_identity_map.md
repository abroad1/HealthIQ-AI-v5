# ARCH-CONV-D — ALT identity map

**Work ID:** `ARCH-CONV-D`  
**Branch:** `feature/arch-conv-d-alt-identity-closure`  
**Baseline:** `main` / `origin/main` = `e2d7ce38adc095387e632c6e50ebad68110cbe10` (ARCH-CONV-C merged)  
**Author role:** Cursor (`healthiq-core-engine`) — repository evidence only  
**Status:** Phase 0 identity evidence; no identity decision recorded

This map is identity and authority reconstruction only. It does not approve,
reject, compile, promote, or medically classify any ALT frame.

---

## 1. Live ALT signal identities

### 1.1 `signal_alt_high`

| Field | Repository fact |
|---|---|
| signal_id | `signal_alt_high` |
| Canonical research identity | Embedded in investigation spec: `spec_id: inv_alt_high_hepatocellular_injury`; `signal_id: signal_alt_high` (`knowledge_bus/research/investigation_specs/inv_alt_high_hepatocellular_injury_v1.yaml:1-2`) |
| Canonical source path | `knowledge_bus/research/investigation_specs/inv_alt_high_hepatocellular_injury_v1.yaml` |
| Canonical source SHA-256 | `7189a0761558937d4dd4397e823bbe06c7bee0b13ef9bbe0b3afc70a73b7413a` |
| Primary package | `pkg_s24_alt_high_hepatocellular_injury` |
| Package source_document | `knowledge_bus/research/investigation_specs/inv_alt_high_hepatocellular_injury_v1.yaml` (`package_manifest.yaml:8`) |
| translation_mode | `creation` (`package_manifest.yaml:9`) |
| Explicit on-disk `source_spec_id` in package YAML | **Absent** — runtime activation identity is derived from the investigation-spec `source_document` stem (without `_vN`) as `inv_alt_high_hepatocellular_injury` |
| Identity-index status | **Present** under `signal_family_id: signal_alt_high` — six frames (`medical_frame_identity_index_v1.yaml:124-277`) |
| Primary marker | `alt` |
| Signal-layer reachability | Live via `SignalRegistry` package glob load (`backend/core/analytics/signal_evaluator.py`) |
| Legacy WHY asset | **None** — not listed in `ROOT_CAUSE_TARGET_SPECS` |
| Compiled WHY status | **None** — absent from `compiled_why_authority_register_v1.yaml` |
| Runtime WHY-authority status | Out of `_PILOT_SIGNAL_IDS` (`why_authority_v1.py:22-46`) → legacy mode if targeted; compiler never targets this signal_id → **no WHY emit path** |

Live activation keys under this family:

```text
signal_alt_high::inv_alt_high_hepatocellular_injury
signal_alt_high::inv_alt_high_hepatocellular_injury_pattern
signal_alt_high::inv_alt_high_metabolic_steatotic_liver_pattern
signal_alt_high::inv_alt_high_muscle_source_or_exertional_pattern
```

Additional live packages for Pass 3 frames (all `signal_id: signal_alt_high`, `translation_mode: creation`):

- `pkg_kb52c_alt_high_hepatocellular_injury_pattern`
- `pkg_kb52c_alt_high_metabolic_steatotic_liver_pattern`
- `pkg_kb52c_alt_high_muscle_source_or_exertional_pattern`

### 1.2 `signal_hepatic_alt_context`

| Field | Repository fact |
|---|---|
| signal_id | `signal_hepatic_alt_context` |
| Embedded canonical investigation-spec identity | **Absent** |
| Package source_document | `docs/architecture/HealthIQ_Investigation_Layer.md` (`pkg_hepatic_alt_context/package_manifest.yaml:9`) — architecture doc, not an investigation spec |
| Inferred runtime source_spec_id | `inv_alt_context` (derived from package body); **no** `inv_alt_context` investigation-spec YAML exists |
| package_id | `pkg_hepatic_alt_context` |
| translation_mode | `creation` (`package_manifest.yaml:10`) |
| Identity-index status | **Absent** — zero `signal_hepatic_alt_context` rows in `medical_frame_identity_index_v1.yaml` |
| Primary marker | `alt` |
| Signal-layer reachability | Live via same package glob loader |
| Legacy WHY asset | **Owns** `knowledge_bus/root_cause/hypotheses/alt_hypotheses_v1.yaml` (`primary_signal_id: signal_hepatic_alt_context` at line 4) |
| Registry path | `ROOT_CAUSE_TARGET_SPECS` → `signal_hepatic_alt_context` → `load_alt_hypotheses_v1` → `alt_hypotheses_v1.yaml` (`backend/core/knowledge/root_cause_registry_v1.py:32`; `load_root_cause_hypotheses.py:79-80`) |
| Compiled WHY status | **None** |
| Runtime WHY-authority status | Out of pilot → legacy family-level WHY on this signal_id only |

Live activation key:

```text
signal_hepatic_alt_context::inv_alt_context
```

---

## 2. Pass 3 duplicate-family listings

The same three Pass 3 candidates are listed under **both** ALT packages in
`pass3_frame_coverage_audit_v1.yaml`:

| Candidate | Listed under `signal_hepatic_alt_context` | Listed under `signal_alt_high` | Translated package signal_id |
|---|---|---|---|
| `inv_alt_high_hepatocellular_injury_pattern` | yes (`:111-119`) | yes (`:459-467`) | `signal_alt_high` only |
| `inv_alt_high_metabolic_steatotic_liver_pattern` | yes | yes | `signal_alt_high` only |
| `inv_alt_high_muscle_source_or_exertional_pattern` | yes | yes | `signal_alt_high` only |

| Candidate | activation_key | Provenance (live) | Signal-layer | WHY authority |
|---|---|---|---|---|
| Hepatocellular injury pattern | `signal_alt_high::inv_alt_high_hepatocellular_injury_pattern` | BLOCKED (batch JSON source) | live | none registered |
| Metabolic steatotic liver pattern | `signal_alt_high::inv_alt_high_metabolic_steatotic_liver_pattern` | BLOCKED | live | none registered |
| Muscle / exertional pattern | `signal_alt_high::inv_alt_high_muscle_source_or_exertional_pattern` | BLOCKED | live | none registered |

Cross-family listing in the coverage audit is inventory evidence only. Translated
Pass 3 packages emit `signal_alt_high`, not `signal_hepatic_alt_context`.

Additional non-Pass-3 ALT candidate:

- `inv_alt_high_hepatocellular_injury` — s24 / research YAML identity;
  activation `signal_alt_high::inv_alt_high_hepatocellular_injury`; indexed as
  three medical frames (Hy's Law active; severity + cholestatic marked inactive
  in the identity index).

---

## 3. Behavioural differences (signal layer)

| Aspect | `signal_alt_high` (s24) | `signal_hepatic_alt_context` |
|---|---|---|
| Activation | `lab_range_exceeded` on ALT | `lab_range_exceeded` on ALT |
| Escalation model | Three separate `all_of` override rules | One `any_of` multimarker override |
| Severity rule | ALT `> 120.0` | none equivalent |
| Hy's Law style rule | bilirubin `> 20.0` (`all_of`) | bilirubin `> 20.0` as one arm of `any_of` |
| Cholestatic arm | ALP `> 130.0` (`all_of`) | ALP `> 130.0` as one arm of `any_of` |
| Extra multimarker arms | — | AST `> 45.0`, GGT `> 60.0` |
| Supporting metrics | ast, ggt, alp, bilirubin, **albumin** | ast, ggt, alp, bilirubin |
| WHY ownership | none | owns legacy ALT WHY |

Runtime signal logic is therefore **not identical**.

---

## 4. Hardcoded-threshold governance flag

**FLAG: HARDCODED_ALT_CONTEXT_THRESHOLDS_NOT_FROM_BIOMARKER_SSOT**

| Value | Metric | Package / rule | File |
|---:|---|---|---|
| `9999.0` | alt | placeholder (activation is lab_range) | both ALT packages + kb52c libraries |
| `120.0` | alt | s24 severity `all_of` | `pkg_s24_alt_high_hepatocellular_injury/signal_library.yaml:53` |
| `20.0` | bilirubin | s24 Hy's Law `all_of` | `:61` |
| `130.0` | alp | s24 mixed cholestatic `all_of` | `:69` |
| `45.0` | ast | hepatic `any_of` | `pkg_hepatic_alt_context/signal_library.yaml:60` |
| `60.0` | ggt | hepatic `any_of` | `:64` |
| `130.0` | alp | hepatic `any_of` | `:68` |
| `20.0` | bilirubin | hepatic `any_of` | `:72` |

Baseline ALT activation uses runtime `lab_ranges` (lab-range path). The numeric
override cutoffs above are package literals, not governed biomarker SSOT reads.

If STOP A retains or transfers any of this override behaviour, the threshold
issue is a mandatory successor (ARCH-CONV-E) precondition / blocker. This package
must not remediate the thresholds.

---

## 5. Legacy WHY and authority-selection boundary

```text
ROOT_CAUSE_TARGET_SPECS
  → signal_hepatic_alt_context
  → load_alt_hypotheses_v1()
  → knowledge_bus/root_cause/hypotheses/alt_hypotheses_v1.yaml
```

- `signal_alt_high` has **no** registry WHY target and **no** compiled WHY row.
- Legacy ALT WHY selection is **family-level** on `signal_hepatic_alt_context`,
  not activation-key-level.
- Pilot/compiled WHY uses activation-key selection; ALT is outside that cohort.
- Package discovery uses sorted filesystem glob for iteration only; duplicate
  activation-key resolution is authority-ranked and forbids path/package/load-order
  wins. Within a single package, same-rank override rules resolve to the later YAML
  rule.

---

## 6. Exclusion boundaries

| Boundary | Status |
|---|---|
| AST (`signal_ast_high`) | Outside ARCH-CONV-D. No identity-index family; no AST authority creation in this package. |
| ALP/GGT / `cholestatic_source_axis` | Established by ARCH-CONV-C; adjudicated and runtime-enforced. Policy notes ALT remains outside (`signal_authority_collision_model_v1.yaml:129-139`). ARCH-CONV-D must not alter it. |
| Bilirubin / hyperbilirubinemia | Outside ARCH-CONV-D. Live signals exist; ARCH-CONV-C preserved future independence. No bilirubin authority change here. |
| Frontend | No frontend change authorised or performed. |

---

## 7. STOP A decision (recorded)

**Reference:** `ARCH-CONV-D-STOP-A-HOA-2026-07-30`  
**Selected option:** `MERGE_TO_SIGNAL_ALT_HIGH`

| Question | Approved answer |
|---|---|
| Canonical survivor | `signal_alt_high` — sole canonical future ALT authority identity |
| Predecessor | `signal_hepatic_alt_context` — legacy predecessor/context implementation; not a separately canonical medical family |
| Runtime alias | **Not created** (behaviours are non-identical) |
| Legacy WHY owner | Remains `signal_hepatic_alt_context` temporarily until ARCH-CONV-E |
| Threshold flag | Mandatory ARCH-CONV-E precondition |
| `hepatocellular_injury_axis` | Reserved / required for ARCH-CONV-E design review; not created here |

Governance encoding:

- `knowledge_bus/governance/arch_conv_d_alt_identity_relationship_v1.yaml`
- identity-index supersession fields (non-runtime index; `runtime_consumed: false`)
- `docs/architecture/ARCH-CONV-D_identity_decision_register.yaml`

## 8. Architecture questions answered by STOP A

Final options were PENDING at Phase 0 submission and are now recorded in the
approved decision register. Medical WHY roles, compile/activate, and threshold
remediation remain out of scope for ARCH-CONV-D.
