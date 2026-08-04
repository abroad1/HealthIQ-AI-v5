---
document_id: HEALTHIQ-CROSS-DOMAIN-RULESET-001
title: HealthIQ Cross-Domain Clinical Prioritisation Ruleset
version: "0.2"
supersedes: "0.1"
governing_contract: HEALTHIQ-CLIN-PRIORITY-CONTRACT-001 v0.6
incorporates:
  - HEALTHIQ-HMR-CROSS-DOMAIN-RECONCILIATION-001 v0.1
  - HEALTHIQ-ELECTROLYTE-SUPPLEMENTAL-EVIDENCE-001 v0.1
status: DRAFT_FOR_FINAL_INDEPENDENT_CONSISTENCY_REVIEW
implementation_status: NOT_AUTHORISED
---

# Cross-Domain Clinical Prioritisation Ruleset v0.2

**Evidence labels:** `[E]` · `[C]` · `[J]` · `[U]`.

---

## 0. Changes from v0.1

| # | Change |
|---|---|
| 1 | **Contract v0.5 conformance completed.** v0.1 was authored against v0.4 plus a principle summary; the actual v0.5 has now been read and every workstream checked clause by clause (§1) |
| 2 | Supplemental electrolyte evidence incorporated; RE-U2, RE-U3, RE-U4 closed (§4) |
| 3 | Accepted rules separated from unresolved policy decisions throughout |
| 4 | Unsourced thresholds removed or quarantined (§5) |
| 5 | Interim pregnancy policy adopted (§6) |
| 6 | Unsafe-without-context register created (§7) |
| 7 | Tier 0 count corrected from 20 to **23**; all specification-only (§9) |
| 8 | Cardiovascular risk calculation and FIB-4 quarantined pending regulatory approval (§10) |
| 9 | Thyroid-only limitation stated explicitly (§11) |
| 10 | Proposed cross-domain lead distinguishers **removed** — unratified (§13) |
| 11 | Acceptance-test matrix updated (§15) |

---

## 1. Contract v0.5 conformance

The six workstreams were authored against v0.4 plus the v0.5 principle summary. v0.5 has now been read. It differs from v0.4 in six substantive respects, all of which were the corrections raised at the v0.4 confirmatory review.

| v0.5 change | Workstream conformance |
|---|---|
| §5 — interpretability validation moved **before** urgency and severity classification | **Conforms.** Every domain's marker–modifier rules gate interpretability before grading. Renal calcium-without-albumin is the reference case and behaves correctly |
| §7.4 — co-lead cap does not apply to same-day; multiple indistinguishable same-day findings form one co-equal group | **Conforms.** v0.1 §9 already specified an uncapped same-day group |
| §9.4 — severity inheritance applies to **present** constituents and does not authorise worst-case inference from a missing discriminator | **Conforms.** All 30 indeterminate rules floor at the lower plausible band; none inherits worst case |
| §16.2 — insufficient-data limitation scoped to the affected finding or domain; cannot displace a Tier 0/1 lead | **Conforms.** Every domain has an explicit "-ID-1" clause to this effect |
| §20.18 — governed indeterminate-severity rules required per domain | **Conforms.** Six domains, five rules each |
| §21.1 — haematology must supply an indeterminate-severity rule and distinguish specification-only Tier 0 | **Conforms.** HAEM §6 and §13 |

**XD-CONF-1** — No non-conformance found. One documentation correction: the hepatic ruleset v0.2 states it adopts "v0.4 plus summary" and must be relabelled to adopt **v0.6** before ratification (contract §21.2).

---

## 2. Universal rules — accepted

Confirmed across all six workstreams; accepted in principle by the HMR reconciliation §2.

