---
document_id: HEALTHIQ_CROSS_DOMAIN_ACCEPTANCE_SCENARIO_APPROVAL_PACK
version: "1.2"
work_id: CLIN-PRIORITY-ACCEPTANCE-3
status: READY_FOR_ANTHONY_ACCEPTANCE_SCENARIO_APPROVAL
supersedes: HEALTHIQ_CROSS_DOMAIN_ACCEPTANCE_SCENARIO_APPROVAL_PACK_v1_1.md
historical_provenance:
  - HEALTHIQ_CROSS_DOMAIN_ACCEPTANCE_SCENARIO_APPROVAL_PACK_v1_0.md
  - HEALTHIQ_CROSS_DOMAIN_ACCEPTANCE_SCENARIO_MEDICAL_ADJUDICATION_v0_1.md
prepared_by: Claude Code (independent architecture and consistency reviewer)
scope: Self-contained consolidation of the complete active acceptance-scenario estate for the ratified Cross-Domain Clinical Prioritisation package, for contract §23.6 condition 7
self_contained: true
clinical_rules_amended: false
new_clinical_thresholds_created: false
anthony_approval_recorded: false
no_forced_lead_decision_status: PROPOSED_PENDING_ANTHONY_APPROVAL
implementation_authorised: false
cursor_prompt_authorised: false
---

# HealthIQ AI — Cross-Domain Clinical Prioritisation
## Acceptance Scenario Consolidation and Approval Pack v1.2 (Self-Contained)

## 1. Metadata and status

This is the final, self-contained acceptance-scenario approval pack. It supersedes v1.1 in full. An approver does not need to consult v1.0, v1.1, or the medical adjudication to know what is being approved — every active scenario's complete governed fields are reproduced in §7-§9 below. Those three documents remain cited as historical provenance only.

**This document corrects two defects in v1.1:**
1. v1.1 incorrectly recorded the no-forced-lead position as an Anthony product decision already made. It had not been separately ratified. This version identifies it as a **proposed** product decision, pending approval in the same act as the scenario estate (§3, §18).
2. v1.1 carried most scenario content forward by reference to v1.0. This version reproduces the complete active estate directly (§7-§9).

A third correction aligns the source-inventory wording for the six domain rulesets with their actual repository status (§4).

**This document does not record Anthony's approval of anything.** It presents the estate and the proposed product decision as ready for a single approval act and proposes the exact statement that act would require (§18). No decision is presumed.

## 2. Purpose and approval boundary

The purpose of this pack is to state whether the complete acceptance-scenario estate, together with one proposed product decision, is ready for Anthony's approval under **contract §23.6 condition 7**.

A single Anthony approval of this pack would:

- confirm the expected consolidated finding, urgency, severity treatment, tier, role, missing-data/indeterminate behaviour, override behaviour, and action class for each of the 109 scenarios in §7-§9;
- adopt the no-forced-lead product rule proposed in §3 and applied in `XD-AS-32`;
- **not** alter any clinical rule, threshold, band, override or adjudication;
- **not** close R1, R2, R3, R4, R5 or R6, or any other regulatory or legal dependency;
- **not** authorise Tier 0 activation;
- **not** authorise consumer-facing disease-name release;
- **not** authorise reliance on unresolved or unenforced questionnaire context;
- **not** authorise implementation, Cursor prompt authoring, or release.

Until that approval is given, every scenario below is a proposed specification, and the no-forced-lead rule is a proposed product decision, not governing behaviour.

## 3. Authority and supersession hierarchy

1. `HEALTHIQ_CLINICAL_FINDING_PRIORITISATION_CONTRACT_v0_6_3.md` — ratified clinical policy
2. `HEALTHIQ_CROSS_DOMAIN_CLINICAL_PRIORITISATION_RULESET_v0_5.md` — ratified cross-domain rules
3. `HEALTHIQ_CROSS_DOMAIN_HMR_ADJUDICATION_REGISTER_v0_4.md` — ratified closed adjudications
4. `HEALTHIQ_SIX_DOMAIN_CLINICAL_CLOSURE_REPORT_v0_4.md` — ratified package position
5. `HEALTHIQ_CROSS_DOMAIN_ACCEPTANCE_SCENARIO_MEDICAL_ADJUDICATION_v0_1.md` — `MEDICAL_ADJUDICATION_COMPLETE`; authoritative only for the bounded scenario clarifications it records; creates no new threshold and does not replace tiers 1-4
6. Six domain prioritisation rulesets — **subordinate domain evidence, each individually still `DRAFT_FOR_CENTRAL_RECONCILIATION` in its own front matter.** They are not, in themselves, ratified clinical authority. Their content is accepted into this pack **only** where it is incorporated, preserved, adjudicated, or left unchanged by tiers 1-4 above (§4).
7. `HEALTHIQ_CROSS_DOMAIN_PRODUCT_RATIFICATION_CLINICIAN_FIRST_v1_0.md` — `PRODUCT_RATIFIED` (Anthony, 2026-08-03); governs product-layer decisions only (lead selection, prominence, presentation), never clinical findings, severity, urgency or tier
8. `CLIN-PRIORITY-ARCH-HARDEN-1_cross_domain_prioritisation_architecture_hardening.md` — architecture-hardening verdict `HARDENED_READY_FOR_ANTHONY_ARCHITECTURE_APPROVAL`, approved by Anthony; governs architecture and Cursor-authoring gate status only

### Proposed product decision — pending Anthony approval, not yet ratified

The following is a **proposed** extension of clinician-first v1.0 §5-§6, drafted to resolve an edge case that document leaves open (three-or-more co-equal, non-same-day findings, no governed distinguisher). **Anthony has not yet separately approved this position.** It is presented here for approval in the same act as the scenario estate (§18):

> **Proposed:** for a case containing three or more equally ranked, non-same-day findings where no governed clinical distinguisher establishes a principal concern or a pair of co-leads: do not force a lead; do not manufacture two co-leads; retain all clinically distinct findings visibly within their governed tier; do not imply that one finding matters more where clinical authority does not support that conclusion. This applies only where no governed lead-selection rule resolves the case. The ordinary two-co-lead rule remains a maximum, not a requirement to designate two co-leads.

This proposal does not conflict with clinician-first v1.0 — it extends that document's own governing test (§3) and its existing prohibition on manufacturing co-lead status "merely to avoid making a difficult prioritisation decision" (§6) into a case that document does not explicitly resolve. `XD-AS-32` (§8) is drafted against this proposed rule. **`XD-AS-32`'s underlying clinical construction (three findings, their tiers, the absence of any governed distinguisher) is medically complete and not contingent on this proposal. Only the presentation consequence — no forced lead — depends on Anthony approving the proposal in §18.**

**Rule applied throughout this pack:** where a subordinate document states an outcome as unresolved or presents two candidate outcomes, and a document at a higher tier has since adjudicated that question, the higher-tier adjudication is the current authoritative expected outcome.

## 4. Source inventory

