# HealthIQ AI — Strategic Vision and Phase 1 Sprint Plan
*Version 1.5 — master strategic record for Phase 1*

> Final note: This version preserves the governing strategic spine of v1.4 while updating the document to reflect current platform maturity more honestly, making product intent clearer to a cold reader, restoring the missing operational rules from v1.4, and strengthening protection against drift into a weaker product, unnecessary architectural detours, or micro-sprint fragmentation.

---

## 0. Why this document exists

This is not just a sprint list.

It is the master strategic record for Phase 1 of HealthIQ AI.

Its purpose is to ensure that every team member, sprint author, reviewer, and future operator can answer five questions clearly:

1. What are we building?
2. Why are we building it in this sequence?
3. What does each wave add to the final platform?
4. What kinds of drift are unacceptable, even if they look productive in the short term?
5. What counts as Phase 1 completion rather than partial technical progress?

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
- end Phase 1 with a real deployable market-ready product, not merely a strong internal engine

This remains the governing strategic direction for Phase 1.

### 1.1 Governance infrastructure is part of the moat

HealthIQ’s moat is not only analytical depth.
It also includes the governance discipline used to preserve deterministic truth as the platform scales.

The Knowledge Bus, Automation Bus, validator authority, hardened sprint protocol, deterministic gate, and audit discipline are not incidental overhead.
They are part of how HealthIQ protects analytical integrity while continuing to expand the platform.

That governance layer should not be traded away for apparent speed.

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
- support a working customer-facing product experience
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
- context-aware deterministic interpretation

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

Phase 1 is complete only when HealthIQ has both:

1. a sufficiently complete deterministic metabolic engine, and
2. a real deployable market-ready product shell around that engine.

### 4.1 Analytical truth gate

Before HealthIQ can be treated as Phase 1 complete and ready for market deployment, the following analytical truth conditions must be substantially satisfied:

- WHY hypothesis coverage exists across the primary metabolic pathways the product claims to interpret
- renal interaction-map gaps are resolved sufficiently that renal output is not structurally incomplete
- phenotype fixtures and regression assets are strong enough to support governed pathway and phenotype interpretation
- governed context inputs are analytically consumed, not merely collected
- no known determinism or structural-truth defects remain that materially weaken the credibility of the analytical engine

### 4.2 Product readiness gate

Phase 1 must also culminate in a genuine launchable product, including:

- a working frontend product experience
- authenticated customer access
- a My Account / customer-account management layer
- governed Layer C narrative translation operating on structured truth
- privacy, security, and data-governance readiness appropriate to the intended launch markets
- operational deployment readiness for live use

This means Phase 1 is **not** complete when the engine alone is strong.
It is complete when the engine is strong **and** embodied in a real product that can be deployed credibly to market.

### 4.3 What Phase 1 should be able to do

By the end of this Phase 1 roadmap, HealthIQ should be materially closer to a platform that can:

- interpret a realistic commercial blood panel deterministically
- emit non-contradictory biomarker and system-level outputs
- map users to one or more overlapping metabolic phenotypes
- explain key states with structured WHY reasoning
- use governed context inputs in a controlled and auditable way
- produce a coherent clinician-grade structured report
- support safe downstream narrative translation
- provide a deployable customer-facing experience around that analytical core

This is the bridge between:

- a blood interpretation tool
- a metabolic intelligence platform
- a future longitudinal dataset engine

---

## 5. Long-term company vision

The long-term company vision still has three strategic layers.

### Phase 1 — Engine moat
Build the best deterministic metabolic reasoning engine in the market and embody it in a deployable product.

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

### 6.1 Current baseline state snapshot

The platform has already moved materially beyond the maturity assumed in earlier strategy language.
To keep this document honest, the baseline should be read as a dated snapshot rather than as timeless truth.

| Metric | Baseline state as of 2026-04-03 |
|---|---|
| Latest completed sprint referenced by repo review | KB-S61 |
| Canonical biomarkers in SSOT | 103 |
| Knowledge Bus packages | 187 |
| Signals across packages | approximately 234 |
| WHY / hypothesis coverage | materially behind signal breadth |
| Pathways with zero active interaction edges | renal |
| Authentication status | non-functional / disabled stub |
| Narrative / LLM layer | infrastructure exists, not yet final governed production path |

These figures should be updated in future document revisions rather than assumed to remain current.

### 6.2 What is already materially true

Several important architectural and delivery foundations are already in place.

