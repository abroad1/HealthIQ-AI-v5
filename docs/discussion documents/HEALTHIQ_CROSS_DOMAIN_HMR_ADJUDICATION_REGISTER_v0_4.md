---
document_id: HEALTHIQ-CROSS-DOMAIN-HMR-ADJUDICATION-REGISTER-001
title: HealthIQ Cross-Domain HMR Adjudication Register
version: "0.4"
supersedes: "0.3"
governing_contract: HEALTHIQ-CLIN-PRIORITY-CONTRACT-001 v0.6.3
companion_documents:
  - HEALTHIQ-CROSS-DOMAIN-RULESET-001 v0.5
  - HEALTHIQ-SIX-DOMAIN-CLOSURE-REPORT-001 v0.4
status: CLINICALLY_RATIFIED_FOR_ARCHITECTURE_HARDENING
implementation_status: NOT_AUTHORISED
---

# Cross-Domain HMR Adjudication Register v0.4

**Status vocabulary:** `CLINICALLY_ADJUDICATED` · `PRODUCT_RATIFIED` · `REG_LEGAL_PENDING` · `DEFERRED_IMPLEMENTATION_DEPENDENCY` · `OPEN`.

**Evidence labels:** `[E]` · `[C]` · `[J]` · `[U]`.

**No clinical adjudication from this package remains open.**

---

## 0. Changes from v0.3

Two corrections to the A8 record. **No adjudication is reopened and no other entry changes.**

1. **Vitamin D contextual handling corrected.** The v0.3 record permitted vitamin D to appear as a contributor to a hypocalcaemia interpretation "regardless of whether it independently meets the <25 nmol/L rule". That allowed a normal result to be presented as an aetiological contributor, which is clinically wrong. Contextual handling is now concentration-dependent.
2. **Vitamin D evidence attribution corrected.** The v0.3 record attributed the full three-band structure to SACN/NICE and carried a sign-off note asking for the exact citation to be reconciled later. Both are corrected: only the `<25 nmol/L` threshold is attributed to the governed source, the other bands are recorded as HealthIQ policy dispositions, and the deferred-citation note is removed.

Package status updated to `CLINICALLY_RATIFIED_FOR_ARCHITECTURE_HARDENING`.

---

## 1. A8 — Vitamin D
**Status: `CLINICALLY_ADJUDICATED` — CLOSED. Not quarantined.**

### 1.1 Concentration bands

| Concentration | Disposition |
|---|---|
| **<25 nmol/L** | Vitamin D deficiency finding · **Tier 2** · **routine**, where no higher-priority calcium finding absorbs it |
| **25–50 nmol/L** | **No independent clinical finding in this version.** May be used as limited contextual information where clinically relevant |
| **>50 nmol/L** | **No vitamin D concern** |

### 1.2 Contextual handling beneath hypocalcaemia — concentration-dependent

**Corrected in v0.4.** The three cases are not interchangeable.

**Vitamin D <25 nmol/L with hypocalcaemia present:**
- vitamin D deficiency **may be nested beneath the calcium finding as a plausible contributing factor**;
- it **must not** occupy a separate competing Tier 2 concern slot;
- the calcium finding **retains its own tier and urgency**.

**Vitamin D 25–50 nmol/L with hypocalcaemia present:**
- it may be shown **only as limited contextual information**;
- it **must not** be described as proven deficiency;
- it **must not** be described as an established cause of the hypocalcaemia;
- it **does not** create an independent vitamin D finding.

**Vitamin D >50 nmol/L with hypocalcaemia present:**
- it **must not** be nested as an aetiological contributor;
- it may be used **only** to state that vitamin D deficiency is not supported by the available result;
- **investigation of the calcium finding must proceed independently**.

The v0.3 formulations permitting nesting "regardless of whether it independently meets the <25 nmol/L rule" or at "any value" are **withdrawn**. A normal vitamin D result is evidence against a vitamin D cause, not context supporting one.

### 1.3 Evidence attribution — corrected in v0.4

The governed UK evidence supports **`<25 nmol/L` as the threshold below which risk of poor musculoskeletal health increases** `[E]`.

HealthIQ **does not create an independent finding at `25–50 nmol/L`** in this version and **creates no vitamin D concern above `50 nmol/L`**. Those two dispositions are **HealthIQ policy dispositions**, not source-defined diagnostic categories, and the governed source is not cited as authority for them.

