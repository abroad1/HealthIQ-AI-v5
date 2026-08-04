---
document_id: HEALTHIQ-IRON-INFLAM-RULESET-001
title: HealthIQ Iron and Inflammatory Prioritisation Ruleset
version: "0.1"
workstream: D
governing_contract: HEALTHIQ-CLIN-PRIORITY-CONTRACT-001 v0.5
status: DRAFT_FOR_CENTRAL_RECONCILIATION
implementation_status: NOT_AUTHORISED
---

# Iron and Inflammatory Prioritisation Ruleset v0.1

> **Contract availability note.** Authored against contract v0.4 plus the v0.5 principle summary in authoring spec §2. Re-check at reconciliation.

**Evidence labels:** `[E]` · `[C]` · `[J]` · `[U]`.

---

## 1. Scope and the domain's defining characteristic

**In scope:** ferritin, transferrin saturation, serum iron, transferrin/TIBC, CRP, ESR where available, with declared dependencies on haemoglobin and MCV.

**Out of scope:** paediatric; pregnancy; HFE genotyping and haemochromatosis diagnosis; transfusion-dependent populations; autoimmune serology; ESR-based rheumatological diagnosis.

### 1.1 Defining characteristic

**This domain has almost no intrinsic urgency and almost all of its meaning in combination.** No ferritin, TSAT or CRP value on its own generates a same-day action in UK primary care. What this domain supplies is *interpretation of other domains' findings*: why the anaemia, whether the raised ferritin means overload, whether an in-range value is falsely reassuring.

**IRIN-P1 `[J]`** — Consequently this domain must be unusually disciplined about **not** creating concerns. A ruleset that turns every abnormal ferritin and CRP into a finding will bury the domains that carry real urgency.

**IRIN-P2 `[E]`** — And it must be equally disciplined about the opposite failure: an in-range ferritin under inflammation may conceal iron deficiency, and this domain owns that rule.

---

## 2. Clinician first-look hierarchy

| Attention | Markers |
|---|---|
| **First look** | Ferritin, transferrin saturation, plus haemoglobin and MCV from haematology `[E]` |
| **Conditional** | CRP (interpretation of ferritin), serum iron, transferrin/TIBC |
| **Low yield alone** | Serum iron — diurnal variation and meal effects make it near-uninterpretable in isolation `[C]` |
| **Derived, not requested** | TSAT where iron and TIBC are present (§8) |

**IRIN-FL-1 `[E]`** — Ferritin and TSAT are inspected **together**, not sequentially. The BSH raised-ferritin guideline makes TSAT the key discriminating test; a ferritin read without it answers a different question from the one being asked.

---

## 3. Canonical finding taxonomy

| ID | Finding | Constituents |
|---|---|---|
| IRIN-F1 | Iron deficiency (without anaemia) | Low ferritin ± TSAT |
| IRIN-F2 | Iron deficiency anaemia | Low ferritin + low Hb (± low MCV) — **consolidated with haematology** |
| IRIN-F3 | Possible iron overload | Raised ferritin + TSAT >45% |
| IRIN-F4 | Inflammatory or dysmetabolic hyperferritinaemia | Raised ferritin + TSAT ≤45% |
| IRIN-F5 | Functional iron deficiency / masked deficiency | In-range ferritin + raised CRP + anaemia or low TSAT |
| IRIN-F6 | Acute inflammatory response | Raised CRP |
| IRIN-F7 | Persistent unexplained inflammation | Raised CRP on repeated occasions |
| IRIN-F8 | Indeterminate ferritin | Raised ferritin, TSAT unavailable and underivable |

**IRIN-CONS-1 `[C]`** — Ferritin, TSAT, serum iron and transferrin never form separate concerns. They form **one** iron-status finding.

**IRIN-CONS-2 `[E]`** — Where anaemia is present, IRIN-F2 is one finding jointly owned with haematology. **Anaemia must never appear twice** on a HealthIQ output.

**IRIN-CONS-3 `[J]`** — CRP does not form a finding when it is explaining another finding. See §11.

---

## 4. Urgency rules and time bands

### 4.1 Same day

**None.** No iron or inflammatory marker value generates a same-day action from biochemistry alone in this scope. `[J]`, on the basis that no UK guidance consulted specifies one.

