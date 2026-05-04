# Insulin Resistance Risk Detection Bundle

**Executive summary (what this bundle does and why you’d trust it).**  
This bundle detects an *insulin-resistance phenotype* early—often **before** someone crosses guideline thresholds for prediabetes or type 2 diabetes—using a deterministic index (the **Triglyceride–Glucose index, TyG**) computed from a standard fasting lipid panel + fasting glucose. In a White European prospective cohort (**n=4,820**, mean follow-up **8.84 years**), incident type 2 diabetes risk rose progressively at **TyG ≥8.31**, and TyG discriminated future diabetes better than fasting glucose alone in those starting with “normal fasting glucose” (AUC **0.75** vs **0.66**). citeturn12view1 A Tier 1 meta-analysis of **13 cohort studies (n=70,380)** found higher TyG associated with incident type 2 diabetes (pooled overall HR **2.44**; RR **3.12**), though with **high heterogeneity**, so *one universal cut-off is not defensible across all populations*. citeturn12view0  
Because major guidelines (e.g., the **American Diabetes Association Standards of Care 2026**) diagnose and risk-stratify dysglycaemia using **HbA1c, fasting plasma glucose, and/or OGTT** (not TyG), this bundle uses those guideline criteria as **hard “guardrails”**: if prediabetes/diabetes thresholds are met, the user is tiered “At risk” and directed to medical follow-up regardless of TyG. citeturn3view2turn4view1 For actions, the bundle prioritises interventions with outcome evidence: the **Diabetes Prevention Program** lifestyle intervention reduced diabetes incidence **58%** (vs placebo) and metformin **31%** over 2.8 years (n=3,234). citeturn8view1 For obese people with prediabetes, physician-guided pharmacotherapy can meaningfully reduce progression risk (e.g., liraglutide 3.0 mg HR **0.21** for time-to-diabetes over 160 weeks in a large RCT). citeturn11view0  
**Assumption (explicit):** you stated two attached internal documents exist but are **not accessible** for this task; I therefore rely only on public clinical guidelines and peer‑reviewed literature.  

---

## 1. BUNDLE NAME
**Insulin Resistance Risk Detection (TyG + Glycaemic Guardrails)** citeturn12view1turn3view2

---

## 2. BIOLOGICAL QUESTION
“Do my fasting blood results suggest I’m developing insulin resistance and higher risk of prediabetes/type 2 diabetes—even if my glucose tests still look ‘normal’?” citeturn12view1turn12view0

---

## 3. CLINICAL RATIONALE

**What disease/dysfunction does it predict?**  
This bundle predicts *early metabolic dysfunction consistent with insulin resistance* that is associated with higher risk of **incident type 2 diabetes**, **metabolic syndrome**, and (in validated cohorts) higher risk of **future cardiovascular events**. citeturn12view1turn12view0turn14view1turn16view0

**What’s the pathophysiological mechanism?**  
Insulin resistance is a state where tissues (especially liver, muscle, adipose) respond less effectively to insulin. A common early clinical pattern includes relatively higher fasting glucose (even within “normal”) plus higher triglycerides, reflecting hepatic insulin resistance and dysregulated lipid handling. TyG uses fasting **triglycerides × glucose** as a composite signal that correlates with clamp‑measured insulin sensitivity in mechanistic validation work (note: this clamp validation is cross-sectional and not Tier 1 outcomes evidence). citeturn14view0turn12view1

**At what stage does this provide early warning?**  
Tier 1/2 longitudinal evidence shows TyG can predict future diabetes *even among people who start normoglycaemic*. In the Vascular‑Metabolic CUN cohort, among those with baseline fasting glucose <100 mg/dL, the highest TyG quartile had HR **6.87** for incident diabetes vs the lowest quartile. citeturn12view1 This is the “early warning” use case: identifying risk gradients before overt dysglycaemia appears.

**Why does this matter for health outcomes?**  
Prediabetes itself (the clinically recognised intermediate state) is associated with increased risks of **all-cause mortality** and **cardiovascular disease** in large meta-analytic evidence—so preventing or delaying progression is not cosmetic; it affects morbidity and mortality. citeturn6search6 Importantly, highly effective preventive interventions exist (e.g., DPP-class lifestyle programmes), and the benefit is largest when intervention starts before long-standing dysglycaemia. citeturn8view1turn10view0

---

## 4. EVIDENCE BASE

### Primary Research (Tier 1 priority)

