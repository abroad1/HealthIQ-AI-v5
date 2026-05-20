# HealthIQ AI — Core Scaffold Completion Sprint Plan  
## FINAL Compressed Version for Next Build Phase

## 1. Purpose

This plan defines the next major phase of HealthIQ AI development following the LC-S12A forensic architecture audit and subsequent roadmap reviews.

The purpose is not to rush towards launch, external users, or early revenue.

The purpose is to complete the core application scaffold so HealthIQ AI becomes a stable, governed medical-intelligence platform capable of absorbing future Knowledge Bus expansion safely, repeatedly and predictably.

The long-term product will require tens or hundreds of signal libraries, biomarker interactions, questionnaire modifiers, medication overlays, clinical caveats, drug-context rules, disease-context rules and edge-case interpretations.

We should not attempt to build all of that medical intelligence now.

Instead, we need to make sure the machinery that ingests, governs, scores, assembles, protects and surfaces that intelligence is structurally correct.

The target is:

```text
Architecture first.
Scaffold complete.
Then governed intelligence expansion.
Then product presentation redesign.
Then launch.
```

---

## 2. Strategic position

The LC-S12A architecture audit concluded that HealthIQ AI does not require a rebuild. The core analytical scaffold is real and worth continuing.

The deterministic analytical engine, Knowledge Bus pathway, unit governance, lab-derived reference range handling, root-cause hypothesis assets, Layer B / Layer C separation, replay manifesting and Automation/Sentinel workflow are genuine foundations.

However, the audit also identified that the application is not yet a complete platform scaffold.

The most important remaining gaps are:

- questionnaire/lifestyle intelligence is computed but not sufficiently surfaced
- scoring needs a proper direction-aware mechanism
- frontend/report coherence is not yet adequately guarded
- Knowledge Bus assets need a more systematic registration and surfacing framework
- root-cause / WHY registration needs to become more scalable
- persisted result replay is still too weak
- SSOT biomarker metadata is incomplete for future intelligence authoring
- orchestrator maintainability needs improving before the intelligence estate grows further

This compressed version reduces the scaffold programme from 13 separate sprints to 7 larger governed sprints.

The compression principle is:

```text
Combine investigation, documentation, guardrails and adjacent scaffold work where the evidence flow is shared.
Do not combine multiple unrelated HIGH-risk backend architecture changes in the same sprint.
```

---

## 3. Target state after scaffold completion

After this scaffold-completion programme, HealthIQ AI should have:

- deterministic Layer B analytical engine
- governed signal ingestion pathway
- governed root-cause / WHY ingestion pathway
- safe biomarker canonicalisation and unit handling
- lab-derived reference range preservation
- direction-aware biomarker scoring
- questionnaire and lifestyle propagation pathway
- structured Layer B → Layer C payload contract
- coherent frontend surfacing of governed assets
- persisted-result replay compatibility
- stale-result strategy
- Sentinel protection for escaped defects and product-level coherence
- scalable Knowledge Bus registration process
- maintainable orchestration phases
- completed SSOT metadata for active signal biomarkers
- documented developer/content-author workflow

The goal is that future sprints become mostly:

```text
Add / validate / govern new medical intelligence assets
```

rather than:

```text
Repair architecture so the assets can be used
```

---

## 4. Scaffold grade vs medical application grade

This plan is designed to build an A− scaffold.

It is not designed, by itself, to produce a fully A-grade medical application.

A scaffold is the platform machinery: how the app receives data, normalises it, scores it, fires signals, loads knowledge assets, compiles WHY, builds DTOs, renders the frontend, protects regressions and allows future intelligence to be added safely.

A medical application is the scaffold plus enough governed clinical intelligence to handle the common real-world cases users will bring to it.

Expected outcome after this plan:

```text
Scaffold architecture grade: A−
Medical application grade: B+
```

The medical application grade rises further only during the KB-WAVE phase, when the scaffold is populated with broader governed WHY coverage, combination-case reasoning, medication overlays and clinical edge-case intelligence.

The scaffold plan therefore creates the machinery for an A-grade medical intelligence platform. The KB-WAVE phase earns the medical depth.

This grade model is strategic shorthand, not an Automation Bus pass/fail criterion. Sprint acceptance is governed by the concrete gates, tests, audits and evidence defined below.

---

# 5. Global execution governance

## 5.1 Cross-sprint regression policy

Every scaffold sprint must begin by running a scaffold smoke pack that proves prior scaffold protections remain green before new changes begin.

At minimum, each sprint prompt must include:

```text
Run prior scaffold regression/Sentinel guards before implementation.
Do not proceed if a prior sprint guard is failing unless GPT explicitly classifies the failure as unrelated and authorises continuation.
```

The smoke pack should grow as the scaffold phase progresses.

Initial categories:

