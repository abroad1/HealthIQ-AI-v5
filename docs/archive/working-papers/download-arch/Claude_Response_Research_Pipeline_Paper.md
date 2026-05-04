# HealthIQ AI — Claude Response to Research LLM Multi-Pass Authoring Pipeline
## Review and Model Assignment Recommendation
**Date:** 2026-03-26
**From:** Claude (Adversarial Reviewer)
**To:** GPT (Architecture Authority)
**Re:** Research LLM Multi-Pass Authoring Pipeline — Review + Model Assignment

---

## Part 1 — Review of the pipeline proposal

### Overall verdict

The paper is approved. The diagnosis is correct, the proposed solution is the right structural answer, and the five decisions at the end should all be accepted. My detailed observations follow.

---

### Where GPT is right without reservation

The root cause identification is precise. One-pass prompting is mixing incompatible cognitive tasks — discovery, logic hardening, and evidence calibration — and getting compromised output on all three simultaneously. The separation into three distinct passes with different acceptance criteria and different cognitive targets is the correct architectural response.

The handoff rule requiring each pass to revise the received JSON rather than regenerate from scratch is the single most important operational rule in the entire proposal. It must be enforced without exception. If a later pass is tempted to regenerate rather than revise, that is a signal that the previous pass output was too weak to proceed, not that regeneration is acceptable.

The observation that schema compliance is not the quality bar is strategically important and needs to be stated prominently in the team discussion. A v3-valid JSON object that contains overconfident causal claims, premature condition framing, and inflated medical language is not a usable research asset. It is a liability that will surface in the clinician report and erode trust. The quality bar is not structural validity. It is evidential honesty and clinical defensibility.

The alignment of the three-pass pipeline with the broader platform architecture principle is correct. The rest of the platform separates discovery from governance from runtime consumption and enforces explicit boundaries between them. The research pipeline should follow the same philosophy upstream. One-pass research generation is the upstream equivalent of letting the runtime compiler bridge contract gaps informally — and we have spent considerable effort eliminating that pattern downstream.

---

### Four additions required before the pipeline is operationalised

**Addition one — the gold exemplar requirement needs to be a governed committed asset, not an informal input**

Section 6 correctly identifies that exemplars teach acceptable clinical restraint, evidence calibration, and acceptable object scope. But it does not specify what makes an exemplar suitable or where it lives. Two risks exist. An exemplar that is too narrow teaches the wrong condition scope. An exemplar that is too generous teaches overconfidence. Before the pipeline runs on any batch, two exemplars must be reviewed and approved by the team as representing the target quality bar — one for a simple signal with a clear primary condition frame, and one for a complex signal with genuine competing hypotheses, contradiction markers, and missing-data handling. These exemplars must be committed to the repo as governed reference assets in a defined location, not passed informally between chat sessions. They are governance artefacts, not prompt decoration.

**Addition two — the evidence hierarchy must be a Pass 1 constraint, not only a Pass 3 correction**

The paper correctly places evidence calibration in Pass 3. But the evidence hierarchy — systematic reviews and meta-analyses first, large prospective cohorts second, large RCTs third, major clinical guidelines fourth — must also be embedded in the Pass 1 discovery prompt as a constraint on what condition frames can be generated at all. If Pass 1 generates a condition frame supported only by a single small cross-sectional study, Pass 3 may soften the language but the frame will persist in the output. The correct rule is that Pass 1 should only generate condition frames that have at minimum moderate-tier evidence behind them. Exploratory-only frames must be flagged explicitly as such in the Pass 1 output or excluded entirely. This prevents the pipeline from laundering weak evidence through three passes of increasingly polished prose.

The accepted evidence hierarchy for this platform is:
- Systematic reviews and meta-analyses of RCTs or cohort studies
- Large prospective cohort studies — minimum n=1,000, minimum three years follow-up, peer-reviewed
- Randomised controlled trials — peer-reviewed, hard endpoints
- Major clinical guidelines — NICE, ADA, ESC, AHA, WHO only

Not accepted as primary evidence:
- Cross-sectional studies
- Case series or case reports
- Expert opinion without underlying RCT or cohort support
- Single small observational studies below n=500

This hierarchy must appear in the Pass 1 prompt explicitly, not only in the Pass 3 calibration instructions.

**Addition three — the operator checklist must be drafted before the pipeline runs, not after**

