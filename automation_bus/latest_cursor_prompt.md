---
work_id: ARCH-CONV-A
branch: feature/arch-conv-a-estate-why-authority-migration
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# ARCH-CONV-A — Estate-Wide WHY Authority Migration

## 1. Role and execution authority

You are Cursor operating under Automation Bus SOP v1.3.1, Knowledge Bus SOP v1.3.1 and the Knowledge Bus Pass 3 Promotion Protocol v1.1.

Implement only the work authorised in this prompt.

This is a HIGH-risk MIXED work package touching the Intelligence Core and changing emitted medical reasoning. MIXED work is governed using BEHAVIOUR controls.

You may:

* investigate the repository;
* update architecture and inventory artefacts;
* prepare medical-review evidence packs;
* implement deterministic compilation and runtime integration after the relevant STOP gates have been ratified;
* add or update tests;
* disconnect legacy WHY authority after explicit retirement authority;
* execute the Automation Bus lifecycle and required verification.

You may not:

* make medical decisions;
* infer approval from existing legacy content;
* ratify investigation frames;
* bypass GPT medical review or Anthony’s human ratification;
* compile or activate an unratified frame;
* continue past a STOP gate without explicit continuation authority;
* merge;
* self-certify correctness;
* manually edit kernel-owned Automation Bus status.

## 2. Product outcome

Complete estate-wide WHY authority migration so that:

> Every active production WHY target has explicit frame identity, ratified canonical medical authority, a deterministic compiled artefact and a governed runtime selection path.

The package is not complete merely because new artefacts exist.

Completion requires:

* canonical research authority;
* explicit target-to-frame identity;
* GPT medical review;
* Anthony ratification;
* deterministic compilation;
* governed runtime selection;
* structural inactivity of rejected and deferred frames;
* removal of migrated targets’ dependence on legacy WHY authority;
* aligned consumer and clinician outputs;
* provenance-bearing Layer B output;
* Layer C remaining render/translation only.

## 3. Authoritative sprint inputs

Read these sprint-specific documents in full:

```text
docs/architecture/ARCH-CONV-A_stage0_outcome_and_package_boundary.md
docs/architecture/ARCH-CONV-A_active_why_target_inventory.md
docs/architecture/ARCH-CONV-A_identity_and_source_readiness.md
docs/architecture/ARCH-CONV-A_medical_review_wave_plan.md
docs/architecture/ARCH-CONV-A_compile_and_runtime_integration_design.md
docs/architecture/ARCH-CONV-A_stop_gates_and_acceptance.md
docs/architecture/ARCH-CONV-A_test_and_replay_strategy.md
docs/architecture/ARCH-CONV-A_legacy_retirement_policy.md
docs/architecture/ARCH-CONV-A_stage0_advisory.md
docs/architecture/ARCH-CONV_ABC_minimum_package_validation.md
docs/architecture/ADR-RT-001_research_to_runtime_day_one_architecture.md
```

Locate the exact ADR path if its repository location differs.

Use the existing Package 1–3 and `ARCH-CONV-CORRECT-1` implementation and regression evidence as mandatory protection baselines.

The standard SOPs already govern this package and should not be copied into new project documents.

## 4. Fixed estate facts

The ratified estate baseline is:

```text
41 verified active WHY registry targets
5 targets represented by the proven migrated cohort
36 remaining targets in Package A scope
```

The migrated cohort currently represents:

```text
10 medically reviewed frames
9 COMPILED_ACTIVE
1 REJECTED and structurally inactive
```

The final frame count for the remaining 36 targets is:

```text
UNKNOWN UNTIL PHASE 1 IDENTITY AND SOURCE CLOSURE
```

Do not assume one target equals one frame.

No target may proceed to medical review or compilation until its complete target-to-frame disposition has passed STOP A.

## 5. Authority and identity model

Preserve these identities:

```text
signal_id
  = signal-family identity

activation_key
  = runtime activation identity

investigation_id / frame_id
  = medical interpretation identity
```

Every active interpretation must be addressable through explicit activation key and explicit frame identity.

Do not permit:

* ambiguous signal-only frame selection;
* lexicographic or load-order selection;
* file-name-based medical identity;
* duplicate activation-key registration;
* hidden fallback from a rejected or deferred frame;
* collapsing context/anchor frames with causal frames;
* treating one shared legacy file as one frame identity where it serves several interpretations;
* unresolved identity plurality entering medical review or compilation.

