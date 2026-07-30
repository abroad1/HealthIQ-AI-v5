---
work_id: ARCH-CONV-E
branch: feature/arch-conv-e-alt-why-authority
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# ARCH-CONV-E — ALT WHY-Authority Migration and Legacy Retirement

## Objective

Migrate ALT WHY authority to the canonical identity:

```text
signal_alt_high::inv_alt_high_hepatocellular_injury
```

and retire the temporary runtime WHY ownership held by:

```text
signal_hepatic_alt_context
```

only after:

- canonical identity and source closure;
- Head of Medical Research Gate 1 decisions;
- Anthony Gate 2 ratification;
- deterministic compilation and runtime implementation;
- independent STOP C proof.

The intended end state is:

```text
signal_alt_high
  = canonical ALT signal identity
  = governed compiled ALT WHY authority

signal_hepatic_alt_context
  = no longer owns runtime ALT WHY
  = retained only as governed legacy/predecessor evidence
```

This sprint must also close the small, directly related ARCH-CONV-C lineage defect by recomputing and correcting the stale ALP/GGT compiled-output hashes before new hepatic compiled authority is added.

## Governing rules

Apply the repository-governed versions of:

- `AUTOMATION_BUS_SOP_v1.3.1.md`
- `KNOWLEDGE_BUS_SOP_v1.3.1.md`
- `KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md`

Mandatory lifecycle:

```text
Stage 0 scope already approved
→ Claude hardening
→ Automation Bus start
→ Phase 0
→ independent STOP A
→ Phase 1 Gate 1 submission
→ Head of Medical Research Gate 1
→ Anthony Gate 2 ratification
→ Phase 2 implementation
→ independent STOP C
→ Automation Bus finish
→ independent audit
→ explicit human merge authority
```

Cursor must not self-certify STOP A, Gate 1, Gate 2 or STOP C.

Identity must come from governed embedded fields and explicit registers, never filenames, package names, directory order or load order.

Canonical research is the only medical authority. Package files and compiled artefacts may express or reduce canonical research but must not invent new medical meaning.

Runtime must consume governed compiled artefacts only. Frontend remains render-only.

## Mandatory hardening

Before Automation Bus start, Claude must execute:

```text
harden work_id: ARCH-CONV-E — verify source content and produce evidence checklist
```

Do not begin repository implementation until:

```text
automation_bus/latest_prompt_hardening.json
```

records:

```text
work_id: ARCH-CONV-E
status: HARDENED
```

## Baseline and branch preparation

1. Fetch and confirm local `main == origin/main`.
2. Confirm ARCH-CONV-D is merged and published.
3. Create:

```text
feature/arch-conv-e-alt-why-authority
```

from current `main`.
4. Confirm the working tree is clean.
5. Confirm stash is empty.
6. Confirm there is no active Automation Bus token.
7. Run:

```text
python backend/scripts/run_work_package.py start
```

8. Confirm kernel state:

```text
work_id: ARCH-CONV-E
status: IN_PROGRESS
```

STOP if any lifecycle artefact refers to another work ID.

# Scope

## In scope

### Canonical ALT target

```text
signal_alt_high::inv_alt_high_hepatocellular_injury
knowledge_bus/research/investigation_specs/inv_alt_high_hepatocellular_injury_v1.yaml
pkg_s24_alt_high_hepatocellular_injury
```

### Candidate ALT frames for medical review

```text
signal_alt_high::inv_alt_high_hepatocellular_injury_pattern
signal_alt_high::inv_alt_high_metabolic_steatotic_liver_pattern
signal_alt_high::inv_alt_high_muscle_source_or_exertional_pattern
```

### Legacy predecessor and WHY authority

```text
signal_hepatic_alt_context
signal_hepatic_alt_context::inv_alt_context
knowledge_bus/root_cause/hypotheses/alt_hypotheses_v1.yaml
```

### Hepatocellular collision policy

