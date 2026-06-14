# Batch 2 Thyroid and Androgen Context Authority Review

## Executive summary

Overall verdict: the Batch 2 patterns are clinically plausible only when HealthIQ separates biological plausibility from runtime safety. Several androgen markers are useful in specialist endocrine practice, but only a subset are safe as deterministic HealthIQ runtime signals.

### Activation candidates

| Pattern | Status |
|---|---|
| Free T3 low | ACTIVATE_WITH_GATES |
| Free Androgen Index high | ACTIVATE_WITH_GATES, female-only unless later clinician sign-off expands use |
| Free testosterone high | ACTIVATE_WITH_GATES, sex-specific and assay-gated |
| Free testosterone low | ACTIVATE_WITH_GATES for adult male reduced-androgen-availability context only |

### Should not activate yet

| Pattern | Reason |
|---|---|
| DHEA high | Standalone DHEA is weaker than DHEA-S; activate only if source biomarker is clearly DHEA-S and gates are added |
| DHEA low | Too non-specific; age, illness, adrenal/pituitary context and steroid exposure confound interpretation |
| Free Androgen Index low | Weak, non-diagnostic, SHBG-driven and not guideline-supported as a standalone low-androgen signal |
| Free testosterone percentage high | Not sufficiently guideline-supported as a primary interpretation signal |
| Free testosterone percentage low | Not sufficiently guideline-supported as a primary interpretation signal |

### Highest-risk interpretation areas

- Mistaking low FT3 for thyroid disease without TSH/FT4 and illness/energy-availability context.
- Mistaking FAI/free testosterone high for PCOS or adrenal disease without sex, age, menstrual/menopause status, symptoms, SHBG and therapy/supplement context.
- Treating calculated free testosterone, direct analogue free testosterone, FAI, and free testosterone percentage as equivalent measures.
- Ignoring testosterone therapy, anabolic steroid exposure, DHEA supplementation, oral contraceptives, HRT, pregnancy, acute illness, calorie restriction or biotin interference.

### Most important required context fields

- Biological sex
- Age
- Pregnancy/postpartum status where relevant
- Menstrual / menopause status where relevant
- Thyroid medication use
- Testosterone therapy / anabolic-androgenic steroid exposure
- DHEA supplementation
- HRT / oral contraceptive / fertility treatment
- Recent acute illness / infection / recovery
- Calorie restriction, fasting, under-eating or recent significant weight loss
- Heavy training load / overtraining / low energy availability
- Biotin supplementation where immunoassays are used
- Relevant symptoms, separated into symptom-present, symptom-absent and not-answered states

---

## Pattern-by-pattern review

### Free T3 low

#### Proposed interpretation
Low T3 syndrome / non-thyroidal illness context / reduced peripheral T3 availability.

#### Clinical validity verdict
VALID_WITH_GATES

#### Clinical reasoning
Low T3 is a recognised biochemical pattern in non-thyroidal illness syndrome and may also be seen with severe or prolonged illness, calorie restriction, low energy availability and recovery states. It is not a standalone diagnosis of thyroid disease. NICE thyroid guidance centres assessment on TSH and FT4, with FT3 used selectively rather than as an isolated screening marker. Endotext describes non-thyroidal illness as commonly showing reduced T3, especially in illness contexts.

#### Required companion biomarkers

| Biomarker | Requirement level | Reason |
|---|---|---|
| TSH | REQUIRED | Needed to distinguish primary thyroid patterns from non-thyroidal or central patterns. |
| Free T4 | REQUIRED | Needed to assess whether low FT3 is isolated or part of broader thyroid hormone abnormality. |
| Free T3 | REQUIRED | Primary marker. |
| CRP / inflammatory marker | STRONGLY_RECOMMENDED | Supports illness/inflammation context. |
| ALT / AST / albumin | OPTIONAL_MODIFIER | Liver disease and systemic illness can affect thyroid hormone metabolism and binding. |
| Cortisol | OPTIONAL_MODIFIER | Relevant if severe illness or adrenal/endocrine context suspected. |
| Glucose / HbA1c | OPTIONAL_MODIFIER | Metabolic stress context only. |

#### Required context fields

| Context field | Classification | Reason |
|---|---|---|
| Thyroid medication use | REQUIRED_GATE | Thyroid treatment can invalidate naive interpretation. |
| Recent acute illness | REQUIRED_GATE | Central to safe low-T3 interpretation. |
| Recent infection | REQUIRED_GATE | Common non-thyroidal illness trigger. |
| Recovery from illness | REQUIRED_GATE | Low T3 may persist during recovery. |
| Calorie restriction / fasting | REQUIRED_GATE | Can reduce peripheral T3 availability. |
| Under-eating / low energy availability | REQUIRED_GATE | Important non-thyroidal explanation. |
| Recent significant weight loss | REQUIRED_GATE | Can lower T3 through adaptive energy conservation. |
| Heavy training load / overtraining | OPTIONAL_MODIFIER | Can contribute to low energy availability and endocrine adaptation. |
| Relevant thyroid symptoms | REQUIRED_DISCLOSURE_ONLY | Symptoms can guide follow-up wording but cannot diagnose. |
| Pregnancy / postpartum | EXCLUSION_CONDITION unless specific pregnancy/postpartum logic exists | Requires specialist reference ranges and context. |
| Medications affecting thyroid hormones | REQUIRED_GATE | Amiodarone, glucocorticoids, dopamine, anti-epileptics and others can alter TFTs. |
| Biotin supplementation | REQUIRED_DISCLOSURE_ONLY | Immunoassay interference can distort thyroid tests. |

#### Fail-closed rules

- Do not emit if TSH or FT4 is missing.
- Do not emit if thyroid medication use is unanswered.
- Do not emit if recent illness / infection / recovery and energy-availability questions are all unanswered.
- Do not emit if pregnancy/postpartum is disclosed and pregnancy-specific logic is not available.
- Do not emit if pattern suggests overt thyroid dysfunction requiring clinician interpretation, for example clearly abnormal TSH with abnormal FT4.
- Do not emit if assay interference is suspected and the lab result is discordant with the clinical pattern.

#### Edge cases / exclusions

- Acute illness or recovery phase
- Chronic systemic inflammation
- Calorie restriction, fasting, eating disorder risk or low carbohydrate dieting
- Overtraining / low energy availability
- Liver disease
- Thyroid hormone medication
- Amiodarone, glucocorticoids, dopamine, anti-epileptics
- Pregnancy/postpartum
- Biotin interference
- Laboratory variation and FT3 assay limitations

#### Safe wording

HealthIQ may say:
- "This pattern may be consistent with reduced peripheral T3 availability, which can sometimes be seen during illness, recovery, calorie restriction or low energy availability."
- "This is not diagnostic of thyroid disease on its own and should be interpreted alongside TSH, FT4, medication history and recent illness context."

HealthIQ must not say:
- "You have low T3 syndrome."
- "You have hypothyroidism."
- "Your thyroid is underactive."
- "You need thyroid hormone."

Maximum strength of claim: "may be consistent with".

Diagnosis language prohibited: yes.

Urgent medical advice wording: only if accompanied by severe symptoms or clearly dangerous thyroid/adrenal patterns outside this signal.

#### Runtime activation recommendation
ACTIVATE_WITH_GATES

#### Required activation gates

- FT3 low relative to lab range.
- TSH present.
- FT4 present.
- Thyroid medication question answered.
- Recent illness/infection/recovery context answered.
- Energy-availability context answered.
- Pregnancy/postpartum either not applicable/answered no, or pregnancy-specific logic available.
- Medication/biotin disclosure captured.

#### Confidence

