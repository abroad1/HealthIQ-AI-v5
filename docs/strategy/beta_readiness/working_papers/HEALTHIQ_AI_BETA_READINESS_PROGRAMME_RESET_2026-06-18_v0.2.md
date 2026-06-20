# HealthIQ AI — Beta Readiness Programme Reset and Layer Strategy
Version: v0.2 team review draft  
Date: 18 June 2026  
Audience: HealthIQ AI leadership, architecture, product, engineering, research, safety and validation reviewers  
Status: Draft for team review  
Repository target path: `docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_PROGRAMME_RESET_2026-06-18.md`

---

## 1. Executive summary

HealthIQ AI is materially beyond a prototype concept.

The product already has an emerging deterministic intelligence architecture, governed Knowledge Bus promotion controls, runtime contracts, clinician-facing reporting structures, package and research assets, replay/versioning concepts, Sentinel validation material, and internal UAT evidence. The platform is no longer a blank canvas and should not be treated as one.

What has been proven is important:

- the platform has enough architecture and asset depth to justify a structured completion programme rather than a restart;
- the Layer A / Layer B / Layer C model is now clear enough to act as the governing architecture boundary;
- the product is not “an LLM writing a blood report,” but a deterministic medical intelligence platform with controlled downstream presentation;
- the estate contains reusable materials across systems taxonomy, scoring policy, Knowledge Bus packages, Pass 3 research, clinician reporting, explainer content, phenotype fixtures, replay policy and validation assets;
- recent UAT and audit work shows that the product can be improved through disciplined completion rather than reinvention.

However, HealthIQ AI is not yet beta-ready.

It is not beta-ready because the product still lacks complete launch-core domain coverage, subsystem depth remains uneven, Layer B explanation/prose coverage is partial, Layer C presentation/Gemini is not ready to be trusted as a downstream translator, UX trust issues remain, and the validation estate is not yet broad enough to support safe controlled external exposure.

So the programme objective is not “ship something quickly.”
The objective is:

**Complete the platform in the right order so that controlled beta, when it happens, rests on deterministic medical truth, provenance, auditability, and a coherent product surface rather than on UX polish or LLM improvisation.**

Before controlled beta, the product must complete:

- missing launch-core systems;
- minimum subsystem depth;
- Layer B WHY/prose/clinician substrate;
- safety/provenance/governance hardening;
- replay/auditability hardening;
- phenotype and edge-case beta validation;
- only then Layer C/Gemini presentation activation and UX redesign.

---

## 2. What we audited

This reset is based on a specific audited evidence base rather than on general intuition.

### 2.1 Cursor eight-block audit
Cursor produced a beta-readiness estate audit grounded in the live repository. It was strongest on filesystem inventory, current implementation status, available assets, and practical codebase maturity. It helped confirm that the current estate is richer than initially assumed and that the product should not be rebuilt from memory.

### 2.2 Claude eight-block audit
Claude produced a parallel eight-block audit. It was stronger on architectural interpretation, Layer B substrate requirements, replay/auditability concerns, prose/narrative constraints, and the risks of letting Gemini or presentation layers absorb medical reasoning.

### 2.3 Late-discovered documents
Additional late-discovered strategic and product documents materially changed the interpretation of the estate. These included the adopted Strategic Vision v1.5 document, frontend visualisation policy material, and related architecture papers. These documents strengthened the conclusion that systems-level, phenotype-aware, deterministic medical intelligence remains the correct strategic direction.

### 2.4 Layer Authority Index r2
A Layer Architecture Authority Index was created and revised to identify which documents actually govern the interpretation of Layers A, B and C. This helped prevent older or narrower documents from overriding the now-correct architecture reading.

### 2.5 Layer-Boundary Reconciliation ADR
A Layer Boundary Reconciliation ADR was then created, reviewed and merged. This was a critical step because it locked the corrected interpretation of the architecture and reduced the risk that future chats or sprints would slide back into “Gemini as the intelligence engine” or “frontend decides what matters” thinking.