A new governed hepatocellular authority group/axis may be created only after Gate 1 and Gate 2 adjudication.

### Threshold governance

Hardcoded ALT-context thresholds must be:

- mapped;
- medically reviewed;
- either replaced by governed SSOT/runtime marker status, explicitly retained under ratified evidence, or removed from the new authority path;
- never silently transferred.

### ARCH-CONV-C lineage repair

Verify and, if required, correct only the stale `output_hash` values in:

```text
knowledge_bus/compiled/manifests/arch_conv_c_alp_high.yaml
knowledge_bus/compiled/manifests/arch_conv_c_ggt_high.yaml
```

The repair must:

- recompute hashes from the actual compiled artefacts;
- prove source and compiled bytes are otherwise unchanged;
- not recompile, rewrite or medically alter ALP/GGT content;
- be separately identified in commits and STOP C evidence.

## Explicit exclusions

Do not migrate or create authority for:

```text
signal_ast_high
signal_bilirubin_high
signal_hyperbilirubinemia
signal_alp_low
```

Do not alter:

- the ratified `cholestatic_source_axis` ALP/GGT policy;
- ALP or GGT compiled medical content;
- liver-card scoring;
- frontend medical logic;
- unrelated reports, snapshots, fixtures or estate records;
- raw Pass 3 sources;
- unrelated knowledge packages.

AST, bilirubin, ALP and GGT may appear only as supporting, contradiction or future-boundary context where present in canonical ALT sources. This grants no authority to those families.

# Phase 0 — Architecture identity, source and lineage closure

Before making any medical or runtime decision, create:

```text
docs/architecture/ARCH-CONV-E_STOP_A_identity_source_and_lineage_closure.md
docs/architecture/ARCH-CONV-E_target_to_frame_map.md
docs/architecture/ARCH-CONV-E_medical_review_pack.md
docs/architecture/ARCH-CONV-E_medical_decision_register.yaml
docs/architecture/ARCH-CONV-E_arch_conv_c_hash_repair_evidence.md
```

## Phase 0A — Reconfirm ARCH-CONV-D identity closure

Verify from current `main` that:

- `signal_alt_high` is the sole canonical future ALT authority identity;
- `signal_hepatic_alt_context` is recorded as a legacy predecessor/context implementation;
- no runtime alias exists;
- legacy WHY remains temporarily owned by `signal_hepatic_alt_context`;
- all ARCH-CONV-E successor blockers are present.

STOP if the merged repository does not match the approved ARCH-CONV-D decision.

## Phase 0B — Canonical ALT source reconstruction

Record for the canonical frame and each candidate:

```text
activation_key
signal_id
embedded spec_id
canonical source path
source SHA-256
package_id
translation_mode
identity-index status
provenance status
signal-layer status
legacy WHY status
compiled WHY status
runtime authority status
```

Do not infer identity from filenames.

Validate the canonical investigation spec using the repository validator.

## Phase 0C — Legacy ALT reconstruction

Map exactly:

- every hypothesis in `alt_hypotheses_v1.yaml`;
- the registry and loader path;
- its primary signal identity;
- all assumptions, causes, supporting markers, contradiction markers and caveats;
- any claims not traceable to the canonical ALT source;
- any family-level collapse or duplicate-output risk;
- current runtime output when only `signal_hepatic_alt_context` fires;
- current runtime output when both live ALT signals fire.

No legacy disconnection is authorised in Phase 0 or Phase 1.

## Phase 0D — Threshold reconstruction

Map every numeric literal used in the two live ALT signal implementations, including:

```text
ALT > 120
AST > 45
GGT > 60
ALP > 130
bilirubin > 20
```

For each, record:

```text
source file
governed source, if any
clinical purpose
runtime effect
whether it duplicates lab-range SSOT
whether it is required by canonical ALT research
whether transfer would alter emitted behaviour
```

Do not remediate thresholds before Gate 1 and Gate 2.

## Phase 0E — ARCH-CONV-C manifest hash repair