| Document | Version | Actual status | Role in this pack |
|---|---|---|---|
| Clinical Finding Prioritisation Contract | v0.6.3 | `CLINICALLY_RATIFIED_FOR_ARCHITECTURE_HARDENING` | Governing clinical policy |
| Cross-Domain Clinical Prioritisation Ruleset | v0.5 | `CLINICALLY_RATIFIED_FOR_ARCHITECTURE_HARDENING` | Source of `XD-AS-1` to `-30`; governing cross-domain rules |
| Cross-Domain HMR Adjudication Register | v0.4 | `CLINICALLY_RATIFIED_FOR_ARCHITECTURE_HARDENING` | Closed adjudications (A1-A10, B1-B7) |
| Six-Domain Clinical Closure Report | v0.4 | `CLINICALLY_RATIFIED_FOR_ARCHITECTURE_HARDENING` | Confirms no clinical adjudication remains open |
| Acceptance-Scenario Medical Adjudication | v0.1 | `MEDICAL_ADJUDICATION_COMPLETE` | Source of `XD-AS-31` to `-36`, `HAEM-AS-1` to `-6`, and the `RE-AS-11`/`HEP-AS-4`/`RE-AS-2`/`HEP-AS-10` corrections |
| Haematology Prioritisation Ruleset | v0.1 | **`DRAFT_FOR_CENTRAL_RECONCILIATION` — not itself ratified** | Subordinate domain evidence; its accepted content (taxonomy, bands) is governed through the ratified tiers 1-4 above |
| Hepatic Prioritisation Ruleset | v0.2 | **`DRAFT_FOR_CENTRAL_RECONCILIATION` — not itself ratified** | Subordinate domain evidence; hepatic Tier 1 floor is ratified at register B1, not by this ruleset's own authority |
| Renal and Electrolyte Prioritisation Ruleset | v0.1 | **`DRAFT_FOR_CENTRAL_RECONCILIATION`, verdict `REQUIRES_ADDITIONAL_DOMAIN_RESEARCH` for three electrolyte band sets — not itself ratified** | Subordinate domain evidence; potassium/sodium/calcium bands used here are ratified at register level (B2, A1-A4), not by this ruleset's own authority |
| Iron and Inflammatory Prioritisation Ruleset | v0.1 | **`DRAFT_FOR_CENTRAL_RECONCILIATION` — not itself ratified** | Subordinate domain evidence |
| Thyroid and Endocrine Prioritisation Ruleset | v0.1 | **`DRAFT_FOR_CENTRAL_RECONCILIATION` — not itself ratified** | Subordinate domain evidence |
| Cardiometabolic and Nutritional Prioritisation Ruleset | v0.1 | **`DRAFT_FOR_CENTRAL_RECONCILIATION` — not itself ratified** | Subordinate domain evidence |
| Product Ratification — Clinician-First Model | v1.0 | `PRODUCT_RATIFIED` | Product-layer authority; source of the co-lead-cap-as-ceiling rule |
| Architecture Hardening Report | `CLIN-PRIORITY-ARCH-HARDEN-1` | `HARDENED_READY_FOR_ANTHONY_ARCHITECTURE_APPROVAL`, approved by Anthony | Confirms architecture gate status |

**Correction applied in this version:** the six domain rulesets are described here strictly by their own recorded status (`DRAFT_FOR_CENTRAL_RECONCILIATION`), not as "ratified." Where this pack treats a domain ruleset's content as settled — e.g. the hepatic Tier 1 floor, the potassium/sodium/calcium bands, the haematology taxonomy — that content's actual governing authority is the ratified contract, ruleset, adjudication register or closure report (tiers 1-4), which has incorporated, adjudicated, or left it unchanged. No domain ruleset is cited here as if its own draft status were sufficient authority.

## 5. Changes from v1.1

1. **No-forced-lead position reclassified.** No longer presented as an Anthony decision already made. It is now a proposed product decision, explicitly pending approval, drafted for approval in the same act as the scenario estate (§3, §18).
2. **`XD-AS-32` status clarified.** Its clinical construction remains medically complete and unconditional. Its presentation consequence (no forced lead) is marked ready for approval **subject to** Anthony approving the proposed product decision in the same approval act (§8).
3. **Full self-containment.** All 109 active scenarios are reproduced with complete governed fields in §7-§9. No content requires consulting v1.0 or v1.1.
4. **Domain-ruleset authority wording corrected.** The six domain rulesets are described by their actual `DRAFT_FOR_CENTRAL_RECONCILIATION` status, not as ratified (§4).
5. **No clinical outcome, threshold, tier, scenario expectation, or dependency was altered.** Every field value in §7-§9 is identical in substance to v1.1; only presentation (self-containment) and the two corrections above have changed.

## 6. Scenario-normalisation method

Unchanged: each scenario carries a stable, domain-prefixed ID drawn from its authoritative source (the cross-domain ruleset for `XD-AS-1` to `-30`; the medical adjudication for `XD-AS-31` to `-36` and `HAEM-AS-1` to `-6`; the respective domain ruleset for all other domain-prefixed IDs). No panel, expected finding, tier, or governing citation has been altered from its authoritative source in producing this self-contained version.

## 7. Complete consolidated scenario matrix — cross-domain and contract fixture

Columns: ID | Inputs/context | Consolidated finding | Urgency | Severity/treatment | Tier | Role | Missing-data/indeterminate | Override/combination | Action/timeframe class | Prohibited behaviour | Dependency/quarantine

### 7.1 Contract hepatic regression fixture

| ID | Inputs | Finding | Urgency | Severity | Tier | Role | Missing-data | Override | Action class | Prohibited | Dependency |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `CONTRACT-FIX-1` | ALT 250 (5.1×ULN), ALP 46, R≈12.9, bilirubin/GGT normal, AST absent, MCV 99.5, transferrin mildly low | One consolidated hepatocellular enzyme elevation | Within days | Marked (5-10×ULN) | Tier 1 | Principal concern | Albumin/INR not assessable, stated; confidence reduced (AST absent), significance not reduced | n/a | Discuss/investigate | No urgent diagnostic claim from this fixture alone | None. **This scenario is identical in panel and outcome to `HEP-AS-1` (§7.3) — a confirmed literal duplicate, both retained for traceability: the contract cites it as the non-negotiable hepatic pilot regression fixture; the hepatic ruleset independently reproduces it.** |

### 7.2 Cross-domain scenarios (`XD-AS-*`), 39 active

