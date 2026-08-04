---
document_id: HEALTHIQ-SIX-DOMAIN-CLOSURE-REPORT-001
title: HealthIQ Six-Domain Clinical Closure Report
version: "0.4"
supersedes: "0.3"
covers:
  - HEALTHIQ-CLIN-PRIORITY-CONTRACT-001 v0.6.3
  - HEALTHIQ-CROSS-DOMAIN-RULESET-001 v0.5
  - HEALTHIQ-CROSS-DOMAIN-HMR-ADJUDICATION-REGISTER-001 v0.4
status: CLINICALLY_RATIFIED_FOR_ARCHITECTURE_HARDENING
implementation_status: NOT_AUTHORISED
---

# Six-Domain Clinical Closure Report v0.4

One final targeted correction pass. No new review, no fresh clinical authoring, no implementation. No settled product decision or clinical adjudication was reopened.

Three corrections only: vitamin D contextual handling; vitamin D evidence attribution; package status.

---

## 1. Vitamin D contextual handling — corrected

**The v0.4 package was wrong and the HMR was right to catch it.**

The previous wording allowed vitamin D to be nested beneath a hypocalcaemia finding as an aetiological contributor "regardless of whether it independently meets the <25 nmol/L rule", and at "any value". That permitted a **normal** vitamin D result to be presented as a plausible cause of a low calcium. It is not one. A normal vitamin D is evidence *against* a vitamin D cause, and presenting it as context supporting one would misdirect investigation away from the actual cause of the hypocalcaemia — in a domain where the Society for Endocrinology treats symptomatic hypocalcaemia at any level below the reference range as an emergency.

The corrected rule is concentration-dependent, and the three cases are not interchangeable.

**Vitamin D <25 nmol/L with hypocalcaemia present**
- may be nested beneath the calcium finding as a **plausible contributing factor**;
- must **not** occupy a separate competing Tier 2 concern slot;
- the calcium finding **retains its own tier and urgency**.

**Vitamin D 25–50 nmol/L with hypocalcaemia present**
- may be shown **only as limited contextual information**;
- must **not** be described as proven deficiency;
- must **not** be described as an established cause of the hypocalcaemia;
- does **not** create an independent vitamin D finding.

**Vitamin D >50 nmol/L with hypocalcaemia present**
- must **not** be nested as an aetiological contributor;
- may be used **only** to state that vitamin D deficiency is not supported by the available result;
- **investigation of the calcium finding must proceed independently**.

Updated consistently across `XD-VITD-2`, `XD-C15`, the vitamin D table, shared-marker ownership, all acceptance scenarios, and every summary in the contract, register and this report. `XD-AS-29` is replaced; `XD-AS-28` is retained and clarified; `XD-AS-30` is added to cover the 25–50 nmol/L case, which the previous matrix did not test.

**Retained unchanged:** `<25 nmol/L` → Tier 2 routine deficiency finding where no higher-priority calcium finding absorbs it; `25–50 nmol/L` → no independent finding; `>50 nmol/L` → no concern; no supplementation dose; no Tier 1 finding from concentration alone; no pregnancy-specific interpretation; no additional treatment or escalation rules.

---

## 2. Vitamin D evidence attribution — corrected

The previous package attributed the full three-band structure to the governed UK source and carried a sign-off note asking for the exact citation to be reconciled later. Both are corrected.

> The governed UK evidence supports `<25 nmol/L` as the threshold below which risk of poor musculoskeletal health increases. HealthIQ does not create an independent finding at `25–50 nmol/L` in this version and creates no vitamin D concern above `50 nmol/L`.

The two upper dispositions are **HealthIQ policy dispositions**, not source-defined diagnostic categories, and the governed source is not cited as authority for them. No document in the package presents the three-band structure as a source-defined classification.

**The deferred-citation note is removed.** The final documents contain the exact evidence attribution they rely upon; nothing is left to be added later.

This matters beyond tidiness. Attributing a HealthIQ policy choice to a national source makes it look harder to revisit than it is, and it would misrepresent the strength of the evidence behind the 25–50 nmol/L band in particular.

---

## 3. Package status

Status is now `CLINICALLY_RATIFIED_FOR_ARCHITECTURE_HARDENING`, applied consistently to the contract, ruleset, adjudication register and this report — in front matter, contract §25, and every summary and verdict.

