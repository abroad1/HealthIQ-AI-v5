# HealthIQ AI — Pre-Sprint 1 Decision Pack

**Date:** 2026-05-06  
**Revised:** 2026-05-09 v4 — all decisions recorded from Anthony Broad; gate checklist updated  
**Purpose:** Close the Pre-Sprint 1 gate defined in the final Launch-Core Transformation Plan.  
**Status:** Decisions recorded — one ownership item remains open (QA/UAT named human). Gate cannot formally close until that item is assigned.

---

## How to use this pack

This pack closes the Pre-Sprint 1 gate. Anthony reviews proposed defaults, makes binding decisions, and signs off.

**Anthony's job in this document:**
- ~~confirm or override each proposed default~~ — **done**
- assign named QA/UAT owner — **done**
- sign off at §5 — **done**

**Not Anthony's job:**
- populate evidence or verification fields — those are done
- fill in ownership by role — those are done

**Gate is complete when:** every item has a Final decision, the checklist is fully closed, and §5 is signed.

### Time-box
Pre-Sprint 1 is hard-limited to **one calendar week** from gate open date.

---

## 1. Decision authority

| Item | Entry |
|---|---|
| Named decision authority | **Anthony Broad** |
| Date authority confirmed | 2026-05-09 |
| Operating model | Anthony decides. GPT pressure-tests strategy. Claude Code populates/hardens. Cursor implements. Binding defaults sit with Anthony alone. |

---

## 2. Ownership model

| Area | Owner | Status |
|---|---|---|
| Core engine decisions | GPT (architecture) + Claude Code (evidence/hardening) | Assigned — advisory role |
| Frontend/report decisions | Cursor (implementation) | Assigned — implementation role |
| QA/UAT and proving decisions | **Anthony Broad** | **CLOSED — sole human QA/UAT owner for Pre-Sprint 1 and Sprint 5 proving** |
| Programme/docs coordination | Anthony Broad (or named delegate) | Assigned unless delegated |

**QA/UAT ownership decision:** Anthony Broad will act as the named human QA/UAT owner for gate closure and proving until or unless he delegates this later.

---

## 3. Decision register

---

## 3.1 Launch-core biology slice

**Question:** What biological slice are we proving in this phase?

| Field | Entry |
|---|---|
| Owner | Core engine owner (GPT + Claude Code) |
| Evidence reviewed | Verification ledger (2026-05-04): both AB and VR UK commercial panels (82 biomarkers each) produce `signal_homocysteine_elevation_context` as the lead finding with 4 governed hypotheses and zero fallback strings across 12 runs. 37 signals registered for governed WHY. Market positioning paper: cardiometabolic, lipid, vascular, and inflammatory domains are the first-wedge commercial priority. |
| Proposed default | **The active signal set that fires on the AB and VR representative panels, comprising:** `signal_homocysteine_elevation_context` (lead, both panels), `signal_homocysteine_high` (rank 2 AB), `signal_mcv_high` (rank 3 AB), `signal_apoa1_cardio_risk` (rank 5 AB), `signal_ldl_high` (rank 7 AB), `signal_alp_low` and `signal_hypercortisolism` (VR co-primaries). This is wider than a homocysteine-only demo slice and narrower than the full 37-signal estate. It maps to the homocysteine / methylation / cardiometabolic / lipid cluster — the slice the engine handles best and that has strongest commercial relevance. |
| Alternative options considered | (1) Narrower: homocysteine-only — too narrow for commercial credibility. (2) Wider: full 37-signal WHY estate — uncontrolled WHY expansion, violates programme stance. |
| **Final decision** | **CLOSED — 2026-05-09.** Approved: the bounded slice comprising the active signal set already proven on AB and VR — the homocysteine / methylation / cardiometabolic / lipid cluster as named in the proposed default. No additions, no narrowing. |
| Decision date | 2026-05-09 |
| Notes | Sprint 1 WHY-authoring scope is bound to this signal list. Any signal outside this cluster does not receive WHY assets in Sprint 1. |

---

## 3.2 Launch-core frontend/report surface

**Question:** What exact launch-core surface are we proving?