| ID | Inputs | Finding | Urgency | Severity | Tier | Role | Missing-data/indeterminate | Override | Action class | Prohibited | Dependency |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `XD-AS-1` | K⁺6.8; ALT300(6.1×) | Two findings | Same day (both) | Not specified per-domain | Tier 0 (both) | Co-equal same-day group, no ordering | n/a | Same-day override on both | Immediate | No cross-domain severity comparison; K⁺ carries artefact wording | `TIER_0_PATHWAY_DEPENDENCY` (R1) |
| `XD-AS-1b` | K⁺6.2, else normal | Hyperkalaemia | Same day | Moderate (6.0-6.4) | Tier 0 | Principal concern | n/a | B2 adjudication (>6.0 same day) | Immediate | No mild-consequence language | `TIER_0_PATHWAY_DEPENDENCY` |
| `XD-AS-2` | Platelets 45; ALT 200 | Two findings | Not specified | Not specified | Tier 1 (haem primary) | Haematology primary below 50 boundary | n/a | Consolidation-boundary override | Discuss/investigate | Hepatic must not absorb below 50×10⁹/L | None |
| `XD-AS-3` | Platelets 120; ALT200; AST260 | One hepatic finding | Not restated | Marked | Tier 1 | Principal concern | n/a | XD-C1; platelets nested | Discuss/investigate | Platelets must not be double-counted as independent | None |
| `XD-AS-4` | Ferritin420; TSAT58%; ALT90 | Two findings | Not specified | Not specified | Tier 1 (both) | Independent secondary (iron not absorbed) | n/a | XD-C9 | Discuss/investigate | Hepatic must not absorb the overload concern | None |
| `XD-AS-5` | Ferritin1400; TSAT22%; ALT90 | One hepatic finding | Not specified | Not specified | Tier 1 | Principal concern | n/a | XD-C8; ferritin nested | Discuss/investigate | Magnitude must not promote ferritin to independent status | None |
| `XD-AS-6` | TSH14, freeT4 unavailable; LDL5.9 | Thyroid indeterminate + lipid secondary-cause | Within weeks | Indeterminate | Tier 1 | Dual role, one fact | Indeterminate — free T4 missing, both states named | XD-DUAL-1 | Discuss/investigate | Must not present as two concerns | None |
| `XD-AS-7` | TG24; Na⁺128 | Two findings | Same day (both) | Not specified | Tier 0 (both) | Co-equal, neither suppressed | n/a | XD-ARTEFACT-1 | Immediate | Sodium must carry pseudohyponatraemia caveat, not be suppressed | `TIER_0_PATHWAY_DEPENDENCY` |
| `XD-AS-8` | B12 110; Hb82; platelets88; ANC1.1 | One pancytopenia finding | Same day | Severe (3-lineage) | Tier 0 | Principal concern | n/a | XD-C5; B12 as aetiology | Immediate | Must not present three separate cytopenias | `TIER_0_PATHWAY_DEPENDENCY` |
| `XD-AS-9` | Calcium2.85, albumin absent; K⁺6.7 | Potassium finding + calcium insufficient-data | Same day (K⁺) | n/a (Ca) | Tier 0 (K⁺) | K⁺ lead; calcium alongside, not leading | Insufficient data (calcium) | n/a | Immediate (K⁺) | Calcium must not displace K⁺ lead nor be reported as normal | `TIER_0_PATHWAY_DEPENDENCY` |
| `XD-AS-10` | eGFR38 (no baseline); MCV104; CRP9; TSH5.8 | Renal Tier 1 + three Tier 2 findings | Within weeks (renal) | Not specified | Tier 1 (renal), Tier 2 (others) | Renal lead | AKI not assessable (renal) | XD-HEP-FLOOR-2 (non-export proof) | Discuss/investigate + monitor | No hepatic-style floor applied to MCV or CRP | None |
| `XD-AS-11` | Entirely normal broad panel | No-concern | n/a | n/a | n/a | n/a | n/a | n/a | Monitor/no action | Must not imply disease excluded beyond panel scope | None |
| `XD-AS-12` | K⁺6.8; platelets18; TG24 | Three findings | Same day (all) | Not specified | Tier 0 (all) | Three-member co-equal group | n/a | Same-day overrides ×3 | Immediate | No internal ranking within same-day group | `TIER_0_PATHWAY_DEPENDENCY` |
| `XD-AS-13` | K⁺2.3, no symptoms | Hypokalaemia | Same day | Severe (<2.5) | Tier 0 | Principal concern | n/a | n/a | Immediate | No mild-consequence language | `TIER_0_PATHWAY_DEPENDENCY` |
| `XD-AS-14` | Adjusted Ca²⁺2.05, no symptoms | Hypocalcaemia | Within weeks | Not specified band | Tier 1/2 | Principal concern | Symptom-conditional emergency statement mandatory | n/a | Discuss/investigate | Must state any level below range is emergency if symptomatic | None |
| `XD-AS-15` | Na⁺152, else normal | Hypernatraemia | Within days `[J]` | Mild (146-150) | Tier 1 | Principal concern | n/a | HYPERNA-J1 | Discuss/investigate | `[J]` label must travel with rule, not be upgraded downstream | None |
| `XD-AS-16` | Calcium1.75 uncorrected, albumin absent | Insufficient data | n/a | n/a | n/a | n/a | Insufficient data — no finding created | n/a | n/a | Must not create hypocalcaemia finding from uncorrected value | None |
| `XD-AS-17` | TC8.9, non-HDL7.2, full risk-factor set | Lipid finding | Within weeks | NICE threshold | Tier 1 | Principal concern | n/a | n/a | Investigate | No risk % computed or displayed | `REGULATORY_DEPENDENCY` (R2 quarantine) |
| `XD-AS-18` | ALT90, AST130, platelets135, age61 | Fibrosis finding | Within weeks | AST:ALT + platelets | Tier 1 | Principal concern | n/a | n/a | Investigate | FIB-4 not computed | `REGULATORY_DEPENDENCY` (R3 quarantine) |
| `XD-AS-19` | `may_be_pregnant`; ALT180, TSH6.2 | Out-of-scope/withheld | n/a | n/a | n/a | Visible, not suppressed | n/a | XD-PREG-1/2 | Specialist-rules-required | Must not silently suppress | `QUESTIONNAIRE_DEPENDENCY` |
| `XD-AS-20` | Hb108, sex present | Anaemia | Within weeks (implied) | Sex-specific threshold | Tier 1 | Principal concern | n/a | n/a | Discuss/investigate | n/a | None |
| `XD-AS-20b` | Hb108, sex absent (malformed) | Anaemia, indeterminate | Within weeks | Indeterminate | Tier 1 | Principal concern | Indeterminate; assumption stated, no silent default | n/a | Discuss/investigate | No silent default to a sex assumption | `QUESTIONNAIRE_DEPENDENCY` |
| `XD-AS-21` | K⁺3.2, Mg not measured | Hypokalaemia | Within weeks | Mild | Tier 2 | Principal concern | Magnesium requested as companion | XD-C14 | Monitor | n/a | None |
| `XD-AS-22` | Hb52, else normal FBC | Severe anaemia | Within days (not same day) | Severe | Tier 1 | Principal concern | n/a | Adjudicated decline (A5) | Discuss/investigate | Residual risk accepted per A5; no same-day claim | None |
| `XD-AS-23` | Bilirubin95, ALT/ALP/albumin normal | Isolated hyperbilirubinaemia | Within weeks (hepatic floor) | Not specified | Tier 1 | Principal concern | n/a | A9 (no Tier 0 bilirubin rule) | Discuss/investigate | No standalone bilirubin Tier 0 claim | None |
| `XD-AS-23b` | ALT200(4.1×), bilirubin2.4×ULN, ALP1.1×ULN | Hy's law pattern | Same day | Severe | Tier 0 | Principal concern | n/a | A9 boundary (Hy's law fires) | Immediate | n/a | `TIER_0_PATHWAY_DEPENDENCY` |
| `XD-AS-24` | ALT58(1.2×), else normal | One hepatic finding | Within weeks | Mild | Tier 1 | Principal concern | n/a | XD-HEP-FLOOR-1 | Discuss/investigate | Must not be described as urgent merely for entering Tier 1 | None |
| `XD-AS-25` | ALT250, ALP210, GGT180, bilirubin32, albumin normal | One hepatic concern, 4 nested constituents | Not specified | Not specified | Tier 1 | Principal concern | n/a | XD-HEP-FLOOR-1 | Discuss/investigate | Must not split into 4 separate concerns | None |
| `XD-AS-26` | Vitamin D18, calcium normal | Vitamin D deficiency | Routine | n/a | Tier 2 | Principal concern (sole finding) | n/a | XD-VITD-1 | Monitor | No supplementation dose; no Tier 1 escalation | None |
| `XD-AS-27` | Vitamin D38, calcium normal | No independent finding | n/a | n/a | n/a | Contextual only | n/a | XD-VITD-1 | n/a | Must not be described as proven deficiency | None |
| `XD-AS-28` | Vitamin D18, adjusted Ca²⁺2.05 | Calcium finding + nested vitamin D contributor | Per calcium band | Per calcium band | Per calcium tier | Calcium lead; vitamin D nested | n/a | XD-VITD-2 §9.2.1 | Per calcium action class | Vitamin D must not occupy separate Tier 2 slot | None |
| `XD-AS-29` | Vitamin D62, adjusted Ca²⁺2.05 | Calcium finding stands alone | Per calcium band | Per calcium band | Per calcium tier | Calcium lead; vitamin D not nested | n/a | XD-VITD-2 §9.2.3 | Per calcium action class | Vitamin D must not be nested as aetiological contributor | None |
| `XD-AS-30` | Vitamin D38, adjusted Ca²⁺2.05 | Calcium finding stands; vitamin D limited context | Per calcium band | Per calcium band | Per calcium tier | Calcium lead | n/a | XD-VITD-2 §9.2.2 | Per calcium action class | Must not describe as proven deficiency or established cause | None |
| `XD-AS-31` | K⁺6.2 mmol/L; creatinine, eGFR, other analytes normal | Hyperkalaemia (`RE-F3`) | Same day (urgency-derived tier 0) | Moderate (severity-derived tier 1) | **Tier 0 — more serious of the two governs** | Principal concern | n/a | n/a | Same day; mandatory artefact-safe wording (`RE-A-WORD-1`) | Must not cap same-day urgency at the moderate severity band | `TIER_0_PATHWAY_DEPENDENCY` |
| `XD-AS-32` | eGFR38 no prior; ferritin420/TSAT58%; TSH14/freeT4 low | Three findings: reduced eGFR undetermined chronicity (`RE-F10`); possible iron overload (`IRIN-F3`); overt hypothyroidism (`THY-F1`) | All within weeks | Not specified | All Tier 1 | **No lead forced; all three visible** — presentation consequence pending Anthony approval of the proposed product decision (§3) | Renal: AKI not assessable without prior creatinine (`UWC-2`) | n/a | Investigate (all three) | Must not select two co-leads by cross-domain severity comparison (§18.24); must not suppress the third to satisfy display convention | **`PRODUCT_DECISION_PENDING`** (§3, §18) — clinical construction is complete and unconditional |
| `XD-AS-33` | TSH14, freeT4 not measured, else normal | Indeterminate thyroid-axis abnormality (`THY-F5`) | Within weeks | Indeterminate | Tier 1 | Principal concern | Indeterminate — both states named (subclinical/overt), free T4 requested | n/a | Investigate | Must not infer worst case or default-low; must not suppress tier for missing modifier | None |
| `XD-AS-34` | Total calcium2.05, albumin not measured, else normal | None for calcium — insufficient data | n/a | n/a | n/a | n/a | Insufficient data; albumin named as required modifier | n/a | n/a | Must not create finding from uncorrected value; must not report as normal | None |
| `XD-AS-35` | K⁺6.8, no repeat, eGFR55 | Hyperkalaemia with renal impairment (`RE-F9`) | Same day | Severe | **Tier 0 (clinical classification, made regardless of release state)** | Principal concern | n/a | n/a | Same-day guidance **withheld** — finding itself visible | Must not downgrade to Tier 1/2; must not present as no-concern or omit the finding | `TIER_0_PATHWAY_DEPENDENCY` (R1) |
| `XD-AS-36` | Ferritin420, TSAT58%, hepatic analytes normal | Possible iron overload (`IRIN-F3`) | Within weeks | Not specified | Tier 1 | Principal concern | n/a | `IRIN-OV-1` | Investigate | Must not name haemochromatosis or imply genetic diagnosis to the consumer; permitted internally in provenance/clinician material | `REGULATORY_DEPENDENCY` (R4) |

