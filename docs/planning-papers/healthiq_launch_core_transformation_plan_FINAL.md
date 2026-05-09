# HealthIQ AI — Launch-Core Transformation Plan v5

**Date:** 2026-05-06  
**Status:** Draft for team circulation  
**Purpose:** Define the next programme phase for moving HealthIQ AI from a partially assembled product into a bounded, credible, launch-core product that works end-to-end in the real world.

---

## Executive summary

HealthIQ has completed meaningful stabilisation work:

- the major engine trust bugs have been fixed
- the documentation estate is now steerable
- the engine has been verified as materially stronger than feared
- lead findings on AB/VR are real and governed
- runner-up handling exists
- IDL is live
- Sentinel Phase 1 is real

But the product is still not launch-grade.

The issue is no longer that the engine is hollow.  
The issue is that the product has been assembled, but not yet composed into a coherent, bounded launch product.

In particular:

- analytical depth is uneven below the lead finding
- the full results experience is not yet carrying the engine cleanly
- questionnaire/lifestyle input produces little visible user payoff
- medication/drug influence is not yet a visible, proven part of the product
- some critical trust/coherence protections are still immature

The next phase should therefore not be a random sequence of local fixes.  
It should be a deliberately bounded programme to prove the full end-to-end personalised pipeline on a launch-core slice.

---

## Core programme stance

This programme is intended to prove the full real-world pipeline on a bounded launch-core slice. It must not create demo-only logic or short-lived workaround architecture.

We are **not** building a fake MVP that only works for a narrow demo path.

We **are** building a bounded but real vertical slice of the final product architecture, so that:

- the mechanics are real
- the contracts are real
- the data flow is real
- the personalisation layer is real
- the narrative handoff is real
- the testing is real
- future work becomes expansion, not rebuild

That means every sprint in this phase must satisfy two tests:

1. Does it solve the bounded launch-core use case?
2. Is it built in the same architectural shape the real product will use later?

If the answer to the first is yes but the second is no, we should not do it.

This approach will be slower in the short run than shortcut-driven delivery. That is intentional. We are trading short-term speed for avoidance of rebuild, architectural drift, and false progress.

---

## What the launch-core slice must prove

The launch-core slice must prove that all major moving parts of a personalised health report work together:

- biomarkers fire the correct signals
- ranking/arbitration chooses a believable lead finding
- governed WHY appears where it should
- fallback appears where it should
- lifestyle inputs visibly influence output
- medication/drug category inputs visibly influence output
- Layer B produces the correct structured truth
- Layer C receives a governed payload and polishes rather than reinterprets
- the UX carries that truth coherently
- the same inputs reproduce the same outputs
- regression tests protect the proven slice

This is the threshold at which future work can begin to look like knowledge-expansion sprints rather than infrastructure-rescue sprints.

---

## What this phase is not

This phase is not intended to:

- expand WHY Wave 2 across the full signal estate
- broaden the questionnaire further
- ship Section 5 / IDL prematurely if it is not needed for the bounded launch product
- do a broad frontend redesign before the launch-core contract is settled
- build a large amount of temporary logic just to make a demo work
- over-optimise for AB/VR only while ignoring real-world extensibility

---

## Strategic principles

### 1. Build the real pipeline, not a veneer
Every asset built in this phase must be a valid component of the eventual full product.  
No throwaway demo logic. No one-off bypasses. No fake integrations.

### 2. Prove the bounded slice before expanding breadth
We should not continue widening the intelligence estate until the launch-core pipeline is proven end-to-end.

### 3. Keep the questionnaire minimal for proving
Human testing will be heavy. A long-form questionnaire is counterproductive during the proving phase.  
Use the minimum set of questions needed to prove the personalisation pipeline.

### 4. Personalisation must be visible
If users provide lifestyle and medication inputs, they must be able to see that those inputs influenced the report.

### 5. Future growth must be additive
The bounded slice must be built so future work is mainly:
- new signals
- new edge cases
- new hypothesis assets
- new medication classes
- broader questionnaire scope
- richer narrative depth

not structural rework.

### 6. Be explicit about launch-core choices
The plan must not leave critical choices implicit.  
Launch-core biology, launch-core frontend surface, mock-mode honesty, `insights[]` disposition, silent-WHY handling, and proving acceptance criteria must be decided before implementation begins.

---

## Pre-Sprint 1 — Launch-core decision gate

This is not an implementation sprint.  
It is a short decision and contract-lock phase that exists to prevent Sprint 2–5 from discovering fundamental scope questions under load.

### Time-box
Pre-Sprint 1 is hard-limited to **one calendar week**.  
If any item remains unresolved at the deadline, a default decision is recorded, ownership is assigned, and the gate closes. The programme does not remain open-ended at this stage.

