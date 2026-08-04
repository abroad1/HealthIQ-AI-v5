---
document_id: HEALTHIQ-CROSS-DOMAIN-HMR-ADJUDICATION-REGISTER-001
title: HealthIQ Cross-Domain HMR Adjudication Register
version: "0.2"
supersedes: "0.1"
governing_contract: HEALTHIQ-CLIN-PRIORITY-CONTRACT-001 v0.6.1
status: ADJUDICATIONS_CLOSED_REGULATORY_OPEN
implementation_status: NOT_AUTHORISED
---

# Cross-Domain HMR Adjudication Register v0.2

## 0. Revision note and one missing input

**Missing governing input.** `HEALTHIQ_UPLOAD_QUESTIONNAIRE_CONTEXT_AUDIT_v0.1.md` was named as a governing input but was **not supplied**. The consequence is bounded and is stated wherever it applies: this register records **that** a questionnaire/runtime defect exists and is deferred, but does **not** characterise its specifics, because the audit has not been read. Every reference to the defect below is deliberately non-specific for that reason.

**Status vocabulary.** Every item now carries exactly one status:

| Status | Meaning |
|---|---|
| `CLINICALLY_ADJUDICATED` | Decided on clinical authority; recorded under contract §13 where no citation exists |
| `PRODUCT_RATIFIED` | Decided by product authority |
| `REG_LEGAL_PENDING` | Requires specialist review not available to this team |
| `DEFERRED_IMPLEMENTATION_DEPENDENCY` | Clinical and product position is settled; delivery is deferred and remains a hard dependency |
| `OPEN` | Not yet decided |

**Evidence labels:** `[E]` · `[C]` · `[J]` · `[U]`.

---

## 1. Items closed in this revision

### A4 — Hypernatraemia 146–154 mmol/L placement
**Status: `CLINICALLY_ADJUDICATED` — CLOSED**

**Decision:** `within days`, labelled `[J]`.

Adjudicated rather than evidence-derived. No UK national guideline bands this direction; the underlying band set is `[C]` grade and the placement within it is HealthIQ judgement. Rationale retained: hypernatraemia is rare in ambulatory primary care `[E]`, so its presence in an ambulatory adult implies impaired thirst, impaired water access or excessive free-water loss — the finding's significance derives from what it implies about the person rather than from the concentration.

**Recorded under contract §13 as a documented clinical adjudication.** The `[J]` label must travel with the rule wherever it appears and must not be upgraded to `[E]` or `[C]` in any downstream document.

Anthony: no · Reg/legal: no · Blocking: **no**

---

### A5 — Severe-anaemia same-day threshold
**Status: `CLINICALLY_ADJUDICATED` — CLOSED (declined)**

**Decision:** **No severe-anaemia same-day threshold is authorised in this version.** Anaemia caps at `within days` unless later specialist haematology adjudication establishes a same-day rule.

This is a decision to decline, not a deferral. WHO's 2024 guideline explicitly declines to establish an outcome-linked severity classification for individual clinical use, and importing an oncology grading scale would be an unlabelled cross-context import prohibited by contract §18.

**Consequences:**
- `HAEM-U-SD-5` is **removed**, not left as a placeholder. Contract §18 prohibits a finding with no governed severity or indeterminate disposition, and a Tier 0 rule with no threshold is exactly that.
- Haematology Tier 0 falls from 5 rules to **4**.
- The residual clinical risk is stated plainly: a haemoglobin of 55 g/L will not reach same day in this version. That is a known and accepted consequence of declining to invent a threshold, and it should be the first item put to specialist haematology when that review happens.

Anthony: no · Reg/legal: no · Blocking: **no**

---

### A9 — Bilirubin urgent threshold
**Status: `CLINICALLY_ADJUDICATED` — CLOSED (declined)**

**Decision:** **No standalone numeric total-bilirubin Tier 0 rule is authorised.** Only other governed hepatic Tier 0 combinations are retained.

**Scope of the decision — stated precisely, because the boundary matters:**