**Navarro‑González et al., Preventive Medicine, 2016, doi:10.1016/j.ypmed.2016.01.022**  
APA: Navarro‑González, D., Sánchez‑Íñigo, L., Pastrana‑Delgado, J., Fernández‑Montero, A., & Martínez, J. A. (2016). Triglyceride‑glucose index (TyG index) in comparison with fasting plasma glucose improved diabetes prediction in patients with normal fasting glucose: The Vascular‑Metabolic CUN cohort. *Preventive Medicine, 86*, 99–105. https://doi.org/10.1016/j.ypmed.2016.01.022 citeturn12view1  
Cohort size / follow-up: **n=4,820**, mean follow-up **8.84±4.39 years**; **332** incident diabetes cases. citeturn12view1  
Key finding: Diabetes risk rose progressively at **TyG ≥8.31**; in baseline normoglycaemia (<100 mg/dL), Q4 vs Q1 HR **6.87** (95% CI 2.76–16.85). citeturn12view1  
Predictive metrics: In normoglycaemia, AUC TyG **0.75** vs fasting glucose **0.66** and triglycerides **0.71** (p=0.017). citeturn12view1

**da Silva et al., Primary Care Diabetes, 2020, doi:10.1016/j.pcd.2020.09.001 (Systematic review/meta-analysis)**  
APA: da Silva, A., Caldas, A. P. S., Rocha, D. M. U. P., & Bressan, J. (2020). Triglyceride‑glucose index predicts independently type 2 diabetes mellitus risk: A systematic review and meta-analysis of cohort studies. *Primary Care Diabetes, 14*(6), 584–593. https://doi.org/10.1016/j.pcd.2020.09.001 citeturn12view0  
Cohort size: **13 cohort studies**, total **n=70,380**. citeturn12view0  
Key finding: Higher TyG associated with incident T2D (overall HR **2.44**, 95% CI 2.17–2.76; RR **3.12**, 95% CI 2.31–4.21). citeturn12view0  
Critical nuance (must not be hand-waved): **High heterogeneity** was present; therefore, “one global TyG cut-off” is not Tier 1 defensible for all populations. citeturn12view0

**Son et al., Nutr Metab Cardiovasc Dis, 2022, doi:10.1016/j.numecd.2021.11.017**  
APA: Son, D.‑H., Lee, H.‑S., Lee, Y.‑J., & Han, J.‑H. (2022). Comparison of triglyceride‑glucose index and HOMA‑IR for predicting prevalence and incidence of metabolic syndrome. *Nutrition, Metabolism and Cardiovascular Diseases, 32*(3), 596–604. https://doi.org/10.1016/j.numecd.2021.11.017 citeturn14view1  
Cohort size / follow-up: Baseline analysed **n=9,730**; incident analysis **n=6,091**; follow-up **12 years**. citeturn14view1  
Key finding: TyG outperformed HOMA‑IR for incident metabolic syndrome (AUROC **0.654** vs **0.556**, p<0.001). citeturn14view1  
Cut-offs reported: TyG cut-off for **incident metabolic syndrome** **8.518** (population-specific, but provides an evidence anchor near 8.52). citeturn14view1

**Sánchez‑Íñigo et al., Eur J Clin Invest, 2016, doi:10.1111/eci.12583**  
APA: Sánchez‑Íñigo, L., Navarro‑González, D., Fernández‑Montero, A., Pastrana‑Delgado, J., & Martínez, J. A. (2016). The TyG index may predict the development of cardiovascular events. *European Journal of Clinical Investigation, 46*(2), 189–197. https://doi.org/10.1111/eci.12583 citeturn16view0  
Cohort size / follow-up: **n=5,014**, median follow-up **10 years**. citeturn16view0  
Key finding: Highest TyG quintile HR **2.32** (95% CI 1.65–3.26) for incident CVD; adding TyG to Framingham variables increased AUC from **0.708** to **0.719** (p=0.014). citeturn16view0

### Supporting Research (Tier 2 acceptable, plus mechanistic context)

**Guerrero‑Romero et al., J Clin Endocrinol Metab, 2010, doi:10.1210/jc.2010-0288**  
APA: Guerrero‑Romero, F., Simental‑Mendía, L. E., González‑Ortiz, M., et al. (2010). The product of triglycerides and glucose, a simple measure of insulin sensitivity. Comparison with the euglycemic‑hyperinsulinemic clamp. *The Journal of Clinical Endocrinology & Metabolism, 95*(7), 3347–3351. https://doi.org/10.1210/jc.2010-0288 citeturn14view0  
Why it’s here: It validates TyG against the clamp (correlation r≈−0.681; AUC ≈0.858), but it is **cross-sectional and small**, so it is **not** used to justify population risk cut-offs (Tier 1 requirement not met for that use). citeturn14view0

**Cai et al., BMJ, 2020, doi:10.1136/bmj.m2297 (Prediabetes outcomes meta-analysis)**  
APA: Cai, X., Zhang, Y., Li, M., et al. (2020). Association between prediabetes and risk of all cause mortality and cardiovascular disease: Updated meta-analysis. *BMJ, 370*, m2297. https://doi.org/10.1136/bmj.m2297 citeturn6search6  
Why it’s here: It quantifies why “early metabolic dysfunction” matters—prediabetes is not benign. citeturn6search6

### Clinical Guidelines (Tier 1, major bodies)

