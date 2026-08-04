---
document_id: HEALTHIQ-CROSS-DOMAIN-RULESET-001
title: HealthIQ Cross-Domain Clinical Prioritisation Ruleset
version: "0.4"
supersedes: "0.3"
governing_contract: HEALTHIQ-CLIN-PRIORITY-CONTRACT-001 v0.6.2
incorporates:
  - HEALTHIQ-CROSS-DOMAIN-HMR-ADJUDICATION-REGISTER-001 v0.3
  - HEALTHIQ-ELECTROLYTE-SUPPLEMENTAL-EVIDENCE-001 v0.1
  - HEALTHIQ-UPLOAD-QUESTIONNAIRE-CONTEXT-AUDIT-001 v0.1
hmr_disposition: CLINICALLY_RATIFIED_SUBJECT_TO_TARGETED_DOCUMENT_CORRECTION
status: DRAFT_FOR_FINAL_INDEPENDENT_CONSISTENCY_REVIEW
implementation_status: NOT_AUTHORISED
---

# Cross-Domain Clinical Prioritisation Ruleset v0.4

**Evidence labels:** `[E]` · `[C]` · `[J]` · `[U]`.

---

## 0. Changes from v0.3

| # | Change |
|---|---|
| 1 | **B1 closed** — literal hepatic Tier 1 floor incorporated (§2) |
| 2 | **A8 closed** — narrow vitamin D rule authorised; **removed from quarantine** (§9) |
| 3 | Open clinical-item register now **empty** (§11) |
| 4 | Questionnaire audit references corrected — the audit is **complete** and its findings are recorded (§4.2) |
| 5 | Product-status wording corrected — "fully unblocked" removed (§11.1) |
| 6 | Acceptance-test matrix updated with five new scenarios (§13) |
| 7 | **Tier 0 count unchanged at 18** — neither authorised change alters Tier 0 |

---

## 1. Tier 0 register — 18 fully specified rules

**Unchanged by this revision.** The hepatic Tier 1 floor operates at Tier 1 and the vitamin D rule at Tier 2; neither touches Tier 0.

| # | Domain | Rule |
|---|---|---|
| 1 | Haematology | Platelets <20 × 10⁹/L (new) |
| 2 | Haematology | Platelets <150 × 10⁹/L with new thrombosis or renal impairment |
| 3 | Haematology | Absolute neutrophil count <0.5 × 10⁹/L |
| 4 | Haematology | Pancytopenia (three-lineage cytopenia) |
| 5 | Hepatic | ALT or AST ≥10× ULN |
| 6 | Hepatic | ALT or AST >1000 U/L |
| 7 | Hepatic | Hy's law pattern — ALT/AST ≥3× ULN **and** bilirubin ≥2× ULN **and** ALP <2× ULN |
| 8 | Hepatic | Any abnormal hepatic analyte **and** albumin below lower reference limit |
| 9 | Hepatic | Any abnormal hepatic analyte **and** INR >1.5 without anticoagulation |
| 10 | Renal/electrolyte | K⁺ **>6.0 mmol/L** |
| 11 | Renal/electrolyte | K⁺ <2.5 mmol/L |
| 12 | Renal/electrolyte | Na⁺ <125 mmol/L |
| 13 | Renal/electrolyte | Na⁺ ≥155 mmol/L |
| 14 | Renal/electrolyte | Adjusted Ca²⁺ >3.0 mmol/L |
| 15 | Renal/electrolyte | Adjusted Ca²⁺ <1.9 mmol/L |
| 16 | Renal/electrolyte | NICE NG148 AKI criteria met |
| 17 | Renal/electrolyte | eGFR <15 mL/min/1.73m² |
| 18 | Cardiometabolic | Triglycerides >20 mmol/L |

| Domain | Count | Release status without contract §17 |
|---|---|---|
| Haematology | 4 | Tier 0 blocked; Tier 1 and below releasable |
| Hepatic | 5 | Tier 0 blocked; Tier 1 and below releasable |
| Renal/electrolyte | **8** | See §1.1 |
| Iron/inflammatory | **0** | **Fully releasable** |
| Thyroid/endocrine | **0** | **Fully releasable** |
| Cardiometabolic/nutritional | 1 | That rule blocked; rest releasable |
| **Total** | **18** | All specification-only |

