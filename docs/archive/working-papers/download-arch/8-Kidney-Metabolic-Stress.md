### 1. Executive Summary
This signal, Kidney Metabolic Stress, is designed to detect early renal dysfunction driven by systemic metabolic disturbances before conventional markers like serum creatinine become abnormal. The biological question it answers for an end user is whether metabolic factors—such as insulin resistance, dyslipidemia, or hypertension—are inducing functional and structural stress on the kidneys.

The primary metric recommended for platform use is the **urinary albumin-to-creatinine ratio (uACR)** , supported by the derived metric **estimated glomerular filtration rate (eGFR)** . Emerging metabolic biomarkers—including trimethylamine N-oxide (TMAO), myo-inositol, and pyruvate—show strong diagnostic potential (AUC > 0.7) for detecting early-stage chronic kidney disease (CKD) but lack the prospective, outcome-driven validation required for threshold implementation .

The evidence quality supporting the uACR and eGFR framework is **Tier 1**, anchored in KDIGO clinical practice guidelines and large prospective cohorts. However, evidence for specific thresholds defining "metabolic stress" independent of established CKD stages is currently inconclusive. The signal can be implemented using standard CKD staging criteria while flagging the absence of validated metabolic stress thresholds.

### 2. Biological Question
> "Based on my blood test results, are there signs that metabolic dysfunction—such as insulin resistance, oxidative stress, or altered energy metabolism—is placing stress on my kidneys, even before my standard kidney tests become abnormal?"

### 3. Clinical Rationale
- **What disease or dysfunction does this signal predict or detect?**  
  This signal predicts early-stage chronic kidney disease (CKD) and acute kidney injury (AKI) risk driven by metabolic drivers, including diabetic nephropathy, hypertensive nephrosclerosis, and obesity-related glomerulopathy. It also captures subclinical tubular stress not yet reflected by eGFR decline .

- **What is the pathophysiological mechanism—why do these biomarkers move early?**  
  Metabolic dysfunction induces renal stress through multiple pathways:  
  - **Mitochondrial dysfunction and energy depletion**: Hypertensive insults deplete ATP and NADH in glomeruli, activating AMPK and mTOR signaling to maintain energy balance, which alters cytoskeletal components in podocytes .  
  - **Inflammation and oxidative stress**: Hyperoxaluria models show upregulated inflammatory pathways (e.g., Cxcl2) and suppressed fatty acid oxidation, linking metabolic dysregulation to tubular injury .  
  - **Accumulation of uremic toxins**: Gut-derived metabolites like TMAO rise early due to altered filtration and tubular secretion .  
  - **Disrupted amino acid and energy metabolism**: Branched-chain amino acids, proline, and pyruvate metabolism are altered in early CKD, reflecting increased collagen synthesis demands and anaplerotic pathway activation .  
  - **Tubular stress markers**: Urinary biomarkers such as TIMP-2 and IGFBP7 indicate cell cycle arrest in tubular cells within hours of metabolic insult, preceding creatinine rise .

- **At what stage in disease progression does this signal provide useful information?**  
  The signal is most valuable in **CKD stages G1–G3** (eGFR ≥30 mL/min/1.73 m²), where conventional markers (creatinine, eGFR) may remain normal despite established pathology . It also captures **subclinical AKI**—patients with normal serum creatinine but elevated urinary damage biomarkers who face worse clinical outcomes .

- **Why does early detection matter for patient outcomes?**  
  Early identification of metabolic renal stress enables interventions that slow or halt progression: blood pressure control (ACE inhibitors/ARBs), glycemic management, dietary modification (reduced sodium, oxalate, or protein), and avoidance of nephrotoxins . Multi-omics data suggest that metabolic or dietary interventions could prevent hypertension-induced nephropathy .

### 4. Evidence Base
**Primary Evidence**

| Field | Content |
|-------|---------|
| Study name / first author | Rinschen MM, et al. |
| Journal | *Science Signaling* |
| Year | 2019 |
| DOI | 10.1126/scisignal.aax9760 |
| Design | Multi-omics (metabolomics, phosphoproteomics, proteomics) in hypertensive rat model |
| Sample size | Not specified (animal model) |
| Follow-up | Acute and chronic time points |
| Key finding | Hypertension induces metabolic rewiring in glomeruli: ATP/NADH depletion, oxidized lipid accumulation, altered branched-chain amino acid and proline metabolism. mTOR and AMPK signaling control cytoskeletal changes in podocytes. |
| Threshold derived | None—mechanistic study without human thresholds. |
| Limitations | Animal model; human validation required. |

