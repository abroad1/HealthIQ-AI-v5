# HealthIQ AI — Moat Roadmap and Sprint Plan
*Single document: Phase 1 detailed sprint plan + Phase 2/3 vision plan (for saving into the repo).*

## Executive intent
HealthIQ AI is building a **clinical-grade, deterministic biomarker analysis engine** with lab-range sovereignty, explicit knowledge assets, and replayable outputs. The near-term roadmap strengthens the **engine moat** (Phase 1), then builds a **dataset moat** (Phase 2), then reaches **outcomes + regulated workflows + strategic buyer fit** (Phase 3).

This plan is written to align with the existing KB-Sxx operating model (Automation Bus SOP v1.2, deterministic analytics, versioned knowledge assets).

---

## Phase 1 (0–18 months): Engine moat + governed knowledge production
**Goal:** become the best deterministic biomarker reasoning engine in the market, with a scalable “knowledge factory” that produces clinical-grade packages safely and quickly.

### Phase 1 success criteria (business-level)
- Users receive **connected** and **prioritised** findings (interaction mapping) rather than a checklist.
- Every finding and connection is **auditable**: versioned knowledge assets + deterministic replay.
- Coverage is broad across major domains and can expand weekly without schema drift.
- The platform is ready for longitudinal tracking (data structures stable), even before the UX is built.

### Phase 1 principles (non-negotiable)
- Deterministic computation only in analytics engine.
- Lab-range sovereignty preserved (ranges, one-sided bounds, band profiles + effective-from notes).
- Clinical logic is explicit, versioned, and reviewable (knowledge assets, not runtime inference).
- Additive changes with regression tests and clear acceptance baselines.

---

## Phase 1 — Detailed sprint plan
### Current baseline (completed)
- KB-S21: Signal contract authority (anti-drift).
- KB-S22: Investigation catalogue expansion (initial).
- KB-S23: Investigation quality hardening (panels harness + guards).
- KB-S24 (Tranche 1–3): Investigation coverage completion (tracker shows zero pending).
- KB-S25: Narrative payload standardisation for investigation signals.
- KB-S26: Preserve one-sided lab ranges end-to-end.
- KB-S27: Lab reference profiles (bands + effective-from + note) pass-through + lab_band_label classification.
- KB-S28: Signal interaction mapping v1 (deterministic map + builder + tests).
- KB-S29: Signal confidence model v1 (next).

> Note: Dates are intentionally omitted; the plan is milestone-driven under SOP.

---

### KB-S29 — Signal Confidence Model v1 (next sprint)
**Objective**
Populate `signal_results[].confidence` and chain confidence deterministically so interaction outputs and narrative prioritisation are trust-aware from day one.

**Deliverables**
- `confidence` float per signal (0–1).
- `confidence_reasons` as a closed token vocabulary (enum).
- Chain confidence for `interaction_chains[]` using `min(confidence)` across nodes.
- Tests: determinism, vocabulary enforcement, primary-metric-absent penalty, chain aggregation, non-regression of signal_state.

**Non-goals**
- No changes to signal activation logic.
- No biomarker-value-based heuristics.
- No ML/probabilistic scoring.

**Acceptance**
- Gate PASS; baseline failures unchanged.
- `confidence` no longer null for evaluated signals.
- `confidence_reasons` tokens strictly from the allowed enum.
- Interaction chains emit chain confidence deterministically.

---

### KB-S30 — Interaction Map Governance + Expansion v1.1
**Objective**
Make the interaction map a durable clinical knowledge asset with controlled change and improved coverage within the already-agreed macro pathways.

**Deliverables**
- Formalised interaction map governance:
  - required fields per edge (relationship_type, evidence_strength, rationale)
  - review checklist for new edges
  - versioning discipline (map_version bump rules)
- Expand map within the v1 pathways only (no new pathways yet):
  - tighten metabolic→hepatic→inflammatory→vascular chain edges
  - improve thyroid→lipid→metabolic connectivity
  - strengthen iron→hematologic chain
- Tests:
  - edge isolation test (new edge doesn’t affect unrelated panels)
  - deterministic chain output snapshots

**Non-goals**
- No runtime inference.
- No new signal logic.
- No “optimal node” linking (unless explicitly scheduled later).

**Acceptance**
- Map changes are reviewable and test-locked.
- Deterministic chain outputs remain stable across replays.

---

### KB-S31 — Intervention Evidence Layer v1 (conservative, audited)
**Objective**
Introduce **evidence-backed action options** without claiming quantified personalised risk. This is the first step toward defensible “what to do next” outputs.

**Deliverables**
- A versioned intervention library (knowledge asset) that:
  - links intervention options to *signal types* (not individual biomarkers)
  - includes evidence_strength and a conservative evidence summary
  - includes safety boundaries (“consult clinician if…”)
