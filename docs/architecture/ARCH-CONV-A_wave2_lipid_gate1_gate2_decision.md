# ARCH-CONV-A — Wave 2 Lipid Gate 1 / Gate 2 Decision

**Work ID:** `ARCH-CONV-A`  
**Wave:** 2 — Lipid / cardiometabolic  
**Date (UTC):** 2026-07-28  
**Gate 1 reference:** `GPT-GATE1-ARCH-CONV-A-W2-LIPID-2026-07-28-v1`  
**Gate 2 reference:** `ANTHONY-GATE2-ARCH-CONV-A-W2-LIPID-2026-07-28-v1`

This artefact records the ratified medical boundaries for the three approved Wave 2
lipid frames. It is durable decision authority for Package A implementation.

Medical research authority remains the existing governed investigation specifications
and their Pass 3 lineage. This decision encodes runtime and output boundaries only;
it does not introduce external medical claims, mechanisms, thresholds, or interventions.

## Decision Summary

Approved frames and dispositions:

```text
signal_ldl_cholesterol_high::inv_ldl_high_dyslipidaemia
→ APPROVE_WITH_NARROWING

signal_hdl_cholesterol_low::inv_hdl_low_cardiovascular
→ CONTEXT_ONLY

signal_triglycerides_high::inv_triglycerides_high_metabolic
→ APPROVE_WITH_NARROWING
```

Canonical medical-frame identities use embedded investigation-spec `spec_id` values.
Do not create `_v1` activation keys from filenames.

Canonical identities:

```text
signal_ldl_cholesterol_high::inv_ldl_high_dyslipidaemia
signal_hdl_cholesterol_low::inv_hdl_low_cardiovascular
signal_triglycerides_high::inv_triglycerides_high_metabolic
```

Source files remain:

```text
knowledge_bus/research/investigation_specs/inv_ldl_high_dyslipidaemia_v1.yaml
knowledge_bus/research/investigation_specs/inv_hdl_low_cardiovascular.yaml
knowledge_bus/research/investigation_specs/inv_triglycerides_high_metabolic_v1.yaml
```

## Global Ratified Rules

These rules apply across the full Wave 2 lipid set:

- One coherent lipid interpretation per panel.
- Cross-frame hierarchy:
  - LDL high → principal atherogenic cholesterol-burden lane
  - triglycerides high → triglyceride-rich-lipoprotein / metabolic-risk lane
  - HDL low → context only
- When multiple lipid abnormalities coexist, do not emit three repetitive causal WHY narratives.
- Integrate LDL, triglyceride, and HDL evidence into one coherent lipid interpretation.
- Do not create or activate `signal_total_cholesterol_high`.
- Do not create or activate `signal_lipid_transport_dysfunction`.
- Do not create or activate `signal_apoa1_cardio_risk`.
- Do not invent a new composite medical frame.
- Do not duplicate familial-hypercholesterolaemia warnings.
- Do not substitute these frames for QRISK3 or another governed cardiovascular-risk calculator.
- Consumer and clinician outputs must remain aligned.
- Layer C must not reconstruct lipid medical meaning.

### Consumer restrictions

Permitted language includes: above or below range; adverse lipid pattern; associated with;
contributes to long-term risk; may reflect; worth considering alongside overall cardiovascular risk.

Prohibited language includes: your arteries are blocked; you have heart disease;
you have familial hypercholesterolaemia; you have metabolic syndrome; you are insulin resistant;
you need a statin; start medication; stop medication.

### Clinician restrictions

Clinician output may describe the observed lipid phenotype; distinguish LDL burden from
triglyceride and HDL context; identify marked abnormalities; describe concordance or
discordance with governed supporting biomarkers; list possible secondary contributors
already supported by canonical authority; and recommend clinical correlation or further
assessment.

It must not diagnose an inherited lipid disorder automatically; make an automated
prescribing decision; collapse LDL, HDL, and triglycerides into one unsupported mechanism;
or use total cholesterol as a duplicate causal authority.

## Frame Boundaries

### 1. `signal_ldl_cholesterol_high::inv_ldl_high_dyslipidaemia`