**entity["organization","American Diabetes Association","diabetes society"] Standards of Care in Diabetes—2026 (diagnosis/prediabetes criteria and screening approach).**  
Prediabetes and diabetes thresholds (HbA1c, FPG, OGTT) and requirement for confirmatory testing when hyperglycaemia is not unequivocal are explicitly stated in ADA 2026. citeturn3view2turn4view1

**entity["organization","U.S. Preventive Services Task Force","guideline body"] 2021 recommendation: screening for prediabetes and type 2 diabetes in adults 35–70 with overweight/obesity, and offering effective preventive interventions for prediabetes.** citeturn0search6turn0search2

**entity["organization","National Institute for Health and Care Excellence","health guideline body uk"] NICE PH38 (Type 2 diabetes: prevention in people at high risk).**  
NICE defines a “high risk” confirmation blood test range including fasting plasma glucose **5.5–6.9 mmol/L** or HbA1c **42–47 mmol/mol (6.0–6.4%)**, and recommends at least annual testing in people confirmed high-risk. citeturn0search3turn0search7

**Metabolic syndrome harmonised criteria (joint interim statement; triglycerides ≥1.7 mmol/L is one criterion).**  
APA: Alberti, K. G. M. M., Eckel, R. H., Grundy, S. M., et al. (2009). Harmonizing the metabolic syndrome: A joint interim statement… *Circulation, 120*(16), 1640–1645. https://doi.org/10.1161/CIRCULATIONAHA.109.192644 citeturn1search2

**Explicit Tier 1 gap (must be stated):** No major guideline (ADA 2026, NICE PH38, USPSTF 2021) currently recommends **TyG** as a diagnostic test for insulin resistance or as a primary screening test; they base screening/diagnosis on **A1c/FPG/OGTT**. This bundle therefore positions TyG as a *risk signal* and uses guideline thresholds as safety guardrails. citeturn3view2turn0search3turn0search6

---

## 5. REQUIRED BIOMARKERS

### Minimum required markers (must be present to compute the core signal)

- **Fasting plasma glucose (FPG)** — required for TyG computation and for ADA glycaemic guardrails (prediabetes/diabetes thresholding). citeturn12view1turn3view2turn4view1  
- **Fasting triglycerides (TG)** — required for TyG computation; also a metabolic syndrome component (pathophysiologic context and risk clustering). citeturn12view1turn1search2  

### Optional markers (enhance safety, interpretability, and/or cross-validation)

- **HbA1c** — strengthens guardrails and reduces misclassification when fasting status is imperfect; ADA defines prediabetes at HbA1c **5.7–6.4% (39–47 mmol/mol)**. citeturn3view2turn4view1  
- **Fasting insulin** — enables HOMA‑IR computation, but insulin assays vary and thresholds are not harmonised in guidelines; treat as “supporting evidence,” not the primary tier gate. citeturn13search2turn14view1  
- **HDL‑cholesterol** — helps recognise atherogenic dyslipidaemia/metabolic syndrome patterns (low HDL + high TG). citeturn1search2  
- **Waist circumference, blood pressure** — non-lab measures but clinically meaningful to identify metabolic syndrome clustering and escalation needs. citeturn1search2  

### Table 1 — Required vs optional biomarkers (with rationale and units)

| Biomarker (canonical) | Fasting? | SI unit (UK) | Common US unit | Why it’s needed | Evidence anchor |
|---|---:|---|---|---|---|
| Fasting plasma glucose (glucose) | Yes (≥8h) | mmol/L | mg/dL | Core TyG input; diagnostic/guardrail thresholds for prediabetes/diabetes | TyG cohort formula + diabetes/prediabetes criteria citeturn12view1turn4view1turn3view2 |
| Triglycerides (triglycerides) | Yes (≥8h) | mmol/L | mg/dL | Core TyG input; part of metabolic syndrome phenotype | TyG formula; metabolic syndrome harmonised criteria citeturn12view1turn1search2 |
| HbA1c (hba1c) | No | mmol/mol | % | Strong guardrail; catches chronic dysglycaemia even with “normal” fasting glucose | ADA 2026 thresholds citeturn3view2turn4view1 |
| Fasting insulin (insulin) | Yes (≥8h) | pmol/L or mIU/L (lab dependent) | µU/mL (mIU/L) | Optional HOMA‑IR (context only; not primary tier gate) | HOMA model origin; cohort comparison vs TyG citeturn13search2turn14view1 |
| HDL‑cholesterol (hdl_cholesterol) | Prefer fasting | mmol/L | mg/dL | MetS/atherogenic dyslipidaemia context and cross-check | MetS harmonised criteria citeturn1search2 |

### Missing-data handling (explicit and deterministic)

