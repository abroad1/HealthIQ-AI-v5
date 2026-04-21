---
work_id: N-6
branch: feature/n-6-functional-interpretation-and-confidence-assets
risk_level: STANDARD
execution_model: TWO_PHASE_START_FINISH
change_type: CONTENT
---

# N-6 — Functional interpretation and confidence assets

## Objective

Create the first governed functional-interpretation, confidence, clarification, and monitoring assets that the future deterministic narrative compiler will consume for benchmark-style reasoning.

This is a CONTENT sprint.
It is not a frontend sprint.
It is not a compiler implementation sprint.
Do not modify backend analytical logic unless a tiny validation/registry touch is strictly required and justified.
Do not widen into narrative assembly.

The purpose of N-6 is to author the reusable governed assets needed for benchmark-grade interpretive moves such as:
- “this is not simple persistent deficiency; it is incomplete pathway efficiency”
- “why this matters beyond itself”
- “confidence is moderate because…”
- “what would clarify the picture”
- “what improvement would look like”

---

## Strategic context already settled

The following are already decided and are not open for reinterpretation in this sprint:

- The benchmark narrative is locked.
- The merged reverse-engineering matrix is locked.
- The narrative compiler architecture is locked.
- N-3 closed the longitudinal raw-value contract gap.
- N-4 created the first lifestyle interpretation bridge assets.
- N-5 created pathway-grade explainer assets for the two benchmark-priority systems.
- One of the major remaining deterministic gaps is the absence of governed assets for functional reading, confidence framing, clarification logic, and monitoring criteria.
- N-6 exists to create those governed assets before N-8 compiler implementation.

Your job is to create the first high-quality governed asset pack for these interpretive moves.

---

## Required inputs

Treat the following as required inputs:

1. Benchmark target lock  
`docs/golden-narrative/AB_GOLD_STANDARD_NARRATIVE_TARGET_LOCK.md`

2. Merged reverse-engineering matrix  
`docs/golden-narrative/AB_GOLD_STANDARD_NARRATIVE_REVERSE_ENGINEERING_MERGED.md`

3. Final sprint strategy  
`docs/golden-narrative/HealthIQ_Deterministic_Narrative_Sprint_Strategy_FINAL.md`

4. Narrative compiler architecture  
`docs/golden-narrative/HealthIQ_Deterministic_Narrative_Compiler_Architecture_v1.md`

5. Relevant current authority files, at minimum:
- `knowledge_bus/root_cause/hypotheses/hcy_hypotheses_v1.yaml`
- relevant lipid transport / LDL hypotheses
- `knowledge_bus/registries/confirmatory_tests_v1.yaml`
- `knowledge_bus/pathway_explainers_v1/pathway_explainers_v1.yaml`
- `knowledge_bus/interpretation_display_layer_v1/idl_records_v1.yaml`
- any other current hypothesis/registry/explainer-bearing assets you determine are relevant

---

## Core problem this sprint must solve

HealthIQ already has:
- signals
- hypotheses
- confirmatory tests
- pathway explainers
- some short “why it matters” strings

But it does not yet have governed assets for the higher-order interpretive moves that make the benchmark report feel intelligent rather than descriptive.

This sprint must create those governed assets in reusable form so that later compiler work can produce disciplined outputs such as:
- functional reading
- confidence / limits
- clarification paths
- monitoring relevance
- “why this matters beyond itself”

without relying on ad hoc prose assembly.

---

## Required outcome

Deliver a bounded CONTENT implementation that:

1. defines the correct governed home for these new interpretive assets
2. authors the first v1 assets for the benchmark-priority domains
3. keeps the prose medically serious, reusable, and non-alarmist
4. avoids diagnosis inflation or causal overclaiming
5. leaves the assets ready for later narrative compiler consumption

---

## In scope

### 1. Preflight authority verification
Before writing assets, verify and cite:

- what current hypothesis/IDL/confirmatory-test fields already partially support these interpretive moves
- which current fields are too shallow for benchmark needs
- what the cleanest governed home is for reusable functional/confidence/monitoring assets
- whether these should extend an existing governed asset family or become a new pack

You must confirm the correct authority location before authoring content.

### 2. Governed asset location decision
Choose and justify the governed home for these assets.

Possible options include:
- extending an existing governed hypothesis family
- extending the new pathway explainer pack
- creating a new functional interpretation asset pack
- another bounded governed structure

Prefer clarity, reuse, and future compiler compatibility.

Do not blur:
- pathway explanation
- hypothesis evidence
- display-layer copy
- higher-order interpretive framing

### 3. One-carbon / methylation functional interpretation assets
Author governed assets for the lead benchmark domain covering, in reusable terms:

- functional reading
  - e.g. distinction between simple serum deficiency framing and incomplete pathway efficiency / clearance friction
- why this matters beyond itself
  - vascular context
  - blood-cell maturation context
  - interpretive relevance
- confidence framing
  - what supports the reading
  - what limits certainty
- clarification assets
  - what additional markers or conditions would sharpen the picture
- monitoring relevance
  - what improvement would look like
  - what persistence would mean

These should be reusable governed assets, not a bespoke report section.

### 4. Lipid transport functional interpretation assets
Author governed assets for the secondary benchmark domain covering, in reusable terms:

- functional reading
  - residual LDL-related exposure within a more protective transport context
- why this matters beyond itself
  - cumulative exposure
  - transport architecture context
- confidence framing
  - what makes this reading relatively stronger or weaker
- clarification assets
  - what wider context modifies interpretation
- monitoring relevance
  - what future drift would matter
  - what stable control would mean

Again, this is a reusable governed asset set, not a final assembled section.

### 5. Asset structure and field design
The structure must support later compiler consumption of things like:
- functional_reading
- why_beyond_itself
- confidence_grade_label
- confidence_limits
- clarification_paths
- monitoring_improvement_signals
- monitoring_persistence_signals

Do not write one large undifferentiated prose block unless you explicitly justify it.

### 6. Validation / structural checks if needed
If the chosen governed home needs validation or structural tests, add the minimum appropriate checks.

If no code/schema change is needed beyond a content asset plus lightweight structure test, say so clearly.

### 7. Short sprint note
Add a concise implementation note documenting:
- what asset location was chosen
- what interpretive assets were added
- what later sprint this unblocks

---

## Out of scope

The following are explicitly out of scope:

- narrative compiler implementation
- frontend changes
- body-overview compiler work
- broader pathway explainer work beyond the two benchmark domains
- new lifestyle bridge work
- new longitudinal contract work
- new phenotype/IDL entities unless absolutely required by the chosen asset structure
- Gemini / LLM work

---

## Design rules

### Rule 1 — reusable interpretive assets, not bespoke copy
These assets must support many future reports, not just the AB benchmark case.

### Rule 2 — medically disciplined framing
Do not drift into dramatic, fluffy, speculative, or overly certain language.

### Rule 3 — no diagnosis inflation
Explain interpretive meaning without making claims the panel alone cannot support.

### Rule 4 — clear authority separation
Do not muddle pathway explainers, root-cause evidence, and higher-order interpretive framing into one unsafe layer.

### Rule 5 — benchmark relevance first
Focus on the two benchmark-priority domains before widening to more systems.

### Rule 6 — compiler-ready structure
Author the content in a form the later narrative compiler can consume cleanly and selectively.

---

## Expected implementation shape

The expected shape is:

1. inspect current interpretive-bearing assets
2. decide the correct governed home
3. author the first functional/confidence/monitoring assets
4. add minimal validation if needed
5. write a short sprint note

This must remain a targeted asset-authoring sprint, not narrative assembly.

---

## STOP conditions

STOP immediately and report if any of the following are true:

1. there is no clean governed home and architectural adjudication is needed first
2. the chosen asset location would blur authority with pathway explainers, hypotheses, or display-layer copy in an unsafe way
3. the prose needed would require unresolved interpretation-entity decisions first
4. schema/validation work needed is much larger than expected
5. touched-file scope expands materially beyond the intended governed-content layer

If blocked, report:
- the exact blocker
- the affected files
- the smallest safe remediation path
- whether N-6 should be split before continuing

---

## Success criteria

This sprint is successful only if:

1. the governed home for functional interpretation/confidence assets is clear
2. the one-carbon / methylation asset set exists
3. the lipid transport asset set exists
4. the assets are medically serious, reusable, and non-alarmist
5. later narrative compiler work is materially unblocked
6. the sprint remains bounded and does not become narrative assembly

---

## Deliverables

At finish, the sprint should leave behind:

- the new or extended governed asset file(s)
- any minimal validation needed
- a short sprint note explaining:
  - what was added
  - where it lives
  - what future sprint it unblocks

Report back with:
- files touched
- governed asset location chosen
- how each of the two benchmark domains is now supported
- any remaining limitation later sprints must respect

---

## Evidence requirements

You must show, with exact file paths and grounded repo evidence:

- what current assets were insufficient
- where the new functional/confidence assets now live
- what structure they use
- why that structure is suitable for later compiler consumption
- how this specifically unblocks later deterministic narrative work

Do not claim success merely because some explanatory prose was added.
Show that benchmark-critical functional interpretation and confidence framing is now governed and reusable.