| Domain | Confidence | Reason |
|---|---|---|
| Biological plausibility | HIGH | Low T3 is well described in non-thyroidal illness and energy-conservation contexts. |
| Clinical interpretation | MODERATE | Interpretation is highly context-dependent. |
| Runtime safety | MODERATE | Safe if strict gates are enforced. |
| Wording safety | HIGH | Cautious wording can avoid diagnosis. |

#### Evidence basis

| Source | Supports |
|---|---|
| NICE NG145, Thyroid disease: assessment and management — https://www.nice.org.uk/guidance/ng145 | TSH/FT4-centred thyroid assessment and cautious use of thyroid function tests. |
| Endotext, Non-Thyroidal Illness Syndrome — https://www.endotext.org/wp-content/uploads/pdfs/the-non-thyroidal-illness-syndrome.pdf | Low T3 pattern in non-thyroidal illness. |
| Endotext, Assay of Thyroid Hormone and Related Substances — https://www.ncbi.nlm.nih.gov/books/NBK279113/ | Thyroid hormone assay limitations and interference. |
| NICE exceptional surveillance on biotin interference — https://www.nice.org.uk/guidance/ng145/resources/2023-exceptional-surveillance-of-thyroid-disease-assessment-and-management-nice-guideline-ng145-pdf-17094825912517 | Need to consider biotin interference in thyroid function testing. |

---

### DHEA high

#### Proposed interpretation
Adrenal androgen excess context.

#### Clinical validity verdict
VALID_ONLY_AS_WEAK_CONTEXTUAL_SIGNAL

#### Clinical reasoning
High adrenal androgens can be clinically meaningful, but the more defensible marker is DHEA-S rather than standalone DHEA. DHEA-S is produced predominantly by the adrenal cortex and is commonly used in the investigation of adrenal androgen excess. The 2025 Society for Endocrinology androgen excess guideline states that elevated DHEAS strongly suggests an adrenal source and is useful in biochemical work-up. Standalone DHEA is less commonly used and more vulnerable to interpretive ambiguity.

#### Required companion biomarkers

| Biomarker | Requirement level | Reason |
|---|---|---|
| DHEA-S | REQUIRED | Required to make an adrenal-source interpretation defensible. |
| Total testosterone | REQUIRED | Helps classify androgen excess pattern. |
| Free testosterone or calculated free testosterone | STRONGLY_RECOMMENDED | Supports biochemical hyperandrogenism assessment. |
| SHBG | STRONGLY_RECOMMENDED | Needed for FAI/free testosterone context. |
| Androstenedione | STRONGLY_RECOMMENDED | Useful in androgen excess work-up. |
| 17-hydroxyprogesterone | STRONGLY_RECOMMENDED | Helps assess non-classic congenital adrenal hyperplasia when clinically relevant. |
| LH / FSH | OPTIONAL_MODIFIER | Helps contextualise ovarian axis patterns. |
| Cortisol / ACTH | OPTIONAL_MODIFIER | Relevant if adrenal pathology or adrenal insufficiency/excess is suspected. |
| HbA1c / glucose / insulin | OPTIONAL_MODIFIER | Insulin resistance can interact with androgen excess. |

#### Required context fields

| Context field | Classification | Reason |
|---|---|---|
| Biological sex | REQUIRED_GATE | Interpretation differs by sex. |
| Age | REQUIRED_GATE | DHEA/DHEA-S are strongly age-dependent. |
| Menstrual / menopause status | REQUIRED_GATE for females | Postmenopausal severe androgen excess carries different risk. |
| DHEA supplementation | EXCLUSION_CONDITION | Supplement use invalidates endogenous interpretation. |
| Testosterone therapy / anabolic steroid exposure | EXCLUSION_CONDITION | Invalidates endogenous androgen excess interpretation. |
| HRT / hormone therapy | REQUIRED_GATE | May alter interpretation. |
| Fertility treatment | REQUIRED_GATE | Can alter gonadal hormone interpretation. |
| Androgen excess symptoms | REQUIRED_DISCLOSURE_ONLY | Rapid virilisation changes escalation wording. |
| Acute illness or major stress | OPTIONAL_MODIFIER | Can affect endocrine axes. |
| Biotin supplementation | REQUIRED_DISCLOSURE_ONLY | Relevant to some immunoassays. |

#### Fail-closed rules

- Do not emit adrenal androgen excess signal if only DHEA is available and DHEA-S is missing.
- Do not emit if biological sex or age is missing.
- Do not emit as endogenous excess if DHEA supplementation, testosterone therapy or anabolic steroid exposure is disclosed.
- Do not emit routine educational wording if severe virilisation or rapid-onset symptoms are disclosed; escalate to clinician review wording.
- Do not emit if pregnancy is disclosed.

#### Edge cases / exclusions

- DHEA supplementation
- Testosterone therapy or anabolic steroid exposure
- PCOS
- Non-classic congenital adrenal hyperplasia
- Adrenal tumour/adrenal mass context
- Severe insulin resistance
- Menopause/postmenopause
- Pregnancy
- Assay variation

#### Safe wording

HealthIQ may say:
- "If this result represents DHEA-S rather than DHEA, an elevated value can sometimes support an adrenal contribution to androgen excess, but it is not diagnostic on its own."
- "This should be interpreted with testosterone, SHBG, symptoms, age, sex and supplement/medication context."

HealthIQ must not say:
- "You have adrenal androgen excess."
- "You have an adrenal tumour."
- "You have PCOS."
- "Your adrenal glands are overactive."

Maximum strength of claim: "can sometimes support" / "may contribute to".

Diagnosis language prohibited: yes.

Urgent medical advice wording: use prompt clinician review wording if rapid-onset virilisation, very high DHEA-S or severe androgen excess pattern is present.

#### Runtime activation recommendation
DO_NOT_ACTIVATE_YET_CONTEXT_MODEL_INSUFFICIENT

#### Required activation gates

Future activation would require:
- Explicit distinction between DHEA and DHEA-S.
- DHEA-S as primary adrenal androgen marker.
- Sex and age gates.
- Supplement/therapy exclusion.
- Testosterone/SHBG companion markers.
- Symptom severity gate.

#### Confidence

| Domain | Confidence | Reason |
|---|---|---|
| Biological plausibility | MODERATE | Adrenal androgen biology is strong, but DHEA alone is weaker than DHEA-S. |
| Clinical interpretation | LOW | Standalone DHEA is not enough for safe runtime interpretation. |
| Runtime safety | LOW | Current pattern name is ambiguous if DHEA and DHEA-S are conflated. |
| Wording safety | MODERATE | Safe wording is possible, but only if DHEA-S is explicit. |

#### Evidence basis

| Source | Supports |
|---|---|
| Society for Endocrinology Clinical Practice Guideline for the Evaluation of Androgen Excess in Women, 2025 — https://pmc.ncbi.nlm.nih.gov/articles/PMC12413683/ | DHEAS as useful adrenal-source marker in androgen excess work-up. |
| Lab Tests Online UK, DHEAS — https://labtestsonline.org.uk/tests/dheas | DHEAS use in adrenal function, adrenal tumours, virilisation and hirsutism investigation. |
| Sharma & Welt, Practical Approach to Hyperandrogenism in Women, 2021 — https://pmc.ncbi.nlm.nih.gov/articles/PMC8548673/ | DHEAS role and adrenal tumour exclusion when markedly elevated. |

---

### DHEA low

#### Proposed interpretation
Adrenal androgen reduction context.

#### Clinical validity verdict
VALID_ONLY_AS_WEAK_CONTEXTUAL_SIGNAL