| Field | Entry |
|---|---|
| Owner | Frontend owner (Cursor) |
| Evidence reviewed | Verification ledger (2026-05-04): all four main surfaces are populated with governed content at runtime — `consumer_domain_scores` (bands, headlines, consequence sentences), `narrative_report_v1` (retail_summary, lead_narrative, next_steps_narrative), `clinician_report_v1.sections.page1` (primary concern, key findings, chains, runner-up, confidence), `interpretation_display_layer_v1` (11 records, 4 enabled on AB). |
| Proposed default | **Primary hero + consumer domain cards + clinician/PDF surface.** Concretely: `narrative_report_v1` + `consumer_domain_scores` + `clinician_report_v1`. IDL / Section 5 is handled separately in §3.8. This covers what a paying user reads and what a clinician receives — the minimum coherent end-to-end proving surface. |
| Alternative options considered | Excluding clinician/PDF — would leave the clinician value proposition untested, which is commercially important for the first-wedge buyer (blood-testing companies, longevity clinics). |
| **Final decision** | **CLOSED — 2026-05-09.** Include all working parts needed to prove the pipeline is firing correctly. Do not artificially narrow the proving surface. The intent is to test the whole end-to-end pathway, not a cosmetically reduced subset. Clinician/PDF surface is in. IDL surface is in (see §3.8). |
| Decision date | 2026-05-09 |
| Notes | The full proving surface is: `narrative_report_v1` + `consumer_domain_scores` + `clinician_report_v1` + `interpretation_display_layer_v1` (IDL). No surface that is working and governs output is to be excluded from proving. |

---

## 3.3 Medication proving category

**Question:** Which single medication/drug category proves the modifier architecture?

| Field | Entry |
|---|---|
| Owner | Core engine owner (GPT + Claude Code) |
| Evidence reviewed | Transformation plan recommends statins: directly relevant to lipid interpretation (LDL/HDL effects), clinically understandable, commercially plausible. Both AB and VR panels fire lipid signals (`signal_ldl_high`, `signal_apoa1_cardio_risk`) where statin context is directly meaningful. Market positioning paper: lipid transport is a first-priority commercial domain. |
| Proposed default | **Statins.** Statin use affects LDL, HDL, triglycerides, and liver enzymes (ALT/AST) — all present in the AB and VR panels. A statin-aware modifier produces visible, defensible effects on the most commercially relevant panel findings. |
| Alternative options considered | Corticosteroids (already a caveat class — less commercially central), Metformin (glycaemic signals are weaker panel leads), HRT (meaningful but narrower first-wedge relevance). |
| **Final decision** | **CLOSED — 2026-05-09.** Statins. |
| Decision date | 2026-05-09 |
| Notes | Statin modifier prerequisites are deferred to the pre-Sprint 2 gate — see §3.4. This decision does not change; the sequencing of when the prerequisites are delivered changes. |

---

## 3.4 Medication governance source

**Question:** Where does the governed truth for the chosen medication category live, and is it real enough to support Sprint 2?

