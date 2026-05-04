# HealthIQ AI — Strategic Vision and 12-Month Sprint Plan
 *Version 1.5 revision v7 — master strategic record for Phase 1*

> Revision note: This version preserves the governing strategic spine of v1.4 while updating the document to reflect current platform maturity more honestly, making product intent clearer to a cold reader, hardening operational rules that were accidentally omitted in earlier v1.5 drafts, and correcting the sequencing of the customer/product-shell build so that Phase 1 ends in a real launchable product rather than a strong engine wrapped too late.

---

## 0. Why this document exists

This is not just a sprint list.

It is the master strategic record for Phase 1 of HealthIQ AI.

Its purpose is to ensure that every team member, sprint author, reviewer, and future operator can answer clearly:

1. What are we building?
2. Why are we building it in this sequence?
3. What does each wave add to the final platform?
4. What kinds of drift are unacceptable, even if they look productive in the short term?
5. What must be true before Phase 1 can be considered commercially launchable?

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
- end Phase 1 with a real deployable market-ready product, not just an impressive engine

### 1.1 Governance infrastructure is part of the moat

HealthIQ's moat is not only analytical depth. It also includes the governance discipline used to preserve deterministic truth as the platform scales.

The Knowledge Bus, Automation Bus, validator authority, hardened sprint protocol, deterministic gate, and audit discipline are not incidental overhead. They are part of how HealthIQ protects analytical integrity while continuing to expand the platform.

That governance layer should not be traded away for apparent speed.

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
- support a real authenticated product experience for end users and clinicians
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

Phase 1 does **not** end when the engine is merely interesting.
Phase 1 ends when HealthIQ has a deployable first commercial product built on governed deterministic truth.

By the end of this Phase 1 roadmap, HealthIQ should be able to:

### 4.1 Analytical truth gate
- interpret a realistic commercial blood panel deterministically
- emit non-contradictory biomarker and system-level outputs
- map users to one or more overlapping metabolic phenotypes in the pathways that are declared governed for Phase 1
- explain key states with structured WHY reasoning
- use governed context inputs in a controlled and auditable way
- produce a coherent clinician-grade structured report
- support safe downstream narrative translation

### 4.2 Product and launch gate
- provide a working frontend product experience rather than isolated upload/results screens only
- provide authenticated customer access and persistent account capability
- provide report history, analysis continuity, and account/profile surfaces
- deliver Layer C narrative on top of governed Layer B truth
- meet the privacy, compliance, data-governance, and operational readiness requirements appropriate to the intended launch markets
- be deployable as a real product, not merely reviewable as a technical platform

This is the bridge between:
- a blood interpretation tool
- a metabolic intelligence platform
- a first commercial product
- a future longitudinal dataset engine

---

## 5. Long-term company vision

The long-term company vision still has three strategic layers.

### Phase 1 — Engine moat
Build the best deterministic metabolic reasoning engine in the market, embodied in a real first-launch product.

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

### 6.1 Current baseline snapshot
The figures below should always be read as time-stamped baseline facts, not eternal truths.

| Metric | Baseline state for this revision |
|---|---|
| Latest completed sprint in live repo reality | KB-S61 |
| Canonical biomarkers in SSOT | 103 |
| Knowledge Bus package estate | 187 packages |
| Signal estate | ~234 signals across packages |
| WHY hypothesis coverage | Still narrow relative to live signal breadth; the majority of live signals still produce no WHY reasoning at runtime |
| Renal interaction-map status | Structurally incomplete; zero active renal interaction edges |
| Authentication status | Disabled/unfinished foundation; not yet a production-capable auth layer |
| Narrative layer | Infrastructure and direction exist; production-governed launch path not yet complete |

### 6.2 What is already materially true
Several important architectural and delivery foundations are already in place.

These include:
- clinician-report contract and renderer path
- intelligence-model and investigation-spec contract hardening
- Knowledge Bus governance alignment
- intervention-effects registry foundation
- live runtime signal, package, and test infrastructure beyond the original narrow early baseline