Independently recompute the compiled artefact hashes for canonical ALP and GGT.

If the manifest hashes already match, record `NO_CHANGE_REQUIRED`.

If they do not match:

1. prove the compiled artefact bytes match the merged ARCH-CONV-C implementation;
2. prove canonical source hashes remain correct;
3. update only the stale manifest `output_hash` fields;
4. run the focused ARCH-CONV-C validators and tests;
5. commit the repair separately:

```text
fix(governance): repair ARCH-CONV-C compiled manifest hashes
```

Do not modify compiled ALP/GGT artefacts.

STOP and escalate if any mismatch involves compiled content rather than manifest metadata.

## Phase 0F — Proposed hepatocellular authority boundary

Reconstruct, but do not adjudicate:

- whether ALT can be primary authority for a hepatocellular biochemical pattern;
- how AST, bilirubin, ALP, GGT, albumin, symptoms, medication/exposure history, exercise/muscle injury and serial results may support or contradict;
- how the hepatocellular pattern remains separate from `cholestatic_source_axis`;
- how concurrent ALT and ALP/GGT findings avoid duplicate or conflicting user-facing output;
- whether one new authority group is required;
- deterministic selection requirements;
- future bilirubin and AST boundaries.

No medical or collision-policy decision may be made by Cursor.

# STOP A — Independent architecture approval

Stop after Phase 0.

The STOP A submission must answer:

1. Is the canonical migration target unambiguously:

```text
signal_alt_high::inv_alt_high_hepatocellular_injury
```

2. Are all candidate identities, sources, provenance states and legacy paths closed?
3. Is the ARCH-CONV-C manifest-hash defect either repaired safely or proven absent?
4. Is the threshold issue fully mapped?
5. Is the proposed medical-review boundary sufficient?
6. Are AST, bilirubin and `cholestatic_source_axis` exclusions preserved?
7. Can Phase 1 prepare Gate 1 decisions without implementation?

Return:

```text
ARCH-CONV-E PHASE 0 COMPLETE

Branch
Baseline commit
Hardening reference
Automation Bus start result
Kernel status
Phase 0 commit(s)
Working-tree status
Stash status

Canonical ALT identity
Candidate frame map
Legacy WHY ownership and risks
Threshold map
ARCH-CONV-C hash-repair result
Proposed hepatocellular authority boundary
Explicit exclusions

Created artefacts
Verification performed

STOP A status:
AWAITING INDEPENDENT HEAD OF ARCHITECTURE APPROVAL
```

Do not proceed until explicit STOP A approval.

# Phase 1 — Gate 1 medical-review submission

Proceed only after independent STOP A approval.

Finalise:

```text
docs/architecture/ARCH-CONV-E_medical_review_pack.md
docs/architecture/ARCH-CONV-E_medical_decision_register.yaml
```

Set state:

```text
GATE_1_SUBMISSION_READY_FOR_HEAD_OF_MEDICAL_RESEARCH
```

All medical and collision-policy decisions must remain `PENDING`.

## Gate 1 decisions required

### Canonical ALT frame

For:

```text
signal_alt_high::inv_alt_high_hepatocellular_injury
```

request structured decisions on:

- `APPROVE`, `APPROVE_WITH_NARROWING`, `REJECT`, `DEFER_EVIDENCE_INSUFFICIENT` or `CONTEXT_ONLY`;
- causal versus context-only role;
- whether ALT alone may support a hepatocellular biochemical-pattern WHY;
- magnitude/severity handling;
- serial-result requirements;
- symptom/history requirements;
- medication/toxin/viral/exposure wording boundaries;
- specific-disease prohibitions;
- missing-data fail-closed rules.

### Pass 3 candidate frames

Request separate decisions for:

```text
inv_alt_high_hepatocellular_injury_pattern
inv_alt_high_metabolic_steatotic_liver_pattern
inv_alt_high_muscle_source_or_exertional_pattern
```

