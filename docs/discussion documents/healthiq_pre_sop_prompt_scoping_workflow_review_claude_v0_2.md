# Pre-SOP Scoping Workflow v0.2 — Claude Code Review

**Date:** 2026-06-21

---

## Overall verdict

Structurally much better than v0.1. The trigger rules, mode split, throughput rules, and invocation phrases are all right. The core design works.

The problem is the document itself violates §17. It is 532 lines across 21 sections. A working convention for reducing admin overhead should not be a 21-section governance document. If someone has to read 532 lines before they can run a scope advisory, the workflow has already lost.

Target: 10 sections, under 200 lines. Everything else belongs in CLAUDE.md or nowhere.

---

## What to cut

**§3 — Non-negotiable product principle (14 bullets)**  
This is CLAUDE.md §1/2/3 restated. Do not maintain two copies. Replace with one sentence: *"Pass 3 research is the canonical medical authority. The scoping workflow must protect its richness. See CLAUDE.md §§1-3."* Cut the rest.

**§9 — 11 required Stage B questions**  
The canonical output format (§8) already implies most of these. If the format is filled correctly, questions 1-10 are answered by definition. The only question worth keeping explicitly is #11 (inherited carry-forward restriction check) because it is the least obvious and most likely to be skipped. Cut questions 1-10. Keep 11 as a short note under §8: *"Always check whether an inherited carry-forward artificially narrows the candidate set and whether targeted in-sprint remediation could lift it."*

**§10 — Stage B evidence cache (14-bullet list)**  
The concept is right but the spec is premature. A working convention does not need a 14-field cache schema. Collapse to two sentences: *"Where practical, write advisory findings to `automation_bus/latest_scope_advisory.md` with file:line citations. Stage D can treat cited structural findings as inherited rather than re-reading them."* That is the entire rule. The 14 bullets are implementation detail that can emerge from use.

**§11 and §12 — What Stage D may/must inherit or re-read**  
Both are already captured in §20 (Stage D preamble), which is the only place Cursor/Claude needs to see this. Having it in two places means two things to maintain and two things to read. Delete §11 and §12. §20 is the authority.

**§13 — Advisory staleness**  
One bullet in §20: *"If advisory is older than 48 hours or relevant files changed since it was written, re-verify structural claims."* Not a section.

**§14 — Stage D consistency check**  
One sentence in §20, not a section. Already drafted adequately there.

**§16 — Agent-boundary rules (full table)**  
Already in CLAUDE.md §5/6. Maintaining a second copy will diverge. Replace with: *"Agent boundaries are governed by CLAUDE.md §§5-6. Scoping must assign ownership before the formal prompt is written."* Cut the table.

**§18 — Expected benefits**  
Delete. Benefits are either obvious from the design or they are not. A list of hoped-for outcomes adds no working value.

---

## What to keep, tightened

**§5 (trigger rules)** — Right. Keep as-is. This is the most used section.

**§6 (modes)** — Right. Mode 1 under 300 words, Mode 2 under 600 words. Keep the word limits — they are the primary anti-admin control.

**§7 (mandatory repo-read step)** — Right. Keep. Shorten the bullet list to three items: carry-forward manifests, candidate files/packages, validator/readiness state if applicable. The ADR/SOP reads should be on-demand, not mandatory.

**§8 (canonical output format)** — Mostly right, but `EVIDENCE CACHE` as a named output section is premature for a working convention. Remove it from the format. The evidence ends up in `latest_scope_advisory.md` as a by-product of the advisory, not as a separately headed section Cursor has to fill in. Removing it keeps the output format lean.

**§15 (throughput rules)** — Tight and correct. Keep exactly as-is.

**§17 (documentation discipline)** — Right. Keep. Apply it to this document too.

**§19 (invocation template)** — Right. Keep. This is the practical interface.

**§20 (Stage D preamble)** — Right. Absorb the staleness rule and consistency check here rather than as separate sections.

---

## One missing thing

The document still does not say what happens if Stage B is skipped when it was mandatory. Without a consequence, the trigger rules are advisory rather than enforceable. One sentence is enough: *"If Stage B was mandatory and was skipped, Claude should flag this during Stage D hardening before proceeding."* This gives the trigger rules teeth without adding a process step.

---

## Target structure for v0.3

1. Problem (5 lines)
2. Intent (5 lines)
3. Non-negotiable product principle (3 lines + reference to CLAUDE.md)
4. Workflow — 5 stages, one paragraph each
5. Trigger rules
6. Modes (1 and 2, with word limits)
7. Mandatory repo-read step (3 bullets)
8. Canonical output format (the box, minus EVIDENCE CACHE)
9. Throughput rules
10. Documentation discipline
11. Invocation template (Stage B)
12. Stage D preamble (absorbing staleness, consistency check, inherit/fresh rules)

That is the whole workflow. Anything not in those 12 sections is either in CLAUDE.md or is documentation overhead the workflow is supposed to prevent.