| # | Rule | Class |
|---|---|---|
| U1 | The unit of prioritisation is a consolidated clinical finding | `[E]` |
| U2 | Urgency and severity are separable | `[E]` |
| U3 | Confidence affects explanation only, never prominence, tier or lead | `[E]` |
| U4 | Supporting-marker count, frame count and panel completeness have no role in priority | `[E]` |
| U5 | Frames consolidate before tiering | `[E]` |
| U6 | A finding independently meeting Tier 0/1 may not be assigned contextual role | `[E]` |
| U7 | Missing data reduces confidence, never clinical significance | `[E]` |
| U7a | Missing modifiers produce one of two declared consequences — insufficient data or indeterminate severity (contract §8.1) | `[E]` |
| U8 | Absent baseline is never evidence of stability | `[E]` |
| U9 | Direction asymmetry is the norm | `[E]` |
| U10 | No trend-based downgrade is authorised as a universal mechanism | `[E]` |
| U11 | An empty Tier 0 register is a legitimate domain outcome (contract §6.2) | `[J]` |
| U12 | No-concern outputs require domain-specific statements of what a normal result does not exclude | `[E]` |
| U13 | Derived modifiers must be calculated where inputs permit, under a governed derivation contract (contract §8.2) | `[C]` |
| U14 | Unevaluable combination criteria are reported as not assessable, never as not met | `[E]` |
| U15 | Anaemia must never appear twice | `[E]` |
| U16 | Domain-specific conventions may not be exported without cross-domain validation and contract amendment | `[E]` |

---

## 3. Urgency time-band register

Contract §4.1 bands. **The only cross-domain comparison surface.**

### 3.1 Same day — 23 rules, all specification-only

| Domain | Criteria | Count |
|---|---|---|
| Haematology | Platelets <20; platelets <150 with new thrombosis or renal impairment; ANC <0.5; pancytopenia; severe anaemia (**threshold open — A5**) | 5 |
| Hepatic | ALT/AST ≥10× ULN; >1000 U/L; Hy's law pattern; abnormal analyte + low albumin; abnormal analyte + INR >1.5; jaundice-range bilirubin + abnormal enzymes (**threshold open — A9**) | 6 |
| Renal/electrolyte | K⁺ ≥6.5 or >6.0 (**open — B2**); **K⁺ <2.5 (new)**; Na⁺ <125; **Na⁺ ≥155 (new)**; adjusted Ca²⁺ >3.0; **adjusted Ca²⁺ <1.9 (new)**; NICE AKI criteria met; eGFR <15 | 8 |
| Iron/inflammatory | **None** | 0 |
| Thyroid | **None** | 0 |
| Cardiometabolic/nutritional | TG >20 mmol/L | 1 |

**Correction from v0.1:** the total is **23**, not 20. Renal/electrolyte holds 8 — unchanged in count because the three new rules replace the three provisional `[U]` placeholders that were not countable.

### 3.2 Severity-method incommensurability — retained finding

Eight methods across six domains: absolute count, absolute concentration, ULN multiple, disease-stage band, change-from-baseline, pattern relationship, calculated long-term risk, consequence class. **No cross-domain severity comparison is possible or permitted** (contract §18.24).

---

## 4. Electrolyte bands — newly incorporated

Full derivation in `HEALTHIQ_ELECTROLYTE_SUPPLEMENTAL_EVIDENCE_v0_1.md`.

| Finding | Bands | Same-day trigger | Grade |
|---|---|---|---|
| Hypokalaemia | Mild 3.0–3.4 · Moderate 2.5–2.9 · Severe <2.5 | K⁺ <2.5 | `[E]` |
| Hypernatraemia | Mild 146–150 · Moderate 151–155 · Severe >155 | Na⁺ ≥155 | **`[C]` — no UK national guideline bands this direction** |
| Hypocalcaemia | Mild >1.9 asymptomatic · 1.9–2.1 intermediate · Severe <1.9 and/or symptomatic | Adjusted Ca²⁺ <1.9 | `[E]` |

**XD-ELEC-1 `[E]`** — All hypocalcaemia bands apply to **adjusted** calcium only. Uncorrected calcium without albumin is an insufficient-data output (contract §8.1).

**XD-ELEC-2 `[E]`** — Hypokalaemia biochemical banding is explicitly arbitrary without symptoms and ECG. HealthIQ may state the concentration band; it may not characterise the consequence as mild.

**XD-ELEC-3 `[E]`** — The severe-hypocalcaemia definition includes "symptomatic at any level below the reference range". **HealthIQ cannot evaluate that limb and will systematically under-detect emergencies between 1.9 and the lower reference limit.** Mitigation is symptom-conditional user-facing language, not a lower band and not suppression.

