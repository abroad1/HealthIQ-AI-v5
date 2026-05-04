# HealthIQ AI — Strategic Vision and 12-Month Sprint Plan
*Version 1.5 draft — revised to make the system intent, wave purpose, phenotype role, and strategic sequencing legible to a cold reader*

> Draft note: This version preserves the strategic direction of v1.4 while making the document easier to understand for new readers. It adds a clearer explanation of what HealthIQ is building, how the engine works, how phenotypes fit into the architecture, and what each wave is trying to achieve in application terms. It also reflects the reality that breadth coverage has advanced materially and that runtime truth, WHY depth, phenotype coherence, and governed context consumption remain central to Phase 1 completion.

---

## 0. Why this document exists

This is not just a sprint list.

It is the strategic build map for the first serious version of HealthIQ AI.

HealthIQ is not being built as a prettier blood report. It is being built as a deterministic metabolic reasoning engine that can:

- interpret realistic commercial blood panels
- convert biomarker data into governed metabolic signals
- connect those signals into pathway-level and system-level reasoning
- map users to one or more phenotype-level metabolic states
- explain why those states are active
- incorporate governed non-biomarker context inputs
- produce clinician-grade structured outputs
- later support safe narrative translation, longitudinal tracking, and cohort intelligence

This document exists so that every team member can answer three questions at any point in the roadmap:

1. What are we building?
2. Why are we building it in this sequence?
3. What capability does each wave add to the final platform?

---

## 1. Executive intent

HealthIQ AI is being built as:

1. the reference platform for deterministic metabolic intelligence
2. a platform that can evolve toward clinician-grade and regulated workflow use
3. a data-and-reasoning infrastructure asset with long-term strategic buyer value

The strategy is therefore not “ship the fastest blood-test demo.”

The strategy is:

- build breadth and depth together
- protect the deterministic engine at all costs
- avoid micro-sprints where they do not improve safety
- keep work packages large enough to matter, but bounded enough to audit, test, and reverse safely
- treat AB and VR as realistic minimum commercial harnesses, not the final product boundary
- build toward phenotype-level metabolic interpretation, not a collection of disconnected marker alerts

This remains the governing intent from v1.4. The wording here is expanded so the purpose is obvious to a new reader as well as to the original team. Source intent remains aligned with v1.4’s Executive Intent, Product Vision, and Company Vision sections. fileciteturn25file0

---

## 2. What HealthIQ is actually building

### 2.1 The layered engine model

HealthIQ should be understood as a layered deterministic system.

### Layer 1 — Inputs
HealthIQ begins with structured inputs:
- biomarker values and lab ranges
- later, governed context inputs such as anthropometrics, blood pressure, smoking, alcohol, medications, exercise, sleep, and stress

### Layer 2 — Signal layer
Each biomarker or biomarker pattern activates one or more governed signals.
A signal is not just “marker high” or “marker low.”
A signal is a deterministic claim about a meaningful biological state.

Examples:
- iron deficiency context
- lipid transport dysfunction
- systemic inflammation
- thyroid-axis disturbance
- hepatic metabolic stress

### Layer 3 — Interaction and system layer
Signals do not live in isolation.
They connect through interaction logic, pathway relationships, and system-level reasoning.
This is where the engine begins moving beyond individual biomarkers into metabolic structure.

### Layer 4 — Phenotype layer
Signals and signal chains resolve into phenotype-level metabolic states.
A user may express one or more overlapping phenotypes.
These phenotypes are not decorative labels. They are a key part of:
- interpretation
- cohorting
- future dataset structure
- product strategy
- eventual buyer value

### Layer 5 — WHY / root-cause layer
The system explains why a signal or phenotype may be active.
This includes:
- supporting markers
- contradiction markers
- confidence limits
- confirmatory tests
- plausible upstream biological drivers

### Layer 6 — Structured report layer
The engine produces governed structured outputs such as:
- top findings
- root-cause hypotheses
- signal and phenotype relevance
- safe next-step outputs
- clinician-facing structured reports

### Layer 7 — Narrative layer
Only after the structured layers are coherent should an LLM-based translation layer turn structured truth into human-readable narrative.
The LLM must never become the analytical engine.

This layered view is consistent with the v1.4 roadmap direction and is now made explicit because the previous document assumed too much prior context. fileciteturn25file0

### 2.2 Why phenotypes matter

HealthIQ is not intended to stop at “user has abnormal ALT” or “user has high triglycerides.”

