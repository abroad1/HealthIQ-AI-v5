# HealthIQ AI — Strategic Vision and 12-Month Sprint Plan
*Version 1.3 — Reviewed and amended against live codebase audit 2026-03-21, with lifestyle/context-input roadmap clarification and final BE-S0 split/governance refinement*

> **Review note (Claude Code, 2026-03-21):** Plan reviewed against live codebase audit (`docs/AUDIT_SPRINT_PLAN_2026-03-20.md`) and metabolic pathway coverage audit (`docs/METABOLIC_PATHWAY_COVERAGE_AUDIT_2026-03-20.md`). Four amendments applied: KB-S39 baseline status clarified in §0; KB-S54 risk classification confirmed HIGH; BE-S1 risk classification corrected to STANDARD; KB-S58 scope-splitting note added. This version also adds an explicit governed lifestyle/questionnaire context workstream so high-impact non-biomarker inputs are treated as part of the platform architecture rather than background detail, and finalises the context-hardening sequence by splitting BE-S0 into objective and subjective/context-caveat sub-sprints with explicit escalation rules. No architectural conflicts with existing intelligence found. All sprints in this plan are additive. See individual amendment notes inline.

## Version Notes

- **v1.3:** adds the governed lifestyle / questionnaire / medication context workstream; inserts context hardening before narrative enablement; clarifies context-governance rules; records KB-S39 as completed baseline work on `main`; confirms KB-S54 HIGH classification, BE-S1 classification correction, and KB-S58 scope-boundary rule; and splits BE-S0 into BE-S0a / BE-S0b with explicit escalation guidance and baseline SSOT acknowledgement.
- **v1.2:** established the braided 12-month breadth/depth roadmap and formalised the revised sprint numbering as the governing sequence.
- **v1.1 and earlier:** interim strategy drafts used during audit/review; superseded by this controlled roadmap.

---

## 0. Baseline Confirmation Before This Roadmap Begins

**KB-S39 is already completed and merged to `main` at commit `c803994`.**

That means the earlier temporary prerequisite state has been resolved. This roadmap now assumes a clean post-KB-S39 baseline on updated `main` before any new sprint is authored.

Operational rule going forward:
1. start each roadmap sprint from clean updated `main`
2. do not begin new work with unresolved control-plane or HIGH-risk in-flight modifications
3. create a fresh sprint branch only after baseline cleanliness is confirmed

This remains non-negotiable per the standing rule against concurrent in-flight modifications to control-plane scripts and other HIGH-risk infrastructure surfaces.

In parallel with roadmap execution: **begin the renal interaction map research promotion process early.** Do not wait until KB-S56 is reached — by then it will be too late to avoid a blocked sprint.

---

## 1. Executive Intent

HealthIQ AI is not being built as a better blood report.

It is being built as:

1. the reference platform for deterministic metabolic intelligence
2. a platform that can evolve into a Class II medical product
3. a company with the potential to become strategic acquisition infrastructure at very high enterprise value

The build strategy is therefore not "ship the fastest panel demo."

The strategy is:

- build breadth and depth together
- protect the deterministic engine at all costs
- avoid micro-sprints where they do not improve safety
- keep work packages large enough to matter, but bounded enough to audit, test, and reverse safely
- treat AB and VR as realistic minimum commercial test harnesses, not the final product boundary

---

## 2. Product Vision

### 2.1 What HealthIQ AI is becoming

HealthIQ AI is intended to become the deterministic operating system for metabolic interpretation.

That means:

- broad biomarker coverage across real-world commercial blood panels
- explicit, versioned, auditable biological reasoning
- root-cause and WHY explanation, not just abnormality surfacing
- connected cross-system interpretation
- safe structured next-step outputs
- narrative translation layered on top of governed structured intelligence
- explicit incorporation of high-impact structured context inputs such as anthropometrics, blood pressure, smoking, alcohol, medications, sleep, exercise, and stress
- eventual longitudinal and outcomes-linked intelligence

### 2.2 What it is not

HealthIQ AI is not:

- a generic LLM wrapper around blood tests
- a traffic-light UI with prettier wording
- a narrow AB/VR-only interpreter
- a frontend-heavy application with hidden logic in the UI
- a probabilistic black box

---

## 3. Long-Term Company Vision

The platform vision has three strategic layers.

### Phase 1 — Engine moat
Build the best deterministic metabolic reasoning engine in the market.

