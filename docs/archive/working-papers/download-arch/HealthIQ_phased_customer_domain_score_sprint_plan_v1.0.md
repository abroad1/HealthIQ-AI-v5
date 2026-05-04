# HealthIQ AI — Phased Customer Domain Score Sprint Plan v1.0

## Purpose

This document sets out a practical phased sprint plan for implementing the new customer-facing health-domain score model in HealthIQ AI.

It is based on:

- the agreed Strategy A launch direction
- the repo-grounded implementation blueprints
- the repo-grounded domain narrative contract work
- the decision to phase delivery around what the current codebase can credibly support first

This is a planning document, not a work package prompt.

---

## Executive summary

HealthIQ should not attempt a flat 6-domain launch immediately.

The strongest route is a phased rollout:

### Phase 1 — Launch the first 3 domains
1. Cardiovascular health
2. Blood sugar control
3. Liver health

### Phase 2 — Extend to the next 3 domains
4. Blood, iron & oxygen
5. Kidney function
6. Thyroid & energy regulation

### Phase 3 — Reassess second-wave domains
7. Silent inflammation
8. Hormone balance

This phased approach is preferred because:

- the first 3 domains already map most cleanly to the current repo
- score grounding is strongest there
- confidence logic is most tractable there
- narrative assembly is already largely supported
- the remaining 3 require more aggregation, scoring-policy work, or calibration cleanup

---

## Strategic principles

These principles apply throughout all phases.

### 1. Domain scores are a translation layer
They are not a replacement for:
- the clinician report
- the phenotype engine
- the scoring engine
- the root-cause layer

### 2. Consumer and clinical naming must remain separate
- dashboard → consumer labels
- clinician handout → clinical labels
- engine → internal phenotype/system constructs

### 3. No fake scoring
A domain score must only be shown where there is a medically grounded deterministic basis for it.

### 4. Confidence must be explicit
Every domain score must be paired with a confidence level and confidence explanation.

### 5. Narrative must be deterministic
Narrative for each domain must be assembled from:
- score band
- active signals
- IDL content
- Layer3 next steps
- missing-data structures
not from free-form generation.

### 6. Phase around codebase reality
The rollout order must follow what the repo already supports, not what sounds most elegant in theory.

---

## Agreed launch domains

### Launch-core six
1. Cardiovascular health
2. Blood sugar control
3. Liver health
4. Blood, iron & oxygen
5. Thyroid & energy regulation
6. Kidney function

### Second-wave only for now
7. Silent inflammation
8. Hormone balance

---

## Domain readiness summary

| Domain | Current readiness | Notes |
|---|---|---|
| Cardiovascular health | Strong | Best overall maturity across score rail, signals, WHY, and IDL |
| Blood sugar control | Strong | Cleanest first implementation path |
| Liver health | Moderate to strong | Scoring rail is narrower than the full domain story |
| Blood, iron & oxygen | Moderate | Strong biology, but needs cross-system aggregation |
| Kidney function | Moderate | MVP is possible, but eGFR treatment remains a medium-term need |
| Thyroid & energy regulation | Moderate | Strong signal/WHY layer, but missing first-class scoring rail |
| Silent inflammation | Provisional | Keep second-wave unless promoted later by evidence |
| Hormone balance | Provisional | Keep second-wave unless promoted later by evidence |

---

## Phase 1 — Launch the first 3 domains

## Goal

Ship the first customer-facing health-domain score layer for the 3 strongest domains:

1. Cardiovascular health
2. Blood sugar control
3. Liver health

These three should be implemented as the first true product translation layer above the deterministic engine.

---

## Phase 1 Sprint 1 — Domain score contract and assembler (Wave 1)

### Objective
Create the deterministic backend translation layer for the first three domains.

### Scope
- new domain score assembler
- new DTO contract surface for domain scores
- deterministic mapping from existing scoring / burden / signal / IDL outputs into domain objects

