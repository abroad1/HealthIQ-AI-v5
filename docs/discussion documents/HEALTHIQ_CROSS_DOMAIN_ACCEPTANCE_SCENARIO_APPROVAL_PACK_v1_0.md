---
document_id: HEALTHIQ_CROSS_DOMAIN_ACCEPTANCE_SCENARIO_APPROVAL_PACK
version: "1.0"
work_id: CLIN-PRIORITY-ACCEPTANCE-1
status: DRAFT_FOR_ANTHONY_REVIEW
prepared_by: Claude Code (independent architecture and consistency reviewer)
scope: Consolidation of existing acceptance scenarios across the ratified Cross-Domain Clinical Prioritisation package, for contract §23.6 condition 7
clinical_rules_amended: false
new_scenarios_authored: false
implementation_authorised: false
---

# HealthIQ AI — Cross-Domain Clinical Prioritisation
## Acceptance Scenario Consolidation and Approval Pack v1.0

## 1. Status and purpose

This document consolidates **existing** acceptance scenarios, challenge cases, regression fixtures and sign-off tables already present across the ratified clinical package and its subordinate domain rulesets. It does not create new scenarios, does not set new expected outcomes, and does not reopen any closed clinical adjudication.

Its purpose is to state, for Anthony's review, whether the existing scenario estate is complete and consistent enough to satisfy **contract §23.6 condition 7** ("acceptance scenarios are approved"). It is a consolidation and gap-analysis exercise, not a clinical authoring exercise.

**This document is not itself a clinical authority.** Where it identifies a conflict between a subordinate domain ruleset and the ratified cross-domain package, it applies the governing precedence rule already established by those documents (later ratified cross-domain authority governs) and records the result — it does not invent a resolution.

## 2. Authority and supersession hierarchy

Applied in this order, per the governing instruction:

1. `HEALTHIQ_CLINICAL_FINDING_PRIORITISATION_CONTRACT_v0_6_3.md` — `CLINICALLY_RATIFIED_FOR_ARCHITECTURE_HARDENING`
2. `HEALTHIQ_CROSS_DOMAIN_CLINICAL_PRIORITISATION_RULESET_v0_5.md` — `CLINICALLY_RATIFIED_FOR_ARCHITECTURE_HARDENING`
3. `HEALTHIQ_CROSS_DOMAIN_HMR_ADJUDICATION_REGISTER_v0_4.md` — `CLINICALLY_RATIFIED_FOR_ARCHITECTURE_HARDENING`
4. `HEALTHIQ_SIX_DOMAIN_CLINICAL_CLOSURE_REPORT_v0_4.md` — `CLINICALLY_RATIFIED_FOR_ARCHITECTURE_HARDENING`
5. Six domain prioritisation rulesets (haematology v0.1, hepatic v0.2, renal/electrolyte v0.1, iron/inflammatory v0.1, thyroid/endocrine v0.1, cardiometabolic/nutritional v0.1) — each `DRAFT_FOR_CENTRAL_RECONCILIATION`, subordinate evidentiary source
6. `HEALTHIQ_CROSS_DOMAIN_PRODUCT_RATIFICATION_CLINICIAN_FIRST_v1_0.md` — `PRODUCT_RATIFIED` (Anthony, 2026-08-03) — product-layer authority only; does not determine clinical findings, severity, urgency, tier
7. `CLIN-PRIORITY-ARCH-HARDEN-1_cross_domain_prioritisation_architecture_hardening.md` — `HARDENED_READY_FOR_ANTHONY_ARCHITECTURE_APPROVAL`; Cursor prompt authoring currently `PROHIBITED` pending remaining §23.6 conditions

**Rule applied throughout this pack:** where a domain ruleset (tier 5) states an outcome as unresolved, contested, or dependent on a named open question, and a document at tier 1-4 has since adjudicated that same question, the tier 1-4 adjudication is the current authoritative expected outcome. The domain ruleset's own unresolved-question framing is recorded as historical context, not as a live blocker. Four such cases were found (§8).

## 3. Source inventory

| Document | Version | Status | Acceptance content inspected |
|---|---|---|---|
| Contract | v0.6.3 | Ratified | §19 hepatic regression fixture (1 scenario) |
| Cross-domain ruleset | v0.5 | Ratified | §13 acceptance-test matrix (33 scenarios, including `-b` sub-variants) |
| HMR adjudication register | v0.4 | Ratified | No independent scenario table; adjudication entries (A1-A10, B1-B7) used to resolve domain-level conflicts |
| Six-domain closure report | v0.4 | Ratified | No independent scenario table; confirms no clinical adjudication remains open |
| Haematology ruleset | v0.1 | Draft | §14 lead-selection examples (6 informal examples, no scenario IDs) |
| Hepatic ruleset | v0.2 | Draft | §14 acceptance scenarios AS-1 to AS-14 (14 scenarios; AS-1 is identical in panel to the contract §19 fixture) |
| Renal/electrolyte ruleset | v0.1 | Draft, verdict `REQUIRES_ADDITIONAL_DOMAIN_RESEARCH` | §14 acceptance scenarios AS-1 to AS-14 (14 scenarios) |
| Iron/inflammatory ruleset | v0.1 | Draft | §14 acceptance scenarios AS-1 to AS-12 (12 scenarios) |
| Thyroid/endocrine ruleset | v0.1 | Draft | §13 acceptance scenarios AS-1 to AS-12 (12 scenarios) |
| Cardiometabolic/nutritional ruleset | v0.1 | Draft | §13 acceptance scenarios AS-1 to AS-13 (13 scenarios) |
| Product ratification (clinician-first) | v1.0 | Product-ratified | No independent numbered scenarios — supplies the clinician-first governing test used to assess lead-selection scenarios (§4-§9 of that document) |
| Architecture hardening report | — | Ready for Anthony architecture approval; not yet approved | No independent scenarios — confirms Package A must be tested against the hepatic pilot's existing scenarios (its own §15) |

**Raw scenario count:** 1 + 33 + 6 + 14 + 14 + 12 + 12 + 13 = 105.
**Unique scenario count after removing one confirmed literal duplicate** (contract §19 fixture = hepatic AS-1, identical panel): **104.**

## 4. Scenario-normalisation method

Each scenario is assigned a stable ID using its source document's own numbering, prefixed by domain:

- `CONTRACT-FIX-1` — contract §19 (duplicate of `HEP-AS-1`, retained in the inventory and flagged, not double-counted in totals)
- `XD-AS-#` — cross-domain ruleset §13
- `HAEM-EX-#` — haematology §14 (informal; the source document does not assign IDs, so `1-6` are assigned here in table order for traceability only, not as governed identifiers)
- `HEP-AS-#` — hepatic §14
- `RE-AS-#` — renal/electrolyte §14
- `IRIN-AS-#` — iron/inflammatory §14
- `THY-AS-#` — thyroid/endocrine §13
- `CN-AS-#` — cardiometabolic/nutritional §13