These include:
- clinician-report contract and renderer path
- intelligence-model and investigation-spec contract hardening
- Knowledge Bus governance alignment
- intervention-effects registry foundation
- deterministic Layer B / Layer C separation in runtime design
- live runtime signal, package, and test infrastructure well beyond the original narrow early baseline

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
- a usable deployable product shell

### 6.4 What remains materially incomplete

The most important incomplete areas now are:

1. the majority of live signals still do not produce WHY reasoning at runtime
2. phenotype and chain maturity remain uneven across pathways
3. renal remains structurally incomplete, with zero active interaction-map edges and therefore incomplete governed output truth
4. authentication is not yet functional and must be treated as a foundational product gap, not a cosmetic enhancement
5. context consumption is not yet governed strongly enough to count as a completed platform layer
6. structural truth is now less about absence of runtime wiring and more about correctness, coherence, and trusted semantics
7. narrative should still not be treated as a priority layer until these conditions are stronger
8. age and sex scoring adjustments are strategically important but are not yet fully realised as governed analytical truth in the live scoring path

### 6.5 Breadth is not the same as completion

It is important that future readers do not mistake increased signal or package counts for Phase 1 completion.

More signal breadth is valuable.
But breadth without enough WHY, interaction, phenotype, and context maturity risks producing a larger but still strategically weaker engine.

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
- age and biological sex where these materially change governed interpretation

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

### 6.8 Upstream research pipeline dependency

Upstream research generation now follows a governed multi-pass pipeline rather than an informal one-step authoring model.

All new investigation-spec and research-generation work should be understood as flowing through the governed research pipeline before any ingestion or WHY expansion sprint can treat those assets as ready for translation or promotion.

This is a core upstream dependency for both ingestion and WHY work.
Future operators should not assume that research assets are ready for product use merely because draft source material exists.

### 6.9 Documentation and authority note

The repository contains many historical planning, sprint, and architecture documents.
This roadmap is not intended to inventory all of them.

Future readers should use the documentation hierarchy and the current governance documents to determine which documents are authoritative and which are historical artifacts.

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

## 8. Sprint classification rules

These rules are part of the master strategic record because they are the operational interpretation of the governing principles.

### 8.1 Ingestion sprints
Default classification:
- change_type: CONTENT
- risk_level: STANDARD

These are suitable for faster sequential execution.

Exception:
If a batch requires new derived metrics, ratio-registry additions, or runtime logic changes, do not silently widen the ingestion sprint.
Instead:
- create a separate prerequisite sprint for the derived-metric/runtime addition
- classify that prerequisite sprint appropriately
- then proceed with the ingestion sprint afterward

### 8.2 WHY expansion sprints
Default classification:
- change_type: MIXED
- risk_level: HIGH

These sprints touch hypothesis assets, compiler-linked behavioural logic, confirmatory logic, and regression surfaces.

Each WHY sprint must have a mechanical prerequisite:
- clinical content must be authored first
- the prompt must include a STOP condition if the required hypothesis assets do not already exist

### 8.3 Structural completion sprints
Panel formalisation, runtime truth completion, renal completion, phenotype regression work, and major engine-coherence work are governed as backend or mixed architectural sprints, with risk level determined by the exact touched files.

### 8.4 Context-hardening sprints
Questionnaire, lifestyle, age/sex, and medication-context hardening work is governed as backend or mixed product-integration work.

Default intent:
- formalise which context fields are first-class inputs
- distinguish numeric/objective inputs from subjective/categorical inputs and govern consumption appropriately
- verify mapping from collected input to governed runtime consumption
- prevent silent drift between questionnaire capture, mapper logic, overlays, and user-facing narrative
- keep medication handling inside an explicitly bounded interpretation-caveat model unless a later sprint authorises deeper medication-aware reasoning

Risk rule:
- if touched-file scope stays inside mapper, questionnaire, registry, contract, or renderer-adjacent integration code, classification may remain below HIGH subject to hardening review
- if touched-file scope crosses into deterministic analytical runtime behaviour or control-plane authority, classification escalates accordingly

### 8.5 Narrative sprints
Narrative enablement must remain downstream of structured engine completeness.
No narrative sprint may introduce LLM reasoning into the analytical path.

### 8.6 Product-shell and launch-readiness sprints
Auth, customer account, compliance, privacy, deployment-readiness, and operational hardening sprints are productisation and launch-readiness work, not optional cosmetics.

They must be authored with explicit scope boundaries because these sprints can easily expand into vague catch-all operational work.

---

## 9. Anti-drift doctrine

The roadmap must explicitly defend against five failure modes.