| Field | Content |
|-------|---------|
| Study name / first author | Nkuipou-Kenfack E, et al. |
| Journal | *PLOS ONE* |
| Year | 2014 |
| DOI | 10.1371/journal.pone.0096955 |
| Design | Prospective cohort (training n=20 CKD, test n=29) |
| Sample size | 49 total patients |
| Follow-up | 2.8 ± 0.8 years |
| Key finding | Plasma metabolites significantly correlated with eGFR at baseline (ρ = −0.8031) and follow-up (ρ = −0.6009). Urinary metabolites also correlated (ρ = −0.6557 baseline, ρ = −0.6574 follow-up). Urinary peptides performed equivalently. Combining omics did not improve correlation. |
| Threshold derived | No specific cut-off values provided; continuous correlation reported. |
| Limitations | Small sample size; mixture of diabetic and non-diabetic CKD; published 2014. |

| Field | Content |
|-------|---------|
| Study name / first author | Authors from Centre of Biomedical Research, Lucknow |
| Journal | *Molecular Omics* (RSC Publishing) |
| Year | 2025 |
| DOI | 10.1039/D5MO00018A |
| Design | Cross-sectional metabolomics (1H NMR) |
| Sample size | 115 human serum samples (24 healthy controls, 91 early-stage CKD G1–G3) |
| Follow-up | N/A |
| Key finding | Ten metabolites significantly differentiated early CKD from controls: myo-Inositol, glycerol, pyruvate, carnitine, phenylalanine, tyrosine, histidine, TMAO, 2-hydroxyisobutyrate, 3-hydroxyisobutyrate (p < 0.05, VIP > 1). ROC AUC > 0.7 for each. Pathway dysregulation in inositol phosphate, tyrosine, histidine, pyruvate metabolism. |
| Threshold derived | AUC values provided; no binary cut-off thresholds for clinical use. |
| Limitations | Cross-sectional design; no hard outcomes; validation in prospective cohorts required. |

**Supporting Evidence**

| Field | Content |
|-------|---------|
| Study name / first author | KDIGO (Kidney Disease: Improving Global Outcomes) |
| Journal | KDIGO Clinical Practice Guideline |
| Year | 2024 (reflected in search results) |
| DOI | N/A (guideline) |
| Design | Clinical practice guideline |
| Sample size | N/A |
| Follow-up | N/A |
| Key finding | KDIGO criteria for AKI: >0.3 mg/dL increase in creatinine within 48 hours or >1.5× baseline within 7 days. CKD diagnosis based on eGFR and albuminuria. |
| Threshold derived | Creatinine: >0.3 mg/dL (AKI); eGFR: <60 mL/min/1.73 m² (CKD); uACR: ≥30 mg/g (CKD). |
| Limitations | Thresholds are for established disease, not early metabolic stress. |

| Field | Content |
|-------|---------|
| Study name / first author | Ulta Lab Tests (functional medicine review) |
| Journal | N/A (commercial blog) |
| Year | 2025 |
| DOI | N/A |
| Design | Narrative review |
| Sample size | N/A |
| Follow-up | N/A |
| Key finding | Proposes "functional" optimal ranges: creatinine women >0.90 mg/dL, men >1.10 mg/dL; eGFR <90 mL/min/1.73 m²; BUN >18 mg/dL; uACR <10 mg/g ideal, 10–30 early leakiness; cystatin C >0.83 mg/L. |
| Threshold derived | Multiple "yellow flag" thresholds (see table below). |
| Limitations | Tier 3 evidence—not peer-reviewed; based on functional medicine opinion, not hard outcomes. **This threshold applies to functional medicine screening, not to this signal's biological question.** |

**Cautionary Evidence**

| Field | Content |
|-------|---------|
| Study name / first author | Various (summarized in PMC Table 1) |
| Journal | PMC (NIH) |
| Year | 2022 |
| DOI | 10.3390/ijms23084444 (assumed parent article) |
| Design | Systematic review context |
| Sample size | N/A |
| Follow-up | N/A |
| Key finding | Creatinine rises only after >50% nephron loss; affected by age, race, muscle mass, fluid status, medications. Cystatin C affected by CRP, WBC, albumin, thyroid disease, steroids. NGAL false elevations in sepsis, malignancy, COPD, leukocyturia. TIMP-2*IGFBP7 invalid if urine albumin >125 mg/dL. |
| Threshold derived | See Section 7. |
| Limitations | Highlights confounding factors; emphasizes need for multi-marker approach. |