**§1.1 — XD-T0-1, unchanged.** Renal/electrolyte holds 8 of 18, six concerning potentially life-threatening results. The B2 adjudication increased the weight of this item: lowering the same-day potassium threshold to >6.0 means HealthIQ identifies **more** people with a result it has no governed way to act on. Register **R6**.

**XD-T0-2** — Where Tier 0 is suppressed, findings are withheld with an explicit, auditable statement, **never demoted** (contract §17, §18.19).

---

## 2. Hepatic Tier 1 floor — literal BSG position

**XD-HEP-FLOOR-1 `[E]` — ratified, `CLINICALLY_ADJUDICATED`.**

Any out-of-range core hepatic analyte produces **one consolidated Tier 1 hepatic finding**, unless a more urgent governed hepatic rule applies.

Basis: BSG Recommendation 4 (grade B) — investigate with a liver aetiology screen irrespective of level and duration, where abnormal means outside the laboratory reference range `[E]`. BSG Recommendation 3 — the extent of abnormality is not necessarily a guide to clinical significance `[E]`.

**Required behaviour:**

1. The panel produces **one** consolidated hepatic concern.
2. All supporting hepatic abnormalities are **nested beneath it**.
3. Individual analytes do **not** become separate concern slots.
4. A minor abnormality is **not** described as urgent merely because it enters Tier 1.
5. The finding means the abnormal hepatic result **warrants discussion or investigation** — contract §6.3.
6. Abnormalities independently meeting Tier 0 or Tier 1 criteria **in another domain** may not be absorbed — contract §4.8.
7. The consolidated finding inherits the highest urgency band among its **present** constituents — contract §9.4.
8. Contextual attachments (MCV within the mild band, low transferrin, ferritin with TSAT ≤45%, vitamin D where relevant to a calcium finding) nest at Tier 3 and remain reconcilable with the raw value.

**XD-HEP-FLOOR-2 — non-export, unchanged.** The hepatic Tier 1 floor remains **hepatic-bound**. It is falsified in haematology (isolated mild macrocytosis, Tier 2 with reassurance available `[E]`) and in inflammatory markers (isolated mild CRP, Tier 2). Contract §18.23 prohibits its export. Ratifying the floor within hepatic does **not** authorise it anywhere else.

**XD-HEP-FLOOR-3.** Contract §15.2.1 records the presentation decision and is explicitly scoped to the hepatic domain. **No other domain may adopt hepatic-style consolidation on the strength of it.** Broader cross-domain Tier 1 presentation-density decisions remain open under contract §15.2 and register item P5.

**No magnitude-gated alternative is retained.** The hepatic Tier 1 floor is not described as unresolved anywhere in this package.

---

## 3. Fixed adjudications

| Rule | Position | Label |
|---|---|---|
| Hepatic Tier 1 floor | **Literal BSG.** One consolidated nested finding | `[E]` |
| Vitamin D | **<25 nmol/L → Tier 2 routine.** 25–50 no independent finding. >50 no concern. Contextual under calcium regardless | `[E]` |
| Potassium same day | **>6.0 mmol/L** — deliberate conservative HealthIQ adjudication, knowing departure from UKKA's ≥6.5 because UKKA assumes a clinical pathway with ECG that HealthIQ lacks | `[E]` bands, adjudicated threshold |
| Hypernatraemia 146–154 | **Within days** | **`[J]`** — must travel with the rule; may not be upgraded downstream |
| Severe anaemia | **No same-day rule authorised.** Caps at within days pending specialist haematology adjudication | Adjudicated decline |
| Bilirubin | **No standalone numeric total-bilirubin Tier 0 rule.** Hy's law retained | Adjudicated decline |
| CRP | Primarily contextual; promotion on persistence only | Adjudicated |
| Subclinical hyperthyroidism | Ungraded at within weeks; mirroring the hypothyroid ≥10 threshold prohibited | Adjudicated |
| Cardiovascular risk calculation | **Quarantined** pending R2 | Quarantined |
| FIB-4 | **Quarantined** pending R3 | Quarantined |