### 9.1 Shallow blood-report drift
The platform must not degrade into a prettier consumer blood report with nicer explanation language.

### 9.2 Disconnected signal-engine drift
The platform must not become merely a larger validated catalogue of isolated biomarker signals.
Signals must increasingly contribute to pathway reasoning, phenotype interpretation, and coherent metabolic states.

### 9.3 Narrative-first drift
The platform must not sound intelligent before the deterministic substrate deserves translation.

### 9.4 Architecture-for-its-own-sake drift
The platform must not disappear into endless contract and governance work that is no longer materially improving product truth, scale, or defensibility.

### 9.5 Micro-sprint fragmentation drift
The platform must not be slowed by over-splitting large meaningful work into tiny procedural sprints that protect process more than product.

---

## 10. Pre-sprint and ingestion rules that remain active

### 10.1 One-off compatibility check rule

Before a major ingestion wave is authored, the platform must have a compatibility check across the target ingestion estate.

Required outputs include:
- which biomarker IDs are already in SSOT
- which derived metrics already exist in the ratio registry
- what missing derived metric prerequisites remain
- what schema or naming mismatches would block clean ingestion
- whether the translation path from JSON source material into canonical Knowledge Bus assets is clear

If this check has already been completed for the relevant estate, the result should be cited.
If it has not, the rule remains active.

### 10.2 Ingestion translation rule

Each ingestion batch consists of investigation-spec JSON or equivalent structured research source files.

Those assets are:
- structured research assets
- ingestion-friendly source material
- not yet canonical Knowledge Bus package artefacts

Therefore every ingestion sprint must explicitly include:

1. translation of source material into canonical KB artefacts
2. SSOT and registry compatibility confirmation
3. validator-passing package creation
4. fixture or synthetic-panel confirmation that the new signals fire as expected
5. promotion readiness evidence consistent with current KB governance

No sprint may assume that source JSON assets are directly promotable.

---

## 11. How to read the roadmap

The roadmap should be read as six connected build phases:

1. **Breadth waves** expand the signal surface so the engine can see more of real-world metabolism.
2. **WHY waves** deepen explanatory reasoning in the most important metabolic domains.
3. **Structural-truth waves** make outputs coherent, testable, and panel-truthful.
4. **Phenotype / fixture / regression waves** make multi-signal states stable enough to trust.
5. **Context-hardening waves** make non-biomarker inputs governable and meaningful.
6. **Product-shell / narrative / launch-readiness waves** translate governed truth into a deployable market-ready product safely.

This is not a list of technical chores.
It is the staged construction of a phenotype-aware deterministic metabolic platform.

---

## 12. The Phase 1 strategic build plan

### Important note on sprint numbering

Earlier roadmap versions described a large portion of Phase 1 using specific KB sprint IDs that now overlap with sprint numbers already used for different live repo work.

To prevent this document from becoming misleading, the Phase 1 build plan below is expressed primarily as **logical sprint groups and remaining strategic workstreams**, not as a rigid future mapping of all KB sprint IDs.

Where specific IDs are already stable and still useful, they may be referenced.
Where numbering has diverged from the earlier roadmap, the strategic workstream matters more than preserving outdated numeric labels.

### 12.1 Completed or materially advanced foundations before the remaining Phase 1 build

As of this version, the following have materially advanced:
- breadth ingestion well beyond the original six-batch framing
- Knowledge Bus governance alignment and validator-driven package promotion
- signal evaluator, scoring, arbitration, and deterministic assembly foundations
- Layer C-adjacent narrative infrastructure in bounded form
- clinician report contract and renderer path
- intervention-effects registry foundation
- bounded deterministic lifestyle-modifier infrastructure
- clustering and system-level structural foundations

The remaining Phase 1 plan should therefore be read as a **completion programme**, not as a greenfield build.

---

## Wave 1 — WHY depth completion in central metabolic domains

### Purpose of this wave
Strengthen WHY coverage where the live signal estate most obviously outruns runtime explanatory depth.

### Why this wave exists
The platform already has substantial breadth. The central strategic gap is that too many live signals still produce no WHY reasoning at runtime.

### What this wave improves in the product
After this wave, HealthIQ should:
- explain more of its most central metabolic states rather than merely flagging them
- reduce the mismatch between live signal breadth and root-cause reasoning
- strengthen the explanatory substrate required for phenotype credibility

### Representative workstreams

#### WHY-1 — Insulin resistance and systemic inflammation completion
Purpose: complete and harden WHY coverage in the most central, high-prevalence metabolic pathways.

