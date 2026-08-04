---
document_id: HEALTHIQ-CROSS-DOMAIN-HMR-ADJUDICATION-REGISTER-001
title: HealthIQ Cross-Domain HMR Adjudication Register
version: "0.3"
supersedes: "0.2"
governing_contract: HEALTHIQ-CLIN-PRIORITY-CONTRACT-001 v0.6.2
companion_documents:
  - HEALTHIQ-CROSS-DOMAIN-RULESET-001 v0.4
  - HEALTHIQ-SIX-DOMAIN-CLOSURE-REPORT-001 v0.3
hmr_disposition: CLINICALLY_RATIFIED_SUBJECT_TO_TARGETED_DOCUMENT_CORRECTION
status: ALL_CLINICAL_ADJUDICATIONS_CLOSED
implementation_status: NOT_AUTHORISED
---

# Cross-Domain HMR Adjudication Register v0.3

**Status vocabulary:** `CLINICALLY_ADJUDICATED` · `PRODUCT_RATIFIED` · `REG_LEGAL_PENDING` · `DEFERRED_IMPLEMENTATION_DEPENDENCY` · `OPEN`.

**Evidence labels:** `[E]` · `[C]` · `[J]` · `[U]`.

**No clinical adjudication from this package remains open.**

---

## 1. Items closed in this revision

### B1 — Hepatic Tier 1 floor
**Status: `CLINICALLY_ADJUDICATED` — CLOSED**

**Decision: adopt the BSG position literally.**

Any out-of-range core hepatic analyte produces **one consolidated Tier 1 hepatic finding**, unless a more urgent governed hepatic rule applies.

**Required interpretation, in full:**

1. The panel produces **one** consolidated hepatic concern.
2. All supporting hepatic abnormalities are **nested beneath it**.
3. Individual analytes do **not** become separate concern slots.
4. A minor abnormality is **not** described as urgent merely because it enters Tier 1.
5. The finding means the abnormal hepatic result **warrants discussion or investigation** — contract §6.3.
6. Abnormalities independently meeting Tier 0 or Tier 1 criteria **in another domain** may not be absorbed into the hepatic finding — contract §4.8.

**Basis.** BSG Recommendation 4 (grade B) directs that patients with abnormal liver blood tests should be considered for a liver aetiology screen irrespective of level and duration, where abnormal means outside the laboratory reference range `[E]`. BSG Recommendation 3 states that the extent of abnormality is not necessarily a guide to clinical significance `[E]`.

**No magnitude-gated alternative is retained.** The hepatic Tier 1 floor must not be described as unresolved in any document in this package.

**Note on how the objection was resolved.** The volume objection to the literal reading was that a high Tier 1 hepatic rate would swamp the concern set — roughly 30% of UK liver test requests contain at least one out-of-range result `[E]`. The P2 ratification resolved this **structurally**: with one consolidated nested finding, the panel yields one hepatic concern regardless of how many analytes are abnormal. Volume was a presentation problem and has been addressed as one, without departing from a grade B national recommendation.

Recorded in contract v0.6.2 §15.2.1, scoped to the hepatic domain only.

Anthony: closed via P2 · Reg/legal: no · **Blocking: no**

---

### A8 — Vitamin D
**Status: `CLINICALLY_ADJUDICATED` — CLOSED. Removed from quarantine.**

**Authorised rule — serum 25-hydroxyvitamin D:**

| Concentration | Disposition |
|---|---|
| **<25 nmol/L** | Vitamin D deficiency finding · **Tier 2** · **routine** |
| **25–50 nmol/L** | **No independent clinical finding in this version.** May be used as contextual information where clinically relevant |
| **>50 nmol/L** | No vitamin D concern |
| **Any value** | Where vitamin D contributes to a hypocalcaemia interpretation, it may appear as **context beneath the calcium finding**, regardless of whether it independently meets the <25 nmol/L rule |

**Source and label.** The governed UK source recorded in the HMR A8 decision. The threshold corresponds to the SACN 2016 definition of vitamin D deficiency at <25 nmol/L, carried into NICE guidance, with 25–50 nmol/L classified as insufficiency `[E]`.

*Documentation note:* the exact citation string should be carried across verbatim from the HMR A8 decision record at sign-off, so that this register and that record agree word for word.