The real product goal is to identify meaningful metabolic states.
The 12-core-phenotype framing helps explain why breadth, interaction mapping, WHY depth, and phenotype fixtures all matter together.

The metabolic phenotype direction can be summarised as:
- signals = intelligence atoms
- interactions = biological structure
- phenotypes = interpretable metabolic states
- trajectories = future dataset value

This framing is now important enough to be explicit in the roadmap because phenotype work is already represented in real schema and audit artefacts, not just strategic prose. The phenotype schema and coverage audit show that phenotypes, required signals, required edges, fixtures, and chain expectations already exist as governed concepts in the repo. fileciteturn26file0turn26file1

---

## 3. Phase 1 success definition

By the end of this Phase 1 roadmap, HealthIQ should be materially closer to a platform that can:

- interpret a realistic commercial blood panel deterministically
- emit non-contradictory biomarker and system-level outputs
- map users to one or more overlapping metabolic phenotypes
- explain key states with structured WHY reasoning
- use governed context inputs in a controlled and auditable way
- produce a coherent clinician-grade structured report
- support safe downstream narrative translation

This is the bridge between:
- a blood interpretation tool
- a metabolic intelligence platform
- a future longitudinal dataset engine

---

## 4. Long-term company vision

The long-term company vision still has three strategic layers:

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

This remains directly aligned with v1.4. What has changed in v1.5 is not the strategy, but the clarity with which the roadmap ties each wave back to this destination. fileciteturn25file0

---

## 5. Current baseline and reality check

### 5.1 What is already complete

The v1.4 document remains correct that several foundations are already complete, including:
- clinician report shell and renderer path
- intelligence-model schema hardening and lock
- upstream investigation-spec v3 alignment
- Knowledge Bus SOP alignment
- intervention-effects registry foundation

These foundations matter because they mean the platform already has:
- a governed structured engine core
- a real clinician-report contract path
- a more mature architectural base than earlier strategy drafts assumed fileciteturn25file0

### 5.2 What is still materially incomplete

The most important incomplete areas remain:
1. WHY / root-cause coverage is still too shallow across much of the live signal estate
2. structural runtime truth and system-level scoring are not yet complete enough
3. AB/VR are still more harness than fully formalised acceptance objects
4. governed lifestyle/questionnaire/context influence is not yet fully hard-wired into interpretation
5. narrative exists architecturally but should not be considered the current strategic priority until structural truth is stronger fileciteturn25file0

### 5.3 Phenotype maturity reality

The phenotype coverage audit makes the current maturity state much clearer:
- phenotype fixtures exist across several pathways
- phenotype schema exists and is governed
- many pathways have interaction edges and phenotype map coverage
- but WHY coverage is still thin for many live runtime signals
- renal remains notably incomplete in interaction-map maturity

That means phenotype work is already active, but unevenly mature. The roadmap therefore needs to make the difference between signal breadth, WHY depth, interaction maturity, and phenotype truth more explicit than v1.4 did. fileciteturn26file0turn26file1

---

## 6. Core planning principles

These remain non-negotiable.

### 6.1 Deterministic analytics only
No LLM reasoning in the analytical core.

### 6.2 LLM as translation layer only
Narrative translation may sit on top of governed structured output.
It must never become the source of metabolic reasoning.

### 6.3 Breadth-depth braid
The platform must not front-load all ingestion before all WHY work, nor all WHY work before breadth is adequate.
Breadth and depth must advance together in meaningful waves.

### 6.4 No micro-sprints for their own sake
Sprints should be large enough to matter.
They should only be split when governance risk, rollback risk, testability, or audit scope requires it.

### 6.5 Safety with pace
Every sprint must remain bounded, testable, auditable, and reversible where feasible.

### 6.6 AB/VR are a floor, not the destination
AB and VR are the current minimum commercial harness.
They are not the product’s final ontology or strategic ceiling.

### 6.7 Governed context inputs are part of the platform
Context inputs are not questionnaire decoration.
They are part of the deterministic platform architecture and must be governed accordingly.

All of these principles remain directly consistent with v1.4. fileciteturn25file0

---

## 7. How to read the roadmap

The roadmap should now be read as six connected build phases:

1. **Breadth waves** expand the signal surface so the engine can see more of real-world metabolism.
2. **WHY waves** deepen causal/explanatory reasoning in the most important metabolic domains.
3. **Structural-truth waves** make runtime outputs coherent, testable, and panel-truthful.
4. **Phenotype/fixture/regression waves** make multi-signal states and test harnesses stable enough to trust.
5. **Context-hardening waves** make non-biomarker inputs governable and meaningful.
6. **Narrative waves** translate governed truth into user-facing language safely.

This makes clear that the roadmap is not a list of technical chores.
It is the staged construction of a deterministic metabolic platform.

---

# 8. The 12-month strategic build plan

## Wave 1 — Breadth and Depth, Pass 1

### Purpose of this wave
Wave 1 gives HealthIQ enough initial breadth to matter and enough WHY depth to begin feeling intelligent rather than descriptive.
It starts the braid between more biomarker coverage and more explanatory value.

### Why this wave exists now
Without early breadth, the platform stays too narrow to be commercially relevant.
Without early WHY, it risks becoming a larger but still shallow engine.
Wave 1 is the first serious attempt to avoid both problems.

### What this wave improves in the application
After Wave 1, the application should be able to:
- interpret a broader early panel surface
- explain core metabolic domains more intelligently
- move beyond simple abnormality surfacing in the first high-value pathways

### How this wave advances the final platform
It lays the first braid between commercial usefulness and clinical reasoning quality.

#### KB-S45 — Biomarker Ingestion Batch 1
Purpose: broaden analytical surface with the first pre-researched batch.
Application impact: HealthIQ becomes able to see more of the panel meaningfully.
Strategic value: expands the signal base needed for both phenotype and WHY work.

#### KB-S46 — WHY Expansion 1: Insulin Resistance + Systemic Inflammation
Purpose: deepen interpretation in two of the most central metabolic pathways.
Application impact: the engine starts giving more meaningful metabolic explanations in high-prevalence states.
Strategic value: these pathways are core to user relevance, phenotype value, and future dataset compounding.

#### KB-S47 — Biomarker Ingestion Batch 2
Purpose: continue widening the real-world signal surface.
Application impact: the application sees more of the panel without waiting for all WHY work to finish.
Strategic value: prevents depth work from becoming detached from breadth.

#### KB-S48 — WHY Expansion 2: Lipid / Vascular
Purpose: add clinically important explanation in one of the most commercially relevant domains.
Application impact: lipid findings become more meaningful than isolated LDL/HDL flags.
Strategic value: strengthens cardiovascular interpretation and early phenotype scaffolding.

---

## Wave 2 — Breadth and Depth, Pass 2

### Purpose of this wave
Wave 2 repeats the braid at a more mature level, adding breadth while deepening additional biological systems that are common, clinically important, and commercially visible.

### Why this wave exists now
By this point the platform should not just know more markers. It should begin to reason across iron, oxygen transport, hepatic extension, and thyroid more credibly.

### What this wave improves in the application
After Wave 2, the application should:
- interpret more common real-world blood patterns
- start covering iron, oxygen, hepatic, and thyroid reasoning more convincingly
- be much closer to a true metabolic engine rather than a panel anomaly engine

### How this wave advances the final platform
It increases the density and connectedness of the reasoning graph in clinically common domains.

#### KB-S49 — Biomarker Ingestion Batch 3
Purpose: continue expanding the surface area of interpretation.
Application impact: more panel elements become governed signals rather than ignored inputs.
Strategic value: supports downstream phenotype and WHY completeness.

#### KB-S50 — WHY Expansion 3: Iron / Oxygen + Iron Overload Phenotype
Purpose: deepen iron and oxygen-transport reasoning, including overload and deficiency frames.
Application impact: the engine becomes more useful in a common domain frequently misunderstood in simple lab-review tools.
Strategic value: helps build phenotype-level metabolic structure around hematology and iron regulation.

#### KB-S51 — Biomarker Ingestion Batch 4
Purpose: continue breadth expansion in a governed way.
Application impact: more real-world panels become meaningfully interpretable.
Strategic value: keeps the braid alive rather than over-concentrating on one domain.

#### KB-S52 — WHY Expansion 4: Hepatic Extension + Thyroid Completion
Purpose: deepen hepatic and thyroid explanation beyond partial current coverage.
Application impact: the application becomes more coherent in two important metabolic-control systems.
Strategic value: strengthens system-level reasoning in areas that affect many downstream phenotypes.

---

## Wave 3 — Structural Truth and Platform Hardening

### Purpose of this wave
Wave 3 turns HealthIQ from a broadening engine into a trustworthy one.
This wave is about runtime truth, panel truth, and structural coherence.

