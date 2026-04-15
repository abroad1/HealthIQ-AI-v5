# HealthIQ AI — Future Screening and Stratification Priorities

## Purpose

This document sets out which future interpretation classes HealthIQ should prioritise as the platform matures into Phase 2 and Phase 3, with a focus on large-scale preventive health, population screening, employer and insurer relevance, longitudinal metabolic tracking, and early intervention routing.

This is not a list of interesting biomarkers.
It is a strategic prioritisation of interpretation domains that are commercially valuable, medically credible, and realistically screenable from blood biomarkers and related metadata.

---

## Part 1 — Screening priority table

| candidate domain | recommended class | why commercially valuable | likely biomarker basis | intervention / use-case pathway | likely buyer relevance | priority | confidence |
|---|---|---|---|---|---|---|---|
| Dysglycaemia / prediabetes / insulin resistance | syndrome-state or risk construct | Very high prevalence, strong progression risk, and clear prevention pathways. Prediabetes is common at population scale and already sits inside structured prevention programmes. | HbA1c, fasting glucose, fasting insulin, triglycerides, HDL-C, TyG-style derived metrics, waist/BMI metadata | lifestyle coaching, diabetes prevention routing, repeat testing, weight-management pathway, treatment triage | NHS/public health, insurer, employer, clinic, B2C | High | High |
| Atherogenic cardiometabolic risk / ASCVD risk layer | risk construct | Cardiovascular disease remains the largest long-term prevention opportunity. This domain is highly legible for payers and employers because it links to major events, medication pathways, and measurable long-term cost reduction. | Total cholesterol, HDL-C, non-HDL-C, LDL-C, triglycerides, ApoB, Lp(a), hs-CRP, BP/smoking metadata | statin pathway, lipid optimisation, hypertension review, lifestyle intervention, specialist referral | NHS/public health, insurer, employer, clinic, B2C | High | High |
| CKD / kidney risk stratification | risk construct or organ-pattern | CKD is common, expensive, and highly actionable. It is well suited to blood-led and blood-plus-urine screening, and it already maps cleanly to formal monitoring pathways. | Creatinine, eGFR, urea, uric acid, cystatin C where available, urine ACR, BP, diabetes context | repeat monitoring, BP control, diabetes optimisation, nephrology triage, medication review | NHS/public health, insurer, clinic, B2C | High | High |
| MASLD / liver fibrosis risk stratification | screening / routing pattern | Very common, tightly linked to obesity and diabetes, and now increasingly managed through blood-based non-invasive triage. Strong opportunity for early detection and escalation into imaging or fibrosis assessment. | ALT, AST, GGT, platelets, albumin, glucose/HbA1c, triglycerides, BMI/waist, derived scores such as FIB-4 | lifestyle and weight-loss pathway, liver-risk clinic routing, elastography referral, repeat fibrosis surveillance | NHS/public health, insurer, employer, clinic, B2C | High | High |
| Integrated metabolic syndrome / cardiometabolic clustering | other stratification class | Buyers often want a population-level stratification layer, not isolated biomarkers. This is valuable for longitudinal tracking, intervention prioritisation, and employer or insurer cohort segmentation. | glucose/HbA1c, triglycerides, HDL-C, BP, waist/BMI, liver enzymes, uric acid | coaching segmentation, preventive clinic routing, population risk cohorts, repeat monitoring | insurer, employer, clinic, B2C; some NHS relevance | High | Medium-High |
| Iron deficiency / anaemia / iron depletion | syndrome-state | Very common, easy to detect, and highly actionable. It also has unusually direct productivity and fatigue relevance, which gives it employer value as well as women’s health and public-health relevance. | Ferritin, transferrin saturation, transferrin, CBC indices, CRP context | oral/IV iron pathway, menstrual/GI-loss review, fatigue pathway, repeat monitoring | employer, clinic, B2C, public health | High | High |
| Thyroid dysfunction stratification | organ-pattern | Common and clinically useful, especially in fatigue, lipid disturbance, and women’s health pathways, but less commercially central than dysglycaemia, CVD, kidney, or liver domains. | TSH, free T4, free T3, TPOAb, TgAb, lipids | repeat thyroid testing, GP or endocrine review, medication initiation or adjustment | clinic, B2C, some employer relevance | Medium | Medium-High |
| Chronic inflammatory burden / vascular inflammation | risk construct | Useful as a modifier and engagement layer, but weak as a standalone screening pillar because the signal is non-specific. Best used to refine cardiometabolic, kidney, or liver interpretation. | hs-CRP, CRP, ESR where available, fibrinogen, CBC-derived inflammation patterns | repeat testing, lifestyle change, cardiometabolic refinement, selective referral | insurer, clinic, B2C | Medium | Medium |
| Hormonal ageing / androgen deficiency | syndrome-state | Commercially attractive in private and men’s-health markets, but weaker for mass preventive screening because prevalence, reimbursement logic, and intervention economics are less clean than metabolic or cardiovascular domains. | total testosterone, SHBG, free testosterone, LH/FSH, albumin, symptom metadata | repeat morning testing, sleep/weight-loss pathway, endocrinology or TRT evaluation | clinic, B2C | Medium | Medium |
| Nutrient insufficiency bundle | syndrome-state | Useful in B2C and some employer wellness settings, but less central to large-scale payer or public-health prevention unless tied to fatigue, pregnancy, anaemia, or defined risk groups. | ferritin, B12, folate, vitamin D, CBC, homocysteine | supplementation, dietary intervention, repeat testing | B2C, employer, clinic | Medium-Low | Medium |
| Stress / cortisol / recovery / fatigue biology | explanatory or routing layer | Attractive in consumer markets but currently weak as a rigorous blood-led preventive screening domain. Bloods alone do not screen this cleanly enough for population-scale medical stratification. | cortisol/DHEA where available, CRP, CBC, thyroid, iron, testosterone, symptom metadata | coaching, sleep and stress pathway, repeat contextual review | B2C, some employer wellness | Low | Medium |
| Broad cancer early-detection patterning from standard bloods | other stratification class | Commercially tempting but weakly screenable from routine bloods alone. Standard blood chemistry is better for incidental prompting than for a core screening proposition. | CBC, inflammatory markers, liver profile, proteins; usually insufficient alone | route to formal screening or GP review when concerning | limited clinic/B2C relevance | Low | High |