## 6. Package boundaries

### Package A owns

* exact active WHY target inventory;
* complete target-to-frame mapping;
* identity and canonical-source closure;
* medical-review evidence packs;
* medical-decision registers;
* deterministic WHY compilation;
* compile manifests and lineage primitives;
* explicit runtime WHY resolution;
* wave-level legacy authority replacement;
* target-local reachability proof;
* safe local legacy disconnection;
* regression and replay evidence.

### Package B retains

* estate-wide dual-authority elimination beyond target-local migration;
* shared fallback quarantine and retirement;
* cross-producer precedence;
* layered `why_it_matters` consolidation;
* configuration-driven fail-open closure;
* final physical retirement of shared legacy assets;
* selector mechanics spanning several authority producers.

### Package C retains

* complete replay manifests;
* full output-authority provenance;
* result-version policy;
* current/stale/incompatible classification;
* regeneration lineage;
* historic analysis disposition;
* historic waist-analysis remediation;
* authority-change-driven regeneration behaviour.

Do not absorb Package B or Package C outcomes into this package.

Package A must emit the source, compiler, authority and content lineage primitives Package C will later consume.

## 7. Internal wave structure

Retain one Package A work package with seven internal medical-review waves:

```text
Wave 0 — Homocysteine elevation-context disposition: 1 target
Wave 1 — Thyroid axis: 7 targets
Wave 2 — Lipid/cardiometabolic: 6 targets
Wave 3 — Renal: 3 targets
Wave 4 — Hepatic/biliary: 7 targets
Wave 5 — Iron/haematology: 8 targets
Wave 6 — Metabolic/systemic residual: 4 targets
```

Total: 36 remaining targets.

Wave allocation may change only during Phase 1 where identity plurality or canonical-source evidence proves reassignment is required.

Do not create separate work packages or sprints for:

* individual waves;
* individual targets;
* individual frames;
* compiler changes;
* registries;
* validators;
* documentation;
* policy;
* configuration;
* test-estate expansion.

Use internal phases and STOP gates.

## 8. Medical decision authority

Every proposed frame must receive:

```text
Gate 1 — structured GPT medical review
Gate 2 — explicit Anthony ratification
```

Medical decisions must use one of:

```text
APPROVE
APPROVE_WITH_NARROWING
REJECT
DEFER_EVIDENCE_INSUFFICIENT
CONTEXT_ONLY
```

Runtime consequences:

### APPROVE

Eligible for deterministic compilation after Anthony ratification.

### APPROVE_WITH_NARROWING

Compile only the explicitly ratified bounded interpretation.

### REJECT

The frame must be structurally incapable of:

* firing;
* ranking;
* serving WHY;
* appearing in consumer output;
* appearing in clinician output;
* driving interventions;
* returning through legacy fallback.

### DEFER_EVIDENCE_INSUFFICIENT

No active compiled frame may be produced.

Existing legacy content must not receive inherited approval or silently remain the authoritative substitute without explicit architectural disposition.

### CONTEXT_ONLY

A bounded non-causal context may be served.

Causal WHY must fail closed.

Cursor may prepare research inventories, evidence matrices, legacy comparisons and proposed frame mappings. Cursor must not decide the medical status.

## 9. Execution lifecycle

This package uses one Automation Bus lifecycle with human-controlled continuations.

```text
START
→ Phase 0
→ Phase 1
→ STOP A

authorised continuation
→ Phase 2 by wave
→ STOP B for each wave

ratified continuation
→ Phase 3
→ Phase 4 first-wave integration
→ STOP C

authorised continuation
→ later wave compilation and integration
→ Phase 5 retirement decisions
→ STOP D where required

final authorised continuation
→ Phase 6
→ independent audit
→ FINISH
```

Do not call Automation Bus `finish` at an internal STOP gate.

Do not create a new work package for each continuation unless the Automation Bus kernel proves incapable of safely maintaining this work package across gated continuations. If that control-plane limitation is encountered, STOP and report it. Do not invent a workaround or fragment the package.

## 10. Phase 0 — Estate and index reconciliation

### Objective

Create a verified operational baseline before identity closure.

### Required actions

* reconcile the Stage 0 target inventory against current runtime registries;
* confirm exactly 41 active WHY targets and identify any baseline drift;
* identify the 5 migrated targets and the 36 Package A targets;
* map every active target to:

  * runtime activation source;
  * current WHY source;
  * current loader;
  * current registry;
  * report/output consumers;
  * intervention consumers;