Superseded statuses removed throughout: `CLINICALLY_RATIFIED_SUBJECT_TO_TARGETED_DOCUMENT_CORRECTION`; `CLINICALLY_VALIDATED_FOR_DOMAIN_AUTHORING_WITH_CLOSURE_AMENDMENTS`; `DRAFT_FOR_FINAL_INDEPENDENT_CONSISTENCY_REVIEW`; `READY_FOR_FINAL_INDEPENDENT_CONSISTENCY_REVIEW`.

**`implementation_status: NOT_AUTHORISED` is retained in every document.**

The new status means the clinical package is ready for architecture hardening. **It does not authorise implementation or release.** Contract §23.6 governance conditions continue to apply.

---

## 4. Settled positions — all preserved unchanged

Confirmed carried forward without amendment:

| Position | State |
|---|---|
| Literal hepatic Tier 1 floor | Unchanged |
| Nested consolidated hepatic presentation | Unchanged |
| Tier 0 count | **18** — neither correction touches Tier 0 |
| Potassium >6.0 mmol/L same-day rule | Unchanged |
| Hypernatraemia `[J]` (146–154 placement) and `[C]` (band set) labels | Unchanged |
| No severe-anaemia same-day rule | Unchanged |
| No standalone bilirubin Tier 0 rule | Unchanged |
| Hy's law | Unchanged |
| CRP contextual policy | Unchanged |
| Subclinical hyperthyroidism policy | Unchanged |
| Pregnancy policy | Unchanged |
| Sex and ancestry policy | Unchanged |
| Questionnaire remediation carry-forward | Unchanged — deferred and release-blocking |
| Regulatory and legal blockers | Unchanged — all open |
| P1, P3, P4, P5, P6 | Unchanged — open and non-blocking |
| FIB-4 and cardiovascular-risk quarantine | Unchanged |

---

## 5. Position at close

**No clinical adjudication from this package remains open.** The open clinical-item register is empty.

**No remaining product decision blocks clinical ruleset ratification. P1, P3, P4, P5 and P6 remain open as non-blocking presentation, communication or release decisions.**

**Regulatory and legal dependencies remain open** and cannot be closed by clinical or product authority: R1 (Tier 0 action guidance, 18 rules), R2 (cardiovascular risk calculation, quarantined), R3 (FIB-4, quarantined), R4 (disease-name outputs), R5 (population exclusions and intended-purpose wording), R6 (renal/electrolyte release with Tier 0 suppressed). **R6 remains the most consequential.**

**Questionnaire remediation remains deferred and release-blocking.** The audit is complete; the defect is not fixed; the ratified pregnancy and sex positions differ from current runtime behaviour, and that gap is recorded rather than resolved.

**No implementation is authorised.**

---

## 6. Consistency check across the four revised documents

| Item | Position |
|---|---|
| Contract version | **v0.6.3** |
| Ruleset version | **v0.5** |
| Adjudication register version | **v0.4** |
| Closure report version | **v0.4** (this document) |
| Final clinical status | **`CLINICALLY_RATIFIED_FOR_ARCHITECTURE_HARDENING`** |
| Implementation status | **`NOT_AUTHORISED`** |
| Vitamin D thresholds | **<25 nmol/L Tier 2 routine · 25–50 no independent finding · >50 no concern** |
| Vitamin D contextual handling | **Concentration-dependent: <25 nests as plausible contributor · 25–50 limited context only, not proven deficiency, not an established cause · >50 not nested, may only state deficiency unsupported** |
| Evidence attribution | **`<25 nmol/L` governed UK evidence; 25–50 and >50 are HealthIQ policy dispositions** |
| Hepatic Tier 1 treatment | **Literal BSG; one consolidated nested finding; hepatic-bound, not a universal Tier 1 density rule** |
| Tier 0 count | **18** |
| Questionnaire dependency | **Complete audit; remediation deferred; release-blocking; not fixed** |
| Remaining product decisions | **P1, P3, P4, P5, P6 open and non-blocking** |
| Regulatory and legal blockers | **R1, R5, R6 blocking; R2 and R3 blocking their capabilities; R4 open** |

**No superseded "any vitamin D value may be contextual" wording remains anywhere in the package.** The withdrawn formulations are recorded as withdrawn in ruleset §9.2 `XD-VITD-3` and register §1.2 so the correction is auditable, but no operative clause carries them.

---

## STATUS: CLINICALLY_RATIFIED_FOR_ARCHITECTURE_HARDENING
