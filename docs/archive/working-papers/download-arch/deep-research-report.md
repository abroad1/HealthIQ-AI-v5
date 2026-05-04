# Insulin Resistance Risk Detection Bundle Specification

## Bundle summary

**1. Bundle name**  
**Insulin Resistance Risk Detection (TyG + Glycaemic Guardrails)**. citeturn12view0turn33view0turn31search0

**2. Biological question**  
“Based on my blood tests, are there signs my body is becoming insulin resistant—*even before* I meet criteria for prediabetes or type 2 diabetes?” citeturn12view0turn33view0turn31search0

## Clinical rationale

**3. Clinical rationale**

**What disease/dysfunction does it predict?**  
This bundle is designed to detect *early metabolic dysfunction consistent with insulin resistance* and to stratify risk of progression to **type 2 diabetes** and related cardiometabolic outcomes (metabolic syndrome, atherosclerotic cardiovascular risk). citeturn33view0turn12view0turn15view0turn8view0

**Pathophysiological mechanism (why these signals move early)**  
Insulin resistance is characterised by reduced responsiveness of liver, skeletal muscle, and adipose tissue to insulin. Clinically, this often shows up first as a need for higher insulin secretion to maintain “normal” glucose, and as atherogenic dyslipidaemia (notably higher triglycerides) that reflects impaired lipid handling and hepatic insulin resistance. citeturn30search1turn33view0turn12view0

**At what stage does this provide early warning?**  
The intent is to flag risk *before overt dysglycaemia* (i.e., while fasting glucose and/or HbA1c can still be “normal”), by using the **triglyceride–glucose index (TyG)**—a published, reproducible composite signal that predicts incident diabetes in normoglycaemic cohorts and adds information beyond fasting glucose alone in at least one long-term European cohort. citeturn12view0turn33view0turn3view0

**Why this matters for health outcomes**  
Even intermediate dysglycaemia (“prediabetes”) is associated with higher risks of all-cause mortality and incident cardiovascular disease in large-scale meta-analytic evidence, so earlier detection and risk reduction is clinically meaningful. citeturn8view0turn31search0

## Evidence base

**4. Evidence base**

### Primary research

**Vascular-Metabolic CUN cohort (Preventive Medicine, 2016; doi:10.1016/j.ypmed.2016.01.022)**  
*Design / cohort size / follow-up:* Prospective cohort, **n=4,820**, mean follow-up **8.84 years**. citeturn12view0  
*Key finding:* Diabetes risk increased progressively at **TyG ≥8.31**; among participants with baseline fasting glucose <100 mg/dL, those in the highest TyG quartile had **HR 6.87** (95% CI 2.76–16.85) vs lowest quartile. citeturn12view0  
*Predictive metrics:* In normoglycaemic baseline subgroup, discrimination (AUC) **0.75** (0.70–0.81) for TyG vs **0.66** (0.60–0.72) for fasting plasma glucose and **0.71** (0.65–0.77) for triglycerides (TyG superior to fasting glucose; p=0.017). citeturn12view0  
*Clinical implication:* TyG can identify increased diabetes risk *within* a “normal fasting glucose” stratum, supporting its use as an early risk signal. citeturn12view0

### Supporting research

**Systematic review & meta-analysis of cohort studies (Primary Care Diabetes, 2020; doi:10.1016/j.pcd.2020.09.001)**  
*Design / cohort size:* **13 cohort studies**, total **n=70,380**. citeturn33view0  
*Key finding:* Higher TyG associated with incident type 2 diabetes with pooled **overall HR 2.44** (95% CI 2.17–2.76); pooled **RR 3.12** (95% CI 2.31–4.21). citeturn33view0  
*Important nuance:* High heterogeneity noted, implying threshold values may not transport perfectly across populations without calibration. citeturn33view0