**XD-ELEC-4 `[J]`, open** — Na⁺ 146–154 placed at within days (HYPERNA-J1). Requires adjudication — register A4.

---

## 5. Removed and quarantined thresholds

Contract §18 prohibits presenting a finding with no governed severity or indeterminate disposition, and prohibits temporary thresholds carried forward as precedent.

| Threshold | v0.1 status | v0.2 action |
|---|---|---|
| Hepatic 10%-of-ULN MCV contextual margin | Deleted in hepatic v0.2 | **Confirmed removed.** Replaced by haematology's governed mild band |
| Vitamin D bands | Not adopted; finding created ungraded | **QUARANTINED.** Finding may not be issued until A8 resolves. Vitamin D retained as contextual to hypocalcaemia only |
| CRP "marked elevation" (IRIN-U-W-4) | Implicit, unthresholded | **QUARANTINED.** CRP promotes on **persistence only** until A10 resolves. The unthresholded marked-elevation route is withdrawn |
| Anaemia severity sub-bands | Absent | **Remains absent.** Anaemia caps at within days until A5 resolves. Oncology grading may not be imported |
| Subclinical hyperthyroidism bands | Absent | **Remains absent** (A6). Mirroring the hypothyroid ≥10 threshold is prohibited — direction asymmetry |
| Low-TSAT deficiency threshold | Absent | **Withdrawn as a requirement** (A7). Deficiency runs on ferritin; TSAT is the overload discriminator only |
| Baseline-validity windows | `[J]` throughout | **Retained as interim, explicitly labelled adjudicated.** AKI windows (48h, 7d) remain `[E]` |
| Haematology sex-unknown default to female Hb threshold | Proposed | **REJECTED by HMR.** Replaced: state the assumption and treat as indeterminate under §4.9 until sex is captured (B5) |

---

## 6. Interim pregnancy policy — adopted

Per contract v0.6 §26.

| Domain | Pregnancy materially affects reference framework? | Affected findings |
|---|---|---|
| Haematology | **Yes** `[E]` | Anaemia thresholds (dilutional); platelet thresholds (gestational thrombocytopenia) |
| Hepatic | **Yes** `[E]` | ALP (physiologically raised); albumin (physiologically reduced) |
| Renal/electrolyte | **Yes** `[E]` | eGFR (physiologically raised); sodium |
| Iron/inflammatory | **Yes** `[C]` | Ferritin and Hb in pregnancy |
| Thyroid | **Yes** `[E]` | All patterns — trimester-specific ranges |
| Cardiometabolic/nutritional | **Yes** `[E]` | Lipids rise physiologically; risk tools not validated |

**XD-PREG-1** — All six domains declare pregnancy as material. Where pregnancy is known, affected findings produce an explicit out-of-scope, specialist-rules-required output. **Silent suppression is prohibited** — this replaces the thyroid workstream's proposed domain suppression.

**XD-PREG-2** — Where pregnancy status is unknown, output states that interpretation assumes non-pregnant adult reference rules. Since all six domains are affected, this is a **single panel-level statement**, not six.

**XD-PREG-3 `[U]`** — Wording requires Anthony (P7) and interacts with intended-purpose (R5).

---

## 7. Unsafe-without-context register

Per contract v0.6 §27. Tests: (a) value not interpretable at all; (b) reference framework changes; (c) action category materially changes.

