---
work_id: P1-8
branch: work/P1-8-scoring-lab-range-engine
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# P1-8 — Scoring Lab-Range Engine

## Objective

Implement the scoring-engine architecture required before thyroid / hormonal scoring can proceed safely.

P1-6R established that the current scoring architecture does not safely support lab-range-only thyroid scoring because biomarker bands are structurally required in the system orchestration path.

This sprint must add a governed, generic, lab-range-relative biomarker scoring capability that does not require hardcoded global/default biomarker bands.

This is an enabling architecture sprint inside the eight-block beta-readiness programme.

It must update the beta-readiness build register at closure.

---

## Strategic purpose

HealthIQ AI’s non-negotiable policy is:

```text
Use lab-provided reference ranges for biomarker interpretation where available.
Do not substitute global/default reference ranges.
```

The current scoring engine creates a blocker for thyroid and any other marker where scoring should be relative to the lab-provided reference range rather than hardcoded scoring bands.

This sprint must fix that engine-level limitation.

It must not turn thyroid on.

It must not add thyroid cards.

It must not activate thyroid signals.

It must not add TSH, FT3 or FT4 to production scoring policy unless the implementation is explicitly limited to a non-runtime test fixture.

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
git switch -c work/P1-8-scoring-lab-range-engine
```

Do not proceed if the working tree is dirty.

Confirm the Automation Bus active work package/state file if required by SOP.

---

## Required prerequisites on main

These files must exist on `main`:

```text
docs/sprints/beta_readiness/P1-6R_thyroid_scoring_architecture_recovery.md
docs/architecture/ADR-THYROID-SCORING-LAB-RANGE-ARCHITECTURE-1.md
docs/sprints/beta_readiness/P1-7_research_to_runtime_adequacy_gate.md
docs/sprints/beta_readiness/P1-7_research_to_runtime_readiness_matrix.yaml
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

If any are missing, stop and report:

```text
P1-8 prerequisite beta-readiness evidence is not present on main. P1-8 must not proceed.
```

---

## First authority documents

Read these first, in this order:

```text
docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md
docs/sprints/beta_readiness/P1-6R_thyroid_scoring_architecture_recovery.md
docs/architecture/ADR-THYROID-SCORING-LAB-RANGE-ARCHITECTURE-1.md
docs/sprints/beta_readiness/P1-7_research_to_runtime_adequacy_gate.md
docs/sprints/beta_readiness/P1-7_research_to_runtime_readiness_matrix.yaml
docs/architecture/ADR-LAYER-BOUNDARY-RECONCILIATION-1.md
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

P1-6R and the thyroid scoring ADR are the immediate architectural trigger documents.

Do not contradict them.

---

## Files to inspect

Inspect before modifying anything:

```text
backend/ssot/scoring_policy.yaml
backend/core/scoring/
backend/tests/unit/test_scoring_rules.py
backend/tests/
docs/architecture/
docs/intelligence/
docs/testing/
```

Search for:

```text
scoring_policy
BiomarkerRule
calculate_biomarker_score
reference_range
lab_range
range_low
range_high
bands
direction_class
system_weight
min_biomarkers_required
biomarkers
unit
```

If scoring code is elsewhere, locate it and inspect it before changing anything.

---

## Critical scope boundary

This sprint may change scoring-engine architecture and directly related tests/docs only.

It must not implement thyroid runtime behaviour.

Do not modify:

```text
backend/core/analytics/domain_score_assembler.py
backend/core/analytics/domain_narrative_wave1.py
backend/core/analytics/wave1_subsystem_evidence.py
backend/core/dto/persisted_replay_contract_v1.py
backend/core/knowledge/health_system_card_evidence.py
knowledge_bus/compiled/
frontend/
Gemini paths
fallback parser paths
Knowledge Bus source packages
Pass 3 source material
```

Do not create:

```text
- thyroid domain row
- thyroid compiled card
- thyroid narrative helpers
- thyroid subsystem evidence wiring
- thyroid DTO/replay contract entry
- thyroid frontend rendering
- thyroid Gemini prompt
- thyroid production scoring rail activation
```

Do not activate:

```text
- FT3 low
- FT3 high
- FT4 high
- FT4 low
- TSH high
- TSH low
- thyroid antibodies
```

---

## Required architecture outcome

Implement a generic scoring-policy capability that allows a biomarker rule to be valid without hardcoded bands when lab-provided ranges are available.

The exact implementation must follow the existing codebase pattern, but the intended capability is:

```text
A biomarker can be scored relative to its lab-provided reference range without requiring policy-level optimal/normal/borderline/high/very_high/critical bands.
```

The design must preserve existing band-based scoring for all existing markers.

No existing scored biomarker behaviour may drift.

---

## Permitted implementation directions

Cursor must inspect the current implementation and choose the smallest safe change.

Acceptable patterns may include, depending on existing architecture:

```text
- adding an explicit lab-range-relative scoring mode to BiomarkerRule
- adding a bandless rule type in scoring policy loading
- allowing selected biomarker rules to omit bands when rule_type/lab_range_mode declares that behaviour
- separating rule construction requirements from band-based scoring requirements
- adding schema validation for lab-range-only rules
- adding tests proving bandless lab-range rules work and band-based rules remain unchanged
```

The chosen approach must be explicit, not implicit.

Do not silently allow all bandless biomarkers.

A bandless/lab-range-only rule must require an explicit declaration such as a rule type, scoring mode, or equivalent governed field.

---

## Prohibited implementation directions

Do not:

```text
- add placeholder bands
- add 0.0–1.0 pseudo-bands in clinical units
- add common textbook/lab/NICE/NHS/ATA/BTA/ETA ranges
- add thyroid-specific scoring thresholds
- add thyroid markers to production scoring_policy.yaml
- change non-thyroid biomarker weights
- change existing scoring outputs for existing markers
- weaken schema validation globally
- make missing bands silently acceptable for all biomarkers
- bypass unit checks
- disable existing tests rather than fixing architecture
```

---

## Required STOP conditions

Stop and report a blocker if:

```text
- the existing scoring engine cannot be safely extended without broad rewrite;
- the required change would create output drift in existing scoring systems;
- schema expectations are too unclear to modify safely;
- bandless lab-range scoring cannot be made explicit and governed;
- tests cannot prove existing scored markers remain unchanged;
- implementation would require thyroid scoring policy activation;
- implementation would require domain assembler / DTO / compiled card changes.
```

If stopped, produce the report and register entry as Blocked / Partial. Do not make speculative code changes.

---

## Required design rules

The final implementation must satisfy:

```text
1. Existing band-based scoring remains supported.
2. Existing biomarker outputs are unchanged unless explicitly tested and justified.
3. Lab-range-only scoring is opt-in, explicit and governed.
4. Lab-provided ranges are used at scoring time.
5. No global/default range is introduced.
6. No placeholder bands are introduced.
7. Unit checks remain meaningful.
8. Absence of lab range must fail closed or return insufficient-data behaviour, not fabricate a score.
9. Directionality handling remains explicit.
10. The code path must be testable without activating thyroid in production.
```

---

## Production scoring policy rule

Do not enable the hormonal rail in production during this sprint.

Do not add TSH / FT3 / FT4 to production `backend/ssot/scoring_policy.yaml` unless all of the following are true:

```text
- the entries are only for a non-runtime test fixture or isolated test policy;
- they do not affect production scoring;
- the final report clearly explains why production behaviour is unaffected.
```

Expected default:

```text
backend/ssot/scoring_policy.yaml remains unchanged except where a generic schema/version/comment field is absolutely required by the new architecture.
```

If the engine can be changed and tested without changing production scoring policy, prefer that.

---

## Required tests

Add or update targeted tests proving the new scoring architecture.

Tests must prove:

```text
1. A lab-range-only biomarker rule can be constructed without bands when explicitly declared.
2. A lab-range-only biomarker can be scored using the lab-provided reference range.
3. Missing lab range fails closed or returns insufficient data.
4. Placeholder bands are not required.
5. Existing band-based biomarker rules still construct and score as before.
6. Existing scoring policy still validates.
7. Existing non-thyroid scoring behaviour is not changed.
8. Thyroid production scoring is not activated.
9. No TSH / FT3 / FT4 production bands exist.
10. Directionality is respected for low-only and high-only concerns where applicable.
```

Use test fixtures if needed.

Do not add runtime thyroid domain tests because no thyroid domain is being implemented in this sprint.

---

## Required deliverable 1 — Implementation report

Create:

```text
docs/sprints/beta_readiness/P1-8_scoring_lab_range_engine.md
```

Use this structure:

```markdown
# P1-8 — Scoring Lab-Range Engine

