---
document_id: HEALTHIQ-CARDIO-NUTRI-RULESET-001
title: HealthIQ Cardiometabolic and Nutritional Prioritisation Ruleset
version: "0.1"
workstream: F
governing_contract: HEALTHIQ-CLIN-PRIORITY-CONTRACT-001 v0.5
status: DRAFT_FOR_CENTRAL_RECONCILIATION
implementation_status: NOT_AUTHORISED
---

# Cardiometabolic and Nutritional Prioritisation Ruleset v0.1

> **Contract availability note.** Authored against contract v0.4 plus the v0.5 principle summary in authoring spec §2. Re-check at reconciliation.

**Evidence labels:** `[E]` · `[C]` · `[J]` · `[U]`.

---

## 1. Scope and the two defining characteristics

**In scope:** total cholesterol, non-HDL cholesterol, LDL, HDL, triglycerides, HbA1c, fasting glucose where available; B12, folate, vitamin D, homocysteine where governed.

**Out of scope:** paediatric; pregnancy; established diabetes management; statin dosing or any treatment recommendation; genetic lipid disorder diagnosis; nutritional supplementation dosing.

### 1.1 Cardiometabolic — severity is future risk, not present abnormality

**CN-P1 `[E]`** — This is the domain that required contract §4.2's ninth severity method. NICE lipid guidance is entirely risk-framed: it directs using clinical findings, lipid profile and family history to judge the likelihood of a familial lipid disorder **rather than strict lipid cut-off values alone** `[E]`. An LDL of 6.0 mmol/L is barely abnormal by distance-from-range and profoundly consequential over decades.

**CN-P2 `[J]`** — Consequently, **low urgency must never be presented as low importance** in this domain (contract §4.2). This is the domain where that clause does its work.

### 1.2 Nutritional — urgency is irreversibility, not magnitude

**CN-P3 `[E]`** — B12 deficiency can produce neuropsychiatric and spinal-cord manifestations that precede or occur without anaemia or macrocytosis, and neurological recovery may be incomplete if treatment is delayed. Urgency here derives from **irreversibility of harm**, not from how low the concentration is.

**CN-P4 `[E]`** — BSH is explicit that the clinical picture is the most important factor in assessing cobalamin status because there is no gold-standard test. A serum B12 in range does not exclude functional deficiency.

### 1.3 Why these two halves share a workstream

Both are dominated by **context HealthIQ does not hold** — for lipids, the risk-factor set required to compute risk; for nutrition, diet, symptoms and absorption history. Both produce findings whose severity method is unusual. Pairing them keeps that shared limitation in one governance conversation. `[J]`

---

## 2. Clinician first-look hierarchy

| Attention | Markers |
|---|---|
| **First look — cardiometabolic** | Total cholesterol, non-HDL cholesterol, triglycerides, HbA1c `[E]` |
| **First look — nutritional** | B12, folate, plus Hb and MCV from haematology `[C]` |
| **Conditional** | LDL, HDL, fasting glucose, vitamin D, homocysteine, MMA |
| **Low yield alone** | HDL; vitamin D in most contexts `[C]` |
| **Preferred over LDL** | Non-HDL cholesterol — NICE recommends non-HDL rather than LDL for measuring and monitoring, and does not require fasting samples `[E]` |

**CN-FL-1 `[E]`** — HealthIQ should present non-HDL cholesterol in preference to LDL where both are available. This is a UK-specific position and differs from international convention.

---

## 3. Canonical finding taxonomy

| ID | Finding | Constituents |
|---|---|---|
| CN-F1 | Severe hypertriglyceridaemia | Triglycerides |
| CN-F2 | Possible familial hypercholesterolaemia pattern | Total cholesterol / non-HDL ± family history |
| CN-F3 | Elevated long-term cardiovascular risk | Lipid profile + risk factors |
| CN-F4 | Dysglycaemia (non-diabetic hyperglycaemia or diabetes range) | HbA1c ± fasting glucose |
| CN-F5 | B12 deficiency | B12 ± MMA/homocysteine ± Hb/MCV |
| CN-F6 | Folate deficiency | Folate ± Hb/MCV |
| CN-F7 | Functional B12 deficiency with in-range serum level | B12 in range + clinical/haematological/metabolic markers |
| CN-F8 | Vitamin D deficiency | 25-OH vitamin D |
| CN-F9 | Indeterminate lipid risk | Lipids without the risk-factor set |