This matters because the platform has already moved beyond the maturity assumed by some earlier strategy language.

### 6.3 Where repo maturity has advanced materially
The platform’s signal breadth has advanced materially beyond the original “six batches / 56 additional biomarkers” framing.

The strategic implication is important:

HealthIQ is no longer primarily constrained by whether it can ingest more biomarkers at all.
It is increasingly constrained by whether the enlarged signal estate is matched by:
- sufficient WHY depth
- coherent interaction-map maturity
- phenotype truth and fixture coverage
- governed context consumption
- robust analytical correctness and runtime semantics
- product-shell readiness for market launch

### 6.4 What remains materially incomplete
The most important incomplete areas now are:

1. the majority of live signals still do not produce governed WHY reasoning at runtime
2. phenotype and chain maturity remain uneven across pathways
3. renal remains structurally incomplete rather than merely “weaker”
4. context consumption is not yet governed strongly enough to count as a completed platform layer
5. structural truth is now less about absence of runtime wiring and more about correctness, coherence, and trusted semantics
6. authentication, persistence, account management, and customer-history surfaces are not yet complete enough to support a commercial launch
7. narrative should still not be treated as a priority layer until these conditions are stronger

### 6.5 Breadth is not the same as completion
It is important that future readers do not mistake increased signal or package counts for Phase 1 completion.

More signal breadth is valuable.
But breadth without enough WHY, interaction, phenotype, context, and product-shell maturity risks producing a larger but still strategically weaker platform.

### 6.6 Context reality
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

### 6.7 Medication and intervention boundary
Medication handling remains bounded in Phase 1.

HealthIQ is **not** building a drug library.
Canonical intervention knowledge should remain governed through a class-level intervention-effects registry.
User intervention/exposure state remains separate from canonical knowledge.
Medication context may surface caveats and interpretation warnings, but it must not silently alter analytical thresholds or invent medication-specific reasoning unless later governance explicitly authorises that behaviour.

### 6.8 Upstream research pipeline reality
Upstream research generation is no longer an informal precursor to ingestion.
New investigation-spec generation should be understood as flowing through the governed multi-pass research pipeline with operator checklist, gold exemplar discipline, and validation before promotion-adjacent work begins.

This matters because ingestion and WHY expansion should not be authored as if governed source material simply appears ready for runtime use.
Upstream research is now part of the governed production path.

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

### 7.10 Product-shell work must not be deferred to the end
Customer auth, persistence, account continuity, and product-shell surfaces are not decorative launch extras.
They are part of Phase 1 commercial viability and must begin before the final launch wave.

---

## 8. Sprint classification rules going forward

These rules are part of the strategic record because they are the operational interpretation of the governing principles.

### 8.1 Ingestion sprints
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

### 8.2 WHY expansion sprints
Default classification:
- change_type: MIXED
- risk_level: HIGH

These sprints touch hypothesis assets, compiler-linked behavioural logic, confirmatory logic, and regression surfaces.

Each WHY sprint must have a mechanical prerequisite:
- clinical content must be authored first
- the prompt must include a STOP condition if the required hypothesis assets do not already exist

This rule is mandatory.

### 8.3 Structural completion sprints
Panel formalisation, cluster runtime wiring, renal completion, phenotype truth expansion, and major fixture expansion are governed as backend / mixed architectural work, with risk level determined by the exact touched files.

### 8.4 Context-hardening sprints
Questionnaire / lifestyle / medication-context hardening work is governed as backend or mixed product-integration work.

Default intent:
- formalise which context fields are first-class inputs
- distinguish numeric/objective inputs from subjective/categorical inputs and govern consumption appropriately
- verify mapping from collected input to governed runtime consumption
- prevent silent drift between questionnaire capture, mapper logic, overlays, and user-facing narrative
- keep medication handling inside an explicitly bounded interpretation-caveat model unless a later sprint authorises deeper medication-aware reasoning