## 1. Summary
- what architecture blocker was addressed
- whether lab-range-only scoring is now supported
- whether production thyroid scoring remains blocked or unblocked
- what changed

## 2. Authority baseline
- P1-6R decision
- ADR-THYROID-SCORING-LAB-RANGE-ARCHITECTURE-1
- P1-7 adequacy finding
- relevant layer boundary constraints

## 3. Existing scoring architecture before P1-8
- how band-based scoring worked
- where bands were required
- why thyroid was blocked

## 4. Design decision
- chosen lab-range-only rule pattern
- why this pattern is explicit and governed
- why it avoids global/default ranges
- why it preserves existing scoring

## 5. Runtime/code changes
- files changed
- functions/classes changed
- schema/policy changes, if any
- production scoring policy impact

## 6. Safety boundaries
Confirm:
- no placeholder bands
- no hardcoded global/default ranges
- no thyroid signal activation
- no thyroid domain card
- no compiled thyroid card
- no DTO/domain row
- no frontend/Gemini/fallback parser
- no Knowledge Bus source packages or Pass 3 artefacts changed

## 7. Tests and validation
- tests added/updated
- commands run
- results
- any limitations

## 8. Effect on thyroid programme
State:
- whether hormonal scoring rail can now be safely enabled in a later sprint
- whether P1-4 retry is still blocked by TSH authority or other blockers
- what must happen next

## 9. Carry-forwards
- hormonal rail enablement
- TSH package authority
- thyroid card retry
- other systems that can benefit from lab-range-only scoring

## 10. Recommended next sprint
Recommend the next sprint with rationale.
```

---

## Required deliverable 2 — ADR

Create:

```text
docs/architecture/ADR-SCORING-LAB-RANGE-ONLY-BIOMARKER-RULES-1.md
```

Use this structure:

```markdown
# ADR-SCORING-LAB-RANGE-ONLY-BIOMARKER-RULES-1

## Status
Accepted / Blocked

## Context
Explain:
- lab-provided reference ranges are authoritative;
- P1-6 failed by adding hardcoded thyroid bands;
- P1-6R proved bands were structurally required before this sprint;
- P1-8 introduces or blocks a governed lab-range-only scoring path.

## Decision
State whether lab-range-only biomarker rules are now supported.

If supported, describe the explicit rule pattern.

If blocked, explain why.

## Non-negotiable constraints
- no global/default ranges
- no placeholder bands
- no diagnostic thresholds
- opt-in explicit rule type/mode
- fail-closed when lab range is absent
- preserve existing band-based scoring
- no signal activation from scoring rules
- no Layer C/Gemini/frontend reasoning

## Consequences
- what future scoring-policy sprints may do
- what remains blocked
- how this affects thyroid
- how this affects other systems

## Files reviewed
List files reviewed.

## Files changed
List files changed.
```

Use `Status: Accepted` only if the engine capability has been implemented and tested.

Use `Status: Blocked` if the sprint stops before implementation.

---

## Required deliverable 3 — Build deliverable register update

At closure, update:

```text
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

Append a short entry:

```markdown
## P1-8 — Scoring lab-range engine

**Status:** Complete / Partial / Blocked  
**Date closed:** <YYYY-MM-DD>  
**Programme block(s):** Block 1 Core health systems model; Block 3 Layer B intelligence/prose substrate; Block 6 Medical safety, research provenance and governance; Block 7 Auditability, reproducibility and traceability  

### Delivered / ticked off
- <what this sprint completed against the beta-readiness programme>
- <major scoring architecture outcome>

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

Do not duplicate the full implementation report.

---

## Expected changed file categories

Expected if implementation proceeds:

```text
backend/core/scoring/
backend/tests/
docs/sprints/beta_readiness/P1-8_scoring_lab_range_engine.md
docs/architecture/ADR-SCORING-LAB-RANGE-ONLY-BIOMARKER-RULES-1.md
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
automation_bus/
```

`backend/ssot/scoring_policy.yaml` should usually remain unchanged.

If it changes, the final report must explain exactly why and prove:

```text
- no production thyroid markers were added
- no production thyroid bands were added
- no non-thyroid weights changed
- no existing scores drifted
```

No other product files should change.

---

## Prohibited changes

Do not modify:

```text
backend/core/analytics/domain_score_assembler.py
backend/core/analytics/domain_narrative_wave1.py
backend/core/analytics/wave1_subsystem_evidence.py
backend/core/dto/persisted_replay_contract_v1.py
backend/core/knowledge/health_system_card_evidence.py
knowledge_bus/compiled/
knowledge_bus packages
Pass 3 source material
frontend/
Gemini paths
fallback parser paths
```

Do not update:

```text
docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md
docs/AUTHORITY_MAP.md
```

---

## Validation

Run:

```powershell
git diff --stat
git diff --name-only
git status --short
```

Run relevant scoring tests, at minimum:

```powershell
python -m pytest backend/tests/unit/test_scoring_rules.py
```

Run any new or updated tests created by this sprint.

If broader scoring tests exist, run the smallest relevant suite covering scoring policy loading, biomarker rule construction, and scoring behaviour.

If tests cannot be run, state why.

If tests fail because of this sprint, fix or report blocked.

---

## Required final report

Return:

```text
- branch name
- main SHA baseline
- scoring architecture decision
- whether lab-range-only biomarker rules are now supported
- files changed
- whether backend/ssot/scoring_policy.yaml changed
- whether any production thyroid scoring was added
- whether any hardcoded/placeholder bands were added
- tests run and results
- whether existing band-based scoring remains unchanged
- whether thyroid domain/card remains blocked or partially unblocked
- recommended next sprint
- confirmation no domain assembler / DTO / compiled card / frontend / Gemini / fallback / KB source / Pass 3 files changed
- git diff --stat
- git diff --name-only
- git status --short
```

Do not merge until Claude audit, GPT architectural review and human approval.

---

## Acceptance criteria

This sprint is complete only if:

```text
1. Implementation report exists at:
   docs/sprints/beta_readiness/P1-8_scoring_lab_range_engine.md

2. ADR exists at:
   docs/architecture/ADR-SCORING-LAB-RANGE-ONLY-BIOMARKER-RULES-1.md

3. The sprint either implements and tests a governed lab-range-only biomarker rule path, or stops with a clear blocker.

4. No hardcoded global/default reference ranges are introduced.

5. No placeholder clinical-unit bands are introduced.

6. Existing band-based scoring remains supported.

7. Existing non-thyroid scoring behaviour does not drift.

8. Missing lab-provided range fails closed or returns insufficient-data behaviour.

9. No thyroid signal is activated.

10. No thyroid domain card, compiled card, DTO row, subsystem evidence, narrative helper, frontend rendering or Gemini path is created.

11. No Knowledge Bus source packages or Pass 3 artefacts are changed.

12. Any scoring engine change is covered by targeted tests.

13. Build deliverable register is updated with a short P1-8 entry.

14. Final report states whether hormonal scoring rail can now be safely enabled in a later sprint.

15. Final report includes validation output and clean git status.
```
