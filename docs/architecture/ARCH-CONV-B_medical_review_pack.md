# ARCH-CONV-B — Renal Medical-Review Pack

**Work ID:** `ARCH-CONV-B`  
**Date (UTC):** 2026-07-30  
**Pack state:** `PHASE_0_DRAFT_AWAITING_STOP_A_APPROVAL`  
**Medical decisions:** **NONE**  
**Gate 1 reference:** PENDING  
**Gate 2 reference:** PENDING

This record refreshes the preserved ARCH-CONV-A Wave 3 material into ARCH-CONV-B scope. It is not yet a Gate 1 submission: independent STOP A approval is required first. It authorises no compile, runtime activation, authority registration, or legacy disconnection.

Allowed reviewer decisions after STOP A approval:

```text
APPROVE
APPROVE_WITH_NARROWING
REJECT
DEFER_EVIDENCE_INSUFFICIENT
CONTEXT_ONLY
```

## Scope

| Item | Role |
|---|---|
| `signal_creatinine_high::inv_creatinine_high_renal` | In-scope candidate |
| `signal_urea_high::inv_urea_high_renal` | In-scope candidate |
| `signal_egfr_low` chronic and hemodynamic frames | Boundary evidence only; no B compile |
| `signal_urate_high` canonical and gout/crystal frames | Explicitly excluded |

## Identity verification

| signal_id | Source filename | Embedded source_spec_id | Proposed activation_key | Source hash prefix |
|---|---|---|---|---|
| `signal_creatinine_high` | `inv_creatinine_high_renal_v1.yaml` | `inv_creatinine_high_renal` | `signal_creatinine_high::inv_creatinine_high_renal` | `b53c0d924fde540c` |
| `signal_urea_high` | `inv_urea_high_renal.yaml` | `inv_urea_high_renal` | `signal_urea_high::inv_urea_high_renal` | `3c8d3d2e8c813802` |

The creatinine filename suffix is not activation-key material. Identity comes from `spec_id` at `inv_creatinine_high_renal_v1.yaml:1`.

## Authority baseline

| Target | Current causal-WHY | Compiled WHY | Parallel medical framing |
|---|---|---|---|
| Creatinine | Legacy `creatinine_high_hypotheses_v1.yaml` | None | Pass 3 reduced-glomerular-filtration package |
| Urea | Legacy `urea_high_hypotheses_v1.yaml` | None | Pass 3 prerenal-volume-depletion/catabolic package |
| eGFR | None | None | Two active signal packages; distinct collision authority |
| Urate | Legacy, unchanged | None | Metabolic vs gout/crystal mixture; excluded |

## Candidate 1 — Creatinine high

### Source identity

| Field | Value |
|---|---|
| signal_id | `signal_creatinine_high` |
| source_spec_id | `inv_creatinine_high_renal` |
| activation_key | `signal_creatinine_high::inv_creatinine_high_renal` |
| canonical source | `knowledge_bus/research/investigation_specs/inv_creatinine_high_renal_v1.yaml` |
| legacy WHY | `knowledge_bus/root_cause/hypotheses/creatinine_high_hypotheses_v1.yaml` |
| S24 package | `pkg_s24_creatinine_high_renal` |
| Pass 3 parallel | `signal_creatinine_high::inv_creatinine_high_reduced_glomerular_filtration` |

### Canonical evidence summary

- Research domain: renal.
- eGFR is a severity marker; urea is a corroborator; potassium is a severity marker (`inv_creatinine_high_renal_v1.yaml:20-35`).
- Existing overrides use eGFR below 60 and high potassium (`:36-59`).
- Recorded confounders are high muscle mass, creatine supplementation, and dehydration (`:60-72`).
- The source notes that serum creatinine reflects production and renal excretion and requires eGFR interpretation (`:80-89`).

This summary is source transcription, not medical approval.

### Questions for Gate 1 after STOP A

1. Is the canonical creatinine frame medically acceptable as causal WHY?
2. Does it require narrowing to filtration-marker/renal-clearance context?
3. Is the Pass 3 reduced-GFR frame rejected, context-only, deferred, or a separate causal frame?
4. How may eGFR support, strengthen, contradict, or suppress creatinine interpretation?
5. Which claims belong exclusively to future standalone `signal_egfr_low` WHY?
6. What fail-closed wording is required when chronicity, serial results, UACR, cystatin C, or clinical history are absent?
7. Is legacy WHY replacement equivalent enough to permit later disconnection?

### Boundary constraints

- Isolated creatinine elevation must not diagnose CKD or AKI.
- Creatinine must not emit or claim standalone `signal_egfr_low` WHY.
- Existing eGFR signal primacy and renal collision policy must remain unchanged.
- eGFR concordance may be used only as specifically ratified.
- eGFR absence or non-low result must not be silently treated as renal disease confirmation.
- No medication start/stop, treatment plan, or frontend-authored medical inference.

### Evidence gaps

| Gap | Review consequence |
|---|---|
| No structured UACR in the canonical creatinine spec | Do not infer albuminuria or CKD-risk grade |
| No serial/history input | Acute/chronic claims require fail-closed caveat or deferral |
| Muscle mass/creatine/dehydration confounding | Must remain context, not causal diagnosis |
| Pass 3 reduced-GFR overlap | Explicit medical-role disposition required |
| Medication and exercise context not fully structured | Do not invent governed claims |

### Decision fields