No scenario's stated panel, expected finding, tier, or governing citation has been altered from its source document. Where a source scenario leaves a field unstated, the matrix records **"not specified in source"** rather than inferring a value.

## 5. Consolidated scenario matrix

Columns: **ID | Panel/context | Consolidated finding(s) | Urgency (time-band) | Severity/band | Tier | Lead/co-lead/secondary role | Supporting/modifier/contextual relationships | Missing-data/indeterminate behaviour | Override/combination | Action/timeframe class | Approvable now?**

### 5.1 Contract §19 fixture

| ID | Panel | Finding(s) | Urgency | Severity | Tier | Role | Supporting/context | Missing-data | Override | Action class | Approvable |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CONTRACT-FIX-1 (= HEP-AS-1) | ALT 250 (5.1×ULN), ALP 46, R≈12.9, bilirubin/GGT normal, AST absent, MCV 99.5, transferrin mildly low | One consolidated hepatocellular enzyme elevation | Within days | Marked (5-10×ULN band) | Tier 1 | Lead (only finding of consequence) | MCV, transferrin: contextual, not promoted | Albumin/INR: not assessable, stated | Not applicable | Discuss/investigate | **Yes** — this is the named, non-negotiable regression fixture; already approvable and load-bearing |

### 5.2 Cross-domain ruleset (`XD-AS-*`), 33 scenarios

| ID | Panel (abridged) | Finding(s) | Urgency | Severity/band | Tier | Role | Supporting/context | Missing-data/indeterminate | Override/combination | Action class | Approvable |
|---|---|---|---|---|---|---|---|---|---|---|---|
| XD-AS-1 | K⁺6.8; ALT300(6.1×) | Two findings | Same day (both) | Not specified in source (per-domain) | Tier 0 (both) | Co-equal same-day group | Potassium carries artefact wording | n/a | Same-day override on both | Immediate/same-day | Yes (spec); `TIER_0_PATHWAY_DEPENDENCY` |
| XD-AS-1b | K⁺6.2, else normal | Hyperkalaemia | Same day | Moderate (6.0-6.4) | Tier 0 | Lead | n/a | n/a | B2 adjudication (>6.0 same day) | Immediate | Yes (spec); `TIER_0_PATHWAY_DEPENDENCY` |
| XD-AS-2 | Platelets 45; ALT 200 | Two findings | Not specified per-finding | Not specified | Tier 1 (haem primary) | Haematology primary (below 50 boundary) | n/a | n/a | Consolidation-boundary override | Discuss/investigate | Yes |
| XD-AS-3 | Platelets 120; ALT 200; AST 260 | One hepatic finding | Within days/weeks (not restated) | Marked | Tier 1 | Lead | Platelets nested as fibrosis constituent | n/a | XD-C1 | Discuss/investigate | Yes |
| XD-AS-4 | Ferritin 420; TSAT 58%; ALT 90 | Two findings | Not specified | Not specified | Tier 1 (both) | Independent secondary (iron not absorbed) | n/a | n/a | XD-C9 | Discuss/investigate | Yes |
| XD-AS-5 | Ferritin 1400; TSAT 22%; ALT 90 | One hepatic finding | Not specified | Not specified | Tier 1 | Lead | Ferritin nested as context | n/a | XD-C8 | Discuss/investigate | Yes |
| XD-AS-6 | TSH 14, freeT4 unavailable; LDL 5.9 | Thyroid indeterminate + lipid secondary-cause presentation | Within weeks | Indeterminate | Tier 1 | Dual role, one fact | Thyroid attaches to lipid finding | Indeterminate (free T4 missing) | XD-DUAL-1 | Discuss/investigate | Yes |
| XD-AS-7 | TG 24; Na⁺ 128 | Two findings | Same day (both) | Not specified | Tier 0 (both) | Co-equal, neither suppressed | Sodium carries pseudohyponatraemia caveat | n/a | XD-ARTEFACT-1 | Immediate | Yes (spec); `TIER_0_PATHWAY_DEPENDENCY` |
| XD-AS-8 | B12 110; Hb 82; platelets 88; ANC 1.1 | One pancytopenia finding | Same day | Severe (3-lineage) | Tier 0 | Lead | B12 as aetiology within finding | n/a | XD-C5 | Immediate | Yes (spec); `TIER_0_PATHWAY_DEPENDENCY` |
| XD-AS-9 | Calcium 2.85, albumin absent; K⁺ 6.7 | Potassium finding + calcium insufficient-data | Same day (K⁺) | Not applicable (Ca insufficient data) | Tier 0 (K⁺) | K⁺ lead; calcium alongside, not leading | n/a | Insufficient data (calcium) | n/a | Immediate (K⁺) | Yes (spec); `TIER_0_PATHWAY_DEPENDENCY` |
| XD-AS-10 | eGFR 38 (no baseline); MCV 104; CRP 9; TSH 5.8 | Renal Tier 1 + three Tier 2 findings | Within weeks (renal) | Not specified | Tier 1 (renal), Tier 2 (others) | Renal lead | Three Tier 2 findings compressed, not floored to Tier 1 | AKI not assessable (renal) | XD-HEP-FLOOR-2 (non-export proof) | Discuss/investigate + monitor | Yes |
| XD-AS-11 | Entirely normal broad panel | No-concern | n/a | n/a | n/a | n/a | Six domain-specific non-exclusion statements | n/a | n/a | Monitor/no action | Yes |
| XD-AS-12 | K⁺ 6.8; platelets 18; TG 24 | Three findings | Same day (all) | Not specified | Tier 0 (all) | Three-member co-equal group | n/a | n/a | Same-day overrides ×3 | Immediate | Yes (spec); `TIER_0_PATHWAY_DEPENDENCY` |
| XD-AS-13 | K⁺ 2.3, no symptoms | Hypokalaemia | Same day | Severe (<2.5) | Tier 0 | Lead | n/a | n/a | n/a | Immediate; no mild-consequence language | Yes (spec); `TIER_0_PATHWAY_DEPENDENCY` |
| XD-AS-14 | Adjusted Ca²⁺ 2.05, no symptoms | Hypocalcaemia | Within weeks | Not specified band | Tier 1/2 (implied by "within weeks") | Lead | n/a | Symptom-conditional emergency statement mandatory | n/a | Discuss/investigate | Yes |
| XD-AS-15 | Na⁺ 152, else normal | Hypernatraemia | Within days `[J]` | Mild (146-150) | Tier 1 | Lead | n/a | n/a | HYPERNA-J1 | Discuss/investigate | Yes; `[J]`-labelled, must travel with rule |
| XD-AS-16 | Calcium 1.75 uncorrected, albumin absent | Insufficient data | n/a | n/a | n/a | n/a | n/a | Insufficient data — no finding created | n/a | n/a | Yes |
| XD-AS-17 | TC 8.9, non-HDL 7.2, full risk-factor set | Lipid finding | Within weeks | NICE threshold | Tier 1 | Lead | n/a | n/a | n/a | Investigate; no risk % displayed | Yes (spec); `REGULATORY_DEPENDENCY` (R2 quarantine confirmed, not reopened) |
| XD-AS-18 | ALT 90, AST 130, platelets 135, age 61 | Fibrosis finding | Within weeks | AST:ALT + platelets | Tier 1 | Lead | n/a | n/a | n/a | Investigate; FIB-4 not computed | Yes (spec); `REGULATORY_DEPENDENCY` (R3 quarantine) |
| XD-AS-19 | `may_be_pregnant`; ALT 180, TSH 6.2 | Out-of-scope/withheld | n/a | n/a | n/a | Visible, not suppressed | n/a | n/a | XD-PREG-1/2 | Specialist-rules-required | Yes (spec); `QUESTIONNAIRE_DEPENDENCY` |
| XD-AS-20 | Hb 108, sex present | Anaemia | Within weeks (implied) | Sex-specific threshold | Tier 1 | Lead | n/a | n/a | n/a | Discuss/investigate | Yes |
| XD-AS-20b | Hb 108, sex absent (malformed) | Anaemia, indeterminate | Within weeks | Indeterminate | Tier 1 | Lead | n/a | Indeterminate; assumption stated, no silent default | n/a | Discuss/investigate | Yes (spec); `QUESTIONNAIRE_DEPENDENCY` |
| XD-AS-21 | K⁺ 3.2, Mg not measured | Hypokalaemia | Within weeks | Mild | Tier 2 | Lead | Magnesium requested as companion | n/a | XD-C14 | Monitor | Yes |
| XD-AS-22 | Hb 52, else normal FBC | Severe anaemia | Within days (not same day) | Severe | Tier 1 | Lead | n/a | n/a | Adjudicated decline (A5) | Discuss/investigate | Yes; residual-risk accepted per A5 |
| XD-AS-23 | Bilirubin 95, ALT/ALP/albumin normal | Isolated hyperbilirubinaemia | Within weeks (hepatic floor) | Not specified | Tier 1 | Lead | n/a | n/a | A9 (no Tier 0 bilirubin rule) | Discuss/investigate | Yes |
| XD-AS-23b | ALT 200 (4.1×), bilirubin 2.4×ULN, ALP 1.1×ULN | Hy's law pattern | Same day | Severe | Tier 0 | Lead | n/a | n/a | A9 boundary (Hy's law fires) | Immediate | Yes (spec); `TIER_0_PATHWAY_DEPENDENCY` |
| XD-AS-24 | ALT 58 (1.2×), else normal | One hepatic finding | Within weeks | Mild | Tier 1 | Lead | n/a | n/a | XD-HEP-FLOOR-1 | Discuss/investigate; must not be called urgent | Yes |
| XD-AS-25 | ALT 250, ALP 210, GGT 180, bilirubin 32, albumin normal | One hepatic concern, 4 nested constituents | Not specified | Not specified | Tier 1 | Lead | Four constituents nested | n/a | XD-HEP-FLOOR-1 | Discuss/investigate | Yes |
| XD-AS-26 | Vitamin D 18, calcium normal | Vitamin D deficiency | Routine | Not applicable | Tier 2 | Lead (only finding) | n/a | n/a | XD-VITD-1 | Monitor; no supplementation dose, no Tier 1 escalation | Yes — see §8 (conflicts with `CN-AS-11`) |
| XD-AS-27 | Vitamin D 38, calcium normal | No independent finding | n/a | n/a | n/a | Contextual only | Limited contextual information | n/a | XD-VITD-1 | n/a | Yes |
| XD-AS-28 | Vitamin D 18, adjusted Ca²⁺ 2.05 | Calcium finding + nested vitamin D contributor | Per calcium band | Per calcium band | Per calcium tier | Calcium lead; vitamin D nested | Vitamin D nests, no separate Tier 2 slot | n/a | XD-VITD-2 §9.2.1 | Per calcium action class | Yes |
| XD-AS-29 | Vitamin D 62, adjusted Ca²⁺ 2.05 | Calcium finding stands alone | Per calcium band | Per calcium band | Per calcium tier | Calcium lead; vitamin D not nested | Vitamin D used only to state deficiency unsupported | n/a | XD-VITD-2 §9.2.3 | Per calcium action class | Yes |
| XD-AS-30 | Vitamin D 38, adjusted Ca²⁺ 2.05 | Calcium finding stands; vitamin D limited context only | Per calcium band | Per calcium band | Per calcium tier | Calcium lead | Vitamin D: limited context, not proven deficiency, no independent finding | n/a | XD-VITD-2 §9.2.2 | Per calcium action class | Yes |