**XD-ADJ-2 — residual risk, retained.** A haemoglobin of 55 g/L will not reach same day in this version. Accepted consequence of declining to invent a threshold where WHO explicitly declines to establish one; first item for specialist haematology review.

---

## 4. Pregnancy and questionnaire context

### 4.1 Pregnancy policy — ratified

**XD-PREG-1.** `pregnant` and `may_be_pregnant` are treated **identically** for all clinical interpretation. No rule in any domain may distinguish between them.

**XD-PREG-2.** Where either status is declared, affected findings produce an explicit out-of-scope, specialist-rules-required output. The finding remains **visible as withheld**. Silent suppression is prohibited — contract §26.2.

**XD-PREG-3.** All six domains declare pregnancy as materially affecting their reference framework: haematology (dilutional anaemia thresholds, gestational thrombocytopenia) `[E]`; hepatic (ALP raised, albumin reduced) `[E]`; renal/electrolyte (eGFR raised, sodium) `[E]`; iron/inflammatory (ferritin, haemoglobin) `[C]`; thyroid (all patterns, trimester-specific ranges) `[E]`; cardiometabolic/nutritional (lipids rise physiologically, risk tools not validated) `[E]`. Because all six are affected, the unknown-status statement is a **single panel-level statement**.

### 4.2 Questionnaire context audit — complete, remediation deferred

`HEALTHIQ_UPLOAD_QUESTIONNAIRE_CONTEXT_AUDIT_v0.1.md` is **complete** and its findings are recorded in the merged governing register entry for the questionnaire rationalisation carry-forward.

**Audit position:**

- no pregnancy question currently exists in the canonical questionnaire;
- mandatory questionnaire data is enforced only in the frontend;
- the backend permits analysis without questionnaire data;
- missing sex can silently default;
- unanswered pregnancy status currently permits non-pregnant interpretation;
- regeneration can perpetuate incomplete questionnaire context;
- full questionnaire rationalisation and mandatory-context remediation is **deferred to a later dedicated sprint**;
- this remains a **hard dependency before release and before runtime reliance on questionnaire context**.

**XD-PREG-4.** Pregnancy status is a **mandatory** question in the target upload flow and a missing answer must **block** upload and analysis. **This enforcement is not implemented.** The defect is documented and deferred.

**XD-PREG-5.** No statement in this or any companion document describes the questionnaire requirement as implemented or the defect as fixed. Contract §26.3 governs the interim unknown-status case and is explicitly labelled a defensive fallback — it is not authority for operating without pregnancy status once enforcement exists.

**XD-CTX-1.** The audit finding that unanswered pregnancy status currently permits non-pregnant interpretation is the runtime counterpart of the XD-PREG-2 policy. Until remediation, the ratified policy and current runtime behaviour differ. This is recorded, not resolved, and is the reason the carry-forward is release-blocking.

---

## 5. Sex and ancestry

**XD-SEX-1 — ratified.** Biological sex required for laboratory interpretation is **already a mandatory question in the standard product flow** and is treated as **available by design**. Domain rules may assume it is present.

**XD-SEX-2 — defensive fallback only.** Fail-closed handling for malformed or legacy requests is retained. Where sex is genuinely absent, the affected finding is **indeterminate** under contract §4.9, the assumption is stated, and there is **no silent default**. This is a fallback, not a normal operating mode.

**XD-SEX-3.** The audit records that missing sex can currently silently default at runtime. That behaviour is **inconsistent with XD-SEX-2** and forms part of the deferred remediation. It is recorded here so the gap between ratified policy and current runtime is visible.

**XD-ANC-1 — prohibited.** Ancestry is **not** captured. **No ancestry-specific reference adjustment is authorised in any domain.** Where a source guideline specifies an ancestry-dependent threshold, the unadjusted threshold applies and the limitation is stated.

Accepted consequences: benign ethnic neutropenia is not adjusted for, so the standard neutrophil band will over-call neutropenia in people of African and some Middle Eastern ancestry; ancestry-related ferritin reference expectations are not applied. There is no conservative direction in which to adjust without governed data.

