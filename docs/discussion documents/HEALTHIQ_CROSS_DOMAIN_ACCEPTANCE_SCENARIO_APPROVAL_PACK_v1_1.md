---
document_id: HEALTHIQ_CROSS_DOMAIN_ACCEPTANCE_SCENARIO_APPROVAL_PACK
version: "1.1"
work_id: CLIN-PRIORITY-ACCEPTANCE-2
status: READY_FOR_ANTHONY_ACCEPTANCE_SCENARIO_APPROVAL
supersedes: HEALTHIQ_CROSS_DOMAIN_ACCEPTANCE_SCENARIO_APPROVAL_PACK_v1_0.md
prepared_by: Claude Code (independent architecture and consistency reviewer)
incorporates: HEALTHIQ_CROSS_DOMAIN_ACCEPTANCE_SCENARIO_MEDICAL_ADJUDICATION_v0_1.md
scope: Consolidation of existing and medically adjudicated acceptance scenarios across the ratified Cross-Domain Clinical Prioritisation package, for contract §23.6 condition 7
clinical_rules_amended: false
new_clinical_thresholds_created: false
anthony_approval_recorded: false
implementation_authorised: false
cursor_prompt_authorised: false
---

# HealthIQ AI — Cross-Domain Clinical Prioritisation
## Acceptance Scenario Consolidation and Approval Pack v1.1

## 1. Metadata and status

This is the rebuilt, complete acceptance-scenario approval pack. It supersedes v1.0 in full. It incorporates every scenario and clarification authorised by `HEALTHIQ_CROSS_DOMAIN_ACCEPTANCE_SCENARIO_MEDICAL_ADJUDICATION_v0_1.md` and records one explicit product decision made directly by Anthony in the course of commissioning this rebuild (§3, §9).

**This document does not record Anthony's approval of the scenario estate.** It presents the estate as ready for that approval and proposes the exact statement Anthony would need to issue (§18). Approval remains a separate, future act.

## 2. Purpose and approval boundary

The purpose of this pack is to state whether the complete existing and medically adjudicated acceptance-scenario estate is ready for Anthony's approval under **contract §23.6 condition 7**.

Approving the scenarios listed in §15:

- confirms the expected consolidated finding, urgency, severity treatment, tier, role, supporting relationships, missing-data behaviour and action class recorded for each scenario;
- confirms the no-forced-lead product decision (§9, `XD-AS-32`) where clinical authority supplies no distinguisher between three or more co-equal, non-same-day findings;
- does **not** alter any clinical rule, threshold, band, override or adjudication;
- does **not** close R1, R2, R3, R4, R5 or R6, or any other regulatory or legal dependency;
- does **not** authorise Tier 0 activation;
- does **not** authorise consumer-facing disease-name release;
- does **not** authorise reliance on unresolved or unenforced questionnaire context;
- does **not** authorise implementation, Cursor prompt authoring, or release.

## 3. Authority and supersession hierarchy

Applied in this order, per the governing instruction for this task:

1. `HEALTHIQ_CLINICAL_FINDING_PRIORITISATION_CONTRACT_v0_6_3.md` — ratified
2. `HEALTHIQ_CROSS_DOMAIN_CLINICAL_PRIORITISATION_RULESET_v0_5.md` — ratified
3. `HEALTHIQ_CROSS_DOMAIN_HMR_ADJUDICATION_REGISTER_v0_4.md` — ratified
4. `HEALTHIQ_SIX_DOMAIN_CLINICAL_CLOSURE_REPORT_v0_4.md` — ratified
5. `HEALTHIQ_CROSS_DOMAIN_ACCEPTANCE_SCENARIO_MEDICAL_ADJUDICATION_v0_1.md` — `MEDICAL_ADJUDICATION_COMPLETE`; authoritative **only** for the bounded scenario clarifications it records (§4 of that document); it does not replace the governing contract or rulesets and creates no new threshold
6. Six ratified domain prioritisation rulesets (haematology v0.1, hepatic v0.2, renal/electrolyte v0.1, iron/inflammatory v0.1, thyroid/endocrine v0.1, cardiometabolic/nutritional v0.1) — subordinate domain evidence
7. `HEALTHIQ_CROSS_DOMAIN_PRODUCT_RATIFICATION_CLINICIAN_FIRST_v1_0.md` — `PRODUCT_RATIFIED` (Anthony, 2026-08-03); governs product-layer decisions only (lead selection, prominence, presentation), never clinical findings, severity, urgency or tier
8. `CLIN-PRIORITY-ARCH-HARDEN-1_cross_domain_prioritisation_architecture_hardening.md` — architecture-hardening verdict `HARDENED_READY_FOR_ANTHONY_ARCHITECTURE_APPROVAL`, **approved by Anthony**; governs architecture and Cursor-authoring gate status only, and does not itself authorise implementation, Cursor prompt authoring or release

**Additional Anthony product decision applied in this pack** (supplied directly for this task, consistent with and extending clinician-first v1.0 §5-§6, and resolving the residual product question the medical adjudication left open at its Item C, §14 item 1):