* refresh or correct the stale compiled-estate index where authorised by current architecture;
* record operational LLM allow-flag state where it can affect output behaviour;
* verify current production-capable entry points;
* verify there are no scheduled or background analysis paths omitted from the estate;
* reconcile all known Stage 0 findings D-1 through D-9;
* confirm Wave 0–6 allocations against repository reality;
* record all discrepancies.

### Outputs

Update or create the package-specific working artefacts required by the Stage 0 design, including:

* authoritative active-target inventory;
* runtime caller map;
* current-authority map;
* identity issue register;
* source-readiness register;
* wave allocation;
* evidence-gap register.

Use existing artefacts where Stage 0 specifies them rather than creating duplicate authorities.

### STOP conditions

STOP immediately if:

* the active target count cannot be reconciled;
* runtime contains an unmapped WHY authority;
* current behaviour materially contradicts Stage 0;
* the branch baseline already changed Package A scope;
* an unknown loader or registry can emit WHY;
* a parallel authority source exists outside the audited estate;
* a required authoritative input is missing.

Phase 0 may proceed directly into Phase 1 only where the operational estate is reconciled.

## 11. Phase 1 — Identity and canonical-source closure

### Objective

Establish the complete target-to-frame and canonical-source map for all 36 remaining targets.

### Required actions per target

Confirm:

```text
signal family
direction
signal_id
activation_key
all investigation/frame identities
current runtime WHY source
legacy source
canonical investigation specification
canonical-source status
medical-review readiness
consumer outputs
clinician outputs
intervention dependencies
risk classification
wave allocation
```

Classify source readiness using the Stage 0 model:

```text
COMPILED_AND_RATIFIED
COMPILED_BUT_RATIFICATION_INCOMPLETE
CANONICAL_RESEARCH_AVAILABLE_COMPILE_INCOMPLETE
CANONICAL_RESEARCH_INCOMPLETE_OR_AMBIGUOUS
LEGACY_ACTIVE_NO_ACCEPTED_REPLACEMENT
DUAL_SERVED
RUNTIME_UNREACHABLE
UNKNOWN
```

### Mandatory identity findings

Provide explicit dispositions for D-1 through D-9.

Resolve before relevant medical review:

* D-2: homocysteine elevation-context disposition;
* D-3: bilirubin identity duplication;
* any registry limitation preventing frame plurality;
* any shared legacy file serving multiple medical identities;
* any probable duplicate signal identity;
* each unconfirmed canonical-spec match;
* any contradictory governance register.

### Canonical-source rules

* Locate the canonical investigation specification where it exists.
* Do not use legacy runtime wording as canonical evidence.
* Do not promote raw Pass 3 or investigation specifications directly into runtime.
* Record absence or ambiguity rather than inventing a source.
* Do not edit medical research during Phase 1 unless separately authorised through the medical-review process.

### Required Phase 1 outputs

Produce the STOP A evidence pack containing:

```text
exact active target count
36-target Package A inventory
complete target-to-frame map
final frame count
canonical-source disposition for every frame
identity issues and resolutions
unresolved identity blockers
wave allocations
source-readiness counts
medical-review pack requirements
runtime and legacy-source mappings
Package B hand-offs
Package C lineage requirements
```

## 12. STOP A — Identity and source closure

At completion of Phase 1:

1. Commit the bounded Phase 0/1 work on the sprint branch.
2. Run relevant deterministic inventory, schema and non-runtime regression checks.
3. Produce the STOP A report.
4. Stop all Package A execution.

Do not:

* conduct medical review;
* edit canonical medical meaning;
* compile new medical artefacts;
* activate new runtime WHY;
* disconnect legacy authority;
* proceed to Phase 2.

Required decision:

```text
GPT architectural review
Anthony ratification
```

Package execution resumes only after an explicit continuation instruction.

## 13. Phase 2 — Medical-review waves

This phase begins only after STOP A ratification.

### Required action by wave

For each frame in the authorised wave:

* assemble canonical research;
* map current legacy interpretation;
* identify evidence supporting the proposed interpretation;
* identify contradictions and exclusions;
* identify confirmatory evidence;
* distinguish context from causal WHY;
* identify intervention implications;
* identify consumer/clinician wording implications;
* identify unsafe overstatement;
* prepare a structured medical-review pack.

Cursor must stop and return the pack for:

```text
GPT structured medical review
Anthony ratification
```

### Medical-review register

For each frame record:

```text
signal family
direction
activation_key
frame identity
canonical source
proposed interpretation
evidence boundaries
contradictions
confirmatory markers/tests
context versus causal status
consumer implications
clinician implications
intervention implications
medical decision
GPT review reference
Anthony ratification reference
```

Do not fabricate review references.

### Missing research

Where canonical evidence is absent or insufficient:

* record the research gap;
* classify the frame as blocked from compilation;
* return it for medical-research commissioning;
* do not translate existing legacy content into a compiled artefact;
* do not allow legacy authority to be treated as approved.

## 14. STOP B — Medical ratification by wave

STOP B repeats for every wave.

No frame may proceed to compilation until:

* GPT has completed structured medical review;
* Anthony has explicitly ratified the decision;
* the decision and references are recorded;
* the source specification reflects the ratified authority where required;
* upstream validation passes.

A wave may contain approved, narrowed, rejected, deferred and context-only frames.

The existence of blocked frames does not automatically block other independent frames in the wave, provided runtime identity and fallback safety permit isolated progression.

If the unresolved frame shares authority, loader or fallback behaviour with approved frames, STOP the affected group until safe separation is proven.

## 15. Phase 3 — Deterministic compile and validation

Phase 3 begins for ratified frames only.

### Compile chain

Use the existing architecture:

```text
validated canonical investigation specification
→ deterministic compiler/promotion process
→ compiled WHY artefact
→ compile manifest
→ authority registration candidate
```

Extend the proven compiler rather than creating a parallel compiler or hand-authored artefact path.

### Requirements

The compiler must:

* consume validated canonical research;
* fail on unresolved target/frame identity;
* fail when medical ratification is absent;
* support all ratified medical statuses safely;
* produce deterministic outputs;
* reject unsupported manual edits to compiled medical meaning;
* preserve source and authority lineage;
* produce governed artefacts suitable for thin runtime loading;
* not require runtime access to raw research;
* not create a second medical authority.

### Required lineage

Each compiled artefact or its manifest must preserve the existing canonical equivalents of:

```text
signal_id
direction
activation_key
investigation_id / frame_id
source_spec_id
source path
source version
source hash
medical decision status
GPT review reference
Anthony ratification reference
compiler id
compiler version
authority version
runtime compatibility version
output artefact identity
output hash / content hash
validation result
compile timestamp
legacy predecessor
promotion mode
```

Use existing canonical field names where they already represent these semantics.

Do not introduce duplicate schema fields merely to match this wording.

### Required validation

* upstream investigation-spec validation;
* compiler schema validation;
* deterministic repeat compilation;
* source-hash verification;
* output-hash verification;
* manifest completeness;
* frame identity completeness;
* activation-key uniqueness;
* no direct raw-research runtime reads;
* no package-layer invention of medical meaning.

Knowledge Bus promotion must follow the current validated process. Do not rely on any lifecycle mechanism documented as non-authoritative.

## 16. Phase 4 — Runtime integration by wave

### Objective

Make ratified compiled WHY the governed runtime authority for the integrated frame.

### Required actions

* register compiled authority against explicit activation key and frame identity;
* ensure runtime selection cannot rely on signal-only ambiguity;
* ensure loader remains thin and deterministic;
* ensure raw research is not read at runtime;
* ensure rejected/deferred frames remain structurally inactive;
* ensure context-only frames cannot emit causal WHY;
* ensure compiled authority wins deterministically over migrated legacy authority;
* preserve structured Layer B output;
* preserve Layer C render-only boundaries;
* update output and intervention mappings only where ratified;
* retain immutable rollback artefacts;
* add targeted tracing or evidence needed to prove runtime selection.

### First-wave selection

Use the ratified Stage 0 sequence unless STOP A or medical review produces a safer first runtime wave.

Wave 0 may be used as the first proof only if its homocysteine elevation-context disposition is medically and architecturally resolved.

Do not use an unresolved dual-authority case as the unattended integration template.

### First-wave evidence

Test at minimum:

* approved frame positive panel;
* gate-unmet panel;
* ambiguous panel;
* missing-data panel;
* contradictory-evidence panel where applicable;
* rejected/deferred inactivity;
* compiled-versus-legacy precedence;
* consumer output;
* clinician output;
* intervention references;
* provenance;
* Layer C non-inference;
* rollback.

