---
work_id: P1-12
branch: work/P1-12-pass3-deferred-cbc-iron-hematology-batch-c
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: CONTENT
---

# P1-12 — Pass 3 Signal Intelligence Batch C: Deferred CBC / Iron / Haematology Review Cohort

## Objective

Run the third Pass 3 signal-intelligence batch promotion sprint.

This sprint focuses on the CBC / iron / haematology clusters deferred by P1-11 because of frame-authority, medical-review, or source-support blockers.

This sprint must determine which deferred clusters can now be safely promoted into staged, non-runtime PSI artefacts, and which must remain deferred with a clear blocker.

This sprint is part of the eight-block beta-readiness programme.

It follows:

```text
P1-10 — Pass 3 Launch-Core Signal Intelligence Batch A
P1-11 — Pass 3 CBC / Iron / Oxygen Signal Intelligence Batch B
```

P1-11 promoted the safe Batch B cohort and deferred conflicted clusters. P1-12 must now resolve the deferred cohort in a governed way without forcing unsafe medical intelligence into the signal estate.

Promotion is not activation.

Do not make anything runtime-active.

Do not change runtime behaviour.

## Strategic purpose

This sprint prevents the Pass 3 ingestion programme from accumulating unresolved deferred medical-intelligence clusters.

The goal is not to promote everything.

The goal is to make a governed decision for each deferred CBC / iron / haematology cluster:

```text
promote safely to staged PSI
promote partially with explicit blockers
defer pending medical review
defer pending frame-authority decision
defer pending source research support
defer pending schema support
```

This must remain a batch sprint, not one-marker-at-a-time work.

## Branch and state checks

Start from `main`.

```powershell
git switch main
git pull origin main
git status --short
git rev-parse main
git rev-parse origin/main
```

Confirm:

```text
- current branch is main
- local main == origin/main
- working tree is clean
```

Then create:

```powershell
git switch -c work/P1-12-pass3-deferred-cbc-iron-hematology-batch-c
```

Do not proceed if the working tree is dirty.

Confirm the Automation Bus active work package/state file if required by SOP.

## Required prerequisites on main

These files must exist on `main`:

```text
docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md
docs/sprints/beta_readiness/P1-9_pass3_research_to_runtime_exploitation_map.md
docs/sprints/beta_readiness/P1-9_pass3_research_to_runtime_exploitation_matrix.yaml
docs/sprints/beta_readiness/P1-10_pass3_launch_core_signal_intelligence_batch_a.md
docs/sprints/beta_readiness/P1-10_signal_intelligence_batch_a_manifest.yaml
docs/sprints/beta_readiness/P1-11_pass3_cbc_iron_oxygen_signal_intelligence_batch_b.md
docs/sprints/beta_readiness/P1-11_signal_intelligence_batch_b_manifest.yaml
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
docs/governance/KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md
```

If any are missing, stop and report:

```text
P1-12 prerequisite beta-readiness or governance evidence is not present on main. P1-12 must not proceed.
```

## First authority documents

Read these first, in this order:

```text
docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md
docs/sprints/beta_readiness/P1-11_pass3_cbc_iron_oxygen_signal_intelligence_batch_b.md
docs/sprints/beta_readiness/P1-11_signal_intelligence_batch_b_manifest.yaml
docs/sprints/beta_readiness/P1-10_pass3_launch_core_signal_intelligence_batch_a.md
docs/sprints/beta_readiness/P1-10_signal_intelligence_batch_a_manifest.yaml
docs/sprints/beta_readiness/P1-9_pass3_research_to_runtime_exploitation_map.md
docs/sprints/beta_readiness/P1-9_pass3_research_to_runtime_exploitation_matrix.yaml
docs/governance/KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md
docs/governance/KNOWLEDGE_BUS_SOP_v1.3.1.md
docs/architecture/ADR-RT-001_research_to_runtime_day_one_architecture.md
docs/architecture/ADR-LAYER-BOUNDARY-RECONCILIATION-1.md
docs/architecture/User Health to Systems Map_FINAL.md
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

Use the `healthiq-knowledge-bus-medical-intelligence` agent rule if available.

If the agent rule is missing, continue under the approved sprint prompt, but record that the specialist rule was not available.

## Scope

Use P1-11’s deferred clusters as the starting point.

Candidate deferred clusters include, if present in P1-11 deliverables:

```text
- haemoglobin low / oxygen-carrying-capacity pattern
- haemoglobin high / erythrocytosis-context pattern
- iron low
- iron high
- MCHC high / spherocytic-context pattern
- platelet high / clonal-context pattern
- platelet low / marrow-suppression-context pattern
- any Batch B cluster classified as DEFER_FRAME_AUTHORITY_CONFLICT
- any Batch B cluster classified as DEFER_MEDICAL_REVIEW_REQUIRED
- any Batch B cluster classified as DEFER_INSUFFICIENT_SCHEMA_SUPPORT
```

Do not assume these are safe to promote.

For each deferred cluster, determine whether new or already-existing source evidence, schema support, frame authority, or medical-review evidence supports staged non-runtime PSI promotion.

## Direct source inspection requirement

For each cluster considered, inspect the relevant Pass 3 / investigation-spec content directly.

Do not infer from filenames only.

Inspect source research for:

```text
- biomarker identity
- high/low/directional pattern
- biological rationale
- corroborating markers
- contradiction or suppression markers
- context requirements
- safety cautions
- non-diagnostic wording constraints
- system/subsystem mapping
- evidence/provenance references
- whether source support is primary or only secondary/contextual
```

Important rule:

Do not create a primary PSI signal for a biomarker if no direct primary Pass 3 investigation spec supports that biomarker/pattern.

You may capture the blocker in the sprint report and manifest.

## Adjudication classifications

Classify each considered cluster using only the following sprint-level values:

```text
PROMOTE_TO_STAGED_PSI
PROMOTE_PARTIAL_STAGED_PSI_WITH_BLOCKERS
DEFER_FRAME_AUTHORITY_CONFLICT
DEFER_MEDICAL_REVIEW_REQUIRED
DEFER_INSUFFICIENT_SOURCE_SUPPORT
DEFER_INSUFFICIENT_SCHEMA_SUPPORT
DEFER_NOT_BATCH_C_RELEVANT
```

Use these only in the sprint report and Batch C manifest unless the governed PSI schema already supports them.

Do not put unsupported fields into `promoted_signal_intelligence.yaml`.

## Medical-review boundary

Cursor does not perform medical review.

Cursor may only determine whether existing approved research/governance material supports promotion.

If a cluster requires medical judgement beyond existing approved source material, classify it as:

```text
DEFER_MEDICAL_REVIEW_REQUIRED
```

Do not promote it by inventing cautious wording.

Do not downgrade high-risk patterns to make them promotable.

## Expected promotion target

Use the same staged non-runtime pattern as P1-10 and P1-11.

Expected staged path:

```text
knowledge_bus/generated_pilot/p1_12_batch_c/
```

Do not write directly into production package manifests.

Do not create production manifest opt-ins.

Do not modify production packages.

Do not create a duplicate signal repository.

If the P1-10/P1-11 staged PSI pattern is not available on main, stop and report.

## Promotion rules

For any cluster that is safe to promote, create staged non-runtime PSI artefacts using the governed PSI schema.

Each PSI artefact must preserve, where schema-supported:

```text
- stable signal identifier
- source Pass 3 path and spec ID
- biomarker(s)
- directionality
- activation concept
- lab evidence requirements
- context requirements
- corroborating markers
- contradiction / suppression conditions
- cautious non-diagnostic framing
- root-cause / WHY substrate
- system or subsystem mapping
- evidence/provenance
```

Use repository-native schema vocabulary only.

Do not invent signal systems.

Do not invent trigger directions.

Do not use `trigger_direction: both`.

Do not add unsupported lifecycle, scoring, review or runtime fields to PSI.

Capture readiness metadata in the sprint report, Batch C manifest, or compile manifest only.

## Specific safety constraints

Do not add diagnostic claims such as confirmed anaemia, iron deficiency, iron overload, infection, malignancy, bleeding, haemochromatosis, thrombocytopenia, myeloproliferative disorder, haemolysis, immune disorder, or marrow failure.

Do not recommend treatment, medication, supplements, referral urgency, or investigation pathways.

Do not add global/default reference ranges.

Do not add placeholder scoring bands.

Do not override lab-provided reference ranges.

Do not infer symptoms unless present in approved source context.

## Runtime non-activation rule

All Batch C promoted artefacts must remain non-runtime-active.

Do not add production manifest opt-ins.

Do not modify runtime loaders.

Do not modify compiled cards.

Do not modify scoring policy.

Do not modify backend runtime or frontend.

If a promotion would become runtime-consumed automatically, stop and report before writing it.

## Permitted changes

Expected product changes may include:

```text
knowledge_bus/generated_pilot/p1_12_batch_c/
docs/sprints/beta_readiness/P1-12_pass3_deferred_cbc_iron_hematology_batch_c.md
docs/sprints/beta_readiness/P1-12_signal_intelligence_batch_c_manifest.yaml
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
automation_bus/
```

Within `knowledge_bus/generated_pilot/p1_12_batch_c/`, expected artefacts may include:

```text
- batch compile manifest index
- package-scoped promoted_signal_intelligence.yaml files
- package-scoped compile_manifest.yaml files
```

## Prohibited changes

Do not modify:

```text
frontend/
Gemini paths
fallback parser paths
backend/core/
backend/ssot/scoring_policy.yaml
runtime DTO contracts
domain assemblers
narrative assemblers
compiled runtime cards
production package manifests
Pass 3 source files
investigation-spec source files
Knowledge Bus source package files outside the approved staged Batch C target
docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md
docs/AUTHORITY_MAP.md
```

## Required deliverable 1 — Sprint report

Create:

```text
docs/sprints/beta_readiness/P1-12_pass3_deferred_cbc_iron_hematology_batch_c.md
```

Use this structure:

```markdown
# P1-12 — Pass 3 Signal Intelligence Batch C: Deferred CBC / Iron / Haematology Review Cohort

