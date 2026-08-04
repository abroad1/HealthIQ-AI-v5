---
document_id: HEALTHIQ-CROSS-DOMAIN-RULESET-001
title: HealthIQ Cross-Domain Clinical Prioritisation Ruleset
version: "0.3"
supersedes: "0.2"
governing_contract: HEALTHIQ-CLIN-PRIORITY-CONTRACT-001 v0.6.1
incorporates:
  - HEALTHIQ-CROSS-DOMAIN-HMR-ADJUDICATION-REGISTER-001 v0.2
  - HEALTHIQ-ELECTROLYTE-SUPPLEMENTAL-EVIDENCE-001 v0.1
status: DRAFT_FOR_FINAL_INDEPENDENT_CONSISTENCY_REVIEW
implementation_status: NOT_AUTHORISED
---

# Cross-Domain Clinical Prioritisation Ruleset v0.3

**Evidence labels:** `[E]` · `[C]` · `[J]` · `[U]`.

**Missing input note.** `HEALTHIQ_UPLOAD_QUESTIONNAIRE_CONTEXT_AUDIT_v0.1.md` was named as a governing input but was not supplied. This document records **that** a questionnaire/runtime defect exists and is deferred; it does **not** characterise its specifics.

---

## 0. Changes from v0.2

| # | Change |
|---|---|
| 1 | Severe-anaemia Tier 0 placeholder **removed** (A5) |
| 2 | Standalone bilirubin Tier 0 placeholder **removed**; Hy's law retained (A9) |
| 3 | Potassium same-day threshold changed to **>6.0 mmol/L** (B2) |
| 4 | Hypernatraemia 146–154 retained at within days, `[J]` (A4) |
| 5 | Hepatic presentation: **one consolidated finding, supporting abnormalities nested** (P2) |
| 6 | Pregnancy and possible pregnancy treated identically; questionnaire enforcement recorded as **not implemented** (P7) |
| 7 | Sex available by design; missing-sex retained as defensive fallback only (P8) |
| 8 | Ancestry adjustment confirmed prohibited (P8) |
| 9 | Tier 0 register recounted — **18 fully specified rules** |
| 10 | Vitamin D, FIB-4 and cardiovascular risk remain quarantined |

---

## 1. Tier 0 register — one definitive enumerated count

**Counting rule.** Only **fully specified** rules are counted. A rule with an unauthorised or missing threshold is not a rule and is not counted; contract §18 prohibits carrying it as a placeholder.

### 1.1 The definitive enumeration — 18 rules

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

### 1.2 Count by domain

| Domain | Tier 0 rules | Release status without contract §17 |
|---|---|---|
| Haematology | 4 | Tier 0 blocked; Tier 1 and below releasable |
| Hepatic | 5 | Tier 0 blocked; Tier 1 and below releasable |
| Renal/electrolyte | **8** | See §1.4 |
| Iron/inflammatory | **0** | **Fully releasable** |
| Thyroid/endocrine | **0** | **Fully releasable** |
| Cardiometabolic/nutritional | 1 | That rule blocked; rest releasable |
| **Total** | **18** | All specification-only |

### 1.3 Reconciliation with previous counts

| Version | Count | Reason for change |
|---|---|---|
| v0.1 | 20 | Included three renal/electrolyte placeholders that had no bands |
| v0.2 | 23 | Electrolyte bands supplied; three placeholders became real rules |
| **v0.3** | **18** | Severe anaemia removed (A5); standalone bilirubin removed (A9); the v0.2 figure double-counted the three electrolyte rules that had already been counted as placeholders in v0.1 |

**XD-T0-COUNT-1.** The v0.2 figure of 23 was wrong. The three new electrolyte rules replaced three placeholders that had already been counted, so the correct v0.2 figure was 20, not 23. Removing two rules under A5 and A9 gives **18**. This is now the single definitive count and supersedes every earlier figure in the package.

### 1.4 XD-T0-1 — renal/electrolyte, unchanged and reinforced

Renal/electrolyte holds **8 of 18** Tier 0 rules, of which six concern potentially life-threatening results: severe hyperkalaemia, severe hypokalaemia, profound hyponatraemia, severe hypernatraemia, severe hypercalcaemia and severe hypocalcaemia — plus AKI and kidney failure.

**The B2 adjudication increases the weight of this item.** Lowering the same-day potassium threshold to >6.0 means HealthIQ identifies **more** people with a result it has no governed way to act on. Register **R6**.

