# DHEA-S High Activation Medical Research Review

## Executive Verdict

**Verdict: A. VALID_AS_STANDALONE_CAUTIONARY_SIGNAL**

High **DHEA-S / DHEAS** is medically valid as a cautious, non-diagnostic HealthIQ runtime signal when the result is above the **lab-provided, age/sex-appropriate reference range** and the marker has been correctly canonicalised as **DHEA-S**, not unsulfated DHEA.

However, HealthIQ must keep the claim narrow. A standalone high DHEA-S result may support a cautious statement that DHEA-S is an adrenal androgen marker and that the result may reflect increased adrenal androgen production. It must **not** diagnose PCOS, adrenal disease, adrenal tumour, hyperandrogenism, adrenal dysfunction, or adrenal overactivity.

Downstream androgen markers and symptoms are **not required** to emit a basic DHEA-S-high educational signal. They are required only if HealthIQ wants to escalate the interpretation from “DHEA-S is high” to a broader **androgen-excess context**.

## Final Activation Recommendation

**DHEA_S_HIGH_ACTIVATE_NOW**

Activate DHEA-S high only when:

1. The marker is canonicalised as `dhea_s` / DHEA-S / DHEAS, not unsulfated DHEA.
2. The value is above the lab-provided reference range.
3. Age is present, because DHEA-S is strongly age-dependent.
4. Biological sex is present, because interpretation and reference intervals are sex-dependent.
5. DHEA supplementation, testosterone therapy, anabolic steroid exposure, pregnancy status where applicable, and relevant hormone therapy context have been captured or explicitly marked not answered.

If companion androgen markers or symptoms are missing, HealthIQ may still emit a low-strength DHEA-S-high signal, but must downgrade to biomarker-level wording and state that broader interpretation is limited without testosterone/SHBG/FAI/symptom context.

## Clinical Validity Assessment

DHEA-S is the sulphated form of DHEA and is produced predominantly by the adrenal glands. Lab Tests Online UK states that DHEAS testing measures adrenal production and is used to investigate hormone imbalances, virilisation, hirsutism, adrenal tumours and certain adrenal gland disorders.

The Endocrine Society hirsutism guideline states that evaluation of hyperandrogenaemic women may include measurement of DHEA-S to screen for adrenal hyperandrogenism, alongside other clinical and biochemical assessment.

The 2025 Society for Endocrinology guideline for androgen excess in women states that elevated DHEAS concentrations strongly suggest an adrenal source of androgen excess and are useful in the biochemical work-up of an adrenal mass.

Mayo Clinic Laboratories states that elevated DHEA/DHEAS levels indicate increased adrenal androgen production, while also cautioning that mild-to-moderate adult elevations are usually idiopathic and that more pronounced elevations are the context in which adrenal tumours should be considered.

Therefore, high DHEA-S is clinically meaningful as a cautious educational signal, but only if HealthIQ avoids over-interpreting mild isolated elevations.

## Required Corroboration

| Marker / context | Requirement | Reason |
|---|---|---|
| Total testosterone | STRONGLY_RECOMMENDED | Helps determine whether DHEA-S elevation is part of broader biochemical androgen excess. |
| Free testosterone | STRONGLY_RECOMMENDED | Helps assess downstream free androgen exposure, especially if SHBG is abnormal. |
| Free androgen index / FAI | STRONGLY_RECOMMENDED | Useful female hyperandrogenism support marker where testosterone and SHBG are available. |
| SHBG | STRONGLY_RECOMMENDED | Needed to interpret FAI/free androgen context; low SHBG may amplify androgen exposure. |
| Androstenedione | OPTIONAL | Useful in specialist androgen excess work-up but not required for basic DHEA-S-high signal. |
| 17-hydroxyprogesterone | OPTIONAL | Important if non-classic congenital adrenal hyperplasia is clinically suspected. |
| LH / FSH | OPTIONAL | Useful for ovarian/gonadal-axis context but not required for DHEA-S-high signal. |
| Cortisol | OPTIONAL | Useful if Cushing syndrome/adrenal condition is suspected. |
| ACTH | OPTIONAL | Useful in adrenal-axis assessment, not required for basic DHEA-S-high signal. |
| Age | REQUIRED | DHEA-S declines with age; age is essential for reference-range interpretation. |
| Biological sex | REQUIRED | Reference ranges and interpretation differ by sex. |
| Menstrual / menopausal status where applicable | STRONGLY_RECOMMENDED | Important for female androgen-excess interpretation and escalation. |
| Pregnancy status | REQUIRED where applicable | Pregnancy requires different endocrine interpretation; suppress routine signal if pregnant. |
| Androgen-excess symptoms | STRONGLY_RECOMMENDED | Required to escalate beyond biomarker-level wording. |
| PCOS-relevant symptoms | OPTIONAL | Useful context but not required; PCOS must not be diagnosed. |
| Adrenal-relevant symptoms | OPTIONAL | Useful for escalation if severe/rapid features exist. |
| DHEA supplementation | REQUIRED | Directly invalidates endogenous DHEA-S-high interpretation. |
| Testosterone therapy | REQUIRED | Confounds androgen interpretation and should downgrade/suppress broader androgen claims. |
| Anabolic steroid exposure | REQUIRED | Confounds androgen interpretation and should downgrade/suppress broader androgen claims. |
| HRT / hormone therapy | REQUIRED where applicable | Can alter androgen/SHBG context and symptom interpretation. |