For each, require:

- approval status;
- causal/context role;
- provenance sufficiency;
- required supporting data;
- prohibited attribution;
- compile or defer disposition.

### Supporting-marker roles

Request explicit decisions on:

- AST;
- bilirubin;
- ALP;
- GGT;
- albumin;
- metabolic context;
- exercise/muscle injury context;
- alcohol and medication context;
- symptoms and serial trends.

No supporting marker may gain independent WHY authority through ARCH-CONV-E.

### Threshold decisions

For every current hardcoded threshold, request one:

```text
REPLACE_WITH_GOVERNED_LAB_STATUS
REPLACE_WITH_GOVERNED_SSOT_THRESHOLD
RETAIN_WITH_EXPLICIT_MEDICAL_RATIONALE
REMOVE_FROM_CANONICAL_RUNTIME_PATH
DEFER_AND_BLOCK_IMPLEMENTATION
```

No threshold may be transferred by default.

### Hepatocellular collision policy

Request decisions on:

- axis/group name;
- primary/supporting/context families;
- ALT-only behaviour;
- ALT plus AST;
- ALT plus bilirubin;
- ALT plus ALP/GGT cholestatic pattern;
- ALT plus exercise/muscle evidence;
- consolidation, suppression, parallel-output and refusal rules;
- duplicate-user-facing-signal prohibition;
- future-safe bilirubin and AST boundaries;
- activation-key-explicit deterministic selection.

### Legacy disposition

Request explicit adjudication of:

```text
alt_hypotheses_v1.yaml
signal_hepatic_alt_context
signal_hepatic_alt_context::inv_alt_context
```

Choose:

```text
CONDITIONAL_REPLACE
PARTIAL_CONTENT_TRANSFER
RETAIN_TEMPORARILY
RETIRE_WITHOUT_TRANSFER
DEFER
```

Specify exactly when runtime disconnection is allowed.

Stop for Head of Medical Research Gate 1.

# Gate 2 — Anthony ratification

No Phase 2 implementation may begin until Anthony explicitly ratifies the complete Gate 1 decision register.

The Gate 2 record must identify:

- Gate 1 reference;
- ratified canonical and candidate-frame decisions;
- ratified threshold treatment;
- ratified hepatocellular collision policy;
- ratified legacy transfer/retirement conditions;
- explicit exclusions;
- Phase 2 authorisation boundary.

# Phase 2 — Implementation

Proceed only after both Gate 1 and Gate 2 are recorded.

## Required outcomes

Implement only the ratified decisions.

Where authorised, this may include:

- canonical compiled ALT WHY artefact;
- compile manifest with source and output hashes;
- compiled/root-cause authority-register rows;
- explicit `why_role`;
- conditional role metadata;
- hepatocellular authority-group/collision-policy row;
- activation-key-explicit collision resolution;
- governed threshold replacement;
- lineage metadata;
- root-cause compiler/report/DTO propagation required for the ratified role;
- deterministic legacy runtime disconnection for the ratified activation key;
- focused tests.

## Legacy retirement requirement

If Gate 1 and Gate 2 authorise replacement:

- `signal_alt_high` must become the active governed ALT WHY authority;
- `signal_hepatic_alt_context` must no longer emit runtime ALT WHY;
- no runtime alias may collapse the two implementations;
- `alt_hypotheses_v1.yaml` must remain physically present unless deletion is separately authorised;
- retirement must be represented explicitly in authority registers;
- direct legacy fallback must be unreachable for the retired identity;
- no duplicate ALT user-facing findings may remain.

## Fail-closed requirements

- Missing or unsupported activation identity must not select a frame.
- Missing required supporting markers must not upgrade causal eligibility.
- Missing history/exposure data must not be inferred.
- Unsupported role or conditional metadata must raise or refuse, never default to causal.
- No filename, lexical, package, filesystem or load-order selection.
- No frontend medical inference.

## Explicit non-goals during implementation

Do not:

- create AST WHY;
- migrate bilirubin/hyperbilirubinemia;
- alter ALP/GGT clinical policy;
- change liver-card scoring;
- rewrite unrelated report prose;
- promote blocked Pass 3 candidates without ratified authority;
- update unrelated fixtures to conceal regressions.

# STOP C — Independent runtime proof

Create:

```text
docs/architecture/ARCH-CONV-E_STOP_C_runtime_proof.md
```

Prove:

1. `signal_alt_high` is the active canonical ALT WHY authority.
2. `signal_hepatic_alt_context` no longer owns runtime ALT WHY if retirement was ratified.
3. Legacy asset remains physically preserved.
4. No duplicate ALT user-facing WHY is emitted.
5. Every ratified ALT concordance/discordance state behaves deterministically.
6. Every deferred/rejected frame is unreachable.
7. Threshold behaviour exactly matches Gate 1 and Gate 2.
8. Unsupported/missing metadata fails closed.
9. Role survives compiler, report, DTO and serialisation paths.
10. Hepatocellular and cholestatic authority groups do not suppress or duplicate one another incorrectly.
11. AST and bilirubin gain no independent authority.
12. ALP/GGT compiled content remains unchanged.
13. ARCH-CONV-C manifest hashes are valid.
14. Frontend remains render-only and unchanged unless DTO typing alone was explicitly required.
15. Source and output hashes reproduce exactly.
16. Repeated and reverse-input runs are deterministic.
17. Full-suite comparison shows zero new ARCH-CONV-E-attributable failures.

If the full suite has baseline failures, compare exact node IDs against an isolated worktree at the baseline commit. Classify shared, resolved, newly introduced and environmental/non-comparable outcomes.

STOP for independent Head of Architecture approval.

Do not run Automation Bus finish before STOP C approval.

# Verification

At minimum run:

- canonical investigation-spec validation;
- relevant Knowledge Bus package validators;
- identity-index validator;
- compiled WHY authority gate;
- focused ARCH-CONV-C hash/authority tests;
- focused ARCH-CONV-D identity tests;
- new ARCH-CONV-E ALT authority tests;
- combined ARCH-CONV-B/C/E authority suites;
- collision-policy tests;
- clinician-report and DTO role-propagation tests;
- default golden-panel semantic comparison;
- full backend suite with baseline comparison if failures exist;
- lint/type checks for touched code;
- repository hygiene and stash checks.

Do not claim PASS from truncated output. Preserve full command output or exact test-node extracts where needed.

# Post-Implementation Closure Protocol

After independent STOP C approval:

1. Run and report:

```text
git branch --show-current
git status --short
git log --oneline -n 5
git diff --name-only
git diff --cached --name-only
git stash list
```

2. Classify all tracked, staged, untracked, tooling, out-of-scope and stash items.
3. Confirm branch and diff boundaries.
4. Run the required Automation Bus gate.
5. Run:

```text
python backend/scripts/run_work_package.py finish
```

only after gate PASS.
6. Commit kernel-generated `COMPLETE` status only in accordance with Automation Bus SOP v1.3.1.
7. Return final gate evidence, kernel status, closure audit and merge-readiness report.
8. Do not merge without explicit human merge authority.

# Completion criteria

ARCH-CONV-E is complete only when:

- canonical ALT identity/source closure is preserved;
- Gate 1 and Gate 2 are recorded;
- `signal_alt_high` owns ratified compiled ALT WHY authority;
- legacy ALT WHY ownership is retired or retained exactly as ratified;
- no duplicate ALT user-facing authority remains;
- thresholds are governed exactly as ratified;
- hepatocellular collision policy is explicit and deterministic;
- AST, bilirubin and ALP/GGT boundaries hold;
- ARCH-CONV-C manifest hashes validate;
- STOP C proves runtime safety and zero attributable regressions;
- Automation Bus finish passes;
- independent audit recommends merge;
- explicit human merge authority is given.