- **If TG is missing:** TyG cannot be computed → output **“insufficient data for TyG”**; fall back to ADA glycaemic guardrails using FPG ± HbA1c to determine whether immediate clinical follow-up is needed. citeturn4view1turn3view2  
- **If FPG is missing (but TG present):** TyG cannot be computed → output **“insufficient data for TyG.”**  
- **If HbA1c is missing:** guardrails still operate using FPG thresholds, but confidence drops because HbA1c can identify risk not captured by one fasting sample (this is a design assumption; guidelines permit screening with FPG or A1c). citeturn3view2turn4view1  
- **If fasting status is uncertain:** compute TyG only if the sample is reported as fasting; otherwise output **“non-fasting—TyG not valid”** (design choice to avoid false positives). citeturn4view1  

---

## 6. CALCULATION METHOD

### Core published algorithm: TyG index (primary signal)

**TyG formula (canonical):**  
`TyG = ln( [TG(mg/dL) × FPG(mg/dL)] / 2 )` citeturn12view1

**Unit conversions (explicit, deterministic):**  
Because UK labs often report SI units, convert to mg/dL before applying the validated TyG formula:

- **Glucose:** `mg/dL = mmol/L × 18.018` (equivalently, `mmol/L = mg/dL × 0.0555`). citeturn22search3  
- **Triglycerides:** `mg/dL = mmol/L × 88.57` (equivalently, `mmol/L = mg/dL × 0.01129`). citeturn22search2  

### Guardrail logic (guideline-aligned; overrides TyG tiering)

From ADA 2026 criteria: citeturn4view1turn3view2  
- **Diabetes:** HbA1c ≥ **6.5% (≥48 mmol/mol)** OR FPG ≥ **7.0 mmol/L (≥126 mg/dL)** OR 2‑h OGTT ≥ **11.1 mmol/L (≥200 mg/dL)** OR random glucose ≥ **11.1 mmol/L (≥200 mg/dL)** with classic symptoms. citeturn4view1turn4view3  
- **Prediabetes:** HbA1c **5.7–6.4% (39–47 mmol/mol)** OR FPG **5.6–6.9 mmol/L (100–125 mg/dL)** OR 2‑h OGTT **7.8–11.0 mmol/L (140–199 mg/dL)**. citeturn3view2  

### Optional supportive derived metric: HOMA‑IR (not the primary tier gate)

If fasting insulin is available, compute:  
`HOMA‑IR = (Fasting insulin [µU/mL] × FPG [mmol/L]) / 22.5`  
HOMA-IR originates from the homeostasis model assessment framework. citeturn13search2turn13search6  
**Important limitation:** HOMA‑IR cut-offs are not universally standardised in major screening guidelines; if used, it should adjust *confidence/narrative*, not determine escalation alone (design choice to avoid over-medicalising assay variability). citeturn14view1  

### Mermaid decision logic flowchart (TyG → tier → actions)

```mermaid
flowchart TD
  A[Start: fasting labs available?] --> B{Fasting confirmed?}
  B -- No --> Z[Stop: non-fasting -> "TyG not valid" + use HbA1c/FPG guardrails only]
  B -- Yes --> C{Have FPG and TG?}
  C -- No --> Y[Stop: "insufficient data for TyG" + use HbA1c/FPG guardrails only]
  C -- Yes --> D[Convert units to mg/dL and calculate TyG]
  D --> E{Diabetes-range guardrail met?}
  E -- Yes --> R1[At risk (urgent): diabetes-range -> prompt clinical confirmation/management]
  E -- No --> F{Prediabetes-range guardrail met?}
  F -- Yes --> R2[At risk: prediabetes -> intensive prevention + clinician follow-up]
  F -- No --> G{TyG tier}
  G -- "< 8.31" --> T1[Optimal: maintenance + routine monitoring]
  G -- "8.31 to 8.51" --> T2[Suboptimal: intensive lifestyle + retest 8-12 weeks]
  G -- ">= 8.52" --> T3[At risk: treat as high cardiometabolic-risk phenotype + clinician review]
```

---

## 7. OUTPUT TIERS

**Design principle (non-negotiable):** Tiering is based on TyG *only when* dysglycaemia guardrails are negative. If prediabetes/diabetes criteria are met, the user is “At risk” regardless of TyG. citeturn3view2turn4view1

### OPTIMAL range

**Biomarker values (SI units + mg/dL conversions):**  
- Guardrails: HbA1c **<5.7% (<39 mmol/mol)** (if available) AND FPG **<5.6 mmol/L (<100 mg/dL)**. citeturn3view2turn4view1  
- TyG: **< 8.31**. citeturn12view1  

**What this means for the user:**  
Your fasting glucose–triglyceride pattern does not match the higher-risk TyG strata associated with markedly increased incident diabetes risk in the key prospective evidence. This is reassuring, not a lifetime guarantee—risk still changes with weight, ageing, medications, and sleep/activity patterns. citeturn12view1turn12view0

**Prevalence in population:**  
There is no single Tier 1 estimate of population prevalence for *these exact cut-offs* across ancestries and ages; TyG distributions vary, and the meta-analysis shows heterogeneity. Treat prevalence statements as approximate and cohort-dependent. citeturn12view0

