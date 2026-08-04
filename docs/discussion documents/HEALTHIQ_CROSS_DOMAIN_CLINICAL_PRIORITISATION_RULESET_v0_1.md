---
document_id: HEALTHIQ-CROSS-DOMAIN-RULESET-001
title: HealthIQ Cross-Domain Clinical Prioritisation Ruleset
version: "0.1"
governing_contract: HEALTHIQ-CLIN-PRIORITY-CONTRACT-001 v0.5
governing_spec: HEALTHIQ-PARALLEL-DOMAIN-PRIORITY-AUTHORING-001 v0.1
consolidates: Workstreams A–F v0.1/v0.2
status: DRAFT_FOR_HMR_RECONCILIATION
implementation_status: NOT_AUTHORISED
---

# Cross-Domain Clinical Prioritisation Ruleset v0.1

> **Contract availability note.** All six workstreams were authored against contract v0.4 plus the v0.5 principle summary in authoring spec §2, because v0.5 itself was not supplied. The v0.5 principles relied upon — uncapped same-day co-equal group, per-domain indeterminate-severity rules, governed marker–modifier pairs, distinct no-concern and insufficient-data outputs — are all listed in spec §2 and are all incorporated. **A clause-level re-check against actual v0.5 is the first reconciliation action.**

**Evidence labels:** `[E]` · `[C]` · `[J]` · `[U]`.

---

## 1. Consolidation status and workstream verdicts

| WS | Domain | Verdict | Blocking gaps |
|---|---|---|---|
| A | Haematology | `READY_FOR_CENTRAL_RECONCILIATION` | HAEM-U1 severe-anaemia threshold; HAEM-U2 ethnic neutropenia |
| B | Hepatic v0.2 | `READY_FOR_CENTRAL_RECONCILIATION` | HEP-U1 Tier 1 floor policy; HEP-U2 bilirubin threshold |
| C | Renal + electrolytes | **`REQUIRES_ADDITIONAL_DOMAIN_RESEARCH`** | **RE-U2/U3/U4: no cited UK bands for hypokalaemia, hypernatraemia, hypocalcaemia.** RE-U6 Tier 0 release acceptability |
| D | Iron + inflammatory | `READY_FOR_CENTRAL_RECONCILIATION` | IRIN-U2 CRP bands |
| E | Thyroid + endocrine | `READY_FOR_CENTRAL_RECONCILIATION` | ENDO-U1 scope beyond thyroid; THY-U3/U4 pregnancy |
| F | Cardiometabolic + nutritional | `READY_FOR_CENTRAL_RECONCILIATION` | CN-U2 risk calculation (regulatory); CN-U4 vitamin D bands |

**Five of six are reconciliation-ready. Workstream C is not**, and its gap is the one that matters most clinically: three of six electrolyte finding classes have no cited severity bands, in the domain carrying the largest life-threatening Tier 0 surface.

---

## 2. Universal rules — confirmed across all six workstreams

Each held in every domain, with no domain requiring an exception.

| # | Rule | Class |
|---|---|---|
| U1 | The unit of prioritisation is a consolidated clinical finding. Every workstream produced a taxonomy of 8–11 findings from 5–15 markers; none produced one finding per marker | `[E]` |
| U2 | Urgency and severity are separable. Iron/inflammatory has high-consequence findings with an **empty Tier 0**; electrolytes has low-magnitude findings at same day. The two dimensions moved independently in every domain | `[E]` |
| U3 | Confidence affects explanation only. No domain required confidence to control prominence | `[E]` |
| U4 | Supporting-marker count has no role. No domain used it | `[E]` |
| U5 | Frames consolidate before tiering. Load-bearing in haematology (multi-lineage), iron (TSAT/ferritin), thyroid (TSH/fT4) | `[E]` |
| U6 | A finding independently meeting Tier 0/1 may not be assigned contextual role. Every domain produced a boundary: MCV band, platelet 50 boundary, CRP orphan rule, TSAT >45%, thyroid dual role | `[E]` |
| U7 | Missing data reduces confidence, never significance — with two bounded consequences, see §7 | `[E]` |
| U8 | Absent baseline is never evidence of stability. Critical in renal, material in haematology and thyroid | `[E]` |
| U9 | Direction asymmetry is the norm. Ferritin, MCV, TSH, sodium, potassium, calcium, albumin, B12 | `[E]` |
| U10 | **No domain produced a safe trend-based downgrade rule.** Six for six. Contract §12.2's floor protection is doing real work | `[E]` |
| U11 | **New:** an empty Tier 0 is a legitimate domain outcome, not a specification gap. Iron/inflammatory and thyroid both have one | `[J]` |
| U12 | **New:** every domain required at least one mandatory statement in its no-concern output about what a normal result does *not* exclude. This is a universal presentation requirement, not a domain quirk | `[E]` |