### Decision authority
Pre-Sprint 1 requires a **single named decision authority** who can record binding defaults if consensus is not reached within the time-box.

Without this authority, the gate cannot function as intended. The decision authority should be agreed before the gate opens.

### Exit criteria
Pre-Sprint 1 is complete only when:

- all decision items below are documented
- each decision has a named owner
- each decision has a recorded outcome
- each decision is grounded in the relevant verification evidence
- proving acceptance criteria are translated into binary checks
- the gate is signed off and closed

### Default ownership model
Use the existing role split as the working ownership model unless leadership chooses otherwise:

- **Core engine owner:** biology slice, silent-WHY policy, medication-governance source, Layer B → Layer C boundary
- **Frontend owner:** launch-core surface, mock-mode honesty carriage, IDL consumer surfacing decision
- **QA/UAT owner:** acceptance criteria, smoke-test checkpoint, binary proving checks
- **Programme/docs owner:** `insights[]` disposition, gate record, decision log, sign-off pack

### Commercial filter
The launch-core biology slice and launch-core surface must be chosen not only for technical feasibility, but for how clearly they demonstrate HealthIQ’s value as specialist-grade interpretation infrastructure to a first commercial buyer.

When technically viable options exist, prefer the option that best demonstrates:
- cross-marker reasoning
- specialist-grade interpretation
- confidence and missing-data discipline
- visible differentiation from basic dashboard/report products

### Outputs that must be settled here

#### 1. Launch-core biology slice
Choose explicitly what biological slice is being proven in this phase.

**Recommended default:**  
Use the **smallest real launch-core lead-finding set supported by representative panel evidence**.

This is wider than a homocysteine-only demo slice, but narrower than “all common panel scenarios.” It keeps the proving slice real while preventing uncontrolled WHY expansion.

The decision must not stay abstract. It should state whether the bounded slice is:
- a narrower “homocysteine / methylation / cardiometabolic” proving slice
or
- a wider “common UK commercial panel lead-finding” slice

This decision controls the scope of Sprint 1 and prevents uncontrolled WHY expansion.

When choosing between technically viable slices, prefer the slice that best demonstrates commercially valuable interpretation depth on realistic buyer-relevant panels, rather than the slice that is merely easiest to implement.

**Evidence input:** verification ledger findings on lead signals and active findings.

#### 2. Launch-core frontend/report surface
Name the exact launch-core carriage surface for this phase, for example:
- primary hero + domain cards + clinician/PDF surface
- or another clearly bounded surface set

Do not leave this implicit.

**Evidence input:** verification ledger findings on which surfaces are already carrying meaningful truth.

#### 3. Medication proving scope
Medication must be included, but bounded.

The proving phase should select **one medication/drug category** to prove the modifier architecture rather than attempting broad medication coverage.

**Suggested default:**  
- **statins**

Reason:
- clinically understandable
- directly relevant to lipid interpretation
- commercially and medically plausible for launch-core testing

#### 4. Medication governance source
Decide where the governed truth for the chosen medication category lives.

This must answer explicitly:
- what artefact holds the modifier truth
- what schema governs it
- whether the chosen medication category already exists in usable governed form
- if not, whether creation of that governed asset is part of Sprint 1 or a prerequisite before Sprint 2 starts

This is the most likely operational blocker if left unresolved.

**Additional verification requirement:**  
Before Sprint 2 is authored, complete an explicit verification of the current medication/drug modifier path and record the result in the gate output. Sprint 2 must not be scoped on assumption alone.

#### 5. Silent-WHY handling policy
For active findings without governed WHY, decide explicitly whether launch-core will:
- suppress them from key user-visible ranking surfaces
- show them with honest governed fallback
- or add new WHY assets for them as part of launch-core hardening

This should be a conscious policy, not discovered later.

**Evidence input:** verification ledger findings on active findings without governed WHY.

#### 6. Legacy `insights[]` disposition
Decide whether the legacy `insights[]` array is:
- removed from the public launch-core path
- gated behind a feature flag
- or rebuilt from real structured data

This decision must happen before carriage work, not at the end.

**Recommended default:**  
Remove or gate `insights[]` behind a feature flag unless a strong reason emerges to retain it on the launch-core path.

**Evidence input:** verification ledger finding that `insights[]` is a generic placeholder surface.

#### 7. Mock-mode honesty decision
Decide what the user is told when runtime is `deterministic_mock`.

This should cover:
- whether that is visible to users
- where it is disclosed
- what wording is used

**Evidence input:** verification ledger findings on mock-mode honesty risk.

#### 8. Section 5 / IDL consumer-surfacing decision
IDL is already live in runtime. The question is not whether to “build IDL,” but whether the **already-live IDL** should be surfaced to consumers in the launch-core slice, or deferred to Phase 1.1.

