# Pre-SOP Prompt Scoping Workflow v0.6.1

## Throughput-Gated Scoping Amendment

**Status:** Adopted amendment  
**Date:** 2026-06-26  
**Applies to:** HealthIQ AI Pre-SOP sprint-planning workflow  
**Purpose:** Prevent pre-SOP advisory work from expanding into a parallel audit cycle. Advisory work must be proportionate, mode-declared, visibly receipt-gated, and smaller than the implementation package it protects.

---

## 1. Problem statement

The Pre-SOP advisory process was introduced to speed up safe development by improving sprint sequencing before formal Automation Bus execution.

The process failed when advisory requests became broader than the implementation sprints they were meant to protect. In particular, advisory prompts began to request broad file reads, multiple grep searches, package comparisons, test discovery, and structured implementation planning. Claude/Cursor then executed these prompts faithfully, often using background/fork agents, consuming more time and credits than the actual build work.

This amendment introduces mandatory throughput controls.

The new rule is simple:

> Advisory work must pass a visible receipt gate before any file is opened, any search is run, or any background/fork agent is launched.

---

## 2. Terminology correction

Do not use the bare phrase **Stage 0** in sprint-planning prompts.

There are two different concepts that were being confused:

| Term | Meaning | When it applies |
|---|---|---|
| Pipeline Advisory Gate | Pre-SOP batch-level sprint sequencing advisory | Before GPT authors a formal SOP prompt |
| Automation Bus Stage 0 Branch Alignment | Formal Automation Bus lifecycle branch-alignment stage | After a governed work package has started |

Use the full names.

Do not say only **Stage 0** unless the context is explicitly clear.

---

## 3. Default path

The default path is now:

1. GPT writes the formal SOP prompt directly from existing authority.
2. The SOP prompt carries bounded uncertainty through candidate-level STOP gates.
3. Claude performs normal Stage D hardening.
4. Cursor executes under Automation Bus SOP.

Do not request advisory work unless a specific advisory trigger exists.

The advisory layer is not mandatory by default.

---

## 4. Mandatory advisory mode declaration

Every advisory request must declare one mode:

```text
Mode: B0
Mode: B1
Mode: B2
```

A `scope-advisory`, `pipeline advisory`, `Stage B`, `throughput check`, `blocker check`, or `pre-SOP` prompt without a declared mode is malformed.

If no mode is declared, Claude/Cursor must stop and respond:

```text
Mode missing. Please redeclare this request as B0, B1 or B2 before I proceed.
```

Claude/Cursor must not infer B2 from prompt complexity.

---

## 5. Mandatory Advisory Receipt Gate

For every prompt containing any of the following:

- `scope-advisory`
- `pipeline advisory`
- `Stage B`
- `throughput check`
- `blocker check`
- `pre-SOP`

Claude/Cursor’s first action must be the Advisory Receipt Gate.

Claude/Cursor must not read files, run grep, launch a fork/background agent, or write an advisory until the receipt gate is complete and passed.

### Required receipt gate output

Claude/Cursor must respond first with:

```text
ADVISORY RECEIPT GATE

Declared mode:
B0 | B1 | B2 | MISSING

Mandatory file reads requested:
[number]

Mandatory search/grep operations requested:
[number]

Structured questions requested:
[number]

Fork/background agent requested:
yes/no

Mode compliance:
PASS | FAIL

Decision:
PROCEED | REJECT_AND_NARROW | REQUIRE_MODE_DECLARATION | REQUIRE_B2_AUTHORISATION
```

Only after this receipt gate passes may advisory work proceed.

Invisible compliance is not sufficient. The receipt gate must be visible to the user/GPT before work begins.

---

## 6. Mode definitions

### B0 — No advisory

Use B0 when:

- the next sprint is already sequenced;
- medical/product/architecture authority already exists;
- uncertainty can be carried safely through STOP gates;
- the sprint pattern is established.

Action:

GPT writes the SOP prompt directly.

No advisory file is produced.

---

### B1 — Lean blocker check

Use B1 when:

- the sprint is already sequenced;
- the scope is mostly known;
- only a small number of blocker facts need checking.

Hard limits:

- maximum 7 mandatory file reads;
- maximum 6 structured questions;
- maximum 3 targeted searches;
- no broad repo discovery;
- no background/fork agent;
- no audit-style advisory;
- no more than one concise blocker note.

If Claude/Cursor needs more than 7 files, it must stop and say:

```text
B1 scope exceeded. These additional files appear necessary: [list]. Please authorise B2 or narrow the questions.
```