### 2.6 UAT R1 and UAT R2
Internal UAT evidence was reviewed. UAT R1 surfaced serious results-page trust and product issues. UAT R2 corrected stale conclusions and showed that some previously high-severity issues had been resolved or downgraded. This matters because it means the product is improving, but it does not yet justify beta exposure.

### 2.7 Programme recommendation paper
A comparison and recommendation paper consolidated the Cursor and Claude findings into a multi-sprint programme recommendation. That paper concluded that the correct next move was not immediate implementation, but a structured beta-readiness programme beginning with mapping of missing launch-core build materials and Layer B prose/explainer substrate.

---

## 3. The architectural decision now locked

The most important architecture decision is now locked and should be treated as authoritative for roadmap planning.

### 3.1 Layer A = ingestion and canonical facts
Layer A owns:

- ingestion;
- parsing;
- canonicalisation;
- factual normalisation;
- unit/range preservation;
- lab-specific range preservation;
- clean structured factual input preparation.

Layer A must not:

- interpret medical meaning;
- activate signals;
- infer causality;
- score domains;
- rank findings;
- decide what should be surfaced.

### 3.2 Layer B = all medical intelligence
Layer B is the source of medical truth.

Layer B owns:

- biomarker interpretation;
- signal activation and suppression;
- hierarchy;
- primary concern logic;
- WHY/root-cause reasoning;
- evidence and counter-evidence;
- confidence/completeness handling;
- subsystem and system reasoning;
- phenotype mapping;
- surfacing decisions;
- clinician report content;
- deterministic boilerplate/explainer selection;
- safety boundaries;
- prohibited claims;
- provenance and traceability for what is said.

This means Layer B decides:
- what matters;
- why it matters;
- how strongly it is supported;
- what complicates the picture;
- what is safe to say;
- what the user and clinician should see.

### 3.3 Layer C = presentation / translation only
Layer C owns:
- wording;
- composition;
- arrangement;
- translation of governed Layer B outputs into a polished report experience.

Layer C may improve readability and user experience.
It may not:
- reason medically;
- activate/suppress signals;
- rank findings;
- inspect raw biomarkers outside governed Layer B payloads;
- create new claims;
- override Layer B.

### 3.4 Gemini
Gemini, if used, is an optional constrained Layer C component only.

It may be used later for wording/presentation improvement against a governed Layer B brief.
It is not the analytical engine, not the report brain, and not the medical reasoning layer.

This point is non-negotiable.

---

## 4. The eight beta-readiness blocks

The programme is organised around eight blocks.

### 4.1 Core systems
HealthIQ needs a complete and coherent launch-core systems model, not a loose set of observations. Missing or incomplete launch-core domains must be mapped and completed before beta.

### 4.2 Subsystems
The product must go beyond shallow top-level system summaries into meaningful subsystem depth. This is important both for medical coherence and for the educational “wow” value of the product.

### 4.3 Layer B intelligence / prose / clinician report
This is the true HealthIQ core. The product cannot rely on Gemini to improvise explanation. Layer B must own WHY, hierarchy, explainer selection, clinician report content, safe consumer prose, and the educational boilerplate assets that make the product feel rich and trustworthy.

### 4.4 Layer C presentation / Gemini
Layer C should remain presentation/translation only. Gemini, if activated later, belongs here only as a constrained wording/presentation tool. It should not be activated before Layer B is ready.

### 4.5 UX / results page
The results page and product journey matter, but should be built around stable Layer B outputs. UX redesign must follow stable architecture, not precede it.

### 4.6 Safety / provenance
The product must preserve research-to-runtime provenance, lab-range authority, controlled package promotion, non-diagnostic wording, and traceable claims.

### 4.7 Auditability / replay
Replayability, versioning, result compatibility, Sentinel/regression packs and deterministic reproducibility must be expanded before controlled beta.

### 4.8 Phenotype and beta validation test estate
Phenotype fixtures, edge cases, suppression/counter-evidence tests, and broader panel diversity must be expanded before external exposure.

---

## 5. Current estate summary

### 5.1 What already exists
The product already has:

- a strategic north star in Strategic Vision v1.5;
- a corrected Layer A/B/C architecture boundary;
- a systems taxonomy authority;
- Knowledge Bus governance and Pass 3 promotion controls;
- scoring policy;
- Knowledge Bus packages;
- Pass 3 research;
- NarrativePayloadV1;
- ClinicianReportV1;
- root-cause and explainer assets;
- replay/versioning concepts;
- Sentinel and validation materials;
- internal UAT evidence;
- results-page hardening work.

### 5.2 What is partial
The following are real, but not yet complete:

- launch-core system coverage;
- subsystem depth;
- Layer B prose/explainer substrate;
- clinician-report completeness;
- consumer education assets;
- Layer C/Gemini readiness;
- results-page trust and clarity;
- phenotype/edge-case validation;
- replay/auditability breadth.

### 5.3 What is missing
Still missing or not sufficiently complete for beta:

- mapped build materials for all missing launch-core domains;
- sufficiently rich Layer B boilerplate/explainer estate;
- enough validation to trust consumer-facing behaviour across representative cases;
- complete beta gates across safety, provenance, replay, phenotype and UX trust.

### 5.4 What must not be reinvented
The following must not be recreated from scratch unless mapping proves they are unusable:

- systems taxonomy;
- Wave 1 domain-card patterns;
- scoring policy;
- Knowledge Bus packages;
- Pass 3 research;
- NarrativePayloadV1;
- ClinicianReportV1;
- retail explainer registry;
- phenotype fixtures;
- replay/versioning logic;
- Sentinel packs.

### 5.5 Production-shaped vs launch-blocking
To reduce confusion:

**Production-shaped areas**
- layer boundary strategy;
- governance and promotion controls;
- strategic architecture direction;
- some runtime contracts and report structures;
- parts of results-page flow.

**Launch-blocking gaps**
- incomplete launch-core domains;
- uneven subsystem and phenotype depth;
- partial Layer B prose/explainer estate;
- insufficient auditability and beta validation breadth;
- incomplete product trust at the results layer;
- premature temptation to use Gemini before Layer B is complete.

---

## 6. Key reusable assets

### 6.1 Authority assets
These define what future sprints must respect:

- Strategic Vision v1.5;
- Layer Boundary Reconciliation ADR;
- User Health to Systems Map;
- Knowledge Bus SOP;
- Pass 3 Promotion Protocol;
- scoring policy;
- domain narrative and retail explainer boundary documents;
- primary concern and ambiguity policy.

### 6.2 Runtime assets
These are directly reusable build materials:

- Wave 1/domain card patterns;
- Knowledge Bus packages;
- Pass 3 research assets;
- NarrativePayloadV1;
- ClinicianReportV1;
- Interpretation Display Layer concepts;
- retail explainer registry;
- compiled card/evidence assets where present.

### 6.3 Validation and test assets
These must be expanded, not reinvented:

- phenotype fixtures;
- AB/VR/golden panels;
- ReplayManifest/replay policy;
- Sentinel packs;
- suppression tests;
- UAT R1/R2;
- launch-core replay and result-versioning policies.

---

## 7. Strategic delivery principles

### 7.1 No Gemini before Layer B is ready
Gemini must not be used to fill explanation gaps that Layer B has not yet solved deterministically.

### 7.2 No frontend inference
Frontend remains render-only. It may arrange, present and display governed outputs, but must not infer medical meaning or create new claims.

### 7.3 No fallback parser
Do not introduce fallback/dummy parsing behaviour to create an illusion of completeness.

### 7.4 No default/global ranges where lab ranges exist
Lab-provided ranges remain the interpretation authority where present.

### 7.5 Preserve provenance
Every clinically meaningful claim must remain traceable from research/policy/package to runtime output.

### 7.6 UX polish after architecture is stable
UX should become compelling after the architecture is stable enough to deserve it.

### 7.7 Outcome-based sprints, not fragmented micro-sprints
The programme should use meaningful, outcome-based sprint packages and only split when safety, governance or STOP gates require it.

---

## 8. The multi-sprint programme

### Phase 0 — Governance and evidence consolidation
Goal: make sure the team is using the correct authorities and the right evidence before building.

### Phase 1 — Missing launch-core systems
Goal: complete missing core systems and map the build materials for each one before implementation.