| Field | Entry |
|---|---|
| Owner | Core engine owner (GPT + Claude Code) |
| Current artefact/path | `backend/core/analytics/medication_caveat_assembler_v1.py` — the only medication-related backend asset. |
| Governing schema | None. The caveat assembler produces a bounded free-text caveat string only. No drug modifier schema, no modifier engine, no governed drug-effect YAML. |
| Current state verified? | **YES — verified by repo inspection (2026-05-09).** |
| Verification result | **No statin modifier path exists anywhere in the codebase.** `medication_caveat_assembler_v1.py` handles three medication classes (Corticosteroids, Atypical antipsychotics, HIV/AIDS treatments) as text caveats only — not as analytical modifiers. `backend/ssot/questionnaire.json` `long_term_medications` question does not include statins. No drug modifier engine comparable to `LifestyleModifierEngine` exists. No statin-effect YAML or schema exists. |
| What Sprint 2 needs that does not exist | (1) Statin capture added to `questionnaire.json` and `questionnaire_mapper.py`. (2) A drug modifier engine (analogous to `LifestyleModifierEngine`) with a governed schema. (3) A governed statin-effect asset (YAML or equivalent) for lipid signal modifiers. (4) Wiring of the modifier to at least one user-visible surface. |
| **Blocker status** | **CONFIRMED BLOCKER for Sprint 2.** Sprint 2 cannot be scoped on the assumption that this infrastructure exists — it does not. |
| Proposed default | **Anthony must choose one of two paths:** |
| | **Option A — Sprint 1 carries the statin prerequisites.** Sprint 1 scope includes: questionnaire addition, drug modifier engine, statin asset authoring via KB pipeline, surface wiring. This is medium-large scope on top of the analytical hardening work. Sprint 1 becomes a heavier sprint. Recommended if medication proving is a firm Sprint 2 commitment. |
| | **Option B — Statin prerequisites become a separate pre-Sprint 2 gate.** Sprint 1 focuses on analytical hardening and WHY assets only. A separate gate before Sprint 2 is authored confirms the statin modifier is delivered. Sprint 2 authoring is blocked until that gate closes. |
| **Final decision** | **CLOSED — 2026-05-09. Option B.** Statin modifier prerequisites become a separate pre-Sprint 2 gate. Sprint 1 stays focused on analytical hardening and WHY assets only. Sprint 2 authoring is blocked until the pre-Sprint 2 gate is confirmed closed. Additionally: the questionnaire must be reduced to the minimum proving set so human testing remains practical during this phase. |
| Decision date | 2026-05-09 |
| Notes | Sprint 2 must not be drafted until the pre-Sprint 2 statin gate closes. This gate must confirm: (1) statin capture in `questionnaire.json` and `questionnaire_mapper.py`, (2) a governed drug modifier engine and statin-effect asset, (3) surface wiring on at least one user-visible field. The Sprint 2 prompt front matter must state this gate as a prerequisite. Check 3 in §3.10 is correspondingly gated — see that section. |

---

## 3.5 Silent-WHY handling policy

**Question:** For active findings without governed WHY, what is the launch-core policy?

| Field | Entry |
|---|---|
| Owner | Core engine owner (GPT + Claude Code) |
| Evidence reviewed | Verification ledger (2026-05-04): AB panel — active suboptimal findings with no governed WHY at ranks 2 (`signal_homocysteine_high`), 3 (`signal_mcv_high`), 5 (`signal_apoa1_cardio_risk`), 7 (`signal_ldl_high`). VR panel — ranks 4 (`signal_hypercortisolism`), 6 (`signal_cortisol_high`), 7 (`signal_creatine_kinase_high`). Fallback string `"No hypothesis set available for this concern in v1."` exists in `report_compiler_v1.py:535` but is poor UX if surfaced to users. |
| Proposed default | **Two-part policy:** (1) Add governed WHY assets in Sprint 1 for the launch-core silent signals in the top 5: `signal_homocysteine_high`, `signal_mcv_high`, `signal_ldl_high`. `signal_apoa1_cardio_risk` may be handled by deduplication against the canonical lipid-transport signal — to be confirmed during Sprint 1 authoring. (2) Suppress from user-visible top-findings rendering any active signal outside the launch-core slice that lacks governed WHY. Fallback string visible only in clinician surfaces. |
| **Final decision** | **CLOSED — 2026-05-09.** Sprint 1 must build the governed WHY assets needed to support: the chosen test panel (AB + VR), the minimal proving questionnaire, and the drug-usage pathway. This is targeted WHY completion for the proving slice only — not broad WHY expansion. The objective is to verify that governed WHY is actually triggering correctly across the launch-core use case. No governed WHY outside the proving slice is to be authored in Sprint 1. |
| Decision date | 2026-05-09 |
| Notes | This replaces the proposed two-part policy. The suppression logic for out-of-slice signals without governed WHY remains as a consequence of scoping, but the primary stance is: complete the WHY assets for the proving slice rather than relying on suppression as the mechanism. The signals requiring WHY in Sprint 1 are those in the §3.1 biology slice that currently carry the fallback string. |

---

## 3.6 Legacy `insights[]` disposition

**Question:** What happens to the legacy `insights[]` surface on the launch-core path?