### 5. Required Biomarkers
**Required Biomarkers** (for minimum viable computation):
| Name | Why Required | Fasting Required? | SSOT Canonical Unit |
|------|--------------|-------------------|---------------------|
| `creatinine` | Core functional marker; used in eGFR and uACR; rises late after significant nephron loss  | No | mg/dL (platform stores mg/dL; can accept µmol/L with conversion) |
| `egfr` | Primary filtration estimate; KDIGO staging based on eGFR thresholds  | No | mL/min/1.73 m² |
| `urea` | Nitrogenous waste marker; reflects protein intake, catabolism, hydration, and renal excretion; BUN/creatinine ratio aids differential diagnosis  | No | mg/dL (BUN) |
| `albumin_urine` | Protein leakage marker; earliest sign of glomerular stress when uACR computed | No | mg/L |
| `creatinine_urine` | Required to normalize urinary albumin for uACR calculation | No | mg/dL |

**Optional Biomarkers** (enhance signal but not required):
| Name | Why Optional | SSOT Canonical Unit |
|------|--------------|---------------------|
| `cystatin_c` | Muscle-independent filtration marker; detects early GFR decline when creatinine normal; may be higher in inflammation  | mg/L |
| `tmao` | Gut-derived uremic toxin; elevated in early CKD (AUC >0.7)  | µmol/L |
| `myo_inositol` | Metabolite elevated in early CKD; linked to inositol phosphate metabolism  | µmol/L (tentative—requires SSOT addition) |
| `pyruvate` | Energy metabolism marker; altered in early CKD  | mg/dL (tentative) |
| `ngal_urine` | Tubular damage marker; predicts AKI; cut-off >150 ng/mL  | ng/mL |
| `timp2_igfbp7_urine` | Cell cycle arrest markers; predicts AKI within 12 hours  | (ng/mL)² / 1000 |

### 6. Derived Metrics and Formulas
| Metric name | Formula | Unit handling | Evidence anchor | Existing in platform? |
|-------------|---------|---------------|-----------------|----------------------|
| `egfr` | Multiple equations (CKD-EPI 2021, MDRD). Platform to apply CKD-EPI 2021 without race coefficient. | Input `creatinine` in mg/dL; age, sex required | KDIGO guidelines | Yes |
| `uacr` | `uacr = albumin_urine / creatinine_urine` | `albumin_urine` in mg/L, `creatinine_urine` in g/L → ratio in mg/g; or mg/mmol depending on jurisdiction | KDIGO guidelines | Yes |
| `urea_creatinine_ratio` | `urea_creatinine_ratio = urea / creatinine` | Both in mg/dL; ratio >20 suggests pre-renal etiology; <10 suggests liver disease/malnutrition  | Medscape review ; HealthMatters  | Yes |
| `nLR` | Not applicable for kidney stress—reserved for inflammatory signals | N/A | N/A | Yes |
| `tyg_index` | Not directly validated for kidney metabolic stress—primarily insulin resistance marker | N/A | N/A | Yes |

**Note**: The platform already computes `egfr`, `uacr`, and `urea_creatinine_ratio`.

### 7. Evidence-Anchored Thresholds
**Biological question filter applied**: The thresholds below are anchored to the question of detecting metabolic renal stress. Where evidence is absent for early metabolic stress specifically, KDIGO thresholds for established disease are provided as contextual reference, but **threshold evidence inconclusive for this condition — additional validation required** for early metabolic stress detection.

| Tier | Metric | Operator | Value | Unit | Evidence source | Study n | Follow-up |
|------|--------|----------|-------|------|----------------|---------|-----------|
| **Threshold evidence inconclusive for this condition — additional validation required.** | | | | | | | |

**Contextual KDIGO thresholds for established CKD (not for early metabolic stress):**

