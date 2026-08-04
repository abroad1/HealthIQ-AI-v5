---
document_id: HEALTHIQ-CROSS-DOMAIN-PRIORITY-VALIDATION-REPORT-001
title: HealthIQ Cross-Domain Clinical Prioritisation Validation Report
version: "0.1"
reviews: HEALTHIQ-CROSS-DOMAIN-PRIORITY-VALIDATION-001 v0.1
governing_contract: HEALTHIQ-CLIN-PRIORITY-CONTRACT-001 v0.3
reviewer_role: Independent cross-domain medical validation reviewer
verdict: VALIDATE_WITH_CONTRACT_AMENDMENTS
---

# Cross-Domain Clinical Prioritisation Validation Report v0.1

**Evidence classes used throughout:** `[E]` evidence-supported rule · `[C]` accepted clinical convention · `[J]` HealthIQ clinical judgement · `[U]` unresolved question.

---

## 1. Executive conclusion

The contract v0.3 model survives breadth testing. Its core architecture — consolidated findings as the unit, separated dimensions, urgency and severity as tier floors, confidence excluded from prominence, supporting-marker count excluded entirely — held in all nine domains without a single case where a domain *required* a prohibited behaviour to produce a safe answer. That is the result that matters, and it is a stronger result than I expected going in.

Four findings qualify that.

**1.1 The model has no way to assign severity under indeterminacy, and thyroid exposes it.** A raised TSH with free T4 unavailable is compatible with subclinical hypothyroidism (common, Tier 2) or overt hypothyroidism (uncommon, Tier 1). Contract §4.5 correctly forbids the missing marker from reducing priority. Contract §9.4 assigns the highest constituent severity — but §9.4 governs *frames*, not *missing discriminators*, and applying it here escalates a finding affecting up to 10% of iodine-sufficient populations `[E]`. Neither escalating nor defaulting low is safe as a blanket rule. **This is the primary contract amendment (A1, §7).**

**1.2 Severity is not cross-domain comparable; urgency is.** This is the most useful structural finding in the exercise. Severity units are incommensurable — 5× ULN, 6.6 mmol/L, 18 × 10⁹/L, an LDL of 6.0 — and no amount of banding makes them so. But *time-to-harm* is a single scale that every domain can express: same-day, days, weeks, routine. Cross-domain lead contests should therefore be adjudicated on urgency expressed as a time band, with severity used only within a domain. **This converts the "unresolved cross-domain tie-break" from an open problem into a bounded one (A2, §7).** It does not resolve Tier 0 versus Tier 0 across domains, which remains genuinely open.

**1.3 The hepatic ruleset contains exactly one concept that must not universalise, and it is a serious one.** HEP-PRINCIPLE-2 — reference-range exceedance sets a Tier 1 floor — derives from BSG Recommendation 4, which is a hepatology-specific grade B recommendation `[E]`. Applied to haematology it would place isolated mild macrocytosis in Tier 1, directly contradicting NHS Scotland guidance that such patients should be reassured that no further tests are needed `[E]`. Applied to iron, inflammatory and nutritional markers it would generate large volumes of Tier 1 noise. **Prohibited universalisation, §9.**

**1.4 Lipids do not fit the contract's severity definition.** Contract §4.2 defines severity as "the degree of abnormality or dysfunction". An LDL of 6.0 mmol/L is barely abnormal by distance-from-range and profoundly consequential over decades. The domain's severity method is calculated long-term risk, which §4.2's list does not include. **Amendment A3.**

None of these is a redesign trigger. All four are additive. The verdict is `VALIDATE_WITH_CONTRACT_AMENDMENTS`.

**Sequencing:** the recommended first detailed domain is **haematology**, not hepatic. Reasoning in §10.

---

## 2. Domain-by-domain validation tables

### 2.1 Hepatic

| Field | Content |
|---|---|
| First-look markers | ALT, ALP, bilirubin, albumin `[E]` — BSG Rec 1 defines the initial panel as bilirubin, albumin, ALT, ALP and GGT with FBC |
| Deferred/conditional | AST (reflex after abnormal ALT), GGT (ALP origin, alcohol context), INR, platelets |
| Major consolidated findings | Hepatocellular / cholestatic / mixed injury pattern; synthetic dysfunction; suspected advanced fibrosis; isolated hyperbilirubinaemia; isolated raised ALP; isolated raised GGT |
| Urgency drivers | Synthetic dysfunction (low albumin, INR >1.5, jaundice with abnormal enzymes); extreme magnitude (≥10× ULN, >1000 U/L); Hy's law combination `[E]`/`[C]` |
| Severity method | Multiples of ULN for transaminases and ALP; **not** magnitude for prognosis — BSG Rec 3 states extent of abnormality is not necessarily a guide to clinical significance `[E]` |
| Trend role | **Important**, not essential. Persistence does not reduce concern (BALLETS: 84% still abnormal at 1 month, 75% at 2 years) and normalisation does not exclude disease `[E]` |
| Combination rules | ALT+ALP → pattern; ferritin+TSAT>45% → iron overload; AST:ALT>1 or low platelets → fibrosis; enzymes+albumin/INR → synthetic failure `[E]` |
| Contextual markers | Mild isolated MCV, low transferrin, raised ferritin with normal TSAT `[E]` |
| Confidence-only | Missing AST, GGT, split bilirubin; absent alcohol/medication/metabolic context |
| Provisional tiers | T0 synthetic failure or extreme magnitude; T1 any confirmed abnormal core analyte (see §9 caveat); T2 isolated GGT ≤100, Gilbert's pattern; T3 contextual attachments |
| Contract fit | **Conditional pass** — fits, but its Tier 1 floor principle is domain-bound |
| Dependencies | Haematology (platelets, MCV bands); context capture (alcohol, medication) |

### 2.2 Electrolytes and acute metabolic disturbance