| Field | Entry |
|---|---|
| Owner | Programme/docs (decision); Frontend / Cursor (implementation) |
| Evidence reviewed | Verification ledger (2026-05-04): all 12 runs emitted 6 identical generic placeholder entries — `manifest_id: legacy_v1`, empty `biomarkers`, empty `drivers`, empty `evidence`, `confidence: 0.72`. Content is panel-invariant and profile-invariant. Frontend inspection (2026-05-09): `analysis_result.insights` is actively consumed at `frontend/app/(app)/results/page.tsx:141`, `frontend/app/(app)/actions/page.tsx:62`, `frontend/app/state/clusterStore.ts:467`, and `frontend/app/lib/resultsPageLayout.ts:387`. `InsightsPanel.tsx` and `InsightCard.tsx` exist with full rendering logic. The insights[] data IS being rendered to users via the clusterStore and results/actions pages. |
| Proposed default | **Gate behind a feature flag (`HEALTHIQ_LEGACY_INSIGHTS=false` off by default) as Sprint 1 carriage work, then rebuild from `top_findings` + `interpretation_display_layer_v1` + `root_cause_v1` in Sprint 4.** Outright removal is not safe: multiple active frontend paths consume `analysis_result.insights` including the clusterStore state management. Gating with the flag off ensures the placeholder content is invisible to users without breaking the consuming code. |
| **Final decision** | **CLOSED — 2026-05-09.** Retire `insights[]` as an intelligence layer. Replace it with a presentation projection derived from: `top_findings`, `consumer_domain_scores`, `root_cause_v1`, `interpretation_display_layer_v1`, `narrative_report_v1`. Start the removal process now. Once the replacement projection is tested safe, delete `insights[]` from the pipeline and frontend entirely — it must not be allowed to re-emerge as a parallel source of truth. |
| Decision date | 2026-05-09 |
| Notes | Implementation must audit and update all active frontend consumers before any deletion: `results/page.tsx:141`, `actions/page.tsx:62`, `clusterStore.ts:467`, `resultsPageLayout.ts:387`, `InsightsPanel.tsx`, `InsightCard.tsx`. The feature-flag gating approach from the proposed default remains available as a safety step during the transition, but the end state is full retirement and deletion, not permanent flag-gating. This work belongs to Sprint 4 carriage, but the decision to retire (not merely gate) is recorded now. |

---

## 3.7 Mock-mode honesty

**Question:** What does the user get told when runtime is `deterministic_mock`?

| Field | Entry |
|---|---|
| Owner | Frontend owner (Cursor, with Anthony approving wording) |
| Evidence reviewed | Verification ledger (2026-05-04): `meta.narrative_runtime.runtime_mode = "deterministic_mock"` on every run. Flag is not surfaced in user-visible narrative. Retail summary and `lead_narrative` use possessive language ("your measured homocysteine", "your cardiovascular read on this panel"). A paying user could reasonably read this as personalised AI output. The questionnaire producing near-zero visible payoff makes the impression worse. |
| Proposed default | Add a visible disclosure label on the retail report surface when Gemini is not active. Two wording options for Anthony to choose: |
| | **Option A (factual, minimal):** `"Analysis generated from your lab data using deterministic clinical rules."` |
| | **Option B (honest, warmer):** `"Your report is built from governed clinical rules applied to your lab data. AI-personalised narrative is not active in this view."` |
| | Placement: non-intrusive label in the report header or footer area, visible without scrolling. This is a small Sprint 4 carriage task. |
| **Final decision** | **CLOSED — 2026-05-09. Option B wording approved:** `"Your report is built from governed clinical rules applied to your lab data. AI-personalised narrative is not active in this view."` |
| Decision date | 2026-05-09 |
| Notes | This wording is approved as written. No modifications. Placement: non-intrusive label in the report header or footer, visible without scrolling. This is a Sprint 4 carriage task. |

---

## 3.8 Section 5 / IDL consumer-surfacing decision

**Question:** Should the already-live IDL be surfaced to consumers in the launch-core slice, or deferred to Phase 1.1?

