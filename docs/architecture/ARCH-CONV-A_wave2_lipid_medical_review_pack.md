# ARCH-CONV-A — Wave 2 Lipid Medical-Review Pack (STOP B)

**Work ID:** `ARCH-CONV-A`  
**Wave:** 2 — Lipid / cardiometabolic (specification-ready subset)  
**Date (UTC):** 2026-07-28  
**Pack role:** Gate 1 / Gate 2 **submission and decision record** assembled by Cursor  
**Medical decisions in this pack:** recorded from Gate 1 / Gate 2 — Cursor does not invent further medical content  

Allowed decision values:

```text
APPROVE
APPROVE_WITH_NARROWING
REJECT
DEFER_EVIDENCE_INSUFFICIENT
CONTEXT_ONLY
```

**Gate 1 reference:** `GPT-GATE1-ARCH-CONV-A-W2-LIPID-2026-07-28-v1`  
**Gate 2 reference:** `ANTHONY-GATE2-ARCH-CONV-A-W2-LIPID-2026-07-28-v1`  
**Decision artefact:** `docs/architecture/ARCH-CONV-A_wave2_lipid_gate1_gate2_decision.md`  
**Decision register:** `docs/architecture/ARCH-CONV-A_wave2_medical_decision_register.yaml`

Wave 2 blocked / research-gap targets (not submitted; not compiled):

- `signal_total_cholesterol_high`
- `signal_apoa1_cardio_risk`
- `signal_lipid_transport_dysfunction`

Canonical identities use embedded `spec_id` values (no filename `_v1` activation keys).

---

## Pack summary

| # | signal_id | activation_key | canonical inv | medical decision | GPT ref | Anthony ref |
|---:|---|---|---|---|---|---|
| 1 | signal_ldl_cholesterol_high | signal_ldl_cholesterol_high::inv_ldl_high_dyslipidaemia | inv_ldl_high_dyslipidaemia_v1.yaml | **APPROVE_WITH_NARROWING** | GPT-GATE1-ARCH-CONV-A-W2-LIPID-2026-07-28-v1 | ANTHONY-GATE2-ARCH-CONV-A-W2-LIPID-2026-07-28-v1 |
| 2 | signal_hdl_cholesterol_low | signal_hdl_cholesterol_low::inv_hdl_low_cardiovascular | inv_hdl_low_cardiovascular.yaml | **CONTEXT_ONLY** | GPT-GATE1-ARCH-CONV-A-W2-LIPID-2026-07-28-v1 | ANTHONY-GATE2-ARCH-CONV-A-W2-LIPID-2026-07-28-v1 |
| 3 | signal_triglycerides_high | signal_triglycerides_high::inv_triglycerides_high_metabolic | inv_triglycerides_high_metabolic_v1.yaml | **APPROVE_WITH_NARROWING** | GPT-GATE1-ARCH-CONV-A-W2-LIPID-2026-07-28-v1 | ANTHONY-GATE2-ARCH-CONV-A-W2-LIPID-2026-07-28-v1 |

---

## Frame 1 — signal_ldl_cholesterol_high

### Identity

| Field | Value |
|---|---|
| signal_id | signal_ldl_cholesterol_high |
| activation_key | signal_ldl_cholesterol_high::inv_ldl_high_dyslipidaemia |
| source_spec_id | inv_ldl_high_dyslipidaemia |
| embedded YAML spec_id | inv_ldl_high_dyslipidaemia |
| wave | 2 |

### Canonical source

| Field | Value |
|---|---|
| path | `knowledge_bus/research/investigation_specs/inv_ldl_high_dyslipidaemia_v1.yaml` |
| primary marker | ldl_cholesterol |

### Medical decision register

| Field | Value |
|---|---|
| medical decision | APPROVE_WITH_NARROWING |
| GPT review reference | GPT-GATE1-ARCH-CONV-A-W2-LIPID-2026-07-28-v1 |
| Anthony ratification reference | ANTHONY-GATE2-ARCH-CONV-A-W2-LIPID-2026-07-28-v1 |
| narrowing bounds | See decision artefact — atherogenic lipoprotein-burden / CV-risk frame; no diagnosis; no medication recommendation; supporting markers context-only |

---

## Frame 2 — signal_hdl_cholesterol_low

### Identity

| Field | Value |
|---|---|
| signal_id | signal_hdl_cholesterol_low |
| activation_key | signal_hdl_cholesterol_low::inv_hdl_low_cardiovascular |
| source_spec_id | inv_hdl_low_cardiovascular |
| wave | 2 |

### Canonical source

| Field | Value |
|---|---|
| path | `knowledge_bus/research/investigation_specs/inv_hdl_low_cardiovascular.yaml` |
| primary marker | hdl_cholesterol |

### Medical decision register

| Field | Value |
|---|---|
| medical decision | CONTEXT_ONLY |
| GPT review reference | GPT-GATE1-ARCH-CONV-A-W2-LIPID-2026-07-28-v1 |
| Anthony ratification reference | ANTHONY-GATE2-ARCH-CONV-A-W2-LIPID-2026-07-28-v1 |
| runtime encoding | why_role: morphology_context; causal_why: prohibited |

---

## Frame 3 — signal_triglycerides_high

### Identity

| Field | Value |
|---|---|
| signal_id | signal_triglycerides_high |
| activation_key | signal_triglycerides_high::inv_triglycerides_high_metabolic |
| source_spec_id | inv_triglycerides_high_metabolic |
| embedded YAML spec_id | inv_triglycerides_high_metabolic |
| wave | 2 |

### Canonical source

| Field | Value |
|---|---|
| path | `knowledge_bus/research/investigation_specs/inv_triglycerides_high_metabolic_v1.yaml` |
| primary marker | triglycerides |

### Medical decision register

| Field | Value |
|---|---|
| medical decision | APPROVE_WITH_NARROWING |
| GPT review reference | GPT-GATE1-ARCH-CONV-A-W2-LIPID-2026-07-28-v1 |
| Anthony ratification reference | ANTHONY-GATE2-ARCH-CONV-A-W2-LIPID-2026-07-28-v1 |
| narrowing bounds | See decision artefact — TG / metabolic-risk frame; no assumed single cause; no pancreatitis diagnosis; no treatment plan |

---

## Wave 2 research-gap register (not submitted)

| signal_id | readiness | blocker |
|---|---|---|
| signal_total_cholesterol_high | A5 / D-5 | no accepted inv; identity vs LDL/HDL subsumption unresolved |
| signal_apoa1_cardio_risk | A5 / D-5 | no accepted inv |
| signal_lipid_transport_dysfunction | A4 / D-4 | composite mismatch |

---

## STOP B status

```text
Wave 2 STOP B pack status: RATIFIED — Gate 1 / Gate 2 complete
frames proposed for medical review: 3
frames ratified: 3
frames compiled: see STOP C
```