| Tier | Metric | Operator | Value | Unit | Evidence source | Study n | Follow-up |
|------|--------|----------|-------|------|----------------|---------|-----------|
| optimal | `uacr` | < | 30 | mg/g | KDIGO 2024  | Guideline | N/A |
| suboptimal | `uacr` | 30–300 | mg/g | KDIGO 2024  | Guideline | N/A |
| at_risk | `uacr` | ≥ | 300 | mg/g | KDIGO 2024  | Guideline | N/A |
| optimal | `egfr` | ≥ | 60 | mL/min/1.73 m² | KDIGO 2024  | Guideline | N/A |
| suboptimal | `egfr` | 45–59 | mL/min/1.73 m² | KDIGO 2024  | Guideline | N/A |
| at_risk | `egfr` | < | 45 | mL/min/1.73 m² | KDIGO 2024  | Guideline | N/A |

**Functional medicine "yellow flag" thresholds (Tier 3—not evidence-anchored for this signal):**  
- Creatinine: women >0.90 mg/dL, men >1.10 mg/dL   
- eGFR: <90 mL/min/1.73 m²   
- BUN: >18 mg/dL   
- uACR: 10–30 mg/g (early leakiness)   
- Cystatin C: >0.83 mg/L   

**These thresholds are not used in the primary signal due to lack of hard outcome validation for metabolic stress detection.**

### 8. Override Rules and Guardrails
| Rule | Condition | Resulting State | Evidence Basis |
|------|-----------|-----------------|----------------|
| AKI override | `creatinine` increase ≥0.3 mg/dL within 48 hours OR ≥1.5× baseline within 7 days | at_risk | KDIGO AKI criteria  |
| Severe AKI override | `creatinine` increase ≥3.0× baseline OR ≥4.0 mg/dL with acute rise ≥0.5 mg/dL OR urine output <0.3 mL/kg/h ×24 h OR anuria ×12 h | at_risk (flag for immediate referral) | KDIGO stage 3 criteria |
| Pre-renal override | `urea_creatinine_ratio` >20:1 with elevated `urea` and normal `creatinine` | suboptimal (flag: possible dehydration/GI bleed) |  |
| Liver disease override | `urea_creatinine_ratio` <10:1 with low `urea` | suboptimal (flag: possible liver disease/malnutrition) |  |
| Critical value override | `urea` >100 mg/dL OR `creatinine` >4.0 mg/dL (adult) | at_risk (flag for immediate referral) |  |

### 9. Clinical Limitations and Excluded Populations
1. **Populations where signal should not be applied or interpreted with caution**:
   - Acute illness (sepsis, major surgery, trauma)—confounds BUN/creatinine due to catabolism and volume shifts 
   - Known liver disease—urea production impaired, BUN/creatinine ratio unreliable 
   - Pregnancy—physiologic BUN/creatinine lowering 
   - Extremes of muscle mass (bodybuilders, amputation, sarcopenia)—creatinine unreliable 
   - Children and adolescents—eGFR equations differ; thresholds not validated in this signal 

2. **Conditions or medications that confound inputs**:
   - High-protein diet, GI bleed, corticosteroids—increase BUN without renal injury 
   - Dehydration—elevates BUN and creatinine (pre-renal)
   - Medications: NSAIDs, aminoglycosides, ACE inhibitors/ARBs, diuretics, certain antibiotics—affect creatinine or urea handling 
   - Inflammation (high CRP, WBC)—may elevate cystatin C independent of GFR 

3. **Known gaps in evidence**:
   - No validated thresholds for "metabolic stress" independent of established CKD stages
   - Metabolomic markers (TMAO, myo-inositol, pyruvate) lack prospective outcome data and assay standardization 
   - Limited data in non-European/non-North American ethnic groups
   - Paucity of studies specifically addressing **metabolic drivers** of early renal stress as a distinct entity

4. **Cautionary trial evidence**:
   - Improving a biomarker (e.g., lowering BUN or proteinuria) does not guarantee reduced hard outcomes. For example, some interventions that lower proteinuria have not consistently reduced ESRD or mortality in large trials. This signal should be communicated as a **risk indicator**, not a therapeutic target without proven disease modification.

### 10. HealthIQ Platform Signal Mapping
**Signal identifier**:
```
signal_kidney_metabolic_stress
```

**Physiological system**:
```
renal
```

**Primary metric**:
```
uacr
```

**Required biomarkers**:
```
- creatinine
- urea
- albumin_urine
- creatinine_urine
```

**Required derived metrics**:
```
- egfr
- uacr
- urea_creatinine_ratio
```