### 5.3 Haematology (`HAEM-EX-*`, informal, no source IDs) — see §8, §11 (not ready)

| ID (assigned here) | Panel | Finding(s) | Tier/role stated in source | Notes |
|---|---|---|---|---|
| HAEM-EX-1 | Platelets 18, Hb 128(M), MCV 92 | Severe thrombocytopenia leads | "Same day outranks the borderline Hb" | No severity band, no missing-data/override field stated |
| HAEM-EX-2 | Hb 95, MCV 78, platelets normal | Anaemia, microcytic subtype — one finding | Consolidation example only | No tier/urgency stated explicitly |
| HAEM-EX-3 | MCV 99.5, else normal | No lead from this domain | Tier 2 implied | Contingent framing only ("if another domain has Tier 0/1...") |
| HAEM-EX-4 | MCV 99.5, platelets 140, Hb 118(F) | Multi-lineage — one finding, within days | HAEM-OV-1 | No explicit tier label given |
| HAEM-EX-5 | Neutrophils 0.4, else normal | Severe neutropenia | Same day | No formal Tier 0 specification-only caveat restated here |
| HAEM-EX-6 | WCC 3.1, no differential | Low WCC + neutropenia not assessable | HAEM-IND-2 | Indeterminate/insufficient-data mix, not disambiguated in table |

### 5.4 Hepatic (`HEP-AS-*`), 14 scenarios