**IRIN-U-SD-NEG `[J]`** — This is a positive finding, not an omission. It should be recorded in the consolidated ruleset: a domain may legitimately have an empty Tier 0.

**`[U]` IRIN-U1** — Very high ferritin (conventionally >10,000 µg/L) in the presence of systemic features raises hyperinflammatory syndromes. HealthIQ has no clinical features and this is a secondary-care entity. Should any ferritin threshold generate urgency? Currently: no. Flagged for adjudication.

### 4.2 Within days

| ID | Criterion | Basis |
|---|---|---|
| IRIN-U-D-1 | Iron deficiency anaemia with Hb in haematology's within-days band | Urgency derives from the **anaemia**, not the iron marker `[C]` |
| IRIN-U-D-2 | Raised CRP with a cytopenia | Combination; haematology leads `[C]` |

### 4.3 Within weeks

| ID | Criterion | Basis |
|---|---|---|
| IRIN-U-W-1 | Low ferritin (iron deficiency), with or without anaemia | Specific, actionable, requires cause-finding `[C]` |
| IRIN-U-W-2 | Raised ferritin **with** TSAT >45% (IRIN-F3) | BSG: haemochromatosis defined as raised ferritin with TSAT >45%, refer to specialist clinic `[E]` |
| IRIN-U-W-3 | Functional/masked deficiency (IRIN-F5) | `[E]` |
| IRIN-U-W-4 | Marked CRP elevation without explanation | `[C]` — `[U]` IRIN-U2, threshold not set |
| IRIN-U-W-5 | Persistent unexplained inflammation (IRIN-F7) | `[C]` |

### 4.4 Routine

| ID | Criterion | Basis |
|---|---|---|
| IRIN-U-R-1 | Raised ferritin with TSAT ≤45% and no other abnormality | Dysmetabolic pattern is common in alcohol excess and steatotic liver disease and does not reflect haemochromatosis `[E]` |
| IRIN-U-R-2 | Isolated mild CRP elevation | `[C]` |
| IRIN-U-R-3 | Isolated low serum iron with normal ferritin | Non-specific `[C]` |

**IRIN-U-NEG-1 `[E]`** — **Iron overload can generally be excluded when TSAT <45%.** A ferritin of 1400 with TSAT 22% is a routine finding with an inflammatory or dysmetabolic explanation, not an overload concern.

**IRIN-U-NEG-2 `[C]`** — Isolated mild CRP elevation does not warrant Tier 1. This is the domain's contribution to the anti-universalisation evidence: applying the hepatic Tier 1 floor here would place every mildly raised CRP in the discuss-or-investigate tier.

---

## 5. Severity rules

**Severity methods: direction-asymmetric for ferritin; persistence-weighted for CRP. Neither uses multiples of a reference limit.**

### 5.1 Ferritin — direction asymmetry `[E]`

| Direction | Interpretation | Severity method |
|---|---|---|
| **Low** | Specific and highly actionable — low ferritin invariably indicates reduced iron stores `[E]` | Magnitude is weakly informative; presence is what matters |
| **High** | Broad differential — iron overload, inflammation, liver or renal disease, malignancy, metabolic syndrome `[E]` | **Magnitude is a poor severity proxy; TSAT is the severity determinant** |

**IRIN-S-1 `[E]` — the domain's signature rule.** Ferritin 420 µg/L with TSAT 58% outranks ferritin 1400 µg/L with TSAT 22%. The lower-magnitude finding is the more concerning one. This is the clearest demonstration in the landscape that magnitude is not severity.

### 5.2 TSAT `[E]`

| Band | Value | Meaning |
|---|---|---|
| Overload plausible | >45% | Threshold for further investigation; genotyping thresholds are sex-specific — females TSAT >45% with ferritin >200 µg/L, males TSAT >50% with ferritin >300 µg/L `[E]` |
| Overload effectively excluded | <45% | `[E]` |
| Low | `[U]` IRIN-U3 — deficiency threshold not set in this version |

### 5.3 CRP `[C]`, weak

**IRIN-S-2 `[C]`** — CRP magnitude bands are weakly informative without clinical context. **Persistence is more informative than height.** A CRP of 40 in someone with a cold is unremarkable; a CRP of 20 on three occasions over six months is not.

**IRIN-S-3 `[J]`** — No numeric CRP severity bands are set in this version. `[U]` IRIN-U2.

### 5.4 Ancestry and reference-range caveats