### SUBOPTIMAL range

**Biomarker values:**  
- Guardrails negative: HbA1c <5.7% and FPG <5.6 mmol/L (or at least not in prediabetes range). citeturn3view2  
- TyG: **8.31 to 8.51** (anchored at 8.31 diabetes-risk inflection in the CUN cohort; upper bound set just below the incident metabolic syndrome cut-off ~8.518). citeturn12view1turn14view1  

**What this means for the user:**  
You appear to be drifting toward a higher insulin-resistance risk phenotype *before* guideline-defined prediabetes. This tier is designed to be a “course-correct now” signal: still highly modifiable, but no longer “low concern.” citeturn12view1turn12view0

**Risk implications:**  
Across cohorts, higher TyG is associated with substantially higher incident diabetes risk (pooled HR >2 in meta-analysis). However, because study methods differ, this tier does **not** claim a precise absolute risk percentage for an individual. citeturn12view0

### AT RISK range

**Biomarker values (any trigger places user here):**  
- **Prediabetes criteria met** (guardrail override): HbA1c **5.7–6.4% (39–47 mmol/mol)** OR FPG **5.6–6.9 mmol/L (100–125 mg/dL)** OR OGTT 2‑h glucose **7.8–11.0 mmol/L (140–199 mg/dL)**. citeturn3view2  
**OR**  
- Guardrails negative but TyG **≥ 8.52** (evidence anchor: incident metabolic syndrome TyG cut-off **8.518**; rounded to ≥8.52 for deterministic implementation). citeturn14view1  
**OR**  
- **Diabetes-range criteria** (urgent escalation): HbA1c ≥6.5% (≥48 mmol/mol) or FPG ≥7.0 mmol/L (≥126 mg/dL), etc. citeturn4view1turn4view3

**What this means for the user:**  
Your results suggest a high-risk cardiometabolic state. If you meet prediabetes criteria, you are already in a guideline-recognised category where intensive preventive interventions and clinician follow-up are recommended. citeturn3view2turn10view0

**Urgency level:**  
- **High urgency:** any diabetes-range value or classic symptoms with high random glucose → prompt medical confirmation/management. citeturn4view3turn4view1  
- **Moderate urgency:** TyG ≥8.52 without prediabetes → treat as high-risk phenotype; intervene now, retest after a defined interval, and consider clinician review, especially if other risk factors cluster. citeturn14view1turn16view0  

### Table 2 — Tier cutoffs and action summary

| Tier | Core numeric cutoffs | Evidence anchors | Default action intensity |
|---|---|---|---|
| Optimal | TyG <8.31 AND no prediabetes/diabetes guardrails | CUN cohort diabetes risk inflection; ADA thresholds citeturn12view1turn3view2 | Maintain lifestyle; routine monitoring |
| Suboptimal | TyG 8.31–8.51 AND guardrails negative | CUN cohort threshold; incident MetS cut-off anchor citeturn12view1turn14view1 | Intensive lifestyle; retest 8–12 weeks |
| At risk | Any prediabetes/diabetes guardrail OR TyG ≥8.52 | ADA criteria; Korean cohort cut-off for incident MetS citeturn3view2turn14view1 | Medical follow-up + structured prevention; consider meds if appropriate |

---

## 8. ACTIONABLE RECOMMENDATIONS

### OPTIMAL tier (maintenance)

1) **Maintain a “DPP-dose” activity baseline (≥150 min/week moderate activity).**  
Evidence: In DPP, lifestyle intervention targeting ≥150 min/week activity plus weight loss reduced diabetes incidence by **58%** vs placebo. citeturn8view1  
Action (specific): Keep ≥150 min/week moderate aerobic activity plus 2 resistance sessions/week (clinical practice standard; resistance training improves metabolic health but the strongest quantified outcomes here come from DPP-style programmes). citeturn8view1  

2) **Adopt/maintain a Mediterranean dietary pattern with concrete components (olive oil or nuts).**  
Evidence: In the PREDIMED-Reus RCT, Mediterranean diet + olive oil HR **0.49** and + nuts HR **0.48** for incident diabetes vs low-fat advice over median 4.0 years. citeturn7view1  
Action: Use olive oil as primary added fat; include ~30 g/day mixed nuts; prioritise legumes/vegetables; minimise refined grains and sugary drinks. citeturn7view1  

3) **Avoid weight gain; if overweight, aim for modest loss rather than “fine, I’m normal.”**  
Evidence: DPP shows structured lifestyle change substantially reduces incident diabetes; the mechanism is strongly weight-mediated even though this tier is not prediabetes. citeturn8view1  
Action: If BMI is above healthy range, set a modest target (e.g., 3–5% loss) and track waist circumference; this is pragmatic and aligns with prevention programming. citeturn10view0  

