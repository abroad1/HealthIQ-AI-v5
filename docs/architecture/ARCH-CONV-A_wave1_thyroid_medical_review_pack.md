# ARCH-CONV-A — Wave 1 Thyroid Medical-Review Pack (STOP B)

**Work ID:** `ARCH-CONV-A`  
**Wave:** 1 — Thyroid axis (specification-ready subset)  
**Date (UTC):** 2026-07-27  
**Pack role:** Gate 1 / Gate 2 **submission evidence** assembled by Cursor  
**Medical decisions in this pack:** **NONE** — all decision fields left for GPT + Anthony  

Allowed decision values (for reviewers only):

```text
APPROVE
APPROVE_WITH_NARROWING
REJECT
DEFER_EVIDENCE_INSUFFICIENT
CONTEXT_ONLY
```

Pilot thyroid frames already compiled (out of scope for this pack):  
`signal_free_t3_low::inv_free_t3_low_low_t3_syndrome`,  
`signal_tpo_ab_high::*` (2 frames).

Wave 1 blocked (not submitted): `signal_thyroid_tsh_context`, `signal_tgab_high` — research gaps.

---

## Pack summary

| # | signal_id | activation_key (proposed) | canonical inv | legacy YAML | medical decision | GPT ref | Anthony ref |
|---:|---|---|---|---|---|---|---|
| 1 | signal_tsh_high | signal_tsh_high::inv_tsh_high_hypothyroidism | inv_tsh_high_hypothyroidism_v1.yaml | tsh_high_hypotheses_v1.yaml | **PENDING** | | |
| 2 | signal_tsh_low | signal_tsh_low::inv_tsh_low_hyperthyroidism | inv_tsh_low_hyperthyroidism_v1.yaml | tsh_low_hypotheses_v1.yaml | **PENDING** | | |
| 3 | signal_free_t3_high | signal_free_t3_high::inv_free_t3_high_t3_predominant_thyrotoxicosis | inv_free_t3_high_t3_predominant_thyrotoxicosis.yaml | free_t3_high_hypotheses_v1.yaml | **PENDING** | | |
| 4 | signal_free_t4_high | signal_free_t4_high::inv_free_t4_high_thyrotoxicosis_context | inv_free_t4_high_thyrotoxicosis_context.yaml | free_t4_high_hypotheses_v1.yaml | **PENDING** | | |
| 5 | signal_free_t4_low | signal_free_t4_low::inv_free_t4_low_thyroid_hormone_deficiency | inv_free_t4_low_thyroid_hormone_deficiency.yaml | free_t4_low_hypotheses_v1.yaml | **PENDING** | | |

---

## Frame 1 — signal_tsh_high

### Identity

| Field | Value |
|---|---|
| signal family | thyroid / TSH |
| direction | high |
| signal_id | signal_tsh_high |
| activation_key | signal_tsh_high::inv_tsh_high_hypothyroidism |
| frame identity / source_spec_id | inv_tsh_high_hypothyroidism |
| wave | 1 |

### Canonical source

| Field | Value |
|---|---|
| path | `knowledge_bus/research/investigation_specs/inv_tsh_high_hypothyroidism_v1.yaml` |
| spec_id | inv_tsh_high_hypothyroidism |
| primary marker | tsh |
| evidence strength (spec) | strong |
| cited sources (spec) | NICE NG145 (2019); ETA subclinical hypothyroidism guideline (2013) |

### Proposed interpretation (from canonical narrative — not a medical approval)

Elevated TSH as pituitary response to reduced thyroid hormone feedback; free T4 distinguishes subclinical vs overt pattern. Spec narrative mechanism: HPT axis TRH→TSH→T4/T3.

### Legacy comparison

| Field | Value |
|---|---|
| legacy path | `knowledge_bus/root_cause/hypotheses/tsh_high_hypotheses_v1.yaml` |
| legacy hypotheses | `tsh_high_axis_elevation_v1` (Elevated TSH pattern); `tsh_high_ft4_discordance_v1` (TSH elevation with free T4 context) |
| note | Legacy wording is **not** current medical authority; listed for differential only |

### Evidence boundaries / contradictions / confirmatory markers (from inv)

| Field | Value |
|---|---|
| supporting markers | free_t4 low (severity); free_t3 low (optional); ldl high; creatine_kinase high |
| override escalate | free_t4 below_min → at_risk; TSH > 10 → at_risk |
| confounders | non-thyroidal illness recovery; biotin; diurnal TSH |
| contradictions / exclusions | for reviewer — not pre-decided |

### Context vs causal

| Field | Value |
|---|---|
| proposed status | Causal WHY candidate (direction-specific high) — **pending Gate 1** |
| consumer / clinician / intervention implications | for reviewer |
| unsafe overstatement risks | diagnosing hypothyroidism; treatment advice |

### Medical decision register (blank)

| Field | Value |
|---|---|
| medical decision | PENDING |
| GPT review reference | |
| Anthony ratification reference | |
| narrowing bounds (if any) | |

---

## Frame 2 — signal_tsh_low

### Identity

