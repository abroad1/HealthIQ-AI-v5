# MR-BATCH-001B — Candidate Prose Test Output

**Status:** CANDIDATE / TEST-ONLY — not medically approved

> **SUPERSESSION / CONTINUITY NOTE (ARCH-GOV-BASELINE-1, 2026-07-25)**  
> This output is a **Round 1 benchmark / test fixture only**.  
> - **Not** medically approved  
> - **Not** for promotion  
> - **Not** for production runtime  
> - **Must not** proceed to medical review as a promotion route  
> - Useful only as evidence for future Round 2 prose pipeline design  
> Candidate assets themselves are unchanged.

**Source pack:** `docs/sprints/beta_readiness/MR-BATCH-001B_candidate_prose_assets.yaml`
**Isolation:** Loaded only via `candidate_test_mode=True` test loader

## Test cases run

### Cystatin C in-range

- **Selected asset IDs:** cystatin_c_base_explainer_v1_b, cystatin_c_in_range_context_v1

```text
[base] Cystatin C
Kidney filtration is something the body does quietly, continuously, and at a rate that standard creatinine measurements can sometimes misrepresent — especially if someone has unusually low or high muscle mass. Cystatin C fills that gap. It is a small protein produced at a stable rate by cells throughout the body, then filtered by the kidneys. Because its production rate does not depend on muscle, it gives a filtration estimate (eGFR) that is less biased by body composition than creatinine alone. When used alongside creatinine-based eGFR, it can either reinforce confidence in the filtration picture or signal that the two estimates need reconciling. Cystatin C is most useful when creatinine-based eGFR returns an unexpected or borderline value — it provides a second line of evidence. Thyroid status, corticosteroid use and smoking can also influence cystatin C levels, so context matters here too.

[in_range] A cystatin C result within the laboratory's reference range supports the picture that kidney filtration is not flagging a concern at this time. When combined with an in-range creatinine and eGFR, it reinforces confidence in the renal filtration assessment — two independent estimates pointing in the same direction carry more weight than either alone. Cystatin C is less influenced by muscle mass than creatinine, so an in-range reading is particularly reassuring where body composition might otherwise make creatinine harder to interpret. The single-timepoint nature of this result means it cannot confirm long-term stability; prior readings are the only basis for assessing trend.

[Interpretive limitations]
- Cystatin C is still influenced by thyroid status, steroid use and smoking — it is not entirely muscle-mass independent.
- An in-range cystatin C on a single occasion does not establish a stable filtration trend; previous results are needed to assess direction.
```

### Cystatin C high

- **Selected asset IDs:** cystatin_c_base_explainer_v1_b, cystatin_c_high_context_v1

```text
[base] Cystatin C
Kidney filtration is something the body does quietly, continuously, and at a rate that standard creatinine measurements can sometimes misrepresent — especially if someone has unusually low or high muscle mass. Cystatin C fills that gap. It is a small protein produced at a stable rate by cells throughout the body, then filtered by the kidneys. Because its production rate does not depend on muscle, it gives a filtration estimate (eGFR) that is less biased by body composition than creatinine alone. When used alongside creatinine-based eGFR, it can either reinforce confidence in the filtration picture or signal that the two estimates need reconciling. Cystatin C is most useful when creatinine-based eGFR returns an unexpected or borderline value — it provides a second line of evidence. Thyroid status, corticosteroid use and smoking can also influence cystatin C levels, so context matters here too.

[high] A cystatin C above the laboratory's reference range suggests the kidneys may be filtering at a reduced rate. Because cystatin C is less influenced by muscle mass than creatinine, a raised reading carries particular weight when creatinine appears borderline or within range — the two estimates disagreeing is itself a signal worth taking seriously. The combination of a raised cystatin C and a reduced creatinine-based eGFR gives stronger grounds for follow-up than either marker alone. Corticosteroid use and thyroid overactivity can raise cystatin C independently of kidney filtration, so these factors are relevant context when interpreting a raised result.

[Interpretive limitations]
- Cystatin C is still influenced by thyroid status, steroid use and smoking — it is not entirely muscle-mass independent.
- A raised cystatin C without a concurrent or recent creatinine-based eGFR makes it harder to characterise the degree of filtration change.
```

### Cystatin C low