**Korean Genome and Epidemiology Study cohort (Translational Research, 2021; doi:10.1016/j.trsl.2020.08.003)**  
*Design / cohort size / follow-up:* Prospective cohort of **n=4,285** nonobese adults, **12 years**, incident diabetes **14.7%**. citeturn12view1  
*Key finding:* Highest TyG quartile predicted incident diabetes with adjusted **HR 3.67** (95% CI 2.71–4.98) vs lowest quartile (dose–response across quartiles). citeturn12view1

**Large-scale longitudinal cohort in people with “normal” fasting glucose and triglycerides (Frontiers in Endocrinology, 2025; doi:10.3389/fendo.2025.1598171)**  
*Design / cohort size / follow-up:* **n=155,337**, mean follow-up **3.13 years**. citeturn3view0  
*Key finding:* Diabetes incidence rose across TyG quartiles, with adjusted HR reported as high as **3.80** for the highest quartile vs lowest; authors report an inflection around **TyG 8.41** and markedly higher risk above that point (very large HR reported for above-threshold). citeturn3view0  
*Use in this bundle:* Supports a practical “higher risk” zone beginning around the mid–high 8’s even when component labs look “normal.” citeturn3view0

**Metabolic syndrome prediction vs HOMA-IR (Nutr Metab Cardiovasc Dis, 2022; doi:10.1016/j.numecd.2021.11.017)**  
*Design / cohort size / follow-up:* Community-based prospective cohort; baseline analysed **n=9,730**, incident analysis **n=6,091**, follow-up **12 years**. citeturn15view0  
*Key finding:* TyG outperformed HOMA-IR for prevalent metabolic syndrome (AUROC **0.837** vs 0.680) and for incident metabolic syndrome (AUROC **0.654** vs 0.556). Reported optimal TyG cut-off for **incident metabolic syndrome ~8.518**. citeturn15view0  
*Bundle relevance:* Provides a second “anchor” threshold near **8.5** that maps to incident cardiometabolic clustering. citeturn15view0

**Cardiovascular events prediction add-on to Framingham variables (European Journal of Clinical Investigation, 2016; doi:10.1111/eci.12583)**  
*Design / cohort size / follow-up:* **n=5,014**, median follow-up **10 years**. citeturn13view0  
*Key finding:* Highest TyG quintile associated with increased incident CVD risk (HR **2.32**, 95% CI 1.65–3.26). Adding TyG to Framingham variables increased AUC from **0.708** to **0.719** (p=0.014). citeturn13view0

### Clinical guidelines (what major bodies recommend tracking)

**Guidelines clearly recommend screening for dysglycaemia (the clinically actionable downstream state).**  
Major guideline bodies emphasise identifying **prediabetes and diabetes** using **HbA1c, fasting plasma glucose, and/or OGTT**, and recommending preventive interventions for those meeting prediabetes criteria. This bundle deliberately uses those guideline cut-offs as “safety guardrails” for urgency and referral, even though TyG itself is not a formal diagnostic test. citeturn31search0turn9view0turn7search10

*Recommended documents and positions used in this bundle:*
- entity["organization","American Diabetes Association","medical society, US"] Standards of Care in Diabetes—2026: diagnostic thresholds for prediabetes/diabetes (HbA1c, fasting glucose, OGTT) and prevention guidance. citeturn31search0turn31search4  
- entity["organization","U.S. Preventive Services Task Force","preventive guideline body, US"] recommendation statement: screening adults 35–70 years with overweight/obesity, and offering effective preventive interventions for prediabetes. citeturn9view0  
- entity["organization","NICE","guideline body, UK"] type 2 diabetes prevention guidance: identifying high risk using fasting plasma glucose and/or HbA1c (and OGTT where appropriate). citeturn7search10  
- Metabolic syndrome harmonised criteria (joint interim statement including multiple major societies) to justify lipid/waist/BP thresholds often co-tracking with insulin resistance. citeturn30search1

## Biomarkers and calculation