## 8. Formal domain scenarios — haematology (`HAEM-AS-*`), 6 active

Formalises and supersedes `HAEM-EX-1` to `-6` (retirement record: §10).

| ID | Inputs | Finding | Urgency | Severity | Tier | Role | Missing-data/indeterminate | Override | Action class | Prohibited | Dependency |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `HAEM-AS-1` | Platelets18×10⁹/L; Hb128g/L(M); MCV92fL | Severe thrombocytopenia (`HAEM-F4`) | Same day | Severe (<20) | Tier 0 | Principal concern; Hb128 forms a separate mild finding, does not compete | None; no film — standing limitation stated | None fired (`HAEM-OV-4` inapplicable — no thrombosis/renal impairment) | Immediate; pseudothrombocytopenia confirmation mandatory | Must not assert the count is genuine or artefact without repeat | `TIER_0_PATHWAY_DEPENDENCY` |
| `HAEM-AS-2` | Hb95g/L; MCV78fL; platelets normal | Anaemia, microcytic subtype — one finding (`HAEM-F1` via `HAEM-OV-6`) | Within weeks | No severity sub-band exists (A5 declined) | Tier 1 | Principal concern; MCV is a constituent, not separate | Ferritin, if absent, stated as not assessable | `HAEM-OV-6` | Further investigation | Anaemia must not appear twice with iron domain (U15) | None |
| `HAEM-AS-3` | MCV99.5fL; remainder of FBC normal | Isolated macrocytosis (`HAEM-F2`) | Routine | Mild macrocytosis | **Tier 2, unconditionally** | Role determined by wider panel: principal concern if no higher-tier finding exists elsewhere; contextual if a hepatic/nutritional parent exists within the mild-band boundary | None | `HAEM-OV-3` does not fire (no other FBC abnormality) | Monitor/planned reassessment | **The hepatic Tier 1 floor must not be applied here** (`XD-HEP-FLOOR-2` — load-bearing anti-universalisation counterexample) | None |
| `HAEM-AS-4` | MCV99.5fL; platelets140×10⁹/L; Hb118g/L(F) | Multi-lineage cytopenia — one finding (`HAEM-F10`) | Within days | Individually low-tier; combination governs | Tier 1 | Principal concern; individual cytopenias are constituents, not separate concerns | No film — standing limitation, stated | `HAEM-OV-1` (two lineages reduced) | Further investigation | Must not present as three separate low-tier findings | None |
| `HAEM-AS-5` | ANC0.4×10⁹/L; remainder of FBC normal | Severe neutropenia (`HAEM-F6`) | Same day | Severe (<0.5) | Tier 0 | Principal concern | Ancestry not captured, no adjustment made (`XD-ANC-1`), limitation stated | None | Immediate | Must not adjust band for presumed ancestry without governed data | `TIER_0_PATHWAY_DEPENDENCY` |
| `HAEM-AS-6` | Total WCC3.1×10⁹/L; no differential; remainder of FBC normal | **Two coexisting states**: (1) low total WCC — valid finding; (2) neutrophil question — insufficient data | (1) Within weeks | (1) Not specified; (2) n/a | (1) Tier 1; (2) n/a | Principal concern (state 1) | (2) Insufficient data — absolute differential required to answer the neutrophil question (contract §8.1; `HAEM-IND-2`) | None | Further investigation; repeat with differential | Must not report neutrophils as normal or infer count from total; must not suppress either state | None |

## 9. Complete consolidated scenario matrix — remaining domains

### 9.1 Hepatic (`HEP-AS-*`), 14 active