**Constraints — all binding:**

- **No supplementation dose is authorised.** HealthIQ does not recommend doses.
- **No higher "optimal" threshold is authorised.** The 25–50 nmol/L insufficiency band does not generate a finding in this version.
- **No Tier 1 vitamin D finding is authorised from concentration alone.**
- **Pregnancy-specific interpretation remains outside scope** — contract §26.
- **No additional insufficiency bands, treatment rules or symptom-based escalation** may be introduced.

Anthony: no · Reg/legal: no · **Blocking: no**

---

## 2. Open clinical-item register

**Empty.**

B1 and A8 were the last two entries and both are closed. No clinical adjudication from this package remains open.

---

## 3. Items closed in earlier revisions — carried forward unchanged

### 3.1 Clinical adjudications

| ID | Decision | Label |
|---|---|---|
| A1 | Hypokalaemia bands 3.0–3.4 / 2.5–2.9 / <2.5; K⁺ <2.5 same day; no mild-consequence language | `[E]` |
| A2 | Hypernatraemia bands 146–150 / 151–155 / >155; Na⁺ ≥155 same day | **`[C]` grade — recorded as such** |
| A3 | Hypocalcaemia bands; adjusted Ca²⁺ <1.9 same day; mandatory symptom-conditional language | `[E]` |
| A4 | Hypernatraemia 146–154 mmol/L → within days | **`[J]`** — label must travel with the rule and may not be upgraded downstream |
| A5 | **No severe-anaemia same-day threshold authorised.** Anaemia caps at within days pending specialist haematology adjudication | Adjudicated decline |
| A6 | Subclinical hyperthyroidism ungraded at within weeks; mirroring the hypothyroid ≥10 threshold prohibited | Adjudicated |
| A7 | Low-TSAT deficiency requirement withdrawn; TSAT is the overload discriminator only | `[E]` |
| A9 | **No standalone numeric total-bilirubin Tier 0 rule.** Hy's law retained — bilirubin there is a multiple of the laboratory's own ULN inside a governed combination | Adjudicated decline |
| A10 | CRP primarily contextual; promotion on persistence only | Adjudicated |
| B2 | **K⁺ >6.0 mmol/L same day** — deliberate conservative HealthIQ adjudication, a knowing departure from UKKA's ≥6.5 because UKKA assumes a clinical pathway with ECG that HealthIQ lacks | Adjudicated departure |
| B4 | Three-part unsafe-without-context test and per-domain registers | Adjudicated |
| B6 | Baseline-validity windows interim, explicitly labelled adjudicated | Adjudicated |
| B7 | Thyroid-only scope; extension is new authoring | Adjudicated |

### 3.2 Product ratifications

| ID | Decision |
|---|---|
| P2 | **Hepatic presentation** — one consolidated finding, supporting abnormalities nested beneath it |
| P7 | **Pregnancy** — mandatory question; `pregnant` and `may_be_pregnant` clinically identical; no answer blocks upload and analysis. **Enforcement not implemented** — §5 |
| P8 | **Sex** — already mandatory in the standard flow, available by design; defensive fail-closed retained for malformed or legacy requests. **Ancestry** — not captured, no adjustment authorised |

---

## 4. Product decisions remaining open — non-blocking

**No remaining product decision blocks clinical ruleset ratification. P1, P3, P4, P5 and P6 remain open as non-blocking presentation, communication or release decisions.**

| ID | Decision | Status | Blocking |
|---|---|---|---|
| P1 | Same-day co-equal group presentation, including at three or more members | `OPEN` | No |
| P3 | Dual-role presentation — one fact appearing as its own concern and as another domain's context | `OPEN` | No |
| P4 | Disease-name communication policy | `OPEN` — interacts with R4 | No |
| P5 | No-concern limitation presentation | `OPEN` | No |
| P6 | Release sequencing for domains with and without Tier 0 | `OPEN` | No |

These are not closed by this revision and must not be recorded as closed.

---

## 5. Questionnaire audit and carry-forward

`HEALTHIQ_UPLOAD_QUESTIONNAIRE_CONTEXT_AUDIT_v0.1.md` is **complete** and has been read. Its findings are recorded in the merged governing register entry for the questionnaire rationalisation carry-forward.

**Summary of the audit position:**

