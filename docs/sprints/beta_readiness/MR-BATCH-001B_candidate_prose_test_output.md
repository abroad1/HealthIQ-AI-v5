# MR-BATCH-001B — Candidate Prose Test Output

**Status:** CANDIDATE / TEST-ONLY — not medically approved
**Source pack:** `docs/sprints/beta_readiness/MR-BATCH-001B_candidate_prose_assets.yaml`
**Isolation:** Loaded only via `candidate_test_mode=True` test loader

## Test cases run

### Cystatin C in-range

- **Selected asset IDs:** cystatin_c_base_explainer_v1_b, cystatin_c_in_range_context_v1

```text
[base] Cystatin C
Kidney filtration is something the body does quietly, continuously, and at a rate that standard creatinine measurements can sometimes misrepresent — especially if someone has unusually low or high muscle mass. Cystatin C fills that gap. It is a small protein produced at a stable rate by cells throughout the body, then filtered by the kidneys. Because its production rate does not depend on muscle, it gives a filtration estimate (eGFR) that is less biased by body composition than creatinine alone. When used alongside creatinine-based eGFR, it can either reinforce confidence in the filtration picture or signal that the two estimates need reconciling. Cystatin C is most useful when creatinine-based eGFR returns an unexpected or borderline value — it provides a second line of evidence. Thyroid status, corticosteroid use and smoking can also influence cystatin C levels, so context matters here too.

[in_range] A cystatin C result within the laboratory's reference range supports the picture that kidney filtration is not flagging a concern at this time. When combined with an in-range creatinine and eGFR, it reinforces confidence in the renal filtration assessment — two...
```

### Cystatin C high

- **Selected asset IDs:** cystatin_c_base_explainer_v1_b, cystatin_c_high_context_v1

```text
[base] Cystatin C
Kidney filtration is something the body does quietly, continuously, and at a rate that standard creatinine measurements can sometimes misrepresent — especially if someone has unusually low or high muscle mass. Cystatin C fills that gap. It is a small protein produced at a stable rate by cells throughout the body, then filtered by the kidneys. Because its production rate does not depend on muscle, it gives a filtration estimate (eGFR) that is less biased by body composition than creatinine alone. When used alongside creatinine-based eGFR, it can either reinforce confidence in the filtration picture or signal that the two estimates need reconciling. Cystatin C is most useful when creatinine-based eGFR returns an unexpected or borderline value — it provides a second line of evidence. Thyroid status, corticosteroid use and smoking can also influence cystatin C levels, so context matters here too.

[high] A cystatin C above the laboratory's reference range suggests the kidneys may be filtering at a reduced rate. Because cystatin C is less influenced by muscle mass than creatinine, a raised reading carries particular weight when creatinine appears borderline or withi...
```

### Cystatin C low

- **Selected asset IDs:** cystatin_c_base_explainer_v1_b, cystatin_c_low_context_v1

```text
[base] Cystatin C
Kidney filtration is something the body does quietly, continuously, and at a rate that standard creatinine measurements can sometimes misrepresent — especially if someone has unusually low or high muscle mass. Cystatin C fills that gap. It is a small protein produced at a stable rate by cells throughout the body, then filtered by the kidneys. Because its production rate does not depend on muscle, it gives a filtration estimate (eGFR) that is less biased by body composition than creatinine alone. When used alongside creatinine-based eGFR, it can either reinforce confidence in the filtration picture or signal that the two estimates need reconciling. Cystatin C is most useful when creatinine-based eGFR returns an unexpected or borderline value — it provides a second line of evidence. Thyroid status, corticosteroid use and smoking can also influence cystatin C levels, so context matters here too.

[low] A cystatin C result below the laboratory's reference range is not a clinically significant finding. Low cystatin C does not indicate that filtration is unusually strong, nor does it carry a specific protective interpretation. It is generally unremarkable and does no...
```

### UACR in-range

- **Selected asset IDs:** uacr_base_explainer_v1_b, uacr_in_range_context_v1