| ID | Panel (abridged) | Finding(s) | Urgency | Severity | Tier | Role | Supporting/context | Missing-data/indeterminate | Override | Action class | Approvable |
|---|---|---|---|---|---|---|---|---|---|---|---|
| HEP-AS-1 | = CONTRACT-FIX-1 | (see §5.1) | Within days | Marked | Tier 1 | Lead | MCV/transferrin contextual | Albumin/INR not assessable | n/a | Discuss/investigate | Yes (duplicate of CONTRACT-FIX-1) |
| HEP-AS-2 | Same + albumin 28 | Synthetic dysfunction (HEP-F4) | Same day | Severe | Tier 0 | Lead (HEP-LEAD-1) | Albumin non-hepatic-cause caveat mandatory | n/a | n/a | Immediate | Yes (spec); `TIER_0_PATHWAY_DEPENDENCY` |
| HEP-AS-3 | ALT 550 (11.2×), else normal | Hepatocellular, severe | Same day | Severe (≥10×) | Tier 0 | Lead | n/a | n/a | n/a | Immediate | Yes (spec); `TIER_0_PATHWAY_DEPENDENCY` |
| HEP-AS-4 | ALT 60 (1.2×), isolated | Hepatocellular, mild | Within weeks | Mild | **Tier 1 (literal) — see §8** | Lead | n/a | n/a | HEP-P2 | Discuss/investigate | **No** — as-worded presents two outcomes; HEP-U1 closure (§3, §8) resolves to Tier 1 only |
| HEP-AS-5 | ALP 240 (2.1×), GGT normal, ALT normal | Reclassified HEP-F7, non-hepatic origin | Not specified | Significant ALP band | Own floor retained | Reclassified, not suppressed | n/a | n/a | n/a | Investigate (non-hepatic) | Yes |
| HEP-AS-6 | Bilirubin 38 isolated, no anaemia | Gilbert's pattern | Routine | Not applicable | Tier 2 | Lead | Split-bilirubin caveat if unmeasured | n/a | n/a | Reassurance available | Yes |
| HEP-AS-7 | Bilirubin 38 isolated, Hb low | Different finding from AS-6 | Within weeks | Not specified | Tier 1 | Lead | Haemolysis must be considered | n/a | n/a | Discuss/investigate | Yes |
| HEP-AS-8 | Ferritin 1400, TSAT 22%, ALT 90 | Hepatic Tier 1; ferritin contextual | Within weeks | Not specified | Tier 1 | Lead | Ferritin contextual, magnitude doesn't promote | n/a | n/a | Discuss/investigate | Yes |
| HEP-AS-9 | Ferritin 420, TSAT 58%, ALT 90 | Two Tier 1 findings | Within weeks (both) | Not specified | Tier 1 (both) | Co-lead eligible | n/a | n/a | n/a | Discuss/investigate | Yes |
| HEP-AS-10 | ALT 30, AST 45, platelets 130, age 58 | HEP-F5 fibrosis | Within weeks | AST:ALT>1 + platelets + FIB-4 | Tier 1 | Lead | n/a | n/a | n/a | Investigate | Yes; `DOCUMENTED_EXPECTATION_GAP` — does not explicitly restate the FIB-4-not-computed caveat present in XD-AS-18 for the same rule class (§9) |
| HEP-AS-11 | ALT 250, ALP absent | HEP-F9, pattern undetermined | Not specified | By severity alone | Tier 1 | Lead | n/a | Pattern not assessable (R not computed) | n/a | Discuss/investigate | Yes |
| HEP-AS-12 | Complete normal hepatic panel | No-concern | n/a | n/a | n/a | n/a | Must state normal enzymes don't exclude fibrosis/cirrhosis | n/a | n/a | Monitor | Yes |
| HEP-AS-13 | ALT 250, MCV 118 | Two findings | Not specified | Not specified | Tier 1 (both) | MCV not contextual (above mild band) | n/a | n/a | n/a | Discuss/investigate | Yes |
| HEP-AS-14 | ALT 250, platelets 35 | Two findings | Not specified | Not specified | Tier 1 (hepatic); haem same-day-eligible | Haematology leads on time band | Platelets not absorbed below 50 boundary | n/a | n/a | Discuss/investigate + haem urgency | Yes |

### 5.5 Renal/electrolyte (`RE-AS-*`), 14 scenarios

| ID | Panel (abridged) | Finding(s) | Urgency | Severity | Tier | Role | Supporting/context | Missing-data/indeterminate | Override | Action class | Approvable |
|---|---|---|---|---|---|---|---|---|---|---|---|
| RE-AS-1 | K⁺ 6.8, no repeat, eGFR 55 | RE-F9 | Same day | Severe | Tier 0 | Lead | Mandatory artefact-safe wording | n/a | RE-OV-2 | Immediate | Yes (spec); `TIER_0_PATHWAY_DEPENDENCY` |
| RE-AS-2 | K⁺ 6.2, eGFR 88 | Hyperkalaemia | Same day (per B2) | Moderate | **Tier 0 — see §8** | Lead | n/a | n/a | n/a | Immediate | **No** — as-worded presents two outcomes; RE-U1/B2 closure (§8) resolves to Tier 0 only |
| RE-AS-3 | Creatinine 145, prior 70 six days ago | AKI | Same day | ≥50% rise/7d (NICE) | Tier 0 | Lead | n/a | n/a | RE-OV-3 | Immediate | Yes (spec); `TIER_0_PATHWAY_DEPENDENCY` |
| RE-AS-4 | Creatinine 145, no prior | RE-F10 | Within weeks (from eGFR category) | Not specified | Tier 1 | Lead | n/a | AKI not assessable | n/a | Investigate | Yes |
| RE-AS-5 | eGFR 52, prior 54 four months ago | Stable CKD G3a | Routine | G3a | Tier 2 | Lead | n/a | ACR unavailable — staging incomplete | n/a | Monitor | Yes |
| RE-AS-6 | eGFR 72, no other markers | Not CKD | n/a | n/a | n/a/Tier 3 context | n/a | n/a | n/a | RE-U-NEG-1 | n/a | Yes |
| RE-AS-7 | Calcium 2.85, albumin absent | Insufficient data | n/a | n/a | n/a | n/a | n/a | Insufficient data — not a finding, not suppression | RE-OV-9 | n/a | Yes |
| RE-AS-8 | Calcium 2.85, albumin 40 → adjusted 2.83 | Mild hypercalcaemia | Within days | Mild | Tier 1 | Lead | Albumin as modifier | n/a | n/a | Discuss | Yes |
| RE-AS-9 | Sodium 122 | Profound hyponatraemia | Same day | Profound | Tier 0 | Lead | n/a | Chronicity unknown, stated | n/a | Immediate | Yes (spec); `TIER_0_PATHWAY_DEPENDENCY` |
| RE-AS-10 | Sodium 131 | Mild hyponatraemia | Within weeks `[J]` | Mild | Tier 1 | Lead | n/a | n/a | RE-U-W-2 | Investigate | Yes; deliberate departure from UK "no investigation" guidance, `[J]`-labelled |
| RE-AS-11 | Urea 12, creatinine/eGFR normal | Contextual or Tier 1 | Within weeks (if Tier 1) | Not specified | Tier 3 or Tier 1 | Ambiguous by source's own wording | n/a | n/a | n/a | Investigate/monitor | Yes; `DOCUMENTED_EXPECTATION_GAP` — source states an either/or outcome without a deterministic selection rule |
| RE-AS-12 | K⁺ 6.8 and ALT 300 (6.1×) | Same-day co-equal group | Same day (both) | Not specified | Tier 0 (both) | Co-equal, no ordering | n/a | n/a | n/a | Immediate | Yes (spec); `TIER_0_PATHWAY_DEPENDENCY` |
| RE-AS-13 | eGFR 40, platelets 45 | Two findings | Not specified | Not specified | Tier 1 (renal); haem same-day-eligible | Haematology primary | n/a | n/a | RE-OV-7 | Investigate + haem urgency | Yes |
| RE-AS-14 | Complete normal renal/electrolyte panel | No-concern | n/a | n/a | n/a | n/a | Must state AKI could not be assessed without prior | n/a | n/a | Monitor | Yes |