| ID | Rule | Missing context | Test | Behaviour when absent |
|---|---|---|---|---|
| UWC-1 | Any calcium finding | Albumin | (a) | Insufficient-data output |
| UWC-2 | AKI detection | Valid prior creatinine | (a) | AKI reported **not assessable** |
| UWC-3 | Hypokalaemia 3.0–3.4 | Cardiac status, digoxin | (c) | Band fires; **no mild-consequence language**; state that severity depends on symptoms and ECG |
| UWC-4 | Hypocalcaemia 1.9 to lower reference limit | Symptoms | (c) | Band fires; **must** state that any level below range is an emergency if symptomatic, and list recognised symptoms |
| UWC-5 | Thyroid patterns | Treatment status | (c) | State the result cannot be interpreted without knowing treatment status; do not assume untreated |
| UWC-6 | Hepatic INR >1.5 criterion | Anticoagulation status | (c) | Criterion fires; state anticoagulation not excluded |
| UWC-7 | All pregnancy-affected findings | Pregnancy status | (b) | Contract §26 |
| UWC-8 | Statin-doubling hepatic rule | Statin start date, pre-statin baseline | (a) | Criterion **not assessable** |
| UWC-9 | TG >20 urgent rule | Alcohol intake, glycaemic control | (c) | **Rule fires with the qualifier stated.** Must not be suppressed — HbA1c on the panel resolves one limb |
| UWC-10 | B12 with neurological features | Symptoms | (c) | Cannot fire on biochemistry alone; the deficiency finding stands at its own band |
| UWC-11 | Sex-dependent thresholds (Hb, TSAT/ferritin) | Sex | (b) | Indeterminate under §4.9; state the assumption; **no silent default** |
| UWC-12 | Neutrophil bands | Ancestry | (b) | **No adjustment.** State the limitation. There is no conservative direction |

**XD-UWC-1 `[J]`** — Twelve rules across six domains. Everything not listed is deemed safe to run without context and must not be silently withheld (contract §27.3).

---

## 8. Shared-marker ownership and boundaries — accepted

| Marker | Owner | Other roles | Boundary | Disposition |
|---|---|---|---|---|
| Haemoglobin | **Haematology** | Iron, inflammatory, nutritional (consequence) | Haematology always owns the band | Consolidate — one anaemia finding |
| MCV | **Haematology** | Hepatic, nutritional (context) | Top of mild band; any other FBC abnormality | Contextual within band; independent outside |
| Platelets | **Haematology** | Hepatic (fibrosis indicator) | **50 × 10⁹/L**, and any haematology same-day criterion | Consolidate above; haematology primary below |
| Ferritin / TSAT | **Iron** | Hepatic (aetiology screen), inflammatory | **TSAT 45%** | ≤45% contextual to hepatic; >45% independent |
| Albumin | **Domain-conditional — no single owner** | Hepatic (synthetic function); renal (calcium modifier); inflammatory (negative APR) | Role declared per domain | Contract §9.6. **Landscape reference case** |
| CRP | **Inflammatory** | Iron, haematology, nutritional | Orphan status + persistence | Attach where a parent exists |
| Potassium | **Renal/electrolyte** | — | — | Single owner |
| Creatinine / eGFR | **Renal** | Cardiometabolic (CVD context, nephrotic secondary cause) | Renal always primary | Attach contextually |
| Thyroid pattern | **Thyroid** | Cardiometabolic (lipid secondary cause), haematology (macrocytosis cause) | Both stand | **One fact, two presentations** (XD-DUAL-1) |
| B12 / folate | **Nutritional** | Haematology (consequence) | Haematology owns count bands | Consolidate |
| Sodium | **Renal/electrolyte** | Cardiometabolic (pseudohyponatraemia with severe hypertriglyceridaemia) | — | Cross-reference — XD-ARTEFACT-1 |
| HbA1c | **Cardiometabolic** | Own lipid secondary cause | Internal | Dual role within one domain |

### 8.1 Two central rules

**XD-DUAL-1 `[J]`** — A finding may appear both as its own concern and as context for another domain's concern. **One fact, not two problems.** Presentation requires Anthony (P3).

**XD-ARTEFACT-1 `[E]`** — Where TG >20 mmol/L coexists with hyponatraemia, the sodium finding carries a mandatory pseudohyponatraemia caveat and confirmation advice. **Neither finding is suppressed.** Both may reach same day; both enter the co-equal group.

---

## 9. Cross-domain combination register — accepted