### Why this wave exists now
A platform that knows more biology but produces contradictory or weak panel-level outputs is not commercially or clinically credible.
This wave exists to ensure breadth and WHY are grounded in trustworthy runtime behaviour.

### What this wave improves in the application
After Wave 3, the application should:
- treat AB/VR as real acceptance harnesses
- produce more coherent structured outputs
- be closer to phenotype-truth rather than disconnected signal alerts
- be safer to build context and narrative on top of

### How this wave advances the final platform
It protects trust, which is a prerequisite for clinician adoption, dataset quality, and long-term strategic value.

#### KB-S53 — AB/VR Panel Formalisation + Acceptance Harness
Purpose: turn AB and VR into explicit panel truth objects rather than informal fixtures.
Application impact: the team can measure whether the engine is actually believable on realistic panels.
Strategic value: gives honest acceptance truth for the minimum commercial floor.

#### KB-S54 — Cluster Runtime Wiring + System-Level Scoring Completion
Purpose: complete runtime/system-level output truth.
Application impact: outputs become more coherent, more connected, and less likely to feel like disconnected signal alerts.
Strategic value: this is the bridge from breadth into trustworthy phenotype-level reasoning.

---

## Wave 4 — Final Phase-1 Breadth Completion

### Purpose of this wave
Wave 4 completes the current known breadth programme and expands phenotype/fixture/regression truth so the enlarged engine is testable and trustworthy.

### Why this wave exists now
A larger engine without fixture truth, phenotype expansion, or SSOT clarity becomes fragile.
This wave is about finishing the planned breadth push without sacrificing governance.

### What this wave improves in the application
After Wave 4, the application should:
- cover a materially broader commercial panel surface
- have stronger phenotype and regression scaffolding
- be closer to credible minimum-market readiness

### How this wave advances the final platform
It closes the first major breadth build while increasing the realism and testability of the platform.

#### KB-S55 — Biomarker Ingestion Batch 5
Purpose: continue breadth completion in governed batch form.
Application impact: more biomarkers become part of the live engine.
Strategic value: closes remaining commercial-panel gaps.

#### KB-S56 — Renal Research Promotion + Renal WHY Completion
Purpose: finish the renal pathway after its prerequisite research promotion.
Application impact: fills one of the remaining structurally incomplete system domains.
Strategic value: renal completeness matters both clinically and for phenotype honesty.

#### KB-S57 — Biomarker Ingestion Batch 6 + SSOT Coverage Check
Purpose: finish the planned breadth programme and verify canonical/SSOT integrity.
Application impact: the engine becomes cleaner and more complete as a governed product surface.
Strategic value: reduces hidden coverage debt before later phases.

#### KB-S58 — Phenotype / Fixture / Regression Expansion
Purpose: strengthen fixture, phenotype, and regression truth across the enlarged estate.
Application impact: the platform becomes more dependable on the same kinds of panels and phenotypes it claims to understand.
Strategic value: makes the engine defensible and measurable at a higher breadth/depth level.

---

## Wave 5 — Context Hardening Before Narrative

### Purpose of this wave
Wave 5 makes non-biomarker inputs meaningfully governable.
This is where HealthIQ begins moving from blood-only interpretation to true metabolic context-aware reasoning.

### Why this wave exists now
Context materially changes interpretation, but the engine should not consume it loosely or prematurely.
By sequencing this after breadth, WHY, and structural truth, the roadmap protects the deterministic core while preparing for more intelligent outputs.

### What this wave improves in the application
After Wave 5, the application should:
- consume key objective and subjective context inputs in governed ways
- reduce the gap between collected user data and analytical use
- prepare the platform for more meaningful and safer translation/reporting

### How this wave advances the final platform
It moves HealthIQ beyond pure biomarker interpretation toward true metabolic interpretation.

#### BE-S0a — Objective Context Hardening
Purpose: formalise objective numeric inputs such as waist, BP, height, weight, and BMI-related measures.
Application impact: these inputs can begin to change structured interpretation lawfully.
Strategic value: improves deterministic metabolic relevance without narrative shortcuts.

#### BE-S0b — Subjective / Behavioural Context Hardening
Purpose: formalise governed use of smoking, alcohol, exercise, sleep, stress, and medication caveats.
Application impact: the platform becomes more realistic and context-aware while staying safe.
Strategic value: essential for long-term metabolic-platform credibility and future intervention tracking.