---

## 6. Universal rules — unchanged

U1–U16 carried forward from v0.2 without amendment: consolidated findings as the unit; urgency and severity separable; confidence affects explanation only; supporting-marker count, frame count and panel completeness have no role; frames consolidate before tiering; Tier 0/1-eligible findings may not be contextual; missing data reduces confidence not significance; two declared missing-modifier consequences; absent baseline is never stability; direction asymmetry is the norm; no universal trend downgrade; empty Tier 0 is legitimate; no-concern outputs require domain-specific non-exclusion statements; governed derivation obligation; not-assessable never not-met; anaemia never appears twice; domain conventions may not be exported without cross-domain validation.

---

## 7. Urgency time-band register

Contract §4.1 bands remain the **only** cross-domain comparison surface. Eight incommensurable severity methods are in play; no cross-domain severity comparison is possible or permitted — contract §18.24.

Same day: §1, 18 rules. Empty Tier 0: iron/inflammatory, thyroid/endocrine — both fully releasable without contract §17.

---

## 8. Shared-marker ownership and combinations — unchanged

| Marker | Owner | Boundary |
|---|---|---|
| Haemoglobin, MCV, platelets | **Haematology** | Platelets: 50 × 10⁹/L and any haematology same-day criterion. MCV: top of mild band, and any other FBC abnormality |
| Ferritin, TSAT | **Iron** | TSAT 45% |
| Albumin | **Domain-conditional — no single owner** | Hepatic synthetic function; renal calcium modifier; inflammatory negative acute-phase reactant — contract §9.6 |
| CRP | **Inflammatory** | Orphan status plus persistence |
| Potassium, sodium, calcium, creatinine/eGFR | **Renal/electrolyte** | Renal always primary for the renal finding |
| Thyroid pattern | **Thyroid** | Also lipid secondary cause and macrocytosis cause — one fact, two presentations |
| B12, folate | **Nutritional** | Haematology owns the count bands |
| **Vitamin D** | **Nutritional** | **Contextual to hypocalcaemia; renal/electrolyte owns the calcium finding** |
| HbA1c | **Cardiometabolic** | Dual role within the domain |

Cross-domain combination register XD-C1 to XD-C14 carried forward unchanged. Every consolidation preserves the highest urgency band; none absorbs a constituent independently meeting Tier 0/1 — contract §9.5.

**XD-ARTEFACT-1 `[E]`** retained: where TG >20 mmol/L coexists with hyponatraemia, the sodium finding carries a mandatory pseudohyponatraemia caveat and confirmation advice; neither finding is suppressed.

**XD-C15 — new.** Vitamin D below the deficiency threshold **with** hypocalcaemia: vitamin D nests as context beneath the calcium finding (§9.2). It does not form a competing concern.

---

## 9. Vitamin D — authorised rule

### 9.1 The rule

**XD-VITD-1 `[E]` — `CLINICALLY_ADJUDICATED`. Removed from quarantine.**

Serum 25-hydroxyvitamin D:

| Concentration | Disposition |
|---|---|
| **<25 nmol/L** | **Vitamin D deficiency finding · Tier 2 · routine** |
| **25–50 nmol/L** | **No independent clinical finding in this version.** May be used as contextual information where clinically relevant |
| **>50 nmol/L** | No vitamin D concern |

**Source.** The governed UK source recorded in the HMR A8 decision. The threshold corresponds to the SACN 2016 definition of vitamin D deficiency at <25 nmol/L, carried into NICE guidance, with 25–50 nmol/L classified as insufficiency `[E]`.

### 9.2 Contextual role under calcium

**XD-VITD-2 `[E]`.** Where vitamin D contributes to a hypocalcaemia interpretation, it appears as **context beneath the calcium finding**, regardless of whether it independently meets the <25 nmol/L rule. This reflects `CA-LOW-C5` — vitamin D deficiency is a common contributor to hypocalcaemia.

Where vitamin D is <25 nmol/L **and** hypocalcaemia is present, the vitamin D finding does **not** additionally occupy a separate Tier 2 slot; it nests as the aetiological context for the calcium concern (XD-C15).