| ID | Trigger | Effect | Class |
|---|---|---|---|
| XD-C1 | Thrombocytopenia ≥50 + abnormal hepatic | Consolidate into hepatic fibrosis finding; higher band preserved | `[E]` |
| XD-C2 | Thrombocytopenia <50 + abnormal hepatic | **Do not consolidate.** Haematology primary | `[E]` |
| XD-C3 | Low ferritin + low Hb | One iron deficiency anaemia finding | `[C]` |
| XD-C4 | B12/folate deficiency + macrocytosis | One finding | `[E]` |
| XD-C5 | B12 deficiency + pancytopenia | Haematology same-day; nutritional supplies aetiology | `[E]` |
| XD-C6 | Reduced eGFR + thrombocytopenia | Haematology same-day rule fires | `[E]` |
| XD-C7 | Reduced eGFR + hyperkalaemia | RE-F9; potassium leads on band | `[E]` |
| XD-C8 | Raised ferritin + abnormal hepatic + TSAT ≤45% | Ferritin contextual to hepatic | `[E]` |
| XD-C9 | Raised ferritin + abnormal hepatic + TSAT >45% | Two findings | `[E]` |
| XD-C10 | Raised CRP + any cytopenia | Haematology primary; CRP contextual | `[C]` |
| XD-C11 | Abnormal lipids + abnormal thyroid, hepatic, HbA1c or renal | **Reframe, not downgrade** | `[E]` |
| XD-C12 | Hypothyroid pattern + macrocytosis | Haematology primary; thyroid contextual and also stands | `[C]` |
| XD-C13 | TG >20 + hyponatraemia | Both stand; pseudohyponatraemia caveat mandatory | `[E]` |
| **XD-C14** | **Hypokalaemia + hypomagnesaemia, or hypocalcaemia + hypomagnesaemia** | **New.** Magnesium requested as a companion; refractory pattern noted. Not a modifier — neither finding is uninterpretable without it | `[E]` |

Every consolidation preserves the highest urgency band; none absorbs a constituent independently meeting Tier 0/1 (contract §9.5).

---

## 10. Quarantined capabilities pending regulatory approval

| Capability | Status | Register |
|---|---|---|
| **Individual cardiovascular risk calculation** | **PROHIBITED pending regulatory approval.** May not be computed or displayed. Named NICE referral thresholds remain permitted — they are thresholds, not risk calculations | R2 |
| **FIB-4** | **PROHIBITED pending regulatory approval.** Hepatic fibrosis findings may run on AST:ALT ratio and platelets, which are direct observations | R3 |
| Tier 0 action-and-timeframe guidance | **All 23 rules specification-only** pending contract §17 | R1 |
| Disease naming | Pending P4/R4 | — |

**XD-QUAR-1 `[J]`** — Quarantine removes the *calculation*, not the *finding*. A raised cholesterol still produces a finding; what is withheld is a computed risk percentage. Contract §18 prohibits suppressing findings, not withholding derived scores.

---

## 11. Scope limitations — stated explicitly

**XD-SCOPE-1** — **Thyroid-only coverage does not constitute endocrine coverage.** Workstream E covers TSH, free T4, free T3 and TPO antibodies. Cortisol, PTH, sex hormones and IGF-1 have **no rules**. PTH is inseparable from calcium (owned by renal/electrolytes) and cortisol requires dynamic testing HealthIQ cannot perform. Any extension is **new authoring**, not a revision (B7).

**XD-SCOPE-2** — Excluded populations across all domains: paediatric and neonatal; pregnancy (contract §26); dialysis and transplant recipients; post-chemotherapy and post-transplant counts.

**XD-SCOPE-3** — Structurally unavailable data: blood film; ACR (so CKD staging is incomplete by construction); urine output (so one AKI criterion is unavailable); urine electrolytes; blood gases; symptoms and examination.

**XD-SCOPE-4 `[E]`** — Coagulation is not covered and no rules exist. Nearly all abnormalities are acute and HealthIQ has no clinical context. A scoping decision should precede any rule authoring.

---

## 12. Tier 0 register — 23 rules, all specification-only

| Domain | Count | Release status without §17 |
|---|---|---|
| Haematology | 5 | Tier 0 blocked; Tier 1 and below releasable |
| Hepatic | 6 | Tier 0 blocked; Tier 1 and below releasable |
| Renal/electrolyte | 8 | **See XD-T0-1** |
| Iron/inflammatory | **0** | **Fully releasable** (contract §6.2, §17) |
| Thyroid | **0** | **Fully releasable** |
| Cardiometabolic/nutritional | 1 | That rule blocked; rest releasable |

