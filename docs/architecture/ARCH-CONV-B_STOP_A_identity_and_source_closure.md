# ARCH-CONV-B — STOP A Identity, Source, and Package-Boundary Closure

**Work ID:** `ARCH-CONV-B`  
**Date (UTC):** 2026-07-30  
**Author role:** Cursor (`healthiq-core-engine`) — repository evidence only  
**Authority:** Automation Bus SOP v1.3.1; `automation_bus/latest_cursor_prompt.md`  
**Status:** `STOP_A_APPROVED_BY_HEAD_OF_ARCHITECTURE`

> **STOP A approval (recorded 2026-07-30):** Head of Architecture approved this
> STOP A evidence in-session and authorised Phase 1 (Gate 1 pack finalisation) only.
> No formal approval reference string was supplied; the Head of Architecture may
> attach one to `head_of_architecture_stop_a_reference` in
> `docs/architecture/ARCH-CONV-B_medical_decision_register.yaml`. Approval does not
> authorise medical decisions, compilation, runtime authority changes, legacy
> disconnection, Automation Bus finish, or Phase 2.

> **Bounded Phase 2 scope extension (recorded 2026-07-30):** Head of Architecture
> authorised the minimum clinician-report contract and compiler changes required
> to preserve governed `why_role` end to end for
> `signal_urea_high::inv_urea_high_renal`. The extension permits one structured
> role field, deterministic propagation, fail-closed validation, and focused
> backend/output tests only. It does not authorise contract redesign, frontend
> medical logic, unrelated report-field changes, eGFR or urate WHY, package-only
> Pass 3 promotion, physical legacy deletion, Automation Bus finish, or merge.

---

## Work package

| Field | Evidence |
|---|---|
| Branch | `feature/arch-conv-b-renal-why-authority` |
| Baseline | `main` / `origin/main` = `290ac180a62681da22d3132653c5cbe25d1dbb80` before branch preparation |
| Preserved preparation | Cherry-picked `31c37a2f8b4dbf06a46a4ecbc474efd2e5c9818a` as `2ad1d3a`; docs only |
| Kernel authority | `automation_bus/state/work_package_active.json` = `ARCH-CONV-B`, matching branch |
| Change boundary reached | Phase 0 and STOP A evidence only |
| Medical decisions | **None made** |
| Compile/runtime/authority changes | **None made** |

## Stage 1A authority preflight

### Causal-WHY authority

| Signal | Current authority | Evidence |
|---|---|---|
| `signal_creatinine_high` | Legacy WHY asset | `backend/core/knowledge/root_cause_registry_v1.py:89`; loader at `backend/core/knowledge/load_root_cause_hypotheses.py:171-172`; asset `knowledge_bus/root_cause/hypotheses/creatinine_high_hypotheses_v1.yaml` |
| `signal_urea_high` | Legacy WHY asset | `backend/core/knowledge/root_cause_registry_v1.py:90`; loader at `backend/core/knowledge/load_root_cause_hypotheses.py:175-176`; asset `knowledge_bus/root_cause/hypotheses/urea_high_hypotheses_v1.yaml` |
| `signal_egfr_low` | No root-cause registry entry and no compiled WHY row | Absent from `backend/core/knowledge/root_cause_registry_v1.py` and `knowledge_bus/governance/compiled_why_authority_register_v1.yaml` |
| `signal_urate_high` | Legacy WHY asset; unchanged and excluded | `backend/core/knowledge/root_cause_registry_v1.py:91`; loader at `backend/core/knowledge/load_root_cause_hypotheses.py:179-180` |

`backend/core/knowledge/why_authority_v1.py:22-42` does not include creatinine, urea, eGFR, or urate in the migrated cohort. Its out-of-cohort rule at lines 152-153 preserves legacy WHY. The compiled register contains no renal target row. Therefore the current causal-WHY state is unambiguous: creatinine and urea remain legacy; eGFR has no WHY authority; no renal compiled frame is active.

### Signal and collision authority is a separate layer

This is not a contradiction to the WHY findings:

- `knowledge_bus/governance/authority_runtime_execution_register_v1.yaml:9-26` records the runtime-enforced `renal_filtration_axis`.
- `signal_egfr_low` is primary and `signal_creatinine_high` is supporting.
- The two eGFR signal packages are active at lines 36-48.
- `knowledge_bus/governance/signal_authority_collision_model_v1.yaml:41-53` suppresses duplicate creatinine filtration framing when eGFR is present while preserving the distinct acute electrolyte layer.

These records govern signal presentation/collision, not causal-WHY emission. ARCH-CONV-B must not modify that distinction without later ratified authority.

## Canonical identity closure

Identity is taken from embedded fields, never filenames or package names.