**IRIN-S-4 `[E]`** — Ferritin reference expectations differ by ancestry; individuals of East Asian descent have been reported to have ferritin values 1.5–2× the reported upper limit. HFE testing is not recommended in people of non-European ancestry because the prevalence is very rare `[E]`. HealthIQ does not reliably hold ancestry. **`[U]` IRIN-U4** — this must not be applied silently in either direction.

---

## 6. Indeterminate-severity rules

| ID | Situation | Plausible states | Missing discriminator | Disposition |
|---|---|---|---|---|
| IRIN-IND-1 | Raised ferritin, TSAT absent and underivable | Overload (weeks, specialist pathway) vs inflammatory/dysmetabolic (routine) | TSAT | **IRIN-F8.** Floor at within weeks — the lower-consequence state is routine, but overload cannot be excluded and the discriminating test is cheap and on the same sample. State both, request TSAT `[E]` |
| IRIN-IND-2 | In-range ferritin, CRP raised, anaemia present | Genuine adequate iron vs masked deficiency | TSAT, or CRP-adjusted ferritin interpretation | **IRIN-F5.** Do not report iron status as normal. Contract §3.1 in-range rule applies `[E]` |
| IRIN-IND-3 | Low ferritin, no Hb | Deficiency without anaemia (weeks) vs iron deficiency anaemia (weeks or days) | Haemoglobin | Floor at within weeks; anaemia status not assessable `[C]` |
| IRIN-IND-4 | Raised CRP, no prior | Acute self-limiting vs persistent | Prior CRP | Floor at routine for mild, weeks for marked. Persistence not assessable — **not** reported as absent `[C]` |
| IRIN-IND-5 | Ferritin raised, ancestry unknown | Genuinely raised vs within an ancestry-adjusted expectation | Ancestry | Do not adjust. State the finding on the laboratory range and note the limitation `[J]` |

**IRIN-IND-1 is the domain's most important indeterminate case** and the one most likely to occur, because TSAT is frequently not ordered.

---

## 7. Trend and baseline rules

**Classification: trend-modifying for iron; trend-important for inflammatory.**

| ID | Rule | Class |
|---|---|---|
| IRIN-T1 | Persistence is the principal severity input for CRP. A single raised CRP is weak; a persistent one is a finding `[C]` | `[C]` |
| IRIN-T2 | Falling ferritin within range may indicate depleting stores — contract §3.1 in-range rule `[C]` | `[C]` |
| IRIN-T3 | Response to iron replacement is a trend finding, but HealthIQ does not reliably know treatment status `[J]` | `[J]` |
| IRIN-T4 | No trend-based downgrade rule. A normalising CRP does not exclude the underlying process `[C]` | `[J]` |
| IRIN-T5 | Baseline validity: 6 months for CRP persistence; 12 months for ferritin trajectory `[J]` — unsourced, flagged | `[J]` |

---

## 8. Modifier and interpretability rules

| Marker | Required modifier | Without it |
|---|---|---|
| **Ferritin (raised, for the overload question)** | **TSAT** | Overload question **not assessable**. IRIN-F8 — not a low-confidence overload finding, and not an inflammatory finding by default `[E]` |
| Ferritin (any, for the deficiency question) | CRP | Deficiency cannot be excluded on an in-range ferritin when inflammation is present. State the limitation `[E]` |
| TSAT | Serum iron + TIBC (or transferrin) | **Derive it.** See IRIN-MOD-1 |
| Iron deficiency (for clinical meaning) | Haemoglobin | Anaemia status not assessable `[C]` |

**IRIN-MOD-1 `[C]` — TSAT calculation policy.** TSAT = serum iron ÷ TIBC × 100. Where serum iron and TIBC (or transferrin, from which TIBC is derivable) are both present, **HealthIQ must compute TSAT rather than report it as missing.** Declaring a derivable value unavailable, and thereby routing a resolvable case to IRIN-F8, is a self-inflicted indeterminacy.

**IRIN-MOD-2 `[E]`** — Fasting status affects TSAT; guidance directs repeating a raised TSAT on a fasting sample before further investigation. Affects **confidence and the recommendation**, not tier.

**IRIN-MOD-3 `[E]`** — Where computed, the fact that TSAT was derived rather than directly measured must be stated.

---

## 9. Combination and override register