### Deliverables
- `consumer_domain_scores` (or equivalent) on the analysis output contract
- domain score object containing at minimum:
  - domain id
  - consumer label
  - clinical label
  - numeric score
  - band label
  - confidence tier
  - contributor sentence
  - consequence sentence
  - next-step sentence
  - missing markers / confidence-improvers
  - active signal ids
  - primary IDL record id

### Domains in scope
- Cardiovascular health
- Blood sugar control
- Liver health

### Backend design notes
- Cardiovascular health:
  - use current cardiovascular scoring rail
  - add bounded domain assembly
- Blood sugar control:
  - use current metabolic scoring rail
  - explicitly keep blood sugar domain separate from broader metabolic burden score
- Liver health:
  - use existing liver score as the base
  - apply bounded assembly / blending with hepatic capacity or burden context only if supported by agreed rule

### Out of scope
- frontend rendering
- thyroid scoring
- kidney eGFR policy redesign
- blood/iron/oxygen multi-system aggregation
- second-wave domains

### Risk
HIGH

### Why HIGH
- new backend contract
- new translation layer in analytics path
- domain score becomes a user-visible truth layer

---

## Phase 1 Sprint 2 — Domain confidence model (Wave 1)

### Objective
Build explicit confidence logic for the same 3 domains.

### Scope
For each of the three domains, define deterministic confidence from:
- coverage
- coherence
- specificity
- depth

### Deliverables
- confidence tier:
  - high
  - good
  - moderate
  - limited
- confidence explanation sentence
- missing markers / “what would improve confidence” list

### Domain-specific notes

#### Cardiovascular
Use:
- core lipid marker coverage
- derived ratio presence
- optional extended markers (ApoB, ApoA1, homocysteine, etc.) as confidence enhancers, not mandatory base requirements

#### Blood sugar
Use:
- glucose + HbA1c as base
- insulin / triglycerides / TyG-related paths as confidence enhancers
- explicit handling for prediabetes override logic

#### Liver
Requires extra care:
- cluster confidence is too narrow on its own
- domain-level hepatic confidence counter should be created from the broader hepatic marker pool

### Out of scope
- frontend rendering
- second-wave domains
- broad narrative redesign

### Risk
HIGH

---

## Phase 1 Sprint 3 — Domain narrative contract implementation (Wave 1)

### Objective
Implement the narrative assembly contract for the first 3 domains.

### Scope
For each domain card:
- score-band statement
- contributor sentence
- confidence sentence
- consequence sentence
- next-step sentence

### Sources of truth
Use deterministic sources only:
- system scores
- active signals
- IDL subtitle
- IDL `why_it_matters`
- Layer3 next steps
- root cause missing-data structures

### Key known gap to address
- cardiovascular lipid-dominant consequence line needs a clean governed path if current IDL remains thin for that pattern
- liver confidence requires domain-specific handling

### Deliverables
Fully assembled domain narrative payloads for the first 3 domains.

### Risk
HIGH

---

## Phase 1 Sprint 4 — Frontend domain card UX (Wave 1)

### Objective
Build the first customer-facing domain score cards in the UI.

### Scope
- domain card component(s)
- score display
- confidence badge
- short explainer
- expandable detail
- use of domain narrative contract from backend
- integration into results/dashboard experience

### UX elements
Each card should show:
- consumer label
- short explainer
- score /100
- band label
- confidence level
- one-line summary

Expanded:
- why this score
- what contributed most
- what this may mean over time
- what to do next
- what would improve confidence

### Out of scope
- clinician PDF relabeling
- biomarker card redesign
- second-wave domain UI

### Risk
STANDARD

---

## Phase 1 Sprint 5 — Wave 1 UAT and calibration review

### Objective
Test the first 3 domains end to end.

### Scope
- UX review
- score plausibility review
- confidence plausibility review
- narrative coherence review
- evidence traceability review
- customer interpretation sanity check

### Outputs
- launch/no-launch recommendation for Wave 1
- list of calibration or wording defects
- list of contract gaps discovered under real use

### Risk
STANDARD

---

