---
work_id: N-5
branch: feature/n-5-pathway-explainer-asset-pack-v1
risk_level: STANDARD
execution_model: TWO_PHASE_START_FINISH
change_type: CONTENT
---

# N-5 — Pathway explainer asset pack v1

## Objective

Create the first governed pathway-grade explainer assets that the future deterministic narrative compiler will consume for benchmark-style system biology interpretation.

This is a CONTENT sprint.
It is not a frontend sprint.
It is not a compiler implementation sprint.
Do not modify backend analytical logic unless a tiny loader/registry touch is strictly required and justified.
Do not widen into narrative assembly.

The purpose of N-5 is to author and govern the reusable explanatory assets needed to support the benchmark narrative at pathway level, starting with the two highest-priority domains:
- methylation / one-carbon / homocysteine handling
- lipid transport / cholesterol handling

---

## Strategic context already settled

The following are already decided and are not open for reinterpretation in this sprint:

- The benchmark narrative is locked.
- The merged reverse-engineering matrix is locked.
- The narrative compiler architecture is locked.
- N-3 has closed the longitudinal raw-value contract gap.
- N-4 has created the first lifestyle interpretation bridge assets.
- One of the major remaining deterministic gaps is the absence of governed pathway-grade explainer assets.
- N-5 exists to create those governed explainer assets before N-6 and N-8.

Your job is to create the first high-quality governed pathway explainer pack that later compiler work can consume.

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

5. Relevant current runtime and authority files, at minimum:
- `knowledge_bus/interpretation_display_layer_v1/idl_records_v1.yaml`
- `knowledge_bus/phenotypes/phenotype_map_v1.yaml`
- relevant homocysteine / macrocytosis / lipid transport packages and hypotheses
- `backend/ssot/retail_explainer_v1/registry.yaml`
- any current explainer-bearing asset paths you determine are relevant

---

## Core problem this sprint must solve

HealthIQ currently has:
- signals
- hypotheses
- rankings
- some short “why it matters” strings

But it does not yet have governed pathway-level explanation assets that can tell the user, in medically disciplined and reusable prose:
- what a pathway/system does
- how the body uses it
- why the relevant markers belong together
- why the pattern matters beyond a single number

This sprint must create those assets in a governed form that later deterministic compiler work can consume.

---

## Required outcome

Deliver a bounded CONTENT implementation that:

1. defines the correct governed home for pathway explainers
2. authors the first v1 pathway explainer assets for the two benchmark-priority systems
3. keeps the prose medically serious, readable, and reusable
4. avoids overclaiming or diagnosis inflation
5. leaves the assets ready for later compiler consumption

---

## In scope

### 1. Preflight authority verification
Before writing assets, verify and cite:

- what current explainer-bearing assets exist
- whether any current field in IDL, phenotype map, or SSOT already partially serves this role
- what current asset locations are clearly too shallow for benchmark needs
- what the cleanest governed home is for reusable pathway explainers

You must confirm the correct authority location before authoring content.

### 2. Governed asset location decision
Choose and justify the governed home for these explainers.

Possible options include:
- extending an existing governed registry
- creating a new pathway explainer registry
- another bounded governed structure

Prefer clarity, reuse, and future compiler compatibility.

Do not bury long pathway prose in an inappropriate existing field if that would create muddled authority.

### 3. Methylation / one-carbon pathway explainer
Author a governed pathway explainer for the lead benchmark domain.

It should cover, in disciplined reusable terms:
- what the pathway does
- how homocysteine fits into it
- why remethylation / transsulfuration matter
- why red-cell maturation belongs nearby
- why this pathway can show friction even when serum availability looks improved
- why it matters beyond a single marker reading

This is not a full patient report.
It is a reusable governed asset.

### 4. Lipid transport / cholesterol handling explainer
Author a governed pathway explainer for the secondary benchmark domain.

It should cover, in disciplined reusable terms:
- what the lipid transport system does
- why LDL/HDL/ApoB/triglycerides are part of one transport story
- why a single LDL number is not the whole architecture
- how protective and atherogenic features can coexist
- why the system matters beyond simplistic “high cholesterol” framing

Again, this is a reusable governed asset, not a full report section.

### 5. Asset structure and field design
The asset structure must make clear which parts are for later compiler use.

At minimum, the design should support clean compiler consumption of things like:
- pathway role / function
- system-in-action explanation
- why markers belong together
- why it matters beyond itself
- bounded uncertainty / interpretive caution where needed

Do not write one giant unstructured prose blob unless that is explicitly the cleanest governed design and you justify it.

### 6. Tests / validation if required
If the chosen asset location requires validation or schema coverage, add the minimum appropriate checks.

If no code/schema change is required because this is a docs-only governed content addition under an already-valid structure, say so clearly.

### 7. Short sprint note
Add a concise implementation note documenting:
- what asset location was chosen
- what explainers were added
- what future sprint this unblocks

---

## Out of scope

The following are explicitly out of scope:

- full narrative compilation
- frontend changes
- body-overview compiler work
- confidence/uncertainty compiler work
- monitoring criteria assets unless minimally required by the chosen schema
- new lifestyle bridge work
- new longitudinal work
- Gemini / LLM work

---

## Design rules

### Rule 1 — reusable, not bespoke report prose
These assets must support many future reports, not just the AB benchmark case.

### Rule 2 — medically disciplined explanation
Do not drift into fluffy wellness language, dramatic prose, or unsupported simplifications.

### Rule 3 — system biology, not diagnosis inflation
Explain the biology and interpretive logic without turning explanatory text into diagnostic claims.

### Rule 4 — governed authority clarity
Make it obvious where these explainers live and what owns them.

### Rule 5 — benchmark relevance first
Focus on the two highest-value domains needed by the benchmark before widening to more systems.

### Rule 6 — compiler-ready structure
Author the content in a form the later narrative compiler can consume cleanly.

---

## Expected implementation shape

The expected shape is:

1. inspect current explainer-bearing assets
2. decide the correct governed home
3. author the first pathway explainer assets
4. add minimal validation if needed
5. write a short sprint note

This must remain a targeted asset-authoring sprint, not a narrative assembly sprint.

---

## STOP conditions

STOP immediately and report if any of the following are true:

1. there is no clean governed home and architectural adjudication is needed first
2. the chosen asset location would blur authority with IDL, phenotype definitions, or frontend copy in an unsafe way
3. the prose needed would require unresolved interpretation-entity decisions first
4. schema/validation work needed is much larger than expected
5. touched-file scope expands materially beyond the intended governed-content layer

If blocked, report:
- the exact blocker
- the affected files
- the smallest safe remediation path
- whether N-5 should be split before continuing

---

## Success criteria

This sprint is successful only if:

1. the governed home for pathway explainers is clear
2. the methylation/one-carbon explainer exists
3. the lipid transport explainer exists
4. the assets are medically serious and reusable
5. later narrative compiler work is materially unblocked
6. the sprint remains bounded and does not become narrative assembly

---

## Deliverables

At finish, the sprint should leave behind:

- the new or extended governed explainer asset file(s)
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

- what current explainer assets were insufficient
- where the new pathway explainers now live
- what structure they use
- why that structure is suitable for later compiler consumption
- how this specifically unblocks later deterministic narrative work

Do not claim success merely because two prose entries were added.
Show that benchmark-critical pathway explanation is now governed and reusable.