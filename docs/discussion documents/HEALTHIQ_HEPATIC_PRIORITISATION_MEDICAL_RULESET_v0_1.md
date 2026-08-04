---
document_id: HEALTHIQ-HEPATIC-RULESET-001
title: HealthIQ Hepatic Prioritisation Medical Ruleset
version: "0.1"
status: DRAFT_FOR_HMR_RECONCILIATION
governing_policy: HEALTHIQ-CLIN-PRIORITY-CONTRACT-001 v0.3
author_role: Independent hepatic-domain medical research reviewer
implementation_status: NOT_AUTHORISED
scope: Adults aged 18 and over. Paediatric, neonatal and pregnancy hepatic interpretation are explicitly out of scope.
---

# HealthIQ Hepatic Prioritisation Medical Ruleset v0.1

## 0. Scope note and one procedural flag

### 0.1 Governing scope

**`HEALTHIQ_HEPATIC_CLINICAL_PRIORITISATION_PILOT_SPEC_v0.1.md` was named as the governing scope but was not present in the uploads.** Only contract v0.3 was supplied. The scope of this ruleset has therefore been taken from the fourteen items enumerated in the commissioning instruction and from contract v0.3 §21.1.

The practical consequence is confined to §13. The instruction requires "all required acceptance scenarios", and "required" implies a set defined in the pilot spec that I cannot see. The scenarios in §13 are derived from contract v0.3 §19, from the challenge cases in the earlier independent review, and from the failure modes this ruleset creates. **They must be reconciled against the pilot spec's own list before sign-off.** Everything else in this document is derivable from the contract and the evidence base and should not be affected.

### 0.2 Evidence labelling

| Tag | Meaning |
|---|---|
| `[E]` | Evidence-supported rule — traceable to a cited guideline or authoritative source |
| `[C]` | Accepted clinical convention — widely practised, not a graded guideline recommendation |
| `[J]` | HealthIQ clinical judgement — a product-safety decision made in the absence of directly applicable evidence |
| `[U]` | Unresolved question — requires Head of Medical Research adjudication before release |

Contract v0.3 §13 requires every override to be attributable to a named clinical rule with a cited source *or* documented clinical adjudication. Every `[J]` item in this document is therefore a documented-adjudication candidate and must be signed off individually, not accepted as a block.

### 0.3 Contract compliance statement

This ruleset was written against contract v0.3 clauses: §3.1 (consolidated finding as unit), §4.3 (significance assessed as-characterised), §4.5 (confidence excluded from prominence), §6.1 (tier algebra, floor rule, one-tier promotion cap), §8 (supporting-marker policy), §9 (frame consolidation before tiering), §12.1/12.2 (change-defined vs change-modified), §13 (override discipline), §16 (no-concern and insufficient-data outputs).

---

## 1. The central clinical tension in this domain

This must be read before any rule below, because it determines whether the entire severity-band structure is being used correctly.

The BSG guideline on the management of abnormal liver blood tests makes two recommendations that sit awkwardly against a graded prioritisation model:

- <cite index="79-1">Recommendation 3 states that the extent of liver blood test abnormality is not necessarily a guide to clinical significance, which is instead determined by the specific analyte that is abnormal and by the clinical context (level 5, grade D)</cite>. `[E]`
- <cite index="79-1">Recommendation 4 states that patients with abnormal liver blood tests should be considered for investigation with a liver aetiology screen irrespective of level and duration of abnormality, where abnormal means outside the laboratory reference range (level 2b, grade B)</cite>. `[E]`

The guideline supports this with concrete counterexamples: a patient with acute hepatitis A may have ALT above 1000 U/L and be well ten years later, while a patient with hepatitis C may have ALT inside the reference interval and progress to end-stage disease; and the commonest causes of chronic liver disease in the UK — steatotic liver disease, alcohol-related liver disease and hepatitis C — are frequently associated with only mild or moderate biochemical abnormality. <cite index="79-1">The guideline also notes that current upper limits of normal for ALT may be too high, probably because people with occult fatty liver disease were included in the populations used to derive them</cite>. `[E]`

**Implication for HealthIQ.** Severity bands in this domain are legitimate for setting **urgency and prominence**. They are **not** legitimate for deciding whether a finding warrants clinical attention at all. UK evidence says that any liver analyte outside the reference range warrants consideration for an aetiology screen. Two rules follow, and they are the most consequential decisions in this document:

**HEP-PRINCIPLE-1 `[E]`** — Magnitude sets urgency and prominence, never eligibility. A mild ALT elevation is not a lesser *kind* of finding than a marked one; it is the same finding with lower urgency.

**HEP-PRINCIPLE-2 `[J]`, derived from `[E]`** — The tier floor for any confirmed out-of-range core hepatic analyte on a person's first HealthIQ panel is **Tier 1**, not Tier 2. Tier 2 is available only where a governed rule supplies a reason to expect no yield from investigation (§10.3).

**This is the primary reconciliation item.** HEP-PRINCIPLE-2 is clinically the most defensible reading of BSG Recommendation 4, but it will place a large fraction of hepatic findings in Tier 1. The BSG guideline reports that of 130,849 liver blood test requests received by one UK trust in a year, <cite index="79-1">around 30% contained at least one result outside the stated reference range</cite>, while <cite index="79-1">in the BALLETS primary-care cohort fewer than 5% of adults with abnormal liver blood tests had a specific liver disease, and only 1.3% had a specific liver disease requiring immediate treatment</cite>. `[E]`

So the honest position is: the evidence supports investigating, and simultaneously shows that most investigation is negative. A consumer product that faithfully implements Recommendation 4 will generate a high Tier 1 volume with a low positive yield. That is a defensible clinical stance and an uncomfortable product one.

**`[U]` HEP-U1 — the Head of Medical Research must decide** whether HealthIQ adopts the BSG position (Tier 1 floor, high volume, high fidelity) or a modified position that reserves Tier 1 for a defined magnitude or pattern and places minimal isolated elevations in Tier 2 with recheck advice. The second option is a deliberate, documented departure from a grade B recommendation and must be recorded as such under contract §13, not adopted silently for volume reasons.

Contract v0.3 §15.2 Tier 1 volume control is therefore load-bearing for this domain specifically. If HEP-PRINCIPLE-2 is adopted, the presentation-density rule is what makes it usable.

---

## 2. Hepatic finding taxonomy

Per contract §3.1, the unit is the consolidated clinical finding. The following are the hepatic finding types this ruleset recognises. Each is a candidate concern; none is a signal frame.

### 2.1 Pattern-level findings (primary)

| ID | Finding | Constituents | Notes |
|---|---|---|---|
| HEP-F1 | Hepatocellular liver injury pattern | ALT ± AST, with ALP for R-value | The transaminase-predominant pattern `[E]` |
| HEP-F2 | Cholestatic liver injury pattern | ALP ± GGT ± bilirubin | ALP-predominant `[E]` |
| HEP-F3 | Mixed liver injury pattern | ALT and ALP both raised, R between 2 and 5 | `[C]` |
| HEP-F4 | Hepatic synthetic dysfunction | Albumin, INR, bilirubin, platelets | <cite index="79-1">Bilirubin, albumin and INR convey information on liver function; platelets convey information on the level of fibrosis</cite> `[E]` |
| HEP-F5 | Suspected advanced fibrosis / chronic liver disease | AST:ALT ratio, platelets, FIB-4 where computable | `[E]` |
| HEP-F6 | Isolated hyperbilirubinaemia | Bilirubin alone, all other hepatic analytes normal | Gilbert's pattern `[E]` |
| HEP-F7 | Isolated raised ALP | ALP alone, GGT normal or absent | Often non-hepatic `[E]` |
| HEP-F8 | Isolated raised GGT | GGT alone | Low specificity, prognostically non-trivial `[E]` |
| HEP-F9 | Non-classifiable hepatic abnormality | Any abnormal hepatic analyte where pattern cannot be determined from available markers | Created rather than defaulting to a pattern `[J]` |