### 5.6 Iron/inflammatory (`IRIN-AS-*`), 12 scenarios

| ID | Panel (abridged) | Finding(s) | Urgency | Severity | Tier | Role | Supporting/context | Missing-data/indeterminate | Override | Action class | Approvable |
|---|---|---|---|---|---|---|---|---|---|---|---|
| IRIN-AS-1 | Ferritin 1400, TSAT 22% | IRIN-F4 | Routine | TSAT-determined, low | Tier 2 | Lead | n/a | n/a | IRIN-OV-2 | Monitor | Yes |
| IRIN-AS-2 | Ferritin 420, TSAT 58% | IRIN-F3 | Within weeks | TSAT-determined, higher | Tier 1 | Lead | n/a | n/a | IRIN-OV-1 | Investigate/specialist | Yes |
| IRIN-AS-3 | Ferritin 900, TSAT absent, iron+TIBC present | Computed TSAT, then AS-1/AS-2 path | Depends on computed value | Depends on computed value | Depends | Lead | n/a | TSAT derived, labelled as such | IRIN-MOD-1 | Depends | Yes |
| IRIN-AS-4 | Ferritin 900, TSAT absent, iron+TIBC absent | IRIN-F8 | Within weeks | Indeterminate | Tier 1 | Lead | n/a | Indeterminate; both states stated, TSAT requested | n/a | Investigate | Yes |
| IRIN-AS-5 | Ferritin 45 (in range), CRP 60, Hb 105 | IRIN-F5 | Within weeks | Not specified | Tier 1 | Lead | n/a | Not reported as normal despite in-range value | IRIN-OV-4 | Investigate | Yes |
| IRIN-AS-6 | Ferritin 8, Hb 98, MCV 72 | One consolidated iron-deficiency-anaemia finding | Within weeks | Not specified | Tier 1 | Lead (with haematology) | n/a | n/a | IRIN-OV-3 | Investigate | Yes |
| IRIN-AS-7 | CRP 12, else normal | Contextual/low-specificity | Routine | Not specified | Tier 2 | Lead | n/a | n/a | n/a | Monitor | Yes |
| IRIN-AS-8 | CRP 12 ×3 over 9 months | IRIN-F7 | Within weeks | Persistence-based | Tier 1 | Lead | n/a | n/a | n/a | Investigate | Yes |
| IRIN-AS-9 | CRP 60, platelets 40 | Haematology primary, same-day | Same day (haem) | Not specified | Tier 0 (haem) | CRP contextual | CRP attaches to haem finding | n/a | IRIN-OV-5 | Immediate (haem) | Yes (spec); `TIER_0_PATHWAY_DEPENDENCY` |
| IRIN-AS-10 | Ferritin 1100, ALT 120, TSAT 30% | Hepatic finding leads; ferritin contextual | Not specified | Not specified | Tier 1 (hepatic) | Hepatic lead | Ferritin contextual (IRIN-OV-6) | n/a | n/a | Investigate | Yes |
| IRIN-AS-11 | Ferritin 1100, ALT 120, TSAT 55% | Two findings | Not specified | Not specified | Tier 1 (both) | Independent secondary (not absorbed) | n/a | n/a | IRIN-OV-7 | Investigate | Yes |
| IRIN-AS-12 | Complete normal iron panel, CRP normal | No-concern | n/a | n/a | n/a | n/a | Normal ferritin doesn't exclude deficiency w/ inflammation | n/a | n/a | Monitor | Yes |

### 5.7 Thyroid/endocrine (`THY-AS-*`), 12 scenarios

| ID | Panel (abridged) | Finding(s) | Urgency | Severity | Tier | Role | Supporting/context | Missing-data/indeterminate | Override | Action class | Approvable |
|---|---|---|---|---|---|---|---|---|---|---|---|
| THY-AS-1 | TSH 14, freeT4 8 (low) | THY-F1 overt hypothyroid | Within weeks | Overt | Tier 1 | Lead | n/a | n/a | THY-OV-1 | Treat | Yes |
| THY-AS-2 | TSH 14, freeT4 15 (normal) | THY-F2, TSH≥10 | Within weeks | Intermediate | Tier 1 | Lead | n/a | n/a | THY-OV-2 | Treatment-consideration | Yes |
| THY-AS-3 | TSH 6.2, freeT4 15 (normal) | THY-F2, TSH<10 | Routine | Lower | Tier 2 | Lead | n/a | n/a | n/a | Repeat/discuss | Yes |
| THY-AS-4 | TSH 14, freeT4 unavailable | THY-F5 indeterminate | Within weeks | Indeterminate | Tier 1 | Lead | n/a | Both states named; freeT4 requested; may not default to subclinical | n/a | Investigate | Yes — reference case for contract §4.9 |
| THY-AS-5 | TSH<0.01, freeT4 32 (raised) | THY-F3 overt hyperthyroid | Within weeks | Overt | Tier 1 | Lead | n/a | n/a | THY-OV-3 | Treat | Yes |
| THY-AS-6 | TSH<0.01, freeT4 18 (normal), freeT3 unavailable | THY-F4 with THY-IND-3 | Within weeks | Not gradable numerically | Tier 1 | Lead | n/a | T3-toxicosis not assessable | n/a | Investigate | Yes |
| THY-AS-7 | TSH 12, freeT4 28 (both raised) | THY-F6 discordant | Within days | Not gradable | Tier 1 | Lead | n/a | n/a | THY-OV-4 | Specialist interpretation; must not be auto-explained | Yes |
| THY-AS-8 | TSH 6.5, freeT4 normal, TPO positive | THY-F2 | Routine | Lower | Tier 2 | Lead | Antibodies contextual | n/a | n/a | Discuss | Yes |
| THY-AS-9 | TSH 14, freeT4 low, pregnancy known | Domain suppressed | n/a | n/a | n/a | Withheld, visible | n/a | n/a | THY-OV-7 | Specialist-rules-required | Yes (spec); `QUESTIONNAIRE_DEPENDENCY` |
| THY-AS-10 | TSH 8, freeT4 normal, LDL 5.8 | Dual role: THY-F2 + lipid secondary-cause context | Routine (thyroid) | Lower | Tier 2 (thyroid) | Dual role, one fact | Attached to lipid finding | n/a | THY-OV-5 | Discuss | Yes |
| THY-AS-11 | TSH 8, freeT4 normal, MCV 104, else normal FBC | THY-F2 + macrocytosis context | Routine | Lower | Tier 2 | Dual role | Contextual to haematology finding | n/a | THY-OV-6 | Discuss | Yes |
| THY-AS-12 | Normal TSH and freeT4 | No-concern | n/a | n/a | n/a | n/a | Biotin/illness distortion caveat | n/a | n/a | Monitor | Yes |