**5. Required biomarkers**

### Minimum required markers (for the core TyG algorithm)

**Fasting plasma glucose (FPG)**  
Why needed: It is (a) one of the two inputs to TyG; (b) a guideline-endorsed screening test for prediabetes/diabetes that anchors urgency and medical follow-up decisions. citeturn12view0turn31search0turn9view0

**Fasting triglycerides (TG)**  
Why needed: It is (a) the second TyG input; (b) a core metabolic syndrome component thresholded in widely used harmonised criteria (≥150 mg/dL / 1.7 mmol/L), linking dyslipidaemia to insulin resistance phenotypes and cardiometabolic clustering. citeturn12view0turn30search1turn15view0

### Enhanced analysis (optional markers)

**HbA1c (glycated haemoglobin)**  
Additional insight: Captures longer-term glycaemic exposure and supports guideline-based classification of normoglycaemia vs prediabetes vs diabetes (especially if fasting status is unreliable or glucose varies). citeturn31search0turn7search10

**Fasting insulin (to compute HOMA-IR as an ancillary “directional” signal)**  
Additional insight: Can indicate hyperinsulinaemia at normal glucose (a plausible early insulin resistance phenotype), but assay variability and lack of universal cut-offs limit its use as a strict tiering gate in a medical-grade bundle. citeturn15view0turn21search0turn22view0

**HDL cholesterol, waist circumference, blood pressure**  
Additional insight: Enables parallel metabolic-syndrome pattern recognition using harmonised criteria (important because insulin resistance clusters with these signals, and because cardiovascular risk management is often driven by the broader cluster, not glucose alone). citeturn30search1turn15view0

**6. Calculation method**

**Published algorithm (core): Triglyceride–Glucose Index (TyG)**  
TyG is calculated as:  
**TyG = ln [ (fasting TG in mg/dL × fasting plasma glucose in mg/dL) / 2 ]** citeturn12view0turn12view1turn13view0

**Unit handling (en-GB friendly):**  
If your lab reports SI units (mmol/L):  
- glucose mg/dL = glucose (mmol/L) × 18  
- triglycerides mg/dL = triglycerides (mmol/L) × 88.57  
Then apply the standard TyG formula above. citeturn12view0turn30search1

**Why this method is defensible**  
TyG is not just a “biomarker association”; it has longitudinal outcome evidence for incident type 2 diabetes (including a European cohort with AUC reporting) plus meta-analytic cohort evidence. citeturn12view0turn33view0

**Important honesty (medical-grade caveat):**  
There is **no single universally accepted TyG cut-off** across ancestries, ages, and clinical settings; several high-quality sources explicitly show heterogeneity. This bundle therefore uses **evidence-anchored zones** with “guardrails” from formal diagnostic criteria (HbA1c/FPG) to prevent false reassurance. citeturn33view0turn31search0turn15view0

## Output tiers

**7. Output tiers**

This bundle reports (a) TyG tier; (b) whether guideline-defined dysglycaemia is present; (c) a plain-language risk interpretation.

### Optimal range

**Biomarker values**
- **TyG < 8.30** (below the level where diabetes risk rose progressively in the long-term European cohort). citeturn12view0  
- **AND** no guideline-defined prediabetes/diabetes:  
  - HbA1c **< 5.7%** (<39 mmol/mol) and fasting glucose **< 5.6 mmol/L** (<100 mg/dL), if available. citeturn31search0  

**What this means for the user**  
Your current fasting glucose–lipid pattern does not suggest an insulin-resistance phenotype at a level associated with markedly elevated incident diabetes risk in the key validating cohorts. This is *not* a “free pass”—risk still depends on weight trajectory, activity, family history, and ethnicity—but it’s a reassuring metabolic baseline. citeturn12view0turn33view0turn9view0