**XD-T0-2** — Where Tier 0 is suppressed, findings are **withheld with an explicit, auditable statement, never demoted** (contract §17, §18.19).

---

## 2. Fixed adjudications now incorporated

| Rule | Position | Label |
|---|---|---|
| Potassium same day | **>6.0 mmol/L** — deliberate conservative HealthIQ adjudication, a knowing departure from UKKA's ≥6.5 because UKKA assumes a clinical pathway with ECG that HealthIQ lacks | `[E]` bands, adjudicated threshold |
| Hypernatraemia 146–154 | **Within days** | **`[J]`** — must travel with the rule and may not be upgraded downstream |
| Severe anaemia | **No same-day rule authorised.** Anaemia caps at within days pending specialist haematology adjudication | Adjudicated decline |
| Bilirubin | **No standalone numeric total-bilirubin Tier 0 rule.** Hy's law retained — bilirubin there is a multiple of the laboratory's own ULN inside a governed combination, not a HealthIQ-set number | Adjudicated decline |
| CRP | **Primarily contextual.** Promotion on persistence only | Adjudicated |
| Subclinical hyperthyroidism | **Ungraded at within weeks.** Mirroring the hypothyroid ≥10 threshold remains prohibited — direction asymmetry | Adjudicated |
| Vitamin D | **Quarantined** unless a governed UK threshold is confirmed | Quarantined |
| Cardiovascular risk calculation | **Quarantined** pending regulatory approval | Quarantined |
| FIB-4 | **Quarantined** pending regulatory approval | Quarantined |

**XD-ADJ-1.** Four of these are declines, and a decline is a decision, not a gap. Contract §18 prohibits carrying an unauthorised threshold as a placeholder, so each removed rule is removed rather than parked.

**XD-ADJ-2 — residual risk, stated plainly.** A haemoglobin of 55 g/L will not reach same day in this version. That is the accepted consequence of declining to invent a threshold where WHO explicitly declines to establish one, and it is the first item for specialist haematology review.

---

## 3. Hepatic presentation — nested consolidated finding

**XD-HEP-PRES-1 — product-ratified.** The hepatic domain produces **one consolidated finding**, with supporting hepatic abnormalities **nested beneath it**.

A panel with ALT 250, ALP 46, GGT raised and bilirubin raised yields **one** hepatic concern with four nested constituents — not four concerns, and not one concern with three findings suppressed.

**Constraints (contract §15.2, §4.8):**

1. Nesting may not reorder, may not lower any tier, may not remove a finding, and may not conceal that nested abnormalities exist.
2. A nested constituent that independently meets Tier 0 or Tier 1 criteria **in another domain** may not be absorbed. The platelet-below-50 boundary is the reference case: platelets <50 × 10⁹/L remain a haematology finding and may not be nested under a hepatic fibrosis finding.
3. The consolidated finding inherits the highest urgency band among its present constituents (contract §9.4).
4. Contextual attachments (MCV within the mild band, low transferrin, ferritin with TSAT ≤45%) nest at Tier 3 beneath the hepatic parent and remain reconcilable with the raw value.

**XD-HEP-PRES-2.** This closes the Tier 1 volume concern structurally rather than by compression, and it matches what contract §3.1 and hepatic `HEP-CONS-1` already required. It also weakens the volume argument against adopting the hepatic Tier 1 floor literally — see §11, B1.

---

## 4. Pregnancy — policy and dependency

### 4.1 Policy — ratified

**XD-PREG-1.** `pregnant` and `may_be_pregnant` are treated **identically** for all clinical interpretation. Both require pregnancy-sensitive handling. **No rule in any domain may distinguish between them.**

**XD-PREG-2.** Where either status is declared, affected findings produce an explicit out-of-scope, specialist-rules-required output. The finding remains **visible as withheld**. Silent suppression is prohibited (contract §26.2).

**XD-PREG-3.** All six domains have declared pregnancy as materially affecting their reference framework:

| Domain | Affected |
|---|---|
| Haematology | Anaemia thresholds (dilutional); platelet thresholds (gestational thrombocytopenia) `[E]` |
| Hepatic | ALP physiologically raised; albumin physiologically reduced `[E]` |
| Renal/electrolyte | eGFR physiologically raised; sodium `[E]` |
| Iron/inflammatory | Ferritin and haemoglobin in pregnancy `[C]` |
| Thyroid | All patterns — trimester-specific ranges `[E]` |
| Cardiometabolic/nutritional | Lipids rise physiologically; risk tools not validated `[E]` |