- A deterministic “intervention suggester” that:
  - selects interventions for fired signals based on explicit mapping rules
  - outputs structured intervention objects (no free text generation)
- Tests:
  - deterministic selection
  - evidence_strength present for every intervention mapping
  - non-regression to signal evaluation

**Non-goals**
- No quantified personalised risk (no hazard ratios, no time-to-event predictions).
- No clinical prescribing.

**Acceptance**
- Users can see “next steps” grounded in explicit evidence assets, auditably.

---

### KB-S32 — Report Compiler Contract (UI-ready structured output)
**Objective**
Convert raw InsightGraph into a stable **Report Object** suitable for any frontend (web/mobile/clinical export) without requiring narrative hacks.

**Deliverables**
- A versioned `report_v1` object generated deterministically from:
  - signal_results (with confidence)
  - interaction_chains (with chain confidence)
  - interventions (v1)
  - lab reference profile notes (effective_from)
- Report object includes:
  - “Top findings” list (ranked by state + confidence)
  - “Top chains” list (ranked by chain confidence)
  - “What to do next” structured actions
- Tests:
  - contract validation
  - deterministic ordering
  - non-regression to signal evaluation

**Non-goals**
- No LLM narrative generation in the analytic path.

**Acceptance**
- A stable “handoff object” exists for the UX team and for clinical export experiments.

---

### KB-S33 — Longitudinal Foundations (data model + replay continuity)
**Objective**
Prepare the platform for repeat panels and trend interpretation, especially considering lab range changes (effective-from notes).

**Deliverables**
- A versioned longitudinal record model:
  - panel_date at panel-level
  - reference profile effective-from retained per biomarker
  - stable biomarker identity mapping across time
- Deterministic “trend summary” scaffolding:
  - no medical prediction, only change detection and comparability flags
- Tests:
  - two panels same user → stable identity; deterministic summaries
  - detects “range regime changed” and flags for caution

**Non-goals**
- No outcomes claims.
- No predictive risk.

**Acceptance**
- Data structures and replay are ready for Phase 2 dataset moat work.

---

## Phase 2 (18–36 months): Dataset moat (longitudinal + outcomes-adjacent) + validation
**Goal:** build the asset strategic buyers pay for: a proprietary dataset linking biomarkers → signals → interventions → trajectories over time.

### What Phase 2 is
Phase 2 is **repeatability and learning loops**:
- repeated panels per user
- structured intervention tracking
- trajectory outcomes (biomarker improvements, proxy endpoints)
- validation that reasoning maps to real-world patterns

### Phase 2 deliverables (vision)
1) **Longitudinal user journeys**
- retest programs and 90-day cycles (or similar)
- deterministic response-to-intervention tracking

2) **Outcomes-adjacent endpoints**
- biomarker trajectory endpoints (HbA1c, ApoB, TG/HDL, hsCRP, ALT, etc.)
- adherence proxies (structured)
- optional symptoms/self-report (bounded, structured)

3) **Clinical validation program**
- observational cohorts using engine outputs
- demonstrate signals/chains/confidence align with meaningful improvements over time (without overclaiming)

4) **Distribution wedge**
Pick a channel designed to create repeat panels:
- private clinics / retest programs
- employer prevention programs
- insurer prevention pathways

### Phase 2 success criteria
- Proprietary longitudinal dataset with consistent schema and versioned engine outputs.
- Retention loop: users return because the platform tracks change and prioritises next actions.
- Evidence that outputs correlate with meaningful changes over time.

---

## Phase 3 (36–60 months): Outcomes + regulated workflows + strategic buyer fit
**Goal:** become acquisition-ready by combining a governed reasoning engine with outcomes-linked datasets and workflow distribution.

### Phase 3 deliverables (vision)
1) **True outcomes linkage**
- partnerships for outcomes data (clinical, claims, or structured clinician-confirmed endpoints)

2) **Regulated trajectory**
- documented risk controls, traceability, and clinical evaluation plan

3) **Pharma/R&D licensing product line**
- cohort discovery and stratification from signals/chains
- response signatures over time (non-interventional at first)

4) **Distribution lock-in**
At least one high-switching-cost channel:
- embedded clinical workflow
- enterprise contracts
- exclusive data partnerships

### Phase 3 success criteria
- Dataset + engine is hard to replicate and compounding in value.
- Credible clinical utility evidence.
- Revenue/partnerships reflect durable demand.

---

## Summary: not a pivot
This roadmap clarifies why the KB-Sxx plan is the correct Phase 1 moat build, and what must come next to reach Tempus/Flatiron-style defensibility:
- Engine moat → Dataset moat → Outcomes + Workflow moat.

---

## Immediate next action
Proceed with **KB-S29** (confidence), then KB-S30 (interaction map governance + expansion), then KB-S31–KB-S33 to complete Phase 1 readiness for longitudinal and distribution work.
