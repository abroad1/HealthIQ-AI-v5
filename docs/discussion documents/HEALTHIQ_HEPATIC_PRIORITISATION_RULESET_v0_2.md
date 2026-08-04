---
document_id: HEALTHIQ-HEPATIC-RULESET-001
title: HealthIQ Hepatic Prioritisation Ruleset
version: "0.2"
supersedes: "0.1"
workstream: B
governing_contract: HEALTHIQ-CLIN-PRIORITY-CONTRACT-001 v0.5
status: DRAFT_FOR_CENTRAL_RECONCILIATION
implementation_status: NOT_AUTHORISED
scope: Adults ≥18. Paediatric, neonatal and pregnancy hepatic interpretation excluded.
---

# Hepatic Prioritisation Ruleset v0.2

> **Contract availability note.** Authored against contract v0.4 plus the v0.5 principle summary in authoring spec §2. Must be re-checked against actual v0.5 at reconciliation.

**Evidence labels:** `[E]` · `[C]` · `[J]` · `[U]`.

---

## 0. Changes from v0.1 (required by authoring spec §3.2)

| Change | Status |
|---|---|
| Hepatic Tier 1 floor labelled **domain-specific** | Done — §12.1. Now carries an explicit non-export clause |
| Temporary haematology thresholds removed | Done — the 10%-of-ULN MCV margin is deleted and replaced by a reference to the haematology ruleset's governed bands (§11.1) |
| Haematology dependencies preserved explicitly | Done — §16, three named dependencies |
| Specification-only Tier 0 rules distinguished | Done — §13 |
| R-value, ULN multiples and hepatic investigation rules confined to this domain | Done — §17 |
| Urgency mapped to common time bands | Done — §4 |
| Indeterminate-severity rules added | Done — §6 (new in v0.2) |
| Marker–modifier pairs enumerated | Done — §8 |
| Cross-domain consolidation with haematology governed | Done — §16 |

---

## 1. Scope and exclusions

**In scope:** ALT, AST, ALP, GGT, bilirubin, albumin, INR where available, platelets in hepatic context.

**Out of scope:** paediatric (different aetiology panel and referral threshold) `[E]`; pregnancy (ALP raised, albumin reduced physiologically) `[E]`; aetiological diagnosis; medication cessation advice; drug library.

---

## 2. The domain's governing clinical tension

Must be read before any rule below.

BSG Recommendation 3: the extent of liver blood test abnormality is not necessarily a guide to clinical significance, which is determined by the specific analyte and the clinical context `[E]`. BSG Recommendation 4 (grade B): patients with abnormal liver blood tests should be considered for a liver aetiology screen irrespective of level and duration, where abnormal means outside the laboratory reference range `[E]`.

Two rules follow:

**HEP-P1 `[E]`** — Magnitude sets urgency and prominence, never eligibility.

**HEP-P2 `[E]`, domain-bound** — Any confirmed out-of-range core hepatic analyte floors at **Tier 1** on a first panel.

**HEP-P2 IS NOT EXPORTABLE.** It derives from a hepatology-specific grade B recommendation. Applied to haematology it would place isolated mild macrocytosis at Tier 1, contradicting UK guidance that such patients should be reassured `[E]`. Applied to inflammatory markers it would place isolated mild CRP elevation at Tier 1. Contract §18.23 prohibits its export; the haematology ruleset §12 records the counterexample.

**The cost of HEP-P2 is real and must be accepted knowingly.** BSG reports around 30% of liver test requests at one UK trust contained at least one out-of-range result, while the BALLETS cohort found fewer than 5% of adults with abnormal liver blood tests had a specific liver disease and 1.3% needed immediate treatment `[E]`. High Tier 1 volume, low positive yield. **`[U]` HEP-U1 remains the primary adjudication** — adopt BSG literally, or adopt a magnitude-gated variant recorded as a documented departure from a grade B recommendation.

---