```text
[base] Urine albumin-to-creatinine ratio (UACR)
The kidneys act as a precision filter — keeping proteins in the blood while clearing waste into urine. UACR measures how much albumin appears in urine relative to creatinine. Even small amounts can indicate the filtration membrane is under strain. Because albumin should largely stay in the blood, persistently raised urine albumin is a sensitive early signal of kidney stress — especially with hypertension or diabetes. The ratio corrects for urine concentration, making results more comparable across hydration states. Single-sample UACR is sensitive to exertion, illness, infection, and time of day — repeat confirmation is standard before acting on a finding.

[in_range] A UACR within the laboratory's reference range indicates that albumin is not appearing in the urine at raised concentrations on this sample. This is the expected finding in someone whose kidney filtering membrane is functioning without obvious strain. Where the overall renal panel — eGFR, creatinine — is also within range, an in-range UACR adds to a broadly reassuring filtration picture. The main limitation is that UACR on a single sample can be transiently low due to ...
```

### UACR high

- **Selected asset IDs:** uacr_base_explainer_v1_b, uacr_high_context_v1

```text
[base] Urine albumin-to-creatinine ratio (UACR)
The kidneys act as a precision filter — keeping proteins in the blood while clearing waste into urine. UACR measures how much albumin appears in urine relative to creatinine. Even small amounts can indicate the filtration membrane is under strain. Because albumin should largely stay in the blood, persistently raised urine albumin is a sensitive early signal of kidney stress — especially with hypertension or diabetes. The ratio corrects for urine concentration, making results more comparable across hydration states. Single-sample UACR is sensitive to exertion, illness, infection, and time of day — repeat confirmation is standard before acting on a finding.

[high] A UACR above the laboratory's reference range indicates that albumin is passing into the urine at a rate higher than expected. The kidney filtering membrane is allowing through a protein it would normally retain. Common contributing factors include sustained high blood pressure, elevated blood glucose, and kidney filtering membrane stress — but transient causes such as intense physical exertion, urinary infection, or illness in the days before sampling can also produce a t...
```

### WBC high

- **Selected asset IDs:** white_blood_cells_base_explainer_v1_b, wbc_high_context_v1

```text
[base] White blood cells (WBC)
White blood cells are the body's immune patrol — a diverse army of cells, each with a specific role in fighting infection, managing inflammation, and maintaining immune surveillance. They are produced in the bone marrow and continuously circulate in the blood at levels that reflect the current immune state. A full blood count measures the total WBC and, in a differential, the five main subtypes: neutrophils (rapid responders to bacterial infection and tissue damage), lymphocytes (involved in viral defence and immune memory), monocytes, eosinophils (relevant in allergy and parasitic responses), and basophils. Total WBC alone tells you the overall level of immune activity; the differential tells you why. An elevated total count may reflect infection, inflammation, physiological stress, certain medications, or haematological causes. A low total count can reflect viral suppression, specific medications, or bone marrow effects. The two directions have entirely different interpretive pathways.

[high] A total white blood cell count above the laboratory's reference range indicates that the immune system is more active than baseline. The most common short-...
```

### WBC low

- **Selected asset IDs:** white_blood_cells_base_explainer_v1_b, wbc_low_context_v1

```text
[base] White blood cells (WBC)
White blood cells are the body's immune patrol — a diverse army of cells, each with a specific role in fighting infection, managing inflammation, and maintaining immune surveillance. They are produced in the bone marrow and continuously circulate in the blood at levels that reflect the current immune state. A full blood count measures the total WBC and, in a differential, the five main subtypes: neutrophils (rapid responders to bacterial infection and tissue damage), lymphocytes (involved in viral defence and immune memory), monocytes, eosinophils (relevant in allergy and parasitic responses), and basophils. Total WBC alone tells you the overall level of immune activity; the differential tells you why. An elevated total count may reflect infection, inflammation, physiological stress, certain medications, or haematological causes. A low total count can reflect viral suppression, specific medications, or bone marrow effects. The two directions have entirely different interpretive pathways.

[low] A total white blood cell count below the laboratory's reference range indicates that circulating immune cells are reduced. The clinical significance depends...
```

### Creatine kinase high + exercise/statin modifiers