> For a case containing three or more equally ranked, non-same-day findings where no governed clinical distinguisher establishes a principal concern or a pair of co-leads: do not force a lead; do not manufacture two co-leads; retain all clinically distinct findings visibly within their governed tier; do not imply that one finding matters more where clinical authority does not support that conclusion. This applies only where no governed lead-selection rule resolves the case. The ordinary two-co-lead rule remains a maximum, not a requirement to designate two co-leads.

This decision does not conflict with clinician-first v1.0 — it resolves an edge case that document's §6 leaves open (three-or-more co-equal, non-same-day, no distinguisher) using the same governing test (§3 of that document) and the same prohibition on manufacturing co-lead status "merely to avoid making a difficult prioritisation decision" (§6). No STOP condition is triggered.

**Rule applied throughout this pack:** where a subordinate document states an outcome as unresolved or presents two candidate outcomes, and a document at a higher tier has since adjudicated that question, the higher-tier adjudication is the current authoritative expected outcome, and the subordinate document's framing is recorded as historical/administrative, not as a live blocker.

## 4. Source inventory

| Document | Version | Status | Role in this pack |
|---|---|---|---|
| Acceptance Scenario Approval Pack | v1.0 | Superseded by this document | Baseline; every scenario, gap and conflict carried forward or corrected |
| Acceptance-Scenario Medical Adjudication | v0.1 | `MEDICAL_ADJUDICATION_COMPLETE` | Source of all corrections and new scenarios in §8-§9 |
| Clinical Finding Prioritisation Contract | v0.6.3 | Ratified | Governing clinical policy |
| Cross-Domain Clinical Prioritisation Ruleset | v0.5 | Ratified | Governing cross-domain rules; source of original `XD-AS-1` to `XD-AS-30` |
| Cross-Domain HMR Adjudication Register | v0.4 | Ratified | Closed adjudications (B1, B2, A1-A10, etc.) |
| Six-Domain Clinical Closure Report | v0.4 | Ratified | Confirms no clinical adjudication remains open |
| Haematology Prioritisation Ruleset | v0.1 | Draft, subordinate | Source of `HAEM-EX-1` to `-6` (now superseded, §10) |
| Hepatic Prioritisation Ruleset | v0.2 | Draft, subordinate | Source of `HEP-AS-1` to `-14` |
| Renal and Electrolyte Prioritisation Ruleset | v0.1 | Draft, subordinate, verdict `REQUIRES_ADDITIONAL_DOMAIN_RESEARCH` (electrolyte bands only — does not affect scenario approvability) | Source of `RE-AS-1` to `-14` |
| Iron and Inflammatory Prioritisation Ruleset | v0.1 | Draft, subordinate | Source of `IRIN-AS-1` to `-12` |
| Thyroid and Endocrine Prioritisation Ruleset | v0.1 | Draft, subordinate | Source of `THY-AS-1` to `-12` |
| Cardiometabolic and Nutritional Prioritisation Ruleset | v0.1 | Draft, subordinate | Source of `CN-AS-1` to `-13` (one retired, §10) |
| Product Ratification — Clinician-First Model | v1.0 | `PRODUCT_RATIFIED` | Product-layer authority; source of the co-lead cap and the clinician-first governing test |
| Architecture Hardening Report | `CLIN-PRIORITY-ARCH-HARDEN-1` | `HARDENED_READY_FOR_ANTHONY_ARCHITECTURE_APPROVAL`, approved by Anthony | Confirms architecture gate status; not itself a scenario source |

No duplicate copies of any of the above were created. All paths are the actual repository paths discovered during inspection.

## 5. Changes from v1.0

1. **`RE-AS-11` corrected** — replaced the either/or outcome with the medically adjudicated deterministic result: no independent renal finding, Tier 3 contextual, distinct low-prominence orphan group, no urgency/severity/action class (§7.5, medical adjudication §5).
2. **Six new cross-domain scenarios added**: `XD-AS-31` to `XD-AS-36`, closing all five previously documented behaviour gaps (§8).
3. **Six haematology scenarios formalised**: `HAEM-AS-1` to `-6` replace the informal `HAEM-EX-1` to `-6` (§9). The informal examples are retired, not retained as additional entries (§10).
4. **Four stale scenarios corrected administratively**: `HEP-AS-4` (Tier 1 only), `RE-AS-2` (Tier 0 only), `HEP-AS-10` (FIB-4 not computed/displayed caveat added), and `CN-AS-11` (retired and replaced by `XD-AS-26`, not merely relabelled) (§7, §10, §12).
5. **Document and approval status corrected**: the architecture-hardening report is recorded as approved by Anthony (no longer "pending"); the product-ratification condition is recorded as satisfied via the clinician-first document. Neither statement authorises implementation, Cursor prompt authoring, or release (§3, §13).
6. **One explicit Anthony product decision recorded**: the no-forced-lead rule for three-or-more co-equal, non-same-day findings (§3, §9 `XD-AS-32`).
7. **Coverage matrix rebuilt**: all 26 mandatory behaviours are now explicitly covered (§11), against 21/26 in v1.0.
8. **Scenario counts recalculated transparently, not by mechanical addition** (§17).
9. **Verdict changed** from `READY_FOR_PARTIAL_APPROVAL_WITH_EXPLICIT_EXCLUSIONS` (v1.0) to `READY_FOR_ANTHONY_ACCEPTANCE_SCENARIO_APPROVAL` (§19).