4) **Monitoring cadence (low friction, guideline-consistent):**  
If results are normal, ADA suggests repeat screening at least every **3 years** (more often if risk increases). citeturn3view2turn4view1  
Action: Repeat fasting glucose + TG annually if weight/lifestyle risk increases; otherwise 1–3 yearly is reasonable.

**Referral triggers (Optimal):**  
If fasting glucose rises into **≥5.6 mmol/L** or HbA1c reaches **≥39 mmol/mol**, move to clinician-led prevention pathways. citeturn3view2

---

### SUBOPTIMAL tier (intensive lifestyle with rapid feedback loop)

1) **Structured weight-loss target if overweight: 5–7% within 6–12 months.**  
Evidence: DPP lifestyle intervention (7% weight loss goal) reduced diabetes incidence by **58%** (95% CI 48–66) vs placebo. citeturn8view1  
Action: Set a 12-week “implementation block” (food logging + step target + weekly weigh-ins) aimed at measurable loss, not vague improvement.

2) **Join a formal diabetes prevention programme or dietitian-led programme (not DIY).**  
Evidence: ADA 2026 highlights CDC‑recognised DPP-style programmes and reports that registered dietitian nutritionist counselling can help people with prediabetes achieve **7–10% weight loss**. citeturn10view0  
Action: Enrol in a structured programme if available; if not, replicate the DPP structure (weekly accountability, explicit weight/activity targets). citeturn8view1turn10view0  

3) **Diet: Mediterranean diet with compliance features (olive oil/nuts) or equivalent whole-food pattern.**  
Evidence: PREDIMED-Reus showed ~**52%** relative reduction when Mediterranean arms pooled vs control advice. citeturn7view1  
Action: Keep the diet “ad libitum but structured” (Mediterranean pattern, minimise ultra‑processed foods); don’t rely on calorie restriction alone.

4) **Activity: escalate to ≥150–300 min/week moderate (or equivalent), plus resistance training.**  
Evidence: DPP used ≥150 min/week and achieved large risk reduction; a prospective-study meta-analysis also supports lower diabetes risk with higher activity levels (directionally consistent). citeturn8view1turn6search1  
Action: Add a daily step target plus 2–3 resistance sessions/week.

5) **Retest timeline (explicit assumption): repeat fasting glucose + TG (and HbA1c if available) after 8–12 weeks.**  
Rationale: This is a pragmatic feedback interval used in preventive metabolic programmes; guidelines specify annual testing for prediabetes, but do not specify TyG retesting intervals for normoglycaemia—so this is a **design assumption** for behavioural reinforcement rather than a guideline mandate. citeturn3view2turn0search3  

**Medical referral criteria (Suboptimal):**  
Refer to primary care if any of the following occur:  
- FPG enters prediabetes range (**≥5.6 mmol/L**) or HbA1c reaches **≥39 mmol/mol**, or  
- TyG remains ≥8.31 after a structured 8–12 week intervention, especially if other cardiometabolic factors cluster (BP, HDL, waist). citeturn3view2turn14view1turn1search2  

---

### AT RISK tier (medical follow-up + high-intensity prevention)

1) **Confirm and classify glycaemic status with guideline-based testing.**  
Evidence: ADA 2026 requires confirmatory testing for diagnosis in the absence of unequivocal hyperglycaemia, and defines diabetes/prediabetes thresholds. citeturn4view1turn3view2  
Action: Repeat HbA1c and/or FPG; consider OGTT if discordant or if clinical suspicion is high.

2) **DPP-class intensive lifestyle intervention (treat this as treatment, not “wellness”).**  
Evidence: DPP: lifestyle reduced diabetes incidence by **58%** (NNT ~6.9 over 3 years). citeturn8view1  
Action: Aim for ≥7% weight loss and ≥150 min/week activity, with weekly accountability. citeturn8view1  

3) **Consider metformin for diabetes prevention when clinician agrees (especially higher-risk subgroups).**  
Evidence: DPP metformin reduced diabetes incidence by **31%** vs placebo. citeturn8view1  
Guideline alignment: ADA 2026 states metformin has the most robust efficacy/safety data for prevention among people with prediabetes and should be recommended as an option for high-risk individuals (e.g., younger, history of gestational diabetes, BMI ≥35). citeturn10view0  
Action: Discuss with GP/endocrinology; do not self-initiate.

4) **For obesity + prediabetes: consider physician-guided anti-obesity pharmacotherapy with outcomes evidence (example: liraglutide 3.0 mg).**  
Evidence: In the SCALE Obesity and Prediabetes RCT (n=2,254), liraglutide 3.0 mg reduced time-to-diabetes with HR **0.21** (95% CI 0.13–0.34) over 160 weeks; diabetes occurred in 2% vs 6% on-treatment (liraglutide vs placebo). citeturn11view0  
Action: This is specialist/GP-led; evaluate contraindications and side effects; combine with lifestyle.

