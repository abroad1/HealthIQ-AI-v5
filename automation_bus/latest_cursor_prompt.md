---
work_id: P1-7
branch: work/P1-7-research-to-runtime-adequacy-gate
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: CONTENT
---

# P1-7 — Research-to-Runtime Adequacy Gate for Remaining Systems and Subsystems

## Objective

Run a programme-level research-to-runtime adequacy gate across the remaining HealthIQ AI systems and subsystem candidates before any further system-card or subsystem-card implementation continues.

This sprint is part of the eight-block beta-readiness programme.

It exists because P1-4, P1-5 and P1-6R exposed a broader risk:

```text id="ox1l5n"
HealthIQ AI may have rich upstream medical research, but not all of that research has been consistently promoted into governed runtime-safe artefacts:
- compiled card evidence
- signal authority
- scoring rails
- root-cause / WHY authority
- subsystem evidence
- prose / explainer assets
- medical-review status
- test fixtures
- replay/audit surfaces
```

The purpose is to distinguish:

```text id="clwzwp"
research exists
```

from:

```text id="v0o6qa"
research is promoted, governed, testable, and runtime-safe
```

Do not implement any runtime system cards in this sprint.

Do not promote any packages.

Do not modify Knowledge Bus packages.

Do not change scoring policy.

Do not alter runtime behaviour.

This sprint produces a readiness matrix and programme recommendation only.

---

## Strategic framing

This is not an investigation side quest.

This is a beta-readiness programme gate.

The output must tell the team:

```text id="12sz4n"
1. Which remaining systems/subsystems are genuinely ready for runtime card implementation.
2. Which are research-present but not compiled/promoted.
3. Which are blocked by governance drift.
4. Which are blocked by scoring architecture.
5. Which are blocked by thin prose/explainer/root-cause material.
6. Which need medical-review or Pass 3 promotion before implementation.
7. What the next build sprint should be.
```

This sprint must prevent thin runtime cards being created merely because the UI or domain model expects them.

---

## Branch and state checks

Start from `main`.

```powershell id="hss4jt"
git switch main
git pull origin main
git status --short
git rev-parse main
git rev-parse origin/main
```

Confirm:

```text id="0he8aq"
- current branch is main;
- local main == origin/main;
- working tree is clean.
```

Then create:

```powershell id="fcz31t"
git switch -c work/P1-7-research-to-runtime-adequacy-gate
```

Do not proceed if the working tree is dirty.

Confirm the Automation Bus active work package/state file if required by SOP.

---

## Prerequisites

Required files on `main`:

```text id="eos9h4"
docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md
docs/sprints/beta_readiness/P1-1_launch_core_domain_build_materials_map.md
docs/sprints/beta_readiness/P1-2_kidney_function_domain_card.md
docs/sprints/beta_readiness/P1-3_blood_iron_oxygen_domain_card.md
docs/sprints/beta_readiness/P1-4_thyroid_energy_regulation_domain_card.md
docs/sprints/beta_readiness/P1-5_ft3_thyroid_authority_reconciliation.md
docs/sprints/beta_readiness/P1-6R_thyroid_scoring_architecture_recovery.md
docs/architecture/ADR-THYROID-FT3-AUTHORITY-RECONCILIATION-1.md
docs/architecture/ADR-THYROID-SCORING-LAB-RANGE-ARCHITECTURE-1.md
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

If any are missing, stop and report:

```text id="9eg34d"
P1-7 prerequisite beta-readiness evidence is not present on main. P1-7 must not proceed.
```

---

## First authority documents

Read these first, in this order:

```text id="sh1m8s"
docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md
docs/sprints/beta_readiness/P1-1_launch_core_domain_build_materials_map.md
docs/sprints/beta_readiness/P1-2_kidney_function_domain_card.md
docs/sprints/beta_readiness/P1-3_blood_iron_oxygen_domain_card.md
docs/sprints/beta_readiness/P1-4_thyroid_energy_regulation_domain_card.md
docs/sprints/beta_readiness/P1-5_ft3_thyroid_authority_reconciliation.md
docs/sprints/beta_readiness/P1-6R_thyroid_scoring_architecture_recovery.md
docs/architecture/ADR-THYROID-FT3-AUTHORITY-RECONCILIATION-1.md
docs/architecture/ADR-THYROID-SCORING-LAB-RANGE-ARCHITECTURE-1.md
docs/architecture/ADR-LAYER-BOUNDARY-RECONCILIATION-1.md
docs/architecture/User Health to Systems Map_FINAL.md
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

Do not list the standard Knowledge Bus SOP or Automation Bus SOP as authority documents in the deliverable unless a specific governance requirement cannot otherwise be located.

---

## Additional files and directories to inspect

Inspect as needed. Do not modify.