**CN-CONS-1 `[E]`** — Total cholesterol, non-HDL, LDL, HDL and triglycerides form **one** lipid finding, not five. Presenting each fraction as a concern is the clearest possible violation of contract §3.1.

**CN-CONS-2 `[C]`** — B12 and folate consolidate with any accompanying anaemia into **one** finding jointly owned with haematology.

**CN-CONS-3 `[J]`** — Vitamin D does not consolidate with B12/folate. Different pathway, different action.

---

## 4. Urgency rules and time bands

### 4.1 Same day

| ID | Criterion | Basis |
|---|---|---|
| **CN-U-SD-1** | **Triglycerides >20 mmol/L**, not explained by excess alcohol or poor glycaemic control | NICE CG181: refer for **urgent** specialist review. Pancreatitis risk `[E]` |

**CN-U-SD-2 `[U]`** — Should severe symptomatic hyperglycaemia (very high HbA1c, or high glucose with symptoms) generate a same-day band? HealthIQ has no symptoms and HbA1c is a 3-month average, not an acute measure. Currently no. Flagged.

**CN-U-SD-1 is specification-only pending contract §17 — see §13.**

**CN-U-SD-NOTE `[E]` — communication requirement.** The urgency here is **pancreatitis**, not cardiovascular. If the explanation does not say so, the reader will misclassify the risk and may reasonably conclude it can wait. This is the domain's sharpest communication requirement.

### 4.2 Within days

| ID | Criterion | Basis |
|---|---|---|
| CN-U-D-1 | Triglycerides 10–20 mmol/L | NICE: repeat with a fasting test after 5 days but within 2 weeks; specialist referral advisable above 10 `[E]` |
| CN-U-D-2 | B12 deficiency **with** neurological features | Urgent referral where neurological deficits are present `[E]` — but HealthIQ has no symptoms, so this fires only on user-reported context. `[U]` CN-U1 |
| CN-U-D-3 | B12 deficiency with pancytopenia | Cross-domain; haematology primary `[E]` |

### 4.3 Within weeks

| ID | Criterion | Basis |
|---|---|---|
| CN-U-W-1 | Total cholesterol >9.0 mmol/L **or** non-HDL >7.5 mmol/L | NICE: arrange specialist assessment even in the absence of a first-degree family history of premature CHD `[E]` |
| CN-U-W-2 | Total cholesterol >7.5 mmol/L with family history of premature CHD | NICE: consider FH and investigate per the FH guideline `[E]` |
| CN-U-W-3 | HbA1c ≥48 mmol/mol | Diabetes diagnostic range `[C]` |
| CN-U-W-4 | Clear B12 or folate deficiency without neurological or multi-lineage features | `[E]` |
| CN-U-W-5 | CN-F7 functional B12 deficiency | `[E]` |
| CN-U-W-6 | Triglycerides 4.5–9.9 mmol/L with non-HDL >7.5 | NICE: seek specialist advice `[E]` |

### 4.4 Routine

| ID | Criterion | Basis |
|---|---|---|
| CN-U-R-1 | CN-F3 elevated long-term CVD risk without a named referral threshold being met | `[E]` — risk-framed, not urgency-framed |
| CN-U-R-2 | HbA1c 42–47 mmol/mol (non-diabetic hyperglycaemia) | `[C]` |
| CN-U-R-3 | Triglycerides 2.3–4.4 mmol/L | `[C]` |
| CN-U-R-4 | Vitamin D deficiency without other abnormality | `[C]` |
| CN-U-R-5 | Borderline B12 or folate without corroboration | `[E]` |

**CN-U-NEG-1 `[E]`** — NICE directs excluding common secondary causes of dyslipidaemia — excess alcohol, uncontrolled diabetes, hypothyroidism, liver disease, nephrotic syndrome — **before** referring for specialist review. HealthIQ can check three of these on the same panel (HbA1c, thyroid, hepatic) and must do so before framing a lipid finding as requiring specialist referral. See CN-OV-5.

---

## 5. Severity rules