## Phase 2 — Extend from 3 domains to 6 domains

## Goal

Add the next 3 domains only after the first 3 are working coherently:

4. Blood, iron & oxygen
5. Kidney function
6. Thyroid & energy regulation

---

## Phase 2 Sprint 6 — Blood, iron & oxygen aggregation design

### Objective
Design and implement the cross-system aggregation for Blood, iron & oxygen.

### Problem
This domain spans:
- CBC-related rails
- hematological burden/capacity
- iron-related markers/signals
- possibly nutritional rails depending on governed mapping

### Scope
- deterministic aggregation rules
- clear distinction between red-cell output and iron-store/transport context
- score grounding and confidence logic
- truthful narrative assembly

### Deliverables
- blood/iron/oxygen domain score logic
- confidence logic
- narrative contract
- DTO support

### Risk
HIGH

### Why HIGH
This is the most complex many-to-many translation problem in the launch-core set.

---

## Phase 2 Sprint 7 — Kidney function enhancement

### Objective
Implement Kidney function as a consumer domain cleanly.

### Base
- creatinine + urea score rail already exists

### Work
- domain score assembly
- confidence logic
- bounded use of eGFR context
- decide whether eGFR remains contextual in MVP or is upgraded into first-class scoring

### Deliverables
- kidney domain score
- kidney confidence
- kidney narrative contract
- expanded card support

### Risk
STANDARD to HIGH

### Important decision point
If eGFR must be first-class in score calibration, this may require governed scoring-engine work and should be treated as HIGH.

---

## Phase 2 Sprint 8 — Thyroid scoring rail and domain implementation

### Objective
Build Thyroid & energy regulation into a medically grounded scored domain.

### Current gap
The thyroid signal/WHY/IDL layer is stronger than the scoring infrastructure.
A clean 0–100 consumer domain likely requires a first-class thyroid scoring rail.

### Scope
- thyroid scoring-policy work
- thyroid cluster/schema updates if needed
- domain score assembly
- confidence logic
- narrative contract
- frontend support

### Deliverables
- thyroid score rail
- thyroid domain score
- thyroid confidence
- thyroid narrative contract

### Risk
HIGH

### Why HIGH
This likely touches governed SSOT/scoring policy and therefore is not just assembly work.

---

## Phase 2 Sprint 9 — Frontend extension from 3 to 6 domains

### Objective
Extend the UX from the first 3 domains to the full 6 launch-core domains.

### Scope
- new cards
- layout handling for 6 domains
- expand-card consistency
- confidence presentation consistency
- progressive disclosure review

### Risk
STANDARD

---

## Phase 2 Sprint 10 — Full 6-domain UAT and comparative product review

### Objective
Assess the 6-domain model as a whole.

### Scope
- does the score layer feel coherent?
- do the domains feel genuinely useful?
- do confidence levels feel credible?
- do narratives still feel grounded?
- are there domains that should still be withheld?

### Deliverables
- go/no-go recommendation on 6-domain release
- defects and calibration changes
- recommendation on whether second-wave domains should remain deferred

### Risk
STANDARD

---

## Phase 3 — Second-wave domains

## Goal

Reassess:
- Silent inflammation
- Hormone balance

Only proceed if:
- governed coverage is strong enough
- confidence logic is credible
- domain score semantics are not too fuzzy
- repo-grounded evidence supports promotion

---

## Phase 3 Sprint 11 — Silent inflammation feasibility review

### Objective
Determine whether Silent inflammation should become a real scored domain.

### Questions
- do we have enough direct markers?
- is the domain too broad?
- is it just a contextual layer rather than a top-level score?
- can it be made non-alarmist?

### Outcome
- promote to implementation
or
- keep as contextual layer only

### Risk
STANDARD research / HIGH if promoted

---

## Phase 3 Sprint 12 — Hormone balance feasibility review

### Objective
Determine whether Hormone balance should become a real scored domain.

### Questions
- are sex-specific paths strong enough?
- is coverage too variable?
- does the domain need sex/age-aware score behavior?
- can confidence be represented honestly?

