---
document_id: HEALTHIQ-XD-ACCEPTANCE-SCENARIO-MEDICAL-ADJUDICATION-001
title: HealthIQ Cross-Domain Acceptance-Scenario Medical Adjudication
version: "0.1"
role: Head of Medical Research — bounded medical-authority review
reviews: HEALTHIQ_CROSS_DOMAIN_ACCEPTANCE_SCENARIO_APPROVAL_PACK_v1_0.md
governing_contract: HEALTHIQ-CLIN-PRIORITY-CONTRACT-001 v0.6.3
status: MEDICAL_ADJUDICATION_COMPLETE
implementation_status: NOT_AUTHORISED
---

# Cross-Domain Acceptance-Scenario Medical Adjudication v0.1

## 1. Scope and authority

A bounded medical-authority review of the gaps identified in the Claude Code acceptance-scenario approval pack v1.0. It supplies **only the minimum medical decisions** needed to allow a complete acceptance-scenario pack to be prepared.

It is not a repeat of the six-domain research, not a redesign, and not an approval of the scenarios on Anthony's behalf.

The approval pack is an architecture and consistency artefact. It is **not clinical authority**, and where its wording and the ratified clinical documents differ, the ratified documents govern.

**Authority hierarchy applied throughout:** later ratified cross-domain authority governs over conflicting or stale wording in an earlier domain document. Where a domain ruleset contains two clauses that cannot both be true, the categorical taxonomy rule governs over an incidental band listing, and the inconsistency is recorded rather than silently resolved.

**Boundaries observed.** No code, no repository change, no architecture, no frontend mechanics, no Cursor prompt, no regulatory or legal closure, no Tier 0 activation, no release authorisation.

---

## 2. Documents reviewed

| # | Document | Version | Role |
|---|---|---|---|
| 1 | Clinical Finding Prioritisation Contract | v0.6.3 | Governing clinical policy |
| 2 | Cross-Domain Clinical Prioritisation Ruleset | v0.5 | Governing cross-domain rules |
| 3 | Cross-Domain HMR Adjudication Register | v0.4 | Closed adjudications |
| 4 | Six-Domain Clinical Closure Report | v0.4 | Package position |
| 5 | Haematology Prioritisation Ruleset | v0.1 | Domain source |
| 6 | Hepatic Prioritisation Ruleset | v0.2 | Domain source |
| 7 | Renal and Electrolyte Prioritisation Ruleset | v0.1 | Domain source |
| 8 | Iron and Inflammatory Prioritisation Ruleset | v0.1 | Domain source |
| 9 | Thyroid and Endocrine Prioritisation Ruleset | v0.1 | Domain source |
| 10 | Cardiometabolic and Nutritional Prioritisation Ruleset | v0.1 | Domain source |
| 11 | Electrolyte Supplemental Evidence | v0.1 | Domain source |
| 12 | Product Ratification — Clinician-First Model | v1.0 | Product-layer authority |
| 13 | Acceptance-Scenario Approval Pack | v1.0 | Subject of review |

**Documentation note, non-blocking.** Document 6 is labelled as adopting contract v0.4 plus a summary. It must be relabelled to v0.6.3. This is the known outstanding relabel item and does not affect any determination below, since later cross-domain authority governs.

---

## 3. Decisions not reopened

Confirmed closed and untouched by this adjudication:

- **HEP-U1** — hepatic Tier 1 floor, literal BSG position;
- **B2** — potassium >6.0 mmol/L same day;
- **A8** — vitamin D thresholds and contextual handling;
- **A5** — no severe-anaemia same-day threshold;
- **A4, A9, A6, A7, A10, B4, B6, B7** and all other entries recorded closed in adjudication register v0.4;
- **P2, P7, P8** and the fifteen ratified product principles in clinician-first v1.0 §18.

Nothing in this document alters a tier, threshold, band, override or consolidation rule.

---

## 4. Item-by-item classification