**Two severity methods, both unusual, neither transferable.**

### 5.1 Cardiometabolic — calculated long-term risk plus named referral thresholds

| Threshold | Value | Source |
|---|---|---|
| Urgent specialist review | TG >20 mmol/L | NICE CG181 `[E]` |
| Specialist referral advisable | TG >10 mmol/L | NICE `[E]` |
| Risk underestimated by tools | TG 4.5–9.9 mmol/L | NICE `[E]` |
| Specialist assessment regardless of family history | TC >9.0 or non-HDL >7.5 mmol/L | NICE `[E]` |
| Consider FH | TC >7.5 mmol/L with family history | NICE `[E]` |
| FH criteria (Simon Broome, adult) | TC >7.5 or LDL >4.9 mmol/L with tendon xanthomas or genetic confirmation | `[C]` |
| Diabetes range | HbA1c ≥48 mmol/mol | `[C]` |
| Non-diabetic hyperglycaemia | HbA1c 42–47 mmol/mol | `[C]` |

**CN-S-1 `[E]`** — NICE explicitly directs using clinical findings, lipid profile and family history to judge likelihood of a familial disorder **rather than strict cut-offs alone.** The thresholds above are referral triggers, not severity grades, and must be presented as such.

**CN-S-2 `[E]`** — Risk assessment tools must **not** be used in people with familial hypercholesterolaemia or other inherited lipid disorders, and the QRISK CKD tick-box should not be driven from eGFR. HealthIQ cannot reliably identify FH, which constrains what it may compute. `[U]` CN-U2.

### 5.2 Nutritional — consequence, not concentration

**CN-S-3 `[E]`** — There is no gold-standard test for cobalamin status and the clinical picture is the most important factor. Serum B12 concentration is therefore a weak severity input.

**CN-S-4 `[E]`** — Severity is driven by **consequence class**: neurological features > multi-lineage haematological features > isolated macrocytosis or anaemia > biochemical abnormality alone.

**CN-S-5 `[C]`** — MCV >115 fL is reported as more specific for B12/folate deficiency than other causes of macrocytosis, and is therefore a severity-relevant supporting pattern — consumed from the haematology band, not redefined here.

**CN-S-6 `[U]`** — Vitamin D bands (commonly <25 nmol/L deficient, 25–50 insufficient) are widely used in UK practice but were not confirmed against a cited NICE or SACN source in this exercise. **Not adopted in this version.** Flagged rather than imported.

---

## 6. Indeterminate-severity rules

| ID | Situation | Plausible states | Missing discriminator | Disposition |
|---|---|---|---|---|
| CN-IND-1 | Raised cholesterol, no family history, no risk factors | FH (weeks, specialist) vs common dyslipidaemia (routine) | Family history, risk-factor set | **CN-F9.** Where a named NICE threshold is met, band on that threshold — it applies *regardless of family history* `[E]`. Below it, band routine and state that FH could not be assessed `[J]` |
| CN-IND-2 | Raised triglycerides, alcohol and glycaemic status unknown | Requires urgent referral vs explained by a secondary cause | Alcohol intake, HbA1c | HbA1c is often on the same panel — **check it first** (CN-OV-5). Alcohol is not available; the >20 rule fires with the qualifier stated, not suppressed `[E]` |
| CN-IND-3 | Low-ish B12, no MMA/homocysteine, no symptoms | Functional deficiency (weeks) vs analytically low but sufficient (routine) | MMA or homocysteine; symptoms | Floor at routine with confirmatory testing recommended; **may not report B12 status as normal** `[E]` |
| CN-IND-4 | In-range B12 with macrocytosis or neurological context | Adequate vs functional deficiency | MMA, homocysteine, holotranscobalamin | **CN-F7**, within weeks. Contract §3.1 in-range rule `[E]` |
| CN-IND-5 | Raised HbA1c, single result | Diabetes (requires confirmation) vs transient/analytical | Second HbA1c | Diabetes diagnosis requires confirmation; band on the range but **may not assert a diagnosis** `[C]` |

---

## 7. Trend and baseline rules

**Cardiometabolic: largely cross-sectional for risk; trend-important for treatment response. Nutritional: trend-modifying.**