### Phase 2 — Layer B WHY / prose / clinician substrate
Goal: complete the deterministic explanation estate that makes HealthIQ educational, clinically credible and differentiating.

### Phase 3 — Safety / provenance / auditability
Goal: harden traceability, replayability, versioning, safety and research-to-output credibility.

### Phase 4 — Layer C presentation / Gemini
Goal: only after Layer B is sufficient, define and possibly test constrained Gemini/presentation behaviour.

### Phase 5 — UX / results redesign
Goal: redesign the results journey and report experience around stable Layer B outputs and user trust.

### Phase 6 — Beta validation and test estate
Goal: prove behaviour across phenotypes, panels, edge cases and user contexts before any controlled external beta.

This phase order should be preserved.
It is strategically correct and prevents UX-first or Gemini-first shortcuts.

---

## 9. First recommended work packages

### 9.1 P1-1 — Launch-core domain build-materials map
This should be first.

Purpose:
map exactly what already exists for the missing launch-core domains:

- blood / iron / oxygen;
- thyroid / energy regulation;
- kidney function.

Outputs:
- package/spec/signal map;
- biomarker-to-domain map;
- subsystem candidate map;
- prose/explainer asset map;
- tests/fixtures map;
- implementation recommendations.

This is a CONTENT sprint.
No runtime code.
No frontend changes.
No Gemini.
No implementation.

### 9.2 P2-1 — Layer B prose/explainer gap matrix
This should be second.

Purpose:
identify what Layer B prose/explainer assets already exist and what is missing for:

- biomarkers;
- pathways;
- systems;
- clinician report;
- consumer education;
- missing-marker and counter-evidence handling.

Outputs:
- gap matrix;
- coverage map;
- priorities for deterministic prose expansion.

### 9.3 P1-2 — First missing domain implementation package
This should come after P1-1 findings.

Purpose:
implement the first selected missing launch-core domain using mapped existing assets rather than reinventing logic from memory.

Selection should depend on:
- asset readiness;
- safety;
- testability;
- clarity of package/spec support.

---

## 10. What the team needs to review

### 10.1 Does the architecture feel right?
- Is the Layer A/B/C split now clear enough?
- Does everyone agree Layer B owns medical truth, WHY, hierarchy and surfacing?
- Does everyone agree Layer C/Gemini must not reason medically?

### 10.2 Are the sprint phases correctly ordered?
- Does the phase order feel right?
- Is there any reason to move Phase 2 ahead of Phase 1?
- Is any proposed phase too broad or too fragmented?

### 10.3 Are any known assets missing?
- Have we missed any major authority documents?
- Have we missed any major runtime or validation assets?

### 10.4 Are any dependencies wrong?
- Are there dependencies we have understated?
- Are any package/runtime/prose relationships misread?

### 10.5 Are any risks understated?
- Is the Gemini-overreach risk correctly stated?
- Are UX trust risks given enough weight?
- Are we underestimating subsystem depth or beta validation gaps?

### 10.6 Does this give enough clarity to proceed?
- Is this enough to begin P1-1 safely?
- What else would the team need before starting?

---

## 11. Decision required

The team is asked to decide:

1. whether to agree this as the working beta-readiness programme baseline;
2. whether to agree P1-1 as the first sprint package;
3. whether to agree that no Gemini/UX-first shortcut should be taken;
4. whether to agree that Layer B remains the source of analytical truth.

---

## 12. Final recommendation

HealthIQ AI should proceed with a structured beta-readiness programme based on the corrected layer model and the eight-block framework.

The platform is not starting again.
It is not ready for beta yet.
It is ready for a disciplined completion programme.

The correct immediate next step is:

**P1-1 — Launch-core domain build-materials map**

That sprint should preserve the estate, reduce reinvention risk, and provide the evidence needed to select the first safe implementation package.

The guiding architecture remains:

- Layer A = facts and canonicalisation
- Layer B = deterministic medical intelligence and WHY
- Layer C = presentation and translation only

That is the safest path to a product that is not merely polished, but medically credible, traceable, differentiated and genuinely beta-ready.