- LC-S8F / LC-S8G unit and display fidelity guards
- LC-S10B launch-core protection guards
- LC-S11A trust blocker guards
- LC-S13 lifestyle/coherence guards once created
- LC-S14 direction-aware scoring guards once created
- LC-S16/17/19 DTO/KB surfacing guards once created
- LC-S18 WHY registration guards once created
- LC-S20/22 persisted replay/render guards once created
- LC-S21/23/23B orchestrator/documentation/SSOT guards once created

Purpose:

```text
Each sprint protects the scaffold built by previous sprints before altering the next layer.
```

No sprint may silently break prior scaffold protections.

## 5.2 Sentinel and test-harness policy

Every scaffold sprint must explicitly decide whether it needs:

- ordinary unit tests
- backend regression tests
- frontend tests
- Playwright/render-level checks
- Sentinel pack entries
- DTO/schema compatibility tests
- fixture/fingerprint updates

Escaped defects and scaffold-defining behaviours must be promoted into Sentinel, not left as isolated tests.

Sentinel is required when a defect class is:

- user-facing
- previously escaped
- likely to recur
- cross-layer
- clinically trust-sensitive
- related to unit/display/reference-range safety
- related to internal token or placeholder leakage
- related to DTO compatibility or persisted replay
- related to Knowledge Bus asset surfacing

The sprint prompt must include a section titled:

```text
Sentinel / test harness obligations
```

and must state either:

```text
Sentinel update required
```

or:

```text
Sentinel update not required because...
```

A sprint is not complete if a known escaped-defect class has been fixed without a regression or Sentinel guard.

## 5.3 Rescoping authority

Cursor may not self-authorise material rescoping.

If a sprint investigation reveals that the implementation scope is materially different from the approved prompt, the sprint must STOP and return to GPT/human authority for one of:

- amended prompt on the same branch
- split sprint
- new Automation Bus work package
- explicit decision to defer part of the work

Material rescoping includes:

- changing sprint risk level
- moving from investigation to implementation when not authorised
- widening from one layer to multiple layers
- changing DTO contract shape
- changing backend scoring/signalling architecture
- changing root-cause registration mechanism
- changing frontend rendering contract
- discovering that the assumed internal computation path is broken
- discovering that more than a bounded minority of visible frontend content is unsupported/fallback-backed

---

# 6. Compressed Scaffold Completion Roadmap

## Sprint 1 — LC-S12B — Core Scaffold Definition, Gates and Execution Governance

### Risk

MEDIUM unless implementation files are touched. If this sprint edits control-plane scripts or runtime scaffold files, reclassify according to SOP.

### Purpose

Define what “core scaffold complete” means and establish the execution gates for the compressed scaffold programme.

This is not a launch-readiness sprint. It defines what must be true before HealthIQ AI can move from architecture-building mode into intelligence-ingestion mode.

### Scope

Define the target scaffold architecture and required platform capabilities:

- parsing / canonicalisation
- lab-range handling
- unit conversion
- scoring
- signal firing
- root-cause WHY compilation
- lifestyle modifier propagation
- domain/system assembly
- frontend rendering
- persisted replay
- Sentinel protection
- Knowledge Bus registration
- DTO contract
- stale-result handling
- documentation/onboarding standards

Define what is allowed to remain incomplete:

- full WHY coverage
- all signal libraries
- all drug interactions
- all disease-context permutations
- final frontend design
- full Gemini activation
- all complex combination-case intelligence

Define the future “knowledge ingestion sprint” template.

Define the difference between:

```text
architecture/scaffold defect
missing knowledge asset
frontend presentation issue
clinical content backlog
```

### Mandatory gates created by this sprint

#### Gate A — Scaffold definition approval

No later scaffold sprint may begin until LC-S12B has been reviewed and approved by:

- GPT Head of Product Architecture
- Claude Code audit
- Human product owner

The approved document becomes the controlling scaffold-definition reference for the remainder of the scaffold phase.

#### Gate B — Sprint 4 internal audit-before-implementation gate

Sprint 4 must complete and review the Knowledge Asset Frontend-Surface Audit before implementing or finalising the Knowledge Bus framework and payload-contract hardening elements.

If the audit materially changes the understanding of what is visible, governed, fallback-backed or unsupported, Sprint 4 must STOP and return to GPT/human authority for amended scope before implementation continues.

#### Gate C — Sprint 6 persisted replay fixture gate

Sprint 6 must establish a concrete persisted replay fixture strategy before finalising Sentinel Phase 2 render-level checks.

If Sprint 6 cannot establish a fixture contract, the Sentinel Phase 2 scope must be revised by GPT/human authority before implementation continues.

### Output

```text
docs/planning-papers/HealthIQ_AI_core_scaffold_completion_definition_v1.md
```

### Acceptance bar

The team can clearly distinguish a platform/scaffold defect from a missing knowledge asset.

The execution gates are written into the controlling scaffold definition and referenced by later Automation Bus prompts.

### What not to do