- **Selected asset IDs:** cystatin_c_base_explainer_v1_b, cystatin_c_low_context_v1

```text
[base] Cystatin C
Kidney filtration is something the body does quietly, continuously, and at a rate that standard creatinine measurements can sometimes misrepresent — especially if someone has unusually low or high muscle mass. Cystatin C fills that gap. It is a small protein produced at a stable rate by cells throughout the body, then filtered by the kidneys. Because its production rate does not depend on muscle, it gives a filtration estimate (eGFR) that is less biased by body composition than creatinine alone. When used alongside creatinine-based eGFR, it can either reinforce confidence in the filtration picture or signal that the two estimates need reconciling. Cystatin C is most useful when creatinine-based eGFR returns an unexpected or borderline value — it provides a second line of evidence. Thyroid status, corticosteroid use and smoking can also influence cystatin C levels, so context matters here too.

[low] A cystatin C result below the laboratory's reference range is not a clinically significant finding. Low cystatin C does not indicate that filtration is unusually strong, nor does it carry a specific protective interpretation. It is generally unremarkable and does not change the renal assessment derived from creatinine and eGFR. The focus in this context remains on the in-range and above-range findings in the broader kidney panel.

[Interpretive limitations]
- Cystatin C is still influenced by thyroid status, steroid use and smoking — it is not entirely muscle-mass independent.
- A low cystatin C does not confer additional protective significance beyond what an in-range creatinine and eGFR already indicate.
```

### UACR in-range

- **Selected asset IDs:** uacr_base_explainer_v1_b, uacr_in_range_context_v1

```text
[base] Urine albumin-to-creatinine ratio (UACR)
The kidneys act as a precision filter — keeping proteins in the blood while clearing waste into urine. UACR measures how much albumin appears in urine relative to creatinine. Even small amounts can indicate the filtration membrane is under strain. Because albumin should largely stay in the blood, persistently raised urine albumin is a sensitive early signal of kidney stress — especially with hypertension or diabetes. The ratio corrects for urine concentration, making results more comparable across hydration states. Single-sample UACR is sensitive to exertion, illness, infection, and time of day — repeat confirmation is standard before acting on a finding.

[in_range] A UACR within the laboratory's reference range indicates that albumin is not appearing in the urine at raised concentrations on this sample. This is the expected finding in someone whose kidney filtering membrane is functioning without obvious strain. Where the overall renal panel — eGFR, creatinine — is also within range, an in-range UACR adds to a broadly reassuring filtration picture. The main limitation is that UACR on a single sample can be transiently low due to timing, hydration, or low physical exertion before sampling; transient illness or infection, conversely, can mask what might otherwise be an elevated result. In higher-risk contexts (diabetes, high blood pressure), periodic repeat testing matters even when a result is in range.

[Interpretive limitations]
- A single UACR sample is sensitive to timing, exertion, hydration, and urinary infection; repeat testing under standardised conditions is needed to confirm any finding.
- An in-range UACR is reassuring when confirmed on repeat testing; a single in-range result in someone with high blood pressure or diabetes is less conclusive.
```

### UACR high

- **Selected asset IDs:** uacr_base_explainer_v1_b, uacr_high_context_v1

```text
[base] Urine albumin-to-creatinine ratio (UACR)
The kidneys act as a precision filter — keeping proteins in the blood while clearing waste into urine. UACR measures how much albumin appears in urine relative to creatinine. Even small amounts can indicate the filtration membrane is under strain. Because albumin should largely stay in the blood, persistently raised urine albumin is a sensitive early signal of kidney stress — especially with hypertension or diabetes. The ratio corrects for urine concentration, making results more comparable across hydration states. Single-sample UACR is sensitive to exertion, illness, infection, and time of day — repeat confirmation is standard before acting on a finding.

[high] A UACR above the laboratory's reference range indicates that albumin is passing into the urine at a rate higher than expected. The kidney filtering membrane is allowing through a protein it would normally retain. Common contributing factors include sustained high blood pressure, elevated blood glucose, and kidney filtering membrane stress — but transient causes such as intense physical exertion, urinary infection, or illness in the days before sampling can also produce a temporarily raised result. The finding is most clinically meaningful as part of a pattern across at least two samples taken under standardised conditions. Where the eGFR is also reduced, the renal picture is more complete; where eGFR is within range, a raised UACR may represent an earlier signal.

[Interpretive limitations]
- A single UACR sample is sensitive to timing, exertion, hydration, and urinary infection; repeat testing under standardised conditions is needed to confirm any finding.
- A single raised UACR should not be interpreted as confirming kidney damage without repeat testing; transient causes are common.
```

