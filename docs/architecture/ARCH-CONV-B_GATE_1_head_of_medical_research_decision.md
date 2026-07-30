# ARCH-CONV-B — Gate 1 Head of Medical Research Decision

**Reference:** `ARCH-CONV-B-GATE1-HMR-2026-07-30`  
**Work ID:** `ARCH-CONV-B`  
**Gate:** Gate 1 — Head of Medical Research  
**Status:** COMPLETE — AWAITING ANTHONY GATE 2 RATIFICATION  
**Runtime authority:** NOT AUTHORISED

## Decision summary

| Candidate | Decision | Approved role |
|---|---|---|
| `signal_creatinine_high::inv_creatinine_high_renal` | `APPROVE_WITH_NARROWING` | Narrow causal-candidate frame describing possible reduced renal clearance / filtration-marker abnormality |
| `signal_urea_high::inv_urea_high_renal` | `APPROVE_WITH_NARROWING` | `CONTEXT_ONLY_NON_CAUSAL` |
| Pass 3 creatinine reduced-GFR package-only candidate | `DEFER_EVIDENCE_INSUFFICIENT` | No compile or authority |
| Pass 3 urea prerenal/catabolic package-only candidate | `DEFER_EVIDENCE_INSUFFICIENT` | No compile or authority |
| `signal_egfr_low` boundary | Confirmed separate | No ARCH-CONV-B compile |
| `signal_urate_high` | Excluded | No decision or change |

## 1. Creatinine

### Decision

`APPROVE_WITH_NARROWING`

The frame may represent **possible reduced renal clearance or a filtration-marker abnormality**. It must not represent isolated creatinine elevation as a diagnosis of chronic kidney disease, acute kidney injury, or a standalone eGFR abnormality.

### Required role

`CAUSAL_CANDIDATE_NARROWED_RENAL_CLEARANCE_CONTEXT`

This permits a bounded candidate explanation for the creatinine signal, while preserving uncertainty and alternative non-renal influences.

### Mandatory safeguards

- Low eGFR may strengthen severity or supporting context only.
- Creatinine must not emit, alias, retire or displace `signal_egfr_low` WHY authority.
- CKD wording requires chronicity and appropriate kidney-damage evidence.
- AKI wording requires dynamic creatinine change and clinical context.
- Missing eGFR, serial results, UACR, cystatin C or clinical history must fail closed.
- Normal or non-low eGFR must not be treated as confirmation of renal impairment.
- Muscle mass, creatine supplementation, exercise and dehydration remain explicit alternative/contextual explanations.
- The package-only reduced-glomerular-filtration candidate is deferred until a canonical investigation specification exists.

### Legacy disposition

`CONDITIONAL_REPLACE_AFTER_GATE2_AND_STOP_C`

Legacy creatinine WHY may be disconnected only after Anthony ratification, deterministic compilation, runtime reachability, safe output comparison and independent STOP C proof.

## 2. eGFR boundary

`CONFIRMED_PRESERVE_DISTINCT_EGFR_AUTHORITY`

The chronic kidney-function-reduction and hemodynamic-filtration-drop eGFR frames remain separate future WHY authorities.

ARCH-CONV-B must not:

- compile either eGFR frame;
- treat creatinine and eGFR activation keys as duplicates;
- use creatinine as surrogate authority for chronic or hemodynamic eGFR states;
- alter the existing renal-filtration signal collision decision.

## 3. Urea

### Decision

`APPROVE_WITH_NARROWING`

### Required role

`CONTEXT_ONLY_NON_CAUSAL`

The current evidence does not support standalone causal renal-impairment authority from isolated urea elevation. The permitted output is a non-specific contextual frame covering possible renal-clearance, hydration and protein/catabolic influences.

### Mandatory safeguards

- Do not emit a standalone causal renal diagnosis or renal-failure explanation from urea alone.
- Creatinine or eGFR concordance may strengthen renal context but does not establish diagnosis.
- Dehydration, high protein intake, catabolic illness, corticosteroid exposure and gastrointestinal bleeding remain differential/context items only.
- Low haemoglobin must not be described as evidence that gastrointestinal bleeding is present.
- Renal, prerenal, catabolic, steroid and bleeding concepts must not be silently merged into one causal claim.
- The package-only prerenal/catabolic frame is deferred until canonical investigation-spec authority exists.
- If runtime cannot preserve context-only, non-causal behaviour, this frame must not be compiled or promoted.

### Legacy disposition

`CONDITIONAL_REPLACE_WITH_CONTEXT_ONLY_AFTER_GATE2_AND_STOP_C`

Legacy urea causal authority may be disconnected only if the approved context-only replacement is correctly enforced and independently proven. No new causal urea WHY authority is approved.

## 4. Urate

Exclusion is confirmed. No medical decision, compilation, activation, authority registration or legacy change is authorised under ARCH-CONV-B.

## Gate 2 requirement

These decisions do not authorise implementation. Anthony must explicitly ratify:

1. the narrowed creatinine causal-candidate role;
2. preservation of separate eGFR authority;
3. urea as context-only and non-causal;
4. deferral of both package-only Pass 3 candidates;
5. conditional legacy replacement rules.

Only after Gate 2 ratification may Cursor proceed to Phase 2.