| Field | Content |
|---|---|
| First-look markers | Sodium, potassium, adjusted calcium |
| Deferred/conditional | Magnesium, phosphate, bicarbonate, ionised calcium, urine electrolytes (not available to HealthIQ) |
| Major consolidated findings | Hyperkalaemia; hypokalaemia; hyponatraemia; hypernatraemia; hypercalcaemia; hypocalcaemia |
| Urgency drivers | **Absolute concentration**, and rate of change. K⁺ ≥6.5 mmol/L is severe and an emergency; 6.0–6.4 moderate `[E]`. Na⁺ <125 profound `[E]`. Adjusted Ca²⁺ >3.0 severe, >3.4–3.5 life-threatening `[E]` |
| Severity method | **Absolute concentration only.** Multiples of ULN are actively misleading here — K⁺ 6.6 against ULN 5.3 is 1.25× ULN and a medical emergency `[E]` |
| Trend role | **Modifying but clinically potent.** Acute change >0.5 mmol/L K⁺ over 6–12 h may matter more than the absolute level `[E]`. Chronicity governs hyponatraemia risk |
| Combination rules | K⁺ with renal impairment; Ca²⁺ requires albumin adjustment before any interpretation `[E]`; sodium may read falsely low with severe hypertriglyceridaemia `[E]` |
| Contextual markers | Albumin (as calcium modifier, not a finding); magnesium in refractory hypokalaemia |
| Confidence-only | Absent symptoms; absent medication list (RAAS inhibitors, diuretics); absent baseline |
| Provisional tiers | T0 severe bands; T1 moderate; T2 mild; T3 rarely applicable — electrolytes are poor contextual markers |
| Contract fit | **Pass**, with a mandatory artefact-language exception (§3.2) |
| Dependencies | Tier 0 operational pathway (contract §17) **must exist before this domain is authored**; renal |

### 2.3 Renal

| Field | Content |
|---|---|
| First-look markers | Creatinine, eGFR, potassium |
| Deferred/conditional | Urea, ACR (usually unavailable), bicarbonate, calcium/phosphate |
| Major consolidated findings | Acute kidney injury (change-defined); chronic reduced eGFR; renal impairment with electrolyte disturbance |
| Urgency drivers | **Rate of change.** NICE NG148 detects AKI by a creatinine rise ≥26 µmol/L in 48 h or ≥50% in 7 days `[E]` |
| Severity method | Change from baseline for AKI; disease-stage bands for CKD. Distance from reference range is the weakest of the three |
| Trend role | **Trend-essential.** This is the only domain where the principal finding cannot exist without a baseline |
| Combination rules | Renal impairment + hyperkalaemia raises both; renal impairment + thrombocytopenia is a haematology red flag `[E]` |
| Contextual markers | Urea — contextual, not causal; raised urea alone is a poor renal finding |
| Confidence-only | Muscle mass, ethnicity, hydration, recent nephrotoxics — all typically absent |
| Provisional tiers | T0 marked acute change; T1 new or unexplained reduced eGFR; T2 stable chronic reduction; T3 urea |
| Contract fit | **Pass** — contract §12.1 handles this correctly and was clearly written with this domain in view |
| Dependencies | Longitudinal data capture. **Without a valid baseline, HealthIQ cannot detect the domain's most important finding and must say so** |

### 2.4 Haematology

| Field | Content |
|---|---|
| First-look markers | Haemoglobin, MCV, platelets, total white count, **absolute** neutrophil count `[C]` — per spec §6.4, and correct: percentage differentials mislead when the total count is abnormal |
| Deferred/conditional | RDW, MCH, MCHC, lymphocytes, monocytes, eosinophils, film |
| Major consolidated findings | Anaemia (with red-cell size subtype); isolated macrocytosis; thrombocytopenia; thrombocytosis; neutropenia; leucocytosis; **multi-lineage cytopenia** |
| Urgency drivers | Absolute counts crossing recognised bands: platelets <20 × 10⁹/L warrants urgent haematology discussion, <50 urgent outpatient referral `[E]`; severe neutropenia; symptomatic anaemia; **any two-lineage or three-lineage cytopenia** `[C]` |
| Severity method | **Absolute cell count.** Not multiples of range |
| Trend role | Important. New versus long-standing changes management materially |
| Combination rules | This is the domain most governed by combination. Macrocytosis with any other FBC abnormality routes to a different pathway entirely `[E]`; thrombocytopenia with new thrombosis or renal impairment escalates `[E]`; anaemia + low MCV → iron pathway; anaemia + high MCV → B12/folate pathway |
| Contextual markers | RDW, MCH, MCHC, differential percentages |
| Confidence-only | No film; no reticulocytes; no prior counts; no bleeding/infection symptoms |
| Provisional tiers | T0 severe cytopenias and multi-lineage cytopenia; T1 single-lineage abnormality outside reassurance criteria; **T2 isolated mild macrocytosis with an otherwise normal FBC** `[E]`; T3 indices |
| Contract fit | **Pass** — and this is the domain that most clearly falsifies the hepatic Tier 1 floor |
| Dependencies | Iron, nutritional and hepatic all depend on **this** domain's bands, not the reverse |

### 2.5 Iron status

