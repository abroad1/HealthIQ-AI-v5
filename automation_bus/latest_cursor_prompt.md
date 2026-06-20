---
work_id: P1-9
branch: work/P1-9-pass3-research-to-runtime-exploitation-map
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: CONTENT
---

# P1-9 — Pass 3 Research-to-Runtime Exploitation Map

## Objective

Deeply inspect the Pass 3 / investigation-spec research corpus and map what high-value medical research exists but has not yet been promoted into governed runtime-safe HealthIQ AI artefacts.

This sprint is part of the eight-block beta-readiness programme.

It follows P1-7, which established that the estate is research-rich but unevenly promoted. P1-7 assessed the promoted/runtime-facing estate. P1-9 must now inspect the upstream Pass 3 research corpus directly.

The purpose is to answer:

```text
What medical intelligence exists in the Pass 3 research files that has not yet been promoted into:
- package authority
- signal intelligence
- compiled card evidence
- root-cause / WHY authority
- scoring readiness
- prose / explainer assets
- test fixtures
- replay/provenance surfaces
- runtime-ready system or subsystem cards
```

This sprint must distinguish:

```text
research exists
```

from:

```text
research has been safely promoted into governed runtime artefacts
```

---

## Strategic purpose

This sprint is not a local thyroid investigation.

It is a programme-level research exploitation sprint.

HealthIQ AI’s defensible business value depends on having a repeatable, auditable production line for converting medical research into safe, deterministic, explainable runtime intelligence.

This sprint must create the map needed to industrialise that production line.

Do not implement runtime behaviour.

Do not promote packages.

Do not modify Knowledge Bus source packages.

Do not modify compiled cards.

Do not modify scoring policy.

Do not change backend or frontend code.

Do not activate signals.

Do not create new medical claims.

---

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
git switch -c work/P1-9-pass3-research-to-runtime-exploitation-map
```

Do not proceed if the working tree is dirty.

Confirm the Automation Bus active work package/state file if required by SOP.

---

## Required prerequisites on main

These files must exist on `main`:

```text
docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md
docs/sprints/beta_readiness/P1-7_research_to_runtime_adequacy_gate.md
docs/sprints/beta_readiness/P1-7_research_to_runtime_readiness_matrix.yaml
docs/sprints/beta_readiness/P1-8_scoring_lab_range_engine.md
docs/architecture/ADR-SCORING-LAB-RANGE-ONLY-BIOMARKER-RULES-1.md
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

If any are missing, stop and report:

```text
P1-9 prerequisite beta-readiness evidence is not present on main. P1-9 must not proceed.
```

---

## First authority documents

Read these first, in this order:

```text
docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md
docs/sprints/beta_readiness/P1-7_research_to_runtime_adequacy_gate.md
docs/sprints/beta_readiness/P1-7_research_to_runtime_readiness_matrix.yaml
docs/sprints/beta_readiness/P1-8_scoring_lab_range_engine.md
docs/architecture/ADR-SCORING-LAB-RANGE-ONLY-BIOMARKER-RULES-1.md
docs/architecture/ADR-LAYER-BOUNDARY-RECONCILIATION-1.md
docs/architecture/User Health to Systems Map_FINAL.md
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

Do not list standard SOP files as authority documents in the output unless a specific requirement cannot otherwise be located.

---

## Pass 3 corpus discovery

Locate the Pass 3 / investigation-spec corpus.

Start by inspecting likely paths:

```text
knowledge_bus/research/investigation_specs/
knowledge_bus/research/investigation_specs/multi_llm_research/
knowledge_bus/research/
```

Search for files containing:

```text
investigation_spec
pass_3
Pass 3
research_claims
clinical_interpretation
evidence
biomarker
signal
activation
medical_review
```

If the Pass 3 corpus is stored elsewhere, locate it using repository search.

The report must state:

```text
- exact paths inspected
- number of files found
- file types found
- whether each file appears to be a true Pass 3 / investigation-spec research asset
- any expected corpus paths that were missing
```

Do not assume file locations from memory.

---

## Depth requirement

This sprint must inspect the upstream research corpus directly.

Do not rely only on:

```text
- package files
- compiled cards
- estate index
- readiness matrix
- runtime registers
- prior summaries
```

Those artefacts are useful comparison targets, but the central task is to inspect the Pass 3 / investigation-spec source material itself.

For each material Pass 3 file, inspect enough content to determine:

```text
- biomarkers covered
- signal/pattern concepts
- clinical rationale
- context requirements
- evidence strength
- contraindications / safety cautions
- root-cause / WHY material
- system/subsystem relevance
- prose/explainer potential
- promotion status, if indicated
```

Do not claim a file was assessed if only its filename was scanned.

If the corpus is too large to read every line manually, use script-assisted extraction to index and summarise structured fields, but the output must still identify source paths and not rely on filename-only inference.

Do not commit temporary scripts or temporary generated files unless explicitly needed as deliverables.

---

## Comparison targets

For each Pass 3 research item, compare against promoted/runtime-facing artefacts, including where present:

```text
knowledge_bus/
knowledge_bus/governance/
knowledge_bus/compiled/
knowledge_bus/compiled/estate_index_v1.yaml
knowledge_bus/compiled/health_system_cards/
knowledge_bus/compiled/manifests/
knowledge_bus/pathway_explainers_v1/
backend/ssot/scoring_policy.yaml
backend/core/analytics/
backend/core/knowledge/
backend/core/dto/
backend/tests/
docs/intelligence/
docs/testing/
docs/architecture/
docs/sprints/beta_readiness/P1-7_research_to_runtime_readiness_matrix.yaml
```

Do not modify these files.

---

## Classification taxonomy

Classify each Pass 3 research item or cluster into one primary research-to-runtime state:

```text
FULLY_PROMOTED_RUNTIME_VISIBLE
PROMOTED_RUNTIME_ACTIVE_SIGNAL_ONLY
PROMOTED_COMPILED_CARD_ONLY
PROMOTED_HIDDEN_MED_REV1
PACKAGE_PRESENT_BUT_CARD_MISSING
RESEARCH_PRESENT_PACKAGE_MISSING
RESEARCH_PRESENT_SIGNAL_INTELLIGENCE_MISSING
RESEARCH_PRESENT_ROOT_CAUSE_WHY_MISSING
RESEARCH_PRESENT_SCORING_BLOCKED
RESEARCH_PRESENT_PROSE_THIN
RESEARCH_PRESENT_TEST_THIN
RESEARCH_PRESENT_GOVERNANCE_CONFLICT
RESEARCH_PRESENT_MEDICAL_REVIEW_REQUIRED
RESEARCH_PRESENT_CONTEXT_MODEL_REQUIRED
RESEARCH_PRESENT_UNMAPPED_TO_SYSTEM
RESEARCH_PRESENT_UNMAPPED_TO_SUBSYSTEM
NOT_LAUNCH_RELEVANT
UNKNOWN_INSUFFICIENT_EVIDENCE
```

Use one primary classification per row, with secondary blockers where needed.

Choose the conservative classification where evidence is mixed.

---

## Required dimensions

For each material research item or cluster, assess:

```text
1. Upstream research depth
2. Biomarker / pattern clarity
3. Signal activation readiness
4. Package promotion status
5. Compiled card evidence status
6. Root-cause / WHY readiness
7. Scoring readiness
8. Prose / explainer readiness
9. Medical-review status
10. Context requirements
11. Test readiness
12. Runtime integration readiness
13. System/subsystem mapping clarity
14. Beta-readiness relevance
```

Use ratings:

```text
Strong
Partial
Weak
Absent
Blocked
Unknown
Not applicable
```

---

## Required deliverable 1 — Exploitation report

Create:

```text
docs/sprints/beta_readiness/P1-9_pass3_research_to_runtime_exploitation_map.md
```

Use this structure exactly:

```markdown
# P1-9 — Pass 3 Research-to-Runtime Exploitation Map