- **Selected asset IDs:** creatine_kinase_base_explainer_v1_b, creatine_kinase_high_context_v1, lifestyle_exercise_creatinine_ck_fragment_v1_b, medication_statin_lipid_context_fragment_v1_b

```text
[base] Creatine kinase (CK)
Muscle cells run a constant energy-recycling process, and creatine kinase (CK) is the enzyme at the centre of it. When muscle fibres are put under stress — from hard exercise, an injury, or certain medications — CK leaks into the bloodstream, where it can be measured. A temporary spike after vigorous or unaccustomed exercise is normal and typically resolves within a day or two. CK is also monitored on statins, where muscle effects are recognised but relatively uncommon. CK is found in skeletal and cardiac muscle; isoform pattern matters clinically, though routine panels measure total CK. Interpretation depends on degree of elevation, timing relative to activity, medications — particularly statins — and whether muscle symptoms are present. Without this context, a single CK reading has limited standalone meaning.

[high] A raised CK indicates that muscle fibres are releasing this enzyme into the bloodstream at a higher than usual rate. The most common and benign cause is vigorous or unaccustomed exercise — particularly resistance training — in the 24 to 72 hours before the sample was taken. This kind of rise is transient and expected. A persistently rai...
```

### Calcium high

- **Selected asset IDs:** calcium_base_explainer_v1_b, calcium_high_context_v1

```text
[base] Calcium
Calcium does far more than build bones — it triggers every heartbeat, drives muscle contraction, enables nerve signalling, and plays a role in blood clotting. It is one of the body's most tightly regulated minerals, maintained within a narrow range by parathyroid hormone (PTH) and vitamin D working in concert. Standard blood tests measure total calcium, which includes a fraction bound to albumin and a smaller biologically active ionised fraction. Because albumin affects the total reading, many laboratories report a corrected calcium figure that adjusts for albumin concentration — this is often more meaningful than total calcium alone. Calcium is most interpretable alongside albumin, vitamin D, PTH, and renal function. Without these, a total calcium reading can be misleading.

[high] A raised calcium result indicates that more calcium is circulating than the laboratory's reference range expects. The regulatory system that keeps calcium in balance — primarily parathyroid hormone (PTH) and vitamin D — may be producing more calcium release from bone or intestinal absorption than is being cleared. Common reasons for raised calcium include parathyroid-related changes, e...
```

### Calcium low

- **Selected asset IDs:** calcium_base_explainer_v1_b, calcium_low_context_v1

```text
[base] Calcium
Calcium does far more than build bones — it triggers every heartbeat, drives muscle contraction, enables nerve signalling, and plays a role in blood clotting. It is one of the body's most tightly regulated minerals, maintained within a narrow range by parathyroid hormone (PTH) and vitamin D working in concert. Standard blood tests measure total calcium, which includes a fraction bound to albumin and a smaller biologically active ionised fraction. Because albumin affects the total reading, many laboratories report a corrected calcium figure that adjusts for albumin concentration — this is often more meaningful than total calcium alone. Calcium is most interpretable alongside albumin, vitamin D, PTH, and renal function. Without these, a total calcium reading can be misleading.

[low] A low calcium result needs to be interpreted carefully before drawing conclusions. Total calcium in the blood includes a fraction bound to albumin, so if albumin is also low, the total calcium figure can appear reduced even when the biologically active (ionised) fraction is actually normal. A corrected calcium calculation accounts for this — it is an important first step in interpreting...
```

### Cortisol high (sampling-time limits in asset)

- **Selected asset IDs:** cortisol_base_explainer_v1_b, cortisol_high_context_v1

```text
[base] Cortisol
Cortisol is the body's primary stress hormone — it mobilises energy, dials down inflammation, and modulates blood pressure in response to physical or psychological demand. It is produced by the adrenal glands under instruction from the pituitary and hypothalamus, a signalling chain known as the HPA axis. Cortisol follows a strong diurnal rhythm: levels are typically at their peak shortly after waking and fall steeply across the day, reaching their lowest late at night. This rhythm makes timing critical — a reading that looks elevated at 9 am may be entirely expected, while the same number at midnight would not be. Cortisol is also influenced by glucocorticoid medications, some hormonal contraceptives, and acute stress at the time of sampling. A single cortisol reading without sampling time relative to waking loses most interpretive value — the HPA axis dynamic, not the snapshot, is what matters.

[high] A cortisol above the laboratory's reference range may have several explanations that depend almost entirely on when the sample was taken. In the early morning — when cortisol naturally peaks — a high reading may still be at the upper end of physiological variation...
```