No deferred-citation note is carried. This record contains the exact evidence attribution it relies upon.

### 1.4 Constraints — binding, unchanged

- **No supplementation dose is authorised.**
- **No higher "optimal" threshold is authorised.**
- **No Tier 1 vitamin D finding from concentration alone.**
- **Pregnancy-specific interpretation remains outside scope** — contract §26.
- **No additional insufficiency bands, treatment rules or symptom-based escalation** may be introduced.

Anthony: no · Reg/legal: no · **Blocking: no**

---

## 2. B1 — Hepatic Tier 1 floor
**Status: `CLINICALLY_ADJUDICATED` — CLOSED. Unchanged from v0.3.**

**Decision: adopt the BSG position literally.** Any out-of-range core hepatic analyte produces **one consolidated Tier 1 hepatic finding**, unless a more urgent governed hepatic rule applies.

Required interpretation: one consolidated hepatic concern; supporting abnormalities nested beneath it; individual analytes do not become separate concern slots; a minor abnormality is not described as urgent merely because it enters Tier 1; the finding means the abnormal result warrants discussion or investigation; abnormalities independently meeting Tier 0 or Tier 1 criteria in another domain may not be absorbed.

Basis: BSG Recommendation 4 (grade B) `[E]`; BSG Recommendation 3 `[E]`.

**No magnitude-gated alternative is retained.** Recorded in contract §15.2.1, scoped to the hepatic domain only.

Anthony: closed via P2 · Reg/legal: no · **Blocking: no**

---

## 3. Open clinical-item register

**Empty.**

---

## 4. Items closed in earlier revisions — carried forward unchanged

### 4.1 Clinical adjudications

| ID | Decision | Label |
|---|---|---|
| A1 | Hypokalaemia bands 3.0–3.4 / 2.5–2.9 / <2.5; K⁺ <2.5 same day; no mild-consequence language | `[E]` |
| A2 | Hypernatraemia bands 146–150 / 151–155 / >155; Na⁺ ≥155 same day | **`[C]` grade** |
| A3 | Hypocalcaemia bands; adjusted Ca²⁺ <1.9 same day; mandatory symptom-conditional language | `[E]` |
| A4 | Hypernatraemia 146–154 mmol/L → within days | **`[J]`** — label must travel with the rule |
| A5 | **No severe-anaemia same-day threshold authorised.** Anaemia caps at within days | Adjudicated decline |
| A6 | Subclinical hyperthyroidism ungraded at within weeks; mirroring the hypothyroid ≥10 threshold prohibited | Adjudicated |
| A7 | Low-TSAT deficiency requirement withdrawn; TSAT is the overload discriminator only | `[E]` |
| A9 | **No standalone numeric total-bilirubin Tier 0 rule.** Hy's law retained | Adjudicated decline |
| A10 | CRP primarily contextual; promotion on persistence only | Adjudicated |
| B2 | **K⁺ >6.0 mmol/L same day** — deliberate conservative HealthIQ adjudication, knowing departure from UKKA's ≥6.5 | Adjudicated departure |
| B4 | Three-part unsafe-without-context test and per-domain registers | Adjudicated |
| B6 | Baseline-validity windows interim, explicitly labelled adjudicated | Adjudicated |
| B7 | Thyroid-only scope; extension is new authoring | Adjudicated |

### 4.2 Product ratifications

| ID | Decision |
|---|---|
| P2 | **Hepatic presentation** — one consolidated finding, supporting abnormalities nested beneath it |
| P7 | **Pregnancy** — mandatory question; `pregnant` and `may_be_pregnant` clinically identical; no answer blocks upload and analysis. **Enforcement not implemented** — §6 |
| P8 | **Sex** — mandatory in the standard flow, available by design; defensive fail-closed retained. **Ancestry** — not captured, no adjustment authorised |

---

## 5. Product decisions remaining open — non-blocking

**No remaining product decision blocks clinical ruleset ratification. P1, P3, P4, P5 and P6 remain open as non-blocking presentation, communication or release decisions.**

| ID | Decision | Status | Blocking |
|---|---|---|---|
| P1 | Same-day co-equal group presentation, including at three or more members | `OPEN` | No |
| P3 | Dual-role presentation | `OPEN` | No |
| P4 | Disease-name communication policy | `OPEN` | No |
| P5 | No-concern limitation presentation; broader cross-domain Tier 1 presentation density | `OPEN` | No |
| P6 | Release sequencing for domains with and without Tier 0 | `OPEN` | No |