## Required Gates

### Mandatory biomarker gates

- Canonical marker must be `dhea_s` / DHEA-S / DHEAS.
- Marker must not be unsulfated DHEA.
- Unit and reference range must be compatible with DHEA-S reporting.
- Result must be above the lab-provided reference range.
- Lab-provided reference range must be preserved and used for interpretation.

### Mandatory demographic gates

- Age present.
- Biological sex present.
- Pregnancy status captured where biologically applicable.

### Mandatory questionnaire/context gates

- DHEA supplementation captured.
- Testosterone therapy captured.
- Anabolic steroid / AAS exposure captured.
- HRT / hormone therapy captured where applicable.
- Menstrual/menopause status captured where applicable if female androgen-excess wording is considered.

### Mandatory exclusion gates

- Suppress endogenous DHEA-S-high interpretation if DHEA supplementation is disclosed.
- Suppress routine interpretation in pregnancy unless pregnancy-specific endocrine logic exists.
- Suppress diagnosis-like wording in all cases.
- Suppress adrenal tumour/adrenal disease wording unless an explicitly clinician-review escalation pathway is triggered by extreme elevation and/or severe clinical context.

### Optional supporting markers

- Total testosterone.
- Free testosterone.
- SHBG.
- FAI.
- Androstenedione.
- 17-hydroxyprogesterone.
- LH/FSH.
- Cortisol/ACTH.
- Glucose/HbA1c/insulin if metabolic/PCOS context is being considered.

## Exclusion / Suppression Rules

| Condition | Action | Reason |
|---|---|---|
| DHEA supplementation | SUPPRESS | Directly invalidates endogenous DHEA-S-high interpretation. |
| Testosterone therapy | DOWNGRADE | Does not necessarily cause high DHEA-S, but confounds androgen interpretation and symptoms. |
| Anabolic steroid use | DOWNGRADE | Confounds androgen interpretation; suppress broad androgen-excess claims. |
| Pregnancy | SUPPRESS | Pregnancy requires specialist/pregnancy-specific interpretation. |
| Known adrenal condition | DOWNGRADE | Use condition-aware wording; avoid presenting as new inference. |
| Known PCOS | ALLOW_WITH_CAUTION | DHEA-S can be elevated in PCOS, but HealthIQ must not attribute causality or diagnose. |
| Glucocorticoid medication | DOWNGRADE | Glucocorticoids can affect adrenal androgen production; context needed. |
| Severe acute illness | DOWNGRADE | Acute illness can alter endocrine interpretation; avoid strong claims. |
| Missing age | SUPPRESS | DHEA-S is age-dependent. |
| Missing biological sex | SUPPRESS | Reference ranges and interpretation are sex-dependent. |
| Missing symptom context | DOWNGRADE | Emit biomarker-level wording only; do not frame androgen-excess context. |
| Missing testosterone/SHBG/FAI data | ALLOW_WITH_CAUTION | Standalone DHEA-S-high signal is allowed, but do not infer broader hyperandrogenism. |

## Safe Wording

Maximum safe wording strength:

Acceptable:

- “may support”
- “may be consistent with”

Use with caution only in clinician-facing/internal language, not preferred for consumer wording:

- “could indicate”

Prohibited:

- “suggests”
- “strongly suggests”
- “indicates”
- “diagnostic of”

Safest user-facing wording:

> Your DHEA-S result is above the reference range provided by the laboratory. DHEA-S is an adrenal androgen marker, meaning it is mainly produced by the adrenal glands and can act as a precursor to other sex hormones. A higher result may be consistent with increased adrenal androgen production, but this result is not diagnostic on its own. Interpretation depends on age, biological sex, symptoms, hormone therapy, anabolic steroid or DHEA supplement use, pregnancy status where relevant, and other androgen markers such as testosterone, SHBG or free androgen index if available. If the level is markedly raised, if symptoms such as rapid new facial/body hair growth, acne, scalp hair thinning, voice deepening or menstrual change are present, or if this is unexpected, clinical review is appropriate.

