# HealthIQ AI — Strategic Vision and 12-Month Sprint Plan
*Version 1.5 draft — proposed master strategic record for Phase 1*

> Draft note: This version preserves the governing strategic spine of v1.4 while updating the document to reflect current platform maturity more honestly, making product intent clearer to a cold reader, and strengthening protection against drift into a weaker product, unnecessary architectural detours, or micro-sprint fragmentation.

---

## 0. Why this document exists

This is not just a sprint list.

It is the master strategic record for Phase 1 of HealthIQ AI.

Its purpose is to ensure that every team member, sprint author, reviewer, and future operator can answer four questions clearly:

1. What are we building?
2. Why are we building it in this sequence?
3. What does each wave add to the final platform?
4. What kinds of drift are unacceptable, even if they look productive in the short term?

This document exists because delivery pressure, governance work, and local sprint concerns can gradually obscure system intent.

HealthIQ must not allow daily sprint execution to become the de facto product strategy.

---

## 1. Executive intent

HealthIQ AI is not being built as a prettier blood report.

It is being built as:

1. the reference platform for deterministic metabolic intelligence
2. a platform that can evolve toward clinician-grade and regulated workflow use
3. a data-and-reasoning infrastructure asset with long-term strategic buyer value

The strategy is therefore not “ship the fastest blood-test demo.”

The strategy is:

- build breadth and explanatory depth together
- protect the deterministic engine at all costs
- keep work packages large enough to move the product materially forward
- allow bounded maturity work only when it protects governed truth, future scale, or architectural integrity
- treat AB and VR as minimum commercial harnesses, not the final product boundary
- build toward phenotype-aware metabolic interpretation, not a disconnected catalogue of marker alerts
- end Phase 1 in a deployable market-ready product, not an engine without a usable product shell

This remains the governing strategic direction for Phase 1.

---

## 2. What HealthIQ is actually building

### 2.1 The product category

HealthIQ should be understood as a deterministic metabolic interpretation platform.

It is intended to:

- interpret realistic commercial blood panels
- convert biomarker data into governed metabolic signals
- connect those signals into pathway-level and system-level reasoning
- map users to one or more overlapping phenotype-level metabolic states
- explain why those states may be active
- incorporate governed non-biomarker context inputs
- produce clinician-grade structured outputs
- later support safe narrative translation, longitudinal tracking, and cohort intelligence

### 2.2 What it is not

HealthIQ is not:

- a generic LLM wrapper around blood tests
- a marker-by-marker commentary tool
- a traffic-light dashboard with more persuasive language
- a narrative-first product that compensates for weak analytical truth
- a frontend-heavy app with hidden biological logic in the UI
- a narrow AB/VR interpreter as the final ambition

### 2.3 The layered engine model

HealthIQ should be understood first through the canonical architecture boundary used across the platform documents.

#### Layer A — Canonicalisation and governed inputs
This layer receives raw lab data and converts it into governed analytical input.
It covers:
- biomarker values and lab ranges from the uploaded panel
- canonicalisation and normalisation of those values into the platform’s governed input form
- over time, governed non-biomarker context inputs such as anthropometrics, blood pressure, smoking, alcohol, medications, exercise, sleep, and stress

Layer A is the input and normalisation layer.
It must not become the place where clinical reasoning is improvised.

#### Layer B — Deterministic analytical engine
This is the biological reasoning core of HealthIQ.
It is where governed inputs are transformed into structured metabolic intelligence.

Inside Layer B, the platform builds through several connected internal components:
- signal activation and signal-state evaluation
- interaction and system-level reasoning
- phenotype formation and phenotype coherence
- WHY / root-cause reasoning
- structured output generation including clinician-grade reporting

In product terms, this is where HealthIQ moves beyond isolated marker commentary and toward deterministic metabolic interpretation.
A signal is not just “marker high” or “marker low.”
A signal is a governed deterministic claim about a biologically meaningful state.

Examples include:
- insulin resistance
- lipid transport dysfunction
- systemic inflammation
- thyroid-axis disturbance
- hepatic metabolic stress
- iron deficiency context

This means HealthIQ’s strategic ambition inside Layer B is not merely to accumulate more signals.
It is to connect signals into pathway-level, phenotype-aware, root-cause-capable metabolic reasoning.

#### Layer C — Narrative translation and presentation
Only after Layers A and B are coherent should the platform translate structured truth into human-readable language.

Layer C covers:
- user-facing narrative translation
- presentation of governed outputs
- readable explanation of structured truth

Layer C must never become the analytical engine.
It translates governed truth; it does not invent or replace it.