**XD-T0-1 `[U]`, escalated** — Renal/electrolyte holds 8 of 23, of which six concern potentially life-threatening results: severe hyperkalaemia, severe hypokalaemia, profound hyponatraemia, severe hypernatraemia, severe hypercalcaemia, severe hypocalcaemia — plus AKI and kidney failure. **The supplemental evidence has increased, not reduced, the weight of the argument that this domain should not be released with Tier 0 suppressed.** Register R6.

**XD-T0-2** — Where Tier 0 is suppressed, findings are **withheld with an explicit, auditable statement, never demoted** (contract §17, §18.19).

---

## 13. Cross-domain lead selection

**XD-LEAD-1 `[E]`** — Order by the common urgency time band. Only comparison surface.

**XD-LEAD-2 `[E]`** — Severity orders only within a domain. Cross-domain severity comparison prohibited.

**XD-LEAD-3 `[E]`** — Same-day findings that cannot be distinguished by a governed rule form **one co-equal group with no internal ordering**. The co-lead cap does not apply (contract §7.4).

**XD-LEAD-4 — REMOVED.** The three proposed universal distinguishers (organ dysfunction over marker abnormality; irreversible over reversible harm; direct over derived measurement) are **not ratified** and are withdrawn from this ruleset. HMR position: clinically plausible but not sufficiently bounded across all domains.

**Consequence:** equal-time-band cross-domain findings resolve as co-leads, or at same day as one co-equal group. This is the correct residual behaviour and no gap is created.

---

## 14. Unresolved-decision register

| ID | Decision | Owner | Blocking |
|---|---|---|---|
| A4 | Na⁺ 146–154 band placement | HMR | Yes |
| A5 | Severe-anaemia same-day threshold | HMR (adjudication — no citation exists) | Yes |
| A6 | Subclinical hyperthyroidism bands | HMR | No |
| A8 | Vitamin D — adopt or exclude | HMR | Yes |
| A9 | Bilirubin urgent threshold | HMR (adjudication) | Yes |
| A10 | CRP marked-elevation route | HMR | No (quarantined) |
| B1 | Hepatic Tier 1 floor | HMR + Anthony | Yes |
| B2 | Potassium urgent threshold | HMR (adjudication) | Yes |
| B3 | Pregnancy policy adoption | HMR + Anthony + Reg | Yes |
| B4 | Unsafe-without-context registers per domain | HMR | Yes |
| B5 | Sex and ancestry handling | HMR + Anthony | Yes |
| B6 | Baseline-validity framework | HMR | No (labelled interim) |
| B7 | Endocrine scope | HMR | No (limitation stated) |
| P1–P8 | Product decisions | **Anthony** | P2, P7 yes |
| R1–R6 | Regulatory/legal | **Reg/legal** | R1, R5, R6 yes |
| XD-CONF-1 | Hepatic ruleset relabel to v0.6 | Documentation | No |

---

## 15. Acceptance-test matrix