| Rule | Fate | Reason |
|---|---|---|
| `HEP-U0-6` — new conjugated hyperbilirubinaemia at jaundice-range levels with abnormal enzymes | **REMOVED** | It depended on a HealthIQ-invented numeric bilirubin threshold. UK guidance frames the trigger as *clinical* jaundice, which HealthIQ cannot observe |
| Hy's law pattern — ALT/AST ≥3× ULN **and** bilirubin ≥2× ULN **and** ALP <2× ULN | **RETAINED** | Bilirubin here is expressed as a multiple of the reporting laboratory's own ULN inside a governed combination, not as a HealthIQ-set numeric threshold. It is a combination rule, not a standalone bilirubin rule |

Bilirubin therefore remains an active constituent of a Tier 0 rule; what is declined is bilirubin **alone** triggering Tier 0 on a number HealthIQ would have had to invent.

**Consequence:** hepatic Tier 0 falls from 6 rules to **5**.

Anthony: no · Reg/legal: no · Blocking: **no**

---

### B2 — Potassium urgent threshold
**Status: `CLINICALLY_ADJUDICATED` — CLOSED**

**Decision:** **K⁺ >6.0 mmol/L is same day.** Recorded as a deliberate conservative HealthIQ adjudication.

This is a knowing departure from the UK Kidney Association's ≥6.5 severe threshold, in favour of the CCS/KDIGO >6.0 urgent-treatment threshold. The reason must travel with the rule: **UKKA's threshold assumes a clinical pathway that can assess a person at 6.0–6.4. HealthIQ has no clinician in the loop and no ECG.** UKKA itself recommends ECG and cardiac monitoring at ≥6.0, which is the capability HealthIQ lacks.

**Recorded under contract §13 as a documented adjudication with a stated reason.** It must not be presented in any downstream document as the UK national threshold.

The mandatory artefact-safe wording (RE-A-WORD-1) continues to apply: the finding stays, the urgency stays, and the language directs urgent repeat and clinical contact without asserting either that the result is genuine or that it is artefact.

Anthony: no · Reg/legal: no · Blocking: **no**

---

### P2 — Tier 1 volume control
**Status: `PRODUCT_RATIFIED` — CLOSED**

**Decision:** **One consolidated hepatic finding, with supporting hepatic abnormalities nested beneath it.**

This closes the volume concern that made P2 blocking. The concern arose because adopting the hepatic Tier 1 floor literally (B1) places any out-of-range core hepatic analyte at Tier 1, and roughly 30% of UK liver test requests contain at least one out-of-range result `[E]`.

Nested presentation resolves it structurally rather than by compression: the panel yields **one** hepatic concern regardless of how many hepatic analytes are abnormal, which is also the clinically correct reading — contract §3.1 and hepatic `HEP-CONS-1` already required consolidation, and this ratifies the presentation that matches it.

**Constraints that continue to apply (contract §15.2):** nesting may not reorder findings, may not lower any tier, may not remove a finding, and may not conceal that nested abnormalities exist. A nested abnormality that independently meets Tier 0 or Tier 1 criteria in **another** domain may not be absorbed (contract §4.8) — the platelet-below-50 boundary is the reference case.

Anthony: **ratified** · Reg/legal: no · Blocking: **no**

---

### P7 — Pregnancy handling and user-facing wording
**Status: `PRODUCT_RATIFIED` (policy) + `DEFERRED_IMPLEMENTATION_DEPENDENCY` (enforcement)**

**Decisions ratified:**

1. Pregnancy status is a **mandatory** question in the upload flow.
2. `pregnant` and `may_be_pregnant` are treated **identically** for clinical interpretation. Both require pregnancy-sensitive handling. No rule may distinguish between them.
3. A missing answer must **block** upload and analysis.

**Not yet implemented.** The questionnaire and runtime enforcement of these decisions does not exist. A defect in the current questionnaire/runtime behaviour has been documented separately and is **deferred to a later full questionnaire rationalisation sprint**.

**This register does not describe the questionnaire requirement as implemented, and no downstream document may do so.** Contract §26.3 is retained as an interim defensive provision governing the unknown-status case until enforcement exists, and is explicitly labelled as such in v0.6.1.