| Field | Entry |
|---|---|
| Owner | Frontend owner (Cursor, with Anthony deciding) |
| Evidence reviewed | Verification ledger (2026-05-04): AB panel returns 11 IDL records, 4 enabled for frontend — "Vascular Inflammation Risk" (`strong_signal`, `clinical_only`), "Methylation pathway pattern" (`strong_signal`, `phenotype_allowed`), "LDL in context" (`phenotype_allowed`). Each record has `why_it_matters`, `severity_state`, `frontend_allowed_term`, `display_order_priority`, `supporting_biomarkers_summary`. `InterpretationPatternsSection.tsx` exists and reads these records. |
| Proposed default | **Surface IDL in the launch-core slice.** The content is live, governed, and non-placeholder. Pattern-level reasoning across markers is the strongest visible demonstration of specialist-grade interpretation to a first commercial buyer. `clinical_only` records must be gated from consumer surfaces (this is already defined in the IDL contract). `phenotype_allowed` records are consumer-safe and ready. Deferring leaves a proven differentiator invisible during proving. |
| **Final decision** | **CLOSED — 2026-05-09.** Include IDL in the launch-core proving surface. Not deferred. |
| Decision date | 2026-05-09 |
| Notes | IDL is part of the §3.2 full proving surface decision. The `clinical_only` gate must be verified as correctly enforced in the consumer rendering path before IDL records are exposed. `phenotype_allowed` records are consumer-safe and ready. This verification is a Sprint 4 carriage task. |

---

## 3.9 Layer B → Layer C boundary

**Question:** What is the exact boundary between Layer B truth and Layer C polish?

| Field | Entry |
|---|---|
| Owner | Core engine owner (GPT + Claude Code) |
| Current behaviour verified? | **YES — verified by repo inspection (2026-05-09).** |
| Verification result | **Layer B** produces `AnalysisDTO` with all structured analytical fields: `top_findings`, `consumer_domain_scores` (score, band_label, headline_sentence, consequence_sentence, next_step_sentence, confidence_tier), `insight_graph`, `root_cause_v1`, `clinician_report_v1.sections.page1` (all structured fields), `interpretation_display_layer_v1.records`, `actions`, `meta`. **Layer C (deterministic_mock — the production default):** `narrative_report_compiler_v1.py` reads IDL records, insight_graph, and three governed KB YAML assets and assembles five `narrative_report_v1` fields only: `retail_summary`, `lead_narrative`, `body_overview`, `next_steps_narrative`, `clinician_synthesis`. It does not touch any other DTO field. **Layer C (Gemini/LLM mode):** `synthesis.py` generates prose from the insight_graph; `validate_llm_output_v2` cross-checks output against structured truth before acceptance. |
| Proposed boundary | **Layer C MAY polish:** `narrative_report_v1` fields only — `retail_summary`, `lead_narrative`, `body_overview`, `next_steps_narrative`, `clinician_synthesis`. **Layer C MUST preserve exactly (zero modification):** all other AnalysisDTO fields — `top_findings` (ordering, ids, confidence, signal states), `consumer_domain_scores` (all structured fields including band_label and headline_sentence), `interpretation_display_layer_v1.records`, `root_cause_v1`, `clinician_report_v1.sections.page1`, `actions`, `meta`. **Layer C MUST NOT:** change the lead finding, alter any confidence score or band, alter runner-up designation, alter the hypothesis set, or produce narrative that contradicts structured truth already in the DTO. |
| **Final decision** | **CLOSED — 2026-05-09.** Approved as written, with the governing rule and full boundary list below. |
| Decision date | 2026-05-09 |
| Notes | In deterministic_mock (current production default) this boundary is already respected — the compiler is template-only. The Gemini path is the risk surface; `validate_llm_output_v2` is the guard. The guard's validation contract must be reviewed before Sprint 3 authors the Layer C payload. The boundary list below is permanent written authority — not chat history. |

### Approved Layer B → Layer C boundary

**Governing rule: Layer B decides. Layer C synthesises.**

#### Layer B must hand off the richest deterministic narrative contract possible, including:

##### 1. Core analytical verdicts
- lead finding
- runner-up
- ranked findings
- domain scores / banding
- confidence state
- missing-data state
- contradiction state