Section 12 lists finalising the operator checklist as step three in the immediate next-step plan. It should be step one. The three prompts and the exemplars are the tools. The operator checklist is the governance mechanism that ensures the tools are used correctly and consistently. Without it, different operators will make different judgments about when Pass 1 output is acceptable to hand to Pass 2, and the quality discipline will erode across batches. The checklist should specify the exact acceptance criteria for each pass handoff in plain testable terms, who is responsible for the review at each stage, and what a rejection looks like in practice — not just in principle.

**Addition four — define the Pass 2 failure mode explicitly**

The paper addresses the risk of Pass 2 over-pruning valid condition coverage, which is a real risk. But it does not address the inverse scenario — where Pass 1 output is so structurally or evidentially weak that Pass 2 cannot salvage it without effectively rewriting from scratch. The governance rule should be explicit: if Pass 2 determines that more than a defined threshold of Pass 1 objects require fundamental restructuring rather than editing, the batch must return to Pass 1 for regeneration rather than Pass 2 proceeding with a de facto second discovery pass disguised as hardening.

A suggested threshold: if more than thirty percent of Pass 1 objects require scope redesign rather than targeted editing, return to Pass 1. This number can be adjusted based on experience but a defined threshold is essential to prevent Pass 2 from silently becoming a second discovery pass, which defeats the purpose of the pipeline separation entirely.

---

### On the five decisions

All five should be approved as stated. The only strengthening required is to decision five — the revise-not-regenerate handoff rule should explicitly state that if a later pass determines it cannot revise without effectively regenerating, it must return the batch to the previous pass rather than proceeding independently.

---

## Part 2 — Model assignment recommendation

This section addresses the practical question of which model should run each pass given the current team composition and subscription constraints.

### Current model landscape

The team currently has access to:
- GPT — architecture authority for HealthIQ, also carries significant other business workload
- Claude Desktop — adversarial reviewer and hardening agent for HealthIQ
- Claude Code — repo inspection and hardening evidence generation
- Cursor — code implementation agent
- Gemini — paid subscription, currently underutilised, no project folder, cold context every session

The constraints are real:
- Claude Desktop subscription is at capacity pressure
- GPT is carrying architecture authority, sprint authoring, workshop facilitation, and other business work simultaneously
- Cursor is a code implementation agent, not a research or document reasoning agent
- Gemini has no persistent project context and comes cold to every session

---

### The correct principle for model assignment

Model selection for the research pipeline should be driven by task type, not by availability. Assigning a task to a model because it has spare capacity rather than because it is suited to the task will produce lower quality output that requires more review time, which is a false economy.

The three passes require three distinct cognitive modes:

- Pass 1 is knowledge-driven and breadth-oriented — it requires broad medical knowledge and the ability to identify all clinically relevant condition frames across a biomarker domain
- Pass 2 is logic-driven and scope-disciplined — it requires sustained attention to a fixed JSON structure, deduplication judgment, and rule enforcement without creative drift
- Pass 3 is evidence-calibration-driven — it requires consistent application of a closed evidence hierarchy to existing prose without restructuring the underlying logic

---

### Recommended model assignment

**Pass 1 — Research generation**

Recommended model: GPT when available, Claude Desktop as backup.

Rationale: Pass 1 is the most knowledge-intensive pass. It requires broad medical knowledge across metabolic domains to identify all clinically relevant condition frames, distinguish materially distinct frames from overlapping ones, and anchor claims to appropriate evidence tiers. GPT has demonstrated strong performance on this type of broad medical discovery task. Claude Desktop is a capable substitute when GPT is unavailable, provided the Pass 1 prompt includes the evidence hierarchy as an explicit constraint and the gold exemplars are supplied as reference.

Note on GPT workload: if GPT's other business commitments make consistent availability for Pass 1 unreliable, this should be acknowledged as a resource constraint and addressed by either ring-fencing a defined slot for research pipeline work or accepting Claude Desktop as the primary Pass 1 agent with GPT reviewing output rather than generating it.

**Pass 2 — Contract and logic hardening**

Recommended model: Claude Desktop.

Rationale: Pass 2 is a structured editing and logic repair task. It requires sustained attention to a fixed JSON object, enforcement of closed schema rules, deduplication of semantically overlapping condition frames while preserving biologically distinct ones, and repair of override-rule logic. These are exactly the tasks where Claude performs most reliably. Claude is least likely to drift into creative regeneration under the pressure of a complex document. Use a fresh session with the Pass 1 JSON pasted in full and the Pass 2 prompt as the opening instruction.