| ID | Rule | Class |
|---|---|---|
| CN-T1 | CVD risk is computed cross-sectionally; a single lipid profile is sufficient for the calculation `[E]` | `[E]` |
| CN-T2 | HbA1c reflects roughly 3 months of glycaemia; two values <3 months apart do not represent independent timepoints `[C]` | `[C]` |
| CN-T3 | Diabetes diagnosis on HbA1c requires confirmation on a second sample in asymptomatic people `[C]` | `[C]` |
| CN-T4 | Falling B12 within range across serial results may indicate depleting stores — contract §3.1 `[C]` | `[C]` |
| CN-T5 | No trend-based downgrade rule. Lipids improving on treatment is a treatment-response finding, not a reason to lower a finding below its floor | `[J]` |
| CN-T6 | Baseline validity: HbA1c ≥3 months; lipids 12 months; B12 12 months `[J]` — unsourced | `[J]` |

---

## 8. Modifier and interpretability rules

| Marker | Required modifier | Without it |
|---|---|---|
| **Lipid profile (for CVD risk)** | **Age, sex, smoking, blood pressure, diabetes status, family history** | Risk **cannot be computed**. CN-F9 indeterminate — named referral thresholds still apply because NICE frames them independently of family history `[E]` |
| Triglycerides >20 (for the urgent rule) | Alcohol intake, glycaemic control | Rule fires with the qualifier stated. **Must not be suppressed** because the exclusions are unavailable `[E]` |
| Lipids (for specialist referral framing) | Thyroid, hepatic, HbA1c, renal — secondary causes | Check what is on the panel; state what could not be excluded `[E]` |
| B12 (for functional status) | MMA or homocysteine | Functional deficiency not assessable; do not report B12 as normal `[E]` |
| B12/folate (for haematological consequence) | Hb, MCV | Consequence not assessable `[C]` |
| HbA1c | — | Invalid in conditions affecting red cell survival (haemolysis, recent transfusion, haemoglobinopathy) `[C]` — `[U]` CN-U3 |

**CN-MOD-1 `[E]`** — The triglyceride case deserves emphasis. NICE's urgent-referral rule is written with two exclusions HealthIQ cannot check. **The correct behaviour is to fire the rule and state the exclusions, not to withhold it.** Withholding an urgent finding because a mitigating explanation cannot be ruled out is exactly the suppression contract §18 prohibits.

---

## 9. Combination and override register

| ID | Trigger | Direction | Effect | Basis |
|---|---|---|---|---|
| CN-OV-1 | TG >20 mmol/L | Promote | Same day; pancreatitis framing mandatory | `[E]` |
| CN-OV-2 | TC >9.0 or non-HDL >7.5 | Promote | Within weeks, specialist assessment | `[E]` |
| CN-OV-3 | TC >7.5 + family history of premature CHD | Promote | Within weeks, FH pathway | `[E]` |
| CN-OV-4 | TG 4.5–9.9 + non-HDL >7.5 | Promote | Within weeks | `[E]` |
| CN-OV-5 | Abnormal lipids + abnormal thyroid, hepatic, HbA1c or renal on the same panel | **Cross-domain classify** | Secondary cause identified; lipid finding reframed, **not downgraded**. State which cause and that it should be addressed first | `[E]` |
| CN-OV-6 | B12 or folate deficiency + macrocytosis | **Cross-domain consolidate** | One finding with haematology | `[E]` |
| CN-OV-7 | B12 deficiency + pancytopenia | **Cross-domain promote** | Haematology same-day rule fires; haematology primary | `[E]` |
| CN-OV-8 | In-range B12 + macrocytosis or neurological context | Promote | CN-F7 | `[E]` |
| CN-OV-9 | HbA1c ≥48 + lipid abnormality | Promote | Both stand; dysglycaemia is also a lipid secondary cause (CN-OV-5) | `[E]` |

**CN-OV-5 note.** This is a **reframing**, not a downgrade. NICE directs excluding secondary causes before *referral*, not before *concern*. A lipid abnormality explained by untreated hypothyroidism is still a lipid abnormality; what changes is the recommended action. Contract §13 forbids the override lowering the finding below its floor.

---

## 10. Contextual markers and confidence-only factors

**Contextual:**