**Bounded limitation:** the specifics of the current defect are not characterised here because `HEALTHIQ_UPLOAD_QUESTIONNAIRE_CONTEXT_AUDIT_v0.1.md` was not supplied to this team (§0).

Anthony: **ratified** · Reg/legal: **R5 remains open** — a declared population exclusion bears on intended-purpose wording · Blocking the clinical ruleset: **no**. Blocking release: **yes**, via the implementation dependency.

---

### P8 — Sex and ancestry capture
**Status: `PRODUCT_RATIFIED` — CLOSED**

**Decisions ratified:**

1. **Sex.** Biological sex required for laboratory interpretation is **already a mandatory question in the standard product flow**. It is treated as available by design. Domain rules may assume it is present.
2. **Defensive behaviour retained.** Fail-closed handling for malformed or legacy requests remains. Where sex is genuinely absent, the affected finding is indeterminate under contract §4.9 and the assumption is stated. **This is a fallback, not a normal operating mode**, and it may not be cited as authority for operating without sex.
3. **Ancestry.** Ancestry is **not** captured and **no ancestry-specific adjustment is authorised** in any domain.

**Consequences by domain:**

| Domain | Effect |
|---|---|
| Haematology | The WHO sex-specific anaemia thresholds (<130 g/L men, <120 g/L women) apply normally. The HMR-rejected silent default to the female threshold stays rejected; the fallback is indeterminate-plus-statement |
| Iron | Sex-specific TSAT/ferritin genotyping thresholds `[E]` apply normally |
| Haematology | **Benign ethnic neutropenia remains unadjusted.** The standard neutrophil band applies and the limitation is stated. This will over-call neutropenia in people of African and some Middle Eastern ancestry, and that is the accepted position — there is no conservative direction in which to adjust without governed data |
| Iron | Ancestry-related ferritin reference expectations remain unapplied, with the limitation stated |

Anthony: **ratified** · Reg/legal: no · Blocking: **no**

---

## 2. Items closed in v0.1 — carried forward unchanged

| ID | Decision | Status |
|---|---|---|
| A1 | Hypokalaemia bands 3.0–3.4 / 2.5–2.9 / <2.5; K⁺ <2.5 same day; no mild-consequence language | `CLINICALLY_ADJUDICATED` `[E]` |
| A2 | Hypernatraemia bands 146–150 / 151–155 / >155; Na⁺ ≥155 same day — **recorded as `[C]` grade** | `CLINICALLY_ADJUDICATED` `[C]` |
| A3 | Hypocalcaemia bands; adjusted Ca²⁺ <1.9 same day; mandatory symptom-conditional language | `CLINICALLY_ADJUDICATED` `[E]` |
| A6 | Subclinical hyperthyroidism **remains ungraded at `within weeks`**. Mirroring the hypothyroid ≥10 threshold remains prohibited — direction asymmetry | `CLINICALLY_ADJUDICATED` |
| A7 | Low-TSAT deficiency requirement withdrawn; deficiency runs on ferritin, TSAT is the overload discriminator only | `CLINICALLY_ADJUDICATED` `[E]` |
| A10 | **CRP remains primarily contextual.** Promotion on persistence only; the unthresholded marked-elevation route stays withdrawn | `CLINICALLY_ADJUDICATED` |
| B4 | Three-part unsafe-without-context test and per-domain registers | `CLINICALLY_ADJUDICATED` |
| B6 | Baseline-validity windows retained as interim, explicitly labelled adjudicated | `CLINICALLY_ADJUDICATED` |
| B7 | Thyroid-only scope; extension to other endocrine axes is new authoring, not revision | `CLINICALLY_ADJUDICATED` |

---

## 3. Items remaining open

### B1 — Hepatic Tier 1 floor
**Status: `OPEN`**

The clinical choice — adopt BSG Recommendation 4 literally, or a documented magnitude-gated departure — is not among the decisions ratified in this revision.

**However, P2's ratification has materially changed its stakes.** The volume objection to the literal reading was that a high Tier 1 hepatic rate would swamp the concern set. With one consolidated nested hepatic finding, the panel yields one hepatic concern regardless of how many analytes are abnormal. **The volume argument against the literal reading is substantially weakened.**