### Phase 2 — Dataset moat
Turn repeated panels, intervention tracking, and trajectories into a proprietary longitudinal metabolic dataset.

### Phase 3 — Outcomes + regulated workflow moat
Translate the engine and dataset into:
- clinical validation
- regulated-product readiness
- workflow insertion
- strategic buyer fit

The roadmap is therefore not just a sprint sequence.
It is the first 12 months of building "The Metabolic Platform."

---

## 4. Current Baseline

### 4.1 What is already complete

Recent completed work includes:

- KB-S44 — Knowledge Bus operational alignment
- KB-S44a — Clinician report runtime contract alignment
- FE-S1 — Clinician summary report renderer

This means the delivery pipe and clinician-report shell are already built:
- backend assembles `ClinicianReportV1`
- API exposes it
- frontend renders it
- frontend remains renderer-only

### 4.2 What is materially incomplete

The platform is still structurally incomplete in five critical ways:

1. root-cause / WHY coverage is still too shallow across the live signal estate
2. cluster runtime wiring and system-level scoring are not fully complete in runtime
3. AB and VR are not yet formalised as explicit panel profiles and acceptance targets
4. structured lifestyle, anthropometric, blood-pressure, smoking, alcohol, medication, and related context inputs are not yet elevated into the roadmap as an explicit governed platform workstream
5. the narrative layer exists architecturally but is not yet production-enabled as the final user-facing translation layer

### 4.3 Additional coverage reality

A separate ingestion programme already exists:
- 56 additional biomarkers have been researched
- they are already structured in ingestion-friendly batch folders
- they must be ingested in those existing batches, not re-sorted one by one
- these biomarkers extend the platform toward realistic commercial-panel breadth beyond the current minimum test harness

Important clarification:
- these investigation-spec assets are currently in JSON source format
- they are not themselves deployable Knowledge Bus signal-library packages
- they must be translated into canonical KB package/YAML artifacts before validation and promotion

### 4.4 Lifestyle / Questionnaire Context Reality

The platform must not treat biomarker values as the only meaningful inputs.

For metabolic interpretation, several non-biomarker inputs are strategically important enough to be treated as governed platform inputs, not incidental questionnaire detail.

The minimum high-impact context set for Phase 1 should include:
- waist circumference / waist-to-height relationship
- blood pressure
- height / weight / BMI-related inputs
- current medications
- smoking / tobacco exposure
- alcohol consumption
- exercise
- sleep
- stress

These inputs matter for three reasons:
1. they materially change interpretation of biomarker patterns
2. they strengthen root-cause / WHY reasoning beyond blood chemistry alone
3. they are part of the long-term transition from blood-report application to metabolic platform

Existing foundation note:
- the codebase already contains substantial questionnaire and lifestyle SSOT assets, including `backend/ssot/questionnaire.json` and `backend/ssot/lifestyle_registry.yaml`
- the strategic need is therefore not to invent lifestyle context from scratch
- it is to harden, formalise, and govern how those existing inputs are consumed by the engine and downstream narrative layers

Important interpretation boundary for Phase 1:
- numeric and objectively measured inputs (for example waist circumference, blood pressure, height, weight, BMI-linked measures) can be governed through typed schema, validation rules, and deterministic overlay logic
- subjective or self-reported categorical inputs (for example stress, sleep quality, alcohol pattern, exercise pattern) must only be consumed through explicitly governed mapping from response state to defined interpretation category
- medication context is not equivalent to other context inputs; in Phase 1 it should be used to flag interpretation caveats and context warnings only, not to alter analytical thresholds or generate medication-specific causal reasoning unless a later governed workstream explicitly authorises that behaviour

The roadmap below now treats this as an explicit workstream, not an implicit assumption.

---

## 5. Core Planning Principles

These are non-negotiable.

### 5.1 Deterministic analytics only
No LLM reasoning in the analytical core.

### 5.2 LLM as translation layer only
Narrative translation can sit on top of the governed structured engine.
It must never become the source of metabolic reasoning.

### 5.3 Breadth-depth braid
We will not front-load all ingestion before all WHY work.
We will not front-load all WHY work while breadth remains too narrow.
We will alternate breadth and explanatory depth in strategically meaningful waves.

### 5.4 No micro-sprints for their own sake
Work packages should be large enough to matter.
They should only be split when:
- governance risk requires it
- rollback risk becomes unacceptable
- testability degrades
- audit scope becomes too broad

