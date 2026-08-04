---
document_id: HEALTHIQ-SIX-DOMAIN-CLOSURE-REPORT-001
title: HealthIQ Six-Domain Clinical Closure Report
version: "0.2"
supersedes: "0.1"
covers:
  - HEALTHIQ-CLIN-PRIORITY-CONTRACT-001 v0.6.1
  - HEALTHIQ-CROSS-DOMAIN-RULESET-001 v0.3
  - HEALTHIQ-CROSS-DOMAIN-HMR-ADJUDICATION-REGISTER-001 v0.2
status: REVISION_COMPLETE
implementation_status: NOT_AUTHORISED
---

# Six-Domain Clinical Closure Report v0.2

A targeted revision. The six-domain review was not restarted, no ratified product decision was reopened, no new clinical threshold was invented, and no implementation, questionnaire redesign, architecture or sprint work was performed.

**Missing governing input.** `HEALTHIQ_UPLOAD_QUESTIONNAIRE_CONTEXT_AUDIT_v0.1.md` was named but not supplied. Consequence, stated once and applied throughout: this package records **that** a questionnaire/runtime defect exists and is deferred, but does **not** characterise its specifics. Nothing else in the revision depended on it.

---

## 1. Product decisions now closed

| ID | Decision | Effect on the clinical package |
|---|---|---|
| **P2** | **Hepatic presentation** — one consolidated finding, supporting abnormalities nested beneath it | Closes the Tier 1 volume concern **structurally** rather than by compression. A panel with four abnormal hepatic analytes yields one hepatic concern with four nested constituents. This is also what contract §3.1 and hepatic `HEP-CONS-1` already required, so ratification aligned presentation with the clinical model rather than overriding it |
| **P7** | **Pregnancy** — mandatory question; `pregnant` and `may_be_pregnant` clinically identical; no answer blocks upload and analysis | Policy closed. **Enforcement is not implemented** and is deferred; see §4 |
| **P8** | **Sex** — already mandatory in the standard flow, available by design; defensive fail-closed retained for malformed or legacy requests. **Ancestry** — not captured, no adjustment authorised | Sex-dependent thresholds now operate normally rather than via indeterminate disposition. Ancestry non-adjustment becomes a **permanent declared limitation** rather than a pending gap |

**The product category is now fully unblocked.** P1, P3, P4, P5 and P6 remain open but none blocks the clinical ruleset.

**One consequence worth flagging.** P2 has weakened the volume argument against adopting the hepatic Tier 1 floor literally (B1). With nested consolidation, the panel yields one hepatic concern regardless of how many analytes are abnormal. The product dimension of B1 is now closed; only the clinical choice remains, and the main practical objection to the literal reading has largely dissolved.

---

## 2. HMR adjudications now closed

| ID | Decision | Type |
|---|---|---|
| **A4** | Hypernatraemia 146–154 mmol/L → `within days`, labelled **`[J]`** | Adjudicated. The `[J]` label must travel with the rule and may not be upgraded downstream |
| **A5** | **No severe-anaemia same-day threshold authorised.** Anaemia caps at `within days` pending specialist haematology adjudication | Adjudicated **decline** |
| **A9** | **No standalone numeric total-bilirubin Tier 0 rule.** Other governed hepatic Tier 0 combinations retained | Adjudicated **decline** |
| **B2** | **K⁺ >6.0 mmol/L is same day** — deliberate conservative HealthIQ adjudication | Adjudicated **departure** from the UK national threshold, with the reason recorded |

Carried forward from v0.1 and unchanged: A1, A2 (`[C]` grade), A3, A6 (subclinical hyperthyroidism ungraded at within weeks), A7, A10 (CRP primarily contextual), B4, B6, B7.

### 2.1 Three consequences that matter

**The Tier 0 count is now 18, and the earlier figures were wrong.** v0.1 said 20 including three unbanded placeholders; v0.2 said 23, which double-counted the three electrolyte rules that had already been counted as placeholders. The correct v0.2 figure was 20. Removing the severe-anaemia rule (A5) and the standalone bilirubin rule (A9) gives **18 fully specified rules**, now enumerated one by one in ruleset v0.3 §1.1. **This supersedes every earlier count in the package.** I introduced the error at v0.2 and it is corrected here.

**A9's boundary needed stating precisely, and does not do what it might appear to.** The removed rule is `HEP-U0-6` — new conjugated hyperbilirubinaemia at jaundice-range levels with abnormal enzymes — because it depended on a numeric bilirubin threshold HealthIQ would have had to invent, where UK guidance frames the trigger as *clinical* jaundice. The **Hy's law pattern is retained**: bilirubin there is expressed as a multiple of the reporting laboratory's own ULN inside a governed combination, not as a HealthIQ-set number. Bilirubin therefore remains an active Tier 0 constituent.

**A5 leaves a stated residual risk.** A haemoglobin of 55 g/L will not reach same day in this version. That is the accepted consequence of declining to invent a threshold where WHO explicitly declines to establish one for individual clinical use. It is recorded rather than buried, and it should be the first item put to specialist haematology.

---

## 3. Regulatory and legal items — all remain open

None has been closed and none may be closed by clinical or product authority.

| ID | Item | Blocking |
|---|---|---|
| **R1** | Tier 0 action-and-timeframe guidance — **18 fully specified rules**, all specification-only | **Yes for any Tier 0 release** |
| **R2** | Individual cardiovascular risk calculation — **quarantined** | Yes, that capability |
| **R3** | FIB-4 — **quarantined** | Yes, that capability |
| R4 | Consumer disease-name outputs | Yes |
| **R5** | Population exclusions and intended-purpose wording — **now includes the ratified pregnancy exclusion**, which enlarges this item | **Yes** |
| **R6** | Whether renal/electrolytes may be released with Tier 0 suppressed | **Yes** |