| ID | Trigger | Direction | Effect | Basis |
|---|---|---|---|---|
| IRIN-OV-1 | Raised ferritin + TSAT >45% | Promote | IRIN-F3, within weeks, specialist pathway | `[E]` |
| IRIN-OV-2 | Raised ferritin + TSAT ≤45% | **Classify** (not promote) | IRIN-F4, routine | `[E]` |
| IRIN-OV-3 | Low ferritin + low Hb | **Cross-domain consolidate** | IRIN-F2 with haematology; single finding; band from the anaemia | `[C]` |
| IRIN-OV-4 | In-range ferritin + raised CRP + anaemia or low TSAT | Promote | IRIN-F5; iron status may not be reported as normal | `[E]` |
| IRIN-OV-5 | Raised CRP + any cytopenia | **Cross-domain promote** | Haematology primary; CRP contextual | `[C]` |
| IRIN-OV-6 | Raised ferritin + abnormal hepatic analytes + TSAT ≤45% | Classify | Dysmetabolic pattern; contextual to the hepatic finding, not an independent concern | `[E]` |
| IRIN-OV-7 | Raised ferritin + abnormal hepatic analytes + TSAT >45% | Promote | IRIN-F3 stands as an independent finding; hepatic does not absorb it | `[E]` |
| IRIN-OV-8 | Raised CRP explaining a raised ferritin | **Demote to contextual** | CRP becomes Tier 3 attached to the iron finding. **Permitted because CRP retains no independent criterion here** — it is a role assignment, not a severity downgrade | `[J]` |

**IRIN-OV-8 note.** This is the one entry in the six workstreams that moves a marker downward. It is a *contextual role assignment* under contract §4.8, permitted only because the CRP in question does not independently meet Tier 0 or Tier 1 criteria. If it does, §4.8 prohibits the assignment and IRIN-OV-8 must not fire. Recorded explicitly so that reconciliation can check it is not a disguised downgrade.

---

## 10. Contextual-marker rules

| Marker | Usual role | Becomes independent when |
|---|---|---|
| **CRP** | **Usually contextual to another domain's finding** — the explanation for a raised ferritin, an anaemia or a cytopenia `[J]` | Marked or persistent unexplained elevation with no other finding to attach to (IRIN-F6/F7) |
| Serum iron | Contextual constituent | Never independent `[C]` |
| Transferrin / TIBC | Contextual constituent; derivation input for TSAT | Never independent `[C]` |
| ESR | Contextual `[C]` | `[U]` IRIN-U5 — role not defined in this version |
| Ferritin (raised, TSAT ≤45%) | Contextual to hepatic or metabolic findings `[E]` | Where no parent finding exists — then IRIN-F4 at routine, orphan handling per contract §6.5 |

**IRIN-CTX-1 `[J]`** — CRP is the landscape's clearest example of a marker whose primary product role is *service to other domains*. Treating it as a concern generator by default would produce high-volume low-value output.

---

## 11. Confidence-only factors

Absent symptoms or infection history; absent menstrual, dietary or bleeding history; absent ancestry; non-fasting sample (for TSAT); absent treatment status (iron replacement, transfusion); absent inflammatory disease history.

**IRIN-CONF-1 `[E]`** — None reduces tier. The BSH raised-ferritin pathway assumes a clinician takes an alcohol, transfusion, family and symptom history; HealthIQ has none of it. That is a standing limitation stated in output, not a reason to demote.

---

## 12. Concern-tier mapping and lead selection

| Tier | Content |
|---|---|
| **Tier 0** | **Empty** (IRIN-U-SD-NEG) |
| Tier 1 | Iron deficiency; IRIN-F3 possible overload; IRIN-F5 masked deficiency; marked or persistent unexplained inflammation |
| Tier 2 | IRIN-F4 inflammatory/dysmetabolic hyperferritinaemia; isolated mild CRP; isolated low serum iron |
| Tier 3 | CRP as explanation; serum iron; transferrin/TIBC; ferritin where contextual to a hepatic finding |

**IRIN-LEAD-1 `[E]`** — Within the domain, IRIN-F3 leads over IRIN-F4 regardless of ferritin magnitude.

**IRIN-LEAD-2 `[C]`** — Where anaemia is present, the consolidated anaemia finding leads and the iron finding is its aetiology, not a competitor.

