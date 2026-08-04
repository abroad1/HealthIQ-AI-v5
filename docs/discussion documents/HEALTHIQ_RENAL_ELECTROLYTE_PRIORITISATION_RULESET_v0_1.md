---
document_id: HEALTHIQ-RENAL-ELEC-RULESET-001
title: HealthIQ Renal and Electrolyte Prioritisation Ruleset
version: "0.1"
workstream: C
governing_contract: HEALTHIQ-CLIN-PRIORITY-CONTRACT-001 v0.5
status: DRAFT_FOR_CENTRAL_RECONCILIATION
implementation_status: NOT_AUTHORISED
---

# Renal and Electrolyte Prioritisation Ruleset v0.1

> **Contract availability note.** Authored against contract v0.4 plus the v0.5 principle summary in authoring spec §2. Re-check at reconciliation.

**Evidence labels:** `[E]` · `[C]` · `[J]` · `[U]`.

---

## 1. Scope, exclusions and the domain's defining constraint

**In scope:** creatinine, eGFR, urea, potassium, sodium, calcium (albumin-adjusted), bicarbonate, magnesium, phosphate where available.

**Out of scope:** paediatric; pregnancy (physiological eGFR rise, altered sodium); dialysis and transplant populations (different tolerances) `[E]`; urine studies (ACR, urine electrolytes) — HealthIQ does not receive them; acid–base interpretation requiring blood gases.

### 1.1 The defining constraint

**This is the only domain whose most important finding cannot exist without a baseline.**

NICE NG148 detects AKI by a creatinine rise ≥26 µmol/L within 48 hours, or ≥50% within 7 days, or a fall in urine output `[E]`. HealthIQ has no urine output and often no prior creatinine. Where no valid baseline exists, **AKI is not assessable** — it is not absent.

**RE-P1 `[E]`** — Every renal output on a single-timepoint panel must state that acute change could not be assessed. Contract §12.1 requires this; in this domain it is the primary safety statement, not a footnote.

**RE-P2 `[E]`** — Electrolytes are the mirror image: almost entirely cross-sectional, with urgency carried by absolute concentration. The two halves of this workstream have opposite trend dependencies, which is precisely why authoring them together is necessary — a single trend policy would be wrong for one of them.

### 1.2 Why renal and electrolytes are one workstream

Renal impairment conditions electrolyte interpretation (potassium tolerance, calcium/phosphate handling) and electrolyte disturbance both signals and worsens renal dysfunction. Authoring them separately would produce two incompatible treatments of the potassium/renal interaction. `[C]`

---

## 2. Clinician first-look hierarchy

| Attention | Markers |
|---|---|
| **First look** | Creatinine, eGFR, potassium, sodium, adjusted calcium `[C]` |
| **Conditional** | Urea, bicarbonate, magnesium, phosphate `[C]` |
| **Low yield alone** | Urea — a poor renal finding in isolation and a common source of spurious alarm `[C]` |
| **Modifier, not a finding** | Albumin (for calcium adjustment) `[E]` |

---

## 3. Canonical finding taxonomy

| ID | Finding | Constituents |
|---|---|---|
| RE-F1 | Acute kidney injury (change-defined) | Creatinine + valid baseline |
| RE-F2 | Reduced eGFR — chronic or undetermined chronicity | eGFR ± creatinine |
| RE-F3 | Hyperkalaemia | Potassium |
| RE-F4 | Hypokalaemia | Potassium ± magnesium |
| RE-F5 | Hyponatraemia | Sodium |
| RE-F6 | Hypernatraemia | Sodium |
| RE-F7 | Hypercalcaemia | Adjusted calcium |
| RE-F8 | Hypocalcaemia | Adjusted calcium |
| RE-F9 | Renal impairment with electrolyte disturbance | Combination |
| RE-F10 | Indeterminate renal function (no baseline) | eGFR/creatinine without prior |

**RE-CONS-1 `[C]`** — Creatinine and eGFR consolidate into one renal finding. eGFR is derived from creatinine; presenting both is presenting one thing twice.