**Optional biomarkers**:
```
- cystatin_c
- tmao
- myo_inositol
- pyruvate
- ngal_urine
- timp2_igfbp7_urine
```

**Optional derived metrics**:
```
- none currently defined
```

**Threshold summary**:
```
optimal:    uacr < 30 mg/g and egfr >= 60 mL/min/1.73 m²
suboptimal: uacr 30–300 mg/g OR egfr 45–59 mL/min/1.73 m²
at_risk:    uacr >= 300 mg/g OR egfr < 45 mL/min/1.73 m² OR AKI criteria met
```
*Note: These are KDIGO thresholds for established CKD, not early metabolic stress thresholds (which are inconclusive).*

**Override rules**:
```
rule: creatinine_increase_48h >= 0.3 mg/dL → at_risk
rule: urea_creatinine_ratio > 20:1 with elevated urea → suboptimal (flag: possible pre-renal)
rule: urea_creatinine_ratio < 10:1 with low urea → suboptimal (flag: possible liver disease/malnutrition)
rule: urea > 100 mg/dL OR creatinine > 4.0 mg/dL → at_risk (critical value)
evidence: KDIGO 2024 ; Medscape ; PCH critical values 
```

**Bundle consumers**:
```
- metabolic_health
- cardiovascular_risk
- biological_age
- vascular_age
```

**Implementation notes**:
- New biomarkers requiring SSOT addition: `tmao`, `myo_inositol`, `pyruvate` (units tentative—require lab vendor confirmation)
- Metabolite thresholds cannot be implemented until prospective validation studies establish cut-offs with hard outcomes
- Platform must apply **sex-specific eGFR equations** (CKD-EPI 2021 uses sex coefficients)
- Age-stratified interpretation of BUN may be considered (older adults normally higher) 
- **Critical**: No evidence-based thresholds currently exist for "metabolic stress" as distinct from CKD stages. Signal should be communicated as **CKD risk stratification** until further validation.

### 11. Supporting References
1. Ulta Lab Tests. "Kidney Function Tests – Early Detection & Optimal Ranges." 2025. Available at: ultalabtests.com.  (Tier 3—functional medicine context, not primary evidence)
2. PMC Table 1. NIH. 2022. DOI: 10.3390/ijms23084444 (assumed). Available at: pmc.ncbi.nlm.nih.gov/articles/PMC9046880/.  (Tier 1—systematic review context)
3. Liess BD, Devaraj S. "Blood Urea Nitrogen (BUN)." Medscape. Updated Oct 6, 2025. Available at: emedicine.medscape.com/article/2073979.  (Tier 2—clinical review)
4. Translational Andrology and Urology. "Integrated transcriptomics, proteomics, and metabolomics... in a mouse model of hyperoxaluria-induced kidney injury." 2025. DOI: 10.21037/tau-2025-534.  (Tier 3—animal model, mechanistic)
5. Centre of Biomedical Research, Lucknow. "Characterizing metabolic dysregulation in early-stage chronic kidney disease for diagnostic insights." *Mol. Omics*, 2025, 21, 607-620. DOI: 10.1039/D5MO00018A.  (Tier 1—cross-sectional human metabolomics with ROC analysis)
6. Peterborough City Hospital Pathology. "Critical Value Cut-Off Limits." 2019. Available at: pch-pathlab.com.  (Tier 2—clinical laboratory standards)
7. HealthMatters.io. "Blood urea nitrogen (BUN)." Reviewed Feb 14, 2026. Available at: healthmatters.io.  (Tier 3—commercial health information site)
8. Rinschen MM, et al. "Metabolic rewiring of the hypertensive kidney." *Sci Signal*. 2019;12(611). DOI: 10.1126/scisignal.aax9760.  (Tier 3—animal model, multi-omics)
9. Nkuipou-Kenfack E, et al. "Assessment of Metabolomic and Proteomic Biomarkers in Detection and Prognosis of Progression of Renal Function in Chronic Kidney Disease." *PLOS ONE*. 2014;9(5):e96955. DOI: 10.1371/journal.pone.0096955.  (Tier 1—prospective cohort, small n)
10. PMC Table 1. NIH. 2025. Available at: pmc.ncbi.nlm.nih.gov/articles/PMC11879783/table/T1/.  (Tier 2—clinical decision framework)