### WBC high

- **Selected asset IDs:** white_blood_cells_base_explainer_v1_b, wbc_high_context_v1

```text
[base] White blood cells (WBC)
White blood cells are the body's immune patrol — a diverse army of cells, each with a specific role in fighting infection, managing inflammation, and maintaining immune surveillance. They are produced in the bone marrow and continuously circulate in the blood at levels that reflect the current immune state. A full blood count measures the total WBC and, in a differential, the five main subtypes: neutrophils (rapid responders to bacterial infection and tissue damage), lymphocytes (involved in viral defence and immune memory), monocytes, eosinophils (relevant in allergy and parasitic responses), and basophils. Total WBC alone tells you the overall level of immune activity; the differential tells you why. An elevated total count may reflect infection, inflammation, physiological stress, certain medications, or haematological causes. A low total count can reflect viral suppression, specific medications, or bone marrow effects. The two directions have entirely different interpretive pathways.

[high] A total white blood cell count above the laboratory's reference range indicates that the immune system is more active than baseline. The most common short-term causes are infection, inflammation, physiological or psychological stress, and certain medications — including corticosteroids, which are a well-recognised cause of a raised neutrophil count. The critical question is which subtype is driving the elevation: raised neutrophils point in a different direction from raised lymphocytes or eosinophils. Without the differential breakdown, the total count tells you there is an immune signal but not what it means. A raised CRP alongside a raised WBC strengthens the picture of an active inflammatory or infective state.

[Interpretive limitations]
- Total WBC count alone is rarely conclusive; the subtype differential is needed to interpret the clinical direction of any abnormality.
- A raised total WBC without a differential subtype count cannot determine whether the elevation reflects infection, inflammation, medication effect, or haematological cause.
```

### WBC low

- **Selected asset IDs:** white_blood_cells_base_explainer_v1_b, wbc_low_context_v1

```text
[base] White blood cells (WBC)
White blood cells are the body's immune patrol — a diverse army of cells, each with a specific role in fighting infection, managing inflammation, and maintaining immune surveillance. They are produced in the bone marrow and continuously circulate in the blood at levels that reflect the current immune state. A full blood count measures the total WBC and, in a differential, the five main subtypes: neutrophils (rapid responders to bacterial infection and tissue damage), lymphocytes (involved in viral defence and immune memory), monocytes, eosinophils (relevant in allergy and parasitic responses), and basophils. Total WBC alone tells you the overall level of immune activity; the differential tells you why. An elevated total count may reflect infection, inflammation, physiological stress, certain medications, or haematological causes. A low total count can reflect viral suppression, specific medications, or bone marrow effects. The two directions have entirely different interpretive pathways.

[low] A total white blood cell count below the laboratory's reference range indicates that circulating immune cells are reduced. The clinical significance depends almost entirely on which subtype is low and the degree of reduction. A low neutrophil count carries different implications from a low lymphocyte count. Common causes include certain viral infections (which can temporarily suppress WBC), specific medications such as immunosuppressants or antithyroid drugs, and effects on bone marrow function. Medication history is particularly important context here. Where the count is only mildly below range and other full blood count markers are in range, the finding is less specific; a more marked or combined reduction across cell lines warrants closer attention.

[Interpretive limitations]
- Total WBC count alone is rarely conclusive; the subtype differential is needed to interpret the clinical direction of any abnormality.
- A low total WBC without a differential subtype count limits interpretation to confirming suppression is present — not its cause or subtype pattern.
```

### Creatine kinase high + exercise/statin modifiers

- **Selected asset IDs:** creatine_kinase_base_explainer_v1_b, creatine_kinase_high_context_v1, lifestyle_exercise_creatinine_ck_fragment_v1_b, medication_statin_lipid_context_fragment_v1_b