---

## Wave 6 — Narrative Translation Layer

### Purpose of this wave
Wave 6 enables user-facing narrative only after the engine underneath is broad, truthful, explainable, and context-aware enough to deserve translation.

### Why this wave exists now
Narrative must be the last layer, not the first. Otherwise the platform risks sounding intelligent without actually being trustworthy.

### What this wave improves in the application
After Wave 6, the application should:
- translate structured truth into human-readable outputs
- keep the frontend renderer-only
- deliver a more usable product experience without sacrificing deterministic integrity

### How this wave advances the final platform
This is the phase that turns a strong engine into a product experience while preserving governance boundaries.

#### BE-S1 — LLM Narrative Production Enablement
Purpose: enable narrative translation on top of governed structured intelligence.
Application impact: HealthIQ becomes more understandable to end users without putting reasoning into the LLM.
Strategic value: prepares the platform for product readiness without compromising engine truth.

#### FE-S2 — Narrative Presentation Layer
Purpose: render the narrative cleanly in the frontend.
Application impact: the user sees a coherent interpretation experience rather than raw structured output.
Strategic value: turns engine value into usable product value while keeping the UI logic-thin.

---

## 9. Phenotype direction and why it matters

The roadmap is not trying to build 50 fragmented phenotype labels.
The phenotype strategy is to begin with a small number of high-value, overlapping metabolic states that can be:
- biologically meaningful
- panel-visible
- cohortable
- commercially relevant
- useful for downstream dataset value

The phenotype coverage audit shows this work is already partially real in the codebase, but not yet evenly mature across pathways. In particular:
- insulin resistance, lipid transport, hepatic stress, systemic inflammation, thyroid, iron/oxygen, and renal stress all have some level of phenotype support
- but WHY and interaction-map completeness vary substantially by pathway
- renal remains especially incomplete due to missing promoted interaction edges
- many live signals still lack proper hypothesis assets fileciteturn26file0turn26file1

That means phenotype work should now be seen as a cross-wave concern:
- breadth gives phenotypes more building blocks
- WHY gives phenotypes explanatory depth
- interaction maps give phenotypes causal structure
- fixture and regression work give phenotypes truth and testability

---

## 10. Why this sequence is strategically correct

This sequence is designed to satisfy all of the following simultaneously:

1. widen coverage without waiting for all breadth to be complete
2. deepen WHY without over-investing in a too-narrow signal surface
3. avoid six straight ingestion sprints that create breadth without depth
4. avoid WHY work becoming detached from the real live signal estate
5. formalise runtime truth before narrative
6. explicitly harden context before allowing narrative to depend on it
7. keep the phenotype direction alive without pretending phenotype maturity already exists everywhere
8. preserve governance, auditability, and rollback discipline

This remains the strategic heart of the roadmap. The wording is expanded here so the logic is obvious rather than assumed. fileciteturn25file0turn26file0

---

## 11. What this plan is building by the end of Phase 1

By the end of this 12-month roadmap, HealthIQ should be much closer to:

- a broad deterministic metabolic reasoning engine
- a platform that can interpret realistic commercial blood panels, not just a narrow subset
- a governed WHY and root-cause system with much stronger explanatory depth
- a phenotype-aware interpretation engine rather than a bag of isolated signals
- an explicitly governed context-input layer combining biomarkers with key lifestyle, anthropometric, hemodynamic, and medication context
- a structurally complete platform ready for narrative translation
- a credible launch point for Phase 2 longitudinal and dataset-moat work

This is not the final company vision.
It is the first full platform-construction year.

---

## 12. What comes after this roadmap

### Phase 2 — Dataset moat
After the engine is stronger and structurally complete:
- repeat-panel journeys
- intervention tracking
- trajectory summaries
- phenotype-density growth
- longitudinal identity continuity
- observational validation

### Phase 3 — Regulated workflow and strategic buyer readiness
After the dataset loop is live:
- documented risk controls
- clinical evaluation plan
- workflow insertion
- outcomes linkage
- strategic-buyer fit
- acquisition-grade defensibility

---

## 13. Final strategic statement

This roadmap is not optimised for the fastest demo.

It is optimised for building the first full version of a deterministic metabolic platform safely, at pace, and without architectural dishonesty.

The guiding principle remains:

**Build breadth and depth together.**
**Formalise truth before narrative.**
**Move fast, but never in a way that puts the engine at risk.**