5) **Treat global cardiometabolic risk, not just glucose.**  
Evidence: Prediabetes is associated with increased risk of CVD and mortality in meta-analysis; TyG is also associated with incident cardiovascular events in cohort evidence. citeturn6search6turn16view0  
Action: Clinician assessment of BP, lipids, smoking, and weight distribution; escalate risk-factor treatment per standard cardiovascular prevention pathways.

**Medical referral triggers (At risk):**  
- **Urgent (same day / prompt):** diabetes-range values (HbA1c ≥48 mmol/mol or FPG ≥7.0 mmol/L) or classic hyperglycaemic symptoms with random plasma glucose ≥11.1 mmol/L. citeturn4view1turn4view3  
- **Within weeks:** prediabetes-range HbA1c/FPG or persistent TyG ≥8.52, especially with hypertension/dyslipidaemia/central obesity. citeturn3view2turn14view1turn1search2  

---

## 9. COMPETITIVE ANALYSIS

### InsideTracker: what they provide, evidence quality, and gaps

**Approach (as publicly described):**  
InsideTracker states they test **fasting blood glucose, fasting insulin, and HbA1c** to provide a “rigorous view” of blood sugar. citeturn19search10 They publish educational content on fasting insulin and include insulin in at least some plans. citeturn19search1turn19search3 They also acknowledge that **HOMA‑IR is primarily a research tool** and lacks defined diagnostic thresholds. citeturn5search0  

**Evidence quality (as delivered in product experience):**  
They provide lifestyle recommendations and “optimal zones,” but their public materials do not present an externally validated, outcome-based insulin resistance *risk algorithm* with disclosed calibration/AUC for incident diabetes, nor a reproducible formula-based tiering method (at least in the cited pages). citeturn19search14turn5search0  

**Gaps:**  
- No explicit, reproducible TyG-based pathway despite strong cohort evidence for prediction of incident diabetes and CVD. citeturn12view1turn16view0  
- Reliance on fasting insulin can be limited by availability and assay variability; their own content highlights uncertainty around HOMA-IR thresholds. citeturn5search0  

### Function Health: what they provide, evidence quality, and gaps

**Approach (as publicly described):**  
Function Health publishes education framing insulin sensitivity around fasting glucose, HbA1c, and insulin. citeturn19search5 They market internal “Function Index” statistics (e.g., “>65% outside optimal fasting insulin range”), but these appear to be internal observational summaries, not peer-reviewed model validation. citeturn19search2 They advise fasting (8 hours) for testing, consistent with the need for accurate fasting markers. citeturn19search15  

**Gaps:**  
- Public-facing materials do not specify a published, externally validated computation (formula + cut-offs) that maps to incident diabetes outcomes with known AUC/calibration. citeturn19search5turn19search2  
- Heavy emphasis on fasting insulin may increase false reassurance/false alarm risk without standardised thresholds and without transparent validation. (No Tier 1 guideline standardises insulin thresholds for screening in the same way as HbA1c/FPG.) citeturn3view2turn5search0  

### Table 3 — Competitor feature comparison (publicly evident)

| Feature | This bundle (TyG + guardrails) | InsideTracker | Function Health |
|---|---|---|---|
| Core signal from standard fasting panel (FPG + TG) | Yes citeturn12view1 | Not clearly emphasised as a computed index in cited pages citeturn19search10 | Not clearly emphasised as a computed index in cited pages citeturn19search5 |
| Transparent, reproducible formula | Yes (TyG formula specified) citeturn12view1 | No (public “optimal zones” described as platform-derived) citeturn19search14 | Not disclosed in cited materials citeturn19search5turn19search2 |
| Uses guideline “guardrails” for dysglycaemia | Yes (ADA/NICE thresholds) citeturn3view2turn0search3 | Not clearly specified in cited pages | Not clearly specified in cited pages |
| Tiering anchored to longitudinal outcomes | Yes (diabetes, MetS, CVD cohorts + meta-analysis) citeturn12view1turn12view0turn14view1turn16view0 | Not shown as external validation | Not shown as external validation |
| Action plan tied to outcome trials (DPP-class) | Yes citeturn8view1turn10view0 | General lifestyle recommendations | General lifestyle recommendations |
| Explicit referral triggers | Yes (ADA criteria) citeturn4view1turn4view3 | Not explicit in cited pages | Not explicit in cited pages |

### How this bundle is 10× better (specific differentiators)

1) **Outcome-anchored signal, not “optimisation vibes.”** TyG tier boundaries are anchored to prospective cohort outcomes (incident diabetes, incident metabolic syndrome, and cardiovascular events). citeturn12view1turn14view1turn16view0  
2) **Transparent computation.** Users (and clinicians) can reproduce TyG exactly, including unit conversions. citeturn12view1turn22search2turn22search3  
3) **Clinically safe escalation.** Dysglycaemia is handled using guideline criteria with explicit referral urgency. citeturn4view1turn0search3  
4) **Actionability tied to quantified effect sizes.** Lifestyle and medication options cite hard outcome reductions (DPP, Finnish DPS, SCALE). citeturn8view1turn10view1turn11view0  