**RE-CONS-2 `[E]`** — Where renal impairment and hyperkalaemia coexist, RE-F9 is formed. The potassium retains its own urgency band and is **not** absorbed if it independently meets a same-day criterion (contract §4.8).

**RE-CONS-3 `[J]`** — Urea does not form an independent finding. It is a constituent or contextual.

---

## 4. Urgency rules and time bands

### 4.1 Same day

| ID | Criterion | Basis |
|---|---|---|
| RE-U-SD-1 | Potassium ≥6.5 mmol/L | UKKA severe band; emergency treatment indicated `[E]` |
| RE-U-SD-2 | Potassium 6.0–6.4 mmol/L | UKKA moderate band; ECG and cardiac monitoring recommended at ≥6.0 `[E]`. **`[U]` RE-U1** — CCS/KDIGO use >6.0 as the urgent-treatment threshold where UKKA uses >6.5. HealthIQ must choose and record |
| RE-U-SD-3 | Sodium <125 mmol/L | Profound hyponatraemia; symptoms may develop requiring urgent investigation and treatment `[E]`. Laboratories commonly telephone results below 120 `[E]` |
| RE-U-SD-4 | Adjusted calcium >3.0 mmol/L | Severe; prompt treatment usually indicated in the 3.0–3.5 range, urgent correction required above 3.5 `[E]` |
| RE-U-SD-5 | Creatinine rise meeting NICE AKI criteria (≥26 µmol/L / 48h, or ≥50% / 7d) | NICE NG148 `[E]` |
| RE-U-SD-6 | eGFR <15 (G5) | Kidney failure category `[E]` |
| RE-U-SD-7 | Potassium <2.5 mmol/L | `[C]` — `[U]` RE-U2, threshold not from a cited UK source |
| RE-U-SD-8 | Adjusted calcium markedly low with symptoms | `[U]` — symptoms unavailable to HealthIQ; see §11 |

**All same-day rules are specification-only pending contract §17 — see §13.**

### 4.2 Within days

| ID | Criterion | Basis |
|---|---|---|
| RE-U-D-1 | Potassium 5.5–5.9 mmol/L | UKKA mild band; repeat within 3 days if detected unexpectedly in the community `[E]` |
| RE-U-D-2 | Sodium 125–129 mmol/L | Moderate hyponatraemia `[E]` |
| RE-U-D-3 | Adjusted calcium 2.65–3.0 mmol/L | Mild hypercalcaemia; discuss with endocrinology `[E]` |
| RE-U-D-4 | eGFR 15–29 (G4), new or chronicity undetermined | `[E]` |
| RE-U-D-5 | Potassium 3.0–3.4 mmol/L | `[C]` |
| RE-U-D-6 | New renal impairment with any electrolyte abnormality (RE-F9) | `[C]` |

### 4.3 Within weeks

| ID | Criterion |
|---|---|
| RE-U-W-1 | eGFR 30–59 (G3a/G3b), new or chronicity undetermined `[E]` |
| RE-U-W-2 | Sodium 130–133 mmol/L `[E]` — note UK guidance considers 130–133 mild and not requiring investigation; placed here rather than routine because HealthIQ lacks the clinical context that supports non-investigation `[J]` |
| RE-U-W-3 | Persistent mild hypokalaemia `[C]` |
| RE-U-W-4 | Isolated raised urea with normal creatinine `[C]` |

### 4.4 Routine

| ID | Criterion |
|---|---|
| RE-U-R-1 | Stable eGFR 45–59 (G3a) with a documented prior at the same level `[E]` |
| RE-U-R-2 | eGFR 60–89 (G2) **without** other markers of kidney disease — this is not CKD `[E]` |

**RE-U-NEG-1 `[E]`** — An eGFR above 60 must **not** be classified as CKD unless other markers of kidney disease are present. UK Kidney Association is explicit on this and it is the single most common over-call in this domain.

---

## 5. Severity rules

**Two severity methods, both domain-specific. Multiples of a reference limit are prohibited (contract §18.4).**

### 5.1 Electrolytes — absolute concentration only