## 6. Scenario-normalisation method

Unchanged from v1.0: each scenario carries a stable, domain-prefixed ID drawn from its source document's own numbering (or, for the six new cross-domain and six formalised haematology scenarios, from the medical adjudication document that authored them). No scenario's panel, expected finding, tier, or governing citation has been altered from its authoritative source. Where this pack corrects a scenario, the correction is recorded as a named administrative alignment against a specific closed adjudication (§12), never as a new interpretation.

## 7. Complete consolidated scenario matrix

Unchanged scenarios from v1.0 are not reproduced in full here to avoid restating ~100 unchanged rows; they are carried forward by reference to v1.0 §5.2, §5.4-§5.8, with the following corrections applied in place. Full detail for all new and reformalised scenarios is in §8-§9.

### 7.1 Scenarios carried forward unchanged from v1.0

All 33 original `XD-AS-*` scenarios, all 12 `IRIN-AS-*`, all 12 `THY-AS-*`, 12 of 13 `CN-AS-*` (all except `AS-11`), 12 of 14 `HEP-AS-*` (all except `AS-4` and `AS-10`, corrected below), 13 of 14 `RE-AS-*` (all except `AS-2` and `AS-11`, corrected below), and `CONTRACT-FIX-1`/`HEP-AS-1` (unchanged, still a confirmed literal duplicate).

### 7.2 `HEP-AS-4` — corrected

| Field | v1.0 (stale) | v1.1 (corrected) |
|---|---|---|
| Expected tier | "Tier 1 under HEP-P2 — or Tier 2 under modified reading; both defensible; HEP-U1 decides" | **Tier 1 only** |
| Action class | Discuss/investigate | **Within-weeks discuss/investigate** |
| New requirement | — | **Must explicitly state that a minor hepatic abnormality is not described as urgent merely because the hepatic Tier 1 floor applies** (`XD-HEP-FLOOR-1` point 4) |

Basis: `HEP-U1` closed by adjudication register B1 (literal BSG position; no magnitude-gated alternative retained). Medical adjudication §12 (Item H), classification `ADMINISTRATIVE_ALIGNMENT_ONLY`.

### 7.3 `RE-AS-2` — corrected

| Field | v1.0 (stale) | v1.1 (corrected) |
|---|---|---|
| Expected tier | "Tier 0 or high Tier 1 depending on RE-U1; both defensible" | **Tier 0 only** |
| Basis | — | K⁺ 6.2 mmol/L falls within the closed B2 same-day band (>6.0 mmol/L) |
| Relationship to `XD-AS-31` | — | Overlapping but not duplicate: `RE-AS-2` tests the **clinical threshold** (does 6.2 mmol/L meet the same-day criterion); `XD-AS-31` tests the **"more serious tier wins" algebra** (urgency-tier vs severity-tier resolution) using the same value. Both retained. |

Basis: `RE-U1` closed by adjudication register B2. Medical adjudication §12 (Item H) and §6 (Item B).

### 7.4 `RE-AS-11` — corrected

| Field | v1.0 (stale) | v1.1 (corrected) |
|---|---|---|
| Inputs | Urea 12, creatinine/eGFR normal | Unchanged |
| Consolidated finding | "Tier 3 contextual **or** Tier 1 within weeks" (either/or) | **None.** Urea does not form an independent finding (`RE-CONS-3` governs over the incidental `RE-U-W-4` band listing) |
| Urgency | "Within weeks (if Tier 1)" | **Not applicable** — no finding, therefore no urgency band |
| Severity | Not specified | **Not applicable** |
| Tier | Ambiguous | **Tier 3 — contextual** |
| Role | Ambiguous | **Contextual information** (clinician-first §8) |
| Parent | Not specified | **None present.** Orphan handling under contract §6.5 → distinct low-prominence contextual group, reconcilable with the raw value |
| Missing-data | Not specified | None triggered — urea has no governed modifier |
| Override | Not specified | None |
| Action class | "Investigate/monitor" | **None.** No action class is assigned to a Tier 3 contextual item |
| Prohibited | Not stated | Presenting urea as renal impairment or renal failure; assigning it an independent tier or action |
| Explicitly preserved as open, not resolved by this correction | — | `RE-U5` (whether urea ever forms an independent finding with clinical context) remains open; no urea:creatinine combination rule is created (§14) |

Basis: medical adjudication §5, classification `MEDICAL_CLARIFICATION_OF_EXISTING_AUTHORITY`.

### 7.5 `HEP-AS-10` — corrected

| Field | v1.0 | v1.1 (corrected) |
|---|---|---|
| Finding | HEP-F5 fibrosis via AST:ALT ratio and platelets | Unchanged — retained in full |
| New explicit requirement | Absent (flagged as `DOCUMENTED_EXPECTATION_GAP` in v1.0) | **FIB-4 is not computed. FIB-4 is not displayed. Quarantine removes the calculation, not the underlying finding** (`XD-QUAR-1`, R3) |