```text
[base] Creatine kinase (CK)
Muscle cells run a constant energy-recycling process, and creatine kinase (CK) is the enzyme at the centre of it. When muscle fibres are put under stress — from hard exercise, an injury, or certain medications — CK leaks into the bloodstream, where it can be measured. A temporary spike after vigorous or unaccustomed exercise is normal and typically resolves within a day or two. CK is also monitored on statins, where muscle effects are recognised but relatively uncommon. CK is found in skeletal and cardiac muscle; isoform pattern matters clinically, though routine panels measure total CK. Interpretation depends on degree of elevation, timing relative to activity, medications — particularly statins — and whether muscle symptoms are present. Without this context, a single CK reading has limited standalone meaning.

[high] A raised CK indicates that muscle fibres are releasing this enzyme into the bloodstream at a higher than usual rate. The most common and benign cause is vigorous or unaccustomed exercise — particularly resistance training — in the 24 to 72 hours before the sample was taken. This kind of rise is transient and expected. A persistently raised CK, or a markedly elevated result without an obvious exercise explanation, warrants more attention — particularly in someone taking a statin, where muscle effects are a recognised consideration. The significance of a raised CK depends on the degree of elevation, the timing relative to activity, current medications, and whether any muscle pain, weakness, or dark urine is present.

[modifier] Recent vigorous exercise — particularly heavy resistance or unaccustomed loading — can temporarily raise creatinine and creatine kinase. This is a well-recognised physiological effect and typically resolves within one to two days. It may transiently reduce the apparent precision of eGFR calculations.

[modifier] Statins are designed to lower LDL and related atherogenic lipid markers — lipid results should be interpreted knowing a statin is being taken and for how long. Muscle-related CK elevation is an uncommon but recognised effect; hepatic enzyme changes are possible but not universally expected at standard doses.

[Interpretive limitations]
- CK interpretation requires knowledge of recent exercise, medication context (especially statins), and degree of elevation — a number without context is hard to interpret.
- Degree of elevation and exercise timing are critical context — a mildly raised post-exercise CK and a markedly raised resting CK are different findings requiring different interpretation.
- Post-exercise CK and creatinine rises are transient. Without knowing the timing and intensity of recent activity, the degree of influence on any result cannot be precisely estimated.
- The degree of expected LDL reduction varies by statin type and dose; interpreting lipid results requires knowing which statin is taken and for how long.
```

### Calcium high

- **Selected asset IDs:** calcium_base_explainer_v1_b, calcium_high_context_v1

```text
[base] Calcium
Calcium does far more than build bones — it triggers every heartbeat, drives muscle contraction, enables nerve signalling, and plays a role in blood clotting. It is one of the body's most tightly regulated minerals, maintained within a narrow range by parathyroid hormone (PTH) and vitamin D working in concert. Standard blood tests measure total calcium, which includes a fraction bound to albumin and a smaller biologically active ionised fraction. Because albumin affects the total reading, many laboratories report a corrected calcium figure that adjusts for albumin concentration — this is often more meaningful than total calcium alone. Calcium is most interpretable alongside albumin, vitamin D, PTH, and renal function. Without these, a total calcium reading can be misleading.

[high] A raised calcium result indicates that more calcium is circulating than the laboratory's reference range expects. The regulatory system that keeps calcium in balance — primarily parathyroid hormone (PTH) and vitamin D — may be producing more calcium release from bone or intestinal absorption than is being cleared. Common reasons for raised calcium include parathyroid-related changes, excess vitamin D intake, certain medications including some diuretics, or less commonly other causes. The albumin level matters here: where albumin is also raised, a corrected calcium figure helps determine whether the elevation is real. Identifying the mechanism requires PTH and vitamin D to be available alongside the calcium result.

[Interpretive limitations]
- Total calcium must be considered alongside albumin concentration; a corrected calcium figure is needed before drawing conclusions from a total calcium reading.
- The cause of raised calcium cannot be established without PTH and vitamin D; total calcium alone does not reveal the mechanism.
```

### Calcium low

- **Selected asset IDs:** calcium_base_explainer_v1_b, calcium_low_context_v1