| Field | Content |
|---|---|
| First-look markers | Ferritin, transferrin saturation, haemoglobin, MCV |
| Deferred/conditional | Serum iron, transferrin/TIBC, CRP, HFE genotype (out of scope) |
| Major consolidated findings | Iron deficiency; iron deficiency anaemia; possible iron overload; inflammatory/dysmetabolic hyperferritinaemia |
| Urgency drivers | Low — this domain has almost no true urgency. Urgency comes from the *associated* anaemia, not from the iron marker |
| Severity method | Direction-asymmetric. Low ferritin is specific and highly actionable; high ferritin has a broad differential — inflammation, liver disease, malignancy, metabolic syndrome, overload `[E]` |
| Trend role | Modifying |
| Combination rules | **Ferritin is uninterpretable without TSAT for the overload question.** TSAT >45% is the discriminator; iron overload can generally be excluded when TSAT <45% `[E]`. Ferritin is an acute-phase reactant, so CRP conditions the deficiency reading |
| Contextual markers | Transferrin, serum iron, TIBC — these refine, they do not lead |
| Confidence-only | Absent CRP; non-fasting sample; absent menstrual/dietary history |
| Provisional tiers | T1 iron deficiency, and raised ferritin **with** raised TSAT; T2 raised ferritin with normal TSAT; T3 individual iron indices |
| Contract fit | **Pass**, and the cleanest demonstration of the contract's anti-magnitude stance: ferritin 420 with TSAT 58% outranks ferritin 1400 with TSAT 22% |
| Dependencies | Haematology; inflammatory |

### 2.6 Thyroid and endocrine

| Field | Content |
|---|---|
| First-look markers | TSH, free T4 |
| Deferred/conditional | Free T3, TPO antibodies, TRAb |
| Major consolidated findings | Overt hypothyroidism; subclinical hypothyroidism; overt hyperthyroidism; subclinical hyperthyroidism; **indeterminate thyroid-axis abnormality** (new class, see A1) |
| Urgency drivers | Genuinely low for the biochemistry alone. Thyroid emergencies are clinical, not biochemical, and HealthIQ has no clinical observation |
| Severity method | **Pattern, not magnitude.** The TSH number alone does not determine severity; the TSH/fT4 *relationship* does. TSH >10 mIU/L is the conventional treatment threshold in subclinical disease `[C]` |
| Trend role | Modifying. Spontaneous normalisation is common in mild subclinical elevation `[C]` |
| Combination rules | TSH+fT4 is the finding; neither alone is. Discordant patterns (both raised, both low) require specialist interpretation and should not be auto-explained `[U]` |
| Contextual markers | TPO antibodies — refine prognosis, do not lead |
| Confidence-only | Absent treatment status; non-thyroidal illness. **Absent fT4 is not confidence-only in effect — see A1** |
| Provisional tiers | T1 overt patterns and TSH >10; T2 mild subclinical; T0 essentially unreachable from biochemistry alone `[J]` |
| Contract fit | **Amendment required (A1)** |
| Dependencies | Pregnancy status — trimester-specific ranges apply and misapplication is a real harm `[E]` |

### 2.7 Cardiometabolic and lipid risk

| Field | Content |
|---|---|
| First-look markers | Total cholesterol, non-HDL cholesterol, triglycerides, HbA1c |
| Deferred/conditional | LDL, HDL, ApoB, Lp(a), fasting glucose |
| Major consolidated findings | Severe hypertriglyceridaemia; possible familial hypercholesterolaemia; elevated long-term CVD risk; dysglycaemia |
| Urgency drivers | Almost none, with **one sharp exception**: NICE directs urgent specialist review for triglycerides above 20 mmol/L not explained by excess alcohol or poor glycaemic control, because of pancreatitis risk `[E]` |
| Severity method | **Calculated long-term risk**, plus named referral thresholds: specialist assessment for total cholesterol >9.0 mmol/L or non-HDL >7.5 mmol/L regardless of family history; suspect FH above total cholesterol 7.5 mmol/L with relevant family history `[E]` |
| Trend role | Largely cross-sectional for risk scoring; trend matters for treatment response |
| Combination rules | Lipids are interpreted against age, sex, BP, smoking and diabetes — a risk score, not a marker. NICE directs excluding secondary causes (alcohol, uncontrolled diabetes, hypothyroidism, liver disease, nephrotic syndrome) before referral `[E]` |
| Contextual markers | HDL, individual fractions |
| Confidence-only | Absent family history; absent BP/smoking; absent treatment status |
| Provisional tiers | T0 TG >20; T1 FH-suspicious thresholds and TC >9.0 / non-HDL >7.5; T2 moderate abnormality with elevated aggregate risk; T3 individual fractions |
| Contract fit | **Amendment required (A3)** — severity here is future risk, not present abnormality |
| Dependencies | Context capture (Wave 5); thyroid, hepatic and renal as secondary-cause exclusions |

### 2.8 Inflammatory and immune-context markers

| Field | Content |
|---|---|
| First-look markers | CRP |
| Deferred/conditional | ESR, plasma viscosity, ferritin-as-APR, albumin-as-negative-APR, immunoglobulins |
| Major consolidated findings | Acute inflammatory response; persistent unexplained inflammation; inflammation as explanation for another finding |
| Urgency drivers | Very weak in isolation. CRP has no reference-range-based urgency without clinical context `[C]` |
| Severity method | Magnitude bands are weakly informative; **persistence is more informative than height** `[C]` |
| Trend role | Important — persistent unexplained elevation is the finding, not a single value |
| Combination rules | This domain's main job is combinatorial: CRP conditions ferritin interpretation `[E]`; inflammation with anaemia suggests anaemia of chronic disease; inflammation with cytopenia escalates |
| Contextual markers | **CRP is usually the contextual marker for another domain, not a concern in its own right** `[J]` |
| Confidence-only | Absent symptoms, absent infection history — which is most of what makes CRP interpretable |
| Provisional tiers | T2 isolated mild elevation; T1 marked or persistent unexplained elevation; T3 as explanatory context. T0 not reachable from CRP alone |
| Contract fit | **Pass** — and the best test of contract §4.8, since CRP is the domain most often correctly contextual |
| Dependencies | Iron, haematology |

### 2.9 Nutritional and deficiency markers