| Item | Subject | Classification |
|---|---|---|
| **A** | `RE-AS-11` urea selector | `MEDICAL_CLARIFICATION_OF_EXISTING_AUTHORITY` |
| **B** | "More serious tier wins" scenario | `ADMINISTRATIVE_ALIGNMENT_ONLY` |
| **C** | Two-co-lead cap below same-day | `MEDICAL_CLARIFICATION_OF_EXISTING_AUTHORITY` (with one residual `PRODUCT_DECISION_REQUIRED`) |
| **D** | Missing modifiers, no worst-case inference | `ADMINISTRATIVE_ALIGNMENT_ONLY` |
| **E** | Tier 0 withheld but not downgraded | `ADMINISTRATIVE_ALIGNMENT_ONLY` |
| **F** | Disease-name quarantine | `ADMINISTRATIVE_ALIGNMENT_ONLY` (release of disease names remains `REGULATORY_DECISION_REQUIRED`, R4) |
| **G1–G5** | `HAEM-EX-1`, `-2`, `-4`, `-5`, plus `-3` tier | `ADMINISTRATIVE_ALIGNMENT_ONLY` |
| **G3b** | `HAEM-EX-3` lead framing | `MEDICAL_CLARIFICATION_OF_EXISTING_AUTHORITY` |
| **G6** | `HAEM-EX-6` state disambiguation | `MEDICAL_CLARIFICATION_OF_EXISTING_AUTHORITY` |
| **H** | Four stale scenarios | `ADMINISTRATIVE_ALIGNMENT_ONLY` — no medical objection |

**No item required a new clinical adjudication. No item was excluded for insufficient evidence.**

---

## 5. Item A — `RE-AS-11`, isolated raised urea

**Classification: `MEDICAL_CLARIFICATION_OF_EXISTING_AUTHORITY`**

### 5.1 A deterministic selector already exists

The renal/electrolyte ruleset contains two clauses that cannot both govern:

- **`RE-CONS-3`** (§3, finding taxonomy): *"Urea does not form an independent finding. It is a constituent or contextual."* — a categorical taxonomy rule.
- **`RE-U-W-4`** (§4.3, urgency bands): *"Isolated raised urea with normal creatinine"* listed at within weeks — a band entry that presupposes an independent finding.

**`RE-CONS-3` governs.** Three reasons, in order of weight:

1. It is the taxonomy rule that determines whether a finding exists at all. A band entry cannot create a finding class that the taxonomy denies; it can only band one the taxonomy has already established.
2. Contract §3.1 makes the consolidated clinical finding the unit of prioritisation. Urea is a constituent of the renal picture, not a finding.
3. Clinician-first v1.0 §8 defines contextual information as *"relevant information that helps explain the clinical picture but would not independently drive action"*. An isolated raised urea with normal creatinine and normal eGFR does not, on its own, generate a renal management action. Its common causes — reduced fluid intake, high protein intake, catabolic states, corticosteroids, reduced renal perfusion — are interpreted from the wider picture, not from the urea value.

`RE-U-W-4` is an authoring inconsistency and is superseded.

### 5.2 The orphan case — and why the source looked ambiguous

`RE-AS-11` has **normal creatinine and eGFR**, so there is no renal parent finding for the urea to attach to. This is contract §6.5's orphan Tier 3 case, and it is almost certainly why the original author reached for a Tier 1 alternative: the intuition that the value cannot simply vanish is correct.

Contract §6.5 offers two resolutions — promote to Tier 2 with de-escalating language, or present in a distinct low-prominence group.

**Adjudication: the low-prominence contextual group.** Promoting to Tier 2 would attach a monitoring or planned-reassessment action class (clinician-first §9) that an isolated raised urea does not warrant, and would create exactly the independent management priority `RE-CONS-3` excludes. The low-prominence group preserves reconcilability with the raw value — which contract §6.5 requires — without inventing an action.

### 5.3 Expected outcome for `RE-AS-11`

| Field | Value |
|---|---|
| Inputs | Urea 12 mmol/L; creatinine normal; eGFR normal |
| Consolidated finding | **None.** Urea does not form an independent finding (`RE-CONS-3`) |
| Urgency | Not applicable — no finding, therefore no urgency band |
| Severity | Not applicable |
| Tier | **Tier 3 — contextual** |
| Role | **Contextual information** (clinician-first §8) |
| Parent | None present. Orphan handling under contract §6.5 → **distinct low-prominence contextual group**, remaining reconcilable with the raw value |
| Missing-data behaviour | None triggered. Urea has no governed modifier |
| Override | None |
| Action class | **None.** No action class is assigned to a Tier 3 contextual item |
| Prohibited | Presenting urea as renal impairment or renal failure (renal ruleset §17 item 9); assigning it an independent tier or action |

### 5.4 One thing deliberately not created