## 1. Executive summary
- why this sprint was run
- which P1-11 deferred clusters were reconsidered
- what Batch C promoted
- what remained deferred
- whether runtime activation remains unchanged
- recommended next sprint

## 2. Programme context
- relationship to eight-block beta-readiness
- relationship to P1-9
- relationship to P1-10
- relationship to P1-11
- why this is batch-based rather than one-marker-at-a-time

## 3. Deferred cluster baseline from P1-11
For each deferred cluster:
- P1-11 classification
- P1-11 blocker
- what P1-12 rechecked

## 4. Source research inspected
For each Pass 3 file/spec inspected:
- path
- spec IDs
- biomarkers/patterns
- source themes
- whether support is primary or secondary/contextual
- limitations

## 5. Adjudication findings
For each considered cluster:
- Batch C classification
- reason for promote/defer
- source-support finding
- frame-authority finding
- medical-review finding
- schema-support finding

## 6. Promotion implementation
For each promoted cluster:
- PSI artefact path
- compile manifest path
- source evidence path/spec ID
- runtime activation state
- system/subsystem mapping
- safety framing
- downstream gaps

## 7. Still-deferred clusters
For each still-deferred cluster:
- reason for deferral
- blocker type
- what is needed next
- whether it should be medical-review, frame-authority, schema, or source-research work

## 8. Safety and non-activation confirmation
Confirm:
- no runtime activation
- no scoring_policy change
- no backend/core change
- no frontend/Gemini/parser change
- no DTO/domain assembler change
- no compiled card change
- no production package manifest change
- no Pass 3 source change
- no diagnostic/treatment claims
- no global/default ranges
- no placeholder bands

## 9. Validation
- PSI validators run
- YAML parse checks
- git diff checks
- hash updates
- limitations

## 10. Business value delivered
Explain:
- what deferred ambiguity was reduced
- which research value was safely captured
- why any remaining deferrals protect product safety
- how this improves the signal estate without runtime activation

## 11. Carry-forwards
- clusters still requiring medical review
- clusters still requiring frame adjudication
- clusters still requiring source research
- clusters still requiring schema support
- scoring-policy needs
- prose/WHY needs
- runtime integration needs

## 12. Recommended next sprint
Recommend the next sprint with:
- title
- risk_level
- change_type
- scope
- STOP gates
- rationale
```

## Required deliverable 2 — Batch C manifest

Create:

```text
docs/sprints/beta_readiness/P1-12_signal_intelligence_batch_c_manifest.yaml
```

Use this structure:

```yaml
work_id: P1-12
classification_date: <YYYY-MM-DD>
source_authorities:
  - path: <path>
    role: <role>
batch:
  name: Pass 3 Signal Intelligence Batch C — Deferred CBC / Iron / Haematology
  considered_clusters: <number>
  promoted_clusters: <number>
  deferred_clusters: <number>
  promoted_psi_files: <number>
clusters:
  - id: <stable_cluster_slug>
    name: <human readable cluster name>
    p1_11_classification: <classification>
    p1_12_classification: PROMOTE_TO_STAGED_PSI | PROMOTE_PARTIAL_STAGED_PSI_WITH_BLOCKERS | DEFER_FRAME_AUTHORITY_CONFLICT | DEFER_MEDICAL_REVIEW_REQUIRED | DEFER_INSUFFICIENT_SOURCE_SUPPORT | DEFER_INSUFFICIENT_SCHEMA_SUPPORT | DEFER_NOT_BATCH_C_RELEVANT
    source_pass3_paths:
      - <path>
    source_spec_ids:
      - <spec_id>
    biomarkers:
      - <biomarker>
    support_type: primary | secondary_contextual | absent | unclear
    system_mapping:
      - <system>
    subsystem_mapping:
      - <subsystem>
    promotion_action: created | enriched | deferred | blocked
    staged_psi_paths:
      - <path>
    compile_manifest_paths:
      - <path>
    runtime_activation_state: inactive | blocked | review_required | not_runtime_consumed | unknown
    downstream_gaps:
      - <gap>
    evidence_paths:
      - <path>
    recommended_next_action: <short action>