---

## Part 2 — Top priority shortlist

### Ranked shortlist

1. Dysglycaemia / prediabetes / insulin-resistance stratification  
2. Atherogenic cardiometabolic / ASCVD risk stratification  
3. CKD / kidney risk stratification  
4. MASLD / liver fibrosis risk stratification  
5. Integrated metabolic syndrome / cardiometabolic clustering  
6. Iron deficiency / anaemia / iron depletion  
7. Thyroid dysfunction stratification as a secondary expansion lane  

### Why this shortlist matters

These domains sit at the strongest intersection of:

- prevalence at population scale
- high downstream morbidity and cost
- realistic screenability from blood biomarkers and basic metadata
- plausible intervention pathways
- relevance across multiple buyers, not just B2C users

They are also suitable for both:

- population screening value
- longitudinal stratification value
- intervention-routing value

---

## Part 3 — Naming and framing implications

### 1. Dysglycaemia / prediabetes / insulin resistance
Best framed as: **syndrome-state** or **risk construct**  
Use phenotype language carefully. “Insulin-resistant phenotype” can be valid in research-facing contexts, but for product strategy the safer framing is insulin resistance state, prediabetes state, or glycaemic risk.

### 2. Atherogenic cardiometabolic / ASCVD
Best framed as: **risk frame**  
This is strongest when presented as cardiovascular risk, atherogenic burden, or ASCVD risk. It should not be treated as a phenotype.

### 3. CKD / kidney
Best framed as: **organ-risk** or **screening / routing pattern**  
The established language is kidney function risk, CKD risk category, or kidney health stratification, not phenotype.

### 4. MASLD / liver fibrosis
Best framed as: **screening / routing pattern** or **organ-pattern**  
The commercially useful framing is liver fat / fibrosis risk or MASLD liver-risk pattern, not a phenotype label.

### 5. Integrated metabolic syndrome / clustering
Best framed as: **stratification layer**  
This is useful precisely because it is a synthesis layer that groups risk and dysfunction across multiple systems. It does not need phenotype terminology to be credible.

### 6. Iron deficiency / anaemia
Best framed as: **syndrome-state**  
This is clinically legible, commercially useful, and highly actionable without needing phenotype language.

### 7. Thyroid dysfunction
Best framed as: **organ-pattern**  
Use thyroid dysfunction pattern or thyroid-linked metabolic pattern rather than phenotype.

---

## Part 4 — Strategic conclusion

### What classes of future interpretation are most commercially valuable?

The most commercially valuable future classes are the ones that combine:

- very high prevalence
- high downstream cost
- clear blood-led screenability
- actionable follow-up pathways
- relevance across multiple buyer types

Those are:

- dysglycaemia / insulin resistance / prediabetes
- cardiometabolic / atherogenic risk
- kidney risk / CKD stratification
- MASLD / liver fibrosis risk
- integrated metabolic clustering
- iron deficiency / anaemia

### Which of those are realistic for a blood-led platform?

The most realistic blood-led platform domains are:

- dysglycaemia / insulin resistance
- ASCVD / lipid-driven cardiometabolic risk
- CKD / kidney risk
- MASLD / fibrosis routing
- iron deficiency / anaemia
- thyroid dysfunction as a secondary but useful domain

These all have strong fit with blood biomarkers, clear follow-up logic, and strong longitudinal potential.

### Which should HealthIQ prioritise in future Phase 2 / Phase 3 roadmap planning?

#### Phase 2 priorities

- deepen dysglycaemia / insulin resistance
- deepen cardiometabolic / ASCVD risk
- deepen CKD / kidney risk
- deepen MASLD / liver fibrosis risk
- build integrated metabolic clustering as a master stratification layer

#### Phase 3 priorities

- add longitudinal change tracking across those domains
- add screening-to-routing logic for employers, insurers, and clinics
- strengthen cohort-level segmentation and intervention prioritisation
- develop programme-fit outputs for payer, employer, and preventive-clinic pathways

### Which are interesting medically but probably not commercially central?

These may be useful, but should not become the foundation of the core commercial roadmap:

- generic inflammation as a standalone category
- stress / cortisol / recovery constructs
- broad cancer patterning from routine bloods
- highly niche endocrine optimisation layers
- broad nutrient-insufficiency bundles as a flagship platform layer

These areas may help B2C engagement or add-on products, but they are weaker as the basis of a scalable preventive screening business.

---

## Final strategic recommendation

HealthIQ should not optimise future interpretation growth around “what else can be measured.”

It should optimise around:

- what is common enough to matter at scale
- what is expensive enough to matter to buyers
- what is screenable enough to be blood-led
- what is actionable enough to change outcomes or cost
- what is trackable enough to support long-term platform value

That points clearly toward a future interpretation architecture centred on:

1. metabolic dysregulation  
2. cardiovascular risk  
3. kidney risk  
4. liver / MASLD risk  
5. integrated cardiometabolic clustering  
6. iron deficiency as a high-volume adjunct domain  

These are the strongest candidates for HealthIQ’s Phase 2 and Phase 3 expansion if the goal is to become genuinely valuable in preventive and population-scale blood-based screening.