Basis: medical adjudication §12 (Item H), classification `ADMINISTRATIVE_ALIGNMENT_ONLY`.

### 7.6 `CN-AS-11` — retired, not relabelled

`CN-AS-11` is **retired** from the active scenario estate. It is not renamed, relabelled, or kept as a live scenario under a new basis. Its content ("no governed vitamin D threshold exists") is medically stale: the A8 adjudication closed a governed `<25 nmol/L` threshold before this scenario's premise was written. Retaining it under any label would misstate why the current tier is what it is.

**`XD-AS-26`** (already present in the estate, unchanged) is the scenario of record for this exact panel (Vitamin D 18 nmol/L, calcium normal) under the current, correct basis: a governed Tier 2 routine deficiency finding under the closed A8 adjudication.

Basis: medical adjudication §12 (Item H).

## 8. Formal cross-domain scenarios (new)

Full detail reproduced from the medical adjudication (§6-§10 of that document); no field has been altered.

### `XD-AS-31` — more serious tier wins

| Field | Value |
|---|---|
| Inputs | K⁺ 6.2 mmol/L; creatinine, eGFR and all other analytes normal |
| Consolidated finding | Hyperkalaemia (`RE-F3`) |
| Urgency-derived tier | Tier 0 — K⁺ >6.0 mmol/L is same day (closed B2) |
| Severity-derived tier | Tier 1 — 6.0-6.4 mmol/L is the UKKA moderate band |
| Final tier | **Tier 0** — the more serious of the two governs (contract §6.1) |
| Role | Principal concern (sole finding) |
| Action class | Same day; mandatory artefact-safe wording (`RE-A-WORD-1`) |
| Dependency | `TIER_0_PATHWAY_DEPENDENCY` — specification-only, withheld per `XD-AS-35`'s mechanic |
| Demonstrates | Urgency and severity are assessed independently; a moderate severity band does not cap a same-day urgency |

### `XD-AS-32` — three Tier 1 concerns, no forced lead

| Field | Value |
|---|---|
| Inputs | eGFR 38, no prior creatinine; ferritin 420 µg/L, TSAT 58%; TSH 14 mIU/L, free T4 low |
| Findings | Three consolidated findings: reduced eGFR of undetermined chronicity (`RE-F10`); possible iron overload (`IRIN-F3`); overt hypothyroidism (`THY-F1`) |
| Urgency | All three within weeks |
| Tier | All three **Tier 1** |
| Co-leads | **None forced.** No governed rule establishes co-equality between any two, and no governed distinguisher separates them |
| Visibility | All three visible as Tier 1 concerns |
| Cap behaviour | The two-co-lead ceiling is not breached because no co-leads are designated — per the Anthony product decision (§3), the cap is a maximum, not a requirement |
| Prohibited | Selecting two co-leads by cross-domain severity comparison (contract §18.24); suppressing the third to satisfy a display convention (clinician-first §10) |
| Missing-data | Renal finding states acute change could not be assessed without a prior creatinine (`UWC-2`) |
| Demonstrates | Clinician prioritisation, not display convenience |

### `XD-AS-33` — indeterminate severity (TSH without free T4)

| Field | Value |
|---|---|
| Inputs | TSH 14 mIU/L; free T4 not measured; no other abnormality |
| Consolidated finding | Indeterminate thyroid-axis abnormality (`THY-F5`, via `THY-IND-1`) |
| Missing modifier | Free T4 |
| Consequence class | Indeterminate severity (contract §8.1) |
| Urgency | Within weeks |
| Severity | Indeterminate — not resolved to either state |
| Tier | Tier 1 |
| Role | Principal concern |
| Required output | Both plausible states stated (subclinical/overt hypothyroidism); free T4 named and recommended |
| Prohibited | Worst-case inference (contract §18.25); default-low inference (contract §6.1); tier/prominence suppression (contract §4.5, §8.1) |
| Demonstrates | A missing modifier produces a declared indeterminate state, not an inference in either direction |

### `XD-AS-34` — insufficient data (calcium without albumin)

| Field | Value |
|---|---|
| Inputs | Total calcium 2.05 mmol/L; albumin not measured; all other analytes normal |
| Consolidated finding | None for calcium — uncorrected calcium is not a clinical quantity without albumin |
| Missing modifier | Albumin |
| Consequence class | Insufficient data (contract §8.1; `UWC-1`) |
| Tier | Not applicable — no finding created |
| Required output | Insufficient-data state, visible, albumin named as required modifier |
| Prohibited | Creating a hypocalcaemia finding from the uncorrected value; representing calcium as normal; silently omitting the question |
| Placement | Presented alongside other findings; may not take the lead (contract §16.2 as scoped) |
| Demonstrates | The second missing-modifier consequence, distinct from `XD-AS-33` |

### `XD-AS-35` — Tier 0 withheld, not downgraded