##### 2. Governed medical reasoning
- hypothesis / WHY set
- evidence-for
- evidence-against / limiting factors
- missing confirmatory markers
- pathway/system interpretation
- why it matters medically

##### 3. Personalisation/context outputs that actually fired
- lifestyle modifiers
- medication/drug modifiers
- relevant body-composition / age / sex context if used
- longitudinal context if available
- explicit statement of what changed because of those modifiers

##### 4. Narrative intent
For each section, Layer B should indicate what the prose is trying to do, for example:
- reassure
- prioritise
- explain mechanism
- express uncertainty
- frame next steps
- support clinician fast-read

##### 5. Wording and claim boundaries
- allowed consumer wording
- clinician-only wording
- prohibited claims
- allowed claim strength such as "suggests", "may reflect", "is consistent with"

#### Layer C may do only this
- translate structured truth into natural prose
- combine deterministic facts into coherent sentences
- improve readability, flow, tone, and audience fit
- personalise emphasis using fired deterministic modifiers

#### Layer C must not do this
- invent new medical reasoning
- change lead finding or ranking
- alter confidence or banding
- add causal claims
- introduce new evidence
- reinterpret absent data
- invent confounders or next steps
- produce claims outside the allowed wording boundaries

---

## 3.10 Human proving acceptance criteria

**Question:** What exact binary pass/fail criteria define success for the proving phase?

| Field | Entry |
|---|---|
| Owner | QA/UAT owner (Anthony Broad) |
| Criteria reviewed | Transformation plan §Pre-Sprint 1, verification ledger §6, gap map §3. Each check below closes a specific verified gap. |
| Proposed binary checks | **CHECK 1 — Lifestyle visible payoff.** Run a stressed profile (BMI 32, BP 158/96, smoker, 35 alcohol units/wk) and a healthy profile on the AB panel. At least one of `consumer_domain_scores[cardiovascular].band_label`, `.headline_sentence`, or `narrative_report_v1.retail_summary` must differ between profiles. → PASS / FAIL |
| | **CHECK 2 — Alcohol bridge in human language.** Run the stressed profile on AB panel. The alcohol-methylation bridge sentence must appear in `lead_narrative` in user-readable language (not the raw rationale code `alcohol_intake_moderate_or_higher_with_one_carbon_lab_coherence`). → PASS / FAIL |
| | **CHECK 3 — Medication modifier visible.** Run a statin-on vs statin-off profile pair on the AB panel. At least one user-visible field in `consumer_domain_scores`, `lead_narrative`, or `clinician_report_v1.sections.page1` must differ. → PASS / FAIL *(gated on §3.4 — statin modifier must exist)* |
| | **CHECK 4 — No legacy insights surface.** On the launch-core path, `analysis_result.insights[]` must contain no `legacy_v1` manifest entries visible to users. → PASS / FAIL |
| | **CHECK 5 — No band ↔ headline contradiction.** Cardiovascular `consumer_domain_scores.band_label: "stable"` must not co-exist with `headline_sentence` text that says "not a simple all-clear" without a governed explanation. → PASS / FAIL |
| | **CHECK 6 — Cross-section lead coherence.** On AB and VR panels, `clinician_report_v1.sections.page1.primary_concern` and `narrative_report_v1.retail_summary` must reference the same lead pattern. → PASS / FAIL |
| Binary checks defined? | **Yes — all six approved.** |
| **Final decision** | **CLOSED — 2026-05-09.** All six binary checks approved as written. |
| Decision date | 2026-05-09 |
| Notes | Check 3 (medication modifier visible) is gated on the pre-Sprint 2 statin gate (§3.4 Option B). Check 3 is a Sprint 5 proving item only after the pre-Sprint 2 gate has closed and the statin modifier is confirmed delivered. The Sprint 1 prompt must state this dependency explicitly. Checks 1, 2, 4, 5, 6 are not gated and apply from Sprint 5 onwards regardless. |

---

## 4. Gate closure checklist