**IRIN-LEAD-3 `[J]`** — This domain will rarely supply the panel lead. That is correct and expected, not a defect in the ruleset.

**IRIN-LEAD-4** — Cross-domain contests resolve on the common time band only.

---

## 13. Tier 0 specification-only register

**Empty.** This domain has no Tier 0 content and is therefore **not blocked by contract §17**. It is the only workstream that can be released in full without the operational escalation pathway.

**IRIN-T0-1 `[J]`** — This makes iron/inflammatory a candidate for early release if §17 proves slow, though its dependency on haematology (§16) is unaffected by that.

---

## 14. Acceptance scenarios

| # | Panel | Expected |
|---|---|---|
| AS-1 | Ferritin 1400, TSAT 22% | **IRIN-F4, Tier 2, routine.** Inflammatory/dysmetabolic framing. Explicitly state overload is unlikely given TSAT. Magnitude does not promote |
| AS-2 | Ferritin 420, TSAT 58% | **IRIN-F3, Tier 1, within weeks.** Lower ferritin, higher priority. Tests IRIN-S-1 |
| AS-3 | Ferritin 900, TSAT absent, iron and TIBC present | **Compute TSAT** (IRIN-MOD-1), then AS-1 or AS-2 path. State it was derived |
| AS-4 | Ferritin 900, TSAT absent, iron and TIBC absent | **IRIN-F8, Tier 1, within weeks.** Both states stated; TSAT requested. May not default to inflammatory |
| AS-5 | Ferritin 45 (in range), CRP 60, Hb 105 | **IRIN-F5.** Iron status may **not** be reported as normal. Tests contract §3.1 |
| AS-6 | Ferritin 8, Hb 98, MCV 72 | **One** consolidated iron deficiency anaemia finding with haematology. Not two |
| AS-7 | CRP 12, everything else normal | Tier 2, routine, low-specificity framing. **Not Tier 1** — tests the anti-universalisation position |
| AS-8 | CRP 12 on three panels over 9 months | **IRIN-F7, Tier 1, within weeks.** Persistence, not height, promotes |
| AS-9 | CRP 60, platelets 40 × 10⁹/L | Haematology primary and same-day; CRP **contextual**. Tests IRIN-OV-5 |
| AS-10 | Ferritin 1100, ALT 120, TSAT 30% | Hepatic finding leads; ferritin **contextual** to it (IRIN-OV-6). One finding plus context, not two concerns |
| AS-11 | Ferritin 1100, ALT 120, TSAT 55% | **Two** findings — hepatic pattern and IRIN-F3. Hepatic does not absorb the overload concern (IRIN-OV-7) |
| AS-12 | Complete normal iron panel, CRP normal | No-concern output; must state that a normal ferritin does not exclude iron deficiency where inflammation is present, and that CRP was normal at this timepoint only |

---

## 15. No-concern and insufficient-data outputs

**No-concern — mandatory content:**
1. A normal ferritin does not exclude iron deficiency where inflammation is present `[E]`.
2. A normal CRP reflects one timepoint and does not exclude inflammatory disease.
3. Whether TSAT was available or derivable, and if not, that iron overload could not be assessed.
4. Symptoms warrant review irrespective of the summary.

**IRIN-NC-1 `[J]`** — "Your iron levels are fine" is prohibited where CRP is raised or absent.

**Insufficient data:** minimum viable iron assessment is **ferritin**. Where ferritin is raised and TSAT is neither measured nor derivable, an insufficient-data statement for the overload question accompanies the IRIN-F8 finding.

**IRIN-ID-1 `[J]`** — Presented alongside higher-tier findings, never taking the lead.

---

## 16. Cross-domain boundaries

| Marker | This domain's role | Other domain primary when | Disposition |
|---|---|---|---|
| Haemoglobin | Determines whether deficiency is anaemic | Haematology owns the anaemia finding and its severity band | **Consolidate** — one anaemia finding; iron supplies aetiology |
| MCV | Subtype pointer | Haematology owns the band | Reference haematology's band; do not define a competing one |
| Ferritin | Primary | Hepatic uses it as an aetiology-screen constituent | Consolidate into hepatic where TSAT ≤45%; independent where TSAT >45% |
| TSAT | Primary | Hepatic aetiology screen | Same rule as ferritin |
| CRP | Primary, but usually contextual | Inflammatory service to iron, haematology, nutritional | Attach; promote only when orphaned and marked/persistent |
| Albumin | **Not used in this domain as a finding** | Hepatic (synthetic), renal (calcium modifier) | Negative acute-phase reactant role acknowledged as **interpretation context only** (contract §9.6) |