| Analyte | Bands | Source |
|---|---|---|
| Potassium (high) | Mild 5.5–5.9 · Moderate 6.0–6.4 · Severe ≥6.5 | UKKA `[E]` |
| Potassium (low) | `[U]` RE-U2 — no cited UK band set |
| Sodium (low) | Mild 130–133 · Moderate 125–129 · Profound <125 | NHS GGC `[E]` |
| Sodium (high) | `[U]` RE-U3 — no band set in this version |
| Adjusted calcium (high) | Mild 2.65–3.00 · Moderate 3.01–3.40 · Severe >3.40 | Network guidance `[E]`; risk of cardiac arrest above 3.5 `[E]` |
| Adjusted calcium (low) | `[U]` RE-U4 |

**RE-S-1 — why ULN multiples are prohibited here.** A potassium of 6.6 mmol/L against a ULN of 5.3 is approximately 1.25× ULN — a multiplier that in the hepatic domain would sit in the mildest band — and is a medical emergency `[E]`. This is the landscape's clearest demonstration that severity methods are not transferable.

### 5.2 Renal — disease-stage bands and change

CKD GFR categories `[E]`: G1 ≥90 · G2 60–89 · G3a 45–59 · G3b 30–44 · G4 15–29 · G5 <15 (kidney failure).

**RE-S-2 `[E]`** — CKD requires eGFR <60 **or** other markers of kidney disease, sustained ≥3 months. A single low eGFR is not CKD.

**RE-S-3 `[E]`** — For AKI, severity is change, not level. A creatinine of 140 µmol/L is unremarkable in stable CKD and an emergency if it was 70 two days ago.

**RE-S-4 `[U]`** — ACR categories (A1 <3, A2 3–30, A3 >30 mg/mmol) materially affect CKD risk stratification `[E]` but ACR is a urine test HealthIQ does not receive. CKD staging is therefore incomplete by construction and must be stated as such.

---

## 6. Indeterminate-severity rules

| ID | Situation | Plausible states | Missing discriminator | Disposition |
|---|---|---|---|---|
| RE-IND-1 | Reduced eGFR, no baseline | AKI (same day) vs stable CKD (weeks/routine) | Prior creatinine | **RE-F10.** Band from the eGFR category alone; AKI reported **not assessable**. May not default to chronic `[E]` |
| RE-IND-2 | Raised potassium, no repeat | Genuine (band applies) vs pseudohyperkalaemia | Repeat sample | Band retained on potential consequence (contract §11); confirmation advice mandatory `[E]` |
| RE-IND-3 | Hyponatraemia, chronicity unknown | Acute (higher risk) vs chronic (lower, but correction risk) | Prior sodium, symptoms | Band from concentration; chronicity stated as unknown. Chronicity is a management modifier, not a severity input `[C]` |
| RE-IND-4 | Raised calcium, albumin absent | Genuine hypercalcaemia vs artefact of protein binding | Albumin | **Not indeterminate — insufficient data.** See §8 `[E]` |
| RE-IND-5 | Low potassium, magnesium absent | Simple vs magnesium-dependent refractory | Magnesium | Band from potassium; magnesium requested `[C]` |

---

## 7. Trend and baseline rules

**Renal: trend-essential. Electrolytes: trend-modifying.** This split is the domain's structural signature.

| ID | Rule | Class |
|---|---|---|
| RE-T1 | AKI is change-defined. Trend evaluation mandatory; without a valid baseline, state not assessable | `[E]` |
| RE-T2 | CKD requires abnormality sustained ≥3 months. A single result cannot establish CKD | `[E]` |
| RE-T3 | Acute potassium change >0.5 mmol/L over 6–12 hours may be more significant than the absolute level | `[E]` |
| RE-T4 | Rate of sodium change governs correction risk; HealthIQ does not advise correction but must not imply a rapid change is benign | `[C]` |
| RE-T5 | Absent baseline is never evidence of stability | `[E]` (contract §18.9) |
| RE-T6 | No trend-based downgrade rule is defined. A stable chronic reduction sits at a lower band **by its own severity criteria**, not by a downgrade | `[J]` |