**U11 and U12 are new findings from this exercise** and are proposed for the contract at §11.

---

## 3. Urgency time-band register

Common bands per contract §4.1. **This is the only cross-domain comparison surface.**

### 3.1 Same day

| Domain | Criteria |
|---|---|
| Haematology | Platelets <20; platelets <150 with new thrombosis or renal impairment; ANC <0.5; pancytopenia; severe anaemia (`[U]` threshold) |
| Hepatic | ALT/AST ≥10× ULN; ALT/AST >1000 U/L; Hy's law pattern; abnormal analyte + low albumin; abnormal analyte + INR >1.5; jaundice-range bilirubin + abnormal enzymes |
| Renal/electrolyte | K⁺ ≥6.5 (or ≥6.0, `[U]`); Na⁺ <125; adjusted Ca²⁺ >3.0; NICE AKI criteria met; eGFR <15; K⁺ <2.5 (`[U]`) |
| Iron/inflammatory | **None** |
| Thyroid | **None** |
| Cardiometabolic/nutritional | TG >20 mmol/L |

### 3.2 Distribution observation

| Band | Domains contributing |
|---|---|
| Same day | 4 of 6 |
| Within days | 5 of 6 |
| Within weeks | 6 of 6 |
| Routine | 6 of 6 |

**XD-BAND-1 `[E]`** — The time band is the only dimension every domain could express. Severity methods were absolute count, absolute concentration, ULN multiple, disease-stage band, change-from-baseline, pattern relationship, calculated risk and consequence class — **eight incommensurable methods across six domains.** This is the empirical confirmation of contract §4.2's non-comparability clause and §18.24's prohibition.

---

## 4. Shared-marker boundary register

Per authoring spec §7. Every entry records the marker's role in each domain, the boundary at which another domain becomes primary, the disposition, and the applicable band.

| Marker | Domain A role | Domain B role | Boundary | Disposition | Conflict? |
|---|---|---|---|---|---|
| **Platelets** | Haem: cytopenia severity (absolute count) | Hepatic: fibrosis indicator | **50 × 10⁹/L**, and any haem same-day criterion | Above 50 → consolidate into hepatic fibrosis finding preserving the higher band. Below → **haematology primary, consolidation prohibited** (contract §4.8) | Resolved |
| **MCV** | Haem: macrocytosis severity | Hepatic: contextual explanation; Nutritional: B12/folate pointer | **Top of haematology's mild band** (>ULN to 105 fL), and presence of any other FBC abnormality | Within band + isolated → contextual attachment. Outside → haematology primary, independent finding | Resolved. **v0.1 hepatic 10%-of-ULN placeholder deleted** |
| **Haemoglobin** | Haem: anaemia definition and severity (owner) | Iron: deficiency consequence; Inflammatory: ACD; Nutritional: deficiency consequence | Haematology is always the band owner | **Consolidate — one anaemia finding.** Other domains supply aetiology, never a second concern | Resolved |
| **Albumin** | Hepatic: synthetic-function marker | Renal: **calcium modifier**; Inflammatory: negative acute-phase reactant | Role is declared per domain; no global application | Contract §9.6. Renal never treats low albumin as a hepatic finding; hepatic never treats it as a calcium modifier | Resolved — **the landscape's reference case** |
| **Ferritin** | Iron: primary | Hepatic: aetiology-screen constituent; Inflammatory: acute-phase reactant | **TSAT 45%** | TSAT ≤45% → contextual to hepatic/metabolic. TSAT >45% → independent iron finding; hepatic does not absorb | Resolved |
| **TSAT** | Iron: severity determinant | Hepatic: aetiology-screen constituent | — | Iron primary; hepatic references | Resolved |
| **CRP** | Inflammatory: primary but usually contextual | Iron: ferritin interpretation; Haem: cytopenia context; Nutritional: deficiency-marker distortion | Orphan status + marked or persistent | Attach where a parent exists; independent only when orphaned | Resolved |
| **Potassium** | Renal/electrolyte: primary (owned) | — | — | Single owner | Resolved |
| **Creatinine / eGFR** | Renal: primary | Cardiometabolic: CVD-risk context; also nephrotic-syndrome secondary cause for lipids | Renal always primary for the renal finding | Attach contextually to cardiometabolic | Resolved |
| **Thyroid pattern** | Thyroid: primary | Cardiometabolic: lipid secondary cause; Haem: macrocytosis cause | Both stand | **Dual presentation of one fact** — see XD-DUAL-1 | Resolved with a caveat |
| **B12 / folate** | Nutritional: primary | Haem: macrocytosis/anaemia cause | Haematology owns the count bands | Consolidate into one finding | Resolved |
| **Sodium** | Renal/electrolyte: primary | Cardiometabolic: severe hypertriglyceridaemia falsely lowers it `[E]` | — | **Cross-reference required** — see XD-ARTEFACT-1 | **New — see §12** |
| **HbA1c** | Cardiometabolic: primary | Also its own lipid secondary cause | Internal to the domain | Dual role within one workstream | Resolved |

