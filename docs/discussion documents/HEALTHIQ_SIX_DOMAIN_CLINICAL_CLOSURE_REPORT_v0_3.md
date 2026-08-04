---
document_id: HEALTHIQ-SIX-DOMAIN-CLOSURE-REPORT-001
title: HealthIQ Six-Domain Clinical Closure Report
version: "0.3"
supersedes: "0.2"
covers:
  - HEALTHIQ-CLIN-PRIORITY-CONTRACT-001 v0.6.2
  - HEALTHIQ-CROSS-DOMAIN-RULESET-001 v0.4
  - HEALTHIQ-CROSS-DOMAIN-HMR-ADJUDICATION-REGISTER-001 v0.3
hmr_disposition: CLINICALLY_RATIFIED_SUBJECT_TO_TARGETED_DOCUMENT_CORRECTION
status: CORRECTION_PASS_COMPLETE
implementation_status: NOT_AUTHORISED
---

# Six-Domain Clinical Closure Report v0.3

One targeted correction pass. No new review, no fresh clinical authoring, no implementation. No ratified product decision or completed HMR adjudication was reopened.

---

## 1. B1 — hepatic Tier 1 floor: CLOSED

**Status: `CLINICALLY_ADJUDICATED`.**

The BSG position is adopted **literally**. Any out-of-range core hepatic analyte produces **one consolidated Tier 1 hepatic finding**, unless a more urgent governed hepatic rule applies.

Required interpretation, recorded identically in the contract, register and ruleset:

1. One consolidated hepatic concern per panel.
2. Supporting hepatic abnormalities nested beneath it.
3. Individual analytes do not become separate concern slots.
4. A minor abnormality is not described as urgent merely because it enters Tier 1.
5. The finding means the abnormal hepatic result warrants discussion or investigation.
6. Abnormalities independently meeting Tier 0 or Tier 1 criteria in another domain may not be absorbed.

**No magnitude-gated alternative is retained**, and the floor is not described as unresolved anywhere in the package.

**Two things worth recording about how this closed.** The volume objection — roughly 30% of UK liver test requests contain an out-of-range result `[E]` — was resolved **structurally** by the P2 nested-consolidation ratification, not by departing from a grade B national recommendation. And the floor remains **hepatic-bound**: it is falsified in haematology (isolated mild macrocytosis, Tier 2 with reassurance available) and in inflammatory markers (isolated mild CRP, Tier 2). Contract §18.23 continues to prohibit its export, and contract §15.2.1 is explicitly scoped so that no other domain may adopt hepatic-style consolidation on the strength of it.

---

## 2. A8 — vitamin D: CLOSED

**Status: `CLINICALLY_ADJUDICATED`. Removed from quarantine.**

Authorised rule for serum 25-hydroxyvitamin D:

| Concentration | Disposition |
|---|---|
| **<25 nmol/L** | Vitamin D deficiency finding · **Tier 2** · **routine** |
| **25–50 nmol/L** | **No independent clinical finding** in this version; contextual only where clinically relevant |
| **>50 nmol/L** | No vitamin D concern |
| Any value | Where vitamin D contributes to a hypocalcaemia interpretation, it appears as context beneath the calcium finding regardless of whether it independently meets the <25 nmol/L rule |

**Source:** the governed UK source recorded in the HMR A8 decision — the SACN 2016 deficiency threshold of <25 nmol/L, carried into NICE guidance, with 25–50 nmol/L classified as insufficiency. **`[E]`**.

Constraints, all binding: no supplementation dose; no higher "optimal" threshold; no Tier 1 vitamin D finding from concentration alone; pregnancy-specific interpretation out of scope; no additional insufficiency bands, treatment rules or symptom-based escalation.

*One documentation item:* the exact citation string should be carried across verbatim from the HMR A8 decision record at sign-off, so the register and that record agree word for word.

---

## 3. No clinical adjudication remains open

**The open clinical-item register is empty.** B1 and A8 were the last two entries.

Every clinical decision in this package is now one of: adjudicated and adopted; adjudicated and declined; or explicitly labelled interim with its evidence grade attached. Adjudicated declines carried forward — no severe-anaemia same-day threshold (A5), no standalone bilirubin Tier 0 rule (A9), no subclinical hyperthyroidism bands (A6), no CRP severity bands (A10) — remain declines, not gaps.

Two labels must survive downstream reworking and are called out here because they are the kind that quietly disappear: **hypernatraemia 146–154 mmol/L is `[J]`**, and the **hypernatraemia band set as a whole is `[C]`**, not `[E]`.

---

## 4. Product decisions

**Product decisions required for clinical ratification are closed:** P2 (hepatic presentation), P7 (pregnancy policy) and P8 (sex and ancestry).

**No remaining product decision blocks clinical ruleset ratification. P1, P3, P4, P5 and P6 remain open as non-blocking presentation, communication or release decisions.**

| ID | Decision | Status |
|---|---|---|
| P1 | Same-day co-equal group presentation, including at three or more members | `OPEN`, non-blocking |
| P3 | Dual-role presentation | `OPEN`, non-blocking |
| P4 | Disease-name communication policy | `OPEN`, non-blocking |
| P5 | No-concern limitation presentation; broader cross-domain Tier 1 presentation density | `OPEN`, non-blocking |
| P6 | Release sequencing for domains with and without Tier 0 | `OPEN`, non-blocking |

These five are **not** closed by this pass and are not recorded as closed. The v0.2 phrasing that the product category was "fully unblocked" has been removed from every document, because it could be read as closing them.