| ID | Inputs | Finding | Urgency | Severity | Tier | Role | Missing-data/indeterminate | Override | Action class | Prohibited | Dependency |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `HEP-AS-1` | = `CONTRACT-FIX-1` (§7.1) | Same as `CONTRACT-FIX-1` | Within days | Marked | Tier 1 | Principal concern | Albumin/INR not assessable | n/a | Discuss/investigate | No urgent diagnostic claim | None — confirmed duplicate of `CONTRACT-FIX-1` |
| `HEP-AS-2` | Same + albumin28 | Synthetic dysfunction (`HEP-F4`) | Same day | Severe | Tier 0 | Principal concern (`HEP-LEAD-1`) | n/a | n/a | Immediate; albumin non-hepatic-cause caveat mandatory | Must not assert albumin cause is hepatic without exclusion | `TIER_0_PATHWAY_DEPENDENCY` |
| `HEP-AS-3` | ALT550(11.2×), else normal | Hepatocellular, severe | Same day | Severe (≥10×) | Tier 0 | Principal concern | n/a | n/a | Immediate | n/a | `TIER_0_PATHWAY_DEPENDENCY` |
| `HEP-AS-4` **(corrected)** | ALT60(1.2×), isolated | Hepatocellular, mild | Within weeks | Mild | **Tier 1 only** (HEP-U1 closed literal; no Tier 2 alternative) | Principal concern | n/a | HEP-P2 | Discuss/investigate | **Must not be described as urgent merely because the hepatic Tier 1 floor applies** (`XD-HEP-FLOOR-1` point 4) | None |
| `HEP-AS-5` | ALP240(2.1×), GGT normal, ALT normal | Reclassified `HEP-F7`, non-hepatic origin | Not specified | Significant ALP band | Own floor retained | Reclassified, not suppressed | n/a | n/a | Investigate (non-hepatic) | Must not assume hepatic origin without GGT support | None |
| `HEP-AS-6` | Bilirubin38 isolated, no anaemia | Gilbert's pattern | Routine | n/a | Tier 2 | Principal concern | Split-bilirubin caveat if unmeasured | n/a | Reassurance available | Must not assert Gilbert's without conjugated fraction | None |
| `HEP-AS-7` | Bilirubin38 isolated, Hb low | Different finding from `HEP-AS-6` | Within weeks | Not specified | Tier 1 | Principal concern | n/a | n/a | Discuss/investigate | Haemolysis must be considered, not dismissed | None |
| `HEP-AS-8` | Ferritin1400, TSAT22%, ALT90 | Hepatic Tier 1; ferritin contextual | Within weeks | Not specified | Tier 1 | Principal concern | n/a | n/a | Discuss/investigate | Magnitude must not promote ferritin | None |
| `HEP-AS-9` | Ferritin420, TSAT58%, ALT90 | Two Tier 1 findings | Within weeks (both) | Not specified | Tier 1 (both) | Co-lead eligible | n/a | n/a | Discuss/investigate | n/a | None |
| `HEP-AS-10` **(corrected)** | ALT30, AST45, platelets130, age58 | `HEP-F5` fibrosis via AST:ALT ratio and platelets | Within weeks | AST:ALT>1 + platelets | Tier 1 | Principal concern | n/a | n/a | Investigate | **FIB-4 is not computed. FIB-4 is not displayed. Quarantine removes the calculation, not the finding** (`XD-QUAR-1`) | `REGULATORY_DEPENDENCY` (R3) |
| `HEP-AS-11` | ALT250, ALP absent | `HEP-F9`, pattern undetermined | Not specified | By severity alone | Tier 1 | Principal concern | Pattern not assessable (R not computed) | n/a | Discuss/investigate | Must not be called hepatocellular without ALP | None |
| `HEP-AS-12` | Complete normal hepatic panel | No-concern | n/a | n/a | n/a | n/a | Must state normal enzymes don't exclude fibrosis/cirrhosis | n/a | Monitor | Must not state liver is "healthy" | None |
| `HEP-AS-13` | ALT250, MCV118 | Two findings | Not specified | Not specified | Tier 1 (both) | MCV not contextual (above mild band) | n/a | n/a | Discuss/investigate | Must not attach MCV as context above the mild band | None |
| `HEP-AS-14` | ALT250, platelets35 | Two findings | Not specified | Not specified | Tier 1 (hepatic); haem same-day-eligible | Haematology leads on time band | n/a | n/a | Discuss/investigate + haem urgency | Platelets must not be absorbed below the 50 boundary | None |

### 9.2 Renal/electrolyte (`RE-AS-*`), 14 active

| ID | Inputs | Finding | Urgency | Severity | Tier | Role | Missing-data/indeterminate | Override | Action class | Prohibited | Dependency |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `RE-AS-1` | K⁺6.8, no repeat, eGFR55 | `RE-F9` | Same day | Severe | Tier 0 | Principal concern | n/a | `RE-OV-2` | Immediate; mandatory artefact-safe wording | Must not assert genuine or artefact without repeat | `TIER_0_PATHWAY_DEPENDENCY` |
| `RE-AS-2` **(corrected)** | K⁺6.2, eGFR88 | Hyperkalaemia | Same day (per closed B2) | Moderate | **Tier 0 only** | Principal concern | n/a | n/a | Immediate | Tests the clinical threshold; overlaps `XD-AS-31` (which tests the tier algebra) — both retained | `TIER_0_PATHWAY_DEPENDENCY` |
| `RE-AS-3` | Creatinine145, prior70 six days ago | AKI | Same day | ≥50% rise/7d (NICE) | Tier 0 | Principal concern | n/a | `RE-OV-3` | Immediate | n/a | `TIER_0_PATHWAY_DEPENDENCY` |
| `RE-AS-4` | Creatinine145, no prior | `RE-F10` | Within weeks (from eGFR category) | Not specified | Tier 1 | Principal concern | AKI not assessable | n/a | Investigate | Must not be presented as chronic | None |
| `RE-AS-5` | eGFR52, prior54 four months ago | Stable CKD G3a | Routine | G3a | Tier 2 | Principal concern | ACR unavailable — staging incomplete, stated | n/a | Monitor | n/a | None |
| `RE-AS-6` | eGFR72, no other markers | Not CKD | n/a | n/a | n/a/Tier 3 context | n/a | n/a | `RE-U-NEG-1` | n/a | Must not classify eGFR60-89 as CKD without other markers | None |
| `RE-AS-7` | Calcium2.85, albumin absent | Insufficient data | n/a | n/a | n/a | n/a | Insufficient data — not a finding, not suppression | `RE-OV-9` | n/a | Must not present uncorrected calcium as a finding | None |
| `RE-AS-8` | Calcium2.85, albumin40→adjusted2.83 | Mild hypercalcaemia | Within days | Mild | Tier 1 | Principal concern | Albumin as modifier | n/a | Discuss | n/a | None |
| `RE-AS-9` | Sodium122 | Profound hyponatraemia | Same day | Profound | Tier 0 | Principal concern | Chronicity unknown, stated | n/a | Immediate | n/a | `TIER_0_PATHWAY_DEPENDENCY` |
| `RE-AS-10` | Sodium131 | Mild hyponatraemia | Within weeks `[J]` | Mild | Tier 1 | Principal concern | n/a | `RE-U-W-2` | Investigate | Deliberate departure from UK "no investigation" guidance, `[J]`-labelled | None |
| `RE-AS-11` **(corrected)** | Urea12 mmol/L, creatinine/eGFR normal | **None.** Urea does not form an independent finding (`RE-CONS-3` governs over the incidental `RE-U-W-4` band listing) | Not applicable — no finding, no urgency band | Not applicable | **Tier 3 — contextual** | **Contextual information** (clinician-first §8) | None triggered; urea has no governed modifier | None | **None** — no action class assigned to a Tier 3 contextual item | Must not be presented as renal impairment or renal failure (renal ruleset §17 item 9); must not be assigned an independent tier or action | None — orphan handling per contract §6.5: distinct low-prominence contextual group, reconcilable with the raw value. Does not resolve open `RE-U5`; no urea:creatinine combination rule created (§14 of this pack) |
| `RE-AS-12` | K⁺6.8 and ALT300(6.1×) | Same-day co-equal group | Same day (both) | Not specified | Tier 0 (both) | Co-equal, no ordering | n/a | n/a | Immediate | No cross-domain severity comparison | `TIER_0_PATHWAY_DEPENDENCY` |
| `RE-AS-13` | eGFR40, platelets45 | Two findings | Not specified | Not specified | Tier 1 (renal); haem same-day-eligible | Haematology primary | n/a | `RE-OV-7` | Investigate + haem urgency | n/a | None |
| `RE-AS-14` | Complete normal renal/electrolyte panel | No-concern | n/a | n/a | n/a | n/a | Must state AKI could not be assessed without prior | n/a | Monitor | Must not state kidneys "working normally" | None |