Risk rule:
- if touched-file scope stays inside mapper, questionnaire, registry, contract, or renderer-adjacent integration code, classification may remain below HIGH subject to hardening review
- if touched-file scope crosses into `backend/core/analytics/`, `backend/core/pipeline/`, overlay logic that changes signal/runtime behaviour, or any control-plane authority, classification escalates to HIGH automatically
- prompt authors must state this explicitly when these sprints are authored

### 8.5 Narrative sprints
Narrative enablement must remain downstream of structured engine completeness.
No narrative sprint may introduce LLM reasoning into the analytical path.

### 8.6 Product-foundation sprints
Authentication, persistence, account continuity, dashboard/history, and user-facing product-shell work should be classified according to the touched surfaces:
- frontend-only work may remain CONTENT or MIXED depending on scope
- any backend auth, persistence, session, or data-access changes should be classified according to the behavioural and contract surfaces touched
- where data persistence, access control, privacy, or session semantics are introduced, prompt scoping must be explicit before authorship

---

## 9. Active pre-sprint and ingestion governance rules

### 9.1 One-off compatibility check rule
Before any remaining ingestion wave is authored, the compatibility status of the relevant source batch must be explicitly known.

The compatibility check exists to confirm:
- which biomarker IDs are already in SSOT
- which derived metrics already exist in the ratio registry
- any missing derived metric prerequisites
- any schema or naming mismatches that would block clean ingestion
- whether the translation path from JSON source material into canonical KB package artefacts is clear

If this check has already been completed for a tranche, that fact should be recorded.
If not, it remains an active rule.

### 9.2 Ingestion translation rule
Each ingestion batch consists of investigation-spec JSON source files.

Those JSON files are:
- structured research assets
- ingestion-friendly source material
- not yet canonical Knowledge Bus package artefacts

Therefore, every ingestion sprint must explicitly include:
1. translation of the batch JSON source material into canonical KB package assets
2. SSOT and registry compatibility confirmation
3. validator-passing package creation
4. fixture or synthetic-panel confirmation that the new signals fire as expected
5. promotion-readiness evidence consistent with current KB governance

No sprint may assume that JSON assets are directly promotable by the Knowledge Bus lifecycle without this translation step.

---

## 10. Known governance debt to carry explicitly

A master strategic record should not leave known governance debt undocumented.

### 10.1 KB SOP update debt
Known SOP carry-forward work from earlier governance sprints should be explicitly acknowledged as Phase 1 governance debt and given a home in the roadmap rather than left implicit.

This work does not outrank product truth, but nor should it disappear from strategic view.
It belongs alongside structural-truth / governance hardening work, not outside the roadmap entirely.

### 10.2 Documentation hierarchy and authority drift
The wider documentation estate contains historical and superseded planning artefacts.
Future operators should continue to rely on the documentation hierarchy and current authority documents rather than treating every planning file in the repo as equally binding.

---

## 11. Anti-drift doctrine

The roadmap must explicitly defend against five failure modes.

### 11.1 Shallow blood-report drift
The platform must not degrade into a prettier consumer blood report with nicer explanation language.

### 11.2 Disconnected signal-engine drift
The platform must not become merely a larger validated catalogue of isolated biomarker signals.
Signals must increasingly contribute to pathway reasoning, phenotype interpretation, and coherent metabolic states.

### 11.3 Narrative-first drift
The platform must not sound intelligent before the deterministic substrate deserves translation.

### 11.4 Architecture-for-its-own-sake drift
The platform must not disappear into endless contract and governance work that is no longer materially improving product truth, scale, or defensibility.

### 11.5 Micro-sprint fragmentation drift
The platform must not be slowed by over-splitting large meaningful work into tiny procedural sprints that protect process more than product.

---

## 12. How to read the roadmap

The roadmap should be read as six connected build phases plus a parallel product-foundation thread:

1. **Breadth waves** expand the signal surface so the engine can see more of real-world metabolism.
2. **WHY waves** deepen explanatory reasoning in the most important metabolic domains.
3. **Structural-truth waves** make outputs coherent, testable, and panel-truthful.
4. **Phenotype / fixture / regression waves** make multi-signal states stable enough to trust.
5. **Context-hardening waves** make non-biomarker inputs governable and meaningful.
6. **Narrative and launch waves** translate governed truth into user-facing language safely.
7. **Product-foundation thread** builds authentication, persistence, account continuity, and usable product surfaces in parallel rather than leaving them all to the final wave.

This is not a list of technical chores.
It is the staged construction of a phenotype-aware deterministic metabolic platform and its first commercial product shell.

---

# 13. The 12-month strategic build plan

## 13.0 Important roadmap interpretation note on sprint IDs
The original v1.4 roadmap described Waves 1–4 using KB-S45 through KB-S58 as the strategic planning sequence.

Repo reality has since moved beyond that original planning window.
Therefore, this section should be read as a **logical wave plan**, not as a claim that the original KB-S45–KB-S58 labels still map one-to-one to current repo sprint numbers.

Where historic sprint IDs are retained below, they are retained for strategic lineage and traceability, not as a guarantee that repo meaning has remained frozen.

---

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

#### Historical lineage: KB-S45 — Biomarker Ingestion Batch 1
Purpose: broaden analytical surface with the first pre-researched batch.
Strategic note: in historical roadmap terms this remains part of the original breadth braid, but final Phase 1 planning must now treat ingestion more as estate-completion and quality-governed expansion than as an untouched future surface.
Batch identification note: at the time of authoring, the sprint prompt author must identify the target source batch from available ungated research artefacts in `knowledge_bus/research/`. Batch readiness must be confirmed against the current KB SOP before the prompt is written. No ingestion sprint may be authored against a batch that has not been confirmed as pipeline-ready.

#### Historical lineage: KB-S46 — WHY Expansion 1: Insulin Resistance + Systemic Inflammation
Purpose: deepen reasoning in two central metabolic pathways.
Strategic value: high prevalence, high explanatory value, strong relevance to phenotype direction.
Status: complete as of KB-S46 — hypothesis assets exist and are registered in the compiler. No remaining sprint work is assumed for this specific workstream unless later hardening reveals a new governed gap.

#### Historical lineage: KB-S47 — Biomarker Ingestion Batch 2
Purpose: continue widening the real-world signal surface.
Strategic note: breadth work must remain aligned to governed translation and promotion, not raw research accumulation.
Batch identification note: at the time of authoring, the sprint prompt author must identify the target source batch from available ungated research artefacts in `knowledge_bus/research/`. Batch readiness must be confirmed against the current KB SOP before the prompt is written. No ingestion sprint may be authored against a batch that has not been confirmed as pipeline-ready.

#### Historical lineage: KB-S48 — WHY Expansion 2: Lipid / Vascular
Purpose: add clinically important explanation in a commercially central domain.
Strategic value: strengthens cardiovascular interpretation and early phenotype scaffolding.
Structural prerequisite: this workstream must not be authored as though lipid WHY is a pure hypothesis task. The lipid interaction-map structure beneath `signal_lipid_transport_dysfunction` must be explicitly checked and, if still incomplete, unblocked as part of the governed prerequisite path before convincing WHY reasoning is claimed.

---

## Wave 2 — Breadth and Depth, Pass 2 + Product Foundation Start

### Purpose of this wave
Wave 2 repeats the braid at a more mature level, adding breadth while deepening additional biological systems that are common, clinically important, and commercially visible.

At the same time, this is the point where the commercial product foundation must begin in parallel.
Product-shell work must not wait until the final launch wave.

### Why this wave exists
By this point the platform should not just know more markers. It should begin to reason more credibly across iron, oxygen transport, hepatic extension, and thyroid.
At the same time, auth and product-foundation delay creates unacceptable launch risk if pushed too late.

### What this wave improves in the application
After Wave 2, the application should:
- interpret more common real-world blood patterns
- cover iron, oxygen, hepatic, and thyroid reasoning more convincingly
- move closer to true metabolic interpretation rather than anomaly commentary
- begin building the real customer/product shell needed for Phase 1 launch