Because all six are affected, the unknown-status statement is a **single panel-level statement**, not six.

### 4.2 Dependency — not implemented

**XD-PREG-4.** Pregnancy status is a **mandatory** question in the target upload flow and a missing answer must **block** upload and analysis.

**This enforcement is not implemented.** A defect in current questionnaire/runtime behaviour has been documented separately and is **deferred to a later full questionnaire rationalisation sprint**. It remains a **hard dependency** for release.

**XD-PREG-5.** No statement in this document, or in any downstream document, may describe the questionnaire requirement as implemented. Contract §26.3 governs the interim unknown-status case and is explicitly labelled a defensive fallback in v0.6.1 — it is not authority for operating without pregnancy status once enforcement exists.

**XD-PREG-6.** The specifics of the current defect are not characterised here; the audit was not supplied to this team.

---

## 5. Sex and ancestry

**XD-SEX-1 — ratified.** Biological sex required for laboratory interpretation is **already a mandatory question in the standard product flow** and is treated as **available by design**. Domain rules may assume it is present.

**XD-SEX-2 — defensive fallback only.** Fail-closed handling for malformed or legacy requests is retained. Where sex is genuinely absent, the affected finding is **indeterminate** under contract §4.9, the assumption is stated, and there is **no silent default**. This is a fallback, not a normal operating mode, and may not be cited as authority for operating without sex.

**Affected rules:** WHO sex-specific anaemia thresholds (<130 g/L men, <120 g/L women) `[E]`; sex-specific TSAT/ferritin genotyping thresholds `[E]`.

**XD-ANC-1 — prohibited.** Ancestry is **not** captured. **No ancestry-specific reference adjustment is authorised in any domain.** Where a source guideline specifies an ancestry-dependent threshold, the unadjusted threshold applies and the limitation is stated.

**Accepted consequences, stated rather than hidden:**
- Benign ethnic neutropenia is not adjusted for. The standard neutrophil band will over-call neutropenia in people of African and some Middle Eastern ancestry.
- Ancestry-related ferritin reference expectations are not applied.

There is no conservative direction in which to adjust without governed data — adjusting risks under-calling in one group, not adjusting risks over-calling in another. The unadjusted position with a stated limitation is the defensible one.

---

## 6. Universal rules — unchanged

U1–U16 from v0.2 are carried forward without amendment. Summarised: consolidated findings as the unit; urgency and severity separable; confidence affects explanation only; supporting-marker count, frame count and panel completeness have no role; frames consolidate before tiering; Tier 0/1-eligible findings may not be contextual; missing data reduces confidence not significance; two declared missing-modifier consequences; absent baseline is never stability; direction asymmetry is the norm; no universal trend downgrade; empty Tier 0 is legitimate; no-concern outputs require domain-specific non-exclusion statements; governed derivation obligation; not-assessable never not-met; anaemia never appears twice; domain conventions may not be exported without cross-domain validation.

---

## 7. Urgency time-band register

Contract §4.1 bands remain the **only** cross-domain comparison surface. Eight incommensurable severity methods are in play; no cross-domain severity comparison is possible or permitted (contract §18.24).

Same day: §1.1, 18 rules.

Domains with an **empty Tier 0**: iron/inflammatory, thyroid/endocrine. Both are fully releasable without contract §17 (contract §6.2).

---

## 8. Shared-marker ownership — unchanged

| Marker | Owner | Boundary |
|---|---|---|
| Haemoglobin, MCV, platelets | **Haematology** | Platelets: 50 × 10⁹/L and any haematology same-day criterion. MCV: top of mild band, and any other FBC abnormality |
| Ferritin, TSAT | **Iron** | TSAT 45% |
| Albumin | **Domain-conditional — no single owner** | Hepatic synthetic function; renal calcium modifier; inflammatory negative acute-phase reactant (contract §9.6) |
| CRP | **Inflammatory** | Orphan status plus persistence |
| Potassium, sodium, calcium, creatinine/eGFR | **Renal/electrolyte** | Renal always primary for the renal finding |
| Thyroid pattern | **Thyroid** | Also appears as lipid secondary cause and macrocytosis cause — one fact, two presentations |
| B12, folate | **Nutritional** | Haematology owns the count bands |
| HbA1c | **Cardiometabolic** | Dual role within the domain |