**Disposition:** `APPROVE_WITH_NARROWING`

**Permitted role:** atherogenic lipoprotein-burden / cardiovascular-risk frame

Ratified boundary:

```text
LDL high
  -> preserve high-LDL signal
  -> explain elevated LDL as contributing to long-term atherosclerotic cardiovascular risk
  -> do not diagnose cardiovascular disease, atherosclerosis, or familial hypercholesterolaemia
  -> do not calculate individual absolute cardiovascular risk unless a separately governed risk calculator holds authority
  -> do not recommend starting, stopping, or changing lipid-lowering medication
  -> marked or persistent elevation may trigger cautious assessment language for inherited or secondary causes only where already supported by the canonical specification
  -> supporting markers (non-HDL, ApoB, triglycerides, HDL, Lp(a)) may modify context but must not become unratified causal authorities
```

Implementation boundary:

- Causal WHY is permitted only within the narrowed atherogenic-risk framing above.
- Signal presence is preserved when LDL is high.
- Supporting markers refine context; they do not open independent Wave 2 causal frames.

### 2. `signal_hdl_cholesterol_low::inv_hdl_low_cardiovascular`

**Disposition:** `CONTEXT_ONLY`

Ratified boundary:

```text
HDL low
  -> preserve low-HDL signal
  -> do not compile or emit a standalone causal WHY for low HDL
  -> do not claim that measured HDL concentration proves impaired reverse cholesterol transport or impaired arterial cholesterol clearance
  -> permit low HDL only as an adverse cardiometabolic or cardiovascular risk-marker context
  -> allow it to strengthen an integrated lipid pattern when triglycerides, LDL, glycaemia, or other governed risk markers are present
  -> do not diagnose metabolic syndrome, insulin resistance, or cardiovascular disease
  -> do not recommend treatment specifically to raise HDL
```

Implementation boundary:

```text
why_role: morphology_context   # canonical runtime equivalent of context_only
causal_why: prohibited
```

- HDL may emit a compiled context finding with `why_role: morphology_context`.
- No causal WHY for HDL alone or as a third causal narrative alongside LDL/TG.

### 3. `signal_triglycerides_high::inv_triglycerides_high_metabolic`

**Disposition:** `APPROVE_WITH_NARROWING`

**Permitted role:** elevated triglyceride / triglyceride-rich-lipoprotein and metabolic-risk frame

Ratified boundary:

```text
triglycerides high
  -> preserve high-triglyceride signal
  -> do not assume one specific cause (hepatic VLDL overproduction, alcohol, insulin resistance, genetic disease)
  -> mild or moderate elevation may support cardiometabolic and atherogenic-risk context
  -> fasting status, alcohol, medicines, and secondary conditions may modify interpretation only where data and canonical authority exist
  -> non-fasting or unknown fasting status must not automatically suppress the signal
  -> marked elevation may enter the canonical pancreatitis-risk severity lane only where the existing investigation specification supports the threshold and wording
  -> do not diagnose pancreatitis
  -> do not recommend fibrates, omega-3 therapy, medication changes, or a specific treatment plan
```

Implementation boundary:

- Causal WHY is permitted only within the narrowed triglyceride / metabolic-risk framing above.
- Signal presence is preserved when triglycerides are high, including non-fasting / unknown fasting status.
- Severity escalation language for marked elevation must remain within the canonical specification threshold and must not diagnose pancreatitis.

## Explicit Non-Authorisations

- No compilation or activation of `signal_total_cholesterol_high`.
- No compilation or activation of `signal_apoa1_cardio_risk`.
- No compilation or activation of `signal_lipid_transport_dysfunction`.
- No `_v1` duplicate activation identities derived from filenames.
- No alteration of Wave 1 thyroid medical boundaries.
- No legacy retirement or disconnection under this decision.
- No Wave 3 work under this decision.

## Implementation Note

The ratified narrowing must be encoded using the smallest governed runtime surface that
preserves:

- the approved lipid hierarchy;
- HDL context-only behaviour;
- fail-closed behaviour for blocked Wave 2 targets;
- aligned consumer and clinician wording;
- signal presence separately from causal-WHY eligibility.