#### Why the A / B / C model matters
This distinction is strategically important because it keeps the product honest.
It prevents HealthIQ from drifting into a narrative-first product, a frontend-led interpretation product, or a weak blood-report application that sounds intelligent while compensating for incomplete deterministic truth.

---

## 3. Why phenotype direction matters

HealthIQ is not intended to stop at “ALT is high” or “triglycerides are high.”

The strategic destination is not a larger validated signal catalogue.
It is a phenotype-aware metabolic interpretation platform.

The Phase 1 position should therefore be stated clearly:

HealthIQ is building toward reliable phenotype-aware interpretation through governed signals, interactions, WHY assets, fixtures, and context inputs.

This does **not** mean phenotype maturity is already complete or even across all pathways.
It means Phase 1 should be understood as the construction of the substrate required for trustworthy phenotype-level interpretation.

The strategic frame is:

- signals = intelligence atoms
- interactions = biological structure
- phenotypes = interpretable metabolic states
- trajectories = future dataset value

If this is not made explicit, future teams may wrongly interpret the product as “more biomarkers + better explanations,” which is materially weaker than the platform actually being built.

---

## 4. Phase 1 success definition

By the end of this Phase 1 roadmap, HealthIQ should deliver not only a strong deterministic engine but a real deployable Phase 1 product that can be taken to market.

That means HealthIQ should be materially closer to a platform that can:

- interpret a realistic commercial blood panel deterministically
- emit non-contradictory biomarker and system-level outputs
- map users to one or more overlapping metabolic phenotypes
- explain key states with structured WHY reasoning
- use governed context inputs in a controlled and auditable way
- produce a coherent clinician-grade structured report
- support safe downstream Layer C narrative translation
- provide a functioning customer-facing frontend product experience
- provide authenticated customer access, including login and a My Account / account-management area
- reach privacy, security, and compliance readiness appropriate to the intended launch markets

The critical point is:

**Phase 1 does not end with an impressive engine alone.  
Phase 1 ends when the engine is embodied in a real launchable product shell.**

That Phase 1 product shell should include, at minimum:

- deterministic Layer B analytical truth as the core product asset
- Layer C narrative translation operating only on governed structured outputs
- a working frontend experience for customers
- authenticated access and account management
- the operational/privacy/compliance foundations needed for deployment

This is the bridge between:

- a blood interpretation tool
- a metabolic intelligence platform
- a deployable Phase 1 product
- a future longitudinal dataset engine

---

## 5. Long-term company vision

The long-term company vision still has three strategic layers.

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

This roadmap is therefore not merely an MVP plan.
It is the first serious year of building the platform that makes those later moats possible.

---

## 6. Current baseline and reality check

### 6.1 What is already materially true

Several important architectural and delivery foundations are already in place.

These include:
- clinician-report contract and renderer path
- intelligence-model and investigation-spec contract hardening
- Knowledge Bus governance alignment
- intervention-effects registry foundation
- live runtime signal, package, and test infrastructure beyond the original narrow early baseline

This matters because the platform has already moved beyond the maturity assumed by some earlier strategy language.

### 6.2 Where repo maturity has advanced materially

The platform’s signal breadth has advanced materially beyond the original “six batches / 56 additional biomarkers” framing.

The strategic implication is important:

HealthIQ is no longer primarily constrained by whether it can ingest more biomarkers at all.
It is increasingly constrained by whether the enlarged signal estate is matched by:
- sufficient WHY depth
- coherent interaction-map maturity
- phenotype truth and fixture coverage
- governed context consumption
- robust analytical correctness and runtime semantics

### 6.3 What remains materially incomplete

The most important incomplete areas now are:

1. WHY / root-cause coverage remains too shallow relative to live signal breadth
2. phenotype and chain maturity remain uneven across pathways
3. renal remains a gated structural weak point
4. context consumption is not yet governed strongly enough to count as a completed platform layer
5. structural truth is now less about absence of runtime wiring and more about correctness, coherence, and trusted semantics
6. narrative should still not be treated as a priority layer until these conditions are stronger

### 6.4 Breadth is not the same as completion

It is important that future readers do not mistake increased signal or package counts for Phase 1 completion.

More signal breadth is valuable.
But breadth without enough WHY, interaction, phenotype, and context maturity risks producing a larger but still strategically weaker engine.

### 6.5 Context reality

HealthIQ must not treat biomarker values as the only meaningful inputs.

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

These matter because they:
1. materially change interpretation of biomarker patterns
2. strengthen WHY reasoning beyond blood chemistry alone
3. help move the product from blood-report app toward metabolic platform