### 9.3 Iron/inflammatory (`IRIN-AS-*`), 12 active

| ID | Inputs | Finding | Urgency | Severity | Tier | Role | Missing-data/indeterminate | Override | Action class | Prohibited | Dependency |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `IRIN-AS-1` | Ferritin1400, TSAT22% | `IRIN-F4` | Routine | TSAT-determined, low | Tier 2 | Principal concern | n/a | `IRIN-OV-2` | Monitor | Must not present overload concern given low TSAT | None |
| `IRIN-AS-2` | Ferritin420, TSAT58% | `IRIN-F3` | Within weeks | TSAT-determined, higher | Tier 1 | Principal concern | n/a | `IRIN-OV-1` | Investigate/specialist | Magnitude must not determine severity over TSAT | None |
| `IRIN-AS-3` | Ferritin900, TSAT absent, iron+TIBC present | Computed TSAT, then `IRIN-AS-1`/`-2` path | Depends on computed value | Depends | Depends | Principal concern | TSAT derived, labelled as such | `IRIN-MOD-1` | Depends | Must not report TSAT as missing when derivable | None |
| `IRIN-AS-4` | Ferritin900, TSAT absent, iron+TIBC absent | `IRIN-F8` | Within weeks | Indeterminate | Tier 1 | Principal concern | Indeterminate; both states stated, TSAT requested | n/a | Investigate | Must not default to inflammatory | None |
| `IRIN-AS-5` | Ferritin45 (in range), CRP60, Hb105 | `IRIN-F5` | Within weeks | Not specified | Tier 1 | Principal concern | Not reported as normal despite in-range value | `IRIN-OV-4` | Investigate | Must not report iron status as normal | None |
| `IRIN-AS-6` | Ferritin8, Hb98, MCV72 | One consolidated iron-deficiency-anaemia finding | Within weeks | Not specified | Tier 1 | Principal concern (with haematology) | n/a | `IRIN-OV-3` | Investigate | Must not create a separate haematology finding | None |
| `IRIN-AS-7` | CRP12, else normal | Contextual/low-specificity | Routine | Not specified | Tier 2 | Principal concern | n/a | n/a | Monitor | Must not escalate to Tier 1 (anti-universalisation) | None |
| `IRIN-AS-8` | CRP12 ×3 over 9 months | `IRIN-F7` | Within weeks | Persistence-based | Tier 1 | Principal concern | n/a | n/a | Investigate | Height alone must not promote; persistence does | None |
| `IRIN-AS-9` | CRP60, platelets40 | Haematology primary, same-day | Same day (haem) | Not specified | Tier 0 (haem) | CRP contextual | n/a | `IRIN-OV-5` | Immediate (haem) | n/a | `TIER_0_PATHWAY_DEPENDENCY` |
| `IRIN-AS-10` | Ferritin1100, ALT120, TSAT30% | Hepatic finding leads; ferritin contextual | Not specified | Not specified | Tier 1 (hepatic) | Hepatic lead | n/a | `IRIN-OV-6` | Investigate | n/a | None |
| `IRIN-AS-11` | Ferritin1100, ALT120, TSAT55% | Two findings | Not specified | Not specified | Tier 1 (both) | Independent secondary (not absorbed) | n/a | `IRIN-OV-7` | Investigate | Hepatic must not absorb the overload concern | None |
| `IRIN-AS-12` | Complete normal iron panel, CRP normal | No-concern | n/a | n/a | n/a | n/a | Normal ferritin doesn't exclude deficiency w/ inflammation | n/a | Monitor | Must not state iron levels are "fine" if CRP raised/absent | None |

### 9.4 Thyroid/endocrine (`THY-AS-*`), 12 active

| ID | Inputs | Finding | Urgency | Severity | Tier | Role | Missing-data/indeterminate | Override | Action class | Prohibited | Dependency |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `THY-AS-1` | TSH14, freeT4 8 (low) | `THY-F1` overt hypothyroid | Within weeks | Overt | Tier 1 | Principal concern | n/a | `THY-OV-1` | Treat | n/a | None |
| `THY-AS-2` | TSH14, freeT4 15 (normal) | `THY-F2`, TSH≥10 | Within weeks | Intermediate | Tier 1 | Principal concern | n/a | `THY-OV-2` | Treatment-consideration | NICE two-occasion requirement must be stated | None |
| `THY-AS-3` | TSH6.2, freeT4 15 (normal) | `THY-F2`, TSH<10 | Routine | Lower | Tier 2 | Principal concern | n/a | n/a | Repeat/discuss | n/a | None |
| `THY-AS-4` | TSH14, freeT4 unavailable | `THY-F5` indeterminate | Within weeks | Indeterminate | Tier 1 | Principal concern | Both states named; free T4 requested; may not default to subclinical | n/a | Investigate | No worst-case or default-low inference | None |
| `THY-AS-5` | TSH<0.01, freeT4 32 (raised) | `THY-F3` overt hyperthyroid | Within weeks | Overt | Tier 1 | Principal concern | n/a | `THY-OV-3` | Treat | n/a | None |
| `THY-AS-6` | TSH<0.01, freeT4 18 (normal), freeT3 unavailable | `THY-F4` with `THY-IND-3` | Within weeks | Not gradable numerically | Tier 1 | Principal concern | T3-toxicosis not assessable | n/a | Investigate | n/a | None |
| `THY-AS-7` | TSH12, freeT4 28 (both raised) | `THY-F6` discordant | Within days | Not gradable | Tier 1 | Principal concern | n/a | `THY-OV-4` | Specialist interpretation | Must not be auto-explained | None |
| `THY-AS-8` | TSH6.5, freeT4 normal, TPO positive | `THY-F2` | Routine | Lower | Tier 2 | Principal concern | Antibodies contextual | n/a | Discuss | Must not present TPO as independent finding | None |
| `THY-AS-9` | TSH14, freeT4 low, pregnancy known | Domain suppressed | n/a | n/a | n/a | Withheld, visible | n/a | `THY-OV-7` | Specialist-rules-required | Must not silently suppress | `QUESTIONNAIRE_DEPENDENCY` |
| `THY-AS-10` | TSH8, freeT4 normal, LDL5.8 | Dual role: `THY-F2` + lipid secondary-cause context | Routine (thyroid) | Lower | Tier 2 (thyroid) | Dual role, one fact | n/a | `THY-OV-5` | Discuss | Must not present as two separate concerns | None |
| `THY-AS-11` | TSH8, freeT4 normal, MCV104, else normal FBC | `THY-F2` + macrocytosis context | Routine | Lower | Tier 2 | Dual role | n/a | `THY-OV-6` | Discuss | n/a | None |
| `THY-AS-12` | Normal TSH and freeT4 | No-concern | n/a | n/a | n/a | n/a | Biotin/illness distortion caveat | n/a | Monitor | Must not state thyroid is "normal" without caveat | None |

### 9.5 Cardiometabolic/nutritional (`CN-AS-*`), 12 active