### Baseline validity `[J]` — all flagged, none from a cited UK source

| Purpose | Window |
|---|---|
| AKI 48-hour criterion | Prior creatinine ≤48h |
| AKI 7-day criterion | Prior creatinine ≤7 days |
| CKD chronicity | Two results ≥3 months apart, both within 24 months |
| Potassium rate of change | ≤12 hours |

**RE-T7 `[J]`** — An eight-month-old creatinine is **not** a 48-hour baseline. Where the available prior falls outside the window, the criterion is not assessable and the older result may be used only for chronicity, clearly labelled.

---

## 8. Modifier and interpretability rules

| Marker | Required modifier | Without it |
|---|---|---|
| **Calcium** | **Albumin** | **Uncorrected calcium is not a clinical quantity.** Produces an **insufficient-data output** for the calcium question, not a low-confidence finding `[E]` |
| Creatinine (for AKI) | Valid prior creatinine | AKI not assessable `[E]` |
| eGFR (for CKD) | Second result ≥3 months apart | CKD not assessable; report reduced eGFR of undetermined chronicity `[E]` |
| eGFR (for staging completeness) | ACR | Staging incomplete; state so `[E]` |
| Potassium (for genuineness) | Repeat sample | Finding stands; confirmation advice mandatory `[E]` |
| Hypokalaemia (for management) | Magnesium | Not blocking; requested `[C]` |

**RE-MOD-1 `[E]`** — Calcium is the landscape's reference case for contract §8's marker–modifier rule. Serum calcium is bound to albumin and measurements should be adjusted for it; presenting uncorrected calcium as a finding is presenting an artefact.

**RE-MOD-2 `[E]`** — eGFR itself is estimated and affected by muscle mass, ethnicity and hydration, none of which HealthIQ reliably holds. This affects **confidence**, not tier.

---

## 9. Analytical caveats and artefact-safe wording

| ID | Caveat | Affects |
|---|---|---|
| RE-A1 `[E]` | Pseudohyperkalaemia from haemolysis, delayed separation, or high platelet/white counts. UK guidance requires its exclusion before acting |
| RE-A2 `[E]` | Severe hypertriglyceridaemia can produce a falsely low sodium |
| RE-A3 `[C]` | Cuff/tourniquet technique affects calcium and potassium |
| RE-A4 `[E]` | eGFR unreliable at extremes of muscle mass and in acute change |
| RE-A5 `[C]` | Delayed sample transport raises potassium |

**RE-A-WORD-1 `[E]` — mandatory artefact-safe wording.** Where an artefact-prone result meets a same-day criterion, the finding stays, the urgency stays, and the language is:

> *"This result needs to be repeated urgently and discussed with a clinician. Results like this can sometimes be affected by how the sample was taken or handled, so it needs confirming — but it should not be ignored while that happens."*

**Prohibited:** asserting the abnormality is genuine; asserting it is probably artefact; demoting it pending repeat. Contract §11 and §18.15.

---

## 10. Combination and override register

| ID | Trigger | Direction | Effect | Basis |
|---|---|---|---|---|
| RE-OV-1 | Potassium ≥6.5 | Promote | Same day | `[E]` |
| RE-OV-2 | Potassium ≥6.0 **with** reduced eGFR | Promote | Same day regardless of RE-U1 resolution | `[E]` |
| RE-OV-3 | AKI criteria met | Promote | Same day | `[E]` |
| RE-OV-4 | Adjusted calcium >3.0 | Promote | Same day | `[E]` |
| RE-OV-5 | Sodium <125 | Promote | Same day | `[E]` |
| RE-OV-6 | Reduced eGFR + any electrolyte abnormality | Promote | Form RE-F9; band ≥ within days | `[C]` |
| RE-OV-7 | Reduced eGFR + thrombocytopenia | **Cross-domain promote** | Haematology same-day criterion fires (new thrombocytopenia with renal impairment) — haematology primary | `[E]` |
| RE-OV-8 | Hypercalcaemia + reduced eGFR | Promote | Both raised; calcium leads on time band | `[C]` |
| RE-OV-9 | Raised calcium **without** albumin | **Reclassify** | Insufficient data for the calcium question — not a finding, not a suppression | `[E]` |

