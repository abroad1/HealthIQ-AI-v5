# HealthIQ AI — Pre-SOP Prompt Scoping Workflow: Claude Code Review

**Reviewing:** `healthiq_pre_sop_prompt_scoping_workflow_proposal_v0_1.md`  
**Reviewer:** Claude Code  
**Date:** 2026-06-21

---

## 1. Overall verdict

The proposal is well-reasoned. The problem diagnosis (§1) is accurate — the P1-18 / P1-19 sprint pair is a clear example of a governance cycle that consumed substantial overhead to deliver what was ultimately a single validator policy change and one PSI opt-in. The intent (§2) is right.

The separation from Automation Bus SOP is clean and should be kept that way.

The three things that will determine whether this works or becomes another layer of administration are: whether Stage B produces a standardised output, whether there is a clear trigger for when it runs, and whether the advisory has any teeth if GPT ignores it.

---

## 2. What is working well

**The 5-stage chain (A→B→C→D→E) is structurally correct.** Pre-SOP advisory does not replace hardening. Hardening does not absorb advisory. Cursor does not move until after Stage D. The boundaries are right.

**The 10-question framework for Stage B (§4) covers the right ground.** Agent ownership, blocker classification, throughput justification, safe broadening, and collapse risk are all there. The framing is useful.

**The product-throughput rules (§6) are pragmatic and needed.** The "should not proceed" list is especially valuable as an explicit check on micro-sprinting. This list should survive into whatever formal convention is adopted.

**The Pass 3 non-dilution rule (§8) is important.** This is the product thesis in one paragraph. It should be in the SOP as well, not only in the scoping workflow.

**The agent-boundary rules (§7) are consistent with the existing CLAUDE.md architecture.** No conflict with existing governance.

---

## 3. Issues and recommended changes

### 3.1 Stage B has no canonical output format

The proposal says Claude should "answer" the 10 questions with "concise bullets" and "cite files/lines." In practice, free-form advisory is as variable as a conversation — the quality depends entirely on the context and what Claude happens to emphasise on the day.

Without a canonical output structure, GPT cannot reliably extract the amendments it needs. The advisory becomes a discussion rather than a document.

**Recommended fix:** Define a mandatory lightweight output format for every Stage B advisory:

```
THROUGHPUT VERDICT:   PROCEED | AMEND | SPLIT | DEFER
SCOPE RECOMMENDATION: [what is in / conditionally in / out]
AGENT ASSIGNMENT:     [primary agent / handoff gates if mixed]
BROADENING OPP.:      [specific candidates with repo evidence]
HARD STOP GATES:      [blockers that block the whole sprint]
CANDIDATE STOP GATES: [blockers that block individual candidates only]
GPT AMENDMENTS:       [numbered, specific, actionable]
```

The advisory should end with `GPT AMENDMENTS` as a numbered list of exact changes GPT must make before writing the formal SOP prompt. This is what GPT actually needs.

---

### 3.2 Stage B has no mandatory repo-read step

The proposal says Claude should "answer" questions about the sprint concept. But the most common failure mode is that both GPT and Claude are reasoning from carry-forward documents and memory rather than from current repo state.

P1-17 identified ferritin_high as needing a production host package. P1-18 correctly carried this forward. But at Stage A / Stage B, if no one explicitly reads `knowledge_bus/packages/pkg_kb52c_ferritin_high*/`, the advisory will not catch that the production host is still absent. This is exactly the kind of missed broadening opportunity the proposal is trying to prevent.

**Recommended fix:** Stage B must begin with a mandatory repo-read step before any advisory is issued. Claude must read:

- any relevant carry-forward YAML from prior sprints;
- the current state of candidate files/packages in repo;
- the current validator state (activation-readiness report if applicable).

Without this, Stage B is an opinion not grounded in current repo reality. Add to the Stage B advisory prompt: *"Before answering, read the relevant carry-forward manifests and check the current repo state of all candidate files/packages."*