| Marker | Role | Becomes independent when |
|---|---|---|
| HDL | Constituent of the lipid finding `[C]` | Never independent |
| LDL | Constituent; superseded by non-HDL in UK practice `[E]` | Never independent |
| Vitamin D | Usually contextual `[J]` | `[U]` CN-U4 — no band adopted (CN-S-6) |
| Homocysteine, MMA | Confirmatory for B12 status `[E]` | Never independent |
| eGFR | Contextual to CVD risk `[E]` | Renal domain is always primary for the renal finding itself |
| Thyroid pattern | Contextual as lipid secondary cause | Thyroid domain primary for the thyroid finding |

**Confidence-only:** absent family history; absent BP, smoking, ethnicity, BMI; absent treatment status (statin, metformin, B12 injections); absent diet and absorption history; absent symptoms; non-fasting sample (acceptable for lipids per NICE `[E]`, relevant for glucose).

**CN-CONF-1 `[E]`** — Absent risk factors do not lower a lipid finding's tier. They prevent risk *computation*, which is a different thing and routes to CN-F9.

---

## 11. Concern-tier mapping and lead selection

| Tier | Content |
|---|---|
| **Tier 0** | CN-F1 (TG >20) — **the domain's only Tier 0 content** |
| Tier 1 | TG 10–20; TC >9.0 / non-HDL >7.5; TC >7.5 with family history; HbA1c ≥48; clear B12/folate deficiency; CN-F7 |
| Tier 2 | CN-F3 elevated long-term risk; HbA1c 42–47; TG 2.3–4.4; borderline B12/folate; vitamin D deficiency |
| Tier 3 | HDL, LDL as constituents; vitamin D as context; eGFR and thyroid as CVD-risk or secondary-cause context |

**CN-LEAD-1 `[E]`** — CN-F1 leads unconditionally within the domain.

**CN-LEAD-2 `[E]`** — B12 deficiency with neurological or multi-lineage features leads over any lipid finding, because irreversibility outranks long-horizon risk at the same time band.

**CN-LEAD-3 `[J]`** — Tier 2 long-term risk findings will rarely lead a panel and should not. But **CN-P2 applies to their presentation**: not leading must not read as not mattering.

**CN-LEAD-4** — Cross-domain contests resolve on the common time band only. This domain's severity — a risk percentage, or a consequence class — is not comparable with any other domain's severity and must never be compared (contract §18.24).

---

## 12. Tier 0 specification-only register

| Rule | Status |
|---|---|
| CN-U-SD-1 (TG >20) | **Specification-only** |

Single Tier 0 rule. Everything else is release-eligible. Where suppressed, withheld with a statement — never demoted.

---

## 13. Acceptance scenarios

| # | Panel | Expected |
|---|---|---|
| AS-1 | TG 24 mmol/L, HbA1c 40, no alcohol data | **Tier 0, same day.** Fires with the exclusion qualifier stated. HbA1c checked and normal, so poor glycaemic control excluded; alcohol stated as unassessed. **Pancreatitis framing mandatory** |
| AS-2 | TG 24 mmol/L, HbA1c 78 | Tier 0 stands, but CN-OV-5 reframes: poor glycaemic control is a plausible secondary cause and should be addressed. **Not downgraded** |
| AS-3 | TC 9.4, non-HDL 7.8, no family history | **Tier 1, within weeks.** NICE threshold applies regardless of family history — tests that CN-IND-1 does not suppress on missing history |
| AS-4 | TC 7.9, no family history, no risk factors | **CN-F9**, Tier 2 routine. FH could not be assessed; state it. Risk not computable |
| AS-5 | LDL 5.2, HDL 1.1, TC 7.2, TG 1.8 | **One** lipid finding, Tier 2. Not four. Non-HDL presented in preference to LDL |
| AS-6 | HbA1c 52, single result | Tier 1, within weeks. **May not assert a diabetes diagnosis** — confirmation required |
| AS-7 | B12 120 ng/L, Hb 98, MCV 112 | **One** consolidated finding with haematology (CN-OV-6), Tier 1, within weeks |
| AS-8 | B12 320 ng/L (in range), MCV 108, normal Hb | **CN-F7**, Tier 1. In-range value, real finding. Tests contract §3.1 and CN-P4 |
| AS-9 | B12 110, Hb 82, platelets 90, neutrophils 1.2 | **Haematology primary and same-day** (pancytopenia). B12 is the aetiology within that finding, not a competitor (CN-OV-7) |
| AS-10 | TC 8.8, TSH 12, free T4 low | Lipid finding **reframed** by CN-OV-5 — hypothyroidism is a secondary cause NICE directs excluding before referral. Both findings stand; thyroid leads on actionability within the same band `[J]` |
| AS-11 | Vitamin D 18 nmol/L, all else normal | **No band adopted** (CN-S-6). Finding created and shown at Tier 2 with an explicit statement that HealthIQ has not adopted a governed threshold. Tests that absence of a band does not become suppression |
| AS-12 | TG 24 **and** K⁺ 6.8 | **Same-day co-equal group.** Both presented; no ordering; no severity comparison between a triglyceride and a potassium |
| AS-13 | Complete normal lipid and nutritional panel | No-concern output; must state that a normal lipid profile does not exclude cardiovascular risk from other factors, and that a normal B12 does not exclude functional deficiency |