| Field | Content |
|---|---|
| First-look markers | B12, folate, ferritin (shared with iron), vitamin D |
| Deferred/conditional | MMA, homocysteine, holotranscobalamin, intrinsic factor antibodies |
| Major consolidated findings | B12 deficiency; folate deficiency; functional B12 deficiency with a normal serum level; vitamin D deficiency |
| Urgency drivers | **Neurological consequence, not magnitude.** B12 deficiency can produce neuropsychiatric and spinal cord manifestations that precede or occur without anaemia or macrocytosis `[E]`, and neurological recovery may be incomplete if treatment is delayed `[E]` |
| Severity method | Not concentration alone. BSH is explicit that the clinical picture is the most important factor in assessing cobalamin status because there is no gold-standard test `[E]` |
| Trend role | Modifying |
| Combination rules | B12/folate with macrocytosis; B12 with pancytopenia → urgent `[E]`; deficiency markers distorted by inflammation and binding proteins |
| Contextual markers | Vitamin D in most contexts; individual binding proteins |
| Confidence-only | Absent MMA/homocysteine; absent diet, metformin use, bariatric history |
| Provisional tiers | T1 clear deficiency, and any deficiency with neurological or multi-lineage haematological features; T2 borderline without corroboration; T3 vitamin D as context |
| Contract fit | **Pass**, and the strongest independent evidence for contract §3.1's in-range-findings rule — a normal serum B12 does not exclude functional deficiency `[E]` |
| Dependencies | Haematology; inflammatory |

---

## 3. Challenge-case results

Abbreviated to the adjudication and the reason.

### 3.1 Hepatic
- **Marked transaminase elevation, incomplete supporting markers** → Tier 1, single lead, confidence reduced only. Contract handles cleanly.
- **Mild isolated abnormality** → Tier 1 under BSG Rec 4, Tier 2 under a modified reading. **Unresolved and domain-bound** — see §9.
- **Injury pattern with possible synthetic dysfunction** → Tier 0 if albumin low or INR >1.5 `[E]`; if albumin absent, the criterion is *not assessable*, not *not met*.
- **Contextual MCV / ferritin** → contextual, provided each stays below its own domain's independent threshold.
- **Normal enzymes, unresolved fibrosis risk** → the no-concern output **must** state that normal enzymes do not exclude advanced fibrosis `[E]`. Highest-volume false-reassurance risk in the domain.

### 3.2 Electrolytes
- **Marked potassium abnormality** → Tier 0 at ≥6.5, Tier 0 or high Tier 1 at 6.0–6.4 `[E]`. Note international divergence: CCS/KDIGO use >6.0 as the urgent-treatment threshold where the UK Renal Association uses >6.5 `[E]`. `[U]` HealthIQ must choose and record.
- **Possible haemolysis/artefact** → finding stays, urgency stays, wording changes. Guidance requires pseudohyperkalaemia to be excluded `[E]`, so the mandatory formulation is *repeat urgently and contact a clinician*, not *you are in danger*.
- **Sodium with uncertain chronicity** → 130–133 mild, <130 moderate, <125 profound `[E]`. Chronicity is a confidence and management modifier, not a severity input.
- **Calcium requiring albumin correction** → **the finding cannot be created from uncorrected calcium.** If albumin is absent this is an insufficient-data output for the calcium finding, not a low-confidence finding `[E]`. Distinct from the general missing-marker rule: some markers are not interpretable at all without their modifier.
- **Abnormal result, symptoms unavailable** → priority unchanged; symptom absence is not symptom negativity. Contract §4.5 correct.

### 3.3 Renal
- **Creatinine change from valid baseline** → Tier 0 if NICE AKI criteria met `[E]`.
- **Reduced eGFR without baseline** → Tier 1 with an explicit statement that acute change could not be assessed. Contract §12.1 handles this and it is one of the contract's better provisions.
- **Stable chronic reduction** → Tier 2. A legitimate *severity-band* Tier 2, not a trend downgrade.
- **Urea elevation** → Tier 3 contextual. Urea alone is a weak renal finding and a common source of spurious alarm.
- **Renal + potassium** → combination raises both; the potassium leads on urgency.

### 3.4 Haematology
- **Isolated anaemia** → Tier 1; subtype by MCV.
- **Low Hb + low MCV** → one consolidated iron-deficiency-pattern finding, not two.
- **Macrocytosis without anaemia** → **Tier 2 with reassurance available** where the rest of the FBC is normal `[E]`. The single most important counterexample to the hepatic Tier 1 floor.
- **Macrocytosis with another cytopenia** → Tier 1, different pathway entirely `[E]`. Same MCV, different finding.
- **Thrombocytopenia** → banded: <20 Tier 0, <50 Tier 1 urgent, 50–100 Tier 1, plus the pseudothrombocytopenia caveat `[E]`.
- **Neutropenia** → absolute count only. A normal-looking percentage with a low total white count conceals severe neutropenia; a real failure mode for any system keyed on differentials.
- **Multi-lineage cytopenia** → Tier 0 or high Tier 1 as a **single** combination finding, not two or three separate cytopenias `[C]`. The clearest case in the exercise where consolidation-before-tiering (contract §9.1) does genuine clinical work: three separately-Tier-2 cytopenias are collectively a Tier 0/1 concern.

### 3.5 Iron
- **Low ferritin** → Tier 1, specific and actionable.
- **Raised ferritin, low/normal TSAT** → Tier 2, inflammatory/dysmetabolic framing `[E]`.
- **Raised ferritin, high TSAT** → Tier 1, distinct finding `[E]`. Lower magnitude, higher priority.
- **Absent TSAT despite available iron and transferrin** → TSAT is derivable as iron/TIBC. If HealthIQ holds the constituents it should compute it rather than declare it missing `[C]`. If it cannot, iron overload must not be implied to be excluded.
- **Iron findings with inflammation** → CRP conditions the reading; a "normal" ferritin with high CRP may mask deficiency `[C]`. Contract §3.1 in-range rule applies.
- **Iron findings with anaemia** → consolidate into one iron-deficiency-anaemia finding.