#### Historical lineage: KB-S49 — Biomarker Ingestion Batch 3
Purpose: continue expanding the governed signal surface.
Batch identification note: at the time of authoring, the sprint prompt author must identify the target source batch from available ungated research artefacts in `knowledge_bus/research/`. Batch readiness must be confirmed against the current KB SOP before the prompt is written. No ingestion sprint may be authored against a batch that has not been confirmed as pipeline-ready.

#### Historical lineage: KB-S50 — WHY Expansion 3: Iron / Oxygen + Iron Overload Phenotype
Purpose: deepen iron and oxygen-transport reasoning, including overload and deficiency frames.
Strategic value: common domain, phenotype relevance, important current gap.

#### Historical lineage: KB-S51 — Biomarker Ingestion Batch 4
Purpose: continue breadth expansion in governed batch form.
Batch identification note: at the time of authoring, the sprint prompt author must identify the target source batch from available ungated research artefacts in `knowledge_bus/research/`. Batch readiness must be confirmed against the current KB SOP before the prompt is written. No ingestion sprint may be authored against a batch that has not been confirmed as pipeline-ready.

#### Historical lineage: KB-S52 — WHY Expansion 4: Hepatic Extension + Thyroid Completion
Purpose: deepen hepatic and thyroid explanation beyond current partial coverage.
Strategic value: strengthens system-level reasoning in important control systems.

#### FE-FOUNDATION — Authentication and product access foundation
Purpose: begin the product-shell thread no later than Wave 2.

Minimum intent:
- backend auth foundation and session model
- frontend login / register entry points
- route/session gating for authenticated product surfaces
- explicit scoping of persistence and account boundaries
- resolution of the current “auth is effectively disabled” state

Strategic note: this thread runs in parallel with engine work and is not dependent on full engine completion.

---

## Wave 3 — Structural Truth and Platform Hardening + Product Persistence

### Purpose of this wave
Wave 3 turns HealthIQ from a broadening engine into a trustworthy one while also laying the persistence and continuity foundations needed for a real product.

### Why this wave exists
A platform that knows more biology but produces contradictory, semantically weak, or poorly trusted outputs is not commercially or clinically credible.
Likewise, a “product” without persistence, continuity, or usable history is not commercially ready.

### What this wave improves in the application
After Wave 3, the application should:
- treat AB/VR as real acceptance harnesses
- produce more coherent structured outputs
- move closer to trusted multi-signal interpretation
- establish user/account persistence and analysis continuity

#### Historical lineage: KB-S53 — AB/VR Panel Formalisation + Acceptance Harness
Purpose: formalise AB and VR as explicit acceptance truth rather than relying only on informal fixture meaning.
Strategic note: AB/VR remain the floor, but the platform must also acknowledge wider live coverage beyond them.

#### Historical lineage: KB-S54 — Cluster Runtime Wiring + System-Level Scoring Completion
Purpose: complete trustworthy runtime/system-level output behaviour.
Strategic note: this wave is now less about whether clustering exists at all and more about whether system-level interpretation is coherent, correct, and trusted.

Preflight orientation: before this sprint is authored, the prompt author must read the current state of `backend/core/clustering/cluster_engine_v2.py`, `backend/core/analytics/system_burden_engine.py`, and `backend/core/analytics/scoring_policy_registry.py` and identify specific coherence or correctness gaps against the AB and VR acceptance panels. The sprint must close a named, verified gap. If no specific gap is confirmed in preflight, the sprint is a no-op and must not proceed.

#### GOV-UPDATE — KB SOP carry-forward and governance debt cleanup
Purpose: explicitly clear known strategic governance debt rather than leaving it implicit.

Preflight orientation: the specific debt items for this sprint must be drawn from outstanding action items in automation_bus/ gate evidence and KB SOP review artefacts at the time of authoring. The prompt author must enumerate the specific items before the prompt is written. This sprint must not be authored as open-ended governance cleanup. If no confirmed outstanding debt exists at authoring time, this sprint is a no-op and must not proceed.

