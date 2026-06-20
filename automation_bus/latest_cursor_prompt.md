---
work_id: P1-11
branch: work/P1-11-pass3-cbc-iron-oxygen-signal-intelligence-batch-b
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: CONTENT
---

# P1-11 — Pass 3 Signal Intelligence Batch B: CBC / Iron / Oxygen Frame-Adjudication Cohort

## Objective

Run the second Pass 3 signal-intelligence batch promotion sprint.

This sprint focuses on the CBC / iron / oxygen-carrying-capacity research estate and must determine which related Pass 3 signal clusters can be safely promoted into governed non-runtime signal intelligence, and which must remain blocked or deferred because of unresolved frame authority.

This sprint is part of the eight-block beta-readiness programme.

It follows:

```text
P1-9 — Pass 3 Research-to-Runtime Exploitation Map
P1-10 — Pass 3 Launch-Core Signal Intelligence Batch A
```

P1-10 established the reusable batch-promotion pattern:

```text
Pass 3 investigation specs
→ staged governed PSI artefacts
→ compile manifests
→ batch manifest
→ build register entry
→ no runtime activation
```

P1-11 must continue that pattern, using the specialist Knowledge Bus medical-intelligence promotion discipline.

## Strategic purpose

This sprint must continue batch-based Pass 3 ingestion without falling into micro-sprints.

The goal is to capture the richness of the CBC / iron / oxygen research estate while preserving medical safety, frame authority, and non-runtime staging.

Promotion is not activation.

Do not make anything runtime-active.

Do not add production scoring policy.

Do not create or modify compiled runtime cards.

Do not modify backend runtime, frontend, Gemini, parser, DTO, or domain assembler files.

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
git switch -c work/P1-11-pass3-cbc-iron-oxygen-signal-intelligence-batch-b
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
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
docs/governance/KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md
```

If any are missing, stop and report:

```text
P1-11 prerequisite beta-readiness or governance evidence is not present on main. P1-11 must not proceed.
```

## First authority documents

Read these first, in this order:

```text
docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md
docs/sprints/beta_readiness/P1-9_pass3_research_to_runtime_exploitation_map.md
docs/sprints/beta_readiness/P1-9_pass3_research_to_runtime_exploitation_matrix.yaml
docs/sprints/beta_readiness/P1-10_pass3_launch_core_signal_intelligence_batch_a.md
docs/sprints/beta_readiness/P1-10_signal_intelligence_batch_a_manifest.yaml
docs/governance/KNOWLEDGE_BUS_PASS3_PROMOTION_PROTOCOL_v1.1.md
docs/governance/KNOWLEDGE_BUS_SOP_v1.3.1.md
docs/architecture/ADR-RT-001_research_to_runtime_day_one_architecture.md
docs/architecture/ADR-LAYER-BOUNDARY-RECONCILIATION-1.md
docs/architecture/User Health to Systems Map_FINAL.md
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

Use the new `healthiq-knowledge-bus-medical-intelligence` agent rule if available.

If the agent rule is missing, continue under the approved sprint prompt, but record that the specialist agent rule was not available.

## Critical frame-adjudication gate

Before promoting any CBC / iron / oxygen signal intelligence, identify whether there are unresolved frame-authority conflicts.

Search for and inspect evidence relating to:

```text
CBC
haematology
hemoglobin
haemoglobin
hematocrit
haematocrit
RBC
MCV
MCH
MCHC
RDW
platelets
WBC
neutrophils
lymphocytes
ferritin
iron
transferrin
transferrin saturation
TIBC
UIBC
oxygen carrying capacity
anaemia
anemia
iron deficiency
iron overload
inflammation
blood oxygen
```

Inspect relevant Pass 3 / investigation-spec files directly.

Likely files may include, if present:

```text
knowledge_bus/research/investigation_specs/multi_llm_research/cbc_hematology_pass_3.json
knowledge_bus/research/investigation_specs/multi_llm_research/iron_pass_3.json
knowledge_bus/research/investigation_specs/multi_llm_research/Batch_*.json
```

Do not infer from filenames only.

The sprint must classify each selected CBC / iron / oxygen cluster as one of:

```text
PROMOTE_TO_STAGED_PSI
PROMOTE_PARTIAL_STAGED_PSI_WITH_BLOCKERS
DEFER_FRAME_AUTHORITY_CONFLICT
DEFER_MEDICAL_REVIEW_REQUIRED
DEFER_INSUFFICIENT_SCHEMA_SUPPORT
DEFER_NOT_BATCH_B_RELEVANT
```