---

## 14. No-concern and insufficient-data outputs

**No-concern — mandatory content:**
1. A normal lipid profile does not mean low cardiovascular risk — risk depends on age, blood pressure, smoking, diabetes and family history, most of which were not available `[E]`.
2. A normal serum B12 does not exclude functional deficiency `[E]`.
3. Whether cardiovascular risk could be computed; if not, that it was not assessed.
4. Symptoms — particularly neurological symptoms — warrant review irrespective of the summary `[E]`.

**CN-NC-1 `[J]`** — "Your cholesterol is fine" and "your heart risk is low" are both prohibited. HealthIQ measures lipids; it does not measure cardiovascular risk without the risk-factor set.

**Insufficient data:** minimum viable lipid assessment is **total cholesterol + triglycerides**. Minimum viable nutritional assessment is **B12 or folate**. Where the risk-factor set is unavailable, CN-F9 is issued with an explicit not-computed statement — a finding, not an insufficient-data output, because the named referral thresholds remain applicable.

---

## 15. Cross-domain boundaries

| Marker | This domain's role | Other domain primary when | Disposition |
|---|---|---|---|
| Hb, MCV | Consequence of deficiency | **Haematology always** — owns the anaemia and macrocytosis findings and their bands | **Consolidate**; nutritional supplies aetiology |
| Thyroid pattern | Lipid secondary cause | Thyroid domain owns the thyroid finding | Attach contextually; both stand |
| Hepatic analytes | Lipid secondary cause | Hepatic domain primary | Attach contextually |
| eGFR | CVD-risk context; also a lipid secondary cause via nephrotic syndrome | Renal always primary | Attach contextually |
| HbA1c | Primary; also a lipid secondary cause | — | Owned here; dual role within the domain |
| Ferritin | Not used here | Iron domain | — |
| Sodium | Not used here, but severe hypertriglyceridaemia can falsely lower it `[E]` | Renal/electrolyte primary | **Cross-reference required** — a low sodium alongside TG >20 may be artefactual |

**CN-XD-1 `[E]`** — The sodium cross-reference is a genuine safety item: severe hypertriglyceridaemia producing pseudohyponatraemia could otherwise generate a spurious same-day electrolyte finding alongside a genuine same-day lipid finding. The central register must carry this.

---

## 16. Prohibited behaviours (domain additions)

1. Presenting lipid fractions as separate concerns.
2. Presenting cardiovascular risk as assessed when the risk-factor set was unavailable.
3. Suppressing the TG >20 rule because alcohol or glycaemic status is unknown.
4. Framing TG >20 urgency as cardiovascular rather than pancreatitis.
5. Asserting a diabetes diagnosis from a single HbA1c.
6. Downgrading a lipid finding because a secondary cause was identified.
7. Using LDL in preference to non-HDL where both are available.
8. Reporting B12 status as normal on an in-range value where macrocytosis or neurological context is present.
9. Adopting vitamin D bands not confirmed against a UK source.
10. Applying risk assessment tools where FH is suspected.
11. Recommending statin initiation, dose or cessation.
12. Importing the hepatic Tier 1 floor — a mildly raised cholesterol is not a within-weeks finding.

