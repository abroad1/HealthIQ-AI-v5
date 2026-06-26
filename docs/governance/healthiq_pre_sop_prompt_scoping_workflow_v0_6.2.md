# Pre-SOP Prompt Scoping Workflow v0.6.2
status: ACTIVE
date: 2026-06-26
supersedes: healthiq_pre_sop_prompt_scoping_workflow_v0_6.1.md

---

## DEFAULT PATH

1. GPT writes SOP directly from existing authority.
2. Claude runs Stage D hardening.
3. If wrong: Claude issues REJECT_AND_RETURN with exact corrections.
4. GPT resubmits once with corrections.
5. Stage D proceeds.

Advisory is not the default. Do not request advisory unless a trigger below applies.

---

## MODES

Every advisory prompt must declare one mode. No mode = malformed. Stop and request redeclaration.

### B0 — No advisory
GPT writes SOP directly. No advisory file produced. Use when:
- next sprint already identified
- sprint pattern established (PSI opt-in, signal activation, compiled card, etc.)
- unknowns are file paths, schema shape, loader behaviour, risk class, test placement

### B1A — Pipeline Throughput Review
Use at batch boundaries or when audit says next sprint is unresolved.
Answers: what sprint next, next 3–5 sequence, safe combinations, true blockers.
Must not inspect implementation code except one targeted read if a sequencing blocker cannot otherwise be classified.
Reads: BUILD_DELIVERABLE_REGISTER + latest audit summary + latest carry-forward + latest pipeline advisory.
Output written to: `automation_bus/latest_pipeline_advisory.md`

### B1B — Lean Blocker Check
Use when sprint is sequenced, scope mostly known, one small blocker fact needed before SOP authoring.

B1 hard limits (both B1A and B1B):
- max 7 file reads
- max 6 structured questions
- max 3 targeted searches
- no broad repo discovery
- no fork/background agent
- no implementation plan
- no advisory artefact unless explicitly requested

If limits exceeded: stop and say exactly which files/questions were over limit. Ask to narrow, authorise B2, or move to Stage D.

### B2 — Strategic/programmatic decisions only
Requires explicit authorisation. Valid triggers:
- no next sprint identifiable from register and B1 cannot resolve it
- multiple competing product/programme directions require a decision
- architecture decision is not inferable from current repo state
- agent ownership conflict not resolvable by SOP role rules
- conflicting authority documents create a governance decision (not a file-path question)
- clinical/medical authority conflict changes what can safely be built
- user explicitly requests full pipeline resequencing

B2 is NOT triggered by: new lane, HIGH risk, multiple files, multiple candidates, unknown code architecture, desire to verify everything before SOP authoring.

B2 output written to: `automation_bus/latest_scope_advisory.md` only if the conclusion will not be invalidated by immediate Stage D code inspection. If the conclusion is conditional on code facts, do not write it as controlling scope.

---

## ADVISORY RECEIPT GATE

Required before any file read, grep, agent launch, or advisory output. Must be visible.

```
ADVISORY RECEIPT GATE
Declared mode: B0 | B1 | B2 | MISSING
Mandatory file reads requested: [n]
Mandatory searches requested: [n]
Structured questions requested: [n]
Fork/background agent requested: yes/no
Repo/code-discovery requested: yes/no
Programme sequencing decision requested: yes/no
Mode compliance: PASS | FAIL
Decision: PROCEED | REJECT_AND_NARROW | REQUIRE_MODE_DECLARATION | REQUIRE_B2_AUTHORISATION | SEND_TO_STAGE_D
```

SEND_TO_STAGE_D when: the prompt is asking code/repo-discovery questions answerable by Stage D hardening.

---

## SOP PROMPT RECEIPT GATE

Required before Claude reads any file or begins hardening. Must be visible.

```
PROMPT RECEIPT GATE
Front matter complete: YES | NO — missing fields: [list]
Declared risk_level: HIGH | STANDARD | LOW
Declared change_type: CONTENT | BEHAVIOUR | MIXED
Files in scope: [count] — [list]
Behaviour changes touch Intelligence Core: YES | NO
Tests listed for BEHAVIOUR changes: YES | NO | NOT APPLICABLE
Scope proportionality: PASS | FAIL — [reason]
Advisory duplication detected: YES | NO
Scope creep signals: [list] | NONE
Decision: ACCEPT | REJECT_AND_RETURN
```

Mandatory front matter fields: work_id, branch, risk_level, execution_model, change_type. Any missing = REJECT.

Scope proportionality FAIL if:
- CONTENT prompt lists Intelligence Core files (domain_score_assembler.py, signal_evaluator.py, backend/core/pipeline/, backend/core/analytics/)
- LOW risk prompt lists more than 5 files
- STANDARD risk prompt lists more than 10 files without justification
- prompt contains open-ended discovery ("also check", "verify all", "read everything in")

BEHAVIOUR or MIXED with no tests listed = REJECT.

On REJECT: state exact reason, exactly what GPT must fix, condition for resubmission. Do not begin hardening. Do not fix the prompt. Return to GPT.

---

## STAGE D REJECTION FORMAT

```
STAGE D HARDENING VERDICT: REJECT_AND_RETURN
Reason: [precise defect]
Evidence: [file/path/line]
Corrected classification:
  risk_level:
  change_type:
  execution_model:
GPT must resubmit with:
  - [exact file scope correction]
  - [exact test correction]
  - [exact STOP gate correction]
  - [exact out-of-scope correction]
Do not run advisory. Do not execute implementation.
```

Do not convert hardening into a scope advisory. Do not request a new advisory unless the blocker is genuinely strategic/programmatic and cannot be resolved by file inspection.

---

## WHAT BELONGS IN STAGE D, NOT B2

These questions go to Stage D hardening, never to B2 advisory:
- What files does this compiler/loader read?
- What YAML/schema format is required?
- Which Python files must change?
- Is this CONTENT, BEHAVIOUR, or MIXED based on code?
- Does the repo already support this?
- What tests are needed?
- What directory contains the relevant runtime artefacts?
- Does a current function already route this signal/domain?
- What exact schema fields are required?
- Which regression tests currently exist?

---

## ANTI-MICRO-SPRINT RULE

Do not split a sprint without a hard safety reason. State the reason explicitly.

Valid split reasons: incompatible risk classes; conflicting file ownership; unresolved medical authority; unresolved SSOT/domain identity blocking the whole sprint; unavoidable sequencing dependency; validation scope too large to audit safely; one part requires a different formal authority approval.

Invalid split reasons: different biomarkers; different package folders; more files to read; prompt length; desire to fully understand everything before execution; code architecture unknown but verifiable during Stage D; sprint is HIGH risk; sprint has multiple candidates.

Candidate-level STOP gates inside one sprint are preferred over splitting into multiple sprints.

---

## AMBIGUITY DEFAULTS

Mode ambiguous → default B1. State: "Mode ambiguous; defaulting to B1 lean blocker check."
Request is asking code/repo-discovery questions → state: "This is Stage D hardening work. Recommend GPT writes the SOP and sends to Stage D."
Do not escalate to B2 without explicit permission.
