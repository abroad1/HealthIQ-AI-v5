# Clinical Sign-Off — KBP-0002 Insulin Resistance Risk Detection

## Review Status

**Status: PENDING REVIEW**

This document must be completed by a named clinical reviewer and committed before this package
may be promoted to Layer B implementation (KB-S9). No code implementing derived metrics or
signal logic from this package may be committed to `backend/core/` without a completed sign-off.

---

## Package Information

| Field | Value |
|-------|-------|
| Package ID | KBP-0002 |
| Package directory | `knowledge_bus/packages/pkg_insulin_resistance/` |
| Signal | `signal_insulin_resistance` |
| Translation mode | Confirmation — research validates existing KBP-0001 signal |
| Primary metric | `derived.tyg_index` |
| Source document | `knowledge_bus/research/study_01_insulin_resistance.md` |
| Translation date | 2026-03-08 |
| Translated by | Claude Translation Engine — Research-to-Knowledge Translation Specification v1 |

---

## Translation Mode: Confirmation

`signal_insulin_resistance` already exists in KBP-0001 with fully specified thresholds,
override rules, and bundle consumers. This package does not create new signal logic.

KBP-0002 documents the scientific evidence that confirms those thresholds are correct:

| Threshold | KBP-0001 value | Research evidence |
|-----------|---------------|-------------------|
| Optimal boundary | < 8.30 | Navarro-González et al. (2016): diabetes risk rose progressively at TyG ≥8.31; AUC 0.75 in normoglycaemic subgroup |
| At-risk boundary | ≥ 8.50 | Irace et al. (2022): optimal TyG cut-off for incident metabolic syndrome ~8.518; AUROC 0.837 vs HOMA-IR 0.680 |
| Prediabetes override HbA1c | ≥ 5.7% | ADA Standards of Care 2026 prediabetes diagnostic threshold |
| Prediabetes override FPG | ≥ 5.6 mmol/L | ADA Standards of Care 2026 prediabetes diagnostic threshold |

**The thresholds in KBP-0001 match the evidence. No modifications are required.**

---

## Evidence Summary

### Primary evidence

**Vascular-Metabolic CUN cohort (Preventive Medicine, 2016; doi:10.1016/j.ypmed.2016.01.022)**
- n = 4,820; mean follow-up 8.84 years; prospective cohort
- Diabetes risk rose progressively at TyG ≥ 8.31
- Normoglycaemic subgroup: AUC 0.75 (0.70–0.81) for TyG vs 0.66 (0.60–0.72) for fasting glucose (p=0.017)
- TyG superior to fasting glucose for early diabetes detection in the normal glucose range
- Provides the optimal/suboptimal boundary at 8.30

**Irace et al. (Nutrition Metabolism and Cardiovascular Diseases, 2022; doi:10.1016/j.numecd.2021.11.017)**
- n = 9,730 baseline; n = 6,091 incident analysis; 12-year follow-up
- TyG AUROC 0.837 vs HOMA-IR 0.680 for prevalent metabolic syndrome
- TyG AUROC 0.654 vs HOMA-IR 0.556 for incident metabolic syndrome
- Optimal TyG cut-off for incident metabolic syndrome ~8.518
- Provides the at-risk boundary at 8.50 (rounds to include ~8.518)

### Supporting evidence

**Meta-analysis (Primary Care Diabetes, 2020; doi:10.1016/j.pcd.2020.09.001)**
- 13 cohort studies; n = 70,380
- Pooled HR 2.44 (95% CI 2.17–2.76) for incident T2DM with higher TyG
- High heterogeneity noted — confirms predictive validity at population scale

**Korean Genome and Epidemiology Study (Translational Research, 2021; doi:10.1016/j.trsl.2020.08.003)**
- n = 4,285 nonobese adults; 12 years; incident diabetes 14.7%
- Highest TyG quartile: adjusted HR 3.67 (95% CI 2.71–4.98) vs lowest; dose–response confirmed

**Cardiovascular risk (European Journal of Clinical Investigation, 2016; doi:10.1111/eci.12583)**
- n = 5,014; median follow-up 10 years
- TyG adds incremental cardiovascular risk information beyond Framingham variables
- AUC increase 0.708 → 0.719 (p=0.014); supports cardiovascular bundle consumers

**ADA Standards of Care 2026 (Diabetes Care; doi:10.2337/dc26-S002)**
- Guideline-anchored prediabetes thresholds: HbA1c ≥5.7%, FPG ≥5.6 mmol/L
- Basis for prediabetes_override logic in signal_insulin_resistance