#### Clinical reasoning
Low DHEA-S may increase suspicion of adrenal insufficiency when interpreted with cortisol/ACTH and clinical context, but it is not diagnostic. DHEA/DHEA-S decline with age and can be affected by illness, pituitary/adrenal disease and glucocorticoid exposure. Endotext describes low age/sex-adjusted DHEAS as an additional marker that can increase suspicion of primary adrenal insufficiency but not as diagnostic.

#### Required companion biomarkers

| Biomarker | Requirement level | Reason |
|---|---|---|
| DHEA-S | REQUIRED | Preferred stable adrenal androgen marker. |
| Morning cortisol | REQUIRED | Required before adrenal insufficiency framing. |
| ACTH | STRONGLY_RECOMMENDED | Helps distinguish primary vs central adrenal patterns. |
| Sodium / potassium | STRONGLY_RECOMMENDED | Supports adrenal insufficiency context when abnormal. |
| Renin / aldosterone | OPTIONAL_MODIFIER | Specialist adrenal context. |
| Total testosterone / SHBG | OPTIONAL_MODIFIER | Helps distinguish broader androgen availability. |
| LH / FSH | OPTIONAL_MODIFIER | Gonadal axis context. |

#### Required context fields

| Context field | Classification | Reason |
|---|---|---|
| Biological sex | REQUIRED_GATE | Reference ranges are sex-specific. |
| Age | REQUIRED_GATE | DHEA-S declines substantially with age. |
| Prescribed steroid use | EXCLUSION_CONDITION unless specialist logic exists | Glucocorticoids suppress adrenal androgen production. |
| HRT / hormone therapy | OPTIONAL_MODIFIER | Can alter symptoms and endocrine interpretation. |
| Acute illness or major stress | REQUIRED_GATE | Can alter adrenal-axis interpretation. |
| Symptoms of adrenal insufficiency | REQUIRED_DISCLOSURE_ONLY | Needed for safe escalation wording. |
| DHEA supplementation | EXCLUSION_CONDITION | Invalidates endogenous interpretation. |
| Calorie restriction / low energy availability | OPTIONAL_MODIFIER | Can affect endocrine axes. |

#### Fail-closed rules

- Do not emit if DHEA-S is missing.
- Do not emit adrenal insufficiency language without morning cortisol and preferably ACTH.
- Do not emit if age/sex are missing.
- Do not emit if prescribed glucocorticoid use is disclosed unless a steroid-exposure caveat path exists.
- Do not emit if DHEA supplementation is disclosed.
- Do not emit if symptoms suggest adrenal crisis; urgent clinical advice should override educational signal.

#### Edge cases / exclusions

- Normal ageing
- Glucocorticoid exposure
- Pituitary disease
- Primary adrenal insufficiency
- Chronic illness
- Acute severe illness
- DHEA supplementation
- Assay and reference range variability

#### Safe wording

HealthIQ may say:
- "A low age- and sex-adjusted DHEA-S can sometimes be seen with reduced adrenal androgen production, but it is non-specific and not diagnostic."
- "Interpretation requires cortisol, ACTH, medication history and clinical context."

HealthIQ must not say:
- "You have adrenal insufficiency."
- "You have Addison’s disease."
- "Your adrenal glands are failing."
- "You need DHEA."

Maximum strength of claim: "can sometimes be seen with".

Diagnosis language prohibited: yes.

Urgent medical advice wording: yes, if symptoms suggest adrenal crisis or severe adrenal insufficiency context.

#### Runtime activation recommendation
DO_NOT_ACTIVATE_EVIDENCE_INSUFFICIENT

#### Required activation gates

Not recommended yet. If reconsidered:
- DHEA-S not DHEA.
- Age/sex-adjusted range.
- Morning cortisol and ACTH.
- Steroid exposure exclusion.
- Symptom gate.

#### Confidence

| Domain | Confidence | Reason |
|---|---|---|
| Biological plausibility | MODERATE | DHEA-S is adrenal-derived and low in adrenal insufficiency contexts. |
| Clinical interpretation | LOW | Low DHEA-S is non-specific and age-dependent. |
| Runtime safety | LOW | High risk of over-interpretation. |
| Wording safety | MODERATE | Safe wording possible but weak product value. |

#### Evidence basis

| Source | Supports |
|---|---|
| Endotext, Adrenal Insufficiency — https://www.ncbi.nlm.nih.gov/books/NBK279083/ | Low age/sex-adjusted DHEAS can increase suspicion but is not diagnostic. |
| Endocrine Society Primary Adrenal Insufficiency Guideline, 2016 — https://www.endocrine.org/clinical-practice-guidelines/primary-adrenal-insufficiency | Diagnosis requires adrenal-axis testing, not DHEA alone. |
| Saini et al., DHEA-S in diagnosing adrenal insufficiency, 2025 — https://pmc.ncbi.nlm.nih.gov/articles/PMC12406124/ | DHEA-S can be low in primary/central adrenal insufficiency but is adjunctive. |

---

### Free Androgen Index high

#### Proposed interpretation
Biochemical hyperandrogenism context.

#### Clinical validity verdict
VALID_WITH_GATES

#### Clinical reasoning
FAI is a calculated estimate: total testosterone / SHBG × 100. It is used in women as a practical estimate of free testosterone and is recommended or accepted in PCOS/hyperandrogenism assessment. The 2023 International PCOS guideline recommends total and free testosterone for biochemical hyperandrogenism assessment and states that free testosterone can be estimated using FAI. The 2025 Society for Endocrinology androgen excess guideline supports using an index of free testosterone, particularly when total testosterone is normal but androgen excess is suspected.

#### Required companion biomarkers

| Biomarker | Requirement level | Reason |
|---|---|---|
| Total testosterone | REQUIRED | Numerator for FAI and core androgen marker. |
| SHBG | REQUIRED | Denominator for FAI; low SHBG can drive high FAI. |
| Free testosterone / calculated free testosterone | STRONGLY_RECOMMENDED | Helps confirm free androgen interpretation. |
| DHEA-S | STRONGLY_RECOMMENDED | Helps assess adrenal contribution. |
| Androstenedione | STRONGLY_RECOMMENDED | Useful if testosterone not elevated. |
| LH / FSH | OPTIONAL_MODIFIER | Ovarian axis context. |
| HbA1c / glucose / insulin | OPTIONAL_MODIFIER | Low SHBG and PCOS often relate to insulin resistance/metabolic context. |
| ALT / liver markers | OPTIONAL_MODIFIER | Liver disease affects SHBG. |
| TSH / FT4 | OPTIONAL_MODIFIER | Thyroid status affects SHBG. |
| Prolactin | OPTIONAL_MODIFIER | Relevant in menstrual disturbance/endocrine differential. |

#### Required context fields

| Context field | Classification | Reason |
|---|---|---|
| Biological sex | REQUIRED_GATE | FAI is mainly interpretable for biochemical hyperandrogenism in females. |
| Age | REQUIRED_GATE | Androgen ranges are age-dependent. |
| Menstrual / menopause status | REQUIRED_GATE for females | Interpretation differs premenopause/postmenopause. |
| HRT / hormone therapy | REQUIRED_GATE | Can alter SHBG/testosterone. |
| Oral contraceptive use | REQUIRED_GATE | Raises SHBG and suppresses androgens; affects interpretation. |
| Testosterone therapy / AAS exposure | EXCLUSION_CONDITION | Invalidates endogenous interpretation. |
| DHEA supplementation | EXCLUSION_CONDITION | Can contribute to androgen excess. |
| Fertility treatment | REQUIRED_GATE | Alters reproductive hormone interpretation. |
| Androgen excess symptoms | REQUIRED_DISCLOSURE_ONLY | Needed for safe context and escalation. |
| Pregnancy | EXCLUSION_CONDITION | Requires pregnancy-specific interpretation. |
| Biotin supplementation | REQUIRED_DISCLOSURE_ONLY | Immunoassay interference risk. |