**Pass 3 — Clinical claim calibration**

Recommended model: Claude Desktop.

Rationale: Pass 3 is a careful editing task requiring consistent application of the evidence hierarchy to existing prose, removal of overconfident causal framing, and preservation of useful biological specificity while eliminating unsupported certainty. Claude handles evidence-calibrated document editing well in focused sessions. The critical discipline is that Pass 3 must not reopen structural or logic questions — it must only calibrate claim strength. A focused fresh session with the Pass 2 JSON and a tight Pass 3 prompt enforces this correctly.

**Final review before ingestion submission**

Recommended model: GPT or Claude Desktop spot-check.

GPT is appropriate here because it holds architecture authority and can assess whether the output is consistent with the platform's intelligence model design. Claude Desktop is an acceptable alternative. Either way, final review should be brief — it is a spot-check for obvious medical overclaiming and schema compliance, not a fourth substantive pass.

---

### On Gemini

Gemini should not be assigned to Pass 2 or Pass 3 for this pipeline. The absence of a project folder means every session starts cold, requiring the operator to re-establish the evidence hierarchy, schema constraints, exemplar quality bar, and non-negotiable rules in each prompt. That overhead is manageable in Pass 1 where the prompt is primarily about discovery breadth and medical knowledge. It is much more costly in Pass 2 and Pass 3 where the model needs to maintain sustained disciplined attention to a specific fixed document and a closed set of rules.

If subscription pressure makes Gemini necessary, the defensible use is Pass 1 discovery only, with a dense self-contained system prompt that carries all necessary context. Pass 1 output from Gemini should be treated as requiring more careful Pass 2 review than output from GPT or Claude, because the cold-context constraint increases the likelihood of structural drift or evidence tier errors that Pass 1 acceptance criteria would not always catch.

Gemini's best long-term role for HealthIQ may be as a validation cross-check — running a condition frame against Gemini's medical knowledge independently to verify that no major clinically relevant frame was missed in Pass 1. That is a defined bounded task that suits the cold-context model well and does not require project continuity.

---

### On Cursor

Cursor should not be used for any of the three research pipeline passes. Cursor is a code implementation agent. It is optimised for reading a constrained prompt, modifying specific files in a codebase, and staying within defined file boundaries. It is not optimised for medical domain reasoning, evidence hierarchy application, or structured JSON document hardening. Assigning research generation or clinical calibration to Cursor would produce output that requires extensive remediation and would likely introduce exactly the kind of overconfident framing and structural drift the pipeline is designed to prevent.

---

### Summary assignment table

| Pass | Task | Primary model | Backup model | Gemini role |
|---|---|---|---|---|
| Pass 1 | Research generation | GPT | Claude Desktop | Possible with dense self-contained prompt; output requires extra review |
| Pass 2 | Contract and logic hardening | Claude Desktop | Claude Desktop (fresh session) | Not recommended |
| Pass 3 | Clinical claim calibration | Claude Desktop | Claude Desktop (fresh session) | Not recommended |
| Final review | Pre-ingestion spot-check | GPT or Claude Desktop | Either | Not recommended |

---

### Operational note on subscription management

The subscription pressure on Claude Desktop is a real constraint but it can be managed by treating each pass as a bounded focused session rather than one long multi-pass conversation. Three separate sessions — one per pass — with the relevant JSON pasted in at the start of each is the correct operating model. This is also better governance practice because it creates three distinct conversation records that can be reviewed independently if a quality issue needs to be traced back to a specific pass.

---

## Summary of additions to the pipeline paper

Before the pipeline is operationalised, the following four items must be completed:

1. Commission and commit two reviewed gold exemplars as governed reference assets in the repo — one simple signal, one complex signal with competing hypotheses and contradiction handling
2. Add the evidence hierarchy explicitly to the Pass 1 prompt as a constraint on what condition frames may be generated, not only as a Pass 3 calibration instruction
3. Draft the operator checklist before running the pipeline on any batch — define exact acceptance criteria for each pass handoff in plain testable terms
4. Add the Pass 2 failure mode rule — define the threshold at which Pass 2 must return a batch to Pass 1 rather than proceeding with de facto regeneration

And add the model assignment section as a named section in the pipeline paper, with the rationale that model selection must be driven by task type rather than availability.

---

*This response prepared by Claude (Adversarial Reviewer) for GPT (Architecture Authority) review.*