The urea:creatinine ratio is a recognised pointer to hypovolaemia and to upper gastrointestinal bleeding. **No governed rule exists for it**, and I have not created one — the instruction not to invent a threshold applies, and a combination rule of that consequence should be authored deliberately rather than as a by-product of resolving a scenario ambiguity.

`RE-U5` (does urea ever form an independent finding without clinical context?) remains open in the renal ruleset. This adjudication resolves `RE-AS-11` without resolving `RE-U5`, and the two should not be conflated. **Recommendation for a future adjudication cycle, not now:** consider whether a raised urea with anaemia, or a markedly raised urea:creatinine ratio, warrants a governed combination rule. That is `NEW_MEDICAL_ADJUDICATION_REQUIRED` if pursued, and it is out of scope here.

---

## 6. Item B — "more serious tier wins"

**Classification: `ADMINISTRATIVE_ALIGNMENT_ONLY`**

Existing authority is sufficient. Contract §6.1 assigns the initial tier as the more serious of the urgency-derived and severity-derived tiers. A demonstrating scenario needs a case where the two genuinely differ, using only enumerated governed bands on both sides.

**Potassium 6.2 mmol/L is that case**, and it is the cleanest available because both sides are fully enumerated.

### Proposed scenario `XD-AS-31`

| Field | Value |
|---|---|
| Inputs | K⁺ 6.2 mmol/L; creatinine, eGFR and all other analytes normal |
| Consolidated finding | Hyperkalaemia (`RE-F3`) |
| **Urgency-derived tier** | **Tier 0** — K⁺ >6.0 mmol/L is same day under the closed B2 adjudication |
| **Severity-derived tier** | **Tier 1** — 6.0–6.4 mmol/L is the UKKA *moderate* band, which maps below Tier 0 |
| **Final tier** | **Tier 0** — the more serious of the two governs (contract §6.1) |
| Expected lead role | **Principal concern.** Sole finding on the panel |
| Expected action | Same day. Mandatory artefact-safe wording (`RE-A-WORD-1`) — urgent repeat and clinical contact, without asserting that the result is genuine or that it is artefact |
| Runtime state | **Tier 0 specification-only.** Withheld and auditable; see Item E |
| Demonstrates | Urgency and severity are assessed independently; a moderate severity band does not cap a same-day urgency |

**Why this case rather than a lipid case.** Triglycerides >20 mmol/L also diverge — same-day urgency for pancreatitis against a long-term-risk severity method — but the cardiometabolic ruleset does not enumerate a severity-derived tier for lipids, so one side of the demonstration would have to be asserted rather than cited. The potassium case cites both sides.

---

## 7. Item C — two-co-lead cap below same-day

**Classification: `MEDICAL_CLARIFICATION_OF_EXISTING_AUTHORITY`**, with one residual product option.

### 7.1 The cap itself is ratified

Clinician-first v1.0 §6 settles it: *"Below the same-day band, the default maximum is two co-leads. Additional clinically important findings remain visible in their assigned tier."* Reinforced by §10, which prohibits suppressing an independent concern because another ranks higher, downgrading to reduce visible volume, and hiding findings because the display is crowded.

No new policy is needed to author a scenario.

### 7.2 The clarification required

The pack's difficulty is real but is a misreading of what the cap does. With three equally-ranked Tier 1 findings in the same time band and no governed cross-domain distinguisher, selecting *which two* are co-leads would require the cross-domain severity comparison that contract §18.24 prohibits — and the three candidate distinguishers were deliberately left unratified (ruleset v0.5 §13 `XD-LEAD-4`, removed).

**The clarification is this: the two-co-lead cap is a ceiling on co-leads, not a requirement to produce two.**

Clinician-first §5 directs presenting one principal concern *"where the governed clinical findings show that one issue clearly matters most"*. Where none clearly matters most, §5 does not compel a lead, and §6 explicitly warns that co-lead status *"must not be used merely to avoid making a difficult prioritisation decision"* — which cuts against manufacturing two co-leads out of three co-equals just as much as it cuts against manufacturing one.

The governed outcome is therefore: **no forced lead; all three remain visible in Tier 1; co-leads are presented only where a governed rule establishes co-equality between exactly two.**

This is clinically right as well as procedurally right. A clinician presented with new renal impairment, possible iron overload and overt hypothyroidism would not rank two of them and demote the third; they would address all three.

### 7.3 Proposed scenario `XD-AS-32`