### 5.5 Safety with pace
We build quickly, but we do not gamble with the engine.
Every sprint must remain:
- bounded
- testable
- auditable
- reversible where feasible

### 5.6 AB/VR are a floor, not the destination
AB and VR are the current test harness for minimum real-world panel coverage.
They are not the full future product ontology.
Coverage must grow beyond them.

### 5.7 Governed context inputs are part of the platform
The platform must treat high-impact lifestyle, anthropometric, blood-pressure, smoking, alcohol, and medication inputs as governed context, not loose questionnaire decoration.

That does not mean lifestyle work comes before core engine work.
It means the roadmap must explicitly harden, formalise, and intentionally consume the context inputs that materially affect deterministic metabolic interpretation.

---

## 6. Sprint Classification Rules Going Forward

### 6.1 Ingestion sprints
Default classification:
- change_type: CONTENT
- risk_level: STANDARD

These are suitable for faster sequential execution.

Exception:
If a batch requires new derived metrics, ratio-registry additions, or runtime logic changes, do not silently widen the ingestion sprint.
Instead:
- create a separate prerequisite sprint for the derived-metric/runtime addition
- classify that prerequisite sprint appropriately (typically MIXED / HIGH)
- then proceed with the ingestion sprint afterward

### 6.2 WHY expansion sprints
Default classification:
- change_type: MIXED
- risk_level: HIGH

These sprints touch hypothesis assets, compiler-linked behavioural logic, confirmatory logic, and regression surfaces.

Each WHY sprint must have a mechanical prerequisite:
- clinical content must be authored first
- the prompt must include a STOP condition if the required hypothesis assets do not already exist

This rule is mandatory.

### 6.3 Structural completion sprints
Panel formalisation, cluster runtime wiring, renal completion, and major fixture expansion are governed as backend / mixed architectural work, with risk level determined by the exact touched files.

### 6.4 Context-hardening sprints
Questionnaire / lifestyle / medication-context hardening work is governed as backend or mixed product-integration work.

Default intent:
- formalise which context fields are first-class inputs
- distinguish numeric/objective inputs from subjective/categorical inputs and govern consumption appropriately
- verify mapping from collected input to governed runtime consumption
- prevent silent drift between questionnaire capture, mapper logic, overlays, and user-facing narrative
- keep medication handling inside an explicitly bounded interpretation-caveat model unless a later sprint authorises deeper medication-aware reasoning

Baseline expectation:
- these sprints build on an existing SSOT foundation already present in `backend/ssot/questionnaire.json` and `backend/ssot/lifestyle_registry.yaml`
- they are hardening and governing consumption of an existing input layer, not inventing lifestyle infrastructure from scratch

Risk rule:
- if touched-file scope stays inside mapper, questionnaire, registry, contract, or renderer-adjacent integration code, classification may remain below HIGH subject to hardening review
- if touched-file scope crosses into `backend/core/analytics/`, `backend/core/pipeline/`, overlay logic that changes signal/runtime behaviour, or any control-plane authority, classification escalates to HIGH automatically
- prompt authors must state this explicitly when BE-S0a / BE-S0b are authored

### 6.5 Narrative sprints
Narrative enablement must remain downstream of structured engine completeness.
No narrative sprint may introduce LLM reasoning into the analytical path.

---

## 7. One-Off Immediate Pre-Sprint Task

Before KB-S45 is authored, perform a one-off compatibility check across all six ingestion batches.

### Required outputs of the compatibility check
For each batch:
- confirm which biomarker IDs are already in SSOT
- confirm which derived metrics already exist in the ratio registry
- identify any missing derived metric prerequisites
- identify any schema or naming mismatches that would block clean ingestion
- confirm the translation path from JSON source material into canonical KB YAML/package artifacts is clear

### Important rule
This compatibility check is a task, not a sprint.

Its purpose is to prevent:
- SSOT gaps
- ratio-registry surprises
- blocked ingestion prompts
- avoidable sprint churn

---

## 8. Ingestion Translation Rule

Each ingestion batch consists of investigation-spec JSON source files.

Those JSON files are:
- structured research assets
- ingestion-friendly source material
- not yet canonical Knowledge Bus package artifacts

Therefore, every ingestion sprint must explicitly include:

1. translation of the batch JSON source material into canonical Knowledge Bus YAML/package assets
2. SSOT and registry compatibility confirmation
3. validator-passing package creation
4. fixture or synthetic-panel confirmation that the new signals fire as expected
5. promotion readiness evidence consistent with current KB governance