### 5.8 Cardiometabolic/nutritional (`CN-AS-*`), 13 scenarios

| ID | Panel (abridged) | Finding(s) | Urgency | Severity | Tier | Role | Supporting/context | Missing-data/indeterminate | Override | Action class | Approvable |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CN-AS-1 | TG 24, HbA1c 40, no alcohol data | Severe hypertriglyceridaemia | Same day | Severe | Tier 0 | Lead | HbA1c excludes poor glycaemic control; alcohol unassessed, stated | n/a | CN-OV-1 | Immediate; pancreatitis framing mandatory | Yes (spec); `TIER_0_PATHWAY_DEPENDENCY` |
| CN-AS-2 | TG 24, HbA1c 78 | Same, reframed | Same day | Severe | Tier 0 (not downgraded) | Lead | Dysglycaemia as plausible secondary cause | n/a | CN-OV-5 | Immediate | Yes (spec); `TIER_0_PATHWAY_DEPENDENCY` |
| CN-AS-3 | TC 9.4, non-HDL 7.8, no family history | Lipid finding | Within weeks | NICE threshold | Tier 1 | Lead | n/a | Applies regardless of family history | CN-OV-2 | Specialist assessment | Yes |
| CN-AS-4 | TC 7.9, no family history/risk factors | CN-F9 indeterminate risk | Routine | Not computable | Tier 2 | Lead | n/a | FH not assessable, stated | n/a | Monitor | Yes |
| CN-AS-5 | LDL 5.2, HDL 1.1, TC 7.2, TG 1.8 | One lipid finding | Not specified | Not specified | Tier 2 | Lead | Non-HDL preferred to LDL | n/a | n/a | Monitor | Yes |
| CN-AS-6 | HbA1c 52, single result | Dysglycaemia | Within weeks | Diagnostic range | Tier 1 | Lead | n/a | Diagnosis not assertable — confirmation required | n/a | Investigate | Yes |
| CN-AS-7 | B12 120, Hb 98, MCV 112 | One consolidated finding with haematology | Within weeks | Not specified | Tier 1 | Lead (with haematology) | n/a | n/a | CN-OV-6 | Investigate | Yes |
| CN-AS-8 | B12 320 (in range), MCV 108, normal Hb | CN-F7 | Within weeks | Not specified | Tier 1 | Lead | n/a | In-range value, real finding (contract §3.1) | CN-OV-8 | Investigate | Yes |
| CN-AS-9 | B12 110, Hb 82, platelets 90, neutrophils 1.2 | Haematology primary and same-day | Same day (haem) | Severe (pancytopenia) | Tier 0 (haem) | B12 aetiology within finding | n/a | n/a | CN-OV-7 | Immediate (haem) | Yes (spec); `TIER_0_PATHWAY_DEPENDENCY` |
| CN-AS-10 | TC 8.8, TSH 12, freeT4 low | Lipid reframed; both findings stand | Within weeks (thyroid leads on actionability) | Not specified | Tier 1 (both) | Thyroid leads within band | n/a | n/a | CN-OV-5 | Treat thyroid; investigate lipid | Yes |
| CN-AS-11 | Vitamin D 18, else normal | "No band adopted" (CN-S-6) | Routine | Not specified | Tier 2 | Lead | Explicit no-governed-threshold statement | n/a | n/a | Monitor | **No** — superseded; see §8 (conflicts with `XD-AS-26`) |
| CN-AS-12 | TG 24 and K⁺ 6.8 | Same-day co-equal group | Same day (both) | Not specified | Tier 0 (both) | Co-equal, no ordering | n/a | n/a | n/a | Immediate | Yes (spec); `TIER_0_PATHWAY_DEPENDENCY` |
| CN-AS-13 | Complete normal lipid and nutritional panel | No-concern | n/a | n/a | n/a | n/a | Normal lipid doesn't exclude CV risk; normal B12 doesn't exclude functional deficiency | n/a | n/a | Monitor | Yes |

## 6. Coverage matrix against the 26 mandatory behaviours

| # | Mandatory behaviour | Covered by | Status |
|---|---|---|---|
| 1 | Interpretability before prioritisation | HEP-AS-11, RE-AS-7, THY-AS-4 | Covered |
| 2 | Domain-specific severity bands | HEP-AS-3, RE-AS-1/9, IRIN-AS-1/2, THY-AS-2, CN-AS-3/4 | Covered |
| 3 | Urgency independently from severity | CONTRACT-FIX-1/HEP-AS-1 (confidence reduced, significance not) | Covered, implicitly |
| 4 | "More serious tier wins" (urgency vs severity algebra, contract §6.1) | None found as a dedicated scenario | `DOCUMENTED_SCENARIO_GAP` |
| 5 | Consolidation before prioritisation | HEP-AS-1, XD-AS-25, CN-AS-5 | Covered |
| 6 | Same-domain frame consolidation | XD-AS-25, CN-AS-5 | Covered |
| 7 | Cross-domain duplicate consolidation | XD-AS-4/5, IRIN-AS-10/11, HEP-AS-8/9 | Covered |
| 8 | Direct finding vs contextual/phenotype | XD-AS-10, HEP-AS-13 | Covered |
| 9 | Independent secondary concerns | XD-AS-4, RE-AS-13, IRIN-AS-11 | Covered |
| 10 | Ordinary co-lead behaviour | HEP-AS-9 | Covered, single example only |
| 11 | Same-day co-equal concern groups | XD-AS-1/7/12, RE-AS-12, CN-AS-12 | Covered extensively |
| 12 | Ordinary two-co-lead cap below same-day band | None found | `DOCUMENTED_SCENARIO_GAP` |
| 13 | Supporting-marker nesting | HEP-AS-8, XD-AS-3, XD-AS-28 | Covered |
| 14 | Modifiers that change urgency/severity | RE-AS-8, IRIN-AS-3 | Covered |
| 15 | Override behaviour | HAEM-OV/RE-OV/IRIN-OV examples cited across matrix | Covered |
| 16 | Insufficient-data behaviour | RE-AS-7, XD-AS-9/16 | Covered |
| 17 | Indeterminate-severity behaviour | THY-AS-4/6, HEP-AS-11 | Covered |
| 18 | Missing modifiers must not cause worst-case inference | Principle stated in domain rulesets (e.g. HAEM-IND-PRINCIPLE); no standalone scenario isolates the no-escalation direction specifically | `DOCUMENTED_SCENARIO_GAP` (partial) |
| 19 | Pregnancy-dependent suppression/limitation | XD-AS-19, THY-AS-9 | Covered |
| 20 | Sex-dependent interpretation | XD-AS-20/20b | Covered |
| 21 | No-concern output | XD-AS-11, HEP-AS-12, RE-AS-14, IRIN-AS-12, THY-AS-12, CN-AS-13 | Covered extensively |
| 22 | Tier 0 specification-only and withheld behaviour | RE-AS-1, HEP-AS-2, XD-AS-1 (and all Tier 0 scenarios) | Covered |
| 23 | Tier 0 non-downgrade behaviour | Stated as policy (XD-T0-2) but no scenario demonstrates the withheld-not-demoted mechanic operationally | `DOCUMENTED_SCENARIO_GAP` |
| 24 | Quarantined disease-name, FIB-4, CV-risk capabilities | XD-AS-17 (CV risk), XD-AS-18 (FIB-4) covered; disease-name quarantine has no dedicated scenario | `DOCUMENTED_SCENARIO_GAP` (disease-name only) |
| 25 | Hepatic pilot regression behaviour | CONTRACT-FIX-1 / HEP-AS-1 | Covered — this is the named fixture |
| 26 | Clinician-first lead selection across unlike domains | XD-AS-1/7/12, RE-AS-13; governing test in product ratification §3-§9 | Covered |