---

## 5. Regulatory and legal dependencies — all remain open

| ID | Item | Blocking |
|---|---|---|
| **R1** | Tier 0 action-and-timeframe guidance — **18 fully specified rules**, all specification-only | **Yes for any Tier 0 release** |
| **R2** | Individual cardiovascular risk calculation — **quarantined** | Yes, that capability |
| **R3** | FIB-4 — **quarantined** | Yes, that capability |
| R4 | Consumer disease-name outputs | Yes |
| **R5** | Population exclusions and intended-purpose wording — includes the ratified pregnancy exclusion | **Yes** |
| **R6** | Whether renal/electrolytes may be released with Tier 0 suppressed | **Yes** |

None may be closed by clinical or product authority.

**R6 remains the most consequential open item in the package.** Renal/electrolyte holds 8 of the 18 Tier 0 rules, six concerning potentially life-threatening results. The B2 adjudication lowering the same-day potassium threshold to >6.0 means HealthIQ identifies more people with a result it has no governed way to act on. Nothing in this correction pass changes that.

---

## 6. Questionnaire remediation — deferred and release-blocking

`HEALTHIQ_UPLOAD_QUESTIONNAIRE_CONTEXT_AUDIT_v0.1.md` is **complete** and has been read. The v0.2 statements that it was not supplied have been removed from every document and replaced with accurate references to the completed audit and the merged carry-forward register entry.

Audit position, as recorded across the package:

- no pregnancy question currently exists in the canonical questionnaire;
- mandatory questionnaire data is enforced only in the frontend;
- the backend permits analysis without questionnaire data;
- missing sex can silently default;
- unanswered pregnancy status currently permits non-pregnant interpretation;
- regeneration can perpetuate incomplete questionnaire context;
- full questionnaire rationalisation and mandatory-context remediation is **deferred to a later dedicated sprint**;
- this remains a **hard dependency before release and before runtime reliance on questionnaire context**.

**The questionnaire defect has not been fixed and no document in this package implies otherwise.**

**One consequence stated plainly.** The ratified P7 policy (pregnancy identical treatment, explicit out-of-scope output) and the ratified P8 position (no silent sex default) both differ from current runtime behaviour as the audit describes it. That gap is recorded in ruleset v0.4 §4.2 and §5, not resolved, and it is exactly why the carry-forward is release-blocking rather than merely outstanding. Contract §26.3 and §27.4 are both explicitly labelled defensive fallbacks governing the interim, and neither is authority for operating without the context once enforcement exists.

---

## 7. Implementation

**No implementation is authorised.** No implementation, architecture hardening, sprint planning, questionnaire redesign or regulatory adjudication was performed in this pass. All documents carry `implementation_status: NOT_AUTHORISED`.

---

## 8. Consistency check across the four revised documents

| Item | Position |
|---|---|
| Contract version | **v0.6.2** |
| Ruleset version | **v0.4** |
| Adjudication register version | **v0.3** |
| Closure report version | **v0.3** (this document) |
| B1 status | **`CLINICALLY_ADJUDICATED` — closed.** Literal BSG; no magnitude-gated alternative |
| A8 status | **`CLINICALLY_ADJUDICATED` — closed.** Vitamin D out of quarantine |
| Vitamin D thresholds | **<25 nmol/L → Tier 2 routine · 25–50 no independent finding · >50 no concern · contextual under calcium regardless** |
| Hepatic Tier 1 treatment | **One consolidated finding, supporting abnormalities nested; hepatic-bound; not a universal Tier 1 density rule** |
| Questionnaire audit status | **Complete; remediation deferred; release-blocking; not fixed** |
| Remaining product decisions | **P1, P3, P4, P5, P6 open and non-blocking.** No product decision blocks clinical ratification |
| Regulatory/legal blockers | **R1, R5, R6 blocking; R2 and R3 blocking their specific capabilities; R4 open** |
| Tier 0 count | **18** — unchanged; neither authorised change touches Tier 0 |

No superseded statement has been left in place. The v0.2 "audit not supplied" and "fully unblocked" wordings are removed throughout, and the vitamin D quarantine entry has been removed from the quarantine table rather than merely annotated.

---

## VERDICT: READY_FOR_FINAL_INDEPENDENT_CONSISTENCY_REVIEW

Contract v0.6.2, cross-domain ruleset v0.4, adjudication register v0.3 and this report are ready for one final independent cross-domain consistency review.

No clinical adjudication from this package remains open. Product decisions required for clinical ratification are closed and five non-blocking ones remain open. Regulatory and legal dependencies remain open and cannot be closed by clinical or product authority. Questionnaire remediation remains deferred and release-blocking. No implementation is authorised.

**Four items the consistency reviewer should target.**

**`XD-AS-24`** — ALT at 1.2× ULN producing one Tier 1 hepatic finding that is explicitly *not* described as urgent. This is the literal floor at its mildest and the scenario where the tone requirement is easiest to get wrong.

**`XD-AS-28` and `XD-AS-29`** — vitamin D nesting beneath a calcium finding, with and without meeting the <25 nmol/L rule. Tests that the contextual route is genuinely independent of the finding route rather than a special case of it.

**Contract §15.2.1 scope** — the clause must not have leaked into a general Tier 1 consolidation rule. `XD-AS-10` is the guard: MCV and CRP must remain separate Tier 2 findings with no hepatic-style consolidation applied.

**The Tier 0 count of 18** — unchanged in this pass, but I introduced a counting error two revisions ago and it should be verified against the six domain files rather than trusted.