---

## 10. VALIDATION STRATEGY

### Public datasets suitable for validation (named explicitly)

- **NHANES (CDC/NCHS)** for cross-sectional biomarker availability and for associations with **linked mortality outcomes** via NCHS-linked mortality files (note: NHANES is not primarily an incident-diabetes cohort). citeturn20search4turn20search0  
- **ARIC** (NHLBI) for prospective cardiometabolic outcomes (incident diabetes and CVD endpoints are commonly available in ARIC analyses). citeturn20search1  
- **Framingham Heart Study** (NHLBI) for long-term longitudinal cardiovascular outcomes and metabolic risk analyses. citeturn20search3turn20search7  
- **MESA** (NHLBI) for multi-ethnic prospective cardiovascular outcomes and risk modelling. citeturn20search10turn20search2  
- **UK Biobank** for large-scale prospective endpoints and broad lab availability (with careful attention to baseline non-fasting variability in some subsets). citeturn17search2  

### Outcomes to track (pre-specified)

Primary outcome:
- **Incident type 2 diabetes** (by standard diagnostic criteria; exclude prevalent diabetes at baseline). citeturn4view1turn12view1  

Secondary outcomes:
- **Incident metabolic syndrome** (where components are available). citeturn14view1turn1search2  
- **Incident cardiovascular events** (MI, stroke, revascularisation, etc; dataset dependent). citeturn16view0  
- **All-cause and cardiovascular mortality** (NHANES-linked mortality for mortality endpoints). citeturn20search0  

### Metrics and comparisons (clinically meaningful, not just “statistically significant”)

- Discrimination: **AUC/c-index** for incident diabetes; compare (a) FPG alone, (b) HbA1c alone, (c) FPG+TG components, (d) **TyG**, and (e) TyG plus conventional risk factors. citeturn12view1turn16view0  
- Calibration: calibration plots and calibration-in-the-large (avoid overcalling risk in low-prevalence groups). citeturn12view0  
- Reclassification: NRI/IDI when adding TyG to baseline models (mirrors how the CVD cohort assessed value added to Framingham variables). citeturn16view0  

### Sample size / event size requirements

- Target **≥500 incident diabetes events** for stable estimates across tiers and for subgroup analyses (sex, age band, BMI category, ethnicity). This is consistent with event counts used in major cohort work (e.g., hundreds of incident cases in TyG cohorts) but formal power should be dataset-specific. citeturn12view1turn12view0  

---

## 11. LIMITATIONS & CAVEATS

**This is not a diagnosis of insulin resistance.**  
TyG is a validated *risk signal* for future diabetes/metabolic syndrome/CVD events, but it does not directly measure insulin resistance in the way a clamp study does. Clamp validation exists but is small and cross-sectional (not Tier 1). citeturn14view0turn12view1

**Cut-offs are not universal (and pretending they are would be medically sloppy).**  
The best Tier 1 synthesis shows substantial heterogeneity across cohort studies. Therefore, these tiers are anchored to strong published thresholds (8.31; ~8.52) but should be treated as *risk zones* rather than absolute “you are/aren’t insulin resistant” cut points for every person on Earth. citeturn12view0turn12view1turn14view1

**False positives / misleading elevations can occur.**  
TyG can rise due to factors other than gradual insulin resistance progression, including:  
- **Non-fasting samples** (postprandial triglycerides/glucose). citeturn4view1  
- **Acute illness or stress** affecting glucose (ADA notes illness/stress can affect glucose and sample handling issues can distort results). citeturn3view2  
- **Medications** that increase diabetes risk or alter metabolism (ADA specifically notes screening considerations with statins, thiazides, certain HIV medications, and glucocorticoids). citeturn3view2  

**Populations not validated for this tiering (use clinician pathways instead):**  
- **Pregnancy** (gestational diabetes pathways are different). citeturn4view2  
- **Established diabetes** (this bundle is for risk detection/prevention, not diabetes pharmacologic management). citeturn4view1  
- **Children/adolescents** (require paediatric validation and age-specific cut-offs). citeturn3view2  
- **People on triglyceride-lowering therapies or intensive glucose-lowering treatments** (TyG becomes an “on-treatment” signal and needs recalibration).

**When medical testing is needed instead (hard triggers):**  
- Any **prediabetes/diabetes** threshold is met → requires clinician confirmation and structured prevention/management. citeturn3view2turn4view1  
- Symptoms of hyperglycaemia (polyuria, polydipsia, unexplained weight loss) with high random glucose → urgent medical evaluation. citeturn4view3

**What this cannot tell you:**  
- It cannot determine *why* insulin resistance is developing (sleep apnoea, endocrine disorders, medications, alcohol, etc.). It flags risk and directs escalation. citeturn3view2turn10view0