B1 may answer only:

- are candidate source/package files present?
- are required artefacts present?
- is domain/SSOT mapping clear?
- is there any hard blocker to GPT writing the SOP?
- what STOP gates must be included?

B1 must not:

- repeat medical review;
- repeat previous audit findings;
- inspect unrelated architecture;
- produce a full implementation plan;
- run broad grep sweeps;
- use a fork/background agent;
- read files “just in case”.

---

### B2 — Full scoping advisory

Use B2 only when explicitly authorised and at least one hard trigger exists.

Valid B2 triggers:

- new programme lane;
- unknown architecture;
- unclear agent ownership;
- conflicting authority documents;
- no identified next sprint;
- multiple competing product directions;
- newly changed medical authority invalidating the prior sequence;
- user explicitly requests full pipeline resequencing.

B2 must still be proportionate.

B2 is not an audit sprint.

A detailed prompt is not implicit B2 authorisation.

---

## 7. Default if ambiguous

If advisory mode is ambiguous, default to B1.

Claude/Cursor must state:

```text
Mode ambiguous; defaulting to B1 lean blocker check.
```

Claude/Cursor must not escalate to B2 without explicit permission.

---

## 8. B1 overrun protection

If a prompt declared as B1 asks for more than B1 allows, Claude/Cursor must stop before doing any work and respond:

```text
B1 scope exceeded. This prompt requests:
- [x] file reads
- [y] searches
- [z] structured questions

This exceeds B1 limits. Please either:
1. narrow the prompt to B1 limits; or
2. explicitly authorise B2.
```

Claude/Cursor must not silently execute the oversized prompt.

---

## 9. Fork/background agent rule

Fork/background agents are forbidden in B1.

Claude/Cursor may use a fork/background agent only when:

- mode is explicitly B2; and
- the user or GPT explicitly authorises fork/background agent use.

A detailed prompt is not implicit fork-agent authorisation.

---

## 10. GPT prompt-authoring rule

GPT must not write a B1 advisory prompt that exceeds B1 limits.

Before giving Claude/Cursor a B1 prompt, GPT must check:

- no more than 7 mandatory file reads;
- no more than 6 structured questions;
- no more than 3 targeted searches;
- no broad repo discovery;
- no fork/background agent;
- no audit-style output requested.

If more is needed, GPT must either:

- reduce the prompt to the true blocker questions; or
- explicitly declare B2 and justify why.

---

## 11. Candidate-level STOP gates are preferred

For candidate-set sprints, do not pre-audit every candidate exhaustively before SOP writing.

If uncertainty can safely be handled inside the formal SOP using candidate-level STOP gates, it must not be moved into advisory.

The SOP should:

- attempt the full candidate set where safe;
- use candidate-level STOP gates;
- allow passing candidates to proceed;
- stop failing candidates independently;
- record stopped candidates as carry-forward.

Pre-SOP advisory should decide only:

- is this sprint safe to attempt?
- is there a whole-sprint blocker?
- which candidate-level STOP gates must be included?

---

## 12. Anti-micro-sprint rule

Before splitting a sprint, Claude/Cursor must state the hard safety reason.

Valid split reasons:

- incompatible risk classes that cannot safely be governed together;
- conflicting file ownership;
- unresolved medical authority;
- unresolved SSOT/domain identity blocking the whole sprint;
- unavoidable sequencing dependency;
- validation scope too large to audit safely.

Invalid split reasons:

- different biomarkers;
- different package folders;
- “more files to read”;
- convenience;
- prompt length;
- desire to fully understand everything before execution.

---

## 13. Pipeline Advisory Gate — exception only

A Pipeline Advisory Gate is allowed only when at least one is true:

- no next sprint is already identified;
- the previous audit explicitly says the next sprint sequence is unresolved;
- the programme is crossing into a new architectural lane;
- the next work requires choosing between multiple competing product directions;
- carry-forwards materially change the build sequence;
- medical authority has newly changed and invalidates the previous sequence;
- the user explicitly requests pipeline resequencing.

A Pipeline Advisory Gate must not be used merely because:

- a sprint is HIGH risk;
- a sprint touches multiple files;
- a sprint has multiple candidates;
- the next sprint requires candidate-level STOP gates;
- Claude/Cursor wants to verify everything before GPT writes the SOP.

---

## 14. P1-26 correction record

The P1-26 pre-SOP advisory overran because the prompt requested B2-level work without a declared mode:

- too many mandatory file reads;
- too many grep/search patterns;
- too many structured questions;
- broad package comparison;
- background/fork-agent execution.