---

### 3.3 The 10-question list is missing the most important broadening question

The questions cover agent, scope, blockers, and collapse risk. But they do not ask:

> *Does an inherited carry-forward from a prior sprint artificially restrict this scope, and can that restriction be lifted with small remedial work inside the same sprint?*

This is the question that would have caught the ferritin_high situation: the production host packages are missing, but the staged PSI are validator-PASS and could be opted in if the host packages were created first. The gap was detectable. It was not flagged because no question in Stage B was looking for it.

**Recommended fix:** Add question 11 to both §4 Stage B and the prompt in §5:

> 11. Does any inherited carry-forward restriction from a prior sprint artificially narrow the candidate set, and can it be cleared with targeted remediation inside the same sprint or as a same-day micro-action before formal scoping?

---

### 3.4 No trigger rules — Stage B will be skipped when most needed

The proposal does not say when Stage B is mandatory versus optional. Without explicit trigger rules, Stage B will be applied inconsistently — applied to easy sprints where it adds little value, and skipped for complex sprints where it would be most useful.

**Recommended fix:** Add a short trigger section:

**Stage B is mandatory when any of the following apply:**
- The sprint involves a candidate set (more than one candidate to adjudicate).
- Two or more carry-forward items from a prior sprint feed into this sprint.
- The risk level is HIGH.
- The proposed sprint is primarily adjudication, report, or classification rather than implementation.
- The prior sprint generated a carry-forward manifest.

**Stage B is optional (lightweight throughput check only) when:**
- The sprint is a targeted single-action fix with known scope.
- No carry-forward items from prior sprints are in scope.
- The agent assignment is unambiguous.

This prevents Stage B becoming reflexive overhead on simple sprints.

---

### 3.5 No feedback loop if GPT ignores the advisory

The proposal says GPT "uses Claude's advisory to write the real `latest_cursor_prompt.md` content." But it does not say what happens if GPT's formal SOP prompt significantly departs from the advisory.

Currently, if GPT ignores Stage B and writes a narrow prompt anyway, Stage D hardening would accept it (hardening checks the prompt against SOP rules, not against Stage B advice). The governance cost of the bad scoping is then paid in wasted hardening cycles and prompt amendments.

**Recommended fix:** Stage D hardening should include one additional check that is not currently in the hardening schema:

> *Does the scope of this prompt materially contradict the Stage B advisory? If so, flag the specific departure and require GPT to confirm it was intentional before hardening proceeds.*

This can be lightweight — not a blocker by default, but a required acknowledgement. It gives the pre-SOP workflow teeth without making it another gate.

---

### 3.6 The advisory prompt in §5 invites long responses

The current prompt asks 10 open-ended questions with no word/length constraint. This will produce long advisory responses that GPT then has to parse for the specific amendments it needs.

**Recommended fix:** Add an explicit constraint to the §5 prompt:

```
Keep the total advisory under 600 words.
Use the standard output format: THROUGHPUT VERDICT, SCOPE RECOMMENDATION,
AGENT ASSIGNMENT, BROADENING OPP., HARD STOP GATES, CANDIDATE STOP GATES, GPT AMENDMENTS.
GPT AMENDMENTS must be a numbered list of exact actionable changes.
```

Short, structured output is more useful to GPT than a long advisory. The goal is a document GPT reads in 60 seconds and converts into a better formal prompt.

---

### 3.7 Consider two advisory modes

Not every sprint concept needs the same depth of advisory. A sprint that is clearly well-scoped needs only a throughput check. A sprint with a large candidate set or complex agent boundary needs the full treatment.

**Recommended fix:** Define two advisory modes:

**Mode 1 — Throughput check (5 minutes):** Used when the sprint concept is already reasonably well-defined. Claude reads the relevant carry-forward and answers only: is this worth a full SOP cycle, and is the scope appropriately bounded? Output: THROUGHPUT VERDICT + GPT AMENDMENTS only.