No sprint may assume that JSON assets are directly promotable by the Knowledge Bus lifecycle without this translation step.

---

## 9. The 12-Month Strategic Build Plan

This roadmap is the agreed strategic direction for the next 12 months.

It is intentionally structured as larger, meaningful capability waves.

---

# Wave 1 — Breadth and Depth, Pass 1

## KB-S45 — Biomarker Ingestion Batch 1
**Type:** KB / CONTENT / STANDARD
**Purpose:** ingest the first pre-existing batch of ten researched biomarkers into governed Knowledge Bus signal packages.
**Why now:** broadens analytical surface immediately using work that is already prepared.
**Unlocks:** wider real-world panel coverage without speculative research delay.
**Includes explicitly:** JSON-to-KB-YAML/package translation.

## KB-S46 — WHY Expansion 1: Insulin Resistance + Systemic Inflammation
**Type:** KB + backend / MIXED / HIGH
**Purpose:** add root-cause / WHY coverage for:
- insulin resistance
- systemic inflammation

**Why now:** these are among the most clinically important and structurally connected early explanatory gaps.
**Important governance rule:** both hypothesis sets must be authored before sprint execution begins.

## KB-S47 — Biomarker Ingestion Batch 2
**Type:** KB / CONTENT / STANDARD
**Purpose:** ingest the second pre-existing batch of ten researched biomarkers.
**Why here:** maintains breadth growth while not allowing WHY work to become detached from signal surface expansion.
**Includes explicitly:** JSON-to-KB-YAML/package translation.

## KB-S48 — WHY Expansion 2: Lipid / Vascular
**Type:** KB + backend / MIXED / HIGH
**Purpose:** add WHY coverage across lipid and vascular metabolic interpretation.
**Why now:** lipid findings are frequent, commercially important, and central to meaningful metabolic explanation.

---

# Wave 2 — Breadth and Depth, Pass 2

## KB-S49 — Biomarker Ingestion Batch 3
**Type:** KB / CONTENT / STANDARD
**Purpose:** ingest the third prepared biomarker batch.
**Includes explicitly:** JSON-to-KB-YAML/package translation.

## KB-S50 — WHY Expansion 3: Iron / Oxygen + Iron Overload Phenotype
**Type:** KB + backend / MIXED / HIGH
**Purpose:** add WHY coverage for:
- iron deficiency context
- iron overload context
- oxygen transport / hematologic interpretation

**Why now:** iron and hematologic reasoning are common, clinically meaningful, and still under-explained.
**Includes:** missing iron overload phenotype fixture.

## KB-S51 — Biomarker Ingestion Batch 4
**Type:** KB / CONTENT / STANDARD
**Purpose:** ingest the fourth prepared biomarker batch.
**Includes explicitly:** JSON-to-KB-YAML/package translation.

## KB-S52 — WHY Expansion 4: Hepatic Extension + Thyroid Completion
**Type:** KB + backend / MIXED / HIGH
**Purpose:** complete broader WHY coverage for:
- hepatic interpretation beyond ALT-only depth
- thyroid signal completion where current pathway coverage is partial

**Why here:** this closes secondary but still commercially important explanatory domains.

---

# Wave 3 — Structural Truth and Platform Hardening

## KB-S53 — AB/VR Panel Formalisation + Acceptance Harness
**Type:** backend / MIXED / risk to be confirmed at prompt stage
**Purpose:** formalise AB and VR as explicit panel test profiles and acceptance objects.
**Why now:** AB/VR are not the final product boundary, but they must become real codebase validation targets.
**Unlocks:** honest coverage accounting and panel-specific regression truth.

## KB-S54 — Cluster Runtime Wiring + System-Level Scoring Completion
**Type:** backend / BEHAVIOUR / HIGH
**Purpose:** wire cluster/runtime/system-level scoring fully into live structured output.
**Why now:** the engine should be structurally complete before narrative enablement.
**Unlocks:** richer cross-domain structured substrate for future narrative and clinical interpretation.
**Amendment (2026-03-21):** Classification confirmed HIGH — not "to be confirmed." Wiring `ClusterEngineV2` requires modifying `AnalysisOrchestrator`, which drives signal evaluation, clustering, arbitration, and burden engine execution. This is a change to pipeline behaviour and output generation — a mandatory SOP §10 HIGH trigger. Requires Claude audit + GPT architectural review + dual approval before merge. Regression surface is the three-layer pipeline verification script.