| Field | Value |
|---|---|
| Inputs | K⁺ 6.8 mmol/L; no repeat sample; eGFR 55 |
| Consolidated finding | Hyperkalaemia with renal impairment (`RE-F9`) |
| Clinical classification | **Tier 0.** Same day. Made and recorded regardless of release state |
| Runtime state | **Withheld — specification-only.** Tier 0 operational pathway not authorised (R1) |
| Auditability | Classification, firing rule, and fact of withholding all recorded |
| Prohibited — downgrade | Presenting as Tier 1 or Tier 2 (contract §17, §18.19; clinician-first §9) |
| Prohibited — no-concern | Treating the withheld state as no-concern, or omitting the finding |
| Expected user-facing state | The finding is present and visible; only the same-day action-and-timeframe guidance is withheld |
| Demonstrates | Clinical classification and runtime release state are independent |

### `XD-AS-36` — disease-name quarantine

| Field | Value |
|---|---|
| Inputs | Ferritin 420 µg/L; TSAT 58%; ALT, ALP and all other hepatic analytes normal |
| Consolidated finding | Possible iron overload (`IRIN-F3`, via `IRIN-OV-1`) |
| Urgency | Within weeks |
| Tier | Tier 1 |
| Role | Principal concern |
| Finding visible | **Yes**, in full |
| Consumer-facing wording | Must use the clinician-first §14 permitted set — biochemical pattern, warrants investigation, may be associated with |
| Prohibited consumer-facing | Naming haemochromatosis, or wording implying a genetic diagnosis (HFE genotyping not performed) |
| Permitted internally | Disease concept may remain in internal provenance, rule identifiers, clinical source material, approved clinician-facing material |
| Dependency | `REGULATORY_DEPENDENCY` — consumer-facing release of any disease name remains R4, not decided here |
| Demonstrates | Quarantine constrains the label, not the finding |

## 9. Formal domain scenarios (new) — haematology

Formalises and supersedes `HAEM-EX-1` through `-6` (§10). Full detail reproduced from the medical adjudication §11; no underlying clinical result has changed.

| ID | Inputs | Finding | Urgency | Severity | Tier | Role | Supporting/context | Missing-data | Override | Action class | Dependency |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `HAEM-AS-1` | Platelets 18×10⁹/L; Hb 128 g/L (M); MCV 92 fL | Severe thrombocytopenia (`HAEM-F4`) | Same day | Severe (<20) | Tier 0 | Principal concern | Hb 128 marginally below male threshold, separate mild finding, does not compete | None; no film — standing limitation stated | None fired (`HAEM-OV-4` inapplicable) | Immediate; pseudothrombocytopenia confirmation caveat mandatory | `TIER_0_PATHWAY_DEPENDENCY` |
| `HAEM-AS-2` | Hb 95 g/L; MCV 78 fL; platelets normal | Anaemia, microcytic subtype — one finding (`HAEM-F1` via `HAEM-OV-6`) | Within weeks | No sub-band exists (A5 declined) | Tier 1 | Principal concern | MCV is a constituent, not separate; iron supplies aetiology, anaemia never appears twice (U15) | Ferritin, if absent, stated as not assessable | `HAEM-OV-6` | Further investigation | None |
| `HAEM-AS-3` | MCV 99.5 fL; remainder of FBC normal | Isolated macrocytosis (`HAEM-F2`) | Routine | Mild macrocytosis | **Tier 2, unconditionally** | Determined by wider panel — principal concern if no higher-tier finding exists; contextual if a hepatic/nutritional parent exists within the mild-band boundary | n/a | None | `HAEM-OV-3` does not fire | Monitor/planned reassessment | None. **The hepatic Tier 1 floor must not be applied here** (`XD-HEP-FLOOR-2`) |
| `HAEM-AS-4` | MCV 99.5 fL; platelets 140×10⁹/L; Hb 118 g/L (F) | Multi-lineage cytopenia — one finding (`HAEM-F10`) | Within days | Individually low-tier; combination governs | Tier 1 | Principal concern | Individual cytopenias are constituents, not separate concerns | No film — standing limitation, stated | `HAEM-OV-1` (two lineages reduced) | Further investigation | None |
| `HAEM-AS-5` | ANC 0.4×10⁹/L; remainder of FBC normal | Severe neutropenia (`HAEM-F6`) | Same day | Severe (<0.5) | Tier 0 | Principal concern | n/a | Ancestry not captured, no adjustment made (`XD-ANC-1`), limitation stated | None | Immediate | `TIER_0_PATHWAY_DEPENDENCY` |
| `HAEM-AS-6` | Total WCC 3.1×10⁹/L; no differential; remainder of FBC normal | **Two states**: (1) low total WCC — valid finding; (2) neutrophil question — insufficient data | (1) Within weeks | (1) Not specified; (2) not applicable | (1) Tier 1; (2) n/a | (1) Principal concern | n/a | (2) Insufficient data — absolute differential is a governed modifier of total WCC and is required to answer the neutrophil question (contract §8.1; `HAEM-IND-2`) | None | Further investigation; repeat with differential | None |