### 4.1 Two boundary rules that required central adjudication

**XD-DUAL-1 `[J]`** — A finding may legitimately appear both as its own concern and as context for another domain's concern (thyroid abnormality that is also a lipid secondary cause; HbA1c likewise). **This is one fact, not two problems**, and the presentation must make that explicit. Domain files may not resolve this alone because neither domain owns the presentation.

**XD-ARTEFACT-1 `[E]` — new, and a genuine safety item.** Severe hypertriglyceridaemia can produce a falsely low sodium. A panel with TG >20 mmol/L may therefore produce **two** same-day findings, one of which is artefactual. Workstream C recorded pseudohyponatraemia as a caveat and workstream F recorded the cross-reference, but neither could close it. **Central rule:** where TG >20 mmol/L coexists with hyponatraemia, the sodium finding carries a mandatory pseudohyponatraemia caveat and confirmation advice; it is **not** suppressed (contract §11), and the triglyceride finding is unaffected.

---

## 5. Cross-domain combination register

| ID | Trigger | Domains | Effect | Class |
|---|---|---|---|---|
| XD-C1 | Thrombocytopenia ≥50 + abnormal hepatic analytes | Haem + Hepatic | Consolidate into hepatic fibrosis finding; higher band preserved | `[E]` |
| XD-C2 | Thrombocytopenia <50 + abnormal hepatic analytes | Haem + Hepatic | **Do not consolidate.** Two findings; haematology leads on band | `[E]` |
| XD-C3 | Low ferritin + low Hb | Iron + Haem | One iron deficiency anaemia finding | `[C]` |
| XD-C4 | B12/folate deficiency + macrocytosis | Nutritional + Haem | One finding | `[E]` |
| XD-C5 | B12 deficiency + pancytopenia | Nutritional + Haem | Haematology same-day; nutritional supplies aetiology | `[E]` |
| XD-C6 | Reduced eGFR + thrombocytopenia | Renal + Haem | Haematology same-day rule fires | `[E]` |
| XD-C7 | Reduced eGFR + hyperkalaemia | Renal + Electrolyte (same WS) | RE-F9; potassium leads on band | `[E]` |
| XD-C8 | Raised ferritin + abnormal hepatic + TSAT ≤45% | Iron + Hepatic | Ferritin contextual to hepatic | `[E]` |
| XD-C9 | Raised ferritin + abnormal hepatic + TSAT >45% | Iron + Hepatic | Two findings; hepatic does not absorb | `[E]` |
| XD-C10 | Raised CRP + any cytopenia | Inflammatory + Haem | Haematology primary; CRP contextual | `[C]` |
| XD-C11 | Abnormal lipids + abnormal thyroid, hepatic, HbA1c or renal | Cardio + others | **Reframe, not downgrade** — secondary cause identified | `[E]` |
| XD-C12 | Hypothyroid pattern + macrocytosis | Thyroid + Haem | Haematology primary; thyroid contextual, and also stands alone | `[C]` |
| XD-C13 | TG >20 + hyponatraemia | Cardio + Electrolyte | **Both stand; pseudohyponatraemia caveat mandatory** | `[E]` |

**XD-COMB-1 `[E]`** — Every consolidation above preserves the highest urgency band and none absorbs a constituent that independently meets Tier 0 or Tier 1 criteria. Contract §9.5 satisfied throughout.