Cross-domain combination register XD-C1 to XD-C14 carried forward unchanged from v0.2. Every consolidation preserves the highest urgency band; none absorbs a constituent independently meeting Tier 0/1 (contract §9.5).

**XD-ARTEFACT-1 `[E]`** retained: where TG >20 mmol/L coexists with hyponatraemia, the sodium finding carries a mandatory pseudohyponatraemia caveat and confirmation advice; neither finding is suppressed.

---

## 9. Quarantined capabilities and thresholds

| Item | Status | Register |
|---|---|---|
| **Individual cardiovascular risk calculation** | **QUARANTINED** pending regulatory approval. May not be computed or displayed. Named NICE referral thresholds remain permitted — they are thresholds, not risk calculations | R2 |
| **FIB-4** | **QUARANTINED** pending regulatory approval. Hepatic fibrosis findings run on AST:ALT ratio and platelets, which are direct observations | R3 |
| **Vitamin D** | **QUARANTINED** unless a governed UK threshold is confirmed. Retained as contextual to hypocalcaemia only. The finding may not be issued | A8 |
| Tier 0 action-and-timeframe guidance | **All 18 rules specification-only** pending contract §17 | R1 |
| Disease naming | Pending P4/R4 | — |
| CRP marked-elevation route | **WITHDRAWN.** Promotion on persistence only | A10 |
| Subclinical hyperthyroidism bands | **Absent by decision.** Mirroring the hypothyroid threshold prohibited | A6 |
| Anaemia severity sub-bands | **Absent by decision** | A5 |
| Baseline-validity windows | Interim, explicitly labelled adjudicated. AKI windows (48h, 7d) remain `[E]` | B6 |

**XD-QUAR-1.** Quarantine removes the **calculation or the grading**, not the finding. A raised cholesterol still produces a finding; a computed risk percentage is withheld. Vitamin D is the one exception — the finding itself is withheld, because contract §18 prohibits issuing a finding with no governed severity disposition.

---

## 10. Unsafe-without-context register

Twelve rules, per contract §27. Two entries revised in this version.

| ID | Rule | Missing context | Behaviour |
|---|---|---|---|
| UWC-1 | Any calcium finding | Albumin | Insufficient-data output |
| UWC-2 | AKI detection | Valid prior creatinine | AKI **not assessable** |
| UWC-3 | Hypokalaemia 3.0–3.4 | Cardiac status, digoxin | Band fires; **no mild-consequence language** |
| UWC-4 | Hypocalcaemia 1.9 to lower reference limit | Symptoms | Band fires; **must** state that any level below range is an emergency if symptomatic, with symptoms listed |
| UWC-5 | Thyroid patterns | Treatment status | State the result cannot be interpreted without it; do not assume untreated |
| UWC-6 | Hepatic INR >1.5 criterion | Anticoagulation status | Criterion fires; state anticoagulation not excluded |
| UWC-7 | All pregnancy-affected findings | Pregnancy status | Contract §26; **interim only** — enforcement pending |
| UWC-8 | Statin-doubling hepatic rule | Statin start date, pre-statin baseline | Criterion **not assessable** |
| UWC-9 | TG >20 urgent rule | Alcohol intake, glycaemic control | **Rule fires with the qualifier stated.** Must not be suppressed |
| UWC-10 | B12 with neurological features | Symptoms | Cannot fire on biochemistry alone; deficiency finding stands at its own band |
| **UWC-11** | **Sex-dependent thresholds** | Sex | **Revised.** Sex is available by design. This entry is now a **defensive fallback only** — indeterminate under §4.9, assumption stated, no silent default |
| **UWC-12** | **Neutrophil bands** | Ancestry | **Revised.** Ancestry is not captured and will not be. **No adjustment, ever.** State the limitation. This is a permanent declared limitation, not a pending gap |

**XD-UWC-1.** Everything not listed is deemed safe to run without context and must not be silently withheld (contract §27.3).

---

## 11. Unresolved-decision register