```text
[base] Calcium
Calcium does far more than build bones — it triggers every heartbeat, drives muscle contraction, enables nerve signalling, and plays a role in blood clotting. It is one of the body's most tightly regulated minerals, maintained within a narrow range by parathyroid hormone (PTH) and vitamin D working in concert. Standard blood tests measure total calcium, which includes a fraction bound to albumin and a smaller biologically active ionised fraction. Because albumin affects the total reading, many laboratories report a corrected calcium figure that adjusts for albumin concentration — this is often more meaningful than total calcium alone. Calcium is most interpretable alongside albumin, vitamin D, PTH, and renal function. Without these, a total calcium reading can be misleading.

[low] A low calcium result needs to be interpreted carefully before drawing conclusions. Total calcium in the blood includes a fraction bound to albumin, so if albumin is also low, the total calcium figure can appear reduced even when the biologically active (ionised) fraction is actually normal. A corrected calcium calculation accounts for this — it is an important first step in interpreting any low calcium reading. Where corrected calcium is genuinely low, possible contributors include low vitamin D, changes in parathyroid function, magnesium status, or kidney function, among others. PTH and vitamin D results are needed to characterise the mechanism further.

[Interpretive limitations]
- Total calcium must be considered alongside albumin concentration; a corrected calcium figure is needed before drawing conclusions from a total calcium reading.
- Low total calcium must always be interpreted alongside albumin — a corrected calcium is required to determine whether the reduction is real.
```

### Cortisol high (sampling-time limits in asset)

- **Selected asset IDs:** cortisol_base_explainer_v1_b, cortisol_high_context_v1

```text
[base] Cortisol
Cortisol is the body's primary stress hormone — it mobilises energy, dials down inflammation, and modulates blood pressure in response to physical or psychological demand. It is produced by the adrenal glands under instruction from the pituitary and hypothalamus, a signalling chain known as the HPA axis. Cortisol follows a strong diurnal rhythm: levels are typically at their peak shortly after waking and fall steeply across the day, reaching their lowest late at night. This rhythm makes timing critical — a reading that looks elevated at 9 am may be entirely expected, while the same number at midnight would not be. Cortisol is also influenced by glucocorticoid medications, some hormonal contraceptives, and acute stress at the time of sampling. A single cortisol reading without sampling time relative to waking loses most interpretive value — the HPA axis dynamic, not the snapshot, is what matters.

[high] A cortisol above the laboratory's reference range may have several explanations that depend almost entirely on when the sample was taken. In the early morning — when cortisol naturally peaks — a high reading may still be at the upper end of physiological variation. Later in the day, the same reading would be more notable. Acute stress at the time of the blood draw, poor sleep, illness, or intense physical activity can all transiently push cortisol above range. Glucocorticoid medications, including some topical or inhaled preparations, can also affect the measurement. A single above-range reading requires sampling time and clinical context before any interpretation is possible. Without a documented sampling time, a high cortisol cannot be meaningfully classified.

[Interpretive limitations]
- A single cortisol value cannot characterise HPA axis function; dynamic testing or paired sampling is required for clinical assessment.
- A high cortisol reading requires documented sampling time and clinical context; it cannot be interpreted as abnormal without both.
```

### Cortisol low

- **Selected asset IDs:** cortisol_base_explainer_v1_b, cortisol_low_context_v1

```text
[base] Cortisol
Cortisol is the body's primary stress hormone — it mobilises energy, dials down inflammation, and modulates blood pressure in response to physical or psychological demand. It is produced by the adrenal glands under instruction from the pituitary and hypothalamus, a signalling chain known as the HPA axis. Cortisol follows a strong diurnal rhythm: levels are typically at their peak shortly after waking and fall steeply across the day, reaching their lowest late at night. This rhythm makes timing critical — a reading that looks elevated at 9 am may be entirely expected, while the same number at midnight would not be. Cortisol is also influenced by glucocorticoid medications, some hormonal contraceptives, and acute stress at the time of sampling. A single cortisol reading without sampling time relative to waking loses most interpretive value — the HPA axis dynamic, not the snapshot, is what matters.

[low] A cortisol below the laboratory's reference range carries very different weight depending on when the sample was taken. Late in the evening, low cortisol is physiologically expected — the diurnal rhythm falls to its lowest at this time. The same reading at 8–9 am, when cortisol is normally at its highest, is more clinically significant and warrants careful review. The morning is when this test has its greatest discriminatory value: a low cortisol at that time indicates that the adrenal glands are not producing the expected morning surge. Chronic use of glucocorticoid medications (including some long-term inhalers or topical steroids) can suppress adrenal output and produce a genuinely low cortisol. Establishing the sampling time is essential before drawing any conclusion from a below-range result.

[Interpretive limitations]
- A single cortisol value cannot characterise HPA axis function; dynamic testing or paired sampling is required for clinical assessment.
- A low cortisol requires the sampling time to interpret; without it, the result cannot be classified as physiological or concerning.
```