#### Fail-closed rules

- Do not emit if total testosterone or SHBG missing.
- Do not emit if biological sex or age missing.
- Do not emit in males unless a separately approved male-specific FAI policy exists.
- Do not emit as endogenous hyperandrogenism if testosterone therapy, AAS or DHEA supplementation is disclosed.
- Do not emit if pregnancy is disclosed.
- Do not emit routine wording if rapid-onset virilisation or severe androgen excess symptoms are disclosed; use clinician-review escalation wording.

#### Edge cases / exclusions

- Low SHBG from obesity, insulin resistance, hypothyroidism, nephrotic syndrome or glucocorticoids
- High SHBG from oral contraceptives, pregnancy, hyperthyroidism or liver disease
- Menopause/postmenopause
- PCOS
- Non-classic congenital adrenal hyperplasia
- Adrenal or ovarian tumours in severe/rapid cases
- Assay limitations at low female testosterone concentrations

#### Safe wording

HealthIQ may say:
- "This pattern may be consistent with biochemical hyperandrogenism, especially when interpreted in a female patient alongside symptoms, menstrual status and companion androgens."
- "FAI is calculated from testosterone and SHBG, so a high result can reflect high testosterone, low SHBG, or both."

HealthIQ must not say:
- "You have PCOS."
- "You have an androgen disorder."
- "You have an adrenal or ovarian tumour."
- "This proves excess testosterone."

Maximum strength of claim: "may be consistent with".

Diagnosis language prohibited: yes.

Urgent medical advice wording: clinician review should be recommended if rapid virilisation, very high testosterone/DHEAS or postmenopausal new androgen excess is disclosed.

#### Runtime activation recommendation
ACTIVATE_WITH_GATES

#### Required activation gates

- FAI high relative to lab/sex-specific reference range.
- Total testosterone and SHBG present from same sample or same report context.
- Biological sex and age present.
- Female-specific interpretation only initially.
- Menstrual/menopause status answered where applicable.
- Hormone therapy/OCP/testosterone/AAS/DHEA supplement context answered.
- Pregnancy excluded or not applicable.
- Androgen excess symptom disclosure captured.

#### Confidence

| Domain | Confidence | Reason |
|---|---|---|
| Biological plausibility | HIGH | FAI reflects free androgen estimate through testosterone/SHBG. |
| Clinical interpretation | MODERATE | Useful in female hyperandrogenism but SHBG-driven confounding is common. |
| Runtime safety | MODERATE | Safe if sex-specific and therapy gates are strict. |
| Wording safety | HIGH | Cautious wording avoids diagnosis. |

#### Evidence basis

| Source | Supports |
|---|---|
| 2023 International Evidence-Based PCOS Guideline — https://www.asrm.org/practice-guidance/practice-committee-documents/recommendations-from-the-2023-international-evidence-based-guideline-for-the-assessment-and-management-of-polycystic-ovary-syndrome/ | Total and free testosterone recommended; free testosterone can be estimated by FAI. |
| Society for Endocrinology androgen excess guideline, 2025 — https://pmc.ncbi.nlm.nih.gov/articles/PMC12413683/ | Use index of free testosterone in evaluation of androgen excess. |
| Gloucestershire Hospitals NHS, FAI — https://www.gloshospitals.nhs.uk/our-services/services-we-offer/pathology/tests-and-investigations/free-androgen-index-fai/ | FAI formula and sample/interpretation caveats. |

---

### Free Androgen Index low

#### Proposed interpretation
Reduced free androgen availability context.

#### Clinical validity verdict
VALID_ONLY_AS_WEAK_CONTEXTUAL_SIGNAL

#### Clinical reasoning
Low FAI can reflect lower testosterone, higher SHBG, or both. It is not a strong standalone disease marker. In women, low androgen states are not diagnosed from FAI alone. In men, FAI is not the preferred diagnostic approach; testosterone deficiency evaluation relies on symptoms plus consistently low morning testosterone, with SHBG/free testosterone used selectively.

#### Required companion biomarkers

| Biomarker | Requirement level | Reason |
|---|---|---|
| Total testosterone | REQUIRED | Needed to know whether FAI is low due to testosterone. |
| SHBG | REQUIRED | Needed because high SHBG can drive low FAI. |
| Albumin | STRONGLY_RECOMMENDED | Needed for calculated free testosterone if used. |
| LH / FSH | STRONGLY_RECOMMENDED in males | Needed for gonadal axis context. |
| Oestradiol | OPTIONAL_MODIFIER | Relevant in women/HRT context. |
| TSH / FT4 | OPTIONAL_MODIFIER | Thyroid status can affect SHBG. |
| Liver markers | OPTIONAL_MODIFIER | Liver disease affects SHBG. |

#### Required context fields

| Context field | Classification | Reason |
|---|---|---|
| Biological sex | REQUIRED_GATE | Interpretation differs markedly. |
| Age | REQUIRED_GATE | Testosterone and SHBG are age-dependent. |
| HRT / oral contraceptives | REQUIRED_GATE | Can raise SHBG and lower FAI. |
| Menopause status | REQUIRED_GATE for females | Alters androgen context. |
| Testosterone therapy / AAS exposure | EXCLUSION_CONDITION | Invalidates endogenous low interpretation. |
| Androgen deficiency symptoms | REQUIRED_DISCLOSURE_ONLY | Needed, especially in males. |
| Acute illness / major stress | OPTIONAL_MODIFIER | Can transiently suppress gonadal axis. |
| Calorie restriction / overtraining | OPTIONAL_MODIFIER | Can suppress reproductive hormones. |

#### Fail-closed rules

- Do not emit if total testosterone or SHBG missing.
- Do not emit low-androgen wording if symptoms are not disclosed or answered.
- Do not emit in women as androgen deficiency.
- Do not emit in men as testosterone deficiency; at most route to total/free testosterone logic if available.
- Do not emit if therapy/supplement exposure invalidates interpretation.

#### Edge cases / exclusions

- High SHBG due to oral contraceptives, hyperthyroidism or liver disease
- Low total testosterone due to acute illness
- Age-related changes
- Menopause
- HRT
- Overtraining / low energy availability
- Assay variation

#### Safe wording

HealthIQ may say:
- "A low FAI can reflect lower testosterone, higher SHBG, or both, and is not diagnostic on its own."

HealthIQ must not say:
- "You have low androgen availability."
- "You have testosterone deficiency."
- "You need hormone treatment."

Maximum strength of claim: "can reflect".

Diagnosis language prohibited: yes.

Urgent medical advice wording: no, not based on FAI low alone.

#### Runtime activation recommendation
DO_NOT_ACTIVATE_EVIDENCE_INSUFFICIENT

#### Required activation gates

Do not activate as a primary signal. Use as optional modifier for total/free testosterone interpretation only.

#### Confidence

| Domain | Confidence | Reason |
|---|---|---|
| Biological plausibility | MODERATE | Mathematically reflects testosterone/SHBG balance. |
| Clinical interpretation | LOW | Not guideline-supported as standalone low-androgen signal. |
| Runtime safety | LOW | High risk of misleading low-androgen claims. |
| Wording safety | MODERATE | Safe wording possible but limited utility. |

#### Evidence basis