**No downgrade overrides defined.**

---

## 11. Contextual markers and confidence-only factors

**Contextual:**

| Marker | Role | Becomes independent when |
|---|---|---|
| Urea | Contextual to renal findings `[C]` | Very high with clinical context — but HealthIQ lacks that context; **`[U]` RE-U5** |
| Albumin | **Modifier, not a finding, in this domain** | Never — hepatic and inflammatory hold the other roles (contract §9.6) |
| Bicarbonate | Contextual `[C]` | Markedly low with reduced eGFR — `[U]` |
| Phosphate | Contextual in CKD G4/G5 `[E]` | `[U]` |

**Confidence-only (never tier):** absent symptoms; absent medication list (RAAS inhibitors, potassium-sparing diuretics, NSAIDs, supplements); absent hydration status; absent muscle mass and ethnicity for eGFR; absent recent illness.

**RE-CONF-1 `[E]`** — Symptom absence is not symptom negativity. Hyperkalaemia and hypercalcaemia are frequently asymptomatic at levels requiring action; hyponatraemia patients often present with non-specific complaints and normal vital signs.

---

## 12. Concern-tier mapping and lead selection

| Tier | Content |
|---|---|
| Tier 0 | All same-day criteria (§4.1) |
| Tier 1 | Within-days and within-weeks criteria; new or undetermined-chronicity eGFR reduction |
| Tier 2 | Stable documented chronic reduction; G2 without other markers of kidney disease |
| Tier 3 | Urea; bicarbonate; phosphate as CKD context |

**RE-LEAD-1 `[C]`** — Within this domain, an electrolyte disturbance at the same time band as a renal finding leads, because electrolyte harm is more immediate and more directly modifiable.

**RE-LEAD-2 `[E]`** — In RE-F9, the constituent with the higher time band determines the consolidated band.

**RE-LEAD-3** — Cross-domain contests resolve on the common time band only. This domain's absolute-concentration severity may never be compared with another domain's severity (contract §18.24).

**RE-LEAD-4 `[J]`** — Where a same-day electrolyte finding coexists with a same-day finding from another domain, both are presented in the same-day co-equal group with no internal ordering (v0.5 principle, authoring spec §2).

---

## 13. Tier 0 specification-only register

**Every same-day rule in §4.1 is specification-only** pending contract §17 ratification. This domain carries the largest Tier 0 surface in the landscape and is therefore the most constrained by §17.

| Rule | Status |
|---|---|
| RE-U-SD-1 to RE-U-SD-8 | **All specification-only** |

**RE-T0-1 `[J]`** — Where Tier 0 is suppressed, findings are withheld with an explicit statement, never demoted to Tier 1. Given that this domain's Tier 0 content includes life-threatening hyperkalaemia, **suppression of Tier 0 in this domain should be treated as a reason to delay release of the domain, not as a workable operating mode.** `[U]` RE-U6 — is a renal/electrolyte release without Tier 0 capability clinically acceptable at all?

---

## 14. Acceptance scenarios