validation:
  manifest_yaml_parse: pass | fail | not_run
  psi_validator: pass | fail | partial | not_run | not_found
  runtime_activation_check: pass | fail | not_run
```

The manifest is a planning and audit artefact.

It must not be consumed by runtime.

## Required deliverable 3 — Build deliverable register update

At closure, update:

```text
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

Append a short entry:

```markdown
## P1-12 — Pass 3 deferred CBC / iron / haematology Batch C

**Status:** Complete / Partial / Blocked  
**Date closed:** <YYYY-MM-DD>  
**Programme block(s):** Block 1 Core health systems model; Block 2 Subsystems and depth model; Block 3 Layer B intelligence/prose substrate; Block 6 Medical safety, research provenance and governance; Block 7 Auditability, reproducibility and traceability  

### Delivered / ticked off
- <what this sprint completed against the beta-readiness programme>
- <major Batch C promotion or adjudication outcome>

### Carry-forwards
- <what still needs to be done later>
- <known gaps exposed by this sprint>

### Blockers / risks
- <only material blockers or risks that affect future work>

### Recommended next sprint
- <next work package recommendation>
```

Keep the entry short.

Do not list every file touched.

Do not duplicate the sprint report.

## Validation

Run:

```powershell
git diff --stat
git diff --name-only
git status --short
```

Validate the Batch C manifest YAML:

```powershell
python -c "import yaml; from pathlib import Path; p=Path('docs/sprints/beta_readiness/P1-12_signal_intelligence_batch_c_manifest.yaml'); data=yaml.safe_load(p.read_text(encoding='utf-8')); assert data['work_id']=='P1-12'; assert 'clusters' in data; print('P1-12 Batch C manifest YAML parsed successfully')"
```

Run the PSI validator against every new or changed `promoted_signal_intelligence.yaml`.

Do not rely only on self-asserted PASS fields in compile manifests.

Capture the exact validator command and output for all changed PSI files.

If any validator fails, stop and report failure.

If compile manifests contain output hashes, update hashes after PSI edits and report the updated hashes.

## Runtime non-activation validation

Confirm:

```text
- no backend/core files changed
- no backend/ssot/scoring_policy.yaml change
- no frontend files changed
- no Gemini or fallback parser files changed
- no runtime DTO or assembler files changed
- no compiled cards changed
- no production package manifests changed
- no Pass 3 source files changed
- no staged PSI artefact is runtime-active
```

If compile manifests include `runtime_active`, confirm all are `false`.

If PSI files include any runtime or visibility field, report all values.

## Required final report

Return:

```text
- branch name
- main SHA baseline
- specialist agent availability
- P1-11 deferred clusters reconsidered
- source Pass 3 files/specs inspected
- clusters promoted
- clusters still deferred
- source-support blockers
- frame-authority blockers
- medical-review blockers
- schema-support blockers
- files changed
- runtime activation status
- PSI validator commands and outputs
- manifest YAML parse result
- hash updates
- whether production package manifests changed
- whether scoring_policy.yaml changed
- whether backend/frontend/runtime files changed
- whether Pass 3 source files changed
- recommended next sprint
- git diff --stat
- git diff --name-only
- git status --short
```

Do not merge until Claude audit, GPT architectural review and human approval.

## Acceptance criteria

This sprint is complete only if:

```text
1. P1-11 deferred CBC / iron / haematology clusters are reconsidered.

2. Relevant Pass 3 source research is directly inspected.

3. Source support is distinguished as primary, secondary/contextual, absent or unclear.

4. Safe clusters are promoted to staged, non-runtime PSI artefacts.

5. Unsafe or unsupported clusters remain deferred, not forced.

6. No runtime activation occurs.

7. No production scoring policy is changed.

8. No backend/core, frontend, Gemini, parser, DTO, assembler or compiled-card files are changed.

9. No production package manifest is changed.

10. No Pass 3 or investigation-spec source file is changed.

11. PSI files use governed schema vocabulary only.

12. No unsupported lifecycle fields are inserted into PSI.

13. No diagnostic or treatment claims are added.

14. No global/default ranges or placeholder scoring bands are added.

15. PSI validator is run against every new or changed PSI file.

16. Batch C report exists at:
    docs/sprints/beta_readiness/P1-12_pass3_deferred_cbc_iron_hematology_batch_c.md

17. Batch C manifest exists at:
    docs/sprints/beta_readiness/P1-12_signal_intelligence_batch_c_manifest.yaml

18. Build deliverable register is updated with a short P1-12 entry.

19. Manifest YAML validation passes.

20. Final report includes validation output and clean git status.
```