- Do not turn this into a launch plan.
- Do not define commercial readiness.
- Do not create theoretical standards we cannot test.
- Do not expand scope into product redesign.

---

## Sprint 2 — LC-S13 — Lifestyle Propagation, Coherence Guard and Narrative Language Audit

### Risk

HIGH

This sprint is unconditionally HIGH because it is expected to touch backend lifestyle/analytics behaviour, DTO or frontend surfacing, and Sentinel packs.

### Purpose

Prove that questionnaire-derived intelligence can travel from structured input to governed user-visible output, while also protecting the user-facing report from contradictions and misleading deterministic/mock-mode language.

This sprint combines the original LC-S13 and LC-S15 because both concern the Layer B → user-facing surface relationship and can share fixtures, frontend review and Sentinel guardrails.

### Current issue

The lifestyle/questionnaire layer is being computed internally, but the user gets little visible payoff.

However, previous audits found `lifestyle.confidence_adjustments` was uniformly `0.0` across contrasting lifestyle profiles. That means this may not be only a missing-output-wire problem. It may also be a broken or dormant computation path.

### Mandatory preflight

Before wiring anything to user-visible output, trace whether lifestyle confidence/modifier computation is actually producing non-zero or meaningful internal output for any profile.

Preflight questions:

- Are lifestyle modifiers computing internally?
- Are `confidence_adjustments` ever non-zero?
- Are lifestyle bridges firing correctly?
- Are lifestyle outputs present in DTO/meta fields?
- Are outputs absent from UI because they are unwired, or absent because computation is not happening?
- Are the rules gated by conditions that never trigger?

### STOP / split condition

If lifestyle modifiers and confidence adjustments are not computing meaningful internal outputs, Scope A must STOP and split into:

```text
LC-S13A — Lifestyle computation repair
LC-S13B — Lifestyle surface propagation
```

Scopes B and C do not disappear. Their handling is:

- Scope B — Coherence guard may proceed as a separate bounded LC-S13C work package if it does not depend on lifestyle computation.
- Scope C — Narrative language audit may proceed as part of LC-S13C if it is static/source-level and does not depend on lifestyle computation.
- LC-S13B must not begin until LC-S13A proves internal lifestyle computation is meaningful.
- Cursor may not decide this split independently; GPT/human authority must approve the split and amended prompt.

Do not proceed to lifestyle frontend surfacing until the internal computation path is proven.

### Scope A — Lifestyle propagation

- Trace questionnaire input → mapped lifestyle factors.
- Trace lifestyle factors → modifier engine.
- Trace modifier engine → analytical DTO.
- Trace bridge outputs → narrative/domain/action surfaces.
- Confirm whether `confidence_adjustments` are functioning.
- Repair dormant/broken computation path if bounded.
- Define where lifestyle context is allowed to appear.
- Define how lifestyle can modify:
  - confidence
  - explanation
  - caveats
  - next-step priority
  - but not biomarker truth
- Add tests using contrasting lifestyle profiles.
- Ensure lifestyle output is plain English, not raw internal bridge codes.

### Scope B — Coherence guard

Add tests/Sentinel guards for:

- hero finding agrees with body overview
- domain card band agrees with headline/consequence text
- “stable” cards do not carry warning copy unless explicitly contextualised
- “strong” or “needs review” cards have supporting evidence
- no domain claims active signals when none exist
- no “active concern” copy without active signal
- no raw signal IDs or governance tokens leak into user-facing prose

Known defect class to guard:

```text
Card says Stable / High confidence while headline says “not a simple all-clear”.
```

### Scope C — Narrative language audit

Audit deterministic/mock-mode prose for first-person possessive or AI-implying language.

Minimum search terms:

```text
"your measured"
"your cardiovascular"
"your results"
"your report"
"your blood"
"your panel"
"AI-personalised"
"personalised narrative"
```

The audit must distinguish:

- acceptable user-addressed explanatory language
- deterministic template language that overclaims personalisation
- internal governance/runtime labels leaking to users

Required outcome:

Either:

- reframe deterministic template language into neutral interpretive language, or
- add clear disclosure where required.

### Sentinel / test harness obligations

This sprint must add or update Sentinel defect classes for:

```text
lifestyle_visible_payoff_missing
lifestyle_bridge_internal_code_leakage
domain_band_headline_polarity_contradiction
domain_active_signal_false_claim
mock_mode_personalisation_overclaim
governance_label_user_visible_leakage
```

The Sentinel pack entries must point to deterministic regression tests, not merely status notes.

### Acceptance bar

The sprint must prove:

```text
Lifestyle intelligence is computed.
Lifestyle intelligence is surfaced.
Report coherence is guarded.
Deterministic/template narrative does not overclaim AI-style personalisation.
```

Same blood panel + different questionnaire profile must produce a governed, visible, explainable difference in output.

### What not to do