### 9.3 Constraints — binding

- **No supplementation dose is authorised.**
- **No higher "optimal" threshold is authorised.** The 25–50 nmol/L insufficiency band generates no finding in this version.
- **No Tier 1 vitamin D finding from concentration alone.**
- **Pregnancy-specific interpretation remains outside scope** — contract §26.
- **No additional insufficiency bands, treatment rules or symptom-based escalation** may be introduced.

---

## 10. Quarantined capabilities

| Item | Status | Register |
|---|---|---|
| **Individual cardiovascular risk calculation** | **QUARANTINED** pending regulatory approval. May not be computed or displayed. Named NICE referral thresholds remain permitted — they are thresholds, not risk calculations | R2 |
| **FIB-4** | **QUARANTINED** pending regulatory approval. Hepatic fibrosis findings run on AST:ALT ratio and platelets, which are direct observations | R3 |
| Tier 0 action-and-timeframe guidance | **All 18 rules specification-only** pending contract §17 | R1 |
| Disease naming | Pending P4/R4 | — |
| CRP marked-elevation route | **WITHDRAWN.** Promotion on persistence only | A10 |
| Subclinical hyperthyroidism bands | **Absent by decision** | A6 |
| Anaemia severity sub-bands | **Absent by decision** | A5 |
| Baseline-validity windows | Interim, explicitly labelled adjudicated. AKI windows (48h, 7d) remain `[E]` | B6 |

**Vitamin D is no longer quarantined** — see §9.

**XD-QUAR-1.** Quarantine removes the calculation, not the finding. A raised cholesterol still produces a finding; a computed risk percentage is withheld.

---

## 11. Unresolved-decision register

### 11.1 Clinical — empty

**No clinical adjudication from this package remains open.** B1 and A8 were the last two entries; both are closed.

### 11.2 Product

**No remaining product decision blocks clinical ruleset ratification. P1, P3, P4, P5 and P6 remain open as non-blocking presentation, communication or release decisions.**

| ID | Decision | Status | Blocking |
|---|---|---|---|
| P1 | Same-day co-equal group presentation, including at three or more members | `OPEN` | No |
| P3 | Dual-role presentation | `OPEN` | No |
| P4 | Disease-name communication policy | `OPEN` | No |
| P5 | No-concern limitation presentation; broader cross-domain Tier 1 presentation density | `OPEN` | No |
| P6 | Release sequencing for domains with and without Tier 0 | `OPEN` | No |

### 11.3 Regulatory and legal — all open

| ID | Decision | Blocking |
|---|---|---|
| **R1** | Tier 0 action guidance — 18 rules | **Yes for Tier 0 release** |
| R2 | Cardiovascular risk calculation | Yes, that capability |
| R3 | FIB-4 | Yes, that capability |
| R4 | Consumer disease-name outputs | Yes |
| **R5** | Population exclusions and intended-purpose wording | **Yes** |
| **R6** | Renal/electrolyte release with Tier 0 suppressed | **Yes** |

### 11.4 Implementation

| Item | Status | Blocking |
|---|---|---|
| Questionnaire rationalisation carry-forward | `DEFERRED` | **Release and runtime reliance on questionnaire context — not the clinical ruleset** |
| Hepatic ruleset relabel to v0.6.2 | Documentation | No |

---

## 12. Scope limitations

**XD-SCOPE-1** — **Thyroid-only coverage does not constitute endocrine coverage.** Cortisol, PTH, sex hormones and IGF-1 have no rules. Extension is new authoring, not revision.

**XD-SCOPE-2** — Excluded populations: paediatric and neonatal; **pregnancy** (contract §26); dialysis and transplant recipients; post-chemotherapy and post-transplant counts.

**XD-SCOPE-3** — Structurally unavailable data: blood film; ACR (CKD staging incomplete by construction); urine output (one AKI criterion unavailable); urine electrolytes; blood gases; symptoms and examination; **ancestry**.

**XD-SCOPE-4** — Coagulation is not covered and no rules exist.

**XD-SCOPE-5 — new.** Vitamin D coverage is limited to the deficiency threshold in §9. No insufficiency finding, no supplementation guidance, no pregnancy-specific interpretation.