**XD-COMB-2 `[J]`** — XD-C11 is the register's only *reframing* entry. NICE directs excluding secondary causes before **referral**, not before **concern**. The lipid finding retains its floor; only the recommended action changes.

---

## 6. Indeterminate-severity register

Contract §4.9 requires each domain to define its own rule and authorises no universal arithmetic. All six complied.

| Domain | Rules | Reference case |
|---|---|---|
| Haematology | 5 (HAEM-IND-1 to 5) | Low Hb without MCV |
| Hepatic | 5 (HEP-IND-1 to 5) | Raised ALT without ALP |
| Renal/electrolyte | 5 (RE-IND-1 to 5) | Reduced eGFR without baseline |
| Iron/inflammatory | 5 (IRIN-IND-1 to 5) | Raised ferritin without TSAT |
| Thyroid | 5 (THY-IND-1 to 5) | **TSH raised without free T4** |
| Cardiometabolic/nutritional | 5 (CN-IND-1 to 5) | Raised cholesterol without the risk-factor set |

**XD-IND-1 `[J]` — the common pattern.** Independently, all six workstreams converged on the same disposition: **floor at the lower plausible urgency band, state the higher, name the discriminator, recommend the test.** No workstream escalated to worst case; none defaulted to the lowest. This convergence is evidence that contract §4.9's deferral of the arithmetic was correct — six domains reached a consistent disposition through clinical reasoning without a formula.

**XD-IND-2 `[J]`** — THY-IND-1 is offered as the **reference implementation**. It is the case that generated the contract provision, and it is the clearest instance of the trade-off: escalating over-calls a condition affecting ~10% of the population; defaulting low breaches contract §6.1.

**XD-IND-3 — an important distinction the domains surfaced.** Missing modifiers produce **two different consequences**, and both are contract-supported:

| Consequence | When | Reference case |
|---|---|---|
| **Insufficient data** | The value is not a clinical quantity without the modifier | Uncorrected calcium without albumin `[E]` |
| **Indeterminate severity** | The value is real but cannot discriminate between management pathways | TSH without free T4 `[E]` |

This distinction is not currently explicit in contract §8 and is proposed as an amendment (§11, A7).

---

## 7. Marker–modifier register

| Marker | Required modifier | Consequence class | Domain |
|---|---|---|---|
| **Calcium** | **Albumin** | **Insufficient data** — uncorrected calcium is not a clinical quantity `[E]` | Renal/electrolyte |
| Total WCC | Absolute differential | Insufficient data for the neutrophil question `[E]` | Haematology |
| Haemoglobin | Sex | Insufficient data — anaemia thresholds are sex-specific `[E]` | Haematology |
| **TSH** | **Free T4** | **Indeterminate severity** `[E]` | Thyroid |
| Ferritin (raised) | TSAT | Indeterminate severity `[E]` | Iron |
| ALT | ALP | Indeterminate severity — pattern not classifiable `[J]` | Hepatic |
| ALP | GGT | Indeterminate — origin undetermined `[E]` | Hepatic |
| Bilirubin | Conjugated fraction | Indeterminate — Gilbert's may not be asserted `[E]` | Hepatic |
| Creatinine | Valid prior creatinine | Indeterminate — AKI not assessable `[E]` | Renal |
| eGFR | Second result ≥3 months apart | Indeterminate — CKD not assessable `[E]` | Renal |
| eGFR | ACR | Staging incomplete — **structurally unavailable** `[E]` | Renal |
| Lipid profile | Risk-factor set | Indeterminate — risk not computable; named thresholds still apply `[E]` | Cardiometabolic |
| B12 | MMA or homocysteine | Indeterminate — functional status not assessable `[E]` | Nutritional |
| Hb/MCV | Blood film | **Standing limitation, not per-case** — HealthIQ never receives films `[J]` | Haematology |

**XD-MOD-1 `[C]` — derivation obligation.** Where a modifier is **derivable** from markers on the panel, it must be derived rather than reported missing. TSAT from serum iron and TIBC is the reference case; adjusted calcium from calcium and albumin is another. Declaring a derivable value unavailable is a self-inflicted indeterminacy. Derived values must be labelled as derived.

**XD-MOD-2 `[E]`** — Every unevaluable combination criterion is reported as **not assessable**, never as **not met**. All six workstreams implemented this.

---