## Unsafe Wording

| Phrase | Safety classification | Rule |
|---|---|---|
| Adrenal androgen excess | SAFE ONLY WITH QUALIFICATION | May be used only as “may support an adrenal contribution to androgen-excess context” when symptoms or companion androgen markers support it. Not standalone. |
| Adrenal overactivity | UNSAFE | Too broad, non-specific and disease-like. |
| Adrenal tumour | UNSAFE | Do not state or imply. May only say marked elevations can warrant clinical review to exclude rarer adrenal causes. |
| PCOS | UNSAFE | Do not infer or diagnose PCOS from DHEA-S. May mention only if user has declared known PCOS or in clinician-facing differential context. |
| Hyperandrogenism | SAFE ONLY WITH QUALIFICATION | May be used only as “biochemical hyperandrogenism context” when testosterone/free testosterone/FAI/symptoms support it. |
| Adrenal dysfunction | UNSAFE | Too vague and disease-like. |

HealthIQ must never say:

- “You have adrenal androgen excess.”
- “You have adrenal overactivity.”
- “This means you have PCOS.”
- “This suggests an adrenal tumour.”
- “Your adrenal glands are dysfunctional.”
- “You need DHEA/testosterone/hormone treatment.”
- “This confirms hyperandrogenism.”

## DHEA-S Low Decision

**Decision: C. BIOMARKER_LEVEL_EXPLANATION_ONLY**

Low DHEA-S should remain inactive as a primary runtime interpretation signal. It may be explained at biomarker level as below the lab reference range and as a non-specific finding that can vary with age, adrenal-axis context, pituitary/adrenal disease, glucocorticoid exposure and illness. It should not activate a deterministic “adrenal androgen reduction” or “adrenal insufficiency” signal.

Rationale: Endocrine Society guidance recommends against making clinical androgen-deficiency diagnoses in healthy women and recommends against routine DHEA therapy because evidence is limited. Low DHEA-S can occur in adrenal insufficiency, but adrenal insufficiency requires proper adrenal-axis testing and clinical assessment, not DHEA-S alone.

## Unsulfated DHEA Decision

| Marker | Recommendation | Reason |
|---|---|---|
| Unsulfated DHEA high | DO_NOT_ACTIVATE | Less stable and less commonly used than DHEA-S for adrenal androgen interpretation; not approved as runtime signal. |
| Unsulfated DHEA low | DO_NOT_ACTIVATE | Non-specific and not suitable as a deterministic runtime signal. |

Unsulfated DHEA and DHEA-S must remain separate canonical concepts. A commercial report label such as “DHEA” may only resolve to DHEA-S when unit/reference-range evidence supports DHEA-S identity. Otherwise, the marker must remain unsulfated DHEA or unresolved, not silently mapped.

## Evidence Summary

1. DHEA-S is an adrenal androgen marker. Lab Tests Online UK states that DHEAS testing assesses adrenal production and is used in investigation of virilisation, hirsutism, adrenal tumours and adrenal gland disorders.
2. DHEA-S is used in androgen-excess evaluation. The Endocrine Society hirsutism guideline states that evaluation of hyperandrogenaemic women may include DHEAS measurement to screen for adrenal hyperandrogenism.
3. Elevated DHEAS can support adrenal-source interpretation. The 2025 Society for Endocrinology androgen-excess guideline states that elevated DHEAS concentrations strongly suggest an adrenal source of androgen excess and are useful in adrenal mass work-up.
4. Mild elevations should not be overcalled. Mayo Clinic Laboratories states that mild-to-moderate adult elevations are usually idiopathic, while pronounced elevations may suggest androgen-producing adrenal tumours.
5. DHEA-S should not be used to diagnose wellness states or justify supplementation. Endocrine Society guidance recommends against routine DHEA use in women because indications and long-term safety evidence are inadequate.

## References