| Field | Value |
|---|---|
| Inputs | eGFR 38, no prior creatinine; ferritin 420 µg/L with TSAT 58%; TSH 14 mIU/L with free T4 low |
| Findings | Three consolidated findings: reduced eGFR of undetermined chronicity (`RE-F10`); possible iron overload (`IRIN-F3`); overt hypothyroidism (`THY-F1`) |
| Urgency | All three **within weeks** |
| Tier | All three **Tier 1** |
| Co-leads | **None forced.** No governed rule establishes co-equality between any two, and no governed distinguisher separates them |
| Visibility | **All three visible as Tier 1 concerns**, in their assigned tier |
| Cap behaviour | The two-co-lead ceiling is not breached because no co-leads are designated. The cap does not require two |
| Prohibited | Selecting two co-leads by cross-domain severity comparison (contract §18.24); suppressing the third to satisfy a display convention (clinician-first §10) |
| Missing-data behaviour | Renal finding must state that acute change could not be assessed without a prior creatinine (`UWC-2`) |
| Demonstrates | Clinician prioritisation, not display convenience — the result is three concerns because a clinician would address three |

### 7.4 The residual, and it belongs to product

**`PRODUCT_DECISION_REQUIRED`** — if the product layer requires a lead to be populated in every case for interface reasons, that is a product decision, and it cannot be satisfied clinically. There is no ratified clinical distinguisher to select one, and creating one would reopen the three distinguishers the HMR declined to ratify.

I record this as a product question rather than answering it. If it is pursued, the clinical constraint is that any forced selection must not be presented to the user as a clinical judgement that one finding matters more.

---

## 8. Item D — missing modifiers and worst-case inference

**Classification: `ADMINISTRATIVE_ALIGNMENT_ONLY`**

Contract §8.1 supplies both consequences; §4.9 and §18.25 supply the prohibitions; clinician-first §12 supplies the product obligation. Two governed cases demonstrate the full behaviour and no new threshold is needed.

### 8.1 Proposed scenario `XD-AS-33` — indeterminate severity

| Field | Value |
|---|---|
| Inputs | TSH 14 mIU/L; free T4 **not measured**; no other abnormality |
| Consolidated finding | Indeterminate thyroid-axis abnormality (`THY-F5`, via `THY-IND-1`) |
| Missing modifier | Free T4 |
| Consequence class | **Indeterminate severity** — TSH is a valid measurement that cannot discriminate between materially different management pathways (contract §8.1) |
| Urgency | **Within weeks** — the band at which both plausible states converge on the same immediate action |
| Severity | **Indeterminate.** Not resolved to either state |
| Tier | **Tier 1** |
| Role | Principal concern (sole finding) |
| Required output | Both plausible states stated — subclinical and overt hypothyroidism; free T4 named as the discriminating test and recommended |
| **Prohibited — worst-case** | Assigning the overt-hypothyroidism severity on the strength of the missing marker (contract §18.25) |
| **Prohibited — default-low** | Defaulting to subclinical because it is commoner (contract §6.1) |
| **Prohibited — suppression** | Reducing tier, prominence or lead eligibility because free T4 is absent (contract §4.5, §8.1) |
| Demonstrates | A missing modifier produces a declared indeterminate state, not an inference in either direction |

### 8.2 Proposed scenario `XD-AS-34` — insufficient data

| Field | Value |
|---|---|
| Inputs | Total calcium 2.05 mmol/L; albumin **not measured**; all other analytes normal |
| Consolidated finding | **None for calcium.** Uncorrected calcium is not a clinical quantity without albumin |
| Missing modifier | Albumin |
| Consequence class | **Insufficient data** (contract §8.1; `UWC-1`) |
| Tier | Not applicable — no finding is created |
| Required output | Insufficient-data state for the calcium question, **visible**, with albumin named as the required modifier |
| **Prohibited** | Creating a hypocalcaemia finding from the uncorrected value; representing the calcium as normal; silently omitting the calcium question |
| Placement | Presented alongside any other findings; may not take the lead (contract §16.2 as scoped) |
| Demonstrates | The second missing-modifier consequence, and that it is a declared visible state rather than a silent omission |

**Why both are needed.** The two consequences behave differently and the pack does not currently test the distinction. `XD-AS-33` produces a finding; `XD-AS-34` does not. Testing only one would leave the contract §8.1 distinction unverified.

---

## 9. Item E — Tier 0 withheld but not downgraded

**Classification: `ADMINISTRATIVE_ALIGNMENT_ONLY`**