#### FE-PERSISTENCE — Analysis persistence and continuity foundation
Purpose:
- persist user analyses/results
- define the minimum Phase 1 persistence model
- support dashboard/history continuity
- support future report retrieval and authenticated product use

Strategic note: this work must also align with privacy/compliance assumptions and should not be treated as a cosmetic frontend concern.

#### FE-VISUALISATION — Core reusable product visualisation surfaces
Purpose: implement the visualisation and user-facing structured-output surfaces that are necessary for a usable product, not just a raw results page.

Preflight orientation: the confirmed stub components requiring implementation are `BiomarkerChart`, `ClusterCard`, `InsightPanel`, and `PipelineStatus`. Preflight should confirm current stub state and identify the data contracts each component must satisfy from the existing results pipeline. Scope is bounded to these four components unless a specific additional gap is confirmed in preflight.

---

## Wave 4 — Final Phase-1 Breadth Completion + Product Surfaces

### Purpose of this wave
Wave 4 completes the planned breadth programme while expanding phenotype, fixture, and regression truth so the enlarged engine is testable and trustworthy.
In parallel, it turns persistence into usable customer product surfaces.

### Why this wave exists
A larger engine without fixture truth, phenotype realism, or SSOT clarity becomes fragile.
A persisted product without usable pages remains commercially incomplete.

### What this wave improves in the application
After Wave 4, the application should:
- cover a materially broader commercial panel surface
- have stronger phenotype and regression scaffolding
- expose customer-facing history/report/account surfaces beyond upload/results only
- be closer to credible minimum-market readiness

#### Historical lineage: KB-S55 — Biomarker Ingestion Batch 5
Purpose: continue governed breadth completion.
Batch identification note: at the time of authoring, the sprint prompt author must identify the target source batch from available ungated research artefacts in `knowledge_bus/research/`. Batch readiness must be confirmed against the current KB SOP before the prompt is written. No ingestion sprint may be authored against a batch that has not been confirmed as pipeline-ready.

#### Historical lineage: KB-S56 — Renal Research Promotion + Renal WHY Completion
Purpose: complete the renal pathway after its prerequisite research promotion.
Strategic value: renal remains structurally incomplete and should not be left outside governed truth.

#### Historical lineage: KB-S57 — Biomarker Ingestion Batch 6 + SSOT Coverage Check
Purpose: finish the planned breadth programme and verify canonical integrity.
Batch identification note: at the time of authoring, the sprint prompt author must identify the target source batch from available ungated research artefacts in `knowledge_bus/research/`. Batch readiness must be confirmed against the current KB SOP before the prompt is written. No ingestion sprint may be authored against a batch that has not been confirmed as pipeline-ready.

#### Historical lineage: KB-S58 — Phenotype / Fixture / Regression Expansion
Purpose: strengthen phenotype truth, fixtures, and regression coverage across the enlarged estate.
Strategic value: this is a key anti-drift wave because it prevents the platform from becoming a broad but weakly testable engine.

#### FE-PAGES — Dashboard, reports, analysis detail, continuity surfaces
Purpose:
- implement the currently incomplete customer-facing product pages
- make history, report retrieval, and detailed analysis genuinely usable
- move the app beyond upload/results into a persistent product

#### FE-ACCOUNT — Profile, settings, and My Account management
Purpose:
- implement account/profile/settings capability
- support the minimum account-management experience required for launch

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
Purpose: formalise objective inputs such as waist, BP, height, weight, BMI-related measures, and any analytically relevant age/sex application gaps that remain unresolved in Layer B.

#### BE-S0b — Subjective / Behavioural Context Hardening
Purpose: formalise governed use of smoking, alcohol, exercise, sleep, stress, and medication caveats.

---

## Wave 6 — Narrative, Launch Integration, and Market Readiness

### Purpose of this wave
Wave 6 should be the final integration and launch gate.
It should not be the place where the entire product shell is built from scratch.

