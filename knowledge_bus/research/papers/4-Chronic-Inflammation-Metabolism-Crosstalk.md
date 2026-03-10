### **1\. Executive Summary**

Chronic systemic inflammation, specifically "metaflammation," is a subacute, persistent state driven by metabolic excess and mediated by the innate immune system within adipose, hepatic, and vascular tissues.1 This crosstalk reinforces metabolic dysfunction, where low-grade inflammatory signaling directly blunts insulin sensitivity and promotes vascular remodeling.2

This report evaluates the interaction between metabolic health and inflammatory load using three primary research signals: high-sensitivity C-reactive protein (hs-CRP), the neutrophil-to-lymphocyte ratio (NLR), and white blood cell (WBC) distribution.4 The biological question addressed is whether a user's current inflammatory burden is sufficient to accelerate insulin resistance and cardiovascular aging.1

The primary metric recommended for platform use is the **Neutrophil-to-Lymphocyte Ratio (NLR)**, supported by the **Metabolic Score for Insulin Resistance (METS-IR)** as a required integrative metric. Tier 1 evidence from prospective cohort studies (NHANES, Kailuan, MELANY) demonstrates that these markers are robust, independent predictors of incident type 2 diabetes, diabetic kidney disease, and cardiovascular mortality.

### ---

**2\. Biological Question**

"Based on my blood test results, is chronic inflammatory load interacting with my metabolism to increase my risk of insulin resistance, vascular damage, and accelerated metabolic aging?"

### ---

**3\. Clinical Rationale**

* **Disease Prediction:** This signal identifies subclinical "metaflammation," which predicts the progression from normoglycemia to prediabetes and overt type 2 diabetes (T2DM). It also detects "residual inflammatory risk" in patients with optimal lipid profiles who remain at risk for major adverse cardiovascular events (MACE).8  
* **Pathophysiological Mechanism:**  
  * **Insulin Resistance:** Pro-inflammatory cytokines (TNF\-![][image1], IL-6) released from hypertrophied adipose tissue activate intracellular kinases (JNK, IKK$\\beta$) that catalyze inhibitory serine phosphorylation of insulin receptor substrate 1 (IRS-1), blunting glucose uptake.  
  * **Vascular Damage:** Hyperglycemia activates neutrophils to release reactive oxygen species (ROS) and form neutrophil extracellular traps (NETs), which promote endothelial dysfunction and microthrombosis.3  
  * **Metabolic Aging:** "Inflammaging" is driven by the accumulation of cellular debris ("garb-aging") and Senescence-Associated Secretory Phenotype (SASP) factors that disrupt mitochondrial function and nutrient-sensing pathways (mTOR, AMPK).11  
* **Disease Stage:** These signals move early in the subclinical phase, often years before HbA1c or fasting glucose meet diagnostic criteria for prediabetes.  
* **Clinical Importance:** Early detection allows for the intensification of anti-inflammatory lifestyle strategies or the initiation of metabolic therapies (e.g., SGLT2 inhibitors, GLP-1 RAs) that simultaneously target both inflammation and glycemic control.

### ---

**4\. Evidence Base**

| Field | Content |
| :---- | :---- |
| Study name / first author | Kailuan Study / Wang et al. 13 |
| Journal | ResearchGate / JAPI |
| Year | 2025 |
| DOI | Unavailable |
| Design | Prospective cohort |
| Sample size | n=94,841 |
| Follow-up | 13.1 years |
| Key finding | MetS combined with hs-CRP \>3 mg/L increases heart failure risk 1.85-fold (HR 1.85) |
| Threshold derived | hs-CRP \> 3.0 mg/L |
| Limitations | Primarily East Asian population |

| Field | Content |
| :---- | :---- |
| Study name / first author | NHANES / Dong et al. 14 |
| Journal | PMC |
| Year | 2023 |
| DOI | 10.1186/s12933-023-01998-y |
| Design | Prospective cohort (NHANES 2003–2016) |
| Sample size | n=3,251 |
| Follow-up | Median 91 months |
| Key finding | NLR \>3.48 associated with a 2.03-fold risk of all-cause mortality and 2.76-fold risk of CVD mortality |
| Threshold derived | NLR \> 3.48 |
| Limitations | Self-reported diabetes diagnosis included |