### 6.6 Medication and intervention boundary

Medication handling remains bounded in Phase 1.

HealthIQ is **not** building a drug library.
Canonical intervention knowledge should remain governed through a class-level intervention-effects registry.
User intervention/exposure state remains separate from canonical knowledge.
Medication context may surface caveats and interpretation warnings, but it must not silently alter analytical thresholds or invent medication-specific reasoning unless later governance explicitly authorises that behaviour.

---

## 7. Core planning principles

These are non-negotiable.

### 7.1 Deterministic analytics only
No LLM reasoning in the analytical core.

### 7.2 LLM as translation layer only
Narrative may sit on top of governed structured output.
It must never become the source of metabolic reasoning.

### 7.3 Breadth-depth braid
The platform must not front-load all ingestion before all WHY work, nor all WHY work before breadth is adequate.
Breadth and depth must advance together in meaningful waves.

### 7.4 No micro-sprints for their own sake
Work packages must be large enough to move the product materially forward.
They should only be split when:
- governance risk requires it
- rollback risk becomes unacceptable
- testability degrades
- audit scope becomes too broad

Caution is not a justification for fragmentation.

### 7.5 Safety with pace
Every sprint must remain bounded, testable, auditable, and reversible where feasible.

### 7.6 AB/VR are a floor, not the destination
AB and VR are the minimum commercial harnesses.
They are not the strategic ontology or commercial boundary of the platform.

### 7.7 Governed context inputs are part of the platform
Context inputs are not questionnaire decoration.
They are part of the deterministic interpretive substrate and must be governed accordingly.

### 7.8 Governed truth beats research accumulation
Research JSON, draft artefacts, or partially prepared assets are not product truth.
Knowledge becomes product truth only when it is translated into governed runtime-recognised artefacts.

### 7.9 Bounded maturity work is permitted only for protection, not drift
Foundational maturity work is allowed when it protects governed truth, future scale, contract integrity, or architectural correctness.
It must not become a standing excuse for endless architecture detours.

---

## 8. Anti-drift doctrine

The roadmap must explicitly defend against five failure modes.

### 8.1 Shallow blood-report drift
The platform must not degrade into a prettier consumer blood report with nicer explanation language.

### 8.2 Disconnected signal-engine drift
The platform must not become merely a larger validated catalogue of isolated biomarker signals.
Signals must increasingly contribute to pathway reasoning, phenotype interpretation, and coherent metabolic states.

### 8.3 Narrative-first drift
The platform must not sound intelligent before the deterministic substrate deserves translation.

### 8.4 Architecture-for-its-own-sake drift
The platform must not disappear into endless contract and governance work that is no longer materially improving product truth, scale, or defensibility.

### 8.5 Micro-sprint fragmentation drift
The platform must not be slowed by over-splitting large meaningful work into tiny procedural sprints that protect process more than product.

---

## 9. How to read the roadmap

The roadmap should be read as six connected build phases:

1. **Breadth waves** expand the signal surface so the engine can see more of real-world metabolism.
2. **WHY waves** deepen explanatory reasoning in the most important metabolic domains.
3. **Structural-truth waves** make outputs coherent, testable, and panel-truthful.
4. **Phenotype / fixture / regression waves** make multi-signal states stable enough to trust.
5. **Context-hardening waves** make non-biomarker inputs governable and meaningful.
6. **Narrative waves** translate governed truth into user-facing language safely.

This is not a list of technical chores.
It is the staged construction of a phenotype-aware deterministic metabolic platform.

---

# 10. The 12-month strategic build plan

## Wave 1 — Breadth and Depth, Pass 1

### Purpose of this wave
Wave 1 gives HealthIQ enough early breadth to matter and enough WHY depth to begin feeling intelligent rather than descriptive.

### Why this wave exists
Without early breadth, the platform stays too narrow to matter commercially.
Without early WHY, it risks becoming a broader but still shallow engine.

### What this wave improves in the application
After Wave 1, the application should be able to:
- interpret a broader panel surface
- explain a few central metabolic domains more intelligently
- begin moving beyond abnormality surfacing in high-value pathways

#### KB-S45 — Biomarker Ingestion Batch 1
Purpose: broaden analytical surface with the first pre-researched batch.
Strategic note: in historical roadmap terms this remains part of the original breadth braid, but final Phase 1 planning must now treat ingestion more as estate-completion and quality-governed expansion than as an untouched future surface.

#### KB-S46 — WHY Expansion 1: Insulin Resistance + Systemic Inflammation
Purpose: deepen reasoning in two central metabolic pathways.
Strategic value: high prevalence, high explanatory value, strong relevance to phenotype direction.