## 1. Executive summary
- why this sprint was run
- whether Pass 3 research was directly inspected
- estate-level finding
- highest-value unpromoted research areas
- most common promotion gaps
- recommended next sprint

## 2. Programme context
- relationship to eight-block beta-readiness programme
- relationship to P1-7 adequacy gate
- relationship to P1-8 scoring lab-range engine
- why this is not a local thyroid investigation

## 3. Corpus discovery
- paths searched
- files found
- files assessed
- file types
- limitations
- any expected paths missing

## 4. Method
- authority documents read
- extraction/search approach
- comparison targets
- classification taxonomy
- how filename-only inference was avoided
- limitations

## 5. Estate-level research finding
State whether the upstream research estate is:
- thin;
- rich but unpromoted;
- unevenly promoted;
- governance-conflicted;
- context-model blocked;
- scoring blocked;
- prose/WHY thin;
- or another evidenced formulation.

## 6. Pass 3 research-to-runtime matrix
Create a table:

| Research item / cluster | Source Pass 3 path(s) | Biomarkers / patterns | System / subsystem mapping | Primary classification | Research depth | Package status | Signal authority | Compiled card status | Root-cause / WHY readiness | Scoring readiness | Prose / explainer readiness | Test readiness | Runtime readiness | Evidence paths | Recommended action |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

Include all material items discovered.

## 7. Highest-value unpromoted research
Identify the research items/clusters with the highest commercial/runtime value that are not yet fully promoted.

For each:
- why it matters;
- what exists upstream;
- what is missing downstream;
- recommended promotion action.

## 8. Launch-core impact
Assess impact on launch-core systems:
- cardiovascular / lipids / inflammation
- blood sugar / metabolic
- liver / detox
- kidney function
- blood / iron / oxygen
- thyroid / energy regulation

State which launch-core systems are already sufficiently promoted and which remain thin or blocked.

## 9. Subsystem impact
Assess impact on subsystem depth:
- compiled but hidden MED-REV1 subsystems
- orphaned compiled artefacts
- subsystem candidates from User Health to Systems Map
- subsystem candidates present in Pass 3 but not promoted

## 10. Promotion gap analysis
Group gaps by:
- package missing
- signal intelligence missing
- compiled card missing
- root-cause / WHY missing
- scoring blocked
- context model required
- medical review required
- prose/explainer thin
- test/provenance thin
- governance conflict

## 11. Batch promotion strategy
Recommend a batch-based promotion strategy.

Do not recommend one-marker-at-a-time promotion unless clinically unavoidable.

Do not recommend uncontrolled mass promotion.

Define 3–6 proposed cohorts, for example:
- launch-core blockers
- MED-REV1 hidden compiled subsystems
- research-present uncompiled clusters
- scoring-ready lab-range-only candidates
- context-dependent high-risk endocrine/androgen/thyroid candidates
- prose/WHY uplift cohort

For each cohort:
- scope
- expected value
- risk
- STOP gates
- recommended sequencing

## 12. Immediate next sprint recommendation
Name the single next sprint.

Include:
- title
- risk_level
- change_type
- expected scope
- STOP gates
- why it should be next

## 13. Carry-forwards by beta-readiness block
Group carry-forwards under:
- Block 1 Core health systems model
- Block 2 Subsystems and depth model
- Block 3 Layer B intelligence/prose substrate
- Block 6 Medical safety, research provenance and governance
- Block 7 Auditability, reproducibility and traceability
- Block 5 UX/results page, only where relevant

## 14. Business interpretation
Explain in business terms:
- whether the research estate is a weakness or an underexploited asset;
- what this means for HealthIQ AI’s defensibility;
- how the promotion factory should become a strategic capability.
```

---

## Required deliverable 2 — Machine-readable exploitation matrix

Create:

```text
docs/sprints/beta_readiness/P1-9_pass3_research_to_runtime_exploitation_matrix.yaml
```

Use this structure:

```yaml
work_id: P1-9
classification_date: <YYYY-MM-DD>
source_authorities:
  - path: <path>
    role: <role>