## 10. Retired, replaced and duplicate scenario register

| Status | Scenario(s) | Reason | Replacement |
|---|---|---|---|
| Confirmed literal duplicate (retained, not removed) | `CONTRACT-FIX-1` = `HEP-AS-1` | Identical panel, identical outcome | n/a — both citations preserved for traceability |
| Retired, superseded | `HAEM-EX-1` to `-6` (all six, informal) | Replaced by formal scenarios with complete field sets and no change in underlying clinical result | `HAEM-AS-1` to `-6` (§9) |
| Retired, superseded (basis changed, not merely relabelled) | `CN-AS-11` | Premise ("no governed vitamin D threshold exists") is medically stale — A8 adjudication closed a governed threshold before this scenario's premise was written | `XD-AS-26` (unchanged, already in the estate) |
| Corrected in place (same ID, not retired) | `HEP-AS-4`, `RE-AS-2`, `RE-AS-11`, `HEP-AS-10` | Stale or incomplete wording aligned to already-closed adjudications; no new clinical decision | n/a — same scenarios, corrected text |

## 11. Coverage matrix against all 26 mandatory behaviours

| # | Mandatory behaviour | Covering scenario(s) | Status |
|---|---|---|---|
| 1 | Interpretability before prioritisation | `HEP-AS-11`, `RE-AS-7`, `THY-AS-4`/`XD-AS-33` | Covered |
| 2 | Domain-specific severity bands | `HEP-AS-3`, `RE-AS-1`/`XD-AS-31`, `IRIN-AS-1`/`-2`, `THY-AS-2`, `CN-AS-3`/`-4` | Covered |
| 3 | Urgency independently from severity | `CONTRACT-FIX-1`/`HEP-AS-1`, `XD-AS-31` | Covered |
| 4 | "More serious tier wins" | **`XD-AS-31`** | Covered (new) |
| 5 | Consolidation before prioritisation | `HEP-AS-1`, `XD-AS-25`, `CN-AS-5` | Covered |
| 6 | Same-domain frame consolidation | `XD-AS-25`, `CN-AS-5`, `HAEM-AS-2`/`-4` | Covered |
| 7 | Cross-domain duplicate consolidation | `XD-AS-4`/`-5`, `IRIN-AS-10`/`-11`, `HEP-AS-8`/`-9` | Covered |
| 8 | Direct finding vs contextual/phenotype | `XD-AS-10`, `HEP-AS-13`, `HAEM-AS-3` | Covered |
| 9 | Independent secondary concerns | `XD-AS-4`, `RE-AS-13`, `IRIN-AS-11` | Covered |
| 10 | Ordinary co-lead behaviour | `HEP-AS-9` | Covered |
| 11 | Same-day co-equal concern groups | `XD-AS-1`/`-7`/`-12`, `RE-AS-12`, `CN-AS-12` | Covered |
| 12 | Ordinary two-co-lead cap below same-day band | **`XD-AS-32`** | Covered (new) |
| 13 | Supporting-marker nesting | `HEP-AS-8`, `XD-AS-3`/`-28` | Covered |
| 14 | Modifiers that change urgency/severity | `RE-AS-8`, `IRIN-AS-3` | Covered |
| 15 | Override behaviour | `HAEM-AS-1`/`-4`/`-5`, `RE-OV`/`IRIN-OV` examples across matrix | Covered |
| 16 | Insufficient-data behaviour | `RE-AS-7`, `XD-AS-9`/`-16`, **`XD-AS-34`** | Covered |
| 17 | Indeterminate-severity behaviour | `THY-AS-4`, `HEP-AS-11`, **`XD-AS-33`** | Covered |
| 18 | Missing modifiers, no worst-case inference | **`XD-AS-33`**, **`XD-AS-34`**, `HAEM-AS-6` | Covered (new — both directions now demonstrated) |
| 19 | Pregnancy-dependent suppression/limitation | `XD-AS-19`, `THY-AS-9` | Covered |
| 20 | Sex-dependent interpretation | `XD-AS-20`/`-20b` | Covered |
| 21 | No-concern output | `XD-AS-11`, `HEP-AS-12`, `RE-AS-14`, `IRIN-AS-12`, `THY-AS-12`, `CN-AS-13` | Covered |
| 22 | Tier 0 specification-only and withheld behaviour | All Tier 0 scenarios; `RE-AS-1`, `HEP-AS-2`/`-3` | Covered |
| 23 | Tier 0 non-downgrade behaviour | **`XD-AS-35`** | Covered (new) |
| 24 | Quarantined disease-name, FIB-4, CV-risk capabilities | `XD-AS-17` (CV-risk), `XD-AS-18`/`HEP-AS-10` (FIB-4), **`XD-AS-36`** (disease-name) | Covered (fully, new for disease-name) |
| 25 | Hepatic pilot regression behaviour | `CONTRACT-FIX-1`/`HEP-AS-1` | Covered |
| 26 | Clinician-first lead selection across unlike domains | `XD-AS-1`/`-7`/`-12`, **`XD-AS-32`**, product ratification §3-§9 | Covered |