### 3.6 Thyroid
- **Raised TSH, low fT4** → overt hypothyroidism, Tier 1.
- **Raised TSH, normal fT4** → subclinical; Tier 2 below 10 mIU/L, Tier 1 at or above `[C]`.
- **Suppressed TSH, raised fT4** → overt hyperthyroidism, Tier 1; lower threshold for urgency than the hypo- direction `[C]`.
- **Isolated TSH abnormality, fT4 missing** → **the A1 case.** Cannot be resolved under contract v0.3 without either over-escalating a very common finding or defaulting low in a way that breaches §4.5.
- **Abnormal result, treatment or pregnancy status unavailable** → pregnancy is the sharper problem: trimester-specific ranges apply, and applying non-pregnant ranges causes both false alarm and false reassurance `[E]`. `[U]`

### 3.7 Cardiometabolic
- **Severely raised triglycerides** → Tier 0 above 20 mmol/L `[E]`. The only Tier 0 in the domain, and it is a *pancreatitis* risk, not a cardiovascular one — the explanation must say so or the user will misread the urgency.
- **Markedly raised LDL/TC** → Tier 1 at the NICE referral thresholds `[E]`.
- **Moderate abnormality, high aggregate risk** → Tier 1 or 2 depending on a risk calculation HealthIQ mostly cannot perform without context. `[U]`
- **Minor abnormality, major long-term consequence** → **the A3 case.** Under §4.2's current severity definition this lands Tier 2 and can be promoted only one tier. Probably survivable, but the mechanism is wrong: it treats a decades-long risk as a mild abnormality that got promoted, rather than as a different kind of severity.
- **Urgency versus long-term actionability discordance** → resolved correctly by dimension separation. Low urgency plus high actionability is exactly what the model is built to express.

### 3.8 Inflammatory
- **Isolated CRP elevation** → Tier 2. Not Tier 1 — the second clear counterexample to the hepatic Tier 1 floor.
- **Persistent inflammatory pattern** → Tier 1. Persistence, not height, promotes it.
- **CRP explaining ferritin** → CRP is Tier 3 contextual, attached to the iron finding.
- **Inflammatory markers with anaemia** → consolidated anaemia-of-chronic-disease pattern.
- **Non-specific abnormality without symptoms** → shown, Tier 2, with explicit low-specificity framing.

### 3.9 Nutritional
- **Severe deficiency with neurological/haematological consequence** → Tier 1, urgent framing. Urgency derives from irreversibility of neurological damage, not from the concentration `[E]`.
- **Borderline deficiency without corroboration** → Tier 2, confirmatory testing recommended.
- **Functional deficiency with in-range value** → contract §3.1 permits the finding; BSH supports it `[E]`. If the system produces nothing here, §3.1 is not implemented.
- **Marker distorted by inflammation/binding proteins** → confidence only.
- **Multiple deficiencies versus a more urgent direct finding** → deficiencies consolidate; the urgent finding leads.

### 3.10 Cross-domain lead contests

| Contest | Adjudication | Basis |
|---|---|---|
| Marked hepatic injury vs mild macrocytosis | Hepatic leads; macrocytosis contextual | Resolved by tier `[E]` |
| Thrombocytopenia vs suspected hepatic fibrosis | **Consolidate.** Usually one finding — low platelets in a hepatic context *is* the fibrosis signal `[E]`. Separate only where the count independently meets a haematological Tier 0/1 threshold | Contract §9.1 |
| Severe electrolyte abnormality vs high long-term CV risk | Electrolyte leads | **Urgency time-band** — hours versus decades. A2 |
| Acute renal decline vs chronic lipid risk | Renal leads | Same-day versus routine. A2 |
| Possible iron overload vs inflammatory ferritin | Iron overload leads at equal or lower ferritin | TSAT discriminator `[E]` |
| Multiple Tier 1s with different action pathways | **Co-leads**, capped at two per contract §7.4 | Contract |

**Where this remains unresolved:** two Tier 0 findings in different domains, both requiring same-day action. The time band does not separate them and no shared severity scale exists. `[U]` X1. Recommended interim behaviour: present both as co-leads with equal prominence rather than forcing an order. Forcing an order here would be arbitrary and the arbitrariness would be invisible to the user.

---

## 4. Confirmed universal rules

Held in all nine domains, with no domain requiring an exception.

| # | Rule | Note |
|---|---|---|
| U1 | The unit of prioritisation is a consolidated clinical finding, never a marker or frame | Strongest demonstration: multi-lineage cytopenia (§3.4) `[E]` |
| U2 | Urgency and severity are separable, and both are separable from confidence | Iron (high severity, no urgency) and electrolytes (low relative magnitude, high urgency) are the polar demonstrations `[E]` |
| U3 | Confidence affects explanation, never prominence | Thyroid stresses it (A1) but does not break it — A1 is a gap in *severity assignment*, not a case for confidence controlling prominence `[E]` |
| U4 | Supporting-marker count has no role in priority | No clinician in any domain counts corroborating markers to decide what matters `[E]` |
| U5 | Frames consolidate before tiering | Load-bearing in haematology and iron `[E]` |
| U6 | A finding that independently meets Tier 0/1 criteria may not be assigned contextual role | MCV, platelets, CRP and ferritin all have a magnitude above which contextual status is unsafe `[E]` |
| U7 | Missing data may reduce confidence, never clinical significance | One bounded exception below |
| U7a | **Bounded exception:** some markers are *uninterpretable* without a modifier and must produce an insufficient-data output rather than a low-confidence finding. Calcium without albumin is the reference case `[E]` | See A4 |
| U8 | Absent baseline is never evidence of stability | Critical in renal `[E]` |
| U9 | Direction asymmetry is the norm, not the exception | Ferritin, MCV, TSH, sodium, potassium, albumin `[E]` |
| U10 | Persistence more often *raises* concern than lowers it | **No domain produced a safe trend-based downgrade rule.** Contract §12.2's floor protection is doing real work `[E]` |