### SHBG high

- **Selected asset IDs:** shbg_base_explainer_v1_b, shbg_high_context_v1

```text
[base] SHBG (sex hormone-binding globulin)
SHBG acts as the transport and availability regulator for sex hormones. The liver produces this protein, and it binds testosterone and oestradiol tightly — determining how much hormone is biologically active rather than just circulating. Only the fraction not bound to SHBG (or loosely bound to albumin) is immediately available to cells. This means SHBG level directly shapes how much usable hormone the body has access to, even when total hormone levels appear typical. SHBG is influenced by thyroid function, insulin levels, body weight, and certain medications including hormonal contraceptives and thyroid hormone replacement. High SHBG reduces the proportion of hormone available to tissues; low SHBG has the opposite effect. SHBG must be interpreted alongside total testosterone and free testosterone — a SHBG result without these markers gives an incomplete picture of hormone bioavailability.

[high] Raised SHBG means a higher proportion of circulating testosterone or oestradiol is bound to this transport protein and therefore less available to tissues. High SHBG is associated with hyperthyroidism, certain hormonal contraceptives, thyroid hormone replacement therapy, older age, and lower body weight. The practical effect is that a person with raised SHBG may have total testosterone that appears within range, while free testosterone — the biologically active fraction — is reduced. Whether this matters depends on the degree of SHBG elevation and what the free testosterone and total testosterone show. High SHBG is a context modifier for those other measurements, not an independent finding.

[Interpretive limitations]
- SHBG without paired total and free testosterone cannot be used to assess androgen bioavailability.
- The clinical significance of high SHBG cannot be assessed without free and total testosterone; SHBG alone does not indicate any specific condition.
```

### Free testosterone in-range

- **Selected asset IDs:** free_testosterone_base_explainer_v1_b, free_testosterone_in_range_context_v1

```text
[base] Free testosterone
Only a small fraction of testosterone in the bloodstream is immediately available to cells — this is free testosterone, unbound to transport proteins. Because total testosterone includes protein-bound fractions that may not be biologically active, free testosterone often gives a more complete picture of androgen availability, particularly where SHBG is abnormal. Most testosterone circulates either tightly bound to SHBG or loosely bound to albumin; the free fraction is typically less than three per cent of the total. Free testosterone values are commonly calculated from total testosterone, SHBG, and albumin rather than measured directly, because direct assay methods vary considerably between laboratories. Testosterone levels also follow a diurnal pattern — typically higher in the morning — so the timing of sampling matters. Free testosterone measurement methods vary considerably; calculated estimates depend on accurate SHBG and albumin values, and without these the calculation may be unreliable.

[in_range] Free testosterone within the laboratory's reference range suggests that the immediately available androgen fraction is not reduced below expected limits for this individual at the time of testing. This is most informative alongside total testosterone and SHBG — together, the three markers give a clearer picture of androgen status than any single value. An in-range free testosterone is reassuring in its own context, but the interpretation carries more weight when the calculation method is known, the sample was taken in the morning when testosterone is typically at its daily peak, and SHBG values are reliable.

[Interpretive limitations]
- Free testosterone is most interpretable alongside total testosterone and SHBG; the three values together give a better picture than any single one.
- Free testosterone reference ranges and assay methods vary; the lab-specific method should be confirmed before drawing conclusions.
```

### Missing HbA1c metabolic caveat

- **Selected asset IDs:** missing_hba1c_metabolic_context_v1_b

```text
[missing-marker] HbA1c reflects glucose exposure over roughly 8–12 weeks — far less swayed by day-to-day variation than a single fasting glucose. Without it, glycaemic context is a snapshot, not a trend.
Fasting glucose can shift with recent illness, stress, or fasting timing; HbA1c is largely unaffected by those short-term factors. Absence of HbA1c limits how confidently single glucose readings reflect longer-term pattern.
HealthIQ cannot separate transient glucose fluctuation from underlying glycaemic pattern when HbA1c is absent from the panel.

[Interpretive limitations]
- Without HbA1c, glycaemic context is limited to a single time-point — transient factors such as illness, stress, or fasting variability can affect glucose but would leave HbA1c unchanged.
```