```text id="so76r7"
docs/AUTHORITY_MAP.md
docs/strategy/eight_block_beta_readiness/EIGHT_BLOCK_BETA_READINESS_COMPARISON_AND_PROGRAMME_RECOMMENDATION_2026-06-18.md
docs/strategy/LAYER_ARCHITECTURE_AUTHORITY_INDEX_2026-06-17_r2.md
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
docs/medical_review/
```

If any listed path does not exist, record that honestly.

---

## Required search/discovery terms

Search the repository for system, subsystem, research, promotion and governance coverage using terms including:

```text id="fnaevd"
system
subsystem
health_system
health system
compiled card
card evidence
package_refs
runtime_active_canonical
compiled_not_promoted
blocked
deferred
activation_eligibility
medical review
root cause
WHY
pathway explainer
retail explainer
scoring_policy
system_weight
biomarkers
Pass 3
investigation spec
research asset
frame identity
authority register
signal intelligence
promoted_signal_intelligence
```

Also search for each health system or subsystem name found in:

```text id="8xjn93"
docs/architecture/User Health to Systems Map_FINAL.md
knowledge_bus/compiled/estate_index_v1.yaml
backend/core/knowledge/health_system_card_evidence.py
backend/core/analytics/wave1_subsystem_evidence.py
```

Do not rely on memory.

Every material claim must cite a source path.

---

## Scope

This sprint covers the remaining systems and subsystem candidates needed for beta-readiness, including but not limited to:

```text id="wh3csc"
- launch-core systems not fully implemented
- subsystems named in the User Health to Systems Map
- compiled health-system cards
- subsystem evidence surfaces
- package-backed but uncompiled research areas
- governance-blocked areas
- scoring-blocked areas
- prose/explainer-thin areas
```

Already implemented launch-core cards should still be assessed briefly for depth gaps and carry-forwards, but the focus is the remaining estate.

Implemented so far:

```text id="7dg33t"
- original Wave 1 visible domains
- P1-2 kidney function
- P1-3 blood / iron / oxygen
```

Blocked or unresolved:

```text id="uvj8p9"
- P1-4 thyroid / energy regulation
- hormonal scoring rail
- TSH launch authority
```

Verify all of the above from source files before reporting.

---

## Classification taxonomy

Classify each remaining system/subsystem candidate into one primary readiness state:

```text id="bub9o1"
READY_FOR_RUNTIME_CARD
READY_FOR_COMPILED_CARD_ONLY
RESEARCH_PRESENT_RUNTIME_READY_AFTER_MINOR_WIRING
RESEARCH_PRESENT_UNCOMPILED
RESEARCH_PRESENT_UNMAPPED
COMPILED_NOT_PROMOTED
GOVERNANCE_CONFLICT
SCORING_ARCHITECTURE_BLOCKED
SIGNAL_AUTHORITY_BLOCKED
ROOT_CAUSE_WHY_THIN
PROSE_LAYER_THIN
TEST_ESTATE_THIN
MEDICAL_REVIEW_REQUIRED
NOT_READY
UNKNOWN_INSUFFICIENT_EVIDENCE
```

Use only one primary classification per row, but include secondary blockers where relevant.

Do not overstate readiness.

If evidence is mixed, choose the more conservative classification.

---

## Readiness dimensions

For each system/subsystem candidate, assess these dimensions:

```text id="x4pcuh"
1. Upstream research presence
2. Knowledge Bus package presence
3. Pass 3 / investigation-spec support
4. Signal activation authority
5. Medical-frame identity authority
6. Root-cause / WHY authority
7. Scoring-policy readiness
8. Compiled card evidence presence
9. Pathway/retail explainer readiness
10. Clinician-report / narrative support
11. Test fixture / regression coverage
12. Replay/audit/provenance readiness
13. Layer B runtime integration readiness
14. Layer C / UX dependency
```

Rate each dimension:

```text id="j8tnfi"
Strong
Partial
Weak
Absent
Blocked
Unknown
Not applicable
```

---

## Required deliverable 1 — Adequacy gate report

Create:

```text id="83yjjk"
docs/sprints/beta_readiness/P1-7_research_to_runtime_adequacy_gate.md
```

Use this structure exactly:

```markdown id="gdls58"
# P1-7 — Research-to-Runtime Adequacy Gate for Remaining Systems and Subsystems

## 1. Executive summary
- why this gate was run
- what it found
- whether the issue is isolated or systemic
- which areas are ready
- which areas are blocked
- recommended next sprint

## 2. Programme context
- eight-block beta-readiness programme relationship
- P1-2 kidney outcome
- P1-3 blood / iron / oxygen outcome
- P1-4 thyroid STOP
- P1-5 FT3 reconciliation
- P1-6R scoring architecture decision

## 3. Method
- authority documents read
- directories inspected
- search terms used
- classification taxonomy
- limitations

## 4. Estate-level finding
State whether the medical research estate is:
- research-thin;
- research-rich but unevenly promoted;
- governance-conflicted;
- scoring-blocked;
- prose/explainer-thin;
- test-thin;
- or another evidenced formulation.

## 5. Readiness matrix
Create a table:

| System / subsystem candidate | Primary classification | Upstream research | KB packages | Pass 3/spec support | Signal authority | Frame/root-cause authority | Scoring readiness | Compiled card evidence | Prose/explainer readiness | Test readiness | Runtime integration readiness | Evidence paths | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

Include all material candidates discovered.

## 6. Ready or near-ready candidates
For each candidate that is READY_FOR_RUNTIME_CARD, READY_FOR_COMPILED_CARD_ONLY, or RESEARCH_PRESENT_RUNTIME_READY_AFTER_MINOR_WIRING:
- summarise evidence;
- name missing minor gaps;
- state safe next implementation shape.

## 7. Blocked candidates
Group candidates by blocker:
- governance conflict
- scoring architecture blocked
- signal authority blocked
- medical review required
- root-cause/WHY thin
- prose/explainer thin
- test estate thin
- unknown/insufficient evidence

## 8. Research-to-runtime promotion gaps
Explain where rich research exists but has not been promoted into:
- runtime packages;
- signal intelligence;
- compiled card evidence;
- root-cause/WHY authority;
- scoring rails;
- prose/explainer assets;
- tests;
- provenance/replay surfaces.

## 9. Specific thyroid lesson
Summarise what thyroid revealed about the wider estate:
- FT3 register drift;
- inert scoring rail;
- TSH inactive authority;
- scoring architecture band requirement;
- why this pattern may recur elsewhere.

## 10. Recommended programme sequencing
Recommend the next 3–6 sprint sequence.

Do not default to micro-sprints.
Group work into outcome-based packages with internal STOP gates where appropriate.

## 11. Immediate next sprint recommendation
Name the single next sprint to run.

Include:
- title;
- risk_level;
- change_type;
- expected scope;
- STOP gates;
- why it is the next best action.

## 12. Carry-forwards by beta-readiness block
Group carry-forwards under:
- Block 1 Core health systems model
- Block 2 Subsystems and depth model
- Block 3 Layer B intelligence/prose substrate
- Block 6 Medical safety, research provenance and governance
- Block 7 Auditability, reproducibility and traceability
- Block 5 UX/results page, only where relevant
```

---

## Required deliverable 2 — Machine-readable readiness matrix

Create:

```text id="asf7q6"
docs/sprints/beta_readiness/P1-7_research_to_runtime_readiness_matrix.yaml
```

Use this structure:

```yaml id="y54hpd"
work_id: P1-7
classification_date: <YYYY-MM-DD>
source_authorities:
  - path: <path>
    role: <role>
summary:
  estate_finding: <short finding>
  ready_count: <number>
  blocked_count: <number>
  unknown_count: <number>
  recommended_next_sprint: <title>
candidates:
  - id: <stable_slug>
    name: <human readable name>
    category: system | subsystem | domain | signal_cluster | unknown
    primary_classification: READY_FOR_RUNTIME_CARD | READY_FOR_COMPILED_CARD_ONLY | RESEARCH_PRESENT_RUNTIME_READY_AFTER_MINOR_WIRING | RESEARCH_PRESENT_UNCOMPILED | RESEARCH_PRESENT_UNMAPPED | COMPILED_NOT_PROMOTED | GOVERNANCE_CONFLICT | SCORING_ARCHITECTURE_BLOCKED | SIGNAL_AUTHORITY_BLOCKED | ROOT_CAUSE_WHY_THIN | PROSE_LAYER_THIN | TEST_ESTATE_THIN | MEDICAL_REVIEW_REQUIRED | NOT_READY | UNKNOWN_INSUFFICIENT_EVIDENCE
    dimensions:
      upstream_research: Strong | Partial | Weak | Absent | Blocked | Unknown | Not applicable
      kb_packages: Strong | Partial | Weak | Absent | Blocked | Unknown | Not applicable
      pass3_spec_support: Strong | Partial | Weak | Absent | Blocked | Unknown | Not applicable
      signal_authority: Strong | Partial | Weak | Absent | Blocked | Unknown | Not applicable
      frame_root_cause_authority: Strong | Partial | Weak | Absent | Blocked | Unknown | Not applicable
      scoring_readiness: Strong | Partial | Weak | Absent | Blocked | Unknown | Not applicable
      compiled_card_evidence: Strong | Partial | Weak | Absent | Blocked | Unknown | Not applicable
      prose_explainer_readiness: Strong | Partial | Weak | Absent | Blocked | Unknown | Not applicable
      test_readiness: Strong | Partial | Weak | Absent | Blocked | Unknown | Not applicable
      runtime_integration_readiness: Strong | Partial | Weak | Absent | Blocked | Unknown | Not applicable
    evidence_paths:
      - <path>
    secondary_blockers:
      - <blocker>
    recommended_action: <short action>
```