Contract §17 and clinician-first v1.0 §9 both supply the required behaviour. No pathway design is performed here.

### Proposed scenario `XD-AS-35`

| Field | Value |
|---|---|
| Inputs | K⁺ 6.8 mmol/L; no repeat sample; eGFR 55 |
| Consolidated finding | Hyperkalaemia with renal impairment (`RE-F9`) |
| **Clinical classification** | **Tier 0.** Same day. This classification is made and recorded regardless of release state |
| **Runtime state** | **Withheld — specification-only.** The Tier 0 operational pathway is not authorised (R1) |
| Auditability | The withheld Tier 0 evaluation must remain **auditable**: the classification, the rule that fired, and the fact of withholding are all recorded |
| **Prohibited — downgrade** | Presenting the finding as Tier 1 or Tier 2. Contract §17 and §18.19; clinician-first §9: *Tier 0 must never be silently downgraded* |
| **Prohibited — no-concern** | Treating the withheld state as a no-concern result, or omitting the finding from the output |
| Expected user-facing state | The finding is present and visible; what is withheld is the **same-day action-and-timeframe guidance**, not the finding |
| Demonstrates | Clinical classification and runtime release state are independent; suppression of an action pathway does not alter the clinical tier |

**Clarification worth recording.** Withholding operates on the **guidance**, not on the finding. A reading in which the whole finding disappears would breach clinician-first §10 (must not hide clinically meaningful findings) and would produce the exact false-reassurance outcome contract §16 exists to prevent.

---

## 10. Item F — disease-name quarantine

**Classification: `ADMINISTRATIVE_ALIGNMENT_ONLY`** for the scenario. Release of consumer-facing disease names remains **`REGULATORY_DECISION_REQUIRED`** (R4) and is not decided here.

Clinician-first v1.0 §14 supplies the permitted wording set and the internal-provenance permission.

### Proposed scenario `XD-AS-36`

| Field | Value |
|---|---|
| Inputs | Ferritin 420 µg/L; TSAT 58%; ALT, ALP and all other hepatic analytes normal |
| Consolidated finding | Possible iron overload (`IRIN-F3`, via `IRIN-OV-1`) |
| Urgency | Within weeks |
| Tier | **Tier 1** |
| Role | Principal concern |
| **Finding visible** | **Yes.** The governed clinical finding is presented in full |
| **Consumer-facing wording** | Must use the §14 permitted set — for example a raised transferrin saturation with raised ferritin as a **biochemical pattern** that **warrants investigation**, and which **may be associated with** iron accumulation |
| **Prohibited consumer-facing** | Naming haemochromatosis, or any wording implying a genetic diagnosis. HFE genotyping has not been performed and the governed evidence supports a pattern, not a diagnosis |
| **Permitted internally** | The disease concept may remain in internal provenance, rule identifiers, clinical source material and approved clinician-facing material (§14) |
| Intended purpose | User-facing wording must remain within the approved intended purpose and must not become an unauthorised medical instruction (§11) |
| Demonstrates | Quarantine constrains the **label**, not the **finding**. The clinical concern is fully visible; only the diagnostic name is withheld |

**Why this case.** Iron overload is the strongest test in the landscape: the finding is genuinely important, the disease name is well known to consumers, and the evidence supports a pattern requiring investigation rather than a diagnosis. A scenario built on a weaker finding would not test the tension.

---

## 11. Item G — `HAEM-EX-1` to `HAEM-EX-6`

All six are clinically governed by the haematology ruleset. **None requires a change to its underlying clinical result.** Five need only field completion; two need a stated clarification.

### `HAEM-EX-1` → proposed `HAEM-AS-1` — `ADMINISTRATIVE_ALIGNMENT_ONLY`

| Field | Value |
|---|---|
| Inputs | Platelets 18 × 10⁹/L; Hb 128 g/L (male); MCV 92 fL |
| Consolidated finding | Severe thrombocytopenia (`HAEM-F4`) |
| Urgency | **Same day** (`HAEM-U-SD-1`) |
| Severity band | **Severe** — platelets <20 × 10⁹/L |
| Tier | **Tier 0** — specification-only, withheld per Item E |
| Role | **Principal concern** |
| Supporting/contextual | Hb 128 g/L is marginally below the WHO male anaemia threshold of 130 g/L and forms a separate mild finding; it does not compete for lead |
| Missing-data | None. No film available — standing domain limitation (`HAEM-IND-5`), stated |
| Override | None fired. `HAEM-OV-4` does not apply — no thrombosis or renal impairment present |
| Action class | Immediate/same-day contact, with the mandatory pseudothrombocytopenia confirmation caveat |