- Do not redesign the questionnaire.
- Do not introduce speculative lifestyle claims.
- Do not make lifestyle data override biomarkers.
- Do not add Gemini.
- Do not create generic wellness filler.
- Do not wire broken internal modifier values to the frontend.
- Do not redesign the frontend.
- Do not turn this into broad copywriting.

### Q-1 / Q-2 questionnaire dependency

Before this sprint starts, check whether Q-1/Q-2 questionnaire redesign work is still active.

If questionnaire input shape, field names, mapping or frontend collection flow are changing, LC-S13 must either:

- wait until Q-1/Q-2 is merged, or
- explicitly scope itself to backend modifier propagation using stable mapped DTO inputs only.

---

## Sprint 3 — LC-S14 — Direction-Aware Scoring Framework

### Risk

HIGH

### Purpose

Replace biomarker-specific scoring exceptions with a general directionality policy.

### Current issue

The LC-S11A ALT fix solved one false alarm, but did so through a targeted bypass. The underlying scoring scaffold still needs a proper way to represent biomarkers where high and low deviations have different clinical meaning.

### Scope

Create a governed directionality model for biomarker scoring.

Support:

- high-only concern
- low-only concern
- bidirectional concern
- protective-high
- protective-low
- informational-only deviation

Encode this in policy/SSOT rather than hardcoded rules.

Start with representative markers:

- ALT
- AST
- GGT
- ALP
- HDL
- ApoA1
- ferritin/transferrin where appropriate

Preserve lab-derived reference ranges.

Keep scoring and signal-firing distinct.

### Sentinel / test harness obligations

This sprint must add or update Sentinel defect classes for:

```text
direction_sensitive_marker_false_alarm
low_enzyme_false_alarm
protective_high_marker_penalised
hardcoded_biomarker_scoring_exception
scoring_signal_directionality_conflation
```

Regression tests must cover at minimum:

- low ALT is not critical/alarming
- high ALT remains concerning
- high ApoA1/HDL is not penalised as cardiovascular risk solely because high
- representative low-only / high-only / bidirectional marker behaviour
- no fallback to global/default reference ranges

### Acceptance bar

The architecture can safely represent clinically asymmetric markers without adding bespoke code for each biomarker.

### What not to do

- Do not redesign the whole scoring engine.
- Do not introduce global/default clinical ranges.
- Do not weaken genuinely concerning high values.
- Do not add one hardcoded exception per biomarker.
- Do not conflate scoring directionality with signal activation.

---

## Sprint 4 — LC-S16/17/19 — Knowledge Asset Frontend Surface, KB Framework and Payload Contract

### Risk

HIGH

This sprint is unconditionally HIGH because it is expected to inspect and likely affect DTO contracts, backend payload structure, frontend consumers and Knowledge Bus surfacing rules.

### Purpose

Understand what governed intelligence is actually visible to the user, formalise the Knowledge Bus lifecycle, and harden the Layer B → Layer C payload contract without breaking existing frontend consumers.

This sprint combines the original LC-S16, LC-S17 and LC-S19 because they are sequentially related:

```text
What does the user see?
What Knowledge Bus lifecycle is needed to govern it?
What DTO contract is required to carry it safely?
```

### Scope A — Knowledge Asset Frontend-Surface Audit

For representative outputs, map every visible frontend section to its source:

- hero / primary finding
- “what’s driving this”
- body overview
- domain cards
- expanded domain details
- pattern sections
- long-form WHY
- clinician/advanced sections
- biomarker dials
- next steps
- missing-data caveats
- trust/data-quality strip

For each visible content block, classify:

```text
governed Knowledge Bus asset
governed DTO field
scoring/domain boilerplate
generic fallback
frontend-derived display text
internal/debug/governance leakage
unsupported or contradictory text
```

Output:

```text
docs/audit-papers/LC-S16_knowledge_asset_frontend_surface_audit.md
```

### Internal gate: audit-before-implementation

The frontend-surface audit must be completed and reviewed before Knowledge Bus framework and payload-contract implementation begins.

If the audit reveals that visible frontend sections are materially more boilerplate-backed, fallback-backed or unsupported than expected, this sprint must STOP.

Material mismatch examples:

- a majority of visible content is generic fallback/boilerplate rather than governed assets
- frontend surfaces depend on fields not represented in the current DTO contract model
- major visible sections cannot be traced to stable DTO fields
- governed assets exist but are not reachable by the current frontend contract
- contract hardening would require breaking frontend consumers

If STOP is triggered, Cursor may not self-rescope. GPT/human authority must decide whether to:

- amend the Sprint 4 prompt
- split the sprint
- convert remaining work into a new Automation Bus package
- defer Scope B or C

### Scope B — Knowledge Bus Registration and Coverage Framework

Define signal package lifecycle:

- draft
- validated
- runtime-loaded
- signal-only
- WHY-enabled
- frontend-surfaced
- Sentinel-protected

Define required files for each package type:

- `signal_library.yaml`
- `research_brief.yaml`
- root-cause hypothesis YAML
- IDL/display metadata
- tests