**Prevalence in population (approximate)**  
In a large cohort study that used TyG quartiles, “below high-risk cut points” generally corresponds to the lower and middle distribution (roughly the lower ~50–75% depending on population). Exact prevalence will vary substantially by age, adiposity, and ancestry. citeturn3view0turn33view0

### Suboptimal range

**Biomarker values**
- **TyG 8.30 to 8.49** (the “transition zone” between the diabetes-risk signal observed at ~8.31 and the incident metabolic syndrome cut point around ~8.52). citeturn12view0turn15view0  
- **AND** not meeting formal prediabetes/diabetes criteria (HbA1c <5.7% and fasting glucose <5.6 mmol/L), if measured. citeturn31search0

**What this means for the user**  
This is the “you’re drifting” category: your combined fasting triglyceride–glucose signal is high enough that, in multiple cohorts, people in higher TyG strata had meaningfully higher future diabetes risk—even when they started without diagnosed diabetes. Treat it as an early warning that is still highly modifiable. citeturn33view0turn12view1turn12view0

**Risk implications**  
In cohort meta-analysis, higher TyG was associated with substantially higher incident diabetes risk (pooled HR >2). This tier is not meant to specify *your* exact absolute risk; it flags that you are no longer in the low-risk metabolic distribution. citeturn33view0

**Prevalence in population (approximate)**  
In datasets reported in quartiles, a zone like this often corresponds to “upper-middle” distribution (often ~15–30%), but this is population-dependent. citeturn3view0

### At risk range

**Biomarker values (any of the following triggers “At risk”)**
- **TyG ≥ 8.50** (aligns with an evidence-based incident metabolic syndrome cut point ~8.518 and sits within the higher-risk strata across multiple cohorts). citeturn15view0turn33view0  
**OR**
- **Prediabetes by guideline criteria**, even if TyG is lower:  
  - HbA1c **5.7–6.4%** (39–47 mmol/mol) and/or fasting plasma glucose **5.6–6.9 mmol/L** (100–125 mg/dL). citeturn31search0  
  - UK high-risk ranges used in prevention guidance also include fasting plasma glucose **5.5–6.9 mmol/L** or HbA1c **42–47 mmol/mol (6.0–6.4%)**. citeturn7search10  

**What this means for the user**  
You have a lab pattern consistent with materially elevated cardiometabolic risk. If you also meet prediabetes criteria, you are already in a clinically recognised high-risk state where intensive prevention is recommended. citeturn31search0turn31search4

**Urgency level**
- **Moderate urgency (within weeks):** At-risk TyG without prediabetes/diabetes thresholds → act now, repeat fasting labs in ~3 months after intervention, and assess broader cardiometabolic risk factors. citeturn12view0turn15view0turn33view0  
- **High urgency (prompt clinical confirmation):** Any diabetes-range value (HbA1c ≥6.5% / ≥48 mmol/mol or fasting glucose ≥7.0 mmol/L / ≥126 mg/dL) requires clinician confirmation and management; this bundle is not designed to “handle” a new diabetes diagnosis without medical supervision. citeturn31search0

**Prevalence in population (approximate)**  
A high TyG zone often overlaps with the top quartile of TyG in population cohorts; separately, prediabetes prevalence can be substantial in adult populations, with a major guideline statement citing ~34.5% meeting prediabetes criteria in the US (varies by country and age). citeturn9view0turn31search0

## Actionable recommendations

**8. Actionable recommendations**

These are tier-specific and prioritise interventions with outcome evidence (incident diabetes reduction and/or cardiometabolic risk reduction).

### Optimal tier interventions

**Intervention: Maintain (or build) guideline-level physical activity as a protective baseline**  
Evidence: In a systematic review and dose–response meta-analysis, high vs low total physical activity was associated with lower incident type 2 diabetes risk (summary RR **0.65**). citeturn29view0  
Action spec: Aim for at least **150 minutes/week** moderate activity and include some vigorous or resistance work if safe—then keep it consistent rather than episodic.