| ID | Inputs | Finding | Urgency | Severity | Tier | Role | Missing-data/indeterminate | Override | Action class | Prohibited | Dependency |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `CN-AS-1` | TG24, HbA1c40, no alcohol data | Severe hypertriglyceridaemia | Same day | Severe | Tier 0 | Principal concern | HbA1c excludes poor glycaemic control; alcohol unassessed, stated | `CN-OV-1` | Immediate; pancreatitis framing mandatory | Must not frame as cardiovascular urgency | `TIER_0_PATHWAY_DEPENDENCY` |
| `CN-AS-2` | TG24, HbA1c78 | Same, reframed | Same day | Severe | Tier 0 (not downgraded) | Principal concern | Dysglycaemia as plausible secondary cause | `CN-OV-5` | Immediate | Must not downgrade despite secondary cause | `TIER_0_PATHWAY_DEPENDENCY` |
| `CN-AS-3` | TC9.4, non-HDL7.8, no family history | Lipid finding | Within weeks | NICE threshold | Tier 1 | Principal concern | Applies regardless of family history | `CN-OV-2` | Specialist assessment | n/a | None |
| `CN-AS-4` | TC7.9, no family history/risk factors | `CN-F9` indeterminate risk | Routine | Not computable | Tier 2 | Principal concern | FH not assessable, stated | n/a | Monitor | n/a | None |
| `CN-AS-5` | LDL5.2, HDL1.1, TC7.2, TG1.8 | One lipid finding | Not specified | Not specified | Tier 2 | Principal concern | n/a | n/a | Monitor | Must not present four separate fraction concerns; non-HDL preferred to LDL | None |
| `CN-AS-6` | HbA1c52, single result | Dysglycaemia | Within weeks | Diagnostic range | Tier 1 | Principal concern | Diagnosis not assertable — confirmation required | n/a | Investigate | Must not assert diabetes diagnosis from single result | None |
| `CN-AS-7` | B12 120, Hb98, MCV112 | One consolidated finding with haematology | Within weeks | Not specified | Tier 1 | Principal concern (with haematology) | n/a | `CN-OV-6` | Investigate | n/a | None |
| `CN-AS-8` | B12 320 (in range), MCV108, normal Hb | `CN-F7` | Within weeks | Not specified | Tier 1 | Principal concern | In-range value, real finding (contract §3.1) | `CN-OV-8` | Investigate | Must not report B12 as normal given context | None |
| `CN-AS-9` | B12 110, Hb82, platelets90, neutrophils1.2 | Haematology primary and same-day | Same day (haem) | Severe (pancytopenia) | Tier 0 (haem) | B12 aetiology within finding | n/a | `CN-OV-7` | Immediate (haem) | Must not present B12 as a competing concern | `TIER_0_PATHWAY_DEPENDENCY` |
| `CN-AS-10` | TC8.8, TSH12, freeT4 low | Lipid reframed; both findings stand | Within weeks (thyroid leads on actionability) | Not specified | Tier 1 (both) | Thyroid leads within band | n/a | `CN-OV-5` | Treat thyroid; investigate lipid | n/a | None |
| `CN-AS-12` | TG24 and K⁺6.8 | Same-day co-equal group | Same day (both) | Not specified | Tier 0 (both) | Co-equal, no ordering | n/a | n/a | Immediate | No cross-domain severity comparison | `TIER_0_PATHWAY_DEPENDENCY` |
| `CN-AS-13` | Complete normal lipid and nutritional panel | No-concern | n/a | n/a | n/a | n/a | Normal lipid doesn't exclude CV risk; normal B12 doesn't exclude functional deficiency | n/a | Monitor | Must not state cholesterol is "fine" or heart risk is "low" | None |

**Note:** `CN-AS-11` does not appear above. It is retired, not renumbered — see §10.

## 10. Retired, replaced and duplicate scenario register

| Status | Scenario(s) | Reason | Current scenario of record |
|---|---|---|---|
| Confirmed literal duplicate (both retained) | `CONTRACT-FIX-1` = `HEP-AS-1` | Identical panel, identical outcome | Both — contract cites the pilot regression fixture; hepatic ruleset independently reproduces it |
| Retired, superseded | `HAEM-EX-1` to `-6` (informal) | Replaced by formal scenarios with complete fields; no change in underlying clinical result | `HAEM-AS-1` to `-6` (§8) |
| Retired, superseded (basis changed, not relabelled) | `CN-AS-11` | Premise ("no governed vitamin D threshold exists") is medically stale — A8 closed a governed threshold before this scenario's premise was written | `XD-AS-26` (§7.2, unchanged) |
| Corrected in place (same ID) | `HEP-AS-4`, `RE-AS-2`, `RE-AS-11`, `HEP-AS-10` | Stale or incomplete wording aligned to already-closed adjudications | Same IDs, §9.1-§9.2, corrected text |

## 11. Coverage matrix against all 26 mandatory behaviours

| # | Mandatory behaviour | Covering scenario(s) | Status |
|---|---|---|---|
| 1 | Interpretability before prioritisation | `HEP-AS-11`, `RE-AS-7`, `XD-AS-33` | Covered |
| 2 | Domain-specific severity bands | `HEP-AS-3`, `RE-AS-1`/`XD-AS-31`, `IRIN-AS-1`/`-2`, `THY-AS-2`, `CN-AS-3`/`-4` | Covered |
| 3 | Urgency independently from severity | `CONTRACT-FIX-1`/`HEP-AS-1`, `XD-AS-31` | Covered |
| 4 | "More serious tier wins" | `XD-AS-31` | Covered |
| 5 | Consolidation before prioritisation | `HEP-AS-1`, `XD-AS-25`, `CN-AS-5` | Covered |
| 6 | Same-domain frame consolidation | `XD-AS-25`, `CN-AS-5`, `HAEM-AS-2`/`-4` | Covered |
| 7 | Cross-domain duplicate consolidation | `XD-AS-4`/`-5`, `IRIN-AS-10`/`-11`, `HEP-AS-8`/`-9` | Covered |
| 8 | Direct finding vs contextual/phenotype | `XD-AS-10`, `HEP-AS-13`, `HAEM-AS-3` | Covered |
| 9 | Independent secondary concerns | `XD-AS-4`, `RE-AS-13`, `IRIN-AS-11` | Covered |
| 10 | Ordinary co-lead behaviour | `HEP-AS-9` | Covered |
| 11 | Same-day co-equal concern groups | `XD-AS-1`/`-7`/`-12`, `RE-AS-12`, `CN-AS-12` | Covered |
| 12 | Ordinary two-co-lead cap below same-day band | `XD-AS-32` | Covered (clinical construction complete; presentation consequence pending §3/§18) |
| 13 | Supporting-marker nesting | `HEP-AS-8`, `XD-AS-3`/`-28` | Covered |
| 14 | Modifiers that change urgency/severity | `RE-AS-8`, `IRIN-AS-3` | Covered |
| 15 | Override behaviour | `HAEM-AS-1`/`-4`/`-5`, various `RE-OV`/`IRIN-OV` entries | Covered |
| 16 | Insufficient-data behaviour | `RE-AS-7`, `XD-AS-9`/`-16`/`-34` | Covered |
| 17 | Indeterminate-severity behaviour | `THY-AS-4`, `HEP-AS-11`, `XD-AS-33` | Covered |
| 18 | Missing modifiers, no worst-case inference | `XD-AS-33`, `XD-AS-34`, `HAEM-AS-6` | Covered |
| 19 | Pregnancy-dependent suppression/limitation | `XD-AS-19`, `THY-AS-9` | Covered |
| 20 | Sex-dependent interpretation | `XD-AS-20`/`-20b` | Covered |
| 21 | No-concern output | `XD-AS-11`, `HEP-AS-12`, `RE-AS-14`, `IRIN-AS-12`, `THY-AS-12`, `CN-AS-13` | Covered |
| 22 | Tier 0 specification-only and withheld behaviour | All Tier 0 scenarios; `RE-AS-1`, `HEP-AS-2`/`-3` | Covered |
| 23 | Tier 0 non-downgrade behaviour | `XD-AS-35` | Covered |
| 24 | Quarantined disease-name, FIB-4, CV-risk capabilities | `XD-AS-17` (CV-risk), `XD-AS-18`/`HEP-AS-10` (FIB-4), `XD-AS-36` (disease-name) | Covered |
| 25 | Hepatic pilot regression behaviour | `CONTRACT-FIX-1`/`HEP-AS-1` | Covered |
| 26 | Clinician-first lead selection across unlike domains | `XD-AS-1`/`-7`/`-12`, `XD-AS-32`, product ratification §3-§9 | Covered |