#### WHY-2 — Lipid and vascular WHY expansion
Purpose: add structured WHY reasoning across the key lipid and vascular signals that currently remain under-explained at runtime.

#### WHY-3 — Hepatic and thyroid WHY completion
Purpose: complete WHY depth in the current partially covered hepatic and thyroid pathways.

---

## Wave 2 — WHY depth completion in iron, oxygen transport, and adjacent common domains

### Purpose of this wave
Complete WHY coverage in additional common, commercially visible, and biologically important domains.

### Why this wave exists
Iron, oxygen transport, and related domains are frequent in real-world panels and remain materially under-explained relative to breadth.

### What this wave improves in the product
After this wave, HealthIQ should:
- interpret more common real-world blood patterns with stronger explanatory depth
- improve phenotype realism in hematology and iron-regulation domains
- reduce user-visible gaps between findings and explanations

### Representative workstreams

#### WHY-4 — Iron / oxygen reasoning completion
Purpose: deepen iron deficiency, iron overload, ferritin, haemoglobin, and oxygen transport reasoning.

#### PHENO-1 — Iron overload phenotype completion
Purpose: add the missing iron-overload phenotype and associated fixtures/regression coverage.

---

## Wave 3 — Structural truth, governance debt closure, and engine coherence

### Purpose of this wave
Turn HealthIQ from a broadened engine into a trusted one by closing structural truth gaps, governance debt, and major coherence issues.

### Why this wave exists
A platform that knows more biology but produces contradictory, semantically weak, or incompletely governed outputs is not clinically or commercially credible.

### What this wave improves in the product
After this wave, the product should:
- have stronger acceptance truth for minimum commercial harnesses
- treat system-level and panel-level interpretation more coherently
- resolve known governance debts that would otherwise confuse future build work
- move closer to trustworthy phenotype and burden interpretation

### Representative workstreams

#### STRUCT-1 — AB/VR panel formalisation and acceptance truth
Purpose: formalise AB and VR as explicit acceptance truth rather than relying only on informal fixture meaning.

#### STRUCT-2 — Runtime structural truth and scoring correctness
Purpose: complete system-level coherence and close known analytical correctness gaps in scoring, bounds, and interpretation semantics.

#### GOV-1 — Knowledge Bus SOP update and known governance debt closure
Purpose: carry forward known KB SOP edits and other governance debt that should not remain undocumented or reverted.

#### GOV-2 — Research-pipeline acknowledgement and operator alignment
Purpose: ensure the governed three-pass research authoring pipeline is explicitly reflected in the Phase 1 operating model.

---

## Wave 4 — Renal unblock, phenotype truth, fixture expansion, and regression discipline

### Purpose of this wave
Complete the structurally incomplete parts of the platform that prevent trustworthy governed output in specific pathways and phenotypes.

### Why this wave exists
Renal remains structurally incomplete, phenotype maturity is uneven, and regression truth must catch up to breadth.

### What this wave improves in the product
After this wave, the product should:
- reduce structurally incomplete pathway behaviour
- increase phenotype reliability and testability
- strengthen regression discipline across the enlarged signal estate

### Representative workstreams

#### RENAL-1 — Renal interaction-map promotion and pathway completion
Purpose: unblock renal by promoting the missing governed interaction structure needed for coherent pathway output.

#### RENAL-2 — Renal WHY and phenotype validation completion
Purpose: complete renal explanatory and phenotype truth once structural prerequisites are in place.

#### PHENO-2 — Phenotype / fixture / regression expansion
Purpose: strengthen phenotype truth, fixtures, and regression coverage across the enlarged estate.

---

## Wave 5 — Context hardening before product translation

### Purpose of this wave
Make non-biomarker inputs meaningfully governable and analytically real.

### Why this wave exists
Context materially changes interpretation, but the engine should not consume it loosely or prematurely.

### What this wave improves in the product
After this wave, the product should:
- consume key objective and subjective context inputs in governed ways
- reduce the gap between collected user data and actual analytical use
- prepare the platform for safer and more meaningful translation, reporting, and customer use

### Representative workstreams

#### CONTEXT-1 — Objective context hardening
Purpose: formalise objective inputs such as waist, BP, height, weight, BMI-related measures, age, and biological sex where they materially affect governed interpretation.

#### CONTEXT-2 — Subjective / behavioural context hardening
Purpose: formalise governed use of smoking, alcohol, exercise, sleep, stress, and medication caveats.

---

## Wave 6 — Product shell, narrative, and launch readiness