### `HAEM-EX-2` → proposed `HAEM-AS-2` — `ADMINISTRATIVE_ALIGNMENT_ONLY`

| Field | Value |
|---|---|
| Inputs | Hb 95 g/L; MCV 78 fL; platelets normal |
| Consolidated finding | **One** finding — anaemia, microcytic subtype (`HAEM-F1` via `HAEM-OV-6`) |
| Urgency | **Within weeks** (`HAEM-U-W-2`) |
| Severity band | Anaemia present by WHO definition. **No severity sub-band exists** — A5 declined to create one |
| Tier | **Tier 1** |
| Role | Principal concern |
| Supporting/contextual | MCV is a constituent of the consolidated finding, **not** a separate concern |
| Cross-domain | Iron domain supplies aetiology within this finding; **anaemia must not appear twice** (U15) |
| Missing-data | Ferritin not stated in the source scenario; if absent, iron status is not assessable and must be stated |
| Override | `HAEM-OV-6` |
| Action class | Further investigation |

### `HAEM-EX-3` → proposed `HAEM-AS-3` — `MEDICAL_CLARIFICATION_OF_EXISTING_AUTHORITY`

The source states "no lead from this domain", which is contingent framing rather than a tier assignment. **Clarification: the tier is not contingent; the lead role is.**

| Field | Value |
|---|---|
| Inputs | MCV 99.5 fL; remainder of FBC normal |
| Consolidated finding | Isolated macrocytosis (`HAEM-F2`) |
| Urgency | **Routine** (`HAEM-U-R-1`) |
| Severity band | **Mild macrocytosis** |
| Tier | **Tier 2 — unconditionally.** The tier does not depend on what else is on the panel |
| Role | **Determined by the wider panel**, not by this domain. Principal concern where no higher-tier finding exists; contextual attachment where a hepatic or nutritional parent exists and the mild-band boundary is met (`HEP-CTX-1`) |
| Missing-data | None |
| Override | `HAEM-OV-3` does **not** fire — no other FBC abnormality |
| Action class | Monitoring or planned reassessment |
| Anti-universalisation | **The hepatic Tier 1 floor must not be applied here.** This is the load-bearing counterexample (`XD-HEP-FLOOR-2`) |

### `HAEM-EX-4` → proposed `HAEM-AS-4` — `ADMINISTRATIVE_ALIGNMENT_ONLY`

| Field | Value |
|---|---|
| Inputs | MCV 99.5 fL; platelets 140 × 10⁹/L; Hb 118 g/L (female) |
| Consolidated finding | **One** finding — multi-lineage cytopenia (`HAEM-F10`) |
| Urgency | **Within days** (`HAEM-U-D-3`, two-lineage) |
| Severity band | Individually: Hb below the female anaemia threshold; platelets borderline (100–149). **Collectively the combination governs** |
| Tier | **Tier 1** |
| Role | Principal concern |
| Supporting/contextual | The individual cytopenias are **constituents**, not separate concerns |
| Missing-data | No film — standing limitation, stated |
| Override | **`HAEM-OV-1`** — two lineages reduced |
| Action class | Further investigation |
| Demonstrates | Three individually low-tier values producing one higher-tier finding — consolidation doing genuine clinical work |

### `HAEM-EX-5` → proposed `HAEM-AS-5` — `ADMINISTRATIVE_ALIGNMENT_ONLY`

| Field | Value |
|---|---|
| Inputs | Absolute neutrophil count 0.4 × 10⁹/L; remainder of FBC normal |
| Consolidated finding | Severe neutropenia (`HAEM-F6`) |
| Urgency | **Same day** (`HAEM-U-SD-3`) |
| Severity band | **Severe** — ANC <0.5 × 10⁹/L |
| Tier | **Tier 0** — specification-only, withheld per Item E |
| Role | Principal concern |
| Missing-data | Ancestry not captured. **No adjustment is made** (`XD-ANC-1`); the limitation is stated. Benign ethnic neutropenia cannot be excluded and this must not alter the band |
| Override | None |
| Action class | Immediate/same-day contact |
| Note | The Tier 0 specification-only caveat, absent from the informal source entry, is restated here |