**Mode 2 — Full scoping advisory (20-30 minutes):** Used when the sprint concept is early-stage, has a candidate set, or inherits complex carry-forwards. Claude performs mandatory repo reads and answers all questions. Output: full canonical format.

The invoker specifies the mode in the Stage B prompt. This prevents the workflow from defaulting to maximum overhead on every sprint.

---

### 3.8 §9 Expected benefits — one missing benefit

The expected benefits list is accurate but omits one that matters for long-term governance:

> *Prevents the Automation Bus audit trail from being diluted by sprints that deliver little product value — keeping the historical record meaningful.*

Every sprint that goes through the full SOP cycle creates audit artefacts, gate evidence, audit summaries, and carry-forward manifests. If many of these sprints are micro-scope, the audit trail becomes noisy and the meaningful architectural decisions are harder to locate. Stage B should protect the quality of the audit trail, not just delivery throughput.

---

## 4. Questions from §10 answered directly

**1. Is this separation from Automation Bus SOP clean?**  
Yes. The firewall at Stage B (no JSON, no hardening, no kernel) is correctly placed and should not be changed.

**2. Are the roles of GPT and Claude clear enough?**  
For Claude yes — advisory is clearly defined. For GPT, the role is less prescriptive. The proposal says GPT "uses" the advisory but doesn't constrain how. The canonical output format (§3.1 above) fixes this.

**3. Should the pre-hardening advisory produce a standard output format?**  
Yes — this is the most important improvement. See §3.1. Without it, the advisory is a conversation, not a governance document.

**4. What safeguards are missing?**  
(a) No mandatory repo-read before advisory (§3.2). (b) No trigger rules (§3.4). (c) No feedback loop into Stage D (§3.5). (d) No constraint on advisory length (§3.6).

**5. How can this workflow better maximise safe product throughput?**  
By adding question 11 (§3.3) and the mandatory repo-read step (§3.2). These are the two changes most likely to catch safe broadening opportunities that would otherwise be missed.

**6. How can we prevent it becoming another layer of administration?**  
Trigger rules (§3.4) and the two-mode advisory structure (§3.7) are the key controls. Stage B only runs when the sprint concept genuinely needs it, and runs at the depth the sprint concept actually requires.

**7. What should be changed before we adopt it as a working convention?**  
In priority order:
1. Define the canonical Stage B output format (§3.1).
2. Add the mandatory repo-read step to Stage B (§3.2).
3. Add question 11 to the advisory (§3.3).
4. Add trigger rules (§3.4).
5. Add the advisory length/format constraint to the §5 prompt (§3.6).

---

## 5. Suggested invocation phrase

The §5 prompt is good but should have a short invocation phrase that Claude can recognise unambiguously as a Stage B advisory request (distinct from a formal hardening request):

```
scope-advisory: [work-theme or proposed work_id] — pre-SOP only, no hardening
```

This mirrors the hardening phrase (`harden work_id: [ID] — verify source content...`) and makes it clear which mode Claude is in. It also prevents accidental triggering of formal hardening behaviour.

---

## 6. Summary of recommended changes

| # | Change | Priority |
|---|---|---|
| 1 | Define canonical Stage B output format with GPT AMENDMENTS as final section | High |
| 2 | Add mandatory repo-read step before Stage B advisory | High |
| 3 | Add question 11 — inherited carry-forward restriction check | High |
| 4 | Add trigger rules (mandatory vs. optional) | High |
| 5 | Add length/format constraint to §5 advisory prompt | Medium |
| 6 | Add two-mode advisory structure (throughput check vs. full scoping) | Medium |
| 7 | Add Stage D consistency check against Stage B advisory | Medium |
| 8 | Add audit-trail quality to §9 Expected Benefits | Low |
| 9 | Define formal invocation phrase (`scope-advisory: ...`) | Low |