| # | Panel | Expected |
|---|---|---|
| AS-1 | K⁺ 6.8, no repeat, eGFR 55 | **Tier 0**, same day. RE-F9. Mandatory artefact-safe wording (RE-A-WORD-1). Release blocked pending §17 |
| AS-2 | K⁺ 6.2, eGFR 88 | Tier 0 or high Tier 1 depending on RE-U1 resolution. **Both defensible; must be recorded** |
| AS-3 | Creatinine 145, prior 70 six days ago | **Tier 0** — ≥50% rise within 7 days meets NICE AKI criteria |
| AS-4 | Creatinine 145, no prior | **RE-F10**, Tier 1. AKI **not assessable** — stated explicitly. May not be presented as chronic |
| AS-5 | eGFR 52, prior eGFR 54 four months ago | Tier 2, stable CKD G3a. Note ACR unavailable ⇒ staging incomplete |
| AS-6 | eGFR 72, no other markers | **Not CKD.** No finding, or Tier 3 context. Tests RE-U-NEG-1 |
| AS-7 | Calcium 2.85, albumin absent | **Insufficient-data output for the calcium question.** Not a finding, not suppression. Tests contract §8 marker–modifier rule |
| AS-8 | Calcium 2.85, albumin 40 → adjusted 2.83 | Tier 1, within days, mild hypercalcaemia |
| AS-9 | Sodium 122 | **Tier 0.** Chronicity unknown, stated |
| AS-10 | Sodium 131 | Tier 1 within weeks. Note the deliberate departure from UK guidance's "mild, does not require investigation" — HealthIQ lacks the context that supports non-investigation `[J]` |
| AS-11 | Urea 12, creatinine and eGFR normal | Tier 3 contextual or Tier 1 within weeks. Must not be presented as renal failure |
| AS-12 | K⁺ 6.8 **and** ALT 300 (6.1× ULN) | **Same-day co-equal group.** Potassium and hepatic findings both presented; no ordering between them; no severity comparison. Tests the v0.5 uncapped same-day rule |
| AS-13 | eGFR 40, platelets 45 × 10⁹/L | Haematology primary for the platelet finding (below the 50 boundary, and the renal-impairment combination fires a haematology same-day rule). Two findings, not one |
| AS-14 | Complete normal renal/electrolyte panel, single timepoint | No-concern output **must** state that acute kidney injury could not be assessed without a prior result |

---

## 15. No-concern and insufficient-data outputs

**No-concern — mandatory content:**
1. **Acute kidney injury could not be assessed** without a valid prior creatinine (unless one was available).
2. CKD cannot be established from a single result; it requires abnormality sustained ≥3 months `[E]`.
3. ACR was not available, so kidney-disease risk staging is incomplete `[E]`.
4. eGFR is an estimate affected by muscle mass and other factors.
5. Symptoms warrant review irrespective of the summary.

**RE-NC-1 `[J]`** — "Your kidneys are working normally" is prohibited. A single normal eGFR is compatible with early kidney disease detectable only on ACR.

**Insufficient data:** minimum viable assessment is **creatinine or eGFR**. Calcium without albumin always produces a domain-partial insufficient-data statement (§8).

**RE-ID-1 `[J]`** — Where a Tier 0 or Tier 1 finding exists elsewhere on the panel, the insufficient-data statement is presented alongside it and does not take the lead.

---

## 16. Cross-domain boundaries

| Marker | This domain's role | Other domain primary when | Disposition |
|---|---|---|---|
| Albumin | **Calcium modifier only** | Hepatic — synthetic function. Inflammatory — negative acute-phase reactant | Contract §9.6: three declared roles, no global application. **This domain never treats low albumin as a hepatic finding** |
| Potassium | Primary | — | Owned here |
| Creatinine/eGFR | Primary | Cardiometabolic uses eGFR as CVD-risk context | Attach contextually to cardiometabolic; renal remains primary |
| Calcium | Primary | — | Owned here |
| Platelets | Not owned | Haematology always | RE-OV-7 routes to haematology |
| Sodium | Primary | Cardiometabolic — severe hypertriglyceridaemia can falsely lower sodium (RE-A2) | Confidence caveat, cross-referenced |

---

## 17. Prohibited behaviours (domain additions)

1. Expressing electrolyte severity as multiples of a reference limit.
2. Importing the hepatic Tier 1 floor.
3. Presenting uncorrected calcium as a finding.
4. Classifying eGFR 60–89 as CKD without other markers of kidney disease.
5. Presenting a single low eGFR as CKD.
6. Reporting AKI as absent when no baseline exists.
7. Demoting an artefact-prone urgent result pending repeat.
8. Asserting a potassium result is genuine, or is artefact, without a repeat.
9. Presenting raised urea alone as renal failure.
10. Using a baseline outside the governed window for a change-defined criterion.
11. Treating albumin as a hepatic finding within this domain.

---

## 18. Unresolved questions