---

## Implementation Notes for KB-S9

The following must be confirmed before KB-S9 is authored:

1. **`derived.tyg_index` not yet in `ratio_registry.py`**
   Formula: `TyG = ln((triglycerides_mg_dL × glucose_mg_dL) / 2)`
   Unit conversion required: glucose_mg_dL = glucose_mmol × 18; triglycerides_mg_dL = triglycerides_mmol × 88.57
   This derived metric must be added to `ratio_registry.py` in KB-S9.

2. **HOMA-IR formula variant must be confirmed before implementation**
   `insight_graph_builder.py` currently uses divisor 405 (implies glucose in mg/dL).
   Platform stores glucose in mmol/L. If glucose is in mmol/L at computation, correct divisor is 22.5.
   An 18x error in either direction would produce clinically meaningless tier classifications.
   This must be verified and documented before HOMA-IR is committed to `ratio_registry.py`.

3. **Layer C bundle connection requires KB-S10 architectural decision**
   KBP-0001/0002 list four bundle consumers: `metabolic_health`, `cardiovascular_risk`,
   `biological_age`, `brain_metabolic_resilience`. None of these currently match Layer C
   constructs in `insight_graph_builder.py`. Bundle connection is a separate sprint (KB-S10).

---

## Known Limitations

1. **No universal TyG cut-off across ancestries.** Meta-analysis showed high heterogeneity.
   Thresholds are evidence-anchored zones from predominantly European and East Asian cohorts.
   Platform population may require calibration.

2. **TyG is a risk signal, not a diagnostic test.** It is not a replacement for clinical
   diabetes diagnosis (HbA1c, fasting glucose, OGTT). The prediabetes_override ensures
   guideline-defined dysglycaemia is not masked by a favourable TyG.

3. **Triglyceride-elevating conditions can confound TyG.** Hypertriglyceridaemia from alcohol,
   hypothyroidism, nephrotic syndrome, corticosteroids, or antipsychotics can elevate TyG
   independently of insulin resistance, producing false signals.

4. **HOMA-IR assay variability.** Fasting insulin assay lacks universal standardisation.
   HOMA-IR is supported as a directional signal but is classified as optional in this package.

---

## Clinical Reviewer Sign-Off

**Reviewer name:** [PENDING]

**Role / credentials:** [PENDING]

**Review date:** [PENDING]

### Threshold acceptance

| Threshold | Value | Evidence source | Accepted |
|-----------|-------|----------------|---------|
| TyG optimal | < 8.30 | Navarro-González et al. (2016), Preventive Medicine | [ ] |
| TyG suboptimal | 8.30 – 8.49 | Transition zone (CUN cohort + Irace 2022) | [ ] |
| TyG at_risk | ≥ 8.50 | Irace et al. (2022), incident metabolic syndrome cut point | [ ] |
| Prediabetes override HbA1c | ≥ 5.7% | ADA Standards of Care 2026 | [ ] |
| Prediabetes override FPG | ≥ 5.6 mmol/L | ADA Standards of Care 2026 | [ ] |

### Excluded populations

Reviewer confirms these exclusions are appropriate for product use:

- [ ] Pregnancy (gestational physiology differs)
- [ ] Children and adolescents (cut points and natural history differ)
- [ ] Established diabetes on glucose-lowering therapy
- [ ] People on intensive triglyceride-lowering treatment (inputs altered by therapy)
- [ ] Non-fasting samples (inputs distorted)
- [ ] Acute illness (inputs distorted)

### Known limitations acknowledged

- [ ] No universal TyG cut-off across ancestries
- [ ] Triglyceride-elevating conditions can confound TyG independently of insulin resistance
- [ ] TyG is a risk signal, not a diagnostic test
- [ ] HOMA-IR formula variant must be confirmed before KB-S9 implementation

### Additional notes

```
[Reviewer to complete]
```

### Sign-off statement

I confirm that the signal thresholds, override logic, excluded populations, and limitations
documented in KBP-0002 have been reviewed against the cited research evidence and are accepted
for implementation in the HealthIQ platform.

**Signed:** ___________________________

**Date:** ___________________________

---

*This document was generated by Claude Translation Engine under Research-to-Knowledge Translation
Specification v1. The sign-off section requires human completion before this package may proceed
to Layer B implementation.*