**R6 has become more consequential, not less.** The B2 adjudication lowers the same-day potassium threshold to >6.0, so HealthIQ will now identify **more** people with a life-threatening result it has no governed way to act on. Renal/electrolyte holds 8 of the 18 Tier 0 rules, six of them potentially life-threatening. Closing clinical questions has sharpened this one rather than easing it.

---

## 4. Questionnaire remediation — documented and deferred

The pregnancy questionnaire and runtime enforcement required by P7 **is not implemented**.

A defect in current questionnaire/runtime behaviour has been documented separately and is **deferred to a later full questionnaire rationalisation sprint**. It remains a **hard dependency for release**.

**No document in this package describes the questionnaire requirement as implemented.** Contract v0.6.1 §26.3 is retained as an **interim defensive provision** governing the unknown-status case, explicitly labelled as such, and it is not authority for operating without pregnancy status once enforcement exists.

This dependency blocks **release**. It does **not** block the clinical ruleset workstream, which is complete on this point: policy is ratified, all six domains have declared pregnancy materiality, and `pregnant` and `may_be_pregnant` are handled identically throughout.

The specifics of the defect are not characterised in this package because the audit was not supplied to this team.

---

## 5. Clinical ruleset workstream — current

The clinical ruleset workstream remains **current and unaffected** by the questionnaire dependency.

| Element | State |
|---|---|
| Six domain rulesets | Complete; conformance to contract v0.5 verified with no non-conformance found |
| Universal rules U1–U16 | Unchanged |
| Shared-marker ownership and boundaries | Unchanged |
| Cross-domain combination register XD-C1–C14 | Unchanged |
| Electrolyte bands | Incorporated |
| Tier 0 register | Corrected and enumerated — 18 |
| Unsafe-without-context register | 12 rules; UWC-11 and UWC-12 revised for the sex and ancestry ratifications |
| Acceptance-test matrix | Expanded from 21 to 27 scenarios, including 7 new tests of the fixed adjudications |
| Quarantined items | Vitamin D, FIB-4, cardiovascular risk |

**One documentation item outstanding:** the hepatic ruleset states it adopts v0.4 plus a summary and must be relabelled to v0.6.1. Non-blocking.

---

## 6. Contract disposition

**`HEALTHIQ_CLINICAL_FINDING_PRIORITISATION_CONTRACT_v0.6.1.md` issued.** A wording and status correction was required, so the conditional instruction to issue it is met.

Three corrections, none substantive:

1. **§26.2** — `pregnant` and `may_be_pregnant` are treated identically for clinical interpretation; no rule may distinguish between them.
2. **§26.3** — the unknown-pregnancy-status clause is reframed as an **interim defensive provision** pending enforcement, rather than a standing expectation, and explicitly records that enforcement is not implemented.
3. **§27.4** — sex is available by design; missing-sex provisions are a **defensive fail-closed fallback** for malformed or legacy requests only. Ancestry is not captured and no ancestry adjustment is authorised.

**v0.7 was not created.** No substantive new clinical policy was introduced — the four HMR adjudications operate within existing contract mechanisms (§13 documented adjudication, §18 prohibition on unauthorised placeholders), and the product ratifications required alignment of wording and status, not new policy.

---

## 7. Blocking summary

| Category | Blocking |
|---|---|
| Clinical | **B1** hepatic Tier 1 floor; **A8** vitamin D (that finding only) |
| Product | **None** |
| Regulatory/legal | **R1, R5, R6**; plus R2 and R3 for their specific capabilities |
| Implementation | Questionnaire enforcement — blocks release, not the clinical ruleset |

---

## VERDICT: READY_FOR_FINAL_INDEPENDENT_CONSISTENCY_REVIEW

Contract v0.6.1, consolidated ruleset v0.3 and adjudication register v0.2 are ready for one final independent cross-domain consistency review.

Every revision requested was made. Seven register items closed (A4, A5, A9, B2, P2, P7, P8), two placeholders removed rather than parked, the potassium threshold changed with its departure reason attached, the Tier 0 count corrected and enumerated definitively, and the pregnancy dependency recorded as deferred and explicitly not implemented.

Two clinical items remain open — B1 and A8 — and both are named, bounded and adjudicable rather than research questions. Neither prevents a consistency review, which is what "ready" means here: nothing in the package is being advanced toward release, and every capability that would be unsafe to release is quarantined or specification-only.

**Four things the consistency reviewer should target specifically.**

The **Tier 0 count of 18** should be verified against the six domain files individually. I introduced a counting error at v0.2 and corrected it here; the correction should be checked rather than trusted.

The **A9 boundary** — `XD-AS-23` and `XD-AS-23b` together test that the standalone bilirubin rule was removed without disturbing Hy's law. This is the revision most likely to have been implemented too broadly or too narrowly.

**`XD-AS-16`** — uncorrected calcium of 1.75 with no albumin produces insufficient data and **no finding**, despite sitting below every emergency threshold. This remains the hardest consequence of contract §8.1 and the one most likely to be argued with.

The **`[J]` label on hypernatraemia 146–154** should be confirmed as visible wherever the rule appears. It rests on my judgement, not on evidence, and it is the kind of label that quietly disappears as a document is reworked.