**21 of 26 behaviours are fully covered by existing scenarios. 5 have a documented gap** (items 4, 12, 18 partial, 23, 24 partial). None of the gaps requires inventing a new clinical rule to close — each would be closed by authoring an additional scenario against an already-ratified rule.

## 7. Duplicate and overlap analysis

- **Confirmed literal duplicate:** `CONTRACT-FIX-1` and `HEP-AS-1` — identical panel, identical expected outcome. Not a conflict; retained as one scenario for approval purposes, both citations preserved for traceability (the contract cites it as the load-bearing regression fixture; the hepatic ruleset independently reproduces it).
- **Same-panel, contradictory-outcome overlap:** `XD-AS-26` and `CN-AS-11` — same vitamin D panel (18 nmol/L, otherwise normal), incompatible expected outcomes. See §8.
- **Conceptual (non-contradictory) overlap, different panels, same rule class:**
  - Hepatic/haematology platelet-consolidation boundary (<50 ×10⁹/L): tested by `XD-AS-2`, `XD-AS-3`, `HEP-AS-14`, `RE-AS-13` — four scenarios exercising the same boundary rule with different panels. Consistent outcomes throughout; redundant but not conflicting.
  - Ferritin/TSAT severity-inversion rule: tested by `XD-AS-4`, `XD-AS-5`, `IRIN-AS-1`, `IRIN-AS-2`, `HEP-AS-8`, `HEP-AS-9`, `IRIN-AS-10`, `IRIN-AS-11` — eight scenarios, all consistent.
  - FIB-4/CV-risk quarantine: `XD-AS-17`, `XD-AS-18`, `HEP-AS-10` (partial — see §9 expectation gap), `CN-AS-*` risk-framed scenarios.
  - Same-day co-equal grouping: `XD-AS-1`, `XD-AS-7`, `XD-AS-12`, `RE-AS-12`, `CN-AS-12` — five scenarios, all consistent, no internal-ordering language in any.

No other material duplication was found. The estate is redundant in places (multiple domains independently re-proving the same cross-domain rule) but this redundancy is evidence of independent domain authoring converging on the same rule, not evidence of drift.

## 8. Contradiction analysis

Four contradictions were found. In each case the governing precedence rule (§2) is applied and the result recorded — no new clinical position is created.

| # | Conflict | Earlier/subordinate position | Later/superseding ratified position | Resolution applied |
|---|---|---|---|---|
| 1 | `HEP-AS-4` vs `HEP-U1` | Hepatic ruleset itself: "Tier 1 under HEP-P2 — or Tier 2 under modified reading. Both defensible; HEP-U1 decides." | Adjudication register §2 (B1): "Adopt the BSG position literally... No magnitude-gated alternative is retained." | `HEP-U1` is closed by the ratified register. `HEP-AS-4`'s authoritative expected outcome is **Tier 1 only**. The scenario as currently worded in the hepatic ruleset is stale text, not a live conflict — but it cannot be marked "ready for approval" **as worded**, because its own text still presents two outcomes. Recommend the hepatic ruleset's AS-4 wording be corrected to state Tier 1 only before formal approval; the correction is administrative (aligning stale text to an already-closed adjudication), not a new clinical decision. |
| 2 | `RE-AS-2` vs `RE-U1` | Renal ruleset itself: "Tier 0 or high Tier 1 depending on RE-U1 resolution... both defensible." | Adjudication register (B2): "K⁺ >6.0 mmol/L same day — deliberate conservative HealthIQ adjudication." Cross-domain ruleset §1, rule #2: "Platelets... K⁺ 6.0–6.4 mmol/L" listed as Tier 0. | `RE-U1` is closed by B2. K⁺ 6.2 falls within the ratified 6.0-6.4 same-day band. `RE-AS-2`'s authoritative expected outcome is **Tier 0 only**. Same administrative-correction recommendation as above. |
| 3 | `CN-AS-11` vs `XD-AS-26`/`XD-VITD-1` | Cardiometabolic ruleset itself (predates the A8 vitamin D adjudication): "No band adopted (CN-S-6)... Finding created and shown at Tier 2 with an explicit statement that HealthIQ has not adopted a governed threshold." | Adjudication register A8 (closed) and ruleset `XD-VITD-1`: `<25 nmol/L` → Tier 2 routine deficiency finding, governed UK threshold adopted. `XD-AS-26` tests the identical panel (Vitamin D 18 nmol/L, calcium normal) against the correct, current outcome. | `CN-AS-11` is stale — it documents a state the cross-domain package has since closed. **`CN-AS-11` is not ready for approval as worded**; `XD-AS-26` is the current, correct, approvable scenario for this exact panel. Recommend retiring `CN-AS-11` or updating its text to point to `XD-VITD-1` rather than restating the now-superseded "no band adopted" position. |
| 4 | `HAEM` domain's own severe-anaemia framing vs adjudication register A5 | Haematology ruleset (§18, HAEM-U1 — a different, haematology-specific item from hepatic's `HEP-U1`): lists the severe-anaemia same-day threshold as an open, blocking question. | Adjudication register A5 (closed): "No severe-anaemia same-day threshold authorised. Anaemia caps at within days." Reflected in `XD-AS-22` (Hb 52 → within days, "residual risk accepted"). | The haematology ruleset's own framing of this as still-blocking is superseded — A5 already declined to set a same-day threshold, deliberately, as a permanent (not interim) position. `XD-AS-22` is the correct, approvable scenario. No haematology-ruleset scenario directly tests this panel, so this is recorded as a resolved conflict feeding into §9's gap register, not a scenario requiring correction. |