Use these classifications only in the sprint report and Batch B manifest unless the governed artefact schema already supports them.

Do not put unsupported classification fields into `promoted_signal_intelligence.yaml`.

## Batch B target scope

Target a meaningful cohort, not a micro-sprint.

Target size:

```text
Minimum: 4 material clusters
Maximum: 8 material clusters
```

Candidate clusters to consider include, if supported by source research and repository evidence:

```text
- haemoglobin low / oxygen-carrying-capacity pattern
- haemoglobin high / concentration or erythrocytosis-context pattern
- haematocrit high / low pattern
- MCV low / microcytic-pattern context
- MCV high / macrocytic-pattern context
- RDW high / anisocytosis or mixed-pattern context
- ferritin low / iron-store depletion context
- ferritin high / inflammation or iron-overload-context pattern
- transferrin saturation high / iron-overload-context pattern
- transferrin saturation low / iron-availability context
- platelet high / reactive-pattern context
- platelet low / thrombocytopenia-context pattern
- neutrophil high / inflammation or stress-response context
- lymphocyte low / immune/stress-context pattern
```

Do not force all of these into scope.

Select the most coherent 4–8 clusters based on Pass 3 richness, launch-core relevance, downstream gap, and frame safety.

If a cluster has unresolved frame authority, do not force promotion. Defer it and explain why.

## Promotion target

Use the same staging pattern as P1-10 unless the repository governance documents require a different pattern.

Expected staged path:

```text
knowledge_bus/generated_pilot/p1_11_batch_b/
```

Do not write directly into production package manifests unless explicitly required by the sprint and confirmed safe.

Do not create a duplicate authority source.

If the authoritative PSI staging pattern from P1-10 is unavailable or invalid, stop and report.

## Promotion rules

For each selected cluster that is safe to promote, create staged, non-runtime PSI artefacts using the governed PSI schema.

Each promoted PSI artefact must preserve, where the schema supports it:

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
- non-diagnostic safety framing
- root-cause / WHY substrate
- system or subsystem mapping
- evidence/provenance
```

Use repository-native schema vocabulary only.

Do not invent signal systems.

Do not invent trigger directions.

Do not use `signal_system: cardiovascular` if the PSI schema does not allow it.

Do not use legacy `trigger_direction: both`; use valid vocabulary such as `bidirectional` or `context_dependent` where schema-supported.

Do not add unsupported lifecycle fields to PSI.

If readiness, runtime activation, medical-review, or scoring status cannot be stored in PSI, capture it in:

```text
- sprint report
- Batch B manifest
- compile manifest
```

## Runtime non-activation rule

All Batch B promoted artefacts must remain non-runtime-active.

Do not add production manifest opt-ins.

Do not modify runtime loaders.

Do not modify compiled cards.

Do not modify scoring policy.

Do not modify backend runtime or frontend.

If a promotion would become runtime-consumed automatically, stop and report before writing it.

## Specific safety constraints

Do not add diagnostic claims such as confirmed anaemia, iron deficiency, iron overload, infection, malignancy, bleeding, haemochromatosis, thrombocytopenia diagnosis, or immune disorder diagnosis.

Use cautious educational wording only.

Do not recommend treatment.

Do not add supplement or medication advice.

Do not add global/default reference ranges.

Do not add placeholder scoring bands.

Do not override lab-provided reference ranges.

Do not infer symptoms unless present in source context.

## Permitted changes

Expected product changes may include:

```text
knowledge_bus/generated_pilot/p1_11_batch_b/
docs/sprints/beta_readiness/P1-11_pass3_cbc_iron_oxygen_signal_intelligence_batch_b.md
docs/sprints/beta_readiness/P1-11_signal_intelligence_batch_b_manifest.yaml
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
automation_bus/
```

Within `knowledge_bus/generated_pilot/p1_11_batch_b/`, expected artefacts may include:

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
Knowledge Bus source package files outside the approved staged Batch B target
docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md
docs/AUTHORITY_MAP.md
```

## Required deliverable 1 — Sprint report

Create:

```text
docs/sprints/beta_readiness/P1-11_pass3_cbc_iron_oxygen_signal_intelligence_batch_b.md
```

Use this structure:

```markdown
# P1-11 — Pass 3 Signal Intelligence Batch B: CBC / Iron / Oxygen Frame-Adjudication Cohort

## 1. Executive summary
- why this sprint was run
- what Batch B promoted
- what was deferred
- whether frame authority blocked any clusters
- whether runtime activation remains unchanged
- recommended next sprint

## 2. Programme context
- relationship to eight-block beta-readiness
- relationship to P1-9
- relationship to P1-10
- why this is batch-based rather than one-marker-at-a-time

## 3. Source research inspected
For each Pass 3 file/spec inspected:
- path
- spec IDs
- biomarkers/patterns
- source themes
- limitations

## 4. Frame-adjudication findings
For each considered cluster:
- frame authority status
- selected classification
- reason for promote/defer
- safety constraints

## 5. Batch B selection rationale
- clusters considered
- clusters selected
- clusters deferred
- why this is the right-sized batch

## 6. Promotion implementation
For each promoted cluster:
- PSI artefact path
- compile manifest path
- source evidence path/spec ID
- runtime activation state
- system/subsystem mapping
- safety framing
- downstream gaps

## 7. Deferred clusters
For each deferred cluster:
- reason for deferral
- blocker type
- what is needed next

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
- limitations

## 10. Business value delivered
Explain:
- how this improves the blood / iron / oxygen signal estate
- how much Pass 3 richness was captured
- why staged promotion improves defensibility without unsafe activation

## 11. Carry-forwards
- deferred clusters for Batch C or medical review
- frame-authority decisions needed
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

## Required deliverable 2 — Batch B manifest

Create:

```text
docs/sprints/beta_readiness/P1-11_signal_intelligence_batch_b_manifest.yaml
```

Use this structure:

```yaml
work_id: P1-11
classification_date: <YYYY-MM-DD>
source_authorities:
  - path: <path>
    role: <role>
batch:
  name: Pass 3 Signal Intelligence Batch B — CBC / Iron / Oxygen
  selected_clusters: <number>
  deferred_clusters: <number>
  promoted_psi_files: <number>
clusters:
  - id: <stable_cluster_slug>
    name: <human readable cluster name>
    batch_classification: PROMOTE_TO_STAGED_PSI | PROMOTE_PARTIAL_STAGED_PSI_WITH_BLOCKERS | DEFER_FRAME_AUTHORITY_CONFLICT | DEFER_MEDICAL_REVIEW_REQUIRED | DEFER_INSUFFICIENT_SCHEMA_SUPPORT | DEFER_NOT_BATCH_B_RELEVANT
    source_pass3_paths:
      - <path>
    source_spec_ids:
      - <spec_id>
    biomarkers:
      - <biomarker>
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
## P1-11 — Pass 3 CBC / iron / oxygen signal intelligence Batch B

**Status:** Complete / Partial / Blocked  
**Date closed:** <YYYY-MM-DD>  
**Programme block(s):** Block 1 Core health systems model; Block 2 Subsystems and depth model; Block 3 Layer B intelligence/prose substrate; Block 6 Medical safety, research provenance and governance; Block 7 Auditability, reproducibility and traceability  

### Delivered / ticked off
- <what this sprint completed against the beta-readiness programme>
- <major Batch B promotion or frame-adjudication outcome>

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

Validate the Batch B manifest YAML:

```powershell
python -c "import yaml; from pathlib import Path; p=Path('docs/sprints/beta_readiness/P1-11_signal_intelligence_batch_b_manifest.yaml'); data=yaml.safe_load(p.read_text(encoding='utf-8')); assert data['work_id']=='P1-11'; assert 'clusters' in data; print('P1-11 Batch B manifest YAML parsed successfully')"
```

Run the PSI validator against every new or changed `promoted_signal_intelligence.yaml`.

Do not rely only on self-asserted PASS fields in compile manifests.

Capture the exact validator command and output for all changed PSI files.

If any validator fails, stop and report failure.

If no validator exists, record this clearly and use YAML/schema/manual checks.

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
- source Pass 3 files/specs inspected
- clusters considered
- clusters promoted
- clusters deferred
- frame-authority blockers
- files changed
- runtime activation status
- PSI validator commands and outputs
- manifest YAML parse result
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
1. CBC / iron / oxygen Pass 3 source research is directly inspected.

2. Frame authority is assessed before promotion.

3. A meaningful Batch B cohort is considered.

4. Safe clusters are promoted to staged, non-runtime PSI artefacts.

5. Unsafe or conflicted clusters are deferred, not forced.

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

16. Batch B report exists at:
    docs/sprints/beta_readiness/P1-11_pass3_cbc_iron_oxygen_signal_intelligence_batch_b.md

17. Batch B manifest exists at:
    docs/sprints/beta_readiness/P1-11_signal_intelligence_batch_b_manifest.yaml

18. Build deliverable register is updated with a short P1-11 entry.

19. Manifest YAML validation passes.

20. Final report includes validation output and clean git status.
```