**All 26 mandatory behaviours are explicitly covered with a deterministic expected outcome or a correctly specified constrained state.** No behaviour is marked covered on the strength of an implicit or inferred outcome.

## 12. Contradiction-resolution record

All conflicts identified in v1.0 are resolved. No new conflict was introduced by this rebuild.

| # | Conflict | Resolution | Authority |
|---|---|---|---|
| 1 | `HEP-AS-4` presented two outcomes | Corrected to Tier 1 only | `HEP-U1` closed (register B1); medical adjudication Item H |
| 2 | `RE-AS-2` presented two outcomes | Corrected to Tier 0 only | `RE-U1` closed (register B2); medical adjudication Item B, H |
| 3 | `CN-AS-11` contradicted `XD-AS-26` | `CN-AS-11` retired, not relabelled | A8 closed; medical adjudication Item H |
| 4 | `RE-AS-11` presented an either/or outcome from two incompatible domain clauses (`RE-CONS-3` vs `RE-U-W-4`) | `RE-CONS-3` (categorical taxonomy rule) governs over `RE-U-W-4` (incidental band listing); orphan handling per contract §6.5 | Medical adjudication §5, Item A |
| 5 | `HAEM-EX-6` conflated two distinct states (indeterminate vs insufficient data) into one ambiguous entry | Disambiguated into two coexisting states within `HAEM-AS-6`: a valid low-WCC finding, and a separate insufficient-data state for the neutrophil question | Medical adjudication §11, Item G6 |
| 6 | `HAEM-EX-3`'s "no lead from this domain" framing conflated tier with role | Clarified: the Tier 2 classification is unconditional; only the lead/contextual role depends on the wider panel | Medical adjudication §11, Item G3b |

**Zero unresolved clinical conflicts remain.**

## 13. Dependency register

Approval of a scenario confirms its specification only. None of the following is closed by that approval.

| Class | Items |
|---|---|
| `REGULATORY_DEPENDENCY` | Consumer-facing disease-name release (R4, `XD-AS-36`); population exclusions/intended-purpose wording (R5); renal/electrolyte release with Tier 0 suppressed (R6) |
| `TIER_0_PATHWAY_DEPENDENCY` | R1 — every Tier 0 scenario (`XD-AS-1`/`-1b`/`-7`-`-9`/`-12`/`-13`/`-23b`/`-31`/`-35`, `HEP-AS-2`/`-3`, `RE-AS-1`/`-3`/`-9`/`-12`, `IRIN-AS-9`, `CN-AS-1`/`-2`/`-9`/`-12`, `HAEM-AS-1`/`-5`) — specification approvable now; activation blocked until the contract §17 pathway is authorised |
| `QUESTIONNAIRE_DEPENDENCY` | `XD-AS-19`, `XD-AS-20b`, `THY-AS-9` — specification approvable; operational reliance on the pregnancy-known path remains architecturally unreachable through the canonical questionnaire pending remediation |
| FIB-4 / cardiovascular-risk quarantine | R2 (`XD-AS-17`), R3 (`XD-AS-18`, `HEP-AS-10`) — specification correctly reflects quarantine; capability activation remains blocked |
| Disease-name release | R4 (`XD-AS-36`) — finding is fully visible; only the diagnostic label is withheld pending regulatory decision |

## 14. Non-blocking carry-forward register

None of the following blocks acceptance-scenario approval. They are recorded so they are not lost or mistaken for approval-blocking issues.

| Item | Nature | Why non-blocking |
|---|---|---|
| Governed urea:creatinine combination rule | Future medical enhancement, deliberately not created | `RE-AS-11` is fully resolved without it (medical adjudication §5.4) |
| `RE-U5` (whether urea ever forms an independent finding with clinical context) | Open clinical research question in the renal ruleset | Unaffected by, and not required for, `RE-AS-11`'s resolution |
| Hepatic ruleset relabel to v0.6.3 | Documentation/administrative | Later cross-domain authority already governs regardless of the label |
| Questionnaire rationalisation and enforcement remediation | Implementation, deferred | Blocks release and runtime reliance on questionnaire context, not scenario-specification approval |
| Regulatory/legal release dependencies generally (R1-R6) | External authority | Blocks activation/release of the associated capability, not the specification |

**Distinctions preserved:** acceptance-scenario completeness (this pack, achieved) is separate from future clinical enhancement (urea:creatinine, not pursued here), regulatory closure (R1-R6, unaffected), implementation readiness (a Package A deliverable per the architecture-hardening report), and release readiness (gated by all of the above plus questionnaire remediation).

## 15. Scenarios ready for Anthony's approval

**All 109 unique active scenarios** in the estate (§17) are ready for approval, including all Tier 0, regulatory-quarantined, and questionnaire-dependent scenarios — approval of those confirms only that the expected specification is correct and internally consistent, per the approval boundary (§2).

## 16. Scenarios not ready for approval