Recommendation unchanged: adopt literally. If the modified reading is chosen, the departure from a grade B recommendation must be documented in the override register and never adopted silently.

Anthony: no longer required (P2 closed the product dimension) · Reg/legal: no · **Blocking: yes**

### A8 — Vitamin D
**Status: `OPEN` — quarantined**

Remains quarantined unless a governed UK threshold is confirmed. The finding may not be issued in the interim; vitamin D is retained as contextual to hypocalcaemia only. Contract §18 prohibits issuing a finding with no governed severity disposition, which is why quarantine — not "create the finding ungraded" — is the correct interim state.

**Blocking: yes**, for that finding only.

### B3 — Pregnancy policy
**Status: policy `PRODUCT_RATIFIED` via P7; `REG_LEGAL_PENDING` for intended-purpose wording (R5)**

The clinical and product positions are settled. What remains is R5.

### B5 — Sex and ancestry handling
**Status: `PRODUCT_RATIFIED` via P8 — CLOSED**

---

## 4. Product items — remaining

| ID | Decision | Status | Blocking |
|---|---|---|---|
| P1 | Same-day co-equal group presentation, including at three or more members | `OPEN` | No |
| P3 | Dual-role presentation — one fact appearing as its own concern and as another domain's context | `OPEN` | No |
| P4 | Disease-name communication policy | `OPEN` — interacts with R4 | No |
| P5 | No-concern limitation presentation | `OPEN` | No |
| P6 | Release sequencing for domains with and without Tier 0 | `OPEN` | No |
| **P2, P7, P8** | | **CLOSED** | |

---

## 5. Regulatory and legal — all remain open

Unchanged. No item in this category has been closed and none may be closed by clinical or product authority.

| ID | Decision | Status | Blocking |
|---|---|---|---|
| **R1** | Tier 0 action-and-timeframe guidance — **18 fully specified rules** | `REG_LEGAL_PENDING` | **Yes for any Tier 0 release** |
| **R2** | Individual cardiovascular risk calculation — **quarantined** | `REG_LEGAL_PENDING` | **Yes for that capability** |
| **R3** | FIB-4 — **quarantined** | `REG_LEGAL_PENDING` | **Yes for that capability** |
| R4 | Consumer disease-name outputs | `REG_LEGAL_PENDING` | Yes |
| **R5** | Declared population exclusions and intended-purpose wording — now includes the ratified pregnancy exclusion | `REG_LEGAL_PENDING` | **Yes** |
| **R6** | Whether renal/electrolytes may be released with Tier 0 suppressed | `REG_LEGAL_PENDING` | **Yes** |

**R6 is unchanged by this revision and remains the package's most consequential open item.** The B2 adjudication has if anything increased its weight: lowering the potassium same-day threshold to >6.0 means HealthIQ will identify *more* people with a life-threatening result it has no governed way to act on.

---

## 6. Blocking summary

| Category | Blocking items |
|---|---|
| Clinical | **B1** (hepatic Tier 1 floor), **A8** (vitamin D, that finding only) |
| Product | **None** |
| Regulatory/legal | **R1, R5, R6**; plus R2 and R3 for their specific capabilities |
| Implementation dependency | **Questionnaire enforcement** — deferred to a later full questionnaire rationalisation sprint; blocks release, not the clinical ruleset |

**Closed since v0.1:** A4, A5, A9, B2, B5, P2, P7, P8.
**Product category is now fully unblocked.**

---

## 7. Sign-off

| Field | Value |
|---|---|
| Register version | 0.2 |
| Contract version | v0.6.1 |
| HMR name / registration | ☐ |
| A4 · A5 · A9 · B2 confirmed as documented adjudications under §13 | ☐ |
| A5 residual risk accepted (no same-day anaemia rule this version) | ☐ |
| A9 boundary confirmed — Hy's law retained, standalone bilirubin rule removed | ☐ |
| B2 departure reason recorded with the rule | ☐ |
| P2 · P7 · P8 recorded as product-ratified | ☐ |
| Questionnaire enforcement recorded as deferred and **not** implemented | ☐ |
| B1 remains open | ☐ |
| Regulatory items confirmed open | ☐ |
| Signature / date | ☐ |