**Intervention: Choose a cardiometabolic dietary pattern (Mediterranean/DASH-style) as default**  
Evidence: Mediterranean diet trials in high-risk but non-diabetic adults showed substantial reductions in incident diabetes (e.g., HR ~0.49–0.48 vs control in one randomised trial). citeturn18view0  
Action spec: Make the “default plate” vegetables/legumes + minimally processed carbs + olive oil/nuts + fish/poultry; reduce refined starches and ultra-processed foods.

**Intervention: Avoid weight gain (because risk rises sharply with weight trajectory)**  
Evidence: Intensive lifestyle programmes that achieved weight-loss and activity targets reduced diabetes incidence by **~58%** in people at high risk; while you’re not “high risk,” the direction of effect is clear: maintaining a favourable weight/activity pattern is protective. citeturn17search2turn17search13

**Intervention: Re-test cadence**  
Action spec: Repeat TyG inputs (fasting glucose + fasting triglycerides) **annually** if stable; earlier (3–6 months) if weight gain, medication changes, or rising HbA1c occur. This is a pragmatic clinical monitoring choice consistent with prevention-oriented screening logic (not a formal guideline mandate for TyG). citeturn9view0turn31search0

### Suboptimal tier interventions

**Intervention: Structured lifestyle programme targeting 5–7% weight loss if overweight**  
Evidence: In the Diabetes Prevention Program trial, intensive lifestyle intervention reduced incident diabetes by **58%** vs placebo. citeturn17search2turn17search5  
Action spec: If BMI is above healthy range, set a 12–24 week target of **5–7% loss**, using calorie deficit + food quality + stepcount/fitness tracking.

**Intervention: Physical activity prescription (don’t “just exercise more”)**  
Evidence: Prospective evidence links higher activity to lower diabetes risk; meta-analysis shows meaningful reductions across activity domains. citeturn29view0  
Action spec:  
- **150–300 min/wk** moderate OR **75–150 min/wk** vigorous,  
- plus **2–3 resistance sessions/week**,  
- plus reduce prolonged sedentary time (break up sitting).

**Intervention: Mediterranean diet with specific adjuncts (olive oil / nuts) rather than vague “eat better”**  
Evidence: Mediterranean diet interventions (including olive oil and nuts supplementation arms) reduced incident diabetes in older high-risk adults in randomised evidence. citeturn18view0turn19view0  
Action spec: Daily olive oil as primary added fat; nuts (e.g., ~30 g/day); prioritise legumes and whole foods; reduce refined grains and sugar-sweetened beverages.

**Intervention: Set a measurable lab target and timeline**  
Action spec: Recheck fasting glucose + triglycerides (and ideally HbA1c) after **~12 weeks** of consistent intervention to confirm TyG is trending down (TyG is sensitive to both glucose and triglyceride changes). Cohort evidence supports that risk tracks with TyG strata; trend direction is clinically meaningful even if absolute cut-offs vary. citeturn12view0turn33view0

**Medical referral criteria (Suboptimal tier)**  
Refer to primary care if:  
- HbA1c is rising toward prediabetes range,  
- fasting glucose is persistently near 5.6 mmol/L,  
- triglycerides are elevated (≥1.7 mmol/L) or secondary causes suspected (thyroid disease, alcohol excess, medications). This aligns with prevention guidance that escalates assessment when glycaemic risk becomes measurable. citeturn31search0turn7search10turn30search1

### At risk tier interventions

**Intervention: Intensive lifestyle intervention (same “dose” as DPP-class programmes)**  
Evidence: DPP lifestyle intervention reduced incident diabetes by **58%**; Finnish DPS similarly demonstrated prevention efficacy (also ~58% reduction reported in that trial). citeturn17search2turn17search13  
Action spec: Treat this like a clinical programme, not a健康 resolution: weekly accountability, explicit activity targets, dietary pattern, and weight target.

