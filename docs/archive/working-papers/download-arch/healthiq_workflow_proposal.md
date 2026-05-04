# HealthIQ AI — Build Workflow Problem Statement & Recommended Automation Architecture

**Status:** Proposal for review and agreement  
**Author:** Claude (Anthropic) — based on workflow analysis sessions  
**Date:** March 2026

---

## 1. The Problem

### What the current workflow looks like

The HealthIQ AI build pipeline uses three AI agents plus automated scripts and CI, each operating at a different level of the stack:

| Agent | Role |
|---|---|
| GPT | Strategic architecture, contract definition, Cursor prompt writing |
| Cursor | Code execution, file changes, local test runs |
| Claude Desktop | Strategic oversight, prompt quality review, architecture direction |
| Claude Code | Diff review, code quality audit, CI and schema inconsistency detection |
| Local scripts | Verification gates (baseline, three-layer, collision, golden runner) |
| CI / GitHub Actions | Authoritative merge enforcement |
| You (Founder) | Product direction, invariant decisions, merge authority |

This multi-agent model is intentional and correct. The safety of the system comes from no single agent having full authority. That must be preserved.

### What is actually broken

**You are the wire connecting every agent.**

90% of your time is spent on three manual relay tasks that repeat for every work package:

1. **Copying GPT's prompt into Cursor** — you are a clipboard
2. **Manually running PowerShell tests to verify Cursor's work** — you are a test runner, because Cursor has a demonstrated tendency to self-report tests as passing when they have not
3. **Copying test failures and Claude Code diff findings back to GPT** — you are a postman

None of these three tasks require your judgement. They are pure information relay. But because they go through you, every work package requires your active involvement in technically complex areas that are outside your domain expertise.

### Why this is a risk, not just an inconvenience

- Cursor self-reporting false passes has already caused production issues that were only caught by manual testing
- Decisions are being made in chat windows with no persistent audit trail
- The workflow is dependent on your availability and stamina, not on deterministic process
- As the sprint complexity grows, the relay burden grows with it

---

## 2. The Root Cause

**There is no shared workspace between the agents.**

Right now your chat windows are the communication channel. Information only moves between agents when you physically carry it. The agents cannot read each other's outputs directly — everything is mediated through you.

The fix is not more intelligence. It is a shared location in the repo that all agents read from and write to, removing you as the relay for everything except genuine product decisions.

---

## 3. Recommended Workflow

### The target state in plain terms

GPT writes into the repo. Cursor reads from the repo, executes, and writes evidence back into the repo. Claude Code reads the repo, reviews the diff, runs verification, and writes its findings into the repo. You receive one summary per work package and make one decision: **approve merge or not.**

You stop carrying information. The repo carries it.

### The three agents and their consolidated roles

**GPT** remains the strategic architecture agent. It writes Cursor prompts and architecture contracts. In the new workflow it writes these directly into a work package folder in the repo rather than into a chat window for you to copy.

**Cursor** remains the executor. It reads the prompt from the work package folder, makes the change, runs the gate script automatically as its final step, and writes the raw evidence output (not its interpretation of it) into the work package folder. It never self-reports pass or fail — it always produces raw terminal output.

**Claude Code** consolidates the roles currently split between Claude desktop and Claude Code. It reads the repo directly so it has the diff, the spec, the evidence, and the codebase all in context. It replaces the need to paste diffs into a chat window. It writes its review findings into the work package folder. It can also perform the strategic oversight and prompt quality checking currently done in Claude desktop, because it has full repo access and can be asked strategic questions directly.

**You** approve the work package spec before anything starts. You review the consolidated summary at the end. You make the merge decision. That is all.

### The work package folder

Every unit of work gets a folder in the repo:

```
/workpackages/WP_025/
    spec.md              ← GPT writes this; you approve before Cursor starts
    cursor_prompt.md     ← GPT writes this; pulled directly into Cursor
    evidence.json        ← Cursor writes this; raw gate script output
    claude_review.md     ← Claude Code writes this; diff + quality findings
    gpt_audit.md         ← GPT writes this; decision based on evidence + review
    status.md            ← Current state: APPROVED / IN PROGRESS / PASS / NO-GO
```