#### KB-S47 — Biomarker Ingestion Batch 2
Purpose: continue widening the real-world signal surface.
Strategic note: breadth work must remain aligned to governed translation and promotion, not raw research accumulation.

#### KB-S48 — WHY Expansion 2: Lipid / Vascular
Purpose: add clinically important explanation in a commercially central domain.
Strategic value: strengthens cardiovascular interpretation and early phenotype scaffolding.

---

## Wave 2 — Breadth and Depth, Pass 2

### Purpose of this wave
Wave 2 repeats the braid at a more mature level, adding breadth while deepening additional biological systems that are common, clinically important, and commercially visible.

### Why this wave exists
By this point the platform should not just know more markers. It should begin to reason more credibly across iron, oxygen transport, hepatic extension, and thyroid.

### What this wave improves in the application
After Wave 2, the application should:
- interpret more common real-world blood patterns
- cover iron, oxygen, hepatic, and thyroid reasoning more convincingly
- move closer to true metabolic interpretation rather than anomaly commentary

#### KB-S49 — Biomarker Ingestion Batch 3
Purpose: continue expanding the governed signal surface.

#### KB-S50 — WHY Expansion 3: Iron / Oxygen + Iron Overload Phenotype
Purpose: deepen iron and oxygen-transport reasoning, including overload and deficiency frames.
Strategic value: common domain, phenotype relevance, important current gap.

#### KB-S51 — Biomarker Ingestion Batch 4
Purpose: continue breadth expansion in governed batch form.

#### KB-S52 — WHY Expansion 4: Hepatic Extension + Thyroid Completion
Purpose: deepen hepatic and thyroid explanation beyond current partial coverage.
Strategic value: strengthens system-level reasoning in important control systems.

---

## Wave 3 — Structural Truth and Platform Hardening

### Purpose of this wave
Wave 3 turns HealthIQ from a broadening engine into a trustworthy one.

### Why this wave exists
A platform that knows more biology but produces contradictory, semantically weak, or poorly trusted outputs is not commercially or clinically credible.

### What this wave improves in the application
After Wave 3, the application should:
- treat AB/VR as real acceptance harnesses
- produce more coherent structured outputs
- move closer to trusted multi-signal interpretation
- provide a stronger substrate for phenotype reasoning and later narrative

#### KB-S53 — AB/VR Panel Formalisation + Acceptance Harness
Purpose: formalise AB and VR as explicit acceptance truth rather than relying only on informal fixture meaning.
Strategic note: AB/VR remain the floor, but the platform must also acknowledge wider live coverage beyond them.

#### KB-S54 — Cluster Runtime Wiring + System-Level Scoring Completion
Purpose: complete trustworthy runtime/system-level output behaviour.
Strategic note: this wave is now less about whether clustering exists at all and more about whether system-level interpretation is coherent, correct, and trusted.

---

## Wave 4 — Final Phase-1 Breadth Completion

### Purpose of this wave
Wave 4 completes the planned breadth programme while expanding phenotype, fixture, and regression truth so the enlarged engine is testable and trustworthy.

### Why this wave exists
A larger engine without fixture truth, phenotype realism, or SSOT clarity becomes fragile.

### What this wave improves in the application
After Wave 4, the application should:
- cover a materially broader commercial panel surface
- have stronger phenotype and regression scaffolding
- be closer to credible minimum-market readiness

#### KB-S55 — Biomarker Ingestion Batch 5
Purpose: continue governed breadth completion.

#### KB-S56 — Renal Research Promotion + Renal WHY Completion
Purpose: complete the renal pathway after its prerequisite research promotion.
Strategic value: renal remains a special-case gap and should not be left structurally weak.

#### KB-S57 — Biomarker Ingestion Batch 6 + SSOT Coverage Check
Purpose: finish the planned breadth programme and verify canonical integrity.

#### KB-S58 — Phenotype / Fixture / Regression Expansion
Purpose: strengthen phenotype truth, fixtures, and regression coverage across the enlarged estate.
Strategic value: this is a key anti-drift wave because it prevents the platform from becoming a broad but weakly testable engine.

---

## Wave 5 — Context Hardening Before Narrative

### Purpose of this wave
Wave 5 makes non-biomarker inputs meaningfully governable.
This is where HealthIQ moves from blood-only interpretation toward true metabolic context-aware reasoning.

### Why this wave exists
Context materially changes interpretation, but the engine should not consume it loosely or prematurely.