| Source | Supports |
|---|---|
| Endocrine Society testosterone guideline, 2018 — https://www.endocrine.org/clinical-practice-guidelines/testosterone-therapy | Testosterone deficiency requires symptoms and consistently low testosterone, not FAI alone. |
| Society for Endocrinology male hypogonadism position statement, 2018 — https://www.endocrinology.org/media/2710/male-hypogonadism-and-ageing-2018.pdf | Male hypogonadism interpretation requires symptoms and biochemical confirmation. |
| Gloucestershire Hospitals NHS, FAI — https://www.gloshospitals.nhs.uk/our-services/services-we-offer/pathology/tests-and-investigations/free-androgen-index-fai/ | FAI is calculated from testosterone and SHBG and should be interpreted cautiously. |

---

### Free testosterone high

#### Proposed interpretation
Androgen excess context.

#### Clinical validity verdict
VALID_WITH_GATES

#### Clinical reasoning
Free testosterone is clinically relevant in androgen excess assessment, especially in women, and in testosterone deficiency assessment where SHBG is abnormal. However, direct analogue free testosterone assays may be unreliable; calculated free testosterone depends on accurate total testosterone, SHBG and albumin. In women, high free testosterone can support biochemical hyperandrogenism but cannot diagnose PCOS, adrenal disease or ovarian disease alone. In men, high free testosterone requires careful assessment for testosterone therapy, anabolic steroid exposure and rare endogenous causes.

#### Required companion biomarkers

| Biomarker | Requirement level | Reason |
|---|---|---|
| Total testosterone | REQUIRED | Needed to contextualise free testosterone and assay plausibility. |
| SHBG | REQUIRED | Major determinant of free testosterone. |
| Albumin | STRONGLY_RECOMMENDED | Required for calculated free testosterone formulas. |
| DHEA-S | STRONGLY_RECOMMENDED in females | Helps assess adrenal contribution. |
| Androstenedione | STRONGLY_RECOMMENDED in females | Supports androgen excess work-up. |
| LH / FSH | STRONGLY_RECOMMENDED | Helps gonadal-axis interpretation. |
| Oestradiol | OPTIONAL_MODIFIER | Relevant in sex/hormone therapy context. |
| HbA1c / glucose / insulin | OPTIONAL_MODIFIER | Insulin resistance can lower SHBG and raise free androgen fraction. |
| Liver markers / TSH | OPTIONAL_MODIFIER | Liver and thyroid status influence SHBG. |

#### Required context fields

| Context field | Classification | Reason |
|---|---|---|
| Biological sex | REQUIRED_GATE | Interpretation differs by sex. |
| Age | REQUIRED_GATE | Age-specific ranges and risks. |
| Menstrual / menopause status | REQUIRED_GATE for females | Important for androgen excess differential. |
| Testosterone therapy | EXCLUSION_CONDITION for endogenous interpretation | Common cause of high free testosterone. |
| Anabolic steroid/AAS exposure | EXCLUSION_CONDITION | Invalidates endogenous interpretation. |
| DHEA supplementation | EXCLUSION_CONDITION or modifier | Can contribute to androgen excess. |
| HRT / hormone therapy | REQUIRED_GATE | Alters SHBG/androgens. |
| Oral contraceptive use | REQUIRED_GATE | Alters SHBG and testosterone. |
| Fertility treatment | REQUIRED_GATE | Alters reproductive hormones. |
| Androgen excess symptoms | REQUIRED_DISCLOSURE_ONLY | Needed for escalation and context. |
| Pregnancy | EXCLUSION_CONDITION | Requires specialist interpretation. |
| Biotin supplementation | REQUIRED_DISCLOSURE_ONLY | Some immunoassays may be affected. |

#### Fail-closed rules

- Do not emit if biological sex or age missing.
- Do not emit if total testosterone and SHBG are missing.
- Do not treat directly measured free testosterone as equivalent to calculated free testosterone unless assay method is known/accepted.
- Do not emit as endogenous excess if testosterone therapy/AAS is disclosed.
- Do not emit routine wording if rapid virilisation or severe pattern is disclosed.
- Do not emit in pregnancy.

#### Edge cases / exclusions

- Assay method uncertainty
- Calculated vs direct free testosterone differences
- Low SHBG states: obesity, insulin resistance, hypothyroidism
- High SHBG states: OCP, pregnancy, hyperthyroidism
- PCOS
- Adrenal/ovarian tumours in severe/rapid presentations
- Testosterone therapy/AAS
- DHEA supplementation
- Menopause/postmenopause

#### Safe wording

HealthIQ may say:
- "This pattern may be consistent with increased free androgen exposure, but it is not diagnostic on its own."
- "Interpretation depends on sex, age, total testosterone, SHBG, albumin, symptoms and hormone/supplement use."

HealthIQ must not say:
- "You have PCOS."
- "You have androgen excess disorder."
- "You have an adrenal or ovarian tumour."
- "This confirms high testosterone disease."

Maximum strength of claim: "may be consistent with".

Diagnosis language prohibited: yes.

Urgent medical advice wording: clinician review wording if severe/rapid virilisation or markedly elevated androgens.

#### Runtime activation recommendation
ACTIVATE_WITH_GATES

#### Required activation gates

- Free testosterone high relative to lab/sex-specific range.
- Biological sex and age present.
- Total testosterone and SHBG present.
- Albumin present if calculated free testosterone is used.
- Method flag: calculated/equilibrium dialysis preferred; direct analogue assay requires caution label.
- Hormone therapy/testosterone/AAS/DHEA/OCP context answered.
- Pregnancy excluded where applicable.
- Symptoms disclosure captured.

#### Confidence

| Domain | Confidence | Reason |
|---|---|---|
| Biological plausibility | HIGH | Free testosterone reflects bioactive androgen exposure. |
| Clinical interpretation | MODERATE | Stronger in female hyperandrogenism with proper assays and context. |
| Runtime safety | MODERATE | Safe with method and therapy gates. |
| Wording safety | HIGH | Cautious wording is straightforward. |

#### Evidence basis

| Source | Supports |
|---|---|
| 2023 International PCOS Guideline — https://www.asrm.org/practice-guidance/practice-committee-documents/recommendations-from-the-2023-international-evidence-based-guideline-for-the-assessment-and-management-of-polycystic-ovary-syndrome/ | Total and free testosterone in biochemical hyperandrogenism. |
| Endocrine Society testosterone therapy guideline, 2018 — https://www.endocrine.org/clinical-practice-guidelines/testosterone-therapy | Free testosterone estimation when SHBG abnormal; diagnosis requires symptoms and reliable assays. |
| Bhasin et al., Testosterone Therapy in Men With Hypogonadism, JCEM 2018 PDF — https://genetic.org/wp-content/uploads/2016/01/KS-Testosterone-Hypogonadism-Guidelines-2018.pdf | Free testosterone should be measured by equilibrium dialysis or calculated from total testosterone, SHBG and albumin. |
| Society for Endocrinology androgen excess guideline, 2025 — https://pmc.ncbi.nlm.nih.gov/articles/PMC12413683/ | Androgen excess evaluation and severe androgen excess risk framing. |

---

### Free testosterone low

#### Proposed interpretation
Androgen deficiency / reduced androgen availability context.

#### Clinical validity verdict
VALID_WITH_GATES

#### Clinical reasoning
Low free testosterone can support reduced androgen availability, particularly in adult males with compatible symptoms and low or borderline total testosterone, especially where SHBG is abnormal. Endocrine Society guidance requires both symptoms/signs and consistently low testosterone concentrations to diagnose hypogonadism; HealthIQ must not diagnose hypogonadism. In women, low free testosterone is not a robust standalone consumer interpretation pattern.

#### Required companion biomarkers