### `HAEM-EX-6` → proposed `HAEM-AS-6` — `MEDICAL_CLARIFICATION_OF_EXISTING_AUTHORITY`

The pack correctly identifies an undisambiguated indeterminate/insufficient-data mix. **Clarification: these are two distinct states attaching to two distinct questions, not one ambiguous state.**

| Field | Value |
|---|---|
| Inputs | Total WCC 3.1 × 10⁹/L; **no differential**; remainder of FBC normal |
| **Finding 1** | **Low total white cell count** — a valid consolidated finding. Tier 1, within weeks |
| **Finding 2 — the neutrophil question** | **Insufficient data.** The absolute differential is a governed modifier of total WCC; without it the neutrophil question cannot be validly constructed (contract §8.1; `HAEM-IND-2`) |
| Why insufficient data rather than indeterminate severity | Total WCC is a valid measurement for the *leucopenia* question and produces a finding. It is **not** a valid measurement for the *neutrophil* question at all, because neutropenia is defined on the absolute count. The consequence class differs by question, and both may coexist on one panel |
| **Prohibited** | Reporting neutrophils as normal; inferring a neutrophil count from the total; suppressing either state |
| Required output | Both states visible; the absolute differential named and requested |
| Action class | Further investigation, plus repeat with differential |
| Demonstrates | A single panel carrying a valid finding and an insufficient-data state simultaneously |

---

## 12. Item H — stale and superseded scenarios

**Classification for all four: `ADMINISTRATIVE_ALIGNMENT_ONLY`. No medical objection.**

| Scenario | Correction | Medical position |
|---|---|---|
| `HEP-AS-4` | ALT 60 U/L (1.2× ULN) isolated → **Tier 1 only** | Correct. HEP-U1 closed on the literal BSG position; the magnitude-gated alternative is not retained. The either/or wording is stale, not a live clinical question. **One addition:** the scenario must also carry the `XD-HEP-FLOOR-1` point 4 requirement — a minor abnormality must **not** be described as urgent merely because it enters Tier 1 |
| `RE-AS-2` | K⁺ 6.2 mmol/L → **Tier 0 only** | Correct. B2 closed on >6.0 mmol/L same day. Note this scenario now overlaps `XD-AS-31` (Item B); they may coexist, since `RE-AS-2` tests the threshold and `XD-AS-31` tests the tier algebra |
| `CN-AS-11` | Superseded by `XD-AS-26` | Correct, with one clarification. The **tier is unchanged** (Tier 2), but the **basis has changed entirely**: `CN-AS-11` showed an ungraded finding with a statement that no governed threshold existed; `XD-AS-26` is a governed vitamin D deficiency finding under the closed A8 adjudication. The scenario must be replaced, not merely relabelled, or the provenance will misrepresent why the tier is what it is |
| `HEP-AS-10` | Retain the finding; **FIB-4 must not be computed or displayed** while quarantined | Correct. The fibrosis finding runs on AST:ALT ratio and platelets, which are direct observations. Quarantine removes the **calculation**, not the finding (`XD-QUAR-1`). The caveat must be explicit in the scenario, since its absence is what the pack flagged |

---

## 13. Evidence references

| Determination | Authority |
|---|---|
| Urea not an independent finding | Renal/electrolyte ruleset `RE-CONS-3`; contract §3.1; clinician-first §8 |
| Orphan Tier 3 handling | Contract §6.5 |
| More-serious-tier-wins | Contract §6.1 |
| Potassium >6.0 same day | Adjudication register v0.4, B2 (closed) |
| Potassium 6.0–6.4 moderate band | UK Kidney Association hyperkalaemia guideline, via electrolyte supplemental evidence v0.1 |
| Two-co-lead cap below same-day | Clinician-first v1.0 §6 |
| Lead not compelled absent a clearly-first finding | Clinician-first v1.0 §5, §6 |
| Prohibition on cross-domain severity comparison | Contract §18.24; ruleset v0.5 §7 |
| Two missing-modifier consequences | Contract §8.1 |
| No worst-case inference | Contract §18.25, §9.4 |
| No default-low inference | Contract §6.1 |
| Thyroid indeterminate rule | Thyroid ruleset `THY-IND-1`; NICE NG145 pattern definitions |
| Calcium requires albumin | Renal ruleset `RE-MOD-1`; ruleset v0.5 `UWC-1` |
| Tier 0 withheld not downgraded | Contract §17; clinician-first v1.0 §9 |
| Disease-name wording set | Clinician-first v1.0 §14 |
| TSAT >45% iron overload | BSH raised ferritin guideline; BSG; EASL — via iron ruleset `IRIN-OV-1` |
| Platelet <20 same day | Barts Health; King's Health Partners — via haematology `HAEM-U-SD-1` |
| ANC <0.5 same day | Haematology ruleset `HAEM-U-SD-3` |
| Isolated macrocytosis Tier 2 | NHS Scotland isolated macrocytosis pathway — via `HAEM-U-R-1` |
| No ancestry adjustment | Ruleset v0.5 `XD-ANC-1`; register v0.4 P8 |
| Anaemia never appears twice | Ruleset v0.5 U15 |