## 8. Tier 0 specification-only register

Contract §17: no Tier 0 release without the operational escalation pathway.

| Domain | Tier 0 rules | Release status without §17 |
|---|---|---|
| Haematology | 5 | **Blocked for Tier 0**; Tier 1 and below releasable |
| Hepatic | 6 | **Blocked for Tier 0**; Tier 1 and below releasable |
| Renal/electrolyte | 8 | **Blocked for Tier 0** — and see XD-T0-1 |
| Iron/inflammatory | **0** | **Fully releasable** |
| Thyroid | **0** | **Fully releasable** |
| Cardiometabolic/nutritional | 1 | Blocked for that rule only; everything else releasable |
| **Total** | **20** | |

**XD-T0-1 `[U]` — the register's most serious finding.** Renal/electrolyte holds 8 of the 20 Tier 0 rules, and four of them concern potentially life-threatening results: severe hyperkalaemia, profound hyponatraemia, severe hypercalcaemia and AKI. Workstream C's position is that **suppression of Tier 0 in that domain should be treated as a reason to delay the domain's release, not as a workable operating mode.** Central reconciliation endorses that position and escalates it: a product that detects a potassium of 6.8 and has no governed way to act on it is in a worse position than one that does not measure potassium.

**XD-T0-2 `[J]`** — Where Tier 0 is suppressed anywhere, findings are **withheld with an explicit statement, never demoted to Tier 1** (contract §18.19). All six workstreams implemented this identically.

**XD-T0-3 `[J]`** — Iron/inflammatory and thyroid being fully releasable without §17 is a genuine sequencing option, and it interacts with §10.

---

## 9. Same-day co-equal group rules

Per the v0.5 principle (spec §2): same-day findings may form an uncapped co-equal group.

**XD-SD-1 `[J]`** — Where two or more findings from different domains reach the same-day band and no governed cross-domain rule distinguishes them, **all are presented as a co-equal group with no internal ordering.** The co-lead cap does not apply to the same-day band.

**XD-SD-2 `[E]`** — No severity comparison is permitted between members of the group. §3.2 establishes that eight incommensurable severity methods are in play; any ordering between a potassium of 6.8 and an ALT of 6× ULN would be arbitrary, and the arbitrariness would be invisible to the reader.

**XD-SD-3 `[J]`** — Realistic group sizes: two is common (electrolyte + hepatic; haematology + renal), three is plausible on a broad panel with multi-system illness. The presentation must remain intelligible at three.

**XD-SD-4 `[E]`** — Members carrying artefact risk (potassium, platelets, calcium, sodium-with-high-TG) retain their mandatory confirmation wording **inside** the group. Group membership does not simplify the language.

**XD-SD-5 `[J]`** — Where a same-day group exists, no insufficient-data output may take the lead (contract §16.2 as scoped). Limitations are stated alongside.

---

## 10. Cross-domain lead-selection rules

**XD-LEAD-1 `[E]`** — Order by the common urgency time band. This is the only cross-domain comparison surface.

**XD-LEAD-2 `[E]`** — Within a band, severity may be used **only** within a domain. Cross-domain severity comparison is prohibited (contract §18.24).

**XD-LEAD-3 `[J]`** — Where findings from different domains share a band and no governed rule distinguishes them, present as co-leads (§9).

**XD-LEAD-4 — governed cross-domain distinguishers.** Three were identified that legitimately break a within-band tie:

| ID | Rule | Basis |
|---|---|---|
| XD-LEAD-4a | Organ dysfunction outranks marker abnormality at the same band | Generalised from hepatic HEP-LEAD-1 (function outranks injury), tested and held in renal (AKI over urea) and haematology (multi-lineage over single) `[J]` |
| XD-LEAD-4b | Irreversible harm outranks reversible harm at the same band | Nutritional CN-LEAD-2 — B12 neurological damage may not fully recover `[E]` |
| XD-LEAD-4c | Direct measurement outranks derived interpretation at the same band | Contract §7.2 directness-of-evidence, applied cross-domain `[J]` |

**XD-LEAD-5 `[J]`** — These three are proposed as governed cross-domain rules. They are **not** a severity comparison; each is a categorical distinction that applies regardless of the underlying units. They should be ratified individually.

**XD-LEAD-6 `[U]`** — Beyond these three, cross-domain within-band ordering remains unresolved and defaults to co-leads. This is the correct residual behaviour.