| Biomarker | Requirement level | Reason |
|---|---|---|
| Total testosterone | REQUIRED | Primary biochemical anchor. |
| SHBG | REQUIRED | Needed for free testosterone context. |
| Albumin | STRONGLY_RECOMMENDED | Required for calculated free testosterone formulas. |
| LH | STRONGLY_RECOMMENDED in adult males | Helps distinguish primary vs secondary gonadal patterns. |
| FSH | STRONGLY_RECOMMENDED in adult males | Gonadal axis context. |
| Prolactin | OPTIONAL_MODIFIER | Relevant to secondary hypogonadism differential. |
| TSH / FT4 | OPTIONAL_MODIFIER | Thyroid disease can affect symptoms and SHBG. |
| HbA1c / glucose | OPTIONAL_MODIFIER | Metabolic disease can affect testosterone. |
| Liver / renal markers | OPTIONAL_MODIFIER | Chronic disease can suppress gonadal axis or alter binding. |

#### Required context fields

| Context field | Classification | Reason |
|---|---|---|
| Biological sex | REQUIRED_GATE | Initial activation should be adult male-only. |
| Age | REQUIRED_GATE | Testosterone interpretation is age-dependent. |
| Time of sample / morning sample if available | REQUIRED_DISCLOSURE_ONLY | Testosterone is diurnal; morning confirmation is standard. |
| Androgen deficiency symptoms | REQUIRED_GATE | Diagnosis/interpretation requires symptoms, not labs alone. |
| Acute illness / major stress | REQUIRED_GATE | Can transiently suppress testosterone. |
| Calorie restriction / low energy availability | REQUIRED_GATE | Can suppress reproductive axis. |
| Heavy training / overtraining | OPTIONAL_MODIFIER | Can lower testosterone through recovery stress. |
| Testosterone therapy / AAS exposure | EXCLUSION_CONDITION | Invalidates endogenous low interpretation. |
| Opioids / glucocorticoids / relevant medication classes | REQUIRED_DISCLOSURE_ONLY | Can suppress gonadal axis. |
| Fertility goals/treatment | REQUIRED_DISCLOSURE_ONLY | Not for treatment advice, but important caveat. |

#### Fail-closed rules

- Do not emit if biological sex or age missing.
- Do not emit for females until separate clinician-reviewed low-androgen policy exists.
- Do not emit if total testosterone or SHBG missing.
- Do not emit if androgen-deficiency symptoms are not answered.
- Do not emit if acute illness/recovery or calorie restriction context is unanswered.
- Do not emit if testosterone therapy/AAS exposure is disclosed.
- Do not diagnose hypogonadism.

#### Edge cases / exclusions

- Acute illness
- Sleep deprivation
- Calorie restriction / overtraining
- Obesity/metabolic disease
- Opioids, glucocorticoids and other medications
- High SHBG causing low free testosterone despite normal total testosterone
- Low SHBG affecting total/free interpretation
- Assay method uncertainty
- Age-related decline

#### Safe wording

HealthIQ may say:
- "In an adult male, this pattern may be consistent with reduced free androgen availability if it is persistent and accompanied by relevant symptoms."
- "This is not diagnostic of hypogonadism and usually requires repeat morning testing and clinical assessment."

HealthIQ must not say:
- "You have hypogonadism."
- "You are testosterone deficient."
- "You need testosterone."
- "This explains your symptoms."

Maximum strength of claim: "may be consistent with".

Diagnosis language prohibited: yes.

Urgent medical advice wording: no, unless combined with pituitary/red-flag symptoms outside this signal.

#### Runtime activation recommendation
ACTIVATE_WITH_GATES

#### Required activation gates

- Adult male context.
- Free testosterone low relative to lab/age/sex range.
- Total testosterone and SHBG present.
- Albumin present if calculated free testosterone used.
- Symptoms answered.
- Acute illness and energy-availability context answered.
- Testosterone/AAS exposure answered no.
- Wording includes repeat-morning-test caveat.

#### Confidence

| Domain | Confidence | Reason |
|---|---|---|
| Biological plausibility | HIGH | Low free testosterone can reflect reduced androgen availability. |
| Clinical interpretation | MODERATE | Requires symptoms, repeat testing and context. |
| Runtime safety | MODERATE | Safe as non-diagnostic adult male signal with gates. |
| Wording safety | HIGH | Clear non-diagnostic wording is feasible. |

#### Evidence basis

| Source | Supports |
|---|---|
| Endocrine Society testosterone guideline, 2018 — https://www.endocrine.org/clinical-practice-guidelines/testosterone-therapy | Diagnosis requires symptoms and consistently low testosterone; avoid screening healthy men. |
| Bhasin et al., JCEM 2018 PDF — https://genetic.org/wp-content/uploads/2016/01/KS-Testosterone-Hypogonadism-Guidelines-2018.pdf | Accurate free testosterone measurement/calculation requirements. |
| Society for Endocrinology male hypogonadism position statement, 2018 — https://www.endocrinology.org/media/2710/male-hypogonadism-and-ageing-2018.pdf | Symptoms are non-specific and biochemical confirmation is required. |

---

### Free testosterone percentage high

#### Proposed interpretation
Elevated free androgen fraction context.

#### Clinical validity verdict
VALID_ONLY_AS_WEAK_CONTEXTUAL_SIGNAL

#### Clinical reasoning
Free testosterone percentage is a ratio/fraction, usually reflecting the relationship between free testosterone, total testosterone and binding proteins, especially SHBG. It can provide mechanistic context but is not a guideline-standard primary signal for diagnosing androgen excess. A high percentage may result from low SHBG rather than excess androgen production.

#### Required companion biomarkers

| Biomarker | Requirement level | Reason |
|---|---|---|
| Total testosterone | REQUIRED | Needed to interpret percent free testosterone. |
| Free testosterone | REQUIRED | Numerator for fraction. |
| SHBG | REQUIRED | Major determinant of free fraction. |
| Albumin | STRONGLY_RECOMMENDED | Binding context if calculated. |
| HbA1c / glucose / insulin | OPTIONAL_MODIFIER | Low SHBG/metabolic context. |
| Liver markers / TSH | OPTIONAL_MODIFIER | SHBG modifiers. |

#### Required context fields

| Context field | Classification | Reason |
|---|---|---|
| Biological sex | REQUIRED_GATE | Interpretation differs by sex. |
| Age | REQUIRED_GATE | Age and sex ranges differ. |
| Testosterone therapy / AAS | EXCLUSION_CONDITION | Invalidates endogenous interpretation. |
| Hormonal contraception / HRT | REQUIRED_GATE | Alters SHBG. |
| Pregnancy | EXCLUSION_CONDITION | Alters binding proteins. |
| Metabolic context | OPTIONAL_MODIFIER | Low SHBG often tracks metabolic state. |

#### Fail-closed rules

- Do not emit if total testosterone, free testosterone or SHBG are missing.
- Do not emit as androgen excess.
- Do not emit if therapy/supplement exposure invalidates endogenous interpretation.
- Do not emit if assay/calc method unknown.

#### Edge cases / exclusions

- Low SHBG from insulin resistance/obesity/hypothyroidism
- High SHBG from OCP/pregnancy/hyperthyroidism
- Calculation method variation
- Testosterone therapy/AAS

#### Safe wording

HealthIQ may say:
- "A higher free testosterone percentage can reflect a greater unbound fraction, often influenced by SHBG."

HealthIQ must not say:
- "You have androgen excess."
- "You have high testosterone disease."
- "This is diagnostic."

Maximum strength of claim: "can reflect".

Diagnosis language prohibited: yes.

Urgent medical advice wording: no.