| ID | Decision | Owner | Status | Blocking |
|---|---|---|---|---|
| **B1** | Hepatic Tier 1 floor — literal BSG Rec 4 or documented departure | HMR | `OPEN` | **Yes** |
| **A8** | Vitamin D — confirm a governed UK threshold or formally exclude | HMR | `OPEN` | **Yes**, that finding only |
| P1 | Same-day co-equal group presentation | Anthony | `OPEN` | No |
| P3 | Dual-role presentation | Anthony | `OPEN` | No |
| P4 | Disease-name communication policy | Anthony | `OPEN` | No |
| P5 | No-concern limitation presentation | Anthony | `OPEN` | No |
| P6 | Release sequencing for domains with and without Tier 0 | Anthony | `OPEN` | No |
| **R1** | Tier 0 action guidance — 18 rules | Reg/legal | `PENDING` | **Yes for Tier 0 release** |
| R2 | Cardiovascular risk calculation | Reg/legal | `PENDING` | Yes, that capability |
| R3 | FIB-4 | Reg/legal | `PENDING` | Yes, that capability |
| R4 | Consumer disease-name outputs | Reg/legal | `PENDING` | Yes |
| **R5** | Population exclusions and intended-purpose wording — now includes the ratified pregnancy exclusion | Reg/legal | `PENDING` | **Yes** |
| **R6** | Renal/electrolyte release with Tier 0 suppressed | Reg/legal | `PENDING` | **Yes** |
| — | **Questionnaire enforcement** | Implementation | `DEFERRED` | **Yes for release**, not for the clinical ruleset |
| — | Hepatic ruleset relabel to v0.6.1 | Documentation | `OPEN` | No |

**Note on B1.** P2's ratification has weakened the volume argument against the literal reading: with one nested consolidated hepatic finding, the panel yields one hepatic concern regardless of how many analytes are abnormal. The product dimension of B1 is closed; only the clinical choice remains.

---

## 12. Scope limitations

**XD-SCOPE-1** — **Thyroid-only coverage does not constitute endocrine coverage.** Cortisol, PTH, sex hormones and IGF-1 have no rules. Extension is new authoring, not revision.

**XD-SCOPE-2** — Excluded populations: paediatric and neonatal; **pregnancy** (contract §26); dialysis and transplant recipients; post-chemotherapy and post-transplant counts.

**XD-SCOPE-3** — Structurally unavailable data: blood film; ACR (CKD staging incomplete by construction); urine output (one AKI criterion unavailable); urine electrolytes; blood gases; symptoms and examination; **ancestry**.

**XD-SCOPE-4** — Coagulation is not covered and no rules exist.

---

## 13. Acceptance-test matrix