| Field | Content |
| :---- | :---- |
| Study name / first author | MELANY Cohort / Twig et al. 15 |
| Journal | PMC |
| Year | 2013 |
| DOI | 10.2337/dc12-1143 |
| Design | Prospective cohort |
| Sample size | n=24,897 |
| Follow-up | 7.5 years |
| Key finding | WBC count \>6,900 cells/![][image2] within the normal range increases diabetes risk by 52% |
| Threshold derived | WBC \> 6,900 cells/![][image2] |
| Limitations | Young, healthy male population only |

| Field | Content |
| :---- | :---- |
| Study name / first author | METS-IR / Zhang et al. 17 |
| Journal | PMC |
| Year | 2025 |
| DOI | 10.1186/s12933-024-02220-z |
| Design | Meta-analysis of cohort studies |
| Sample size | n=Unavailable (Multiple cohorts) |
| Follow-up | Various |
| Key finding | METS-IR inflection point at 40.56 for composite CVD risk acceleration |
| Threshold derived | METS-IR \> 40.56 |
| Limitations | Heterogeneity in individual cohort risk estimates |

### ---

**5\. Required Biomarkers**

**Required Biomarkers:**

* **hs\_crp** — Downstream marker of systemic inflammatory activity induced by IL-6 7; Fasting preferred; SSOT unit: mg/L.  
* **neutrophils\_abs** — Represents innate immune response and acute inflammatory stress 10; Fasting no; SSOT unit: ![][image3]/L.  
* **lymphocytes\_abs** — Reflects adaptive immune regulation and physiological stress (lymphopenia) 10; Fasting no; SSOT unit: ![][image3]/L.  
* **glucose** — Component of METS-IR formula; Fasting yes; SSOT unit: mmol/L.  
* **triglycerides** — Component of METS-IR formula; Fasting yes; SSOT unit: mmol/L.  
* **hdl\_cholesterol** — Component of METS-IR formula; Fasting yes; SSOT unit: mmol/L.  
* **wbc\_count** — Total white blood cell count for diabetes prediction 15; Fasting no; SSOT unit: ![][image3]/L.

**Optional Biomarkers:**

* **platelets** — Required for Systemic Immune-Inflammation Index (SII).14  
* **monocytes\_abs** — Required for Systemic Inflammatory Response Index (SIRI).  
* **hba1c** — To correlate inflammatory state with chronic glycemic control.

### ---

**6\. Derived Metrics and Formulas**

* **Metric name:** nlr  
* **Formula:** ![][image4]  
* **Unit handling:** Inputs must be in the same units (e.g., ![][image3]/L); result is a ratio.  
* **Evidence anchor:** Dong et al. 14, Leucuța et al..6  
* **Existing in platform?** Yes.  
* **Metric name:** mets\_ir  
* **Formula:** ![][image5]  
* **Unit handling:** FBG, TG, and HDL-C must be in mg/dL.  
  * Conversion from mmol/L: Glucose (mmol/L) ![][image6], TG (mmol/L) ![][image7], HDL (mmol/L) ![][image8].  
* **Evidence anchor:** Zhang et al..17  
* **Existing in platform?** No.  
* **Metric name:** sii  
* **Formula:** ![][image9]  
* **Unit handling:** Same cell count units for all inputs (![][image3]/L).  
* **Evidence anchor:**.  
* **Existing in platform?** No.

### ---

**7\. Evidence-Anchored Thresholds**

| Tier | Metric | Operator | Value | Unit | Evidence source | Study n | Follow-up |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| optimal | derived.nlr | \< | 2.0 | ratio |  | 202 / 13k | Cross-sec |
| suboptimal | derived.nlr |  | 2.0 – 3.0 | ratio |  | 202 / 13k | Cross-sec |
| at\_risk | derived.nlr | \> | 3.0 | ratio |  | 202 / 13k | Cross-sec |

| Tier | Metric | Operator | Value | Unit | Evidence source | Study n | Follow-up |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| optimal | hs\_crp | \< | 1.0 | mg/L | 8 | Meta | 20+ years |
| suboptimal | hs\_crp |  | 1.0 – 3.0 | mg/L | 13 | 94,841 | 13.1 yrs |
| at\_risk | hs\_crp | \> | 3.0 | mg/L | 13 | 94,841 | 13.1 yrs |