**IRIN-XD-1 `[E]`** — The three named haematology dependencies are: anaemia definition, anaemia severity band, MCV band. This domain **consumes** them and must not redefine them.

---

## 17. Prohibited behaviours (domain additions)

1. Ranking raised ferritin by magnitude.
2. Reporting iron overload as excluded when TSAT is unavailable.
3. Reporting iron status as normal on an in-range ferritin with raised CRP.
4. Declaring TSAT missing when iron and TIBC are present.
5. Creating an anaemia finding separate from haematology's.
6. Treating isolated mild CRP as Tier 1.
7. Applying ancestry-based ferritin adjustment without governed ancestry data.
8. Applying IRIN-OV-8 to a CRP that independently meets Tier 0 or Tier 1.
9. Importing the hepatic Tier 1 floor.
10. Using serum iron alone to assess iron status.

---

## 18. Unresolved questions

| ID | Question | Blocking |
|---|---|---|
| IRIN-U1 | Should any ferritin threshold generate urgency (hyperinflammatory syndromes)? Currently no | No |
| IRIN-U2 | CRP severity bands — none set; no authoritative UK source found | **Yes** for IRIN-U-W-4 |
| IRIN-U3 | Low-TSAT deficiency threshold not set | Yes |
| IRIN-U4 | Ancestry-related ferritin expectations without ancestry data | **Yes** |
| IRIN-U5 | ESR role — undefined | No |
| IRIN-U6 | Sex-specific TSAT/ferritin thresholds are evidence-based `[E]` but require reliable sex data. Behaviour where sex is unknown? | Yes |
| IRIN-U7 | Whether HealthIQ should mention haemochromatosis by name in consumer output, given it is a genetic diagnosis requiring genotyping | Yes — communication |
| IRIN-U8 | Baseline windows (IRIN-T5) unsourced | No |

---

## 19. Evidence table

| Source | Used for |
|---|---|
| BSH — Investigation and management of a raised serum ferritin, *Br J Haematol* 2018 | TSAT as key discriminator; raised-ferritin differential; investigation set |
| Newsome PN et al., BSG. *Gut* 2018 | Ferritin + TSAT >45% specialist referral; dysmetabolic iron overload framing; aetiology-screen role |
| EASL Clinical Practice Guidelines on haemochromatosis, *J Hepatol* 2022 | Sex-specific TSAT/ferritin genotyping thresholds; TSAT >45% elevated |
| BC Guidelines — high ferritin and iron overload (BSH-derived) | Overload excluded below TSAT 45%; ancestry-related reference expectations; non-European HFE prevalence |
| NHS Lothian RefHelp — high ferritin | Sex-differentiated referral TSAT thresholds |

**Gaps:** no authoritative UK source bands CRP severity; ESR role undefined; low-TSAT deficiency threshold not established here.

---

## 20. Clinical sign-off

| Field | Value |
|---|---|
| Version | 0.1 |
| Contract authored against | v0.4 + v0.5 summary — re-check required |
| HMR name / registration | ☐ |
| IRIN-U2 (CRP bands) | ☐ |
| IRIN-U4 (ancestry) | ☐ |
| IRIN-U6 (sex-specific thresholds without sex) | ☐ |
| IRIN-U7 (naming haemochromatosis) | ☐ |
| TSAT derivation policy approved | ☐ |
| IRIN-OV-8 confirmed as role assignment, not downgrade | ☐ |
| Empty Tier 0 confirmed as correct | ☐ |
| Signature / date | ☐ |

---

## VERDICT: READY_FOR_CENTRAL_RECONCILIATION

The iron half is well sourced and the domain's signature rule — TSAT, not ferritin magnitude, determines severity — is directly evidence-supported. The inflammatory half is thinner: CRP has no authoritative UK severity banding, and this ruleset has deliberately declined to invent one rather than import bands by analogy. That gap (IRIN-U2) constrains one within-weeks rule but does not block the domain, because CRP's primary role here is contextual service to other domains rather than concern generation.

The empty Tier 0 is a genuine finding and should be recorded as such: this is the only workstream releasable without contract §17.