**Intervention: Consider metformin when risk is high enough and clinician agrees**  
Evidence: In DPP, metformin reduced diabetes incidence by **31%** vs placebo (less than lifestyle overall). citeturn17search2turn17search5  
Guideline position: ADA prevention guidance recognises metformin as the pharmacologic option with the most robust evidence base for diabetes prevention among people with prediabetes, with subgroup nuances (e.g., higher benefit in certain higher-risk groups). citeturn31search4  
Action spec: This is not a self-start supplement; it is a GP/endocrinology decision.

**Intervention: Confirmatory testing and formal risk work-up**  
Evidence: Guideline bodies recommend diagnostic confirmation and appropriate preventive interventions once prediabetes/diabetes thresholds are met. citeturn31search0turn9view0turn7search10  
Action spec:  
- Repeat HbA1c and fasting glucose to confirm abnormality,  
- consider OGTT if discordant or if clinical suspicion is high,  
- assess blood pressure, lipids, liver markers, and adiposity distribution as part of cardiometabolic evaluation.

**Intervention: Cardiovascular risk reduction is not optional**  
Evidence: Prediabetes is associated with higher incident cardiovascular disease and mortality in very large meta-analysis; reducing global risk factors matters even before diabetes diagnosis. citeturn8view0  
Action spec: clinician-led assessment of lipids, blood pressure, smoking, and consideration of statin/antihypertensive therapy as indicated by standard risk algorithms (outside this bundle’s scope, but clinically necessary).

**Medical referral triggers (At risk tier)**  
- **Immediate clinician review (days to 1–2 weeks):** diabetes-range HbA1c or fasting glucose. citeturn31search0  
- **GP / primary care within weeks:** prediabetes range HbA1c/FPG, or TyG persistently ≥8.5 after short-term intervention. citeturn31search0turn15view0turn33view0  
- **Specialist referral (endocrinology/metabolic clinic):** rapid progression, multiple abnormalities, suspected secondary endocrine causes, or complex comorbidity. This is consistent with guideline-driven escalation when progression risk is high. citeturn31search0turn7search10

## Competitive analysis

**9. Competitive analysis**

### What does InsideTracker provide for insulin resistance?

**Approach**  
entity["company","InsideTracker","health analytics company"] groups “sugar biomarkers” including fasting glucose, fasting insulin, and HbA1c, and states that the combination is used for a more comprehensive view of blood sugar. citeturn22view1  
InsideTracker publishes fasting insulin educational content, including noting lack of universally accepted fasting insulin reference ranges and providing an internally-derived “generally recommended” range with advice to discuss with a doctor. citeturn22view0  
InsideTracker explicitly describes HOMA-IR as primarily a research tool and notes the lack of a defined normal range. citeturn21search0

**Evidence quality (as presented)**  
They link out to studies and discuss insulin biology, but their “optimal zones” are proprietary/derived and not presented as a validated clinical prediction model with externally validated AUC/calibration for hard outcomes within their product documentation. citeturn22view0turn21search20

**Gaps**
- No clear, published, outcome-validated insulin resistance *risk score* in their consumer-facing materials (mostly education + ranges). citeturn22view0turn22view1  
- HOMA-IR is discussed as a research tool with unclear thresholding, which is honest but leaves the user without a defensible tiering algorithm. citeturn21search0  
- No explicit TyG-based detection pathway despite strong cohort evidence that TyG predicts diabetes risk in normoglycaemia and adds discrimination beyond fasting glucose in at least one European cohort. citeturn12view0turn33view0

### What does Function Health provide?

**Approach**  
entity["company","Function Health","health testing company"] publishes an “insulin sensitivity” explainer that frames testing around fasting glucose, HbA1c, and insulin. citeturn25search2turn25search4  
They market a large lab panel approach and claim a substantial proportion of their users have fasting insulin outside “optimal” ranges, but those statistics appear to be internal/observational and not peer-reviewed validation. citeturn25search4