| Role | signal_id | Embedded source_spec_id | Canonical path | SHA-256 |
|---|---|---|---|---|
| In scope | `signal_creatinine_high` | `inv_creatinine_high_renal` | `knowledge_bus/research/investigation_specs/inv_creatinine_high_renal_v1.yaml` | `b53c0d924fde540c08226bf61a4d5b6b24eee9c10e1f8646f5d3a7861482163c` |
| In scope | `signal_urea_high` | `inv_urea_high_renal` | `knowledge_bus/research/investigation_specs/inv_urea_high_renal.yaml` | `3c8d3d2e8c8138021981f4adfb9545c858d10354bf6a6c93a70f85d70a6abf60` |
| Boundary only | `signal_egfr_low` | `inv_egfr_low_chronic_kidney_function_reduction` | `knowledge_bus/research/investigation_specs/inv_egfr_low_chronic_kidney_function_reduction.yaml` | `514607dd894d466b60ea0275787903dda8dd8186bfe44e3d978bfa834a558e10` |
| Boundary only | `signal_egfr_low` | `inv_egfr_low_hemodynamic_filtration_drop` | `knowledge_bus/research/investigation_specs/inv_egfr_low_hemodynamic_filtration_drop.yaml` | `49a28a760ca5c0d33f0b9f8602166065bfd144a3236b278e43ecb32369bb8c37` |
| Exclusion proof | `signal_urate_high` | `inv_uric_acid_high_metabolic` | `knowledge_bus/research/investigation_specs/inv_uric_acid_high_metabolic.yaml` | `a7edef6ee3c28a4da8be1d79a2f5e36b0f80f7af5c7b7e5a140418208fc078cd` |

The creatinine filename has a `_v1` suffix, but its embedded `spec_id` does not (`inv_creatinine_high_renal_v1.yaml:1-2`). The activation key is therefore:

```text
signal_creatinine_high::inv_creatinine_high_renal
```

## Candidate and parallel-source closure

### Creatinine

- Target: `signal_creatinine_high::inv_creatinine_high_renal`.
- Canonical S24 package: `knowledge_bus/packages/pkg_s24_creatinine_high_renal/`.
- Package-only Pass 3 parallel: `pkg_kb52c_creatinine_high_reduced_glomerular_filtration`, activation key `signal_creatinine_high::inv_creatinine_high_reduced_glomerular_filtration`.
- A non-runtime promoted duplicate also exists at `knowledge_bus/generated_pilot/kb_util_2_pilot/promoted_candidates/pkg_creatinine_high_renal_pass3_v1/`.
- The parallel Pass 3 frame has no standalone peer under `knowledge_bus/research/investigation_specs/`.
- This is same-signal/different-source-spec medical overlap, not an identical activation-key duplicate. It must not be resolved lexicographically or by package/load order.

### eGFR boundary

- Both canonical identities exist and both signal packages are runtime active:
  - `pkg_kb47_egfr_low_chronic_kidney_function_reduction`
  - `pkg_kb47_egfr_low_hemodynamic_filtration_drop`
- The chronic frame requires persistence/albuminuria context (`inv_egfr_low_chronic_kidney_function_reduction.yaml:36-77`).
- The hemodynamic frame requires trajectory, medication, illness, and volume context (`inv_egfr_low_hemodynamic_filtration_drop.yaml:36-75`).
- Neither is an ARCH-CONV-B compile target.
- Creatinine may later use ratified eGFR context as supporting/severity evidence only. It may not emit, retire, alias, or displace `signal_egfr_low` WHY.
- This is a cross-signal medical-authority boundary, not a same-activation-key duplicate.

### Urea

- Target: `signal_urea_high::inv_urea_high_renal`.
- Canonical S24 package: `knowledge_bus/packages/pkg_s24_urea_high_renal/`.
- Package-only Pass 3 parallel: `pkg_kb52c_urea_high_prerenal_volume_depletion_or_catabolic_load`, activation key `signal_urea_high::inv_urea_high_prerenal_volume_depletion_or_catabolic_load`.
- The parallel frame has no standalone peer under `knowledge_bus/research/investigation_specs/`.
- S24 supports creatinine concordance and haemoglobin differential (`inv_urea_high_renal.yaml:20-31`) but only structures high-protein and dehydration confounders (`:44-51`).
- Prerenal, intrinsic renal, catabolic, corticosteroid, and bleeding-related concepts must remain separate pending medical disposition.

### Urate exclusion

- Embedded identity: `signal_urate_high::inv_uric_acid_high_metabolic`.
- Canonical domain is metabolic (`inv_uric_acid_high_metabolic.yaml:1-8`).
- Its renal handling is supporting context, while a competing package-only gout/crystal frame exists.
- Including urate would widen the medical decision and rollback boundary.
- No urate medical review, compilation, registration, runtime change, or legacy disconnection is authorised by ARCH-CONV-B.

## Evidence and structured-field gaps