---

## 11. Proposed contract amendments

Three arose from this exercise. All are additive.

### A7 — Two consequences of a missing modifier (**required**)

Contract §8 routes uninterpretable markers to insufficient data. The workstreams surfaced a second, distinct consequence.

> Where a governed rule identifies a required modifier, its absence produces one of two consequences, declared per marker–modifier pair: **insufficient data**, where the marker is not a clinical quantity without the modifier (uncorrected calcium); or **indeterminate severity** under §4.9, where the marker is a valid measurement that cannot discriminate between materially different management pathways (TSH without free T4). The consequence class must be declared in the domain's marker–modifier register.

`[E]` — both reference cases are evidence-supported and behave differently.

### A8 — Derivation obligation (**recommended**)

> Where a required modifier is derivable from markers present on the panel, it must be derived rather than reported unavailable. Derived values must be labelled as derived. Failure to derive an available value is not a legitimate route to indeterminate severity or insufficient data.

`[C]` — TSAT and adjusted calcium are the reference cases.

### A9 — Empty Tier 0 as a legitimate outcome (**recommended**)

> A domain may have no Tier 0 content. An empty Tier 0 is a clinical property of the domain, not a specification gap, and must not be treated as an omission during review. Domains with empty Tier 0 registers are not constrained by §17.

`[J]` — iron/inflammatory and thyroid both reached this position independently.

---

## 12. Prohibited universalisation register

Every entry was tested against at least one domain that falsifies it.

| # | Candidate | Verdict | Falsifying domain |
|---|---|---|---|
| P1 | Multiples of ULN as a universal severity metric | **Prohibited** | Electrolytes: K⁺ 6.6 ≈ 1.25× ULN and an emergency `[E]` |
| P2 | Reference-range abnormality as a universal Tier 1 floor | **Prohibited — hepatic-bound** | Haematology (isolated mild macrocytosis, Tier 2 with reassurance) and inflammatory (isolated mild CRP, Tier 2) `[E]` |
| P3 | Supporting-marker count | **Prohibited** | All six — none used it |
| P4 | Requirement for corroboration before raising a finding | **Prohibited** | Nutritional: functional B12 deficiency with in-range serum level `[E]` |
| P5 | Trend-based downgrading | **Prohibited as a general mechanism** | All six — none produced a safe one; hepatic evidence actively contradicts it `[E]` |
| P6 | Static domain priority | **Prohibited** | Contract §14 principle; no domain requested it |
| P7 | Fixed ordering of marker classes | **Prohibited** | Iron sometimes outranks hepatic; hepatic sometimes outranks haematology; order is data-dependent `[E]` |
| P8 | Worst-case severity inheritance under missing data | **Prohibited** | Thyroid: would over-call a condition affecting ~10% of the population `[C]` |
| P9 | Percentage white-cell differentials | **Prohibited** | Haematology `[E]` |
| P10 | Hepatic "any abnormality warrants an aetiology screen" framing | **Prohibited outside hepatic** | Same as P2 `[E]` |
| P11 | **New:** R-value as a general pattern classifier | **Prohibited outside hepatic** | Meaningless in every other domain; it is a DILI causality convention `[C]` |
| P12 | **New:** absolute-concentration severity as a universal method | **Prohibited** | Correct for electrolytes, meaningless for lipids (risk) and thyroid (pattern) `[E]` |
| P13 | **New:** persistence-as-severity | **Prohibited as universal** | Correct for CRP; hepatic evidence shows persistence is near-universal there and therefore non-discriminating (84% at 1 month, 75% at 2 years) `[E]` |
| P14 | **New:** consequence-class severity | **Prohibited as universal** | Correct for nutritional (irreversibility); no equivalent basis in electrolytes or lipids `[J]` |

**XD-PROHIB-1** — P11 to P14 are new to this exercise and each arises from a domain-specific severity method that worked well enough locally to look generalisable. **The pattern to watch is that every domain's best idea is the one most likely to be wrongly exported.**

---

## 13. Acceptance-test matrix

Cross-domain scenarios that no single workstream can validate alone.