### Outcome
- promote to implementation
or
- keep as contextual layer only

### Risk
STANDARD research / HIGH if promoted

---

## Non-code research work needed outside the sprint plan

These are important and should run alongside the codebase sprints.

## Research Track R1 — Medical calibration review

### Purpose
Ensure domain scores are medically defensible and not just product-friendly.

### Questions
- are the score-band meanings appropriate?
- are consequence sentences calibrated correctly?
- what claims are safe at each band?
- what confidence thresholds are credible?

### Output
- medical review memo on score calibration
- recommendations for:
  - score bands
  - confidence tiers
  - safe consequence framing

---

## Research Track R2 — Consumer comprehension testing

### Purpose
Test whether ordinary users understand:
- the six labels
- the score concept
- confidence
- expand-card content
- “what this means over time”

### Questions
- which labels confuse people?
- which explanations reassure vs alarm?
- do users understand confidence?
- do users understand that consumer labels differ from clinical ones?

### Output
- label comprehension report
- copy refinement suggestions
- UX framing recommendations

---

## Research Track R3 — Clinical handout credibility review

### Purpose
Protect clinician credibility while the consumer layer evolves.

### Questions
- are the clinical labels correct and restrained?
- is the handout still medically grounded?
- are consumer labels fully contained to dashboard/patient surfaces?
- does any new narrative drift into overstatement?

### Output
- clinician-facing review note
- list of forbidden crossovers between consumer and clinical layers

---

## Research Track R4 — Competitive product positioning review

### Purpose
Make sure the domain-score layer actually beats competitor UX rather than just adding more abstraction.

### Questions
- does the first screen now feel more reassuring than competitors?
- do score + confidence + explainer + next step feel distinctive?
- which competitor patterns should still be avoided?

### Output
- short competitor-differentiation memo
- UX recommendations for making the first 90 seconds stronger

---

## Research Track R5 — Narrative language governance review

### Purpose
Ensure all domain narratives stay:
- non-diagnostic
- calm
- useful
- medically credible
- not “wellness fluff”

### Questions
- which phrases should be banned?
- what level of directness is appropriate?
- how do we balance reassurance and truth?
- how should “what this may mean over time” be written?

### Output
- narrative style and safety rules
- approved / disallowed wording list

---

## Future roadmap after domain-score rollout

Once the domain score layer is working, future sprints may include:

1. domain trends over time
2. domain confidence change over time
3. score-to-action prioritisation
4. domain-specific PDF summaries
5. domain-aware results hero redesign
6. richer biomarker explainers linked to domain context
7. symptom-to-domain bridging
8. second-wave domains if justified

These should not be mixed into the first implementation wave.

---

## Recommended sequencing summary

### Build first
1. Wave 1 domain score assembler
2. Wave 1 confidence model
3. Wave 1 narrative contract implementation
4. Wave 1 frontend domain cards
5. Wave 1 UAT

### Build second
6. Blood, iron & oxygen aggregation
7. Kidney domain enhancement
8. Thyroid scoring/domain implementation
9. 6-domain frontend extension
10. 6-domain UAT

### Reassess later
11. Silent inflammation feasibility
12. Hormone balance feasibility

### Run in parallel outside code
- medical calibration
- consumer comprehension
- clinician credibility
- competitor positioning
- narrative governance

---

## Practical recommendation

If you want the strongest, lowest-risk starting point:

### Immediate implementation target
- Blood sugar control
- Cardiovascular health
- Liver health

### Immediate non-code parallel research
- medical calibration
- consumer comprehension
- narrative governance

That gives you the best chance of producing a genuinely improved first product layer without overextending the architecture.

---

## Working conclusion

HealthIQ should now move from concept work to phased implementation.

The right next move is not another broad reset.
It is a disciplined delivery sequence built around the strongest supported domains first, with explicit confidence, deterministic narrative, and parallel non-code research to keep the product medically grounded and commercially legible.