---

## 17. Unresolved questions

| ID | Question | Blocking |
|---|---|---|
| CN-U1 | B12 with neurological features requires user-reported symptoms. Does HealthIQ collect them, and may a rule depend on self-report? | **Yes** |
| CN-U2 | Which risk calculation, if any, may HealthIQ perform? QRISK-type tools are the most device-like output in the landscape — regulatory interaction under contract §22 | **Yes — regulatory** |
| CN-U3 | HbA1c invalidity in haemoglobinopathy, haemolysis and recent transfusion. HealthIQ may detect some of these from the FBC | Yes |
| CN-U4 | Vitamin D bands — not adopted (CN-S-6). Confirm against SACN/NICE or decline the marker | **Yes** |
| CN-U5 | Homocysteine and MMA availability and governance | Yes |
| CN-U6 | Should HealthIQ name familial hypercholesterolaemia in consumer output, given it is a genetic diagnosis? | Yes — communication |
| CN-U7 | Whether any dysglycaemia finding should reach same day (CN-U-SD-2) | Yes |
| CN-U8 | Baseline windows (CN-T6) unsourced | No |

**CN-U2 is the most consequential.** A calculated cardiovascular risk percentage delivered to an individual is close to the paradigm case in MHRA's software guidance of a product that analyses patient-specific data to produce an individual risk assessment. It should be raised with the regulatory workstream before any risk-calculation capability is specified further.

---

## 18. Evidence table

| Source | Used for |
|---|---|
| **NICE CG181 — CVD risk assessment and reduction, including lipid modification** | TG >20 urgent referral; TG 10–20 repeat and referral; TG 4.5–9.9 risk underestimation; TC >9.0 / non-HDL >7.5 specialist assessment; TC >7.5 with family history → FH; secondary-cause exclusion; non-HDL preferred to LDL; fasting not required; risk tools not for FH |
| NICE CG71 — Familial hypercholesterolaemia (via CG181) | FH investigation pathway |
| NHS RUH Bath — lipids in primary care | TG >20 pancreatitis risk and urgent lipid-consultant discussion |
| Simon Broome criteria (UK, 1980s) | FH adult criteria `[C]` |
| **BSH/BCSH — cobalamin and folate disorders, *Br J Haematol* 2014** | No gold-standard test; clinical picture primary; functional deficiency with normal serum B12; MCV >115 specificity |
| B12 deficiency neurological literature | Neuropsychiatric manifestations without anaemia; incomplete recovery if delayed |
| GPnotebook / primary care | Pseudohyponatraemia with severe hypertriglyceridaemia |

**Gaps:** vitamin D bands not confirmed to a UK source and deliberately not adopted; HbA1c diagnostic thresholds are convention here rather than a directly cited NICE recommendation; no UK guidance on lipid interpretation without the risk-factor set.

---

## 19. Clinical sign-off

| Field | Value |
|---|---|
| Version | 0.1 |
| Contract authored against | v0.4 + v0.5 summary — re-check required |
| HMR name / registration | ☐ |
| CN-U1 (symptom self-report dependency) | ☐ |
| **CN-U2 (risk calculation — regulatory)** | ☐ raised with regulatory workstream |
| CN-U4 (vitamin D bands) | ☐ ADOPT / ☐ DECLINE MARKER |
| CN-U3, U6, U7 | ☐ |
| Pancreatitis framing for TG >20 approved | ☐ |
| CN-OV-5 confirmed as reframe, not downgrade | ☐ |
| Signature / date | ☐ |

---

## VERDICT: READY_FOR_CENTRAL_RECONCILIATION

The cardiometabolic half is unusually well sourced — NICE CG181 supplies every referral threshold directly — and the nutritional half rests on a current BSH guideline. The domain's two structural peculiarities (risk-as-severity, irreversibility-as-urgency) are both accommodated by contract v0.4/v0.5 without further amendment.

Two items require attention before reconciliation rather than during it: CN-U4, where a vitamin D band has been deliberately withheld rather than imported (leaving a finding that can be created but not graded), and CN-U2, where the risk-calculation question is a regulatory matter that may constrain what this domain is permitted to output at all.