Do not leave it half-in/half-out.

#### 9. Layer B → Layer C boundary rules
Define the high-level contract boundary now.

This must explicitly state:
- Layer C is confined to translation/polish of governed payloads
- Layer C must not perform analytical augmentation or reinterpretation
- which fields Layer C may polish
- which fields it must preserve exactly

This is already a settled governance principle and should be implemented, not rediscovered.

**Additional verification requirement:**  
Pre-Sprint 1 should include a quick verification of what Layer C currently does with its payload, so the gate closes on implementation reality as well as policy intent.

#### 10. Human proving acceptance criteria
Set pass/fail criteria now.

Minimum suggested proving bars:
- two contrasting questionnaire profiles on the same panel must change at least one user-visible field
- the alcohol/lifestyle bridge must surface in user-readable language when active
- the chosen medication category must change at least one user-visible field where relevant
- no placeholder `insights[]` surface remains active on the launch-core path
- no band ↔ headline polarity contradiction survives on any launch-core surface

These criteria should be translated into binary checks before the gate closes.

---

## Proposed next-phase sprint sequence

## Sprint 1 — Launch-core analytical hardening

**Purpose:** Strengthen the bounded launch-core analytical surface so that the most plausible lead findings on representative launch panels are credible, governed, and non-embarrassing.

### Outputs
- agreed launch-core lead signals strengthened
- governed WHY added or verified for those signals
- fallback behaviour made honest and useful where WHY is still absent
- clinician/root-cause surface populated for launch-core lead cases
- no silent omission on the chosen launch-core lead set

### Architectural rule
Only expand WHY for signals that are actually proven to emerge as lead findings on representative launch panels.

### Scope note
Sprint 1 scope is explicitly contingent on the Pre-Sprint 1 biology-slice decision. The team should not commit Sprint 1 capacity until the gate is closed.

### Non-goals
- full WHY Wave 2
- broad signal-estate expansion
- patching renal or other later-phase domains out of sequence

---

## Sprint 2 — Launch-core context integration

**Purpose:** Make lifestyle and the chosen bounded medication/drug category materially and visibly affect the launch-core analytical output.

### Outputs
- lifestyle modifier behaviour connected to the launch-core interpretation flow
- one bounded medication/drug category connected to the launch-core interpretation flow
- visible modifier logic governed and deterministic
- no raw technical bridge language on user-facing surfaces
- no “questionnaire theatre”

### What this sprint should solve
At present, the questionnaire is largely invisible in the output.  
This sprint makes the context layer visibly matter.

### Architectural rule
This must use the real context-modifier architecture that can later scale to more factors and categories.

### Important constraint
Lifestyle and medication are not symmetrical.
- lifestyle already has more machinery
- medication is likely less mature

So medication proving here is about **proving the architecture**, not broad coverage.

### Mandatory smoke-test gate
A lightweight human smoke-test runs at the **end of Sprint 2**.

Minimum smoke-test:
- run two contrasting questionnaire profiles on the AB panel
- confirm at least one user-visible field changes
- confirm the lifestyle bridge surfaces in human-readable language when active
- confirm no obvious contradiction appears on the chosen launch-core surface

If this smoke-test fails, Sprint 3 does not begin until the issue is corrected or formally re-scoped.

### Non-goals
- full behavioural rewriting of all signals
- broad drug database completion
- deep Phase 2 personalisation ambitions

---

## Sprint 3 — Layer B to Layer C implementation

**Purpose:** Formalise and implement the governed payload sent from analytical truth to narrative generation.

### Outputs
- one governed narrative payload/file for the launch-core slice
- contains lead finding, runner-up if relevant, WHY, missing data, confidence framing, context modifiers, actions, and evidence trail
- Layer C polish contract implemented
- deterministic fallback path remains safe when no LLM is active

### Contract rule
Sprint 3 must state explicitly:
- which payload fields Layer C may rewrite
- which payload fields Layer C must preserve byte-for-byte
- how reinterpretation is prevented or detected

### Why it matters
This is the sprint that makes the report feel composed rather than assembled.

### Architectural rule
The payload must be the real long-term Layer B → Layer C handoff shape, even if only a bounded subset of content is populated initially.

### Non-goals
- broad prose experimentation before the payload is locked
- ad hoc prompt stuffing
- one-off narrative bridges outside the governed payload

---

## Sprint 4 — Launch-core report carriage

**Purpose:** Ensure the UX carries the launch-core truth coherently.

### Outputs
- one coherent primary finding journey
- visible personalisation payoff from the proving questionnaire
- strong evidence trail
- no generic placeholder `insights[]`-style surface
- no contradiction between hero, overview, domain cards, and clinician/PDF surface
- visible honest handling of confidence, missing data, and fallbacks
- explicit handling of mock-mode honesty per the Pre-Sprint 1 decision