---

## 13. Acceptance-test matrix

| # | Panel | Expected | Tests |
|---|---|---|---|
| XD-AS-1 | K⁺ 6.8; ALT 300 (6.1× ULN) | Same-day co-equal group; no ordering; potassium carries artefact wording | §7; P1 |
| XD-AS-1b | K⁺ 6.2, otherwise normal | **Same day.** Would have been within days under the old ≥6.5 rule | B2 |
| XD-AS-2 | Platelets 45; ALT 200 | Two findings; haematology primary below the 50 boundary. **Platelets may not be nested under the hepatic finding** | XD-HEP-FLOOR-1 point 6 |
| XD-AS-3 | Platelets 120; ALT 200; AST 260 | One hepatic finding, platelets nested as a fibrosis constituent | XD-C1 |
| XD-AS-4 | Ferritin 420; TSAT 58%; ALT 90 | Two findings; hepatic does not absorb the iron overload concern | XD-C9 |
| XD-AS-5 | Ferritin 1400; TSAT 22%; ALT 90 | One hepatic finding with ferritin nested as context | XD-C8 |
| XD-AS-6 | TSH 14, free T4 unavailable; LDL 5.9 | Thyroid indeterminate **and** thyroid as lipid secondary cause — one fact, two presentations | XD-DUAL-1 |
| XD-AS-7 | TG 24; Na⁺ 128 | Both same-day; sodium carries pseudohyponatraemia caveat; neither suppressed | XD-ARTEFACT-1 |
| XD-AS-8 | B12 110; Hb 82; platelets 88; ANC 1.1 | One pancytopenia finding, same day, B12 as aetiology | XD-C5 |
| XD-AS-9 | Calcium 2.85, albumin absent; K⁺ 6.7 | Potassium same-day; calcium **insufficient data**, alongside, not leading | Contract §8.1, §16.2 |
| XD-AS-10 | eGFR 38 (no baseline); MCV 104; CRP 9; TSH 5.8 | Renal Tier 1 (AKI not assessable); three Tier 2 findings compressed. **No hepatic-style floor applied to MCV or CRP** | XD-HEP-FLOOR-2 |
| XD-AS-11 | Entirely normal broad panel | Six domain-specific non-exclusion statements | U12 |
| XD-AS-12 | K⁺ 6.8; platelets 18; TG 24 | Three-member same-day group | P1 |
| XD-AS-13 | K⁺ 2.3, no symptoms | Same day. **No mild-consequence language**; states severity depends on symptoms and ECG | UWC-3 |
| XD-AS-14 | Adjusted Ca²⁺ 2.05, no symptoms | Within weeks — **and** mandatory statement that any level below range is an emergency if symptomatic | UWC-4 |
| XD-AS-15 | Na⁺ 152, otherwise normal | **Within days `[J]`.** Label visible in provenance | A4 |
| XD-AS-16 | Calcium 1.75 uncorrected, albumin absent | **Insufficient data. No finding created**, despite being below any emergency threshold | Contract §8.1 |
| XD-AS-17 | TC 8.9, non-HDL 7.2, full risk-factor set available | Lipid finding at its NICE threshold. **No risk percentage computed or displayed** | R2 quarantine |
| XD-AS-18 | ALT 90, AST 130, platelets 135, age 61 | Fibrosis finding via AST:ALT >1 and platelets. **FIB-4 not computed** | R3 quarantine |
| XD-AS-19 | `may_be_pregnant` declared; ALT 180, TSH 6.2 | **Identical handling to `pregnant`.** Both domains produce explicit out-of-scope outputs. **Visible, not suppressed** | XD-PREG-1, XD-PREG-2 |
| XD-AS-20 | Hb 108, sex present (normal flow) | Anaemia assessed against the sex-specific threshold. **No indeterminate disposition** | XD-SEX-1 |
| XD-AS-20b | Hb 108, sex absent (malformed/legacy request) | Indeterminate under §4.9; assumption stated; **no silent default** | XD-SEX-2 |
| XD-AS-21 | K⁺ 3.2, Mg not measured | Within weeks; magnesium requested as companion. Not an insufficient-data output | XD-C14 |
| XD-AS-22 | Hb 52 g/L, otherwise normal FBC | **Within days — not same day.** Residual risk accepted and recorded | A5 |
| XD-AS-23 | Bilirubin 95 µmol/L, ALT normal, ALP normal, albumin normal | **No Tier 0 rule fires.** Finding stands at Tier 1 under the hepatic floor | A9; XD-HEP-FLOOR-1 |
| XD-AS-23b | ALT 200 (4.1× ULN), bilirubin 2.4× ULN, ALP 1.1× ULN | **Tier 0 — Hy's law fires.** Tests that A9 removed the standalone rule without disturbing the combination | A9 boundary |
| **XD-AS-24** | **ALT 58 U/L (ULN 49, 1.2×), all other hepatic analytes normal** | **One consolidated Tier 1 hepatic finding.** Warrants discussion or investigation. **Must not be described as urgent.** Tests the literal floor at its mildest | **XD-HEP-FLOOR-1 points 4, 5** |
| **XD-AS-25** | **ALT 250, ALP 210, GGT 180, bilirubin 32, albumin normal** | **One** hepatic concern with four nested constituents. **Not four concerns; not one concern with three suppressed** | **XD-HEP-FLOOR-1 points 1–3** |
| **XD-AS-26** | **Vitamin D 18 nmol/L, calcium normal, otherwise normal** | **Vitamin D deficiency finding · Tier 2 · routine.** No supplementation dose. No Tier 1 escalation | **XD-VITD-1** |
| **XD-AS-27** | **Vitamin D 38 nmol/L, otherwise normal** | **No independent vitamin D finding.** May appear as contextual information only where clinically relevant. **No insufficiency finding is created** | **XD-VITD-1** |
| **XD-AS-28** | **Vitamin D 18 nmol/L, adjusted Ca²⁺ 2.05** | Calcium finding leads at its own band; **vitamin D nested beneath it as aetiological context.** Does **not** additionally occupy a separate Tier 2 slot | **XD-VITD-2, XD-C15** |
| **XD-AS-29** | **Vitamin D 62 nmol/L, adjusted Ca²⁺ 2.05** | Calcium finding stands. Vitamin D **may still appear as context beneath it** despite not meeting the <25 nmol/L rule | **XD-VITD-2** |