## 17. STOP C — First-wave runtime proof

After the first authorised wave is integrated:

1. run targeted unit, integration and replay tests;
2. run the Package 1–3 and CORRECT-1 protection suites;
3. perform before/after representative replay;
4. prove rollback;
5. obtain independent Claude audit;
6. produce the STOP C evidence pack;
7. stop.

The STOP C pack must prove:

```text
compiled WHY is canonical
legacy cannot win
rejected and deferred frames are inactive
missing or contradictory evidence fails closed
identity selection is explicit
consumer and clinician outputs align
interventions do not reference suppressed frames
source and authority lineage are emitted
Layer C does not reconstruct medical meaning
rollback is executable and safe
```

Do not integrate later waves until:

```text
GPT architectural and medical review
Anthony continuation authorisation
```

Preparation of later medical-review packs may continue only where it cannot alter runtime authority or contaminate the first-wave proof.

## 18. Later-wave compilation and integration

After STOP C authorisation:

* repeat the proven compiler and runtime pattern for each ratified wave;
* stop at STOP B for each wave’s medical decisions;
* maintain per-wave evidence and rollback boundaries;
* do not generalise around a frame type the compiler does not represent safely;
* do not conceal exceptional behaviour inside hard-coded per-frame logic;
* return to STOP where a wave requires a materially different authority or runtime mechanism.

Package A remains one work package.

## 19. Phase 5 — Legacy authority retirement

For each migrated frame or target, classify the predecessor using exactly one applicable state:

```text
AUTHORITY_RETIRED
RUNTIME_DISCONNECTED
SHARED_PENDING_PACKAGE_B
HISTORIC_COMPATIBILITY_ONLY
ARCHIVED
PHYSICALLY_DELETED
```

### Rules

* authority retirement may precede physical deletion;
* compiled authority must not coexist indefinitely with a legacy authority for the same question;
* rejected or deferred frames must not fall back to legacy;
* migrated targets must not depend on legacy WHY;
* shared legacy files must not be deleted while unmigrated or Package B callers remain;
* compatibility readers must be isolated and non-authoritative;
* archived assets must not remain runtime-loadable;
* reachable fallback must not remain “just in case”;
* physical deletion requires caller and reachability proof;
* Git history is adequate preservation once deletion is authorised.

### Package B boundary

Use `SHARED_PENDING_PACKAGE_B` only where:

* Package A authority for migrated targets is retired;
* the legacy asset remains required by explicit Package B scope;
* migrated Package A targets cannot select it;
* all remaining callers are identified;
* the hand-off is recorded.

## 20. STOP D — Legacy retirement authority

Before disabling, archiving or physically deleting a legacy source, produce:

```text
legacy source
all known callers
affected targets and frames
replacement artefacts
runtime authority proof
replay comparison
intentional behaviour changes
rollback artefact
shared dependencies
static reachability evidence
runtime reachability evidence
recommended retirement state
Package B hand-off where applicable
```

Stop for:

```text
GPT architecture review
Anthony retirement authority
```

Do not physically delete a shared asset without explicit STOP D authority.

Target-local registry disconnection that has already been explicitly authorised may proceed where rollback and caller evidence are complete.

## 21. Phase 6 — Estate regression, replay and closure

### Required verification

Run all applicable:

* compiler schema tests;
* compiler determinism tests;
* manifest completeness tests;
* activation-key uniqueness tests;
* target-to-frame plurality tests;
* frame identity tests;
* legacy-versus-compiled precedence tests;
* rejected-frame structural inactivation tests;
* deferred-frame fail-closed tests;
* context-only versus causal-WHY tests;
* missing-evidence tests;
* contradictory-evidence tests;
* intervention reference tests;
* consumer/clinician alignment tests;
* source and authority provenance tests;
* thin-loader tests;
* Layer C non-inference tests;
* rollback tests;
* representative panel replay;
* historical replay where source inputs are valid;
* existing Package 1–3 protections;
* existing CORRECT-1 protections;
* MCV co-service protections;
* canonical broader regression and end-to-end suites.

Each clinically relevant wave must contain:

```text
positive panel
negative / gate-unmet panel
ambiguous panel
missing-data panel
contradictory-evidence panel
```

Expand the phenotype and replay estate inside Package A where coverage is insufficient.

### Final independent audit

Before Automation Bus `finish`, obtain an independent Claude audit covering:

* exact target and frame completion;
* medical-decision traceability;
* compiler determinism;
* runtime authority;
* dual-authority absence within Package A scope;
* rejected/deferred inactivity;
* legacy retirement states;
* replay and output alignment;
* Layer C boundary;
* Package B/C boundary compliance;
* regression results;
* closure readiness.

Cursor cannot substitute its own report for independent audit.

## 22. Success criteria

Package A can pass only when all are true:

```text
100% of active WHY targets are inventoried
100% of Package A targets have complete target-to-frame disposition
100% of frames have explicit identity
100% of frames have canonical-source disposition
100% of promoted frames have GPT review and Anthony ratification
100% of promoted artefacts are deterministically compiled
100% of promoted artefacts carry required lineage
0 promoted targets depend on legacy WHY authority
0 rejected frames remain runtime-reachable
0 deferred frames fail open to legacy
0 ambiguous signal-only selections remain within Package A scope
all required wave tests and replay suites pass
consumer and clinician outputs align
intervention references remain governed
Layer C non-inference protections pass
Package 1–3 and CORRECT-1 protections pass
all Package A legacy sources have explicit disposition
```

Package A may close while shared files remain physically present only where they are:

```text
SHARED_PENDING_PACKAGE_B
```

and cannot serve migrated Package A targets.

## 23. PASS, CORRECT and STOP

### PASS

Return PASS only when:

* all Package A success criteria are met;
* STOP A–D have received their required approvals;
* every promoted frame is ratified, compiled and governed;
* migrated targets no longer depend on legacy WHY;
* tests and replay pass;
* independent audit passes;
* only explicitly bounded Package B and Package C work remains.

### CORRECT

Return CORRECT only where:

* defects are bounded;
* the ratified architecture remains valid;
* no unsafe promotion occurred;
* correction does not require new medical authority;
* correction does not reopen Package A/B/C boundaries.

### STOP

Return STOP where:

* target/frame identity cannot be resolved;
* canonical research is absent for a required interpretation;
* medical review is incomplete;
* Anthony ratification is absent;
* compiler output is non-deterministic;
* runtime authority is ambiguous;
* a rejected or deferred frame can still surface;
* legacy can still win or fail open;
* rollback is unsafe;
* a medically meaningful unexplained replay drift occurs;
* Package A requires Package B or C to satisfy its own success criteria;
* Automation Bus state or branch authority is invalid.

## 24. Branch and repository discipline

Before starting:

* confirm local `main == origin/main`;
* ensure the working tree is clean;
* create and use exactly:

```text
feature/arch-conv-a-estate-why-authority-migration
```

* ensure the branch matches prompt front matter;
* run the Automation Bus start command using the governed work ID;
* confirm the active authority token matches `ARCH-CONV-A`.

Do not carry unrelated files, tooling files or pre-existing changes into the branch.

Follow the Post-Implementation Closure Protocol before `finish`.

## 25. Immediate authorised execution boundary

On first receipt of this prompt, Cursor is authorised only to:

```text
start the Automation Bus work package
execute Phase 0
execute Phase 1
prepare STOP A evidence
commit the bounded Phase 0/1 work
stop
```

Cursor is not authorised on first receipt to:

* begin medical review;
* edit medical authority;
* compile new WHY artefacts;
* activate new runtime authority;
* disconnect or delete legacy sources;
* proceed to Phase 2 or later phases.

Return the STOP A report for GPT architectural review and Anthony ratification.

## 26. STOP A return format

Return:

```text
WORK PACKAGE
work_id
branch
baseline main commit
current commit
Automation Bus status
authority token status

PHASE 0
active target count
migrated target count
Package A target count
registry and loader reconciliation
current WHY authorities
runtime entry points
estate-index corrections
LLM allow-flag finding
baseline discrepancies

PHASE 1
final target count
complete target-to-frame count
final frame count
frame plurality findings
canonical-source dispositions
source-readiness counts
identity findings D-1 through D-9
D-2 disposition
D-3 disposition
wave allocation
Package B hand-offs
Package C lineage requirements

STOP A
identity closure complete: YES / NO
canonical-source closure complete: YES / NO
targets blocked from medical review
unresolved evidence gaps
architecture blockers
medical-research requirements
tests run
files changed
commits
working-tree status

VERDICT
READY FOR STOP A REVIEW
or
STOP — IDENTITY/SOURCE CLOSURE INCOMPLETE

next authorised action
```

Stop after this report.