1. Lab Tests Online UK. **DHEAS**. https://labtestsonline.org.uk/tests/dheas
2. Martin KA, et al. **Evaluation and Treatment of Hirsutism in Premenopausal Women: An Endocrine Society Clinical Practice Guideline**. JCEM, 2018. https://academic.oup.com/jcem/article/103/4/1233/4924418
3. Elhassan YS, et al. **Society for Endocrinology Clinical Practice Guideline for the Evaluation of Androgen Excess in Women**. Clinical Endocrinology, 2025. https://pmc.ncbi.nlm.nih.gov/articles/PMC12413683/
4. Mayo Clinic Laboratories. **Dehydroepiandrosterone (DHEA), Serum — Interpretation**. https://www.mayocliniclabs.com/test-catalog/overview/81405
5. Wierman ME, et al. **Androgen Therapy in Women: A Reappraisal — An Endocrine Society Clinical Practice Guideline**. JCEM, 2014. https://academic.oup.com/jcem/article/99/10/3489/2836272
6. Sharma A, Welt CK. **Practical Approach to Hyperandrogenism in Women**. Med Clin North Am, 2021. https://pmc.ncbi.nlm.nih.gov/articles/PMC8548673/
7. Carmina E, et al. **Increased Prevalence of Elevated DHEAS in PCOS Women with Non-Classic Phenotypes**. 2022. https://pmc.ncbi.nlm.nih.gov/articles/PMC9601254/

## Final Machine-Readable Decision

```yaml
dhea_s_high:
  activation_recommendation: DHEA_S_HIGH_ACTIVATE_NOW
  standalone_signal_allowed: true
  corroboration_required: false
  required_biomarkers:
    - dhea_s_above_lab_reference_range
  strongly_recommended_biomarkers:
    - total_testosterone
    - free_testosterone
    - shbg
    - free_androgen_index
  optional_biomarkers:
    - androstenedione
    - seventeen_hydroxyprogesterone
    - lh
    - fsh
    - cortisol
    - acth
    - glucose
    - hba1c
    - insulin
  required_context:
    - age
    - biological_sex
    - dhea_supplementation_status
    - testosterone_therapy_status
    - anabolic_steroid_exposure_status
    - pregnancy_status_where_applicable
    - hrt_or_hormone_therapy_status_where_applicable
  exclusion_gates:
    - suppress_if_dhea_supplementation_disclosed
    - suppress_if_pregnancy_disclosed_without_pregnancy_specific_logic
    - suppress_if_age_missing
    - suppress_if_biological_sex_missing
    - downgrade_if_testosterone_therapy_disclosed
    - downgrade_if_anabolic_steroid_exposure_disclosed
    - downgrade_if_known_adrenal_condition_disclosed
    - downgrade_if_glucocorticoid_medication_disclosed
    - downgrade_if_severe_acute_illness_disclosed
    - downgrade_if_symptom_context_missing
    - allow_with_caution_if_testosterone_shbg_fai_missing
  maximum_claim_strength:
    - may_support
    - may_be_consistent_with
  prohibited_claims:
    - suggests
    - strongly_suggests
    - indicates
    - diagnostic_of
    - adrenal_overactivity
    - adrenal_tumour
    - pcOS_diagnosis
    - adrenal_dysfunction
    - confirmed_hyperandrogenism
  safe_wording: >
    Your DHEA-S result is above the reference range provided by the laboratory.
    DHEA-S is an adrenal androgen marker, meaning it is mainly produced by the
    adrenal glands and can act as a precursor to other sex hormones. A higher
    result may be consistent with increased adrenal androgen production, but this
    result is not diagnostic on its own. Interpretation depends on age, biological
    sex, symptoms, hormone therapy, anabolic steroid or DHEA supplement use,
    pregnancy status where relevant, and other androgen markers such as
    testosterone, SHBG or free androgen index if available. If the level is
    markedly raised, if symptoms such as rapid new facial/body hair growth, acne,
    scalp hair thinning, voice deepening or menstrual change are present, or if
    this is unexpected, clinical review is appropriate.
  clinician_review_triggers:
    - markedly_raised_dhea_s
    - rapid_onset_virilisation_symptoms
    - postmenopausal_new_androgen_excess_symptoms
    - severe_or_progressive_hyperandrogenic_symptoms
    - known_adrenal_condition_with_unexpected_elevation
    - abnormal_dhea_s_with_concerning_cortisol_or_acth_context

dhea_s_low:
  recommendation: BIOMARKER_LEVEL_EXPLANATION_ONLY
  reason: >
    Low DHEA-S is non-specific and age/context dependent. It may be relevant in
    adrenal-axis assessment but should not activate a primary HealthIQ runtime
    signal without cortisol/ACTH and clinical evaluation.

unsulfated_dhea:
  high_recommendation: DO_NOT_ACTIVATE
  low_recommendation: DO_NOT_ACTIVATE
  reason: >
    Unsulfated DHEA is separate from DHEA-S and is not approved as a deterministic
    runtime signal. Do not silently map unsulfated DHEA to DHEA-S unless unit and
    reference-range evidence support DHEA-S canonicalisation.
```