| # | Panel | Expected | Tests |
|---|---|---|---|
| XD-AS-1 | K⁺ 6.8; ALT 300 (6.1× ULN) | Same-day co-equal group; no ordering; potassium carries artefact wording | §13; P1 |
| XD-AS-2 | Platelets 45; ALT 200 | Two findings; haematology primary below the 50 boundary | XD-C2 |
| XD-AS-3 | Platelets 120; ALT 200; AST 260 | One hepatic fibrosis finding, platelets consolidated | XD-C1 |
| XD-AS-4 | Ferritin 420; TSAT 58%; ALT 90 | Two findings; hepatic does not absorb | XD-C9 |
| XD-AS-5 | Ferritin 1400; TSAT 22%; ALT 90 | One finding plus context; magnitude does not promote | XD-C8 |
| XD-AS-6 | TSH 14, free T4 unavailable; LDL 5.9 | Thyroid indeterminate **and** thyroid as lipid secondary cause — one fact, two presentations | XD-DUAL-1 |
| XD-AS-7 | TG 24; Na⁺ 128 | Both same-day; sodium carries pseudohyponatraemia caveat; neither suppressed | XD-ARTEFACT-1 |
| XD-AS-8 | B12 110; Hb 82; platelets 88; ANC 1.1 | One pancytopenia finding, same day, B12 as aetiology | XD-C5 |
| XD-AS-9 | Calcium 2.85, albumin absent; K⁺ 6.7 | Potassium same-day; calcium **insufficient data**, alongside, not leading | Contract §8.1, §16.2 |
| XD-AS-10 | eGFR 38 (no baseline); MCV 104; CRP 9; TSH 5.8 | Renal Tier 1 (AKI not assessable); three Tier 2 findings compressed. No hepatic-style floor on MCV or CRP | P2; prohibited universalisation |
| XD-AS-11 | Entirely normal broad panel | Six domain-specific "does not exclude" statements; **one** panel-level pregnancy-assumption statement | U12; XD-PREG-2 |
| XD-AS-12 | K⁺ 6.8; platelets 18; TG 24 | Three-member same-day group | P1 |
| **XD-AS-13** | **K⁺ 2.3, no symptoms** | **Same day.** No mild-consequence language. States severity depends on symptoms and ECG, not assessed | UWC-3; XD-ELEC-2 |
| **XD-AS-14** | **Adjusted Ca²⁺ 2.05, no symptoms** | Within weeks band — **and** mandatory statement that any level below range is an emergency if symptomatic, with symptoms listed | UWC-4; XD-ELEC-3 |
| **XD-AS-15** | **Na⁺ 152, otherwise normal** | Within days (pending A4). States hypernatraemia usually reflects fluid balance or water access | XD-ELEC-4 |
| **XD-AS-16** | **Calcium 1.75 uncorrected, albumin absent** | **Insufficient data.** No hypocalcaemia finding created despite a value below any threshold. Tests that §8.1 holds even at emergency-range values | Contract §8.1 |
| **XD-AS-17** | **TC 8.9, non-HDL 7.2, full risk-factor set available** | Lipid finding at its NICE threshold. **No risk percentage computed or displayed** | §10 quarantine |
| **XD-AS-18** | **ALT 90, AST 130, platelets 135, age 61** | Fibrosis finding via AST:ALT >1 and platelets. **FIB-4 not computed** | §10 quarantine |
| **XD-AS-19** | **Pregnancy known; ALT 180, TSH 6.2** | Both domains produce explicit out-of-scope, specialist-rules-required outputs. **Visible, not suppressed** | Contract §26.2 |
| **XD-AS-20** | **Hb 108, sex unknown** | Indeterminate under §4.9; assumption stated; **no silent default to the female threshold** | B5; UWC-11 |
| **XD-AS-21** | **K⁺ 3.2, Mg not measured** | Within weeks; magnesium requested as companion. **Not** an insufficient-data output — the finding is interpretable without it | XD-C14 |

---

## 16. Sign-off

| Field | Value |
|---|---|
| Version | 0.2 |
| Contract | v0.6 |
| v0.5 conformance check completed | ☐ |
| Electrolyte bands incorporated | ☐ |
| Quarantined thresholds confirmed (§5) | ☐ |
| Pregnancy policy adopted (§6) | ☐ |
| Unsafe-without-context register accepted (§7) | ☐ |
| 23 Tier 0 rules confirmed specification-only | ☐ |
| CV risk and FIB-4 quarantine confirmed | ☐ |
| Lead distinguishers confirmed removed | ☐ |
| Unresolved-decision register accepted (§14) | ☐ |
| HMR signature / date | ☐ |

---

## VERDICT: REQUIRES_CROSS_DOMAIN_ADJUDICATION

Retained from v0.1, for a materially smaller reason. The three electrolyte research gaps that drove the v0.1 verdict are **closed**. What remains is adjudication, not research: eleven blocking decisions across HMR, product and regulatory, itemised in §14.

The model itself is not in question. Contract v0.5 conformance is complete with no non-conformance found; the universal rule set held across all six domains; the shared-marker register resolves every boundary; and the unratified lead distinguishers have been removed without creating a gap.