### Purpose of this wave
Turn the strengthened engine into a real deployable customer-facing product without compromising deterministic integrity.

### Why this wave exists
Narrative, auth, account management, privacy, and operational readiness are required for market deployment, but they must remain downstream of analytical truth.

### What this wave improves in the product
After this wave, the product should:
- translate structured truth into readable outputs
- provide authenticated customer access
- give users account-level access and product continuity
- meet the operational and compliance baseline required for launch

### Representative workstreams

#### FE-S3 — Customer login and account management layer
Purpose: deliver authenticated customer access and My Account capabilities as a foundational product requirement.

**Important note:** this sprint requires a dedicated scoping exercise before prompt authoring. The current auth foundation is materially incomplete, so this sprint is a prerequisite-level product shell task, not a cosmetic enhancement.

#### BE-S1 — Governed Layer C narrative production enablement
Purpose: activate and govern the existing narrative infrastructure on top of structured deterministic truth.

**Important note:** this sprint should be read as governed enablement of existing narrative infrastructure, not creation of the narrative concept from zero.

#### FE-S2 — Narrative presentation layer
Purpose: render governed narrative cleanly in the frontend.

#### OPS-S1 — Launch readiness, privacy, security, and operational hardening
Purpose: deliver the compliance, data-governance, CI/CD, security, and deployment-readiness foundations appropriate to the intended launch markets.

**Important note:** this sprint requires a dedicated scoping exercise before prompt authoring. Privacy and compliance scope depends materially on the intended launch geography and operating model.

---

## 13. How the roadmap should now be interpreted

The roadmap should no longer be read as though the platform is still at the very start of signal breadth construction.

It should be read as a Phase 1 completion plan in which:
- breadth has already advanced materially
- WHY depth is still too shallow relative to breadth
- phenotype and interaction maturity remain uneven
- renal remains structurally incomplete
- context consumption is not yet fully governed
- auth and product-shell readiness remain incomplete
- narrative must remain downstream of truth

This is the most important interpretation update from v1.4 to v1.5.

---

## 14. Why this sequence is strategically correct

This sequence is designed to satisfy all of the following simultaneously:

1. preserve and extend breadth without pretending breadth alone is completion
2. deepen WHY without over-investing in a too-narrow signal surface
3. avoid a large signal estate with weak explanatory depth
4. avoid WHY work becoming detached from the live signal estate
5. formalise runtime and phenotype truth before narrative
6. explicitly harden context before allowing narrative to depend on it
7. keep phenotype direction alive without pretending phenotype maturity already exists everywhere
8. turn the engine into a real deployable product before claiming Phase 1 completion
9. preserve governance, auditability, and rollback discipline
10. move at pace without letting process fragment the product into trivial sprint slices

---

## 15. What this plan is building by the end of Phase 1

By the end of this roadmap, HealthIQ should be much closer to:

- a broad deterministic metabolic reasoning engine
- a platform that can interpret realistic commercial blood panels, not just a narrow subset
- a governed WHY and root-cause system with much stronger explanatory depth
- a phenotype-aware interpretation engine rather than a bag of isolated signals
- an explicitly governed context-input layer combining biomarkers with key lifestyle, anthropometric, hemodynamic, medication, age, and sex context where relevant
- a structurally coherent platform ready for narrative translation
- a deployable product with frontend experience, customer auth, account management, and launch-readiness foundations
- a credible launch point for Phase 2 longitudinal and dataset-moat work

This is not the final company vision.
It is the first full platform-construction year.

---

## 16. What comes after this roadmap

### Phase 2 — Dataset moat
After the engine is stronger and structurally complete:
- repeat-panel journeys
- intervention tracking
- trajectory summaries
- phenotype-density growth
- longitudinal identity continuity
- observational validation

**Important note:** Phase 2 depends on a longitudinally viable persistence and identity model. Phase 1 should not ignore that future requirement even if the full design belongs to the next phase.

### Phase 3 — Regulated workflow and strategic buyer readiness
After the dataset loop is live:
- documented risk controls
- clinical evaluation plan
- workflow insertion
- outcomes linkage
- strategic-buyer fit
- acquisition-grade defensibility

---

## 17. Final strategic statement

This roadmap is not optimised for the fastest demo.

It is optimised for building the first full version of a deterministic metabolic platform safely, at pace, and without architectural dishonesty.

The guiding principle remains:

**Build breadth and depth together.**
**Formalise truth before narrative.**
**Reach market with a real product, not just an engine.**
**Move fast, but never in a way that weakens the engine or fragments the build into trivial work.**