**No contradiction was found that the stated authority hierarchy could not resolve.** No STOP condition was triggered on this basis.

## 9. Dependency register

| Class | Items |
|---|---|
| `REGULATORY_DEPENDENCY` | All scenarios testing CV-risk-calculation output (`XD-AS-17`) and FIB-4 (`XD-AS-18`, `HEP-AS-10`) depend on R2/R3 remaining quarantined as specified — approvable as-is (the scenario correctly specifies quarantine), but the underlying capability cannot be released until R2/R3 close. Disease-name quarantine (behaviour #24) has no dedicated scenario and also depends on R4. |
| `TIER_0_PATHWAY_DEPENDENCY` | Every scenario whose expected tier is Tier 0 (`XD-AS-1/1b/7/8/9/12/13/23b`, `HEP-AS-2/3`, `RE-AS-1/3/9/12`, `IRIN-AS-9`, `CN-AS-1/2/9/12`) — the scenario's expected specification is approvable now; activation/release of that specification remains blocked by R1 (contract §17) regardless of this pack's approval. |
| `QUESTIONNAIRE_DEPENDENCY` | `XD-AS-19` (pregnancy known), `XD-AS-20b` (sex absent), `THY-AS-9` (pregnancy known) — expected behaviour is approvable as a specification; operational reliance on the pregnancy-known path is not currently reachable through the canonical questionnaire (per the architecture hardening report §11.2) and must not be treated as operationally proven. |
| `DOCUMENTED_CONFLICT` (resolved, administrative correction recommended) | `HEP-AS-4`, `RE-AS-2`, `CN-AS-11` (§8) |
| `DOCUMENTED_SCENARIO_GAP` | Behaviours #4, #12, #18 (partial), #23, #24 (disease-name only) (§6); haematology's severe-anaemia same-day question has no domain scenario reflecting the A5 closure (§8, item 4); `HAEM-U2` (ethnic neutropenia — resolved by `XD-ANC-1`'s general no-ancestry-adjustment rule, but no haematology scenario demonstrates it); `RE-U9` (whether CKD staging without ACR should be presented at all) remains open and untested; `ENDO-U1` (thyroid workstream's scope boundary) is a scope question, not a scenario gap. |
| `DOCUMENTED_EXPECTATION_GAP` | `HEP-AS-10` (FIB-4-not-computed caveat not restated, §5.4); `RE-AS-11` (either/or outcome without a deterministic selector, §5.5); all six `HAEM-EX-*` items (informal, no scenario IDs, incomplete field coverage, §5.3, §11). |

## 10. Scenarios ready for Anthony's approval

**95 of 104 unique scenarios**, comprising:
- `CONTRACT-FIX-1`/`HEP-AS-1` (counted once)
- All 33 `XD-AS-*` scenarios except none excluded (all 33 ready; the vitamin D conflict is resolved in `XD-AS-26`'s favour, not against it)
- 13 of 14 `HEP-AS-*` scenarios (all except `HEP-AS-4`)
- 13 of 14 `RE-AS-*` scenarios (all except `RE-AS-2`)
- All 12 `IRIN-AS-*` scenarios
- All 12 `THY-AS-*` scenarios
- 12 of 13 `CN-AS-*` scenarios (all except `CN-AS-11`)

Approval of a Tier 0, regulatory-quarantined, or questionnaire-dependent scenario in this list confirms only that its **expected specification is correct and internally consistent** — per the approval boundary (§12), it does not authorise activation, release, or operational reliance on the associated dependency.

## 11. Scenarios not ready for approval, and why

| Scenario(s) | Reason | Class |
|---|---|---|
| `HEP-AS-4` | States two possible outcomes; the closed `HEP-U1` adjudication resolves this to one, but the scenario text has not been updated to reflect it | `DOCUMENTED_CONFLICT` |
| `RE-AS-2` | Same pattern — closed `RE-U1`/B2 adjudication resolves to one outcome, text not updated | `DOCUMENTED_CONFLICT` |
| `CN-AS-11` | Directly contradicts the ratified `XD-VITD-1`/A8 position for an identical panel; superseded | `DOCUMENTED_CONFLICT` |
| `HAEM-EX-1` through `HAEM-EX-6` (all six) | Informal, unlabelled, and incomplete against the required field set (no severity band, no explicit missing-data/override annotation, no scenario ID) — cannot be approved as governed acceptance scenarios in their current form regardless of their underlying clinical correctness | `DOCUMENTED_EXPECTATION_GAP` |

None of these nine items requires new clinical authoring to fix — each requires only an administrative text correction (three) or a formal scenario-ID/field-completion pass (six), against rules that are already ratified.

## 12. Proposed approval statement

> Anthony's approval of the 95 scenarios listed in §10 confirms that their expected consolidated findings, tiers, urgency, severity treatment, roles and missing-data behaviour correctly reflect the ratified Cross-Domain Clinical Prioritisation package as it stands today.
>
> This approval:
> - does not alter any clinical rule, threshold, or adjudication;
> - does not close R1, R2, R3, R4, R5 or R6, or any other regulatory or legal dependency;
> - does not authorise Tier 0 activation — Tier 0 scenarios remain specification-only and unreachable pending the contract §17 operational pathway;
> - does not authorise reliance on unresolved or unenforced questionnaire context — pregnancy- and sex-dependent scenarios remain specifications only, not proof of operational reachability;
> - does not authorise implementation execution or release;
> - satisfies contract §23.6 condition 7 **only for the 95 scenarios listed**, not for the full theoretical scenario space of the ratified package.

## 13. §23.6 condition 7 verdict

`READY_FOR_PARTIAL_APPROVAL_WITH_EXPLICIT_EXCLUSIONS`

95 of 104 unique existing scenarios are ready for Anthony's approval as-is. Nine are excluded for the reasons in §11, none requiring new clinical authoring. Five of the 26 mandatory behaviours (§6) have a documented, closeable scenario gap that does not block approving the 95 but should be scheduled before condition 7 can be marked fully and permanently satisfied for the whole behaviour set.

---

**No clinical rule, threshold, or adjudication was created, amended, or reopened by this pack. No code, schema, test, or Cursor prompt was authored.**