---

# Wave 4 — Final Phase-1 Breadth Completion

## KB-S55 — Biomarker Ingestion Batch 5
**Type:** KB / CONTENT / STANDARD
**Purpose:** ingest the fifth prepared biomarker batch.
**Includes explicitly:** JSON-to-KB-YAML/package translation.

## KB-S56 — Renal Research Promotion + Renal WHY Completion
**Type:** KB + backend / MIXED / HIGH
**Purpose:** complete the renal pathway after its required research-promotion prerequisite.
**Why here:** renal remains a gated special case and should not distort earlier sequencing.
**Important note:** the research-promotion work should begin early in parallel so this sprint is not blocked when reached.

## KB-S57 — Biomarker Ingestion Batch 6 + SSOT Coverage Check
**Type:** KB / CONTENT / STANDARD
**Purpose:** ingest the final prepared biomarker batch and complete canonical/SSOT coverage verification.
**Why now:** closes the current known ingestion programme cleanly.
**Includes explicitly:** JSON-to-KB-YAML/package translation.

## KB-S58 — Phenotype / Fixture / Regression Expansion
**Type:** KB + backend / MIXED / risk to be confirmed at prompt stage
**Purpose:** expand phenotype fixtures, regression assets, and acceptance coverage across all newly ingested biomarkers and newly covered WHY domains.
**Why here:** locks the enlarged engine into deterministic regression discipline.
**Amendment (2026-03-21):** Scope must be bounded at prompt time. By the time this sprint runs, the system will have ingested ~60 new biomarkers across 6 batches and added WHY coverage across 4+ major domains. A single sprint covering all of this is likely too wide. Rule: if fixture and regression expansion spans more than three WHY domains or more than two ingestion batches, split into KB-S58a / KB-S58b before the prompt is authored. Do not attempt to cover the full scope in one HIGH-risk sprint.

---

# Wave 5 — Context Hardening Before Narrative

**Sequencing note:**
Context hardening is intentionally placed after the core breadth/WHY expansion waves and structural platform-completion work.
This is deliberate, not accidental.

Reason:
- the current priority remains safe completion of breadth, WHY depth, panel truth, and system-level runtime completeness
- the platform already has an existing questionnaire/lifestyle SSOT foundation
- but narrative must not be enabled until high-impact context inputs are explicitly governed, typed, and consumed in a controlled way

Therefore context hardening sits **before narrative enablement**, but **after core engine completion waves**.

## BE-S0a — Objective Context Hardening
**Type:** backend / MIXED or BEHAVIOUR depending on touched files / confirmed at hardening
**Purpose:** harden governed consumption of high-impact numeric/objective non-biomarker inputs before narrative enablement.
**Scope:**
- waist circumference / waist-to-height context
- blood pressure
- height / weight / BMI-related inputs
- typed schema confirmation
- validation rules
- deterministic overlay or governed runtime consumption logic
- alignment between questionnaire capture, mapper logic, overlay logic, and downstream analytical/narrative use for objective fields

**Governed consumption model required in this sprint:**
- numeric/objective inputs must have typed schema, validation rules, and deterministic overlay/consumption logic
- the sprint must state clearly which objective fields are merely captured, which are mapped into overlays, and which materially influence structured interpretation

**Why this is split out:**
- objective inputs are the cleanest and most deterministic context class
- they are architecturally different from subjective/categorical self-report inputs
- splitting them prevents the sprint from becoming too wide and reinforces the boundary described in §4.4

## BE-S0b — Subjective / Behavioural Context Hardening
**Type:** backend / MIXED or BEHAVIOUR depending on touched files / confirmed at hardening
**Purpose:** harden governed consumption of high-impact subjective/categorical context inputs and medication caveat handling before narrative enablement.
**Scope:**
- smoking / tobacco exposure
- alcohol consumption
- exercise
- sleep
- stress
- current medications
- governed mapping from response state to defined interpretation category
- caveat-layer handling for medication context
- alignment between questionnaire capture, mapper logic, overlay logic, and downstream analytical/narrative use for subjective/categorical fields

**Governed consumption model required in this sprint:**
- subjective/categorical inputs must map from user response states to explicitly governed interpretation categories; they must not be consumed as vague free-text sentiment
- the sprint must state clearly which fields are only collected, which are mapped to overlays, and which are surfaced as interpretation caveats