- no pregnancy question currently exists in the canonical questionnaire;
- mandatory questionnaire data is enforced only in the frontend;
- the backend permits analysis without questionnaire data;
- missing sex can silently default;
- unanswered pregnancy status currently permits non-pregnant interpretation;
- regeneration can perpetuate incomplete questionnaire context;
- full questionnaire rationalisation and mandatory-context remediation is **deferred to a later dedicated sprint**;
- this remains a **hard dependency before release and before runtime reliance on questionnaire context**.

**The questionnaire defect has not been fixed.** Nothing in this register, or in any companion document, may imply otherwise.

**Interaction with P7 and P8.** The P7 pregnancy policy and the P8 sex position are **clinical and product positions**, ratified and recorded. Neither is an implementation claim. Contract v0.6.2 §26.3 governs the interim unknown-pregnancy-status case and is explicitly labelled a defensive fallback; §27.4 records that sex is mandatory in the standard flow by design while retaining fail-closed handling. The audit confirms that runtime enforcement matching these positions does not yet exist, which is precisely why the carry-forward is release-blocking.

**Status: `DEFERRED_IMPLEMENTATION_DEPENDENCY`.**

---

## 6. Regulatory and legal items — all remain open

None has been closed and none may be closed by clinical or product authority.

| ID | Item | Status | Blocking |
|---|---|---|---|
| **R1** | Tier 0 action-and-timeframe guidance — **18 fully specified rules**, all specification-only | `REG_LEGAL_PENDING` | **Yes for any Tier 0 release** |
| **R2** | Individual cardiovascular risk calculation — **quarantined** | `REG_LEGAL_PENDING` | Yes, that capability |
| **R3** | FIB-4 — **quarantined** | `REG_LEGAL_PENDING` | Yes, that capability |
| R4 | Consumer disease-name outputs | `REG_LEGAL_PENDING` | Yes |
| **R5** | Population exclusions and intended-purpose wording — includes the ratified pregnancy exclusion | `REG_LEGAL_PENDING` | **Yes** |
| **R6** | Whether renal/electrolytes may be released with Tier 0 suppressed | `REG_LEGAL_PENDING` | **Yes** |

**R6 remains the package's most consequential open item.** The B2 adjudication lowered the same-day potassium threshold to >6.0, so HealthIQ identifies more people with a life-threatening result it has no governed way to act on. Renal/electrolyte holds 8 of the 18 Tier 0 rules, six of them potentially life-threatening.

---

## 7. Blocking summary

| Category | Blocking items |
|---|---|
| **Clinical** | **None.** No unresolved clinical adjudication remains in this package |
| **Product** | **None blocking clinical ruleset ratification.** P1, P3, P4, P5, P6 remain open and non-blocking |
| **Regulatory/legal** | **R1, R5, R6**; plus R2 and R3 for their specific capabilities |
| **Implementation** | **Questionnaire rationalisation carry-forward** — deferred; blocks release and runtime reliance on questionnaire context, not the clinical ruleset |

**Closed in this revision:** B1, A8.
**Closed in v0.2:** A4, A5, A9, B2, B5, P2, P7, P8.
**Vitamin D removed from quarantine.** FIB-4 and cardiovascular risk calculation remain quarantined pending R2 and R3.

---

## 8. Version consistency

| Document | Version |
|---|---|
| Contract | **v0.6.2** |
| Cross-domain ruleset | **v0.4** |
| Adjudication register | **v0.3** (this document) |
| Closure report | **v0.3** |
| Tier 0 count | **18** |

---

## 9. Sign-off

| Field | Value |
|---|---|
| Register version | 0.3 |
| Contract version | v0.6.2 |
| HMR name / registration | ☐ |
| B1 closed — literal BSG position, no magnitude-gated alternative retained | ☐ |
| A8 closed — narrow vitamin D rule, all five constraints confirmed | ☐ |
| Vitamin D citation string reconciled verbatim with the HMR A8 decision record | ☐ |
| Open clinical-item register confirmed empty | ☐ |
| P1, P3, P4, P5, P6 confirmed open and non-blocking | ☐ |
| Questionnaire carry-forward confirmed deferred and **not** fixed | ☐ |
| Regulatory items confirmed open | ☐ |
| Signature / date | ☐ |