#### Runtime activation recommendation
DO_NOT_ACTIVATE_EVIDENCE_INSUFFICIENT

#### Required activation gates

Do not activate as a primary signal. Use only as optional modifier inside free testosterone or FAI logic.

#### Confidence

| Domain | Confidence | Reason |
|---|---|---|
| Biological plausibility | MODERATE | Fraction has binding-protein logic. |
| Clinical interpretation | LOW | Not guideline-standard as primary signal. |
| Runtime safety | LOW | Easy to overinterpret. |
| Wording safety | MODERATE | Safe as a modifier only. |

#### Evidence basis

| Source | Supports |
|---|---|
| Endocrine Society testosterone guideline, 2018 — https://www.endocrine.org/clinical-practice-guidelines/testosterone-therapy | Prefer total/free testosterone assessment with SHBG context, not percent-free standalone diagnosis. |
| Bhasin et al., JCEM 2018 PDF — https://genetic.org/wp-content/uploads/2016/01/KS-Testosterone-Hypogonadism-Guidelines-2018.pdf | Free testosterone estimates depend on total testosterone, SHBG and albumin. |

---

### Free testosterone percentage low

#### Proposed interpretation
Reduced free androgen fraction context.

#### Clinical validity verdict
VALID_ONLY_AS_WEAK_CONTEXTUAL_SIGNAL

#### Clinical reasoning
Low free testosterone percentage usually reflects higher binding or lower free fraction relative to total testosterone. It is not a guideline-standard primary interpretation signal for androgen deficiency. It may be useful as a modifier when total testosterone, free testosterone, SHBG and symptoms are already interpreted.

#### Required companion biomarkers

| Biomarker | Requirement level | Reason |
|---|---|---|
| Total testosterone | REQUIRED | Needed to interpret fraction. |
| Free testosterone | REQUIRED | Needed to interpret fraction. |
| SHBG | REQUIRED | Main binding-protein explanation. |
| Albumin | STRONGLY_RECOMMENDED | Binding context if calculated. |
| TSH / FT4 | OPTIONAL_MODIFIER | Thyroid status can alter SHBG. |
| Liver markers | OPTIONAL_MODIFIER | Liver disease can alter SHBG. |

#### Required context fields

| Context field | Classification | Reason |
|---|---|---|
| Biological sex | REQUIRED_GATE | Sex-specific interpretation. |
| Age | REQUIRED_GATE | Age-specific interpretation. |
| HRT / oral contraceptives | REQUIRED_GATE | Can increase SHBG and lower fraction. |
| Pregnancy | EXCLUSION_CONDITION | Binding proteins change substantially. |
| Androgen deficiency symptoms | REQUIRED_DISCLOSURE_ONLY | Needed before any low-androgen context. |
| Acute illness / low energy availability | OPTIONAL_MODIFIER | Can alter gonadal axis. |

#### Fail-closed rules

- Do not emit as primary signal.
- Do not emit if total/free testosterone and SHBG are missing.
- Do not emit low-androgen wording without symptoms and total/free testosterone interpretation.
- Do not emit in pregnancy.

#### Edge cases / exclusions

- High SHBG due to OCP, pregnancy, hyperthyroidism, liver disease
- Assay/calculation variation
- Low total testosterone with normal fraction
- Acute illness and energy restriction

#### Safe wording

HealthIQ may say:
- "A lower free testosterone percentage can reflect a lower unbound fraction, often influenced by SHBG."

HealthIQ must not say:
- "You have androgen deficiency."
- "You have hypogonadism."
- "You need testosterone."

Maximum strength of claim: "can reflect".

Diagnosis language prohibited: yes.

Urgent medical advice wording: no.

#### Runtime activation recommendation
DO_NOT_ACTIVATE_EVIDENCE_INSUFFICIENT

#### Required activation gates

Do not activate as primary signal. Use only as optional modifier.

#### Confidence

| Domain | Confidence | Reason |
|---|---|---|
| Biological plausibility | MODERATE | Fraction reflects binding-protein physiology. |
| Clinical interpretation | LOW | Not standalone clinically decisive. |
| Runtime safety | LOW | High risk of misleading low-androgen claims. |
| Wording safety | MODERATE | Safe as modifier only. |

#### Evidence basis

| Source | Supports |
|---|---|
| Endocrine Society testosterone guideline, 2018 — https://www.endocrine.org/clinical-practice-guidelines/testosterone-therapy | Testosterone deficiency interpretation requires symptoms and reliable testosterone assessment. |
| Bhasin et al., JCEM 2018 PDF — https://genetic.org/wp-content/uploads/2016/01/KS-Testosterone-Hypogonadism-Guidelines-2018.pdf | Free testosterone estimates depend on total testosterone, SHBG and albumin. |

---

## Cross-pattern synthesis

### Shared androgen interpretation principles

1. Biological sex and age are mandatory gates.
2. Female hyperandrogenism and male androgen deficiency are different interpretation domains and must not share generic wording.
3. Testosterone therapy, anabolic steroid exposure and DHEA supplementation are exclusion conditions for endogenous androgen interpretation.
4. FAI is suitable mainly as a female biochemical hyperandrogenism support marker.
5. Low FAI and free testosterone percentage values are weak as primary signals.
6. Calculated free testosterone, equilibrium dialysis free testosterone and direct analogue free testosterone must not be treated as automatically equivalent.
7. SHBG is central: abnormal SHBG can create misleading FAI/free fraction patterns.
8. Severe or rapid-onset virilisation requires clinician-review escalation wording, not consumer educational signal wording.
9. Pregnancy requires exclusion unless pregnancy-specific endocrine logic exists.

### Shared thyroid low-T3 interpretation principles

1. Low FT3 is not a standalone thyroid disease signal.
2. TSH and FT4 are required companion biomarkers.
3. Illness, recovery and energy availability are required context gates.
4. Thyroid medication and thyroid-affecting medication exposure must be captured.
5. Pregnancy/postpartum requires exclusion unless specific logic exists.
6. Biotin/interference disclosure should be captured when immunoassays are used.

### Shared context fields reusable across future biomarkers

| Context primitive | Purpose |
|---|---|
| biological_sex | Mandatory endocrine interpretation gate. |
| age | Age-specific endocrine ranges and disease probabilities. |
| pregnancy_postpartum_status | Exclusion or specialist pathway for thyroid/androgen interpretation. |
| menstrual_menopause_status | Required for female androgen interpretation. |
| thyroid_medication_use | Required for thyroid pattern interpretation. |
| testosterone_therapy_or_AAS | Exclusion for endogenous androgen interpretation. |
| DHEA_supplementation | Exclusion/modifier for adrenal androgen interpretation. |
| HRT_or_oral_contraceptive_use | Required for SHBG/androgen interpretation. |
| recent_acute_illness_or_recovery | Required for low-T3 and low-testosterone interpretation. |
| energy_availability_status | Required for low-T3 and low-testosterone interpretation. |
| heavy_training_load | Modifier for endocrine suppression/adaptation. |
| biotin_supplementation | Immunoassay interference disclosure. |
| symptom_cluster_disclosure | Required for safe wording and escalation. |

### Recommended HealthIQ context primitives

Use explicit states rather than Boolean-only logic:

```text
answered_yes
answered_no
not_answered
unknown
not_applicable
```

Separate:

```text
disclosure_state
positive_exposure
negative_exposure
missing_context
not_applicable
```

Recommended primitive groups:

- `sex_age_context`
- `female_reproductive_context`
- `pregnancy_postpartum_context`
- `thyroid_medication_context`
- `hormone_therapy_context`
- `androgen_exposure_context`
- `supplement_interference_context`
- `acute_illness_recovery_context`
- `energy_availability_context`
- `training_recovery_pressure_context`
- `symptom_cluster_context`