Nothing travels through you. You read `status.md` and make one decision.

### The gate script

A single script — `golden_gate_local.py` — that Cursor runs as the mandatory final step of every work package. It:

- Runs all verification scripts in sequence
- Captures raw terminal output (not interpreted results)
- Writes structured output to `evidence.json` in the work package folder
- Prints PASS or FAIL
- Exits non-zero on any failure

Cursor's prompt always ends with: **run `golden_gate_local.py`, paste the raw output verbatim, do not summarise, do not interpret.**

This eliminates false self-reporting. The evidence is the output, not Cursor's opinion of the output.

### CI remains the merge authority

CI runs the same gate scripts independently. Local evidence is for fast feedback during development. CI evidence is authoritative for merge. If they ever disagree, CI wins.

---

## 4. What You Keep and Never Automate

- Approving the work package spec before Cursor starts
- Overriding any agent recommendation
- Merge authority
- Any decision touching clinical meaning, product direction, or SSOT expansion
- The decision to add new systems, new canonical IDs, or change pipeline architecture

These are the decisions that require your judgement. Everything else is mechanical and should be automated.

---

## 5. What Changes and What Stays the Same

| | Today | Proposed |
|---|---|---|
| GPT prompt delivery to Cursor | You copy-paste | GPT writes to repo folder; Cursor reads directly |
| Test verification | You run manually in PowerShell | Cursor runs gate script; writes evidence to folder |
| Diff review | Claude Code in PowerShell; you paste findings to GPT | Claude Code reads repo directly; writes to folder |
| Strategic oversight | Claude desktop via chat; you paste context | Claude Code with repo access; reads everything directly |
| GPT audit | You paste evidence into GPT | GPT reads evidence file from folder |
| Your decisions per work package | ~20 relay actions + decisions | 2 decisions: approve spec, approve merge |
| Audit trail | Chat history (ephemeral) | Work package folders (versioned, in repo) |
| Agent authority | No single agent | No single agent (preserved) |

---

## 6. Implementation Sequence

These should be done in order. Do not skip ahead.

**Step 1 — Fix Cursor self-reporting immediately (no infrastructure needed)**  
Append a standard evidence pack footer to every Cursor prompt from today. Cursor must paste raw terminal output, not a summary. This fixes the most dangerous problem with zero infrastructure cost.

**Step 2 — Build `golden_gate_local.py`**  
One script that runs all verification in sequence and writes `evidence.json`. Cursor runs this as the final step of every work package automatically.

**Step 3 — Establish work package folder structure**  
Agree the folder schema. GPT starts writing prompts and specs to folders. Claude Code starts writing reviews to folders. The folder becomes the shared workspace.

**Step 4 — Configure Claude Code as the consolidated oversight agent**  
Claude Code replaces Claude desktop for strategic oversight and diff review. Because it has repo access it does not need context pasted into it — it reads directly. This eliminates the application switching and the remaining copy-paste.

**Step 5 — CI artifact enforcement**  
CI uploads its own evidence JSON on every run. Merge requires CI PASS. Local evidence is advisory only.

---

## 7. What This Is Not

This is not removing human oversight. You remain the decision authority.  
This is not trusting any single AI more. The multi-agent safety model is preserved.  
This is not automating product or clinical decisions. Those stay with you.

This is removing the mechanical relay work that currently sits between the agents and goes through you by default because there is no other path for information to travel.

---

## 8. Open Questions for Agreement

Before implementation begins, the following need explicit agreement:

1. Is GPT the confirmed author of all Cursor prompts, or should Claude Code take that role for some work packages?
2. Does Claude Code fully replace Claude desktop, or are there strategic conversations better suited to a chat interface?
3. Who has authority to create a new work package — you only, or can GPT propose one for your approval?
4. What is the maximum number of files Cursor is ever permitted to touch in a single work package without a STOP and escalation?

---

*This document should be reviewed by GPT for architecture alignment before any implementation begins.*