### Why it matters
The engine can already do more than the user currently experiences.  
This sprint makes the launch-core slice readable, credible, and coherent.

### Architectural rule
Use the real DTO/report contracts. Do not create alternative demo-only UI pathways.

### Non-goals
- broad future-state UI redesign
- expansion of non-core product sections
- speculative Phase 1.1/2 features

---

## Sprint 5 — Human proving sprint

**Purpose:** Test the full bounded launch-core pipeline repeatedly with real human review against pre-agreed pass/fail criteria.

### Outputs
- AB, VR, and additional representative panels tested
- multiple contrasting questionnaire profiles tested
- medication/drug modifier tested
- visible payoff confirmed
- contradictions, silence, thinness, and incoherence identified
- correction list generated for the bounded slice
- launch-core pass/fail judged against the criteria set in Pre-Sprint 1

### Named tester requirement
This sprint should identify the named human tester(s) or reviewer cohort in advance, so the evidence has traceable ownership.

### Why it matters
This is where we prove that the pipeline works in practice, not just in code.

### Architectural rule
Testing must target the real production path for the bounded slice.

### Non-goals
- broadening questionnaire scope during the proving phase
- trying to validate the entire eventual product in one go

---

## Sprint 6 — Protection of the proven slice

**Purpose:** Lock down the proven launch-core slice so future expansion does not break it.

### Outputs
- regression tests for the launch-core personalised pipeline
- coherence guard across sections
- persistence/replay protection for the slice
- questionnaire-visible-payoff test
- medication/lifestyle modifier tests
- removal, gating, or replacement of any placeholder legacy surfaces
- upgrade of current status-reporting placeholders into real guards where relevant

### Explicit protection target
This should include promoting known placeholder/status checks into real protections where they are needed for the launch-core path.

### Why it matters
Once the slice is proven, it must become a protected foundation.

### Architectural rule
Tests should protect real production contracts and behaviours, not narrow demo-only outputs.

### Non-goals
- full Sentinel Phase 2 breadth if not required to protect the launch-core slice
- broad testing redesign beyond what the slice needs right now

---

## What should happen after these sprints

If the six-sprint phase succeeds, the programme should change character.

At that point, future work should increasingly become:

- new signals
- new WHY assets
- new edge cases
- new combinations
- broader questionnaire scope
- richer medication/drug coverage
- stronger IDL/pattern depth
- improved testing breadth

In other words:
**knowledge-expansion sprints, not infrastructure-rescue sprints.**

---

## Specific strategic implications for the questionnaire

The questionnaire should now be treated as part of the launch-core personalisation model, not as a standalone UX deliverable.

### Launch-core stance
At this phase, the questionnaire should:
- be minimal
- be visibly influential
- be honest about what it affects
- be built on the real architecture
- be easy for humans to test repeatedly

### Not the goal yet
The goal is not to prove the final full questionnaire.  
The goal is to prove that personalisation works and is visible.

### Implication
If a five-question proving questionnaire works properly through the real pipeline, later questionnaire expansion becomes a knowledge/product expansion problem, not a pipeline problem.

---

## Specific strategic implications for medication/drug inputs

Medication/drug usage should be included in the proving slice.

### Why
Because if HealthIQ is to become a real-world personalised interpretation product, medication context cannot remain theoretical.

### Launch-core stance
We do not need a complete medication ontology at this phase.
We do need:
- a bounded set of medication/drug categories
- a real modifier path
- visible user-facing effect where appropriate

### Implication
This should be treated exactly like lifestyle:
a real but bounded modifier layer that can expand later without changing architectural shape.

---

## What we must not do next

- do not expand all of WHY Wave 2 immediately
- do not broaden the questionnaire before visible payoff exists
- do not patch the next visible defect without reference to the full launch-core pipeline
- do not build Section 5/IDL the wrong way just to make it appear present
- do not create demo-only shortcuts
- do not confuse a narrow proving set with a fake MVP veneer
- do not begin implementation before the launch-core scope gate is settled

---

## Immediate recommendation to the team

Approve the next phase as:

**Launch-core personalised pipeline completion**

with four programme priorities:

1. settle the launch-core scope gate
2. strengthen only the chosen launch-core analytical surface
3. prove visible personalisation and medication/lifestyle influence using a tiny proving questionnaire
4. lock the real Layer B → Layer C → UX chain before broadening intelligence

This phase should be judged successful only if, at the end:

- the bounded launch-core report is genuinely personalised
- the product visibly uses the core inputs it asks the user for
- the full pipeline works end-to-end
- and future work can mostly be additive rather than reconstructive