### Recommended package activation order

1. Free T3 low, because it has clear gates and strong fail-closed rules.
2. FAI high, female-only, because guideline support exists when testosterone/SHBG and reproductive context are present.
3. Free testosterone high, with sex-specific and method-specific gates.
4. Free testosterone low, adult male-only, symptom-gated.
5. Defer DHEA high/low until DHEA vs DHEA-S identity is resolved.
6. Do not promote FAI low or free testosterone percentage high/low as primary signals; retain only as modifiers.

### Recommended STOP gates before runtime activation

- STOP if context states cannot distinguish answered_no from not_answered.
- STOP if testosterone therapy/AAS/DHEA supplementation cannot be captured.
- STOP if biological sex or age are absent.
- STOP if pregnancy/postpartum cannot be excluded or routed.
- STOP if FT3 low can fire without TSH and FT4.
- STOP if FAI high can fire without total testosterone and SHBG.
- STOP if free testosterone logic cannot distinguish calculated/equilibrium dialysis/direct assay where available.
- STOP if DHEA and DHEA-S are not separated as distinct biomarkers.
- STOP if symptom fields are not available for low testosterone interpretation.
- STOP if clinician-review escalation wording cannot override routine educational wording for severe androgen excess patterns.

---

## Final activation matrix

| Pattern | Activate? | Required gates | External clinician sign-off required? | Confidence | Notes |
|---|---|---|---|---|---|
| Free T3 low | ACTIVATE_WITH_GATES | FT3 low + TSH + FT4 + illness/recovery + energy availability + thyroid medication context | No, if non-diagnostic wording enforced | MODERATE | Must not imply thyroid disease. |
| DHEA high | DO_NOT_ACTIVATE_YET_CONTEXT_MODEL_INSUFFICIENT | Future: DHEA-S explicit + sex/age + testosterone/SHBG + supplement exclusions | Yes before activation | LOW | DHEA-S high may become valid; DHEA alone should not. |
| DHEA low | DO_NOT_ACTIVATE_EVIDENCE_INSUFFICIENT | Future: DHEA-S + cortisol/ACTH + sex/age + steroid exposure | Yes before activation | LOW | Too non-specific for runtime signal. |
| Free Androgen Index high | ACTIVATE_WITH_GATES | Female + age + total testosterone + SHBG + menopause/menstrual context + therapy exclusions + pregnancy excluded | Not routinely; yes for severe/rapid virilisation pathway | MODERATE | Strongest androgen activation candidate. |
| Free Androgen Index low | DO_NOT_ACTIVATE_EVIDENCE_INSUFFICIENT | N/A as primary signal | Yes if ever reconsidered | LOW | Use only as modifier. |
| Free testosterone high | ACTIVATE_WITH_GATES | Sex/age + total testosterone + SHBG + method flag + therapy exclusions + symptom disclosure | Not routinely; yes for severe/rapid virilisation/high severity | MODERATE | Strong but assay/context-dependent. |
| Free testosterone low | ACTIVATE_WITH_GATES | Adult male + symptoms + total testosterone + SHBG + illness/energy context + therapy exclusions | No, if non-diagnostic and repeat-test caveat enforced | MODERATE | Do not diagnose hypogonadism. |
| Free testosterone percentage high | DO_NOT_ACTIVATE_EVIDENCE_INSUFFICIENT | N/A as primary signal | Yes if ever reconsidered | LOW | Modifier only; SHBG-driven. |
| Free testosterone percentage low | DO_NOT_ACTIVATE_EVIDENCE_INSUFFICIENT | N/A as primary signal | Yes if ever reconsidered | LOW | Modifier only; SHBG-driven. |

---

## Unresolved research questions

1. Should HealthIQ canonicalise the "DHEA" package to DHEA-S where the lab marker is actually DHEA-S, or maintain separate DHEA and DHEA-S signal families?
2. Which free testosterone methods will HealthIQ accept as runtime-safe: equilibrium dialysis, calculated free testosterone, LC-MS/MS-derived calculations, or direct analogue immunoassay?
3. Should high free testosterone in males produce a signal at all, or only a therapy/supplement caveat unless symptoms and companion markers indicate endogenous excess?
4. What severity thresholds should trigger clinician-review wording for androgen excess, especially postmenopausal women or rapid virilisation?
5. Should FAI high be restricted to premenopausal females initially, or include postmenopausal females only under external clinician sign-off?
6. Should HealthIQ collect oral contraceptive use as a distinct context primitive rather than generic HRT/hormone therapy?
7. Can low testosterone patterns safely activate without two repeat morning samples, or should HealthIQ only state that a single low result "may warrant repeat confirmation"?
8. Should FT3 low activation require inflammatory marker availability, or is declared illness/energy context sufficient?
9. Should biotin disclosure be a universal endocrine assay primitive across thyroid, androgen and adrenal packages?

---

## Source list

1. NICE NG145: Thyroid disease: assessment and management — https://www.nice.org.uk/guidance/ng145
2. NICE 2023 exceptional surveillance: biotin interference in thyroid function tests — https://www.nice.org.uk/guidance/ng145/resources/2023-exceptional-surveillance-of-thyroid-disease-assessment-and-management-nice-guideline-ng145-pdf-17094825912517
3. Endotext: The Non-Thyroidal Illness Syndrome — https://www.endotext.org/wp-content/uploads/pdfs/the-non-thyroidal-illness-syndrome.pdf
4. Endotext: Assay of Thyroid Hormone and Related Substances — https://www.ncbi.nlm.nih.gov/books/NBK279113/
5. 2023 International Evidence-Based PCOS Guideline summary — https://www.asrm.org/practice-guidance/practice-committee-documents/recommendations-from-the-2023-international-evidence-based-guideline-for-the-assessment-and-management-of-polycystic-ovary-syndrome/
6. Society for Endocrinology Clinical Practice Guideline for the Evaluation of Androgen Excess in Women, 2025 — https://pmc.ncbi.nlm.nih.gov/articles/PMC12413683/
7. Sharma A, Welt CK. Practical Approach to Hyperandrogenism in Women, 2021 — https://pmc.ncbi.nlm.nih.gov/articles/PMC8548673/
8. Gloucestershire Hospitals NHS: Free Androgen Index — https://www.gloshospitals.nhs.uk/our-services/services-we-offer/pathology/tests-and-investigations/free-androgen-index-fai/
9. Endocrine Society: Testosterone Therapy for Hypogonadism Guideline, 2018 — https://www.endocrine.org/clinical-practice-guidelines/testosterone-therapy
10. Bhasin et al. Testosterone Therapy in Men With Hypogonadism, JCEM 2018 PDF — https://genetic.org/wp-content/uploads/2016/01/KS-Testosterone-Hypogonadism-Guidelines-2018.pdf
11. Society for Endocrinology Position Statement on Male Hypogonadism and Ageing, 2018 — https://www.endocrinology.org/media/2710/male-hypogonadism-and-ageing-2018.pdf
12. Endocrine Society: Primary Adrenal Insufficiency Guideline, 2016 — https://www.endocrine.org/clinical-practice-guidelines/primary-adrenal-insufficiency
13. Endotext: Adrenal Insufficiency — https://www.ncbi.nlm.nih.gov/books/NBK279083/
14. Lab Tests Online UK: DHEAS — https://labtestsonline.org.uk/tests/dheas
15. Saini et al. DHEA-S in diagnosing adrenal insufficiency, 2025 — https://pmc.ncbi.nlm.nih.gov/articles/PMC12406124/