Under v0.6.1, the prompt would have failed the Advisory Receipt Gate before any file was opened.

For P1-26, the valid B1 blocker facts were:

1. all five candidate package paths were present;
2. staged PSI files were present;
3. iron required `_BLOOD_IRON_OXYGEN_LAUNCH_SIGNAL_IDS` update;
4. homocysteine domain mapping was clear and already routed by predicate;
5. no iron candidate required calculated TSAT;
6. no obvious user-facing wording blockers were found.

No further P1-26 advisory work should be run.

---

## 15. Operational rule going forward

Every advisory prompt must pass the Advisory Receipt Gate before work begins.

If the receipt gate fails, stop.

Do not open files.

Do not run grep.

Do not launch agents.

Do not write advisory output.

Ask for mode correction, narrowing, or explicit B2 authorisation.

---

## 17. SOP Prompt Receipt Gate — scope creep stop gate

Every GPT-authored SOP prompt (Stage A concept, formal SOP prompt, or any prompt submitted for Stage D hardening) must pass a visible Prompt Receipt Gate before Claude reads any file, runs any search, or begins hardening.

This gate is separate from and in addition to the Advisory Receipt Gate (§5). Both apply the same visible-first, work-after principle.

### Required receipt gate output

Claude must respond first with:

```text
PROMPT RECEIPT GATE

Front matter complete:
YES | NO — missing fields: [list]

Declared risk_level:
HIGH | STANDARD | LOW

Declared change_type:
CONTENT | BEHAVIOUR | MIXED

Files in scope:
[count] — [list]

Behaviour changes touch Intelligence Core:
YES | NO

Tests listed for BEHAVIOUR changes:
YES | NO | NOT APPLICABLE

Scope proportionality:
PASS | FAIL — [reason if fail]

Scope creep signals:
[list any detected] | NONE

Decision:
ACCEPT | REJECT_AND_RETURN
```

Only after this gate outputs ACCEPT may Claude begin Stage D hardening or any file reading.

### What the gate checks

**Front matter completeness** — all five mandatory fields must be present: `work_id`, `branch`, `risk_level`, `execution_model`, `change_type`. Any missing field is an immediate REJECT.

**Scope proportionality** — the file list must be proportionate to the declared change type and risk level. Triggers a FAIL if:

- a `CONTENT` prompt lists Intelligence Core files (`domain_score_assembler.py`, `signal_evaluator.py`, `backend/core/pipeline/`, `backend/core/analytics/`);
- a `LOW` risk prompt lists more than 5 files in scope;
- a `STANDARD` risk prompt lists more than 10 files in scope without justification;
- the prompt contains open-ended discovery instructions ("also check", "verify all", "read everything in", "any related files").

**Behaviour without tests** — any `BEHAVIOUR` or `MIXED` prompt that lists no tests is a REJECT.

**Advisory-within-SOP** — if the SOP prompt embeds discovery work (broad grep sweeps, candidate package comparison, architecture exploration) it is a REJECT. Discovery belongs in a declared B1 or B2 advisory, not inside a formal SOP prompt.

**Contradictions** — if the declared `change_type` contradicts the listed files (e.g. `CONTENT` but files include signal evaluator or assembler), it is a REJECT.

### On REJECT

Claude must state:

```text
PROMPT RECEIPT GATE — REJECT

Reason: [specific reason]
GPT must fix: [exactly what needs to change]
Do not resubmit until: [condition]
```

Claude must not begin any hardening work on a rejected prompt. Claude must not attempt to fix the prompt itself. The prompt must be returned to GPT for correction and resubmission.

### What the gate does not check

The gate checks form, proportionality, and structural compliance. It does not verify whether listed files exist, whether the stated approach is architecturally correct, or whether STOP gates are medically sound. Those are Stage D hardening responsibilities.

---

## 16. Summary decision

Adopt v0.6.1 as the controlling Pre-SOP throughput amendment.

The intended development rhythm is:

1. Use advisory only by exception.
2. Prefer B0 direct SOP authoring.
3. Use B1 lean blocker checks only where a small blocker question must be answered.
4. Reserve B2 for explicit, justified, full scoping needs.
5. Carry bounded uncertainty through SOP STOP gates rather than pre-auditing the world.

Two mandatory gates protect every entry point:

- **Advisory Receipt Gate (§5)** — applies to all advisory prompts before any advisory work begins.
- **SOP Prompt Receipt Gate (§17)** — applies to all GPT-authored SOP prompts before any hardening begins.

Both gates must produce visible output. Invisible compliance is not sufficient.