---

## 5. Domain-specific exceptions

| # | Exception | Domain | Note |
|---|---|---|---|
| D1 | Reference-range exceedance sets a Tier 1 floor | **Hepatic only.** BSG Rec 4 `[E]` | Must not universalise — §9 |
| D2 | Multiples of ULN as a severity metric | Hepatic (transaminases, ALP); cardiometabolic named thresholds `[E]` | Unsafe elsewhere |
| D3 | Absolute concentration as sole severity metric | Electrolytes `[E]` | |
| D4 | Absolute cell count as sole severity metric | Haematology `[E]` | |
| D5 | Change-from-baseline as the finding itself | Renal `[E]` | |
| D6 | Calculated long-term risk as severity | Cardiometabolic `[E]` | Requires A3 |
| D7 | Pattern relationship rather than magnitude as severity | Thyroid `[C]` | Requires A1 |
| D8 | A marker whose primary role is contextual to other domains | Inflammatory (CRP) `[J]` | |
| D9 | Urgency derived from irreversibility rather than magnitude | Nutritional (B12 neurological) `[E]` | |
| D10 | Mandatory artefact-confirmation language before urgent framing | Electrolytes, haematology (platelets), hepatic (AST/muscle) `[E]` | |

---

## 6. Cross-domain dependencies

| ID | Dependency | Blocks |
|---|---|---|
| X1 | Tier 0 versus Tier 0 across domains — unresolved `[U]` | Any panel producing two same-day findings |
| X2 | **Haematology bands are a dependency of hepatic, iron, inflammatory and nutritional** — not the reverse | Hepatic ruleset has three open dependencies on it |
| X3 | Renal function conditions electrolyte interpretation and vice versa | Both domains |
| X4 | Inflammatory status conditions iron and nutritional interpretation `[E]` | Iron, nutritional |
| X5 | Thyroid, hepatic and renal are secondary-cause exclusions for lipids `[E]` | Cardiometabolic |
| X6 | Albumin serves three domains in three different roles: hepatic synthetic marker, calcium modifier, negative acute-phase reactant `[E]` | Requires explicit governance so one domain's interpretation does not leak into another |
| X7 | Pregnancy status materially changes thyroid, hepatic, haematology and lipid interpretation `[E]` | All four; currently unaddressed |
| X8 | Context capture (alcohol, medication, symptoms, family history) — Wave 5 | Hepatic, cardiometabolic, nutritional, electrolytes |
| X9 | Tier 0 operational pathway (contract §17) | **Electrolytes, haematology and renal cannot be released without it**; hepatic can be released Tier-0-suppressed |

X6 deserves emphasis. Albumin is the clearest case in the landscape of a marker whose *meaning* is domain-conditional. Any design that assigns albumin a single interpretation will be wrong in two of three domains.

---

## 7. Proposed contract amendments

### A1 — Indeterminate severity rule (**required**)

**Gap:** contract v0.3 has no rule for assigning severity when a discriminating marker is absent and the finding is compatible with two materially different severity levels. §9.4's highest-severity inheritance governs *frames*, not missing discriminators, and applying it by analogy over-escalates.

**Proposed clause:**

> Where a finding is compatible with two or more severity levels and the discriminating marker is unavailable, the finding is assigned the **indeterminate** severity class. An indeterminate finding takes the tier of its *lower* plausible severity **plus one**, capped at the tier of its higher plausible severity, and must state both possibilities, name the discriminating test, and recommend it. Indeterminate status is a property of the finding, not a reduction in confidence, and may not be used to suppress a finding or to lower it below any applicable urgency floor.

Applied to the thyroid case: raised TSH with fT4 absent sits between subclinical (Tier 2) and overt (Tier 1). Lower plausible tier + 1 = Tier 1, capped at Tier 1 → **Tier 1, stating both, recommending fT4.** This escalates relative to the commonest truth and de-escalates relative to blanket worst-case, which is the correct trade for a finding whose resolution costs one additional test. `[J]`

**`[U]`** The Head of Medical Research should confirm the +1 rule rather than a straight worst-case rule. I have chosen it because worst-case inheritance compounds across a panel: four indeterminate findings under worst-case produce four escalated concerns and destroy the orienting value of the lead.

### A2 — Urgency expressed as a time band (**required**)

**Gap:** contract §7.2 orders by urgency then severity, but urgency is currently a tier and severity is domain-specific. Neither is cross-domain comparable, so §7.2 cannot actually adjudicate a hepatic Tier 1 against a haematological Tier 1.

**Proposed clause:**

> Urgency is expressed as a time-to-action band common to all domains: **same-day**, **within days**, **within weeks**, **routine**. Domain rules map their findings onto these bands using domain-appropriate criteria. Cross-domain ordering is adjudicated on the time band. Severity is used for ordering only within a domain. Where two findings from different domains share a time band and no governed cross-domain rule applies, they are presented as co-leads rather than ordered arbitrarily.

This is the highest-value amendment in the report. It makes §7.2 executable across domains without the shared severity scale that §20.10 defers, and does so using a dimension that is genuinely comparable — how long you have. `[J]`, structurally supported by the observation that every UK pathway examined expresses escalation in time terms (same-day discussion, urgent referral, routine referral, monitor).

### A3 — Long-term risk as a severity method (**required**)

**Gap:** §4.2 defines severity as "the degree of abnormality or dysfunction" and lists eight methods, none of which is calculated future risk.

**Proposed clause:** add to §4.2's list — *calculated long-term risk, where the domain's evidence base expresses consequence as future event probability rather than present dysfunction* — plus a note that a finding whose severity is expressed as long-term risk carries low urgency by construction and must be presented so that low urgency is not read as low importance. `[E]`, on the basis that NICE lipid guidance is entirely risk-framed.