| Tier | Metric | Operator | Value | Unit | Evidence source | Study n | Follow-up |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| optimal | derived.mets\_ir | \< | 38.0 | index | 17 | Meta | Various |
| suboptimal | derived.mets\_ir |  | 38.0 – 40.5 | index | 17 | Meta | Various |
| at\_risk | derived.mets\_ir | \> | 40.5 | index | 17 | Meta | Various |

### ---

**8\. Override Rules and Guardrails**

* **Rule:** hs\_crp \> 10.0 mg/L ![][image10] at\_risk (Acute Phase Response)  
  * **Evidence basis:** Levels \>10 mg/L typically reflect acute infection or trauma, not chronic metaflammation.20  
* **Rule:** achieved LDL-C target AND hs\_crp ![][image11] 2.0 mg/L ![][image10] suboptimal (Residual Inflammatory Risk)  
  * **Evidence basis:** ESC/EAS 2025 focused update.9  
* **Rule:** wbc\_count \> 11.0 ![][image3]/L ![][image10] at\_risk  
  * **Evidence basis:** Standard clinical leukocytosis threshold.

### ---

**9\. Clinical Limitations and Excluded Populations**

1. **Excluded Populations:**  
   * Patients with acute infections (e.g., pneumonia, UTI) or recent major trauma/surgery.  
   * Pregnant individuals (WBC and NLR naturally trend higher).21  
   * Patients with primary hematologic malignancies (e.g., CML, CLL).21  
2. **Confounding Medications:**  
   * **Statins & Bempedoic Acid:** Directly lower hs-CRP independently of LDL-C, potentially masking residual risk.20  
   * **SGLT2 inhibitors & GLP-1 RAs:** Known to reduce NLR and hs-CRP.  
   * **Corticosteroids:** Induced neutrophilia and lymphopenia will artificially inflate NLR.  
3. **Evidence Gaps:** Actions of NLR thresholds in North American populations have shown smaller effects compared to Asian cohorts.5

### ---

**10\. HealthIQ Platform Signal Mapping**

**Signal identifier**:

signal\_metabolic\_inflammation

**Physiological system**:

inflammatory

**Primary metric**:

derived.nlr

**Required biomarkers**:

\- hs\_crp  
\- neutrophils\_abs  
\- lymphocytes\_abs  
\- glucose  
\- triglycerides  
\- hdl\_cholesterol  
\- wbc\_count

**Required derived metrics**:

\- derived.nlr  
\- derived.mets\_ir

**Optional biomarkers**:

\- platelets  
\- monocytes\_abs  
\- hba1c

**Optional derived metrics**:

\- derived.sii  
\- derived.siri

**Threshold summary**:

optimal:    derived.nlr \< 2.0 ratio  
suboptimal: derived.nlr 2.0 – 3.0 ratio  
at\_risk:    derived.nlr \> 3.0 ratio

**Override rules**:

rule: hs\_crp \> 10.0 mg/L → at\_risk (exclude from chronic assessment)  
evidence: \[20, 13\]  
rule: mets\_ir \> 40.5 index → at\_risk  
evidence: 

**Bundle consumers**:

\- metabolic\_health  
\- biological\_age  
\- biological\_age\_acceleration  
\- cardiovascular\_risk  
\- brain\_metabolic\_resilience

**Implementation notes**:

Implement derived.mets\_ir formula with internal conversions for mmol/L to mg/dL to ensure index validity. Flag hs\_crp values above 10.0 mg/L as "Acute Event" to prevent misclassification of chronic risk.

### ---

**11\. Supporting References**