### What this wave improves in the application
After Wave 5, the application should:
- consume key objective and subjective context inputs in governed ways
- reduce the gap between collected user data and actual analytical use
- prepare the platform for safer and more meaningful translation/reporting

#### BE-S0a — Objective Context Hardening
Purpose: formalise objective inputs such as waist, BP, height, weight, and BMI-related measures.

#### BE-S0b — Subjective / Behavioural Context Hardening
Purpose: formalise governed use of smoking, alcohol, exercise, sleep, stress, and medication caveats.

---

## Wave 6 — Narrative, Product Shell, and Launch Readiness

### Purpose of this wave
Wave 6 completes the transition from strong deterministic engine to real deployable Phase 1 product.

### Why this wave exists
Narrative must still come last, not first.
But Phase 1 also cannot end with engine truth floating in isolation.
To be genuinely market-ready, HealthIQ needs the product shell around the engine: readable outputs, customer access, account management, and deployment-grade privacy/compliance readiness.

### What this wave improves in the application
After Wave 6, the application should:
- translate structured truth into readable outputs
- keep the frontend renderer-only for biological logic
- provide a functioning customer-facing product experience
- provide authenticated access and account-management capability
- be materially closer to deployment readiness for the intended launch markets

#### BE-S1 — LLM Narrative Production Enablement
Purpose: enable narrative translation on top of governed structured intelligence.
Strategic note: this remains downstream of deterministic truth and must never become a substitute for it.

#### FE-S2 — Narrative Presentation Layer
Purpose: render the narrative cleanly in the frontend.

#### FE-S3 — Customer Login and My Account Layer
Purpose: provide authenticated customer access, account management, and the core user-facing product shell needed for a deployable Phase 1 release.
Strategic note: this is not separate from the engine moat goal; it is part of converting the engine into a real market-ready product.

#### OPS-S1 — Privacy, Security, and Launch Readiness
Purpose: establish the privacy, security, and deployment-readiness foundations required for a Phase 1 go-to-market product.
Scope should include the compliance, data-governance, and operational controls appropriate to the intended launch markets.
Strategic note: this does not mean full later-stage regulated-product completion; it means HealthIQ must be deployable responsibly at the end of Phase 1.

---

## 11. How the roadmap should now be interpreted

The roadmap should no longer be read as though the platform is still at the very start of signal breadth construction.

It should be read as a Phase 1 completion plan in which:
- breadth has already advanced materially
- WHY depth is still too shallow relative to breadth
- phenotype and interaction maturity remain uneven
- renal remains a gated weak point
- context consumption is not yet fully governed
- narrative must remain last

This is the most important interpretation update from v1.4 to v1.5.

---

## 12. Why this sequence is strategically correct

This sequence is designed to satisfy all of the following simultaneously:

1. widen coverage without waiting for all breadth to be complete
2. deepen WHY without over-investing in a too-narrow signal surface
3. avoid a large signal estate with weak explanatory depth
4. avoid WHY work becoming detached from the live signal estate
5. formalise runtime and phenotype truth before narrative
6. explicitly harden context before allowing narrative to depend on it
7. keep phenotype direction alive without pretending phenotype maturity already exists everywhere
8. preserve governance, auditability, and rollback discipline
9. move at pace without letting process fragment the product into trivial sprint slices

---

## 13. What this plan is building by the end of Phase 1

By the end of this roadmap, HealthIQ should be much closer to:

- a broad deterministic metabolic reasoning engine
- a platform that can interpret realistic commercial blood panels, not just a narrow subset
- a governed WHY and root-cause system with much stronger explanatory depth
- a phenotype-aware interpretation engine rather than a bag of isolated signals
- an explicitly governed context-input layer combining biomarkers with key lifestyle, anthropometric, hemodynamic, and medication context
- a structurally coherent platform ready for narrative translation
- a functioning deployable product shell around the engine, including frontend experience, login, and account capability
- privacy, security, and compliance readiness appropriate to a Phase 1 market launch
- a credible launch point for both real market entry and Phase 2 longitudinal / dataset-moat work

This is not the final company vision.
It is the first full platform-construction year and should culminate in a real launchable Phase 1 product, not just a technically impressive engine.

---

## 14. What comes after this roadmap

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

## 15. Final strategic statement

This roadmap is not optimised for the fastest demo.

It is optimised for building the first full version of a deterministic metabolic platform safely, at pace, and without architectural dishonesty.

The guiding principle remains:

**Build breadth and depth together.**
**Formalise truth before narrative.**
**Move fast, but never in a way that weakens the engine or fragments the build into trivial work.**