| Field | Value |
|---|---|
| signal_id | signal_tsh_low |
| activation_key | signal_tsh_low::inv_tsh_low_hyperthyroidism |
| source_spec_id | inv_tsh_low_hyperthyroidism |
| direction | low |

### Canonical source

| Field | Value |
|---|---|
| path | `knowledge_bus/research/investigation_specs/inv_tsh_low_hyperthyroidism_v1.yaml` |
| primary marker | tsh |
| narrative mechanism (spec) | Excess T4/T3 suppresses TRH/TSH |

### Legacy comparison

| Field | Value |
|---|---|
| legacy path | `knowledge_bus/root_cause/hypotheses/tsh_low_hypotheses_v1.yaml` |
| legacy hypotheses | `tsh_low_axis_suppression_v1`; `tsh_low_ft4_coupling_v1` |

### Evidence boundaries

| Field | Value |
|---|---|
| supporting / severity markers | free_t4 / free_t3 (per spec) |
| confounders | biotin; non-thyroidal illness; exogenous hormone — for reviewer from spec |
| context vs causal | Causal WHY candidate — pending Gate 1 |

### Medical decision register (blank)

| Field | Value |
|---|---|
| medical decision | PENDING |
| GPT review reference | |
| Anthony ratification reference | |

---

## Frame 3 — signal_free_t3_high

### Identity

| Field | Value |
|---|---|
| signal_id | signal_free_t3_high |
| activation_key | signal_free_t3_high::inv_free_t3_high_t3_predominant_thyrotoxicosis |
| source_spec_id | inv_free_t3_high_t3_predominant_thyrotoxicosis |
| direction | high |

### Canonical source

| Field | Value |
|---|---|
| path | `knowledge_bus/research/investigation_specs/inv_free_t3_high_t3_predominant_thyrotoxicosis.yaml` |
| primary marker | free_t3 |
| proposed framing (spec title) | T3-predominant thyrotoxicosis pattern |

### Legacy comparison

| Field | Value |
|---|---|
| legacy path | `knowledge_bus/root_cause/hypotheses/free_t3_high_hypotheses_v1.yaml` |
| legacy hypotheses | `ft3_high_thyroid_hormone_excess_pattern_v1`; `ft3_high_tsh_suppression_context_v1` |

### Cross-axis note (non-decision)

Already-compiled `signal_free_t3_low` must not be contradicted narratively; reviewer should ensure high/low frames remain mutually exclusive.

### Medical decision register (blank)

| Field | Value |
|---|---|
| medical decision | PENDING |
| GPT review reference | |
| Anthony ratification reference | |

---

## Frame 4 — signal_free_t4_high

### Identity

| Field | Value |
|---|---|
| signal_id | signal_free_t4_high |
| activation_key | signal_free_t4_high::inv_free_t4_high_thyrotoxicosis_context |
| source_spec_id | inv_free_t4_high_thyrotoxicosis_context |
| direction | high |

### Canonical source

| Field | Value |
|---|---|
| path | `knowledge_bus/research/investigation_specs/inv_free_t4_high_thyrotoxicosis_context.yaml` |
| primary marker | free_t4 |

### Legacy comparison

| Field | Value |
|---|---|
| legacy path | `knowledge_bus/root_cause/hypotheses/free_t4_high_hypotheses_v1.yaml` |
| legacy hypotheses | `ft4_high_thyroxine_excess_pattern_v1`; `ft4_high_tsh_suppression_context_v1` |

### Medical decision register (blank)

| Field | Value |
|---|---|
| medical decision | PENDING |
| GPT review reference | |
| Anthony ratification reference | |

---

## Frame 5 — signal_free_t4_low

### Identity

| Field | Value |
|---|---|
| signal_id | signal_free_t4_low |
| activation_key | signal_free_t4_low::inv_free_t4_low_thyroid_hormone_deficiency |
| source_spec_id | inv_free_t4_low_thyroid_hormone_deficiency |
| direction | low |

### Canonical source

| Field | Value |
|---|---|
| path | `knowledge_bus/research/investigation_specs/inv_free_t4_low_thyroid_hormone_deficiency.yaml` |
| primary marker | free_t4 |

### Legacy comparison

| Field | Value |
|---|---|
| legacy path | `knowledge_bus/root_cause/hypotheses/free_t4_low_hypotheses_v1.yaml` |
| legacy hypotheses | `ft4_low_hormone_deficiency_pattern_v1`; `ft4_low_tsh_elevation_context_v1` |

### Medical decision register (blank)

| Field | Value |
|---|---|
| medical decision | PENDING |
| GPT review reference | |
| Anthony ratification reference | |

---

## Wave 1 research gaps (explicit)

| signal_id | gap | effect on this STOP B |
|---|---|---|
| signal_thyroid_tsh_context | No confirmed context-framed inv | Not submitted |
| signal_tgab_high | No inv_*.yaml | Not submitted |

---

## Reviewer request

Please complete Gate 1 (GPT structured medical review) and Gate 2 (Anthony ratification) for frames 1–5 using the decision vocabulary above.  
Do **not** treat legacy YAML wording as approved evidence.  
Do **not** authorise compile/runtime activation in this STOP B response unless explicitly stated for later Phase 3 continuation.