This matrix is a planning artefact only.

It must not be consumed at runtime.

Do not place it in `backend/ssot/`, `knowledge_bus/compiled/`, or any runtime path.

---

## Required deliverable 3 — Build deliverable register update

At closure, update:

```text id="n4a49o"
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

Append a short entry:

```markdown id="nqjw35"
## P1-7 — Research-to-runtime adequacy gate

**Status:** Complete / Partial / Blocked  
**Date closed:** <YYYY-MM-DD>  
**Programme block(s):** Block 1 Core health systems model; Block 2 Subsystems and depth model; Block 3 Layer B intelligence/prose substrate; Block 6 Medical safety, research provenance and governance; Block 7 Auditability, reproducibility and traceability  

### Delivered / ticked off
- <what this sprint completed against the beta-readiness programme>
- <major adequacy finding or classification outcome>

### Carry-forwards
- <what still needs to be done later>
- <known gaps exposed by this sprint>

### Blockers / risks
- <only material blockers or risks that affect future work>

### Recommended next sprint
- <next work package recommendation>
```

Keep the register entry short.

Do not list every file touched.

Do not duplicate the full report.

---

## Prohibited changes

Do not modify:

```text id="f2koc6"
backend/
frontend/
knowledge_bus/
```

Exception:

```text id="c8pdx5"
You may read files under those directories, but must not change them.
```

Do not modify:

```text id="0fxnr4"
docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md
docs/AUTHORITY_MAP.md
```

Do not modify any source package, compiled card, governance register, scoring policy, runtime code, tests, frontend, Gemini path, parser path, or Pass 3 source material.

Expected product changes are limited to:

```text id="ailajj"
docs/sprints/beta_readiness/P1-7_research_to_runtime_adequacy_gate.md
docs/sprints/beta_readiness/P1-7_research_to_runtime_readiness_matrix.yaml
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

Bus files may change as part of SOP lifecycle.

---

## Validation

Run:

```powershell id="uujhq2"
git diff --stat
git diff --name-only
git status --short
```

Validate the readiness matrix YAML if a YAML validation tool or existing validation pattern is available.

If no YAML validation exists for this planning artefact, at minimum parse it with Python:

```powershell id="h3i59j"
python - <<'PY'
import yaml
from pathlib import Path
path = Path("docs/sprints/beta_readiness/P1-7_research_to_runtime_readiness_matrix.yaml")
data = yaml.safe_load(path.read_text(encoding="utf-8"))
assert data["work_id"] == "P1-7"
assert isinstance(data.get("candidates"), list)
assert data["candidates"], "matrix must contain at least one candidate"
print("P1-7 readiness matrix YAML parsed successfully")
PY
```

No runtime tests are required because this is CONTENT-only.

If any code/runtime/source package/governance register file is changed, stop and report failure.

---

## Required final report

Return:

```text id="ab37eq"
- branch name
- main SHA baseline
- files changed
- estate-level finding
- number of candidates classified
- number ready / near-ready / blocked / unknown
- recommended next sprint
- top 5 blockers
- confirmation no runtime/code/source package/scoring/governance files changed
- validation run and results
- git diff --stat
- git diff --name-only
- git status --short
```

Do not merge until Claude audit, GPT architectural review and human approval.

---

## Acceptance criteria

This sprint is complete only if:

```text id="w08iq3"
1. Adequacy gate report exists at:
   docs/sprints/beta_readiness/P1-7_research_to_runtime_adequacy_gate.md

2. Machine-readable readiness matrix exists at:
   docs/sprints/beta_readiness/P1-7_research_to_runtime_readiness_matrix.yaml

3. Build deliverable register is updated with a short P1-7 entry.

4. The report explicitly answers whether the problem is isolated or broader/systemic.

5. The report classifies all material remaining system/subsystem candidates discovered from the authority documents and repository evidence.

6. Each candidate has a primary classification from the approved taxonomy.

7. Evidence paths are provided for material claims.

8. The matrix distinguishes research presence from runtime promotion readiness.

9. Thyroid is specifically analysed as a warning pattern for wider estate maturity.

10. The report recommends a 3–6 sprint programme sequence and a single immediate next sprint.

11. No runtime code, backend code, frontend code, scoring policy, governance register, Knowledge Bus source package, compiled card, test, Gemini, fallback parser, or Pass 3 source file is changed.

12. Only the expected documentation/planning files and bus files are changed.

13. Matrix YAML parses successfully.

14. Final report includes validation output and clean git status.
```