### A4 — Uninterpretable-without-modifier rule (**recommended**)

**Gap:** §8 and §16.2 distinguish missing supporting markers (confidence) from insufficient data (no assessment). They do not cover the middle case: a marker present but uninterpretable without a specific companion.

**Proposed clause:**

> Where a governed rule identifies a marker as uninterpretable without a named modifier, absence of that modifier produces an insufficient-data output for that finding, not a low-confidence finding. Uncorrected calcium without albumin is the reference case. Such pairs must be enumerated per domain.

Also fold in the hepatic ruleset's HEP-MISS-1 here — a combination criterion that cannot be evaluated must be reported as *not assessable* rather than *not met*. It applies to every combination rule in every domain and should not sit inside a single domain asset. `[E]`

### A5 — Domain-conditional marker meaning (**recommended**)

Where a marker carries different clinical meaning in different domains (albumin being the reference case), each domain rule must declare its own interpretation, and no domain's interpretation may be applied outside it. `[E]`

### A6 — Consolidation across domains (**recommended**)

**Gap:** §9.1 consolidates frames over the same analyte. It does not address findings from *different* domains that are clinically one thing — thrombocytopenia plus hepatic abnormality being the reference case.

**Proposed clause:** governed combination rules may consolidate findings across domain boundaries where the constituents form a single recognised clinical entity. The consolidated finding inherits the highest urgency band and remains subject to §4.8 — a constituent that independently meets Tier 0/1 criteria may not be absorbed. `[E]`

---

## 8. Prohibited universalisation list

Tested explicitly per spec §8.5.

| # | Candidate | Verdict | Reason |
|---|---|---|---|
| P1 | Multiples of ULN as a universal severity metric | **Prohibited** | K⁺ 6.6 is ~1.25× ULN and an emergency; MCV 99.5 is 1.04× ULN and often nothing `[E]` |
| P2 | Reference-range abnormality as a universal Tier 1 floor | **Prohibited** | Hepatic-specific, from BSG Rec 4. Falsified by isolated macrocytosis and isolated CRP, both of which UK guidance treats as low-concern `[E]` |
| P3 | Supporting-marker count | **Prohibited universally** | No domain requires it; it is an inverse proxy for panel completeness `[E]` |
| P4 | Requirement for corroboration before a finding is raised | **Prohibited** | Would suppress functional B12 deficiency with a normal serum level `[E]` and single-marker electrolyte emergencies |
| P5 | Trend-based downgrading | **Prohibited as a general mechanism** | No domain produced a safe one; hepatic evidence actively contradicts it `[E]`. Permitted only via a governed, sourced override subject to the floor |
| P6 | Static domain priority | **Prohibited** | Same defect as static IDL priority — an authoring-time constant competing with patient data |
| P7 | Fixed ordering of marker classes | **Prohibited** | Iron sometimes outranks hepatic, hepatic sometimes outranks haematology; correct order is data-dependent |
| P8 | Worst-case severity inheritance under missing data | **Prohibited as a blanket rule** | Compounds across a panel; see A1 |
| P9 | Percentage differentials for white cell interpretation | **Prohibited** | Absolute counts only; percentages conceal severe neutropenia `[C]` |
| P10 | Hepatic-style "any abnormality warrants an aetiology screen" framing | **Prohibited outside hepatic** | Domain-bound `[E]` |

---

## 9. The hepatic contamination check (breadth gate item 8)

The spec required explicit confirmation that no hepatic-specific concept has silently become universal.

**Contaminating concept found: one.** HEP-PRINCIPLE-2, the Tier 1 floor for reference-range exceedance. Correct for hepatic, wrong for at least three other domains. Recorded as D1/P2 and must be relabelled domain-bound in the hepatic ruleset before that ruleset is reused.

**Concepts checked and found safely generalisable:** consolidation before tiering; function-outranks-injury (generalises as *organ dysfunction outranks marker abnormality*); the contextual-role boundary; missing-marker-affects-confidence-only; the not-assessable formulation for unevaluable criteria.

**Concept needing generalisation in the other direction:** HEP-MISS-1 is a good rule sitting in the wrong document. It belongs in the contract — folded into A4.

---

## 10. Recommended sequence for detailed ruleset authoring

Assessed against spec §10. **Hepatic is not recommended first.**

### First: haematology

- **Cross-domain dependency value — decisive.** Four domains depend on haematology bands (X2). The hepatic ruleset already has three open dependencies on it and currently carries a placeholder (a 10%-of-ULN MCV margin explicitly labelled non-clinical). Placeholders in a governed asset become precedent.
- **Model-testing value — high.** Tests absolute-count severity, the contextual/independent boundary, multi-lineage consolidation and direction asymmetry. It also contains the clearest falsification of the hepatic Tier 1 floor, which should be established early rather than late.
- **Guidance availability — good.** BSH guidelines, NHS trust haematology referral guides, NHS Scotland macrocytosis pathways.
- **Coverage — highest.** The FBC is on virtually every panel HealthIQ will see.
- **Regulatory — moderate.** No calculated risk score of the FIB-4 kind.
- **Constraint:** Tier 0 content (severe cytopenias) requires the §17 pathway. Tier 1 and below can be authored and released without it.

### Second: hepatic

Already drafted; blocking dependencies close once haematology lands. Reconcile HEP-U1 with the P2 finding here and relabel HEP-PRINCIPLE-2 as domain-bound.

### Third: renal and electrolytes together

Mutually conditioning (X3); authoring them separately will produce two incompatible treatments of the potassium/renal interaction. Both require the §17 Tier 0 pathway. Renal additionally requires a decision on longitudinal baseline capture, without which the domain's principal finding is undetectable.

### Fourth: iron, then inflammatory

Both are largely defined by their interactions, which makes them poor early domains.

### Fifth: thyroid

Should not be authored until A1 is ratified — it is the domain that generates the amendment and the one that most depends on it. Also requires a pregnancy decision (X7).