### Missing cystatin C renal caveat

- **Selected asset IDs:** missing_cystatin_c_renal_context_v1_b

```text
[missing-marker] Cystatin C is filtered at a steady rate, independent of muscle mass — useful when creatinine-based eGFR may mislead in very lean or muscular people, or with creatine use. Without it, filtration rests on creatinine alone.
If creatinine-based eGFR is borderline or muscle mass is atypical, absent cystatin C removes an independent cross-check.
Creatinine-based eGFR is usually sufficient; cystatin C mainly adds value where the creatinine picture is uncertain.

[Interpretive limitations]
- Where creatinine-based eGFR returns an unexpected or borderline result in someone with low or high muscle mass, the absence of cystatin C means no alternative filtration estimate is available.
```

### Positive resilience qualifier (renal stable panel) with cystatin C in-range

- **Selected asset IDs:** cystatin_c_base_explainer_v1_b, cystatin_c_in_range_context_v1, resilience_renal_stable_panel_qualifier_v1_b

```text
[base] Cystatin C
Kidney filtration is something the body does quietly, continuously, and at a rate that standard creatinine measurements can sometimes misrepresent — especially if someone has unusually low or high muscle mass. Cystatin C fills that gap. It is a small protein produced at a stable rate by cells throughout the body, then filtered by the kidneys. Because its production rate does not depend on muscle, it gives a filtration estimate (eGFR) that is less biased by body composition than creatinine alone. When used alongside creatinine-based eGFR, it can either reinforce confidence in the filtration picture or signal that the two estimates need reconciling. Cystatin C is most useful when creatinine-based eGFR returns an unexpected or borderline value — it provides a second line of evidence. Thyroid status, corticosteroid use and smoking can also influence cystatin C levels, so context matters here too.

[in_range] A cystatin C result within the laboratory's reference range supports the picture that kidney filtration is not flagging a concern at this time. When combined with an in-range creatinine and eGFR, it reinforces confidence in the renal filtration assessment — two independent estimates pointing in the same direction carry more weight than either alone. Cystatin C is less influenced by muscle mass than creatinine, so an in-range reading is particularly reassuring where body composition might otherwise make creatinine harder to interpret. The single-timepoint nature of this result means it cannot confirm long-term stability; prior readings are the only basis for assessing trend.

[resilience] Where kidney filtration markers — including eGFR and creatinine — sit within the laboratory's reference range with no pattern suggesting a declining trend, this part of the panel does not indicate current renal strain in this context.

[Interpretive limitations]
- Cystatin C is still influenced by thyroid status, steroid use and smoking — it is not entirely muscle-mass independent.
- An in-range cystatin C on a single occasion does not establish a stable filtration trend; previous results are needed to assess direction.
- Stability at this reading does not rule out slowly progressive changes detectable only across serial measurements.
```

## Assets not reachable in this test pass

- None — all representative cases produced output.

## Loader / architecture limitations

- Candidate pack remains in `docs/sprints/beta_readiness/`; production retail/pathway registries unchanged.
- Test loader lives under `backend/tests/support/` and is not wired into orchestrator or `attach_retail_explainers_v1`.
- Hybrid composition is test-side only; narrative compiler does not yet select MR candidate assets.
- WBC scope uses `white_blood_cells` biomarker id; directional assets use `wbc_*` asset ids.
- Glucose marker-state assets are not in MR-BATCH-001B; missing HbA1c caveat is composed standalone.

## Candidate/test-only confirmation

- All assets remain `review_status: CANDIDATE`.
- No production runtime consumption without explicit `candidate_test_mode=True`.
- Gemini narrative path remains inactive by default policy gates.

## Recommended next engineering step

> **SUPERSEDED (ARCH-GOV-BASELINE-1):** Do **not** run medical review of MR-BATCH-001B as a promotion route.  
> Historical recommendation text is intentionally not regenerated.

**Current disposition:** Round 1 benchmark / test fixture only — not medically approved; not for promotion; not for production runtime; useful only as evidence for future Round 2 prose pipeline design.