| # | Panel | Expected | Tests |
|---|---|---|---|
| XD-AS-1 | K⁺ 6.8; ALT 300 (6.1× ULN) | Same-day co-equal group; no ordering; potassium carries artefact wording | §7; P1 |
| **XD-AS-1b** | **K⁺ 6.2, otherwise normal** | **Same day.** Tests the B2 threshold. Would have been within days under the old ≥6.5 rule | B2 |
| XD-AS-2 | Platelets 45; ALT 200 | Two findings; haematology primary below the 50 boundary. **Platelets may not be nested under the hepatic finding** | XD-HEP-PRES-1 constraint 2 |
| XD-AS-3 | Platelets 120; ALT 200; AST 260 | One hepatic finding, platelets nested as a fibrosis constituent | XD-C1; nesting |
| XD-AS-4 | Ferritin 420; TSAT 58%; ALT 90 | Two findings; hepatic does not absorb the iron overload concern | XD-C9 |
| XD-AS-5 | Ferritin 1400; TSAT 22%; ALT 90 | One hepatic finding with ferritin nested as context | XD-C8 |
| XD-AS-6 | TSH 14, free T4 unavailable; LDL 5.9 | Thyroid indeterminate **and** thyroid as lipid secondary cause — one fact, two presentations | XD-DUAL-1 |
| XD-AS-7 | TG 24; Na⁺ 128 | Both same-day; sodium carries pseudohyponatraemia caveat; neither suppressed | XD-ARTEFACT-1 |
| XD-AS-8 | B12 110; Hb 82; platelets 88; ANC 1.1 | One pancytopenia finding, same day, B12 as aetiology | XD-C5 |
| XD-AS-9 | Calcium 2.85, albumin absent; K⁺ 6.7 | Potassium same-day; calcium **insufficient data**, alongside, not leading | Contract §8.1, §16.2 |
| XD-AS-10 | eGFR 38 (no baseline); MCV 104; CRP 9; TSH 5.8 | Renal Tier 1 (AKI not assessable); three Tier 2 findings compressed. No hepatic-style floor on MCV or CRP | Prohibited universalisation |
| XD-AS-11 | Entirely normal broad panel | Six domain-specific non-exclusion statements | U12 |
| XD-AS-12 | K⁺ 6.8; platelets 18; TG 24 | Three-member same-day group | P1 |
| XD-AS-13 | K⁺ 2.3, no symptoms | Same day. **No mild-consequence language**; states severity depends on symptoms and ECG | UWC-3 |
| XD-AS-14 | Adjusted Ca²⁺ 2.05, no symptoms | Within weeks — **and** mandatory statement that any level below range is an emergency if symptomatic | UWC-4 |
| XD-AS-15 | Na⁺ 152, otherwise normal | **Within days `[J]`.** Label must be visible in provenance | A4 |
| XD-AS-16 | Calcium 1.75 uncorrected, albumin absent | **Insufficient data. No finding created**, despite being below any emergency threshold | Contract §8.1 |
| XD-AS-17 | TC 8.9, non-HDL 7.2, full risk-factor set available | Lipid finding at its NICE threshold. **No risk percentage computed or displayed** | R2 quarantine |
| XD-AS-18 | ALT 90, AST 130, platelets 135, age 61 | Fibrosis finding via AST:ALT >1 and platelets. **FIB-4 not computed** | R3 quarantine |
| **XD-AS-19** | **`may_be_pregnant` declared; ALT 180, TSH 6.2** | **Identical handling to `pregnant`.** Both domains produce explicit out-of-scope, specialist-rules-required outputs. **Visible, not suppressed** | XD-PREG-1, XD-PREG-2 |
| **XD-AS-20** | **Hb 108, sex present (normal flow)** | Anaemia assessed against the sex-specific threshold. **No indeterminate disposition** — sex is available by design | XD-SEX-1 |
| **XD-AS-20b** | **Hb 108, sex absent (malformed/legacy request)** | Indeterminate under §4.9; assumption stated; **no silent default**. Defensive fallback only | XD-SEX-2 |
| XD-AS-21 | K⁺ 3.2, Mg not measured | Within weeks; magnesium requested as companion. Not an insufficient-data output | XD-C14 |
| **XD-AS-22** | **Hb 52 g/L, otherwise normal FBC** | **Within days — not same day.** Tests A5. The residual risk is accepted and recorded | A5 |
| **XD-AS-23** | **Bilirubin 95 µmol/L, ALT normal, ALP normal, albumin normal** | **No Tier 0 rule fires.** No standalone bilirubin Tier 0 rule exists. Finding stands at its own band | A9 |
| **XD-AS-23b** | **ALT 200 (4.1× ULN), bilirubin 2.4× ULN, ALP 1.1× ULN** | **Tier 0 — Hy's law pattern fires.** Tests that A9 removed the standalone rule without disturbing the combination | A9 boundary |
| **XD-AS-24** | **Vitamin D 18 nmol/L, otherwise normal** | **No vitamin D finding issued.** Quarantined. Not a finding shown ungraded | A8 |
| **XD-AS-25** | **ALT 250, ALP 210, GGT 180, bilirubin 32, albumin normal** | **One** hepatic concern with four nested constituents. Not four concerns; not one concern with three suppressed | XD-HEP-PRES-1 |

---

## 14. Sign-off

| Field | Value |
|---|---|
| Version | 0.3 |
| Contract | v0.6.1 |
| Tier 0 count confirmed at 18, enumerated | ☐ |
| Severe-anaemia placeholder confirmed removed | ☐ |
| Standalone bilirubin placeholder confirmed removed; Hy's law retained | ☐ |
| K⁺ >6.0 same-day threshold confirmed with departure reason attached | ☐ |
| Na⁺ 146–154 `[J]` label confirmed | ☐ |
| Nested hepatic presentation confirmed | ☐ |
| Pregnancy identical-treatment rule confirmed | ☐ |
| Questionnaire enforcement recorded as **not implemented** | ☐ |
| Sex-missing confirmed as defensive fallback only | ☐ |
| Ancestry non-adjustment confirmed as permanent | ☐ |
| Vitamin D, FIB-4, CV risk quarantine confirmed | ☐ |
| HMR signature / date | ☐ |

---

## VERDICT: REQUIRES_CROSS_DOMAIN_ADJUDICATION

Two clinical items remain open — **B1** (hepatic Tier 1 floor) and **A8** (vitamin D). Both are named, bounded and adjudicable; neither requires research.

The product category is now fully unblocked. Six regulatory and legal items remain pending and cannot be closed by clinical or product authority, with **R6** the most consequential and, after the B2 adjudication, more consequential than it was.