| Field | Value |
|---|---|
| medical decision | `PENDING` |
| causal/context/rejected/deferred role | `PENDING` |
| legacy authority disposition | `PENDING` |
| Head of Medical Research reference | null |
| Anthony ratification reference | null |

## eGFR cross-signal boundary

### Existing canonical frames

| activation_key | Distinguishing authority |
|---|---|
| `signal_egfr_low::inv_egfr_low_chronic_kidney_function_reduction` | Persistence, UACR, and cystatin C; a single low value is insufficient (`inv_egfr_low_chronic_kidney_function_reduction.yaml:36-77`) |
| `signal_egfr_low::inv_egfr_low_hemodynamic_filtration_drop` | Trajectory, volume, medication, illness, creatinine, and cystatin C (`inv_egfr_low_hemodynamic_filtration_drop.yaml:36-75`) |

Both eGFR signal packages are runtime active under `knowledge_bus/governance/authority_runtime_execution_register_v1.yaml:36-48`. Neither has causal-WHY authority in `root_cause_registry_v1.py` or the compiled WHY register.

### Required reviewer safeguards

- Keep eGFR as a distinct signal family and future WHY migration boundary.
- Do not treat a creatinine activation key as a duplicate of either eGFR activation key.
- Do not use creatinine as surrogate authority for chronic or hemodynamic eGFR frames.
- Do not alter the existing `renal_filtration_axis` signal collision decision.
- Specify any permissible eGFR supporting/severity use inside creatinine WHY.

## Candidate 2 — Urea high

### Source identity

| Field | Value |
|---|---|
| signal_id | `signal_urea_high` |
| source_spec_id | `inv_urea_high_renal` |
| activation_key | `signal_urea_high::inv_urea_high_renal` |
| canonical source | `knowledge_bus/research/investigation_specs/inv_urea_high_renal.yaml` |
| legacy WHY | `knowledge_bus/root_cause/hypotheses/urea_high_hypotheses_v1.yaml` |
| S24 package | `pkg_s24_urea_high_renal` |
| Pass 3 parallel | `signal_urea_high::inv_urea_high_prerenal_volume_depletion_or_catabolic_load` |

### Canonical evidence summary

- Research domain: renal, while interpretation also depends on protein metabolism and hydration.
- Creatinine high is a corroborator; low haemoglobin is a differential marker for possible GI blood/protein load (`inv_urea_high_renal.yaml:20-31`).
- The existing override escalates on concurrent high creatinine (`:32-43`).
- Structured confounders are high-protein diet and dehydration (`:44-51`).
- The source describes urea as both a renal-function and metabolic/hydration marker (`:59-66`).

This summary is source transcription, not medical approval.

### Questions for Gate 1 after STOP A

1. Is `inv_urea_high_renal` adequate for one causal frame?
2. Are renal/excretory and prerenal volume-depletion/catabolic framings one frame or separate frames?
3. Should the Pass 3 frame be causal, context-only, rejected, or deferred?
4. Is the source evidence sufficient, or must the frame be narrowed/deferred?
5. How should dehydration, protein load, catabolic illness, corticosteroids, GI bleeding, creatinine concordance, and absent eGFR data be handled?
6. Is legacy replacement equivalent enough to permit later disconnection?

### Boundary constraints

- Isolated urea elevation must not diagnose renal impairment.
- Do not silently merge renal, prerenal, catabolic, steroid, or bleeding-related concepts.
- Creatinine concordance may strengthen context but does not establish diagnosis.
- Low haemoglobin may be a differential marker only; it does not diagnose GI bleeding.
- No treatment plan or medication change from urea alone.

### Evidence gaps

| Gap | Review consequence |
|---|---|
| S24 source is thin relative to Pass 3 framing | Narrowing or deferral may be required |
| Catabolic and corticosteroid contexts not structured in S24 | Do not add without accepted authority |
| Pass 3 source is package-only | Do not infer canonical investigation authority |
| Urea frames absent from medical frame identity index | Governance gap; not repaired under Phase 0 |

### Decision fields

| Field | Value |
|---|---|
| medical decision | `PENDING` |
| causal/context/rejected/deferred role | `PENDING` |
| legacy authority disposition | `PENDING` |
| Head of Medical Research reference | null |
| Anthony ratification reference | null |

## Urate exclusion

Confirmed identity:

```text
signal_urate_high::inv_uric_acid_high_metabolic
```

Reasons for exclusion:

- The canonical source domain is metabolic (`inv_uric_acid_high_metabolic.yaml:1-8`).
- Renal handling is only one supporting mechanism (`:20-25`).
- A competing package-only gout/crystal-deposition frame exists.
- Inclusion would widen medical review and rollback beyond creatinine/urea.

No urate decision field is presented. No urate medical review, compile, activation, authority registration, or legacy change is permitted.

## Gate-readiness checklist

| Requirement | Current state |
|---|---|
| Identity and source evidence assembled | COMPLETE |
| Creatinine/eGFR boundary documented | COMPLETE |
| Urea evidence gaps documented | COMPLETE |
| Urate excluded | COMPLETE |
| Independent STOP A approval | **PENDING** |
| Head of Medical Research Gate 1 | **NOT STARTED** |
| Anthony Gate 2 ratification | **NOT STARTED** |
| Compiled frames | 0 |
| Runtime changes | 0 |

```text
PACK DRAFT COMPLETE — STOP AT STOP A
```

After explicit independent STOP A approval, this pack may be finalised for Gate 1 without Cursor making the medical decisions.