---

## 14. Version consistency

| Document | Version |
|---|---|
| Contract | **v0.6.2** |
| Cross-domain ruleset | **v0.4** (this document) |
| Adjudication register | **v0.3** |
| Closure report | **v0.3** |
| Tier 0 count | **18** |
| B1 | `CLINICALLY_ADJUDICATED` — closed |
| A8 | `CLINICALLY_ADJUDICATED` — closed; vitamin D out of quarantine |

---

## 15. Sign-off

| Field | Value |
|---|---|
| Version | 0.4 |
| Contract | v0.6.2 |
| Tier 0 count confirmed at 18, unchanged by this revision | ☐ |
| Literal hepatic Tier 1 floor incorporated; no magnitude-gated alternative retained | ☐ |
| Hepatic floor confirmed non-exportable | ☐ |
| Vitamin D rule and all five constraints confirmed | ☐ |
| Vitamin D removed from quarantine | ☐ |
| Open clinical-item register confirmed empty | ☐ |
| P1, P3, P4, P5, P6 confirmed open and non-blocking | ☐ |
| Questionnaire audit referenced accurately; defect **not** described as fixed | ☐ |
| Regulatory items confirmed open | ☐ |
| HMR signature / date | ☐ |

---

## VERDICT: READY_FOR_FINAL_INDEPENDENT_CONSISTENCY_REVIEW

No clinical adjudication from this package remains open. The Tier 0 register is unchanged at 18, both authorised changes operate below Tier 0, and every capability that would be unsafe to release remains quarantined or specification-only.

No remaining product decision blocks clinical ruleset ratification. Six regulatory and legal items remain open and cannot be closed by clinical or product authority, with **R6** the most consequential. The questionnaire rationalisation carry-forward remains deferred and release-blocking.