**Gaps**
- Public materials do not present an externally validated, published algorithm (with calibration/AUC for incident diabetes) that users can compute and interpret consistently across labs. citeturn25search2turn25search4  
- As with most fasting-insulin-centric approaches, there is the unresolved issue of assay variability and the absence of globally accepted cut-offs for “insulin resistance” diagnosis using fasting insulin alone. citeturn22view0turn21search0

### How is this bundle 10x better?

**Specific differentiators**
- Uses a **published, explicit formula (TyG)** that is computable from standard fasting labs and has **cohort and meta-analytic longitudinal outcome evidence** for incident type 2 diabetes risk. citeturn12view0turn33view0  
- Provides **evidence-anchored thresholds** (8.31 diabetes-risk signal; ~8.52 incident metabolic syndrome cut point) while explicitly acknowledging heterogeneity and preventing false reassurance via guideline-based glycaemic guardrails. citeturn12view0turn15view0turn31search0turn33view0  
- Couples detection with **tiered actions tied to outcome trials** (DPP lifestyle/metformin; Mediterranean diet RCTs). citeturn17search2turn18view0turn31search4  
- Separates “risk detection” from “diagnosis” with **clear referral triggers aligned with major clinical guidance**—this is what makes it clinically defensible rather than wellness-flavoured. citeturn31search0turn9view0turn7search10

## Validation strategy and limitations

**10. Validation strategy**

**How to validate this bundle (practical and defensible)**  
Validation must occur at two levels: (1) *risk signal validity* (association with outcomes); (2) *clinical utility* (does tiering improve decisions vs standard markers).

**Datasets that can test it**
- Prospective cohorts with fasting glucose/triglycerides and incident diabetes endpoints to replicate the hazard gradients (similar to the cohorts already published). citeturn33view0turn12view0  
- National survey datasets with linked mortality follow-up can test associations with all-cause/CVD mortality (though not incident diabetes in the same way). citeturn8view0

(Examples named in your prompt—NHANES/Framingham—are appropriate in principle, but access and endpoint structure differ; the key requirement is longitudinal endpoints.)

**Outcomes to track (primary and secondary)**
- Primary: incident type 2 diabetes (standard diagnostic criteria). citeturn12view0turn33view0turn31search0  
- Secondary: incident metabolic syndrome; incident cardiovascular events; all-cause and CVD mortality. citeturn15view0turn13view0turn8view0

**Sample size needed (rule of thumb for model validation)**
- For calibration/discrimination of a 3-tier rule, the limiting factor is the number of events. A practical target is **≥500 incident diabetes events** to support stable estimation across tiers and subgroup checks (sex/age/BMI strata). This aligns with the event volumes seen in large cohorts (hundreds to thousands of diabetes events) used in published TyG work. citeturn12view0turn12view1turn3view0

**11. Limitations & caveats**

**What this cannot tell you**
- It cannot diagnose insulin resistance directly (gold-standard clamp testing is not being done). It is a *risk signal* for future diabetes/cardiometabolic outcomes, not a definitive physiological measurement for an individual. citeturn12view0turn33view0  
- It is not a substitute for guideline-defined diagnostic criteria for prediabetes/diabetes. citeturn31search0turn9view0

**False positive scenarios (TyG can be high for reasons that are not “classic” insulin resistance progression)**
- Hypertriglyceridaemia driven by alcohol intake, untreated hypothyroidism, nephrotic syndrome, or certain medications can elevate TG and therefore TyG independent of a stable long-term insulin-resistance trajectory (clinical evaluation required). The existence of secondary-cause pathways is part of why lipid guidelines recommend review of secondary causes at higher triglyceride levels. citeturn30search3turn30search5  
- Acute illness, recent major dietary changes, or non-fasting sampling can distort the inputs.