corpus:
  inspected_paths:
    - <path>
  files_found: <number>
  files_assessed: <number>
  limitations:
    - <limitation>
summary:
  estate_finding: <short finding>
  material_items: <number>
  fully_promoted_count: <number>
  unpromoted_or_partial_count: <number>
  blocked_count: <number>
  recommended_next_sprint: <title>
items:
  - id: <stable_slug>
    name: <human readable name>
    source_pass3_paths:
      - <path>
    biomarkers_or_patterns:
      - <name>
    system_mapping:
      - <system>
    subsystem_mapping:
      - <subsystem>
    primary_classification: FULLY_PROMOTED_RUNTIME_VISIBLE | PROMOTED_RUNTIME_ACTIVE_SIGNAL_ONLY | PROMOTED_COMPILED_CARD_ONLY | PROMOTED_HIDDEN_MED_REV1 | PACKAGE_PRESENT_BUT_CARD_MISSING | RESEARCH_PRESENT_PACKAGE_MISSING | RESEARCH_PRESENT_SIGNAL_INTELLIGENCE_MISSING | RESEARCH_PRESENT_ROOT_CAUSE_WHY_MISSING | RESEARCH_PRESENT_SCORING_BLOCKED | RESEARCH_PRESENT_PROSE_THIN | RESEARCH_PRESENT_TEST_THIN | RESEARCH_PRESENT_GOVERNANCE_CONFLICT | RESEARCH_PRESENT_MEDICAL_REVIEW_REQUIRED | RESEARCH_PRESENT_CONTEXT_MODEL_REQUIRED | RESEARCH_PRESENT_UNMAPPED_TO_SYSTEM | RESEARCH_PRESENT_UNMAPPED_TO_SUBSYSTEM | NOT_LAUNCH_RELEVANT | UNKNOWN_INSUFFICIENT_EVIDENCE
    dimensions:
      upstream_research_depth: Strong | Partial | Weak | Absent | Blocked | Unknown | Not applicable
      biomarker_pattern_clarity: Strong | Partial | Weak | Absent | Blocked | Unknown | Not applicable
      signal_activation_readiness: Strong | Partial | Weak | Absent | Blocked | Unknown | Not applicable
      package_promotion_status: Strong | Partial | Weak | Absent | Blocked | Unknown | Not applicable
      compiled_card_status: Strong | Partial | Weak | Absent | Blocked | Unknown | Not applicable
      root_cause_why_readiness: Strong | Partial | Weak | Absent | Blocked | Unknown | Not applicable
      scoring_readiness: Strong | Partial | Weak | Absent | Blocked | Unknown | Not applicable
      prose_explainer_readiness: Strong | Partial | Weak | Absent | Blocked | Unknown | Not applicable
      medical_review_status: Strong | Partial | Weak | Absent | Blocked | Unknown | Not applicable
      context_requirements: Strong | Partial | Weak | Absent | Blocked | Unknown | Not applicable
      test_readiness: Strong | Partial | Weak | Absent | Blocked | Unknown | Not applicable
      runtime_integration_readiness: Strong | Partial | Weak | Absent | Blocked | Unknown | Not applicable
    evidence_paths:
      - <path>
    downstream_gaps:
      - <gap>
    recommended_action: <short action>
```

This matrix is a planning artefact only.

It must not be consumed at runtime.

Do not place it in `backend/ssot/`, `knowledge_bus/compiled/`, `knowledge_bus/governance/`, or any runtime path.

---

## Required deliverable 3 — Build deliverable register update

At closure, update:

```text
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

Append a short entry:

```markdown
## P1-9 — Pass 3 research-to-runtime exploitation map

**Status:** Complete / Partial / Blocked  
**Date closed:** <YYYY-MM-DD>  
**Programme block(s):** Block 1 Core health systems model; Block 2 Subsystems and depth model; Block 3 Layer B intelligence/prose substrate; Block 6 Medical safety, research provenance and governance; Block 7 Auditability, reproducibility and traceability  

### Delivered / ticked off
- <what this sprint completed against the beta-readiness programme>
- <major Pass 3 exploitation or promotion-readiness finding>

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

Do not duplicate the full report.

---

## Prohibited changes

Do not modify:

```text
backend/
frontend/
knowledge_bus/
```

Exception:

```text
You may read files under those directories, but must not change them.
```

Do not modify:

```text
docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md
docs/AUTHORITY_MAP.md
```

Do not modify any:

```text
source package
compiled card
governance register
scoring policy
runtime code
test file
frontend file
Gemini path
fallback parser path
Pass 3 source file
Knowledge Bus source file
```

Expected product changes are limited to:

```text
docs/sprints/beta_readiness/P1-9_pass3_research_to_runtime_exploitation_map.md
docs/sprints/beta_readiness/P1-9_pass3_research_to_runtime_exploitation_matrix.yaml
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

Bus files may change as part of SOP lifecycle.

---

## Validation

Run:

```powershell
git diff --stat
git diff --name-only
git status --short
```

Validate the exploitation matrix YAML.

If no specific schema validator exists, at minimum parse it with Python using a PowerShell-compatible command:

```powershell
python -c "import yaml; from pathlib import Path; p=Path('docs/sprints/beta_readiness/P1-9_pass3_research_to_runtime_exploitation_matrix.yaml'); data=yaml.safe_load(p.read_text(encoding='utf-8')); assert data['work_id']=='P1-9'; assert isinstance(data.get('items'), list); assert data['items'], 'matrix must contain at least one item'; print('P1-9 exploitation matrix YAML parsed successfully')"
```

No runtime tests are required because this is CONTENT-only.

If any code/runtime/source package/governance register/test file is changed, stop and report failure.

---

## Required final report

Return:

```text
- branch name
- main SHA baseline
- files changed
- Pass 3 corpus paths inspected
- number of Pass 3 files found
- number of Pass 3 files assessed
- estate-level finding
- number of material research items/clusters classified
- top unpromoted research assets
- top downstream promotion gaps
- recommended batch promotion strategy
- recommended next sprint
- confirmation no runtime/code/source package/scoring/governance/test files changed
- validation run and results
- git diff --stat
- git diff --name-only
- git status --short
```

Do not merge until Claude audit, GPT architectural review and human approval.

---

## Acceptance criteria

This sprint is complete only if:

```text
1. Exploitation report exists at:
   docs/sprints/beta_readiness/P1-9_pass3_research_to_runtime_exploitation_map.md

2. Machine-readable exploitation matrix exists at:
   docs/sprints/beta_readiness/P1-9_pass3_research_to_runtime_exploitation_matrix.yaml

3. Build deliverable register is updated with a short P1-9 entry.

4. Pass 3 / investigation-spec corpus paths are directly inspected and reported.

5. The report states how many Pass 3 files were found and assessed.

6. The report avoids filename-only inference.

7. The report distinguishes upstream research depth from downstream runtime promotion readiness.

8. Material Pass 3 research items/clusters are classified using the approved taxonomy.

9. Launch-core impact is explicitly assessed.

10. Subsystem impact is explicitly assessed.

11. Highest-value unpromoted research areas are identified.

12. Batch promotion strategy is recommended rather than one-by-one or uncontrolled mass promotion.

13. A single immediate next sprint is recommended.

14. Matrix YAML parses successfully.

15. No runtime code, backend code, frontend code, scoring policy, governance register, Knowledge Bus source package, compiled card, test, Gemini, fallback parser, or Pass 3 source file is changed.

16. Only the expected documentation/planning files and bus files are changed.

17. Final report includes validation output and clean git status.
```