Define how a signal moves into `_ROOT_CAUSE_TARGETS` or successor mechanism.

Define how orphaned/unused packages are detected.

Define asset coverage reporting.

Define “signal exists but WHY not yet available” behaviour.

Define how frontend-surface findings affect package lifecycle requirements.

### Enforcement requirement for Scope B

For each lifecycle control, explicitly classify whether it is:

```text
machine-enforced now
documented now, machine-enforced later
advisory only
```

At minimum, these should be machine-enforced or have a concrete validator backlog item:

- orphaned package detection
- package lifecycle state validity
- required file presence for WHY-enabled packages
- signal library schema validity
- root-cause hypothesis metadata validity
- asset coverage reporting for active signals

Documentation-only lifecycle rules must be explicitly labelled as documentation-only and must not be treated as gates.

### Scope C — Structured Payload Contract Hardening

Review all major DTO sections:

- biomarkers
- top findings
- root cause
- consumer domain scores
- clinician report
- narrative report
- IDL bundle
- actions/interventions
- lifestyle context
- replay manifest

Classify fields as:

- analytical truth
- explanatory evidence
- display metadata
- caveat
- polishable prose
- internal-only
- legacy/compatibility-only

Tasks:

- identify internal fields currently leaking into consumer payload
- identify frontend-consumed fields
- identify fields that should remain stable for compatibility
- identify fields that are legacy but still required
- ensure no frontend section depends on generic fallback where governed assets exist
- ensure payload supports future Gemini safely
- ensure frontend redesign can later happen without changing analytical logic

### Mandatory DTO constraint

Do not rename, restructure or remove DTO fields currently consumed by the frontend unless the corresponding frontend update is made and validated in the same sprint.

Field classification is governance work. It does not, by itself, require changing the serialisation shape.

Any change to DTO structure must include:

- frontend consumer search
- TypeScript type update
- runtime rendering validation
- regression test
- stale-result compatibility assessment

### Sentinel / test harness obligations

This sprint must add or update Sentinel defect classes for:

```text
frontend_section_not_backed_by_governed_source
knowledge_asset_not_surfaced_when_available
generic_fallback_used_when_governed_asset_exists
consumer_payload_internal_field_leakage
dto_frontend_contract_breakage
raw_signal_or_internal_id_visible
kb_lifecycle_required_file_missing
kb_orphan_package_unreported
```

Where Sentinel cannot yet execute a full render-level check, deterministic backend/DTO regression tests must be added and the limitation documented.

### Acceptance bar

The team can produce a clear map:

```text
visible frontend section → DTO field → runtime source → governed asset or fallback type
```

A future developer or content author can add a new governed signal package using a documented repeatable pathway.

The DTO is better understood and better governed without accidentally breaking existing frontend consumers.

Machine-enforced vs documentation-only KB lifecycle controls are explicitly distinguished.

### What not to do

- Do not re-audit the whole backend chain already covered in LC-S12A.
- Do not fix frontend design in this sprint.
- Do not add broad new Knowledge Bus content.
- Do not attempt to complete all WHY coverage.
- Do not redesign the UI.
- Do not introduce Gemini.
- Do not add new medical interpretation logic.
- Do not move clinical logic into the frontend.
- Do not rename/restructure DTO keys as “cleanup”.
- Do not remove consumed fields unless frontend and compatibility impact are handled in the same sprint.
- Do not let Cursor self-rescope if Scope A materially changes the problem.

---

## Sprint 5 — LC-S18 — Root Cause / WHY Registration Generalisation

### Risk

HIGH

### Purpose

Reduce manual wiring in the root-cause compiler so WHY expansion scales.

### Current issue

Adding governed WHY currently depends on a manually maintained registration table. That is manageable at the current scale but will not be efficient if the estate grows to hundreds of signal libraries.

The current root-cause compiler is one of the strongest parts of the application. Replacing manual registration with metadata-driven registration is the right long-term move, but it is high risk because a subtle registration bug could silently stop currently working WHY assets from loading.

### Scope

- Discover and fingerprint the current registered root-cause target set at sprint start.
- Investigate whether root-cause hypothesis assets can be auto-discovered by metadata.
- Define a standard hypothesis asset schema.
- Replace or supplement hardcoded registration with metadata-driven registration where safe.
- Preserve deterministic loading and validation.
- Preserve current behaviour for all existing registered WHY assets.
- Add tests proving new WHY assets can be added with minimal code changes.

### Mandatory guardrails

Before implementation:

- GPT architectural review of the proposed mechanism is required.
- Claude Code audit of the proposed migration path is required.
- Existing root-cause target output must be fingerprinted before change.
- New mechanism must fail loudly on malformed or missing metadata.
- No silent skip behaviour is allowed.

### Dynamic target-count rule

Do not hardcode the number of current root-cause targets in the acceptance criteria.

At sprint start, discover and fingerprint the current registered root-cause target set.