**Medication boundary for Phase 1:**
- medication context must be treated as a governed interpretation-caveat layer only
- medication inputs may flag that a biomarker or pattern could be confounded or requires cautious interpretation
- medication inputs must not change analytical thresholds, alter core signal firing rules, or generate medication-specific reasoning unless a later explicitly approved workstream authorises that behaviour

**Risk escalation note for BE-S0a / BE-S0b:**
- if touched-file scope includes `backend/core/analytics/`, `backend/core/pipeline/`, overlay logic that changes signal/runtime behaviour, or any control-plane authority, classification escalates to HIGH automatically
- this expectation must be restated explicitly when each sprint prompt is authored

---

# Wave 6 — Narrative Translation Layer

## BE-S1 — LLM Narrative Production Enablement
**Type:** backend / MIXED / STANDARD — confirmed at hardening; escalate to HIGH if touched-file scope crosses into analytical/runtime behavioural generation or control-plane authority
**Purpose:** enable the narrative layer in the verified path using governed structured input only.
**Rules:**
- LLM translates
- LLM does not reason
- no raw biomarker-value reasoning in the LLM layer
- narrative must reflect governed biomarker, WHY, and context inputs rather than bypassing them
- prompt contract, safety boundaries, and acceptance testing must be explicit
**Amendment (2026-03-21):** Classification corrected from "likely HIGH" to STANDARD — confirmed at hardening; escalate to HIGH if touched-file scope crosses into analytical/runtime behavioural generation or control-plane authority. `InsightSynthesizer` sits in Layer C, downstream of the `InsightGraphV1` contract boundary. It does not touch `backend/core/analytics/`, `backend/ssot/`, `backend/core/pipeline/`, or any control-plane script — none of the SOP §10 HIGH triggers apply. Final classification must be confirmed by the hardening agent at prompt time based on actual files touched.

## FE-S2 — Narrative Presentation Layer
**Type:** frontend / CONTENT or MIXED depending on scope
**Purpose:** present the user-facing plain-English narrative cleanly in the application.
**Rules:**
- frontend remains renderer-only
- no clinician or biological logic may move into the UI
- the rendered narrative must remain downstream of governed biomarker and context inputs

---

## 10. Why This Sequence Is Strategically Correct

This sequence is designed to satisfy seven goals simultaneously:

1. widen coverage without waiting for all breadth to be complete
2. deepen WHY without over-investing in a too-narrow signal surface
3. avoid six straight ingestion sprints that create breadth without depth
4. avoid four straight WHY sprints that deepen only a narrow engine surface
5. formalise structural truth before enabling narrative
6. explicitly harden high-impact lifestyle, anthropometric, blood-pressure, medication, smoking, alcohol, and related context inputs before narrative enablement
7. preserve governance, auditability, and rollback discipline

This is the right compromise between:
- pace
- safety
- strategic compounding
- platform ambition

---

## 11. What This Plan Is Building

By the end of this 12-month roadmap, the product should be much closer to:

- a broad deterministic metabolic reasoning engine
- a platform that can interpret realistic commercial blood panels, not just a narrow subset
- a governed WHY and root-cause system with much stronger explanatory depth
- an explicitly governed context-input layer that combines biomarkers with key lifestyle, anthropometric, hemodynamic, and medication context
- a structurally complete platform ready for narrative translation
- a credible launch point for Phase 2 longitudinal / dataset moat work

This is not yet the full company vision.
It is the first serious platform-construction year.

---

## 12. What Comes After This 12-Month Plan

### Phase 2 — Dataset moat
After the engine is stronger and structurally complete:
- repeat-panel journeys
- intervention tracking
- trajectory summaries
- longitudinal identity continuity
- observational validation

### Phase 3 — Regulated workflow and strategic buyer readiness
After the dataset loop is live:
- documented risk controls
- clinical evaluation plan
- workflow insertion
- outcomes linkage
- high-switching-cost channel strategy
- acquisition-grade strategic defensibility

---

## 13. Final Strategic Statement

This roadmap is not optimised for the fastest demo.

It is optimised for building the first full version of the deterministic metabolic platform safely, at pace, and without architectural dishonesty.

The guiding principle is:

**Build breadth and depth together.
Formalise truth before narrative.
Move fast, but never in a way that puts the engine at risk.**

---