**None.** Every scenario previously excluded in v1.0 (`HEP-AS-4`, `RE-AS-2`, `CN-AS-11`, `HAEM-EX-1` to `-6`) has been corrected, retired-and-replaced, or formalised, per §7, §9, §10. No scenario in the current estate carries an unresolved conflict, an incomplete required field, or a non-deterministic expected outcome.

## 17. Scenario-count reconciliation

Shown transparently, not by mechanical addition of the six new items to the old total.

**v1.0 unique active total:** 104 (105 raw entries, minus 1 confirmed literal duplicate).

**Changes applied:**

| Change | Effect |
|---|---|
| Add `XD-AS-31` to `-36` (six new cross-domain scenarios, authored by the medical adjudication) | **+6** |
| Retire `CN-AS-11` (superseded by `XD-AS-26`, which already existed in the v1.0 count — no replacement scenario added) | **-1** |
| Replace `HAEM-EX-1` to `-6` (six informal entries) with `HAEM-AS-1` to `-6` (six formal entries) | **+0 net** (one-for-one formalisation, not an addition) |
| Correct `HEP-AS-4`, `RE-AS-2`, `RE-AS-11`, `HEP-AS-10` in place | **+0** (same IDs, corrected text, no count change) |

**v1.1 unique active total: 104 + 6 - 1 + 0 + 0 = 109.**

**Verification by direct count:** `XD-AS-*` (33 original + 6 new = 39) + `HAEM-AS-*` (6) + `HEP-AS-*` (14, includes `AS-1` = duplicate of `CONTRACT-FIX-1`) + `RE-AS-*` (14) + `IRIN-AS-*` (12) + `THY-AS-*` (12) + `CN-AS-*` (13 originally authored, minus 1 retired = 12) = 39+6+14+14+12+12+12 = **109.** Matches.

**Raw historical entry count** (every literal entry ever authored across all inspected documents, including retired/superseded ones, for full traceability): 1 (`CONTRACT-FIX-1`) + 39 (`XD-AS`, current) + 6 (`HAEM-EX`, retired) + 6 (`HAEM-AS`, current) + 14 (`HEP-AS`) + 14 (`RE-AS`) + 12 (`IRIN-AS`) + 12 (`THY-AS`) + 13 (`CN-AS`, including retired `AS-11`) = **117.**

**Reconciliation:** 117 raw - 1 duplicate (`CONTRACT-FIX-1`) - 7 superseded (6 `HAEM-EX` + 1 `CN-AS-11`) = **109 unique active.** Matches both prior calculations.

| Metric | Count |
|---|---|
| Raw historical entries | 117 |
| Confirmed duplicates | 1 |
| Superseded/retired | 7 |
| Unique active scenarios | 109 |
| Ready for Anthony approval | 109 |
| Excluded | 0 |
| Documented scenario gaps (behaviour-level) | 0 |
| Documented expectation gaps | 0 |
| Unresolved clinical conflicts | 0 |

## 18. Proposed Anthony approval statement

> I approve the complete Cross-Domain Clinical Prioritisation acceptance-scenario estate of 109 scenarios recorded in `HEALTHIQ_CROSS_DOMAIN_ACCEPTANCE_SCENARIO_APPROVAL_PACK_v1_1.md` §7-§10, as consistent with the ratified contract v0.6.3, cross-domain ruleset v0.5, HMR adjudication register v0.4, six-domain closure report v0.4, and the bounded Acceptance-Scenario Medical Adjudication v0.1.
>
> I confirm the expected consolidated finding, urgency, severity treatment, tier, role, supporting relationships, missing-data behaviour and action class recorded for each listed scenario.
>
> I confirm the no-forced-lead product decision: where three or more clinically distinct, non-same-day findings are equally ranked and no governed clinical distinguisher identifies a principal concern or a pair of co-leads, all such findings remain visible in their governed tier, no lead is forced, and no two are manufactured as co-leads.
>
> This approval does not alter any clinical rule, threshold, band, override or adjudication. It does not close any regulatory or legal dependency (R1-R6). It does not authorise Tier 0 activation. It does not authorise consumer-facing disease-name release. It does not authorise reliance on unresolved or unenforced questionnaire context. It does not authorise implementation, Cursor prompt authoring, or release.

**This statement has not been issued. It is proposed for Anthony's decision.**

## 19. Contract §23.6 condition 7 verdict

`READY_FOR_ANTHONY_ACCEPTANCE_SCENARIO_APPROVAL`

All medically identified scenario defects from v1.0 are incorporated and resolved (§7-§10, §12). All 26 mandatory behaviours are explicitly covered with a deterministic expected outcome (§11). No unresolved clinical conflict remains (§12). Every one of the 109 unique active scenarios carries one deterministic expected outcome or a correctly specified constrained state (indeterminate-severity and insufficient-data states are constrained, not ambiguous). The remaining dependencies (§13) are explicitly non-medical — regulatory, Tier 0 activation, and questionnaire enforcement — and do not prevent specification approval.

---

**No clinical rule, threshold, adjudication, or new clinical action was created, amended, or reopened by this pack. No code, schema, test, or Cursor prompt was authored. Anthony's approval of the scenario estate has not been presumed or recorded — §18 proposes the statement; it has not been issued.**