| Item | Status | Notes |
|---|---|---|
| Decision authority named | **CLOSED** | Anthony Broad, confirmed 2026-05-09. |
| Ownership model assigned | **CLOSED** | Role-based owners confirmed. Anthony Broad assigned as named human QA/UAT owner. |
| Biology slice decided | **CLOSED** | Approved: homocysteine / methylation / cardiometabolic / lipid cluster, active signal set on AB + VR. See §3.1. |
| Frontend/report surface decided | **CLOSED** | All working surfaces included to prove the full pipeline. `narrative_report_v1` + `consumer_domain_scores` + `clinician_report_v1` + IDL. See §3.2. |
| Medication category decided | **CLOSED** | Statins. See §3.3. |
| Medication governance source verified and decided | **CLOSED — Option B.** | No statin modifier path exists (confirmed). Statin prerequisites deferred to a separate pre-Sprint 2 gate. Sprint 2 authoring blocked until that gate closes. See §3.4. |
| Silent-WHY policy decided | **CLOSED** | Sprint 1 must build targeted WHY assets for the proving slice (chosen panel + minimal questionnaire + drug-usage pathway). Not broad WHY expansion. See §3.5. |
| `insights[]` disposition decided | **CLOSED** | Retire as intelligence layer. Replace with projection from `top_findings`, `consumer_domain_scores`, `root_cause_v1`, `interpretation_display_layer_v1`, `narrative_report_v1`. Start removal now; delete fully once tested safe. See §3.6. |
| Mock-mode honesty decided | **CLOSED** | Option B wording approved as written. See §3.7. |
| IDL consumer-surfacing decided | **CLOSED** | IDL included in launch-core proving surface. See §3.8. |
| Layer B → Layer C boundary decided and reality-checked | **CLOSED** | Governing rule and full boundary list approved. Recorded as permanent written authority in §3.9. |
| Acceptance criteria translated into binary checks | **CLOSED** | All 6 checks approved. Check 3 gated on pre-Sprint 2 statin gate. QA/UAT owner to own execution once named. See §3.10. |
| Gate signed off | **READY FOR SIGN-OFF** | All decision items are now closed. Anthony Broad can formally sign off §5 and close the gate. |

---

## 5. Final sign-off

| Field | Entry |
|---|---|
| Decision authority | Anthony Broad |
| Sign-off | **Pending final signature by Anthony Broad — all ten decisions recorded and QA/UAT owner assigned. Gate is ready to close.** |
| Date closed | **Anthony Broad, confirmed 2026-05-09.** |
| Gate outcome | **Ready to close on Anthony sign-off** |
| Notes for Sprint 1 authoring | All decisions needed to author Sprint 1 are recorded. Anthony Broad is also the named QA/UAT owner for the proving phase unless and until delegated. Sprint 1 can proceed on the following confirmed scope: (1) WHY assets for the §3.1 biology slice — targeted completion for the proving slice only. (2) No statin modifier prerequisites — deferred to pre-Sprint 2 gate. (3) Questionnaire reduced to minimum proving set. (4) `insights[]` retirement initiated (implementation Sprint 4, but decision recorded now). (5) Mock-mode honesty wording confirmed for Sprint 4. (6) All 6 acceptance criteria confirmed; Check 3 gated on pre-Sprint 2 statin gate. |

---

## 6. Immediate next step after gate closure

Once this gate is signed off, the next artefact is the **Sprint 1 work package** for launch-core analytical hardening.

Sprint 1 prompt must include, at minimum:
- the confirmed named signal list from §3.1 — homocysteine / methylation / cardiometabolic / lipid cluster
- the targeted WHY authoring scope from §3.5 — only signals in the proving slice that currently carry the fallback string
- explicit statement that statin modifier prerequisites are **not** Sprint 1 scope (§3.4 Option B) and are deferred to a named pre-Sprint 2 gate
- the questionnaire scope constraint: minimum proving set only
- record that `insights[]` retirement decision is made (§3.6) — implementation is Sprint 4 carriage
- the mock-mode honesty wording is confirmed (§3.7) — implementation is Sprint 4 carriage
- reference to the Layer B → Layer C boundary authority in §3.9 as the governing contract for Sprint 3 payload design
- Check 3 gating note: medication-modifier proving check is gated on pre-Sprint 2 statin gate closure

No Sprint 1 implementation begins before this gate is signed.