**Populations not validated for (or requiring special handling)**
- Pregnancy (gestational physiology differs; diabetes screening uses different pathways).  
- People with established diabetes on glucose-lowering therapy (risk prediction is not the goal; management is). citeturn31search0  
- Children/adolescents (cut points and natural history differ; require paediatric validation).  
- People on intensive lipid-lowering or triglyceride-lowering treatments (TyG inputs are altered by therapy; interpretation becomes “on-treatment risk,” which needs separate calibration).

**When medical testing is needed instead**
- Any **prediabetes/diabetes thresholds** by HbA1c or fasting glucose require medical confirmation, personalised management, and evaluation for comorbid risks. citeturn31search0turn7search10  
- If TyG is persistently high despite strong lifestyle adherence, consider clinician-led evaluation (secondary causes, fatty liver, endocrine disorders, medication effects). citeturn30search3turn30search5

## References in APA format

Alberti, K. G. M. M., et al. (2009). Harmonizing the metabolic syndrome: A joint interim statement of international organisations. *Circulation, 120*(16), 1640–1645. doi:10.1161/CIRCULATIONAHA.109.192644 citeturn30search1

American Diabetes Association Professional Practice Committee. (2026). Diagnosis and Classification of Diabetes: Standards of Care in Diabetes—2026. *Diabetes Care, 49*(Supplement_1), S27–S49. doi:10.2337/dc26-S002 citeturn31search0

American Diabetes Association Professional Practice Committee. (2026). Prevention or Delay of Diabetes and Associated Comorbidities: Standards of Care in Diabetes—2026. *Diabetes Care, 49*(Supplement_1). citeturn31search4

Aune, D., et al. (2015). Physical activity and the risk of type 2 diabetes: A systematic review and dose-response meta-analysis. *European Journal of Epidemiology, 30*(7), 529–542. doi:10.1007/s10654-015-0056-z citeturn29view0

Cai, X., et al. (2020). Association between prediabetes and risk of all cause mortality and cardiovascular disease: Updated meta-analysis. *BMJ, 370*, m2297. doi:10.1136/bmj.m2297 citeturn8view0

da Silva, A., et al. (2020). Triglyceride–glucose index predicts independently type 2 diabetes mellitus risk: A systematic review and meta-analysis of cohort studies. *Primary Care Diabetes, 14*(6), 584–593. doi:10.1016/j.pcd.2020.09.001 citeturn33view0

Knowler, W. C., et al. (2002). Reduction in the incidence of type 2 diabetes with lifestyle intervention or metformin. *The New England Journal of Medicine, 346*, 393–403. doi:10.1056/NEJMoa012512 citeturn17search2turn17search5

Navarro-González, D., et al. (2016). TyG index in comparison with fasting plasma glucose improved diabetes prediction in patients with normal fasting glucose: The Vascular-Metabolic CUN cohort. *Preventive Medicine, 86*, 99–105. doi:10.1016/j.ypmed.2016.01.022 citeturn12view0

Park, B., et al. (2021). TyG index as a predictor of incident type 2 diabetes among nonobese adults: 12-year longitudinal study. *Translational Research, 228*, 42–51. doi:10.1016/j.trsl.2020.08.003 citeturn12view1

Salas-Salvadó, J., et al. (2011). Reduction in the incidence of type 2 diabetes with the Mediterranean diet: Randomised trial results. *Diabetes Care, 34*(1), 14–19. doi:10.2337/dc10-1288 citeturn18view0

Tuomilehto, J., et al. (2001). Prevention of type 2 diabetes mellitus by changes in lifestyle among subjects with impaired glucose tolerance. *The New England Journal of Medicine, 344*(18), 1343–1350. doi:10.1056/NEJM200105033441801 citeturn17search13

U.S. Preventive Services Task Force. (2021). Screening for Prediabetes and Type 2 Diabetes: Recommendation Statement. *JAMA, 326*(8), 736–743. doi:10.1001/jama.2021.12531 citeturn9view0