| ID | Question | Blocking |
|---|---|---|
| RE-U1 | Potassium urgent threshold: UKKA >6.5 or CCS/KDIGO >6.0, for a consumer product with no clinician in the loop | **Yes** |
| RE-U2 | Hypokalaemia bands — no cited UK source | **Yes** |
| RE-U3 | Hypernatraemia bands — not set | **Yes** |
| RE-U4 | Hypocalcaemia bands — not set | **Yes** |
| RE-U5 | Does urea ever form an independent finding without clinical context? | No |
| RE-U6 | **Is a renal/electrolyte release without Tier 0 capability clinically acceptable?** | **Yes — scope-determining** |
| RE-U7 | Baseline validity windows (§7) are judgement, not sourced | Yes |
| RE-U8 | Pregnancy — currently excluded | Yes |
| RE-U9 | Should HealthIQ present eGFR-based CKD staging at all, given ACR is structurally unavailable? | **Yes — completeness** |
| RE-U10 | Dialysis/transplant populations tolerate higher potassium `[E]`. HealthIQ cannot identify them. Does this warrant a general caveat or an exclusion? | Yes |

**RE-U6 is the domain's defining question.** Four of the eight same-day rules concern potentially life-threatening results. A release that specifies but cannot act on them is a different product from one that can, and the decision is clinical and legal, not technical.

---

## 19. Evidence table

| Source | Used for |
|---|---|
| UK Kidney Association / Renal Association — hyperkalaemia guideline | Potassium bands; pseudohyperkalaemia exclusion; ECG at ≥6.0 |
| NHS RUH Bath — hyperkalaemia guidance for GPs | Acute change >0.5 mmol/L significance; renal tolerance |
| Published comparison of RA (>6.5) and CCS/KDIGO (>6.0) urgent thresholds | RE-U1 |
| NICE NG148 — Acute kidney injury | AKI detection criteria |
| NICE NG203 — Chronic kidney disease | GFR categories G1–G5; ACR categories; CKD definition |
| UK Kidney Association — CKD staging | eGFR >60 not CKD without other markers |
| NHS Greater Glasgow & Clyde — hyponatraemia and hypercalcaemia | Sodium and calcium severity bands |
| NHS Kent & Medway hypercalcaemia network guidance; North Bristol primary-care hypercalcaemia guideline | Calcium bands; cardiac arrest risk >3.5 |
| GPnotebook / primary-care lipid sources | RE-A2 (triglycerides and falsely low sodium) |

**Gaps:** no cited UK band set for hypokalaemia, hypernatraemia or hypocalcaemia; baseline windows unsourced; ACR structurally unavailable.

---

## 20. Clinical sign-off

| Field | Value |
|---|---|
| Version | 0.1 |
| Contract authored against | v0.4 + v0.5 summary — re-check required |
| HMR name / registration | ☐ |
| RE-U1 (potassium threshold) | ☐ UKKA >6.5 / ☐ >6.0 — reason: |
| RE-U2, U3, U4 (missing bands) | ☐ |
| RE-U6 (Tier 0 release acceptability) | ☐ |
| RE-U9 (CKD staging without ACR) | ☐ |
| RE-U10 (dialysis population) | ☐ |
| Artefact-safe wording approved | ☐ |
| All `[J]` items reviewed | ☐ |
| Signature / date | ☐ |

---

## VERDICT: REQUIRES_ADDITIONAL_DOMAIN_RESEARCH

The renal half and the hyperkalaemia, hyponatraemia and hypercalcaemia rules are complete and well sourced. **Three of the six electrolyte finding classes have no cited UK severity bands** — hypokalaemia, hypernatraemia and hypocalcaemia (RE-U2, RE-U3, RE-U4). Publishing this workstream with three empty band sets would leave findings that can be created but not graded, and the temptation at implementation would be to fill them by analogy from potassium, which is exactly the universalisation the contract prohibits.

This verdict is not a structural failure. The taxonomy, urgency architecture, trend split, marker–modifier rules and cross-domain boundaries are complete and reconciliation-ready. What is missing is bounded, named and researchable: three band sets and the RE-U6 scope decision. Those should be closed before central reconciliation rather than carried into it as placeholders.