### Sixth: cardiometabolic, then nutritional

Cardiometabolic depends on A3 and on context capture, most of which is Wave 5. Authoring it earlier produces rules that cannot run.

**Not recommended for detailed authoring in this phase:** coagulation. Almost all abnormalities are acute, HealthIQ has no clinical context, and a scoping decision on whether to interpret the domain at all should precede rule writing. `[U]`

---

## 11. Evidence table

| Source | Domains |
|---|---|
| Newsome PN et al., BSG. Guidelines on the management of abnormal liver blood tests. *Gut* 2018;67(1):6–19 | Hepatic |
| NHS Devon; NHS Specialist Pharmacy Service; NHS Highland abnormal-LFT pathways | Hepatic |
| UK Kidney Association / Renal Association hyperkalaemia guideline | Electrolytes, renal |
| NHS Greater Glasgow & Clyde — hyponatraemia and hypercalcaemia management guidance | Electrolytes |
| NHS Kent & Medway hypercalcaemia network guidance; North Bristol primary-care hypercalcaemia guideline | Electrolytes |
| NICE NG148 — Acute kidney injury | Renal |
| NHS trust haematology GP referral guides (Barts Health; King's Health Partners; Newcastle) | Haematology |
| NHS Scotland Right Decisions / RefHelp; NHS Highland; NHS Kernow — macrocytosis pathways | Haematology, hepatic |
| BSH — Investigation and management of a raised serum ferritin, *Br J Haematol* 2018 | Iron |
| EASL haemochromatosis guideline 2022; BC Guidelines iron overload | Iron |
| BSH / BCSH — Guidelines for the diagnosis and treatment of cobalamin and folate disorders, *Br J Haematol* 2014 | Nutritional |
| NICE CG181 — CVD risk assessment and lipid modification | Cardiometabolic |
| NICE CG71 — Familial hypercholesterolaemia (via CG181 cross-reference) | Cardiometabolic |
| NHS RUH Bath — Assessment and management of lipids in primary care | Cardiometabolic |
| Subclinical hypothyroidism treatment-threshold literature (TSH >10 mIU/L convention) | Thyroid — `[C]`, no UK guideline directly cited |
| RCPath — alert systems and communication of unexpected findings; ACB UK critical alert limits survey | All — Tier 0 framing |
| EASL / AASLD DILI guidance | Hepatic — international, used where UK guidance is silent |

**Evidence gaps material to the conclusions:**
- No UK guideline provides a cross-domain severity or priority scale. A2 is a structural proposal, not an evidence-derived one.
- Thyroid thresholds rest on convention rather than a cited UK guideline in the sources reviewed. **The weakest evidence base of the nine domains, reinforcing the recommendation to sequence thyroid late.** `[U]`
- Inflammatory-marker severity banding has no authoritative UK source. CRP's role here is judgement.
- No guidance exists anywhere on laboratory interpretation without clinical context, which is HealthIQ's actual operating condition in every domain.

---

## 12. Unresolved clinical questions

| ID | Question | Blocking |
|---|---|---|
| X1 | Tier 0 versus Tier 0 across domains | Yes — will occur in production |
| CD1 | A1's +1 rule versus straight worst-case inheritance | Yes — determines thyroid and several other domains |
| CD2 | Potassium urgent threshold: UK Renal Association >6.5 or CCS/KDIGO >6.0, for a consumer product | Yes |
| CD3 | Pregnancy handling across thyroid, hepatic, haematology and lipids (X7) | Yes |
| CD4 | Whether coagulation is interpreted at all | Yes, for scope |
| CD5 | Which findings HealthIQ may compute at all without context (alcohol, medication, symptoms, family history) | Yes — determines what any ruleset can do at launch |
| CD6 | Whether calculated scores (FIB-4, QRISK-type, FH criteria) are within the intended product purpose, given contract §22 | Yes — regulatory interaction |
| CD7 | Baseline capture and validity windows per domain | Yes for renal |
| CD8 | The hepatic Tier 1 floor decision (HEP-U1), now with P2 as additional input | Yes for hepatic |
| CD9 | Whether an insufficient-data output for one domain suppresses that domain silently or is stated | Recommended: stated `[J]` |

CD5 is the one I would push hardest. Every domain in this exercise produced rules whose source guidance assumes a clinician holds context HealthIQ does not have. That does not make interpretation impossible — but the decision about which rules are *unsafe* without context, as opposed to merely lower-confidence, has not been made anywhere in the governance chain. It is not a confidence question. It is a scope question, and it belongs to the Head of Medical Research.

---

## VERDICT: VALIDATE_WITH_CONTRACT_AMENDMENTS

**Breadth gate result:** 8 of 10 items pass unconditionally (1, 2, 3, 4, 5, 6, 8, 9). Item 7 (cross-domain contests) passes conditionally on A2, with X1 explicitly bounded rather than resolved. Item 10 (safe authoring sequence) passes, with the sequence at §10 differing from the assumed one.

**Required amendments:** A1 (indeterminate severity), A2 (urgency time bands), A3 (long-term risk as severity method). A4–A6 recommended.

**Assessment.** The contract's central bet — that separating urgency, severity, confidence and context is safer than any single ranking score — is vindicated by breadth testing. Nine unlike domains expressed their findings in the same dimensions without a single case requiring confidence to control prominence or supporting-marker count to determine priority. That is a stronger result than the exercise needed to produce.

The three required amendments are all additions rather than corrections, and two of them (A1, A3) were generated by domains the original contract could not have been written against. That is the exercise working as intended.

The most important non-amendment finding is §9: the hepatic ruleset contains one concept that would be actively unsafe if generalised, and it was on a path to generalisation by virtue of being the first domain authored. Sequencing haematology first is partly a defence against that — it establishes the counterexample in a governed asset before hepatic conventions harden into house style.