---

## 14. Unresolved items and required authority

| # | Item | Required authority | Blocking the acceptance pack? |
|---|---|---|---|
| 1 | Forced lead where three or more co-equal Tier 1 findings exist and no governed distinguisher applies | **Product** (Anthony). Not clinically resolvable without reopening the unratified lead distinguishers | **No** — the governed clinical outcome (no forced lead, all visible) is complete and sufficient to author `XD-AS-32` |
| 2 | Tier 0 activation for all 18 rules | **Regulatory/legal** (R1) | No — scenarios are authored against the specification-only state |
| 3 | Consumer-facing disease-name release | **Regulatory/legal** (R4) | No — `XD-AS-36` is authored against the quarantined state |
| 4 | Urea:creatinine ratio as a governed combination rule | **Future medical adjudication**, deliberately not created here | No — `RE-AS-11` is fully resolved without it |
| 5 | `RE-U5` — whether urea ever forms an independent finding with clinical context | **Open in the renal ruleset**; unaffected by this adjudication | No |
| 6 | Questionnaire rationalisation carry-forward | **Implementation**, deferred | No for scenario authoring; yes for release |
| 7 | Hepatic ruleset relabel to v0.6.3 | **Documentation** | No |

**No item on this list requires further medical research.** Items 1, 2 and 3 are non-medical dependencies; item 4 is a discretionary future enhancement; items 5, 6 and 7 are pre-existing and unaffected.

---

## 15. Summary of proposed scenarios

Nine new or completed scenarios, all authored from existing clinical authority:

| ID | Subject | Item |
|---|---|---|
| `RE-AS-11` (revised) | Isolated raised urea — Tier 3 contextual, orphan handling | A |
| `XD-AS-31` | More serious tier wins — K⁺ 6.2 | B |
| `XD-AS-32` | Three Tier 1 findings, no forced lead | C |
| `XD-AS-33` | Indeterminate severity — TSH without free T4 | D |
| `XD-AS-34` | Insufficient data — calcium without albumin | D |
| `XD-AS-35` | Tier 0 withheld, not downgraded — K⁺ 6.8 | E |
| `XD-AS-36` | Disease-name quarantine — iron overload | F |
| `HAEM-AS-1` to `HAEM-AS-6` | Six haematology scenarios formalised | G |

Plus four administrative corrections under Item H.

**None changes an underlying clinical result.** Where the informal source and the formal scenario differ, the difference is field completion or a stated clarification, never a different clinical answer.

---

## VERDICT: MEDICALLY_COMPLETE_WITH_EXPLICIT_NON_MEDICAL_DEPENDENCIES

Every item in the acceptance-scenario pack requiring medical interpretation is resolved from existing ratified authority. **No new clinical adjudication was required and no item was excluded for insufficient evidence.**

Two items needed a stated clarification rather than a new decision, and both were the same kind of problem: a categorical rule and an incidental listing that could not both govern (`RE-AS-11`), and two distinct states that had been read as one ambiguous state (`HAEM-EX-6`). Neither is a gap in the clinical model; both are authoring artefacts that the pack was right to surface.

The verdict carries "explicit non-medical dependencies" because three items remain outside medical authority and must travel with the pack: **Tier 0 activation (R1, regulatory)**, **consumer-facing disease-name release (R4, regulatory)**, and **whether the product requires a lead to be populated when no finding clearly matters most (product)**. The scenarios are authored against the current constrained state of all three, so none blocks the pack from being completed — but none may be treated as resolved by this document.

This adjudication is returned for architecture review and subsequent Anthony ratification where required. **It does not approve the acceptance scenarios**, authorise Tier 0, authorise release, or close any regulatory dependency.