Acceptance is that every target present at sprint start produces identical WHY output after migration.

### Sentinel / test harness obligations

This sprint must add or update Sentinel defect classes for:

```text
root_cause_target_not_loaded
why_asset_silent_skip
metadata_malformed_not_failed
why_output_changed_after_registration_migration
new_why_asset_requires_backend_code
```

Regression tests must prove:

- every pre-existing registered target still loads
- every pre-existing target produces identical WHY output
- malformed metadata fails loudly
- a new metadata-compliant WHY asset can be registered without bespoke backend code, if that is the chosen design

### Acceptance bar

- All currently registered root-cause targets continue to load.
- Every target present at sprint start produces identical WHY output under the new mechanism as under the old.
- No silent skip is possible.
- Missing/malformed metadata fails loudly.
- Adding a new WHY-enabled signal becomes primarily asset work, not backend code work.

### What not to do

- Do not remove the old mechanism until the new one is proven.
- Do not silently ignore malformed assets.
- Do not change existing WHY output.
- Do not combine this with new WHY content expansion.
- Do not treat this as a low-risk refactor.

---

## Sprint 6 — LC-S20/22 — Persisted Replay, Stale-Result Strategy and Sentinel Phase 2 Scaffold

### Risk

HIGH if frontend e2e, persisted DTO handling, API contracts or Sentinel infrastructure are changed.

### Purpose

Ensure stored reports remain compatible and trustworthy after code changes, and extend Sentinel from backend escaped-defect tracking into product-level coherence and render-level protection.

This combines the original LC-S20 and LC-S22 because Sentinel Phase 2 depends on a persisted replay fixture strategy.

### Scope A — Persisted replay and stale-result strategy

- Upgrade persisted-result replay from placeholder/status check to real compatibility check.
- Load stored analysis DTOs through the current schema/renderer path.
- Confirm core fields remain readable:
  - analysis_id
  - biomarkers
  - consumer_domain_scores
  - clinician_report_v1
  - narrative_report_v1
  - interpretation_display_layer_v1
  - replay manifest
- Define stale-result handling:
  - when old analyses remain valid
  - when old analyses require regeneration
  - when UI should warn that an analysis was generated under an older engine version
- Decide whether analysis results should be immutable historical artefacts or regeneratable reports.

### Gate inside this sprint

Sentinel Phase 2 render-level checks must not be finalised until the persisted replay fixture strategy exists.

If a concrete persisted replay fixture contract cannot be established, the Sprint 6 prompt must be amended by GPT/human authority before Sentinel Phase 2 implementation continues.

### Scope B — Sentinel Phase 2 scaffold

Add render-level and contract-level smoke checks for:

- page renders
- lead finding visible
- domain cards present
- no placeholder text
- no raw internal tokens
- no unguarded governance labels
- correct display units/labels
- DTO schema compatibility
- Knowledge Bus asset surfacing
- frontend section presence
- persisted result compatibility

### Sentinel / test harness obligations

This sprint must add or update Sentinel defect classes for:

```text
persisted_result_schema_incompatible
persisted_result_render_failure
stale_analysis_unmarked
results_page_missing_primary_finding
results_page_placeholder_text_visible
results_page_internal_token_visible
results_page_unit_display_regression
results_page_missing_domain_cards
```

The Sentinel pack must include at least one render-level or API-to-render smoke path, not just backend status checks.

### Acceptance bar

A report generated today remains renderable and interpretable after future code changes, or is clearly marked as stale/requiring regeneration.

Sentinel catches the class of defects currently requiring manual human page review.

### What not to do

- Do not attempt database migration unless required.
- Do not change analysis logic.
- Do not silently mutate historical results without policy.
- Do not create brittle pixel-perfect tests.
- Do not attempt exhaustive UI testing.
- Do not duplicate unit tests.
- Do not build broad visual regression testing yet.

---

## Sprint 7 — LC-S21/23/23B — Orchestrator Decomposition, Scaffold Documentation and SSOT Metadata

### Risk

HIGH

Change type: MIXED.

LC-S21 touches `backend/core/pipeline/` and is HIGH risk under SOP regardless of intent. Because this sprint combines BEHAVIOUR work with CONTENT work, BEHAVIOUR controls apply to the whole sprint unless the sprint is explicitly split.

### Purpose

Make the analytical pipeline maintainable before the knowledge estate grows, document the scaffold for future developers/content authors, and complete the minimum SSOT metadata required to support governed future WHY authoring.

This combines the original LC-S21, LC-S23 and LC-S23B because all three prepare the scaffold for scalable future intelligence expansion.

### Scope A — Orchestrator phase decomposition

Decompose orchestration into named phase modules:

- canonicalisation phase
- unit normalisation phase
- scoring phase
- signal evaluation phase
- root-cause phase
- IDL phase
- report assembly phase
- replay/audit phase

Preserve one high-level orchestration entry point.

Preserve behaviour exactly.