**All 26 mandatory behaviours remain explicitly covered.** Behaviour #12's covering scenario (`XD-AS-32`) has a clinically complete, unconditional construction; only its presentation consequence depends on the pending product-decision approval (§3), which does not reduce it to an uncovered behaviour — the expected clinical output (three visible Tier 1 findings, no forced ranking) is deterministic either way.

## 12. Contradiction-resolution record

| # | Conflict | Resolution | Authority |
|---|---|---|---|
| 1 | `HEP-AS-4` presented two outcomes | Corrected to Tier 1 only | `HEP-U1` closed (register B1) |
| 2 | `RE-AS-2` presented two outcomes | Corrected to Tier 0 only | `RE-U1` closed (register B2) |
| 3 | `CN-AS-11` contradicted `XD-AS-26` | `CN-AS-11` retired, not relabelled | A8 closed |
| 4 | `RE-AS-11`'s `RE-CONS-3` vs `RE-U-W-4` | `RE-CONS-3` (categorical taxonomy) governs over `RE-U-W-4` (incidental band listing); orphan handling per contract §6.5 | Medical adjudication §5 |
| 5 | `HAEM-EX-6` conflated indeterminate and insufficient-data into one entry | Disambiguated into two coexisting states in `HAEM-AS-6` | Medical adjudication §11 |
| 6 | `HAEM-EX-3`'s "no lead" framing conflated tier with role | Tier (2, unconditional) separated from role (panel-dependent) in `HAEM-AS-3` | Medical adjudication §11 |

**Zero unresolved clinical conflicts remain.**

## 13. Dependency register

| Class | Items |
|---|---|
| `REGULATORY_DEPENDENCY` | Disease-name release (R4, `XD-AS-36`); population exclusions/intended-purpose wording (R5); renal/electrolyte release with Tier 0 suppressed (R6); FIB-4 (R3, `XD-AS-18`/`HEP-AS-10`); CV-risk calculation (R2, `XD-AS-17`) |
| `TIER_0_PATHWAY_DEPENDENCY` (R1) | Every Tier 0 scenario listed in §7-§9 — specification approvable now; activation blocked pending the contract §17 pathway |
| `QUESTIONNAIRE_DEPENDENCY` | `XD-AS-19`, `XD-AS-20b`, `THY-AS-9` — specification approvable; operational reliance on the pregnancy-known path is not currently reachable through the canonical questionnaire |
| `PRODUCT_DECISION_PENDING` | `XD-AS-32`'s presentation consequence (no forced lead) — pending Anthony's approval of the proposed product decision in §3/§18. This is the only item in the estate pending a decision rather than merely pending activation/release of an already-decided specification. |

Approval of a scenario confirms its specification only. None of the above is closed by that approval.

## 14. Non-blocking carry-forward register

| Item | Nature | Why non-blocking |
|---|---|---|
| Governed urea:creatinine combination rule | Future medical enhancement, deliberately not created | `RE-AS-11` is fully resolved without it |
| `RE-U5` (whether urea ever forms an independent finding with clinical context) | Open clinical research question | Unaffected by `RE-AS-11`'s resolution |
| Hepatic ruleset relabel to v0.6.3 | Documentation/administrative | Later cross-domain authority already governs regardless of label |
| Questionnaire rationalisation and enforcement remediation | Implementation, deferred | Blocks release and runtime reliance on questionnaire context, not scenario approval |
| Regulatory/legal release dependencies (R1-R6) | External authority | Blocks activation/release of the associated capability, not the specification |

## 15. Scenarios ready for Anthony's approval

**All 109 unique active scenarios**, reproduced in full in §7-§9, are ready for approval. This includes `XD-AS-32`, whose clinical construction is complete and unconditional; only the no-forced-lead presentation consequence is contingent on Anthony approving the proposed product decision in the same act (§3, §18).

## 16. Scenarios not ready for approval

**None.**

## 17. Scenario-count reconciliation

| Metric | Count |
|---|---|
| Raw historical entries (all literal entries ever authored, including retired) | 117 |
| Confirmed duplicates | 1 (`CONTRACT-FIX-1` = `HEP-AS-1`) |
| Superseded/retired | 7 (6 `HAEM-EX` + `CN-AS-11`) |
| **Unique active scenarios** | **109** |
| Ready for Anthony approval | 109 |
| Excluded | 0 |
| Documented scenario gaps (behaviour-level) | 0 |
| Documented expectation gaps | 0 |
| Unresolved clinical conflicts | 0 |
| Items pending a product decision (not a scenario defect) | 1 (`XD-AS-32` presentation consequence) |

**Direct verification:** `XD-AS-*` (39) + `HAEM-AS-*` (6) + `HEP-AS-*` (14) + `RE-AS-*` (14) + `IRIN-AS-*` (12) + `THY-AS-*` (12) + `CN-AS-*` (12) = 39+6+14+14+12+12+12 = **109.** Matches.

## 18. Proposed Anthony approval statement

> I approve the complete Cross-Domain Clinical Prioritisation acceptance-scenario estate of 109 scenarios recorded in full in `HEALTHIQ_CROSS_DOMAIN_ACCEPTANCE_SCENARIO_APPROVAL_PACK_v1_2.md` §7-§9, as consistent with the ratified contract v0.6.3, cross-domain ruleset v0.5, HMR adjudication register v0.4, six-domain closure report v0.4, and the bounded Acceptance-Scenario Medical Adjudication v0.1.
>
> I confirm the expected consolidated finding, urgency, severity treatment, tier, role, missing-data/indeterminate behaviour, override behaviour and action class recorded for each listed scenario.
>
> I additionally approve the following product decision, proposed in §3 of that pack: where three or more clinically distinct, non-same-day findings are equally ranked and no governed clinical distinguisher identifies a principal concern or a pair of co-leads, all such findings remain visible in their governed tier, no lead is forced, and no two are manufactured as co-leads. The ordinary two-co-lead rule remains a maximum, not a requirement.
>
> This approval does not alter any clinical rule, threshold, band, override or adjudication. It does not close any regulatory or legal dependency (R1-R6). It does not authorise Tier 0 activation. It does not authorise consumer-facing disease-name release. It does not authorise reliance on unresolved or unenforced questionnaire context. It does not authorise implementation, Cursor prompt authoring, or release.

**This statement has not been issued. It is proposed for Anthony's decision, covering both the scenario estate and the product decision in one act.**

## 19. Contract §23.6 condition 7 verdict

`READY_FOR_ANTHONY_ACCEPTANCE_SCENARIO_APPROVAL`

All 109 active scenarios are fully reproduced with complete governed fields in §7-§9 — no reference to a superseded document is required to know what is being approved. All 26 mandatory behaviours remain explicitly covered (§11). No unresolved clinical conflict exists (§12). Every scenario carries one deterministic expected outcome or a correctly specified constrained state. The one item still pending — the no-forced-lead product decision — is explicitly presented as proposed and unratified (§3), not presumed, and is folded into the single proposed approval act (§18) rather than blocking the verdict, because it is a product-authority question, not a scenario defect: `XD-AS-32`'s clinical construction does not depend on it.

---

**No clinical rule, threshold, adjudication, or new clinical action was created, amended, or reopened by this pack. No code, schema, test, or Cursor prompt was authored. Anthony's approval of the scenario estate, and Anthony's approval of the proposed no-forced-lead product decision, have not been presumed or recorded — §18 proposes one statement covering both; neither has been issued.**