### Why this wave exists
Narrative must be the last layer, not the first.
Likewise, launch-readiness work should harden and integrate the completed platform and product shell, not compensate for work deferred too late.

### What this wave improves in the application
After Wave 6, the application should:
- translate structured truth into readable outputs
- present a coherent authenticated product experience
- satisfy launch-readiness expectations for the intended markets
- be ready for first commercial deployment

#### BE-S1 — LLM Narrative Production Enablement
Purpose: enable narrative translation on top of governed structured intelligence.
Strategic note: this governs and activates the existing narrative direction on top of deterministic truth; it is not a licence to move reasoning into Layer C.

#### FE-S2 — Narrative Presentation Layer
Purpose: render the narrative cleanly in the frontend.

#### FE-LAUNCH-INTEGRATION — Final product integration pass
Purpose:
- ensure auth, persistence, dashboard/history/report pages, account surfaces, and narrative work as one coherent product
- resolve remaining product-shell integration issues before launch

#### OPS-S1 — Launch readiness, privacy, compliance, CI/CD, and operational controls
Purpose:
- complete the privacy, security, deployment, CI/CD, and operational readiness work appropriate to the intended launch markets
- verify the controls needed for the intended launch geography and product model
- complete the operational and governance checklist required for first deployment

Strategic note: FE-LAUNCH-INTEGRATION and OPS-S1 both require dedicated scoping before prompt authoring. OPS-S1 must not be authored until the following are confirmed outside the sprint process: intended launch market or markets, data residency requirements, the operating model (B2C, B2B, or hybrid), and the minimum compliance framework applicable to health data in those markets. A cold sprint author should treat OPS-S1 as blocked until these inputs are explicitly provided.

---

## 14. How the roadmap should now be interpreted

The roadmap should no longer be read as though the platform is still at the very start of signal breadth construction.

It should be read as a Phase 1 completion plan in which:
- breadth has already advanced materially
- WHY depth is still too shallow relative to breadth
- phenotype and interaction maturity remain uneven
- renal remains structurally incomplete
- auth/persistence/product-shell work must start before the final launch wave
- context consumption is not yet fully governed
- narrative must remain last

This is the most important interpretation update from v1.4 to v1.5.

---

## 15. Why this sequence is strategically correct

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
10. build the commercial product shell in parallel rather than leaving it all to the final wave

---

## 16. What this plan is building by the end of Phase 1

By the end of this roadmap, HealthIQ should be much closer to:

- a broad deterministic metabolic reasoning engine
- a platform that can interpret realistic commercial blood panels, not just a narrow subset
- a governed WHY and root-cause system with much stronger explanatory depth
- a phenotype-aware interpretation engine rather than a bag of isolated signals
- an explicitly governed context-input layer combining biomarkers with key lifestyle, anthropometric, hemodynamic, and medication context
- a structurally coherent Layer C narrative capability
- a working authenticated customer product with persistence, history, account continuity, and deployable frontend surfaces
- a product that is commercially launchable for the intended Phase 1 markets
- a credible launch point for Phase 2 longitudinal and dataset-moat work

This is not the final company vision.
It is the first full platform-construction year and the first real commercial product.

---

## 17. What comes after this roadmap

### Phase 2 — Dataset moat
After the engine and first product are stronger and structurally complete:
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

### Longitudinal note
Phase 2 should not be treated as if its data model can be invented from zero after Phase 1.
Phase 1 does not need to deliver the full longitudinal layer, but it should avoid product and persistence decisions that create unnecessary redesign cost later.

---

## 18. Final strategic statement

This roadmap is not optimised for the fastest demo.

It is optimised for building the first full version of a deterministic metabolic platform safely, at pace, and without architectural dishonesty.

The guiding principle remains:

**Build breadth and depth together.**
**Formalise truth before narrative.**
**Build the product shell in time, not at the end.**
**Move fast, but never in a way that weakens the engine or fragments the build into trivial work.**