Add phase-level regression protection.

### Scope B — Scaffold-level documentation and developer onboarding

Create or update:

- architecture map:
  - ingestion
  - canonicalisation
  - units
  - scoring
  - signals
  - root cause
  - Knowledge Bus
  - DTO
  - frontend rendering
  - Sentinel
- guide: how to add a new signal package
- guide: how to add WHY coverage
- guide: how to add a lifestyle modifier
- guide: how to test a new intelligence asset
- guide: what must never be done
- guide: how to classify scaffold defect vs missing content asset

### Scope C — SSOT metadata completion for active signal biomarkers

Complete metadata for biomarkers that:

- already have active signal libraries
- are part of current root-cause targets
- are likely to be used in early KB-WAVE work
- are common commercial blood-test markers

Fields to review/complete where applicable:

- key risks when high
- key risks when low
- known modifiers
- clinical caveats
- relevant systems
- common confounders
- interpretation-direction notes
- signal/WHY relevance

### Scope split rule

If Scope A hits coupling problems, requires GPT review, or cannot proceed safely, it does not automatically block Scopes B and C.

At that point, the sprint must STOP and GPT/human authority must decide whether to:

- continue Scope B/C as a CONTENT-only split package
- pause all scopes
- complete documentation/metadata first and defer orchestrator decomposition
- create a new Automation Bus prompt for the remaining work

Cursor may not self-authorise continuing mixed-scope work after Scope A is blocked.

### LC-S23B priority tiers

#### Tier 1 — required for sprint completion unless split is authorised

- LDL
- HDL
- ApoB
- ApoA1
- total cholesterol
- triglycerides
- TSH
- Free T4
- ferritin
- transferrin
- CRP
- eGFR
- creatinine
- ALT
- AST
- GGT
- ALP
- homocysteine
- B12
- folate
- HbA1c

#### Tier 2 — complete if feasible or carry into KB-WAVE preparation

- glucose
- insulin
- cortisol
- creatine kinase
- additional sex hormone markers

### Standing documentation obligation

The architecture map and contributor guides produced here become standing documents.

Every future KB-WAVE sprint must include a documentation update step if it introduces or changes an architectural pattern.

Examples:

- new combination-case pattern
- new modifier class
- new medication overlay pattern
- new WHY registration pattern
- new DTO field category
- new Sentinel requirement

Documentation must remain aligned to actual runtime behaviour, not historical scaffold state.

### Sentinel / test harness obligations

This sprint must add or update Sentinel defect classes for:

```text
orchestrator_phase_output_changed
pipeline_phase_regression
scaffold_documentation_missing_for_new_pattern
active_signal_biomarker_missing_ssot_metadata
ssot_metadata_unreviewed_for_kb_wave_target
```

For the orchestrator decomposition, regression tests must prove unchanged behaviour before/after decomposition.

For SSOT metadata, tests or validators should check required metadata presence for Tier 1 biomarkers.

### Acceptance bar

- Pipeline phases become understandable and independently testable without changing output.
- A future developer/content author can understand the architecture without relying on chat history.
- Tier 1 active-signal biomarkers have sufficient SSOT metadata to support future governed WHY authoring.
- Documentation becomes a standing, maintained scaffold asset.

### What not to do

- Do not redesign the pipeline.
- Do not change scoring, signals or narrative behaviour.
- Do not combine with product/frontend redesign.
- Do not change output fingerprints except where intentionally restamped and justified.
- Do not write generic documentation.
- Do not document hoped-for architecture; document actual runtime architecture.
- Do not use SSOT metadata as runtime interpretation authority unless explicitly wired later.
- Do not introduce unreviewed clinical claims.
- Do not attempt all 100+ biomarkers in one sprint.
- Do not confuse metadata completion with full WHY asset creation.
- Do not substitute generic/global reference ranges for lab-derived ranges.
- Do not let blocked BEHAVIOUR work automatically block separable CONTENT work without GPT/human review.

---

# 7. Work moved out of scaffold phase

## Medication modifier pathway

Medication modifier pathway work is not part of the compressed scaffold phase.

Reason:

- lifestyle propagation has not yet been fully proven
- medication context is more complex than lifestyle context
- statin-specific behaviour already exists from previous work
- medication intelligence should use the proven modifier pattern later, not drive the pattern now

Medication work should sit in the later Knowledge Bus / intelligence expansion phase:

```text
KB-WAVE-7 — Medication interaction overlays
```

---

# 8. Future intelligence expansion phase

Once the scaffold is complete, future work can become governed intelligence ingestion.

Examples:

```text
KB-WAVE-1  — LDL / ApoB / lipid transport WHY expansion
KB-WAVE-2  — TSH / FT4 / thyroid axis WHY expansion
KB-WAVE-3  — Ferritin / transferrin / inflammation interaction
KB-WAVE-4  — eGFR / creatinine / renal filtration context
KB-WAVE-5  — Cortisol / stress-axis interpretation
KB-WAVE-6  — Creatine kinase / muscle injury / training context
KB-WAVE-7  — Medication interaction overlays
KB-WAVE-8  — Sex hormone interpretation
KB-WAVE-9  — Iron + inflammation combination cases
KB-WAVE-10 — Liver enzyme pattern intelligence
```