| # | Panel | Expected | Tests |
|---|---|---|---|
| XD-AS-1 | K⁺ 6.8; ALT 300 (6.1× ULN) | **Same-day co-equal group**, both presented, no ordering, no severity comparison. Potassium carries artefact-confirmation wording | §9; P1 |
| XD-AS-2 | Platelets 45; ALT 200; albumin normal | **Two findings.** Haematology primary — below the 50 boundary, consolidation prohibited. Haematology leads on band | XD-C2; contract §4.8 |
| XD-AS-3 | Platelets 120; ALT 200; AST 260 | **One finding** — hepatic fibrosis pattern, platelets consolidated. AST:ALT >1 supports it | XD-C1 |
| XD-AS-4 | Ferritin 420; TSAT 58%; ALT 90 | **Two findings** — hepatic pattern and iron overload. Hepatic does not absorb | XD-C9 |
| XD-AS-5 | Ferritin 1400; TSAT 22%; ALT 90 | **One finding plus context** — hepatic leads, ferritin contextual | XD-C8; P1 |
| XD-AS-6 | TSH 14, free T4 unavailable; LDL 5.9 | Thyroid indeterminate (Tier 1, weeks) **and** thyroid as lipid secondary cause. **One fact, two presentations** | XD-DUAL-1; §6 |
| XD-AS-7 | TG 24; Na⁺ 128 | **Both same-day.** Sodium carries mandatory pseudohyponatraemia caveat; neither suppressed | XD-ARTEFACT-1 |
| XD-AS-8 | B12 110; Hb 82; platelets 88; neutrophils 1.1 | **One finding** — pancytopenia, same day, B12 as aetiology. Not four findings | XD-C5; U1 |
| XD-AS-9 | Calcium 2.85, albumin absent; K⁺ 6.7 | Potassium same-day; calcium **insufficient data**, presented alongside, **not leading** | §7; contract §16.2 scoping |
| XD-AS-10 | eGFR 38 (no baseline); MCV 104; CRP 9; TSH 5.8, free T4 normal | Renal Tier 1 (AKI not assessable); MCV Tier 2 isolated; CRP Tier 2; thyroid Tier 2. **Renal leads; three Tier 2 findings compressed.** No hepatic-style floor applied to MCV or CRP | P2; contract §15.2 |
| XD-AS-11 | Entirely normal broad panel | No-concern output carrying **six domain-specific "does not exclude" statements** — fibrosis, kidney disease without ACR, functional B12 deficiency, iron deficiency under inflammation, evolving thyroid disease, CVD risk from other factors | U12 |
| XD-AS-12 | K⁺ 6.8; platelets 18; TG 24 | **Three-member same-day group.** Tests XD-SD-3 intelligibility ceiling |

---

## 14. Unresolved questions — clinical, product and regulatory

### 14.1 Clinical (HMR)

| ID | Question | Source | Blocking |
|---|---|---|---|
| C-1 | **Hypokalaemia, hypernatraemia and hypocalcaemia bands** — no cited UK sources | WS C | **Yes — the exercise's largest gap** |
| C-2 | Potassium urgent threshold: UKKA >6.5 or CCS/KDIGO >6.0 | WS C | Yes |
| C-3 | Severe-anaemia threshold for same-day escalation | WS A | Yes |
| C-4 | Benign ethnic neutropenia without ancestry data | WS A | Yes |
| C-5 | Hepatic Tier 1 floor: adopt BSG Rec 4 literally or a documented departure | WS B | Yes |
| C-6 | Bilirubin jaundice-range threshold | WS B | Yes |
| C-7 | CRP severity bands | WS D | Yes |
| C-8 | Vitamin D bands — deliberately not adopted | WS F | Yes |
| C-9 | **Pregnancy across all six domains.** Thyroid suppresses; haematology, hepatic, renal and cardiometabolic exclude. **No domain handles it, and pregnancy status is usually unknown** | All | **Yes** |
| C-10 | Sex-specific thresholds (Hb, TSAT/ferritin) where sex is unknown | A, D | Yes |
| C-11 | Ancestry-related reference expectations (neutrophils, ferritin) | A, D | Yes |
| C-12 | Baseline validity windows — every domain set them by judgement; none is sourced | All | Yes |
| C-13 | **Which rules are unsafe without clinical context, as opposed to merely lower-confidence?** Every workstream raised this independently | All | **Yes** |

### 14.2 Product (Anthony)