Not closed by this revision and not recorded as closed.

---

## 6. Questionnaire audit and carry-forward — unchanged

`HEALTHIQ_UPLOAD_QUESTIONNAIRE_CONTEXT_AUDIT_v0.1.md` is **complete**. Findings recorded in the merged governing register entry for the questionnaire rationalisation carry-forward:

- no pregnancy question currently exists in the canonical questionnaire;
- mandatory questionnaire data is enforced only in the frontend;
- the backend permits analysis without questionnaire data;
- missing sex can silently default;
- unanswered pregnancy status currently permits non-pregnant interpretation;
- regeneration can perpetuate incomplete questionnaire context;
- full questionnaire rationalisation and mandatory-context remediation is **deferred to a later dedicated sprint**;
- this remains a **hard dependency before release and before runtime reliance on questionnaire context**.

**The questionnaire defect has not been fixed.**

**Status: `DEFERRED_IMPLEMENTATION_DEPENDENCY`.**

---

## 7. Regulatory and legal items — all remain open

| ID | Item | Status | Blocking |
|---|---|---|---|
| **R1** | Tier 0 action-and-timeframe guidance — **18 fully specified rules**, all specification-only | `REG_LEGAL_PENDING` | **Yes for any Tier 0 release** |
| **R2** | Individual cardiovascular risk calculation — **quarantined** | `REG_LEGAL_PENDING` | Yes, that capability |
| **R3** | FIB-4 — **quarantined** | `REG_LEGAL_PENDING` | Yes, that capability |
| R4 | Consumer disease-name outputs | `REG_LEGAL_PENDING` | Yes |
| **R5** | Population exclusions and intended-purpose wording | `REG_LEGAL_PENDING` | **Yes** |
| **R6** | Renal/electrolyte release with Tier 0 suppressed | `REG_LEGAL_PENDING` | **Yes** |

None may be closed by clinical or product authority. **R6 remains the package's most consequential open item.**

---

## 8. Blocking summary

| Category | Blocking items |
|---|---|
| **Clinical** | **None** |
| **Product** | **None blocking clinical ruleset ratification.** P1, P3, P4, P5, P6 open and non-blocking |
| **Regulatory/legal** | **R1, R5, R6**; plus R2 and R3 for their specific capabilities |
| **Implementation** | **Questionnaire rationalisation carry-forward** — deferred; blocks release and runtime reliance on questionnaire context, not the clinical ruleset |

---

## 9. Version consistency

| Item | Position |
|---|---|
| Contract | **v0.6.3** |
| Cross-domain ruleset | **v0.5** |
| Adjudication register | **v0.4** (this document) |
| Closure report | **v0.4** |
| Clinical status | **`CLINICALLY_RATIFIED_FOR_ARCHITECTURE_HARDENING`** |
| Implementation status | **`NOT_AUTHORISED`** |
| Tier 0 count | **18** |
| Vitamin D thresholds | **<25 Tier 2 routine · 25–50 no independent finding · >50 no concern** |
| Vitamin D contextual handling | **Concentration-dependent** |
| Vitamin D attribution | **`<25 nmol/L` governed UK evidence; other bands HealthIQ policy** |
| Hepatic Tier 1 | **Literal BSG; one consolidated nested finding; hepatic-bound** |

---

## 10. Sign-off

| Field | Value |
|---|---|
| Register version | 0.4 |
| Contract version | v0.6.3 |
| HMR name / registration | ☐ |
| A8 vitamin D contextual handling confirmed concentration-dependent | ☐ |
| A8 evidence attribution confirmed — only `<25 nmol/L` attributed to the governed source | ☐ |
| No deferred-citation note remains | ☐ |
| B1 confirmed unchanged | ☐ |
| Open clinical-item register confirmed empty | ☐ |
| P1, P3, P4, P5, P6 confirmed open and non-blocking | ☐ |
| Questionnaire carry-forward confirmed deferred and **not** fixed | ☐ |
| Regulatory items confirmed open | ☐ |
| Status confirmed `CLINICALLY_RATIFIED_FOR_ARCHITECTURE_HARDENING` | ☐ |
| Signature / date | ☐ |