At that point, most sprints should be about:

- source evidence
- clinical rules
- signal thresholds
- caveats
- hypothesis assets
- interaction logic
- runtime validation
- frontend surfacing checks

rather than foundational platform repair.

Each KB-WAVE must update standing documentation if it introduces or changes an architectural pattern.

---

# 9. Final compressed sequence

```text
Sprint 1 — LC-S12B       — Core Scaffold Definition, Gates and Execution Governance
Sprint 2 — LC-S13        — Lifestyle Propagation, Coherence Guard and Narrative Language Audit [HIGH]
Sprint 3 — LC-S14        — Direction-Aware Scoring Framework [HIGH]
Sprint 4 — LC-S16/17/19  — Knowledge Asset Frontend Surface, KB Framework and Payload Contract [HIGH]
Sprint 5 — LC-S18        — Root Cause / WHY Registration Generalisation [HIGH]
Sprint 6 — LC-S20/22     — Persisted Replay, Stale-Result Strategy and Sentinel Phase 2 Scaffold
Sprint 7 — LC-S21/23/23B — Orchestrator Decomposition, Scaffold Documentation and SSOT Metadata [HIGH / MIXED]
```

Then:

```text
KB-WAVE-1+ — governed intelligence expansion by biomarker system, signal family, questionnaire modifier, medication context and clinical interaction pattern
```

---

# 10. Architectural principles for all future sprints

1. Do not polish weak logic.
2. Do not hide defects in frontend copy.
3. Do not expand Knowledge Bus breadth while core surfacing is broken.
4. Do not add Gemini to compensate for incoherent deterministic output.
5. Keep Layer B deterministic.
6. Keep frontend as renderer, not analyst.
7. Preserve lab-derived reference ranges.
8. Use policy-driven fixes over hardcoded exceptions.
9. Convert escaped defects into regression/Sentinel protections.
10. Separate scaffold defect from missing knowledge asset.
11. Treat coherence as platform integrity, not product polish.
12. Treat medication intelligence as later content/modifier expansion unless a core scaffold gap is proven.
13. Do not wire broken internal computation paths to user-facing surfaces.
14. Do not restructure DTO contracts casually.
15. Treat SSOT metadata as a prerequisite for governed content authoring.
16. Keep standing documentation current as the intelligence estate expands.
17. Any new architectural pattern introduced by a KB-WAVE must update the contributor guides.
18. Do not allow Cursor to self-authorise material sprint rescoping.
19. Run prior scaffold guards before beginning the next scaffold sprint.
20. Treat compressed sprints as governed grouped work packages, not permission for broad uncontrolled implementation.

---

# 11. Expected grade after scaffold completion

This plan should not be judged by whether HealthIQ AI is ready to sell.

It should be judged by whether the core machine is complete enough that new medical intelligence can be added safely, repeatedly and predictably.

Expected outcome after the seven compressed scaffold sprints:

```text
Scaffold architecture grade: A−
Medical application grade: B+
```

Reason:

The scaffold can become A− because the platform machinery will be structured, testable, maintainable and scalable.

The full medical application will not yet be A-grade because governed intelligence coverage will still be incomplete. That grade is earned during the KB-WAVE phase, when the scaffold is populated with sufficient governed WHY, modifier, interaction and edge-case content.

The corrected strategic model is therefore:

```text
Phase 1 objective:
Build an A− scaffold.

Phase 2 objective:
Use that scaffold to build an A− medical intelligence platform.
```

This grade model is strategic shorthand, not an Automation Bus pass/fail criterion. Sprint acceptance is governed by the concrete gates, tests, audits and evidence defined above.

---

# 12. Summary

The architecture is worth continuing.

The next phase is not a rebuild, not frontend polish, and not a rush to launch.

The next phase is scaffold completion.

The compressed seven-sprint plan preserves the substance of the 13-sprint roadmap while reducing ceremony and grouping compatible work.

This revision incorporates the latest execution-hardening review by:

- making Sprint 2 unconditionally HIGH
- making Sprint 4 unconditionally HIGH
- clarifying Sprint 2 split handling for coherence and narrative audit scopes
- requiring GPT/human authority for Sprint 4 material rescoping
- adding cross-sprint regression/smoke policy
- distinguishing machine-enforced vs documentation-only KB lifecycle controls
- clarifying Sprint 1 Gate B wording
- marking Sprint 7 as HIGH / MIXED
- allowing separable Sprint 7 content work to continue only by explicit authority if behaviour work blocks

The intended end state is a platform where adding new medical intelligence is predictable asset work, not repeated architectural repair.