| Gap | Classification | Effect |
|---|---|---|
| Creatinine S24 frame vs reduced-GFR Pass 3 frame | `MEDICAL_DISPOSITION_REQUIRED` | Gate 1 must decide causal/context/deferred/rejected roles |
| Creatinine lacks structured UACR and history/serial inputs | `CANONICAL_RESEARCH_INCOMPLETE_OR_AMBIGUOUS` | CKD/AKI claims must fail closed |
| Creatinine muscle mass, creatine, and dehydration confounders | `CONTEXT_PRESENT_NOT_CAUSAL` | Must not become standalone diagnoses |
| Urea S24 source is thin relative to Pass 3 | `EVIDENCE_GAP` | May require narrowing or deferral |
| Corticosteroid/catabolic context not structured in S24 urea spec | `EVIDENCE_GAP` | Must not be silently added |
| Urea/urate absent from `medical_frame_identity_index_v1.yaml` | `GOVERNANCE_INDEX_GAP` | Record for review; do not widen Phase 0 into index repair |
| Package-only Pass 3 candidates lack standalone inv YAMLs | `PACKAGE_ONLY_SOURCE` | Not equivalent to canonical investigation-spec authority |
| eGFR signal authority vs absent eGFR WHY | `LAYER_DISTINCTION_CONFIRMED` | Preserve both facts; do not infer contradiction |
| Urate metabolic/gout/renal mixture | `OUT_OF_SCOPE_DEFERRED` | Successor metabolic/systemic programme |

## Stage 1C affected surfaces

### Read during Phase 0

- Canonical research: the five investigation specs listed above.
- Package records: S24 and KB47/KB52C renal-related packages.
- Legacy WHY: creatinine, urea, and urate hypothesis assets and loaders.
- WHY authority: `root_cause_registry_v1.py`, `why_authority_v1.py`, `compiled_why_authority_register_v1.yaml`.
- Signal collision: `signal_authority_collision_model_v1.yaml`, `authority_runtime_execution_register_v1.yaml`, `signal_authority_collision_resolver.py`, `signal_evaluator.py`.
- Duplicate authority: `duplicate_authority_resolution_v1.py`.
- Consumers: `root_cause_compiler_v1.py`, `report_compiler_v1.py`, ReportV1/narrative/provenance consumers.
- Tests: collision enforcement, activation identity, duplicate resolution, legacy WHY, kidney card, Package 1/2 provenance and frame identity, Wave 1/2 WHY authority patterns.

### Expected later output changes, only after STOP A and STOP B

- Creatinine and urea may move from legacy WHY to explicitly ratified compiled authority.
- Only ratified causal frames may emit causal WHY.
- Context-only, rejected, and deferred frames must remain non-causal/unreachable.

### Outputs that must remain unchanged

- eGFR signal activation and `renal_filtration_axis` collision behaviour.
- No standalone eGFR WHY under creatinine.
- Urate signal and WHY behaviour.
- Thyroid, lipid/cardiometabolic, homocysteine, and all unrelated domains.
- Report DTO structure and frontend behaviour.

## Phase 0 verification

Focused non-runtime verification:

```text
python -m pytest \
  backend/tests/unit/test_duplicate_authority_resolution_v1.py \
  backend/tests/regression/test_signal_authority_collision_enforcement.py \
  backend/tests/unit/test_why_authority_pkg3.py \
  backend/tests/unit/test_root_cause_v1_homocysteine.py::test_root_cause_v1_renal_kb_s56b_emits_hypotheses_for_creatinine_urea_urate -q

29 passed
```

The broader `test_root_cause_v1_homocysteine.py` module produced 44 passes and one unrelated existing total-cholesterol failure: `signal_total_cholesterol_high` with a blank activation key fails closed under the already-merged Wave 2 authority state. ARCH-CONV-B changed no runtime or test code and does not remediate this out-of-scope lipid issue.

## STOP A checklist

| Requirement | Result |
|---|---|
| Embedded identities confirmed | PASS |
| Canonical and package-only sources distinguished | PASS |
| Legacy causal-WHY authority identified | PASS |
| Compiled renal authority state identified | PASS — none active |
| Signal/collision authority separated from WHY authority | PASS |
| Creatinine/eGFR cross-signal boundary recorded | PASS |
| Urea structured/evidence gaps recorded | PASS |
| Urate implementation exclusion recorded | PASS |
| Medical approval or ratification made by Cursor | **NO** |
| Compilation, runtime activation, registration, or legacy disconnection performed | **NO** |

## Verdict

```text
STOP A APPROVED BY HEAD OF ARCHITECTURE — PHASE 1 (GATE 1 PACK FINALISATION) AUTHORISED
```

Approval authorises finalisation of the Gate 1 medical-review pack for Head of Medical Research only. It does not authorise Cursor to make medical decisions, compile frames, register or modify runtime authority, disconnect legacy authority, run Automation Bus finish, or proceed to Phase 2.