* **Metabolic Syndrome, High-Sensitivity C-reactive Protein, and the Risk of Heart Failure: The Kailuan Cohort Study.** *ResearchGate/JAPI*. 2025..13 *Identified high-risk hs-CRP threshold of 3.0 mg/L for HF.*  
* **The Neutrophil–Lymphocyte Ratio as a Risk Factor for All-Cause and Cardiovascular Mortality in Diabetes Patients.** *PMC*. 2023\. DOI: 10.1186/s12933-023-01998-y.14 *Established NLR as a mortality predictor in diabetic cohorts.*  
* **Metabolic Score for Insulin Resistance (METS-IR) and Incident Cardiovascular Disease.** *PMC*. 2025\. DOI: 10.1186/s12933-024-02220-z.17 *Validated non-insulin index for CVD risk.*  
* **White Blood Cell Count and the Risk of Diabetes in Young Men.** *Diabetes Care (MELANY Study)*. 2013\. DOI: 10.2337/dc12-1143.15 *Linked WBC count within the normal range to incident diabetes.*  
* **2025 Focused Update of the 2019 ESC/EAS Guidelines for the Management of Dyslipidaemias.** *ESC*. 2025..9 *Universal screening of hs-CRP for risk modification.*

#### **Works cited**

1. Chronic tissue inflammation and metabolic disease \- PMC, accessed on March 9, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC7919414/](https://pmc.ncbi.nlm.nih.gov/articles/PMC7919414/)  
2. Inflammation and Insulin Resistance \- PMC \- NIH, accessed on March 9, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC2246086/](https://pmc.ncbi.nlm.nih.gov/articles/PMC2246086/)  
3. Metabolic and vascular insulin resistance: partners in the pathogenesis of cardiovascular disease in diabetes \- American Journal of Physiology, accessed on March 9, 2026, [https://journals.physiology.org/doi/10.1152/ajpheart.00826.2024](https://journals.physiology.org/doi/10.1152/ajpheart.00826.2024)  
4. Cardiology Triglycerides as Determinants of Global Lipoprotein-Derangement: Implications for Cardiovascular Prevention \- AWS, accessed on March 9, 2026, [https://journal-api.s3.ap-south-1.amazonaws.com/issues/articles/japi-74-1-52.pdf](https://journal-api.s3.ap-south-1.amazonaws.com/issues/articles/japi-74-1-52.pdf)  
5. Association Between Neutrophil‐to‐Lymphocyte Ratio and Glycemic ..., accessed on March 9, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC12862005/](https://pmc.ncbi.nlm.nih.gov/articles/PMC12862005/)  
6. Competing risks analysis for neutrophil to lymphocyte ratio as a predi \- Dove Medical Press, accessed on March 9, 2026, [https://www.dovepress.com/competing-risks-analysis-for-neutrophil-to-lymphocyte-ratio-as-a-predi-peer-reviewed-fulltext-article-DMSO](https://www.dovepress.com/competing-risks-analysis-for-neutrophil-to-lymphocyte-ratio-as-a-predi-peer-reviewed-fulltext-article-DMSO)  
7. Systemic Inflammatory Biomarkers (Interleukin-6, High-Sensitivity C-Reactive Protein, and Neutrophil-to-Lymphocyte Ratio) and Prognosis in Heart Failure: A Meta-Analysis of Prospective Cohort Studies \- MDPI, accessed on March 9, 2026, [https://www.mdpi.com/2077-0383/14/23/8610](https://www.mdpi.com/2077-0383/14/23/8610)  
8. Prioritizing Health | hsCRP: A Promising Risk Assessment Tool \- American College of Cardiology, accessed on March 9, 2026, [https://www.acc.org/latest-in-cardiology/articles/2025/12/01/01/prioritizing-health-hscrp](https://www.acc.org/latest-in-cardiology/articles/2025/12/01/01/prioritizing-health-hscrp)  
9. Molecular Pathways Mediating Immunosuppression in Response to Prolonged Intensive Physical Training, Low-Energy Availability, and Intensive Weight Loss \- Frontiers, accessed on March 9, 2026, [https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2019.00907/full](https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2019.00907/full)  
10. Competing Risks Analysis for Neutrophil to Lymphocyte Ratio as a Predictor of Diabetic Nephropathy Incidence \- PMC, accessed on March 9, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC12927795/](https://pmc.ncbi.nlm.nih.gov/articles/PMC12927795/)  
11. Inflammaging and 'Garb-aging' | Request PDF \- ResearchGate, accessed on March 9, 2026, [https://www.researchgate.net/publication/309454180\_Inflammaging\_and\_'Garb-aging'](https://www.researchgate.net/publication/309454180_Inflammaging_and_'Garb-aging')  
12. The Interaction between Metabolic Disease and Ageing \- Peertechz Publications, accessed on March 9, 2026, [https://www.clinsurggroup.us/Obesity-Diabetes-Metabolic-Syndrome/GJODMS-1-102.php](https://www.clinsurggroup.us/Obesity-Diabetes-Metabolic-Syndrome/GJODMS-1-102.php)  
13. (PDF) Metabolic syndrome, high-sensitivity C-reactive protein and ..., accessed on March 9, 2026, [https://www.researchgate.net/publication/391030135\_Metabolic\_syndrome\_high-sensitivity\_C-reactive\_protein\_and\_the\_risk\_of\_heart\_failure\_the\_Kailuan\_cohort\_study](https://www.researchgate.net/publication/391030135_Metabolic_syndrome_high-sensitivity_C-reactive_protein_and_the_risk_of_heart_failure_the_Kailuan_cohort_study)  
14. The neutrophil–lymphocyte ratio as a risk factor for all-cause and ..., accessed on March 9, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC10541705/](https://pmc.ncbi.nlm.nih.gov/articles/PMC10541705/)  
15. White Blood Cells Count and Incidence of Type 2 Diabetes in Young Men \- PMC, accessed on March 9, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC3554323/](https://pmc.ncbi.nlm.nih.gov/articles/PMC3554323/)  
16. PATHOLOGY HANDBOOK \- ICDST E-print archive of engineering and scientific PDF documents, accessed on March 9, 2026, [http://dl.icdst.org/pdfs/files/384c841708911ba763e1eeefe02269b2.pdf](http://dl.icdst.org/pdfs/files/384c841708911ba763e1eeefe02269b2.pdf)  
17. Metabolic score for insulin resistance and the incidence of ..., accessed on March 9, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC12575141/](https://pmc.ncbi.nlm.nih.gov/articles/PMC12575141/)  
18. (PDF) The 2024 American Diabetes Association guidelines on Standards of Medical Care in Diabetes: key takeaways for laboratory \- ResearchGate, accessed on March 9, 2026, [https://www.researchgate.net/publication/382507589\_The\_2024\_American\_Diabetes\_Association\_guidelines\_on\_Standards\_of\_Medical\_Care\_in\_Diabetes\_key\_takeaways\_for\_laboratory](https://www.researchgate.net/publication/382507589_The_2024_American_Diabetes_Association_guidelines_on_Standards_of_Medical_Care_in_Diabetes_key_takeaways_for_laboratory)  
19. Platelet and White Blood Cell Counts Are Elevated in Patients With the Metabolic Syndrome, accessed on March 9, 2026, [https://www.researchgate.net/publication/7438509\_Platelet\_and\_White\_Blood\_Cell\_Counts\_Are\_Elevated\_in\_Patients\_With\_the\_Metabolic\_Syndrome](https://www.researchgate.net/publication/7438509_Platelet_and_White_Blood_Cell_Counts_Are_Elevated_in_Patients_With_the_Metabolic_Syndrome)  
20. High-Sensitivity C-Reactive Protein and Residual Inflammatory Risk ..., accessed on March 9, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC12782873/](https://pmc.ncbi.nlm.nih.gov/articles/PMC12782873/)  
21. A Practical Guide to Lymphocytes | Learn With Superpower, accessed on March 9, 2026, [https://superpower.com/biomarker-guides/lymphocytes](https://superpower.com/biomarker-guides/lymphocytes)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAwAAAAaCAYAAACD+r1hAAAAz0lEQVR4Xu3RvwqBURjH8UdSlJKNTMrMYDCZWUxKyQ1YrJTVHXABsmJUZHIdMpisSpHFn+/xvIfjvQGG91ef5TnPc07nHJEg/5w4ov6iP2E0sMUeF0yRcnq+MsMRFYSQwwFr0ROHaNnmCG6o24Lo0Bh3VLFC1i62vULMFrz08EAfI9FNpIATip++d2qiA8ar2cQ0npG2BSd2YOkWM6KvknSLojt2RAcm/oUBym6RzEXvZU7foIm8XTSXNe9untbstkNJ9G+6uGKBhB0I8ts8AXIsJDG6DfHRAAAAAElFTkSuQmCC>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACUAAAAVCAYAAADB5CeuAAAB0UlEQVR4Xu1VPyjFURQ+QinyJyKxUJSFwUSSQWJgsBrYLCYGZbBZLMpAiUESgzLZDDIpK4tSb1AmizJI/nxf9x7v/M57z5v03vD76qvf/c595557/twnkqIoNsEdL5YSq+C4F0uNXrDBi+WCHi+UAyq8kMKAvXQNNntDo1u35tG4pl7pdEWdW7c5jaXhwaQtUwt4L2YvozyTMJLf0bgebbNROwI7o9YBZiR5WJcEH4fgJ3gHLkTbGvgFHoD1URsE3yS3f8bACX5MgnvgtoQAdsGquGk6ag9xTeitmAXFkoRLXUjYv2JsetlLo/WBL2Ct0RKYAkfBK/AZ7Da2ZQkOeahCHdYYbT7qGfAWbDK2fQmZ4uUVfCSpFQUP3zBrZuJRQlaYHYIZPAHfdZMDfcyZ9QD4KiGDegm2yw34pJv+Ah0ya4oR8AM8lmzt2Tt0RqfsMZZXwUMZAANRMED6ZV8phiRcipfrB4eNLQE2baHSLRqN39TYJyypLSsHoFDp7H+a9u4MuCXJsibAYNiItvE4TZwQToqCwTB7zOK5ZCeSoMYgLBhkRkLACk6oJuBUcp+RX/Dd8W8P36R8P2CZ2r0IVEvuiPM9sgOhoF87vSlS/Ct+ADwVVI0v+HX9AAAAAElFTkSuQmCC>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABsAAAAXCAYAAAD6FjQuAAABZUlEQVR4Xu2Tu0oEMRSGj3hBUPGGhYWFoIiCjbbWVquFWAg2doIvYCN2Ym8v4hsoKFgILtrpS+gDWFhoI17+35OsmTOT7CyMhbAffLDJyeyfOZOI/HPm4JGTv/+MSbgdjHfhVTCulBWnZw0+B+McHXAKdtqCoxtOwwU4ZGo2bBO+B+MGDGGPz+EjHM9UlZroTi/gsei6waA+I9k2HsCvYPzDPPyAb6LFJykO4y63RDdGxuCJ6NsSzl/DEdG35/f6dLUci/BVisNYu4S9Zp6b48nz8BN4+GbRA5IKY/9PzRzh+jrsd57BHjgKb+FqY6UhFcZjHAvz67vgoejGbuCO/LY8RyqMrWoWRmbhsmQPTiGpMAaVCStNKqxMG1siFRY7ILwud3DAFpqRClsSvUN9Zp5Hn3ctehBipML4wR/gsJln2IaZS8I/5kPWuujd8ezBF7gv2tZ7yV7iypmA66Jh7ESbNtXwDcIRVCP2elEkAAAAAElFTkSuQmCC>

[image4]: <data:image/png;base64,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>

[image5]: <data:image/png;base64,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>

[image6]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAE8AAAAWCAYAAACBtcG5AAADXElEQVR4Xu2XS6hOURTHl1BEiPIulEcikRCRRyYGJErEHJFEMVQkyQQDyiMkE24kDET6imIgUkQehRhQEkUhj///rrPcddY9Z58vfWbnV//ud9beZz/+e5+19xWpqampqflXhkB9YtDRD5oNjYG6h7IqekATod6xINAFGg11jQUZLB8IzYWGhzIP+5ku2ud/ZwD0HVocCzL6Q0+h41AD+iw6kSpowiboA3Qu+7tXis1nexehl6ILWcQt6D50JPu7IF/czj7oI/RadE7nocG5Gi2Ag6VpFHfcbyk2byb0KAbBdahXDAYeQ1dEd55xUHRytito5CDR3fIFeiXF5q2Uzju3DTrmntnmHsmPi2Pg3Da6WA5WLlpNg4P3E4hwUGXmMcbJRhrSeTIRtkmzPNuz+NoQJynz+B5N9pzKZHCscR5nslhcxL9shi5DfWNBRkOKjTFS5i0SLZvkYj2h/VL96fI9TtpjE/STNlLmbRHd7T7X8YtY554niC70FBdjP+yvIYnF5kS2QddcjB3ddM9lpMwjk0XLqV/QpXxxIVzllHmNECcp8wjL/Ti4iFXQzG/QnFgQMQO5A8245bkaxVSZx8T/VToGTlXlO2uzlebtFDXCxsC5ptIVy6xe1VfSDivdg+5Kc8aRlHlcXSbloaKn23PRujzxUgOnua00jyf+adHDbRX0SdLG2Ebamv1umhfQbdGTtBlS5rHzZ+6ZpvAQ+AnNc/EiWmVeN+iw5HM6rx9s5x00zsUNbhy217RxI6AH2W++xOOZp0wVZeZxEpxMNIC8keK4h236qwSx07bo3TLzpmZlkWmi6cSPm5ds3gdnuRgv90clYaQZ5z9VM7DsFDbKzON7d6ATIU5o3kL3fEj0ZPN9sU6b6M4xuGuZt3h/jJSZN0q0rch80frjXYzpaoloG6Yd0G5XJweN4ySXxQJRA7n7UgYOEzWPx37MY2ugH5JfNebBs5Kvy/fjAuwSNWRG9jxSNKVwMWI/bJ/9vBc93X1//M22/G4iN7K41eUcbRxRq7M6neA9b2kMOtZDK2JQOu5AUf4TsX+xeHLz7wHRPBMX4yH0BBrrYsyPNOqt6Ls8bK6KJn/DUkMcA+XvZVww5tkL0AbopHT+V8/yaRSvNf4rqampqampaY4/pyDc/0TvVbIAAAAASUVORK5CYII=>

[image7]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADsAAAAXCAYAAAC1Szf+AAADGUlEQVR4Xu2WWahOURTHlwwRZYwM5aZ4NGSKPHgQGTN7QIkiEkrxplvyjiLJkKQMieKWKX3lgfIgRcmQIZKErvBAhv//rrPvWWedfb7zFUo5//r1fWeddc7Za6+1194ilSpV+l/VFUwAPfwNo15gChgOOrt7RRoEOjpbd9DXXDeBzaCbsf0VcSCbwBtwCnwEh0QHZNUHPASHQU3Ub6V1KFANfALnwUFwD3wF84zPTPATfAcvwQtH/9T197QCXBMNhuLvdXC63UOzyImwGZoM3pvrItVEAwm0gjmgg/FZ53w8uSpiJnJGJ5aq1UDwHGx09rGiMxo0F3ww10HbpX7ZU8wo31ekTuAIGO/sQ8BNMNHZ27QFXAQ9/Y1EfJiDthoAnoiW1WpjZ/Ast6BQZiONjevrkmQzFFNZsEzAGtF+EMSkHQDbpOD9NPLmVckHzEBvOBvFZ3ZLWi4jwDTwFMwwflwzDJ4+e0VLvRncMj5FYrBsfLPBftHy9w3Laxk4KyUNywYcFAJdZGxWnJgzooH8AK8knonRkk4K/S5INhtFugKegR1gKHgLjku+AVo9AJO8MaYQMIMoCzSI5ckPhGDuiGbZitn4ItnGsS/jEddlyX5/leizOyVeorTVpLwXZMS1yAVu9zOvMaJbDsuG4of4nx2TAwraCh6Za2aF5UyfqcbeiIaB16LVwSXjxX6x0BvrieWyRPTBFsmv4SAO+Dbo7excY+y+nN1+4D7YlfFIK4gduUj0eQfWGlvYAThRvmGyWXG8bIgNiYHeTf7zY/UCPibxkuFzJxJ7GFwsKC6TmD2IzzMoNqkuiY394DP4Jnoas+L7eKiI9YycQqB2jdiAvZpFm8fgrLmt9Z9L/nOS2HWPprfbxWOjLUWu/fWSrkXuoWyWdsuiP0uY7/QJCBNRGiz32fneaMQBLPVG0c38sWj2WJZsTlyf7L5B4UjJZsffPaJr/aTxobjWOCl2y9ggmi1WEY+asRNUUJiIUf7GnxQzOQ4sT36LTmLTRX0WgyaJDzgmNskFos/6U5wVvztLGn9vpUqVKv0b+gWwFKDTFIDLjAAAAABJRU5ErkJggg==>

[image8]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADsAAAAXCAYAAAC1Szf+AAADFklEQVR4Xu2WS8hNURTHl1CECHkUeRRFXuUVKV95FKXkXTKQwRcJJY9k8EmGBpQYeAwMMDAQSlEuCpkpSh55pGSAUhTl8f9be7nrrrvvuZe+gXJ+9e+0195nn732XmvtI1JSUvK/0hsaCvWIHY5+0BxoDNQ99LUC556Qnp6R0FaoZ7B3Or2g49AL6Bb0HToD9XdjCNuPoRNQBfoIrfMDCuA3DkNfoQvQa2ia618E/YC+pb5XQYOqQ/+ebtDRJJ5UF2i/6IcvunHsOwd1dbbZ0HvXbkRf6Bp0ExoGTYGeJhs3gbSLfrOR6qKIL9YZAzF8BkIPRSfsSLYlqf0ptc32wbWNXaLhXwTnuSzVbw+BDkDzUpsbfhKantoGN+YONDPYf7ENuiS6kzn4MhcdYZ7ylOzUNos6e//3iGqYTXI25tcV0Wgogu/tiUYHN2GDaD0weGjHoJ3SYH4a2XlV6h2mo8zHZgyA7onmznJnZ848EF04c4/52wHddWNyMNr4znpoO/QcugGN94MyrIbOS5OC5R02zFG/+AhDqQ16KZpPc2t6Feaa5RCLGHPan0YORg3HX4d2i0YPiyFTYoYbF3kEzYrGHOYwT7cVR4k5y1Nj9dsh9bvKhX6W2sJxpGZEPeYsw93mGw29EY2KGIGE669I81pQwzPRBGdo/gncIJZ/LtJgCD5xbbtKOKbN2SODRcew2hp0opLsLHAR1oxl0VjECGil6IushLkdJNztBdBEZ/OLoVNWsVlBPRZBuQUblrN+8UXOslhxvSyILUFHrZJyQUUOHxT96DtoXLL1EQ192u2virkcF0YYBTm7Jzrlr7u1zk4sqqYGexZz1OeodzjCYhGdjWHMTWJ+nUptD38b57s2r6aNUntdfBENecPmp0Y5O6GTvJebOst7dmk0OriAVRnbJtHCwzv6tOi1c1v0f9VgcdoieuJ8HoLeQmfdGMJw5ab44safCP4tMTr2iX5rr+R/gLhxrPSTY0dnwtxaCK2BxkqDi1x0DENvhehmNBoX4WbxtPju8NDn4QYsltbnLSkpKfk3+Al3G6QmXpW2twAAAABJRU5ErkJggg==>

[image9]: <data:image/png;base64,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>

[image10]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABMAAAAYCAYAAAAYl8YPAAAAfUlEQVR4XmNgGAWjYHACWSDuBmIOdAlyQTkUUwWIAfF+IDZDlyAXgAw6AsQq6BI8QCxJBg4G4kdAzMmABCqggqTiZ0D8H4jjGSgE3EC8EIj70CVIBa5AvJoBzXvkABYGiIs80CXIAdJAvBmIRdAlyAGsQCwExIzoEqNggAEAkekYp+CjMnEAAAAASUVORK5CYII=>

[image11]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA8AAAAXCAYAAADUUxW8AAAAl0lEQVR4XmNgGAVkAWEgzkMXJBYwA7E/EK8DYnU0OZIAIxCbA/FxID7DADGYZAAyRA+IbwFxBBCzokoTB0DeAHnnGRAnATEnqjRxQBGI5zNADCHZFXxAXAPETxiI1AyyjWTnwvx5iYFIW0AAFLq7GCBR5MRAZDTB4vYIlAbxhzsA5ardQPyISMwD0QYBoAACGSBJJB5gAAAF/hsoBl8+3gAAAABJRU5ErkJggg==>