## 3. Clinician first-look hierarchy

| Attention | Markers | Basis |
|---|---|---|
| First look | Bilirubin, albumin, ALT, ALP, GGT | BSG Rec 1 defines exactly this initial panel, with FBC if not done within 12 months `[E]` |
| Conditional | AST (reflex on abnormal ALT), INR, platelets | `[E]` |
| Low yield alone | GGT diagnostically — though prognostically strong `[E]` |

---

## 4. Canonical finding taxonomy and urgency time bands

### 4.1 Taxonomy

| ID | Finding |
|---|---|
| HEP-F1 | Hepatocellular injury pattern |
| HEP-F2 | Cholestatic injury pattern |
| HEP-F3 | Mixed injury pattern |
| HEP-F4 | Hepatic synthetic dysfunction |
| HEP-F5 | Suspected advanced fibrosis |
| HEP-F6 | Isolated hyperbilirubinaemia (Gilbert's pattern) |
| HEP-F7 | Isolated raised ALP (origin undetermined or non-hepatic) |
| HEP-F8 | Isolated raised GGT |
| HEP-F9 | Non-classifiable hepatic abnormality |
| HEP-F10 | Possible iron overload in hepatic context |

**HEP-CONS-1 `[J]`** — ALT, AST, ALP, GGT and bilirubin forming a recognised pattern produce **one** finding. ALT 250 with ALP 46 and normal bilirubin is one concern, not three.

**HEP-CONS-2 `[E]`** — Aetiological frames (alcohol, metabolic, viral, autoimmune, drug-induced, iron) consolidate. They fail contract §9.3's separation test because BSG Rec 5 specifies **one** standard aetiology screen common to all of them.

### 4.2 Urgency time bands

| Band | Criteria | Basis |
|---|---|---|
| **Same day** | ALT/AST ≥10× ULN `[E]`; ALT/AST >1000 U/L absolute `[E]`; Hy's law pattern (ALT/AST ≥3× ULN + bilirubin ≥2× ULN + ALP <2× ULN) `[C]`; abnormal hepatic analyte + albumin <LRL `[E]`; abnormal hepatic analyte + INR >1.5 without anticoagulation `[E]`; new conjugated hyperbilirubinaemia at jaundice range with abnormal enzymes `[E]` |
| **Within days** | ALT/AST ≥5× to <10× ULN `[J]` |
| **Within weeks** | Any other confirmed out-of-range core analyte (HEP-P2) `[E]`; suspected fibrosis (FIB-4 above threshold, AST:ALT >1, low platelets with abnormal analytes) `[E]`; isolated GGT >100 U/L `[E]`; isolated raised bilirubin **with** anaemia `[E]` |
| **Routine** | Isolated GGT ≤100 U/L `[J]`; established Gilbert's pattern `[E]` |

**`[U]` HEP-U2** — the bilirubin value at which the jaundice-range rule fires. UK guidance frames it clinically ("unexplained clinical jaundice → immediate referral") and HealthIQ has no clinical observation. Interim: fire on total bilirubin and state that the conjugated fraction was not measured.

---

## 5. Severity rules

**Severity method: multiples of ULN for transaminases and ALP.** Domain-bound (contract §18.4, §18.24).

### 5.1 ALT / AST

| Band | Range | Boundary source |
|---|---|---|
| Mild | >ULN to <3× | BSG Rec 4 lower bound `[E]`; 3× from UK statin-monitoring practice `[E]` |
| Moderate | ≥3× to <5× | `[E]` |
| Marked | ≥5× to <10× | EASL designates hepatocellular injury at ≥5× ALT `[E]`, international |
| Severe | ≥10× or >1000 U/L | NHS Devon 10× rule; NHS SPS >1000 differential `[E]` |

AST modifiers: less liver-specific — abundant in skeletal, cardiac and smooth muscle, so may be raised in myocardial infarction or myositis `[E]`; but more sensitive in alcohol-related disease and some autoimmune hepatitis `[E]`. Non-hepatic source reduces **confidence**, never severity.

### 5.2 ALP

| Band | Range |
|---|---|
| Mild | >ULN to <2× |
| Significant | ≥2× ULN `[C]` |

ALP is not liver-specific — abundant in bone, present in intestine, kidney and white cells; physiologically higher in childhood and pregnancy `[E]`. Where GGT is normal alongside raised ALP, hepatic origin is not supported → reclassify to HEP-F7 `[E]`. Where GGT is absent, origin is **undetermined** and must be stated, not assumed hepatic `[J]`.

### 5.3 GGT

Diagnostically weak: commonly raised by obesity, alcohol or drug induction, with low specificity `[E]`. Prognostically strong: one of the best predictors of liver mortality, with greatest risk at the largest elevations `[E]`. Specific threshold: GGT >100 U/L prompts fibrosis assessment as for the higher-risk alcohol group `[E]`.

**HEP-GGT-1 `[J]`** — Isolated GGT ≤100 U/L is placed at **routine**, a deliberate and flagged exception to HEP-P2. `[U]` HEP-U3 — is this defensible given HEP-GGT prognostic strength?

---

## 6. Indeterminate-severity rules (new in v0.2)

| ID | Situation | Plausible states | Missing discriminator | Disposition |
|---|---|---|---|---|
| HEP-IND-1 | Raised ALT, ALP absent | Hepatocellular vs mixed vs cholestatic | ALP | HEP-F9. R **not computed**. Band from ALT severity alone. Must not be described as hepatocellular `[J]` |
| HEP-IND-2 | Abnormal enzymes, albumin and INR both absent | Injury only (weeks) vs synthetic failure (same day) | Albumin, INR | Band from enzyme severity; **synthetic failure reported as not assessable**, not absent. Explicitly request both `[J]` |
| HEP-IND-3 | Raised ALP, GGT absent | Hepatic (weeks) vs bony/other (different domain) | GGT | HEP-F7 with origin undetermined. Do not route to a non-hepatic domain on assumption `[E]` |
| HEP-IND-4 | Raised bilirubin, split unavailable | Gilbert's (routine) vs hepatic/obstructive (weeks or same day with enzymes) | Conjugated fraction | Floor at the presence of other abnormalities: isolated → routine with the caveat; with abnormal enzymes → weeks or above `[E]` |
| HEP-IND-5 | Abnormal enzymes, no prior result | Acute vs chronic | Baseline | Treat as new. Contract §18.9 `[E]` |

---

## 7. R-value rules

R = (ALT ÷ ALT ULN) ÷ (ALP ÷ ALP ULN). Hepatocellular R ≥5, mixed 2–5, cholestatic ≤2 `[C]`.

**HEP-R-1 — evidence status.** This is a DILI causality convention from EASL and AASLD. BSG classifies pattern qualitatively and specifies **no numeric R**. `[E]` for the qualitative classification; `[C]` for the cutoffs.

**HEP-R-2 `[J]`** — R classifies pattern and selects explanation content. It may **not** set urgency or severity. R = 12.9 says the injury is hepatocellular; magnitude is carried entirely by the ALT band.

**HEP-R-3 `[J]`** — R must never be surfaced to a consumer as a headline number.

**HEP-R-4 `[J]`** — Not computed unless both ALT and ALP are present with reference limits, and at least one is abnormal. AST may substitute for ALT with reduced confidence `[C]`.

**HEP-R-5 — non-export.** R is meaningless outside this domain and must not be generalised as a pattern-classification method (contract §18.23 spirit; authoring spec §3.2).

---

## 8. Modifier and interpretability rules

| Marker | Required modifier | Without it |
|---|---|---|
| ALT | ALP (for pattern) | Pattern not assessable → HEP-F9 |
| ALP | GGT (for origin) | Origin not assessable — not assumed hepatic `[E]` |
| Bilirubin | Conjugated fraction (for Gilbert's assertion) | Gilbert's may not be asserted `[E]` |
| Any enzyme | Albumin + INR (for synthetic-failure criteria) | Criteria reported **not assessable**, not not-met `[J]` |
| FIB-4 | Age, AST, ALT, platelets — all four | Not computed; fibrosis risk reported not assessed `[E]` |

**HEP-MOD-1 `[E]`** — BSG Rec 2 states results should only be interpreted after review of previous results, past medical history and current condition. HealthIQ typically holds none of these. This is a **standing domain limitation stated in every hepatic output**, not a per-case caveat. It is the strongest argument in the landscape for the contract §16.2 discipline.

---

## 9. Trend and baseline rules

**Classification: trend-important.**

| ID | Rule |
|---|---|
| HEP-T1 `[E]` | Statin monitoring is change-defined: stop only if enzymes double within 3 months of starting, including with abnormal baseline. Requires a pre-statin result and start date; without them, report not assessable |
| HEP-T2 `[C]` | Where baseline ALT is ≥1.5× ULN, DILI signal thresholds are expressed relative to baseline |
| HEP-T3 `[E]` | FIB-4 recalculated every 3 years; refer if it rises above the age-related cut-off |
| HEP-T4 `[E]` | **Persistence does not reduce concern.** BALLETS: 84% still abnormal at 1 month, 75% at 2 years |
| HEP-T5 `[E]` | **Normalisation does not exclude disease.** Explicitly true for HCV and steatotic liver disease |
| HEP-T6 `[J]` | Consequent to T4 and T5: **no trend-based downgrade rule exists in this domain** |

Baseline validity `[J]`: 3 months for statin doubling; most recent pre-exposure for DILI; 24 months for chronicity; 3 years for FIB-4.

---

## 10. Analytical and contextual caveats

**Analytical `[E]`** — haemolysis raises AST; muscle injury, myositis and recent intense exercise raise AST and ALT (creatine kinase discriminates); ALP physiologically raised in pregnancy; drug induction raises GGT; intercurrent illness raises enzymes generally.

**Contextual `[E]`** — statins: DILI is very rare and studies show statins are safe in people with pre-existing abnormal enzymes; **HealthIQ never advises medication cessation.** Alcohol: NICE NG50 thresholds 50 units/week men, 35 women; AUDIT >19 indicates dependency. Metabolic risk factors route to the FIB-4 pathway. Hepatotoxic drugs (BSG list includes carbamazepine, methyldopa, minocycline, macrolides, nitrofurantoin, statins, sulfonamides, terbinafine, chlorpromazine, methotrexate) raise DILI as an alternative interpretation — **caveat only, not a drug library**.

---

## 11. Contextual-marker rules

### 11.1 MCV — **temporary threshold removed**

v0.1 used a 10%-of-ULN margin explicitly labelled non-clinical. **That margin is deleted.**

**HEP-CTX-1 `[E]`** — MCV may be attached contextually to a hepatic finding only within the **mild macrocytosis band as defined by the haematology ruleset §5.4**, and only where no other FBC abnormality is present. Above that band, or with any other FBC abnormality, contract §4.8 prohibits contextual assignment and haematology is primary.

### 11.2 Other contextual markers

| Marker | Rule |
|---|---|
| Transferrin (low) | Contextual `[C]` — non-specific: negative acute-phase protein, reduced hepatic synthesis, or undernutrition |
| Transferrin **saturation** | **Not contextual** — required constituent of the BSG aetiology screen and trigger for HEP-F10 `[E]` |
| Ferritin, TSAT ≤45% | Contextual `[E]` — dysmetabolic pattern common in alcohol excess and steatotic liver disease; does not reflect haemochromatosis |
| Ferritin, TSAT >45% | **Not contextual** — distinct Tier 1 finding HEP-F10 `[E]` |
| Platelets | Contextual as a fibrosis indicator **only** at ≥50 × 10⁹/L per haematology §10; below that, haematology is primary `[E]` |

---

## 12. Concern-tier mapping and lead selection

### 12.1 Tier mapping

| Tier | Content |
|---|---|
| Tier 0 | All same-day criteria (§4.2) |
| Tier 1 | Within-days and within-weeks criteria; **HEP-P2 floor applies here — domain-bound** |
| Tier 2 | Isolated GGT ≤100; established Gilbert's pattern |
| Tier 3 | Contextual attachments (§11) |

**Non-export clause.** The HEP-P2 Tier 1 floor is a property of this domain only. No other workstream may adopt it; the consolidated ruleset records it in the prohibited-universalisation register.

### 12.2 Lead selection

- **HEP-LEAD-1 `[J]`** — HEP-F4 (synthetic dysfunction) outranks HEP-F1/F2/F3 at equal tier. Function outranks injury `[E]` — bilirubin, albumin and INR convey liver *function*; enzymes convey ongoing *injury*.
- **HEP-LEAD-2 `[J]`** — Injury patterns outrank HEP-F5 (fibrosis) only at marked severity or above. Below that, fibrosis stage predicts outcome and enzyme level does not (BSG Rec 3).
- **HEP-LEAD-3** — Contextual items never lead.
- **HEP-LEAD-4** — Cross-domain contests are adjudicated on the common time band (contract §7.2). Hepatic severity is never compared with another domain's severity.

---

## 13. Tier 0 specification-only register

| Rule | Status |
|---|---|
| ALT/AST ≥10× ULN | **Specification-only** |
| ALT/AST >1000 U/L | **Specification-only** |
| Hy's law pattern | **Specification-only** |
| Abnormal analyte + low albumin | **Specification-only** |
| Abnormal analyte + INR >1.5 | **Specification-only** |
| Jaundice-range bilirubin + abnormal enzymes | **Specification-only and threshold-blocked** (HEP-U2) |

Tier 1 and below release-eligible. Where Tier 0 is suppressed, findings are withheld with an explicit statement — **not demoted** (contract §18.19).

---

## 14. Acceptance scenarios

Contract §19 regression fixture retained, plus domain scenarios.

| # | Panel | Expected |
|---|---|---|
| **AS-1** (contract §19 fixture) | ALT 250 (ULN 49, 5.1×), ALP 46 (ULN 116), R ≈12.9, bilirubin & GGT normal, AST absent, MCV 99.5 (ULN 96), transferrin mildly low | One consolidated hepatocellular finding, **Tier 1**, within days. Confidence reduced (AST absent); significance **not** reduced. MCV contextual — within haematology's mild band with no other FBC abnormality. Transferrin contextual. Albumin/INR **not assessable**, stated. No urgent diagnostic claim |
| AS-2 | Same + albumin 28 g/L | **Tier 0**, same day. Lead is HEP-F4 per HEP-LEAD-1. Albumin non-hepatic-cause caveat mandatory. Release blocked pending §17 |
| AS-3 | ALT 550 (11.2×), all else normal | **Tier 0** by magnitude alone. Tests the 10× boundary |
| AS-4 | ALT 60 (1.2×), isolated | **Tier 1** under HEP-P2 — or Tier 2 under a modified reading. **Both defensible; HEP-U1 decides.** Under either, the finding is shown |
| AS-5 | ALP 240 (2.1×), GGT normal, ALT normal | Reclassify to HEP-F7, non-hepatic origin likely. Handed on with its own floor intact — **reclassification, not suppression** |
| AS-6 | Bilirubin 38 isolated, no anaemia | Tier 2, Gilbert's pattern, reassurance available. Split-bilirubin caveat if unmeasured |
| AS-7 | Bilirubin 38 isolated, Hb low | **Tier 1** — same bilirubin, different finding. Haemolysis must be considered |
| AS-8 | Ferritin 1400, TSAT 22%, ALT 90 | Hepatic Tier 1; ferritin **contextual**. Magnitude does not promote context |
| AS-9 | Ferritin 420, TSAT 58%, ALT 90 | **Two** Tier 1 findings — hepatic pattern and HEP-F10. Co-lead eligible if action pathways differ |
| AS-10 | ALT 30, AST 45, platelets 130, age 58 | **HEP-F5 Tier 1** via AST:ALT >1 and FIB-4. All values in or near range — tests contract §3.1. If nothing is produced, the in-range rule is not implemented |
| AS-11 | ALT 250, ALP absent | **HEP-F9**, Tier 1 by severity. R not computed. Must not be called hepatocellular |
| AS-12 | Complete normal hepatic panel | No-concern output **must** state that normal enzymes do not exclude advanced fibrosis or cirrhosis |
| **AS-13** (new) | ALT 250, MCV 118 fL | MCV **may not** be contextual — above haematology's mild band. Two findings. Tests contract §4.8 and the removal of the v0.1 placeholder |
| **AS-14** (new) | ALT 250, platelets 35 × 10⁹/L | Platelets **may not** be absorbed into a hepatic fibrosis finding — below the 50 boundary, haematology is primary and the count independently meets a same-day criterion. Two findings, haematology leads on time band |

**Evidence discipline.** Bands were derived from cited sources before the fixture was consulted. Had ALT been 500 against the same ULN, AS-1 would have resolved to Tier 0 and the fixture would not have governed. Thresholds must not be adjusted to force any expected answer.

---

## 15. No-concern and insufficient-data outputs

**No-concern — mandatory hepatic content:**
1. **Normal liver enzymes do not exclude liver disease.** Both AST and ALT can be normal in cirrhosis, and many people with significant fibrosis have normal enzymes and normal synthetic function `[E]`. This sentence is mandatory in every hepatic no-concern output.
2. Which analytes were and were not measured.
3. Whether fibrosis risk could be assessed (FIB-4 computability).
4. Whether synthetic function was assessed.
5. Symptoms warrant review irrespective of the summary.

**HEP-NC-1 `[J]`** — "Your liver is healthy" or equivalent is prohibited. HealthIQ measures enzymes, not liver health.

**Insufficient data:** minimum viable hepatic assessment is **ALT (or AST) + ALP**. Without both, issue an insufficient-data output for the domain. Where the minimum is met but synthetic markers are absent, issue a finding with an explicit synthetic-function-not-assessed statement — a different thing from "we could not look".

---

## 16. Cross-domain boundaries

| Marker | Hepatic role | Other domain primary when | Disposition |
|---|---|---|---|
| Platelets | Fibrosis indicator | Count <50 × 10⁹/L or any haematology same-day criterion | Consolidate above the boundary; **haematology primary below it** `[E]` |
| MCV | Contextual explanation | Above haematology's mild band, or any other FBC abnormality | Attach only within the band |
| Albumin | Synthetic-function marker | Renal/electrolyte domain uses it as the **calcium modifier**; inflammatory uses it as a **negative acute-phase reactant** | Contract §9.6 — three roles, three declarations, no global application |
| Ferritin / TSAT | Aetiology-screen constituent | Iron domain primary for the overload finding itself | Consolidate as HEP-F10 or hand to iron |
| Bilirubin | Hepatic function | Haematology where haemolysis is the driver | Combination rule HEP-OV-12 routes to haematology/iron |

**Named haematology dependencies (preserved, not closed):**
1. Platelet band boundary for fibrosis-context absorption (§11.2) — supplied by haematology §5.1.
2. MCV mild-band boundary for contextual attachment (§11.1) — supplied by haematology §5.4.
3. FBC-abnormality definition for the isolated-versus-not test — supplied by haematology §3.

---

## 17. Prohibited behaviours (domain additions)

1. Exporting HEP-P2 (the Tier 1 floor) to any other domain.
2. Exporting multiples-of-ULN as a severity method.
3. Exporting the R-value as a general pattern classifier.
4. Exporting "any abnormality warrants an aetiology screen" framing.
5. Surfacing R as a consumer-facing number.
6. Describing a pattern as hepatocellular without ALP.
7. Asserting Gilbert's without the conjugated fraction.
8. Reducing severity or tier because AST, GGT, albumin or INR are absent.
9. Advising medication cessation.
10. Using the deleted 10%-of-ULN MCV margin, or any other locally invented haematology threshold.
11. Reporting an unevaluable synthetic-failure criterion as not met.

---

## 18. Unresolved questions

| ID | Question | Blocking |
|---|---|---|
| HEP-U1 | Adopt BSG Rec 4 literally (Tier 1 floor, high volume) or a magnitude-gated variant recorded as documented departure | **Yes — primary** |
| HEP-U2 | Numeric bilirubin threshold for the jaundice rule; behaviour without the conjugated fraction | **Yes — Tier 0 incomplete** |
| HEP-U3 | Is isolated GGT ≤100 at routine defensible given its mortality association? | No |
| HEP-U4 | Pregnancy: is suppression safe, or is a pregnancy-adjusted set needed? | **Yes** |
| HEP-U5 | Should HealthIQ compute and surface FIB-4 at all? Most device-like output in the domain — regulatory interaction, contract §22 | **Yes** |
| HEP-U6 | Should HealthIQ apply lower internal ALT thresholds than the laboratory, given BSG's note that ALT ULN may be too high? Would generate findings on results reported as normal | No, but material |
| HEP-U7 | Which hepatic rules are unsafe without alcohol/medication/metabolic context, as opposed to merely lower-confidence? | **Yes** |

---

## 19. Evidence table

| Source | Used for |
|---|---|
| Newsome PN et al., BSG. *Gut* 2018;67(1):6–19 | Recs 1–5, 7, 9, 10; pattern recognition; analyte roles; aetiology screen; Gilbert's; ALP origin; GGT; AST:ALT; FIB-4; BALLETS persistence; pregnancy; ferritin/TSAT 45% |
| NHS Devon (North & East) abnormal LFT guidance | 10× ULN same-day rule; statin doubling; 3-yearly FIB-4 |
| NHS Specialist Pharmacy Service | >1000 U/L; low albumin referral; INR |
| NHS Highland referral pathway | Liver screen composition |
| NICE NG50 / NG49 | Alcohol thresholds; fibrosis context |
| EASL DILI CPG 2019; AASLD DILI guidance | R-value; 5× ULN; Hy's law; INR >1.5 — international, where UK guidance is silent |

**Gaps:** no UK guideline bands transaminases numerically (§5.1 is a sourced synthesis, labelled `[J]`); no UK guideline endorses numeric R; no guidance addresses interpretation without clinical context.

---

## 20. Clinical sign-off

| Field | Value |
|---|---|
| Version | 0.2 |
| Contract authored against | v0.4 + v0.5 summary — re-check required |
| HMR name / registration | ☐ |
| HEP-U1 | ☐ ADOPT BSG LITERAL / ☐ MODIFIED — reason: |
| HEP-U2, U4, U5, U7 | ☐ |
| v0.1 placeholder removal confirmed | ☐ |
| Non-export clause on HEP-P2 confirmed | ☐ |
| Haematology dependencies accepted as open | ☐ |
| Tier 0 specification-only register confirmed | ☐ |
| Signature / date | ☐ |

---

## VERDICT: READY_FOR_CENTRAL_RECONCILIATION

All five v0.1 remediation items are complete. HEP-U1 remains the domain's primary open decision and is a clinical policy question rather than a research gap — both answers are defensible and the choice must be recorded. The three haematology dependencies are now explicitly named and bounded rather than filled with placeholders.