| ID | Question |
|---|---|
| P-1 | Same-day co-equal group presentation at three members (XD-SD-3) |
| P-2 | Tier 1 volume control, given hepatic HEP-P2 and XD-AS-10 |
| P-3 | XD-DUAL-1 presentation — one fact appearing in two roles |
| P-4 | Whether domains with empty Tier 0 registers may be released ahead of those blocked by §17 |
| P-5 | Six mandatory "does not exclude" statements in a single no-concern output (XD-AS-11) — how presented without becoming unreadable |
| P-6 | Whether HealthIQ names conditions (haemochromatosis, FH, Hashimoto's) in consumer output |

### 14.3 Regulatory

| ID | Question | Source |
|---|---|---|
| R-1 | **Calculated cardiovascular risk** — the most device-like output in the landscape | WS F, CN-U2 |
| R-2 | **FIB-4** — a calculated score with referral implications | WS B, HEP-U5 |
| R-3 | Whether Tier 0 action-and-timeframe guidance is permissible in the chosen regulatory model | Contract §22.5 |
| R-4 | Whether domain-level suppression (thyroid in pregnancy) creates a documented limitation of intended purpose | WS E |

---

## 15. Assessment and evidence position

### 15.1 What the exercise established

Six unlike domains expressed their findings in one set of clinical dimensions. **Not one required confidence to control prominence, supporting-marker count to determine priority, or one-finding-per-marker.** Eight incommensurable severity methods coexisted without a single cross-domain severity comparison. The common time band carried every cross-domain contest that could be carried.

The parallel method also worked as intended in one specific way worth recording: **six workstreams independently converged on the same indeterminate-severity disposition** without a shared formula. That convergence is stronger evidence for the contract's approach than any single domain could have provided.

### 15.2 Where the evidence is thinnest

| Domain | Evidence position |
|---|---|
| Cardiometabolic | **Strongest** — NICE CG181 supplies every referral threshold directly |
| Renal (not electrolyte) | Strong — NICE NG148, NG203, UKKA |
| Thyroid | **Stronger than expected** — NICE NG145 supplies pattern definitions and the ≥10 threshold. The cross-domain validation's "weakest domain" assessment is superseded |
| Hepatic | Strong for pathways, **weak for numeric bands** — no UK guideline bands transaminases |
| Haematology | Strong for platelets, **weak for anaemia severity** — WHO explicitly declines to establish outcome-linked bands |
| Iron | Strong |
| Inflammatory | **Weakest** — no authoritative UK CRP severity banding exists |
| Electrolytes | Strong for K⁺, Na⁺, Ca²⁺ high; **absent for three finding classes** |

### 15.3 The limitation no guideline addresses

Every workstream raised C-13 independently, in its own words. UK guidance is written for clinicians who hold history, examination, symptoms, medication lists and prior results. HealthIQ holds a panel. That does not make interpretation impossible — this exercise demonstrates it does not — but the question of **which rules are unsafe without context, rather than merely lower-confidence**, has not been decided anywhere in the governance chain. It is not a confidence question and it is not answerable domain by domain. It belongs here, and it belongs to the Head of Medical Research.

---

## VERDICT: REQUIRES_CROSS_DOMAIN_ADJUDICATION

The consolidated model is coherent. Five of six workstreams are reconciliation-ready, the universal-rule set held across all six, the shared-marker register resolves every boundary, and the cross-domain combination register preserves urgency and floors throughout. No hepatic-specific concept has escaped into general use, and four new prohibited-universalisation entries were caught before they could.

The verdict is not `READY_FOR_HMR_RECONCILIATION` for three reasons, in order of weight:

**First, workstream C returned `REQUIRES_ADDITIONAL_DOMAIN_RESEARCH`** and its gap is three missing severity band sets in the domain holding eight of the landscape's twenty Tier 0 rules. Consolidating around an incomplete electrolyte ruleset would leave findings that can be created but not graded, and the implementation-time temptation would be to fill them by analogy from potassium — the exact universalisation P1 prohibits.

**Second, XD-T0-1 is a scope decision, not a threshold.** Renal/electrolyte carries four potentially life-threatening Tier 0 rules. Whether that domain may be released with Tier 0 suppressed determines what the product is, and it cannot be settled inside a domain file.

**Third, C-9 (pregnancy) is unhandled across the whole landscape.** Every domain excluded or suppressed it, pregnancy status is usually unknown, and no workstream could resolve it alone. Six coordinated exclusions are not a policy.

None of these is a defect in the model. All three are decisions that require the Head of Medical Research, and one (XD-T0-1) additionally requires product and legal input. Three contract amendments (A7–A9) are proposed and all are additive.