### 2.2 Composite / override findings

| ID | Finding | Trigger |
|---|---|---|
| HEP-F10 | Hepatocellular injury with hyperbilirubinaemia (Hy's law pattern) | See §3.2 |
| HEP-F11 | Liver injury with synthetic failure | See §3.2 |
| HEP-F12 | Possible iron overload in hepatic context | Ferritin with transferrin saturation — see §11 |

### 2.3 Consolidation rules (contract §9)

**HEP-CONS-1 `[J]`** — ALT, AST, ALP, GGT and bilirubin do not generate independent concerns when they form a recognised pattern. They consolidate into a single HEP-F1/F2/F3 finding. A panel with ALT 250, ALP 46 and normal bilirubin produces **one** concern, not three.

**HEP-CONS-2 `[J]`** — Aetiological frames over a single hepatic pattern (alcohol-related, metabolic/steatotic, viral, autoimmune, drug-induced, iron-related) consolidate into one finding with alternative interpretations. They meet contract §9.3's separation test only where the initial action set genuinely diverges. It generally does not: <cite index="79-1">BSG Recommendation 5 specifies a single standard liver aetiology screen — abdominal ultrasound, hepatitis B surface antigen, hepatitis C antibody with follow-on PCR, anti-mitochondrial antibody, anti-smooth muscle antibody, antinuclear antibody, serum immunoglobulins, and simultaneous serum ferritin and transferrin saturation</cite> — which is common to all of these aetiologies `[E]`. One pattern, one screen, one concern.

**HEP-CONS-3 `[J]`** — Per contract §9.4, a consolidated hepatic finding inherits the highest urgency and severity among its constituents. A panel with mild ALT elevation and marked ALP elevation inherits the marked band.

---

## 3. Urgency rules

Urgency answers "how soon", and per contract §6.1 it sets a tier floor that nothing may lower. Urgency in this domain is **not** a function of magnitude alone; the synthetic-function and combination rules matter more than the enzyme level.

### 3.1 Tier 0 urgency criteria (prompt clinical review)

Subject to contract §17 — no Tier 0 output may be released until the operational escalation pathway is defined and ratified.

| ID | Criterion | Basis |
|---|---|---|
| HEP-U0-1 | ALT or AST ≥10× ULN | NHS Devon abnormal-LFT referral guidance directs telephone contact with the on-call gastroenterologist at ALT greater than 10× ULN `[E]` |
| HEP-U0-2 | ALT or AST >1000 U/L in absolute terms | <cite index="6-1">NHS Specialist Pharmacy Service guidance states that marked elevations of ALT or AST above 1000 IU/L suggest drug-induced liver injury, acute viral hepatitis, ischaemic or autoimmune hepatitis and may require referral to secondary care</cite>. Retained alongside HEP-U0-1 because ULN varies between laboratories and the absolute value carries an independent differential `[E]` |
| HEP-U0-3 | Hy's law pattern: ALT or AST ≥3× ULN **and** total bilirubin ≥2× ULN **and** ALP <2× ULN | The hepatocellular-plus-jaundice combination carries the highest mortality risk in DILI and is the basis of Hy's law `[E]`, international source `[C]` in UK terms |
| HEP-U0-4 | Any abnormal hepatic analyte **and** albumin below the laboratory lower reference limit | <cite index="6-1">NHS SPS guidance directs referral of any patient with low albumin and abnormal liver blood tests to secondary care or a liver specialist</cite> `[E]` |
| HEP-U0-5 | Any abnormal hepatic analyte **and** INR >1.5 in a person not on anticoagulation | <cite index="6-1">Jaundice, low albumin or prolonged INR are identified as signs of synthetic liver failure warranting urgent referral</cite> `[E]`. INR >1.5 is the accepted coagulopathy threshold in acute liver failure definitions `[C]` |
| HEP-U0-6 | New conjugated hyperbilirubinaemia at jaundice-range levels with abnormal hepatic enzymes | <cite index="79-1">BSG states that unexplained clinical jaundice or suspicion of possible hepatic or biliary malignancy should lead to an immediate referral</cite> `[E]`. See HEP-U2 below on the jaundice-range threshold |

**`[U]` HEP-U2 — bilirubin jaundice threshold.** UK guidance frames this clinically ("clinical jaundice"), not biochemically. Clinical jaundice is conventionally visible above roughly 40–50 µmol/L, but HealthIQ has no clinical observation and this figure is a convention rather than a guideline threshold. The Head of Medical Research must set the numeric bilirubin value at which HEP-U0-6 fires, and must decide whether it fires on total bilirubin where the conjugated fraction is unavailable. The safe default pending that decision is to fire on total bilirubin and state explicitly that the conjugated fraction was not measured.

### 3.2 Explicit non-urgency rules

**HEP-U-NEG-1 `[E]`** — Magnitude of transaminase elevation below the HEP-U0 thresholds does not by itself generate urgency. BSG Recommendation 3 is directly on point: extent of abnormality is not necessarily a guide to clinical significance.

**HEP-U-NEG-2 `[E]`** — Isolated raised bilirubin with all other hepatic analytes normal does not generate urgency. <cite index="79-1">Where the majority of elevated bilirubin is unconjugated and haemolysis is absent, the cause is virtually always Gilbert's syndrome, which is not associated with liver disease or ill health, and such individuals should be fully reassured</cite>. Caveat: <cite index="79-1">where unconjugated bilirubin is more markedly elevated, above 40 µmol/L, rarer causes such as Crigler-Najjar syndrome should be considered</cite>.

**HEP-U-NEG-3 `[E]`** — Isolated raised ALP with normal GGT does not generate hepatic urgency. <cite index="79-1">When ALP is elevated in isolation, GGT measurement can indicate whether the ALP is of hepatic or non-hepatic origin; the commonest cause of an isolated raised ALP is likely to be vitamin D deficiency, with other causes including Paget's disease and bony metastases</cite>.

---

## 4. Severity bands

Per §1, these bands govern urgency contribution and prominence, not eligibility.

### 4.1 ALT severity bands `[J]`, thresholds sourced individually

| Band | Range | Source of the boundary |
|---|---|---|
| HEP-S0 | ≤ ULN | Reference interval. Note the BSG caveat that ALT ULN may be set too high `[E]` |
| HEP-S1 — mild | >ULN to <3× ULN | Lower bound from BSG Rec 4 (abnormal = outside reference range) `[E]`; upper bound from the 3× ULN level widely used in UK statin-monitoring and DILI-signal practice `[E]` |
| HEP-S2 — moderate | ≥3× to <5× ULN | 3× ULN is associated with greater risk of significant liver injury in the statin-monitoring literature `[E]` |
| HEP-S3 — marked | ≥5× to <10× ULN | <cite index="84-1">EASL DILI guidance designates liver injury hepatocellular at a 5-fold or higher rise in ALT alone</cite>; 5× ULN is also the standard hepatic-safety signal threshold in regulated monitoring `[E]`, international `[C]` |
| HEP-S4 — severe | ≥10× ULN, or >1000 U/L absolute | NHS Devon 10× rule and NHS SPS >1000 U/L differential `[E]` |

### 4.2 AST severity bands `[J]`

Identical numeric bands to ALT, with two mandatory modifiers:

**HEP-AST-1 `[E]`** — AST is less liver-specific. <cite index="79-1">AST is abundantly present in skeletal, cardiac and smooth muscle and so may be elevated in patients with myocardial infarction or myositis</cite>. Where AST is raised disproportionately to ALT and no hepatic pattern is otherwise supported, the finding must carry a non-hepatic-source caveat and, per contract §4.5, this reduces interpretive confidence only — it does not reduce severity or tier.

**HEP-AST-2 `[E]`** — AST may be the more sensitive indicator in some contexts. <cite index="79-1">The concentration of AST may be a more sensitive indicator of liver injury in conditions such as alcohol-related liver disease and in some cases of autoimmune hepatitis</cite>.

### 4.3 ALP handling `[E]`

| Band | Range |
|---|---|
| HEP-ALP-0 | ≤ ULN |
| HEP-ALP-1 — mild | >ULN to <2× ULN |
| HEP-ALP-2 — significant | ≥2× ULN — the threshold at which DILI convention designates cholestatic injury `[C]` |

Mandatory ALP modifiers:

- **HEP-ALP-M1 `[E]`** — ALP is not liver-specific. <cite index="79-1">ALP is produced mainly in the liver but is also found in abundance in bone and in smaller quantities in the intestines, kidneys and white blood cells; levels are physiologically higher in childhood and in pregnancy due to placental production</cite>.
- **HEP-ALP-M2 `[E]`** — Where GGT is available and normal alongside raised ALP, hepatic origin is not supported and the finding is reclassified from HEP-F2 to HEP-F7.
- **HEP-ALP-M3 `[J]`** — Where GGT is absent, ALP origin is undetermined. The finding must state this. It must not be presented as hepatic by default and must not be suppressed. Per contract §4.5 this affects wording, not tier.

### 4.4 GGT handling `[E]`

GGT is the analyte in this domain where evidence most clearly separates diagnostic value from prognostic value, and the ruleset must reflect both.

- **HEP-GGT-1 `[E]`** — Diagnostically weak in isolation. <cite index="79-1">GGT is most commonly elevated as a result of obesity, excess alcohol consumption or drug induction, and has low specificity for liver disease</cite>.
- **HEP-GGT-2 `[E]`** — Prognostically meaningful. <cite index="79-1">An elevated GGT is one of the best predictors of liver mortality, and a raised GGT is associated with increased liver as well as all-cause mortality, with the greatest risk in those with the most significant elevations</cite>.
- **HEP-GGT-3 `[E]`** — A specific threshold exists in the alcohol pathway. <cite index="79-1">For patients drinking below the harmful thresholds, if GGT is elevated above 100 U/L then consideration should be given to an assessment of liver fibrosis, as for the higher-risk group</cite>.
- **HEP-GGT-4 `[J]`** — Isolated raised GGT (HEP-F8) is assigned Tier 2 by default, promoted to Tier 1 where GGT >100 U/L or where any other hepatic analyte is abnormal. The default Tier 2 reflects HEP-GGT-1; the promotion reflects HEP-GGT-2 and HEP-GGT-3. **This is a deliberate exception to HEP-PRINCIPLE-2** and is flagged as such for adjudication.

### 4.5 Prohibited severity behaviour

**HEP-S-PROHIB-1** — No universal ULN-multiple severity formula may be applied across hepatic analytes. ALT at 3× ULN and ALP at 3× ULN are not equivalent findings. Contract §4.2 and §18.4.

**HEP-S-PROHIB-2** — Severity must not be lowered because AST, GGT, bilirubin, albumin or INR are absent. Contract §8, §18.3.

---

## 5. R-value rules

### 5.1 Calculation `[C]`

R = (ALT ÷ ALT ULN) ÷ (ALP ÷ ALP ULN), using the reporting laboratory's own reference limits.

<cite index="80-1">Cases are categorised by R value into hepatocellular (R ≥ 5), mixed (2 < R < 5), and cholestatic (R ≤ 2) profiles</cite>. <cite index="84-1">EASL applies the same structure, designating injury hepatocellular where the ALT:ALP activity ratio is 5 or more, cholestatic where it is 2 or less, and mixed between 2 and 5</cite>.

### 5.2 Evidence-status warning — read before use

**The R-value is a DILI causality-assessment convention from international hepatology guidance. It is not a UK primary-care guideline instrument.** The BSG guideline classifies patterns qualitatively — <cite index="79-1">"predominantly raised ALP and GGT indicate cholestasis" and "predominantly raised ALT and AST indicate hepatocellular liver injury"</cite> — and does not specify a numeric R threshold. `[E]` for the qualitative classification; `[C]` for the numeric cutoffs.

Two consequences:

**HEP-R-1 `[J]`** — R-value may be used to classify pattern and to select explanation content. It may not, on its own, set urgency or severity. Pattern classification is a *what kind* judgement, not a *how serious* one. An R of 12.9 tells you the injury is hepatocellular; it tells you nothing about magnitude, which is carried entirely by the ALT band.

**HEP-R-2 `[J]`** — The R-value must not be surfaced to a consumer as a headline number. It is an internal classifier. Presenting "R = 12.9" to a lay reader implies a precision and a clinical standing the value does not have outside DILI causality assessment.

### 5.3 Computability rules `[J]`

- R requires both ALT and ALP with their reference limits. If either is missing, R is **not computed** and the finding is classified HEP-F9 (non-classifiable), not defaulted to hepatocellular.
- R is meaningful only when at least one of ALT or ALP is abnormal. R computed from two normal values is noise and must be suppressed.
- Where AST is present and ALT is absent, AST may substitute in the numerator, with a recorded reduction in interpretive confidence `[C]` — AASLD guidance describes the ratio using ALT or AST in the numerator.

---

## 6. Synthetic-function modifiers

<cite index="79-1">BSG is explicit that hepatobiliary enzymes convey information on the level of ongoing injury, whereas bilirubin, albumin and INR convey information on liver function, with platelets conveying information on the level of fibrosis</cite>. `[E]`

This distinction is the single most important structural point in hepatic prioritisation: **enzymes tell you about injury, synthetic markers tell you about function, and function outranks injury.**

### 6.1 Albumin

| Rule | Effect | Basis |
|---|---|---|
| HEP-ALB-1 | Albumin below LRL + any abnormal hepatic analyte → Tier 0 (HEP-U0-4) | NHS SPS referral direction `[E]` |
| HEP-ALB-2 | Low albumin must carry a non-hepatic-cause caveat | <cite index="79-1">Albumin concentrations are reduced in many clinical situations, including sepsis, systemic inflammatory disorders, nephrotic syndrome, malabsorption and gastrointestinal protein loss; overinterpretation of albumin as a marker of severity of liver disease is not always merited</cite> `[E]` |
| HEP-ALB-3 | Albumin absent → synthetic function not assessed; must be stated (§7) | Contract §16.2 `[J]` |

### 6.2 INR

| Rule | Effect | Basis |
|---|---|---|
| HEP-INR-1 | INR >1.5 without anticoagulation + abnormal hepatic analyte → Tier 0 (HEP-U0-5) | `[E]` / `[C]` |
| HEP-INR-2 | Anticoagulant use, where known, suppresses HEP-INR-1 but must be stated, not silently applied | Contract §13 `[J]` |
| HEP-INR-3 | Raised INR must carry a vitamin K caveat | <cite index="79-1">A prolonged PT/INR can also be caused by vitamin K deficiency as seen in fat malabsorption and chronic cholestasis</cite> `[E]` |
| HEP-INR-4 | INR is rarely present on consumer panels. Its absence must not reduce the severity or tier of any hepatic finding | Contract §8 `[J]` |

### 6.3 Bilirubin

- **HEP-BIL-1 `[E]`** — Raised bilirubin with raised transaminases is a materially different finding from isolated raised bilirubin. The former contributes to HEP-U0-3 and HEP-U0-6; the latter is HEP-F6.
- **HEP-BIL-2 `[E]`** — Split bilirubin governs interpretation. Predominantly unconjugated without anaemia → Gilbert's pattern, reassurance appropriate. Where the split is unavailable, the finding must state that the conjugated fraction was not measured and must not assert Gilbert's.
- **HEP-BIL-3 `[E]`** — Isolated raised bilirubin with anaemia requires haemolysis to be considered. <cite index="79-1">If the patient is anaemic, haemolysis needs to be excluded by requesting reticulocyte count, lactate dehydrogenase and haptoglobin</cite>. This converts HEP-F6 from a Tier 2 reassurance finding to a Tier 1 combination finding.

### 6.4 Platelets

- **HEP-PLT-1 `[E]`** — Platelets are a fibrosis indicator in the hepatic context. <cite index="79-1">Thrombocytopenia is the most common haematological abnormality in patients with chronic liver disease and is an indicator of advanced disease</cite>.
- **HEP-PLT-2 `[J]`** — Low platelets **with** abnormal hepatic analytes generates HEP-F5 (suspected advanced fibrosis) as a distinct Tier 1 finding. It does not merely annotate HEP-F1.
- **HEP-PLT-3 — boundary rule `[J]`** — Where the platelet count independently meets haematological Tier 0 or Tier 1 criteria, contract §4.8 forbids assigning it contextual role. Severe thrombocytopenia is a haematological finding in its own right; the hepatic ruleset may reference it but may not absorb it. **Cross-domain dependency: the haematology pilot must define these thresholds. Until it does, HealthIQ must not consolidate a low platelet count into a hepatic finding.** `[U]` HEP-U3.

### 6.5 AST:ALT ratio and FIB-4

- **HEP-FIB-1 `[E]`** — <cite index="79-1">An AST:ALT ratio of >1 indicates advanced fibrosis or cirrhosis, and the utility of the ratio persists even if both values are within the normal reference interval</cite>. This is a direct evidential basis for contract §3.1's in-range-findings rule: a hepatic finding may be created from two normal values.
- **HEP-FIB-2 `[E]`** — FIB-4 = (age × AST) ÷ (platelets × √ALT). <cite index="79-1">A low FIB-4 is below 1.3 for those aged under 65 or below 2.0 for those over 65; indeterminate is 1.3 to 3.25; patients with FIB-4 above 3.25 should be considered for referral to a specialist clinic irrespective of second-line tests</cite>.
- **HEP-FIB-3 `[J]`** — FIB-4 requires age, AST, ALT and platelets. It is computed only when all four are present with a valid age. Where computable and above the age-adjusted threshold, it generates HEP-F5 at Tier 1. Where not computable, HealthIQ must state that fibrosis risk could not be assessed rather than omit the topic — the guideline is emphatic that normal enzymes do not exclude advanced fibrosis.
- **HEP-FIB-4 `[E]`** — <cite index="79-1">Both AST and ALT can be normal even in the setting of cirrhosis</cite>. This must be reflected in no-concern output (§12).

---

## 7. Missing-marker rules

Per contract §8 and §18.3, absence reduces confidence only.

| Missing marker | Effect on confidence | Effect on severity/tier | Required output |
|---|---|---|---|
| AST | Reduced — AST:ALT ratio unavailable, so fibrosis signal and alcohol-pattern discrimination are lost, and the ALT elevation cannot be cross-checked against a second transaminase | **None** | State that AST was not measured; recommend it. BSG notes reflex AST testing following an abnormal ALT is desirable `[E]` |
| ALP | Reduced — R not computable, pattern not classifiable | **None** | Classify as HEP-F9; state pattern undetermined |
| GGT | Reduced — ALP hepatic origin undetermined; alcohol/induction signal lost | **None** | State GGT not measured |
| Bilirubin | Reduced | **None**, but HEP-U0-3 and HEP-U0-6 cannot be evaluated | Must state that the jaundice and Hy's-law criteria could not be assessed — contract §12.1 pattern applied to combination rules `[J]` |
| Albumin | Reduced | **None**, but HEP-U0-4 cannot be evaluated | Must state that synthetic function was not assessed |
| INR | Reduced | **None**, but HEP-U0-5 cannot be evaluated | Must state |
| Platelets | Reduced | **None**, but FIB-4 not computable | Must state that fibrosis risk was not assessed |

**HEP-MISS-1 `[J]`** — Where any Tier 0 combination criterion cannot be evaluated because a constituent is absent, HealthIQ must not state or imply that the criterion was not met. The required formulation is that it could not be assessed. This is contract §12.1's not-assessable rule generalised from change-defined criteria to combination-defined criteria, and is proposed as a contract amendment candidate.

**HEP-MISS-2 `[J]`** — Missing markers generate a *recommended additional tests* output attached to the finding, per contract §10 (confidence may control missing-test recommendations). For a hepatocellular pattern the recommendation set is the BSG standard liver aetiology screen `[E]`, presented as tests to discuss with a clinician rather than tests the user should self-arrange.

---

## 8. Trend and baseline rules

### 8.1 Change-defined hepatic rules (contract §12.1)

| ID | Rule | Baseline requirement | Basis |
|---|---|---|---|
| HEP-T1 | Statin monitoring: enzyme doubling within 3 months of starting a statin | Prior result within the relevant window and known statin start date | NHS Devon guidance directs stopping a statin only if liver enzyme levels double within 3 months of starting, including in people with abnormal baseline results `[E]` |
| HEP-T2 | DILI baseline-adjusted thresholds: where baseline ALT is already ≥1.5× ULN, signal thresholds are expressed relative to baseline rather than to ULN | Documented pre-exposure baseline | Standard hepatic-safety monitoring convention `[C]` |
| HEP-T3 | FIB-4 trajectory: NICE-aligned periodic re-scoring | Prior FIB-4 or its constituents | <cite index="10-1">NHS Devon guidance directs calculating a FIB-4 score every 3 years and referring if it increases above the age-related cut-off</cite> `[E]` |

Where no valid baseline exists, contract §12.1 requires HealthIQ to state that the criterion could not be assessed. For HEP-T1 this means: HealthIQ cannot tell a statin user whether their enzymes have doubled without a pre-statin result, and must say so rather than reassure.

### 8.2 Change-modified rules (contract §12.2)

**HEP-T4 `[E]`** — Persistence does not reduce concern in this domain, and the intuition that it should is explicitly contradicted. <cite index="79-1">BALLETS found 84% of adults still had abnormal tests when repeated one month later, and even at 2 years 75% remained abnormal</cite>. <cite index="79-1">BSG further states that a strategy of simply repeating abnormal tests can only be justified where there is a high degree of certainty that the abnormality will resolve in response to an identified acute insult</cite>.

**HEP-T5 `[E]`** — Normalisation does not exclude disease. <cite index="79-1">While transient abnormality may occur in some acute liver diseases, it is manifestly not the case for many chronic liver diseases such as HCV and NAFLD, where even normalised liver blood tests do not necessarily imply absence or resolution of disease</cite>. A resolving trend may not lower a hepatic finding below its floor — contract §12.2 as amended in v0.3.

**HEP-T6 `[J]`** — Because HEP-T4 and HEP-T5 both cut against downgrading, this ruleset defines **no trend-based downgrade rule for the hepatic domain**. Trend in hepatic findings acts on within-tier ordering and on explanation only.

### 8.3 Baseline validity `[J]`

| Purpose | Maximum baseline age | Rationale |
|---|---|---|
| Statin doubling (HEP-T1) | 3 months before the current result, plus a documented statin start date | The rule is defined over a 3-month window `[E]` |
| DILI baseline adjustment (HEP-T2) | Most recent pre-exposure result | Definitional `[C]` |
| Chronicity assessment | 24 months | BALLETS 2-year persistence data supports a comparison horizon of this length `[E]`-informed `[J]` |
| FIB-4 trajectory | 3 years | NHS Devon 3-yearly recalculation interval `[E]` |

**HEP-T7 `[E]`** — <cite index="79-1">BSG Recommendation 2 states that abnormal liver blood test results should only be interpreted after review of the previous results, past medical history and current medical condition</cite>. HealthIQ typically has none of the second and third. This is a structural limitation of the product in this domain and must be stated in output, not worked around. It is the strongest single argument for the contract §16 insufficient-data discipline.

---

## 9. Analytical and contextual caveats

### 9.1 Analytical (contract §4.6 — annotation only, never a tier input)

| ID | Caveat | Affects |
|---|---|---|
| HEP-A1 `[E]` | Haemolysed sample raises AST | AST |
| HEP-A2 `[E]` | Skeletal muscle injury, myositis, recent intense exercise and myocardial injury raise AST; creatine kinase measurement helps determine whether an isolated transaminase rise is of skeletal muscle origin | AST, ALT |
| HEP-A3 `[E]` | ALP is raised physiologically in pregnancy and in childhood growth | ALP |
| HEP-A4 `[E]` | Enzyme induction by drugs raises GGT | GGT |
| HEP-A5 `[E]` | Bilirubin in Gilbert's rises further on fasting — the confirmatory manoeuvre, not an artefact, but relevant to interpreting a fasting sample | Bilirubin |
| HEP-A6 `[E]` | Intercurrent illness can raise liver enzymes | All |

### 9.2 Contextual (affects explanation and recommendation, not tier)

| ID | Context | Effect |
|---|---|---|
| HEP-C1 `[E]` | Statin therapy | <cite index="79-1">Although statins can lead to drug-induced liver injury this is very rare, with studies demonstrating they are safe in patients with pre-existing abnormal liver enzymes</cite>. Must not trigger a stop-your-medication recommendation. HealthIQ must never advise medication cessation |
| HEP-C2 `[E]` | Alcohol | NICE NG50 thresholds of 50 units/week for men and 35 for women above which fibrosis assessment is recommended; AUDIT >19 indicates dependency warranting alcohol-services referral |
| HEP-C3 `[E]` | Metabolic risk factors (BMI, T2DM, dyslipidaemia, hypertension) | Support a steatotic-liver interpretation and route to the FIB-4 pathway |
| HEP-C4 `[E]` | Known hepatotoxic drugs — the BSG-cited list includes carbamazepine, methyldopa, minocycline, macrolides, nitrofurantoin, statins, sulfonamides, terbinafine, chlorpromazine and methotrexate | Raises DILI as an alternative interpretation. Contract v0.3 and Strategic Vision §6.7 bound medication handling to interpretation caveats; this must not become a drug library |
| HEP-C5 `[E]` | Pregnancy | Out of scope for this ruleset version. <cite index="79-1">In pregnancy ALP is often elevated and albumin reduced</cite>; applying these rules to a pregnant user would generate false concern. HealthIQ must not issue hepatic findings where pregnancy is known, pending a dedicated rule set. `[U]` HEP-U4 |
| HEP-C6 `[E]` | Age under 18 | Out of scope. BSG applies materially different paediatric rules including different aetiology panels and a lower referral threshold |

---

## 10. Combination and override register

Per contract §13, each entry is enumerated, named, sourced, versioned and directionally constrained. All entries below are promotion-only except where stated.

| ID | Trigger | Direction | Target | Source | Class |
|---|---|---|---|---|---|
| HEP-OV-1 | ALT or AST ≥10× ULN | Promote | Tier 0 | NHS Devon referral guidance | `[E]` |
| HEP-OV-2 | ALT or AST >1000 U/L | Promote | Tier 0 | NHS SPS | `[E]` |
| HEP-OV-3 | Hy's law pattern (§3.1) | Promote | Tier 0 | Hy's law; EASL/AASLD DILI | `[C]` |
| HEP-OV-4 | Abnormal hepatic analyte + albumin < LRL | Promote | Tier 0 | NHS SPS | `[E]` |
| HEP-OV-5 | Abnormal hepatic analyte + INR >1.5 without anticoagulation | Promote | Tier 0 | NHS SPS; ALF convention | `[E]`/`[C]` |
| HEP-OV-6 | New conjugated hyperbilirubinaemia + abnormal enzymes | Promote | Tier 0 | BSG immediate-referral rule | `[E]` |
| HEP-OV-7 | Raised ferritin + transferrin saturation >45% | Promote | Tier 1, distinct finding HEP-F12 | <cite index="79-1">BSG directs referral to a specialist clinic for haemochromatosis, defined as raised ferritin and transferrin saturation above 45%</cite> | `[E]` |
| HEP-OV-8 | FIB-4 >3.25 (or >age-adjusted threshold) | Promote | Tier 1, HEP-F5 | BSG NAFLD algorithm | `[E]` |
| HEP-OV-9 | AST:ALT ratio >1 with any hepatic abnormality or with metabolic/alcohol context | Promote | Tier 1, HEP-F5 | BSG fibrosis marker | `[E]` |
| HEP-OV-10 | Low platelets + abnormal hepatic analytes | Promote | Tier 1, HEP-F5 | BSG platelets-as-fibrosis-indicator | `[E]` |
| HEP-OV-11 | Isolated raised GGT >100 U/L | Promote | Tier 1 | BSG ARLD algorithm | `[E]` |
| HEP-OV-12 | Isolated raised bilirubin **with** anaemia | Promote | Tier 1 | BSG haemolysis rule | `[E]` |
| HEP-OV-13 | Isolated raised ALP **with** normal GGT | **Reclassify** to HEP-F7, non-hepatic origin likely | Reclassification, not downgrade — the finding retains its own floor as a non-hepatic ALP concern and is handed to the appropriate domain | BSG ALP origin rule | `[E]` |

**Register discipline `[J]`** — HEP-OV-13 is the only entry that moves a finding away from the hepatic domain, and it is deliberately framed as reclassification rather than downgrade so that it cannot be used as a suppression route. Contract §13 forbids downgrade below floor; a reclassification that dropped the finding entirely would achieve the same effect by another name.

**No downgrade overrides are defined for this domain.** If one is later proposed, §8.2 (HEP-T4, HEP-T5) is the evidence it must overcome.

---

## 11. Contextual attachment of MCV, transferrin, ferritin

This section implements contract §4.8 and is where the original UAT failure lived.

### 11.1 MCV

**HEP-CTX-1 `[E]`** — Isolated mild macrocytosis alongside a hepatic finding is contextual. NHS Scotland guidance on isolated macrocytosis is explicit that where investigations are normal and there are no other blood-count abnormalities, the patient has idiopathic macrocytosis and should be reassured that no further tests are needed; NHS Lothian guidance notes that excess alcohol and chronic liver disease commonly cause macrocytosis. Attachment to the hepatic finding is therefore both clinically correct and more informative than presenting it separately.

**HEP-CTX-2 `[E]` — the boundary.** Contextual role is unavailable where the macrocytosis is not isolated. UK pathways route macrocytosis with any additional full blood count abnormality — anaemia, neutropenia, thrombocytopenia, monocytosis or combinations — to the separate macrocytic anaemia pathway. In that case MCV forms an independent haematological finding.

**HEP-CTX-3 `[J]`** — Contextual role is also unavailable where MCV independently meets a Tier 1 severity threshold in the haematology domain. Contract §4.8 forbids it. **The MCV band structure is a haematology-pilot dependency.** `[U]` HEP-U5. Pending that work, this ruleset applies a conservative interim rule: MCV may be attached contextually only where it is within 10% of ULN and no other FBC abnormality is present. The 10% figure is an interim safety margin, not a clinical threshold, and must be replaced.

**HEP-CTX-4 `[J]`** — Per contract §9.1, multiple MCV interpretation frames consolidate into one macrocytosis item before tiering. In hepatic context they consolidate into a single contextual note, not three.

### 11.2 Transferrin

**HEP-CTX-5 `[C]`** — Low transferrin is non-specific: it falls as a negative acute-phase protein in inflammation, in liver disease from reduced synthesis, and in protein-energy undernutrition. Attached contextually to a hepatic finding as a supporting observation. It does not generate an independent concern.

**HEP-CTX-6 `[E]`** — Transferrin *saturation* is a different matter entirely and is not contextual. It is a required constituent of the BSG standard liver aetiology screen and, with ferritin, triggers HEP-OV-7.

### 11.3 Ferritin

**HEP-CTX-7 `[E]`** — Raised ferritin **without** transferrin saturation above 45% in a hepatic context is contextual, not a concern. <cite index="79-1">An isolated elevated serum ferritin result is commonly seen in dysmetabolic iron overload syndrome as found in the setting of alcohol excess, NAFLD and other chronic liver diseases and does not reflect haemochromatosis</cite>.

**HEP-CTX-8 `[E]`** — Raised ferritin **with** transferrin saturation >45% is a distinct Tier 1 finding (HEP-F12, HEP-OV-7), not context. This is the case where the lower-magnitude finding is the more concerning one: ferritin of 400 with TSAT 60% outranks ferritin of 1200 with TSAT 25%.

**HEP-CTX-9 `[J]`** — Where ferritin is raised and transferrin saturation is absent, iron overload cannot be excluded. Per contract §8, this must not reduce the finding. The correct output is a Tier 1 hepatic finding with an explicit recommendation for simultaneous ferritin and transferrin saturation, which is what BSG Recommendation 5 specifies in any case.

### 11.4 General attachment rule

**HEP-CTX-10 `[J]`** — A contextual attachment must state its relationship to the parent ("this may be related to the liver finding"), never be presented as an independent abnormality, and must remain reconcilable with the raw value per contract §6.5. If the hepatic parent finding is removed or reclassified, the contextual items must be re-evaluated for orphan status under contract §6.5 rather than silently dropped.

---

## 12. Concern-tier mapping, lead selection, and no-concern outputs

### 12.1 Hepatic tier mapping

Applying contract §6.1: initial tier = the more serious of the urgency-derived and severity-derived tiers.

| Urgency-derived tier | Trigger |
|---|---|
| Tier 0 | Any HEP-U0 criterion met |
| Tier 1 | Any confirmed out-of-range core hepatic analyte, per HEP-PRINCIPLE-2 |
| Tier 2 | Isolated raised GGT ≤100 U/L (HEP-GGT-4); established Gilbert's pattern (HEP-F6 without anaemia) |
| Tier 3 | Not available to primary hepatic analytes; reserved for HEP-CTX items |

| Severity-derived tier | Trigger |
|---|---|
| Tier 0 | HEP-S4 (ALT/AST ≥10× ULN or >1000 U/L) |
| Tier 1 | HEP-S1 through HEP-S3; HEP-ALP-1 and HEP-ALP-2 |
| Tier 2 | No hepatic severity band maps to Tier 2 by severity alone |

Note the deliberate consequence: because severity never maps below Tier 1 for an abnormal analyte, and urgency floors at Tier 1 under HEP-PRINCIPLE-2, hepatic Tier 2 is reachable only through the two named exceptions. This is the structural expression of BSG Recommendation 4 and the reason HEP-U1 is the primary reconciliation item.

### 12.2 Lead-selection behaviour

Per contract §7, hepatic findings compete on urgency, then severity, then clinical significance, then actionability, then trend, then directness.

**HEP-LEAD-1 `[J]`** — Within a hepatic panel, HEP-F4 (synthetic dysfunction) outranks HEP-F1/F2/F3 (injury patterns) at equal tier, because function outranks injury (§6). A panel with ALT 200 and albumin 28 leads on the synthetic finding.

**HEP-LEAD-2 `[J]`** — HEP-F1/F2/F3 outrank HEP-F5 (suspected fibrosis) at equal tier only where the injury pattern is in HEP-S3 or above. Below that, HEP-F5 is the more consequential finding, because fibrosis stage predicts outcome and enzyme level does not — BSG Recommendation 3 again.

**HEP-LEAD-3** — Contextual items (§11) may never lead. Contract §4.8, §6.5, §18.17.

**HEP-LEAD-4 `[J]`** — Where a hepatic finding and a non-hepatic finding both qualify, cross-domain comparison requires the shared severity scale that contract §20.10 defers. **This ruleset cannot resolve cross-domain lead contests and does not attempt to.** Until the cross-domain mapping exists, contests between a hepatic Tier 1 and, say, a haematological Tier 1 must be escalated as an unresolved case rather than settled by within-domain logic. `[U]` HEP-U6.

### 12.3 No-concern output (contract §16.1)

Hepatic-specific mandatory content:

1. **Normal liver enzymes do not exclude liver disease.** <cite index="79-1">Both AST and ALT can be normal even in the setting of cirrhosis</cite>, and <cite index="79-1">many patients with significant liver fibrosis may have liver enzymes in the normal reference range and normal synthetic function</cite>. `[E]` This statement is mandatory in every hepatic no-concern output. It is the single most important false-reassurance safeguard in the domain.
2. Which hepatic analytes were and were not measured.
3. Whether fibrosis risk could be assessed (FIB-4 computability) and, if not, that it was not assessed.
4. Whether synthetic function was assessed (albumin, INR, bilirubin availability).
5. That symptoms warrant clinical review irrespective of the result summary.

**HEP-NC-1 `[J]`** — The phrase "your liver is healthy", or any equivalent, is prohibited. HealthIQ measures enzymes, not liver health.

### 12.4 Insufficient-data output (contract §16.2)

Fires where the panel cannot support hepatic assessment. Minimum viable hepatic assessment `[J]`: ALT (or AST) **and** ALP. Without both, no pattern can be classified and HealthIQ must issue an insufficient-data output for the hepatic domain rather than a partial finding dressed as a conclusion.

Where the minimum is met but synthetic markers are absent, the output is a finding with an explicit synthetic-function-not-assessed statement — not an insufficient-data output. The distinction matters: one says "we could not look", the other says "we looked at injury but not function".

---

## 13. Acceptance scenarios

**Reconciliation required** — see §0.1. These are derived, not taken from the pilot spec.

### AS-1 — Contract v0.3 §19 regression fixture

ALT 250 (ULN 49, 5.1×), ALP 46 (ULN 116), R ≈ 12.9, bilirubin normal, GGT normal, AST absent, MCV 99.5 (ULN 96), transferrin mildly low.

**Independently derived result** — rules applied without reference to the expected answer:

| Step | Rule | Outcome |
|---|---|---|
| Consolidation | HEP-CONS-1 | ALT + ALP + bilirubin + GGT → one finding |
| Pattern | R = 12.9 ≥ 5 | Hepatocellular, HEP-F1 |
| Severity | ALT 5.1× ULN | HEP-S3 marked (≥5× to <10×) |
| Urgency | HEP-U0-1: 5.1× < 10× → not met. HEP-U0-2: 250 < 1000 → not met. HEP-U0-3: bilirubin normal → not met. HEP-U0-4/5: albumin and INR absent → **could not be assessed**, HEP-MISS-1 | No Tier 0 criterion met |
| Urgency tier | HEP-PRINCIPLE-2 | Tier 1 |
| Severity tier | HEP-S3 | Tier 1 |
| Initial tier | More serious of the two | **Tier 1** |
| Promotion | No governed rule fires | Tier 1 |
| Confidence | AST absent → reduced for aetiological characterisation and fibrosis assessment | Explanation only |
| Significance | Assessed as-characterised; unaffected by missing AST (contract §4.3) | Not reduced |
| MCV | 99.5 vs ULN 96 = 3.6%, within the HEP-CTX-3 interim 10% margin; no other FBC abnormality stated | Contextual, attached |
| Transferrin | HEP-CTX-5 | Contextual, attached |
| Lead | Only Tier 1 finding | Hepatocellular liver injury pattern |

**Result: Tier 1, hepatocellular pattern, single lead, MCV and transferrin contextual, AST absent reduces confidence not priority, no urgent diagnostic claim.**

This matches contract §19.2 in every particular. **The match was not engineered.** The determining rules were HEP-U0-1 (10× threshold, NHS Devon), HEP-S3 (5× band, EASL), and HEP-PRINCIPLE-2 (BSG Rec 4) — all sourced before the fixture was consulted. Had the ALT been 500 U/L against the same ULN (10.2×), the derived answer would have been Tier 0, and the fixture would not have been the governing case.

**Required outputs beyond the fixture:** the finding must state that albumin and INR were not measured and that synthetic function could not be assessed; must recommend the BSG standard liver aetiology screen including AST; must not name a diagnosis.

### AS-2 — Same ALT, albumin low

ALT 250 (5.1×), ALP 46, albumin 28 g/L (LRL 35).
Expected: **Tier 0** via HEP-OV-4. Lead is HEP-F4 synthetic dysfunction per HEP-LEAD-1, with the hepatocellular pattern presented within it. Action-and-timeframe language. Albumin non-hepatic-cause caveat (HEP-ALB-2) required. Tier 0 operational pathway (contract §17) must exist before this scenario can be released.

### AS-3 — ALT 550 U/L, ULN 49 (11.2×), all else normal

Expected: **Tier 0** via HEP-OV-1. Demonstrates that magnitude alone reaches Tier 0 at the 10× boundary. Confirmation advice not required (transaminases are not artefact-prone in the way potassium and platelets are), but the recommendation to repeat with a full liver screen is.

### AS-4 — ALT 60 U/L, ULN 49 (1.2×), isolated

Expected: **Tier 1** under HEP-PRINCIPLE-2, HEP-S1 mild. This is the scenario that tests HEP-U1 directly. If the Head of Medical Research adopts the modified position, this becomes Tier 2. **The two answers are both defensible and the choice must be recorded.** Under either answer the finding is shown, and under both the no-concern language is prohibited.

### AS-5 — ALP 240 (ULN 116, 2.1×), GGT normal, ALT normal

Expected: reclassified via HEP-OV-13 to HEP-F7, non-hepatic ALP likely. Not a hepatic concern. Handed to the appropriate domain with its own floor intact. Tests that reclassification is not being used as suppression.

### AS-6 — Bilirubin 38 µmol/L isolated, no anaemia, all other hepatic analytes normal

Expected: **Tier 2**, HEP-F6 Gilbert's pattern, reassurance appropriate per HEP-U-NEG-2, with the caveat that split bilirubin was not measured if it was not. Tests the one place in this domain where reassurance is evidence-supported.

### AS-7 — Bilirubin 38 µmol/L isolated, haemoglobin low

Expected: **Tier 1** via HEP-OV-12. Same bilirubin, different finding. Tests that combination rules override the isolated-finding default.

### AS-8 — Ferritin 1400 µg/L, TSAT 22%, ALT 90 (1.8×)

Expected: hepatic finding Tier 1 (HEP-S1). Ferritin **contextual** via HEP-CTX-7 — dysmetabolic pattern, not haemochromatosis. Tests that magnitude does not promote a contextual finding.

### AS-9 — Ferritin 420 µg/L, TSAT 58%, ALT 90 (1.8×)

Expected: **two** Tier 1 findings — the hepatic pattern and HEP-F12 possible iron overload via HEP-OV-7. Co-lead eligible under contract §7.4 if the action pathways are judged materially different (aetiology screen versus HFE testing). Tests the case where a lower ferritin outranks a higher one.

### AS-10 — ALT 30, AST 45, platelets 130, age 58

All values in or near range. AST:ALT ratio 1.5 (>1), FIB-4 computable.
Expected: **HEP-F5 Tier 1** via HEP-OV-9 and, if FIB-4 exceeds the age threshold, HEP-OV-8. Tests contract §3.1's in-range-findings rule against real evidence (HEP-FIB-1). If the system produces no finding here, the in-range rule is not implemented.

### AS-11 — ALT 250, ALP absent

Expected: **HEP-F9 non-classifiable**, Tier 1 by severity (HEP-S3). R not computed. Must **not** be described as hepatocellular. Tests HEP-R-1 and §5.3.

### AS-12 — Complete normal hepatic panel

Expected: **no-concern output** per §12.3, mandatorily including the statement that normal liver enzymes do not exclude liver disease or advanced fibrosis, plus fibrosis-assessability status. Tests the highest-volume and highest-false-reassurance-risk output in the domain.

### AS-13 — ALT 250, MCV 118 fL

Expected: MCV **may not** be contextual — outside the HEP-CTX-3 interim margin. Two findings. Tests contract §4.8's prohibition on assigning contextual role to a finding that independently warrants concern, and exposes the haematology dependency (HEP-U5).

---

## 14. Unresolved clinical questions

| ID | Question | Blocking? |
|---|---|---|
| HEP-U1 | Does HealthIQ adopt BSG Recommendation 4 literally (Tier 1 floor for any abnormal hepatic analyte, high volume) or a modified magnitude-gated position? A departure must be documented as clinical adjudication under contract §13 | **Yes — primary reconciliation item** |
| HEP-U2 | Numeric bilirubin threshold for HEP-U0-6, and behaviour when the conjugated fraction is unavailable | **Yes — Tier 0 rule incomplete** |
| HEP-U3 | Platelet thresholds at which a low count becomes an independent haematological finding rather than a hepatic fibrosis indicator (HEP-PLT-3) | **Yes — cross-domain** |
| HEP-U4 | Pregnancy handling. Current position is to suppress hepatic findings where pregnancy is known. Is suppression safe, or should a pregnancy-adjusted rule set be built before launch? Suppression is itself a clinical decision | **Yes** |
| HEP-U5 | MCV band structure. The 10%-of-ULN interim margin in HEP-CTX-3 is a placeholder and must be replaced by haematology-derived bands | **Yes** |
| HEP-U6 | Cross-domain lead contests (HEP-LEAD-4). Cannot be resolved within a single domain pilot | Yes, but properly a contract §20.10 item |
| HEP-U7 | Should HealthIQ compute and surface FIB-4 at all, given it requires age and platelets and produces a score with referral implications? This is arguably the most device-like output in the domain and should be raised with the regulatory workstream under contract §22 | **Yes — regulatory interaction** |
| HEP-U8 | Whether the BSG observation that ALT reference intervals may be set too high should lead HealthIQ to apply lower internal thresholds than the reporting laboratory's. Doing so would generate findings on results the laboratory reported as normal | No, but material |
| HEP-U9 | Whether isolated raised GGT ≤100 U/L at Tier 2 (HEP-GGT-4) is defensible given its mortality association (HEP-GGT-2) | No |
| HEP-U10 | Alcohol and medication context are required by several rules (HEP-C2, HEP-C4, HEP-T1) but are Wave 5 context-hardening capabilities. Which hepatic rules are permitted to run without them, and which must state that context was unavailable? | **Yes — determines what this ruleset can actually do at launch** |

**HEP-U10 deserves emphasis.** A substantial part of the hepatic evidence base is context-conditional. Without alcohol history, medication list, BMI or symptoms, HealthIQ is applying rules whose source guidance assumes a clinician holds that context. BSG Recommendation 2 says results should only be interpreted after review of previous results, past medical history and current condition. HealthIQ will frequently have none of these. That does not make interpretation impossible, but it must be stated in output, and the Head of Medical Research should decide whether any hepatic rule is unsafe to run without context rather than merely lower-confidence.

---

## 15. Evidence table

| Source | Used for | Type |
|---|---|---|
| Newsome PN et al. Guidelines on the management of abnormal liver blood tests. British Society of Gastroenterology. *Gut* 2018;67(1):6–19 | HEP-PRINCIPLE-1/2; Recs 1–5, 7, 9, 10; pattern recognition; analyte roles; aetiology screen; Gilbert's; ALP origin; GGT specificity and prognosis; AST:ALT ratio; FIB-4 thresholds; BALLETS persistence data; pregnancy; ferritin/TSAT 45% | Primary UK guideline |
| NHS Devon (North & East) — Management of Abnormal LFTs in Asymptomatic Adults | HEP-U0-1 (10× ULN); HEP-T1 (statin doubling); HEP-T3 (3-yearly FIB-4) | UK regional pathway |
| NHS Specialist Pharmacy Service — Assessing liver function and interpreting liver blood tests | HEP-U0-2 (>1000 U/L); HEP-U0-4 (low albumin); HEP-U0-5 (INR) | UK national resource |
| NHS Highland — Abnormal liver blood results referral pathway (over 16s) | Liver screen composition; pattern-based referral | UK regional pathway |
| NICE NG50 — Cirrhosis in over 16s | Alcohol thresholds 50/35 units/week | NICE |
| NICE NG49 — NAFLD assessment and management | Fibrosis assessment context | NICE |
| EASL Clinical Practice Guidelines: Drug-induced liver injury, *J Hepatol* 2019 | R-value definition and cutoffs; 5× ULN hepatocellular designation | International — used where UK guidance is silent |
| AASLD practice guidance on drug, herbal and dietary supplement induced liver injury | R-value categorisation; Hy's law; INR >1.5 as a DILI detection criterion | International — used where UK guidance is silent |
| NHS Scotland Right Decisions / RefHelp — isolated macrocytosis; NHS Highland macrocytosis guideline; NHS Kernow macrocytosis referral criteria | HEP-CTX-1, HEP-CTX-2, artefactual MCV | UK regional pathways |
| Royal College of Pathologists — alert systems and communication of unexpected findings | Tier 0 pathway framing (contract §17) | UK professional body |

**Evidence gaps recorded honestly:**
- No UK guideline specifies numeric transaminase severity bands. The bands in §4.1 are assembled from UK referral thresholds (3×, 10×, 1000 U/L) and an international DILI threshold (5×). This is a synthesis, labelled `[J]`.
- No UK guideline endorses the numeric R-value. §5.2 records this.
- No UK guideline addresses prioritisation of hepatic findings against findings in other domains. §12.2 records this as out of scope.
- No UK guideline addresses lab interpretation without clinical context, which is HealthIQ's actual operating condition. HEP-U10.

---

## 16. Clinical sign-off

This ruleset is not clinically valid until the fields below are completed by a person holding appropriate qualifications, competence and scope under contract v0.3 §23.1.

| Field | Value |
|---|---|
| Ruleset version | 0.1 |
| Governing contract version | HEALTHIQ-CLIN-PRIORITY-CONTRACT-001 v0.3 |
| Pilot spec version reconciled against | ☐ *(pilot spec was not available to the author — see §0.1)* |
| Head of Medical Research — name | ☐ |
| Registration / qualification | ☐ |
| Date of review | ☐ |
| HEP-U1 adjudication (Tier 1 floor position) | ☐ ADOPT BSG LITERAL / ☐ MODIFIED — reason: |
| HEP-U2 adjudication (bilirubin threshold) | ☐ |
| HEP-U3 adjudication (platelet boundary) | ☐ |
| HEP-U4 adjudication (pregnancy) | ☐ |
| HEP-U5 adjudication (MCV bands) | ☐ |
| HEP-U7 raised with regulatory workstream (FIB-4) | ☐ YES / ☐ NO |
| HEP-U10 adjudication (context-free operation) | ☐ |
| All `[J]` items individually reviewed | ☐ |
| Override register (§10) approved as a versioned asset | ☐ |
| Acceptance scenarios (§13) reconciled against pilot spec | ☐ |
| Tier 0 operational pathway exists (contract §17) | ☐ YES / ☐ NO — if NO, no Tier 0 rule may be released |
| Signature | ☐ |

---

## VERDICT: READY_FOR_HMR_RECONCILIATION

The hepatic rules are derivable from UK evidence and are set out above with sources and evidence classes. The regression fixture passes on independently derived rules, and §13 AS-1 documents the derivation path so the independence can be audited.

Three qualifications on that verdict, in order of weight:

**First, HEP-U1 is a genuine clinical policy question, not a research gap.** BSG Recommendation 4 says investigate any out-of-range liver analyte irrespective of level; BALLETS says fewer than 5% of those investigations find liver disease. Both are true. Whether HealthIQ follows the recommendation literally or departs from it is a decision only the Head of Medical Research can make, and it determines the tier volume of the entire domain. It is the reason this document goes to reconciliation rather than to sign-off.

**Second, five Tier 0 and boundary rules are incomplete** (HEP-U2 through HEP-U5, HEP-U10). Three of them are cross-domain dependencies that a hepatic pilot structurally cannot close.

**Third, the pilot spec was not available.** §0.1 states the consequence and it is confined to §13.

None of these makes the domain unsafe to specify. They make it unsafe to release without adjudication, which is exactly what reconciliation is for.