### Cortisol low

- **Selected asset IDs:** cortisol_base_explainer_v1_b, cortisol_low_context_v1

```text
[base] Cortisol
Cortisol is the body's primary stress hormone — it mobilises energy, dials down inflammation, and modulates blood pressure in response to physical or psychological demand. It is produced by the adrenal glands under instruction from the pituitary and hypothalamus, a signalling chain known as the HPA axis. Cortisol follows a strong diurnal rhythm: levels are typically at their peak shortly after waking and fall steeply across the day, reaching their lowest late at night. This rhythm makes timing critical — a reading that looks elevated at 9 am may be entirely expected, while the same number at midnight would not be. Cortisol is also influenced by glucocorticoid medications, some hormonal contraceptives, and acute stress at the time of sampling. A single cortisol reading without sampling time relative to waking loses most interpretive value — the HPA axis dynamic, not the snapshot, is what matters.

[low] A cortisol below the laboratory's reference range carries very different weight depending on when the sample was taken. Late in the evening, low cortisol is physiologically expected — the diurnal rhythm falls to its lowest at this time. The same reading at 8–9 am, ...
```

### SHBG high

- **Selected asset IDs:** shbg_base_explainer_v1_b, shbg_high_context_v1

```text
[base] SHBG (sex hormone-binding globulin)
SHBG acts as the transport and availability regulator for sex hormones. The liver produces this protein, and it binds testosterone and oestradiol tightly — determining how much hormone is biologically active rather than just circulating. Only the fraction not bound to SHBG (or loosely bound to albumin) is immediately available to cells. This means SHBG level directly shapes how much usable hormone the body has access to, even when total hormone levels appear typical. SHBG is influenced by thyroid function, insulin levels, body weight, and certain medications including hormonal contraceptives and thyroid hormone replacement. High SHBG reduces the proportion of hormone available to tissues; low SHBG has the opposite effect. SHBG must be interpreted alongside total testosterone and free testosterone — a SHBG result without these markers gives an incomplete picture of hormone bioavailability.

[high] Raised SHBG means a higher proportion of circulating testosterone or oestradiol is bound to this transport protein and therefore less available to tissues. High SHBG is associated with hyperthyroidism, certain hormonal contraceptives, thyroid h...
```

### Free testosterone in-range

- **Selected asset IDs:** free_testosterone_base_explainer_v1_b, free_testosterone_in_range_context_v1

```text
[base] Free testosterone
Only a small fraction of testosterone in the bloodstream is immediately available to cells — this is free testosterone, unbound to transport proteins. Because total testosterone includes protein-bound fractions that may not be biologically active, free testosterone often gives a more complete picture of androgen availability, particularly where SHBG is abnormal. Most testosterone circulates either tightly bound to SHBG or loosely bound to albumin; the free fraction is typically less than three per cent of the total. Free testosterone values are commonly calculated from total testosterone, SHBG, and albumin rather than measured directly, because direct assay methods vary considerably between laboratories. Testosterone levels also follow a diurnal pattern — typically higher in the morning — so the timing of sampling matters. Free testosterone measurement methods vary considerably; calculated estimates depend on accurate SHBG and albumin values, and without these the calculation may be unreliable.

[in_range] Free testosterone within the laboratory's reference range suggests that the immediately available androgen fraction is not reduced below expected limi...
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

[in_range] A cystatin C result within the laboratory's reference range supports the picture that kidney filtration is not flagging a concern at this time. When combined with an in-range creatinine and eGFR, it reinforces confidence in the renal filtration assessment — two...
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

Run medical review on MR-BATCH-001B, then design a promotion/import sprint that maps approved assets into governed packs with runtime selection behind an explicit candidate flag.

